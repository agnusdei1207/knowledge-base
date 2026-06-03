+++
title = "5. 정보시스템 감리기준 (행정안전부 고시)"
description = "행정안전부가 고시한 정보시스템 감리기준의 체계, 주요 내용 및 실무 적용 방법"
date = 2026-04-05

[taxonomies]
tags = ["design_supervision"]

[extra]
tags = ["design_supervision"]
+++

# 05. 정보시스템 감리기준

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정보시스템 감리기준은 행정안전부가 고시하는 공공 정보화 사업 감리의 표준(Supreme Standard)으로, 모든 공공 감리의을보장하는을 가진 기준이다.
> 2. **가치**: 이 기준은 감리의 업무 흐름([Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/) Definition, Planning, Execution, Reporting)을 표준화하여, 감리 사람에 따라 결과가 다르거나 편향되는 문제를한다.
> 3. **융합**: 국제 표준([ISACA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/021_isaca_global_standard/), [COBIT](/knowledge-base/studynote/12_it_management/01_governance_strategy/004_cobit/))과 법률(전자정부법) 사이에서bridge 역할을 하며, 한국 실정에맞는 최적의 감리 프레임워크를 제공한다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

정보시스템 감리기준은 국가가 공공 정보화 사업의 감리 업무를 수행함에 있어 참조해야 할 표준이다. 이 기준이 없다면, 감리마다 다른 방법을 사용하고, 감리 마다 다른 깊이와으로 접근하게 되어, 감리 결과의 일관성과 비교이 отсутствует하게 된다.

예를 들어, A감리법인은 보안 취약점을 47개 항목 점검하는 상세 감리를 수행했고, B감리법인은 간단한 취약점 목록 5개만 확인하고 감리를종료했다고 가정해보자. 발주자는 두 감리 결과를 비교할 수 없고, 사업자는 어떤 수준의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 인정받아야 하는지할 수 없다. 바로 이러한을방지하기 위해 공적 기준이 존재한다.

감리기준의 필요성은 크게 세 가지로 요약된다. 첫째, **모범의**: 가장인 감리을화하여감리 단계에서에와/과을/를하다。 둘째, ** 확보**: 개인적 경험이나bias에의존성하지 않고, 된 검사과 방법론으로 감리를 수행하게 함으로써 결과의을보장한다. 셋째, ** 근거 제공**: 감리 지적 사항의을할 때, 감리인은 "기준 제○조 제○항에 따라문제"이라는한법률를 할 수 있다.

다음 다이어그램은 정보시스템 감리기준이 감리의 을 관통하는 구조를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">정보시스템 감리기준 영역 맵</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감리 전 과정 (End-to-End)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">계획</div><div class="kb-diagram-note">──►</div><div class="kb-diagram-node">준비</div><div class="kb-diagram-note">──►</div><div class="kb-diagram-node">실시</div><div class="kb-diagram-note">──►</div><div class="kb-diagram-node">보고</div><div class="kb-diagram-note">──► [] │</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감리기준 적용 (전 단계 관통)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">관리</div><div class="kb-diagram-node">응용시스템</div><div class="kb-diagram-node">DB/보안</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 통합관리 - 기능요구 - 데이터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 범위관리 - UI/UX - DB 성능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 일정관리 - 테스트 - 접근통제</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 품질관리 - 화면구현 - 암호화</div></div>
</div>
</div>



이 도식의 핵심은 감리기준이 단순히 하나의만 적용하는 것이 아니라, 감리프로세스의 모든 단계([Plan-Do-Check-Act](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/))를 관통하며, 감리 영역의 모든(사업관리, 응용시스템, DB/보안)를 포괄한다는 구조라는 점이다.

📢 **섹션 요약 비유**: 정보시스템 감리기준은 <strong>'음식물안전'의 축제 '</strong>과 같습니다. HACCP(위생관리체계)은 음식점을 점검할 때 전 과정을 빠짐없이 확인하듯이, 감리기준도 정보화 사업의 전 영역을 빠짐없이 점검하도록 하는 방위적 검사 표준입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

정보시스템 감리기준의 내용은 크게 **감리 실시 일반**, **감리 영역별 상세 기준**, **감리 절차 및 방법**, <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/018_audit_report/">감리 보고서</a> 작성 기준</strong>의 네 가지 축으로 구성된다.

**[정보시스템 감리기준 체계]**

