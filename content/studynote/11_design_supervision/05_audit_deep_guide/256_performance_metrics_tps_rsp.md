+++
title = "256. 성능 진단 지표 TPS/응답시간 (Performance Metrics TPS/Response Time)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 진단의 3대 지표인 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)([Response Time](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)), 동시 사용자 수(Concurrent User), [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(TPS, Transactions Per Second)은 상호 의존적이며, 하나의 최적화가 다른 지표에 영향을 준다.
> 2. **가치**: TPS가 낮고 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 길면 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))의 위치를 정확히 특정하지 않은 채 서버 증설만으로는 해결되지 않는다.
> 3. **판단 포인트**: 목표 TPS, 최대 동시 사용자 수, 허용 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)(예: 95th percentile ≤ 3초)을 사전에 정의하고 [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/) 결과와 비교하는 것이 감리의 핵심이다.

---

## Ⅰ. 개요 및 필요성
[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)([Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))은 기능 정확성과 함께 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)의 핵심 요소다. 특히 국민 다수가 사용하는 공공 포털, 행정 시스템은 특정 시점(수능 원서 접수, 재난지원금 신청 등)에 순간 급증하는 부하(Peak Load)에도 안정적으로 동작해야 한다. ISO/IEC 25010([소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/) 모델)은 [성능 효율성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/343_performance_efficiency/)([Performance Efficiency](/knowledge-base/studynote/04_software_engineering/06_software_architecture/343_performance_efficiency/))을 품질 특성으로 명시한다.

| 지표 | 영문 | 단위 | 정의 |
|:---|:---|:---|:---|
| [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | [Response Time](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | 초(sec), 밀리초(ms) | 요청 전송부터 응답 수신까지의 시간 |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | TPS (Transactions Per Second) | tps | 초당 처리 완료 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 수 |
| 동시 사용자 수 | Concurrent User | 명 | 동시에 활성 요청을 하는 사용자 수 |
| 오류율 | Error Rate | % | 전체 요청 중 오류 응답 비율 |
| 포화점 | Saturation Point | - | TPS가 더 이상 증가하지 않는 부하 수준 |

| [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 유형 | 목표 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | 비고 |
|:---|:---|:---|
| 단순 조회 | ≤ 1초 | 95th percentile |
| 복잡 조회/검색 | ≤ 3초 | 95th percentile |
| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드 | ≤ 10초 | 10MB 기준 |
| 보고서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | ≤ 30초 | 비동기 처리 권장 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Problem</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Core Idea</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Expected Gain</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)은 "음식 주문 후 첫 번째 요리가 나오는 시간"이고, TPS는 "주방에서 시간당 처리하는 주문 수"다. 손님(동시 사용자)이 많아질수록 두 지표 모두 악화된다.

---

## Ⅱ. 아키텍처 및 핵심 원리


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">성능 지표 상관관계 그래프</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TPS</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← 포화점 (Saturation Point)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ TPS 하락 (과부하)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ (선형 증가 구간)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">동시 사용자 수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">응답시간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(급격 증가)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(허용 한계 초과)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">동시 사용자 수</div></div>
</div>
</div>





<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">총 응답 시간 = 네트워크 지연 + 서버 처리 + DB 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클라이언트 WAS DB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요청(ms) 쿼리(ms)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">►</div><div class="kb-diagram-cell">►</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◄</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◄</div><div class="kb-diagram-cell">결과 반환</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">응답(ms)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분석 포인트:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">N/W 지연: 20ms (허용 기준 &lt; 50ms)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">WAS 처리: 150ms (허용 기준 &lt; 200ms)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DB 처리: 830ms ← 병목! (목표 &lt; 100ms)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">총 응답: 1,000ms</div></div>
</div>
</div>



단순 평균(Average) [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)은 실제 사용자 경험을 왜곡한다. 99%의 요청이 1초 이내이지만 1%가 30초라면 평균은 1.3초처럼 보이지만 실제로는 큰 문제다.

| 측정 방식 | 의미 | 감리 적용 |
|:---|:---|:---|
| 평균 (Average) | 전체 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 평균 | 참고용 (왜곡 가능) |
| 중앙값 (P50) | 50%의 요청이 이 시간 이내 | 일반 사용자 경험 |
| P95 | 95%의 요청이 이 시간 이내 | 표준 감리 기준 |
| P99 | 99%의 요청이 이 시간 이내 | 고품질 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기준 |
| 최대값 (Max) | 가장 느린 요청 | [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 기준 |

- **📢 섹션 요약 비유**: 평균 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)만 보는 것은 "가장 빠른 선수와 가장 느린 선수의 평균으로 팀 전체 수준을 판단"하는 것이다. P95가 실제 대부분 사용자의 경험을 반영한다.

---

## Ⅲ. 비교 및 연결
| 테스트 유형 | 목적 | 부하 패턴 | 주요 측정 지표 |
|:---|:---|:---|:---|
| [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/) ([Load Test](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/)) | 목표 부하 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 점진적 증가 | TPS, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) |
| [스트레스 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/447_stress_test/) ([Stress Test](/knowledge-base/studynote/04_software_engineering/11_testing_validation/447_stress_test/)) | 한계점(Break Point) 탐색 | 한계 초과 부하 | 포화점, 오류율 |
| [내구성 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/449_endurance_soak_test/) (Soak Test) | 장시간 운영 안정성 | 지속 부하 | [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/), TPS 변화 |
| [스파이크 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/448_spike_test/) ([Spike Test](/knowledge-base/studynote/04_software_engineering/11_testing_validation/448_spike_test/)) | 순간 급증 대응 | 급격한 피크 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 |
| 볼륨 테스트 ([Volume](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) Test) | 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 | 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 변화 |

| 도구 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 지원 | 특징 | 사용 환경 |
|:---|:---|:---|:---|
| JMeter | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), JDBC, JMS, [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), GUI | 범용 |
| Gatling | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), [WebSocket](/knowledge-base/studynote/03_network/09_application_layer_web_email/480_websocket_full_duplex/) | 코드 기반, 고성능 | 개발자 친화 |
| nGrinder | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) | NAVER 개발, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 테스트 | 국내 공공 다수 사용 |
| Locust | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) | Python 기반 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경 |
| k6 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), [WebSocket](/knowledge-base/studynote/03_network/09_application_layer_web_email/480_websocket_full_duplex/) | JS 기반, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 연동 | [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경 |

- **📢 섹션 요약 비유**: [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/)는 "실제 개업 전 친구들을 초대해 식당을 가득 채워보는 리허설"이다. 예상치 못한 병목(주방 동선)을 미리 발견하고 개선할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단
감리인은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표가 명확히 문서화되었는지 먼저 확인한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">성능 목표 정의 체크리스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 최대 동시 사용자 수: ____명</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 목표 TPS: ____tps</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 허용 응답 시간 (P95): ____초</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 목표 가용성: ____% (예: 99.9%)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 피크 부하 배수: ____배 (예: 평균의 3배)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 오류율 허용 기준: ____% 미만</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">★ 목표 미정의 시: 감리 지적 사항 (성능 목표 부재)</div></div>
</div>
</div>



| 상황 | 판단 | 조치 |
|:---|:---|:---|
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표 문서 없음 | 심각한 지적 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요건 정의서 작성 요구 |
| [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/) 미수행 | 주요 지적 | 테스트 수행 후 재감리 |
| P95 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 목표 초과 | 보완 필요 | 병목 원인 분석 및 튜닝 |
| 오류율 1% 초과 | 주요 지적 | 오류 원인 분석 필수 |
| 포화점이 목표 부하 이하 | 심각한 지적 | 아키텍처 개선 또는 증설 |

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·로그가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표 없이 시스템을 납품하는 것은 "달리기 경기에서 목표 기록 없이 출발"하는 것이다. 어디까지 빨라야 합격인지 기준이 없으면 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자체가 불가능하다.

---

## Ⅴ. 기대효과 및 결론
명확한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표(TPS, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/), 동시 사용자)를 기반으로 한 체계적 감리는 오픈 직후 발생하는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·장애를 사전 예방한다. 2021년 재난지원금 신청 시스템 마비, 2023년 수능 원서 접수 장애 등의 사례는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 감리 부재가 실제 국민 불편으로 직결됨을 보여준다. P95 기반 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 목표 관리와 사전 [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/) 수행은 공공정보화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 감리의 기본 요건이다.

