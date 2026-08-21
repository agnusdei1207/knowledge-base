---
sidebar:
  order: 82
  label: "082. SOME/IP (차량 이더넷 미들웨어)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "차량용 이더넷 SOA 미들웨어 : SOME/IP 및 SOME/IP-SD (Scalable service-Oriented MiddlewarE over IP)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 82
extra:
  question_no: "082"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "AUTOSAR 적응형 플랫폼, 서비스 지향 아키텍처(SOA), SOME/IP-SD 동적 서비스 디스커버리 및 E2E Protection"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SOME/IP(Scalable service-Oriented MiddlewarE over IP)**: 차량 내 고대역폭 이더넷(100BASE-T1/1000BASE-T1) 통신망에서 ECU 간의 결합도(Coupling)를 낮추고 서비스 기반 통신을 구현하기 위해 AUTOSAR 표준에 통합된 서비스 지향 아키텍처(SOA) 미들웨어 프로토콜.
- **서비스 지향 아키텍처(SOA, Service-Oriented Architecture)**: 하드웨어 물리 주소(IP/Port) 기반의 정적 점대점 통신을 탈피하여, 기능 단위의 서비스 인터페이스(Methods, Events, Fields)를 정의하고 이를 동적으로 탐색·호출·구독하는 분산 컴퓨팅 패러다임.

</details>

- 정의/개념: 차량용 IP 네트워크 상에서 서비스 제공자(Server)와 소비자(Client) 간의 **원격 프로시저 호출(RPC)**, **발행/구독(Pub/Sub)** 통신을 제공하고, **SOME/IP-SD(Service Discovery)** 를 통해 서비스 위치와 인스턴스를 런타임에 동적으로 바인딩하는 **AUTOSAR 표준 차량용 미들웨어**
- 배경/필요성: SDV(소프트웨어 정의 차량) 및 자율주행 도입으로 차량 내 소프트웨어 기능이 폭증함에 따라, 정적 신호 기반 통신(CAN Signal Matrix)의 확장성 한계를 극복하고 기능의 동적 추가 및 OTA 업데이트 유연성을 확보할 요구

#### 한줄 요약
- 차량용 이더넷 상에서 SOA 기반 동적 서비스 탐색(SD), RPC 및 이벤트 통신을 제공하는 AUTOSAR 미들웨어이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SOME/IP-SD(Service Discovery)**: UDP 멀티캐스트를 활용하여 서비스 제공자가 자신의 서비스(ServiceID, InstanceID, IP, Port)를 네트워크에 광고(Offer)하고, 소비자가 필요한 서비스를 탐색(Find) 및 구독(Subscribe)하도록 지원하는 프로토콜.
- **E2E 보호(End-to-End Protection)**: AUTOSAR 표준 규격(Profile 01~07)에 따라 데이터 무결성을 보장하기 위해 페이로드 헤더에 데이터 ID, 카운터(Counter), CRC 체크섬을 결합하여 전송 오류 및 재전송 공격(Replay Attack)을 방어하는 안전 메커니즘.

</details>

- **경량 직렬화(Lightweight Serialization)**: 차량용 임베디드 리소스 제약을 고려하여 헤더 오버헤드를 16바이트로 최소화하고 Big-Endian 기반 구조체 직렬화 수행
- **동적 서비스 런타임 바인딩**: 컴파일 타임의 하드코딩된 IP 연결 대신 런타임에 SOME/IP-SD를 통해 서비스 제공자의 IP/Port를 동적 매핑
- **다양한 통신 패턴 지원**: 동기식 요청-응답(Request-Response), 단방향 알림(Fire & Forget), 비동기 이벤트 스트리밍(Event/Field Notification) 제공

#### 한줄 요약
- 경량 직렬화, SOME/IP-SD 동적 서비스 디스커버리, E2E 기능 안전 보호를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SOME/IP 헤더(16바이트 고정)**: Service ID(16bit), Method/Event ID(16bit), Length(32bit), Client ID(16bit), Session ID(16bit), Protocol Version(8bit), Interface Version(8bit), Message Type(8bit), Return Code(8bit)로 구성.

