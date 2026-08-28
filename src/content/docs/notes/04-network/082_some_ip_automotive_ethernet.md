---
sidebar:
  order: 82
  label: "082. SOME/IP 차량 이더넷 미들웨어"
  badge:
    text: "기출 · 30%"
    variant: note
title: "차량용 이더넷 SOA 미들웨어 : SOME/IP 및 SOME/IP-SD"
date: "2026-08-26T14:00:13+09:00"
tags:
  - "notes-network"
weight: 82
extra:
  question_no: "82"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "AUTOSAR 적응형 플랫폼, 서비스 지향 아키텍처(SOA), SOME/IP-SD 동적 서비스 디스커버리 및 E2E Protection"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SOME/IP**: 차량용 이더넷 상에서 ECU 간 서비스 지향 통신(SOA)을 구현하는 AUTOSAR 표준 L7 미들웨어 프로토콜.
- **SOME/IP-SD (Service Discovery)**: 런타임에 서비스의 제공(Offer), 탐색(Find), 이벤트 구독(Subscribe)을 동적으로 처리하는 플러그 앤 플레이 모듈.

</details>

- 정의/개념: 차량용 이더넷 상에서 ECU 간 **RPC, Pub/Sub 통신, SOME/IP-SD 서비스 탐색 및 E2E 보호를 제공하는 AUTOSAR 표준 SOA 미들웨어 기술**
- 배경/필요성: CAN의 신호 기반 정적 브로드캐스팅은 기능을 추가할 때마다 **전 ECU의 메시지 정의를 함께 고치는 강한 결합(Tight Coupling) 비용**을 치르므로, 이더넷 위에 서비스 단위 인터페이스와 동적 디스커버리를 두어 통신 상대 결정을 실행 시점으로 미룸

#### 한줄 요약
- 경량 직렬화, SOME/IP-SD 동적 서비스 디스커버리, E2E 기능 안전 보호를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lightweight Serialization**: 헤더 오버헤드를 16바이트로 최소화하고 Big-Endian 기반 구조체 직렬화를 수행하는 경량 데이터 변환.
- **E2E Protection (AUTOSAR)**: Data ID·카운터·CRC로 통신 오류를 검출하는 기능 안전 메커니즘.

</details>

- **경량 직렬화(Lightweight Serialization)**: 헤더 오버헤드를 **16바이트로 최소화하고 Big-Endian 기반 구조체 직렬화** 수행
- **동적 서비스 런타임 바인딩**: 컴파일 타임 하드코딩 대신 **SOME/IP-SD를 통해 서비스 제공자 IP/Port 동적 매핑**
- **다양한 통신 패턴 지원**: 동기식 요청-응답(RPC), 단방향 알림(Fire & Forget), 비동기 이벤트 스트리밍(Pub/Sub) 제공

#### 한줄 요약
- 런타임 바인딩으로 얻은 확장 유연성의 대가로 직렬화·디스커버리 오버헤드와 실행 시점 결합 실패 가능성을 떠안는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SOME/IP Header (16B)**: Service ID(16b), Method ID(16b), Length(32b), Client ID(16b), Session ID(16b), Message Type(8b) 등으로 구성.

</details>

```text
[SOME/IP 통신 체계]
|-- 클라이언트 ECU
|-- 차량용 이더넷
`-- 서버 ECU
    |-- SOME/IP Core
    |-- SOME/IP-SD
    |-- E2E Protection
    `-- AUTOSAR RTE
```

선의 의미: Client와 Server가 SOME/IP-SD를 통해 서비스 위치를 파악하고 구독을 수립한 후 L4 UDP/TCP 상에서 SOME/IP 메시지를 송수신하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **SOME/IP Core** | 직렬화와 RPC·이벤트 메시지 처리 |
| **SOME/IP-SD** | 서비스 광고·탐색·구독 관리 |
| **E2E Protection** | 카운터·Data ID·CRC 오류 검출 |
| **AUTOSAR RTE** | 응용과 통신 스택 사이 인터페이스 제공 |

#### 한줄 요약
- SOME/IP-SD가 통신 상대 탐색을 런타임으로 옮기고 E2E 보호 모듈이 전송 경로와 무관하게 무결성을 책임지므로, 애플리케이션은 상대 ECU의 위치와 전송망 구성을 알 필요가 없다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Event Group**: 관련된 복수의 이벤트/필드를 하나의 논리적 그룹으로 묶어 단 한 번의 요청으로 일괄 구독하게 하는 집합 단위.

