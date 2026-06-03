+++
title = "624. BMT (Bench Mark Test) 절차 및 평가 항목"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [벤치마크 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/450_benchmark_test/) (BMT, Bench Mark Test)는 장비 도입 전에 실제 업무와 유사한 부하를 걸어, 후보 시스템의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·운영성을 객관적으로 비교하는 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차다.
> 2. **가치**: 카탈로그의 최대 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 대신, 조직이 정의한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기·동시 사용자·[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 기준·장애 시나리오를 동일 조건에서 시험함으로써 구매 실패 위험을 크게 줄인다.
> 3. **판단 포인트**: 좋은 BMT는 최고 속도 한 번이 아니라 p95/p99 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간, 운영 편의성, 재현성을 함께 본다.

---

## Ⅰ. 개요 및 필요성

BMT는 서버, 스토리지, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 장비, 네트워크 장비를 실제 도입하기 전에 시험 환경에서 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 절차다. 핵심은 "무엇이 가장 빠른가"보다 "우리 업무 조건에서 누가 안정적으로 요구 수준을 만족하는가"를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 데 있다. 그래서 BMT는 단순 기술 테스트가 아니라, 조달과 운영을 연결하는 의사결정 단계라고 볼 수 있다.

BMT가 필요한 이유는 제조사 스펙이 대개 특정 조건에서 측정된 최댓값이기 때문이다. 예를 들어 저장장치가 4KB, 100% 읽기, 큐 깊이 최대 조건에서 100만 IOPS를 낸다고 해도, 실제 업무가 64KB 혼합 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 높은 동시성으로 움직인다면 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 크게 다를 수 있다. 결국 구매자는 자기 업무 패턴을 반영한 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이는 "빠른 장비"가 아니라 "우리 환경에서 맞는 장비"를 고르기 어렵다.

특히 공공·금융·대형 기업 환경에서는 한 번의 장비 선정이 수년의 운영 안정성을 좌우한다. 따라서 BMT는 단순한 기술 비교가 아니라, 장애 비용과 재도입 비용을 줄이는 <strong>사전 <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a> 통제 장치</strong>로 이해해야 한다.

- **📢 섹션 요약 비유**: BMT는 광고만 보고 차를 사지 않고, 내가 매일 다니는 언덕길과 막히는 출근길에서 직접 시승해 보는 절차와 같다. 화려한 카탈로그보다 내 길에서의 실제 반응이 더 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 BMT는 요구사항 정의부터 점수화까지 단계가 분명해야 한다. 먼저 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 ([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), [Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)), 목표 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 ([RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [Recovery Time Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)), 목표 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시점 ([RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), [Recovery Point Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)) 같은 운영 기준을 수치로 확정한다. 그 다음 생산계와 유사한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋, 동시 사용자 수, 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비율, 배치 작업 패턴을 설계하고, 후보 장비들을 같은 조건에서 반복 측정한다.

| 단계 | 수행 내용 | 대표 평가 항목 |
| :-- | :-- | :-- |
| 요구사항 정의 | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), 용량, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 목표, 장애 허용 범위 확정 | p95/p99 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 |
| 시험 환경 구축 | 네트워크, OS, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 기준 통일 | 비교 공정성, 재현성 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 시험 | 정상 부하·최대 부하·혼합 부하 실행 | TPS/IOPS, CPU headroom, tail [latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 시험 | 디스크, [NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/), 전원, 노드 장애 주입 | [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) 시간, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 여부 |
| 운영성 평가 | 설치, 증설, 모니터링, 알람, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 관리 편의성, 자동화 수준 |

아래 흐름은 BMT가 단순 벤치마크 한 번이 아니라, 사전 기준을 둔 의사결정 과정임을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BMT flow: same workload, same rules, measurable result</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Requirement</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Workload Model -&gt; Testbed Setup -&gt; Run &amp; Repeat -&gt; Fault Injection</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Scorecard &amp; Pass/Fail Decision</div></div>
</div>
</div>



이 과정에서 중요한 것은 워밍업 구간과 정상 상태 구간을 분리하고, 평균값뿐 아니라 꼬리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 자원 여유율을 함께 보는 것이다. 또한 장애 시험은 단순 핑 손실이 아니라 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 절체, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 운영 알람까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다. BMT의 품질은 테스트 도구보다 <strong>조건 통제와 평가 기준의 명확성</strong>에서 결정된다.

- **📢 섹션 요약 비유**: BMT는 한 번의 달리기 기록만 보는 체력장이 아니라, 오래 뛰기·비 오는 날 달리기·넘어졌다 다시 일어나기까지 함께 보는 종합 체력 검사와 같다.

---

## Ⅲ. 비교 및 연결

실무에서는 개념 증명 (PoC, Proof of [Concept](/knowledge-base/studynote/14_data_engineering/02_math_mining/120_concept/))과 BMT를 자주 혼동하지만 목적이 다르다. PoC는 "이 기술이 우리 문제를 해결할 가능성이 있는가"를 빠르게 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 탐색 단계이고, BMT는 "도입 후보 중 누가 요구 기준을 안정적으로 만족하는가"를 비교하는 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계다. 또한 구매 이후 장비가 계약 조건에 맞게 납품되었는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 인수 시험 ([FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)/[SAT](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/), Factory/Site [Acceptance Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/))과도 구분해야 한다.

| 구분 | 질문 | 시점 | 결과물 |
| :-- | :-- | :-- | :-- |
| PoC | 적용 가능성은 있는가? | 도입 검토 초반 | 기술 적합성 판단 |
| BMT | 후보 장비 중 누가 기준을 만족하는가? | 제안·선정 단계 | 점수표, 우선협상 근거 |
| [FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)/[SAT](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/) | 계약 장비가 약속대로 납품·설치되었는가? | 구매 이후 | 인수 승인 근거 |

BMT는 다른 운영 지표와도 연결된다. 예를 들어 고가용성 장비라면 [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), 절체 성공률을 함께 봐야 하고, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 장비라면 표준 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)평가위원회 ([TPC](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/154_tpc/), [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing [Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) Council) 벤치마크 같은 참고 지표와 자체 실부하 시험을 같이 활용할 수 있다. 즉 BMT는 단독 이벤트가 아니라, SLA와 인수 기준을 수치로 연결하는 중간 다리다.

- **📢 섹션 요약 비유**: PoC는 메뉴 시식회, BMT는 본선 요리 대회, [FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)/SAT는 배달 온 음식이 주문서와 맞는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 단계와 같다. 이름은 비슷해 보여도 묻는 질문이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 좋은 BMT를 만들려면 먼저 합격 기준을 벤더 시험 전에 확정해야 한다. 예를 들어 "p99 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 50ms 이하, 노드 장애 시 30초 내 절체, 72시간 안정 운전, 운영 알람 자동 연동"처럼 수치와 조건을 먼저 못 박아야, 시험 중에 기준이 흔들리지 않는다. 또한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋은 익명화하더라도 실제 분포와 크기를 반영해야 하며, 후보별 튜닝 허용 범위도 동일하게 맞춰야 공정성이 유지된다.

기술사 관점의 체크리스트는 다음과 같다.

1. 평균 응답시간이 아니라 p95/p99 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 자원 여유율을 함께 보는가?
2. 정상 부하, 피크 부하, 장시간 안정성 시험이 모두 포함되는가?
3. 장애 주입 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 절체 시간, 운영 알람까지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는가?
4. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 40, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 30, 운영성 20, 비용 10처럼 가중치가 사전에 정의돼 있는가?

흔한 실패는 벤더가 잘하는 스크립트만 돌리고 끝내는 것이다. 또 하나의 실패는 최고 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 숫자만 보고 선택해, 실제 운영에서 꼬리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이나 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 나쁜 장비를 뽑는 경우다. BMT의 목표는 우승 기록이 아니라 <strong>운영 가능한 장비를 증거 기반으로 고르는 것</strong>이라는 점을 잊지 말아야 한다.

- **📢 섹션 요약 비유**: 시험 범위를 미리 정하지 않으면 학생이 잘하는 문제만 풀고도 만점처럼 보일 수 있다. BMT는 전 과목과 실전 상황까지 포함해 진짜 실력을 보게 만드는 감독 규칙이다.

---

## Ⅴ. 기대효과 및 결론

BMT를 제대로 수행하면 장비 선정의 실패 확률을 줄이고, 운영 중 예상치 못한 병목과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 문제를 사전에 발견할 수 있다. 또한 벤더 제안서의 추상적 표현을 수치와 로그로 바꾸어, 내부 승인과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응에도 강한 근거를 남길 수 있다. 대규모 사업일수록 이 문서화 효과는 기술적 효과만큼 중요하다.

물론 BMT가 모든 미래를 보장하지는 않는다. 생산계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화, 사용자 증가, 소프트웨어 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 차이로 실제 운영 결과는 달라질 수 있으므로, 도입 후에도 주기적 재검증과 모니터링이 필요하다. 그래도 BMT는 "감으로 사는 장비"를 "증거로 고르는 장비"로 바꾸는 핵심 절차다. 이 주제는 결국 <strong>벤더 스펙을 믿을 것인가가 아니라, 우리 기준으로 증명시킬 것인가의 문제</strong>로 기억하면 된다.

- **📢 섹션 요약 비유**: BMT는 큰 시험 전에 미리 실전 모의고사를 치러 보는 것과 같다. 점수를 미리 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 본시험에서 놀랄 일이 줄어든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 ([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), [Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) | BMT의 합격 기준을 정의하는 출발점 |
| 개념 증명 (PoC, Proof of [Concept](/knowledge-base/studynote/14_data_engineering/02_math_mining/120_concept/)) | BMT 이전 단계의 기술 가능성 검토 |
| 꼬리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (Tail [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 평균값만으로 숨겨지는 실사용 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제 |
| 절체 ([Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 시험에서 반드시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 핵심 동작 |
| 인수 시험 ([FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)/[SAT](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/), Factory/Site [Acceptance Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)) | 구매 이후 계약 이행 여부를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 후속 절차 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">요구사항 · SLA 정의</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">워크로드 모델링 · 시험 환경 통일</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">성능 · 가용성 · 운영성 반복 측정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">점수화 · 우선순위 결정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">도입 이후 FAT/SAT 및 운영 검증 연계</div>
</div>
</div>



이 흐름은 BMT가 단발 테스트가 아니라, 선정·구매·운영 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 잇는 연속 절차임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. BMT는 새 자전거를 사기 전에 진짜 길에서 타 보고 고르는 시험이에요.
2. 빨리 달리는지만 보는 게 아니라, 오래 타도 괜찮은지와 넘어졌을 때 잘 버티는지도 함께 봐요.
3. 그래서 BMT를 하면 멋져 보이기만 하는 자전거보다 정말 잘 탈 수 있는 자전거를 고를 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 624 / 803

← **이전**: [623. 데이터센터 PUE (Power Usage Effectiveness)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/623_datacenter_pue/)
**다음**: [625. SLA (Service Level Agreement) 하드웨어 가용성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/625_sla_hardware_availability/) →

---
