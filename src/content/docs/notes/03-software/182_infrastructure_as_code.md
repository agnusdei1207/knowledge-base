---
sidebar:
  order: 182
  label: "182. IaC 인프라스트럭처 코드 (Infrastructure as Code)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "IaC 인프라스트럭처 코드 (Infrastructure as Code)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 182
extra:
  question_no: "182"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "상태•계획•편차 통제의 자동화 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **IaC (Infrastructure as Code)**: 서버, DB 등 클라우드 인프라를 수동 조작이 아닌 기계가 읽을 수 있는 선언적 코드(Declarative Code)로 정의·배포하는 자동화 관행.
- **Terraform (테라폼)**: HashiCorp가 개발한 오픈소스 IaC 도구. HCL(HashiCorp Configuration Language)을 사용하여 인프라를 구축하는 업계 표준 플랫폼.
- **Idempotency (멱등성)**: 코드를 수회 실행해도 최종 인프라 상태(End-State)는 항상 동일하게 유지되어야 한다는 선언형 IaC 핵심 철학.

</details>

- 정의: 인프라 구성 요소를 코드로 정의하여 버전 관리(Git), 테스트, CI/CD 등 엔지니어링 생태계를 인프라로 확장한 코드형 인프라(IaC).
- 배경: 수동 관리(Click-Ops)로 인한 휴먼 에러, 환경 불일치, 복제 불가능성 극복.

#### 한줄 요약

- **IaC(Infrastructure as Code)**: 서버, 데이터베이스 등 클라우드 인프라를 수동 조작 대신 기계가 읽을 수 있는 선언적 코드(Declarative Code)로 정의·배포하는 자동화 관행.
- **테라폼(Terraform)**: HashiCorp가 개발한 HCL(HashiCorp Configuration Language) 기반 오픈소스 IaC 도구로, 인프라 구축의 업계 표준 플랫폼.
- **멱등성(Idempotency)**: 반복 실행해도 최종 인프라 상태(End-State)가 동일하게 유지되어야 하는 선언형 IaC의 핵심 철학.

</details>

- 정의: 인프라 구성 요소를 코드로 정의하고 버전 관리(Git), 테스트, CI/CD 등 엔지니어링 생태계를 인프라 영역으로 확장한 자동화 기술.
- 배경: 수동 관리(Click-Ops) 방식의 휴먼 에러, 환경 불일치, 복제 불가능성 등의 한계 극복.

#### 한줄 요약

- 서버 설치 설명서를 실행 코드로 변환하여 변경 전 계획 검토 및 환경 재현을 지원하는 인프라 관리 기술.

## Ⅱ. 특징 (IaC 3대 핵심 성질)

<details><summary>핵심 용어</summary>

- **불변 인프라(Immutable Infrastructure)**: 기존 서버 수정(Update) 대신 신규 서버 이미지(AMI, Docker)로 대체(Replace)하여 환경 일관성을 보장하는 클라우드 네이티브 철학.
- **선언형 접근(Declarative Approach)**: 절차적 스크립트가 아닌 최종 필요한 상태(What)만 선언 시 엔진이 생성 및 변경을 수행하는 방식.
- **버전 관리 및 감사(Version Control & Auditing)**: 변경 사항을 Git 등으로 관리하여 이력 추적 및 롤백을 지원하는 체계.
- **편차 탐지(Drift Detection)**: 선언적 목표 상태와 실제 인프라 상태 간의 불일치를 자동 식별하여 동기화를 유도하는 기능.

</details>

#### 한줄 요약

- 코드만 저장하는 것이 아니라 실제 자원과 연결한 상태 장부를 함께 관리해야 수동 변경과 삭제 영향을 계획에서 찾을 수 있다.

## Ⅲ. 구조 및 구성요소 (Terraform 기반 IaC 아키텍처)

<details><summary>핵심 용어</summary>

- **상태 파일(State File)**: Terraform이 실제 클라우드 인프라에 생성한 리소스 정보를 매핑한 JSON 형식의 장부(`.tfstate`). 선언된 코드와 실제 환경을 비교하는 핵심 기준점.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   테라폼 기반 IaC 실행 아키텍처                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. [개발자 코드] (main.tf)                                             │
│         │                                                              │
│         ▼                                                              │
│ 2. [테라폼 코어 엔진] ◄──(비교)── 3. [상태 파일 (.tfstate)]          │
│         │ (계획 및 적용)                      (S3 / Terraform Cloud)   │
│         ▼                                                              │
│ 4. [프로바이더 플러그인] (AWS, GCP, K8s API 변역기)                  │
│         │                                                              │
│         ▼ (API 호출)                                                   │
│ 5. [실제 클라우드 인프라] (EC2, VPC, RDS 등)                         │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 개발자가 작성한 HCL 코드를 엔진이 읽고, 과거에 만들어 둔 상태 파일(.tfstate)과 대조하여 어떤 리소스를 추가/삭제할지 결정(Plan)한 후 프로바이더를 통해 클라우드에 적용(Apply)하는 구조.

| 핵심 구성요소 | 기능 및 책임 | 실무 적용 |
|:---|:---|:---|
| **Configuration Code** | **인프라의 최종 형상을 정의한 소스코드** | `.tf` 파일 (VPC, 서브넷 선언) |
| **Terraform Core** | **코드 파싱, 의존성 트리 생성 및 State 비교 엔진**| `terraform plan/apply` 실행 |
| **State Backend** | **팀 협업 시 `.tfstate` 파일을 안전하게 원격 저장**| AWS S3 + DynamoDB (Lock) |
| **Provider** | **클라우드 벤더의 API와 통신하는 어댑터 플러그인**| AWS Provider, GitHub Provider |

