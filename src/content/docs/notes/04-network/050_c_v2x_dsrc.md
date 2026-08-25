---
sidebar:
  order: 50
  label: "050. C-V2X와 DSRC 비교"
  badge:
    text: "기출 · 30%"
    variant: note
title: "차량 사물 통신 표준 비교 : C-V2X vs DSRC (C-V2X vs DSRC)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 50
extra:
  question_no: "50"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "3GPP C-V2X(PC5/Uu), IEEE 802.11p WAVE(DSRC), MAC 계층 채널 접속 및 진화 로드맵"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **C-V2X (Cellular V2X)**: 3GPP 표준 기반으로 직접 통신(PC5)과 셀룰러 기지국 통신(Uu)을 결합한 차량 통신 기술.
- **DSRC / WAVE (802.11p)**: Wi-Fi(802.11a)를 차량용 5.9GHz 대역으로 개량하여 기지국 없이 CSMA/CA로 애드혹 통신하는 1세대 표준.

</details>

- 정의/개념: C-ITS 구현을 위해 개발된 **3GPP 이동통신 기반 C-V2X와 IEEE 와이파이(802.11p) 기반 DSRC(WAVE) 차량 무선 통신 표준**
- 배경/필요성: 1세대 DSRC(802.11p)의 CSMA/CA 경합 방식 한계로 인한 **차량 밀집 시 패킷 충돌 급증, 통신 거리 한계(300m) 및 5G-NR 협력 주행 진화 불가**

#### 한줄 요약
- DSRC는 CSMA/CA 기반 단거리 통신이며, C-V2X는 준지속 스케줄링(SPS)과 광역 셀룰러 결합 기술이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPS (Semi-Persistent Scheduling, Mode 4)**: C-V2X에서 기지국 없이 차량이 무선 채널을 자체 센싱하여 간섭이 적은 자원 블록을 선점 예약하는 알고리즘.
- **CSMA/CA Contention**: DSRC에서 반송파 감지 후 임의의 백오프 시간을 대기하여 채널을 경쟁 점유하는 방식.

</details>

- **C-V2X의 고밀도 신뢰성**: SC-FDMA/OFDMA 기반 자원 블록(RB) 분할 및 **자율 센싱 스케줄링(SPS, Mode 4)**을 통한 충돌 방지
- **통신 범위 및 서비스 확장성**: DSRC가 300m에 국한되는 반면 **C-V2X는 PC5(직접 1km)와 Uu(기지국 광역망)를 결합 지원**
- **글로벌 단일 표준 수렴**: 한국, 미국, 중국 등 주요국이 차세대 C-ITS 단일 표준으로 **C-V2X 공식 채택**

#### 한줄 요약
- C-V2X는 SPS 스케줄링, 1km 도달 거리, 5G-NR 진화성에서 DSRC 대비 우위를 갖는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Dual-Mode RSU**: 기존 구축된 DSRC 인프라와 신규 C-V2X 차량 단말을 동시에 수용하기 위해 두 무선 규격을 모두 탑재한 하이브리드 노변 기지국.

</details>

```text
[C-V2X (이중 인터페이스) vs DSRC (단일 애드혹) 아키텍처 비교]
|-- C-V2X Architecture
|   |-- PC5 Sidelink (3GPP Rel-14/15/16: 5.9GHz 직접 통신, 10ms, 최대 1km)
|   |-- OBU <-> OBU (V2V 충돌 경보, 군집 주행 Platooning)
|   |-- OBU <-> RSU (V2I 신호 주기 SPaT, 보행자 검지)
|   `-- Uu Cellular Link (5G gNB -> 5GC Core -> 광역 C-ITS 관제 센터 연동)
`-- DSRC / WAVE Architecture
    |-- IEEE 802.11p / 1609 (5.9GHz OFDM CSMA/CA 애드혹 통신, 최대 300m)
    `-- OBU <-> RSU (단거리 단순 브로드캐스트 경보)
