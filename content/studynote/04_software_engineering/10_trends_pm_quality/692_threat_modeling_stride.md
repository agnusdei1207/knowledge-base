+++
title = "692. 위협 모델링 STRIDE"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)은 크게 2가지로 나뉜다. 하나는 코딩 실수(버그)고, 다른 하나는 설계 자체의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)(Design Flaw)이다. 코딩 실수는 SAST나 [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) 같은 자동화 도구로 잡아낼 수 있지만, "비밀번호를 평문으로 DB에 저장하도록 설계했다"거나 "결제 API에 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 단계를 빼먹었다" 같은 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)은 보안 스캐너가 절대 잡아낼 수 없다.

설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)은 완성 후 고치려면 시스템 뼈대를 뜯어고쳐야 하므로 재앙에 가깝다. 따라서 건물을 올리기 전 설계도를 놓고 소방 시설이 충분한지 점검하듯, 코드를 짜기 전에 아키텍처 상의 보안 허점을 짚어내는 체계적인 방법론이 필요했다. 이것이 바로 <strong><a href="/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/">위협 모델링</a>(<a href="/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/">Threat Modeling</a>)</strong>이다.

- **📢 섹션 요약 비유**: 은행을 짓기 전에 금고 설계도를 펴놓고, "도둑이 환풍구로 들어오면 어떡하지? 다이너마이트로 벽을 부수면 어떡하지?"를 미리 상상해서 센서와 철창을 설계도에 추가해 놓는 작업이다.

---

다음은 [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  위협 모델링 STRIDE                               |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)은 일반적으로 4단계(What are we building? $\rightarrow$ What can go wrong? $\rightarrow$ What are we going to do? $\rightarrow$ [Did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) we do a good job?)로 진행된다.

이 중 "무엇이 잘못될 수 있는가?"를 찾기 위해 가장 널리 쓰이는 기법이 <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">STRIDE</a> 모델</strong>이다. STRIDE는 해커가 저지를 수 있는 6가지 대표적인 나쁜 짓의 앞 글자를 딴 것이다.

| 위협 (Threat) | 의미 | 위반되는 보안 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 대표적인 방어 대책 ([Mitigation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/)) |
|:---|:---|:---|:---|
| **S**poofing | **위장/신분 도용**: 다른 사람인 척 속임 (예: [세션 하이재킹](/knowledge-base/studynote/03_network/14_network_security_threats/707_session_hijacking_tcp_seq_cookie/)) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) | 강력한 암호, 2FA(다중 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 서명 |
| **T**ampering | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 변조</strong>: 전송 중이나 저장된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조작함 (예: 패킷 변조) | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(메시지 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 코드), [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 암호화 통신 |
| **R**epudiation | **부인**: "내가 안 했어!"라고 잡아뗌 (예: 결제 후 취소 우기기) | 부인 방지 (Non-repudiation) | 강력한 디지털 서명, 시스템 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/) Log) |
| **I**nformation Disclosure | **정보 유출**: 보지 말아야 할 기밀을 빼감 (예: DB 덤프) | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) ([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) | DB 암호화, [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) |
| **D**enial of [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/">서비스 거부</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/">DoS</a>)</strong>: 서버를 다운시켜 정상 유저를 막음 | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) | 쓰로틀링(Throttling), [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), 오토스케일링 |
| **E**levation of Privilege | <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/">권한 상승</a></strong>: 일반 유저가 관리자 권한을 탈취함 | [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) ([Authorization](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)) | [최소 권한 원칙](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/)([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)/[ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/)), 권한 분리 |

