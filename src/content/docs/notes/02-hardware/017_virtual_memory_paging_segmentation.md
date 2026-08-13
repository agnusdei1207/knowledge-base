---
sidebar:
  order: 17
  label: "017. 가상 메모리: 페이징•세그멘테이션 (Virtual Memory Paging Segmentation)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "가상 메모리: 페이징•세그멘테이션 (Virtual Memory Paging Segmentation)"
date: "2026-08-13T11:39:07+09:00"
tags:
  - "notes-hardware"
weight: 17
extra:
  question_no: "017"
  source_status: "기출"
  source_history: "120회, 125회, 138회"
  priority: 70
  priority_note: "반복 기출•주소 변환 방식 판별"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **가상 메모리(Virtual Memory)**: 프로세스에 실제 물리적 DRAM 용량과 무관한 커다란 연속 추상화 주소 공간을 제공하고, 물리 메모리와 보조기억장치를 연동하여 주소 격리 및 요구 적재(Demand Paging)를 지원하는 관리 체계.
- **물리 프레임(Physical Frame / Page Frame)**: 물리 메모리(DRAM)를 페이지 크기(예: 4KB)와 동일한 고정 크기 블록으로 분할하여 데이터를 배치하는 단위.
- **페이징(Paging)**: 가상 주소 공간과 물리 주소 공간을 고정 크기(Fixed-size)의 페이지 및 프레임으로 분할 매핑하여 메인 메모리를 관리하는 기술.
- **세그멘테이션(Segmentation)**: 코드, 데이터, 스택 등 의미론적 논리 블록 단위인 가변 크기(Variable-size) 세그먼트로 메모리를 분할 매핑하는 기술.

</details>

- 정의: **페이징**과 **세그멘테이션**으로 구별되는 **가상 메모리** 아키텍처
- 배경: 물리 메모리 한계로 다중 프로세스 **동시 적재 불가** 및 주소 침범 위험

#### 한줄 요약
- 가상·물리 주소 분리로 프로세스 격리 및 **요구 페이징** 보장

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **가상 주소 공간(Virtual Address Space)**: 각 독립 프로세스가 타 프로세스와의 충돌 없이 독점 참조할 수 있는 0번지부터의 논리적 연속 주소 영역.
- **요구 페이징(Demand Paging)**: 프로그램 실행에 필요한 페이지 데이터만 참조 시점(Page Fault 발생)에 보조기억장치에서 물리 RAM 프레임으로 인출 적재하는 기술.
- **비상주 페이지(Non-Resident Page / Present=0)**: 가상 주소 공간상에는 할당되었으나 실제 물리 RAM에는 들어있지 않고 SSD 스왑 파티션에 위치한 상태.
- **보조기억장치(Secondary Storage / Swap Area)**: 비상주 익명 페이지나 파일 데이터를 보관하는 저장장치 영역.

</details>

- 프로세스별 독립 **가상 주소 공간** 보장, 무단 접근 차단
- 물리 RAM 초과 주소를 **비상주 페이지**로 스왑 영역 오프로드
- **요구 페이징**으로 참조 시점에만 프레임 할당

#### 한줄 요약
- 가상·물리 분리로 접근 보호 및 **요구 페이징** 기반 효율화

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **메모리 관리 장치(Memory Management Unit, MMU)**: 가상 주소(VA)를 받아 페이징/세그멘테이션 메타데이터를 참조하여 물리 주소(PA)로 하드웨어 실시간 변환하는 블록.
- **변환 색인 버퍼(Translation Lookaside Buffer, TLB)**: 최근 주소 변환(VPN->PPN) 결과를 캐싱하여 MMU 변환을 1주기 이내로 가속하는 전용 룩업 캐시.
- **페이지 테이블 항목(Page Table Entry, PTE)**: PPN, Valid/Present Bit, Dirty Bit, Reference Bit, R/W/X Protection Bit 정보가 담긴 페이징 엔트리.
- **세그먼트 기술자(Segment Descriptor)**: 세그먼트 시작 물리 주소(Base), 세그먼트 크기(Limit), 접근 권한이 담긴 8바이트 서술자 표.
- **물리 페이지 번호(Physical Page Number, PPN)**: 메인 메모리 내 물리 페이지 프레임의 고유 번호.
- **페이지 테이블(Page Table)**: 프로세스의 가상 페이지 번호(VPN)를 물리 페이지 번호(PPN)로 매핑한 메모리 내 배열.

