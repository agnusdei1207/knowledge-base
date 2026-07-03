---
title: "IaC 인프라스트럭처 코드 (Infrastructure as Code)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 220
---

# 📖 【암기용】 개념 완전 이해

> 목적: IaC를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: IaC(Infrastructure as Code)는 서버·네트워크·DB·권한 같은 인프라 리소스를 **선언형 코드**로 정의하고, 그 코드를 실행해 실제 인프라를 자동으로 생성·변경·삭제하는 **인프라 자동화** 방식이다.
- **왜 필요한가**: 콘솔에서 클릭으로 리소스를 만들면 "누가 언제 무엇을 왜 바꿨는지"가 기록에 남지 않아, 재현·감사·재해 복구가 어렵다.
- **핵심 직관**: "무엇을 어떻게 만들지"를 절차로 적는 게 아니라 "최종적으로 무엇이 존재해야 하는지"만 코드로 선언하면, 도구가 현재 상태와의 차이를 계산해 알아서 맞춰준다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 인프라 자동화 | 이 개념이 속한 상위 범주 — 사람 손을 거치지 않고 인프라를 다루는 것 전반 | 공장 자동화 |
| 선언형(Declarative) | "최종 결과가 어떤 모습이어야 하는지"만 기술 — 도구가 방법을 알아서 찾음 | "3층 건물을 원한다"고만 말함 |
| 명령형(Imperative) | "어떤 순서로 무엇을 실행할지" 절차를 하나하나 기술 | "벽돌을 여기 놓고, 다음에 저기 놓고..."를 직접 지시 |
| State(상태 파일) | 코드가 만든 리소스와 실제 클라우드 리소스를 매핑해 기록한 파일 | 시공 결과를 적어둔 준공 대장 |
| Plan / Diff | 코드(목표 상태)와 State(현재 상태)를 비교해 "무엇이 추가·변경·삭제될지" 미리 계산 | 공사 전에 뽑아보는 변경 견적서 |
| Apply | Plan에서 계산된 차이를 실제로 클라우드에 실행 | 견적대로 실제 시공 |
| Idempotency(멱등성) | 같은 코드를 몇 번 실행해도 결과가 항상 동일함(이미 존재하면 다시 안 만듦) | 이미 켜진 전등 스위치를 다시 눌러도 상태는 그대로 |
| Drift(구성 편류) | 코드 밖에서(콘솔로) 리소스를 직접 바꿔서 실제 상태와 코드가 어긋나는 현상 | 도면과 다르게 현장에서 임의로 고친 부분 |
| Module | 리소스 묶음을 재사용 가능한 부품으로 만든 것 | 표준화된 조립식 부품 세트 |
| Policy as Code | 보안·비용·명명 규칙 같은 조직 정책을 코드로 검증(OPA, Sentinel) | 시공 전 건축 법규 자동 검사 |

## 깊이 이해

### 왜 필요했나 — 리소스가 늘어날수록 수동 관리가 무너지는 이유
- 스타트업 초기에는 VPC 1개, EC2 5대 정도라 콘솔 클릭으로도 관리된다. 하지만 서비스가 커지면 VPC, Subnet, Security Group, IAM Role, RDS, EKS 등 리소스가 수백 개로 늘고, dev/stage/prod 3개 환경이 각각 존재하며, 하루에도 수십 번 변경이 발생한다. 이 시점에서 "누가 어제 이 Security Group의 인바운드 규칙을 왜 열었는지" 콘솔만으로는 알 수 없다. IaC는 모든 변경을 코드 커밋(Git)으로 남겨 "무엇을, 왜, 누가" 바꿨는지 추적 가능하게 만든다.

### 선언형 vs 명령형 — 같은 목표, 다른 접근
- 명령형으로 "VPC 하나와 서브넷 2개를 만들어라"를 적으면, 이미 VPC가 있는지 먼저 확인하고, 없으면 생성 API를 호출하고, 서브넷도 하나씩 존재 여부를 확인하며 만들어야 한다 — 스크립트가 "어떻게(how)"를 전부 책임진다.
- 선언형으로는 "VPC 1개, 서브넷 2개가 존재해야 한다"라고만 코드에 적는다. 도구(Terraform 등)가 현재 State를 조회해 "VPC는 이미 있고 서브넷은 1개만 있다"를 파악하면, 서브넷 1개만 추가로 생성하는 최소한의 작업을 스스로 계산한다. 사람은 "무엇(what)"만 정의하면 된다.

