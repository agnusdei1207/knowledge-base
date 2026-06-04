+++
title = "543. 서비스 수준 관리 SLA SLO SLI (Service Level Management SLA SLO SLI)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SLA(서비스 수준 협약)는 고객-공급자 간 법적/계약적 약속이고, SLO(서비스 수준 목표)는 이를 정량화한 목표치(예: 월 가용성 99.95%), SLI(서비스 수준 지표)는 그 목표를 측정하는 원시 지표(예: 5xx 비율, p99 레이턴시)로, **SLA ⊃ SLO ⊃ SLI**의 계층적 관계를 가진다.
> 2. **가치**: 명확한 SLI/SLO 정의는 **에러 버짓(Error Budget)** 기반의 객관적 의사결정 프레임워크를 제공하여, 100% 가용성을 추구해 발생하는 과잉 투자(OpEx/CapEx 절감)와 무분별한 릴리즈로 인한 신뢰 하락(SLO 위반 비용 절감) 사이의 균형을 가능케 한다.
> 3. **판단 포인트**: "**얼마나 측정 가능한가(observability vs. reality)**", "**어떤 윈도우(rolling 30일 vs. calendar month)**로 집계할 것인가", "**SLO 위반 시 어떤 계약적/기술적 조치가 트리거되는가**"가 핵심 설계 변수로 작용하며, 마이크로서비스 환경에서는 서비스 간 SLI의 **전이(cascading) 전파** 설계가 가장 큰 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 서비스가 On-Premise 단일 시스템에서 클라우드 네이티브 MSA(Microservices Architecture)로 전환되면서, 단일 시스템의 MTBF/MTBR로 품질을 표현하던 고전적 SLA 체계는 한계에 부딪혔다. 수십~수백 개 서비스가 분산 환경에서 상호 호출하며 비동기·반응형 패턴(Reactive System)을 구성하는 환경에서는, 서비스의 "성공"이 단일 컴포넌트의 정상 동작이 아닌 **사용자 관점의 종단간(End-to-End) 트랜잭션 성공률**로 정의되어야 한다. 또한, 클라우드 SLA는 AWS EC2의 99.99% Multi-AZ 같은 형태로, 컴포넌트별 가용성 곱셈(예: AZ 99.95% × AZ 99.95% = 99.9% Multi-AZ)으로 산정되므로 **구성 요소의 정확한 SLI 매트릭스 설계** 없이는 거버넌스가 불가능하다.

SRE(Site Reliability Engineering) 문화가 Google을 통해 정형화되면서, "**100%는 잘못된 목표**"라는 전제하에, 잔여 에러 버짓을 Release Engineering과 SRE가 공유하는 모델이 표준화되었다. 이로 인해 SLI -> SLO -> SLA의 3계층 모델은 단순한 문서 산출물이 아니라, **릴리즈 게이팅(Deployment Gating), 인시던트 대응, 용량 계획(Capacity Planning), 재해 복구(DR) 훈련**까지 관통하는 운영 거버넌스의 척도가 되었다.

