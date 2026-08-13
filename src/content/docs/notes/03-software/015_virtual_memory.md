---
sidebar:
  order: 15
  label: "015. 가상 메모리•페이징•세그멘테이션 (Virtual Memory)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "가상 메모리•페이징•세그멘테이션 (Virtual Memory)"
date: "2026-08-13T13:23:00+09:00"
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

- **Virtual Memory (가상 메모리)**: 가상 주소를 물리 프레임에 매핑하여 프로세스별 주소 공간과 보호를 제공하는 메모리 추상화.
- **Paging (페이징)**: 가상 주소 공간과 물리 주소 공간을 고정된 동일 크기 블록(Page / Frame, 보통 4KB)으로 분할하여 메모리를 관리하는 비연속 메모리 할당 기법.
- **Segmentation (세그멘테이션)**: 논리적 의미 단위(Code, Data, Stack, Heap 등)의 가변 크기 세그먼트 블록 단위로 메모리를 분할 주소 변환하는 기법.

</details>

- 정의/개념: 물리적 RAM 크기 제약을 극복하고 논리 주소를 물리 주소로 자동 바인딩 매핑하는 매커니즘인 **가상 메모리(Virtual Memory)** 및 구현 기법인 **Paging & Segmentation**
- 배경/필요성: 제한된 **물리 메모리**로는 대형 프로세스의 온전한 적재와 다중 실행 불가

#### 한줄 요약

- 독립 가상 주소를 물리 메모리와 후면 저장소에 연결한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **MMU (Memory Management Unit)**: 페이지 테이블과 TLB를 이용해 가상 주소를 물리 주소로 변환하고 권한을 검사하는 하드웨어.
- **Page Table**: 가상 페이지 번호(VPN)를 물리 프레임 번호(PFN)로 변환하기 위해 메모리 상에 상주하는 주소 변환 매핑 테이블.
- **TLB (Translation Lookaside Buffer)**: MMU 내부에 탑재된 고속 하드웨어 주소 변환 캐시 메모리.

</details>

- 프로세스 독립 주소 공간(Isolation) 보장 및 보호(Protection Bit)
- **Paging (고정 크기, 내부 단편화)** vs **Segmentation (가변 크기, 외부 단편화)**
- **MMU•Page Table•TLB** 기반 주소 변환과 접근 권한 검사

#### 한줄 요약

- 주소 공간 격리와 요구 페이징 기반 탄력적 할당이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Internal Fragmentation (내부 단편화)**: 페이징 기법에서 고정 4KB 블록 할당 시 내부 남은 여유 공간이 낭비되는 현상.
- **External Fragmentation (외부 단편화)**: 세그멘테이션 기법에서 가변 크기 할당 및 해제가 반복되면서 총 여유 공간은 충분하나 연속된 공간이 부족하여 할당 불가한 현상.

</details>

```text
[주소 변환 구조]
 ├─ MMU & TLB
 ├─ Multi-level Page Table
 ├─ Segment Table
 └─ 페이지 폴트 처리기
```

| 구성요소 | 책임 |
|:---|:---|
| MMU & TLB | 가상 주소 변환 캐시 조회와 **권한 검사** |
| Multi-level Page Table | 사용 주소 범위만 하위 테이블을 할당해 메모리 절감 |
| Segment Table | Segment Base 및 Limit 바운더리를 기록하여 논리 세그먼트 주소 변환 |
| 페이지 폴트 처리기 | 페이지 부재 예외를 처리해 적재•매핑 또는 접근 거부 |

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

1. **TLB 조회**: 가상 주소 인가 시 MMU 내부 **TLB**를 우선 검색해 주소 변환
2. **페이지 테이블 워크**: TLB 미스 시 메모리 상의 다단계 테이블 트래버스 연산 수행
3. **변환 상태 판정**: 유효 비트와 권한 비트를 검증해 접근 허용 여부 확인
4. **물리 메모리 접근**: 유효 비트 확인 후 **프레임 주소**를 결합해 물리 메모리 접근
5. **페이지 폴트 처리**: 부재 시 디스크에서 **페이지 적재** 후 매핑을 갱신해 재실행

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
| 주요 장점 | 외부 단편화 제거와 비연속 할당 | 논리 단위 보호•공유 | 논리 보호와 비연속 할당 결합 |

#### 한줄 요약

- 비연속 할당은 페이징, 논리 보호는 세그멘테이션이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Huge Pages**: Linux 커널에서 기본 4KB 페이지 대신 2MB/1GB 대형 페이지를 할당하여 Page Table 메모리 상주량 및 TLB Miss 오버헤드를 대폭 억제하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 메모리 사용 시 TLB 미스 증가 | 워크로드 검증 후 **Huge Pages** 적용 | TLB 도달 범위 확대 |
| 64-bit 주소 공간 적용으로 페이지 테이블 크기 비대화 | **Multi-level Page Table** 또는 Inverted Page Table 적용 | 주소 매핑 메모리 절감 |
| 세그멘테이션 적용 시 메모리 구멍 발생(외부 단편화) | **Compaction (메모리 압축)** 및 Paged Segmentation 전환 | 가용 연속 메모리 확보 |

> 사례: Linux x86-64 **4-Level / 5-Level Paging** 및 Oracle DB 전용 **HugePages** 튜닝

#### 한줄 요약

- 권한•폴트•TLB 비용을 함께 고려해 페이지 정책을 정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **가상 메모리 선택 기준(Virtual Memory Architecture Criteria)**: 시스템 아키텍처 비트 수, 워크로드 메모리 크기, TLB 커버리지 수치에 근거한 설계 체계.

</details>

- 범용 환경은 **다단계 페이징**, 대용량 워크로드는 **HugePages** 적용

#### 한줄 요약

- 비연속 할당과 논리 보호에 맞는 분할 방식을 선택한다.