### Plan/Apply — 변경 전에 미리 눈으로 확인하는 안전장치(수치 예)
- 코드를 수정하고 `plan`을 실행하면 도구는 State(현재 상태)와 코드(목표 상태)를 비교해 예를 들어 "리소스 3개 추가, 1개 변경, 0개 삭제"라는 diff를 보여준다. 이 단계에서 "Security Group 인바운드에 0.0.0.0/0이 새로 추가된다"처럼 위험한 변경을 사람이 apply 전에 발견할 수 있다. 실제로 `apply`를 눌러야만 클라우드에 반영되므로, "잘못된 diff를 보고 멈춘다"가 항상 가능하다.

### Idempotency(멱등성)가 없으면 생기는 문제
- 만약 "EC2 인스턴스를 생성하라"는 명령형 스크립트를 실수로 두 번 실행하면 인스턴스가 2개 만들어져 버릴 수 있다. 선언형 IaC는 "인스턴스 1개가 존재해야 한다"만 보장하므로, 스크립트를 10번 실행해도 결과는 항상 인스턴스 1개다 — 이 성질이 idempotency다. CI 파이프라인에서 배포 스크립트가 재시도되어도 안전한 이유가 이것이다.

### Drift(구성 편류) 탐지 — 코드와 현실이 어긋나는 순간(수치 예)
- 장애 대응 중 담당자가 콘솔에서 급하게 Security Group에 포트 하나를 임시로 열었다고 하자. 이 변경은 Git 코드에는 반영되지 않았으므로, 다음에 `plan`을 돌리면 도구는 "코드에는 없는데 실제로는 존재하는 규칙 1건"을 drift로 검출한다. 이를 방치하면 다음 `apply` 때 그 임시 규칙이 예고 없이 삭제되거나, 반대로 위험한 설정이 영구히 남을 수 있다. 그래서 주기적으로 `plan`을 돌려 drift 0건을 유지하는 것이 운영 원칙이다.

### 비유와 흔한 오해
- **비유**: 건축 현장에서 도면, 자재 목록, 변경 승인서를 모두 Git에 두고, 실제 시공(apply) 전에 변경분을 도면상에서 미리 검토(plan)하는 것과 같다.
- **오해**: "IaC는 그냥 자동화 스크립트다"가 아니다. bash 스크립트로 리소스를 자동 생성하는 것은 명령형 자동화일 뿐이며, State 관리·목표 상태 비교·drift 탐지·정책 검증이 함께 있어야 IaC라 부를 수 있다.

## 연결 개념
- Terraform·Pulumi — IaC 원리를 구현하는 대표적 도구(221에서 도구별 차이를 상세히 다룸)
- Immutable Infrastructure — IaC가 만든 새 인스턴스로 기존 인스턴스를 교체하는 배포 원칙(219)
- Ansible·Chef·Puppet — IaC가 리소스를 "만든다"면, 이들은 만들어진 서버 "내부" 설정을 코드로 관리(222)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: IaC는 도구명이 아니라 선언형 모델, state, plan/apply, 정책 검증, drift 관리 체계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IaC는 인프라 리소스를 코드로 선언하고 목표 상태와 실제 상태 차이를 자동 조정하는 운영 방식이다.
> 2. **가치**: 재현성, 변경 승인, 감사 추적, 재해 복구 시간을 코드와 pipeline으로 통제한다.
> 3. **판단 포인트**: state 관리, module 표준화, secret 분리, policy-as-code, drift detection이 핵심 설계 요소이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 자동화 이해 확인 | 선언형, state, plan/apply, module | 단순 shell 자동화로 설명 |
| 운영 거버넌스 판단 확인 | PR 승인, policy-as-code, drift 탐지 | 보안그룹·IAM 검증 누락 |
| 장애·복구 설계 확인 | remote state, locking, backup, rollback | state 파일 유실과 secret 노출 누락 |

> 요약: IaC 답안은 리소스 생성 자동화보다 변경 통제와 목표 상태 관리에 초점을 둬야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 인프라 코드 관리 방식
- 배경: 수동 콘솔 작업은 재현성, 감사성, 복구 시간을 악화시킨다.
- 필요성: 선언형 코드, state, pipeline, 정책 검증으로 인프라 변경을 관리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Git Repository -> IaC Module -> CI Plan
-> Policy Check -> Approval -> Apply
-> Remote State/Lock -> Cloud Resources -> Drift Detection
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| IaC Code/Module | VPC, IAM, DB 등 리소스 선언 | Terraform module, CloudFormation stack |
| State Backend | 실제 리소스와 코드 매핑 | S3+DynamoDB lock, Terraform Cloud |
| Plan/Apply Pipeline | 변경 영향 검토와 적용 | PR 기반 승인, change set |
| Policy as Code | 보안·비용·표준 검증 | OPA, Sentinel, Checkov |

