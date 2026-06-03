+++
title = "327. SCA 오픈소스 컴플라이언스 스캔 (SCA Software Composition Analysis Open Source Compliance License Scan)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) ([Software Composition Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/))는 소프트웨어 프로젝트가 사용하는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 알려진 취약점([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))과 라이선스 문제를 자동으로 탐지한다. 현대 소프트웨어의 70~90%가 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)로 구성되어, [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 없는 보안은 절반짜리 보안이다.
> 2. <strong>라이선스 <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong>: [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/)([CVE-2021-44228](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/))처럼 하나의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 취약점이 수천 개 제품에 동시 영향을 준다. GPL 라이선스를 모르고 상업 제품에 포함시키면 법적 분쟁이 발생한다.
> 3. **판단 포인트**: [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 결과의 모든 CVE를 즉시 차단하면 개발이 중단된다. 실제 악용 가능성([CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/) v3 Exploitability), 고정 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 존재 여부, 코드 경로에서 실제 사용 여부를 종합해 우선순위를 정해야 한다.

---

## Ⅰ. 개요 및 필요성

2021년 12월 [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/) 취약점 발표 당일, 전 세계 수만 개 조직이 "우리 제품에 Log4j가 있는가"를 수동으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하느라 수백 시간을 소비했다. [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 도구가 있었다면 30분 만에 답이 나왔을 것이다.

현대 소프트웨어 개발에서 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 사용은 선택이 아닌 필수다. npm 생태계는 200만 개 이상의 패키지, Maven Central은 900만 개 이상의 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)를 보유한다. 개발자가 의도적으로 선택한 직접 의존성 외에도, 그 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 의존하는 간접 의존성(Transitive Dependency)까지 합하면 실제 프로젝트는 수백 개의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)를 포함한다.

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) ([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))은 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 분석의 결과물로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 공식 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 목록이다.

