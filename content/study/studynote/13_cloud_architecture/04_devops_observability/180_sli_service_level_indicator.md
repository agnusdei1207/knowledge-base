+++
weight = 180
title = "180. SLI (Service Level Indicator, 서비스 수준 지표)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[102_sli_slo_service_level_indicator_objective|SLI]] ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]], [[090_service_kubernetes_network_load_balancing|서비스]] 수준 지표)는 사용자가 실제로 겪은 성공·실패·[[015_지연_데이터_관점|지연]]을 일정한 분모와 시간 창으로 계산한 관측 수치다.
> 2. **가치**: 좋은 SLI가 있어야 [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]), [[101_error_budget_sre|Error Budget]], 온콜 우선순위가 감이 아니라 [[001_dikw_pyramid|데이터]]로 움직인다.
> 3. **판단 포인트**: CPU (Central Processing Unit), 메모리처럼 측정하기 쉬운 내부 지표보다 [[568_logs_distributed_logging_elk_fluentd|로그]]인·결제·조회 같은 핵심 사용자 여정을 먼저 고르고, 성공 기준·분모·집계 창·백분위수를 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

SLI는 "[[090_service_kubernetes_network_load_balancing|서비스]]가 잘 되고 있는가?"를 숫자로 답하게 만드는 기준선이다. 같은 장애라도 사용자는 500 오류를 겪을 수도 있고, 성공은 했지만 8초를 기다렸다고 느낄 수도 있다. 따라서 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 관리는 서버 상태 자체보다 **사용자가 실제로 받은 결과**를 측정하는 지점에서 시작해야 한다.

문제가 되는 이유는 운영팀이 자주 내부 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 사용자 경험으로 착각하기 때문이다. CPU 사용률이 낮아도 결제 [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]])가 타임아웃이면 [[090_service_kubernetes_network_load_balancing|서비스]]는 나쁜 상태이고, 반대로 CPU 사용률이 높아도 사용자가 정상 응답을 받으면 그 순간의 SLI는 유지될 수 있다. SLI는 바로 이 차이를 구분해 "무엇이 원인 후보인지"와 "무엇이 실제 품질 저하인지"를 분리한다.

아래 그림은 사용자 경험 지표와 내부 진단 지표의 경계를 보여 준다. 핵심은 SLI가 원인 분석용 [[342_routing_metric_hop_bandwidth_delay|메트릭]]이 아니라, **사용자 관점의 품질 결과물**이라는 점이다.

```text
┌──────────────────────────────────────────────────────────────┐
│ 사용자 경험과 내부 메트릭의 경계                              │
├──────────────────────────────────────────────────────────────┤
│ 사용자 요청                                                   │
│    │                                                         │
│    ▼                                                         │
│ 로그인 / 결제 / 조회 / 데이터 적재                           │
│    │                                                         │
│    ├─ 성공했는가? ───────────────▶ Availability SLI           │
│    ├─ 충분히 빨랐는가? ─────────▶ Latency SLI                │
│    └─ 결과가 올바른가? ─────────▶ Quality SLI                │
│                                                              │
│ CPU · Memory · Queue Depth · DB Connection                   │
│    └─ 원인 분석용 supporting metric, SLI 자체는 아님         │
└──────────────────────────────────────────────────────────────┘
```

결국 SLI는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 피라미드의 맨 아래층이다. SLI가 정의되어야 SLO를 세울 수 있고, 그 SLO가 외부 계약으로 올라가면 [[085_sla|SLA]] ([[085_sla|Service Level Agreement]])가 된다. 따라서 SLI가 부정확하면 이후의 목표와 계약도 모두 흔들린다.

- **📢 섹션 요약 비유**: SLI는 식당 주방 온도가 아니라 손님이 실제로 받은 음식의 맛과 대기 시간을 점수로 적는 표와 같다. 주방 사정이 좋아 보여도 손님 경험이 나쁘면 좋은 식당이라고 할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 SLI는 보통 네 요소로 구성된다. 첫째, **관찰 대상 사용자 여정**이 있어야 한다. 둘째, 성공/실패를 가르는 **좋은 이벤트와 나쁜 이벤트 [[104_classification_analysis|분류]] 기준**이 있어야 한다. 셋째, 5분·1시간·30일 같은 **집계 창**이 있어야 한다. 넷째, 결과를 백분율·백분위수·초 단위처럼 표현하는 **계산식**이 있어야 한다.

