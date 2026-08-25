---
sidebar:
  order: 77
  label: "077. IoT 아키텍처"
  badge:
    text: "미출 · 30%"
    variant: note
title: "사물인터넷 E2E 시스템 구조 : IoT 아키텍처 (IoT Architecture)"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: 물리 센서·액추에이터(Device), 이종 프로토콜 변환(Gateway), 초저지연 로컬 제어(Edge), 빅데이터 분석(Cloud)으로 구성되는 **E2E 사물인터넷 시스템 아키텍처**
- 배경/필요성: 수백만 대의 저전력 이종 단말 난립으로 인한 **통신 프로토콜 파편화, 클라우드 전송 지연에 따른 실시간 제어 실패 및 전사 장비(OTA/보안) 관리 불가**

#### 한줄 요약
- Device, Gateway, Edge, Cloud 4계층을 유기적으로 연계하여 데이터 수집부터 지능형 제어까지 E2E로 완결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Protocol Translation (프로토콜 변환)**: BLE, Zigbee, Modbus 등 비-IP 산업용/근거리 프로토콜을 표준 TCP/IP 및 MQTT, HTTPS로 상호 변환하는 기능.
- **Device Shadow / Digital Twin**: 단말 오프라인 시에도 클라우드 상에서 마지막 상태(Reported)와 목표 상태(Desired)를 동기화하는 가상 복제본.

</details>

- **이종 디바이스 프로토콜 통합 변환**: BLE, Zigbee, Modbus 등 **비-IP 신호를 Gateway에서 표준 IP/MQTT로 변환**
- **초저지연 엣지 자율성(Edge Autonomy)**: 네트워크 단절 시에도 **엣지 레벨(10ms 이내)에서 독립 안전 제어 루프 수행**
- **디바이스 섀도우 기반 비동기 상태 동기화**: 단말 접속 상태와 무관하게 **클라우드 상에서 목표 제어 상태(Desired) 유지**

#### 한줄 요약
- 이종 프로토콜 변환, 엣지 초저지연 자율성, 디바이스 섀도우 기반 비동기 상태 동기화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Device-Gateway-Edge-Cloud**: 단말(Device), 중계 변환(Gateway), 분산 컴퓨팅(Edge), 중앙 플랫폼(Cloud)의 4계층 계층 구조.

</details>

```text
[IoT 엔드투엔드 4계층 시스템 아키텍처]
|-- Cloud Platform Layer (AWS IoT / Azure IoT Hub)
|   |-- Device Registry (X.509 인증서 신원 인증 및 자격 증명)
|   |-- Device Shadow / Digital Twin (Desired vs Reported 상태 동기화)
|   `-- Time-Series DB & AI Analytics (빅데이터 분석 및 전역 A/B OTA 배포)
`-- Edge Computing Layer (Edge Gateway: K3s, EdgeX Foundry -> 10ms 초저지연 로컬 자율 제어)
`-- Gateway Layer (Protocol Translation: BLE/Zigbee/Modbus/RS-485 <-> MQTT/IP 변환)
`-- Device Layer (Sensors & Actuators: 온습도, 진동, 압력 센서 및 서보 모터, 밸브)
```

선의 의미: 말단 센서 데이터가 게이트웨이와 엣지를 거쳐 클라우드로 취합되고 제어 명령이 역방향으로 하향 전달되는 구조

| 계층 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **클라우드 계층 (Cloud)** | **전역 디바이스 상태 동기화(Shadow), 빅데이터 분석, OTA 배포 총괄** | SaaS / PaaS |
| **엣지 계층 (Edge)** | **10ms 이내 초저지연 로컬 분석 및 클라우드 단절 시 자율 운영** | Edge Server |
| **게이트웨이 (Gateway)**| **BLE, Zigbee, Modbus를 IP/MQTT로 상호 번역 및 패킷 필터링** | L2~L7 변환 |
| **디바이스 계층 (Device)**| **물리 환경 계측(Sensing), 전기 신호 변환, 기계식 구동(Actuation)** | MCU, RTOS |

#### 한줄 요약
- Device, Gateway, Edge, Cloud 4계층이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **A/B Dual Partition OTA**: 플래시 메모리를 A/B 파티션으로 분할하여 신규 펌웨어를 백그라운드 설치 후 무결성 검증을 거쳐 부팅하는 안전 무선 업데이트.

</details>

