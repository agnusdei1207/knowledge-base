+++
title = "120. 선언적 인프라와 멱등성 (Declarative Infrastructure & Idempotence) - IaC 핵심 원칙"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선언적 인프라는 <strong>"무엇을 원하는가(What)"만 정의</strong>하면 도구가 현재→목표 상태로 자동 변환하며, [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)(Idempotence)은 <strong>같은 코드를 여러 번 실행해도 결과가 동일</strong>한 성질이다.
> 2. **가치**: 명령형 스크립트(`apt install nginx`)는 이미 설치된 경우 에러가 나지만, 선언적 코드(`state: present`)는 **이미 설치됐으면 아무 것도 하지 않는다(멱등)**. 이 덕분에 반복 실행이 안전하다.
> 3. **판단 포인트**: [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)·[Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/)(선언적 모드)·K8s manifest가 선언적+멱등 도구의 대표이며, 쉘 스크립트는 본질적으로 <strong>비멱등(idempotent하지 않음)</strong>이므로 IaC에 부적합하다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">명령형 vs 선언적 + 멱등성</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">명령형 (비멱등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1번 실행: apt install nginx → 설치됨 ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2번 실행: apt install nginx → 이미 설치, 에러? ⚠️</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">선언적 (멱등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1번 실행: state=present → nginx 설치됨 ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2번 실행: state=present → 이미 있음, 변경 없음 ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3번 실행: state=present → 여전히 변경 없음 ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 같은 코드 몇 번 실행해도 항상 같은 결과!</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)은 엘리베이터 버튼이다. 1번 누르나 10번 누르나 <strong>같은 층에 도착</strong>한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 도구별 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)

| 도구 | 패러다임 | [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a></strong> | 선언적 (HCL) | ✅ (Plan→Apply) |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/">Ansible</a></strong> | 선언적 (YAML) | ✅ ([state](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 기반) |
| **K8s manifest** | 선언적 (YAML) | ✅ (Reconciliation) |
| **쉘 스크립트** | 명령형 | ❌ (수동 체크 필요) |

- **📢 섹션 요약 비유**: 선언적 도구는 항온기(25도 유지)이고, 쉘 스크립트는 에어컨 리모컨(수동 ON/OFF, 상태 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 명령형 | 선언적 |
|:---|:---|:---|
| **표현** | How (방법) | **What (목표)** |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a></strong> | 수동 구현 | **내장** |
| **반복 실행** | 위험 | **안전** |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | 불가 | **최적** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 멱등 설계 원칙
1. 리소스 존재 여부를 먼저 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 후 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)/수정.
2. `CREATE IF NOT EXISTS` 패턴 활용.
3. 쉘 스크립트 사용 시 `set -e` + 조건 체크로 방어.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 명령형 | 선언적+멱등 | 개선 |
|:---|:---|:---|:---|
| 반복 실행 | 위험 | **안전** | 자동화 신뢰 |
| 드리프트 | 방치 | **자동 복원** | 상태 보장 |
| [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | 불가 | **최적** | 운영 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |

선언적+멱등은 <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a>·<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a>·K8s 운영의 철학적 기반</strong>이며, 이를 이해하지 않으면 현대 인프라 관리를 할 수 없다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a></strong> | 같은 연산 반복 시 결과 동일 |
| <strong>선언적 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | K8s의 핵심 운영 모델 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a></strong> | 선언적 IaC의 대표 도구 |
| **Reconciliation** | 선언 상태로 자동 수렴 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | 선언적+멱등 위에 구축 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">쉘 스크립트 (명령형, 비멱등, 2000s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Puppet/Chef (2005~) — 선언적 구성 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Ansible (2012) — YAML 선언적, 에이전트리스</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Terraform (2014) — 멀티클라우드 선언적 IaC</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: K8s + GitOps — 선언적+멱등의 완전체</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 명령형은 "에어컨 켜, 25도로 맞춰"라고 **하나하나** 말하는 거예요.
2. 선언적은 "방 온도 25도"라고 **목표만 말하면** 항온기가 알아서 조절해요.
3. [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)은 <strong>같은 버튼을 몇 번 눌러도 항상 같은 결과</strong>가 나오는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 973

← **이전**: [119. GitOps (Single Source of Truth) - Git을 단일 진실 원천으로 한 선언적 운영](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)
**다음**: [121. CI/CD 파이프라인 자동화 - 빌드·테스트·배포의 지속적 통합/전달 체계](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/121_cicd_pipeline_automation/) →

---
