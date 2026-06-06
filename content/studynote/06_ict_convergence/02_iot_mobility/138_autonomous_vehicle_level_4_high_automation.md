---
title: "138. Autonomous Vehicle Level 4 High Automation"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SAE Level 4는 <strong>특정 ODD(지역·날씨·속도) 내에서 인간 개입 없이 완전 자율주행</strong>이 가능하며, Takeover 요청이 없어 **운전석이 필요 없을 수 있다**.
> 2. **가치**: L3는 운전자가 항상 대기해야 하지만, L4는 <strong>해당 ODD 내에서 완전 무인</strong>이므로 로보택시·무인 셔틀·무인 배달이 가능하다.
> 3. **판단 포인트**: Waymo(피닉스·샌프란시스코)·Cruise·Baidu Apollo가 L4 로보택시를 운영 중이며, ODD 확장(도심->교외->악천후)이 핵심 과제이다.

---

## Ⅰ. 개요 및 필요성

```text
L4: 특정 ODD 내 완전 자율 (운전석 불필요)
  Waymo: 피닉스·SF 도심 로보택시
  Cruise: SF 야간 운행
  ODD 한계: 악천후·비정형 도로 미지원
```

- **📢 섹션 요약 비유**: L4는 <strong>특정 노선의 무인 셔틀</strong>이다. 정해진 구간에서는 완벽하지만, 구간 밖은 못 간다.

---

## Ⅱ~Ⅴ. 결론

L4는 <strong>로보택시·무인 배달의 현실</strong>이며, ODD 확장과 규제 정비가 대중화의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **L4** | 고도 자율 (ODD 한정) |
| **Waymo** | L4 로보택시 |
| **ODD** | 운행 설계 영역 |
| **로보택시** | L4 핵심 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| **L5** | 완전 자율 (미달성) |

### 📈 관련 키워드 및 발전 흐름도

```text
[L2 ADAS (2015)] -> [L3 Mercedes (2023)]
    -> [L4 Waymo 로보택시 (2020~)] -> [L4 Cruise (2022)]
    -> [현재: L4 ODD 확장 + 규제 정비]
```

### 👶 어린이를 위한 3줄 비유 설명
1. L4는 <strong>정해진 구간의 무인택시</strong>예요. 운전자가 **전혀 필요 없어요**!
2. Waymo처럼 **특정 도시에서 혼자 달리는** 택시가 이미 있어요.
3. 하지만 폭우나 **낯선 도로에서는 아직** 못 달려요(ODD 한계)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 552

<- **이전**: [137. 자율주행 Level 3 조건부 자율 - 시스템 책임의 시작](/studynote/06_ict_convergence/02_iot_mobility/137_autonomous_vehicle_level_3_conditional/)
**다음**: [139. 센서 퓨전 (Camera·LiDAR·Radar) - 자율주행 인지 통합](/studynote/06_ict_convergence/02_iot_mobility/139_sensor_fusion_camera_lidar_radar/) ->

---
