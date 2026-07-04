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
- **개요**: Terraform과 Pulumi는 IaC(220 참조 — 선언형 코드로 목표 상태를 정의하고 실제 상태와의 차이를 계산해 적용하는 방식)를 구현하는 대표적 **IaC 도구**로, Terraform은 HCL이라는 전용 선언형 언어를, Pulumi는 TypeScript·Python 같은 **범용 프로그래밍 언어**를 사용한다는 점이 가장 큰 차이다.
- **왜 필요한가**: 여러 클라우드(AWS/GCP/Azure)와 SaaS(Datadog, GitHub 등) API를 각각 따로 다루면 리소스 생성 방식이 제각각이라, 하나의 공통된 도구·문법으로 다루는 추상화 계층이 필요하다.
- **핵심 직관**: Terraform은 정해진 양식(HCL)에 값만 채우는 표준 설계도이고, Pulumi는 프로그래밍 언어로 직접 짜는 설계 프로그램이다 — 둘 다 "목표 상태"를 만들어 도구에 넘긴다는 점은 같다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Provider | 특정 클라우드/서비스의 API를 호출하도록 만든 플러그인(AWS Provider, GCP Provider 등) | 특정 브랜드 전용 어댑터 |
| HCL(HashiCorp Configuration Language) | Terraform 전용의 선언형 설정 언어 | 정해진 서식의 신청서 |
| 범용 프로그래밍 언어 | Pulumi가 쓰는 TypeScript·Python·Go·C# 등 — 반복문·함수·클래스 사용 가능 | 자유 양식 기획서 |
| State Backend | State 파일을 저장하는 위치(S3, Terraform Cloud, Pulumi Cloud 등) | 준공 대장을 보관하는 서고 |
| State Lock | 동시에 두 사람이 apply하지 못하게 잠그는 장치(DynamoDB lock 등) | 회의실 예약 시스템의 중복 예약 방지 |
| Plan(Terraform) / Preview(Pulumi) | apply/update 전에 변경 diff를 미리 계산해 보여주는 단계 | 시공 전 견적서 확인 |
| Resource Graph | 리소스 간 의존관계(A가 있어야 B를 만들 수 있음)를 표현한 그래프 | 선행 공정을 표시한 공정표 |
| Module(Terraform) / Stack(Pulumi) | 리소스 묶음을 재사용 단위로 캡슐화한 것 | 표준 조립 부품 세트 |
| Policy Pack / Sentinel / OPA | apply 전 보안·비용·명명 규칙을 코드로 강제 검증하는 정책 엔진 | 시공 전 건축 법규 자동 심사 |

## 깊이 이해

### Provider — 클라우드 API를 다루는 공통 창구
- Terraform이든 Pulumi든, 실제로 AWS나 GCP에 리소스를 만드는 것은 도구 자체가 아니라 **Provider**라는 플러그인이다. 예를 들어 "AWS에 VPC를 만들어라"라는 코드를 실행하면, AWS Provider가 내부적으로 AWS SDK/API를 호출해 실제 VPC 생성 요청을 보낸다. 그래서 GCP 리소스를 다루려면 GCP Provider를 추가하면 되고, 코드의 나머지 구조(선언·plan·apply)는 동일하게 유지된다 — 이것이 "멀티 클라우드를 하나의 도구로 다룬다"는 말의 실체다.

### HCL vs 범용 언어 — 실제로 무엇이 다른가(코드로 이해)
- Terraform(HCL)은 아래처럼 "리소스 종류와 속성값"을 고정된 블록 문법으로 채운다.
  ```hcl
  resource "aws_instance" "web" {
    count         = 3
    instance_type = "t3.micro"
  }
  ```
  3대를 만들려면 `count = 3`처럼 Terraform이 제공하는 반복 문법(`count`, `for_each`)을 써야 하고, 복잡한 조건 분기는 표현력이 제한적이다.
- Pulumi(TypeScript)는 프로그래밍 언어의 반복문·조건문·함수를 그대로 쓴다.
  ```typescript
  for (const env of ["dev", "staging", "prod"]) {
    new aws.ec2.Instance(`web-${env}`, { instanceType: "t3.micro" });
  }
  ```
  환경마다 다른 개수·설정을 만들 때 일반 for문, 함수 재사용, 외부 npm 패키지 활용까지 가능해 표현력이 크다. 대신 "언어를 잘못 쓰면 선언형의 예측 가능성이 깨질 위험"(예: 실행마다 다른 무작위 값 생성)도 함께 커진다.

### State Lock — 동시 apply 충돌을 막는 장치(수치 예)
- 담당자 A와 B가 동시에 같은 환경에 `apply`를 실행하면 State 파일에 서로 다른 변경이 동시에 쓰여 파일이 깨질 수 있다. 그래서 실무에서는 S3(state 저장) + DynamoDB(lock 테이블) 조합을 쓴다. A가 apply를 시작하면 DynamoDB에 lock 레코드가 생성되고, B가 동시에 apply를 시도하면 "이미 lock 되어 있음" 오류를 받고 대기하거나 취소된다. Pulumi는 Pulumi Cloud 또는 자체 backend가 같은 역할의 lock을 제공한다.

### Plan/Preview 결과를 읽는 법(수치 예)
- `terraform plan` 실행 결과가 `Plan: 2 to add, 1 to change, 1 to destroy`로 나왔다면, 이 중 "1 to destroy"가 프로덕션 DB 인스턴스라면 즉시 apply를 멈추고 코드를 재검토해야 한다. PR 리뷰 단계에서 이 diff를 첨부해 리뷰어가 destroy 항목을 반드시 확인하게 하는 것이 실무 표준이다. Pulumi의 `pulumi preview`도 동일하게 add/change/delete 개수를 보여준다.

### 비유와 흔한 오해
- **비유**: Terraform은 관공서 표준 양식(HCL)에 정해진 칸을 채우는 것이고, Pulumi는 워드 프로세서로 자유롭게 문서를 작성하는 것과 같다 — 둘 다 최종적으로는 같은 형식의 "신청 결과"(리소스 그래프)를 만들어 제출(apply/update)한다.
- **오해**: "Pulumi는 범용 언어니까 임의 순서로 아무 작업이나 실행하는 절차형 스크립트가 된다"는 오해가 흔하다. 실제로는 Pulumi도 내부적으로 선언한 리소스들을 그래프로 만들어 State와 비교한 뒤 diff만 적용한다 — 언어만 다를 뿐 "목표 상태 선언 + diff 적용"이라는 IaC의 본질은 Terraform과 동일하다.

## 연결 개념
- IaC(220) — 이 둘이 공통으로 구현하는 상위 원리(선언형·State·Plan/Apply)
- Policy as Code — OPA, Sentinel, Pulumi Policy Pack으로 apply/update 전 정책 위반을 차단
- Ansible·Chef·Puppet(222) — Terraform·Pulumi가 인프라를 "만든다"면, 이들은 만들어진 서버 "내부" 설정을 관리 — 역할이 다름

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

- 개요: 목표 상태 기반 IaC 도구
- 배경: 클라우드 리소스가 20개 이상이거나 dev/stage/prod 3환경이면 수동 작업은 변경 누락과 감사 공백을 만든다.
- 필요성: plan/preview, 승인, 정책 검증으로 배포 전 변경 위험을 확인해야 한다.

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

| 구분 | 기존/대안 | Terraform·Pulumi | 선택 기준 |
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
