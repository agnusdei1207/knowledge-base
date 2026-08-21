---
sidebar:
  order: 10
  label: "010. CRL•OCSP 인증서 폐지 (CRL OCSP Certificate Revocation)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증서 실시간 유효성 및 폐기 검증 : CRL 및 OCSP (Certificate Revocation Mechanisms)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 10
extra:
  question_no: "010"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "CRL(배포점/주기적 서명), OCSP(RFC 6960/실시간 응답), OCSP Stapling(RFC 6066), Must-Staple 및 Soft-fail/Hard-fail"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **인증서 폐기(Certificate Revocation)**: 발급된 X.509 인증서가 유효기간(Validity) 만료 이전이라도 개인키 유출, 퇴사, 도메인 소유권 변경, CA 오발급 등의 사유로 신뢰성을 상실했을 때 해당 인증서의 효력을 영구 무효화하는 절차.
- **인증서 폐기 목록(Certificate Revocation List, CRL / RFC 5280)**: CA가 폐기된 인증서들의 일련번호(Serial Number)와 폐기 일시를 모아 주기적으로 전자서명하여 배포하는 정적 목록 파일.
- **온라인 인증서 상태 프로토콜(Online Certificate Status Protocol, OCSP / RFC 6960)**: 클라이언트가 특정 인증서 1건의 폐기 상태를 질의하면 CA 응답 서버가 실시간으로 서명된 상태(Good, Revoked, Unknown)를 반환하는 1:1 경량 프로토콜.

</details>

- 정의/개념: 인증서의 실시간 신뢰성을 보장하기 위해 주기적 일괄 파일 배포 방식의 **CRL(인증서 폐기 목록)** 과 실시간 개별 조회 방식의 **OCSP(온라인 상태 프로토콜)** 및 웹 서버가 응답을 동봉하는 **OCSP Stapling** 을 결합한 **인증서 효력 무효화 검증 체계**
- 배경/필요성: 인증서 유효기간 만료일만 확인하는 정적 검증 시, 해킹 등으로 개인키가 유출된 도난 인증서를 통한 중간자 도청 및 피싱 사이트 개설을 차단할 수 없는 보안 취약점을 해소할 요구

#### 한줄 요약
- 만료 전 유출·오발급된 인증서를 즉시 무효화하기 위해 CRL 파일 및 실시간 OCSP/Stapling 검증을 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OCSP 스테이플링(OCSP Stapling / RFC 6066)**: 클라이언트가 CA의 OCSP 서버에 직접 질의하는 대신, TLS 웹 서버가 주기적으로 CA로부터 유효한 OCSP 응답을 미리 발급받아 캐싱해 두고 TLS 핸드셰이크 시 클라이언트에 함께 동봉(Staple)하여 전달하는 고효율 확장 규격.
- **소프트 실패(Soft-fail) vs 하드 실패(Hard-fail)**: OCSP 응답 서버가 네트워크 장애 등으로 응답하지 못할 때, 가용성을 위해 연결을 허용하는 방식(Soft-fail)과 보안을 위해 연결을 전면 차단하는 방식(Hard-fail).

</details>

- **전파 지연(Propagation Delay) 극복**: 주기적 갱신(수일)으로 보안 공백이 발생하는 CRL의 한계를 실시간 1:1 질의 OCSP로 해결
- **프라이버시 보호 및 지연시간 단축 (OCSP Stapling)**: 클라이언트의 방문 사이트 이력이 CA에 노출되는 사생활 침해를 차단하고 추가 RTT 지연 제거
- **엄격한 신선도(Freshness) 보증**: OCSP 응답 내 `thisUpdate` 및 `nextUpdate` 타임스탬프를 검증하여 재전송 공격(Replay Attack) 차단

#### 한줄 요약
- 실시간 폐기 검증, OCSP Stapling 지연/프라이버시 해소, 타임스탬프 기반 재전송 방지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OCSP 응답자(OCSP Responder)**: CA의 폐기 데이터베이스와 실시간 동기화되어 클라이언트나 웹 서버의 OCSP Request에 대해 CA 개인키로 서명된 OCSP Response를 생성하는 고가용성 전용 서버.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 인증기관 (CA) 폐기 관리 시스템 (Revocation Authority DB) ]             │
│  ├─ 폐기 요청 접수 (개인키 탈취, 소유권 이전 등)                          │
│  ├─ 1. 주기적 전체 파일 생성 ──▶ [ CRL 배포점 (CDP: HTTP/LDAP) ]         │
│  └─ 2. 실시간 상태 동기화 ──────▶ [ OCSP 응답 서버 (OCSP Responder) ]     │
└───────────────────────────────────────────────┬─────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼ (OCSP Stapling: 주기적 응답 선발급)                          ▼ (직접 질의: Legacy OCSP)
┌─────────────────────────────────────────────────┐           ┌─────────────────────────────────┐
│ [ TLS 웹 서버 (Origin Web Server) ]             │           │ [ 레거시 클라이언트 (Browser) ] │
│  ├─ OCSP Response 주기적 갱신 및 캐싱 (1시간)   │           │  └─ OCSP 서버에 직접 질의      │
│  └─ TLS Handshake 시 Certificate + OCSP 동봉    │           └────────────────┬────────────────┘
└────────────────────────┬────────────────────────┘                            │
                         │                                                     │
                         ▼ (3. TLS 핸드셰이크 시 원스톱 전달)                  │
