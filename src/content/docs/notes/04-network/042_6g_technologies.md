---
sidebar:
  order: 42
  label: "042. 6G 핵심 기술 (6G Vision & Technologies)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "6G 핵심 기술 (6G Vision & Technologies)"
date: "2026-08-03T08:48:47+09:00"
tags:
  - "notes-network"
weight: 42
extra:
  question_no: "042"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "설명•설계형: 128•135회 6G 반복"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030)**: 국제전기통신연합(International Telecommunication Union, ITU)이 6세대 이동통신(Sixth Generation, 6G)을 위해 정의한 사용 시나리오와 핵심 역량의 국제 이동통신 체계
- **인공지능(Artificial Intelligence, AI)**: 통신망의 관측 정보를 바탕으로 경로•빔•자원 정책을 판단하는 지능 기술

</details>

- 정의/개념: 통신•센싱•AI를 통합하는 **IMT-2030 이동통신 체계**
- 배경/필요성: 5세대 이동통신(Fifth Generation, 5G)의 지상 셀•통신 중심 구조로 **입체 연결•환경 감지** 제약

#### 한줄 요약

- 6G는 더 빠른 통신만이 아니라 주변을 감지하고 망이 스스로 경로와 자원을 조절하려는 이동통신 체계다

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **비지상망(Non-Terrestrial Network, NTN)**: 위성•고고도 플랫폼을 이용해 지상 셀 밖까지 연결 범위를 확장하는 망
- **통신•센싱 통합(Integrated Sensing and Communication, ISAC)•인공지능 내재형(Artificial Intelligence-Native, AI-Native)**: 같은 무선 자원으로 통신과 감지를 수행하고 인공지능(Artificial Intelligence, AI)을 망 제어의 기본 기능으로 사용하는 구조
- **국제전기통신연합 전파통신부문(International Telecommunication Union Radiocommunication Sector, ITU-R)**: 국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030) 사용 시나리오와 무선 역량을 정의하는 국제 표준화 부문
- **테라헤르츠(Terahertz, THz)•재구성 지능형 표면(Reconfigurable Intelligent Surface, RIS)**: 6세대 이동통신(Sixth Generation, 6G)의 대역 확장과 전파 경로 제어를 위한 후보 기술

</details>

- 6G 역량을 체계화하는 **ITU-R M.2160의 6대 사용 시나리오**
- **NTN 기반 지상 셀 밖 입체 연결 확대**
- **ISAC•AI-Native 기반 통신•센싱•지능 제어 통합**

#### 한줄 요약

- 6G는 목표가 정해지는 단계이므로 THz•RIS 같은 후보 기술을 확정 규격으로 보면 안 된다

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **분산 컴퓨팅**: 단말•에지•중앙의 여러 연산 자원에 작업을 나눠 처리하는 구조
- **재구성 지능형 표면(Reconfigurable Intelligent Surface, RIS)**: 반사 소자의 전자기 응답을 조절해 전파 경로를 재구성하는 지능형 표면
- **인공지능 내재형(Artificial Intelligence-Native, AI-Native)**: 인공지능을 경로•빔•자원 제어의 기본 기능으로 사용하는 망 구조
- **비지상망(Non-Terrestrial Network, NTN)**: 위성•고고도 플랫폼을 지상망과 통합해 입체 연결을 제공하는 망
- **6세대 이동통신(Sixth Generation, 6G)**: 통신•센싱•지능•컴퓨팅을 통합하는 차세대 이동통신 체계

</details>

```mermaid
block
    columns 1
    block:SIXG["6G 통합망"]
        columns 2
        AI["AI-Native 제어"]
        COMPUTE["분산 컴퓨팅"]
        ACCESS["지상•NTN 통합 접속"]
        RADIO["다중 대역•RIS 무선"]
    end
    AI --- COMPUTE
    AI --- ACCESS
    ACCESS --- RADIO
```

| 구성요소 | 책임 |
|:---|:---|
| AI-Native 제어 | 관측값으로 경로•빔•**자원 정책** 결정 |
| 분산 컴퓨팅 | 추론•응용을 단말•에지•중앙에 **분산 배치** |
| 지상•NTN 통합 접속 | 지상 셀과 위성 **접속 경로** 연계 |
| 다중 대역•RIS 무선 | **대역•빔•반사 위상 기반 무선 경로 형성** |

#### 한줄 요약

- 망이 채널과 주변 환경을 보고 지상•위성 경로와 연산 위치를 함께 고르는 구조다

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **디지털 트윈**: 실제 망 상태를 가상 모델에 동기화해 자원 정책의 결과를 예측하는 모델
- **폐루프 제어**: 관측•판단•실행 결과를 다시 관측해 설정을 반복 조정하는 제어 방식
- **인공지능 정책(Artificial Intelligence Policy, AI Policy)**: 관측•예측 결과로 경로•빔•연산 위치를 결정하는 제어 정책

