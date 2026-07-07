---
title: "객체 탐지 — YOLO·R-CNN (Object Detection)"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 70
---


## Ⅰ. 개요

- **정의/개념**: 이미지나 영상 내에서 특정 대상($Object$)의 위치를 바운딩 박스($Bounding$ $Box$)로 특정($Localization$)함과 동시에, 해당 객체의 범주를 분류($Classification$)하는 컴퓨터 비전 기술임
- **배경/필요성**: 이미지 분류($Classification$)는 '무엇'인지만 판단하나, 실제 자율주행이나 보안 관제에서는 객체가 '어디에', '몇 개' 있는지에 대한 공간 정보가 필수적임. 이를 위해 고속 추론과 높은 정밀도를 동시에 달성하는 알고리즘 최적화가 요구됨

## Ⅱ. 특징 및 비교

### 1. 탐지 방식별 아키텍처 비교

| 판단 기준 | $2$-$Stage$ $Detector$ ($R$-$CNN$ 계열) | $1$-$Stage$ $Detector$ ($YOLO$ 계열) |
|:---|:---|:---|
| **처리 절차** | 후보 영역 추출($RPN$) $\rightarrow$ 분류/회귀 | 추출과 분류를 단일 파이프라인으로 통합 |
| **추론 속도** | 낮음 ($Latency$ 발생) | 매우 높음 ($Real$-$time$ 가능) |
| **탐지 정밀도** | 우수 (작은 객체 및 중첩 객체 강점) | 상대적 낮음 ($Background$ $Error$ 발생 가능) |
| **손실 함수** | $Cross$-$Entropy$, $L1/L2$ $Loss$ | $Focal$ $Loss$, $GIoU/DIoU/CIoU$ |

> 요약: 높은 정확도가 필요한 의료/정밀 검사에는 $2$-$Stage$를, 실시간 응답이 필수인 자율주행/드론에는 $1$-$Stage$를 적용함

### 2. $PPA$ 관점의 트레이드오프 ($Trade$-$offs$)
- **Performance**: $YOLO$ $v8 \sim v11$ 등 최신 모델은 $FPS$(초당 프레임 수)를 극대화하면서도 $mAP$(평균 정밀도)를 $2$-$Stage$ 수준으로 근접시킴
- **Precision**: $IoU(Intersection$ $over$ $Union)$ 임계치에 따라 성능 지표가 급변하며, 정밀도와 재현율($Recall$) 간의 트레이드오프 조절이 핵심임
- **Area(Resource)**: 모델 경량화($Tiny$ 버전)를 통해 $NPU/FPGA$ 등 제한된 자원의 엣지 디바이스 내 탑재 가능 여부를 결정함

## Ⅲ. 구성요소/구조

### 1. 객체 탐지 프레임워크 인사이트 ($Architecture$ $Insight$)
- **Backbone**: 이미지의 특징 기하 구조를 추출하는 심층 신경망 ($ResNet$, $CSP$-$Darknet$ 등)
- **Neck**: 다양한 크기의 객체를 탐지하기 위해 특징 맵을 재구성하고 결합 ($FPN$, $PAN$, $BiFPN$ 등)
- **Head**: 최종적인 위치 좌표 $(x, y, w, h)$와 클래스 확률($Confidence$ $Score$)을 예측하는 레이어
- **$NMS$ ($Non$-$Maximum$ $Suppression$ )**: 중복된 예측 박스 중 $Confidence$가 낮고 $IoU$가 높은 박스를 제거하는 필수 후처리 공정

### 2. $1$-$Stage$ $Detector$ ($YOLO$) 동작 원리
```text
[Input Image] -> [S x S Grid 분할] -> [Grid별 Bounding Box 예측] -> [Class 확률 Map 생성] -> [Final Detection]
      |                 |                       |                       |                      |
   Raw RGB        공간 구조 유지          Box (x,y,w,h,conf)          Softmax 분류            NMS 후처리
```

## Ⅳ. 문제점 및 개선방안

### 1. 실무적 문제점 및 대응 전략
1. **[작은 객체($Small$ $Object$) 탐지 누락]**: 고해상도 특징 맵이 소실되어 멀리 있는 객체나 작은 부품 탐지 실패
   - **개선방안**: $Feature$ $Pyramid$ $Network$($FPN$)를 통해 하위 층의 세부 정보를 상위로 전달하거나, 고해상도 타일링($Tiling$) 기법 적용 (확인: $mAP_{small}$)
2. **[클래스 불균형 ($Class$ $Imbalance$)]**: 배경 영역이 객체 영역보다 압도적으로 많아 배경을 객체로 오인하는 문제
   - **개선방안**: $Focal$ $Loss$를 도입하여 쉬운 배경 샘플의 가중치를 낮추고 어려운 객체 샘플 학습에 집중함 (확인: $Precision$-$Recall$ $Curve$)
3. **[동적 환경에서의 낮은 강건성]**: 야간, 우천, 안개 등 환경 변화 시 탐지 성능이 급격히 저하됨
   - **개선방안**: 기상 조건이 반영된 데이터 증강($Augmentation$) 및 열화상/라이다($LiDAR$) 센서 퓨전 기술 도입 (확인: 환경별 $Recall$ 변동폭)

### 2. 리얼월드 트러블슈팅 ($Real$-$world$ $Troubleshooting$)
- **상황**: 컨베이어 벨트 위의 고속 이동 제품 검사 시 $Motion$ $Blur$로 인해 바운딩 박스가 흔들리고 오탐 발생
- **해결**: 카메라 셔터 스피드 최적화와 동시에, 학습 시 $Blur$ $Augmentation$을 추가하여 저품질 이미지에 대한 내성을 확보함

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **자율주행 ADAS** | 전방 차량, 보행자, 신호등을 $YOLO$ 기반 실시간 탐지하여 급제동 및 조향 제어에 활용 | $Latency$ ($<30ms$), $mAP$ |
| **지능형 관제 (VMS)** | 침입자나 배회자를 자동 탐지하고 $NMS$를 통해 동일 인물 중복 알람 방지 | 정탐률, 미탐률, $FPS$ |
| **의료 영상 분석** | $X$-$ray$나 $MRI$ 영상 내 병변(종양 등) 위치를 $2$-$Stage$ 모델로 정밀 탐지 | $Dice$ $Coefficient$, 민감도 |

## Ⅵ. 결론

객체 탐지는 세상을 '보는' 인공지능을 넘어 '공간을 이해하는' 인공지능으로 가는 핵심 관문임. 초기 $Anchor$ 기반 방식에서 현재는 $Anchor$-$free$ 방식과 $Transformer$ 기반의 $DETR$ 구조로 진화하며 고정 관념을 탈피하고 있음. 향후 단순히 정확도를 높이는 것을 넘어, 추론 과정을 설명 가능한 $XAI$ 기술과 결합하여 자율주행 및 의료 분야의 신뢰성을 확보하는 방향으로 발전할 것임.
