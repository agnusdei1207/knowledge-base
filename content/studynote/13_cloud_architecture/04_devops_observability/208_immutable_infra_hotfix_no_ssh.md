+++
title = "208. 인프라 불변성 원칙과 핫픽스 금지 (Immutable Infrastructure)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)([Immutable Infrastructure](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) 원칙은 운영 중인 서버에 직접 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 접속하여 변경하는 것을 금지하고, 모든 변경은 코드→빌드→배포 파이프라인을 통해서만 적용하여 Configuration Drift를 원천 차단한다.
> 2. **가치**: 모든 서버가 Git 코드와 동일한 상태임을 보장하면, 인프라 상태를 언제든지 재현할 수 있고 "이 서버만 특이하게 동작하는" 스노우플레이크([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)) 서버 문제가 사라진다.
> 3. **판단 포인트**: 긴급 핫픽스 압박 상황에서 불변 원칙을 지키려면 "코드 수정→빠른 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD→배포"가 30분 이내에 완료되는 파이프라인 속도가 뒷받침되어야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 서버 관리는 "뮤터블(Mutable)" 방식이었다. 서버에 SSH로 접속해서 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 파일을 직접 수정하고, 패키지를 설치하고, 스크립트를 실행했다. 이 방식은 빠르고 편리하지만 심각한 문제를 만든다: <strong><a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/">Configuration Drift</a>(<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 표류)</strong>.

