---
sidebar:
  order: 84
  label: "084. SoC AI 온디바이스 칩 (SoC On-Device AI Chip)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "SoC AI 온디바이스 칩 (SoC On-Device AI Chip)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **온디바이스 AI(On-Device AI)**: 인터넷 연결(클라우드 서버) 없이 스마트폰, 스마트카, IoT edge 단말 자원만으로 딥러닝 추론(Inference)을 100% 로컬 수행하는 기술.
- **NPU(Neural Processing Unit)**: 딥러닝 텐서 행렬 곱셈/누적(MAC) 연산을 초고속, 저전력으로 하드웨어 가속하는 전용 온칩 IP 코어.
- **SoC(System on Chip)**: CPU, GPU, NPU, ISP, LPDDR 메모리 컨트롤러 및 SRAM 버퍼가 실리콘 단일 다이에 통합된 시스템 반도체.

</details>

- 정의/개념: 단말 단독 로컬 추론을 위해 CPU, GPU, **NPU** 가속기 및 공유 SRAM 버퍼를 실리콘 칩 상에 융합한 **SoC AI 온디바이스 칩**
- Background/필요성: 클라우드 연동 네트워크 지연시간(Latency), 통신 장애 위험, 데이터센터 서버 통신 비용 및 개인정보(Privacy) 유출 파급 차단 요구

#### 한줄 요약

- 온디바이스 AI는 단말 내부의 이기종 연산기로 저지연•오프라인 추론을 수행한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **TOPS(Tera Operations Per Second)**: 1초당 1조(10^12) 회의 8-bit/16-bit 텐서 연산을 수행할 수 있는 온디바이스 AI 가속기의 성능 지표.
- **DVFS(Dynamic Voltage Frequency Scaling)**: 칩 발열량과 런타임 텐서 부하량에 따라 모듈의 공급 전압 및 주파수를 동적 제어하는 전력 절감 기술.
- **TDP(Thermal Design Power)**: 칩셋이 정상 구동 시 허용 가능한 최대 발열/소비전력 한계선.

</details>

- 초저지연, 데이터 보안, 오프라인 독립성을 보장하는 **온디바이스 AI** 구동
- 10~50 **TOPS** 급 저전력 신경망 가속 전용 **NPU** 및 SRAM 타일링(Tiling) 기반 메모리 대역폭 절감
- 단말 배터리 수명 및 **TDP** 제한을 수용하기 위한 **DVFS** 제어

#### 한줄 요약

- 메모리 대역폭과 TDP 한도가 NPU 지속 처리량을 제한한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Systolic Array**: 텐서 행렬 연산 데이터가 체스판 형태의 MAC(Multiply-Accumulate) 연산기 셀들을 거치며 메모리 접근을 극소화하는 NPU 코어 구조.
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
| 공유 온칩 버퍼 | LPDDR 억세스를 최소화하기 위해 가중치(Weight) 및 활성화 데이터 상주 보관 |
| 전력·열 제어 | 칩셋 온도 스로틀링(Throttling) 방지 및 부하 기반 **DVFS** 스케줄링 |

#### 한줄 요약

- CPU•GPU 호스트, NPU 실행부, 메모리•온칩 버퍼, 전력•열 제어가 결합된 SoC 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **양자화(Quantization)**: FP32(32비트 부동소수점) 파라미터를 INT8(8비트 정수)로 변환하여 메모리 및 연산량을 75% 절감하는 최적화 기법.
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

1. **모델 컴파일·연산자 분할**: **양자화(INT8)**, **그래프 융합** 및 NPU 지원 연산자 분할 파이프라인 형성.
2. **텐서·온칩 버퍼 계획**: SRAM 메모리 맵핑 및 가중치 전송 최소화 Tiling 계획 구성.
3. **이기종 서브그래프 실행**: Conv/MatMul 레이어는 **NPU** 가속, Custom 연산자는 CPU/GPU fallback 수행.
4. **전력·열 피드백 제어**: NPU 발열 계측 및 **DVFS** 전력 조절 후 결과 래칭.

#### 한줄 요약

- 모델 컴파일·연산자 분할, 텐서·온칩 버퍼 계획, 전력·열 피드백 제어를 함께 최적화해야 지속 추론 성능을 유지할 수 있다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Cloud AI**: 서버급 GPU/TPU 어레이 및 무제한 전력을 바탕으로 대규모 초거대 모델(LLM 등)을 추론하는 방식.

</details>

| 비교 항목 | On-Device AI (SoC NPU) | Cloud AI (Data-Center GPU) |
|:---|:---|:---|
| 연산 위치 | 단말기 소형 **SoC** 단독 (로컬 단말) | 데이터센터 중앙 서버 (클라우드 파이프라인) |
| 반응 지연 (Latency) | 초저지연 (실시간 응답, <10ms) | 통신 지연 발생 (100ms ~ 수 초) |
| 개인정보 보안 | 완벽한 보안 (데이터 로컬 수용) | 데이터 송신 시 유출 위험성 상존 |
| 연산/전력 자원 | **TDP** 제한 (배터리/소형 발열 한계) | 무제한 전력 수용 및 초대형 모델 연산 |

#### 한줄 요약

- 개인정보와 지연 요구를 전력·온도 한도 안에서 만족하면 단말에서 추론하고, 자원 한도를 넘는 모델은 클라우드와 분담한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Fallback**: NPU 컴파일러가 새로 추가된 미지원 커스텀 레이어 수용 시 CPU/GPU 코어로 처리를 이관하는 예외 처리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NPU 미지원 딥러닝 연산자 포함 시 **Fallback** 오버헤드 | 컴파일러 커스텀 커널 업데이트 및 CPU/GPU 오프로드 | 모델 실행 끊김 방지 |
| LPDDR DRAM 메모리 대역폭 부족에 따른 NPU 유휴 | INT8/INT4 **양자화** 및 **SRAM Tiling** | 메모리 병목 완전 해소 |
| 런타임 연속 연산 시 단말 발열 스로틀링 발생 | **DVFS** 제어 및 NPU 전력 효율(TOPS/W) 극대화 | 무중단 온디바이스 추론 달성 |

> 사례: 45 TOPS NPU 탑재 **SoC AI 칩셋** 기반 온디바이스 LLM/비전 추론 실증

#### 한줄 요약

- 자원 프로파일러로 연산자, 메모리 대역폭, 열 스로틀링을 함께 검증한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **On-Device AI 선택 기준(On-Device AI Selection Criteria)**: 텐서 연산 지원성, NPU TOPS/Watt 효율, 메모리 대역폭 및 TDP 범위에 기반한 아키텍처 수립 체계.

</details>

- **On-Device AI 선택 기준**에 따라 실시간 비전/음성 및 개인정보 보호 필요 시 **SoC AI 온디바이스 칩** 채택

#### 한줄 요약

- 지속 전력•개인정보•응답시간 요구를 모두 충족할 수 있을 때 온디바이스 AI를 선택한다.
