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

- **네트워크 자동화(Network Automation)**: 목표 네트워크 상태를 선언적 모델과 코드로 정의하고 자동 파이프라인으로 검증•배포•복구하는 가상화 인프라 자율 운영 체계.
- **진실의 원천(Source of Truth, SoT)**: IP 주소, VLAN 토폴로지, 보안 정책의 목표 선언(Intent) 상태를 유일한 단일 기준(Single Source of Truth)으로 관리하는 데이터 저장소.
- **명령줄 인터페이스(Command-Line Interface, CLI)**: 장비별 전용 텍스트 명령 및 비구조화(Unstructured) 문자열 기반의 수동 조작 방식.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: JSON/XML 포맷의 구조화 데이터 스키마 기반 네트워크 설정 및 상태 프로그래밍 제어 인터페이스.

</details>

- 정의/개념: **네트워크 자동화(Network Automation)**는 **진실의 원천(Source of Truth, SoT)**에 정의된 목표 망 상태를 YANG 데이터 모델 및 코드(IaC)로 변환하여 수동 개입 없이 검증•배포•복구하는 자율 운영 프로토콜 체계.
- 배경/필요성: 장비별 수동 **CLI** 접속 방식은 사람의 실수(Human Error), 설정 파편화, 감사 누락을 유발하므로 **API** 기반 프로그래밍 가능 네트워크(Programmable Network) 전환 필수.

#### 한줄 요약

- 선언적 코드로 네트워크 목표 상태를 정의하고 CI/CD 파이프라인으로 검증 및 배포하는 자동화 체계 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **설정 드리프트(Configuration Drift)**: 실운영 장비 설정이 진실의 원천(SoT)에 정의된 목표 상태에서 이탈하여 임의 변경된 현상.
- **멱등성(Idempotency)**: 동일한 자동화 스크립트/플레이북을 반복 실행해도 추가 부작용 없이 항상 동일한 목표 상태를 유지하는 성질.
- **지속적 통합(Continuous Integration, CI)**: 코드 변경 시 구문 검사(Linting), YANG 스키마 검증, 시뮬레이션 테스트를 자동 수행하는 메커니즘.
- **YANG 모델(YANG Data Model)**: NETCONF/RESTCONF 프로토콜의 네트워크 설정 및 상태 데이터 계층 구조, 자료형, 제약 조건을 정의하는 데이터 모델링 언어(RFC 6020/7950).

</details>

- **설정 드리프트(Configuration Drift)** 탐지를 통해 실운영 상태와 **SoT** 정본 간 갭을 자동 감시 및 복구.
- **YANG 모델** 기반 구조화 데이터 및 **CI** 검증 단계를 도입하여 배포 전 구문 오류(Syntax Error) 및 정책 충돌 선제 차단.
- **멱등성(Idempotency)** 보장으로 플레이북 재실행 시 변경분(Diff)만 부분 적용하여 서비스 연속성 유지.

#### 한줄 요약

- YANG 모델 기반 구조화 스키마와 멱등성 보장으로 설정 드리프트를 차단하는 선언적 네트워크 관리 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **네트워크 설정 프로토콜(Network Configuration Protocol, NETCONF)**: YANG 모델 기반 데이터를 SSH 상의 XML-RPC 통신으로 조회•수정하고 커밋/롤백 트랜잭션을 지원하는 IETF 표준 프로토콜.
- **원격 프로시저 호출(Remote Procedure Call, RPC)**: 클라이언트가 원격 장비 제어 기능을 로컬 함수처럼 호출하는 통신 메커니즘.
- **REST 설정 프로토콜(REST Configuration Protocol, RESTCONF)**: HTTP/1.1 및 HTTP/2 프로토콜 기반으로 JSON/XML 포맷을 활용하여 YANG 자원을 조작하는 경량 RESTful API 프로토콜.
- **하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**: GET, POST, PUT, DELETE 메서드로 네트워크 관리 자원을 조작하는 웹 표준 프로토콜.
- **자바스크립트 객체 표기법(JavaScript Object Notation, JSON)**: 경량의 텍스트 기반 데이터 교환 형식으로 RESTCONF 메시지 구조 지원.
- **확장성 마크업 언어(Extensible Markup Language, XML)**: 계층적 데이터를 정의하는 표준 태그 언어로 NETCONF 표준 페이로드로 사용.
- **앤서블(Ansible)**: 에이전트리스(Agentless) 방식으로 SSH/NETCONF 접속을 통해 대상 장비에 선언형 플레이북(Playbook)을 동적 적용하는 오케스트레이션 도구.

</details>

