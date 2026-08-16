---
sidebar:
  order: 182
  label: "182. IaC 인프라스트럭처 코드"
  badge:
    text: "미출 • 50%"
    variant: note
title: "IaC 인프라스트럭처 코드 (Infrastructure as Code)"
date: "2026-08-14T04:00:00+09:00"
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

- **IaC(Infrastructure as Code)**: 클라우드 인프라를 수동 대신 기계가 판독 가능한 선언적 코드(Declarative Code)로 정의·배포하는 자동화 관행.
- **테라폼(Terraform)**: HCL(HashiCorp Configuration Language) 기반 오픈소스 IaC 도구로 인프라 구축의 업계 표준 플랫폼.
- **멱등성(Idempotency)**: 반복 실행해도 최종 인프라 상태(End-State)가 동일하게 유지되는 선언형 IaC의 핵심 철학.

</details>

- 정의/개념: Infrastructure를 실행 가능한 Code로 관리하는 **IaC**
- 배경/필요성: Click-Ops는 **변경 이력•재현성•환경 일치** 보장 곤란

#### 한줄 요약

- 인프라 목표 상태를 코드와 변경 이력으로 남겨 같은 환경을 반복 생성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **불변 인프라(Immutable Infrastructure)**: 서버 수정(Update) 대신 신규 서버 이미지로 대체(Replace)하여 환경 일관성을 보장하는 철학.
- **선언형 접근(Declarative Approach)**: 최종 상태(What)만 선언 시 엔진이 생성/변경을 수행하는 방식.
- **편차 탐지(Drift Detection)**: 선언적 목표 상태와 실제 인프라 상태 간 불일치를 식별하여 동기화를 유도하는 기능.

</details>

- **Declarative Config**로 목표 상태 정의
- **State**•**Plan**으로 실제 자원과 변경 범위 비교
- **Version Control•Review**로 인프라 변경 추적

#### 한줄 요약

- 코드와 실제 상태의 차이를 계획으로 검토한 뒤 승인된 변경만 적용한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **상태 파일(State File)**: 생성된 인프라 리소스 정보를 매핑한 JSON 장부(`.tfstate`). 코드와 실제 환경 비교의 핵심 기준점.

</details>

```text
[IaC Engine]
 ├── [Config]
 ├── [Core]
 ├── [Backend]
 └── [Provider]
```

| 구성요소 | 책임 |
|---|---|
| Config | Resource의 **목표 상태•의존성** 선언 |
| Core | Config•State•실제 자원의 **차이 계산** |
| Backend | State의 **원격 저장•Lock•Version** 관리 |
| Provider | 공급자 API와 Resource **CRUD Adapter** 제공 |

#### 한줄 요약

- 구성은 목표, 상태는 관리 장부, Provider는 실제 자원 API 경계를 맡는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Terraform Plan**: 인프라 변경 전 리소스 생성(+), 변경(~), 삭제(-) 내역을 시뮬레이션하여 치명적 실수를 방지하는 단계.

</details>

```text
[IaC 변경 요청]
      │
      ▼
1. Config 검증
      │
      ▼
2. State•실제 자원 Refresh
      │
      ▼
3. 변경 Plan 생성
      │
      ▼
4. Review•Policy 승인
      │
      ▼
5. Apply•State 갱신
      │
      ▼
[인프라 결과 반환]
```

### 동작 원리

1. **Config 검증**: Syntax•Type•Module 입력 확인
2. **State•실제 자원 Refresh**: 관리 객체와 현재 속성 대조
3. **변경 Plan 생성**: 생성•변경•교체•삭제 범위 산출
4. **Review•Policy 승인**: 파괴 변경•비용•보안 기준 검사
5. **Apply•State 갱신**: Provider 호출과 결과 장부 기록

#### 한줄 요약

- 파괴 변경과 편차를 Plan에서 확인하고 승인 후 실제 자원과 State를 함께 갱신한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **구성 관리(Configuration Management)**: 인프라 프로비저닝 후 OS 내 패키지 설치 및 환경 설정(Conf)을 제어(Ansible, Chef 등).

</details>

| 항목 | 프로비저닝 (Terraform) | 구성 관리 (Ansible) |
|:---|:---|:---|
| 핵심 목적 | 자원(VPC, DB) 생성/소멸 | OS 내부 S/W 및 설정 |
| 접근 방식 | 선언형(상태 파일 관리) | 절차형(순차 스크립트) |
| 운영 철학 | 불변 인프라(대체) | 가변 인프라(덮어쓰기) |

#### 한줄 요약

- 자원 수명주기는 Provisioning, OS 내부 상태는 구성 관리가 주로 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **구성 편차(Configuration Drift)**: 수동 조작으로 코드와 실제 인프라 상태가 어긋나는 현상.

</details>

| 난제 | 원인 | 대책 |
|:---|:---|:---|
| 편차 | 무단 콘솔 수동 조작 | 감지 알람 및 IAM 쓰기 권한 통제 |
| 동시 수정 | 중복 Apply 실행 | S3+DynamoDB 기반 State Lock |
| 민감 정보 | 코드 내 패스워드 포함 | Secret Manager 연동 및 파일 암호화 |

#### 한줄 요약

- 원격 State를 잠그고 민감값을 분리하며 Console 변경은 Drift로 탐지한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **GitOps**: IaC 코드까지 Git으로 관리하고, PR 머지 시 자동 인프라 배포를 수행하는 현대적 CI/CD 방법론.

</details>

- 공유 자원은 **원격 State•Lock•Plan Review**, 임시 자원은 불변 교체

#### 한줄 요약

- 선언 코드와 실제 자원을 계속 대조하고 승인된 Plan만 적용해 재현성과 통제를 확보한다.
