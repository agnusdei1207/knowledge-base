---
title: "IaC 인프라스트럭처 코드 (Infrastructure as Code)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 220
extra:
  question_no: "220"
  exam_status: "미출제"
---

## 미리 알고가기

- IaC는 Compute·Network·Storage·IAM·Middleware 구성을 코드로 정의하고 Version Control·Review·Pipeline으로 변경하는 방식임
- Declarative IaC는 목표 상태와 실제 상태의 차이를 계산하고 Imperative IaC는 실행할 명령·순서를 기술함
- State는 자원 ID·속성·의존성을 코드 주소에 연결하므로 암호화·잠금·Backup·접근 통제가 필요함
- Plan은 변경 예정 자원과 교체·삭제 영향을 보여주며 Apply 전 Policy·비용·보안 검사를 통과해야 함
- Console 수동 변경은 Drift로 탐지해 코드로 반영하거나 선언 상태로 복구해야 함

## 작성 근거(검토용)

- IaC는 표현 방식, 상태·의존성, Plan·Apply, Module, Policy, Drift, Secret을 핵심 축으로 설명함
- 비교표는 선언형·명령형의 기술 대상·순서·상태·멱등성·변경 분석·적합 조건을 대비함
- 개발 환경과 재해 복구 환경은 Drift·수동 변경·배포 Lead Time·재구성 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: IaC는 인프라 자원과 정책의 목표 상태·생성 절차를 코드로 관리하고 자동화 Engine이 Plan·Apply·Drift Detection으로 실제 환경에 반영하는 운영 방식임
- **배경/필요성**: 환경별 수동 생성·변경으로 구성·권한·Version이 달라지는 문제를 재현 가능한 코드와 검토·승인·감사 이력으로 통제해야 함

## Ⅱ. 특징

- Resource·Data Source·Module·Variable·Output으로 자원 경계와 재사용 Interface를 정의함
- 의존 Graph가 생성·변경·삭제 순서를 계산하고 병렬 가능한 자원을 분리함
- Remote State와 Lock이 여러 실행의 자원 Mapping 충돌과 동시 Apply를 방지함
- Pull Request에서 Format·Validate·Plan·Policy·보안·비용 결과를 검토한 뒤 승인된 Commit만 Apply함
- Import·Refresh·Drift Detection으로 기존·수동 변경 자원을 코드·State와 대조함
- Secret 값을 코드·Plan·Log·State에 평문으로 남기지 않고 Secret Manager 참조와 민감 출력 마스킹을 적용함

## Ⅲ. 종류 및 비교

| 판단 기준 | Declarative IaC | Imperative IaC |
|:---|:---|:---|
| 기술 대상 | 자원의 목표 상태·관계 | 실행할 명령·조건·순서 |
| 변경 순서 | Engine이 의존 Graph로 계산 | 작성자가 절차와 예외 분기를 제어 |
| 상태 관리 | State·Provider 조회로 실제 자원과 비교 | 명령 결과·Inventory·응용 상태로 판단 |
| 반복 실행 | 목표 상태가 같으면 변경 계획이 없어야 함 | 멱등 조건을 각 Task·Script에 구현 |
| 변경 분석 | Plan에서 생성·수정·교체·삭제를 제시 | Dry-Run·Check Mode·실행 Log로 영향 확인 |
| 적합 조건 | Cloud 자원·정책의 목표 상태 관리 | OS 설정·배포 절차·조건별 작업 제어 |

> 요약: 선언형은 목표 상태의 차이를 Engine이 계산하고 명령형은 작성한 실행 순서와 멱등 조건으로 상태를 변경함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Resource·Provider | 관리 대상 자원 Schema와 API CRUD 동작을 정의함 |
| Module·Variable·Output | 재사용 경계·입력 계약·생성 결과를 캡슐화함 |
| Dependency Graph | 자원 참조에서 생성·변경·삭제 순서와 병렬성을 계산함 |
| State Backend·Lock | 코드 주소와 실제 자원 ID·속성을 저장하고 동시 실행을 막음 |
| Plan·Apply Engine | 현재·목표 상태 차이를 제시하고 승인된 변경을 실행함 |
| Policy·Drift·Audit | 보안·비용 규칙과 수동 변경·실행 주체·결과를 검사함 |

```text
IaC Commit -> Validate·Plan -> Policy·Review -> Apply Engine -> Provider API
                    State Backend·Lock <-> Actual Infrastructure
```

> 요약: Plan Engine이 코드·State·실제 자원을 비교하고 Policy 승인 후 Provider API로 변경과 State를 함께 갱신함.

## Ⅴ. 원리 및 절차 흐름도

```text
코드 변경 -> 정적 검사 -> Plan -> Policy·Review -> Apply -> State 갱신 -> Drift 검사
```

1. **코드 변경**: Resource·Module·Variable과 Provider Version을 Pull Request로 수정함
2. **정적 검사**: Format·Syntax·Module Test·Secret·보안 규칙을 확인함
3. **Plan 생성**: State·실제 자원·목표 코드 차이와 교체·삭제 영향을 계산함
4. **승인·Apply**: Policy·비용·담당자 Review를 통과한 Plan만 잠금 후 실행함
5. **State·Drift 관리**: 결과를 Remote State에 기록하고 주기적으로 수동 변경을 탐지함

> 요약: IaC 변경은 Plan의 자원 영향을 검토한 뒤 잠금 상태에서 Apply하고 실행 결과와 Drift를 State로 관리함.

## Ⅵ. 실무 사례

1. 개발 환경은 IaC Module·Policy 검사를 적용하고 Drift 건수·환경 생성 Lead Time을 확인함
2. 재해 복구 환경은 Versioned IaC와 Remote State Backup을 적용하고 재구성 시간·환경 차이를 확인함

## Ⅶ. 결론

- IaC는 코드·Provider·State·Plan·Policy·Secret·Drift를 동일 변경 Pipeline에서 검토·승인·감사해야 함
