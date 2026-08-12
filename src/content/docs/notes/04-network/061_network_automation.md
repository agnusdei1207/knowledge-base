---
sidebar:
  order: 61
  label: "061. 네트워크 자동화 - Ansible•RESTCONF•NETCONF (Network Automation)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "네트워크 자동화 - Ansible•RESTCONF•NETCONF (Network Automation)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-network"
weight: 61
extra:
  question_no: "061"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "설계•운영형: 자동화•검증•Rollback 현재성"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **네트워크 자동화(Network Automation)**: 목표 네트워크 상태를 모델과 코드로 정의하고 반복 가능한 파이프라인으로 검증•배포•복구하는 가상화 인프라 운영 체계이다.
- **진실의 원천(Source of Truth, SoT)**: IP 주소, VLAN 토폴로지, 보안 정책의 목표 선언(Intent) 상태를 유일한 단일 기준(Single Source of Truth)으로 수용하는 데이터 저장소이다.
- **명령줄 인터페이스(Command-Line Interface, CLI)**: 장비별 전용 텍스트 명령과 비구조화된(Unstructured) 문자열 출력을 주고받는 기존 네트워크 조작 인터페이스이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: JSON/XML 기반의 구조화 데이터 스키마를 통해 네트워크 설정과 상태를 프로그래밍 방식으로 조작하는 표준 호출 규격이다.

</details>

- 정의/개념: **네트워크 자동화**(Network Automation)는 **진실의 원천**(Source of Truth)에 선언한 목표 망 상태를 YANG 데이터 모델 및 코드(IaC)로 변환하여 수동 개입 없이 검증•배포•복구하는 자율 운영 프로토콜 체계이다.
- 배경/필요성: 엔지니어가 장비별로 개별 접속하는 수동 **CLI** 방식은 사람의 실수(Human Error), 설정 파편화, 감사 누락을 유발하므로, **API** 기반의 프로그래밍 가능 네트워크(Programmable Network) 전환이 필수적이다.

#### 한줄 요약

- 선언적 코드로 네트워크 목표 상태를 정의하고 CI/CD 파이프라인을 통해 동적으로 검증 및 배포하는 자동화 구축 체계 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **설정 드리프트(Configuration Drift)**: 장비의 실제 운영 설정이 진실의 원천(SoT)에 정의된 목표 선언 상태에서 벗어나 임의로 변경된 현상이다.
- **멱등성(Idempotency)**: 동일한 자동화 스크립트나 플레이북을 여러 번 반복 실행하더라도 추가적인 부작용 없이 항상 동일한 목표 상태를 유지하는 성질이다.
- **지속적 통합(Continuous Integration, CI)**: 코드 변경 사항이 발생할 때마다 구문 검사(Linting), YANG 스키마 검증, 시뮬레이션 테스트를 자동으로 수행하는 개발 및 운영 메커니즘이다.
- **YANG 모델(YANG Data Model)**: NETCONF/RESTCONF 프로토콜에서 네트워크 설정 및 상태 데이터의 계층 구조, 자료형, 제약 조건을 표준화하여 정의하는 데이터 모델링 언어(RFC 6020/7950)이다.

</details>

- **설정 드리프트**(Configuration Drift) 탐지 기능을 통해 장비의 실제 가동 상태와 **SoT** 정본 간의 갭을 지속적으로 감시 및 원상 복구한다.
- **YANG 모델** 기반의 구조화 데이터 및 **CI** 검증 단계를 도입하여 배포 이전에 Syntax Error 및 정책 충돌을 미리 선제 차단한다.
- **멱등성**(Idempotency)을 보장함으로써 플레이북 재실행 시 수용 변경분만 부분적으로 적용하여 네트워크 연속성을 유지한다.

#### 한줄 요약