| [[102_sli_slo_service_level_indicator_objective|SLI]] 유형 | 대표 질문 | 계산 예시 | 실무 포인트 |
| :--- | :--- | :--- | :--- |
| [[452_availability|가용성]] ([[452_availability|Availability]]) | 요청이 성공했는가? | `good / total` | 2xx만 좋은지, 3xx 포함 여부 정의 필요 |
| [[015_지연_데이터_관점|지연]]시간 ([[141_latency|Latency]]) | 충분히 빨랐는가? | `p95 < 300ms` 또는 `300ms 이내 비율` | 평균값보다 p95/p99가 사용자 체감에 민감 |
| 품질/[[002_bigdata_5v|정확성]] (Quality) | 결과가 올바른가? | 정합성 검사 통과율 | 200 OK여도 잘못된 결과면 실패로 봐야 함 |
| 신선도 (Freshness) | [[001_dikw_pyramid|데이터]]가 최신인가? | 5분 이내 반영 비율 | [[001_dikw_pyramid|데이터]] 플랫폼·[[217_cdc_binlog_change_capture_debezium|CDC]] 파이프라인에 중요 |
| 처리 완결성 (Completeness) | 빠짐없이 저장됐는가? | 손실 없는 이벤트 비율 | [[568_logs_distributed_logging_elk_fluentd|로그]] 유실, 중복 제거 정책과 연결 |

특히 계산식 설계가 중요하다. 예를 들어 [[452_availability|가용성]] SLI는 흔히 `성공 요청 수 / 전체 적격 요청 수`로 계산한다. 반면 [[015_지연_데이터_관점|지연]]시간은 평균으로 계산하면 극단값을 숨기기 쉬우므로, `p99 200ms 이내` 또는 `200ms 이하 응답 비율 99.5%`처럼 tail latency를 반영하는 식이 더 실무적이다.

아래 그림은 SLI가 어떻게 수집·가공되는지 보여 준다. 한 번의 요청 [[568_logs_distributed_logging_elk_fluentd|로그]]가 곧바로 SLI가 되는 것이 아니라, 관측 [[001_dikw_pyramid|데이터]]가 **good/bad [[104_classification_analysis|분류]] → 집계 → 시계열화**를 거쳐 [[181_slo_service_level_objective|SLO]] 판단 자료가 된다.

```text
┌──────────────────────────────────────────────────────────────┐
│ SLI 계산 파이프라인                                           │
├──────────────────────────────────────────────────────────────┤
│ Real User Monitoring / Load Balancer Log / Trace / Synthetic │
│                    │                                         │
│                    ▼                                         │
│         요청별 good / bad / slow 분류                        │
│                    │                                         │
│        ┌───────────┼───────────┐                             │
│        ▼                       ▼                             │
│  5분 단기 집계             30일 장기 집계                    │
│        │                       │                             │
│        └───────────┬───────────┘                             │
│                    ▼                                         │
│      SLI Time Series → SLO 비교 → Error Budget 계산         │
└──────────────────────────────────────────────────────────────┘
```

수집 지점 역시 설계 요소다. 로드밸런서에서 재면 외부 관점 [[452_availability|가용성]]에 강하고, 애플리케이션 내부에서 재면 비즈니스 성공 여부를 더 정교하게 볼 수 있다. 모바일·웹 [[090_service_kubernetes_network_load_balancing|서비스]]는 Synthetic Monitoring과 Real User Monitoring을 같이 써서 "밖에서 보이는 품질"과 "실제 사용자 [[160_session_controlling_terminal|세션]] 품질"을 동시에 보는 경우가 많다.

