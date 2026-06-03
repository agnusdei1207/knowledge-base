+++
title = "043. 옵티미스틱 롤업 & 사기 증명 (Optimistic Rollup & Fraud Proof)"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

> **핵심 인사이트**
> 1. 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)(Optimistic [Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/))은 "일단 믿고, 문제 있으면 증명"하는 낙관적 가정으로 설계된 이더리움 Layer 2 확장 솔루션으로 — ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)과 달리 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 유효성 증명을 즉시 생성하지 않아 [가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/) 비용이 낮지만, 출금 시 7일 이의제기 기간(Challenge Period)이 발생한다.
> 2. 사기 증명(Fraud Proof)은 "시퀀서가 잘못된 상태 전이를 제출했다"고 누군가 증명하면 해당 배치가 롤백되는 메커니즘으로 — 이의제기자에게 보상을 주어 감시 인센티브를 만들고 시퀀서에게 슬래시(Slash) 패널티를 부과한다.
> 3. Optimism(OP [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))과 Arbitrum이 양대 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 구현체이며 — OP Stack의 오픈소스화로 Base(Coinbase), Zora, Mantle 등 수십 개의 Layer 2 체인이 동일한 스택으로 구축되는 "Superchain" 생태계가 형성되고 있다.

---

## Ⅰ. 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">롤업 (Rollup) 원리:</div>
<div class="kb-diagram-note">대량 트랜잭션을 L2(Layer 2)에서 실행</div>
<div class="kb-diagram-note">→ 실행 결과(상태 루트)만 L1(이더리움 메인넷)에 제출</div>
<div class="kb-diagram-note">→ L1 데이터 가용성 활용 + L1 실행 비용 절감</div>
<div class="kb-diagram-note">옵티미스틱 (Optimistic) 의미:</div>
<div class="kb-diagram-note">"트랜잭션이 유효하다고 낙관적으로 가정"</div>
<div class="kb-diagram-note">즉시 유효성 검증 없이 상태 전이 수용</div>
<div class="kb-diagram-note">vs ZK 롤업:</div>
<div class="kb-diagram-note">ZK: 매 배치마다 유효성 증명(zk-proof) 생성 및 검증</div>
<div class="kb-diagram-note">Optimistic: 7일 이의제기 기간 동안 누가 문제 제기하지 않으면 확정</div>
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-note">시퀀서 (Sequencer):</div>
<div class="kb-diagram-note">L2 트랜잭션 수집 및 순서 결정</div>
<div class="kb-diagram-note">배치 상태 루트를 L1에 제출</div>
<div class="kb-diagram-note">L1 계약 (Rollup Contract):</div>
<div class="kb-diagram-note">배치 데이터 저장 (calldata or blob)</div>
<div class="kb-diagram-note">상태 루트 기록</div>
<div class="kb-diagram-note">이의제기 처리</div>
<div class="kb-diagram-note">이의제기자 (Challenger):</div>
<div class="kb-diagram-note">배치 데이터를 재실행하여 검증</div>
<div class="kb-diagram-note">오류 발견 시 사기 증명 제출</div>
<div class="kb-diagram-note">흐름:</div>
<div class="kb-diagram-note">L2 트랜잭션 → 시퀀서 → 배치 압축 → L1 제출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">7일 이의제기 기간</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이의 없음 → 최종 확정</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 선불 여행 정산 — 회사 출장비를 먼저 쓰고(L2 실행), 나중에 영수증 제출(L1 제출). 7일 내 문제 제기 없으면 확정.

---

