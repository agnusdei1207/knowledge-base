---
title: "Data Catalog 데이터 카탈로그 (Data Catalog)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 309
---

# 📖 【암기용】 개념 완전 이해

> 목적: Data Catalog를 조직의 데이터 자산을 검색하고 이해하며 책임·품질·권한 정보를 확인하는 metadata 관리 체계로 이해하게 만든다.

## 한눈에
- **개요**: 데이터 자산의 위치, 스키마, 의미, 소유자, 품질, 권한, lineage를 관리하는 검색형 metadata 저장소
- **왜 필요한가**: 데이터가 많아질수록 어떤 테이블을 써야 하는지, 누가 책임지는지, 품질과 접근 조건이 무엇인지 알기 어렵다.
- **핵심 직관**: 도서관의 검색 시스템처럼 책 제목만이 아니라 저자, 주제, 위치, 대출 가능 여부, 관련 도서를 함께 보여준다.

## 깊이 이해
- **배경·문제의식**: 데이터 레이크와 웨어하우스에 테이블은 많지만 의미와 최신성이 불명확하면 사용자는 같은 데이터를 반복 생성한다.
- **작동 원리**: 데이터 catalog는 connector로 metadata를 수집하고 business glossary, tag, owner, lineage, quality score, access workflow를 연결한다.
- **비유**: 쇼핑몰 상품 페이지에 상품명, 상세 설명, 판매자, 리뷰, 재고, 반품 정책이 있어야 구매자가 선택할 수 있는 것과 같다.
- **구체 예시**: `customer_master` 테이블을 검색하면 PII tag, owner, refresh 주기, downstream report, 접근 신청 링크, 품질 규칙 통과 여부가 함께 표시된다.
- **흔한 오해·주의점**: Data Catalog는 테이블 목록 페이지가 아니다. 신뢰할 수 있는 metadata와 운영 프로세스가 없으면 오래된 링크 모음이 된다.

## 연결 개념
- Data Lineage — 데이터 흐름과 영향 분석
- Data Governance — 소유권, 정책, 품질 통제
- Data Mesh — 데이터 제품 검색과 계약 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Data Catalog는 검색 기능이 아니라 metadata 수집, 의미 관리, 접근 통제, 품질·lineage 연결을 답해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Data Catalog는 조직 데이터 자산의 기술·업무·운영 metadata를 수집하고 검색·거버넌스에 활용하는 체계임.
> 2. **가치**: 사용자는 데이터 의미, 소유자, 품질, 권한, lineage를 확인해 중복 생성과 오사용을 줄임.
> 3. **판단 포인트**: metadata freshness, glossary, ownership, lineage, access workflow, quality integration이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| metadata 관리 이해 확인 | technical/business/operational metadata | 테이블 검색 UI로만 설명 |
| 거버넌스 적용 판단 확인 | owner, glossary, classification, access | 데이터 저장소와 혼동 |
| 운영 지표 확인 | catalog coverage, freshness, usage | 도입 효과를 정성 표현으로만 작성 |

> 요약: 이 문제는 catalog를 데이터 검색과 거버넌스를 연결하는 metadata 운영 체계로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 데이터 자산 metadata 목록
- 배경: 데이터 자산 증가로 위치, 의미, 품질, 접근 조건을 찾는 시간이 늘고 중복 데이터가 생성됨.
- 필요성: 데이터 사용자는 catalog에서 소유자, 품질, lineage, 접근 절차를 확인해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Data Sources -> Metadata Connector -> Catalog Repository
       +-> Glossary / Tag / Owner
       +-> Lineage / Quality / Access Workflow -> Data Consumer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Metadata Connector | DB, lake, BI, pipeline metadata 수집 | 자동 수집 필요 |
| Catalog Repository | 자산, 스키마, tag, owner 저장 | graph model 활용 |
| Business Glossary | 업무 용어와 데이터 의미 연결 | 표준 용어 관리 |
| Access Workflow | 권한 신청과 승인 이력 관리 | 감사 로그 |

