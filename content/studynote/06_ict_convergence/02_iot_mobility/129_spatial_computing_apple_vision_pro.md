---
title: 129. 공간 컴퓨팅 & Apple Vision Pro - 차세대 인터페이스 패러다임
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]]([[232_spatial_computing_digital_twin|Spatial Computing]])은 **3차원 물리 공간을 컴퓨팅 인터페이스로 사용**하는 패러다임으로, 눈·손·음성으로 공간 속 디지털 콘텐츠와 상호작용하며, Apple Vision Pro(2024)가 대표 디바이스이다.
> 2. **가치**: 2D 화면([[229_monitor|모니터]]·스마트폰)은 **크기 제약·[[675_multitasking_terminology_preemptive|멀티태스킹]] 한계**가 있지만, [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 **무한한 가상 디스플레이·3D 콘텐츠 배치**로 작업 공간을 혁신한다.
> 3. **판단 포인트**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]] = XR(VR+AR+MR) + **환경 인식([[140_lidar_light_detection_and_ranging_tof|LiDAR]])** + **자연 입력(눈·손·음성)** + **공간 앵커(물리 공간에 디지털 콘텐츠 고정)**이며, visionOS가 개발 플랫폼이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    공간 컴퓨팅 구성                                   │
├───────────────────────────────────────────────────────┤
│  [입력] 눈 추적 · 손 제스처 · 음성                   │
│  [환경] LiDAR · 카메라 → 3D 공간 인식               │
│  [디스플레이] Micro-OLED · 패스스루 MR               │
│  [콘텐츠] 가상 윈도우 · 3D 객체 · 몰입 환경         │
│  [앵커] 가상 객체를 물리 공간에 고정                  │
│                                                       │
│  플랫폼: visionOS (SwiftUI + RealityKit)              │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 **"공기 중에 화면이 떠 있는" 컴퓨터**이다. 눈으로 보고, 손으로 만지고, 말로 명령한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2D vs [[232_spatial_computing_digital_twin|공간 컴퓨팅]]

| 비교 | 2D ([[229_monitor|모니터]]) | [[232_spatial_computing_digital_twin|공간 컴퓨팅]] |
|:---|:---|:---|
| **입력** | 키보드·마우스 | **눈·손·음성** |
| **디스플레이** | 평면 | **3D 공간** |
| **화면 수** | 1~3 | **무제한** |
| **몰입** | 낮음 | **높음** |

- **📢 섹션 요약 비유**: [[229_monitor|모니터]]는 창문(고정), [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 눈앞의 무한한 하늘(자유 배치)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | VR 헤드셋 | Vision Pro |
|:---|:---|:---|
| **패스스루** | 제한적 | **고품질 MR** |
| **입력** | 컨트롤러 | **손·눈** |
| **OS** | 게임 중심 | **범용 OS (visionOS)** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 분야
- 작업: 무한 가상 [[229_monitor|모니터]] (생산성).
- 설계: 3D 모델 공간 검토 (CAD).
- 의료: 수술 가이드 AR 오버레이.
- 협업: 공간 화상 회의 (Persona).

---

## Ⅴ. 기대효과 및 결론

[[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 **"화면 뒤"에서 "공간 속"으로 컴퓨팅을 이동**시키는 차세대 인터페이스이며, [[164_pc|PC]]→모바일 전환에 이은 3번째 패러다임 시프트이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[232_spatial_computing_digital_twin|공간 컴퓨팅]]** | 3D 공간 기반 컴퓨팅 |
| **visionOS** | Apple [[232_spatial_computing_digital_twin|공간 컴퓨팅]] OS |
| **패스스루** | 카메라로 현실 투과 |
| **공간 앵커** | 가상 객체를 물리에 고정 |
| **[[140_lidar_light_detection_and_ranging_tof|LiDAR]]** | 3D 공간 인식 센서 |

### 📈 관련 키워드 및 발전 흐름도

```text
[VR 헤드셋 (Oculus Rift, 2012~)]
    │
    ▼
[AR 글래스 (Google Glass, 2013)]
    │
    ▼
[MR (HoloLens, 2016~)]
    │
    ▼
[공간 컴퓨팅 (Apple Vision Pro, 2024~)]
    │
    ▼
[현재: AR 안경 경량화 — 일상 착용 공간 컴퓨팅]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 **공기 중에 화면이 떠 있는** 컴퓨터예요.
2. **눈으로 보고, 손으로 만지고, 말로 명령**해요. 키보드가 필요 없어요!
3. 방 안 어디에나 **가상 화면**을 놓을 수 있어서 무한히 넓은 책상이 생겨요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 552

← **이전**: [[128_vr_ar_mr_xr_spatial_computing|128. VR·AR·MR·XR & 공간 컴퓨팅 - 현실과 가상의 융합 기술 스펙트럼]]
**다음**: [[130_6dof_tracking_pitch_yaw_roll|130. 6DoF 트래킹 (Pitch·Yaw·Roll) - XR/공간 컴퓨팅의 움직임 추적]] →

---
