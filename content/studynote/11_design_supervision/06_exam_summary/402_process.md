---
title: 402. 데이터 접근 객체 (Data Access Object, DAO)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])은 [[001_dikw_pyramid|데이터]] 저장소 접근 세부 구현을 캡슐화해 비즈니스 로직과 분리하는 패턴이다.
> 2. **가치**: 저장 기술 교체와 테스트 격리를 쉽게 한다.
> 3. **판단 포인트**: DAO는 저장소 기술 세부를 숨기는 패턴이며, 리포지터리와의 역할 차이도 구분하면 좋다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])은 [[001_dikw_pyramid|데이터]] 저장소 접근 세부 구현을 캡슐화해 비즈니스 로직과 분리하는 패턴이다. SQL, 연결 관리, 매핑 규칙이 [[090_service_kubernetes_network_load_balancing|서비스]] 코드에 섞이면 핵심 규칙보다 저장소 세부사항이 더 많은 코드를 차지한다. 이 개념이 필요한 이유는 [[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 저장소 변경이 곧 [[090_service_kubernetes_network_load_balancing|서비스]] 로직 수정과 테스트 비용 증가로 이어진다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐
│    Data    │──▶│    DAO     │──▶│  Boundary  │
└────────────┘   └────────────┘   └────────────┘
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 접수 창구를 구분하지 않으면 민원, 결제, 안내가 한 줄에 엉키는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])의 핵심 원리는 "[[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 DAO가 CRUD, [[298_qkv_attention|쿼리]], 매핑, 예외 변환을 담당하고 상위 계층은 인터페이스로만 의존한다. 동시에 단순 ORM 사용에 DAO를 과하게 겹치면 중복 추상화가 될 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | [[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | DAO가 CRUD, [[298_qkv_attention|쿼리]], 매핑, 예외 변환을 담당하고 상위 계층은 인터페이스로만 의존한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 단순 ORM 사용에 DAO를 과하게 겹치면 중복 추상화가 될 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Caller  │──▶│ Contract │──▶│   DAO    │──▶│  Store   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [[346_maintainability_portability|유지보수성]], 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 물류 전달 벨트처럼 입력과 저장 사이의 책임이 분리되어야 흐름이 막히지 않는다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **경계 분리 상태** 와 **계층 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 경계 분리 상태는 [[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일에 맞춰 영향 범위를 줄인다 | 계층 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 경계 분리 상태는 DAO가 CRUD, [[298_qkv_attention|쿼리]], 매핑, 예외 변환을 담당하고 상위 계층은 인터페이스로만 의존한다 | 계층 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 경계 분리 상태는 저장 기술 교체와 테스트 격리를 쉽게 한다 | 계층 혼재 상태는 저장소 변경이 곧 [[090_service_kubernetes_network_load_balancing|서비스]] 로직 수정과 테스트 비용 증가로 이어진다 |

연결 개념으로는 리포지터리, [[191_transaction_concept_states|트랜잭션]] 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 직접 전달과 중간 허브를 비교하면 경계의 가치가 더 뚜렷해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 무조건 채택하기보다 DAO는 저장소 기술 세부를 숨기는 패턴이며, 리포지터리와의 역할 차이도 구분하면 좋다. 아래 [[435_checklist_based_testing|체크리스트]]는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 계층 간 계약이 명확하고 중복 변환이 과도하지 않은가?
2. 비즈니스 규칙이 전송/저장 계층으로 새지 않는가?
3. 예외 처리와 [[191_transaction_concept_states|트랜잭션]] 경계가 문서화되어 있는가?
4. [[282_performance_tactics|성능]] 최적화가 책임 분리를 무너뜨리지 않는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 운영 체크시트처럼 계층 간 계약과 [[001_dikw_pyramid|데이터]] 일관성을 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])의 기대효과는 분명하다. 저장 기술 교체와 테스트 격리를 쉽게 한다. 다만 단순 ORM 사용에 DAO를 과하게 겹치면 중복 추상화가 될 수 있다. 결국 기억할 관점은 [[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 업무 인수인계서처럼, 좋은 엔터프라이즈 패턴은 사람과 시스템 모두 이해하기 쉬워야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 리포지터리 | [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[191_transaction_concept_states|트랜잭션]] | [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| ORM | [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| 매핑 | [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[서비스 내부 SQL] → [[[054_dao_decentralized_autonomous_organization|DAO]] 분리] → [저장소 캡슐화]

### 👶 어린이를 위한 3줄 비유 설명
1. [[001_dikw_pyramid|데이터]] 접근 객체 ([[001_dikw_pyramid|Data]] Access Object, [[054_dao_decentralized_autonomous_organization|DAO]])은 교실 대표가 선생님께 출석표를 대신 전달하는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 [[001_dikw_pyramid|데이터]] 접근 책임을 전용 계층에 격리하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 480 / 530

← **이전**: [[401_process|401. 데이터 전송 객체 (Data Transfer Object, DTO)]]
**다음**: [[403_architecture|403. 안티 패턴 (Anti-Patterns)]] →

---