| 구분 | 주요 내용 | 핵심 키워드 | 비고 |
|:---|:---|:---|:---|
| **제1편 총칙** | 목적, 용어 정의, 적용 범위 | 감리 대상, 감리 종류, 관련 법령 | 기본 틀 정의 |
| **제2편 감리 실시** | 감리 계획, 준비, 수행, 보고 절차 | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)기술, 증거수집, 분석방법 | [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) 기반 |
| **제3편 감리 영역별 세부기준** | 사업관리, 응용시스템, DB/보안 | [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/),항목 | 핵심 내용 |
| **제4편 감리 증거 및 보고** | 증거의 종류, 보고서 양식, 조치 | [객관적 증거](/knowledge-base/studynote/11_design_supervision/01_audit_framework/056_objective_evidence_collection/), 시정권고 | 법 뒷받침 |

감리기준의 영역별 검사 항목을 수준대별로 정리한 표는 다음과 같다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">감리영역별 수준 구분표</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수준 1 (기본)</div><div class="kb-diagram-cell">수준 2 (표준)</div><div class="kb-diagram-cell">수준 3 (고급)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">사업관리</div><div class="kb-diagram-cell">- 진척 관리</div><div class="kb-diagram-cell">- 진척 관리</div><div class="kb-diagram-cell">- EVM 기반</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 예산 관리</div><div class="kb-diagram-cell">- 예산 관리</div><div class="kb-diagram-cell">- 원가 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 위험 관리</div><div class="kb-diagram-cell">- 리스크</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">응용시스템</div><div class="kb-diagram-cell">- 화면구현</div><div class="kb-diagram-cell">- 화면구현</div><div class="kb-diagram-cell">- UX 심화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 테스트 항목</div><div class="kb-diagram-cell">- 테스트 적정성</div><div class="kb-diagram-cell">- 성능 테스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 코드 분석</div><div class="kb-diagram-cell">- SAST 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DB/보안</div><div class="kb-diagram-cell">- ERD 충실성</div><div class="kb-diagram-cell">- ERD 충실성</div><div class="kb-diagram-cell">- DB 최적화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 백업 확인</div><div class="kb-diagram-cell">- 백업/복구</div><div class="kb-diagram-cell">- DR 실태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 보안 점검</div><div class="kb-diagram-cell">- 모의해킹</div></div>
</div>
</div>



이 수준 구분표의 핵심은 감리가 프로젝트의 규모와 중요도에 따라 적정한 수준의 점검을 수행해야 한다는 점이다. 규모가 작은 사업에 고난도 수준의 감리를 적용하면 오히려 업무이/가하고, 중요한 사업에 기본 수준만 적용하면 risk를 놓칠 수 있다. 감리인은 프로젝트의 특성에 맞게 점검 수준을 조절하는 것이 핵심이다.

📢 **섹션 요약 비유**: 감리기준의 수준 구분은 <strong>'의료 검사 단계'</strong>와 같습니다. 일반 건강검진(수준 1)에서는 기본 혈압,만 보고, 정밀 검사(수준 2)에서는 초음파, MRI를 추가하며, 종합 건강검진(수준 3)에서는 유전체 분석까지 실시하듯이, 감리도 사업 규모에 맞게 적절한 깊이의 점검을 수행합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

정보시스템 감리기준은 표준과 어떻게 다른가? 또한 한국의 특수한에 어떻게맞춰져 있는가?

**[국내 감리기준 vs 국제 표준 비교]**

| 비교 항목 | 행정안전부 감리기준 | [ISACA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/021_isaca_global_standard/) 감리기준 ([CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/)) | [COBIT](/knowledge-base/studynote/12_it_management/01_governance_strategy/004_cobit/) 프레임워크 |
|:---|:---|:---|:---|
| **** | 공공 정보화 사업 (의무감리) | 시스템 (범용) | 기업 IT 거버넌스 |
| **법률적** | 국가 고시 () | 가이드라인 (권고) |Framework (권고) |
| **** | 행정안전부 | [ISACA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/021_isaca_global_standard/) (민간 국제기구) | [ISACA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/021_isaca_global_standard/) (민간 국제기구) |
| **검사** | 공공·민생 밀착형 |보안·통제 위주 | IT 거버넌스·관리-process |
| **특징** | 연계, 한국 반영 | 국제 공인, | 프로세스도 |

이러한 차이에도 불구하고, 두은 상호 보완적으로될 수 있다. 즉, 공공 사업 감리 시에는 국내 기준의 항목과 의 보편적 방법론을 함께 적용하여, 적법성과 적을 동시에 확보할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">국내 감리기준 + 표준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한국형 Fusion Audit Model</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">행정안전부</div><div class="kb-diagram-node">ISACA/CISA</div><div class="kb-diagram-node">COBIT</div></div>
<div class="kb-diagram-note">방법론 기업 거버넌스</div>
<div class="kb-diagram-note">검사프로젝트 프로세스 benchmark</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감리 결과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(+ 적법)</div></div>
</div>
</div>



