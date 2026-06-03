+++
title = "047. 하드 포크 — Hard Fork & Chain Split"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

> **핵심 인사이트**
> 1. 하드 포크(Hard Fork)는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 프로토콜을 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 호환되지 않는 방식으로 업그레이드하는 것 — 과반수 노드가 새 규칙을 채택하지 않으면 체인이 영구 분리(Chain Split)되며, 이더리움 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 사건과 비트코인 캐시 분리가 대표적 실례다.
> 2. 소프트 포크 vs 하드 포크의 핵심 차이 — 소프트 포크는 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 노드가 새 블록을 유효하다고 판단(하위 호환), 하드 포크는 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 노드가 새 블록을 무효로 판단(비호환). 이더리움 PoS 전환(Merge)은 체인 분리 없는 하드 포크의 예다.
> 3. 체인 분리 시 리플레이 어택([Replay Attack](/knowledge-base/studynote/09_security/03_network_security/274_replay_attack/))이 새로운 보안 위협 — 한 체인의 서명된 트랜잭션이 다른 체인에도 유효해 의도치 않은 자산 이동이 발생하며, 체인 ID 분리와 리플레이 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 구현이 필수다.

---

## Ⅰ. 하드 포크 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">포크 유형:</div>
<div class="kb-diagram-note">소프트 포크 (Soft Fork):</div>
<div class="kb-diagram-note">새 규칙 ⊂ 이전 규칙 (더 엄격한 규칙)</div>
<div class="kb-diagram-note">이전 노드: 새 블록을 유효하다고 판단 (OK)</div>
<div class="kb-diagram-note">새 노드: 이전 블록을 무효로 판단</div>
<div class="kb-diagram-note">예: SegWit (Bitcoin, 2017)</div>
<div class="kb-diagram-note">이전 노드: SegWit 트랜잭션을 "아무 사람이나 쓸 수 있는 출력"으로 봄 (유효)</div>
<div class="kb-diagram-note">새 노드: 위트니스 서명 검증</div>
<div class="kb-diagram-note">체인 분리 없음 (과반수 지지 시)</div>
<div class="kb-diagram-note">하드 포크 (Hard Fork):</div>
<div class="kb-diagram-note">새 규칙 ≠ 이전 규칙 (비호환 변경)</div>
<div class="kb-diagram-note">이전 노드: 새 블록을 무효로 판단 (거부)</div>
<div class="kb-diagram-note">새 노드: 이전 블록을 무효로 판단</div>
<div class="kb-diagram-note">과반수 미달 → 두 체인 영구 공존</div>
<div class="kb-diagram-note">하드 포크 유형:</div>
<div class="kb-diagram-note">1. 합의 하드 포크 (Consensual):</div>
<div class="kb-diagram-note">커뮤니티 전체 동의 → 모두 업그레이드</div>
<div class="kb-diagram-note">이전 체인 사실상 소멸</div>
<div class="kb-diagram-note">예: 이더리움 Merge (PoW→PoS)</div>
<div class="kb-diagram-note">모든 노드 동의 → 단일 체인</div>
<div class="kb-diagram-note">2. 논쟁 하드 포크 (Contentious):</div>
<div class="kb-diagram-note">커뮤니티 분열 → 체인 분리</div>
<div class="kb-diagram-note">예: 비트코인 캐시 (BCH, 2017)</div>
<div class="kb-diagram-note">비트코인에서 분리</div>
<div class="kb-diagram-note">두 체인 독립 유지</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 하드 포크는 교통법 개정 — 소프트 포크는 "더 좁은 도로에서도 달릴 수 있어요"(모든 차 호환), 하드 포크는 "전혀 다른 도로 규칙"(구형 차 못 달림). 도로가 갈라지면 체인 분리!

---

