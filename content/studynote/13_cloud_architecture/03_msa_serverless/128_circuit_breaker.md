+++
title = "128. Circuit Breaker - MSA 장애 전파 차단 패턴"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Circuit Breaker는 **원격 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출 실패가 임계치를 초과하면 자동으로 회로를 열어(Open) 호출을 차단**하고, 일정 시간 후 반 열림(Half-Open)으로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 시도하는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 복원력(Resilience) 패턴이다.
> 2. **가치**: [Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) 없이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) B가 장애이면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) A가 **타임아웃까지 대기→[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 고갈→A도 장애(Cascading Failure)**가 발생하지만, Circuit Breaker가 **즉시 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) 응답**을 반환하여 장애 전파를 차단한다.
> 3. **판단 포인트**: Closed(정상)→Open(차단)→Half-Open([복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시도)의 3가지 상태를 이해하고, Hystrix(Netflix, 레거시)→Resilience4j(Java 표준)→[Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/))의 구현 진화를 파악해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Circuit Breaker 상태 전이                          │
├───────────────────────────────────────────────────────┤
│  [Closed — 정상]                                      │
│   모든 요청 통과, 실패 카운트                        │
│   실패 > 임계치 → Open                               │
│                                                       │
│  [Open — 차단]                                        │
│   모든 요청 즉시 거부, Fallback 반환                 │
│   타이머 만료 → Half-Open                            │
│                                                       │
│  [Half-Open — 복구 시도]                              │
│   일부 요청 통과하여 테스트                           │
│   성공 → Closed / 실패 → Open                       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Circuit Breaker는 전기의 **차단기(브레이커)**이다. 과전류(장애)가 흐르면 자동으로 차단하여 화재(Cascading Failure)를 방지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 |
|:---|:---|
| **캐시 반환** | 이전 성공 응답 반환 |
| **기본값** | 정적 기본값 제공 |
| **대체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)** | 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출 |
| **에러 반환** | 사용자에게 에러 안내 |

- **📢 섹션 요약 비유**: Fallback은 비상구이다. 정문([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 막히면 비상구(대체)로 나간다.

---

## Ⅲ. 비교 및 연결

| 비교 | CB 없음 | CB 있음 |
|:---|:---|:---|
| **장애 전파** | Cascading | **차단** |
| **[응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)** | 타임아웃까지 대기 | **즉시 [Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)** |
| **[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)** | 수동 | **자동 (Half-Open)** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) 구현

| 도구 | 특징 |
|:---|:---|
| **Resilience4j** | Java 표준, 경량 |
| **[Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)** | [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), 코드 무관 |
| **Envoy** | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 레벨 CB |

---

## Ⅴ. 기대효과 및 결론

Circuit Breaker는 **[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 복원력의 가장 기본적이고 중요한 패턴**이며, Retry·[Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)·Bulkhead와 함께 복합 적용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)** | 장애 전파 차단 |
| **[Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)** | 대체 응답 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| **Cascading Failure** | CB가 방지하는 연쇄 장애 |
| **[Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)** | 격벽 패턴 (리소스 격리) |
| **Retry** | 재시도 (CB와 함께 사용) |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 호출 (장애 전파, ~2010s)]
    │
    ▼
[Hystrix (Netflix, 2012~) — 최초 CB 라이브러리]
    │
    ▼
[Resilience4j (2018~) — Hystrix 대체, Java 표준]
    │
    ▼
[서비스 메시 CB (Istio/Envoy, 2018~) — 코드 무관]
    │
    ▼
[현재: 자동 CB 튜닝 — AI가 임계치 자동 조정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Circuit Breaker는 전기의 **차단기(브레이커)**예요.
2. 과전류(장애)가 흐르면 **자동으로 끊어서** 화재(연쇄 장애)를 막아요.
3. 잠시 기다렸다가 **살짝 켜보고(Half-Open)**, 안전하면 다시 정상으로 돌아가요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 371

← **이전**: [127. Service Discovery - MSA 서비스 자동 등록·탐색 메커니즘](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/127_service_discovery/)
**다음**: [129. Fallback 패턴 - MSA 장애 시 대체 응답 전략](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) →

---
