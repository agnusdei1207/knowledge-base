+++
title = "036. 클라우드 기반 감리 (Cloud-Based Audit)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

> **핵심 인사이트**
> 1. 클라우드 기반 감리는 전통적 현장 방문 대신 원격 접속·클라우드 산출물 검토·[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 자동화 도구를 활용해 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)·[PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)·[IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경의 정보시스템을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 현대화된 감리 방식이다.
> 2. 클라우드 공유 책임 모델(Shared Responsibility Model)에 따라 감리 범위가 명확히 구분되어야 하며, [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)(Cloud [Service Provider](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/))의 책임 영역(물리 인프라)은 CSP의 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 보고서([SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/855_soc_2/), ISO 27001)로 대체된다.
> 3. [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) 코드 검토, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [CSPM](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/)([Cloud Security](/knowledge-base/studynote/09_security/17_framework_compliance/842_iso_27017_cloud_security/) Posture [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/)) 리포트가 클라우드 감리의 핵심 산출물이 되고 있다.

---

## I. 전통 감리 vs 클라우드 감리

```
전통 감리:
  현장 방문 -> 서버실·문서 확인
  물리적 환경 검토 가능
  산출물: 소스코드, 설계서, 테스트 결과서

클라우드 감리:
  원격 접속 -> 클라우드 콘솔·API
  물리적 접근 불가 (CSP 관리)
  산출물: IaC 코드, CI/CD 로그, CSPM 보고서
           CSP 감사 인증 (SOC 2, ISO 27001)
```

| 감리 항목    | 전통 감리          | 클라우드 감리             |
|-----------|------------------|--------------------------|
| 인프라 검토  | 서버실 직접 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)   | [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 + [CSPM](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/) 리포트  |
| 소스코드    | 서버 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템   | GitHub/GitLab + [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)|
| 보안 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)   | OS/[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 점검    | [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드 검토 + [CSPM](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/)      |
| 변경 이력   | [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 문서    | 코드 커밋 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) + [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 서버 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)    | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) + 복원 테스트  |

> 📢 **섹션 요약 비유**: 전통 감리는 공장에 직접 방문해 기계를 보는 것, 클라우드 감리는 원격 모니터링과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 대체하는 것.

---

## II. 공유 책임 모델과 감리 범위

```
IaaS 환경:
  CSP 책임: 물리, 네트워크, 하이퍼바이저
  고객 책임: OS, 미들웨어, 앱, 데이터, 보안 설정
  감리 대상: 고객 책임 범위 전체

PaaS 환경:
  CSP 책임: OS + 런타임 + 미들웨어
  고객 책임: 앱, 데이터
  감리 대상: 앱 코드, API 설계, 데이터 보호

SaaS 환경:
  CSP 책임: 대부분의 기술 스택
  고객 책임: 데이터 관리, 사용자 설정
  감리 대상: 접근 통제, 데이터 분류, 사용자 관리
```

> 📢 **섹션 요약 비유**: [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 임차 사무실(인테리어 직접), [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 오피스(공용 시설 포함), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 클라우드 앱(모든 인프라 포함) — 감리 범위도 그에 맞게 달라진다.

---

## III. 클라우드 감리 핵심 도구

```
1. IaC (Infrastructure as Code) 검토
   Terraform / CloudFormation 코드 분석
   tfsec, Checkov로 보안 정책 자동 검사

2. CSPM (Cloud Security Posture Management)
   Prisma Cloud, AWS Security Hub
   잘못된 설정(Misconfiguration) 자동 탐지

3. SIEM 로그 분석
   AWS CloudTrail, Azure Monitor
   감사 추적, 접근 로그 검토

4. CI/CD 파이프라인 감사
   SAST/DAST 결과 검토
   취약점 관리 프로세스 확인
```

> 📢 **섹션 요약 비유**: 감리원이 코드 한 줄도 직접 짜지 않지만, 자동화 도구가 모든 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 스캔해 문제를 찾아준다 — 로봇 감리사.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 활용

| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)         | 내용                            | 감리 활용              |
|------------|--------------------------------|----------------------|
| [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/855_soc_2/) Type II | 보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·처리 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 등 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) 보안 역량 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)     |
| ISO 27001   | [정보 보안 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/095_information_security_management/) 체계             | 물리 인프라 보안 대체  |
| CSA STAR    | 클라우드 특화 보안 자가 평가     | 클라우드 보안 성숙도   |
| [PCI](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) DSS     | 결제 카드 산업 보안             | 금융 클라우드 필수     |

> 📢 **섹션 요약 비유**: CSP가 이미 권위 있는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)를 받아 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 받았다면, 감리원은 그 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것으로 물리 인프라 감리를 대체한다.

---

## V. 실무 시나리오 — 공공 클라우드 SI 감리

| 감리 항목           | [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 방법                               |
|-------------------|----------------------------------------|
| 인프라 보안         | AWS [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 리포트, [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서     |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 적합성     | Checkov / tfsec 자동 스캔 결과          |
| [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)           | [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 검토, [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) 활성화 여부           |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화        | [KMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 스토리지 암호화 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)           |
| [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 및 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)          | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 주기, 복원 테스트 기록            |
| [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)           | CloudTrail [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 승인 프로세스   |
| 취약점 관리          | ECR/ACR 이미지 스캔, [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 리포트        |

> 📢 **섹션 요약 비유**: 클라우드 감리원은 서버를 직접 만지지 않지만, 대신 코드·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서라는 디지털 증거를 철저히 검토한다.

---

## 📌 관련 개념 맵

```
클라우드 기반 감리
+-- 공유 책임 모델 이해
|   +-- IaaS / PaaS / SaaS 범위
+-- 핵심 산출물
|   +-- IaC 코드 (Terraform, CloudFormation)
|   +-- CSPM 리포트 (Prisma Cloud)
|   +-- CI/CD 파이프라인 로그
|   +-- CSP 감사 인증 (SOC 2, ISO 27001)
+-- 자동화 도구
|   +-- Checkov / tfsec (IaC 보안)
|   +-- AWS Security Hub / Azure Defender
+-- 관련 개념
    +-- DevSecOps
    +-- Zero Trust 아키텍처
    +-- CSPM, CWPP, CNAPP
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 정보시스템 감리]
현장 방문, 물리적 인프라 검토
      |
      v
[클라우드 도입 초기 (2010s)]
현장 감리 한계 인식
공유 책임 모델 정립
      |
      v
[클라우드 감리 방법론 개발]
원격 접속 + CSP 인증 활용
IaC 코드 검토 표준화
      |
      v
[현재: 자동화 기반 지속적 감리]
CSPM, DevSecOps 통합
스프린트 단위 지속 감리 개념 등장
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 감리는 서버실을 직접 방문하는 대신, 원격으로 코드와 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
2. 클라우드 회사(AWS 등)가 이미 안전하다는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 받았으면, 그 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 물리 보안을 대신해요.
3. 자동화 도구가 수천 개의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 자동으로 점검해서 감리를 더 빠르고 정확하게 만들어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 49 / 530

← **이전**: [36. 감리 품질 관리 (Audit Quality Management)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/036_audit_quality_management/)
**다음**: [037. 데이터 품질 진단 (Data Quality Diagnosis)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/037_data_quality_diagnosis/) →

---
