---
sidebar:
  order: 61
  label: "061. 네트워크 자동화 - Ansible•RESTCONF•NETCONF (Network Automation)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "네트워크 자동화 - Ansible•RESTCONF•NETCONF (Network Automation)"
date: "2026-08-13T16:14:00+09:00"
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

<details><summary>용어 설명</summary>

- **네트워크 자동화(Network Automation)**: 네트워크 목표 상태를 선언적 모델과 코드로 정의하고, 파이프라인으로 검증·배포·복구하는 자율 운영 인프라 체계.
- **진실의 원천(SoT, Source of Truth)**: IP, VLAN, 보안 정책 등 네트워크 목표 상태(Intent)를 관리하는 단일 기준 데이터 저장소.
- **명령줄 인터페이스(CLI, Command-Line Interface)**: 장비별 전용 명령과 비구조화(Unstructured) 문자열 기반 수동 조작 방식.
- **응용 프로그래밍 인터페이스(API, Application Programming Interface)**: JSON/XML 등 구조화 데이터 스키마 기반 네트워크 설정 및 상태 제어 인터페이스.

</details>

- **개념**: **네트워크 자동화**는 **진실의 원천** 기반 목표 상태를 **YANG(Yet Another Next Generation)** 데이터 모델 및 코드(IaC, Infrastructure as Code)로 변환, 수동 개입 없이 검증·배포·복구하는 자율 운영 프로토콜 체계.
- **필요성**: 장비별 수동 **CLI**는 사람의 실수(Human Error), 설정 파편화, 감사 누락을 유발하므로 **API** 기반 프로그래밍 가능 네트워크(Programmable Network) 전환 필수.

#### 한줄 요약
- 선언적 IaC 및 CI/CD 자동화 파이프라인 체계 적용.
## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **설정 드리프트(Configuration Drift)**: 장비 설정이 SoT 목표 상태에서 이탈하여 임의 변경된 현상.
- **멱등성(Idempotency)**: 자동화 스크립트 반복 실행 시 항상 동일한 결과 상태를 보장하는 성질.
- **지속적 통합(CI, Continuous Integration)**: 코드 변경 시 린팅(Linting), YANG 검증, 테스트를 자동 수행하는 메커니즘.
- **YANG 모델(YANG Data Model)**: NETCONF/RESTCONF의 설정·상태 계층 구조와 자료형을 정의하는 모델링 언어(RFC 6020/7950).

</details>

- **설정 드리프트** 탐지로 실운영 상태와 **SoT** 정본 간 갭을 자동 복구.
- **YANG 모델** 및 **CI** 검증 단계로 배포 전 구문 오류(Syntax Error)와 정책 충돌 선제 차단.
- **멱등성** 보장으로 플레이북 재실행 시 델타(Diff)만 부분 적용하여 연속성 유지.

#### 한줄 요약
- YANG 모델 기반 구조화와 멱등성 보장을 통한 설정 드리프트 차단 관리 원칙 준수.
## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NETCONF(Network Configuration Protocol)**: YANG 기반 데이터를 SSH 상의 XML 인코딩 RPC로 조회·수정하는 IETF 표준.
- **RPC(Remote Procedure Call)**: 클라이언트가 원격 제어 기능을 로컬 함수처럼 호출하는 통신 메커니즘.
- **RESTCONF(REST Configuration Protocol)**: HTTP/1.1~2 기반 JSON/XML 활용 YANG 자원 조작 경량 RESTful API.
- **HTTP(Hypertext Transfer Protocol)**: GET/POST/PUT/DELETE 메서드로 네트워크 관리 자원을 조작하는 웹 표준.
- **JSON(JavaScript Object Notation)**: RESTCONF에서 메시지 구조를 지원하는 경량 데이터 교환 형식.
- **XML(Extensible Markup Language)**: NETCONF 표준 페이로드로 사용되는 계층적 표준 태그 언어.
- **앤서블(Ansible)**: SSH/NETCONF 접속으로 이종 장비에 선언형 플레이북(Playbook)을 적용하는 에이전트리스 오케스트레이션 도구.

</details>

- **NETCONF**는 XML 인코딩 **RPC**와 **YANG**을 사용하고, **RESTCONF**는 HTTP와 JSON/XML로 웹 연동성 제공.
- **Ansible**은 에이전트 없이 **SoT** 변수를 바인딩하여 이종 장비 설정을 자동 동기화.

