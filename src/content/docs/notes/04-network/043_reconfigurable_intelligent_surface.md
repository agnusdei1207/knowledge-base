---
sidebar:
  order: 43
  label: "043. 지능형 반사 표면 (RIS, Reconfigurable Intelligent Surface)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "지능형 반사 표면 (RIS, Reconfigurable Intelligent Surface)"
date: "2026-08-13T17:04:00+09:00"
tags:
  - "notes-network"
weight: 43
extra:
  question_no: "043"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "설명형: 135회 6G RIS 핵심 구성요소"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **재구성 지능형 표면(Reconfigurable Intelligent Surface, RIS)**: 메타물질(Metamaterial) 기반 단위 셀 소자의 반사 계수를 조절하여 입사하는 전파의 반사 위상과 빔 방향을 실시간 재구성하는 무선 표면 기술이다.

</details>

- 정의/개념: **재구성 지능형 표면(RIS, Reconfigurable Intelligent Surface)**은 메타물질 기반 수백~수천 개의 수동 반사 소자(Unit Cell)로 구성되어, 입사하는 무선 전파의 위상(Phase)과 진폭(Amplitude)을 제어기(Controller)로 실시간 조절하여 빔을 원하는 전파 음영 구역으로 회절·반사시키는 차세대 6G 무선 기술이다.
- 배경/필요성: 5G mmWave(28GHz) 및 6G Sub-THz(100GHz~) 전파의 극심한 직진성과 장애물/건물 차폐로 발생하는 전파 음영 구역(NLOS) 문제를 고비용·고전력 능동 증폭기(RF Chain) 없이 극복하기 위해 개발되었다.

#### 한줄 요약

- 메타물질 수동 반사 소자의 위상을 실시간 제어하여 고주파 전파의 섀도잉 음영 구역으로 빔포밍 반사 경로를 형성하는 6G 핵심 무선 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **연쇄 채널(Cascaded Channel)**: 기지국과 RIS 간 무선 채널(BS-RIS)과 RIS와 단말 간 무선 채널(RIS-UE)이 곱해진 결합 전파 검증 경로이다.
- **빔 이탈(Beam Misalignment)**: 단말의 이동이나 채널 추정 지연으로 인해 RIS 반사 빔의 위상 집속 위치와 실제 단말의 위치가 어긋나 수신 전력이 급감하는 현상이다.

</details>

- **초저전력 수동 전파 제어**: 신호를 능동 증폭하는 RF Chain(전력 증폭기)이 없어 전력 소모가 극소(수 mW 이하)하며 잡음 증폭(Noise Amplification)이 발생하지 않는다.
- **스마트 전파 환경(Smart Radio Environment) 구축**: 차폐된 비가시 영역(NLOS)에 고지향성 반사 빔을 형상화하여 가시 영역(LOS) 통신 환경으로 정밀 제어 변환한다.
- **위상 동상 결합(Phase Coherent Combining)**: 제어기가 소자별 반사 위상을 개별 조정하여 수신 단말 위치에서 모든 반사파가 동일한 위상으로 동상 중첩되게 하여 신호 전력을 극대화한다.

#### 한줄 요약

- 능동 RF 증폭기 없는 저전력 메타표면 구조, 실시간 위상 제어를 통한 수동 빔포밍, 전파 음영 구역의 NLOS-to-LOS 전환 제공.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **단위 셀(Unit Cell Element)**: 독립적인 위상 Shift 및 진폭 응답을 제공하는 메타물질 기반의 최소 수동 반사 소자 단위이다.
- **반사 계수(Reflection Coefficient)**: 입사 전파 신호 대비 반사 신호의 진폭 변쇄비 및 위상 변화량을 결정하는 복소수 변수이다.

</details>

