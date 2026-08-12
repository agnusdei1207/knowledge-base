---
sidebar:
  order: 65
  label: "065. 채널 용량 : 섀넌 한계 (Shannon Channel Capacity)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "채널 용량 : 섀넌 한계 (Shannon Channel Capacity)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 65
extra:
  question_no: "065"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "설명•계산형: 135회 Shannon 용량 직접 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **채널 용량(Channel Capacity)**: 주어진 주파수 대역폭과 신호대잡음비(SNR) 조건 하에서 전송 오류율을 임의의 0에 가깝게 유지하면서 전달할 수 있는 이론적 최고 정보 전송률($C$, unit: bps)이다.
- **섀넌 한계(Shannon Limit / Shannon Capacity Theorem)**: 클로드 섀넌이 정립한 공식($C = B \log_2 (1 + S/N)$)으로, 백색 가우시안 잡음 채널에서 물리적으로 도달 가능한 최대 전송 한계선이다.
- **가산 백색 가우스 잡음(Additive White Gaussian Noise, AWGN)**: 전 주파수 대역에 걸쳐 전력 스펙트럼 밀도가 일정하고 진폭이 가우시안 정규 분포를 따르는 가장 기본적이고 보편적인 물리 채널 잡음 모델이다.

</details>

- 정의/개념: **채널 용량**(Channel Capacity)은 대역폭($B$)과 신호대잡음비($S/N$)가 주어진 **AWGN** 무선/유선 채널 환경에서, 수신 측 복호 오류를 0으로 만들 수 있는 정보 전송 한계선인 **섀넌 한계**(Shannon Limit)를 산출하는 정보 이론의 근간 수식 체계이다.
- 배경/필요성: 무선 물리 계층 설계 시 물리적 한계를 초과하는 불가능한 대역폭/전력 목표 설정을 방지하고, 변조 방식(QAM 등) 및 FEC 부호율 조합(MCS)의 수용 한계를 통계적으로 검증하기 위해 필수적으로 활용된다.

#### 한줄 요약

- 주파수 대역폭과 신호대잡음비의 물리적 한계치인 섀넌 정리를 통해 무선 채널의 최대 전송 용량을 산출하는 채널 용량 분석 체계 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **대역폭(Bandwidth)**: 신호 전송에 할당된 점유 주파수 스펙트럼 폭($B$, unit: Hz)으로, 채널 용량 $C$에 직접적인 비례 관계(Linearity)를 형성한다.
- **신호대잡음비(Signal-to-Noise Ratio, SNR)**: 수신된 유효 신호 전력($S$) 대비 무선 대역 내 누적 잡음 전력($N$)의 선형 전력 비율($S/N$)이다.
- **로그 관계(Logarithmic Relationship)**: SNR 증가에 따른 채널 용량 수용 증가분이 $\log_2$ 함수에 의해 체감되는(Diminishing Returns) 한계효용 특성이다.
- **메가헤르츠(Megahertz, MHz)**: 1초당 $10^6$회 진동하는 주파수의 대역폭 측정 단위이다.
- **데시벨(Decibel, dB)**: 신호대잡음비 전력 비율을 상용 로그로 변환($10 \log_{10} (S/N)$)하여 표현하는 상대 수치 단위이다.

</details>

![대역폭과 신호대잡음비에 따른 Shannon 이론 채널 용량](/study/diagrams/shannon-capacity.svg)

> 파란 1MHz와 붉은 2MHz 선은 대역폭을 두 배로 하면 용량도 두 배가 되지만 SNR 증가는 로그 형태로 용량을 높이는 이론 상한이며, 실제 변조•부호화 처리량은 이보다 낮다.

- 데이터 전송률 $R$이 **채널 용량** $C$보다 작을 경우($R < C$), 순방향 오류 정정(FEC)을 통해 오류율을 0에 가깝게 낮출 수 있다.
- **대역폭**($B$)은 용량에 직관적 비례(Linear) 관계로 기여하나, **신호대잡음비**($S/N$)는 비선형적 **로그 관계**($\log_2$)를 가져 수신 전력을 높여도 대역폭 확장 대비 이득 효율이 둔화된다.
- 대역폭 단위인 **MHz**와 데시벨 수치 **dB**를 수식 연산 주입 시 반드시 Hz 및 선형 전력비(Linear Ratio)로 변환해 연산해야 한다.

#### 한줄 요약

- 대역폭 비례성과 SNR 로그 둔화 특성을 명확히 반영하여 상한선 미만에서 오류율 0를 지향하는 물리계층 설계 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **수식 기호 읽기와 역할(Formula Notation and Symbols)**: $C=B \log_2 (1 + S/N)$ 수식에서 $C$는 Capacity(bps), $B$는 Bandwidth(Hz), $S$는 Signal Power(Watt), $N$은 Noise Power(Watt)를 각각 규정한다.

</details>

- **수식 기호 읽기와 역할**을 분석하면, $B$ 확장은 선형 가속을 이끌고, $S/N$ 증대는 로그 스케일로 감쇄하며, 총 잡음 전력 $N = N_0 \times B$ ($N_0$: 잡음 전력 스펙트럼 밀도) 관계를 가진다.

