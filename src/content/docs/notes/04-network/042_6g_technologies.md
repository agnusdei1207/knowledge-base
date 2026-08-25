---
sidebar:
  order: 42
  label: "042. 6G 핵심 기술"
  badge:
    text: "기출 · 70%"
    variant: note
title: "6G 이동통신 핵심 기술 : IMT-2030 (6G Technologies)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 42
extra:
  question_no: "42"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "ITU-R IMT-2030 6대 시나리오, Sub-THz 대역, ISAC(통신·센싱 융합), AI-Native"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IMT-2030 (6G)**: ITU-R에서 정의한 2030년대 차세대 이동통신 표준으로 최대 1Tbps 전송률과 0.1ms 무선 지연을 지향하는 프레임워크.
- **AI-Native Network**: 물리 계층(PHY) 신호 처리부터 코어망 오케스트레이션까지 딥러닝 AI가 완전 내재화되어 자율 제어되는 구조.

</details>

- 정의/개념: 테라헤르츠(Sub-THz), 비지상망(**NTN**), 통신·센싱 융합(**ISAC**), **RIS**, **AI-Native**를 결합하여 **지상-우주를 연결하는 차세대 이동통신 기술(IMT-2030)**
- 배경/필요성: 5G 지상 2D 평면 통신의 한계로 인한 **UAM/항공/해양 초공간 음영, 실시간 홀로그램(Tbps) 전송 및 환경 인식 센싱 결합 불가**

#### 한줄 요약
- Sub-THz 대역, 3차원 NTN, ISAC 센싱 융합, AI-Native 자율 제어를 통해 초공간 통신을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ISAC (Integrated Sensing and Communication)**: 통신 신호 자체로 주변 환경의 3차원 위치, 형상, 속도를 고해상도로 탐지하는 레이더-통신 융합 기술.
- **Sub-THz (100GHz~3THz)**: 수십 GHz 이상의 초광대역 연속 채널을 확보하여 테라비트(Tbps)급 초고속 전송을 가능하게 하는 주파수 대역.

</details>

- **극대화된 무선 전송 성능**: Sub-THz 대역을 활용하여 **최대 1Tbps 전송 속도 및 0.1ms(100㎲) 이하 초저지연 달성**
- **3차원 초공간 커버리지(NTN)**: 저궤도(LEO) 위성과 성층권 HAPS를 지상망과 수직 통합하여 지구 전역 음영 배제
- **물리 환경 인지 융합(ISAC)**: 통신 전파 파형을 공간 센싱 매체로 활용하여 cm급 고정밀 위치 추적 및 제스처 인식

#### 한줄 요약
- 1Tbps 처리량, NTN 3D 입체 커버리지, ISAC 환경 센싱, AI-Native 자율 제어를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Deep Distributed Computing**: 단말, 엣지, 클라우드, 우주 위성 노드의 이기종 컴퓨팅 자원을 단일 가상 컴퓨터로 통합하는 연산 프레임워크.

</details>

```text
[6G 초공간·초감각 융합 네트워크 아키텍처]
|-- Space / Aerial Layer (NTN: LEO 저궤도 위성군, HAPS 성층권 비행체 -> 전 지구 3D 커버리지)
`-- Terrestrial Radio Access Layer
    |-- Sub-THz Massive MIMO gNB (100GHz~1THz 초광대역 피크 전송)
    |-- RIS Metasurfaces (건물 외벽/유리창 메타물질 위상 제어 수동 반사)
    `-- ISAC Dual-Functional Rad-Comm (통신 데이터 송수신 + 3D 공간 환경 센싱)
`-- Control & Compute Layer
    |-- AI-Native Core & Zero-Touch Automation (머신러닝 자율 빔포밍/슬라이싱)
    `-- Deep Distributed Computing & Real-time Digital Twin
```

선의 의미: 계층 및 우주 NTN 위성망과 지상 Sub-THz/RIS 무선망이 AI-Native 코어 및 분산 컴퓨팅으로 융합되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **Sub-THz 무선 전송** | 100GHz~1THz 대역에서 수십 GHz 대역폭을 결합하여 **1Tbps 피크 속도 및 초저지연 전송** | 광소자-RF 융합 |
| **지능형 반사 표면 (RIS)**| 초고주파의 차폐 감쇠를 극복하기 위해 **메타물질로 전파 경로를 수동 조향·집속** | 스마트 무선 환경 |
| **비지상 네트워크 (NTN)** | LEO 위성군 및 HAPS 연계를 통해 **지상 10km 이상 상공 및 해양 통신 음영 완전 해소** | 3차원 3D 통신 |
| **통신·센싱 융합 (ISAC)** | 단일 전파 파형으로 **고속 데이터 전송과 mm 단위 공간 객체 감지/추적 동시 수행** | DFRC 통합 파형 |
| **AI-Native 코어 및 트윈**| 물리 통신 환경을 디지털 트윈으로 복제하고 **AI 기반으로 빔포밍과 자원을 자율 스케줄링** | 제로터치 오토메이션 |

