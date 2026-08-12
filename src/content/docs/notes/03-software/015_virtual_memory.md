---
sidebar:
  order: 15
  label: "015. 가상 메모리•페이징•세그멘테이션 (Virtual Memory)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "가상 메모리•페이징•세그멘테이션 (Virtual Memory)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 15
extra:
  question_no: "015"
  source_status: "기출"
  source_history: "120회, 125회, 126회"
  priority: 70
  priority_note: "120•125•126회 반복, 가상 메모리 구조 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Virtual Memory (가상 메모리)**: 물리 메모리(RAM) 크기의 한계를 넘어, 보조기억장치(Disk Swap Space)의 일부를 주기억장치처럼 확장하여 각 프로세스에게 독립된 논리적 주소 공간(Address Space)을 제공하는 기술.
- **Paging (페이징)**: 가상 주소 공간과 물리 주소 공간을 고정된 동일 크기 블록(Page / Frame, 보통 4KB)으로 분할하여 메모리를 관리하는 비연속 메모리 할당 기법.
- **Segmentation (세그멘테이션)**: 논리적 의미 단위(Code, Data, Stack, Heap 등)의 가변 크기 세그먼트 블록 단위로 메모리를 분할 주소 변환하는 기법.

</details>

- 정의/개념: 물리적 RAM 크기 제약을 극복하고 논리 주소를 물리 주소로 자동 바인딩 매핑하는 매커니즘인 **가상 메모리(Virtual Memory)** 및 구현 기법인 **Paging & Segmentation**
- 배경/필요성: 프로세스 간 메모리 침범 방지(Isolation), 프로그래머의 주소 공간 관리 용이성 및 다중 프로그래밍 가용성 극대화 요구성

#### 한줄 요약

- 독립 가상 주소를 물리 메모리와 후면 저장소에 연결한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **MMU (Memory Management Unit)**: CPU에 내장된 하드웨어 칩으로, 프로세스의 가상 주소(Virtual Address)를 물리 주소(Physical Address)로 고속 변환 연산하는 장치.
- **Page Table**: 가상 페이지 번호(VPN)를 물리 프레임 번호(PFN)로 변환하기 위해 메모리 상에 상주하는 주소 변환 매핑 테이블.
- **TLB (Translation Lookaside Buffer)**: MMU 내부에 탑재된 고속 하드웨어 주소 변환 캐시 메모리.

</details>

- 프로세스 독립 주소 공간(Isolation) 보장 및 보호(Protection Bit)
- **Paging (고정 크기, 내부 단편화)** vs **Segmentation (가변 크기, 외부 단편화)**
- **MMU, Page Table, TLB** 하드웨어 기반 고속 주소 변환 바이패스 구조

#### 한줄 요약

- 주소 공간 격리와 요구 페이징 기반 탄력적 할당이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Internal Fragmentation (내부 단편화)**: 페이징 기법에서 고정 4KB 블록 할당 시 내부 남은 여유 공간이 낭비되는 현상.
- **External Fragmentation (외부 단편화)**: 세그멘테이션 기법에서 가변 크기 할당 및 해제가 반복되면서 총 여유 공간은 충분하나 연속된 공간이 부족하여 할당 불가한 현상.

</details>

```text
                [프로세서]
                    |
                [MMU•TLB]
                    |
             [페이지 테이블]
                    |
           [페이지 폴트 처리기]
                    |
      [물리 메모리•후면 저장소]
```

선의 의미: 프로세서 가상 주소가 MMU/TLB를 거쳐 페이지 테이블 및 물리 메모리/Swap 공간으로 변환 연결되는 메모리 파이프라인.

| 구성요소 | 책임 |
|:---|:---|
| MMU & TLB | CPU 가상 주소(VA)를 수 $ns$ 이내에 물리 주소(PA)로 변환 (**TLB Hit**) |
| Multi-level Page Table | 4단계(x86-64 48-bit/57-bit) 계층형 페이지 테이블 구조로 메인 메모리 절감 |
| Segment Table | Segment Base 및 Limit 바운더리를 기록하여 논리 세그먼트 주소 변환 |
| Page Fault Handler | TLB/Page Table 상의 Valid Bit = 0 시 인터럽트를 수신하여 Disk Swap 이송 |

#### 한줄 요약

- MMU, 페이지 테이블, 페이지 폴트 처리기가 주소 변환 구조를 이룬다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Page Table Walk**: TLB Miss 발생 시, MMU가 DRAM 메모리 상의 다단계 페이지 테이블(PGD-P4D-PUD-PMD-PTE) 노드들을 순차 트래버스하는 하드웨어 연산.

