---
title: 173. 구성 관리 도구 (Configuration Management) — Ansible, Chef, Puppet
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[089_configuration_management|구성 관리]] 도구 ([[089_configuration_management|Configuration Management]] Tool)는 서버가 "어떤 상태여야 하는가"를 코드로 적고, 실제 상태를 그 [[025_baseline|기준선]]으로 수렴시키는 자동화 계층이다.
> 2. **가치**: Ansible은 에이전트리스 (Agentless)로 빠르게 시작하기 좋고, Chef와 Puppet은 에이전트 기반의 지속적 수렴과 [[164_policy|정책]] 통제로 대규모 레거시 서버 운영에 강하다.
> 3. **판단 포인트**: 인프라 [[087_process_state_transition|생성]]은 [[062_infrastructure_as_code|Infrastructure as Code]] ([[793_iac_idempotency_template|IaC]]), 애플리케이션 릴리스는 [[164_continuous_delivery|Continuous Delivery]] (CD), [[001_operating_system_purpose|운영체제]]와 미들웨어의 지속 일관성은 [[089_configuration_management|구성 관리]]가 맡는다는 경계를 분명히 해야 드리프트와 운영 부채가 줄어든다.

---

## Ⅰ. 개요 및 필요성

[[089_configuration_management|구성 관리]] ([[089_configuration_management|Configuration Management]])는 [[001_operating_system_purpose|운영체제]], 패키지, [[009_config|설정]] [[501_file_definition_logical_record|파일]], 사용자 권한, [[090_service_kubernetes_network_load_balancing|서비스]] 기동 상태를 코드로 정의하고 반복 적용해 동일한 서버 상태를 유지하는 방식이다. 서버 수가 한두 대일 때는 [[538_ssh_vs_telnet_secure_remote|Secure Shell]] ([[538_ssh_vs_telnet_secure_remote|SSH]]) 접속과 수작업으로 버틸 수 있지만, 수십 대만 넘어가도 "어느 서버에 어떤 수정이 들어갔는가"가 금세 불투명해진다. 이때 생기는 대표적 문제가 스노우플레이크 서버 ([[541_cassandra|Snowflake]] Server), 즉 문서에도 코드에도 없는 예외 [[009_config|설정]]이 누적된 서버다.

[[089_configuration_management|구성 관리]]가 필요한 이유는 서버 운영의 본질이 "[[087_process_state_transition|생성]]"보다 "유지"에 가깝기 때문이다. [[598_vm_migration_nic|Virtual Machine]] ([[598_vm_migration_nic|VM]])이나 베어메탈 (Bare Metal)은 처음 한 번 띄우는 것보다 이후의 패치, 계정 관리, 보안 [[009_config|설정]], [[090_service_kubernetes_network_load_balancing|서비스]] 재기동, 규정 준수 점검이 훨씬 오래 지속된다. 그래서 Terraform이 서버를 만든 뒤에도, 그 위에 Nginx를 설치하고 `/etc` [[009_config|설정]]을 맞추고 보안 [[025_baseline|기준선]]을 지키게 만드는 별도 계층이 필요하다.

