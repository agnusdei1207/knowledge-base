---
sidebar:
  order: 55
  label: "055. NB-IoT와 LTE-M (NB-IoT LTE-M)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "NB-IoT와 LTE-M (NB-IoT LTE-M)"
date: "2026-08-13T15:38:00+09:00"
tags:
  - "notes-network"
weight: 55
extra:
  question_no: "055"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "비교형: 125회 NB-IoT 동작 Mode 출제"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **협대역 사물인터넷(Narrowband Internet of Things, NB-IoT)**: 180kHz 협대역 주파수와 깊은 실내 커버리지 향상(CE) 기술을 기반으로 고정형 소량 센서를 연결하는 3GPP 표준 LPWAN 기술이다.
- **기계형 롱텀 에볼루션(Long-Term Evolution for Machines, LTE-M / Cat-M1)**: 1.4MHz 대역폭을 사용하여 최대 1Mbps 전송 속도, 이동성 핸드오버 및 VoLTE 음성 통화를 지원하는 3GPP 표준 LPWAN 기술이다.
- **저전력 광역망(Low-Power Wide-Area Network, LPWAN)**: 광역에서 저비용·저전력 IoT 단말의 소용량 데이터를 전송하는 무선 네트워크 계열이다.

</details>

- 정의/개념: **NB-IoT(Narrowband IoT)**와 **LTE-M(Cat-M1)**은 3GPP 면허 주파수 대역에서 대규모 저전력·고커버리지 IoT 서비스를 제공하기 위해 도입된 셀룰러 저전력 광역망(Cellular LPWAN) 2대 핵심 통신 규격이다.
- 배경/필요성: 소량 데이터를 간헐적으로 송신하는 센서 단말에 기존 고비용 LTE 모뎀을 채택할 경우 발생하는 배터리 조기 소모 및 모뎀 단가 부담을 극복하기 위해 제정되었다.

#### 한줄 요약

- 면허 대역에서 절전 기능과 음영 커버리지를 제공하는 3GPP 셀룰러 LPWAN.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **킬로헤르츠(Kilohertz, kHz)**: 주파수의 단위로, NB-IoT는 LTE 자원 블록(PRB) 1개 크기인 180kHz 극협대역을 사용하여 주파수 효율성을 극대화한다.
- **절전 모드(Power Saving Mode, PSM)**: 망 등록 상태를 유지한 채 무선 송수신을 중단하여 단말 소비 전력을 줄이는 절전 기술이다.
- **확장 불연속 수신(extended Discontinuous Reception, eDRX)**: 하향 호출(Paging)을 확인하기 위한 수신 대기 주기를 수십 초에서 수 시간까지 연장하여 전력을 절감하는 기술이다.

</details>

- **NB-IoT (180kHz 초협대역 고정형)**: 180kHz 단일 자원 블록(PRB)을 사용하고, 반복 전송(Repetition)을 통한 커버리지 확장(CE Level)으로 지하 맨홀 등 최대 164dB MCL 링크 예산을 확보한다.
- **LTE-M (1.4MHz 중속 이동형)**: 1.4MHz 대역폭과 이동성, VoLTE 지원으로 추적·음성 서비스에 적합하다.
- **PSM 및 eDRX 절전 기법**: PSM과 긴 Paging 주기의 eDRX를 적용하여 단말 수신 대기 전력을 절감한다.

#### 한줄 요약

- NB-IoT의 180kHz 협대역 고음영 침투성, LTE-M의 1.4MHz 대역폭 및 핸드오버, PSM/eDRX 기반 저전력 수명 보장.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **범용 가입자 식별 모듈(Universal Subscriber Identity Module, USIM)**: 셀룰러 LPWAN 가입자의 고유 식별자(IMSI)와 코어망 접속 인증 키를 제공하는 보안 모듈이다.
- **사물인터넷(Internet of Things, IoT)**: 센서 데이터를 셀룰러 기지국을 통해 서버 플랫폼으로 전달하는 전반적인 장치 응용 네트워크이다.
- **코어망(Evolved Packet Core, EPC / 5GC)**: MME, S-GW/P-GW 및 SCEF(C-SoT 전송)를 포함하여 가입자의 PSM/eDRX 절전 타이머를 설정하고 제어하는 중심망이다.

</details>

```text
셀룰러 LPWAN (NB-IoT / LTE-M) 아키텍처
├─ 사물인터넷 단말 도메인 (IoT Devices with USIM)
├─ 무선 기지국 도메인 (eNB / gNB - In-band / Guard-band / Standalone)
├─ 셀룰러 코어망 도메인 (EPC / 5GC - MME / C-SoT / PSM Timer)
└─ 사물인터넷 서비스 플랫폼 도메인 (IoT Service Platform / OneM2M)
```

선의 의미: USIM이 내재된 IoT 단말이 기지국 무선 구간을 통과하여 5G/LTE 코어망과 PSM 타이머를 협상하고 IoT 서비스 플랫폼으로 데이터를 전달하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 사물인터넷 단말 (IoT Devices) | 현장 상태를 측정하고 USIM 인증을 거쳐 PSM/eDRX 모드 기반으로 업링크 소량 데이터 송신 |
| 무선 기지국 (eNB / gNB) | In-band, Guard-band, Standalone 옵션(NB-IoT)으로 무선 자원을 배치하고 반복 전송 처리 |
| 셀룰러 코어망 (MME / SCEF) | 단말의 망 부착(Attach) 시 T3412(PSM) 및 T3324(Active) 타이머를 협상하고 데이터 라우팅 |
| IoT 서비스 플랫폼 | LwM2M, CoAP, MQTT 프로토콜을 통해 소용량 패킷을 수집하고 앱 서버에 연동 전달 |