이 융합 모델의 핵심은 감리기준의 검사프로젝트에 표준의 방법론을 입혀, 모두에서 가능한 감리 결과를 산출하는 것이다. 예를 들어, [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) [47개 보안 약점](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/497_kisa_secure_coding_guide/) 검사는 기준의 필수이지만, 이를 검사하는 기법은 ISACA의 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 방법론을 적용하는 식이다.

📢 **섹션 요약 비유**: 감리기준과 표준의는 <strong>'한국 음식 레시피 + French 기술'</strong>과 같습니다. 기본은 한국 전통 불고기( 기준)이지만, 요리 기술을 French 미식 배운 기술( 방법론)로 보완하여, 한국인도 인도 맛있게 먹는 레스토랑 요리를 만들 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실제 감리 현장에서 감리기준을 적용할 때 발생하는 기술적 판단 사례를 살펴보자.

**1. 판단: "이것은 기능이 아니라 디자인 변경 아닌가?"**
* **상황**: 사업자가 "사용자 만족도 향상을 위한 화면 디자인 개선"이라고 주장하며 추가 비용을 요구했다. 그러나 발주자 RFP에는 없는 항목이었다.
* **기술사적 판단**: 감리기준 제3편 제2장 응용시스템 감리에서 "[요구사항 명세](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/) 대비 기능 구현 여부"를 반드시 점검하도록 규정하고 있다. 따라서 감리인은 RFP 원본 요구사항과 실제 구현 내용을 1:1 대조하여, 해당 항목이 신규 기능인지 단순 디자인 변경인지 명확히 구분해야 한다. 명세에 없는 기능은 추가 비용 소명이 필요하며, 이를 확인하는 것이 감리인의 역할이다.

<strong>2.새로운 기술 적용 판단: "<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 챗봇을 도입했는데, 감리기준에 해당 항목이 없습니다"</strong>
* **상황**:[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 민원 답변 챗봇을 도입했는데, 감리기준의 응용시스템 검사에는AI 관련 세부 기준이 없다.
* **기술사적 판단**: 감리기준은 mínimos 요구사항이지, 기술을하지 않는다.[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 챗봇도 시스템의이므로 기능적 요구사항(민원 자동 답변 정확도), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요구사항([응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)), 보안요구사항([개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) )을 기존 기준프레임워크에 맞춰 적용하면 된다. 핵심은 "기술 중심"이 아닌 "목적 중심"으로 감리기준을 적용하는 유연성이다.

<strong>3.감리 지적 강도 판단: "이 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a>은 Mandatory 개선 대상인가, 권고 대상인가?"</strong>
* **상황**: 감리 결과 일부 화면에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직이 빠져 있지만, 전체 시스템 동작에는 영향을 주지 않는 상황이다.
* **기술사적 판단**: 감리기준에는 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 등급을 Major(필수 시정), Minor(권고 사항)로 구분하는 가이드가 있다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직의는 보호와 직결되므로, 현재 영향이 적더라도 보호조치 미흡은 Major 지적 대상이다. 감리인은 기준의에 얽매이지 말고, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)의 질과 잠재적 영향를 예측하여 적절한 등급을 부여해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">감리기준 적용 의사결정프로세스</div></div>
<div class="kb-diagram-note">1. 해당 항목이 검사인가?</div>
<div class="kb-diagram-note">2. Yes ──&gt; 기준 조항 (제○편 제○장 제○조)</div>
<div class="kb-diagram-note">3. 결함 발견 ──&gt; 영향도 분석 (개인정보/보안/성능/기능)</div>
<div class="kb-diagram-note">4. │ 영향도 High? (보안, 법령 위반)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">── YES ──&gt;</div><div class="kb-diagram-node">Major 지적</div><div class="kb-diagram-note">──&gt; 시정 조치 확인 의무</div></div>
<div class="kb-diagram-note">── NO</div>
<div class="kb-diagram-tree-item" style="--depth:0">즉각적 장애 발생 위험?</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">── YES ──&gt;</div><div class="kb-diagram-node">Major 지적</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">── NO ──&gt;</div><div class="kb-diagram-node">Minor 권고</div><div class="kb-diagram-note">──&gt; 향후 고도화에서 반영</div></div>
</div>
</div>



이 의사결정 플로우의 핵심은 감리기준이 까지_framework일 뿐, 감리인의 전문적 판단을할 수 없다는 점이다. 동일한 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)에 대해서도 감리인의 경험과 뎁스에 따라 다른 등급이 부여될 수 있으므로, 감리인의 역량이 곧 감리의을 결정한다.

