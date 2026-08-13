---
sidebar:
  order: 66
  label: "066. 변조 방식 : AM•FM•QAM•QPSK (Modulation Methods)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "변조 방식 : AM•FM•QAM•QPSK (Modulation Methods)"
date: "2026-08-13T16:49:00+09:00"
tags:
  - "notes-network"
weight: 66
extra:
  question_no: "066"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "비교형: 변조 선택의 대역폭•잡음 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **변조(Modulation)**: 기저대역 정보 신호(디지털 비트/아날로그 음성)를 고주파 반송파(Carrier Wave)의 진폭, 주파수, 위상 특성에 실어 물리 전송 채널로 보낼 파형으로 변환하는 과정이다.
- **기저대역(Baseband)**: 변조되기 직전의 유효 정보 신호가 가지는 고유한 변환 주파수 영역($0 \sim f_m$ Hz)이다.
- **대역통과 채널(Bandpass Channel)**: 특정 중심 주파수($f_c$) 부근의 전파 주파수 대역만을 통과시키는 유선/무선 물리 전송 채널 환경이다.

</details>

- 정의/개념: **변조**(Modulation)는 송신 측에서 **기저대역**(Baseband) 데이터 신호를 고주파 반송파의 진폭, 주파수, 위상 파라미터로 매핑하여 무선/유선 **대역통과 채널**(Bandpass Channel) 상에서 감쇄 없이 전달될 수 있는 대역통과 신호(Passband Signal)로 변환하는 물리계층 신호 처리 기술이다.
- 배경/필요성: 낮은 주파수의 기저대역 신호를 무선 공간에 직접 방사하기 위해서는 파장($\lambda=c/f$)에 비례하여 거대한 안테나가 필요하므로, 고주파 반송파에 신호를 얹어 안테나 크기를 현실화하고 다중화(Multiplexing) 전송을 구현하기 위해 필수적이다.

#### 한줄 요약

- 정보 비트열을 고주파 반송파의 진폭, 주파수, 위상 상태에 매핑하여 안테나로 송출하는 변조 처리 기술 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **심벌(Symbol)**: 단위 시간(Symbol Time, $T_s$) 동안 전송되는 진폭과 위상의 단일 전파 파형 상태로, 변조 차수($M$)에 따라 $\log_2 M$ 개의 비트를 내포한다.
- **성상도(Constellation Diagram)**: 동상(In-phase, I) 성분과 직교(Quadrature, Q) 성분의 2차원 복소 평면상에 디지털 변조 심벌들의 좌표를 가시화한 신호 배치도이다.
- **신호대잡음비(Signal-to-Noise Ratio, SNR)**: 수신된 신호 전력 대비 잡음 전력의 비율로, 높은 변조 차수(High-order QAM)를 복호하기 위한 필수 전제 조건이다.
- **직교 진폭 변조(Quadrature Amplitude Modulation, QAM)**: 서로 90도 위상차를 갖는 두 개의 직교 반송파의 진폭을 동시에 다치(Multi-level) 조절하여 high-density 비트 전송을 구현하는 디지털 변조 방식이다.
- **첨두전력대평균전력비(Peak-to-Average Power Ratio, PAPR)**: 신호의 순간 최대 전력 대비 평균 전력의 비율로, 고차 QAM 및 OFDM 신호에서 송신 전력 증폭기(PA)의 비선형 왜곡을 유발하는 지표이다.

</details>

- 변조 차수($M=2, 4, 16, 64, 256, 1024$)가 증가함에 따라 단일 **심벌** 당 전송 비트 수($m = \log_2 M$)가 늘어 대역폭 효율성(bps/Hz)이 급증한다.
- 2차원 **성상도**(Constellation) 상에서 심벌 간 거리가 좁아질수록 동일한 **SNR** 조건에서 잡음 훼손에 의한 비트 판정 오류율(BER) 손실 리스크가 커진다.
- 256-QAM 및 1024-**QAM** 등 고차 변조는 **PAPR** 상승으로 인해 송신 전력 증폭기(PA)의 Linear Region 운용 요구 조건이 까다로워진다.

#### 한줄 요약

- 변조 차수 확장을 통한 대역폭 효율 극대화와 성상도 심벌 간격 마진 확보 간의 Trade-off 수용 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **무선 주파수부(Radio Frequency, RF Front-End)**: 기저대역 디지털 심벌을 아날로그 고주파 파형으로 상향 변환(Up-conversion) 및 전력 증폭(PA)하거나, 수신 파형을 LNA로 증폭 및 하향 변환(Down-conversion)하는 믹서/증폭기 하드웨어이다.
- **파일럿(Pilot Signal / Symbol)**: 무선 채널의 위상 위곡 및 위상 잡음(Phase Noise)을 복원하기 위해 송수신 간 미리 약속된 기지의 레퍼런스 신호이다.
- **변조·부호화 조합(Modulation and Coding Scheme, MCS)**: 무선 링크 SNR 환경에 맞추어 변조 차수(QPSK, 16QAM, 64QAM, 256QAM)와 FEC 부호율(1/2, 2/3, 3/4, 5/6)을 조합 결정하는 지능형 파라미터 지표이다.

