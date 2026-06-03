+++
title = "67. 51% 공격 (51% Attack) - 악의적 노드가 전체 해시 파워의 51% 이상을 장악해 장부를 조작하는 공격"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 51% 공격은 과반의 해시 파워나 지분을 장악해 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 합의를 흔드는 공격이다.
> 2. **가치**: 더블 스펜딩, reorg, 검열 가능성을 통해 [블록체인 보안](/knowledge-base/studynote/09_security/19_ai_advanced_security/989_blockchain_security/) 가정의 한계를 드러낸다.
> 3. **판단**: PoW와 PoS에서 공격 조건이 다르므로 합의 모델에 맞춰 위협을 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 다수결에 기대는 시스템이다. 따라서 과반이 한쪽으로 쏠리면 결과를 조작할 수 있다.

51% 공격은 이런 합의 구조를 직접 무너뜨리는 대표 위협이다.

- **📢 섹션 요약 비유**: 반장 투표에서 한쪽이 절반 이상을 차지하면 결과가 바뀌는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Majority Control
  ↓
Chain Reorganization
  ↓
Double Spending / Censorship
```

| 효과 | 의미 |
| :-- | :-- |
| Double Spending | 같은 자산 재사용 시도 |
| Reorg | 체인 재구성 |
| Censorship | 거래 배제 |

과반 자원을 가진 공격자는 자신에게 유리한 체인을 더 길게 만들 수 있다. 그래서 확정되지 않은 거래는 위험하다.

- **📢 섹션 요약 비유**: 기록부를 많이 가진 쪽이 더 유리해지는 상황이다.

---

## Ⅲ. 비교 및 연결

| 합의 방식 | 위험 |
| :-- | :-- |
| PoW | 해시 파워 과반 |
| PoS | 지분/검증자 과반 |
| [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) | quorum 파괴 또는 구성 공격 |

| 결과 | 설명 |
| :-- | :-- |
| Reorg | 기록 뒤집힘 |
| [Finality](/knowledge-base/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/) 약화 | 확정 신뢰 저하 |

51% 공격은 [블록체인 보안](/knowledge-base/studynote/09_security/19_ai_advanced_security/989_blockchain_security/)의 기본 가정을 시험하는 사례다.

- **📢 섹션 요약 비유**: 줄 서는 사람들 중 절반 이상이 한 편이면 순서가 바뀔 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 과반 장악 위험을 설명할 수 있는가?
2. 더블 스펜딩과 reorg를 구분하는가?
3. PoW/PoS 별 공격 조건을 아는가?
4. 확정성과 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 횟수를 이해하는가?
5. 분산도와 보안 가정을 평가하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 51% 공격을 단순 해킹으로만 보는 설계
- PoW와 PoS를 같은 기준으로 보는 설계
- 확정되지 않은 거래를 안전하다고 보는 설계
- 분산성 검토 없이 운영하는 설계

기술사 관점에서는 51% 공격을 "과반 장악형 합의 조작"으로 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: 숫자가 많아지면 규칙도 쉽게 바뀐다.

---

## Ⅴ. 기대효과 및 결론

51% 공격을 이해하면 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 설계에서 분산성과 완결성의 중요성을 분명히 볼 수 있다.

결론적으로 51% 공격은 과반 장악으로 장부를 조작하는 공격이다.

- **📢 섹션 요약 비유**: 사람들이 너무 한쪽에 많으면 결과가 흔들린다.

---

## 관련 개념 맵

```text
Majority Control
  ↓
51% Attack
  ↓
Reorg / Double Spending
  ↓
Blockchain Security
```

---

## 관련 키워드 및 발전 흐름도

```text
Consensus
  ↓
51% Attack
  ↓
Finality Risk
  ↓
Mitigation
```

---

## 어린이를 위한 3줄 비유 설명

한쪽 사람이 너무 많으면 결과가 바뀔 수 있어요.  
[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)도 똑같아요.  
51% 공격은 그런 과반 장악이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 552

← **이전**: [66. 지향성 비순환 그래프 (DAG, Directed Acyclic Graph) - 블록체인 대신 트랜잭션들이 거미줄처럼 서로를 증명하는](/knowledge-base/studynote/06_ict_convergence/01_blockchain/066_dag_directed_acyclic_graph_tangle/)
**다음**: [68. 이클립스 공격 (Eclipse Attack) - 특정 노드의 주변 P2P 연결을 악성 노드가 장악하여 네트워크를 고립시키고 허위](/knowledge-base/studynote/06_ict_convergence/01_blockchain/068_eclipse_attack_p2p_isolation/) →

---
