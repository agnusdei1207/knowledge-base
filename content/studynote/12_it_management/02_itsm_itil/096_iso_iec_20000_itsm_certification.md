+++
title = "96. ISO/IEC 20000 - IT 서비스 관리 체계 (ITSM) 국제 표준"
date = 2026-04-10

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ISO/IEC 20000은 기업이나 조직이 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리 (ITSM; [IT Service Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_itsm/)) 체계를 국제적인 베스트 프랙티스([ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/))에 맞게 훌륭히 운영하고 있음을 공인하는 국제 표준 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이다.
> 2. **가치**: 고객에게 "장애 발생 시 체계적으로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하며, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질을 지속적으로 유지할 수 있다"는 객관적 신뢰를 제공하여, B2B 사업 수주와 아웃소싱 계약에서 결정적인 경쟁 우위를 창출한다.
> 3. **판단 포인트**: 단순히 규정집을 만드는 것을 넘어, 계획-실행-점검-조치 ([PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/)) 사이클이 조직의 실제 업무 문화로 내재화되어 지속적인 개선 (Continual Improvement)이 이루어지고 있는지가 핵심 심사 기준이다.

---

## Ⅰ. 개요 및 필요성

IT 시스템이 기업의 비즈니스와 생존에 직결되면서, 서버가 죽었을 때 담당자가 주먹구구식으로 고치는 방식은 더 이상 용납되지 않는다. 고객(발주사)은 IT 아웃소싱 업체(SI/[SM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/))가 일정한 품질 이상의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 안정적으로 제공할 수 있다는 확실한 보증 수표를 원하게 되었다. 

이를 위해 영국의 IT 인프라 라이브러리인 [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) ([IT Infrastructure Library](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/))이라는 훌륭한 교과서가 널리 퍼졌으나, [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 자체는 권고사항일 뿐 기업을 강제하거나 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)해 주지 않았다. 따라서 "이 기업이 진짜 [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 교과서대로 똑바로 운영하고 있는가?"를 객관적인 심사원이 체크하고 공식 자격증을 부여하기 위해 탄생한 심사 잣대가 바로 ISO/IEC 20000이다.

- **📢 섹션 요약 비유**: 맛집 레시피 책([ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/))을 읽었다고 누구나 요리를 잘하는 건 아닙니다. 심사위원이 직접 식당에 와서 레시피대로 재료를 계량하고 위생적으로 요리하는지 검사한 뒤 문 앞에 달아주는 '미슐랭 3스타 마크'가 바로 ISO 20000입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ISO 20000 체계는 경영 시스템의 기본인 [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) ([Plan-Do-Check-Act](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/)) 사이클을 엔진으로 삼고, 그 위에 14개 이상의 핵심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [관리 프로세스](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/018_admin_processes/) 톱니바퀴들을 맞물려 돌린다. 



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ISO/IEC 20000의 PDCA 기반 핵심 프로세스 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Plan (계획)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Do (실행)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 서비스 제공: SLA, 가용성, 용량, 정보보안, 예산/과금</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 관계 관리 : 비즈니스 관계, 공급자 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 해결 프로세스: 사고 관리(Incident), 문제 관리(Problem)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 통제 프로세스: 구성 관리(CI), 변경 관리, 릴리스 관리</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Act (개선)</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-node">Check (점검)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(프로세스 최적화) (SLA 달성률 모니터링)</div></div>
</div>
</div>



이 다이어그램은 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 멈추지 않고 돌아가기 위한 4대 핵심 영역(제공, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 해결, 통제)을 보여준다. 사고가 나면 해결 프로세스가 작동하고, 서버를 증설할 때는 통제 프로세스의 승인을 받는다. 이 모든 행위는 기록되고 점검(Check)되어 다음 달의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질을 높이는(Act) 거름이 된다.

- **📢 섹션 요약 비유**: 비행기를 운항할 때 기장의 감으로 조종하는 것이 아니라, 이륙 전 점검표(제공), 관제탑 교신([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)), 난기류 대응(해결), 부품 교체(통제) 매뉴얼을 칼같이 지키고 비행 후 비행기록장치를 분석해 다음 비행을 더 안전하게 만드는([PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/)) 항공사 시스템과 같다.

---

## Ⅲ. 비교 및 연결

IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리 분야에서 자주 헷갈리는 3가지 개념인 ITSM, [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/), ISO 20000의 경계를 명확히 해야 한다.

| 구분 | 개념 및 역할 | 특징 |
| :--- | :--- | :--- |
| <strong>ITSM (IT <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> Mgmt.)</strong> | 기업이 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 관리하는 **목적과 행위 그 자체** | 철학이자 목표 (What) |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/">ITIL</a> (IT Infra. <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">Library</a>)</strong> | ITSM을 달성하기 위한 전 세계 선배들의 **베스트 프랙티스 모음집** | 가이드라인, 참고서 (How) |
| **ISO/IEC 20000** | 조직이 [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 등 표준에 맞춰 ITSM을 잘 수행하는지 평가하는 <strong>국제 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong> | 심사 기준, 자격증 (Standard) |

또한, ISO 가문 내에서도 다른 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)들과 연계된다. 품질 경영 전반을 다루는 ISO 9001, 정보 보안을 다루는 ISO 27001과 함께 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 취득하면(통합 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), 프로세스의 낭비를 줄이고 기업의 대외 신뢰도를 무적 수준으로 끌어올릴 수 있다.