따라서 SLI의 핵심 원리는 간단하다. **측정하기 쉬운 것**이 아니라 **[[090_service_kubernetes_network_load_balancing|서비스]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 대표하는 것**을 정의하고, 그 수치를 일관된 창에서 반복 계산해야 한다. 그래야 장애·배포·[[282_performance_tactics|성능]] 개선이 모두 같은 기준선을 공유한다.

- **📢 섹션 요약 비유**: [[102_sli_slo_service_level_indicator_objective|SLI]] 설계는 시험 점수 계산법을 정하는 일과 같다. 평균만 볼지, 과락 기준을 둘지, 수행평가를 포함할지 정해야 같은 실력이라도 공정하게 비교할 수 있다.

---

## Ⅲ. 비교 및 연결

SLI를 제대로 이해하려면 비슷해 보이는 다른 지표들과 경계를 나눠야 한다. 가장 흔한 혼동은 **시스템 [[342_routing_metric_hop_bandwidth_delay|메트릭]]**, **[[102_sli_slo_service_level_indicator_objective|SLI]]**, **비즈니스 [[018_kpi|KPI]] ([[020_kpi|Key Performance Indicator]])** 를 한데 섞는 것이다.

| 구분 | 무엇을 묻는가 | 예시 | 잘못 쓰면 생기는 문제 |
| :--- | :--- | :--- | :--- |
| 시스템 [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 내부 자원이 버티는가? | CPU 85%, GC ([[380_garbage_collection|Garbage Collection]]) 시간, 큐 길이 | 사용자 영향 없는 경보가 늘어남 |
| [[102_sli_slo_service_level_indicator_objective|SLI]] | 사용자가 좋은 경험을 했는가? | 결제 성공률 99.95%, p99 250ms | 목표와 운영 판단이 가능해짐 |
| 비즈니스 [[018_kpi|KPI]] | 사업 결과가 좋아졌는가? | 재구매율, 전환율, 매출 | 장애와 사업 변동을 구분하기 어려움 |

또한 SLI는 수집 방식에 따라 **블랙박스 (Black-box)** 와 **화이트박스 (White-box)** 로 나눠 볼 수 있다.

| 수집 관점 | 장점 | 한계 | 잘 맞는 경우 |
| :--- | :--- | :--- | :--- |
| 블랙박스 [[102_sli_slo_service_level_indicator_objective|SLI]] | 실제 외부 사용자 관점에 가까움 | 내부 원인 파악은 느릴 수 있음 | 홈페이지, [[568_logs_distributed_logging_elk_fluentd|로그]]인, 글로벌 [[014_api_posix|API]] |
| 화이트박스 [[102_sli_slo_service_level_indicator_objective|SLI]] | [[090_service_kubernetes_network_load_balancing|서비스]] 내부 성공/실패 원인을 세밀하게 반영 | 클라이언트 단 실패를 놓칠 수 있음 | 내부 [[014_api_posix|API]], [[001_dikw_pyramid|데이터]] 처리 파이프라인 |

예를 들어 결제 [[090_service_kubernetes_network_load_balancing|서비스]]는 외부 합성 테스트로 "결제 화면이 열리는가"를 블랙박스로 보고, 동시에 애플리케이션 내부에서 "승인 요청이 1초 내 성공하는가"를 화이트박스로 볼 수 있다. 둘을 함께 봐야 화면은 열리지만 실제 승인 호출이 느린 상황, 반대로 내부는 정상인데 외부 [[511_dns_hierarchical_distributed_architecture|DNS]] ([[511_dns_hierarchical_distributed_architecture|Domain Name System]]) 문제가 생긴 상황을 구분할 수 있다.

SLI는 [[181_slo_service_level_objective|SLO]], [[085_sla|SLA]], Error Budget과도 연속선에 있다. SLI가 **측정값**, SLO가 **내부 목표**, SLA가 **외부 약속**이라면, Error Budget은 "얼마나 실패를 허용할지"를 운영과 배포 속도에 연결하는 장치다. 즉 SLI는 단일 지표가 아니라, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 거버넌스 전체를 작동시키는 입력값이다.

- **📢 섹션 요약 비유**: 시스템 [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[102_sli_slo_service_level_indicator_objective|SLI]], KPI의 차이는 자동차 계기판·주행 품질·매출 기록의 차이와 같다. 엔진 온도는 원인, 승차감은 품질, 판매량은 사업 결과다. 셋은 모두 중요하지만 같은 질문에 답하지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 중요한 판단은 "무엇을 SLI로 삼지 않을 것인가"다. 사용자 경험과 직접 연결되지 않는 CPU, 메모리, [[092_thread_lwp|스레드]] 수, 단순 평균 응답시간은 [[102_sli_slo_service_level_indicator_objective|SLI]] 후보가 아니라 원인 분석용 참고 지표다. SLI는 [[090_service_kubernetes_network_load_balancing|서비스]] 성격에 따라 1~3개의 핵심 여정으로 압축하는 편이 좋다.

| [[090_service_kubernetes_network_load_balancing|서비스]] 유형 | 권장 [[102_sli_slo_service_level_indicator_objective|SLI]] 예시 | 권장 창/기준 | 이유 |
| :--- | :--- | :--- | :--- |
| 결제 [[014_api_posix|API]] | 승인 성공률, p99 승인 [[015_지연_데이터_관점|지연]] | 5분 + 30일, p99 1초 | 실패 비용이 커서 짧은 경보와 장기 계약 둘 다 필요 |
| Software [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]] ([[309_saas|SaaS]]) 웹 [[090_service_kubernetes_network_load_balancing|서비스]] | [[568_logs_distributed_logging_elk_fluentd|로그]]인 성공률, [[286_page_frame|페이지]] 렌더 완료율 | 1분 + 28일 | 사용자 체감과 외부 약속을 함께 봄 |
| [[001_dikw_pyramid|데이터]] 적재 파이프라인 | 5분 이내 반영 비율, 유실 없는 이벤트 비율 | 15분 + 7일 | 신선도와 완결성이 핵심 |
| 내부 플랫폼 | 배포 성공률, 환경 [[087_process_state_transition|생성]] 시간 | 1시간 + 30일 | 내부 고객 경험을 [[090_service_kubernetes_network_load_balancing|서비스]]처럼 측정해야 함 |

실무 체크리스트는 다음과 같다.

1. 핵심 사용자 여정이 명확한가?
2. `good`과 `total`의 분모·분자가 논쟁 없이 정의되는가?
3. 평균값이 아니라 p95/p99, 또는 임계값 이내 비율을 쓰는 게 더 적절하지 않은가?
4. 단기 경보 창과 장기 목표 창을 분리했는가?
5. 재시도, 캐시 적중, 클라이언트 취소를 어떻게 [[104_classification_analysis|분류]]할지 정했는가?

흔한 안티패턴도 분명하다. 첫째, 너무 많은 SLI를 만들어 아무도 보지 않게 만드는 경우다. 둘째, 200 OK만 성공으로 보고 실제 비즈니스 실패를 놓치는 경우다. 셋째, 평균 응답시간만 보고 tail [[141_latency|latency]] 악화를 숨기는 경우다. 넷째, 인프라 지표를 SLI로 오인해 배포 중단 판단을 잘못 내리는 경우다.

기술사 답안에서는 "SLI는 [[090_service_kubernetes_network_load_balancing|서비스]] 품질 지표다"로 끝내지 말고, **사용자 여정 선정 → 성공 기준 정의 → 집계 창 [[009_config|설정]] → [[181_slo_service_level_objective|SLO]] 연결**의 순서로 설명해야 설계 판단이 드러난다. 좋은 SLI는 운영팀을 바쁘게 만드는 지표가 아니라, 팀이 무엇을 먼저 고쳐야 하는지 분명하게 알려 주는 지표다.

- **📢 섹션 요약 비유**: [[102_sli_slo_service_level_indicator_objective|SLI]] 선택은 병원 건강검진 항목을 고르는 일과 같다. 몸 상태를 보여 주는 핵심 수치를 골라야지, 측정하기 쉬운 숫자만 많이 모으면 정작 중요한 병을 놓칠 수 있다.

---

## Ⅴ. 기대효과 및 결론

SLI가 잘 정의되면 장애 대응과 [[090_service_kubernetes_network_load_balancing|서비스]] 개선이 같은 숫자를 바라보게 된다. 온콜은 감으로 심각도를 판단하지 않아도 되고, 제품팀은 새 기능 배포가 Error Budget을 얼마나 쓰는지 이해할 수 있으며, 경영진은 [[085_sla|SLA]] 논의를 실제 운영 [[001_dikw_pyramid|데이터]] 위에서 할 수 있다. 결국 SLI는 기술 운영과 비즈니스 의사결정을 연결하는 공통 언어가 된다.

물론 SLI만으로 모든 것을 설명할 수는 없다. 너무 거친 SLI는 국소 장애를 숨기고, 너무 세분화된 SLI는 운영 복잡도만 높인다. 그래서 좋은 운영은 **소수의 사용자 중심 [[102_sli_slo_service_level_indicator_objective|SLI]]**와 **풍부한 진단 [[342_routing_metric_hop_bandwidth_delay|메트릭]]**을 함께 가져간다. SLI는 전체 품질을 대표하는 전광판이고, 세부 [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 그 원인을 추적하는 계기판이라고 기억하면 된다.

결론적으로 SLI는 "측정 가능한 사용자 고통의 좌표"다. 사용자가 어디에서 느려지고, 어디에서 실패하고, 어디에서 신뢰를 잃는지 숫자로 잡아낼 수 있을 때 [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]])와 [[652_devops_calms_culture|DevOps]] 운영도 비로소 정밀해진다.

