+++
title = "647. 비잔틴 장애 허용 (BFT) 분산 시스템 검증"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비잔틴 장애 허용 (Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/), BFT) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 일부 노드가 거짓말하거나 서로 다른 메시지를 보내더라도, <strong>제안·투표·합의 결과·<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong>가 여전히 올바른지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 절차다.
> 2. **가치**: 단순 장애 허용보다 한 단계 더 나아가 메시지 위조, 이중 제안, 가짜 커밋을 막아 주므로, 금융 네트워크·컨소시엄 체인·고신뢰 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서비스의 안전한 최종 확정성을 만든다.
> 3. **판단 포인트**: BFT의 성패는 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 속도만이 아니라 <strong>정족수 계산, 뷰 변경, 상태 이전 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>까지 한 세트로 설계했는지에 달려 있으며, 암호 가속은 보조 수단이지 안전성 자체를 대신하지 않는다.

---

## Ⅰ. 개요 및 필요성

BFT [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 노드 일부가 단순히 멈추는 것이 아니라, 잘못된 값을 보내거나 서로 다른 상대에게 서로 다른 제안을 던질 수 있다고 가정한다. 따라서 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 목표는 `누가 살아 있는가`보다 `무엇이 정당한 합의인가`를 판별하는 데 있다. 이것이 크래시 장애 허용 시스템보다 훨씬 강한 가정이자, 더 복잡한 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차가 필요한 이유다.

대표적으로 BFT 계열 합의는 `f`개의 비잔틴 노드를 견디기 위해 최소 `3f + 1`개의 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이 필요하고, 의미 있는 정족수 증거는 보통 `2f + 1`개의 일치된 표로 만든다. 이 수학적 조건이 깨지면 악성 노드가 소수 의견으로도 합의 결과를 위조할 수 있다. 그래서 BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의, 상태 머신 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 동시에 보는 통합 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 문제다.

- **📢 섹션 요약 비유**: 이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 단순 출석 체크가 아니라 배심원단 재판과 같다. 몇 명이 앉아 있는지만 보는 게 아니라, 같은 증거를 보고 같은 판결에 동의했는지까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 판결이 효력을 가진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 보통 제안 수신, 메시지 진위 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 정족수 증명 조립, [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 적용의 순서로 진행된다. 최신 계열의 실용적 BFT (Practical Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/), [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)) 또는 HotStuff류 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 단계 수와 메시지 패턴은 다르지만, 공통적으로 `이 제안이 올바른 부모를 잇는가`, `충분한 수의 정당한 투표가 붙었는가`, `같은 높이에 이중 커밋이 없는가`를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Generic BFT verification pipeline</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Proposal -&gt; verify sender + parent QC -&gt; replicas vote</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">signature check 2f+1 matching votes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&gt; Quorum Certificate &gt; Commit</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">State apply</div></div>
</div>
</div>



| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 대상 | [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 내용 | 빠지면 생기는 문제 |
| :--- | :--- | :--- |
| 송신자 진위 | 디지털 서명, 키 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 메시지 포맷 | 가짜 노드가 투표를 위조 |
| 제안 연속성 | 부모 제안, 높이, 뷰 번호, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 순서 | 포크된 커밋 또는 이중 실행 |
| 정족수 증명 | `2f + 1`개의 일치된 표 존재 여부 | 소수 의견이 합의로 오인 |
| [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | 실행 결과 해시, 체크포인트, 상태 이전 증명 | 노드마다 다른 결과를 커밋 |

여기서 [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/)적 병목이 크기 때문에 공개키 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 종종 하드웨어 가속의 도움을 받는다. 예를 들어 암호 연산 가속기, 스마트 [네트워크 인터페이스 카드](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/), [신뢰 실행 환경](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/), [TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/)) 은 서명 처리와 키 보호를 보조한다. 그러나 어떤 가속기를 써도 `정족수 교집합`과 `로그 연속성` 규칙이 무너지면 시스템은 안전하지 않다.

- **📢 섹션 요약 비유**: 아무리 빠른 바코드 스캐너가 있어도, 물류센터에서 박스 번호와 배송 순서를 안 맞추면 택배는 엉뚱한 곳에 간다. 속도보다 먼저 지켜야 할 것은 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 규칙의 순서다.

---

## Ⅲ. 비교 및 연결

BFT를 이해하려면 크래시 장애 허용 (Crash [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/), CFT) 과의 경계를 분명히 해야 한다. CFT는 노드가 멈추기만 한다고 보므로 다수결이 비교적 단순하지만, BFT는 노드가 거짓 메시지를 보내고 이중 행동을 할 수 있다고 보기 때문에 같은 다수결이라도 훨씬 엄격한 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하다.

| 항목 | CFT 합의 | BFT 합의 |
| :--- | :--- | :--- |
| 장애 가정 | 노드 중단, 응답 없음 | 중단 + 거짓말 + 이중 제안 |
| 필요한 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수 | 보통 `2f + 1` | 보통 `3f + 1` |
| 커밋 증거 | 과반수 응답 | `2f + 1`개의 정당한 표와 교집합 보장 |
| 대표 예시 | [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/), Paxos | [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/), HotStuff, Tendermint 계열 |
| 주 병목 | 리더 선출, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 메시지 수, 뷰 변경 복잡도 |

현대 BFT는 이 병목을 줄이기 위해 정족수 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 (Quorum Certificate, QC), 집계 서명, 배치 투표를 사용한다. 또한 일부 시스템은 본-린-샤참 서명 (Boneh-Lynn-Shacham Signature, BLS Signature) 같은 집계 기법으로 통신량을 줄이고, 하드웨어 키 보호와 원격 증명으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자 신원을 더 강하게 묶는다. 즉 BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 이론과 컴퓨터 아키텍처가 만나는 지점이다.

- **📢 섹션 요약 비유**: CFT가 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 고장만 대비하는 철도라면, BFT는 일부 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)원이 일부러 거짓 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 보낼 상황까지 가정한 철도다. 그래서 선로만 튼튼하면 되는 것이 아니라 관제 규칙도 훨씬 촘촘해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 `누가 참여하는가`와 `얼마나 빨리 확정해야 하는가`가 핵심이다. 참여자가 제한된 컨소시엄이라면 강한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 체계와 낮은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 장점을 살릴 수 있지만, 노드 수가 늘수록 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 네트워크 메시지 비용이 빠르게 커진다. 따라서 무조건 BFT를 택하기보다, 정말로 악성 행위까지 가정해야 하는 업무인지부터 따져야 한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 허용할 비잔틴 노드 수 `f`에 대해 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수 `3f + 1`과 정족수 `2f + 1`을 만족하는가?
2. 제안·투표·체크포인트·상태 이전에 각각 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 해시와 서명 체계가 있는가?
3. 뷰 변경 시 이전 리더의 미완료 제안이 안전하게 정리되는가?
4. 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 병목이라면 배치 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 집계 서명, 하드웨어 가속의 비용 대비 효과를 검토했는가?
5. 시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 실패나 [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/) 급증 시 [timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) 조정 전략이 준비되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 표를 중앙 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 서버 한 대가 대신 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하게 만들어 단일 장애점을 만드는 경우
- 정상 경로 테스트만 하고, 악성 노드의 이중 제안·늦은 메시지·가짜 체크포인트를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하지 않는 경우
- 키 회전과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 폐기를 운영 절차로 묶지 않아, 논리적으로는 안전해도 실제 배포에서는 취약해지는 경우

기술사 관점에서는 `합의가 돌아간다`와 `검증 가능하게 안전하다`를 구분해야 한다. 서명이 빠르게 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)된다고 끝이 아니라, 그 서명이 어느 뷰·어느 높이·어느 부모를 가리키는지까지 추적되어야 한다. 결국 BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 암호 연산 속도와 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 상태 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 검사를 함께 맞추는 설계 문제다.

