---
title: "DID 분산신원 (Decentralized Identifier)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 350
extra:
  question_no: "350"
  exam_status: "기출"
  exam_history: "132회"
---

## 미리 알고가기

- DID는 중앙 신원 제공자에 종속되지 않는 식별자와 공개키 문서 체계임
- DID는 VC와 지갑과 검증자 생태계와 함께 이해해야 실무 구조가 보임
- 프라이버시 보호와 복구성과 상호운용성 설계가 실제 도입의 핵심 과제임

## Ⅰ. 개요

- **정의/개념**: Decentralized Identifier는 사용자가 스스로 제어 가능한 식별자와 이에 연결된 공개키 및 서비스 엔드포인트 정보를 분산 방식으로 관리해 중앙 기관 없이도 신원 확인과 자격증명 검증을 가능하게 하는 식별 체계임
- **배경/필요성**: 플랫폼 계정과 중앙 ID 제공자 중심 구조는 이동성과 프라이버시와 자격증명 재사용성에 한계가 있어 자기주권형 신원과 검증 가능한 디지털 자격 체계에 대한 요구가 커짐

## Ⅱ. 특징

- 식별자 제어권을 사용자나 조직이 직접 보유할 수 있음
- VC와 결합해 필요한 정보만 선택적으로 제시하는 프라이버시 강화가 가능함
- 특정 플랫폼 계정에 종속되지 않아 신원 이식성과 상호운용성이 높음
- 키 분실 복구와 DID method 난립 문제가 해결되지 않으면 사용자 경험과 운영 일관성이 약해질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Centralized ID | Federated ID | DID |
|:---|:---|:---|:---|
| 신원 제어권 | 서비스 사업자 | 연합 ID 제공자 | 사용자/보유자 |
| 이동성 | 낮음 | 중간 | 높음 |
| 프라이버시 | 사업자 수집 중심 | 제공자 의존 | 선택적 제시 가능 |
| 대표 한계 | 종속성 | 제공자 집중 | 복구/상호운용 복잡성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| DID Identifier | 사용자나 조직을 고유하게 식별하는 문자열로 분산 신원 체계의 기본 주소 역할을 수행함 |
| DID Document | 공개키와 인증 방식과 서비스 엔드포인트를 담아 검증자가 신원 주체의 검증 방법을 해석하게 하는 메타데이터 계층임 |
| Wallet or Agent | 보유자의 키와 자격증명을 저장하고 제시를 관리해 실제 사용자 경험을 담당하는 실행 계층임 |
| Verifiable Credential and Presentation | 발급자와 보유자와 검증자 사이에서 자격증명 발급과 선택적 제시를 가능하게 하는 증명 계층임 |
| Resolver and Registry Layer | DID method에 따라 문서를 찾고 검증해 분산 식별자를 실제 서비스와 연결하는 연계 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| DID         | -> | DID Document| -> | Wallet / VC | -> | Verifier /  |
| Identifier  |    | / Resolver  |    | Presentation|    | Service     |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| DID 생성      | -> | 문서 등록/해결 | -> | VC 발급       | -> | 선택 제시     | -> | 검증/접근 허용 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **DID 생성**: 사용자가 식별자와 키를 생성함
2. **문서 등록과 해결**: DID document를 게시하고 resolver가 찾을 수 있게 함
3. **VC 발급**: 기관이 자격증명을 발급함
4. **선택 제시**: 사용자가 필요한 속성만 제시함
5. **검증과 접근 허용**: 검증자가 문서와 자격증명을 확인함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 키 분실이나 지갑 손실 시 중앙 관리자 없이 복구가 어려우면 대중 사용성이 크게 떨어질 수 있음
   - 해결방안: social recovery model과 enterprise recovery governance를 적용하고 successful recovery rate와 unrecoverable identity incident count로 검증함
2. 문제: DID method와 지갑과 검증 포맷이 다양하면 상호운용성이 낮아 서비스 간 이동성이 제한될 수 있음
   - 해결방안: interoperable credential profile과 conformance certification program을 적용하고 cross wallet verification success rate와 method interoperability coverage로 검증함
3. 문제: 선택적 제시가 제대로 적용되지 않으면 분산신원이라도 서비스 간 추적 가능성이 남아 프라이버시 이점이 줄어들 수 있음
   - 해결방안: privacy preserving presentation design과 correlation risk assessment를 적용하고 unnecessary attribute disclosure rate와 verifier correlation risk score로 검증함

## Ⅶ. 적용 사례

- 신원 플랫폼이 사회적 복구 모델을 운영하며 확인 지표는 successful recovery rate와 unrecoverable identity incident count임
- DID 생태계가 적합성 인증 프로그램을 적용하며 확인 지표는 cross wallet verification success rate와 method interoperability coverage임
- 개인정보 설계팀이 선택 제시 중심 구조를 적용하며 확인 지표는 unnecessary attribute disclosure rate와 verifier correlation risk score임

## Ⅷ. 결론

DID는 중앙 ID 대체 기술이 아니라 제어권과 이동성과 프라이버시를 다시 설계하는 체계이므로 복구와 상호운용성과 선택 제시 품질이 도입 성패를 좌우함.
