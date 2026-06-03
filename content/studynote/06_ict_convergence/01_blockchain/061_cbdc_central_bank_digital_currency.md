+++
title = "61. CBDC (Central Bank Digital Currency) - 중앙은행 디지털 화폐"
date = 2026-04-07

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CBDC(Central Bank Digital Currency)는 중앙은행이 직접 발행하고 가치를 보증하는 공식 디지털 법정화폐로, 민간 암호화폐와 본질적으로 다르다.
> 2. **가치**: 가격 변동성이 거의 없고, 결제·송금·통화정책 집행을 디지털로 정교하게 수행할 수 있으며, 금융 포용(Financial Inclusion)을 실현하는 국가 결제 인프라다.
> 3. **판단 포인트**: 소매형(Retail)과 도매형(Wholesale) 설계 목적이 근본적으로 다르며, 개인정보 보호와 거래 추적성의 균형, 기존 금융 인프라와의 공존 전략이 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

현금 사용은 전 세계적으로 급격히 줄어들고 있다. 스마트폰 결제, 간편 송금, 디지털 지갑이 일상화되면서 종이돈과 동전은 뒷전으로 밀리고 있다. 그러나 민간 전자지갑(Pay 서비스)이나 신용카드망만으로는 국가가 화폐 흐름을 직접 설계·통제하기 어렵다. 민간 결제 플랫폼은 독점화 우려가 있고, 민간 암호화폐(Bitcoin, Ethereum 등)는 가격 변동성이 극심해 법정화폐의 대안이 될 수 없다.

CBDC는 이런 환경에서 국가가 직접 발행하는 디지털 현금이다. 중앙은행이 법적 권위와 신뢰를 바탕으로 발행하기 때문에 시장 가격 변동 없이 법정통화와 1:1 가치를 유지한다. 단순한 전자화폐가 아니라 통화정책, 금융 안정성, 결제 효율화, 금융 포용이라는 복합적 목표를 동시에 달성하기 위한 국가 결제 인프라 재설계다.

2024년 기준으로 전 세계 130개국 이상이 CBDC를 연구·개발 중이며, 바하마(Sand Dollar), 나이지리아(eNaira), 중국(디지털 위안·e-CNY) 등이 이미 실제 운영 중이다. 한국도 한국은행 주도로 CBDC 파일럿 테스트를 진행하고 있다. BIS(국제결제은행)는 2030년까지 전 세계 주요국의 다수가 CBDC를 도입할 것으로 전망한다.

CBDC가 필요한 이유를 기술사 관점에서 정리하면: 첫째, 현금 쇠퇴 대응 - 디지털 경제에서 중앙은행의 화폐 공급 역할을 유지해야 한다. 둘째, 금융 포용 - 은행 계좌 없는 취약 계층도 디지털 결제에 참여할 수 있게 한다. 셋째, 결제 효율화 - 국경 간 송금 비용과 시간을 획기적으로 줄인다. 넷째, 통화 주권 수호 - 페이스북의 리브라(Libra)와 같은 민간 글로벌 스테이블코인에 대한 국가 주권 방어다.

- **📢 섹션 요약 비유**: 종이돈을 스마트폰 안에 넣되, 그 돈의 주인은 여전히 국가이고 가치 보증도 국가가 하는 셈이다. 네이버페이나 카카오페이와 달리, 이 디지털 지갑 안의 돈은 은행 예금이 아니라 현금 그 자체다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. CBDC의 두 가지 유형

| 구분 | 소매형 (Retail CBDC) | 도매형 (Wholesale CBDC) |
| :--- | :--- | :--- |
| 대상 | 일반 국민, 기업 | 금융기관, 중앙은행 |
| 목적 | 일상 결제, 금융 포용 | 기관 간 정산, 교차 통화 |
| 익명성 | 설계에 따라 조절 가능 | 일반적으로 신원 확인 필수 |
| 사례 | 중국 e-CNY, 바하마 Sand Dollar | FedNow, BIS mBridge |
| 보안 요건 | 소비자 단말 보안 중요 | 기관 간 네트워크 보안 중요 |

### 2. 기술 구조 모델

CBDC는 크게 세 가지 기술 구조로 설계된다.

**직접형(Direct) 모델**: 중앙은행이 개인에게 직접 계좌를 제공한다. 중간 기관 없이 중앙은행과 개인이 직접 연결되어 간단하지만, 중앙은행이 수억 개의 소매 계좌를 직접 관리해야 하는 운영 부담이 있다.

