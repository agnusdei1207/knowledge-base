+++
weight = 120
title = "120. 선언적 인프라와 멱등성 (Declarative Infrastructure & Idempotence) - IaC 핵심 원칙"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선언적 인프라는 **"무엇을 원하는가(What)"만 정의**하면 도구가 현재→목표 상태로 자동 변환하며, [[171_idempotency_iac_terraform|멱등성]](Idempotence)은 **같은 코드를 여러 번 실행해도 결과가 동일**한 성질이다.
> 2. **가치**: 명령형 스크립트(`apt install nginx`)는 이미 설치된 경우 에러가 나지만, 선언적 코드(`state: present`)는 **이미 설치됐으면 아무 것도 하지 않는다(멱등)**. 이 덕분에 반복 실행이 안전하다.
> 3. **판단 포인트**: [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]·[[198_ansible_os_configuration_management_ssh|Ansible]](선언적 모드)·K8s manifest가 선언적+멱등 도구의 대표이며, 쉘 스크립트는 본질적으로 **비멱등(idempotent하지 않음)**이므로 IaC에 부적합하다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    명령형 vs 선언적 + 멱등성                          │
├───────────────────────────────────────────────────────┤
│  [명령형 (비멱등)]                                    │
│   1번 실행: apt install nginx → 설치됨 ✅            │
│   2번 실행: apt install nginx → 이미 설치, 에러? ⚠️  │
│                                                       │
│  [선언적 (멱등)]                                      │
│   1번 실행: state=present → nginx 설치됨 ✅           │
│   2번 실행: state=present → 이미 있음, 변경 없음 ✅   │
│   3번 실행: state=present → 여전히 변경 없음 ✅       │
│   → 같은 코드 몇 번 실행해도 항상 같은 결과!        │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[171_idempotency_iac_terraform|멱등성]]은 엘리베이터 버튼이다. 1번 누르나 10번 누르나 **같은 층에 도착**한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 도구별 [[171_idempotency_iac_terraform|멱등성]]

| 도구 | 패러다임 | [[171_idempotency_iac_terraform|멱등성]] |
|:---|:---|:---|
| **[[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]** | 선언적 (HCL) | ✅ (Plan→Apply) |
| **[[198_ansible_os_configuration_management_ssh|Ansible]]** | 선언적 (YAML) | ✅ ([[272_state_pattern|state]] 기반) |
| **K8s manifest** | 선언적 (YAML) | ✅ (Reconciliation) |
| **쉘 스크립트** | 명령형 | ❌ (수동 체크 필요) |

- **📢 섹션 요약 비유**: 선언적 도구는 항온기(25도 유지)이고, 쉘 스크립트는 에어컨 리모컨(수동 ON/OFF, 상태 [[396_validation|확인]] 필요)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 명령형 | 선언적 |
|:---|:---|:---|
| **표현** | How (방법) | **What (목표)** |
| **[[171_idempotency_iac_terraform|멱등성]]** | 수동 구현 | **내장** |
| **반복 실행** | 위험 | **안전** |
| **[[119_gitops_single_source_of_truth|GitOps]]** | 불가 | **최적** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 멱등 설계 원칙
1. 리소스 존재 여부를 먼저 [[396_validation|확인]]한 후 [[087_process_state_transition|생성]]/수정.
2. `CREATE IF NOT EXISTS` 패턴 활용.
3. 쉘 스크립트 사용 시 `set -e` + 조건 체크로 방어.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 명령형 | 선언적+멱등 | 개선 |
|:---|:---|:---|:---|
| 반복 실행 | 위험 | **안전** | 자동화 신뢰 |
| 드리프트 | 방치 | **자동 복원** | 상태 보장 |
| [[119_gitops_single_source_of_truth|GitOps]] | 불가 | **최적** | 운영 [[194_consistency_database_integrity|일관성]] |

선언적+멱등은 **[[793_iac_idempotency_template|IaC]]·[[119_gitops_single_source_of_truth|GitOps]]·K8s 운영의 철학적 기반**이며, 이를 이해하지 않으면 현대 인프라 관리를 할 수 없다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[171_idempotency_iac_terraform|멱등성]]** | 같은 연산 반복 시 결과 동일 |
| **선언적 [[014_api_posix|API]]** | K8s의 핵심 운영 모델 |
| **[[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]** | 선언적 IaC의 대표 도구 |
| **Reconciliation** | 선언 상태로 자동 수렴 |
| **[[119_gitops_single_source_of_truth|GitOps]]** | 선언적+멱등 위에 구축 |

### 📈 관련 키워드 및 발전 흐름도

```text
[쉘 스크립트 (명령형, 비멱등, 2000s)]
    │
    ▼
[Puppet/Chef (2005~) — 선언적 구성 관리]
    │
    ▼
[Ansible (2012) — YAML 선언적, 에이전트리스]
    │
    ▼
[Terraform (2014) — 멀티클라우드 선언적 IaC]
    │
    ▼
[현재: K8s + GitOps — 선언적+멱등의 완전체]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 명령형은 "에어컨 켜, 25도로 맞춰"라고 **하나하나** 말하는 거예요.
2. 선언적은 "방 온도 25도"라고 **목표만 말하면** 항온기가 알아서 조절해요.
3. [[171_idempotency_iac_terraform|멱등성]]은 **같은 버튼을 몇 번 눌러도 항상 같은 결과**가 나오는 거예요!
