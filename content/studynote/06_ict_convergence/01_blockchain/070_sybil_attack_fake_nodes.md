+++
title = "70. 시빌 공격 (Sybil Attack) - 한 명이 여러 개의 가짜 노드(신분)를 생성하여 투표율/합의를 조작하는 공격"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시빌 공격은 한 공격자가 다수의 가짜 신분을 만들어 네트워크 의사결정을 왜곡하는 공격이다.
> 2. **가치**: [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/), [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/), 평판 시스템에서 신원 기반 신뢰를 무너뜨린다.
> 3. **판단**: 가짜 노드 수가 많아질수록 합의와 투표가 왜곡되므로 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 중요하다.

---

## Ⅰ. 개요 및 필요성

네트워크가 "노드 수"를 신뢰하면 가짜 노드가 많아질 때 문제가 생긴다. 시빌 공격은 바로 그 허점을 노린다.

한 사람이 여러 신분을 만들어 영향력을 키우는 것이다.

- **📢 섹션 요약 비유**: 한 사람이 표를 여러 장 들고 온 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Attacker
  v create many identities
Fake Nodes
  v
Manipulated Consensus
```

| 요소 | 의미 |
| :-- | :-- |
| Identity | 노드 신원 |
| [Fake](/knowledge-base/studynote/04_software_engineering/11_testing_validation/855_fake_test_double/) Node | 가짜 참여자 |
| Consensus | 합의 왜곡 |

시빌 공격은 노드 수가 많아 보이면 신뢰가 올라가는 시스템의 약점을 이용한다.

- **📢 섹션 요약 비유**: 이름표를 여러 개 달고 사람 수를 부풀리는 것이다.

---

## Ⅲ. 비교 및 연결

| 공격 | 특징 | 차이 |
| :-- | :-- | :-- |
| Sybil | 신원 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) | 수량 기반 왜곡 |
| Eclipse | 연결 고립 | 특정 노드 포위 |
| 51% | 과반 장악 | 자원 기반 |

| 방어 | 의미 |
| :-- | :-- |
| Identity [Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| Cost to Create Identity | 비용 장벽 |

시빌 공격은 신원 자체를 믿기 어려운 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 특히 중요하다.

- **📢 섹션 요약 비유**: 사람 수를 속이면 투표판도 속는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 있는가?
2. 가짜 계정 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용이 있는가?
3. 평판/투표 가중치를 조정하는가?
4. 합의와 신원을 분리해서 보는가?
5. 방어 메커니즘을 설계했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 계정 수만 세는 설계
- 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 합의하는 설계
- 저비용 다중 계정 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 허용하는 설계
- Sybil, Eclipse, 51%를 혼동하는 설계

기술사 관점에서는 시빌 공격을 "신원 기반 합의 왜곡"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 이름을 여러 번 바꾸면 진짜 인원이 늘어난 것처럼 보인다.

---

## Ⅴ. 기대효과 및 결론

시빌 공격을 이해하면 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 신뢰 모델을 더 정확히 설계할 수 있다.

결론적으로 시빌 공격은 다수의 가짜 신분으로 합의와 투표를 조작하는 공격이다.

- **📢 섹션 요약 비유**: 한 사람이 여러 사람인 척하면 공정성이 무너진다.

---

## 관련 개념 맵

```text
Identity
  v
Sybil Attack
  v
Consensus Manipulation
  v
Defense
```

---

## 관련 키워드 및 발전 흐름도

```text
P2P Network
  v
Sybil Attack
  v
Identity Verification
  v
Trust Model
```

---

## 어린이를 위한 3줄 비유 설명

한 사람이 여러 명인 척해요.
그러면 표가 많아 보여요.
시빌 공격은 그런 속임수예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 552

<- **이전**: [69. 크립토재킹 (Cryptojacking) - 타인의 PC나 서버 리소스를 해킹하여 몰래 암호화폐를 채굴하는 공격](/knowledge-base/studynote/06_ict_convergence/01_blockchain/069_cryptojacking_malware_mining/)
**다음**: [71. 블록체인 서비스형 (BaaS, Blockchain as a Service) - 클라우드 기반 블록체인 인프라 제공 서비스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/071_baas_blockchain_as_a_service/) ->

---