- **NETCONF**는 **XML-RPC** 및 **YANG 모델**을 활용해 트랜잭션(Edit-config, Commit)을 보장하며, **RESTCONF**는 **HTTP** 메서드와 **JSON** 포맷 기반으로 웹 연동성을 제공.
- **Ansible**은 에이전트 없이 **SoT** 변수를 바인딩하여 이종 벤더 장비 설정을 자동 동기화.

```text
네트워크 자동화 구조 (Network Automation Architecture)
├─ 단일 진실 원천 (NetBox / Nautobot)
├─ 깃 기반 지속적 통합/배포 파이프라인 (Git, GitHub Actions, GitLab CI)
├─ 자동화 조율 엔진 (Ansible Engine, NSO)
├─ 통신 프로토콜 및 데이터 모델 (NETCONF / RESTCONF / YANG)
└─ 다중 벤더 네트워크 장비 (스위치 / 라우터)
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **진실의 원천(Source of Truth, SoT)** | IPAM/DCIM 연동을 통한 목표 IP, VLAN, 인터페이스 구성 정본 관리 |
| **Git 및 CI/CD 파이프라인** | IaC 코드 버전 관리, Syntax/YANG 검증 및 승인 이력 관리 |
| **앤서블 오케스트레이터(Ansible Orchestration)** | Playbook 기반 다중 벤더 장비 배포 순서 및 의존성 동적 조율 |
| **YANG 및 관리 API** | NETCONF/RESTCONF 프로토콜 표준 기반 트랜잭션 처리 및 설정 조작 |
| **네트워크 장비(Network Devices)** | 후보 설정(Candidate) 검증 후 주설정(Running) 확정 및 텔레메트리 수집 |

#### 한줄 요약

- SoT 정본 관리, Git/Ansible 파이프라인, NETCONF/RESTCONF 표준 API 연계를 통한 전주기 오케스트레이션 아키텍처 구현 필수.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **후보 설정(Candidate Configuration)**: 실행 중 설정(Running Config) 반영 전 변경 사항을 임시 저장하여 구문 검증 및 롤백을 준비하는 공간.
- **기능 광고(Capability Advertisement)**: NETCONF 세션 수립 시 장비의 지원 YANG 모듈 및 확장 기능을 상대에게 알리는 절차.
- **롤백(Rollback)**: 배포 실패 또는 네트워크 도달성 상실 시 이전 검증 정상 설정 상태로 즉시 복구하는 기능.
- **깃(Git)**: 설정 코드 변경 이력 관리, 코드 리뷰(Pull Request) 및 자동화 파이프라인 트리거를 담당하는 버전 관리 시스템.
- **사전 검증(Pre-validation)**: 스키마 타당성, IP 중복성, 정책 충돌을 배포 전 시뮬레이터에서 선제 검사하는 단계.
- **승인 변경 전달(Approved Change Delivery)**: 코드 리뷰 승인을 받은 검증 코드만 프로덕션 자동화 엔진으로 이관하는 단계.
- **설정 차이 배포(Diff-based Provisioning)**: 목표 상태와 현 상태의 델타(Diff) 값만 산출하여 Candidate 저장소에 주입하는 단계.
- **실체 상태 보고(State Reporting)**: 변경 후 실제 라우팅 테이블 및 인터페이스 상태를 텔레메트리로 관측하는 단계.
- **검증 실패 시 롤백(Rollback on Validation Failure)**: 건강 상태 점검 실패 시 자동 타임아웃 롤백을 발동하는 회복 단계.

</details>

```text
목표 상태 변경 요청 (코드 제출 및 변경 요청)
        │
        ▼
1. 사전 검증 (문법 및 YANG 스키마 검증)
        ├─ [실패] 변경 차단 및 피드백
        └─ [통과]
            │
            ▼
2. 승인 변경 전달 (파이프라인 이관)
            │
            ▼
3. 설정 차이 배포 (NETCONF 후보 설정 수정)
            │
            ▼
4. 실제 상태 검증 (커밋 및 텔레메트리 건강 점검)
            ├─ [성공] 실행 설정 확정 및 파이프라인 완료
            └─ [실패] 5. 검증 실패 시 자동 복구
                              │
                              ▼
                         이전 정상 상태 복구 (확정 커밋 롤백)
