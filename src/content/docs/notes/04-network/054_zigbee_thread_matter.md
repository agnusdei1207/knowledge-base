---
sidebar:
  order: 54
  label: "054. Zigbee, Thread, Matter"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Zigbee, Thread, Matter"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-network"
weight: 54
extra:
  question_no: "054"
  source_status: "기출"
  source_history: "131회"
  priority: 30
  priority_note: "비교•설계형: 131회 Matter•Thread 연계"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **지그비(Zigbee)**: IEEE 802.11b/g 기반 2.4GHz 무선 주파수에서 비-IP 고유 애플리케이션 프로파일과 메시 네트워크를 제공하는 초저전력 IoT 통신 표준이다.
- **스레드(Thread)**: IEEE 802.15.4 기반의 6LoWPAN 기술을 채택하여 저전력 기기들에 네이티브 IPv6 통신을 보장하는 무선 메시 전송 네트워크 표준이다.
- **매터(Matter)**: IP 기반(Wi-Fi, Ethernet, Thread) 위에서 동작하며 제조사 브랜드에 상관없이 스마트홈 기기 간 100% 호환을 보장하는 최상위 애플리케이션 상호 운용성 표준이다.
- **인터넷 프로토콜 버전 6(Internet Protocol version 6, IPv6)**: 128비트 대용량 IP 주소 체계로, 저전력 IoT 기기에 개별 글로벌 IP를 부여하는 핵심 전송 규격이다.
- **사물인터넷(Internet of Things, IoT)**: 센서, 가전, 기계들이 무선 네트워크로 연결되어 상호 데이터를 교환하고 제어되는 지능형 플랫폼 환경이다.

</details>

- 정의/개념: **Zigbee, Thread, Matter**는 스마트홈 및 스마트빌딩 IoT 구축을 위한 무선 네트워크 및 애플리케이션 표준 기술군으로, 비-IP 기반 저전력 메시망(**Zigbee**), IPv6 기반 저전력 전송망(**Thread**), 그리고 최상위 멀티 벤더 스마트홈 애플리케이션 상호 운용성 표준(**Matter**)으로 구별된다.
- 배경/필요성: 기존 스마트홈 기기 간 제조사 전용(Proprietary) 응용 프로토콜 파편화로 인한 상호 운용성 부재, 고유 게이트웨이 필수 요구 및 음성 비서 생태계 고립 문제를 극복하기 위해 CSA(Connectivity Standards Alliance) 주도로 제정되었다.

#### 한줄 요약

- 저전력 비-IP 메시망(Zigbee), IEEE 802.15.4 기반 IPv6 전송망(Thread), 멀티 벤더 스마트홈 애플리케이션 상호 운용성 표준(Matter)으로 이루어진 IoT 표준 아키텍처.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **전기전자공학자협회(Institute of Electrical and Electronics Engineers, IEEE)**: IEEE 802.15.4 무선 물리/MAC 계층 표준 규격을 정립한 국제 표준화 기구이다.
- **블루투스 저에너지(Bluetooth Low Energy, BLE)**: 스마트폰과 신규 Matter/Thread 기기 간 초기 커미셔닝(Commissioning) 보안 세션 형성에 활용되는 근거리 무선 규격이다.

</details>

- **Zigbee (비-IP 기반 독자 메시)**: IEEE 802.15.4 무선층 위에서 자체 메시 네트워크와 응용 프로파일(ZCL)을 사용하여 전용 게이트웨이가 필수적으로 요구된다.
- **Thread (네이티브 IPv6 저전력 메시)**: 6LoWPAN 기술을 적용하여 802.15.4 무선 장치에 네이티브 IPv6 주소를 부여하고, 단일 장애점(SPOF)이 없는 스레드 경계 라우터(Thread Border Router)를 통해 IP망과 직결된다.
- **Matter (IP 기반 애플리케이션 융합)**: Ethernet, Wi-Fi 및 Thread 네트워크 레이어 위에서 공통 데이터 모델(Data Model)을 제공함으로써 삼성, 애플, 구글 등 이종 플랫폼 간 기기를 100% 호환 제어한다.

#### 한줄 요약

- Zigbee의 고유 프로파일 및 비-IP 메시망, Thread의 저전력 6LoWPAN/IPv6 메시망, Matter의 IP 기반 멀티 벤더 통합 앱 및 PKI 보안 수용.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **Thread 경계 라우터(Thread Border Router)**: 저전력 802.15.4 Thread 메시망과 외부 일반 유무선 IPv6 네트워크(Wi-Fi/Ethernet) 사이에서 패킷을 패키징·라우팅하는 장치이다.
- **Matter 브리지(Matter Bridge)**: IP 통신을 직접 지원하지 않는 기존 비-IP 기기(Zigbee, Z-Wave)의 데이터 모델과 명령을 Matter 표준 포맷으로 상호 변환해 주는 장치이다.

