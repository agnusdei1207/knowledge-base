---
title: 146. mTLS (Mutual TLS) - 서비스 간 상호 인증·암호화
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: mTLS는 **클라이언트와 서버가 양쪽 모두 [[303_authentication_authorization_patterns|인증]]서를 [[395_verification_process_review|검증]](상호 [[303_authentication_authorization_patterns|인증]])**하는 [[694_thread_local_storage_tls|TLS]] 확장이며, [[302_service_mesh_istio|서비스 메시]]([[302_service_mesh_istio|Istio]])에서 **[[090_service_kubernetes_network_load_balancing|서비스]] 간 통신의 암호화·[[303_authentication_authorization_patterns|인증]]·[[003_integrity|무결성]]**을 보장하는 핵심 메커니즘이다.
> 2. **가치**: 일반 TLS는 **서버만 [[303_authentication_authorization_patterns|인증]]**(클라이언트는 아무나)하지만, mTLS는 **양쪽 모두 [[303_authentication_authorization_patterns|인증]]**하여 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 네트워크에서 "네트워크 내부라도 신뢰하지 않는" 원칙을 실현한다.
> 3. **판단 포인트**: [[302_service_mesh_istio|서비스 메시]]([[302_service_mesh_istio|Istio]])가 **자동 [[303_authentication_authorization_patterns|인증]]서 발급·회전·[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 적용**을 사이드카에서 처리하므로, 애플리케이션 코드 변경 없이 적용된다.

---

## Ⅰ. 개요 및 필요성

```text
TLS:   클라이언트 → 서버 인증서 검증 (서버만 인증)
mTLS:  클라이언트 ↔ 서버 양쪽 인증서 교환·검증
  → Zero Trust: 내부 네트워크도 암호화
  Istio: 자동 인증서 발급 → Envoy 사이드카에서 mTLS
```

- **📢 섹션 요약 비유**: TLS는 **신분증 [[396_validation|확인]](서버만)**, mTLS는 **양쪽 모두 신분증 [[396_validation|확인]]**이다.

---

## Ⅱ~Ⅴ. 결론

mTLS는 **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]·[[302_service_mesh_istio|서비스 메시]]의 보안 핵심**이며, Istio가 자동화를 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]]** | 상호 [[303_authentication_authorization_patterns|인증]] |
| **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]** | 내부도 불신 |
| **[[302_service_mesh_istio|Istio]]** | 자동 [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] |
| **[[303_authentication_authorization_patterns|인증]]서 회전** | 자동 갱신 |
| **SPIFFE** | [[090_service_kubernetes_network_load_balancing|서비스]] ID 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[평문 통신 (~2015)] → [TLS (서버 인증)]
    → [mTLS (상호 인증, 2017~)]
    → [Istio 자동 mTLS (2018)]
    → [현재: SPIFFE/SPIRE — 서비스 ID 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. TLS는 **가게(서버)만 신분증**을 보여주는 거예요.
2. mTLS는 **손님(클라이언트)도 신분증**을 보여야 들어갈 수 있어요.
3. 이렇게 하면 **가짜 손님**이 못 들어와서 안전해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 371

← **이전**: [[145_sidecar_proxy_pattern|145. 사이드카 프록시 패턴 (Sidecar Proxy) - Envoy 기반]]
**다음**: [[147_ddd_domain_driven_design|147. DDD (Domain-Driven Design) - 도메인 주도 설계]] →

---
