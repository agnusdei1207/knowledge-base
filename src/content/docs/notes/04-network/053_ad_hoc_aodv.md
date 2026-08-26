---
sidebar:
  order: 53
  label: "053. 애드혹 라우팅 AODV"
  badge:
    text: "기출 · 30%"
    variant: note
title: "애드혹 라우팅 프로토콜 : AODV (Ad Hoc On-Demand Distance Vector)"
date: "2026-08-26T13:50:04+09:00"
tags:
  - "notes-network"
weight: 53
extra:
  question_no: "53"
  source_status: "기출"
  source_history: "129회"
  priority: 30
  priority_note: "반응형(Reactive) 라우팅, RREQ/RREP/RERR 메시지, DestSeqNum 루프 방지 및 Expanding Ring Search"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AODV (Ad Hoc On-Demand Distance Vector)**: MANET에서 데이터 전송 요청 시에만 경로를 동적 탐색하는 온디맨드 반응형 거리 벡터 라우팅 프로토콜 (RFC 3561).
- **DestSeqNum (목적지 시퀀스 번호)**: 목적지 노드가 발급하는 단조 증가 번호로 최신 경로 판단 및 Count-to-Infinity 루프를 원천 방지하는 기준값.

</details>

- 정의/개념: 기지국 없는 무선망에서 데이터 송신 시점에 **RREQ/RREP 제어 메시지로 경로를 수립하고 DestSeqNum으로 루프를 차단하는 반응형 라우팅 프로토콜**
- 배경/필요성: 기존 선제형(DSDV) 프로토콜의 상시 라우팅 광고로 인한 **노드 배터리 고갈, 무선 대역폭 낭비 및 빈번한 이동 시 테이블 수렴 지연**

#### 한줄 요약
- 온디맨드 경로 탐색(RREQ/RREP)과 DestSeqNum 루프 방지를 통해 무선 자원과 배터리를 보존한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RERR (Route Error)**: 이동으로 링크가 끊어졌을 때 해당 경로를 사용하는 선행 노드(Precursor)들에게 에러를 통보하여 경로를 무효화하는 제어 패킷.
- **On-Demand Minimal Overhead**: 데이터 전송이 없는 유휴 노드는 라우팅 테이블 갱신 패킷을 전송하지 않아 제어 오버헤드를 극소화하는 특성.

</details>

- **온디맨드(On-Demand) 경로 탐색**: 실제 전송 트래픽 발생 시에만 RREQ를 플러딩하여 대역폭 소모 최소화
- **DestSeqNum 기반 루프 차단**: 목적지 시퀀스 번호의 대소 비교를 통해 **무한 루프(Count-to-Infinity) 원천 제거**
- **동적 장애 복구(RERR)**: 노드 이동으로 링크 단절 발생 시 RERR 패킷을 선행 노드로 즉시 전파하여 경로 재탐색

#### 한줄 요약
- 온디맨드 오버헤드 절감, DestSeqNum 기반 루프 차단, RERR 동적 장애 복구를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RREQ vs RREP**: 송신 노드가 목적지를 찾기 위해 브로드캐스트하는 요청(RREQ)과 목적지가 역방향 경로로 유니캐스트 회신하는 응답(RREP).

</details>

| 메시지 유형 | 전송 방식 | 주요 포함 필드 | 역할 및 책임 |
|:---|:---|:---|:---|
| **RREQ (Route Request)**| **브로드캐스트 (Flooding)** | 출발지 IP/SeqNum, 목적지 IP/SeqNum, Hop Count | **경로 탐색 개시 및 중간 노드 역방향 포인터 구축** |
| **RREP (Route Reply)** | **유니캐스트 (Unicast)** | 목적지 IP/DestSeqNum, Hop Count, Lifetime | **최신 경로 확정 및 순방향 포워딩 엔트리 확정** |
| **RERR (Route Error)** | 유니캐스트/브로드캐스트 | 도달 불가 목적지 IP 리스트 및 DestSeqNum | **링크 단절 통보 및 무효화된 경로 테이블 엔트리 삭제** |
| **Hello 패킷** | 로컬 브로드캐스트 (1-Hop) | 송신 노드 IP, 유효 시간 | **인접 1홉 이웃 노드와의 무선 링크 생존 여부 감시** |

#### 한줄 요약
- RREQ, RREP, RERR, Hello 메시지가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Expanding Ring Search (확장 링 탐색)**: RREQ 패킷의 IP TTL 값을 1부터 점진적으로 증가시켜 전역 브로드캐스트 폭풍(Storm)을 방지하는 기법.

</details>

