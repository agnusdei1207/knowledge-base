---
sidebar:
  order: 79
  label: "079. OPC UA 산업 표준 통신"
  badge:
    text: "기출 · 50%"
    variant: note
title: "스마트 팩토리 상호운용 표준 : OPC UA (OPC Unified Architecture)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 79
extra:
  question_no: "79"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "객체 지향 정보 모델(Address Space), 보안 프로파일(X.509 PKI), C/S 및 Pub/Sub(TSN 연동)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OPC UA (OPC Unified Architecture)**: 이종 설비와 상위 IT 시스템 간 상호운용성을 보장하는 플랫폼 독립적 서비스 지향 산업 통신 표준 (IEC 62541).
- **Semantic Information Model**: 원시 바이트뿐만 아니라 데이터의 단위, 범위, 계층 관계를 객체 지향 주소 공간(Address Space)으로 모델링한 구조.

</details>

- 정의/개념: 이종 산업 설비 간의 벤더 종속성을 제거하고 **주소 공간 기반 시맨틱 정보 모델, X.509 PKI 보안, C/S 및 Pub/Sub을 제공하는 산업용 통신 표준**
- 배경/필요성: 레거시 OPC DA의 윈도우 DCOM 종속 및 이종 필드버스 파편화로 인한 **리눅스/임베디드 연동 불가, 보안 취약점 노출 및 IT-OT 융합 한계**

#### 한줄 요약
- 플랫폼 독립성, 시맨틱 주소 공간 모델링, 다계층 보안 및 C/S-Pub/Sub 듀얼 통신 모델을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cross-Platform**: 특정 OS나 언어에 종속되지 않고 리눅스, 윈도우, 경량 RTOS 및 임베디드 MCU에서 동작하는 개방형 구조.
- **Security-by-Design (IEC 62541-2)**: 애플리케이션 수준의 X.509 인증서 상호 검증, 사용자 RBAC 인가, AES-256 전송 암호화를 내장한 보안 체계.

</details>

- **플랫폼 및 OS 독립성(Cross-Platform)**: 윈도우 DCOM 종속성을 완전 탈피하여 **리눅스, 임베디드 RTOS, 클라우드 네이티브 환경 지원**
- **객체 지향 시맨틱 주소 공간**: 데이터에 메타데이터(엔지니어링 단위, 범위, 경보)를 캡슐화하여 **데이터의 의미를 표준화 보존**
- **다양한 통신 패턴 지원**: 1:1 요청-응답 C/S 모델과 **1:N 대규모 실시간 배포를 위한 Pub/Sub(TSN 연동) 모델 동시 수용**

#### 한줄 요약
- OS 독립성, 시맨틱 주소 공간 모델링, 다계층 보안 및 C/S-Pub/Sub 듀얼 통신 모델을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Companion Specification**: 반도체(SEMI), 공작기계(umati), 로봇(VDMA) 등 산업군별 공통 데이터 모델을 정의한 표준 확장 명세.
- **GDS (Global Discovery Server)**: 공장 내 수천 대의 OPC UA 엔드포인트 탐색과 X.509 인증서 발급·갱신을 중앙 자동화하는 보안 서버.

</details>

```text
[OPC UA 엔드투엔드 IT-OT 통합 아키텍처]
|-- IT / Cloud Layer (MES / ERP / SCADA: OPC UA TCP / HTTPS / MQTT over TLS)
`-- OPC UA Server / Edge Gateway Layer
|   |-- Address Space (Root -> Objects -> Device -> Variables & Methods)
|   |-- Semantic Information Model (산업별 Companion Specs: VDMA, umati, EUROMAP)
|   `-- Multi-Layer Security Stack (X.509 App Auth, User RBAC, AES-256 Encryption)
|-- Real-Time Field Fabric (OPC UA Pub/Sub over IEEE 802.1 TSN / UDP Multicast)
`-- Field Device Layer (PLC, 산업용 로봇, CNC, 온습도/진동 센서 노드)
```

선의 의미: 현장 센서 및 PLC 데이터가 OPC UA 서버의 주소 공간에 시맨틱 객체로 모델링되어 상위 IT/MES 시스템으로 안전하게 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **주소 공간 (Address Space)** | 모든 설비 파라미터와 메서드를 **노드(NodeId, Attributes, References)로 모델링** | 데이터/서비스 저장소 |
| **정보 모델 (Information Model)**| 센서 데이터의 **물리적 단위, 정상 동작 범위, 경보(Alarm) 상태 정의** | 시맨틱 메타데이터 |
| **보안 스택 (Security Stack)** | 비대칭 암호(RSA) 채널 수립 및 **대칭 암호(AES-256) 데이터 전송 암호화** | IEC 62541-2 |
| **Pub/Sub 브로커 / TSN** | UDP 멀티캐스트 또는 MQTT를 활용한 **대규모 저지연 비동기 데이터 배포** | 결정론적 실시간 전송 |
| **GDS (중앙 디스커버리)** | 공장 내 **엔드포인트 탐색 및 X.509 인증서 수명주기(발급/갱신) 자동화** | PKI 중앙 관리 |

#### 한줄 요약
- 주소 공간, 정보 모델, 다계층 보안 스택, Pub/Sub 엔진, GDS 인증 서버가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Subscription & MonitoredItem**: 클라이언트가 주기적 폴링 없이 값 변경(Change of State) 시에만 서버로부터 비동기 알림을 받는 이벤트 모델.

</details>

```text
OPC UA 보안 채널 수립 및 이벤트 구독 파이프라인
        │
   1. [엔드포인트 탐색] 클라이언트가 GetEndpoints를 호출하여 보안 프로파일(SignAndEncrypt) 획득
        │
   2. [보안 채널 수립] X.509 인증서 검증 및 비대칭 키 교환으로 암호화된 Secure Channel 생성
        │
   3. [세션 활성화 및 인가] 사용자 자격 증명(ID/PW, 인증서)을 검증하여 역할 기반 세션 활성화
        │
   4. [주소 공간 브라우징] 계층형 참조(Reference)를 따라 주소 공간을 탐색하고 대상 NodeId 식별
        │
   ▼
