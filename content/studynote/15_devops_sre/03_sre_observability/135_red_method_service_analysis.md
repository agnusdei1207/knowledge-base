---
title: 135. RED 메서드 (Rate·Errors·Duration) - 서비스 중심 분석
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RED 메서드는 **Rate(초당 요청 수)·Errors(에러율)·Duration([[138_response_time|응답 시간]])**의 3가지 지표로 [[532_microservices_decomposition_patterns|마이크로서비스]]의 상태를 [[229_monitor|모니터]]링하는 Weaveworks의 방법론이다.
> 2. **가치**: USE는 인프라(CPU·메모리) 중심이지만, RED는 **[[090_service_kubernetes_network_load_balancing|서비스]]([[014_api_posix|API]]·엔드포인트) 관점**에서 사용자 경험에 직접 영향을 미치는 지표에 집중한다.
> 3. **판단 포인트**: **인프라=USE, [[090_service_kubernetes_network_load_balancing|서비스]]=RED, 종합=Golden [[611_conditional_access_signals|Signals]]**로 상황에 맞게 선택하며, [[302_service_mesh_istio|서비스 메시]]([[302_service_mesh_istio|Istio]])가 RED [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 자동 수집한다.

---

## Ⅰ. 개요 및 필요성

```text
Rate:     초당 요청 수 (RPS) — 트래픽 양
Errors:   에러율 (5xx/전체) — 실패 비율
Duration: 응답 시간 (P50, P99) — 지연
  → 서비스별 이 3개만 보면 상태 파악 가능
```

- **📢 섹션 요약 비유**: RED는 식당의 3대 KPI이다. Rate=손님 수, Errors=주문 실수율, Duration=음식 나오는 시간.

---

## Ⅱ~Ⅴ. 결론

RED는 **[[532_microservices_decomposition_patterns|마이크로서비스]] [[229_monitor|모니터]]링의 핵심 방법론**이며, USE(인프라)와 함께 사용하여 전체 시스템을 파악한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **RED** | [[090_service_kubernetes_network_load_balancing|서비스]] 중심 분석 |
| **Rate** | 초당 요청 수 |
| **Errors** | 에러율 |
| **Duration** | [[138_response_time|응답 시간]] |
| **USE** | 인프라 중심 (보완) |

### 📈 관련 키워드 및 발전 흐름도

```text
[비체계적 서비스 모니터링] → [RED 메서드 (Weaveworks, 2017)]
    → [서비스 메시 자동 수집 (Istio, 2018~)]
    → [4 Golden Signals 통합]
    → [현재: AI RED 분석 — 이상 패턴 자동 감지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RED는 식당의 **3대 [[018_kpi|KPI]]**예요. 손님 수(Rate), 실수율(Errors), 음식 속도(Duration)!
2. 이 **3가지만 보면** 식당이 잘 운영되는지 알 수 있어요.
3. USE(주방 장비 상태)와 함께 보면 **더 완벽하게** 파악할 수 있답니다!
