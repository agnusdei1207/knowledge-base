---
title: 127. Service Discovery - MSA 서비스 자동 등록·탐색 메커니즘
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[090_service_kubernetes_network_load_balancing|Service]] Discovery는 **MSA에서 동적으로 변하는 [[090_service_kubernetes_network_load_balancing|서비스]] 인스턴스의 위치(IP:[[446_port_and_bus|Port]])를 자동으로 등록·탐색·갱신**하는 메커니즘이며, [[090_service_kubernetes_network_load_balancing|서비스]] [[235_registry_immutable_tag|레지스트리]]([[090_service_kubernetes_network_load_balancing|Service]] [[235_registry_immutable_tag|Registry]])가 핵심 컴포넌트이다.
> 2. **가치**: [[561_container_based_deployment|컨테이너]] 환경에서 [[090_service_kubernetes_network_load_balancing|서비스]] 인스턴스는 [[249_scaling_normalization_standardization|스케일링]]·재배포 시 **IP가 수시로 변경**되므로 하드코딩이 불가능하며, [[090_service_kubernetes_network_load_balancing|Service]] Discovery가 **"주문 [[090_service_kubernetes_network_load_balancing|서비스]] 어디 있어?"에 실시간 답변**한다.
> 3. **판단 포인트**: **Client-side(클라이언트가 [[235_registry_immutable_tag|레지스트리]] 조회)** vs **Server-side(로드밸런서가 [[235_registry_immutable_tag|레지스트리]] 조회)**를 구분하고, K8s의 [[511_dns_hierarchical_distributed_architecture|DNS]] 기반 [[090_service_kubernetes_network_load_balancing|Service]] Discovery가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Service Discovery 동작                             │
├───────────────────────────────────────────────────────┤
│  1. 서비스 인스턴스 시작 → Registry에 등록           │
│     (Order-Svc: 10.0.1.5:8080)                       │
│  2. 호출자가 "Order-Svc 어디?" → Registry 조회       │
│  3. Registry 응답: 10.0.1.5:8080                     │
│  4. 호출자 → 10.0.1.5:8080 직접 호출                │
│  5. 인스턴스 종료 → Registry에서 제거 (헬스체크)     │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[090_service_kubernetes_network_load_balancing|Service]] Discovery는 **전화번호부**이다. 사람([[090_service_kubernetes_network_load_balancing|서비스]])이 이사(IP 변경)해도 전화번호부([[235_registry_immutable_tag|레지스트리]])를 보면 **현재 주소를 찾을 수 있다**.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Client-side vs Server-side

| 방식 | 동작 | 대표 |
|:---|:---|:---|
| **Client-side** | 클라이언트가 [[235_registry_immutable_tag|레지스트리]] 조회 + LB | **Eureka** |
| **Server-side** | LB가 [[235_registry_immutable_tag|레지스트리]] 조회 | **K8s [[090_service_kubernetes_network_load_balancing|Service]]** |

### K8s [[303_service_discovery|Service Discovery]]
- [[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[087_process_state_transition|생성]] → kube-dns에 자동 등록.
- `order-svc.default.svc.cluster.local`로 [[511_dns_hierarchical_distributed_architecture|DNS]] 조회.

- **📢 섹션 요약 비유**: Client-side는 직접 전화번호부를 찾는 것, Server-side는 안내 데스크(LB)에 물어보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 하드코딩 | [[303_service_discovery|Service Discovery]] |
|:---|:---|:---|
| **IP 변경** | 코드 수정 | **자동 갱신** |
| **[[249_scaling_normalization_standardization|스케일링]]** | 수동 | **동적 등록** |
| **장애** | 감지 불가 | **헬스체크 제거** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 도구
- **Consul** (HashiCorp): [[303_service_discovery|Service Discovery]] + [[009_config|Config]].
- **Eureka** (Netflix): Client-side, Spring Cloud.
- **K8s [[090_service_kubernetes_network_load_balancing|Service]]**: Server-side, [[511_dns_hierarchical_distributed_architecture|DNS]] 기반.
- **[[078_etcd_distributed_key_value_store|etcd]]**: K8s의 상태 저장소.

---

## Ⅴ. 기대효과 및 결론

[[090_service_kubernetes_network_load_balancing|Service]] Discovery는 **MSA의 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신의 기본 인프라**이며, K8s 환경에서는 [[511_dns_hierarchical_distributed_architecture|DNS]] 기반으로 투명하게 제공된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[090_service_kubernetes_network_load_balancing|Service]] [[235_registry_immutable_tag|Registry]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 위치 저장소 |
| **헬스체크** | 비정상 인스턴스 자동 제거 |
| **Consul** | HashiCorp [[306_service_discovery_pattern|서비스 디스커버리]] |
| **Eureka** | Netflix 클라이언트 사이드 |
| **K8s [[511_dns_hierarchical_distributed_architecture|DNS]]** | 서버 사이드 디스커버리 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드코딩 IP (전통, ~2010s)]
    │
    ▼
[Client-side Discovery (Eureka, 2012~)]
    │
    ▼
[Server-side Discovery (K8s Service, 2015~)]
    │
    ▼
[Service Mesh (Istio/Envoy, 2018~) — 투명한 Discovery]
    │
    ▼
[현재: 멀티 클러스터 Discovery — 클러스터 간 서비스 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[090_service_kubernetes_network_load_balancing|Service]] Discovery는 **전화번호부**예요. 친구([[090_service_kubernetes_network_load_balancing|서비스]])가 이사해도 **새 주소**를 찾을 수 있어요.
2. 전화번호부가 없으면 친구가 이사할 때마다 **직접 물어봐야** 해서 불편해요.
3. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]](K8s)는 전화번호부를 **자동으로 업데이트**해줘서 편리하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 126 / 371

← **이전**: [[126_bff|126. BFF (Backend For Frontend) - 클라이언트별 맞춤 API 레이어]]
**다음**: [[128_circuit_breaker|128. Circuit Breaker - MSA 장애 전파 차단 패턴]] →

---
