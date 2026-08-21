---
sidebar:
  order: 79
  label: "079. OPC UA (산업 표준 통신)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "스마트 팩토리 산업용 상호운용 표준 통신 : OPC UA (Open Platform Communications Unified Architecture)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 79
extra:
  question_no: "079"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "객체 지향 정보 모델(Address Space), 보안 프로파일(X.509 PKI), C/S 및 Pub/Sub(TSN 연동)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OPC UA(Open Platform Communications Unified Architecture)**: 산업 자동화 및 스마트 팩토리 분야에서 이기종 설비(PLC, CNC, 센서)와 상위 시스템(SCADA, MES, ERP, 클라우드) 간의 안전하고 신뢰성 있는 데이터 교환을 위해 OPC Foundation이 표준화한 플랫폼 독립적(OS-agnostic) 서비스 지향 통신 프로토콜 (IEC 62541).
- **시맨틱 정보 모델(Semantic Information Model)**: 단순한 원시 수치값(Raw Data)만을 전송하는 것을 넘어, 데이터의 이름, 엔지니어링 단위(Unit), 센서 위치, 범위(Range), 장비 메타데이터를 객체 지향적(Object-Oriented) 노드 구조로 함께 캡슐화하여 제공하는 데이터 모델.

</details>

- 정의/개념: 이기종 산업 설비 간의 벤더 종속성을 제거하기 위해 **주소 공간(Address Space)** 기반의 시맨틱 정보 모델, **계층화된 종단 보안(X.509/TLS)** 및 **Client/Server 및 Pub/Sub 통신 모델**을 통합 제공하는 **산업용 개방형 상호운용성 표준 아키텍처**
- 배경/필요성: 기존 OPC Classic의 Microsoft COM/DCOM 기술 종속성, 방화벽 통과 불가, 보안성 결여 문제를 해결하고, 크로스 플랫폼(Linux, RTOS, 임베디드) 환경에서 IT/OT 융합 통신을 실현할 요구

#### 한줄 요약
- 플랫폼 독립적 정보 모델과 X.509 다계층 보안을 통해 IT와 OT 간의 상호운용성을 보장하는 산업용 통신 표준이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **주소 공간(Address Space)**: 설비의 모든 데이터와 서비스 기능들을 노드(Node)와 노드 간의 관계(Reference)로 정의하여 계층적 트리 구조로 노출하는 OPC UA 서버 내부의 데이터베이스.
- **다계층 보안(Layered Security Architecture)**: 전송 계층 암호화(TLS/Secure Channel), 애플리케이션 레벨의 X.509 인증서 상호 검증, 사용자 레벨의 역할 기반 접근 제어(RBAC)를 단계별로 강제하는 보안 체계.

</details>

- **플랫폼 및 OS 독립성**: 윈도우뿐만 아니라 Linux, Android, VxWorks, 임베디드 마이크로컨트롤러까지 단일 C/C++, Java, .NET 스택으로 구동
- **객체 지향 시맨틱 모델링**: 노드(Node), 객체(Object), 변수(Variable), 메서드(Method)를 유기적으로 모델링하여 기기 자체 설명(Self-Descriptive) 기능 제공
- **다양한 통신 패턴 지원**: 전통적인 RPC 형태의 Request/Response(Client/Server) 모델과 1:N 대규모 브로드캐스팅 및 실시간 TSN 연동을 위한 Pub/Sub(UDP/MQTT) 모델 동시 수용

#### 한줄 요약
- OS 독립성, 시맨틱 주소 공간 모델링, 다계층 보안 및 C/S-Pub/Sub 듀얼 통신 모델을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **컴패니언 명세(Companion Specification)**: 반도체(SEMI), 공작기계(umati), 로봇(VDMA), 플라스틱 사출기(EUROMAP) 등 각 산업별 표준화 기구가 OPC UA 정보 모델을 기반으로 공통 도메인 데이터 구조를 표준화한 확장 규격.
- **GDS(Global Discovery Server)**: 공장 내 수백~수천 대의 OPC UA 서버 및 클라이언트의 X.509 인증서 발급, 갱신, 폐기(CRL) 및 엔드포인트 탐색을 중앙 집중 관리하는 보안 서버.