- **📢 섹션 요약 비유**: 좋은 SLI는 배의 항해 지도에 찍힌 등대와 같다. 배 안의 엔진 소리만 듣는 것이 아니라, 실제로 어디로 가고 있는지를 바깥 기준점으로 계속 확인하게 해 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]) | SLI를 바탕으로 정하는 내부 목표치 |
| [[085_sla|SLA]] ([[085_sla|Service Level Agreement]]) | SLO가 외부 계약과 보상 조건으로 확장된 형태 |
| [[101_error_budget_sre|Error Budget]] | SLI가 목표보다 얼마나 벗어날 수 있는지 계산하는 운영 여유 |
| [[164_synthetic_monitoring_dummy_client|Synthetic Monitoring]] | 외부 사용자 관점의 블랙박스 [[102_sli_slo_service_level_indicator_objective|SLI]] 수집 수단 |
| [[163_rum_real_user_monitoring|Real User Monitoring]] | 실제 [[160_session_controlling_terminal|세션]] 기반 체감 품질을 보는 [[102_sli_slo_service_level_indicator_objective|SLI]] 수집 수단 |
| RED (Rate, Errors, Duration) Method | 요청량·오류·[[015_지연_데이터_관점|지연]] 중심의 [[090_service_kubernetes_network_load_balancing|서비스]] 지표 선정 프레임 |
| Burn Rate Alert | [[101_error_budget_sre|Error Budget]] 소진 속도를 보고 경보하는 운영 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
사용자 여정 정의
    │
    ▼
good / bad 기준 설정
    │
    ▼
SLI (Service Level Indicator) 시계열 계산
    │
    ▼
SLO (Service Level Objective) 설정
    │
    ▼
Error Budget · Burn Rate 운영
    │
    ▼
SLA (Service Level Agreement) 및 배포 정책 의사결정
```

이 흐름은 단순 모니터링 수치를 넘어서, 사용자 경험 측정이 목표·계약·릴리스 판단으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SLI는 "오늘 놀이터 미끄럼틀이 몇 번 잘 작동했는지"를 세는 점수판이에요.
2. 점수판이 있어야 "오늘은 너무 자주 고장 났네"라고 정확하게 말할 수 있어요.
3. 그래서 어른들은 기계 안쪽 소리만 듣지 않고, 아이들이 정말 잘 놀았는지를 숫자로 확인한답니다.
