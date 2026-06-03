+++
title = "67. 51% 공격 (51% Attack) - 악의적 노드가 전체 해시 파워의 51% 이상을 장악해 장부를 조작하는 공격"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 51% 공격은 악의적인 행위자가 PoW 네트워크에서 전체 해시 파워의 과반(>50%), PoS 네트워크에서 스테이킹된 자산의 과반을 장악하여 블록 생성 순서를 제어하고 이중 지출(Double Spending)이나 체인 재구성(Reorg)을 실행하는 합의 조작 공격이다.
> 2. **가치**: 블록체인의 보안 가정("정직한 참여자가 과반을 유지한다")이 무너지면 어떤 결과가 발생하는지 보여주는 핵심 위협 시나리오로, 소규모·신생 블록체인 네트워크에서 실제 발생한 사례가 있다.
> 3. **판단 포인트**: 공격 가능성은 네트워크 해시레이트·스테이킹 총량 대비 공격자 자원 비율과 공격 비용(임대 비용, 기회비용) 대비 기대 이익으로 평가해야 하며, 방어는 확인 수 증가, 분산된 채굴 풀, PoS 슬래싱 등 다층적 방어가 필요하다.

---

## Ⅰ. 개요 및 필요성

블록체인은 본질적으로 다수결에 의한 합의 시스템이다. 비트코인에서는 "가장 긴 체인이 정당한 체인"이라는 원칙이 있는데, 이는 결국 "가장 많은 연산 자원을 투입한 체인이 정당하다"는 의미다. 따라서 전체 해시 파워의 과반을 장악하면 자신이 원하는 체인을 가장 빠르게 성장시킬 수 있다.

51% 공격은 이 합의 구조의 약점을 직접 파고드는 공격이다. 2018년부터 2020년대 초반에 걸쳐 Ethereum Classic(ETC), Bitcoin Gold(BTG), Vertcoin(VTC) 등 소규모 PoW 체인에서 실제로 51% 공격이 발생하여 수백만 달러의 피해가 발생했다. ETC는 2020년에만 3번의 51% 공격을 받았다.

이 공격이 중요한 이유는 단순한 해킹과 달리 코드 취약점을 이용하는 것이 아니라, 블록체인의 근본 합의 메커니즘 자체를 표적으로 하기 때문이다. 소프트웨어 패치로 간단히 해결되지 않으며, 네트워크의 분산도와 채굴 생태계의 건전성이 방어의 핵심이다.

비트코인처럼 해시레이트가 매우 높고 채굴 풀이 분산된 경우 51% 공격 비용은 수십억 달러에 달해 현실적으로 불가능하다. 그러나 소규모 PoW 체인은 NiceHash 같은 해시 파워 임대 서비스를 활용하면 수십만 달러로 공격이 가능해진다.

- **📢 섹션 요약 비유**: 반장 투표에서 한쪽이 절반 이상을 차지하면 결과가 바뀌는 것과 같다. 단, 이 투표에서 표를 많이 사들이려면 엄청난 돈이 필요하고, 큰 학교일수록 표 매수 비용이 기하급수적으로 올라간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 51% 공격의 단계별 실행 과정



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">51% 공격 (이중 지출) 단계</div></div>
<div class="kb-diagram-note">공격자가 전체 해시 파워 &gt; 50% 확보</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">정상 체인</div><div class="kb-diagram-note">(피해자가 보는 체인)</div></div>
<div class="kb-diagram-note">블록 A → 블록 B → 블록 C → 블록 D</div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">공격자의 거래(Tx) 포함 (코인 지불)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비밀 체인</div><div class="kb-diagram-note">(공격자가 몰래 구성 중)</div></div>
<div class="kb-diagram-note">블록 A → 블록 B → 블록 C' → 블록 D' → 블록 E'</div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">공격자의 거래 없음 (이중 지출 준비)</div>
<div class="kb-diagram-note">공격자의 해시 파워 &gt; 50% → 비밀 체인이 더 빠르게 성장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">피해자에게 거래 확인 후 상품·서비스 수령</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">공격자가 더 긴 비밀 체인 공개</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">네트워크가 더 긴 체인으로 전환 (Reorg)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">피해자의 체인에서 공격자 거래 무효화 (이중 지출 성공)</div>
<div class="kb-diagram-note">공격자: 코인 되돌려받음 + 상품·서비스 유지</div>
</div>
</div>



### 2. 51% 공격의 세 가지 주요 결과

