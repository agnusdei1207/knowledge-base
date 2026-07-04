---
title: "AIOps (Artificial Intelligence for IT Operations)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 214
---

# 📖 【암기용】 개념 완전 이해

> 목적: AIOps를 IT 운영 데이터에 AI를 적용해 장애 탐지, 원인 분석, 자동 조치를 수행하는 체계로 이해하게 만든다.

## 한눈에
- **개요**: 로그, 메트릭, 이벤트, 트레이스를 AI로 분석해 IT 운영 장애를 탐지·분석·조치하는 체계
- **왜 필요한가**: 클라우드와 MSA 환경은 이벤트 수가 많고 장애 전파 경로가 복잡해 사람이 알람을 하나씩 해석하기 어렵다.
- **핵심 직관**: AIOps는 관제 화면에 쌓인 신호를 묶어 실제 장애 후보와 원인 후보를 좁히는 운영 분석 엔진임.

## 깊이 이해
- **배경·문제의식**: 전통 NMS와 단순 threshold 알람은 정상 변동과 장애 징후를 구분하지 못해 alert fatigue를 만든다.
- **작동 원리**: 관측 데이터를 수집하고 중복 이벤트를 상관분석하며 이상탐지, RCA, 예측, runbook 자동화를 수행함.
- **비유**: 병원 응급실에서 체온, 혈압, 검사 결과를 함께 보고 환자 우선순위와 원인을 추정하는 triage와 유사함.
- **구체 예시**: 결제 API p95 latency가 200ms에서 1.2초로 상승하고 DB connection error가 동시 증가하면 동일 incident로 묶어 DB pool 고갈을 원인 후보로 제시함.
- **흔한 오해·주의점**: AIOps는 모든 장애를 자동 복구하는 만능 운영자가 아니라 데이터 품질과 runbook 성숙도에 의존하는 보조 체계임.

## 연결 개념
- Observability — 로그·메트릭·트레이스 기반 관측
- SRE — SLO와 error budget 기반 운영 원칙
- Incident Management — 장애 접수, 분석, 복구, 사후 분석 프로세스

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AIOps는 운영 데이터를 AI/ML로 분석해 이상탐지, 이벤트 상관분석, 원인 추정, 자동 조치를 수행하는 IT 운영 체계임.
> 2. **가치**: 알람 중복 제거, MTTA/MTTR 단축, 장애 예측, runbook 자동화로 운영 품질을 수치로 관리함.
> 3. **판단 포인트**: AIOps 도입은 알고리즘보다 로그 표준화, CMDB/토폴로지, SLO, 자동 조치 권한 설계가 우선임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 지능형 IT 운영 이해 확인 | 이상탐지, 이벤트 상관분석, RCA, 자동화 | AI가 장애를 모두 해결한다고 과장 |
| 클라우드 운영 설계 확인 | 로그·메트릭·트레이스, topology, SLO 연결 | 모니터링 도구 목록만 나열 |
| 운영 지표 기반 판단 확인 | MTTA, MTTR, false positive, alert reduction | 정량 지표 없이 효과 설명 |

> 요약: AIOps 문제는 AI 기법 자체보다 운영 데이터와 장애 대응 프로세스를 어떻게 연결하는지 평가함.

---

## Ⅰ. 개요 및 필요성

- 개요: AI 기반 IT 운영
- 배경: MSA와 클라우드는 서비스 간 호출, 동적 인스턴스, 대량 이벤트로 인해 단순 threshold 관제가 한계에 도달함.
- 필요성: alert noise 50% 이상 감소, MTTA 5분 이하, MTTR 30분 이하 같은 운영 목표가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Log/Metric/Trace -> Data Lake -> Correlation Engine
-> Anomaly Detection -> RCA -> Runbook Automation
CMDB/Topology -> Correlation Engine
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Collector | 로그·메트릭·트레이스 수집 | OpenTelemetry 연계 |
| Correlation Engine | 중복 알람과 연관 이벤트 묶음 | topology aware |
| Anomaly Detection | 정상 패턴 대비 이상 신호 탐지 | time-series model |
| RCA Engine | 장애 원인 후보와 영향 범위 추정 | dependency graph |
| Automation | runbook 실행과 ticket 생성 | 승인 단계 필요 |