- **📢 섹션 요약 비유**: ITSM은 '건강해지려는 목표'이고, ITIL은 '헬스장 운동법 책'이며, ISO 20000은 의사가 발급해 주는 '건강 검진 합격 진단서'입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현업에서 ISO 20000을 도입할 때 기술사가 가장 경계해야 할 안티패턴은 <strong>"<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>만을 위한 서류 작업"</strong>으로 변질되는 것이다. 

### 기술사 판단: 도입 시 핵심 고려사항
1. <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">Service Level Agreement</a>)의 현실화</strong>: 고객과 맺은 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 지표가 "서버 가동률 100%"처럼 달성 불가능하거나 "고객 만족도"처럼 측정 모호하면 안 된다. "업무 시간 내 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 2시간 이내 99% 달성"처럼 정량적이고 측정 가능해야 한다.
2. <strong>사고 관리와 <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/">문제 관리</a>의 분리</strong>: 서버가 멈췄을 때 즉시 재부팅해서 살리는 것(사고 관리)과, 왜 죽었는지 메모리 덤프를 분석해 근본 원인을 제거하는 것([문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/))을 철저히 분리하여 헬프데스크가 과부하에 걸리지 않게 설계해야 한다.
3. **도구(Tool) 자동화**: 수십 가지 프로세스를 엑셀로 관리하면 1년 안에 포기하게 된다. JIRA, ServiceNow 같은 ITSM 자동화 솔루션을 도입하여 변경 승인과 사고 접수 워크플로우를 시스템에 강제해야 한다.

- **📢 섹션 요약 비유**: 교통법규 준수 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 받기 위해 심사관이 있을 때만 안전벨트를 매는 척(서류 작업)을 해서는 안 됩니다. 아예 차에 시동을 걸면 안전벨트를 맬 때까지 경고음이 울리도록 시스템을 뜯어고쳐(ITSM 도구 도입) 무의식적으로 법을 지키게 만들어야 합니다.

---

## Ⅴ. 기대효과 및 결론

ISO/IEC 20000 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 획득하면 조직 내부에 팽배했던 부서 간의 책임 떠넘기기([사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) 현상)가 사라지고, 명확한 절차에 따라 장애가 처리되어 IT 운영 비용이 장기적으로 크게 감소한다. 또한 공공기관이나 대형 금융권의 대규모 SI/[SM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/) 사업 입찰에서 자격 요건을 충족하여 막대한 비즈니스 기회를 얻게 된다.

하지만 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 한 번 받았다고 끝나는 것이 아니다. ISO 20000은 정기적인 사후 심사(갱신)를 요구하며, 조직이 계속해서 [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) 사이클을 돌리고 있음을 증명해야 한다. 결론적으로 이 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)은 "우리는 완벽하다"는 증명이 아니라, "우리는 어제보다 오늘 더 나아지고 있는 훌륭한 체계를 가졌다"는 살아있는 증표로 기억해야 정답이다.

- **📢 섹션 요약 비유**: 운전면허를 한 번 땄다고 평생 사고 안 나는 게 아닙니다. 면허증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)은 기본 자격일 뿐, 매일 차를 점검하고 방어 운전을 하는 건강한 습관(지속적 개선)이 있어야 진짜 베스트 드라이버가 될 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/">ITIL</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/">IT Infrastructure Library</a>)</strong> | ISO 20000 심사 항목의 모태가 되는 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리 모범 사례집 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">Service Level Agreement</a>)</strong> | IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자와 고객 간의 품질 수준을 약속한 공식 계약서 |
| <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/">PDCA</a> (<a href="/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/">Plan-Do-Check-Act</a>)</strong> | ISO 경영 시스템 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 관통하는 지속적 개선 프로세스 사이클 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/">CAB</a> (Change Advisory Board)</strong> | IT 시스템을 변경(패치, 업그레이드)할 때 위험을 심사하고 승인하는 변경 위원회 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">IT 운영의 태동 (주먹구구식 장애 처리)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ITIL 등장 · 글로벌 베스트 프랙티스의 정립 (가이드라인)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">BS 15000 · 영국 국가 표준 제정 (심사 기준의 틀 마련)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ISO/IEC 20000 · ITSM 국제 표준 인증 발효 (글로벌 잣대)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">통합 인증체계 진화 · ISO 27001(보안) 등과 연계 및 자동화 솔루션 융합</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 집에서 장난감이 망가지면 아빠가 대충 고쳐주시죠? 이건 동네 구멍가게 방식이에요.
2. 하지만 애플스토어에 가면 접수증을 뽑고, 전문가가 고치고, 결과를 기록해요. 이게 '시스템'이에요.
3. ISO 20000은 "이 회사는 애플스토어처럼 아주 똑똑하고 체계적인 규칙을 지키면서 일합니다!"라고 주는 멋진 훈장 같은 거랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 176 / 587

← **이전**: [96. ISO/IEC 20000](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000/)
**다음**: [97. ITSM 도구 플랫폼 (ServiceNow, Jira Service Management 등)](/knowledge-base/studynote/12_it_management/02_itsm_itil/097_itsm_tool_platform/) →

---