</details>

```text
┌──────────────────────────────┐
│ 가상 주소•접근 유형         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. TLB 조회                 │◀──────────────┐
│ 2. 페이지 테이블 워크       │               │
│ 3. 변환 상태 판정           │               │
└───────┬──────────────────────┘               │
        ├─ 권한 위반 ─────────────▶ [접근 차단]
        ├─ 상주•허용 ─────────────▶ [4. 물리 메모리 접근]
        │ 비상주                               │
        ▼                                      │
┌──────────────────────────────┐              │
│ 5. 페이지 폴트 처리         │              │
│ 적재•매핑 갱신              │──────────────┘
└──────────────────────────────┘   명령 재실행
```

### 동작 원리

1. **TLB 조회**: 가상 주소(VPN) 인가 시 MMU 내부 **TLB** 우선 검색 (TLB Hit 시 즉시 물리 주소 연산 완료).
2. **페이지 테이블 워크**: TLB Miss 시 DRAM 상의 **Page Table Walk** 트래버스 연산 수행.
3. **변환 상태 판정**: Valid Bit (상주 여부) 및 Protection Bits (Read/Write/Exec) 검증.
4. **물리 메모리 접근**: Valid Bit = 1 이면 물리 프레임 주소(PFN) 결합 후 DRAM 억세스.
5. **페이지 폴트 처리**: Valid Bit = 0 이면 **Page Fault Interrupt**발동 $\to$ Disk Swap에서 DRAM 적재 후 매핑 갱신 및 명령 재실행.

#### 한줄 요약

- TLB 미스•페이지 부재에 따라 변환과 적재를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Paged Segmentation**: 세그멘테이션으로 논리 영역(Code, Data, Stack)을 나누고, 각 세그먼트 내부를 다시 고정 크기 페이징으로 세분화하는 혼합 메모리 관리 기법.

</details>

| 비교 항목 | Paging (페이징) | Segmentation (세그멘테이션) | Paged Segmentation |
|:---|:---|:---|:---|
| 분할 단위 | 고정 크기 (Fixed 4KB, 2MB, 1GB) | 가변 크기 (논리적 세그먼트 단위) | 세그먼트 분할 후 세부 페이징 |
| 단편화 문제 | **내부 단편화 (Internal Frag)** | **외부 단편화 (External Frag)** | 내부 단편화 미세 잔류 |
| 주소 구조 | 단일 연속 가상 주소 ($Page + Offset$) | 2차원 논리 주소 ($Segment + Offset$) | 2차원 주소의 페이징 변환 |
| 메인 장점 | 외부 단편화 전면 소멸, Swap 용이 | 논리적 단위의 보안 및 공유 완벽 | 단편화 차단 + 논리적 보호 우수 |

#### 한줄 요약

- 비연속 할당은 페이징, 논리 보호는 세그멘테이션이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Huge Pages**: Linux 커널에서 기본 4KB 페이지 대신 2MB/1GB 대형 페이지를 할당하여 Page Table 메모리 상주량 및 TLB Miss 오버헤드를 대폭 억제하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 메모리(수백 GB DB) 사용 시 TLB Miss 폭증 | **Huge Pages (2MB / 1GB)** 적용 | TLB 커버리지 극대화 및 미스 소멸 |
| 64-bit 주소 공간 적용으로 페이지 테이블 크기 비대화 | **Multi-level Page Table** 또는 Inverted Page Table 적용 | 주소 매핑 메모리 절감 |
| 세그멘테이션 적용 시 메모리 구멍 발생(외부 단편화) | **Compaction (메모리 압축)** 및 Paged Segmentation 전환 | 가용 연속 메모리 확보 |

> 사례: Linux x86-64 **4-Level / 5-Level Paging** 및 Oracle DB 전용 **HugePages** 튜닝

#### 한줄 요약

- 권한•폴트•TLB 비용을 함께 고려해 페이지 정책을 정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **가상 메모리 선택 기준(Virtual Memory Architecture Criteria)**: 시스템 아키텍처 비트 수, 워크로드 메모리 크기, TLB 커버리지 수치에 근거한 설계 체계.

</details>

- **가상 메모리 선택 기준**에 따라 현대 범용 OS 및 하이퍼바이저는 **Paging / Multi-level Page Table & HugePages** 구현체 채택

#### 한줄 요약

- 비연속 할당과 논리 보호에 맞는 분할 방식을 선택한다.
