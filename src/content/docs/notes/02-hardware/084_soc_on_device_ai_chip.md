---
sidebar:
  order: 84
  label: "084. SoC AI 온디바이스 칩 (SoC On-Device AI Chip)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "SoC AI 온디바이스 칩 (SoC On-Device AI Chip)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 84
extra:
  question_no: "084"
  source_status: "기출"
  source_history: "134회, 135회"
  priority: 85
  priority_note: "연산자•메모리•지속 전력의 반복 기출"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **온디바이스 AI(On-Device AI)**: 스마트폰·차량·IoT 단말의 로컬 자원에서 AI 추론을 수행하는 기술.
- **NPU(Neural Processing Unit)**: 딥러닝 텐서 행렬 곱셈/누적(MAC) 연산을 초고속, 저전력으로 하드웨어 가속하는 전용 온칩 IP 코어.
- **SoC(System on Chip)**: CPU, GPU, NPU, ISP, LPDDR 메모리 컨트롤러 및 SRAM 버퍼가 실리콘 단일 다이에 통합된 시스템 반도체.

</details>

- 정의/개념: 단말 단독 로컬 추론을 위해 CPU, GPU, **NPU** 가속기 및 공유 SRAM 버퍼를 실리콘 칩 상에 융합한 **SoC AI 온디바이스 칩**
- 배경/필요성: 클라우드 전용 추론은 **망 지연·단절과 원본 데이터 전송 의존**

#### 한줄 요약

- 온디바이스 AI는 단말 내부의 이기종 연산기로 저지연•오프라인 추론을 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TOPS(Tera Operations Per Second)**: 초당 조 단위 연산 수를 나타내며 정밀도·연산 정의를 함께 봐야 하는 지표.
- **DVFS(Dynamic Voltage Frequency Scaling)**: 칩 발열량과 런타임 텐서 부하량에 따라 모듈의 공급 전압 및 주파수를 동적 제어하는 전력 절감 기술.
- **TDP(Thermal Design Power)**: 냉각 설계가 지속적으로 처리해야 하는 대표 열 설계 전력.

</details>

- 망 왕복 지연과 원본 데이터 전송을 줄이는 **온디바이스 AI** 구동
- **TOPS**보다 연산자 지원·메모리·지속 전력을 반영한 **NPU** 실효 성능 평가
- 단말 배터리 수명 및 **TDP** 제한을 수용하기 위한 **DVFS** 제어

#### 한줄 요약

- 메모리 대역폭과 TDP 한도가 NPU 지속 처리량을 제한한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Systolic Array**: 데이터가 MAC 셀 배열을 규칙적으로 이동하며 재사용되는 NPU 연산 구조.
- **공유 온칩 버퍼(SRAM/SRAM Buffer)**: 외부 LPDDR DRAM 접근 시 소모되는 전력을 막기 위해 딥러닝 가중치/활성화 값을 칩 내부 상주시키는 콤팩트 SRAM.

</details>

```text
[CPU•GPU 호스트] -- [메모리•온칩 버퍼] -- [NPU]
                                                |
                                                |
                                        [전력•열 제어]
```

선의 의미: CPU/GPU 호스트 제어 하에 NPU 가속기가 공유 온칩 SRAM 버퍼 및 전력/열 제어 모듈과 긴밀히 연동되는 칩 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| CPU/GPU 호스트 | 런타임 제어, 전후처리(Pre/Post-Processing) 및 미지원 레이어 fallback 수용 |
| NPU 가속기 | **Systolic Array** 및 MAC 연산기를 통한 Convolution/Linear 레이어 가속 |
| 공유 온칩 버퍼 | LPDDR 접근을 줄이기 위해 가중치와 활성화 데이터 재사용 |
| 전력·열 제어 | 칩셋 온도 스로틀링(Throttling) 방지 및 부하 기반 **DVFS** 스케줄링 |

#### 한줄 요약

- CPU•GPU 호스트, NPU 실행부, 메모리•온칩 버퍼, 전력•열 제어가 결합된 SoC 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **양자화(Quantization)**: 부동소수점 값을 저정밀 정수로 변환해 모델 크기와 연산 비용을 줄이는 기법.
- **그래프 융합(Graph Fusion)**: Conv + Bias + ReLU와 같은 연속적 레이어를 1개 융합 연산자로 합쳐 메모리 전송을 절감하는 컴파일 기법.

