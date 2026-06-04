---
title: "163. RUM (Real User Monitoring)"
date: "2026-04-21"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RUM (Real User Monitoring, 실제 사용자 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링)은 실제 사용자의 브라우저나 모바일 앱에서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 오류, 상호작용 지표를 수집해 사용자가 체감한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질을 직접 측정하는 관측성 기법이다.
> 2. **가치**: 서버 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 정상이어도 네트워크, 브라우저, 기기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 지역별 콘텐츠 전송 경로 때문에 사용자 경험은 크게 달라질 수 있으며, RUM은 이 간극을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 드러낸다.
> 3. **판단 포인트**: RUM은 평균값보다 퍼센타일 (Percentile)과 세그먼트 분석이 중요하고, 샘플링·프라이버시·[합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/) ([Synthetic Monitoring](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)) 및 [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) (Application [Performance Monitoring](/studynote/02_operating_system/10_security/609_performance_monitoring/)) 연계까지 함께 설계해야 실무 가치가 커진다.

---

## Ⅰ. 개요 및 필요성

RUM은 실제 사용자의 환경에서 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 로딩 시간, 자바스크립트 오류, 인터랙션 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 화면 흔들림 같은 경험 지표를 수집하는 방식이다. 테스트 랩이나 개발자 노트북이 아니라, 실제 브라우저·모바일 앱·네트워크 조건에서 일어난 일을 기록한다는 점이 핵심이다. 그래서 시스템이 정상인가보다 사용자가 괜찮게 느꼈는가를 답하는 데 강하다.

이 개념이 필요한 이유는 서버 관점과 사용자 관점 사이에 큰 차이가 존재하기 때문이다. 서버 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 200밀리초 (ms)여도, 느린 스마트폰에서 렌더링이 오래 걸리거나 해외 사용자가 먼 콘텐츠 전송 네트워크 (Content Delivery Network, [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)) 경로를 타면 체감 속도는 훨씬 나빠질 수 있다. 즉 백엔드 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)만으로는 마지막 1마일의 경험을 설명하기 어렵다.

특히 전자상거래, 광고, 검색 같은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 1~2초 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)만으로도 이탈률과 전환율이 크게 변한다. 이런 환경에서는 실제 사용자에게서 Largest Contentful Paint ([LCP](/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/)), Interaction to Next Paint (INP), Cumulative Layout Shift (CLS), 오류율을 직접 수집해야 우선순위를 제대로 정할 수 있다.

- **📢 섹션 요약 비유**: RUM은 주방장이 "요리가 잘 나갔다"고 말하는 대신, 손님에게 직접 "음식이 따뜻했고 먹기 편했나요?"를 묻는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RUM의 기본 구조는 브라우저나 앱 안에 심어진 경량 수집기와, 이를 받아 분석하는 백엔드 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 이루어진다. 웹에서는 Navigation Timing [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), Resource Timing [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), PerformanceObserver 같은 브라우저 API를 통해 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이벤트를 읽고, 비콘 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Beacon](/studynote/03_network/12_iot_wpan_edge/608_beacon_technology_ibeacon_eddystone/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))나 비동기 전송으로 수집 서버에 전달한다. 모바일에서는 소프트웨어 개발 키트 (Software Development Kit, SDK)가 화면 전환, 네트워크 실패, 크래시, 사용자 행동을 함께 수집한다.

