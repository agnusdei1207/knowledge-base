---
title: "[핵심] 가상메모리·페이지교체 종합 (Virtual Memory & Page Replacement)"
date: "2026-06-30"
weight: 80
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 보조기억장치를 주기억장치의 연장으로 사용하여 물리메모리 크기를 초과하는 프로세스를 실행하는 기법으로, 요구 페이징(Demand Paging)으로 필요한 페이지만 적재한다.

## Ⅱ. 구성요소 / 원리
- 요구 페이징: 참조 시점에 페이지를 적재, 미적재 참조 시 페이지 부재(Page Fault) 발생
- 페이지 교체(Page Replacement): 빈 프레임 부족 시 희생 페이지를 선정해 교체
- LRU(Least Recently Used, 최근 최소사용): 가장 오래 미참조 페이지 교체, 시간지역성 활용
- Clock(2차 기회): 참조비트(Reference Bit)로 LRU를 근사, 하드웨어 부담 경감
- 스래싱(Thrashing): 과도한 페이지 부재로 처리율 급락 → 워킹셋·PFF로 조절

## Ⅲ. 흐름도 / 구조
```text
CPU 논리주소 참조 → 페이지테이블 조회
       │
   적재됨? ──Yes→ 프레임 접근
       └──No(Page Fault)→ 빈 프레임? ──Yes→ 디스크에서 적재
                              └──No→ 교체알고리즘(LRU/Clock)으로 희생선정→적재
   다중프로그래밍↑ & 부재율↑ → Thrashing → 워킹셋(Working Set)/PFF 조절
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | FIFO=단순 / OPT(Optimal)=이론최적 / LRU=시간지역성 / Clock=LRU 근사·저비용 |
| 장점 | OPT=부재율 최소(기준), LRU=Belady 모순 없음, Clock=참조비트로 효율적 구현 |
| 한계 | FIFO=Belady's Anomaly(프레임↑인데 부재↑), LRU=구현비용↑, OPT=미래참조 필요로 비현실 |

## Ⅴ. 기술사적 적용
- LRU 근사 구현은 Clock 알고리즘으로 참조비트를 순회 검사하여 하드웨어 비용 절감
- 스래싱은 워킹셋(Working Set) 모델로 지역성 집합을 보장하거나 페이지부재빈도(PFF)로 프레임 수 동적 조절
- 다중프로그래밍 정도(Degree of Multiprogramming)와 CPU 이용률의 임계점 관리가 핵심
