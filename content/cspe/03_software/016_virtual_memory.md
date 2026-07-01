---
title: "가상 메모리·페이징·세그멘테이션 (Virtual Memory)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 16
---

# 📖 【암기용】 개념 완전 이해

> 목적: 가상 메모리를 처음 봐도 주소 공간 추상화와 메모리 보호 장치로 이해하게 만든다. 시험 답안 양식이 아니라, paging과 segmentation의 역할을 설명한다.

## 한눈에
- **개요**: 가상 메모리는 프로세스마다 독립된 주소 공간을 제공하고 필요한 부분만 물리 메모리에 올리는 메모리 관리 기법이다.
- **왜 필요한가**: 프로그램은 물리 메모리 크기와 배치 위치를 몰라도 실행되어야 한다. OS는 보호, 공유, 적재 지연, 단편화 제어를 동시에 처리해야 한다.
- **핵심 직관**: 각 프로세스에게 큰 개인 책상처럼 보이는 주소 공간을 주고, 실제 책상 칸은 OS가 page table로 매핑한다.

## 깊이 이해
- **배경·문제의식**: 물리 주소만 쓰면 프로세스가 서로의 메모리를 침범하고, 큰 프로그램은 RAM보다 작게 나눠 실행하기 어렵다. 가상 주소는 실행 파일, heap, stack을 논리적으로 분리한다.
- **작동 원리**: CPU가 가상 주소를 내면 MMU가 page table과 TLB를 사용해 물리 주소로 변환한다. 페이지가 없으면 page fault가 발생하고 OS가 디스크에서 적재한다.
- **비유**: 도서관 좌석 번호는 사용자에게 보이는 가상 주소이고, 실제 책이 꽂힌 서가 위치는 물리 주소다. 사서는 목록표(page table)로 둘을 연결한다.
- **구체 예시**: 48bit 가상 주소, 4KB page, 4단계 page table 구조에서 TLB hit이면 수 ns, major page fault이면 ms 단위 I/O가 발생한다.
- **흔한 오해·주의점**: 가상 메모리는 RAM을 무한히 늘리는 기술이 아니다. working set이 RAM을 넘으면 page fault와 swap I/O가 증가한다.

## 연결 개념
- Page Table — 가상 page와 물리 frame의 매핑표
- TLB — 주소 변환 결과를 캐싱하는 MMU 내부 캐시
- Demand Paging — 실제 접근 시점에 page를 적재하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 가상 메모리는 주소 변환, 보호, demand paging, 단편화 제어를 CPU·메모리·I/O trade-off로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가상 메모리는 프로세스별 가상 주소를 page table을 통해 물리 frame으로 매핑하는 주소 공간 추상화 기법이다.
> 2. **가치**: 보호 비트, demand paging, 공유 page로 격리와 메모리 사용률을 동시에 제공한다.
> 3. **판단 포인트**: TLB hit ratio, page fault rate, internal/external fragmentation, protection fault를 함께 관리해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 주소 변환 원리 확인 | VA, VPN, offset, page table, TLB, PA | 단순 swap 설명으로 축소하지 않음 |
| paging·segmentation 비교 확인 | 고정 크기 page, 논리 단위 segment | 내부·외부 단편화 차이 누락하지 않음 |
| 운영 지표 판단 확인 | TLB miss, page fault, working set | RAM 증설만 해법으로 제시하지 않음 |

> 요약: 이 문제는 가상 주소 변환 구조와 page fault 비용을 함께 설명하는 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

가상 메모리는 프로세스별 독립 주소 공간을 제공한다. OS와 MMU는 가상 주소를 물리 주소로 변환하고, page 단위 적재와 보호 비트로 격리와 공유를 제어한다. 메모리 보호, 큰 프로그램 실행, 단편화 완화가 핵심 필요성이다.

---

## Ⅱ. 구조 및 구성요소

