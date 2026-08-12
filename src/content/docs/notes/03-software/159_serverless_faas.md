---
sidebar:
  order: 159
  label: "159. 서버리스 컴퓨팅•FaaS (Serverless Computing•FaaS)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "서버리스 컴퓨팅•FaaS (Serverless Computing•FaaS)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 159
extra:
  question_no: "159"
  source_status: "기출"
  source_history: "120회, 122회"
  priority: 30
  priority_note: "이벤트 실행과 콜드 스타트는 기존 출제 범위임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Serverless Computing (서버리스 컴퓨팅)**: 개발자가 서버 인프라(OS, EC2)를 직접 프로비저닝하거나 관리하지 않고, 코드 작성에만 집중하는 클라우드 실행 모델.
- **FaaS (Function as a Service / 서비스형 함수)**: 서버리스의 핵심 구현 방식으로, 특정 이벤트(S3 파일 업로드, HTTP 요청) 발생 시에만 1회성 함수(AWS Lambda) 코드가 0.1초 만에 실행된 후 종료되는 모델.
- **Cold Start (콜드 스타트)**: 한동안 호출되지 않아 쿨다운된 런타임 환경에 첫 요청이 유입될 때, 컨테이너 인스턴스를 최초 부팅하느라 1~3초 응답 지연(Latency)이 발생하는 현상.

</details>

- 정의/개념: 서버 인프라 관리 0%, 사용한 밀리초(ms) 단위 코딩 실행 시간만 지불하며, 이벤트 구동(Event-driven) 방식으로 0에서 무제한으로 자동 확장되는 컴퓨팅 패러다임인 **Serverless & FaaS**
- 배경/필요성: 24시간 365일 켜 둔 EC2 인스턴스의 90% 유휴 자원 비용 낭비 절감, 초고속 서버리스 이벤트 아키텍처 구축 요구성

#### 한줄 요약

- 사진 업로드처럼 사건이 생길 때만 함수 인스턴스가 열리고 처리가 끝나면 플랫폼이 회수하므로 상시 서버를 준비할 필요가 줄어든다.

## Ⅱ. 특징 (FaaS 3대 핵심 운용 메커니즘)

<details><summary>핵심 용어</summary>

- **Pay-per-Execution**: 24시간 서버 렌탈비가 아닌, 오직 함수가 호출되어 실행된 시간(100ms 단위) 및 메모리 사용량에 비례하여 과금.

</details>

- **Zero Server Management (OS 패치, 서버 프로비저닝, 가상머신 관리 100% 불필요)**
- **Event-Driven Auto-Scaling (이벤트 폭증 시 0개에서 수천 개 Lambda 인스턴스 자동 확장)**
- **Pay-per-Execution Billing (유휴 시간 과금 0원, 실행 시간 100ms 단위 실효 청구)**

#### 한줄 요약

- 서버 수를 직접 정하지 않는 대신 새 실행 환경이 열리는 시간과 같은 사건이 다시 도착하는 상황을 함수 설계가 흡수해야 한다.

## Ⅲ. 구조 및 구성요소 (FaaS 3대 코어 파이프라인 아키텍처)

<details><summary>핵심 용어</summary>

- **Event Trigger Sources**: S3 Bucket 업로드, DynamoDB Stream 갱신, API Gateway HTTP 요청, EventBridge 스케줄러 등 Lambda를 트리거하는 사건 공급원.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Serverless FaaS (AWS Lambda) Pipeline                │
├────────────────────────────────────────────────────────────────────────┤
│ [1. Event Source] ──► S3 Upload / API Gateway HTTP / DynamoDB Stream   │
│                             │                                          │
│                             ▼ (Event Trigger)                          │
│ [2. FaaS Container] ──► AWS Lambda Function (MicroVM Firecracker)      │
│                             │ (Stateless Execution 100ms)              │
│                             ▼                                          │
│ [3. State Persistence]► AWS DynamoDB / ElastiCache Redis / S3 Bucket   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종 이벤트 소스가 발생하면 FaaS(AWS Lambda)가 즉시 1회성 구동되어 결과를 외부 영속 DB에 저장하고 소멸하는 구조.

| FaaS 구성 요소 | 기술 역할 및 메커니즘 | 실무 예시 (AWS Stack) |
|:---|:---|:---|
| **Event Source (Trigger)**| **FaaS 함수를 0.1초 만에 깨우는 이벤트 소스** | **AWS S3, API Gateway, SQS** |
| **FaaS Engine (Execution)**| **이벤트 수신 시 1회성 함수 코드를 초고속 구동**| **AWS Lambda, GCP Cloud Functions**|
| **Stateless State Store** | **Lambda 소멸 후에도 상태를 보존할 외부 DB** | **Amazon DynamoDB, Redis** |