```text
지능형 반사 표면 (RIS) 하드웨어 아키텍처
├─ 전파 수용 및 반사 계층 (Metamaterial Unit Cell Array)
├─ 위상 및 진폭 변조 제어부 (PIN Diode / Varactor Controller)
└─ 기지국 연동 제어 인터페이스 (BS Control Link & Channel Estimator)
```

선의 의미: 기지국 연동 인터페이스가 채널 상태를 전달하면 위상 제어부가 PIN 다이오드를 구동하여 메타물질 단위 셀 배열의 반사 위상을 조절하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 단위 셀 배열 (Unit Cell Array) | 메타표면에 패치 형태로 배치되어 전파를 수용하고 설정된 위상값으로 파형 반사 |
| 위상 및 진폭 제어부 | PIN 다이오드 또는 바랙터(Varactor)의 온/오프 상태를 바꿈으로써 1bit~3bit 위상 변조 수행 |
| 기지국 연동 제어 링크 | 기지국(gNB)으로부터 계산된 소자별 반사 계수를 받거나 채널 추정 알고리즘 연동 |
| 채널 추정기 (Channel Estimator) | 기지국-RIS-단말 간 연쇄 채널(Cascaded Channel)의 복소 위상값 추정 |

#### 한줄 요약

- 메타물질 단위 셀 배열, PIN 다이오드/바랙터 위상 제어기 및 기지국 연동 채널 추정 인터페이스로 구성된 수동 반사 시스템.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **채널 추정(Channel Estimation)**: 기지국이 보낸 파일럿(Pilot) 신호를 기반으로 BS-RIS 및 RIS-UE 간 연쇄 채널 행렬을 추정하는 알고리즘이다.
- **위상 결합(Phase Coherent Combining)**: 여러 단위 셀에서 반사된 전파들의 위상이 단말 위치에서 정확히 동상(In-phase)으로 중첩되도록 각 소자의 반사 위상을 보정하는 기법이다.

</details>

```text
1. 기지국 파일럿 기준 신호 관측 (Pilot Signal Transmission)
      │
      v
2. 기지국-RIS-단말 간 연쇄 채널 추정 (Cascaded Channel Estimation)
      │
      v
3. 반사 계수 및 소자별 위상값 계산·설정 (Phase Shift Configuration)
      │
      v
4. 데이터 패킷 입사 및 수동 빔포밍 반사 (Signal Incident & Reflection)
      │
      v
5. 단말 위치에서의 무선 신호 위상 동상 결합 (Phase Coherent Combining)
      │
      v
단말 이동•채널 변동 시 위상 재계산
```

### 동작 원리

1. **파일럿 신호 송신 및 관측**: 기지국이 전파를 송신하고, RIS 표면을 거쳐 수신 단말에 도달하는 기준 신호(Pilot)를 관측한다.
2. **연쇄 채널(Cascaded Channel) 추정**: 기지국 및 컨트롤러가 기지국-RIS-단말 간의 전체 복소 채널 행렬을 정밀 추정한다.
3. **소자별 반사 계수 매핑**: 수신 단말 위치에서 신호가 극대화되도록 소자별 개별 위상 반사각(0~360도)을 도출하여 RIS 제어기에 하향 설정한다.
4. **수동 빔포밍 전파 반사**: 기지국에서 발사된 고주파(Sub-THz) 데이터 신호가 RIS 소자 배열에 부딪히며 설정된 위상각으로 회절 반사된다.
5. **단말 위치에서의 무선 신호 위상 동상 결합**: 반사파 집속

#### 한줄 요약

- 기준 신호 수신, 연쇄 채널 추정, 소자별 위상 계산 및 메타표면 수동 빔포밍을 통해 단말 위치로 신호를 동상 결합시키는 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **중계기(Repeater / AF Relay)**: 약해진 무선 신호를 수신하여 능동 RF 전력 증폭기를 거쳐 재송신하는 전통적 커버리지 확장 장비이다.
- **무선주파수 회로 계통(Radio Frequency Chain, RF Chain)**: 주파수 변환기, 혼합기, 저잡음 증폭기(LNA) 및 전력 증폭기(PA)로 구성된 능동 회로 계통이다.

