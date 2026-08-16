---
sidebar:
  order: 76
  label: "076. 아키텍처 결정 기록 ADR (Architecture Decision Record)"
  badge:
    text: "미출제 • 30%"
    variant: note
title: "아키텍처 결정 기록 ADR (Architecture Decision Record)"
date: "2026-08-13T17:50:00+09:00"
tags:
  - "notes-software"
weight: 76
extra:
  question_no: "076"
  source_status: "미출제"
  source_history: ""
  priority: 30
  priority_note: "ADR은 설계 근거•대안 추적의 실무 문서"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ADR (Architecture Decision Record, 아키텍처 결정 기록)**: 소프트웨어 아키텍처의 중요한 의사결정(Decision) 내용, 당시의 비즈니스/기술적 맥락(Context), 검토된 대안(Alternatives) 및 결정에 따른 이점과 결과(Consequences)를 마크다운 형태의 짧은 텍스트 문서로 깃(Git) 소스코드와 함께 버전 관리하는 기록 체계.
- **Architectural Decision Log (ADL)**: 프로젝트 내에서 작성된 개별 ADR 문서들의 집합체 및 변경 관리 이력 모음.
- **Nygard Architecture Decision Record Format**: 마이클 나이 가드(Michael Nygard)가 제안한 가장 대표적인 ADR 템플릿 표준 구조.

</details>

- 정의/개념: 소프트웨어 개발 과정에서 내려진 중요 아키텍처 의사결정의 배경 맥락, 선택 이유, 대안 및 파급 결과를 1개 파일당 1개 결정 단위로 Git 저장소에 소스코드와 동시 버전 관리하는 **ADR (Architecture Decision Record)**
- 배경/필요성: 구두•산재 문서는 **결정 근거•대안•변경 이력** 유실

#### 한줄 요약

- 맥락•대안•결정•결과를 보존하는 아키텍처 결정 기록이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Immutable Log (불변적 변경 기록)**: 한 번 승인된 ADR은 수정하여 덮어쓰지 않고, 새로운 결정 시 신규 ADR을 발행하여 기존 ADR을 'Superseded(대체됨)' 상태로 연결 상태 업데이트.
- **Co-located with Source Code**: 별도 Wiki나 Confluence가 아닌 Git 소스코드 레포지토리 내(`doc/adr/`)에 Markdown 형태로 직접 저장되어 PR(Pull Request) 리뷰 대상으로 동시 관리.

</details>

- **Co-located with Code (Git 버전 관리 시스템과의 완전 통합)**
- 단편적 결과가 아닌 **Context & Trade-off Consequences 기록**
- 불변 이력 보존 및 **Superseded (대체됨) 링크 연결 수명주기**

#### 한줄 요약

- 공동 이력, 근거 보존, 대체 연결이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **5대 핵심 필드**: Title(제목 및 번호), Status(상태: Proposed, Accepted, Deprecated, Superseded), Context(맥락), Decision(결정), Consequences(결과 및 이점/비용).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│               ADR-0005: Event Sourcing & CQRS Pattern 도입              │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Accepted (승인됨) | Date: 2026-08-10                           │
├─────────────────────────────────────────────────────────────────────────┤
│ Context: 기존 RDB 트랜잭션 수평 확장 한계 및 변경 이력 추적성 요구 발생  │
├─────────────────────────────────────────────────────────────────────────┤
│ Decision: Kafka + Event Store 기반 Event Sourcing & CQRS 아키텍처 채택  │
├─────────────────────────────────────────────────────────────────────────┤
│ Consequences:                                                           │
│ (+) 장점: 변경 이력 추적과 조회 모델 독립 확장                           │
│ (-) 단점: 시스템 복잡도 및 Eventual Consistency 지연 처리 오버헤드 발생 │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 1개 ADR 파일 내에 제목, 상태, 맥락, 결정, 파급 결과가 구조화되어 기록되는 템플릿 아키텍처.

| ADR 구성 영역 | 필수 입력 내용 | 작성 지침 및 가이드 |
|:---|:---|:---|
| Title (제목) | `ADR-0001: RDB 대신 MongoDB 채택` 형태로 순번과 명칭 부여 | 짧고 명확한 결정 단위 표현 |
| Status (상태) | **Proposed (제안) / Accepted (승인) / Deprecated (폐기) / Superseded (대체)** | 현 상태를 명확히 표시 |
| Context (맥락) | 왜 이 결정이 필요했는지의 비즈니스/기술적 배경 및 제약조건 | 주관적 주장이 아닌 객관적 문제 명시 |
| Decision (결정) | **선택한 아키텍처 솔루션 및 기각된 대안들** | 기술적 선택 근거 명시 |
| Consequences (결과) | **결정에 따른 positive(이점) 및 negative(트레이드오프/비용) 파급 효과** | 감수할 단점(Negative)까지 솔직히 서술 |

