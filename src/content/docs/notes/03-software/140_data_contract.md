---
sidebar:
  order: 140
  label: "140. 데이터 계약"
  badge:
    text: "미출 · 50%"
    variant: note
title: "데이터 계약 (Data Contract)"
date: "2026-08-27T03:06:00+09:00"
tags:
  - "notes-software"
weight: 140
extra:
  question_no: "140"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "생산자•소비자 간 스키마•품질 계약 현안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **데이터 계약(Data Contract)**: 데이터 생산자(Producer)와 소비자(Consumer) 간에 스키마, 데이터 타입, 비즈니스 의미, 품질 SLA를 명시적으로 정의하는 약정서.
- **Breaking Change(파괴적 변경)**: 예고 없는 컬럼 삭제나 타입 변경(`String -> Int`)으로 인해 하류 파이프라인과 대시보드가 일괄 마비되는 장애.

</details>

- 정의/개념: 데이터 생산자와 소비자 간에 **스키마 구조, 의미(Semantics), 품질 규칙(Quality), SLA를 명시적으로 체결하는 인터페이스 규약**
- 배경/필요성: 생산자의 예고 없는 스키마 변경(Breaking Change)으로 인한 **하류 데이터 파이프라인 연쇄 붕괴 및 전사 분석 지표 오염 해결 불가**

#### 한줄 요약
- 스키마, 의미론, 품질 기준, SLA를 코드로 명시하여 파이프라인 파괴적 변경을 사전에 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OpenDataContract Standard(ODCS)**: YAML/JSON 기반으로 스키마, 데이터 품질 룰셋, 서비스 레벨을 표준 기술하는 오픈 포맷.
- **CI/CD Breaking Change Gate**: DB 마이그레이션 PR 시 계약서와의 호환성을 자동 검증하여 비호환 변경의 배포를 자동 차단하는 관문.

</details>

- 데이터 생산자와 소비자 간의 **명확한 책임 분계점(RACI) 확립**
- 스키마 구문(Syntax), 비즈니스 의미(Semantic), 품질 룰셋(Quality), **SLA의 4대 요소 통합 정의**
- CI/CD 파이프라인 상에서 파괴적 변경을 사전에 차단하는 **자동화된 Contract Enforcement**

#### 한줄 요약
- 4대 요소 명세화, 명확한 책임 배정, CI/CD 사전 차단을 통해 데이터 파이프라인 무결성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Data Contract Spec 4대 구성**: Metadata/Owner(책임자), Schema(컬럼/타입), Quality(완전성/유효성), ServiceLevel(신선도/가용성).

</details>

```text
[Data Contract 구성]
|-- 메타데이터 및 소유자
|-- 스키마 및 의미론
|-- 품질 검증 규칙
|-- 서비스 수준 협약
`-- 진화 정책
```

선의 의미: 계층 및 메타데이터, 스키마, 품질 규칙, SLA가 하나의 파일에 통합 선언되는 규약 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 메타데이터 및 소유자 | 데이터셋 식별자, 버전 번호, **생산자 팀 및 소비자 책임 주체 명시** | Owner 이메일/채널 |
| 스키마 및 의미론 | 컬럼명, 데이터 타입, Null 허용 여부, **비즈니스 업무 정의를 구조화 명세** | Syntax & Semantics |
| 품질 검증 규칙 (Quality) | 결측치 허용률, 유효 범위, 건수 등 **데이터 통과를 위한 최소 합격선 정의** | Great Expectations |
| 서비스 수준 협약 (SLA) | 데이터 신선도(Freshness), **적재 지연 한계 시간, 시스템 가용성 보장** | 시간 단위 SLA |
| 진화 정책 (Evolution) | 스키마 변경 시 사전 공지 기간, **하위 호환성 유지 및 버전 업그레이드 규칙** | SemVer 정책 |

#### 한줄 요약
- 메타데이터, 스키마, 품질 규칙, 서비스 수준(SLA), 진화 정책이 유기적으로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Contract Enforcement 5단계**: PR 생성 $\to$ 호환성 검사 $\to$ 영향도 분석 $\to$ CI/CD 배포 차단/승인 $\to$ 런타임 품질 감시.

</details>

```text
백엔드 개발자가 DB 스키마 변경 PR(Pull Request) 생성
        │
   [계약 호환성 검사] GitHub Actions가 기존 Data Contract와 변경된 DDL 간 호환성 자동 검사
        │
   하류 시스템을 깨뜨리는 Breaking Change가 존재하는가?
   ┌────┴───────────────────────────┐
  예 (비호환 변경 발생)             아니오 (하위 호환성 유지)
   │                                 │
