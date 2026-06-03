+++
title = "048. 일관 해싱 — Consistent Hashing & Ring"
date = 2026-04-05

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

> **핵심 인사이트**
> 1. 일관 해싱([Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/))은 노드 추가/제거 시 최소한의 키 재배치만 발생하도록 설계된 해싱 기법 — 전통적인 모듈러 해싱([key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) % N)은 노드 수 N이 변하면 거의 모든 키를 재매핑해야 하지만, 일관 해싱은 (K/N)개의 키만 이동한다.
> 2. 링(Ring) 구조 + 가상 노드(Virtual Node)의 조합이 핵심 — 0~2^32 범위의 원형 해시 공간에 노드를 배치하고, 가상 노드를 통해 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 달성하는 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·[DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/)·[Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster의 근간이다.
> 3. 핫 스팟(Hot Spot) 문제 해결이 실제 구현의 핵심 과제 — 이론적 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)과 달리 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 접근 패턴이 불균등하여, 가상 노드 수 조정과 키 설계가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 성능을 결정한다.

---

## Ⅰ. 전통 해싱의 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전통 모듈러 해싱:</div>
<div class="kb-diagram-note">서버 3대: node_id = hash(key) % 3</div>
<div class="kb-diagram-note">key "user_123" → hash = 1000 → 1000 % 3 = 1 → 노드 1</div>
<div class="kb-diagram-note">key "order_456" → hash = 2001 → 2001 % 3 = 0 → 노드 0</div>
<div class="kb-diagram-note">서버 추가 (4대로):</div>
<div class="kb-diagram-note">node_id = hash(key) % 4 (기준이 3→4로 변경!)</div>
<div class="kb-diagram-note">"user_123" → 1000 % 4 = 0 → 노드 0 (기존 노드 1 ≠)</div>
<div class="kb-diagram-note">"order_456" → 2001 % 4 = 1 → 노드 1 (기존 노드 0 ≠)</div>
<div class="kb-diagram-note">거의 모든 키의 위치가 변함!</div>
<div class="kb-diagram-note">→ 대규모 캐시 미스 (Cache Storm)</div>
<div class="kb-diagram-note">→ 데이터베이스에 갑작스러운 부하 폭증</div>
<div class="kb-diagram-note">문제 규모:</div>
<div class="kb-diagram-note">노드 N → N+1 추가:</div>
<div class="kb-diagram-note">재배치 비율 = N/(N+1) ≈ 100% (대부분 재배치)</div>
<div class="kb-diagram-note">10만 키 분산 시스템에 노드 추가:</div>
<div class="kb-diagram-note">→ ~9만 키가 새 노드로 이동</div>
<div class="kb-diagram-note">→ 네트워크 + I/O + 다운타임 위험</div>
<div class="kb-diagram-note">일관 해싱의 목표:</div>
<div class="kb-diagram-note">노드 추가/제거 시 최소 이동 = K/N</div>
<div class="kb-diagram-note">(K: 전체 키 수, N: 노드 수)</div>
<div class="kb-diagram-note">예: 10만 키, 10노드 → 1만 키만 이동</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 전통 해싱 문제 = 사물함 번호 규칙 변경 — 사물함 10개일 때 학번 % [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 사물함 11개 추가 시 학번 % 11로 변경 → 90%가 새 사물함으로 이사. 일관 해싱은 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%만 이사!

---

## Ⅱ. 일관 해싱 링 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">일관 해싱 링:</div>
<div class="kb-diagram-note">1. 해시 공간을 원형(Ring)으로 구성:</div>
<div class="kb-diagram-note">0 2^32-1</div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">(원형: 2^32-1 다음이 0)</div>
<div class="kb-diagram-note">2. 노드를 링 위에 배치:</div>
<div class="kb-diagram-note">hash("node_A") = 10 → 링의 10 위치</div>
<div class="kb-diagram-note">hash("node_B") = 25 → 링의 25 위치</div>
<div class="kb-diagram-note">hash("node_C") = 40 → 링의 40 위치</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">링: 0..10</div><div class="kb-diagram-node">A</div><div class="kb-diagram-note">..25</div><div class="kb-diagram-node">B</div><div class="kb-diagram-note">..40</div><div class="kb-diagram-node">C</div><div class="kb-diagram-note">..2^32</div></div>
<div class="kb-diagram-note">3. 키를 시계 방향으로 첫 노드에 배치:</div>
<div class="kb-diagram-note">hash("user_1") = 15 → 시계 방향 첫 노드: B(25)</div>
<div class="kb-diagram-note">hash("user_2") = 5 → 시계 방향 첫 노드: A(10)</div>
<div class="kb-diagram-note">hash("user_3") = 30 → 시계 방향 첫 노드: C(40)</div>
<div class="kb-diagram-note">4. 노드 D 추가 (링의 20 위치):</div>
<div class="kb-diagram-note">hash("node_D") = 20 → 링의 20 위치</div>
<div class="kb-diagram-note">A(10)..D(20)..B(25)..C(40)</div>
<div class="kb-diagram-note">재배치:</div>
<div class="kb-diagram-note">A~D(10~20) 사이 키만 A→D로 이동</div>
<div class="kb-diagram-note">나머지 키: 그대로!</div>
<div class="kb-diagram-note">이동량: 전체 키의 약 1/노드수 (K/N)</div>
<div class="kb-diagram-note">5. 노드 B 제거 (링의 25 위치):</div>
<div class="kb-diagram-note">B(25) 제거</div>
<div class="kb-diagram-note">A(10)..D(20)..C(40)</div>
<div class="kb-diagram-note">재배치:</div>
<div class="kb-diagram-note">D~B(20~25) 사이 키만 B→C로 이동</div>
<div class="kb-diagram-note">나머지: 그대로!</div>
<div class="kb-diagram-note">이진 탐색으로 노드 찾기:</div>
<div class="kb-diagram-note">노드 목록을 정렬 배열로 유지</div>
<div class="kb-diagram-note">bisect_right(sorted_nodes, hash(key))</div>
<div class="kb-diagram-note">→ O(log N) 탐색</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 일관 해싱 링 = 원형 시계 사물함 배치 — 학생(키)이 자기 번호 위치에서 시계 방향으로 가장 가까운 사물함(노드) 이용. 사물함 추가 시 그 구간 학생만 이사!

---

## Ⅲ. 가상 노드 (Virtual Nodes)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">가상 노드 (VNode, Virtual Node):</div>
<div class="kb-diagram-note">실제 노드 하나가 링 위에 여러 위치를 점유</div>
<div class="kb-diagram-note">문제: 균등 분산 실패</div>
<div class="kb-diagram-note">3개 노드: A(10), B(25), C(40)</div>
<div class="kb-diagram-note">A 담당: 0~10 (구간 10)</div>
<div class="kb-diagram-note">B 담당: 11~25 (구간 15)</div>
<div class="kb-diagram-note">C 담당: 26~40 + 41~max + 0~... (구간 나머지)</div>
<div class="kb-diagram-note">→ 불균등! C가 훨씬 많은 키 담당</div>
<div class="kb-diagram-note">가상 노드 해결:</div>
<div class="kb-diagram-note">각 물리 노드 → K개 가상 노드</div>
<div class="kb-diagram-note">노드 A → A_1(3), A_2(20), A_3(45), A_4(70), ...</div>
<div class="kb-diagram-note">노드 B → B_1(8), B_2(27), B_3(55), B_4(80), ...</div>
<div class="kb-diagram-note">노드 C → C_1(15), C_2(35), C_3(60), C_4(90), ...</div>
<div class="kb-diagram-note">링: 0..A_1(3)..B_1(8)..A_2(20)..B_2(27)..A_3(45)..B_3(55)...</div>
<div class="kb-diagram-note">→ 각 물리 노드가 링 전체에 고르게 분산</div>
<div class="kb-diagram-note">→ 균등 분산 달성</div>
<div class="kb-diagram-note">적정 가상 노드 수:</div>
<div class="kb-diagram-note">Cassandra: 각 노드 기본 256개 VNode</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">균등 분산 (통계적)</div>
<div class="kb-diagram-note">노드 추가/제거 시 더 고른 부하 분산</div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-note">메타데이터 증가 (링 정보가 커짐)</div>
<div class="kb-diagram-note">토큰 관리 복잡</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 가상 노드 = 순환 근무 배치 — 직원 3명(A,B,C)이 12시간 중 8시간씩 겹치면 불균등. 대신 4교대(가상 노드)로 나눠 배치하면 균등하게 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)!