- YANG 모델 기반 구조화 스키마와 멱등성 보장을 통해 설정 드리프트를 차단하는 선언적 네트워크 관리 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **네트워크 설정 프로토콜(Network Configuration Protocol, NETCONF)**: YANG 모델 기반 데이터를 SSH 상의 XML-RPC 통신으로 안전하게 조회 및 수정하며 커밋/롤백 트랜잭션을 지원하는 IETF 표준 프로토콜이다.
- **원격 프로시저 호출(Remote Procedure Call, RPC)**: 클라이언트가 원격 네트워크 장비의 관리 기능을 로컬 함수처럼 호출하는 가상화 통신 메커니즘이다.
- **REST 설정 프로토콜(REST Configuration Protocol, RESTCONF)**: HTTP/1.1 및 HTTP/2 프로토콜 기반으로 JSON/XML 포맷을 활용하여 YANG 데이터 자원을 다루는 경량화 RESTful API 프로토콜이다.
- **하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**: 웹 통신 표준 프로토콜로서 GET, POST, PUT, DELETE 메서드를 네트워크 관리 자원 조작에 활용한다.
- **자바스크립트 객체 표기법(JavaScript Object Notation, JSON)**: 경량의 텍스트 기반 데이터 교환 형식으로 RESTCONF 통신 시 가독성 높은 메세지 구조를 제공한다.
- **확장성 마크업 언어(Extensible Markup Language, XML)**: 태그 구조를 통해 계층적 데이터를 명확히 규정하며 NETCONF 프로토콜의 표준 페이로드로 사용된다.
- **앤서블(Ansible)**: 에이전트리스(Agentless) 방식으로 SSH/NETCONF 접속을 통해 인벤토리 대상 장비에 선언형 플레이북(Playbook) 설정을 동적 적용하는 오케스트레이션 도구이다.

</details>

- **NETCONF**는 **XML-RPC** 및 **YANG 모델**을 활용해 강력한 트랜잭션(Edit-config, Commit)을 제공하고, **RESTCONF**는 **HTTP** 메서드와 **JSON** 포맷을 활용해 웹 애플리케이션 연동 편의성을 증대시킨다.
- **Ansible**은 에이전트 설치 없이 **SoT** 변수를 바인딩하여 다종 벤더 장비의 설정 상태를 동기화한다.

