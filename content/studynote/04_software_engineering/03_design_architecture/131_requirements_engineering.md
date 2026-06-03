+++
title = "131. 요구사항 공학 (Requirements 엔진ering) - 체계적 요구 수집·분석·관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구사항 공학은 <strong>요구 도출(Elicitation)→분석(Analysis)→명세(<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/">Specification</a>)→<a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>)→관리(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a>)</strong>의 체계적 프로세스로 소프트웨어가 무엇을 해야 하는지를 정의한다.
> 2. **가치**: 프로젝트 실패의 60%+가 요구사항 문제(누락·모호·변경)에서 발생하며, 개발 후반 요구 변경 비용은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 대비 <strong>50~200배</strong>이므로 체계적 공학이 필수이다.
> 3. **판단 포인트**: 기능 요구사항(FR)과 [비기능 요구사항](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/)([NFR](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))을 구분하고, [요구사항 추적 매트릭스](/knowledge-base/studynote/04_software_engineering/03_design_architecture/157_requirements_traceability_matrix_rtm/)([RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/))로 전 생명주기 추적해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
도출 → 분석 → 명세(SRS) → 검증 → 관리
         ↑____________________________|  (반복)
```

- **📢 섹션 요약 비유**: 요구사항 공학은 건축의 <strong>설계도 작업</strong>이다. 설계도 없이 짓기 시작하면 완공 후 벽을 허물어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 활동 | 핵심 기법 |
|:---|:---|
| **도출** | 인터뷰, 워크숍, 프로토타이핑 |
| **분석** | 우선순위(MoSCoW), 갈등 해결 |
| **명세** | SRS(IEEE 830), 유스케이스 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> | 리뷰, [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **관리** | [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)(추적 매트릭스), [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) |

---

## Ⅲ~Ⅴ. 결론

요구사항 공학은 <strong>프로젝트 성공의 가장 중요한 첫 단추</strong>이며, Agile에서도 [User Story](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/)·BDD로 지속적으로 수행된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SRS** | 요구사항 명세서 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/">RTM</a></strong> | [요구사항 추적 매트릭스](/knowledge-base/studynote/04_software_engineering/03_design_architecture/157_requirements_traceability_matrix_rtm/) |
| **MoSCoW** | 우선순위 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/">User Story</a></strong> | [Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 요구사항 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">NFR</a></strong> | [비기능 요구사항](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/) (품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 요구 수집 (~1990s)] → [IEEE 830 SRS (1998)]
    → [유스케이스 (UML, 2000s)] → [User Story (Agile, 2005~)]
    → [현재: AI 요구사항 분석 — 자연어→요구사항 자동 분류]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 요구사항 공학은 <strong>설계도</strong>예요. 집을 짓기 전에 **뭘 만들지 정확히** 그려야 해요.
2. 설계도 없이 짓으면 **다 짓고 나서 벽을 허물어야** 해서 돈이 50배 더 들어요.
3. "무엇을, 얼마나 빠르게, 얼마나 안전하게" **모두 적어둬야** 완벽한 설계도예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 973

← **이전**: [130. 인수 기준 vs 완료 정의 (Acceptance Criteria vs Definition of Done)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/130_acceptance_criteria_vs_dod/)
**다음**: [132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류](/knowledge-base/studynote/04_software_engineering/03_design_architecture/132_types_of_requirements/) →

---
