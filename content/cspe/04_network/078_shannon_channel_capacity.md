---
title: "채널 용량 — 섀넌 한계 (Shannon Channel Capacity)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 78
---

# 📖 【암기용】 개념 완전 이해

> 목적: 채널 용량과 섀넌 한계를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 잡음이 있는 채널에서 임의로 낮은 오류율로 보낼 수 있는 최대 정보 전송률
- **왜 필요한가**: 대역폭을 늘리거나 송신 전력을 키우면 전송률은 증가하지만 무한히 늘어나지 않는다. Shannon은 대역폭 B와 신호대잡음비 S/N으로 이론 한계를 제시했다.
- **핵심 직관**: 도로 폭(B)과 차량 구분 선명도(S/N)가 정해지면, 사고 없이 지나갈 수 있는 차량 수에도 한계가 있다.

## 깊이 이해
- **배경·문제의식**: 통신 시스템은 변조, 코딩, 안테나를 개선해도 채널이 가진 물리 한계를 넘을 수 없다. Shannon-Hartley 정리는 AWGN 채널에서 용량을 `C = B log2(1+S/N)`로 표현한다.
- **작동 원리**: 대역폭 B가 커지면 더 많은 심벌을 보낼 수 있고, S/N이 커지면 심벌 간 구분이 쉬워진다. 그러나 S/N 증가는 로그 함수로 반영되어 전력 증가 대비 용량 증가가 둔화된다.
- **비유**: 강의실에서 더 많은 사람이 동시에 말하려면 방 크기와 목소리 선명도가 필요하지만, 소리만 키우면 울림과 간섭 때문에 전달 가능한 정보는 제한된다.
- **구체 예시**: B=10MHz, SNR=20dB이면 S/N=100이고 C=10M log2(101)로 약 66.6Mbps이다. 이 값은 해당 조건에서 오류 없는 통신률의 이론 상한이다.
- **흔한 오해·주의점**: 채널 용량은 실제 처리량이 아니다. 프로토콜 헤더, 코딩 오버헤드, 재전송, 간섭, 구현 손실을 빼면 실제 처리량은 용량보다 낮다.

## 연결 개념
- 채널 코딩 — 섀넌 한계에 접근하기 위한 오류 정정 기술
- 변조 방식 — S/N과 대역폭을 심벌 전송률로 변환
- MIMO — 공간 스트림을 활용해 유효 채널 용량 확장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Shannon 식, B와 S/N의 영향, 실제 처리량과 이론 한계 차이를 명확히 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Shannon Channel Capacity는 잡음 채널에서 오류율을 임의로 낮게 유지하며 전송 가능한 최대 정보율이다.
> 2. **가치**: `C = B log2(1+S/N)`로 대역폭, 전력, 잡음, 코딩·변조 설계의 상한선을 제공한다.
> 3. **판단 포인트**: 용량은 이론 상한이며 실제 throughput은 coding overhead, MAC overhead, retransmission, implementation loss를 제외해 평가한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 정보이론 기본 이해 확인 | C=B log2(1+S/N), B, SNR, AWGN | 공식 없이 개념만 설명 |
| 시스템 설계 판단 | 대역폭 확장 vs 전력 증가 로그 효과 | 전력 증가가 선형 용량 증가로 착각 |
| 현실 적용 한계 | Shannon limit, coding gap, protocol overhead | 이론 용량과 실제 처리량 동일시 |

> 요약: 이 문제는 채널 용량 공식을 기반으로 무선·유선 링크 설계의 상한과 구현 손실을 구분하는 답안이 필요하다.

---

## Ⅰ. 개요 및 필요성

채널 용량은 잡음 채널의 최대 정보 전송률이다. 모든 통신 시스템은 대역폭, 전력, 잡음 조건에 의해 전송 한계를 가진다. Shannon 식은 변조·코딩·MIMO 설계가 넘을 수 없는 기준선을 제시해 링크 예산과 성능 평가의 기준이 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Information Source -> Encoder/Modulator -> Channel Bandwidth B and Noise N
-> Receiver Demodulator/Decoder -> Achievable Rate R
-> Compare with Capacity C
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Bandwidth B | 주파수 자원 폭 | Hz 단위, 용량에 선형 반영 |
| Signal Power S | 수신 신호 전력 | link budget, path loss 영향 |
| Noise Power N | 열잡음·간섭 | S/N 또는 SNR dB 사용 |
| Capacity C | 이론 최대 정보율 | bps, AWGN 기준 C=B log2(1+S/N) |

