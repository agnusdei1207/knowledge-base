---
sidebar:
  order: 55
  label: "055. 객체 탐지: YOLO•R-CNN (Object Detection)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "객체 탐지: YOLO•R-CNN (Object Detection)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-basic-theory"
weight: 55
extra:
  question_no: "055"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "탐지 구조 비교와 현장 적용"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **객체 탐지(Object Detection)**: 단일 이미지 내에 존재하는 다중 객체들의 클래스 범주(Classification)와 기하학적 위치를 바운딩 박스(Bounding Box: $x, y, w, h$)로 동시 예측하는 컴퓨터 비전 핵심 과업.
- **IoU(Intersection over Union)**: 예측된 바운딩 박스 $A$와 실제 정답 박스 $B$ 간의 교집합 면적을 합집합 면적으로 나눈 영역 중첩도 평가 지표 ($\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$).
- **mAP(mean Average Precision)**: 클래스별 정밀도-재현율(PR) 곡선 아래 면적인 AP를 모든 객체 클래스에 대해 산술 평균한 객체 탐지 표준 성능 척도.

</details>

- 정의/개념: 입력 영상에서 객체의 위치(Localization, 회귀)와 범주(Classification, 분류)를 동시에 추론하고 NMS로 중복을 제거하는 **딥러닝 시각 인지 파이프라인**
- 배경/필요성: 단순 이미지 분류(Classification)를 넘어 자율주행, 지능형 CCTV, 제조 결함 검사 등에서 **다중 객체의 공간적 좌표와 수량을 실시간으로 특정 필수**

#### 한줄 요약

- 이미지 내 다중 객체의 바운딩 박스 위치와 클래스 확률을 동시에 예측하고 평가

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NMS(Non-Maximum Suppression)**: 동일 객체에 대해 생성된 수많은 중복 후보 박스 중 신뢰도(Confidence Score)가 가장 높은 박스를 선택하고, $\text{IoU} \ge \text{Threshold}$인 나머지 박스를 억제하는 후처리 알고리즘.
- **FPN(Feature Pyramid Network)**: 백본의 저수준 고해상도 특징과 고수준 의미론적 특징을 Top-down 경로와 Lateral 연결로 결합하여 크기가 다른 다중 스케일 객체를 탐지하는 구조.

</details>

- 바운딩 박스 좌표 회귀($L_{box}$)와 클래스 분류($L_{cls}$) 및 객체성($L_{obj}$)의 **다중 손실(Multi-task Loss) 동시 최적화**
- FPN(Feature Pyramid) 도입을 통한 **소형(Small) 및 대형(Large) 객체의 강건한 탐지**
- 1-Stage(YOLO, SSD)의 **실시간성(Real-Time)** vs 2-Stage(Faster R-CNN)의 **초정밀도(High Precision) 분기**

#### 한줄 요약

- 다중 해상도 특징 피라미드로 다중 크기 객체를 탐지하고, NMS 후처리로 최적 박스만 보존

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **객체 탐지 3대 핵심 블록**:
  - Backbone: 원본 이미지에서 계층적 특징 추출 (CSPDarknet, ResNet).
  - Neck: 다중 해상도 피처 맵 융합 (FPN, PANet, BiFPN).
  - Head: 최종 바운딩 박스 오프셋 및 클래스 확률 예측 (Decoupled Head, Anchor/Anchor-free).

</details>

```text
[ 현대 객체 탐지기(YOLO/R-CNN) 표준 3단 아키텍처 ]
 입력 이미지 (H × W × 3)
       │
       ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 1. 백본 (Backbone: CSPDarknet / ResNet)                   │ ── 계층별 특징 맵 추출 (C3, C4, C5)
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 2. 넥 (Neck: FPN + PANet)                                 │ ── Top-Down + Bottom-Up 양방향 특징 융합
 └─────────────────────────────┬─────────────────────────────┘
                               │ (P3: 소형, P4: 중형, P5: 대형)
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 3. 헤드 (Head: Decoupled Head)                            │ ── BBox 회귀 (CIoU) + 클래스 분류 (BCE)
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 4. 후처리 엔진 (NMS Engine)                               │ ── 신뢰도 필터링 및 중복 박스 억제
 └───────────────────────────────────────────────────────────┘
```

선의 의미: 백본 특징 추출, 넥 다중 스케일 피처 결합, 헤드 예측 및 NMS 후처리 파이프라인.

| 구성요소 | 책임 |
|:---|:---|
| 백본 (Backbone) | 입력 영상에서 **에지, 텍스처, 의미론적 공간 특징 맵 추출** |
| 넥 (Neck / FPN) | 상하위 계층 특징을 융합하여 **스케일 불변 특징 피라미드 구성** |
| 탐지 헤드 (Head) | 그리드 셀/영역별로 **BBox 좌표($x,y,w,h$), 객체성, 클래스 확률 출력** |
| NMS 후처리 모듈 | IoU 임계치(0.5) 초과 중복 박스를 제거하여 **최종 단일 박스 확정** |

#### 한줄 요약

- 백본-넥-헤드 구조로 특징 추출과 박스 예측을 수행하고, NMS로 최적 박스를 선별

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CIoU Loss(Complete IoU)**: 바운딩 박스 회귀 시 겹침 영역(IoU), 중심점 거리($\rho$), 종횡비($v$)를 모두 페널티로 반영하여 빠른 수렴을 유도하는 손실 함수.

</details>

