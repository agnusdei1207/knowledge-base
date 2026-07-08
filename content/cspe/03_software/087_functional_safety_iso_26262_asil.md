---
title: "기능 안전 ISO 26262·ASIL (Functional Safety ISO 26262)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 87
extra:
  question_no: "087"
  exam_status: "기출"
  exam_history: "134회"
---

## 미리 알고가기

- ISO 26262는 자동차 전기전자 시스템의 기능 안전 국제 표준임
- ASIL은 위험도에 따라 안전 요구 강도를 구분하는 등급 체계임
- 안전 목표는 시스템 고장 시 운전자와 탑승자에게 미치는 영향을 줄이기 위해 정의됨

## Ⅰ. 개요

- **정의/개념**: ISO 26262는 자동차 전기전자 시스템의 위험을 분석해 안전 목표와 요구사항과 검증 활동을 생명주기 전반에 배치하는 기능 안전 표준이며, ASIL은 위험 심각도와 노출도와 제어 가능도를 조합해 요구 강도를 구분하는 등급 체계임
- **배경/필요성**: 차량 소프트웨어와 ECU 복잡도가 높아지면서 단일 고장이 대형 사고로 연결될 수 있으므로, 설계와 검증과 운영 변경까지 통제하는 체계적 안전 기준이 필요함

## Ⅱ. 특징

- HARA를 통해 위험 시나리오를 먼저 정의하고 안전 목표를 도출함
- ASIL 등급에 따라 개발 프로세스와 검증 깊이와 독립성 요구가 달라짐
- 시스템과 하드웨어와 소프트웨어 안전 요구를 계층적으로 할당함
- 변경 관리와 생산 이후 운영까지 포함하므로 단발성 시험으로 끝나지 않음

## Ⅲ. 종류 및 비교

| 판단 기준 | QM | ASIL A~D |
|:---|:---|:---|
| 위험 수준 | 일반 품질 관리 수준 | 기능 안전 통제가 필요한 수준 |
| 개발 통제 | 일반 개발 절차 | 위험도에 비례한 강화 절차 |
| 검증 강도 | 상대적으로 낮음 | ASIL이 높을수록 강화 |
| 적용 대상 | 안전 영향이 낮은 기능 | 안전 목표와 연결된 기능 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| HARA | 위험 사건을 식별하고 ASIL을 산정해 안전 활동의 기준선을 만듦 |
| Safety Goal | 허용 불가능한 위험을 막기 위한 상위 안전 목표를 정의함 |
| Technical Safety Requirement | 시스템과 ECU 수준으로 분해된 안전 요구를 구현과 시험 항목으로 연결함 |
| Verification and Validation | 독립 검토와 시험과 안전 사례 평가로 요구 충족 여부를 증명함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| HARA 수행      | --> | 안전 목표 정의  | --> | 요구 할당      | --> | 검증/안전 사례 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **HARA 수행**: 위험 사건별 심각도와 노출도와 제어 가능도를 평가함
2. **안전 목표 정의**: 허용 불가능한 위험을 막는 목표를 설정함
3. **요구 할당**: 시스템과 하드웨어와 소프트웨어 요구로 분해함
4. **검증 및 안전 사례**: 시험과 리뷰로 충족 근거를 누적함

## Ⅵ. 문제점 및 해결 방안

1. 문제: HARA가 기능 경계와 운용 상황을 충분히 반영하지 못하면 ASIL 산정이 실제 위험보다 낮아질 수 있음
   - 해결방안: 시나리오 기반 HARA와 cross-functional review를 운영하고 scenario coverage ratio와 ASIL reclassification count로 검증함
2. 문제: 상위 안전 목표가 하위 소프트웨어 요구로 정확히 추적되지 않으면 검증 누락이 발생할 수 있음
   - 해결방안: end-to-end traceability를 구축하고 requirement trace completeness와 orphan requirement count로 검증함
3. 문제: 차량 출시 후 변경 사항이 안전 사례에 반영되지 않으면 인증 상태와 실제 구성이 어긋날 수 있음
   - 해결방안: change impact assessment를 의무화하고 post-release safety review timeliness와 safety case freshness로 검증함

## Ⅶ. 적용 사례

- ADAS 제어기 개발에서는 HARA와 ASIL 산정을 수행하고 확인 지표는 scenario coverage ratio와 ASIL reclassification count임
- ECU 소프트웨어 검증에서는 요구 추적성을 관리하고 확인 지표는 requirement trace completeness와 orphan requirement count임
- 양산 이후 차량 업데이트 관리에서는 안전 사례를 재검토하고 확인 지표는 post-release safety review timeliness와 safety case freshness임

## Ⅷ. 결론

ISO 26262의 실무 가치는 표준 준수 자체보다 위험 기반으로 안전 목표와 개발 증거를 끝까지 연결해 출시 후 변경까지 통제하는 데 있음.
