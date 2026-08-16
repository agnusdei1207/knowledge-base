---
sidebar:
  order: 89
  label: "089. 광 인터커넥트 (Optical Interconnect)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "광 인터커넥트 (Optical Interconnect)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 89
extra:
  question_no: "089"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "인공지능 클러스터 대역폭•에너지 병목 대응"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **광 인터커넥트(Optical Interconnect)**: 기존 구리(Copper) 선로의 물리적 감쇠 및 발열 한계를 극복하기 위해, 광파이프라인 및 광섬유(Optical Fiber)를 통해 빛(Laser)으로 데이터를 송수신하는 고속 인터커넥트 기술.
- **E/O & O/E 변환**: 전기 신호를 광 신호로 변환하는 광 송신(E/O) 및 광 신호를 다시 전기 신호로 래칭하는 광 수신(O/E) 변환 과정.
- **CPO(Co-Packaged Optics)**: ASIC과 광 엔진을 같은 기판·인터포저에 배치해 전기 I/O 거리를 줄이는 기술.

</details>

- 정의/개념: 전기 데이터를 광으로 변조해 광섬유로 전송하고 다시 전기로 복원하는 **광 인터커넥트**
- 배경/필요성: 대규모 AI 클러스터(GPU/NPU 어레이) 간 고속 직렬 전송 시 구리선 감쇠(Attenuation) 및 발열/전력 폭증 문제 극복 요구성

#### 한줄 요약

- 광전 변환과 광섬유 전송 및 전기 데이터 복원을 결합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WDM(Wavelength Division Multiplexing)**: 단일 광섬유에 여러 파장 채널을 결합해 병렬 전송하는 다중화 기술.
- **링크 버짓(Link Budget, $P_{\mathrm{rx}} = P_{\mathrm{tx}}-L_{\mathrm{total}}$)**: 광 송신기 출력($P_{\mathrm{tx}}$), 커넥터/광섬유 손실($L_{\mathrm{total}}$) 및 수신 감도($P_{\mathrm{sens}}$)를 종합 계산한 신호 여유(Margin) 지표.
- **EMI(Electromagnetic Interference) 내성**: 광섬유 전송 구간이 전자기 간섭의 영향을 적게 받는 특성.

</details>

- 전송 구간의 구리선 손실과 **EMI** 영향을 줄이는 광섬유 전송
- 단일 파이버에서 복수 파장을 병렬 전송하는 **WDM** 대역폭 확장
- 칩셋 간 거리 단축을 위한 **CPO(Co-Packaged Optics)** 패키징 기술 융합

$$
P_{\mathrm{rx}} = P_{\mathrm{tx}}-L_{\mathrm{total}},\qquad
M = P_{\mathrm{rx}}-P_{\mathrm{sens}}
$$

#### 한줄 요약

- WDM의 대역폭 이득과 광전 변환 전력·비용 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 칩 내부 병렬 전기 데이터를 고속 직렬 신호로 변환 및 원복하는 물리 계층 칩셋.
- **PIC/Modulator(Silicon Photonics)**: 전기 신호를 빛의 세기·위상으로 변조하는 광집적회로.
- **Mux/Demux**: **WDM** 다중 파장 빛을 결합(Mux) 및 수신측에서 분리(Demux)하는 필터 광학 소자.

</details>

```text
[SerDes] -- [광 송신부] -- [WDM 결합•분리기]
                                      |
                           [광섬유 경로] -- [광 수신부]
```

선의 의미: SerDes 전기 신호가 광 송신부(E/O), WDM Mux를 거쳐 광섬유 경로로 전송된 후 Demux 및 광 수신부(O/E)로 수용되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| SerDes | 병렬 데이터 직렬 변환 및 PAM4 고속 패킷 신호 인가 |
| 광 송신부(E/O) | Laser 광원 수용 및 **Silicon Photonics** 변조기 기반 E/O 변환 |
| WDM 결합•분리기 | 다중 파장 광 신호의 결합(**Mux**) 및 분리(**Demux**) |
| 광섬유 경로(Optical Fiber) | 링크 버짓 안에서 광 신호를 장거리 전송 |
| 광 수신부(O/E) | Photo Detector(PD) 및 TIA/LA 증폭기 기반 O/E 변환 |

