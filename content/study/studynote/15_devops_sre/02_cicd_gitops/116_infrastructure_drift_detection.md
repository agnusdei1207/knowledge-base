---
title: 116. 인프라 드리프트 감지 (Infrastructure Drift Detection) - IaC 상태 불일치 자동 탐지
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인프라 드리프트(Drift)란 **[[793_iac_idempotency_template|IaC]] 코드([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]/CloudFormation)에 정의된 기대 상태와 실제 클라우드 인프라 상태가 불일치**하는 현상이며, Drift Detection은 이를 자동으로 탐지·알림·복원하는 프로세스다.
> 2. **가치**: 운영자가 콘솔에서 수동 변경(보안 그룹 열기, 인스턴스 타입 변경)하면 [[793_iac_idempotency_template|IaC]] 코드와 실제가 달라져 **"코드가 진실이 아니게"** 되며, 이후 `terraform apply` 시 예기치 않은 변경이 발생한다.
> 3. **판단 포인트**: `terraform plan`을 주기적으로 실행하여 Diff를 감지하거나, **Driftctl·AWS CloudFormation Drift [[961_deepfake_detection|Detection]]·Spacelift**로 자동화한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    드리프트 발생 시나리오                              │
├───────────────────────────────────────────────────────┤
│  1. Terraform: security_group = [22, 443]            │
│  2. 운영자: AWS 콘솔에서 8080 포트 수동 추가 ⚠️      │
│  3. 실제 상태: [22, 443, 8080]                        │
│     Terraform 코드: [22, 443]                         │
│     → 드리프트 발생!                                  │
│  4. terraform apply 실행 시:                          │
│     8080이 코드에 없으므로 삭제됨 → 서비스 장애!     │
│                                                       │
│  해결: 주기적 terraform plan으로 Diff 감지            │
│     → 코드 동기화 또는 수동 변경 되돌리기             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 드리프트는 건축 대장([[793_iac_idempotency_template|IaC]])과 실제 건물(인프라)이 다른 상태다. 건축 대장대로 리모델링하면 몰래 만든 방이 철거된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 드리프트 감지 도구

| 도구 | 방식 | 특징 |
|:---|:---|:---|
| **[[195_terraform_hashicorp_agnostic_aws_gcp|terraform]] plan** | [[272_state_pattern|State]] vs 실제 비교 | 기본, 수동/크론 실행 |
| **Driftctl** | [[793_iac_idempotency_template|IaC]] 미관리 리소스 탐지 | [[191_oss_license_compliance|OSS]], 커버리지 높음 |
| **CloudFormation Drift** | CF [[057_stack|스택]] vs 실제 비교 | AWS 네이티브 |
| **Spacelift** | 자동 드리프트 스캔 + 알림 | [[309_saas|SaaS]] |

### 드리프트 대응 [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 설명 |
|:---|:---|
| **Reconcile** | [[793_iac_idempotency_template|IaC]] 코드를 실제 상태에 맞춰 수정 (코드 [[212_synchronization_mechanisms|동기화]]) |
| **Remediate** | 실제 상태를 [[793_iac_idempotency_template|IaC]] 코드에 맞춰 복원 (자동 적용) |
| **Alert** | 드리프트 감지 시 알림만 (수동 판단) |

- **📢 섹션 요약 비유**: Reconcile은 "몰래 만든 방을 대장에 추가"하는 것이고, Remediate는 "몰래 만든 방을 철거"하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 드리프트 미감지 | 주기적 Plan | 자동 감지+복원 |
|:---|:---|:---|:---|
| **코드 신뢰** | ✗ | 수동 [[396_validation|확인]] | **100%** |
| **사고 위험** | 높음 | 중간 | **낮음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 자동화 [[123_pipe|파이프]]라인
```yaml
# GitHub Actions: 매일 드리프트 스캔
schedule:
  - cron: '0 9 * * *'
steps:
  - run: terraform plan -detailed-exitcode
  # exit code 2 = drift detected → Slack 알림
```

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **콘솔 수동 변경 허용**: [[793_iac_idempotency_template|IaC]] [[119_gitops_single_source_of_truth|GitOps]] 원칙 파괴. 콘솔 변경 시 반드시 [[793_iac_idempotency_template|IaC]] 코드에 반영.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 드리프트 미감지 | 드리프트 감지 | 개선 |
|:---|:---|:---|:---|
| [[793_iac_idempotency_template|IaC]] 코드 [[085_confidence_association_rule_conditional_probability|신뢰도]] | 불확실 | **100%** | 단일 진실 원천 |
| 예기치 않은 변경 | 빈번 | **즉시 감지** | 사고 예방 |

드리프트 감지는 [[793_iac_idempotency_template|IaC]] GitOps의 **필수 보완 장치**이며, [[237_opa_open_policy_agent_gatekeeper|OPA]]([[237_opa_open_policy_agent_gatekeeper|Open Policy Agent]])와 결합하여 드리프트 유형별 자동 [[164_policy|정책]](허용/거부/알림)을 적용하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[793_iac_idempotency_template|IaC]] ([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]])** | 드리프트가 발생하는 [[793_iac_idempotency_template|인프라 코드]] |
| **[[119_gitops_single_source_of_truth|GitOps]]** | 코드 = 진실이라는 원칙, 드리프트가 위반하는 대상 |
| **Driftctl** | [[191_oss_license_compliance|OSS]] 드리프트 감지 도구 |
| **[[195_terraform_hashicorp_agnostic_aws_gcp|terraform]] plan** | 기본적인 드리프트 감지 명령 |
| **[[237_opa_open_policy_agent_gatekeeper|OPA]]** | 드리프트 대응 [[164_policy|정책]] 자동화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 인프라 관리 (콘솔 변경 빈번)]
    │
    ▼
[IaC 도입 (2014~) — 코드로 인프라 관리]
    │
    ▼
[드리프트 문제 인식 (2018~) — 코드 vs 실제 불일치]
    │
    ▼
[Driftctl / CF Drift Detection (2020~) — 자동 감지]
    │
    ▼
[현재: 자동 Remediation — 드리프트 감지→자동 복원]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 설계도([[793_iac_idempotency_template|IaC]])에는 **방 3개**라고 써있는데, 누군가 몰래 **방 1개를 더 만들었어요** (드리프트).
2. 나중에 설계도대로 리모델링하면 **몰래 만든 방이 없어져서** 사고가 나요.
3. 드리프트 감지는 매일 설계도와 실제 건물을 **비교해서 다른 점을 찾아주는** 검사원이에요!