## Ⅱ. 주요 하드 포크 사례



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">역사적 하드 포크 사례:</div>
<div class="kb-diagram-note">1. 이더리움 DAO 해킹 사건 (2016):</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">DAO(탈중앙 자율 조직) 3.6억 달러 해킹</div>
<div class="kb-diagram-note">커뮤니티 결정:</div>
<div class="kb-diagram-note">"블록체인 불변성 vs 피해 복구"</div>
<div class="kb-diagram-note">하드 포크 찬성파 (ETH):</div>
<div class="kb-diagram-note">특정 블록에서 해킹 트랜잭션 되돌리기</div>
<div class="kb-diagram-note">→ 오늘날 이더리움 (ETH)</div>
<div class="kb-diagram-note">하드 포크 반대파 (ETC):</div>
<div class="kb-diagram-note">"블록체인은 불변이어야"</div>
<div class="kb-diagram-note">→ 이더리움 클래식 (ETC, 포크 전 체인)</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">ETH: 현재 시총 2위 (대부분 채택)</div>
<div class="kb-diagram-note">ETC: 소수 유지</div>
<div class="kb-diagram-note">2. 비트코인 캐시 (BCH, 2017):</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">비트코인 확장성 논쟁</div>
<div class="kb-diagram-note">"블록 크기 1MB → 8MB"</div>
<div class="kb-diagram-note">찬성: 대형 블록으로 TPS 향상</div>
<div class="kb-diagram-note">반대: "탈중앙화 저해"</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">BTC: 1MB 유지 (SegWit 채택)</div>
<div class="kb-diagram-note">BCH: 8MB 분리 → 이후 BSV 재분리</div>
<div class="kb-diagram-note">3. 이더리움 Merge (2022):</div>
<div class="kb-diagram-note">PoW → PoS 전환</div>
<div class="kb-diagram-note">합의 하드 포크 (전체 동의)</div>
<div class="kb-diagram-note">ETHPOW: 소수 PoW 유지 체인 (시장 외면)</div>
<div class="kb-diagram-note">4. 이더리움 콘스탄티노플, 베를린, 런던 등:</div>
<div class="kb-diagram-note">EIP 묶음 업그레이드</div>
<div class="kb-diagram-note">커뮤니티 합의 하드 포크</div>
<div class="kb-diagram-note">(이전 체인 소멸, 단일 체인 유지)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/) vs ETC는 도시 분열 — 해킹 사건 후 "피해 보상해야([ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/))" vs "원칙 지켜야(ETC)" 의견 충돌. 도시가 둘로 분리, 각자의 법으로 독립!

---

## Ⅲ. 리플레이 어택



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">리플레이 어택 (Replay Attack):</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">체인 분리 직후: A체인 = B체인 (동일 기록 공유)</div>
<div class="kb-diagram-note">A체인 트랜잭션이 B체인에도 유효!</div>
<div class="kb-diagram-note">시나리오:</div>
<div class="kb-diagram-note">A(ETH): Alice → Bob 10 ETH 서명 전송</div>
<div class="kb-diagram-note">B(ETC): 동일 서명을 ETC 네트워크에 브로드캐스트</div>
<div class="kb-diagram-note">→ Alice의 ETC도 Bob에게 이동! (의도 없이)</div>
<div class="kb-diagram-note">발생 조건:</div>
<div class="kb-diagram-note">두 체인이 동일한 개인키, 주소 체계</div>
<div class="kb-diagram-note">체인 분리 전 트랜잭션 형식 동일</div>
<div class="kb-diagram-note">해결 방법:</div>
<div class="kb-diagram-note">1. 체인 ID 분리 (EIP-155):</div>
<div class="kb-diagram-note">트랜잭션에 체인 고유 ID 포함</div>
<div class="kb-diagram-note">ETH: chainId = 1</div>
<div class="kb-diagram-note">ETC: chainId = 61</div>
<div class="kb-diagram-note">BSC: chainId = 56</div>
<div class="kb-diagram-note">서명 = ECDSA(txData + chainId)</div>
<div class="kb-diagram-note">→ 다른 체인에서 서명 무효</div>
<div class="kb-diagram-note">2. 리플레이 보호 (Replay Protection):</div>
<div class="kb-diagram-note">새 블록에 고유 코인베이스 데이터 추가</div>
<div class="kb-diagram-note">또는 특정 OP코드 추가</div>
<div class="kb-diagram-note">3. 사용자 주의:</div>
<div class="kb-diagram-note">체인 분리 직후 일정 기간 대기</div>
<div class="kb-diagram-note">각 체인에서 별도 트랜잭션 발행 후 사용</div>
<div class="kb-diagram-note">이더리움 ETC 분리 시:</div>
<div class="kb-diagram-note">EIP-155 없었음 → 초기 리플레이 공격 발생</div>
<div class="kb-diagram-note">이후 양 체인 모두 chainId 추가로 해결</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 리플레이 어택은 복사 영수증 — "A 가게 영수증"을 "B 가게"에 그대로 내밀어 환불 요청. 두 가게가 같은 규칙이면 통해요! 체인 ID는 가게 도장(구별자)!

