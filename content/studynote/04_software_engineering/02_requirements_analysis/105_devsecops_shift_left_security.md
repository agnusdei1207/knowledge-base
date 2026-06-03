+++
title = "105. DevSecOps - 보안의 좌측 이동 (Shift-Left Security)"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) (Development, [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), and Operations)의 핵심인 '보안의 좌측 이동 ([Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))'은 소프트웨어 개발 수명 주기 ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/))의 맨 우측(마지막 배포 단계)에 있던 보안 검사를 맨 좌측(기획 및 코딩 단계)으로 전진 배치하는 사상이다.
> 2. **가치**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/) / [Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/)) 파이프라인 내부에 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)([SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)), [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 분석([SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/)) 등의 자동화 도구를 심어, 보안 통제가 개발 속도를 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시키는 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/)) 현상을 원천적으로 제거한다.
> 3. **판단 포인트**: 취약점을 배포 전에 미리 발견하고 차단함으로써 수정에 드는 재작업 비용(Rework Cost)을 기하급수적으로 낮추는, 품질과 속도의 동시 달성 전략이다.

---

## Ⅰ. 개요 및 필요성

과거의 개발 패러다임에서 보안([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))은 소프트웨어 개발 수명 주기 ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/); Software Development Life Cycle)의 맨 마지막인 릴리스 직전에 수행되는 통제 및 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 행위였다. 개발과 운영 부서가 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 문화를 도입하여 하루에도 수십 번씩 코드를 자동 배포하며 속도전을 벌이기 시작하자, 전통적이고 수동적인 보안 검사 부서는 치명적인 병목 현상의 주범으로 전락하고 말았다. 

빠르게 코드를 짰음에도 배포 직전 보안팀이 모의 해킹과 진단을 위해 2주간 승인을 멈추고, 심지어 치명적 취약점이 발견되어 처음부터 다시 개발(Rework)하라고 코드를 엎어버리는 비극이 속출했다. 이러한 모순을 해결하기 위해 등장한 것이 보안의 좌측 이동 ([Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))이다. 파이프라인의 오른쪽(끝)에 뭉쳐 있던 무거운 보안 통제를 왼쪽(시작점), 즉 개발자의 IDE 에디터나 소스 코드 커밋 순간으로 끌고 와서 자동화된 로봇에게 검사를 맡기자는 혁명적 전환이다.

- **📢 섹션 요약 비유**: 기존 보안은 완성된 자동차를 출고 직전에 망치로 두드려보며 불량이면 폐차하는 아찔한 '충돌 테스트'였다면, [Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) 보안은 자동차 조립 공정의 첫 번째 나사를 조일 때부터 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 카메라가 감시하며 "나사 덜 조였어!"라고 즉각 경고해 주는 자동화 감시 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) Security는 사람의 수동 점검 대신, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인의 각 단계마다(왼쪽부터 차례대로) 보안 스캐닝 봇을 내재화(Built-in)하여 작동한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DevSecOps 파이프라인의 Shift-Left 보안 통합 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Left: 개발 초기</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-node">Right: 배포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Plan ▶ Code ▶ Build ▶ Test ▶ Deploy ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(위협 모델링) (IDE 플러그인) (SCA/SAST) (DAST/IAST) (CSPM)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">보안</div><div class="kb-diagram-node">보안</div><div class="kb-diagram-node">보안</div><div class="kb-diagram-node">보안</div><div class="kb-diagram-node">보안</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기획 시 코딩 중 빌드 시 테스트 시 운영 시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">보안 리뷰 빨간줄 경고 오픈소스/코드 취약점 런타임 공격 모니터링</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자동 스캔 시뮬레이션</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 핵심: 취약점이 오른쪽(Deploy)으로 흘러가기 전에 왼쪽에서 차단</div></div>
</div>
</div>