</details>

- **MCS** 선택 알고리즘에 의해 입력 비트를 심벌 좌표로 매핑하고, **RF** 트랜시버를 거쳐 안테나로 발사되며, 수신 측은 **파일럿** 신호를 이용해 채널 위상 왜곡을 정밀 보정한다.

```text
변조 시스템 구성요소
├─ 심벌 매퍼(Symbol Mapper)
├─ 송신 RF부(Tx RF Front-End)
├─ 무선 채널(Wireless Channel)
├─ 수신 동기·등화부(Sync & Equalizer)
└─ 심벌 디매퍼(Symbol Demapper)
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **심벌 매퍼 (Symbol Mapper)** | 비트 묶음을 성상도 I/Q 좌표상의 특정 심벌 전압 레벨로 변환 |
| **송신 RF부 (Tx RF Front-End)** | I/Q 기저대역 신호를 직교 믹서로 고주파 반송파($f_c$)에 상향 변환 후 전력 증폭 |
| **무선 채널 (Wireless Channel)** | Rayleigh/Rician Fading, multipath interference, AWGN 잡음 부가 |
| **수신 동기·등화부 (Sync & Equalizer)** | Carrier Sync, Timing Sync 및 파일럿 기반 채널 왜곡 보정(Zero-Forcing/MMSE) |
| **심벌 디매퍼 (Symbol Demapper)** | 등화된 수신 I/Q 좌표와 성상점 간 유클리드 거리를 산출하여 비트 가능도(LLR) 계산 |

#### 한줄 요약

- I/Q 심벌 매핑과 RF 반송파 상하향 변환, 파일럿 기반 동기화 및 심벌 디매핑 연산이 유기적으로 연계된 송수신 구조 적용.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **동기화(Synchronization)**: 수신 RF 신호에서 반송파의 위상/주파수 오프셋 및 심벌 타이밍 시점을 정확히 맞추는 처리 프로세스이다.
- **등화(Equalization)**: 무선 다중경로(Multi-path) 채널로 인해 왜곡된 신호의 심벌 간 간섭(ISI)을 억제하고 원래의 성상도 위치로 복원하는 신호 보정 기술이다.
- **복조(Demodulation)**: 수신된 대역통과 파형을 기저대역 복소 신호로 전환하여 송신 성상점에 가장 가까운 심벌을 디코딩하는 과정이다.
- **오류 벡터 크기(Error Vector Magnitude, EVM)**: 실제 수신된 심벌 좌표와 이상적인 기준 성상점 간의 벡터 거리를 측정하여 변조 신호의 정밀도 및 왜곡 상태를 나타내는 지표(unit: % 또는 dB)이다.
- **채널 품질 보고(CQI Reporting)**: 수신 단말이 채널 SNR, EVM, BLER을 측정하여 최적의 MCS를 기지국에 알려주는 단계이다.
- **변조·부호율 설정(MCS Allocation)**: 기지국이 수신된 CQI를 기반으로 적절한 QPSK/QAM 변조 차수를 확정하는 단계이다.
- **변조 신호 전송(Modulated Signal Transmission)**: 매핑된 심벌에 반송파를 실어 안테나로 반출하는 단계이다.
- **왜곡 수신 신호 전달(Distorted Signal Delivery)**: 채널 왜곡 및 잡음이 추가된 파형을 수신기 RF로 주입하는 단계이다.
- **동기·등화·심벌 판정(Sync, Equalization & Symbol Decision)**: 위상 보정 및 등화를 거쳐 최종 비트열을 복원 판정하는 단계이다.

</details>

```text
1. 채널 품질 보고
      │
      ▼
2. 변조·부호율 설정
      │
      ▼
3. 변조 신호 전송
      │
      ▼
4. 왜곡 수신 신호 전달
      │
      ▼
