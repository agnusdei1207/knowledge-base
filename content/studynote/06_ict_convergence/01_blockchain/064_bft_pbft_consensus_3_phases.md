+++
title = "64. BFT 합의의 3단계 - Pre-prepare, Prepare, Commit"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PBFT(Practical Byzantine Fault Tolerance)는 비잔틴 결함(Byzantine Fault), 즉 악의적이거나 결함 있는 노드가 존재하는 환경에서도 Pre-prepare → Prepare → Commit의 3단계 투표 과정을 통해 일관된 합의를 빠르게 확정하는 분산 합의 알고리즘이다.
> 2. **가치**: 작업증명(PoW)처럼 막대한 에너지를 소비하지 않고, 다중 메시지 서명 교환만으로 최종성(Finality)을 즉각 보장하며, n개 노드 중 f개가 Byzantine 결함이어도 n ≥ 3f+1 이면 합의를 달성한다.
> 3. **판단 포인트**: PBFT는 노드 수가 늘어날수록 메시지 복잡도가 O(n²)로 증가하므로 소규모 허가형(Permissioned) 네트워크, 컨소시엄 블록체인에 적합하며, 공개형 대규모 네트워크에는 적합하지 않다.

---

## Ⅰ. 개요 및 필요성

분산 시스템에서 노드 간 합의(Consensus)는 핵심 과제다. 단순히 노드가 오프라인이 되는 충돌 결함(Crash Fault)과 달리, Byzantine 결함은 노드가 의도적으로 잘못된 메시지를 보내거나 다른 노드에게 모순된 응답을 하는 훨씬 심각한 문제다. 비잔틴 장군 문제(Byzantine Generals Problem)는 1982년 램포트, 쇼스탁, 피스(Lamport, Shostak, Pease)가 제시한 이 개념의 고전적 표현이다.

PBFT(Practical Byzantine Fault Tolerance)는 1999년 카스트로(Castro)와 리스코프(Liskov)가 제안한 알고리즘으로, Byzantine 결함이 있는 환경에서 실용적인 성능으로 합의를 달성하는 방법을 제시했다. 이전 BFT 알고리즘들이 이론적으로만 가능했던 것과 달리, PBFT는 실제 분산 파일 시스템에 적용 가능한 수준의 성능을 보여줬다.

블록체인 맥락에서 PBFT의 중요성은 허가형 블록체인(Hyperledger Fabric, Quorum 등) 설계에 있다. 금융 기관, 공급망, 의료 등 서로 신뢰하지만 완전히 믿지는 못하는 컨소시엄 환경에서, PoW의 에너지 낭비 없이 빠른 확정성을 제공하는 합의 메커니즘으로 PBFT 계열 알고리즘이 널리 사용된다.

- **📢 섹션 요약 비유**: 회의실에서 중요한 결정을 내릴 때, 거짓말하는 사람이 섞여 있어도 '규정 정족수 이상의 도장'을 모아야만 최종 결론이 확정되는 구조다. 반대하는 사람 몇 명이 있어도 규칙이 지켜지면 회의가 성립된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. PBFT 3단계 합의 프로토콜

PBFT는 클라이언트가 요청을 보내면, 프라이머리(Primary, 리더) 노드가 이를 수신하고 3단계를 거쳐 합의를 달성한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">PBFT 3단계 합의 흐름도</div></div>
<div class="kb-diagram-note">클라이언트 (Client)</div>
<div class="kb-diagram-note">요청 (Request)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">프라이머리 노드 (Primary / Leader)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1단계</div><div class="kb-diagram-note">PRE-PREPARE 메시지 브로드캐스트</div></div>
<div class="kb-diagram-note">→ 모든 레플리카에 제안 번호(n)와 내용(m) 전달</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">모든 레플리카 노드 (Replica Nodes)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2단계</div><div class="kb-diagram-note">PREPARE 메시지 브로드캐스트</div></div>
<div class="kb-diagram-note">→ 제안 수신 확인, 서로에게 검증 메시지 전달</div>
<div class="kb-diagram-note">→ 2f+1 이상 PREPARE 메시지 수집 시 다음 단계</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">모든 레플리카 노드</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3단계</div><div class="kb-diagram-note">COMMIT 메시지 브로드캐스트</div></div>
<div class="kb-diagram-note">→ 최종 확인 메시지 서로에게 전달</div>
<div class="kb-diagram-note">→ 2f+1 이상 COMMIT 메시지 수집 시 실행</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">모든 레플리카 노드 (상태 업데이트)</div>
<div class="kb-diagram-note">요청 실행 + 클라이언트에 응답 전송</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클라이언트 (f+1 이상 동일 응답 수신 시 합의 완료)</div>
</div>
</div>