아래 그림은 [[089_configuration_management|구성 관리]]가 자동화 스택에서 어디에 놓이는지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                   Where configuration management fits              │
├─────────────────────────────┬──────────────────────────────────────┤
│ Provisioning                │ VM, network, subnet, load balancer  │
│                             │ example: Terraform                  │
├─────────────────────────────┼──────────────────────────────────────┤
│ Configuration management    │ package, file, user, service state  │
│                             │ example: Ansible, Chef, Puppet      │
├─────────────────────────────┼──────────────────────────────────────┤
│ Application delivery        │ artifact rollout, version switch    │
│                             │ example: CI/CD pipeline             │
└─────────────────────────────┴──────────────────────────────────────┘
```

즉 [[089_configuration_management|구성 관리]]는 "인프라를 만든 뒤 아무도 손대지 않는다"는 가정이 깨지는 순간 본격적으로 중요해진다. 특히 전통적인 [[598_vm_migration_nic|VM]], [[002_database_definition|데이터베이스]] 서버, 보안 장비, 사내 미들웨어, [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 노드 [[001_operating_system_purpose|운영체제]]처럼 장기 생명주기를 가진 자산에서는 여전히 핵심 역할을 한다.

- **📢 섹션 요약 비유**: 새 아파트를 짓는 일은 프로비저닝이고, 입주 후 전기·수도·가구 배치를 표준대로 계속 유지하는 일은 [[089_configuration_management|구성 관리]]다. 집을 한 번 세우는 것보다 같은 상태로 오래 관리하는 일이 더 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[089_configuration_management|구성 관리]] 도구의 핵심 원리는 세 가지다. 첫째, 원하는 상태 ([[080_kube_controller_manager_desired_state|Desired State]])를 코드로 선언한다. 둘째, [[178_as_is_to_be_analysis|현재 상태]] (Actual [[272_state_pattern|State]])를 읽어 차이를 계산한다. 셋째, 같은 코드를 다시 실행해도 결과가 망가지지 않는 [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]])을 지향한다. 예를 들어 "Nginx 패키지가 설치되어 있어야 한다", "[[009_config|설정]] [[501_file_definition_logical_record|파일]]은 이 내용과 같아야 한다", "[[090_service_kubernetes_network_load_balancing|서비스]]는 실행 중이어야 한다"를 표현하는 식이다.

도구별 아키텍처는 제어 모델에서 갈린다. Ansible은 컨트롤 노드가 대상 서버에 SSH로 접속해 작업을 밀어 넣는 푸시 (Push) 모델이다. 반면 Chef와 Puppet은 보통 에이전트가 서버 안에 상주하거나 주기적으로 동작해 중앙 서버에서 [[164_policy|정책]]을 받아오는 풀 (Pull) 기반 수렴 모델에 가깝다. 이 차이는 단순 연결 방식이 아니라, "상태를 누가 언제 다시 맞추는가"에 직접 영향을 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                    Convergence model by tool                       │
├───────────────────────────────┬────────────────────────────────────┤
│ Ansible                       │ Chef / Puppet                      │
├───────────────────────────────┼────────────────────────────────────┤
│ Control node                  │ Policy server / master            │
│   │                           │        ▲                          │
│   ├─ SSH push --------------> │        │ periodic pull            │
│   ├─ module execution         │   agent on each node              │
│   └─ run on demand            │   continuous convergence          │
│                               │   compliance-friendly             │
└───────────────────────────────┴────────────────────────────────────┘
```

| 비교 축 | [[198_ansible_os_configuration_management_ssh|Ansible]] | Chef | Puppet |
| :--- | :--- | :--- | :--- |
| 기본 제어 모델 | Push | Pull 중심 | Pull 중심 |
| 에이전트 | 없음 | Chef [[003_audit_stakeholders|Client]] 필요 | Puppet Agent 필요 |
| 주 표현 방식 | YAML Ain't Markup Language (YAML) [[637_playbook|Playbook]] | Ruby Domain-Specific Language (DSL) Recipe | Puppet DSL Manifest |
| 강점 | 시작이 빠르고 운영자 친화적 | 복잡한 로직과 재사용성 | 강한 선언형 모델과 규정 준수 |
| 주된 운영 감각 | 실행형 [[073_container_orchestration_tools|오케스트레이션]] | 코드형 시스템 관리 | [[164_policy|정책]]형 [[025_baseline|기준선]] 관리 |

여기서 중요한 차이는 "실행"과 "지속 수렴"이다. Ansible은 사람이 파이프라인이나 운영 작업에서 Playbook을 실행할 때 강력하고, Chef/Puppet은 시간이 지나도 [[025_baseline|기준선]]을 계속 강제하는 구조에 더 잘 맞는다. 다만 Ansible도 모듈을 잘 선택하면 선언형으로 운영할 수 있고, Chef/Puppet도 결국 운영 방식에 따라 차이가 줄어들 수 있으므로 도구 이름보다 운영 모델을 먼저 봐야 한다.

또 하나의 핵심은 셸 스크립트와 전용 모듈의 차이다. `shell: useradd ...`처럼 명령만 던지면 매번 결과를 예측하기 어렵지만, `user`, `package`, `service` 같은 전용 리소스나 모듈은 [[178_as_is_to_be_analysis|현재 상태]]를 알고 필요한 변경만 수행한다. [[089_configuration_management|구성 관리]] 도구의 진짜 힘은 자동화 그 자체보다 **반복 실행해도 같은 상태로 수렴하는 성질**에서 나온다.

