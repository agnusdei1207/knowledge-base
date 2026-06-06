---
title: "Load Test Bottleneck Diagnosis"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/)([Load Test](/studynote/04_software_engineering/11_testing_validation/838_load_test/))의 목적은 병목([Bottleneck](/studynote/02_operating_system/10_security/617_io_bottleneck/)) 위치를 정확히 특정하는 것이며, 단순히 "느리다"는 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 아닌 **CPU·메모리·디스크 I/O·네트워크** 중 어디가 포화 상태인지를 진단해야 한다.
> 2. **가치**: 병목 위치를 오판하면 비용만 낭비된다. CPU 병목인데 DB 서버를 증설하거나, [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/)([Memory Leak](/studynote/02_operating_system/10_security/612_memory_leak_detection/))인데 CPU를 업그레이드하는 실수가 실무에서 빈번하다.
> 3. **판단 포인트**: [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/) 중 CPU 사용률 70% 미만, 메모리 점진적 증가, 디스크 I/O Wait 20% 초과, 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Bandwidth](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) 70% 초과 여부를 지표별로 독립 진단한다.

---

## Ⅰ. 개요 및 필요성
[부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/)([Load Test](/studynote/04_software_engineering/11_testing_validation/838_load_test/))는 시스템이 목표 부하 조건에서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표를 달성하는지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 테스트다. 감리 맥락에서는 단순 "테스트 수행 여부"가 아니라, 테스트 결과를 바탕으로 병목 원인이 명확히 진단되고 조치되었는지를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

