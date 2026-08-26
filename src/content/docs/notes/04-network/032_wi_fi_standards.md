---
sidebar:
  order: 32
  label: "032. Wi-Fi 표준"
  badge:
    text: "기출 · 50%"
    variant: note
title: "Wi-Fi 무선 LAN 표준 : 802.11ac•ax•be (Wi-Fi Standards)"
date: "2026-08-26T13:42:33+09:00"
tags:
  - "notes-network"
weight: 32
extra:
  question_no: "32"
  source_status: "기출"
  source_history: "125회, 134회"
  priority: 50
  priority_note: "IEEE 802.11ac, 802.11ax(Wi-Fi 6), 802.11be(Wi-Fi 7) 진화 및 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IEEE 802.11**: 비면허 주파수 대역에서 무선 LAN의 물리(PHY) 및 MAC 계층을 정의하는 국제 무선 통신 표준.
- **AP (Access Point)**: 유선 이더넷 백본망(DS)과 무선 단말(STA) 간에 프레임 변환 및 전파 송수신을 중계하는 무선 기지국 장비.

</details>

- 정의/개념: 비면허 대역(2.4GHz, 5GHz, 6GHz)에서 **대역폭 확장, 고차 변조(4096-QAM) 및 다중 링크(MLO)를 진화시킨 무선 LAN 표준 규격(IEEE 802.11ac/ax/be)**
- 배경/필요성: 구형 무선 규격의 단일 링크 한계로 인한 **고밀도 환경 주파수 충돌, 4K/8K 스트리밍 및 AR/VR 초저지연 지원 불가**

#### 한줄 요약
- 비면허 대역 확장, OFDMA 다중 접속, 4096-QAM 변조, MLO 다중 링크를 통해 초고속 무선 통신을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OFDMA (Orthogonal Frequency Division Multiple Access)**: 단일 채널을 복수의 자원 단위(RU)로 세분화하여 다수 단말이 동시 통신하는 기술.
- **MLO (Multi-Link Operation)**: 2.4GHz, 5GHz, 6GHz 대역의 복수 링크를 단일 단말이 동시 결합하여 대역폭 증대 및 지연을 최소화하는 기술.

</details>

- **세대별 대역 확장**: Wi-Fi 5(5GHz) $\to$ Wi-Fi 6/6E(2.4/5/6GHz) $\to$ Wi-Fi 7(최대 320MHz 초광대역 및 MLO)
- **고차 변조 진화**: 256-QAM(11ac) $\to$ 1024-QAM(11ax) $\to$ **4096-QAM(11be, 4K-QAM)** 심볼당 비트 극대화
- **고밀도 다중 접속 최적화**: BSS Coloring, Target Wake Time(TWT), UL/DL MU-MIMO 다중 단말 수용

#### 한줄 요약
- 4096-QAM 변조, 320MHz 채널 폭, OFDMA 다중 접속, MLO 다중 링크 결합을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BSS (Basic Service Set)**: 단일 AP와 이에 결합(Associate)된 무선 단말(STA)들로 구성되는 기본 무선 셀 단위.
- **Distribution System (분배 시스템, DS)**: 복수의 AP(BSS)를 연결하여 로밍 및 유선망 연동을 제공하는 백본 스위치 네트워크.

</details>

```text
[Wi-Fi 무선 LAN 인프라 토폴로지 및 MLO 링크 결합]
|-- Wireless Stations (STA: Smart Phone / AR Glass / Laptop)
|   `-- MLO Engine (2.4GHz + 5GHz + 6GHz 다중 대역 동시 링크 결합 송수신)
`-- Access Point (AP: 802.11be Tri-Band Wi-Fi 7 기지국)
    |-- Radio Interfaces (2.4GHz, 5GHz, 6GHz 독립 RF 모듈)
    |-- MAC / PHY Controller (OFDMA Multi-RU 스케줄링, 4096-QAM 변복조)
    `-- Security Engine (WPA3-SAE 동시 인증)
`-- Distribution System (DS: 유선 백본 스위칭망 / 게이트웨이 라우터)
```

선의 의미: 계층 및 무선 단말이 3개 주파수 대역을 MLO로 결합하여 AP에 접속하고 AP가 유선 DS 백본망으로 프레임을 중계하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **무선 단말 (STA)** | 무선 NIC를 탑재하여 AP와 결합하고 **MLO 다중 대역을 동시 결합 송수신** | 스마트폰, IoT |
| **무선 접근점 (AP)** | 802.11 무선 프레임과 802.3 이더넷 프레임을 **상호 브리지하고 무선 매체 스케줄링 제어** | 무선 기지국 |
| **기본 서비스 세트 (BSS)**| 단일 AP의 무선 전파 도달 범위 내에서 **수립된 기본 무선 통신 셀 도메인 (BSSID)** | 기본 통신 셀 |
| **분배 시스템 (DS)** | 복수 BSS 간의 **무선 단말 로밍 및 유선 네트워크 연결을 제공하는 고속 백본망** | 유선 스위칭망 |