┌──────────────────────────────────────────────────────────────────────────────▼────────────────┐
│ [ 클라이언트 검증 엔진 (Relying Party / Browser) ]                                             │
│  ├─ 1. CA 서명 유효성 및 인증서 체인 검증                                                    │
│  ├─ 2. OCSP 응답의 CA 서명 검증 및 thisUpdate / nextUpdate 신선도 대조                      │
│  └─ 3. [Revoked 판정 시 즉시 차단] / [Good 판정 시 TLS 세션 연결 수립]                       │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

선의 의미: CA의 폐기 DB로부터 CRL과 OCSP가 생성되고, 웹 서버가 OCSP 응답을 미리 받아 클라이언트에 동봉(Stapling)하여 클라이언트가 원스톱으로 폐기 여부를 검증하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **CA 폐기 데이터베이스** | 신고 접수된 인증서의 일련번호, 폐기 일시 및 사유 코드(Reason Code) 관리 | Revocation DB |
| **CRL 배포점 (CDP)** | 전체 폐기 목록을 바이너리 파일(`.crl`)로 묶어 주기적으로 서명 배포하는 저장소 | RFC 5280 CDP |
| **OCSP 응답 서버** | 특정 일련번호 질의에 대해 `Good/Revoked/Unknown` 서명 응답을 실시간 전송 | RFC 6960 OCSP |
| **웹 서버 (Stapling)** | 주기적으로 OCSP 응답을 수신 캐싱하여 TLS 연결 시 클라이언트에 동봉 전송 | RFC 6066 Stapling |
| **클라이언트 검증기** | 수신된 OCSP 응답의 서명과 신선도(`nextUpdate`)를 검증하여 세션 차단/허용 판정 | Relying Party |

#### 한줄 요약
- CA 폐기 DB, CRL 배포점(CDP), OCSP 응답기, 웹 서버 스테이플링 캐시, 클라이언트 검증기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OCSP Must-Staple(RFC 7633)**: 인증서 발급 시 확장 필드에 `id-pe-tlsfeature (status_request)`를 강제 포함하여, 서버가 OCSP Stapling 응답을 동봉하지 않을 경우 클라이언트가 무조건 연결을 거부(Hard-fail)하도록 강제하는 보안 강화 규격.

</details>

```text
1. 사용자가 웹 브라우저로 HTTPS 사이트 접속 요청 (TLS ClientHello + status_request 확장 포함)
            │
            ▼
2. 웹 서버가 미리 CA로부터 발급받아 캐싱해 둔 유효한 OCSP Response를 Certificate 메시지에 동봉하여 전송 (OCSP Stapling)
            │
            ▼
3. 브라우저가 수신된 OCSP 응답의 CA 전자서명 무결성 검증
            │
            ▼
4. [신선도 검증] 현재 UTC 시각이 `thisUpdate`와 `nextUpdate` 타임스탬프 유효 범위 내인지 확인
            │
            ├─ [Revoked 판정 또는 Must-Staple 누락] ➔ 보안 경고 발생 및 즉시 연결 차단
            ▼
5. [Good 판정 및 검증 성공] ➔ 정상 통신 허용 (추가적인 OCSP 서버 외부 통신 지연 0초)
```

**동작 원리**

1. **상태 질의 요청**: 클라이언트가 TLS 핸드셰이크 시 `status_request` 확장을 통해 스테이플링 의사 표명
2. **캐시된 응답 회신**: 웹 서버가 자체 캐시된 OCSP 응답(CA 서명 완료본)을 Certificate와 함께 반환
3. **서명 및 신뢰 검증**: 클라이언트가 공인 CA의 공개키로 OCSP 응답 자체의 암호학적 서명 대조
4. **유효 기간 점검**: 응답의 만료 시각(`nextUpdate`)을 점검하여 오래된 응답(Replay) 공격 차단
5. **즉시 인가 완결**: 별도 DNS 질의 및 OCSP 서버 접속 없이 로컬에서 폐기 검증을 즉각 완료

