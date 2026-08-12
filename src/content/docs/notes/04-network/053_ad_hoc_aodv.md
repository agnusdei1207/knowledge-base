---
sidebar:
  order: 53
  label: "053. FANET 드론 애드혹 네트워크 (FANET Drone Network)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "애드혹 라우팅 AODV (AODV Routing)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 53
extra:
  question_no: "053"
  source_status: "기출"
  source_history: "129회"
  priority: 30
  priority_note: "설명•비교형: 129회 AODV 장문 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **애드혹 주문형 거리 벡터(Ad Hoc On-Demand Distance Vector, AODV)**: 이동 애드혹 네트워크(MANET)에서 데이터 전송 요청이 발생했을 때만 동적으로 경로를 탐색하고 유지하는 반응형(Reactive/On-Demand) 라우팅 프로토콜이다.
- **반응형 라우팅(Reactive / On-Demand Routing)**: 평시 라우팅 테이블 갱신을 정지하고, 데이터를 송신해야 하는 이벤트가 발생했을 때만 플러딩 기반 경로 탐색을 개시하는 라우팅 방식이다.

</details>

- 정의/개념: **AODV(Ad Hoc On-Demand Distance Vector)**는 이동 애드혹 네트워크(MANET)에서 데이터 송신 요청이 발생할 때만 RREQ/RREP 제어 메시지를 통해 동적으로 경로를 형성하고 유지하는 반응형(Reactive) 거리 벡터 라우팅 프로토콜이다.
- 배경/필요성: 선제형(Proactive/Table-driven) 라우팅 방식이 미사용 경로까지 주기적으로 갱신함으로 인해 발생하는 무선 대역폭 소모, 라우팅 제어 오버헤드 및 노드 배터리 낭비 문제를 극복하기 위해 제정되었다.

#### 한줄 요약

- 데이터 송신 필요 시에만 RREQ/RREP 브로드캐스트/유니캐스트 메시지를 통해 최적 동적 경로를 수립하는 반응형 애드혹 라우팅 프로토콜.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **역방향·순방향 경로(Reverse & Forward Path)**: RREQ 수신 시 이전 홉(Hop)을 역방향 경로로 저장하고, RREP 응답 시 역경로를 거슬러 순방향 데이터 라우팅 통로를 완성하는 기법이다.
- **목적지 순차 번호(Destination Sequence Number, DestSeqNum)**: 목적지 노드가 라우팅 정보의 최신성(Freshness)을 나타내기 위해 발급·증가시키는 32비트 정수 값으로, 라우팅 루프(Loop)를 원천 차단한다.
- **경로 요청 및 응답(Route Request / Route Reply, RREQ / RREP)**: 경로를 찾기 위해 브로드캐스팅하는 RREQ와 유연한 순방향 경로를 형성하며 회신되는 유니캐스트 RREP 제어 메시지이다.

</details>

- **온디맨드(On-Demand) 경로 수립**: 데이터 전송 요구가 없는 평시에는 라우팅 제어 패킷을 송신하지 않아 무선 채널 오버헤드를 최소화한다.
- **DestSeqNum 기반 루프 차단 및 최신성 확보**: 모든 라우팅 테이블 엔트리에 DestSeqNum을 부여하여 값이 더 큰(최신의) 경로만 채택함으로써 라우팅 루프 발생을 차단한다.
- **역방향/순방향 포워딩 매핑**: RREQ 전파 시 역방향 경로(Reverse Path)를 노드 테이블에 기재하고, RREP 회신 시 순방향 경로(Forward Path)를 매핑하여 데이터 전달 통로를 완성한다.

#### 한줄 요약

- 온디맨드 경로 탐색, DestSeqNum 기반 루프 차단 및 RREQ/RREP 기반 역방향·순방향 라우팅 형성.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **라우팅 테이블(Routing Table)**: 목적지 IP, 목적지 순차 번호(DestSeqNum), 다음 홉(Next Hop), 홉 카운트(Hop Count) 및 경로 생존 시간(Lifetime)을 보관하는 노드 메모리 구조이다.
- **경로 오류(Route Error, RERR)**: 노드 이동으로 다음 홉 링크가 단절되었을 때 이를 발견한 노드가 송신측으로 경로 파기를 알리는 제어 메시지이다.

</details>