#### 한줄 요약
- Sub-THz 전송, RIS 메타표면, NTN 위성망, ISAC 센싱, AI-Native 코어가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Digital Twin 무선 예측**: 무선 채널의 전파 경로와 장애물 환경을 실시간 가상 공간에 복제하여 수 초 후의 채널 품질을 사전 예측하는 기술.

</details>

```text
6G ISAC 공간 센싱 및 1Tbps 초공간 통신 파이프라인
        │
   1. [ISAC 통합 파형 송출] 기지국이 레이더-통신 융합 파형을 송출하여 3D 공간 스캔
        │
   2. [디지털 트윈 채널 맵 갱신] 반사파 지연-도플러 분석으로 지형 및 단말 궤적 모델링
        │
   3. [AI 선제적 빔포밍 최적화] AI-Native 엔진이 차폐를 예측하여 인근 RIS 위상 행렬 제어
        │
   ▼
4. [초공간 1Tbps 전송 개시] Sub-THz 지상 링크 및 LEO 위성 NTN 경로를 통해 0.1ms 초저지연 데이터 전송
```

#### 한줄 요약
- ISAC 공간 센싱 → 디지털 트윈 채널 예측 → AI 빔포밍/RIS 제어 → 1Tbps 초광대역 전송 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IMT-2020 (5G)** vs **IMT-2030 (6G)**: 지상 중심 3대 서비스(5G)와 우주 포함 초공간·초감각 6대 서비스(6G).

</details>

| 비교 항목 | 5G 이동통신 (IMT-2020) | 6G 이동통신 (IMT-2030) |
|:---|:---|:---|
| **최대 피크 속도** | **최대 20 Gbps (체감 100 Mbps)** | **최대 1 Tbps (체감 1 Gbps 이상, 50배 향상)** |
| **무선 전송 지연** | **1 ms (User Plane)** | **0.1 ms (100 ㎲ 이하, 10배 단축)** |
| **주요 주파수 대역** | Sub-6GHz (3.5GHz), mmWave (28GHz) | **Sub-THz 대역 (100 GHz ~ 3 THz)** |
| **커버리지 공간** | 지표면 2차원 평면 (지상 기지국 의존) | **지상 + 공중(UAM) + 해양 + 우주 3차원 (NTN)** |
| **인공지능(AI) 결합**| 상위 플랫폼 보조적 AI 적용 | **물리 계층부터 코어까지 완전 내재화 (AI-Native)** |
| **핵심 신규 서비스** | 스마트폰 eMBB, 스마트팩토리, V2X | **홀로그램 텔레프레즌스, 디지털 트윈, 공간 ISAC** |

#### 한줄 요약
- 5G 대비 50배 속도(1Tbps), 10배 저지연(0.1ms), Sub-THz 대역, 3차원 NTN, AI-Native를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Conditional Handover (조건부 핸드오버, CHO)**: LEO 위성의 고속 이동에 따라 연결 품질이 임계치 이하로 떨어지기 전 사전 구성된 타깃 위성으로 즉각 전환하는 무손실 핸드오버.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Sub-THz 대역의 극심한 대기 흡수 및 건물 차폐로 인한 통신 단절 | **`RIS (지능형 반사 표면)` 및 `분산 다중 안테나(Distributed MIMO)` 배치** | 가상 가시선(LOS) 확보 및 통신 도달 범위 확장 |
| AI 모델 오작동으로 인한 비정상 빔 조향 및 제어 루프 발진 | **`규칙 기반 안전 경계(Safety Boundary)` 및 수동 복구(Manual Fallback)** | 제어 발진 방지 및 통신망 무결성 보장 |
| 저궤도 위성(LEO) 고속 이동에 따른 지연 변동 및 핸드오버 유실 | 궤도 예측 기반 **`사전 조건부 핸드오버(CHO)` 및 도플러 주파수 보상** | 위성 전환 시 통신 단절 방지 및 세션 연속성 확보 |
| 1Tbps 초고속 신호 처리에 따른 기지국 반도체 발열 및 전력 폭증 | **`광자(Photonic) 신호 처리 소자` 및 저전력 뉴로모픽 칩 적용** | 신호 처리 효율 10배 향상 및 에너지 절감 |

#### 한줄 요약
- RIS로 Sub-THz 차폐를 극복하고, 안전 경계로 AI를 통제하며, CHO로 위성 세션을 유지한다.

## Ⅶ. 결론

- 차세대 6G(IMT-2030) 통신 인프라 구축을 위해 **Sub-THz 광대역 전송과 RIS 수동 빔포밍, 저궤도 위성(NTN)을 결합한 3차원 초공간 통신망을 표준화**하고, 레이더와 통신을 융합한 **ISAC 기술과 AI-Native 자율 제어 플랫폼**을 내재화하여 초성능·초지능 글로벌 디지털 신경망 완성

#### 한줄 요약
- 6G 기술은 Sub-THz, 3차원 NTN, ISAC 센싱 융합, AI-Native를 통해 초성능·초공간 통신을 실현하는 차세대 이동통신 패러다임이다.