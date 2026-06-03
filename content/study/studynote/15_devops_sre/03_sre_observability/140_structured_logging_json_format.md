---
title: 140. 구조화 로깅 (Structured Logging) - JSON 포맷 표준화
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구조화 로깅은 **[[568_logs_distributed_logging_elk_fluentd|로그]]를 사람이 읽는 텍스트가 아닌 [[343_json|JSON]] 등 기계가 파싱 가능한 구조로 출력**하여, 검색·필터·집계·[[325_correlation_analysis_pearson_spearman|상관 분석]]을 자동화하는 로깅 패턴이다.
> 2. **가치**: 비구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]("ERROR: payment failed for user 123")는 **grep으로만 검색 가능**하지만, 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]({"level":"ERROR","user_id":123})는 **Loki·ELK에서 필드별 [[298_qkv_attention|쿼리]]·집계**가 가능하다.
> 3. **판단 포인트**: [[568_logs_distributed_logging_elk_fluentd|로그]] 레벨(DEBUG·INFO·WARN·ERROR·FATAL), Correlation ID([[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]), [[033_context|컨텍스트]] 필드(user_id·request_id·trace_id)가 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]의 필수 요소이다.

---

## Ⅰ. 개요 및 필요성

```text
비구조화: "2024-01-15 10:30:22 ERROR Payment failed for user 123"
구조화 (JSON):
  {"ts":"2024-01-15T10:30:22Z","level":"ERROR",
   "msg":"Payment failed","user_id":123,
   "trace_id":"abc123","service":"payment"}
→ 필드별 검색: user_id=123 AND level=ERROR
```

- **📢 섹션 요약 비유**: 비구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]는 **자유 형식 메모**, 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]는 **엑셀 표**이다. 표가 검색·정렬·분석에 훨씬 유리하다.

---

## Ⅱ~Ⅴ. 결론

구조화 로깅은 **현대 [[111_observability_metrics_logs_traces|관측 가능성]]의 기본**이며, [[343_json|JSON]]+Correlation ID로 [[136_variance|분산]] 시스템의 [[568_logs_distributed_logging_elk_fluentd|로그]]를 추적한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **구조화 로깅** | [[343_json|JSON]] 형식 |
| **Correlation ID** | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 연결 |
| **[[568_logs_distributed_logging_elk_fluentd|로그]] 레벨** | DEBUG~FATAL |
| **Loki** | 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]] [[298_qkv_attention|쿼리]] |
| **Serilog/Zap** | 구조화 로깅 [[336_library_vs_framework|라이브러리]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[printf 로깅 (~2010s)] → [구조화 로깅 (Serilog, 2013)]
    → [JSON 로그 표준화 (2016~)]
    → [OTel Log Signal (2023)]
    → [현재: 구조화 로그 + AI 이상 탐지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 비구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]는 **자유 형식 메모**예요. 찾기 어려워요.
2. 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]는 **엑셀 표**예요. 칸(필드)마다 정리되어 **검색이 쉬워요**.
3. "에러인 것 중 사용자 123번"처럼 **정확히 필터**할 수 있어요!