**간접형(Indirect) 모델**: 중앙은행이 상업은행에 CBDC를 발행하고, 상업은행이 개인에게 유통한다. 기존 은행 인프라를 활용할 수 있고, 중앙은행의 운영 부담이 줄어든다. 대부분의 국가가 선호하는 방식이다.

**혼합형(Hybrid) 모델**: 간접형과 유사하지만 중앙은행이 최종 원장(Ledger)을 관리한다. 민간 기관이 유통을 담당하지만 소유권 기록은 중앙은행이 보유한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">CBDC 아키텍처 계층도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중앙은행 (Central Bank)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- CBDC 발행/소각</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 마스터 원장 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 통화정책 연계</div></div>
<div class="kb-diagram-note">도매 CBDC (Wholesale)</div>
<div class="kb-diagram-note">발행 / 정산</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중간 기관 (상업은행 / 결제 서비스 제공사)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 소매 CBDC 유통</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- KYC/AML 수행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 고객 지갑 서비스</div></div>
<div class="kb-diagram-note">소매 CBDC (Retail)</div>
<div class="kb-diagram-note">지갑 / 결제</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">개인 / 기업 (최종 사용자)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 모바일 지갑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- NFC 결제, QR코드 결제</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 오프라인 결제 (칩 내장 카드 등)</div></div>
</div>
</div>



### 3. 핵심 설계 차원

| 설계 차원 | 옵션 A | 옵션 B | 설명 |
| :--- | :--- | :--- | :--- |
| 계좌 방식 | Account-based | Token-based | 계좌 vs 토큰 중심 |
| 익명성 | 완전 실명 | 단계적 익명 | 소액은 익명, 고액은 신원 확인 |
| 이자 부여 | 이자형 | 무이자형 | 저축 수단 vs 결제 수단 |
| 오프라인 | 지원 | 미지원 | 네트워크 끊겨도 결제 가능 여부 |
| 프로그래머빌리티 | 스마트 컨트랙트 활용 | 단순 이전만 | 조건부 지급, 지원금 자동 분배 |

### 4. 프로그래머블 화폐 (Programmable Money)

CBDC의 혁신적 기능 중 하나는 프로그래머빌리티다. 스마트 컨트랙트(Smart Contract)를 결합하면:
- 사용 조건 설정: 복지 지원금을 식품 구매에만 사용하도록 제한
- 만료 기한 설정: 경기 부양을 위한 소비 기한 설정
- 자동 세금 납부: 거래 시 세금이 자동으로 국고로 이전
- 조건부 해제: 특정 조건 충족 시 자동으로 결제 승인

이는 기존 화폐로는 불가능한 새로운 통화정책 수단이지만, 프라이버시 침해 우려도 동반한다.

- **📢 섹션 요약 비유**: 장난감 동전이 아니라, 은행 시스템 전체와 연결된 디지털 지폐다. 게다가 이 지폐는 '언제, 어디서, 무엇을 살 수 있는지'까지 프로그래밍할 수 있는 스마트 화폐다.

---

## Ⅲ. 비교 및 연결

### 1. CBDC vs 유사 개념 비교

| 항목 | 현금 | 은행 예금 | 민간 스테이블코인 | 민간 암호화폐 | CBDC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 발행 주체 | 중앙은행 | 상업은행 | 민간 기업 | 분산 네트워크 | 중앙은행 |
| 부채 성격 | 중앙은행 직접 부채 | 상업은행 부채 | 발행사 부채 | 없음 | 중앙은행 직접 부채 |
| 가치 | 법정통화 | 예금보험 한도 내 안전 | 담보 자산 의존 | 시장 변동 | 법정통화와 동일 |
| 익명성 | 높음 | 낮음(KYC) | 설계 의존 | 설계 의존 | 정책에 따라 조절 |
| 결제 속도 | 오프라인 강점 | 영업일 의존 | 네트워크 의존 | 네트워크 의존 | 정책에 따라 최적화 |
| 프로그래머빌리티 | 없음 | 제한적 | 가능 | 가능 | 가능 |
| 규제 | 국가 법령 | 은행법 | 신규 규제 대상 | 불명확 | 중앙은행법 |

### 2. 주요국 CBDC 현황 비교

