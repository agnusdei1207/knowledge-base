---
sidebar:
  order: 95
  label: "095. SIEM vs SOAR 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "보안 관제 아키텍처 비교 및 상호 연계 : SIEM vs SOAR"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 95
extra:
  question_no: "95"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "SIEM(탐지/상관분석/가시성)과 SOAR(오케스트레이션/플레이북 자동화/대응)의 상호보완적 폐루프(Closed-Loop) 아키텍처"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SIEM vs SOAR**: 로그 수집과 상관 분석 기반 탐지(SIEM)와 API 오케스트레이션 및 플레이북 기반 대응(SOAR).
- **Closed-Loop Security (폐루프 보안관제)**: 탐지(SIEM) $\rightarrow$ 조사/대응(SOAR) $\rightarrow$ 결과 피드백 및 룰 튜닝으로 순환하는 관제 체계.

</details>

- 정의/개념: 로그 수집 및 상관 분석 기반의 **SIEM(탐지)과 API 오케스트레이션 및 플레이북 기반의 SOAR(대응)을 결합한 통합 폐루프 보안관제 아키텍처**
- 배경/필요성: SIEM 단독 운영 시의 수동 조치 지연과 SOAR 단독 운영 시의 원시 로그 분석 한계로 인한 **관제 병목 지속 및 복합 침해에 대한 실시간 차단 실패**

#### 한줄 요약
- SIEM의 가시성·탐지와 SOAR의 자동 대응을 결합하여 탐지-조사-대응-피드백의 폐루프를 완성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Alert Contract (경보 계약)**: SIEM이 SOAR로 인시던트를 전달할 때 이벤트 ID, 공격 유형, 신뢰도, 소스/목적지 IP 등을 JSON 표준 규격으로 약정하는 인터페이스.
- **Feedback Loop (피드백 환류)**: SOAR의 대응 결과(성공 여부, 오탐 판정)를 SIEM으로 역전송하여 탐지 룰 임계치를 자동 보정하는 메커니즘.

</details>

- **탐지(Detection)와 대응(Response)의 상호보완**: SIEM의 다차원 상관 분석과 **SOAR의 플레이북 기반 즉각 조치가 유기적으로 결합**
- **표준 경보 계약(Alert Contract) 기반 무손실 연동**: SIEM이 발행한 인시던트를 **JSON 스키마로 패키징하여 SOAR로 실시간 스트리밍**
- **대응 결과 환류(Feedback Loop)를 통한 지능형 튜닝**: SOAR의 조치 결과 및 분석가 판정을 **SIEM 탐지 룰 임계치 보정에 즉각 반영**

#### 한줄 요약
- 탐지-대응 상호보완, 표준 경보 계약 연동, 피드백 기반 룰 튜닝을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Security Actuators**: 방화벽, IPS, WAF, EDR, AD 등 SOAR의 API 호출을 받아 실제 차단/격리를 물리적으로 집행하는 보안 통제 장비들.

</details>

```text
[SIEM 및 SOAR 상호 연계 폐루프 아키텍처]
|-- Enterprise Ingress (방화벽/IPS, WAF, OS 이벤트, 클라우드 로그 수집)
`-- SIEM Layer (빅데이터 상관 분석 및 침해 탐지: Detection)
    |-- Log Collector & Normalizer (CEF/ECS 표준 스키마 변환)
    `-- Correlation Engine (시계열 복합 시나리오 평가 -> 인시던트 티켓 발행)
`-- Standard Alert Contract (Webhook / REST API: 심각도, IP, 파일 해시 전달)
`-- SOAR Layer (오케스트레이션 및 대응 자동화: Response)
    |-- Threat Enricher (TI 위협 평판 자동 보강)
    |-- Playbook Engine (BPMN 대응 시나리오 실행)
    |-- HITL Approval Gate (고위험 조치 시 관리자 1-클릭 승인)
    `-- REST API Connectors (방화벽 IP 차단, EDR 엔드포인트 격리)
`-- Feedback Loop (조치 결과 및 오탐 분석 데이터 -> SIEM 탐지 룰 튜닝 환류)
```

선의 의미: 인프라 로그가 SIEM에서 상관 분석되어 생성된 인시던트가 SOAR로 전달되고 플레이북 조치 후 결과가 다시 SIEM 룰 튜닝으로 환류되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SIEM 탐지 엔진** | 전사 로그 수집, **표준 스키마 정규화, 다차원 상관 분석 및 인시던트 발행** | Detection Platform |
| **경보 연동 인터페이스**| 사건 메타데이터, 위험도, **공격 증적을 표준 JSON 포맷으로 패키징 전달** | Webhook / API |
| **SOAR 플레이북 엔진** | 위협 맥락 보강, **의사결정 분기, 다중 장비 API 호출 및 자동 조치 집행** | Workflow Engine |
| **보안 통제 장비** | 방화벽, EDR, AD 등 **실제 차단 및 네트워크 격리를 집행하는 장비** | Security Actuators |
| **결과 환류 모듈** | 실제 대응 성공 여부 및 **분석가 판정 결과를 SIEM으로 전송하여 룰 보정** | Feedback Pipeline |

