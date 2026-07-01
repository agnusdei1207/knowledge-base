---
title: "WDM·DWDM 광 다중화 (WDM DWDM)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 84
---

# 📖 【암기용】 개념 완전 이해

> 목적: WDM과 DWDM을 처음 봐도 파장 다중화와 광 백본 용량 확장의 원리를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 하나의 광섬유에 여러 파장(lambda)을 동시에 실어 전송 용량을 늘리는 광 다중화 기술
- **왜 필요한가**: 광섬유 포설은 비용과 시간이 크다. WDM은 기존 광섬유 한 가닥에 여러 독립 채널을 올려 Tbps급 백본을 구성한다.
- **핵심 직관**: 한 도로에 색깔이 다른 차선을 여러 개 만들어 각 파장별 데이터를 동시에 보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: TDM만으로 속도를 올리면 송수신 전자 회로 한계와 재생 장비 비용이 증가한다. 파장을 나누면 각 채널은 독립 속도를 유지하면서 총 용량을 합산할 수 있다.
- **작동 원리**: 송신 측 transponder가 서로 다른 광 파장으로 변환하고 mux가 합친다. 수신 측 demux가 파장을 분리하며 EDFA, ROADM, OTN이 전송과 운용을 보조한다.
- **비유**: 라디오 방송국이 서로 다른 주파수로 동시에 송출하고 수신기가 원하는 주파수를 고르는 것과 같다.
- **구체 예시**: DWDM은 ITU-T grid에서 100GHz 또는 50GHz 간격을 사용하며, 80채널 x 100Gbps 구성은 8Tbps급 광섬유 용량을 제공한다.
- **흔한 오해·주의점**: 파장을 무한히 늘릴 수 없다. chromatic dispersion, OSNR, nonlinear effect, wavelength drift가 채널 간격과 거리 한계를 만든다.

## 연결 개념
- Optical Internet — IP/MPLS와 광 전송망 연계
- OTN — DWDM 위에서 클라이언트 신호를 감싸는 전송 계층
- ROADM — 파장 단위 add/drop과 경로 재구성 장비

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: WDM/DWDM은 광섬유 용량 확장 문제이며 wavelength grid, OSNR, dispersion, ROADM 운용을 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WDM/DWDM은 하나의 광섬유에 여러 파장 채널을 다중화해 총 전송 용량을 채널 수 x 채널 속도로 확장하는 기술이다.
> 2. **가치**: 신규 광섬유 포설 없이 40/80/96개 파장과 100G/400G coherent 채널로 Tbps급 백본을 구성한다.
> 3. **판단 포인트**: channel spacing, OSNR, dispersion, nonlinear effect, ROADM 운용성이 설계의 핵심 제약이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 광 다중화 원리 확인 | wavelength, mux/demux, transponder | 단순 주파수 분할로만 설명 |
| CWDM/DWDM 차이 확인 | 채널 간격, 채널 수, 거리, 비용 | WDM과 DWDM을 동일 개념으로 처리 |
| 백본 설계 판단 확인 | OSNR, EDFA, dispersion, ROADM | 용량만 쓰고 품질 지표 누락 |

> 요약: 이 문제는 파장 다중화 구조와 광 물리 품질 제약을 함께 제시하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

WDM/DWDM은 광섬유의 파장 자원을 나누어 다중 전송하는 기술이다.
IP 트래픽, 클라우드, 데이터센터 연동은 백본 용량을 Tbps 단위로 요구하지만 광섬유 증설은 선로·허가·공사 제약이 크다.
WDM/DWDM은 파장 단위 채널을 병렬화해 기존 광섬유 활용률을 높이고 장거리 광 백본의 확장 기준을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Signal -> Transponder -> Wavelength Channel
              / lambda1
              / lambda2
              / lambdaN
-> Optical Mux -> Fiber/EDFA/ROADM -> Demux -> Receiver
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Transponder | 전기 신호를 특정 광 파장으로 변환 | 100G/400G coherent |
| Mux/Demux | 여러 파장을 결합·분리 | AWG, filter |
| EDFA | C-band 광 증폭 | O/E/O 변환 없이 증폭 |
| ROADM | 파장 단위 add/drop | colorless/directionless 옵션 |

