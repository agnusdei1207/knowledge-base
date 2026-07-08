---
title: "Data Mesh 데이터 메시 (Data Mesh)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 307
extra:
  question_no: "307"
  exam_status: "기출"
  exam_history: "123회, 135회"
---

## 미리 알고가기

- Data Mesh는 중앙 데이터팀이 모든 파이프라인을 통제하던 구조를 도메인 분산형 데이터 제품 모델로 바꾸는 접근임
- 핵심 원칙은 domain ownership, data as a product, self serve platform, federated governance임
- 기술 스택보다 조직 책임과 운영 모델 변화가 더 큰 성공 요인임

## Ⅰ. 개요

- **정의/개념**: Data Mesh는 데이터를 중앙 집중 자산이 아니라 각 비즈니스 도메인이 소유하고 서비스하는 데이터 제품으로 보고 공통 플랫폼과 연합 거버넌스를 통해 조직 전체가 이를 자율적으로 생산하고 활용하게 하는 분산형 데이터 아키텍처임
- **배경/필요성**: 중앙 데이터팀에 요청이 몰리는 구조에서는 파이프라인 확장과 품질 개선 속도가 느려져 도메인 지식을 가진 현업 조직이 데이터 책임을 직접 지는 모델이 필요해짐

## Ⅱ. 특징

- 도메인별 데이터 소유권을 명확히 해 변경 책임과 품질 책임을 가까운 곳에 둠
- 데이터를 제품처럼 계약과 SLA와 메타데이터를 갖춘 제공물로 다룸
- 공통 플랫폼은 셀프서비스 기능을 제공하고 거버넌스는 연합형으로 조정함
- 조직 역량 차이가 크면 데이터 품질과 표준 수준이 도메인마다 벌어질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Mesh | Centralized Data Lake | Data Fabric |
|:---|:---|:---|:---|
| 운영 모델 | 도메인 분산 소유 | 중앙 집중 운영 | 메타데이터 자동화 중심 |
| 핵심 성공 요인 | 조직 책임과 계약 | 중앙 플랫폼 역량 | 통합 메타데이터 품질 |
| 거버넌스 방식 | federated governance | 중앙 통제 | 정책 자동화 |
| 대표 장점 | 확장성과 현업 밀착성 | 일관된 표준 | 연결성과 자동화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Domain Data Product | 각 도메인이 소유하는 데이터셋과 API와 문서를 포함해 실제 소비 가능 상태로 제공되는 핵심 단위임 |
| Self Service Data Platform | 저장과 파이프라인과 관측과 보안 기능을 공통 서비스로 제공해 도메인이 인프라 세부 구현 없이 제품을 운영하게 하는 기반 계층임 |
| Federated Governance Council | 품질과 보안과 메타데이터 표준을 중앙 강제 대신 합의 기반 규칙으로 운영해 자율성과 일관성을 균형 있게 맞추는 조정 계층임 |
| Data Contract and SLA | 스키마와 갱신 주기와 품질 조건을 명문화해 공급자와 소비자 간 기대치를 운영 가능한 계약으로 만드는 통제 장치임 |
| Discoverability Layer | 카탈로그와 계보와 검색 기능을 제공해 분산된 데이터 제품을 조직 전체가 찾고 재사용하게 하는 활용 촉진 계층임 |

```text
+-------------+    +-------------+    +-------------+
| Domain A DP |    | Domain B DP |    | Domain C DP |
+-------------+    +-------------+    +-------------+
        \              |              /
         \             |             /
          v            v            v
           +-----------------------+
           | Self Service Platform |
           +-----------------------+
                     |
                     v
           +-----------------------+
           | Federated Governance  |
           +-----------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 도메인 식별   | -> | 데이터 제품화  | -> | 계약/메타 등록 | -> | 공통 플랫폼 운영 | -> | 소비/피드백     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **도메인 식별**: 비즈니스 경계와 책임 조직을 기준으로 데이터 소유 단위를 정함
2. **데이터 제품화**: 데이터셋과 API와 문서와 SLA를 제품 형태로 구성함
3. **계약과 메타 등록**: 스키마와 품질과 접근 정책을 카탈로그에 등록함
4. **공통 플랫폼 운영**: 도메인이 셀프서비스 기능으로 적재와 모니터링과 보안을 수행함
5. **소비와 피드백**: 소비 조직이 활용하며 품질과 사용성 피드백을 다시 공급자에게 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 도메인별 데이터 역량 차이가 크면 제품 품질과 운영 안정성이 조직 전체에서 불균형하게 나타날 수 있음
   - 해결방안: domain enablement program과 minimum product standard를 적용하고 compliant data product ratio와 domain onboarding lead time으로 검증함
2. 문제: 데이터 계약과 메타데이터 표준이 약하면 분산 소유 구조가 오히려 재사용성 저하와 중복 구축으로 이어질 수 있음
   - 해결방안: mandatory data contract policy와 catalog quality gate를 적용하고 reusable product discovery rate와 contract completeness score로 검증함
3. 문제: 자율성을 강조하는 과정에서 보안과 규정 준수 기준이 도메인마다 다르게 해석될 수 있음
   - 해결방안: federated policy templates와 centralized audit automation을 적용하고 policy deviation count와 governed access coverage로 검증함

## Ⅶ. 적용 사례

- 대기업 데이터 조직이 도메인 온보딩 프로그램을 운영하며 확인 지표는 compliant data product ratio와 domain onboarding lead time임
- 분석 플랫폼이 데이터 계약 기반 등록 절차를 적용하며 확인 지표는 reusable product discovery rate와 contract completeness score임
- 규제 산업이 연합 거버넌스 정책 템플릿을 운영하며 확인 지표는 policy deviation count와 governed access coverage임

## Ⅷ. 결론

Data Mesh는 저장 기술보다 조직 책임 재설계가 핵심이므로 도메인 자율성과 연합 거버넌스를 동시에 운영할 수 있을 때 효과가 커짐.
