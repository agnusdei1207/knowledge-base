---
sidebar:
  order: 32
  label: "032. Wi-Fi 표준: 802.11ac•ax•be (Wi-Fi Standards)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "Wi-Fi 무선 LAN 표준 : 802.11ac•ax•be (Wi-Fi Standards)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "125회, 134회"
  priority: 50
  priority_note: "IEEE 802.11ac, 802.11ax(Wi-Fi 6), 802.11be(Wi-Fi 7) 진화 및 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IEEE 802.11**: 무선 근거리 통신망(WLAN)의 물리 계층(PHY) 및 매체 접근 제어 계층(MAC) 기술을 정의하는 국제 표준 규격 세트.
- **무선 접근점(Access Point, AP)**: 유선 이더넷 백본망(DS)과 무선 단말(STA) 간의 프레임 변환 및 전파 송수신을 중계하는 무선 네트워크 장비.

</details>

- 정의/개념: 비면허 대역(2.4GHz, 5GHz, 6GHz)에서 고속 무선 데이터 전송을 제공하기 위해 대역폭 확장, 고차 변조 및 다중 사용자 다중 접속을 표준화한 **무선 LAN 규격(IEEE 802.11ac/ax/be)**
- 배경/필요성: 스마트 기기 급증 및 고밀도 환경에서의 주파수 간섭 극복, 4K/8K 스트리밍 및 초저지연 AR/VR 서비스를 위한 실효 전송률(Throughput) 개선 요구

#### 한줄 요약
- 비면허 대역에서 대역폭 확장, 다중 접속(OFDMA), 다중 링크(MLO)를 통해 고속 무선 통신을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **직교 주파수 분할 다중 접속(OFDMA)**: 단일 무선 채널을 복수의 자원 단위(Resource Unit, RU)로 세분화하여 다수의 사용자가 동시에 데이터를 송수신할 수 있도록 지원하는 다중 접속 기술.
- **다중 링크 동작(Multi-Link Operation, MLO)**: 단말과 AP가 2.4GHz, 5GHz, 6GHz 대역의 복수 채널을 동시에 결합하여 처리량을 증대시키고 지연을 최소화하는 기술.

</details>

- **세대별 대역 확장**: Wi-Fi 5(5GHz) $\rightarrow$ Wi-Fi 6/6E(2.4/5/6GHz) $\rightarrow$ Wi-Fi 7(최대 320MHz 초광대역 및 MLO 지원)
- **고차 변조 기술 진화**: 256-QAM(802.11ac) $\rightarrow$ 1024-QAM(802.11ax) $\rightarrow$ **4096-QAM(802.11be)** 을 통한 심볼당 전송 비트수 극대화
- **고밀도 환경 효율화**: BSS Coloring, Target Wake Time(TWT) 및 UL/DL MU-MIMO를 통한 다중 단말 수용력 증대

#### 한줄 요약
- 4096-QAM 변조, 320MHz 채널 폭, OFDMA 다중 접속 및 MLO 다중 링크 결합을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **기본 서비스 세트(Basic Service Set, BSS)**: 단일 AP와 이에 결합(Associate)된 단말(STA)들로 구성되는 무선 LAN의 기본 네트워크 단위.
- **분배 시스템(Distribution System, DS)**: 복수의 AP들을 상호 연결하여 확장 서비스 세트(ESS)를 구성하는 유선 백본 네트워크.

</details>

```text
[ 무선 단말 (STA 1..N) ] ── (2.4GHz / 5GHz / 6GHz 전파) ──▶ [ 무선 접근점 (AP) ]
                                                              │
                                                              ▼ (유선 이더넷 트렁크)
                                              [ 분배 시스템 (DS / 백본 스위치) ]
```

선의 의미: 무선 단말이 비면허 주파수 대역을 통해 AP에 접속하고, AP가 프레임을 변환하여 유선 분배 시스템으로 전달하는 구조

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **무선 단말 (Station, STA)** | 무선 네트워크 인터페이스를 탑재하여 AP와 결합하고 통신하는 단말 기기 | 스마트폰, 노트북, IoT |
| **무선 접근점 (AP)** | 802.11 무선 프레임과 802.3 이더넷 프레임을 상호 브리지하고 무선 매체 제어 | 무선 라우터 |
| **기본 서비스 세트 (BSS)** | 단일 AP의 무선 커버리지 영역 내에서 수립된 기본 통신 도메인 | BSSID (AP MAC) |
| **분배 시스템 (DS)** | 복수 BSS 간의 핸드오버 및 유선 네트워크 연결을 제공하는 백본망 | 유선 스위칭망 |

#### 한줄 요약
- STA, AP, BSS, 분배 시스템(DS)이 결합하여 유무선 통합 네트워크를 형성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **비콘 프레임(Beacon Frame)**: AP가 자신의 존재, SSID, 지원 전송 속도 및 보안 파라미터를 주기적으로 브로드캐스트하는 L2 관리 프레임.
- **결합(Association)**: 인증이 완료된 단말이 AP와의 데이터 전송 논리 링크를 수립하고 리소스 할당을 완료하는 단계.

</details>