```text
IoT 텔레메트리 수집 및 디바이스 섀도우 제어 파이프라인
        │
   1. [상호 인증] 단말이 X.509 인증서 및 TPM 토큰으로 게이트웨이/클라우드에 mTLS 상호 인증
        │
   2. [텔레메트리 수집 및 변환] 센서 측정값을 게이트웨이가 MQTT/Protobuf로 변환하여 상향 스트리밍
        │
   3. [엣지 로컬 실시간 판단] 엣지 분석 엔진이 임계치 초과 감지 시 즉각 로컬 액추에이터 긴급 차단
        │
   4. [클라우드 AI 분석] 클라우드가 시계열 데이터를 집계하고 최적 제어 파라미터 산출
        │
   ▼
5. [디바이스 섀도우 동기화 및 OTA] 목표 상태(Desired)를 하향 주입하고 A/B 듀얼 뱅크 무선 패치 집행
```

#### 한줄 요약
- 상호 인증 → 텔레메트리 전송 → 엣지 저지연 판단 → 클라우드 분석 → 디바이스 섀도우 제어 및 OTA 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Gateway-Centric** vs **Edge-Centric** vs **Direct Cellular**: 저전력 센서망, 고성능 자율 제어 산업망, 이동 자산 트래커.

</details>

| 비교 항목 | 게이트웨이 중계형 (Gateway-Centric) | 엣지 컴퓨팅형 (Edge-Centric) | 직접 연결형 (Direct Cellular) |
|:---|:---|:---|:---|
| **통신 인프라** | BLE, Zigbee, LoRa $\rightarrow$ 게이트웨이 | TSN, Industrial Ethernet, 5G 특화망 | **5G NR, LTE-M, NB-IoT 셀룰러 직결** |
| **제어 지연 시간** | 중간 (100ms ~ 수 초) | **초저지연 ($\le 10\text{ms}$ 현장 완결)** | 통신 왕복 지연 (50~200ms) |
| **단말 자원 소모** | **초경량 MCU (코인 배터리 수년 구동)** | 경량 RTOS 및 센서 노드 | 고성능 모뎀 및 대용량 배터리 요구 |
| **오프라인 자율성**| 낮음 (게이트웨이 캐싱 의존) | **매우 높음 (로컬 엣지 독립 제어)** | 전무 (기지국 단선 시 제어 불가) |
| **대표 적용 분야** | 스마트홈, 원격 검침(AMI), 스마트팜 | **스마트팩토리, 로봇 제어, 자율주행** | 커넥티드 카, 스마트 워치, 자산 트래커 |

#### 한줄 요약
- 게이트웨이형은 저전력 센서망, 엣지형은 미션 크리티컬 산업망, 직접 연결형은 모바일 자산 트래킹에 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Device Bricking (단말 벽돌화)**: OTA 펌웨어 업데이트 중 전원 차단이나 이미지 손상으로 부트로더가 훼손되어 장비가 영구 마비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| WAN 클라우드 백홀 단선 시 현장 설비 모니터링 및 비상 제어 마비 | **현장 `엣지(Edge Gateway) 자율 페일오버 및 로컬 룰 엔진`** 구축 | 네트워크 단절 시에도 100% 현장 설비 연속성 및 안전 정지 |
| 광역망 불안정 상태에서 OTA 중단 시 **단말 벽돌화(Bricking)** 발생 | **`A/B 듀얼 뱅크 플래시 파티셔닝` 및 부팅 실패 시 자동 롤백** | 펌웨어 손상으로 인한 현장 출동 제거 및 100% 무중단 복구 |
| 네트워크 복구 시 대규모 단말 데이터 일시 유입으로 **타임스탬프 왜곡** | **`단말 로컬 버퍼링 타임스탬프 보존` 및 메시지 브로커 멱등성** 처리 | 중복 데이터 삽입 방지 및 시계열 분석 정합성 유지 |
| 말단 IoT 기기의 물리적 탈취를 통한 펌웨어 추출 및 암호키 유출 위협 | **`하드웨어 RoT (Root of Trust) 및 TPM/Secure Element` 칩셋 탑재** | 기기 내 저장된 개인키 무단 추출 및 펌웨어 변조 원천 차단 |

#### 한줄 요약
- 엣지 자율 제어, A/B 듀얼 뱅크 OTA, 타임스탬프 로컬 보존, 하드웨어 RoT 보안으로 운영한다.

## Ⅶ. 결론

- 대규모 분산 디바이스의 지능형 제어와 비즈니스 통찰을 확보하기 위해 **Device-Gateway-Edge-Cloud 4계층 IoT 아키텍처를 표준 모델로 도입**하되, 현장 운영의 신뢰성과 보안성을 담보하기 위해 **A/B 듀얼 뱅크 기반 안전한 OTA 체계, 엣지 자율 분산 제어, 하드웨어 RoT(Root of Trust) 기반 엔드투엔드 보안**을 통합 구축하여 고가용성 스마트 IoT 생태계 완성

#### 한줄 요약
- IoT 아키텍처는 Device-Gateway-Edge-Cloud 4계층 구조를 통해 대규모 사물 데이터 수집과 엣지/클라우드 지능형 제어를 실현하는 핵심 인프라다.