```text
+-----------------------------------------------------------------------------+
|              SLA / SLO / SLI 계층 구조 및 운영 거버넌스 흐름도                |
+-----------------------------------------------------------------------------+
|                                                                             |
|   [고객/법무]                                                                 |
|       | 계약                                                                  |
|       v                                                                      |
|  +--------------------------------------------------------------------+     |
|  |  SLA (Service Level Agreement)  <- 계약/법적 의무 + 금전적 크레딧    |     |
|  |  • 대상: 비즈니스 단위(예: 전자상거래 결제 서비스)                    |     |
|  |  • 항목: 가용성 99.9%, 응답시간 p95 < 300ms, RTO 4h                   |     |
|  |  • 위반 시: 월 이용료 10% 크레딧, SLO 미달 누적 시 계약 해지         |     |
|  +--------------------------------------------------------------------+     |
|       | 분해                                                                  |
|       v                                                                      |
|  +--------------------------------------------------------------------+     |
|  |  SLO (Service Level Objective)   <- 엔지니어링 목표 + 에러버짓        |     |
|  |  • 대상: 서비스 단위(예: payment-api, order-api)                      |     |
|  |  • 항목: 30일 rolling window 기준 availability ≥ 99.95%              |     |
|  |  • 에러버짓: 0.05% = 30일 기준 21.6분의 허용 다운타임                |     |
|  +--------------------------------------------------------------------+     |
|       | 측정                                                                  |
|       v                                                                      |
|  +--------------------------------------------------------------------+     |
|  |  SLI (Service Level Indicator)   <- 원시 측정값 + 집계 방식            |     |
|  |  • 대상: 엔드포인트/메서드 단위(예: POST /charge)                     |     |
|  |  • 항목: (good events / total valid events) × 100                    |     |
|  |  • 예: HTTP 2xx 응답 수 / 전체 HTTP 응답 수 - 401(인증실패 제외)      |     |
|  +--------------------------------------------------------------------+     |
|       |                                                                      |
|       v                                                                      |
|  +--------------------------------------------------------------------+     |
|  |  Observability Pipeline (Prometheus / OpenTelemetry / Datadog)       |     |
|  |  -> SLO 대시보드 -> Multi-Window Multi-Burn-Rate Alert -> PagerDuty     |     |
|  +--------------------------------------------------------------------+     |
|                                                                             |
+-----------------------------------------------------------------------------+
```

**왜 필요한가? - 기존 vs 신규 패러다임 비교**

| 비교 차원 | 전통적 ITIL SLA (2000년대) | SRE 기반 SLO (2016년~) |
| :--- | :--- | :--- |
| **측정 단위** | 시스템/서버 단위 (서버 가동률) | 사용자 트랜잭션/요청 단위 |
| **목표 설정** | "최대한 100%에 가깝게" | "100%는 비용 대비 비효율, 에러버짓으로 통제" |
| **위반 대응** | 사후 RMA, 분쟁 | 사전 Burn-rate Alert, SLO-Based Release Gating |
| **조직 책임** | 서비스 데스크 + 운영팀 분립 | Dev + SRE 공동 책임 (Shared Ownership) |
| **지표 종류** | 가용성 위주 (Uptime) | 가용성 + 지연시간(Latency) + 처리량(Throughput) + 내구성(Durability) |
| **집계 방식** | 월 1회 보고서 | 실시간 카운터, Rolling 28~30일 |

- **📢 섹션 요약 비유**: SLA는 "손해배상 조항이 달린 이사 계약서"이고, SLO는 "이사 완료까지 3일 이내"라는 약속, SLI는 "실제 짐을 다 옮기는 데 걸린 시간을 초 단위로 재는 스톱워치"입니다. 손해배상(크레딧)은 계약서(SLA)에, 약속(SLO)은 협상 기준에, 측정(SLI)은 매일의 데이터에서 옵니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. SLI(SLI) 설계의 4가지 핵심 원칙 (Google SRE Workbook 기반)

Google SRE Workbook은 모든 SLI가 다음 4가지 사용자 질문을 만족해야 한다고 명시한다.

1. **(Availability)**: "사용자가 이 서비스를 *사용하려고* 했을 때, *사용할 수 있었는가?*"
2. **(Latency)**: "사용자가 *얼마나 빨리* 응답을 받았는가?"
3. **(Throughput)**: "사용자가 *얼마나 많은* 작업을 단위 시간당 처리했는가?" (Firestore 같은 시스템에 적용)
4. **(Durability)**: "사용자가 저장한 데이터가 *여전히 존재하는가?* (지속성)"

이 4질문은 본질적으로 **사용자 여정(User Journey) 중심**으로 SLI를 정의하도록 강제한다. 예를 들어 `GET /api/orders/{id}` 엔드포인트의 Availability SLI는 다음과 같이 정의된다.

