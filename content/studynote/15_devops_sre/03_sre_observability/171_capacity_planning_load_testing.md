---
title: 171. 용량 계획 및 부하 테스트 (Capacity Planning/Load Testing)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 용량 계획 (Capacity Planning)은 미래 수요를 견딜 자원 규모를 미리 계산하는 일이고, [[446_load_test|부하 테스트]] ([[267_load_testing_ci_jmeter_k6|Load Testing]])는 그 계산이 실제 시스템에서 성립하는지 [[395_verification_process_review|검증]]하는 실험이다.
> 2. **가치**: 둘이 함께 있어야 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 ([[123_slo_service_level_objective|Service Level Objective]], [[181_slo_service_level_objective|SLO]])를 지키면서도 과잉 증설과 장애 위험을 동시에 줄일 수 있다.
> 3. **판단 포인트**: 핵심 결과는 "최대 Requests Per Second (RPS)가 얼마인가"보다 "어느 계층이 먼저 포화되고, 무릎점 이전에 어느 정도 여유를 남겨야 하는가"를 찾는 데 있다.

---

## Ⅰ. 개요 및 필요성

용량 계획은 평균 트래픽을 보는 일이 아니라, 사업 이벤트와 장애 재시도까지 포함해 **미래의 피크 수요를 견딜 수 있는지**를 따지는 작업이다. 반면 [[446_load_test|부하 테스트]]는 가상 사용자를 발생시켜 [[138_response_time|응답 시간]], 오류율, 자원 사용률이 어떻게 변하는지 실측하는 과정이다. 하나만 있으면 절반짜리다. 계획만 있고 [[395_verification_process_review|검증]]이 없으면 엑셀 상의 자신감에 그치고, 테스트만 있고 계획이 없으면 어떤 수준까지 대비해야 하는지 기준이 없다.

특히 [[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]] ([[100_sre_site_reliability_engineering_error_budget|SRE]]) 환경에서는 평균값이 거의 의미가 없다. 전자상거래 할인 시작 5분, 방송 직후 [[568_logs_distributed_logging_elk_fluentd|로그]]인 몰림, 재시도 폭주, 배치 작업 겹침처럼 실제 장애는 대부분 짧은 피크 구간에서 일어난다. 따라서 용량 계획은 평균 Central Processing Unit (CPU) 사용률이 아니라 피크 [[014_concurrency|동시성]], 읽기/[[289_cqrs_db|쓰기]] 비율, 캐시 [[264_hit_ratio|적중률]], 외부 [[014_api_posix|Application Programming Interface]] ([[014_api_posix|API]]) 한도까지 함께 모델링해야 한다.

```text
┌──────────────────────────────────────────────────────────────┐
│          평균이 아니라 피크와 회복시간이 시스템을 결정한다    │
├──────────────────────────────────────────────────────────────┤
│ 일평균:        1,000 RPS                                     │
│ 이벤트 피크:   6,000 RPS                                     │
│ 재시도 폭주:   9,000 RPS                                     │
│ 외형상 평온해도, 실제 장애는 짧은 포화 구간에서 발생         │
└──────────────────────────────────────────────────────────────┘
```

그래서 용량 계획과 [[446_load_test|부하 테스트]]는 운영 안정성의 앞뒤 절반이다. 계획은 얼마를 준비할지 정하고, 테스트는 그 준비가 어느 계층에서 무너지는지 보여 준다. 둘이 연결되어야만 "왜 이 정도 자원이 필요한가"를 기술적·사업적으로 설명할 수 있다.

- **📢 섹션 요약 비유**: 용량 계획은 소풍에 몇 명이 올지 보고 도시락 수를 계산하는 일이고, [[446_load_test|부하 테스트]]는 실제로 그 도시락 배급 줄이 막히지 않는지 미리 연습해 보는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 용량 계획은 단일 서버 스펙이 아니라 요청이 지나가는 전체 경로를 모델링한다. 사용자는 Content Delivery Network ([[506_cdn_content_delivery_network_edge_caching|CDN]]), [[031_load_balancer|Load Balancer]], 애플리케이션, 캐시, [[002_database_definition|데이터베이스]], 외부 API를 거치며, 가장 느린 한 지점이 전체 [[139_throughput|처리량]]을 결정한다. 따라서 CPU만 여유 있다고 안심할 수 없고, [[002_database_definition|데이터베이스]] 연결 수나 외부 호출 제한이 먼저 병목이 될 수 있다.

```text
┌────────────────────────────────────────────────────────────────────┐
│               Capacity Model: 수요가 병목을 통과하는 경로          │
├────────────────────────────────────────────────────────────────────┤
│ Users → CDN → Load Balancer → App                                │
│                                ├─ Cache (hit ratio)              │
│                                ├─ Database (conn pool)           │
│                                └─ External API (rate limit)      │
│                                                                    │
│ 병목 후보: worker 수 · queue depth · slow query · timeout         │
│ 가장 먼저 포화되는 지점 = 실제 시스템 처리량의 상한                │
└────────────────────────────────────────────────────────────────────┘
```

