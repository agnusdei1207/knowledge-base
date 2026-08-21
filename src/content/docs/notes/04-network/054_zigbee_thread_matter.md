---
sidebar:
  order: 54
  label: "054. Zigbee, Thread, Matter"
  badge:
    text: "기출 · 30%"
    variant: note
title: "스마트홈 IoT 통신 및 응용 계층 표준 : Zigbee, Thread, Matter"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 54
extra:
  question_no: "054"
  source_status: "기출"
  source_history: "131회"
  priority: 30
  priority_note: "IEEE 802.15.4, 6LoWPAN/IPv6 기반 Thread, CSA Matter 응용 표준 및 상호운용성"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Zigbee(지그비)**: IEEE 802.15.4 물리/MAC 계층 기반의 저전력 무선 메시(Mesh) 네트워크 기술로, 비-IP(Non-IP) 프로토콜 스택을 사용하여 별도의 전용 게이트웨이(허브)를 통해 상위망과 연동하는 1세대 스마트홈 기술.
- **Thread(스레드)**: IEEE 802.15.4 무선 매체 위에서 6LoWPAN 및 IPv6를 네이티브로 지원하여, 허브 종속 없이 저전력 노드에 종단간(End-to-End) IP 라우팅을 제공하는 2세대 메시 네트워크 표준.
- **Matter(매터)**: Connectivity Standards Alliance(CSA)가 주도하여 Wi-Fi, Ethernet, Thread 전송 계층 위에서 동작하도록 표준화한 개방형 애플리케이션 계층 스마트홈 상호운용성 프로토콜.

</details>

- 정의/개념: 무선 물리 계층(IEEE 802.15.4) 및 저전력 IPv6 메시 라우팅(**Thread**)을 기반으로, 제조사 생태계에 구애받지 않고 단일 공통 프로토콜로 기기를 제어하는 **CSA Matter 응용 계층 표준 아키텍처**
- 배경/필요성: 기존 제조사별 독점 허브 및 비표준 프로토콜로 인한 기기 간 비호환성(파편화)을 해소하고, IP 네이티브 통신을 통한 전역 상호운용성과 로컬 제어 보안성을 확보할 요구

#### 한줄 요약
- 비-IP Zigbee와 저전력 IPv6 Thread 전송 기반 위에 공통 Matter 응용 계층을 융합하여 기기 상호운용성을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **6LoWPAN(IPv6 over Low-Power Wireless Personal Area Networks)**: 128바이트의 작은 패킷 크기를 갖는 IEEE 802.15.4 프레임 상에서 128비트 IPv6 헤더를 적응 계층(Adaptation Layer) 압축을 통해 효율적으로 전송하는 표준 (RFC 4944/6282).
- **다중 관리자(Multi-Admin)**: Matter 표준에서 특정 기기를 애플 홈(Apple Home), 삼성 스마트싱스(SmartThings), 구글 홈(Google Home) 등 복수의 제어 플랫폼에 동시 등록하여 제어할 수 있는 기능.

</details>

- **Zigbee의 폐쇄적 비-IP 구조**: 전용 게이트웨이의 L7 프로토콜 변환에 전적으로 의존하며 타사 에코시스템과의 직접 통신 불가
- **Thread의 네이티브 IPv6 메시 통신**: **6LoWPAN** 기반으로 센서 노드까지 엔드투엔드 IPv6 주소를 할당하여 단일 장애점(SPOF) 없는 자가 치유(Self-Healing) 메시망 구축
- **Matter의 전송 계층 독립성 및 보안성**: TCP/UDP 기반 IPv6 인프라(Wi-Fi, Ethernet, Thread) 위에서 동작하며, 기기 증명서(DAC)와 **PASE/CASE** 암호화 세션으로 종단 보안 보장