[CI/CD 배포 즉시 차단]            [PR Merge 승인 및 배포]
소비자 팀 승인 및 v2 버전        신규 스키마 배포 완료
분리 계약 체결 전까지 병합 차단   및 파이프라인 정상 가동
        │                               │
   └────┬───────────────────────────┘
        ▼
   런타임 단계에서 Great Expectations를 통해 실제 데이터가 계약된 품질과 SLA를 준수하는지 상시 감시
```

#### 한줄 요약
- PR 생성 → 호환성 검사 → Breaking Change 차단 / 승인 → 런타임 품질 감시 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **API Contract vs Data Contract**: 실시간 REST 호출용 인터페이스 계약(API Contract)과 분석 파이프라인용 데이터 품질 계약(Data Contract).

</details>

| 비교 항목 | API Contract (OpenAPI / Swagger) | Data Contract (OpenDataContract) |
|:---|:---|:---|
| 주요 적용 대상 | **마이크로서비스 간 동기 REST/gRPC 통신** | **이종 데이터 파이프라인 및 DW/레이크하우스 수집**|
| 핵심 명세 내용 | HTTP Method, Endpoint, Request/Response | **Schema, Quality Rules, Freshness SLA, Semantics** |
| 파괴적 변경 대응 | API URL 엔드포인트 버저닝 (`/v1` $\rightarrow$ `/v2`)| **Contract 버전 분리 및 CI/CD 사전 의존성 차단** |
| 주 달성 목표 | 서비스 간 기능 동작 인터페이스 일관성 | **데이터 무결성 보장 및 파이프라인 붕괴 방지** |

#### 한줄 요약
- 서비스 통신 규약은 API Contract, 데이터 품질과 파이프라인 무결성은 Data Contract를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Producer Resistance**: 백엔드 개발자가 추가적인 계약서 작성 및 검증 절차에 대해 부담을 느껴 도입을 거부하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 백엔드 개발자의 계약서 작성 거부감 (**Producer Resistance**) | **DB DDL 및 Protobuf에서 Contract YAML을 자동 생성하는 CLI 배포** | 개발자 수동 작업 90% 경감 |
| 계약서만 작성되고 시스템 검증이 누락되는 **Contract Drift** | **GitHub Actions CI/CD 파이프라인에 Contract 호환성 검증 강제** | 배포 시점 계약 불일치 원천 차단 |
| 레거시 DB의 직접 수정으로 인한 계약 우회 장애 | **Kafka Schema Registry와 Data Contract를 연동하여 런타임 검증** | 런타임 비정상 데이터 차단 |
| 계약 위반 시 하류 파이프라인 전체 마비 | **위반 레코드만 Quarantine 테이블로 격리하고 정상 데이터 계속 처리** | 파이프라인 가용성 유지 |

#### 한줄 요약
- 자동 생성 CLI 배포, CI/CD 검증 강제, 스키마 레지스트리 연동, 격리 테이블 운영으로 정착시킨다.

## Ⅶ. 결론

- 파괴적 변경 방지는 **데이터 계약**, 검증은 **CI/CD 게이트** 선택

#### 한줄 요약
- 데이터 계약은 생산자와 소비자 간의 스키마와 품질 책임을 명시적으로 규정하여 파이프라인의 파괴적 변경을 방지하는 현대 데이터 엔지니어링의 핵심 협업 체계다.
