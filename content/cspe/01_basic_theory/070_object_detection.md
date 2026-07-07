---
title: "객체 탐지 (Object Detection)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 70
---

# 객체 탐지 (Object Detection)

## 1. 개요

- **정의/개념**: 객체 탐지는 이미지나 영상에서 객체의 클래스와 위치를 동시에 예측하는 컴퓨터 비전 과제이다.
- **배경/필요성**: 이미지 분류는 이미지 전체의 라벨만 제공하므로, 자율주행·검사·감시처럼 객체가 어디에 있는지까지 필요한 업무에는 탐지 모델이 필요하다.

객체 탐지의 핵심 출력은 `class + bounding box + confidence`이며, 분류와 위치 회귀가 함께 수행된다.

## 2. 특징 및 비교

| 구분 | 1-stage Detector | 2-stage Detector |
|---|---|---|
| 방식 | 후보 생성과 분류를 한 번에 수행 | region proposal 후 분류·회귀 |
| 대표 | YOLO, SSD | R-CNN, Faster R-CNN |
| 장점 | 빠른 추론 | 높은 정확도 |
| 약점 | 작은 객체·정밀도 한계 가능 | 추론 지연 큼 |
| 적용 | 실시간 탐지 | 정밀 분석 |

선택 기준은 실시간성, 작은 객체 성능, 정확도, 연산 자원, 배포 환경이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Backbone | 이미지 특징 추출 | CNN, Transformer |
| Neck | 다중 스케일 특징 결합 | FPN 등 |
| Detection Head | 클래스·박스 예측 | classification/regression |
| Anchor/Query | 후보 박스 기준 | 모델 방식별 차이 |
| NMS | 중복 박스 제거 | 최종 결과 정리 |

```text
Image -> Backbone -> Feature Pyramid -> Detection Head -> NMS -> Boxes
```

탐지는 특징 추출, 후보 생성, 박스 회귀, 중복 제거가 연결된 파이프라인이므로 병목도 단계별로 다르게 나타난다.

## 4. 문제점 및 개선방안

1. **작은 객체 탐지 어려움**
   - 해상도 축소와 feature 손실로 작은 객체가 사라질 수 있다.
   - **개선방안**: FPN, 고해상도 입력, data augmentation을 적용한다.

2. **중복 탐지**
   - 같은 객체에 여러 박스가 생성될 수 있다.
   - **개선방안**: NMS, Soft-NMS, IoU threshold 튜닝을 수행한다.

3. **실시간성 제약**
   - 정확도가 높은 모델은 지연 시간이 커질 수 있다.
   - **개선방안**: 모델 경량화, quantization, edge accelerator 활용을 검토한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 자율주행 | 차량·보행자·표지판 위치 탐지 | mAP, latency |
| 제조 검사 | 결함 위치와 유형 동시 탐지 | recall, false alarm |
| 영상 관제 | 사람·차량 객체를 실시간 탐지 | FPS, 추적 연계율 |

## 6. 결론

객체 탐지는 이미지 내 객체의 종류와 위치를 동시에 찾는 비전 과제이다. 1-stage/2-stage 선택, feature pyramid, box regression, NMS, 실시간성 제약을 연결해 설명해야 분류와 다른 탐지의 본질이 분명해진다.