</details>

| 비교 항목 | **지능형 반사 표면 (RIS)** | **기존 무선 중계기 (AF Relay / Repeater)** |
|:---|:---|:---|
| 작동 원리 | 메타물질 반사 소자 위상 변조 (수동 빔포밍) | RF 체인 신호 수신, 증폭 및 재송신 (능동 증폭) |
| RF Chain 및 전력 소모 | 수동 소자 중심•제어 전력 필요 | RF 증폭기•복합 회로 전력 필요 |
| 증폭 잡음 (Noise Amplification) | 신호를 증폭하지 않으므로 잡음 증폭 없음 | 수신 신호와 열잡음을 함께 증폭하여 SNR 저하 |
| 통신 방식 | 수동 반사•별도 재송신 없음 | 반이중 또는 자기간섭 통제 필요 |
| 구축 비용 | 대면적 소자•제어망 비용 | RF 증폭 장비•전원 비용 |

> 요약: RIS는 RF 증폭기 없이 저전력으로 잡음 증폭 없는 수동 빔포밍을 제공하고, 중계기는 능동 증폭을 통해 원거리 감쇄를 보상.

#### 한줄 요약

- RIS는 RF 증폭기 없이 저전력으로 잡음 증폭 없는 수동 빔포밍을 제공하고, 중계기는 능동 증폭을 통해 원거리 감쇄를 보상.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **신호 대 잡음비(Signal-to-Noise Ratio, SNR)**: 수신 단말에 도달하는 유효 신호 전력 대 잡음 전력의 비로, 수신 품질의 척도이다.
- **위상 양자화(Phase Quantization Error)**: RIS 소자가 연속적인 위상을 표현하지 못하고 1bit(0,180도) 또는 2bit(0,90,180,270도) 등 이산적 양자화값을 지원함에 따른 반사 빔 성능 손실이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 연쇄 채널 추정 오버헤드 | 소자 수가 수백 개로 증가 시 파일럿 신호 추정 시간 폭증 | 딥러닝 기반 채널 추정 및 소자 블록(Group) 단위 제어 | 채널 추정 오버헤드 단축 및 실시간 위상 갱신 |
| 위상 양자화 오차 | 1bit 저가 소자 사용 시 빔 집속 정확도 저하 | 2bit/3bit 양자화 소자 채택 및 빔포밍 코드북 최적화 | 위상 양자화 손실 최소화 및 SNR 3dB 이상 추가 확보 |
| 단말 고속 이동 시 빔 이탈 | 단말 이동 속도를 RIS 위상 재계산 주기가 따라가지 못함 | 단말 이동 궤적 예측 기반 Predictive Beamtracking | 빔 이탈 예방 및 데이터 전송 끊김 방지 |
| RIS 입사 전력 부족 | 기지국과 RIS 간 거리가 지나치게 멀어 전파 도착 전 감쇄 | 기지국-RIS 간 직진성 LOS 무선 가시 경로 사전 확보 | 입사 전력 확보 및 RIS 수동 반사 이득 극대화 |

#### 한줄 요약

- 2bit/3bit 위상 양자화 메타소자 적용, Deep Learning 연쇄 채널 추정, 기지국-RIS 제어 인터페이스 지연 단축으로 RIS 전파 성능 극대화.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **입사 전력(Incident Power)**: 기지국으로부터 RIS 물리 표면에 도착하는 단위 면적당 전파 에너지 전력값이다.

</details>

- 전원•증폭이 필요하면 **중계기**, 수동 경로 보정은 **RIS** 선택

#### 한줄 요약

- 고주파 전파 음영 해소를 위한 RIS 수동 빔포밍 최적 위치 선정 및 연쇄 채널 추정 시스템 구현 필수.
