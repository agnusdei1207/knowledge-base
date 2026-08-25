---
sidebar:
  order: 78
  label: "078. MQTT 프로토콜"
  badge:
    text: "기출 · 50%"
    variant: note
title: "경량 IoT 메시징 프로토콜 : MQTT (Message Queuing Telemetry Transport)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 78
extra:
  question_no: "78"
  source_status: "기출"
  source_history: "105회, 114회, 120회, 125회"
  priority: 50
  priority_note: "IoT/임베디드 핵심 경량 발행-구독 메시징 프로토콜"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MQTT (Message Queuing Telemetry Transport)**: 최소 2바이트 고정 헤더를 갖는 비동기 발행-구독(Pub/Sub) 경량 메시징 표준 (ISO/IEC 20922).
- **MQTT Broker**: 발행자로부터 메시지를 수신하여 계층형 토픽(Topic) 트리를 기반으로 구독자에게 라우팅하는 중앙 서버.

</details>

- 정의/개념: 최소 2바이트 헤더와 **토픽 기반 비동기 발행-구독 모델, 3단계 QoS를 제공하는 경량 IoT 메시징 프로토콜**
- 배경/필요성: HTTP의 거대 텍스트 헤더 오버헤드 및 동기식 폴링 한계로 인한 **저전력 MCU 배터리 방전, 대역폭 낭비 및 실시간 푸시 불가**

#### 한줄 요약
- 최소 2바이트 헤더, 비동기 Pub/Sub 디커플링, 3단계 QoS를 통해 저전력·저대역폭 IoT 통신을 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Retained Message**: 브로커가 특정 토픽의 마지막 유효 메시지를 캐싱하여 신규 구독자가 접속하자마자 즉시 최신 상태를 전달받게 하는 기능.
- **LWT (Last Will and Testament)**: 클라이언트가 비정상 단절될 때 브로커가 대리로 다른 구독자들에게 전송하는 유언 메시지.

</details>

- **최소 2바이트 초경량 헤더**: 패킷 오버헤드를 극소화하여 **대역폭 절감 및 배터리 수명 극대화**
- **비동기 발행-구독(Pub/Sub) 디커플링**: 송수신자 간의 시간·공간적 결합을 제거하여 **대규모 분산 노드 확장성 보장**
- **3단계 신뢰성 전송(QoS 0/1/2)**: 서비스 중요도에 따라 **유실 허용(0)부터 중복 없는 유일 전달(2)까지 선택**
- **상태 보존(Retained Message & LWT)**: 신규 접속 기기를 위한 **상태 캐싱 및 비정상 단절 시 유언 메시지 자동 배포**

#### 한줄 요약
- 초경량 헤더, 비동기 디커플링, 3단계 QoS, LWT 단절 알림을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Topic Tree & Wildcard**: `/`로 구분되는 계층 경로로 단일 레벨 대체 `+`와 하위 전체 대체 `#` 와일드카드를 지원하는 라우팅 키.

</details>

```text
[MQTT 발행-구독 메시징 토폴로지 아키텍처]
|-- Publisher (IoT 센서 단말: `factory/temp` 토픽으로 25.4°C 데이터 PUBLISH)
`-- MQTT Broker (EMQX / Mosquitto: 토픽 트리 매칭, QoS 필터링, Retained 캐시)
    |-- Session Store (오프라인 클라이언트를 위한 미전송 QoS 1/2 큐 보관)
    `-- Access Control (mTLS X.509 인증 및 토픽별 RBAC 접근 인가)
`-- Subscribers (관심 토픽 구독 및 비동기 수신)
    |-- Control Server (`factory/#` 와일드카드 구독 -> 긴급 차단 제어)
    `-- Mobile Dashboard (`factory/+/status` 구독 -> 실시간 시각화)
```

선의 의미: 발행자가 브로커로 메시지를 전송하고 브로커가 등록된 토픽 트리에 따라 다중 구독자에게 메시지를 라우팅하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **발행자 (Publisher)** | 센서 데이터를 수집하여 특정 토픽 경로에 **메시지를 생성 및 전송하는 클라이언트** | IoT 단말 |
| **MQTT 브로커 (Broker)**| 연결 관리, **토픽 필터링, 메시지 큐잉 및 라우팅을 수행하는 중앙 서버** | EMQX, HiveMQ |
| **구독자 (Subscriber)** | 특정 토픽을 등록하여 **관심 메시지를 브로커로부터 비동기로 수신** | 서버, 대시보드 |
| **토픽 (Topic)** | `/` 구분자를 사용하는 **계층형 라우팅 키 (`+`, `#` 와일드카드 지원)** | Routing Path |
| **세션 (Session)** | Clean Session 설정에 따라 **오프라인 중 미전송 QoS 1/2 메시지 보관** | State Store |

