"""
FastAPI OpenAPI 스펙을 Notion 페이지로 동기화하는 스크립트

사전 준비:
1. Notion Integration 생성: https://www.notion.so/my-integrations
2. Integration을 대상 페이지에 공유 (Share → Invite)
3. .env 파일에 아래 항목 설정:
   - NOTION_API_KEY: Integration 토큰
   - NOTION_PAGE_ID: 문서를 생성할 Notion 페이지 ID
   - OPENAPI_URL: FastAPI 서버 URL (기본값: http://localhost:8000/openapi.json)

실행:
   uv run docs/sync_notion.py
"""

import json
import os
import sys
from pathlib import Path

import requests
from notion_client import Client

# 프로젝트 루트의 .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
OPENAPI_URL = os.getenv("OPENAPI_URL", "http://localhost:8000/openapi.json")

METHOD_EMOJI = {
    "get": "🔵",
    "post": "🟢",
    "patch": "🟡",
    "put": "🟠",
    "delete": "🔴",
}

HTTP_METHOD_COLORS = {
    "get": "blue",
    "post": "green",
    "patch": "yellow",
    "put": "orange",
    "delete": "red",
}


# ── 블록 헬퍼 ──────────────────────────────────────────────

def rich_text(content: str, bold: bool = False, code: bool = False) -> dict:
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {"bold": bold, "code": code},
    }


def heading_block(content: str, level: int = 2) -> dict:
    t = f"heading_{level}"
    return {"object": "block", "type": t, t: {"rich_text": [rich_text(content)]}}


def text_block(content: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [rich_text(content)] if content else []},
    }


def divider_block() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def callout_block(method: str, path: str) -> dict:
    color = HTTP_METHOD_COLORS.get(method.lower(), "default")
    emoji = METHOD_EMOJI.get(method.lower(), "🔗")
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                rich_text(f"{method.upper()}", bold=True, code=True),
                rich_text(f"  {path}", bold=True),
            ],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": f"{color}_background",
        },
    }


def table_block(headers: list[str], rows: list[list[str]]) -> dict:
    def make_cell(text: str) -> list:
        return [rich_text(text)]

    header_row = {
        "object": "block",
        "type": "table_row",
        "table_row": {"cells": [make_cell(h) for h in headers]},
    }
    data_rows = [
        {
            "object": "block",
            "type": "table_row",
            "table_row": {"cells": [make_cell(c) for c in row]},
        }
        for row in rows
    ]

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": True,
            "has_row_header": False,
            "children": [header_row] + data_rows,
        },
    }


# ── OpenAPI 스펙 파싱 헬퍼 ────────────────────────────────

def resolve_ref(ref: str, spec: dict) -> dict:
    """$ref 문자열을 실제 스키마로 변환"""
    name = ref.split("/")[-1]
    return spec.get("components", {}).get("schemas", {}).get(name, {})


def get_schema_fields(schema: dict, spec: dict) -> list[tuple[str, str, str, str]]:
    """스키마에서 (필드명, 타입, 필수여부, 설명) 목록 반환"""
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], spec)

    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])
    rows = []

    for field_name, field_info in properties.items():
        if "$ref" in field_info:
            field_info = resolve_ref(field_info["$ref"], spec)

        field_type = field_info.get("type", "")
        if not field_type and "anyOf" in field_info:
            types = [t.get("type", "") for t in field_info["anyOf"] if t.get("type") != "null"]
            field_type = " | ".join(filter(None, types)) or "any"

        enum_values = field_info.get("enum", [])
        if enum_values:
            field_type += f" ({', '.join(str(e) for e in enum_values)})"

        required = "✅" if field_name in required_fields else "—"
        description = field_info.get("description", "")
        rows.append((field_name, field_type, required, description))

    return rows


# ── 엔드포인트 블록 생성 ──────────────────────────────────

