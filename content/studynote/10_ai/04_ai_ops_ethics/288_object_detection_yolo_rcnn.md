+++
title = "288. 객체 탐지 (Object Detection)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 객체 탐지(Object [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))는 이미지 내 모든 객체의 **[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/))와 위치(Localization)**를 동시에 수행하며, 1단계 탐지기(YOLO, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))와 2단계 탐지기(R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))의 정확도-속도 트레이드오프가 핵심이다.
> 2. **가치**: 자율주행, 보안 카메라, 의료 영상 등 실시간·고정밀 탐지가 모두 필요한 현장에서 YOLO와 R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 계열은 각각의 강점으로 보완적으로 사용된다.
> 3. **판단 포인트**: 시험에서는 IoU (Intersection over Union) 계산, NMS (Non-Maximum Suppression)의 역할, 앵커 박스(Anchor Box) 개념, mAP (mean Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) 평가 지표, 1단계 vs 2단계 탐지기의 속도·정확도 비교를 묻는다.

---

## Ⅰ. 개요 및 필요성

### 객체 탐지의 정의와 난이도

단순 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/))는 "이 이미지에 무엇이 있나?"를 답하지만, 객체 탐지(Object [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))는 **"무엇이, 어디에, 몇 개나 있나?"** 를 동시에 답해야 한다.

탐지가 어려운 이유:
1. **다중 객체**: 한 이미지에 수십 개의 객체가 존재
2. **다양한 크기**: 작은 보행자부터 큰 트럭까지 동시 탐지
3. **클래스 불균형**: 객체보다 배경이 압도적으로 많음
4. **실시간 요구**: 자율주행에서 30 FPS 이상 필요

### 핵심 서브 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)

| [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) | 입력 | 출력 | 예시 |
|:---|:---|:---|:---|
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) ([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) | 이미지 | 클래스 레이블 | "고양이" |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)+위치 추정 (Localization) | 이미지 | 클래스 + 바운딩 박스 1개 | "고양이, (x,y,w,h)" |
| 객체 탐지 (Object [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) | 이미지 | N개의 클래스+바운딩 박스 | "고양이, 개, 자동차 각 위치" |
| 인스턴스 분할 (Instance [Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)) | 이미지 | 클래스+박스+픽셀 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)크 | Mask R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 "사진에 고양이 있어?"라면, 객체 탐지는 "어디에 몇 마리나 있어?"다. 넓은 사진에서 수십 개 객체를 동시에 찾고 박스를 쳐야 하니 훨씬 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념: IoU, NMS, 앵커 박스

**IoU (Intersection over Union)**:
두 바운딩 박스의 겹침 정도를 0~1로 표현한다. 일반적으로 IoU > 0.5이면 정탐(True Positive)으로 판정.

```
┌──────────────────────────────────────────┐
│  예측 박스 (Predicted Box)               │
│  ┌──────────────────┐                   │
│  │         ┌────────┼───────┐            │
│  │         │ 교집합 │       │            │
│  │         │(Inter- │  GT   │            │
│  └─────────┼section)│  Box  │            │
│            └────────┴───────┘            │
│                                          │
│  IoU = 교집합 넓이 / 합집합 넓이         │
│      = Intersection / Union              │
└──────────────────────────────────────────┘
```

**NMS (Non-Maximum Suppression)**:
동일 객체에 대해 여러 겹치는 박스가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)될 때, **가장 높은 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)([Confidence](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/))의 박스만 남기고** IoU > 임계값인 나머지를 제거한다.

```
NMS 동작 순서:
1. 신뢰도 점수 내림차순 정렬
2. 최고 점수 박스 선택
3. 나머지 중 IoU > 0.5인 박스 모두 제거
4. 남은 박스로 2~3 반복
```

**앵커 박스 (Anchor Box)**:
다양한 크기와 종횡비(Aspect Ratio)의 사전 정의된 박스들. 모델은 실제 객체 위치를 앵커 박스 대비 오프셋(Offset)으로 예측한다.

### 2단계 탐지기: R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 계열

```
R-CNN 계열 발전 과정:

R-CNN (2014)
    │  입력 이미지
    │  → Selective Search (영역 제안 ~2000개)
    │  → 각 영역 CNN 특징 추출 (개별 처리)
    │  → SVM 분류 + 박스 회귀
    │  속도: 47초/이미지 (느림)
    ▼
Fast R-CNN (2015)
    │  입력 이미지 → CNN 전체 특징 맵
    │  → RoI Pooling (영역별 특징 추출)
    │  → FC + 분류 + 회귀
    │  속도: 2초/이미지
    ▼
Faster R-CNN (2015)
    │  입력 이미지 → CNN 특징 맵
    │  → RPN (Region Proposal Network, 학습 가능)
    │  → RoI Pooling → 분류 + 회귀
    │  속도: 0.2초/이미지 (5 FPS)
    │  정확도: mAP ~70% (PASCAL VOC)
```

