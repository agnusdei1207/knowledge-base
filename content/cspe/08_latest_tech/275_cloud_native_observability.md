---
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 275
---

# 📖 【암기용】 개념 완전 이해

> 목적: 클라우드 네이티브 관측성을 컨테이너·MSA·동적 인프라에서 시스템 내부 상태를 metric, log, trace, event로 추론하는 운영 체계로 이해하게 만든다.

## 한눈에
- **개요**: 분산 시스템의 내부 상태를 metrics, logs, traces, events로 수집·상관분석해 장애 원인과 SLO 상태를 파악하는 체계
- **왜 필요한가**: Kubernetes와 MSA는 Pod가 계속 생성·삭제되고 호출 경로가 동적으로 바뀌어 서버별 모니터링만으로 원인 추적이 어렵다.
- **핵심 직관**: 한 건물의 전기 계량기만 보는 것이 아니라 각 방의 온도, 출입 기록, 이동 경로를 함께 보는 운영 방식이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 네이티브 환경은 autoscaling, rolling update, service mesh, ephemeral pod 때문에 장애 위치와 원인이 배포·스케일 이벤트마다 달라진다.
- **작동 원리**: 애플리케이션과 인프라가 OpenTelemetry 등으로 telemetry를 생성하고 collector가 backend로 전달해 SLO, RED, USE 지표와 trace를 분석한다.
- **비유**: 병원에서 심박수, 혈압, 검사 기록, 진료 동선을 함께 봐야 환자 상태를 판단하는 것과 같다.
- **구체 예시**: checkout API의 p95 latency가 500ms를 넘으면 trace에서 payment service span 지연을 찾고, 해당 Pod의 CPU throttling metric을 확인한다.
- **흔한 오해·주의점**: 관측성은 로그를 많이 쌓는 일이 아니다. 질문에 답할 수 있는 telemetry와 SLO 기준, cardinality 통제가 함께 있어야 한다.

## 연결 개념
- OpenTelemetry — metric, log, trace 수집 표준
- Service Mesh — 서비스 간 telemetry와 mTLS 상태 제공
- SRE/SLO — 관측 지표를 사용자 영향 기준으로 해석하는 운영 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 클라우드 네이티브 관측성은 telemetry 수집이 아니라 SLO 기반 원인 추적과 운영 의사결정 체계다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cloud Native Observability는 metrics, logs, traces, events로 분산 시스템 상태와 사용자 영향을 추론하는 운영 체계임.
> 2. **가치**: ephemeral workload와 MSA 호출 경로에서 장애 원인, error budget, 배포 영향도를 분 단위로 판별함.
> 3. **판단 포인트**: OpenTelemetry 표준화, cardinality 통제, SLO 연결, sampling 정책을 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측성 개념 이해 확인 | metric, log, trace, event, SLO | 모니터링 대시보드 나열로 축소 |
| 클라우드 네이티브 특성 확인 | ephemeral pod, autoscaling, service graph | 서버별 CPU 감시만 설명 |
| 운영 판단 확인 | RED/USE, error budget, cardinality, sampling | 로그 전량 저장을 해결책으로 서술 |

> 요약: 이 문제는 telemetry를 사용자 영향과 장애 원인 분석에 연결하는 운영 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 분산 시스템 상태 추론 체계
- 배경: Kubernetes·MSA는 워크로드가 동적으로 이동하고 호출 경로가 분산되어 단일 서버 감시로 장애 원인을 찾기 어려움.
- 필요성: SLO, trace, metric, log를 연결해 배포 영향과 장애 원인을 분 단위로 확인해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
App / Pod / Node / Mesh -> OpenTelemetry SDK / Agent -> Collector
Collector -> Metrics Backend / Log Store / Trace Backend / Event Store
SLO Dashboard / Alert -> Incident Response -> Postmortem
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Instrumentation | 애플리케이션 telemetry 생성 | SDK, auto instrumentation |
| Collector | 수집·가공·전송 중계 | sampling, filtering |
| Backend | metric·log·trace 저장과 조회 | Prometheus, Loki, Tempo 등 |
| SLO/Alert | 사용자 영향 기반 판단 | error budget, burn rate |