</details>

```text
[ 상위 IT/클라우드 계층 (MES / ERP / SCADA / Analytics) ]
   │
   ▼ (OPC UA TCP / HTTPS / MQTT over TLS)
[ OPC UA 서버 (OPC UA Server / Edge Gateway) ]
 ├─ [ 주소 공간 (Address Space) ] ── (Root ➔ Objects ➔ Device ➔ Variables / Methods)
 ├─ [ 시맨틱 정보 모델 (Companion Specs: VDMA, EUROMAP, umati) ]
 └─ [ 다계층 보안 스택 (X.509 App Auth + User RBAC + AES-256 Encryption) ]
   │
   ▼ (필드버스 / I/O 인터페이스: Modbus, Profinet, EtherCAT)
[ 하위 현장 설비 계층 (PLC / 로봇 / CNC / 센서 노드) ]
```

선의 의미: 현장 센서 및 PLC 데이터가 OPC UA 서버의 주소 공간에 시맨틱 객체로 모델링되어 상위 IT/MES 시스템으로 안전하게 전달되는 계층 아키텍처

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **주소 공간 (Address Space)** | 모든 설비 파라미터와 메서드를 노드(NodeId, Attributes, References)로 모델링 | 데이터/서비스 저장소 |
| **정보 모델 (Information Model)**| 센서 데이터의 물리적 단위, 정상 동작 범위, 경보(Alarm) 상태 정의 | 시맨틱 메타데이터 |
| **보안 스택 (Security Stack)** | 비대칭 암호(RSA) 기반 채널 수립 및 대칭 암호(AES-128/256) 데이터 전송 | IEC 62541-2 |
| **Pub/Sub 브로커 / TSN** | UDP 멀티캐스트 또는 MQTT/AMQP를 활용한 대규모 저지연 비동기 데이터 배포 | 결정론적 실시간 전송 |
| **GDS (중앙 디스커버리)** | 공장 내 OPC UA 엔드포인트 탐색 및 X.509 인증서 수명주기(발급/갱신) 자동화 | PKI 중앙 관리 |

#### 한줄 요약
- 주소 공간, 정보 모델, 다계층 보안 스택, Pub/Sub 엔진, GDS 인증 서버가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **구독 및 모니터드 아이템(Subscription & MonitoredItem)**: 클라이언트가 주기적으로 폴링하지 않고, 서버 측에서 특정 변수값의 변화(Change of State) 또는 임계치 초과 발생 시에만 비동기로 통지(Notification)하도록 등록하는 이벤트 기반 통신 방식.

</details>

```text
1. 클라이언트가 OPC UA 서버 엔드포인트로 GetEndpoints 요청 ➔ 지원 보안 프로파일(SignAndEncrypt) 획득
            │
            ▼
2. X.509 인증서 교환 및 비대칭 키 검증을 통해 암호화된 안전한 보안 채널(Secure Channel) 생성
            │
            ▼
3. 사용자 자격 증명(ID/PW 또는 X.509)을 검증하여 권한(Role)이 부여된 세션(Session) 활성화
            │
            ▼
4. 클라이언트가 주소 공간을 브라우징(Browse)하여 타겟 설비 노드(NodeId) 식별
            │
            ▼
5. MonitoredItem을 생성하여 값 변경 시에만 비동기 통지(Subscription) 수신 또는 제어 메서드(Call) 실행
```

**동작 원리**

1. **보안 협상**: 클라이언트와 서버가 지원하는 암호화 알고리즘(Basic256Sha256 등) 및 보안 모드 합의
2. **상호 신원 인증**: 양단의 Application Instance Certificate를 상호 대조하여 신뢰 목록(TrustList) 검증
3. **사용자 인가**: 활성화된 채널 상에서 엔지니어, 작업자, 관리자 역할에 따른 세부 접근 권한 부여
4. **시맨틱 탐색**: 계층적 레퍼런스를 따라 주소 공간을 탐색하여 대상 데이터 객체 참조
5. **이벤트 구독**: 서버 측 버퍼 큐를 활용하여 데이터 샘플링 후 변경 분만 발행함으로써 대역폭 보존

