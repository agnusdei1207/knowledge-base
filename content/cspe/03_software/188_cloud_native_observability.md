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
- **개요**: **관측성(Observability)**은 **메트릭·로그·트레이스** 3대 신호를 상관 분석해 시스템 내부 상태를 외부 출력만으로 추론하는 운영 체계다.
- **왜 필요한가**: 모니터링은 "이미 아는 장애 패턴"을 임계치로 감시하지만, MSA·쿠버네티스 환경은 pod가 수시로 뜨고 사라지며 예상 못 한 조합의 장애가 발생한다. 관측성은 "몰랐던 질문"에도 답할 수 있어야 한다.
- **핵심 직관**: 건강검진에서 체온계 숫자(메트릭), 진료 기록 원문(로그), 환자 이동 경로(트레이스)를 한 사람의 차트로 묶어 보는 것과 같다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 관측성(Observability) | 내부 상태를 외부 신호만으로 추론하는 능력 — 이 개념의 정체성 | 블랙박스 안을 계기판만 보고 짐작 |
| 모니터링(Monitoring) | 미리 정한 임계치를 감시하는 것(관측성의 부분집합) | 정해진 질문에만 답하는 체크리스트 |
| 메트릭(Metric) | 시간에 따라 집계된 숫자 신호 | 자동차 계기판 속도·RPM |
| 로그(Log) | 특정 시점에 발생한 이벤트의 원문 기록 | 블랙박스 음성 녹음 |
| 트레이스(Trace) | 하나의 요청이 지나간 전체 경로 기록 | 택배 송장의 이동 스캔 이력 |
| trace_id | 하나의 요청을 끝까지 추적하는 상관관계 키 | 접수번호 |
| Cardinality(카디널리티) | 라벨 값 조합이 만들어내는 시계열 개수 | 옷 사이즈×색상 조합이 늘수록 재고 종류 폭증 |
| Sampling(샘플링) | 전체 데이터 중 일부만 저장하는 정책 | 설문조사에서 전수조사 대신 표본추출 |
| RED 방법론 | Rate·Error·Duration — 요청 중심 서비스의 3대 지표 | 콜센터 통화량·실패율·통화시간 |
| USE 방법론 | Utilization·Saturation·Error — 자원 중심 지표 | 도로의 혼잡도·정체·사고 건수 |
| SLI/SLO | 사용자 체감 측정값과 목표치(192에서 상세) | 시험 점수와 목표 점수 |

## 깊이 이해

### 모니터링과 관측성은 왜 다른가
- 모니터링은 "CPU 90% 넘으면 경고"처럼 미리 정한 질문에 답한다. 사전에 정의하지 못한 장애(예: 특정 고객의 특정 API 조합에서만 발생하는 지연)는 잡지 못한다.
- 관측성은 "왜 이 사용자만 느린가"처럼 사후에 즉석 질문을 던져도 로그·메트릭·트레이스를 조합해 답할 수 있는 시스템 설계 자체를 가리킨다. 즉 모니터링은 결과물(대시보드·알람)이고, 관측성은 그 답을 가능하게 하는 데이터 구조(3대 신호 + 상관관계 키)다.

### 3대 신호가 각각 답하는 질문 — 수치로 이해
- 결제 API의 p95 지연이 300ms에서 1.2s로 4배 뛰었다고 하자.
  - 메트릭이 답하는 질문: "언제부터, 얼마나" — 대시보드에서 14:32부터 p95가 300ms → 1.2s로 상승했음을 확인.
  - 트레이스가 답하는 질문: "어디서" — 같은 시간대 trace를 열어 `payment(1.15s) -> fraud(50ms) -> db(950ms)` span 분해를 보면 db span이 병목.
  - 로그가 답하는 질문: "왜" — 같은 trace_id로 필터링한 구조화 로그에서 `SQL timeout, connection pool exhausted`를 확인.
- 세 신호를 trace_id·service.name·deployment.version 같은 공통 키로 엮지 않으면, 메트릭에서 이상을 봐도 로그·트레이스로 좁혀갈 방법이 없다. 관측성의 핵심은 신호 자체가 아니라 이 **상관관계(Correlation)**다.

### Cardinality 문제 — 왜 라벨을 함부로 못 붙이나
- 메트릭에 라벨(태그)을 붙일 때마다 시계열 개수는 라벨 값 개수의 곱으로 늘어난다.
- 예: service 50종 × http.method 5종 × status_code 10종 × pod_instance(동적 이름) 200개 = 500,000개 시계열. Prometheus 같은 TSDB는 시계열 하나당 메모리를 점유하므로 이 조합이 곧 메모리 폭증과 조회 지연으로 이어진다.
- 그래서 pod_instance처럼 계속 바뀌는(high-cardinality) 값은 메트릭 라벨에서 빼고 트레이스·로그 속성으로만 남긴다 — "집계할 값은 메트릭, 개별 식별은 트레이스/로그"가 판별 기준이다.

### Sampling — 전수 저장이 왜 불가능한가
- 초당 10,000건 요청을 100% 트레이스로 저장하면 하루 8.6억 span이 쌓여 저장 비용과 조회 성능이 감당되지 않는다.
- head-based sampling: 요청 시작 시점에 1% 확률로 저장 여부를 결정 — 구현이 단순하지만 정작 중요한(느리거나 실패한) 요청이 99% 확률로 누락될 수 있다.
- tail-based sampling: 요청이 끝난 뒤 "에러였는가", "p95를 넘겼는가"를 보고 그런 요청만 우선 보존 — 전체의 1%만 저장해도 문제 요청은 대부분 남는다. 대신 요청 완료까지 버퍼링해야 하므로 Collector 자원이 더 든다.

### 비유와 흔한 오해
- **비유**: 택배 지연 민원이 들어오면 물류센터 시간당 처리량(메트릭), 기사의 배송 기록 원문(로그), 송장 스캔 경로(트레이스)를 함께 봐야 "어디서 며칠 묶여 있었는지"를 알 수 있다. 한 가지만 보면 추측에 그친다.
- **오해**: 로그를 많이 쌓는 것이 관측성이 아니다. trace_id로 신호를 엮는 상관관계, cardinality 통제, sampling 정책, 보관 기간, 알림 임계치 설계가 없으면 비용과 잡음만 늘어난다.

## 연결 개념
- OpenTelemetry — 3대 신호를 표준화해 수집하는 계측 표준(189에서 상세)
- Distributed Tracing — 트레이스 신호의 구조(trace/span)를 상세히 다룸(190에서 상세)
- SRE — 관측성 데이터를 SLI로 삼아 오류 예산을 운영하는 체계(191에서 상세)

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

- 개요: 장애 원인 추론 체계
- 배경: 클라우드 네이티브 환경은 pod, service, function이 동적으로 변해 단일 서버 중심 모니터링으로 원인 분석이 어렵다.
- 필요성: metric, log, trace를 SLO와 연결해 사용자 영향과 복구 우선순위를 판단한다.

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
