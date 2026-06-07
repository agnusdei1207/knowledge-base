---
title: "072. Platform Business Two Sided Market"
date: "2026-06-07"
tags:
  - "enterprise_systems"
  - "studynote-enterprise-systems"
weight: 72
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 플랫폼 비즈니스는 공급자와 수요자를 연결하는 생태계 운영 모델이다.
> 2. **가치**: [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/)로 가치가 커지고, 규칙/수수료를 통해 수익을 만든다.
> 3. **판단**: 플랫폼은 제품이 아니라 거래와 상호작용의 장을 설계하는 것이다.

---

## Ⅰ. 개요 및 필요성

상품을 직접 다 만드는 것보다 연결을 잘 만드는 모델이 더 강력할 수 있다.

플랫폼 비즈니스가 그렇다.

- **📢 섹션 요약 비유**: 놀이터를 지어 사람들이 모이게 하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Supply Side
  ↔ platform ↔
Demand Side
```

| 요소 | 의미 |
| :-- | :-- |
| Two-sided Market | 양면 시장 |
| [Network Effect](/studynote/12_it_management/01_governance_strategy/824_network_effect/) | [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/) |
| Rule / Fee | 규칙과 수수료 |

플랫폼은 양쪽 참여자가 많아질수록 더 강해진다. 그래서 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)와 규칙 설계가 중요하다.

- **📢 섹션 요약 비유**: 손님과 가게를 모두 모으는 시장이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 전통 비즈니스 | 플랫폼 비즈니스 |
| :-- | :-- | :-- |
| 생산 | 직접 제조 | 연결/중개 |
| 수익 | 판매 마진 | 수수료/광고 |
| 성장 | 선형 | [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/) |

| 핵심 | 의미 |
| :-- | :-- |
| Governance | 규칙 |
| Matching | 연결 |

플랫폼은 거래를 만들어내는 구조이며, 운영과 거버넌스가 매우 중요하다.

- **📢 섹션 요약 비유**: 가게를 짓는 게 아니라 장터를 여는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 공급자와 수요자를 모두 보는가?
2. [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/)를 설계하는가?
3. 규칙과 수수료가 명확한가?
4. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 참여 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 넘길 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?
5. 신뢰와 거버넌스를 고려하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 한쪽만 생각하는 설계
- 거래 규칙이 없는 설계
- [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/)를 무시하는 설계
- 플랫폼과 단일 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 차이를 모르는 설계

기술사 관점에서는 플랫폼 비즈니스를 "양면 시장을 연결하는 생태계 모델"로 설명해야 한다.

- **📢 섹션 요약 비유**: 사람들을 모아 계속 돌게 만드는 놀이터다.

---

## Ⅴ. 기대효과 및 결론

플랫폼 비즈니스는 연결을 통해 가치가 커진다.

결론적으로 플랫폼 비즈니스는 양면 시장을 연결하는 생태계 모델이다.

- **📢 섹션 요약 비유**: 모이면 모일수록 더 강해지는 시장이다.

---

## 관련 개념 맵

```text
Supply Side
  ↔
Platform
  ↔
Demand Side
```

---

## 관련 키워드 및 발전 흐름도

```text
Two-sided Market
  v
Platform Business
  v
Network Effect
```

---

## 어린이를 위한 3줄 비유 설명

사람들을 서로 이어 줘요.
모일수록 더 좋아져요.
플랫폼은 그런 시장이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 482

<- **이전**: [71. 디지털 트랜스포메이션 (DX / DT, Digital Transformation) - AI, 클라우드, 빅데이터로 비즈니스 모델](/studynote/07_enterprise_systems/01_strategy_governance/071_digital_transformation_dx/)
**다음**: [73. 옴니채널 (Omni-Channel) - 오프라인, 온라인, 모바일 등 모든 채널을 통합해 일관된 고객 경험 제공 (O2O의 진화)](/studynote/07_enterprise_systems/01_strategy_governance/073_omni_channel_o2o_evolution/) ->

---
