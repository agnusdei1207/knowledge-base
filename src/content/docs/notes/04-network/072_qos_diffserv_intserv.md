---
sidebar:
  order: 72
  label: "072. QoS, DiffServ, IntServ"
  badge:
    text: "미출 · 50%"
    variant: note
title: "IP 네트워크 서비스 품질 보장 : QoS, DiffServ 및 IntServ"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 72
extra:
  question_no: "072"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "DiffServ(DSCP/PHB) vs IntServ(RSVP), 트래픽 조절(Policing/Shaping) 및 큐잉 알고리즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **서비스 품질(Quality of Service, QoS)**: 한정된 네트워크 대역폭 자원 내에서 트래픽의 중요도와 서비스 특성에 따라 전송 우선순위를 차등 부여함으로써 대역폭 보장, 전송 지연(Delay), 지터(Jitter), 패킷 손실률(Packet Loss)을 통제하는 트래픽 엔지니어링 기술.
- **최선형(Best-Effort) 서비스**: 모든 패킷을 동일한 우선순위로 선착순(FIFO) 처리하는 전통적 IP 네트워크의 기본 전송 방식으로, 혼잡 발생 시 무차별 패킷 손실 유발.

</details>

- 정의/개념: 실시간 음성(VoIP), 비디오 스트리밍, 미션 크리티컬 데이터의 통신 품질을 보장하기 위해 인입 트래픽을 분류·마킹하고 **큐잉 스케줄링(Queuing)** 과 **혼잡 회피(Congestion Avoidance)** 기법을 적용하는 **IP QoS 아키텍처**
- 배경/필요성: 단일 IP 네트워크 망에서 대용량 데이터 전송과 실시간 멀티미디어 서비스가 공존함에 따라 발생하는 대역폭 고갈 및 패킷 지연을 해결하고, SLA 기반의 서비스 차별화를 달성할 요구

#### 한줄 요약
- 트래픽을 분류 및 마킹하여 자원을 차등 배분함으로써 실시간 패킷의 지연과 손실을 보증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **홉별 동작(Per-Hop Behavior, PHB)**: DiffServ 노드가 패킷 헤더의 DSCP 값을 기반으로 개별 패킷에 대해 수행하는 큐잉 및 폐기 제어 동작 (EF: 가속 포워딩, AF: 확정 포워딩, BE: 최선형).
- **트래픽 폴리싱(Policing)과 셰이핑(Shaping)**: 계약 대역폭 초과 트래픽 발생 시 즉각 패킷을 드롭/재마킹하는 방식(Policing)과 버퍼 큐에 일시 저장하여 지연 송출함으로써 트래픽을 평활화하는 방식(Shaping).

</details>

- **차등적 자원 스케줄링**: 중요 트래픽(EF)에 대해 우선순위 큐(PQ)를 배정하여 0ms에 근접한 초저지연 보장
- **단계별 트래픽 컨디셔닝**: 엣지 라우터에서 패킷을 분류(Classification) 및 마킹(Marking)하고 초과 트래픽은 토큰 버킷(Token Bucket) 기반으로 폴리싱/셰이핑 집행
- **확장성 기반의 계층적 분리**: 코어 라우터는 개별 플로우 상태를 유지하지 않고 DSCP 기반의 집약된 집합체(Aggregate) 처리만 수행하여 대규모 백본망 수용

#### 한줄 요약
- 트래픽 분류/마킹, 홉별 동작(PHB), 토큰 버킷 기반 폴리싱 및 셰이핑을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **차등 서비스 코드 포인트(Differentiated Services Code Point, DSCP)**: IPv4 ToS(Type of Service) 필드 또는 IPv6 Traffic Class 필드의 상위 6비트를 사용하여 총 64개의 트래픽 서비스 클래스를 정의하는 필드 (RFC 2474).
- **자원 예약 프로토콜(Resource ReSerVation Protocol, RSVP)**: IntServ 모델에서 수신자가 송신자까지의 전송 경로상에 위치한 모든 라우터에 대역폭 예약을 요청하는 시그널링 프로토콜 (RFC 2205).

</details>

