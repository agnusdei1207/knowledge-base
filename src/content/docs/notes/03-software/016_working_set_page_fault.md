---
sidebar:
  order: 16
  label: "016. 워킹 셋•페이지 폴트 (Working Set•Page Fault)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 워킹 셋•페이지 폴트 (Working Set•Page Fault)
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 16
extra:
  question_no: "016"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출, 워킹 셋•페이지 폴트 제어"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Working Set**: 프로세스가 특정 윈도우 시간($\Delta$) 동안 참조한 페이지들의 집합으로, 프로그램 국부성(Locality)에 기반하여 동적으로 변동하는 최적 상주 메모리(Resident Set) 요구량.
- **Page Fault**: 프로세스가 가상 주소를 억세스할 때 해당 페이지의 Valid Bit = 0 이어서 물리 DRAM에 부재하여 하드웨어 인터럽트 및 디스크 I/O 적재가 수반되는 현상.
- **PFF (Page Fault Frequency)**: 상한선(Upper Limit)과 하한선(Lower Limit)을 설정하여, 런타임 Page Fault 주기에 따라 프로세스에 프레임을 동적으로 증감시키는 알고리즘.

</details>

- 정의/개념: 프로세스의 런타임 지역성(Locality)을 추적하여 물리 메모리 할당량을 동적으로 조율하고 Page Fault 발생을 제어하는 대표적 메커니즘인 **Working Set & Page Fault Frequency (PFF)**
- 배경/필요성: 고정(Static) 프레임 할당 정책의 비효율성을 극복하고 스레싱(Thrashing) 예방 및 시스템 전체 메모리 가용성 극대화 요구성

#### 한줄 요약

- 최근 참조와 폴트율에 따른 동적 프레임 할당이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Working Set Window ($\Delta$)**: 프로세스의 과거 페이지 참조 이력을 추적하여 Working Set을 산출하는 시간/참조 건수 기준 윈도우.
- **Locality of Reference (참조 국부성)**: 시간적(Temporal) 및 공간적(Spatial)으로 프로그램이 특정 메모리 구역을 집중 참조하는 성질.

</details>

- 참조 윈도우($\Delta$) 크기에 따른 **Working Set** 동적 가변성
- **Locality of Reference** 특성을 수용하여 프레임 적재 최적화
- **PFF** 상하한선 모니터링을 통한 사전 차단식 프레임 할당/회수

#### 한줄 요약

- 참조 창 크기에 따른 추정 누락•과대 산정 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Upper / Lower Bound (PFF 상하한선)**: PFF 알고리즘에서 Page Fault 간격(Inter-fault time)이 상한보다 짧으면 프레임 증설, 하한보다 길면 유휴 프레임 회수 판단 기준.

</details>

```text
              [프로세스]
                  |
          [참조•상주 상태]
                  |
         [워킹 셋 추적기]
                  |
        [페이지 폴트 처리기]
                  |
           [프레임 할당기]
```

선의 의미: 프로세스 참조 이력이 추적기를 통해 Working Set 및 PFF 처리기로 인가되어 프레임 할당기에 의해 동적 프레임이 할당/회수되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 참조 윈도우 ($\Delta$) | 과거 지정된 틱($\Delta$) 동안의 페이지 참조 비트(Reference Bit) 기록 |
| Working Set Tracker | $W(t, \Delta)$ 수식을 통해 프로세스별 현재 필요한 최소 물리 프레임 수 산출 |
| Page Fault Handler | Page Fault 발생 간격($t_i - t_{i-1}$)을 계측하여 PFF 알고리즘 트리거 |
| Dynamic Frame Allocator | **PFF Upper Limit** 초과 시 프레임 추가 증설, **Lower Limit** 미달 시 프레임 회수 |

#### 한줄 요약

- 워킹 셋 추정기, 페이지 폴트 처리기, 프레임 할당기의 제어 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Inter-fault Time**: 연속으로 발생한 두 Page Fault 간의 물리적 시간 간격($F = t_i - t_{i-1}$).

</details>