- **📢 섹션 요약 비유**: Ansible은 감독이 직접 각 지점을 순회하며 [[435_checklist_based_testing|체크리스트]]를 수행하는 방식이고, Chef와 Puppet은 각 지점 직원이 본사 매뉴얼을 주기적으로 확인하며 스스로 표준 상태로 되돌리는 방식이다.

---

## Ⅲ. 비교 및 연결

[[198_ansible_os_configuration_management_ssh|Ansible]], Chef, Puppet을 비교할 때는 "어느 도구가 더 현대적인가"보다 "내 환경의 생명주기와 통제 요구가 무엇인가"를 보는 것이 정확하다. 짧은 러닝커브, 멀티클라우드, 네트워크 [[292_accessibility_kwcag_wcag|접근성]], 운영자 중심 파이프라인이 중요하면 Ansible이 유리하다. 반대로 장기 운영 서버가 많고, 중앙 [[164_policy|정책]] 강제, [[606_auditing_linux_auditd|감사]], 규정 준수, 자동 드리프트 수정이 중요하면 Puppet이나 Chef가 더 설득력 있다.

| 상황 | 더 어울리는 선택 | 이유 |
| :--- | :--- | :--- |
| 클라우드 [[459_quic_fec_forward_error_correction|초기]] 자동화, 소규모 운영팀 | [[198_ansible_os_configuration_management_ssh|Ansible]] | [[538_ssh_vs_telnet_secure_remote|SSH]] 기반으로 빠르게 도입 가능 |
| 레거시 서버 수백~수천 대, 지속 [[025_baseline|기준선]] 관리 | Puppet | 선언형 [[025_baseline|기준선]]과 리포팅이 강함 |
| 복잡한 애플리케이션 조립, 개발자 DSL 친화성 | Chef | Ruby 기반 재사용성과 세밀한 로직 |
| [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 노드, 미들웨어, [[002_database_definition|데이터베이스]] OS 운영 | [[198_ansible_os_configuration_management_ssh|Ansible]] 또는 Puppet | 장기 서버 상태 관리가 핵심 |
| 완전 불변 이미지 중심 플랫폼 | [[089_configuration_management|구성 관리]] 비중 축소 | 이미지 빌드와 재배포가 더 적합 |

[[089_configuration_management|구성 관리]] 도구는 다른 자동화 계층과도 경계가 분명해야 한다. [[062_infrastructure_as_code|Infrastructure as Code]] ([[793_iac_idempotency_template|IaC]])는 서버를 만들고 네트워크를 연결하는 데 강하고, 이미지 빌더인 Packer는 베이스 이미지를 굽는 데 강하며, GitOps는 선언 [[501_file_definition_logical_record|파일]]을 Git으로 운영하는 통제 모델이다. [[089_configuration_management|구성 관리]]는 이들 사이에서 "[[087_process_state_transition|생성]] 후 [[001_operating_system_purpose|운영체제]]와 [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 계속 일관되게 맞추는 역할"을 담당한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                     Related automation layers                      │
├─────────────────────────────┬──────────────────────────────────────┤
│ Terraform / IaC             │ create infrastructure               │
│ Packer / image build        │ bake reusable base image            │
│ Config management           │ converge OS / middleware state      │
│ CI/CD / GitOps              │ release application and policy      │
└─────────────────────────────┴──────────────────────────────────────┘
```

이 연결 관점이 중요한 이유는, [[089_configuration_management|구성 관리]] 도구에 모든 문제를 집어넣으면 자동화가 오히려 흐려지기 때문이다. 예를 들어 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 안에 무거운 원격 셸을 넣거나, [[198_ansible_os_configuration_management_ssh|Ansible]] [[637_playbook|Playbook]] 안에서 네트워크 토폴로지까지 모두 만들기 시작하면 책임 경계가 흐려진다. 좋은 설계는 "[[087_process_state_transition|생성]], 수렴, 배포"를 나누되 서로 잘 연결하는 구조다.

- **📢 섹션 요약 비유**: 건물을 지을 때 설계팀, 시공팀, 유지보수팀의 역할이 다르듯이, IaC와 [[089_configuration_management|구성 관리]], 배포 자동화도 각각 맡아야 할 구역이 다르다. 한 팀이 다 하려고 하면 오히려 사고 지점이 많아진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 흔한 성공 패턴은 "Terraform으로 만들고, [[198_ansible_os_configuration_management_ssh|Ansible]]·Chef·Puppet으로 맞추고, [[090_configuration_item|CI]]/CD로 배포한다"는 분리 구조다. 이렇게 하면 인프라 [[087_process_state_transition|생성]] 실패와 [[001_operating_system_purpose|운영체제]] 구성 실패, 애플리케이션 릴리스를 서로 독립적으로 추적할 수 있다. 또한 Git 저장소 구조도 [[793_iac_idempotency_template|인프라 코드]], [[089_configuration_management|구성 관리]] 코드, 애플리케이션 배포 코드를 분리해야 변경 리뷰가 쉬워진다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                   Practical operating pipeline                     │
├────────────────────────────────────────────────────────────────────┤
│ Git change                                                         │
│   │                                                                │
│   ├─ IaC pipeline ----------> VM / subnet / security group         │
│   ├─ Config pipeline -------> package / file / service baseline    │
│   └─ Release pipeline ------> app artifact / rollout               │
│                                                                    │
│ Periodic run or agent check -> detect drift -> converge again      │
└────────────────────────────────────────────────────────────────────┘
```

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 비밀정보는 [[198_ansible_os_configuration_management_ssh|Ansible]] [[567_vault|Vault]], HashiCorp [[567_vault|Vault]], Puppet Hiera 같은 별도 [[514_secret_management_vault_kms|시크릿]] 관리와 연계한다.
2. 가능하면 `package`, `service`, `template`, `user` 같은 전용 리소스를 쓰고, `shell`과 `command`는 예외로 둔다.
3. Inventory나 Node Classification을 환경별로 분리해 개발·[[395_verification_process_review|검증]]·운영 [[025_baseline|기준선]]을 명확히 나눈다.
4. 실행 [[568_logs_distributed_logging_elk_fluentd|로그]], 드리프트 보고서, 실패 리트라이 [[164_policy|정책]]을 남겨 [[606_auditing_linux_auditd|감사]] 가능성을 확보한다.
5. 패치와 보안 [[025_baseline|기준선]]은 주기 실행 또는 지속 수렴으로 유지한다.

### 선택 판단

| 판단 질문 | 권장 답변 |
| :--- | :--- |
| 팀이 빠르게 시작해야 하고 [[538_ssh_vs_telnet_secure_remote|SSH]] 접근이 가능한가? | [[198_ansible_os_configuration_management_ssh|Ansible]] 우선 검토 |
| 중앙 [[164_policy|정책]] 강제와 지속적 재수렴이 더 중요한가? | Puppet 또는 Chef 검토 |
| 장기 서버보다 [[561_container_based_deployment|컨테이너]] 이미지 교체가 중심인가? | [[089_configuration_management|구성 관리]]보다 이미지/[[073_container_orchestration_tools|오케스트레이션]] 우선 |
| 운영자가 수동 변경을 자주 하는가? | 드리프트 보고와 재수렴 체계를 먼저 마련 |

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 운영 중 콘솔과 SSH로 직접 수정한 내용을 코드에 반영하지 않는 것
- Playbook이나 Recipe 안에 비밀정보를 평문으로 남기는 것
- 비멱등 셸 스크립트로 "한 번만 성공하는 자동화"를 만드는 것
- [[089_configuration_management|구성 관리]] 도구로 네트워크 [[087_process_state_transition|생성]]부터 애플리케이션 릴리스까지 모든 책임을 섞는 것

기술사 답안에서는 "Ansible이 쉽다" 수준에서 멈추지 말고, **에이전트 유무 → 제어 모델 → 지속 수렴 여부 → 드리프트 통제 → IaC와의 경계** 순서로 설명하면 깊이가 살아난다. 결국 도구 비교는 기능 목록이 아니라 운영 책임 설계의 문제다.

- **📢 섹션 요약 비유**: 학교를 운영할 때 학생 명단을 만드는 일, 교실 규칙을 유지하는 일, 수업 자료를 배포하는 일은 서로 다르다. [[089_configuration_management|구성 관리]] 도구는 그중 "모든 교실이 같은 규칙을 지키게 하는 생활지도부"에 가깝다.

---

## Ⅴ. 기대효과 및 결론

[[089_configuration_management|구성 관리]] 도구를 제대로 도입하면 서버 온보딩 시간은 줄고, 장애 복구와 보안 [[025_baseline|기준선]] 유지, [[606_auditing_linux_auditd|감사]] 대응이 훨씬 쉬워진다. 특히 새 서버를 띄웠을 때 사람이 문서를 뒤져 수동 [[009_config|설정]]하는 대신, 코드를 재실행해 기준 상태로 되돌릴 수 있다는 점이 크다. 이는 속도보다 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 측면에서 더 큰 가치다.

물론 한계도 있다. 에이전트 기반 도구는 운영 부담이 있고, 에이전트리스 도구는 지속 수렴을 별도로 설계해야 한다. 또한 모든 인프라가 불변 이미지와 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]로 옮겨간 환경에서는 [[089_configuration_management|구성 관리]]의 역할이 줄어들 수 있다. 그러나 [[001_operating_system_purpose|운영체제]] 수준 패치, 미들웨어, [[002_database_definition|데이터베이스]], 사내 레거시 시스템, 규정 준수 [[025_baseline|기준선]]에서는 여전히 대체하기 어렵다.

