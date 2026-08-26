---
sidebar:
  order: 31
  label: "031. 상호 TLS 보안: mTLS"
  badge:
    text: "기출 · 50%"
    variant: note
title: "상호 전송 계층 보안 : mTLS (Mutual TLS)"
date: "2026-08-26T13:41:55+09:00"
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
- 배경/필요성: 단방향 TLS의 한계로 인한 **마이크로서비스(MSA) 간 통신 시 클라이언트 신원 위변조, 내부망 횡적 이동(Lateral Movement) 침해 방어 불가**

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
[mTLS 양방향 상호 인증 및 서비스 메시 아키텍처]
|-- Common Root CA / SPIFFE Trust Anchor (공통 신뢰 앵커)
|-- Client Workload (Service A Envoy Sidecar)
|   |-- Client Certificate + Private Key (X.509 SVID 신원)
|   `-- Trust Store (Root CA 공개키 보관)
`-- Server Workload (Service B Envoy Sidecar)
    |-- Server Certificate + Private Key (X.509 SVID 신원)
    `-- Trust Store (Root CA 공개키 보관)
`-- Encrypted Data Channel (ECDHE 키 교환 -> AES-256-GCM 대칭 세션 키 통신)
```

선의 의미: 계층 및 공통 Root CA를 신뢰하는 양측 워크로드가 상호 인증서를 검증하고 세션 키를 유도하여 통신하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **인증기관 (CA)** | 사설 PKI 또는 SPIFFE 기반으로 **워크로드 인증서를 자동 발급 및 수명주기 갱신 관리** | Trust Anchor |
| **클라이언트 인증서/개인키**| 클라이언트 워크로드의 신원을 증명하는 **X.509 인증서와 개인키 기반 전자서명 생성** | 클라이언트 신원 |
| **서버 인증서/개인키** | 서버 도메인/서비스 신원을 나타내는 **X.509 인증서와 ECDHE 키 교환용 개인키** | 서버 신원 |
| **신뢰 저장소 (Trust Store)**| 상대방 인증서 체인의 유효성을 검증하기 위해 **로컬에 보관하는 공통 CA 인증서 목록** | 검증 기준 정본 |
| **대칭 세션 키** | 상호 인증 완료 후 키 교환을 통해 생성된 **전송 구간 초고속 대칭 암호화 키 (AES-GCM)** | 기밀성/무결성 |

#### 한줄 요약
- CA 신뢰 앵커, 클라이언트/서버 X.509 인증서, 신뢰 저장소, 대칭 세션 키가 결합된다.

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
- ClientHello → ServerHello/CertRequest → 서버 검증 → 클라이언트 CertVerify 전송 → 상호 인증 완료 순으로 수립된다.

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

- 대고객 웹은 **단방향 TLS**, 서비스 간 통신은 **mTLS** 선택

#### 한줄 요약
- mTLS는 양방향 X.509 인증서 검증을 통해 기계 신원을 보증하며, 서비스 메시 자동화와 결합하여 제로 트러스트를 실현하는 핵심 전송 보안 기술이다.