#### 한줄 요약
- ClientHello 확장 요청, OCSP Stapling 응답 회신, CA 서명 검증, 타임스탬프 신선도 대조, 연결 인가/차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **인증서 폐기 검증 메커니즘 비교**: 전통적 정적 파일 CRL, 실시간 질의 OCSP, 현대 웹 표준 OCSP Stapling의 비교.

</details>

| 비교 항목 | 인증서 폐기 목록 (CRL) | 온라인 상태 프로토콜 (OCSP) | OCSP 스테이플링 (OCSP Stapling) |
|:---|:---|:---|:---|
| **검증 메커니즘** | **전체 폐기 파일 일괄 다운로드** | **특정 일련번호 1건 실시간 질의** | **웹 서버가 미리 받아 클라이언트에 동봉** |
| **실시간성 (신선도)**| 낮음 (갱신 주기 수일~수주 지연) | **매우 높음 (실시간 질의)** | **높음 (수 시간 단위 캐싱 갱신)** |
| **네트워크 오버헤드**| **극심함 (파일 크기 수십 MB 증가)** | 중간 (접속 시마다 추가 RTT 발생)| **최저 (TLS 핸드셰이크에 포함, 0 RTT)**|
| **프라이버시 보호** | 양호 (단순 파일 다운로드) | **취약 (CA가 방문 도메인 도청 가능)**| **완벽 (클라이언트가 CA에 미접속)** |
| **서버 장애 시 영향**| 파일 캐시로 가용성 유지 | OCSP 서버 다운 시 Soft-fail 우회 | 서버가 캐시하므로 CA 장애 영향 극소화 |

#### 한줄 요약
- CRL은 무거운 정적 파일, OCSP는 실시간이나 프라이버시 침해, OCSP Stapling은 지연과 사생활을 완벽 해결한 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OCSP 소프트 실패 우회 공격(Soft-fail Bypass)**: 공격자가 피해자의 트래픽을 도청/변조할 때, 피해자 브라우저가 CA의 OCSP 서버로 보내는 폐기 확인 패킷을 방화벽이나 DNS 차단으로 고의 드롭시켜, 브라우저가 Soft-fail 정책에 따라 유출된 도난 인증서를 정상 승인하게 만드는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공격자가 OCSP 통신을 고의 차단하여 Soft-fail을 유도하는 **도난 인증서 우회 공격** | 인증서에 **OCSP Must-Staple(RFC 7633) 확장을 주입하고 웹 서버 Stapling 의무화** | 스테이플링 미동봉 시 무조건 차단(Hard-fail)하여 우회 공격 원천 봉쇄 |
| 브라우저가 모든 접속마다 OCSP 서버를 직접 찔러 발생하는 **웹 로딩 지연 및 CA 트래픽 폭주** | 웹 서버 엔진(Nginx/Apache/Envoy)에 **`ssl_stapling on` 및 캐시 자동 갱신 구성** | 폐기 검증 레이턴시 0ms 달성 및 브라우저 개인정보(방문 기록) 보호 |
| 폐쇄망/오프라인 엔터프라이즈 환경에서 외부 인터넷 단절로 인한 **OCSP 질의 실패 장애** | 사내망에 **폐기 전용 분할 CRL(Partitioned CRL / Delta CRL) 배포 시스템** 구축 | 오프라인 인트라넷 환경에서 100% 무중단 인증서 폐기 검증 보장 |

#### 한줄 요약
- Must-Staple로 Soft-fail을 방어하고, 서버 Stapling으로 지연을 없애며, Delta CRL로 오프라인 폐기 검증을 보장한다.

## Ⅶ. 결론

- 공개키 기반구조의 보안 완결성을 결정짓는 **인증서 폐기 검증 아키텍처**는 도난되거나 오발급된 인증서의 악용을 차단하는 핵심 킬 스위치이며, 실무 구현 시 **웹 서비스 전역의 OCSP Stapling 활성화**, **고보안 도메인의 OCSP Must-Staple 표준 적용**, **내부망 Delta CRL 및 단축된 인증서 수명주기(90일) 전환**을 결합하여 폐기 검증 사각지대가 없는 고신뢰 신원 증명 체계를 완성

#### 한줄 요약
- OCSP Stapling과 Must-Staple 및 단기 인증서 수명주기 관리를 결합하여 무결점 인증서 폐기 검증을 실현한다.