#### 한줄 요약
- SIEM 탐지 엔진, 경보 연동 인터페이스, SOAR 플레이북 엔진, 보안 통제 장비, 결과 환류 모듈이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **State Verification (상태 재조회)**: SOAR가 방화벽에 차단 API를 호출한 후 실제로 정책 테이블에 룰이 정상 적재되었는지 GET으로 재조회하여 확인하는 절차.

</details>

```text
SIEM 탐지 및 SOAR 자동 대응 폐루프 파이프라인
        │
   1. [로그 수집 및 정규화] 이종 인프라의 이상 로그가 SIEM 수집기로 실시간 인입 및 CEF 변환
        │
   2. [상관 분석 인시던트 발행] SIEM 상관 분석 엔진이 다단계 침해 시나리오 확정 후 인시던트 생성
        │
   3. [표준 경보 계약 전달] JSON 스키마를 통해 SOAR 플랫폼으로 티켓과 공격 아티팩트 자동 전달
        │
   4. [플레이북 API 오케스트레이션] SOAR가 TI 보강 후 방화벽 IP 차단 및 감염 PC 네트워크 격리 집행
        │
   ▼
5. [상태 재조회 및 룰 환류] 대상 장비 상태 재조회 검증 후 오탐 분석 결과를 SIEM으로 환류하여 룰 튜닝
```

#### 한줄 요약
- SIEM 상관 탐지 → 표준 티켓 전달 → SOAR 플레이북 실행 → 다중 API 조치 → 상태 검증 및 룰 환류 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SIEM vs SOAR**: 탐지·가시성 중심(SIEM)과 오케스트레이션·대응 자동화 중심(SOAR)의 아키텍처 비교.

</details>

| 비교 항목 | SIEM (보안 정보 및 이벤트 관리) | SOAR (보안 오케스트레이션/자동화/대응) |
|:---|:---|:---|
| **핵심 목적** | **전사 보안 가시성 확보 및 위협 탐지 (Detection)** | **사고 대응 프로세스 자동화 및 조치 (Response)** |
| **주요 입력 데이터** | **전사 원시 로그 (Syslog, Event Log, Flow, Audit)** | **SIEM/EDR이 정제하여 발행한 보안 경보 (Alert)** |
| **핵심 기술 메커니즘**| **로그 정규화, 시계열 상관 분석, UEBA 머신러닝** | **API 오케스트레이션, 플레이북(BPMN), 멱등성** |
| **결과물 (Output)** | **위협 인시던트(Incident) 경보, 대시보드, 감사 로그**| **방화벽 차단, PC 격리, 티켓 자동 종결, 감사 보고서**|
| **단독 운영 한계** | 탐지 후 조치가 수동으로 이루어져 대응 지연 발생 | 광범위한 원시 로그 상관 분석 및 저장 능력 부재 |

#### 한줄 요약
- SIEM은 빅데이터 상관 분석을 통한 탐지 플랫폼이며, SOAR는 API 오케스트레이션을 통한 자동 대응 플랫폼이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Concentration of Privilege (권한 집중 위험)**: SOAR가 사내 모든 방화벽, AD, EDR의 마스터 API Key를 보유함에 따라 SOAR 침해 시 전사 제어권이 탈취될 수 있는 위험.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SIEM의 오탐 경보가 SOAR 자동화와 연계되어 정상 트래픽 오차단 발생 | **신뢰도 점수(Confidence $\ge 90$) 필터링** 및 **고영향 조치 HITL 승인** | 정상 서비스 가용성 보호 및 오탐으로 인한 중단 방지 |
| SOAR 조치 API 호출 후 네트워크 장애로 인한 차단 미반영 보안 구멍 | 플레이북 내 **조치 후 대상 상태 재조회(State Verification)** 필수화 | 차단 룰 적재 성공률 100% 검증 및 보안 사각지대 제거 |
| SOAR 마스터 계정 탈취로 인한 전사 보안 통제권 상실 위협 | SOAR 계정의 **최소 권한(Least Privilege) 및 API Key HSM/MFA 관리** | 권한 집중 리스크 해소 및 플랫폼 침해 저항성 확보 |
| SIEM-SOAR 간 대량 알람 전송 시 Webhook 타임아웃 및 이벤트 유실 | **메시지 브로커(Kafka) 기반 비동기 이벤트 버퍼링 연동** | 대규모 이벤트 폭증 시에도 100% 무손실 전달 보장 |

#### 한줄 요약
- 신뢰도 필터링으로 오차단을 방지하고, 상태 재조회로 조치 성공을 검증하며, 최소 권한으로 SOAR 계정을 보호한다.

## Ⅶ. 결론

- 차세대 지능형 보안관제센터(SOC)의 효율성과 신뢰성을 극대화하기 위해 **SIEM의 빅데이터 상관 분석 탐지 능력과 SOAR의 오케스트레이션 기반 자동 대응 능력을 결합한 통합 폐루프 아키텍처를 표준 모델로 도입**하되, 운영 안정성을 확보하기 위해 **표준 경보 계약 체결, HITL 승인 관문 분기, 상태 재조회 및 룰 피드백 환류 체계**를 통합 구축하여 지능형 자율 사이버 방어 인프라 완성

#### 한줄 요약
- SIEM의 탐지와 SOAR의 자동 대응을 폐루프로 결합하여 고신뢰 차세대 보안관제를 실현한다.