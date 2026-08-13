---
sidebar:
  order: 159
  label: "159. 서버리스 컴퓨팅•FaaS (Serverless Computing•FaaS)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "서버리스 컴퓨팅•FaaS (Serverless Computing•FaaS)"
date: "2026-08-14T02:28:00+09:00"
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

- **서버리스 컴퓨팅(Serverless Computing)**: 클라우드 제공자가 인프라를 전담 관리하고, 개발자는 코드 실행에만 집중하는 컴퓨팅 모델.
- **FaaS(Function as a Service)**: 이벤트 발생 시 1회성 함수(AWS Lambda)가 짧게 실행 후 종료되는 서버리스 구현 방식.
- **콜드 스타트(Cold Start)**: 런타임 환경 최초 부팅 시 컨테이너를 새로 생성하며 발생하는 1~3초의 응답 지연(Latency) 현상.

</details>

- 정의/개념: Event에 따라 Function을 실행하는 **Serverless•FaaS**
- 배경/필요성: 간헐 작업의 상시 Server는 **유휴 비용•운영 부담** 발생

#### 한줄 요약

- 사진 업로드처럼 사건이 생길 때만 함수 인스턴스가 열리고 처리가 끝나면 플랫폼이 회수하므로 상시 서버를 준비할 필요가 줄어든다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Pay-per-Execution**: 24시간 서버 렌탈비가 아닌, 오직 함수가 호출되어 실행된 시간(100ms 단위) 및 메모리 사용량에 비례하여 과금.

</details>

- 공급자가 **인프라•Runtime Scaling** 관리
- Event 수요에 맞춰 **Function Instance** 탄력 조정
- 호출•실행 시간•자원량 기반 **종량 과금**

#### 한줄 요약

- 서버 수를 직접 정하지 않는 대신 새 실행 환경이 열리는 시간과 같은 사건이 다시 도착하는 상황을 함수 설계가 흡수해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Event Trigger Sources**: S3 Bucket 업로드, DynamoDB Stream 갱신, API Gateway HTTP 요청, EventBridge 스케줄러 등 Lambda를 트리거하는 사건 공급원.

</details>

```text
[Event Source] ───── [FaaS Control Plane]
                           │
[External State] ─── [Function Runtime]
```

| 구성요소 | 책임 |
|---|---|
| Event Source | HTTP•Queue•Stream 등 **실행 Trigger** 제공 |
| FaaS Control Plane | 배치•동시성•재시도와 **수명주기** 관리 |
| Function Runtime | 사용자 Code와 **의존성 실행 환경** 제공 |
| External State | 실행 간 **상태•결과•멱등성 Key** 보존 |

#### 한줄 요약

- 트리거가 작업 접수, 제어 계층이 좌석 배정, 런타임이 작업 공간, 외부 상태 서비스가 함수가 사라져도 남는 장부 역할을 한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Provisioned Concurrency**: Cold Start 응답 지연을 방지하기 위해, Lambda 컨테이너 N개를 항상 웜(Warm) 상태로 미리 켜 두는 사전 프로비저닝 기능.

</details>

```text
[Event 도착]
    │
    ▼
1. Trigger•권한 검증
    │
    ▼
2. Warm Runtime 탐색
 ┌──┴────────────┐
 │ 없음          │ 있음
3. Runtime 초기화│
 └──┬────────────┘
4. Function 실행
    │
    ▼
5. 결과 저장•응답
    │
    ▼
[처리 결과 반환]
```

### 동작 원리

1. **Trigger•권한 검증**: Event 형식과 실행 권한 확인
2. **Warm Runtime 탐색**: 재사용 가능한 실행 환경 조회
3. **Runtime 초기화**: 없으면 Image•Code•Runtime 준비
4. **Function 실행**: 입력 처리와 외부 Service 호출
5. **결과 저장•응답**: 상태 보존과 성공•실패 반환

#### 한줄 요약

- 같은 파일 업로드 사건이 다시 전달돼도 외부 장부에서 식별자를 확인한 뒤 한 번만 결과를 쓰면 재시도가 중복 파일을 만들지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Stateless Nature**: FaaS 함수는 실행 후 즉시 소멸하므로, 함수 내부 로컬 디스크나 글로벌 변수에 상태(State)를 절대로 보존하지 못함.

</details>

| 비교 항목 | Traditional EC2 Server | Serverless FaaS (AWS Lambda) |
|:---|:---|:---|
| **인프라 관리** | OS•Patch•Scaling 직접 관리 | **공급자 관리 범위 확대** |
| **과금 체계** | Provisioning 자원 시간 기반 | **호출•실행 자원 기반**|
| **실행 시간** | 장기 Process에 적합 | 공급자별 **실행 제한** 존재 |
| **초기 응답 지연** | 상시 Process면 작음 | **Cold Start** 발생 가능 |

#### 한줄 요약

- 짧고 간헐적인 사건은 서비스형 함수가 인스턴스를 회수해 유휴 비용을 줄이고 지속 연결과 긴 작업은 컨테이너가 실행 제어를 유지한다.

## Ⅵ. 실무 고려사항 및 대책

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

- 간헐•짧은 Event는 **FaaS**, 장기•지속 연결은 Container 선택

#### 한줄 요약

- 실행 시간과 상태 수명, 지연 목표가 공급자 제한 안에 드는 사건형 작업에 FaaS를 적용한다.
