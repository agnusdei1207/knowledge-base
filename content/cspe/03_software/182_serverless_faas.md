---
title: "서버리스 컴퓨팅·FaaS (Serverless FaaS)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 182
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서버리스 컴퓨팅과 FaaS를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서버 운영 단위를 숨기고 이벤트가 발생할 때 함수 단위 코드를 실행하는 클라우드 실행 모델
- **왜 필요한가**: 요청이 불규칙한 업무에서 서버 상시 운영, 패치, 용량 산정 부담을 줄이고 이벤트 기반 처리를 자동 확장한다.
- **핵심 직관**: 주방 전체를 빌리는 대신 주문이 들어올 때 조리대와 요리사를 초 단위로 빌리는 방식이다.

## 깊이 이해
- **배경·문제의식**: VM과 컨테이너는 서버 크기, 런타임 패치, 오토스케일 설정을 사용자가 책임진다. FaaS는 이벤트와 함수만 정의하고 실행 인프라는 CSP가 관리한다.
- **작동 원리**: API Gateway, Queue, Object Storage 이벤트가 함수를 호출하고, 플랫폼은 컨테이너 샌드박스를 할당해 코드를 실행한 뒤 사용 시간과 호출 수 기준으로 과금한다.
- **비유**: 24시간 상주 직원을 두지 않고 호출 벨이 울릴 때마다 검증된 작업자를 호출해 짧은 작업을 처리하는 구조이다.
- **구체 예시**: 이미지 업로드 이벤트가 발생하면 512MB Lambda가 3초 동안 썸네일을 생성하고 S3에 저장하며, 100만 호출과 실행 GB-second 기준으로 비용을 산정한다.
- **흔한 오해·주의점**: 서버리스는 서버가 없는 것이 아니라 서버 운영 책임이 CSP로 이동한 것이다. 콜드 스타트, 실행 시간 제한, 벤더 종속, 상태 관리 제약이 남는다.

## 연결 개념
- 이벤트 기반 아키텍처 - Queue, Pub/Sub, Object Event와 결합
- 오토스케일링 - 함수 동시 실행 수와 throttling 관리
- 마이크로서비스 - 기능 단위 배포와 API 조합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 서버리스 답안은 비용 절감 주장보다 이벤트 구조, 콜드 스타트, 상태 분리, 벤더 종속 대응을 판단해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Serverless FaaS는 이벤트 발생 시 함수 단위 코드를 실행하고 인프라 프로비저닝, 패치, 확장을 플랫폼이 담당하는 모델임.
> 2. **가치**: 호출 수와 실행 시간 기반 과금, 자동 확장, 운영 자동화로 변동성 큰 워크로드의 자원 우측정 문제를 줄임.
> 3. **판단 포인트**: 콜드 스타트 p95, 동시 실행 한도, 실행 시간 제한, 상태 외부화, 관측성, 벤더 종속을 기준으로 적용해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 실행 모델 이해 확인 | BaaS, FaaS, event trigger, managed runtime | "서버 없음"으로 오해 |
| 아키텍처 판단 확인 | stateless function, event source, external state | DB 연결 폭증과 상태 관리 누락 |
| 운영 리스크 확인 | cold start, timeout, concurrency, lock-in | 장점만 나열 |

> 요약: 이 문제는 이벤트 기반 실행의 장점과 운영 제약을 함께 판단하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

Serverless FaaS는 이벤트 기반 함수 실행 모델임. 인프라 운영 책임을 플랫폼에 맡기고 개발자는 함수 코드, 트리거, 권한, 관측 지표를 정의한다. 요청 변동이 크고 짧은 작업은 초 단위 과금과 자동 확장으로 서버 상시 운영 부담을 줄일 수 있다.

---

## Ⅱ. 구조 및 구성요소

