---
sidebar:
  order: 82
  label: "082. 퍼시스턴트 메모리 (Persistent Memory)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "퍼시스턴트 메모리 (Persistent Memory)"
date: "2026-08-13T12:21:04+09:00"
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

- **PMEM(Persistent Memory)**: 바이트 주소 지정과 전원 차단 후 데이터 유지 특성을 결합한 영속 메모리.
- **바이트 주소 지정(Byte-Addressability)**: 블록 I/O 대신 CPU가 로드·스토어 명령으로 주소에 접근하는 성질.
- **재시작 지연(Restart Latency)**: 장애 발생 후 메모리 상태 및 DB 포인터 레코드를 비휘발 영역에서 즉시 로딩하여 서비스 재개에 걸리는 복구 시간.

- **영속성 메모리(Persistent Memory, PMEM)**: DRAM 수준의 나노초급 바이트 단위 직접 접근 속도와 비휘발성(Non-volatility) 데이터 영속성을 동시에 제공하는 스토리지-클래스 메모리.
</details>

- 정의/개념: 바이트 주소 **직접 접근**과 전원 차단 시 **비휘발성**을 결합한 메모리
- 배경/필요성: **블록 I/O** 병목과 메모리 휘발성으로 시스템 **재시작 지연** 단축 불가

#### 한줄 요약

- 퍼시스턴트 메모리는 바이트 주소 지정과 비휘발성을 결합하여 재시작 지연을 줄인다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DAX(Direct Access)**: 파일 매핑 후 페이지 캐시와 전통적 블록 I/O 경로 없이 영속 메모리에 접근하는 방식.
- **캐시 라인 플러시(clflush/clwb)**: CPU 캐시 메모리 상의 갱신 데이터를 차세대 비휘발 PMEM 영역으로 강제 덤프 유도하는 CPU 명령어.
- **sfence(Store Fence)**: 메모리 쓰기(Write) 명령 간의 순서를 보장하여 영속성 파이프라인의 순서 정합성을 보증하는 바리어 명령어.
- **장애 정합성(Crash Consistency)**: 전원 불시 차단(Power Outage) 시에도 영속 자료구조 및 DB 상태가 무결하게 복구되는 안전 속성.

</details>

- OS 페이지 캐시를 우회하는 초저지연 **DAX** 구동
- **clwb** 및 **sfence** 명령으로 영속 쓰기 순서 통제
- 영속 상태 재사용으로 **재시작 지연**을 줄이고 **장애 정합성** 설계

#### 한줄 요약

- 캐시 라인 플러시와 메모리 펜스 및 커밋 순서로 장애 정합성을 보장하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ADR(Asynchronous DRAM Refresh)**: 전원 장애 순간 CPU 캐시 외 버퍼 메모리의 전력을 유지하여 PMEM으로 덤프 완료시키는 하드웨어 전원 보호 회로.
- **PMDK(Persistent Memory Development Kit)**: PMEM 전용 영속 힙(Heap), 트랜잭션, 락(Lock)을 C/C++ 표준 제어하는 오픈소스 라이브러리 스택.

</details>

```text
[영속 자료구조] -- [DAX 매핑] -- [캐시•영속 제어] -- [영속성 영역]
```

선의 의미: 사용자 공간의 영속 자료구조가 DAX 매핑 및 캐시·영속 제어를 거쳐 HW ADR 영역과 PMEM으로 영속 연동되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 영속 자료구조 | PMDK 기반 B-Tree, WAL 영속 자료구조 구성 |
| DAX 매핑 | 커널 파일시스템 I/O 우회 및 사용자 주소 공간 물리 1:1 직결 |
| 캐시•영속 제어 | **clwb**, **sfence** 명령어를 통한 캐시 덤프 및 영속 순서 강제 |
| 영속성 영역 | **PMEM** 매체와 전원 장애 시 쓰기 보호용 **ADR** 영역 |

#### 한줄 요약

- DAX 매핑과 캐시•영속 제어로 영속 자료구조와 영속성 영역을 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **순서 보존 쓰기(Ordered Persistence)**: Log -> Data -> Commit Record 순서대로 clwb/sfence를 인가하여 전원 사고 시 데이터 오염을 차단하는 기법.

