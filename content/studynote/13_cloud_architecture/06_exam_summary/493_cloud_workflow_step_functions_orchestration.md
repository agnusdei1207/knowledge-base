---
title: "493. 클라우드 워크플로 Step Functions 오케스트레이션 (Cloud Workflow Step Functions Orchestration)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS Step Functions는 **Amazon States Language(ASL)**라는 JSON 기반 선언형 도메인 특화 언어(DSL)로 상태 머신(State Machine)을 정의하고, 이를 통해 마이크로서비스·Lambda 함수·SaaS API를 **시각적 오케스트레이션(Visual Orchestration)** 하는 완전 관리형 서버리스 워크플로 엔진입니다.
> 2. **가치**: 200개 이상의 AWS 서비스에 대해 **SDK/직접 통합(Direct Integration)** 을 지원하여 코드량을 평균 60~80% 절감하고, 상태 전환당 $0.025(Standard) 또는 100만 회당 $1(Express) 수준으로 **사용한 만큼만 과금(Usage-based Pricing)** 합니다. 자동 재시도·Catch/Fallback·사람 승인(CallBack Pattern)·CloudWatch Logs 자동 통합으로 **운영 가시성(Observability)** 을 제공합니다.
> 3. **판단 포인트**: 워크플로 실행 시간이 **1년(Standard)** 인지 **5분(Express)** 인지에 따라 워크플로 유형이 결정되며, 상태당 $0.025의 과금 모델은 **상태 폭주(State Fan-out)** 시 비용 폭탄이 될 수 있어 **Map/Parallel 패턴 사용 시 Concurrency Limit** 설정이 필수입니다. 페이로드 크기 256KB 제한과 상태 머신 정의 100KB 제한이라는 경계 조건을 고려한 데이터 패싱 전략이 핵심 의사결정 포인트입니다.

---

## Ⅰ. 개요 및 필요성

### 1. 마이크로서비스 시대의 워크플로 난제

클라우드 네이티브 아키텍처로 전환하면서 시스템은 수십~수백 개의 독립된 마이크로서비스, Lambda 함수, 외부 SaaS API의 **임시 결합(Loose Coupling)** 으로 구성됩니다. 2010년대 초반까지는 이를 **코레오그래피(Choreography)** 방식, 즉 SQS/SNS/Kafka로 이벤트를 흘려보내 각 서비스가 자율적으로 다음 단계를 결정하도록 했습니다. 하지만 다음 문제가 발생합니다.

- **흐름 가시성 부재**: "지금 주문 1,234건이 결제·재고·배송 중 어디에 멈춰 있는가?"를 알 수 없음
- **보상 트랜잭션(Compensating Transaction) 복잡**: 결제 후 재고 부족 시 결제를 되돌리는 SAGA 패턴을 모든 서비스에 분산 구현해야 함
- **디버깅 불가**: 이벤트 로그를 서비스별로 뒤져야 함
- **오류 처리 중복**: 재시도·백오프·데드레터 큐 로직이 각 서비스에 중복 작성됨

### 2. 오케스트레이션의 등장

2016년 AWS는 re:Invent에서 **AWS Step Functions**를 정식 출시(GA)하며, 코레오그래피의 한계를 극복할 **중앙 집중형 오케스트레이터(Centralized Orchestrator)** 를 제공했습니다. 핵심 컨셉은 "**상태 머신(State Machine)**"이며, BPMN(Business Process Model and Notation)처럼 워크플로를 한 장의 다이어그램으로 모델링하고, 그 그림이 곧 실행 가능한 코드가 됩니다.

```text
+---------------------------------------------------------------------+
|        코레오그래피(Choreography) vs 오케스트레이션(Orchestration)  |
+---------------------------------------------------------------------+

[코레오그래피 - SQS/SNS 이벤트 체인]                [오케스트레이션 - Step Functions]

   주문서비스 --이벤트발행--+                       +---> 결제서비스(Lambda)
        |                  |                       |
        v                  v                       |
   결제서비스 --이벤트---> 재고서비스 --이벤트---> 배송   <---+
        |                  |                       |    |
        +-실패시 보상처리? (각자 구현)                |   Steps
        +-재고 부족? (각자 구현)                    |    |  (중앙에서 조정)
        +-중복 결제? (각자 구현)                    |    |
                                                  +--+
   문제점:
   - 흐름 추적 불가  ❌                            장점:
   - 보상 로직 중복  ❌                            - 한눈에 흐름 파악  ✅
   - 디버깅 지옥      ❌                            - 보상 로직 중앙화 ✅
                                                    - 실행 이력 자동  ✅
```

