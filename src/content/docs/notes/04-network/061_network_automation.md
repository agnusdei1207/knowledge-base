---
sidebar:
  order: 61
  label: "061. 네트워크 자동화 (Network Automation)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "프로그래머블 네트워크 운영 자동화 : NETCONF, RESTCONF, Ansible (Network Automation)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 61
extra:
  question_no: "061"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "진실의 원천(SoT), YANG 데이터 모델, NETCONF/RESTCONF 트랜잭션, 멱등성 및 자동 롤백"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 자동화(Network Automation)**: CLI(Command Line Interface) 기반의 수동 장비 구성을 배제하고, 인프라 코드화(IaC) 툴과 프로그래머블 API를 활용하여 네트워크 프로비저닝, 구성 검증, 텔레메트리 모니터링, 롤백을 자동화하는 소프트웨어 공학적 운영 체계.
- **진실의 원천(Source of Truth, SoT)**: 네트워크의 이상적인 목표 구성 상태(IP 주소, VLAN, 라우팅 정책 등)를 단일하게 정의하여 보관하는 신뢰 저장소(Git, NetBox 등).

</details>

- 정의/개념: 선언적 데이터 모델(**YANG**)과 표준 트랜잭션 프로토콜(**NETCONF/RESTCONF**) 및 오케스트레이션 도구(**Ansible/Terraform**)를 결합하여 이종 네트워크 장비의 설정 생애주기를 코드로 자동 제어하는 **NetDevOps 아키텍처**
- 배경/필요성: 수동 CLI 설정 과정에서 발생하는 인간 실수(Human Error)로 인한 광역 네트워크 장애를 원천 차단하고, 수천 대의 장비 구성을 수 분 내에 일관되게 배포·검증할 요구

#### 한줄 요약
- SoT와 YANG 모델, NETCONF/RESTCONF 및 Ansible을 통해 네트워크 구성을 코드로 자동화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **설정 드리프트(Configuration Drift)**: 진실의 원천(SoT)에 정의된 표준 기준 설정과 실제 운영 중인 네트워크 장비의 활성 설정(Running Config) 사이에 불일치가 발생하는 현상.
- **멱등성(Idempotency)**: 동일한 자동화 스크립트나 API 요청을 여러 번 반복 실행하더라도 네트워크 장비의 최종 상태가 항상 목표 상태와 동일하게 유지되는 성질.

</details>

- **설정 드리프트 자동 탐지 및 자가 치유**: 장비의 실제 상태(Actual State)를 주기적으로 감사하여 SoT의 의도된 상태(Intended State)와 대조하고 차이점 발생 시 자동 원복
- **트랜잭션 원자성(ACID) 및 Confirmed Commit**: 다중 장비 설정 적용 중 오류 발생 시 전체 변경을 이전 안정 상태로 즉시 되돌리는 자동 롤백(Rollback) 지원
- **구조화된 표준 데이터 모델링(YANG)**: 비구조적 텍스트 문자열(CLI) 파싱의 한계를 탈피하여 표준 XML/JSON 데이터 구조 기반의 엄격한 타입 검증 수행

#### 한줄 요약
- 설정 드리프트 자가 치유, 멱등성 보장, 트랜잭션 원자성 기반 자동 롤백을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **YANG(Yet Another Next Generation)**: 네트워크 장비의 구성 데이터(Configuration)와 상태 데이터(State)를 계층적 트리 구조로 모델링하는 IETF 표준 데이터 모델링 언어 (RFC 6020/7950).
- **NETCONF(Network Configuration Protocol)**: SSH 상에서 XML 기반 메시지(RPC)를 송수신하며 원자적 트랜잭션과 롤백을 지원하는 네트워크 관리 프로토콜 (RFC 6241).
- **RESTCONF**: YANG 데이터 모델을 기반으로 HTTP/HTTPS 상에서 JSON/XML 페이로드를 RESTful API 형태로 조작하는 경량 관리 프로토콜 (RFC 8040).

</details>

