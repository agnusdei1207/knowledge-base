---
title: "Terraform·Pulumi (Terraform Pulumi)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 221
---

# 📖 【암기용】 개념 완전 이해

> 목적: Terraform·Pulumi를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Terraform과 Pulumi는 클라우드 인프라를 코드로 선언·배포·변경 통제하는 IaC 도구
- **왜 필요한가**: 콘솔 수동 작업은 환경 재현, 변경 승인, drift 탐지, 감사 추적을 어렵게 만든다
- **핵심 직관**: Terraform은 HCL 설계도, Pulumi는 TypeScript·Python 같은 범용 언어 설계도로 인프라를 만든다

## 깊이 이해
- **배경·문제의식**: 멀티 클라우드와 Kubernetes 환경은 VPC, IAM, DB, Secret, Helm chart가 함께 바뀐다. 사람이 순서를 기억해 배포하면 누락·권한 과다·환경 차이가 생긴다.
- **작동 원리**: Terraform은 Provider와 state를 기준으로 `plan` 차이를 계산한 뒤 `apply`한다. Pulumi는 범용 언어 런타임으로 리소스 그래프를 만들고 preview 후 update한다.
- **비유**: Terraform은 표준 양식 도면, Pulumi는 프로그래밍 언어로 쓰는 설계 프로그램에 가깝다.
- **구체 예시**: AWS VPC, EKS, RDS를 Terraform module로 만들면 PR에서 destroy 1건 여부를 검토한다. Pulumi는 TypeScript 함수로 dev/prod 리소스 수와 태그 정책을 재사용한다.
- **흔한 오해·주의점**: Pulumi가 프로그래밍 언어를 쓴다고 임의 절차 스크립트가 되는 것은 아니다. 두 도구 모두 목표 상태, state, provider, preview 검증이 핵심임.

## 연결 개념
- IaC - 목표 상태와 실제 상태 차이를 코드로 조정
- Policy as Code - OPA, Sentinel, Pulumi Policy Pack으로 배포 전 검증
- GitOps - Git PR을 인프라 변경 승인 기준으로 사용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 도구 문법 나열이 아니라 선언형 모델, state, preview, 정책 검증, 팀 역량에 따른 선택 기준을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Terraform·Pulumi는 인프라 목표 상태를 코드로 정의하고 provider API를 통해 생성·수정·삭제하는 IaC 도구이다.
> 2. **가치**: PR 승인, plan/preview, remote state, policy check로 변경 이력과 배포 위험을 통제한다.
> 3. **판단 포인트**: 표준 모듈과 운영 인력은 Terraform, 애플리케이션 코드 재사용과 동적 로직은 Pulumi를 우선 검토한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IaC 도구 선택 역량 확인 | HCL vs 범용 언어, provider, state, plan/preview | Terraform과 Pulumi를 단순 자동화 도구로 설명 |
| 운영 통제 설계 확인 | remote state, locking, policy-as-code, drift detection | state 파일 보안·동시 변경 충돌 누락 |
| 클라우드 표준화 판단 확인 | module/stack 재사용, PR 승인, tag/IAM 정책 | 문법 비교만 쓰고 조직 적용 기준 누락 |

> 요약: 이 문제는 도구 선호가 아니라 state 관리와 조직 역량에 맞춘 IaC 운영 모델을 묻는다.

---

## Ⅰ. 개요 및 필요성

Terraform·Pulumi는 인프라 목표 상태를 코드로 관리하는 IaC 도구이다. 클라우드 리소스가 20개 이상이거나 dev/stage/prod 3환경이면 수동 작업은 변경 누락과 감사 공백을 만든다. plan/preview, 승인, 정책 검증으로 배포 전 위험을 확인해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Git Repo -> IaC Code(HCL/Language) -> Provider SDK
-> Plan/Preview -> Policy Check -> Apply/Update
-> Remote State -> Cloud Resource -> Drift Scan
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Terraform HCL | 선언형 리소스 정의 | module registry, provider 생태계 |
| Pulumi Program | 범용 언어 기반 리소스 그래프 생성 | TypeScript, Python, Go, C# |
| State Backend | 코드와 실제 리소스 매핑 | S3 lock, Terraform Cloud, Pulumi Cloud |
| Policy Gate | 보안·비용·표준 검증 | Sentinel, OPA, Pulumi Policy Pack |

