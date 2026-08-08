---
sidebar:
  order: 122
  label: "122. 인텔리전스 기반 CTI 자동화 (CTI Automation)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인텔리전스 기반 CTI 자동화 (CTI Automation)"
date: "2026-08-06T23:27:50+09:00"
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

- 정의/개념: **CTI**의 수집•정규화•평가•배포를 연결하는 **CTI 자동화**이다.
- 배경/필요성: 검증 없는 피드 자동 배포는 중복•만료 지표의 오차단을 일으킨다.

#### 한줄 요약

- 외부 공격 정보를 우리 자산과 대조해 믿을 만하고 아직 유효한 정보만 탐지•차단에 전달하는 것이 핵심이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **IoC(Indicator of Compromise)**: 침해 흔적을 식별하는 관측값이다.
- **TTP(Tactics, Techniques, and Procedures)**: 공격자가 목표 달성에 사용하는 행동 방식이다.
- **TLP(Traffic Light Protocol)**: CTI의 수신자와 재공유 범위를 표시하는 규칙이다.
- **STIX(Structured Threat Information eXpression)**: 위협 객체와 관계를 구조화하는 표현 표준이다.
- **TAXII(Trusted Automated eXchange of Intelligence Information)**: CTI를 조직•도구 사이에서 교환하는 프로토콜이다.

</details>

- **STIX** 객체•관계로 위협정보를 구조화한다.
- **TAXII** 교환과 **TLP** 표시로 공유 범위를 제한한다.
- **IoC**•**TTP**의 출처•신뢰도•시효•자산 관련성을 통제한다.

#### 한줄 요약

- 형식만 맞추지 않고 출처•유효기간•내부 자산 관련성을 함께 검증하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **TIP(Threat Intelligence Platform)**: 여러 CTI 피드를 정규화•평가•배포하는 플랫폼이다.
- **OSINT(Open-Source Intelligence)**: 공개 출처에서 수집한 위협 정보이다.
- **API(Application Programming Interface)**: TIP과 보안 도구가 CTI를 교환하는 연결 규격이다.

</details>

```text
CTI 자동화
├─ CTI 수집•출처
├─ STIX 2.1 정규화
├─ 신뢰도•시효•자산 보강
├─ TAXII 2.1•TLP 2.0 배포
└─ 적중•오탐 품질 환류
```

| 구성요소 | 책임 |
|:---|:---|
| CTI 수집•출처 | **OSINT**•상용•공유 피드 수집 |
| STIX 2.1 정규화 | 객체•관계•시간 형식 통일 |
| 신뢰도•시효•자산 보강 | 출처 점수•만료•영향 결합 |
| TAXII 2.1•TLP 2.0 배포 | **API** 교환•공유 범위 통제 |
| 적중•오탐 품질 환류 | 탐지 결과로 품질 점수 갱신 |

- **TIP**은 수집한 피드의 정규화•평가•배포를 통합한다.

#### 한줄 요약

- IP 하나도 출처와 관측 시점, 공격 관계, 내부 사용 여부를 확인한 뒤 배포하는 것이 핵심이다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **품질 점수**: 출처 신뢰도•시효•자산 관련성•적중 결과를 결합한 배포 판단값이다.
- **STIX CTI 객체 구성**: 위협정보를 객체•관계•출처•시간 구조로 정규화하는 단계이다.
- **CTI 보강•품질 점수 산정**: 출처•시효•자산 관련성을 평가해 배포 판단값을 만드는 단계이다.
- **배포 승인•공유 범위 결정**: 품질 기준과 TLP에 따라 자동 배포 및 수신자를 정하는 단계이다.
- **TAXII CTI 묶음 생성**: 승인된 지표와 관계를 표준 교환 형식으로 구성하는 단계이다.
- **적중•오탐•만료 평가**: 배포한 지표의 탐지 성과와 유효성을 다시 평가하는 단계이다.

</details>

```text
CTI 피드
   │
   ▼
1. STIX CTI 객체 구성
   │
   ▼
2. CTI 보강•품질 점수 산정
   │
   ▼
3. 배포 승인•공유 범위 결정
   ├─ 기준 충족 ─────► 4. TAXII CTI 묶음 생성
   │                         │
   │                         ▼
   │                  보안 도구 배포
   │                         │
   │                         ▼
   │                  5. 적중•오탐•만료 평가
   │                         │
   └─ 기준 미달 ─────► 보류•폐기
                             │
                             └── 품질 점수 환류
```

### 동작 원리

1. **STIX CTI 객체 구성**: 객체•관계•출처•시간 형식으로 정규화한다.
2. **CTI 보강•품질 점수 산정**: 출처•시효•자산 관련성을 평가한다.
3. **배포 승인•공유 범위 결정**: 자동 배포 여부와 TLP 수신자 범위를 결정한다.
4. **TAXII CTI 묶음 생성**: 승인된 지표•관계를 API 배포 형식으로 구성한다.
5. **적중•오탐•만료 평가**: 탐지 성과와 지표 유효성을 품질에 반영한다.

#### 한줄 요약

- 방어 목적을 먼저 정하고 검증된 지표만 제한적으로 배포한 뒤 결과로 신뢰도를 다시 조정하는 것이 핵심이다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **STIX 역할**: 위협의 객체•관계•시간•출처를 표현하는 역할이다.
- **TAXII 역할**: 조직•도구 사이에서 CTI를 전송하는 역할이다.
- **TIP 역할**: 다중 피드의 수집•평가•배포를 통합하는 역할이다.

</details>

| 자동화 요소 | 역할 | 연계 결과 |
|:---|:---|:---|
| **STIX 역할** | 위협의 객체•관계•시간•출처 표현 | 도구가 해석할 공통 CTI 데이터 |
| **TAXII 역할** | 조직•도구 사이의 HTTPS API 교환 | 인증•권한이 적용된 CTI 전송 |
| **TIP 역할** | 다중 피드의 수집•평가•배포 통합 | 신뢰도•시효•자산 기반 배포 판단 |

> 요약: STIX는 표현, TAXII는 교환, TIP은 운영을 담당하는 것이 핵심이다.

#### 한줄 요약

- 같은 형식과 전송 규칙을 써도 내용이 오래되거나 틀리면 TIP의 품질 통제가 필요하다는 점이 핵심이다.

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
| 객체 의미•관계가 다르면 도구별 탐지 해석 불일치 | **OASIS STIX 2.1** 적용 | CTI 구조화•상호운용 확보 |
| 교환 API가 다르면 자동 수집•배포 연계 실패 | **OASIS TAXII 2.1**과 **HTTPS** 적용 | CTI API 배포 표준화 |
| 공유 범위가 없으면 민감 CTI의 재공유•공개 | **FIRST TLP 2.0** 표시 | 수신자별 오용 방지 |

- **OASIS** 표준으로 표현•교환을 통일하고 **FIRST** 규칙으로 공유 범위를 표시한다.

#### 한줄 요약

- 수신 CTI를 STIX 객체로 검증하고 TAXII로 배포하되 TLP 표시에 따라 수신자와 재공유 범위를 제한한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **시효 관리**: 오래되거나 관련 없는 위협정보가 차단 정책으로 확산되지 않게 만료를 통제하는 활동이다.

</details>

- **시효 관리**를 적용해 출처•시효•자산 관련성이 기준을 충족하면 자동 배포하고 불충족하면 보류•폐기한다.

#### 한줄 요약

- 자동화 속도보다 오래되거나 관련 없는 위협 정보가 차단 정책으로 확산되지 않게 하는 것이 중요하다는 점이 핵심이다.
