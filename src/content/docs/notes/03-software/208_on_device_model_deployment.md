---
sidebar:
  order: 208
  label: "208. 온디바이스 AI 모델 배포: LiteRT•ONNX"
  badge:
    text: "기출 · 85%"
    variant: note
title: "온디바이스 AI 모델 배포: LiteRT•ONNX (On-Device Model Deployment)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 208
extra:
  question_no: "208"
  source_status: "기출"
  source_history: "134회"
  priority: 85
  priority_note: "기기 추론•경량화•배포가 최근 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **온디바이스 AI 배포 (On-Device Deployment)**: 양자화·경량화된 모델을 모바일 및 엣지 단말 NPU에 탑재하여 로컬에서 실시간 추론을 수행하는 기술.
- **LiteRT (구 TensorFlow Lite) & ONNX Runtime**: 단말 하드웨어 가속기(NPU/GPU)를 직접 제어하는 크로스 플랫폼 초경량 추론 런타임.

</details>

- 정의/개념: 경량화된 AI 모델을 모바일 및 엣지 단말에 탑재하여 **네트워크 연결 없이 로컬 하드웨어에서 실시간 추론을 수행하는 온디바이스 배포 기술**
- 배경/필요성: 클라우드 중앙 추론 시 발생하는 **네트워크 전송 지연, 서버 API 인프라 비용 폭증 및 개인정보 외부 유출 해결 불가**

#### 한줄 요약
- INT8 양자화, LiteRT/ONNX 런타임, 안전한 OTA 배포를 통해 초저지연 온디바이스 AI를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Quantization (양자화: FP32 $\to$ INT8)**: 부동소수점 가중치를 8비트 정수로 압축하여 모델 크기를 75% 절감하고 NPU 연산 속도를 극대화.
- **Hardware Delegate (하드웨어 델리게이트)**: 추론 연산자를 단말 NPU(NNAPI, CoreML) 전용 가속 명령어로 매핑하는 드라이버 인터페이스.

</details>

- 네트워크 오프라인 상태에서도 10ms 이내 실시간 동작하는 **초저지연 오프라인 추론**
- 단말기 내부에서만 데이터를 처리하여 외부 유출을 원천 차단하는 **강력한 프라이버시 보호**
- 이기종 하드웨어 가속기(NPU, GPU, DSP)를 활용하는 **하드웨어 델리게이트 가속**

#### 한줄 요약
- 초저지연 오프라인 추론, 완벽한 프라이버시, NPU 하드웨어 가속을 통해 단말 성능을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **온디바이스 배포 4대 아키텍처**: Cloud Optimization(양자화/컴파일), OTA Controller(무선 배포), On-Device Runtime(LiteRT), Hardware NPU(가속 엔진).

</details>

```text
[온디바이스 AI 모델 변환, OTA 배포 및 엣지 실행 아키텍처]
|-- 1. Cloud Model Optimization (PyTorch -> INT8 QAT 양자화 -> LiteRT / ONNX 변환)
|-- 2. OTA Model Distribution (단말 사양별 바이너리 매핑 + 비대칭 전자서명 검증)
`-- 3. Edge Device Execution Environment
    |-- 4. Inference Runtime: LiteRT / ONNX Runtime (Operator Graph 파싱 및 델리게이트)
    `-- 5. Hardware Acceleration Layer: NPU (INT8 텐서 가속) / GPU (FP16) / CPU Fallback
```

선의 의미: 계층 및 클라우드에서 경량화되어 서명된 모델이 단말 추론 런타임에 로드되어 NPU/GPU 가속기를 통해 실시간 추론되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **경량화 변환기 (Optimization)**| 원본 모델을 **INT8 양자화(PTQ/QAT), 가지치기하여 LiteRT/ONNX 표준 포맷으로 변환**| LiteRT Converter |
| **추론 런타임 (Runtime)** | 모델 그래프를 파싱하고 **연산자를 분석하여 NPU/GPU 델리게이트에 최적 분배 실행** | ONNX Runtime, LiteRT |
| **하드웨어 가속기 (NPU)** | 단말 내부 칩셋에서 **초당 수십조 회(TOPS)의 병렬 텐서 연산을 저전력으로 처리** | NPU / CoreML |
| **온디바이스 앱 (Device App)** | 카메라, 마이크 센서 입력을 전처리하고 **추론 결과를 즉각 로컬 비즈니스에 반영** | 오프라인 앱 |
| **OTA 제어기 (Distribution)** | 기기 사양별 모델 바이너리를 **Canary 방식으로 무선 배포하고 오류 시 즉시 롤백** | 안전한 OTA 배포 |

