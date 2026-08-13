---
sidebar:
  order: 28
  label: "028. 사이버 킬체인 (Cyber Kill Chain)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "사이버 킬체인 (Cyber Kill Chain)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 28
extra:
  question_no: "028"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출이며 ATT&CK 비교•대응설계에 재사용됨"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **사이버 킬체인(Cyber Kill Chain)**: 록히드 마틴(Lockheed Martin)이 제안한 모델로, 사이버 공격의 침해 과정을 7단계(정찰부터 목적달성까지)로 모델화하여 단계별 끊기(Kill) 지점을 식별하는 침해 대응 방어 프레임워크.
- **캠페인(Campaign)**: 하나의 공격 목표(Data Exfiltration, Ransomware 등) 달성을 위해 일정 기간 전개되는 다단계 공격 작전.

</details>

- 정의/개념: 침해 과정을 7단계로 나눠 차단 지점을 찾는 **사이버 킬체인**
- 배경/필요성: 단일 경계 방어는 **다단계 침해의 후속 행위**를 차단하지 못한다.

#### 한줄 요약

- 사이버 침해 과정을 7단계(정찰-무기화-전달-악용-설치-C2-목적달성)로 정의하여 공격 체인을 끊어내는 선형 방어 프레임워크

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **유효 계정(Valid Account)**: 정상적으로 등록된 계정이나 공격자에게 자격증명이 탈취되어 정상 권한으로 위장 투입되는 공격 통로.
- **다중 차단 기회(Multiple Intercept Opportunities)**: 7단계 공격 연쇄 중 단 한 단계에서만 성공적으로 차단해도 공격자의 최종 목적 달성을 원천 무력화할 수 있는 방어 기회.
- **선형 모델의 한계(Limitations of Linear Model)**: 실제 최신 APT 공격은 단계를 임의 생략, 자가 반복, 비선형 역행하는 특성이 있어 고정 7단계 모델 적용 시 사각지대 발생.

</details>

- 7단계 침해 프로세스 모델링을 통한 단계별 공격 행위 연결성 식별
- **다중 차단 기회(Multiple Intercept Opportunities)** 체계를 구축하여 앞선 방어선 실패 시 후속 단계 차단
- **선형 모델의 한계**를 극복하기 위해 **유효 계정(Valid Account)** 남용 및 비선형 TTP 탐지 기법 병행

#### 한줄 요약

- 다중 차단 기회(Multiple Intercept Opportunities) 확보, 단계별 연속 차단 및 선형 모델 한계(비선형 TTP) 보완

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **관측•검증 지점(Observation & Verification Points)**: 7단계 각 과정에서 공격 징후 증적(Log, Packet, Event)을 수집·분석하고 차단 성공 여부를 검증하는 모니터링 포인트.
- **대응 책임(Response Accountability)**: 탐지된 킬체인 단계에 대응하여 조치(Detect, Deny, Disrupt, Degrade, Deceive, Destroy)를 집행하는 거버넌스 담당 체계.

</details>

```text
사이버 킬체인 대응 구조
├─ 단계 분류기
├─ 공격 활동•증거
├─ 관측•검증 지점
├─ 예방•차단 통제
└─ 대응 책임
```

가지의 의미: 단계별 탐지 분류, 공격 증적 관측, 통제 배치 및 집행 책임 구별 아키텍처

| 구성요소 | 책임 |
|:---|:---|
| 공격 활동•증거 | 네트워크 페이로드, 이메일 헤더, 레지스트리에서 관측되는 공격 증적 산출 |
| 단계 분류기 | 탐지된 공격 이벤트를 킬체인 7단계 메커니즘으로 분류 바인딩 |
| 관측•검증 지점 | SIEM, EDR, NDR을 활용한 단계별 탐지 무결성 및 차단 효과 검증 |
| 예방•차단 통제 | 각 킬체인 연결고리를 차단하는 보안 통제(WAF, EDR, IPS, Email Gateway) 배치 |
| 대응 책임 | SOC 분석가 및 CSIRT 팀의 단계별 사고 조치, 격리 및 6D 대응 실행 |


#### 한줄 요약

