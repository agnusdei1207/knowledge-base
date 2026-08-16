---
sidebar:
  order: 91
  label: "091. 하드웨어 성능 카운터•PMU (Hardware Performance Counter and PMU)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "하드웨어 성능 카운터•PMU (Hardware Performance Counter and PMU)"
date: "2026-08-13T12:21:04+09:00"
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

- **PMU(Performance Monitoring Unit)**: CPU 내부의 사이클, 캐시 미스, 분기 실패 등 마이크로아키텍처 사건을 계수하는 하드웨어 블록.
- **HPC(Hardware Performance Counter)**: PMU 내부에 배치되어 특정 성능 이벤트 발생 횟수를 카운팅하고 기록하는 특수한 MSR(Model Specific Register) 카운터 레지스터.
- **IPC(Instructions Per Cycle)**: 1 CPU 사이클당 수행 완료(Retired)된 명령어 수로, 마이크로아키텍처 병목 유무를 판단하는 핵심 메트릭 지표.

</details>

- 정의/개념: CPU 파이프라인의 명령 은퇴, 캐시 미스, 분기 예측 실패 등 microarchitectural 이벤트를 소프트웨어 개입 없이 하드웨어 모듈이 측정 분석하는 **PMU & 하드웨어 성능 카운터**
- 배경/필요성: 벽시계 시간만으로는 **캐시·분기·파이프라인 정체 원인 식별 불가**

#### 한줄 요약

- 하드웨어 성능 카운터로 CPU 내부 사건을 계수하여 실행•메모리 병목 원인을 분석한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PEBS/SPE(Precise Event-Based Sampling)**: 이벤트 발생 위치와 실행 정보를 낮은 스키드로 샘플링하는 정밀 계측 기능.
- **Multiplexing**: 물리 카운터보다 많은 이벤트를 시간 분할해 번갈아 측정하는 기법.

</details>

![PMU 다중화 실행 비율에 따른 보정 배율 차트](/study/diagrams/pmu-multiplex-scale.svg)

- 소프트웨어 계측보다 낮은 간섭의 **하드웨어 수집**
- **IPC(Instructions Per Cycle)**, 캐시 미스율, 분기 예측 실패율 기반 정밀 병목 진단
- **PEBS/SPE** 기반 사건 위치 표본화와 **Multiplexing** 시간 보정

$$
\mathrm{IPC}=\frac{N_{\mathrm{retired}}}{N_{\mathrm{cycles}}},\qquad
\mathrm{MissRate}=\frac{N_{\mathrm{miss}}}{N_{\mathrm{access}}},\qquad
\hat N=N_{\mathrm{raw}}\frac{T_{\mathrm{enabled}}}{T_{\mathrm{running}}}
$$

#### 한줄 요약

- 카운터 다중화는 측정 간섭을 줄이지만 CPU 모델별 이벤트 의미와 환산 오차를 확인해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Event Selector(PerfEvtSel MSR)**: 카운터가 계측할 특정 하드웨어 이벤트(Cache Miss, Branch Miss 등) 및 유저/커널 모드 비트를 지정하는 레지스터.
- **Performance Counter MSR(PMC MSR)**: Event Selector에 의해 지정된 이벤트 횟수가 물리적으로 1씩 증가 누적되는 카운터 레지스터.

</details>

```text
PMU 계측 구조
├─ 이벤트 원천
├─ 이벤트 선택기
├─ 성능 카운터
└─ 수집•분석 도구
```

선의 의미: CPU 파이프라인의 이벤트 원천이 Event Selector(MSR)와 Performance Counter를 거쳐 OS 수집/분석 도구(Perf/VTune)로 연동되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 이벤트 원천 | ALU, Cache, Branch Unit 등 CPU 내부 뼈대 장치에서 발생한 Event 인가 |
| Event Selector (MSR) | 측정 타깃 이벤트 코드 번호 인코딩 및 CPL(Privilege Level) 필터링 설정 |
| Performance Counter (PMC) | 이벤트 계수 보관 및 임계값 도달 시 PMI 인터럽트 발생 |
| 수집•분석 도구 | Linux **perf**, Intel **VTune**, Linux eBPF 등 MSR 수치 파싱 및 GUI 프로파일링 |

#### 한줄 요약

- 이벤트 원천, 이벤트 선택기, 성능 카운터, 수집•분석 도구의 PMU 계측 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PMI(Performance Monitor Interrupt)**: 카운터 레지스터가 Overflow 되었을 때 OS로 제어권을 넘겨 PEBS 샘플 버퍼를 비우게 하는 하드웨어 인터럽트.