> 요약: 채널 용량은 대역폭과 신호대잡음비가 결정하며, 실제 전송률 R은 C 이하에서 설계된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Measure Bandwidth B -> Measure SNR dB -> Convert S/N Linear
-> Compute C = B log2(1+S/N)
-> Select Modulation/Coding Rate -> Validate Throughput and BER
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 채널 대역폭 B 확인 | licensed/unlicensed bandwidth |
| 2 | SNR dB를 선형 S/N으로 변환 | S/N = 10^(SNRdB/10) |
| 3 | Shannon-Hartley 식으로 C 산출 | bps 단위 계산 |
| 4 | MCS와 coding rate 선택 | R < C, BER 목표 충족 |
| 5 | 실제 처리량과 gap 분석 | throughput/C ratio |

> 요약: 용량 산정은 B와 SNR 측정, 선형 변환, 공식 계산, MCS 선택, 실제 처리량 검증 순서로 수행한다.

---

## Ⅳ. 특징

| 구분 | 대역폭 증가 | SNR 증가 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 용량 영향 | B에 선형 비례 | log2(1+S/N)로 증가 | B 2배는 C 2배 근접 |
| 비용 | 주파수 자원 필요 | 송신전력·안테나 이득 필요 | 규제 전력 한계 |
| 한계 | 대역 확보 제약 | 로그 증가로 수익 감소 | 3dB 증가는 S/N 2배 |
| 적용 | 5G carrier aggregation | beamforming, coding | spectrum vs power trade-off |

> 요약: 용량 증대는 대역폭 확보가 선형 효과를 주고, SNR 증가는 로그 특성 때문에 전력 대비 증가 폭이 제한된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 성능 평가 | 속도 측정값 | Shannon 용량 상한 | 링크 예산과 이론 한계 비교 |
| 개선 수단 | 송신 전력 증가 | B, SNR, coding, MIMO 조합 | 전력 규제와 spectrum 비용 |
| 운영/위험 | 최대 속도 광고 | effective throughput 산정 | overhead, BER, retransmission 반영 |

> 요약: 설계 판단은 이론 C와 실제 R의 gap을 보고 대역폭, SNR, 코딩, MIMO 중 병목을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 과대 산정 | 프로토콜 오버헤드 미반영 | PHY/MAC/application throughput 분리 | goodput/C ratio |
| SNR 변동 | 이동성·페이딩·간섭 | link adaptation, diversity | SNR p5, outage probability |
| 구현 손실 | 비이상 코딩·RF 손실 | coding gain 개선, calibration | coding gap dB |

> 요약: Shannon 용량은 상한이므로 실제 설계에서는 오버헤드, SNR 변동, 구현 손실을 별도 반영한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 용량 계산 | C=B log2(1+S/N) 산출 | spectrum analyzer, link budget |
| Gap | actual throughput/C 50%~80% | iperf, PHY counter |
| 신뢰도 | BER/BLER 목표 충족 | BER tester, modem KPI |

> 요약: 링크 평가는 이론 용량, 실제 처리량 비율, BER/BLER를 동시에 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. B, SNR dB, noise figure, path loss를 링크 예산표에 입력하고 `C=B log2(1+S/N)`로 상한을 산정함
2. 목표 R이 C에 근접하면 고차 QAM, 낮은 code rate, MIMO stream, carrier aggregation 조합을 검토함
3. 실제 goodput은 PHY rate에서 FEC, MAC header, retransmission, TCP/UDP overhead를 차감해 검증함

**결론 (2줄):**
- 기술사 판단: 요구 전송률이 Shannon 용량의 80%를 초과하면 대역폭 추가, SNR 개선, MIMO 적용 중 하나를 설계 변경으로 반영함
- 향후 방향: 5G/6G는 massive MIMO, RIS, adaptive coding으로 Shannon 한계와 실제 처리량 gap을 줄이는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | B, S/N, C 계산 흐름 | 대역폭 vs SNR 영향 비교 |
| 요구사항 명시형 | "계산하시오", "비교하시오", "방안을 제시하시오" | SNR dB 변환과 용량 산정 | throughput gap, coding gap, 개선 수단 |

> 요약: 설명형은 Shannon 식 의미, 계산형은 B·SNR 변환과 실제 처리량 차이를 중심으로 작성한다.
