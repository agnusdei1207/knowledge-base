+++
title = "134. USE 메서드 (Utilization·Saturation·Errors) - 리소스 중심 분석"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: USE 메서드는 <strong>모든 리소스(CPU·메모리·디스크·네트워크)에 대해 Utilization(사용률)·Saturation(포화도)·Errors(에러)를 점검</strong>하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 체계적으로 찾는 Brendan Gregg의 방법론이다.
> 2. **가치**: 수백 개 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 중 어디를 봐야 할지 모를 때, USE로 <strong>모든 리소스를 3가지 관점으로 순회</strong>하면 병목을 빠르게 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 있다.
> 3. **판단 포인트**: USE는 **인프라(하드웨어) 리소스** 분석에 최적이며, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(애플리케이션) 분석에는 RED(Rate·Errors·Duration)를 사용한다.

---

## Ⅰ. 개요 및 필요성

```text
모든 리소스(CPU·메모리·디스크·NIC)에 대해:
  U: Utilization → 사용률 (%) 
  S: Saturation → 포화도 (큐 길이)
  E: Errors → 에러 수
→ 하나라도 이상이면 병목!
```

- **📢 섹션 요약 비유**: USE는 의사의 <strong>기본 건강 검진(체온·혈압·혈당)</strong>이다. 모든 장기를 3가지 지표로 점검한다.

---

## Ⅱ~Ⅴ. 결론

USE는 <strong>인프라 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 분석의 체계적 방법론</strong>이며, [골든 시그널](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/186_golden_signals_sre_monitoring/)·RED와 함께 상황에 맞게 조합하여 사용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **USE** | 리소스 중심 분석 |
| **Utilization** | 사용률 (%) |
| **Saturation** | 포화도 (큐) |
| **RED** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중심 분석 |
| **Brendan Gregg** | USE 메서드 창시자 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비체계적 성능 분석 (~2010s)]
    → [USE 메서드 (Brendan Gregg, 2012)]
    → [RED 메서드 (Weaveworks, 2017)]
    → [4 Golden Signals (Google SRE)]
    → [현재: AI 성능 분석 — 자동 병목 진단]
```

### 👶 어린이를 위한 3줄 비유 설명
1. USE는 <strong>건강 검진</strong>이에요. 모든 장기(리소스)를 <strong>3가지(체온·혈압·혈당)</strong>로 점검해요.
2. 하나라도 이상이면 **"여기가 문제!(병목)"** 알 수 있어요.
3. 체계적으로 <strong>하나씩 점검</strong>하면 빠르게 원인을 찾을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 373

← **이전**: [133. 4대 골든 시그널 (Four Golden Signals) - SRE 핵심 모니터링 지표](/knowledge-base/studynote/15_devops_sre/03_sre_observability/133_four_golden_signals/)
**다음**: [135. RED 메서드 (Rate·Errors·Duration) - 서비스 중심 분석](/knowledge-base/studynote/15_devops_sre/03_sre_observability/135_red_method_service_analysis/) →

---
