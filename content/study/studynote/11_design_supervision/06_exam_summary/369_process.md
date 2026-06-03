+++
weight = 369
title = "369. 이벤트 소싱 (Event Sourcing)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])은 [[178_as_is_to_be_analysis|현재 상태]] 대신 상태를 만든 이벤트들의 불변 로그를 원본 [[001_dikw_pyramid|데이터]]로 저장하는 방식이다.
> 2. **가치**: [[606_auditing_linux_auditd|감사]] 가능성, 재현성, 시간 축 분석 능력을 크게 높인다.
> 3. **판단 포인트**: [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 모든 시스템의 기본 저장 방식이 아니라 높은 추적성과 재생 가치가 있는 [[064_relation_domain|도메인]]에 선택적으로 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])은 [[178_as_is_to_be_analysis|현재 상태]] 대신 상태를 만든 이벤트들의 불변 로그를 원본 [[001_dikw_pyramid|데이터]]로 저장하는 방식이다. [[606_auditing_linux_auditd|감사]] 추적, 시간 여행 조회, 상태 재구성이 중요한 [[064_relation_domain|도메인]]에서 [[022_snapshot_backup_architecture|스냅샷]] 중심 저장만으로는 한계가 드러났다. 이 개념이 필요한 이유는 상태 변화 자체를 원본 사실로 보존하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 누가 언제 어떤 의사결정을 했는지 추적하기 어렵고 [[658_ir_recovery|복구]] 근거도 부족해진다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Request   │──▶│     ES     │──▶│   Stable   │
└────────────┘   └────────────┘   └────────────┘
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 도시를 구획 없이 확장하면 길과 배관이 엉키는 것처럼, 구조 원칙이 없으면 시스템도 빨리 혼잡해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])의 핵심 원리는 "상태 변화 자체를 원본 사실로 보존하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 [[064_relation_domain|도메인]] 이벤트를 append-only 로그에 기록하고 필요 시 재생(replay)과 [[022_snapshot_backup_architecture|스냅샷]]으로 상태를 복원한다. 동시에 이벤트 [[005_schema|스키마]] 진화, 재생 비용, 읽기 모델 구성 난도가 높아 운영 성숙도가 필요하다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 상태 변화 자체를 원본 사실로 보존하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | [[064_relation_domain|도메인]] 이벤트를 append-only 로그에 기록하고 필요 시 재생(replay)과 [[022_snapshot_backup_architecture|스냅샷]]으로 상태를 복원한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 이벤트 [[005_schema|스키마]] 진화, 재생 비용, 읽기 모델 구성 난도가 높아 운영 성숙도가 필요하다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Client  │──▶│ Boundary │──▶│   Core   │──▶│  Infra   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [[346_maintainability_portability|유지보수성]], 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 도로망과 관제 센터가 분리된 도시처럼, 경계와 흐름을 함께 설계해야 운영이 안정된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **구조 적용 상태** 와 **경계 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 구조 적용 상태는 상태 변화 자체를 원본 사실로 보존하는 일에 맞춰 영향 범위를 줄인다 | 경계 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 구조 적용 상태는 [[064_relation_domain|도메인]] 이벤트를 append-only 로그에 기록하고 필요 시 재생(replay)과 [[022_snapshot_backup_architecture|스냅샷]]으로 상태를 복원한다 | 경계 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 구조 적용 상태는 [[606_auditing_linux_auditd|감사]] 가능성, 재현성, 시간 축 분석 능력을 크게 높인다 | 경계 혼재 상태는 누가 언제 어떤 의사결정을 했는지 추적하기 어렵고 [[658_ir_recovery|복구]] 근거도 부족해진다 |

연결 개념으로는 이벤트 스토어, [[306_cqrs|CQRS]] 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 계획도시와 무계획 확장을 비교해 보면 어디서 비용이 커지는지 바로 드러난다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 무조건 채택하기보다 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 모든 시스템의 기본 저장 방식이 아니라 높은 추적성과 재생 가치가 있는 [[064_relation_domain|도메인]]에 선택적으로 적용해야 한다. 아래 [[435_checklist_based_testing|체크리스트]]는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 경계와 책임이 코드·문서·배포 단위에서 일치하는가?
2. [[001_dikw_pyramid|데이터]] 소유권과 장애 전파 경로가 명확한가?
3. 관찰가능성, 보안, 배포 전략이 구조와 함께 설계되었는가?
4. 도입 복잡도가 조직 규모와 팀 성숙도에 맞는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 관제실의 운영 [[435_checklist_based_testing|체크리스트]]처럼, 경계·장애 전파·관찰가능성을 같이 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])의 기대효과는 분명하다. [[606_auditing_linux_auditd|감사]] 가능성, 재현성, 시간 축 분석 능력을 크게 높인다. 다만 이벤트 [[005_schema|스키마]] 진화, 재생 비용, 읽기 모델 구성 난도가 높아 운영 성숙도가 필요하다. 결국 기억할 관점은 상태 변화 자체를 원본 사실로 보존하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 도시 운영 규정집처럼, 좋은 아키텍처는 기술보다 판단 기준을 오래 남긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 이벤트 스토어 | [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[306_cqrs|CQRS]] | [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[022_snapshot_backup_architecture|스냅샷]] | [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[606_auditing_linux_auditd|감사]] 추적 | [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[현재 상태 저장] → [이벤트 소싱] → [재생·[[606_auditing_linux_auditd|감사]] 중심 모델]

### 👶 어린이를 위한 3줄 비유 설명
1. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])은 오늘 점수만 적는 대신 경기 기록을 매번 남겨 다시 볼 수 있게 하는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 상태 변화 자체를 원본 사실로 보존하는 일이 더 중요해져요.