- **📢 섹션 요약 비유**: SQS/SNS 이벤트 체인이 "각자 알아서 다음 사람에게 공을 던지는 릴레이 경기"라면, Step Functions는 **"코치가 휘슬을 불면서 차례로 주자를 지정하고 기록을 수첩에 적는 4×100m 릴레이"** 입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Amazon States Language (ASL): 선언형 상태 머신

Step Functions의 워크플로는 **ASL(Amazon States Language)** 이라는 JSON/YA로 작성된 DSL로 정의됩니다. ASL은 JSON Schema Draft-4를 따르며, 다음의 핵심 상태(State) 타입을 제공합니다.

| 상태 타입 | 역할 | 사용 사례 |
| :--- | :--- | :--- |
| `Task` | 단일 작업 수행 (Lambda 호출, AWS API 직접 호출, HTTP/SaaS 호출) | Lambda 함수 실행, DynamoDB PutItem, SNS Publish |
| `Choice` | 조건부 분기 (Rule 기반) | 주문 금액 ≥ 100,000원이면 무이자 할부 |
| `Parallel` | 동시 실행 분기 (Branches) | 결제 진행 + 재고 확인 동시 처리 |
| `Map` | 동적 병렬 반복 (반복 횟수를 런타임에 결정) | 주문 1,000건의 데이터를 병렬로 처리 (Distributed Map은 S3의 TB급 데이터도 처리) |
| `Wait` | 시간/날짜 기반 지연 | 결제 후 3분 뒤 결제 확인 |
| `Pass` | 입출력 변환/주입 (Lambda 없이 데이터 가공) | JSONPath로 필드 매핑, 주석, 페이로드 정제 |
| `Fail` / `Succeed` | 명시적 종료 | 입력 검증 실패 시 즉시 실패 종료 |

### 2. 워크플로 유형: Standard vs Express

Step Functions는 **두 가지 워크플로 유형**을 제공하며, 이는 비용·지속 시간·의미론(Semantics)이 완전히 다릅니다. 이 선택이 아키텍처의 첫 번째 의사결정입니다.

| 항목 | Standard Workflows | Express Workflows |
| :--- | :--- | :--- |
| 최대 실행 시간 | **1년** | **5분** |
| 실행 의미론 | **Exactly-once** (중복 실행 방지) | **At-least-once** (최소 1회, 중복 가능) |
| 과금 모델 | **상태 전환당(State Transition)** $0.025 | **실행 횟수 × 메모리·초** (1,000회당 $0.0000167 ~ $0.0000669) |
| 워크로드 특성 | 장기 실행, 비즈니스 트랜잭션, 사람의 승인 | 고빈도 이벤트 처리, IoT 데이터 스트림, ETL |
| 실행 이력 | Step Functions 콘솔에서 90일간 조회 | CloudWatch Logs에 기록 (콘솔 미저장) |
| Lambda 통합 | Run a Job / Callback with Task Token 지원 | Start sync/async만 지원 |

### 3. 직접 통합(Direct Integrations) - Lambda 없는 통합

기존에는 Step Functions -> Lambda -> AWS SDK -> 실제 서비스의 2단 호출이 필요했습니다. 현재는 **200+ AWS 서비스**에 대해 **Lambda 우회 직접 통합**을 지원합니다.

```text
[기존 방식] Lambda 우회 (2-Hop, 콜드 스타트 비용 + Lambda 과금)
   State -> Lambda 함수 -> AWS SDK -> DynamoDB/SNS/SQS ...

[현재 방식] Direct Integration (1-Hop, Lambda 과금 절감)
   State --Resource: "arn:aws:states:::dynamodb:putItem"---> DynamoDB
   State --Resource: "arn:aws:states:::sns:publish"-----> SNS
   State --Resource: "arn:aws:states:::s3:putObject"----> S3
   State --Resource: "arn:aws:states:::lambda:invoke"---> Lambda
   State --Resource: "arn:aws:states:::http:invoke"----> 외부 HTTP API
   State --Resource: "arn:aws:states:::aws-sdk:invoke"-> 220+ 서비스
```

### 4. 실행 메커니즘: 이벤트 소싱(Event Sourcing)

Step Functions는 **이벤트 소싱 패턴**으로 실행 이력을 관리합니다.