#### 한줄 요약
- 경량화 변환기, 추론 런타임, NPU 가속기, 단말 앱, OTA 제어기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **온디바이스 배포 5단계**: INT8 양자화 변환 $\to$ Device Farm 실기기 검증 $\to$ 암호화 서명 등록 $\to$ 카나리 OTA 배포 $\to$ 발열/크래시 모니터링.

</details>

```text
온디바이스 AI 모델 경량화 및 배포 파이프라인
        │
   1. [양자화 변환] PyTorch 객체 검출 모델을 QAT를 거쳐 500MB에서 45MB 크기 LiteRT로 압축
        │
   2. [디바이스 팜 검증] Device Farm 실기기 50대에서 추론 속도(15ms) 및 배터리 소모량 측정
        │
   3. [암호화 서명 등록] 변조 방지를 위해 비대칭 키로 전자서명하고 기종별 패키지 분리 등록
        │
   4. [카나리 OTA 배포] 백그라운드 Wi-Fi 연결 시 전체 단말의 5%에만 신규 모델 조용히 다운로드
        │
   5. [텔레메트리 관측] NPU 크래시 및 배터리 발열 지표 정상을 확인하고 전사 100% 확대 배포
```

#### 한줄 요약
- 양자화 변환 → 기기 검증 → 암호화 서명 → 카나리 배포 → 텔레메트리 관측 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **On-Device vs Cloud vs Hybrid 추론**: 단말 단독 실행(On-Device), 서버 전송 실행(Cloud), 상황별 동적 분기(Hybrid).

</details>

| 비교 항목 | 온디바이스 추론 (On-Device AI) | 클라우드 추론 (Cloud AI) | 하이브리드 추론 (Hybrid AI) |
|:---|:---|:---|:---|
| 핵심 적용 기준 | **오프라인 음영 지역, 초저지연 제어, 민감 데이터**| **초대형 파운데이션 모델(70B+), 고성능 연산** | **단말 사양 편차 극복, 질문 복잡도별 분기**|
| 네트워크 의존도 | **전무 (0ms 전송 지연, 완전 오프라인)** | 필수 (수백 ms 네트워크 레이턴시 발생) | 단말 1차 처리 후 필요시 클라우드 호출 |
| 프라이버시 보호 | **최고 (단말 외부로 데이터 일체 미전송)** | 보통~낮음 (서버로 민감 데이터 전송) | 민감 데이터는 단말 처리, 일반 질의만 전송 |
| 하드웨어 제약 | 단말 NPU 메모리 및 배터리 발열 제약 | 클라우드 GPU 확장으로 제약 없음 | 단말 경량 모델과 클라우드 대형 모델 연계 |

#### 한줄 요약
- 초저지연과 프라이버시는 온디바이스, 초대형 연산은 클라우드, 비용과 품질 균형은 하이브리드를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **QAT (Quantization-Aware Training)**: 양자화로 인한 소수점 정밀도 손실을 학습 과정에서 미리 시뮬레이션하여 정확도 저하를 1% 미만으로 방어하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 양자화 압축으로 원본 대비 모델 정확도 급락 | **단순 사후 양자화(PTQ) 대신 `양자화 인지 학습(QAT)` 의무 적용** | 원본 대비 99% 이상 정확도 유지 |
| 안드로이드/iOS 수백 개 칩셋 파편화로 특정 NPU 크래시 | **실제 기기 기반 `Device Farm` 자동화 호환성 회귀 테스트 수행** | 단말 크래시율 0% 달성 |
| 배포된 온디바이스 모델 파일의 탈취 및 리버스 엔지니어링 | **모델 가중치 AES 암호화 및 `Secure Enclave / KeyStore` 복호화** | AI 지식재산권(IP) 완벽 보호 |
| 잦은 대용량 모델 업데이트로 인한 사용자 모바일 데이터 낭비 | **차분 업데이트(Delta Update) 및 Wi-Fi 연결 시 자동 다운로드** | 사용자 데이터 비용 및 이탈 방지 |

#### 한줄 요약
- QAT 적용, 디바이스 팜 테스트, 모델 가중치 암호화, 차분 업데이트로 운영한다.

## Ⅶ. 결론

- 클라우드 인프라 비용을 절감하고 데이터 주권과 즉각적 반응성을 실현하기 위해 **PyTorch 모델의 INT8 QAT 양자화와 LiteRT/ONNX 표준 포맷 변환을 의무화**하고, **Device Farm 기반의 칩셋 호환성 검증과 안전한 OTA 카나리 배포 거버넌스**를 결합하여 고성능 온디바이스 AI 생태계 완성

#### 한줄 요약
- 온디바이스 AI 배포는 모델 경량화, 크로스 플랫폼 런타임, OTA 카나리 배포를 통해 네트워크 없이 초저지연과 프라이버시를 보장하는 핵심 엣지 컴퓨팅 기술이다.