아래 그림은 RUM [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떻게 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되고 분석되는지 보여 준다.

```text
+----------------------------------------------------------------------+
|                     RUM 수집 아키텍처                               |
+----------------------------------------------------------------------+
| 실제 사용자 브라우저/앱                                             |
|   +- 성능 API: Navigation / Resource / Paint / Event Timing         |
|   +- 오류 수집: JS Error, API Fail, Crash                           |
|   +- 사용자 맥락: URL, 기기, 브라우저, 지역, 네트워크 유형          |
|   +- RUM SDK                                                         |
|              |                                                       |
|              v                                                       |
|       Beacon/API 전송 ---> 수집 엔드포인트 ---> 저장/집계 파이프라인   |
|                                              |                      |
|                                              v                      |
|                    대시보드 · 경보 · 세그먼트 분석 · APM 연계        |
+----------------------------------------------------------------------+
```

| 지표 | 의미 | 대표 기준 |
| :--- | :--- | :--- |
| [LCP](/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) (Largest Contentful Paint) | 주요 콘텐츠가 보이는 시간 | 2.5초 이하 권장 |
| INP (Interaction to Next Paint) | 입력 후 화면 반응까지 걸린 시간 | 200ms 이하 권장 |
| CLS (Cumulative Layout Shift) | 화면 흔들림 정도 | 0.1 이하 권장 |
| TTFB (Time to First [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)) | 첫 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 도착 시간 | 서버/네트워크 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 판단 |
| JS 오류율 | 실제 사용자 오류 발생 비율 | 배포 회귀 탐지에 유용 |

운영에서 중요한 것은 평균보다 퍼센타일이다. 예를 들어 [LCP](/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) 평균이 2초여도 하위 25% 사용자가 6초를 겪으면 사용자 불만은 여전히 크다. 그래서 RUM은 보통 P75나 P90 기준으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표 ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/), [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/))를 잡는다.

- **📢 섹션 요약 비유**: RUM은 놀이공원 대기 시간을 평균만 보는 것이 아니라, 가장 오래 기다린 손님들이 얼마나 힘들었는지까지 함께 보는 방식이다.

---

## Ⅲ. 비교 및 연결

RUM은 [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/), [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/), [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/)과 경쟁 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 아니라 서로 다른 층위를 보는 도구다. 무엇을 측정하느냐가 다르기 때문에 함께 써야 전체 그림이 잡힌다.

| 항목 | RUM | [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/) ([Synthetic Monitoring](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)) | [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) |
| :--- | :--- | :--- | :--- |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처 | 실제 사용자 | 스크립트 기반 가상 사용자 | 서버 애플리케이션 내부 |
| 강점 | 실제 경험 측정 | 사전 탐지, 반복 가능성 | 병목 위치 추적 |
| 약점 | 트래픽이 없으면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 적음 | 현실 사용자 다양성을 반영 못함 | 브라우저 체감 품질은 직접 못 봄 |
| 대표 질문 | "사용자가 정말 느렸나?" | "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 지금 살아 있나?" | "느린 원인이 어디인가?" |

예를 들어 해외 모바일 사용자의 결제 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) LCP가 급등했다면, RUM은 어느 지역·브라우저·기기에서 문제가 큰지 알려 준다. 그다음 [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)은 특정 리전에서 재현 여부를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, APM은 백엔드 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)인지 외부 결제 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 병목인지 보여 준다. 즉 RUM은 증상, APM은 원인 추적의 단서, [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)은 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/) 역할을 한다.

또한 RUM은 디지털 경험 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 (Digital Experience Monitoring)과 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([Site Reliability 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)) 운영을 연결한다. 서버 [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) ([Service Level Indicator](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/))가 정상이어도 사용자 경험 SLI가 나쁘다면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 기술적으로 살아 있어도 사업적으로는 실패할 수 있다.

- **📢 섹션 요약 비유**: [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)이 미리 준비된 시험 문제를 푸는 모의고사라면, RUM은 실제 시험장에서 학생들이 어떻게 느꼈는지 성적표를 받는 과정과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 모든 이벤트를 무제한 수집하기보다, 중요한 화면과 사용자 흐름에 맞춰 샘플링과 세그먼트를 설계해야 한다. 보통 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인, 검색, 상품 상세, 결제 같은 핵심 여정 (Critical User Journey)을 우선 계측하고, 지역·기기·브라우저·네트워크 유형별로 분해해 본다. 이때 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)는 최소화하고, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) (General [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) Regulation)이나 [CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) ([California Consumer Privacy Act](/studynote/09_security/16_data_privacy/800_ccpa/)) 같은 규정에 맞춰 익명화와 동의 절차를 갖춰야 한다.

### 운영 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 모바일/데스크톱, 국가, 브라우저, 네트워크 유형별 세그먼트가 준비되어 있는가?
2. P75 [LCP](/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/), P75 INP, 오류율처럼 사용자 체감에 가까운 지표를 경보 조건으로 쓰는가?
3. 배포 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 기능 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), 실험군 정보를 함께 수집해 회귀 원인을 좁힐 수 있는가?
4. RUM 이벤트에서 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제거했는가?

