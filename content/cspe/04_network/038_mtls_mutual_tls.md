---
title: "mTLS 상호 인증 (mTLS Mutual TLS)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 38
---

# 📖 【암기용】 개념 완전 이해

> 목적: mTLS를 서버 인증 TLS에 클라이언트 인증서를 추가한 상호 신원 확인 방식으로 이해하게 만든다. 시험 답안 양식이 아니라, Zero Trust와 내부 서비스 인증 관점에서 익히기 위한 설명이다.

## 한눈에
- **개요**: mTLS는 서버와 클라이언트가 모두 X.509 인증서를 제시해 상호 인증하는 TLS 방식
- **왜 필요한가**: 내부 API, 마이크로서비스, B2B 연동에서 IP 기반 신뢰만으로는 위장 클라이언트와 lateral movement를 막기 어려움.
- **핵심 직관**: 일반 TLS는 손님이 서버 신분증만 확인하고, mTLS는 서버도 손님의 사원증을 확인하는 절차임.

## 깊이 이해
- **배경·문제의식**: HTTPS는 보통 서버 인증만 수행함. 그러나 내부망 침해, API key 유출, 서비스 위장 상황에서는 클라이언트 신원까지 암호학적으로 확인해야 함.
- **작동 원리**: 서버가 CertificateRequest를 보내면 클라이언트는 자신의 인증서와 개인키 서명(CertificateVerify)을 제시함. 서버는 CA chain, SAN, EKU, revocation 상태를 검증하고 접근 정책에 매핑함.
- **비유**: 건물 출입문에서 경비원이 회사 건물 신분을 보여주고, 방문자도 사원증과 출입 권한을 확인받는 양방향 검문임.
- **구체 예시**: 서비스 메시(Istio, Linkerd)는 sidecar proxy가 서비스별 SPIFFE ID 인증서를 사용해 pod 간 mTLS를 자동 구성함.
- **흔한 오해·주의점**: mTLS는 인증(authentication) 수단이며 인가(authorization)를 자동 해결하지 않음. 인증서 주체를 RBAC/ABAC 정책에 연결해야 함.

## 연결 개념
- TLS 1.3 Handshake: mTLS의 기반 핸드셰이크
- Zero Trust Architecture: 네트워크 위치보다 신원 기반 접근
- Service Mesh: 서비스 간 mTLS 자동화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: mTLS는 인증서 기반 클라이언트 신원 확인이며, PKI 운영·인증서 수명·폐기·인가 매핑까지 답안에 포함해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: mTLS는 TLS 핸드셰이크에서 서버 인증서와 클라이언트 인증서를 모두 검증하는 상호 인증 방식이다.
> 2. **가치**: API 호출 주체를 인증서 기반으로 확인해 내부 서비스 위장, API key 탈취, 네트워크 위치 기반 신뢰를 줄인다.
> 3. **판단 포인트**: CA 체계, 인증서 발급·회전, SAN/SPIFFE ID, revocation, RBAC 매핑을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 상호 인증 구조 이해 확인 | client certificate, CertificateRequest, chain 검증 | 일반 TLS와 차이 누락 |
| Zero Trust 적용 판단 확인 | 서비스 신원, least privilege, 정책 매핑 | mTLS를 인가 대체 수단으로 설명 |
| 운영 리스크 인식 확인 | 인증서 만료, 폐기, 키 유출, CA 관리 | 인증서 자동 회전·모니터링 누락 |

> 요약: mTLS 문제는 양방향 인증 절차와 PKI 운영 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라이언트와 서버가 서로의 인증서를 검증하는 상호 인증 TLS 방식
- 배경: 내부 API·서비스 간 통신에서 호출 주체를 암호학적으로 확인할 필요가 있음
- 필요성: Zero Trust 환경에서는 네트워크 위치 대신 인증서 신원과 정책으로 접근을 결정함

---

## Ⅱ. 구조 및 구성요소