```text
╔════════════════════════════════╗
║ 반복: 관찰 구간마다           ║
║ 1. 참조 창 갱신               ║
║              │                 ║
║              ▼                 ║
║ 2. 워킹 셋•폴트율 산정        ║
║              │                 ║
║              ▼                 ║
║ 3. 상주 집합 상태 판정        ║
║   ├─ 미수용·상한 초과         ║
║   │        └─▶ 4. 프레임 증설 ║
║   ├─ 과잉·하한 미만           ║
║   │        └─▶ 5. 프레임 회수 ║
║   └─ 적정 ─────▶ 할당 유지    ║
╚════════════════╤═══════════════╝
                 ▼
          [다음 관찰 구간]
```

### 동작 원리

1. **참조 창 갱신**: $\Delta$ 윈도우 내 프로세스 페이지 참조 비트(Reference Bit) 지속 갱신.
2. **워킹 셋·폴트율 산정**: 현재 고유 집합 $W(t, \Delta)$ 크기 및 **Inter-fault Time** 산출.
3. **상주 집합 상태 판정**: $F < \text{Upper Bound}$ (Fault 잦음) vs $F > \text{Lower Bound}$ (Fault 드묾) 판정.
4. **프레임 증설**: $F < \text{Upper Bound}$ 시 프로세스에 물리 프레임 추가 수용 할당.
5. **프레임 회수**: $F > \text{Lower Bound}$ 시 윈도우 내 미참조 페이지 프레임 회수 및 타 프로세스 반납.

#### 한줄 요약

- 워킹 셋•폴트율 피드백 기반 프레임 증감이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Working Set Algorithm vs PFF Algorithm**: Working Set은 주기적 $\Delta$ 윈도우 계산(상시 오버헤드)인 반면, PFF는 Page Fault 발생 시에만 간격을 검사(낮은 평시 오버헤드)하는 차이점.

</details>

| 비교 항목 | Working Set 알고리즘 | Page Fault Frequency (PFF) 알고리즘 |
|:---|:---|:---|
| 프레임 재조정 시점 | 지속적인 주기적 $\Delta$ 윈도우 관찰 시점 | **Page Fault 발생 순간에만** 갱신 판단 |
| 오버헤드 크기 | 높음 (매 메모리 억세스/주기마다 참조 비트 스캔) | 낮음 (Page Fault 인터럽트 발생시에만 계산) |
| 핵심 파라미터 | Working Set Window ($\Delta$) 크기 | **Upper Bound** 및 **Lower Bound** 시간 간격 |
| 스레싱 예방성 | 매우 뛰어남 (선제적 메모리 보장) | 우수함 (사후 반응형 동적 할당) |

#### 한줄 요약

- 필요량 추정은 워킹 셋, 부족 감지는 폴트 빈도가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **LRU-K**: 최근 $K$번째 참조된 시점을 기준으로 가장 오래된 페이지를 교체하여 Working Set을 정밀 보정하는 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| $\Delta$ 윈도우 크기 튜닝 실패로 인한 과대/과소 프레임 할당 | 워크로드 패턴 기반 동적 $\Delta$ 가변 튜닝 | 메모리 파편화 및 낭비 차단 |
| Working Set 상시 추적으로 인한 CPU 알고리즘 연산 지연 | **PFF (Page Fault Frequency)** 사후 시그널 방식 전환 | 런타임 오버헤드 대폭 감소 |
| 순차 스캔(Sequential Scan) 작업 시 Working Set 팽창 | **LRU-K** 및 Clock-Pro 교체 알고리즘 혼용 | 스캔성 억세스의 워킹 셋 오염 방지 |

> 사례: Linux 커널 메모리 관리자(mm) 내 **Active/Inactive LRU List** 및 **psi(Page Stall Information)** 튜닝

#### 한줄 요약

- 참조 창•폴트 유형•서비스 수준 기반 할당을 조정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **동적 프레임 할당 기준(Dynamic Frame Allocation Criteria)**: 워킹 셋 윈도우 크기, Page Fault 발생 간격 및 시스템 메모리 압박 지수에 의거한 튜닝 체계.

</details>

- **동적 프레임 할당 기준**에 따라 가상 메모리 관리 시 **Working Set 추정**과 **PFF 저비용 알고리즘**을 상호 보완 적용

#### 한줄 요약

- 워킹 셋 미수용•주요 폴트 초과 시 자원을 재조정한다.
