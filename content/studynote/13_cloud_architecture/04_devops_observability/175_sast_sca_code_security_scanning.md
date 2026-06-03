+++
title = "175. 코드 정적 스캐닝 및 종속성 취약점 스캐닝 (Static Application Security Testing, Software Composition Analysis; SAST, SCA)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing ([SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/))는 직접 작성한 코드의 취약한 흐름을, [Software Composition Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/) ([SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/))는 가져다 쓴 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)와 전이 의존성의 알려진 위험을 추적하는 상보적 검사다.
> 2. **가치**: 두 검사를 [Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 단계에 배치하면 배포 직전이 아니라 변경 순간에 위험이 드러나므로 수정 비용, 릴리스 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 노출을 함께 줄일 수 있다.
> 3. **판단 포인트**: 모든 경고를 똑같이 막으면 개발이 멈추므로, 새 코드인지, 실제 실행 경로에 닿는지, 치명도가 어느 수준인지에 따라 차단 기준을 분리해야 한다.

---

## Ⅰ. 개요 및 필요성

코드 보안 스캐닝은 출시 직전에 한 번 수행하는 점검이 아니라, 소스 변경과 의존성 변경이 일어날 때마다 위험을 다시 계산하는 조기 피드백 체계다. 현대 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 직접 작성한 코드와 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 의존성이 뒤섞여 있으므로, 취약점의 유입 경로도 "내 코드의 실수"와 "가져다 쓴 부품의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)"으로 나뉜다. SAST는 [입력 검증](/knowledge-base/studynote/09_security/uncategorized/601_input_validation/) 누락, 안전하지 않은 애플리케이션 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 호출, 하드코딩된 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 같은 문제를 빠르게 드러내고, SCA는 `log4j`처럼 이미 공개된 Common Vulnerabilities and Exposures ([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))와 위험한 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 연결해 준다.

문제는 이 둘 중 하나만 봐서는 빈틈이 남는다는 점이다. 코드 리뷰만 잘해도 전이 의존성의 치명적 취약점은 놓칠 수 있고, [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)만 관리해도 직접 만든 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 우회 로직은 보이지 않는다. 그래서 Development, [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), and Operations ([DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/))에서 코드 보안 스캐닝은 "도구 하나"가 아니라, 서로 다른 질문을 던지는 두 검사 축으로 이해해야 한다.

아래 그림은 코드 보안 위험이 들어오는 두 경로를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    Two entry points for code risk                   │
├──────────────────────────────┬───────────────────────────────────────┤
│ Own source code              │ 3rd-party components                 │
│ controller -> service -> DB  │ manifest -> dep A -> dep B           │
│ weak validation / secrets    │ known CVE / malicious package        │
│ logic flaw lives in repo     │ risk travels through transitive deps │
└──────────────────────────────┴───────────────────────────────────────┘
```

핵심은 애플리케이션 보안을 "내가 작성한 줄"과 "내가 가져온 줄"의 결합 문제로 보는 것이다. 둘 중 하나만 관리하면 나머지 절반의 공격면이 그대로 남는다.

- **📢 섹션 요약 비유**: SAST는 내가 직접 지은 집의 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 찾는 검사이고, SCA는 집을 지을 때 쓴 철근과 자재 중 리콜 대상이 섞였는지 확인하는 검사다. 집 자체와 자재를 둘 다 봐야 안전해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SAST의 핵심은 코드를 실행하지 않고 구조를 읽는 데 있다. 파서가 Abstract Syntax Tree (AST)를 만들고, 규칙 엔진이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름과 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용 패턴을 분석해 [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), [Cross-Site Scripting](/knowledge-base/studynote/09_security/05_web_app_security/470_xss/) ([XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/)), [Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/) ([SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/)), 하드코딩 키 같은 취약 패턴을 찾는다. 정교한 도구는 단순 문자열 검색을 넘어 [Taint](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/) Analysis로 "사용자 입력이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 위험한 함수까지 도달하는가"를 추적한다.

SCA의 핵심은 의존성 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)다. `pom.xml`, `package-lock.json`, `go.sum`, `requirements.txt` 같은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 직접·전이 의존성을 펼쳐 보고, [National Vulnerability Database](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/) ([NVD](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/))나 벤더 Advisory와 대조해 어느 패키지 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 알려진 취약점과 연결되는지 계산한다. 최근에는 Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) ([SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))와 Reachability Analysis를 함께 써서 "취약 패키지가 있긴 한데 실제 코드 경로에서 호출되는가"까지 줄여 본다.

아래 그림은 [Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 기준으로 두 검사가 어떻게 합쳐지는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    PR-centered security scan flow                   │
├──────────────────────────────────────────────────────────────────────┤
│ Git diff                                                             │
│   ├─ source files ----------> parser / AST / data-flow -> SAST       │
│   │                                                   └-> code path  │
│   └─ lockfile / manifest ---> dependency graph ------> SCA           │
│                                                       ├-> CVE match  │
│                                                       └-> fix path   │
│                                                                      │
│ Findings -> dedupe -> reachability / severity tuning -> policy gate  │
│          -> PR comment / build fail / ticket / baseline record       │
└──────────────────────────────────────────────────────────────────────┘
```

| 관점 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) | [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) |
| :--- | :--- | :--- |
| 분석 입력 | 소스 코드, 변경된 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 | Manifest, Lockfile, [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/), 패키지 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) |
| 탐지 방식 | 규칙 기반, [Taint](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/) Analysis, 패턴/흐름 분석 | 의존성 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) + [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/)/Advisory 매칭 |
| 강한 영역 | [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 우회, [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 하드코딩, 안전하지 않은 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용 | 취약 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 전이 의존성, 라이선스 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 노출 |
| 약한 영역 | 런타임 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 외부 바이너리, 환경 의존 취약점 | 직접 작성한 로직 버그, 미공개 [Zero-day](/knowledge-base/studynote/02_operating_system/10_security/597_zero_day_exploit/) |
| 출력 형태 | 코드 위치, 취약 흐름, 수정 가이드 | 패키지명, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 전이 경로, 권장 업그레이드 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |

실무적으로 중요한 차이는 "탐지 단위"다. SAST는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 함수 수준으로 내려가며, SCA는 컴포넌트와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 수준으로 올라간다. 따라서 둘을 함께 보면 "어디서 위험이 생겼는지"와 "무엇을 바꿔야 닫히는지"를 동시에 볼 수 있다.

- **📢 섹션 요약 비유**: SAST는 도시 지도에서 사고가 난 교차로를 찾는 일이고, SCA는 그 도시에 깔린 부품 중 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 부품이 어느 공장에서 왔는지 역추적하는 일이다. 한쪽은 위치를, 다른 한쪽은 부품 계보를 보여준다.

---

## Ⅲ. 비교 및 연결

SAST와 SCA를 이해하려면 다른 보안 검사와의 경계도 분명히 봐야 한다. Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing ([DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/))는 실행 중인 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 공격자 관점에서 시험하고, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 스캐닝은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 패키지와 베이스 이미지 계층을 본다. 즉 질문이 서로 다르므로 대체재가 아니라 계층적 보완재다.

| 검사 기법 | 주된 질문 | 잘 찾는 것 | 놓치기 쉬운 것 | 적합 시점 |
| :--- | :--- | :--- | :--- | :--- |
| [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) | 코드가 위험하게 작성됐는가 | [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 실수, 하드코딩 키 | 런타임 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 문제, 실제 배포 환경 | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/), 빌드 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) |
| [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) | 가져온 부품이 위험한가 | 취약 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 전이 의존성, 라이선스 | 직접 코드 로직 버그, 미공개 취약점 | 의존성 변경 시, 주기적 재평가 |
| [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) | 실행된 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 실제로 뚫리는가 | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 흐름, 헤더 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 실제 공격면 | 코드 내부 위치, 사용하지 않는 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | 스테이징, 릴리스 전후 |
| 이미지 스캔 | 배포 단위에 위험 패키지가 있는가 | OS 패키지, 베이스 이미지 취약점 | 애플리케이션 코드 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) | 패키징, 배포 직전 |

