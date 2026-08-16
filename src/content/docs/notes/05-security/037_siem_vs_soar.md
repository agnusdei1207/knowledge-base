---
sidebar:
  order: 37
  label: "037. SIEM vs SOAR 비교 (SIEM vs SOAR)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "SIEM vs SOAR 비교 (SIEM vs SOAR)"
date: "2026-08-13T19:06:00+09:00"
tags:
  - "notes-security"
weight: 37
extra:
  question_no: "037"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 직전 비교 기출이라 동일문구 반복은 감점함"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **보안 정보•이벤트 관리(Security Information and Event Management, SIEM)**: 이종 로그를 수집•정규화하고 상관관계 분석을 통해 실시간 탐지 경보를 생성하는 데이터 허브 플랫폼.
- **보안 오케스트레이션•자동화 및 대응(Security Orchestration, Automation and Response, SOAR)**: 보안 도구를 연계하고 표준 플레이북 기반으로 사건 조사, 승인, 차단 조치를 자동화하는 플랫폼.

</details>

- 정의/개념: 탐지 **SIEM**과 대응 **SOAR**의 연계 구조
- 배경/필요성: 단일 솔루션으로는 **탐지-조치 병목** 해소 불가

#### 한줄 요약

- SIEM의 실시간 위협 탐지 경보를 SOAR가 수신하여 표준 플레이북 기반 자동 조치를 집행함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **사건 ID(Incident Correlation ID)**: SIEM의 탐지 경보와 SOAR의 대응 플레이북 티켓을 일대일 연결하는 통합 고유 식별자.
- **폐쇄 루프(Closed-loop Feedback)**: 자동 조치 및 수동 대응 결과를 SIEM 탐지 상관 규칙에 반영하여 탐지 정밀도를 높이는 환류 체계.

</details>

- **SIEM**을 통한 이종 로그 수집, 정규화 및 상관분석 경보 생성.
- **SOAR** 기반의 인텔리전스 정보 보강, 판단 및 플레이북 오케스트레이션 수행.
- 공통 **사건 ID(Incident Correlation ID)** 기반 대응 결과를 **폐쇄 루프**로 환류하여 연속성 확보.

#### 한줄 요약

- 사건 ID 기반 연계와 폐쇄 루프 피드백을 통해 탐지 규칙 정밀도와 대응 적시성을 상호 보완함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인계 계약(Handoff Contract / Interface Spec)**: SIEM과 SOAR 간 사건 ID, 증적 데이터, 위험도, 파싱 필드를 표준 규격으로 상호 정의한 인터페이스 명세.
- **엔드포인트 탐지•대응(Endpoint Detection and Response, EDR)**: 단말 단위의 프로세스 및 네트워크를 제어하여 위협 시스템을 격리하는 기술.
- **신원 제공자(Identity Provider, IdP)**: 중앙 신원 및 계정 인증을 관리하여 위협 계정 자격을 즉시 회수•잠금하는 시스템.

</details>

```text
SIEM•SOAR 연계 구조
├─ SIEM 수집•상관
├─ 인계 계약
├─ SOAR 보강•조치
├─ EDR•IdP
└─ 결과 환류
```

가지의 의미: 탐지•인계•조치•집행과 결과 환류의 정적 책임 구성을 표현.

| 구성요소 | 책임 |
|:---|:---|
| SIEM 수집•상관 | **SIEM**이 원본 로그 기반 경보 및 조사 증적 생성 |
| 인계 계약 | **인계 계약**을 통한 사건 ID•증적•위험도 데이터 표준 전달 |
| SOAR 보강•조치 | **SOAR** 기반 사건 승인, 플레이북 조치 및 복구 수행 |
| EDR•IdP | **EDR** 및 **IdP** 연동 기반 단말 네트워크 격리 및 계정 세션 차단 |
| 결과 환류 | **폐쇄 루프**를 통한 탐지 시나리오 튜닝 및 상관 규칙 보완 |

#### 한줄 요약

- **인계 계약** 명문화로 경보와 조치 이력 추적성 확보

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **실행 증적(Execution Audit Evidence)**: API 호출 성공을 넘어 대상 시스템의 실제 보안 정책 변경이 완결되었음을 증명하는 검증 기록.
- **최소 권한 응용 프로그래밍 인터페이스(Least Privilege API)**: SOAR 조치 연동 시 필요한 최저 수준의 조회•변경 권한만을 부여한 API 호출 방식.
- **로그 상관•위험도 산정(Log Correlation & Risk Scoring)**: 원본 증적 및 자산 맥락 기반 위험도와 조사 우선순위를 계산하는 단계.
- **현재 상태•위협 보강(Current State & Threat Enrichment)**: 타깃 장비의 현재 상태와 위협 인텔리전스를 추가 수집•결합하는 단계.
- **승인•정책 분기(Approval & Policy Branching)**: 비즈니스 영향도 및 가역성에 따라 수동/승인/자동 실행을 결정하는 단계.
- **격리•차단•복구 실행(Containment & Remediation Execution)**: 승인된 플레이북 기반 최소 권한 API를 호출하여 조치를 집행하는 단계.
- **실행 증적•상태 검증(Audit Evidence & State Verification)**: 실제 정책 반영 상태를 검증하고 조치 결과를 SIEM에 환류하는 단계.

