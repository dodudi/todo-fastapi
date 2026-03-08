---
name: API Feature
about: API 기능 개발
title: "[API] "
labels: feature
assignees: ""
---

## Description

기능 설명

예:
게시글 목록 조회 API 구현

---

## Requirements

- 기능1
- 기능2
- 기능3

---

## API Spec

### Endpoint

```
GET /api/...
```

### Query Params

| name | type | required | description |
|------|------|----------|-------------|
| page | int  | N        | 페이지 번호      |
| size | int  | N        | 페이지 사이즈     |

### Request

```json
{}
```

### Response

```json
{}
```

### Error

| code | description           |
|------|-----------------------|
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 500  | Internal Server Error |

---

## Acceptance Criteria

- 기능 정상 동작
- 예외 처리 구현
- 테스트 통과

---

## Tasks

- [ ] Repository 구현
- [ ] Service 구현
- [ ] Controller 구현
- [ ] Test 작성