| 공격 결과 | 설명 | 실제 영향 |
| :--- | :--- | :--- |
| 이중 지출 (Double Spending) | 같은 코인을 두 번 사용 | 거래소 피해, 신뢰 훼손 |
| 체인 재구성 (Reorg) | 확정된 블록들을 되돌림 | 기록 조작, 거래 무효화 |
| 거래 검열 (Censorship) | 특정 주소의 거래를 블록에서 배제 | 특정 사용자 서비스 차단 |
| 셀피시 채굴 (Selfish Mining) | 블록을 숨겨 다른 채굴자 낭비 유도 | 해시레이트 집중화 |

### 3. PoW vs PoS에서의 51% 공격 비교

| 항목 | PoW 51% 공격 | PoS 66% 공격 (Long Range) |
| :--- | :--- | :--- |
| 공격 조건 | 해시 파워 > 50% | 스테이킹 지분 > 2/3 |
| 왜 더 많이 필요한가 | 과반이면 더 긴 체인 생성 가능 | BFT 합의는 2/3 초과 필요 |
| 공격 자원 | ASIC, 임대 해시 파워 | 코인 매수 (가격 상승 촉발) |
| 경제적 억제력 | 공격 시 코인 가치 하락으로 손해 | 슬래싱으로 스테이킹 자산 소각 |
| 방어 수단 | 높은 해시레이트, 분산화 | 슬래싱, 체크포인트 |

### 4. 공격 비용 계산 (PoW)

```
51% 공격 비용 = 해시 파워 임대 비용 × 공격 시간

예시: Bitcoin Gold (BTG, 2018 공격)
 - BTG 네트워크 해시레이트: 약 1.3 Mhash/s
 - NiceHash에서 동등 해시파워 임대 비용: 시간당 ~$500
 - 이중 지출 성공을 위한 최소 시간: 2-3시간
 - 총 공격 비용 추정: $1,000~$1,500
 - 실제 도난 금액: 약 $18만 달러

예시: Bitcoin (BTC)
 - BTC 네트워크 해시레이트: 약 600 EH/s (2024년)
 - 해시파워 임대 비용: 시간당 수억 달러 수준
 - 1시간 공격 비용 >> 이중 지출 기대 이익
 - 현실적으로 불가능
```

### 5. 해시레이트 분포와 보안



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">채굴 풀 집중도와 51% 공격 위험</div></div>
<div class="kb-diagram-note">건강한 분포 (비트코인 기준):</div>
<div class="kb-diagram-note">Foundry USA: ~25%</div>
<div class="kb-diagram-note">AntPool: ~20%</div>
<div class="kb-diagram-note">ViaBTC: ~15%</div>
<div class="kb-diagram-note">F2Pool: ~12%</div>
<div class="kb-diagram-note">기타: ~28%</div>
<div class="kb-diagram-note">→ 상위 2개 풀 합산 45%, 단독으로는 51% 불가</div>
<div class="kb-diagram-note">위험한 집중도:</div>
<div class="kb-diagram-note">Pool-A: &gt;51% → 단독 51% 공격 가능</div>
<div class="kb-diagram-note">(여러 채굴 풀이 협력해도 51% 이상)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 기록부를 많이 가진 쪽이 더 유리해지는 상황이다. 하지만 기록부를 더 많이 확보하려면 엄청난 비용이 필요하고, 네트워크가 클수록 그 비용이 기하급수적으로 늘어난다.

---

## Ⅲ. 비교 및 연결

### 1. 합의 방식별 51% 공격 취약성 비교

| 합의 방식 | 공격 임계값 | 공격 비용 요소 | 사실상 방어선 |
| :--- | :--- | :--- | :--- |
| PoW (비트코인) | 해시 파워 > 50% | ASIC 구매/임대, 전기비 | 막대한 물리적 자원 |
| PoS (이더리움) | 지분 > 33% (일부 공격), > 66% (치명적) | 코인 매수 (가격 상승) | 슬래싱 + 경제적 처벌 |
| BFT (허가형) | Byzantine 노드 > f (n≥3f+1) | 참여자 신원 위조 | KYC/신원 인증 |
| DPoS | 슈퍼 대표 > 15/21명 | 투표권 장악 | 커뮤니티 거버넌스 |

### 2. 실제 51% 공격 사례