</details>

```text
원본 로그 유입
        │
        ▼
1. 로그 상관•위험도 산정
        └─ 사건 ID•탐지 근거 인계
                │
                ▼
2. 현재 상태•위협 보강
        │
        ▼
3. 승인•정책 분기
        ├─ 거부•고위험 ── 수동 대응
        └─ 승인•자동 실행
                │
                ▼
4. 격리•차단•복구 실행
        │
        ▼
5. 실행 증적•상태 검증
        ├─ 실패 ── 재시도•롤백
        └─ 성공 ── SIEM에 검증 결과 환류
```

### 동작 원리

1. **로그 상관•위험도 산정**: 원본 데이터 상관분석 및 위험 심각도 산정.
2. **현재 상태•위협 보강**: 대상 자산 상태 재조회 및 위협 CTI 보강.
3. **승인•정책 분기**: 비즈니스 영향도 기반 실행 모드(무인/승인/수동) 분기.
4. **격리•차단•복구 실행**: **최소 권한 응용 프로그래밍 인터페이스** 기반 제어 명령 호출.
5. **실행 증적•상태 검증**: **실행 증적** 기반 조치 완료 검증 및 SIEM에 환류 데이터 업데이트.

#### 한줄 요약

- 로그 상관분석부터 현황 보강, 정책 분기, 격리 집행 및 실행 증적 검증까지의 관제 프로세스를 연결함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **탐지 근거(Detection Rationale / Evidence)**: 원본 데이터, 정규화 파싱 결과 및 상관분석 시나리오 조건으로 구성된 SIEM의 탐지 입증 자료.
- **대응 수행(Response Execution / Orchestration)**: 승인된 워크플로 및 커넥터를 통해 외부 장비 제어 조치를 완결하는 SOAR의 기능적 책임.

</details>

| 보안 관제 플랫폼 | SIEM | SOAR |
|:---|:---|:---|
| 적용 기준 | **탐지 근거** 필요 시 | 자동 대응 필요 시 |
| 핵심 특징 | **SIEM**의 로그 상관•경보 생성 | **SOAR**의 **대응 수행** |
| 한계 | 로그 품질 저하•오탐 | 오탐 자동화•권한 집중 |

> 요약: SIEM의 데이터 탐지 근거 제공과 SOAR의 프로세스 대응 수행의 상호보완 관계.

#### 한줄 요약

- SIEM의 고품질 데이터 상관분석과 SOAR의 즉각적 대응 오케스트레이션을 상호 유기적으로 결합함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: 정보보호 가이드라인 표준을 제공하는 미국 정부 기관.
- **특별 간행물(Special Publication, SP 800-92)**: 전사 보안 로그 수집, 생성, 정규화, 관리 프로세스에 관한 규정.
- **구조화 정보 표준 발전 기구(Organization for the Advancement of Structured Information Standards, OASIS)**: CACAO 등 오케스트레이션 명세를 수립하는 기구.
- **자동화된 행동 과정 협업(Collaborative Automated Course of Action Operations, CACAO 2.0)**: SOAR 시스템 간 자동 대응 플레이북 교환을 가능케 하는 표준 명세서.
- **EDR 격리(EDR Host Isolation)**: 엔드포인트 agent를 이용하여 감염 시스템의 네트워크 망 통신을 완전 물리/논리 차단하는 보안 조치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 로그 품질•추적성 | **NIST SP 800-92** 적용 | 경보 근거 신뢰성 확보 |
| 플레이북 이식성 | **OASIS CACAO 2.0** 적용 | 대응 절차 상호운용 확보 |
| 오탐 자동 조치 | **사건 ID**•승인•**폐쇄 루프** 환류 | 오조치 확산•책임 공백 방지 |

#### 한줄 요약

- SIEM이 단말의 이상 행위를 이상 로그로 인지하면 SOAR가 분석 승인을 거쳐 EDR 네트워크 격리를 실시간 수행함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **운영 추적성(Operational Traceability)**: 최초 탐지 경보부터 자동 보강, 승인, 조치 집행 및 결과 환류까지의 전 과정이 단일 감사 이력으로 보존되는 속성.

</details>

- **운영 추적성** 확보를 위해 탐지 및 증적 관리는 **SIEM**, 워크플로 자동 대응은 **SOAR**가 담당하고, 공통 **사건 ID** 기반 **폐쇄 루프** 통합 구축.

#### 한줄 요약

- **탐지 근거**는 SIEM, **대응 수행**은 SOAR로 역할 분리
