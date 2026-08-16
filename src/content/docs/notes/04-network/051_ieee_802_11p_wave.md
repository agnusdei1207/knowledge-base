---
sidebar:
  order: 51
  label: "051. IEEE 802.11p WAVE"
  badge:
    text: "기출 • 30%"
    variant: note
title: "IEEE 802.11p WAVE"
date: "2026-08-13T17:20:00+09:00"
tags:
  - "notes-network"
weight: 51
extra:
  question_no: "051"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "설명형: 138회 V2X의 802.11p 하위 기술"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **차량 환경 무선 접속(Wireless Access in Vehicular Environments, WAVE / IEEE 802.11p)**: 5.9GHz 대역 주파수를 사용하여 가입 절차 없이 고속 이동 차량 간(V2V) 및 차량-인프라 간(V2I) 안전 메시지를 교환하는 무선 통신 기술 표준이다.
- **전기전자공학자협회(Institute of Electrical and Electronics Engineers, IEEE)**: IEEE 802.11p 물리/MAC 규격 및 IEEE 1609 상위 표준을 정립한 글로벌 학술 표준화 기구이다.
- **기본 서비스 집합 외부 통신(Outside the Context of a Basic Service Set, OCB)**: 무선 AP 가입 및 결합(Association) 절차를 생략하고 즉시 무선 데이터 프레임을 송수신하는 802.11p 전용 접속 모드이다.

</details>

- 정의/개념: **IEEE 802.11p WAVE(Wireless Access in Vehicular Environments)**는 5.9GHz 무선 주파수 대역에서 가입 접속 절차 없이(OCB 모드) 고속 이동하는 차량 간(V2V) 및 차량-인프라 간(V2I) 초저지연 안전 메시지(WSMP)를 교환하는 차량 전용 단거리 무선 통신 표준 규격이다.
- 배경/필요성: 기존 무선랜(IEEE 802.11a/g)의 BSS 접속 핸드셰이크 및 AP 로밍 과정으로 인한 접속 지연(수초 소요)을 제거하고, 100km/h 이상의 고속 이동 차량 간 10ms 이내의 충돌 회피 메시지 교환을 실현하기 위해 도입되었다.

#### 한줄 요약

- BSS 가입 절차 없이(OCB 모드) 5.9GHz 대역에서 고속 이동 차량 간 초저지연 안전 메시지를 송수신하는 IEEE 802.11p/1609 WAVE 표준 규격.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **직교 주파수 분할 다중화(Orthogonal Frequency-Division Multiplexing, OFDM)**: 서로 직교하는 부반송파를 이용해 데이터를 병렬 전송하는 무선 변조 기술로, 802.11p에서는 10MHz 채널로 변형 채택된다.
- **메가헤르츠(Megahertz, MHz)**: 무선 주파수 대역폭 크기를 나타내는 단위로, 802.11p는 도플러 수용성을 높이기 위해 기존 20MHz 무선랜을 10MHz 반채널(Half-clocked)로 둔감화하여 활용한다.

</details>

- **OCB 모드의 가입 절차 생략**: BSS 인증 없이 채널 접근 후 프레임을 전송한다.
- **10MHz 반채널(Half-clocked) OFDM 변조**: 고속 주행 시 발생하는 심한 도플러 시프트와 다중 경로 지연 확산(Delay Spread)에 견디도록 10MHz 반채널 주파수 규격을 채택한다.
- **IEEE 1609 상위 프로토콜 스택 수용**: 무선 물리/MAC층(802.11p) 위에 1609.2(보안 서명), 1609.3(WSMP 네트워킹), 1609.4(멀티채널 스위칭) 기술이 유기적으로 조합된다.

#### 한줄 요약

- OCB 즉시 프레임 발사, 10MHz 대역폭 OFDM 변조, IEEE 1609 상위 프로토콜 연동을 통한 차량 직접 통신 제공.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **WAVE 단문 메시지 프로토콜(WAVE Short Message Protocol, WSMP)**: IP 프로토콜 오버헤드를 제거하여 기본 안전 메시지(BSM/CAM)를 수ms 이내 초저지연 전달하는 전용 라우팅 프로토콜이다.
- **제어 채널 및 서비스 채널(Control Channel & Service Channel, CCH / SCH)**: 1609.4 규격에 따라 무선 채널을 긴급 제어 전용(CCH)과 일반 서비스 전용(SCH)으로 50ms마다 교번(Switching) 분할하는 채널 구조이다.