> 요약: 관측성 체계는 telemetry 생성, 수집, 저장, SLO 판단, 대응 프로세스를 하나의 폐루프로 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 발생 -> trace context 생성 -> service span 기록
-> metric/log/event 수집 -> collector 가공 -> backend 저장
-> SLO alert 판단 -> trace 기반 원인 분석 -> 대응
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청에 trace id와 span 생성 | trace propagation rate |
| 2 | RED/USE metric과 구조화 log 수집 | label cardinality |
| 3 | collector가 sampling·filtering 수행 | dropped telemetry |
| 4 | SLO alert와 trace drill-down으로 원인 확인 | MTTA, MTTR |

> 요약: 관측성은 요청 단위 trace와 지표를 결합해 alert에서 원인 분석까지 이어지는 흐름으로 동작한다.

---

## Ⅳ. 특징

| 구분 | 전통 모니터링 | Cloud Native Observability | 판단 기준 |
|:---|:---|:---|:---|
| 대상 | 서버·프로세스 중심 | 서비스·워크로드·요청 경로 | MSA 복잡도 |
| 데이터 | metric·log 중심 | metric·log·trace·event 결합 | 원인 추적 필요 |
| 알림 | 임계치 기반 | SLO·error budget 기반 | 사용자 영향 |
| 운영 리스크 | 데이터 적음 | cardinality와 비용 증가 | label 설계 |

> 요약: 클라우드 네이티브 관측성은 인프라 상태보다 사용자 요청 경로와 SLO 영향에 초점을 둔다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서버 모니터링 | telemetry pipeline | ephemeral workload |
| 비용/성능 | 저장량 제한 | high-cardinality 관리 필요 | sampling·retention 정책 |
| 운영/위험 | 단일 장애 지점 분석 | trace·service graph 분석 | 분산 호출 수 |

> 요약: MSA와 Kubernetes에서는 서버별 임계치보다 telemetry pipeline과 SLO 기반 분석이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Cardinality 폭증 | user_id 등 고유 label 사용 | label allowlist | series count |
| Trace 누락 | context propagation 미적용 | 표준 header 전파 | trace completeness |
| 알림 피로 | 임계치 알림 과다 | SLO burn rate alert | alert precision |

> 요약: 관측성 리스크는 cardinality, trace 누락, 알림 피로이며 label 정책과 SLO alert로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 사용자 영향 | SLO 99.9% 등급 충족 | error budget |
| 원인 분석 | MTTA·MTTR 목표 이내 | incident record |
| 비용 | telemetry 저장 비용 예산 이내 | retention·sampling report |

> 요약: 관측성 도입 효과는 SLO, MTTA/MTTR, telemetry 비용으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 API별 SLI를 latency, error rate, availability로 정의하고 SLO와 error budget을 먼저 설정함.
2. OpenTelemetry SDK·Collector를 표준 수집 경로로 지정하고 trace context 전파를 gateway, service, message broker에 적용함.
3. label allowlist, tail sampling, retention 정책을 적용해 cardinality와 저장 비용을 통제함.

**결론 (2줄):**
- 기술사 판단: Kubernetes·MSA 운영에서는 metric만으로 원인 분석이 제한되므로 trace·log·event를 SLO에 연결한 관측성을 선택함.
- 향후 방향: 관측성은 AIOps, service mesh, eBPF telemetry와 결합되어 자동 원인 분석과 정책 기반 복구로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "클라우드 네이티브 관측성을 설명하시오" | telemetry pipeline과 SLO alert 흐름 | 전통 모니터링 대비 차이 |
| 요구사항 명시형 | "MSA 장애 대응 방안을 제시하시오" | trace 기반 원인 분석 절차 | cardinality·알림 피로 리스크 |

> 요약: 설명형은 관측성 구성요소를, 운영형은 SLO와 원인 분석 절차를 중심으로 작성한다.
