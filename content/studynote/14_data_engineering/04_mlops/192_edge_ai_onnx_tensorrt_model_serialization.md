+++
title = "192. 엣지 AI 컴파일러 (Edge AI - ONNX, TensorRT) 모델 직렬화 패키징 배포망"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 엣지 AI는 모델을 클라우드 대신 엣지 디바이스에서 추론하여 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없는 실시간 처리와 오프라인 동작을 실현한다.
> 2. **가치**: ONNX(Open Neural Network Exchange)는 프레임워크 독립적 모델 교환 포맷이고, TensorRT는 NVIDIA GPU에서 레이어 융합·[양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)로 추론 속도를 최대 8배 향상한다.
> 3. **판단 포인트**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)), 비용(Cost), 프라이버시(Privacy), 연결성(Connectivity) 4가지 기준으로 클라우드 vs 엣지 추론을 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([Edge AI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/174_edge_ai_on_device_ai/)) 정의

엣지 AI는 딥러닝 추론(Inference)을 클라우드 서버가 아닌 <strong>엣지 디바이스(스마트폰, <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 센서, 카메라, 자동차 ECU)</strong> 에서 직접 수행하는 패러다임이다.

### 1.2 클라우드 vs 엣지 추론 비교

| 항목 | 클라우드 추론 | 엣지 추론 |
|:---|:---|:---|
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 100ms ~ 1s (네트워크 포함) | 1ms ~ 10ms |
| 프라이버시 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 서버로 전송 | 로컬 처리, 전송 없음 |
| 비용 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서버 임대비 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 하드웨어 비용 |
| 연결성 | 상시 네트워크 필요 | 오프라인 동작 가능 |
| 모델 업데이트 | 즉시 반영 | OTA([Over-the-Air](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) 배포 필요 |
| 연산 한계 | 무제한 스케일 | 디바이스 리소스 제한 |

### 1.3 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 파이프라인 개요

```
모델 학습 (Cloud)
    │
    ▼
모델 변환/최적화
 (ONNX / TensorRT / TFLite / OpenVINO)
    │
    ▼
패키징 (Docker Edge Runtime / OCI)
    │
    ▼
배포망 (OTA Update / Edge Orchestration)
    │
    ▼
엣지 디바이스에서 추론 실행
```

📢 **섹션 요약 비유**: 엣지 AI는 "현장 출장 의사"와 같다. 병원(클라우드)까지 갈 필요 없이 현장에서 즉시 진단(추론)하고, 환자 정보([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 외부로 내보내지 않아 프라이버시도 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 ONNX (Open Neural Network Exchange)

ONNX는 Microsoft와 Facebook이 공동 개발한 <strong>프레임워크 독립적 모델 교환 표준 포맷</strong>이다. PyTorch, TensorFlow, MXNet 등 다양한 프레임워크 모델을 동일 포맷으로 표현한다.

```
PyTorch 모델 (.pth)
    │ torch.onnx.export()
    ▼
┌─────────────────────┐
│   ONNX 모델 (.onnx) │
│   - 연산자 그래프    │
│   - 가중치(Weight)  │
│   - 입출력 명세      │
└──────────┬──────────┘
           │
    ┌──────┴────────────────────────┐
    │                               │
    ▼                               ▼
ONNX Runtime             TensorRT 변환
(CPU/GPU 범용 추론)        (NVIDIA GPU 최적화)
    │                               │
    ▼                               ▼
Intel OpenVINO           .engine 파일
ARM NN                   최고 성능 추론
TFLite (변환)
```

#### ONNX 주요 특징

| 특징 | 설명 |
|:---|:---|
| 표준 연산자 집합 | 150+ 표준 연산자 정의 |
| [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 | opset [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지 |
| 커스텀 연산자 | 프레임워크별 확장 가능 |
| [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/) | 연산별 실행 시간 측정 |

### 2.2 TensorRT (NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 최적화 추론 엔진)

TensorRT는 NVIDIA가 개발한 고성능 딥러닝 추론 라이브러리로, ONNX 모델을 GPU에 최적화된 엔진으로 컴파일한다.

```
ONNX 모델 입력
    │
    ▼
┌───────────────────────────────────────┐
│         TensorRT 최적화 단계           │
│                                       │
│  1. 레이어 융합 (Layer Fusion)         │
│     Conv + BN + ReLU → 단일 커널       │
│                                       │
│  2. 정밀도 캘리브레이션 (Calibration)  │
│     FP32 → FP16 / INT8 양자화         │
│     대표 데이터셋으로 임계값 결정       │
│                                       │
│  3. 커널 자동 선택 (Kernel Autotuning) │
│     GPU 아키텍처별 최적 커널 선택       │
│                                       │
│  4. 메모리 최적화 (Memory Optimizer)   │
│     텐서 메모리 재사용, 레이아웃 최적화 │
└───────────────────────┬───────────────┘
                        │
                        ▼
              .engine 파일 생성
              (특정 GPU에 최적화)
```

#### TensorRT [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 모드 비교

| 모드 | 메모리 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 정확도 손실 |
|:---|:---|:---|:---|
| FP32 (기본) | 4 bytes/값 | [1x](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/584_802_1x_pnac_eap_radius/) | 없음 |
| FP16 | 2 bytes/값 | 2~3x | 미미 |
| INT8 | 1 [byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)/값 | 3~4x | 주의 필요 |
| INT4 | 0.5 bytes/값 | 4~8x | 높음 |

### 2.3 모델 경량화 기법

```
┌─────────────────────────────────────────────────┐
│              모델 경량화 4대 기법                  │
│                                                 │
│  ┌───────────────┐  ┌───────────────┐           │
│  │ 양자화        │  │ 가지치기       │           │
│  │(Quantization)│  │(Pruning)      │           │
│  │ FP32 → INT8  │  │ 불필요 뉴런    │           │
│  │ 연산 정밀도 감소│  │ 가중치 제거  │           │
│  └───────────────┘  └───────────────┘           │
│                                                 │
│  ┌───────────────┐  ┌───────────────┐           │
│  │ 지식 증류     │  │ 아키텍처 탐색  │           │
│  │(Distillation) │  │(NAS)          │           │
│  │ 큰 모델 → 작은│  │ 경량 모델 자동 │           │
│  │ 모델로 지식전달│  │ 설계          │           │
│  └───────────────┘  └───────────────┘           │
└─────────────────────────────────────────────────┘
```

### 2.4 주요 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 런타임

| 런타임 | 개발사 | 타겟 하드웨어 | 특징 |
|:---|:---|:---|:---|
| ONNX Runtime | Microsoft | CPU/[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)/[NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) | 범용, 크로스플랫폼 |
| TensorRT | NVIDIA | NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) | 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| TFLite | Google | ARM/Cortex-M | 초경량 MCU |
| OpenVINO | Intel | Intel CPU/VPU | Intel 최적화 |
| CoreML | Apple | Apple Silicon | iOS/macOS |
| TorchScript | Meta | 범용 | PyTorch 모바일 |

📢 **섹션 요약 비유**: TensorRT는 외국 요리 레시피(ONNX)를 받아서 우리 주방(NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) 환경에 완벽히 최적화하는 전담 요리사다. 같은 레시피라도 주방 도구와 재료 배치를 최적화해 요리 시간(추론 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))을 대폭 줄인다.

---

## Ⅲ. 비교 및 연결

### 3.1 모델 배포망 전체 아키텍처

```
┌────────────────────────────────────────────────────────┐
│                   엣지 AI 배포망                         │
│                                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              클라우드 (Model Registry)            │   │
│  │  MLflow / DVC / Vertex AI Model Registry         │   │
│  │  학습된 모델 버전 관리 + A/B 테스트               │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │ OTA(Over-the-Air) 배포        │
│                ┌────────┴────────┐                     │
│                │                 │                     │
│   ┌────────────▼────┐  ┌────────▼──────────┐          │
│   │  엣지 게이트웨이 │  │  엣지 게이트웨이   │          │
│   │ (공장 서버)      │  │ (자동차 ECU)       │          │
│   │ ONNX Runtime    │  │ TensorRT Engine   │          │
│   └────────┬────────┘  └────────┬──────────┘          │
│            │                    │                      │
│   ┌────────▼────┐      ┌────────▼────┐                │
│   │ IoT 센서    │      │ 카메라 모듈  │                │
│   │ TFLite      │      │ OpenVINO    │                │
│   └─────────────┘      └─────────────┘                │
└────────────────────────────────────────────────────────┘
```

### 3.2 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 최적화 흐름 (PyTorch → TensorRT)

```python
# 1. PyTorch 모델 → ONNX 변환
import torch
model = MyModel().eval()
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "model.onnx",
                  opset_version=17,
                  input_names=["input"],
                  output_names=["output"])

# 2. ONNX → TensorRT 변환 (trtexec 사용)
# trtexec --onnx=model.onnx --saveEngine=model.engine \
#         --fp16 --workspace=4096

# 3. TensorRT 엔진 추론
import tensorrt as trt
import numpy as np
# 엔진 로드 및 컨텍스트 생성으로 추론 실행
```

### 3.3 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) 방식 비교

| 방식 | 시점 | 정확도 | 구현 난이도 |
|:---|:---|:---|:---|
| PTQ (Post-[Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | 학습 후 | 중간 | 쉬움 |
| QAT ([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)-Aware [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) | 학습 중 | 높음 | 복잡 |
| Dynamic [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 런타임 | 낮음 | 매우 쉬움 |

📢 **섹션 요약 비유**: 모델 직렬화는 복잡한 요리 레시피를 특정 주방에 맞게 단순화하는 것이다. ONNX는 국제 표준 레시피 포맷이고, TensorRT는 NVIDIA 주방에서 가장 빠르게 요리할 수 있도록 재구성한 맞춤 레시피다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 도입 의사결정 프레임워크

```
추론 배포 위치 결정

지연 요구사항 < 10ms?
├─ YES → 엣지 추론 필수
│         (자율주행, 로봇 제어, 실시간 QA)
└─ NO  → 네트워크 연결 안정적?
          ├─ YES → 클라우드 추론 고려
          │         (비용 효율, 최신 모델)
          └─ NO  → 엣지 추론 필요
                    (공장 자동화, 원격지)

프라이버시 민감 데이터?
├─ YES → 엣지 추론 강력 권장
│         (의료 영상, 금융 데이터)
└─ NO  → 비용/성능 기준으로 선택
```

### 4.2 TensorRT 최적화 실전 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 단계 | 작업 | 도구 |
|:---|:---|:---|
| 1. 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | ONNX 연산자 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | onnx-checker |
| 2. [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/) | 레이어별 실행 시간 분석 | Nsight Systems |
| 3. 캘리브레이션 | INT8 대표 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 준비 | IInt8EntropyCalibrator |
| 4. 엔진 빌드 | GPU별 최적화 엔진 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | TensorRT [Builder](/knowledge-base/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/) |
| 5. 벤치마크 | [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)/[Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 측정 | trtexec --iterations=1000 |
| 6. 정확도 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | FP32 대비 정확도 손실 측정 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 |

### 4.3 실무 사례: 제조업 품질 검사

```
[카메라 → 엣지 서버 → 불량 탐지]

카메라 (30fps, 4K)
    │ 이미지 스트림
    ▼
NVIDIA Jetson AGX Xavier
  ├─ TensorRT Engine (YOLOv8-nano INT8)
  ├─ 추론 시간: 5ms/장
  ├─ 정확도: FP32 대비 99.2% 유지
  └─ 전력: 30W (클라우드 대비 1/100)

결과: 불량품 즉시 라인 제거 (100ms 이내 판단)
클라우드 업로드: 불량 케이스 샘플만 (데이터 90% 절감)
```

### 4.4 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안 고려사항

| 위협 | 대응 방법 |
|:---|:---|
| 모델 도난 | 모델 암호화 + TrustZone/[TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) |
| 적대적 공격(Adversarial) | 입력 전처리 방어, [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) |
| [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 변조 | 서명 기반 OTA 배포, 부트 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 | 온디바이스 처리, [차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/) |

📢 **섹션 요약 비유**: 엣지 AI는 중앙 서버에 의존하지 않는 "현장 전문가 파견"이다. 각 현장에 최적화된 전문가(TensorRT 엔진)를 파견해 빠르고 보안에 강한 처리를 수행하고, 중요한 케이스만 본사(클라우드)에 보고한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 도입 기대효과

| 효과 | 정량 지표 |
|:---|:---|
| 추론 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 감소 | 클라우드 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 감소 |
| 네트워크 비용 절감 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송량 80~95% 감소 |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상 | 오프라인 동작으로 99.99% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) |
| 프라이버시 강화 | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로컬 처리로 규제 준수 |
| 전력 효율 | 특수 하드웨어([NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)) 활용 시 10배 이상 |

### 5.2 기술 트렌드

```
엣지 AI 기술 발전 방향
┌─────────────────────────────────────────┐
│                                         │
│  현재: 모델 경량화 + 하드웨어 가속        │
│  ↓                                      │
│  단기: 연합 학습(Federated Learning)     │
│       엣지에서 분산 학습                  │
│  ↓                                      │
│  중기: 엣지 클라우드 협력 추론            │
│       (부분 추론 분산)                    │
│  ↓                                      │
│  장기: 자율 엣지 AI 에이전트              │
│       (학습 + 추론 + 자가 업데이트)       │
└─────────────────────────────────────────┘
```

### 5.3 결론 요약

ONNX는 딥러닝 모델의 이식성을 보장하는 표준 포맷이고, TensorRT는 NVIDIA GPU에서의 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 끌어내는 컴파일러다. 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포는 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 비용, 프라이버시의 균형점을 찾는 엔지니어링 최적화 문제이며, 기술사 관점에서는 <strong>하드웨어 선택 → 모델 최적화 → 배포망 설계 → 보안 강화</strong>의 4단계 프레임워크로 접근해야 한다.

📢 **섹션 요약 비유**: 엣지 AI는 대형 병원의 전문 장비(클라우드 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))를 작은 의료 가방(엣지 디바이스)에 압축하는 기술이다. 작아진 만큼 빠르고 어디서나 쓸 수 있으며, 환자 정보([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))도 병원 밖으로 나가지 않아 안전하다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 포맷 표준 | ONNX (Open Neural Network Exchange) | 프레임워크 독립적 모델 교환 포맷 |
| 추론 엔진 | TensorRT | NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 최적화 컴파일러 |
| 경량화 | [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | FP32→INT8 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 감소로 속도 향상 |
| 경량화 | [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) ([가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 불필요 뉴런 제거 |
| 경량화 | [Knowledge Distillation](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)) | 대형 모델 → 소형 모델 지식 전달 |
| 런타임 | ONNX Runtime | 크로스플랫폼 범용 추론 런타임 |
| 런타임 | TFLite | Google 초경량 모바일 런타임 |
| 배포 | OTA ([Over-the-Air](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) | 무선 모델 업데이트 |
| 보안 | [TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)) | 모델 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 실행 환경 |

### 👶 어린이를 위한 3줄 비유 설명

1. 엣지 AI는 공부 잘하는 친구([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델)를 여러 곳에 복사해서 파견하는 것이에요. 매번 선생님(클라우드)께 물어볼 필요 없이 현장에서 바로 답을 내줘요.

### 📈 관련 키워드 및 발전 흐름도

```text
클라우드 전용 추론 (지연 · 대역폭 비용)
    │
    ▼
엣지 AI: 디바이스에서 직접 추론
    ├─► 모델 변환: ONNX · TensorRT · TFLite
    ├─► 경량화: 양자화 (INT8) · 프루닝 · 지식 증류
    └─► 직렬화: FlatBuffers · Protocol Buffers
    │
    ▼
엣지 디바이스
    ├─► NVIDIA Jetson · Google Coral TPU
    ├─► 스마트폰 NPU · 라즈베리파이
    └─► WebAssembly (WASM) 추론
    │
    ▼
OTA 모델 업데이트 · 엣지-클라우드 연방 학습
```
2. ONNX는 여러 나라 음식 레시피를 하나의 표준 레시피 책으로 만드는 거예요. 어느 주방(디바이스)에서도 같은 책으로 요리(추론)할 수 있어요.
3. TensorRT는 요리사가 특정 주방(NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))에서 가장 빠르게 요리하도록 모든 동선을 최적화한 맞춤 레시피예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 192 / 258

← **이전**: [191. 람다/카파 아키텍처 재현 (Event Sourcing Replay - Lambda/Kappa Architecture)](/knowledge-base/studynote/14_data_engineering/04_mlops/191_event_sourcing_replay_lambda_kappa/)
**다음**: [193. 뉴로모픽 반도체 (Neuromorphic Chip) SNN 저전력 추론](/knowledge-base/studynote/14_data_engineering/04_mlops/193_neuromorphic_chip_snn_low_power_inference/) →

---
