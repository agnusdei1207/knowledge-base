---
sidebar:
  order: 14
  label: "014. 프로세스 스레싱 (Process Thrashing)"
  badge:
    text: "기출 • 70%"
    variant: note
title: 프로세스 스레싱 (Process Thrashing)
date: "2026-08-13T13:20:00+09:00"
tags: [notes-software]
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 70
  priority_note: "129•131회 반복, 스레싱•워킹 셋 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Thrashing (스레싱)**: 프로세스 수행에 필요한 최소한의 페이지 프레임(Page Frame)을 확보하지 못해, 실제 유용한 연산 시간보다 페이지 교체(Page Fault / Swap I/O)에 대부분의 시간이 소모되는 가상 메모리 붕괴 현상.
- **Working Set (워킹 셋)**: 프로세스가 특정 윈도우 시간($\Delta$) 동안 빈번하게 참조하는 페이지들의 집합.

- **메이저 페이지 폴트(Major Page Fault)**: 참조하려는 가상 페이지가 물리 메모리에 없어 디스크(스왑 영역)로부터 읽어오기 위해 극심한 I/O 지연을 유발하는 페이지 부재.
- **스왑 대기(Swap Wait)**: 스래싱 발생 시 과도한 페이지 교체 I/O로 인해 프로세스들이 CPU 연산 대신 디스크 I/O 큐에서 무한 대기하는 현상.
</details>

- 정의/개념: 가용 물리 메모리 부족으로 인해 지속적인 Page Fault 및 Swap In/Out 입출력 연산이 폭증하여 CPU 이용률이 급격히 추락하는 **프로세스 스레싱**
- 배경/필요성: 다중프로그래밍 과도화로 **프레임 할당량**이 부족하여 유효 연산 처리 불가

#### 한줄 요약

- **가용 프레임** 부족으로 페이지 교체가 폭증하여 처리량이 급감하는 붕괴 상태

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Degree of Multiprogramming (DOM)**: 주기억장치 상에 동시에 상주하여 실행 대기 중인 프로세스의 개수.
- **Page Fault Frequency (PFF)**: 상한값(Upper Bound)과 하한값(Lower Bound)을 설정하여 프로세스에 할당되는 프레임 수량을 동적으로 제어하는 스레싱 방지 알고리즘.

</details>

- DOM 증가 시 특정 임계점 이후 CPU 이용률(Utilization) 및 스루풋 급감
- 빈번한 **Major Page Fault** 발생 및 디스크 I/O 대기열(Disk Wait Queue) 폭증
- **Working Set Model** 및 **PFF(Page Fault Frequency)** 알고리즘 기반 프레임 재배치 대책 수립

#### 한줄 요약

- 페이지 폴트와 **Swap 대기** 연쇄 발생으로 **CPU 이용률**이 급감하는 현상

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Working Set Window ($\Delta$)**: 프로세스의 과거 페이지 참조 이력을 추적하여 워킹 셋을 계산하는 기준 시간 범위.
- **Resident Set**: 프로세스에 실제로 물리 메모리(DRAM) 상에 할당되어 존재하는 페이지들의 집합.

</details>

```text
┌─────────────────────────────────────────┐
│            상주 집합 관리자             │
├────────────────────┬────────────────────┤
│   워킹 셋 추적기   │ 페이지 폴트 감시기 │
└────────────────────┴────────────────────┘
┌─────────────────────────────────────────┐
│               부하 제어기               │
└─────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 워킹 셋 추적기 | **Working Set Window ($\Delta$)** 내 페이지 참조 수치 기반 최적 **Working Set** 수량 추정 |
| 상주 집합 관리자 | 물리 메모리 내 **Resident Set** 할당, 페이지 대체(LRU/Clock) 및 Page Frame 관리 |
| 페이지 폴트 감시기 | **PFF(Page Fault Frequency)** 상한/하한을 계측하여 폴트 주기를 모니터링 |
| 부하 제어기 (Load Controller) | Thrashing 포획 시 DOM(Degree of Multiprogramming) 강제 축소 및 프로세스 Swapping |

#### 한줄 요약

- 워킹 셋 추적기와 **페이지 폴트 감시기**를 기반으로 프레임과 작업 수 조정

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Thrashing Cascade Loop**: DOM 증가 $\to$ 프로세스 당 Frame 부족 $\to$ Page Fault 폭증 $\to$ Disk I/O 병목 $\to$ CPU Idle 발생 $\to$ OS가 DOM 추가 증대 오판 $\to$ Thrashing 악순환.

</details>

```text
┌──────────────────────────────┐
│ 워킹 셋 > 할당 프레임       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 재참조 폴트 증가         │◀──────────────┐
│ 2. 교체 I/O 증가            │               │
│ 3. CPU 이용률 저하          │               │
└───────┬──────────────────────┘               │
        ├─ 스레싱 판정 ─▶ [작업 수 축소·프레임 재배분]
        │ 오판                                  │
        ▼                                       │