```text
Client Cert -> TLS Handshake -> Server Cert
        / CA Trust Store
        / CertificateRequest
        / Policy Mapping -> RBAC/ABAC
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Client Certificate | 클라이언트 신원 증명 | SAN, SPIFFE ID 사용 가능 |
| Server Certificate | 서버 신원 증명 | DNS SAN 검증 |
| CA/Trust Store | 인증서 신뢰 체인 | 내부 CA, root rotation |
| CertificateVerify | 개인키 보유 증명 | TLS handshake 서명 |
| Policy Engine | 인증 주체를 권한에 매핑 | RBAC, ABAC, OPA |

> 요약: mTLS는 인증서와 CA 신뢰 체인을 기반으로 양쪽 신원을 확인하고 정책 엔진이 접근 권한을 판단함.

---

## Ⅲ. 동작원리 및 흐름도

```text
ClientHello -> ServerHello/Certificate -> CertificateRequest
-> Client Certificate -> CertificateVerify -> Finished
-> SAN/SPIFFE 검증 -> Policy 허용/거부
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서버가 인증서와 CertificateRequest 전송 | TLS config |
| 2 | 클라이언트가 인증서 체인과 서명 제시 | private key possession |
| 3 | 양측이 CA chain과 유효기간 확인 | expiry, issuer |
| 4 | 서버가 SAN/EKU/revocation 검증 | CRL, OCSP |
| 5 | 인증 주체를 RBAC/ABAC 정책에 매핑 | allow/deny log |

> 요약: mTLS는 TLS 핸드셰이크 안에서 클라이언트 인증서를 검증한 뒤 인증 주체를 접근 정책에 연결함.

---

## Ⅳ. 특징

| 구분 | 일반 TLS | mTLS | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 인증 방향 | 서버 인증 | 서버+클라이언트 인증 | X.509 양방향 검증 |
| 신원 기준 | DNS 이름 | 클라이언트 SAN/SPIFFE | SPIFFE ID 예: spiffe:// |
| 운영 부담 | 서버 인증서 중심 | 양측 인증서 lifecycle | 만료·회전 자동화 필요 |
| 적용 영역 | 웹 공개 서비스 | 내부 API, B2B, mesh | Istio PeerAuthentication |

> 요약: mTLS는 클라이언트 신원을 인증서로 확인하지만 PKI lifecycle 운영 부담이 함께 증가함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | mTLS | 선택 기준 |
|:---|:---|:---|:---|
| API Key | 공유 비밀 | 인증서 개인키 기반 | 키 복제 위험과 회전 주기 |
| JWT | 토큰 주체 | 채널 주체 인증 | 사용자 위임과 서비스 신원 분리 |
| VPN/IP ACL | 네트워크 위치 | 워크로드 신원 | Zero Trust 요구 |

> 요약: mTLS는 서비스 신원 인증에 강점이 있고, 사용자 권한은 JWT·RBAC와 결합해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인증서 만료 | 수동 발급·갱신 | cert-manager, 자동 회전 | expiry 30일 경보 |
| 폐기 지연 | 키 유출 후 CRL 미반영 | short-lived cert, OCSP | revoked cert access |
| 정책 누락 | 인증과 인가 분리 실패 | SAN 기반 RBAC, OPA policy | denied/allowed audit |

> 요약: mTLS 운영 리스크는 인증서 수명과 권한 매핑이며 자동 회전과 감사 로그로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| mTLS 적용률 | 서비스 간 트래픽 95% 이상 | mesh telemetry |
| 인증 실패 | 정상 배포 후 0.1% 이하 | TLS alert log |
| 인증서 수명 | 24시간~90일 정책 준수 | PKI inventory |

> 요약: mTLS 성공 여부는 적용률, 인증 실패율, 인증서 수명 준수로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 서비스 메시: Istio PeerAuthentication STRICT, DestinationRule TLS ISTIO_MUTUAL로 pod 간 mTLS 기본 적용
2. PKI 운영: 내부 CA, short-lived certificate, cert-manager 자동 회전, root/intermediate CA 분리 구성
3. 접근 제어: 인증서 SAN 또는 SPIFFE ID를 RBAC/ABAC 정책에 매핑하고 audit log를 SIEM으로 전송

**결론 (2줄):**
- 기술사 판단: 서비스 간 신원 확인이 요구되면 mTLS를 적용하고, 사용자 권한 판단은 JWT·RBAC와 분리 설계함
- 향후 방향: Zero Trust와 service mesh 확산으로 workload identity 기반 mTLS가 내부 통신의 기본 통제 수단이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "mTLS를 설명하시오" | 양방향 인증서 handshake 절차 | 일반 TLS와 인증 방향 차이 |
| 요구사항 명시형 | "Zero Trust 적용 방안을 제시하시오" | SPIFFE, policy mapping 흐름 | 인증서 lifecycle과 RBAC 대응 |

> 요약: 설명형은 상호 인증 절차, 보안형은 PKI 운영과 정책 매핑 중심으로 전환함.
