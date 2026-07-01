---
title: "클라우드 네이티브 관측성 - 메트릭·로그·트레이싱 (Cloud Native Observability)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 188
---

# 📖 【암기용】 개념 완전 이해

> 목적: 클라우드 네이티브 관측성을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 메트릭, 로그, 트레이싱을 결합해 분산 시스템 내부 상태를 외부 신호로 추론하는 운영 체계
- **왜 필요한가**: MSA, Kubernetes, 서버리스는 구성요소가 계속 변해 단일 서버 로그만으로 장애 원인을 찾기 어렵다.
- **핵심 직관**: 건강검진에서 체온(메트릭), 진료 기록(로그), 검사 경로(트레이싱)를 함께 보는 방식이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 네이티브 환경은 인스턴스가 짧게 살고 요청이 여러 서비스를 지나간다. 장애 시 "어디가 느린가", "어떤 요청이 실패했나", "어느 배포 이후인가"를 연결해야 한다.
- **작동 원리**: 메트릭은 시간별 수치, 로그는 이벤트 상세, 트레이싱은 요청 경로와 span 지연을 제공한다. 세 신호를 trace ID, service name, deployment version으로 연결한다.
- **비유**: 택배 지연을 조사할 때 물류센터 처리량, 기사 기록, 송장 이동 경로를 동시에 확인하는 것과 같다.
- **구체 예시**: 결제 API p95가 300ms에서 1.2s로 증가하면 trace에서 `payment -> fraud -> db` span을 확인하고, 같은 trace ID 로그로 SQL timeout 원인을 좁힌다.
- **흔한 오해·주의점**: 로그를 많이 모으는 것이 관측성이 아니다. SLI/SLO, cardinality 관리, sampling, 보관 정책, 알림 피로 통제가 없으면 비용과 잡음이 증가한다.

## 연결 개념
- OpenTelemetry - 관측 데이터 수집 표준
- SRE - SLI/SLO, error budget 기반 운영
- Distributed Tracing - 요청 경로와 지연 원인 분석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 관측성 답안은 3대 신호 나열보다 SLI/SLO, 상관관계, 비용·카디널리티 통제를 포함해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 관측성은 metric, log, trace를 상관 분석해 분산 시스템의 상태와 장애 원인을 추론하는 체계임.
> 2. **가치**: p95 latency, error rate, saturation, trace span, structured log를 연결해 MTTR을 30분에서 10분 이하로 줄이는 운영 판단을 지원함.
> 3. **판단 포인트**: SLI/SLO, trace ID 상관, sampling, cardinality, retention, alert rule 품질을 기준으로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측성 개념 이해 확인 | metric, log, trace, SLI/SLO | 모니터링과 동일시 |
| 분산 시스템 운영 확인 | correlation ID, service map, error budget | 로그 수집만 언급 |
| 비용·품질 판단 확인 | cardinality, sampling, retention | 수집량 증가만 제시 |

> 요약: 이 문제는 장애 원인 추론 구조와 운영 지표를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

관측성은 장애 원인 추론 체계임. 클라우드 네이티브 환경은 pod, service, function이 동적으로 변해 단일 서버 중심 모니터링으로 원인 분석이 어렵다. metric, log, trace를 SLO와 연결해야 서비스 영향과 복구 우선순위를 판단할 수 있다.

---

## Ⅱ. 구조 및 구성요소

```text
Application/Platform -> Metric/Log/Trace Collector -> Storage -> Query/Alert -> Incident Response
  / Correlation: trace_id, service, version
  / Governance: sampling, retention, cardinality
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Metric | 시간별 수치 상태 | p95 latency, error rate, CPU |
| Log | 이벤트 상세와 원문 맥락 | structured log, trace_id |
| Trace | 요청 경로와 span 지연 | parent-child span |
| SLI/SLO | 사용자 영향 기준 | availability, latency 목표 |

> 요약: 관측성은 metric, log, trace를 trace ID와 SLO로 연결해 장애 원인을 좁히는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 처리 -> metric 생성 -> structured log 기록 -> trace span 생성 -> collector 수집 -> alert/analysis -> remediation
  / SLO 위반 -> incident 생성
  / cardinality 초과 -> label 제한
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스가 RED/USE metric 생성 | request, error, duration |
| 2 | trace_id 포함 structured log 기록 | JSON log 비율 95% 이상 |
| 3 | 요청 경로별 span 생성 | trace coverage 95% 이상 |
| 4 | collector가 backend로 전송 | drop rate 1% 이하 |
| 5 | SLO 기반 alert와 incident 처리 | MTTA, MTTR |

> 요약: 관측성은 수집보다 상관 분석과 SLO 기반 대응까지 이어질 때 운영 가치가 생김.

---

## Ⅳ. 특징

| 구분 | 전통 모니터링 | 클라우드 네이티브 관측성 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 대상 | 서버, VM 중심 | service, pod, function | ephemeral resource 추적 |
| 신호 | CPU, memory 위주 | metric, log, trace 결합 | 3대 신호 coverage |
| 기준 | 임계치 alert | SLO, error budget | burn rate alert |
| 비용 | 고정 로그 수집 | sampling, retention 정책 | cardinality 상한 |

> 요약: 클라우드 네이티브 관측성은 동적 자원과 분산 요청을 SLO 중심으로 분석함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 인프라 모니터링 | service-centric observability | MSA 서비스 10개 이상 |
| 비용/처리 | 전체 로그 보관 | sampling, retention | 월 수집 비용 예산 |
| 운영/위험 | 임계치 알림 | SLO burn rate | 알림 피로와 MTTR |

> 요약: 서비스 수와 요청 경로가 늘면 SLO 기반 관측성 체계가 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 비용 폭증 | high cardinality label | label allowlist, sampling | series count |
| 원인 추적 실패 | trace/log 상관 누락 | trace_id 표준화 | correlated log ratio |
| 알림 피로 | 증상별 임계치 남발 | SLO burn rate alert | alert action rate |

> 요약: 관측성 리스크는 비용, 상관관계, 알림 품질을 기준으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 품질 | trace coverage 95% 이상 | tracing backend |
| 운영 | MTTR 10분 이하 | incident record |
| 비용 | cardinality 상한 준수 | metric backend usage |

> 요약: 관측성 성공 여부는 coverage, MTTR, cardinality 비용으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 표준 신호 설정: RED(Request, Error, Duration)와 USE(Utilization, Saturation, Error)를 서비스별 SLI로 지정
2. 상관관계 확보: trace_id, service.name, deployment.version을 log와 trace에 공통 삽입하고 OpenTelemetry Collector로 수집
3. 비용·알림 통제: high cardinality label 금지, tail sampling, 7/30/90일 retention, SLO burn rate alert를 적용

**결론 (2줄):**
- 기술사 판단: MSA와 Kubernetes 운영은 로그 수집보다 metric, log, trace 상관관계와 SLO 운영이 우선임
- 향후 방향: OpenTelemetry, eBPF, AI 기반 incident analysis가 관측성 데이터 표준화와 원인 분석을 연결함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "관측성을 설명하시오", "기술하시오" | metric, log, trace 수집과 상관 흐름 | 모니터링 대비 SLO 중심 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "설계하시오" | SLI/SLO, collector, alert 설계 | MTTR, cardinality, sampling 기준 |

> 요약: 설명형은 3대 신호, 운영형은 SLO와 비용 통제 중심으로 전환함.
