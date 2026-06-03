+++
title = "125. 12 Factor App - 클라우드 네이티브 애플리케이션 설계 12원칙"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 12 Factor App은 Heroku 공동창업자가 정리한 **[SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)/[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 애플리케이션 설계의 12가지 [Best Practice](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)**이며, 이식성·확장성·개발-운영 일관성을 보장한다.
> 2. **가치**: 12 Factor를 따르지 않은 앱은 **환경 의존성·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 하드코딩·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 직접 관리** 등으로 클라우드 배포 시 문제가 발생하지만, 12 Factor를 따르면 **어떤 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)/K8s에서도 동일하게 동작**한다.
> 3. **판단 포인트**: 특히 **III. [Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)([환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/))·VI. Processes([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))·XI. [Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(stdout 스트림)**가 가장 자주 위반되며, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서 12 Factor 준수가 필수이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    12 Factor App                                      │
├───────────────────────────────────────────────────────┤
│  I.   Codebase — 1앱 = 1리포                         │
│  II.  Dependencies — 명시적 선언 (requirements.txt)  │
│  III. Config — 환경 변수로 분리 (하드코딩 금지)      │
│  IV.  Backing Services — DB·캐시를 리소스로          │
│  V.   Build/Release/Run — 단계 분리                  │
│  VI.  Processes — Stateless (세션은 외부 저장소)      │
│  VII. Port Binding — 자체 HTTP 서버                   │
│  VIII.Concurrency — 프로세스 수평 확장               │
│  IX.  Disposability — 빠른 시작·우아한 종료          │
│  X.   Dev/Prod Parity — 개발≈프로덕션               │
│  XI.  Logs — stdout 스트림                            │
│  XII. Admin Processes — 일회성 관리 작업              │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 12 Factor는 클라우드 앱의 **건축 법규 12조**이다. 이 규칙을 따라야 어떤 땅(클라우드)에서도 안전한 건물(앱)을 지을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가장 중요한 3가지

| Factor | 핵심 | 위반 예 |
|:---|:---|:---|
| **III. [Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)** | [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/) | DB 비번 하드코딩 |
| **VI. Processes** | [Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) | 로컬 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 저장 |
| **XI. [Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)** | stdout | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 직접 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) |

- **📢 섹션 요약 비유**: Config는 "비밀번호를 코드에 적지 마", Processes는 "기억력(상태)에 의존하지 마", Logs는 "일기장([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) 대신 방송(stdout)해라"이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 앱 | 12 Factor 앱 |
|:---|:---|:---|
| **[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)** | [config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/).xml 포함 | **[환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)** |
| **[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)** | 로컬 메모리 | **[Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)/외부** |
| **[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)** | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 직접 관리 | **stdout 스트림** |
| **배포** | 서버 종속 | **이식 가능** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### K8s와의 매핑
- [Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) → [ConfigMap](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/102_configmap_secret_kubernetes_12_factor_app/)/[Secret](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/).
- Processes → StatelessSet, [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/).
- [Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) → stdout → Fluentd → [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/).
- [Disposability](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/015_disposability/) → Graceful Shutdown (SIGTERM).

---

## Ⅴ. 기대효과 및 결론

12 Factor App은 **[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 설계의 기본 교과서**이며, K8s·[Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)·[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 환경에서 필수 준수 사항이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)** | [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 분리 |
| **[Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)** | 프로세스 무상태 원칙 |
| **[Disposability](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/015_disposability/)** | 빠른 시작·우아한 종료 |
| **[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)** | 12 Factor의 상위 패러다임 |
| **K8s** | 12 Factor 구현의 최적 플랫폼 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 서버 앱 (설정·상태 내장, ~2010s)]
    │
    ▼
[12 Factor App (Heroku, 2011) — SaaS 설계 원칙]
    │
    ▼
[Docker + K8s (2014~) — 12 Factor 최적 구현]
    │
    ▼
[Beyond 12 Factor (2016) — API First, 텔레메트리 등 추가]
    │
    ▼
[현재: 클라우드 네이티브 — 12 Factor + MSA + GitOps]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 12 Factor는 클라우드 앱의 **건축 법규 12가지**예요.
2. "비밀번호를 코드에 적지 마([Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))", "기억력에 의존하지 마([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))" 같은 규칙이에요.
3. 이 규칙을 따르면 어떤 클라우드에서도 **안전하게 앱이 동작**한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 973

← **이전**: [124. 클라우드 네이티브 아키텍처 - CNCF 기반 현대 소프트웨어 개발 패러다임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/124_cloud_native_development_architecture/)
**다음**: [126. BDD (Behavior-Driven Development) - Given/When/Then 행위 기반 개발](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/126_bdd_behavior_driven_development_given_when_then/) →

---
