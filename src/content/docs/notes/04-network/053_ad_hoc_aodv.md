---
sidebar:
  order: 53
  label: "053. 애드혹 라우팅 AODV (AODV Routing)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "온디맨드 애드혹 라우팅 프로토콜 : AODV (Ad Hoc On-Demand Distance Vector)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 53
extra:
  question_no: "053"
  source_status: "기출"
  source_history: "129회"
  priority: 30
  priority_note: "반응형(Reactive) 라우팅, RREQ/RREP/RERR 메시지, DestSeqNum 루프 방지 및 Expanding Ring Search"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AODV(Ad Hoc On-Demand Distance Vector)**: 모바일 애드혹 네트워크(MANET)에서 사전에 라우팅 테이블을 유지하지 않고, 송신할 데이터가 발생한 시점에만 온디맨드(On-Demand)로 경로를 탐색·수립하는 반응형(Reactive) 거리 벡터 라우팅 프로토콜 (RFC 3561).
- **반응형 라우팅(Reactive / On-Demand Routing)**: 주기적인 전체 토폴로지 광고 패킷 전송을 배제하고, 트래픽 송신 요구가 있을 때만 RREQ 브로드캐스트를 통해 경로를 동적으로 개설하는 라우팅 방식.

</details>

- 정의/개념: 기지국이 없는 이동 무선망에서 데이터 전송 요청 시점에 **RREQ(요청) / RREP(응답)** 제어 메시지를 통해 최신 경로를 수립하고, **목적지 순차 번호(DestSeqNum)** 로 라우팅 루프를 원천 차단하는 **반응형 라우팅 프로토콜(AODV)**
- 배경/필요성: 주기적 라우팅 갱신(Proactive) 방식에서 발생하는 배터리 전력 낭비와 무선 대역폭 고갈(Control Overhead)을 제거하고, 노드 이동성이 높은 MANET 환경에서 에너지 효율성을 극대화할 요구

#### 한줄 요약
- 데이터 전송 요구 시점에만 RREQ/RREP로 경로를 수립하고 DestSeqNum으로 루프를 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **목적지 순차 번호(Destination Sequence Number, DestSeqNum)**: 목적지 노드가 자신의 경로 정보 최신성을 증명하기 위해 단조 증가시키는 일련번호로, 오래된 경로 정보 수용에 따른 카운트 투 인피니티(Count-to-Infinity) 및 라우팅 루프를 차단하는 핵심 척도.
- **역방향/순방향 경로(Reverse / Forward Path)**: RREQ 플러딩 시 송신지 방향의 역방향 포인터를 중간 노드에 기록하고, RREP 유니캐스트 회신 시 목적지 방향의 순방향 엔트리를 라우팅 테이블에 확정하는 2단계 경로 설정 메커니즘.

</details>

- **온디맨드 제어 오버헤드 최소화**: 데이터 송신 전까지 제어 메시지 전송을 억제하여 유휴 상태의 무선 채널 점유율과 배터리 소모 0화
- **DestSeqNum 기반 루프 프리(Loop-Free) 보장**: 더 높은(최신) DestSeqNum을 우선 수용하고, 동일 번호일 경우 더 작은 홉 수(Hop Count)를 선택하여 벨만-포드 루프 원천 차단
- **동적 에러 복구(RERR)**: 노드 이동으로 활성 경로 단절 발생 시 RERR(Route Error) 패킷을 선행 노드(Precursor)로 즉시 전파하여 경로 무효화 및 재탐색 개시

#### 한줄 요약
- 온디맨드 오버헤드 절감, DestSeqNum 기반 루프 차단, RERR 동적 장애 복구를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RREQ (Route Request)**: 송신 노드가 목적지 경로를 탐색하기 위해 브로드캐스트하는 경로 요청 패킷.
- **RREP (Route Reply)**: 목적지 노드 또는 유효한 최신 경로를 보유한 중간 노드가 송신 노드로 역방향 경로를 따라 유니캐스트 회신하는 경로 응답 패킷.
- **RERR (Route Error)**: 링크 단절을 감지한 노드가 해당 경로를 사용 중인 선행 노드들에게 전달하는 에러 통보 패킷.