#### 한줄 요약

- 트리거가 작업 접수, 제어 계층이 좌석 배정, 런타임이 작업 공간, 외부 상태 서비스가 함수가 사라져도 남는 장부 역할을 한다.

## Ⅳ. 흐름도 (Cold Start vs Warm Start 렌더링 흐름)

<details><summary>핵심 용어</summary>

- **Provisioned Concurrency**: Cold Start 응답 지연을 방지하기 위해, Lambda 컨테이너 N개를 항상 웜(Warm) 상태로 미리 켜 두는 사전 프로비저닝 기능.

</details>

```text
[First Request (Cold Start)] ──► [Init MicroVM (1-3s Latency)] ──► [Execute Code] ──► [Warm Container]
                                                                                           │
[Second Request (Warm Start)] ─────────────────────────────────────────────────────────────┘ (Execute <10ms)
```

### 동작 원리

1. **Cold Start**: 최초 호출 시 Firecracker MicroVM 및 런타임을 다운받아 켜느라 1~3초 응답 지연 발생.
2. **Warm Start**: 한 번 부팅된 컨테이너가 5~15분간 메모리에 살아있어 2번째 요청부터는 10ms 이내 초고속 반환 (**FaaS Execution 완결**).

#### 한줄 요약

- 같은 파일 업로드 사건이 다시 전달돼도 외부 장부에서 식별자를 확인한 뒤 한 번만 결과를 쓰면 재시도가 중복 파일을 만들지 않는다.

## Ⅴ. 종류 및 비교 (Monolithic EC2 vs Serverless FaaS)

<details><summary>핵심 용어</summary>

- **Stateless Nature**: FaaS 함수는 실행 후 즉시 소멸하므로, 함수 내부 로컬 디스크나 글로벌 변수에 상태(State)를 절대로 보존하지 못함.

</details>

| 비교 항목 | Traditional EC2 Server | Serverless FaaS (AWS Lambda) |
|:---|:---|:---|
| **인프라 관리** | **직접 OS, 패치, 스케일링 설정** | **0% (CSP가 100% 전담 관리)** |
| **과금 체계** | **24시간 켜진 시간 기반 정액제 (OPEX)**| **실행 시간(100ms) 및 메모리 사용량 기반**|
| **최대 실행 시간** | 무제한 | **최대 15분 제한 (15-min Timeout)** |
| **초기 응답 지연** | 없음 (항상 부팅되어 있음) | **Cold Start 지연 발생 가능 (1~3초)** |

#### 한줄 요약

- 짧고 간헐적인 사건은 서비스형 함수가 인스턴스를 회수해 유휴 비용을 줄이고 지속 연결과 긴 작업은 컨테이너가 실행 제어를 유지한다.

## Ⅵ. 실무 고려사항 및 대책 (FaaS 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **RDBMS Connection Exhaustion**: Lambda가 초당 5,000개 오토스케일링 확장되면서 PostgreSQL RDBMS 커넥션 풀(Max 100개)을 일순간 파괴시키는 참사.

</details>

| 3대 FaaS 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Cold Start Latency** | 최초 부팅 시 1~3초 지연 발생 | **Provisioned Concurrency 또는 SnapStart 적용**|
| **2. DB Connection Surge**| Lambda 1천 개 확장으로 RDBMS 뻗음 | **AWS RDS Proxy 도입으로 DB 커넥션 풀링** |
| **3. 15-Minute Timeout** | 15분 이상 걸리는 대용량 ETL 실패 | **AWS Step Functions 오케스트레이션 적용** |

> 사례: **토스 / 당근마켓 / 쿠팡 AWS Lambda + API Gateway + DynamoDB 기반 서버리스 구축**

#### 한줄 요약

- 이미지 업로드가 폭증해도 함수 동시성을 데이터베이스 처리량 아래로 제한하고 식별자로 중복을 막아 미리보기를 하나만 남겨야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Serverless/FaaS 수립 기준(Serverless Standards)**: AWS Lambda, Provisioned Concurrency, RDS Proxy, Step Functions 및 Event-Driven Architecture에 의거한 체계.

</details>

- **Serverless/FaaS 수립 기준**에 따라 이벤트 구동형 앱 구축 시 **Serverless FaaS & AWS Lambda & RDS Proxy** 필수 적용

#### 한줄 요약

- 짧고 재처리 가능한 사건은 서비스형 함수로, 지속 연결이나 긴 상태 작업은 관리형 컨테이너로 나눠 실행 모델을 선택해야 한다.
