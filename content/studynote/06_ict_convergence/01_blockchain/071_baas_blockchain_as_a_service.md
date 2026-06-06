---
title: "071. Baas Blockchain As A Service"
tags:
  - "ict_convergence"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BaaS는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 네트워크 구축과 운영을 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 제공하는 모델이다.
> 2. **가치**: 직접 노드를 운영하지 않고도 빠르게 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 실험할 수 있다.
> 3. **판단**: 인프라 복잡도를 줄이지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)과 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 확인해야 한다.

---

## Ⅰ. 개요 및 필요성

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)을 직접 깔려면 노드, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 합의, 키 관리가 번거롭다. BaaS는 이를 줄여 준다.

그래서 PoC와 빠른 도입에 유리하다.

- **📢 섹션 요약 비유**: 집을 새로 짓지 않고 빌려 쓰는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 공장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Cloud Platform
  v
BaaS
  v
Blockchain Network
  v
Application
```

| 요소 | 의미 |
| :-- | :-- |
| Managed Nodes | 관리형 노드 |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) / Console | 사용 인터페이스 |
| [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) | 키 관리 |

BaaS는 배포, 확장, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 모니터링을 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 제공한다. 사용자는 비즈니스 로직에 집중할 수 있다.

- **📢 섹션 요약 비유**: 전기와 수도가 다 갖춰진 건물에 들어가는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 직접 구축 | [BaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) |
| :-- | :-- | :-- |
| 운영 | 직접 | 위임 |
| 속도 | 느림 | 빠름 |
| 자유도 | 높음 | 제한 |

| 고려 | 의미 |
| :-- | :-- |
| [Vendor Lock-in](/studynote/06_ict_convergence/03_cloud_infrastructure/254_cloud_vendor_lock_in_avoidance_portability_multi_cloud/) | [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) |
| Governance | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |

BaaS는 도입 장벽을 낮추지만, 장기 운영에서 공급자 의존성을 고려해야 한다.

- **📢 섹션 요약 비유**: 편하지만 집주인 규칙은 따라야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 빠른 PoC가 필요한가?
2. 관리형 인프라가 유리한가?
3. 보안/키 관리가 제공되는가?
4. [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 리스크를 보는가?
5. 운영 비용을 비교했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- BaaS를 무조건 무료 인프라처럼 보는 설계
- 공급자 종속을 무시하는 설계
- 키 관리 책임을 흐리는 설계
- 실제 요구보다 과도하게 복잡한 설계

기술사 관점에서는 BaaS를 "[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 인프라의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)화"로 설명해야 한다.

- **📢 섹션 요약 비유**: 직접 집을 짓지 않고 임대하는 방식이다.

---

## Ⅴ. 기대효과 및 결론

BaaS는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 도입을 빠르게 만든다. 그래서 실험과 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 적합하다.

결론적으로 BaaS는 클라우드 기반 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 인프라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다.

- **📢 섹션 요약 비유**: [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 장비를 빌려 쓰는 것이다.

---

## 관련 개념 맵

```text
Cloud
  v
BaaS
  v
Blockchain Network
  v
Application
```

---

## 관련 키워드 및 발전 흐름도

```text
Blockchain Infrastructure
  v
BaaS
  v
Managed Service
  v
PoC
```

---

## 어린이를 위한 3줄 비유 설명

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)을 빌려 쓰는 거예요.
직접 만들지 않아도 돼요.
BaaS는 그런 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 552

<- **이전**: [70. 시빌 공격 (Sybil Attack) - 한 명이 여러 개의 가짜 노드(신분)를 생성하여 투표율/합의를 조작하는 공격](/studynote/06_ict_convergence/01_blockchain/070_sybil_attack_fake_nodes/)
**다음**: [72. ERC-20 (이더리움 대체 가능 토큰 표준)](/studynote/06_ict_convergence/01_blockchain/072_erc_20_fungible_token_standard/) ->

---
