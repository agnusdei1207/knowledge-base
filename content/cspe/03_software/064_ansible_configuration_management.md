---
title: "Ansible (Ansible Configuration)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 64
---

## Ⅰ. 개요
- **정의**: 에이전트 없이 SSH 기반으로 서버 구성을 선언적으로 관리하는 구성관리 도구
- **배경/필요성**: 서버 수가 증가하면 수동 설정은 환경 편차를 유발하므로, 멱등성 있는 자동 구성관리가 필요함
- **비유**: 체크리스트를 들고 여러 지점을 순회하는 감독관 — 각 지점이 기준에 맞는지 확인하고 차이만 교정함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 구성관리와 프로비저닝 구분 | Agentless, 멱등성, YAML 플레이북 | IaC 프로비저닝 도구(063 참조)와 역할 혼동 금지 |

> 요약: Agentless 방식으로 다수 서버의 구성 상태를 선언적으로 수렴시키는 도구임

## Ⅱ. 구성요소
```text
Control Node --SSH--> Managed Node 1
      |          +--> Managed Node 2
      |          +--> Managed Node N
      v
  Inventory + Playbook + Module
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Control Node | Ansible이 실행되는 관리 서버 | 본사 감독관 |
| Inventory | 관리 대상 호스트 목록과 그룹 정의 | 지점 주소록 |
| Playbook | YAML로 작성된 작업 시나리오 | 점검 체크리스트 |
| Module | 패키지 설치·파일 복사 등 개별 작업 단위 | 공구 세트 |

> 요약: Control Node가 Inventory 기반으로 Playbook의 Module을 대상 서버에 실행함

## Ⅲ. 절차
```text
Write Playbook --> Check Inventory --> Dry-Run --> Apply
```
- 1단계: YAML Playbook에 원하는 구성 상태를 선언함
- 2단계: Inventory 파일로 대상 호스트·그룹을 확인함
- 3단계: `--check` 모드로 변경 사항을 사전 시뮬레이션함
- 4단계: Playbook을 실행하여 대상 서버에 구성을 적용함

> 요약: 작성-대상확인-시뮬레이션-적용의 4단계로 구성을 관리함

## Ⅳ. 문제점
- SSH 병목: 대규모 호스트에 순차 SSH 연결 시 실행 시간이 선형 증가함
- 상태 미저장: 별도 State 파일이 없어 현재 구성 상태를 외부에서 조회하기 어려움
- Playbook 비대화: Role 분리 없이 단일 파일에 작성하면 유지보수 난이도가 급증함

> 요약: SSH 병목, 상태 비저장, Playbook 비대화가 주요 문제임

## Ⅴ. 개선방안
1. 단기: `forks` 값을 조정하고 비동기 실행(`async`/`poll`)으로 병렬성을 확보함
2. 중기: CMDB·Fact Cache를 연동하여 외부에서 구성 상태를 조회 가능하게 함
3. 장기: Ansible Collection·Role 단위로 분리하고 Galaxy 레지스트리로 재사용함

> 요약: 병렬 실행, 상태 외부화, 모듈화로 개선함

## Ⅵ. 전망
- 발전 방향: Ansible Automation Platform과 Event-Driven Ansible로 이벤트 기반 자동화가 확대됨
- 기술사적 판단: 프로비저닝은 Terraform(063 참조), 구성관리는 Ansible로 역할 분리하는 패턴이 표준화됨
- 기술사 제언: IaC 도구와의 책임 경계를 명확히 정의하고 Playbook 모듈화를 초기부터 설계할 필요
