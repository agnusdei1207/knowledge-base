+++
title = "63. 트랜잭션 풀 (Mempool / Memory Pool) - 블록에 포함되지 않은 대기 중인 트랜잭션 저장소"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멤풀(Mempool, Memory Pool)은 블록체인에 아직 포함되지 않은 트랜잭션이 네트워크 노드에 임시로 대기하는 공간으로, 각 노드가 독립적으로 관리하는 로컬 저장소다.
> 2. **가치**: 멤풀은 수수료 경매 시장(Fee Auction Market)의 역할을 하여 채굴자·검증자의 트랜잭션 선택과 블록 구성 우선순위를 결정하며, 네트워크 혼잡도를 실시간으로 반영한다.
> 3. **판단 포인트**: 미확정 트랜잭션은 최종 합의 상태가 아니므로, 지갑·거래소·디앱 설계 시 멤풀 대기 상태와 블록 확정 상태를 반드시 구분해야 하며, RBF(Replace-By-Fee)와 CPFP(Child-Pays-For-Parent) 전략을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

블록체인은 거래를 즉시 확정하지 않는다. 사용자가 트랜잭션을 전송하면, 그 트랜잭션은 먼저 P2P 네트워크를 통해 전파되고, 각 노드의 멤풀에 저장된 뒤, 채굴자나 검증자에 의해 선택될 때 비로소 블록에 포함된다. 그리고 그 블록이 충분히 많은 다른 블록에 의해 이어져야 '확정(Confirmed)'된다.

이 과정에서 멤풀은 핵심적인 중간 단계다. 멤풀을 이해하지 못하면, 왜 수수료가 오르면 거래가 빨라지는지, 왜 네트워크가 막히면 확인이 수 시간 혹은 수 일이 걸리는지, 왜 '보냈는데 아직 안 들어간다'는 상황이 발생하는지 설명할 수 없다.

멤풀은 노드마다 독립적으로 관리된다. 즉, 비트코인 네트워크에 전 세계적으로 수천 개의 멤풀이 존재하며, 각각의 멤풀은 서로 완전히 동일하지 않다. 이는 분산 시스템의 특성으로, 어떤 노드는 아직 트랜잭션을 받지 못했을 수도 있고, 어떤 노드는 이미 삭제했을 수도 있다.

멤풀의 크기는 네트워크 혼잡도의 직접적인 지표다. 2017년 비트코인 블록 크기 논쟁(SegWit 논쟁) 당시 멤풀에는 수십만 개의 트랜잭션이 쌓였고, 평균 수수료가 50 달러 이상으로 치솟았다. 이더리움 DeFi 여름(2020년)과 NFT 붐(2021년) 때도 이더리움 멤풀이 폭발적으로 증가했다. 이런 역사가 멤풀 관리와 수수료 최적화의 중요성을 보여준다.

- **📢 섹션 요약 비유**: 식당 번호표를 뽑고 기다리는 대기실과 같다. 식당(블록)이 아무리 빨리 돌아가도, 손님(트랜잭션)이 너무 많이 몰리면 기다림은 길어진다. 그리고 팁(수수료)을 많이 내는 손님은 먼저 불린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 트랜잭션 생명주기 (Transaction Lifecycle)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">트랜잭션 생명주기</div></div>
<div class="kb-diagram-note">사용자 지갑 (Wallet)</div>
<div class="kb-diagram-note">트랜잭션 서명 및 생성</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">P2P 네트워크 전파 (Broadcast)</div>
<div class="kb-diagram-note">gossip 프로토콜로 전파</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">대기 단계, 미확정</div></div>
<div class="kb-diagram-note">유효성 검사 통과 시 저장</div>
<div class="kb-diagram-note">- 서명 유효성</div>
<div class="kb-diagram-note">- 이중 지출 (Double Spend) 없음</div>
<div class="kb-diagram-note">- nonce/UTXO 조건 충족</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">채굴자/검증자 선택 (Selection)</div>
<div class="kb-diagram-note">수수료 우선순위 기반</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">블록에 포함 (Block Inclusion)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">1 확인</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">최종 확정</div></div>
</div>
</div>



### 2. 수수료 시장 메커니즘

멤풀은 단순한 큐(Queue)가 아니라 수수료 기반 경매 시장이다. 채굴자는 수익 극대화를 위해 가장 높은 수수료를 제공하는 트랜잭션을 우선 선택한다.

**비트코인**: 수수료율(Fee Rate) = 수수료 / 트랜잭션 크기(바이트, satoshi/vByte 단위)
**이더리움**: EIP-1559 이후 기본 수수료(Base Fee) + 우선 수수료(Priority Fee, Tip) 구조