1. **IDE 내장 검사**: 개발자가 코드를 작성하는 즉시 하드코딩된 패스워드나 민감 정보를 감지하여 에디터 내 플러그인이 보안 위반을 경고한다.
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/">SAST</a> (Static Application <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> Testing)</strong>: 코드를 깃허브 등에 Commit/Push 하는 순간, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 서버가 깨어나 소스 코드의 문맥을 정적으로 분석하여 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 등의 로직 결함을 1분 만에 찾아낸다.
3. <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/453_sca/">SCA</a> (<a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/">Software Composition Analysis</a>)</strong>: 외부 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(예: Log4j)의 버전을 스캔하여, 알려진 보안 취약점([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))이 포함되어 있으면 빌드를 강제로 실패(Red) 처리한다.

- **📢 섹션 요약 비유**: 공항 검색대에서 비행기 탑승 직전에만 폭발물을 검사하느라 수천 명이 줄을 서는(병목) 대신, 승객이 짐을 싸는 순간과 공항 버스에 타는 순간마다 자동으로 엑스레이를 통과시켜 탑승구 프리패스를 만드는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

기존 보안 방식과 [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 방식을 비교하면 비용과 속도의 패러다임 차이가 극명하게 나타난다.

| 비교 항목 | 기존 전통적 보안 (Siloed [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) | [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) ([Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/)) |
|:---|:---|:---|
| **검사 시점** | [SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/) 후반 (Test/Release 단계) | [SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/) 전반 (Plan/[Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 단계부터 내재화) |
| **주체** | 독립된 보안 부서 (수동 검사 및 결재) | 개발자, 자동화된 파이프라인 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 봇 |
| **취약점 조치 비용** | 100배 (운영 환경 배포 후 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 및 재설계) | 1배 (개발 IDE 환경에서 즉시 수정) |
| **배포 속도** | 심각한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (병목 현상 발생) | 중단 없는 고속 배포 유지 |

버그나 보안 취약점은 코드에 심어지는 순간부터 배포까지 시간이 지날수록 수정 비용이 기하급수적으로 상승한다. Shift-Left는 단순히 검사를 일찍 하는 것을 넘어, "보안 책임을 보안팀에 전가하지 않고 코드를 짜는 개발자 스스로가 피드백을 받아 내재화한다"는 문화적 융합(Culture Shift)을 수반한다. 나아가 최근에는 코드를 넘어 클라우드 인프라 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)까지 왼쪽으로 당기는 <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>) 보안</strong>으로 연결되고 있다.

- **📢 섹션 요약 비유**: 암 덩어리를 말기(배포 단계)에 발견해서 대수술로 막대한 비용과 고통을 치르는 대신, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 건강검진(코드 작성 단계)에서 작은 용종을 찾아내 레이저로 5분 만에 저렴하게 떼어내는 예방 의학의 승리입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

DevSecOps를 도입한다고 무작정 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 도구만 파이프라인에 집어넣으면, 쏟아지는 오탐(False Positive) 알람에 지친 개발자들이 보안 도구를 꺼버리는 참사가 발생한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 포인트
1. <strong>차단 <a href="/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/">Blocking</a> Threshold) 조절</strong>: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인에 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)기를 연동할 때, 처음부터 '모든 경고 시 빌드 실패'로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하면 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)가 마비된다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 치명적(Critical) 등급의 명백한 [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) 취약점만 차단(Block)하고 나머지는 경고(Warn)로 남겨 수용성을 높여야 한다.
2. <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/453_sca/">SCA</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 분석) 도입의 우선순위</strong>: 개발자가 직접 짜는 코드의 취약점보다, `npm install`로 가져다 쓰는 외부 패키지의 취약점 파급력이 훨씬 크다. 따라서 복잡한 SAST보다 깃허브 디펜다봇(Dependabot) 같은 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 도구를 가장 먼저 연동하는 것이 투자 대비 효과([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))가 높다.
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> 스캐닝 의무화</strong>: [테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) 같은 코드로 클라우드 인프라를 구성할 때, 소스 코드뿐만 아니라 'S3 버킷 퍼블릭 오픈' 같은 치명적 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류가 없는지도 왼쪽에서 미리 검사해야 한다.

