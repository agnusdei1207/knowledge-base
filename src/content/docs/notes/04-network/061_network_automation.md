---
sidebar:
  order: 61
  label: "061. 네트워크 자동화"
  badge:
    text: "미출 · 50%"
    variant: note
title: "프로그래머블 네트워크 운영 자동화 : NetDevOps (Network Automation)"
date: "2026-08-26T13:48:42+09:00"
tags:
  - "notes-network"
weight: 61
extra:
  question_no: "61"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "진실의 원천(SoT), YANG 데이터 모델, NETCONF/RESTCONF 트랜잭션, 멱등성 및 자동 롤백"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Network Automation (네트워크 자동화)**: 수동 CLI 구성을 배제하고 IaC와 표준 API로 네트워크 프로비저닝과 검증을 자동화하는 운영 체계.
- **Source of Truth (진실의 원천, SoT)**: IP, VLAN, 라우팅 정책 등 네트워크의 목표 구성 상태를 단일하게 정의 보관하는 Git/NetBox 저장소.

</details>

- 정의/개념: **YANG·NETCONF·RESTCONF·Ansible**로 장비 설정을 코드화한 NetDevOps
- 배경/필요성: 장비별 수동 CLI 입력에 따른 **휴먼 에러 빈발, 대규모 망 설정 변경 시 수일의 지연 및 트랜잭션/자동 롤백 불가**

#### 한줄 요약
- Git 기반 SoT와 NETCONF/YANG 트랜잭션을 통해 무중단 자동 프로비저닝 및 자동 롤백을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Idempotency (멱등성)**: 동일한 자동화 스크립트를 여러 번 반복 실행하더라도 네트워크 장비 상태가 항상 목표 상태와 동일하게 유지되는 특성.
- **YANG Data Model**: 장비 설정 항목의 데이터 타입과 유효성 검증 규칙을 구조화하여 정의하는 IETF 표준 모델링 언어 (RFC 6020/7950).

</details>

- **진실의 원천(SoT) 기반 선언적 관리**: Git 저장소의 코드를 단일 기준값으로 삼아 인프라 드리프트(Drift) 원천 차단
- **트랜잭션 ACID 및 자동 롤백**: 설정 오류 또는 통신 단절 시 **Confirmed Commit 기능을 통한 자동 롤백(Rollback)**
- **구조화된 표준 데이터 모델(YANG)**: 벤더별 상이한 CLI 텍스트 파싱을 탈피하여 **NETCONF/RESTCONF 표준 API로 통합 제어**

#### 한줄 요약
- SoT 선언적 관리, YANG 표준 데이터 모델링, Confirmed Commit 기반 트랜잭션 및 자동 롤백을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NETCONF vs RESTCONF**: SSH 상에서 XML RPC로 트랜잭션을 제어하는 NETCONF(RFC 6241)와 HTTPS 상에서 JSON/XML로 조작하는 경량 RESTCONF(RFC 8040).

</details>

```text
[NetDevOps 네트워크 자동화 파이프라인 및 아키텍처]
|-- 진실의 원천 (목표 구성 상태)
|-- 자동화 오케스트레이터 (멱등 배포)
|-- YANG 데이터 모델 (구조·검증 규칙)
|-- NETCONF (트랜잭션 제어)
`-- RESTCONF (RESTful 제어)
```

선의 의미: Git의 SoT 코드가 Ansible 엔진을 거쳐 표준 프로토콜(NETCONF/RESTCONF)로 이종 장비의 저장소 파이프라인에 안전하게 주입되는 구조

| 구성요소 | 책임 |
|:---|:---|
| 진실의 원천 | IP·VLAN·라우팅의 **단일 목표 상태 유지** |
| 자동화 오케스트레이터 | 장비 설정의 **멱등 배포** |
| YANG 데이터 모델 | 자료형·계층·**유효성 규칙 정의** |
| NETCONF | Candidate·Running의 **트랜잭션 제어** |
| RESTCONF | YANG 모델의 **RESTful CRUD 제공** |

#### 한줄 요약
- SoT, 자동화 엔진, YANG 데이터 모델, NETCONF/RESTCONF 프로토콜이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Confirmed Commit**: 장비에 변경 설정을 적용한 후 지정된 타임아웃(예: 120초) 내에 최종 확인(Confirm)이 없으면 자동으로 이전 설정으로 롤백하는 안전장치.

</details>

```text
NetDevOps Confirmed Commit 및 자동 롤백 파이프라인
        │
   [코드 작성 및 PR 생성] 엔지니어가 Git에 구성 코드(YAML/YANG) 커밋 및 PR 생성
        │
   [CI 사전 검증] YANG 린팅 및 가상 네트워크(Containerlab) 시뮬레이션 자동 테스트
        │
   [후보 저장소 전송] Ansible이 NETCONF로 대상 장비의 Candidate Datastore에 주입
        │
   [Confirmed Commit 실행] `commit confirmed 120` 명령으로 120초 동안 헬스체크 수행
        │
   ├─ [정상 헬스체크 통과] ➔ 최종 `commit` 확정 ➔ 배포 성공 완료
   ▼
