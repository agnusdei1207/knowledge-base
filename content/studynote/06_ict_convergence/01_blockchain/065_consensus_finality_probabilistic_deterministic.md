+++
title = "65. 합의 완결성 (Finality) - 블록이 체인에 기록되어 뒤집히지 않음이 보장되는 상태 (PoW는 확률적 완결성, BFT는 즉각적 완결성)"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Finality(합의 완결성)는 한 번 확정된 블록이나 트랜잭션이 체인 재구성(Reorg)으로 되돌릴 수 없다는 보장 정도를 의미하며, 확률적(Probabilistic) 완결성과 결정적(Deterministic) 완결성의 두 종류가 있다.
> 2. **가치**: PoW(작업증명)는 블록이 쌓일수록 재구성 가능성이 지수적으로 감소하는 확률적 완결성을, BFT 계열은 합의 완료 즉시 절대 되돌릴 수 없는 결정적 완결성을 제공하므로 사용 목적에 따라 선택이 달라진다.
> 3. **판단 포인트**: 결제·정산 시스템은 '완전 확정' 시점이 언제인지 정확히 정의해야 하며, PoW는 충분한 확인(Confirmation) 수를, BFT는 네트워크 규모와 허가 구조를 고려하여 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

블록체인에서 트랜잭션이 블록에 포함됐다는 것이 곧 '최종 확정'을 의미하지는 않는다. 특히 작업증명(PoW) 기반 네트워크에서는 블록 재구성(Chain Reorganization, Reorg)이 발생할 수 있어, 이미 블록에 들어간 트랜잭션이 나중에 취소될 수도 있다.

Finality(완결성)는 이런 불확실성을 다루는 개념이다. '이 거래가 언제 최종 확정되는가?'는 결제, 거래소, DeFi, 크로스체인 브리지 등 모든 블록체인 응용에서 핵심 질문이다. 확정되지 않은 거래를 완료로 처리하면 이중 지출(Double Spending) 공격에 노출될 수 있고, 과도하게 많은 확인을 기다리면 UX가 저하된다.

전통 금융의 결제 최종성(Settlement Finality) 개념과 비교하면, 신용카드 결제는 즉시처럼 보이지만 실제 정산은 T+2(거래 후 2영업일)에 이루어진다. 블록체인은 이 과정을 수분~수초로 단축하면서도 각 합의 메커니즘에 따라 완결성 보장 방식이 다르다.

규제 측면에서도 Finality는 중요하다. EU의 결제결산 완결성 지침(Settlement Finality Directive)은 지급결제 시스템에서 취소 불가능성을 법적으로 요구한다. 중앙은행 디지털 화폐(CBDC)나 토큰화된 증권 시스템은 법적 Finality를 기술적 Finality와 연계해야 한다.

- **📢 섹션 요약 비유**: 서류에 도장이 찍혔다고 다 끝난 게 아니라, 다시 못 고치게 확정됐는지가 더 중요하다. 공증(확률적 완결성)과 등기(결정적 완결성)의 차이처럼, 어느 수준의 확정성이 필요한지에 따라 선택이 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 완결성의 두 가지 유형

| 유형 | 의미 | 대표 합의 | 특징 |
| :--- | :--- | :--- | :--- |
| 확률적 완결성 (Probabilistic) | 블록이 쌓일수록 재구성 가능성이 지수적으로 감소 | PoW (Bitcoin) | 완전한 100% 보장은 없지만 현실적으로 안전 |
| 결정적 완결성 (Deterministic) | 합의 완료 즉시 절대 취소 불가 | BFT (PBFT, Tendermint) | 즉각적이고 절대적 보장 |
| 경제적 완결성 (Economic) | 공격 비용이 이익보다 훨씬 커서 사실상 안전 | PoS (Ethereum) | 슬래싱으로 경제적 처벌 |
| 주관적 완결성 (Subjective) | 각 노드가 독립적으로 완결 판단 | DAG | 글로벌 단일 완결 시점 없음 |

### 2. PoW 확률적 완결성 메커니즘

비트코인에서 블록이 체인에 추가된 후, 그 블록 위에 새로운 블록이 쌓일수록 재구성(Reorg) 가능성이 급격히 감소한다.

```
[비트코인 Reorg 확률 (공격자 해시 파워 비율 q)]

q = 10% (공격자 해시 파워 10%)
 - 1 확인 후 reorg 성공 확률: ~0.2%
 - 6 확인 후 reorg 성공 확률: ~0.001% 미만

q = 30% (공격자 해시 파워 30%)
 - 1 확인 후 reorg 성공 확률: ~17.7%
 - 6 확인 후 reorg 성공 확률: ~0.2%
 - 경제적 가치 고려 시 통상 6 확인 이상 권장

q = 50% 이상 → 51% 공격 가능, 이중 지출 위험
```

