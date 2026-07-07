---
title: "하드웨어 성능 카운터·PMU (Hardware Performance Counter PMU)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 107
---

# 하드웨어 성능 카운터·PMU (Hardware Performance Counter PMU)

## 미리 알고가기

- PMU(Performance Monitoring Unit): CPU(Central Processing Unit) 내부 이벤트를 측정하는 성능 모니터링 장치임
- 성능 카운터: cache miss, branch miss, cycle, instruction 같은 이벤트 횟수를 세는 레지스터임
- CPI(Cycles Per Instruction): 한 명령어를 실행하는 데 소요된 평균 cycle 수임
- IPC(Instructions Per Cycle): 한 cycle 동안 평균 몇 개 명령어가 완료되는지를 나타내는 지표임
- TLB(Translation Lookaside Buffer): 가상 주소와 물리 주소 변환 결과를 캐시하는 버퍼임
- Sampling: 모든 이벤트를 기록하지 않고 일정 주기나 조건에 따라 대표 데이터를 수집하는 방식임

## 1. 개요

- **정의/개념**: 하드웨어 성능 카운터와 PMU는 프로세서 내부에서 발생하는 cycle, instruction, cache miss, branch miss, TLB miss 같은 이벤트를 하드웨어 레지스터로 측정하는 성능 분석 기능임.
- **배경/필요성**: 애플리케이션 지연은 CPU, 메모리, 캐시, 분기, I/O(Input/Output) 중 어느 요인인지 외부 시간 측정만으로 구분하기 어려움. PMU는 낮은 오버헤드로 마이크로아키텍처 이벤트를 수집해 시스템 병목을 추측이 아니라 CPU 이벤트 기준으로 진단하게 함.
- **비유**: 자동차 속도계만 보는 것이 아니라 엔진 회전수, 연료 분사, 브레이크 사용 횟수까지 기록하는 계기판과 같음.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 성능 병목 계측 능력 | PMU event, counter, sampling, CPI, cache miss | 단순 로그 모니터링으로 설명 |

> 요약: PMU는 CPU 내부 이벤트를 계측해 성능 저하 원인을 구조적으로 분석하는 하드웨어 기능임.

## 2. 특징 및 비교

| 판단 기준 | 소프트웨어 프로파일링 | 하드웨어 PMU 계측 |
|:---|:---|:---|
| 관측 대상 | 함수 시간, 호출 빈도, 코드 경로 | cycle, cache, branch, TLB, pipeline 이벤트 |
| 오버헤드 | instrumentation 방식은 오버헤드가 클 수 있음 | sampling 기반으로 낮은 오버헤드 가능 |
| 원인 분석 | 어느 함수가 느린지 확인 | 왜 느린지 마이크로아키텍처 원인 확인 |
| 한계 | 하드웨어 병목 해석이 어려움 | 이벤트 의미와 카운터 제약을 이해해야 함 |

> 요약: PMU는 소프트웨어 위치와 하드웨어 원인을 연결해 최적화 판단을 가능하게 함.

- **적용 조건**: 측정 대상 CPU와 운영체제가 필요한 PMU 이벤트와 권한을 제공해야 함
- **선택 지표**: IPC, CPI, cache miss rate, branch miss rate를 함께 해석해야 함
- **운영 관점**: 기준선과 측정 조건이 고정되어야 성능 변화의 원인을 비교할 수 있음

## 3. 구성요소/구조

```text
+----------+      +----------+      +----------+
| CPU core | ---> | PMU      | ---> | Counters |
+----------+      +----------+      +----------+
      |                |                |
      v                v                v
+----------+      +----------+      +----------+
| Events   |      | Sampler  |      | Profiler |
+----------+      +----------+      +----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 이벤트 소스 | pipeline, cache, branch predictor, TLB에서 측정 이벤트를 생성함 | 센서 |
| PMU 제어기 | 선택한 이벤트를 카운터에 연결하고 overflow interrupt를 관리함 | 계기판 제어부 |
| 성능 카운터 | 이벤트 횟수와 cycle을 저장하는 하드웨어 레지스터임 | 숫자 계량기 |
| 분석 도구 | perf, VTune 같은 도구가 counter 값을 수집·해석함 | 정비 진단기 |

> 요약: PMU는 CPU 이벤트 소스와 카운터, 분석 도구를 연결해 병목 데이터를 제공함.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Select   | ---> | Configure| ---> | Measure  | ---> | Analyze  |
+----------+      +----------+      +----------+      +----------+
```

1. **이벤트 선택** — 분석 목표에 따라 cycles, instructions, cache misses, branch misses 등을 선택함
2. **카운터 설정** — privilege level, sampling period, core binding, multiplexing 조건을 설정함
3. **실행·측정** — workload를 실행하며 카운터 값 또는 샘플 스택을 수집함
4. **병목 해석** — CPI, cache miss rate, branch miss rate, IPC를 계산해 원인을 판단함

> 요약: PMU 분석은 목표 이벤트를 선택하고 측정 조건을 고정한 뒤 비율 지표로 해석해야 함.

## 4. 문제점 및 개선방안

- **P1 이벤트 해석 오류**: CPU 세대별 이벤트 정의가 달라 같은 이름의 counter도 의미와 정확도가 다를 수 있음
- **P1 대응**: CPU vendor event guide와 errata를 기준으로 이벤트 의미를 확인함 (확인: event mapping version)
- **P2 카운터 자원 제한**: 동시에 측정 가능한 이벤트 수가 제한되어 multiplexing 시 오차가 생김
- **P2 대응**: 측정 목적별 이벤트 세트를 나누고 반복 실행으로 multiplexing 오차를 낮춤 (확인: counter scaling error)
- **P3 관측 교란**: sampling interrupt, context switch, CPU frequency 변화가 측정값을 왜곡할 수 있음
- **P3 대응**: CPU pinning, 고정 주파수, warm-up, baseline 측정으로 환경 변동을 통제함 (확인: run-to-run variance)

> 요약: PMU 값은 원시 숫자가 아니라 이벤트 정의 검증, 측정 세트 분리, 환경 통제를 거쳐 해석해야 함.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 서비스 지연 분석 | perf 같은 분석 도구로 cache miss, branch miss, CPI(Cycles Per Instruction)를 측정해 코드 병목 원인을 분리함 | IPC, cache miss rate |
| 데이터베이스 튜닝 | CPU(Central Processing Unit) pinning 후 PMU sampling으로 lock 경합, 메모리 대기, branch miss를 비교함 | CPI, run-to-run variance |
| 클라우드 용량 기준선 | 인스턴스 유형별 PMU 지표를 기준선으로 저장해 배포 전후 성능 변화를 검증함 | IPC change, counter scaling error |

> 요약: 실무에서는 wall-clock 지연과 PMU 원인 지표를 연결해 성능 개선의 근거를 검증함.

## 6. 결론

- **발전 방향**: eBPF(Extended Berkeley Packet Filter), cloud observability, heterogeneous CPU/GPU(Graphics Processing Unit) PMU, confidential computing 환경의 제한 계측과 결합해 운영 분석으로 확대됨
- **기술사적 판단**: 성능 개선 주장은 wall-clock 시간뿐 아니라 PMU 기반 원인 지표와 재현 가능한 측정 조건을 함께 제시해야 함
- **기술사 제언**: 주요 서비스의 성능 기준선에는 IPC, cache miss, branch miss, memory bandwidth 같은 PMU 지표를 포함해야 함
