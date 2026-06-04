+++
title = "98. 인프라로서의 코드 (IaC, Infrastructure as Code)"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인프라로서의 코드 ([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), [Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/))는 마우스 클릭과 터미널 수동 명령어로 서버를 세팅하던 방식을 버리고, 인프라의 상태와 구성을 텍스트 형태의 '소스 코드'로 선언하여 자동 구축하는 기술이다.
> 2. **가치**: 코드 한 줄로 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) (Idempotence)을 보장하여 "눈송이 서버 ([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) Server, 구성 드리프트)" 문제를 완벽하게 종식시키고 수천 대의 서버를 1분 만에 동일하게 찍어내는 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 혁명을 가져왔다.
> 3. **판단 포인트**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 코드 작성과 학습 비용([테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) HCL 등)이 발생하지만, Git을 통한 인프라 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리와 1초 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 다중 클라우드 이식성을 얻기 위해 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 환경에서 예외 없이 채택된다.

---

## Ⅰ. 개요 및 필요성

과거의 인프라 구축은 고통스러운 수작업의 연속이었다. 엔지니어가 클라우드 콘솔에 접속해 1번 서버를 켜고, IP를 잡고, 패키지를 설치하는 과정을 10번, 100번 반복해야 했다.

이러한 수작업은 필연적으로 치명적인 인적 오류 (Human Error)를 낳는다. 실수로 4번 서버만 포트를 덜 열거나 패키지 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 틀어지는 현상이 발생하는데, 이를 구성 드리프트 ([Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)) 또는 서로 미세하게 다르다는 뜻의 눈송이 서버 ([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) Server) 문제라고 한다. IaC는 이 끔찍한 노가다와 불일치를 없애기 위해 등장했다. 서버 종류, 개수, 네트워크 설정을 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(YAML, [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), HCL)에 설계도로 적어 두면, 자동화 도구 로봇이 코드를 읽고 클라우드 환경에 완벽히 똑같은 인프라를 지어주는 패러다임 전환이다.

- **📢 섹션 요약 비유**: 수동 인프라 세팅은 도예가가 물레를 돌려 손으로 도자기를 100개 빚는 것과 같습니다. 만들 때마다 미세하게 흠집이 다릅니다. IaC는 완벽한 3D 프린터용 '설계도(코드)'를 입력하여 오차율 0%의 동일한 제품을 수천 개 쏟아내는 제조업의 혁명입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IaC는 주로 명령형 (Imperative) 방식과 선언형 ([Declarative](/knowledge-base/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/)) 방식으로 나뉘지만, [테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) ([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) 같은 현대적 도구는 선언형 철학을 따른다.

```text
+--------------------------------------------------------------+
|              명령형 vs 선언형 방식의 차이점 (IaC 핵심 철학)             |
+--------------------------------------------------------------+
| 1. 명령형 (Imperative, 셸 스크립트 방식)                       |
|    "AWS에 접속해라 --> EC2 생성 명령어를 3번 실행해라"              |
|    (이미 서버가 3대 있는데 또 실행하면 6대가 되어버리는 참사 발생)      |
|                                                              |
| 2. 선언형 (Declarative, Terraform 방식) ★ 멱등성 보장           |
|    "최종 상태(State)가 'EC2 3대 구동 중'이 되게 만들어라"             |
|    (현재 1대가 있다면 2대만 추가하고, 4대가 있다면 1대를 삭제함)       |
|                                                              |
| [IaC 엔진 동작 파이프라인]                                      |
|  [Code(설계도)] --> [IaC Engine (상태 파일 검사)] --> [클라우드 API 통신] |
+--------------------------------------------------------------+
```

엔지니어는 "어떻게 (How) 만들 것인가"를 고민하지 않고, "무엇이 (What) 필요한가"라는 최종 목표 상태만 코드에 선언한다. [테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 등의 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 엔진은 자신이 기록해 둔 상태 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))과 실제 클라우드 환경을 비교(Diff)한 뒤, 누락되거나 변경된 부분만을 API를 통해 정확히 맞춰낸다. 이것이 동일한 코드를 백 번 실행해도 결과가 똑같은 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) (Idempotence)의 원리이다.

