---
sidebar:
  order: 122
  label: "122. 인텔리전스 기반 CTI 자동화 (CTI Automation)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인텔리전스 기반 CTI 자동화 (CTI Automation)"
date: "2026-08-05T01:48:44+09:00"
tags:
  - "notes-security"
weight: 122
extra:
  question_no: "122"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 기출이며 CTI 수집•분석•대응 자동화가 핵심임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **CTI(Cyber Threat Intelligence)**: 위협 행위자•기법•지표를 분석한 사이버 위협 인텔리전스이다.
- **CTI 자동화**: CTI의 수집•정규화•평가•배포를 연결하는 운영 방식이다.

</details>

- 정의/개념: CTI의 수집•정규화•평가•배포를 자동화하는 **위협정보 운영 체계**
- 배경/필요성: 검증 없는 피드 자동 배포로 **중복•만료 지표의 오차단 발생**

#### 한줄 요약

- 외부 공격 정보를 우리 자산과 대조해 믿을 만하고 아직 유효한 정보만 탐지•차단에 전달함

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **IoC(Indicator of Compromise)**: 침해 흔적을 식별하는 관측값이다.
- **TTP(Tactics, Techniques, and Procedures)**: 공격자가 목표 달성에 사용하는 행동 방식이다.
- **TLP(Traffic Light Protocol)**: CTI의 수신자와 재공유 범위를 표시하는 규칙이다.
- **STIX(Structured Threat Information eXpression)**: 위협 객체와 관계를 구조화하는 표현 표준이다.
- **TAXII(Trusted Automated eXchange of Intelligence Information)**: CTI를 조직•도구 사이에서 교환하는 프로토콜이다.

</details>

- STIX 객체•관계 기반 **위협정보 구조화**
- TAXII 교환•TLP 표시 기반 **제한적 공유**
- 출처•신뢰도•시효•자산 기반 **품질 통제**

#### 한줄 요약

- 형식만 맞추지 않고 출처•유효기간•내부 자산 관련성을 함께 검증함

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **TIP(Threat Intelligence Platform)**: 여러 CTI 피드를 정규화•평가•배포하는 플랫폼이다.
- **OSINT(Open-Source Intelligence)**: 공개 출처에서 수집한 위협 정보이다.
- **API(Application Programming Interface)**: TIP과 보안 도구가 CTI를 교환하는 연결 규격이다.

</details>

| 구성요소 | 책임 |
|:---|:---|
| CTI 수집•출처 | **OSINT•상용•공유 피드** 수집 |
| STIX 2.1 정규화 | **객체•관계•시간 형식** 통일 |
| 신뢰도•시효•자산 보강 | **출처 점수•만료•영향** 결합 |
| TAXII 2.1•TLP 2.0 배포 | **API 교환•공유 범위** 통제 |
| 적중•오탐 품질 환류 | 탐지 결과로 **품질 점수** 갱신 |

#### 한줄 요약

- IP 하나도 출처와 관측 시점, 공격 관계, 내부 사용 여부를 확인한 뒤 배포함

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **품질 점수**: 출처 신뢰도•시효•자산 관련성•적중 결과를 결합한 배포 판단값이다.

</details>

```mermaid
sequenceDiagram
  participant D as 방어 조직
  participant C as CTI 수집기
  participant T as TIP
  participant S as 보안 도구
  participant A as 분석가
  D->>C: 방어 요구•신뢰 출처
  C->>C: 1. STIX CTI 객체 구성
  C->>T: CTI 객체 전달
  T->>T: 2. CTI 보강•품질 점수 산정
  T->>A: 보강 CTI 전달
  A->>A: 3. 배포 승인•공유 범위 결정
  A->>T: 승인 결과 전달
  T->>T: 4. TAXII CTI 묶음 생성
  T->>S: CTI 묶음 전달
  S->>S: 5. 적중•오탐•만료 평가
  S->>T: 평가 결과 전달
```

**동작 원리**

1. **STIX CTI 객체 구성**: 객체•관계•출처•시간 형식으로 정규화
2. **CTI 보강•품질 점수 산정**: 출처•시효•자산 관련성 평가
3. **배포 승인•공유 범위 결정**: 자동 배포 여부와 TLP 수신자 범위 결정
4. **TAXII CTI 묶음 생성**: 승인된 지표•관계를 API 배포 형식으로 구성
5. **적중•오탐•만료 평가**: 탐지 성과와 지표 유효성을 품질에 반영

#### 한줄 요약

- 방어 목적을 먼저 정하고 검증된 지표만 제한적으로 배포한 뒤 결과로 신뢰도를 다시 조정함

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **STIX 역할**: 위협의 객체•관계•시간•출처를 표현하는 역할이다.
- **TAXII 역할**: 조직•도구 사이에서 CTI를 전송하는 역할이다.
- **TIP 역할**: 다중 피드의 수집•평가•배포를 통합하는 역할이다.

</details>

| 자동화 요소 | 역할 | 연계 결과 |
|:---|:---|:---|
| **STIX 2.1** | 위협의 **객체•관계•시간•출처 표현** | 도구가 해석할 공통 CTI 데이터 |
| **TAXII 2.1** | 조직•도구 사이의 **HTTPS API 교환** | 인증•권한이 적용된 CTI 전송 |
| **TIP** | 다중 피드의 **수집•평가•배포 통합** | 신뢰도•시효•자산 기반 배포 판단 |

> 요약: STIX는 표현, TAXII는 교환, TIP은 운영을 담당함

#### 한줄 요약

- 같은 형식과 전송 규칙을 써도 내용이 오래되거나 틀리면 TIP의 품질 통제가 필요함

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **OASIS(Organization for the Advancement of Structured Information Standards)**: 구조화 정보표준 촉진기구이다.
- **HTTPS(Hypertext Transfer Protocol Secure)**: 암호화된 웹 통신 프로토콜이다.
- **OASIS STIX 2.1**: CTI 구조화 표현의 표준 규격이다.
- **OASIS TAXII 2.1**: HTTPS 기반 CTI 교환의 표준 규격이다.
- **FIRST(Forum of Incident Response and Security Teams)**: 사고대응•보안팀 국제 포럼이다.
- **FIRST TLP 2.0**: CTI 정보의 공유 범위를 표시하는 규칙이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 객체 의미•관계가 다르면 도구별 탐지 해석 불일치 | **OASIS STIX 2.1** 적용 | CTI의 **구조화•상호운용** 확보 |
| 교환 API가 다르면 자동 수집•배포 연계 실패 | **OASIS TAXII 2.1** 적용 | CTI **API 배포 표준화** |
| 공유 범위가 없으면 민감 CTI의 재공유•공개 | **FIRST TLP 2.0** 표시 | 수신자별 **재공유•공개 오용** 방지 |

#### 한줄 요약

- 수신 CTI를 STIX 객체로 검증하고 TAXII로 배포하되 TLP 표시에 따라 수신자와 재공유 범위를 제한한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **시효 관리**: 오래되거나 관련 없는 위협정보가 차단 정책으로 확산되지 않게 만료를 통제하는 활동이다.

</details>

- 출처•시효•자산 관련성이 기준을 충족하면 **자동 배포**, 불충족하면 **보류•폐기**

#### 한줄 요약

- 자동화 속도보다 오래되거나 관련 없는 위협 정보가 차단 정책으로 확산되지 않게 하는 것이 중요함
