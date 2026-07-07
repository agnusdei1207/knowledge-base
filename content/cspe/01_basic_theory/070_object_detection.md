---
title: "객체 탐지 — YOLO·R-CNN (Object Detection) [출제: 126회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 70
---

# 070. 객체 탐지 — YOLO·R-CNN (Object Detection) [출제: 126회]

## Ⅰ. 개요

- **정의/개념**: 이미지나 영상 내에서 관심 대상인 객체(Object)의 위치(Localization)를 바운딩 박스(Bounding Box)로 특정하고, 해당 객체가 어떤 범주(Classification)인지 동시에 식별하는 컴퓨터 비전 기술임
- **배경/필요성**: 단순 이미지 분류(Classification)는 이미지당 하나의 라벨만 제공하므로, 자율주행, 보안 관제, 결함 탐지 등 한 화면 내 여러 객체의 상세 위치와 종류를 모두 파악해야 하는 실무 환경에서 필수적임

## Ⅱ. 특징 및 비교

| 판단 기준 | 2-Stage Detector (R-CNN 계열) | 1-Stage Detector (YOLO 계열) |
|:---|:---|:---|
| **처리 방식** | 후보 영역 추출(RPN) 후 분류 수행 | 후보 추출과 분류를 단일 단계로 처리 |
| **핵심 장점** | 높은 탐지 정확도 (Precision) | 압도적인 처리 속도 (Real-time) |
| **핵심 단점** | 느린 속도로 인해 실시간 적용 어려움 | 작은 객체 탐지 및 정밀도 상대적 저하 |
| **대표 모델** | R-CNN, Fast R-CNN, Faster R-CNN | YOLO (v1~v11), SSD, RetinaNet |

> 요약: 정밀한 분석이 필요하면 2-Stage를, 자율주행 등 실시간성이 중요하면 1-Stage를 선택함

## Ⅲ. 구성요소/구조

- **구성요소**:
  - **Backbone**: 이미지로부터 특징 맵(Feature Map)을 추출하는 신경망(ResNet, Darknet 등)임
  - **Neck**: 백본과 헤드를 연결하며, 다양한 크기의 객체를 탐지하기 위해 특징 맵을 재구성함 (FPN, PAN 등)
  - **Head**: 최종적으로 바운딩 박스의 좌표(x, y, w, h)와 클래스 확률을 예측함
  - **Anchor Box**: 객체가 있을 법한 다양한 크기와 비율의 미리 정의된 후보 박스임
  - **NMS (Non-Maximum Suppression)**: 중복된 여러 바운딩 박스 중 점수가 가장 높은 것만 남기고 제거하는 후처리 기법임

- **탐지 프로세스**:
```text
[Input Image] -> [Backbone] -> [Neck(FPN)] -> [Detection Head] -> [Post-processing]
      |               |              |                |                  |
    Raw RGB      Feature Map    Multi-scale    Box/Class Pred        NMS/Threshold
```

## Ⅳ. 문제점 및 개선방안

1. **[작은 객체 탐지 성능 저하]**: 특징 맵이 압축되면서 작은 객체의 정보가 소실되어 탐지율이 떨어짐
   - **개선방안**: 특징 피라미드 네트워크(FPN)를 도입하여 고해상도 하위 층의 정보를 결합하거나 이미지 해상도를 높임 (확인: mAP_small)
2. **[배경 오탐지 (False Positive)]**: 객체가 없는 배경 영역을 객체로 잘못 판단하여 정밀도가 하락함
   - **개선방안**: Focal Loss와 같이 배경 클래스(Easy Negative)의 비중을 낮추고 어려운 샘플에 집중하는 손실 함수를 사용함 (확인: Precision)
3. **[임베디드 환경 연산 제약]**: 실시간 탐지 모델이라도 엣지 장비에서는 연산량과 메모리 부족으로 성능이 저하됨
   - **개선방안**: 모델 경량화(Pruning, Quantization)를 수행하거나 MobileNet과 같은 경량 백본을 사용함 (확인: FPS (Frames Per Second))

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **자율주행 자동차** | 주변 차량, 보행자, 차선을 YOLO 등을 통해 실시간으로 탐지하여 경로 계획에 반영 | Latency (ms), mAP |
| **스마트 팩토리** | 컨베이어 벨트 위의 제품 불량(스크래치, 찍힘) 위치를 정밀하게 탐지 | Recall, 검출 누락률 |
| **지능형 CCTV** | 침입자나 배회하는 인물을 탐지하여 관제실에 즉시 알림 전송 | 정탐률, 오경보율 |

> 요약: 실무에서는 환경(서버 vs 엣지)과 요구되는 정확도에 따라 1-Stage와 2-Stage 모델을 전략적으로 선택함

## Ⅵ. 결론

객체 탐지는 인공지능이 세상을 '보는' 것을 넘어 공간적으로 '이해'하게 하는 핵심 기술임. 초기 리전 프로포절 기반의 복잡한 구조에서 시작해 현재는 단일 네트워크 기반의 초고속 탐지 및 Transformer 기반의 DETR(DEtection TRansformer)로 진화하고 있으며, 단순히 성능을 높이는 것을 넘어 다양한 조도와 기상 조건에서도 안정적으로 작동하는 강건성(Robustness) 확보가 향후 실용화의 관건이 될 것임.
