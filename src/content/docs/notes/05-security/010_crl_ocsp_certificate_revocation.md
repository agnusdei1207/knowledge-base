---
sidebar:
  order: 10
  label: "010. CRL•OCSP 인증서 폐지"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증서 실시간 유효성 및 폐기 검증 : CRL 및 OCSP"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 10
extra:
  question_no: "10"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "CRL(배포점/주기적 서명), OCSP(RFC 6960/실시간 응답), OCSP Stapling(RFC 6066), Must-Staple 및 Soft-fail/Hard-fail"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Certificate Revocation (인증서 폐기)**: 개인키 유출이나 오발급 시 유효기간 만료 전이라도 인증서 효력을 영구 무효화하는 절차.
- **CRL vs OCSP**: 정적 폐기 목록 파일 배포 방식(CRL, RFC 5280)과 1:1 실시간 상태 질의 프로토콜(OCSP, RFC 6960).

</details>

- 정의/개념: 개인키 유출이나 오발급 시 인증서의 효력을 무효화하기 위해 **정적 서명 목록(CRL)과 실시간 상태 질의(OCSP/Stapling)를 제공하는 폐기 검증 기술**
- 배경/필요성: 인증서 폐기 검증 체계 부재 시 발생하는 **도난된 개인키를 이용한 해커의 위장 사이트 개설, 유출 인증서의 무단 통신 및 중간자 공격(MITM) 방어 불가**

#### 한줄 요약
- CRL 목록과 OCSP 실시간 질의 및 스테이플링을 통해 무효화된 인증서의 통신을 즉시 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OCSP Stapling (RFC 6066)**: 웹 서버가 CA로부터 OCSP 응답을 미리 발급받아 캐시해 두고 TLS 핸드셰이크 시 클라이언트에 동봉하여 지연과 프라이버시 침해를 해결하는 기술.
- **Soft-fail vs Hard-fail**: 폐기 확인 서버 접속 실패 시 통신을 허용하는 Soft-fail 정책과 연결을 즉시 차단하는 Hard-fail 정책.

</details>

- **실시간 무효화 상태 판정**: OCSP를 통해 **특정 인증서 1건에 대해 `Good/Revoked/Unknown` 상태를 밀리초 단위로 확인**
- **OCSP Stapling을 통한 제로 레이턴시**: 웹 서버가 **CA 응답을 미리 캐싱하여 TLS 연결 시 동봉함으로써 클라이언트 지연 0ms 실현**
- **프라이버시 침해 원천 차단**: 스테이플링 적용 시 **클라이언트의 도메인 방문 기록이 CA에 실시간 노출되는 문제 완벽 해소**

#### 한줄 요약
- 실시간 상태 판정, OCSP Stapling 기반 0ms 지연, 클라이언트 프라이버시 보호를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CDP (CRL Distribution Point)**: X.509 인증서 내에 명시되어 클라이언트가 최신 CRL 파일을 다운로드할 수 있는 HTTP/LDAP URL.

</details>