┌──────────────────────────────┐               │
│ 4. 다중프로그래밍 증가      │               │
│ 5. 프로세스별 프레임 감소   │───────────────┘
└──────────────────────────────┘
```

### 동작 원리

1. 재참조 폴트 증가: 가용 프레임 부족으로 인한 **Working Set** 이탈 및 Page Fault 폭증
2. 교체 I/O 증가: Disk Swap In/Out 대기열 폭증 및 I/O 병목 유발
3. CPU 이용률 저하: 프로세스가 I/O 대기 상태에 빠져 **연산량** 감소
4. 다중프로그래밍 증가: 커널이 유휴 상태를 부하 부족으로 오판해 **작업 수 증대**
5. 프로세스별 프레임 감소: 다중프로그래밍 증대로 할당 프레임이 축소되어 폴트 악화

#### 한줄 요약

- 할당 프레임 축소와 **폴트 악화**가 반복되는 Thrashing 순환 구조

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Demand Paging**: 필요한 시점에만 페이지를 물리 메모리로 로딩하는 기본 가상 메모리 기법.

</details>

| 비교 항목 | 정상 Demand Paging 상태 | Thrashing 붕괴 상태 |
|:---|:---|:---|
| Page Fault 발생률 | 워킹 셋 적재 후 안정 | 재참조 폴트가 지속적으로 증가 |
| CPU 이용률 | 유용한 연산 비중 유지 | 교체 I/O 대기로 연산 비중 감소 |
| 주요 시간 소비 | CPU 명령어 연산 시간 | Disk Swap In/Out I/O 대기시간 |
| 해결책 | LRU/Page Replacement 정책 유지 | **DOM 축소 (Process Swapped Out)** & Working Set 확보 |

#### 한줄 요약

- 페이지 폴트율 지표를 모니터링하여 **요구 페이징 정상 상태**와 Thrashing 구별

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cgroups Memory Limit**: Linux cgroups를 통해 특정 프로세스/컨테이너 그룹의 상주 메모리 및 Swap 사용량을 물리 제약하는 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DOM 과도화로 인한 전체 가상 메모리 스레싱 | **Working Set Model** 기반 프레임 확보와 **DOM 축소** | 교체 I/O 감소와 처리량 회복 |
| 특정 프로세스의 메모리 폭증에 따른 타 프로세스 침범 | **PFF (Page Fault Frequency)** 기준 동적 프레임 할당 | 프레임 불균형 해소 |
| Docker/K8s 컨테이너의 무제한 메모리 점유 | **Linux cgroups Memory Limit** 및 OOM Killer 제어 | 노드 전체 스레싱 방지 |

> 사례: Kubernetes Pod **Memory Limit/Request** 설정을 통한 노드 레벨 **Thrashing** 방지

#### 한줄 요약

- **PFF 수용 제어** 및 컨테이너 메모리 **cgroups Limit** 지정을 통한 방지책 구성

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **스레싱 방지 관리 기준(Thrashing Prevention Criteria)**: PFF 한계치 설정, DOM 조정 및 cgroups 용량 제한에 근거한 수립 체계.

</details>

- 단일 프로세스는 **PFF** 기반 프레임 제어, 컨테이너 환경은 **cgroups** 메모리 격리 적용

#### 한줄 요약

- **PFF** 및 **워킹 셋** 기반으로 작업 수를 제어하여 프레임 재할당 수행