> 요약: 두 도구 모두 코드, provider, state, 검증 게이트가 있어야 운영 도구로 성립한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 -> Module/Stack 작성 -> Plan/Preview Diff
-> 정책 검사 -> 승인 -> Apply/Update
-> 상태 저장 -> 운영 검증 -> Drift 탐지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 리소스 코드 작성과 변수 입력 | naming/tag 준수율 100% |
| 2 | plan/preview로 변경 차이 계산 | delete 리소스 승인 필수 |
| 3 | 보안·비용 정책 검사 | public ingress 0건, cost 20% 증가 차단 |
| 4 | state lock 후 적용 | lock conflict 0건, apply log 보존 |

> 요약: Terraform·Pulumi는 배포 전 diff와 정책 검사를 통해 변경 위험을 사전에 식별한다.

---

## Ⅳ. 특징

| 구분 | Terraform | Pulumi | 판단 수치 |
|:---|:---|:---|:---|
| 언어 | HCL 선언형 | TypeScript·Python 등 범용 언어 | 팀 숙련자 3명 이상 기준 |
| 재사용 | module 중심 | class/function/package 중심 | 표준 컴포넌트 10개 이상 |
| 상태 | backend와 lock 필수 | stack state와 secret 관리 | state 암호화 100% |
| 위험 | HCL 표현 한계 | 코드 복잡도·리뷰 난도 | PR 리뷰 2인 승인 |

> 요약: Terraform은 표준화와 생태계, Pulumi는 언어 재사용과 추상화에서 선택 기준이 갈린다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Terraform·Pulumi | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 콘솔·Shell | 목표 상태 기반 리소스 그래프 | 리소스 20개 이상, 환경 2개 이상 |
| 비용/성능 | 작업 시간 누적 | module/stack 재사용 | 신규 환경 생성 30분 이하 목표 |
| 운영/위험 | 변경 이력 분산 | state·policy·drift 관리 | 감사로그 180일 이상 보존 |

> 요약: IaC 도구 선택은 배포 속도보다 변경 통제, state 복구, 정책 검증 체계로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| State 유실 | local state, 백업 부재 | remote backend, versioning, encryption | state backup 성공률 100% |
| 권한 과다 | provider 권한 범위 확대 | least privilege IAM, OIDC federation | admin 권한 사용 0건 |
| Drift 누적 | 콘솔 긴급 변경 | scheduled plan, drift alert | drift 미해결 0건 |

> 요약: 핵심 리스크는 state, 권한, drift이며 원격 상태와 정책 검사로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 통제 | plan/preview 첨부 PR 100% | CI audit |
| 보안 검증 | secret scan 100%, public CIDR 0건 | Checkov, OPA, trufflehog |
| 복구 능력 | state restore 30분 이하 | DR drill |

> 요약: 도입 효과는 PR 검증률, 정책 위반 건수, state 복구 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Terraform remote state는 S3 versioning+DynamoDB lock, Pulumi는 Pulumi Cloud 또는 self-managed backend로 암호화 적용
2. VPC, Kubernetes, DB, IAM을 표준 module/stack으로 분리하고 mandatory tag·least privilege IAM을 OPA/Policy Pack으로 검증
3. PR에 plan/preview 결과를 첨부하고 destroy, public ingress, 월 비용 20% 초과 변경은 2인 승인 적용

**결론 (2줄):**
- 기술사 판단: 인프라 표준화와 인력 수급은 Terraform, 애플리케이션 언어 추상화와 동적 구성은 Pulumi 선택
- 향후 방향: IaC는 GitOps, Policy as Code, FinOps, 공급망 서명 검증을 포함한 플랫폼 엔지니어링 체계로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Terraform과 Pulumi를 설명하시오" | provider, state, plan/preview 흐름 | HCL vs 범용 언어 비교 |
| 요구사항 명시형 | "IaC 도구 선택 기준을 제시하시오" | 조직 역량, state, 정책 검증 절차 | Terraform/Pulumi 선택 기준과 리스크 대응 |

> 요약: 설명형은 IaC 동작 원리, 선택형은 조직 역량·state·정책 검증 기준으로 목차를 전환한다.