```text
+----------------------------------------------------------------------+
|                  Step Functions 내부 실행 흐름 (Event Sourcing)     |
+----------------------------------------------------------------------+

[사용자] StartExecution 요청
   |
   v
[API 계층] ---> 상태 머신 정의(ASL) 로드 + 새 Execution 생성
   |
   v
[오케스트레이터] 1. 첫 번째 상태 결정 (예: "CheckOrder" Task)
   |             2. HistoryEvent 기록: {type: "TaskStateEntered", ...}
   |             3. 해당 Task의 Resource(예: Lambda) 호출
   |             4. 응답 수신 후 HistoryEvent 추가
   |             5. 다음 상태 결정 (Choice -> A or B)
   |
   v
[History Table]  ---> 모든 단계가 순차적으로 기록됨 (변경 불가, Append-Only)
   |
   v
[실패/타임아웃 시] Catch 또는 Retry 정책에 따라:
   - Exponential Backoff: 1초->2초->4초->8초 (최대 2년, 999회)
   - Jitter: 0~30% 랜덤 지연
   - Fallback State: 실패 시 보상 트랜잭션(Lambda) 호출

[완료 시] ExecutionSucceeded Event 기록 -> CloudWatch Logs 자동 전송
```

### 5. 콜백 패턴(Callback Pattern): 사람/외부 시스템 통합

Lambda의 15분 타임아웃이나 **사람의 승인(Human-in-the-loop)** 이 필요한 경우 `.waitForTaskToken` 통합을 사용합니다.

```text
[State: "ApprovalTask"]
   Type: Task
   Resource: "arn:aws:states:::lambda:invoke.waitForTaskToken"
   Parameters:
     Payload:
       "taskToken.$": "$$.Task.Token"   # 토큰을 페이로드에 동봉
   Next: Approved

[Lambda가 토큰을 SNS/이메일로 사람에게 전달]
   |
   v
[사람이 SNS/Slack에서 "승인" 클릭]
   |
   v
[승인 시스템이 SendTaskSuccess API 호출]
   - TaskToken + Output 포함
   |
   v
[Step Functions: 토큰 매칭 -> 다음 상태(Approved)로 진행]
```

```text
+------------------------------------------------------------------------+
|      Step Functions 아키텍처 및 주요 컴포넌트 (ASCII 다이어그램)       |
+------------------------------------------------------------------------+

                  +----------------------------------+
                  |   AWS Step Functions Service    |
                  |   +--------------------------+   |
                  |   |   ASL 정의(상태 머신)     |   |
                  |   |  +--------------------+  |   |
                  |   |  |  States:           |  |   |
                  |   |  |  1. CheckOrder     |  |   |
                  |   |  |  2. Choice:        |  |   |
                  |   |  |     - VIP path     |  |   |
                  |   |  |     - Normal path  |  |   |
                  |   |  |  3. Parallel:      |  |   |
                  |   |  |     - Payment      |  |   |
                  |   |  |     - Inventory    |  |   |
                  |   |  |  4. Wait + Succeed |  |   |
                  |   |  +--------------------+  |   |
                  |   +--------------------------+   |
                  +----------+-------------+----------+
                             |             |
            +----------------+             +----------------+
            |                                               |
            v                                               v
   +------------------+                          +------------------+
   | 1. AWS Services  |                          | 2. 외부 시스템    |
   |  (Direct Integ)  |                          |  (HTTP 통합)      |
   | ---------------- |                          | ---------------- |
   | • Lambda         |                          | • Slack Webhook   |
   | • DynamoDB       |                          | • Twilio (SMS)    |
   | • SQS / SNS      |                          | • Salesforce API  |
   | • S3 / Glue      |                          | • 결제 게이트웨이  |
   | • ECS / Fargate  |                          |                  |
   | • SageMaker      |                          |                  |
   | • EventBridge    |                          |                  |
   +------------------+                          +------------------+
            |                                               |
            +---------------+-------------------------------+
                            v
                  +----------------------+
                  |  CloudWatch Logs /   |
                  |  X-Ray 트레이싱 /    |
                  |  EventBridge 이벤트   |
                  +----------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **State Machine** | 워크플로 자체의 청사진 | ASL(JSON)로 정의, 최대 100KB, 버전/별칭(Alias) 관리 가능 |
| **Execution** | State Machine의 단일 인스턴스 실행 | ExecutionArn으로 식별, `Standard`는 1년 보관, `Express`는 CloudWatch Logs에만 |
| **Task State** | 실제 작업을 수행하는 노드 | `Resource` 필드로 호출 대상 지정, `Retry`/`Catch` 블록 내장 |
| **Choice Rule** | 입력 JSON에 기반한 조건 분기 | `Variable.$, StringEquals, NumericGreaterThan, And/Or/Not` 등 비교 연산
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 493 / 800

<- **이전**: [492. 클라우드 검색 서비스 Elasticsearch OpenSearch](/studynote/13_cloud_architecture/06_exam_summary/492_cloud_search_service_elasticsearch_opensearch/)
**다음**: [494. 클라우드 배치 처리 Batch EMR 대용량](/studynote/13_cloud_architecture/06_exam_summary/494_cloud_batch_processing_batch_emr_large_scale/) ->

---
