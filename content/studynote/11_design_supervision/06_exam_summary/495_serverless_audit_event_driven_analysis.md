---
title: "495. 서버리스 감리 이벤트 드리븐 분석 (Serverless Audit Event Driven Analysis)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 환경에서 AWS CloudTrail, Azure Activity Log, GCP Cloud Audit Logs가 생성하는 API 호출 이벤트와 VPC Flow Logs, EKS Audit Log, Lambda Invoke Trace 등을 EventBridge/Eventarc 기반의 서버리스 함수(Lambda/Functions)가 실시간 수집·정규화하여 SIEM(Sentinel/Splunk/Chronicle)과 SOAR로 전달하는 **이벤트 소싱(Event Sourcing) + 스트림 프로세싱** 기반의 능동형 IT 감리 체계.
> 2. **가치**: 배치 기반 일·주 단위 사후 감리를 **밀리초~초 단위 실시간 탐지**로 전환하여 ISMS-P·전자금융감독규정·클라우드 보안인증(CSAP) 위반 징후를 즉시 차단하고, 감리 리드타임을 평균 14일 -> 90초로 단축, 운영 비용은 상시 가동 대비 **약 60~75% 절감**(AWS Lambda 기준 실행당 과금 모델).
> 3. **판단 포인트**: 콜드 스타트 지연(150ms~3s), 동시성 제한(Account Concurrency 1,000 기본), At-Least-Once 전달로 인한 중복 이벤트, Lambda 15분 실행 한도, 멀티 계정/멀티 리전 이벤트 라우팅의 팬아웃 설계, 그리고 **감리 로그의 불변성(WORM)·무결성(Hash Chain)·법적 보존(5년)** 요구사항을 어떻게 이벤트 드리븐 아키텍처 안에 녹일 것인가가 핵심 의사결정 사항.

---

## Ⅰ. 개요 및 필요성

전통적 IT 감리 패러다임은 **"주차장(Parking Lot) 방식"**이었다. 감사인이 분기/반기 단위로 현장에 출장하여 서버실의 로그 파일을 USB로 복사하고, 엑셀로 통계 내고, 보고서를 출력하는 1990년대 방식이 2020년대 클라우드 환경에서도 그대로 유지되고 있다. 그러나 다음과 같은 구조적 한계에 부딪힌다.

```text
+------------------------------------------------------------------------------+
|               기존 일괄(Batch) 감리 vs 서버리스 이벤트 드리븐 감리            |
+------------------------------------------------------------------------------+

  [기존 방식 - 주기적 사후 감리]                    [서버리스 이벤트 드리븐 방식]
  ------------------------                          --------------------------------

  +---------+    +---------+    +---------+       +---------+  실시간  +---------+
  | 서버실  |    |  로그   |    |  USB    |       |CloudTrail| --event-->|Lambda   |
  | 출장    |---->|  수집   |---->| 복사    |       |Audit Log |          |Collector|
  |(주 1회) |    |(Shell)  |    |         |       +---------+          +----+----+
  +---------+    +---------+    +----+----+                                |JSON
                                     v                                      |정규화
                              +-------------+                               v
                              |  엑셀 통계  |                          +-------------+
                              |  (수작업)   |                          |  Kinesis /  |
                              +------+------+                          | EventBridge |
                                     |                                 +------+------+
                                     v                                        |
                              +-------------+          +--------------------+  |
                              |  보고서     |          |  SIEM (Sentinel/   |<--+
                              |  (T+14일)   |          |  Splunk/Chronicle) |
                              +-------------+          +--------+-----------+
                                                                | 탐지 룰
                                                                v
                              +-------------+          +--------------------+
                              |  문제 인지  |          |   SOAR 자동 대응   |
                              |  (T+15일)   |          |   (즉시 격리/차단) |
                              +-------------+          +--------------------+
                              ❌ 이미 피해 확산           ✅ MTTD 90초, MTTR 5분
```

기존 방식은 클라우드 환경에서 **3가지 구조적 결함**을 가진다.

1. **휘발성 문제**: AWS Lambda는 기본적으로 CloudWatch Logs 외에 영속 감사 로그를 남기지 않으며, EC2는 인스턴스가 종료되면 로컬 로그가 소실된다. 주 1회 수집 시점 사이의 이벤트는 영구히 유실된다.
2. **책임회계 모델 불일치**: 클라우드 공유 책임 모델(Shared Responsibility Model)에서 IaaS 계층의 OS 로그는 고객이, PaaS/SaaS의 제어 평면(Control Plane) API 로그는 CSP가 보관한다. 이 경계가 **계정·리전·VPC별로碎片화**되어 있어 단일 감사 뷰를 구성하기 어렵다.
3. **증거 인과관계(Chain of Custody) 붕괴**: 한국 전자금융감독규정 제15조 및 ISMS-P 인증기준은 "감사 추적 기록의 변조 방지와 최소 1년 이상 보존"을 명시한다. 그러나 중앙 SIEM으로 전송된 로그가 **수집 시점 이후 변조되었는지**를 입증하려면 Merkle Tree 기반 해시 체인이 필요하다. 일괄 복사 방식은 이 무결성 증명이 원천적으로 불가능하다.