</details>

```text
Matter 및 Thread/Zigbee 연동 아키텍처
├─ 응용 상호운용 계층 (Matter Application Layer - Data Model & Fabric)
├─ IP 및 네트워크 전송 계층 (IP Network Transport - Wi-Fi / Ethernet / Thread)
│  ├─ 스레드 경계 라우터 (Thread Border Router)
│  └─ 스레드 매터 기기 (Thread Matter Node)
└─ 비-IP 레거시 변환 계층 (Legacy Conversion Layer)
   └─ 매터 브리지 (Matter Bridge ── Zigbee Device)
```

선의 의미: Matter 애플리케이션 계층이 Wi-Fi 및 Thread 경계 라우터를 거치는 IPv6망 위에서 운용되며 Matter 브리지를 통해 레거시 Zigbee 기기를 수용하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| Matter 컨트롤러 / 패브릭 | 스마트홈 제어 권한을 가진 단말(스마트폰, 월패드)로, 기기 가입을 인가하고 Matter 명령 수송 |
| Thread 경계 라우터 | Thread 메시 노드의 802.15.4 IPv6 패킷을 사내 Wi-Fi/Ethernet 라우터 패킷으로 직결 라우팅 |
| Thread Matter 기기 | IEEE 802.15.4 무선과 Thread/IPv6 전송망 및 Matter 데이터 모델을 모두 탑재한 저전력 스마트 기기 |
| Matter 브리지 (Bridge) | Zigbee 노드의 전용 속성(ZCL) 및 명령을 Matter 클러스터 모델로 1:1 양방향 실시간 매핑 변환 |
| 레거시 Zigbee 노드 | 기존 비-IP 지그비 무선망으로 작동하며 Matter 브리지에 매핑되어 상위 시스템 제어 수용 |

#### 한줄 요약

- Matter 애플리케이션 계층이 Wi-Fi 및 Thread 경계 라우터를 거치는 IPv6망 위에서 운용되며 Matter 브리지를 통해 레거시 Zigbee 기기를 수용하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **커미셔닝(Commissioning)**: 신규 IoT 기기를 스마트홈 네트워크에 안전하게 등록하고 인증서 및 자격 증명(Credentials)을 부여하는 초기 설정 절차이다.
- **기기 증명서(Device Attestation Certificate, DAC)**: 제조사가 생산 시 기기에 주입한 고유 PKI 인증서로, Matter 정식 인증 기기임을 검증하는 증명서이다.
- **빠른 응답 코드(Quick Response Code, QR Code)**: 기기 표면에 인쇄된 QR 코드를 통해 커미셔닝 시 필요한 기기 식별값 및 페어링 코드를 스마트폰으로 수신하는 기법이다.

</details>

```text
1. BLE 통신 및 QR Code 스캔 기반 기기 탐색 (BLE Discovery)
      │
      v
2. PASE 암호화 세션 수립 및 보안 채널 형성 (PASE Session Setup)
      │
      v
3. 제조사 DAC(Device Attestation Certificate) 기기 무결성 검증 (DAC Verification)
      │
      ├─ 검증 실패 ---- 커미셔닝 차단 (Commissioning Reject)
      └─ 검증 성공
            │
            v
      4. 운영 인증서(NOC) 및 Thread/Wi-Fi 자격 증명 발급 (NOC & Credentials)
            │
            v
      5. IPv6 무선망 접속 및 Matter Fabric 보안 패브릭 바인딩 개통
```

### 동작 원리

1. **BLE 기반 기기 검색**: 신규 Matter 기기의 전원을 켜고 스마트폰으로 기기의 QR 코드를 스캔하면 BLE 무선 채널로 기기를 자동 탐색한다.
2. **PASE 세션 형성 및 기기 인증**: QR 코드의 통신 페어링 값을 활용해 암호화된 PASE(Passcode-Authenticated Session Establishment) 보안 세션을 수립한다.
3. **제조사 DAC 무결성 검증**: 기기에 저장된 제조사 DAC 인증서를 추출하고 3차 하위 CA 체인을 확인하여 Matter 공식 승인 제품인지 검증한다.
4. **운영 인증서(NOC) 및 네트워크 자격 제공**: 검증이 완료되면 구내 전용 운영 인증서(NOC)와 Thread/Wi-Fi 접속 패스워드를 기기에 전달한다.
5. **Thread/IPv6 망 접속 및 Fabric 완료**: 기기가 BLE를 끄고 전달받은 자격 정보로 Thread IPv6망에 접속하여 컨트롤러의 보안 패브릭(Fabric) 구성원으로 등록된다.

