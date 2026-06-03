---
title: 133. 4대 골든 시그널 (Four Golden Signals) - SRE 핵심 모니터링 지표
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 4대 [[186_golden_signals_sre_monitoring|골든 시그널]]은 **[[141_latency|Latency]]([[138_response_time|응답 시간]])·Traffic(요청량)·Errors(에러율)·Saturation(포화도)**이며, Google SRE가 정의한 **"이 4가지만 [[229_monitor|모니터]]링하면 [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 파악할 수 있다"**는 핵심 지표이다.
> 2. **가치**: 수백 개 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 중 진정으로 중요한 것만 추리면 이 4가지이며, 대시보드·알림을 이 4개에 집중하면 **노이즈 없이 장애를 조기 감지**할 수 있다.
> 3. **판단 포인트**: RED(Rate·Errors·Duration)은 [[532_microservices_decomposition_patterns|마이크로서비스]]용 변형, USE(Utilization·Saturation·Errors)는 인프라용 변형이다.

---

## Ⅰ. 개요 및 필요성

```text
Latency:    요청 처리 시간 (P50, P99)
Traffic:    초당 요청 수 (RPS, QPS)
Errors:     실패율 (5xx/전체)
Saturation: 리소스 포화도 (CPU·메모리·디스크)
```

- **📢 섹션 요약 비유**: 4대 [[186_golden_signals_sre_monitoring|골든 시그널]]은 자동차의 **속도계·RPM·경고등·연료 게이지** — 이 4개만 보면 차 상태를 안다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 시그널 | 알림 기준 예 |
|:---|:---|
| **[[141_latency|Latency]]** | P99 > 500ms |
| **Traffic** | RPS < 정상의 50% |
| **Errors** | 5xx > 1% |
| **Saturation** | CPU > 80% |

---

## Ⅲ~Ⅴ. 결론

4대 [[186_golden_signals_sre_monitoring|골든 시그널]]은 **[[100_sre_site_reliability_engineering_error_budget|SRE]] [[229_monitor|모니터]]링의 출발점**이며, 이 4가지에 집중하면 알림 노이즈를 줄이고 장애를 빠르게 감지할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Golden [[611_conditional_access_signals|Signals]]** | [[100_sre_site_reliability_engineering_error_budget|SRE]] 4대 핵심 지표 |
| **RED** | [[090_service_kubernetes_network_load_balancing|서비스]]용 변형 |
| **USE** | 인프라용 변형 |
| **[[102_sli_slo_service_level_indicator_objective|SLI]]** | [[186_golden_signals_sre_monitoring|골든 시그널]] 기반 지표 |
| **[[136_prometheus|Prometheus]]** | 수집 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수백 개 메트릭 (2000s)] → [Google SRE 4 Golden Signals (2016)]
    → [RED 방법론 (2017, Weaveworks)]
    → [USE 방법론 (Brendan Gregg)]
    → [현재: AI 이상 탐지 — 골든 시그널 자동 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 4대 [[186_golden_signals_sre_monitoring|골든 시그널]]은 자동차의 **속도계·RPM·경고등·연료 게이지**예요.
2. 이 **4가지만 보면** 차(시스템)가 잘 달리는지 알 수 있어요.
3. 너무 많은 계기판을 보면 **혼란스러우니까**, 핵심 4개에 집중해요!
