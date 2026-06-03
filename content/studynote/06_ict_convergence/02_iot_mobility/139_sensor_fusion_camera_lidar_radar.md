+++
title = "139. 센서 퓨전 (Camera·LiDAR·Radar) - 자율주행 인지 통합"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 센서 퓨전은 **카메라(시각)·[LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/)(3D 거리)·레이더(속도·거리)·초음파 등 이종 센서 데이터를 통합**하여 단일 센서보다 정확하고 강건한 환경 인지를 달성하는 기술이다.
> 2. **가치**: 카메라는 색상·텍스트 인식에 강하지만 야간·역광에 약하고, LiDAR는 정밀 거리 측정에 강하지만 비용이 높으며, 퓨전으로 **각 센서의 단점을 보완**한다.
> 3. **판단 포인트**: Early Fusion(센서 레벨)·Late Fusion(결정 레벨)·Mid Fusion(특징 레벨)으로 구분하며, Tesla(카메라 Only)와 Waymo([LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/)+카메라) 논쟁이 업계 핵심이다.

---

## Ⅰ. 개요 및 필요성

| 센서 | 강점 | 약점 |
|:---|:---|:---|
| **카메라** | 색상·표지판 | 야간·역광 |
| **[LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/)** | 3D 정밀 거리 | 고비용·악천후 |
| **레이더** | 속도·악천후 강건 | 저해상도 |

- **📢 섹션 요약 비유**: 센서 퓨전은 **시각+청각+촉각을 합치는** 것이다. 눈만으로 판단하는 것보다 더 정확하다.

---

## Ⅱ~Ⅴ. 결론

센서 퓨전은 **자율주행 안전성의 핵심**이며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 Mid-Level Fusion이 현재 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **센서 퓨전** | 이종 센서 통합 |
| **카메라** | 2D 시각 인지 |
| **[LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/)** | 3D 포인트 클라우드 |
| **레이더** | 속도·거리 감지 |
| **Tesla vs Waymo** | Camera Only vs 퓨전 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 센서 (카메라, 2010s)] → [LiDAR + 카메라 퓨전 (2015)]
    → [Tesla Camera Only (2021)] → [BEV Fusion (2022)]
    → [현재: Transformer 기반 통합 퓨전]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 센서 퓨전은 **눈(카메라)+귀(레이더)+손([LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/))**을 합치는 거예요.
2. 눈만으로 판단하면 **어두울 때 실수**하지만, 귀와 손도 쓰면 정확해요.
3. 자율주행차가 **안전하게 달리려면** 여러 감각을 합쳐야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 552

← **이전**: [138. 자율주행 Level 4 고도 자율 - 특정 영역 완전 무인](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/138_autonomous_vehicle_level_4_high_automation/)
**다음**: [140. LiDAR (Light Detection and Ranging) - ToF 기반 3D 거리 측정](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/) →

---