#### 한줄 요약

- BLE/QR코드 기기 검색, PASE 암호화 세션 수립, DAC 기기 검증, NOC 자격증명 전달 및 Matter Fabric 보안 등록 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **운영 인증서(Node Operational Certificate, NOC)**: 특정 스마트홈 패브릭 안에서 커미셔닝이 완료된 후 기기 간 명령 교환을 허용하는 PKI 암호화 인증서이다.

</details>

| 비교 항목 | **Zigbee** | **Thread** | **Matter** |
|:---|:---|:---|:---|
| 적용 OSI 계층 | PHY, MAC, Network, App 전 계층 수직 통합 | PHY, MAC, Network 계층 (OSI 1~4 계층) | Application 계층 (OSI 7 계층) |
| IP 지원 여부 | 비-IP (Non-IP 고유 게이트웨이 필요) | 100% 네이티브 IPv6 지원 (6LoWPAN) | 100% 네이티브 IP (Thread, Wi-Fi, Ethernet 수용) |
| 네트워크 토폴로지 | 게이트웨이 중심 무선 메시망 | SPOF 없는 가변 리더/경계 라우터 메시망 | IP 네트워크 기반 피어-투-피어(P2P) 및 클러스터 |
| 주체 및 표준 기구 | CSA (Zigbee Alliance) | Thread Group | CSA (Connectivity Standards Alliance) |
| 기기 호환성 | 브리지 없이 타 제조사 연동 불가능 | IP 패킷 전송 통로만 제공 (앱 표준 미포함) | 삼성 SmartThings, Apple Home, Google Nest 간 100% 호환 |

> 요약: Zigbee는 비-IP 전용 메시망, Thread는 저전력 IPv6 전송망, Matter는 최상위 애플리케이션 통합 표준으로 3자가 유기적 연동.

#### 한줄 요약

- Zigbee는 비-IP 전용 메시망, Thread는 저전력 IPv6 전송망, Matter는 최상위 애플리케이션 통합 표준으로 3자가 유기적 연동.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **모델·명령 매핑(Data Model & Command Mapping)**: Matter 브리지가 기존 Zigbee 기기의 속성을 Matter의 스위치/조명 클러스터 모델로 양방향 번역하는 변환 규격이다.
- **패브릭(Fabric)**: 동일한 PKI 루트 신뢰점(Root of Trust)을 공유하여 안전하게 상호 제어할 수 있는 Matter 기기들의 보안 영역 단위이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 계층 간 책임 혼동 | Thread(전송망)와 Matter(앱) 기술을 동일 선상 오인 | 계층 분리 설계 (Matter on Thread / Matter on Wi-Fi) | 네트워크 하주 구조와 응용 상호운용성 이중 달성 |
| 레거시 지그비 기기 고립 | 비-IP 지그비 기기가 Matter 환경에서 통신 불가 | Matter Bridge 개발 및 ZCL-to-Matter 모델 1:1 매핑 | 기존 설치 인프라 보존 및 단계적 Matter 전환 |
| Thread 경계 라우터 장애 | 단일 경계 라우터 다운 시 Thread 기기 이탈 | Thread 경계 라우터 다중화 (Dynamic Leader Election) | 메인 라우터 장애 시에도 메시망 라우팅 자동 복구 |
| 미승인 위조 기기 침입 | 중국산 저가 복제 기기의 커미셔닝 시도 | DAC 인증서 검증 필수화 및 PKI CRL 실시간 대조 | 위조 단말 통제 및 스마트홈 홈 보안성 확보 |

#### 한줄 요약

- Thread Border Router 이중화, Matter Bridge 속성-명령 1:1 매핑, PKI 기반 NOC 인증서 보안 강화를 통해 융합 IoT 망 품질 완성.

## Ⅶ. 결론

- 스마트홈/스마트빌딩 IoT망 구축 시 **IPv6 기반 Thread/Wi-Fi 전송망 채택**, **Matter 상호운용 응용 표준 적용**, **Zigbee 레거시 Matter 브리지 연동 필수**.

#### 한줄 요약

- Thread 기반 저전력 IPv6 메시망 구축, Matter 기반 멀티 벤더 애플리케이션 통합 및 Matter 브리지 체계 구현 필수.