📢 **섹션 요약 비유**: 감리기준 적용의 판단은 <strong>'교통 신호등의 판단'</strong>과 같습니다. 신호등(감리기준)이 녹색(기준 충족)인지 빨간색(기준 위반)인지는 명확하지만, 황색(기준 위반이인 경우)은 운전자의 판단(감리인 판단)에 따라 멈출지 진행할지가 결정됩니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

정보시스템 감리기준의 준수를 통해 기대할 수 있는적 효과는 다음과 같다.

| 관점 | 기대 효과 | 정량적 지표 |
|:---|:---|:---|
| **감리의** | 전 동일의 감리서비스 제공 | 감리 결과 90% 이상 향상 |
| ** 경쟁력** | 경쟁 환경 조성 및 불필요한 분쟁 예방 | 감리 관련 분쟁 건수 30% 이상 감소 |
| **발주자 만족** |적 품질 인증으로 의사결정 | 감리 결과 기반 개선율 85% 이상 |
| **감리인 역량** | 전문 감리 인력 양성의 systematic한 기준 확립 | [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) 등 국제 자격보유 50% 이상 향상 |

**미래 전망:**
감리기준은 Fourth Industrial Revolution 기술([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), Big [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), Cloud, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [Blockchain](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/))의 등장에 따라 지속업데이트될 전망이다. 특히 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서의 감리 추가, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 및 윤리 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 항목, 그리고 실시간 모니터링 기반의 지속적 감리(Continuous [Auditing](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)) 방법론의 제도화가 주요 검토로되고 있다.

📢 **섹션 요약 비유**: 미래의 감리기준 발전은 <strong>'자동차 검사 기준 의'</strong>과 같습니다. 처음에는 차체 흠집과 브레이크만 확인했지만, 이제는 연비, 배기가스, 전자제어장치, 자율주행 기능까지 확인하듯이, 정보시스템 감리기준도에 맞춰 계속 진화할 것입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* 행정안전부 고시 | 국가가 공식적으로 발표하는 binding한규칙으로, 공공은 반드시 따라야 함
* [COBIT](/knowledge-base/studynote/12_it_management/01_governance_strategy/004_cobit/) (Control Objectives for Information and Related Technologies) | ISACA가 개발한 IT 거버넌스 및 관리 프레임워크로, 감리기준의 국제적 기반
* [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) (Certified Information Systems Auditor) | ISACA의 공인 정보시스템 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 자격으로, 국제적 감리 전문성 인정
* [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) ([Secure Coding](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/)) | 소스코드 단계에서 보안 약점을 차단하는 coding 규칙으로, 감리기준 보안 항목의 핵심
* [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) ([Plan-Do-Check-Act](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/)) | 감리 업무의전역적 흐름을 나타내는 지속적 개선 사이클

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">행정안전부 고시</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">COBIT (Control Objectives for IT)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CISA (Certified IS Auditor)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시큐어 코딩 (Secure Coding)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">PDCA (Plan-Do-Check-Act)</div></div>
</div>
</div>



이 흐름도는 행정안전부 고시에서 출발해 [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) ([Plan-Do-Check-Act](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 학교 시험에는 반드시 맞춰야 할 출제 범위가 있죠? 감리에도 나라에서 정한 "반드시 점검해야 할 항목"이 있어요. 이것이 바로 감리기준이에요.
2. **원리**: 선생님(감리인)이 이 기준에 맞춰 시험(감리)을 치면, 친구들(사업자)이 어디를해야 하는지 정확히 알 수 있어요.
3. **효과**: 이 기준이 있기에 친구들이 여러 선생님에게 다른 답을 들을 필요 없이, 동일한 기준으로 평가받을 수 있어해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 5 / 530

← **이전**: [4. 전자정부법 제57조 (감리 의무화 규정) - 행정/공공기관의 일정 규모 이상 정보화 사업 의무 감리 지정](/knowledge-base/studynote/11_design_supervision/01_audit_framework/004_egov_law_article_57/)
**다음**: [6. 감리 프레임워크 (Audit Framework) 3차원 구조 - 감리 영역, 감리 관점, 감리 단계](/knowledge-base/studynote/11_design_supervision/01_audit_framework/006_audit_framework_3dimensional/) →

---