#### 한줄 요약

- 저장소가 설계도, 파이프라인이 검사소, 엔진이 시공자, 원격 상태가 실제 건물과 설계도를 연결하는 장부 역할을 한다.

## Ⅳ. 흐름도 (IaC 워크플로우 및 상태 동기화 흐름)

<details><summary>핵심 용어</summary>

- **Terraform Plan (계획)**: 실제 인프라를 변경하기 직전에, 코드를 바탕으로 어떤 리소스가 생성(+), 변경(~), 삭제(-)될지 시뮬레이션 결과를 미리 보여주는 치명적 실수 방어 명령어.

</details>

```text
[Developer]                         [Terraform]                        [Cloud]
     │                                   │                                │
     ├─ 1. Write Code (VPC 추가) ───────►│                                │
     │                                   │                                │
     ├─ 2. `terraform init` ────────────►│ (Provider 다운로드)            │
     │                                   │                                │
     ├─ 3. `terraform plan` ────────────►│◄──(Read State & Actual Info)───┤
     │                                   │                                │
     │◄── 4. Print Plan (+1 Add) ────────┤ (생성/변경 내역 시뮬레이션)    │
     │                                   │                                │
     ├─ 5. `terraform apply` ───────────►│ (API 호출)                     │
     │                                   ├───────────────────────────────►│
     │                                   │                                │
     │◄── 6. Apply Complete ─────────────┤◄──(Update State File)──────────┤
```

### 동작 원리

1. **Init**: 프로젝트 초기화 및 Provider 플러그인 다운로드.
2. **Plan**: 코드, State, 실제 상태를 대조(Diff)하여 변경 시나리오 도출 및 승인 대기.
3. **Apply**: 시나리오에 따라 클라우드 API 호출(CRUD) 후 State 파일 업데이트.

#### 한줄 요약

- 검토한 Plan과 같은 변경만 적용하고 실행 동안 상태를 잠가 두 사람이 같은 자원을 동시에 만들거나 덮어쓰지 않게 한다.

## Ⅴ. 종류 및 비교 (IaC 도구 패러다임 1:1 비교)

<details><summary>핵심 용어</summary>

- **구성 관리 도구(Configuration Management)**: 인프라 프로비저닝 후 이미 실행 중인 OS 내부에 접속하여 패키지 설치 및 환경 설정 파일(conf)을 제어하는 데 특화된 Ansible, Chef 등 도구.

</details>

| 비교 항목 | 프로비저닝 도구 (Terraform) | 구성 관리 도구 (Ansible) |
|:---|:---|:---|
| **핵심 목적** | **인프라 자체(VPC, DB, EC2)의 생성과 소멸** | **OS 내부의 S/W 설치 및 환경 설정**|
| **접근 방식** | **선언형 (Declarative) - 상태 파일로 관리** | **절차형 (Procedural) - 순차적 스크립트 실행**|
| **상태 관리** | **State 파일(.tfstate) 필수 존재** | State 파일 없음 (실행할 때마다 멱등성 체크) |
| **운영 철학** | **불변 인프라 (업데이트 시 기존 자원 폐기 및 신규 생성)**| 가변 인프라 (기존 서버에 접속하여 덮어쓰기) |

#### 한줄 요약

- 선언형은 완성 모습을 적어 엔진이 차이를 맞추고 명령형은 만드는 순서를 직접 적어 각 단계의 재실행 안전성까지 작성자가 책임진다.

## Ⅵ. 실무 고려사항 및 대책 (IaC 3대 실무 장애 요인 대책)

<details><summary>핵심 용어</summary>

- **Configuration Drift (구성 편차)**: 테라폼 코드로 관리되는 인프라를 누군가가 AWS 콘솔(GUI)에 몰래 접속해서 수동으로 바꿔버려, 코드(Git)와 실제 클라우드의 상태가 심각하게 어긋나는 현상.

</details>

| 3대 IaC 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Configuration Drift** | 관리자의 무단 AWS 콘솔 수동 조작 | **Drift Detection 파이프라인 알람 및 IAM 콘솔 쓰기 권한 압수**|
| **2. State 파일 동시 수정**| 두 팀원이 동시에 Apply 명령어 실행 | **S3 Backend와 DynamoDB를 연동한 State Lock(잠금) 적용**|
| **3. 민감 정보 하드코딩** | DB 패스워드를 `.tf` 코드에 직접 작성 | **AWS Secrets Manager 연동 및 State 파일 접근 통제/암호화**|

> 사례: **배달의민족과 토스의 AWS Multi-Account 인프라 통합 관리 시 Terraform Cloud 기반 State 격리 및 CI/CD(GitHub Actions) 연동 체계**

#### 한줄 요약

- 운영에서 긴급 변경했다면 다음 Plan이 되돌릴 수 있으므로 예외를 코드에 반영하거나 실제 자원을 원복하는 결정을 즉시 남겨야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **GitOps (깃옵스)**: 애플리케이션 소스코드뿐만 아니라 인프라(IaC) 설정 코드까지 모두 Git에 올려두고, Git PR(Pull Request)이 머지되면 자동으로 인프라가 배포되는 현대적 CI/CD 방법론.

</details>

- IaC 아키텍처 기반 클라우드 네이티브 MSA 환경 설계 시 선언형 프로비저닝 및 불변 인프라 체계 적용.

#### 한줄 요약

- 저장된 Plan만 승인해 적용하고 원격 상태 잠금·삭제 보호·편차 복구를 갖춰야 코드형 인프라가 단순 자동화가 아닌 변경 통제가 된다.