```text
섀넌 채널 용량 수식 아키텍처 (Shannon Capacity Formula)
C = B × log₂(1 + S/N)   [bps]
├─ 대역폭 B (Bandwidth, Hz) : 선형 비례 관계 (Linear Impact)
└─ 신호대잡음비 S/N (Linear SNR) : 로그 비례 관계 (Logarithmic Impact)
   ├─ 수신 신호 전력 S (Signal Power, Watts)
   └─ 대역 내 잡음 전력 N (Noise Power = N₀ × B, Watts)
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **대역폭 $B$ (Bandwidth)** | 채널이 점유하는 신호 전송 영역 주파수 폭 (Hz 단위 주입 필수) |
| **신호 전력 $S$ (Signal Power)** | 안테나 수신 프론트엔드에 도달한 유효 기저대역 전력 (Watts) |
| **잡음 전력 $N$ (Noise Power)** | 열잡음 밀도($N_0$)와 대역폭($B$)의 곱으로 결정되는 통계적 AWGN 전력 |
| **선형 SNR ($S/N$)** | $dB$ 수치를 선형 배수로 치환한 전력비 ($S/N = 10^{(SNR_{dB}/10)}$) |
| **채널 용량 $C$ (Capacity)** | 주어진 물리 환경에서 이질적 부호화로 다다를 수 있는 미시적 최대 비트 전송률 (bps) |

#### 한줄 요약

- $C = B \log_2(1+S/N)$ 방정식 구조 내 $B$와 선형 SNR $S/N$ 배수 치환 연산 아키텍처 적용.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **구현 격차(Implementation Gap)**: 유한한 블록 길이 및 실제 FEC 부호 복잡도 한계로 인해 이론적 섀넌 한계 $C$ 대비 요구되는 추가 SNR 손실값(약 1~3dB 간격)이다.
- **타당성 여유(Feasibility Margin)**: 무선 신호의 이동성 페이딩 및 섀도잉 현상을 대비하여 목표 전송률 전면에 미리 확보해두는 Link Budget 안전 여유분이다.
- **블록 오류율(Block Error Rate, BLER)**: 전송된 데이터 패킷 블록 중 복호에 실패한 비율로 real-time 무선 스케줄링 시 target BLER(보통 10% 또는 1%)을 유지한다.
- **$B$·$S$·$N$ 측정값(Measured $B$, $S$, $N$ Values)**: 스펙트럼 분석기 및 무선 단말 지표로 수집한 대역폭, 수신 신호, 열잡음 전력 수치이다.
- **$S/N$ 선형비 변환(Linear SNR Conversion)**: 측정된 $SNR_{dB}$ 값을 상용로그 역연산($10^{dB/10}$)으로 변환하는 연산 단계이다.
- **섀넌 용량 결과(Shannon Capacity Calculation)**: 수식 산출을 통해 이론 최대 물리계층 전송률을 계산하는 단계이다.
- **목표 전송률 후보(Target Bitrate Candidate)**: 이론 용량에서 파손 마진과 MCS 테이블 맵핑 손실을 차감한 실제 전송 목표 속도이다.
- **운용 전송률 확정(Operational Bitrate Confirmation)**: 목표 BLER 조건과 프로토콜 헤더 오버헤드를 검증하여 가동 속도를 확정하는 단계이다.

</details>

```text
현장 무선 환경 측정 (RF Field Measurement)
      │
      ▼
1. B, S, N 물리 측정값 수집 (RF Spectrum & Noise Measurement)
      │
      ▼
2. SNR(dB) 내 선형 전력비(S/N) 변환 (dB to Linear Conversion)
      │
      ▼
3. Shannon 이론 채널 용량 산출 (C = B * log2(1 + S/N))
      │
      ▼
4. Implementation Gap & Link Margin 차감 (Gap & Margin Subtraction)
      │
      ▼
