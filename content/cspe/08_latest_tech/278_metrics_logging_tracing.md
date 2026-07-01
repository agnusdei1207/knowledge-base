---
title: "관측 3요소 (Metrics Logging Tracing)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 278
---

# 📖 【암기용】 개념 완전 이해

> 목적: metrics, logs, traces를 서로 대체 관계가 아니라 장애 감지·사건 확인·경로 분석을 나누어 맡는 관측 데이터로 이해하게 만든다.

## 한눈에
- **개요**: metric은 집계 수치, log는 사건 기록, trace는 요청 경로를 표현하는 관측성 핵심 signal
- **왜 필요한가**: 장애 대응은 "문제가 있는가", "무슨 일이 있었는가", "어디서 지연됐는가"에 각각 답해야 한다.
- **핵심 직관**: 자동차 운행에서 계기판 수치, 블랙박스 영상, 내비게이션 이동 경로를 함께 보는 방식이다.

## 깊이 이해
- **배경·문제의식**: 서버 수가 적을 때는 로그와 CPU 지표만 봐도 충분했지만, MSA에서는 장애 원인이 서비스 경로·배포 버전·외부 API에 흩어진다.
- **작동 원리**: metric은 SLO alert를 만들고, log는 오류 문맥을 제공하며, trace는 요청이 어느 서비스와 span에서 지연됐는지 연결한다.
- **비유**: 병원에서 체온·혈압(metric), 진료 기록(log), 검사 이동 동선(trace)을 함께 봐야 환자 상태를 판단할 수 있다.
- **구체 예시**: API error rate가 5분 동안 2%를 넘으면 trace로 실패 요청 경로를 찾고 log에서 exception과 request id를 확인한다.
- **흔한 오해·주의점**: 관측 3요소를 모두 많이 저장하는 것이 답은 아니다. SLO와 장애 질문에 필요한 label, field, sampling, retention을 정해야 한다.

## 연결 개념
- OpenTelemetry — metrics, logs, traces 수집 표준
- Distributed Tracing — traces 영역의 대표 기법
- SRE/SLO — metrics를 사용자 영향 기준으로 해석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 관측 3요소는 수집 항목 나열이 아니라 장애 대응 질문별 signal 조합과 비용 통제 설계다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Metrics, Logs, Traces는 시스템 상태, 사건 상세, 요청 경로를 다른 관점으로 표현하는 관측 signal임.
> 2. **가치**: metric으로 감지하고 trace로 범위를 좁히며 log로 오류 근거를 확인해 장애 대응 시간을 줄임.
> 3. **판단 포인트**: SLO 연결, 구조화 로그, trace context, cardinality, retention 정책을 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측성 기본 이해 확인 | metric, log, trace의 역할 차이 | 세 signal을 모두 로그로 설명 |
| 장애 대응 설계 확인 | 감지, 분석, 근거 확인 순서 | 대시보드 수만 늘리는 답안 |
| 운영 비용 판단 확인 | cardinality, sampling, retention | 전량 저장을 해결책으로 단정 |

> 요약: 이 문제는 관측 signal의 역할 분담과 SLO 기반 활용 절차를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 관측성 핵심 signal 3종
- 배경: 클라우드 네이티브 환경은 서버·Pod·서비스 호출 경로가 계속 바뀌어 단일 로그 분석만으로 장애 범위를 확정하기 어려움.
- 필요성: metric, log, trace를 trace id와 label로 연결해 alert에서 원인 확인까지 이어지는 대응 흐름을 구성해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application / Infra -> Metrics / Logs / Traces
Metrics -> SLO Alert
Traces -> Request Path / Latency Breakdown
Logs -> Event Detail / Audit Evidence
Correlation ID -> Incident Analysis
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Metrics | 시계열 수치와 임계 판단 | RED, USE, SLI |
| Logs | 사건 상세와 오류 문맥 | structured logging |
| Traces | 요청 경로와 span 지연 | trace id, span id |
| Correlation | signal 간 연결 키 | request id, trace id |