**📢 섹션 요약 비유**: 기존 감리가 "🏥 1년에 한 번 종합건강검진"이라면, 서버리스 이벤트 드리븐 감리는 "⌚ 스마트워치의 24시간 심전도 모니터링"이다. 심장발작이 발생한 뒤 병원에 가는 것이 아니라, 부정맥이 발생하는 **그 순간**에 알람이 울리고 AED가 작동하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서버리스 이벤트 드리븐 감리는 **5계층 파이프라인**으로 구성된다. 각 계층은 서버리스 컴퓨팅의 "필요할 때만 실행(Pay-per-Use)" 특성을 살려 평시에는 0에 가까운 비용으로 대기하다가, 이벤트가 발생하면 수십~수백 개가 동시에 Fan-out되어 병렬 처리한다.

```text
+------------------------------------------------------------------------------+
|          멀티 계정·멀티 리전 서버리스 이벤트 드리븐 감리 아키텍처              |
+------------------------------------------------------------------------------+

  [AWS Organization / Azure Tenant / GCP Folder]
   +------+------+------+------+
   | Prod | Dev  | Stg  |Sandbx|  <- Control Tower / Landing Zone
   +--+---+--+---+--+---+--+---+
      |      |      |      |
      | CloudTrail / Activity Log / Audit Log (중앙 S3/LA Workspace/BQ)
      v      v      v      v
  +----------------------------------------------------------------+
  | ① 이벤트 소스 계층 (Event Source Plane)                         |
  |   • API Audit : CloudTrail, Azure Activity, GCP Cloud Audit    |
  |   • Network  : VPC Flow Logs, NSG Flow, VPC Flow (GCP)         |
  |   • Identity : CloudTrail IAM, Azure AD Sign-in, Cloud IAM     |
  |   • Data    : S3 GetObject, BigQuery Audit, Azure Data Lake    |
  |   • Runtime : Lambda Invoke, EKS Audit, Cloud Function Exec    |
  |   • K8s     : EKS kube-apiserver audit.log, AKS diag          |
  +--------------------------+-------------------------------------+
                             | (JSON, CloudEvents v1.0, CEF, LEEF)
                             v
  +----------------------------------------------------------------+
  | ② 이벤트 버스 계층 (Event Bus Plane) - Fan-out 라우터          |
  |   • AWS EventBridge (이벤트 버스 × 100+, Archive 365일)        |
  |   • Azure Event Grid (Topic + Event Domain, MQTT 5.0)          |
  |   • GCP Eventarc (CloudEvents 표준)                            |
  |   • Apache Kafka (MSK) / Kinesis Data Streams (Sharding)       |
  |   • 패턴 필터: { "source": ["aws.iam"], "detail-type": [...] }  |
  +--------------------------+-------------------------------------+
                             | (라우팅 규칙: Route Rule, Subscription)
                             v
  +----------------------------------------------------------------+
  | ③ 서버리스 프로세싱 계층 (Lambda Plane) - Cold Start 최적화    |
  |   • Collector : S3 -> Firehose -> 정규화 Lambda (Python 3.12)   |
  |   • Enricher : Threat Intel (Tanium, MISP) 조인 함수          |
  |   • Detector : 룰 엔진 + ML 추론 (SageMaker Async Endpoint)   |
  |   • Notifier : SES/Teams/Webhook Fan-out                      |
  |   • 메모리: 512MB~3008MB, Ephemeral Disk /tmp 10GB            |
  |   • Provisioned Concurrency: 핵심 경로 워밍업                  |
  +--------------------------+-------------------------------------+
                             | (OCSF v1.2 표준 스키마로 변환)
                             v
  +----------------------------------------------------------------+
  | ④ 저장·분석 계층 (Storage & Analytics Plane)                   |
  |   • Hot : OpenSearch / Elasticsearch (7일, ILM 정책)           |
  |   • Warm : S3 + Athena Spectrum (30일, Parquet+ZSTD)          |
  |   • Cold : S3 Glacier Instant / Deep Archive (5년)            |
  |   • SIEM : Splunk ES / MS Sentinel / Google Chronicle         |
  |   • 무결성: S3 Object Lock (Compliance Mode) + S3 Inventory    |
  +--------------------------+-------------------------------------+
                             | (KQL / SPL / YARA-L)
                             v
  +----------------------------------------------------------------+
  | ⑤ 대응·증적 계층 (Response & Evidence Plane)                   |
  |   • SOAR: AWS Step Functions, Azure Logic Apps, Torq         |
  |   • 자동 액션: IAM Key Disable, Security Group 폐쇄, Quarantine|
  |   • 티켓: Jira/ServiceNow 양방향 동기화                       |
  |   • 리포팅: QuickSight / Power BI / Looker 대시보드           |
  |   • 법적 제출용: PDF+SHA-256 해시 + RFC 3161 TSA 타임스탬프   |
  +----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이벤트 소스 Collector** | CSP 감사 로그의 중앙 집중화 | CloudTrail Lake(최대 7년 보존, SQL 쿼리 가능), Azure Lighthouse(테넌트 간 위임), GCP Aggregated Log Sink(조직 수준 폴더 라우팅). 멀티 계정 트레일(Trail)을 Organizations 마스터에 적용. |
| **이벤트 정규화(OCSF)** | 이기종 로그를 단일 스키마로 변환 | Open Cybersecurity Schema Framework v1.2 (예: `class_uid: 1001` = Authentication). AWS Service Reference, Azure RM API 스펙에서 `eventName`->`action` 매핑 테이블. Lambda Layer로 공유 라이브러리 배포. |
| **Fan-out 라우터** | 이벤트 유형별 병렬 분배 | EventBridge Rule `event-pattern` JSON 매칭. Dead-Letter Queue(SQS) 필수 — 14일 후 자동 폐기 또는 재처리. Cross-Region Bus Peering으로 글로벌 단일 감사 뷰 구성. |
| **Lambda Detector** | 룰·ML 기반 이상 탐지 | 메모리 1,024MB, 타임아웃 5분, X-Ray 트레이싱 활성. Kinesis `IteratorAge` 메트릭으로 백로그 모니터링. Provisioned Concurrency로 콜드 스타트 200ms 이내 통제. |
| **SIEM Correlation** | 다단계 탐지 룰 실행 | Splunk SPL 예: `| tstats count from datamodel=Authentication where Authentication.user=* by Authentication.src, _time span=5m`. UEBA 모델로 사용자/엔터티 행동 베이스라인 수립. |
| **SOAR Playbook** | 자동 대응 워크플로우 | Step Functions ASL로 정의. 실패 시 보상 트랜잭션(Compensation). 휴먼 인 더 루프(HITL) 승인 게이트 — 위험 등급 Critical만 자동 실행, High/Medium은 분석가 승인. |
| **무결성 저장소** | 변조 방지 장기 보존 | S3 Object Lock(Compliance Mode) — 루트 권한으로도 삭제 불가. AWS KMS Customer Managed Key + S3 Inventory + Macie PII 마스킹. RFC 3161 TSA로 공인 타임스탬프. |
| **감사 증거 패키지** | 감독기관 제출용 번들 | PDF + JSON + CSV + 매니페스트(`manifest.json` with SHA-256). e-감리 표준(한국인터넷진흥원 KISA) e-Audit XML 스키마 준수. |

### 핵심 메커니즘: At-Least-Once 전달과 멱등성(Idempotency)

서버리스 이벤트 드리븐 감리가 직면하는 **가장 미묘한 기술적 과제**는 Lambda 함수의 At-Least-Once 실행 모델이다. EventBridge는 동일 이벤트를 최대 2회까지 재전송할 수 있으며, Kinesis는 `SequenceNumber`를 통해 순서를 보장하지만 샤드당 처리량이 초당 1,000건/1MB로 제한된다.

```text
  [이벤트 중복 시나리오]
  -----------------------
  T+0.0s : EventBridge -> Lambda Invoke (event_id=evt-9F2A)
  T+0.1s : Lambda 시작, DynamoDB PutItem({event_id, processed_at})
  T+0.8s : Lambda 비즈니스 로직 실행 중 일시적 네트워크 오류
  T+0.9s : EventBridge 타임아웃 -> 재시도 트리거 (Invoke #2)
  T+1.0s : 두 번째 호출이 동일 item을 PutItem -> ConditionalCheckFailedException

  ✅ 멱등성 보장 패턴
  +------------------------------------------------------------+
  | def handler(event, context):                               |
  |     event_id = event['id']                                 |
  |     try:                                                    |
  |         table.put_item(                                     |
  |             Item={'pk': event_id, 'ttl': now+86400},       |
  |             ConditionExpression='attribute_not_exists(pk)'  |
  |         )                                                   |
  |     except ClientError as e:                               |
  |         if
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 495 / 600

<- **이전**: [494. 컨테이너 감리 오케스트레이션 검증](/studynote/11_design_supervision/06_exam_summary/494_container_audit_orchestration_validation)
**다음**: [496. IoT 시스템 감리 연결성 보안 평가](/studynote/11_design_supervision/06_exam_summary/496_iot_system_audit_connectivity_security/) ->

---