```

선의 의미: C-V2X는 직접 통신(PC5)과 광역 셀룰러(Uu)를 동시 지원하고 DSRC는 단일 직접 통신만을 지원하는 구조

| 비교 요소 | C-V2X (Cellular V2X) | DSRC / WAVE (802.11p) |
|:---|:---|:---|
| **물리/MAC 표준** | **3GPP Rel-14/15/16 (LTE-V2X, 5G-V2X)** | **IEEE 802.11p / IEEE 1609 (WAVE)** |
| **채널 다중화 방식** | **SC-FDMA / OFDMA 기반 스케줄링** | **OFDM 기반 CSMA/CA (경합 방식)** |
| **통신 인터페이스** | **PC5 (사이드링크 직접) + Uu (셀룰러 광역)** | **802.11p (단일 직접 통신 링크)** |
| **최대 통신 거리** | **최대 1,000 m (직접 통신 기준)** | **최대 300 m 이내** |
| **자원 할당 방식** | 자율 센싱 기반 준지속 스케줄링 (**SPS, Mode 4**) | 비인프라 난수 백오프 CSMA/CA |

#### 한줄 요약
- C-V2X는 PC5/Uu 이중 인터페이스와 OFDMA 스케줄링을, DSRC는 802.11p 단일 링크와 CSMA/CA를 채택한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CBR (Channel Busy Ratio)**: 차량 밀집 지역에서 채널 혼잡도를 측정하여 SPS 전송 간격을 동적 제어하는 혼잡 지표.

</details>

```text
C-V2X Mode 4 자율 스케줄링 vs DSRC CSMA/CA 동작 파이프라인
        │
   [C-V2X Mode 4 (SPS)]              [DSRC 802.11p (CSMA/CA)]
        │                                 │
   1. [서브채널 RSRP/RSSI 센싱]       1. [캐리어 센싱 (CCA)]
      1,000ms 채널 간섭 계측             채널 유휴 여부 즉각 판정
        │                                 │
   2. [하위 20% 최적 후보군 선별]     2. [DIFS 대기 & 백오프]
      비어있는 자원 블록(RB) 선별         무작위 Contention Window
        │                                 │
   3. [SPS 예약 타이머 설정]          3. [브로드캐스트 송출]
      충돌 없는 주기적 BSM 송출           동시 송출 시 충돌/유실 발생
```

#### 한줄 요약
- C-V2X는 채널 센싱 기반 SPS 예약으로 충돌을 회피하고, DSRC는 CSMA/CA 무작위 백오프로 송출한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **5G-NR V2X**: Rel-16 이후 초저지연(1ms)과 고신뢰(99.999%), 1Gbps 대역폭을 제공하여 센서 공유 및 원격 제어를 가능하게 하는 기술.

</details>

| 비교 항목 | C-V2X (Cellular V2X) | DSRC / WAVE (IEEE 802.11p) |
|:---|:---|:---|
| **주관 표준화 기구** | **3GPP, 5GAA (통신·자동차 연합)** | **IEEE, ISO (전통 무선랜 진영)** |
| **고밀도 환경 신뢰성**| **우수 (자원 예약 스케줄링으로 패킷 충돌 억제)** | **취약 (차량 증가 시 충돌 급증 및 PDR 급감)** |
| **최대 고속 이동성** | **최대 250 ~ 500 km/h (도플러 보정 지원)** | **최대 200 km/h 내외** |
| **차세대 진화 로드맵**| **5G-NR V2X, 6G-V2X (센서 공유, 군집주행)** | IEEE 802.11bd (표준 개발 지연 및 투자 축소) |
| **국가별 정책 채택** | **한국, 미국, 중국 단일 표준 공식 채택** | 초기 시범 사업 후 C-V2X로 전환 추세 |

#### 한줄 요약
- C-V2X는 고밀도 안정성, 5G 진화성, 글로벌 표준 채택 면에서 DSRC 대비 기술적 우위를 확보했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Telematics + V2X SoC**: 5G 셀룰러 모뎀과 C-V2X 사이드링크 모뎀을 단일 실리콘 칩으로 통합한 차량용 원칩 반도체.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기존 기구축된 DSRC 기반 RSU 인프라와 신규 C-V2X 단말 간 비호환성 | **`이중 모드(Dual-Mode RSU/OBU)` 도입 및 단계적 전환** | 기존 인프라 매몰 비용 방지 및 원활한 표준 전환 |
| 5.9GHz V2X 전용 대역 내 비인가 무선랜(Wi-Fi 6E) 간섭 위협 | V2X 대역(5.850~5.925GHz) 전용 보호 및 **RF 대역통과 필터** | 인접 Wi-Fi 간섭 차단 및 통신 신뢰성 확보 |
| C-V2X 모뎀과 5G 텔레매틱스 분리 탑재 시 차량 원가 및 배선 복잡 | **`5G 텔레매틱스 + C-V2X 통합 SoC(원칩)` 솔루션 적용** | 부품 단가 절감 및 차량 장착 간소화 |
| 고속 주행 시 도플러 편이로 인한 사이드링크 복조 실패 | **DMRS(복조 파일럿) 고밀도 배치 및 `고속 도플러 추정 보정`** | 200km/h 이상 고속 주행 시 패킷 수신율 유지 |

#### 한줄 요약
- Dual-Mode 장비 전환, RF 필터링, 통합 SoC 원칩화, DMRS 도플러 보정으로 운영한다.

## Ⅶ. 결론

- 글로벌 지능형 교통 체계(C-ITS) 표준이 고밀도 환경 신뢰성과 5G 진화성이 우수한 **3GPP C-V2X로 단일화 확정**됨에 따라, 기존 DSRC 인프라와의 연동을 위해 **이중 모드(Dual-Mode) RSU**를 과도기 적용하고, 완전 자율주행(Level 4/5)을 위해 **5G-NR V2X 기반 협력 주행 인프라**를 조기 구축

#### 한줄 요약
- C-V2X는 SPS 스케줄링과 5G-NR 진화성을 통해 자율주행의 글로벌 표준으로 자리잡은 핵심 차량 통신 기술이다.