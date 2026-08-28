---
sidebar:
  order: 79
  label: "079. OPC UA 산업 표준 통신"
  badge:
    text: "기출 · 50%"
    variant: note
title: "스마트 팩토리 상호운용 표준 : OPC UA (OPC Unified Architecture)"
date: "2026-08-26T14:06:20+09:00"
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

- 정의/개념: **주소 공간·PKI·C/S·Pub/Sub**의 산업 통신 표준
- 배경/필요성: OPC DA는 DCOM에 묶여 윈도우 이외 환경마다 **별도 게이트웨이 구축 비용**을 치르므로, 전송 방식과 분리된 시맨틱 주소 공간 모델을 두어 OS·벤더별 개별 연동 작업을 대신

#### 한줄 요약
- **플랫폼 독립·시맨틱 모델·다계층 보안** 제공

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cross-Platform**: 특정 OS나 언어에 종속되지 않고 리눅스, 윈도우, 경량 RTOS 및 임베디드 MCU에서 동작하는 개방형 구조.
- **Security-by-Design (IEC 62541-2)**: 애플리케이션 수준의 X.509 인증서 상호 검증, 사용자 RBAC 인가, AES-256 전송 암호화를 내장한 보안 체계.

</details>

- **플랫폼 독립성**: Linux·RTOS·클라우드 환경 지원
- **시맨틱 주소 공간**: 단위·범위·경보의 의미 보존
- **이중 통신 모델**: C/S와 Pub/Sub·TSN 동시 지원

#### 한줄 요약
- OS 독립성, 시맨틱 주소 공간 모델링, 다계층 보안 및 C/S-Pub/Sub 듀얼 통신 모델을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Companion Specification**: 반도체(SEMI), 공작기계(umati), 로봇(VDMA) 등 산업군별 공통 데이터 모델을 정의한 표준 확장 명세.
- **GDS (Global Discovery Server)**: 공장 내 수천 대의 OPC UA 엔드포인트 탐색과 X.509 인증서 발급·갱신을 중앙 자동화하는 보안 서버.

</details>

```text
[OPC UA 정적 구성]
|-- 주소 공간
|-- 정보 모델
|-- 보안 스택
|-- Pub/Sub 브로커 / TSN
`-- GDS
```

선의 의미: 현장 센서 및 PLC 데이터가 OPC UA 서버의 주소 공간에 시맨틱 객체로 모델링되어 상위 IT/MES 시스템으로 안전하게 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 주소 공간 | 설비를 **NodeId·속성·참조로 모델링** | 데이터/서비스 저장소 |
| 정보 모델 | **단위·범위·경보 정의** | 시맨틱 메타데이터 |
| 보안 스택 | **X.509 인증·AES 암호화** | IEC 62541-2 |
| Pub/Sub 브로커 / TSN | **저지연 비동기 배포** | 결정론적 전송 |
| GDS | **엔드포인트·인증서 수명주기 관리** | PKI 중앙 관리 |

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
    |
3. 세션 활성화·인가
    |
4. 주소 공간 탐색
    |
5. MonitoredItem 구독
    |
변경 통지
```

- 1. 엔드포인트 탐색
- 2. 보안 채널 수립
- 3. 세션 활성화·인가
- 4. 주소 공간 탐색
- 5. MonitoredItem 구독

#### 한줄 요약
- MonitoredItem 구독은 값이 변할 때만 데이터를 올리므로, 주기적 폴링이 치르던 회선 부하가 서버 측 변화 감지 부담으로 옮겨간다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Client/Server (1:1 RPC 세션)** vs **Pub/Sub (1:N 비동기 브로드캐스트 / TSN 연동)**.

</details>

| 비교 항목 | 클라이언트-서버 모델 (Client/Server) | 발행-구독 모델 (Pub/Sub) |
|:---|:---|:---|
| 통신 패러다임 | **1:1 요청-응답** | **1:N·M:N 비동기 배포** |
| 전송 프로토콜 | **OPC UA TCP·HTTPS** | **UDP·MQTT·AMQP·TSN** |
| 실시간 결정론성 | 소프트 실시간 | **TSN 기반 하드 실시간** |
| 네트워크 확장성 | 세션 수에 비례 | **다수 노드 동시 배포** |
| 주요 적용 분야 | 구성·정밀 제어 | **센서 수집·필드버스 대체** |

#### 한줄 요약
- Client/Server는 정밀 구성 및 1:1 제어에 적합하고, Pub/Sub는 대규모 데이터 수집 및 실시간 TSN 연동에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Certificate Expiration (인증서 만료)**: 노드 간 보안 채널 형성에 쓰이는 X.509 인증서가 만료될 때 통신이 전면 차단되어 공장 가동이 중단되는 리스크.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 제조사별 변수명 차이 | **Companion Specification** 채택 | 데이터 의미 표준화 |
| 인증서 만료로 설비 통신 차단 | **GDS 인증서 자동 갱신** | 만료 중단 예방 |
| 센서 폴링으로 서버 부하 증가 | **Subscription·Pub/Sub** | 부하 분산·실시간 전송 |
| 외부 침입에 따른 설비 조작 | **RBAC·SignAndEncrypt** | 비인가 명령 차단 |

#### 한줄 요약
- **Companion 명세·GDS·Pub/Sub**로 운영 안정성 확보

## Ⅶ. 결론

- 정밀 설정은 **C/S**, 대규모 실시간 배포는 **Pub/Sub·TSN** 선택

#### 한줄 요약
- **주소 공간·PKI·TSN**으로 IT-OT 상호운용성 확보
