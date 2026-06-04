+++
title = "430. 서버리스 컨테이너 보안 이미지 스캔 (Serverless Container Image Security Scanning)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **본질**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) [컨테이너 보안](/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/) 이미지 스캔은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지를 빌드 직후 자동 분석하여 취약한 산출물이 운영계에 들어가기 전에 차단하는 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/) 통제 절차다.
2. **가치**: 공개 취약점 목록(Common Vulnerabilities and Exposures, [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/)), 비밀정보 노출, 라이선스 위반을 조기에 발견해 배포 실패 비용보다 훨씬 작은 비용으로 위험을 제거한다.
3. **판단 포인트**: 스캔 자체보다 더 중요한 것은 배포 게이트 연계, 예외 승인 절차, 결과 추적성, 기준 이미지 갱신 주기가 닫힌 통제로 설계되었는지다.

## Ⅰ. 개요 및 필요성
[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [컨테이너 보안](/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/) 이미지 스캔은 [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/[지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD) 파이프라인에서 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지를 이벤트 기반으로 자동 검사하는 방식이다. 감리 관점에서는 “어디서 스캔했는가”보다 “취약 이미지가 승인 없이 운영 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)와 배포 단계로 넘어갈 수 있는가”를 먼저 본다. 즉, 이 주제는 단순 스캐너 도입이 아니라 빌드·검사·승인·배포를 하나의 통제 체계로 묶는 문제다.

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 방식이 중요한 이유는 스캔 작업 자체를 별도 상시 서버 없이 필요할 때만 실행함으로써 비용 효율성과 확장성을 동시에 확보할 수 있기 때문이다. 대규모 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서는 이미지가 수시로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되므로, 수동 검토나 야간 일괄 점검만으로는 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 공격과 최신 취약점 반영 속도를 따라가기 어렵다. 따라서 이미지 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 순간과 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 등록 순간에 자동 차단점을 배치해야 한다.

```text
+----------+   +----------+   +------------+   +----------+
| 소스 변경 |--->| 이미지 빌드 |--->| 서버리스 스캔 |--->| 배포 승인 |
+----------+   +----------+   +------------+   +----+-----+
                                                     |
                                   차단/예외 승인 <---+
```

결국 필요성의 핵심은 속도와 보안을 동시에 잡는 것이다. 기술사 답안에서는 [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 자동화, [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/), 배포 게이트를 한 흐름으로 묶어 서술하면 논지가 단단해진다.
- **📢 섹션 요약 비유**: 공항 수하물 검색대처럼, 짐을 싣기 전에 위험 물건을 걸러야 비행기가 뜬 뒤 비상착륙하는 일을 막을 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리
아키텍처의 핵심은 이미지 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 이벤트를 받아 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 스캐너가 즉시 동작하고, 결과를 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 판정한 뒤, 통과 이미지만 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)와 배포 파이프라인으로 넘기는 폐쇄형 구조다. 여기서 스캔 범위는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 패키지 취약점, [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 의존성, 비밀정보, 악성 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [소프트웨어 자재 명세서](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/690_sbom_software_supply_chain_security/)(Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/), [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 여부까지 확장될 수 있다.

| 구성 요소 | 핵심 원리 | 감리 포인트 |
| --- | --- | --- |
| 이미지 빌드 단계 | 신뢰 가능한 베이스 이미지와 최소 패키지 원칙으로 공격면을 줄인다. | 베이스 이미지 출처, 태그 고정 여부, 재현 가능한 빌드인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 스캔 함수 | 이미지 푸시 또는 빌드 완료 이벤트를 받아 필요 시점에만 스캔을 수행한다. | 스캔 누락 없는 이벤트 연계, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 검토 |
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 및 승인 게이트 | 심각도 기준, 예외 기간, 서명 여부를 규칙으로 판정한다. | 실패 시 기본 차단(Fail Closed), 예외 승인 이력, 만료 관리 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)·배포 연계 | 통과 이미지에만 서명과 배포 권한을 부여한다. | 스캔 결과와 배포 버전의 매핑, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 기준 검토 |

```text
+------------+   +------------+   +------------+
| Build Event |--->| Scan Engine |--->| Policy Rule |
+-----+------+   +-----+------+   +-----+------+
      |                CVE/SBOM/Secret        |
      |                                       | Pass
      v                                       v
+------------+                           +------------+
| Audit Log  |<---------------------------| Registry   |
+------------+                           +------------+
```

핵심 원리는 세 가지다. 첫째, 스캔은 배포 직전이 아니라 이미지 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점에 가까울수록 효과가 크다. 둘째, 결과는 리포트로 끝나면 안 되고 승인 게이트와 연결되어야 한다. 셋째, 예외는 허용하되 만료일과 책임자를 강제해 영구 면제가 되지 않도록 해야 한다.
- **📢 섹션 요약 비유**: 빵 공장에서 굽고 난 뒤 맛만 보는 것이 아니라, 재료 입고·반죽·포장마다 검사를 걸어 불량 빵이 진열대에 오르지 못하게 하는 구조다.

## Ⅲ. 비교 및 연결
[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [컨테이너 보안](/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/) 이미지 스캔은 다른 보안 통제와 역할이 다르므로 비교형 답안이 유리하다. 특히 정적 애플리케이션 보안 테스트(Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing, [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)), [소프트웨어 구성 분석](/knowledge-base/studynote/15_devops_sre/05_devsecops/246_sca_software_composition_analysis_cve/)([Software Composition Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/495_sca_software_composition_analysis/), [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/)), 런타임 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)와의 차이를 분명히 쓰면 답안의 채점 포인트가 선명해진다.

| 비교 항목 | 이미지 스캔 | 정적 애플리케이션 보안 테스트 | 런타임 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| --- | --- | --- | --- |
| 대상 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지, 패키지, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 소스코드 취약 구문 | 운영 중 프로세스·행위 |
| 시점 | 빌드 후·배포 전 | 개발 중·빌드 전 | 배포 후 |
| 강점 | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 통제, 배포 차단, 재현성 | 코드 수준 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 조기 발견 | 실제 공격 탐지와 차단 |
| 한계 | 코드 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 취약점은 제한적 | 환경 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·이미지 취약점은 약함 | 이미 운영계 진입 후 대응 |

따라서 실무 연결은 “소스-이미지-배포-운영” 전 주기에서 어디를 막는 통제인가를 구분하는 데 있다. 이미지 스캔은 그중 배포 직전의 게이트 역할이므로, 앞단의 코드 분석과 뒷단의 런타임 방어를 보완하는 중간 통제로 설명해야 한다.
- **📢 섹션 요약 비유**: 건강검진으로 비유하면, 문진은 소스 분석이고 엑스레이는 이미지 스캔이며 응급실 모니터링은 런타임 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)다. 셋은 같은 병원을 지키지만 맡은 순간이 다르다.

## Ⅳ. 실무 적용 및 기술사 판단
실제 현장에서는 스캐너 도입 여부보다 운영 통제의 완결성이 더 중요하다. [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 기반이라고 해도 스캔 실패 시 배포가 계속된다면 보안 장식품에 불과하다. 기술사는 도구 이름보다 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·증적·예외관리의 닫힘 구조를 평가해야 한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 취약점 심각도 기준이 조직의 [위험 수용](/knowledge-base/studynote/09_security/01_intro_principles/037_risk_acceptance/) 수준과 연결되어 있는가?
- 베이스 이미지와 의존성 갱신 주기가 정해져 있으며 자동 재스캔되는가?
- 예외 승인에 책임자, 만료일, 대체 통제가 함께 기록되는가?
- 통과한 이미지에만 서명, [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 등록, 배포 권한이 부여되는가?
- 결과 리포트가 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 변경관리 기록까지 이어지는가?

답안에서는 “스캔 도구 도입”으로 끝내지 말고 “[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기준 초과 시 자동 차단, 예외는 기한부 승인, 운영 반영 전 재검증”까지 적어야 실무형 판단이 된다. 또한 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 특성상 실행 시간이 짧고 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 높으므로 대량 이미지 처리에 유리하지만, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)과 외부 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 접근 권한은 별도 통제가 필요하다고 쓰면 좋다.
- **📢 섹션 요약 비유**: 학교 급식 검수처럼, 재료 검사표가 있어도 조리사가 마음대로 통과시키면 소용없고, 누가 왜 예외를 허용했는지 끝까지 남아야 안전하다.

## Ⅴ. 기대효과 및 결론
기대효과는 명확하다. 첫째, 취약 이미지의 운영 반입을 사전에 차단해 사고 확률을 낮춘다. 둘째, 자동화된 스캔과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 게이트로 개발 속도를 크게 늦추지 않으면서도 보안 수준을 표준화한다. 셋째, 스캔 이력과 예외 승인 기록이 남아 감리·규제 대응 근거가 강화된다.

결론적으로 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [컨테이너 보안](/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/) 이미지 스캔은 “이미지를 검사한다”는 기술 기능보다 “안전하지 않은 산출물은 배포되지 못한다”는 통제 철학으로 이해해야 한다. 기술사 답안에서는 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 게이트, 예외관리, 추적성을 함께 묶어 쓰는 것이 고득점 포인트다.
- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 탑승 전 교통카드와 짐을 함께 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하듯, 마지막 문 앞에서 한 번 더 통제해야 전체 여정이 안전해진다.

### 📌 관련 개념 맵
- <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/">데브섹옵스</a>(<a href="/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/">DevSecOps</a>)</strong>: 개발·배포 흐름 안에 보안 통제를 내장하는 운영 철학
- <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a></strong>: 이미지 내부 구성요소를 목록화해 취약점 추적과 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 분석을 돕는 증적
- **이미지 서명(Signing)**: 통과한 이미지의 무결성과 승인 상태를 보증하는 배포 조건
- **어드미션 컨트롤(Admission Control)**: [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 등에서 미검증 이미지를 배포 단계에서 차단하는 최종 게이트

### 📈 관련 키워드 및 발전 흐름도
```text
수동 취약점 점검
    v
CI 빌드 후 이미지 스캔
    v
정책 기반 자동 차단
    v
SBOM/서명 연계 공급망 보안
    v
배포·런타임 연동 전주기 검증
```

### 👶 어린이를 위한 3줄 비유 설명
1. 도시락을 싸서 소풍 가기 전에 상한 반찬이 없는지 먼저 검사하는 거예요.
2. 나쁜 반찬이 보이면 도시락 뚜껑을 닫지 못하게 막는 거예요.
3. 그래서 밖에 나가서 배탈 나는 일을 미리 줄일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 508 / 530

<- **이전**: [429. 마이크로 세그멘테이션 기반 제로 트러스트 (Microsegmentation, Zero Trust)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/429_process/)
**다음**: [431. 마이크로 커널 플러그인 확장 구조망 (Microkernel Architecture)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/431_architecture/) ->

---
