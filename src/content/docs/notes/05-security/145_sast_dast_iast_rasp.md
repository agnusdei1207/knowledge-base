---
sidebar:
  order: 145
  label: "145. SAST·DAST·IAST·RASP"
  badge:
    text: "기출 · 70%"
    variant: note
title: SAST·DAST·IAST·RASP
date: "2026-07-31T11:25:46+09:00"
tags:
  - notes-security
weight: 145
extra:
  question_no: "145"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "반복 출제된 응용 보안 검증 기법"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **응용 보안 검증**: 코드·실행·운영의 서로 다른 관점에서 취약점과 공격 가능성을 확인하는 활동이다.

</details>

- 정의/개념: 코드·실행·운영의 **단계별 응용 보안 검증**
- 배경/필요성: 단일 시험만으로는 코드·실행·운영 관점의 **보안 사각을 충분히 줄이기 어려움**

#### 한줄 요약

- 설계도 검사·외부 동작 검사·내부 센서·현장 방어를 함께 써 사각을 줄임

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **정적 응용보안시험(Static Application Security Testing, SAST)·동적 응용보안시험(Dynamic Application Security Testing, DAST)·상호작용 응용보안시험(Interactive Application Security Testing, IAST)·런타임 응용 자기보호(Runtime Application Self-Protection, RASP)**: 정적 코드·외부 실행·내부 계측·운영 맥락에서 각각 응용 보안을 검증·보호하는 기법이다.

</details>

- SAST·DAST로 **내부 코드와 외부 공격면 상호 보완**
- IAST의 **요청·코드 실행 경로 연결**
- RASP의 **운영 맥락 기반 탐지·완화**

#### 한줄 요약

- 같은 결함도 보는 위치와 시점이 달라 여러 결과를 실제 경로와 영향 기준으로 합쳐야 함

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **소프트웨어 구성분석(Software Composition Analysis, SCA)**: 제3자 구성요소의 버전·라이선스·취약점을 분석하는 시험이다.
- **응용보안 결과 연계**: 정적 응용보안시험(SAST), 동적 응용보안시험(DAST), 상호작용 응용보안시험(IAST), 런타임 응용 자기보호(RASP)의 결과를 실제 경로·영향과 연결한다.
- **도달 가능성**: 취약 코드가 실제 입력·실행 경로에서 호출되는지를 나타내는 속성이다.

</details>

```mermaid
block-beta
  columns 1
  S["SAST·SCA 코드 검사"]
  I["IAST 내부 실행 계측"]
  D["DAST 외부 동적 검증"]
  R["RASP 운영 보호"]
  M["도달 가능성·영향 위험관리"]
  S --- I --- D
  D --- R --- M
```

| 구성요소 | 책임 |
|:---|:---|
| **SAST·SCA 코드 검사** | 코드 흐름·구성요소 **후보 탐지** |
| **IAST 내부 실행 계측** | 요청·함수·**데이터 흐름 연결** |
| **DAST 외부 동적 검증** | 실제 요청·응답의 **악용 확인** |
| **RASP 운영 보호** | 실행 맥락의 **공격 탐지·완화** |
| **도달 가능성·영향 위험관리** | 노출·업무 영향·**오탐 판정** |

#### 한줄 요약

- 결과를 한곳에 모아 실제로 닿고 악용되며 중요한 결함부터 고침

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **보안 회귀검증**: 수정한 취약점과 공격 경로가 다시 나타나지 않는지 확인하는 활동이다.

</details>

```mermaid
sequenceDiagram
  participant T as 제품팀
  participant S as 정적 검사
  participant D as 동적·상호작용 검사
  participant R as 위험관리
  participant O as 운영 보호
  T->>S: 코드·구성요소 제출
  S->>S: 1. 정적 코드·구성요소 분석
  T->>D: 시험 대상·역할·인증정보 제공
  D->>D: 2. 동적·상호작용 경로 검증
  S->>R: 정적 검사 결과 전달
  D->>R: 동적 검사 결과 전달
  R->>R: 3. 도달 가능성·악용성·영향 분석
  R->>T: 수정 대상·우선순위 전달
  T->>T: 4. 코드·설정·의존성 근본 수정
  T->>O: 수정 빌드 배포
  O->>O: 5. 회귀검증·운영 공격 관측
  O-->>T: 잔여위험 결과 환류
```