```text
1. 탐색(Scanning): 비콘 프레임 수신(Passive) 또는 Probe Request/Response(Active)
            │
            ▼
2. 인증(Authentication): WPA3-SAE 기반의 사전 공유키 또는 802.1X EAP 인증 수행
            │
            ▼
3. 결합(Association): 대역폭, 채널 폭, MIMO 기능 협상 및 결합(Association ID) 완료
            │
            ▼
4. 4-Way Handshake (802.11i): PTK/GTK 암호화 키 유도 ➔ 암호화 데이터 송수신 개시
```

**동작 원리**

1. **매체 탐색**: 단말이 AP의 비콘 신호를 청취하거나 능동적으로 Probe 프레임을 전송하여 대상 AP 식별
2. **신원 인증**: WPA3(SAE) 핸드셰이크를 통해 비밀번호 검증 및 상호 인증 완료
3. **링크 결합**: 지원 가능한 통신 규격(802.11ax/be 등)과 링크 속도를 협상하여 결합 완료
4. **키 유도 및 통신**: 4-Way Handshake를 거쳐 유니캐스트 암호화 키(PTK)를 생성하고 실제 데이터 전송 수행

#### 한줄 요약
- 비콘 탐색, WPA3 인증, 결합 협상, 4-Way Handshake를 거쳐 보안 통신 채널을 수립한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Wi-Fi 5 (802.11ac)**: 5GHz 전용 대역에서 256-QAM과 DL MU-MIMO를 도입하여 기가비트 무선 속도를 개척한 표준.
- **Wi-Fi 6/6E (802.11ax)**: 2.4/5/6GHz 대역에서 OFDMA, 1024-QAM, BSS Coloring을 도입하여 고밀도 다중 접속 효율을 극대화한 표준.
- **Wi-Fi 7 (802.11be)**: 최대 320MHz 채널 폭, 4096-QAM, MLO 및 16x16 MU-MIMO를 통해 최대 46Gbps 처리량을 지향하는 초고속 저지연 표준.

</details>

| 비교 항목 | Wi-Fi 5 (802.11ac) | Wi-Fi 6/6E (802.11ax) | Wi-Fi 7 (802.11be) |
|:---|:---|:---|:---|
| **지원 주파수 대역** | 5 GHz 전용 | 2.4 GHz, 5 GHz, **6 GHz (6E)** | 2.4 GHz, 5 GHz, 6 GHz |
| **최대 채널 대역폭** | 160 MHz | 160 MHz | **320 MHz** |
| **최고 변조 방식** | 256-QAM | 1024-QAM | **4096-QAM (4K-QAM)** |
| **다중 접속 기술** | OFDM | **OFDMA (자원 단위 RU 분할)** | **OFDMA + Multi-RU** |
| **핵심 다중화 기술** | DL MU-MIMO (최대 4x4) | UL/DL MU-MIMO (최대 8x8) | **MLO (다중 링크 동시 결합)**, 16x16 MIMO |
| **이론상 최대 속도** | 약 6.9 Gbps | 약 9.6 Gbps | **약 46 Gbps** |

#### 한줄 요약
- 802.11ac(단일 속도), 802.11ax(고밀도 OFDMA), 802.11be(초광대역 320MHz 및 MLO)로 진화했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BSS 컬러링(BSS Coloring)**: 동일 채널을 사용하는 인접 BSS의 프레임에 색상 식별자(Color Bit)를 부여하여 다른 BSS의 간섭 신호 무시하고 공간을 재사용하는 기술.
- **에어타임 공평성(Airtime Fairness)**: 저속 단말의 무선 매체 점유 시간 독점을 방지하고 단말별 전파 사용 시간을 균등 분배하는 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동일 채널 인접 AP 간섭으로 인한 처리량 저하 및 지연 증가 | Wi-Fi 6 **BSS Coloring(공간 재사용)** 및 동적 임계치(OBSS_PD) 적용 | 인접 셀 간 간섭 회피 및 공간 재사용을 통한 실효 속도 향상 |
| WPA2 사전 대입 공격(Dictionary Attack) 및 패킷 스니핑 취약점 | **WPA3-Enterprise(192비트)** 및 **WPA3-Personal(SAE 방식)** 의무화 | 오프라인 사전 대입 공격 원천 방어 및 전송 암호화 강화 |
| 레거시 저속 단말(802.11b/g/n)의 긴 전파 점유로 전체 AP 속도 저하 | **에어타임 공평성(Airtime Fairness)** 및 **밴드 스티어링(Band Steering)** 적용 | 고속 단말의 전송 기회 보장 및 고주파수(5G/6GHz) 유도 분산 |

#### 한줄 요약
- BSS Coloring 공간 재사용, WPA3 보안 적용, Airtime Fairness 튜닝으로 무선 품질과 보안성을 극대화한다.

## Ⅶ. 결론

- 고밀도 엔터프라이즈 무선망 구축 시 다중 사용자 환경의 접속 효율을 위해 **Wi-Fi 6(802.11ax)** 를 표준으로 구축하고, 실시간 초저지연 및 초고속 백본이 요구되는 환경에는 **Wi-Fi 7(802.11be)의 MLO 기술**을 단계적으로 도입하되, **WPA3 보안**과 **Airtime Fairness** 최적화를 결합하여 신뢰성 있는 무선 인프라를 달성

#### 한줄 요약
- Wi-Fi 6/7 표준 기술과 대역별 튜닝을 결합하여 고품질·고보안 무선 LAN 환경을 완성한다.
