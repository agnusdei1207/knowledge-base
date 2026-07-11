---
title: "Ansible·Chef·Puppet (Ansible Chef Puppet)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 222
extra:
  question_no: "222"
  exam_status: "미출제"
---

## 미리 알고가기

- 구성 관리는 OS·Package·File·Service·Account의 목표 상태를 코드로 정의하고 반복 적용해 Drift를 교정하는 방식임
- Ansible은 Control Node가 Inventory 대상에 SSH·WinRM으로 Module을 실행하는 Agentless Push 방식이 중심임
- Chef는 Node의 Client가 Cookbook·Recipe를 받아 Resource를 수렴시키는 Client-Server Pull 방식이 중심임
- Puppet은 Agent Fact로 Catalog를 요청하고 Manifest에서 Compile한 목표 상태를 적용·보고하는 Pull 방식이 중심임
- 세 도구 모두 명령 실행 성공이 아니라 두 번째 실행의 불필요한 변경 여부와 실제 서비스 상태로 멱등성을 검증해야 함

## 작성 근거(검토용)

- Ansible·Chef·Puppet은 실행 주체, Agent, 정의 언어, 상태 계산, 대상 정보, 실행 주기, 적합 조건으로 비교함
- 구조와 절차는 Inventory·Fact·정책 Compile·Resource 적용·Report·Drift 교정의 공통 흐름으로 설명함
- 서버 초기 설정과 상시 구성 관리는 변경 Host 비율·실패율·Drift 교정 시간·준수율로 검증함

## Ⅰ. 개요

- **정의/개념**: Ansible·Chef·Puppet은 서버의 Package·File·Service·Account 상태를 코드와 Resource로 정의하고 원격 Push 또는 Agent Pull 실행으로 목표 상태에 수렴시키는 구성 관리 도구임
- **배경/필요성**: Server별 수동 명령과 장기 운영 변경으로 설정·권한·Package Version이 달라지는 문제를 반복 가능한 정책·실행 기록·Drift 교정으로 통제해야 함

## Ⅱ. 특징

- Inventory·Fact가 Host Group·OS·Network·Role 정보를 제공하고 Template·Variable이 환경별 값을 분리함
- Resource·Module이 현재 상태를 조회한 뒤 필요한 변경만 수행하도록 멱등 조건을 구현함
- Role·Collection·Cookbook·Module로 공통 구성을 재사용하고 Version을 고정함
- Secret은 Vault·Encrypted Data Bag·외부 Secret Manager에서 주입하고 Log·Report에 값을 남기지 않음
- Lint·Unit·Integration·Test Instance에서 변경·재실행·Rollback 조건을 검증한 뒤 대상 Group을 단계별 확대함
- 실행 결과의 Changed·Failed·Skipped·Drift·Compliance 상태를 중앙 Report와 Monitoring에 연결함

## Ⅲ. 종류 및 비교

| 판단 기준 | Ansible | Chef | Puppet |
|:---|:---|:---|:---|
| 실행 주체 | Control Node가 대상에 Playbook Push | Chef Client가 정책을 Pull해 수렴 | Puppet Agent가 Catalog를 Pull해 적용 |
| Agent 요구 | SSH·WinRM 대상은 상주 Agent 불필요 | Node에 Chef Client 필요 | Node에 Puppet Agent 필요 |
| 정의 방식 | YAML Playbook·Role·Module | Ruby DSL Recipe·Cookbook·Resource | Declarative Manifest·Class·Module |
| 상태 계산 | Module이 원격 현재 상태를 확인 | Client가 Resource Collection을 Compile·Converge | Server가 Fact 기반 Catalog를 Compile |
| 대상 정보 | 정적·동적 Inventory와 Gathered Facts | Node Attribute·Ohai Data | Facter Fact·Node Classification |
| 실행 시점 | 배포·운영자가 Job·Event로 실행 | Client 주기·Job으로 실행 | Agent 주기·Orchestrator Job으로 실행 |
| 적합 조건 | 초기 설정·배포 절차·즉시 원격 작업 | Recipe 기반 상시 수렴과 응용 배포 | Catalog 기반 정책·준수 상태 관리 |

> 요약: Ansible은 Agentless Push, Chef는 Recipe Convergence, Puppet은 Fact 기반 Catalog 적용으로 서버 구성을 관리함.

## Ⅳ. 구성요소 및 구조

| 도구 | 핵심 구성요소 | 역할 |
|:---|:---|:---|
| Ansible | Control Node·Inventory·Playbook·Module | 대상 Group에 Task를 순서대로 원격 실행함 |
| Chef | Workstation·Chef Server·Client·Cookbook | Policy를 배포하고 Node Resource를 Converge함 |
| Puppet | Server·Agent·Manifest·Catalog·Facter | Fact로 Catalog를 Compile하고 목표 상태를 적용함 |
| 공통 | Repository·Secret·CI Test | 구성 코드 Version·민감 값·시험을 관리함 |
| 공통 | Report·Compliance·Drift | 실행 결과·준수 상태·수동 변경을 추적함 |

```text
Config Repository -> Controller|Server -> Inventory|Facts -> Managed Nodes
                                              Apply Resources -> Report
```

> 요약: 코드 저장소의 정책을 Controller·Server가 대상 정보와 결합하고 Node 적용 결과를 Report로 회수함.

## Ⅴ. 원리 및 절차 흐름도

```text
대상·Fact 수집 -> 정책 해석·Compile -> 현재 상태 비교 -> Resource 적용 -> Report -> 재실행·Drift 교정
```

1. **대상·Fact 수집**: Inventory·Node Attribute·Facter가 Host와 현재 환경 정보를 제공함
2. **정책 해석**: Playbook·Recipe·Manifest를 Variable·Role과 결합해 실행 Resource를 만듦
3. **현재 상태 비교**: Package·File·Service·Account가 목표와 다른지 Module·Provider가 확인함
4. **Resource 적용**: 필요한 변경만 수행하고 Handler·Notification으로 의존 Service를 갱신함
5. **Report·교정**: 변경·실패·준수 결과를 저장하고 재실행·수동 Drift를 교정함

> 요약: 대상 Fact와 정책을 결합해 현재·목표 상태 차이만 적용하고 Report·재실행으로 멱등성과 Drift를 확인함.

## Ⅵ. 실무 사례

1. 신규 서버 설정은 Ansible Role·동적 Inventory를 적용하고 변경 Host 비율·실패 Host 수를 확인함
2. 상시 서버 정책은 Puppet Agent·Catalog를 적용하고 Drift 교정 시간·정책 준수율을 확인함

## Ⅶ. 결론

- Ansible·Chef·Puppet은 연결 방식·Agent 운영·정책 표현·실행 주기·Report·Secret 관리 요구로 선택해야 함
