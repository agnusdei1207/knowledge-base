+++
title = "658. 애자일 스크럼 (Scrum) 역할 분담"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

전통적인 폭포수(Waterfall) 프로젝트에서는 시스템 오픈을 하고 모든 일정이 끝난 뒤(6개월~1년 뒤)에야 '포스트모템(Post-mortem, 사후 분석)' 회의를 했다. "우리 그때 요구사항 분석을 잘못해서 망할 뻔했지..."라고 후회해 봤자 프로젝트는 이미 끝나버려서 개선할 기회가 없었다.

[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/))은 이를 비판했다. <strong>"1년 뒤에 반성하지 말고, 2주에 한 번씩(<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/">스프린트</a> 종료 시) 우리가 어떻게 일했는지 반성하고 바로 다음 날부터 고쳐서 일하자!"</strong>

이 위대한 성찰의 시간이 바로 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/">스프린트 회고</a>(<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/">Sprint Retrospective</a>)</strong>다. 회고가 없는 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/)은 그저 2주 단위로 코딩만 미친 듯이 찍어내는 기계 공장(Mini-waterfall)일 뿐, 진정한 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)이 아니다.

- **📢 섹션 요약 비유**: 옛날엔 수능 시험이 다 끝난 뒤에야 "아, 수학부터 풀걸" 하고 후회했다(폭포수). [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 회고는 모의고사를 볼 때마다 끝나고 모여서 "이번엔 시간이 모자랐으니 다음엔 영어부터 풀자(Action Item)"라고 작전을 고치며 진짜 수능(오픈)을 준비하는 과정이다.

---

다음은 [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  애자일 스크럼 (Scrum) 역할 분                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

회고는 그냥 모여서 수다를 떠는 시간이 아니다. 보통 KPT, 4L 등의 프레임워크를 사용하여 체계적으로 진행된다.

- **📢 섹션 요약 비유**: [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

---

## Ⅲ. 비교 및 연결

[스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/)에는 헷갈리는 3가지 핵심 회의가 있다. 누구를 대상으로, 무엇을 리뷰하는지에 따라 목적이 다르다.

| 회의 종류 | 영문 명칭 | 목적 | 대상 (What to [review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/)) | 참여자 |
|:---|:---|:---|:---|:---|
| <strong>일일 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/">스크럼</a></strong> | [Daily Scrum](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/069_daily_standup_scrum/) | 오늘 하루의 병목(Blocker) 해결 | 어제 한 일, 오늘 할 일, 방해물 | 개발팀, [스크럼 마스터](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/064_scrum_master_sm/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/">스프린트 리뷰</a></strong>| [Sprint Review](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/) | 만들어진 **'제품(Product)'** 시연 | **소프트웨어 (기능/코드)** | 고객(PO), 개발팀 전원 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/">스프린트 회고</a></strong>| [Sprint Retrospective](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/)| 우리의 <strong>'일하는 방식(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/">Process</a>)'</strong> 반성 | **팀워크, 소통, 개발 도구** | [스크럼 마스터](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/064_scrum_master_sm/), 개발팀 |

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/">스프린트 리뷰</a></strong>가 끝나면 "이 버튼 색깔을 파란색으로 바꾸자"는 백로그(기능 요구사항)가 나오고, <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/">스프린트 회고</a></strong>가 끝나면 "[코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) 시간을 오후 2시로 고정하자"는 액션 아이템(행동 규칙)이 나온다.

- **📢 섹션 요약 비유**: 일일 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/)은 선수들이 벤치에서 "오늘 컨디션 어때?" 묻는 것이고, [스프린트 리뷰](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/)는 "오늘 우리가 2골 넣었네!" 하고 경기 결과를 칭찬하는 것이며, [스프린트 회고](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/)는 라커룸에서 비디오를 보며 "오늘 패스 워크가 안 좋았으니 내일은 포메이션을 바꾸자"고 전술을 고치는 것이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

회고는 100% 심리학이다. 팀장이나 기술 리더가 완장(권위)을 차는 순간 회고는 처참하게 망가진다.

- **📢 섹션 요약 비유**: [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

[스프린트 회고](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/)가 건강하게 돌아가는 팀은 '자기 주도적(Self-organizing)' 팀으로 진화한다. 팀원들 스스로 불합리한 프로세스를 부수고, 새로운 도구를 도입하며 끊임없이 체질을 개선(Continuous Improvement)하기 때문에 생산성이 복리의 마법처럼 우상향한다.

결론적으로 소프트웨어는 코드가 짜는 게 아니라 사람이 짠다. 코드를 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))하는 것만큼, <strong>'팀이 일하는 방식'을 <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/">리팩토링</a>하는 시간</strong>이 반드시 필요하다. 기술 리더는 기능 개발 일정이 아무리 쫓겨도 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 마지막 날의 2시간짜리 회고를 목숨처럼 사수해야 한다. 회고를 포기하는 것은, 녹슨 톱날을 갈지 않고 계속 나무를 베겠다고 고집부리는 미련함과 같다.

- **📢 섹션 요약 비유**: 칼을 가는 시간(회고)은 낭비가 아니다. 10분 동안 무딘 칼로 무를 써는 것보다, 2분 동안 칼을 갈고 1분 만에 무를 썰어버리는 것이 진짜 속도([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/))다. 회고는 우리 팀의 무뎌진 칼날을 뾰족하게 벼리는 가장 날카로운 시간이다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
애자일 스크럼 (Scrum) 역할 분담 개념 정립
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

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [애자일 스크럼](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) ([Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)) 역할 분담은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 827 / 973

← **이전**: [658. 애자일 스크럼 (Scrum) 역할 분담](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)
**다음**: [659. 스프린트 백로그 / 프로덕트 백로그](/knowledge-base/studynote/04_software_engineering/uncategorized/659_sprint_product_backlog/) →

---
