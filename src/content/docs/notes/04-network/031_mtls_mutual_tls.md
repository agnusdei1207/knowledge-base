---
sidebar:
  order: 31
  label: "031. 상호 TLS 보안: mTLS"
  badge:
    text: "기출 · 50%"
    variant: note
title: "상호 전송 계층 보안 : mTLS (Mutual TLS)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 31
extra:
  question_no: "31"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "양방향 X.509 인증서 기반 기계 신원 검증 및 제로 트러스트 보안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **mTLS (Mutual TLS)**: 클라이언트만 서버를 검증하는 단방향 TLS와 달리, 서버도 클라이언트의 X.509 인증서를 요구하여 양방향 기계 신원(Machine Identity)을 상호 검증하는 프로토콜.
- **Machine Identity (기계 신원)**: 서비스, 컨테이너, 워크로드 간 통신에서 X.509 인증서 및 개인키 서명을 통해 증명되는 암호학적 디지털 신원.

</details>

- 정의/개념: 클라이언트와 서버가 서로의 X.509 인증서를 상호 교환하여 **양방향 신원을 검증하고 전송 구간을 암호화하는 상호 전송 계층 보안 프로토콜**
- 배경/필요성: 서버의 신원만 검증하는 기존 단방향 TLS 환경에서는 마이크로서비스(MSA) 및 M2M/API 연동 시 비인가 클라이언트의 신원 위변조, API 키 탈취를 통한 불법 호출, 침해된 내부 워크로드의 횡적 이동(Lateral Movement) 공격을 방어할 수 없고 IP 기반 접근 제어가 클라우드 동적 환경에서 무력화되는 한계를 극복하기 위해, 통신에 참여하는 양측 모두가 공통 신뢰 앵커(Trust Anchor) 기반의 X.509 디지털 인증서를 상호 교환하고 개인키 전자서명으로 기계 신원(Machine Identity)을 검증하는 mTLS(Mutual TLS)를 도입하여 **네트워크 위치에 의존하지 않는 제로 트러스트(Zero Trust) 상호 인증과 종단 간 암호화 통신**을 달성할 필요

#### 한줄 요약
- 양방향 X.509 인증서 검증을 통해 클라이언트와 서버의 기계 신원을 확인하고 구간 암호화를 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CertificateRequest & CertificateVerify**: 서버가 클라이언트에 인증서를 요구하고(Request), 클라이언트가 핸드셰이크 해시를 개인키로 서명(Verify)하여 소유권을 입증하는 메시지.
- **Zero Trust Network**: "절대 신뢰하지 않고 항상 검증한다"는 보안 패러다임으로, 내부망 트래픽도 mTLS로 상호 인증 및 암호화 강제.

</details>

- IP나 포트에 의존하지 않고 암호학적 X.509 인증서로 엔드포인트를 식별하는 **기계 신원(Machine Identity)**
- `CertificateRequest`와 `CertificateVerify` 핸드셰이크를 통한 **양방향 상호 신뢰 수립**
- 마이크로서비스 간 중간자 도청 및 변조를 원천 차단하는 **제로 트러스트 통신 채널 제공**

#### 한줄 요약
- 기계 신원 기반 상호 검증, 양방향 핸드셰이크, 제로 트러스트 구간 암호화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Trust Store (신뢰 저장소)**: 양 엔드포인트가 신뢰하는 공통 루트 CA 및 중간 CA 인증서 모음.
- **SPIFFE / SPIRE**: 클라우드 네이티브 환경에서 워크로드에 X.509 인증서(SVID)를 자동 발급하는 표준 오픈소스 프레임워크.

</details>

```text
[mTLS 상호 인증 아키텍처]
  │
  ├─ [신뢰 인프라] ── Trust Infrastructure
  │     ├─ 공통 Root CA (사설 PKI / SPIFFE Trust Anchor)
  │     └─ 인증서 발급 관리 (X.509 SVID 수명주기 갱신)
  │
  ├─ [상호 엔드포인트] ── Mutual Endpoints
  │     ├─ 클라이언트 워크로드 (Client Cert & 개인키 전자서명)
  │     ├─ 서버 워크로드 (Server Cert & 개인키 키 교환)
  │     └─ 신뢰 저장소 Trust Store (로컬 보관 Root CA 목록)
  │
  └─ [암호 통신 채널] ── Secure Channel
        ├─ 양방향 검증 (CertRequest / CertVerify 핸드셰이크)
        ├─ 키 교환 (ECDHE 기반 임시 키 교환)
        └─ 데이터 암호화 (AES-256-GCM 고속 대칭 암호화)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 공통 인증기관 (CA) | 워크로드 인증서 **자동 발급·수명주기 갱신 관리** |
| 클라이언트 신원 체계 | 클라이언트 워크로드 **X.509 인증·개인키 전자서명** |
| 서버 신원 체계 | 서버 도메인 **X.509 인증·ECDHE 키 교환** |
| 신뢰 저장소 (Trust Store) | 로컬 보관 Root CA 기반 **인증서 체인 유효성 검증** |
| 대칭 세션 키 | 상호 인증 완료 후 **AES-GCM 구간 암호화** |

#### 한줄 요약
- 신뢰 저장소에 공통 CA 하나만 두면 상대 인증서를 그 체인으로 검증할 수 있으므로, 워크로드 쌍마다 신원을 따로 등록하던 일을 인증기관이 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **mTLS 5단계 핸드셰이크**: ClientHello $\to$ ServerHello/Cert/CertRequest $\to$ 서버 인증서 검증 $\to$ 클라이언트 Cert/CertVerify $\to$ 상호 인증 완료 및 암호화.

</details>

```text
mTLS 양방향 핸드셰이크 파이프라인
        │
   1. [ClientHello] 클라이언트가 지원 암호 스위트(ECDHE-RSA-AES-GCM) 및 TLS 버전 전송
        │
   2. [ServerHello & CertRequest] 서버 인증서 제시 및 `CertificateRequest`로 클라이언트 인증 요구
        │
   3. [서버 인증서 검증] 클라이언트가 Trust Store를 참조하여 서버 인증서 체인/만료 검증
        │
   4. [클라이언트 인증서 및 서명 송출] `Certificate` + 개인키 서명 `CertificateVerify` 전송
        │
   5. [서버 검증 및 보안 채널 확립] 서버가 클라이언트 서명 검증 -> AES-GCM 세션 키 암호화 통신 개시