> 📢 **섹션 요약 비유**: SCA는 슈퍼마켓에서 산 가공식품의 모든 원재료와 유통기한을 자동으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해주는 기계다. 원재료 하나하나를 손으로 찾을 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌────────────────────────────────────────────────────────┐
│                SCA 스캔 흐름                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  package.json / pom.xml / requirements.txt             │
│          │                                             │
│          ▼                                             │
│  ┌────────────────────┐                                │
│  │  SCA 도구           │  (Trivy, Snyk, OWASP          │
│  │  의존성 그래프 분석  │   Dependency-Check)           │
│  └──────────┬─────────┘                                │
│             │                                          │
│    ┌────────┴───────────────┐                          │
│    ▼                        ▼                          │
│  CVE 취약점 조회         라이선스 분류                   │
│  (NVD, GitHub Advisory)  (MIT, Apache, GPL, AGPL)      │
│    │                        │                          │
│    ▼                        ▼                          │
│  위험도 점수화           라이선스 컴플라이언스 판단       │
│  (CVSS v3 + Reachability)  (허용/검토 필요/금지)        │
└────────────────────────────────────────────────────────┘
```

라이선스 위험도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/):

| 라이선스 | 특징 | 상업 제품 사용 |
|:---|:---|:---|
| MIT, Apache 2.0, BSD | 관대한 조건, 귀속 표시 필요 | 허용 |
| LGPL | [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 수정 시 공개 의무 | 조건부 허용 |
| GPL v2/v3 | 파생물 전체 공개 의무 | 주의 필요 |
| AGPL | 네트워크 사용도 공개 의무 | 상업 제품 부적합 |
| 라이선스 없음 | [저작권](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/) 불명확 | 금지 |

> 📢 **섹션 요약 비유**: GPL 라이선스 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)를 상업 제품에 포함하는 것은 남의 레시피를 그대로 써서 음식을 팔면서 레시피를 공개하지 않는 것이다. 레시피 작성자(GPL [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/))의 규칙은 반드시 지켜야 한다.

---

## Ⅲ. 비교 및 연결

| 도구 | 특징 | 강점 |
|:---|:---|:---|
| Trivy | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)/[IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)/[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 통합 | 속도, 무료 |
| Snyk | 개발자 친화, IDE 플러그인 | [DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/), Fix [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| OWASP Dependency-Check | Java/NET 특화 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 무료, 넓은 지원 |
| Black Duck | 엔터프라이즈, 라이선스 전문 | 라이선스 분석 |

Reachability Analysis (도달 가능성 분석): 취약한 함수가 실제 애플리케이션 코드에서 호출되는지 분석해 False Positive를 줄이는 고급 기능이다. Snyk, Google Cloud의 Assured [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 등이 지원한다.

> 📢 **섹션 요약 비유**: Reachability 분석은 건물에 균열이 있어도 그 벽이 하중을 받는 내력벽인지 아닌지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이다. 하중 없는 벽의 균열은 긴급하지 않다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 우선순위 결정 기준

1. <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/">CVSS</a> Score</strong>: 7.0 이상 High/Critical 우선
2. **Fixed Version 존재**: 업그레이드 가능한 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 우선 해결
3. **Reachability**: 실제 코드 경로에서 취약 함수가 호출되는가
4. **EPSS Score**: Exploit Prediction Scoring System - 실제 악용 가능성 점수

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. CI에 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 스캔이 통합되어 PR마다 실행되는가?
2. Critical CVE가 있으면 병합이 차단되는가?
3. 라이선스 허용 목록이 정의되어 AGPL 라이선스 도입을 차단하는가?
4. SBOM이 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되고 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 저장소에 저장되는가?

> 📢 **섹션 요약 비유**: [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 우선순위 결정은 응급실 트리아지다. 모든 환자를 동시에 치료할 수 없으니 생명이 위험한 사람부터 처치한다.

---

## Ⅴ. 기대효과 및 결론

[SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 도입으로 [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/) 같은 대형 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 취약점 발표 시 영향 받는 시스템을 수 시간 내에 파악할 수 있다. 라이선스 컴플라이언스 자동화로 법적 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)도 사전 차단된다.

SCA의 본질은 <strong>"내가 사용하는 것을 아는 것"</strong>이다. 직접 작성하지 않은 코드가 전체의 대부분을 차지하는 현실에서, 그 코드의 보안과 라이선스를 자동으로 관리하는 것이 현대 소프트웨어 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)의 출발점이다.

> 📢 **섹션 요약 비유**: SCA는 냉장고 안의 모든 식재료 유통기한을 자동으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 시스템이다. 직접 사온 재료도, 세트 상품에 포함된 재료도 모두 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) ([Software Composition Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/)) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 의존성 취약점·라이선스 스캔 |
| [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) ([Software Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)) | [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) 결과로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 목록 |
| [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) ([Common Vulnerabilities and Exposures](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/)) | 공개 취약점 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| [CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/) ([Common Vulnerability Scoring System](/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/)) | 취약점 위험도 점수 |
| Transitive Dependency | 간접 의존성, 의존성의 의존성 |
| Reachability Analysis | 취약 함수 실제 호출 여부 분석 |

### 📈 관련 키워드 및 발전 흐름도

```text
오픈소스 무관리 시대        SCA 등장                    공급망 보안 시대
──────────────────   ──────────────────────────   ────────────────────────
의존성 수동 관리    →  OWASP Dependency-Check   →  SBOM 의무화 (EO 14028)
CVE 수동 확인           Snyk, Trivy 등장              Reachability 분석
Log4Shell 대응 혼란      CI 통합 스캔                 AI 기반 취약점 예측
                          라이선스 컴플라이언스 도구     CNAPP 내 SCA 통합
```

### 👶 어린이를 위한 3줄 비유 설명

1. SCA는 마트에서 사온 음식 봉지의 유통기한과 알레르기 성분을 자동으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해주는 스캐너예요.
2. 직접 만든 음식 재료뿐만 아니라, 함께 들어온 소스, 양념의 성분도 모두 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
3. 유통기한이 지난 재료([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))나 금지된 성분(라이선스)이 있으면 즉시 알려줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 327 / 373

← **이전**: [326. SAST DAST IAST 보안 테스트 비교 CI 파이프라인 배치 (SAST DAST IAST Security Testing](/knowledge-base/studynote/15_devops_sre/05_devsecops/326_sast_dast_iast/)
**다음**: [328. SBOM 소프트웨어 구성 자재 명세 공급망 방어 (Software Bill of Materials Supply Chain Defense](/knowledge-base/studynote/15_devops_sre/05_devsecops/328_sbom/) →

---