용량 계산의 기본은 [[014_concurrency|동시성]] 모델이다. Little's Law에 따라 대략 `동시 요청 수 ≈ 처리량 × 응답 시간`으로 볼 수 있다. 예를 들어 2,000 RPS를 처리하면서 평균 [[138_response_time|응답 시간]]이 0.2초라면, 동시에 떠 있는 요청은 약 400개다. 이 값은 워커 수, [[103_thread_pool|스레드 풀]], [[002_database_definition|데이터베이스]] 연결 수를 잡는 데 직접적인 [[167_sql_hint_optimizer_override|힌트]]가 된다.

| 입력 변수 | 왜 중요한가 | 대표 측정 항목 |
| :--- | :--- | :--- |
| 피크 RPS | 순간 [[139_throughput|처리량]] 상한 예측 | 초당 요청 수, [[344_bus|버스]]트 폭 |
| 동시 사용자 수 | [[160_session_controlling_terminal|세션]]·커넥션·워커 계산 | [[483_active_vs_passive_ftp|active]] users, in-flight requests |
| 요청 혼합비 | 읽기/[[289_cqrs_db|쓰기]]/배치 비율이 병목을 바꿈 | read/write ratio, endpoint mix |
| [[001_dikw_pyramid|데이터]] 크기 | [[149_serial_communication_rs232_rs485|직렬]]화, 네트워크, 디스크 부하 영향 | payload size, row count |
| 캐시 [[264_hit_ratio|적중률]] | [[002_database_definition|데이터베이스]] 부하를 크게 좌우 | cache [[359_effective_access_time|hit ratio]] |
| 외부 의존성 한도 | 내부가 여유여도 전체 상한이 될 수 있음 | rate limit, [[319_timeout_prevention|timeout]], [[551_quota_disk_limit|quota]] |

핵심 원리는 간단하다. **수요를 수치화하고, 병목을 찾고, 여유 폭을 남긴다**. [[446_load_test|부하 테스트]]는 이 과정을 [[395_verification_process_review|검증]]하는 도구이며, 단순히 "잘 버텼다"보다 어느 지점에서 [[015_지연_데이터_관점|지연]]시간이 급증하기 시작하는지, 오토스케일링이 따라붙기 전에 얼마나 버티는지를 보는 데 의미가 있다.

- **📢 섹션 요약 비유**: 용량 모델은 고속도로 전체를 보는 교통 지도와 같다. 입구 차선, 톨게이트, 터널, 출구 중 한 곳만 막혀도 전체 속도가 떨어지듯, 시스템도 가장 약한 지점이 전체 [[139_throughput|처리량]]을 정한다.

---

## Ⅲ. 비교 및 연결

[[446_load_test|부하 테스트]]는 하나의 종류가 아니라 질문별로 다른 실험 세트다. 일반 [[446_load_test|부하 테스트]]는 정상 운영 범위에서 [[282_performance_tactics|성능]]을 재고, [[447_stress_test|스트레스 테스트]]는 무너지는 지점을 찾고, [[448_spike_test|스파이크 테스트]]는 급격한 폭증 대응력을 [[396_validation|확인]]하고, 소크 테스트는 장시간 누적 문제를 찾는다. 어떤 테스트를 해야 하는지는 [[090_service_kubernetes_network_load_balancing|서비스]] 특성과 장애 가설에 따라 달라진다.

| 테스트 유형 | 핵심 질문 | 주로 찾는 문제 |
| :--- | :--- | :--- |
| [[446_load_test|Load Test]] | 예상 정상 피크에서 SLO를 지키는가 | 평균 [[282_performance_tactics|성능]] 부족 |
| [[447_stress_test|Stress Test]] | 어디서부터 급격히 무너지는가 | 포화점, 한계 [[139_throughput|처리량]] |
| [[448_spike_test|Spike Test]] | 순간 폭증을 흡수하는가 | 큐 적체, 오토스케일 [[015_지연_데이터_관점|지연]] |
| Soak Test | 오래 돌리면 새는 곳이 있는가 | [[612_memory_leak_detection|메모리 누수]], 핸들 고갈 |

아래 곡선에서 중요한 것은 절대 최대점보다 **무릎점 (Knee Point)**이다. 그 이전까지는 부하 증가에 비례해 [[282_performance_tactics|성능]]이 완만하게 나빠지지만, 무릎점을 넘으면 [[015_지연_데이터_관점|지연]]시간과 오류율이 급격히 악화된다. 운영 기준은 보통 이 지점보다 충분히 낮은 곳에 잡는다.