### 2. 각 단계 상세 설명

| 단계 | 메시지 | 발신자 | 수신자 | 목적 |
| :--- | :--- | :--- | :--- | :--- |
| 0. Request | 요청 | 클라이언트 | 프라이머리 | 서비스 요청 |
| 1. Pre-prepare | PRE-PREPARE | 프라이머리 | 모든 레플리카 | 제안 배포 및 순서 지정 |
| 2. Prepare | PREPARE | 각 레플리카 | 모든 다른 레플리카 | 제안 검증 및 동의 표명 |
| 3. Commit | COMMIT | 각 레플리카 | 모든 다른 레플리카 | 최종 확정 투표 |
| 4. Reply | REPLY | 각 레플리카 | 클라이언트 | 실행 결과 응답 |

### 3. Byzantine Fault Tolerance 수학

n개 노드에서 f개의 Byzantine 결함 노드를 허용하려면:

```
조건: n ≥ 3f + 1
이유:
 - f개 결함 노드가 거짓 투표를 해도
 - 2f+1 개의 정직한 노드가 quorum을 형성해야 함
 - quorum = 2f+1
 - 두 quorum의 교집합에는 최소 1개의 정직한 노드 보장

예시:
 - n=4, f=1 (노드 4개, 결함 1개 허용)
 - n=7, f=2 (노드 7개, 결함 2개 허용)
 - n=10, f=3 (노드 10개, 결함 3개 허용)
```

### 4. 메시지 복잡도 분석

| 단계 | 메시지 수 |
| :--- | :--- |
| Pre-prepare | O(n) |
| Prepare | O(n²) |
| Commit | O(n²) |
| **전체** | **O(n²)** |

n=4 일 때: Prepare+Commit = 4×3×2 = 24개 메시지
n=100 일 때: 100×99×2 ≈ 19,800개 메시지
n=1,000 일 때: 약 2,000,000개 메시지

이것이 PBFT가 대규모 네트워크에 적합하지 않은 이유다.

### 5. View Change (뷰 변경, 리더 교체)

프라이머리 노드가 Byzantine 결함이거나 응답이 없으면 View Change 프로토콜이 활성화된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">View Change 흐름</div></div>
<div class="kb-diagram-note">프라이머리 응답 없음/오류 감지</div>
<div class="kb-diagram-note">타임아웃</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">레플리카들이 VIEW-CHANGE 메시지 브로드캐스트</div>
<div class="kb-diagram-note">새로운 뷰 번호 v+1 제안</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">새 뷰 번호에 2f+1 이상 동의</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">새 프라이머리 선출 (뷰 번호 v+1 기준)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NEW-VIEW 메시지 발송 및 정상 운영 재개</div>
</div>
</div>



### 6. PBFT 변형 알고리즘 비교

| 알고리즘 | 주요 개선점 | 사용처 |
| :--- | :--- | :--- |
| PBFT | 원본 3단계 BFT | 컨소시엄 블록체인 |
| Tendermint | PBFT 기반 + 라운드 투표 | Cosmos 생태계 |
| HotStuff | O(n) 메시지 복잡도 | Facebook (Meta) Diem |
| IBFT (Istanbul BFT) | Ethereum 기반 허가형 체인 | Quorum, Hyperledger Besu |
| BFT-SMaRt | 자바 구현 BFT | Hyperledger Fabric v1 |
| LibraBFT/DiemBFT | HotStuff 변형 | Aptos, Sui |

- **📢 섹션 요약 비유**: 반대하는 사람이 몇 명 있어도, 규정 정족수를 채운 도장이 모여야 서류가 통과된다. 정족수(quorum)가 핵심이다. 그리고 회의 진행자(프라이머리)가 말썽을 부리면 교체(View Change)한다.

---

## Ⅲ. 비교 및 연결

### 1. 합의 알고리즘 종합 비교

| 합의 알고리즘 | 결함 유형 | 최종성 | 에너지 | 확장성 | 적용 네트워크 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PoW | Byzantine | 확률적 | 매우 높음 | 낮음 | Bitcoin, 공개형 |
| PoS | Byzantine | 확률적/결정적 | 낮음 | 중간 | Ethereum 2.0 |
| PBFT | Byzantine | 즉각적 | 매우 낮음 | 낮음 (O(n²)) | 허가형, 컨소시엄 |
| Raft | Crash | 즉각적 | 낮음 | 중간 | 분산 DB, K8s etcd |
| HotStuff | Byzantine | 즉각적 | 낮음 | 높음 (O(n)) | Aptos, Sui |
| Tendermint | Byzantine | 즉각적 | 낮음 | 중간 | Cosmos |

### 2. PBFT vs Raft 비교

