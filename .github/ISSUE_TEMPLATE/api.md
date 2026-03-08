## Title
[API] {기능명}

---

## Description
기능 설명

예:
게시글 목록을 조회하는 API 구현

---

## Requirements
- 게시글 목록 조회
- 최신순 정렬
- 페이지네이션 지원
- 삭제된 게시글 제외

---

## API Spec

### Endpoint
```
GET /api/posts
```

### Query Params

| name | type | required | description |
|-----|-----|-----|-----|
| page | int | N | 페이지 번호 |
| size | int | N | 페이지 사이즈 |

### Request
```json
{}
```

### Response
```json
{
  "content": [
    {
      "id": 1,
      "title": "게시글 제목",
      "author": "user1",
      "createdAt": "2026-03-08T10:00:00"
    }
  ],
  "page": 0,
  "size": 10,
  "totalElements": 120
}
```

### Error
| code | description |
|-----|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 500 | Internal Server Error |

---

## Acceptance Criteria
- pagination 정상 동작
- 삭제된 게시글 조회되지 않음
- 응답 정상 반환

---

## Tasks
- [ ] Repository 구현
- [ ] Service 구현
- [ ] Controller 구현
- [ ] API 테스트 작성