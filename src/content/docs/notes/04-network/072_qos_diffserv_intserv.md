---
sidebar:
  order: 72
  label: "072. QoS, DiffServ, IntServ"
  badge:
    text: "미출 · 50%"
    variant: note
title: "IP 네트워크 서비스 품질 보장 : QoS, DiffServ 및 IntServ"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 72
extra:
  question_no: "72"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "DiffServ(DSCP/PHB) vs IntServ(RSVP), 트래픽 조절(Policing/Shaping) 및 큐잉 알고리즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **QoS (Quality of Service)**: 네트워크 자원을 서비스 중요도에 따라 차등 분배하여 대역폭, 지연, 지터, 손실률을 제어하는 기술.
- **Best-Effort (최선형)**: 모든 패킷을 동일하게 선착순(FIFO) 처리하여 혼잡 시 무차별 패킷 손실을 초래하는 기본 IP 전송 방식.

</details>

- 정의/개념: 인입 트래픽을 분류·마킹하고 **차등 큐잉 스케줄링 및 혼잡 회피를 통해 대역폭, 지연, 지터를 제어하는 IP 서비스 품질 보장 기술**
- 배경/필요성: 전통적 최선형(Best-Effort) 전송의 한계로 인한 **망 혼잡 시 무차별 패킷 폐기, 실시간 음성/영상의 지연·지터 폭증 및 SLA 보장 실패**

#### 한줄 요약
- 트래픽 분류, 마킹, 큐잉 스케줄링, 혼잡 회피를 통해 차등화된 서비스 품질을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DSCP (Differentiated Services Code Point)**: IP 헤더 ToS/TC 필드의 상위 6비트를 사용하여 64개 서비스 클래스를 정의하는 필드 (RFC 2474).
- **PHB (Per-Hop Behavior)**: DiffServ 노드가 DSCP 값에 따라 패킷에 적용하는 개별 포워딩 처리 규칙 (EF, AF, BE).

</details>

- **엣지 분류/마킹 및 코어 상태 비저장(Stateless)**: 엣지에서만 5-Tuple로 정밀 분류하고 코어는 **DSCP 태그 기반 고속 PHB 포워딩**
- **유연한 트래픽 컨디셔닝**: 토큰 버킷 알고리즘 기반 **트래픽 셰이핑(지연 버퍼링) 및 폴리싱(초과분 드롭)**
- **정교한 혼잡 회피(WRED)**: 버퍼 만재 시 발생하는 **테일 드롭(Tail Drop) 및 TCP 전역 동기화 방지**

#### 한줄 요약
- 엣지 마킹/코어 무상태 전송, 트래픽 컨디셔닝, WRED 혼잡 회피, 우선순위 큐잉을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EF vs AF vs BE**: 저지연 엄격 우선순위(EF 46), 보증 대역폭 및 드롭 우선순위(AF), 잉여 대역폭 활용(Best Effort).

</details>

```text
[DiffServ 2계층 QoS 처리 아키텍처]
|-- Ingress Edge Router Layer
|   |-- Traffic Classifier (5-Tuple 패킷 분석 -> 트래픽 클래스 식별)
|   |-- Traffic Marker (IP 헤더 DSCP 6비트 기록: EF, AF, BE)
|   `-- Traffic Metering & Policer (계약 초과 패킷 즉시 드롭 또는 버퍼 셰이핑)
`-- Core Router Layer (Stateless PHB 포워딩)
    |-- Strict Priority Queue (EF: 음성 트래픽 최우선 무지연 전송)
    |-- Class-Based Weighted Fair Queue (AF: 업무 데이터 최소 대역폭 보장)
    |-- Best-Effort Queue (BE: 일반 웹 트래픽 잉여 대역폭 전송)
    `-- Congestion Avoidance Engine (WRED: 가중치 기반 선제적 조기 패킷 폐기)
```

선의 의미: 엣지 라우터에서 정밀 분류 및 DSCP 마킹된 트래픽이 코어 라우터로 진입하여 상태 비저장 기반의 고속 PHB 스케줄링을 거치는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **분류기 (Classifier)** | 패킷 헤더(IP, Port, 프로토콜)를 분석하여 **트래픽 클래스를 1:1 식별** | L3~L4 분석 |
| **마커 (Marker)** | 분류된 패킷의 IPv4 ToS / IPv6 TC 필드에 **DSCP(6bit) 값 부여** | RFC 2474 |
| **미터링 / 폴리서** | 토큰 버킷으로 유입 속도를 계측하고 **계약 초과 패킷을 즉시 폐기** | Single/Dual Rate |
| **스케줄러 (Scheduler)** | LLQ, CBWFQ 알고리즘을 통해 **큐 간 대역폭 배분 및 송출 순서 결정** | 큐잉 엔진 |
| **혼잡 회피 (WRED)** | 버퍼 임계치 도달 전 TCP 윈도우 축소를 위해 **확률적 조기 패킷 폐기** | Tail Drop 방지 |

#### 한줄 요약
- 분류기, 마커, 폴리서/셰이퍼, 큐잉 스케줄러, WRED 혼잡 회피 모듈이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LLQ (Low Latency Queuing)**: 엄격한 우선순위 큐(PQ)와 CBWFQ를 결합하여 음성 패킷을 무지연 전송하면서 일반 데이터의 기아를 방지하는 큐잉 기법.

</details>

```text
DiffServ QoS 분류, 마킹 및 PHB 스케줄링 파이프라인
        │
   1. [엣지 트래픽 분류] 인입 패킷의 5-Tuple(IP/Port/프로토콜)을 분석하여 트래픽 유형 판별
        │
   2. [DSCP 헤더 마킹] 패킷 헤더에 DSCP 값 부여 (음성: EF 46, 비디오: AF41, 일반: CS0)
        │
   3. [트래픽 컨디셔닝] 토큰 버킷으로 속도를 검사하여 초과 트래픽은 폴리싱(Drop) 또는 셰이핑(Buffer)
        │
   4. [코어 PHB 큐 매핑] 코어 라우터가 DSCP를 확인하고 지정된 PHB 큐(EF/AF/BE)로 패킷 배정
        │
   ▼
