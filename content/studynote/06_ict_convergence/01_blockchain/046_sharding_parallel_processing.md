+++
title = "046. 블록체인 샤딩 — Blockchain Sharding"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

> **핵심 인사이트**
> 1. [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)([Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))은 네트워크를 여러 샤드(Shard)로 분할해 각 샤드가 독립적으로 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 처리하는 수평 확장 기법 — 비트코인/이더리움이 모든 노드가 모든 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 구조의 TPS 한계를 돌파하기 위해 도입한다.
> 2. [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/)(Trilemma)와 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) — [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/)·보안·확장성 세 가지를 동시에 완벽히 달성하기 어렵다는 Vitalik의 트릴레마에서, [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 확장성을 높이지만 단일 샤드 공격(1% 공격)·크로스샤드 통신 비용이라는 새 도전을 만든다.
> 3. Ethereum의 Danksharding(2024~)은 실행 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 대신 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) — [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 실행은 L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이 담당하고, 이더리움은 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이어" 역할에 집중하는 설계 방향이다.

---

## Ⅰ. [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 확장성 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">블록체인 TPS 한계:</div>
<div class="kb-diagram-note">비트코인: ~7 TPS (블록크기 1MB, 10분 블록)</div>
<div class="kb-diagram-note">이더리움: ~15 TPS (가스 한도, 12초 블록)</div>
<div class="kb-diagram-note">VISA: 24,000 TPS (평균)</div>
<div class="kb-diagram-note">65,000+ TPS (피크)</div>
<div class="kb-diagram-note">확장성 제약 원인:</div>
<div class="kb-diagram-note">전체 노드 검증:</div>
<div class="kb-diagram-note">모든 풀노드 → 모든 트랜잭션 검증</div>
<div class="kb-diagram-note">→ 전체 네트워크 용량 = 가장 느린 노드 속도</div>
<div class="kb-diagram-note">트릴레마 (Trilemma):</div>
<div class="kb-diagram-note">탈중앙화 (Decentralization)</div>
<div class="kb-diagram-note">보안 (Security)</div>
<div class="kb-diagram-note">확장성 (Scalability)</div>
<div class="kb-diagram-note">→ 셋 중 둘만 달성 가능?</div>
<div class="kb-diagram-note">비트코인: 탈중앙화 + 보안 (확장성 희생)</div>
<div class="kb-diagram-note">EOS: 보안 + 확장성 (21개 BP로 탈중앙화 희생)</div>
<div class="kb-diagram-note">확장 솔루션:</div>
<div class="kb-diagram-note">L1 (온체인):</div>
<div class="kb-diagram-tree-item" style="--depth:1">블록크기 증가 (BSV, BCH)</div>
<div class="kb-diagram-tree-item" style="--depth:1">샤딩 (Ethereum 계획)</div>
<div class="kb-diagram-tree-item" style="--depth:1">합의 알고리즘 변경 (PoS)</div>
<div class="kb-diagram-note">L2 (오프체인):</div>
<div class="kb-diagram-tree-item" style="--depth:1">롤업 (Arbitrum, Optimism)</div>
<div class="kb-diagram-tree-item" style="--depth:1">페이먼트 채널 (Lightning Network)</div>
<div class="kb-diagram-tree-item" style="--depth:1">사이드체인 (Polygon)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 확장성 문제는 단일 계산원 — 슈퍼마켓에 계산원 1명(모든 노드 동일 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)), 줄이 길어도 더 빠른 계산원을 쓸 수 없어요. [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 계산대 여러 개 열기!

---

## Ⅱ. [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">블록체인 샤딩 구조:</div>
<div class="kb-diagram-note">네트워크 분할:</div>
<div class="kb-diagram-note">전체 네트워크 (N개 노드)</div>
<div class="kb-diagram-note">↓ K개 샤드로 분할</div>
<div class="kb-diagram-note">샤드 1: 노드 1~N/K, 트랜잭션 A-F</div>
<div class="kb-diagram-note">샤드 2: 노드 N/K+1~2N/K, 트랜잭션 G-M</div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">샤드 K: 마지막 노드들, 트랜잭션 ...</div>
<div class="kb-diagram-note">각 샤드: 독립 합의, 독립 블록 생성</div>
<div class="kb-diagram-note">→ 병렬 처리 → TPS × K</div>
<div class="kb-diagram-note">샤딩 유형:</div>
<div class="kb-diagram-note">1. 네트워크 샤딩 (Network Sharding):</div>
<div class="kb-diagram-note">노드를 샤드로 분할</div>
<div class="kb-diagram-note">→ 각 샤드만 통신</div>
<div class="kb-diagram-note">2. 트랜잭션 샤딩 (Transaction Sharding):</div>
<div class="kb-diagram-note">트랜잭션을 샤드로 배분</div>
<div class="kb-diagram-note">동일 계정의 TX → 동일 샤드</div>
<div class="kb-diagram-note">3. 상태 샤딩 (State Sharding):</div>
<div class="kb-diagram-note">블록체인 상태(계정 잔액 등)를 분할</div>
<div class="kb-diagram-note">각 샤드가 일부 상태만 보유</div>
<div class="kb-diagram-note">→ 가장 어렵지만 가장 효과적</div>
<div class="kb-diagram-note">크로스 샤드 통신 (Cross-Shard):</div>
<div class="kb-diagram-note">샤드 A의 Alice → 샤드 B의 Bob 전송</div>
<div class="kb-diagram-note">문제: 서로 다른 샤드 = 서로 다른 합의</div>
<div class="kb-diagram-note">해결 방법:</div>
<div class="kb-diagram-note">1. 2단계 커밋 (2-Phase Commit):</div>
<div class="kb-diagram-note">잠금 → 커밋 (느림)</div>
<div class="kb-diagram-note">2. 영수증 기반 (Receipt-Based):</div>
<div class="kb-diagram-note">샤드 A: 소각 영수증 생성</div>
<div class="kb-diagram-note">샤드 B: 영수증 확인 후 발행</div>
<div class="kb-diagram-note">→ Ethereum 초기 샤딩 계획</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 은행 지점 분리 — 전국 거래를 본점(단일 체인) 하나에서 처리하다가, 지역별 지점(샤드)이 독립적으로 처리. 지점 간 송금(크로스샤드)만 복잡!

---

## Ⅲ. 1% 공격과 보안



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">샤딩의 보안 위험: 1% 공격</div>
<div class="kb-diagram-note">단일 체인:</div>
<div class="kb-diagram-note">공격자 51% 해시파워 필요</div>
<div class="kb-diagram-note">전체 네트워크의 51%</div>
<div class="kb-diagram-note">샤딩 (10개 샤드):</div>
<div class="kb-diagram-note">단일 샤드 공격: 샤드 검증자의 51% 필요</div>
<div class="kb-diagram-note">전체 네트워크의 51%/10 = 5.1%</div>
<div class="kb-diagram-note">→ 공격 비용 10× 감소!</div>
<div class="kb-diagram-note">완화 방법:</div>
<div class="kb-diagram-note">1. 랜덤 샤드 배정 (Random Shuffling):</div>
<div class="kb-diagram-note">검증자를 주기적으로 무작위로 샤드 재배정</div>
<div class="kb-diagram-note">VDF (Verifiable Delay Function):</div>
<div class="kb-diagram-note">조작 불가능한 랜덤성 생성 (Ethereum 사용)</div>
<div class="kb-diagram-note">재배정 빈도 ↑ → 보안 ↑ but 오버헤드 ↑</div>
<div class="kb-diagram-note">2. 충분한 샤드 크기:</div>
<div class="kb-diagram-note">샤드당 최소 검증자 수 유지</div>
<div class="kb-diagram-note">Ethereum 목표: 샤드당 128명 검증자</div>
<div class="kb-diagram-note">→ 통계적으로 1% 공격 현실적 불가</div>
<div class="kb-diagram-note">3. 크로스링크 (Crosslink):</div>
<div class="kb-diagram-note">비콘 체인이 각 샤드 상태 주기적 확인</div>
<div class="kb-diagram-note">→ 샤드 조작 탐지</div>
<div class="kb-diagram-note">Ethereum 2.0 (PoS + 샤딩):</div>
<div class="kb-diagram-note">PoS 검증자: 스테이킹 32 ETH</div>
<div class="kb-diagram-note">랜덤 위원회(Committee)로 샤드 배정</div>
<div class="kb-diagram-note">에포크(32 슬롯)마다 재배정</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 1% 공격은 작은 분대 점령 — 전군(전체 체인) 공격은 어려운데, 소부대(샤드) 하나 점령하면 그 샤드 독점. 랜덤 배치(셔플)로 어느 부대에 적이 올지 모르게!

---

## Ⅳ. Danksharding (Ethereum)

```
Ethereum 샤딩 로드맵 변화:

초기 계획 (2018~2021):
  실행 샤딩: 64개 샤드 × 독립 스마트컨트랙트
  크로스샤드 통신 복잡 문제

방향 전환 (2021~):
  "롤업 중심" 전략 발표 (Vitalik)
  
  L2 롤업이 실행 담당
  이더리움 = 데이터 가용성 + 합의

Proto-Danksharding (EIP-4844, 2024.03):
  Blob Transaction 도입
  
  Blob: 임시 데이터 저장 (L2 롤업 데이터)
  크기: 블롭당 ~128 KB
  유지 기간: ~18일 후 자동 삭제
  
  효과:
  롤업 L2 수수료: 10~100× 감소
  (calldata 대비 저렴한 blob 공간)
  
  Cancun 업그레이드로 실제 구현됨

Full Danksharding (미래):
  64개 Blob/블록 (현재 Proto-DAS: 6개)
  PeerDAS: 분산 데이터 가용성 샘플링
  
  최종 목표:
  이더리움: ~16 MB/s 데이터 처리
  L2 TPS 수백만 가능 (롤업 통합)

KZG 약속 (KZG Commitments):
  Blob 데이터 검증 수학적 기법
  모든 노드가 블롭 전체 다운로드 없이
  일부 샘플링으로 가용성 확인 (DAS)
```

> 📢 **섹션 요약 비유**: Danksharding은 창고(이더리움)→배송 네트워크 전환 — 이더리움이 직접 배달(실행) 대신, 배달부(L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)) 위탁 + 창고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장)만 집중. 효율 폭발!