```

#### 한줄 요약
- 단방향 TLS와 갈리는 지점은 서버가 `CertificateRequest`를 덧붙이는 2단계이며, 그 한 요구 때문에 클라이언트도 인증서 제시와 개인키 서명 검증 비용을 핸드셰이크마다 추가로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **mTLS (Mutual TLS)** vs **단방향 TLS (One-Way TLS)**: 양방향 기계 신원 검증(mTLS)과 클라이언트의 서버 단독 검증(One-Way).

</details>

| 비교 항목 | 상호 전송 계층 보안 (mTLS) | 일반 단방향 TLS (One-Way TLS) |
|:---|:---|:---|
| **인증 검증 방향** | **양방향 상호 검증 (클라이언트 $\leftrightarrow$ 서버)**| **단방향 검증 (클라이언트 $\to$ 서버 단독)** |
| **주요 적용 영역** | **M2M, 마이크로서비스(Service Mesh), 금융망 API** | **일반 대고객 웹 서비스 (HTTPS 브라우징)** |
| **클라이언트 신원 증명**| **암호학적 X.509 인증서 기반 강한 기계 신원 보증** | 인증서 없음 (L7 ID/PW, JWT 토큰에 의존) |
| **인증서 관리 복잡도**| **높음 (모든 단말/워크로드에 인증서 발급·갱신 필요)**| 낮음 (서버 단일 인증서만 관리) |

#### 한줄 요약
- mTLS는 M2M 및 제로 트러스트용 양방향 검증을 수행하고, 단방향 TLS는 일반 대고객 웹 서비스에 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Service Mesh (서비스 메시)**: Envoy 등의 사이드카 프록시를 통해 애플리케이션 코드 수정 없이 인프라 계층에서 mTLS 암호화와 인증서 갱신을 투명하게 처리하는 아키텍처.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수많은 마이크로서비스 간 인증서 만료로 인한 서비스 전면 장애 | **`서비스 메시(Istio/Envoy)` 및 `SPIRE 기반 인증서 자동 로테이션`** | 인증서 만료 장애 원천 차단 및 운영 자동화 |
| 유출된 클라이언트 인증서를 악용한 비인가 기계의 위장 접속 | **`단기 유효 인증서(Short-Lived Cert, 1일)` 및 실시간 CRL/OCSP** | 인증서 탈취 피해 시간 극소화 |
| mTLS 인증 성공 후 내부 모든 API에 무제한 접근하는 권한 남용 | mTLS 신원(인증)과 **`OPA (Open Policy Agent) / RBAC 인가` 분리** | 최소 권한 원칙(Least Privilege) 확립 |
| 대규모 mTLS 핸드셰이크 암복호화로 인한 CPU 리소스 과부하 | **`TLS Session Resumption (Session Ticket)` 및 암호화 가속기** | 핸드셰이크 연산 비용 80% 이상 절감 |

#### 한줄 요약
- 서비스 메시 자동 로테이션, 단기 인증서, OPA/RBAC 인가 분리, Session Resumption으로 운영한다.

## Ⅶ. 결론

- 클라우드 네이티브 쿠버네티스 환경과 서비스 메시(Istio/Linkerd), 마이크로서비스 및 금융/핀테크 오픈 API의 **가장 핵심적인 기계 대 기계(M2M) 제로트러스트 보안 표준 프로토콜**로 자리잡았으며, 실무 구축 시에는 **수백~수천 개 워크로드의 인증서 만료 사고를 방지하기 위해 SPIFFE/SPIRE 기반 SVID 자동 발급 및 단기 인증서(Short-Lived Cert) 자동 갱신 체계를 구축하고, L4/L7 인증(mTLS)과 L7 인가(OPA/RBAC 세부 권한 제어)를 분리 설계**하여 고가용성 보안 거버넌스를 완성

#### 한줄 요약
- mTLS는 양방향 X.509 인증서 검증을 통해 기계 신원을 보증하며, 서비스 메시 자동화와 결합하여 제로 트러스트를 실현하는 핵심 전송 보안 기술이다.