</details>

```text
+----------------------------------------------+
|           Virtual Memory Architecture        |
| +------------------------------------------+ |
| |  Paging (Fixed-size Page/Frame)           | |
| |  +--------+    +-------------+           | |
| |  | VPN    |    | Page Table  |    PPN     | |
| |  +--------+    +-------------+           | |
| +------------------------------------------+ |
| +------------------------------------------+ |
| |  Segmentation (Variable-size Segment)    | |
| |  +----------+   +-----------+            | |
| |  | Selector |   | Descriptor|    Base   | |
| |  +----------+   +-----------+            | |
| +------------------------------------------+ |
+----------------------------------------------+
        |               |
   +----+----+     +----+----+
   | MMU     |     | TLB     |
   +---------+     +---------+
```

| 구성요소 | 책임 |
|:---|:---|
| MMU·TLB | 주소 변환 가속 및 접근 권한 검사 |
| 페이지 테이블 | **VPN**을 **PPN**으로 고정 크기 매핑 |
| 세그먼트 기술자 | Base·Limit·권한 기반 가변 크기 매핑 |
| 물리 메모리 | 변환 결과를 받아 데이터 적재·반환 |

#### 한줄 요약
- **MMU/TLB**와 Page Table 또는 Segment Descriptor 결합 구조

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **페이지 폴트(Page Fault)**: 참조하려는 가상 페이지가 RAM에 상주하지 않아(Present=0) OS가 SSD 스왑 영역에서 해당 페이지를 메모리로 읽어오는 트랩 예외.
- **명령 재시작(Instruction Restart)**: Page Fault 수습 완료 후, 중단되었던 기계어 레벨 메모리 접근 명령을 처음부터 다시 가동하는 CPU 회로 기능.
- **가상 페이지 번호(Virtual Page Number, VPN)**: 가상 주소에서 페이지 테이블 인덱싱에 사용되는 상위 비트.
- **접근 예외(Access Exception / General Protection Fault)**: 세그먼트 Limit 크기를 초과하거나 읽기 전용 구역에 쓰기를 시도할 때 하드웨어가 발생하는 보안 트랩.

</details>

```text
 CPU VA Request
      |
      v
+----------------------------------+
| TLB / Page Table Lookup          |
|    (VPN -> PPN 변환)              |
+--------+--------+----------------+
  [Hit]  |        | [Miss: Present=0]
         v        v
  PA 반환     +----------------------------+
              | Page Fault Exception        |
              |    OS Swap-In 수행          |
              +-------------+--------------+
                            |
                            v
              +----------------------------+
              | 명령 재시작                 |
              |    Instruction Restart     |
              +----------------------------+
```

### 동작 원리

- **TLB•페이지 테이블 조회**: **VPN**으로 매핑과 접근 권한 검사
- **Page Fault 예외**: 비상주면 파일•스왑에서 적재, 위반이면 오류 처리
- **명령 재시작**: 복구 가능한 폴트 처리 후 **Instruction Restart** 수행

#### 한줄 요약
- VPN 변환 → Present 검사 → Hit 시 PA 반환, Miss 시 **Page Fault** 수습

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **내부 단편화(Internal Fragmentation)**: 고정 4KB 페이지 할당 시 프로그램 마지막 데이터가 1KB만 사용하여 남아버리는 3KB의 낭비 공간.
- **외부 단편화(External Fragmentation)**: 가변 세그먼트의 반복 할당/해제로 메모리 사이에 총 여유 공간은 충분하나 연속된 구역이 없어 세그먼트를 적재하지 못하는 현상.
- **비연속 프레임 배치(Non-Contiguous Allocation)**: 가상 주소상으로는 연속된 공간이 물리 메모리 DRAM에서는 완전히 파편화된 비연속 프레임들에 나누어 적재되는 성질.

</details>