## Ⅱ. 사기 증명 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">사기 증명 (Fraud Proof) 단계:</div>
<div class="kb-diagram-note">1. 시퀀서의 잘못된 상태 전이 제출:</div>
<div class="kb-diagram-note">배치 번호 100: 상태루트 WRONG_ROOT 제출</div>
<div class="kb-diagram-note">(실제 올바른 상태루트: CORRECT_ROOT)</div>
<div class="kb-diagram-note">2. 이의제기자가 오류 발견:</div>
<div class="kb-diagram-note">배치 데이터 다운로드 (L1 calldata/blob)</div>
<div class="kb-diagram-note">자체 실행 결과: CORRECT_ROOT</div>
<div class="kb-diagram-note">시퀀서 제출: WRONG_ROOT</div>
<div class="kb-diagram-note">→ 불일치 탐지!</div>
<div class="kb-diagram-note">3. 이의제기 (Challenge) 제출:</div>
<div class="kb-diagram-note">L1 Rollup 계약에 이의제기 트랜잭션 발송</div>
<div class="kb-diagram-note">경쟁적 게임 시작</div>
<div class="kb-diagram-note">4. 인터랙티브 이분 게임 (Arbitrum 방식):</div>
<div class="kb-diagram-note">"배치 내 어느 트랜잭션이 잘못됐나?"를 절반씩 좁힘</div>
<div class="kb-diagram-note">최종적으로 단일 트랜잭션 오류 특정</div>
<div class="kb-diagram-note">L1에서 해당 트랜잭션만 재실행 (저비용)</div>
<div class="kb-diagram-note">5. 판정:</div>
<div class="kb-diagram-note">시퀀서 잘못 → 상태 롤백, 시퀀서 슬래시(Slash)</div>
<div class="kb-diagram-note">이의제기 잘못 → 이의제기자 보증금 몰수</div>
<div class="kb-diagram-note">인센티브 설계:</div>
<div class="kb-diagram-note">이의제기자: 성공 시 보상 (시퀀서 슬래시 일부)</div>
<div class="kb-diagram-note">시퀀서: 허위 제출 시 본딩(Bonding) 자산 몰수</div>
<div class="kb-diagram-note">→ 게임이론적 균형: 시퀀서가 정직하게 행동하도록 유도</div>
<div class="kb-diagram-note">이의제기 기간:</div>
<div class="kb-diagram-note">Optimism: 7일</div>
<div class="kb-diagram-note">Arbitrum: 7일</div>
<div class="kb-diagram-note">이유: 이더리움 이클립스 공격 방어 시간 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 사기 증명은 법원 항소 시스템 — 판결(상태 제출) 후 7일 안에 이의신청(Fraud Proof) 가능. 이의가 타당하면 판결 취소, 아니면 확정.

---

## Ⅲ. Optimism vs Arbitrum



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비교:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">Optimism (OP Stack)</div><div class="kb-diagram-cell">Arbitrum One</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">사기 증명</div><div class="kb-diagram-cell">단일 라운드 (Non-interactive)</div><div class="kb-diagram-cell">인터랙티브 이분 게임</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">가스 비용</div><div class="kb-diagram-cell">유사</div><div class="kb-diagram-cell">약간 저렴</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">EVM 호환성</div><div class="kb-diagram-cell">100% EVM 동일</div><div class="kb-diagram-cell">EVM 동일 (Arbitrum Stylus)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스택 오픈소스</div><div class="kb-diagram-cell">OP Stack (MIT 라이선스)</div><div class="kb-diagram-cell">BOLD (사기 증명 개선)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">체인 생태계</div><div class="kb-diagram-cell">Superchain (Base, Zora)</div><div class="kb-diagram-cell">Arbitrum Orbit</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TVL (2025)</div><div class="kb-diagram-cell">~$8B</div><div class="kb-diagram-cell">~$15B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출금 시간</div><div class="kb-diagram-cell">7일</div><div class="kb-diagram-cell">7일</div></div>
<div class="kb-diagram-note">Optimism OP Stack:</div>
<div class="kb-diagram-note">OP Mainnet: 최초 배포</div>
<div class="kb-diagram-note">Base (Coinbase): OP Stack 기반</div>
<div class="kb-diagram-note">Zora: NFT 특화 OP Stack 체인</div>
<div class="kb-diagram-note">Mantle: OP Stack 변형</div>
<div class="kb-diagram-note">Arbitrum:</div>
<div class="kb-diagram-note">Arbitrum One: 범용 L2</div>
<div class="kb-diagram-note">Arbitrum Nova: 게임/소셜 (AnyTrust, 낮은 비용)</div>
<div class="kb-diagram-note">Arbitrum Orbit: OP Stack처럼 자체 체인 구축 프레임워크</div>
<div class="kb-diagram-note">공통점:</div>
<div class="kb-diagram-note">EVM 호환</div>
<div class="kb-diagram-note">이더리움 데이터 가용성 활용</div>
<div class="kb-diagram-note">7일 이의제기 기간</div>
<div class="kb-diagram-note">Bridging 인터페이스 제공</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Optimism vs Arbitrum은 두 제조사의 동일 규격 TV — 화면은 똑같이 잘 나오지만 내부 작동 방식(사기 증명 구현)이 달라요. Optimism은 삼성, Arbitrum은 LG.