```text
[인증서 폐기 검증 CRL / OCSP / OCSP Stapling 토폴로지]
|-- CA Revocation Database (폐기 접수 DB: 일련번호, 폐기일시, 사유 코드)
|   |-- 1. CRL Generator -> [ CRL 배포점 CDP: 정기 서명된 .crl 파일 ]
|   `-- 2. OCSP Responder -> [ OCSP 서버: 1:1 서명 상태 회신 Good/Revoked ]
`-- Web Server (OCSP Stapling 캐시: 주기적으로 OCSP 수신 후 TLS 핸드셰이크 동봉)
`-- Client Browser (Relying Party: CA 서명 및 nextUpdate 신선도 검증 -> 차단/허용 판정)
```

선의 의미: CA의 폐기 DB로부터 CRL과 OCSP가 생성되고 웹 서버가 OCSP 응답을 미리 받아 클라이언트에 동봉하여 클라이언트가 원스톱으로 폐기 여부를 검증하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **CA 폐기 데이터베이스** | 신고 접수된 인증서의 **일련번호, 폐기 일시 및 사유 코드(Reason Code) 관리** | Revocation DB |
| **CRL 배포점 (CDP)** | 전체 폐기 목록을 **바이너리 파일(`.crl`)로 묶어 주기적으로 서명 배포** | RFC 5280 CDP |
| **OCSP 응답 서버** | 특정 일련번호 질의에 대해 **`Good/Revoked/Unknown` 서명 응답을 실시간 전송** | RFC 6960 OCSP |
| **웹 서버 (Stapling)** | 주기적으로 **OCSP 응답을 수신 캐싱하여 TLS 연결 시 클라이언트에 동봉** | RFC 6066 Stapling |
| **클라이언트 검증기** | 수신된 OCSP 응답의 **서명과 신선도(`nextUpdate`)를 검증하여 세션 차단 판정** | Relying Party |

#### 한줄 요약
- CA 폐기 DB, CRL 배포점(CDP), OCSP 응답기, 웹 서버 스테이플링 캐시, 클라이언트 검증기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OCSP Must-Staple (RFC 7633)**: 인증서에 해당 확장을 주입하여 서버가 OCSP Stapling 응답을 누락할 경우 클라이언트가 무조건 연결을 차단(Hard-fail)하도록 강제하는 표준.

</details>

```text
OCSP Stapling 요청, CA 서명 검증, 신선도 대조 및 연결 차단/허용 파이프라인
        │
   1. [ClientHello 확장 요청] 브라우저가 HTTPS 접속 시 `status_request` 확장을 포함하여 요청
        │
   2. [OCSP 응답 동봉] 웹 서버가 캐싱해 둔 유효한 CA 서명 OCSP Response를 Certificate에 동봉 전송
        │
   3. [CA 전자서명 무결성 검증] 브라우저가 수신된 OCSP 응답의 CA 전자서명 일치 여부 확인
        │
   4. [신선도 대조] 현재 UTC 시각이 `thisUpdate`와 `nextUpdate` 타임스탬프 유효 범위 내인지 대조
        │
   ├─ [Revoked 판정 또는 Must-Staple 누락] ➔ 보안 경고 발생 및 즉시 연결 차단
   ▼
5. [Good 판정 및 검증 성공] ➔ 정상 통신 허용 (추가 외부 통신 지연 0초)
```

#### 한줄 요약
- ClientHello 확장 요청 → OCSP Stapling 응답 회신 → CA 서명 검증 → 타임스탬프 신선도 대조 → 연결 인가/차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CRL** vs **OCSP** vs **OCSP Stapling**.

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

- **Soft-fail Bypass**: 공격자가 OCSP 서버로의 네트워크 패킷을 방화벽으로 차단하여 브라우저가 Soft-fail 정책에 따라 탈취된 도난 인증서를 통과시키게 만드는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공격자가 OCSP 통신을 고의 차단하여 Soft-fail을 유도하는 **도난 인증서 우회 공격** | **`OCSP Must-Staple(RFC 7633) 확장을 주입`하고 웹 서버 Stapling 의무화** | 스테이플링 미동봉 시 무조건 차단(Hard-fail)하여 우회 원천 봉쇄 |
| 브라우저가 매 접속마다 OCSP 서버를 직접 찔러 발생하는 **웹 로딩 지연** | **`웹 서버(Nginx/Apache/Envoy) ssl_stapling 활성화` 및 캐시 자동 갱신** | 폐기 검증 지연 0ms 달성 및 브라우저 방문 기록 보호 |
| 폐쇄망 엔터프라이즈 환경에서 외부 인터넷 단절로 인한 **OCSP 질의 실패 장애** | **`사내망 전용 분할 CRL(Delta CRL) 배포 시스템` 구축** | 오프라인 인트라넷 환경에서 100% 무중단 인증서 폐기 검증 보장 |
| CA의 OCSP 응답 생성 키 유출로 인한 가짜 Good 응답 위조 | **OCSP 서명 전용 인증서의 `단기 수명주기(7일 이내)` 강제 적용** | OCSP 서명키 탈취 시 피해 범위 극소화 |

#### 한줄 요약
- Must-Staple로 Soft-fail을 방어하고, 서버 Stapling으로 지연을 없애며, Delta CRL로 오프라인 폐기 검증을 보장한다.

## Ⅶ. 결론

- 공개키 기반구조의 보안 완결성을 결정짓는 **인증서 폐기 검증 아키텍처는 도난되거나 오발급된 인증서의 악용을 차단하는 핵심 킬 스위치**이며, 실무 구현 시 **웹 서비스 전역의 OCSP Stapling 활성화, 고보안 도메인의 OCSP Must-Staple 표준 적용, 내부망 Delta CRL 및 단축된 인증서 수명주기(90일) 전환**을 결합하여 폐기 검증 사각지대가 없는 고신뢰 신원 증명 체계 완성

#### 한줄 요약
- 인증서 폐기 검증은 OCSP Stapling과 Must-Staple 및 단기 수명주기 관리를 결합하여 유출된 무효 인증서의 악용을 완벽 차단하는 핵심 메커니즘이다.