5. [WRED 검증 및 송출] 출력 큐에서 WRED 검증 통과 후 LLQ 우선순위에 따라 라인 레이트 송출
```

#### 한줄 요약
- 엣지 분류/마킹 → 트래픽 컨디셔닝 → 코어 DSCP 기반 PHB 큐잉 → LLQ 전송 및 WRED 혼잡 회피 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IntServ (RSVP 기반 절대 예약)** vs **DiffServ (DSCP 기반 통계적 차등)**.

</details>

| 비교 항목 | 통합 서비스 모델 (IntServ, RFC 1633) | 차등 서비스 모델 (DiffServ, RFC 2475) |
|:---|:---|:---|
| **기본 제어 철학** | **종단 간 연결 지향적 자원 절대 예약** | **비연결 지향적 홉별(PHB) 통계적 차등 대우**|
| **시그널링 프로토콜**| **RSVP (Resource ReSerVation Protocol)** | **별도 시그널링 없음 (IP 헤더 DSCP 직접 활용)**|
| **코어 라우터 상태** | **모든 플로우별 상태(Stateful) 유지 필수** | **상태 유지 없음 (Stateless, 높은 확장성)** |
| **네트워크 확장성** | **매우 낮음 (대규모 백본망 적용 불가)** | **매우 우수 (전 세계 인터넷 백본 표준)** |
| **품질 보장 수준** | 결정론적 100% 절대적 QoS 보장 | 통계적 상대적 클래스 기반 QoS 보장 |
| **주요 활용 분야** | 소규모 전용망, 항공/군용 폐쇄망 | **통신사 백본망, 기업 WAN, 5G 백홀** |

#### 한줄 요약
- IntServ는 상태 유지 기반의 절대적 자원 예약 모델이며, DiffServ는 상태 비저장 기반의 고확장성 통계적 차등 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Starvation (기아 현상)**: 우선순위 큐(PQ)에 패킷이 끊임없이 유입될 때 하위 일반 패킷들이 전송되지 못하고 버려지는 현상.
- **Trust Boundary (신뢰 경계)**: 엔드포인트가 임의로 조작한 DSCP 태그를 엣지 스위치 진입 시 초기화(Reset)하는 보안 경계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 우선순위 큐(PQ) 트래픽 폭증 시 하위 일반 트래픽의 영구 기아 현상 | **`LLQ 내 엄격한 폴리싱 대역폭 상한(Cap)` 설정** | 음성 지연 보장과 동시에 하위 트래픽의 최소 대역폭 방어 |
| 단말이 비인가로 DSCP를 EF(46)로 변조하여 QoS 정책 교란 | 엣지 인입 포트에 **`신뢰 경계(Trust Boundary)` 설정 및 태그 리셋** | 비인가 트래픽의 우선순위 악용 차단 및 정책 일관성 확보 |
| 타 통신사/클라우드 망 연동 경계에서 DSCP 태그 불일치로 QoS 강등 | 이종 사업자 간 **`SLA 기반 DSCP 1:1 상호 매핑(Remarking)` 구축** | 멀티 도메인 전 구간 종단 간(E2E) QoS 연속성 유지 |
| 다중 트래픽 혼잡 시 큐 버퍼 급증으로 인한 버퍼블로트(Bufferbloat) | **`AQM (CoDel / PIE) 적응형 대기열 관리` 알고리즘 활성화** | 불필요한 버퍼 팽창 방지 및 패킷 왕복 지연(RTT) 단축 |

#### 한줄 요약
- LLQ 대역폭 상한으로 기아를 방지하고, Trust Boundary로 변조를 차단하며, DSCP 리마킹으로 도메인 간 QoS를 연계한다.

## Ⅶ. 결론

- 멀티미디어 트래픽과 미션 크리티컬 비즈니스 데이터를 안정적으로 수용하기 위해 **DiffServ 기반 DSCP/PHB 아키텍처를 표준 QoS 모델로 구축**하되, 실무 환경의 자원 고갈 및 정책 왜곡을 방지하기 위해 **LLQ 스케줄링, WRED 혼잡 회피, 신뢰 경계(Trust Boundary) 및 도메인 간 DSCP 매핑 체계**를 통합 적용하여 종단 간 SLA 품질 완성

#### 한줄 요약
- DiffServ는 엣지 마킹과 코어 무상태 PHB 포워딩을 결합하여 인터넷 백본 및 엔터프라이즈 망의 서비스 품질을 보장하는 표준 QoS 모델이다.