- **📢 섹션 요약 비유**: 명령형 방식은 택시기사에게 "우회전 3번, 직진 1번 하세요"라고 말하는 것이고(길을 잘못 들면 망함), 선언형 IaC는 내비게이션에 "목적지: 부산시청"이라고 찍는 것과 같습니다. 현재 위치가 어디든 내비게이션이 알아서 최적 경로를 찾아 목적지(상태)를 달성해 줍니다.

---

## Ⅲ. 비교 및 연결

[IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 생태계는 크게 서버 껍데기를 만드는 '[프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)' 도구와, 만들어진 서버 내부를 세팅하는 '[구성 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/873_configuration_management/)' 도구로 역할이 나뉜다.

| 비교 항목 | [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) ([Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)) 도구 | [구성 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/873_configuration_management/) ([Configuration Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/873_configuration_management/)) 도구 |
|:---|:---|:---|
| **대표 도구** | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) ([테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)), AWS CloudFormation | [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) ([앤서블](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/)), Chef, Puppet |
| **주요 역할** | [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/), 서브넷 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 빈 EC2 인스턴스 띄우기 | 띄워진 EC2 안에 Nginx 깔고 환경변수 세팅하기 |
| **상태 관리** | 별도의 상태 ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 통해 인프라 라이프사이클 추적 | 서버 접속 후 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)을 지키며 패키지 설치 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| **아키텍처 연결**| 하드웨어/클라우드 자원 확보 | OS ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) 위 소프트웨어 세팅 |

최근에는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))와 같은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 오케스트레이션이 인프라와 애플리케이션의 경계를 허물면서 두 역할을 동시에 융합하고 있다. 또한 모든 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드는 애플리케이션 코드처럼 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD ([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포) 파이프라인에 태워져 인프라 변경 자체가 자동화 테스트의 대상이 된다 ([GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 연동).

- **📢 섹션 요약 비유**: [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)([테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/))이 텅 빈 아파트 건물(서버 껍데기)을 짓고 전기와 수도(네트워크)를 연결하는 건설사라면, [구성 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/873_configuration_management/)([앤서블](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/))는 빈집에 들어가 벽지를 바르고 가구를 배치하는(소프트웨어 세팅) 인테리어 업체입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도입은 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 팀의 생산성을 극대화하지만, 그만큼 코드의 권한이 막강하여 치명적 장애를 유발할 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 실무 의사결정

1. <strong>Git 기반 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리 및 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a>)</strong>: 인프라가 텍스트 코드이므로 Git에 올려 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리를 해야 한다. 어제 적용한 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 규칙 변경으로 오늘 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애가 터지면, 클라우드 콘솔을 뒤지는 것이 아니라 Git에서 `git revert` (이전 코드로 되돌리기) 명령을 내린다. [테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)이 즉시 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 과거 상태로 돌려놓는다(1초 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)).
2. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/">멀티 클라우드</a> 이식성 (Portability)</strong>: AWS CloudFormation은 AWS 종속적이지만, [테라폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)은 프로바이더 ([Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)) 플러그인을 통해 AWS, GCP, Azure 코드를 한 번에 관리할 수 있어 [클라우드 벤더 락인](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/063_cloud_vendor_lock_in_avoidance/) ([Lock-in](/knowledge-base/studynote/12_it_management/05_security_compliance/362_lock_in_portability/))을 방지하는 강력한 판단 기준이 된다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **콘솔 혼용의 끔찍한 결말**: IaC로 관리되는 인프라를 운영자가 급하다고 웹 콘솔 화면에서 마우스로 수동 변경해 버리는 짓. IaC의 상태 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))과 실제 클라우드가 불일치 (Drift)하게 되어, 다음번 코드를 배포할 때 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 엔진이 콘솔 변경 사항을 덮어쓰고 날려버리거나 에러를 뿜으며 파이프라인 전체가 마비된다. IaC를 도입했으면 무조건 코드로만 인프라를 수정해야 한다.

