---
title: "136. Brainstorming Jad Requirements"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 브레인스토밍은 <strong>비판 없이 자유롭게 아이디어를 발산</strong>하는 기법이고, JAD(Joint Application Development)는 <strong><a href="/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/">이해관계자</a>·개발자가 함께 모여 구조화된 워크숍으로 요구사항을 합의</strong>하는 기법이다.
> 2. **가치**: 1:1 인터뷰만으로는 다부서 갈등·숨겨진 요구 발견이 어렵지만, JAD 워크숍은 <strong><a href="/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/">이해관계자</a> 갈등을 현장에서 해결</strong>하고 합의를 이끌어낸다.
> 3. **판단 포인트**: 브레인스토밍은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 발산(아이디어 양), JAD는 수렴(합의·결정)에 강하며, <strong>퍼실리테이터(촉진자)</strong>의 역량이 성패를 좌우한다.

---

## Ⅰ. 개요 및 필요성

| 비교 | 브레인스토밍 | JAD |
|:---|:---|:---|
| **목적** | 아이디어 발산 | **합의·결정** |
| **구조** | 비구조 | **구조화 워크숍** |
| **핵심** | 비판 금지 | **퍼실리테이터** |

- **📢 섹션 요약 비유**: 브레인스토밍은 자유 토론(아이디어 양), JAD는 회의(결론 도출)이다.

---

## Ⅱ~Ⅴ. 결론

브레인스토밍+JAD는 <strong>그룹 기반 요구 도출의 핵심 기법</strong>이며, 발산->수렴의 조합으로 활용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **브레인스토밍** | 아이디어 발산 |
| **JAD** | 합의 워크숍 |
| **퍼실리테이터** | JAD [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 촉진자 |
| <strong><a href="/studynote/12_it_management/01_governance_strategy/040_design_thinking/">Design Thinking</a></strong> | 발산->수렴 프레임워크 |
| <strong><a href="/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/">Affinity</a> Diagram</strong> | 아이디어 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 회의 (~2000s)] -> [JAD (IBM, 1977)]
    -> [브레인스토밍 (Osborn, 1953)]
    -> [Design Thinking 통합 (2010s)]
    -> [현재: AI 퍼실리테이터 — 회의 요약·아이디어 분류 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 브레인스토밍은 <strong>자유 토론</strong>이에요. "어떤 아이디어든 OK!"
2. JAD는 <strong>모두 모여서 결론을 내는 회의</strong>예요. 사회자(퍼실리테이터)가 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)해요.
3. 먼저 **많은 아이디어를 내고(발산)**, 그중 **좋은 것을 고르는(수렴)** 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 136 / 973

<- **이전**: [135. 요구사항 도출 기법 - 인터뷰·JAD·프로토타이핑·브레인스토밍](/studynote/04_software_engineering/03_design_architecture/135_requirements_elicitation_techniques/)
**다음**: [137. 페르소나 분석 & 모델링 - 사용자 중심 요구 도출](/studynote/04_software_engineering/03_design_architecture/137_persona_analysis_modeling/) ->

---
