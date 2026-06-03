+++
title = "450. MTBF (평균 무고장 시간)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MTBF (Mean Time Between Failures)는 <strong>수리 가능한 시스템이 두 번의 고장 사이에서 평균적으로 얼마나 오래 정상 동작하는지</strong>를 나타내는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 지표다.
> 2. **가치**: 이 지표는 장비 한 대의 "수명 예언"이 아니라, 대규모 장비군에서 <strong>예상 고장 빈도·예비 부품·<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/">이중화</a> 수준</strong>을 계산하게 해 주는 운영 설계 기준이다.
> 3. **판단 포인트**: MTBF 숫자가 높아도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 안전한 것은 아니며, 실제 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a> (Mean Time To Repair), <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a> (Single Point of Failure), <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/">이중화</a> 구조</strong>와 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

MTBF (Mean Time Between Failures)는 수리 가능한 장비나 시스템에서 한 번 고장이 난 뒤 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)되고 나서, 다음 고장이 발생할 때까지의 평균 간격을 뜻한다. 현장에서는 이를 "평균 정상 가동 시간"처럼 단순화해 쓰는 경우가 많지만, 핵심은 <strong>개별 장비의 운명</strong>보다 <strong>집단 운영에서의 고장 패턴</strong>을 읽는 데 있다.

이 지표가 필요한 이유는 현대 시스템이 더 이상 단일 부품으로 끝나지 않기 때문이다. 서버 한 대에는 중앙처리장치인 CPU (Central Processing Unit), 메모리, 전원공급장치인 PSU ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply Unit), 저장장치, 냉각부가 함께 들어가고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 다시 수십~수천 대의 노드 위에서 돌아간다. 이런 환경에서는 "좋은 부품을 썼다"보다 "얼마나 자주 고장이 발생할 것으로 보고 운영을 설계할 것인가"가 더 중요하다.

특히 데이터센터나 클라우드 환경에서는 고장이 예외가 아니라 상수다. MTBF를 모르면 예비 부품 재고, 유지보수 계약, 교체 주기, 장애 대응 인력 배치를 감으로 정해야 한다. 반대로 MTBF를 이해하면 "고장은 반드시 난다"는 전제 위에서 운영을 수치화할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MTBF가 답하는 질문: "얼마나 오래 버티는가"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">고장 발생 ──▶ 복구 완료 정상 운영 ▶ 다음 고장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&lt;----------- 평균 간격 = MTBF -----------&gt;</div></div>
</div>
</div>



이 그림의 핵심은 MTBF가 "고장이 없는 이상세계"를 뜻하지 않는다는 점이다. 오히려 고장이 반복된다는 현실을 인정하고, 그 사이 간격을 평균값으로 다루는 운영 지표에 가깝다.

📢 섹션 요약 비유: MTBF는 자동차 한 대가 평생 몇 년 탈 수 있는지 맞히는 점쟁이가 아니라, 택시 회사가 "우리 차 1,000대 중 이번 달에 몇 대쯤 정비소에 들어오겠구나"를 계산하는 통계 장부와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MTBF는 보통 고장률이 비교적 안정적인 구간에서 의미가 크다. 전자부품은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 불량 구간, 안정 구간, 마모 구간을 거치는 욕조 곡선 ([Bathtub Curve](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/756_bathtub_curve/)) 특성을 보이는데, MTBF는 주로 <strong>안정 구간의 평균 고장 간격</strong>을 대표값으로 삼는다. 그래서 신품 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 불량이 많거나, 수명 말기에 급격히 마모되는 장비에는 MTBF 하나만으로 설명이 부족할 수 있다.

고장률을 λ([람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/))라고 두고 고장이 무작위로 발생한다고 가정하면, 안정 구간에서는 대략 `MTBF ≈ 1 / λ`로 볼 수 있다. 또한 운영 관점에서는 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair)와 묶어서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)인 Availability를 판단한다. 즉, <strong>자주 안 고장 나는가</strong>와 <strong>고장 나면 얼마나 빨리 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>하는가</strong>가 같이 움직여야 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질이 결정된다.

| 지표 | 의미 | 주로 보는 대상 | 실무 해석 |
| :--- | :--- | :--- | :--- |
| [MTTF](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/) (Mean Time To Failure) | 수리 불가능한 부품의 평균 고장 시점 | 소모성 부품, 수명 종료형 장비 | "언제 교체될 가능성이 큰가" |
| MTBF (Mean Time Between Failures) | 수리 가능한 시스템의 평균 고장 간격 | 서버, 네트워크 장비, 전원계 | "얼마나 자주 장애가 날까" |
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair) | 고장 후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)까지 걸리는 평균 시간 | 운영 프로세스 전체 | "장애가 나면 얼마나 빨리 살릴까" |