</details>

```text
[ 송신 노드 (Source) ]
   │
   ▼ (RREQ 플러딩: 브로드캐스트 / 역방향 경로 역포인터 설정)
┌────────────────────────────────────────────────────────────┐
│ 중간 중계 노드 (Intermediate Nodes)                       │
│ ├─ RREQ 수신 시: 송신지 IP, Broadcast ID 중복 검사       │
│ └─ 역방향 라우팅 테이블 엔트리 생성 (타임아웃 타이머 가동) │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼ (RREP 유니캐스트: 순방향 경로 테이블 확정)
[ 목적지 노드 (Destination) ] ── (DestSeqNum 증가 후 RREP 역전송)
```

선의 의미: RREQ는 전체 망으로 브로드캐스트 전파되며 역방향 포인터를 생성하고, RREP는 생성된 역방향 경로를 따라 송신지로 1:1 유니캐스트 회신되는 대칭 경로 생성 구조

| 메시지 유형 | 전송 방식 | 주요 포함 필드 | 역할 및 책임 |
|:---|:---|:---|:---|
| **RREQ (Route Request)** | **브로드캐스트 (Flooding)** | 출발지 IP/SeqNum, 목적지 IP/SeqNum, Hop Count | 경로 탐색 개시 및 중간 노드 역방향 포인터 구축 |
| **RREP (Route Reply)** | **유니캐스트 (Unicast)** | 목적지 IP/DestSeqNum, Hop Count, Lifetime | 최신 경로 확정 및 순방향 포워딩 엔트리 프로그래밍 |
| **RERR (Route Error)** | 유니캐스트/브로드캐스트 | 도달 불가 목적지 IP 리스트 및 DestSeqNum | 링크 단절 통보 및 무효화된 경로 테이블 엔트리 삭제 |
| **Hello 패킷** | 로컬 브로드캐스트 (1-Hop) | 송신 노드 IP, 유효 시간 | 인접 1홉 이웃 노드와의 무선 링크 생존 여부 감시 |

#### 한줄 요약
- RREQ, RREP, RERR, Hello 메시지가 결합하여 온디맨드 경로 탐색 및 복구를 수행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **확장 링 탐색(Expanding Ring Search)**: RREQ 패킷의 IP TTL(Time-To-Live) 값을 1부터 점진적으로 증가시키며 브로드캐스트 범위를 국소 영역에서 전체 망으로 단계적 확장하는 탐색 기법.

</details>

```text
1. 송신 노드 라우팅 테이블에 목적지 경로 부재 시 RREQ 패킷 생성 (TTL=1 시작)
            │
            ▼
2. RREQ 브로드캐스트 수신 노드가 (출발지 IP, Broadcast ID) 중복 검사 및 역방향 넥스트홉 기록
            │
            ▼
3. 목적지 노드(또는 신선한 경로를 가진 중간 노드) 도달 시 DestSeqNum 갱신 후 RREP 생성
            │
            ▼
4. 역방향 경로를 따라 RREP 유니캐스트 전송 ➔ 중간 노드들이 순방향 라우팅 엔트리 확정
            │
            ▼
5. 송신 노드에 RREP 도달 ➔ 양방향 경로 수립 완료 및 유니캐스트 데이터 패킷 송출
```

**동작 원리**

1. **경로 탐색**: 유효 경로가 없을 때 송신 노드가 DestSeqNum을 포함한 RREQ 송출
2. **역방향 포인터 설정**: RREQ를 중계하는 모든 노드가 송신지 방향의 넥스트홉 인터페이스를 메모리에 캐싱
3. **응답 검증**: 목적지 노드가 자신의 시퀀스 번호를 증가시키고 수신된 RREQ의 홉 수를 0으로 초기화하여 RREP 회신
4. **순방향 확정**: RREP를 수신한 중간 노드가 순방향 넥스트홉을 활성화하여 최종 데이터 전송 경로 완성

