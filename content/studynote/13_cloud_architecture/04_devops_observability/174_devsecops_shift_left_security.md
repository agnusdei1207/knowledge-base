---
title: "DevSecOps, Shift-Left Security"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데브섹옵스](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) ([DevSecOps](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/))는 보안([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))을 배포 직전 승인 절차가 아니라, 개발·빌드·배포 흐름 전체에 녹인 <strong><a href="/studynote/15_devops_sre/01_culture_methodology/022_continuous_feedback_telemetry/">지속적 피드백</a> 구조</strong>다.
> 2. **가치**: [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 유출, 취약 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 잘못된 [Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 코드 작성 시점에 잡으면 수정 비용과 릴리스 지연이 급감하고, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적도 자동으로 남는다.
> 3. **판단 포인트**: Shift-Left는 "무조건 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 다 막는다"가 아니라, **어떤 위험을 어느 단계에서 가장 싸고 정확하게 잡을지** 설계하는 문제이며, 운영 단계의 Shift-Right 관측과 함께 가야 완성된다.

---

## Ⅰ. 개요 및 필요성

[데브섹옵스](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) ([DevSecOps](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/))는 Development, [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), and Operations의 결합으로, 보안을 별도 부서의 최종 승인 행위가 아니라 소프트웨어 전달 체계의 기본 속성으로 만드는 운영 방식이다. 전통적인 프로젝트에서는 기능 개발이 거의 끝난 뒤에야 보안 점검이 들어왔고, 그 결과 취약점 하나가 발견될 때마다 구조 수정, 일정 연기, 책임 공방이 반복됐다. 특히 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 의존성, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지, 클라우드 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 복잡해진 현재 환경에서는 "출시 직전 한 번 검사" 방식으로는 속도도 보안도 둘 다 잃기 쉽다.

핵심 배경은 두 가지다. 첫째, 취약점은 뒤로 갈수록 수정 범위가 넓어진다. 코드 한 줄을 고치면 되는 문제가 운영 배포 후에는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보정, 이미지 재빌드, 고객 공지, 포렌식까지 번질 수 있다. 둘째, 보안 위험의 발생 지점이 소스 코드만이 아니기 때문이다. [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 빌드 파이프라인, 서명되지 않은 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/), 잘못 열린 보안 그룹([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group)도 모두 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 위험이 된다.

아래 그림은 "늦은 보안 게이트"와 "흐름 내장형 보안"의 차이를 보여준다.

```text
+--------------------------------------------------------------------+
|           Late security gate vs integrated security loop           |
+-----------------------+--------------------------------------------+
| Late gate             | Integrated DevSecOps                      |
+-----------------------+--------------------------------------------+
| Code -> Build ->      | Code -> scan -> build -> scan -> deploy   |
| Release -> Security   |            ^ feedback returns immediately |
| issue found at end    |                                            |
| => big rework         | => small fixes, fast recovery             |
+-----------------------+--------------------------------------------+
```

중요한 점은 DevSecOps가 개발자를 보안 담당자로 떠넘기는 구호가 아니라는 점이다. 보안팀은 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/), 예외 프로세스, 도구 운영을 맡고, 개발팀은 그 기준을 코드와 파이프라인 안에서 실천한다. 즉 책임이 사라지는 것이 아니라, <strong>병목형 승인 구조가 협업형 피드백 구조로 바뀌는 것</strong>이 본질이다.

- **📢 섹션 요약 비유**: 건물을 다 지은 뒤 소방법 위반을 찾는 대신, 설계도·자재·시공 단계마다 소방 기준을 넣어 두는 것이 DevSecOps다. 공사 끝에 벽을 다시 뜯는 것보다 훨씬 싸고 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DevSecOps의 핵심은 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/) / [Continuous Delivery](/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) 파이프라인 각 지점에 서로 다른 종류의 보안 검사를 배치하는 것이다. [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 탐지는 가장 앞에서 즉시 차단해야 하고, Static Application [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing ([SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/))은 [Pull Request](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 단계에서 코드 패턴을 본다. [Software Composition Analysis](/studynote/04_software_engineering/11_testing_validation/887_sca_software_composition_analysis/) ([SCA](/studynote/09_security/05_web_app_security/453_sca/))는 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 Common Vulnerabilities and Exposures ([CVE](/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))를 점검하고, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 스캔은 배포 단위 자체를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다. 배포 직전에는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 코드([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))와 동적 점검이, 운영 중에는 런타임 탐지와 이상 행위 관측이 뒤를 받친다.

```text
+--------------------------------------------------------------------+
|                Security placement across delivery                  |
+--------------+----------------------------+------------------------+
| Stage        | Main control               | Best at catching       |
+--------------+----------------------------+------------------------+
| IDE/commit   | secret scan, lint rule     | leaked key, bad habit  |
| PR/build     | SAST, SCA, IaC scan        | code/dependency flaw   |
| Artifact     | image scan, SBOM, signing  | package/image risk     |
| Deploy       | policy gate, admission     | misconfig, drift gate  |
| Runtime      | DAST, runtime detect       | env-only exploit path  |
+--------------+----------------------------+------------------------+
```

이 그림의 메시지는 "한 도구가 모든 취약점을 잡지 못한다"는 점이다. 예를 들어 SAST는 코드 구조를 빨리 보지만 실제 실행 경로를 모두 알지 못하고, Dynamic Application [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing ([DAST](/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/))은 실행 환경에서 보이는 약점을 찾지만 느리고 후행적이다. 따라서 좋은 파이프라인은 도구를 많이 붙이는 것이 아니라, <strong>발견 시점·오탐률·차단 비용이 다른 검사들을 계층적으로 배치</strong>한다.

| 파이프라인 지점 | 대표 통제 | 주된 판단 기준 |
| :--- | :--- | :--- |
| 개발자 로컬 | [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 스캔, 보안 린트 | 즉시 실패시켜도 생산성 타격이 작은가 |
| [Pull Request](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) | [SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/), [SCA](/studynote/09_security/05_web_app_security/453_sca/), [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 스캔 | 새로 추가한 위험을 리뷰 단계에서 막을 수 있는가 |
| 빌드/패키징 | [SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)), 이미지 스캔, 서명 | 배포 단위의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)을 증명할 수 있는가 |
| 배포 게이트 | [Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)), Admission [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) | 조직 기준 위반을 자동 차단할 수 있는가 |
| 운영 | 런타임 탐지, 취약점 재평가 | 배포 후 환경 변화와 실제 공격을 볼 수 있는가 |

실무에서는 여기서 멈추지 않고 "[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 코드화"까지 가야 한다. 예를 들어 `latest` 태그 금지, 루트 권한 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 금지, 공개 버킷 금지, 서명되지 않은 이미지 배포 금지 같은 규칙을 사람이 매번 읽어 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하지 않고 코드로 평가해야 한다. 그래야 속도를 유지하면서도 일관성을 확보할 수 있다.

또한 Shift-Left가 곧 Shift-Only는 아니다. 운영 중 공개된 신규 [CVE](/studynote/09_security/04_endpoint_security/409_cve_lifecycle/), 런타임 [권한 상승](/studynote/09_security/04_endpoint_security/356_privilege_escalation/), 예상치 못한 네트워크 노출은 배포 전 검사만으로는 잡히지 않는다. 그래서 DevSecOps는 앞단 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 뒷단 관측을 잇는 <strong>연속 보안 루프</strong>로 이해해야 한다.

- **📢 섹션 요약 비유**: 공항 보안은 입구 검색대 하나로 끝나지 않는다. 신분 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 수하물 X-Ray, 탑승구 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 기내 보안이 이어져야 전체 여행이 안전해지는 것처럼, DevSecOps도 단계별 보안 분업이 핵심이다.

---

## Ⅲ. 비교 및 연결

DevOps와 DevSecOps의 차이는 단순히 보안 도구를 몇 개 더 붙였느냐가 아니다. DevOps가 속도와 자동화를 중심으로 전달 흐름을 최적화했다면, DevSecOps는 그 흐름 안에 위험 통제를 기본값으로 심는다. 반대로 전통적 SecOps는 보안 관제가 강점이지만, 개발 파이프라인에 늦게 개입하면 병목이 되기 쉽다.

| 관점 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | [DevSecOps](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) | 전통 SecOps |
| :--- | :--- | :--- | :--- |
| 중심 질문 | 얼마나 빨리 배포할까 | 빠르면서 안전하게 배포할까 | 어떤 공격을 막고 탐지할까 |
| 보안 위치 | 후행 검토가 많음 | 파이프라인 내장 | 운영·관제 중심 |
| 장점 | 전달 속도 | 속도와 추적성의 균형 | 깊은 보안 전문성 |
| 약점 | [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 위험 누락 가능 | 오탐 관리 실패 시 개발 마찰 | 릴리스 병목 가능 |

검사 기법도 경계를 이해해야 한다. SAST는 "코드가 위험하게 작성됐는가"를, SCA는 "가져다 쓴 부품이 위험한가"를, DAST는 "실행된 서비스가 실제로 뚫리는가"를 본다. 즉 셋은 서로 대체제가 아니라 질문이 다르다. 여기에 [Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) 스캔과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 탐지를 합치면 코드·의존성·[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)·실행 경로를 각각 다른 각도에서 덮을 수 있다.

또 하나 중요한 연결은 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 보안이다. 최근 공격은 애플리케이션 로직보다 빌드 체인, 패키지 [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 서명되지 않은 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)를 노리는 경우가 많다. 그래서 DevSecOps는 단순 취약점 탐지에서 끝나지 않고, [SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 서명, 출처 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/), [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 배포 통제와 결합해야 한다.

정리하면 Shift-Left는 발견 시점을 앞당기는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이고, Shift-Right는 운영 현실을 놓치지 않는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 둘을 함께 묶어야 "개발 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 예방 + 운영 중 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)"이 완성된다.

- **📢 섹션 요약 비유**: 음식점 위생 관리는 레시피 검사, 재료 유통기한 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 완성 음식 시식, 주방 CCTV가 각각 다른 역할을 한다. 어느 하나만 잘해도 안심할 수 없는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현실적인 [DevSecOps](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 도입은 "모든 경고를 즉시 차단"이 아니라, 위험도와 팀 성숙도에 맞춰 게이트를 설계하는 데서 시작한다. 가장 먼저 하드 페일(Hard Fail)로 묶을 대상은 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 유출, 치명적 원격 실행 취약점, 서명되지 않은 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/), 공개 금지 자산 노출처럼 조직이 절대 허용할 수 없는 항목이다. 반면 레거시 코드 전반에 쌓인 [SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 경고를 첫날부터 모두 빌드 실패로 묶으면 개발 조직이 도구를 우회하려 든다.

```text
+--------------------------------------------------------------------+
|                  Practical gate decision flow                      |
+--------------------------------------------------------------------+
| finding detected?                                                  |
|   |                                                                |
|   +- secret leaked / unsigned artifact? -> block now               |
|   +- critical exploitable on internet path? -> block + fix         |
|   +- high on newly changed code? -> block or require exception     |
|   +- legacy / low risk debt? -> ticket + SLA + trend tracking      |
+--------------------------------------------------------------------+
```

실무 판단 포인트는 다음과 같다.

1. **새 코드 우선 차단**: 기존 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 전체보다 "이번 변경이 새로운 위험을 만들었는가"를 먼저 본다.
2. **예외는 허용하되 만료일을 둔다**: 예외 승인도 코드처럼 추적하고, 30일·90일 같은 만료를 둬야 영구 면책이 되지 않는다.
3. **빌드 시간과 소음 관리**: 모든 검사를 동기식으로 넣지 말고, 빠른 검사는 [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 게이트에, 무거운 검사는 야간 재평가나 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 파이프라인에 배치한다.
4. **개발자 피드백 우선**: IDE 플러그인, [Pull Request](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 코멘트, 자동 수정 제안이 있어야 보안이 "나중에 오는 벌점"이 아니라 "지금 고칠 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)"가 된다.
5. **측정 지표를 운영한다**: 취약점 검출 수보다 평균 수정 시간, 신규 취약점 유입률, 예외 누적량, 차단률 대비 오탐률을 봐야 한다.

기술사 답안에서는 DevSecOps를 문화론만으로 쓰면 얕아진다. <strong>단계별 통제 배치, 게이트 설계, 예외 관리, <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>, Shift-Right 연계</strong>까지 써야 실제 운영 관점이 살아난다. 특히 "빠른 개발을 해치지 않도록 어떤 통제는 즉시 차단하고 어떤 통제는 추적성 위주로 운영하는가"를 설명하면 깊이가 생긴다.

- **📢 섹션 요약 비유**: 학교 규율도 모든 실수를 즉시 퇴학으로 다루면 운영이 망가진다. 반칙의 무게에 따라 즉시 제재할 것과 경고 후 시정할 것을 구분해야 제도가 오래 간다.

---

## Ⅴ. 기대효과 및 결론

DevSecOps를 제대로 정착시키면 취약점이 더 빨리 발견되는 것 이상으로, 보안이 릴리스 속도의 적이 아니라 품질 기준으로 자리 잡는다. 개발자는 코드를 바꾼 직후 위험을 알 수 있고, 보안팀은 파이프라인 로그와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기록으로 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응을 체계화할 수 있다. [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 측면에서도 어떤 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)와 이미지가 언제 어떤 기준으로 승인됐는지 추적 가능해진다.

하지만 한계도 분명하다. 오탐이 많은 도구는 금방 무시되고, 무거운 스캔은 빌드 시간을 늘리며, 운영 중에만 드러나는 취약점은 Shift-Left만으로 해결되지 않는다. 따라서 DevSecOps의 성공 조건은 "도구 도입"이 아니라 <strong><a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>의 명확성, 예외 관리, <a href="/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/">개발자 경험</a>, 운영 단계 관측</strong>의 균형이다.

결국 이 주제는 "보안을 앞당긴다"보다, <strong>보안 피드백을 전달 체계 안에 심는다</strong>로 기억하는 편이 정확하다. 좋은 DevSecOps는 속도를 늦추는 문지기가 아니라, 더 작은 수정으로 더 이른 시점에 위험을 줄여 주는 설계다.

- **📢 섹션 요약 비유**: 자동차 공장에서 불량을 출고장 끝에서만 잡는 대신, 프레스·용접·도장 단계마다 자동 검사기를 두면 전체 생산 속도는 유지하면서 리콜 위험을 크게 낮출 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Shift-Left Security](/studynote/04_software_engineering/02_requirements_analysis/105_devsecops_shift_left_security/) | 취약점 발견 시점을 설계·개발 단계로 앞당기는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) | 소스 코드 패턴을 분석해 조기 결함을 찾는 정적 검사 |
| [SCA](/studynote/09_security/05_web_app_security/453_sca/) | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 의존성과 CVE를 추적하는 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 검사 |
| [SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) | 어떤 부품으로 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)가 구성됐는지 증명하는 목록 |
| [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) | 보안 기준을 기계가 자동 평가하는 방식 |
| Admission Control | 배포 직전 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 리소스를 차단하는 마지막 게이트 |
| Shift-Right [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | 운영 중 실제 공격·환경 변화를 관측하는 보완 축 |

### 📈 관련 키워드 및 발전 흐름도

```text
Late security review
    |
    v
Shift-Left security in CI/CD
    +- secret scan
    +- SAST / SCA / IaC scan
    +- image scan + SBOM + signing
    |
    v
Policy as Code and trusted deployment
    |
    v
Shift-Right runtime detection and continuous verification
```

### 👶 어린이를 위한 3줄 비유 설명

1. [데브섹옵스](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/)는 숙제를 다 한 뒤 틀린 것을 찾는 게 아니라, 쓰는 중간중간 바로 고치게 도와주는 방법이에요.
2. 그래서 큰 실수가 나중에 한꺼번에 터지지 않고, 작은 실수일 때 빨리 고칠 수 있어요.
3. 또 숙제를 내기 전에도 보고, 낸 뒤에도 다시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해서 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 371

<- **이전**: [173. 구성 관리 도구 (Configuration Management) — Ansible, Chef, Puppet](/studynote/13_cloud_architecture/04_devops_observability/173_configuration_management_ansible_chef_puppet/)
**다음**: [175. 코드 정적 스캐닝 및 종속성 취약점 스캐닝 (Static Application Security Testing, Software](/studynote/13_cloud_architecture/04_devops_observability/175_sast_sca_code_security_scanning/) ->

---
