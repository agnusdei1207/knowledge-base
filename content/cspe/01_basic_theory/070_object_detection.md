---
title: "객체 탐지 — YOLO·R-CNN (Object Detection)"
date: "2026-07-02"
tags:
  - "cspe-basic_theory"
weight: 70
---

# 📖 【암기용】 개념 완전 이해

> 목적: 객체 탐지 모델의 두 갈래(1-Stage vs 2-Stage)를 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 이미지 안에서 객체의 '위치(Bounding Box)'를 찾고 '종류(Class)'를 동시에 분류하는 컴퓨터 비전 기술
- **왜 필요한가**: 자율주행차는 화면에 '보행자가 있다'는 분류뿐만 아니라, 그 보행자가 '어디에 있는지(위치)'를 실시간으로 알아야 정차할 수 있다.
- **핵심 직관**: R-CNN(2-Stage)은 "여기 객체가 있을 것 같아(후보 영역)" -> "이건 고양이야(분류)"로 두 단계에 걸쳐 신중히 찾고, YOLO(1-Stage)는 이미지를 격자로 나눠 한 번에 좌표와 클래스를 동시에 찍어낸다.

## 깊이 이해
- **배경·문제의식**: 단순히 "고양이 사진이다"를 넘어, 배경이 복잡하고 여러 객체가 섞인 사진에서 각각의 좌표와 크기를 정확히 알아내야 한다.
- **작동 원리 (2-Stage)**: Faster R-CNN 기준, RPN(Region Proposal Network)이 객체가 있을 만한 박스를 수천 개 던지고, 그 박스들을 CNN으로 다시 들여다보며 정확한 클래스와 정밀 위치를 판별한다. (정확도 우수, 속도 저하)
- **작동 원리 (1-Stage)**: YOLO는 이미지를 N x N 그리드로 분할한다. 각 그리드 셀이 직접 Bounding Box 좌표와 클래스 확률을 단 한 번의 신경망(You Only Look Once) 연산으로 뱉어낸다. (속도 압도적, 작은 객체 탐지 약점)
- **비유**: R-CNN은 돋보기를 들고 의심 부위를 하나하나 정밀 검사하는 탐정이고, YOLO는 사진 전체를 쓱 보고 위치와 종류를 한 번에 말하는 감정사다.
- **흔한 오해·주의점**: YOLO가 항상 최고는 아니다. 자율주행처럼 초당 30프레임 이상의 실시간성이 필요하면 YOLO를, 의료 영상 결절 탐지처럼 미세한 객체를 놓치면 안 되는 상황에서는 Faster R-CNN 기반 구조를 쓴다.

## 연결 개념
- CNN (Convolutional Neural Network) — 특징 맵(Feature Map)을 뽑아내는 척추(Backbone) 네트워크
- Bounding Box & IoU (Intersection over Union) — 예측한 위치 박스와 실제 정답 박스가 겹치는 비율로 정확도를 측정
- NMS (Non-Maximum Suppression) — 동일 객체에 중복 생성된 수많은 예측 박스 중 신뢰도 1등만 남기고 지우는 후처리 기술

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 2-Stage(Faster R-CNN)와 1-Stage(YOLO)의 파이프라인 차이를 명시하고, FPS(속도)와 mAP(정확도) 기반의 적용 판단 기준을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 객체 탐지(Object Detection)는 영상 내 다수 객체의 위치 정보(Bounding Box Regression)와 클래스(Classification)를 동시에 추출하는 딥러닝 비전 기술이다.
> 2. **가치**: 후보 영역 제안과 분류를 분리한 2-Stage(R-CNN)로 정확도를 확보했고, 이를 통합 회귀로 푼 1-Stage(YOLO)로 실시간(Real-time) 비전 처리를 실현했다.
> 3. **판단 포인트**: 도메인 요구사항이 30 FPS 이상의 처리 속도(자율주행, 방범)인지, 미세 객체의 높은 정밀도(의료영상, 정밀 결함)인지에 따라 모델을 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 객체 탐지 아키텍처 발전 흐름 이해 | 2-Stage(Faster R-CNN)와 1-Stage(YOLO) 구조 비교 | R-CNN 발전사만 나열하고 파이프라인 차이 누락 |
| 핵심 평가 지표 활용 역량 | IoU, mAP(mean Average Precision), FPS | 정확도 지표로 단순히 Classification Accuracy만 제시 |
| 실무 도메인별 최적 모델 선정 기준 | 실시간성(FPS) vs 정확도(mAP) 트레이드오프 | "YOLO가 R-CNN보다 무조건 좋다"식 단정적 서술 |