def build_endpoint_blocks(method: str, path: str, info: dict, spec: dict) -> list[dict]:
    blocks = []

    # 제목 callout
    blocks.append(callout_block(method, path))

    # 요약 설명
    if summary := info.get("summary"):
        blocks.append(text_block(summary))

    # Path / Query Parameters 표
    parameters = info.get("parameters", [])
    if parameters:
        blocks.append(heading_block("Parameters", level=3))
        rows = []
        for param in parameters:
            name = param.get("name", "")
            location = param.get("in", "")
            required = "✅" if param.get("required") else "—"
            schema = param.get("schema", {})
            param_type = schema.get("type", "")
            description = param.get("description", "")
            rows.append([name, location, param_type, required, description])
        blocks.append(table_block(["이름", "위치", "타입", "필수", "설명"], rows))

    # Request Body 표
    request_body = info.get("requestBody", {})
    if request_body:
        blocks.append(heading_block("Request Body", level=3))
        content = request_body.get("content", {})
        for _, media_info in content.items():
            schema = media_info.get("schema", {})
            fields = get_schema_fields(schema, spec)
            if fields:
                blocks.append(table_block(["필드", "타입", "필수", "설명"], fields))

    # Responses 표
    responses = info.get("responses", {})
    if responses:
        blocks.append(heading_block("Responses", level=3))
        status_rows = []
        for status_code, resp_info in responses.items():
            description = resp_info.get("description", "")
            # 응답 스키마 필드 추출
            resp_content = resp_info.get("content", {})
            schema_fields = []
            for _, media_info in resp_content.items():
                schema = media_info.get("schema", {})
                schema_fields = get_schema_fields(schema, spec)

            status_rows.append([status_code, description])

        blocks.append(table_block(["상태 코드", "설명"], status_rows))

        # 200 응답 스키마가 있으면 별도 표로
        ok_resp = responses.get("200", {})
        ok_content = ok_resp.get("content", {})
        for _, media_info in ok_content.items():
            schema = media_info.get("schema", {})
            fields = get_schema_fields(schema, spec)
            if fields:
                blocks.append(heading_block("Response Body", level=3))
                blocks.append(table_block(["필드", "타입", "필수", "설명"], fields))

    blocks.append(divider_block())
    return blocks


# ── Notion 동기화 ─────────────────────────────────────────

def clear_page_blocks(notion: Client, page_id: str):
    result = notion.blocks.children.list(block_id=page_id)
    for block in result.get("results", []):
        notion.blocks.delete(block_id=block["id"])


def append_blocks(notion: Client, page_id: str, blocks: list[dict]):
    for i in range(0, len(blocks), 100):
        notion.blocks.children.append(block_id=page_id, children=blocks[i:i + 100])


def sync_to_notion(spec: dict, notion: Client, root_page_id: str):
    paths = spec.get("paths", {})
    info = spec.get("info", {})

    print("루트 페이지 초기화 중...")
    clear_page_blocks(notion, root_page_id)
    append_blocks(notion, root_page_id, [
        heading_block(f"📄 {info.get('title', 'API Docs')}", level=1),
        text_block(f"Version: {info.get('version', '')}"),
        divider_block(),
    ])

    tag_pages: dict[str, str] = {}

    for path, methods in paths.items():
        for method, endpoint_info in methods.items():
            tags = endpoint_info.get("tags", ["기타"])
            tag = tags[0]

            if tag not in tag_pages:
                print(f"태그 페이지 생성: {tag}")
                page = notion.pages.create(
                    parent={"page_id": root_page_id},
                    properties={
                        "title": {"title": [rich_text(f"📁 {tag}")]}
                    },
                )
                tag_pages[tag] = page["id"]
                append_blocks(notion, page["id"], [
                    heading_block(f"{tag} API", level=1),
                    divider_block(),
                ])

            print(f"  엔드포인트 추가: {method.upper()} {path}")
            blocks = build_endpoint_blocks(method, path, endpoint_info, spec)
            append_blocks(notion, tag_pages[tag], blocks)

    print("\n✅ Notion 동기화 완료!")


def main():
    if not NOTION_API_KEY:
        print("❌ 환경변수 NOTION_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)
    if not NOTION_PAGE_ID:
        print("❌ 환경변수 NOTION_PAGE_ID가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"OpenAPI 스펙 가져오는 중: {OPENAPI_URL}")
    try:
        spec = fetch_openapi_spec(OPENAPI_URL)
    except Exception as e:
        print(f"❌ OpenAPI 스펙 로드 실패: {e}")
        sys.exit(1)

    notion = Client(auth=NOTION_API_KEY)
    sync_to_notion(spec, notion, NOTION_PAGE_ID)


def fetch_openapi_spec(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    main()
