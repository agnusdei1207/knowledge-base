---
title: 142. 요구 분석 & 갈등 해결 - 이해관계자 간 상충 요구 조정
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구 분석 갈등 해결은 **[[173_stakeholder_identification_impact_matrix|이해관계자]] 간 상충되는 요구(보안↔편의, [[282_performance_tactics|성능]]↔비용)를 [[655_ir_detection_analysis|식별]]·협상·우선순위화**하여 합의를 도출하는 과정이다.
> 2. **가치**: 갈등을 방치하면 프로젝트 중반에 **요구 변경 폭발([[161_scope_creep_requirements_inflation_prevention|Scope Creep]])**이 발생하며, 초기에 갈등을 해결하면 변경 비용을 **[[489_raid_10_hybrid|10]]~100배** 절감한다.
> 3. **판단 포인트**: MoSCoW(Must·Should·Could·Won't)·AHP([[213_swot_ahp_analytic_hierarchy_process_decision_making|Analytic Hierarchy Process]])·Kano 모델이 우선순위화 기법이며, 트레이드오프 매트릭스로 갈등을 [[003_bigdata_7v|시각화]]한다.

---

## Ⅰ. 개요 및 필요성

```text
MoSCoW: Must(필수) > Should(중요) > Could(선택) > Won't(제외)
AHP: 쌍대 비교 → 가중치 산출 → 정량적 우선순위
Kano: 기본(당연)·성능(비례)·매력(감동) 요구 분류
```

- **📢 섹션 요약 비유**: 갈등 해결은 **예산 편성**이다. 모든 부서가 원하는 것을 다 줄 수 없으므로 우선순위로 배분한다.

---

## Ⅱ~Ⅴ. 결론

요구 갈등 해결은 **프로젝트 성패의 핵심**이며, MoSCoW·AHP로 정량적 우선순위를 부여한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **MoSCoW** | 우선순위 [[104_classification_analysis|분류]] |
| **AHP** | 정량적 [[267_weight_bias_activation|가중치]] |
| **Kano** | 요구 유형 [[104_classification_analysis|분류]] |
| **트레이드오프** | 상충 요구 [[003_bigdata_7v|시각화]] |
| **[[161_scope_creep_requirements_inflation_prevention|Scope Creep]]** | 미해결 갈등의 결과 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 협상 (~2000s)] → [MoSCoW (DSDM, 1994)]
    → [AHP (Saaty, 1980)] → [Kano 모델 (1984)]
    → [현재: AI 요구 충돌 탐지 — 자동 상충 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 갈등 해결은 **예산 나누기**예요. 모든 걸 다 할 수는 없어요.
2. MoSCoW로 **꼭 해야 할 것(Must)**과 **나중에 할 것(Won't)**을 나눠요.
3. 먼저 중요한 것부터 하면 **예산(시간) 낭비**를 줄일 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 973

← **이전**: [[141_focus_group_interview_fgi|141. 포커스 그룹 인터뷰 (FGI) - 그룹 심층 인터뷰 기법]]
**다음**: [[143_structured_analysis_dfd_dd_minispec|143. 구조적 분석 (Structured Analysis) - DFD·DD·Mini-Spec]] →

---
