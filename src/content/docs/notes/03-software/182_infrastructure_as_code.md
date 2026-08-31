---
sidebar:
  order: 182
  label: "182. IaC 인프라스트럭처 코드"
  badge:
    text: "미출 · 50%"
    variant: note
title: "IaC 인프라스트럭처 코드 (Infrastructure as Code)"
date: "2026-08-31T10:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **IaC(Infrastructure as Code)**: 서버, 네트워크 등 인프라 자원을 기계가 판독 가능한 선언적 코드(HCL/YAML)로 정의하여 형상 관리 및 자동 프로비저닝을 수행하는 엔지니어링 관행.
- **Declarative vs Imperative**: 최종 희망 상태(What)만 선언하는 선언형(Terraform)과 순차 실행 명령(How)을 나열하는 절차형(Shell Script).

</details>

- 정의/개념: 인프라 자원을 기계 판독 가능한 **선언적 코드로 작성하여 버전 관리, 변경 계획 검토 및 프로비저닝을 자동화하는 기술**
- 배경/필요성: 클라우드 웹 콘솔(GUI)을 통한 수동 인프라 프로비저닝에서 발생하는 잦은 인적 실수(Human Error), 환경 간 형상 불일치(Configuration Drift), 변경 이력 추적 불가의 한계 및 재해 복구(DR) 시의 환경 재현 지연을 해결하기 위해, 서버·네트워크·보안 설정을 기계 판독 가능한 선언적 코드(HCL/YAML)로 작성하여 Git 버전 관리 및 변경 사전 검토(Plan)를 자동화하는 IaC(코드형 인프라)를 도입하여 **불변 인프라(Immutable Infrastructure) 구축과 멱등성(Idempotency) 기반의 자동 프로비저닝을 달성**할 필요

#### 한줄 요약
- 인프라 목표 상태를 코드로 정의하고 버전 관리하여 재현성과 자동화를 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Idempotency(멱등성)**: 코드를 여러 번 실행해도 최종 인프라 상태가 항상 동일하게 유지되는 성질.
- **State File(`.tfstate`)**: 선언된 코드와 실제 배포된 물리 인프라 리소스를 매핑하여 변경 범위를 계산하는 상태 관리 장부.

</details>

- 최종 희망 상태만 정의하면 엔진이 차이를 계산하는 **선언형 설정(Declarative)**
- 실제 인프라 변경 전 생성/수정/삭제 범위를 시뮬레이션하는 **Plan 기반 영향도 검토**
- Git 형상 관리를 통한 **인프라 변경 이력 추적 및 자동화된 롤백 지원**

#### 한줄 요약
- 선언형 설정, 상태 기반 차이 계산, Plan 사전 검증을 통해 인프라 신뢰성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IaC 엔진 4대 아키텍처 계층**: Configuration(HCL 코드), Core Engine(차이 계산), State Backend(원격 상태 잠금), Provider(CSP API 어댑터).

</details>

```text
[IaC 구성]
|-- 코드 명세
|-- 코어 엔진
|-- 상태 백엔드
`-- 프로바이더
```

선의 의미: 계층 및 선언된 HCL 코드를 Core 엔진이 해석하여 원격 State와 비교 후 Provider API를 통해 실제 인프라를 프로비저닝하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 코드 명세 | 리소스의 **목표 속성·의존성**을 HCL로 정의 | Git 형상 관리 |
| 코어 엔진 | 상태를 대조하여 **변경 계획(Plan)** 산출 | DAG 그래프 해석 |
| 상태 백엔드 | `.tfstate` 원격 저장과 **동시 수정 잠금** | State Locking |
| 프로바이더 | 공급자 API로 **물리 리소스 CRUD** 실행 | 플러그인 어댑터 |

#### 한줄 요약
- 상태 백엔드가 실제 인프라의 장부 역할을 대신하므로, 엔진은 클라우드를 전수 조회하지 않고도 코드와 현실의 차이만 계산해 변경 범위를 좁힌다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IaC 프로비저닝 5단계**: 코드 검증 $\to$ State 갱신 $\to$ Plan 시뮬레이션 $\to$ 리뷰/승인 $\to$ Apply 및 State 저장.

</details>

```text
개발자의 인프라 변경 코드 PR 제출
        │
   1. [코드 유효성 검증] `terraform validate` 및 tflint를 통한 문법 및 보안 정책 검사
        │
   2. [실제 자원 갱신] `terraform refresh`로 원격 클라우드의 실제 인프라 최신 상태 동기화
        │
   3. [변경 계획 생성] `terraform plan`을 실행하여 생성(+), 수정(~), 삭제(-) 내역 산출
        │
   4. [리뷰 및 OPA 승인] 파괴적 삭제(Destroy) 여부 및 보안 정책 준수 여부 동료 검토/승인
        │
   5. `terraform apply` 실행으로 AWS 리소스를 프로비저닝하고 `.tfstate` 원격 장부 갱신
