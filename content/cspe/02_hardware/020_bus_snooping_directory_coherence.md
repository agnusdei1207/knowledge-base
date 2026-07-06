---
title: "버스 스누핑·디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 20
---

## 미리 알고가기

- 버스 스누핑(Bus Snooping): 모든 캐시가 공유 버스의 coherence transaction을 감시하는 방식임
- 디렉터리(Directory): 어떤 코어가 특정 cache line 사본을 보유하는지 기록하는 관리 구조임
- 공유자 벡터(Sharer Vector): line을 가진 코어 목록을 비트로 표시한 디렉터리 정보임
- Broadcast/Unicast: 모든 코어에 보내는 방식과 필요한 코어에만 보내는 방식임

## Ⅰ. 개요

- **정의**: 버스 스누핑과 디렉터리 기반 일관성은 멀티코어 캐시 일관성을 유지하기 위해 coherence 요청을 어디로 보내고 누가 사본 보유 정보를 관리할지 정하는 통신 구조임. 코어 수, broadcast 비용, directory 저장 비용, 지연시간을 기준으로 선택함.
- **배경/필요성**: MESI 같은 상태 프로토콜은 캐시 간 메시지가 필요하지만, 메시지 전달 구조가 코어 수에 따라 병목이 될 수 있음. 소규모 시스템은 스누핑이 단순하고, 대규모 many-core는 디렉터리가 불필요한 broadcast를 줄임.
- **비유**: 스누핑은 건물 전체 안내 방송으로 공지하는 방식이고, 디렉터리는 담당자가 관련 사람 명단을 보고 필요한 사람에게만 연락하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 일관성 메시지 전달 구조의 확장성 비교 | snooping, directory, sharer vector, broadcast, invalidation ack | MESI 상태와 전달 구조를 혼동 |

> 요약: 스누핑과 디렉터리는 같은 일관성 목표를 달성하지만 메시지 전파 범위와 관리 주체가 다름.

## Ⅱ. 특징/비교

| 판단 기준 | 버스 스누핑 | 디렉터리 기반 |
|:---|:---|:---|
| 정보 전달 | 모든 캐시가 bus transaction을 관찰함 | directory가 owner와 sharer에게만 메시지를 보냄 |
| 장점 | 구조가 단순하고 작은 코어 수에서 지연이 낮음 | broadcast를 줄여 많은 코어로 확장하기 쉬움 |
| 비용 | 코어 수 증가 시 버스와 snoop traffic이 병목이 됨 | directory 저장 공간, lookup 지연, ack 관리가 필요함 |
| 적용 기준 | 단일 칩 소규모 SMP, 공유 버스 구조 | many-core, NUMA, 칩렛, NoC 기반 시스템 |

> 요약: 코어 수가 적으면 스누핑, 코어 수와 패키지가 커지면 디렉터리 기반이 유리함.

## Ⅲ. 구성요소

```text
Snooping:
+------+   broadcast bus   +------+
|Core0 | <===============> |Core1 |
+------+                   +------+

Directory:
+------+       +-----------+       +------+
|Core0 | <---> | Directory | <---> |Core1 |
+------+       | sharers   |       +------+
               +-----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Snoop controller | 버스 transaction을 감시하고 local cache 상태를 갱신함 | 방송 청취자 |
| Shared bus/NoC | coherence request, invalidate, data response를 전달함 | 공용 도로 |
| Directory entry | tag별 owner, sharer vector, 상태 정보를 저장함 | 대출 장부 |
| Invalidation ack | sharer가 사본 무효화를 완료했음을 알리는 응답임 | 확인 서명 |

> 요약: 스누핑은 관찰자가 많고, 디렉터리는 사본 보유 정보를 기록한 관리자가 중심이 됨.

## Ⅳ. 절차

```text
+----------+     +----------+     +-----------+     +----------+
| Request  | --> | Locate   | --> | Invalidate| --> | Grant    |
+----------+     +----------+     +-----------+     +----------+
 read/write       bus or dir       sharers         data/permission
```

1. **요청 발생** - 코어가 read miss 또는 write permission 요청을 생성함
2. **사본 위치 확인** - 스누핑은 버스 broadcast로, 디렉터리는 sharer vector 조회로 보유 코어를 찾음
3. **무효화·응답** - 쓰기 요청이면 관련 sharer에게 invalidate를 보내고 ack를 수집함
4. **권한 부여** - 요청 코어에 데이터와 읽기·쓰기 권한을 부여하고 상태 정보를 갱신함

> 요약: 일관성 전달 구조는 사본 위치를 찾고 필요한 코어에만 상태 변경을 확정하는 절차임.

## Ⅴ. 문제점 및 개선방안

- **P1 스누핑 확장성 한계**: 소규모 공유 버스 전제의 스누핑을 코어 수가 많은 시스템에 적용하면 모든 캐시가 모든 transaction을 감시해 bus bandwidth와 전력이 급증함
- **P1 대응**: snoop filter, hierarchical snooping, cluster 단위 broadcast로 감시 범위를 줄임 (확인: snoop traffic, bus utilization)
- **P2 디렉터리 저장·지연 비용**: sharer vector와 directory lookup이 메모리 오버헤드와 추가 지연을 만듦
- **P2 대응**: sparse directory, compressed sharer vector, distributed directory로 저장 공간과 지연을 줄임 (확인: directory miss, lookup latency)
- **P3 메시지 순서·교착 위험**: NoC에서 invalidate, ack, data response 순서가 꼬이면 deadlock 또는 livelock이 발생할 수 있음
- **P3 대응**: virtual channel, ordering rule, timeout/retry, formal protocol verification을 적용함 (확인: deadlock proof, protocol coverage)

> 요약: 스누핑은 broadcast 비용, 디렉터리는 메타데이터와 메시지 제어 비용이 핵심 문제이므로 코어 수와 fabric 구조에 맞춰 선택해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 소규모 대칭형 다중처리(Symmetric Multiprocessing, SMP) 시스템온칩(System on Chip, SoC) | 코어 수가 적고 공유 버스 지연이 낮은 구조에는 bus snooping으로 단순한 coherence를 구현함 | snoop traffic, bus utilization, invalidate latency |
| 비균등 메모리 접근(Non-Uniform Memory Access, NUMA) 서버 | socket과 코어 수가 늘어나는 구조에는 directory와 sharer vector로 owner·sharer에게만 메시지를 전송함 | directory lookup latency, remote socket latency, broadcast 감소율 |
| 칩렛·컴퓨트 익스프레스 링크(Compute Express Link, CXL) fabric | 패키지 경계와 장치까지 coherence domain이 확장되는 구간은 hierarchical directory와 snoop filter를 결합함 | protocol coverage, duplicate response, deadlock proof |

> 요약: 스누핑과 디렉터리는 코어 수, 패키지 경계, 메시지 지연을 기준으로 선택하고 protocol 검증으로 확정해야 함.

## Ⅶ. 전망

- **발전 방향**: 칩렛, NUMA, CXL 환경에서는 계층형 directory와 coherence filter가 확대되고 장치까지 포함한 fabric coherence가 설계 대상이 됨
- **기술사적 판단**: snooping은 소규모 공유 버스에 적합하고 directory는 다수 코어·패키지 경계에 적합하므로 코어 수, NoC 대역폭, directory 저장 비용으로 구분함; invalidation broadcast, directory entry overflow, owner migration, duplicate response, remote socket latency를 시나리오별로 확인함
- **기술사 제언**: MESI는 cache line 상태 규칙이고 snooping/directory는 메시지 전달 구조라는 차이를 분명히 해야 함