#### 한줄 요약
- 발행자, 브로커, 구독자, 계층형 토픽, 세션 스토어가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **4-Way QoS 2 Handshake**: PUBLISH $\rightarrow$ PUBREC(수신 확인) $\rightarrow$ PUBREL(발행 릴리즈) $\rightarrow$ PUBCOMP(완료)로 이어지는 중복 제거 트랜잭션.

</details>

```text
MQTT 세션 수립, 토픽 구독 및 메시지 중계 파이프라인
        │
   1. [CONNECT / CONNACK] 클라이언트가 Keep-Alive, LWT, 인증 정보로 세션 수립
        │
   2. [SUBSCRIBE / SUBACK] 구독자가 토픽 필터(`factory/#`)와 희망 QoS를 지정하여 등록
        │
   3. [PUBLISH 송출] 발행자가 특정 토픽으로 페이로드와 QoS 등급을 담아 브로커로 전송
        │
   4. [토픽 트리 매칭 라우팅] 브로커가 계층 트리를 탐색하여 일치하는 모든 구독자에 복제 중계
        │
   ▼
5. [QoS별 전송 완결] QoS 0(단방향), QoS 1(PUBACK 회신), QoS 2(4-Way 핸드셰이크) 트랜잭션 완료
```

#### 한줄 요약
- 연결 수립 → 토픽 구독 → 메시지 발행 → 브로커 라우팅 → QoS 레벨별 전달 완결 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **QoS 0 vs QoS 1 vs QoS 2**: 최대 1회(유실 가능), 최소 1회(중복 가능), 정확히 1회(중복 없음).

</details>

| 비교 항목 | QoS 0 (At most once) | QoS 1 (At least once) | QoS 2 (Exactly once) |
|:---|:---|:---|:---|
| **메시지 전달 보장** | **최대 1회 전송 (유실 가능)** | **최소 1회 보장 (중복 가능)** | **정확히 1회 보장 (중복 없음)** |
| **핸드셰이크 절차** | **Fire-and-Forget (응답 없음)** | **PUBACK 수신 시까지 재전송** | **4-Way (PUBREC $\rightarrow$ PUBREL $\rightarrow$ PUBCOMP)** |
| **통신 오버헤드** | **최소 (단일 패킷 송출)** | 보통 (2개 패킷 교환) | **최대 (4개 패킷 왕복 교환)** |
| **네트워크 단절 시** | 패킷 유실 방치 | 재전송으로 수신단 중복 유입 | 패킷 식별자(Packet ID)로 완벽 중복 제거 |
| **대표 적용 서비스** | 주기적 온습도 센서 텔레메트리 | 장비 상태 알람, 이벤트 로그 | **금융 과금, 모터 인버터 긴급 차단** |

#### 한줄 요약
- QoS 0은 단순 센서용, QoS 1은 일반 이벤트용, QoS 2는 미션 크리티컬 제어용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shared Subscription (공유 구독, MQTT 5.0)**: `$share/group/topic` 문법으로 다수의 백엔드 컨슈머가 단일 토픽의 메시지를 라운드로빈 부하 분산 처리하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수만 대 IoT 동시 재접속 시 브로커 세션 고갈 및 연결 폭풍 | **MQTT 클러스터링 및 `지수 백오프(Exponential Backoff)` 적용** | 브로커 부하 분산 및 네트워크 폭주 방지 |
| 평문 전송 시 도청 및 비인가 기기에 의한 악성 토픽 오염 | **`mTLS (X.509 상호 인증)` 및 토픽 레벨 RBAC 접근 인가** | 전 구간 암호화 및 비인가 기기 침입 원천 차단 |
| 오프라인 클라이언트의 미전송 QoS 1/2 누적으로 브로커 메모리 고갈 | **`Message Expiry Interval (메시지 만료)` 및 큐 크기 제한** | 유효 시간 경과 패킷 자동 회수 및 메모리 안정성 확보 |
| 대규모 토픽 트래픽 집중으로 단일 컨슈머 서버 처리 병목 | **MQTT 5.0 `공유 구독($share/group)` 기반 로드밸런싱** | 복수 컨슈머 간 부하 분산 및 스케일아웃 달성 |

#### 한줄 요약
- 지수 백오프, mTLS/RBAC 보안, 메시지 만료 시간 설정, MQTT 5.0 공유 구독으로 운영한다.

## Ⅶ. 결론

- 대규모 분산 IoT 환경의 초경량 통신과 신뢰성을 보장하기 위해 **MQTT 프로토콜과 브로커 클러스터 아키텍처를 표준 메시징 인프라로 구축**하되, 엔터프라이즈 운영 요구를 충족하기 위해 **MQTT 5.0 공유 구독 기반 부하 분산, mTLS 상호 인증 보안, 메시지 만료 수명주기 통제**를 통합 적용하여 고확장성 스마트 IoT 플랫폼 완성

#### 한줄 요약
- MQTT는 초경량 헤더와 비동기 Pub/Sub 및 3단계 QoS를 통해 대규모 IoT 연결을 실현하는 글로벌 표준 메시징 프로토콜이다.