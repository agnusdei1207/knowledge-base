---
sidebar:
  order: 77
  label: "077. IoT 아키텍처"
  badge:
    text: "미출 · 30%"
    variant: note
title: "사물인터넷 E2E 시스템 구조 : IoT 아키텍처 (IoT Architecture)"
date: "2026-08-26T14:03:33+09:00"
tags:
  - "notes-network"
weight: 77
extra:
  question_no: "77"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "Device-Gateway-Edge-Cloud 4계층 구조, 디바이스 수명주기(LCM), 양방향 제어 및 OTA"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IoT (Internet of Things)**: 사물에 센서·통신 기능을 내장하여 사람의 개입 없이 데이터를 수집하고 물리 세계를 제어하는 초연결망.
- **IoT Reference Architecture**: Device, Gateway, Edge, Cloud 4계층으로 이종 장치 연동과 수명주기 관리(LCM)를 표준화한 청사진 (ISO/IEC 30141).

</details>

- 정의/개념: Device·Gateway·Edge·Cloud의 **E2E IoT 구조**
- 배경/필요성: 이종 단말 난립으로 **프로토콜 파편화·실시간 제어 제약**

#### 한줄 요약
- **4계층 연계**로 데이터 수집부터 지능형 제어까지 완결

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Protocol Translation (프로토콜 변환)**: BLE, Zigbee, Modbus 등 비-IP 산업용/근거리 프로토콜을 표준 TCP/IP 및 MQTT, HTTPS로 상호 변환하는 기능.
- **Device Shadow / Digital Twin**: 단말 오프라인 시에도 클라우드 상에서 마지막 상태(Reported)와 목표 상태(Desired)를 동기화하는 가상 복제본.

</details>

- **프로토콜 변환**: 비 IP 신호를 Gateway에서 MQTT로 변환
- **엣지 자율성**: 망 단절에도 로컬 안전 제어 수행
- **디바이스 섀도우**: 접속과 무관하게 목표 상태 유지

#### 한줄 요약
- **프로토콜 변환·엣지 자율성·섀도우 동기화** 제공

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Device-Gateway-Edge-Cloud**: 단말(Device), 중계 변환(Gateway), 분산 컴퓨팅(Edge), 중앙 플랫폼(Cloud)의 4계층 계층 구조.

</details>

```text
[IoT 4계층 구조]
|-- 클라우드 계층
|-- 엣지 계층
|-- 게이트웨이
`-- 디바이스 계층
```

선의 의미: 말단 센서 데이터가 게이트웨이와 엣지를 거쳐 클라우드로 취합되고 제어 명령이 역방향으로 하향 전달되는 구조

| 계층 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 클라우드 계층 | **섀도우·분석·OTA 관리** | SaaS / PaaS |
| 엣지 계층 | **로컬 분석·단절 자율 운영** | Edge Server |
| 게이트웨이 | **BLE·Zigbee·Modbus 변환** | L2~L7 변환 |
| 디바이스 계층 | **센싱·액추에이션** | MCU, RTOS |

#### 한줄 요약
- Device, Gateway, Edge, Cloud 4계층이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **A/B Dual Partition OTA**: 플래시 메모리를 A/B 파티션으로 분할하여 신규 펌웨어를 백그라운드 설치 후 무결성 검증을 거쳐 부팅하는 안전 무선 업데이트.

</details>

```text
센서 데이터
    |
1. 상호 인증
    |
2. 텔레메트리 변환
    |
3. 엣지 실시간 판단
    |
4. 클라우드 분석
    |
5. 섀도우 동기화·OTA
    |
제어 명령
```

- 1. 상호 인증
- 2. 텔레메트리 변환
- 3. 엣지 실시간 판단
- 4. 클라우드 분석
- 5. 섀도우 동기화·OTA

#### 한줄 요약
- **인증·엣지 판단·클라우드 분석·OTA** 순으로 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Gateway-Centric** vs **Edge-Centric** vs **Direct Cellular**: 저전력 센서망, 고성능 자율 제어 산업망, 이동 자산 트래커.

</details>

| 비교 항목 | 게이트웨이 중계형 (Gateway-Centric) | 엣지 컴퓨팅형 (Edge-Centric) | 직접 연결형 (Direct Cellular) |
|:---|:---|:---|:---|
| 통신 인프라 | BLE·Zigbee·LoRa | TSN·산업 이더넷·5G | **5G NR·LTE-M·NB-IoT** |
| 제어 지연 시간 | 100ms~수 초 | **10ms 이하** | 50~200ms |
| 단말 자원 소모 | **낮음** | 중간 | 높음 |
| 오프라인 자율성 | 낮음 | **매우 높음** | 없음 |
| 대표 적용 분야 | 스마트홈·검침 | **공장·로봇·자율주행** | 차량·웨어러블·자산 추적 |

#### 한줄 요약
- **Gateway는 저전력**, Edge는 실시간, 직결은 이동성 중심

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Device Bricking (단말 벽돌화)**: OTA 펌웨어 업데이트 중 전원 차단이나 이미지 손상으로 부트로더가 훼손되어 장비가 영구 마비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 백홀 단선 시 현장 제어 마비 | **엣지 자율 페일오버·로컬 룰 엔진** | 단절 중 안전 제어 지속 |
| OTA 중단 시 **단말 벽돌화** | **A/B 듀얼 뱅크·자동 롤백** | 손상 펌웨어 복구 |
| 망 복구 후 **타임스탬프 왜곡** | **로컬 버퍼·브로커 멱등성** | 시계열 정합성 유지 |
| 기기 탈취로 키·펌웨어 유출 | **하드웨어 RoT·TPM** | 키 추출·변조 차단 |

#### 한줄 요약
- **엣지 자율성·A/B OTA·RoT**로 가용성과 보안 확보

## Ⅶ. 결론

- 저전력 연결은 **Gateway**, 실시간 제어는 **Edge·A/B OTA** 선택

#### 한줄 요약
- **4계층 IoT 구조**로 연결성과 현장 자율성 균형
