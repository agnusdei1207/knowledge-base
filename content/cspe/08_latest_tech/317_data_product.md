---
title: "Data Product 데이터 제품 (Data Product)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 317
extra:
  question_no: "317"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Data Product는 단순 데이터셋이 아니라 소유자와 SLA와 문서와 접근 경로를 갖춘 소비 가능한 데이터 제공물임
- Data Mesh와 self service platform 논의에서 핵심 단위로 자주 등장함
- 기술 구현보다 제품 책임과 사용성 설계가 성패를 좌우함

## Ⅰ. 개요

- **정의/개념**: Data Product는 특정 업무 목적을 위해 데이터를 수집하고 정제하고 문서화해 소유자와 품질 기준과 접근 인터페이스를 갖춘 재사용 가능한 데이터 제공물임
- **배경/필요성**: 데이터셋은 많아졌지만 의미와 책임과 품질이 불명확해 재사용성이 낮아지면서 데이터를 소비자 관점의 제품으로 설계하려는 요구가 커짐

## Ⅱ. 특징

- 사용자 관점에서 발견성과 이해성과 신뢰성을 함께 제공함
- 소유자와 SLA가 명확해 품질 문제와 변경 책임을 추적하기 쉬움
- API와 테이블과 이벤트 등 다양한 전달 형식을 제품 형태로 통합할 수 있음
- 제품화 수준이 낮으면 단순 데이터셋 포장에 그쳐 운영 부담만 늘 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Product | Raw Dataset | BI Report |
|:---|:---|:---|:---|
| 핵심 목적 | 재사용 가능한 데이터 서비스 | 저장 자산 보관 | 의사결정 화면 제공 |
| 소유 책임 | 명확함 | 불명확한 경우 많음 | 보고서 소유자 중심 |
| 포함 요소 | 데이터, 문서, SLA, 인터페이스 | 데이터 자체 | 시각화 결과 |
| 소비 방식 | 직접 조회, API, 이벤트 | 추가 가공 필요 | 조회 중심 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Product Owner and Steward | 비즈니스 책임자와 데이터 운영자가 함께 제품 방향과 품질과 변경 관리를 책임지는 소유 체계임 |
| Curated Data Asset | 소비 목적에 맞게 정리된 핵심 데이터와 스키마가 실제 가치 전달의 중심이 되는 내용 계층임 |
| Access Interface | SQL 테이블과 API와 스트림 등 소비 경로를 제공해 다양한 사용자 유형이 동일 제품을 활용하게 하는 전달 계층임 |
| Documentation and Metadata | 정의와 예시와 계보와 사용 제한을 제공해 소비자가 자율적으로 제품을 이해하고 활용하게 하는 설명 계층임 |
| SLA and Observability | freshness와 품질과 사용량을 측정해 제품을 운영 가능한 서비스 수준으로 관리하는 운영 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Owner       | -> | Curated Data| -> | Interface   | -> | Consumers   |
+-------------+    +-------------+    +-------------+    +-------------+
        \_____________________________________/
              Documentation / SLA / Metrics
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 수요 정의     | -> | 데이터 제품화  | -> | 문서/지표 공개 | -> | 소비/피드백    | -> | 개선/진화     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **수요 정의**: 해결할 업무 문제와 소비자를 명확히 정함
2. **데이터 제품화**: 핵심 데이터와 인터페이스와 품질 기준을 구성함
3. **문서와 지표 공개**: 카탈로그와 문서와 SLA를 제공함
4. **소비와 피드백**: 실제 사용자 활용과 피드백을 수집함
5. **개선과 진화**: 사용 패턴과 변경 요구를 반영해 제품을 고도화함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 소유자 책임이 불명확하면 품질 이슈와 변경 요청이 장기간 방치되어 제품 신뢰도가 빠르게 하락할 수 있음
   - 해결방안: named ownership policy와 product operating model을 적용하고 product owner assignment coverage와 unresolved quality issue age로 검증함
2. 문제: 사용량과 SLA와 만족도 지표가 없으면 데이터 제품이 실제 가치가 있는지 판단하기 어려워질 수 있음
   - 해결방안: product KPI dashboard와 consumer feedback loop를 적용하고 monthly active consumers와 SLA attainment rate로 검증함
3. 문제: 소비자별 맞춤 요구를 그대로 수용하면 유사 제품이 남발되어 재사용성과 운영 효율이 동시에 떨어질 수 있음
   - 해결방안: canonical product portfolio와 reuse first review를 적용하고 duplicate product count와 cross team reuse ratio로 검증함

## Ⅶ. 적용 사례

- 데이터 제품 조직이 명시적 소유 체계를 운영하며 확인 지표는 product owner assignment coverage와 unresolved quality issue age임
- 사내 데이터 포털이 제품 KPI 대시보드를 제공하며 확인 지표는 monthly active consumers와 SLA attainment rate임
- 플랫폼 거버넌스가 재사용 우선 심사를 운영하며 확인 지표는 duplicate product count와 cross team reuse ratio임

## Ⅷ. 결론

Data Product는 데이터를 잘 저장하는 개념이 아니라 소비자에게 반복적으로 가치를 전달하는 단위이므로 소유 책임과 서비스 지표가 반드시 함께 있어야 함.
