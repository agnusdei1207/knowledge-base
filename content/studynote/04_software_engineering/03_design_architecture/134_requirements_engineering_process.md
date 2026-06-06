---
title: "134. Requirements Engineering Process"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구 도출(Elicitation)->분석(Analysis)->명세([Specification](/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/), SRS)->[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Validation](/studynote/04_software_engineering/12_testing_maintenance/396_validation/))->관리([Management](/studynote/12_it_management/05_security_compliance/1013_management/)) 5단계를 반복 순환하며, 각 단계마다 고유한 기법과 산출물이 있다.
> 2. **가치**: 도출 기법(인터뷰·워크숍·프로토타이핑)을 적절히 조합해야 <strong>숨겨진 요구사항(Hidden Requirements)</strong>을 발견할 수 있고, 명세의 품질이 전체 프로젝트 품질을 결정한다.
> 3. **판단 포인트**: 도출 기법 선택, SRS 구조(IEEE 830), [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(리뷰·[프로토타입](/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/)·[테스트 케이스](/studynote/04_software_engineering/11_testing_validation/833_test_case/)), [RTM](/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)(요구->설계->코드->테스트 추적)이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
도출: 인터뷰·JAD·브레인스토밍·프로토타이핑
분석: 우선순위(MoSCoW), 갈등 해결, 실현 가능성
명세: SRS (IEEE 830), 유스케이스, User Story
검증: 리뷰·워크스루·프로토타입
관리: RTM, 변경 관리(CCB), 형상 관리
```

- **📢 섹션 요약 비유**: 요구 프로세스는 의사의 진료(도출=문진, 분석=진단, 명세=처방전, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)=경과관찰, 관리=진료기록)이다.

---

## Ⅱ~Ⅴ. 결론

체계적 요구 프로세스는 <strong>"올바른 시스템을 올바르게 만드는" 첫걸음</strong>이며, RTM이 전 생명주기 추적의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **도출** | 인터뷰·JAD·프로토타이핑 |
| **SRS** | IEEE 830 명세서 |
| <strong><a href="/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/">RTM</a></strong> | 요구->테스트 추적 |
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a></strong> | [변경 통제 위원회](/studynote/12_it_management/02_itsm_itil/080_cab/) |
| **MoSCoW** | 우선순위 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 요구 수집] -> [IEEE 830 SRS (1998)] -> [유스케이스 (UML)]
    -> [User Story (Agile)] -> [현재: AI 요구 분석 — 자연어->요구 자동 분류]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 요구 프로세스는 <strong>의사 진료</strong>예요. 먼저 어디 아프냐(도출) 물어봐요.
2. 진단(분석) 후 **처방전(명세)** 을 써요.
3. 약을 먹고 <strong>경과를 지켜보며(<a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>)</strong> 진료 기록(관리)을 남겨요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 973

<- **이전**: [133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의](/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/)
**다음**: [135. 요구사항 도출 기법 - 인터뷰·JAD·프로토타이핑·브레인스토밍](/studynote/04_software_engineering/03_design_architecture/135_requirements_elicitation_techniques/) ->

---