5. 동기·등화·심벌 판정
```

### 동작 원리

1. **채널 품질 보고**: 수신 단말이 무선 신호의 **SNR** 및 **EVM**을 정밀 측정하여 기지국으로 피드백한다.
2. **변조·부호율 설정**: 링크 제어기가 목표 BLER을 충족하는 **MCS** 파라미터를 선정한다.
3. **변조 신호 전송**: 선택된 **QPSK/QAM** 성상도 좌표로 데이터를 변조하여 무선 공간으로 송출한다.
4. **왜곡 수신 신호 전달**: 수신 측은 multipath fading 및 잡음으로 성상점 좌표가 번진 수신 파형을 받는다.
5. **동기·등화·심벌 판정**: **동기화**와 **등화** 후 연판정 **복조** 결과를 채널 복호기로 전달한다.

#### 한줄 요약

- CQI 기반 MCS 동적 할당과 송신 성상 매핑, 수신 등화 및 EVM 신호 복조 프로세스 준수.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **진폭 변조(Amplitude Modulation, AM)**: 기저대역 신호의 전압 변화에 따라 반송파의 진폭 높낮이만을 변화시키는 아날로그 변조 방식이다.
- **주파수 변조(Frequency Modulation, FM)**: 기저대역 신호의 전압 변화에 따라 반송파의 편위 주파수를 유동적으로 순시 변화시키는 아날로그 변조 방식이다.
- **직교 위상 편이 변조(Quadrature Phase Shift Keying, QPSK)**: 반송파의 위상을 90도 간격(4개 위상: 45°, 135°, 225°, 315°)으로 분할하여 심벌당 2비트($2^2=4$)를 전송하는 디지털 변조 기법이다.

</details>

- **AM/FM**은 아날로그 데이터 전송에 특화되어 진폭 및 주파수를 연속 변화시키며, **QPSK/QAM**은 디지털 이진 데이터를 복소 성상 좌표에 불연속적으로 대응시킨다.

| 비교 항목 | AM (Amplitude Mod.) | FM (Frequency Mod.) | QPSK (Phase Shift) | QAM (Quad. Amplitude) |
|:---|:---|:---|:---|:---|
| **변조 대상 파라미터** | 반송파 진폭(Envelope) | 반송파 순시 주파수 | 반송파 4개 위상각 | 직교 반송파 진폭 + 위상 |
| **심벌당 전송 비트** | N/A (아날로그) | N/A (아날로그) | 심벌당 2 비트 ($M=4$) | 심벌당 4~10 비트 ($M=16\sim 1024$) |
| **잡음 및 왜곡 내성** | 진폭 잡음에 취약 | 진폭 잡음에 상대적으로 강함 | 고차 QAM보다 낮은 SNR에 강함 | 차수가 높을수록 잡음에 민감 |
| **대역폭 효율성** | 변조 지수와 대역 제한에 좌우 | 주파수 편이에 따라 대역 증가 | 심벌당 2비트 | 심벌당 $\log_2 M$비트 |
| **주요 응용 분야** | 라디오 방송 (AM), 항공 통신 | FM 라디오, 아날로그 무전기 | 3G/4G/5G 제어 채널, 위성 통신 | Wi-Fi 6/7, 5G NR 고속 데이터 채널 |

> 요약: 높은 잡음 환경 및 제어 신호의 안정적 전달에는 **QPSK**, 고속 대용량 데이터 전송에는 **QAM**(16~1024QAM), 아날로그 음성 전송에는 **FM** 기법을 선택 채택한다.

#### 한줄 요약

- 아날로그 AM/FM과 디지털 QPSK/QAM 변조 간의 대역폭 효율성, 잡음 내성 및 성상 특성 비교 모델 수용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **출력 백오프(Output Back-off, OBO)**: 고차 QAM 신호의 높은 PAPR로 인한 전력 증폭기(PA) 비선형 왜곡 및 옆 채널 간섭(ACLR)을 막기 위해 앰프 동작 지점을 최고 출력 대비 수 dB 낮추어 운용하는 마진 기술이다.
- **적응 변조·부호화(Adaptive Modulation and Coding, AMC)**: 무선 채널의 Time-varying 특성에 대응하여 CQI 지표에 따라 QPSK부터 1024-QAM까지 변조 차수를 실시간 동적 전환하는 기술이다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **고차 QAM BER 급증** | 무선 페이딩으로 SNR 저하 시 성상점 유클리드 거리 붕괴 | 실시간 **AMC** 기법 연동을 통해 순간적으로 QPSK/16QAM으로 하향 | 무선 통신 끊김 예방 및 안정적 주파수 효율 유지 |
| **PA 비선형 신호 왜곡** | 고차 QAM 신호의 높은 **PAPR**로 인해 전력 증폭기 saturation | **출력 백오프**(OBO) 설정 및 디지털 전왜곡(DPD) 앰프 기술 도입 | **EVM** 품질 개선 및 이웃 채널 누설 전력(ACLR) 차단 |
| **위상 잡음 및 왜곡** | 발진기(Oscillator) 불안정으로 성상점 위상 회전 발생 | **파일럿** 심벌 밀도 증가 및 위상 동기화(PLL) 루프 제어 강화 | 위상 오차 수용 및 안정적인 고차 QAM 디매핑 수행 |
| **전력 소모 증가** | 1024-QAM 적용 시 높은 SNR 요구로 송신 전력 증대 | 빔포밍(Beamforming) 연동을 통한 국소 영역 신호 집속 | 송신 전력 효율 최적화 및 단말 배터리 소모 절감 |

#### 한줄 요약

- AMC 기반 변조 차수 유동 전환, PA 백오프(OBO) 설정 및 DPD 보정을 통한 변조 품질 관리 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **효율·강인성 절충(Efficiency-Robustness Trade-off)**: 변조 차수를 올리면 전송속도(bps/Hz)는 증가하나 요구 SNR 기준이 높아져 잡음 내성은 약해지는 물리계층 관계이다.

</details>

- 낮은 SNR·제어 신호는 **QPSK**, 고품질 채널은 **고차 QAM** 선택.

#### 한줄 요약

- 변조 차수별 대역폭 효율성과 EVM/SNR 지표 분석 및 AMC 적응형 기술을 융합한 차세대 변조 아키텍처 구현 필수.