> 요약: WDM/DWDM은 transponder, mux/demux, amplifier, ROADM이 파장 단위 전송 경로를 구성함.

---

## Ⅲ. 동작원리 및 흐름도

```text
클라이언트 신호 수용 -> 파장 변환 -> 파장 다중화
-> 광섬유 전송/증폭 -> 파장 선택 add/drop
-> 역다중화 -> 수신 복원
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Ethernet/OTN 클라이언트 신호 수용 | client rate, FEC status |
| 2 | ITU-T grid 파장에 매핑 | wavelength accuracy |
| 3 | mux 후 광섬유로 동시 전송 | OSNR, launch power |
| 4 | demux/ROADM에서 파장 분리 | BER, chromatic dispersion |

> 요약: 각 클라이언트 신호는 독립 파장으로 변환되고, 광섬유에서는 파장들이 동시에 전달된 뒤 수신부에서 분리됨.

---

## Ⅳ. 특징

| 구분 | CWDM/WDM | DWDM | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 채널 간격 | 넓은 간격 | 100GHz, 50GHz, 25GHz grid | ITU-T G.694.x |
| 채널 수 | 8~18채널 수준 | 40/80/96채널 이상 | C-band/L-band |
| 전송 거리 | metro 중심 | metro/core/long-haul | EDFA, DCM, coherent |
| 운용 | 비용 중심 | ROADM 기반 동적 경로 | OSNR margin dB |

> 요약: CWDM은 metro 비용 중심, DWDM은 좁은 간격과 광 증폭을 활용한 장거리·대용량 백본 중심임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | DWDM | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 파장 광 링크 | 다파장 mux/demux, ROADM | 광섬유 부족, 용량 증가율 |
| 비용/용량 | 광섬유 증설 | 채널 추가로 증설 | 채널당 100G/400G 단가 |
| 운영/위험 | 링크 단순 | OSNR·분산·비선형 관리 | span length, amplifier count |

> 요약: 광섬유 포설 제약과 Tbps급 증설 요구가 있으면 DWDM, 단거리 저채널 요구는 CWDM을 우선 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| OSNR 부족 | 증폭 누적 잡음 | EDFA gain 설계, FEC | OSNR dB, pre-FEC BER |
| 분산 증가 | 장거리 전송 | coherent DSP, DCM | chromatic dispersion ps/nm |
| 비선형 효과 | 과도한 launch power | power equalization | Q-factor, nonlinear penalty |

> 요약: DWDM 품질은 OSNR, 분산, 비선형 효과를 link budget으로 관리해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 광 품질 | OSNR margin 3dB 이상 | optical spectrum analyzer |
| 오류율 | post-FEC BER 10^-15 이하 | transponder PM |
| 파장 운용 | wavelength drift 허용 범위 내 | NMS, optical channel monitor |

> 요약: 도입 평가는 OSNR margin, BER, 파장 drift를 채널별로 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. metro 구간은 CWDM 또는 low-channel DWDM, core 구간은 80채널 이상 DWDM과 ROADM ring으로 분리 설계함.
2. 100G/400G coherent 채널은 span length, EDFA count, OSNR margin을 link budget에 반영함.
3. 운영은 NMS에서 wavelength, pre-FEC BER, optical power, OSNR을 채널별 KPI로 관리함.

**결론 (2줄):**
- 기술사 판단: 광섬유 증설보다 파장 증설 비용이 낮고 OSNR margin이 확보되면 DWDM을 선택함.
- 향후 방향: DWDM은 OTN, coherent optics, flex-grid ROADM과 결합해 데이터센터·클라우드 백본의 기본 전송 계층으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WDM/DWDM을 설명하시오" | 파장 변환 -> mux -> 증폭 -> demux 흐름 | CWDM/DWDM 차이와 적용 영역 |
| 요구사항 명시형 | "광 백본 설계 방안을 제시하시오", "비교하시오" | link budget, OSNR, ROADM 설계 | 채널 수, 거리, 비용, 품질 지표 |

> 요약: 설명형은 파장 다중화 원리, 요구사항형은 광 품질 제약과 증설 판단 기준으로 목차를 전환함.