```text
네트워크 자동화 (Network Automation Architecture)
├─ 진실의 원천 (Source of Truth: NetBox / Nautobot)
├─ Git & CI/CD 파이프라인 (Git, GitHub Actions, GitLab CI)
├─ 자동화 오케스트레이터 (Ansible Engine, NSO)
├─ 프로토콜 및 데이터 모델 (NETCONF / RESTCONF / YANG)
└─ 멀티 벤더 네트워크 장비 (Cisco, Juniper, Arista Switches/Routers)
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **진실의 원천 (Source of Truth, SoT)** | IPAM/DCIM 연동을 통한 목표 IP, VLAN, 인터페이스 구성 정본 수용 |
| **Git & CI/CD 파이프라인 (Git & CI Pipeline)** | IaC 코드 버전 관리, Syntax/YANG 검증 및 자동화 승인 이력 관리 |
| **앤서블 오케스트레이터 (Ansible Orchestration)** | Playbook 기반 멀티 벤더 장비 배포 순서 및 의존성 동적 조율 |
| **YANG & 관리 API (YANG & Mgmt API)** | NETCONF/RESTCONF 프로토콜 표준에 따른 트랜잭션 기반 설정 조회/변경 |
| **네트워크 장비 (Network Devices)** | 후보 설정(Candidate) 검증 후 주설정(Running) 확정 및 Telemetry 수집 |

#### 한줄 요약

- SoT 정본 관리와 Git/Ansible 파이프라인, NETCONF/RESTCONF 표준 API 연계를 통한 End-to-End 오케스트레이션 아키텍처 구현 필수.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **후보 설정(Candidate Configuration)**: 실행 중인 설정(Running Config)에 반영하기 전 변경 사항을 임시 저장하여 미리 구문 검증 및 롤백 준비를 마치는 데이타 저장 공간이다.
- **기능 광고(Capability Advertisement)**: NETCONF 세션 수립 시 장비가 자사의 지원 YANG 모듈 및 확장 기능 패키지를 상대방에게 고지하는 헬로(Hello) 절차이다.
- **롤백(Rollback)**: 배포 실패 또는 네트워크 도달성 상실 시 이전의 검증된 정상 실행 설정 상태로 즉각 복구하는 자동 회복 기능이다.
- **깃(Git)**: 설정 코드의 변경 이력 관리, 코드 리뷰(Pull Request) 및 자동화 파이프라인 트리거 기능을 담당하는 버전 관리 시스템이다.
- **사전 검증(Pre-validation)**: 스키마 타당성, IP 중복성, 룰셋 충돌을 배포 전 시뮬레이터에서 선제 검사하는 단계이다.
- **승인 변경 전달(Approved Change Delivery)**: 리뷰어의 승인(Approval)을 받은 검증 코드만 프로덕션 자동화 엔진으로 이관하는 단계이다.
- **설정 차이 배포(Diff-based Provisioning)**: 목표 상태와 현 운영 상태 간의 델타(Diff) 값만 산출하여 Candidate 저장소에 주입하는 단계이다.
- **실체 상태 보고(State Reporting)**: 변경 후 실제 라우팅 테이블 및 인터페이스 업/다운 상태를 Telemetry로 동적 관측하는 단계이다.
- **검증 실패 시 롤백(Rollback on Validation Failure)**: Health-check 검증에 실패할 경우 자동 타임아웃 롤백을 발동하는 회복 단계이다.

</details>

```text
목표 상태 변경 요청 (Git Commit / PR)
        │
        ▼
1. 사전 검증 (Lint & YANG Validation)
        ├─ [실패] 변경 차단 및 개발자 피드백
        └─ [통과]
            │
            ▼
2. 승인 변경 전달 (CI/CD Pipeline to Ansible)
            │
            ▼
3. 설정 차이 배포 (NETCONF Candidate Edit-config)
            │
            ▼
4. 실제 상태 보고 (Commit & Telemetry Health Check)
            ├─ [성공] Running Config 확정 및 파이프라인 종료
            └─ [실패] 5. 검증 실패 시 롤백 (Automatic Rollback)
                              │
                              ▼
                         이전 정상 상태 복구 (Confirmed Commit Rollback)
