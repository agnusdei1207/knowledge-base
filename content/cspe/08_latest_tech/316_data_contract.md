---
title: "Data Contract 데이터 계약 (Data Contract)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 316
extra:
  question_no: "316"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Data Contract는 데이터 생산자와 소비자가 스키마와 의미와 품질 기준을 합의한 운영 계약임
- API contract와 비슷하지만 데이터 품질과 갱신 주기와 진화 규칙까지 포함하는 점이 다름
- 이벤트 스트림과 분석 테이블과 데이터 제품 운영에서 핵심 통제 장치로 쓰임

## Ⅰ. 개요

- **정의/개념**: Data Contract는 데이터 생산자와 소비자가 데이터 구조와 의미와 품질 기준과 변경 정책과 책임 주체를 명시해 데이터 교환을 예측 가능하게 만드는 운영 계약임
- **배경/필요성**: 데이터 파이프라인이 늘수록 스키마 변경과 의미 해석 차이와 품질 불일치가 잦아져 단순 문서화가 아니라 검증 가능한 합의 기준이 필요해짐

## Ⅱ. 특징

- 스키마뿐 아니라 의미와 품질과 SLA를 함께 다루어 데이터 사용성을 높임
- 생산자 책임을 명확히 해 downstream 파이프라인 안정성을 높임
- CI CD와 검증 도구에 연결하면 계약 위반을 사전에 차단할 수 있음
- 문서만 남고 검증 자동화가 없으면 실제 운영에서는 계약 효력이 약해질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Contract | Schema Registry | API Contract |
|:---|:---|:---|:---|
| 다루는 범위 | 구조, 의미, 품질, 변경 정책 | 스키마 버전 | 요청/응답 인터페이스 |
| 핵심 가치 | 데이터 신뢰와 협업 기준 | 직렬화 호환성 | 서비스 연동 안정성 |
| 운영 주체 | 생산자와 소비자 공동 | 플랫폼 중심 | 서비스 개발팀 |
| 대표 활용 | 스트림, 테이블, 데이터 제품 | 이벤트 포맷 관리 | API 연동 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Schema Definition | 필드 구조와 타입과 필수 여부를 정의해 기본 형식 호환성을 보장하는 계약의 최소 단위임 |
| Semantic and Business Rules | 컬럼 의미와 코드 체계와 계산 기준을 명시해 같은 값이 조직마다 다르게 해석되는 위험을 줄이는 의미 계층임 |
| Quality and SLA Terms | 허용 결측률과 freshness와 중복 기준을 명시해 소비자가 기대할 운영 품질 수준을 명확히 하는 서비스 약속 계층임 |
| Compatibility and Change Policy | breaking change와 비호환 변경 절차를 정의해 생산자 변경이 소비자 장애로 번지지 않도록 제어하는 진화 규칙임 |
| Validation and Enforcement Pipeline | 계약 검증을 테스트와 배포 게이트에 연결해 문서가 아닌 실행 가능한 통제로 만드는 자동화 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Producer    | -> | Contract    | -> | Validation  | -> | Consumer    |
| Ownership   |    | Definition  |    | / Gate      |    | Trust       |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 계약 정의     | -> | 검증 규칙 작성 | -> | 배포 전 검사   | -> | 운영 모니터링 | -> | 변경 관리     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **계약 정의**: 생산자와 소비자가 구조와 의미와 품질 기준을 합의함
2. **검증 규칙 작성**: 스키마와 품질과 호환성 검사를 자동화함
3. **배포 전 검사**: 변경 사항이 계약 위반인지 확인함
4. **운영 모니터링**: 실제 freshness와 품질을 계약 기준과 비교함
5. **변경 관리**: 비호환 변경은 공지와 이행 기간을 거쳐 반영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 계약이 스키마 수준에만 머물면 의미와 품질 기준이 빠져 소비자 관점의 신뢰 문제를 해결하지 못할 수 있음
   - 해결방안: semantic rule extension과 quality SLA template를 적용하고 contract semantic completeness score와 SLA breach detection rate로 검증함
2. 문제: 배포 게이트에 계약 검증이 연결되지 않으면 생산자 변경이 실제 운영 장애로 전파될 수 있음
   - 해결방안: CI contract validation과 breaking change approval workflow를 적용하고 pre production contract violation catch rate와 downstream break incident count로 검증함
3. 문제: 소비자 요구가 과도하게 분화되면 계약이 늘어나 관리 복잡도와 협업 비용이 급증할 수 있음
   - 해결방안: canonical contract model과 consumer segmentation policy를 적용하고 contract reuse ratio와 custom contract maintenance cost로 검증함

## Ⅶ. 적용 사례

- 이벤트 플랫폼이 의미 규칙과 SLA를 포함한 계약을 운영하며 확인 지표는 contract semantic completeness score와 SLA breach detection rate임
- 데이터 배포 파이프라인이 계약 검증 게이트를 적용하며 확인 지표는 pre production contract violation catch rate와 downstream break incident count임
- 데이터 제품 조직이 표준 계약 모델을 도입하며 확인 지표는 contract reuse ratio와 custom contract maintenance cost임

## Ⅷ. 결론

Data Contract는 문서가 아니라 변경과 품질을 제어하는 실행 기준이므로 의미 규칙과 검증 자동화를 함께 갖출 때 실효성이 생김.
