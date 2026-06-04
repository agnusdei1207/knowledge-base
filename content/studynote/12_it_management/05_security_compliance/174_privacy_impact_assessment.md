+++
title = "174. 개인정보 영향평가 (Privacy Impact Assessment, PIA)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 영향평가 ([PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/), Privacy Impact Assessment)는 새로운 시스템이나 중대한 변경이 정보주체의 권리와 프라이버시에 미칠 위험을 사전에 분석하고 설계 단계에서 통제 조치를 반영하는 평가 체계다.
> 2. **가치**: [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 사후 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 항목이 아니라 요구사항으로 끌어올려, 과다 수집, 과도한 보관, 무분별한 연계, 권한 남용 같은 문제를 오픈 전에 줄일 수 있다.
> 3. **판단 포인트**: 처리 규모가 크고, [민감정보](/knowledge-base/studynote/09_security/16_data_privacy/782_sensitive_information/)·고유식별정보가 포함되며, 외부 위탁·결합·[인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/)처럼 위험이 높을수록 PIA의 범위와 업데이트 주기를 더 깊고 촘촘하게 가져가야 한다.

---

## Ⅰ. 개요 및 필요성

PIA는 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)를 많이 다루는 시스템을 만들기 전에 "무엇이 위험한가"를 묻는 절차다. 보안 점검이 주로 취약점과 통제 구현 상태를 본다면, PIA는 그보다 앞선 단계에서 <strong>애초에 어떤 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 왜 수집하고, 어디로 흘려보내며, 언제 지울 것인가</strong>를 묻는다. 그래서 PIA의 핵심 산출물은 단순 점수표가 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름도, 위험 목록, 개선 과제다.

왜 이런 제도가 필요한가 하면, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 사고의 상당수는 해킹 이전에 설계에서 시작되기 때문이다. 수집 목적이 모호한 필드를 계속 쌓아 두거나, 제3자 제공 경로를 불명확하게 남기거나, 삭제 시점을 정하지 않으면 시스템이 정상 동작해도 프라이버시 위험은 이미 구조 안에 들어앉는다. PIA는 이 문제를 출시 전 단계에서 발견해 수정 비용을 크게 낮춘다.

국내에서는 일정 규모 이상의 공공기관 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)파일을 대상으로 법적 영향평가가 요구되며, 민간도 고위험 처리나 글로벌 규제 대응 관점에서 [DPIA](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Impact Assessment) 수준의 평가를 활용한다. 즉 PIA는 특정 기관만의 문서 작업이 아니라, <strong>Privacy by Design을 구현하는 경영·아키텍처 도구</strong>다.

```text
+----------------------------------------------------------------------+
| Why privacy problems must be found before launch                     |
+----------------------------------------------------------------------+
| New service idea                                                     |
|   -> collect data                                                    |
|   -> store data                                                      |
|   -> share / outsource                                               |
|   -> analyze / profile                                               |
|   -> retain / destroy                                                |
|                                                                      |
| If no PIA: hidden risks remain inside design                         |
| If PIA   : risky flow is found before production                     |
+----------------------------------------------------------------------+
```

즉 PIA의 필요성은 규제 준수만이 아니라, <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a> 처리 구조를 설명 가능하고 통제 가능한 형태로 만드는 것</strong>에 있다.

- **📢 섹션 요약 비유**: PIA는 새 놀이터를 만든 뒤 다친 아이를 치료하는 일이 아니라, 미끄럼틀 높이와 바닥 재질을 미리 점검해 다칠 일을 줄이는 설계 검토와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PIA는 보통 `대상 식별 -> 데이터 흐름 파악 -> 위험 분석 -> 개선 설계 -> 이행 확인`의 순서로 진행된다. 여기서 가장 중요한 출발점은 시스템 기능 목록이 아니라 <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a>의 생애주기</strong>다. 무엇을 수집하는지보다, 어디서 들어와 누구를 거쳐 어디에 저장되고 언제 파기되는지까지 끊김 없이 보여 주어야 실질적 위험이 보인다.