아래 그림은 MTBF와 MTTR이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)으로 이어지는 관계를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장애 운영 주기: 신뢰성은 간격과 복구의 합</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">정상 운영(MTBF) 장애 감지/수리(MTTR) 정상 운영(MTBF)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">서비스 체감 품질 = 고장 사이 간격이 길수록 ↑, 복구 시간이 짧을수록 ↑</div></div>
</div>
</div>



[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약인 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) 관점에서는 보통 `Availability ≈ MTBF / (MTBF + MTTR)` 형태로 직관적으로 설명한다. 예를 들어 MTBF가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000시간이고 MTTR이 1시간이면 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 매우 높지만, MTBF가 100,000시간이라도 MTTR이 24시간이면 고객 체감 품질은 크게 흔들릴 수 있다.

📢 섹션 요약 비유: MTBF는 병에 잘 안 걸리는 체질이고, MTTR은 아팠을 때 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) 속도다. 튼튼한 사람도 한 번 앓으면 오래 누워 있으면 문제고, 자주 아파도 금방 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)하면 일상 유지가 가능하다.

---

## Ⅲ. 비교 및 연결

MTBF를 제대로 쓰려면 비슷해 보이는 지표와의 경계를 분명히 해야 한다. 가장 흔한 오해는 MTBF를 "장비 한 대의 보장 수명"으로 받아들이는 것이다. 하지만 MTBF는 개체의 운명을 말하기보다, 같은 조건에서 운영되는 장비 집단의 평균 고장 간격을 말한다.

| 비교 축 | MTBF | [MTTF](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/) | AFR (Annualized Failure Rate) |
| :--- | :--- | :--- | :--- |
| 초점 | 고장 사이 평균 간격 | 처음부터 고장까지 평균 시간 | 1년 기준 예상 고장 비율 |
| 대상 | 수리 가능한 시스템 | 수리보다 교체 중심 부품 | 운영 리포트, 제조사 스펙 비교 |
| 오해 포인트 | 개별 장비 수명으로 착각 | 수리 시스템에 그대로 적용 | 사용 조건 차이를 무시하기 쉬움 |

또 하나의 중요한 연결은 개별 부품 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 시스템 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 다르다는 점이다. [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 의존성이 큰 시스템은 한 부품만 고장 나도 전체가 멈추므로, 시스템 MTBF는 가장 약한 고리의 영향을 강하게 받는다. 반대로 [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) (Redundant [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks), 이중 전원, 클러스터 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)처럼 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)를 두면 개별 부품 MTBF가 낮아도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체 MTBF와 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 크게 높일 수 있다.

운영체제와 클라우드 관점으로 확장하면, MTBF는 결국 [RAS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/449_ras/) ([Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/), [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), Serviceability) 중 Reliability를 수치화한 입력값이다. 여기에 자동 장애 감지, 핫스왑, [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/), 오토스케일링이 붙으면 "부품이 안 고장 나는 시스템"이 아니라 "고장 나도 멈추지 않는 시스템"으로 사고방식이 옮겨간다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">개별 부품 신뢰성</div>
<div class="kb-diagram-tree-item" style="--depth:2">높음 ──▶ 단일 장비 안정성 향상</div>
<div class="kb-diagram-tree-item" style="--depth:2">낮음 ──▶ 이중화·복제 없으면 서비스 장애 증가</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">시스템 수준 설계 필요</div>
<div class="kb-diagram-note">(RAID, Failover, Cluster)</div>
</div>
</div>



📢 섹션 요약 비유: MTBF만 보는 것은 선수 개인 기록만 보고 축구팀 우승 가능성을 판단하는 것과 같다. 스트라이커가 좋아도 수비와 골키퍼가 약하면 팀은 무너지고, 반대로 팀워크와 교체 전략이 좋으면 개인 기록이 평범해도 우승할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 MTBF는 구매 카탈로그를 읽는 숫자가 아니라, 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 정하는 입력값이다. 예를 들어 저장장치 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개를 운영하고 장치당 MTBF가 1,200,000시간이라면, 단순 기대값으로 연간 고장 수는 `10,000 × 8,760 / 1,200,000 ≈ 73건` 수준으로 추정할 수 있다. 이 계산은 완벽한 예언은 아니지만, 예비 디스크 수량, 야간 교체 인력, 자동 리빌드 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 정하는 데 매우 유용하다.

