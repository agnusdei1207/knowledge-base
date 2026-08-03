---
sidebar:
  order: 90
  label: "090. SASE - SD-WAN•CASB•SWG•ZTNA (SASE)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "SASE - SD-WAN•CASB•SWG•ZTNA (SASE)"
date: "2026-08-03T15:05:00+09:00"
tags: ["notes-network"]
weight: 90
extra:
  question_no: "090"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "설계형: 135회 Zero Trust의 SASE 구성"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **보안 액세스 서비스 에지(Secure Access Service Edge, SASE)**: 소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN) 연결과 보안 서비스 에지(Security Service Edge, SSE) 보안을 사용자 인접 접속 거점(Point of Presence, PoP)에서 하나의 정책으로 제공하는 클라우드 네트워크 구조

</details>

- 정의/개념: SD-WAN 연결과 SSE 보안을 PoP에서 결합한 **클라우드 네트워크 구조**
- 배경/필요성: 본사 우회 구조의 **지연•회선 병목•정책 편차**

#### 한줄 요약

- 사용자가 어디에 있든 가까운 거점으로 연결해 빠른 경로와 같은 보안 규칙을 한 번에 적용한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **접속 거점(Point of Presence, PoP)**: 사용자와 가까운 위치에서 트래픽을 받아 연결•보안 기능을 수행하는 사업자 거점
- **통합 정책**: 신원•단말•응용 맥락을 바탕으로 경로 선택과 접근•자료 보안을 함께 결정하는 규칙이다.
- **SD-WAN•SSE**: 소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN)과 보안 서비스 에지(Security Service Edge, SSE)로 연결 경로와 클라우드 보안을 통합하는 구성

</details>

- **신원•단말•응용 맥락**: 경로•접근 정책 통합
- **근접 PoP**: 보안 정책을 적용해 본사 우회 지연 제거
- **SD-WAN•SSE 단일 운영**: 연결•보안 정책 통합

#### 한줄 요약

- 지사마다 장비를 따로 관리하지 않아도 되지만 가까운 거점의 용량과 장애 대비가 실제 사용자 품질을 좌우한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **SD-WAN•SSE**: 소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN)은 응용•회선 품질로 경로를 선택하고 보안 서비스 에지(Security Service Edge, SSE)는 웹•클라우드•사설 응용 접근 보안을 제공하는 구성
- **CASB•SWG•ZTNA**: 클라우드 접근 보안 중개(Cloud Access Security Broker, CASB), 보안 웹 게이트웨이(Secure Web Gateway, SWG), 제로 트러스트 네트워크 액세스(Zero Trust Network Access, ZTNA)는 각각 클라우드 사용 통제, 웹 검사, 신원•단말 기반 응용 접근을 수행하는 SSE 기능
- **접속 거점(Point of Presence, PoP)**: 연결•보안 기능을 사용자 인접 위치에서 실행하는 사업자 거점

</details>

```mermaid
block-beta
    columns 1
    EDGE["사용자•지사 엣지"]
    SDWAN["SD-WAN 연결부"]
    POP["PoP•SSE 보안부"]
    POLICY["통합 정책 제어기"]
    APP["인터넷•클라우드•사설 응용"]
    EDGE --- SDWAN --- POP --- APP
    POLICY --- SDWAN
    POLICY --- POP
```

| 구성요소 | 책임 |
|:---|:---|
| 사용자•지사 엣지 | 신원•단말•회선•응용 정보 수집 |
| SD-WAN 연결부 | 품질•응용 정책으로 경로 선택 |
| PoP•SSE 보안부 | SWG•CASB•ZTNA 정책 실행 |
| 통합 정책 제어기 | 연결•보안 규칙의 일관 배포 |
| 인터넷•클라우드•사설 응용 | 정책 통과 사용자의 목적 자원 |

#### 한줄 요약

- 엣지가 가까운 거점을 골라 트래픽을 보내면 그곳에서 웹과 클라우드, 사설 앱 정책을 검사한 뒤 목적지로 전달한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **품질 기반 접속 거점(Point of Presence, PoP) 선택**: 지연•손실•용량을 측정해 사용자 트래픽을 처리할 근접 거점을 선택하는 과정
- **세션 위험 재평가**: 접속 중 행위와 맥락 변화를 반영해 기존 허용 수준을 다시 판단하는 절차이다.
- **ZTNA•SWG•CASB**: 제로 트러스트 네트워크 액세스(Zero Trust Network Access, ZTNA), 보안 웹 게이트웨이(Secure Web Gateway, SWG), 클라우드 접근 보안 중개(Cloud Access Security Broker, CASB)로 응용•웹•클라우드 접근을 검사하는 기능

</details>

