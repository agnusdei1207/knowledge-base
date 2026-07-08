---
title: "하드웨어 성능 카운터·PMU (Hardware Performance Counter PMU)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 107
extra:
  question_no: "107"
  exam_status: "미출제"
---

## 미리 알고가기

- PMU는 CPU 내부 이벤트를 계측하는 하드웨어 블록임
- CPI와 IPC는 명령 처리 효율을 해석하는 대표 지표임
- cache miss와 branch miss와 TLB miss는 병목 원인 분석에 자주 쓰임

## Ⅰ. 개요

- **정의/개념**: 하드웨어 성능 카운터와 PMU는 CPU 내부에서 발생하는 cycle과 instruction과 cache miss와 branch miss 같은 이벤트를 낮은 오버헤드로 측정해 마이크로아키텍처 병목 원인을 분석하는 계측 기능임
- **배경/필요성**: wall-clock 시간만으로는 코드가 왜 느린지 알기 어려우므로, 성능 최적화와 용량 기준선 수립에는 CPU 내부 이벤트를 직접 관측하는 수단이 필요함

## Ⅱ. 특징

- 소프트웨어 프로파일러보다 하드웨어 병목 원인을 더 직접적으로 보여줌
- sampling 기반으로 운영 환경에서도 비교적 낮은 오버헤드로 사용 가능함
- CPU 세대별 이벤트 의미와 정확도를 이해해야 해석 오류를 줄일 수 있음
- 단일 카운터보다 CPI와 IPC와 miss rate를 함께 읽어야 의미가 생김

## Ⅲ. 종류 및 비교

| 판단 기준 | 소프트웨어 프로파일링 | PMU 계측 |
|:---|:---|:---|
| 관측 대상 | 함수 시간과 호출 경로 | cycle, cache, branch, TLB 이벤트 |
| 장점 | 코드 위치 파악이 쉬움 | 병목 원인 파악이 정밀함 |
| 한계 | 하드웨어 원인 해석이 약함 | 이벤트 의미와 카운터 수 제한 존재 |
| 활용 방식 | 함수 최적화 시작점 | 원인 검증과 기준선 수립 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Event Source | pipeline과 cache와 branch predictor에서 계측 대상 이벤트를 생성함 |
| PMU Controller | 어떤 이벤트를 어떤 카운터로 셀지 정하고 overflow sampling을 제어함 |
| Hardware Counter | 선택된 이벤트 횟수와 cycle을 누적해 정량 비교의 기반 데이터를 제공함 |
| Analysis Tool | perf 같은 도구가 카운터를 수집하고 CPI와 miss rate 해석으로 병목을 드러냄 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 이벤트 선정    | --> | 카운터 설정    | --> | 실행 및 수집   | --> | 비율 해석      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **이벤트 선정**: cycle과 instruction과 miss 계열 중 분석 목표에 맞는 이벤트를 고름
2. **카운터 설정**: sampling 주기와 코어 바인딩과 privilege 범위를 정함
3. **실행 및 수집**: workload를 돌리며 카운터 값과 샘플 스택을 수집함
4. **비율 해석**: CPI와 IPC와 miss rate를 계산해 병목 원인을 판단함

## Ⅵ. 문제점 및 해결 방안

1. 문제: CPU 세대별 이벤트 정의 차이를 무시하면 같은 이름의 카운터도 전혀 다른 의미로 해석될 수 있음
   - 해결방안: vendor event guide와 errata를 기준으로 이벤트를 검증하고 event mapping accuracy와 review defect count로 검증함
2. 문제: 동시에 측정 가능한 카운터 수가 제한되어 multiplexing 시 오차가 커질 수 있음
   - 해결방안: 이벤트 세트를 분리 측정하고 반복 실행으로 보정하며 counter scaling error와 run-to-run variance로 검증함
3. 문제: 주파수 변화와 스케줄링 이동이 섞이면 PMU 수치가 workload 차이보다 환경 잡음을 더 반영할 수 있음
   - 해결방안: CPU pinning과 고정 주파수와 warm-up 절차를 적용하고 run-to-run variance와 baseline drift로 검증함

## Ⅶ. 적용 사례

- 서비스 지연 분석에서는 perf로 cache miss와 CPI를 수집하고, cache miss rate와 CPI로 결과를 확인함
- 데이터베이스 튜닝에서는 코어 고정 후 branch miss와 memory stall을 비교하고, IPC와 run-to-run variance로 결과를 확인함
- 배포 전 성능 기준선 검증에서는 동일 워크로드의 PMU 프로파일을 비교하고, baseline drift와 counter scaling error로 결과를 확인함

## Ⅷ. 결론

PMU는 성능 수치를 설명하는 도구가 아니라 병목 원인을 증명하는 도구이므로, 해석 품질은 이벤트 선택과 측정 조건 통제에 달림.
