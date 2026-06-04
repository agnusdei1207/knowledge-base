+++
title = "491. SAST (Static Application Security Testing) - 소스코드 정적 분석 도구 (보안 룰셋 기반)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) - 소스코드 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구 (보안 룰셋 기반)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: SAST는 소스코드를 읽는 '규칙 기반(Rule-based)' 스캐너 봇이다. 기계가 코드를 텍스트로 쭉 읽다가 `Statement sql = "SELECT * FROM users WHERE name='" + input + "'"` 라는 문장을 발견하면, 내장된 족보(CWE-89)와 비교해보고 "야! 문자열 덧셈으로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 짜면 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/872_injection/) 터지잖아!"라며 빨간 줄을 쫙 긋는다. 프로그램이 켜지기도(런타임) 전인 '컴파일(Compile) 혹은 텍스트 상태'에서 모든 검사가 1분 만에 끝난다.

- **필요성**: 보안팀원 3명이 1,000만 줄의 은행 코드를 일일이 눈으로 읽고(Manual [Code Review](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)) 해킹 구멍을 찾는 것은 미친 짓이다. 게다가 버그 하나 고치는 비용은 코드를 방금 짠 순간에 고치면 10분이지만, 오픈 당일(런타임)에 DAST나 모의 해킹으로 터지면 1달이 걸린다. <strong>"인간의 나태함(실수)을 가장 빠르고, 가장 싸고, 가장 기계적인 방식으로 통제하기 위한 자동화된 린터(Linter)의 확장판"</strong>으로서 SAST가 전 세계 개발 파이프라인의 필수 문지기로 자리 잡았다.

- **💡 비유**: SAST는 건물 짓기 전의 <strong>'설계도면 엑스레이 검수'</strong>와 같습니다. 건물을 다 짓고 나서 흔들어보며([DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)) 무너지는지 확인하는 건 하수입니다. SAST는 아직 콘크리트를 붓기도 전에(프로그램 실행 전), 종이 도면(소스코드)만 쓱 훑어보고 "어? 이 기둥 두께가 10cm면 지진(해킹) 났을 때 100% 무너지겠는데?"라고 족집게처럼 찾아내어 도면 자체를 고치게 만드는 가장 안전한 예방 기술입니다.

- **등장 배경 및 발전 과정**:
  1. **수동 리뷰의 붕괴**: 90년대엔 보안 전문가가 며칠 밤을 새워 코드를 한 줄씩 읽었다([Auditing](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)). 하지만 코드량이 폭발하며 불가능해졌다.
  2. **패턴 매칭 스캐너의 등장 (2000s)**: 단순하게 정규표현식으로 `strcpy()` 나 `password=` 같은 위험한 문자열을 무식하게 찾는(Grep) 1세대 SAST 툴들이 등장했다. 오탐(가짜 경고)이 90%라 욕을 먹었다.
  3. <strong>AST 기반 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 분석 (현재)</strong>: 코드를 문자열이 아닌 **추상 구문 트리(AST)** 형태의 거대한 수학 구조도로 변환한 뒤, "입력값(Source)이 필터링 안 거치고 DB(Sink)까지 흘러가는가?([Taint](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/) Analysis)"를 완벽하게 추적해 내는 [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/), Checkmarx 등 초정밀 3세대 분석기로 진화했다.

- **📢 섹션 요약 비유**: SAST는 맞춤법 검사기(Linter)의 <strong>'형사반장 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a>'</strong>입니다. 맞춤법 검사기가 "띄어쓰기가 틀렸네"라고 잔소리하는 거라면, SAST 형사반장은 "너 방금 비밀번호(Evidence)를 암호화도 안 하고 텍스트 파일에 쓰는 범죄(CWE-259)를 저질렀네? 당장 감방(빌드 Fail) 가!"라고 엄벌을 내리는 무서운 코드 경찰입니다.

---

다음은 SAST (Static Applica의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  SAST (Static Applica                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 SAST (Static Applica가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) - 소스코드 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구 (보안 룰셋 기반)의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
SAST (Static Application Security Testing) 개념 정립
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

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SAST (Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 574 / 973

<- **이전**: [491. SAST (Static Application Security Testing)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/883_sast/)
**다음**: [492. DAST (Dynamic Application Security Testing)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/884_dast/) ->

---
