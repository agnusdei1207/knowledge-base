---
sidebar:
  order: 7
  label: "007. PKI 공개키 기반구조"
  badge:
    text: "기출 · 70%"
    variant: note
title: "공개키 신뢰 사슬 및 인증서 생명주기 관리 : PKI"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 7
extra:
  question_no: "7"
  source_status: "기출"
  source_history: "120회, 138회"
  priority: 70
  priority_note: "Root CA/Intermediate CA 계층 신뢰 체인(RFC 5280), RA의 소유권 증명(PoP), CRL/OCSP 폐기 및 X.509 수명주기"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PKI (Public Key Infrastructure)**: 공개키가 특정 주체의 소유임을 보증하기 위해 X.509 인증서의 생성, 발급, 검증, 폐기 전 생애주기를 관리하는 신뢰 프레임워크.
- **Chain of Trust (신뢰 체인, RFC 5280)**: 최상위 Root CA부터 중간 CA를 거쳐 최종 엔티티 인증서까지 전자서명으로 이어지는 인증 경로.

</details>

- 정의/개념: 공개키와 신원을 결합하는 인증서 생명주기 체계(**PKI**)
- 배경/필요성: 개방된 인터넷 환경에서 비대칭 암호화를 사용할 때 공격자가 대상 서버의 도메인이나 공개키를 위조하여 중간자 공격(Man-In-The-Middle)을 시도할 경우 클라이언트가 수신한 공개키의 실제 소유자가 누구인지 스스로 판별할 수 없는 근본적인 신뢰성 결핍(Authenticity Problem)에 직면함에 따라, 신뢰할 수 있는 공인 인증기관(CA)이 소유자의 신원과 공개키를 암호학적으로 결속(Binding)하여 X.509 인증서를 발급하고 **신뢰 체인**(Chain of Trust)을 통해 검증 및 폐기(CRL/OCSP)를 총괄하는 공개키 기반구조(PKI: Public Key Infrastructure)를 도입하여 전 세계 인터넷 웹 보안(HTTPS/TLS), 이메일 보안(S/MIME), 코드 서명 및 사설 mTLS 인프라의 전역적 신뢰성(Global Trust)과 기밀성/무결성 보장을 달성할 필요

#### 한줄 요약
- CA 전자서명과 X.509 인증서 체인을 통해 공개키의 소유권을 공인하고 중간자 공격을 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Proof of Possession (PoP, 소유권 증명)**: 인증서 신청자가 제출한 공개키에 대응하는 개인키를 실제로 소유하고 있음을 증명하기 위해 CSR을 자체 개인키로 서명하는 절차.
- **Trust Anchor (신뢰 앵커)**: OS나 웹 브라우저에 기본 내장되어 별도의 상위 검증 없이 무조건 신뢰하는 최상위 Root CA 인증서.

</details>

- 오프라인 Root와 Issuing CA의 계층 신뢰 체인
- CSR 서명 검증을 통한 **PoP** 소유권 증명
- CRL·OCSP Stapling 기반 폐기 상태 제공

#### 한줄 요약
- 검증 비용을 앵커 한 곳으로 몰아 준 대가로 그 앵커가 단일 실패점이 되므로, Root를 오프라인에 격리하고 발급 권한만 하위 CA로 내려보내 침해 시 폐기 범위를 좁힌다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RA (Registration Authority)**: 신청자의 신원과 도메인 소유권을 실질적으로 심사하는 등록 대행 기관.

</details>

```text
[PKI 공개키 기반구조]
  │
  ├─ [인증 체인 계층]
  │    ├─ Root CA (최상위 신뢰 앵커)
  │    └─ Intermediate CA (발급 대행)
  │
  ├─ [운영 및 저장 계층]
  │    ├─ 등록 대행 기관 (RA)
  │    └─ 인증서 저장소 (CRL/OCSP)
  │
  └─ [클라이언트 신뢰점]
       └─ Trust Store (내장 루트 저장소)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Root CA | 최상위 신뢰점과 하위 CA 서명 |
| Issuing CA | 엔드 엔티티 인증서 발급 |
| **RA** | 신원·도메인·PoP 심사 |
| Certificate Repository | 인증서·CRL·OCSP 제공 |
| Trust Store | **신뢰 앵커** 보관과 경로 검증 기준 제공 |

#### 한줄 요약
- 신뢰의 뿌리는 CA가 아니라 클라이언트가 미리 품고 있는 Trust Store에 있으므로, 사설 PKI는 알고리즘이 아무리 같아도 Root를 단말에 심는 배포 비용을 따로 치러야 한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Path Validation Algorithm (경로 검증 알고리즘, RFC 5280)**: 엔드 엔티티 인증서부터 Root CA까지 서명 체인, 유효기간, Basic Constraints, Key Usage, 폐기 상태를 순차 검증하는 절차.

</details>

```text
PKI CSR 신청, 신원 심사, X.509 발급 및 체인 경로 검증 파이프라인
        │
       [CSR 생성 및 제출]
        │
   1. [신원 심사 및 PoP 검증]
        │
   2. [X.509 인증서 발급]
        │
       [인증서 제시]
        │
   ▼
   3. [인증 경로 검증]
        │
   4. [폐기 상태 확인]
