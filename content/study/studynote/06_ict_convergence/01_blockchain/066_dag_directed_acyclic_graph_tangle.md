---
title: 66. 지향성 비순환 그래프 (DAG, Directed Acyclic Graph) - 블록체인 대신 트랜잭션들이 거미줄처럼 서로를 증명하는
  분산 원장 구조 (IOTA의 Tangle)
tags:
- ict_convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[401_bayesian_network_dag_causality|DAG]]([[255_apache_airflow_dag|Directed Acyclic Graph]])는 블록이 아닌 [[191_transaction_concept_states|트랜잭션]]들이 서로를 [[316_reference_pattern_nosql|참조]]하며 확장되는 [[136_variance|분산]] 원장 구조다.
> 2. **가치**: Tangle 같은 구조는 참여가 늘수록 [[395_verification_process_review|검증]]도 함께 늘어나는 설계로, 높은 병렬성과 확장성을 노린다.
> 3. **판단**: [[004_blockchain|블록체인]]과 달리 선형 체인이 아니므로, 확정성, 공격 저항성, 네트워크 설계 특성을 따로 봐야 한다.

---

## Ⅰ. 개요 및 필요성

기존 [[004_blockchain|블록체인]]은 블록이 한 줄로 이어지기 때문에 병목이 생길 수 있다. DAG는 이 구조를 그물망처럼 바꿔 확장성을 높이려는 시도다.

IOTA의 Tangle은 대표적인 예로, 각 [[191_transaction_concept_states|트랜잭션]]이 이전 [[191_transaction_concept_states|트랜잭션]]을 [[395_verification_process_review|검증]]한다.

- **📢 섹션 요약 비유**: 한 줄 기차 대신 여러 사람이 서로 짐을 확인하며 연결되는 그물망이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Tx A → Tx B
  ↘   ↗
   Tx C → Tx D
```

| 요소 | 역할 |
| :-- | :-- |
| Node/[[191_transaction_concept_states|Transaction]] | 기록 단위 |
| Edge | 승인/[[316_reference_pattern_nosql|참조]] [[083_relationship_in_er_model|관계]] |
| Acyclic | 순환 없음 |
| Parallel [[396_validation|Validation]] | 동시에 여러 경로 [[395_verification_process_review|검증]] |

DAG에서는 새 [[191_transaction_concept_states|트랜잭션]]이 과거의 [[191_transaction_concept_states|트랜잭션]]을 승인하면서 네트워크에 기여한다. 그래서 참여가 늘수록 [[395_verification_process_review|검증]] 능력도 커질 수 있다.

- **📢 섹션 요약 비유**: 내가 새로 왔으면 앞사람 일을 도와야 다음 줄이 더 빨라지는 품앗이 구조다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[004_blockchain|Blockchain]] | [[401_bayesian_network_dag_causality|DAG]]/Tangle |
| :-- | :-- | :-- |
| 구조 | 선형 체인 | 그물망 |
| 확장성 | 제한적 | 높게 설계 가능 |
| 확정성 | 합의/블록 기반 | 구조별 상이 |

| 장점 | 단점 |
| :-- | :-- |
| 병렬성 | 공격 모델 복잡 |
| 수수료 감소 가능성 | 설계/보안 [[395_verification_process_review|검증]] 난도 높음 |

DAG는 [[004_blockchain|블록체인]]의 대체라기보다, 다른 [[191_transaction_concept_states|트랜잭션]] [[395_verification_process_review|검증]] 철학을 가진 구조다. 성능만 볼 게 아니라 보안 모델까지 같이 봐야 한다.

- **📢 섹션 요약 비유**: 한 줄 줄서기와 여러 줄 줄서기는 빠르기만 다른 게 아니라 규칙도 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. DAG의 [[395_verification_process_review|검증]] 규칙을 설명할 수 있는가?
2. 확정성과 공격 저항성을 이해하는가?
3. [[004_blockchain|블록체인]]과의 차이를 구분하는가?
4. 네트워크 참여가 늘 때의 장단을 아는가?
5. Tangle 같은 구현 예를 알고 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- DAG를 그냥 "빠른 [[004_blockchain|블록체인]]"으로만 보는 설계
- 공격 모델을 검토하지 않는 설계
- 확정성 문제를 무시하는 설계
- 구조만 보고 실사용을 단정하는 설계

기술사 관점에서는 DAG를 "체인 대체"가 아니라 "다른 원장의 설계 선택지"로 봐야 한다.

- **📢 섹션 요약 비유**: 선로가 하나가 아니라고 해서 자동으로 안전한 것은 아니다.

---

## Ⅴ. 기대효과 및 결론

DAG는 높은 병렬성과 확장성을 노리는 [[136_variance|분산]] 원장 구조다. 하지만 보안과 완결성의 균형을 함께 봐야 한다.

결론적으로 DAG는 [[004_blockchain|블록체인]]의 대안적 [[136_variance|분산]] 원장 설계다.

- **📢 섹션 요약 비유**: 길이 여러 개면 빨라질 수 있지만, 표지판도 더 잘 세워야 한다.

---

## 관련 개념 맵

```text
Transaction
  ↓
DAG
  ↓
Tangle
  ↓
Distributed Ledger
```

---

## 관련 키워드 및 발전 흐름도

```text
Blockchain
  ↓
DAG
  ↓
Tangle
  ↓
Scalable Ledger
```

---

## 어린이를 위한 3줄 비유 설명

한 줄로만 줄 서지 않아도 돼요.  
서로 도와서 다음 사람을 확인해요.  
DAG는 그런 그물망 같은 기록 방법이에요.
