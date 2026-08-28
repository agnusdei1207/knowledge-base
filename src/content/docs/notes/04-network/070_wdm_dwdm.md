---
sidebar:
  order: 70
  label: "070. WDM 및 DWDM 광 다중화"
  badge:
    text: "미출 · 30%"
    variant: note
title: "초광대역 광 파장 분할 다중화 : WDM, CWDM, DWDM"
date: "2026-08-26T13:59:37+09:00"
tags:
  - "notes-network"
weight: 70
extra:
  question_no: "70"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "파장 분할 다중화(WDM), CWDM vs DWDM 격자 간격, EDFA 광증폭, ROADM 및 Coherent 전송"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **WDM (Wavelength Division Multiplexing)**: 단일 광섬유 코어에 서로 다른 파장($\lambda$)의 광신호를 결합하여 동시 전송하는 다중화 기술.
- **DWDM vs CWDM**: 0.8nm/0.4nm 조밀 격자로 80채널 이상을 수용하는 고밀도 DWDM과 20nm 넓은 격자로 18채널을 수용하는 저비용 CWDM.

</details>

- 정의/개념: 단일 광섬유 케이블에 서로 다른 레이저 파장($\lambda_1 \sim \lambda_n$)을 **광 MUX로 결합하여 동시 전송하고 수신단 DEMUX로 분리하는 초광대역 광 다중화 기술**
- 배경/필요성: 용량 증설을 케이블 포설로 해결하면 구간마다 **막대한 토목 비용과 광심선 고갈**을 다시 치르므로, 이미 매설된 단일 광섬유 위에 파장을 채널로 나누는 광 다중화 계층을 얹어 물리 증설을 대신

#### 한줄 요약
- 단일 광섬유에 다중 파장을 결합하여 케이블 증설 없이 테라비트급 전송 용량을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **EDFA (Erbium-Doped Fiber Amplifier)**: C-Band(1530~1565nm) 영역의 다중 파장 광신호를 전기 변환 없이 30dB 이상 일괄 광학 증폭하는 핵심 광증폭기.
- **ROADM (Reconfigurable Optical Add-Drop Multiplexer)**: 파장 선택 스위치(WSS)를 통해 특정 파장을 전광(All-Optical)으로 분기·결합하는 지능형 광 노드 장비.

</details>

- **광섬유 인프라의 전송 용량 극대화**: 추가 케이블 매설 없이 단일 광섬유 심선당 **수십 Tbps 이상의 대역폭 확장**
- **프로토콜 및 속도 독립적 투명성(Transparency)**: 이더넷, SDH, OTN 등 이종 프로토콜 신호를 동일 광섬유에 독립 수용
- **전광(All-Optical) 증폭 및 스위칭**: 전기적 O-E-O 변환 없이 **EDFA 일괄 광증폭과 ROADM 파장 라우팅** 지원

#### 한줄 요약
- 케이블 증설 없는 Tbps급 용량 확장, 프로토콜 투명성, EDFA/ROADM 기반 전광(All-Optical) 전송을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Transponder (광 트랜스폰더)**: 비표준 단파장 클라이언트 신호를 ITU-T 표준 파장(C-Band)으로 변환(O-E-O)하고 FEC 패리티를 부가하는 장치.

</details>

```text
[DWDM 전광(All-Optical) 전송 시스템 아키텍처]
|-- 광 트랜스폰더 (표준 파장 변환)
|-- 광 MUX·DEMUX (파장 합성·분리)
|-- EDFA 증폭기 (다중 파장 증폭)
|-- ROADM (파장 경로 제어)
`-- 광 채널 모니터 (파워·OSNR 감시)
```

선의 의미: 트랜스폰더에서 정밀 파장으로 변환된 신호들이 MUX를 통해 단일 광케이블로 합성된 후 인라인 EDFA와 ROADM을 거쳐 수신단 DEMUX로 전달되는 구조

| 구성요소 | 책임 |
|:---|:---|
| 광 트랜스폰더 | 표준 파장 변환과 **FEC 부가** |
| 광 MUX·DEMUX | 다중 파장의 **합성·분리** |
| EDFA 증폭기 | C·L-Band의 **일괄 광증폭** |
| ROADM | 파장의 **통과·분기·결합 제어** |
| 광 채널 모니터 | 파워·드리프트·**OSNR 감시** |

#### 한줄 요약
- MUX/DEMUX가 파장 축을 채널로 분할하고 EDFA가 전기 변환 없이 광 상태 그대로 손실을 보충하므로, 중계 구간마다 필요하던 O-E-O 변환 장비가 경로에서 빠진다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RWA (Routing and Wavelength Assignment)**: 광통신망에서 최적 물리 광 경로를 탐색(Routing)하고 충돌 없는 파장을 선택 할당(Wavelength Assignment)하는 알고리즘.

</details>

```text
DWDM 광 경로(Lightpath) 수립 및 코히어런트 전송 파이프라인
        │
   [광 경로 및 파장 연산] SDN 컨트롤러가 RWA 알고리즘으로 최적 경로 및 동일 파장($\lambda_k$) 할당
        │
   [트랜스폰더 파장 변환] 송신 트랜스폰더가 Coherent 400G DSP를 구동하여 $\lambda_k$ 파장으로 변조
        │
   [광 MUX 합성 및 부스팅] AWG 합파기를 통해 다중 파장을 결합하고 EDFA로 1차 광증폭
        │
   [ROADM 전광 스위칭] 중간 노드들이 WSS 미러를 정렬하여 광 경로를 전기 변환 없이 패스스루
        │
   ▼
