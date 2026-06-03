+++
title = "66. 지향성 비순환 그래프 (DAG, Directed Acyclic Graph) - 블록체인 대신 트랜잭션들이 거미줄처럼 서로를 증명하는 분산 원장 구조 (IOTA의 Tangle)"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DAG(Directed Acyclic Graph, 지향성 비순환 그래프)는 블록이 아닌 개별 트랜잭션들이 서로를 참조·검증하며 그물망 구조로 연결되는 분산 원장 구조로, 선형 체인의 확장성 한계를 극복하려는 대안적 설계다.
> 2. **가치**: 새 트랜잭션이 과거 트랜잭션을 검증하는 품앗이 구조로 참여자가 늘수록 검증 능력도 함께 증가하고, 블록 생성 대기 없이 병렬로 처리하여 IoT 소액 결제처럼 수수료 없는 고처리량 거래가 이론적으로 가능하다.
> 3. **판단 포인트**: DAG는 선형 블록체인과 근본적으로 다른 확정성(Finality) 모델과 보안 가정을 가지므로, 단순히 '빠른 블록체인'으로 보지 않고 검증 메커니즘, 공격 모델, 완결성 보장 방식을 별도로 분석해야 한다.

---

## Ⅰ. 개요 및 필요성

블록체인의 선형(Linear) 구조는 확장성의 근본적인 한계를 가진다. 비트코인은 약 10분에 하나의 블록, 이더리움은 약 12초에 하나의 블록을 생성하는데, 이 단일 체인에 모든 트랜잭션을 순서대로 넣어야 하므로 처리량(TPS)에 한계가 있다. 비트코인의 약 7 TPS, 이더리움의 약 30 TPS는 비자(Visa)의 수만 TPS와 비교하면 수백~수천 배 낮다.

DAG는 이 병목 구조를 해체하는 아이디어다. 블록이라는 묶음 단위를 없애고, 개별 트랜잭션이 네트워크의 기본 단위가 된다. 각 트랜잭션은 이전 트랜잭션 두 개(또는 그 이상)를 참조하고 검증함으로써 네트워크에 기여한다. 이렇게 되면 여러 트랜잭션이 동시에 병렬로 처리될 수 있어 이론적으로 무한한 확장성을 달성할 수 있다.

이 개념을 구현한 대표 사례가 IOTA 프로젝트의 Tangle이다. IOTA는 IoT(사물인터넷) 기기 간 초소액 결제를 수수료 없이 처리하는 것을 목표로 2015년 설계됐다. IoT 기기는 수십 원 단위의 소액 결제가 필요한데, 블록체인의 가스비나 수수료가 결제 금액보다 클 수 있다. DAG 구조는 이런 문제를 해결하는 데 적합한 후보로 제시됐다.

2022년 이후 DAG 기반 합의는 새로운 방향으로 발전하고 있다. Aptos, Sui 등 차세대 블록체인은 DAG 기반 멤풀(DAG-Mempool)을 합의 알고리즘(Bullshark, Narwhal)과 결합하여 높은 처리량과 낮은 지연시간을 달성하고 있다. 이는 전통적인 단선 블록 체인과 순수 DAG를 결합한 하이브리드 접근이다.

- **📢 섹션 요약 비유**: 한 줄 기차 대신 여러 사람이 서로 짐을 확인하며 연결되는 그물망이다. 참여자가 많아질수록 그물이 촘촘해져서 더 많은 짐을 한꺼번에 나를 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DAG 구조의 기본 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선형 블록체인 vs DAG 구조 비교</div></div>
<div class="kb-diagram-note">선형 블록체인:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">블록1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">블록2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">블록3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">블록4</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-note">(병목: 한 번에 하나의 블록만 추가 가능)</div>
<div class="kb-diagram-note">DAG (Tangle 구조):</div>
<div class="kb-diagram-note">Tx-A ► Tx-E</div>
<div class="kb-diagram-note">↘ ↗</div>
<div class="kb-diagram-note">Tx-C ► Tx-F</div>
<div class="kb-diagram-note">↗ ↘</div>
<div class="kb-diagram-note">Tx-B ► Tx-D</div>
<div class="kb-diagram-note">(여러 트랜잭션이 동시에 처리 가능, 병렬성 극대화)</div>
</div>
</div>



### 2. DAG의 핵심 속성

| 속성 | 설명 |
| :--- | :--- |
| 지향성 (Directed) | 엣지(Edge)에 방향이 있음 - 과거에서 현재 방향으로만 참조 |
| 비순환 (Acyclic) | 사이클(순환 참조)이 존재하지 않음 - 시간 순서 보장 |
| 병렬 처리 | 여러 트랜잭션이 동시에 처리 및 검증 가능 |
| 자기 검증 | 새 트랜잭션이 과거 트랜잭션을 검증하며 네트워크에 기여 |