예를 들어 `log4j 2.14.1`은 SCA가 빠르게 찾지만, 직접 작성한 SQL 문자열 연결은 SAST가 훨씬 잘 찾는다. 반대로 잘못 열린 디버그 엔드포인트는 실행 후 DAST가 더 명확하게 잡는다. 결국 좋은 파이프라인은 "가장 싼 시점에 가장 잘 잡는 검사"를 앞단에 배치하고, 후단 검사는 남는 사각지대를 메우는 구조가 된다.

이 연결은 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 보안으로 더 확장된다. [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 결과를 SBOM으로 남기면 새 CVE가 공개됐을 때 이미 배포된 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중 어떤 시스템이 영향을 받는지 빠르게 역조회할 수 있다. 여기에 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 결과까지 묶으면 "취약 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 있으며, 그 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 위험 기능이 실제 호출되는 코드도 존재한다" 같은 우선순위 판단이 가능해진다.

- **📢 섹션 요약 비유**: 병원 진단에서도 문진, 혈액검사, CT가 서로 다른 질문을 던진다. SAST와 SCA도 마찬가지로 서로 다른 검사실이며, 둘을 묶어야 전체 진단이 완성된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "도구를 붙였는가"보다 "어떤 경고를 언제 차단할 것인가"가 더 중요하다. [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/), Semgrep, Checkmarx 같은 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 도구와 Snyk, Open Worldwide Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/) (OWASP) Dependency-Check, Trivy, Dependabot 같은 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 도구를 모두 넣더라도, 모든 경고를 동일하게 빌드 실패로 처리하면 개발 조직은 곧 우회한다. 현실적인 게이트 설계는 신규 위험과 레거시 부채를 분리하고, 치명도와 신뢰도를 함께 봐야 한다.