> 요약: IaC 구조는 코드, state, pipeline, 정책 검증, drift 탐지로 완성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Change Request -> Code Commit -> Plan Diff
-> Security/Cost Policy Check -> Review Approval
-> Apply with State Lock -> Verify Resource -> Drift Scan
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 모듈 작성과 변수 입력 | naming/tag 표준 100% |
| 2 | plan으로 변경 차이 확인 | destroy 리소스 승인 필수 |
| 3 | policy와 secret 검사 | public ingress 0.0.0.0/0 차단 |
| 4 | apply 후 drift 점검 | drift 0건, state lock 사용 |

> 요약: IaC는 plan 단계에서 변경 위험을 검토하고 state lock으로 동시 변경 충돌을 막는다.

---

## Ⅳ. 특징

| 구분 | 수동 인프라 운영 | IaC | 판단 수치 |
|:---|:---|:---|:---|
| 변경 방식 | 콘솔 클릭·개별 작업 | Git PR과 plan/apply | 승인 없는 변경 0건 |
| 재현성 | 작업자 숙련도 의존 | module 재사용 | DR 환경 생성 1시간 이하 |
| 감사성 | 변경 이력 분산 | commit, plan, apply log | traceability 100% |
| 위험 | drift·secret 노출 | state·정책 관리 필요 | drift 0건, secret scan 100% |

> 요약: IaC는 인프라 변경을 코드 리뷰와 자동 검증 대상으로 전환한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Infrastructure as Code | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 콘솔 수동 생성 | 선언형 코드와 state | 리소스 20개 이상 또는 환경 2개 이상 |
| 비용/성능 | 작업 시간 누적 | module 재사용과 pipeline | 신규 환경 생성 30분 이하 목표 |
| 운영/위험 | 변경 추적 누락 | state 유실·drift·권한 오남용 | remote backend와 policy 필수 |

> 요약: 환경 수와 리소스 수가 늘수록 IaC 없이 변경 통제와 복구 시간을 맞추기 어렵다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| State 손상 | local state, 동시 apply | remote state, locking, versioning | state lock conflict 0건 |
| Secret 노출 | 변수·output 평문 저장 | secret manager, sensitive flag, scan | secret leak 0건 |
| 위험 변경 | destroy, public ingress | policy-as-code, manual approval | blocked policy count |

> 요약: IaC 리스크는 state, secret, 위험 변경이며 원격 상태·비밀관리·정책 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 통제 | PR 승인 100%, plan 첨부 100% | CI/CD audit |
| 표준 준수 | tag/naming/IAM policy 위반 0건 | Checkov, OPA |
| 복구 능력 | DR 환경 생성 1시간 이하 | restore drill |

> 요약: IaC 성숙도는 변경 승인률, 표준 위반, 재해 복구 시간을 기준으로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Terraform remote state를 S3 versioning+DynamoDB lock으로 구성하고 환경별 workspace 또는 계정 분리 적용
2. module registry로 VPC, EKS, RDS, IAM 표준 모듈을 제공하고 mandatory tag, least privilege IAM을 OPA/Checkov로 검증
3. PR에 plan 결과를 첨부하고 destroy·public ingress·cost 20% 증가 변경은 수동 승인 게이트를 요구

**결론 (2줄):**
- 기술사 판단: 클라우드 리소스 20개 이상 또는 dev/stage/prod 3환경이면 IaC를 표준으로 적용하고 state 관리부터 설계
- 향후 방향: GitOps, Policy as Code, FinOps 태깅, 공급망 보안 검증이 결합된 플랫폼 엔지니어링 체계로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "IaC를 설명하시오" | plan/apply/state/drift 흐름 | 수동 운영 대비 특징 |
| 요구사항 명시형 | "클라우드 운영 자동화 방안을 제시하시오" | PR, policy, state lock, drift 설계 | 위험 변경·secret·DR 지표 |

> 요약: 설명형은 목표 상태 관리 원리, 방안형은 거버넌스와 복구 지표 중심으로 전환한다.
