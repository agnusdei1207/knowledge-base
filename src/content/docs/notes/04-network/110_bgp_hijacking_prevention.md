---
sidebar:
  order: 110
  label: "110. BGP 하이재킹 방지"
  badge:
    text: "미출 · 50%"
    variant: note
title: "인터넷 경로 탈취 방어 및 라우팅 보안 : BGP 하이재킹 방지"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: BGP의 신뢰 기반 취약성을 극복하기 위해 **RPKI 전자서명(ROA)과 라우터 ROV 검증으로 비인가 BGP 경로 공시를 탐지·폐기하는 인터넷 라우팅 보안 기술**
- 배경/필요성: 인증 없는 BGP의 신뢰 모델로 인한 **허위 BGP 광고를 통한 글로벌 인터넷 트래픽 가로채기(MITM), 암호화폐 탈취 및 통신 두절 사고 방어 불가**

#### 한줄 요약
- RPKI 전자서명과 라우터의 ROV 검증 및 Drop Invalid 정책을 통해 허위 BGP 광고를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ROA (Route Origin Authorization)**: 특정 IP 접두어(Prefix)와 최대 길이(MaxLength)를 공시할 수 있는 정당한 원점 AS 번호를 명시한 암호 서명 객체.
- **ROV (Route Origin Validation, RFC 6811)**: 라우터가 수신한 BGP Update의 Origin AS와 Prefix를 ROA 데이터와 대조하여 Valid, Invalid, NotFound로 판정하는 기법.

</details>

- **암호학적 주소 소유권 증명(ROA)**: RIR의 신뢰 앵커(Trust Anchor)를 통해 **IP 주소 대역과 합법적 Origin AS 간의 매핑 보증**
- **실시간 라우팅 유효성 검증(ROV)**: 라우터가 수신한 BGP 광고를 **VRP 테이블과 대조하여 유효성을 3단계(Valid/Invalid/NotFound)로 판정**
- **Drop Invalid 정책 기반 원천 차단**: 검증 결과가 **Invalid로 판정된 악성 경로는 BGP 라우팅 테이블 적재를 즉시 거부 및 폐기**

#### 한줄 요약
- ROA 암호 서명, 실시간 ROV 유효성 판정, Drop Invalid 원천 폐기 정책을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RTR (RPKI to Router Protocol, RFC 8210)**: RPKI Validator가 검증된 ROA 페이로드(VRP)를 로컬 보더 라우터로 실시간 전달하는 경량 전송 프로토콜.

</details>

```text
[RPKI 및 ROV 기반 BGP 하이재킹 방어 아키텍처]
|-- RIR Trust Anchors (APNIC/KISA: X.509 Root CA 및 ROA 전역 저장소)
`-- Local RPKI Validator (Routinator: ROA 암호 서명 검증 및 VRP 캐시 생성)
    `-- RTR Protocol (TCP 8282 / SSH: 검증된 VRP 테이블 라우터로 실시간 푸시)
`-- Border BGP Routers (코어 라우터)
    |-- External eBGP Peers (외부 피어로부터 BGP Update 수신)
    |-- ROV Engine (수신 경로와 VRP 대조: Valid / Invalid / NotFound)
    `-- BGP Policy Filter (Drop Invalid 정책: Invalid 경로 즉각 폐기)
```

선의 의미: RIR 저장소의 ROA 데이터가 로컬 Validator에서 검증되어 RTR 프로토콜을 통해 보더 라우터로 전달되고 라우터가 Invalid BGP 광고를 즉시 차단하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **RIR Trust Anchor** | KISA/APNIC 등 최상위 기관의 **RPKI 루트 인증서 및 ROA 글로벌 저장소** | Global Repository |
| **RPKI Validator** | ROA 파일 다운로드, **암호 서명 체인 검증 및 VRP 캐시 목록 생성** | Routinator |
| **RTR 프로토콜** | 라우터와 검증기 간 세션을 통해 **VRP 목록을 고속 증분 동기화** | RFC 8210 |
| **ROV 필터 엔진** | 수신된 BGP 경로의 **Origin AS와 Prefix를 VRP와 대조하여 유효성 판정** | Route Validation |
| **BGPsec (RFC 8205)**| 원점뿐만 아니라 **BGP AS-Path 전체 경로의 위변조를 방지하는 확장 규격** | AS-Path Signing |

#### 한줄 요약
- RIR Trust Anchor, RPKI Validator, RTR 프로토콜, 라우터 ROV 필터, BGPsec이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Drop Invalid**: ROV 판정 결과 `Invalid`로 분류된 경로는 BGP RIB에 올리지 않고 즉시 Drop 처리하는 모범 운영 표준(BCP).

</details>