---

## Ⅴ. 실무 시나리오 — Zilliqa [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Zilliqa — 퍼블릭 블록체인 샤딩 구현:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">2018년 메인넷 출시</div>
<div class="kb-diagram-note">업계 최초 실용 샤딩 블록체인</div>
<div class="kb-diagram-note">아키텍처:</div>
<div class="kb-diagram-note">DS Committee (Directory Service):</div>
<div class="kb-diagram-note">→ 새 에포크마다 샤드 구성 결정</div>
<div class="kb-diagram-note">→ PoW로 DS 위원회 선정</div>
<div class="kb-diagram-note">샤드 노드:</div>
<div class="kb-diagram-note">트랜잭션 샤딩 처리</div>
<div class="kb-diagram-note">PBFT 합의 (샤드 내)</div>
<div class="kb-diagram-note">크로스샤드 처리:</div>
<div class="kb-diagram-note">DS Committee 최종 합병</div>
<div class="kb-diagram-note">성능:</div>
<div class="kb-diagram-note">2,400개 노드 기준:</div>
<div class="kb-diagram-note">샤드 4개 → TPS 2,828</div>
<div class="kb-diagram-note">샤드 6개 → TPS ~2,488 (일부 오버헤드)</div>
<div class="kb-diagram-note">이론: 샤드 × 500 TPS</div>
<div class="kb-diagram-note">한계:</div>
<div class="kb-diagram-note">상태 샤딩 미구현 (트랜잭션 샤딩만)</div>
<div class="kb-diagram-note">크로스샤드 스마트컨트랙트 제약</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">샤딩은 기술적으로 가능하지만 복잡</div>
<div class="kb-diagram-note">크로스샤드 통신이 주요 병목</div>
<div class="kb-diagram-note">Ethereum의 전략 전환(롤업+DAS)이 현실적</div>
<div class="kb-diagram-note">현재:</div>
<div class="kb-diagram-note">ZIL: DeFi, 게임 용도</div>
<div class="kb-diagram-note">Ethereum L2 롤업 + Danksharding이 주류 흐름</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Zilliqa [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 최초 실험실 — 이론을 실제로 구현한 선구자. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)으로 TPS 향상. Ethereum은 이 실험을 참고해 더 실용적인 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)+DAS로 진화!