```text
[ 엣지 라우터 (Ingress Edge Router) ]
 ├─ [ 트래픽 분류 (Classification) ] ── (L3 IP / L4 Port 기반 플로우 식별)
 ├─ [ 트래픽 마킹 (Marking) ] ──────── (IP 헤더 내 DSCP 6비트 기록: EF, AF, BE)
 └─ [ 트래픽 조절 (Metering/Policing) ] ─ (계약 대역폭 초과 트래픽 드롭 또는 지연)
                                              │
                                              ▼ (DSCP 기반 집약 패킷 전달)
[ 코어 라우터 (Core Router: PHB 집행) ]
 ├─ [ EF 큐 (Strict Priority) ] ────▶ (음성 트래픽: 즉시 최우선 포워딩)
 ├─ [ AF 큐 (CBWFQ / WRED) ] ───────▶ (업무 데이터: 최소 대역폭 보장 및 혼잡 시 조기 폐기)
 └─ [ BE 큐 (FIFO) ] ───────────────▶ (일반 웹 서핑: 잉여 대역폭 활용)
```

선의 의미: 엣지 라우터에서 정밀 분류 및 DSCP 마킹된 트래픽이 코어 라우터로 진입하여 상태 비저장(Stateless) 기반의 고속 PHB 큐잉 스케줄링을 거치는 2계층 아키텍처

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **분류기 (Classifier)** | 패킷 헤더(IP, Port, 프로토콜)를 분석하여 트래픽 클래스 1:1 식별 | L3~L4 분석 |
| **마커 (Marker)** | 분류된 패킷의 IPv4 ToS / IPv6 TC 필드에 DSCP(6bit) 또는 CoS(3bit) 값 부여 | RFC 2474 |
| **미터링 / 폴리서 (Policer)** | 토큰 버킷(Token Bucket)으로 유입 속도를 측정하고 계약 초과 패킷 즉시 폐기 | Single/Dual Rate |
| **스케줄러 (Scheduler)** | LLQ, CBWFQ, WRR 알고리즘을 통해 큐 간 대역폭 배분 및 패킷 송출 순서 결정 | 큐잉 엔진 |
| **혼잡 회피 (WRED)** | 버퍼 임계치 도달 전 TCP 윈도우 축소를 유도하기 위해 확률적 조기 패킷 폐기 | Tail Drop 방지 |

#### 한줄 요약
- 분류기, 마커, 폴리서/셰이퍼, 큐잉 스케줄러, WRED 혼잡 회피 모듈이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **가중 무작위 조기 검출(Weighted Random Early Detection, WRED)**: 큐 버퍼가 100% 가득 차서 모든 패킷이 일괄 버려지는 테일 드롭(Tail Drop) 현상과 TCP 전역 동기화(Global Synchronization)를 방지하기 위해 버퍼 사용률에 따라 패킷을 선제적으로 확률 폐기하는 기법.

</details>

```text
1. 패킷이 엣지 라우터로 인입 ➔ 5-Tuple(Src/Dst IP, Src/Dst Port, Protocol) 기반 분류
            │
            ▼
2. 패킷 헤더에 DSCP 값 마킹 (음성: EF 46, 비디오: AF41, 업무: AF21, 일반: CS0)
            │
            ▼
3. 토큰 버킷(Token Bucket) 기반 속도 검사 ➔ 초과 트래픽은 폴리싱(Drop) 또는 셰이핑(Buffer)
            │
            ▼
4. 코어 라우터가 DSCP를 확인하고 지정된 PHB 큐(Strict Priority or CBWFQ)로 패킷 라우팅
            │
            ▼
5. 출력 큐에서 WRED 혼잡 회피 알고리즘 검증 통과 후 우선순위에 따라 라인 레이트 송출
```

**동작 원리**

1. **엣지 분류 및 마킹**: 트래픽 진입점에서 심층 패킷 분석을 통해 DSCP 태그 주입
2. **트래픽 컨디셔닝**: CIR(약정 정보 속도) 및 PIR(초과 정보 속도) 기준으로 대역폭 제한
3. **코어 상태 비저장 전송**: 코어 라우터는 플로우 상태 저장 없이 오직 DSCP 헤더만을 보고 PHB 큐 매핑
4. **우선순위 큐잉(LLQ)**: 저지연 큐(Low Latency Queue)를 통해 지연에 민감한 패킷을 최우선 출력
5. **혼잡 선제 회피**: WRED가 DSCP 우선순위가 낮은 패킷부터 선제적으로 드롭하여 TCP 슬로우 스타트 유도