</details>

```text
[트랜잭션 갱신 요청]
          │
          ▼
1. 복구 로그 기록
          │
          ▼
2. 로그 플러시•펜스
          │
          ▼
3. 본 데이터 기록•플러시
          │
          ▼
4. 커밋 표식 영속
          │
    ┌─────┴──────────┐
    │ 정상 완료      │ 전원 장애
    ▼                ▼
[I/O 완료 반환]  5. 복구 상태 판정
                      ┌──┴──────────┐
                      │ 커밋 완료   │ 미완료
                      ▼             ▼
                  [상태 채택]   [로그 복원]
```

### 동작 원리

1. **복구 로그 기록**: WAL(Write-Ahead Log) 메타데이터 비휘발 작성.
2. **로그 플러시·펜스**: 플랫폼 영속성 영역에 맞춰 **clwb**와 **sfence**로 로그 영속화.
3. **본 데이터 기록·플러시**: 실제 데이터 갱신 및 **clwb** 인가.
4. **커밋 표식 영속**: Commit Flag 작성 후 **sfence**로 완료 확정하는 **순서 보존 쓰기**
5. **복구 상태 판정**: 부팅 시 Commit Flag 유무 판단으로 상태 로딩

#### 한줄 요약

- 순서 보존 쓰기로 로그→데이터→커밋 순서를 지켜야 장애 후 완료된 변경과 미완료 변경을 정확히 구분할 수 있다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NVDIMM(Non-Volatile DIMM)**: DRAM과 Flash를 단일 DIMM에 혼합하거나(NVDIMM-N), 차세대 비휘발 소자를 결합한 표준 메인 메모리 폼팩터.

</details>

| 비교 항목 | PMEM (Persistent Memory) | DRAM | NVMe SSD |
|:---|:---|:---|:---|
| 접근 단위 | Byte-Level (**DAX**) | Byte-Level | Block-Level |
| 비휘발성 유무 | 비휘발성 (Non-Volatile) | 휘발성 (Volatile) | 비휘발성 (Non-Volatile) |
| 접근 지연시간 | DRAM보다 길고 SSD보다 짧은 계층 | 가장 짧은 휘발 메모리 계층 | 블록 프로토콜과 매체 지연 포함 |
| 전송 메카니즘 | 시스템 버스 (DDR/CXL) | 시스템 버스 (DDR) | PCIe 레인 (NVMe Protocol) |

#### 한줄 요약

- 빠른 재시작 상태에는 영속 메모리, 휘발 작업 데이터에는 DRAM, 대용량 보관 데이터에는 SSD를 배치한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Power-Failure Injection**: 개발 완료 후 전원을 강제로 비정기 셧다운하여 PMEM 상의 Crash Consistency 정합성을 검증하는 테스팅.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CPU 캐시 데이터가 영속성 영역에 도달하기 전 정전 | **clwb·sfence** 순서와 **ADR/eADR** 범위 확인 | 영속 완료로 오인하는 쓰기 방지 |
| absolute 포인터 주소 기록 시 주소 공간 재배치(ASLR) 오류 | **상대 포인터** 및 offset 기반 매핑 | 시스템 재부팅 후 주소 포인터 복구 성공 |
| 비휘발 갱신 순서 교란에 따른 DB 정합성 와해 | **PMDK** 라이브러리 적용 및 **Power-Failure Injection** | **장애 정합성** 확보 |

> 사례: In-Memory DB(Redis/SAP HANA) 상의 **PMEM** 및 **DAX** 적용을 통한 초고속 복구 인프라 구축

#### 한줄 요약

- 캐시 라인 플러시와 메모리 펜스 순서를 정전 주입 시험으로 검증한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **PMEM 선택 기준(PMEM Adoption Criteria)**: 초저지연 바이트 억세스, 장애 정합성 수용 및 CXL 확장성에 기반한 체계.

</details>

- 바이트 주소 영속 상태는 **PMEM**, 휘발 작업은 **DRAM**, 대용량 보관은 **NVMe SSD** 선택

#### 한줄 요약

- 바이트 영속 상태는 PMEM, 휘발 작업은 DRAM, 대용량 보관은 SSD를 선택한다.
