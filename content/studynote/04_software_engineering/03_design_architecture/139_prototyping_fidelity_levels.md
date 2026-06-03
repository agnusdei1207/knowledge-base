+++
title = "139. 프로토타입 충실도 (Fidelity Levels) - Lo-Fi·Mid-Fi·Hi-Fi"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) 충실도는 **Lo-Fi(종이 스케치)·Mid-Fi(와이어프레임)·Hi-Fi(인터랙티브 목업)** 3단계로 구분되며, 프로젝트 단계·목적에 따라 적절한 수준을 선택한다.
> 2. **가치**: 초기에 Hi-Fi를 만들면 **수정 비용이 크고 피드백이 디자인에 매몰**되므로, Lo-Fi로 시작하여 점진적으로 충실도를 높이는 것이 효율적이다.
> 3. **판단 포인트**: Lo-Fi(5분 제작, 구조 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))→Mid-Fi(Figma 와이어프레임)→Hi-Fi(Figma 인터랙티브, 실제와 유사)의 순서로 진행한다.

---

## Ⅰ. 개요 및 필요성

| 충실도 | 도구 | 시간 | 목적 |
|:---|:---|:---|:---|
| **Lo-Fi** | 종이·화이트보드 | 분 | 구조·흐름 |
| **Mid-Fi** | Figma 와이어프레임 | 시간 | 레이아웃 |
| **Hi-Fi** | Figma 인터랙티브 | 일 | 실제 UX |

- **📢 섹션 요약 비유**: Lo-Fi는 연필 스케치, Mid-Fi는 밑그림, Hi-Fi는 완성 유화이다.

---

## Ⅱ~Ⅴ. 결론

충실도 단계별 접근은 **비용 효율적 UX [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 핵심**이며, Lo-Fi에서 구조를 확정한 후 Hi-Fi로 진행한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Lo-Fi** | 종이 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) |
| **Mid-Fi** | 와이어프레임 |
| **Hi-Fi** | 인터랙티브 목업 |
| **Figma** | 프로토타이핑 도구 |
| **[사용성 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/451_usability_test/)** | Hi-Fi로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[종이 프로토타입 (~2005)] → [Balsamiq (Lo-Fi, 2008)]
    → [Sketch (Mid-Fi, 2010)] → [Figma (Hi-Fi, 2016)]
    → [현재: AI 프로토타입 — 스케치→코드 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Lo-Fi는 **연필 스케치**예요. 빠르게 그려서 **대략적인 모양**을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
2. Hi-Fi는 **완성 그림**이에요. 실제처럼 **클릭도 되고 움직여요**.
3. 처음부터 완성 그림을 그리면 **수정이 어려우니** 스케치부터 시작해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 973

← **이전**: [138. 프로토타이핑 - Throwaway vs Evolutionary 프로토타입](/knowledge-base/studynote/04_software_engineering/03_design_architecture/138_prototyping_throwaway_evolutionary/)
**다음**: [140. 쉐도잉 & 관찰 기법 (Shadowing/Observation) - 현장 기반 요구 도출](/knowledge-base/studynote/04_software_engineering/03_design_architecture/140_shadowing_observation_technique/) →

---
