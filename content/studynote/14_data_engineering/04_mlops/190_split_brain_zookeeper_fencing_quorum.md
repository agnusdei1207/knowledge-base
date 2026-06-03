+++
title = "190. 스플릿 브레인 (Split Brain) 방어 주키퍼 (ZooKeeper) 펜싱 합의 코디 연계망"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스플릿 브레인(Split Brain)은 네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(분할) 발생 시 클러스터가 두 개 이상의 독립 그룹으로 나뉘어 <strong>각자 리더라고 주장하며 이중 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>(Dual Write)를 일으키는</strong> [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 가장 위험한 장애 패턴이다.
> 2. **가치**: 주키퍼([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))의 ZAB([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) Atomic Broadcast) 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)과 쿼럼(Quorum, 과반수) 메커니즘은 네트워크 분할에서도 <strong>하나의 일관된 진실(Single Source of Truth)</strong>을 유지하게 하는 핵심 인프라다.
> 3. **판단 포인트**: Kafka의 KRaft 모드([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 2.8+)는 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존성을 제거하여 운영 복잡도를 낮추고 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 개선—이것이 기술사 답안에서 최신 트렌드로 반드시 언급해야 할 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 스플릿 브레인 발생 시나리오



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">정상 상태: 5-노드 Kafka 클러스터</div>
<div class="kb-diagram-note">브로커1 - 브로커2 - 브로커3 - 브로커4 - 브로커5</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">리더: 브로커1</div></div>
<div class="kb-diagram-note">네트워크 파티션 발생:</div>
<div class="kb-diagram-note">── 그룹 A ── ── 그룹 B ──</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">브로커1</div><div class="kb-diagram-cell">╳</div><div class="kb-diagram-cell">브로커4</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">브로커2</div><div class="kb-diagram-cell">(단절)</div><div class="kb-diagram-cell">브로커5</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">브로커3</div></div>
<div class="kb-diagram-note">스플릿 브레인 위험:</div>
<div class="kb-diagram-note">그룹 A: "우리가 과반수(3/5), 브로커1이 리더 유지!"</div>
<div class="kb-diagram-note">그룹 B: "우리도 과반수라 착각, 브로커4를 리더로 선출!"</div>
<div class="kb-diagram-note">→ 두 리더가 동시에 쓰기 수행 → 데이터 충돌!</div>
<div class="kb-diagram-note">쿼럼 메커니즘으로 방지:</div>
<div class="kb-diagram-note">그룹 A: 3노드 (과반수 O) → 정상 운영</div>
<div class="kb-diagram-note">그룹 B: 2노드 (과반수 X) → 운영 중단 (쓰기 거부)</div>
<div class="kb-diagram-note">→ 단일 리더만 유지 (CAP 이론의 CP 선택)</div>
</div>
</div>



### 1.2 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 이론과 스플릿 브레인



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CAP 이론 트레이드오프:</div>
<div class="kb-diagram-note">C (Consistency): 모든 노드 동일한 데이터</div>
<div class="kb-diagram-note">A (Availability): 모든 요청에 응답</div>
<div class="kb-diagram-note">P (Partition Tolerance): 네트워크 분할 허용</div>
<div class="kb-diagram-note">분산 시스템은 P는 반드시 처리해야 함 → C 또는 A 선택</div>
<div class="kb-diagram-note">CP 시스템 (ZooKeeper, HBase):</div>
<div class="kb-diagram-note">네트워크 분할 시 → 소수 파티션 쓰기 거부 (일관성 우선)</div>
<div class="kb-diagram-note">→ 스플릿 브레인 방지 O, 일부 가용성 포기</div>
<div class="kb-diagram-note">AP 시스템 (Cassandra, CouchDB):</div>
<div class="kb-diagram-note">네트워크 분할에서도 모든 노드 응답 (가용성 우선)</div>
<div class="kb-diagram-note">→ 스플릿 브레인 가능, 나중에 충돌 해결(Eventually Consistent)</div>
</div>
</div>



📢 **섹션 요약 비유**: 스플릿 브레인은 마치 회사가 통신 장애로 두 팀으로 나뉘어, 각 팀이 독립적으로 계약서를 수정하면 나중에 두 개의 서로 다른 계약서가 존재하는 것과 같다. 쿼럼은 "3명 중 2명 동의 없으면 서명 금지" 규칙으로 이를 방지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [ZooKeeper ZAB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/260_zookeeper_leader_election_consensus/) ([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) Atomic Broadcast) 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ZAB 합의 프로토콜 흐름:</div>
<div class="kb-diagram-note">리더 선출 (Leader Election):</div>
<div class="kb-diagram-note">1. 모든 노드가 자신의 서버ID + 트랜잭션ID로 투표</div>
<div class="kb-diagram-note">2. 최신 트랜잭션ID를 가진 노드가 리더 후보</div>
<div class="kb-diagram-note">3. 과반수(N/2 + 1) 투표 받으면 리더 확정</div>
<div class="kb-diagram-note">4. 리더가 팔로워에게 최신 상태 동기화</div>
<div class="kb-diagram-note">정상 쓰기 흐름 (2-Phase Commit):</div>
<div class="kb-diagram-note">클라이언트 쓰기 요청 → 리더 수신</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">리더 → 팔로워 전체에게 PROPOSAL 전송 (Phase 1)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">과반수 팔로워 → ACK 응답</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">리더 → 전체에게 COMMIT (Phase 2)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라이언트에게 성공 응답</div>
<div class="kb-diagram-note">쿼럼: 2n+1 노드 중 n+1개 응답 필요</div>
<div class="kb-diagram-note">3노드: 2개 ACK 필요</div>
<div class="kb-diagram-note">5노드: 3개 ACK 필요</div>
<div class="kb-diagram-note">7노드: 4개 ACK 필요</div>
</div>
</div>



### 2.2 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 클러스터 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZooKeeper 앙상블 (5-노드) 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK-1 (리더) ZK-2 (팔로워) ZK-3 (팔로워)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZAB 리더</div><div class="kb-diagram-cell">◄──►</div><div class="kb-diagram-cell">ZAB팔로워</div><div class="kb-diagram-cell">◄──►</div><div class="kb-diagram-cell">ZAB팔로워</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">쓰기처리</div><div class="kb-diagram-cell">읽기처리</div><div class="kb-diagram-cell">읽기처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK-4 (팔로워) ZK-5 (팔로워)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZAB팔로워</div><div class="kb-diagram-cell">ZAB팔로워</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기처리</div><div class="kb-diagram-cell">읽기처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">쿼럼 = 3 (5/2 + 1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ ZK-1 장애 시: ZK-2~5 중 과반수로 새 리더 선출</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 최대 2개 노드 동시 장애까지 허용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZNode 구조:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">/kafka</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── /brokers</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── /ids/1 (브로커 메타데이터)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── /ids/2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── /controller (현재 Kafka 컨트롤러 ID)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── /consumers (컨슈머 그룹 오프셋)</div></div>
</div>
</div>



### 2.3 펜싱 (Fencing) 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">펜싱의 필요성:</div>
<div class="kb-diagram-note">구형 리더(Old Leader)가 장애에서 복구 시,</div>
<div class="kb-diagram-note">새 리더가 이미 선출된 상태에서 두 리더가 공존 가능</div>
<div class="kb-diagram-note">→ 이중 쓰기 방지를 위해 구형 리더를 강제 격리</div>
<div class="kb-diagram-note">펜싱 기법 1: 에포크 토큰 (Epoch Token / Fencing Token)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">리더 선출 시마다 에포크 번호 증가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">에포크 5: 구형 리더 (이미 격리되어야 함)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">에포크 6: 새 리더</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스토리지 서버: 에포크 &lt; 6인 요청 거부!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 구형 리더의 쓰기 자동 차단</div></div>
<div class="kb-diagram-note">펜싱 기법 2: STONITH (Shoot The Other Node In The Head)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장애 노드(구형 리더)를 물리적으로 강제 종료</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- IPMI/iDRAC/iLO로 원격 전원 차단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- SCSI 예약(SCSI-3 PR)으로 디스크 접근 차단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주의: 잘못 작동 시 정상 노드 종료 위험</div></div>
<div class="kb-diagram-note">펜싱 기법 3: ZooKeeper 에페머럴 ZNode</div>
<div class="kb-diagram-note">리더 = /leader ZNode 소유 (에페머럴)</div>
<div class="kb-diagram-note">리더 세션 만료 시 → ZNode 자동 삭제 → 재선출</div>
<div class="kb-diagram-note">새 리더가 ZNode 재생성 → 구형 리더는 ZNode 없음</div>
<div class="kb-diagram-note">→ 구형 리더의 쓰기 시도 시 ZooKeeper가 거부</div>
</div>
</div>



📢 **섹션 요약 비유**: 펜싱은 마치 회사 사장이 교체된 후 전 사장의 출입카드를 즉시 비활성화하는 것이다. 에포크 토큰은 "새 사장은 직인 번호 6번, 5번 이하 직인은 무효" 규칙으로 전 사장의 서류 결재를 자동 차단한다.

---

## Ⅲ. 비교 및 연결

### 3.1 [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) vs ZAB [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) 비교

| 항목 | [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | ZAB ([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)) |
|:---|:---|:---|
| 설계 목적 | 이해하기 쉬운 합의 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 전용 합의 |
| 리더 선출 | [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 기반 무작위 선출 | FastLeaderElection (투표 기반) |
| [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | AppendEntries [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) | PROPOSAL + ACK + COMMIT |
| 클라이언트 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 리더만 처리 | 리더만 처리 |
| 클라이언트 읽기 | 리더 or 팔로워 (설정에 따라) | 팔로워도 읽기 가능 |
| 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 완료 보장 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 순서 보장 |
| 대표 구현 | [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), Consul, TiKV | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) |

### 3.2 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존성 vs KRaft 모드 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기존 Kafka + ZooKeeper 아키텍처:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kafka 클러스터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">브로커1 - 브로커2 - 브로커3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↕ ↕ ↕</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZooKeeper 앙상블 (별도 운영)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK-1 - ZK-2 - ZK-3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메타데이터: 브로커 목록, 토픽 설정, ISR 등</div></div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-tree-item" style="--depth:1">ZooKeeper 별도 운영 복잡도</div>
<div class="kb-diagram-tree-item" style="--depth:1">메타데이터 변경 시 ZooKeeper 병목</div>
<div class="kb-diagram-tree-item" style="--depth:1">파티션 수 100만 개 이상 시 성능 한계</div>
<div class="kb-diagram-note">Kafka KRaft 모드 (Kafka 2.8+, 3.0 프로덕션 안정):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kafka KRaft 클러스터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨트롤러 1 - 컨트롤러 2 - 컨트롤러 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(RAFT 합의 + 메타데이터 관리 통합)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">브로커 1 - 브로커 2 - 브로커 3</div></div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-tree-item" style="--depth:1">ZooKeeper 불필요 → 운영 단순화</div>
<div class="kb-diagram-tree-item" style="--depth:1">파티션 수 백만 개 이상 지원</div>
<div class="kb-diagram-tree-item" style="--depth:1">컨트롤러 페일오버 수초 → 수십 밀리초로 단축</div>
<div class="kb-diagram-tree-item" style="--depth:1">단일 보안 모델 (ZooKeeper 별도 인증 불필요)</div>
</div>
</div>



### 3.3 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이션 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 비교

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 합의 | 특징 | 주요 사용처 |
|:---|:---|:---|:---|
| [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | ZAB | 성숙한 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 에코시스템 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) (구버전), [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/), [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) |
| [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) | [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 기본 스토어 | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), CoreDNS |
| Consul | [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/) 특화 | [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
| Apache Curator | ZAB (ZK 래퍼) | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 레시피 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 고수준 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |

📢 **섹션 요약 비유**: KRaft 모드는 마치 회사 행정팀([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))이 분리되어 있던 것을 없애고, 경영진([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 컨트롤러)이 직접 회사 기록을 관리하게 된 것이다. 중간 관리 비용이 줄고 의사결정이 빨라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 고가용성 배포 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZooKeeper 엔터프라이즈 배포 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터센터 A 데이터센터 B 데이터센터 C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK-1</div><div class="kb-diagram-cell">ZK-2</div><div class="kb-diagram-cell">ZK-3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK-2(2)</div><div class="kb-diagram-cell">ZK-4</div><div class="kb-diagram-cell">ZK-5</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5노드 앙상블: 최대 2개 노드 장애 허용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터센터 단위 장애 시에도 쿼럼(3/5) 유지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주의사항:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① 홀수 노드 구성 (2n+1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② 전용 SSD 사용 (fsync 지연 최소화)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ NTP 동기화 필수 (타임아웃 기반 선출)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">④ 힙 크기: 4~8GB (너무 크면 GC 정지 악화)</div></div>
</div>
</div>



### 4.2 스플릿 브레인 방지 종합 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
스플릿 브레인 방지 레이어드 전략:

  레이어 1: 네트워크 인프라
  - 이중화 네트워크 (Bonding/LACP)
  - 멀티패스 네트워크 (여러 경로)
  - 네트워크 분리 모니터링

  레이어 2: ZooKeeper/합의 프로토콜
  - 쿼럼(Quorum) 기반 의사결정
  - ZAB/RAFT 합의로 단일 리더 보장

  레이어 3: 펜싱 메커니즘
  - 에포크 토큰 (애플리케이션 레벨)
  - STONITH (인프라 레벨)
  - SCSI 예약 (스토리지 레벨)

  레이어 4: 데이터 검증
  - 체크섬 검증 (CRC32)
  - 버전 벡터 (Vector Clock)
  - 쓰기 후 읽기 검증 (Write-then-Read)
```

### 4.3 기술사 답안 핵심 포인트



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">스플릿 브레인 / ZooKeeper 설계 시 필수 언급:</div>
<div class="kb-diagram-note">✓ 스플릿 브레인 정의 + 이중 쓰기 위험성</div>
<div class="kb-diagram-note">✓ CAP 이론: ZooKeeper는 CP 선택 (일관성 우선)</div>
<div class="kb-diagram-note">✓ ZAB 프로토콜: PROPOSAL → ACK(과반수) → COMMIT</div>
<div class="kb-diagram-note">✓ 쿼럼 계산: 2n+1 노드 구성 필요</div>
<div class="kb-diagram-note">✓ 펜싱 기법: 에포크 토큰 + STONITH 레이어드 방어</div>
<div class="kb-diagram-note">✓ KRaft 모드: Kafka 3.0+ ZooKeeper 의존성 제거</div>
<div class="kb-diagram-note">✓ 홀수 노드 구성 이유: 과반수 계산 용이, 동점 방지</div>
<div class="kb-diagram-note">✓ etcd vs ZooKeeper: Kubernetes는 etcd+RAFT 사용</div>
<div class="kb-diagram-note">✓ ZooKeeper 운영 주의: 전용 SSD, NTP 동기화, 힙 크기</div>
</div>
</div>



📢 **섹션 요약 비유**: 스플릿 브레인 방지 레이어드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 마치 은행 금고의 다중 잠금 장치와 같다. 네트워크 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)(첫 번째 자물쇠), 쿼럼 합의(두 번째 자물쇠), 펜싱(세 번째 자물쇠) 중 하나가 뚫려도 다음 단계에서 차단한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이션 도입 효과

| 효과 | 내용 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 스플릿 브레인 원천 차단으로 이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 0 |
| 리더 선출 자동화 | 수동 개입 없이 수초 내 자동 페일오버 |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금 | 글로벌 뮤텍스로 크리티컬 섹션 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/) | 동적 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 등록·조회 ([마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)) |

### 5.2 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의 기술 발전 방향



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분산 합의 기술 발전 트렌드</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2006: ZooKeeper + ZAB 오픈소스 공개</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2014: etcd + RAFT (CoreOS, Kubernetes 핵심)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2019: Kafka KIP-500: KRaft 제안 (ZK 제거)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2021: Kafka 2.8: KRaft 얼리 액세스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2022: Kafka 3.3: KRaft 프로덕션 안정화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2023: Kafka 3.7: ZooKeeper 지원 완전 제거 예고</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">트렌드:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 합의 알고리즘 내재화 (외부 ZK 의존 제거)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ RAFT 우세 (이해 쉬움, 구현 라이브러리 풍부)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 분산 합의의 클라우드 네이티브화 (etcd + K8s)</div></div>
</div>
</div>



### 5.3 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계 원칙 요약

| 원칙 | 구현 방법 |
|:---|:---|
| 홀수 노드 구성 | 2n+1 노드로 쿼럼 계산 단순화 |
| 레이어드 펜싱 | 에포크 토큰 + STONITH + 스토리지 예약 |
| 장애 허용 설계 | 최대 n개 노드 장애 허용 (n = (클러스터 크기-1)/2) |
| 합의 내재화 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 외부 의존 → KRaft 내재화 |

📢 **섹션 요약 비유**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의의 발전은 마치 회사 이사회 구조 발전과 같다. 처음엔 외부 공증 회사([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))에게 의사결정 기록을 맡겼지만, 이제는 이사회([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 컨트롤러) 자체에 기록과 합의 권한을 내재화하여 더 빠르고 효율적으로 운영하는 방향으로 발전했다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 장애 | 스플릿 브레인 (Split Brain) | 네트워크 분할 시 이중 리더 발생 |
| 해결 메커니즘 | 쿼럼 (Quorum) | 과반수 노드 동의로만 결정 |
| 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | ZAB ([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) Atomic Broadcast) | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 전용 2-phase 합의 |
| 격리 메커니즘 | 펜싱 (Fencing) | 구형 리더 강제 격리 |
| 이론 기반 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)/[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)/[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용 트레이드오프 |
| 비교 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), Consul, KRaft의 [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) |
| 최신 트렌드 | KRaft ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [RAFT](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/)) | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 3.x+ [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존성 제거 |
| 물리적 펜싱 | STONITH | 구형 리더 원격 전원 차단으로 격리 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>스플릿 브레인</strong>은 마치 반장 선거를 하다가 교실이 둘로 나뉘어, 앞쪽 학생들은 A가 반장이라 하고 뒤쪽 학생들은 B가 반장이라고 주장하는 상황이에요—두 명이 동시에 반장 노릇을 하면 학급이 혼란에 빠지는 것처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스도 엉망이 돼요.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">분산 시스템 네트워크 파티션 발생</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">스플릿 브레인: 두 리더가 동시 존재 → 데이터 불일치</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">방어 메커니즘</div>
<div class="kb-diagram-tree-item" style="--depth:2">쿼럼 (Quorum): 과반수 합의 (N/2+1)</div>
<div class="kb-diagram-tree-item" style="--depth:2">펜싱 (Fencing): 이전 리더 강제 차단 (STONITH)</div>
<div class="kb-diagram-tree-item" style="--depth:2">ZooKeeper · etcd: 분산 코디네이터</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CAP 정리: Consistency vs Availability 트레이드오프</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Raft · Paxos 합의 알고리즘 → 안전한 리더 선출</div>
</div>
</div>


2. <strong>쿼럼</strong>은 "반 전체 30명 중 16명 이상이 동의해야 반장이 된다"는 규칙이에요—교실이 둘로 나뉠 때 한쪽이 16명 이상이어야만 반장을 선출할 수 있어서, 양쪽 동시에 반장이 나오는 일이 없어요.
3. <strong>펜싱</strong>은 새 반장이 뽑힌 후 전 반장의 교실 열쇠와 반장 도장을 즉시 회수하는 것처럼, 구형 리더가 실수로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 건드리지 못하게 물리적으로 차단하는 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 190 / 258

← **이전**: [189. 카프카 컨슈머 랙 (Kafka Consumer Lag) 지연 모니터링 경보 파이프](/knowledge-base/studynote/14_data_engineering/04_mlops/189_kafka_consumer_lag_monitoring_alert/)
**다음**: [191. 람다/카파 아키텍처 재현 (Event Sourcing Replay - Lambda/Kappa Architecture)](/knowledge-base/studynote/14_data_engineering/04_mlops/191_event_sourcing_replay_lambda_kappa/) →

---