</details>

```text
WAVE 프로토콜 스택 아키텍처
├─ 애플리케이션 계층 (Vehicle Safety Apps - BSM / CAM)
├─ 보안 및 네트워킹 계층 (IEEE 1609.2 Security / IEEE 1609.3 WSMP & IP)
├─ 채널 운용 계층 (IEEE 1609.4 Multi-Channel Operation - CCH & SCH)
└─ 무선 물리/매체 제어 계층 (IEEE 802.11p MAC & PHY - 5.9GHz OCB)
```

선의 의미: 상위 서비스 응용이 1609.2 보안 서명 및 1609.3 WSMP 라우팅을 거쳐 1609.4 채널 스위칭에 따라 802.11p 무선 프레임으로 송출되는 계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| IEEE 1609.2 (보안 계층) | 가명 인증서 발급/검증, ECDSA 전자서명 부가 및 무결성 확인 |
| IEEE 1609.3 (네트워킹 계층) | 초저지연 WSMP 프로토콜 및 일반 인터넷 통신을 위한 IPv6 프로토콜 제공 |
| IEEE 1609.4 (채널 운용 계층) | 단일 무선 트랜시버로 CCH(제어 채널)와 SCH(서비스 채널)를 50ms 시분할(TDM) 교번 운용 |
| IEEE 802.11p MAC (매체 제어) | OCB 모드 동작 및 CSMA/CA 기반 무선 매체 접속 제어, QoS 우선순위 큐(EDCA) 지원 |
| IEEE 802.11p PHY (물리 계층) | 5.9GHz 대역(5.850~5.925GHz)에서 10MHz 대역폭 OFDM 신호 변복조 및 무선 송수신 |

#### 한줄 요약

- IEEE 1609.2(보안)과 1609.3(WSMP)이 상위 메시지를 처리하고, 1609.4(채널)가 CCH/SCH를 스위칭하며, 802.11p가 OCB 무선 전송을 수행하는 구조.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **최신성(Freshness & Anti-Replay)**: 수신된 무선 프레임의 시각정보와 시퀀스를 판별해 재전송 및 지연 메시지를 차단하는 무결성 속성이다.
- **서명 OCB 프레임(Signed OCB Frame)**: IEEE 1609.2 보안 서명이 부착되어 802.11p OCB 헤더로 포장된 차량 무선 프레임이다.

</details>

```text
1. 차량 온보드 센서 기반 기본 안전 메시지 생성 (BSM Generation)
      │
      v
2. IEEE 1609.2 가명 인증서 전자서명 부가 (Security Sign)
      │
      v
3. IEEE 1609.3 WSMP 헤더 캡슐화 및 네트워크 라우팅 (WSMP Encoding)
      │
      v
4. IEEE 1609.4 제어 채널(CCH 178) 스위칭 타임슬롯 지정 (Channel Sync)
      │
      v
5. IEEE 802.11p OCB 5.9GHz 무선 프레임 CSMA/CA 발사 (PHY Transmission)
```

### 동작 원리

1. 차량 온보드 센서 기반 기본 안전 메시지 생성: 상태 수집
2. IEEE 1609.2 가명 인증서 전자서명 부가: 송신자 서명
3. IEEE 1609.3 WSMP 헤더 캡슐화 및 네트워크 라우팅: 포장
4. IEEE 1609.4 제어 채널 스위칭 타임슬롯 지정: 채널 선택
5. IEEE 802.11p OCB 무선 프레임 CSMA/CA 발사: 전송

#### 한줄 요약

