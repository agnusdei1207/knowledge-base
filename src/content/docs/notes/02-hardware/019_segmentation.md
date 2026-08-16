---
sidebar:
  order: 19
  label: "019. 세그멘테이션 (Segmentation)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "세그멘테이션 (Segmentation)"
date: "2026-08-13T11:40:33+09:00"
tags:
  - "notes-hardware"
weight: 19
extra:
  question_no: "019"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "페이징과의 비교 축"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **세그멘테이션(Segmentation)**: 프로그램의 가상 주소 공간을 의미론적 모듈(코드, 데이터, 스택, 힙 등) 단위인 가변 크기의 논리적 영역(Segment)으로 나누어 독립된 보호 및 주소 변환을 수행하는 메모리 관리 기법.
- **논리 권한 경계(Logical Permission Boundary)**: 코드 세그먼트(Read/Execute), 데이터 세그먼트(Read/Write), 스택 세그먼트(Read/Write/Grow) 등 영역별로 특화된 메인 메모리 보호 및 상호 접근 제어 한계선.
- **평면 주소 공간(Flat Address Space)**: 세그먼트 논리 구분 없이 0번지부터 64-bit 끝 번지까지를 1개의 단일 연속 일직선 메모리로 취급하는 구조.

</details>

- 정의/개념: 프로그램 주소 공간을 의미론적 가변 영역(Code, Data, Stack)으로 구분하고, 세그먼트별 **기준 주소** 및 **한계** 서술자를 통해 주소 변환과 보호를 수행하는 **세그멘테이션**.
- 배경/필요성: 영역별 크기•권한 경계가 없으면 코드 쓰기와 스택 범위 침범을 주소 변환 단계에서 구분하기 어려움.

#### 한줄 요약
- 가상 메모리를 가변 크기의 논리 모듈 단위로 분할하여 개별 Base/Limit 서술자 기반의 주소 변환 및 영역 보호를 제공하는 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **2차원 주소(Two-Dimensional Address Space)**: 프로세스가 주소를 지정할 때 `[Segment Selector : Offset]` 구조의 2개 파라미터 조합으로 참조하는 주소 지정 방식.
- **기준 주소(Base Address)**: 해당 세그먼트가 시작되는 실제 물리 DRAM의 바이트 시작 주소.
- **한계(Limit / Bound)**: 해당 세그먼트가 물리 메모리상에서 차지하는 최대 가변 길이 용량 크기.
- **독립 성장(Independent Growth)**: 스택과 힙 세그먼트가 타 영역을 침범하지 않고 상호 반대 방향으로 용량을 가변 확장하는 성질.

</details>

- 프로세스가 `[Segment Selector : Offset]` 형태의 **2차원 주소(Two-Dimensional Address)**를 사용하여 프로그램 논리 구조와 직접 매핑.
- 세그먼트 기술자에 포함된 **기준 주소**와 **한계** 비트를 대조하여 영역별 **독립 성장**과 경계 범위를 하드웨어적으로 보호.
- 가상 주소 변환 시 별도의 다단계 메인 메모리 테이블 순회 없이 `Physical Address = Base Address + Offset` 공식을 적용하는 **단일 단계 변환** 구동.

#### 한줄 요약
- Segment Selector와 Offset 2차원 주소 구조를 사용하며 Base+Offset 단일 덧셈 변환 및 Limit 경계 검사를 수행함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **세그먼트 기술자(Segment Descriptor)**: 8바이트 구성의 하드웨어 태그로, Base 주소(32/64-bit), Limit 크기(20-bit), Present Bit, Privilege Level(DPL), Protection Bit(R/W/X) 정보를 저장하는 엔트리.
- **세그먼트 테이블(Segment Table / GDT, LDT)**: x86 등 아키텍처에서 시스템 전체(GDT) 및 프로세스별(LDT) 세그먼트 기술자 배열을 저장 보관하는 테이블.

- **서술자 특권 레벨(Descriptor Privilege Level, DPL)**: 세그먼트에 접근하기 위해 요구되는 최소 CPU 특권 등급(Ring 0~3)을 명시한 보안 필드.
</details>

```text
[ Segmentation Address Translation ]
├─ Virtual Address
│  ├─ Segment Selector
│  └─ Offset
├─ Segment Table
│  └─ Descriptor: Base | Limit | Privilege
├─ Protection Checker
└─ Address Generator
```

| 구성요소 | 책임 |
|:---|:---|
| 세그먼트 기술자 | **Base•Limit•DPL•권한** 보관 |
| 보호 검사기 | **Limit•R/W/X•특권** 조건 검사 |
| 주소 생성기 | 유효 요청의 **Base+Offset** 계산 |
| 세그먼트 테이블 | 시스템•프로세스의 **기술자 집합** 보관 |

#### 한줄 요약
- Segment Descriptor, Protection Checker(Limit 대조) 및 Address Generator(Base+Offset 가산기)가 결합하여 구동함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **세그먼트 번호(Segment Selector)**: CS, DS, SS 등 레지스터에 탑재되어 세그먼트 테이블 인덱스 번호를 선택하는 16비트 주소 필드.
- **보호 예외(Protection Exception / Segment Fault)**: Offset >= Limit 이거나 읽기 전용 코드 세그먼트에 쓰기를 시도할 때 하드웨어 MMU가 발생하는 예외 트랩.