</details>

```text
[CPU 병목 가설]
       │
       ▼
1. 이벤트•측정 조건 선택
       │
       ▼
2. 동일 워크로드 반복 실행
       │
       ▼
3. 사건 계수•위치 샘플 수집
       │
       ▼
4. 활성 시간 보정•지표 산출
       │
       ▼
5. 코드 위치•사건 상관 분석
       │
       ▼
[병목 가설 채택•기각]
```

### 동작 원리

1. 이벤트·측정 조건 선택: 분석 타깃 이벤트 선정 및 **Event Selector MSR** 세팅.
2. 동일 워크로드 반복 실행: 프로세스 구동 및 CPU 파이프라인 상의 실시간 하드웨어 이벤트 카운팅.
3. 사건 계수·위치 샘플 수집: PMC 카운터 수치 갱신 및 Overflow 시 **PMI 인터럽트** / **PEBS** 샘플링 덤프.
4. 활성 시간 보정·지표 산출: **Multiplexing** 시간 비율 보정 및 **IPC**, Miss-rate 지표 자동 산출.
5. 코드 위치·사건 상관 분석: 병목 유발 코드 라인(Hotspot) 및 아키텍처 원인 연동 검증.

#### 한줄 요약

- 같은 부하에서 사건 계수·위치 샘플 수집과 코드 위치·사건 상관 분석을 결합하여 CPU 병목 가설을 검증한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Software Profiling**: 샘플링·계측 코드를 이용해 함수 시간, 호출 관계와 할당 등을 분석하는 방식.

</details>

| 비교 항목 | PMU 하드웨어 계측 | Software Profiling |
|:---|:---|:---|
| 수집 방식 | CPU 내장 전용 레지스터(**PMC MSR**) 계측 | 소프트웨어 코드 삽입(Instrumentation) 및 타임 래칭 |
| 측정 오버헤드 | 카운팅은 낮고 샘플링 빈도에 따라 증가 | 샘플링·계측 방식에 따라 변동 |
| 세부 분석 영역 | L1/L2/L3 캐시 미스, TLB, Branch Prediction | 함수 호출 횟수, 벽시계 시간(Wall-clock Time) |
| 정확성 | **PEBS/SPE**로 사건 위치의 스키드 감소 | 계측 삽입 시 실행 시간 교란 가능 |

#### 한줄 요약

- 소프트웨어 프로파일링은 느린 코드 위치를 찾고, PMU는 그 위치에서 발생한 CPU 내부 사건의 원인을 분석한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CPU Pinning**: 분석 스레드가 다른 CPU 코어로 migration 되어 PMU MSR 데이터가 오염되는 것을 막기 위해 코어를 정적 바인딩하는 설정.

- **정밀 이벤트 기반 샘플링(Processor Event-Based Sampling, PEBS)**: 하드웨어 성능 카운터 오버플로 시 CPU 내부 버퍼에 레지스터 상태와 IP 주소를 직접 기록하여 프로파일링 오버헤드를 최소화하는 인텔 하드웨어 기능.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 물리 카운터 제한으로 이벤트 동시 수집 부족 | **Multiplexing**과 활성 시간 보정 적용 | 더 많은 이벤트의 추정 계수 확보 |
| 코어 이동과 부하 변동으로 반복 측정 분산 증가 | **CPU Pinning**과 동일 부하 반복 측정 | 비교 실험의 변동성 감소 |
| 과도한 샘플링률로 PMI 인터럽트 증가 | **PEBS Buffer**와 샘플링 주기 조정 | 프로파일러 자체 간섭 감소 |

> 사례: perf로 캐시 미스 가설을 세우고 반복 실험으로 IPC 변화를 검증

#### 한줄 요약

- 반복 부하의 캐시 미스율과 IPC로 메모리 정체를 검증한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **PMU 분석 선택 기준(PMU Performance Profiling Criteria)**: 타깃 성능 병목, 분석 세밀도(Microarchitectural vs Function), 오버헤드 허용성에 기초한 체계.

</details>

- 캐시·분기 원인은 **PMU**, 함수 시간·호출 관계는 **Software Profiling** 선택

#### 한줄 요약

- 캐시·분기 원인은 PMU, 함수 시간과 호출 관계는 소프트웨어 프로파일링을 선택한다.