확장 방향은 ① [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), ② Continuous [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/), ③ [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 감리는 "고속도로 개통 전 차량 통행 테스트"다. 실제 차가 다니기 전에 얼마나 많은 차를 동시에 처리할 수 있는지, 어디서 막히는지를 반드시 사전에 확인해야 한다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | ISO/IEC 25010 [성능 효율성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/343_performance_efficiency/) | [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/) 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 특성 |
| 상위 개념 | 비기능 요건 (Non-Functional Requirements) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표의 상위 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 하위 개념 | TPS (Transactions Per Second) | 초당 처리 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 수 |
| 하위 개념 | P95 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | 95백분위 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 기준 |
| 하위 개념 | 포화점 (Saturation Point) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계 지점 |
| 연관 개념 | 리틀의 법칙 (Little's Law) | TPS-사용자-응답시간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 공식 |
| 연관 개념 | [APM](/knowledge-base/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) ([Application Performance Management](/knowledge-base/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/)) | 실시간 [성능 모니터링](/knowledge-base/studynote/02_operating_system/10_security/609_performance_monitoring/) 도구 |

### 📈 관련 키워드 및 발전 흐름도
[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표 → [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 진단 지표 TPS/응답시간 → [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)·[APM](/knowledge-base/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) 지표

### 👶 어린이를 위한 3줄 비유 설명
1. TPS는 "피자 가게에서 한 시간에 몇 판을 만들 수 있는지"이고, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)은 "주문하고 피자를 받을 때까지 얼마나 기다리는지"야.
2. 손님이 너무 많아지면(동시 사용자 증가) 피자 굽는 속도는 그대로인데 기다리는 줄이 길어지면서 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 급격히 늘어.
3. P95는 "100명 중 95명이 이 시간 안에 피자를 받았다"는 뜻이야. 단 5명이 30분 기다려도 평균은 괜찮아 보일 수 있어서 P95가 더 정직한 기준이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 317 / 530

← **이전**: [255. 데이터 무결성 이행 감리 (Data Integrity Migration Audit)](/knowledge-base/studynote/11_design_supervision/05_audit_deep_guide/255_data_integrity_migration_audit/)
**다음**: [257. 리틀의 법칙 성능 진단 (Little's Law Performance Audit)](/knowledge-base/studynote/11_design_supervision/05_audit_deep_guide/257_littles_law_performance_audit/) →

---
