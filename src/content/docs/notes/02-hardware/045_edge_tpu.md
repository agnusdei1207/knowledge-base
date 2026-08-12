---
sidebar:
  order: 45
  label: "045. Edge TPU (Edge TPU)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Edge TPU (Edge TPU)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-hardware"
weight: 45
extra:
  question_no: "045"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "완전 정수•CPU 구간의 배포 판단"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Edge TPU(Edge Tensor Processing Unit)**: 모바일/IoT Edge 디바이스에서 완전 정수 양자화 신경망 추론을 전용 처리하도록 구글이 설계한 소형 ASIC 칩.
- **현장 추론(Edge Inference)**: 원격 클라우드 서버 통신 없이 엣지 단말 소스 측에서 즉시 AI 모델을 추론 실행하는 방식.
- **ASIC(Application-Specific Integrated Circuit)**: 특정 기능의 하드웨어 연산 로직을 전용 반도체 회로로 고정 구현한 맞춤형 칩.

</details>

- 정의/개념: **현장 추론** 환경을 위해 완전 정수 양자화(INT8) TFLite 모델 가속을 전용 수행하는 초소형 **ASIC**인 **Edge TPU**
- 배경/필요성: 클라우드 추론의 네트워크 라운드트립 지연, 대역폭 비용 및 통신 단절에 따른 실시간 현장 판정 한계 극복

#### 한줄 요약

- 에지 텐서 처리 장치는 완전 정수 모델을 현장에서 실행해 네트워크 단절 중에도 낮은 전력으로 추론 결과를 제공한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **완전 정수 양자화(Full Integer Quantization)**: 모델 파라미터(가중치/활성화)를 8비트 정수(INT8)로 완전 변환하여 메모리 및 연산량을 삭감하는 변환 기술.
- **지원 연산 컴파일(Supported-Operation Compilation)**: TFLite 모델 내 Edge TPU 전용 지원 연산자를 추출하여 바이트코드로 빌드하는 과정.
- **CPU(Central Processing Unit)**: Edge TPU 미지원 텐서 연산을 우회 처리하는 범용 프로세서.
- **CPU 폴백(CPU Fallback)**: Edge TPU 하드웨어가 직접 지원하지 않는 레이어를 CPU가 전담하여 대치 실행하는 백업 경로.
- **장치 전환 비용(Device-Transition Cost)**: Edge TPU와 CPU 상호 간 경계 텐서 메모리 복사 및 스케줄링 동기화에서 발생하는 오버헤드.

</details>

- 메모리 Footprint 및 소모 전력을 최소화하는 **완전 정수 양자화** 전용 처리
- 칩 내부 가속 영역을 구성하는 **지원 연산 컴파일** 및 연산자 매핑
- 미지원 레이어 발생 시 장치 간 오버헤드를 유발하는 **CPU 폴백** 및 **장치 전환 비용** 발생

#### 한줄 요약

- 에지 텐서 처리 장치 지원 연산률이 낮고 폴백 경계가 많으면 CPU와 장치 사이의 텐서 복사·동기화로 종단 지연이 증가한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **TFLite(TensorFlow Lite)**: 모바일 및 Edge 시스템에 최적화된 경량 추론 프레임워크 및 모델 규격.
- **Edge TPU 컴파일러(Edge TPU Compiler)**: TFLite 모델을 입력받아 Edge TPU 지원 가능 영역과 CPU 폴백 영역으로 수직 분할하는 컴파일 도구.
- **TFLite 런타임(TFLite Runtime)**: 서브그래프 실행 순서를 제어하고 NPU 칩 및 CPU 간 텐서 이송을 제어하는 경량 런타임 엔진.

</details>

```text
[완전 정수 TFLite 모델] -- [Edge TPU 컴파일러] -- [TFLite 런타임•CPU] -- [Edge TPU 코어]
```

선의 의미: 완전 정수 TFLite 모델이 컴파일러 분할을 거쳐 런타임 제어 하에 Edge TPU 전용 코어 및 CPU로 할당되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 완전 정수 TFLite 모델 | 8비트 정수(INT8) 양자화 텐서 그래프 제공 |
| Edge TPU 컴파일러 | 서브그래프 분할 및 Edge TPU 전용 가속 바이트코드 생성 |
| TFLite 런타임•CPU | 실행 순서 제어, 텐서 메모리 할당 및 **CPU 폴백** 총괄 |
| Edge TPU 코어 | INT8 시스톨릭 MAC 연산 및 온칩 SRAM 재사용 실행 |

#### 한줄 요약

- 컴파일러가 정수 모델을 에지 텐서 처리 장치와 CPU 실행 구간으로 나눈다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **정수 실행 계획(Integer Execution Plan)**: Edge TPU 지원/미지원 레이어 분할 및 메모리 할당 순서 명세.
- **경계 텐서(Boundary Tensor)**: Edge TPU 가속 영역과 CPU 폴백 영역의 인터페이스 상에서 교환되는 중간 텐서 데이터.
- **지원 구간(Supported Segment)**: Edge TPU 하드웨어 코어에서 연속적으로 처리 가능한 INT8 가속 연산자 그룹.

</details>

```text
                   [완전 정수 TFLite 모델]
                               |
                  1. 지원 구간•실행 계획 생성
                               |
                       [현장 추론 요청]
                               |
              +-----------------------------------+
              | 반복: 컴파일된 모델 구간         |
              |       [Edge TPU 지원?]            |
              |          /          \             |
              |        [예]         [아니요]       |
              |         |              |           |
              | 2. Edge TPU 실행  3. 경계 텐서•CPU 폴백 |
              |          \            /           |
              |         4. 구간 결과 연결         |
              +-----------------------------------+
                               |
                        [현장 추론 결과]
```

