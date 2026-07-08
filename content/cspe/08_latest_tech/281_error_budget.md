---
title: "Error Budget 오류 예산 (Error Budget)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 281
extra:
  question_no: "281"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- Error Budget은 SLO에서 허용 가능한 실패 범위를 수치화한 운영 여유치임
- 안정성과 배포 속도를 균형 있게 조절하는 실전 의사결정 장치로 쓰임
- SLI와 SLO가 정의되지 않으면 Error Budget도 의미를 가지기 어려움

## Ⅰ. 개요

- **정의/개념**: Error Budget은 일정 기간 동안 SLO를 위반하지 않고 서비스가 허용할 수 있는 실패량 또는 품질 저하 한도를 수치로 표현한 운영 통제 지표임
- **배경/필요성**: 서비스 안정성을 무한정 높이려 하면 출시 속도와 실험 속도가 떨어지므로 허용 가능한 실패 범위를 정량화해 의사결정 기준으로 삼을 필요가 생김

## Ⅱ. 특징

- 신뢰성과 출시 속도의 균형점을 명확한 숫자로 제시함
- 배포 중단과 안정화 우선순위를 정하는 기준으로 활용됨
- 예산 소진 속도를 보면 위험한 운영 패턴을 조기에 감지할 수 있음
- 사용자 영향과 무관한 지표를 쓰면 판단 기준이 왜곡될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Error Budget | SLO | SLA |
|:---|:---|:---|:---|
| 역할 | 허용 실패량 계산 | 운영 품질 목표 | 외부 계약 기준 |
| 활용 시점 | 배포와 운영 의사결정 | 품질 관리 | 계약 준수 |
| 유연성 | 높음 | 높음 | 낮음 |
| 대표 질문 | 얼마나 더 실패할 수 있는가 | 무엇을 목표로 하는가 | 무엇을 보장해야 하는가 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| SLI Baseline | 성공률과 지연 시간 같은 실제 측정 지표가 Error Budget 계산의 입력 기준이 됨 |
| SLO Target | 허용 가능한 목표 수준이 정의되어야 예산 규모를 산정할 수 있는 목표 기준선임 |
| Time Window | 일간과 주간과 월간 단위의 측정 기간이 예산 소진 속도와 의사결정 민감도를 결정함 |
| Burn Rate Tracker | 현재 예산이 얼마나 빠르게 소진되는지 계산해 위험 상태를 조기 탐지하는 분석 계층임 |
| Governance Policy | 예산 상태에 따라 배포 중단과 변경 제한과 안정화 조치를 시행하는 운영 규칙임 |

```text
+-------+    +---------+    +--------------+    +----------------+
| SLI   | -> | SLO     | -> | Error Budget | -> | Governance     |
+-------+    +---------+    +--------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 지표 정의    | -> | 목표 설정    | -> | 예산 계산    | -> | burn rate 측정 | -> | 배포/복구 판단 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **지표 정의**: 사용자 경험을 반영하는 SLI를 선택함
2. **목표 설정**: 기간과 목표 SLO를 수립함
3. **예산 계산**: 허용 가능한 실패량을 수치화함
4. **burn rate 측정**: 현재 예산 소진 속도를 추적함
5. **배포와 복구 판단**: 예산 상태에 맞춰 운영 결정을 내림

## Ⅵ. 문제점 및 해결 방안

1. 문제: 사용자 체감과 무관한 SLI로 예산을 계산하면 배포 차단 기준이 실제 품질과 어긋날 수 있음
   - 해결방안: user journey aligned SLI selection을 적용하고 budget to user impact correlation score와 false halt rate로 검증함
2. 문제: burn rate만 보고 맥락 없이 대응하면 일시적 스파이크에도 과도한 변경 중단이 발생할 수 있음
   - 해결방안: multi window burn analysis와 contextual incident review를 적용하고 alert precision과 unnecessary freeze rate로 검증함
3. 문제: Error Budget을 의사결정 정책에 연결하지 않으면 보고용 숫자로만 남아 운영 개선 효과가 사라질 수 있음
   - 해결방안: release gating policy와 reliability review workflow를 적용하고 budget based release decision rate와 preventable incident reduction rate로 검증함

## Ⅶ. 적용 사례

- SRE 조직이 사용자 여정 기반 SLI를 적용하며 확인 지표는 budget to user impact correlation score와 false halt rate임
- 플랫폼 팀이 다중 창 burn 분석을 운영하며 확인 지표는 alert precision과 unnecessary freeze rate임
- 배포 운영 체계가 예산 연계 게이팅을 사용하며 확인 지표는 budget based release decision rate와 preventable incident reduction rate임

## Ⅷ. 결론

Error Budget은 신뢰성과 변화 속도를 함께 다루는 운영 지표이므로 사용자 중심 SLI와 실질적 거버넌스 정책이 결합되어야 가치가 생김.