| 운영 지점 | 권장 검사 | 즉시 차단 예시 | 추적 관리 예시 |
| :--- | :--- | :--- | :--- |
| IDE / Pre-commit | 빠른 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/), [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 탐지 | 노출된 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서, 토큰 | 스타일성 경고, 낮은 확신의 [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) |
| [Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) + [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) | 신규 High 확신 [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), Reachable Critical [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/), 공개 Exploit 존재 | 신규 Medium 경고, 수정 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 없는 취약점 |
| Nightly / 주기 재평가 | 전체 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 재스캔, 풀 리포지토리 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) | 새로 공개된 Critical [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) | 장기 부채, 만료 임박 예외 |
| Release Gate | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/), [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 게이트, 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 승인되지 않은 라이선스, 미해결 치명 취약점 | 예외 승인 이력 검토 |

아래 흐름은 실제로 자주 쓰는 triage 기준이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                     Practical finding triage                        │
├──────────────────────────────────────────────────────────────────────┤
│ finding detected?                                                    │
│   ├─ secret leak / internet remote code execution -> block now       │
│   ├─ new code + high confidence issue             -> block PR         │
│   ├─ transitive CVE but no reachable path         -> ticket + watch   │
│   └─ legacy medium/low debt                       -> baseline + due    │
└──────────────────────────────────────────────────────────────────────┘
```

판단 포인트는 네 가지다. 첫째, <strong>새로운 위험 유입을 멈추는 것</strong>이 기존 부채를 한 번에 모두 없애는 것보다 우선이다. 둘째, Reachability와 Exploit Maturity를 반영해야 오탐에 묻히지 않는다. 셋째, 예외 승인은 영구 면제가 아니라 만료일이 있는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 객체여야 한다. 넷째, SCA는 주기 재평가가 필수다. 코드가 바뀌지 않아도 어제 공개된 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 때문에 오늘 위험해질 수 있기 때문이다.

기술사 답안에서는 SAST와 SCA를 단순 정의로 끝내지 말고, <strong>분석 대상 차이, 게이트 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>, <a href="/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a> 연계, Reachability 기반 우선순위화, <a href="/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/">DevSecOps</a> 내 배치 위치</strong>까지 써야 실무 판단력이 드러난다.

- **📢 섹션 요약 비유**: 공항 보안도 칼을 들고 들어오는 사람은 바로 막고, 규정이 애매한 물품은 별도 확인대로 보낸다. 중요한 것은 모든 물건을 똑같이 다루는 것이 아니라 위험이 큰 것을 먼저 정확하게 막는 운영 기준이다.

---

## Ⅴ. 기대효과 및 결론

SAST와 SCA를 함께 운영하면 개발 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)의 코드 취약점과 배포 전 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 위험을 동시에 줄일 수 있다. 특히 SCA는 새 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 공개 시점마다 기존 시스템을 역추적하는 능력을 주고, SAST는 코드 변경 순간에 안전하지 않은 흐름을 바로 수정하게 만든다. 그 결과 취약점 수정 시점이 앞당겨지고, 릴리스 막판 보안 이슈로 인한 재작업도 줄어든다.

다만 한계도 분명하다. SAST는 오탐과 런타임 맥락 부족이 문제이고, SCA는 공개되지 않은 Zero-day와 실제 호출 여부 판단에서 제약이 있다. 그래서 이 둘을 만능 해결책으로 보기보다, [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/), 이미지 스캐닝, [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), 런타임 탐지와 이어지는 조기 경보 계층으로 이해하는 편이 정확하다.

결국 기억해야 할 핵심은 간단하다. SAST는 "내 코드가 안전한가", SCA는 "내가 가져온 부품이 안전한가"를 묻는다. 둘을 묶어야 코드 보안이 소스 수준과 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 수준에서 동시에 닫힌다.

- **📢 섹션 요약 비유**: 식당 위생을 지키려면 조리법도 점검해야 하고, 납품 재료도 추적해야 한다. 조리대만 깨끗해도 상한 재료가 들어오면 문제고, 재료만 좋아도 조리 과정이 위험하면 사고가 난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/SCA를 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 안으로 끌어들여 조기 피드백 루프를 만든다. |
| [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) / [NVD](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/) | SCA가 취약 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 판별할 때 참조하는 대표 공개 취약점 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스다. |
| [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) | 배포 산출물에 어떤 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 포함됐는지 명시해 사후 영향 분석을 가능하게 한다. |
| Reachability Analysis | 취약 패키지가 실제 실행 경로에 닿는지 줄여서 우선순위를 높인다. |
| [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) | 실행 환경에서 보이는 공격면을 확인해 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/SCA의 사각지대를 보완한다. |
| [Container Image Scanning](/knowledge-base/studynote/15_devops_sre/05_devsecops/247_container_image_scanning_os_trivy/) | 애플리케이션 코드 밖의 OS 패키지와 베이스 이미지 위험을 추가로 점검한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Manual code review
    │
    ▼
SAST on source-code structure
    │
    ▼
SCA on dependency graph and transitive packages
    │
    ▼
SBOM + reachability + policy gate
    │
    ▼
Continuous supply-chain security and runtime re-evaluation
```

### 👶 어린이를 위한 3줄 비유 설명

1. SAST는 내가 직접 만든 장난감에서 날카로운 부분이 없는지 살펴보는 검사예요.
2. SCA는 친구에게 빌린 부품 중에 이미 고장 난 부품이 섞여 있는지 확인하는 검사예요.
3. 두 검사를 함께 해야 위험한 장난감이 완성되기 전에 미리 고칠 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 174 / 371

← **이전**: [174. 데브섹옵스 (DevSecOps, Shift-Left Security)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/174_devsecops_shift_left_security/)
**다음**: [176. 컨테이너 이미지 취약점 스캐닝 (Container Image Vulnerability Scanning)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/176_container_image_vulnerability_scanning/) →

---