### 1단계 탐지기: YOLO

YOLO (You Only Look Once)는 이미지를 S×S 그리드로 나누고, **한 번의 [순전파](/knowledge-base/studynote/10_ai/03_llm_nlp/271_forward_propagation/)**로 모든 셀에서 바운딩 박스와 클래스 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)을 동시에 예측한다.

```
YOLO 아키텍처 (YOLOv1 기준):

입력 이미지 (448×448)
        │
   CNN 백본
  (24개 합성곱층)
        │
   출력 텐서: S×S×(B×5 + C)
   S=7 (그리드 크기)
   B=2 (셀당 박스 수)
   C=20 (클래스 수, PASCAL VOC)
        │
  7×7×30 텐서
        │
   각 셀의 예측:
   ┌────────────────────────────────┐
   │ 박스1: x, y, w, h, confidence │
   │ 박스2: x, y, w, h, confidence │
   │ 클래스 확률: P(C1)...P(C20)   │
   └────────────────────────────────┘
        │
      NMS 적용
        │
   최종 탐지 결과
```

### 1단계 vs 2단계 탐지기 비교

| 비교 항목 | 1단계 탐지기 (YOLO, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) | 2단계 탐지기 (Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)) |
|:---|:---|:---|
| 처리 방식 | 단일 [순전파](/knowledge-base/studynote/10_ai/03_llm_nlp/271_forward_propagation/) | 영역 제안 → [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 2단계 |
| 속도 | 빠름 (30~100 FPS) | 느림 (5~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) FPS) |
| 정확도 | 상대적으로 낮음 (특히 소형) | 높음 |
| 소형 객체 탐지 | 취약 | 우수 |
| 실시간 적용 | 가능 | 제한적 |
| 사용 예 | 자율주행, [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 실시간 | 의료 영상, 정밀 검사 |

- **📢 섹션 요약 비유**: YOLO는 '한 번에 사진 전체를 훑는 빠른 탐정', R-CNN은 '의심 구역을 하나씩 꼼꼼히 조사하는 형사'다. 빠른 답이 필요하면 YOLO, 정확한 답이 필요하면 R-CNN이다.

---

## Ⅲ. 비교 및 연결

### YOLO [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)별 발전

| [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | 핵심 개선 | 속도 | mAP |
|:---|:---|:---:|:---:|
| YOLOv1 (2015) | 그리드 기반 1단계 탐지 | 45 FPS | 63.4% |
| YOLOv2 (2016) | 앵커 박스, Batch Norm | 67 FPS | 78.6% |
| YOLOv3 (2018) | 다중 스케일 예측, DarkNet-53 | 30 FPS | 33.0 mAP |
| YOLOv4 (2020) | [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/), PANet, Mosaic Aug | 65 FPS | 43.5 mAP |
| YOLOv5/v8 | 경량화, 엔지니어링 최적화 | 140+ FPS | 50+ mAP |

### [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) (Single Shot Multibox Detector)와의 비교

[SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) (Single Shot Multibox Detector)는 다양한 크기의 특징 맵에서 다중 스케일 앵커 박스를 예측하여 소형 객체 탐지를 YOLO보다 개선했다.

```
SSD 다중 스케일 예측:
38×38  ─ 소형 객체 탐지
19×19  ─ 중형 객체 탐지
10×10  ─ 대형 객체 탐지
 5×5   ─ 더 큰 객체
 3×3   ─ 매우 큰 객체
 1×1   ─ 전체 이미지 크기 객체
```

### mAP (mean Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) 평가 지표

mAP (mean Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))는 객체 탐지 모델의 표준 평가 지표다:

1. **[Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)-[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 곡선** 계산 ([신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 임계값 변화에 따라)
2. **[AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) (Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))** = [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 곡선 아래 면적 (클래스별)
3. **mAP** = 모든 클래스의 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 평균

COCO 평가에서는 `mAP@[0.5:0.05:0.95]`(IoU 0.5~0.95 평균)를 사용한다.

- **📢 섹션 요약 비유**: mAP는 '탐지 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 종합 성적표'다. 얼마나 정확하게([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) 얼마나 빠짐없이([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)) 탐지했는지를 모든 클래스에 걸쳐 평균 낸 점수다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 응용 분야별 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택

| 응용 분야 | 요구 사항 | 권장 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
|:---|:---|:---|
| 자율주행 ([Autonomous Driving](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/416_autonomous_driving_lidar_sae_level/)) | 실시간, 고속 | YOLOv4/v5, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) |
| [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 이상 행동 탐지 | 실시간, 경량 | YOLOv8-Nano, MobileNet-[SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) |
| 의료 영상 종양 탐지 | 높은 정확도 | Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), Mask R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) |
| 위성 [이미지 분석](/knowledge-base/studynote/16_bigdata/05_analysis/118_image_analysis/) | 소형 객체, 정밀 | Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) + FPN |
| 산업 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 검출 | 정밀, 설명 가능 | Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) |