비트코인 네트워크의 관행:
- **소액 거래**: 1~3 확인 (10~30분)
- **일반 거래**: 6 확인 (~60분)
- **고액 거래**: 12 확인 이상 (2시간 이상)

### 3. BFT 결정적 완결성 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">PBFT/Tendermint 완결성</div></div>
<div class="kb-diagram-note">클라이언트 요청</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Pre-prepare → Prepare → Commit (3단계 합의)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2f+1 quorum 확보</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">즉각적 완결! (이후 절대 되돌릴 수 없음)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라이언트에 응답</div>
<div class="kb-diagram-note">특징:</div>
<div class="kb-diagram-tree-item" style="--depth:0">응답 받는 즉시 완결</div>
<div class="kb-diagram-tree-item" style="--depth:0">롤백 불가</div>
<div class="kb-diagram-tree-item" style="--depth:0">단, 네트워크 파티션 시 리브니스(Liveness) 중단 가능</div>
</div>
</div>



### 4. 이더리움 2.0 (Casper) 경제적 완결성

이더리움은 Proof-of-Stake(PoS)로 전환하면서 가스퍼(Gasper) 합의를 사용한다. 여기서는 '체크포인트 완결성'이 핵심이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이더리움 완결성 타임라인</div></div>
<div class="kb-diagram-note">슬롯(Slot): 12초마다 블록 제안</div>
<div class="kb-diagram-note">에폭(Epoch): 32 슬롯 = 약 6.4분</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">에폭 종료 시 체크포인트 투표 (2/3 이상 동의)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">두 에폭 연속 체크포인트 완결 → Finalized</div>
<div class="kb-diagram-note">총 소요 시간: 약 12.8분 (2 에폭)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Finalized 후 되돌리려면 전체 스테이킹의 1/3 이상 슬래싱 필요</div>
<div class="kb-diagram-note">→ 수십억 달러 규모의 경제적 처벌 → 사실상 불가능</div>
</div>
</div>



| 완결성 단계 | 상태 | 설명 |
| :--- | :--- | :--- |
| Proposed | 블록 제안됨 | 유효성 미확인 |
| Attested | 위원회 투표됨 | 검증자 일부 서명 |
| Justified | 체크포인트 정당화 | 2/3 이상 투표 |
| Finalized | 완결 | 두 연속 체크포인트 정당화 |

### 5. 완결성 관련 주요 개념

| 개념 | 의미 |
| :--- | :--- |
| Reorg (체인 재구성) | 더 긴 체인 발견 시 현재 체인 일부가 교체되는 현상 |
| Safety | 두 정직한 노드가 서로 다른 값을 확정하지 않는 성질 |
| Liveness | 네트워크가 항상 새로운 값을 확정할 수 있는 성질 |
| CAP 정리 | 분산 시스템에서 일관성(C), 가용성(A), 분산 내성(P) 중 2개만 보장 가능 |
| FLP 불가능성 | 비동기 네트워크에서 결함 허용 합의는 반드시 라이브니스를 포기해야 함 |

- **📢 섹션 요약 비유**: 모래성이 파도를 6번 더 맞고도 안 무너지면 안심할 수 있는 것(PoW 6 Confirmations)과, 벽돌로 만들어 처음부터 굳건한 것(BFT 즉각 완결성)의 차이다.

---

## Ⅲ. 비교 및 연결

### 1. 합의 방식별 완결성 특성 비교

| 합의 방식 | 완결성 유형 | 완결 시간 | 안전성 | 처리량 | 에너지 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Bitcoin PoW | 확률적 | 60분 (6 확인) | 매우 높음 | 낮음 (~7 TPS) | 매우 높음 |
| Ethereum PoS | 경제적 | ~12.8분 (2 에폭) | 매우 높음 | 중간 (~30 TPS) | 낮음 |
| PBFT | 결정적 | 수초 | 허가형에서 높음 | 높음 (수천 TPS) | 매우 낮음 |
| Tendermint | 결정적 | 1~6초 | 높음 | 높음 (~1,000 TPS) | 낮음 |
| HotStuff | 결정적 | 수초 | 높음 | 매우 높음 | 낮음 |

### 2. 완결성과 CAP 정리의 관계

분산 시스템 이론에서 CAP 정리(Consistency, Availability, Partition Tolerance 중 2개만 선택 가능)는 완결성 설계에 직접 영향을 미친다.