---

## Ⅳ. ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)과의 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Optimistic vs ZK Rollup:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">Optimistic Rollup</div><div class="kb-diagram-cell">ZK Rollup</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">유효성 검증</div><div class="kb-diagram-cell">이의제기 기간 (사후)</div><div class="kb-diagram-cell">즉시 (zk-proof)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출금 지연</div><div class="kb-diagram-cell">7일</div><div class="kb-diagram-cell">수십 분~수 시간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">EVM 호환성</div><div class="kb-diagram-cell">100% (간단)</div><div class="kb-diagram-cell">zkEVM 필요 (복잡)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">계산 비용</div><div class="kb-diagram-cell">시퀀서 낮음</div><div class="kb-diagram-cell">증명 생성 비용 높음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">보안 모델</div><div class="kb-diagram-cell">최소 1명의 정직한 검증자</div><div class="kb-diagram-cell">암호학적 보안 (수학적)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">현재 TVL</div><div class="kb-diagram-cell">더 높음</div><div class="kb-diagram-cell">성장 중</div></div>
<div class="kb-diagram-note">Optimistic 롤업 주요 위험:</div>
<div class="kb-diagram-note">1. 시퀀서 검열: 시퀀서가 특정 트랜잭션 제외 가능</div>
<div class="kb-diagram-note">대응: L1 Force Include (이더리움으로 강제 포함)</div>
<div class="kb-diagram-note">2. 이의제기 활성화 가정: 아무도 감시 안 하면?</div>
<div class="kb-diagram-note">대응: Watchers (자동 감시 봇)</div>
<div class="kb-diagram-note">3. 7일 유동성 잠금:</div>
<div class="kb-diagram-note">대응: 브리지 유동성 공급자 (즉시 출금 + 수수료)</div>
<div class="kb-diagram-note">ZK 롤업 확산:</div>
<div class="kb-diagram-note">zkSync Era, Polygon zkEVM, Scroll, StarkNet</div>
<div class="kb-diagram-note">"ZK &gt; Optimistic" 장기 전망 (Vitalik)</div>
<div class="kb-diagram-note">하지만 단기: Optimistic 더 높은 TVL/활동성</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Optimistic vs ZK는 신용 대출 vs 담보 대출 — Optimistic은 일단 믿어줌(낙관적, 빠름), ZK는 담보 증명 필요(느리지만 확실). 장기 추세는 ZK로 이동 중.

---

