---
title: 130. Bulkhead 패턴 - 격벽으로 장애 격리
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[308_bulkhead_pattern|Bulkhead]](격벽)는 **[[090_service_kubernetes_network_load_balancing|서비스]]·리소스를 격리된 풀(Pool)로 분리**하여 하나의 장애가 다른 [[090_service_kubernetes_network_load_balancing|서비스]]로 전파되지 않도록 하는 [[619_msa_traffic_hardware|MSA]] 복원력 패턴이다.
> 2. **가치**: 주문·결제·추천 [[090_service_kubernetes_network_load_balancing|서비스]]가 **같은 [[103_thread_pool|스레드 풀]]을 공유**하면 추천 [[090_service_kubernetes_network_load_balancing|서비스]] 장애 시 [[092_thread_lwp|스레드]] 고갈→주문·결제도 장애(Cascading), Bulkhead로 분리하면 **추천만 영향**.
> 3. **판단 포인트**: [[103_thread_pool|스레드 풀]] [[308_bulkhead_pattern|Bulkhead]]([[090_service_kubernetes_network_load_balancing|서비스]]별 독립 풀)·[[224_semaphore|세마포어]] [[308_bulkhead_pattern|Bulkhead]](동시 호출 수 제한)·K8s ResourceQuota([[561_container_based_deployment|컨테이너]]별 CPU·메모리 격리)가 구현 방식이다.

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
| **[[103_thread_pool|스레드 풀]]** | [[090_service_kubernetes_network_load_balancing|서비스]]별 독립 [[103_thread_pool|스레드 풀]] |
| **[[224_semaphore|세마포어]]** | 동시 호출 수 제한 |
| **K8s Limits** | [[561_container_based_deployment|컨테이너]] CPU·메모리 격리 |

---

## Ⅲ~Ⅴ. 결론

Bulkhead는 **[[304_circuit_breaker|Circuit Breaker]]·Fallback과 함께 [[619_msa_traffic_hardware|MSA]] 복원력의 3대 패턴**이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[308_bulkhead_pattern|Bulkhead]]** | 격벽 (리소스 격리) |
| **[[304_circuit_breaker|Circuit Breaker]]** | 장애 전파 차단 |
| **[[520_rate_limiting|Rate Limiting]]** | 과부하 방지 |
| **ResourceQuota** | K8s 리소스 격리 |
| **Resilience4j** | [[308_bulkhead_pattern|Bulkhead]] 구현 [[336_library_vs_framework|라이브러리]] |

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
3. [[090_service_kubernetes_network_load_balancing|서비스]]마다 **벽을 세우면** 한쪽 문제가 다른 곳에 영향을 안 줘요!
