---
title: 395. 책임 연쇄 패턴 (Chain of Responsibility Pattern)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)은 요청 처리자를 체인으로 연결해 누가 처리할지 런타임에 결정하게 만드는 행동 패턴이다.
> 2. **가치**: [[395_verification_process_review|검증]] 단계 조합과 [[164_policy|정책]] 추가를 중앙 분기 없이 수행하게 해 준다.
> 3. **판단 포인트**: 체인 설계에서는 처리 순서, 중단 조건, 최종 미처리 [[164_policy|정책]]을 반드시 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

[[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)은 요청 처리자를 체인으로 연결해 누가 처리할지 런타임에 결정하게 만드는 행동 패턴이다. [[395_verification_process_review|검증]], 필터링, 승인 절차처럼 여러 단계가 순차로 관여하는 흐름에서 호출자가 모든 처리자를 알 필요는 없다. 이 개념이 필요한 이유는 요청 처리 파이프라인을 유연하게 구성하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 처리 순서가 고정 코드에 박히고 새 단계 추가 시 중앙 로직을 계속 수정하게 된다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐
│ Variation  │──▶│   Chain    │──▶│   Reuse    │
└────────────┘   └────────────┘   └────────────┘
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)의 핵심 원리는 "요청 처리 파이프라인을 유연하게 구성하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 핸들러가 다음 핸들러를 참조하며 처리 가능 여부에 따라 직접 처리하거나 다음 단계로 넘긴다. 동시에 체인이 길어지면 실제 처리 주체 파악이 어려워지고 누락 시 디버깅이 힘들 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 요청 처리 파이프라인을 유연하게 구성하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 핸들러가 다음 핸들러를 참조하며 처리 가능 여부에 따라 직접 처리하거나 다음 단계로 넘긴다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 체인이 길어지면 실제 처리 주체 파악이 어려워지고 누락 시 디버깅이 힘들 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Client  │──▶│  Chain   │──▶│  Object  │──▶│  Result  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [[346_maintainability_portability|유지보수성]], 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 요청 처리 파이프라인을 유연하게 구성하는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 핸들러가 다음 핸들러를 참조하며 처리 가능 여부에 따라 직접 처리하거나 다음 단계로 넘긴다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 [[395_verification_process_review|검증]] 단계 조합과 [[164_policy|정책]] 추가를 중앙 분기 없이 수행하게 해 준다 | 즉흥 구현 상태는 처리 순서가 고정 코드에 박히고 새 단계 추가 시 중앙 로직을 계속 수정하게 된다 |

연결 개념으로는 필터 체인, 미들웨어 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 무조건 채택하기보다 체인 설계에서는 처리 순서, 중단 조건, 최종 미처리 [[164_policy|정책]]을 반드시 함께 제시해야 한다. 아래 [[435_checklist_based_testing|체크리스트]]는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [[198_abstraction_control_data_process|추상화]] 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)의 기대효과는 분명하다. [[395_verification_process_review|검증]] 단계 조합과 [[164_policy|정책]] 추가를 중앙 분기 없이 수행하게 해 준다. 다만 체인이 길어지면 실제 처리 주체 파악이 어려워지고 누락 시 디버깅이 힘들 수 있다. 결국 기억할 관점은 요청 처리 파이프라인을 유연하게 구성하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 필터 체인 | [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 설계하고 감리할 때 함께 보는 연관 개념 |
| 미들웨어 | [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 설계하고 감리할 때 함께 보는 연관 개념 |
| 승인 워크플로 | [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 설계하고 감리할 때 함께 보는 연관 개념 |
| 파이프라인 | [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[중앙 분기 처리] → [책임 연쇄 패턴] → [동적 파이프라인]

### 👶 어린이를 위한 3줄 비유 설명
1. [[276_chain_of_responsibility_pattern|책임 연쇄]] 패턴 ([[276_chain_of_responsibility_pattern|Chain of Responsibility]] Pattern)은 문제가 생기면 담임, 부장, 교장 순서로 차례차례 전달하는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 요청 처리 파이프라인을 유연하게 구성하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 473 / 530

← **이전**: [[394_process|394. 상태 패턴 (State Pattern)]]
**다음**: [[396_process|396. 중재자 패턴 (Mediator Pattern)]] →

---