#### 한줄 요약
- RREQ 브로드캐스트, 역방향 경로 수립, RREP 유니캐스트 회신, 순방향 경로 확정 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **테이블 구동형(Proactive / Table-Driven)**: DSDV, OLSR처럼 상시 모든 노드가 전체 망 라우팅 테이블을 최신 상태로 유지하는 사전 수렴 방식.

</details>

| 비교 항목 | AODV (반응형 / On-Demand) | DSDV / OLSR (선제형 / Table-Driven) |
|:---|:---|:---|
| **경로 탐색 시점** | **데이터 전송 요구 발생 시점에만 동적 탐색** | **주기적으로 전체 네트워크 라우팅 테이블 상시 갱신** |
| **제어 오버헤드** | 유휴 시 제어 패킷 0 (트래픽 발생 시만 RREQ) | 상시 주기적 토폴로지 광고로 무선 채널 점유 |
| **초기 패킷 전송 지연** | **경로 수립(RREQ/RREP)에 따른 초기 지연 존재** | 라우팅 테이블 기확보로 **초기 전송 지연 0ms** |
| **메모리 자원 점유** | 활성 통신 경로만 저장하여 **메모리 절약** | 전체 망 노드 경로를 유지하여 대규모 메모리 요구 |
| **적합 네트워크 환경** | **노드 이동성이 높고 간헐적 통신이 발생하는 망** | 노드 이동성이 낮고 상시 대량 트래픽이 흐르는 망 |

#### 한줄 요약
- AODV는 제어 오버헤드와 메모리를 최소화하고, 선제형 프로토콜은 초기 지연 없이 즉시 패킷을 송출한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **블랙홀 공격(Blackhole Attack)**: 악의적인 노드가 RREQ를 수신하자마자 자신이 목적지 최단 경로인 것처럼 가장 높은 DestSeqNum과 Hop Count 0을 담은 허위 RREP를 즉각 반환하여 모든 트래픽을 가로챈 후 폐기하는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| RREQ 초기 브로드캐스트 플러딩으로 인한 무선 채널 폭풍(Broadcast Storm) | **확장 링 탐색(Expanding Ring Search: TTL 점진적 증가)** 적용 | 인접 노드 탐색 시 불필요한 전역 플러딩 억제 및 대역폭 보존 |
| 허위 높은 DestSeqNum을 응답하여 트래픽을 가로채는 **블랙홀 공격(Blackhole)** | **SAODV(Secure AODV: 디지털 서명 및 해시 체인)** 또는 이중 RREP 검증 | 악의적 허위 RREP 탐지 및 무선 트래픽 탈취 차단 |
| RREQ/RREP 경로 탐색 시간 동안 최초 송신 데이터 패킷 타임아웃 유실 | 송신 노드 내 **송신 버퍼 큐잉(Tx Queueing & Buffering)** 적용 | 경로 수립 완료 시까지 초기 데이터 패킷 유실 방지 |

#### 한줄 요약
- Expanding Ring으로 플러딩을 억제하고, SAODV로 블랙홀 공격을 방어하며, Tx 버퍼링으로 초기 패킷을 보호한다.

## Ⅶ. 결론

- 인프라리스 이동 무선망에서 에너지 및 대역폭 제약을 극복하기 위해 **AODV 반응형 라우팅 프로토콜**을 적용하여 제어 오버헤드를 최소화하고, 무선 취약성을 보완하기 위해 **Expanding Ring Search** 와 **SAODV 디지털 서명 메커니즘**을 결합하여 고효율·고안전성 무선 애드혹 네트워크를 완성

#### 한줄 요약
- 반응형 RREQ/RREP 경로 탐색과 SAODV 보안 검증을 결합하여 고신뢰 MANET 인프라를 실현한다.
