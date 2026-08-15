---
sidebar:
  order: 50
  label: "050. C-V2X와 DSRC 비교 (C-V2X DSRC)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "C-V2X와 DSRC 비교 (C-V2X DSRC)"
date: "2026-08-13T17:18:00+09:00"
tags:
  - "notes-network"
weight: 50
extra:
  question_no: "050"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "비교형: 138회 C-V2X•DSRC 구성축"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **셀룰러 차량·사물 통신(Cellular Vehicle-to-Everything, C-V2X)**: 3GPP 표준 기반의 셀룰러 무선 기술(PC5 Sidelink 및 Uu Cellular)을 사용하여 차량 통신을 수행하는 기술이다.
- **전용 단거리 통신(Dedicated Short-Range Communications, DSRC)**: IEEE 802.11p 및 IEEE 1609(WAVE) 표준을 기반으로 5.9GHz 비면허 대역에서 근거리 무선 전송을 수행하는 기술이다.
- **차량·사물 통신(Vehicle-to-Everything, V2X)**: 차량이 도로상의 차량, 인프라, 보행자, 네트워크와 정보를 주고받는 C-ITS 핵심 통신 기술 체계이다.
- **차량 환경 무선 접속(Wireless Access in Vehicular Environments, WAVE)**: IEEE 802.11p 물리/MAC 계층과 IEEE 1609 상위 프로토콜로 구성된 북미형 DSRC 기술의 대명사이다.

</details>

- 정의/개념: **C-V2X(Cellular V2X)**와 **DSRC(Dedicated Short-Range Communications)**는 자율주행 및 지능형 교통 체계(C-ITS)를 구축하기 위한 양대 무선 V2X 기술 표준으로, 3GPP 기반의 이동통신 연동형(C-V2X) 방식과 IEEE 802.11p/WAVE 기반의 비면허 단거리 무선 방식(DSRC)으로 구분된다.
- 배경/필요성: 각국의 주파수 분배 정책, 기존 구축된 WAVE 인프라 호환성, 그리고 5G/6G 셀룰러 표준 진화의 기술 경쟁 속에서 자율주행 안전성 확보를 위한 최적의 C-ITS 무선 기술 선정이 필요하여 제정되었다.

#### 한줄 요약

- 3GPP 이동통신 기반의 셀룰러 무선 기술(C-V2X)과 IEEE 802.11p 무선랜 기반 단거리 무선 기술(DSRC/WAVE)을 비교 분석하는 C-ITS 무선 기술 표준 체계.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **기본 서비스 집합 외부 통신(Outside the Context of a Basic Service Set, OCB)**: AP 접속 과정(BSS Handshake) 없이 무선 채널상에서 데이터를 즉시 송수신하는 802.11p 무선 접속 모드이다.
- **반송파 감지 다중 접속/충돌 회피(Carrier Sense Multiple Access with Collision Avoidance, CSMA/CA)**: 채널이 비어 있는지 감지한 후 전송하는 경합 방식 무선 매체 접근 제어 프로토콜이다.

</details>

- **C-V2X (3GPP 표준)**: 자원 배정 기반 PC5와 Uu 경로를 활용한다.
- **DSRC / WAVE (IEEE 표준)**: CSMA/CA 방식의 채널 경합 기반으로 작동하며, OCB 모드를 채택하여 접속 지연 없이 5.9GHz 대역에서 단거리 패킷을 직접 브로드캐스팅한다.
- **고밀도 환경 성능 격차**: 차량 밀집 구역에서 DSRC는 CSMA/CA 패킷 충돌로 수신 실패율이 급증하는 반면, C-V2X는 주파수 자원 분할 스케줄링을 통해 높은 수신 성공률(PDR)을 유지한다.

#### 한줄 요약