| 피해 체인 | 시기 | 피해 금액 | 방법 |
| :--- | :--- | :--- | :--- |
| Bitcoin Gold (BTG) | 2018년 5월 | ~$18만 | NiceHash 임대 |
| Vertcoin (VTC) | 2018년 12월 | ~$10만 | 해시 파워 임대 |
| Ethereum Classic (ETC) | 2019년 1월 | ~$110만 | 이중 지출 |
| Ethereum Classic (ETC) | 2020년 8월 (3회) | 수백만 달러 | 반복 공격 |

### 3. 방어 전략 비교

| 방어 방법 | 효과 | 한계 |
| :--- | :--- | :--- |
| 확인 수 증가 | 이중 지출 난이도 증가 | UX 저하 (대기 시간 증가) |
| 채굴 풀 분산화 | 단독 공격 불가능 | 강제 불가, 인센티브 설계 필요 |
| 체크포인트 도입 | 과거 블록 보호 | 중앙화 요소 추가 |
| PoW → PoS 전환 | 경제적 처벌(슬래싱) | 지분 집중화 위험 |
| 알고리즘 변경 (ASIC 저항) | 전용 장비 무력화 | 일반 GPU 임대 가능성 |

- **📢 섹션 요약 비유**: 줄 서는 사람들 중 절반 이상이 한 패거리면 순서가 바뀔 수 있다. 이를 막으려면 줄을 선 사람들이 골고루 다양해야 하고, 나쁜 행동을 하면 강력한 처벌이 있어야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **해시레이트 분산도 평가**: 상위 채굴 풀 2~3개의 해시레이트 합산이 50%를 초과하는가? 집중도가 높으면 공모 공격 위험이 있다.
2. **공격 비용 대비 기대 이익 분석**: crypto51.app 등을 활용하여 네트워크 51% 공격의 시간당 비용을 평가했는가? 거래소 입금 한도와 비교했는가?
3. **확인 수 정책**: 거래 금액별로 필요한 확인 수를 정의했는가? 고액 거래는 더 많은 확인이 필요하다.
4. **임대 해시파워 위협**: NiceHash 같은 해시파워 임대 서비스에서 현재 네트워크 규모의 51%를 확보하는 것이 가능한가?
5. **대응 계획**: 51% 공격 탐지 시 거래소 입금 중단, 확인 수 임시 증가 등의 대응 절차가 있는가?
6. **PoS 슬래싱 설계**: PoS 체인의 경우 악의적 검증자에 대한 슬래싱 조건과 처벌 규모가 경제적 억제력으로 충분한가?

### 안티패턴

- **51% 공격을 단순 해킹으로 보는 설계**: 코드 취약점이 아니라 합의 메커니즘 자체를 공격하는 것이므로 소프트웨어 패치로 해결되지 않는다. 근본적인 네트워크 분산도와 경제 설계가 방어선이다.

- **확정되지 않은 거래를 안전하게 처리**: 거래소나 결제 서비스가 1 확인(비트코인 기준 약 10분) 후 바로 코인을 출금 가능하게 하면, 공격자가 2-3블록 Reorg로 이중 지출을 할 수 있다.

- **소규모 체인에서의 과신**: "블록체인은 안전하다"는 통념을 소규모 PoW 체인에 그대로 적용하면 위험하다. 해시레이트가 낮은 체인은 NiceHash 등으로 수천 달러에 공격이 가능하다.

- **PoW와 PoS 동일 기준 적용**: PoS의 공격 임계값(지분 비율)과 PoW의 공격 임계값(해시 파워 비율)은 다르며, 각 방어 방법도 다르다. 이를 혼동하면 잘못된 보안 평가가 나온다.

기술사 관점에서는 51% 공격을 단순 보안 사고가 아니라 블록체인의 합의 신뢰 전제(Trust Assumption)가 무너지는 시나리오로 봐야 한다. "정직한 노드가 과반을 유지한다"는 가정이 성립하는 범위에서만 블록체인 보안이 의미를 갖는다.

- **📢 섹션 요약 비유**: 숫자가 많아지면 규칙도 쉽게 바뀐다. 이 규칙이 쉽게 바뀌지 않으려면 참여자들이 골고루 분산되어 있어야 하고, 규칙을 어기면 자신도 크게 손해를 보는 구조가 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

51% 공격 개념을 이해하면 블록체인 보안의 근본적인 전제와 한계를 명확하게 파악할 수 있다.

**보안 설계 개선**: 확인 수 정책, 채굴 풀 분산화 인센티브, PoS 슬래싱 설계 등 다층적 방어 체계를 구축할 수 있다.