> 요약: 위치 추정 파이프라인 구조(직렬 vs 통합)를 밝히고, mAP와 FPS 지표에 기반한 아키텍처 선정 기준(Trade-off)을 보여주는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 정의: 입력 이미지에서 다중 객체의 좌표 추정 회귀(Regression)와 객체 종류 분류(Classification)를 동시에 수행하는 기술
- 배경: 단순 이미지 분류 네트워크는 객체의 위치 좌표와 화면 내 개수를 파악할 수 없어 공간 정보가 필요한 실무 적용 불가
- 필요성: 배경 혼잡도 증대, 객체 겹침(Occlusion) 조건 속에서도 mAP 50% 이상, 30 FPS 이상의 고속·고정밀 객체 인식 필수

---

## Ⅱ. 구조 및 구성요소

```text
Input Image -> Backbone (특징 추출) -> Neck (다중 스케일 융합) -> Head (BBox & Class 출력) -> NMS (후처리)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Backbone (백본) | 원본 이미지에서 공간적 구조 정보(Feature Map)를 계층적으로 추출 | ResNet, CSPDarknet 등 활용 |
| Neck (넥) | 크기가 다양한 객체 인식을 위해 스케일별 피처 맵을 융합 연산 | FPN(Feature Pyramid Network) 적용 |
| Head (헤드) | 위치 좌표(x, y, w, h) 회귀 손실 및 클래스 확률값 산출 | YOLO는 1-Stage, R-CNN은 RPN 거친 2-Stage |
| NMS (후처리) | 동일 객체에 생성된 중복 박스 중 신뢰도 최고점 1개만 남기고 억제 | IoU 임계값 기준 초과 시 제거 |

> 요약: 모든 객체 탐지 모델은 특징 추출(Backbone), 피처 융합(Neck), 예측 출력(Head), 박스 정제(NMS) 파이프라인으로 구성된다.

---

## Ⅲ. 동작원리 (1-Stage vs 2-Stage) 및 흐름도

```text
[2-Stage: Faster R-CNN] Feature Map -> RPN (후보 영역 추출) -> RoI Pooling -> Classification & BBox Regression
[1-Stage: YOLO] Feature Map -> Grid Cell 분할 (S×S) -> BBox 예측 & Class 분류 동시 출력 (단일 통합 Network)
```

| 단계 | Faster R-CNN (2-Stage) | YOLO (1-Stage) |
|:---:|:---|:---|
| 1. 특징 추출 | 전체 이미지 CNN 통합 연산 | 전체 이미지 CNN 통합 연산 |
| 2. 후보 영역 | **RPN(Region Proposal Network)**이 객체 의심 영역(Proposal) 제안 | 이미지를 **S × S 그리드(Grid)**로 분할 |
| 3. 특징 정렬 | 제안 영역을 고정 크기 피처로 변환 (**RoI Pooling**) | 각 셀이 BBox 좌표와 Confidence 점수 예측 |
| 4. 분류/회귀 | Fully Connected 층으로 클래스 분류 및 정밀 좌표 회귀 | 단일 신경망 텐서 연산으로 통합 회귀 즉시 산출 |

> 요약: 2-Stage는 RPN과 RoI Pooling의 직렬 구조로 미세 탐지 정밀도를 높였고, YOLO는 그리드 기반 통합 회귀 문제로 치환해 병렬 고속 처리를 달성했다.

---

## Ⅳ. 특징 (성능 평가 지표)

| 지표 | 산출 방식 및 의미 | 판단 포인트 |
|:---|:---|:---|
| IoU (Intersection over Union) | (예측 박스 교집합 정답 박스) / (예측 박스 합집합 정답 박스) | 객체 위치의 정밀도 평가, 통상 IoU 0.5 이상을 정답(TP) 간주 |
| mAP (mean Average Precision) | 각 클래스별 Precision-Recall 곡선 아래 면적(AP)의 전체 평균 | 모델의 전반적 탐지 정확도 및 재현율(Recall) 강건성 지표 |
| FPS (Frames Per Second) | 모델이 초당 처리하여 탐지를 완료하는 이미지 프레임 수 | 30 FPS 이상이어야 비디오 스트림 실시간 끊김 없는 탐지 가능 |

> 요약: 객체 탐지 시스템 도입 시 단일 분류 정확도(Accuracy)가 아닌 위치 정밀도(IoU) 기반의 mAP와 처리 속도(FPS)를 결합하여 성능을 평가한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 2-Stage (Faster R-CNN) | 1-Stage (YOLO) | 선택 기준 |
|:---|:---|:---|:---|
| 아키텍처 | Region Proposal + RoI + Classification | Single Network Regression | 파이프라인 복잡도 및 튜닝 난이도 |
| 성능 특성 | 고정확도 (High mAP), 속도 느림 (<10 FPS) | 실시간 속도 (High FPS, >45 FPS), 정확도 양호 | 30ms 이내 실시간 응답 요구사항 여부 |
| 작은 객체 탐지 | RoI 추출로 미세 객체 군집 인식률 우수 | 그리드 한계로 작은 객체 중첩 시 겹침 현상 취약 | 대상 객체의 픽셀 크기(해상도) 비중 |

> 요약: 자율주행이나 지능형 CCTV 관제 등 실시간성이 최우선이면 YOLO를, 의료 영상 결절 탐지나 정밀 PCB 결함 검사 등 재현율이 우선이면 Faster R-CNN을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 작은 객체 미탐(False Negative) | 특징 맵 해상도 손실, 단일 스케일 예측 한계 | FPN(Feature Pyramid Network) 도입으로 계층별 해상도 피처 융합 | 32×32 픽셀 이하 소형 객체 대상 mAP 스코어 |
| 극심한 클래스 불균형 | 배경(Background) 후보 박스가 실제 객체보다 압도적으로 많음 | Focal Loss 적용 (분류하기 쉬운 배경 예제의 손실 반영 가중치를 축소) | 배경 오탐률 및 소수 클래스 Precision/Recall |

> 요약: 스케일 변이에 의한 소형 객체 누락 리스크는 FPN 아키텍처로 보완하고, 배경-객체 불균형은 Focal Loss 함수 튜닝으로 억제한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 지능형 교통 관제 (ITS): 교차로 CCTV 실시간 차량/보행자 인식을 위해 1-Stage(YOLOv8) 도입, 텐서플로우 라이트(TFLite) 변환으로 Edge 기기에서 60 FPS 확보
2. 스마트 팩토리 정밀 검사: 반도체 웨이퍼 표면 미세 스크래치 탐지를 위해 Faster R-CNN 적용, IoU 임계값을 0.7로 높여 오탐률을 줄이고 mAP 95% 달성
3. NMS 겹침 최적화: 군중이나 적재물 등 밀집 환경에서 NMS가 정상 겹침 객체를 억제하는 현상 방지를 위해 Soft-NMS 적용하여 밀집 객체 재현율(Recall) 개선

**결론 (2줄):**
- 기술사 판단: 객체 탐지 시스템은 도메인의 제약조건(초당 프레임 수 vs 미세 탐지 정확도)에 따라 1-Stage와 2-Stage 백본을 분별 선택하고, FPN과 NMS 후처리로 약점을 보완해야 한다.
- 향후 방향: 최근 객체 탐지 트렌드는 CNN 백본을 넘어 Vision Transformer(ViT) 기반 DETR(Detection Transformer)로 진화하며 NMS 과정 없는 End-to-End 탐지로 발전 중이다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "객체 탐지 알고리즘 발전 과정을 설명하시오" | RPN과 1-Stage 그리드 분할 방식의 원리 차이 | mAP 등 평가지표와 1/2-Stage 비교 |
| 설계/방안형 | "자율주행 환경 적용 방안 설계, Faster R-CNN과 YOLO 비교" | 요구사항(실시간성) 기반 파이프라인 차이 | Ⅴ의 FPS 트레이드오프 심화 비교 및 Edge 배포 방안 |

> 요약: 개념 설명형 문제는 알고리즘 내부 동작(RPN 등) 대비에 집중하고, 적용 설계 문제에서는 FPS/mAP 트레이드오프에 따른 아키텍처 선택 논리를 강조한다.