### 현대 트렌드: [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 탐지기

DETR ([DEtection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) [TRansformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/), Facebook [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 2020)은 NMS와 앵커 박스 없이 **[트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))의 [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/)([Attention Mechanism](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/))**으로 객체를 [End-to-End](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) 탐지한다.

```
DETR 파이프라인:
이미지 → CNN 백본 → 플래튼 → 트랜스포머 인코더
→ N개 쿼리 + 트랜스포머 디코더 → N개 예측 (클래스+박스)
(N = 100, 빈 예측은 "No Object"로 처리)
```

### 기술사 서술 포인트

> "객체 탐지에서 1단계 탐지기(YOLO)는 단일 [순전파](/knowledge-base/studynote/10_ai/03_llm_nlp/271_forward_propagation/)로 실시간 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성하는 반면, 2단계 탐지기(Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))는 별도 영역 제안 네트워크(RPN)로 정확도를 높인다. IoU로 탐지 품질을 측정하고 NMS로 중복 제거 후 mAP로 최종 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 평가한다. 최근 DETR은 [트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)로 앵커와 NMS를 없애는 방향으로 발전하고 있다."

- **📢 섹션 요약 비유**: 실무 선택은 '배달 상황'과 같다. 치킨을 빠르게 배달해야 한다면 오토바이(YOLO), 귀중한 의료 장비를 정확히 배달해야 한다면 전문 운송 트럭(Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))이다. 상황에 맞는 도구가 정답이다.

---

## Ⅴ. 기대효과 및 결론

### 객체 탐지 기술의 핵심 가치

1. **자동화**: 사람이 직접 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 했던 영상 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링을 AI가 대체
2. **실시간성**: YOLO 계열로 30~140 FPS 실시간 탐지 가능
3. **정밀성**: Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) + FPN으로 소형·밀집 객체까지 고정밀 탐지

### 탐지기 선택 프레임워크

```
┌──────────────────────────────────────────────────────────┐
│              탐지기 선택 기준                            │
│                                                          │
│  실시간 처리 필요?                                       │
│      ├── Yes → 1단계 탐지기 (YOLO, SSD)                 │
│      └── No  → 2단계 탐지기 (Faster R-CNN)             │
│                                                          │
│  소형 객체 많음?                                         │
│      ├── Yes → FPN 결합 탐지기 / SSD 다중 스케일        │
│      └── No  → 표준 YOLO 또는 R-CNN                     │
│                                                          │
│  Annotation 비용?                                        │
│      ├── 박스만 → 일반 탐지기                           │
│      └── 픽셀 마스크 → Mask R-CNN                       │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 객체 탐지는 '[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 감시 요원 배치'다. 화면을 빠르게 훑는 YOLO 요원은 위급 상황에 즉각 대응하고, 꼼꼼히 조사하는 R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 요원은 증거를 철저히 수집한다. 임무 성격에 맞는 요원을 선택해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| IoU (Intersection over Union) | 바운딩 박스, 정탐 판정 / 탐지 품질 측정 기준 |
| NMS (Non-Maximum Suppression) | 중복 박스 제거, 후처리 / 최종 탐지 정제 |
| 앵커 박스 (Anchor Box) | 사전 정의 박스, 오프셋 / YOLO/[SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)/Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 공통 |
| mAP (mean Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/), [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 곡선, COCO / 탐지 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 표준 평가 지표 |
| YOLO (You Only Look Once) | 1단계, 실시간 / 속도 우선 탐지기 |
| Faster R-[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) | RPN, 2단계, 정확도 / 정확도 우선 탐지기 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] → [객체 탐지 (Object Detection)] → [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 객체 탐지는 '사진 속 숨은 그림 찾기'야. 고양이가 어디 있는지, 개가 어디 있는지 상자(바운딩 박스)로 표시해주는 거야.
2. YOLO는 '눈 빠른 친구'야. 사진 전체를 순식간에 훑어서 빠르게 "고양이는 여기, 개는 저기!"라고 외쳐. 자율주행 차는 이런 친구가 필요해.
3. IoU는 내가 그린 상자와 정답 상자가 얼마나 겹치는지 점수야. 1.0이면 완벽하게 맞은 거고, 0이면 전혀 못 찾은 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 288 / 420

← **이전**: [287. ResNet (Residual Network)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/)
**다음**: [289. 이미지 분할 (Image Segmentation)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/289_image_segmentation/) →

---