- **PoW**: 파티션 발생 시 양쪽 체인이 계속 성장하다가 나중에 가장 긴 체인으로 합병. 가용성(A) 우선, 일시적 불일치 허용.
- **PBFT**: 파티션 발생 시 quorum을 형성할 수 없으면 시스템 중단. 일관성(C) 우선, 가용성 희생.

이것이 FLP 불가능성 정리가 의미하는 바다: 비동기 네트워크에서 결함 허용(Fault Tolerance)과 즉각적 완결성(Liveness)을 동시에 보장하는 알고리즘은 존재하지 않는다.

### 3. 완결성과 이중 지출 공격의 관계

확률적 완결성에서 이중 지출 공격이 가능하려면:
1. 공격자가 몰래 더 긴 체인을 생성한다 (다수 해시 파워 필요)
2. 피해자가 거래 확인 후 상품 제공
3. 공격자가 더 긴 체인을 공개하여 기존 거래 무효화

이를 '레이스 어택(Race Attack)'이라고도 한다. 충분한 확인 수를 기다리면 이 공격의 성공 확률이 지수적으로 감소한다.

- **📢 섹션 요약 비유**: 점점 굳는 풀(PoW)과 한 번에 딱 굳는 접착제(BFT)의 차이다. 용도에 따라 어느 것이 더 적합한지 다르다 — 정밀 작업에는 순간접착제, 큰 부재 조립에는 천천히 굳는 강력 접착제가 낫다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **완결성 유형 선택**: 서비스 특성에 맞는 완결성 유형을 선택했는가? 금융 정산은 결정적 완결성이 필요하고, 대규모 공개형 네트워크는 확률적 완결성이 더 적합할 수 있다.
2. **확인 수 기준 정의**: PoW 기반 시스템에서 서비스가 허용하는 확인 수(Confirmation)를 명확히 정의했는가? 거래 금액별로 다른 기준을 적용하는가?
3. **Reorg 처리**: 블록 재구성(Reorg) 발생 시 시스템이 어떻게 처리하는가? 이미 처리한 거래가 무효화될 때의 롤백 로직이 있는가?
4. **완결성과 UX 균형**: 높은 확인 수는 보안을 높이지만 UX를 저해한다. 서비스 특성에 맞는 균형점을 찾았는가?
5. **크로스체인 완결성**: 크로스체인 브리지(Bridge)나 스왑에서 양쪽 체인의 완결성 시점이 다를 때 어떻게 처리하는가?
6. **법적 완결성 요건**: 규제 대상 서비스에서 법적 완결성(Legal Finality) 요건을 충족하는가? EU SFID 등 결제 규제 준수 여부를 확인했는가?

### 안티패턴

- **전파와 완결의 혼동**: 트랜잭션이 멤풀에 들어가거나 1 확인을 받은 것을 '완료'로 처리하는 시스템. 비트코인 거래소가 1 확인 후 코인을 출금 가능하게 하면 이중 지출 공격에 취약해진다.

- **PoW의 완결성을 즉시 확정으로 오해**: 비트코인에서 1 확인은 약 10분이고 6 확인은 약 60분이다. 실시간 결제에서 "1 확인이면 충분하다"는 판단은 위험할 수 있다.

- **BFT를 무한정 확장 가능한 것으로 보는 설계**: PBFT의 O(n²) 메시지 복잡도로 인해 노드 수가 증가하면 성능이 급격히 저하된다. 수백만 사용자의 공개형 네트워크에 BFT 완결성을 적용하는 것은 현실적으로 어렵다.

- **파티션 내성과 완결성 동시 요구**: CAP 정리에 따라 네트워크 파티션이 발생하는 환경에서 동시에 완결성(Safety)과 가용성(Liveness)을 보장하는 것은 이론적으로 불가능하다. 이를 모르고 설계하면 시스템이 무한 대기 상태에 빠질 수 있다.

- **사용자에게 완결성 모호하게 안내**: "거래가 처리 중입니다"와 "거래가 완료됐습니다"를 명확히 구분하지 않으면 사용자 혼란과 분쟁이 발생한다. 결제 UX에서 완결 상태를 명확히 표시해야 한다.

기술사 관점에서는 Finality를 합의 메커니즘의 마지막 품질 특성으로 봐야 한다. 확정성의 강도, 완결 시간, 공격 저항성은 서비스 설계에 직접 영향을 주며, 특히 금융 서비스에서는 법적·경제적 완결성 요건과 연계해야 한다.

