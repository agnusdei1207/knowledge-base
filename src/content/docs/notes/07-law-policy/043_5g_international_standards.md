---
sidebar:
  order: 43
  label: "043. 5G 국제 표준 — 3GPP•IMT-2020 (5G International Standards)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "5G 국제 표준 — 3GPP•IMT-2020 (5G International Standards)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-law-policy"
weight: 43
extra:
  question_no: "043"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 50
  priority_note: "반복 기출, 3GPP•IMT 표준화 구조"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **5세대 이동통신(Fifth Generation Mobile Communications, 5G)**: 초고속•초저지연•초연결 서비스를 지원하도록 정의한 이동통신 세대이다.
- **국제전기통신연합 전파통신부문(International Telecommunication Union Radiocommunication Sector, ITU-R)**: 국제이동통신 성능 요구와 무선 인터페이스 승인 및 주파수 이용을 담당하는 국제기구 부문이다.
- **3세대 파트너십 프로젝트(3rd Generation Partnership Project, 3GPP)**: 5G 무선 접속망•코어망•서비스의 상세 구현 규격을 개발하는 국제 표준협력체이다.

</details>

- 정의/개념: ITU-R 국제 요구와 3GPP 상세 규격을 연결하는 **5G 표준 체계**이다.
- 배경/필요성: 독자 규격만으로는 단말•망의 **상호운용성 확보** 및 국제 로밍 보장하기 어렵다.

#### 한줄 요약
- **ITU-R 성능 요구**를 3GPP 상세 규격으로 구현이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **국제이동통신-2020(International Mobile Telecommunications-2020, IMT-2020)**: 국제전기통신연합 전파통신부문(International Telecommunication Union Radiocommunication Sector, ITU-R)이 5G 후보 기술의 성능 요구와 평가 방법 및 승인 무선 인터페이스를 정의한 국제 체계이다.
- **3세대 파트너십 프로젝트 릴리즈(3rd Generation Partnership Project Release, 3GPP Release)**: 무선•코어•서비스 규격을 기능 묶음과 일정에 따라 동결하여 배포하는 버전 단위이다.
- **기술 규격(Technical Specification, TS)**: 3GPP 구현의 규범 요구사항을 담는 문서이다.
- **기술 보고서(Technical Report, TR)**: 후보 기술•요구•영향의 조사 결과를 담는 문서이다.
- **새로운 무선(New Radio, NR)**: 5G 단말과 기지국 사이의 무선 전송 규격이다.

</details>

- **IMT-2020** 요구와 무선 인터페이스 승인 기준이다.
- **3GPP TS•TR** 기반 NR•코어망 구현 규격이 핵심이다.
- 릴리즈 동결•채택•호환 검증을 거치는 **단계적 상용화**가 핵심이다.

#### 한줄 요약
- 3GPP 규격은 **Release 단위**로 단계적 동결이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **무선 접속망(Radio Access Network, RAN)**: 단말을 기지국을 거쳐 코어망에 연결하는 무선 네트워크 영역이다.
- **서비스 및 시스템(Service and System Aspects, SA)**: 3GPP에서 서비스 요구와 시스템 아키텍처를 담당하는 규격 그룹이다.
- **핵심망 및 단말(Core Network and Terminals, CT)**: 3GPP에서 코어망과 단말 연동 프로토콜을 담당하는 규격 그룹이다.

</details>

```text
                       [ITU-R•IMT-2020]
                         /           \
                  [3GPP RAN]     [3GPP SA•CT]
                         \           /
                    [지역 표준•산업 생태계]
```

선의 의미: ITU-R•IMT-2020의 국제 성능 요구를 3GPP RAN과 3GPP SA•CT가 각각 무선 및 시스템•코어 규격으로 구체화하고, 두 규격군은 지역 표준•산업 생태계에서 함께 적용된다.

| 구성요소 | 책임 |
|:---|:---|
| ITU-R•IMT-2020 | IMT 성능 요구와 승인 권고 관리 |
| 3GPP RAN | 무선 접속망의 상세 규격 개발 |
| 3GPP SA•CT | 코어 아키텍처•연동 프로토콜 개발 |
| 지역 표준•산업 생태계 | 지역 표준 전환과 장비 상용화 |

