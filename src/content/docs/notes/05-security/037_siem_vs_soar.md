---
sidebar:
  order: 37
  label: "037. SIEM vs SOAR 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "보안 가시성 탐지와 대응 오케스트레이션의 결합 : SIEM vs SOAR"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 37
extra:
  question_no: "37"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "SIEM(탐지/로그상관/중앙가시성) vs SOAR(대응/플레이북자동화/오케스트레이션), 폐쇄 루프(Closed-Loop) 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SIEM vs SOAR**: 탐지와 전사 로그 상관분석을 담당하는 SIEM(눈과 귀)과 플레이북 기반 API 자동 차단 대응을 담당하는 SOAR(손과 발).
- **Closed-Loop Feedback (폐쇄 루프 환류)**: SOAR의 차단 및 오탐 분석 결과를 다시 SIEM 탐지 룰셋 튜닝에 자동으로 반영하는 선순환 파이프라인.

</details>

- 정의/개념: 탐지 중심 데이터 허브(SIEM)와 실행 중심 오케스트레이터(SOAR)를 **사건 ID 기반 폐쇄 루프로 결합하여 탐지-대응을 초 단위로 통합하는 운영 기술**
- 배경/필요성: SIEM 단독 운용 시 발생하는 **수동 분석·차단 지연(MTTR 수 시간), SOAR 단독 운용 시 원천 로그 및 복합 위협 탐지 트리거 부재**

#### 한줄 요약
- SIEM의 상관 탐지와 SOAR의 플레이북 오케스트레이션을 결합하여 MTTD와 MTTR을 극적으로 단축한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Handoff Contract (인계 계약)**: SIEM이 탐지한 사건 객체를 SOAR가 즉시 플레이북에 바인딩할 수 있도록 표준 JSON 포맷으로 전달하는 데이터 규약.
- **Bi-directional Integration (양방향 연동)**: SIEM 경보가 SOAR 대응을 트리거하고, SOAR 조치 결과가 다시 SIEM 감사 로그로 피드백되는 구조.

</details>

- **상호보완적 역할 분업(Eyes and Hands)**: SIEM은 **전사 빅데이터 상관분석 및 위협 식별, SOAR는 이종 장비 API 차단 및 티켓 자동 처리 집행**
- **무손실 표준 데이터 인계(Handoff Contract)**: 사건 ID, **호스트 IP, 사용자 계정, 원본 증적을 표준 JSON 스키마로 즉시 인계**
- **양방향 폐쇄 루프(Closed-Loop) 최적화**: SOAR의 실제 조치 성공 및 오탐 판정 결과를 **SIEM에 환류하여 탐지 룰셋 자동 정밀 튜닝**

#### 한줄 요약
- 상호보완적 분업(눈과 손발), 무손실 표준 데이터 인계, 양방향 폐쇄 루프 최적화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Incident Correlation ID**: SIEM에서 생성되어 SOAR, 방화벽, ITSM 티켓에 이르기까지 전 추적 과정에서 공유되는 고유 사건 식별자.

</details>

```text
[SIEM 탐지 및 SOAR 자동 대응 폐쇄 루프 아키텍처]
|-- Ingestion & Detection Layer: SIEM (1. 전사 로그 수집, 정규화 상관분석 -> Alert 생성)
`-- Handoff Interface (2. Incident Correlation ID 기반 표준 JSON 사건 전달)
`-- Orchestration & Response Layer: SOAR (Playbook Engine: CTI 보강, Human-in-the-loop)
`-- Action Executors & Closed-Loop Feedback
    |-- Action Execution ──▶ 3. NGFW(C2 차단), EDR(호스트 격리), AD(계정 잠금)
    `-- Feedback Loop ──▶ 4. SIEM 상관분석 룰 튜닝 피드백 및 WORM 증적 저장
```

선의 의미: SIEM이 이종 로그를 분석하여 인시던트를 생성하면 SOAR가 플레이북을 가동해 장비들을 자동 제어하고 그 결과를 SIEM에 환류하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SIEM 탐지 엔진** | 이종 로그 수집, **표준 스키마 정규화, 다차원 상관분석 및 경보 생성** | Detection Core |
| **인계 인터페이스** | SIEM 알람을 **SOAR로 무손실 전달하기 위한 표준 JSON 스키마** | API Contract |
| **SOAR 플레이북 엔진**| 위협 Triage, **CTI 맥락 보강, 이종 API 차단 명령 오케스트레이션** | Response Core |
| **타격 실행 커넥터** | 방화벽, EDR, AD와 연동되어 **실제 격리/차단 명령 집행** | Action Connectors|
| **폐쇄 루프 환류 모듈**| SOAR 조치 결과를 **SIEM 룰셋으로 피드백하여 탐지 정밀도 개선** | Feedback Loop |

#### 한줄 요약
- SIEM 탐지 엔진, 인계 인터페이스, SOAR 플레이북 엔진, 타격 실행 커넥터, 폐쇄 루프 환류 모듈이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SIEM-SOAR 5단계 라이프사이클**: 1. 탐지(Detect) → 2. 인계(Handoff) → 3. 보강 및 승인(Enrich & Approve) → 4. 집행(Execute) → 5. 환류(Feedback).

</details>