### 3. IOTA Tangle의 동작 원리

IOTA Tangle에서 새 트랜잭션을 추가하는 과정:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Tangle 트랜잭션 추가 과정</div></div>
<div class="kb-diagram-note">1단계: 사용자가 새 트랜잭션(Tx-New) 생성</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2단계: 팁 선택 알고리즘(Tip Selection Algorithm) 실행</div>
<div class="kb-diagram-tree-item" style="--depth:2">아직 확인되지 않은 "팁(Tip)" 트랜잭션 2개 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3단계: 선택한 2개 트랜잭션 검증</div>
<div class="kb-diagram-tree-item" style="--depth:2">유효성 확인 (서명, 잔액 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">4단계: 작업증명(PoW) 또는 스팸 방지 작업 수행</div>
<div class="kb-diagram-tree-item" style="--depth:2">소량의 연산으로 스팸 트랜잭션 방지</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">5단계: Tx-New를 네트워크에 전파</div>
<div class="kb-diagram-tree-item" style="--depth:2">두 팁 트랜잭션을 부모(Parent)로 참조</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">6단계: Tx-New 자체가 새로운 "팁"이 됨</div>
<div class="kb-diagram-tree-item" style="--depth:2">미래 트랜잭션이 이를 검증할 때까지 팁 상태 유지</div>
</div>
</div>



### 4. 팁 선택 알고리즘 (Tip Selection Algorithm)

팁 선택은 DAG에서 어느 트랜잭션을 참조할지 결정하는 핵심 로직이다. 나쁜 팁 선택 알고리즘은 네트워크 병목이나 공격에 취약해진다.

| 알고리즘 | 방식 | 특징 |
| :--- | :--- | :--- |
| 랜덤 워크 (Random Walk) | 제네시스부터 무작위로 탐색 | 단순하지만 오래된 팁 무시 가능 |
| 가중 랜덤 워크 (URTS) | 누적 가중치 기반 선택 | 더 안전한 트랜잭션 선호 |
| 균형 팁 선택 | 누적 가중치 + 신선도 고려 | 고아 트랜잭션 감소 |

### 5. DAG 기반 현대 블록체인 (DAG-BFT 하이브리드)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">차세대 DAG 합의 - Narwhal/Bullshark (Aptos, Sui)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">단계 1: DAG-Mempool (Narwhal)</div></div>
<div class="kb-diagram-note">검증자 각각이 독립적으로 트랜잭션 배치(Batch) 생성</div>
<div class="kb-diagram-note">↓ 각 배치를 DAG 형태로 전파</div>
<div class="kb-diagram-note">검증자들이 배치를 참조하며 DAG 구성</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">단계 2: 합의 (Bullshark)</div></div>
<div class="kb-diagram-note">DAG 구조에서 합의 라운드 진행</div>
<div class="kb-diagram-note">↓ 특정 "앵커(Anchor)"가 총 순서 결정</div>
<div class="kb-diagram-note">BFT 합의로 즉각적 완결성 달성</div>
<div class="kb-diagram-note">결과: 높은 처리량(DAG 병렬성) + 즉각 완결성(BFT)</div>
</div>
</div>



### 6. 주요 DAG 기반 프로젝트

| 프로젝트 | DAG 방식 | 목적 | 상태 |
| :--- | :--- | :--- | :--- |
| IOTA/Tangle | 순수 DAG | IoT 소액 결제 | 운영 중 |
| Nano | Block-Lattice | 빠른 결제 | 운영 중 |
| Fantom (Lachesis) | DAG-BFT 하이브리드 | EVM 호환 고속 체인 | 운영 중 |
| Aptos (Narwhal/Bullshark) | DAG-Mempool + BFT | 고속 Layer-1 | 운영 중 |
| Sui (Narwhal/Bullshark) | DAG-Mempool + BFT | 고속 Layer-1 | 운영 중 |
| Hedera Hashgraph | Hashgraph (DAG 변형) | 엔터프라이즈 | 운영 중 |

- **📢 섹션 요약 비유**: 내가 새로 왔으면 앞사람 일을 도와야 다음 줄이 더 빨라지는 품앗이 구조다. 새 참여자가 과거 참여자의 일을 검증해 주면서 자신도 네트워크에 기여한다.

---

## Ⅲ. 비교 및 연결

### 1. 블록체인 vs DAG 상세 비교

| 항목 | 선형 블록체인 | DAG |
| :--- | :--- | :--- |
| 기본 단위 | 블록 (트랜잭션 묶음) | 개별 트랜잭션 |
| 구조 | 선형 체인 | 그물망 그래프 |
| 병렬성 | 낮음 (단일 체인) | 높음 (다중 경로) |
| 완결성 | 블록 기반 (명확) | 구조별 상이 (복잡) |
| 수수료 | 있음 (채굴자/검증자 보상) | 이론상 없음 (자기 검증) |
| 처리량 확장 | Layer-2로 보완 | 참여자 증가로 자연 증가 |
| 보안 모델 | 확립된 PoW/PoS | 프로젝트별 다양, 검증 중 |
| 공격 취약점 | 51% Attack | 파라사이트 체인, 지향성 공격 |

### 2. DAG 기반 시스템의 고유한 보안 위협

| 공격 유형 | 설명 | 방어 방법 |
| :--- | :--- | :--- |
| 파라사이트 체인 공격 | 별도의 숨겨진 DAG 서브그래프를 생성하다가 공개 | 팁 선택 알고리즘 개선 |
| 분열 공격 (Split Attack) | 네트워크를 두 그룹으로 나누어 각각 다른 DAG 생성 | 코디네이터 노드 또는 추가 합의 |
| 지연 공격 (Lazy Tip Selection) | 의도적으로 비인기 팁만 선택하여 일부 트랜잭션 고아화 | 팁 선택 인센티브 설계 |
| 고아 트랜잭션 (Orphan Tx) | 참조되지 않아 영구 미확정 상태가 되는 트랜잭션 | 팁 선택 알고리즘 보완 |

### 3. IOTA vs Nano 비교

| 항목 | IOTA/Tangle | Nano/Block-Lattice |
| :--- | :--- | :--- |
| DAG 구조 | 전체 트랜잭션이 하나의 DAG | 각 계정마다 별도의 블록 체인 |
| 검증 방식 | 새 Tx가 2개 이전 Tx 검증 | 수신자가 별도로 수신 확인 |
| 수수료 | 없음 | 없음 |
| 코디네이터 | 초기 보안용 중앙 노드 존재 (현재 제거 진행 중) | 없음 |
| IoT 적합성 | 높음 | 중간 |

- **📢 섹션 요약 비유**: 한 줄 줄서기(블록체인)와 여러 줄 줄서기(DAG)는 빠르기만 다른 게 아니라 규칙도, 줄 관리 방법도 다르다. 여러 줄은 빠르지만, 어느 줄이 올바른 줄인지 판단하는 기준이 더 복잡해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **완결성 모델 이해**: DAG 시스템의 완결성은 어떻게 정의되는가? 전통적인 블록 기반 확인 수 개념과 어떻게 다른가?
2. **팁 선택 알고리즘 검토**: 채택한 팁 선택 알고리즘이 공격(파라사이트 체인, 게으른 팁 선택)에 얼마나 강건한가?
3. **코디네이터 의존성**: IOTA처럼 중앙화된 보안 노드(코디네이터)에 의존하는 경우, 이는 탈중앙화 가정과 모순되지 않는가?
4. **보안 모델 검증**: DAG 구조의 보안 모델이 학술적으로 검증된 수준인가? 블록체인 PoW/PoS 대비 검증 이력이 어느 정도인가?
5. **네트워크 크기 의존성**: DAG 보안은 참여 노드 수에 의존하는 경우가 많다. 초기 단계에서 소수 노드만 있을 때 보안이 어떻게 유지되는가?
6. **용도 적합성**: IoT 소액 결제, 고처리량 데이터 기록 등 DAG가 실제로 우위를 보이는 사용 사례인가?

### 안티패턴

- **DAG를 단순히 '빠른 블록체인'으로 보는 설계**: DAG는 블록체인의 속도 개선판이 아니라 근본적으로 다른 원장 아키텍처다. 완결성, 보안 모델, 공격 벡터가 모두 다르다.

- **보안 모델 검토 없는 도입**: 블록체인 PoW는 수십 년의 운영 이력이 있지만, 많은 DAG 프로젝트는 상대적으로 새롭고 실전 검증이 부족하다. "이론적으로 안전하다"와 "실제로 안전하다"는 다르다.

- **확정성 문제 무시**: 순수 DAG에서는 트랜잭션의 '최종 확정' 시점이 명확하지 않을 수 있다. 결제 시스템에서 "언제 완결됐는가"를 정의하지 않으면 설계에 구멍이 생긴다.

- **초기 네트워크 중앙화 무시**: IOTA는 초기 보안을 위해 코디네이터(Coordinator)라는 중앙화 컴포넌트를 사용했다. 탈중앙화를 주장하면서 중앙 관리자가 있는 설계는 가정과 현실의 불일치다.

기술사 관점에서는 DAG를 '체인의 대체'가 아니라 '다른 트랜잭션 검증 철학을 가진 원장 설계 선택지'로 봐야 한다. 블록체인이 성숙한 보안 모델을 가진 반면, DAG는 더 높은 확장성을 노리지만 새로운 보안 과제를 수반한다.

- **📢 섹션 요약 비유**: 선로가 하나가 아니라고 해서 자동으로 더 안전한 것은 아니다. 여러 선로가 있으면 더 많이 달릴 수 있지만, 어떤 선로가 올바른 방향인지 확인하는 신호 체계도 그에 맞게 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론

DAG 기반 분산 원장이 성공적으로 구현될 경우 기대 효과:

**IoT 결제 혁신**: 수수료 없는 초소액 결제로 IoT 기기 간 M2M(Machine-to-Machine) 자율 결제가 현실화된다. 스마트 그리드에서 전력을 공급한 만큼 자동으로 결제하거나, 자율주행차가 도로 사용료를 실시간으로 지불하는 시나리오가 가능해진다.

**높은 처리량**: 참여자가 늘수록 처리 능력이 함께 증가하는 긍정적 네트워크 효과로, 이론적으로 수십만 TPS 이상의 처리량을 달성할 수 있다.

**현재 한계와 진화**: 순수 DAG(IOTA Tangle)는 초기 단계에서 코디네이터 의존성 등 중앙화 문제를 겪었다. 최신 트렌드는 DAG-BFT 하이브리드(Narwhal/Bullshark)가 더 현실적인 해결책으로 부상하고 있다. Aptos, Sui 등이 이 방향으로 수천 TPS를 달성하며 상용화에 성공하고 있다.

결론적으로 DAG는 블록체인의 대안적 분산 원장 설계로서, 선형 체인의 확장성 한계를 극복하는 유망한 접근법이다. 하지만 보안 모델의 성숙도, 완결성 보장, 공격 저항성을 단계적으로 검증하면서 도입해야 한다.

- **📢 섹션 요약 비유**: 길이 여러 개면 빨라질 수 있지만, 표지판도 더 잘 세워야 하고 길이 엉키지 않도록 교통 규칙도 더 세심하게 만들어야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 선형 블록체인 | DAG가 극복하려는 확장성 병목 |
| IOTA/Tangle | 대표적 DAG 구현체, IoT 결제 목적 |
| Nano/Block-Lattice | 계정별 독립 체인을 DAG로 연결 |
| 팁 선택 알고리즘 | DAG에서 참조 트랜잭션 선택 방법 |
| Narwhal/Bullshark | 차세대 DAG-BFT 합의 알고리즘 |
| 완결성(Finality) | DAG에서 트랜잭션 확정 판단의 어려움 |
| 고아 트랜잭션 | 참조되지 않아 미확정 상태로 남는 트랜잭션 |
| IoT 소액 결제 | DAG의 핵심 사용 사례 |
| 병렬 처리 | DAG의 핵심 성능 이점 |
| Aptos, Sui | DAG-BFT 하이브리드 적용 현대 블록체인 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">DAG 기반 분산 원장 발전 흐름</div></div>
<div class="kb-diagram-note">블록체인 확장성 한계 인식 (2015~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IOTA Tangle 설계 (2015)</div>
<div class="kb-diagram-note">순수 DAG, IoT 소액 결제 목적</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Nano Block-Lattice (2018)</div>
<div class="kb-diagram-note">계정별 체인, 무수수료 결제</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DAG-BFT 하이브리드 연구 (2020~)</div>
<div class="kb-diagram-note">Narwhal(DAG Mempool) + Bullshark(합의)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Aptos, Sui 등 상용 적용 (2022~)</div>
<div class="kb-diagram-note">수천 TPS, 즉각 완결성 달성</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: DAG + Layer-2 결합 연구</div>
<div class="kb-diagram-note">더 높은 처리량, 낮은 지연 목표</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">미래: 수십만 TPS 목표 차세대 인프라</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 블록체인은 한 줄로 기차가 달리는 것처럼 순서대로 기록해요. 그런데 사람이 많으면 줄이 너무 길어져요.
2. DAG는 여러 사람이 서로의 짐을 확인하면서 동시에 이동하는 것처럼, 여러 거래를 한꺼번에 처리해요.
3. 그래서 이론적으로는 참여자가 많을수록 더 빠르게 처리할 수 있는 그물망 장부예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 552

← **이전**: [65. 합의 완결성 (Finality) - 블록이 체인에 기록되어 뒤집히지 않음이 보장되는 상태 (PoW는 확률적 완결성, BFT는 즉각적](/knowledge-base/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/)
**다음**: [67. 51% 공격 (51% Attack) - 악의적 노드가 전체 해시 파워의 51% 이상을 장악해 장부를 조작하는 공격](/knowledge-base/studynote/06_ict_convergence/01_blockchain/067_51_percent_attack_double_spending/) →

---
