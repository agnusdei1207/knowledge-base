---
sidebar:
  order: 10
  label: "010. CRL•OCSP 인증서 폐지"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증서 실시간 유효성 및 폐기 검증 : CRL 및 OCSP"
date: "2026-08-26T14:42:16+09:00"
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

- 정의/개념: 만료 전 인증서 효력을 판정하는 **CRL·OCSP 폐기 검증 기술**
- 배경/필요성: 인증서는 발급 시점의 판단을 만료일까지 그대로 굳혀 두는 사본이라 그 사이 사정이 바뀌어도 반영되지 않으므로, 유효기간을 짧게 끊어 재발급 비용을 늘리는 대신 발급 상태를 뒤집는 폐기 정보를 별도 계층으로 배포해 검증 시점의 최신 판단을 대신 공급할 필요

#### 한줄 요약
- CRL 목록과 OCSP 실시간 질의 및 스테이플링을 통해 무효화된 인증서의 통신을 즉시 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OCSP Stapling (RFC 6066)**: 웹 서버가 CA로부터 OCSP 응답을 미리 발급받아 캐시해 두고 TLS 핸드셰이크 시 클라이언트에 동봉하여 지연과 프라이버시 침해를 해결하는 기술.
- **Soft-fail vs Hard-fail**: 폐기 확인 서버 접속 실패 시 통신을 허용하는 Soft-fail 정책과 연결을 즉시 차단하는 Hard-fail 정책.

</details>

- 인증서별 **Good·Revoked·Unknown** 상태 판정
- **OCSP Stapling**으로 추가 질의 지연 제거
- CA 직접 질의를 없애 **방문 정보 노출 방지**

#### 한줄 요약
- 스테이플링은 폐기 조회 비용을 클라이언트에서 서버의 주기적 갱신으로 옮긴 것이라, 응답의 신선도는 실시간이 아니라 서버 캐시 주기만큼 뒤처진다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CDP (CRL Distribution Point)**: X.509 인증서 내에 명시되어 클라이언트가 최신 CRL 파일을 다운로드할 수 있는 HTTP/LDAP URL.

</details>

```text
인증서 폐기 검증 체계
|-- CA 폐기 데이터베이스
|   |-- CRL 생성기
|   `-- OCSP 응답 서버
|-- CRL 배포점
|-- 웹 서버 스테이플링 캐시
`-- 클라이언트 검증기
```

선의 의미: CA의 폐기 DB로부터 CRL과 OCSP가 생성되고 웹 서버가 OCSP 응답을 미리 받아 클라이언트에 동봉하여 클라이언트가 원스톱으로 폐기 여부를 검증하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| CA 폐기 데이터베이스 | 인증서 **일련번호·폐기 사유** 관리 | Revocation DB |
| CRL 배포점 (CDP) | 서명된 **CRL 파일** 주기적 배포 | RFC 5280 CDP |
| OCSP 응답 서버 | 일련번호별 **상태 응답** 서명 | RFC 6960 OCSP |
| 웹 서버 (Stapling) | **OCSP 응답** 캐시·TLS 동봉 | RFC 6066 Stapling |
| 클라이언트 검증기 | 응답 **서명·신선도** 검증 | Relying Party |

#### 한줄 요약
- 폐기 사실의 정본은 CA의 DB 하나뿐이고 CRL·OCSP·스테이플링 캐시는 그것을 각기 다른 신선도로 복제한 사본 계층이므로, 어느 사본을 보느냐가 곧 판정 지연 시간을 결정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OCSP Must-Staple (RFC 7633)**: 인증서에 해당 확장을 주입하여 서버가 OCSP Stapling 응답을 누락할 경우 클라이언트가 무조건 연결을 차단(Hard-fail)하도록 강제하는 표준.

</details>

```text
OCSP Stapling 요청, CA 서명 검증, 신선도 대조 및 연결 차단/허용 파이프라인
        │
       [ClientHello status_request]
        │
   1. [OCSP 응답 동봉]
        │
   2. [CA 전자서명 검증]
        │
   3. [신선도 대조]
        │
   ├─ [Revoked 판정 또는 Must-Staple 누락] ➔ 보안 경고 발생 및 즉시 연결 차단
   ▼
       [Good 판정 시 통신 허용]
```

- 1. OCSP 응답 동봉
- 2. CA 전자서명 검증
- 3. 신선도 대조

#### 한줄 요약
- 응답이 오지 않은 경우를 허용으로 볼지 차단으로 볼지가 갈림길로, Must-Staple은 가용성을 포기하고 확인되지 않은 상태를 위험으로 간주하는 쪽을 택한 설정이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CRL** vs **OCSP** vs **OCSP Stapling**.

</details>

| 비교 항목 | 인증서 폐기 목록 (CRL) | 온라인 상태 프로토콜 (OCSP) | OCSP 스테이플링 (OCSP Stapling) |
|:---|:---|:---|:---|
| 검증 메커니즘 | **전체 폐기 목록** 다운로드 | 인증서별 **실시간 질의** | 서버가 **응답을 동봉** |
| 실시간성 | 갱신 주기에 따른 지연 | 질의 시점의 **최신 상태** | 캐시된 **응답 신선도** 의존 |
| 네트워크 부하 | 목록 크기에 비례 | 접속마다 **추가 RTT** | TLS에 포함해 **추가 질의 제거** |
| 프라이버시 | 방문 대상 비노출 | CA에 **방문 정보 노출** | CA 직접 질의 제거 |
| 장애 영향 | 파일 캐시로 검증 | 장애 시 **Soft-fail** 가능 | 캐시 만료 전 검증 |

#### 한줄 요약
- 셋은 같은 폐기 정보를 누가 언제 가져오느냐만 달리한 해법으로, CRL은 클라이언트의 저장 부담, OCSP는 접속마다의 RTT와 방문 노출, 스테이플링은 서버 캐시 주기만큼의 신선도를 각각 대가로 치른다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Soft-fail Bypass**: 공격자가 OCSP 서버로의 네트워크 패킷을 방화벽으로 차단하여 브라우저가 Soft-fail 정책에 따라 탈취된 도난 인증서를 통과시키게 만드는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| OCSP 차단으로 **Soft-fail 우회** | **Must-Staple** 적용 | 응답 누락 시 Hard-fail 차단 |
| 직접 질의로 **추가 RTT** 발생 | 서버 **Stapling 캐시** 갱신 | 지연·방문 정보 노출 감소 |
| 폐쇄망에서 **OCSP 질의 실패** | **Delta CRL** 내부 배포 | 외부 연결 없이 폐기 검증 |
| 응답 서명키 유출로 Good 위조 | 단기 **OCSP 서명 인증서** 적용 | 서명키 피해 기간 제한 |

#### 한줄 요약
- Must-Staple로 Soft-fail을 방어하고, 서버 Stapling으로 지연을 없애며, Delta CRL로 오프라인 폐기 검증을 보장한다.

## Ⅶ. 결론

- 인터넷 서비스는 **OCSP Stapling**, 폐쇄망은 **Delta CRL** 선택

#### 한줄 요약
- 인증서 폐기 검증은 OCSP Stapling과 Must-Staple 및 단기 수명주기 관리를 결합하여 유출된 무효 인증서의 악용을 완벽 차단하는 핵심 메커니즘이다.