- 탐지/분류 엔진, 관측·검증 지점(Observation Points), 단계별 방어 통제 및 대응 책임(Responsibility) 아키텍처

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **1. 정찰(Reconnaissance)**: OSINT, 포트 스캐닝, 소셜 엔지니어링을 통해 표적 인프라 정보 수집.
- **2. 무기화(Weaponization)**: 0-Day 익스플로잇과 악성 페이로드(PDF, HWP, Executable)를 합성 무기화.
- **3. 전달(Delivery)**: 스피어 피싱 이메일, 악성 웹사이트(Watering Hole), USB를 통해 표적에 전송.
- **4. 악용(Exploitation)**: 취약점(Application/OS Zero-day)을 악용하여 악성 코드 실행.
- **5. 설치(Installation)**: 대상 시스템에 백도어, 웹쉘, 모듈형 악성코드 영구 설치 및 지속성 확보.
- **6. 명령제어(Command and Control, C2)**: 외부 C2 서버와 암호화 채널을 수립하여 원격 조종 제어.
- **7. 목적 달성(Actions on Objectives)**: 데이터 탈취(Exfiltration), 파괴(Wiper), 랜섬웨어 암호화 집행.

</details>

```text
1. 정찰•무기화
        │
        ▼
2. 전달•악용
        │
        ▼
3. 설치•C2
        │
        ▼
4. 목적 달성

※ 실제 공격은 단계 생략•반복•역행 가능
```

### 동작 원리

1. **정찰•무기화**: 표적 취약점 탐색 후 무기화된 페이로드 생성
2. **전달•악용**: 이메일•웹으로 전달하고 취약점 악용 코드 실행
3. **설치•C2**: 백도어 설치로 지속성과 원격 명령 채널 확보
4. **목적 달성**: 최종 목표인 중요 데이터 암호화, 파괴 또는 외부 반출 완결


#### 한줄 요약

- 7단계(Recon, Weaponization, Delivery, Exploitation, Installation, C2, Actions) 진행 및 단계별 차단 흐름

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **MITRE ATT&CK**: 실제 공격자 TTP를 14개 전술 단계 및 세부 기술 매트릭스로 대규모 체계화한 지식 기반.
- **사고 대응 수명주기(Incident Response Lifecycle)**: NIST SP 800-61 기반의 사고 준비, 탐지, 격리, 제거, 복구 통제 프로세스.

</details>

| 보안 분석 모델 | **사이버 킬체인 (Cyber Kill Chain)** | **MITRE ATT&CK** | **사고 대응 수명주기 (NIST IR)** |
|:---|:---|:---|:---|
| 주요 목적 | 공격 단계별 조기 차단 지점(Kill Point) 설계 | 세부 공격 행동(TTP) 매핑 및 헌팅 | 사고 발생 시 수습, 격리, 복구 관리 |
| 모델 구조 | 7단계 선형(Linear) 순차 프로세스 | 14개 전술(Tactics) & 500+ 세부 기술(Techniques) 매트릭스 | 4단계 순환(Preparation, Detect, Contain, Post) |
| 장단점 | 단순하고 직관적이나 비선형 TTP 표현 한계 | 세밀하고 정교하나 공격 시순 및 캠페인 맥락 파악 복잡 | 조직 관점 절차 중심이나 기술적 공격 분석 미흡 |

> 요약: 공격 흐름 통제(킬체인) vs 세부 TTP 탐지(ATT&CK) vs 프로세스 수습(NIST IR)의 상호 보완 적용

#### 한줄 요약

- 공격 단계 분석용 사이버 킬체인, 세부 기술 매핑용 MITRE ATT&CK, 사고 수습용 NIST/ISO 대응 수명주기 비교

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **모의훈련(Cyber Simulation / Red Teaming)**: 킬체인 단계별 방어 통제(Email Gateway, EDR, C2 Filter)가 정상 작동하여 실제 공격을 끊어내는지 검증하는 모의 침투 활동.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 경계 방어선 돌파 | **킬체인 7단계별 다중 차단 통제(6D) 배치** | 앞선 방어 실패 시 후속 단계에서 연속 차단 |
| 비선형 공격 TTP 탐지 한계 | **MITRE ATT&CK 프레임워크 상호 매핑** | 킬체인의 선형적 사각지대 보완 |
| 단계별 통제 실효성 미비 | **레드팀 모의훈련(Red Teaming) 및 무력화 검증** | 단계별 센서 및 대응 책임 실전 검증 |

#### 한줄 요약

- 7단계 선형 방어 수립, ATT&CK TTP 매핑 연동, 관측/검증 지점 점검 및 레드팀 모의훈련(Red Teaming) 실전 검증

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **분석 모델 선택(Analysis Model Selection)**: 침해 흐름•세부 기법•운영 프로세스에 맞는 분석 모델 선택 지침.

</details>

- 초기 차단은 **사이버 킬체인**, 세부 행위 탐지는 **ATT&CK TTP**, 사고 격리/수습은 **NIST 사고 대응 수명주기** 선택 적용

#### 한줄 요약

- 킬체인 7단계 차단 통제, ATT&CK TTP 결합, 관측/검증 지점 확보 및 모의훈련(Red Teaming) 기반 심층 방어 체계 구축 필수
