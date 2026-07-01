---
title: "분산 추적 (Distributed Tracing)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 277
---

# 📖 【암기용】 개념 완전 이해

> 목적: 분산 추적을 MSA 요청 1건이 여러 서비스·DB·메시지 큐를 지나간 경로와 시간을 재구성하는 방법으로 이해하게 만든다.

## 한눈에
- **개요**: 요청 단위 trace id와 span으로 서비스 호출 경로, 지연 구간, 오류 발생 지점을 추적하는 관측 기법
- **왜 필요한가**: MSA 장애는 한 서버 로그만 보면 원인을 찾기 어렵고, gateway, service, DB, broker 중 어느 구간에서 지연이 생겼는지 연결해서 봐야 한다.
- **핵심 직관**: 택배 송장 번호 하나로 집하, 허브, 배송차량, 수령까지 각 지점의 시간을 이어 보는 방식이다.

## 깊이 이해
- **배경·문제의식**: 모놀리식은 호출 스택이 한 프로세스 안에 있지만 MSA는 네트워크 호출로 스택이 분산되어 로그 순서만으로 원인 추적이 어렵다.
- **작동 원리**: 최초 요청에서 trace id를 만들고 각 작업 단위를 span으로 기록하며, parent-child 관계와 timestamp로 전체 호출 그래프를 복원한다.
- **비유**: 병원 진료에서 접수, 검사, 진료, 수납 시간을 한 접수번호로 연결해 대기 병목을 찾는 것과 같다.
- **구체 예시**: 주문 API p95 지연 800ms 중 payment span 620ms, inventory span 40ms로 보이면 결제 외부 API나 네트워크 구간을 우선 점검한다.
- **흔한 오해·주의점**: trace는 모든 요청을 영구 저장하는 기술이 아니다. sampling, 보존기간, 개인정보 제거 정책 없이 전량 저장하면 비용과 규제 리스크가 커진다.

## 연결 개념
- OpenTelemetry — trace context와 span 계측 표준
- Metrics Logging Tracing — trace는 요청 경로, metric은 집계 수치, log는 사건 상세 담당
- SRE/SLO — trace를 SLO 위반 원인 분석에 사용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 분산 추적은 호출 경로 시각화가 아니라 사용자 요청 단위로 지연·오류 원인을 분해하는 운영 분석 기법이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Distributed Tracing은 trace id와 span 관계로 분산 서비스 요청 경로와 처리 시간을 복원하는 관측 기법임.
> 2. **가치**: MSA 장애에서 latency hotspot, error propagation, 외부 의존성 지연을 요청 단위로 식별함.
> 3. **판단 포인트**: context propagation, sampling, span naming, PII 제거, log/metric 연계가 설계 품질을 좌우함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MSA 장애 분석 이해 확인 | trace id, span, parent-child, latency breakdown | 로그 검색과 동일시 |
| 관측성 설계 확인 | propagation, sampling, attribute | trace 전량 저장만 제시 |
| 운영 판단 확인 | SLO 위반 원인, 외부 의존성, 병목 구간 | 예쁜 service map 설명에 머묾 |

> 요약: 이 문제는 분산 호출 경로를 재구성해 사용자 영향 원인을 찾는 절차와 통제 지표를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 요청 경로 추적 기법
- 배경: MSA는 서비스 호출이 네트워크와 메시지 큐로 분산되어 단일 로그 파일만으로 전체 처리 경로를 알 수 없음.
- 필요성: SLO 위반 시 trace로 지연 span과 오류 span을 찾아 MTTA·MTTR 목표 이내 대응을 수행해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client Request -> Trace Context -> Service A Span
Service A Span -> Service B Span / DB Span / External API Span
Span Attributes -> Trace Backend -> Waterfall / Service Graph
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Trace ID | 요청 1건의 전체 식별자 | 서비스 경계 통과 시 유지 |
| Span | 작업 단위와 처리 시간 기록 | name, start/end time, status |
| Context Propagation | 부모 span 정보를 다음 서비스로 전달 | W3C Trace Context 등 |
| Trace Backend | span 저장·조회·시각화 | waterfall, dependency graph |