```text
AODV 반응형 라우팅 구조
├─ 메시지 탐색 및 제어 요소 (Routing Control Messages)
│  ├─ 경로 요청 메시지 (RREQ - Broadcast)
│  ├─ 경로 응답 메시지 (RREP - Unicast)
│  └─ 경로 오류 메시지 (RERR - Multicast/Unicast)
└─ 노드 라우팅 테이블 저장 요소 (Routing Table State)
   ├─ 목적지 IP 및 순차 번호 (Dest IP & DestSeqNum)
   ├─ 다음 홉 및 홉 카운트 (Next Hop & Hop Count)
   └─ 경로 생존 시간 및 유효 기간 (Lifetime / Expiration)
```

선의 의미: RREQ/RREP/RERR 제어 메시지가 왕복하면서 노드별 라우팅 테이블의 목적지, 다음 홉, DestSeqNum 및 Lifetime 엔트리를 동적 구성하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 송신 노드 (Source Node) | 라우팅 테이블에 유효 경로가 없을 시 RREQ 메시지를 생성하고 주변 노드로 브로드캐스팅 |
| 중계 노드 (Intermediate Node) | RREQ 수신 시 역방향 경로를 기록하고, 수신된 RREQ의 DestSeqNum보다 높은 유효 경로가 없으면 전달 |
| 목적지 노드 (Destination) | RREQ 수신 시 자사의 DestSeqNum을 1 증가시킨 후 최적 경로를 향해 RREP 메시지를 유니캐스트 회신 |
| 라우팅 테이블 (Routing Table) | Destination IP, DestSeqNum, Valid Sequence Number Flag, Next Hop, Hop Count, Lifetime 관리 |
| RERR 메시지 처리기 | 이동에 의한 링크 단절(Link Break) 감지 시 해당 목적지 정보를 포함한 RERR을 선행 노드들에 분사 파기 |

#### 한줄 요약

- 송신 노드가 RREQ를 확산하고 목적지/중계 노드가 DestSeqNum을 담은 RREP를 유니캐스트로 응답하며 노드별 라우팅 테이블을 업데이트하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **생존 시간(Time to Live, TTL)**: RREQ 패킷이 무한정 플러딩되지 않도록 확산 범위를 제한하는 홉 수 제한 파라미터이다.
- **RREQ 확산 및 RREP 회신**: 송신측의 브로드캐스트 탐색(RREQ)과 수신측/중계측의 유니캐스트 응답(RREP)을 통한 온디맨드 세션 구성 흐름이다.

</details>

```text
1. 송신 노드의 데이터 전송 요구 및 경로 조회 (Packet Send Event)
      │
      ├─ 유효 경로 존재 ── 3. 순방향 라우팅 테이블 기반 데이터 전달 (Data Forwarding)
      │                               │
      │                               ├─ 경로 정상 ── 데이터 전송 완료
      │                               └─ 링크 단절 ── 4. RERR 통보 -> 5. RREQ 재탐색
      │
      └─ 경로 없음 ────── 2a. RREQ 확산 및 역방향 경로 설정 (RREQ Broadcast & Reverse Path)
                                │
                                v
                          2b. RREP 유니캐스트 및 순방향 경로 완성 (RREP Unicast & Forward Path)
```

### 동작 원리

1. **데이터 전송 요구 및 테이블 조회**: 송신 노드가 전송 패킷 수신 시 자신의 라우팅 테이블에 목적지 유효 경로가 있는지 검색한다.
2. **RREQ 확산 및 역방향 경로 기록**: 유효 경로가 없을 경우, RREQ 메시지(DestSeqNum 포함)를 이웃 노드들에 브로드캐스팅하고 이웃 노드들은 역방향 경로를 기록한다.
3. **RREP 응답 및 순방향 경로 형성**: 목적지 노드(또는 최신 DestSeqNum을 가진 중계 노드)가 RREP 메시지를 생성하여 역방향 경로를 따라 유니캐스트 전송하며 순방향 라우팅 경로를 완성한다.
4. **데이터 패킷 포워딩**: 수립된 라우팅 테이블의 Next Hop을 따라 사용자 데이터 패킷을 고속 전달한다.
5. **링크 단절 및 RERR 재탐색**: 노드 이동으로 전송 중 링크가 차단되면, 감지 노드가 RERR 메시지를 상류로 전달하여 해당 경로를 파기하고 송신 노드가 RREQ 재탐색을 수행한다.

#### 한줄 요약