#### 한줄 요약
- 6LoWPAN 기반 IPv6 직결성, 전송 매체 독립적 Matter 공통 데이터 모델, Multi-Admin 동시 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스레드 보더 라우터(Thread Border Router)**: 802.15.4 기반 Thread 메시망과 일반 Wi-Fi/Ethernet LAN 간에 IPv6 패킷을 변환 없이 양방향 라우팅하는 경계 장치.
- **매터 브리지(Matter Bridge)**: 비-Matter 레거시 기기(Zigbee, Z-Wave)의 명령어를 Matter 데이터 모델로 매핑하여 Matter 패브릭 내에서 제어 가능하도록 중계하는 어댑터.

</details>

```text
[ Matter 컨트롤러 (스마트폰 / 스마트 스피커: Multi-Admin) ]
   │ (Matter 공통 데이터 모델 / IPv6)
   ├───────────────────────────────┬───────────────────────────────┐
   ▼ (Wi-Fi / Ethernet LAN)        ▼ (Matter Bridge)               ▼ (Thread Border Router)
[ 고대역폭 Matter 기기 ]       [ 레거시 Zigbee 기기 ]          [ Thread 메시 네트워크 ]
 ├─ 스마트 TV                   ├─ 비-IP Zigbee 센서           ├─ 저전력 Thread 전구
 └─ 보안 카메라                 └─ 전용 게이트웨이 연동         └─ 저전력 도어락 (IPv6)
```

선의 의미: 제어 단말이 Matter 공통 프로토콜을 통해 Wi-Fi 기기, Matter 브리지를 거친 Zigbee 기기, 보더 라우터를 통한 Thread 기기를 단일 인터페이스로 제어하는 구조

| 계층 | 기술 표준 | 책임 및 프로토콜 스택 | 주관 단체 |
|:---|:---|:---|:---|
| **애플리케이션 계층** | **Matter** | 공통 디바이스 데이터 모델, 클러스터 제어, 기기 인증(DAC), 멀티 어드민 | CSA (Connectivity Standards Alliance) |
| **네트워크/전송 계층** | **Thread / Wi-Fi** | IPv6, 6LoWPAN, UDP, CoAP, 자가 치유 메시 라우팅 (MLE/RPL) | Thread Group, Wi-Fi Alliance |
| **물리/데이터링크 계층** | **IEEE 802.15.4 / 802.11** | 2.4GHz 무선 변복조, O-QPSK, DSSS, CSMA/CA 매체 접근 제어 | IEEE 802 LAN/MAN 표준위원회 |

#### 한줄 요약
- Matter 응용 계층, Thread/Wi-Fi 전송 계층, IEEE 802.15.4/802.11 물리 계층이 결합하여 생태계를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **커미셔닝(Commissioning)**: 신규 IoT 기기를 암호화된 절차를 통해 로컬 네트워크(Wi-Fi/Thread)에 안전하게 조인시키고 Matter 패브릭(Fabric)의 제어 권한을 부여하는 초기 등록 과정.
- **기기 증명서(Device Attestation Certificate, DAC)**: 기기 제조 시 하드웨어 보안 칩에 저장되는 공인 X.509 인증서로, CSA 공인 인증 기기임을 증명하는 암호학적 신원.

</details>

```text
1. 사용자가 스마트폰 앱으로 신규 기기의 QR 코드(온보딩 페이로드) 스캔
            │
            ▼
2. BLE(Bluetooth Low Energy) 통신을 통해 송수신 간 PASE(비밀번호 인증 세션) 암호화 수립
            │
            ▼
3. 컨트롤러가 기기의 DAC(기기 증명서) 유효성 및 루트 CA 서명 검증 ➔ 정품 기기 인증
            │
            ▼
4. 컨트롤러가 Wi-Fi 또는 Thread 네트워크 접속 자격 증명(SSID/비밀번호)을 기기로 안전하게 전송
            │
            ▼
5. 기기가 Thread/Wi-Fi 메시망에 접속 ➔ Matter 패브릭(Fabric) 등록 완료 및 IPv6 제어 개시
```

**동작 원리**