---

## 📌 관련 개념 맵

```
블록체인 샤딩
+-- 유형
|   +-- 네트워크 샤딩
|   +-- 트랜잭션 샤딩
|   +-- 상태 샤딩 (가장 어려움)
+-- 보안
|   +-- 1% 공격 취약성
|   +-- 랜덤 검증자 배정 (VDF)
+-- Ethereum 로드맵
|   +-- Proto-Danksharding (EIP-4844)
|   +-- Full Danksharding (미래)
|   +-- Blob Transaction
+-- 구현 사례
    +-- Zilliqa
    +-- Near Protocol (Nightshade)
    +-- Harmony
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[블록체인 확장성 문제 부각 (2017)]
CryptoKitties → 이더리움 네트워크 마비
TPS 한계 주목
      |
      v
[샤딩 연구 (2017~2019)]
Ethereum 샤딩 백서
Zilliqa 메인넷 (2018)
      |
      v
[롤업 전략 전환 (2021)]
Vitalik: 롤업 중심 L2
이더리움 = DA 레이어
      |
      v
[Proto-Danksharding (2024.03)]
EIP-4844, Blob TX
롤업 수수료 10~100× 감소
      |
      v
[Full Danksharding (미래)]
PeerDAS, 1,600만 TPS (L2 포함)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 계산대 여러 개 — 슈퍼마켓에 계산원 1명(단일 체인) → 계산대 10개(10개 샤드)로 동시에 계산. TPS 10배!
2. 1% 공격 위험 — 소규모 그룹(샤드)은 더 쉽게 공격당해요. 주기적 랜덤 배치(셔플)로 공격자가 누구와 한 팀인지 모르게!
3. Ethereum의 선택 — 직접 실행 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 대신, L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이 실행하고 이더리움은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장만. Blob [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 수수료 100배 절감!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 46 / 552

← **이전**: [045. 사이드체인과 브릿지 — Sidechain & Bridge (Polygon)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/045_sidechain_bridge_polygon/)
**다음**: [047. 하드 포크 — Hard Fork & Chain Split](/knowledge-base/studynote/06_ict_convergence/01_blockchain/047_hard_fork_chain_split/) →

---
