+++
title = "130. Bulkhead 패턴 - 격벽으로 장애 격리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)(격벽)는 **[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·리소스를 격리된 풀(Pool)로 분리**하여 하나의 장애가 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 전파되지 않도록 하는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 복원력 패턴이다.
> 2. **가치**: 주문·결제·추천 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 **같은 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 공유**하면 추천 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 시 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 고갈→주문·결제도 장애(Cascading), Bulkhead로 분리하면 **추천만 영향**.
> 3. **판단 포인트**: [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) [Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 풀)·[세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) [Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)(동시 호출 수 제한)·K8s ResourceQuota([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)별 CPU·메모리 격리)가 구현 방식이다.

---

## Ⅰ. 개요 및 필요성

```text
Bulkhead = 선박의 격벽
  한 구획에 물이 차도 다른 구획은 안전
  → 서비스 A 장애 → 서비스 B·C는 정상
```

- **📢 섹션 요약 비유**: Bulkhead는 잠수함의 **격벽**이다. 한 구획이 침수되어도 다른 구획은 안전하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 방식 | 설명 |
|:---|:---|
| **[스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) |
| **[세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/)** | 동시 호출 수 제한 |
| **K8s Limits** | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) CPU·메모리 격리 |

---

## Ⅲ~Ⅴ. 결론

Bulkhead는 **[Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)·Fallback과 함께 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 복원력의 3대 패턴**이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)** | 격벽 (리소스 격리) |
| **[Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)** | 장애 전파 차단 |
| **[Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/)** | 과부하 방지 |
| **ResourceQuota** | K8s 리소스 격리 |
| **Resilience4j** | [Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) 구현 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[공유 스레드 풀 (전통)] → [Hystrix Bulkhead (2012~)]
    → [Resilience4j Bulkhead (2018~)]
    → [K8s ResourceQuota (컨테이너 격리)]
    → [현재: 서비스 메시 Bulkhead — Istio 자동 격리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Bulkhead는 잠수함의 **격벽**이에요. 한 칸에 물이 차도 **다른 칸은 안전**해요.
2. 격벽이 없으면 물(장애)이 전체로 퍼져서 **잠수함(시스템) 전체가 침몰**해요.
3. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 **벽을 세우면** 한쪽 문제가 다른 곳에 영향을 안 줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 371

← **이전**: [129. Fallback 패턴 - MSA 장애 시 대체 응답 전략](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)
**다음**: [131. Database per Service - MSA 데이터 분리 패턴](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/131_database_per_service/) →

---