> 요약: AIOps는 관측 데이터와 토폴로지를 결합해 알람을 incident 단위로 묶고 원인 후보와 조치 절차를 제시함.

---

## Ⅲ. 동작원리 및 흐름도

```text
데이터 수집 -> 정규화 -> 이상탐지
-> 이벤트 상관분석 -> 원인 후보 산출 -> 조치 실행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 로그, 메트릭, 트레이스, 이벤트 수집 | 수집 누락률 1% 이하 |
| 2 | 서비스명, trace ID, severity를 표준화 | 필드 매핑률 95% 이상 |
| 3 | 계절성 기반 이상탐지와 중복 알람 제거 | false positive 10% 이하 |
| 4 | topology와 시간 상관관계로 RCA 수행 | 원인 후보 Top-3 적중률 측정 |
| 5 | 승인된 runbook으로 조치 또는 ticket 발행 | MTTR 30분 이하 |

> 요약: AIOps는 수집·정규화된 운영 데이터를 incident 관점으로 압축하고 RCA와 자동 조치로 연결함.

---

## Ⅳ. 특징

| 구분 | 전통 관제 | AIOps | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 알람 기준 | 고정 threshold | 동적 baseline과 anomaly | false positive 10% 이하 |
| 이벤트 처리 | 개별 알람 확인 | correlation으로 incident 묶음 | alert reduction 50% 이상 |
| 원인 분석 | 담당자 경험 의존 | topology와 시간 상관 분석 | RCA Top-3 적중률 |
| 조치 | 수동 runbook | 승인 기반 자동 실행 | MTTR 30분 이하 |

> 요약: AIOps는 개별 알람 중심 관제를 incident와 SLO 중심 운영으로 바꾸는 기술임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | NMS와 threshold 알람 | 데이터 lake와 AI correlation | 이벤트 일 10만 건 이상 |
| 비용/성능 | 관제 인력 증원 | 알람 압축과 runbook 자동화 | alert noise 50% 이상 목표 |
| 운영/위험 | 수동 RCA | topology 기반 RCA | 서비스 의존관계가 복잡할 때 |

> 요약: AIOps는 이벤트 규모와 서비스 의존성이 커져 수동 관제가 MTTA 목표를 맞추지 못할 때 도입함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 증가 | 로그 품질과 라벨 부족 | 표준 필드, 피드백 라벨링 | false positive 10% 이하 |
| 자동 조치 사고 | runbook 권한 과다 | 승인 단계, blast radius 제한 | 자동 조치 rollback 100% |
| 원인 분석 오류 | topology 정보 누락 | CMDB와 service map 동기화 | 미매핑 서비스 0건 |

> 요약: AIOps 리스크는 데이터 품질, 자동화 권한, 토폴로지 누락에서 발생하므로 운영 통제와 피드백이 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 장애 탐지 | MTTA 5분 이하 | incident timestamp 비교 |
| 복구 시간 | MTTR 30분 이하 | ticket lifecycle 분석 |
| 알람 품질 | alert reduction 50% 이상 | 중복 알람 제거 전후 비교 |

> 요약: AIOps는 MTTA, MTTR, 알람 압축률이 동시에 개선될 때 운영 가치가 검증됨.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. OpenTelemetry 기반으로 service.name, trace_id, error_code, region 필드를 표준화하여 로그·메트릭·트레이스 상관분석률을 95% 이상 확보함.
2. 결제, 로그인, 주문 같은 핵심 서비스부터 SLO와 topology를 등록하고 incident correlation 정책을 적용함.
3. 재시작, scale-out, cache purge 같은 low-risk runbook부터 승인 기반 자동 실행으로 전환함.

**결론 (2줄):**
- 기술사 판단: 관측 데이터 표준화와 service map이 없으면 AIOps보다 observability 정비를 먼저 수행함.
- 향후 방향: AIOps는 SRE, ChatOps, 자동 복구 플랫폼과 결합해 closed-loop 운영으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "AIOps를 설명하시오" | 수집->상관분석->RCA->자동화 흐름 | 전통 관제 대비 차이 |
| 요구사항 명시형 | "장애 대응 개선 방안을 제시하시오" | MTTA/MTTR 중심 운영 절차 | runbook 자동화와 오탐 대응 |

> 요약: 설명형은 지능형 운영 원리, 방안형은 알람 압축·RCA·자동 조치 지표를 중심으로 작성함.