```text
+----------------------------------------------------------------------+
| PIA workflow                                                         |
+----------------------------------------------------------------------+
| Change trigger                                                       |
|   +- new system                                                      |
|   +- major feature expansion                                         |
|   +- third-party linkage                                             |
|   +- AI / analytics profiling                                        |
|        |                                                             |
|        v                                                             |
| Data inventory -> Data flow map -> Risk analysis -> Control design   |
|        |               |                   |                          |
|        |               |                   +- minimization            |
|        |               |                   +- access control          |
|        |               |                   +- retention / deletion    |
|        |               |                   +- transfer safeguards     |
|        v               v                                              |
| Scope confirmation      Remediation plan -> review -> launch decision |
+----------------------------------------------------------------------+
```

| 평가 축 | 대표 질문 | 설계 반영 예시 |
| :--- | :--- | :--- |
| 수집 최소화 | 이 정보가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 목적에 꼭 필요한가? | 선택 입력 전환, 불필요 필드 삭제 |
| 이용 목적 명확성 | 목적 외 사용 가능성이 있는가? | 목적별 테이블 분리, 동의 범위 구분 |
| 보관 및 파기 | 얼마나 오래 보관하고 언제 삭제하는가? | 보존 기간 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 자동 파기 배치 |
| 제공 및 위탁 | 외부 사업자와 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는가? | 위탁 계약, 전송 암호화, 최소 제공 |
| [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) | 누가 어떤 범위까지 볼 수 있는가? | 권한 분리, 마스킹, 접속 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| 정보주체 권리 | 열람·정정·삭제 요청을 처리할 수 있는가? | 셀프서비스 요청 프로세스, 티켓 연계 |

PIA의 핵심 원리는 세 가지로 요약할 수 있다. 첫째, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 중심성</strong>: 화면 기능이 아니라 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 이동 경로를 기준으로 본다. 둘째, **위험 기반 접근**: 모든 시스템을 똑같이 보지 않고 규모·민감도·연계성에 따라 깊이를 조절한다. 셋째, **개선 과제의 실행성**: 보고서로 끝나면 의미가 없고, 설계 변경·개발 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)·운영 통제로 연결되어야 한다.

실무에서 좋은 [PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/) 보고서는 보통 "현재 처리 구조", "[식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 위험", "개선 권고", "[잔여 위험](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/)"을 구분해 기록한다. 이렇게 해야 출시 결정권자, 보안팀, 개발팀이 같은 그림을 보고 판단할 수 있다.

- **📢 섹션 요약 비유**: PIA는 집 구조도를 보며 어디로 물이 새는지 찾는 점검과 같다. 수도관이 어느 방을 지나가는지 모르면 새는 지점도 못 찾지만, 배관도를 그리면 어디에 밸브를 달아야 할지가 보인다.

---

## Ⅲ. 비교 및 연결

PIA는 감리, [ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/) ([Personal Information](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) & [Information Security Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/095_information_security_management/) System), [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) (General [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Regulation)의 DPIA와 자주 함께 언급된다. 비슷해 보이지만 쓰이는 시점과 질문이 다르다.

| 구분 | [PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/) | [DPIA](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) | [정보시스템 감리](/knowledge-base/studynote/12_it_management/05_security_compliance/187_information_system_audit/) | [ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/) |
| :--- | :--- | :--- | :--- | :--- |
| 주된 목적 | 프라이버시 침해 위험의 사전 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 고위험 처리에 대한 [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 준수 | 사업·품질·보안 적정성 점검 | 지속적 관리체계 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) |
| 주요 시점 | 구축 전, 중대한 변경 전 | 고위험 처리 설계 전 | 단계별 산출물 점검 | 상시 운영 |
| 핵심 질문 | 어떤 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 흐름이 권리 침해를 유발하는가? | 고위험 처리가 합법·적정한가? | 시스템이 요구사항과 기준을 충족하는가? | 조직이 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 관리체계를 유지하는가? |
| 대표 산출물 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름도, 위험 목록, 개선 과제 | 위험 평가, [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)조치, [잔여 위험](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/) | 감리 의견, 보완 권고 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·절차·증적 체계 |

이 비교에서 중요한 점은 PIA가 다른 제도의 대체물이 아니라는 것이다. PIA는 설계 초기에 프라이버시 위험을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고, 감리는 그 결과가 프로젝트 산출물에 반영되었는지 확인할 수 있다. ISMS-P는 운영 단계에서 이런 통제가 지속적으로 지켜지는지 관리 체계 차원에서 본다. 즉 PIA는 **선행 설계 통제**, 감리는 <strong>이행 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>, ISMS-P는 <strong>지속 운영 체계</strong>라는 식으로 연결된다.

또한 글로벌 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)라면 국내 PIA와 DPIA를 같이 생각해야 한다. 국내에서는 공공·대규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 중심의 제도적 맥락이 강하고, EU GDPR은 자동화된 의사결정, 대규모 [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/), [민감정보](/knowledge-base/studynote/09_security/16_data_privacy/782_sensitive_information/) 처리 등 "고위험성"을 더 강하게 본다. 그래서 글로벌 플랫폼은 사실상 <strong>국내 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/">PIA</a> + <a href="/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/">DPIA</a> 사고방식</strong>을 함께 가져가는 편이 안전하다.

