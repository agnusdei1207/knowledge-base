---
sidebar:
  order: 167
  label: "167. AIOps (Artificial Intelligence for IT Operations)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "AIOps (Artificial Intelligence for IT Operations)"
date: "2026-08-10T23:40:00+09:00"
tags:
  - "notes-software"
weight: 167
extra:
  question_no: "167"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "이상 탐지•사건 상관•자동 대응 구조 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **AIOps (Artificial Intelligence for IT Operations)**: 방대한 IT 운영 데이터(로그, 지표, 트레이스)에 머신러닝과 AI를 결합하여 장애를 예측하고 근본 원인을 추론하며 복구를 자동화하는 차세대 IT 운영 플랫폼.
- **Alert Fatigue (경고 피로)**: 전통적 임계치(Threshold) 모니터링에서 연관된 수백 개의 알람이 폭주하여, 관제 인력이 진짜 장애 원인을 찾지 못하고 무시하게 되는 부작용.
- **Event Correlation (사건 상관 분석)**: 분리된 서버, DB, 네트워크 장비에서 발생한 수천 개의 로그와 에러를 시간과 토폴로지 기준으로 분석하여 1개의 '근본 장애 사건'으로 압축하는 기술.

</details>

- 정의/개념: 머신러닝 알고리즘을 활용하여 쏟아지는 IT 운영 신호(Telemetry)의 노이즈를 제거하고, 이상 탐지(Anomaly Detection)와 이벤트 상관관계(Correlation)를 분석해 장애의 근본 원인을 자동 식별하는 지능형 IT 운영 체계인 **AIOps**
- 배경/필요성: 마이크로서비스(MSA)와 멀티 클라우드의 도입으로 폭발적으로 증가한 운영 데이터를 인간의 수동 임계치(Threshold) 설정만으로는 통제할 수 없는 한계성 극복

#### 한줄 요약

- 배포 직후 여러 파드에서 경보가 쏟아지면 공통 변경과 의존 관계를 보고 하나의 장애 사건으로 묶어 먼저 확인할 원인과 조치를 제시한다.

## Ⅱ. 특징 (AIOps 3대 핵심 분석 기능)

<details><summary>핵심 용어</summary>

- **Anomaly Detection (이상 탐지)**: "CPU 80% 초과" 같은 고정 룰이 아니라, 과거 3개월 치의 주기적 학습 데이터를 바탕으로 "이 시간에는 평소 20%여야 하는데 지금 60%이므로 비정상"이라고 판단하는 딥러닝 기법.

</details>

- **Noise Reduction & Event Correlation (수만 개 알람을 1개의 근본 원인 알람으로 압축)**
- **Predictive Anomaly Detection (과거 패턴 머신러닝을 통한 미래 임계치 초과 선제적 예측)**
- **Root Cause Analysis (RCA) (토폴로지 그래프 기반 인과관계 분석 및 근본 원인 도출)**

#### 한줄 요약

- AI가 확정 원인을 선언하는 것이 아니라 시간, 대상, 변경 관계가 맞는 증거를 모아 운영자가 볼 후보 수를 줄이는 방식이다.

## Ⅲ. 구조 및 구성요소 (AIOps 참조 아키텍처)

<details><summary>핵심 용어</summary>

- **Machine Learning Engine**: 수집된 텔레메트리 데이터를 군집화(Clustering), 분류(Classification), 시계열 예측(Time-Series Forecasting)하는 AIOps의 두뇌.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        AIOps Platform Architecture                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Data Ingestion : [Metrics(모니터링)] [Logs(ELK)] [Topology(CMDB)]   │
│         │                                                              │
│         ▼                                                              │
│ 2. ML Engine      : [Anomaly Detection] ──► [Event Correlation (노이즈 감소)]│
│         │                                                              │
│         ▼                                                              │
│ 3. Action         : [Root Cause Analysis] ──► [Auto-Remediation (자동 복구)]│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 인프라 데이터가 수집되면 ML 엔진이 이상 징후를 탐지하고 노이즈를 필터링한 후, 근본 원인을 도출하여 자동화된 런북(Runbook)을 트리거하는 구조.

| AIOps 레이어 | 핵심 기능 및 역할 | 실무 적용 알고리즘 |
|:---|:---|:---|
| **Data Ingestion** | **모든 사일로화된 IT 데이터(로그, 메트릭, 트레이스, 티켓) 중앙 통합** | Kafka, ELK Stack |
| **Data Processing**| **데이터 정규화 및 실시간 스트리밍 처리** | Apache Flink, Spark |
| **Machine Learning**| **시계열 이상 탐지 및 이벤트 클러스터링(노이즈 감소)** | LSTM, Random Forest |
| **Action & Automation**| **근본 원인 식별 후 ITSM 티켓 자동 생성 및 Ansible 복구 스크립트 실행** | Root Cause Graph, Ansible |

#### 한줄 요약

- 수집 계층이 서로 다른 경보의 주소를 맞추고 분석 엔진이 관계를 묶으면 사건 관리가 사용자 영향에 따라 순서를 정하고 런북이 제한된 조치를 실행한다.

