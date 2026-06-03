---
title: 195. 결합도 (Coupling) - 모듈 간 상호 의존 정도 (낮을수록 좋음)
date: '2026-05-08'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 결합도 (Coupling) - [[192_module_independence|모듈]] 간 상호 의존 정도 (낮을수록 좋음)은(는) [[001_software_engineering_definition|소프트웨어 공학]]의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[[346_maintainability_portability|유지보수성]]·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[001_software_engineering_definition|소프트웨어 공학]]에서 **어떤 [[192_module_independence|모듈]]이 다른 [[192_module_independence|모듈]]에 의존하는 정도(연관성), 혹은 [[192_module_independence|모듈]] 간에 [[001_dikw_pyramid|데이터]]를 주고받는 끈끈함의 정도**를 의미합니다.
[[193_cohesion_levels|응집도]]([[193_cohesion_levels|Cohesion]])가 [[192_module_independence|모듈]] '내부'의 똘똘 뭉친 정도라면, 결합도는 [[192_module_independence|모듈]] '외부([[192_module_independence|모듈]]과 [[192_module_independence|모듈]] 사이)'의 연결 고리를 나타냅니다.

- **📢 섹션 요약 비유**: 결합도 (Coupling)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

다음은 결합도 (Coupling)의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  결합도 (Coupling)                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 결합도 (Coupling)가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[192_module_independence|모듈]] A와 [[192_module_independence|모듈]] B의 결합도가 너무 높으면, **A 코드를 한 줄 고쳤는데 전혀 상관없는 B [[192_module_independence|모듈]]에서 에러가 터지는 대참사(사이드 이펙트)** 가 발생합니다.
반대로 결합도가 낮으면(느슨하면), B [[192_module_independence|모듈]]을 통째로 덜어내고 다른 [[192_module_independence|모듈]]로 교체하더라도 A [[192_module_independence|모듈]]은 자신이 하던 일을 아무런 영향 없이 계속할 수 있습니다. 이것이 객체지향 설계의 핵심인 '유연성(Flexibility)'입니다.

- **📢 섹션 요약 비유**: 결합도 (Coupling)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | 결합도 (Coupling)의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

## Ⅲ. 비교 및 연결

정보처리기사 단골 문제이며, [[193_cohesion_levels|응집도]]와 마찬가지로 순서를 외우는 것이 중요합니다. **(나쁨) 내-공-제-스-자 (좋음)**

1. **내용 (Content) 결합도 - [최악 💩]**
   - [[192_module_independence|모듈]] A가 [[192_module_independence|모듈]] B의 **내부 변수나 코드를 직접 가져다 쓰거나 수정**하는 상태입니다. B가 변수를 바꾸면 A도 무조건 죽습니다. (예: `goto` 문으로 다른 [[192_module_independence|모듈]] 내부로 침투)
2. **공통 (Common) 결합도**
   - 두 [[192_module_independence|모듈]]이 외부에 있는 **글로벌(전역) 변수를 공유**하여 사용하는 상태입니다. 전역 변수의 값이 바뀌면 이 변수를 쓰는 수백 개의 [[192_module_independence|모듈]]이 동시에 영향을 받습니다.
3. **제어 (Control) 결합도**
   - [[192_module_independence|모듈]] A가 [[192_module_independence|모듈]] B에게 단순히 [[001_dikw_pyramid|데이터]]를 넘기는 게 아니라, **"너 이쪽 분기 타라"고 제어 [[130_signal|신호]]([[186_character_stuffing_dle_stx_etx|Flag]], Boolean 등)를 보내어 B의 내부 로직 흐름을 직접 통제**하는 상태입니다. (B의 자율성이 침해됨)
4. **스탬프 (Stamp / 검인) 결합도**
   - [[192_module_independence|모듈]] 간에 [[001_dikw_pyramid|데이터]]를 주고받을 때 배열이나 객체(Object), [[001_dikw_pyramid|데이터]] 구조체(Record) 등 **복잡한 포장지 통째로** 넘기는 상태입니다. 실제로는 그 객체 안의 변수 1개만 필요한데 구조체 전체를 의존하게 되는 부작용이 있습니다.
5. **자료 ([[001_dikw_pyramid|Data]]) 결합도 - [최고 🌟]**
   - [[192_module_independence|모듈]]끼리 **오직 꼭 필요한 단순 [[001_dikw_pyramid|데이터]](파라미터, 숫자, 문자열)만** 매개변수로 주고받는 가장 느슨하고 완벽한 상태입니다. B [[192_module_independence|모듈]]이 내부적으로 어떻게 돌아가든 A는 파라미터만 넘겨주면 그만입니다.

- **📢 섹션 요약 비유**: 결합도 (Coupling)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대 소프트웨어에서는 제어 결합도나 내용 결합도를 끊어내기 위해 **인터페이스(Interface)** 를 두고 통신하거나, Spring 프레임워크처럼 외부에서 [[192_module_independence|모듈]]을 끼워 넣어주는 **[[337_dependency_injection|의존성 주입]]([[337_dependency_injection|Dependency Injection]], [[190_enterprise_di_framework_lifecycle|DI]])** 기법을 사용하여 결합도를 강제로 낮춥니다.

> 📢 **섹션 요약 비유**: 회사 동료에게 일을 시킬 때, 그 직원의 다이어리(내부 변수)를 내가 맘대로 훔쳐보고 고치면 내용 결합도(최악)입니다. 대신 깔끔한 회사 양식(인터페이스)에 '이름'과 '금액'(자료 결합도)만 딱 적어서 넘겨주고 그 직원이 알아서 일하게 냅두는 것이 최고의 업무 효율(최저 결합도)을 냅니다.

- **📢 섹션 요약 비유**: 결합도 (Coupling)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

## Ⅴ. 기대효과 및 결론

결합도 (Coupling)을(를) 올바르게 적용하면 [[339_software_quality_definition|소프트웨어 품질]]·[[346_maintainability_portability|유지보수성]]·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [[459_quic_fec_forward_error_correction|초기]] 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [[459_quic_fec_forward_error_correction|초기]] 비용이 발생한다

**미래 발전 방향**:
- [[190_ai_llm_requirements_specification|AI]]·[[263_llm_large_language_model|LLM]] 기반 자동화 도구와의 통합으로 적용 효율 향상
- [[531_cloud_native_architecture|클라우드 네이티브]]·[[652_devops_calms_culture|DevOps]] 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

결합도 (Coupling)은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: 결합도 (Coupling)의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [[001_software_engineering_definition|소프트웨어 공학]]의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]]) | 결합도 (Coupling)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle) | 결합도 (Coupling)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | 결합도 (Coupling) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]]) | 결합도 (Coupling)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
결합도 (Coupling) 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [[002_software_crisis|소프트웨어 위기]] 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 결합도 (Coupling)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [[001_software_engineering_definition|소프트웨어 공학]]은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 195 / 973

← **이전**: [[194_cohesion_7_levels|194. 응집도 단계 - 우연적, 논리적, 시간적, 절차적, 통신적, 순차적, 기능적 응집도]]
**다음**: [[196_coupling_5_levels|196. 결합도 단계 - 내용, 공통, 제어, 스탬프, 자료 결합도]] →

---