- C-V2X는 셀룰러 표준 진화 및 스케줄링 자원 할당 제공, DSRC/WAVE는 단순 구조 및 검증된 CSMA/CA 경합 기반 전송 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **차량 탑재 장치(On-Board Unit, OBU)**: C-V2X 또는 DSRC 무선 모듈이 탑재되어 차량 안전 메시지를 송수신하는 단말이다.
- **노변 장치(Roadside Unit, RSU)**: V2I 신호를 수신하고 관제 센터와 연동하는 장치이다.
- **차량·사물 공개키 기반구조(V2X Public Key Infrastructure, V2X PKI / SCMS)**: C-V2X 및 DSRC 통신에 공통 적용되는 가명 인증서 발급 및 무결성 검증 체계이다.

</details>

```text
V2X 무선 표준 아키텍처 비교
├─ C-V2X 구성축 (3GPP C-V2X Architecture)
│  ├─ 차량 단말 및 노변 장치 (OBU & C-V2X RSU)
│  ├─ PC5 사이드링크 무선 채널 (Mode 3 / Mode 4 Sidelink)
│  └─ Uu 인터페이스 및 5G 코어 (gNB & 5GC V2X Control)
└─ DSRC 구성축 (IEEE 802.11p / WAVE Architecture)
   ├─ WAVE 단말 및 노변 장치 (WAVE OBU & WAVE RSU)
   ├─ 802.11p PHY/MAC 무선 채널 (5.9GHz CSMA/CA)
   └─ IEEE 1609 상위 프로토콜 (WAVE Short Message Protocol - WSMP)
```

선의 의미: C-V2X는 3GPP PC5/Uu 및 코어망을 구성축으로 하고, DSRC는 IEEE 802.11p PHY/MAC 및 IEEE 1609 WSMP 프로토콜을 구성축으로 활용하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| C-V2X OBU / RSU | 3GPP PC5 사이드링크 모듈을 내장하여 10ms 이내 초저지연 안전 메시지 스케줄링 전송 |
| DSRC OBU / RSU | IEEE 802.11p 무선 칩셋을 내장하여 CSMA/CA 경합 방식으로 5.9GHz 패킷 브로드캐스팅 |
| C-V2X 5G 코어 및 Uu | gNB 기지국 및 5GC 연동을 통해 V2N 광역 교통 정보 및 C-ITS 다중 센서 오프로딩 제공 |
| IEEE 1609 WSMP | DSRC/WAVE 환경에서 IP 헤더 오버헤드를 줄인 전용 웨이브 단문 프로토콜 전송 |
| 공통 SCMS PKI | C-V2X와 DSRC 무선 파형에 상관없이 공통 가명 인증서 발급 및 전자서명 검증 수행 |

#### 한줄 요약

- C-V2X는 PC5/Uu 이중 채널과 3GPP 코어를 구성축으로 활용하고, DSRC는 802.11p PHY/MAC과 IEEE 1609 WSMP를 구성축으로 활용하는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **사이드링크(Sidelink / PC5)**: 3GPP 표준에서 정의한 기지국을 경유하지 않는 단말 간 직접 무선 통신 통로이다.

</details>

```text
C-ITS 환경•주파수 정책 분석
      │
      ├─ 기존 WAVE 장비 호환 ──────────── DSRC 방식
      │                                         │
      │                                         └─ CSMA/CA 채널 경합 전송
      │
      └─ 셀룰러 연동•자원 스케줄링 ────── C-V2X 방식
                                                │
                                                └─ 반송파 자원 스케줄링 전송
      │
      v
SCMS PKI 가명 인증서 서명 적용
      │
      v
충돌 위험 알림 및 ADAS 제어 반영
```

### 동작 원리

- **C-ITS 환경•주파수 정책 분석**: 기존 인프라 확인
- **DSRC 방식**: WAVE 호환과 단순 직접 통신 적용
- **C-V2X 방식**: 셀룰러 연동과 자원 스케줄링 적용
- **SCMS PKI 가명 인증서 서명 적용**: 송신자 검증
- **충돌 위험 알림 및 ADAS 제어 반영**: 안전 정보 전달

#### 한줄 요약

