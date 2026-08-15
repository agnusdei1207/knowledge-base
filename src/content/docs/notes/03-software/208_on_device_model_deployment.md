---
sidebar:
  order: 208
  label: "208. 온디바이스 AI 모델 배포: LiteRT•ONNX (On-Device Model Deployment)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "온디바이스 AI 모델 배포: LiteRT•ONNX (On-Device Model Deployment)"
date: "2026-08-14T06:05:00+09:00"
tags: ["notes-software"]
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

- **On-Device Model Deployment**: 경량 Model과 Runtime을 단말에 설치해 내부에서 추론하는 방식
- **Offline Inference**: Network 연결 없이 단말 Model로 수행하는 추론

</details>

- 정의/개념: 경량 AI Model을 단말에 배포해 내부 추론하는 **기술**
- 배경/필요성: Cloud 추론의 **Network 지연•전송 비용•Privacy 노출** 발생

#### 한줄 요약

- 제한된 자원에서 저지연•Offline•**Privacy 보존 추론** 제공

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **LiteRT**: Mobile•Embedded Device용 Google ML 추론 Runtime
- **ONNX (Open Neural Network Exchange)**: ML Framework 간 Model 교환 표준

</details>

- **Quantization**: FP32를 INT8 등으로 변환해 크기•연산 감소
- **Pruning**: 영향이 작은 연결을 제거해 Parameter 축소
- **가속기 활용**: CPU•GPU•NPU에 지원 연산자 배치
- **OTA 운영**: Canary 배포와 Rollback•Cloud Fallback 적용

#### 한줄 요약

- 압축•표준 Format•가속기•OTA로 **단말 제약** 극복

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Device Inference Runtime**: Model Graph를 해석해 지원 가속기에 연산을 배치하는 Engine

</details>

```text
[On-Device AI]
 ├── [경량 Model Package | Weight•Operator•서명]
 ├── [Inference Runtime | Graph•가속기 Interface]
 ├── [CPU•GPU•NPU | Tensor 연산]
 ├── [On-Device App | Sensor•전처리•업무 Logic]
 └── [배포•관측 제어기 | OTA•Telemetry•Rollback]
```

| 구성요소 | 책임 |
|---|---|
| 경량 Model Package | Weight•Operator•서명•**Version** 보관 |
| Inference Runtime | Graph 최적화와 **가속기 Interface** 제공 |
| CPU•GPU•NPU | 특성별 **Tensor 연산** 수행 |
| On-Device App | Sensor 전처리•추론 호출•업무 Logic 실행 |
| 배포•관측 제어기 | OTA•Telemetry•**Rollback** 통제 |

#### 한줄 요약

- 경량 Package를 Runtime•가속기가 실행하고 **OTA 제어기**가 운영

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Device Farm**: 다양한 제조사•OS•Chipset 단말을 자동 시험하는 환경

</details>

```text
[학습 Model 입력]
          │
          ▼
[1. 경량 Model 후보 전달]
          │
          ▼
[2. 호환성•품질•자원 검증]
          │
          ▼
[3. 승인 Version 등록]
          │
          ▼
[4. 단계별 OTA 배포]
          │
          ▼
┌───[5. 지연•오류•전력 전달]───┐
│ 이상: Rollback•Cloud Fallback│
│ 정상: 배포 비율 확대         │
└───────────────────────────────┘
```

### 동작 원리

1. **경량 Model 후보 전달**: Quantization•Pruning•Format 변환
2. **호환성•품질•자원 검증**: 기기별 정확도•지연•Memory•전력 측정
3. **승인 Version 등록**: 기기 Tier별 Package와 복구 Version 매핑
4. **단계별 OTA 배포**: 서명된 Model을 Canary Ring에 배포
5. **지연•오류•전력 전달**: Telemetry로 확대•Rollback 결정

#### 한줄 요약

- 실제 기기 검증 후 Canary OTA와 **현장 지표**로 배포 통제

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hybrid Inference**: 요청 난이도•자원•품질에 따라 단말과 Cloud를 분기하는 방식

</details>

| 비교 항목 | On-Device | Cloud | Hybrid |
|---|---|---|---|
| 강점 | 저지연•Offline•Privacy | 대형 Model•중앙 갱신 | **자원별 동적 분기** |
| 제약 | Device 자원•파편화 | Network•비용•정보 전송 | 구현•출력 일관성 |
| 적용 | 민감•실시간 입력 | 고품질 대형 연산 | 기기 편차•복합 요청 |

#### 한줄 요약

- Privacy•지연•Model 규모•Network로 **추론 위치** 결정

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Accuracy Degradation (정확도 저하)**: 과도한 압축으로 원본 대비 예측 품질이 하락하는 현상

</details>

| 고려사항 | 대책 |
|---|---|
| Device별 NPU•Memory 편차 | 기기 Tier별 **Model Variant** 시험 |
| 압축에 따른 정확도 저하 | 대표 Data와 **QAT•허용 오차** 검증 |
| Model 탈취 | Weight 암호화•Keystore•**Secure Enclave** 적용 |
| OTA 오배포 | 서명•Canary•**Automatic Rollback** 연계 |

#### 한줄 요약

- 기기별 품질•자원•보안•복구를 검증해 **현장 장애** 제한

## Ⅶ. 결론

<details><summary>쉽게 이해하기 (학습용)</summary>

- 단말 자원과 Privacy가 충분하면 내부 처리하고, 복잡한 요청은 Cloud로 넘긴다.

</details>

- Privacy•저지연은 **On-Device**, 자원•품질 한계는 Hybrid Fallback 적용
