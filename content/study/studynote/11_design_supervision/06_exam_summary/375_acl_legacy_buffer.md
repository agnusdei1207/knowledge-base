+++
weight = 375
title = "375. 안티 코럽션 레이어 (Anti-Corruption Layer, ACL)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])은 레거시 또는 외부 시스템의 모델 오염이 내부 [[064_relation_domain|도메인]]으로 번지지 않게 번역 계층을 두는 패턴이다.
> 2. **가치**: 레거시 통합 중에도 내부 모델 순도를 지키게 해 준다.
> 3. **판단 포인트**: ACL은 단순 DTO 변환기가 아니라 [[064_relation_domain|도메인]] 의미를 지키는 방어벽이라는 점을 답안에 담아야 한다.

---

## Ⅰ. 개요 및 필요성

[[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])은 레거시 또는 외부 시스템의 모델 오염이 내부 [[064_relation_domain|도메인]]으로 번지지 않게 번역 계층을 두는 패턴이다. 통합 시 외부 용어와 [[001_dikw_pyramid|데이터]] 구조를 그대로 들여오면 내부 모델이 점점 외부 사정에 끌려간다. 이 개념이 필요한 이유는 외부 모델의 의미 오염을 차단하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 핵심 [[064_relation_domain|도메인]] 언어가 외부 시스템 용어에 잠식되어 내부 규칙 설명과 변경이 어려워진다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Request   │──▶│    ACL     │──▶│   Stable   │
└────────────┘   └────────────┘   └────────────┘
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 도시를 구획 없이 확장하면 길과 배관이 엉키는 것처럼, 구조 원칙이 없으면 시스템도 빨리 혼잡해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])의 핵심 원리는 "외부 모델의 의미 오염을 차단하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 변환기, 파사드, [[259_adapter_pattern_interface_wrapper|어댑터]]를 둬 외부 계약을 내부 [[064_relation_domain|도메인]] 언어로 번역한 뒤 코어에 전달한다. 동시에 번역 계층 유지 비용이 들지만 이를 생략하면 장기적으로 [[064_relation_domain|도메인]] 침식 비용이 더 커진다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 외부 모델의 의미 오염을 차단하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 변환기, 파사드, [[259_adapter_pattern_interface_wrapper|어댑터]]를 둬 외부 계약을 내부 [[064_relation_domain|도메인]] 언어로 번역한 뒤 코어에 전달한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 번역 계층 유지 비용이 들지만 이를 생략하면 장기적으로 [[064_relation_domain|도메인]] 침식 비용이 더 커진다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

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

기술사 답안에서는 [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **구조 적용 상태** 와 **경계 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 구조 적용 상태는 외부 모델의 의미 오염을 차단하는 일에 맞춰 영향 범위를 줄인다 | 경계 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 구조 적용 상태는 변환기, 파사드, [[259_adapter_pattern_interface_wrapper|어댑터]]를 둬 외부 계약을 내부 [[064_relation_domain|도메인]] 언어로 번역한 뒤 코어에 전달한다 | 경계 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 구조 적용 상태는 레거시 통합 중에도 내부 모델 순도를 지키게 해 준다 | 경계 혼재 상태는 핵심 [[064_relation_domain|도메인]] 언어가 외부 시스템 용어에 잠식되어 내부 규칙 설명과 변경이 어려워진다 |

연결 개념으로는 [[310_architecture|DDD]], [[383_adapter_pattern_summary|어댑터 패턴]] 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 계획도시와 무계획 확장을 비교해 보면 어디서 비용이 커지는지 바로 드러난다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 무조건 채택하기보다 ACL은 단순 DTO 변환기가 아니라 [[064_relation_domain|도메인]] 의미를 지키는 방어벽이라는 점을 답안에 담아야 한다. 아래 [[435_checklist_based_testing|체크리스트]]는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 경계와 책임이 코드·문서·배포 단위에서 일치하는가?
2. [[001_dikw_pyramid|데이터]] 소유권과 장애 전파 경로가 명확한가?
3. 관찰가능성, 보안, 배포 전략이 구조와 함께 설계되었는가?
4. 도입 복잡도가 조직 규모와 팀 성숙도에 맞는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 관제실의 운영 [[435_checklist_based_testing|체크리스트]]처럼, 경계·장애 전파·관찰가능성을 같이 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

[[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])의 기대효과는 분명하다. 레거시 통합 중에도 내부 모델 순도를 지키게 해 준다. 다만 번역 계층 유지 비용이 들지만 이를 생략하면 장기적으로 [[064_relation_domain|도메인]] 침식 비용이 더 커진다. 결국 기억할 관점은 외부 모델의 의미 오염을 차단하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 도시 운영 규정집처럼, 좋은 아키텍처는 기술보다 판단 기준을 오래 남긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[310_architecture|DDD]] | [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[383_adapter_pattern_summary|어댑터 패턴]] | [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[310_strangler_fig_pattern|스트랭글러 피그]] | [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| 레거시 통합 | [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[외부 모델 직접 침투] → [[[549_acl_access_control_list|ACL]] 적용] → [도메인 언어 보호]

### 👶 어린이를 위한 3줄 비유 설명
1. [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])은 다른 나라 손님 말을 통역사가 우리말로 바꿔 주는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 외부 모델의 의미 오염을 차단하는 일이 더 중요해져요.
