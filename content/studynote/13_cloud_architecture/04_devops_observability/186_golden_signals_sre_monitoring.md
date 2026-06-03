+++
title = "186. 골든 시그널 (4 Golden Signals - SRE 모니터링)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 4 Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/)(4 골든 시그널)는 구글 SRE가 정의한 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 모니터링 필수 지표 4가지로, [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)), 트래픽(Traffic), 에러(Errors), 포화도(Saturation)이며 이 4가지만 제대로 모니터링해도 대부분의 장애를 선제 감지할 수 있다.
> 2. **가치**: 수십 개의 시스템 지표 중 "무엇을 봐야 하는가?"에 대한 명확한 답을 제시하며, 알람 설계와 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 선택의 가이드 프레임워크로 실무에서 즉시 적용 가능하다.
> 3. **판단 포인트**: USE(Utilization, Saturation, Errors)는 인프라/리소스 관점, RED(Rate, Errors, Duration)는 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 관점으로 Golden Signals와 상호 보완적으로 활용한다.

---

## Ⅰ. 개요 및 필요성

[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 모니터링하면 수백 개의 지표가 나온다. CPU, 메모리, 디스크, 네트워크, GC, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수… 어디에 집중해야 할까? 알람을 전부 걸면 알람 피로(Alert Fatigue)로 진짜 중요한 신호를 놓친다.

구글 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 책은 이 문제를 4 Golden Signals로 해결한다. "모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 대해 이 4가지를 모니터링할 수 있다면 합리적인 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 건강 상태를 파악할 수 있다"고 명시한다. 이 프레임워크는 모니터링 설계의 출발점이자 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 선택의 가이드다.

[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 종류와 규모에 관계없이 사용자가 불편함을 느끼는 대부분의 상황은 이 4가지 중 하나 이상에 반영된다. 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)든, 검색 API든, 배치 처리든 동일하게 적용된다.

📢 **섹션 요약 비유**: 4 Golden Signals는 의사의 기본 4가지 생체 징후 측정이다. 체온(에러), 혈압(트래픽), 맥박([지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)), 산소포화도(포화도). 이 4가지만 봐도 환자의 위급 상태를 빠르게 판단한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4 Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">4 Golden Signals</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. Latency (지연 시간)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요청 처리에 걸린 시간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⚠️ 성공 요청 지연 ≠ 오류 요청 지연 구분</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">측정: p50, p95, p99 레이턴시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. Traffic (트래픽)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">서비스가 받는 요청/처리 수요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">측정: RPS(초당 요청 수), TPS, DAU</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. Errors (에러)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실패한 요청의 비율</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⚠️ 명시적(5xx) + 암묵적(잘못된 응답) 포함</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">측정: 에러율(%), 에러 건수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. Saturation (포화도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">서비스가 얼마나 "가득 찼는가"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⚠️ 100% 전에 성능 저하 시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">측정: CPU %, 메모리 %, 큐 길이, 연결 수</div></div>
</div>
</div>



| 시그널 | 핵심 질문 | PromQL 예시 | 알람 기준 |
|:---|:---|:---|:---|
| [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | 요청이 얼마나 빠른가? | `histogram_quantile(0.99, ...)` | p99 > 500ms |
| Traffic | 부하가 얼마나 많은가? | `rate(requests_total[5m])` | 평소 대비 3배 이상 |
| Errors | 얼마나 실패하는가? | `rate(errors_total[5m]) / rate(requests_total[5m])` | 에러율 > 1% |
| Saturation | 리소스가 얼마나 찼는가? | `process_cpu_usage` | CPU > 80% |

📢 **섹션 요약 비유**: Traffic은 고속도로 차량 수, Latency는 평균 통행 시간, Errors는 사고 발생률, Saturation은 도로 점유율이다. 4개를 보면 고속도로([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 상태를 완전히 파악할 수 있다.

---

## Ⅲ. 비교 및 연결

### 세 가지 모니터링 방법론 비교

| 방법론 | 전체 이름 | 초점 | 주요 지표 | 적합 대상 |
|:---|:---|:---|:---|:---|
| Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) | 4 Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 사용자 관점 | [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), Traffic, Errors, Saturation | 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| USE | Utilization, Saturation, Errors | 리소스/인프라 관점 | 사용률, 포화도, 오류 | CPU, 메모리, 디스크 |
| RED | Rate, Errors, Duration | [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 관점 | 요청 비율, 오류 비율, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [MSA API](/knowledge-base/studynote/15_devops_sre/05_devsecops/336_msa_api/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

**방법론 조합 사용:**
- 인프라 레이어: USE (리소스 포화도 감시)
- [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레이어: RED / Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) ([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))
- 비즈니스 레이어: 주문 완료율, 결제 성공률 등 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지표

📢 **섹션 요약 비유**: USE는 엔진 상태, RED는 속도계와 연료 소모, Golden Signals는 승차감까지 포함한 종합 진단이다. 목적에 따라 다른 계기판을 본다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>Golden <a href="/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/">Signals</a> 기반 <a href="/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/">Grafana</a> 대시보드 구성:</strong>

**행 1: Traffic 패널**
- 초당 요청 수 (RPS)
- 시간별 트래픽 추이
- 엔드포인트별 트래픽 분포

<strong>행 2: <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a> 패널</strong>
- p50/p95/p99 레이턴시 추이
- [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분포 히트맵

**행 3: Errors 패널**
- 에러율 (%)
- [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 상태 코드별 분포
- 에러 유형별 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 링크

**행 4: Saturation 패널**
- CPU/메모리 사용률
- 큐 길이, 연결 풀 사용률
- 리소스 임박 지표

<strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a> 측정의 핵심</strong>: 평균(average)이 아닌 백분위수(percentile) 사용 필수
- p50 = 중간값: "절반의 사용자가 이것보다 빠르다"
- p99 = 상위 1%: "99%의 사용자가 이것보다 빠르다"
- 평균은 극단값에 왜곡되어 실제 사용자 경험을 숨긴다

📢 **섹션 요약 비유**: 평균 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) vs p99는 평균 키와 "가장 키 큰 1%"의 차이다. 평균은 대부분을 대표하지만 극단적 경험(느린 사용자)을 숨긴다. SLI는 p99로 설정해야 한다.

---

## Ⅴ. 기대효과 및 결론

4 Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 프레임워크를 모니터링 설계의 기준으로 채택하면, 팀이 "무엇을 봐야 하는가"에 대한 합의를 빠르게 이룰 수 있다. 수백 개의 지표 중 핵심 4개에 집중함으로써 알람 피로를 줄이고 진짜 중요한 신호를 놓치지 않는다.

더 나아가 이 4개 시그널은 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 선택의 출발점이 된다. [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/), Error Rate SLI를 정의하고 SLO를 설정하면, 모니터링-[SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)-SLO-Error Budget의 완전한 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 관리 체계가 완성된다.

📢 **섹션 요약 비유**: 4 Golden Signals는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 건강의 심전도다. 4개의 선이 정상 범위에 있으면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 건강하고, 하나라도 이상해지면 진단이 필요하다는 즉각적인 신호가 된다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) | Golden Signals가 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 선택의 가이드 |
| [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) / [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) | Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 수집·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구 |
| AlertManager | Golden [Signals](/knowledge-base/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 임계값 기반 알람 |
| USE 방법론 | 인프라 레이어 보완 방법론 |
| RED 방법론 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레이어 보완 방법론 |
| p99 레이턴시 | [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 시그널의 올바른 측정 방식 |

### 👶 어린이를 위한 3줄 비유 설명
1. 4 Golden Signals는 의사가 환자를 볼 때 꼭 재는 체온, 혈압, 맥박, 산소포화도예요.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">4 Golden Signals (Google SRE)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Latency: 응답 시간 (p50, p99)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Traffic: 요청량 (QPS, TPS)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Errors: 오류율 (5xx, 비즈니스 에러)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Saturation: 리소스 포화도 (CPU, Mem, Disk)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">USE Method (Utilization · Saturation · Errors)</div>
<div class="kb-diagram-note">RED Method (Rate · Errors · Duration)</div>
</div>
</div>


2. 이 4가지만 정상이면 대부분 건강하고, 하나라도 이상하면 더 자세히 검사해요.
3. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)도 이 4가지([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 트래픽, 에러, 포화도)만 잘 보면 대부분의 문제를 잡을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 185 / 371

← **이전**: [185. 메트릭 (Metrics - Prometheus, Grafana)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/185_metrics_prometheus_grafana/)
**다음**: [187. 로그 및 ELK Stack (Logs, Centralized Logging)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/187_logging_elk_stack_centralized/) →

---
