---
title: "워킹 셋·페이지 폴트 (Working Set Page Fault)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 18
---

# 📖 【암기용】 개념 완전 이해

> 목적: 워킹 셋과 페이지 폴트를 처음 봐도 지역성과 메모리 수요를 측정하는 개념으로 이해하게 만든다. 시험 답안 양식이 아니라, thrashing 제어 원리를 설명한다.

## 한눈에
- **개요**: 워킹 셋은 최근 일정 시간 동안 프로세스가 실제로 참조한 page 집합이고, 페이지 폴트는 필요한 page가 메모리에 없을 때 발생한다.
- **왜 필요한가**: 프로세스가 원활히 실행되려면 현재 지역성에 필요한 page들이 resident set에 있어야 한다. 부족하면 page fault가 늘고 스레싱으로 이어진다.
- **핵심 직관**: 지금 공부하는 과목의 책과 노트 묶음이 working set이고, 책상에 없어서 서가를 다녀오는 일이 page fault다.

## 깊이 이해
- **배경·문제의식**: 프로그램은 전체 주소 공간을 균일하게 쓰지 않고 반복문, 함수, 데이터 블록 주변을 집중적으로 참조한다. 이를 locality라고 한다.
- **작동 원리**: OS는 최근 참조 window delta 안의 page 수를 WSS(Working Set Size)로 추정한다. WSS가 resident set보다 크면 fault rate가 증가하므로 frame을 늘리거나 프로세스를 줄인다.
- **비유**: 요리 중 필요한 도구만 조리대에 올려두면 이동이 적다. 필요한 도구보다 조리대가 좁으면 매번 창고를 왕복한다.
- **구체 예시**: delta 10,000 reference에서 프로세스 A의 WSS가 500 pages이고 resident set이 300 pages이면 최소 200 pages 부족해 fault frequency가 상승한다.
- **흔한 오해·주의점**: page fault가 모두 나쁜 것은 아니다. 최초 접근 minor fault나 demand paging fault는 정상 동작이며, major fault가 지속 증가할 때 병목으로 본다.

## 연결 개념
- Locality — temporal/spatial 참조 집중성
- Resident Set — 실제 물리 메모리에 올라온 page 집합
- PFF(Page Fault Frequency) — fault 비율로 frame을 조절하는 정책

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: working set과 page fault는 locality, resident set, PFF, thrashing control의 연결 구조로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Working Set은 최근 참조 window 내 활성 page 집합이고, Page Fault는 필요한 page가 resident set에 없을 때 발생하는 예외다.
> 2. **가치**: WSS와 PFF는 스레싱을 사전에 감지하고 frame 배분·프로세스 admission을 조정하는 기준이다.
> 3. **판단 포인트**: minor/major fault 구분, resident set 대비 WSS, PFF 상·하한을 함께 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| locality 기반 메모리 관리 이해 | WSS, resident set, delta window | working set을 전체 주소 공간으로 쓰지 않음 |
| page fault 영향 판단 | minor vs major, page-in 비용 | fault 발생 자체를 모두 오류로 보지 않음 |
| 스레싱 제어 방안 확인 | PFF, prepaging, admission control | replacement 알고리즘만 나열하지 않음 |

> 요약: 이 문제는 page fault를 WSS 부족 신호로 해석하고 frame 배분 정책으로 연결하는지 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Working Set은 최근 참조 page 집합이다.
- 배경: 접근 page가 물리 메모리에 없으면 page fault가 발생하고, WSS 합이 RAM 예산을 넘으면 fault 처리와 swap I/O가 실행 시간을 잠식한다.
- 필요성: OS는 WSS 합 <= RAM 80%, Page Fault Frequency, major fault/sec 기준으로 resident set과 admission을 조절한다.

---

## Ⅱ. 구조 및 구성요소

