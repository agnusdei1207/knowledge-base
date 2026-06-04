---
title: "334. Policy as Code OPA Gatekeeper Rego (OPA Open Policy Agent Gatekeeper Rego ConstraintTemplate Conftest Policy as Code)"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code는 보안·컴플라이언스 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 사람이 읽는 문서가 아닌 코드로 정의하고 자동으로 강제하는 접근 방식이다. [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/), 오픈 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 에이전트)는 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 프로젝트로 Rego 언어로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 작성하고 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 등 다양한 환경에서 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 평가한다.
> 2. **Gatekeeper의 역할**: Gatekeeper는 OPA를 [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) Admission Controller로 구현한 것이다. [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 요청이 들어오면 ConstraintTemplate에 정의된 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 검사하고, 위반 시 요청을 거부한다. "루트로 실행 금지", "특정 [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)만 허용" 같은 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 코드로 강제된다.
> 3. **판단 포인트**: Conftest는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) YAML, [Dockerfile](/studynote/13_cloud_architecture/02_iaas_paas_saas/067_dockerfile_container_image_build_script/), [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 코드를 배포 전에 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 검사한다. 배포 후 Gatekeeper가 런타임에 이중으로 강제해 Defense in Depth를 구현한다.

---

## Ⅰ. 개요 및 필요성

기업이 클라우드 환경을 운영하면서 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)을 모든 팀에 일관되게 적용하는 것이 어려워졌다. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 문서는 무시되거나 잊혀지고, 새 팀원이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 모르면 위반이 발생한다.

[Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 코드로 만들어 자동으로 적용한다. "모든 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 비루트 사용자로 실행해야 한다"는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 코드화되면, 위반 시 배포 자체가 차단된다. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반은 불가능한 것이 된다.

> 📢 **섹션 요약 비유**: [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code는 계산기다. 세금 계산 규칙을 사람이 기억하는 대신 계산기 프로그램에 넣으면 항상 정확하게 적용된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+-------------------------------------------------------------+
|              OPA/Gatekeeper 정책 흐름                        |
+-------------------------------------------------------------+
|                                                             |
|  개발자 kubectl apply ->                                     |
|                         Kubernetes API Server               |
|                                  |                          |
|                                  v                          |
|                    Admission Controller (Gatekeeper)        |
|                                  |                          |
|                    ConstraintTemplate 정책 검사              |
|                    (Rego 언어로 작성된 정책)                 |
|                                  |                          |
|              +-------------------+-------------------+       |
|              v                                       v       |
|           허용 (Admitted)                     거부 (Denied)  |
|           -> Pod 생성                         -> 에러 반환   |
+-------------------------------------------------------------+
```

Rego [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 예시:

```rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.runAsRoot == true
    msg := "루트 사용자로 컨테이너를 실행할 수 없습니다"
}
```

> 📢 **섹션 요약 비유**: Gatekeeper는 클럽 입구 보안요원이다. 드레스코드([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/))에 맞지 않으면 입장(배포)을 거부한다.

---

## Ⅲ. 비교 및 연결

| 항목 | [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) | Gatekeeper | Conftest |
|:---|:---|:---|:---|
| 역할 | 범용 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 | K8s Admission Controller | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 검사 |
| 시점 | 런타임 | 런타임 (Admission) | 배포 전 ([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)) |
| 언어 | Rego | Rego + ConstraintTemplate | Rego |
| 대상 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), K8s | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 전용 | 코드/[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |

[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 계층 구조 ([Defense in Depth](/studynote/09_security/01_intro_principles/012_defense_in_depth/)):
- [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 단계: Conftest로 코드 레벨 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 검사
- 배포 단계: Gatekeeper Admission [Webhook](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 강제
- 런타임: [CSPM](/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/)/[CWPP](/studynote/15_devops_sre/05_devsecops/332_cwpp/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링

> 📢 **섹션 요약 비유**: Conftest는 공항 체크인 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/))이고, Gatekeeper는 탑승구(배포 시점)이다. 두 번 검사해서 잘못된 것이 비행기(프로덕션)에 탑승하지 못하게 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 예시

- 모든 Pod은 리소스 제한(CPU/Memory limits)을 명시해야 한다
- 승인된 [컨테이너 레지스트리](/studynote/13_cloud_architecture/02_iaas_paas_saas/070_container_registry_docker_hub_ecr/)(gcr.io, company.[registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))만 사용 가능
- 프로덕션 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)에는 Ingress에 TLS가 필수
- PersistentVolume은 암호화된 StorageClass만 사용 가능

### ConstraintTemplate 구조

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        deny[msg] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("필수 레이블 누락: %v", [missing])
        }
```

> 📢 **섹션 요약 비유**: ConstraintTemplate은 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 틀이다. 틀(템플릿)을 한 번 만들면 여러 종류의 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)(Constraint)를 같은 모양으로 찍어낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

[Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 도입으로 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)이 자동으로 강제되어 인적 실수로 인한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반이 사라진다. [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)) 목적으로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 이력이 git에 보관되고, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경은 [코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/)를 통해 승인된다.

[Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code의 핵심은 <strong>"<a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 강제하는 것이 아니라 위반을 불가능하게 만드는 것"</strong>이다. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 문서를 교육하는 것보다, 위반 시 자동 차단이 더 효과적인 보안을 달성한다.

> 📢 **섹션 요약 비유**: 속도위반 금지 표지판보다 과속방지턱이 더 효과적이다. [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 과속방지턱으로 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 코드로 자동 강제 |
| [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) | [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 범용 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 |
| Rego | [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 작성 언어 |
| Gatekeeper | K8s Admission Controller [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) 구현체 |
| ConstraintTemplate | Gatekeeper [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 템플릿 |
| Conftest | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 코드 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 검사 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 정책 관리            Policy as Code 등장             현대 정책 자동화
------------------   --------------------------   ------------------------
정책 문서 관리       ->  OPA CNCF 프로젝트 등장    ->  GitOps 정책 관리
이메일 교육              Gatekeeper K8s 통합           AI 기반 정책 추천
감사 수작업              Conftest CI 통합               멀티클라우드 정책
위반 사후 처리           Defense in Depth 구현           Crossplane + OPA
```

### 👶 어린이를 위한 3줄 비유 설명

1. [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code는 규칙을 말로 설명하는 대신 컴퓨터가 자동으로 검사하게 만드는 거예요.
2. Gatekeeper는 학교 입구에서 교복을 입었는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 자동문이에요. 교복([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/))을 안 입으면 자동으로 문이 안 열려요.
3. Rego는 그 자동문에게 무엇을 검사해야 하는지 알려주는 설명서예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 334 / 373

<- **이전**: [333. CNAPP 클라우드 통합 보안 플랫폼 (CNAPP Cloud Native Application Protection Platform](/studynote/15_devops_sre/05_devsecops/333_cnapp/)
**다음**: [335. TDD BDD 인수테스트 Mock 격리 (TDD BDD Acceptance Testing Mock Stub Spy Test Pyramid](/studynote/15_devops_sre/05_devsecops/335_tdd_bdd/) ->

---