- **📢 섹션 요약 비유**: 문서 작업에 비유하자면, [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리는 '수정 기록이 100번 저장된 구글 문서'와 같습니다. 실수로 텍스트를 날려먹어도 언제든 과거 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 클릭 한 번에 살릴 수 있는, 인프라계의 무적 타임머신입니다.

---

## Ⅴ. 기대효과 및 결론

인프라로서의 코드([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))는 단순히 시스템 관리자의 타이핑 수고를 덜어준 것이 아니다. 인프라스트럭처 자체를 소프트웨어 엔지니어링의 영역으로 끌어올린 패러다임 시프트다.

재사용성을 통해 미국 지사 서버를 한국 지사 코드 복붙 하나로 찍어내고, 보안 취약점 점검조차 코드 스캔 도구로([DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/)) 배포 전에 막아낸다. 결국 IaC의 궁극적인 결론은 "인프라는 물리적인 철덩어리나 클릭 설정이 아니라, 논리적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능하고 통제 가능한 소프트웨어 텍스트 그 자체"라는 점이다. 클라우드 시대에 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 없는 인프라 관리는 곧 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 그 자체로 취급된다.

- **📢 섹션 요약 비유**: IaC는 서버 관리자들을 마우스 클릭만 반복하는 '공장 조립 라인 작업자'에서, 거대한 로봇 군단(자동화 엔진)을 코드로 조종하는 '[스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 설계자'로 진화시킨 완벽한 지휘봉입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a> (Idempotence)</strong> | 연산을 여러 번 적용하더라도 결과가 달라지지 않는 성질. [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 신뢰성의 핵심 철학 |
| <strong>구성 드리프트 (<a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/">Configuration Drift</a>)</strong> | 시간이 지나며 서버 설정이 매뉴얼이나 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태와 미세하게 달라져 일관성이 붕괴되는 현상 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">테라폼</a> (<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a>)</strong> | 하시코프사에서 만든 선언형 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도구로, [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 통해 인프라 상태를 추적하는 [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) 표준 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | IaC를 기반으로, 인프라의 배포 및 변경 승인 과정을 개발자의 Git [Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 방식으로 통제하는 최신 워크플로 |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 인프라 프로비저닝 (마우스 클릭, 눈송이 서버 발생)
    |
    v
셸 스크립트 기반 자동화 (명령형, 멱등성 보장 불가)
    |
    v
선언형 IaC 도입 (Terraform, CloudFormation / 멱등성 및 상태 관리)
    |
    v
형상 관리와 결합 (인프라 버전 관리 및 롤백 가능)
    |
    v
GitOps 및 DevSecOps (인프라 CI/CD 파이프라인 자동화 및 코드 보안 점검)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 블록 장난감 성을 만들 때 매번 설명서를 보며 손으로 조립해야 해서, 만들 때마다 모양이 조금씩 다르고 실수도 많았어요.
2. IaC는 똑똑한 블록 조립 3D 프린터에 완벽한 '성 만들기 설계도(코드)'를 컴퓨터로 입력해 주는 거예요.
3. 프린터 스위치만 켜면 1분 만에 오차 하나 없는 똑같은 장난감 성 수백 개가 마법처럼 뚝딱 만들어져서 시간도 아끼고 실수도 없어진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 98 / 973

<- **이전**: [97. DevOps (Development + Operations) - 문화, 자동화, 측정, 공유](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/097_devops_culture_calms/)
**다음**: [99. 지속적 배포 (CD, Continuous Deployment / Delivery)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) ->

---