5. [MonitoredItem 구독] 값 변경 시에만 비동기 통지(Notification)를 수신하여 대역폭 보존
```

#### 한줄 요약
- 보안 협상 → Secure Channel 수립 → User 세션 활성화 → 주소 공간 탐색 → MonitoredItem 구독 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Client/Server (1:1 RPC 세션)** vs **Pub/Sub (1:N 비동기 브로드캐스트 / TSN 연동)**.

</details>

| 비교 항목 | 클라이언트-서버 모델 (Client/Server) | 발행-구독 모델 (Pub/Sub) |
|:---|:---|:---|
| **통신 패러다임** | **1:1 양방향 요청-응답 (RPC / Session)** | **1:N 또는 M:N 비동기 브로드캐스트 (Stateless)** |
| **전송 프로토콜** | **OPC UA TCP (기본), HTTPS / WebSockets** | **UDP 멀티캐스트, MQTT, AMQP, IEEE 802.1 TSN** |
| **실시간 결정론성** | TCP 오버헤드로 인해 소프트 실시간 적합 | **TSN 결합 시 수 $\mu\text{s}$ 단위 하드 실시간 보장** |
| **네트워크 확장성** | 노드 수 증가 시 서버 연결 세션 부하 증가 | **수천 대 노드에 동시 데이터 배포 가능 (고확장성)**|
| **주요 적용 분야** | SCADA/MES 구성 설정, 정밀 제어 명령 | **대규모 센서 수집, 필드버스 대체, 클라우드 연동** |

#### 한줄 요약
- Client/Server는 정밀 구성 및 1:1 제어에 적합하고, Pub/Sub는 대규모 데이터 수집 및 실시간 TSN 연동에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Certificate Expiration (인증서 만료)**: 노드 간 보안 채널 형성에 쓰이는 X.509 인증서가 만료될 때 통신이 전면 차단되어 공장 가동이 중단되는 리스크.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 설비 제조사별 상이한 변수 네이밍으로 MES 데이터 통합 단절 | 산업별 표준 **`컴패니언 명세(Companion Specification: umati, VDMA)` 채택** | 데이터 모델 표준화 및 MES/SCADA 상호운용성 확보 |
| X.509 인증서 유효기간 만료로 인한 **전체 설비 통신 차단 및 라인 셧다운** | **`GDS (Global Discovery Server) 기반 인증서 자동 갱신`** 체계 구축 | 인증서 만료 사고 예방 및 365일 무중단 공장 운영 |
| 대규모 센서 폴링 시 TCP 세션 과부하로 인한 OPC UA 서버 CPU 폭증 | **`값 변경 구독(Subscription)` 전환 및 대규모 수집용 `Pub/Sub 모델` 도입** | 서버 CPU 부하 80% 절감 및 실시간 전송 효율 극대화 |
| 산업 제어망 외부 침입 시 설비 임의 조작 위협 | **`역할 기반 접근 제어(RBAC)` 및 SignAndEncrypt 암호화 프로파일 강제** | 비인가 제어 명령 원천 차단 및 무결성 보증 |

#### 한줄 요약
- 컴패니언 명세로 의미를 통일하고, GDS로 인증서 중단을 방지하며, Pub/Sub로 서버 부하를 분산한다.

## Ⅶ. 결론

- 제조 현장의 지능화와 스마트 팩토리 디지털 트윈을 구현하기 위해 **OPC UA 표준 아키텍처를 산업용 백본 프로토콜로 채택**하되, 실무 적용 시 데이터 일관성을 위한 **산업별 컴패니언 명세(Companion Specs)**, 신뢰성 유지를 위한 **GDS 중앙 인증 관리**, 초저지연 필드 제어를 위한 **OPC UA over TSN(Pub/Sub)** 기술을 통합 구현하여 완성도 높은 인더스트리 4.0 통신 인프라 완성

#### 한줄 요약
- OPC UA는 객체 지향 주소 공간과 다계층 보안 및 TSN Pub/Sub을 결합하여 IT와 OT를 융합하는 차세대 스마트 팩토리 표준 프로토콜이다.