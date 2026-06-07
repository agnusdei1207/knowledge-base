---
title: "190. Ai Llm Requirements Specification"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
weight: 190
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

ChatGPT, Claude와 같은 <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/">대규모 언어 모델</a>(<a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a>, <a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">Large Language Model</a>)</strong> 을 활용하여, 고객과의 인터뷰 스크립트나 모호한 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 요구사항 텍스트를 입력받아 정형화된 <strong><a href="/studynote/04_software_engineering/03_design_architecture/149_software_requirements_specification_srs/">소프트웨어 요구사항 명세서</a>(SRS, Software Requirements <a href="/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/">Specification</a>)</strong> 나 <strong>유스케이스(Use Case) 초안을 자동으로 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>하고 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>하는 차세대 요구공학 기법입니다.

- **📢 섹션 요약 비유**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

다음은 AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  AI(LLM) 기반 요구사항 명세서                         |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 결과물을 산출하는 흐름을 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 요구공학 단계 | 기존의 방식 (사람) | AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 지원 방식 |
|:---|:---|:---|
| **1. 도출 (Elicitation)** | 회의록을 들으며 수기로 요구사항 정리 | 회의 [STT](/studynote/03_network/16_data_center_cloud/819_stt_stateless_transport_tunneling_offload/)(음성 -> 텍스트) 데이터를 분석해 **숨겨진 핵심 요구사항(Actor, Action, Goal) 자동 추출** |
| **2. 분석 (Analysis)** | 수백 개의 요구사항 간 충돌(모순) 여부 눈으로 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 수백 개의 문장을 벡터 유사도로 비교하여 **기능적 충돌 및 누락된 엣지 케이스(예외 상황) 자동 경고** |
| <strong>3. 명세 (<a href="/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/">Specification</a>)</strong>| [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)/엑셀 템플릿에 맞추어 하루 종일 타이핑 | 지시한 템플릿(예: BDD의 Given-When-Then, IEEE 830)에 맞춰 <strong>완벽한 형식의 초안 문서 즉시 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong> |
| <strong>4. <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> (<a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>)</strong> | 리뷰 회의를 열어 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 기반 수동 검사 | "ISO 27001 보안 표준에 위배되는 요구사항을 찾아라" 지시로 <strong>보안/<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 제약 사항 자동 <a href="/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/">교차 검증</a></strong> |

- **📢 섹션 요약 비유**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

## Ⅲ. 비교 및 연결

AI가 제대로 된 명세서를 뽑아내게 하려면, 기획자나 분석가([BA](/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))가 **"어떻게 질문할 것인가(프롬프트)"** 가 가장 중요해집니다.
- **예시 프롬프트**: *"이 회의록을 바탕으로, 쇼핑몰 장바구니 결제 기능에 대한 요구사항 명세서를 작성해 줘. 1. 페르소나는 20대 여성, 2. [비기능 요구사항](/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/)(응답속도, 보안) 분리, 3. 포맷은 [BDD](/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/)(Given-When-Then) 구조를 사용할 것."*

- **📢 섹션 요약 비유**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/">할루시네이션</a> (<a href="/studynote/06_ict_convergence/04_ai_llm/275_react_framework/">환각</a>)</strong>: AI가 그럴듯한 거짓 기능(고객이 말하지도 않은 기능)을 멋대로 추가해 버릴 수 있어, <strong>반드시 인간(Human-in-the-Loop)의 최종 리뷰와 승인이 필수</strong>입니다.
- **보안/기밀 유출**: 기업의 핵심 비즈니스 로직이나 민감한 고객 정보가 퍼블릭 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(오픈AI 서버 등)으로 넘어가는 것을 막기 위해, 사내 전용 구축형 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([On-Premise](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) sLLM) 도입이 동반되어야 합니다.

> 📢 **섹션 요약 비유**: 엉망진창으로 녹음된 "고객의 하소연 테이프"를 숙련된 타이피스트이자 법무사인 AI 비서에게 건네주면, 비서가 하소연 속에서 '계약 조건', '위약금', '면책 조항'을 완벽한 법률 문서(요구사항 명세서) 포맷으로 찍어내어 결재를 올리는 환상적인 업무 자동화입니다.

- **📢 섹션 요약 비유**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

## Ⅴ. 기대효과 및 결론

AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원을(를) 올바르게 적용하면 [소프트웨어 품질](/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- AI·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)·[DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원 적용 결과는 QA 활동을 통해 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원에서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
AI(LLM) 기반 요구사항 명세서 초안 자동 생성 지원 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. AI([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 기반 요구사항 명세서 초안 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지원은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 190 / 973

<- **이전**: [189. BDD의 Given-When-Then 문법을 이용한 명세](/studynote/04_software_engineering/03_design_architecture/189_bdd_given_when_then/)
**다음**: [191. 소프트웨어 설계 원칙 - 추상화, 캡슐화, 모듈화, 정보 은닉](/studynote/04_software_engineering/04_testing_quality/191_software_design_principles/) ->

---