### 동작 원리

1. **지원 구간·실행 계획 생성**: **Edge TPU 컴파일러**를 통해 지원 연산 분석 및 **정수 실행 계획** 생성.
2. **Edge TPU 구간 실행**: **TFLite 런타임**이 **지원 구간**을 Edge TPU 온칩 하드웨어로 전달하여 INT8 연산 실행.
3. **경계 텐서·CPU 폴백**: 미지원 레이어 조우 시 **경계 텐서**를 CPU 전용 메모리로 이송 후 **CPU 폴백** 구동.
4. **구간 결과 연결**: 가속 결과와 폴백 결과를 런타임 상에서 병합하여 최종 **현장 추론** 결과 도출.

#### 한줄 요약

- 런타임은 지원 구간을 에지 텐서 처리 장치에서 실행하고, 비지원 구간은 경계 텐서를 CPU로 전달해 실행한 뒤 결과를 다시 연결한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **온디바이스 NPU(On-Device NPU)**: 메인 AP/SoC 칩 내부에 하드웨어로 내장 통합된 신경망 가속 프로세서.
- **클라우드 TPU(Cloud TPU)**: 데이터센터 환경에서 초거대 모델 학습 및 추론을 전담하는 대규모 TPU 인프라.
- **네트워크 왕복 지연(Network Round-Trip Latency)**: 에지 단말과 클라우드 데이터센터 간 왕복 전송 지연시간.

</details>

| 추론 가속 배치 | Edge TPU | 온디바이스 NPU | 클라우드 TPU |
|:---|:---|:---|:---|
| 적용 기준 | 외장 모듈 기반 저전력 현장 추론 시 | 스마트폰/SoC 통합 온디바이스 가속 시 | 클라우드 대규모 모델 학습 및 고성능 추론 시 |
| 핵심 특징 | **Edge TPU** 소형 USB/PCIe 전용 칩 | **온디바이스 NPU** SoC 내장 형태 | **클라우드 TPU** Pod 대규모 클러스터링 |
| 한계 | INT8 양자화 및 **장치 전환 비용** 오버헤드 | SoC 제조사 프레임워크 종속성 | 통신 대역폭 비용 및 **네트워크 왕복 지연** |

> 요약: 소형 모듈 추론은 Edge TPU, SoC 통합은 온디바이스 NPU, 클라우드 대규모 연산은 클라우드 TPU 선정.

#### 한줄 요약

- 외장 모듈형 정수 추론은 에지 텐서 처리 장치, SoC 통합 단말 추론은 온디바이스 NPU, 대규모 학습·추론은 클라우드 TPU가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **대표 보정 데이터(Representative Calibration Data)**: 양자화 시 텐서의 스케일 팩터 및 민감도 범위를 설정하는 샘플 데이터.
- **지원 연산자 대체(Operator Substitution)**: 컴파일 불가능한 연산자를 연산 특성이 동일한 Edge TPU 전용 연산자로 재작성하는 최적화 기법.
- **원자적 모델 교체(Atomic Model Replacement)**: 현장 구동 중 무중단으로 안전하게 갱신 모델을 교체하는 배포 패턴.
- **모델 롤백(Model Rollback)**: 배포 실패 또는 갱신 모델 오류 발생 시 이전 버전으로 즉시 원복시키는 장애 복구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **완전 정수 양자화** 변환에 따른 모델 추론 정확도 하락 | **대표 보정 데이터**를 활용한 Quantization Calibration | INT8 변환 후 정확도 손실 최소화 |
| 잦은 **CPU 폴백** 발생에 따른 텐서 복사 오버헤드 | 컴파일 분석 보고서 검토 및 **지원 연산자 대체** 수행 | **장치 전환 비용** 절감 및 연속 가속 |
| 소형 단말 발열 및 지속 전력 한도 초과 | 추론 듀티 사이클 조절 및 Sleep 모드 제어 | 현장 지속 가용성 및 전력 안정성 확보 |
| 오프라인 에지 환경 모델 업데이트 실패 시 시스템 장애 | **원자적 모델 교체** 및 실패 시 **모델 롤백** 내장 | 엣지 인프라 모델 갱신 안전성 확보 |

> 사례: 컴파일 미지원 레이어를 지원 연산자로 전환하는 **지원 연산자 대체** 적용

#### 한줄 요약

- 비지원 연산을 지원 연산 조합으로 바꾸면 CPU 폴백 경계와 텐서 복사가 줄어든다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **지원 연산률(Supported-Operation Ratio)**: 전체 신경망 레이어 중 Edge TPU 코어에서 컴파일되어 직접 가속 실행되는 비율.
- **Edge TPU 적용 기준(Edge TPU Adoption Criteria)**: 완전 정수 양자화 수용성, 오프라인 미션 크리티컬 환경 여부 및 소비 전력 요구사항에 기반한 선택 기준.

</details>

- **Edge TPU 적용 기준**에 따라 높은 **지원 연산률** 및 오프라인 저전력 추론 필요 시 **Edge TPU** 선택

#### 한줄 요약

- 지원 연산률이 높고 CPU 폴백을 포함한 종단 지연·전력이 목표를 만족할 때 에지 텐서 처리 장치 적용 원칙 준수.