```text
+--------------------------------------------------------------+
|                  STRIDE를 활용한 위협 모델링                 |
+--------------------------------------------------------------+
| [Data Flow Diagram (DFD) 기반 분석]                          |
|                                                              |
|  [User] --(1.로그인)---> [Web Server] --(2.조회)---> [Database]|
|                                                              |
| * 화살표(데이터 흐름)와 박스(저장소/프로세스)마다 질문을 던짐:   |
|                                                              |
| Q(Spoofing): User가 다른 사람의 세션을 훔치면 어떡하지?         |
| Q(Tampering): (1)번 흐름에서 패킷 중간에 가로채서 고치면?       |
| Q(Info Disclosure): DB가 통째로 털리면 암호는 안전한가?         |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 경호원이 VIP를 보호할 때 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)([STRIDE](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/))를 꺼내들고, "S: 누가 VIP 가족으로 변장하면? T: 누가 VIP의 밥에 독을 타면? D: 누가 길을 차로 막아버리면?" 하나하나 따져보며 방어 계획을 세우는 것이다.

---

---

---

---

## Ⅲ. 비교 및 연결

[위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)에는 [STRIDE](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) 외에도 DREAD, [PASTA](/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/) 등 여러 방법론이 존재한다.

| 프레임워크 | 핵심 초점 | 주요 특징 및 활용처 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">STRIDE</a></strong> | **소프트웨어 중심** (개발자 친화적) | 마이크로소프트 고안. 시스템 설계도([DFD](/knowledge-base/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/))를 보며 기술적 취약점을 도출하는 데 가장 범용적으로 쓰임. |
| **DREAD** | **위험 평가** (우선순위 산정) | [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 위협이 얼마나 치명적인지(Damage, Reproducibility 등) 점수를 매겨 패치 우선순위를 정할 때 쓰임. |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/">PASTA</a></strong> | **공격자 중심** (해커의 관점) | 비즈니스 목표부터 시작하여 해커의 동기(동인)를 분석하는 7단계 프로세스. 보안 컨설턴트들이 주로 사용. |

보통 실무에서는 <strong>STRIDE로 위협을 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a></strong>하고, 그 결과물에 **DREAD 모델을 적용하여 점수를 매긴 뒤**, 점수가 높은 것부터 아키텍처에 방어 로직을 추가하는 콤보 전략을 사용한다.

- **📢 섹션 요약 비유**: STRIDE는 의사가 환자의 몸을 보며 "어떤 병에 걸릴 수 있을까?"(진단)를 찾는 것이고, DREAD는 "그중 어떤 병부터 수술해야 살 수 있을까?"(응급도 평가)를 결정하는 것이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)은 훌륭한 도구지만, 현업 개발팀에게 "설계 단계에서 무조건 해라"고 던져주면 프로젝트 일정이 박살 난다.

- **📢 섹션 요약 비유**: [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

[위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)을 아키텍처 설계 단계에 내재화하면, 코드를 단 한 줄도 짜기 전에 가장 치명적이고 고치기 힘든 논리적 보안 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 미리 제거할 수 있다. 이는 취약점 수정 비용을 기하급수적으로 줄여주는 '[시프트 레프트](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/)([Shift-Left](/knowledge-base/studynote/15_devops_sre/05_devsecops/242_shift_left_sdlc/))' 철학의 궁극적 실천이다.

결론적으로 시큐어 코딩이 '어떻게(How) 안전하게 짤 것인가'를 다룬다면, [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)은 '무엇을(What) 방어하도록 설계할 것인가'를 정의하는 나침반이다. 기술 리더는 개발팀이 코드를 짜기 전, 다이어그램을 보며 "해커라면 여기를 어떻게 찌를까?"라고 질문하는 문화를 정착시켜야 한다.

- **📢 섹션 요약 비유**: 설계도 없이 무작정 벽돌부터 쌓은 성은 나중에 무너뜨리고 다시 지어야 한다. [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/)은 설계도 위에 빨간펜으로 적군의 침투 경로를 미리 그려보고, 성벽 두께를 미리 결정하는 가장 현명한 장군의 전략이다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) [STRIDE](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
위협 모델링 STRIDE 개념 정립
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

1. [위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) STRIDE은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 865 / 973

<- **이전**: [691. 오픈소스 컴플라이언스 GPL 카피레프트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/691_opensource_compliance_gpl_copyleft/)
**다음**: [693. 제로 트러스트 아키텍처 최소 권한 원칙](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/693_zero_trust_architecture_least_privilege/) ->

---