5. Target BLER 검증 및 실제 운용 전송률 확정 (Operational Bitrate Allocation)
```

### 동작 원리

1. **$B$·$S$·$N$ 측정값**: 파티션 대역폭 $B$와 안테나 수신 전력 $S$, 잡음 전력 $N$을 정밀 수집한다.
2. **$S/N$ 선형비 변환**: 데시벨 단위로 측정된 $SNR_{dB}$ 수치를 섀넌 방정식 연산에 맞게 **선형비**로 전환한다.
3. **섀넌 용량 결과**: $C = B \log_2(1+S/N)$ 공식으로 이론상 100% 한계 용량을 산출한다.
4. **목표 전송률 후보**: 산출된 이론치 $C$에 실무 **구현 격차**(Implementation Gap, 약 1.5~2dB)와 MCS 한계를 차감한다.
5. **운용 전송률 확정**: **BLER** 타겟 수치 및 **타당성 여유**를 통합하여 실제 시스템 운영 속도를 확정한다.

#### 한줄 요약

- RF 물리량 수집과 선형비 변환, 섀넌 계산 및 Implementation Gap 차감을 거치는 링크 용량 확정 프로세스 준수.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **대역폭 증대(Bandwidth Expansion)**: 주파수 반송파 묶음(Carrier Aggregation) 및 초고주파(mmWave) 대역을 추가 확보하여 전송 용량을 선형적으로 대폭 늘리는 접근법이다.
- **SNR 증대(SNR Enhancement)**: 송신 빔포밍, 출률 증대 및 중계기 설치를 통해 수신 신호 품질 $S/N$을 높여 용량을 로그 곡선으로 증대시키는 방식이다.

</details>

- **대역폭 증대**는 주파수 할당 비용이 크지만 용량을 즉각 선형 비례로 확장시켜 효과가 가장 확실하다.
- **SNR 증대**는 송신 전력을 극적으로 올려도 $\log_2$ 함수에 갇혀 한계효용(Diminishing Return)에 직면하므로 전력 증대만으로는 용량 확장에 한계가 존재한다.

| 비교 항목 | 대역폭 증대 (Bandwidth Expansion) | SNR 증대 (SNR Enhancement) |
|:---|:---|:---|
| **용량 기여 특성** | **선형적 증대** ($C \propto B$) | **로그적 둔화 증대** ($C \propto \log_2(SNR)$) |
| **주요 기술 수단** | 주파수 집성(CA), mmWave 대역 개척, 대역 폭 확충 | 빔포밍(Beamforming), MIMO 안테나 이득, 전력 증폭 |
| **투자 효율성** | 추가 대역폭 확보 시 투자 대비 용량 증가 효과 매우 명확 | SNR 3dB(2배) 증가 시 용량 증가폭은 소폭에 그침 (로그 한계) |
| **실무적 한계** | 주파수 자원 고갈 및 광대역 안테나 RF 복잡도 증가 | 송신 출력 전력 규제(RF Safety) 및 타 셀 간섭(Interference) 증대 |

> 요약: 무선망 설계 시 전력 증대(SNR)는 한계효용에 부딪히므로, 대규모 데이터 처리량 향상에는 **대역폭 증대**(CA, Wideband)와 **MIMO 공간 다중화**를 핵심축으로 채택한다.

#### 한줄 요약

- 용량에 선형 영향을 미치는 대역폭 증대 기술과 로그 한계에 부딪히는 SNR 증대 기술 간의 특성 비교 모델 수용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **스펙트럼 효율(Spectral Efficiency)**: 단위 대역폭 1Hz 당 전송 가능한 비트 수(unit: bps/Hz)로, 무선 주파수 자원의 사용 효율성을 평가하는 지표이다.
- **굿풋(Goodput)**: L1 물리 계층 비트 전송률이 아닌, L7 애플리케이션 수신 측에 최종적으로 도달한 유효 순수 데이터 전송 속도이다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **실효 속도 과다 추정** | 섀넌 용량 $C$를 실제 유효 데이터 속도로 잘못 오인 설계 | **스펙트럼 효율** 반영 및 L2~L7 프로토콜 헤더 차감 연산 | 현실적인 실효 전송률 수용 및 망 용량 오류 방지 |
| **전력 투입 효율 저하** | SNR 증대만을 위해 무리하게 송신 출력 amplifier 강도를 증폭 | 대역폭 확충(CA) 및 Massive MIMO 공간 다중화로 전환 | power efficiency 최적화 및 셀 간 간섭 억제 |
| **대역폭 확장 잡음 비례** | 대역폭 $B$를 늘림에 따라 전체 잡음 전력 $N = N_0 \times B$도 동반 상승 | 수신 필터링 최적화 및 높은 신호 강도 구간 위주 광대역 배정 | 잡음 증가로 인한 SNR 저하 최소화 및 유효 용량 확보 |
| **이동성 페이딩 속도 저하** | 무선 단말 이동 시 SNR 급락으로 인한 물리계층 패킷 드랍 | 실시간 적응형 변복조(AMC) 및 **굿풋** 기반 MCS 갱신 | 모빌리티 채널 변동 시 지속적인 서비스 연속성 유지 |

#### 한줄 요약

- Implementation Gap 차감, 스펙트럼 효율 기반 헤더 산정, AMC 연동을 통한 실무 무선 링크 수용성 확보 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **프로토콜 오버헤드(Protocol Overhead)**: Ethernet, IP, TCP, RLC, MAC 등 각 계층 헤더 및 제어 프레임 소모로 발생하는 비유효 데이터 비율이다.
- **실제 굿풋(Actual Goodput)**: 재전송, 손실, 헤더 오버헤드가 제거되고 사용자가 응용 프로그램에서 체감하는 실제 유속 체감값이다.

</details>

- 네트워크 설계 시 **섀넌 한계**를 통해 한계 물리 용량을 산정하고, **프로토콜 오버헤드** 및 Implementation Gap을 정밀 제외하여 **실제 굿풋** 체감 성능을 달성하는 무선 네트워크 최적화 체계 적용.

#### 한줄 요약

- Shannon 이론 한계치 계산과 전력-대역폭 Trade-off 및 헤더 손실을 고려한 차세대 무선 통신망 용량 설계 체계 구축.