| 국가 | 명칭 | 단계 | 특징 |
| :--- | :--- | :--- | :--- |
| 중국 | e-CNY (디지털 위안) | 실제 운영 중 | 2022 베이징 올림픽 시범, 소매형, 이중 오프라인 결제 |
| 유럽연합 | 디지털 유로 | 준비 단계 | ECB 주도, 2025~2026 실증 예정 |
| 미국 | FedNow (도매 인접) | 연구/논의 중 | 개인정보 우려로 소매형 신중 |
| 바하마 | Sand Dollar | 실제 운영 중 | 세계 최초 소매 CBDC |
| 한국 | 한국은행 파일럿 | 시범 운영 | 분산원장 기반 시범 테스트 |
| 나이지리아 | eNaira | 실제 운영 중 | 아프리카 최초, 금융 포용 목적 |

### 3. CBDC와 DeFi의 충돌과 공존

CBDC는 중앙화된 통제를 강화하는 반면, 탈중앙화 금융(DeFi, Decentralized Finance)은 탈중앙화를 지향한다. 이 둘은 상반된 철학을 갖지만, 향후 도매형 CBDC가 DeFi 인프라와 연결되는 하이브리드 모델이 등장할 가능성도 있다. 예를 들어 규제된 스테이블코인이 CBDC와 연동되어 DeFi 생태계의 안정적 결제 수단이 되는 시나리오다.

- **📢 섹션 요약 비유**: 동네 가게에서 쓰는 소액 쿠폰(Retail CBDC)과 은행끼리 주고받는 정산 장부(Wholesale CBDC)는 쓰임새가 다르다. 전자는 편의점 결제, 후자는 은행 간 대출 정산이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **유형 구분**: 지급 결제의 목표가 소매형(국민 일상 결제)인지 도매형(기관 간 정산)인지 명확히 구분했는가?
2. **프라이버시 균형**: 개인정보 보호와 거래 추적성(AML/CFT) 간의 균형점을 설계했는가? 소액 거래 익명화와 고액 거래 신원 확인의 임계값은?
3. **오프라인 결제**: 인터넷 끊김, 재난 상황에서도 결제가 가능한 오프라인 모드를 지원하는가?
4. **역할 분리**: 중앙은행(발행/정책), 상업은행(유통/KYC), 개인(사용)의 역할과 책임이 명확히 분리되어 있는가?
5. **공존 전략**: 현금, 카드, 간편결제와의 공존 로드맵이 있는가? 기존 결제 인프라 투자를 어떻게 보호할 것인가?
6. **사이버 보안**: 단일 실패점(Single Point of Failure) 없는 고가용성 인프라인가? 국가 차원의 사이버 공격에 대한 복원력이 있는가?
7. **프로그래머빌리티 범위**: 스마트 컨트랙트 기능을 어디까지 허용할 것인가? 지나친 통제는 프라이버시 침해다.
8. **국경 간 상호운용성**: 다른 나라 CBDC와의 교환(mBridge, Nexus 등)을 고려했는가?

### 안티패턴

- **민간 암호화폐와 동일시하는 설계**: CBDC는 분산화와 탈중앙화를 목표로 하지 않는다. 비트코인처럼 설계하면 중앙은행의 통화정책 수단이 오히려 약화된다.

- **과도한 감시 설계**: 모든 거래를 실시간으로 국가가 추적하는 설계는 정치적 반발과 신뢰 붕괴를 초래한다. 독재 정권의 재정 감시 도구로 악용될 위험이 있다.

- **기존 결제망 무시 설계**: 기존 카드사, 간편결제 회사와의 공존 전략 없이 CBDC만 강제 도입하면 결제 생태계 혼란을 야기한다. 시장 파괴(Market Disruption)는 단기적으로 금융 불안을 키운다.

- **이자 설정 오류**: Retail CBDC에 높은 이자를 부여하면 상업은행 예금이 CBDC로 대규모 이동(Bank Run)하여 금융 안정성을 해친다. 이자율 설계는 통화정책과 연계해야 한다.

- **기술 선택 편향**: 블록체인 기술이 반드시 필요하지 않을 수 있다. 목적에 따라 중앙화 데이터베이스가 더 효율적일 수 있다. 기술을 목적에 맞게 선택해야 한다.

기술사 관점에서는 CBDC를 "새 코인"이 아니라 "국가 결제 인프라의 재설계"로 봐야 한다. 기술, 통화정책, 규제가 함께 정합성을 가져야 실제로 작동하며, 어느 하나만 앞서면 시스템 전체가 불안정해진다.