- **📢 섹션 요약 비유**: PIA는 건물을 짓기 전 설계 안전 점검이고, 감리는 공사 중 설계대로 짓는지 확인하는 일이며, ISMS-P는 건물 운영 규정을 계속 지키는 관리실과 같다. 셋은 비슷해 보여도 보는 타이밍과 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 PIA가 가장 자주 실패하는 이유는 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)만 채우고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 제대로 그리지 않기 때문이다. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 한 곳에만 있지 않고, 웹 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 분석 레이크, 위탁사 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 개발 테스트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 흩어져 이동한다. 따라서 PIA는 반드시 <strong>시스템 경계 바깥까지 포함한 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름도</strong>를 기반으로 해야 한다.

| 시나리오 | 주요 위험 | 권장 판단 |
| :--- | :--- | :--- |
| 공공 포털 고도화 | 여러 행정 시스템 간 대량 연계, 권한 남용 | 전체 연계 구간을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고 최소권한·열람로그·마스킹을 설계에 반영한다. |
| 마케팅 개인화 플랫폼 / 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 ([CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/), [C고객 Data Platform](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/115_cdp_customer_data_platform_single_view/)) | 과도한 결합, 목적 외 이용, 장기 보관 | 목적별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분리, 동의 범위 구분, 보유 기간 축소를 우선 적용한다. |
| 생성형 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 상담 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 프롬프트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 재학습 활용, [민감정보](/knowledge-base/studynote/09_security/16_data_privacy/782_sensitive_information/) 유입, 국외 이전 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 마스킹, 학습 전용 분리, 국외 이전·위탁 조건 검토를 별도 항목으로 다룬다. |
| 외부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 소프트웨어 ([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/), Software [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 위탁 운영 | 제3자 제공/위탁 경계 불명확, 삭제 책임 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 계약·[Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 포함해 책임과 파기 절차를 명문화한다. |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 항목별 수집 근거와 보존 기간이 설계 문서에 연결되어 있는가?
2. 제3자 제공, 위탁, 국외 이전, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장 경로까지 범위에 넣었는가?
3. 정보주체 권리 요청이 운영 프로세스와 시스템 기능으로 구현 가능한가?
4. 개선 권고가 실제 개발 티켓, 아키텍처 변경, 운영 절차로 연결되는가?
5. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 목적, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 범위, [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 활용 방식이 바뀌면 PIA를 재수행하도록 되어 있는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 개발 막바지에 형식적으로 보고서만 작성하는 [PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/)
- 운영 DB만 보고 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·분석 시스템을 범위에서 빼는 평가
- 위탁사나 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연계를 계약 문구로만 보고 기술 흐름을 검토하지 않는 접근
- 개선 권고를 남겼지만 예산·책임자·마감일이 없는 상태

기술사 답안에서는 "PIA는 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)법상 평가 제도"라고만 쓰기보다, <strong>"<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 생애주기와 권리 침해 가능성을 설계 단계에서 구조적으로 분석해 통제 조치를 반영하는 사전 예방 도구"</strong>라고 풀어내야 설계·감리·컴플라이언스 관점이 함께 살아난다.

- **📢 섹션 요약 비유**: PIA는 냉장고에 무슨 음식이 있는지만 보는 일이 아니라, 어떤 음식이 어디로 옮겨지고 언제 상하는지까지 적어 두는 가계부와 같다. 그래야 상한 음식이 식탁에 올라오기 전에 막을 수 있다.

---

## Ⅴ. 기대효과 및 결론

PIA를 제대로 수행하면 시스템 오픈 후 뒤늦게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 항목을 삭제하거나 연계 구조를 뜯어고치는 비용을 크게 줄일 수 있다. 또한 법적 준수뿐 아니라 고객 신뢰, 민원 대응, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응, 위탁사 관리 측면에서도 효과가 크다. 결국 PIA의 직접적 성과는 보고서가 아니라, <strong>더 적게 모으고 더 명확하게 쓰고 더 빨리 지우는 시스템 구조</strong>다.

물론 PIA만으로 모든 것이 해결되지는 않는다. 정확한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 목록이 없으면 평가가 공허해지고, 개선 권고를 실행할 거버넌스가 없으면 보고서는 쉽게 사문화된다. 따라서 기억해야 할 핵심은 PIA를 한 번의 행정 절차로 보지 않고, <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a>를 다루는 시스템에 프라이버시 설계를 삽입하는 관리 메커니즘</strong>으로 이해하는 것이다.

- **📢 섹션 요약 비유**: 좋은 지도는 길을 잃은 뒤에 보는 것이 아니라 출발 전에 보는 것이다. PIA는 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 시스템이 잘못된 길로 나서기 전에 방향을 잡아 주는 지도다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Privacy by Design](/knowledge-base/studynote/09_security/01_intro_principles/060_privacy_by_design/) | PIA가 설계 단계에서 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)조치를 반영하는 철학적 기반이다. |
| [DPIA](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Impact Assessment) | 고위험 처리에 대한 글로벌 규제형 영향평가 개념이다. |
| [ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/) | [PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/) 결과를 운영 관리체계로 유지·증빙하는 제도다. |
| [정보시스템 감리](/knowledge-base/studynote/12_it_management/05_security_compliance/187_information_system_audit/) | [PIA](/knowledge-base/studynote/12_it_management/05_security_compliance/976_privacy_impact_assessment_pia_audit_linkage/) 권고가 프로젝트 산출물에 반영되었는지 확인하는 연결 지점이 된다. |
| [Data Flow Diagram](/knowledge-base/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/) | PIA에서 가장 중요한 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 산출물 중 하나다. |
| 가명처리 / 비식별화 | [위험 완화](/knowledge-base/studynote/09_security/01_intro_principles/052_risk_mitigation/) 조치로 자주 선택되는 기술적 대응이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Personal data collection expands
    |
    v
Need for privacy risk visibility
    |
    v
PIA / DPIA methodology
    |
    +- data inventory
    +- flow mapping
    +- risk analysis
    +- remediation planning
    |
    v
Privacy by Design in SDLC (Software Development Life Cycle)
    |
    v
Audit / ISMS-P / digital trust governance
```

이 흐름은 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 단순 보안 점검에서 출발해, 설계·운영·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)까지 연결되는 거버넌스 체계로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. PIA는 새 놀이터를 만들기 전에 어디가 위험한지 먼저 살펴보는 안전 검사예요.
2. 미끄럼틀, 문, 가방 보관함을 하나씩 보면서 누가 다칠 수 있는지 미리 찾아봐요.
3. 그래서 놀이터를 연 뒤에 고생하지 않고, 처음부터 더 안전하게 만들 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 288 / 587

<- **이전**: [173. 정보보호최고책임자 (CISO) 지정 의무 및 역할](/knowledge-base/studynote/12_it_management/05_security_compliance/173_ciso_role_and_responsibility/)
**다음**: [175. 재해 복구 시스템 (Disaster Recovery System, DRS) 및 업무 연속성 계획 (Business Continuity](/knowledge-base/studynote/12_it_management/05_security_compliance/175_drs_bcp_strategy/) ->

---
