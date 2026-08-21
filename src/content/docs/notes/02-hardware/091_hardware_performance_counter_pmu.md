---
sidebar:
  order: 91
  label: "091. 하드웨어 성능 카운터•PMU"
  badge:
    text: "미출 · 50%"
    variant: note
title: "하드웨어 성능 카운터•PMU (Hardware Performance Counter and PMU)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 91
extra:
  question_no: "091"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "CPU 병목 가설을 사건 계수로 검증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PMU(Performance Monitoring Unit)**: CPU 실리콘 다이 내부에 탑재되어 명령어 실행, 캐시 미스, 분기 예측 등 하드웨어 마이크로아키텍처 이벤트를 수집하는 전용 모니터링 하드웨어.
- **HPC(Hardware Performance Counter, PMC)**: PMU 내부에서 특정 하드웨어 이벤트 발생 횟수를 클록 단위로 누적 기록하는 특수 목적 레지스터(MSR).
- **IPC(Instructions Per Cycle)**: CPU가 1클록 사이클당 완료(Retire)한 명령어 수로 파이프라인 효율을 나타내는 핵심 성능 지표.

</details>

- 정의/개념: CPU 실리콘 마이크로아키텍처 내부의 명령어 실행 수, CPU 사이클, 캐시 미스(L1/L2/L3), 분기 예측 실패(Branch Misprediction) 등 하드웨어 이벤트를 소프트웨어 오버헤드 없이 실시간 계측하는 전용 하드웨어 유닛(PMU) 및 카운터 레지스터(PMC/MSR)
- 배경/필요성: 단순 수행 시간 측정의 한계 극복 및 CPU 파이프라인 스톨·캐시 미스 등 마이크로아키텍처 병목 지점의 정량적 원인 규명 필요

#### 한줄 요약

- CPU 내부 마이크로아키텍처 사건을 하드웨어적으로 계측하여 **마이크로초 단위 병목을 분석하는 PMU & 성능 카운터** ## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PEBS(Precise Event-Based Sampling)**: 인텔 CPU에서 지원하는 정밀 하드웨어 샘플링 기술로 이벤트 발생 시 정확한 IP(명령어 포인터)와 레지스터 상태를 버퍼에 덤프(ARM은 SPE).
- **Counter Multiplexing(다중화)**: 물리 카운터 수(보통 4~8개)보다 많은 이벤트를 측정하기 위해 시간을 쪼개어 번갈아 활성화한 후 비례 스케일링하는 기법.

</details>

![PMU 다중화 실행 비율에 따른 보정 배율 차트](/study/diagrams/pmu-multiplex-scale.svg)

- 소스 코드 수정이나 실행 간섭(Probe Effect) 없이 나노초 단위로 정확히 계측하는 **비침습적 하드웨어 수준 수집**
- 파이프라인 프런트엔드/백엔드 바운드, 배드 스펙큘레이션을 체계적으로 진단하는 **Topdown 마이크로아키텍처 분석(TMA)**
- 정확한 병목 코드 라인을 식별하는 **PEBS/SPE 정밀 샘플링** 및 물리 카운터 한계를 극복하는 **시분할 다중화(Multiplexing)** #### 한줄 요약

- **비침습 하드웨어 계측·Topdown 마이크로아키텍처 분석(TMA)·PEBS 정밀 샘플링 및 시분할 다중화(Multiplexing)** ## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Event Selector MSR(IA32_PERFEVTSELx)**: 측정하고자 하는 특정 이벤트 번호, 유저/커널 모드 마스크, 카운터 활성화 비트를 설정하는 제어 레지스터.
- **Performance Counter MSR(IA32_PMCx)**: 이벤트 발생 시 1씩 증가하며 48비트~64비트 크기로 카운트를 누적하는 데이터 레지스터.

</details>