| 병목 유형 | 증상 | 진단 도구 |
|:---|:---|:---|
| CPU 병목 | CPU 사용률 90%+, [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 비례 증가 | top, htop, sar |
| [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) ([Memory Leak](/studynote/02_operating_system/10_security/612_memory_leak_detection/)) | 메모리 사용량 지속 증가, GC 빈도 증가 | jmap, MAT, VisualVM |
| 디스크 I/O 대기 | I/O Wait 20%+, 디스크 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 급증 | iostat, iotop |
| 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 정체, 패킷 손실 증가 | iftop, nethogs, netstat |

일반적으로 부하 증가 시 병목은 다음 순서로 나타난다:
1. **애플리케이션 레이어**: 비효율 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 동기 블로킹 호출
2. **DB 레이어**: 슬로우 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 미사용, 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합
3. **인프라 레이어**: CPU, 메모리, 디스크, 네트워크 포화

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 병목 진단 없는 서버 증설은 "교통 체증의 원인이 신호등인데 차선만 늘리는 것"이다. 원인을 정확히 찾아야 올바른 해결책을 적용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-------------------------------------------------------------+
|       USE 방법론 (Utilization, Saturation, Errors)           |
|                                                             |
|  리소스   | Utilization(사용률) | Saturation(포화) | Errors  |
|  ---------+--------------------+-----------------+-------- |
|  CPU      | %usr + %sys        | 런큐(run queue) | -        |
|           | 기준: < 70% 정상   | > CPU 수 -> 포화  |          |
|  메모리   | Used / Total       | 스왑(Swap) 사용 | OOM      |
|           | 기준: < 80% 정상   | Swap > 0 -> 포화  |          |
|  디스크   | %iowait            | I/O 대기 큐     | EIO      |
|           | 기준: < 20% 정상   | avgqu-sz > 1    |          |
|  네트워크 | 대역폭 사용률      | 패킷 드롭       | TCP 재전송 |
|           | 기준: < 70% 정상   | rxdrop > 0      |          |
+-------------------------------------------------------------+
```

```
+-------------------------------------------------------------+
|         메모리 누수 진단 그래프 패턴                          |
|                                                             |
|  메모리                                                      |
|  사용량                                                      |
|   ^                                                         |
|   |               +------------ OOM 위험 구간              |
|   |           +---+                                         |
|   |       +---+   <- 부하 테스트 중 점진적 증가               |
|   |   +---+       (GC 후에도 완전히 회복 안 됨)              |
|   | --+                                                     |
|   +------------------------------------ 시간                |
|                                                             |
|  정상 패턴: 부하 해제 후 메모리 회복 (톱니 모양)              |
|  누수 패턴: 부하 해제 후에도 메모리 지속 증가 (우상향)         |
+-------------------------------------------------------------+
```

```
# CPU 병목 진단
$ top -d 1                          # CPU 사용률 실시간 확인
$ sar -u 1 10                       # 10회 1초 간격 CPU 통계
$ jstack <PID> | grep BLOCKED       # Java 스레드 블로킹 확인

# 메모리 누수 진단
$ jmap -heap <PID>                  # JVM 힙 메모리 통계
$ jmap -dump:format=b,file=heap.hprof <PID>  # 힙 덤프 생성
$ free -m                           # 전체 메모리 현황

# 디스크 I/O 병목 진단
$ iostat -xz 1                      # 디스크 I/O 통계 (1초 간격)
$ iotop                             # 프로세스별 I/O 사용량

# 네트워크 대역폭 진단
$ iftop -i eth0                     # 인터페이스별 대역폭
$ netstat -s | grep retransmit      # TCP 재전송 수
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: USE 방법론은 "차량 점검 항목표"와 같다. 엔진(CPU), 연료(메모리), 타이어(디스크), 도로(네트워크) 각각을 사용률->포화->오류 순서로 점검한다.

---

## Ⅲ. 비교 및 연결
| 병목 유형 | 주요 증상 | 오진 사례 | 올바른 조치 |
|:---|:---|:---|:---|
| CPU 병목 | CPU 90%+, [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 선형 증가 | DB 서버 증설 | CPU 스케일업 또는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 최적화 |
| [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) | 메모리 점진 증가, [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 | 서버 재시작만 반복 | 힙 덤프 분석 후 코드 수정 |
| 디스크 I/O | I/O Wait 20%+, DB 응답 느림 | WAS 서버 증설 | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 교체, [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화, 캐시 도입 |
| 네트워크 | TPS 정체, 패킷 손실 | WAS [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/) 증가 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 증설, [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 도입 |
| DB [락 경합](/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/) | 특정 요청만 느림, [대기 큐](/studynote/02_operating_system/02_process_thread/089_wait_queue/) 증가 | CPU 업그레이드 | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 분리, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 최적화 |

| 도구 조합 | 역할 | 병목 유형 |
|:---|:---|:---|
| JMeter + [InfluxDB](/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) + [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/) | 부하 발생 + 시계열 저장 + [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 전체 |
| nGrinder + [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 부하 + [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집 | 전체 |
| [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) (Jennifer, Scouter) | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 추적, 메서드 [프로파일링](/studynote/02_operating_system/10_security/613_profiling_gprof/) | CPU, DB |
| jmap + Eclipse MAT | 힙 덤프 분석 | [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) |
| iostat + iotop | 디스크 I/O 상세 분석 | 디스크 I/O |

- **📢 섹션 요약 비유**: 병목 진단 도구 조합은 "종합 건강검진 패키지"다. 혈압계(CPU), MRI(메모리), X-ray(디스크), 심전도(네트워크) 각각의 전문 장비가 있어야 정확한 진단이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단
| 점검 항목 | [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 방법 | 판정 기준 |
|:---|:---|:---|
| 부하 [테스트 시나리오](/studynote/04_software_engineering/11_testing_validation/834_test_scenario/) 적절성 | 테스트 계획서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 실제 업무 패턴 반영 |
| 목표 TPS 달성 여부 | 테스트 결과 리포트 | 목표 TPS 이상 |
| 병목 원인 분석 보고서 | 증빙 문서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 리소스별 지표 포함 |
| CPU 사용률 | 테스트 중 모니터링 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 최대 70% 이하 |
| [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) 여부 | 8시간 [내구성 테스트](/studynote/04_software_engineering/11_testing_validation/841_endurance_soak_test/) 결과 | 메모리 우상향 없음 |
| I/O Wait | iostat [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 20% 미만 |
| 조치 완료 여부 | 재테스트 결과 | 목표치 달성 |

```
힙 덤프 수집 -> Eclipse MAT / VisualVM 분석
-> 가장 많은 메모리 점유 객체 확인
-> 참조(Reference) 체인 추적
-> 누수 원인 코드 수정
  (예: static 컬렉션에 계속 추가, 이벤트 리스너 해제 미처리)
-> 수정 후 재테스트
```

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: 힙 덤프 분석은 "쓰레기통에서 무엇이 가득 차 있는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"하는 것이다. 가득 찬 쓰레기([메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) 객체)를 찾아 버리는 코드를 추가하면 문제가 해결된다.

---

## Ⅴ. 기대효과 및 결론
체계적인 병목 진단은 불필요한 인프라 비용 낭비를 방지하고 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 정확히 해결한다. [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/)는 방치 시 주기적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재시작 조치로 임시 대응하게 되고, 결국 심야 장애로 이어진다. I/O Wait 20% 이상은 아무리 CPU를 증설해도 해결되지 않으며, 반드시 디스크 I/O 최적화([캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전환, [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화)가 필요하다. 감리인은 4대 리소스를 독립적으로 진단하고 각각의 기준치를 적용해야 한다.

확장 방향은 ① [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), ② Continuous [Audit](/studynote/12_it_management/05_security_compliance/363_audit/), ③ [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/) 병목 감리는 "운동선수의 신체 검사"다. 심폐 기능(CPU), 체지방(메모리), 관절(디스크), 순환계(네트워크) 중 어디가 약한지를 정확히 찾아야 올바른 훈련 처방이 나온다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [성능 테스트](/studynote/04_software_engineering/11_testing_validation/837_performance_test_types/) ([Performance Test](/studynote/04_software_engineering/11_testing_validation/837_performance_test_types/)) | [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/)의 상위 범주 |
| 상위 개념 | USE 방법론 | 리소스 진단 프레임워크 |
| 하위 개념 | [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) ([Memory Leak](/studynote/02_operating_system/10_security/612_memory_leak_detection/)) | 힙 덤프 분석으로 진단 |
| 하위 개념 | I/O Wait | 디스크 I/O 병목 핵심 지표 |
| 하위 개념 | 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) ([Bandwidth](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) | 네트워크 병목 핵심 지표 |
| 연관 개념 | [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) ([Application Performance Management](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/)) | 병목 위치 실시간 추적 도구 |
| 연관 개념 | GC ([Garbage Collection](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)) | [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) 진단의 선행 지표 |

### 📈 관련 키워드 및 발전 흐름도
부하 시나리오 -> [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/) 병목 진단 -> 원인별 튜닝·재시험

### 👶 어린이를 위한 3줄 비유 설명
1. 컴퓨터가 느려질 때는 원인이 CPU(두뇌), 메모리(책상), 디스크(책장), 네트워크(도로) 중 하나인데, 어디가 막혔는지 정확히 찾아야 해.
2. [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/)는 "책을 계속 꺼내서 보고 다시 꽂지 않아서 책상이 꽉 차버리는 것"처럼 프로그램이 메모리를 쓰고 돌려주지 않는 거야.
3. 병목을 잘못 진단해서 엉뚱한 곳을 고치면 돈만 쓰고 문제가 해결이 안 되니까, 정확한 진단이 치료보다 더 중요해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 319 / 530

<- **이전**: [257. 리틀의 법칙 성능 진단 (Little's Law Performance Audit)](/studynote/11_design_supervision/05_audit_deep_guide/257_littles_law_performance_audit/)
**다음**: [259. APM 모니터링 감리 (APM Monitoring Audit)](/studynote/11_design_supervision/05_audit_deep_guide/259_apm_monitoring_audit/) ->

---