- 정책 분석, DSRC(CSMA/CA) 또는 C-V2X(스케줄링) 선정, SCMS PKI 보안 검증 및 ADAS 제어 반영으로 이어지는 비교 실행 흐름.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **3세대 파트너십 프로젝트(3rd Generation Partnership Project, 3GPP)**: 5G/6G 등 이동통신 기술 표준 체계를 주도하는 글로벌 표준화 기구이다.
- **전기전자공학자협회(Institute of Electrical and Electronics Engineers, IEEE)**: 802.11 무선랜 및 802.11p WAVE 규격을 주도하는 국제 학술·표준 기구이다.

</details>

| 비교 항목 | **C-V2X (Cellular V2X)** | **DSRC (WAVE / 802.11p)** |
|:---|:---|:---|
| 기술 표준 체계 | 3GPP (Rel-14/15/16/17+) | IEEE (802.11p / IEEE 1609 규격) |
| 무선 액세스 방식 | SC-FDMA / OFDMA (스케줄링 자원 배정) | CSMA/CA (경합 방식 채널 접근) |
| 전송 거리 및 신뢰도 | 최대 450m 이상 / 고밀도 지역 수신율 높음 | 약 300m 이내 / 차량 밀집 시 무선 충돌 폭증 |
| 커버리지 연동 | PC5(직접) + Uu(5G 셀룰러) 광역 통합 | 전용 단거리 통신(DSRC RSU 경유 한정) |
| 미래 표준 진화 | NR-V2X 계열로 발전 | IEEE 802.11bd 계열로 발전 |

> 요약: C-V2X는 스케줄링 자원 할당, 5G/6G 기술 지속 진화 및 높은 고밀도 수신율을 제공하고, DSRC는 검증된 단순 구조와 CSMA/CA 방식을 제공.

#### 한줄 요약

- C-V2X는 스케줄링 자원 할당, 5G/6G 기술 지속 진화 및 높은 고밀도 수신율을 제공하고, DSRC는 검증된 단순 구조와 CSMA/CA 방식을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **백분위수(Percentile Latency / 99th Percentile)**: 무선 지연시간 측정값 중 상위 99% 차량까지 보장되는 수신 완료 시간 수치이다.
- **전달 성능(Message Delivery Performance)**: 도심 밀집 환경에서 안전 패킷의 수신 성공률(PDR)과 지연시간 수치 지표이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| DSRC 고밀도 무선 충돌 | 도심 차량의 CSMA/CA 경합 | C-V2X 또는 802.11bd 성능 시험 | 충돌•지연 위험 비교 |
| C-V2X 무선 칩셋 원가 | DSRC 대비 C-V2X 칩셋 및 모뎀 단가 비쌈 | C-V2X/5G 통합 칩셋 단말 적용 및 구내 보조금 | 단말 보급률 향상 및 C-ITS 생태계 활성화 |
| 99th Percentile 지연 증가 | 주파수 간섭•혼잡 | 우선순위 자원과 혼잡 제어 | 꼬리 지연 완화 |
| 이종 표준 호환 실패 | DSRC•C-V2X 무선 방식 불일치 | 듀얼 모드 RSU•OBU 단계 배치 | 전환기 통신 공백 완화 |

#### 한줄 요약

- 고밀도 전파 시뮬레이션 기반 기술선정, 99th Percentile 수신 지연 검증, SCMS PKI 호환 모듈 구축으로 V2X 인프라 실무 안정성 완성.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **진화 경로(Evolutionary Path)**: C-ITS 무선망이 5G-V2X 및 6G-V2X로 무손실 지속 업그레이드될 수 있는 기술적 진화 수용성이다.

</details>

- 기존 WAVE 호환은 **DSRC**, 셀룰러 연동은 **C-V2X** 선택

#### 한줄 요약

- 5G/6G 지속 진화성이 우수한 C-V2X 중심 통신망 구축 및 하이브리드 RSU/OBU 도입 필수.