## Ⅳ. 흐름도 (AIOps 기반 장애 조치 파이프라인 흐름)

<details><summary>핵심 용어</summary>

- **Auto-Remediation (자동 복구)**: AIOps가 원인을 식별한 후, 사전에 정의된 런북(Runbook/Ansible)을 통해 사람의 개입 없이 서비스를 재시작하거나 디스크를 비우는 자율 조치.

</details>

```text
[Multiple IT Tools (Datadog, Splunk, AWS)] ──► (수만 건의 Raw Alert 쏟아짐)
                                                    │
                                                    ▼
                 [AIOps Machine Learning Engine (Event Correlation)]
                                                    │
                                                    ▼
      [1개의 "DB Connection Pool Full" 인시던트로 압축 (RCA 도출)]
                                                    │
                                                    ▼
[Auto-Remediation] ──► [Ansible: DB Connection Pool 증설 스크립트 자동 실행]
```

### 동작 원리

1. **Alert Storm**: 서버, 네트워크, APM에서 수만 개의 에러 알람이 동시다발적으로 유입.
2. **Correlation & RCA**: AIOps ML 엔진이 시간적/공간적 토폴로지를 분석해 99% 노이즈를 제거하고 'DB 병목'이라는 1개의 근본 원인(RCA)으로 압축.
3. **Automated Action**: 연동된 Ansible 자동화 툴이 DB 커넥션 풀을 증설하여 즉각 장애를 해소 (**AIOps 운영 완결**).

#### 한줄 요약

- 새 버전 배포 뒤 오류와 지연이 함께 늘면 하나의 사건으로 묶고 신뢰도가 높을 때만 승인된 롤백 런북을 실행한 뒤 회복 여부를 다시 측정한다.

## Ⅴ. 종류 및 비교 (전통적 모니터링 대 AIOps 1:1 비교)

<details><summary>핵심 용어</summary>

- **Rule-Based vs ML-Based**: 사람이 직접 IF-THEN(CPU 90% 이상 시 알람)을 세팅하는 룰 기반과, 기계가 패턴을 스스로 학습하는 ML 기반의 차이.

</details>

| 비교 항목 | Traditional Monitoring (전통적 관제) | AIOps (인공지능 IT 운영) |
|:---|:---|:---|
| **임계치 설정 방식**| **운영자가 수동으로 고정 임계치(Static Rule) 설정**| **ML이 동적 베이스라인(Dynamic Baseline) 자동 학습**|
| **장애 대응 시점** | 장애 발생 이후에 알람 수신 (사후 대응) | **징후를 사전 감지하여 장애 전 알람 (사전 예측)** |
| **알람 처리 (노이즈)**| 수백 개 알람 폭탄으로 경고 피로(Fatigue) 발생 | **상관 분석으로 알람 건수를 99% 압축 (RCA 제시)** |
| **문제 해결 주체** | 엔지니어가 대시보드를 보며 수동 해결 | **AI가 조치 스크립트 자동 트리거 (Auto-Remediation)** |

#### 한줄 요약

- 규칙은 이미 아는 온도선을 넘었는지 찾고 AI는 여러 신호가 함께 변한 패턴과 최근 변경을 조합해 낯선 사건을 찾는다.

## Ⅵ. 실무 고려사항 및 대책 (AIOps 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **Garbage In, Garbage Out (GIGO)**: 수집되는 로그나 CMDB 토폴로지 데이터의 품질이 낮으면 AI 모델이 쓰레기 알람만 내뱉는 현상.

</details>

| 3대 AIOps 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Data Silo & Poor Quality**| 네트워크, APM 데이터 규격이 모두 다름 | **OpenTelemetry 표준화로 통합 데이터 파이프라인 구축**|
| **2. Black Box AI** | AI가 RCA를 내놓았지만 근거를 알 수 없음| **Explainable AI(XAI) 적용 및 토폴로지 인과 그래프 시각화**|
| **3. Auto-Remediation 사고**| AI가 오판하여 멀쩡한 DB를 셧다운 시킴 | **도입 초기에는 '추천(Recommendation)'만 하고 인간이 최종 승인(Human-in-the-loop)**|

> 사례: **카카오 / 네이버 자체 AIOps 모델 구축을 통한 Alert 80% 감소 및 장애 인지 시간 단축**

#### 한줄 요약

- 모델 신뢰도가 높아도 데이터베이스 삭제처럼 되돌리기 어려운 조치는 추천에 머물고 재시작이나 롤백처럼 복구 가능한 조치부터 자동화해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **AIOps 수립 기준(AIOps Standards)**: Machine Learning Anomaly Detection, Event Correlation, RCA 도출 및 Auto-Remediation 연계에 의거한 체계.

</details>

- **AIOps 수립 기준**에 따라 대규모 하이브리드 인프라 관제 시 **AIOps Event Correlation & ML Engine** 필수 적용

#### 한줄 요약

- AI는 증거가 있는 원인 후보를 압축하고 고신뢰·저위험·가역 조치만 제한적으로 자동 실행하며 결과를 다시 인간이 검증해야 한다.