```text
99th Percentile Latency
^
│                               포화 구간
│                            /
│                         __/
│                      __/
│                   __/
│__________________/____________________________> RPS
                  ^
                무릎점
```

이 결과는 오토스케일링, 캐시 [[268_strategy_pattern|전략]], [[002_database_definition|데이터베이스]] [[280_sharding|샤딩]], 큐잉 설계와 직결된다. 예를 들어 무릎점이 애플리케이션 CPU가 아니라 [[002_database_definition|데이터베이스]] 연결 풀에서 나타난다면, [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수를 늘려도 전체 [[282_performance_tactics|성능]]은 좋아지지 않는다. 즉 [[446_load_test|부하 테스트]]는 "서버를 더 사자"가 아니라 **어디를 바꿔야 하는가**를 알려 주는 진단 도구다.

- **📢 섹션 요약 비유**: 무릎점은 풍선을 불다가 갑자기 빵 터질 위험이 커지는 지점과 같다. 그 직전까지는 조금씩 커지지만, 그 선을 넘으면 작은 힘에도 급격히 문제가 생긴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 테스트 도구를 고르는 것보다 시나리오를 제대로 만드는 일이 더 중요하다. 프로덕션보다 작은 [[001_dikw_pyramid|데이터]]셋, 항상 따뜻한 캐시, 단일 API만 반복 호출하는 스크립트로는 진짜 병목을 찾기 어렵다. 용량 계획과 [[446_load_test|부하 테스트]]는 "현실을 얼마나 닮았는가"가 결과 품질을 결정한다.

| 판단 상황 | 권장 기준 | 이유 |
| :--- | :--- | :--- |
| 이벤트 대비 증설 | 예상 피크 + 안전 여유 + 스케일 [[015_지연_데이터_관점|지연]] 고려 | 순간 폭증은 평균보다 훨씬 위험하다 |
| 운영 상한 결정 | 무릎점보다 낮은 구간에 정상 운영선 [[009_config|설정]] | 포화 직전 운전은 작은 변동에도 취약하다 |
| 오토스케일 활용 | [[202_scale_out_distributed_horizontal_expansion|Scale-out]] 시간까지 버틸 버퍼 확보 | 확장 결정과 실제 기동 사이에 [[015_지연_데이터_관점|지연]]이 있다 |
| [[002_database_definition|데이터베이스]] 병목 | [[139_throughput|처리량]]보다 연결 수, [[510_lock|lock]], slow query 함께 [[396_validation|확인]] | 앱 서버 증설만으로 해결되지 않는다 |
| 외부 [[014_api_posix|API]] 의존 | 자체 [[282_performance_tactics|성능]]과 별개로 [[551_quota_disk_limit|quota]]·[[319_timeout_prevention|timeout]] 별도 [[395_verification_process_review|검증]] | [[385_third_party_cookie_deprecation_cdw|서드파티]] 한도가 전체 [[090_service_kubernetes_network_load_balancing|서비스]] 상한이 된다 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[181_slo_service_level_objective|SLO]] 기준을 먼저 확정한다. 예: `99th percentile (P99) < 500ms`, `오류율 < 1%`.
2. 대표 사용자 여정별로 요청 혼합비를 만든다. [[568_logs_distributed_logging_elk_fluentd|로그]]인, 조회, 결제, 배치가 섞여야 실제와 닮는다.
3. [[459_dummy_test_double|더미]] [[001_dikw_pyramid|데이터]] 크기와 [[154_database_index_b_tree_search_optimization|인덱스]] 상태를 프로덕션에 가깝게 맞춘다.
4. 캐시가 따뜻할 때와 차가울 때를 나누어 측정한다.
5. CPU, 메모리뿐 아니라 [[058_queue|queue]] depth, [[002_database_definition|데이터베이스]] 연결 수, [[380_garbage_collection|garbage collection]], external timeout을 함께 본다.
6. 테스트 종료 후 "최대치"보다 먼저 포화된 자원을 기준으로 개선 우선순위를 정한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 평균 레이턴시만 보고 상위 백분위 [[015_지연_데이터_관점|지연]]시간을 무시하기
- 읽기 [[014_api_posix|API]] 하나만 때려 놓고 전체 [[090_service_kubernetes_network_load_balancing|서비스]] 용량이라고 착각하기
- 프로덕션보다 훨씬 작은 [[001_dikw_pyramid|데이터]]셋으로 테스트하기
- 배치 작업, 재시도, 장애 [[658_ir_recovery|복구]] 트래픽을 제외하고 계획 세우기
- 오토스케일링이 있으니 용량 계획은 필요 없다고 생각하기

