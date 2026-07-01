---
title: "Data Fabric 데이터 패브릭 (Data Fabric)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 308
---

# 📖 【암기용】 개념 완전 이해

> 목적: Data Fabric을 분산된 데이터 환경을 metadata, knowledge graph, automation으로 연결하는 통합 데이터 관리 아키텍처로 이해하게 만든다.

## 한눈에
- **개요**: 여러 클라우드·온프레미스 데이터 자산을 metadata 기반으로 연결하고 자동화하는 데이터 아키텍처
- **왜 필요한가**: 데이터가 DB, lakehouse, SaaS, 파일, 스트리밍 시스템에 흩어지면 검색, 접근, 품질, 보안 정책이 분리된다.
- **핵심 직관**: 서로 다른 도시를 도로, 표지판, 교통 규칙, 내비게이션으로 연결해 이동 경로를 추천하는 방식임.

## 깊이 이해
- **배경·문제의식**: 기업 데이터는 물리적으로 통합하기 어렵고, 모든 데이터를 한 저장소로 옮기면 비용·지연·규제 문제가 생긴다.
- **작동 원리**: 데이터 fabric은 metadata 수집, catalog, lineage, knowledge graph, policy engine, integration pipeline을 결합해 데이터 검색·접근·통제를 자동화한다.
- **비유**: 백화점 모든 매장을 한 층으로 옮기지 않고, 통합 안내판과 결제·보안 규칙을 붙여 고객이 필요한 매장을 찾게 하는 구조임.
- **구체 예시**: 고객 데이터가 CRM, DW, lakehouse에 분산되어도 metadata graph가 식별자, 품질, 권한, lineage를 연결해 승인된 사용자에게 적정 위치의 데이터를 제공한다.
- **흔한 오해·주의점**: Data Fabric은 ETL 도구 하나가 아니다. metadata를 중심으로 통합, 거버넌스, 보안, 자동화를 묶는 아키텍처 패턴이다.

## 연결 개념
- Data Catalog — metadata 수집과 검색 계층
- Data Lineage — 데이터 이동과 변환 추적
- Data Mesh — 조직 소유권 중심 접근과 상호 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Data Fabric은 물리 통합보다 active metadata, knowledge graph, policy automation을 중심으로 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Data Fabric은 분산 데이터 환경을 active metadata와 자동화로 연결하는 통합 데이터 관리 아키텍처임.
> 2. **가치**: 데이터 이동을 최소화하면서 검색, 접근, 품질, lineage, 보안 정책을 일관된 경험으로 제공함.
> 3. **판단 포인트**: metadata ingestion, knowledge graph, policy engine, virtualization/integration, observability가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터 통합 아키텍처 이해 확인 | active metadata, graph, automation | ETL 파이프라인으로만 설명 |
| Data Mesh와 비교 판단 확인 | fabric은 기술·metadata 중심, mesh는 조직·제품 중심 | 둘을 대체 관계로 단정 |
| 운영 통제 역량 확인 | 권한, 품질, lineage, 정책 자동화 | 검색 포털 기능만 설명 |

> 요약: 이 문제는 Data Fabric을 metadata 기반 통합·자동화 구조로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: metadata 기반 데이터 연결망
- 배경: 멀티클라우드와 SaaS 확산으로 데이터 위치, 의미, 권한, 품질 정보가 시스템별로 분리됨.
- 필요성: 물리적 이관 없이도 데이터 검색, 접근, 정책 적용, lineage 추적을 통합해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Data Sources -> Metadata Ingestion -> Knowledge Graph / Catalog
        +-> Policy / Quality / Lineage Engine
        +-> Integration / Virtualization -> Consumer / AI / BI
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Metadata Ingestion | 스키마·통계·사용량·권한 정보 수집 | active metadata |
| Knowledge Graph | 자산·용어·관계 연결 | semantic layer |
| Policy Engine | 접근통제·마스킹·규제 정책 적용 | RBAC/ABAC |
| Integration Layer | batch, streaming, CDC, virtualization 연결 | 물리 이동 최소화 |