- 안전 메시지 생성, 1609.2 서명, 1609.3 WSMP 캡슐화, 1609.4 CCH 타임슬롯 지정 및 802.11p OCB 프레임 발사 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **WAVE OCB(WAVE OCB Mode)**: 무선랜 AP와의 핸드셰이크 접속 과정이 전면 제거되어 100km/h 이상의 고속 이동 상태에서도 즉시 프레임을 교환하는 접속 방식이다.
- **인프라 와이파이(Infrastructure Wi-Fi)**: AP와 4-Way Handshake를 거쳐 무선 연결(BSS)을 맺고 데이터를 수송하는 일반 무선랜 접속 방식이다.

</details>

| 비교 항목 | **IEEE 802.11p WAVE (OCB)** | **일반 인프라 무선랜 (IEEE 802.11a/g/n)** |
|:---|:---|:---|
| 접속 모드 | OCB 모드 (BSS 핸드셰이크 결합 생략) | BSS 모드 (AP 접속, 가입, WPA 보안 인증) |
| 무선 채널 대역폭 | 10MHz 반채널 (도플러 및 지연 확산 강인) | 20MHz / 40MHz 표준 광대역 |
| 무선 전송 지연 | 가입 절차 생략•채널 경합 지연 | AP 접속•보안 협상 지연 포함 |
| 주요 네트워킹 | WSMP (WAVE Short Message Protocol) | IPv4 / IPv6 패킷 프로토콜 중심 |
| 무선 이동성 | 100km/h 이상 고속 이동 차량 V2V/V2I 지원 | 보행자 수준의 저속 이동 및 AP 간 로밍 지연 |

> 요약: 일반 무선랜 대비 802.11p WAVE는 BSS 가입 생략(OCB), 10MHz 반채널 변조 및 WSMP 프로토콜을 통해 고속 이동 차량 간 초저지연 통신 지원.

#### 한줄 요약

- 일반 무선랜 대비 802.11p WAVE는 BSS 가입 생략(OCB), 10MHz 반채널 변조 및 WSMP 프로토콜을 통해 고속 이동 차량 간 초저지연 통신 지원.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **채널 경쟁(Channel Contention / CSMA/CA)**: 동일 5.9GHz 무선 채널을 주변 차량들이 동시에 사용하려고 경쟁할 때 발생하는 무선 패킷 충돌 현상이다.
- **인증서 폐기 정보(Certificate Revocation List, CRL)**: 만료 전 실효된 가명 인증서 목록을 OBU 단말에 배포하여 위장 메시지를 거부하게 하는 기술이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| CCH/SCH 스위칭 지연 | 1609.4 채널 교번 시 50ms 대기 지연 발생 | Dual-radio 트랜시버 설치 (CCH/SCH 동시 상시 채널 수용) | 스위칭 대기 시간 제거 및 안전 메시지 상시 수신 |
| 고밀도 차량 CSMA/CA 충돌 | 차량 수백 대 밀집 시 CSMA/CA 채널 경쟁 폭증 | EDCA 무선 우선순위 큐 적용 및 파워 자동 제어 | 긴급 제동 메시지(BSM) 무선 손실 방지 |
| 서명 검증 처리 지연 | ECDSA 비대칭키 전자서명 검증 연산 오버헤드 | OBU 내부 HSM(하드웨어 보안 모듈) 암호 가속기 탑재 | 10ms 내 서명 검증 완료 및 ADAS 통제 반영 |
| CCH Guard Interval 오차 | 장치 간 GPS 시각 동기 오차로 채널 전환 믹스 | IEEE 1588 / GPS 수신기 기반 정밀 시각 동기화 | CCH/SCH 채널 간 무선 신호 중첩 간섭 방지 |

#### 한줄 요약

- CCH/SCH 교번 타임슬롯 동기화, ECDSA 서명 검증 가속 하드웨어 적용, CSMA/CA CW(Contention Window) 동적 조절로 WAVE 품질 확보.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **안전 메시지 기한(Safety Message Latency Deadline)**: 서비스별 안전 판단 전에 메시지 처리를 끝내야 하는 시간 한도이다.

</details>

- 기존 WAVE 연동은 **802.11p OCB•IEEE 1609** 적용

#### 한줄 요약

- OCB 모드 기반 가입 즉시 전송 및 IEEE 1609 WSMP 기반 초저지연 안전 통신 체계 구현 필수.