기술사 답안에서는 **수요 예측 → workload 모델 → [[446_load_test|부하 테스트]] → 병목 분석 → 개선 및 재검증** 흐름으로 정리하면 [[369_logic_bomb|논리]]성이 높다. 클라우드는 자원을 빨리 빌려줄 수는 있어도, 갑자기 나타나는 병목을 대신 설계해 주지는 않는다.

- **📢 섹션 요약 비유**: [[446_load_test|부하 테스트]] 실무는 공연 전 리허설과 같다. 무대 크기만 보는 것이 아니라, 배우 동선이 겹치는지, 조명이 늦게 켜지는지, 출입구가 막히는지까지 실제처럼 [[396_validation|확인]]해야 본 공연에서 사고가 없다.

---

## Ⅴ. 기대효과 및 결론

용량 계획과 [[446_load_test|부하 테스트]]가 정착되면 [[090_service_kubernetes_network_load_balancing|서비스]]는 "문제가 생기면 늘린다"에서 "문제가 생기기 전에 한계를 안다"로 바뀐다. 이는 장애 예방뿐 아니라 비용 최적화에도 중요하다. 실제 무릎점과 여유 폭을 알면 과도한 오버프로비저닝을 줄이면서도 피크 대응력을 유지할 수 있기 때문이다.

물론 한계는 있다. 테스트 환경이 프로덕션과 다르면 결과 [[085_confidence_association_rule_conditional_probability|신뢰도]]가 낮아지고, 이벤트 트래픽의 사회적 변수까지 완벽히 예측할 수는 없다. 또한 [[446_load_test|부하 테스트]]가 성공했다고 해서 모든 장애를 막는 것도 아니다. 배포 버그, 외부 [[090_service_kubernetes_network_load_balancing|서비스]] 장애, 지역 단위 네트워크 문제는 별도의 [[233_recovery_database_restoration_overview|회복]] 설계가 필요하다.

그래도 기억해야 할 핵심은 분명하다. **용량 계획은 숫자를 맞추는 일이 아니라, [[090_service_kubernetes_network_load_balancing|서비스]]가 어디서 느려지고 어디서 무너지는지 미리 알아내는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 공학**이다. 좋은 [[100_sre_site_reliability_engineering_error_budget|SRE]] 조직은 서버 수를 외우는 팀이 아니라, 한계와 여유를 계측해 설명할 수 있는 팀이다.

- **📢 섹션 요약 비유**: 용량 계획과 [[446_load_test|부하 테스트]]는 다리 건설 전 하중 실험과 같다. 몇 톤까지 버티는지 모르고 차를 올리는 것보다, 어디서 흔들리고 어느 정도 여유가 있는지 미리 알아 두는 편이 훨씬 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[181_slo_service_level_objective|SLO]] | [[282_performance_tactics|성능]]과 오류율의 목표선, 용량 계획의 품질 기준 |
| Little's Law | [[014_concurrency|동시성]] 추정과 워커·연결 수 계산의 기본 공식 |
| Knee Point | [[015_지연_데이터_관점|지연]]시간이 급증하기 시작하는 운영 한계선 |
| Autoscaling | 용량 계획을 보완하지만, 반응 [[015_지연_데이터_관점|지연]] 때문에 단독 해법은 아님 |
| Soak Test | 장시간 누적 부하로 [[612_memory_leak_detection|메모리 누수]]와 핸들 고갈을 찾는 실험 |
| [[617_io_bottleneck|Bottleneck]] Analysis | CPU, DB, [[058_queue|Queue]], External [[014_api_posix|API]] 중 실제 한계 지점을 찾는 과정 |

### 📈 관련 키워드 및 발전 흐름도

```text
과거 트래픽 · 사업 이벤트 예측
    │
    ▼
Workload Model (RPS · 동시성 · 요청 혼합비)
    │
    ▼
Load / Stress / Spike / Soak Test
    │
    ▼
Knee Point · Bottleneck 발견
    │
    ▼
Scale Strategy · Tuning · 재검증
```

이 흐름은 [[094_capacity_management|용량 관리]]가 단발성 장비 구매가 아니라, 예측과 실험을 반복하는 지속적 운영 활동임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 용량 계획은 운동장에 몇 명이 몰려올지 미리 세어 보고 문을 몇 개 열지 정하는 일이에요.
2. [[446_load_test|부하 테스트]]는 친구들을 미리 불러서 진짜로 줄을 세워 보고 어디가 막히는지 [[396_validation|확인]]하는 일이에요.
3. 그래서 행사 날 사람이 많이 와도 다 같이 덜 밀리고 더 안전하게 들어갈 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 171 / 373

← **이전**: [[170_self_healing_filesystem_zfs_btrfs|170. 하드웨어 에러 자가 치유 파일시스템 (Self-Healing Filesystem) — ZFS, Btrfs]]
**다음**: [[172_cold_start_provisioning_bottleneck|172. 프로비저닝 병목 (Cold Start) 관측 지표]] →

---
