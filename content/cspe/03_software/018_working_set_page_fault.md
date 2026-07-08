---
title: "워킹 셋·페이지 폴트 (Working Set Page Fault)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 18
extra:
  question_no: "018"
  exam_status: "기출"
  exam_history: "131회"
---

## 미리 알고가기

- working set은 일정 시간 창에서 실제로 참조되는 페이지 집합임
- page fault는 필요한 페이지가 메모리에 없을 때 발생하는 예외임
- working set보다 적은 프레임만 주면 fault가 급증하기 쉬움

## Ⅰ. 개요

- **정의/개념**: working set은 프로세스가 현재 활발히 사용하는 페이지 묶음을 뜻하고, page fault는 이 집합 밖의 페이지가 필요하거나 필요한 페이지가 아직 메모리에 없을 때 발생하는 메모리 접근 실패 사건임
- **배경/필요성**: 가상 메모리 환경에서는 프로세스마다 필요한 실제 메모리 규모가 시간에 따라 달라지므로, working set을 기준으로 메모리를 배분해야 스래싱을 줄이고 처리량을 유지할 수 있음

## Ⅱ. 특징

- working set은 locality를 정량적으로 표현하는 운영 지표임
- page fault는 메모리 부족과 참조 패턴 변화의 직접 신호가 됨
- 과도한 page fault는 CPU 활용률보다 디스크 대기 시간을 더 크게 만듦
- working set 변화는 프로세스 단계 전환과 workload 특성 변화를 반영함

## Ⅲ. 종류 및 비교

| 판단 기준 | Working Set 관점 | 단순 Page Fault 관점 |
|:---|:---|:---|
| 초점 | 필요한 메모리 규모 예측 | 발생한 fault 수 관찰 |
| 장점 | 사전적 메모리 배분 가능 | 구현과 측정이 단순 |
| 한계 | 시간 창 설정이 중요 | 원인 분석 없이 결과만 보게 됨 |
| 활용 | resident set 제어 | 경보와 병목 탐지 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Reference Window | 최근 참조를 어느 기간까지 볼지 정해 working set 크기 추정의 기준이 됨 |
| Resident Set | 실제 메모리에 확보된 프레임 수로 working set을 담을 수 있는지 결정함 |
| Page Fault Monitor | fault 빈도를 수집해 메모리 압박과 locality 붕괴 신호를 제공함 |
| Reclaim Policy | working set보다 초과된 페이지를 회수하거나 부족한 프레임을 재배분해 균형을 맞춤 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 참조 이력 수집  | --> | working set 추정 | --> | 프레임 배분 조정 | --> | fault 감시      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **참조 이력 수집**: 최근 페이지 참조를 시간 창 기준으로 기록함
2. **working set 추정**: 현재 필요한 페이지 집합과 크기를 계산함
3. **프레임 배분 조정**: 부족한 프로세스에는 프레임을 늘리고 과다 점유는 회수함
4. **fault 감시**: page fault 추세로 메모리 압박과 스래싱 징후를 확인함

## Ⅵ. 문제점 및 해결 방안

1. 문제: working set 추정 창이 너무 짧거나 길면 실제 locality를 잘못 읽어 메모리 배분이 흔들릴 수 있음
   - 해결방안: workload별 window를 조정하고 working set estimation error와 page fault trend로 검증함
2. 문제: 프로세스 수가 많아 총 working set 합이 물리 메모리를 넘으면 스래싱이 빠르게 발생할 수 있음
   - 해결방안: admission control과 swap pressure 제어를 적용하고 swap I/O rate와 throughput stability로 검증함
3. 문제: page fault 수치만 보고 원인을 구분하지 않으면 파일 캐시 부족과 진짜 메모리 부족을 혼동할 수 있음
   - 해결방안: fault 유형과 reclaim 통계를 함께 분석하고 major fault rate와 reclaim efficiency로 검증함

## Ⅶ. 적용 사례

- 데이터베이스 서버에서는 working set 변화를 기준으로 메모리를 조정하고 확인 지표는 major fault rate와 throughput stability임
- 배치 작업 호스트에서는 admission control을 적용해 스래싱을 억제하고 확인 지표는 swap I/O rate와 CPU utilization stability임
- 커널 메모리 분석에서는 reclaim 통계를 함께 본 뒤 확인 지표는 working set estimation error와 reclaim efficiency임

## Ⅷ. 결론

working set과 page fault는 메모리 관리의 원인과 결과를 잇는 축이므로, 운영 판단은 fault 수치만이 아니라 현재 필요한 메모리 규모를 함께 봐야 정확함.