</details>

```text
[ 서비스 소비자 (Client ECU) ] ──▶ [ SOME/IP 클라이언트 런타임 ]
                                           │
                                           ├─ (1. SOME/IP-SD: FindService / Subscribe)
                                           │
                                           ▼ (2. SOME/IP over TCP/UDP: Method Call / Event)
[ 서비스 제공자 (Server ECU) ] ──▶ [ SOME/IP 서버 런타임 (Service Host) ]
                                           │
                                           └─ (OfferService / EventGroup Multicast)
```

선의 의미: Client와 Server가 SOME/IP-SD를 통해 서비스 위치를 파악하고 구독을 수립한 후, L4 UDP/TCP 상에서 SOME/IP 메시지를 송수신하는 아키텍처

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **SOME/IP Core** | 메시지 헤더 조립, 데이터 구조체 직렬화/역직렬화(Serialization) 및 RPC 라우팅 | L7 미들웨어 계층 |
| **SOME/IP-SD** | 서비스 광고(Offer), 서비스 탐색(Find), 이벤트 그룹 구독(Subscribe) 관리 | UDP 포트 30490 |
| **E2E Protection** | ASIL-D 기능 안전 요건을 충족하기 위해 데이터 카운터 및 CRC 계산/검증 | ISO 26262 준수 |
| **AUTOSAR RTE** | 애플리케이션 SW-C와 SOME/IP 통신 스택 간의 추상화 인터페이스 제공 | Adaptive / Classic |

#### 한줄 요약
- SOME/IP Core, SOME/IP-SD 디스커버리, E2E 보호 모듈, AUTOSAR RTE가 결합하여 SOA 통신을 완성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **이벤트 그룹(Event Group)**: 관련된 복수의 이벤트(Events) 및 필드(Fields)를 하나의 논리적 그룹으로 묶어 소비자가 단 한 번의 요청으로 일괄 구독할 수 있도록 정의한 집합.
- **TTL(Time To Live)**: OfferService 또는 Subscribe 메시지의 유효 수명(초 단위)을 지정하여, 갱신이 없을 경우 서비스 연결을 자동 해제하는 타이머.

</details>

```text
1. 서비스 제공자(Server)가 부팅 후 자신의 ServiceID 및 엔드포인트(IP/Port)를 담은 OfferService 멀티캐스트 송출
            │
            ▼
2. 서비스 소비자(Client)가 FindService를 발송하거나 수신된 OfferService의 인터페이스 버전 무결성 검증
            │
            ▼
3. 소비자가 필요한 데이터 스트림 수신을 위해 SubscribeEventGroup 메시지를 제공자로 유니캐스트 전송
            │
            ▼
4. 제공자가 Subscribe-ACK를 회신하여 세션 수립 ➔ 상태 변경 발생 시 E2E 보호가 적용된 Event 메시지 송출
            │
            ▼
5. 만료 전 Offer/Subscribe 갱신(Refresh) ➔ TTL 만료 시 비정상 노드로 간주하고 연결 세션 자동 폐기
```

**동작 원리**

1. **서비스 공지**: 서버가 주기적으로 `SOME/IP-SD OfferService`를 브로드캐스트/멀티캐스트하여 서비스 상태 알림
2. **호환성 검증**: 클라이언트가 서비스의 Major/Minor Interface Version을 대조하여 직렬화 호환성 판정
3. **구독 수립**: 클라이언트가 특정 이벤트 그룹에 대해 구독 요청을 전송하고 서버가 ACK 승인
4. **실시간 통신**: UDP(저지연 이벤트) 또는 TCP(대용량 데이터)를 통해 E2E 헤더가 부착된 페이로드 전송
5. **생애주기 관리**: 주기적 갱신 메시지로 연결을 유지하며, 통신 장애 시 즉각 타임아웃 처리

