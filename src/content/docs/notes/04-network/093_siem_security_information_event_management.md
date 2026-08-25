---
sidebar:
  order: 93
  label: "093. 융합 보안 관제 SIEM"
  badge:
    text: "기출 · 70%"
    variant: note
title: "빅데이터 보안 관제 플랫폼 : SIEM (Security Information and Event Management)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 93
extra:
  question_no: "93"
  source_status: "기출"
  source_history: "128회, 129회, 138회"
  priority: 70
  priority_note: "이종 로그 수집, 정규화(Normalization), 위협 인텔리전스(TI) 보강, 상관 분석(Correlation) 및 경보 피로도 완화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SIEM (Security Information and Event Management)**: 전사 보안 장비와 서버의 이종 로그를 수집·정규화하고 상관 분석하여 위협을 탐지하는 통합 관제 플랫폼.
- **Correlation Analysis (상관 분석)**: 시간 윈도우, IP, 계정을 축으로 단일 장비에서 놓치기 쉬운 다단계 APT 공격의 인과 관계를 교차 검증하는 기법.

</details>

- 정의/개념: 전사 이종 인프라의 대용량 로그를 수집·정규화하고 **위협 인텔리전스(TI) 맥락 보강 및 시계열 상관 분석으로 복합 침해를 탐지하는 통합 보안관제 플랫폼**
- 배경/필요성: 개별 장비 사일로 관제의 한계로 인한 **단편적 알람 폭증(Alert Fatigue), 장비 간 연계 침해 시나리오(APT) 탐지 불가 및 사고 대응 지연**

#### 한줄 요약
- 이종 로그 수집, 표준 스키마 정규화, 위협 인텔리전스 결합, 시계열 상관 분석을 통해 복합 APT 공격을 탐지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CEF / ECS (Common Event Format / Elastic Common Schema)**: 제조사마다 제각각인 로그 필드명을 단일 글로벌 표준 필드로 통일하는 정규화 스키마.
- **Enrichment (맥락 보강)**: 원시 IP/도메인 로그에 Geo-IP 위치, 내부 자산 중요도, 외부 최신 위협 인텔리전스(TI) 정보를 결합하여 분석 가치를 높이는 과정.

</details>

- **이종 보안 데이터 수집 및 정규화(Normalization)**: 제조사별 이질적인 로그 포맷을 **CEF/ECS 표준 스키마로 단일화**
- **다차원 시계열 상관 분석(Event Correlation)**: 시간 윈도우($\Delta t$) 내에서 방화벽 차단과 웹 인증 성공을 **교차 검증하여 인시던트 승격**
- **경보 집약 및 관제 피로도(Alert Fatigue) 해소**: 수만 건의 단순 이벤트를 **위험 점수(Risk Score) 기반의 단일 고위험 티켓으로 집약**

#### 한줄 요약
- 이종 로그 표준화, 시계열 상관 분석, 위험 점수 기반 알람 집약을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Log Collector & Pipeline**: Syslog, Kafka, 에이전트를 통해 초당 수십만 이벤트(EPS)를 무손실 버퍼링 및 수집하는 스트리밍 파이프라인.

</details>

```text
[SIEM 빅데이터 수집 및 상관 분석 파이프라인]
|-- Distributed Data Sources (방화벽/IPS, WAF, Windows AD, Linux Auth, CloudTrail)
`-- SIEM Big Data Engine
    |-- 1. Log Collector (Kafka 분산 큐 기반 무손실 버퍼링 & NTP 타임스탬프 동기화)
    |-- 2. Normalization & Parser (비정형 로그 -> CEF/ECS 공통 스키마 변환)
    |-- 3. Context Enrichment (CMDB 자산 중요도 DB + STIX/TAXII TI 악성 IP 매핑)
    |-- 4. Correlation Rule & UEBA Engine (시계열 윈도우 룰 평가 & 머신러닝 이상 탐지)
    `-- 5. Indexing & Hot/Cold Storage (초고속 검색 인덱스 및 장기 감사 보존소)
`-- SOC Console & SOAR (위험 점수 기반 인시던트 발행 -> 플레이북 자동 대응 연계)
```

선의 의미: 이종 소스의 로그가 수집기, 정규화기, 맥락 보강 모듈을 거쳐 상관 분석 엔진에서 단일 인시던트로 집약된 후 관제 콘솔 및 SOAR로 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **로그 수집기 (Collector)** | 전사 에이전트 및 Syslog/API를 통한 **비동기 로그 수집 및 무손실 버퍼링** | Logstash, Fluentd |
| **정규화 및 파서 엔진** | 비정형 로그를 **표준 필드(CEF, ECS)로 파싱하고 데이터 스키마 통일** | Normalizer |
| **맥락 보강기 (Enricher)** | 수집 로그에 **내부 자산 정보, Geo-IP, 외부 위협 인텔리전스(TI) 결합** | Context Injection |
| **상관 분석 엔진** | 다차원 조건식과 **시간 윈도우 기반 복합 공격 패턴 및 시나리오 탐지** | CEP / Rule Engine |
| **빅데이터 스토리지** | 인덱싱된 로그의 **실시간 고속 검색 및 법적 컴플라이언스 보존 지원** | Elastic, OpenSearch |

#### 한줄 요약
- 수집기, 정규화 파서, 맥락 보강 모듈, 상관 분석 엔진, 빅데이터 저장소가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Incident Escalation (인시던트 승격)**: 개별 단순 알람이 복합 상관 룰 조건(예: 5분 내 100회 브루트포스 실패 후 1회 로그인 성공 및 DB 대량 덤프)을 만족할 때 공식 침해 사고로 전환하는 절차.

</details>

```text
SIEM 로그 수집, 정규화, 상관 분석 및 인시던트 발행 파이프라인
        │
   1. [이종 로그 수집] 분산 인프라의 원시 로그를 Kafka 분산 큐를 통해 실시간 무손실 수집
        │
   2. [CEF/ECS 정규화] 파서 엔진이 이질적인 타임스탬프와 필드를 단일 표준 스키마로 변환
        │
   3. [TI 및 자산 맥락 보강] STIX/TAXII 악성 IP DB와 CMDB 서버 중요도를 매핑하여 가중치 부여
        │
   4. [시계열 상관 분석 평가] 시계열 윈도우($\Delta t$) 내에서 사전 정의된 복합 침해 시나리오 룰 대조
        │
   ├─ [단일 로그 단순 알람] ➔ 저위험도 분류 및 일반 검색 인덱싱 저장
   ▼
