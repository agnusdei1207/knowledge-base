---
sidebar:
  order: 76
  label: "076. 아키텍처 결정 기록 ADR"
  badge:
    text: "미출 · 30%"
    variant: note
title: "아키텍처 결정 기록 ADR (Architecture Decision Record)"
date: "2026-08-26T17:47:00+09:00"
tags:
  - "notes-software"
weight: 76
extra:
  question_no: "076"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "ADR은 설계 근거•대안 추적의 실무 문서"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ADR(Architecture Decision Record)**: 소프트웨어 아키텍처의 중요 결정 내용, 당시의 맥락(Context), 검토 대안 및 트레이드오프(Consequences)를 Git에 소스코드와 함께 저장하는 경량 문서.
- **Michael Nygard 포맷**: 제목, 상태, 맥락, 결정, 결과 5대 필드로 구성된 가장 널리 쓰이는 표준 ADR 템플릿.

</details>

- 정의/개념: 중요 아키텍처 결정의 **맥락(Context), 선택 대안, 결정(Decision) 및 파급 결과(Consequences)** 를 Git에 소스코드와 함께 버전 관리하는 공학 기록 체계
- 배경/필요성: 결정의 배경이 구두나 흩어진 문서로만 남으면 몇 달 뒤 같은 논의를 반복하고 이미 기각된 대안을 다시 검토하는 비용을 치르므로, 결정 하나를 맥락·대안·결과 단위로 기록한 ADR을 코드와 같은 저장소에서 버전 관리할 필요

#### 한줄 요약
- 아키텍처 결정의 맥락, 대안, 결정, 결과를 Git 저장소에 소스코드와 함께 불변으로 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Co-located with Code**: 위키나 Confluence가 아닌 소스코드 저장소 내부(`docs/adr/`)에 마크다운으로 위치하여 PR(Pull Request) 리뷰 대상이 됨.
- **Superseded(대체됨)**: 이전 결정을 수정해 덮어쓰지 않고, 새로운 결정을 담은 신규 ADR을 발행하여 이전 문서를 대체 연결하는 불변 이력 방식.

</details>

- 소스코드와 동일 저장소에서 관리되는 **코드 공동 배치(Co-located with Code)**
- 단편적 결과가 아닌 **결정 배경 맥락(Context)과 트레이드오프 결과(Consequences) 보존**
- 과거 문서를 덮어쓰지 않고 신규 문서로 갱신하는 **불변 이력 및 대체(Superseded) 연결**

#### 한줄 요약
- ADR은 결정 맥락을 보존하는 대신 결정마다 기록 비용을 요구하므로, 무엇을 중대 결정으로 볼지의 기준이 곧 제도의 지속 가능성을 정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ADR 5대 필드**: Title(식별 번호/제목), Status(Proposed/Accepted/Superseded), Context(맥락), Decision(결정), Consequences(이점 및 감수할 비용).

</details>

```text
[ADR 문서 구조 및 Nygard 템플릿]
|-- Title (제목: ADR-0005: Event Sourcing & CQRS 패턴 도입)
|-- Status (상태: Proposed / Accepted / Superseded / Deprecated)
|-- Context (배경 맥락: RDB 트랜잭션 한계 및 비즈니스 감사 로그 요구사항 발생)
|-- Decision (결정 내용: Kafka + MongoDB 기반 CQRS 아키텍처 채택)
`-- Consequences (결과 및 파급효과)
    |-- (+) 장점: 조회 성능 10배 향상 및 완벽한 이벤트 이력 보존
    `-- (-) 단점: Eventual Consistency 결과적 일관성 지연 처리 오버헤드 감수
```

선의 의미: 계층 및 1개 ADR 파일 내부의 표준 필드 구성

| 구성요소 | 책임 |
|:---|:---|
| Title | 순번과 **핵심 결정 식별** |
| Status | 결정의 **현재 유효 상태** 표시 |
| Context | 결정이 필요한 **배경·제약 기록** |
| Decision | 선택안·기각안과 **근거 기록** |
| Consequences | 이점과 **감수할 비용 기록** |