</details>

```text
SOME/IP-SD 서비스 탐색, 구독 및 이벤트 전송 파이프라인
        │
   1. [OfferService 공지] 서버가 부팅 후 자신의 ServiceID 및 엔드포인트(IP/Port) 멀티캐스트 송출
        │
   2. [인터페이스 버전 대조] 클라이언트가 수신된 OfferService의 Major/Minor 버전 호환성 검증
        │
   3. [이벤트 그룹 구독] 클라이언트가 SubscribeEventGroup 유니캐스트 요청 전송
        │
   4. [Subscribe-ACK 승인] 서버가 구독 승인 회신 ➔ 상태 변경 발생 시 E2E 보호된 Event 메시지 송출
        │
   ▼
5. [TTL 수명주기 관리] 만료 전 주기적 갱신(Refresh) ➔ 장애로 인한 TTL 만료 시 세션 자동 폐기
```

- 1. OfferService 공지: 서버 엔드포인트 광고
- 2. 인터페이스 버전 대조: 계약 호환성 확인
- 3. 이벤트 그룹 구독: 구독 요청 전송
- 4. Subscribe-ACK 승인: 승인 후 이벤트 발행
- 5. TTL 수명주기 관리: 갱신 또는 만료 처리

#### 한줄 요약
- TTL 갱신 성공 여부에서 서비스 유지와 해제로 갈리며, 주기적 광고 트래픽을 지불하는 대가로 ECU 교체·추가를 재구성 없이 흡수한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Request/Response vs Fire & Forget vs Event vs Field**: 양방향 RPC, 단방향 통보, 이벤트 스트리밍, 속성 Get/Set.

</details>

| 통신 메시지 유형 | Message Type 코드 | 통신 동작 및 특성 | 대표 적용 사례 |
|:---|:---|:---|:---|
| Request / Response | `REQUEST` / `RESPONSE` | 호출과 결과 응답 | 도어 제어·진단 |
| Fire & Forget | `REQUEST_NO_RETURN` | 응답 없는 단방향 호출 | 단순 제어 통보 |
| Event Notification | `NOTIFICATION` | 구독자에 상태·주기 이벤트 발행 | 센서 상태 발행 |
| Field | Getter·Setter·Notifier | 속성 조회·변경·통지 | 공조 설정·조회 |

#### 한줄 요약
- Request/Response는 양방향 제어, Fire & Forget은 단방향 통보, Notification은 데이터 스트리밍에 사용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Contract Testing (계약 테스트)**: 사전에 정의한 ARXML 인터페이스 명세와 실제 ECU 펌웨어 구현체가 100% 일치하는지 자동 검증하는 프로세스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ECU 소프트웨어 업데이트 후 버전 불일치로 인한 **역직렬화 런타임 크래시** | **`SOME/IP 인터페이스 버전(Major/Minor) 검증` 및 계약 테스트** | 런타임 파싱 오류 원천 차단 및 무중단 호환성 보증 |
| 차량 시동 시 수백 개 ECU의 동시 SD 브로드캐스트로 **트래픽 폭풍 발생** | **`SD 메시지 지수 백오프(Exponential Back-off)` 및 초기 지연 셔플링** | 시동 초기 Broadcast Storm 억제 및 안정적 망 개통 |
| 차량 통신 버스 상의 제어 메시지 위변조 및 재전송 공격(Replay Attack) 위협 | **`AUTOSAR E2E Profile (Counter + Data ID + CRC)` 및 SecOC 적용** | ASIL-D 기능 안전 충족 및 악성 패킷 재전송 원천 차단 |
| 대용량 비디오 스트리밍 시 UDP 버퍼 오버플로우 패킷 손실 | **`SOME/IP TP (Transport Protocol)` 세그멘테이션 및 TCP 전환** | 대용량 페이로드 무손실 분할 수용 |

#### 한줄 요약
- 인터페이스 버전 검증, 지수 백오프, E2E Protection/SecOC, SOME/IP TP 분할로 운영한다.

## Ⅶ. 결론

- 동적 차량 서비스는 **SOME/IP-SD**, 오류 검출은 E2E 적용

#### 한줄 요약
- SOME/IP 미들웨어와 SOME/IP-SD 및 E2E 보호 기술을 결합하여 SDV 시대의 차량용 SOA 네트워크를 실현한다.