#### 한줄 요약
- 보안 협상, Secure Channel 수립, User 세션 활성화, 주소 공간 탐색, MonitoredItem 구독 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Client/Server 모델 vs Pub/Sub 모델**: 일대일 요청-응답 기반의 상태 유지(Stateful) 세션 모델과 일대다 브로드캐스팅 기반의 상태 비저장(Stateless) 고속 모델.

</details>

| 비교 항목 | 클라이언트-서버 모델 (Client/Server) | 발행-구독 모델 (Pub/Sub) |
|:---|:---|:---|
| **통신 패러다임** | **1:1 양방향 요청-응답 (RPC / Session)** | **1:N 또는 M:N 비동기 브로드캐스트 (Stateless)** |
| **전송 프로토콜** | **OPC UA TCP (기본), HTTPS / WebSockets** | **UDP 멀티캐스트, MQTT, AMQP, IEEE 802.1 TSN** |
| **실시간 결정론성** | TCP 오버헤드로 인해 소프트 실시간 적합 | **TSN 결합 시 수 마이크로초 단위 하드 실시간 보장** |
| **네트워크 확장성** | 노드 수 증가 시 서버 연결 세션 부하 증가 | **수천 대의 노드에 동시 데이터 배포 가능 (고확장성)** |
| **주요 적용 분야** | SCADA/MES 구성 설정, 정밀 제어 명령, 파라미터 변경 | **대규모 센서 데이터 수집, 필드버스 대체, 클라우드 연동** |

#### 한줄 요약
- Client/Server는 정밀 구성 및 1:1 제어에 적합하고, Pub/Sub는 대규모 데이터 수집 및 실시간 TSN 연동에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **인증서 만료(Certificate Expiration)**: OPC UA 노드 간 보안 채널 형성에 사용되는 X.509 인증서의 유효기간 만료 시 통신이 전면 차단되어 스마트 팩토리 가동이 중단되는 리스크.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이기종 설비 제조사별 상이한 변수 네이밍으로 인한 상위 MES 데이터 통합 단절 | 산업별 표준 **컴패니언 명세(Companion Specification: umati, VDMA)** 채택 | 데이터 모델 표준화 및 MES/SCADA 상호운용성 100% 확보 |
| X.509 보안 인증서 유효기간 만료로 인한 전체 설비 보안 채널 단절 및 라인 중단 | **GDS(Global Discovery Server) 기반 인증서 자동 갱신(Push/Pull)** 체계 구축 | 인증서 만료 사전 차단 및 365일 무중단 스마트 공장 운영 보증 |
| 대규모 센서 폴링 시 TCP 세션 과부하로 인한 OPC UA 서버 CPU 점유율 100% 폭증 | **값 변경 구독(Subscription)** 전환 및 대규모 수집용 **Pub/Sub 모델** 도입 | 서버 CPU 부하 80% 절감 및 실시간 텔레메트리 전송 효율 극대화 |

#### 한줄 요약
- 컴패니언 명세로 의미를 통일하고, GDS로 인증서 중단을 방지하며, Pub/Sub로 서버 부하를 분산한다.

## Ⅶ. 결론

- 제조 현장의 지능화와 스마트 팩토리 디지털 트윈을 구현하기 위해 **OPC UA 표준 아키텍처**를 산업용 백본 프로토콜로 채택하되, 실무 적용 시 데이터 일관성을 위한 **산업별 컴패니언 명세(Companion Specs)**, 신뢰성 유지를 위한 **GDS 중앙 인증 관리**, 초저지연 필드 제어를 위한 **OPC UA over TSN(Pub/Sub)** 기술을 통합 구현하여 완성도 높은 인더스트리 4.0 통신 인프라를 완성

#### 한줄 요약
- 시맨틱 정보 모델과 GDS 인증 및 Pub/Sub TSN을 결합하여 고신뢰 스마트 팩토리 통신을 실현한다.