### 실무 시나리오

예를 들어 전체 평균은 정상이지만 브라질 안드로이드 4G 사용자에게서 결제 완료율이 급락했다고 가정하자. RUM을 보면 해당 세그먼트의 LCP와 JS 오류율이 동시에 튀고, APM에서는 서버 이상이 없을 수 있다. 이런 경우 원인은 대개 무거운 번들, 특정 브라우저 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 원거리 [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 캐시 미스처럼 프런트엔드와 전달 경로에 있다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 평균 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)만 보고 모든 사용자가 괜찮다고 판단하는 방식
- 데스크톱 고속망 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 보고 모바일 품질을 추정하는 방식
- [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)를 그대로 실어 보내 관측성과 규제 준수를 동시에 해치는 방식

- **📢 섹션 요약 비유**: RUM 운영은 전국 매장 매출을 볼 때 전체 합계만 보는 것이 아니라, 어느 지역과 어느 시간대에 손님이 불편했는지 매장별로 나눠 보는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

RUM을 도입하면 사용자 경험 문제를 추측이 아니라 측정으로 다룰 수 있다. [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선 우선순위가 명확해지고, 특정 국가·브라우저·기기에서만 발생하는 숨은 장애를 빠르게 발견할 수 있다. Core Web Vitals 개선은 검색 노출, 이탈률, 전환율 같은 비즈니스 지표와도 직접 연결된다.

다만 RUM은 실제 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라는 특성상 노이즈가 많고, 트래픽이 적은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 통계 안정성이 떨어질 수 있다. 또한 클라이언트 코드 삽입, 샘플링 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 설계가 미흡하면 운영 부담이 커진다. 그래서 RUM은 단독 해결책이 아니라 [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/), [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 함께 운영해야 가치가 완성된다.

결론적으로 RUM은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 동작하는가를 넘어 사용자가 만족했는가를 묻는 관측성 계층이다. [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 관점에서는 인프라 정상 여부만이 아니라 사용자 경험의 품질을 함께 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표에 반영하게 만드는 실전 도구라고 기억하면 된다.

- **📢 섹션 요약 비유**: RUM은 병원의 검사 수치만 보는 것이 아니라, 환자에게 직접 "지금 얼마나 아픈가요"를 묻는 문진과 같다. 숫자와 체감이 함께 있어야 진짜 상태를 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Core Web Vitals | RUM이 대표적으로 수집하는 사용자 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| [합성 모니터링](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/) ([Synthetic Monitoring](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)) | 실제 사용 전 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/)을 제공하는 보완 도구 |
| [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) (Application [Performance Monitoring](/studynote/02_operating_system/10_security/609_performance_monitoring/)) | 서버 내부 병목을 추적해 RUM 증상의 원인을 좁힘 |
| 디지털 경험 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 (Digital Experience Monitoring) | RUM이 포함되는 상위 관점 |
| [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)/[SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) | 사용자 경험 기반 목표를 정의할 때 연결되는 운영 지표 |

### 📈 관련 키워드 및 발전 흐름도

```text
서버 중심 모니터링
    |
    v
브라우저 성능 API · 모바일 SDK 계측
    |
    v
RUM (Real User Monitoring)
    |
    +- Core Web Vitals 측정
    +- 오류율 · 세그먼트 분석
    +- 사용자 체감 SLI 도출
    |
    v
Synthetic Monitoring · APM · DEM 통합 관측성
```

이 흐름도는 인프라 중심 관측이 사용자 경험 중심 관측으로 확장되고, 다시 통합 관측성 체계로 연결되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. RUM은 컴퓨터가 "내가 잘했어"라고 말하는 대신, 진짜 사용한 친구들에게 "정말 빨랐니?"를 물어보는 거예요.
2. 어떤 친구는 빠르게 느끼고, 어떤 친구는 오래 기다릴 수 있어서 모두의 이야기를 같이 들어야 해요.
3. 그래서 RUM을 보면 어디에서 누가 가장 불편했는지 찾아서 더 빨리 고칠 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 163 / 373

<- **이전**: [162. APM (Application Performance Management)](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/)
**다음**: [164. 합성 모니터링 (Synthetic Monitoring)](/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/) ->

---
