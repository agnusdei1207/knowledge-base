---
title: "ISO/PAS 8800 AI Safety (ISO/PAS 8800)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 337
extra:
  question_no: "337"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- ISO/PAS 8800은 자동차 안전 관련 시스템에서 AI 사용 시 고려할 위험과 개발 통제를 다루는 공개 사양임
- 기능안전 중심의 ISO 26262와 의도된 기능 안전 중심의 SOTIF를 AI 특성 관점에서 보완하는 흐름으로 이해하면 좋음
- 데이터 품질과 모델 한계와 분포 변화와 운영 모니터링이 핵심 안전 포인트임

## Ⅰ. 개요

- **정의/개념**: ISO/PAS 8800은 도로 차량의 안전 관련 전기전자 시스템에 AI 기술을 적용할 때 데이터와 모델과 학습과 운영 조건에서 발생하는 AI 특유의 위험을 식별하고 통제하기 위한 자동차 AI 안전 지침임
- **배경/필요성**: 자율주행과 ADAS에 AI가 확대되면서 기존 규칙 기반 소프트웨어 안전 기준만으로는 학습 데이터 편향과 불확실성과 분포 변화 위험을 충분히 설명하기 어려워짐

## Ⅱ. 특징

- 데이터와 모델 성능 한계와 운영 조건을 안전 관점에서 함께 관리함
- 기능안전과 SOTIF와 결합해 AI 특화 위험을 보완하는 성격이 강함
- 개발 단계뿐 아니라 운영 중 모니터링과 업데이트 통제까지 중요하게 봄
- 모델 정확도 수치만 높아도 안전 사례가 성립하는 것은 아니라는 점을 분명히 함

## Ⅲ. 종류 및 비교

| 판단 기준 | ISO 26262 | ISO/PAS 21448 SOTIF | ISO/PAS 8800 |
|:---|:---|:---|:---|
| 핵심 초점 | 기능 고장 안전 | 의도된 기능의 한계 | AI 기반 안전 위험 |
| 주요 대상 | E/E 시스템 고장 | 센서/알고리즘 한계 | 데이터와 모델과 운영 변화 |
| 위험 예시 | 하드웨어 고장 | 인지 오검출 | 학습 편향과 분포 변화 |
| 운영 요구 | 개발 검증 중심 | 시나리오 검증 | 지속 모니터링과 업데이트 관리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| AI Item Definition and Safety Context | 어떤 AI 기능이 어떤 ODD와 안전 목표 안에서 동작하는지 정의해 안전 논의의 범위를 고정하는 출발점임 |
| Data and Model Governance | 학습 데이터 품질과 라벨링과 버전과 모델 변경 이력을 관리해 AI 위험의 원인을 추적 가능하게 만드는 거버넌스 계층임 |
| Performance Limitation and Uncertainty Management | 모델 성능 한계와 불확실성과 취약 조건을 문서화해 안전 사례에 반영하는 분석 계층임 |
| Verification Validation and Safety Case | 시뮬레이션과 실제 주행과 시나리오 검증을 통해 AI 기능이 안전 목표를 만족하는지 입증하는 검증 계층임 |
| Operational Monitoring and Update Control | 운영 중 성능 저하와 분포 변화를 감시하고 안전한 업데이트 절차를 유지해 현장 안전성을 지속 관리하는 운영 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| AI Item /   | -> | Data Model  | -> | V&V / Safety| -> | Runtime     |
| ODD Context |    | Governance  |    | Case        |    | Monitoring  |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| AI 기능 정의   | -> | 데이터/모델 위험 분석 | -> | 시나리오 검증  | -> | 안전 사례 작성 | -> | 운영 감시/업데이트 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **AI 기능 정의**: AI 적용 범위와 ODD와 안전 목표를 정함
2. **데이터와 모델 위험 분석**: 편향과 불확실성과 성능 한계를 식별함
3. **시나리오 검증**: 안전 관련 상황에서 AI 동작을 검증함
4. **안전 사례 작성**: 안전 근거와 제한 조건을 정리함
5. **운영 감시와 업데이트**: 현장 데이터와 모델 변경을 지속 통제함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 학습 데이터 분포와 실제 도로 환경 분포가 달라지면 출시 시점 검증만으로는 운영 안전성을 유지하기 어려울 수 있음
   - 해결방안: distribution shift monitoring과 field data feedback governance를 적용하고 detected drift response time과 post release performance degradation rate로 검증함
2. 문제: 모델 성능 지표를 안전 요구와 직접 연결하지 못하면 정확도가 높아도 안전 사례가 설득력을 갖기 어려울 수 있음
   - 해결방안: safety linked performance criteria와 risk scenario traceability matrix를 적용하고 safety requirement to metric trace coverage와 unresolved safety assumption count로 검증함
3. 문제: 지속 업데이트 환경에서 모델 변경 승인 절차가 약하면 성능 개선 명목의 변경이 안전 위험을 다시 도입할 수 있음
   - 해결방안: safety gated model update pipeline과 rollback ready deployment policy를 적용하고 safety reviewed model release coverage와 update rollback readiness score로 검증함

## Ⅶ. 적용 사례

- ADAS AI 조직이 분포 변화 감시 체계를 운영하며 확인 지표는 detected drift response time와 post release performance degradation rate임
- 안전 엔지니어링 팀이 안전 연계 성능 기준을 적용하며 확인 지표는 safety requirement to metric trace coverage와 unresolved safety assumption count임
- 차량 AI 배포 체계가 안전 게이트 기반 업데이트를 적용하며 확인 지표는 safety reviewed model release coverage와 update rollback readiness score임

## Ⅷ. 결론

ISO/PAS 8800은 AI 성능 평가를 안전 사례로 연결하는 기준이므로 데이터와 모델과 운영 변화를 한 묶음으로 관리할 때 의미가 생김.
