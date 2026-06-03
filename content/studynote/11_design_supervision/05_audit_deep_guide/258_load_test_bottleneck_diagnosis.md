---
title: 258. 부하 테스트 병목 진단 (Load Test Bottleneck Diagnosis)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[446_load_test|부하 테스트]]([[446_load_test|Load Test]])의 목적은 병목([[617_io_bottleneck|Bottleneck]]) 위치를 정확히 특정하는 것이며, 단순히 "느리다"는 [[396_validation|확인]]이 아닌 **CPU·메모리·디스크 I/O·네트워크** 중 어디가 포화 상태인지를 진단해야 한다.
> 2. **가치**: 병목 위치를 오판하면 비용만 낭비된다. CPU 병목인데 DB 서버를 증설하거나, [[612_memory_leak_detection|메모리 누수]]([[612_memory_leak_detection|Memory Leak]])인데 CPU를 업그레이드하는 실수가 실무에서 빈번하다.
> 3. **판단 포인트**: [[446_load_test|부하 테스트]] 중 CPU 사용률 70% 미만, 메모리 점진적 증가, 디스크 I/O Wait 20% 초과, 네트워크 [[140_bandwidth|대역폭]]([[140_bandwidth|Bandwidth]]) 70% 초과 여부를 지표별로 독립 진단한다.

---

## Ⅰ. 개요 및 필요성
[[446_load_test|부하 테스트]]([[446_load_test|Load Test]])는 시스템이 목표 부하 조건에서 [[282_performance_tactics|성능]] 목표를 달성하는지 [[395_verification_process_review|검증]]하는 테스트다. 감리 맥락에서는 단순 "테스트 수행 여부"가 아니라, 테스트 결과를 바탕으로 병목 원인이 명확히 진단되고 조치되었는지를 [[396_validation|확인]]한다.

| 병목 유형 | 증상 | 진단 도구 |
|:---|:---|:---|
| CPU 병목 | CPU 사용률 90%+, [[138_response_time|응답 시간]] 비례 증가 | top, htop, sar |
| [[612_memory_leak_detection|메모리 누수]] ([[612_memory_leak_detection|Memory Leak]]) | 메모리 사용량 지속 증가, GC 빈도 증가 | jmap, MAT, VisualVM |
| 디스크 I/O 대기 | I/O Wait 20%+, 디스크 [[138_response_time|응답 시간]] 급증 | iostat, iotop |
| 네트워크 [[140_bandwidth|대역폭]] | [[139_throughput|처리량]] 정체, 패킷 손실 증가 | iftop, nethogs, netstat |

일반적으로 부하 증가 시 병목은 다음 순서로 나타난다:
1. **애플리케이션 레이어**: 비효율 [[001_algorithm_definition|알고리즘]], 동기 블로킹 호출
2. **DB 레이어**: 슬로우 [[298_qkv_attention|쿼리]], [[154_database_index_b_tree_search_optimization|인덱스]] 미사용, 락([[510_lock|Lock]]) 경합
3. **인프라 레이어**: CPU, 메모리, 디스크, 네트워크 포화

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Problem      │──▶│ Core Idea    │──▶│ Expected Gain │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **📢 섹션 요약 비유**: 병목 진단 없는 서버 증설은 "교통 체증의 원인이 신호등인데 차선만 늘리는 것"이다. 원인을 정확히 찾아야 올바른 해결책을 적용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
┌─────────────────────────────────────────────────────────────┐
│       USE 방법론 (Utilization, Saturation, Errors)           │
│                                                             │
│  리소스   │ Utilization(사용률) │ Saturation(포화) │ Errors  │
│  ─────────┼────────────────────┼─────────────────┼──────── │
│  CPU      │ %usr + %sys        │ 런큐(run queue) │ -        │
│           │ 기준: < 70% 정상   │ > CPU 수 → 포화  │          │
│  메모리   │ Used / Total       │ 스왑(Swap) 사용 │ OOM      │
│           │ 기준: < 80% 정상   │ Swap > 0 → 포화  │          │
│  디스크   │ %iowait            │ I/O 대기 큐     │ EIO      │
│           │ 기준: < 20% 정상   │ avgqu-sz > 1    │          │
│  네트워크 │ 대역폭 사용률      │ 패킷 드롭       │ TCP 재전송 │
│           │ 기준: < 70% 정상   │ rxdrop > 0      │          │
└─────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│         메모리 누수 진단 그래프 패턴                          │
│                                                             │
│  메모리                                                      │
│  사용량                                                      │
│   ▲                                                         │
│   │               ╭──────────── OOM 위험 구간              │
│   │           ╭───╯                                         │
│   │       ╭───╯   ← 부하 테스트 중 점진적 증가               │
│   │   ╭───╯       (GC 후에도 완전히 회복 안 됨)              │
│   │ ──╯                                                     │
│   └──────────────────────────────────── 시간                │
│                                                             │
│  정상 패턴: 부하 해제 후 메모리 회복 (톱니 모양)              │
│  누수 패턴: 부하 해제 후에도 메모리 지속 증가 (우상향)         │
└─────────────────────────────────────────────────────────────┘
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
| [[395_verification_process_review|검증]] 포인트 | 테스트·[[568_logs_distributed_logging_elk_fluentd|로그]]·모니터링으로 [[396_validation|확인]]할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: USE 방법론은 "차량 점검 항목표"와 같다. 엔진(CPU), 연료(메모리), 타이어(디스크), 도로(네트워크) 각각을 사용률→포화→오류 순서로 점검한다.