| 수수료 수준 | 대기 예상 시간 | 상황 |
| :--- | :--- | :--- |
| 매우 높음 (상위 10%) | 다음 블록 (10분 이내) | 긴급 거래, 높은 가스비 |
| 높음 (상위 30%) | 1~3 블록 (30분 이내) | 일반 거래 |
| 보통 (중간) | 1~6 블록 (1시간 이내) | 여유 있는 거래 |
| 낮음 (하위 50%) | 수 시간 ~ 수 일 | 비용 절감 우선 |
| 매우 낮음 | 무기한 대기 또는 삭제 | 거래 실패 위험 |

### 3. 핵심 구성 요소 및 설계

| 구성 요소 | 역할 | 세부 사항 |
| :--- | :--- | :--- |
| 트랜잭션 검증기 | 유효성 확인 | 서명, UTXO/nonce, 이중지출 방지 |
| 멤풀 저장소 | 미확정 거래 보관 | 메모리(RAM)에 저장, 용량 제한 있음 |
| 우선순위 정렬기 | 수수료 기반 정렬 | 채굴자 수익 최적화 |
| 추방(Eviction) 정책 | 오래된 거래 삭제 | 14일 후 자동 삭제 (Bitcoin Core) |
| 전파 엔진 | P2P 전달 | gossip 프로토콜 |

### 4. RBF (Replace-By-Fee) 전략

사용자가 너무 낮은 수수료로 트랜잭션을 보냈을 때, 이를 더 높은 수수료의 트랜잭션으로 대체하는 방법이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기존 트랜잭션 (수수료 10 sat/vByte, 멤풀 대기 중)</div>
<div class="kb-diagram-note">↓ RBF 적용</div>
<div class="kb-diagram-note">대체 트랜잭션 (수수료 30 sat/vByte, 동일 입력)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">기존 트랜잭션 멤풀에서 퇴출</div>
<div class="kb-diagram-note">대체 트랜잭션이 더 빠르게 블록 포함</div>
</div>
</div>



**조건**: RBF는 트랜잭션 생성 시 옵트인(Opt-in) 플래그를 설정해야 한다 (Bitcoin BIP 125). 이미 블록에 포함된 트랜잭션에는 적용 불가.

### 5. CPFP (Child-Pays-For-Parent) 전략

부모 트랜잭션의 수수료가 너무 낮아 대기 중일 때, 그 출력(Output)을 사용하는 자식 트랜잭션을 높은 수수료로 생성하여, 채굴자가 묶음으로 처리하도록 유도하는 방법이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">부모 트랜잭션 (수수료 5 sat/vByte, 멤풀 대기 중)</div>
<div class="kb-diagram-note">출력 UTXO 사용</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">자식 트랜잭션 (수수료 100 sat/vByte)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">채굴자: 부모+자식 묶음의 평균 수수료가 높으면 함께 선택</div>
</div>
</div>



### 6. 이더리움 EIP-1559 와 멤풀

이더리움은 2021년 EIP-1559를 통해 수수료 구조를 변경했다.

| 이전 (Legacy) | 이후 (EIP-1559) |
| :--- | :--- |
| 가스 가격(Gas Price) 단일 입찰 | 기본 수수료(Base Fee) + 우선 수수료(Tip) |
| 수수료 전액 채굴자에게 | 기본 수수료는 소각(Burn), 팁만 채굴자에게 |
| 수수료 예측 어려움 | 기본 수수료 알고리즘으로 예측 가능 |
| 입찰 경쟁 복잡 | 우선 수수료로 더 간단한 경쟁 |

EIP-1559 이후에도 네트워크 혼잡 시 기본 수수료가 급등하여 멤풀 대기 문제는 여전히 존재한다.

- **📢 섹션 요약 비유**: 줄서기 대기표에 팁을 많이 내는 손님이 먼저 들어가는 구조다. 그리고 팁을 낮게 냈다면 나중에 더 높은 팁으로 교체 신청(RBF)을 할 수 있고, 아니면 먼저 들어간 친구(부모)를 데리고 나오려고 자신이 대신 큰돈을 내기도 한다(CPFP).

---

## Ⅲ. 비교 및 연결

### 1. 멤풀 vs 관련 개념 비교

| 구분 | 멤풀(Mempool) | 블록체인(Blockchain) | 지갑 큐(Wallet Queue) |
| :--- | :--- | :--- | :--- |
| 상태 | 미확정 (Unconfirmed) | 확정 (Confirmed) | 생성 대기 (Pending) |
| 저장 위치 | 각 노드의 RAM | 전 노드의 디스크 | 사용자 단말 |
| 지속성 | 짧음 (14일 후 삭제) | 영구 (불변) | 사용자 제어 |
| 의미 | 수수료 경쟁 대기 | 영구 기록 | 서명 전 임시 |
| 확정성 | 없음 | 있음 (확률적/결정적) | 없음 |

