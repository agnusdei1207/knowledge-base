---
sidebar:
  order: 79
  label: "079. OPC UA 산업 표준 통신"
  badge:
    text: "기출 · 50%"
    variant: note
title: "스마트 팩토리 상호운용 표준 : OPC UA (OPC Unified Architecture)"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: 설비 데이터를 **Semantic Information Model** 기반 주소 공간으로 모델링하고 X.509 PKI 보안과 C/S·Pub/Sub 전송을 함께 표준화한 산업 통신 표준(IEC 62541)
- 배경/필요성: 과거 공장 자동화에서 사용되던 레거시 OPC Classic(OPC DA/HDA)은 마이크로소프트 윈도우 독점 기술인 DCOM(Distributed COM)에 종속되어 방화벽 통과 불가, 리눅스/임베디드 설비 연동 불가 및 보안 취약점을 노출하고, 벤더별 제각각인 메모리 번지수 기반 원시 데이터 구조로 인해 상위 IT/클라우드 시스템과의 시맨틱(Semantic) 데이터 연동이 불가능했던 한계를 극복하기 위해, 플랫폼 독립적(OS-Agnostic) 객체 지향 주소 공간(Address Space) 모델과 내장형 다계층 보안(X.509 PKI/AES-256) 및 C/S와 Pub/Sub(TSN 결합) 듀얼 전송 체계를 표준화한 OPC UA(IEC 62541)를 도입하여 이종 PLC/설비 간 완벽한 상호운용성(Interoperability), 스마트 팩토리 OT와 IT/클라우드의 심리스 융합 및 산업 제어 시스템 보안 강화를 달성할 필요

#### 한줄 요약
- DCOM 종속 OPC Classic이 설비마다 치르던 드라이버·방화벽·의미 해석 비용을 표준 계층 하나로 흡수하므로, 설비 수가 늘어도 상위 IT가 지불하는 연동 비용은 늘지 않는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cross-Platform**: 특정 OS나 언어에 종속되지 않고 리눅스, 윈도우, 경량 RTOS 및 임베디드 MCU에서 동작하는 개방형 구조.
- **Security-by-Design (IEC 62541-2)**: 애플리케이션 수준의 X.509 인증서 상호 검증, 사용자 RBAC 인가, AES-256 전송 암호화를 내장한 보안 체계.

</details>

- 플랫폼 독립성(**Cross-Platform**): Linux·RTOS·클라우드 환경 지원
- 시맨틱 주소 공간: 단위·범위·경보의 의미 보존
- 이중 통신 모델: C/S와 Pub/Sub·TSN 동시 지원
- 내장 보안(**Security-by-Design**): X.509 상호 인증·RBAC·AES 암호화를 스택에 내장

#### 한줄 요약
- 플랫폼 독립성과 시맨틱 모델은 설비 벤더가 자체 데이터 구조의 자유를 포기하고 공통 모델에 맞춘 대가로 얻는 것이라, 표준 채택률이 곧 상호운용성의 상한이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Companion Specification**: 반도체(SEMI), 공작기계(umati), 로봇(VDMA) 등 산업군별 공통 데이터 모델을 정의한 표준 확장 명세.
- **GDS (Global Discovery Server)**: 공장 내 수천 대의 OPC UA 엔드포인트 탐색과 X.509 인증서 발급·갱신을 중앙 자동화하는 보안 서버.

</details>

```text
[OPC UA 아키텍처]
  ├── [모델링 계층] ─────── [주소 공간 / 정보 모델]
  │                           │
  ├── [보안 관리] ───────── [보안 스택 / GDS]
  │                           │
  └── [전송 계층] ───────── [C/S 세션 / Pub/Sub(TSN)]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 주소 공간 (Address Space) | 설비 자원을 NodeId, 속성(Attribute), 참조(Reference) 기반 객체 모델로 저장 |
| 정보 모델 (Information Model) | 산업군별 데이터 단위, 공학적 범위 및 경보 메타데이터 정의 (Companion Spec) |
| 보안 스택 | X.509 인증서 상호 인증, RBAC 사용자 인가 및 AES-256 통신 암호화 집행 |
| Pub/Sub 브로커 / TSN | 대규모 분산 환경 저지연 비동기 이벤트 배포 및 결정론적 실시간 제어 전송 |
| GDS (글로벌 탐색 서버) | 공장 내 다수 엔드포인트 자동 탐색 및 X.509 인증서 라이프사이클 중앙 관리 |

#### 한줄 요약
- 주소 공간이 벤더별 태그 번호 대신 의미가 붙은 노드를 제공하므로, 상위 IT 시스템은 장비 문서를 해석하는 단계 없이 데이터를 찾아간다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Subscription & MonitoredItem**: 클라이언트가 주기적 폴링 없이 값 변경(Change of State) 시에만 서버로부터 비동기 알림을 받는 이벤트 모델.

</details>

```text
클라이언트 요청
    |