```text
Process VA -> MMU -> TLB Lookup -> Page Table Walk -> Physical Frame
       / Protection Bits -> Access Check
       / Page Fault Handler -> Disk / Swap -> Frame Allocation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Virtual Address | 프로세스가 사용하는 논리 주소 | VPN + offset 구성 |
| Page Table | 가상 page와 물리 frame 매핑 | valid, dirty, permission bit 포함 |
| TLB | 주소 변환 결과 캐시 | hit ratio 95~99% 목표 |

> 요약: 가상 메모리는 MMU, TLB, page table, fault handler가 결합해 주소 변환과 보호를 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
CPU VA Generate -> TLB Lookup
  / Hit -> Permission Check -> Physical Access
  / Miss -> Page Table Walk -> TLB Fill
  / Invalid -> Page Fault -> Load Page -> Resume Instruction
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CPU가 가상 주소와 접근 권한 요청 생성 | load/store/fetch 구분 |
| 2 | TLB에서 VPN 매핑 검색 | TLB hit ratio |
| 3 | miss 시 page table walk 수행 | page walk cycles |
| 4 | invalid page면 fault 처리 후 재시작 | major/minor fault/sec |

> 요약: 주소 변환은 TLB hit이면 즉시 진행되고, miss나 invalid page는 page table walk와 fault handler 비용을 만든다.

---

## Ⅳ. 특징

| 구분 | Paging | Segmentation | 수치·판단 기준 |
|:---|:---|:---|:---|
| 관리 단위 | 고정 크기 page | 코드·데이터·스택 논리 segment | 4KB, 2MB huge page |
| 단편화 | internal fragmentation | external fragmentation | page 평균 낭비 <= 2KB |
| 보호 | page별 R/W/X bit | segment별 limit, permission | NX bit, user/supervisor bit |
| 비용 | page table, TLB miss | segment table, compaction | TLB hit 95% 이상 |

> 요약: 현대 OS는 paging을 기본으로 사용하고, segment 개념은 보호·주소 공간 배치 논리로 제한적으로 활용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 물리 메모리 직접 주소 | 프로세스별 가상 주소 | 프로세스 격리와 보호 필요 시 |
| 비용/성능 | 주소 변환 없음 | TLB miss, page fault 비용 | TLB hit 95% 이상 유지 |
| 운영/위험 | 메모리 침범 가능 | page table 메모리 오버헤드 | huge page, shared page 적용 |

> 요약: 가상 메모리는 변환 비용을 지불하고 보호, 공유, demand paging을 얻는 구조다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TLB Miss 증가 | working set page 수 과다 | huge page, locality 개선 | TLB miss rate |
| Page Fault 폭증 | resident set 부족 | memory limit 조정, prepaging | major fault/sec |
| 권한 위반 | permission bit 설정 오류 | NX, W^X, ASLR 적용 | protection fault, audit log |

> 요약: 주요 리스크는 TLB miss, page fault, 권한 오류이며 MMU 지표와 fault 로그로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변환 비용 | TLB hit ratio 95% 이상 | perf stat, hardware counter |
| Fault 비용 | major fault/sec 기준선 이하 | vmstat, sar |
| 보호 | invalid access 0건 | crash log, sanitizer, audit |

> 요약: 가상 메모리 운영은 TLB hit, page fault, protection fault 세 지표로 성공 여부를 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. DB·JVM처럼 큰 heap을 쓰는 workload는 2MB huge page를 적용해 TLB miss와 page walk cycles를 줄임.
2. 컨테이너는 cgroup memory.max와 OOM 정책을 설정해 overcommit이 page fault storm으로 번지지 않게 함.
3. 실행 보호는 NX bit, W^X, ASLR, guard page를 적용해 code injection과 stack overflow 영향을 제한함.

**결론 (2줄):**
- 기술사 판단: 가상 메모리는 보호·공유·demand paging 이점이 TLB miss와 fault 비용보다 클 때 시스템 기본 구조로 채택됨.
- 향후 방향: confidential computing과 IOMMU까지 포함해 CPU, DMA, VM 단위 주소 변환 격리가 확대됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "가상 메모리를 설명하시오" | TLB, page table, fault 처리 흐름 | paging·segmentation 비교 |
| 요구사항 명시형 | "비교하시오", "운영 방안을 제시하시오" | TLB miss·page fault 진단 절차 | huge page, cgroup, 보호 비트 선택 기준 |

> 요약: 운영형 문제는 주소 변환 원리보다 TLB hit, fault rate, 보호 정책 지표를 중심으로 전개한다.
