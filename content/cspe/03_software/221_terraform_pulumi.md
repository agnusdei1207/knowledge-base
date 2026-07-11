---
title: "Terraform·Pulumi (Terraform Pulumi)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 221
extra:
  question_no: "221"
  exam_status: "미출제"
---

## 미리 알고가기

- Terraform은 HCL의 선언 Resource와 Provider Schema로 목표 인프라를 정의하고 Plan·Apply로 상태 차이를 반영함
- Pulumi는 TypeScript·Python·Go·C#·Java 등 일반 언어 Program이 Resource를 등록하고 Preview·Update로 상태 차이를 반영함
- 두 도구 모두 State가 코드 Resource와 실제 Cloud ID를 연결하므로 Remote Backend·Lock·Secret 암호화가 필요함
- Terraform Module은 HCL 입력·출력, Pulumi Component는 언어의 함수·Class·Package로 재사용 경계를 구성함
- 언어 표현력보다 Provider 지원·State 운영·변경 Plan·팀의 코드 Review·시험 도구를 기준으로 선택해야 함

## 작성 근거(검토용)

- Terraform·Pulumi는 정의 언어, 평가 방식, 추상화, State, 변경 미리보기, Provider, 시험, 적합 조건으로 비교함
- 구조와 절차는 코드 실행·Resource Graph·Provider CRUD·State 갱신의 공통 수명주기로 설명함
- 공용 Cloud Module과 Platform Component는 Plan 오차·Drift·시험 통과율·재사용 서비스 수로 검증함

## Ⅰ. 개요

- **정의/개념**: Terraform과 Pulumi는 코드에서 Resource·의존성을 정의하고 Engine이 실제 Cloud 상태와 비교해 생성·변경·교체·삭제를 Provider API로 수행하는 선언형 IaC 도구임
- **배경/필요성**: HCL 중심의 제한된 선언 문법과 일반 언어의 조건·반복·Type·Package 중 팀이 검토·시험·운영할 표현 방식을 선택하되 State·Provider 변경 안전성은 공통으로 관리해야 함

## Ⅱ. 특징

- Terraform은 HCL Block·Expression·Module을 평가해 Resource Graph와 Plan을 생성함
- Pulumi는 언어 Runtime이 Program을 실행하며 Resource·Input·Output·Dependency를 Engine에 등록함
- Terraform Plan과 Pulumi Preview가 실제 상태 Refresh 후 생성·수정·교체·삭제 항목을 제시함
- Provider Plugin이 Resource Schema·Diff·Create·Read·Update·Delete 동작을 Cloud API에 연결함
- Remote State의 Version·Lock·Encryption·Backup과 Secret 값의 출력·Log 노출을 통제함
- Provider·Module·Package Version을 고정하고 Upgrade 전 State Migration·Replacement Plan·회귀 시험을 확인함

## Ⅲ. 종류 및 비교

| 판단 기준 | Terraform | Pulumi |
|:---|:---|:---|
| 정의 언어 | HCL·JSON Configuration | TypeScript·Python·Go·C#·Java·YAML Program |
| 평가 방식 | HCL 표현을 평가해 Resource Graph 생성 | 언어 Runtime이 실행되며 Resource를 Engine에 등록 |
| 재사용 경계 | Module·Variable·Output·Registry | Component Resource·Class·Function·Package |
| 상태·실행 | State Refresh 후 Plan·Apply | Stack State Refresh 후 Preview·Update |
| Provider | Terraform Provider Plugin | Native Provider·Terraform Provider Bridge |
| 시험 방식 | Validate·Plan·`terraform test`·Policy | 언어 Unit Test·Mock·Integration Test·Policy |
| 적합 조건 | HCL 표준 Module과 Plan Review 중심 팀 | 일반 언어 Type·Package·Test 재사용 중심 팀 |

> 요약: Terraform은 HCL Module·Plan, Pulumi는 일반 언어 Component·Preview를 사용하며 두 도구 모두 Provider·State로 실제 자원을 관리함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | Terraform | Pulumi |
|:---|:---|:---|
| Project 정의 | `.tf` HCL과 Module | Language Program과 Project·Stack 설정 |
| Core Engine | Graph·Plan·Apply | Language Host·Resource Monitor·Deployment Engine |
| Resource Provider | Provider Plugin·Schema | Native·Bridged Provider Package |
| 상태 저장 | Workspace State·Backend·Lock | Stack State·Managed/Self-Managed Backend |
| 재사용 Artifact | Module·Provider Registry | Component·Package·Pulumi Registry |
| 정책·자동화 | Plan Pipeline·Policy Framework | Automation API·Policy Pack·Deployment Pipeline |

```text
HCL|Language Program -> Engine -> Resource Graph -> Provider API
                          <-> Remote State·Lock·Secrets
```

> 요약: 정의 언어는 다르지만 Engine이 Resource Graph와 State를 비교하고 Provider가 Cloud CRUD를 수행하는 구조는 같음.

## Ⅴ. 원리 및 절차 흐름도

```text
코드 평가 -> State Refresh -> Diff·Preview -> Policy·Review -> Provider 실행 -> State 기록
```

1. **코드 평가**: HCL 또는 언어 Program에서 Resource·입력·출력·의존성을 구성함
2. **상태 갱신**: Provider Read로 실제 속성을 조회해 Remote State와 비교함
3. **변경 계산**: Plan·Preview가 Create·Update·Replace·Delete와 미지 값을 제시함
4. **승인·실행**: Policy·시험·담당자 Review를 통과한 변경만 Provider API에 적용함
5. **상태 기록**: 실행 결과 ID·속성·Secret·Output을 Lock된 State Version에 저장함

> 요약: Terraform·Pulumi는 코드와 실제 상태의 차이를 미리 제시하고 승인된 Provider 실행 결과를 State에 기록함.

## Ⅵ. 실무 사례

1. 공용 Cloud 환경은 Terraform Module·Remote State를 적용하고 예상 외 변경 건수·Drift 건수를 확인함
2. Platform 팀은 Pulumi Component·Unit Test를 적용하고 시험 통과율·재사용 서비스 수를 확인함

## Ⅶ. 결론

- Terraform·Pulumi는 팀 언어·추상화·시험 방식과 Provider의 필요 Resource 지원·State 보안·변경 Review를 기준으로 선택해야 함