### 2. 비트코인 vs 이더리움 멤풀 비교

| 항목 | 비트코인 | 이더리움 |
| :--- | :--- | :--- |
| 수수료 단위 | sat/vByte | Gwei (Gas Price) |
| 대체 메커니즘 | RBF (Opt-in) | 같은 nonce 높은 가스비 |
| 순서 결정 | 수수료율 | 가스 가격 + nonce |
| 멤풀 크기 제한 | ~300MB (Bitcoin Core 기본) | 노드 설정에 따라 다름 |
| 예측 도구 | mempool.space 등 | etherscan.io Gas Tracker |

### 3. MEV (최대 추출 가치, Maximal Extractable Value)

이더리움에서는 채굴자/검증자가 멤풀에서 트랜잭션 순서를 조작하여 추가 수익을 얻을 수 있다.

- **프론트러닝(Front-running)**: 수익성 높은 트랜잭션 앞에 자신의 트랜잭션을 삽입
- **샌드위치 공격(Sandwich Attack)**: 대형 DEX 거래 앞뒤에 자신의 거래를 끼워 넣어 가격 차이로 수익 획득
- **백러닝(Back-running)**: 수익성 높은 거래 직후에 트랜잭션 삽입

MEV는 멤풀의 투명성(공개된 거래 내용)이 악용될 수 있다는 점을 보여준다. Flashbots는 MEV를 보다 투명하게 관리하기 위한 인프라를 제공한다.

- **📢 섹션 요약 비유**: 대기실에서 이름이 불려도 진료가 끝난 것은 아니다. 멤풀에 들어간 트랜잭션도 블록에 포함되기 전까지는 '대기 중'일 뿐이다. 그리고 대기실 관리자(채굴자)가 특정 사람을 먼저 불러들일 수도 있다(MEV).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **수수료 추정 로직**: 실시간 멤풀 상태를 기반으로 적절한 수수료를 자동 추정하는 로직이 있는가? mempool.space API, EthGasStation 등 외부 데이터를 활용하는가?
2. **nonce 관리**: 이더리움의 경우 nonce 충돌, 누락, 갭(Gap) 발생 시 처리 로직이 있는가? nonce 재사용 방지 대책이 있는가?
3. **거래 재전송 전략**: 수수료 부족으로 오랫동안 대기 중인 거래에 대해 RBF 또는 CPFP 전략을 사용할 수 있는가?
4. **미확정 거래 취급**: 1 Confirmation도 없는 거래를 완료로 표시하지 않는가? 거래소나 결제 시스템은 충분한 확인 수(Bitcoin 6회 이상)를 기다리는가?
5. **멤풀 혼잡 대응**: 네트워크 혼잡 시 사용자에게 예상 대기 시간을 안내하는가? 긴급 거래와 비긴급 거래를 구분하는 전략이 있는가?
6. **MEV 방지**: DeFi 프로토콜의 경우 프론트러닝, 샌드위치 공격 방어 전략(Private Mempool, Commit-Reveal 등)이 있는가?
7. **오프라인/저수수료 처리**: 라이트닝 네트워크(Lightning Network)나 Layer-2로 소액 결제를 오프로드하여 멤풀 혼잡을 줄이는 전략이 있는가?

### 안티패턴

- **낮은 수수료 고집으로 인한 거래 실패**: 비용 절감을 위해 매우 낮은 수수료를 설정하면 거래가 수 일간 대기하거나 멤풀에서 삭제될 수 있다. 결제 기한이 있는 서비스에서는 치명적이다.

- **nonce 관리 없이 다중 트랜잭션 발송**: 이더리움에서 nonce 순서를 무시하고 여러 트랜잭션을 동시에 보내면 nonce 갭이 발생하여 후속 트랜잭션이 모두 대기 상태에 빠진다. 하나의 nonce가 막히면 이후 모든 거래가 막힌다.

- **멤풀 대기와 블록 확정을 동일시**: '트랜잭션 전송 완료'를 '결제 완료'로 처리하면 이중 지출 공격에 취약해진다. 특히 RBF가 활성화된 경우 멤풀의 트랜잭션은 언제든 대체될 수 있다.

- **고정 수수료 설정**: 수수료를 코드에 하드코딩하면 네트워크 혼잡 시 거래가 지연되거나, 반대로 네트워크가 한산할 때 과도한 수수료를 지불하게 된다. 항상 실시간 수수료 추정을 사용해야 한다.