```
Availability SLI = Good Events / Valid Events
                 = {HTTP 2xx & 3xx responses} / {전체 응답 - 인증실패(401) - 잘못된요청(400)}
```

**중요**: 분모에서 401/400을 제외하는 이유는, **인증 실패는 "서비스의 실패"가 아니라 "유효하지 않은 이벤트가 발생했음"**을 의미하기 때문이다. 이로써 SLI는 "시스템이 정상 동작했는가"에 집중한다.

### 2. SLO의 수학적 정의: 에러 버짓(Error Budget) 공식

SLO는 "목표"이므로 그것을 위반한 정도를 정량화한 것이 **에러 버짓 소진율(Budget Burn Rate)**이다.

```
1. 가용성 SLO를 α라 하면 (예: 99.9% = 0.999)
2. 에러 버짓 = 1 - α = 0.1% = 0.001

3. SLO 윈도우 W (예: 30일 = 2,592,000초)
4. 허용 다운타임 = (1 - α) × W = 0.001 × 2,592,000 = 2,592초 ≈ 43.2분

5. Burn Rate (소진율) = 실제 다운타임 / SLO 윈도우 시간
                       = (1 - SLI) / (1 - α)
```

예를 들어, SLO가 99.9%이고 측정된 SLI가 99.0%라면:
- 1% × 30일 = 7.2시간 다운타임 발생
- 7.2시간 / 43.2분 = **10x Burn Rate** -> 한 달의 에러버짓을 3일 만에 소진

### 3. Multi-Window Multi-Burn-Rate (MWMB) 알림 모델

단순 임계치 알림(예: "가용성 99% 미만 시 알림")은 **지나치게 늦거나 너무 잦은 알림**을 야기한다. Google SRE Workbook이 제시한 MWMB는 두 개의 윈도우를 교차 검증하여 **신호 정확도(precision)와 재현율(recall)을 동시**에 높인다.

```text
+--------------------------------------------------------------------------+
|          Multi-Window Multi-Burn-Rate Alert (2-Threshold 모델)            |
+--------------------------------------------------------------------------+
|                                                                          |
|   페이즈 1:  Fast Burn (1시간 윈도우, Burn Rate ≥ 14.4x)                  |
|   +--------------------------------------------------------+             |
|   | SLO 99.9% 기준 1시간 동안 다운타임 ≥ 4.32분              |             |
|   | -> 2일 안에 30일 에러버짓을 모두 소진할 속도                |             |
|   | -> 페이지(PagerDuty) 즉시 발송, 1차 on-call 대응           |             |
|   +--------------------------------------------------------+             |
|                                                                          |
|   페이즈 2:  Slow Burn (6시간 윈도우, Burn Rate ≥ 6x)                    |
|   +--------------------------------------------------------+             |
|   | 6시간 동안 99.5% 미만으로 지속 시 페이지 발송              |             |
|   | -> 5일 안에 에러버짓 소진, 티켓 생성 후 작업 착수           |             |
|   +--------------------------------------------------------+             |
|                                                                          |
|   [Prometheus Rule 예시]                                                  |
|   expr: (sum(rate(http_requests_total{status!~"5xx"}[1h])) /             |
|         sum(rate(http_requests_total[1h]))) < 0.9986                      |
|   AND                                                                      |
|         (sum(rate(http_requests_total{status!~"5xx"}[6h])) /             |
|         sum(rate(http_requests_total[6h]))) < 0.9994                      |
|   for: 2m                                                                 |
|   labels: { severity: page, slo: availability-999 }                       |
|                                                                          |
+--------------------------------------------------------------------------+
```

