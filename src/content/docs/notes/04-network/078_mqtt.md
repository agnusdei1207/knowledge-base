---
sidebar:
  order: 78
  label: "078. MQTT 프로토콜"
  badge:
    text: "기출 · 50%"
    variant: note
title: "MQTT 프로토콜 (Message Queuing Telemetry Transport)"
date: "2026-08-21T23:48:00+09:00"
tags:
  - "notes-network"
weight: 78
extra:
  question_no: "078"
  source_status: "기출"
  source_history: "105회, 114회, 120회, 125회"
  priority: 50
  priority_note: "IoT/임베디드 핵심 경량 발행-구독 메시징 프로토콜"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MQTT(Message Queuing Telemetry Transport)**: 저전력·저대역폭·불안정한 네트워크 환경의 IoT 기기를 위해 설계된 경량 발행-구독(Pub/Sub) 메시징 프로토콜.
- **브로커(Broker)**: 발행자(Publisher)로부터 메시지를 수신하여 토픽(Topic)을 구독(Subscribe)한 클라이언트에게 라우팅 및 중계하는 중앙 메시지 서버.
- **QoS(Quality of Service)**: MQTT에서 메시지 전달 신뢰성을 보장하기 위해 정의된 3단계 전송 품질 등급(0, 1, 2).

</details>

- 정의: TCP/IP 기반의 **최소 2바이트 고정 헤더를 갖는 경량 발행-구독(Publish/Subscribe) 메시징 프로토콜**
- 배경/필요성: HTTP의 무거운 헤더 오버헤드와 요청-응답(Request-Response) 동기식 구조를 극복하고, 저전력 MCU 및 간헐적 무선망 환경에서 신뢰성 높은 텔레메트리 전송을 지원하기 위해 개발

#### 한줄 요약

- 최소 헤더 오버헤드와 발행-구독 아키텍처로 IoT 기기의 효율적 데이터 중계를 지원하는 표준 프로토콜

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **토픽(Topic)**: 슬래시(`/`) 계층 구조(예: `home/sensor/temp`)로 정의되는 메시지 라우팅 주소.
- **유언 메시지(Last Will and Testament, LWT)**: 클라이언트가 비정상 단절될 때 브로커가 대리로 다른 구독자들에게 전송하는 사전 정의 메시지.

</details>

- **초경량 헤더 구조**: 최소 2바이트 고정 헤더로 네트워크 대역폭 및 배터리 소모 최소화
- **비동기 발행-구독 모델**: 송신자(Publisher)와 수신자(Subscriber) 간의 시간·공간적 완전한 디커플링(Decoupling) 제공
- **3단계 신뢰성 전송(QoS 0/1/2)**: 서비스 중요도에 따른 유연한 전달 보장 메커니즘 지원
- **상태 보존(Retained Message & LWT)**: 신규 접속 기기를 위한 최신 상태 보존 및 비정상 단절 시 유언 메시지 자동 배포

#### 한줄 요약

- 초경량 헤더, 비동기 디커플링, 3단계 QoS, LWT 단절 알림을 통해 안정적인 IoT 통신 구현

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Keep Alive**: 클라이언트와 브로커 간 주기적인 PINGREQ/PINGRESP 교환을 통해 TCP 연결 생존 여부를 모니터링하는 타이머.

</details>

```text
[ 발행자 (Publisher: IoT 센서 기기) ]
                │
                │ PUBLISH (Topic: factory/temp, Payload: 25.4°C)
                ▼
      [ MQTT 브로커 (Broker) ] ◄── (Topic 트리 관리, QoS 필터링, Retained 캐시)
                │
                ├───────────────────────────────┐
                ▼ (Topic 매칭 중계)              ▼ (Topic 매칭 중계)
[ 구독자 A (Control Server) ]       [ 구독자 B (Mobile Dashboard) ]
```

선의 의미: 발행자가 브로커로 메시지를 전송하고, 브로커가 등록된 토픽 트리에 따라 다중 구독자에게 메시지를 라우팅하는 관계

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| 발행자 (Publisher) | 센서 데이터를 수집하여 특정 토픽 경로에 **메시지를 생성 및 전송하는 클라이언트** | IoT 단말 |
| MQTT 브로커 (Broker) | 클라이언트 연결 관리, **토픽 필터링, 메시지 큐잉 및 라우팅을 수행하는 중앙 서버** | EMQX, Mosquitto |
| 구독자 (Subscriber) | 특정 토픽(단일/와일드카드)을 등록하여 **관심 메시지를 비동기로 수신하는 클라이언트** | 서버, 대시보드 |
| 토픽 (Topic) | `/` 구분자를 사용하는 **계층형 메시지 분배 경로 (`+`, `#` 와일드카드 지원)** | Routing Key |
| 세션 (Session) | Clean Session 플래그에 따라 **클라이언트 오프라인 중 미전송 QoS 1/2 메시지 보관** | State Store |

#### 한줄 요약

- 발행자, 브로커, 구독자 3계층이 토픽 기반 계층 라우팅을 통해 메시지를 교환하는 구조

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Clean Session**: 세션 수립 시 `CleanSession=true`이면 기존 세션 상태를 초기화하고, `false`이면 오프라인 중 발생한 메시지를 복원하는 설정 플래그.

</details>