> 요약: Data Catalog는 기술 metadata와 업무 의미, 접근 절차를 한곳에서 연결해야 사용 가능한 자산 목록이 된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
소스 스캔 -> metadata 수집 -> tag / owner 매핑
-> glossary / lineage 연결 -> 검색 / 접근 신청 -> 사용량 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 데이터 소스에서 스키마·통계·권한 수집 | connector success |
| 2 | 민감정보 tag와 owner를 매핑 | classification accuracy |
| 3 | 업무 용어와 lineage를 연결 | glossary coverage |
| 4 | 검색·접근·사용 기록을 운영 metadata로 반영 | usage tracking |

> 요약: Catalog는 metadata를 수집한 뒤 검색, 접근, 품질, lineage 피드백으로 지속 갱신한다.

---

## Ⅳ. 특징

| 구분 | 파일/테이블 목록 | Data Catalog | 판단 기준 |
|:---|:---|:---|:---|
| 정보 범위 | 이름·위치 | 의미·소유자·품질·lineage | 데이터 탐색 요구 |
| 갱신 방식 | 수동 문서 | connector 기반 자동 수집 | freshness 요구 |
| 거버넌스 | 별도 승인 | 접근 workflow와 감사 | 규제 대상 여부 |
| 소비 경험 | 검색 후 별도 문의 | 검색·이해·신청 통합 | self-service 수준 |

> 요약: Data Catalog는 목록 관리가 아니라 데이터 소비자가 안전하게 선택하도록 metadata 맥락을 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 검색 | 위키·문서 | 자동 수집 catalog | 자산 수와 변경 빈도 |
| 의미 관리 | 담당자 문의 | glossary, tag, owner | 업무 용어 혼선 |
| 접근 | 티켓 수동 승인 | catalog workflow | 개인정보·감사 요구 |

> 요약: 데이터 자산이 많고 소유권·권한 문의가 반복되면 catalog 기반 self-service를 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| metadata 노후화 | 수동 등록 의존 | 자동 connector와 freshness SLA | stale asset ratio |
| owner 부재 | 조직 책임 미정의 | domain owner 지정 | unowned asset count |
| 민감정보 노출 | tag·권한 연계 누락 | classification, masking workflow | policy violation |

> 요약: Catalog 리스크는 오래된 metadata, owner 부재, 민감정보 노출이며 자동 수집과 책임 지정으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 커버리지 | 핵심 소스 90% 이상 catalog 등록 | source inventory 대조 |
| 최신성 | metadata freshness SLA 준수 | scan timestamp |
| 활용도 | 검색 후 접근 신청·조회 추적 | catalog analytics |

> 요약: Catalog 성과는 등록 수보다 커버리지, 최신성, 실제 사용량으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. DB, lakehouse, BI, pipeline 도구별 connector를 우선 연결하고 핵심 자산부터 owner와 tag를 보정함.
2. business glossary, PII classification, access workflow, quality score를 catalog 화면과 API에 통합함.
3. stale asset, unowned asset, low-quality asset을 주기 리포트로 추적하고 도메인 owner에게 개선 티켓을 발행함.

**결론 (2줄):**
- 기술사 판단: Catalog는 도구 설치보다 metadata 운영 책임과 갱신 자동화가 선행되어야 함.
- 향후 방향: Data Catalog는 lineage, quality, semantic layer와 결합해 AI agent가 신뢰할 수 있는 enterprise context로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Data Catalog를 설명하시오" | metadata 수집과 검색·접근 흐름 | 단순 목록과 차이 |
| 요구사항 명시형 | "데이터 거버넌스 구현 방안을 제시하시오" | owner·tag·workflow 운영 | freshness·민감정보 리스크 |

> 요약: 설명형은 catalog 구조를, 방안형은 metadata 운영 책임과 접근 통제를 중심으로 작성한다.