[코히어런트 수신 및 DSP 복원] 수신단 OCM이 OSNR을 검증하고 코히어런트 DSP가 색분산 역보상 복원
```

#### 한줄 요약
- 파장 연속성 확보 여부에서 광 경로 그대로 통과와 파장 변환 개입으로 갈리며, 후자는 변환기 비용을 치르고 경로 차단(Blocking)을 피한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CWDM** vs **DWDM** vs **Flex-Grid DWDM**: 20nm 간격(CWDM), 0.8nm 고정 간격(DWDM), 12.5GHz 가변 슬롯(Flex-Grid).

</details>

| 비교 항목 | 거친 파장 다중화 (CWDM) | 고밀도 파장 다중화 (DWDM) | 플렉스 그리드 (Flex-Grid DWDM) |
|:---|:---|:---|:---|
| 채널 간격 (Grid) | **20 nm (광대역 간격)** | **0.8 nm / 0.4 nm (100GHz / 50GHz)** | **12.5 GHz 단위 가변 슬롯 할당** |
| 수용 파장 수 | 최대 16~18 채널 (1270~1610nm) | **최대 80~160 채널 (C/L-Band)** | **수백 채널 (초고밀도 적응형 수용)** |
| 광증폭기 (EDFA) 적용 | **불가 (파장 간격이 너무 넓음)**| **완벽 적용 (C-Band 1550nm 집중)** | **완벽 적용 (C+L 광대역 증폭기)** |
| 전송 거리 및 용도 | 단거리 메트로망 ($\le 80\text{km}$) | **전국 기간 백본망, 해저 케이블** | **400G/800G 차세대 DCI 및 코어망**|
| 구축 비용 (Cost) | 저비용 (온도 제어 불필요) | 고비용 (정밀 쿨링 레이저 필수) | 최고비용 (코히어런트 DSP 및 WSS) |

#### 한줄 요약
- CWDM은 단거리 저비용망, DWDM은 전국 백본망, Flex-Grid는 400G/800G 차세대 초대용량 코어망에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Chromatic Dispersion (색분산, CD)**: 파장별 전파 속도 차이로 인해 광 펄스가 시간 축으로 퍼지는 왜곡 현상.
- **Coherent Optics (코히어런트 광통신)**: 광의 진폭, 위상, 편광을 모두 변조하고 초고속 DSP로 색분산과 PMD를 100% 디지털 역보상하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 파장 구간 점유로 인한 광 경로(Lightpath) 수립 실패 | ROADM 노드에 **`파장 변환기(Wavelength Converter)` 배치** | 파장 경합 해소 및 종단 간 광 경로 설정 성공률 향상 |
| 다단 EDFA 통과 시 자연 방출 잡음(ASE) 누적으로 OSNR 저하 | **`라만(Raman) 분산 증폭기` 결합 및 코히어런트 연판정 FEC** | 잡음 지수 개선 및 2,000km 초장거리 무재생 전송 달성 |
| 100G 이상 고속 전송 시 광섬유 색분산(CD) 및 비선형 왜곡 파형 붕괴 | **`DSP 기반 코히어런트 수신기(Coherent Optics)` 도입** | 물리적 분산 보상 광섬유(DCF) 제거 및 디지털 완벽 복원 |
| 파장별 레이저 노후화로 인한 파장 드리프트 및 인접 채널 간섭 | **`광 파장 잠금 장치(Wavelength Locker)` 및 OCM 상시 감시** | 파장 흔들림 원천 억제 및 50GHz 조밀 채널 간섭 차단 |

#### 한줄 요약
- 파장 변환기로 연속성을 확보하고, Raman/SD-FEC로 OSNR을 보존하며, Coherent DSP로 색분산을 보상한다.

## Ⅶ. 결론

- 거리·채널 수에 따라 **CWDM·DWDM·Flex-Grid**, 장거리는 **Coherent·SD-FEC**

#### 한줄 요약
- DWDM은 단일 광섬유에 다중 파장을 실어 전송하는 핵심 백본 기술이며, ROADM과 Coherent DSP를 결합하여 테라비트급 전광망을 실현한다.