따라서 이 주제는 "셸 스크립트를 예쁘게 만든 도구"가 아니라, **서버 상태를 코드로 수렴시키는 운영 체계**로 기억해야 한다. [[198_ansible_os_configuration_management_ssh|Ansible]], Chef, Puppet의 차이는 문법보다 수렴 방식과 조직 운영 모델의 차이에서 생긴다.

- **📢 섹션 요약 비유**: [[089_configuration_management|구성 관리]] 도구는 체인점 운영 매뉴얼을 넘어서, 매일 매장 상태를 돌아보며 진열대와 가격표를 본사 기준으로 다시 맞추는 점검 시스템과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[080_kube_controller_manager_desired_state|Desired State]] | 서버가 도달해야 할 [[025_baseline|기준선]] 상태 |
| [[194_idempotency|Idempotency]] | 같은 코드를 여러 번 적용해도 결과가 안정적인 성질 |
| Drift | 실제 서버 상태가 코드 [[025_baseline|기준선]]에서 벗어나는 현상 |
| Inventory / Node [[107_classification|Classification]] | 어떤 서버에 어떤 [[164_policy|정책]]을 적용할지 결정하는 대상 정의 |
| Agentless / Agent-based | Push 실행과 지속 Pull 수렴을 가르는 운영 모델 |
| [[204_immutable_infrastructure_configuration_drift_prevention|Immutable Infrastructure]] | [[089_configuration_management|구성 관리]]의 일부 역할을 이미지 교체로 대체하는 접근 |
| [[119_gitops_single_source_of_truth|GitOps]] | [[089_configuration_management|구성 관리]] 코드의 변경 통제와 [[606_auditing_linux_auditd|감사]] 추적을 강화하는 운영 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
Manual SSH and shell script
    │
    ▼
Configuration management
    ├─ Ansible: push, agentless, fast adoption
    ├─ Chef: recipe-driven, reusable logic
    └─ Puppet: policy-driven, continuous convergence
    │
    ▼
IaC separation + secret management + drift control
    │
    ▼
Immutable image / GitOps / policy as code coexistence
```

이 흐름은 서버 운영이 수동 접속에서 출발해, 상태 수렴 자동화와 드리프트 통제를 거쳐, 불변 이미지와 Git 기반 통제 모델로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[089_configuration_management|구성 관리]] 도구는 학교의 모든 교실을 같은 규칙대로 꾸미는 [[435_checklist_based_testing|체크리스트]] 로봇이에요.
2. Ansible은 선생님이 직접 교실을 돌며 확인하는 방식이고, Chef와 Puppet은 각 교실이 스스로 규칙을 다시 맞추는 방식이에요.
3. 그래서 새 교실이 생겨도 같은 책상, 같은 시간표, 같은 규칙을 빠르게 맞출 수 있어요.
