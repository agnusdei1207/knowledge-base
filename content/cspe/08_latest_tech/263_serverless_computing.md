---
title: "Serverless Computing 서버리스 (Serverless Computing)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 263
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서버리스를 서버가 없다는 뜻이 아니라 서버 운영 책임을 platform이 맡고 사용자는 함수·이벤트·요금 단위에 집중하는 모델로 이해하게 만든다.

## 한눈에
- **개요**: 서버 provisioning과 capacity 관리를 cloud provider 또는 platform이 맡고, 사용자는 function/container를 event 기반으로 실행하는 computing model
- **왜 필요한가**: 간헐적 workload, event 처리, API backend는 항상 server를 켜 두면 유휴 비용과 운영 부담이 발생한다.
- **핵심 직관**: 주방을 직접 운영하지 않고, 주문이 들어올 때마다 공유 주방이 필요한 만큼 조리 공간을 배정해 주는 방식이다.

## 깊이 이해
- **배경·문제의식**: VM이나 container cluster는 capacity 계획, patch, scaling, runtime 운영이 필요하다. 서버리스는 이 책임을 platform으로 이전해 code와 event 흐름에 집중하게 한다.
- **작동 원리**: Event source가 function을 호출하면 platform이 sandbox 또는 microVM/container를 준비하고 code를 실행하며, 요청량에 따라 instance 수를 조절하고 사용량 기준으로 과금한다.
- **비유**: 사무실을 장기 임대하지 않고 회의가 있을 때만 시간 단위 회의실을 예약하는 방식이다.
- **구체 예시**: Object storage upload event가 image resize function을 호출하고, 처리 결과를 storage와 message queue에 저장하는 구조가 대표적이다.
- **흔한 오해·주의점**: 서버리스에도 서버는 존재한다. 다만 사용자가 OS patch, node scaling, idle capacity 관리를 직접 수행하지 않는다.

## 연결 개념
- FaaS — function 단위 serverless 실행 모델
- Event-Driven Architecture — serverless trigger와 message 흐름의 기반
- Kubernetes — serverless container platform의 하위 실행 기반으로 사용 가능

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Serverless는 서버 부재가 아니라 운영 책임 이전, event 기반 scale, 사용량 과금, cold start trade-off로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Serverless Computing은 infrastructure provisioning을 platform이 담당하고 code가 event에 반응해 실행되는 운영 모델임.
> 2. **가치**: 간헐적 workload에서 idle capacity 비용을 줄이고 function 단위 배포와 자동 scaling을 제공함.
> 3. **판단 포인트**: Cold start, 실행 시간 제한, state 관리, vendor lock-in을 workload 특성과 비교해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| serverless 개념 확인 | 운영 책임 이전, event 기반 실행 | 서버가 없다고 문자 그대로 설명 |
| 구조 이해 확인 | trigger, function, runtime, managed service | Lambda 제품명만 나열 |
| 적용 판단 확인 | cold start, state, 비용, lock-in | 모든 API에 적합하다고 단정 |

> 요약: 이 문제는 serverless를 event-driven 운영 모델과 trade-off로 설명하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: event 기반 관리형 실행
- 배경: VM/container 상시 운영은 유휴 capacity, patch, scaling, 장애 복구 책임이 application team에 남음.
- 필요성: 간헐적 event 처리와 짧은 API workload는 사용량 기반 실행과 자동 scaling으로 운영 부담을 줄여야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Trigger / API Gateway -> Function Runtime -> Managed Service
              +-> IAM / Secret / Observability -> Billing Meter
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | HTTP, queue, storage, schedule event 발생 | 비동기 처리 많음 |
| Function Runtime | code 실행 sandbox 제공 | cold/warm start 차이 |
| Managed Service | DB, queue, storage 등 backend | state는 외부화 |
| IAM/Policy | function 권한 통제 | least privilege 필요 |

> 요약: Serverless는 event source, function runtime, managed backend, 권한·관측성 계층이 결합된 실행 모델이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Event 발생 -> Trigger Matching -> Runtime 준비
-> Function 실행 -> Managed Service 호출 -> Result / Retry / DLQ 처리 -> Metric / Billing 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | event source가 trigger 조건 충족 | event schema |
| 2 | platform이 runtime instance 준비 | cold start latency |
| 3 | function이 business logic 수행 | execution duration |
| 4 | 성공·실패·재시도·DLQ 처리 | error rate, retry count |

> 요약: Serverless는 event를 trigger로 runtime을 준비하고 실행 결과와 실패 처리를 platform metric으로 남긴다.

---

## Ⅳ. 특징

| 구분 | Container/Kubernetes | Serverless | 판단 기준 |
|:---|:---|:---|:---|
| 운영 책임 | cluster/node 운영 필요 | platform이 capacity와 runtime 관리 | 운영 인력 |
| 실행 모델 | long-running service 중심 | event/function 중심 | workload 지속 시간 |
| 과금 | 할당 자원·node 기준 | 요청·실행 시간 기준 | traffic 변동성 |
| 제약 | control 범위 넓음 | runtime/time/network 제한 | custom runtime 필요 |

> 요약: Serverless는 event성 workload에 적합하지만 runtime 제약과 state 외부화가 설계 전제다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM/Container 상시 실행 | event-triggered function | traffic 간헐성 |
| 비용/성능 | idle 비용 발생 가능 | request/duration 과금, cold start 존재 | p95 latency 요구 |
| 운영/위험 | infra control 가능 | lock-in과 quota 제약 | portability 요구 |

> 요약: Serverless는 간헐적·이벤트성 workload에 적합하고, low-latency 상시 service는 container 또는 managed runtime과 비교해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| cold start | runtime 초기화와 package 크기 | provisioned concurrency, package slim | p95/p99 latency |
| state 관리 오류 | function instance ephemeral 특성 | external state store, idempotency key | duplicate 처리율 |
| lock-in | provider event와 IAM 의존 | adapter layer, open standard 검토 | migration effort |

> 요약: Serverless 리스크는 cold start, state, lock-in이며 latency와 idempotency 설계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95/p99가 SLA 범위 이내 | APM, provider metric |
| 비용 | 요청 수와 실행 시간 기준 예산 이내 | billing tag |
| 신뢰성 | retry, DLQ, idempotency 적용 | failure injection |

> 요약: Serverless 성과는 지연, 비용, 실패 처리 지표가 workload 요구와 맞는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Image processing, queue consumer, scheduled job, webhook처럼 event 기반·간헐적 workload부터 serverless 후보로 선정함.
2. Function은 stateless로 작성하고 state는 managed DB, object storage, queue에 저장하며 idempotency key를 설계함.
3. Cold start, retry, DLQ, timeout, concurrency limit을 운영 지표로 설정하고 p95/p99 latency를 배포 전 검증함.

**결론 (2줄):**
- 기술사 판단: Event 기반이고 실행 시간이 짧으면 Serverless를 선택하고, long-running 연결·custom runtime·낮은 p99 요구가 크면 Kubernetes/Container를 선택함.
- 향후 방향: Serverless는 FaaS에서 container serverless, workflow, event mesh와 결합해 cloud native application의 event 실행 계층으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서버리스를 설명하시오" | event trigger와 runtime 실행 흐름 | container 대비 운영 책임 차이 |
| 요구사항 명시형 | "클라우드 비용 절감 방안을 제시하시오" | workload 선별과 cold start 검증 절차 | 비용·state·lock-in 리스크 |

> 요약: 설명형은 event 기반 실행 모델을, 방안형은 workload 적합성과 운영 지표를 중심으로 작성한다.