#### 한줄 요약

- 문제•결정•결과와 네 가지 유효 상태의 문서 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ADR Lifecycle**: Proposed(제안) $\rightarrow$ Accepted(승인) $\rightarrow$ [환경 변화 시] $\rightarrow$ Superseded(신규 ADR에 의해 대체됨) 또는 Deprecated(폐기).

</details>

```text
       ┌───────────┐
       │ Proposed  │ (의견 수렴 및 PR 리뷰)
       └─────┬─────┘
             │ (팀 합의 완료)
             ▼
       ┌───────────┐
       │ Accepted  │ (현행 아키텍처로 작동)
       └─────┬─────┘
             │ (기술 환경 변화로 신규 ADR-0010 제정 시)
             ├──────────────────────────┐
             ▼                          ▼
      ┌────────────┐             ┌────────────┐
      │ Superseded │             │ Deprecated │
      └────────────┘             └────────────┘
(Replaced by ADR-0010)        (No longer applies)
```

### 동작 원리

1. **Proposed**: 문제•제약•대안•결정 후보를 ADR로 제안.
2. **Accepted**: 검토 합의와 결정 책임자를 기록해 승인.
3. **Superseded**: 환경 변화 시 기존 기록과 신규 ADR을 상호 연결.

#### 한줄 요약

- 결정•구현 연결과 후속 대체 이력 보존 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ADR vs Wiki/Confluence**: Wiki는 시간이 흐르면 최신화가 안 되어 실제 소스코드와 이격(Drift)이 나는 반면, ADR은 Git 코드와 한 브랜치에서 같이 관리되므로 100% 동기화 보장.

</details>

| 비교 항목 | Wiki / Confluence 문서화 | ADR (Architecture Decision Record) |
|:---|:---|:---|
| 저장 위치 | 외부 SaaS / 웹서버 (Wiki 플랫폼) | **Git 소스코드 레포지토리 내부 (`doc/adr/`)** |
| 버전 동기화 | 별도 변경 절차로 코드와 이격 가능 | **동일 PR에서 코드•결정 기록 함께 검토 가능** |
| 역사적맥락(History)| 이전 이력을 덮어써서 파악 곤란 | **불변 파일 추가 방식 (Superseded 링크 관리)** |
| 작성 단위 | 거대한 전체 아키텍처 명세서 | **1개 의사결정당 1개의 짧은 텍스트 문서** |

#### 한줄 요약

- 중대 아키텍처 결정은 아키텍처 결정 기록, 낮은 영향 결정은 간소 기록이 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **adr-tools**: CLI 환경에서 `adr new "Select Postgres for Primary DB"` 형태로 ADR 문서를 자동 생성하고 Superseded 링크를 자동 맺어주는 오픈소스 도구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사소한 코드 변경마다 ADR 작성하여 문서 오버헤드 폭증 | **사소한 변경은 제외, 시스템 영향을 주는 결정만 ADR 선별 작성** | 효율성 통제 |
| ADR 덮어쓰기로 과거 결정 이유 파악 곤란 | **Superseded 상태와 신규 ADR 양방향 링크** | 결정 이력 추적성 확보 |
| 개발자들이 Markdown 양식 작성을 귀찮아함 | **IDE (VS Code, IntelliJ) ADR 전용 플러그인 연동** | 작성 장벽 제거 |

> 사례: **CNCF 및 오픈소스 프로젝트 내 `adr-tools` 기반 Git 레포지토리 관리**

#### 한줄 요약

- 중대 아키텍처 결정 선별과 모듈 연결, 대체 연결이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **ADR 수립 기준(ADR Adoption Standards)**: 아키텍처 영향도, Git 파이프라인 연동성 및 `adr-tools` 활용 체계에 의거한 체계.

</details>

- 영향•복구 비용이 큰 결정은 **ADR**, 국소 구현 선택은 **간소 기록** 적용

#### 한줄 요약

- 영향•비용•추적 필요성에 따른 ADR 작성 기준이 핵심이다.
