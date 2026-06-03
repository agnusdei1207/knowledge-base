+++
title = "DeFi (Decentralized Finance, 탈중앙화 금융)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

> **핵심 인사이트 3줄**
> 1. DeFi(Decentralized Finance)는 [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)를 기반으로 은행·거래소·보험 등 전통 금융 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 탈중앙·무허가·투명한 방식으로 제공하는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 금융 생태계다.
> 2. AMM(Automated Market Maker)·유동성 풀·수익 농업(Yield Farming)·담보 대출이 DeFi의 핵심 메커니즘으로, 코드가 규칙이고 알고리즘이 은행원 역할을 한다.
> 3. DeFi는 금융 포용성(Unbanked 20억 명 접근 가능)과 24/7 무중단 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 제공하지만, [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 버그·플래시론 공격·규제 불확실성이 주요 위험이다.

---

## Ⅰ. DeFi의 정의와 TradFi 비교

DeFi(Decentralized Finance, [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 금융)는 <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a> <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">스마트 컨트랙트</a>로 구현한 탈중앙 금융 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 생태계</strong>다.

| 특성          | TradFi (전통 금융)     | DeFi                     |
|-------------|----------------------|--------------------------|
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 주체   | 은행·증권사·보험사    | [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 코드       |
| [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/)       | 계좌 개설, KYC 필요  | 지갑만 있으면 누구나       |
| 운영 시간    | 영업일 09:00-16:00   | 24/7/365 무중단            |
| 투명성       | 블랙박스 (내부 불공개) | 코드 공개·온체인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)      |
| 수탁        | 은행이 자산 보관      | 사용자 개인키로 자기 수탁  |
| 규제        | 감독기관 통제 하에    | 퍼미션리스, 규제 불확실    |

📢 **섹션 요약 비유**: DeFi는 직원 없는 은행이다 — [ATM](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/272_atm_asynchronous_transfer_mode_53byte_cell/)([스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))이 모든 업무를 처리하고, 운영시간도 없으며, 전 세계 누구나 이용할 수 있다.

---

## Ⅱ. AMM (Automated Market Maker) — 탈중앙 거래소 핵심

### Uniswap v2 AMM 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">x × y = k (상수 곱 공식)</div>
<div class="kb-diagram-note">유동성 풀: ETH 100개, USDC 200,000개 → k = 20,000,000</div>
<div class="kb-diagram-note">ETH 1개 구매 시:</div>
<div class="kb-diagram-note">ETH: 100 - 1 = 99</div>
<div class="kb-diagram-note">USDC: 20,000,000 / 99 ≈ 202,020 → 증가분 2,020 USDC 지불</div>
<div class="kb-diagram-note">→ 실효 가격: 2,020 USDC/ETH (슬리피지 발생)</div>
</div>
</div>



### 유동성 공급자 (LP, Liquidity [Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/))

- LP가 두 토큰을 1:1 비율로 풀에 예치
- 거래 수수료 0.3% 수익 (Uniswap v2 기준)
- LP 토큰 발행 → 지분 표시 → 출금 시 반납

📢 **섹션 요약 비유**: AMM 유동성 풀은 환전소 금고다 — 금고에 달러와 원화를 채워두면, 누군가 환전할 때마다 자동으로 비율이 바뀌고 수수료가 쌓인다.

---

## Ⅲ. DeFi 핵심 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)

| 카테고리   | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)          | 기능                        | TVL (2024 기준) |
|----------|-----------------|----------------------------|---------------|
| DEX      | Uniswap, Curve  | 토큰 교환 (AMM 기반)         | $5B+          |
| 대출     | Aave, Compound  | 담보 예치 → 대출 (초과 담보) | $10B+         |
| 스테이블  | MakerDAO (DAI)  | [ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/) 담보 → DAI 발행          | $4B+          |
| 수익 최적 | Yearn Finance   | DeFi [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 자동화             | $500M+        |
| 보험     | Nexus Mutual    | [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 위험 보장     | $300M+        |

### DeFi 레고 블록 조합 (Composability)

```
Aave에서 ETH 담보 대출 → Curve DEX에서 스왑 →
Yearn Vault에 예치 → 복리 수익 자동 재투자
```

**"Money Lego"**: DeFi [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)들이 API처럼 조합 가능

📢 **섹션 요약 비유**: DeFi 레고는 금융 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 조합이다 — 빌리고(Aave), 바꾸고(Uniswap), 예치(Yearn)하는 과정을 코드 한 줄로 원스톱 처리할 수 있다.

---

## Ⅳ. DeFi 위험 요소

### 주요 공격 유형

| 공격          | 원리                             | 사례                  |
|-------------|----------------------------------|----------------------|
| 플래시론     | 같은 TX에서 무담보 대출→조작→상환 | bZx, Euler ($197M)   |
| 재진입 공격  | 콜백 함수 악용해 반복 출금        | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) Hack (2016, $60M)|
| 오라클 조작  | 가격 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조작 → 청산 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)    | Mango Markets ($117M)|
| 러그풀       | 개발자가 유동성 전액 인출         | Squid Game Token     |

### 비영구적 손실 (Impermanent Loss)

```
LP로 ETH/USDC 예치 후 ETH 가격 2배 상승 시:
  그냥 보유했을 때보다 LP 수익이 낮음
  → "비영구적" 손실 (풀 철수 시 확정)
```

📢 **섹션 요약 비유**: 플래시론 공격은 빈 수표다 — 잠깐 빌려서 사기치고 돌려주는 건데, 은행이 같은 날 입출금을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 안 한 빈틈을 이용한다.

---

## Ⅴ. DeFi 2.0과 규제 동향

### DeFi 2.0 개선 사항

- <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 소유 유동성 (POL)</strong>: Olympus [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 모델
- <strong>실물자산 <a href="/knowledge-base/studynote/09_security/16_data_privacy/820_tokenization/">토큰화</a> (RWA)</strong>: 채권·부동산의 온체인 표현
- **L2 DeFi**: Arbitrum·Optimism 위 가스비 99% 절감
- **크로스체인 DeFi**: LayerZero·Axelar 브릿지

### 규제 현황

```
EU MiCA (2024 시행): 스테이블코인·가상자산 발행자 규제
미국 SEC: DeFi 프로토콜 증권법 적용 시도
한국 가상자산이용자보호법 (2024): 거래소 규제 본격화
```

📢 **섹션 요약 비유**: DeFi 규제는 무법 서부 개척지에 법원이 생기는 것이다 — 자유롭지만 사기도 많았던 DeFi에 규칙(MiCA)이 생기면서 기관 투자자 진입이 가능해진다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DeFi (Decentralized Finance)</div>
<div class="kb-diagram-tree-item" style="--depth:0">핵심 메커니즘</div>
<div class="kb-diagram-note">── AMM (Automated Market Maker)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 상수 곱 공식 x·y=k</div></div>
<div class="kb-diagram-note">── 유동성 풀 / LP 토큰</div>
<div class="kb-diagram-note">── 초과 담보 대출</div>
<div class="kb-diagram-tree-item" style="--depth:0">주요 프로토콜</div>
<div class="kb-diagram-note">── DEX: Uniswap, Curve</div>
<div class="kb-diagram-note">── 대출: Aave, Compound</div>
<div class="kb-diagram-note">── 스테이블: MakerDAO</div>
<div class="kb-diagram-tree-item" style="--depth:0">위험</div>
<div class="kb-diagram-note">── 플래시론 공격</div>
<div class="kb-diagram-note">── 재진입 공격</div>
<div class="kb-diagram-note">── 비영구적 손실 (IL)</div>
<div class="kb-diagram-tree-item" style="--depth:0">발전 방향</div>
<div class="kb-diagram-tree-item" style="--depth:2">RWA 토큰화</div>
<div class="kb-diagram-tree-item" style="--depth:2">L2 DeFi</div>
<div class="kb-diagram-tree-item" style="--depth:2">MiCA 규제 대응</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DeFi 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2017년</div><div class="kb-diagram-cell">MakerDAO 등장</div><div class="kb-diagram-cell">최초 DeFi — CDP·DAI 스테이블</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2018년</div><div class="kb-diagram-cell">Uniswap v1 출시</div><div class="kb-diagram-cell">AMM 패러다임 시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2020년</div><div class="kb-diagram-cell">DeFi Summer</div><div class="kb-diagram-cell">Compound·YFI·유동성 채굴 폭발</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2021년</div><div class="kb-diagram-cell">TVL $100B 돌파</div><div class="kb-diagram-cell">Curve·Aave·L2 DeFi 확장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2022년</div><div class="kb-diagram-cell">크립토 윈터·붕괴</div><div class="kb-diagram-cell">Terra/LUNA·Celsius 파산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2024년</div><div class="kb-diagram-cell">MiCA·RWA·ETF 승인</div><div class="kb-diagram-cell">기관 DeFi·규제 명확화</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">스마트 컨트랙트 → AMM → 유동성 풀 → 수익 농업</div>
<div class="kb-diagram-note">Solidity/EVM x·y=k LP 토큰 Yield Farming</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DeFi 레고(Composability) → TVL 성장 → 규제 강화</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. DeFi는 직원 없는 자동 환전소다 — 코드([스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))가 24시간 자동으로 환전·대출·이자 지급을 처리한다.
2. AMM 유동성 풀은 저울이다 — 한쪽에 이더리움, 다른 쪽에 달러를 올려두고 저울이 항상 균형을 맞추도록 자동으로 가격이 바뀐다.
3. DeFi 레고는 금융 블록 조합이다 — 빌리는 블록, 교환 블록, 예금 블록을 코드로 연결하면 복잡한 금융 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 자동으로 실행된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 552

← **이전**: [DApp (Decentralized Application, 분산 애플리케이션)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/)
**다음**: [유니스왑·AMM (Automated Market Maker, 자동화 시장 조성자)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/034_uniswap_amm_automated_market_maker/) →

---