- **📢 섹션 요약 비유**: 도장이 여러 개일수록 더 확실하지만, 한 번 찍히면 다시 지우기 어렵다. 어디에 쓸 서류인가에 따라 몇 개의 도장이 필요한지 달라진다.

---

## Ⅴ. 기대효과 및 결론

Finality를 올바르게 이해하고 설계에 반영하면:

**보안 측면**: 이중 지출, 체인 재구성 공격에 대한 방어력이 명확해진다. 서비스별 위험 수용 기준(Risk Tolerance)을 정량적으로 설정할 수 있다.

**UX 측면**: 사용자에게 "언제 거래가 최종 확정됐는지"를 명확하게 안내할 수 있다. 과도한 대기 없이 적절한 보안 수준의 서비스가 가능하다.

**규제 준수 측면**: EU 결제결산 완결성 지침, 금융감독원 전자금융 규정 등 법적 완결성 요건을 기술적으로 충족할 수 있다.

**시스템 아키텍처 측면**: 합의 메커니즘 선택(PoW vs BFT vs PoS)이 단순히 성능의 문제가 아니라 완결성 보장 방식의 근본적인 선택임을 이해하면, 서비스 목적에 맞는 올바른 기술 선택이 가능하다.

결론적으로 Finality는 합의된 결과가 뒤집히지 않는 정도를 의미하며, 블록체인 시스템의 가장 중요한 신뢰 속성이다. '전파됐다'와 '확정됐다'의 차이를 정확히 이해하고 설계에 반영하는 것이 건전한 블록체인 기반 서비스의 핵심이다.

- **📢 섹션 요약 비유**: 확정 도장이 찍혀야 진짜 끝난 것이다. 확인서가 1장인지 6장인지, 아니면 바로 공증이 되는지에 따라 '얼마나 믿을 수 있느냐'가 달라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 확률적 완결성 | PoW에서 블록 확인 수에 따른 안전성 증가 |
| 결정적 완결성 | BFT 계열에서 합의 완료 즉시 취소 불가 |
| 체인 재구성 (Reorg) | 완결성이 보장되지 않을 때 발생하는 위험 |
| 이중 지출 (Double Spend) | 완결성 미확보 시 발생 가능한 공격 |
| Safety vs Liveness | 완결성 보장의 두 가지 속성, CAP 정리와 연결 |
| Confirmation 수 | PoW에서 완결성 수준을 나타내는 지표 |
| Slashing | PoS에서 잘못된 검증자에 대한 경제적 처벌 |
| 체크포인트 (Checkpoint) | Ethereum PoS의 완결성 확정 단위 |
| CAP 정리 | 분산 시스템 완결성 설계의 이론적 제약 |
| 결제결산 완결성 | 법적 완결성 요건 (EU SFID 등) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">블록체인 완결성 개념의 발전</div></div>
<div class="kb-diagram-note">비트코인 PoW: 확률적 완결성 (2009)</div>
<div class="kb-diagram-note">↓ 문제: 완결까지 1시간 필요</div>
<div class="kb-diagram-note">PBFT 기반 허가형 체인: 즉각 완결성 (2015~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이더리움 PoW → PoS 전환 (Merge, 2022)</div>
<div class="kb-diagram-note">확률적 → 경제적 완결성 (~12.8분)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">차세대 합의: HotStuff, Tendermint</div>
<div class="kb-diagram-note">결정적 완결 + 높은 처리량</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: SSF (Single Slot Finality) 연구 중</div>
<div class="kb-diagram-note">이더리움에서 12초 이내 완결성 목표</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">미래: L2 기반 즉각 완결성 + L1 경제적 보안</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 블록에 들어갔다고 아직 완전히 끝난 건 아니에요 — 마치 서류에 도장을 찍었어도 다시 취소될 수도 있는 것처럼요.
2. 도장이 여러 개 더 찍히면(확인 수가 늘어나면) 취소되기 점점 어려워져요.
3. BFT 합의에서는 처음 도장이 찍히는 순간부터 절대 취소할 수 없어요 — 완전 즉각 확정이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 65 / 552

← **이전**: [64. BFT 합의의 3단계 - Pre-prepare, Prepare, Commit](/knowledge-base/studynote/06_ict_convergence/01_blockchain/064_bft_pbft_consensus_3_phases/)
**다음**: [66. 지향성 비순환 그래프 (DAG, Directed Acyclic Graph) - 블록체인 대신 트랜잭션들이 거미줄처럼 서로를 증명하는](/knowledge-base/studynote/06_ict_convergence/01_blockchain/066_dag_directed_acyclic_graph_tangle/) →

---
