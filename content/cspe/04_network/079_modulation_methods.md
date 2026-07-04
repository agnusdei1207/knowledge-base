---
title: "변조 방식 — AM·FM·QAM·QPSK (Modulation Methods)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 79
---

# 📖 【암기용】 개념 완전 이해

> 목적: 변조 방식을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 정보를 반송파의 진폭·주파수·위상에 실어 전송 가능한 신호로 바꾸는 기술
- **왜 필요한가**: 원래 데이터 신호를 그대로 보내면 안테나 크기, 채널 대역, 다중화가 맞지 않는다. 변조는 신호를 채널 특성에 맞는 주파수 대역으로 옮기고, 심벌당 비트 수를 조절한다.
- **핵심 직관**: 같은 멜로디를 악기 소리의 크기, 음높이, 박자 위치를 바꿔 멀리 전달하는 것과 같다.

## 깊이 이해
- **배경·문제의식**: 통신 채널은 주파수 대역이 제한되고 잡음과 간섭이 존재한다. 변조는 정보를 반송파 파라미터에 매핑해 제한된 대역에서 목표 전송률과 BER을 맞춘다.
- **작동 원리**: AM은 진폭, FM은 주파수를 바꾼다. PSK는 위상, QAM은 진폭과 위상을 함께 사용한다. QPSK는 4개 위상으로 심벌당 2비트를 전송하고, 16-QAM은 4비트를 전송한다.
- **비유**: 신호등에서 색상만 쓰면 3가지 상태를 표현하지만, 색상과 깜박임 패턴을 함께 쓰면 더 많은 상태를 표현할 수 있다. QAM은 진폭과 위상을 함께 쓰는 방식이다.
- **구체 예시**: 64-QAM은 심벌당 log2(64)=6비트를 전송한다. SNR이 낮으면 constellation point 구분이 어려워져 16-QAM 또는 QPSK로 낮추는 link adaptation이 필요하다.
- **흔한 오해·주의점**: 고차 QAM은 항상 선택되는 방식이 아니다. 심벌당 비트 수가 증가하면 같은 잡음에서 심벌 간 거리가 줄어 BER이 커질 수 있다.

## 연결 개념
- Shannon Channel Capacity — 변조 차수가 넘을 수 없는 이론 한계
- 채널 코딩 — 변조 오류를 정정해 목표 BER 달성
- OFDM — 다수 부반송파에 QAM/QPSK 심벌을 실어 전송

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 변조는 반송파 파라미터, 심벌당 비트 수, SNR 요구, BER의 절충으로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 변조는 디지털/아날로그 정보를 반송파의 진폭, 주파수, 위상에 매핑해 채널을 통해 전송하는 신호 처리 기술이다.
> 2. **가치**: QPSK는 심벌당 2비트, 16-QAM은 4비트, 64-QAM은 6비트를 전송해 대역폭당 정보량을 조절한다.
> 3. **판단 포인트**: 변조 차수는 SNR, BER/BLER, 채널 코딩률, 이동성, 증폭기 선형성을 함께 고려해 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 변조 원리 이해 확인 | AM, FM, PSK, QAM, constellation | 이름 나열로 끝냄 |
| 디지털 변조 선택 판단 | QPSK, 16/64/256-QAM, bits/symbol | 고차 변조를 무조건 우위로 서술 |
| 링크 적응 설명 | SNR, BER, coding rate, MCS | Shannon 한계와 채널 코딩 누락 |

> 요약: 이 문제는 반송파 파라미터와 constellation을 통해 전송률과 오류율의 절충을 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 정보를 반송파에 싣는 방식
- 배경: 통신 채널은 대역폭과 잡음 조건이 정해져 있어 원 신호를 그대로 보내면 전송 거리와 다중화에 제약이 생긴다.
- 필요성: 변조는 주파수 이동, 다중화, 심벌당 비트 수 조절로 링크 요구사항을 만족시킨다.

---

## Ⅱ. 구조 및 구성요소