#### 한줄 요약

- USIM 단말이 기지국 무선 구간을 거쳐 코어망 MME/C-SoT를 통해 PSM/eDRX 타이머를 인가받고 IoT 플랫폼으로 수송되는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **수신 창(Paging Window / Active Time)**: PSM 및 eDRX 절전 기상 후 단말이 서버로부터의 하향 제어 패킷을 수신하기 위해 무선기를 켜두는 시간 구간이다.

</details>

```text
1. 서비스 이동성 및 전송속도 분석
      │
      ├─ 고정형·소량·음영 ── NB-IoT 선택
      └─ 이동형·중속·음성 ── LTE-M 선택
            │
            v
      2. 무선 채널 배치
            │
            v
      3. 망 등록 및 PSM/eDRX 타이머 협상
            │
            v
      4. 센서 데이터 업링크 전송
            │
            v
      5. Paging 수신 후 PSM 진입
```

### 동작 원리

1. **서비스 이동성 및 전송속도 분석**
2. **무선 채널 배치**
3. **망 등록 및 PSM/eDRX 타이머 협상**
4. **센서 데이터 업링크 전송**
5. **Paging 수신 후 PSM 진입**

#### 한줄 요약

- 특성별 규격 선정, 망 붙임 및 PSM/eDRX 타이머 협상, 업링크 전송, Active Window 대기 및 Deep Sleep 진입 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **핸드오버(Handover)**: 이동하는 단말이 서비스 끊김 없이 이전 기지국에서 인접 기지국으로 무선 세션을 이관하는 통신 기술이다.
- **NB-IoT 배치 방식(In-band / Guard-band / Standalone)**: 기존 LTE 대역 내부(In-band), 대역 간 보호대역(Guard-band), 별도 독자 대역(Standalone)에 NB-IoT 주파수를 할당하는 구동 옵션이다.

</details>

| 비교 항목 | **NB-IoT (Cat-NB1/NB2)** | **LTE-M (Cat-M1/M2)** |
|:---|:---|:---|
| 주파수 대역폭 | 180 kHz (단일 PRB) | 1.4 MHz (6개 PRB) |
| 최대 전송 속도 | 약 26 kbps ~ 125 kbps (DL/UL 소량) | 약 375 kbps ~ 1 Mbps (중속 전송) |
| 기지국 핸드오버 | 미지원 (셀 이동 시 끊김 후 재접속) | 지원 (무손실 Seamless 핸드오버 지원) |
| 음성 통화 (VoLTE) | 미지원 | VoLTE 지원 가능 |
| 커버리지 이득 (MCL) | 164 dB (매우 깊은 지하/수도검침 수용) | 155.7 dB (지상 및 건물 내부 수용) |
| 구축 배치 옵션 | In-band, Guard-band, Standalone 지원 | In-band (기존 LTE 대역 내 전용 배치) |

> 요약: NB-IoT는 180kHz 전용 고정형 지하 센서 및 초고음영 침투에 특화되고, LTE-M은 1.4MHz 대역의 이동성 추적 및 음성 통화에 특화.

#### 한줄 요약

- NB-IoT는 180kHz 전용 고정형 지하 센서 및 초고음영 침투에 특화되고, LTE-M은 1.4MHz 대역의 이동성 추적 및 음성 통화에 특화.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **반복 전송(Repetition / Coverage Enhancement)**: 수신 세기가 극도로 저하된 커버리지 확장(CE) 구역에서 동일 패킷을 반복 송신하여 SNR을 극대화하는 무선 기법이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 과도한 반복 전송 전력 소모 | 지하 deep coverage 노드로 인한 CE Level 최대 적용 | 기지국 인근 전파 재배치 및 무선 감도 튜닝 | 패킷 반복 수치(Repetition Count) 감소 및 배터리 수명 보장 |
| 하향 응답 반응 지연 | PSM 슬립 타임이 너무 길어 실시간 제어 불가능 | eDRX Paging Window 지표 단축 설정 | 서버 하향 명령 수신 시간 수초 이내 조율 |
| 이동 단말 접속 마비 | 고속 이동 기기에 NB-IoT 모뎀을 적용하여 셀 이탈 | 자산 추적 단말에 LTE-M 규격 지정 변경 | 기지국 핸드오버 유지 및 연속적 세션 확보 |
| 오프셋 타이머 불일치 | 단말과 코어망 간 T3412/T3324 타이머 설정 불일치 | 3GPP 표준 NAS 억제 및 코어 프로필 통일 | 미승인 Paging 타임아웃 및 세션 연결 이탈 차단 |

#### 한줄 요약

- PSM/eDRX 타이머 최적화, CE Level 반복 전송 수치 조율, 이동성 요구 시 LTE-M 지정으로 셀룰러 LPWAN 성능 최적화.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **셀룰러 저전력 광역망 선택(Cellular LPWAN Selection Criteria)**: 서비스의 필요 데이터 속도, 이동성, 주파수 음영 정도 및 배터리 수명을 고려해 NB-IoT와 LTE-M 중 적합한 규격을 선택하는 의사결정 프로세스이다.

</details>

- 고정·음영 센서는 **NB-IoT**, 이동·음성 단말은 **LTE-M** 선택.

#### 한줄 요약

- 고정/이동성 요구 조건 및 커버리지 음영 특성에 맞춘 NB-IoT/LTE-M 최적 선정 및 PSM/eDRX 타이머 구현 필수.