```text
Client/Event Source -> API Gateway/Queue/Object Event -> Function Runtime -> Managed Service
  / State: DB/Cache/Object Storage
  / Control: IAM/Quota/Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | 함수 호출 트리거 제공 | HTTP, Queue, S3, Cron |
| Function Runtime | 코드 실행 샌드박스 | Node.js, Python, Java |
| Managed State | 상태 저장과 외부 연계 | DynamoDB, RDS Proxy, Redis |
| Control Plane | 권한, 동시성, 로그 관리 | IAM, quota, CloudWatch |

> 요약: FaaS는 이벤트, 함수 런타임, 외부 상태, 통제 계층으로 구성되어 stateless 실행을 전제로 동작함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 발생 -> 트리거 매핑 -> 함수 인스턴스 할당 -> 코드 실행 -> 외부 상태 저장 -> 로그/메트릭 수집
  / cold start -> runtime 초기화
  / concurrency 초과 -> throttling 또는 queue 적재
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API, Queue, Object 이벤트 수신 | trigger error 0건 |
| 2 | 런타임 컨테이너 할당 | cold start p95 측정 |
| 3 | 함수 코드 실행과 외부 API 호출 | timeout 0.1% 이하 |
| 4 | DB, Cache, Object Storage에 상태 저장 | connection pool 제한 |
| 5 | 로그, metric, trace 수집 | error rate, duration, throttle |

> 요약: FaaS는 이벤트 수신부터 상태 외부화와 관측까지 짧은 실행 주기를 반복함.

---

## Ⅳ. 특징

| 구분 | VM/Container 상시 실행 | Serverless FaaS | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 과금 | 인스턴스 시간 | 호출 수, GB-second | idle 비용 0원에 근접 |
| 확장 | HPA, ASG 설정 | 동시 실행 자동 조정 | concurrency quota |
| 지연 | warm process | cold start 존재 | p95 cold start 500ms 이하 목표 |
| 상태 | 로컬 메모리 가능 | 외부 저장소 필요 | stateless 함수 원칙 |

> 요약: FaaS는 변동 요청과 짧은 작업에 맞지만 지연, 상태, 동시성 한도를 설계해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 컨테이너 서비스 | 이벤트 함수 | 요청 지속 시간 15분 이하 |
| 비용/처리 | 상시 인스턴스 | 호출 기반 과금 | idle 60% 이상 업무 |
| 운영/위험 | 런타임 직접 관리 | CSP 관리형 런타임 | 패치 책임 전환 필요 |

> 요약: 실행 시간이 짧고 요청 변동이 큰 이벤트 업무는 FaaS, 장시간 연결과 예측 처리량 업무는 컨테이너를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 콜드 스타트 | 런타임 초기화 | provisioned concurrency, 경량 런타임 | cold start p95 |
| DB 연결 폭증 | 함수 동시 실행 증가 | RDS Proxy, connection pool | active connection |
| 벤더 종속 | CSP event, IAM, SDK 의존 | OpenFaaS, Knative, hexagonal 구조 | 이식 함수 비율 |

> 요약: FaaS 리스크는 지연, 상태, 종속성을 지표와 구조 분리로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 duration, cold start 500ms 이하 | APM, provider metric |
| 오류 | error rate 0.1% 이하, timeout 0건 | log metric filter |
| 비용 | 호출당 비용, GB-second | Cost Explorer, FinOps tag |

> 요약: FaaS 도입 판단은 지연, 오류, 호출당 비용을 함께 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 이벤트 업무 분류: 이미지 처리, 배치 알림, 웹훅처럼 15분 이하 stateless 작업을 FaaS 후보로 선정
2. 상태와 연결 통제: DB 연결은 RDS Proxy 또는 pooler 사용, 함수 메모리 512MB/1024MB별 duration과 비용 비교
3. 운영 기준 설정: cold start p95 500ms 이하, error rate 0.1% 이하, concurrency quota 80% 경보를 SLO로 관리

**결론 (2줄):**
- 기술사 판단: 변동 요청과 이벤트 처리는 FaaS, 지속 연결·장시간 처리·특수 런타임은 컨테이너 서비스가 적합함
- 향후 방향: Knative, WebAssembly runtime, OpenTelemetry가 서버리스 이식성과 관측성의 보완 축으로 확산됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서버리스를 설명하시오", "기술하시오" | 이벤트 수신, 함수 실행, 상태 외부화 흐름 | VM/Container 대비 과금·확장·지연 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "비교하시오", "설계하시오" | cold start, concurrency, DB 연결 통제 | 적용 업무 선별과 SLO 기준 |

> 요약: 설명형은 실행 모델, 방안형은 적용 대상 선별과 운영 지표 중심으로 전환함.