```text
AODV RREQ/RREP 경로 탐색 및 데이터 전송 파이프라인
        │
   1. [경로 탐색 개시] 송신 노드가 목적지 경로 부재 시 RREQ 패킷 생성 (TTL=1 시작)
        │
   2. [역방향 포인터 수립] 중간 노드가 RREQ 중복 검사 후 송신지 방향 넥스트홉 인터페이스 캐싱
        │
   3. [RREP 유니캐스트 회신] 목적지 노드가 DestSeqNum을 증가시키고 역방향 경로로 RREP 회신
        │
   4. [순방향 경로 확정] 중간 노드들이 RREP를 수신하며 순방향 라우팅 테이블 엔트리 활성화
        │
   ▼
5. [데이터 패킷 전송] 송신 노드가 확정된 순방향 경로를 통해 유니캐스트 데이터 전송
```

#### 한줄 요약
- 경로 탐색 개시 → 역방향 포인터 수립 → RREP 유니캐스트 회신 → 순방향 경로 확정 → 데이터 패킷 전송 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AODV (반응형)** vs **DSDV / OLSR (선제형)**: 필요 시점 동적 탐색(AODV)과 상시 테이블 유지(선제형).

</details>

| 비교 항목 | AODV (반응형 / On-Demand) | DSDV / OLSR (선제형 / Table-Driven) |
|:---|:---|:---|
| **경로 탐색 시점** | **데이터 전송 요구 발생 시점에만 동적 탐색** | **주기적으로 전체 네트워크 라우팅 테이블 상시 갱신** |
| **제어 오버헤드** | 유휴 시 제어 패킷 0 (트래픽 발생 시만 RREQ) | 상시 주기적 토폴로지 광고로 무선 채널 대역폭 점유 |
| **초기 패킷 전송 지연**| **경로 수립(RREQ/RREP)에 따른 초기 지연 존재** | 라우팅 테이블 기확보로 **초기 전송 지연 0ms** |
| **메모리 자원 점유** | 활성 통신 경로만 저장하여 **메모리 절약** | 전체 망 노드 경로를 유지하여 대규모 메모리 요구 |
| **적합 네트워크 환경**| **노드 이동성이 높고 간헐적 통신이 발생하는 망**| 노드 이동성이 낮고 상시 대량 트래픽이 흐르는 망 |

#### 한줄 요약
- AODV는 제어 오버헤드와 메모리를 최소화하고, 선제형 프로토콜은 초기 지연 없이 즉시 패킷을 송출한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Blackhole Attack (블랙홀 공격)**: 악의적인 노드가 허위 최신 DestSeqNum과 Hop 0을 담은 RREP를 즉각 반환하여 트래픽을 가로챈 후 무단 폐기하는 공격.
- **SAODV (Secure AODV)**: 디지털 서명과 해시 체인을 적용하여 RREQ/RREP 메시지의 위변조를 방지하는 보안 확장 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| RREQ 초기 브로드캐스트 플러딩으로 인한 **무선 브로드캐스트 폭풍** | **`확장 링 탐색(Expanding Ring Search: TTL 점진적 증가)`** | 인접 노드 탐색 시 전역 플러딩 억제 및 대역폭 절감 |
| 허위 높은 DestSeqNum을 응답하여 트래픽을 탈취하는 **블랙홀 공격** | **`SAODV (디지털 서명 및 해시 체인)` 또는 이중 RREP 검증** | 악의적 허위 RREP 탐지 및 트래픽 가로채기 차단 |
| RREQ/RREP 경로 탐색 시간 동안 최초 송신 데이터 패킷 타임아웃 유실 | 송신 노드 내 **`송신 버퍼 큐잉(Tx Queueing & Buffering)`** | 경로 수립 완료 시까지 초기 데이터 패킷 유실 방지 |
| 고속 노드 이동으로 인한 빈번한 링크 단절 시 재탐색 오버헤드 폭증 | **`로컬 복구(Local Repair)` 기법을 통한 단절 홉 국소 재탐색** | 송신지 전역 재탐색 방지 및 복구 지연 단축 |

#### 한줄 요약
- Expanding Ring으로 플러딩을 억제하고, SAODV로 블랙홀을 방어하며, 로컬 복구로 재탐색을 최소화한다.

## Ⅶ. 결론

- 간헐 통신은 **AODV**, 상시 트래픽은 **DSDV·OLSR** 선택

#### 한줄 요약
- AODV는 반응형 RREQ/RREP 경로 탐색과 DestSeqNum 루프 방지를 통해 자원을 보존하는 핵심 MANET 라우팅 프로토콜이다.
