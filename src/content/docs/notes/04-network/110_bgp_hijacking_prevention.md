---
sidebar:
  order: 110
  label: "110. BGP 하이재킹 방지 (BGP Hijacking Prevention)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "인터넷 경로 탈취 방어 및 라우팅 보안 : BGP 하이재킹 방지 (RPKI & ROV)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
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

- **BGP 하이재킹(BGP Hijacking / Prefix Hijacking)**: 악의적인 공격자 또는 관리자의 실수로 인해 특정 IP 접두어(Prefix)에 대한 소유 권한이 없는 자율 시스템(AS)이 해당 IP 대역을 자신이 원점(Origin)인 것처럼 인터넷 BGP 피어들에게 허위 광고하여, 전 세계 트래픽을 가로채거나(Man-in-the-Middle) 블랙홀(Blackholing)로 폐기하는 공격.
- **RPKI(Resource Public Key Infrastructure, RFC 6480)**: 대륙별 인터넷 주소 관리 기구(RIR)가 X.509 PKI 인증서 구조를 통해 특정 IP 주소 블록 및 AS 번호의 정당한 소유권을 암호학적으로 증명하는 글로벌 공개키 기반 인프라.

</details>

- 정의/개념: BGP의 신뢰 기반 광고 모델 취약성을 보완하기 위해, **RPKI(Resource PKI)** 기반 전자서명 객체인 **ROA(Route Origin Authorization)** 를 발행하고 라우터가 수신된 BGP 경로를 실시간 검증하는 **ROV(Route Origin Validation)** 를 강제하는 **인터넷 라우팅 무결성 보안 체계**
- 배경/필요성: BGP가 라우팅 광고의 진위 여부를 자체 검증하지 않고 **최장 접두어 일치(Longest Prefix Match)** 및 짧은 AS-Path를 무조건 신뢰하는 구조적 취약점으로 인해 발생하는 금융·DNS 서비스 가로채기(Hijacking) 및 글로벌 경로 누출(Route Leak) 사고를 원천 방어할 요구

#### 한줄 요약
- RPKI 전자서명(ROA)과 라우터 ROV 검증을 통해 허위 BGP 광고와 경로 탈취를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ROA(Route Origin Authorization, RFC 9582)**: IP 주소 대역의 정당한 소유자가 "이 IP 접두어(예: 203.0.113.0/24)는 오직 AS 64500에서만 광고할 수 있으며, 최대 길이는 /24까지 허용한다(MaxLength)"를 명시하고 개인키로 서명한 암호 객체.
- **ROV 검증 상태(Validation States)**: 라우터가 수신한 BGP 경로를 RPKI 캐시와 대조하여 판정하는 3가지 상태: `Valid`(일치), `Invalid`(원점 AS 불일치 또는 MaxLength 초과 ➔ 즉시 폐기), `NotFound`(ROA 미발행).

</details>

- **암호학적 원점 권한 증명 (RPKI/ROA)**: 공인 인증기관의 전자서명을 통해 비인가 AS의 허위 IP 대역 광고를 물리적으로 판별
- **더 구체적인 접두어 탈취(Sub-Prefix Hijacking) 방어**: ROA의 `MaxLength` 속성을 통해 /24 등 하위 서브넷 쪼개기 공격을 Invalid로 판정하여 무력화
- **RFC 9234 기반 경로 누출(Route Leak) 탐지**: BGP 오픈 메시지에 `OTC(Only to Customer)` 속성을 부여하여 피어링 관계(Customer-Provider) 위반 재광고 차단

#### 한줄 요약
- RPKI/ROA 전자서명, MaxLength 기반 Sub-Prefix 방어, ROV Invalid 즉시 드롭, OTC 경로 누출 차단을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RPKI 유효성 검증기(RPKI Validator / Relying Party)**: Routinator, OctoRPKI 등의 소프트웨어 데몬으로, 글로벌 RPKI 저장소(Trust Anchors)에서 ROA 인증서를 주기적으로 동기화·검증한 후 RTR 프로토콜로 에지 라우터에 유효 목록을 푸시하는 중계기.
- **RTR 프로토콜(RPKI to Router Protocol, RFC 8210)**: RPKI Validator와 에지 BGP 라우터 간에 검증된 IP-to-AS 매핑 테이블(VRP: Validated ROA Payload)을 전달하는 경량 통신 프로토콜.