- RREQ 확산 및 역방향 경로 설치, RREP 응답 및 순방향 경로 확립, 데이터 전달 및 링크 단절 시 RERR 통보와 RREQ 재탐색 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **선제형 라우팅(Proactive / Table-Driven Routing)**: 데이터 송신 여부와 상관없이 모든 노드가 전체 망의 라우팅 정보를 주기적으로 갱신·유지하는 방식이다.

</details>

| 비교 항목 | **AODV (반응형 / On-Demand)** | **DSDV / OLSR (선제형 / Table-Driven)** |
|:---|:---|:---|
| 경로 탐색 시점 | 트래픽 발생 시 요청 탐색 (On-Demand) | 평시 주기적 전체 경로 테이블 갱신 (Proactive) |
| 제어 트래픽 오버헤드 | 매우 적음 (유휴 시 제어 메시지 제로) | 매우 큼 (미사용 경로도 계속 주기적 갱신) |
| 전송 시작 지연시간 | 첫 패킷 전송 시 RREQ/RREP 지연 발생 | 초기 지연 없음 (이미 구축된 라우팅 테이블 사용) |
| 라우팅 테이블 크기 | 활성화된 목적지 경로만 최소 기재 보관 | 네트워크 내 전체 노드 수만큼 대용량 보관 |
| 적합 네트워크 환경 | 노드 이동성이 높고 통신이 간헐적인 환경 | 노드 수가 적고 이동성이 낮으며 상시 통신 환경 |

> 요약: AODV 반응형은 제어 오버헤드를 대폭 줄이나 초기 전송 지연이 발생하고, 선제형은 초기 지연이 없으나 제어 오버헤드가 큼.

#### 한줄 요약

- AODV 반응형은 제어 오버헤드를 대폭 줄이나 초기 전송 지연이 발생하고, 선제형은 초기 지연이 없으나 제어 오버헤드가 큼.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **확장 링 탐색(Expanding Ring Search)**: RREQ의 TTL을 1, 2, 4, 8로 단계적으로 크게 늘려 가까운 노드부터 탐색함으로써 전역 브로드캐스트 폭주(Broadcast Storm)를 예방하는 기법이다.
- **블랙홀 공격(Blackhole Attack)**: 악의적인 노드가 자신이 목적지까지의 가장 최신(최고 DestSeqNum) 및 최단 경로를 가졌다고 거짓 RREP를 응답하여 패킷을 가로채고 폐기하는 보안 위협이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| RREQ 브로드캐스트 스톰 | 목적지가 멀리 있을 때 RREQ 전역 플러딩 발생 | Expanding Ring Search (TTL 단계 증가 탐색) 적용 | 불필요한 라우팅 제어 패킷 폭주 80% 저감 |
| 블랙홀(Blackhole) 보안 위협 | 악의적 노드가 비정상적으로 높은 DestSeqNum RREP 발송 | SAODV(Digital Signature) 및 RREP DestSeqNum 상한 검증 | 거짓 RREP 가로채기 공격 차단 및 라우팅 무결성 확보 |
| 초기 패킷 전송 지연 | 첫 번째 데이터 전송 시 RREQ/RREP 왕복 지연 발생 | 송신 버퍼(Tx Buffer) 큐잉 및 유효 경로 사전 예비 유지 | 패킷 유실 방지 및 세션 연결성 향상 |
| 잦은 경로 재탐색 폭주 | 노드 이동 속도가 너무 빨라 경로 유효 수명(Lifetime) 초과 | 이동 속도 기반 가변 Lifetime 설정 및 Local Repair 기법 | 중계 노드 단 수준에서의 즉각적인 국소 경로 복구 |

#### 한줄 요약

- Expanding Ring Search(TTL 단계 확대), DestSeqNum 검증을 통한 Blackhole 공격 차단, Route Lifetime 최적화로 AODV 안정성 확보.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **유휴 제어량(Control Traffic Overhead)**: 데이터를 송신하지 않는 평시 상태에서 네트워크가 라우팅 유지보수를 위해 소비하는 대역폭 비율이다.

</details>

- 이동 애드혹 및 드론/센서망 설계 시 **AODV 반응형 라우팅 채택**, **Expanding Ring Search 적용**, **보안형 SAODV/DestSeqNum 검증 구현 필수**.

#### 한줄 요약

- 반응형 AODV 라우팅 프로토콜 적용 및 Expanding Ring Search 기반 브로드캐스트 폭주 차단 구현 필수.
