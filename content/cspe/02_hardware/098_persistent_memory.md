---
title: "퍼시스턴트 메모리 (Persistent Memory)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 98
---

## 미리 알고가기

- Persistent Memory(PM): 바이트 주소 지정과 전원 차단 후 데이터 보존을 함께 제공하는 메모리 계층임
- DAX(Direct Access): 파일시스템 page cache를 우회해 애플리케이션이 영속 메모리에 직접 접근하는 방식임
- Flush/Fence: CPU(Central Processing Unit) cache 데이터를 영속 영역까지 밀어내고 순서를 보장하는 명령·메커니즘임
- Crash Consistency: 장애 후 데이터 구조가 일관된 상태로 복구되는 성질임
- PMDK(Persistent Memory Development Kit): 영속 메모리 자료구조와 트랜잭션 구현을 돕는 라이브러리 집합임

## Ⅰ. 개요

- **정의**: 퍼시스턴트 메모리는 CPU가 byte-addressable 방식으로 접근하면서 전원 장애 후에도 데이터가 유지되는 메모리 계층임. 저장장치 I/O(Input/Output) 지연을 줄이고 인메모리 데이터의 복구 시간을 단축하기 위해 사용함.
- **배경/필요성**: DRAM(Dynamic Random-Access Memory) 기반 인메모리 시스템은 빠르지만 장애 후 재적재 시간이 길고, SSD(Solid-State Drive) 기반 저장은 영속적이지만 syscall과 블록 I/O 오버헤드가 큼. 퍼시스턴트 메모리는 로드/스토어 접근과 영속성을 결합해 두 계층 사이의 간격을 줄임.
- **비유**: 책상 위에서 바로 쓰는 노트가 정전 후에도 그대로 남아 다음 날 이어서 작업할 수 있는 상태와 같음.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리-스토리지 융합 계층 판단 | byte-addressable, persistence, cache flush, crash consistency | 빠른 SSD로만 설명 |

> 요약: 퍼시스턴트 메모리는 메모리 접근 모델과 저장 지속성을 결합한 새로운 계층임.

## Ⅱ. 특징/비교

| 판단 기준 | DRAM | SSD | Persistent Memory |
|:---|:---|:---|:---|
| 주소 지정 | 바이트 단위 | 블록 단위 | 바이트 단위 |
| 지속성 | 전원 차단 시 소실 | 유지 | 유지 |
| 접근 경로 | load/store | syscall, block I/O | load/store 또는 DAX |
| 설계 부담 | 데이터 재적재 필요 | I/O 최적화 필요 | cache flush와 원자성 설계 필요 |

> 요약: 퍼시스턴트 메모리는 빠른 접근을 제공하지만 애플리케이션이 영속성 순서를 직접 고려해야 함.

- **적용 조건**: 데이터 구조가 장애 후 일관성을 검증할 수 있게 설계되어야 함
- **선택 지표**: persist latency, recovery time, write amplification을 함께 봐야 함
- **운영 관점**: 영속 메모리 영역은 메모리이면서 저장 데이터 생명주기 정책을 따라야 함

## Ⅲ. 구성요소

```text
+-------------+      +-------------+      +--------------+
| Application | ---> | PM library  | ---> | PM namespace |
+-------------+      +-------------+      +--------------+
        |                    |                     |
        v                    v                     v
+-------------+      +-------------+      +--------------+
| CPU cache   |      | Flush/fence |      | PM media     |
+-------------+      +-------------+      +--------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 애플리케이션 | 영속 자료구조를 생성하고 load/store로 데이터를 접근함 | 노트를 쓰는 사람 |
| PM 라이브러리 | transaction, allocator, logging으로 일관성을 보조함 | 작성 규칙 안내서 |
| CPU cache 제어 | flush와 fence로 쓰기 순서와 영속 시점을 제어함 | 잉크를 말리는 절차 |
| PM 매체·namespace | OS(Operating System)가 노출한 영속 메모리 영역과 물리 매체임 | 지워지지 않는 종이 |

> 요약: 퍼시스턴트 메모리는 애플리케이션, 라이브러리, cache 제어, 영속 매체가 함께 동작해야 함.

## Ⅳ. 절차

```text
+----------+      +----------+      +----------+      +----------+
| Allocate | ---> | Write    | ---> | Persist  | ---> | Recover  |
+----------+      +----------+      +----------+      +----------+
```

1. **영역 할당** — OS가 PM namespace를 만들고 DAX 파일시스템 또는 device로 애플리케이션에 제공함
2. **데이터 쓰기** — 애플리케이션이 영속 자료구조를 load/store 명령으로 갱신함
3. **영속 보장** — cache line flush와 fence로 기록 순서와 완료 시점을 보장함
4. **장애 복구** — 재시작 시 로그, version, checksum으로 일관된 상태를 찾아 복구함

> 요약: 퍼시스턴트 메모리 사용은 할당보다 쓰기 순서와 장애 후 일관성 검증이 핵심임.

## Ⅴ. 문제점 및 개선방안

- **P1 프로그래밍 복잡도**: 개발자가 cache flush, ordering, 원자성 문제를 잘못 처리하면 장애 후 데이터가 깨질 수 있음
- **P1 대응**: PMDK 같은 라이브러리, transaction 패턴, crash test를 표준화함 (확인: recovery consistency pass rate)
- **P2 성능 예측 어려움**: load/store 경로는 빠르지만 flush, write amplification, NUMA(Non-Uniform Memory Access) 배치에 따라 지연이 변동됨
- **P2 대응**: NUMA-aware allocation, flush batching, profiling으로 지연 변동 원인을 분리함 (확인: p99 persist latency)
- **P3 보안·잔존 데이터**: 전원 차단 후에도 데이터가 남아 있어 폐기, 재할당, 권한 오류 시 정보 노출 위험이 있음
- **P3 대응**: namespace 암호화, secure erase, 재할당 시 zeroing 정책을 적용함 (확인: residual data scan)

> 요약: 퍼시스턴트 메모리 개선은 프로그래밍 모델, 성능 계측, 데이터 생명주기 보안을 함께 다뤄야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 인메모리 DB 복구 | 데이터 구조를 persistent memory에 배치하고 transaction, flush, checksum으로 재시작 복구를 단축함 | recovery time, consistency pass rate |
| 파일시스템·저널 최적화 | journal, metadata, checkpoint를 영속 메모리에 배치해 동기 쓰기 지연을 줄임 | p99 persist latency, write amplification |
| 장비 폐기·재할당 | namespace 암호화, secure erase, zeroing 정책을 운영 절차에 포함해 잔존 데이터를 제거함 | residual data scan, erase verification |

> 요약: 실무에서는 퍼시스턴트 메모리를 성능 장치가 아니라 장애 일관성과 데이터 생명주기 보안을 함께 요구하는 저장 계층으로 다뤄야 함.

## Ⅶ. 전망

- **발전 방향**: CXL.mem(Compute Express Link memory) 기반 메모리 확장, 원격 영속 메모리, 데이터베이스 in-place recovery 기술과 결합할 가능성이 큼
- **기술사적 판단**: 도입은 단순 성능보다 복구 시간 단축, 애플리케이션 수정 비용, 보안 요구를 기준으로 해야 함
- **기술사 제언**: 핵심 업무에는 crash consistency 테스트를 배포 기준에 포함하고, PM 영역의 암호화·폐기 절차를 운영 표준으로 둬야 함