**리스크 평가**: 특정 블록체인 기반 서비스(거래소, 결제 게이트웨이) 도입 시 51% 공격 위험을 정량적으로 평가하고 확인 수 정책 등 리스크 완화 조치를 취할 수 있다.

**생태계 건전성**: 51% 공격 위험은 블록체인 커뮤니티가 채굴 풀 분산화와 광범위한 노드 참여를 지속적으로 추구하는 이유를 설명한다. 비트코인의 수십만 개 노드, 이더리움의 수십만 명 검증자는 이 위협에 대한 직접적인 방어다.

**미래 전망**: PoS로의 전환(이더리움 Merge, 2022)과 슬래싱 메커니즘의 강화는 51% 공격의 경제적 억제력을 높이는 방향이다. 단, PoS에서도 지분 집중화(고래 투자자, 리퀴드 스테이킹 프로토콜)는 새로운 형태의 집중화 위험을 낳는다.

결론적으로 51% 공격은 블록체인의 합의 가정이 깨질 때 어떤 결과가 나타나는지를 보여주는 핵심 위협 시나리오다. 분산도 유지와 경제적 억제력 설계가 방어의 핵심이다.

- **📢 섹션 요약 비유**: 사람들이 너무 한쪽에 많으면 결과가 흔들린다. 이를 막으려면 참여자들이 골고루 분산되어야 하고, 나쁜 행동을 하면 자신도 크게 손해를 보도록 설계해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 이중 지출 (Double Spending) | 51% 공격의 주요 목표 |
| 체인 재구성 (Reorg) | 51% 공격의 핵심 메커니즘 |
| 해시레이트 (Hashrate) | PoW에서 51% 공격 자원의 척도 |
| 채굴 풀 (Mining Pool) | 51% 공격 집중화 위험의 주요 요인 |
| 확인 수 (Confirmations) | 51% 공격 방어를 위한 대기 기준 |
| 슬래싱 (Slashing) | PoS에서 악의적 검증자에 대한 경제적 처벌 |
| NiceHash | 해시파워 임대 서비스, 소규모 체인 공격 가능 |
| 셀피시 채굴 (Selfish Mining) | 51% 미만으로도 유리한 위치를 점하는 전략 |
| 완결성 (Finality) | 51% 공격이 위협하는 핵심 블록체인 속성 |
| PoS 전환 | 51% 공격 방어력을 경제적 처벌로 강화하는 방향 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">51% 공격 위협과 방어 발전 흐름</div></div>
<div class="kb-diagram-note">블록체인 초기: "정직한 노드 과반" 가정 (2009~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">소규모 체인 공격 실증 (2018~2020)</div>
<div class="kb-diagram-note">BTG, VTC, ETC 실제 피해 발생</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">방어 대응:</div>
<div class="kb-diagram-tree-item" style="--depth:2">확인 수 정책 강화 (거래소)</div>
<div class="kb-diagram-tree-item" style="--depth:2">체크포인트 도입 (ETC)</div>
<div class="kb-diagram-tree-item" style="--depth:2">PoW → PoS 전환 연구</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이더리움 Merge (2022)</div>
<div class="kb-diagram-note">PoW → PoS 전환, 슬래싱 도입</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: PoS 생태계의 새로운 집중화 위험</div>
<div class="kb-diagram-note">리퀴드 스테이킹 (Lido 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">미래: 분산화 인센티브 설계 + 다층 방어</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 블록체인은 많은 사람이 함께 같은 장부를 쓰는데, 한 사람이 장부를 절반 이상 가지면 내용을 마음대로 바꿀 수 있어요.
2. 그게 51% 공격이에요 — 공격자가 이미 준 물건값을 되돌려 받으면서 물건은 그대로 갖는 거예요!
3. 그래서 블록체인이 안전하려면 장부를 많은 사람이 골고루 나눠 가지고 있어야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 552

← **이전**: [66. 지향성 비순환 그래프 (DAG, Directed Acyclic Graph) - 블록체인 대신 트랜잭션들이 거미줄처럼 서로를 증명하는](/knowledge-base/studynote/06_ict_convergence/01_blockchain/066_dag_directed_acyclic_graph_tangle/)
**다음**: [68. 이클립스 공격 (Eclipse Attack) - 특정 노드의 주변 P2P 연결을 악성 노드가 장악하여 네트워크를 고립시키고 허위](/knowledge-base/studynote/06_ict_convergence/01_blockchain/068_eclipse_attack_p2p_isolation/) →

---