#### 한줄 요약
- 다섯 필드 중 Context와 Consequences가 결정의 재검토 가능성을 좌우하므로, 결론만 남긴 ADR은 몇 달 뒤 같은 논의를 막지 못한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ADR 라이프사이클**: 제안(Proposed) $\to$ 팀 리뷰 및 머지(Accepted) $\to$ 환경 변화 시 신규 ADR 발행으로 이전 문서 대체(Superseded).

</details>

```text
아키텍처 변경 필요성 발생 (예: MSA 전환, DB 샤딩)
        │
   [Proposed] 아키텍트가 ADR 마크다운 문서를 작성하여 Git 브랜치 생성
        │
   [Pull Request] 팀 엔지니어 및 이해관계자 코드 리뷰 및 기술 토론 진행
        │
   [Accepted] 합의 완료 시 main 브랜치로 병합하여 현행 아키텍처로 공식 승인
        │
   (향후 2년 뒤 신기술 도입으로 설계가 바뀔 경우)
        │
   [Superseded] 신규 ADR-0015를 발행하고 기존 ADR-0005에 'Replaced by ADR-0015' 링크 연결
```

#### 한줄 요약
- Accepted 이후의 결정은 고쳐 쓰지 않고 새 ADR로 대체하므로, 이력이 덮어쓰기가 아닌 축적으로 남아 왜 바뀌었는지까지 추적된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ADR vs Wiki/Confluence**: 코드와 함께 버전 관리되는 ADR과 시간이 지나면 방치되어 코드와 불일치(Drift)하는 Wiki 문서.

</details>

| 비교 항목 | Wiki / Confluence 문서화 | ADR (Architecture Decision Record) |
|:---|:---|:---|
| 저장 위치 | 별도 외부 웹서버 / SaaS | **Git 소스코드 레포지토리 (`docs/adr/`)** |
| 코드 동기화 | 코드 변경 시 업데이트 누락 다수 (Drift) | **동일 PR에서 코드와 ADR을 함께 커밋/리뷰** |
| 변경 이력 관리 | 덮어쓰기로 과거 결정 맥락 유실 | **Git Commit Log 및 Superseded 불변 링크 보존** |
| 작성 부담 | 수십 장의 거대 아키텍처 문서 | **1개 결정당 1~2장의 가벼운 마크다운 텍스트** |

#### 한줄 요약
- 위키는 최신화 누락 위험이 크고, ADR은 코드와 함께 살아 숨쉬며 불변 이력을 보존한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **adr-tools**: 터미널에서 `adr new "Use PostgreSQL"` 명령어로 번호 매김과 Superseded 링크를 자동 생성해주는 CLI 도구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사소한 코드 변경마다 ADR을 써서 문서 피로 누적 | **시스템 구조/비용에 영향을 주는 '중대 결정'만 선별 작성** | 문서화 오버헤드 최소화 |
| 과거 ADR을 덮어써서 결정 히스토리 파악 불가 | **기존 문서는 불변 보존하고 Superseded 상태로 신규 ADR 링크** | 결정 역사 추적성 100% 보장 |
| 개발자들이 마크다운 템플릿 작성을 번거로워함 | **`adr-tools` CLI 도구 또는 IDE 플러그인 연동 자동화** | 작성 장벽 제거 및 도입률 제고 |
| 신규 입사자가 왜 이렇게 설계되었는지 모름 | **온보딩 시 `docs/adr/` 디렉터리 필독 가이드 제공** | 빠른 아키텍처 맥락 파악 및 역량 온보딩 |

#### 한줄 요약
- ADR은 기록 비용을 지불하고 결정의 재논의 비용을 없애므로, 중대 결정만 선별해 부담을 낮추고 폐기된 결정도 Superseded로 남겨 기각 이유까지 자산으로 남긴다.

## Ⅶ. 결론

- 설계 결정은 **ADR 기록**, 변경 이력은 **대체 연결** 선택

#### 한줄 요약
- ADR은 아키텍처 결정의 배경 맥락과 트레이드오프를 코드와 함께 살아있는 문서로 보존하는 소프트웨어 공학의 핵심 지식 관리 도구다.