---

## Ⅳ. 실제 시스템 적용



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Cassandra 일관 해싱:</div>
<div class="kb-diagram-note">각 노드: Murmur3 해시 토큰 공간 (2^64)</div>
<div class="kb-diagram-note">VNode: 각 노드 256개 토큰 (기본값)</div>
<div class="kb-diagram-note">복제: RF=3 → 시계 방향 3개 노드에 복제</div>
<div class="kb-diagram-note">설정:</div>
<div class="kb-diagram-note">num_tokens: 256 # cassandra.yaml</div>
<div class="kb-diagram-note">DynamoDB:</div>
<div class="kb-diagram-note">파티션 키 → 내부 일관 해싱</div>
<div class="kb-diagram-note">파티션 수 자동 관리</div>
<div class="kb-diagram-note">핫 파티션 문제:</div>
<div class="kb-diagram-note">파티션 키 = 날짜(2024-01-01) → 당일 모든 쓰기 집중</div>
<div class="kb-diagram-note">해결: 파티션 키 = 날짜 + UUID suffix (분산)</div>
<div class="kb-diagram-note">Redis Cluster:</div>
<div class="kb-diagram-note">16384개 슬롯 (0~16383)</div>
<div class="kb-diagram-note">일관 해싱으로 슬롯을 노드에 배분</div>
<div class="kb-diagram-note">CRC16(key) % 16384 → 슬롯</div>
<div class="kb-diagram-note">슬롯 → 노드 매핑 (클러스터 설정)</div>
<div class="kb-diagram-note">노드 추가:</div>
<div class="kb-diagram-note">다른 노드에서 일부 슬롯만 이동</div>
<div class="kb-diagram-note">온라인 리샤딩 (무중단)</div>
<div class="kb-diagram-note">구현 (Python 예시):</div>
<div class="kb-diagram-note">import hashlib</div>
<div class="kb-diagram-note">import bisect</div>
<div class="kb-diagram-note">class ConsistentHash:</div>
<div class="kb-diagram-note">def __init__(self, vnodes=256):</div>
<div class="kb-diagram-note">self.ring = {}</div>
<div class="kb-diagram-note">self.sorted_keys = []</div>
<div class="kb-diagram-note">self.vnodes = vnodes</div>
<div class="kb-diagram-note">def add_node(self, node):</div>
<div class="kb-diagram-note">for i in range(self.vnodes):</div>
<div class="kb-diagram-note">key = self._hash(f"{node}:{i}")</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">self.ring</div><div class="kb-diagram-node">key</div><div class="kb-diagram-note">= node</div></div>
<div class="kb-diagram-note">bisect.insort(self.sorted_keys, key)</div>
<div class="kb-diagram-note">def remove_node(self, node):</div>
<div class="kb-diagram-note">for i in range(self.vnodes):</div>
<div class="kb-diagram-note">key = self._hash(f"{node}:{i}")</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">del self.ring</div><div class="kb-diagram-node">key</div></div>
<div class="kb-diagram-note">self.sorted_keys.remove(key)</div>
<div class="kb-diagram-note">def get_node(self, obj_key):</div>
<div class="kb-diagram-note">h = self._hash(obj_key)</div>
<div class="kb-diagram-note">idx = bisect.bisect_right(self.sorted_keys, h)</div>
<div class="kb-diagram-note">if idx == len(self.sorted_keys):</div>
<div class="kb-diagram-note">idx = 0</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">return self.ring[self.sorted_keys</div><div class="kb-diagram-node">idx</div><div class="kb-diagram-note">]</div></div>
<div class="kb-diagram-note">def _hash(self, key):</div>
<div class="kb-diagram-note">return int(hashlib.md5(key.encode()).hexdigest(), 16)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster = 16384 사물함 링 — 16384개 슬롯을 노드에 나눠서. 노드 추가 시 일부 슬롯만 이동(온라인 리샤딩). 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이사 없이 확장!

