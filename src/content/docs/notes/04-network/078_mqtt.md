---
sidebar:
  order: 78
  label: "078. MQTT 프로토콜"
  badge:
    text: "기출 · 50%"
    variant: note
title: "경량 IoT 메시징 프로토콜 : MQTT (Message Queuing Telemetry Transport)"
date: "2026-08-26T14:05:00+09:00"
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

- 정의/개념: 2바이트 헤더와 **Pub/Sub·3단계 QoS**의 경량 프로토콜
- 배경/필요성: HTTP는 요청마다 수백 바이트 헤더와 폴링 왕복을 반복해 **배터리·대역폭 비용**을 상시 지불하므로, 2바이트 고정 헤더와 브로커 중계를 두어 폴링 자체를 발행-구독 푸시로 대체

#### 한줄 요약
- **2바이트 헤더·Pub/Sub·3단계 QoS** 기반 IoT 통신

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Retained Message**: 브로커가 특정 토픽의 마지막 유효 메시지를 캐싱하여 신규 구독자가 접속하자마자 즉시 최신 상태를 전달받게 하는 기능.
- **LWT (Last Will and Testament)**: 클라이언트가 비정상 단절될 때 브로커가 대리로 다른 구독자들에게 전송하는 유언 메시지.

</details>

- **2바이트 헤더**: 대역폭과 배터리 소모 절감
- **비동기 Pub/Sub**: 송수신자의 시간·공간 결합 제거
- **QoS 0·1·2**: 유실 허용부터 정확히 한 번까지 선택
- **Retained Message·LWT**: 상태 캐시와 단절 알림 제공

#### 한줄 요약
- 초경량 헤더, 비동기 디커플링, 3단계 QoS, LWT 단절 알림을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Topic Tree & Wildcard**: `/`로 구분되는 계층 경로로 단일 레벨 대체 `+`와 하위 전체 대체 `#` 와일드카드를 지원하는 라우팅 키.

</details>

```text
[MQTT 정적 구성]
|-- 발행자
|-- MQTT 브로커
|-- 구독자
|-- 토픽
`-- 세션
```

선의 의미: 발행자가 브로커로 메시지를 전송하고 브로커가 등록된 토픽 트리에 따라 다중 구독자에게 메시지를 라우팅하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 발행자 | 토픽에 **메시지 발행** | IoT 단말 |
| MQTT 브로커 | **토픽 필터링·큐잉·라우팅** | EMQX, HiveMQ |
| 구독자 | 관심 토픽의 **메시지 비동기 수신** | 서버, 대시보드 |
| 토픽 | `+`, `#` 지원 **계층형 라우팅 키** | Routing Path |
| 세션 | 오프라인 **QoS 1·2 메시지 보관** | State Store |

#### 한줄 요약
- 브로커가 발행자와 구독자 사이에 끼어들어 상대 주소와 접속 시점을 대신 관리하므로, 단말은 서로의 존재를 몰라도 통신하고 절전 중 메시지는 세션 스토어가 보관한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **4-Way QoS 2 Handshake**: PUBLISH $\rightarrow$ PUBREC(수신 확인) $\rightarrow$ PUBREL(발행 릴리즈) $\rightarrow$ PUBCOMP(완료)로 이어지는 중복 제거 트랜잭션.

</details>

```text
클라이언트 요청
    |
1. CONNECT·CONNACK
    |
2. SUBSCRIBE·SUBACK
    |
3. PUBLISH 송출
    |
4. 토픽 트리 라우팅
    |
5. QoS별 전달 완료
    |
구독자 수신
```

- 1. CONNECT·CONNACK
- 2. SUBSCRIBE·SUBACK
- 3. PUBLISH 송출
- 4. 토픽 트리 라우팅
- 5. QoS별 전달 완료

#### 한줄 요약
- QoS 레벨 선택에서 전달 보장 강도와 왕복 횟수가 함께 갈리며, QoS 2는 4단계 핸드셰이크 비용을 치르고 중복 없는 1회 전달을 산다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **QoS 0 vs QoS 1 vs QoS 2**: 최대 1회(유실 가능), 최소 1회(중복 가능), 정확히 1회(중복 없음).

</details>

| 비교 항목 | QoS 0 (At most once) | QoS 1 (At least once) | QoS 2 (Exactly once) |
|:---|:---|:---|:---|
| 메시지 전달 보장 | **최대 1회** | **최소 1회** | **정확히 1회** |
| 핸드셰이크 절차 | **응답 없음** | **PUBACK** | **PUBREC·PUBREL·PUBCOMP** |
| 통신 오버헤드 | **최소** | 보통 | **최대** |
| 네트워크 단절 시 | 유실 허용 | 재전송·중복 가능 | Packet ID로 중복 제거 |
| 대표 적용 서비스 | 주기 센서 | 장비 알람·로그 | **과금·긴급 제어** |

#### 한줄 요약
- QoS 0은 단순 센서용, QoS 1은 일반 이벤트용, QoS 2는 미션 크리티컬 제어용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shared Subscription (공유 구독, MQTT 5.0)**: `$share/group/topic` 문법으로 다수의 백엔드 컨슈머가 단일 토픽의 메시지를 라운드로빈 부하 분산 처리하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동시 재접속으로 세션 고갈 | **클러스터링·지수 백오프** | 연결 폭주 방지 |
| 평문 도청·악성 토픽 오염 | **mTLS·토픽 RBAC** | 기밀성·접근 통제 |
| QoS 1·2 누적으로 메모리 고갈 | **Message Expiry·큐 제한** | 만료 패킷 회수 |
| 단일 컨슈머 처리 병목 | **MQTT 5.0 공유 구독** | 부하 분산·확장 |

#### 한줄 요약
- **백오프·mTLS·메시지 만료·공유 구독** 적용

## Ⅶ. 결론

- 유실 허용 센서는 **QoS 0**, 중복 불가 제어는 **QoS 2·mTLS** 선택

#### 한줄 요약
- **Pub/Sub·QoS** 선택으로 경량성과 전달 신뢰성 균형