> 요약: 분산 추적은 trace id를 유지하고 span 관계를 기록해 요청 단위 호출 그래프를 복원한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> trace id 생성 / 수신 -> root span 시작
-> 하위 서비스 호출 시 context 전파 -> child span 기록
-> span 종료와 status 기록 -> backend 저장
-> waterfall 분석 -> 병목 span / 오류 span 식별
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | gateway 또는 최초 서비스가 trace context 생성 | trace creation rate |
| 2 | HTTP, gRPC, messaging header로 context 전파 | propagation success rate |
| 3 | 각 서비스가 span duration, status, attribute 기록 | span completeness |
| 4 | backend에서 trace를 조회해 지연·오류 구간 확인 | latency breakdown accuracy |

> 요약: trace는 context 전파와 span 기록이 모두 맞아야 요청 경로와 지연 구간을 재구성할 수 있다.

---

## Ⅳ. 특징

| 구분 | Metric | Log | Distributed Tracing |
|:---|:---|:---|:---|
| 분석 단위 | 집계 시계열 | 사건 상세 | 요청 1건의 경로 |
| 강점 | SLO 위반 감지 | 오류 메시지 확인 | 병목 span 식별 |
| 한계 | 원인 구간 불명확 | 서비스 간 연결 약함 | sampling과 저장 비용 필요 |
| 적용 기준 | alert, dashboard | audit, debug | MSA latency, dependency 분석 |

> 요약: 분산 추적은 metric으로 감지한 SLO 위반을 요청 경로 관점에서 분해하는 역할을 담당한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Distributed Tracing | 선택 기준 |
|:---|:---|:---|:---|
| 장애 분석 | 서버별 로그 검색 | 요청 단위 호출 그래프 | 서비스 호출 수 3개 이상 |
| 지연 분석 | 평균 응답시간 | span별 duration | p95/p99 병목 확인 |
| 의존성 | 수동 문서 | 실제 runtime dependency | 외부 API, DB, queue 연계 |

> 요약: 분산 추적은 호출 경로가 동적으로 변하고 서비스 의존성이 많은 환경에서 원인 분석 기준을 제공한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Trace 단절 | header 누락, 비표준 gateway | W3C Trace Context 적용 | broken trace ratio |
| 저장 비용 증가 | high traffic 전량 trace | head/tail sampling, retention | spans per second |
| 개인정보 노출 | attribute에 user data 저장 | PII masking, allowlist | sensitive field scan |

> 요약: trace 설계는 전파율, sampling, 개인정보 attribute 통제를 함께 다루어야 운영 리스크를 줄인다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 추적 완전성 | 핵심 transaction trace coverage 90% 이상 | endpoint 대조 |
| 원인 분석 | MTTA 목표 이내 | incident timeline |
| 비용 | trace 저장량 예산 이내 | retention, sampling report |

> 요약: 분산 추적 도입 성과는 coverage, MTTA, 저장량으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 user journey를 선정하고 gateway, service, DB client, message broker에 OpenTelemetry trace 계측을 적용함.
2. span naming 규칙과 attribute allowlist를 정의해 service.name, route, status_code 중심으로 분석 가능성을 확보함.
3. 오류 trace와 p95 이상 지연 trace는 tail sampling으로 보존하고 정상 trace는 낮은 비율로 표본 저장함.

**결론 (2줄):**
- 기술사 판단: 서비스 간 호출이 많은 시스템은 metric alert 이후 trace drill-down을 표준 장애 분석 절차로 둔다.
- 향후 방향: 분산 추적은 eBPF, service mesh, AIOps와 결합되어 계측 누락 구간을 줄이고 자동 원인 후보를 제시하는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 추적을 설명하시오" | trace id, span, context 전파 흐름 | metric·log 대비 역할 |
| 요구사항 명시형 | "MSA 장애 원인 분석 방안을 제시하시오" | SLO alert 후 trace drill-down 절차 | sampling, PII, trace 단절 리스크 |

> 요약: 설명형은 원리 중심, 방안형은 장애 분석 절차와 운영 통제를 중심으로 작성한다.
