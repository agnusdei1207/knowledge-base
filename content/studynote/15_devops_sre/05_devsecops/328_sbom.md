+++
title = "328. SBOM 소프트웨어 구성 자재 명세 공급망 방어 (Software Bill of Materials Supply Chain Defense SPDX CycloneDX VEX)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) ([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))은 소프트웨어를 구성하는 모든 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/), [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 라이선스의 공식 인벤토리로, [공급망 공격](/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/)(SolarWinds, XZ Utils 사태) 이후 소프트웨어 투명성의 핵심 수단이 되었다.
> 2. **가치**: SBOM이 있으면 [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/) 같은 Critical [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 발표 시 영향받는 제품을 수 시간 내에 파악할 수 있다. [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 없이는 수천 개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 수동으로 검토해야 한다.
> 3. **판단 포인트**: SBOM은 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)만으로 끝나지 않는다. 빌드마다 갱신되어야 하고, VEX (Vulnerability Exploitability eXchange)와 결합해 "이 CVE가 이 제품에서 실제로 악용 가능한가"까지 답해야 의미 있다.

---

## Ⅰ. 개요 및 필요성

2020년 SolarWinds [공급망 공격](/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/)은 빌드 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 악성 코드가 삽입된 채 배포된 사례로, 미국 정부 기관을 포함한 수천 개 조직이 침해되었다. 이 사건은 소프트웨어 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)에 대한 근본적인 재검토를 촉발했고, 2021년 미국 행정명령 14028에서 연방정부 소프트웨어 공급업체에 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 제공을 의무화했다.

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) ([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))은 제조업의 [BOM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) ([Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/), 부품 목록)에서 유래한 개념이다. 자동차를 구성하는 모든 부품의 목록처럼, 소프트웨어를 구성하는 모든 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)의 완전한 목록이다. 이는 단순한 문서가 아니라 기계가 읽을 수 있는 구조화된 형식으로 제공되어야 한다.