```text
SIEM 상관 탐지, JSON 인계, SOAR CTI 보강, API 차단 및 폐쇄 루프 환류 파이프라인
        │
   1. [SIEM 탐지] 방화벽/EDR 로그 상관분석 ➔ "비인가 권한 상승 후 C2 통신" 인시던트 식별
        │
   2. [표준 인계] SIEM이 사건 ID(#1024), IP, 계정, 증적을 JSON으로 SOAR에 전달
        │
   3. [SOAR 보강 및 판정] CTI TIP 플랫폼과 연동하여 대상 C2 IP 평판 자동 조회 ➔ [위험도 Critical 확정]
        │
   4. [오케스트레이션 차단] 플레이북에 따라 EDR API(호스트 격리) 및 NGFW API(C2 차단) 동시 호출
        │
   ▼
5. [상태 검증 및 폐쇄 루프] 차단 적용 증적을 수집하여 ITSM 티켓 종결 및 SIEM 룰 튜닝 반영
```

#### 한줄 요약
- SIEM 상관 탐지 → 표준 JSON 인계 → SOAR CTI 보강 → EDR/방화벽 동시 차단 → 폐쇄 루프 환류 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SIEM (탐지 레이더)** vs **SOAR (자동 대응 타격대)**.

</details>

| 비교 항목 | 보안 정보 및 이벤트 관리 (SIEM) | 보안 오케스트레이션 및 대응 (SOAR) |
|:---|:---|:---|
| **핵심 목적** | **전사 위협 가시성 확보 및 실시간 상관 탐지** | **침해사고 조사 및 대응 조치 무인 자동화** |
| **주요 역할 비유** | **보안 관제 센터의 '눈과 귀' (탐지 레이더)** | **보안 관제 센터의 '손과 발' (자동 대응 타격대)** |
| **데이터 흐름 방향** | **인바운드 중심 (이종 시스템 로그 대량 수집)**| **양방향 (경보 수신 후 이종 장비로 제어 API 송출)**|
| **핵심 기술 컴포넌트** | **파서, 공통 스키마(CEF/ECS), 상관분석 룰** | **플레이북(CACAO), API 커넥터, 상태 머신** |
| **주요 단독 운용 한계**| 수동 대응 병목으로 인한 MTTR 지연 (알람 피로도)| 탐지 트리거 및 원본 빅데이터 증적 부재 |
| **핵심 도입 효과** | **미탐 방지 및 침해 시나리오 실시간 가시화** | **MTTR 90% 이상 단축 및 관제 수작업 오버헤드 제거**|

#### 한줄 요약
- SIEM은 대규모 로그 상관 탐지(눈), SOAR는 이종 장비 API 오케스트레이션 대응(손발)을 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-92 & OASIS CACAO 2.0**: 로그 무결성 수집 표준(NIST SP 800-92)과 상호운용 가능한 보안 플레이북 표준(CACAO 2.0).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SIEM 경보 형식이 비표준화되어 **SOAR 플레이북 파싱 실패 및 파이프라인 단절** | **`CEF/ECS 기반 표준 인계 계약(Handoff Contract) 수립 및 JSON Schema 검증`** | 탐지-대응 간 데이터 인계 성공률 100% 달성 |
| SOAR 조치 결과가 환류되지 않아 **동일 오탐 경보가 SIEM에서 반복 발생하는 비효율** | **사건 ID 기반의 `양방향 폐쇄 루프(Closed-Loop) 환류 파이프라인 의무화`** | 오탐 룰 능동 자동 튜닝 및 알람 피로도 80% 해소 |
| 이종 장비 교체 시 **기존 SOAR 플레이북과 SIEM 탐지 룰을 재개발하는 벤더 락인** | **`OASIS CACAO 2.0 표준 플레이북 및 Sigma 공통 탐지 룰 표준 채택`** | 벤더 종속 탈피 및 플레이북 100% 재사용 보장 |
| 대규모 SIEM 경보 폭증 시 SOAR 플레이북 동시 실행 큐 오버플로우 | **`플레이북 인스턴스 오토스케일링 및 고/중/저위험도 우선순위 큐`** 적용 | 초당 수백 건 경보 인입 시에도 지연 없는 병렬 대응 |

#### 한줄 요약
- 표준 인계 계약으로 파이프라인을 유지하고, 폐쇄 루프로 오탐을 튜닝하며, CACAO/Sigma로 벤더 락인을 제거한다.

## Ⅶ. 결론

- 지능형 사이버 위협에 대응하여 관제 센터의 완결성을 확보하는 **SIEM과 SOAR의 결합 아키텍처는 현대 SOC 운영의 핵심 표준**이며, 실무 구현 시 **CEF/ECS 기반의 무손실 인계 계약(Handoff Contract) 체결, OASIS CACAO 기반 표준 플레이북 구축, 사건 ID 기반의 양방향 폐쇄 루프(Closed-Loop) 환류 체계**를 통합 가동하여 탐지(MTTD)와 대응(MTTR)을 초 단위로 통합하는 차세대 보안 운영 환경 완성

#### 한줄 요약
- SIEM과 SOAR는 상관분석 탐지와 플레이북 오케스트레이션을 폐쇄 루프로 결합하여 무결점 자동 대응을 실현하는 차세대 보안 아키텍처다.