```

#### 한줄 요약
- Plan 단계가 변경을 적용 전에 드러내므로, 되돌리기 비싼 인프라 변경의 검토 비용이 사고 이후 복구가 아니라 리뷰 시점으로 앞당겨진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Provisioning vs Configuration Management**: 인프라 뼈대 구축(Terraform)과 OS 내부 소프트웨어 패키지 설정(Ansible).

</details>

| 비교 항목 | 인프라 프로비저닝 (Terraform) | 구성 관리 (Ansible) |
|:---|:---|:---|
| 핵심 관리 대상 | **클라우드 인프라 자원 (VPC, Subnet, RDS, K8s)** | **OS 내부 소프트웨어 설치, 환경설정 파일, 계정**|
| 접근 방식 및 언어 | **선언형 (HCL: 상태 파일 기반 차이 계산)** | **절차형/선언형 혼합 (YAML Playbook)** |
| 인프라 운영 철학 | **불변 인프라 (Immutable: 신규 교체 방식)** | **가변 인프라 (Mutable: 기존 서버 덮어쓰기)** |
| 에이전트 설치 여부 | 무설치 (클라우드 REST API 직접 호출) | 무설치 (SSH / WinRM 원격 명령 실행) |

#### 한줄 요약
- 인프라 생성과 뼈대 구축은 Terraform, OS 내부 설정과 패키지 관리는 Ansible을 조합한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Configuration Drift**: 엔지니어가 콘솔에서 임의로 인프라를 수동 조작하여 코드와 실제 인프라 상태가 어긋나는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무단 콘솔 조작으로 인한 구성 편차 (Configuration Drift) | **정기적 `terraform plan` 드리프트 감지 파이프라인 및 IAM 쓰기 제한** | 인프라 코드-실제 일치율 100% |
| 동시 `terraform apply` 실행으로 인한 State 파일 오염 | **S3 Backend와 DynamoDB 기반 분산 Lock (`LockID`) 강제** | State 파일 동시 수정 충돌 방지 |
| State 파일에 DB 패스워드 등 민감정보 평문 노출 | **AWS Secrets Manager 연동 및 S3 SSE-KMS 암호화 적용** | 크리덴셜 유출 사고 원천 차단 |
| 실수로 인한 프로덕션 DB 인프라 강제 삭제 사고 | **HCL 코드 내 `lifecycle { prevent_destroy = true }` 설정** | 중요 리소스 우발적 파괴 방어 |

#### 한줄 요약
- 네 대책은 인프라를 코드로 옮긴 대가로 상태 파일 하나에 집중된 정합성·기밀·파괴 위험을 락과 암호화, 수명주기 규칙으로 되사는 선택이다.

## Ⅶ. 결론

- 클라우드 네이티브 및 데브옵스(DevOps) 환경에서 인프라 변경의 민첩성과 안정성을 확보하는 **가장 핵심적인 인프라 엔지니어링 패러다임**으로 확립되었으며, 실무 구축 시에는 **선언적 프로비저닝의 사실상 표준인 Terraform과 구성 관리용 Ansible의 역할 분담, 상태 파일 충돌을 방지하는 원격 백엔드 분산 락(S3 + DynamoDB Lock), 수동 변경에 따른 드리프트를 감지·차단하는 CI/CD 파이프라인, 파괴적 삭제를 방지하는 `prevent_destroy` 수명주기 통제 및 OPA 정책 검증**을 결합하여 무결점 엔터프라이즈 인프라 거버넌스를 완성

#### 한줄 요약
- IaC는 선언적 코드와 상태 파일 관리를 통해 인프라의 버전 관리, 자동 프로비저닝, 변경 사전 검증을 실현하는 현대 클라우드 운영의 핵심 기술이다.
