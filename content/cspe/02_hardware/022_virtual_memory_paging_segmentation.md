---
title: "가상 메모리 - 페이징·세그멘테이션 (Virtual Memory Paging Segmentation)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 22
---

## 미리 알고가기

- 가상 주소: 프로세스가 보는 논리적 주소로, MMU가 물리 주소로 변환함
- Page: 고정 크기로 나눈 가상 메모리 블록임
- Segment: code, data, stack처럼 의미 단위로 나눈 가변 크기 영역임
- Page fault: 필요한 page가 메모리에 없거나 권한 위반이 있을 때 발생하는 예외임

## Ⅰ. 개요

- **정의**: 가상 메모리는 프로세스가 연속된 큰 주소 공간을 가진 것처럼 보이게 하고 MMU가 이를 물리 메모리와 보조저장장치에 매핑하는 메모리 관리 기법임. 페이징과 세그멘테이션은 각각 고정 크기 page와 의미 단위 segment를 기준으로 주소 변환, 보호, 공간 활용을 판단하는 방식임.
- **배경/필요성**: 여러 프로세스가 동시에 실행되면 주소 충돌, 메모리 부족, 보호 위반을 막아야 함. 가상 메모리는 프로세스 격리, relocation, demand loading, swap을 통해 물리 메모리보다 큰 실행 환경을 제공함.
- **비유**: 사용자는 큰 개인 사무실을 쓰는 것처럼 보지만, 관리자는 실제 책상과 창고 공간을 쪽지 단위로 배치해 운영하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상 주소 변환과 paging/segmentation 비교 | MMU, page table, segment table, protection, page fault | 가상 메모리를 swap과 동일시 |

> 요약: 가상 메모리는 주소 변환과 보호를 통해 프로세스별 독립 주소 공간을 제공하는 운영체제·하드웨어 협력 구조임.

## Ⅱ. 특징/비교

| 판단 기준 | 페이징 | 세그멘테이션 |
|:---|:---|:---|
| 분할 단위 | 고정 크기 page와 frame으로 나눔 | code, data, stack 같은 논리 단위 segment로 나눔 |
| 단편화 | 내부 단편화가 발생할 수 있으나 외부 단편화가 작음 | 외부 단편화가 발생할 수 있으나 의미 단위 보호가 쉬움 |
| 주소 변환 | page number와 offset을 page table로 변환함 | segment number, base, limit로 주소 범위를 검사함 |
| 적용 기준 | 현대 범용 OS의 기본 메모리 관리 방식 | 보호·공유·논리 구조 설명이나 일부 아키텍처에서 활용 |

> 요약: 페이징은 관리 단순성과 공간 활용, 세그멘테이션은 의미 단위 보호와 공유에 강점이 있음.

## Ⅲ. 구성요소

```text
Virtual Address
+-------------+------------+
| Page/Seg No | Offset     |
+------+------+------------+
       |
       v
+-------------+       +-------------+       +-------------+
| MMU/TLB     | ----> | Table Entry | ----> | Frame/Base  |
+-------------+       +-------------+       +------+------+
                                                   |
                                                   v
                                           Physical Address
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| MMU | 가상 주소를 물리 주소로 변환하고 권한을 검사하는 하드웨어임 | 주소 변환 창구 |
| Page table | VPN별 PFN, 권한, valid, dirty, accessed bit를 저장함 | 쪽지 배치표 |
| Segment table | segment base, limit, protection 정보를 저장함 | 구역 사용대장 |
| TLB | 최근 주소 변환 결과를 캐시해 변환 지연을 줄임 | 빠른 주소록 |
| Swap/storage | 메모리에 없는 page를 임시 보관하는 보조저장장치 영역임 | 외부 창고 |

> 요약: 가상 메모리는 MMU, 변환 테이블, TLB, 보조저장장치가 함께 주소 공간을 물리 자원에 매핑함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| VA       | --> | Translate| --> | Check    | --> | Access   |
+----------+     +----------+     +----------+     +----------+
 process addr     TLB/table        valid/perm       memory or fault
```

1. **가상 주소 생성** - CPU가 명령어 fetch, load/store를 위해 프로세스 가상 주소를 생성함
2. **주소 변환** - TLB 또는 page/segment table을 통해 물리 frame 또는 base 주소를 찾음
3. **보호 검사** - valid, read/write/execute, user/kernel 권한과 segment limit를 검사함
4. **접근·예외 처리** - 정상 접근은 cache/memory로 진행하고 부재 또는 위반 시 page fault를 처리함

> 요약: 가상 메모리는 주소 변환과 보호 검사를 거쳐 물리 메모리에 접근하거나 예외를 발생시킴.

## Ⅴ. 문제점

- **P1 변환 오버헤드**: TLB miss와 page table walk가 잦으면 메모리 접근 지연이 크게 증가함
- **P2 page fault·thrashing**: working set이 물리 메모리보다 크면 page fault가 반복되어 실행보다 swap I/O가 많아짐
- **P3 단편화와 보호 설정 오류**: page 내부 단편화, segment 외부 단편화, 잘못된 권한 bit가 공간 낭비나 보안 취약점으로 이어짐

> 요약: 가상 메모리 문제는 변환 지연, 물리 메모리 부족, 보호·단편화 관리 실패에서 발생함.

## Ⅵ. 개선방안

- **P1 대응**: TLB 확장, huge page, multi-level page table 최적화, page walk cache를 적용함 (확인: TLB miss, walk cycle)
- **P2 대응**: working set 모니터링, 적절한 page replacement, memory cgroup, swap I/O 상한을 운영함 (확인: major fault, swap-in/out)
- **P3 대응**: ASLR, NX bit, W^X, guard page, compaction과 page size 정책을 적용함 (확인: 권한 위반 테스트, fragmentation)

> 요약: 가상 메모리 개선은 변환 캐시, working set 관리, 권한 정책을 함께 조정해야 함.

## Ⅶ. 전망

- **발전 방향**: 대용량 메모리, 가상화, 컨테이너, CXL memory 확산으로 2차 주소 변환과 메모리 tiering까지 포함한 가상 메모리 관리가 중요해질 전망임
- **기술사적 판단**: 성능은 TLB와 page fault 지표로, 안정성은 보호 bit와 격리 정책으로, 비용은 물리 메모리와 swap I/O로 판단해야 함
- **기술사 제언**: 답안에서는 paging과 segmentation을 비교한 뒤 현대 OS는 paging 중심으로 보호와 demand paging을 구현한다는 흐름으로 정리해야 함