---

## Ⅳ. 포크와 거버넌스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">블록체인 거버넌스 (Governance):</div>
<div class="kb-diagram-note">누가 하드 포크를 결정하나?</div>
<div class="kb-diagram-note">비트코인 거버넌스:</div>
<div class="kb-diagram-note">BIP (Bitcoin Improvement Proposal)</div>
<div class="kb-diagram-note">코어 개발자 + 채굴자 + 사용자 비공식 합의</div>
<div class="kb-diagram-note">BIP 상태:</div>
<div class="kb-diagram-note">Draft → Accepted → Final/Rejected</div>
<div class="kb-diagram-note">채굴자 신호: "이 업그레이드 지지"</div>
<div class="kb-diagram-note">임계값(예: 95%) 달성 → 활성화</div>
<div class="kb-diagram-note">이더리움 거버넌스:</div>
<div class="kb-diagram-note">EIP (Ethereum Improvement Proposal)</div>
<div class="kb-diagram-note">이더리움 재단 + 클라이언트 팀 + 커뮤니티</div>
<div class="kb-diagram-note">EIP 과정:</div>
<div class="kb-diagram-note">Draft → Review → Last Call → Final</div>
<div class="kb-diagram-note">핵심 EIP: 하드 포크 포함 여부 결정</div>
<div class="kb-diagram-note">DAO 기반 거버넌스 (DeFi):</div>
<div class="kb-diagram-note">Compound, Uniswap:</div>
<div class="kb-diagram-note">토큰 보유자 → 온체인 투표</div>
<div class="kb-diagram-note">→ 프로토콜 업그레이드 결정</div>
<div class="kb-diagram-note">장점: 투명, 탈중앙</div>
<div class="kb-diagram-note">단점: 토큰 집중 → 실질적 중앙화</div>
<div class="kb-diagram-note">고래(Whale)가 과반수 토큰 보유 시 독점</div>
<div class="kb-diagram-note">Polkadot 거버넌스:</div>
<div class="kb-diagram-note">온체인 국민투표 시스템</div>
<div class="kb-diagram-note">DOT 보유량 기반 투표권</div>
<div class="kb-diagram-note">기술위원회(Technical Committee)</div>
<div class="kb-diagram-note">→ 빠른 업그레이드 가능</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 거버넌스는 마을 회의 — 비트코인은 개발자+채굴자 비공식 합의(마을 원로 회의), 이더리움은 EIP 공식 과정, DeFi는 토큰 투표(주주총회). 모두 민주적이지만 방식이 달라요!

---