</details>

```text
[ 글로벌 RPKI 저장소 (KRNIC, APNIC, ARIN Trust Anchors) ]
                       │ (1. RPKI 인증서 및 ROA 서명 객체 동기화: HTTPS / RRDP)
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 사내 RPKI 유효성 검증기 (RPKI Validator: Routinator) ]                │
│  ├─ X.509 인증서 체인 및 ROA 암호학적 서명 검증                         │
│  └─ 유효 ROA 페이로드(VRP Table) 캐싱 생성                              │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. RTR 프로토콜: TCP 포트 8282 / SSH)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 코어 / 보더 BGP 에지 라우터 (Border Routers) ]                        │
│  ├─ 외부 eBGP 피어로부터 BGP Update 수신                                │
│  ├─ BGP 수용 정책 필터 (ROV Engine: Valid / Invalid / NotFound 판정)    │
│  └─ [Invalid 판정 시 BGP 테이블 등록 거부 및 즉시 폐기 (Drop Invalid)]  │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: RIR 저장소의 ROA 데이터가 로컬 Validator에서 검증되어 RTR 프로토콜을 통해 보더 라우터로 전달되고, 라우터가 Invalid BGP 광고를 즉시 차단하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **RIR Trust Anchor** | KISA/APNIC 등 최상위 주소 관리 기관의 RPKI 루트 인증서 및 ROA 저장소 | Global Repository |
| **RPKI Validator** | ROA 파일 다운로드, 암호 서명 체인 검증, VRP(Validated ROA Payload) 목록 생성 | Routinator / OctoRPKI |
| **RTR 프로토콜** | 라우터와 검증기 간 암호화 세션을 통해 VRP 목록을 고속 증분 동기화 | RFC 8210 |
| **ROV 필터 엔진** | 수신된 BGP 경로의 Origin AS와 Prefix를 VRP와 대조하여 유효성 상태 태깅 | Route Validation |
| **BGPsec (RFC 8205)** | 원점뿐만 아니라 BGP AS-Path 전체 경로의 위변조를 방지하는 차세대 프로토콜 | AS-Path Signing |

#### 한줄 요약
- RIR Trust Anchor, RPKI Validator, RTR 프로토콜, 라우터 ROV 필터, BGPsec이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Drop Invalid 정책**: 라우터 BGP 설정에서 ROV 검증 결과가 `Invalid`로 판정된 모든 경로는 BGP RIB(라우팅 테이블)에 적재하지 않고 즉시 폐기(Reject)하는 모범 운영 표준(BCP).

</details>

```text
1. IP 대역 소유 기업이 KISA/APNIC RPKI 포털에서 '203.0.113.0/24 ➔ AS 64500, MaxLength /24' ROA 등록
            │
            ▼
2. 공격자(AS 666)가 인터넷 상에 동일 대역 '203.0.113.0/24 ➔ AS 666' 허위 BGP Update 공시 (하이재킹 시도)
            │
            ▼
3. 글로벌 ISP 라우터가 BGP 수신 ➔ 로컬 RPKI Validator로부터 수신한 VRP 테이블과 대조
            │
            ├─ [Origin AS 불일치 감지: AS 666 != AS 64500] ➔ 검증 상태 'Invalid' 태깅
            ▼
4. ISP 라우터의 'Drop Invalid' 정책에 의해 공격자의 허위 경로는 라우팅 테이블 적재 거부 및 즉시 폐기
            │
            ▼