```text
Input Bits/Signal -> Mapper -> Carrier Amplitude/Frequency/Phase Change
-> Channel Transmission -> Demodulator -> Decision/Decoding
              +-> Constellation and MCS Table
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Carrier | 정보를 실을 기준 파형 | 주파수, 위상, 진폭 |
| Mapper | bit를 symbol로 변환 | QPSK 2bit, 16-QAM 4bit |
| Constellation | 심벌 위치 표현 | Euclidean distance가 BER에 영향 |
| Demodulator | 수신 신호를 심벌로 판정 | coherent/non-coherent 방식 |
| MCS | 변조와 코딩률 조합 | LTE/5G link adaptation |

> 요약: 변조 구조는 bit-to-symbol 매핑, 반송파 변환, 채널 통과, 복조 판정으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Bit Stream -> Symbol Mapping -> Carrier Modulation -> Channel
-> Synchronization -> Demodulation -> Symbol Decision
-> FEC Decoding -> BER/BLER Feedback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 bit를 심벌 그룹으로 묶음 | log2(M) bits/symbol |
| 2 | AM/FM/PSK/QAM 파라미터 변경 | constellation mapping |
| 3 | 채널 통과 중 잡음·페이딩 발생 | SNR, EVM 측정 |
| 4 | 수신기가 동기화 후 심벌 판정 | symbol error rate |
| 5 | FEC 복호와 MCS 조정 | BLER 10% 이하 목표 |

> 요약: 변조는 bit를 constellation 심벌로 바꾸고, 수신기는 SNR과 오류율에 따라 MCS를 조정한다.

---

## Ⅳ. 특징

| 구분 | AM/FM | QPSK | QAM |
|:---|:---|:---|:---|
| 조절 대상 | 진폭/주파수 | 위상 4상태 | 진폭+위상 다중 상태 |
| 정보량 | 아날로그 신호 중심 | 2bit/symbol | 16-QAM 4, 64-QAM 6, 256-QAM 8 |
| 잡음 민감도 | AM은 진폭 잡음 영향 | QAM보다 심벌 간 거리 큼 | 고차일수록 SNR 요구 증가 |
| 적용 | 방송, 음성 | 이동통신 제어/저SNR | Wi-Fi, LTE/5G data channel |

> 요약: QPSK는 낮은 SNR에서, 고차 QAM은 충분한 SNR과 선형성이 확보될 때 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 전송률 | QPSK | 64/256-QAM | SNR margin, EVM 기준 충족 |
| 오류율 | 고차 QAM 고정 | adaptive modulation | BLER 10% 이하 유지 |
| 운영/위험 | 최대 MCS 고정 | CQI 기반 MCS 변경 | 이동성, 간섭, 페이딩 |

> 요약: 변조 방식은 심벌당 비트 수보다 채널 상태에 따른 MCS 적응 능력으로 평가한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| BER 증가 | 고차 QAM constellation 간격 축소 | MCS 하향, coding rate 조정 | BER/BLER, EVM |
| 동기화 오류 | 주파수 offset, phase noise | carrier recovery, pilot symbol | CFO, phase error |
| 증폭기 왜곡 | QAM 진폭 변화와 PAPR | linear PA, DPD, back-off | ACLR, EVM |

> 요약: 변조 리스크는 고차화로 인한 오류율, 동기화, RF 선형성에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 오류율 | BLER 10% 이하, BER 목표 충족 | modem KPI, BER tester |
| 신호 품질 | EVM 표준 기준 이내 | vector signal analyzer |
| 링크 적응 | CQI-MCS 매핑 오류 0건 | scheduler log, throughput test |

> 요약: 변조 품질은 BER/BLER, EVM, CQI-MCS 매핑으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. SNR, EVM, 이동성 조건을 측정해 QPSK, 16-QAM, 64-QAM, 256-QAM의 MCS table을 단계적으로 적용함
2. 목표 BLER 10% 이하를 기준으로 coding rate와 HARQ를 결합하고, SNR 저하 시 MCS를 즉시 하향함
3. 고차 QAM 적용 구간은 PA linearity, DPD, pilot density, synchronization loop를 함께 검증함

**결론 (2줄):**
- 기술사 판단: 낮은 SNR·고이동성은 QPSK, 충분한 SNR·낮은 EVM은 64/256-QAM을 선택함
- 향후 방향: 5G/6G는 OFDM, massive MIMO, adaptive MCS를 결합해 채널 상태별 변조 차수를 동적으로 제어함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | bit-to-symbol, 반송파 변환, 복조 흐름 | AM/FM/QPSK/QAM 차이 |
| 요구사항 명시형 | "비교하시오", "설계하시오", "방안을 제시하시오" | SNR 기반 MCS 선택 절차 | BER, EVM, BLER, 선형성 지표 |

> 요약: 설명형은 변조 원리, 설계형은 SNR과 오류 지표 기반 MCS 선택을 중심으로 작성한다.
