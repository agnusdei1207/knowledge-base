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
- **개요**: 서버, 네트워크, DB, 권한 같은 인프라를 코드로 선언하고 자동 생성·변경하는 방식
- **왜 필요한가**: 콘솔 클릭과 수동 설정은 재현성, 승인 이력, 변경 검토, drift 탐지가 어렵다
- **핵심 직관**: 인프라를 손으로 조립하지 않고 설계도와 시공 기록을 버전 관리하는 방식임

## 깊이 이해
- **배경·문제의식**: 클라우드는 리소스 수가 많고 변경 빈도가 일 10회 이상으로 늘 수 있다. 수동 생성은 누가 언제 무엇을 바꿨는지 추적하기 어렵고, 재해 복구 시 동일 환경을 재생성하기 어렵다.
- **작동 원리**: Terraform, CloudFormation, Pulumi, Ansible 등이 선언 파일을 읽고 현재 상태와 목표 상태 차이를 계산한 뒤 리소스를 생성·수정·삭제한다.
- **비유**: 건축 현장에서 도면, 자재 목록, 변경 승인서를 모두 Git에 두고, 시공 전 변경 차이를 검토하는 방식임
- **구체 예시**: VPC, Subnet, Security Group, EKS, RDS를 Terraform module로 작성하고 PR 승인 후 `plan` 결과를 검토해 `apply`한다.
- **흔한 오해·주의점**: IaC는 자동화 스크립트와 다르다. 목표 상태, state 관리, drift 탐지, 정책 검증이 함께 있어야 한다.

## 연결 개념
- GitOps - Git을 운영 상태의 단일 기준으로 사용
- Policy as Code - OPA, Sentinel로 배포 정책 검증
- Immutable Infrastructure - 코드와 이미지로 새 인프라 교체

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