### 4. 아키텍처 구성 요소별 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **측정 레이어 (Instrumentation)** | 사용자 트랜잭션 단위로 good/bad 이벤트 카운팅 | OpenTelemetry SDK, Prometheus client_jvm/node_exporter, Envoy WASM 필터로 HTTP status code, response_size, grpc_status_code 태깅 |
| **집계 엔진 (Metrics Pipeline)** | 시계열 DB로 카운터 저장, multi-window 집계 계산 | Prometheus(via Recording Rules), Thanos/Cortex(장기 저장), InfluxDB, VictoriaMetrics, ClickHouse for high-cardinality |
| **SLO 계산기 (SLO Engine)** | SLI/SLO/Error Budget을 동적 계산, burn-rate 산출 | Sloth (https://sloth.dev, Prometheus SLO generator), Kuberhealthy, Cloud Operations SLO API (GCP), nobl9, Pyrra |
| **알림 라우터 (Alert Manager)** | MWMB 룰 평가, SLO-aware 페이지 발송 | Alertmanager (Prometheus), Grafana Alerting, Datadog Monitor, PagerDuty Event Rules + Incident Workflow |
| **거버넌스 대시보드** | 서비스별 SLO, 잔여 버짓, 릴리즈 영향 시각화 | Grafana SLO Dashboards, Datadog SLO UI, ServiceNow SLO Tracking, Gremlin Chaos Engineering |
| **릴리즈 게이트 (Deployment Gating)** | 신규 배포가 잔여 버짓을 위협하는지 사전 평가 | Spinnaker Pipeline + SLO plugin, Argo Rollouts + AnalysisTemplate, Flagger (Istio), Keptn SLI-provider |
| **감사/보고 (Audit/Reporting)** | SLA 크레딧 계산, 컴플라이언스 리포트 | ServiceNow GRC, Vanta, Drata (SOC2), 내부 BPM 워크플로우 |

### 5. 지표 유형별 SLI 공식 디테일

| SLI 유형 | 공식 (식) | 구현 시 주의사항 |
| :--- | :--- | :--- |
| **가용성 (Availability)** | `successful_requests / total_valid_requests` | 4xx를 모두 "good"으로 처리하면 SLI가 부풀려짐. 4xx 중 5xx와 동등한 서버 결함(예: rate-limit 429, 회로차단 503)은 bad 이벤트로 분류 필요 |
| **지연시간 (Latency)** | `requests_faster_than_T / total_requests` | **임계값 T** 설정이 핵심. 일반적으로 p95/p99 응답시간 또는 SLO 목표치(예: 300ms) 초과 비율. **T 이하의 요청만 good**으로 카운트 |
| **처리량 (Throughput)** | `processed_events / ingested_events` | Kafka, Pub/Sub, Flink 같은 스트리밍 시스템에 적용. Backpressure 시나리오에서 lag time이 SLI가 될 수 있음 |
| **내구성 (Durability)** | `records_still_readable / records_written` | `scrub_test` (주기적 무결성 검증) 결과를 카운팅. GCS WORM 정책, S3 Object Lock과 연계 |
| **정확성 (Correctness)** | `correct_outputs / total_outputs` | ML 추론, 검색 시스템의 NDCG@10, 결제 정합성 등에서 사용. 일반 시스템에선 적용 어려움 |

### 6. SLO 윈도우 선택과 그 함정

- **Calendar Month (1일~말일)**: 고객 보고에 직관적이나, 월말 클러스터링(연말/월말 트래픽 편중) 시 왜곡 발생
- **Rolling 30 Days (Trailing)**: 평활화 효과, **이력 분포가 안정적**, 권장 방식 (Google SRE 권장)
- **Rolling 28 Days**: 4주(7×4) 단위라 회계/회고 주기와 정합, 주말/평일 패턴에 의한 변동 흡수
- **Sprint-bound Window**: 애자일 팀 내부 목표용, 외부 SLA 보고에는 부적합

### 7.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 543 / 600

<- **이전**: [542. 변경 관리 CAB 영향 분석 승인](/knowledge-base/studynote/11_design_supervision/06_exam_summary/543_change_management_cab_impact_analysis/)
**다음**: [544. 연속성 관리 BCP DRP 재해 복구](/knowledge-base/studynote/11_design_supervision/06_exam_summary/544_continuity_management_bcp_drp_recovery/) ->

---
