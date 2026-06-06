---
title: "135. Requirements Elicitation Techniques"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구 도출(Elicitation)은 <strong><a href="/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/">이해관계자</a>로부터 요구사항을 끌어내는 활동</strong>이며, 인터뷰·JAD·브레인스토밍·프로토타이핑·관찰·설문·[벤치마킹](/studynote/07_enterprise_systems/04_process_consulting/219_benchmarking_best_practice/) 등 다양한 기법을 상황에 맞게 조합한다.
> 2. **가치**: 사용자는 **자신이 원하는 것을 정확히 말하지 못하므로**, 다양한 도출 기법으로 <strong>숨겨진 요구(Hidden Requirements)</strong>를 발견해야 한다.
> 3. **판단 포인트**: 프로토타이핑은 <strong>시각적 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a>->피드백</strong>이 빠르고, JAD는 <strong>다부서 합의</strong>에 강하며, 관찰(Ethnography)은 <strong>실제 업무 흐름</strong>을 파악하는 데 최적이다.

---

## Ⅰ. 개요 및 필요성

| 기법 | 강점 | 적합 상황 |
|:---|:---|:---|
| **인터뷰** | 심층 파악 | 핵심 [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) |
| **JAD** | 다부서 합의 | 이해관계 충돌 |
| **프로토타이핑** | 시각적 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | UI/UX 요구 |
| **관찰** | 실제 업무 발견 | 현장 프로세스 |

- **📢 섹션 요약 비유**: 도출 기법은 의사의 <strong>문진 도구(청진기·X-ray·혈액 검사)</strong>이다. 증상마다 다른 도구를 쓴다.

---

## Ⅱ~Ⅴ. 결론

도출 기법은 <strong>단일 기법이 아닌 조합 사용</strong>이 핵심이며, 숨겨진 요구를 발견하는 것이 프로젝트 성공의 관건이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **인터뷰** | 1:1 심층 도출 |
| **JAD** | 다부서 합의 워크숍 |
| **프로토타이핑** | 시각적 피드백 |
| **관찰** | 현장 업무 흐름 파악 |
| **Hidden Requirements** | 도출의 핵심 목표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 인터뷰 (~2000s)] -> [JAD·워크숍 (2005~)]
    -> [프로토타이핑 (2010s)] -> [Design Thinking (2015~)]
    -> [현재: AI 요구 도출 — 대화형 AI로 요구 추출]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 요구 도출은 의사의 <strong>문진</strong>이에요. "어디가 아프세요?" 물어봐요.
2. 청진기(인터뷰), X-ray(프로토타이핑) 등 <strong>여러 도구</strong>를 같이 써요.
3. 환자가 <strong>말 못 하는 증상(숨겨진 요구)</strong>도 찾아내야 좋은 의사예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 973

<- **이전**: [134. 요구사항 공학 프로세스 - 도출->분석->명세->검증->관리 상세](/studynote/04_software_engineering/03_design_architecture/134_requirements_engineering_process/)
**다음**: [136. 브레인스토밍 & JAD - 그룹 기반 요구 도출 기법](/studynote/04_software_engineering/03_design_architecture/136_brainstorming_jad_requirements/) ->

---
