+++
title = "138. 프로토타이핑 - Throwaway vs Evolutionary 프로토타입"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로토타이핑은 **불완전한 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델을 빠르게 만들어 사용자 피드백을 얻는** 요구 도출·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기법이며, Throwaway(폐기형)과 Evolutionary(진화형)로 구분된다.
> 2. **가치**: SRS 문서만으로는 사용자가 "이게 내가 원하는 것인지" 판단하기 어렵지만, [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/)으로 **시각적으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 숨겨진 요구를 80%+ 더 발견**할 수 있다.
> 3. **판단 포인트**: Throwaway(빠르게 만들고 버림, 요구 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 목적)는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 요구 도출에, Evolutionary(계속 발전시켜 최종 제품화)는 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)·반복 개발에 적합하다.

---

## Ⅰ. 개요 및 필요성

| 비교 | Throwaway | Evolutionary |
|:---|:---|:---|
| **목적** | 요구 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 폐기 | 점진적 제품화 |
| **코드 품질** | 낮음 (빠른 구현) | **높음 (제품 수준)** |
| **방법론** | 폭포수 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 단계 | **[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)·반복** |

- **📢 섹션 요약 비유**: Throwaway는 **클레이 모형(전시 후 폐기)**, Evolutionary는 **점토 조각(계속 다듬어 완성)**이다.

---

## Ⅱ~Ⅴ. 결론

프로토타이핑은 **사용자와의 소통 도구**이며, 목적에 따라 Throwaway·Evolutionary를 선택한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Throwaway** | 폐기형 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) |
| **Evolutionary** | 진화형 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) |
| **Wireframe** | 저수준 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) |
| **Mockup** | 중수준 (시각적) |
| **[MVP](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/)** | 최소 기능 제품 |

### 📈 관련 키워드 및 발전 흐름도

```text
[종이 프로토타입 (~2000s)] → [Wireframe (Balsamiq)]
    → [Interactive Mockup (Figma, 2016)]
    → [No-Code 프로토타입 (2020~)]
    → [현재: AI 프로토타입 — 스케치→코드 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Throwaway는 **클레이 모형**이에요. [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 **버려요**.
2. Evolutionary는 **점토 조각**이에요. 계속 **다듬어서 완성**해요.
3. 먼저 대충 만들어 보여주면 "이건 아니에요!" 를 **빨리** 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 973

← **이전**: [137. 페르소나 분석 & 모델링 - 사용자 중심 요구 도출](/knowledge-base/studynote/04_software_engineering/03_design_architecture/137_persona_analysis_modeling/)
**다음**: [139. 프로토타입 충실도 (Fidelity Levels) - Lo-Fi·Mid-Fi·Hi-Fi](/knowledge-base/studynote/04_software_engineering/03_design_architecture/139_prototyping_fidelity_levels/) →

---
