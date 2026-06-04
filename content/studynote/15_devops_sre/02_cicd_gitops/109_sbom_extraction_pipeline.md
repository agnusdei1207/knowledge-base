+++
title = "109. SBOM 추출 파이프라인 (Software Bill of Materials) - 공급망 보안 의무화"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))은 소프트웨어를 구성하는 <strong>모든 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">라이브러리</a>·<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a>·의존성 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>를 기계 판독 가능한 표준 포맷(SPDX, CycloneDX)으로 기록한 디지털 자재 명세서</strong>다.
> 2. **가치**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 빌드 시점에 자동 추출하여, Log4j 같은 <strong><a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/">공급망 공격</a>(<a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/">Supply Chain Attack</a>) 발생 시 취약 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/">컴포넌트</a> 포함 여부를 수초 내 전수 조사</strong>할 수 있다.
> 3. **판단 포인트**: 미 행정명령(EO 14028)으로 연방 납품 소프트웨어에 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 제출이 <strong>법적 의무화</strong>되었으며, [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) + VEX(실제 악용 가능성 평가) + 디지털 서명(Sigstore)의 3단 결합이 [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 표준이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어의 80~90%는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)로 구성된다. 직접 설치한 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)뿐 아니라 그것이 끌어오는 하위 의존성(Transitive Dependency)까지 합치면 수백~수천 개에 달한다. [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/)([2021](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/)) 사태에서 전 세계 기업이 "우리 시스템에 Log4j가 있는가?"라는 질문에 수주간 답하지 못한 것이 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 의무화의 직접적 계기다.

```text
+-------------------------------------------------------+
|              SBOM 추출 파이프라인 흐름도                |
+-------------------------------------------------------+
|  [Source Code]  ->  [Build Engine]  ->  [SBOM Generator]|
|  (pom, npm)       (Maven, npm)      (Syft, Trivy)    |
|                                          |            |
|                         +----------------v----------+ |
|                         | Standard SBOM Format      | |
|                         | - SPDX (ISO 5962:2021)    | |
|                         | - CycloneDX (OWASP)       | |
|                         +------------+--------------+ |
|                                      |                |
|                    +-----------------v----------+     |
|                    | CVE DB 대조 (취약점 스캔)    |     |
|                    | + VEX (악용 가능성 평가)     |     |
|                    | + Sigstore 서명 (무결성)     |     |
|                    +-----------------------------+     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SBOM은 식품 뒷면의 <strong>성분표</strong>다. 나쁜 재료(취약점)가 발견되면 성분표를 보고 우리 과자가 안전한지 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 표준 포맷

| 포맷 | 주관 | 특징 | 형식 |
|:---|:---|:---|:---|
| **SPDX** | Linux Foundation (ISO 5962) | 법적 라이선스 추적에 강점 | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), RDF, Tag-Value |
| **CycloneDX** | OWASP | 보안 취약점 연계에 강점 | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), XML, Protobuf |

### 핵심 구성 요소

| 요소 | 설명 |
|:---|:---|
| **Inventory** | 포함된 모든 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)(이름·[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·해시) 목록 |
| <strong>Dependency <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/">Graph</a></strong> | 직접·간접 의존성의 트리 구조 |
| **License Info** | 각 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)의 라이선스 유형 (MIT, GPL 등) |
| **Provenance** | 소스 출처, 빌드 환경, [빌더](/knowledge-base/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/) 정보 |

### 3단 보안 결합

1. <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a></strong>: "우리가 뭘 쓰고 있는가?" -> 재고 파악
2. **VEX (Vulnerability Exploitability eXchange)**: "취약하지만 우리 코드에서 실제 실행되는가?" -> 오탐 제거
3. **Sigstore/Cosign**: "이 SBOM은 위조되지 않았는가?" -> [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 보증

- **📢 섹션 요약 비유**: SBOM은 재료 목록, VEX는 "이 재료가 진짜 위험한가?" 판단, Sigstore는 목록 자체의 위조 방지 인감이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) ([정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)) | [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) ([오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 스캔) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 추출 |
|:---|:---|:---|:---|
| **분석 대상** | 내가 짠 코드 | 사용 중 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) | **전체 구성요소 명세** |
| **목적** | 코딩 실수 탐지 | 알려진 취약점 탐지 | <strong>투명성·<a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 관리</strong> |
| **산출물** | 취약점 리포트 | 패치 권고 | <strong>표준 명세서 (<a href="/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/">JSON</a>)</strong> |
| **상호작용** | - | SBOM을 입력으로 사용 | SCA의 기초 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 통합 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>Syft/Trivy</strong>를 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 빌드 스텝에 추가하여 매 빌드마다 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/).
2. **Full Inventory**: 직접 의존성뿐 아니라 Transitive Dependency까지 포함.
3. **서명**: Cosign으로 SBOM에 디지털 서명 부착 -> 배포 시 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/).
4. **저장**: [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) Registry에 SBOM을 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지와 함께 Attestation으로 첨부.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>빌드 후 수동 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: 빌드 환경과 불일치하는 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) -> [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 0.
- <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>만 하고 스캔 미연동</strong>: 명세서를 만들어놓고 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 대조를 안 하면 의미 없음.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 미도입 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 개선 |
|:---|:---|:---|:---|
| Log4j 포함 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | **수주** (수동 조사) | **수초** (자동 대조) | 99.9% 단축 |
| 라이선스 컴플라이언스 | 사후 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | <strong>빌드 시 자동 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> | 법적 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 제거 |
| [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 투명성 | 블랙박스 | **완전 가시성** | 고객 신뢰 확보 |

SBOM은 Google SLSA 프레임워크와 결합하여 빌드 전 과정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 증명하는 핵심 증거로 진화하고 있으며, 모든 소프트웨어 납품 시 '영양성분표'처럼 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 제출을 요구하는 시대가 도래했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/">Supply Chain Security</a></strong> | SBOM이 해결하려는 전체 맥락 |
| **SPDX / CycloneDX** | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 표준 포맷 |
| <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/">CVE</a> (Common Vulnerabilities)</strong> | SBOM과 대조하는 취약점 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) |
| **VEX** | 취약점의 실제 악용 가능성을 평가하는 보충 문서 |
| **SLSA (Supply-chain Levels)** | 빌드 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 보안 등급 체계 |
| **Sigstore / Cosign** | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 및 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지의 디지털 서명 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Log4Shell 사태 (2021.12) — 공급망 취약점 충격]
    |
    v
[미 행정명령 EO 14028 (2021) — 연방 SW에 SBOM 의무화]
    |
    v
[SPDX ISO 표준화 (2021) — ISO/IEC 5962:2021]
    |
    v
[Sigstore + SLSA (2022~) — 빌드 무결성 + 서명 자동화]
    |
    v
[현재: SBOM + VEX + SLSA 3단 결합이 DevSecOps 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 우리가 먹는 과자 뒤에 어떤 재료가 들어갔는지 적힌 <strong>성분표</strong>를 본 적 있니?
2. SBOM은 컴퓨터 프로그램에 어떤 재료([라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))가 들어갔는지 꼼꼼히 적어둔 명세서야.
3. 나쁜 재료(취약점)가 발견되면 이 명세서를 보고 우리 프로그램이 안전한지 바로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있단다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 109 / 373

<- **이전**: [108. 테스트 데이터 마스킹 파이프라인 (Test Data Masking)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/108_test_data_masking_pipeline/)
**다음**: [110. 무중단 DB 스키마 롤아웃 (Zero-Downtime) - Expand and Contract 패턴](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/110_zero_downtime_db_schema_rollout/) ->

---
