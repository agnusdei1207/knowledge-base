---
title: "채널 코딩 — 해밍·Reed-Solomon·터보 (Channel Coding)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 76
---

# 📖 【암기용】 개념 완전 이해

> 목적: 채널 코딩을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 전송 중 생기는 비트 오류를 검출·정정하기 위해 여분 비트를 추가하는 부호화 기술
- **왜 필요한가**: 무선, 광, 저장장치, 위성 링크는 잡음과 간섭 때문에 비트가 뒤집힌다. 재전송만으로 해결하면 지연과 대역폭 사용량이 증가하므로 수신 측 정정 능력이 필요하다.
- **핵심 직관**: 중요한 문서를 보낼 때 원문 일부를 반복하거나 검사 숫자를 붙여, 일부 글자가 훼손되어도 복원하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 실제 채널은 열잡음, 페이딩, 간섭으로 BER이 0이 아니다. 채널 코딩은 정보 비트에 parity/check symbol을 추가해 오류 패턴을 탐지하고, 부호의 최소거리로 정정 가능 범위를 정한다.
- **작동 원리**: 해밍 부호는 단일 비트 오류 정정에 적합하다. Reed-Solomon은 심벌 단위 블록 오류에 강해 CD, QR, 저장장치에 쓰인다. 터보 부호는 interleaver와 반복 복호로 Shannon 한계에 근접한다.
- **비유**: 여행 가방에 물건 목록과 무게 합계를 함께 넣으면, 일부 물건이 빠졌을 때 어떤 항목이 문제인지 추정할 수 있다.
- **구체 예시**: Hamming(7,4)는 4비트 데이터에 3비트 parity를 붙여 1비트 오류를 정정한다. RS(255,223)는 32개 parity symbol로 최대 16 symbol 오류를 정정할 수 있다.
- **흔한 오해·주의점**: 채널 코딩은 압축이 아니다. 소스 코딩은 중복을 줄이고, 채널 코딩은 오류 정정을 위해 의도적으로 중복을 추가한다.

## 연결 개념
- 소스 코딩 — 정보 중복 제거, 채널 코딩과 목적이 반대
- Shannon Channel Capacity — 오류 없는 통신 가능 한계를 제시
- FEC/ARQ — 오류 정정과 재전송 기반 오류 제어 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 채널 코딩은 부호율, 최소거리, 오류 정정 능력, 복호 복잡도를 함께 비교해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 채널 코딩은 정보 비트에 검사용 중복을 추가해 잡음 채널에서 오류 검출·정정을 수행하는 FEC 기술이다.
> 2. **가치**: BER을 10^-3에서 10^-6 수준으로 낮추기 위해 Hamming, Reed-Solomon, Turbo, LDPC 같은 부호를 채널 특성에 맞게 선택한다.
> 3. **판단 포인트**: 부호율 R=k/n, 최소거리 dmin, 정정 능력 t=(dmin-1)/2, 복호 지연과 계산량을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 오류 제어 원리 확인 | parity, syndrome, minimum distance, FEC | 압축 기술과 혼동 |
| 부호별 적용 판단 | Hamming 단일 비트, RS burst error, Turbo 반복 복호 | 장단점만 추상 서술 |
| 정량 지표 활용 | BER, code rate, coding gain, latency | 수식과 지표 누락 |

> 요약: 이 문제는 오류를 어떻게 찾고 고치는지와 부호 선택 기준을 수치로 연결하는 답안이 필요하다.

---

## Ⅰ. 개요 및 필요성

채널 코딩은 전송 오류 정정을 위해 중복 비트를 추가하는 기술이다. 실제 통신 채널은 잡음과 간섭으로 비트 오류가 발생한다. 채널 코딩은 재전송 없이 수신 측에서 오류를 검출·정정해 BER, 지연, 대역폭 사용량을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Bits -> Channel Encoder -> Coded Bits -> Noisy Channel
-> Channel Decoder -> Error Detection/Correction -> Recovered Bits
              +-> Parity/Syndrome/Interleaver
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Encoder | 정보 비트에 parity 추가 | code rate R=k/n |
| Channel | 잡음·간섭·페이딩 발생 | BER, SNR로 품질 측정 |
| Decoder | syndrome/metric 기반 오류 정정 | hard/soft decision |
| Interleaver | burst error 분산 | Turbo, 무선 링크 적용 |

