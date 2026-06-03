+++
title = "71. 블록체인 서비스형 (BaaS, Blockchain as a Service) - 클라우드 기반 블록체인 인프라 제공 서비스"
weight = 71
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BaaS는 [[004_blockchain|블록체인]] 네트워크 구축과 운영을 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]]로 제공하는 모델이다.
> 2. **가치**: 직접 노드를 운영하지 않고도 빠르게 [[004_blockchain|블록체인]] [[090_service_kubernetes_network_load_balancing|서비스]]를 실험할 수 있다.
> 3. **판단**: 인프라 복잡도를 줄이지만, [[090_service_kubernetes_network_load_balancing|서비스]] [[008_dependencies|종속성]]과 운영 [[164_policy|정책]]은 확인해야 한다.

---

## Ⅰ. 개요 및 필요성

[[004_blockchain|블록체인]]을 직접 깔려면 노드, [[303_authentication_authorization_patterns|인증]], 합의, 키 관리가 번거롭다. BaaS는 이를 줄여 준다.

그래서 PoC와 빠른 도입에 유리하다.

- **📢 섹션 요약 비유**: 집을 새로 짓지 않고 빌려 쓰는 [[004_blockchain|블록체인]] 공장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Cloud Platform
  ↓
BaaS
  ↓
Blockchain Network
  ↓
Application
```

| 요소 | 의미 |
| :-- | :-- |
| Managed Nodes | 관리형 노드 |
| [[014_api_posix|API]] / Console | 사용 인터페이스 |
| [[067_db_key_uniqueness_minimality|Key]] [[372_management|Management]] | 키 관리 |

BaaS는 배포, 확장, [[303_authentication_authorization_patterns|인증]], 모니터링을 [[090_service_kubernetes_network_load_balancing|서비스]]로 제공한다. 사용자는 비즈니스 로직에 집중할 수 있다.

- **📢 섹션 요약 비유**: 전기와 수도가 다 갖춰진 건물에 들어가는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 직접 구축 | [[186_baas_backend_as_a_service_firebase|BaaS]] |
| :-- | :-- | :-- |
| 운영 | 직접 | 위임 |
| 속도 | 느림 | 빠름 |
| 자유도 | 높음 | 제한 |

| 고려 | 의미 |
| :-- | :-- |
| [[254_cloud_vendor_lock_in_avoidance_portability_multi_cloud|Vendor Lock-in]] | [[008_dependencies|종속성]] |
| Governance | [[164_policy|정책]] |

BaaS는 도입 장벽을 낮추지만, 장기 운영에서 공급자 의존성을 고려해야 한다.

- **📢 섹션 요약 비유**: 편하지만 집주인 규칙은 따라야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 빠른 PoC가 필요한가?
2. 관리형 인프라가 유리한가?
3. 보안/키 관리가 제공되는가?
4. [[008_dependencies|종속성]] 리스크를 보는가?
5. 운영 비용을 비교했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- BaaS를 무조건 무료 인프라처럼 보는 설계
- 공급자 종속을 무시하는 설계
- 키 관리 책임을 흐리는 설계
- 실제 요구보다 과도하게 복잡한 설계

기술사 관점에서는 BaaS를 "[[004_blockchain|블록체인]] 인프라의 [[090_service_kubernetes_network_load_balancing|서비스]]화"로 설명해야 한다.

- **📢 섹션 요약 비유**: 직접 집을 짓지 않고 임대하는 방식이다.

---

## Ⅴ. 기대효과 및 결론

BaaS는 [[004_blockchain|블록체인]] 도입을 빠르게 만든다. 그래서 실험과 [[459_quic_fec_forward_error_correction|초기]] [[090_service_kubernetes_network_load_balancing|서비스]]에 적합하다.

결론적으로 BaaS는 클라우드 기반 [[004_blockchain|블록체인]] 인프라 [[090_service_kubernetes_network_load_balancing|서비스]]다.

- **📢 섹션 요약 비유**: [[004_blockchain|블록체인]] 장비를 빌려 쓰는 것이다.

---

## 관련 개념 맵

```text
Cloud
  ↓
BaaS
  ↓
Blockchain Network
  ↓
Application
```

---

## 관련 키워드 및 발전 흐름도

```text
Blockchain Infrastructure
  ↓
BaaS
  ↓
Managed Service
  ↓
PoC
```

---

## 어린이를 위한 3줄 비유 설명

[[004_blockchain|블록체인]]을 빌려 쓰는 거예요.  
직접 만들지 않아도 돼요.  
BaaS는 그런 [[090_service_kubernetes_network_load_balancing|서비스]]예요.