#### 한줄 요약
- OfferService 광고, FindService 매칭, Subscribe 구독, E2E 보호 통신, TTL 기반 갱신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Request/Response vs Fire & Forget vs Event/Field**: 반환값이 필수적인 RPC, 반환값 없는 일방 통보, 상태 변경 시 발행되는 구독형 데이터 통신.

</details>

| 통신 메시지 유형 | Message Type 코드 | 통신 동작 및 특성 | 대표 적용 사례 |
|:---|:---|:---|:---|
| **Request / Response** | `REQUEST(0x00)` / `RESPONSE(0x80)` | 클라이언트 호출 후 서버가 연산 결과를 동기/비동기 응답 | 도어 락 제어, 진단 서비스(DoIP) |
| **Fire & Forget** | `REQUEST_NO_RETURN(0x01)` | 클라이언트가 호출만 수행하고 서버 응답을 대기하지 않음 | 턴 시그널(방향지시등) 점멸 명령 |
| **Event Notification** | `NOTIFICATION(0x02)` | 상태 변경 또는 주기 도래 시 구독 클라이언트에 데이터 발행 | 휠 스피드, 카메라 객체 인식 데이터 |
| **Field Notification** | `NOTIFICATION(0x02)` | Getter, Setter, Notifier를 결합한 속성(Property) 제어 | 공조 온도 설정(Set) 및 현재 온도 조회 |

#### 한줄 요약
- Request/Response는 양방향 제어, Fire & Forget은 단방향 통보, Notification은 데이터 스트리밍에 사용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **계약 테스트(Contract Testing)**: 서버와 클라이언트 개발 부서가 사전에 정의한 ARXML 인터페이스 명세(자료형, 엔디안, 패딩)와 실제 구현체가 100% 일치하는지 자동 검증하는 프로세스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ECU 소프트웨어 업데이트 후 인터페이스 버전 불일치로 인한 역직렬화 런타임 크래시 | **SOME/IP 인터페이스 버전(Major/Minor) 검증** 및 사전 **계약 테스트(Contract Test)** 수행 | 런타임 파싱 오류 원천 차단 및 무중단 호환성 보증 |
| 차량 시동 시 수백 개 ECU의 동시 SOME/IP-SD 브로드캐스트로 인한 이더넷 대역폭 고갈 | **SD 메시지 지수 백오프(Exponential Back-off)** 및 초기 지연(Initial Delay) 셔플링 | 시동 초기 트래픽 폭풍(Broadcast Storm) 억제 및 안정적 망 개통 |
| 차량 통신 버스 상의 제어 메시지 위변조 및 재전송 공격(Replay Attack) 위협 | **AUTOSAR E2E Profile(Counter + Data ID + CRC)** 및 SecOC(암호학적 MAC) 적용 | ASIL-D 기능 안전 요건 충족 및 악성 패킷 재전송 원천 무력화 |

#### 한줄 요약
- 인터페이스 버전 검증으로 직렬화 오류를 차단하고, 지수 백오프로 SD 폭풍을 방어하며, E2E Protection으로 위변조를 방지한다.

## Ⅶ. 결론

- 자율주행 및 SDV(소프트웨어 정의 차량) 전환에 대응하여 차량 내부 E/E 아키텍처의 유연성을 극대화하기 위해 **SOME/IP 기반의 서비스 지향 아키텍처(SOA)** 를 도입하되, 실시간 기능 안전(ISO 26262) 및 보안 요건을 충족하기 위해 **AUTOSAR E2E Protection**, **SOME/IP-SD 트래픽 최적화**, **Automotive Ethernet(TSN)** 과의 통합 연계를 통해 고성능 차량용 소프트웨어 플랫폼을 완성

#### 한줄 요약
- SOME/IP 미들웨어와 SOME/IP-SD 및 E2E 보호 기술을 결합하여 SDV 시대의 차량용 SOA 네트워크를 실현한다.