## Ⅴ. 실무 시나리오 — 하드 포크 대응



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">거래소의 하드 포크 대응 전략:</div>
<div class="kb-diagram-note">상황:</div>
<div class="kb-diagram-note">주요 블록체인 하드 포크 예정 (30일 후)</div>
<div class="kb-diagram-note">거래소: 10개 블록체인 지원</div>
<div class="kb-diagram-note">이번 포크: 비트코인 X체인 논쟁 포크</div>
<div class="kb-diagram-note">X체인 → XA체인 + XB체인 분리 예정</div>
<div class="kb-diagram-note">대응 계획:</div>
<div class="kb-diagram-note">30일 전:</div>
<div class="kb-diagram-note">포크 공지: 사용자에게 날짜/방식 안내</div>
<div class="kb-diagram-note">노드 모니터링 팀 구성</div>
<div class="kb-diagram-note">포크 당일 - 3시간 전:</div>
<div class="kb-diagram-note">XA, XB 입출금 일시 중단</div>
<div class="kb-diagram-note">(혼선 방지)</div>
<div class="kb-diagram-note">체인 분리 확인:</div>
<div class="kb-diagram-note">두 체인 독립 실행 확인</div>
<div class="kb-diagram-note">리플레이 보호 구현 여부 확인</div>
<div class="kb-diagram-note">포크 후 24~48시간:</div>
<div class="kb-diagram-note">두 체인 안정성 모니터링</div>
<div class="kb-diagram-note">XA 블록 생성 정상 여부</div>
<div class="kb-diagram-note">XB 블록 생성 정상 여부</div>
<div class="kb-diagram-note">리플레이 보호 없을 경우:</div>
<div class="kb-diagram-note">XA 자산 처리 시 먼저 분리 트랜잭션 발행</div>
<div class="kb-diagram-note">이후 각 체인 독립 운영</div>
<div class="kb-diagram-note">사용자 지원:</div>
<div class="kb-diagram-note">XA 보유자 → XA + XB 동일 수량 에어드롭</div>
<div class="kb-diagram-note">(체인 분리 시점 스냅샷 기준)</div>
<div class="kb-diagram-note">XB 지원 결정:</div>
<div class="kb-diagram-note">시장 지지도 확인 (거래량, 개발 활동)</div>
<div class="kb-diagram-note">상장 여부 결정 (최소 활성 기준)</div>
<div class="kb-diagram-note">결론:</div>
<div class="kb-diagram-note">거래소는 안전을 위해 일시 중단</div>
<div class="kb-diagram-note">사용자 자산 보호 최우선</div>
<div class="kb-diagram-note">충분한 확인 후 서비스 재개</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 거래소 포크 대응은 도시 분열 대비 — 도시가 둘로 나뉘기 전에 "잠깐 통행 멈춤(입출금 중단)". 도시가 안정되면 두 도시 모두 열쇠(자산) 지급!

---

## 📌 관련 개념 맵

```
하드 포크
+-- 유형
|   +-- 합의 포크 (Consensual)
|   +-- 논쟁 포크 (Contentious)
+-- 사례
|   +-- ETH vs ETC (DAO)
|   +-- BTC vs BCH (블록 크기)
|   +-- ETH Merge (PoW→PoS)
+-- 보안 이슈
|   +-- 리플레이 어택
|   +-- EIP-155 (체인 ID)
+-- 거버넌스
    +-- BIP (비트코인)
    +-- EIP (이더리움)
    +-- 온체인 투표 (DeFi)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[비트코인 초기 포크 (2011~)]
소규모 버그 수정 포크
커뮤니티 분열 시작
      |
      v
[이더리움 DAO 포크 (2016)]
최초 논쟁 체인 분리
ETH vs ETC 탄생
      |
      v
[BCH 분리 (2017)]
비트코인 확장성 전쟁
포크 투자 투기 붐
      |
      v
[이더리움 업그레이드 시대 (2019~)]
연속 하드 포크
EIP-1559 (수수료 개혁)
      |
      v
[Merge + 거버넌스 성숙 (2022~)]
PoS 전환 성공
온체인 거버넌스 확산
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 하드 포크는 나라 분열 — 마을([블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)) 규칙을 바꾸는데 모두 동의 안 하면? 마을이 둘로 갈라져요. [ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/) vs ETC가 그 예!
2. 리플레이 어택은 복사 도장 — 한 마을 영수증을 다른 마을에 그대로 내밀어 물건 받기. 체인 ID(마을 도장)로 구별해서 방지!
3. 거버넌스는 마을 회의 — BIP/EIP로 제안하고 투표. 과반수 동의하면 규칙 변경. 동의 안 하면 분열(논쟁 포크) 위험!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 47 / 552

← **이전**: [046. 블록체인 샤딩 — Blockchain Sharding](/knowledge-base/studynote/06_ict_convergence/01_blockchain/046_sharding_parallel_processing/)
**다음**: [048. 소프트 포크 — Soft Fork & 하위 호환성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/048_soft_fork_backward_compatibility/) →

---