```text
네트워크 자동화 아키텍처
├─ 진실의 원천(SoT)
├─ Git 및 CI/CD
├─ Ansible
├─ YANG 및 API
└─ Network Devices
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **진실의 원천** | IPAM/DCIM 연동을 통한 목표 설정 정본 관리 |
| **Git 및 CI/CD** | IaC 코드 버전 관리, 구문/YANG 검증 및 이력 관리 |
| **Ansible** | Playbook 기반 장비 배포 및 의존성 조율 |
| **YANG 및 API** | 프로토콜 표준 기반 트랜잭션 및 설정 조작 |
| **Network Devices** | 후보 설정(Candidate) 검증 후 주설정(Running) 확정 |

#### 한줄 요약
- SoT 정본 관리, CI/CD 파이프라인, 표준 API 연계를 통한 전주기 오케스트레이션 아키텍처 구현 필수.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **후보 설정(Candidate Config)**: 반영 전 변경 사항을 임시 저장하여 검증 및 롤백을 준비하는 공간.
- **기능 광고(Capability Advertisement)**: NETCONF 세션 수립 시 지원 YANG 모듈 및 확장 기능을 알리는 절차.
- **롤백(Rollback)**: 배포 실패 시 이전 정상 상태로 즉시 복구하는 기능.
- **Git**: 설정 코드 변경 이력 관리, 리뷰 및 파이프라인 트리거 담당 버전 관리 시스템.
- **사전 검증(Pre-validation)**: 스키마 타당성, 정책 충돌을 배포 전 시뮬레이터에서 선제 검사하는 단계.
- **승인 변경 전달(Change Delivery)**: 코드 승인을 받은 검증 코드만 프로덕션 엔진으로 이관하는 단계.
- **설정 차이 배포(Diff-based Provisioning)**: 목표 상태와 현재 상태의 델타(Diff) 값만 산출하여 배포하는 단계.
- **텔레메트리(Telemetry)**: 변경 후 실제 라우팅/인터페이스 상태를 이벤트 기반으로 실시간 관측하는 단계.
- **실패 시 복구(Rollback on Failure)**: 점검 실패 시 자동 타임아웃 롤백을 발동하는 회복 단계.

</details>

```text
목표 상태 변경 요청
        │
        ▼
1. 사전 검증 (문법 및 YANG 스키마 검증)
        ├─ [실패] 변경 차단
        └─ [통과]
            │
            ▼
2. 승인 변경 전달 (파이프라인 이관)
            │
            ▼
3. 설정 차이 배포 (NETCONF 후보 설정 수정)
            │
            ▼
4. 실제 상태 검증 (커밋 및 텔레메트리 점검)
            ├─ [성공] 설정 확정
            └─ [실패] 5. 실패 시 자동 복구
                               │
                               ▼
                          이전 상태로 롤백
```

### 동작 원리

1. **사전 검증**: 코드 제출 시 **기능 광고** 기반 YANG 스키마 유효성 및 정책 선제 검사.
2. **승인 변경 전달**: **Git** PR 승인 코드만 Ansible로 전달.
3. **설정 차이 배포**: **NETCONF** Edit-config로 **후보 설정**에 델타 적용.
4. **실제 상태 검증**: Commit 직후 **텔레메트리** 지표로 수렴 여부 관측.
5. **실패 시 복구**: Confirmed Commit 타임아웃으로 자동 **롤백** 수행.

#### 한줄 요약
- Candidate 설정 델타 적용 및 Confirmed Commit 기반 롤백 메커니즘 준수.
## Ⅴ. 종류 및 비교

| 판단 기준 | NETCONF | RESTCONF | CLI 자동화 (Paramiko/Netmiko) |
|:---|:---|:---|:---|
| **적용 기준** | 트랜잭션, 원자성(Atomicity), 커밋/롤백 보장이 최우선일 때 | 웹 대시보드 연동, 경량 REST API 활용이 최우선일 때 | 오픈 API 미지원 레거시 장비 관리가 불가피할 때 |
| **핵심 프로토콜** | SSH 기반 XML 인코딩 **RPC** | HTTP/HTTPS 기반 **JSON/XML** | SSH 기반 비구조화 문자열 스트림 파싱 |
| **데이터 모델** | **YANG 모델** 지원 | **YANG 모델** 지원 | 미지원 (정규표현식 파싱 필요) |
| **트랜잭션 관리** | Candidate 저장소, Commit/Rollback, Lock 지원 | 부분 지원 (HTTP PUT/PATCH) | 미지원 (오류 발생 시 부분 적용 위험) |
| **주요 한계** | 장비별 **기능 광고** 차이, 높은 학습 곡선 | 트랜잭션 원자성 기능 일부 제약 | 장비 OS 업데이트 시 파싱 스크립트 오작동 위험 |

> 요약: 고신뢰성에는 **NETCONF**, 웹 연계에는 **RESTCONF**, 레거시 인프라에는 **CLI 파싱** 적용.

#### 한줄 요약

- NETCONF의 트랜잭션 안정성과 RESTCONF의 웹 연동 편의성을 고려한 관리 프로토콜 선정 모델 비교.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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
- 카나리 배포 전략과 Telemetry 연동 롤백 메커니즘을 적용한 운영 리스크 제어 체계 구축.
## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **자동화 배포 범위(Automation Deployment Scope)**: 위험도에 따라 카나리 그룹, 랙, 데이터센터 단위로 자동화 적용 대상을 단계별 획정하는 전략적 범위.

</details>

- 트랜잭션 변경은 **NETCONF**, 웹 연동은 **RESTCONF** 선택.

#### 한줄 요약
- 선언형 IaC 및 YANG 기반 자동화 파이프라인 활용 자율 운용 네트워크 구축 체계 적용.