</details>

```text
[ Memory Access Request (Segment Selector + Offset) ]
                          │
                          ▼
             [ 1. 기술자 인출 ]
                          │
                          ▼
             [ 2. 권한•존재 검사 ]
             ├─ Invalid / Not Present ──> [ Segment Not Present Fault ]
             └─ Valid
                   │
                   ▼
             [ 3. 한계 검사 ]
             ├─ Offset >= Limit ──> [ Protection Exception (GP Fault) ]
             └─ Offset < Limit
                   │
                   ▼
             [ 4. 물리 주소 생성 ] ──> Physical RAM Access
```

### 동작 원리

1. **기술자 인출**: Selector로 GDT•LDT의 **세그먼트 기술자**를 선택함.
2. **권한•존재 검사**: Present와 **DPL•접근 권한**을 검사함.
3. **한계 검사**: Offset이 Limit을 넘으면 **보호 예외**를 발생함.
4. **물리 주소 생성**: 유효하면 **Base+Offset**으로 선형 주소를 생성함.

#### 한줄 요약
- Descriptor Fetch -> Present/Privilege Check -> Limit Check(Offset < Limit) -> Base+Offset 덧셈으로 PA 생성을 완결함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **외부 단편화(External Fragmentation)**: 가변 크기의 세그먼트들이 할당/해제되는 과정에서 메모리 사이에 자투리 유휴 공간이 흩어져, 총 여유 메모리는 충분하나 연속된 구역이 부족하여 새 세그먼트를 적재하지 못하는 심각한 현상.
- **세그먼트-페이징(Segmented Paging / Paged Segmentation)**: 세그멘테이션으로 논리적 모듈 구분 및 권한 보호를 적용하고, 각 세그먼트 내부를 다시 고정 크기 4KB 페이지로 분할하여 페이징 비연속 배치를 실행하는 결합 구조.

</details>

| 비교 항목 | 세그멘테이션 (Segmentation) | 페이징 (Paging) | 세그먼트-페이징 (Segmented Paging) |
|:---|:---|:---|:---|
| 분할 단위 | 논리적 **가변 크기** (Code, Data, Stack) | 물리적 **고정 크기** (4KB, 2MB) | 논리 세그먼트 내 고정 페이지 분할 |
| 단편화 문제 | **외부 단편화** 발생 | **내부 단편화** 발생 | 내부 단편화만 일부 미세 발생 |
| 주소 변환 | `Base + Offset` 단일 덧셈 | `VPN -> PPN` 페이지 테이블 변환 | `Selector -> Page Table -> PPN` |
| 메모리 배치 | 물리적 연속(Contiguous) 공간 필수 | 비연속(Non-Contiguous) 프레임 분산 | 비연속 물리 프레임 분산 |
| 장점 | 모듈별 보호 및 공유 구현이 극히 단순 | 외부 단편화 원천 제거 및 메모리 활용 | 두 방식의 장점 결합 (보호+비연속) |

#### 한줄 요약
- 세그멘테이션은 모듈 보호에 최적화되었으나 외부 단편화 문제가 심각하여 현대 아키텍처에서는 페이징과 결합한 Segmented Paging으로 채택됨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **가드 영역(Guard Page / Guard Region)**: 스택 등 확장 경계에 접근 금지 페이지를 배치하여 범위 초과를 예외로 감지하는 기법.
- **TLB 지역성(TLB Locality)**: Segmented Paging 구조에서 세그먼트 테이블과 페이지 테이블의 다중 변환 지연을 차단하기 위해 TLB 룩업 캐시를 고도화하는 최적화.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 가변 세그먼트 재할당 시 메모리 파편화로 인한 **외부 단편화** 폭증 | 세그먼트 내부를 고정 4KB 페이지로 자르는 **Segmented Paging** 도입 | 외부 단편화 완벽 제거 및 비연속 물리 메모리 적재 |
| 동적 스택 확장 시 힙 세그먼트 구역을 무단 덮어쓰는 메모리 오염 | 스택-힙 세그먼트 경계면에 접근 불가 **가드 영역** 배치 | 스택 오버플로 발생 시 즉시 하드웨어 예외 트랩으로 세그먼트 보호 |
| 개발자 실수로 오프셋 범위 초과하여 타 영역 메모리 오작동 | **최소 권한** 및 컴파일러 **경계값 시험** | General Protection Fault를 통한 오작동 원천 차단 |
| 세그먼트 테이블 + 페이지 테이블 2중 변환에 따른 주소 지연 | MMU 내부 **TLB** 캐싱 및 **표 지역성** 극대화 | 2중 변환 지연을 1클록 변환으로 가속 |

#### 한줄 요약
- Segmented Paging 기법, Guard Region 배치, Boundary Testing 및 TLB 테이블 지역성 보정을 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **논리 보호 프레임워크(Logical Protection Framework)**: 64비트 아키텍처에서 페이징 기반 하드웨어를 주축으로 활용하면서, 소프트웨어적 세그멘테이션 논리 권한 제어를 결합하는 가상 메모리 설계 기준.

</details>

- 현대 범용 OS는 **페이징**, 논리 경계 보호는 **페이지 권한•Guard Page** 적용.

#### 한줄 요약
- 외부 단편화와 권한 요구를 기준으로 페이징과 논리 경계를 결합함.