#### 한줄 요약
- STA 단말, AP 기지국, BSS 도메인, 분배 시스템(DS)이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Wi-Fi 접속 5단계**: 매체 탐색 $\to$ 신원 인증 $\to$ 링크 결합 $\to$ 4-Way Handshake $\to$ 무선 통신 개시.

</details>

```text
Wi-Fi 단말 접속 및 보안 통신 수립 파이프라인
        │
   1. [매체 탐색] 비콘 수신(Passive Scan) 또는 프로브 요청/응답(Active Scan)
        │
   2. [신원 인증] WPA3-Personal(SAE) 또는 WPA3-Enterprise(802.1X EAP) 상호 인증
        │
   3. [링크 결합] MLO 다중 링크, 채널 폭(320MHz), MIMO 규격 협상 및 Association 완료
        │
   4. [4-Way Handshake] 암호화 키(PTK/GTK) 상호 유도
        │
   ▼
5. [고속 무선 통신 개시] 4096-QAM 및 OFDMA 기반 초고속 데이터 송수신
```

#### 한줄 요약
- 비콘 탐색 → WPA3 인증 → 결합 협상 → 4-Way Handshake → 데이터 통신 순으로 수립된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Wi-Fi 5 (802.11ac)** vs **Wi-Fi 6/6E (802.11ax)** vs **Wi-Fi 7 (802.11be)**.

</details>

| 비교 항목 | Wi-Fi 5 (802.11ac) | Wi-Fi 6/6E (802.11ax) | Wi-Fi 7 (802.11be) |
|:---|:---|:---|:---|
| **지원 주파수 대역** | 5 GHz 전용 | 2.4 GHz, 5 GHz, **6 GHz (6E)** | 2.4 GHz, 5 GHz, **6 GHz 전 대역** |
| **최대 채널 대역폭** | 160 MHz | 160 MHz | **320 MHz (초광대역 2배)** |
| **최고 변조 방식** | 256-QAM | 1024-QAM (10-bit) | **4096-QAM (12-bit, 4K-QAM)** |
| **다중 접속 방식** | OFDM | **OFDMA (자원 단위 RU 분할)** | **OFDMA + Multi-RU 복합 할당** |
| **핵심 다중화 기술** | DL MU-MIMO (최대 4x4) | UL/DL MU-MIMO (최대 8x8) | **MLO (다중 링크 동시 결합), 16x16 MIMO** |
| **이론상 최고 전송률**| 약 6.9 Gbps | 약 9.6 Gbps | **약 46 Gbps (4.8배 향상)** |

#### 한줄 요약
- 802.11ac(단일 5GHz), 802.11ax(고밀도 OFDMA), 802.11be(320MHz 초광대역 및 MLO)로 진화했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BSS Coloring**: 동일 채널을 사용하는 인접 BSS 프레임에 색상 식별 비트를 부여하여 간섭 신호를 무시하고 공간을 재사용(Spatial Reuse)하는 기술.
- **Airtime Fairness**: 저속 구형 단말의 전파 독점을 방지하고 단말별 에어타임 점유 시간을 균등 분배하는 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동일 채널 인접 AP 간섭으로 인한 처리량 저하 및 무선 지연 | **Wi-Fi 6 `BSS Coloring (공간 재사용)` 및 동적 임계치 적용** | 인접 셀 간 간섭 회피 및 실효 대역폭 3배 향상 |
| WPA2 사전 대입 공격(Dictionary Attack) 및 패킷 스니핑 보안 취약점 | **`WPA3-Personal (SAE 동시 인증)` 및 WPA3-Enterprise 의무화** | 오프라인 사전 공격 차단 및 순방향 비밀성 보장 |
| 레거시 저속 단말(802.11b/g/n)의 전파 독점으로 고속 단말 지연 | **`Airtime Fairness (에어타임 공평성)` 및 5G/6GHz 밴드 스티어링** | 고속 단말 전송 기회 보장 및 트래픽 분산 |
| 6GHz 초고주파수 대역의 벽면 투과 손실 및 전파 도달 거리 축소 | **`Wi-Fi 7 MLO 링크 집성` 및 AP 밀집 배치(High-Density AP)** | 음영 지역 해소 및 무중단 고속 연결 유지 |

#### 한줄 요약
- BSS Coloring 공간 재사용, WPA3 보안 의무화, Airtime Fairness, MLO 결합으로 운영한다.

## Ⅶ. 결론

- 고밀도 접속은 **Wi-Fi 6**, 초저지연 다중 링크는 **Wi-Fi 7** 선택

#### 한줄 요약
- Wi-Fi 표준은 320MHz 대역폭, 4096-QAM, MLO 기술을 통해 진화하며, WPA3와 BSS Coloring을 결합하여 고품질·고보안 무선 인프라를 완성한다.