```

- 1. 신원 심사 및 PoP 검증
- 2. X.509 인증서 발급
- 3. 인증 경로 검증(RFC 5280 **경로 검증 알고리즘**)
- 4. 폐기 상태 확인

#### 한줄 요약
- 발급 구간의 신원 심사는 사람이 개입하는 느리고 비싼 1회성 절차인 반면 검증 구간은 접속마다 반복되므로, 실무 부담은 심사 강화보다 폐기 확인의 조회 비용을 줄이는 쪽에 몰린다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **mTLS (mutual TLS, 상호 TLS)**: 클라이언트도 인증서를 제시해 서버와 서로 인증하는 TLS 운용으로, 사설 PKI가 발급한 워크로드 인증서를 서비스 신원으로 삼아 서비스 간 호출을 인증함.

</details>

| 비교 항목 | 글로벌 공개 웹 PKI (Web PKI) | 사설 엔터프라이즈 PKI (Private PKI) |
|:---|:---|:---|
| 신뢰 기준점 | 공개 Trust Store의 Root | 조직이 배포한 사설 Root |
| 운영 주체 | 공인 CA | 조직 내부 CA |
| 적용 영역 | 공개 HTTPS·S/MIME | 내부 **mTLS**·VPN·IoT |
| 정책 통제 | CA·브라우저 정책 준수 | 조직별 프로파일 통제 |
| 외부 호환성 | 공개 신뢰 저장소에 좌우 | Root 미배포 단말은 미신뢰 |

#### 한줄 요약
- 공개 웹 PKI는 글로벌 범용 신뢰용, 사설 PKI는 내부 통제 및 mTLS 마이크로서비스용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Certificate Transparency (CT, RFC 6962)**: CA가 인증서를 발행할 때마다 공개된 불변 분산 로그에 기록하여 부정 발급을 전 세계에 실시간 공개하는 감사 체계.
- **OCSP Stapling (RFC 6066)**: 서버가 CA의 서명된 OCSP 응답을 주기적으로 받아 TLS 핸드셰이크에 동봉해 전달하는 방식으로, 클라이언트가 CA에 직접 조회하는 왕복 지연과 방문 기록 노출을 없앰.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CA의 부정 인증서 발급 | **CT** 로그 모니터링 | 오발급 탐지 |
| Root 키 노출로 **신뢰 앵커** 침해 | 오프라인 Root와 HSM M-of-N 통제 | 키 사용 권한 분산 |
| 인증서 만료로 서비스 장애 | ACME 자동 갱신 | 수명주기 오류 완화 |
| CRL 비대화로 검증 지연 | **OCSP Stapling** | 클라이언트 직접 조회 감소 |

#### 한줄 요약
- PKI의 실무 장애는 암호가 아니라 발급 권한 남용과 만료 누락이라는 운영 사건이므로, 대책은 CA를 감시하는 외부 눈(CT)과 사람 손을 빼는 자동화(ACME)로 귀결된다.

## Ⅶ. 결론

- 전 세계 수십억 웹사이트와 클라이언트 간의 안전한 통신(HTTPS) 및 제로 트러스트 마이크로서비스 신원(mTLS)을 지탱하는 글로벌 디지털 신뢰 생태계의 가장 기본적이면서도 대체 불가능한 핵심 보안 인프라(IETF RFC 5280)로 확고히 안착하였으며, 클라우드 네이티브 ACME 자동화 및 PQC 인증서 체인으로 진화하는 가운데, 실무 PKI 인프라 구축 시에는 침해 시 전사 신뢰 마비를 방지하기 위한 Root CA의 완전 오프라인(Air-Gap) 격리 및 M-of-N 다중 서명 HSM 보관, 인증서 만료로 인한 대규모 서비스 장애를 방지하는 ACME 프로토콜 기반 자동 갱신(Let's Encrypt / Cert-Manager), 부정 인증서 오발급을 전 세계에 실시간 공개 감시하는 인증서 투명성(CT: Certificate Transparency) 및 DNS CAA 레코드 연동을 결합하여 완벽한 디지털 인증 무결성을 완성

#### 한줄 요약
- 외부 사용자에게 보이는 서비스는 공개 웹 PKI, 내부 서비스 간 mTLS는 사설 PKI로 갈라 세우고, 두 Root를 섞지 않는 것이 설계의 첫 선택이다.
