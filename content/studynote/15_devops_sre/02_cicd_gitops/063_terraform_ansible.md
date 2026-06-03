---
title: 63. Terraform vs Ansible
date: '2026-04-05'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Terraform은 선언형으로 인프라 자원을 [[528_provisioning|프로비저닝]]하고, Ansible은 절차형으로 서버 [[009_config|설정]]과 [[089_configuration_management|구성 관리]]를 자동화한다.
> 2. **가치**: Terraform은 상태([[272_state_pattern|State]])와 계획(Plan)으로 인프라 변경을 예측 가능하게 만들고, Ansible은 기존 서버에 빠르게 적용하기 쉽다.
> 3. **판단**: 두 도구는 경쟁 [[083_relationship_in_er_model|관계]]가 아니라 보완 [[083_relationship_in_er_model|관계]]이며, 인프라 [[087_process_state_transition|생성]]과 구성 적용을 분리하면 운영 품질이 올라간다.

---

## Ⅰ. 개요 및 필요성

현실의 운영은 "서버를 만들기"와 "서버를 [[009_config|설정]]하기"가 다르다. Terraform과 Ansible은 이 둘을 각각 잘하는 도구다.

Terraform은 최종 상태를 선언하는 데 강하고, Ansible은 각 서버에 순서대로 명령을 내려 상태를 맞추는 데 강하다. 그래서 둘을 같은 기준으로 비교하면 안 된다.

- **📢 섹션 요약 비유**: 집을 새로 짓는 일과, 이미 있는 집에 가구를 배치하는 일은 같은 일이 아니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Terraform
Code -> Plan -> State -> Apply -> Provider -> Cloud API

Ansible
Inventory -> Playbook -> Task -> Host Change
```

| 개념 | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] | [[198_ansible_os_configuration_management_ssh|Ansible]] |
| :-- | :-- | :-- |
| 스타일 | 선언형 | 절차형 |
| 주 역할 | 인프라 [[528_provisioning|프로비저닝]] | [[089_configuration_management|구성 관리]] |
| 상태 관리 | [[272_state_pattern|State]] 필수 | 실행 시점 [[178_as_is_to_be_analysis|현재 상태]] 중심 |
| 강점 | 변경 예측, [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] | [[009_config|설정]] 배포, 운영 자동화 |
| 대표 입력 | HCL | YAML |

Terraform은 "무엇이 있어야 하는가"를 정의하고, Ansible은 "무엇을 어떤 순서로 해야 하는가"를 정의한다. 이 차이가 두 도구의 핵심이다.

- **📢 섹션 요약 비유**: 완성된 집 설계도와, 그 집 안에 가구를 놓는 작업 지시서가 다르다.

---

## Ⅲ. 비교 및 연결

| 도구 | 적합한 작업 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] | [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]], EC2, LB, DB [[087_process_state_transition|생성]] | 재현성, 상태 관리 | 구성 세부는 약함 |
| [[198_ansible_os_configuration_management_ssh|Ansible]] | 패키지 설치, [[009_config|설정]] [[501_file_definition_logical_record|파일]] 배포 | 빠른 적용, 유연성 | 상태 관리가 약함 |
| CloudFormation | AWS 인프라 | AWS 통합 | AWS 종속 |
| Pulumi | 복잡한 로직 포함 [[793_iac_idempotency_template|IaC]] | 일반 언어 표현력 | 학습 부담 |

Terraform과 Ansible은 함께 쓸 때 가장 자연스럽다. Terraform으로 기반 자원을 만들고, Ansible로 OS와 애플리케이션 구성을 맞추는 방식이 흔하다.

- **📢 섹션 요약 비유**: 땅을 사고 뼈대를 세우는 일과, 벽지를 바르고 전등을 다는 일은 같은 도구로만 처리할 필요가 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 인프라 [[087_process_state_transition|생성]]과 [[009_config|설정]] 변경을 분리했는가?
2. [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] State를 원격 저장소와 잠금으로 관리하는가?
3. [[198_ansible_os_configuration_management_ssh|Ansible]] Playbook이 idempotent하게 작성되었는가?
4. Secret과 [[303_authentication_authorization_patterns|인증]]정보를 안전하게 분리했는가?
5. Plan 리뷰와 Apply 승인을 분리했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Terraform으로 운영 서버의 세세한 패키지 [[009_config|설정]]까지 다 우겨 넣는 설계
- Ansible로 클라우드 자원 [[087_process_state_transition|생성]]을 억지로 장악하는 설계
- [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]]을 로컬에만 두고 협업하는 설계
- Playbook이 서버마다 다른 예외를 잔뜩 품는 설계

기술사 관점에서는 "어떤 도구가 더 세다"보다 "무엇을 어디서 관리할지 경계를 나누는가"가 중요하다. 경계가 명확해야 변경과 책임이 함께 선명해진다.

- **📢 섹션 요약 비유**: 큰 공사는 설계팀과 시공팀을 나눠야 덜 엉킨다.

---

## Ⅴ. 기대효과 및 결론

Terraform과 Ansible을 적절히 분리하면 인프라는 더 예측 가능해지고, 장애 [[658_ir_recovery|복구]]와 환경 재현이 쉬워진다. 결국 운영은 "한 번 잘 만드는 것"보다 "항상 같은 방식으로 만드는 것"이 더 중요하다.

결론적으로 Terraform은 기반을, Ansible은 그 위의 질서를 담당한다.

- **📢 섹션 요약 비유**: 땅과 집을 만드는 사람, 집 안을 정리하는 사람이 나뉘어야 일터가 깔끔하다.

---

## 관련 개념 맵

```text
Infrastructure as Code
  ↓
Terraform
  ↓
State / Provider
  ↓
Ansible
  ↓
Configuration Management
```

---

## 관련 키워드 및 발전 흐름도

```text
수동 서버 설정
  ↓
스크립트 자동화
  ↓
Terraform / Ansible
  ↓
GitOps / IaC
```

---

## 어린이를 위한 3줄 비유 설명

Terraform은 새 집을 짓는 도구예요.  
Ansible은 그 집 안을 깔끔하게 정리하는 도구예요.  
둘을 같이 쓰면 집도 빠르고 예쁘게 완성돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 63 / 373

← **이전**: [[062_infrastructure_as_code|62. 인프라스트럭처 애즈 코드 (Infrastructure as Code, IaC)]]
**다음**: [[064_git_flow_branch_strategy_release|64. Git Flow - 5개 브랜치 전략과 릴리스 관리]] →

---