#### 한줄 요약
- 엣지 분류/마킹, 트래픽 컨디셔닝, 코어 DSCP 기반 PHB 큐잉, LLQ 전송 및 WRED 혼잡 회피 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IntServ(통합 서비스) vs DiffServ(차등 서비스)**: 플로우 단위로 종단 간 사전 자원을 물리적으로 예약하는 방식과, 패킷 단위로 DSCP 마킹을 부여하여 통계적으로 차등 처리하는 방식.

</details>

| 비교 항목 | 통합 서비스 모델 (IntServ, RFC 1633) | 차등 서비스 모델 (DiffServ, RFC 2475) |
|:---|:---|:---|
| **기본 제어 철학** | **종단 간 연결 지향적 자원 절대 예약** | **비연결 지향적 홉별(PHB) 통계적 차등 대우** |
| **시그널링 프로토콜** | **RSVP (Resource ReSerVation Protocol)** | **별도 시그널링 없음 (IP 헤더 DSCP 직접 활용)** |
| **코어 라우터 상태 저장**| **모든 플로우별 상태(Stateful) 유지 필수** | **상태 유지 없음 (Stateless, 높은 확장성)** |
| **네트워크 확장성** | **매우 낮음 (대규모 백본망 적용 불가능)** | **매우 우수 (전 세계 인터넷 백본 표준)** |
| **품질 보장 수준** | 결정론적 100% 절대적 QoS 보장 | 통계적 상대적 클래스 기반 QoS 보장 |
| **주요 활용 분야** | 소규모 전용망, 항공/군용 폐쇄망 | **ISP 통신사 백본망, 기업 WAN, 5G 백홀** |

#### 한줄 요약
- IntServ는 상태 유지 기반의 절대적 자원 예약 모델이며, DiffServ는 상태 비저장 기반의 고확장성 통계적 차등 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **기아 현상(Starvation)**: 엄격한 우선순위 큐(Strict Priority Queue)에 상시 트래픽이 유입될 경우 하위 우선순위의 일반 패킷들이 스케줄링 기회를 얻지 못하고 영구 지연/폐기되는 현상.
- **DSCP 리마킹(Remarking) 및 신뢰 경계(Trust Boundary)**: 신뢰할 수 없는 엔드포인트(PC/서버)가 임의로 조작한 DSCP 태그를 엣지 스위치 진입 시 초기화(Reset)하거나 도메인 간 QoS 매핑 테이블로 재정의하는 보안 조치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 상위 우선순위 큐(PQ) 트래픽 폭증 시 하위 일반 트래픽의 영구 기아 현상(Starvation) | **LLQ(Low Latency Queuing) 내 엄격한 폴리싱 대역폭 상한(Cap)** 설정 | 음성 지연 보장과 동시에 하위 데이터 트래픽의 최소 대역폭 방어 |
| 엔드포인트 단말이 비인가로 DSCP를 EF(46)로 변조하여 QoS 정책 교란 | 엣지 인입 포트에 **신뢰 경계(Trust Boundary)** 설정 및 비인가 태그 리셋 | 비인가 트래픽의 우선순위 악용 원천 차단 및 정책 일관성 확보 |
| 타 통신사/클라우드 망 연동 경계에서 DSCP 태그 정책 불일치로 인한 QoS 강등 | 이종 사업자 간 **SLA 기반 DSCP 1:1 상호 매핑 테이블(Remarking)** 구축 | 멀티 도메인 전 구간 종단 간(E2E) 일관된 QoS 품질 연속성 유지 |

#### 한줄 요약
- LLQ 대역폭 상한으로 기아를 방지하고, Trust Boundary로 변조를 차단하며, DSCP 리마킹으로 도메인 간 QoS를 연계한다.

## Ⅶ. 결론

- 멀티미디어 트래픽과 미션 크리티컬 비즈니스 데이터를 안정적으로 수용하기 위해 **DiffServ 기반 DSCP/PHB 아키텍처**를 표준 QoS 모델로 구축하되, 실무 환경의 자원 고갈 및 정책 왜곡을 방지하기 위해 **LLQ 스케줄링**, **WRED 혼잡 회피**, **신뢰 경계(Trust Boundary)** 및 **도메인 간 DSCP 매핑 체계**를 통합 적용하여 종단 간 SLA 품질을 완성

#### 한줄 요약
- DiffServ DSCP/PHB와 LLQ/WRED 기술을 결합하여 고신뢰 IP 네트워크 QoS를 구현한다.
