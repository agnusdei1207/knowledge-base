---
title: "디지털 변조 (Digital Modulation)"
date: "2026-06-30"
weight: 4
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 디지털 비트열을 아날로그 반송파(Carrier)의 진폭·주파수·위상에 실어 전송 가능한 신호로 변환하는 기술로, ASK·FSK·PSK·QAM 등이 대표적이다.

## Ⅱ. 구성요소 / 원리
- ASK(Amplitude Shift Keying): 반송파 진폭으로 0/1 구분, 잡음에 취약하나 구현 단순
- FSK(Frequency Shift Keying): 반송파 주파수 변화로 데이터 표현, 잡음에 강함
- PSK(Phase Shift Keying): 위상 변화로 표현(BPSK/QPSK), 진폭 일정으로 잡음 강건
- QAM(Quadrature Amplitude Modulation): 진폭+위상 동시 변조(16/64/256QAM), 고속·대용량
- 심볼당 비트수 = log2(M), M↑일수록 효율↑·잡음내성↓(높은 SNR 요구)

## Ⅲ. 흐름도 / 구조
```text
비트열 → [심볼 매핑] → [I/Q 변조] → [반송파 곱] → RF 송신
ASK: 진폭만 | FSK: 주파수 | PSK: 위상 | QAM: 진폭+위상(I/Q 평면)
 16QAM 성좌도: 4x4 = 16점 → 심볼당 4비트
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 디지털 데이터를 전송 매체 특성에 맞는 아날로그 신호로 변환 |
| 장점 | QAM은 단위 대역폭당 전송효율 높음, PSK/FSK는 잡음 강건성 우수 |
| 한계 | 고차 변조는 SNR·선형성 요구가 커지고 PAPR·간섭에 민감 |

## Ⅴ. 기술사적 적용
- Wi-Fi/LTE/5G는 채널 품질(CQI)에 따라 QPSK~256QAM 적응변조(AMC) 적용
- 광통신·고속 백홀은 다단 QAM과 코히어런트 검파로 스펙트럼 효율 극대화
- 저전력 IoT(LoRa, Zigbee)는 잡음 강건성을 위해 FSK/저차 변조 선택