```text
[ PMU 하드웨어 계측 및 프로파일링 데이터 흐름도 ]
┌─────────────────────────────────────────────────────────────┐
│ 1. CPU 마이크로아키텍처 이벤트 원천 (ALU, L1/L2/L3 Cache, BPU)│
└──────────────────────────────┬──────────────────────────────┘
                               │ [ 실시간 하드웨어 펄스 신호 ]
┌──────────────────────────────┴──────────────────────────────┐
│ 2. PMU 하드웨어 유닛 (Performance Monitoring Unit)          │
│  ├─ 3. Event Selector MSR (필터링: IA32_PERFEVTSELx)         │
│  ├─ 4. Performance Counter MSR (계수 누적: IA32_PMCx)       │
│  └─ 5. PEBS 하드웨어 버퍼 (정밀 IP 및 레지스터 상태 덤프)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ [ 카운터 오버플로우 ──> PMI 인터럽트 ]
┌──────────────────────────────┴──────────────────────────────┐
│ 6. 성능 분석 도구 (Linux perf, Intel VTune, eBPF 프로파일러) │
└─────────────────────────────────────────────────────────────┘
```

선의 의미: CPU 파이프라인 이벤트 원천, Event Selector MSR, Performance Counter MSR 및 리눅스 perf/VTune 분석 도구 간의 PMU 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 이벤트 원천 | 연산기(ALU), 캐시 계층, 분기 예측기 등 CPU 내부에서 발생하는 마이크로아키텍처 하드웨어 신호 |
| 이벤트 선택기(Event Selector MSR) | 계측 대상 하드웨어 이벤트 번호, 유저/커널 모드 마스크 및 카운터 활성화를 설정하는 제어 레지스터 |
| 성능 카운터(PMC MSR) | 지정된 하드웨어 이벤트 발생 시마다 값을 누적 계수하고 오버플로우 시 PMI 인터럽트를 발생시키는 레지스터 |
| 수집·분석 도구 | Linux perf, Intel VTune 등 PMC 레지스터를 읽어 Topdown 메트릭 및 코드 라인별 병목을 시각화하는 도구 |

#### 한줄 요약

- **이벤트 원천(ALU/Cache/Branch)·이벤트 선택기(Event Selector MSR)·성능 카운터(PMC MSR)·프로파일링 툴(perf/VTune)** ## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PMI(Performance Monitor Interrupt)**: 성능 카운터 레지스터가 오버플로우될 때 발생하여 OS 커널의 프로파일링 핸들러를 호출하는 하드웨어 인터럽트.

</details>

```text
[ PMU 기반 성능 프로파일링 및 병목 분석 시퀀스 ]
                         │
                         ▼
   [ 1. 분석 대상 이벤트 선정 및 Event Selector MSR 레지스터 구성 ]
                         │
                         ▼
   [ 2. 목표 애플리케이션 실행 ──> PMU 가 하드웨어 사이클/이벤트 카운팅 ]
                         │
                         ▼
   [ 3. 카운터 오버플로우 도달 ──> PMI 인터럽트 발생 및 PEBS 덤프 ]
                         │
                         ▼
   [ 4. 커널 드라이버가 샘플 수집 ──> 다중화(Multiplexing) 스케일링 보정 ]
                         │
                         ▼
   [ 5. IPC, 캐시 미스율, TMA 메트릭 산출 ──> 병목 핫스팟 코드 라인 확정 ]
```

**동작 원리** 1. **이벤트 설정**: `perf` 툴이 측정할 이벤트(CPU Cycles, Instructions, LLC-Misses)를 MSR에 프로그래밍
2. **하드웨어 계수**: CPU 파이프라인에서 명령어가 실행될 때마다 PMU 카운터 레지스터가 1클록 단위로 계수
3. **샘플링 인터럽트**: 설정된 샘플링 주기에 도달하여 카운터가 오버플로우되면 PMI 인터럽트를 발생시키고 PEBS로 현재 IP 덤프
4. **다중화 보정**: 시분할 다중화로 수집된 이벤트에 대해 `(총 경과 시간 / 실제 측정 시간)` 배율을 곱해 실제 이벤트 수 보정
5. **병목 규명**: Topdown 분석법을 적용하여 프런트엔드/백엔드/메모리 바운드 비율을 시각화하고 최적화 포인트 도출