## Ⅴ. 실무 시나리오 — Base 체인 [DApp](/knowledge-base/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/) 배포



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OP Stack 기반 Base 체인 DApp 배포:</div>
<div class="kb-diagram-note">Base 개요:</div>
<div class="kb-diagram-note">Coinbase 운영, OP Stack 기반</div>
<div class="kb-diagram-note">이더리움 L2, TVL ~$5B (2025)</div>
<div class="kb-diagram-note">수수료: 이더리움의 1/50~1/100 수준</div>
<div class="kb-diagram-note">DApp 배포 단계:</div>
<div class="kb-diagram-note">1. 계약 배포:</div>
<div class="kb-diagram-note">이더리움 mainnet 계약 → Base에 그대로 배포</div>
<div class="kb-diagram-note">(EVM 100% 호환)</div>
<div class="kb-diagram-note">forge deploy --rpc-url https://mainnet.base.org</div>
<div class="kb-diagram-note">2. 브리징:</div>
<div class="kb-diagram-note">ETH → Base ETH (7일 출금 지연)</div>
<div class="kb-diagram-note">또는 CEX(Coinbase) 직접 출금으로 즉시 획득</div>
<div class="kb-diagram-note">3. 사용자 경험:</div>
<div class="kb-diagram-note">가스비: ~$0.01~$0.10 (이더리움 $3~$50 대비)</div>
<div class="kb-diagram-note">처리량: ~2,000 TPS (이더리움 ~15 TPS)</div>
<div class="kb-diagram-note">EIP-4844 (Proto-Danksharding) 영향:</div>
<div class="kb-diagram-note">2024년 이더리움 업그레이드</div>
<div class="kb-diagram-note">Blob 데이터: calldata 대비 10~100배 저렴</div>
<div class="kb-diagram-note">→ Optimistic 롤업 수수료 추가 80~90% 감소</div>
<div class="kb-diagram-note">Base, Optimism, Arbitrum 모두 즉시 적용</div>
<div class="kb-diagram-note">결과: 평균 L2 거래 수수료 $0.001~$0.01 수준</div>
<div class="kb-diagram-note">미래: EIP-4844 → Full Danksharding</div>
<div class="kb-diagram-note">수백 개 Blob/블록 → 롤업 비용 거의 0</div>
<div class="kb-diagram-note">"롤업 중심의 이더리움 로드맵" 실현</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Base/OP Stack은 이더리움의 고속도로 톨게이트 절감 — 원래 1만 원 톨비(이더리움 [가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/))를 100원(L2)으로 줄여주는 빠른 우회 도로.

---

## 📌 관련 개념 맵

```
옵티미스틱 롤업
+-- 핵심 메커니즘
|   +-- 낙관적 가정 (사전 증명 없음)
|   +-- 7일 이의제기 기간
|   +-- 사기 증명 (Fraud Proof)
+-- 구현체
|   +-- Optimism / OP Stack
|   +-- Arbitrum (인터랙티브 이분 게임)
+-- 비교
|   +-- vs ZK 롤업 (암호학적 즉시 증명)
+-- 인프라
|   +-- EIP-4844 Blob 데이터
|   +-- Superchain (OP 생태계)
```

---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이더리움 확장성 문제 (2017~)</div></div>
<div class="kb-diagram-note">CryptoKitties로 네트워크 마비</div>
<div class="kb-diagram-note">가스비 급등, TPS 한계</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">롤업 제안 (2018~)</div></div>
<div class="kb-diagram-note">Plasma → 데이터 가용성 문제</div>
<div class="kb-diagram-note">Rollup 개념 등장 (Vitalik)</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Optimism 베타 출시 (2021)</div></div>
<div class="kb-diagram-note">Synthetix, Uniswap 이주</div>
<div class="kb-diagram-note">사기 증명 메커니즘 실전 검증</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Arbitrum One 출시 (2021)</div></div>
<div class="kb-diagram-note">인터랙티브 이분 게임 방식</div>
<div class="kb-diagram-note">더 낮은 가스비로 빠른 성장</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OP Stack 오픈소스 + Base 출시 (2023)</div></div>
<div class="kb-diagram-note">Superchain 생태계 형성</div>
<div class="kb-diagram-note">EIP-4844로 수수료 대폭 감소</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: ZK vs Optimistic 경쟁</div></div>
<div class="kb-diagram-note">ZK 기술 성숙 → 점진적 대체 가능성</div>
<div class="kb-diagram-note">단기: Optimistic이 높은 TVL/생태계 유지</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 "일단 믿어주는 빠른 계산기" — 수천 개 거래를 묶어서 이더리움에 제출하고, 7일 동안 아무도 문제 제기 안 하면 확정이에요!
2. 사기 증명은 법원 항소 — 계산이 틀렸다고 생각하면 증거를 들고 법원(스마트 계약)에 가면 돼요. 맞으면 보상, 틀리면 내 돈 몰수.
3. Base(Coinbase)가 이 방식으로 만들어져 이더리움보다 100배 저렴하게 거래할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 43 / 552

← **이전**: [042. 롤업 (Rollup) — Layer 2 트랜잭션 압축 기술](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)
**다음**: [044. ZK-Rollup & 유효성 증명](/knowledge-base/studynote/06_ict_convergence/01_blockchain/044_zk_rollup_validity_proof/) →

---