```text
[ 진실의 원천 (Source of Truth - Git / NetBox) ] ── (표준 구성 선언: YAML/JSON)
                    │
                    ▼ (CI/CD 파이프라인: 구문 검증 및 정책 테스트)
[ 자동화 오케스트레이션 엔진 (Ansible / Python Nornir) ]
                    │
                    ├───────────────────────────────┬───────────────────────────────┐
                    ▼ (NETCONF - SSH / XML)         ▼ (RESTCONF - HTTPS / JSON)     ▼ (gNMI - gRPC)
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│ 이기종 네트워크 인프라 계층 (YANG Data Model 기반 스위치/라우터/방화벽)                     │
│ ├─ Candidate Config (임시 후보 저장소) ──(Commit 검증)──▶ Running Config (실운영 저장소)  │
│ └─ 자동 롤백 엔진 (Confirmed Commit 만료 시 자동 원복)                                    │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Git 저장소의 SoT 코드가 Ansible 엔진을 거쳐 표준 프로토콜(NETCONF/RESTCONF)로 이종 장비의 저장소 파이프라인에 안전하게 주입되는 구조

| 구성요소 | 책임 및 역할 | 프로토콜 / 표준 |
|:---|:---|:---|
| **진실의 원천 (SoT)** | 네트워크의 모든 IP, VLAN, 라우팅 파라미터의 단일 기준값 유지 | Git, NetBox, Nautobot |
| **자동화 엔진** | 플레이북을 실행하여 대상 장비에 순차/병렬로 변경 명령 배포 | Ansible, Nornir, Terraform |
| **데이터 모델 (YANG)** | 장비 설정 항목의 자료형, 계층 구조, 유효성 검증 규칙 정의 | IETF RFC 6020 / 7950 |
| **NETCONF 프로토콜** | SSH 보안 채널 상에서 Candidate/Running 데이터 저장소 트랜잭션 조작 | RFC 6241 (XML RPC) |
| **RESTCONF 프로토콜**| 웹 기반 RESTful CRUD 인터페이스로 YANG 모델 엔드포인트 제어 | RFC 8040 (HTTP JSON) |

#### 한줄 요약
- SoT(Git), Ansible 자동화 엔진, YANG 데이터 모델, NETCONF/RESTCONF 프로토콜이 유기적으로 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **확정 커밋(Confirmed Commit)**: 장비에 변경 설정을 적용한 후 지정된 타임아웃 시간 내에 운영자 또는 자동화 시스템의 최종 확인(Confirm) 신호가 도착하지 않으면, 통신 단절로 간주하고 자동으로 이전 설정으로 롤백하는 안전장치.

</details>

```text
1. 네트워크 엔지니어가 Git 저장소에 구성 코드(YAML/YANG) 커밋 및 Pull Request 생성
            │
            ▼
2. CI 파이프라인에서 YANG 구문 검증(Linting) 및 가상 네트워크(Containerlab) 시뮬레이션
            │
            ▼
3. Ansible이 NETCONF를 통해 대상 장비의 임시 저장소(Candidate Datastore)로 설정 전송
            │
            ▼
4. 장비에 `commit confirmed 120` 명령 실행 ➔ 120초 동안 텔레메트리 헬스체크(Ping/BGP) 수행
            │
            ├─ [헬스체크 정상] ➔ 최종 `commit` 확정 ➔ 배포 성공 완료
            ▼
