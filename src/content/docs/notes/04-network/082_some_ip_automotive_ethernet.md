---
sidebar:
  order: 82
  label: "082. SOME/IP 차량 이더넷 미들웨어"
  badge:
    text: "기출 · 30%"
    variant: note
title: "차량용 이더넷 SOA 미들웨어 : SOME/IP 및 SOME/IP-SD"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 차량용 이더넷 상에서 ECU 간 RPC, Pub/Sub 통신, **SOME/IP-SD** 서비스 탐색 및 E2E 보호를 제공하는 AUTOSAR 표준 SOA 미들웨어 기술
- 배경/필요성: 자율주행, ADAS, 고화질 인포테인먼트(IVI) 도입으로 인해 차량 내부 데이터 처리량이 수십 Mbps~수 Gbps로 급증하고 전자제어 아키텍처가 존(Zone) 기반의 소프트웨어 정의 차량(SDV)으로 전환되는 환경에서, 전통적인 CAN 버스의 신호 기반(Signal-based) 정적 브로드캐스팅 방식은 대역폭 한계와 신규 기능 추가 시 전 ECU의 데이터베이스(DBC)를 재빌드해야 하는 강한 결합(Tight Coupling)의 한계를 노출함에 따라, 차량용 이더넷(Automotive Ethernet) 상에서 서비스 인터페이스 기반으로 동작하는 AUTOSAR 표준 SOA 미들웨어인 SOME/IP 및 런타임 서비스 탐색 프로토콜(SOME/IP-SD)을 도입하여 기가비트급 대용량 제어/센서 데이터 전송, 런타임 동적 플러그앤플레이 서비스 바인딩 및 기능 안전(E2E Protection) 보증을 달성할 필요

#### 한줄 요약
- 신호 기반 CAN이 기능 추가마다 전 ECU 재빌드 비용을 치르는 강한 결합을, 서비스 인터페이스와 **SOME/IP-SD** 런타임 탐색 계층으로 풀어 대역폭과 결합도를 함께 낮춘다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lightweight Serialization**: 헤더 오버헤드를 16바이트로 최소화하고 Big-Endian 기반 구조체 직렬화를 수행하는 경량 데이터 변환.
- **E2E Protection (AUTOSAR)**: Data ID·카운터·CRC로 통신 오류를 검출하는 기능 안전 메커니즘.

</details>

- 경량 직렬화(**Lightweight Serialization**): 헤더 오버헤드를 16바이트로 최소화하고 Big-Endian 기반 구조체 직렬화 수행
- 동적 서비스 런타임 바인딩: 컴파일 타임 하드코딩 대신 **SOME/IP-SD**를 통해 서비스 제공자 IP/Port 동적 매핑
- 다양한 통신 패턴 지원: 동기식 요청-응답(RPC), 단방향 알림(Fire & Forget), 비동기 이벤트 스트리밍(Pub/Sub) 제공

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
| SOME/IP Core | **SOME/IP Header** 직렬화와 RPC·이벤트 메시지 처리 |
| **SOME/IP-SD** | 서비스 광고·탐색·구독 관리 |
| **E2E Protection** | 카운터·Data ID·CRC 오류 검출 |
| AUTOSAR RTE | 응용과 통신 스택 사이 인터페이스 제공 |

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

분기 결과: 버전 대조에 실패한 OfferService는 구독 단계로 넘어가지 못하고, 통과한 클라이언트만 **Event Group** 단위로 일괄 구독한 뒤 TTL 갱신 여부에 따라 세션이 유지되거나 폐기된다.

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
- **SOME/IP-TP (Transport Protocol)**: UDP MTU를 넘는 페이로드를 세그먼트로 나누고 헤더의 오프셋·More Segments 플래그로 수신 측이 재조립하게 하는 SOME/IP 분할 전송 확장.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ECU 소프트웨어 업데이트 후 버전 불일치로 인한 역직렬화 런타임 크래시 | 인터페이스 Major/Minor 버전 검증 및 **Contract Testing** | 런타임 파싱 오류 원천 차단 및 호환성 보증 |
| 차량 시동 시 수백 개 ECU의 동시 SD 브로드캐스트로 트래픽 폭풍 발생 | SD 초기 지연 랜덤화 및 반복 주기 지수 백오프(Exponential Back-off) | 시동 초기 Broadcast Storm 억제 |
| 차량 통신 버스 상의 제어 메시지 위변조 및 재전송 공격(Replay Attack) 위협 | **E2E Protection** Profile(Counter+Data ID+CRC) 및 SecOC 적용 | 기능 안전 오류 검출 및 악성 패킷 재전송 차단 |
| 대용량 비디오 스트리밍 시 UDP 버퍼 오버플로우 패킷 손실 | **SOME/IP-TP** 세그멘테이션 또는 TCP 전환 | 대용량 페이로드 무손실 분할 수용 |

#### 한줄 요약
- SOA가 CAN에서 가져온 유연성은 런타임에야 드러나는 실패(버전 불일치·스톰·분할)를 낳으므로, 대책의 초점은 결합 실패를 설계 시점의 계약 검증으로 앞당기는 데 있다.

## Ⅶ. 결론

- 전통적인 분산 ECU 제어 방식에서 중앙 집중형 존(Zonal) 아키텍처와 소프트웨어 정의 차량(SDV: Software-Defined Vehicle)으로 전환되는 자동차 산업의 가장 핵심적인 차량용 이더넷 서비스 지향 통신(SOA) 미들웨어 표준으로 확립되었으며, 고성능 자율주행 컴퓨터의 DDS(Data Distribution Service) 및 차량-클라우드(V2C) 연동 프로토콜과 융합하는 가운데, 실무 SDV 플랫폼 구축 시에는 차량 시동 시 브로드캐스트 스톰을 방지하는 **SOME/IP-SD** 지수 백오프(Exponential Backoff) 적용, 인터페이스 파편화 크래시를 방지하는 엄격한 Major/Minor 버전 **계약 테스트**(Contract Testing), ISO 26262 ASIL-D 기능 안전 무결성을 만족하는 AUTOSAR E2E Profile(CRC+Counter) 및 SecOC 암호화 인증, 대용량 센서 데이터 처리를 위한 **SOME/IP-TP** 세그멘테이션을 결합하여 완벽한 차세대 차량 네트워크 신뢰성을 완성

#### 한줄 요약
- SOME/IP 미들웨어와 SOME/IP-SD 및 E2E 보호 기술을 결합하여 SDV 시대의 차량용 SOA 네트워크를 실현한다.