- **📢 섹션 요약 비유**: 새 지갑을 만드는 일이 아니라, 나라의 돈 흐름도를 다시 그리는 일이다. 지갑 디자인보다 '어떤 경로로 돈이 돌아야 하는가'라는 설계 철학이 먼저다.

---

## Ⅴ. 기대효과 및 결론

CBDC가 제대로 설계·도입될 경우 기대할 수 있는 효과는 다음과 같다.

**정량적 효과**: 국경 간 송금 비용 현재 평균 6%대에서 1% 이하로 감소, 결제 정산 시간을 수일에서 실시간(T+0)으로 단축, 지하경제 양성화로 세수 확대, 현금 발행·유통 비용(전 세계 연간 약 3,000억 달러 추산) 절감.

**정성적 효과**: 금융 서비스 소외 계층의 포용(인터넷 없는 오지에서도 칩 기반 오프라인 결제), 통화정책 전달 경로 단순화(마이너스 금리나 헬리콥터 머니 등을 직접 구현 가능), 민간 결제 플랫폼 의존도 감소로 금융 주권 강화.

**미래 전망**: BIS(국제결제은행)가 추진하는 다중통화 CBDC 플랫폼(mBridge)은 여러 나라의 CBDC를 직접 교환하는 글로벌 결제 인프라다. 실현되면 SWIFT 기반 국제 송금 체계를 근본적으로 대체할 수 있다. 또한 IoT 기기 간 자동 마이크로 결제(M2M Payment)도 CBDC의 프로그래머빌리티를 통해 가능해진다.

결국 CBDC는 기술 경쟁이 아니라, 돈의 신뢰를 디지털로 옮기는 사회적 설계 문제다. 성공적인 CBDC는 기술적으로 견고하고, 경제적으로 안정적이며, 사회적으로 수용 가능한 세 가지 조건을 동시에 충족해야 한다.

- **📢 섹션 요약 비유**: 현금의 믿음을 스마트폰 속으로 옮기되, 신뢰의 무게는 그대로 지켜야 한다. 폼은 바뀌어도 본질—국가가 보증하는 화폐—은 변하지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 스테이블코인(Stablecoin) | 민간 발행 vs. 국가 발행 CBDC 비교 |
| 스마트 컨트랙트(Smart Contract) | CBDC의 프로그래머빌리티 구현 기반 |
| DeFi (탈중앙화 금융) | CBDC와 DeFi 생태계 충돌·공존 관계 |
| KYC / AML | CBDC 신원 확인 및 자금 세탁 방지 설계 |
| 분산원장기술(DLT) | CBDC의 기술 인프라 옵션 중 하나 |
| 블록체인 | CBDC에 활용 가능한 분산 원장 기술 |
| 금융 포용(Financial Inclusion) | Retail CBDC의 핵심 정책 목표 |
| 통화정책(Monetary Policy) | CBDC를 통한 금리·유동성 정책 집행 |
| mBridge | BIS 주도 다중통화 CBDC 국제 플랫폼 |
| 개인정보 보호 | CBDC 설계의 핵심 균형 이슈 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">화폐의 디지털화 진화</div></div>
<div class="kb-diagram-note">현금 (종이·동전)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">전자결제 (카드, 계좌이체)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">간편결제 (페이 서비스)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">민간 암호화폐 (Bitcoin, Ethereum)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">스테이블코인 (USDC, USDT)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CBDC (중앙은행 디지털 화폐) ← 현재</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">다중통화 CBDC (mBridge, Nexus)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">프로그래머블 화폐 + IoT M2M 결제</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. CBDC는 종이돈을 스마트폰에 넣은 것처럼 보이지만, 실제 주인은 나라이고 가치도 나라가 보장해 줘요.
2. 그래서 비트코인처럼 가격이 오르락내리락하지 않고 언제나 똑같은 가치를 가져요.
3. 대신 이 디지털 돈을 어떻게 쓸 수 있는지, 누가 가질 수 있는지를 아주 신중하게 정해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 552

← **이전**: [60. 하이퍼레저 아키텍처 - 피어(Peer), 오더러(Orderer), MSP(Membership Service Provider)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/060_hyperledger_architecture_peer_orderer_msp/)
**다음**: [62. 비트코인 반감기 (Halving) - 약 4년마다 채굴 보상이 절반으로 줄어드는 메커니즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/062_bitcoin_halving_supply_shock/) →

---