- **📢 섹션 요약 비유**: 보안 알람을 너무 예민하게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 시도 때도 없이 사이렌이 울리면 사람들이 무시하게 되듯, 진짜 치명적인 늑대(Critical Bug)에게만 사이렌이 울리도록 보안 장비의 민감도를 튜닝하는 것이 실무의 핵심입니다.

---

## Ⅴ. 기대효과 및 결론

DevSecOps와 [Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) 철학은 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)의 생명인 '빠른 배포 속도'와 보안의 생명인 '[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)'이라는 상충하는 두 목표를 자동화라는 무기로 모두 잡아냈다.

릴리스 직전 도장을 들고 기다리던 보안팀을 해체하여 봇(Bot)으로 파이프라인 구석구석에 스며들게 만들었다. 이로 인해 취약점 발견 및 조치 시간이 비약적으로 단축되었으며 재작업(Rework) 비용은 제로에 수렴하게 되었다. 향후 클라우드 환경에서는 애플리케이션, 인프라 구성, 네트워크 정책까지 모든 것이 코드로 선언되므로, 코드의 탄생 순간을 감시하는 [Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/) 보안은 소프트웨어 공학의 필수 불가결한 기본 요건으로 완전히 자리 잡았다.

- **📢 섹션 요약 비유**: Shift-Left는 골키퍼(보안팀) 한 명이 수백 개의 공을 온몸으로 막아내던 낡은 수비에서, 공격수(개발자)부터 미드필더(파이프라인)까지 전 선수가 톱니바퀴처럼 압박 수비를 펼쳐 슈팅 기회 자체를 주지 않는 토털 사커(Total Soccer)로의 진화입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/">SAST</a> (정적 애플리케이션 보안 테스팅)</strong> | 소스 코드 자체를 실행하지 않고 문맥만 분석하여 논리적 취약점을 찾아내는 좌측 보안의 핵심 로봇. |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/">DAST</a> (동적 애플리케이션 보안 테스팅)</strong> | 배포가 완료된 테스트 환경에서 외부 공격자처럼 직접 모의 해킹을 찌르며 반응을 체크하는 스캐너. |
| <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/453_sca/">SCA</a> (<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/246_sca_software_composition_analysis_cve/">소프트웨어 구성 분석</a>)</strong> | 외부 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)에 알려진 해킹 취약점이 있는지 DB와 대조하여 차단하는 의존성 감시자. |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>/CD 파이프라인</strong> | 개발부터 배포까지 코드가 자동으로 흘러가는 궤도로, SAST와 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 로봇이 보안 초소로 배치되는 공간. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Siloed Security (폭포수 모델, 개발 완료 후 수동 보안 점검 ──▶ 병목 발생)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DevOps (개발과 운영의 자동화 융합, 여전히 보안은 릴리스 직전에 방치됨)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Shift-Left Security (보안 점검을 기획 및 코딩 등 파이프라인 좌측으로 이동)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DevSecOps (CI/CD 전 구간에 걸친 SAST/DAST/SCA 자동화 봇 내재화)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Cloud Native Security (컨테이너 이미지, IaC 설정까지 모두 좌측에서 스캔)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 옛날에는 레고 성을 다 만들고 나서 마지막에 검사관이 와서 "튼튼하지 않네, 다 부수고 다시 지어!"라고 해서 친구들이 울었어요.
2. [Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/)(좌측 이동)는 레고 블록을 한 칸 끼울 때마다 똑똑한 로봇이 "잠깐! 그 블록은 약해!"라고 바로바로 알려주는 마법이에요.
3. 덕분에 다 만들고 나서 성을 부술 일도 없고, 세상에서 제일 안전한 성을 엄청나게 빨리 완성할 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 105 / 973

← **이전**: [104. 토일 (Toil) - SRE에서 줄여야 할 단순 반복적 운영 작업](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/104_toil_automation_sre/)
**다음**: [106. FinOps - 클라우드 비용 최적화 및 관리](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/106_finops_cloud_cost_optimization/) →

---