서버 A에서 수정한 내용이 서버 B, C에는 반영되지 않아, 동일한 역할의 서버들이 서로 다른 상태가 된다. "서버 A에서만 되고 B에서는 안 된다", "이 서버는 왜 이러는지 아무도 모른다"는 상황이 발생한다. 이런 서버를 <strong>눈송이(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/">Snowflake</a>) 서버</strong>라고 한다 — 세상에 하나뿐인 고유한 존재가 되어버린 서버.

[불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)([Immutable Infrastructure](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) 원칙은 이 문제를 근본적으로 해결한다: **서버는 교체(Replace)되지, 수정(Modify)되지 않는다.** 새 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필요하면 새 이미지를 만들어 새 서버를 배포하고 구 서버를 삭제한다. 직접 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 접속은 금지된다.

📢 **섹션 요약 비유**: [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 일회용 컵 원칙이다. 컵이 더러워지면 씻는 것이 아니라 새 컵으로 교체한다. 씻으면 결코 완전히 깨끗해지지 않지만, 새 컵은 항상 완전히 깨끗하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 뮤터블 vs [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 비교

```
[뮤터블 인프라 - 전통 방식]
  서버 A: 초기 설정 v1
    → SSH 접속: 패키지 추가
    → SSH 접속: 설정 변경
    → 상태: 알 수 없음 (누가 뭘 바꿨는지)

[불변 인프라 - 현대 방식]
  코드 변경 (Git)
    → 이미지 빌드 (Docker/AMI)
    → 이미지 테스트
    → 새 서버 프로비저닝 (v2 이미지)
    → 기존 서버 삭제 (v1)
  서버 상태 = 항상 Git 코드와 동일
```

### [Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) 발생 과정

```
  Day 1: 서버 A, B, C 동일한 이미지로 시작
          A = B = C = v1 ✅

  Day 10: 긴급상황! 엔지니어가 A에 SSH 접속
          A: SSH → 패치 적용
          B, C: 변경 없음
          A ≠ B = C ❌ (Drift 시작)

  Day 30: A에 또 다른 변경 적용
          A: 수동 설정 2번 적용
          A ≠ B ≠ C ← 아무도 정확한 차이를 모름 ❌
          
  장애 발생 시: "왜 A만 이상하게 동작하지?" → 원인 불명
```

### [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 구현 패턴

| 패턴 | 설명 | 도구 |
|:---|:---|:---|
| [Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/) [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/) | EC2 이미지를 코드로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 서버 교체 시 새 [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/) 사용 | [Packer](/knowledge-base/studynote/15_devops_sre/05_devsecops/199_packer_aws_ami_baking/), HashiCorp |
| [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지로 모든 환경 캡슐화 | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), Podman |
| [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | Git이 인프라 상태의 단일 진실 공간 | ArgoCD, Flux |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) | 인프라를 코드로 정의, 상태 드리프트 감지 | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), Pulumi |

📢 **섹션 요약 비유**: [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)에서 서버는 마치 프린터 잉크 카트리지와 같다. 잉크가 줄면 리필하는 것이 아니라 새 카트리지로 교체한다. 리필한 카트리지는 품질이 불확실하지만, 새 정품 카트리지는 항상 예측 가능하다.

---

## Ⅲ. 비교 및 연결

### [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 관련 개념 연결

| 개념 | [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)와의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) | [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)의 가장 순수한 구현 (이미지 = 불변) |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) | 인프라 상태를 코드로 정의, Drift 감지 |
| [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | Git 코드와 실제 상태가 항상 일치하도록 강제 |
| Blue-Green 배포 | [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)의 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 교체, 수정 아님 |
| Phoenix Server | 정기적으로 서버를 파괴하고 재생성하는 패턴 |

### 핫픽스 금지와 파이프라인 속도의 트레이드오프

| 상황 | 불변 원칙 준수 | 파이프라인 요건 |
|:---|:---:|:---|
| 일반 업데이트 | ✅ | 1~2시간 파이프라인도 허용 |
| 긴급 보안 패치 | ✅ | 30분 이내 Fast-path 파이프라인 필요 |
| 프로덕션 즉각 장애 | ⚠️ [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 우선 | 이전 이미지로 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |

📢 **섹션 요약 비유**: 불변 원칙과 빠른 파이프라인의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 공장 라인과 품질 검사 속도의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. 품질 검사([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD)를 너무 느리게 하면 긴급 상황에서 "이번 한 번만 검사 건너뛰자"는 유혹이 생긴다. 파이프라인을 빠르게 만드는 것이 원칙을 지키는 실질적 조건이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> 접근 차단 방법</strong>:
```
1. AWS Systems Manager Session Manager 활용
   - SSH 포트(22) 완전 차단
   - SSM Agent를 통한 감사 로그 남기는 접속만 허용
   - 읽기 전용 접속만 허용 (디버깅 목적)

2. K8s kubectl exec 제한
   - OPA/Kyverno 정책으로 kubectl exec 제한
   - 엔지니어링 요청 시 임시 디버그 Pod 생성으로 대체

3. 불변 원칙 예외 관리
   - Break-glass 계정: 긴급 시 접근 가능하나 모든 행동 기록
   - 접근 즉시 알림 발송, 사후 검토 의무화
```

**Phoenix Server Pattern (불사조 서버)**:
```
원칙: 서버는 주기적으로 파괴하고 재생성한다
  - 매주 또는 매달: 모든 서버를 새 이미지로 교체
  - 목적: Drift가 축적되기 전에 초기화
  - 결과: 팀이 항상 "서버를 새로 만드는 것"에 익숙해짐
  
Kcattle, not Pets(소떼, 펫 아님):
  - 전통: 서버에 이름을 붙이고 애정을 가짐 (펫)
  - 현대: 서버는 번호 태그만 있는 소떼 — 하나가 죽으면 새 소가 추가됨
```

**기술사 판단 포인트**:
- 진짜 긴급 상황에서는 "[롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)"이 "핫픽스"보다 항상 빠르다. 이전 이미지로 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) → 근본 원인 파악 → 수정 후 재배포가 안전한 순서다.
- [Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) 감지: [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) `terraform plan`이나 AWS Config로 실제 상태와 코드 상태의 차이를 주기적으로 확인한다.
- 불변 원칙을 강제하는 조직 문화는 "SSH가 불편해야 한다"는 환경 설계로 완성된다. 편리하면 유혹이 생긴다.

📢 **섹션 요약 비유**: 불변 원칙 강제는 사무실 냉장고에 자물쇠를 채우는 것과 같다. 다이어트 중인 사람에게 의지력에만 의존하지 않고 환경 자체가 유혹을 방지하도록 설계한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) 제거 | 모든 서버가 항상 코드와 동일한 상태 |
| 재현 가능한 환경 | 어떤 환경이든 동일한 이미지로 언제든 재생성 |
| 보안 강화 | [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 접근 차단으로 공격 표면 축소 |
| 디버깅 용이성 | "이 서버만 이상하다"는 스노우플레이크 현상 제거 |

[불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 DevOps의 "반복 가능성(Repeatability)"과 "[신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)([Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/))" 원칙의 인프라 수준 구현이다. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 IaC가 표준화된 현대 클라우드 환경에서는 불변 원칙이 기본값이 되어야 한다.

📢 **섹션 요약 비유**: [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 요리사가 매번 같은 레시피로 음식을 만드는 것과 같다. 레시피(코드)가 바뀌지 않으면 음식(서버)은 항상 같은 맛이다. 즉흥으로 요리하면([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 수정) 맛이 달라질 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) | [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)가 해결하는 핵심 문제 |
| [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | Git 상태와 인프라 상태의 지속적 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) | 인프라 상태 코드화 + Drift 감지 |
| Phoenix Server | 주기적 서버 재생성으로 Drift 초기화 패턴 |
| [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 | [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)의 가장 순수한 구현체 |
| Break-glass 계정 | 불변 원칙의 긴급 예외 처리 메커니즘 |

### 👶 어린이를 위한 3줄 비유 설명

1. [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 서버를 레고 블록처럼 생각하는 거야. 블록이 잘못됐으면 그 블록을 고치는 게 아니라 새 블록으로 교체해.

### 📈 관련 키워드 및 발전 흐름도

```text
기존: SSH 접속 → 핫픽스 패치 (드리프트 · 추적 불가)
    │
    ▼
불변 인프라: 변경 = 새 이미지 빌드 → 교체
    ├─► No SSH: SSM Session Manager · kubectl exec
    └─► 긴급 대응: Git 커밋 → CI/CD → 새 이미지 배포
```
2. SSH로 서버를 직접 고치는 건 레고 블록에 매직펜으로 낙서하는 것과 같아. 나중에 뭐가 원본이고 뭐가 낙서인지 모르게 돼.
3. 모든 변경은 새 레고 블록을 만드는 것(코드 → 이미지 빌드 → 배포)으로만 해야 해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 207 / 371

← **이전**: [207. ChatOps (챗옵스)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/207_chatops_slack_bot_deployment/)
**다음**: [209. 시스템 신뢰성과 이중화 (Reliability, Resilience, Redundancy)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/209_resilience_reliability_redundancy/) →

---