- **📢 섹션 요약 비유**: 문지기가 신분증만 빨리 훑는다고 안전한 건 아니다. 어느 행사장 입장권인지, 이미 다른 문으로 들어간 표는 아닌지까지 봐야 진짜 통제가 된다.

---

## Ⅴ. 기대효과 및 결론

BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체계가 잘 설계되면 악성 노드가 일부 섞여도 잘못된 커밋을 막고, 높은 신뢰도의 최종 확정성을 제공할 수 있다. 금융 거래, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 원장, 중요한 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서비스에서는 이 특성이 곧 서비스의 신뢰 브랜드가 된다. 또한 정족수 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서와 가속된 서명 처리 덕분에 예전보다 더 큰 규모의 실용적 BFT 시스템도 가능해지고 있다.

반대로 대가도 분명하다. 메시지 수, 키 관리, [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 구현 복잡도가 CFT보다 훨씬 크다. 따라서 이 주제를 기억할 때는 `BFT는 서명 많이 쓰는 합의`가 아니라, <strong>거짓말하는 참여자 속에서도 상태 머신의 단일 진실을 유지하기 위해 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 규칙을 촘촘하게 쌓은 체계</strong>라고 이해해야 한다.

- **📢 섹션 요약 비유**: BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 배를 빠르게 달리게 하는 돛이 아니라, 폭풍 속에서도 배가 같은 방향을 보게 붙잡는 키와 나침반이다. 속도보다 중요한 것은 방향을 잃지 않는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 실용적 비잔틴 장애 허용 (Practical Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/), [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)) | BFT [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차를 실제 시스템에 적용한 대표 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 계열이다. |
| 정족수 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 (Quorum Certificate, QC) | 충분한 수의 투표가 모였음을 압축해 표현하는 핵심 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 증거다. |
| 본-린-샤참 서명 (Boneh-Lynn-Shacham Signature, BLS Signature) | 다수 서명을 하나로 묶어 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·전송 비용을 줄이는 집계 서명 기법이다. |
| 뷰 변경 ([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) Change) | 리더 장애나 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시 안전하게 새 라운드로 넘어가기 위한 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차다. |
| [신뢰 실행 환경](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/), [TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/)) | 키 보호와 일부 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 보조를 담당해 BFT 구현의 공격면을 줄인다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Crash fault assumptions</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">PBFT-style authenticated voting</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Quorum certificates and pipelined commits</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Aggregated signatures + hardware crypto assist</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">High-throughput permissioned BFT services</div>
</div>
</div>



이 흐름은 `중단만 가정하던 복제`에서 `악성 행위까지 검증하는 고신뢰 합의`로 발전하는 경로를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 친구가 같이 규칙을 정할 때, 몇몇 친구가 거짓말을 할 수도 있다고 생각하고 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 방법이 BFT예요.
2. 그래서 누가 말했는지, 몇 명이 같은 말을 했는지, 순서가 맞는지를 하나씩 꼭 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
3. 덕분에 장난꾸러기 친구가 있어도 반 전체가 엉뚱한 결정을 하지 않게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 648 / 803

← **이전**: [646. 블록체인 노드 스토리지 병목 현상](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/646_blockchain_storage_bottleneck/)
**다음**: [648. 캡 정리 (CAP Theorem)와 분산 스토리지](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/648_cap_theorem_storage/) →

---