> 요약: 관측 3요소는 서로 다른 질문에 답하고 correlation id로 하나의 장애 분석 흐름을 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 처리 -> metric 집계 / log 기록 / trace span 생성
-> SLO alert 발생 -> trace로 지연 구간 확인
-> log로 오류 상세 확인 -> 원인 가설 검증 -> 대응
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스가 RED/USE metric을 노출 | SLI coverage |
| 2 | request id와 trace id 포함 구조화 log 기록 | log parse success |
| 3 | 서비스 경계마다 span 생성 | trace completeness |
| 4 | alert, trace, log를 incident timeline에 연결 | MTTA, MTTR |

> 요약: 관측 3요소는 metric alert에서 trace 분석과 log 확인으로 이어질 때 장애 대응 근거가 된다.

---

## Ⅳ. 특징

| 구분 | Metrics | Logs | Traces |
|:---|:---|:---|:---|
| 데이터 형태 | 숫자 시계열 | 구조화 이벤트 | span 관계 그래프 |
| 대표 질문 | 지금 문제가 있는가 | 어떤 오류가 발생했는가 | 어디에서 지연됐는가 |
| 비용 요인 | label cardinality | 저장량, 보존기간 | span volume, sampling |
| 대표 도구 | Prometheus | Loki, Elasticsearch | Jaeger, Tempo |

> 요약: metrics는 감지, logs는 증거, traces는 경로 분석에 적합하므로 장애 질문별로 조합해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 단일 signal 운영 | 관측 3요소 연계 | 선택 기준 |
|:---|:---|:---|:---|
| 감지 | 로그 오류 검색 | SLO metric alert | 사용자 영향 기준 |
| 분석 | 수동 grep | trace drill-down | 서비스 호출 경로 |
| 증거 | 임의 텍스트 | 구조화 log와 trace id | 감사·재현 필요 |

> 요약: 단일 signal 운영은 원인 분석이 느려지므로 MSA는 세 signal의 연결 키를 먼저 표준화해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 비용 초과 | 고유 label, verbose log | label allowlist, log level 정책 | ingest volume |
| 분석 단절 | request id 누락 | trace id를 log field에 포함 | correlation rate |
| 알림 피로 | 임계치 과다 | SLO burn rate alert | alert precision |

> 요약: 관측 3요소의 운영 리스크는 수집량보다 상관분석 단절과 알림 품질에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| SLI 커버리지 | 핵심 API 90% 이상 | service catalog 대조 |
| 상관분석 | log-trace 연결률 95% 이상 | trace id field 검사 |
| 저장 비용 | 예산·보존기간 준수 | backend usage report |

> 요약: 도입 성과는 SLI 커버리지, signal correlation, 저장 비용 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 서비스별 SLI를 latency, traffic, errors, saturation으로 정의하고 metric alert를 SLO burn rate 기반으로 구성함.
2. 모든 log에 timestamp, level, service.name, trace_id, request_id를 포함하고 개인정보 field는 masking 또는 제외 처리함.
3. OpenTelemetry로 trace context를 전파하고 오류 trace와 고지연 trace를 우선 보존하는 sampling 정책을 적용함.

**결론 (2줄):**
- 기술사 판단: MSA 운영에서는 metric만으로 원인 분석이 제한되므로 log와 trace를 같은 request context로 연결해야 함.
- 향후 방향: 관측 3요소는 event, profiling, eBPF telemetry와 결합되어 자동 원인 분석 데이터셋으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "관측 3요소를 설명하시오" | metric, log, trace 생성과 상관분석 흐름 | signal별 역할 차이 |
| 요구사항 명시형 | "장애 대응 체계를 설계하시오" | SLO alert에서 trace·log 확인 절차 | cardinality, retention, alert fatigue |

> 요약: 설명형은 signal 역할, 설계형은 장애 대응 흐름과 비용 통제를 중심으로 작성한다.