```mermaid
sequenceDiagram
    participant 사용자
    participant 엣지
    participant PoP
    participant 정책제어기
    participant 응용
    사용자->>엣지: 접속 요청
    엣지->>PoP: 1. 품질 기반 PoP 접속
    PoP->>정책제어기: 2. 통합 정책 조회
    정책제어기-->>PoP: 경로•접근•자료 규칙
    PoP->>응용: 3. 허용 응용 연결
    응용-->>PoP: 4. 세션 행위 전달
    PoP->>정책제어기: 5. 세션 위험 재평가 요청
    정책제어기-->>사용자: 접근 조정 결과
```

**동작 원리**

- **1. 품질 기반 PoP 접속**: 지연•손실•용량으로 거점 선택
- **2. 통합 정책 조회**: 경로•접근•자료 규칙 결합
- **3. 허용 응용 연결**: ZTNA•SWG•CASB 검사 후 전달
- **4. 세션 행위 전달**: 응용 이용 행위를 PoP에 지속 제공
- **5. 세션 위험 재평가 요청**: 맥락 변화에 따른 권한 재판단

#### 한줄 요약

- 사용자와 단말을 확인해 가장 좋은 거점으로 보내고 같은 곳에서 보안 검사를 마친 뒤 허용된 응용에만 연결한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **SASE•SSE**: 보안 액세스 서비스 에지(Secure Access Service Edge, SASE)는 연결과 보안을 함께 전환하고 보안 서비스 에지(Security Service Edge, SSE)는 기존 광역망(Wide Area Network, WAN)을 유지하면서 보안 기능만 클라우드화하는 방식
- **본사 중심 보안**: 지사•원격 트래픽을 보안 검사를 위해 본사 데이터센터까지 우회시키는 구조이다.
- **소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN)•접속 거점(Point of Presence, PoP)**: 응용별 경로를 선택하고 사용자 인접 위치에서 보안을 적용하는 구성

</details>

| 접속 보안 구조 | SASE | SSE | 본사 중심 보안 |
|:---|:---|:---|:---|
| 적용 기준 | 지사•원격의 **연결•보안 통합** | 기존 WAN 유지•**보안만 전환** | 소수 지점•**본사 중심 서비스** |
| 핵심 특징 | SD-WAN•SSE의 **단일 정책** | 클라우드 **보안 기능 통합** | 본사 장비의 **우회 검사** |
| 한계 | 사업자•**PoP 품질 의존** | 연결•보안 **정책 분리** | 우회 지연•**본사 회선 병목** |

> 요약: 연결 통합 범위•PoP 의존성으로 방식 선택

#### 한줄 요약

- 연결과 보안을 함께 바꾸면 SASE, 보안만 클라우드화하면 SSE, 본사 중심 업무가 작으면 기존 우회 방식을 고려한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **자동 경로 전환**: 현재 PoP 장애나 품질 저하를 감지해 다른 거점으로 접속 경로를 바꾸는 기능이다.
- **응용 단위 권한**: 내부 네트워크 전체가 아니라 검증된 사용자에게 허용한 개별 응용만 연결하는 권한이다.
- **접속 거점(Point of Presence, PoP)**: 사용자 트래픽의 연결•보안 기능을 처리하는 사업자 거점
- **제로 트러스트 네트워크 액세스(Zero Trust Network Access, ZTNA)**: 신원•단말 맥락에 따라 허용한 응용만 연결하는 접근 방식
- **보안 액세스 서비스 에지(Secure Access Service Edge, SASE)**: 소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN) 연결과 보안 서비스 에지(Security Service Edge, SSE) 보안을 근접 PoP에서 통합 제공하는 구조

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| PoP 장애의 **접속 품질 급락** | 다중 PoP와 **자동 경로 전환** | 지연과 **서비스 중단 감소** |
| 연결•보안의 **정책 불일치** | 단일 정책 모델•**배포 검증** | 우회 허용과 **운영 편차 축소** |
| 원격 사용자의 **과도한 망 접근** | **ZTNA 기반 응용 단위 권한 적용** | 횡적 이동과 **노출 범위 감소** |

#### 한줄 요약

- 원격 개발자가 SASE PoP에서 신원과 단말 보안 상태를 검증받은 뒤 사내망 전체가 아닌 소스 저장소에만 접속하게 한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **전환 범위**: 광역망(Wide Area Network, WAN) 연결과 보안을 동시에 보안 액세스 서비스 에지(Secure Access Service Edge, SASE)로 바꿀지, 기존 WAN을 유지하고 보안 서비스 에지(Security Service Edge, SSE)만 도입할지 정하는 범위

</details>

- 연결•보안 동시 전환은 **SASE**, WAN 유지•보안 전환은 **SSE** 선택

#### 한줄 요약

- SASE는 기능 목록보다 사용자가 실제로 거치는 거점의 품질과 그곳에서 연결•보안 정책이 함께 적용되는지를 검증해야 한다.
