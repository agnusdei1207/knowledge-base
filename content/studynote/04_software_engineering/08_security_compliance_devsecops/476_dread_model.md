+++
title = "476. DREAD 모델 - 위협 리스크 산정 지표 (Damage, Reproducibility, Exploitability, Affected users, Discoverability)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DREAD 모델 - 위협 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 산정 지표 (Damage, Reproducibility, Exploitability, Affected users, Discoverability)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 마이크로소프트가 고안한 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 점수화 기법. 5개의 영단어 앞 글자를 땄다. 위협 하나를 잡고, 각 5개 항목에 1점(낮음) ~ 10점(높음)을 매긴다. 그리고 그 점수들의 평균을 내어 "이 취약점은 DREAD 8점(High [Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/))짜리 폭탄이다"라고 수치화한다.
  - **D**amage (피해가 얼마나 큰가?)
  - **R**eproducibility (다시 터뜨리기 쉬운가?)
  - **E**xploitability (해킹하기 쉬운가?)
  - **A**ffected Users (몇 명이 피해를 보나?)
  - **D**iscoverability (해커가 이 구멍을 찾기 쉬운가?)

- **필요성**: 보안팀이 위협 모델링을 신나게 해서 "잠재적 취약점 50개 발견!" 리포트를 개발팀장에게 던지고 갔다. 다음 주가 앱 출시인데 50개를 언제 다 고치나? 팀장은 분노한다. 이때 리포트를 유심히 보니, 49개는 "해커가 서버실을 도끼로 부수고 들어와서 램(RAM)을 뜯어가면 정보가 털림(현실성 0%)" 같은 헛소리들이고, 단 1개만이 "비밀번호가 평문으로 날아감(현실성 100%)"이었다. 이처럼 <strong>"막연한 공포"를 "정확한 확률과 파괴력(<a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">Risk</a> = Impact x <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">Probability</a>)"으로 분리해 내어, 한정된 자원(인건비)을 급소 방어에만 쏟아붓기 위해</strong> DREAD라는 수학적 저울이 필요하다.

- **💡 비유**: DREAD는 응급실의 <strong>'환자 중증도 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>(Triage) 시스템'</strong>과 같습니다. 응급실에 환자 50명이 한꺼번에 몰려왔습니다. 의사가 아무나 먼저 온 순서대로 진료(패치)하면, 감기 환자 고치다가 심장마비 환자는 대기실에서 죽습니다. DREAD는 들어오는 환자 이마에 즉시 "생명 위독(9점, 즉각 수술)", "팔 부러짐(6점, 30분 대기)", "찰과상(1점, 집에 가라)" 딱지를 칼같이 붙여서 의사(개발자)가 누구의 목숨부터 살릴지 정해주는 가장 자비 없는 생존 룰입니다.

- **등장 배경 및 발전 과정**:
  1. **주먹구구식 공포 마케팅**: 90년대 보안 업체들은 취약점 1개만 찾아도 "회사 망합니다! 우리 솔루션 10억 주고 사세요!"라고 사기를 쳤다.
  2. <strong><a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a> 기반 사고(<a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">Risk</a>-based Thinking) 도래</strong>: 마이크로소프트가 STRIDE를 만들며 위협을 왕창 찾아냈는데, 개발자들이 고치다 지쳐 쓰러졌다. 그래서 "점수 매겨서 상위 20%만 고쳐라"라며 DREAD를 짝꿍으로 발표했다.
  3. **CVSS의 대중화와 DREAD의 쇠퇴/진화**: DREAD는 '평가자의 주관적 느낌'이 개입한다는 비판을 받았다. 그래서 전 세계 보안 학계는 이를 더 객관화시킨 <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/">CVSS</a>(공통 취약점 등급 시스템, 1~10점)</strong>라는 글로벌 절대 표준으로 진화시켰다. 하지만 아키텍처 설계 단계(오픈 전)의 직관적 브레인스토밍용으로는 여전히 DREAD가 사랑받고 있다.

- **📢 섹션 요약 비유**: STRIDE가 쓰레기 더미에서 <strong>'금조각 1개와 돌멩이 99개'</strong>를 전부 다 건져 올리는 뜰채라면, DREAD는 그 100개를 감정사 안경을 끼고 쳐다보며 <strong>"이건 10억 원짜리 순금(즉각 패치), 이건 0원짜리 돌멩이(무시)"</strong>라고 가격표를 정확히 매겨 쓰레기를 갖다 버리게 해주는 냉혹한 보석 감정사입니다.

---

다음은 DREAD 모델의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  DREAD 모델                                    |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 DREAD 모델가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

DREAD 모델 - 위협 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 산정 지표 (Damage, Reproducibility, Exploitability, Affected users, Discoverability)의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

DREAD 모델의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: DREAD 모델의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

DREAD 모델을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | DREAD 모델 | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, DREAD 모델은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: DREAD 모델과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

DREAD 모델을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: DREAD 모델은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

DREAD 모델을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

DREAD 모델은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: DREAD 모델의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | DREAD 모델의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | DREAD 모델은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | DREAD 모델 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | DREAD 모델에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
DREAD 모델 개념 정립
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

1. DREAD 모델은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 544 / 973

<- **이전**: [476. DREAD 모델 (DREAD Model)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/476_dread_model/)
**다음**: [477. OWASP Top 10 (2021 기준 주요 취약점)](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/477_owasp_top_10/) ->

---
