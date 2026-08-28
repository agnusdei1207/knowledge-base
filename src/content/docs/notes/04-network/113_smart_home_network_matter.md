---
sidebar:
  order: 113
  label: "113. 스마트 홈 통합 Matter"
  badge:
    text: "기출 · 50%"
    variant: note
title: "스마트 홈 상호운용성 표준 : Matter"
date: "2026-08-26T14:13:18+09:00"
tags:
  - "notes-network"
weight: 113
extra:
  question_no: "113"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "CSA 표준, IPv6 기반 공통 데이터 모델, Wi-Fi/Thread/Ethernet 전송, Multi-Admin 및 DAC/NOC 보안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Matter (CSA)**: Apple, Google, Amazon, Samsung 등이 공동 제정한 IPv6 기반의 스마트 홈 오픈소스 상호운용성 표준.
- **Common Data Model (공통 데이터 모델)**: 기기의 속성(Attributes), 명령(Commands)을 클러스터(Cluster) 구조로 표준화한 L7 애플리케이션 모델.

</details>

- 정의/개념: IPv6와 **공통 데이터 모델** 기반 스마트 홈 표준
- 배경/필요성: 제조사별 독자 규격은 기기마다 **전용 허브와 앱을 중복 도입하는 비용**을 치르므로, IPv6 위에 공통 데이터 모델과 Multi-Admin을 규정해 기기 하나가 여러 생태계에 동시에 속하도록 함

#### 한줄 요약
- IPv6 기반 공통 데이터 모델과 Multi-Admin을 통해 플랫폼 종속 없는 로컬 스마트 홈 제어를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-Admin (다중 관리자)**: 단일 Matter 기기를 Apple HomeKit, Google Home, Samsung SmartThings 등 복수의 스마트 홈 플랫폼에 동시 등록하여 제어하는 기능.
- **Local Control (로컬 완결 제어)**: 외부 클라우드 서버와의 통신 없이 댁내 로컬 IPv6 네트워크 내에서 100% 기기 제어를 완결하는 오프라인 자율성.

</details>

- **Multi-Admin** 기반 복수 플랫폼의 기기 제어
- IPv6 LAN 기반 **로컬 제어** 지원
- **DAC·NOC** 기반 기기 증명과 운영 인증

#### 한줄 요약
- Multi-Admin 다중 제어, 클라우드 독립 로컬 완결 제어, PKI 하드웨어 보안을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Thread Border Router**: 저전력 무선 메시망인 Thread(IEEE 802.15.4)와 고속 댁내 Wi-Fi/Ethernet 간의 IPv6 패킷을 상호 라우팅해 주는 경계 공유기.

</details>

```text
Matter Home
|-- Controller
|-- IPv6 Network
|   |-- Thread Border Router
|   |-- Endpoint
|   `-- Matter Bridge
`-- DCL
```

선의 의미: Matter 응용 계층이 IPv6를 통해 Wi-Fi와 Thread 무선 서브넷으로 분기되어 고대역 기기와 저전력 센서 노드를 단일 제어 평면으로 통합하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Controller** | 패브릭 관리와 제어 명령 송신 |
| **IPv6 Network** | Wi-Fi·Thread·Ethernet 연결 |
| **Thread Border Router** | Thread와 LAN 간 IPv6 라우팅 |
| **Endpoint** | **클러스터·속성·명령** 구현 |
| **Matter Bridge** | 레거시 기기를 Matter 모델로 변환 |
| **DCL** | 제조사 인증서와 제품 정보 제공 |

#### 한줄 요약
- Thread Border Router가 저전력 메시망과 홈 IP망 사이의 변환을 맡으므로, 컨트롤러는 기기의 무선 방식과 무관하게 동일한 데이터 모델로 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PASE vs CASE**: QR 코드 패스코드 기반의 1회용 초기 페어링 보안 채널(PASE)과 노드 간 상호 X.509 인증서 기반의 영구 운영 보안 채널(CASE).

</details>

```text
Matter 기기 커미셔닝, DAC 정품 검증 및 패브릭 가입 파이프라인
        │
       [QR 페이로드 스캔]
        │
   1. [PASE 채널 수립]
        │
   2. [DAC 기기 증명 검증]
        │
   3. [네트워크 자격 증명 전달]
        │
   ▼
   4. [NOC 발급 및 패브릭 가입]
```

- 1. PASE 채널 수립
- 2. DAC 기기 증명 검증
- 3. 네트워크 자격 증명 전달
- 4. NOC 발급 및 패브릭 가입

#### 한줄 요약
- DAC 검증에서 패브릭 가입과 거부로 갈리며, 제조 단계 인증서를 요구하는 대가로 위조 기기의 진입을 원천 차단한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Legacy Zigbee/Z-Wave** vs **Legacy 독자 Wi-Fi** vs **Matter 표준**.

</details>

| 비교 항목 | 레거시 Zigbee / Z-Wave | 레거시 독자 Wi-Fi 기기 | 차세대 Matter 표준 |
|:---|:---|:---|:---|
| 네트워크 계층 | Zigbee는 비-IP | IP | **IPv6** |
| 상호운용 방식 | 허브 생태계별 | 독자 API별 | **공통 데이터 모델** |
| 로컬 제어 | 구현별 상이 | 구현별 상이 | 표준 기능으로 지원 |
| 보안 방식 | 네트워크 키 | 구현별 TLS | **DAC·NOC·CASE** |
| 메시 지원 | Zigbee 메시 | Wi-Fi 토폴로지 | **Thread 메시** |

#### 한줄 요약
- 레거시 Zigbee는 허브 종속, 독자 Wi-Fi는 클라우드 종속이나, Matter는 IPv6 기반 로컬 상호운용 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DNS-SD Discovery Proxy**: Thread 기기들의 mDNS 멀티캐스트 검색 패킷을 Border Router가 프록시 처리하여 Wi-Fi 대역폭 낭비를 막는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| mDNS 증가로 **Wi-Fi 멀티캐스트 부하** | **DNS-SD Discovery Proxy** | 검색 트래픽 완화 |
| Multi-Admin 간 **상태 불일치** | **Subscription** 변경 보고 | 상태 수렴 개선 |
| 센서 폴링으로 **배터리 조기 방전** | **SED·ICD** 적용 | 저전력 동작 지원 |
| 비공인 기기의 패브릭 가입 | **Secure Element DAC·DCL** 검증 | 위조 기기 위험 완화 |

#### 한줄 요약
- DNS-SD 프록시로 mDNS 폭주를 막고, 구독 모델로 동기화를 유지하며, SED 모드로 배터리를 보존한다.

## Ⅶ. 결론

- 저전력 메시는 **Thread**, 다중 플랫폼 제어는 **Matter** 선택

#### 한줄 요약
- Matter는 IPv6 기반 공통 데이터 모델과 Multi-Admin 및 Thread 메시망을 통해 플랫폼 종속 없는 차세대 스마트 홈 표준을 완성한다.