```text
Reference Stream -> Locality Window Delta -> Working Set Estimator
       / Resident Set Manager -> Frame Allocation
       / Page Fault Monitor -> PFF Controller -> Thrashing Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Working Set Window | 최근 참조 범위 설정 | delta reference 또는 시간 기준 |
| Resident Set | 실제 메모리에 적재된 page | WSS보다 작으면 fault 증가 |
| PFF Controller | fault 빈도로 frame 조절 | 상한 초과 시 frame 증가 또는 suspend |

> 요약: working set 구조는 참조 흐름을 관측해 필요한 page 수를 추정하고 resident set을 조절한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Memory Reference -> Check Resident Set
  / Hit -> Continue Execution
  / Miss -> Page Fault -> Page In -> Update WSS/PFF
  -> Adjust Frames / Admit or Suspend Process
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 참조 page가 resident set에 있는지 확인 | hit ratio |
| 2 | miss 시 minor 또는 major fault 처리 | fault type count |
| 3 | window 내 참조 page로 WSS 갱신 | WSS trend |
| 4 | PFF 기준으로 frame 증감 또는 suspend | PFF upper/lower bound |

> 요약: fault는 단순 예외가 아니라 working set 변화와 frame 부족을 알려주는 제어 신호다.

---

## Ⅳ. 특징

| 구분 | Working Set | Page Fault | 수치·판단 기준 |
|:---|:---|:---|:---|
| 의미 | 현재 필요한 page 집합 | page 부재 시 예외 | WSS pages, fault/sec |
| 목적 | frame 수요 예측 | demand paging 실행 | PFF 상한·하한 |
| 위험 | WSS 합 > RAM | major fault 지속 증가 | iowait 10% 초과 |
| 조치 | admission control | page-in, prepaging | RAM 80% 이내 WSS |

> 요약: working set은 메모리 수요 지표이고 page fault는 그 수요와 resident set 차이를 드러내는 관측 지표다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 고정 frame 배분 | WSS/PFF 기반 동적 배분 | workload locality 변화가 클 때 |
| 비용/성능 | 관측 비용 낮음 | reference bit sampling 비용 | fault 감소가 sampling 비용보다 클 때 |
| 운영/위험 | 과소 배분 시 thrashing | 과대 배분 시 메모리 낭비 | WSS 합 <= RAM 80% |

> 요약: 동적 배분은 page fault 감소와 메모리 낭비 사이에서 PFF 상·하한으로 조정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Window 오류 | delta가 너무 작거나 큼 | workload별 delta 튜닝 | WSS 변동성 |
| Major Fault 증가 | resident set 부족 | frame 추가, prepaging | major fault/sec |
| Thrashing | WSS 합이 RAM 초과 | process suspend, DOP 축소 | CPU utilization, iowait |

> 요약: working set 제어는 window 설정, major fault 관측, DOP 조정이 함께 수행되어야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| WSS 적합 | WSS 합 <= RAM 80% | reference sampling, RSS 분석 |
| Fault 제어 | PFF 상한 이하 유지 | vmstat, perf page-faults |
| 실행 영향 | CPU utilization 70% 이상 | mpstat, PSI memory stall |

> 요약: 운영 성공은 WSS 적합성, PFF 상한 준수, CPU utilization 회복으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 서비스별 RSS, major fault/sec, PSI memory stall을 수집해 WSS 추정값과 SLO 영향을 함께 본다.
2. PFF가 상한을 넘으면 cgroup memory.high 조정, replica 축소, 배치 작업 suspend로 resident set 부족을 해소함.
3. 시작 직후 fault 폭증이 있는 workload는 prepaging, warmup traffic, cache priming으로 초기 major fault를 분산함.

**결론 (2줄):**
- 기술사 판단: WSS가 RAM 예산 내이면 page fault는 정상 비용, WSS 초과와 major fault 지속이면 스레싱 대응 대상으로 판단함.
- 향후 방향: PSI와 eBPF 기반 memory telemetry로 page fault를 SLO 위반 전 조기 감지하는 운영으로 전환됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "워킹 셋과 페이지 폴트를 설명하시오" | resident set hit/miss와 fault 처리 흐름 | WSS, PFF, thrashing 관계 |
| 요구사항 명시형 | "스레싱 방안을 제시하시오", "비교하시오" | PFF 기반 frame 조절 절차 | window 튜닝, prepaging, DOP 선택 기준 |

> 요약: 방안형은 working set 추정값을 resident set 조정과 admission control로 연결해야 한다.