5. 정상 경로(AS 64500)만 BGP Best Path로 채택 ➔ 트래픽 탈취 및 통신 두절 원천 차단 완수
```

**동작 원리**

1. **사전 인증서 발행**: 주소 보유자가 자신의 공인 IP 블록에 대해 정당한 원점 AS를 서명 등록
2. **검증 데이터 푸시**: 라우터가 메모리에 VRP(Prefix-AS-MaxLength) 룩업 테이블 유지
3. **실시간 광고 대조**: 외부 피어로부터 BGP 공시가 들어오면 3개 필드(Prefix, Length, AS) 비교
4. **Invalid 즉시 차단**: 공격자가 더 긴 서브넷(/25)을 광고하거나 가짜 AS를 내세워도 Invalid로 폐기
5. **정상 경로 수렴**: 전 세계 인터넷 트래픽이 정상 원점 AS로 안전하게 포워딩

#### 한줄 요약
- ROA 등록, 허위 BGP 광고 인입, RPKI 대조, Invalid 판정 및 즉시 폐기, 정상 경로 유지 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **BGP 하이재킹 공격 유형 비교**: 단순 원점 사칭, 서브넷 쪼개기 최장 일치 탈취, 정상 경로 누출의 메커니즘 비교.

</details>

| 공격 유형 | 단순 원점 하이재킹 (Origin Hijack) | 서브넷 탈취 (Sub-Prefix Hijack) | 경로 누출 (Route Leak) |
|:---|:---|:---|:---|
| **공격 메커니즘** | 타인의 `/24` 대역을 자신의 AS 번호로 공시 | 타인의 `/22` 대역을 `/24`로 쪼개어 공시 | 피어로부터 받은 경로를 상류 Provider로 재광고 |
| **탈취 성공 요인** | AS-Path 길이가 더 짧은 지역 트래픽 탈취 | **최장 접두어 일치(LPM)로 전 세계 트래픽 100% 탈취** | 고대역폭 피어 경로로 글로벌 트래픽 유입 |
| **RPKI ROV 방어력** | **100% 차단 (Origin AS 불일치로 Invalid)** | **100% 차단 (MaxLength 초과로 Invalid)** | **ROV 단독 방어 불가 (RFC 9234 OTC 필요)**|
| **실제 발생 사례** | 2008년 파키스탄 텔레콤 유튜브 차단 | 2018년 MyEtherWallet DNS 가로채기 | 2017년 구글 경로 누출로 인한 일본 인터넷 마비 |

#### 한줄 요약
- Origin/Sub-Prefix 탈취는 RPKI/ROV로 100% 방어하며, Route Leak은 RFC 9234 OTC 정책으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BGPsec(RFC 8205) 확장 요구**: ROV는 '원점(Origin)'만 검증하므로, 공격자가 AS-Path 중간에 가짜 AS를 끼워 넣는 경로 조작(Path Manipulation)을 방어하기 위해 모든 AS가 홉별 전자서명을 부착하는 확장 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| RPKI ROV 미지원 ISP를 경유한 허위 BGP 광고의 글로벌 확산 및 트래픽 탈취 | **전 글로벌 Tier-1/Tier-2 ISP의 'Drop Invalid' 정책 의무화 및 MANRS** 가입 | 악성 BGP 공시의 전 세계 전파 차단 및 신뢰 라우팅 생태계 구축 |
| 정상적인 원점 AS임에도 피어링 관계 위반으로 발생하는 **BGP 경로 누출(Route Leak)** | **RFC 9234 BGP 역할 협상 및 OTC(Only to Customer) 속성 검증 필터** 적용 | 비인가 경로 재광고 차단 및 대규모 트래픽 블랙홀 사고 예방 |
| RPKI Validator와 라우터 간 RTR 세션 단절 시 BGP 검증 중단 및 서비스 장애 | **RPKI Validator 이중화(Active-Standby) 및 캐시 만료 전 만료 방지(Fail-Safe)** | Validator 장애 시에도 기존 VRP 테이블 유지로 무중단 라우팅 보장 |

#### 한줄 요약
- MANRS/Drop Invalid로 글로벌 전파를 막고, RFC 9234 OTC로 경로 누출을 방지하며, Validator 이중화로 가용성을 확보한다.

## Ⅶ. 결론

- 글로벌 인터넷 인프라를 겨냥한 국가 단위 APT 공격 및 금융 트래픽 탈취를 방어하기 위해 **RPKI 기반의 BGP 하이재킹 방어 체계**는 모든 자율 시스템(AS)의 필수 보안 표준으로 정착되었으며, 실무 구축 시 **정확한 ROA 발행 및 MaxLength 최소화**, **에지 라우터의 Drop Invalid 정책 적용**, **RFC 9234 기반 경로 누출 방지 및 장기적 BGPsec 전환**을 통합 추진하여 무결점 인터넷 라우팅 인프라를 완성

#### 한줄 요약
- RPKI/ROA 전자서명과 에지 라우터 ROV 검증 및 OTC 필터를 통해 고신뢰 BGP 라우팅 보안을 실현한다.