</details>

```mermaid
sequenceDiagram
    participant 관측체계
    participant 디지털트윈
    participant AI정책
    participant 통합자원
    관측체계->>디지털트윈: 1. 채널•센싱 상태
    디지털트윈->>AI정책: 2. 예측 상태
    AI정책->>통합자원: 3. 통합 자원 정책
    통합자원-->>디지털트윈: 4. 실행 성과
```

**동작 원리**

1. **채널•센싱 상태**: **디지털 트윈 망 상태 동기화**
2. **예측 상태**: 자원 정책별 지연•연결 품질 예측
3. **통합 자원 정책**: 경로•빔•**연산 위치** 동시 지정
4. **실행 성과**: 정책 결과를 다음 제어 주기에 반영하는 **성과 피드백**

> 요약: 관측•정책 실행•성과 피드백의 **폐루프 제어**

#### 한줄 요약

- 현재 망 상태를 가상 모델에 비춰 보고 경로를 바꾼 뒤 결과가 나쁘면 다시 조절한다

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **6세대 이동통신(Sixth Generation, 6G) 후보 기술**: 국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030) 목표 달성을 위해 연구 중이지만 아직 확정 규격이 아닌 테라헤르츠(Terahertz, THz)•재구성 지능형 표면(Reconfigurable Intelligent Surface, RIS)•인공지능 내재형(Artificial Intelligence-Native, AI-Native) 등의 기술
- **5세대 이동통신(Fifth Generation, 5G)**: 초광대역•초저지연•대규모 접속을 상용화한 현재 이동통신 세대
- **통신•센싱 통합(Integrated Sensing and Communication, ISAC)**: 같은 무선 자원으로 데이터 통신과 환경 감지를 함께 수행하는 기술
- **인공지능(Artificial Intelligence, AI)**: 망 상태를 분석해 경로•빔•자원 정책을 자동 결정하는 기술

</details>

| 이동통신 세대 | 6G | 5G |
|:---|:---|:---|
| 적용 기준 | 미래 사용 시나리오와 후보 기술 검증 | 상용 이동통신 서비스 구축 |
| 핵심 특징 | **AI•ISAC** 기반 지상•비지상 통합 | **초광대역•초저지연** 통신 상용화 |
| 한계 | 후보 기술의 **표준•성숙도** 불확실성 | 센싱 내재화•**입체 연결** 제약 |

> 요약: 6G는 통합 목표와 후보 기술을 구분해 검증

#### 한줄 요약

- 5G는 지금 구축할 규격이고 6G는 앞으로 맞출 목표와 기술 후보를 검증하는 단계다

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **기술 성숙도**: 후보 기술이 연구•시험 단계를 거쳐 실제 서비스에 적용 가능한 수준에 도달했는지를 나타내는 기준
- **수동 복구**: 인공지능(Artificial Intelligence, AI) 정책이 오판할 때 운영자가 안전한 설정으로 직접 되돌리는 절차
- **국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030)**: 6세대 이동통신(Sixth Generation, 6G) 사용 시나리오와 목표 역량을 제시하는 국제 이동통신 체계
- **비지상망(Non-Terrestrial Network, NTN)**: 위성•고고도 플랫폼으로 지상망의 연결 범위를 보완하는 망

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 후보 기술을 확정 규격으로 오인한 **선행 투자** | **IMT-2030 목표•성숙도** 분리 검증 | 미성숙 기술 투자 비용 감소 |
| **AI 정책 오판에 따른 망 전체 품질 저하** | 정책 한계와 **수동 복구** 기준 설정 | 오판 영향 범위•복구 시간 감소 |
| **지상•NTN 전환 지연에 따른 연결 단절** | 궤도별 **전환•복구 시간** 시험 | 재난 통신의 연결 단절 감소 |

#### 한줄 요약

- 지상 기지국이 끊기면 위성 경로로 바뀌는 시간을 확인한다

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **단계 도입**: 국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030) 시나리오별 요구와 기술 성숙도를 검증한 뒤 충족한 기술부터 순차 적용하는 방식
- **6세대 이동통신(Sixth Generation, 6G)**: 통신•센싱•지능•컴퓨팅 통합을 목표로 하는 차세대 이동통신 체계

</details>

- **IMT-2030** 시나리오별 성숙도를 검증해 충족 기술만 단계 도입

#### 한줄 요약

- 6G 목표마다 구현 가능성과 표준 성숙도를 확인한 기술만 단계적으로 선택해야 한다.