[단선/장애 발생] ➔ 120초 타임아웃 만료 시 장비가 이전 정상 설정으로 자동 롤백
```

#### 한줄 요약
- Git PR 생성 → CI 사전 검증 → Candidate 설정 적재 → Confirmed Commit 검증 → 실패 시 자동 롤백 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Screen Scraping (CLI 파싱)**: SSH 콘솔 문자열을 정규표현식으로 파싱하여 장비를 제어하는 고전적 비구조화 방식.

</details>

| 비교 항목 | NETCONF (IETF RFC 6241) | RESTCONF (IETF RFC 8040) | 레거시 CLI 파싱 (Screen Scraping) |
|:---|:---|:---|:---|
| 전송 계층 / 포맷 | **SSH (TCP 830) / XML** | **HTTPS (TCP 443) / JSON, XML** | SSH / 비구조적 순수 텍스트 |
| 데이터 모델링 | **YANG 데이터 모델 필수** | **YANG 데이터 모델 필수** | 모델 부재 (제조사 독점 CLI 구문) |
| 트랜잭션 지원 | **완전 지원 (Candidate/Rollback)**| 부분 지원 (HTTP 상태 코드 의존)| 미지원 (오류 발생 시 부분 적용 방치)|
| 보안 및 인증 | SSH 공개키/패스워드 인증 | HTTPS TLS + OAuth/토큰 인증 | SSH 쉘 계정 인증 |
| 주요 적용 영역 | **코어 백본, 미션 크리티컬 망** | **웹 대시보드 연동, 클라우드 연동** | API 미지원 레거시 장비 수동 제어 |

#### 한줄 요약
- NETCONF는 고신뢰 트랜잭션 백본 제어용, RESTCONF는 경량 웹 API 연동용, CLI 파싱은 레거시용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Blast Radius (폭발 반경)**: 단일 설정 오류나 자동화 버그가 발생했을 때 장애가 전파되는 물리적/논리적 영향 범위.
- **Canary Deployment (카나리 배포)**: 전체 장비 중 1~5%의 시범 노드에 설정을 선제 적용하여 검증 후 단계적 확대 배포하는 전략.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자동화 스크립트 오작동으로 인한 대규모 장비 동시 셧다운 | **`카나리(Canary) 단계별 배포` 및 배치 단위 순차 롤아웃** | 오류 시 영향 범위 국소화 및 전면 장애 방지 |
| 장비 펌웨어 업그레이드 시 CLI 구문 변경으로 스크립트 전면 실패 | 비구조적 CLI 파싱을 배제하고 **`표준 YANG/NETCONF`로 전환** | 장비 OS 변경에 무관한 데이터 모델 정합성 확보 |
| 설정 적용 후 라우팅 고립으로 인한 원격 접속 단절 및 장애 방치 | **`Confirmed Commit (자동 타임아웃 롤백)` 기능 의무화** | 통신 단절 시 자동 이전 설정 복구 및 원격 관리 유지 |
| Git 저장소와 실제 장비 설정 간의 불일치(**Configuration Drift**) | **주기적 `Drift Detection 배치 잡` 및 자동 동기화 트리거** | SoT와 실제 인프라 간의 100% 정합성 유지 |

#### 한줄 요약
- 카나리 배포, YANG/NETCONF 표준화, Confirmed Commit, Drift 감지 배치로 운영한다.

## Ⅶ. 결론

- 표준 모델 장비는 **NETCONF·RESTCONF**, 고위험 변경은 **Confirmed Commit·Canary**

#### 한줄 요약
- SoT와 NETCONF/YANG 및 Confirmed Commit을 결합하여 고신뢰 네트워크 운영 자동화를 실현한다.