> 📢 **섹션 요약 비유**: SBOM은 식품의 영양 성분 표시와 같다. 과자 봉지에 원재료명, 함량, 알레르기 유발 성분이 표시되어 있어야 소비자(사용 조직)가 안전 여부를 판단할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌────────────────────────────────────────────────┐
│              SBOM 생성 및 활용 파이프라인          │
├────────────────────────────────────────────────┤
│  소스코드 + 의존성 파일                           │
│          │                                     │
│          ▼                                     │
│  ┌────────────────┐                            │
│  │  SCA 도구       │  (Syft, Trivy, CycloneDX) │
│  └───────┬────────┘                            │
│          │                                     │
│          ▼                                     │
│  ┌────────────────────────────────────────┐   │
│  │  SBOM 파일 (SPDX 또는 CycloneDX 형식)  │   │
│  │  - 컴포넌트명, 버전, 공급자              │   │
│  │  - 라이선스 (MIT, Apache 2.0, GPL)      │   │
│  │  - 체크섬 (SHA-256)                     │   │
│  └──────┬───────────────┬─────────────────┘   │
│         │               │                      │
│         ▼               ▼                      │
│  CVE 취약점 조회    라이선스 컴플라이언스  VEX  │
│  (NVD, OSV)        분석                악용 가능성│
└────────────────────────────────────────────────┘
```

| [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 형식 | 특징 | 주도 기관 |
|:---|:---|:---|
| SPDX (Software Package [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Exchange) | ISO 국제 표준, 광범위한 생태계 지원 | Linux Foundation |
| CycloneDX | 보안 중심, VEX 기본 지원 | OWASP |

VEX (Vulnerability Exploitability eXchange)는 SBOM의 보완 문서로 "이 제품의 특정 CVE는 악용 가능하다/불가하다/조사 중이다"를 공식 표명한다.

> 📢 **섹션 요약 비유**: SBOM은 약품 첨부 문서다. 약의 성분, 함량, 부작용, 주의사항이 모두 기재되어야 의사(보안팀)가 적절히 처방(대응)할 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) | [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) | VEX |
|:---|:---|:---|:---|
| 유형 | 산출물 (정적 목록) | 프로세스 ([동적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/332_dynamic_analysis/)) | 보완 문서 (악용 가능성) |
| 업데이트 | 빌드마다 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | CI에서 지속 실행 | [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 발표 시 작성 |
| 형식 | SPDX, CycloneDX | 도구별 다양 | CycloneDX VEX |
| [법적 요건](/knowledge-base/studynote/11_design_supervision/01_audit_framework/072_personal_data_destruction_log_retention_audit/) | EO 14028 의무화 | 내부 프로세스 | 자발적/일부 의무화 |

Syft는 [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) 이미지에서 SBOM을 추출하고, Grype는 이 SBOM으로 CVE를 스캔한다. 이미지 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)(Harbor)에 SBOM을 저장하면 운영 중인 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 취약점도 실시간 추적이 가능하다.

> 📢 **섹션 요약 비유**: SCA는 냉장고 내용물을 검사하는 과정이고, SBOM은 그 결과를 정리한 재료 목록표이며, VEX는 "이 재료는 지금 상하지 않았다"는 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)서다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 도구

- **Syft**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템, 소스코드에서 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) (SPDX, CycloneDX 지원)
- **Trivy**: 이미지 스캔 + [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 통합 도구
- **CycloneDX Maven/npm 플러그인**: [빌드 도구](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/070_build_tools_maven_gradle_npm/)에서 직접 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 모든 배포 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)에 SBOM이 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는가?
2. SBOM이 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 저장소(Harbor, Nexus)에 연결 저장되는가?
3. Critical [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 발표 시 SBOM을 조회해 영향 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 목록을 30분 내 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 수 있는가?
4. VEX 문서 작성 프로세스가 정의되어 False Positive CVE를 공식 처리하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 1회 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 후 방치**: 의존성이 바뀔 때마다 갱신하지 않으면 실효성 없음
- **VEX 없는 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)**: [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 우선순위 관리 어려움, 보안팀 과부하

> 📢 **섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 없이 보안 대응은 화재 시 건물 도면 없이 소방 활동하는 것이다. 어느 방에 무엇이 있는지 모르면 구조도, 진압도 늦어진다.

---

## Ⅴ. 기대효과 및 결론

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 도입 조직은 신규 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 발표 시 영향받는 시스템을 수 시간 내에 파악하고 패치 우선순위를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)할 수 있다. SolarWinds, [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/) 같은 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 사고에 대한 대응 시간이 수 주에서 수 시간으로 단축된다.

SBOM의 본질은 **알 권리의 자동화**다. 내가 사용하는 소프트웨어에 무엇이 들어있는지 아는 것이 보안의 첫 번째 단계다. 모르는 것은 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)할 수 없다.

> 📢 **섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 없는 소프트웨어 보안은 내용물 표시 없는 택배 박스다. 박스가 안전한지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하려면 안에 무엇이 있는지 알아야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) ([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)) | 소프트웨어 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 완전한 목록 |
| SPDX (Software Package [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Exchange) | ISO 표준 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 형식 |
| CycloneDX | OWASP 주도 보안 중심 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 형식 |
| VEX (Vulnerability Exploitability eXchange) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) + [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 악용 가능성 표명 |
| [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) ([Software Composition Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/)) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 프로세스 |
| SLSA ([Supply chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) Levels for Software Artifacts) | 빌드 출처 보증 프레임워크 |

### 📈 관련 키워드 및 발전 흐름도

```text
공급망 보안 인식 전          SBOM 표준화 시대            법제화/자동화 시대
──────────────────    ──────────────────────────   ───────────────────────
수동 의존성 추적      →  SPDX, CycloneDX 표준    →  EO 14028 의무화
SolarWinds 사고           Syft, Trivy 도구 등장       VEX 도입
Log4Shell 대응 지연        이미지 레지스트리 통합         SLSA 프레임워크
```

### 👶 어린이를 위한 3줄 비유 설명

1. SBOM은 레고 박스 안에 든 블록 목록이에요. 어떤 블록이 몇 개 들어있는지 정확히 알아야 불량 블록을 바로 찾을 수 있어요.
2. 나쁜 블록([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 취약점)이 발견되면 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 목록을 보고 어느 레고 세트에 그 블록이 들어있는지 바로 알 수 있어요.
3. [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 없이는 모든 레고 세트를 하나하나 뜯어봐야 해서 시간이 너무 오래 걸려요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 328 / 373

← **이전**: [327. SCA 오픈소스 컴플라이언스 스캔 (SCA Software Composition Analysis Open Source Compliance](/knowledge-base/studynote/11_design_supervision/06_exam_summary/327_process/)
**다음**: [329. Secret Manager HashiCorp Vault 시크릿 관리 하드코딩 방지 (Secret Manager HashiCorp](/knowledge-base/studynote/11_design_supervision/06_exam_summary/329_process/) →

---
