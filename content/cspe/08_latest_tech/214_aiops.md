---
title: "AIOps (Artificial Intelligence for IT Operations)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 214
extra:
  question_no: "214"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- AIOps는 로그와 메트릭과 이벤트를 AI로 분석해 IT 운영의 탐지와 상관분석과 대응을 자동화하는 체계임
- 핵심 가치는 경보 폭주를 줄이고 장애 원인 파악과 복구 시간을 단축하는 데 있음
- 자동 조치 수준이 높아질수록 데이터 품질과 정책 통제가 더 중요해짐

## Ⅰ. 개요

- **정의/개념**: AIOps는 IT 인프라와 애플리케이션에서 발생하는 대규모 운영 데이터를 머신러닝과 통계 분석으로 처리하여 이상 징후 탐지와 이벤트 상관분석과 원인 추정과 자동 복구를 지원하는 운영 체계임
- **배경/필요성**: 멀티클라우드와 마이크로서비스 환경에서 운영 데이터가 폭증하면서 사람이 로그와 알람을 직접 상관분석해 장애를 대응하는 방식의 한계가 분명해짐

## Ⅱ. 특징

- 단순 모니터링을 넘어 이상 패턴 학습과 경보 축약과 자동화 조치를 함께 수행함
- 로그와 메트릭과 트레이스와 티켓 데이터를 결합할수록 원인 추정 정확도가 높아짐
- MTTD와 MTTR 개선이 대표 성과 지표임
- 잘못된 자동 조치는 장애를 확산시킬 수 있어 human override와 정책 통제가 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | AIOps | 전통적 IT 운영 | MLOps |
|:---|:---|:---|:---|
| 대상 | 로그, 이벤트, 인프라, 서비스 | 수동 모니터링과 룰 기반 운영 | ML 모델 생애주기 |
| 핵심 기능 | anomaly detection, RCA, automation | threshold alert, 수동 조치 | training, deployment, drift |
| 대표 지표 | MTTD, MTTR, alert reduction | 장애 건수 | model accuracy, retrain time |
| 주요 리스크 | 오탐 자동조치, 데이터 품질 문제 | 알람 피로 | 운영 모델 품질 저하 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Telemetry Collector | 로그와 메트릭과 트레이스와 변경 이력을 수집해 분석 가능한 공통 데이터 평면을 만드는 계층임 |
| Event Correlation Engine | 다수 알람을 하나의 장애 사건으로 묶어 노이즈를 줄이고 사건 단위를 재구성하는 분석 엔진임 |
| Anomaly and RCA Model | 정상 패턴에서 벗어난 이상을 탐지하고 근본 원인 후보를 추정해 운영자의 판단 시간을 줄이는 모델임 |
| Automation Orchestrator | 승인된 런북과 스크립트를 호출해 재시작과 스케일링과 격리 같은 복구 조치를 수행하는 실행 계층임 |
| Operator Console | 사건 흐름과 원인 후보와 자동 조치 이력을 제공해 운영자가 최종 통제권을 유지하게 하는 인터페이스임 |

```text
+-----------+    +------------------+    +----------------+    +------------------+
| Telemetry | -> | Correlation      | -> | Anomaly/RCA    | -> | Automation/Console|
+-----------+    +------------------+    +----------------+    +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 수집  | -> | 이벤트 묶기  | -> | 이상 탐지    | -> | 원인 추정    | -> | 조치 또는 승인 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 수집**: 다양한 운영 데이터 소스를 통합 수집함
2. **이벤트 묶기**: 관련 알람을 서비스 단위 사건으로 묶음 처리함
3. **이상 탐지**: 통계와 ML로 정상 패턴 이탈을 탐지함
4. **원인 추정**: 연관 그래프와 과거 사건으로 근본 원인 후보를 추정함
5. **조치 또는 승인**: 런북 자동화나 운영자 승인 후 복구를 실행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 품질이 낮은 로그와 중복 알람이 그대로 유입되면 이상 탐지 정확도가 낮아지고 경보 피로가 커질 수 있음
   - 해결방안: telemetry normalization과 event deduplication을 적용하고 alert reduction rate와 noisy event ratio로 검증함
2. 문제: 자동 복구 정책이 과도하면 잘못된 재시작이나 스케일 조치가 장애 범위를 오히려 확대할 수 있음
   - 해결방안: risk tiered automation과 human approval gate를 적용하고 failed auto remediation rate와 change induced incident rate로 검증함
3. 문제: 운영 데이터 소스가 분절되면 원인 추정이 편향되어 MTTR 개선 효과가 제한될 수 있음
   - 해결방안: unified observability platform과 topology aware correlation을 적용하고 root cause precision과 MTTR improvement rate로 검증함

## Ⅶ. 적용 사례

- 클라우드 운영 센터가 알람 중복 제거와 사건 상관분석을 적용하며 확인 지표는 alert reduction rate와 MTTD improvement rate임
- 전자상거래 플랫폼이 장애 자동복구를 승인 기반으로 운영하며 확인 지표는 failed auto remediation rate와 MTTR improvement rate임
- 금융 서비스가 서비스 토폴로지 기반 RCA를 도입하며 확인 지표는 root cause precision과 change induced incident rate임

## Ⅷ. 결론

AIOps는 운영 데이터 홍수를 줄여 장애 대응을 가속하는 체계이지만 자동화 수준이 높을수록 데이터 표준화와 정책 통제가 함께 강화되어야 함.
