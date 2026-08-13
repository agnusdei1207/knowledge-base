---
sidebar:
  order: 16
  label: "016. 워킹 셋•페이지 폴트 (Working Set•Page Fault)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 워킹 셋•페이지 폴트 (Working Set•Page Fault)
date: "2026-08-13T13:26:00+09:00"
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
- **Page Fault**: 주소 변환 중 페이지 부재나 권한 위반을 발견해 발생하는 동기 예외.
- **PFF (Page Fault Frequency)**: 상한선(Upper Limit)과 하한선(Lower Limit)을 설정하여, 런타임 Page Fault 주기에 따라 프로세스에 프레임을 동적으로 증감시키는 알고리즘.

</details>

- 정의/개념: 프로세스의 런타임 지역성(Locality)을 추적하여 물리 메모리 할당량을 동적으로 조율하고 Page Fault 발생을 제어하는 대표적 메커니즘인 **Working Set & Page Fault Frequency (PFF)**
- 배경/필요성: 고정 프레임 할당은 지역성 변화 시 **과소•과다 할당** 유발

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

- **Upper / Lower Bound (PFF 상하한선)**: 페이지 폴트 빈도가 상한을 넘으면 증설하고 하한보다 낮으면 회수하는 기준.

</details>

```text
[동적 프레임 할당]
 ├─ 참조 윈도우
 ├─ Working Set Tracker
 ├─ Page Fault Handler
 └─ Dynamic Frame Allocator
```

선의 의미: 프로세스 참조 이력이 추적기를 통해 Working Set 및 PFF 처리기로 인가되어 프레임 할당기에 의해 동적 프레임이 할당/회수되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 참조 윈도우 ($\Delta$) | 과거 지정된 틱($\Delta$) 동안의 페이지 참조 비트(Reference Bit) 기록 |
| Working Set Tracker | $W(t, \Delta)$ 수식을 통해 프로세스별 현재 필요한 최소 물리 프레임 수 산출 |
| Page Fault Handler | 관찰 구간의 페이지 폴트 빈도를 계측해 PFF 트리거 |
| Dynamic Frame Allocator | **PFF 상한** 초과 시 증설하고 하한 미만이면 회수 |

#### 한줄 요약

- 워킹 셋 추정기, 페이지 폴트 처리기, 프레임 할당기의 제어 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Page Fault Frequency**: 관찰 구간의 페이지 폴트 발생 횟수 또는 비율.

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
2. **워킹 셋·폴트율 산정**: 고유 집합 크기와 **페이지 폴트 빈도** 산출
3. **상주 집합 상태 판정**: 폴트 빈도를 상한•하한과 비교
4. **프레임 증설**: 폴트 빈도가 상한을 넘으면 프레임 추가
5. **프레임 회수**: 폴트 빈도가 하한보다 낮으면 미참조 프레임 회수

#### 한줄 요약

- 워킹 셋•폴트율 피드백 기반 프레임 증감이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Working Set Algorithm vs PFF Algorithm**: Working Set은 주기적 $\Delta$ 윈도우 계산(상시 오버헤드)인 반면, PFF는 Page Fault 발생 시에만 간격을 검사(낮은 평시 오버헤드)하는 차이점.

</details>

| 비교 항목 | Working Set 알고리즘 | Page Fault Frequency (PFF) 알고리즘 |
|:---|:---|:---|
| 프레임 재조정 시점 | 지속적인 주기적 $\Delta$ 윈도우 관찰 시점 | **Page Fault 발생 순간에만** 갱신 판단 |
| 오버헤드 크기 | 참조 비트의 주기적 추적 비용 | 폴트 발생 시 빈도 갱신 비용 |
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