**동작 원리**

- **1. 정적 코드·구성요소 분석**: 코드 흐름·의존성 후보 탐지
- **2. 동적·상호작용 경로 검증**: 요청·실행 경로·악용성 확인
- **3. 도달 가능성·악용성·영향 분석**: 중복·오탐·우선순위 판정
- **4. 코드·설정·의존성 근본 수정**: 원인 제거·보완 통제 설정
- **5. 회귀검증·운영 공격 관측**: 수정 재현·잔여위험 환류

#### 한줄 요약

- 취약점 찾기에서 끝내지 않고 원인을 수정하고 같은 공격이 막혔는지 다시 확인함

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **검증 시점·위치**: 개발 코드, 시험 중 외부·내부, 운영 응용처럼 기법이 관찰하는 단계와 지점이다.
- **네 가지 응용보안 기법**: 정적 응용보안시험(Static Application Security Testing, SAST), 동적 응용보안시험(Dynamic Application Security Testing, DAST), 상호작용 응용보안시험(Interactive Application Security Testing, IAST), 런타임 응용 자기보호(Runtime Application Self-Protection, RASP)를 시점·가시성·목적에 따라 선택한다.

</details>

| 응용 보안 기법 | SAST | DAST | IAST | RASP |
|:---|:---|:---|:---|:---|
| **적용 기준** | 개발 초기 **코드** | 외부 **악용 확인** | **요청·코드 위치 연결** | 운영 **즉시 완화** |
| **핵심 특징** | 실행 전 **흐름 분석** | 외부 요청 **실행 검사** | 내부 **실행정보 결합** | 운영 맥락 **공격 차단** |
| **한계** | **오탐·환경 차이** | **인증·원인 추적 누락** | **호환·성능 영향** | **오차단·수정 지연** |

> 요약: 가시성·시점·목적에 맞춰 상호 보완함

#### 한줄 요약

- 각 기법은 보는 시점과 위치가 달라 하나의 도구로 모두 대체할 수 없음

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **오픈 웹 애플리케이션 보안 프로젝트 응용보안 검증표준(OWASP Application Security Verification Standard, OWASP ASVS)·웹 보안 시험 가이드(OWASP Web Security Testing Guide, OWASP WSTG)**: 웹 응용 보안 요구·검증 수준과 동적 시험 시나리오·방법을 제공한다.
- **미국 국립표준기술연구소 안전한 소프트웨어 개발 프레임워크(NIST Secure Software Development Framework, NIST SSDF)**: 개발 수명주기에 안전한 소프트웨어 관행을 통합하는 지침이다.
- **미국 국립표준기술연구소 특별간행물(NIST Special Publication, NIST SP) 800-218**: SSDF v1.1을 수록한 공식 문서이다.
- **정적·동적·상호작용 검증**: 정적 응용보안시험(SAST) 후보를 동적 응용보안시험(DAST)과 상호작용 응용보안시험(IAST)으로 실제 경로에 연결한다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **보안 요구·검증 수준** | **OWASP ASVS 5.0.0 적용** | 검사 범위·**완료 기준 명확화** |
| **웹 동적 시험 시나리오** | **OWASP WSTG v4.2 적용** | 역할·경로·**증거 표준화** |
| **개발 수명주기 통합** | **NIST SP 800-218 연계** | 수정·**재발 방지 환류** |

#### 한줄 요약

- SAST 후보를 DAST·IAST로 실제 노출 경로와 연결하고 수정 후 회귀시험과 운영 관측으로 재검증한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **상호 보완 검증**: 여러 시험 결과를 실제 경로·근본 수정·재시험으로 연결해 단일 기법의 사각을 줄이는 접근이다.
- **응용보안 기법 선택**: 정적 응용보안시험(Static Application Security Testing, SAST)은 초기 코드, 동적 응용보안시험(DAST)과 상호작용 응용보안시험(IAST)은 경로 검증, 런타임 응용 자기보호(RASP)는 운영 완화에 적용한다.

</details>

- 초기 코드는 **SAST**, 경로 검증은 **DAST·IAST**, 운영 완화는 **RASP** 적용

#### 한줄 요약

- 여러 검사를 많이 돌리는 것보다 결과를 실제 경로·수정·재검증으로 연결해야 함
