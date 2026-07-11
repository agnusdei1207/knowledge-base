---
title: "OpenAPI·Swagger (OpenAPI Swagger)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 204
extra:
  question_no: "204"
  exam_status: "미출제"
---

## 미리 알고가기

- OpenAPI Specification은 소스 코드와 무관하게 HTTP API의 기능을 기술하는 언어 독립적 인터페이스 명세임
- OpenAPI Description은 JSON 또는 YAML 문서이며 API 요청·응답 본문의 형식을 JSON·YAML로 제한하지 않음
- Swagger는 현재 OpenAPI 문서를 편집·표시·코드 생성·호출하는 도구군을 뜻하며 OpenAPI와 대체 관계가 아님
- `info.version`은 설명 대상 API 문서의 버전이고 `openapi`는 문서를 해석할 OAS 규격 버전임
- Design-First는 명세에서 구현을 생성하고 Code-First는 구현·주석에서 명세를 추출하므로 계약 기준 위치가 다름

## 작성 근거(검토용)

- OpenAPI와 Swagger는 표준·문서·도구 역할을 구분하고 계약 객체와 Design-First·Code-First 흐름으로 설명함
- 비교표는 두 개발 방식의 기준 산출물·변경 시작점·검증·동기화 위험·적합 조건을 대비함
- 외부 API와 내부 서비스 문서는 계약 위반 건수·생성 성공률·문서 불일치 건수로 검증함

## Ⅰ. 개요

- **정의/개념**: OpenAPI는 HTTP API의 경로·연산·매개변수·본문·응답·보안 계약을 기술하는 표준이고 Swagger는 해당 문서를 작성·시각화·코드 생성·시험하는 도구 생태계임
- **배경/필요성**: API 제공자와 소비자가 구현 코드 없이 호출 계약을 해석하고 문서·Stub·검증·시험 산출물을 같은 정의에서 생성하려면 기계 판독 가능한 명세가 필요함

## Ⅱ. 특징

- `paths`와 Operation이 URL·HTTP 메서드·Parameter·Request Body·Response를 정의함
- `components`가 재사용 Schema·Parameter·Response·Security Scheme을 보관하고 `$ref`가 이를 참조함
- Server·Security Requirement·Tag·Example·Link로 접속점·인증 방식·분류·예시·연산 관계를 기술함
- Linter와 계약 시험이 누락 응답·스키마 불일치·호환성 파괴를 구현 병합 전에 검사함
- Swagger Editor·UI·Codegen 같은 도구는 OAS 문서를 편집·렌더링하고 클라이언트·서버 골격을 생성함
- 명세와 구현을 함께 변경하지 않으면 생성 코드·문서·실제 응답 사이에 계약 불일치가 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | Design-First | Code-First |
|:---|:---|:---|
| 기준 산출물 | OpenAPI Description | 구현 코드·프레임워크 주석 |
| 변경 시작점 | 경로·Schema·Response 계약 수정 | Handler·DTO·Annotation 수정 |
| 구현 연결 | 명세에서 Stub·Interface 생성 | 실행 코드에서 명세 추출 |
| 선행 검증 | Lint·호환성 검사 후 구현 | 빌드·실행 후 생성 명세 검사 |
| 동기화 위험 | 생성 코드의 수동 수정과 명세 미반영 | 런타임 동작·주석·추출 명세 불일치 |
| 적합 조건 | 외부 소비자와 계약을 먼저 합의 | 프레임워크 중심 내부 API를 코드와 함께 변경 |

> 요약: Design-First는 OpenAPI 문서를 계약 원본으로, Code-First는 구현 코드를 원본으로 삼아 명세와 산출물을 동기화함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| OpenAPI·Info·Servers | OAS 버전·API 메타데이터·접속 서버를 정의함 |
| Paths·Operations | 경로별 HTTP 연산·매개변수·요청 본문·응답을 기술함 |
| Components·Schema | 재사용 데이터 구조·응답·매개변수·보안 정의를 관리함 |
| Security Requirement | API 전체 또는 연산별 인증 방식을 연결함 |
| Swagger Editor·UI | 명세를 편집·검증하고 대화형 문서와 호출 화면을 제공함 |
| Generator·Contract Test | 명세에서 코드·Mock을 생성하고 구현 응답을 계약과 대조함 |

```text
OpenAPI YAML/JSON -> Lint -> Docs·Mock·Client/Server Stub
                         -> Implementation -> Contract Test
```

> 요약: OpenAPI 문서의 경로·Schema·보안 계약을 Swagger 도구와 생성기·계약 시험이 문서·코드·검증에 재사용함.

## Ⅴ. 원리 및 절차 흐름도

```text
계약 작성 -> Lint·호환성 검사 -> Mock·Stub 생성 -> 구현 -> 계약 시험 -> 문서 배포
```

1. **계약 작성**: 소비자 시나리오를 Path·Operation·Schema·Response·Security로 기술함
2. **정적 검사**: Linter가 문법·참조·조직 규칙을 확인하고 이전 명세와 파괴적 변경을 비교함
3. **산출물 생성**: Mock·클라이언트 SDK·서버 Interface·문서를 같은 명세에서 생성함
4. **구현·시험**: 서버 응답과 소비자 요청을 Schema·상태 코드·헤더 계약에 대조함
5. **배포·동기화**: 승인한 명세 버전과 문서를 게시하고 구현 변경과 함께 갱신함

> 요약: OpenAPI 계약은 정적 검사·코드 생성·구현·계약 시험·문서 배포를 연결하는 기준 산출물임.

## Ⅵ. 실무 사례

1. 외부 파트너 API는 Design-First와 호환성 검사를 적용하고 계약 위반 건수·SDK 생성 성공률을 확인함
2. 내부 서비스 API는 Code-First와 Swagger UI를 적용하고 문서 불일치 건수·계약 시험 통과율을 확인함

## Ⅶ. 결론

- OpenAPI·Swagger는 계약 원본을 명세와 코드 중 어디에 둘지 정하고 생성·시험·문서 산출물의 동기화를 검증해야 함