```text
입력 영상 인입
   │
   ▼
[ 1. 백본 통과 및 계층별 다중 스케일 특징 맵 추출 ]
   │
   ▼
[ 2. 넥(FPN/PANet) 융합: 소형(P3), 중형(P4), 대형(P5) 앵커 그리드 매핑 ]
   │
   ▼
[ 3. 헤드 추론: 각 그리드 셀별 BBox 좌표 및 클래스 로짓 예측 ]
   │
   ▼
[ 4. 신뢰도 임계치(Score Threshold > 0.25) 1차 필터링 ]
   │
   ▼
[ 5. Non-Maximum Suppression (NMS, IoU Threshold = 0.5) 적용 ]
   │
   ▼
[ 6. 최종 바운딩 박스 좌표 및 클래스 라벨 오버레이 출력 ]
```

**동작 원리**

1. **특징 추출**: 백본 네트워크를 거치며 3가지 해상도(8배, 16배, 32배 다운샘플링)의 피처 맵 도출
2. **피처 융합**: FPN을 통해 상위의 풍부한 의미 정보와 하위의 정밀한 위치 정보 결합
3. **병렬 예측**: 1-Stage 방식 기준 수천 개의 그리드 위치에서 BBox와 클래스를 단일 패스로 예측
4. **신뢰도 스크리닝**: 배경 점수가 높거나 신뢰도가 낮은 다수의 무효 박스 즉시 탈락
5. **NMS 정제**: 남은 박스 중 IoU 중복도가 높은 박스를 억제하고 최고 점수 박스만 확정

#### 한줄 요약

- 다중 스케일 피처를 융합하여 단일 패스로 박스를 예측하고, 신뢰도 필터와 NMS로 최종 확정

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **1-Stage vs 2-Stage 비교**:
  - 1-Stage (YOLO/SSD): RPN 없이 그리드에서 위치와 분류 동시 예측, 초고속(Real-time, 60+ FPS).
  - 2-Stage (Faster R-CNN): RPN(Region Proposal Network)으로 후보 영역을 먼저 제안하고 RoI Pooling 후 분류, 높은 정밀도.

</details>

| 비교 항목 | 1-Stage Detector (YOLO 계열) | 2-Stage Detector (Faster R-CNN) |
|:---|:---|:---|
| 핵심 구조 | **RPN 없이 단일 신경망으로 BBox/클래스 동시 예측** | **RPN(후보 제안) $\to$ RoI Pooling $\to$ 2차 정밀 분류** |
| 추론 속도 | **초고속 (30~140+ FPS, 실시간 최적)** | 상대적 저속 (5~15 FPS) |
| 탐지 정밀도 | 보통~우수 (최신 YOLOv8/v10은 mAP 대폭 향상) | **소형/밀집 객체 위치 정밀도 최우수** |
| 주요 적용처 | **자율주행, 지능형 CCTV, 엣지 로보틱스** | **의료 영상 진단, 위성/항공 정밀 판독** |
| 취약점 | 극소형 객체 뭉개짐(구버전), 밀집 객체 겹침 | 높은 연산량 및 엣지 서빙 불가 |

#### 한줄 요약

- 실시간성과 엣지 배포는 1-Stage(YOLO), 소형 밀집 객체 정밀 검출은 2-Stage(Faster R-CNN)를 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Mosaic 증강**: 4장의 서로 다른 이미지를 무작위로 잘라 하나의 이미지로 합성함으로써 소형 객체 학습 빈도를 높이고 미니배치 통계를 안정화하는 YOLO 핵심 데이터 증강.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 드론/CCTV 원거리 촬영 시 **소형 객체 미탐(False Negative)** | **Mosaic / Mixup 증강 + P2 초고해상도 피처 레이어 추가** | 소형 객체 탐지 재현율(Recall) 대폭 향상 |
| 군중/밀집 객체에서 NMS로 인한 **인접 정상 객체 삭제** | **Soft-NMS (점수 감쇠) 또는 NMS-Free (YOLOv10)** | 밀집 객체 중복 탐지 및 누락 방지 |
| 임베디드 보드(Jetson/NPU)에서의 **FPS 저하 및 발열** | **TensorRT INT8 양자화 및 입력 해상도($640 \to 416$) 최적화** | 60 FPS 이상 실시간 처리량 확보 |
| 극단적 배경-객체 비율로 인한 **클래스 불균형** | **Focal Loss ($\gamma=2.0$) 및 CIoU 회귀 손실** 적용 | 쉬운 배경 손실 억제 및 박스 수렴 가속 |

#### 한줄 요약

- **Mosaic 증강 소형객체 검출·Soft-NMS 밀집객체 보존·TensorRT 양자화 가속·Focal Loss 불균형 해소**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **비전 객체 탐지 아키텍처 표준**: 실시간 엣지 비전 시스템은 YOLOv8/YOLOv10/RT-DETR이 시장 표준을 장악하고 있으며, 초정밀 오프라인 분석 및 서버 배치 작업에는 Swin-Transformer 백본 기반 Cascade R-CNN/DINO가 운용.

</details>

- 실시간 엣지 비디오 분석은 **1-Stage (YOLOv8/v10)**, 의료/위성 초정밀 객체 검출은 **2-Stage (Faster R-CNN/Cascade)** 선택

#### 한줄 요약

- 실시간성과 엣지 배포는 YOLO 1단계, 소형·밀집 객체의 초정밀 검출은 R-CNN 2단계를 선택