> 요약: Data Fabric은 metadata graph와 정책 엔진을 통해 분산 데이터 자산을 통합 경험으로 제공한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
소스 연결 -> metadata 수집 -> graph 관계 생성
-> 정책 / 품질 규칙 적용 -> 데이터 접근 경로 추천 -> lineage / usage 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DB, lake, SaaS, stream에서 metadata 수집 | connector coverage |
| 2 | 용어, 소유자, lineage, 품질 정보를 graph로 연결 | relationship completeness |
| 3 | 사용자·목적·분류에 따라 접근 정책 적용 | policy decision log |
| 4 | 사용량과 품질 결과를 metadata에 반영 | freshness, DQ score |

> 요약: Data Fabric은 수집한 metadata를 다시 정책·추천·품질 자동화에 사용하는 순환 구조다.

---

## Ⅳ. 특징

| 구분 | Data Warehouse | Data Lakehouse | Data Fabric |
|:---|:---|:---|:---|
| 초점 | 정형 분석 저장소 | 통합 저장+테이블 | 분산 자산 연결·자동화 |
| 데이터 이동 | 적재 중심 | lake storage 중심 | 이동·가상화 혼합 |
| 관리 기준 | 스키마·쿼리 | table metadata | active metadata graph |
| 적합 조건 | 표준 BI | 대규모 분석·ML | 멀티환경 통합 거버넌스 |

> 요약: Data Fabric은 저장소를 대체하기보다 여러 저장소 위의 metadata·정책·접근 계층을 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 통합 방식 | 물리 ETL 통합 | metadata 기반 연결 | 데이터 이동 제약 |
| 조직 모델 | 중앙 데이터팀 | 중앙 platform+도메인 협업 | Data Mesh 병행 여부 |
| 자동화 | 수동 catalog 등록 | active metadata 반영 | connector·ML rule 성숙도 |

> 요약: Data Fabric은 데이터 위치를 통합하기 어려운 조직에서 metadata와 정책을 통합하는 방식으로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| metadata 부정확 | connector 누락·수동 입력 | 자동 수집과 owner 검증 | metadata freshness |
| 정책 불일치 | 시스템별 권한 모델 차이 | 중앙 policy engine, ABAC | policy drift count |
| graph 복잡도 | 자산·관계 급증 | 표준 ontology, pruning | graph query latency |

> 요약: Data Fabric 운영 리스크는 metadata 신뢰도, 정책 일관성, graph 확장성으로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결 범위 | 핵심 소스 connector 적용 | source inventory |
| 검색·접근 | 승인된 데이터 접근 성공률 | access workflow log |
| 거버넌스 | 민감정보 자동 분류와 마스킹 적용 | classification audit |

> 요약: Data Fabric 성과는 데이터 이동량이 아니라 metadata 기반 검색·접근·정책 자동화 수준으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 데이터 소스별 connector를 구축하고 schema, owner, usage, lineage, quality metadata를 자동 수집함.
2. 업무 용어, 데이터 도메인, 민감정보 분류를 knowledge graph로 연결하고 ABAC 정책에 반영함.
3. batch, CDC, virtualization 중 데이터 사용 패턴별 접근 방식을 정하고 승인 workflow와 감사 로그를 연결함.

**결론 (2줄):**
- 기술사 판단: 데이터가 물리적으로 분산되고 규제·권한 통제가 복잡한 조직은 Data Fabric을 metadata 우선 아키텍처로 설계해야 함.
- 향후 방향: Data Fabric은 AI agent와 semantic layer가 신뢰할 수 있는 enterprise context를 제공하는 방향으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Data Fabric을 설명하시오" | metadata graph와 정책 적용 흐름 | lakehouse·mesh와 차이 |
| 요구사항 명시형 | "데이터 통합 방안을 제시하시오" | 소스 연결·정책·접근 경로 | metadata 신뢰도와 정책 불일치 대응 |

> 요약: 설명형은 metadata 자동화를, 방안형은 분산 데이터 접근·정책 통제를 중심으로 작성한다.
