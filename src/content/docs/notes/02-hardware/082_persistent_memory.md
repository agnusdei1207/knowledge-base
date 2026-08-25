---
sidebar:
  order: 82
  label: "082. 퍼시스턴트 메모리 (Persistent Memory)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "퍼시스턴트 메모리 (Persistent Memory)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 82
extra:
  question_no: "082"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "바이트 접근•영속 순서•장애 복구"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PMEM(Persistent Memory)**: 메모리 버스에 장착되어 바이트 단위(Byte-Addressable)로 접근하면서 전원 차단 시에도 데이터가 보존되는 비휘발성 메모리.
- **재기동 지연시간(Restart Latency)**: 시스템 재부팅 시 대용량 인메모리 데이터베이스를 SSD에서 DRAM으로 다시 적재하는 데 걸리는 시간.

</details>

- 정의/개념: DRAM급 바이트 주소 접근성과 NAND 플래시의 비휘발성을 결합한 차세대 **퍼시스턴트 메모리(PMEM)**
- 배경/필요성: 서버 재부팅 시 스토리지 재적재에 따른 **수십 분의 재기동 지연(Restart Latency) 및 스토리지 I/O 병목 해결 불가**

#### 한줄 요약
- 나노초 단위 바이트 접근성과 비휘발성을 동시에 제공하여 인메모리 DB의 즉각적 복구를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DAX(Direct Access)**: 커널의 페이지 캐시 및 블록 I/O 계층을 우회하여 유저 공간 애플리케이션이 PMEM 물리 주소를 mmap으로 직접 접근하는 모드.
- **clwb / sfence**: CPU 캐시에 머무는 변경 데이터를 영속성 도메인으로 밀어내고(clwb) 메모리 쓰기 순서를 고정(sfence)하는 명령어.

</details>

- 커널 페이지 캐시 및 블록 드라이버를 우회하는 **DAX(Direct Access)** 초저지연 매핑
- **clwb/sfence** 명령어 기반의 명시적 캐시 플러시와 영속 쓰기 순서(Ordered Persistence) 제어
- 하드웨어 ADR(Asynchronous DRAM Refresh) 회로 연동을 통한 정전 시 쓰기 큐 완벽 보존

#### 한줄 요약
- DAX를 통해 OS 오버헤드 없이 바이트 단위로 직접 접근하며 캐시 플러시 명령어로 영속성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **PMDK(Persistent Memory Development Kit)**: 트랜잭션 원자성과 장애 정합성(Crash Consistency)을 보장하는 오픈소스 C/C++ 라이브러리 슈트.
- **ADR(Asynchronous DRAM Refresh)**: 시스템 정전 시 커패시터 전력으로 CPU 메모리 컨트롤러 쓰기 큐(WPQ) 데이터를 PMEM으로 밀어넣는 하드웨어 회로.

</details>

```text
[퍼시스턴트 메모리(PMEM) 아키텍처]
|-- 사용자 애플리케이션 (PMDK 기반 영속 자료구조)
|-- 파일시스템 계층 (DAX 커널 드라이버 - 페이지 캐시 우회)
|-- CPU 코어 및 휘발성 캐시 계층 (L1/L2/L3 캐시)
|   `-- 캐시 제어 명령어 (clwb -> sfence 영속 순서 보존)
`-- 영속성 도메인 (Persistence Domain)
    |-- 메모리 컨트롤러 쓰기 큐 (WPQ)
    |-- ADR 하드웨어 회로 (정전 시 비상 전원 플러시)
    `-- PMEM 비휘발성 미디어 (CXL.mem / NVDIMM 모듈)