```text
[ 1. 클라이언트: CONNECT 패킷 전송 (Keep Alive, Auth, CleanSession 설정) ]
                       │
                       ▼
[ 2. 브로커: CONNACK 응답 및 세션 수립 ]
                       │
                       ▼
[ 3. 구독자: SUBSCRIBE 요청 (Topic: factory/+, QoS 지정) ──► SUBACK 수신 ]
                       │
                       ▼
[ 4. 발행자: PUBLISH 패킷 전송 (Topic, Payload, QoS 등급) ]
                       │
                       ▼
[ 5. 브로커: 토픽 트리 매칭 후 구독자에게 PUBLISH 전달 및 QoS별 ACK 완결 ]
```

**동작 원리**

1. **연결 수립**: 클라이언트가 브로커로 `CONNECT` 요청 후 `CONNACK` 수신하여 TCP 세션 바인딩
2. **토픽 구독**: 구독자가 수신할 토픽 필터와 희망 QoS를 담아 `SUBSCRIBE` 전송 후 `SUBACK` 확인
3. **메시지 발행**: 발행자가 데이터와 QoS를 지정하여 브로커로 `PUBLISH` 패킷 전송
4. **라우팅 및 전달**: 브로커가 토픽 트리를 탐색하여 일치하는 모든 구독자에게 메시지 복제 전달
5. **QoS 핸드셰이크**: 지정된 QoS 레벨에 따라 단방향 전송(0), 2단계 확인(1), 4단계 핸드셰이크(2) 완결

#### 한줄 요약

- 연결 수립 $\to$ 토픽 구독 $\to$ 메시지 발행 $\to$ 브로커 라우팅 $\to$ QoS 레벨별 전달 완결

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **QoS 0 (At most once)**: 확인 응답 없이 1회 전송하며 네트워크 단절 시 패킷이 유실될 수 있는 최저 오버헤드 모드.
- **QoS 1 (At least once)**: 수신 확인(PUBACK)을 받을 때까지 재전송하여 최소 1회 전달을 보장하나 중복 가능성이 있는 모드.
- **QoS 2 (Exactly once)**: 4단계 핸드셰이크(PUBREC-PUBREL-PUBCOMP)를 통해 메시지의 중복 없는 유일한 1회 전달을 보장하는 최고 신뢰성 모드.

</details>

| MQTT QoS 등급 | **QoS 0 (At most once)** | **QoS 1 (At least once)** | **QoS 2 (Exactly once)** |
|:---|:---|:---|:---|
| 적용 기준 | 주기적 환경 센서 등 **패킷 유실을 허용하는 저비용 텔레메트리** | 상태 알람, 장비 이벤트 등 **유실은 불가하나 중복 처리가 가능한 경우** | 과금 트랜잭션, 제어 명령 등 **중복 실행 시 치명적 오류가 발생하는 경우** |
| 핵심 특징 | **Fire-and-Forget 단방향 전송**, 확인 응답 패킷 없음 | **PUBACK 수신 시까지 재전송**, 패킷 중복 전달 가능 | **4-Way 핸드셰이크 (PUBREC $\to$ PUBREL $\to$ PUBCOMP)** |
| 통신 오버헤드 | **최소 오버헤드 (1개 패킷)** | 보통 오버헤드 (2개 패킷) | **최대 오버헤드 (4개 패킷)** |
| 한계 | 네트워크 불안정 시 **데이터 유실 발생** | 재전송으로 인한 **수신단 중복 처리 로직 필수** | 빈번한 왕복 지연(RTT)으로 인한 **처리량 감소 및 배터리 소모** |

#### 한줄 요약

- 센서 모니터링은 QoS 0, 일반 이벤트 알림은 QoS 1, 크리티컬 원격 제어 및 결제는 QoS 2를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **토픽 와일드카드**: 단일 레벨 대체 `+`와 다중 하위 레벨 전체 대체 `#`를 지원하는 토픽 필터링 문법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수만 대 IoT 기기의 동시 재접속에 따른 **브로커 세션 고갈 및 트래픽 스톰** | **MQTT 클러스터링(EMQX/HiveMQ) 및 지수 백오프(Exponential Backoff) 재연결 적용** | 브로커 부하 분산 및 네트워크 폭주 방지 |
| 평문 전송 시 패킷 스니핑 및 **비인가 발행자에 의한 악성 토픽 오염** | **TLS/mTLS 상호 인증 및 토픽 레벨 RBAC(역할 기반 접근 제어) 적용** | 종단 간 암호화 및 비인가 기기의 토픽 접근 원천 차단 |
| QoS 1/2 세션 누적으로 인한 **브로커 인메모리 버퍼 고갈(OOM)** | **만료 시간(Message Expiry Interval) 설정 및 오프라인 큐 크기 제한** | 미전송 패킷 자동 정리 및 브로커 시스템 안정성 확보 |

#### 한줄 요약

- 브로커 클러스터링, mTLS 암호화, 토픽 인가 및 메시지 만료 설정을 통해 대규모 IoT 운영 안정성 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **MQTT 5.0**: 사용자 프로퍼티, 메시지/세션 만료 기간, 이유 코드(Reason Code), 공유 구독(Shared Subscription)을 추가한 최신 표준 규격.

</details>

- MQTT는 스마트 팩토리, 커넥티드 카(V2X), 스마트 홈 전반의 글로벌 사실상 표준(De-facto Standard) IoT 메시징 프로토콜이며, 최근 대규모 분산 환경 대응을 위해 MQTT 5.0의 공유 구독 기반 로드 밸런싱과 Kafka 연계를 통한 실시간 스트리밍 파이프라인 결합이 핵심 설계 패턴으로 자리잡고 있음

#### 한줄 요약

- 경량성과 3단계 QoS를 기반으로 현대 분산 IoT 인프라의 핵심 메시지 백본을 구축