---

## Ⅲ. 비교 및 연결
| 병목 유형 | 주요 증상 | 오진 사례 | 올바른 조치 |
|:---|:---|:---|:---|
| CPU 병목 | CPU 90%+, [[138_response_time|응답 시간]] 선형 증가 | DB 서버 증설 | CPU 스케일업 또는 [[001_algorithm_definition|알고리즘]] 최적화 |
| [[612_memory_leak_detection|메모리 누수]] | 메모리 점진 증가, [[157_oom_killer|OOM]] 킬러 | 서버 재시작만 반복 | 힙 덤프 분석 후 코드 수정 |
| 디스크 I/O | I/O Wait 20%+, DB 응답 느림 | WAS 서버 증설 | [[327_ssd|SSD]] 교체, [[298_qkv_attention|쿼리]] 최적화, 캐시 도입 |
| 네트워크 | TPS 정체, 패킷 손실 | WAS [[103_thread_pool|스레드 풀]] 증가 | [[140_bandwidth|대역폭]] 증설, [[506_cdn_content_delivery_network_edge_caching|CDN]] 도입 |
| DB [[275_lock_contention_monitoring|락 경합]] | 특정 요청만 느림, [[089_wait_queue|대기 큐]] 증가 | CPU 업그레이드 | [[191_transaction_concept_states|트랜잭션]] 분리, [[154_database_index_b_tree_search_optimization|인덱스]] 최적화 |