```

선의 의미: 계층 및 데이터 영속화 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| **PMDK 라이브러리** | libpmemobj 등을 통해 트랜잭션 WAL 및 메모리 풀 관리 제공 |
| **DAX 매핑** | 파일시스템 메타데이터 오버헤드 없이 PMEM 가상 주소를 직접 포인터 접근 |
| 캐시 제어 명령어 | `clwb`로 캐시 라인을 WPQ로 방출하고 `sfence`로 직렬화 순서 확정 |
| **ADR 회로** | 정전 감지 시 잔여 전력으로 WPQ 데이터를 PMEM 미디어로 안전하게 자동 플러시 |
| PMEM 미디어 | 3D XPoint, STT-MRAM, ReRAM 등 비휘발성 물리 저장 소자 |

#### 한줄 요약
- PMDK, DAX 드라이버, clwb/sfence 명령어, ADR 영속성 회로가 결합되어 장애 정합성을 보장한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Ordered Persistence**: 로그 기록 → 플러시 → 본 데이터 기록 → 플러시 → 커밋 플래그 설정의 순서를 엄격히 지켜 정합성을 보장하는 패턴.

</details>

```text
PMEM 트랜잭션 쓰기 요청 인입
        │
   복구용 WAL(Write-Ahead Logging) 메타데이터 기록
        │
   clwb로 로그 캐시 라인을 플러시하고 sfence로 영속화 확정
        │
   실제 데이터 페이로드를 메모리에 기록하고 clwb 실행
        │
   커밋 플래그(Commit Flag=1) 기록 및 최종 sfence 인가 (순서 보존)
        │
   트랜잭션 정상 완료 (정전 발생 시에도 재부팅 후 플래그 기반 100% 복구)
```

#### 한줄 요약
- WAL 로깅 → clwb/sfence 플러시 → 본 데이터 기록 → 커밋 플래그 영속 순으로 엄격한 순서 보존 쓰기를 실행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CXL.mem**: CXL 표준 상에서 호스트 프로세서가 PCIe 버스를 통해 풀링된 비휘발성 메모리를 바이트 단위로 접근하는 프로토콜.

</details>

| 메모리 및 스토리지 매체 | 퍼시스턴트 메모리 (PMEM) | DRAM (동적 램) | NVMe All-Flash SSD |
|:---|:---|:---|:---|
| 접근 단위 및 지연시간 | 바이트 단위 (Byte), 수십~수백 $\text{ns}$ | 바이트 단위 (Byte), 수십 $\text{ns}$ | 블록 단위 (4KB), 수십 $\mu\text{s}$ |
| 데이터 영속성 | 비휘발성 (전원 차단 시 영구 보존) | 휘발성 (전원 차단 시 즉시 소멸) | 비휘발성 (NAND 플래시 보존) |
| 주 용도 | 인메모리 DB, 트랜잭션 WAL, 대용량 캐시 | 연산 작업 버퍼, 고성능 프로세스 메모리 | 대규모 영구 데이터 스토리지, 파일 시스템 |
| 한계점 | 캐시 플러시(clwb) 코드 최적화 필수 | 재부팅 시 데이터 재적재 지연 극심 | I/O 레이턴시 및 블록 단위 병목 |

#### 한줄 요약
- DRAM의 속도와 SSD의 영속성을 동시에 제공하며, 인메모리 DB의 재기동 지연을 수 초로 단축한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TOID(Typed OID)**: ASLR 환경에서 재부팅 시 가상 주소가 바뀌어도 유효성을 유지하도록 메모리 풀 ID와 오프셋으로 구성된 상대 포인터.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CPU 캐시에 머무는 미플러시 데이터의 정전 유실 | **clwb/sfence 명시적 플러시** 및 ADR 하드웨어 연동 | 정전 시 쓰기 큐 잔여 데이터 100% 영속화 |
| 시스템 재부팅 시 ASLR로 인한 절대 포인터 무효화 | PMDK 상대 오프셋 포인터(**TOID**) 구조 적용 | 재부팅 후 가상 주소 재매핑 시에도 자료구조 무결성 유지 |
| 크래시 시 부분 쓰기(Torn Write)로 자료구조 손상 | PMDK 트랜잭션(Undo/Redo Log) 라이브러리 준수 | 재기동 시 미완료 트랜잭션 원자적 롤백 보장 |
| 비휘발성 메모리 매체 자체의 쓰기 수명 마모 | 웨어 레벨링(Wear Leveling) 내장 컨트롤러 적용 | 특정 메모리 블록 조기 파손 방지 및 내구성 유지 |

#### 한줄 요약
- clwb/ADR 연동, TOID 상대 포인터, PMDK 트랜잭션 로깅, 웨어 레벨링을 통해 완벽한 신뢰성을 달성한다.

## Ⅶ. 결론

- 초저지연 인메모리 DB 및 금융 원장 시스템은 **CXL.mem 기반 PMEM**을 구축하고, **PMDK 트랜잭션 라이브러리**를 적용하여 나노초 단위 장애 정합성 확립

#### 한줄 요약
- 퍼시스턴트 메모리는 메모리와 스토리지의 경계를 허물어 고성능 시스템의 재기동 지연을 없애는 차세대 메모리 아키텍처다.