1. 엔드포인트 탐색
    |
2. 보안 채널 수립
    +-- 인증서 신뢰 실패: 연결 거부
    `-- 신뢰 성공: 세션 활성화
    |
3. 세션 활성화·인가
    |
4. 주소 공간 탐색
    |
5. MonitoredItem 구독
    |
변경 통지
```

분기 결과: 보안 채널 수립에서 X.509 인증서 신뢰 검증에 실패하면 세션 자체가 열리지 않으므로, 주소 공간 탐색과 **Subscription & MonitoredItem** 구독은 상호 인증을 통과한 클라이언트만 도달한다.

#### 한줄 요약
- MonitoredItem 구독은 값이 변할 때만 데이터를 올리므로, 주기적 폴링이 치르던 회선 부하가 서버 측 변화 감지 부담으로 옮겨간다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Client/Server (1:1 RPC 세션)** vs **Pub/Sub (1:N 비동기 브로드캐스트 / TSN 연동)**.

</details>

| 비교 항목 | 클라이언트-서버 모델 (Client/Server) | 발행-구독 모델 (Pub/Sub) |
|:---|:---|:---|
| 통신 패러다임 | 1:1 요청-응답 | 1:N·M:N 비동기 배포 |
| 전송 프로토콜 | OPC UA TCP·HTTPS | UDP·MQTT·AMQP·TSN |
| 실시간 결정론성 | 소프트 실시간 | TSN 기반 하드 실시간 |
| 네트워크 확장성 | 세션 수에 비례 | 다수 노드 동시 배포 |
| 주요 적용 분야 | 구성·정밀 제어 | 센서 수집·필드버스 대체 |

#### 한줄 요약
- Client/Server는 정밀 구성 및 1:1 제어에 적합하고, Pub/Sub는 대규모 데이터 수집 및 실시간 TSN 연동에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Certificate Expiration (인증서 만료)**: 노드 간 보안 채널 형성에 쓰이는 X.509 인증서가 만료될 때 통신이 전면 차단되어 공장 가동이 중단되는 리스크.
- **SignAndEncrypt**: OPC UA 보안 채널의 메시지 보안 모드(MessageSecurityMode) 중 최고 수준으로, 모든 메시지에 서명하고 본문을 암호화해 위변조와 도청을 동시에 막는 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 제조사별 변수명 차이 | **Companion Specification** 채택 | 데이터 의미 표준화 |
| **인증서 만료**로 설비 통신 차단 | **GDS** 인증서 자동 갱신 | 만료 중단 예방 |
| 센서 폴링으로 서버 부하 증가 | **Subscription & MonitoredItem**·**Pub/Sub** 전환 | 부하 분산·실시간 전송 |
| 외부 침입에 따른 설비 조작 | **SignAndEncrypt** 보안 모드·RBAC 인가 | 비인가 명령 차단 |

#### 한줄 요약
- 변수명·인증서·폴링 문제를 설비별로 대응하지 않고 명세·GDS·구독이라는 표준 계층에서 한 번 해결하는 쪽이 설비 수에 비례하는 운영 비용을 끊는다.

## Ⅶ. 결론

- 스마트 팩토리 인더스트리 4.0(RAMI 4.0)의 데이터 모델링과 제어 통신을 주도하며 글로벌 스마트 제조 및 IT-OT 융합의 단일 표준 산업 통신 아키텍처(IEC 62541)로 확고히 자리잡았으며, 필드버스(Fieldbus) 영역까지 완벽히 대체하기 위해 TSN(Time-Sensitive Networking)과 결합한 OPC UA over TSN 및 5G 사설망 연동으로 진화하는 가운데, 실무 스마트 제조 인프라 구축 시에는 공작기계(umati), 로봇(VDMA) 등 산업군별 데이터 의미 표준화를 위한 컴패니언 명세(Companion Specification) 적용, 수천 개 설비의 **인증서 만료** 중단을 방지하는 **GDS**(**Global Discovery Server**) 자동 배포/갱신, 비인가 제어를 원천 차단하는 **SignAndEncrypt** 보안 프로파일과 RBAC 인가를 결합하여 완벽한 산업 제조 신뢰성을 완성

#### 한줄 요약
- 구성·정밀 제어에는 C/S, 대규모 수집·하드 실시간에는 Pub/Sub over TSN을 택하되, 두 모델을 같은 주소 공간 위에 두는 것이 OPC UA를 고르는 이유다.
