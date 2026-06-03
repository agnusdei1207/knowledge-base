+++
weight = 131
title = "131. 요구사항 공학 (Requirements Engineering) - 체계적 요구 수집·분석·관리"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구사항 공학은 **요구 도출(Elicitation)→분석(Analysis)→명세([[148_requirements_specification_formal_informal|Specification]])→[[395_verification_process_review|검증]]([[396_validation|Validation]])→관리([[372_management|Management]])**의 체계적 프로세스로 소프트웨어가 무엇을 해야 하는지를 정의한다.
> 2. **가치**: 프로젝트 실패의 60%+가 요구사항 문제(누락·모호·변경)에서 발생하며, 개발 후반 요구 변경 비용은 [[459_quic_fec_forward_error_correction|초기]] 대비 **50~200배**이므로 체계적 공학이 필수이다.
> 3. **판단 포인트**: 기능 요구사항(FR)과 [[133_non_functional_requirements|비기능 요구사항]]([[133_non_functional_requirements|NFR]], [[282_performance_tactics|성능]]·보안·[[452_availability|가용성]])을 구분하고, [[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]]([[667_requirements_traceability_matrix|RTM]])로 전 생명주기 추적해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
도출 → 분석 → 명세(SRS) → 검증 → 관리
         ↑____________________________|  (반복)
```

- **📢 섹션 요약 비유**: 요구사항 공학은 건축의 **설계도 작업**이다. 설계도 없이 짓기 시작하면 완공 후 벽을 허물어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 활동 | 핵심 기법 |
|:---|:---|
| **도출** | 인터뷰, 워크숍, 프로토타이핑 |
| **분석** | 우선순위(MoSCoW), 갈등 해결 |
| **명세** | SRS(IEEE 830), 유스케이스 |
| **[[395_verification_process_review|검증]]** | 리뷰, [[257_prototype_pattern_object_cloning|프로토타입]] [[395_verification_process_review|검증]] |
| **관리** | [[667_requirements_traceability_matrix|RTM]](추적 매트릭스), [[079_change_enablement|변경 관리]] |

---

## Ⅲ~Ⅴ. 결론

요구사항 공학은 **프로젝트 성공의 가장 중요한 첫 단추**이며, Agile에서도 [[081_user_story_invest|User Story]]·BDD로 지속적으로 수행된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SRS** | 요구사항 명세서 |
| **[[667_requirements_traceability_matrix|RTM]]** | [[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]] |
| **MoSCoW** | 우선순위 [[104_classification_analysis|분류]] |
| **[[081_user_story_invest|User Story]]** | [[004_agile_relation|Agile]] 요구사항 |
| **[[133_non_functional_requirements|NFR]]** | [[133_non_functional_requirements|비기능 요구사항]] (품질 [[082_attribute_types_er_model|속성]]) |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 요구 수집 (~1990s)] → [IEEE 830 SRS (1998)]
    → [유스케이스 (UML, 2000s)] → [User Story (Agile, 2005~)]
    → [현재: AI 요구사항 분석 — 자연어→요구사항 자동 분류]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 요구사항 공학은 **설계도**예요. 집을 짓기 전에 **뭘 만들지 정확히** 그려야 해요.
2. 설계도 없이 짓으면 **다 짓고 나서 벽을 허물어야** 해서 돈이 50배 더 들어요.
3. "무엇을, 얼마나 빠르게, 얼마나 안전하게" **모두 적어둬야** 완벽한 설계도예요!