- **멤풀 상태 모니터링 부재**: 거래소나 결제 서비스가 멤풀 상태를 모니터링하지 않으면, 이상한 수수료 급등이나 네트워크 공격 상황을 탐지하지 못한다.

기술사 관점에서는 멤풀을 단순 대기열이 아닌, 수수료 시장과 확정 지연의 연결고리로 봐야 한다. 이 관점이 있어야 블록체인 기반 결제 UX와 트랜잭션 관리 전략을 제대로 설계할 수 있다.

- **📢 섹션 요약 비유**: 입장권을 먼저 사면 빨리 들어가고, 늦게 사면 오래 기다리는 놀이공원 줄과 같다. 줄을 서 있는 동안에는 '입장한 것'이 아니므로, 입장을 확인하기 전에 자리를 깔아두면 안 된다.

---

## Ⅴ. 기대효과 및 결론

멤풀을 이해하면 블록체인 기반 시스템에서 발생하는 다양한 운영 이슈를 해결할 수 있다. 거래 지연, 수수료 급등, 재전송 실패, 이중 지출 위협 등은 모두 멤풀의 동작 원리를 이해해야 정확히 진단하고 대응할 수 있다.

거래소와 결제 서비스 관점에서는 멤풀 모니터링을 통해 적절한 수수료 추정, 거래 재전송 전략, 확인 수 기준 설정이 가능하다. 지갑 개발자 관점에서는 RBF와 CPFP 지원, nonce 관리, 실시간 수수료 추천이 필수다. DeFi 개발자 관점에서는 MEV 방어 전략이 핵심 보안 요소다.

결론적으로 멤풀은 블록체인 거래의 대기실이자 수수료 경쟁의 전장이며, 사용자 경험(UX)과 시스템 보안의 핵심 연결고리다. "보냈다"와 "확정됐다"의 차이를 정확히 이해하고 설계에 반영하는 것이 건전한 블록체인 시스템의 기본이다.

- **📢 섹션 요약 비유**: 줄을 서서 기다리는 동안에도 순서와 비용이 정해지고, 새치기를 막는 규칙도 필요하다. 멤풀은 이 모든 것을 조율하는 대기실 관리 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 트랜잭션(Transaction) | 멤풀의 기본 저장 단위 |
| P2P 네트워크 | 트랜잭션 전파 경로 |
| 수수료 시장(Fee Market) | 멤풀에서의 트랜잭션 우선순위 결정 |
| RBF (Replace-By-Fee) | 수수료 부족 트랜잭션 교체 전략 |
| CPFP (Child-Pays-For-Parent) | 부모 트랜잭션 가속화 전략 |
| MEV (최대 추출 가치) | 멤풀 투명성을 이용한 채굴자 수익 최적화 |
| nonce | 이더리움 트랜잭션 순서 관리 변수 |
| 이중 지출(Double Spend) | 멤풀 단계에서 방지해야 할 공격 |
| EIP-1559 | 이더리움 수수료 구조 개선안 |
| 라이트닝 네트워크 | 멤풀 혼잡을 줄이는 Layer-2 해결책 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">트랜잭션 처리 흐름과 멤풀 관련 기술 발전</div></div>
<div class="kb-diagram-note">초기 비트코인: 단순 수수료 입찰 방식</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">멤풀 혼잡 문제 (2017 블록 크기 논쟁)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">RBF (Replace-By-Fee) 도입 (BIP 125)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SegWit (Segregated Witness): 거래 크기 축소</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이더리움 EIP-1559: 기본수수료 + 팁 분리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">MEV 문제 부상 → Flashbots, MEV-Boost</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Private Mempool (프론트러닝 방지)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Layer-2 (Lightning, Rollup): 온체인 멤풀 부담 감소</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 블록체인에 돈을 보내면 바로 전달되는 게 아니라, 먼저 대기실(멤풀)에서 기다려야 해요.
2. 대기실에서 기다리는 동안 돈을 더 많이 주면(수수료 높이기) 더 빨리 처리돼요.
3. 대기실에 있는 동안은 아직 '전달된 것'이 아니에요 — 블록에 들어간 후에야 진짜 전달이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 63 / 552

← **이전**: [62. 비트코인 반감기 (Halving) - 약 4년마다 채굴 보상이 절반으로 줄어드는 메커니즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/062_bitcoin_halving_supply_shock/)
**다음**: [64. BFT 합의의 3단계 - Pre-prepare, Prepare, Commit](/knowledge-base/studynote/06_ict_convergence/01_blockchain/064_bft_pbft_consensus_3_phases/) →

---