| 항목 | PBFT | Raft |
| :--- | :--- | :--- |
| 결함 모델 | Byzantine Fault (악의적) | Crash Fault (단순 장애) |
| 네트워크 | 허가형 블록체인 | 분산 데이터베이스 |
| 리더 선출 | View Change | 리더 선출 투표 |
| 메시지 복잡도 | O(n²) | O(n) |
| 보안성 | 높음 (악의적 노드 대응) | 중간 (단순 장애만 대응) |
| 사용 사례 | Hyperledger, Quorum | etcd, Consul, CockroachDB |

### 3. 허가형 블록체인에서 PBFT의 위치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">허가형 블록체인 합의 메커니즘 선택</div></div>
<div class="kb-diagram-note">신뢰 모델 결정</div>
<div class="kb-diagram-tree-item" style="--depth:2">노드 간 완전 신뢰 → Raft (Crash Fault Tolerant)</div>
<div class="kb-diagram-tree-item" style="--depth:2">노드 일부 불신 가능 → PBFT 계열 (Byzantine Fault Tolerant)</div>
<div class="kb-diagram-tree-item" style="--depth:8">소규모 (&lt; 20 노드) → PBFT, IBFT</div>
<div class="kb-diagram-tree-item" style="--depth:8">중대규모 (&gt; 20 노드) → HotStuff, Tendermint</div>
</div>
</div>



- **📢 섹션 요약 비유**: 작은 회의실에서는 전원이 손들기를 해도 되지만, 큰 운동장에서는 너무 느려진다. PBFT는 정예 소수 회의에 최적화된 합의 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **결함 모델 명확화**: 처리해야 하는 결함이 단순 장애(Crash Fault)인가, 악의적 결함(Byzantine Fault)인가? Byzantine Fault가 없다면 Raft로 충분하다.
2. **노드 수 계산**: n ≥ 3f+1 조건을 충족하는가? 허용할 결함 수(f)에 맞는 노드 수를 정확히 계산했는가?
3. **quorum 조건 이해**: 2f+1 이상의 PREPARE/COMMIT 메시지를 수집해야 다음 단계로 진행됨을 이해하고 있는가?
4. **View Change 처리**: 프라이머리 노드 실패 시 View Change 메커니즘이 구현되어 있는가? View Change 타임아웃 값이 적절한가?
5. **성능 한계 인식**: O(n²) 메시지 복잡도를 감안할 때 노드 수 증가에 따른 성능 저하를 수용할 수 있는가? 수십 개 이상 노드에서는 HotStuff 계열 검토가 필요하다.
6. **허가형 네트워크 조건**: PBFT는 알려진 참여자 집합에서 동작한다. 참여자 등록, 제거, 인증 체계가 갖춰져 있는가?
7. **네트워크 동기성 가정**: PBFT는 부분 동기(Partial Synchrony) 모델에서 동작한다. 극도로 불안정한 네트워크에서는 View Change가 과다 발생할 수 있다.

### 안티패턴

- **공개형 대규모 네트워크에 PBFT 그대로 적용**: 이더리움이나 비트코인 같은 수천~수만 노드 네트워크에 PBFT를 적용하면 메시지 폭발로 시스템이 동작 불가능해진다.

- **2f+1 quorum 조건 무시**: PBFT가 'f개 결함을 허용한다'는 표현만 기억하고, 정확한 quorum 조건(2f+1)을 놓치는 경우가 많다. quorum이 잘못 설정되면 두 결론이 동시에 확정되는 포킹(Forking) 문제가 발생한다.

- **View Change 없는 PBFT 설계**: 프라이머리 노드 장애 시 View Change 없이는 시스템이 완전히 멈춘다. View Change 프로토콜은 선택 사항이 아니라 필수다.

- **성능만 보고 Byzantine Fault 무시**: 허가형 네트워크에서도 내부 위협(내부자 공격)이 존재할 수 있다. 신뢰할 수 없는 노드가 있는 환경에서 Raft를 사용하면 하나의 악의적 노드가 전체 시스템을 망가뜨릴 수 있다.

기술사 관점에서는 PBFT를 단순히 '3단계 투표'로 외우는 것보다, '왜 3f+1 노드가 필요하고, 각 단계가 무엇을 보장하는가'를 설명할 수 있어야 한다. 특히 quorum(2f+1) 개념이 두 quorum의 교집합에 정직한 노드가 반드시 포함됨을 보장한다는 핵심 논리를 이해해야 한다.

- **📢 섹션 요약 비유**: 소수 정예 회의는 빠르지만, 사람이 너무 많으면 회의가 길어진다. 그리고 회의 진행자가 이상한 소리를 해도, 규정 정족수 이상이 동의해야만 결론이 나는 민주적 절차가 있다.

