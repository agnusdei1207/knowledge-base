---
title: "PACELC 정리 (PACELC Theorem)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 118
extra:
  question_no: "118"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- PACELC는 CAP를 확장해 평상시에도 지연과 일관성의 trade-off가 있음을 설명함
- Partition일 때는 Availability 또는 Consistency를, Else에는 Latency 또는 Consistency를 본다
- 분산 DB 설계에서 평시 품질 기준을 설명할 때 유용함

## Ⅰ. 개요

- **정의/개념**: PACELC 정리는 분산 시스템이 네트워크 분할 시에는 가용성과 일관성 중 하나를 더 우선해야 하고, 분할이 없을 때에도 낮은 지연 시간과 강한 일관성 사이에서 다시 선택이 필요하다는 분산 데이터 설계 원리임
- **배경/필요성**: CAP만으로는 평상시 응답 시간과 정합성 설계를 설명하기 어려우므로, 정상 상황까지 포함한 더 현실적인 판단 기준이 필요함

## Ⅱ. 특징

- 분할 상황과 정상 상황의 trade-off를 분리해 설명함
- 저지연을 추구할수록 복제 동기화 강도를 낮추는 유인이 커짐
- 강한 일관성은 분산 환경에서 평시 지연 증가를 수반할 수 있음
- 분산 DB 선택 시 사용자 체감 성능과 정합성 기대를 함께 검토하게 함

## Ⅲ. 종류 및 비교

| 판단 기준 | PC/EC 성향 | PA/EL 성향 |
|:---|:---|:---|
| 분할 시 선택 | 일관성 우선 | 가용성 우선 |
| 평시 선택 | 일관성 유지 | 지연 최소화 |
| 장점 | 데이터 신뢰성 높음 | 응답성 우수 |
| 한계 | 지연과 실패 허용 | stale data 허용 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Partition Mode Policy | 네트워크 단절 시 읽기와 쓰기 허용 범위를 정함 |
| Steady-State Latency Policy | 정상 상황에서 동기 복제 수준과 응답 목표를 정함 |
| Replica Coordination | 복제본 간 합의 강도가 정합성과 지연을 함께 결정함 |
| Service SLO Mapping | 업무별로 지연과 정합성 목표를 연결해 구조 선택에 반영함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 업무 요구 분석   | --> | 분할 정책 설정  | --> | 평시 지연/정합 설정 | --> | SLO 검증      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **업무 요구 분석**: 분할 허용 범위와 응답 시간 목표를 확인함
2. **분할 정책 설정**: partition 시 CP 또는 AP 성향을 정함
3. **평시 지연과 정합 설정**: 정상 시 동기화 강도와 지연 목표를 정함
4. **SLO 검증**: 실제 성능과 정합성 목표를 비교함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 분할 시 정책만 정하고 평상시 지연 비용을 무시하면 서비스 선택이 실제 사용자 경험과 맞지 않을 수 있음
   - 해결방안: latency-consistency budget을 정의하고 p95 latency와 consistency violation rate로 검증함
2. 문제: 시스템별 PACELC 성향을 문서화하지 않으면 운영 중 장애 대응 기준이 제각각이 될 수 있음
   - 해결방안: architecture decision record에 성향을 기록하고 decision traceability와 incident response consistency로 검증함
3. 문제: 강한 일관성이 필요한 업무와 아닌 업무를 같은 저장소 정책으로 묶으면 비용과 성능이 모두 비효율적일 수 있음
   - 해결방안: workload tiering을 적용하고 tier fit score와 over-constrained workload ratio로 검증함

## Ⅶ. 적용 사례

- 글로벌 SaaS DB에서는 지연·정합 예산을 정의하고 확인 지표는 p95 latency와 consistency violation rate임
- 플랫폼 아키텍처 조직에서는 설계 결정을 기록하고 확인 지표는 decision traceability와 incident response consistency임
- 멀티서비스 데이터 플랫폼에서는 workload tiering을 적용하고 확인 지표는 tier fit score와 over-constrained workload ratio임

## Ⅷ. 결론

PACELC의 가치는 분산 저장소를 장애 시 행동뿐 아니라 평상시 지연과 정합성 비용까지 포함해 선택하게 만든다는 데 있음.
