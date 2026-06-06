---
title: "130. 6Dof Tracking Pitch Yaw Roll"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 6DoF(Six Degrees of Freedom)는 <strong>3축 회전(Pitch·Yaw·Roll) + 3축 이동(X·Y·Z)</strong>의 6가지 자유도 추적이며, XR/공간 컴퓨팅에서 사용자의 머리·손·물체 위치를 정밀하게 파악한다.
> 2. **가치**: 3DoF(회전만)는 고개만 돌릴 수 있지만, 6DoF는 **걸어다니며 가상 물체에 가까이 다가가는** 등 실제 공간 이동이 반영되어 <strong>높은 몰입감·자연스러운 상호작용</strong>을 제공한다.
> 3. **판단 포인트**: Inside-Out 트래킹(헤드셋 카메라로 추적, Quest·Vision Pro)이 현재 주류이며, [SLAM](/studynote/06_ict_convergence/02_iot_mobility/131_slam_simultaneous_localization_mapping/)(동시 위치 추정·지도 작성) 알고리즘이 핵심 기술이다.

---

## Ⅰ. 개요 및 필요성

```text
6DoF = 3축 회전 + 3축 이동
  Pitch (끄덕), Yaw (도리도리), Roll (갸우뚱)
  + X(좌우), Y(상하), Z(앞뒤)
```

- **📢 섹션 요약 비유**: 3DoF는 의자에 앉아 고개만 돌리기, 6DoF는 일어나서 방 안을 자유롭게 돌아다니기이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | 3DoF | 6DoF |
|:---|:---|:---|
| **회전** | ✅ | ✅ |
| **이동** | ❌ | **✅** |
| **몰입** | 낮음 | **높음** |
| **디바이스** | 카드보드 | Quest·VP |

---

## Ⅲ~Ⅴ. 결론

6DoF는 <strong>공간 컴퓨팅의 필수 기반 기술</strong>이며, Inside-Out + SLAM이 현재 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **6DoF** | 6자유도 추적 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/131_slam_simultaneous_localization_mapping/">SLAM</a></strong> | 동시 위치 추정·지도 작성 |
| **Inside-Out** | 헤드셋 카메라 기반 추적 |
| **Pitch/Yaw/Roll** | 3축 회전 |
| **공간 앵커** | 6DoF 기반 가상 객체 고정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[3DoF (Google Cardboard, 2014)] -> [Outside-In 6DoF (Vive, 2016)]
    -> [Inside-Out 6DoF (Quest, 2019)]
    -> [손·눈 추적 + 6DoF (Vision Pro, 2024)]
    -> [현재: 밀리미터 정밀도 6DoF — AR 글래스]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 3DoF는 **의자에 앉아 고개만** 돌리는 거예요.
2. 6DoF는 **일어나서 방 안을 걸어다니는** 거예요. 가상 물건에 **다가갈 수도** 있어요!
3. 6DoF 덕분에 VR 게임에서 **진짜로 움직이는 것처럼** 느껴진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 552

<- **이전**: [129. 공간 컴퓨팅 & Apple Vision Pro - 차세대 인터페이스 패러다임](/studynote/06_ict_convergence/02_iot_mobility/129_spatial_computing_apple_vision_pro/)
**다음**: [131. SLAM (동시 위치 추정과 지도 작성) - XR/자율주행의 공간 인식 핵심](/studynote/06_ict_convergence/02_iot_mobility/131_slam_simultaneous_localization_mapping/) ->

---