5. [헬스체크 실패 또는 링크 단절] ➔ 120초 타임아웃 만료 시 장비가 이전 상태로 자동 롤백
```

**동작 원리**

1. **사전 검증**: 코드 병합 전 CI 파이프라인에서 문법 오류 및 정책 충돌 사전 차단
2. **후보 적재**: 실운영(Running) 설정에 직접 쓰지 않고 후보(Candidate) 메모리에 변경 사항 탑재
3. **조건부 커밋**: Confirmed Commit을 실행하여 일시적으로 설정을 활성화하고 네트워크 도달성 계측
4. **폐루프 검증**: 스트리밍 텔레메트리가 BGP 세션 및 패킷 포워딩 정상 상태를 확인하면 변경 영구 확정
5. **무손실 복원**: 라우팅 고립 발생 시 자동 타임아웃 롤백을 통해 원격 관리 채널 및 정상 상태 자동 복구

#### 한줄 요약
- Git PR 생성, CI 사전 검증, Candidate 설정 적재, Confirmed Commit 검증, 실패 시 자동 롤백 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CLI 스크래핑(Screen Scraping)**: SSH 콘솔 문자열을 Expect나 정규표현식(Regex)으로 파싱하여 장비를 제어하는 전통적 비구조화 방식.

</details>

| 비교 항목 | NETCONF (IETF RFC 6241) | RESTCONF (IETF RFC 8040) | 레거시 CLI 파싱 (Screen Scraping) |
|:---|:---|:---|:---|
| **전송 계층 / 포맷** | **SSH (TCP 830) / XML** | **HTTPS (TCP 443) / JSON, XML** | SSH / 비구조적 순수 텍스트(CLI) |
| **데이터 모델링** | **YANG 데이터 모델 필수** | **YANG 데이터 모델 필수** | 모델 부재 (벤더별 독점 CLI 구문) |
| **트랜잭션 지원** | **완전 지원 (Candidate/Rollback)**| 부분 지원 (HTTP 상태 코드 의존) | 미지원 (오류 발생 시 부분 적용 방치) |
| **보안 및 인증** | SSH 공개키/패스워드 인증 | HTTPS TLS + OAuth/기본 인증 | SSH 쉘 인증 |
| **적용 시나리오** | 코어 백본, 미션 크리티컬 네트워크 | 웹 대시보드 연동, 클라우드 오케스트레이션 | API 미지원 레거시 장비 수동 제어 |

#### 한줄 요약
- NETCONF는 고신뢰 트랜잭션 백본 제어용, RESTCONF는 경량 웹 API 연동용, CLI 파싱은 레거시용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **카나리 배포(Canary Deployment)**: 대규모 장비군 중 소수의 시범 노드(1~5%)에 설정을 선제 적용하여 이상 유무를 검증한 후 전체 인프라로 단계적 롤아웃하는 배포 전략.
- **폭발 반경(Blast Radius)**: 단일 설정 오류나 자동화 버그가 발생했을 때 장애가 전파되는 물리적/논리적 영향 범위.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자동화 스크립트 오작동으로 인한 대규모 장비 동시 셧다운 및 폭발 반경 확산 | **카나리(Canary) 단계별 배포** 및 배치 단위 순차 롤아웃 | 단일 오류 시 영향 범위 국소화 및 전면 장애 방지 |
| 장비 펌웨어 버전 업그레이드 시 CLI 구문 변경으로 인한 스크립트 전면 실패 | 비구조적 CLI 파싱을 배제하고 **표준 YANG/NETCONF 인터페이스** 로 전환 | 장비 OS 변경에 무관한 데이터 모델 정합성 및 지속성 확보 |
| 설정 커밋 후 라우팅 고립으로 인한 원격 접속 단절 및 장애 방치 | **Confirmed Commit (자동 타임아웃 롤백)** 기능 의무화 | 통신 단절 시 자동 이전 설정 복구 및 원격 관리성 유지 |

#### 한줄 요약
- 카나리 배포로 장애 반경을 축소하고, YANG/NETCONF로 일관성을 확보하며, Confirmed Commit으로 원격 단절을 방지한다.

## Ⅶ. 결론

- 인프라의 복잡도 증가와 휴먼 에러를 방지하기 위해 **NetDevOps 기반 네트워크 자동화 체계**를 필수 구축하되, 배포 신뢰성을 담보하기 위해 **Git 기반 진실의 원천(SoT)**, **YANG 데이터 모델**, **NETCONF Confirmed Commit 트랜잭션**, **카나리 검증 파이프라인**을 통합 구현하여 제로 다운타임(Zero-Downtime) 자율 운영 네트워크를 완성

#### 한줄 요약
- SoT와 NETCONF/YANG 및 Confirmed Commit을 결합하여 고신뢰 네트워크 자동화를 실현한다.
