---
title: "Infrastructure As Code Terraform"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
weight: 724
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

과거의 인프라 엔지니어(시스템 관리자)들은 서버 한 대를 띄우기 위해 서버실에 들어가 랜선을 꽂고, 리눅스 CD를 넣고, 밤새워 까만 화면에 리눅스 명령어를 타이핑했다. 클라우드(AWS)가 등장하자 서버실에 갈 필요는 없어졌지만, 여전히 웹 브라우저 콘솔에 접속해서 수십 번의 '마우스 클릭'을 통해 서버(EC2)와 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group)을 만들어야 했다.

문제는 <strong>'사람의 실수(Human Error)'와 '재현 불가능성'</strong>이었다. 클릭으로 서버를 만들면, "어제 내가 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 포트를 80번을 열었나, 8080번을 열었나?"를 아무도 기억하지 못했다. 퇴사한 직원이 만든 서버와 똑같은 서버를 하나 더 만들려면 며칠 밤을 새우며 메뉴얼을 뒤져야 했다.

이 눈물겨운 삽질([Toil](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))을 끝내기 위해, <strong>"클릭하지 말고, 우리가 원하는 인프라의 상태를 코드로 적어놓자. 그러면 기계가 알아서 클라우드 API를 호출해 코드를 인프라로 똑같이 번역해 주게 만들자"</strong>는 혁명적인 사상이 등장했다. 이것이 바로 <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a>(<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>)</strong>다.

- **📢 섹션 요약 비유**: 마우스로 인프라를 만드는 건 '모래성 쌓기'다. 발로 차서 부서지면 처음부터 내 손으로 다시 만들어야 한다. IaC는 모래성을 만드는 완벽한 '금형 틀(코드)'을 파놓는 것이다. 모래성이 부서져도 금형에 모래를 붓고 찍어내기만 하면 1초 만에 똑같은 성이 계속 복제된다.

---

다음은 [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) 의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  인프라스트럭처 애즈 코드 (IaC)                         |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) 가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

IaC의 대명사인 <strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">테라폼</a>(<a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a>)</strong>을 기준으로 아키텍처와 작동 원리를 살펴보자.

- **📢 섹션 요약 비유**: [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

---

## Ⅲ. 비교 및 연결

[IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도구들은 크게 <strong>'서버를 찍어내는 도구(<a href="/studynote/09_security/11_iam_access_control/528_provisioning/">Provisioning</a>)'</strong>와 <strong>'서버 안의 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>을 맞추는 도구(<a href="/studynote/12_it_management/02_itsm_itil/873_configuration_management/">Configuration Management</a>)'</strong>로 나뉜다.

| [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 주요 목적 | 대표 도구 | 특징 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a> (<a href="/studynote/09_security/11_iam_access_control/528_provisioning/">Provisioning</a>)</strong> | 인프라 뼈대 창조 ([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/), DB [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) | <strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a></strong>, AWS CloudFormation | 선언적. 여러 클라우드(AWS, GCP)를 동시에 지원함. |
| <strong><a href="/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/">형상 관리</a> (Configuration)</strong> | 뼈대 안의 살 붙이기 (OS [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), Nginx 설치) | <strong><a href="/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/">Ansible</a></strong>, Chef, Puppet | 서버에 접속해서 스크립트를 차례대로 실행함. ([멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 보장) |

최근에는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s)와 같은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술이 발달하면서 서버 안에 Nginx를 까는 '[형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)' 작업은 [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지로 대체되었다. 따라서 현대 인프라 엔지니어링은 **Terraform으로 뼈대를 만들고, Docker로 살을 붙이는** 조합이 대세가 되었다.

- **📢 섹션 요약 비유**: Terraform은 빈 땅에 아파트 건물(서버)을 뚝딱 세우고 수도관(네트워크)을 연결하는 건설사다. Ansible은 지어진 빈 아파트 안에 들어가서 도배를 하고 가구를 배치하는 인테리어 업자다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

IaC를 도입하면 인프라가 텍스트 파일이 되므로, [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 위대한 유산인 <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리(Git)</strong>를 인프라에 그대로 쓸 수 있다. 이를 <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong>라고 부른다.

- **📢 섹션 요약 비유**: [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

IaC를 내재화하면, 메인 서버가 랜섬웨어에 감염되어 파괴되더라도 [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 코드를 다시 실행(`terraform apply`)하는 것만으로 단 10분 만에 백지상태에서 새로운 클라우드에 100대의 서버와 네트워크를 완벽하게 복원해 내는 기적(Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))을 시현할 수 있다.

결론적으로 IaC는 인프라 엔지니어를 '케이블을 꽂는 노동자'에서 '클라우드를 코드로 지휘하는 개발자'로 진화시켰다. 기술 리더는 "우리 회사의 인프라를 지금 당장 다 지웠을 때, 클릭 한 번 없이 100% 동일하게 코드로 살려낼 수 있는가?"를 질문하며 시스템 아키텍처의 재현성(Reproducibility)을 확보해야 한다.

- **📢 섹션 요약 비유**: 마법의 복사기([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))다. 아무리 복잡하게 지어진 레고 성(인프라)이라도, 그 성을 만드는 완벽한 '마법의 주문서(코드)'만 가지고 있다면, 세상 어디서든 주문을 외우기만 하면 똑같은 레고 성이 눈앞에 1초 만에 솟아오르는 마법이다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)에서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
인프라스트럭처 애즈 코드 (IaC) 테라폼 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 897 / 973

<- **이전**: [723. COTS 상용 기성품 통합 테스팅](/studynote/04_software_engineering/10_trends_pm_quality/723_cots_commercial_off_the_shelf_testing/)
**다음**: [725. 선언적 인프라 상태 일치 루프](/studynote/04_software_engineering/10_trends_pm_quality/725_declarative_infrastructure_reconciliation_loop/) ->

---