기술사 답안이나 아키텍처 검토에서 중요한 판단은 "MTBF가 높으니 안전하다"가 아니라 "고장 기대 빈도에 비해 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계가 충분한가"다. 따라서 MTBF는 반드시 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/), 핫스페어, 장애 감지 시간, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수준과 같이 제시해야 한다. 특히 단일 장애점인 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure)가 남아 있으면 MTBF가 높은 고급 부품도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관점에서는 큰 의미가 없다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 제조사 MTBF 값이 어떤 온도, 부하, 진동 조건에서 측정되었는지 확인했는가?
2. 장비 수량을 곱해 연간 예상 고장 건수로 환산해 보았는가?
3. 고장 발생 시 MTTR을 줄일 핫스왑, 원격 장애 진단, 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계가 있는가?
4. [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/), 이중 전원, 다중 가용영역처럼 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 제거 설계가 반영되었는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- MTBF를 보증기간이나 개별 장비 수명으로 해석하는 것
- 높은 MTBF 숫자만 믿고 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·예비 부품 확보를 생략하는 것
- 부품 MTBF만 보고 애플리케이션 수준 장애 전파를 검토하지 않는 것

📢 섹션 요약 비유: MTBF는 우산 원단이 얼마나 질긴지 알려 주는 숫자다. 하지만 폭우 속에서 진짜 중요한 것은 우산천 품질만이 아니라, 예비 우산이 있는지, 손잡이가 부러지면 바로 바꿀 수 있는지, 가족이 같은 우산 하나만 쓰고 있지는 않은지까지 함께 보는 일이다.

---

## Ⅴ. 기대효과 및 결론

MTBF를 제대로 이해하면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 감정이 아니라 확률과 운영 계획의 언어로 바꿀 수 있다. 그 결과 인프라 설계자는 예비 부품 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 유지보수 계약, 장애 대응 인력, [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 투자 우선순위를 더 합리적으로 결정할 수 있다. 즉, MTBF는 단순 통계가 아니라 비용과 안정성 사이의 균형점을 잡는 의사결정 도구다.

다만 MTBF는 어디까지나 평균값이며, 실제 장애는 사용 패턴·온도·진동·전력 품질·[펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 결함에 따라 크게 달라진다. 그래서 현대 운영은 제조사 MTBF를 출발점으로 쓰되, Self-Monitoring, Analysis and Reporting Technology인 S.M.A.R.T. 텔레메트리, 예지 정비, 장애 이력 분석으로 자사 환경의 실측 데이터를 계속 보정한다.

앞으로의 방향은 "고장을 더 늦추는 것"만이 아니라 "고장을 빨리 감지하고 우아하게 우회하는 것"에 있다. 따라서 MTBF는 <strong>장비 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>의 절대 진리</strong>가 아니라, <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 설계를 시작하게 만드는 첫 번째 숫자</strong>로 기억하는 것이 가장 정확하다.

📢 섹션 요약 비유: MTBF는 집을 튼튼하게 짓는 기준선이다. 하지만 오래 사는 비결은 벽돌 강도만이 아니라, 누수 경보기, 예비 열쇠, 빠른 수리공 연락처까지 함께 준비해 두는 데 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MTTF](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/) (Mean Time To Failure) | 수리보다 교체 중심 부품의 평균 고장 시점을 나타내며 MTBF와 자주 비교된다. |
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair) | MTBF와 결합해 실제 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 결정하는 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 지표다. |
| [RAS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/449_ras/) ([Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/), [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), Serviceability) | MTBF는 이 중 Reliability를 대표하는 입력값으로 쓰인다. |
| [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure) | 단일 장애점이 남아 있으면 높은 MTBF도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 효과가 제한된다. |
| [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) (Redundant [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks) | 낮은 개별 디스크 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 구조로 보완하는 대표 사례다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">부품 고장 통계</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">MTTF · MTBF · MTTR</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가용성 계산 · 장애 대응 시간 관리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">RAID · 이중 전원 · 클러스터 페일오버</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">예지 정비 · 텔레메트리 기반 신뢰성 운영</div>
</div>
</div>



이 흐름은 "개별 부품의 평균 고장 이해"에서 출발해 "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준의 장애 흡수 설계"로 확장되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MTBF는 장난감이 고장 나기 전까지 평균적으로 얼마나 오래 놀 수 있는지 알려 주는 숫자예요.
2. 하지만 숫자가 크다고 장난감 하나가 무조건 오래 산다는 뜻은 아니고, 장난감이 많으면 어떤 것은 더 빨리 망가질 수도 있어요.
3. 그래서 똑똑한 사람은 장난감을 튼튼하게 사는 것뿐 아니라, 고장 나면 바로 바꿀 예비품도 같이 준비해 둔답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 451 / 803

← **이전**: [449. RAS (Reliability, Availability, Serviceability)](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/449_ras/)
**다음**: [451. MTTR (평균 수리 시간)](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) →

---