| 비교 항목 | 페이징 방식 (Paging) | 세그멘테이션 방식 (Segmentation) |
|:---|:---|:---|
| **분할 단위** | 하드웨어 중심의 **고정 크기** (Fixed 4KB, 2MB) | 사용자/소프트웨어 논리 단위의 **가변 크기** (Code, Data, Stack) |
| **메모리 배치** | **비연속 프레임 배치(Non-Contiguous)** 가능 | 논리 세그먼트 단위의 **연속 메모리 배치** 필수 |
| **주소 구조** | 가상 페이지 번호(VPN) + 오프셋(Offset) | 세그먼트 선택자(Selector) + 오프셋(Offset) |
| **단편화 문제** | **내부 단편화(Internal Fragmentation)** 발생 가능 | **외부 단편화(External Fragmentation)** 심각 발생 |
| **보호 및 공유** | 페이지 단위 접근 권한 비트(R/W/X) 관리 | 논리 영역 단위로 모듈 간 공유 및 코드 보호에 매우 용이 |
| **현대 칩 채택** | 범용 OS 및 64-bit CPU 표준 매핑 방식 | x86-64 등 최신 아키텍처에서는 페이징 기반 통합/축소됨 |

#### 한줄 요약
- **페이징**(고정 크기·내부 단편화)과 **세그멘테이션**(가변 크기·외부 단편화), 현대 OS는 페이징 주력

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **쓰레싱(Thrashing)**: RAM이 작업 집합을 수용하지 못해 연산보다 Page Fault와 스왑 입출력이 반복되는 상태.
- **주 페이지 폴트(Major Page Fault)**: SSD/HDD 등 디스크 I/O가 실제로 수반되어 시스템 지연을 유발하는 Page Fault.
- **부 페이지 폴트(Minor Page Fault)**: 이미 다른 프로세스에 의해 RAM 프레임에 로드되어 있어 디스크 I/O 없이 페이지 테이블 매핑만 연결하는 Page Fault.
- **읽기 전용 공유 프레임(Read-Only Shared Frame)**: `libc` 등 공통 공유 라이브러리 코드를 여러 프로세스가 단 1개의 물리 RAM 프레임에 읽기 전용으로 매핑하여 메모리를 절감하는 기법.
- **페이지-세그멘테이션 혼용 (Paged Segmentation)**: 세그멘테이션의 논리적 공유/보호 장점과 페이징의 외부 단편화 방지 장점을 결합하여 세그먼트 내부를 다시 고정 페이지로 나누어 관리하는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 메모리 부족 시 **주 페이지 폴트(Major Fault)** 급증 및 **쓰레싱(Thrashing)** 발생 | Working Set 기반 메모리 쿼터 설정 및 수평 팟(Pod) 오토스케일링 | 디스크 스왑 I/O 마비 및 서비스 멈춤 현상 원천 차단 |
| 동일 라이브러리가 프로세스별로 중복 적재되어 RAM 낭비 | **읽기 전용 공유 프레임**으로 같은 물리 페이지 매핑 | 공유 코드의 중복 물리 프레임 제거 |
| 순수 세그멘테이션 도입 시 **외부 단편화**로 인한 메모리 배치 불능 | 세그먼트 내부를 4KB 페이지로 분할하는 **Paged Segmentation** 채택 | 외부 단편화 방지 및 세그먼트 논리 보호 장점 동시 수용 |
| 프로세스 생성/종료 시 가상 메모리 테이블 갱신 오버헤드 | CoW(Copy-on-Write) 기법 기반 `fork()` 프로세스 주소 공간 생성 | 메모리 복사 지연 은닉 및 프로세스 생성 속도 대폭 개선 |

#### 한줄 요약
- **Working Set** 모니터링, **Shared Frame**, **Paged Segmentation**, **CoW** 적용

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **메모리 가상화 선택 기준(Memory Virtualization Selection Criteria)**: 대상 시스템의 물리 RAM 용량, 프로세스 간 코드 공유 요구, 외부 단편화 리스크를 평가하여 페이징 및 세그멘테이션 혼용 구조를 선택하는 결정 프레임워크.

</details>

- 범용 OS는 **페이징**, 논리 영역은 페이지 권한•매핑으로 보호

#### 한줄 요약
- 고정 페이지 매핑을 기본으로 공유•복제 요구에는 **CoW** 적용