5. [고위험 인시던트 승격] 복합 공격 체인 확정 시 단일 티켓 생성, 위험 점수 부여 및 SOAR 연계
```

#### 한줄 요약
- 스트리밍 수집 → 필드 정규화 → TI 맥락 보강 → 시계열 상관 분석 → 고위험 인시던트 발행 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **1세대 룰 기반** vs **차세대 AI/UEBA** vs **클라우드 네이티브 SaaS**.

</details>

| 비교 항목 | 1세대 룰 기반 SIEM | 차세대 AI/UEBA SIEM | 클라우드 네이티브 SIEM (SaaS) |
|:---|:---|:---|:---|
| **분석 메커니즘** | **정적 시나리오 조건문 (IF-THEN 룰)** | **머신러닝 기반 사용자/자산 행위 분석 (UEBA)** | **클라우드 스케일 AI 및 분산 검색 엔진** |
| **탐지 대상** | 알려진 패턴(Known Attacks), 무차별 대입 | **내부자 위협, 계정 탈취, 변종 제로데이** | **멀티클라우드(AWS/Azure) 감사 로그** |
| **오탐률 및 유지보수**| **높음 (환경 변화 시 지속적 룰 튜닝)**| **낮음 (동적 기준선 학습으로 오탐 필터링)** | 낮음 (글로벌 벤더 위협 인텔리전스 자동 갱신)|
| **인프라 확장성** | 온프레미스 스토리지 용량 한계 존재 | 대규모 연산 리소스(GPU/서버) 요구 | **서버리스 아키텍처로 무제한 확장 (EPS 무관)**|
| **대표 솔루션** | Splunk Enterprise, ArcSight | Exabeam, QRadar Sense | **Microsoft Sentinel, Chronicle, Datadog** |

#### 한줄 요약
- 1세대는 정적 룰 탐지, 차세대는 AI 기반 이상 행위 분석, 클라우드 네이티브는 무제한 확장성을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Alert Fatigue (관제 피로도)**: 일일 수만 건의 단순 보안 알람이 쏟아져 관제 요원의 주의력이 분산되고 실제 치명적인 위협을 놓치게 되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장비 간 시계 불일치(Time Skew)로 공격 인과 관계 역전 및 상관 분석 실패 | 전사 인프라에 **`NTP/PTP 기반 마이크로초 시간 동기화` 및 수집단 검증** | 타임라인 기반 공격 체인 재구성 및 증적 신뢰성 확보 |
| 과도한 단순 탐지 룰로 인한 수만 건의 알람 발생 및 **관제 피로도(Alert Fatigue)** | **`위험 점수(Risk Scoring) 기반 알람 집약` 및 AI 노이즈 필터링** | 관제 피로도 해소 및 평균 대응 시간(MTTR) 70% 단축 |
| 특정 시간대 로그 폭증(EPS Spike)으로 인한 버퍼 오버플로우 및 로그 유실 | 수집 파이프라인 전단에 **`Apache Kafka 분산 메시지 큐 완충 계층`** 배치 | 대규모 트래픽 유입 시 제로 로그 손실 및 무중단 수집 보장 |
| 장기 로그 보관에 따른 온프레미스 스토리지 비용 폭증 | **`Hot-Warm-Cold 계층형 스토리지(Object Storage)`** 수명주기 정책 | 스토리지 비용 60% 절감 및 컴플라이언스 준수 |

#### 한줄 요약
- NTP 동기화로 타임라인을 일치시키고, 위험 점수로 피로도를 완화하며, Kafka로 로그 유실을 방어한다.

## Ⅶ. 결론

- 전사 IT/OT 인프라에 대한 포괄적 가시성을 확보하고 복합 지능형 침해 사고를 탐지하기 위해 **빅데이터 기반 차세대 SIEM 플랫폼을 핵심 관제 인프라로 구축**하되, 분석의 정확성과 가용성을 유지하기 위해 **NTP 정밀 시간 동기화, Kafka 기반 무손실 수집 파이프라인, AI/UEBA 기반 이상 행위 프로파일링 및 SOAR 자동화 연계**를 통합 적용하여 지능형 자율 보안관제(Autonomous SOC) 완성

#### 한줄 요약
- SIEM은 대용량 로그 정규화와 시계열 상관 분석을 통해 복합 사이버 위협을 실시간 탐지하는 전사 보안관제의 중추 플랫폼이다.