| 도구 조합 | 역할 | 병목 유형 |
|:---|:---|:---|
| JMeter + [[255_time_series_rollup_retention_compression|InfluxDB]] + [[168_grafana|Grafana]] | 부하 발생 + 시계열 저장 + [[003_bigdata_7v|시각화]] | 전체 |
| nGrinder + [[136_prometheus|Prometheus]] | [[136_variance|분산]] 부하 + [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집 | 전체 |
| [[162_apm_application_performance_management|APM]] (Jennifer, Scouter) | [[191_transaction_concept_states|트랜잭션]] 추적, 메서드 [[613_profiling_gprof|프로파일링]] | CPU, DB |
| jmap + Eclipse MAT | 힙 덤프 분석 | [[612_memory_leak_detection|메모리 누수]] |
| iostat + iotop | 디스크 I/O 상세 분석 | 디스크 I/O |

- **📢 섹션 요약 비유**: 병목 진단 도구 조합은 "종합 건강검진 패키지"다. 혈압계(CPU), MRI(메모리), X-ray(디스크), 심전도(네트워크) 각각의 전문 장비가 있어야 정확한 진단이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단
| 점검 항목 | [[396_validation|확인]] 방법 | 판정 기준 |
|:---|:---|:---|
| 부하 [[442_test_scenario|테스트 시나리오]] 적절성 | 테스트 계획서 [[396_validation|확인]] | 실제 업무 패턴 반영 |
| 목표 TPS 달성 여부 | 테스트 결과 리포트 | 목표 TPS 이상 |
| 병목 원인 분석 보고서 | 증빙 문서 [[396_validation|확인]] | 리소스별 지표 포함 |
| CPU 사용률 | 테스트 중 모니터링 [[568_logs_distributed_logging_elk_fluentd|로그]] | 최대 70% 이하 |
| [[612_memory_leak_detection|메모리 누수]] 여부 | 8시간 [[449_endurance_soak_test|내구성 테스트]] 결과 | 메모리 우상향 없음 |
| I/O Wait | iostat [[568_logs_distributed_logging_elk_fluentd|로그]] | 20% 미만 |
| 조치 완료 여부 | 재테스트 결과 | 목표치 달성 |

```
힙 덤프 수집 → Eclipse MAT / VisualVM 분석
→ 가장 많은 메모리 점유 객체 확인
→ 참조(Reference) 체인 추적
→ 누수 원인 코드 수정
  (예: static 컬렉션에 계속 추가, 이벤트 리스너 해제 미처리)
→ 수정 후 재테스트
```

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·[[568_logs_distributed_logging_elk_fluentd|로그]]가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: 힙 덤프 분석은 "쓰레기통에서 무엇이 가득 차 있는지 [[396_validation|확인]]"하는 것이다. 가득 찬 쓰레기([[612_memory_leak_detection|메모리 누수]] 객체)를 찾아 버리는 코드를 추가하면 문제가 해결된다.

---

## Ⅴ. 기대효과 및 결론
체계적인 병목 진단은 불필요한 인프라 비용 낭비를 방지하고 실제 [[282_performance_tactics|성능]] 문제를 정확히 해결한다. [[612_memory_leak_detection|메모리 누수]]는 방치 시 주기적인 [[090_service_kubernetes_network_load_balancing|서비스]] 재시작 조치로 임시 대응하게 되고, 결국 심야 장애로 이어진다. I/O Wait 20% 이상은 아무리 CPU를 증설해도 해결되지 않으며, 반드시 디스크 I/O 최적화([[456_caching|캐싱]], [[327_ssd|SSD]] 전환, [[298_qkv_attention|쿼리]] 최적화)가 필요하다. 감리인은 4대 리소스를 독립적으로 진단하고 각각의 기준치를 적용해야 한다.

확장 방향은 ① [[164_policy|Policy]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]], ② Continuous [[363_audit|Audit]], ③ [[231_ai_turing_test|인공지능]]([[190_ai_llm_requirements_specification|AI]], [[001_artificial_intelligence|Artificial Intelligence]]) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: [[446_load_test|부하 테스트]] 병목 감리는 "운동선수의 신체 검사"다. 심폐 기능(CPU), 체지방(메모리), 관절(디스크), 순환계(네트워크) 중 어디가 약한지를 정확히 찾아야 올바른 훈련 처방이 나온다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [[445_performance_test_types|성능 테스트]] ([[445_performance_test_types|Performance Test]]) | [[446_load_test|부하 테스트]]의 상위 범주 |
| 상위 개념 | USE 방법론 | 리소스 진단 프레임워크 |
| 하위 개념 | [[612_memory_leak_detection|메모리 누수]] ([[612_memory_leak_detection|Memory Leak]]) | 힙 덤프 분석으로 진단 |
| 하위 개념 | I/O Wait | 디스크 I/O 병목 핵심 지표 |
| 하위 개념 | 네트워크 [[140_bandwidth|대역폭]] ([[140_bandwidth|Bandwidth]]) | 네트워크 병목 핵심 지표 |
| 연관 개념 | [[162_apm_application_performance_management|APM]] ([[162_apm_application_performance_management|Application Performance Management]]) | 병목 위치 실시간 추적 도구 |
| 연관 개념 | GC ([[380_garbage_collection|Garbage Collection]]) | [[612_memory_leak_detection|메모리 누수]] 진단의 선행 지표 |

### 📈 관련 키워드 및 발전 흐름도
부하 시나리오 → [[446_load_test|부하 테스트]] 병목 진단 → 원인별 튜닝·재시험

### 👶 어린이를 위한 3줄 비유 설명
1. 컴퓨터가 느려질 때는 원인이 CPU(두뇌), 메모리(책상), 디스크(책장), 네트워크(도로) 중 하나인데, 어디가 막혔는지 정확히 찾아야 해.
2. [[612_memory_leak_detection|메모리 누수]]는 "책을 계속 꺼내서 보고 다시 꽂지 않아서 책상이 꽉 차버리는 것"처럼 프로그램이 메모리를 쓰고 돌려주지 않는 거야.
3. 병목을 잘못 진단해서 엉뚱한 곳을 고치면 돈만 쓰고 문제가 해결이 안 되니까, 정확한 진단이 치료보다 더 중요해.