#### 한줄 요약

- SerDes, 광 송신부, WDM 결합•분리기, 광섬유 경로, 광 수신부의 종단 링크 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PAM4(Pulse Amplitude Modulation 4)**: 4개 전압/광 신호 레벨을 통해 1개 심볼당 2비트를 전송하는 고속 광 변조 방식.

</details>

```text
[병렬 전기 데이터]
        │
        ▼
1. 직렬화•E/O 변조
        │
        ▼
2. WDM 파장 결합
        │
        ▼
3. 광섬유 전송
        │
        ▼
4. 파장 분리•O/E 복원
        │
        ▼
[병렬 수신 데이터]
```

### 동작 원리

1. 직렬화·E/O 변조: **SerDes**를 통한 직렬화 및 실리콘 포토닉스 **E/O 변조기(PAM4)** 구동.
2. WDM 파장 결합: **WDM Mux**를 활용한 복수 파장 광 신호의 단일 파이버 융합.
3. 광섬유 전송: 커넥터/파이버 손실을 수용하며 **링크 버짓** 이내로 광 패킷 수송.
4. 파장 분리·O/E 복원: **WDM Demux** 분리 및 Photo Detector 기반 **O/E 변환**과 SerDes 역직렬화 완결.

#### 한줄 요약

- 직렬화·E/O 변조와 WDM 파장 결합, 광섬유 전송, 파장 분리·O/E 복원을 순서대로 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Pluggable Transceiver**: QSFP, OSFP 등 기존 스위치 전면에 탈착하는 표준 착탈식 광 모듈.

</details>

| 비교 항목 | Pluggable Transceiver | CPO (Co-Packaged Optics) | 구리선 (Direct Attach Copper) |
|:---|:---|:---|:---|
| 전송 구조 | 스위치 전면 패널 포트 탈착 방식 | ASIC 및 광 엔진 단일 기판 인접 패키징 | 단순 구리 차동 선로 직결 |
| 전력 특성 | 긴 전기 호스트 경로와 모듈 DSP 비용 | 짧은 전기 경로와 광 엔진 열 관리 | 짧은 거리에서는 변환 없는 저비용 경로 |
| 전송 거리 | 광 모듈 종류에 따라 단거리·장거리 지원 | 채택 광 엔진과 파이버 규격에 따라 결정 | 속도·케이블 손실에 따라 짧은 거리 중심 |

#### 한줄 요약

- 구리 채널이 거리•속도 한계에 이르고 광전 변환을 포함한 비트당 에너지가 더 낮을 때 광 연결로 전환한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **파장 드리프트(Wavelength Drift)**: 온도 상승 시 레이저 다이오드(LD) 중심 파장이 변동하여 WDM 채널 분리 불량을 유발하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 레이저 발열에 따른 **파장 드리프트** 발생 | ELS(External Laser Source) 분리 장착 및 TEC 온도 제어 | 파장 신뢰성 확보 |
| 패키징 기판 내 광 파이버 정밀 정렬 난제 | 수동 정렬 구조와 능동 정렬 공정 검증 | 결합 손실 감소와 제조 수율 향상 |
| **CPO** 메인 ASIC 고장 시 광 모듈 동시 교체 비용 | ELS 외장화 및 착탈식 CPO 광 커넥터 수용 | 정비성(Maintainability) 확보 |

> 사례: 플러거블과 CPO의 종단 전력·열·정비 시간 비교

#### 한줄 요약

- 송수신 광세기와 삽입 손실을 측정해 링크 버짓을 보정한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **광 인터커넥트 선택 기준(Optical Interconnect Selection Criteria)**: 전송 대역폭, 전송 거리, 비트 당 에너지 효율(pJ/bit) 및 CPO 패키징 가능성에 따른 체계.

</details>

- 초단거리·저비용은 **구리**, 정비성은 **플러거블**, I/O 전력·밀도 한계는 **CPO** 선택

#### 한줄 요약

- 구리 한계와 종단 에너지 이득을 확인하고 정비성에 따라 플러거블·CPO를 선택한다.