#### 한줄 요약
- 3GPP의 **RAN•SA•CT** 규격을 지역 표준으로 전환한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **국제이동통신(International Mobile Telecommunications, IMT)**: 국제전기통신연합이 세대별 이동통신 성능 목표와 평가 절차를 정하는 국제 체계이다.

</details>

```text
ITU-R
   │ 1. IMT 성능 요구•평가 절차 제공
   ▼
3GPP
   │ 2. 동결 규격•후보 무선기술 제출
   ▼
ITU-R
   │ 3. 평가•승인 무선 인터페이스 권고
   ▼
지역 표준기관
   │ 4. 지역 표준•적용 릴리즈 전달
   ▼
장비 생태계
   │ 5. 단말•망 장비 호환 결과 보고
   ▼
지역 표준기관
```

1. **IMT 성능 요구•평가 절차 제공**: 세대별 성능 목표와 후보 평가 기준을 설정한다.
2. **동결 규격•후보 무선기술 제출**: 무선•코어 상세 규격을 확정해 국제 평가를 요청한다.
3. **평가•승인 무선 인터페이스 권고**: 요구 충족성과 타당성을 검증해 국제표준을 승인한다.
4. **지역 표준•적용 릴리즈 전달**: 승인 규격을 지역 표준과 사업자 기준으로 전환한다.
5. **단말•망 장비 호환 결과 보고**: 단말•기지국•코어망의 연동과 로밍을 확인한다.

#### 한줄 요약
- **IMT 요구**에 맞는 3GPP 후보를 평가해 국제 승인이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **비독립모드(Non-Standalone, NSA)**: 기존 장기진화(Long-Term Evolution, LTE) 코어망과 제어 기능을 활용하면서 5세대 새로운 무선(5G New Radio, 5G NR)을 함께 사용하는 구성이다.
- **독립모드(Standalone, SA)**: 5G 전용 코어망과 NR로 슬라이싱•저지연 등 5G 기능을 온전히 제공하는 구성이다.
</details>

| 구분 | ITU-R IMT-2020 | 3GPP 5G 규격 |
|:---|:---|:---|
| 적용 기준 | 기술 인증•**주파수 조정** | 구현•**지역 표준 전환** |
| 핵심 특징 | 국제 성능 요구•**무선 승인** | 무선•코어 **구현 규격** 개발 |
| 한계 | 구현 세부 규격의 **부족** | 국제 요구와의 **불일치** |

#### 한줄 요약
- **ITU-R**은 국제 요구, **3GPP**는 구현 규격 담당이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **릴리즈 호환성**: 단말•기지국•코어가 서로 다른 3GPP Release 선택 기능을 지원하여 접속•서비스가 제한되는 문제이다.
- **주파수 적합성**: 국가별 할당 대역•출력•채널 조건에 맞는 3GPP 밴드와 장비를 선택해야 하는 조건이다.
- **상호운용 시험**: 서로 다른 제조사의 단말•무선망•코어망이 같은 프로파일로 접속•이동•서비스를 수행하는지 확인하는 시험이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ITU 요구와 **구현 규격 혼동** | 성능은 ITU-R, 기능은 **3GPP 규격**으로 추적 | 역할별 **검증 기준 명확화** |
| 장비별 **지원 릴리즈 불일치** | 단말•기지국•코어망의 **지원 버전** 대조 | **연동 장애** 예방 |
| NSA•SA의 **기능 의존성** | 망 조합별 로밍•슬라이싱•**보안 시험** | 단계적 **상용망 전환** 안정화 |
| Release 19 동결•20 **개발 상태 차이** | 제품은 동결 규격, 선행 개발은 **Release 20** 추적 | 버전 선택의 **시점 오류** 방지 |

#### 한줄 요약
- 단말•기지국•코어망의 **지원 Release** 일치가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **국제 요구-상세 규격 관계**: ITU-R은 세대 성능과 국제 무선 체계를 정하고 3GPP는 이를 만족하는 구현 가능한 시스템 규격을 개발하는 관계이다.
- **국제 로밍**: 다른 국가•사업자 망에서도 가입자 인증과 이동통신 서비스를 이어서 사용할 수 있는 기능이다.

</details>

- 국제 적합성은 **ITU-R**, 제품•망 연동은 동일 **3GPP Release** 기준을 검증한다.

#### 한줄 요약
- **IMT 요구•Release 동결 시점**에 맞춰 검증•기고가 핵심이다.