```

### 동작 원리

1. **사전 검증**: 코드 제출 시 **기능 광고** 정보 기반으로 YANG 스키마 유효성 및 정책 도달성을 사전 검사한다.
2. **승인 변경 전달**: **Git** PR 승인을 거친 코드만 Ansible 오케스트레이터로 안전하게 전달한다.
3. **설정 차이 배포**: **NETCONF** 프로토콜의 Edit-config 명령을 호출하여 **후보 설정**(Candidate) 데이터에 델타 적용한다.
4. **실체 상태 보고**: Commit 적용 직후 **텔레메트리** 지표로 라우팅 정상 수렴 여부를 동적으로 파악한다.
5. **검증 실패 시 롤백**: 수렴 실패 시 Confirmed Commit 타임아웃 기능이 동작하여 자동으로 **롤백**을 수행한다.

#### 한줄 요약

- Candidate 설정 델타 적용과 Confirmed Commit 기반 롤백 메커니즘을 결합한 안정적 자동화 배포 프로세스 준수.

## Ⅴ. 종류 및 비교

| 판단 기준 | NETCONF | RESTCONF | CLI 자동화 (Paramiko/Netmiko) |
|:---|:---|:---|:---|
| **적용 기준** | 트랜잭션, 원자성(Atomicity), 확정/롤백 보장이 최우선일 때 | 웹 대시보드 연동, 경량 REST API 활용이 최우선일 때 | 오픈 API 미지원 레거시 장비 관리가 불가피할 때 |
| **핵심 프로토콜** | SSH 기반 **XML-RPC** | HTTP/HTTPS 기반 **JSON/XML** | SSH 기반 비구조화 문자열 스트림 파싱 |
| **데이터 모델** | **YANG 모델** 완벽 지원 | **YANG 모델** 완벽 지원 | 불분명 (RegEx 파싱 필요) |
| **트랜잭션 관리** | Candidate 저장소, Commit/Rollback, Lock 지원 | 부분적 지원 (HTTP PUT/PATCH) | 미지원 (오류 발생 시 부분 적용 위험) |
| **주요 한계** | 장비별 **기능 광고** 차이, 상대적으로 높은 학습 곡선 | 트랜잭션 원자성 기능 일부 제약 | 장비 OS 업데이트 시 파싱 스크립트 파손 위험 |

> 요약: 고신뢰성 트랜잭션 및 대규모 백본 관리에는 **NETCONF**, 웹 연계 및 MSA 구조에는 **RESTCONF**, 레거시 인프라 수용에는 **CLI 파싱**을 선택한다.

#### 한줄 요약

- NETCONF의 트랜잭션 안정성과 RESTCONF의 웹 연동 편의성을 고려한 관리 프로토콜 선정 모델 비교.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **템플릿(Template)**: Jinja2 등의 엔진을 활용하여 SoT 변수 데이터를 장비별 표준 구문으로 동적 변환해주는 코드 파일이다.
- **도달성(Reachability)**: 핑(ICMP) 또는 BGP/OSPF 라우팅 테이블 참조를 통해 목적지 노드 간 서비스 패킷 전송이 가능한 상태이다.
- **텔레메트리(Telemetry)**: SNMP의 주기적 푸시 방식 한계를 극복하여 이벤트 기반으로 장비 내부 지표를 실시간 스트리밍하는 관측 기술이다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **설정 불일치 장애** | 엔지니어의 임의 CLI 명령 입력으로 인한 SoT 간격 발생 | 주기적 **설정 드리프트** 자동 감지 및 SoT 자동 동기화 | 인프라 설정 정본 유지 및 휴먼 에러 원천 차단 |
| **대규모 변경 실패** | 동일 오류 코드가 플레이북을 통해 전 장비로 전파 | Jinja2 **템플릿** 및 카나리(Canary) 단계별 배포 적용 | 서비스 장애 전파 범위(Blast Radius) 최소화 |
| **스크립트 깨짐** | 장비 펌웨어 업데이트 후 CLI 출력 포맷 변경 | **YANG 모델** 및 **NETCONF/RESTCONF**로 전면 전환 | 폼웨어 변경과 무관한 안정적 자동화 파이프라인 유지 |
| **은밀한 라우팅 장애** | 설정 적용은 정상이나 BGP 경로 미수렴 발생 | Confirmed Commit 및 **텔레메트리** 기반 **도달성** 실시간 검증 | 장애 발생 시 자동 타임아웃 롤백을 통한 복구 시간(MTTR) 단축 |

#### 한줄 요약

- 카나리 배포 전략과 Telemetry 연동 롤백 메커니즘을 적용한 네트워크 자동화 운영 리스크 제어 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **자동화 배포 범위(Automation Deployment Scope)**: 변경 위험도에 따라 카나리 그룹, 랙 단위, 데이터센터 단위로 자동화 적용 대상을 단계별로 획정하는 전략적 적용 범위이다.

</details>

- **자동화 배포 범위** 설정 시 SoT 데이터베이스 수립과 YANG 데이터 모델 정립을 선행하고, Confirmed Commit 기반 롤백 메커니즘을 통합 구축하는 지능형 네트워크 자동화 체계 적용.

#### 한줄 요약

- 선언형 IaC 관리와 YANG 프로토콜 기반 자동화 파이프라인을 활용한 자율 운용 네트워크 구축 체계 적용.
