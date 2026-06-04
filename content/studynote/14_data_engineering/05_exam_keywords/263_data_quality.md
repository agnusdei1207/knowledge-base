+++
title = "263. 데이터 품질 관리 프로파일링 정합성 검증 (Data Quality Management Profiling Validation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 프로파일링은 컬럼/테이블/시스템 단위의 통계적·구조적 메타데이터(Min/Max, Cardinality, Null 비율, 데이터 타입, Functional Dependency 등)를 추출해 *데이터의 실제 분포*를 가시화하는 것이고, 정합성 검증(Consistency/Validity/Integrity 검증)은 정의된 DQ Rule(구문·의미·참조·논리 규칙) 엔진이 *기대 분포와 실제 분포의 편차*를 측정·차단·통보하는 제어 루프(Control Loop)다.
> 2. **가치**: Gartner에 따르면 평균적인 조직이 처리하는 데이터의 **30~40%가 품질 기준 미달**(회색데이터, Dark Data)이며, DQ 자동화를 적용한 기업은 데이터 다운스트림 ETL 오류율 **60~80% 감소**, 데이터 거버넌스 SLA 미준수 건수 **45% 감소**, 머신러닝 모델 성능 회귀 **2~3배 조기탐지** 효과를 얻는다. 한국 공공·금융 도메인에서는 NIA의 3등급(우수/양호/미흡) 진단 체계를 만족하기 위한 필수 통제이다.
> 3. **판단 포인트**: (a) **룰 기반 vs ML/통계 기반**(Anomaly Detection, Auto-Detection) (b) **샘플링 전략**(전수 vs 1~5% SRS vs 계층화) (c) **배치 vs 실시간**(Kafka Streams, Flink 기반 스트리밍 DQ) (d) **중심화 vs 페데레이션**(중앙 DQ 허브 vs 도메인별 Data Owner 책임) (e) **Sink-side(검출) vs Source-side(차단) 통제**의 아키텍처 선택이 검증의 신뢰도와 운영비용을 결정한다.

---

## Ⅰ. 개요 및 필요성

데이터는 4차 산업혁명의 *원유*라기보다는 *대장간 원자재*에 가깝다. 아무리 정교한 알고리즘도 **GIGO(Garbage In, Garbage Out)** 원칙을 넘어설 수 없으며, ETL/ELT 파이프라인이 폭증하면서 데이터 결함은 한 노드에서 다른 노드로 *전파·증폭*된다. 통계청·NIA 조사에서 한국大中型 기업의 **데이터 활용 실패 원인 1위가 "신뢰할 수 없는 데이터"**(평균 38.7%)이며, IDC는 *"Poor data quality costs the average organization $12.9M annually"*로 추산했다.

특히 데이터 레이크(Data Lake)·레이크하우스(Lakehouse)·스트리밍 분석으로 패러다임이 이동하면서 **Schema-on-Read** 환경에서 데이터 결함이 사일로에 숨어 들어가는 *Schema Drift*, *Semantic Drift*, *Data Drift* 문제가 대두되었다. 또한 GDPR·개인정보보호법·AI 신뢰성 법안(EU AI Act) 등 컴플라이언스 요구가 데이터의 *근거성(Provenance)*과 *정합성(Consistency)*을 입증 가능한 형태로 관리할 것을 요구한다.

**프로파일링(Profiling)**은 *데이터에 대한 메타데이터를 자동 추출*하는 발견(Discovery) 단계이고, **정합성 검증(Validation)**은 *정의된 기대치를 위반하는 레코드를 차단·표시*하는 통제(Control) 단계다. 둘은 별개가 아니라 **PDCA(Plan-Do-Check-Act) 사이클의 "Check" 단계**를 구성하며, 데이터 카탈로그·리니지·컨트랙트와 결합되어 데이터 거버넌스의 *척추*를 형성한다.

```text
  +----------------------------------------------------------------------+
  |     데이터 품질 관리(데이터 거버넌스) - PDCA & 피드백 루프           |
  |                                                                      |
  |   PLAN(규칙정의)        DO(프로파일링·수집)      CHECK(검증·측정)    |
  |  +--------------+    +------------------+    +------------------+    |
  |  | 비즈니스 룰 |---->| 프로파일링 엔진  |---->| DQ Rule Engine   |    |
  |  | 메타데이터  |    | (Great Expect.)  |    | (Informatica IDQ)|    |
  |  | 표준코드    |    | Apache Griffin   |    | Soda / Deequ     |    |
  |  | 마스터 룰  |    | Deequ / Soda     |    | Ataccama / DQ    |    |
  |  +------+-------+    +--------+---------+    +--------+---------+    |
  |         |                     |                       |             |
  |         |  +------------------v------------------+    |             |
  |         |  |  메타데이터 저장소 (DQ Score Catalog)|    |             |
  |         |  |  - 컬럼 단위 통계/룰 위반 이력       |    |             |
  |         |  |  - 리니지 그래프 (OpenLineage)       |    |             |
  |         |  +------------------+------------------+    |             |
  |         |                     |                       |             |
  |         |                     v                       v             |
  |         |           +------------------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 263 / 300

<- **이전**: [262. 데이터 리니지 혈통 추적 영향도 분석 (Data Lineage Impact Analysis Provenance)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/262_data_lineage/)
**다음**: [264. 마스터 데이터 관리 MDM 골든 레코드 (Master Data Management MDM Golden Record)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/264_mdm_master_data/) ->

---