---

## Ⅴ. 실무 시나리오 — 글로벌 캐시 클러스터 확장



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">글로벌 이커머스 Redis Cluster 스케일아웃:</div>
<div class="kb-diagram-note">현황:</div>
<div class="kb-diagram-note">Redis Cluster 6노드 (master×3 + replica×3)</div>
<div class="kb-diagram-note">일 평균 캐시 히트율: 94%</div>
<div class="kb-diagram-note">블랙프라이데이 예상 트래픽: 평소 × 5배</div>
<div class="kb-diagram-note">현재 노드로 감당 불가 판단</div>
<div class="kb-diagram-note">확장 계획:</div>
<div class="kb-diagram-note">6노드 → 12노드 (master 6개 추가)</div>
<div class="kb-diagram-note">일관 해싱 덕분에 가능한 무중단 확장:</div>
<div class="kb-diagram-note">실행:</div>
<div class="kb-diagram-note">1. 새 노드 6개 Redis 프로세스 시작</div>
<div class="kb-diagram-note">2. CLUSTER MEET 명령으로 클러스터 합류</div>
<div class="kb-diagram-note">3. 슬롯 리밸런싱 (온라인):</div>
<div class="kb-diagram-note">기존 3 마스터가 각 16384/3 = 5461 슬롯 보유</div>
<div class="kb-diagram-note">새 6 마스터에게 각 2730 슬롯씩 이전</div>
<div class="kb-diagram-note">이전 방식:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">CLUSTER SETSLOT 0 MIGRATING</div><div class="kb-diagram-node">대상 노드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">CLUSTER SETSLOT 0 IMPORTING</div><div class="kb-diagram-node">원본 노드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">MIGRATE</div><div class="kb-diagram-node">키 이전</div></div>
<div class="kb-diagram-note">4. 클라이언트는 MOVED 에러 → 자동 재요청 (투명 마이그레이션)</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">전체 키 이전: 슬롯 이전 키만 (약 50%)</div>
<div class="kb-diagram-note">서비스 중단: 0 (무중단 리샤딩)</div>
<div class="kb-diagram-note">이전 소요: 약 2시간 (데이터 100GB)</div>
<div class="kb-diagram-note">블랙프라이데이 결과:</div>
<div class="kb-diagram-note">피크 트래픽: 평소 4.8배 (예상 5배)</div>
<div class="kb-diagram-note">캐시 히트율: 94% → 96% (용량 여유)</div>
<div class="kb-diagram-note">P99 응답시간: 8ms (목표 20ms 이하)</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">일관 해싱이 없었다면:</div>
<div class="kb-diagram-note">전체 데이터 리배치 → 6시간+ 다운타임 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 무중단 확장 = 달리는 기차에 칸 추가 — 일반 해싱이면 기차 세우고 승객([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 전원 재배치. 일관 해싱으로 달리면서 일부 승객만 새 칸으로. 무중단!

---

## 📌 관련 개념 맵

```
일관 해싱 (Consistent Hashing)
+-- 핵심 구조
|   +-- 링 (Ring, 해시 공간)
|   +-- 가상 노드 (VNode)
|   +-- 시계 방향 첫 노드 할당
+-- 장점
|   +-- 노드 변경 시 K/N 키만 이동
|   +-- 무중단 확장/축소
+-- 실제 사용
|   +-- Cassandra (Murmur3 + VNode)
|   +-- Redis Cluster (16384 슬롯)
|   +-- DynamoDB (내부 구현)
+-- 한계
    +-- 핫 스팟 문제
    +-- VNode 수 조정 필요
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[일관 해싱 제안 (1997)]
Karger et al., MIT
CDN 캐시 분산 문제 해결
      |
      v
[Amazon Dynamo (2007)]
가상 노드 도입
분산 DB 핵심 기술
      |
      v
[Cassandra 적용 (2008~)]
Facebook 오픈소스
토큰 링 표준화
      |
      v
[Redis Cluster (2015)]
16384 슬롯 방식
온라인 리샤딩
      |
      v
[현재: 랑데부 해싱 등 변형]
HRW (Highest Random Weight)
더 균등한 분산 알고리즘
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 전통 해싱 문제 = 사물함 번호 규칙 변경 — 사물함 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)→11개로 늘릴 때 거의 모든 학생이 새 사물함으로 이사. 일관 해싱은 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%만!
2. 링 구조 = 원형 시계 사물함 — 학생이 자기 번호에서 시계 방향 첫 사물함 이용. 새 사물함 추가 시 그 구간만 이사!
3. 가상 노드 = 4교대 균등 배치 — 사물함 3개가 불균등한 위치라면 4개씩 복사 배치. 어디서나 고르게 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 258

← **이전**: [047. 컴팩션과 툼스톤 — Compaction & Tombstone](/knowledge-base/studynote/14_data_engineering/01_infrastructure/047_compaction_and_tombstone/)
**다음**: [049. 데이터 메시 — Data Mesh Distributed Ownership](/knowledge-base/studynote/14_data_engineering/01_infrastructure/049_data_mesh_distributed_ownership/) →

---