```

### 동작 원리

1. **사전 검증**: 코드 제출 시 **기능 광고(Capability Advertisement)** 정보 기반으로 YANG 스키마 유효성 및 정책 도달성을 사전 검사.
2. **승인 변경 전달**: **Git** PR 승인을 거친 코드만 Ansible 오케스트레이터로 전달.
3. **설정 차이 배포**: **NETCONF** 프로토콜의 Edit-config 명령을 호출하여 **후보 설정(Candidate Configuration)**에 델타 적용.
4. **실체 상태 보고**: Commit 적용 직후 **텔레메트리(Telemetry)** 지표로 라우팅 수렴 여부 관측.
5. **검증 실패 시 롤백**: 수렴 실패 시 Confirmed Commit 타임아웃 기능 작동으로 자동 **롤백(Rollback)** 수행.

#### 한줄 요약

- Candidate 설정 델타 적용과 Confirmed Commit 기반 롤백 메커니즘을 결합한 안정적 자동화 배포 프로세스 준수.

## Ⅴ. 종류 및 비교

| 판단 기준 | NETCONF | RESTCONF | CLI 자동화 (Paramiko/Netmiko) |
|:---|:---|:---|:---|
| **적용 기준** | 트랜잭션, 원자성(Atomicity), 커밋/롤백 보장이 최우선일 때 | 웹 대시보드 연동, 경량 REST API 활용이 최우선일 때 | 오픈 API 미지원 레거시 장비 관리가 불가피할 때 |
| **핵심 프로토콜** | SSH 기반 **XML-RPC** | HTTP/HTTPS 기반 **JSON/XML** | SSH 기반 비구조화 문자열 스트림 파싱 |
| **데이터 모델** | **YANG 모델** 지원 | **YANG 모델** 지원 | 미지원 (정규표현식 파싱 필요) |
| **트랜잭션 관리** | Candidate 저장소, Commit/Rollback, Lock 지원 | 부분 지원 (HTTP PUT/PATCH) | 미지원 (오류 발생 시 부분 적용 위험) |
| **주요 한계** | 장비별 **기능 광고** 차이, 높은 학습 곡선 | 트랜잭션 원자성 기능 일부 제약 | 장비 OS 업데이트 시 파싱 스크립트 오작동 위험 |

> 요약: 고신뢰성 트랜잭션 및 백본 관리에는 **NETCONF**, 웹 연계 및 MSA 구조에는 **RESTCONF**, 레거시 인프라 수용에는 **CLI 파싱** 적용.

#### 한줄 요약

- NETCONF의 트랜잭션 안정성과 RESTCONF의 웹 연동 편의성을 고려한 관리 프로토콜 선정 모델 비교.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **템플릿(Template)**: Jinja2 등의 엔진으로 SoT 변수를 장비별 표준 구문으로 동적 변환하는 코드 파일.
- **도달성(Reachability)**: ICMP 또는 라우팅 테이블 참조를 통해 목적지 노드 간 패킷 전송이 가능한 상태.
- **텔레메트리(Telemetry)**: 이벤트 기반으로 장비 내부 지표를 실시간 스트리밍하는 관측 기술.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **설정 불일치 장애** | 임의 CLI 명령 입력으로 인한 SoT 갭 발생 | 주기적 **설정 드리프트** 자동 감지 및 SoT 자동 동기화 | 인프라 설정 정본 유지 및 휴먼 에러 차단 |
| **대규모 변경 실패** | 동일 오류 코드가 플레이북으로 전 장비 전파 | Jinja2 **템플릿** 및 카나리(Canary) 단계별 배포 적용 | 서비스 장애 전파 범위(Blast Radius) 최소화 |
| **스크립트 오작동** | 장비 펌웨어 업데이트 후 CLI 출력 포맷 변경 | **YANG 모델** 및 **NETCONF/RESTCONF**로 전면 전환 | 펌웨어 변경과 무관한 안정적 자동화 파이프라인 유지 |
| **은밀한 라우팅 장애** | 설정 적용은 정상이나 BGP 경로 미수렴 발생 | Confirmed Commit 및 **텔레메트리** 기반 **도달성** 실시간 검증 | 장애 발생 시 자동 타임아웃 롤백으로 복구 시간(MTTR) 단축 |

#### 한줄 요약

- 카나리 배포 전략과 Telemetry 연동 롤백 메커니즘을 적용한 네트워크 자동화 운영 리스크 제어 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **자동화 배포 범위(Automation Deployment Scope)**: 위험도에 따라 카나리 그룹, 랙, 데이터센터 단위로 자동화 적용 대상을 단계별 획정하는 전략적 범위.

</details>

- **자동화 배포 범위** 설정 시 SoT 데이터베이스 수립과 YANG 데이터 모델 정립을 선행하고, Confirmed Commit 기반 롤백 메커니즘을 통합 구축하는 지능형 네트워크 자동화 체계 적용.

#### 한줄 요약

- 선언형 IaC 관리와 YANG 프로토콜 기반 자동화 파이프라인을 활용한 자율 운용 네트워크 구축 체계 적용.