</details>

```text
[센서•응용 입력]
        │
        ▼
1. 모델 컴파일•연산자 분할
        │
        ▼
2. 텐서•온칩 버퍼 계획
        │
        ▼
3. 이기종 서브그래프 실행
   ┌────┴──────────────┐
   │ 지원 연산자      │ 미지원 연산자
   ▼                   ▼
 [NPU]            [CPU•GPU 대체]
   └────────┬──────────┘
            ▼
4. 전력•열 피드백 제어
            │
            ├── 다음 실행 계획 조정
            ▼
      [응용 결과 반환]
```

### 동작 원리

1. 모델 컴파일·연산자 분할: **양자화(INT8)**, **그래프 융합** 및 NPU 지원 연산자 분할 파이프라인 형성.
2. 텐서·온칩 버퍼 계획: SRAM 메모리 맵핑 및 가중치 전송 최소화 Tiling 계획 구성.
3. 이기종 서브그래프 실행: Conv/MatMul 레이어는 **NPU** 가속, Custom 연산자는 CPU/GPU fallback 수행.
4. 전력·열 피드백 제어: NPU 온도·전력을 측정하고 **DVFS** 운전점을 조절.

#### 한줄 요약

- 모델 컴파일·연산자 분할, 텐서·온칩 버퍼 계획, 전력·열 피드백 제어를 함께 최적화해야 지속 추론 성능을 유지할 수 있다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cloud AI**: 데이터센터 가속기와 확장 자원을 이용해 원격에서 AI 모델을 추론하는 방식.

</details>

| 비교 항목 | On-Device AI (SoC NPU) | Cloud AI (Data-Center GPU) |
|:---|:---|:---|
| 연산 위치 | 단말기 소형 **SoC** 단독 (로컬 단말) | 데이터센터 중앙 서버 (클라우드 파이프라인) |
| 반응 지연 | 망 왕복 없이 로컬 실행 | 망 상태와 서버 부하 지연 포함 |
| 개인정보 | 원본 데이터 외부 전송을 줄일 수 있음 | 전송·저장·처리 전 구간 보호 필요 |
| 연산/전력 자원 | **TDP**·배터리·메모리 제약 | 데이터센터 자원 확장과 운영 비용 발생 |

#### 한줄 요약

- 개인정보와 지연 요구를 전력·온도 한도 안에서 만족하면 단말에서 추론하고, 자원 한도를 넘는 모델은 클라우드와 분담한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Fallback**: NPU 컴파일러가 새로 추가된 미지원 커스텀 레이어 수용 시 CPU/GPU 코어로 처리를 이관하는 예외 처리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NPU 미지원 딥러닝 연산자 포함 시 **Fallback** 오버헤드 | 컴파일러 커스텀 커널 업데이트 및 CPU/GPU 오프로드 | 모델 실행 끊김 방지 |
| LPDDR 메모리 대역폭 부족에 따른 NPU 유휴 | 저정밀 **양자화**와 **SRAM Tiling** | 외부 메모리 전송량 감소 |
| 연속 추론 시 단말 열 스로틀링 발생 | **DVFS**와 부하 분산·추론 주기 조절 | 지속 처리량과 표면 온도 균형 |

> 사례: 정점 TOPS와 동일 모델의 지속 지연·전력·온도 비교

#### 한줄 요약

- 자원 프로파일러로 연산자, 메모리 대역폭, 열 스로틀링을 함께 검증한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **On-Device AI 선택 기준(On-Device AI Selection Criteria)**: 텐서 연산 지원성, NPU TOPS/Watt 효율, 메모리 대역폭 및 TDP 범위에 기반한 아키텍처 수립 체계.

</details>

- 지연·프라이버시 요구가 자원 안이면 **온디바이스**, 초과 모델은 **클라우드**•**하이브리드** 선택

#### 한줄 요약

- 단말 자원 안이면 로컬, 초과 모델은 클라우드나 하이브리드로 분담한다.