---

## Ⅴ. 기대효과 및 결론

PBFT는 분산 합의 알고리즘의 이정표다. 이론으로만 존재하던 BFT 합의를 실용적인 수준으로 끌어올려, 허가형 분산 시스템에서 Byzantine 결함을 견디는 빠른 합의를 가능하게 했다.

**정량적 효과**: 허가형 블록체인에서 PBFT 사용 시 초당 수천 건의 트랜잭션 처리가 가능하며, PoW 대비 수백만 배 이상의 에너지를 절감한다. Hyperledger Fabric의 경우 PBFT 계열 합의로 초당 수천 TPS(Transactions Per Second)를 달성한다.

**정성적 효과**: 즉각적 최종성(Immediate Finality)으로 블록 확정 후 롤백이 불가능하여 금융 거래에 적합하다. 에너지 효율적 설계로 엔터프라이즈 환경에서 지속 가능하다. 알려진 참여자 집합으로 규제 요건(KYC, AML)을 충족하기 쉽다.

**미래 전망**: HotStuff(Linear BFT)는 PBFT의 O(n²) 메시지 복잡도를 O(n)으로 개선하여 더 많은 노드에서 BFT 합의를 가능하게 한다. Aptos, Sui 등 차세대 블록체인이 HotStuff 변형을 채택하여 높은 처리량과 BFT 보안을 동시에 달성하고 있다.

결론적으로 PBFT는 Byzantine fault를 견디는 합의 절차의 대표 모델이며, 허가형 블록체인과 엔터프라이즈 분산 시스템의 합의 메커니즘 설계에 필수적인 기반 알고리즘이다.

- **📢 섹션 요약 비유**: 거짓말하는 사람이 있어도, 규칙대로 정족수 도장이 모이면 결론이 나는 민주적 절차다. 소규모 신뢰 집단에서 최적의 성능을 발휘하며, 규모가 커지면 더 효율적인 방식(HotStuff 등)을 검토해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Byzantine Fault | PBFT가 해결하는 핵심 문제, 악의적 노드의 모순된 응답 |
| Pre-prepare | 1단계: 프라이머리의 제안 배포 |
| Prepare | 2단계: 레플리카의 제안 검증 및 동의 표명 |
| Commit | 3단계: 최종 확정 투표 |
| View Change | 프라이머리 장애 시 리더 교체 메커니즘 |
| Quorum (2f+1) | 합의 달성을 위한 최소 동의 노드 수 |
| HotStuff | PBFT의 O(n²)를 O(n)으로 개선한 차세대 BFT |
| Tendermint | PBFT 기반 Cosmos 생태계 합의 알고리즘 |
| Hyperledger Fabric | PBFT 계열 합의 사용 허가형 블록체인 |
| Raft | Crash Fault만 처리하는 비-BFT 합의 알고리즘 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">BFT 합의 알고리즘 발전 계보</div></div>
<div class="kb-diagram-note">Byzantine Generals Problem (1982, Lamport)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">PBFT - Practical BFT (1999, Castro &amp; Liskov)</div>
<div class="kb-diagram-note">O(n²) 메시지, 최초 실용적 BFT</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IBFT / Istanbul BFT (Ethereum 기반 허가형)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Tendermint (2014, Cosmos 생태계)</div>
<div class="kb-diagram-note">PBFT 기반, 라운드 기반 투표</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HotStuff (2018, VMware Research)</div>
<div class="kb-diagram-note">O(n) 선형 메시지 복잡도</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">LibraBFT / DiemBFT (Facebook/Meta, 2019)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AptosBFT / Jolteon (2022, Aptos)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: 차세대 BFT 합의 연구 (Bullshark, DAG-BFT 등)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 회의에서 중요한 결정을 내릴 때, 먼저 반장이 의견을 제안하고(Pre-prepare), 모두가 확인하고(Prepare), 마지막에 함께 도장을 찍어야(Commit) 결론이 나요.
2. 거짓말하는 친구가 몇 명 있어도, 규칙 정족수 이상의 친구들이 동의하면 결론이 확정돼요.
3. PBFT는 이런 방식으로 블록체인에서 모두가 같은 장부를 갖게 하는 합의 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 64 / 552

← **이전**: [63. 트랜잭션 풀 (Mempool / Memory Pool) - 블록에 포함되지 않은 대기 중인 트랜잭션 저장소](/knowledge-base/studynote/06_ict_convergence/01_blockchain/063_mempool_transaction_queue/)
**다음**: [65. 합의 완결성 (Finality) - 블록이 체인에 기록되어 뒤집히지 않음이 보장되는 상태 (PoW는 확률적 완결성, BFT는 즉각적](/knowledge-base/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/) →

---