```text
ROA 서명 등록, BGP 하이재킹 인입, ROV 검증 및 Drop Invalid 파이프라인
        │
   1. [ROA 서명 등록] 주소 소유자가 RPKI 포털에서 '203.0.113.0/24 ➔ AS 64500, MaxLength /24' 등록
        │
   2. [하이재킹 공격 공시] 공격자(AS 666)가 인터넷에 '203.0.113.0/24 ➔ AS 666' 허위 BGP Update 공시
        │
   3. [ROV 실시간 대조] ISP 라우터가 수신한 경로를 로컬 RPKI Validator의 VRP 테이블과 대조
        │
   ├─ [Origin AS 불일치 감지: AS 666 != AS 64500] ➔ 검증 상태 'Invalid' 태깅
   ▼
4. [Drop Invalid 즉시 차단] ISP 라우터가 공격자의 허위 경로 적재를 즉각 거부하고 패킷 폐기
        │
   ▼
5. [정상 경로 수렴] 정당한 원점(AS 64500) 경로만 Best Path로 유지되어 트래픽 탈취 원천 방어
```

#### 한줄 요약
- ROA 등록 → 허위 BGP 광고 인입 → RPKI 대조 → Invalid 판정 및 즉시 폐기 → 정상 경로 유지 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Origin Hijack** vs **Sub-Prefix Hijack** vs **Route Leak**.

</details>

| 공격 유형 | 단순 원점 하이재킹 (Origin Hijack) | 서브넷 탈취 (Sub-Prefix Hijack) | 경로 누출 (Route Leak) |
|:---|:---|:---|:---|
| **공격 메커니즘** | 타인의 `/24` 대역을 자신의 AS 번호로 공시 | 타인의 `/22` 대역을 `/24`로 쪼개어 공시 | 피어로부터 받은 경로를 상류 Provider로 재광고 |
| **탈취 성공 요인** | AS-Path 길이가 더 짧은 지역 트래픽 탈취 | **최장 접두어 일치(LPM)로 전 세계 트래픽 100% 탈취** | 고대역폭 피어 경로로 글로벌 트래픽 유입 |
| **RPKI ROV 방어력**| **100% 차단 (Origin AS 불일치로 Invalid)** | **100% 차단 (MaxLength 초과로 Invalid)** | **ROV 단독 방어 불가 (RFC 9234 OTC 필요)**|
| **실제 발생 사례** | 2008년 파키스탄 텔레콤 유튜브 차단 | 2018년 MyEtherWallet DNS 가로채기 | 2017년 구글 경로 누출로 인한 일본 인터넷 마비 |

#### 한줄 요약
- Origin/Sub-Prefix 탈취는 RPKI/ROV로 100% 방어하며, Route Leak은 RFC 9234 OTC 정책으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RFC 9234 OTC (Only to Customer)**: BGP 라우팅 시 고객(Customer) 또는 피어로부터 수신한 경로를 상류 Provider에게 잘못 재광고하는 경로 누출을 차단하는 BGP 확장 속성.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| RPKI 미지원 ISP를 경유한 허위 BGP 광고의 글로벌 확산 및 트래픽 탈취 | **전 글로벌 ISP의 `'Drop Invalid' 정책 의무화 및 MANRS` 가입** | 악성 BGP 공시의 전 세계 전파 차단 및 신뢰 라우팅 구축 |
| 피어링 관계 위반으로 발생하는 대규모 **BGP 경로 누출(Route Leak)** | **`RFC 9234 BGP 역할 협상 및 OTC(Only to Customer) 속성 검증`** | 비인가 경로 재광고 차단 및 트래픽 블랙홀 사고 예방 |
| RPKI Validator와 라우터 간 세션 단절 시 BGP 검증 중단 및 서비스 장애 | **`RPKI Validator 이중화` 및 Fail-Safe(기존 VRP 테이블 유지)** | Validator 장애 시에도 무중단 라우팅 보장 |
| MaxLength 설정 오류로 인한 정상 서브넷 광고의 오차단 | **ROA 등록 시 `MaxLength를 실제 광고 접두어 길이로 엄격 일치`** | 서브넷 위조 공격 방어 및 정상 경로 오차단 방지 |

#### 한줄 요약
- MANRS/Drop Invalid로 글로벌 전파를 막고, RFC 9234 OTC로 경로 누출을 방지하며, Validator 이중화로 가용성을 확보한다.

## Ⅶ. 결론

- 글로벌 인터넷 인프라를 겨냥한 국가 단위 APT 공격 및 금융 트래픽 탈취를 방어하기 위해 **RPKI 기반의 BGP 하이재킹 방어 체계를 필수 보안 표준으로 도입**하되, 실무 구축 시 **정확한 ROA 발행 및 MaxLength 최소화, 에지 라우터의 Drop Invalid 정책 적용, RFC 9234 기반 경로 누출 방지 및 장기적 BGPsec 전환**을 통합 추진하여 무결점 인터넷 라우팅 인프라 완성

#### 한줄 요약
- BGP 하이재킹 방지는 RPKI/ROA 전자서명과 에지 라우터 ROV 검증 및 OTC 필터를 통해 고신뢰 BGP 라우팅을 실현하는 핵심 기술이다.