---
sidebar:
  order: 110
  label: "110. BGP 하이재킹 방지"
  badge:
    text: "미출 · 50%"
    variant: note
title: "인터넷 경로 탈취 방어 및 라우팅 보안 : BGP 하이재킹 방지"
date: "2026-08-26T14:21:55+09:00"
tags:
  - "notes-network"
weight: 110
extra:
  question_no: "110"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "RPKI(ROA 서명), ROV(경로 기원 검증), BGPsec, 최장 접두어 일치(LPM) 탈취 방어 및 경로 누출(Route Leak) 차단"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **BGP Hijacking**: 권한이 없는 자율 시스템(AS)이 타인의 IP 대역을 허위 공시하여 전 세계 트래픽을 가로채거나 폐기하는 공격.
- **RPKI (Resource PKI, RFC 6480)**: 대륙별 주소 관리 기구(RIR)가 X.509 인증서 체계로 IP 블록과 AS 번호의 정당한 소유권을 암호학적으로 증명하는 인프라.

</details>

- 정의/개념: **RPKI·ROA·ROV**로 비인가 BGP 경로를 차단하는 기술
- 배경/필요성: BGP는 광고된 경로의 기원을 검증하지 않아 **허위 광고가 전역으로 퍼진 뒤 사람이 되돌리는 비용**을 치르므로, RIR이 서명한 ROA를 정본으로 두고 라우터가 수신 시점에 대조해 무효 경로를 즉시 폐기

#### 한줄 요약
- RPKI 전자서명과 라우터의 ROV 검증 및 Drop Invalid 정책을 통해 허위 BGP 광고를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ROA (Route Origin Authorization)**: 특정 IP 접두어(Prefix)와 최대 길이(MaxLength)를 공시할 수 있는 정당한 원점 AS 번호를 명시한 암호 서명 객체.
- **ROV (Route Origin Validation, RFC 6811)**: 라우터가 수신한 BGP Update의 Origin AS와 Prefix를 ROA 데이터와 대조하여 Valid, Invalid, NotFound로 판정하는 기법.

</details>

- **ROA 소유권 증명**: Prefix와 합법적 Origin AS 매핑
- **ROV 검증**: VRP 대조로 Valid·Invalid·NotFound 판정
- **Drop Invalid**: Invalid 경로의 RIB 적재 거부

#### 한줄 요약
- ROA 암호 서명, 실시간 ROV 유효성 판정, Drop Invalid 원천 폐기 정책을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RTR (RPKI to Router Protocol, RFC 8210)**: RPKI Validator가 검증된 ROA 페이로드(VRP)를 로컬 보더 라우터로 실시간 전달하는 경량 전송 프로토콜.

</details>

```text
[BGP 경로 검증 정적 구성]
|-- RIR Trust Anchor
|-- RPKI Validator
|-- RTR 프로토콜
|-- ROV 필터 엔진
`-- BGPsec
```

선의 의미: RIR 저장소의 ROA 데이터가 로컬 Validator에서 검증되어 RTR 프로토콜을 통해 보더 라우터로 전달되고 라우터가 Invalid BGP 광고를 즉시 차단하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| RIR Trust Anchor | **루트 인증서·ROA 저장소** | Global Repository |
| RPKI Validator | **서명 검증·VRP 생성** | Routinator |
| RTR 프로토콜 | **VRP 증분 동기화** | RFC 8210 |
| ROV 필터 엔진 | **Origin AS·Prefix 검증** | Route Validation |
| BGPsec | **AS-Path 서명 검증** | RFC 8205 |

#### 한줄 요약
- Validator가 RPKI 저장소 검증을 대신 수행하고 라우터에는 RTR로 판정 결과만 넘기므로, 라우터는 암호 연산 부담 없이 필터링만 집행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Drop Invalid**: ROV 판정 결과 `Invalid`로 분류된 경로는 BGP RIB에 올리지 않고 즉시 Drop 처리하는 모범 운영 표준(BCP).

</details>

```text
주소 소유자 등록
    |
1. ROA 서명 등록
    |
2. BGP Update 수신
    |
3. ROV·VRP 대조
    +-- 불일치: Invalid
    |
4. Drop Invalid 차단
    |
5. 정상 경로 수렴
    |
라우팅 결과
```

- 1. ROA 서명 등록
- 2. BGP Update 수신
- 3. ROV·VRP 대조
- 4. Drop Invalid 차단
- 5. 정상 경로 수렴

#### 한줄 요약
- ROV 판정에서 수용과 즉시 폐기로 갈리며, Drop Invalid를 켜는 대가로 ROA 등록이 누락된 정상 경로까지 함께 끊길 위험을 감수한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Origin Hijack** vs **Sub-Prefix Hijack** vs **Route Leak**.

</details>

| 공격 유형 | 단순 원점 하이재킹 (Origin Hijack) | 서브넷 탈취 (Sub-Prefix Hijack) | 경로 누출 (Route Leak) |
|:---|:---|:---|:---|
| 공격 메커니즘 | 타 대역을 자기 AS로 공시 | 더 긴 Prefix 공시 | 피어 경로를 상류에 재광고 |
| 탈취 성공 요인 | 짧은 AS-Path | **최장 접두어 일치** | 피어 경로 유입 |
| RPKI ROV 방어력 | **Origin 불일치 차단** | **MaxLength 초과 차단** | **ROV 불가·OTC 필요** |
| 실제 발생 사례 | 유튜브 경로 탈취 | MyEtherWallet 탈취 | 구글 경로 누출 |

#### 한줄 요약
- Origin/Sub-Prefix 탈취는 RPKI/ROV로 100% 방어하며, Route Leak은 RFC 9234 OTC 정책으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RFC 9234 OTC (Only to Customer)**: BGP 라우팅 시 고객(Customer) 또는 피어로부터 수신한 경로를 상류 Provider에게 잘못 재광고하는 경로 누출을 차단하는 BGP 확장 속성.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 미검증 ISP를 통한 허위 경로 확산 | **Drop Invalid·MANRS** | 악성 공시 전파 차단 |
| 피어링 위반의 경로 누출 | **RFC 9234 역할·OTC** | 재광고 차단 |
| Validator 세션 단절 | **Validator 이중화·VRP 유지** | 검증 가용성 확보 |
| MaxLength 오류로 정상 경로 차단 | **실제 Prefix 길이 일치** | 오차단 방지 |

#### 한줄 요약
- MANRS/Drop Invalid로 글로벌 전파를 막고, RFC 9234 OTC로 경로 누출을 방지하며, Validator 이중화로 가용성을 확보한다.

## Ⅶ. 결론

- 기원 탈취는 **RPKI·ROV**, 경로 누출은 **RFC 9234 OTC** 적용

#### 한줄 요약
- BGP 하이재킹 방지는 RPKI/ROA 전자서명과 에지 라우터 ROV 검증 및 OTC 필터를 통해 고신뢰 BGP 라우팅을 실현하는 핵심 기술이다.