#### 한줄 요약

- 타깃 이벤트 MSR 설정 $\to$ **워크로드 실행 및 하드웨어 카운팅 $\to$ 카운터 오버플로우 시 PMI 인터럽트/PEBS 기록 $\to$ 시분할 다중화 스케일링 보정 $\to$ Topdown 병목 분석** ## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hardware PMU vs Software Profiling**:
  - Hardware PMU: CPU MSR 직접 계측, 오버헤드 $<1\%$, IPC/캐시미스/스톨 정량화
  - Software Profiling: 소스/바이너리 인스트루멘테이션, 오버헤드 $5\sim 30\%$, 함수 실행시간 한정

</details>

| 구분 | 하드웨어 PMU 계측 (Hardware PMU / PMC) | 소프트웨어 계측 프로파일링 (Software Profiling / Instrumentation) |
|:---|:---|:---|
| 계측 메커니즘 | CPU 내부 하드웨어 전용 MSR 레지스터가 자동 계수 | 소스 코드 또는 바이너리에 타이머/카운터 코드 삽입 |
| 성능 오버헤드 및 간섭 | 극소 오버헤드 ($<1\%$, 프로브 이펙트 최소화) |  함수 호출마다 오버헤드 누적 ($5\sim 30\%$, 프로브 왜곡 발생) |
| 분석 데이터 및 한계 | 마이크로아키텍처 뼛속 병목 (IPC, 캐시 미스, TMA) | 상위 레벨 함수 호출 시간 및 콜 스택 추적 한정 |

#### 한줄 요약

- 마이크로아키텍처 병목 규명은 **PMU 하드웨어 계측**, 상위 콜스택 추적은 **소프트웨어 프로파일링** ## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CPU Affinity(피닝)**: 분석 대상 프로세스를 특정 CPU 코어에 고정하여 스케줄러에 의한 코어 마이그레이션 및 PMU 컨텍스트 오염을 방지하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 물리 성능 카운터 수량 제약(보통 4~8개)으로 인한 다중 하드웨어 이벤트 동시 계측 한계 | **시분할 카운터 다중화(Counter Multiplexing)** 및 시간 가중치 비례 스케일링 적용 | 단일 프로파일링 세션에서 다수의 마이크로아키텍처 이벤트 동시 추정 측정 |
| 스레드의 동적 코어 마이그레이션으로 인한 CPU 카운터 데이터 불일치 및 컨텍스트 오염 | **CPU Affinity(코어 피닝)** 적용을 통한 분석 대상 프로세스 전용 코어 고정 | 코어 이동에 따른 캐시 미스 왜곡 방지 및 측정 데이터 일관성 보장 |
| 과도한 샘플링 빈도로 인한 PMI(Performance Monitor Interrupt) 폭주 및 시스템 성능 저하 | **PEBS(Precise Event-Based Sampling) 하드웨어 버퍼링** 및 샘플링 주기 최적화 | 인터럽트 오버헤드 극소화 및 정확한 명령어 포인터(IP) 덤프 확보 |

#### 한줄 요약

- **카운터 시분할 다중화(Multiplexing) 보정·CPU Affinity 피닝 고정·PEBS 버퍼링 기반 PMI 인터럽트 오버헤드 억제** ## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **eBPF와 PMU의 결합**: eBPF kprobe/tracepoint와 하드웨어 PMU 카운터를 결합하여 실시간 프로덕션 환경에서 무중단으로 하드웨어 병목을 모니터링하는 최신 옵저버빌리티(Observability) 트렌드.

</details>

- 고성능 시스템 최적화 및 커널 튜닝 시 **Intel TMA(Topdown Microarchitecture Analysis) 방법론과 Linux perf/eBPF 연계 표준 채택** #### 한줄 요약

- **하드웨어 이벤트 정량화와 Topdown 분석** 통한 시스템 성능 최적화 달성