1. **근거리 탐색**: BLE를 통해 전원이 켜진 주변 미등록 기기를 즉각 발견
2. **세션 암호화**: SPAKE2+ 프로토콜 기반 PASE 세션을 형성하여 무선 도청 방지
3. **신원 검증**: 기기 내부 보안 칩(Secure Element)의 DAC를 조회하여 위조 기기 차단
4. **패브릭 조인**: 로컬 IPv6 네트워크 크리덴셜을 주입하여 Matter 노드로서 상호 운용 제어 활성화

#### 한줄 요약
- QR 스캔, BLE PASE 암호화 수립, DAC 신원 검증, 자격 증명 주입, Matter 패브릭 가입 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **패브릭(Fabric)**: 동일한 루트 인증 기관(Root CA)을 공유하며 보안 신뢰 관계를 형성한 Matter 기기들의 논리적 제어 네트워크.

</details>

| 비교 항목 | Zigbee (1세대) | Thread (2세대) | Matter (3세대) |
|:---|:---|:---|:---|
| **동작 계층** | **L1 ~ L7 풀스택 (통합 프로토콜)** | **L3 ~ L4 (네트워크/전송 계층)** | **L7 (애플리케이션 계층)** |
| **IP 프로토콜 지원** | **미지원 (Non-IP, 전용 허브 필수)** | **네이티브 IPv6 지원 (6LoWPAN)** | **IPv6 기반 상위 전송망 독립** |
| **기기간 상호운용성** | 제조사별 프로파일 상이로 파편화 | 네트워크 계층 통일 (앱 계층 불일치) | **제조사 무관 100% 완전 상호운용** |
| **네트워크 구조** | Coordinator 기반 트리/메시 | Border Router 기반 자가 치유 메시 | Thread, Wi-Fi, Ethernet 통합 패브릭 |
| **인증 및 보안** | 네트워크 공유 키(Pre-Shared Key) | DTLS, AES-128 MAC 보안 | **공개키 기반 구조(PKI), DAC, CASE** |

#### 한줄 요약
- Zigbee는 비-IP 통합 스택, Thread는 저전력 IPv6 전송 스택, Matter는 전송망 독립 공통 응용 스택이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **단일 장애점(SPOF) 방지**: Thread 보더 라우터를 가정 내 복수 기기(스마트 TV, 스피커)에 분산 활성화하여 특정 장비 전원 차단 시에도 메시망이 무중단 유지되도록 구성하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기구축된 대규모 비-IP Zigbee 인프라와 신규 Matter 에코시스템 간 통신 단절 | **Matter Bridge (Zigbee-to-Matter 게이트웨이)** 어댑터 도입 | 기존 기기 교체 없는 레거시 인프라 수용 및 투자 보호 |
| 단일 Thread Border Router 전원 오프 시 스마트홈 메시 네트워크 단절 | **다중 보더 라우터(Multiple Border Routers)** 자동 페일오버 구성 | 경계 라우터 장애 시 자동 경로 우회 및 고가용성 보장 |
| 비인가 위조 IoT 기기 접속으로 인한 스마트홈 네트워크 침해 및 프라이버시 누출 | 커미셔닝 시 **DAC(기기 증명서) 공인 인증 검증** 의무화 | 비인가 디바이스 네트워크 진입 차단 및 제로 트러스트 보안 확보 |

#### 한줄 요약
- Matter Bridge로 레거시를 수용하고, 다중 보더 라우터로 가용성을 확보하며, DAC 검증으로 위조 기기를 차단한다.

## Ⅶ. 결론

- 파편화된 스마트홈 및 IoT 시장의 기기 호환성을 완성하기 위해 **IPv6 기반 Thread 메시 네트워크** 와 **CSA Matter 애플리케이션 표준**을 차세대 아키텍처로 채택하되, 기존 인프라 전환을 위해 **Matter Bridge 기술**을 적용하고 **다중 보더 라우터 이중화**와 **DAC PKI 보안 인증**을 통합 구축하여 안전하고 확장성 있는 스마트홈 인프라를 구현

#### 한줄 요약
- Thread IPv6 메시 인프라와 Matter 공통 응용 프로토콜을 결합하여 표준화된 스마트홈 환경을 완성한다.
