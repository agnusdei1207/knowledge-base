+++
title = "131. SLAM (동시 위치 추정과 지도 작성) - XR/자율주행의 공간 인식 핵심"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLAM(Simultaneous Localization and [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))은 <strong>센서(카메라·<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/">LiDAR</a>)로 주변 환경의 지도를 작성하면서 동시에 자신의 위치를 추정</strong>하는 알고리즘으로, 자율주행·XR·로봇의 핵심 기술이다.
> 2. **가치**: GPS가 안 되는 실내·지하에서도 SLAM으로 <strong>카메라만으로 위치를 파악</strong>할 수 있으며, Vision Pro·Quest 등 XR 디바이스의 Inside-Out 트래킹이 SLAM 기반이다.
> 3. **판단 포인트**: [Visual SLAM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/132_v_slam_visual_slam_camera/)(카메라)·[LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/) SLAM(라이다)을 구분하고, ORB-SLAM·RTAB-MAP이 대표적 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 구현이다.

---

## Ⅰ. 개요 및 필요성

```text
SLAM = 지도 작성(Mapping) + 위치 추정(Localization) 동시 수행
  센서 → 특징점 추출 → 지도 업데이트 → 위치 보정 → 반복
```

- **📢 섹션 요약 비유**: SLAM은 <strong>눈을 가린 채 손으로 더듬으며 방 지도를 그리면서 내 위치를 파악</strong>하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 유형 | 센서 | 특징 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/132_v_slam_visual_slam_camera/">Visual SLAM</a></strong> | 카메라 | 저비용, XR 표준 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/">LiDAR</a> SLAM</strong> | [LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/) | 정밀, 자율주행 |

---

## Ⅲ~Ⅴ. 결론

SLAM은 <strong>GPS 없는 환경에서 위치·공간을 인식하는 유일한 방법</strong>이며, XR·자율주행·로봇의 핵심 기반 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SLAM** | 동시 위치+지도 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/132_v_slam_visual_slam_camera/">Visual SLAM</a></strong> | 카메라 기반 (XR) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/">LiDAR</a> SLAM</strong> | 라이다 기반 (자율주행) |
| **6DoF** | SLAM이 제공하는 추적 |
| **ORB-SLAM** | 대표 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">EKF-SLAM (1990s)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">PTAM (2007)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ORB-SLAM (2015)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Deep SLAM (2018~, DL 기반)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: Neural Radiance Fields (NeRF) + SLAM — 3D 재구성</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. SLAM은 **눈을 가리고 손으로 더듬어서 방 지도를 그리는** 거예요.
2. 동시에 <strong>"나는 지금 어디쯤이지?"</strong>도 알아내요.
3. VR 헤드셋이 **방 안에서 내 위치를 아는 건** SLAM 덕분이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 552

← **이전**: [130. 6DoF 트래킹 (Pitch·Yaw·Roll) - XR/공간 컴퓨팅의 움직임 추적](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/130_6dof_tracking_pitch_yaw_roll/)
**다음**: [132. Visual SLAM (V-SLAM) - 카메라 기반 동시 위치 추정과 지도 작성](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/132_v_slam_visual_slam_camera/) →

---