> 요약: 채널 코딩은 송신 중복 추가와 수신 오류 정정으로 잡음 채널의 BER을 목표 수준으로 낮춘다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Information Bits -> Generate Parity -> Transmit Codeword
-> Receive with Error -> Compute Syndrome/Metric
-> Locate Error -> Correct Bits/Symbols -> Output Data
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | k비트 정보를 n비트 codeword로 변환 | code rate R=k/n |
| 2 | 채널에서 비트·심벌 오류 발생 | SNR, Eb/N0 측정 |
| 3 | 수신기가 syndrome 또는 likelihood 계산 | syndrome 0 여부 |
| 4 | 오류 위치와 값을 추정해 정정 | t=(dmin-1)/2 |
| 5 | CRC 또는 상위 계층으로 잔여 오류 확인 | residual BER 10^-6 목표 |

> 요약: 부호어 생성, 잡음 통과, syndrome 계산, 오류 정정, 잔여 오류 검증 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | Hamming | Reed-Solomon | Turbo |
|:---|:---|:---|:---|
| 오류 단위 | 비트 오류 | 심벌·burst 오류 | 확률 기반 비트 오류 |
| 대표 구조 | Hamming(7,4) | RS(255,223) | 병렬 convolutional + interleaver |
| 정정 능력 | 1비트 정정 | 16 symbol 정정 예시 | Shannon 한계 근접 coding gain |
| 판단 포인트 | 저복잡도 메모리 | 저장·방송·QR | 이동통신, 반복 복호 지연 |

> 요약: Hamming은 단순 비트 오류, RS는 burst 오류, Turbo는 낮은 SNR 무선 채널에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 오류 제어 | ARQ 재전송 | FEC 채널 코딩 | RTT 크고 재전송 비용 큰 링크 |
| 부호 선택 | 단일 parity | Hamming/RS/Turbo | 오류 패턴, 지연, 복잡도 |
| 운영/위험 | 무부호 전송 | 부호율 R에 따른 중복 추가 | 대역폭 대비 BER 목표 |

> 요약: 재전송 지연이 큰 무선·위성·저장 환경에서는 FEC 부호 선택이 BER 목표 달성의 핵심이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 대역폭 증가 | parity 중복 추가 | code rate R 조정 | overhead percentage |
| 복호 지연 | 반복 복호·복잡한 알고리즘 | iteration limit, 하드웨어 가속 | decoding latency ms |
| 오류 패턴 불일치 | burst 오류에 비트 부호 적용 | interleaving, RS 선택 | residual BER, burst length |

> 요약: 채널 코딩은 BER 감소와 중복·지연 증가의 절충이므로 채널 오류 패턴에 맞춰 선택한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| BER | 10^-6 이하 또는 서비스 기준 | BER tester, packet capture |
| 부호율 | R=k/n, 링크 예산 내 overhead | encoder 설정, throughput 측정 |
| 복호 지연 | 실시간 서비스 지연 예산 이하 | decoder profiling |

> 요약: 도입 효과는 BER, 부호율, 복호 지연을 동시에 측정해 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 오류 패턴이 단일 비트 중심이면 Hamming 계열, burst symbol 오류이면 RS(255,223), 낮은 SNR 무선이면 Turbo/LDPC를 선택함
2. 목표 BER 10^-6, 허용 지연 ms 단위, 부호율 R을 링크 예산표에 반영해 변조·코딩 조합을 결정함
3. FEC 후 CRC와 ARQ를 결합해 residual error를 검출하고, SNR 저하 시 MCS를 단계적으로 낮춤

**결론 (2줄):**
- 기술사 판단: 재전송 비용이 큰 채널은 FEC를 우선 적용하고, 오류 패턴에 따라 Hamming, RS, Turbo 계열을 선택함
- 향후 방향: 5G/위성/저장장치는 LDPC, Polar, AI 기반 복호 최적화로 BER과 복호 지연을 함께 관리함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | parity, syndrome, 오류 정정 흐름 | Hamming, RS, Turbo 비교 |
| 요구사항 명시형 | "비교하시오", "적용 방안을 제시하시오" | 오류 패턴별 부호 선택 절차 | BER, 부호율, 복호 지연 지표 |

> 요약: 설명형은 오류 정정 원리, 비교형은 부호별 오류 패턴과 지표를 중심으로 답안을 구성한다.
