---
sidebar:
  order: 182
  label: "182. IaC 인프라스트럭처 코드"
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

- **IaC(Infrastructure as Code)**: 클라우드 인프라를 수동 대신 기계가 판독 가능한 선언적 코드(Declarative Code)로 정의·배포하는 자동화 관행.
- **테라폼(Terraform)**: HCL(HashiCorp Configuration Language) 기반 오픈소스 IaC 도구로 인프라 구축의 업계 표준 플랫폼.
- **멱등성(Idempotency)**: 반복 실행해도 최종 인프라 상태(End-State)가 동일하게 유지되는 선언형 IaC의 핵심 철학.

</details>

- 정의: 인프라 구성 요소를 코드로 정의하여 버전 관리(Git), 테스트, CI/CD 등 엔지니어링 생태계를 인프라로 확장한 자동화 기술.
- 배경: 수동 관리(Click-Ops)의 휴먼 에러, 환경 불일치, 복제 불가능성 한계 극복.

## Ⅱ. 핵심 성질

<details><summary>핵심 용어</summary>

- **불변 인프라(Immutable Infrastructure)**: 서버 수정(Update) 대신 신규 서버 이미지로 대체(Replace)하여 환경 일관성을 보장하는 철학.
- **선언형 접근(Declarative Approach)**: 최종 상태(What)만 선언 시 엔진이 생성/변경을 수행하는 방식.
- **편차 탐지(Drift Detection)**: 선언적 목표 상태와 실제 인프라 상태 간 불일치를 식별하여 동기화를 유도하는 기능.

</details>

- 코드 기반 상태 장부 관리 및 실 자원 연동 변경 통제.

## Ⅲ. 아키텍처 및 구성요소

<details><summary>핵심 용어</summary>

- **상태 파일(State File)**: 생성된 인프라 리소스 정보를 매핑한 JSON 장부(`.tfstate`). 코드와 실제 환경 비교의 핵심 기준점.

</details>

```text
┌────────────────────────────────────────────────────────────┐
│                  테라폼 기반 IaC 실행 구조                 │
├────────────────────────────────────────────────────────────┤
│ 1. [코드(HCL)] ──► 2. [테라폼 엔진] ◄──(비교)── 3. [상태]   │
│                      │                             │       │
│ 5. [인프라 자원] ◄───(API 호출)── 4. [프로바이더] ◄───────┘
└────────────────────────────────────────────────────────────┘
```

| 구성요소 | 기능 및 책임 | 실무 적용 |
|:---|:---|:---|
| **Config** | 인프라 최종 형상 정의 소스코드 | `.tf` (VPC 선언) |
| **Core** | 코드 파싱 및 상태 비교 엔진 | `plan/apply` |
| **Backend** | 팀 협업 시 상태 파일 원격 저장 | S3 + DynamoDB(Lock) |
| **Provider** | 클라우드 API 통신 어댑터 | AWS/K8s Provider |

## Ⅳ. 콘텐츠 요청 파이프라인

<details><summary>핵심 용어</summary>

- **Terraform Plan**: 인프라 변경 전 리소스 생성(+), 변경(~), 삭제(-) 내역을 시뮬레이션하여 치명적 실수를 방지하는 단계.

</details>

```text
[Dev]               [Terraform]                [Cloud]
  │                      │                        │
  ├─ 1. Write Code ─────►│                        │
  ├─ 2. Plan (시뮬) ───►│◄──(Read State & Info)───┤
  │                      │                        │
  │◄─ 3. Print Plan ─────┤                        │
  │                      │                        │
  ├─ 4. Apply (적용) ───►│ (API 호출) ───────────►│
```

- 흐름: 코드/상태 대조 → 시뮬레이션(Plan) → API 호출 및 상태 갱신.

## Ⅴ. IaC 도구 패러다임 비교

<details><summary>핵심 용어</summary>

- **구성 관리(Configuration Management)**: 인프라 프로비저닝 후 OS 내 패키지 설치 및 환경 설정(Conf)을 제어(Ansible, Chef 등).

</details>

| 항목 | 프로비저닝 (Terraform) | 구성 관리 (Ansible) |
|:---|:---|:---|
| **핵심 목적** | 자원(VPC, DB) 생성/소멸 | OS 내부 S/W 및 설정 |
| **접근 방식** | 선언형(상태 파일 관리) | 절차형(순차 스크립트) |
| **운영 철학** | 불변 인프라(대체) | 가변 인프라(덮어쓰기) |

## Ⅵ. 실무 난제 및 대책

<details><summary>핵심 용어</summary>

- **구성 편차(Configuration Drift)**: 수동 조작으로 코드와 실제 인프라 상태가 어긋나는 현상.

</details>

| 난제 | 원인 | 대책 |
|:---|:---|:---|
| **편차(Drift)** | 무단 콘솔 수동 조작 | 감지 알람 및 IAM 쓰기 권한 통제 |
| **동시 수정** | 중복 Apply 실행 | S3+DynamoDB 기반 State Lock |
| **민감 정보** | 코드 내 패스워드 포함 | Secret Manager 연동 및 파일 암호화 |

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **GitOps**: IaC 코드까지 Git으로 관리하고, PR 머지 시 자동 인프라 배포를 수행하는 현대적 CI/CD 방법론.

</details>

- IaC 기반 불변 인프라 및 변경 통제 체계 적용.
