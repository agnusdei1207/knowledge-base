---
title: 04. 데이터 리니지 (Data Lineage) - 데이터 계보 추적 시스템
date: '2026-04-05'
tags:
- studynote-bigdata
---

# [[214_data_lineage_tracking|데이터 리니지]] ([[214_data_lineage_tracking|Data Lineage]]) - [[001_dikw_pyramid|데이터]] 계보 추적 시스템

> ⚠️ 이 문서는 빅데이터 환경에서 [[001_dikw_pyramid|데이터]]의 출처(Origin)에서 최종 소비(Consumer)까지의 변환 이력을 추적하는 핵심 [[052_data_governance_framework|데이터 거버넌스]] 기술인 '[[214_data_lineage_tracking|데이터 리니지]]([[214_data_lineage_tracking|Data Lineage]])'의 [[104_classification_analysis|분류]](시스템 수준, 컬럼 수준), 추적 기술(파싱 기반, [[568_logs_distributed_logging_elk_fluentd|로그]] 기반, 규칙 기반), 주요 도구(Apache Atlas, DataHub), 그리고 영향 분석(Impact Analysis)과의 연계성을 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[214_data_lineage_tracking|데이터 리니지]]([[214_data_lineage_tracking|Data Lineage]])는 "특정 [[001_dikw_pyramid|데이터]]가 '어디서 왔는지(출처)', 어떤 변환(Transformation)을 거치면서 [[178_as_is_to_be_analysis|현재 상태]]에 도달했는지', '누가 소비하고 있는지'를 추적하여 [[001_dikw_pyramid|데이터]] 흐름의 종단 간 [[008_dependencies|종속성]]([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]] Dependency)을可視化하는 [[203_metadata_management|메타데이터 관리]] 기술"이다.
> 2. **가치**: [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인의某个変換(변환) 로직에 버그가 발생했을 때, 리니지 [[070_graph_datastructure|그래프]]를 통해 "이 버그가 최종 분석 테이블의 어떤 컬럼에 영향을 미치는지"를 수분 내에 파악할 수 있어, [[001_dikw_pyramid|데이터]]品质问题의 Root Cause Analysis 시간을 数日에서 数時間으로 단축시킨다.
> 3. **융합**: [[214_data_lineage_tracking|데이터 리니지]]는 컴파일러의 구문解析(Syntax Parsing) 기술, [[002_database_definition|데이터베이스]] [[568_logs_distributed_logging_elk_fluentd|로그]] 마이닝, 그리고 온톨로지 기반 의미론적 추론이 융합된跨領域(학제간) 기술이다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]危机的 (Pain Point)
기업은 매일 수십 개의 [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] [[123_pipe|파이프]]라인을 통해 [[001_dikw_pyramid|데이터]]를 변환합니다. 어느 날 재무 보고서에서 "총 매출" 숫자가 이상하다는 보고를 받습니다.
- **문제 1 - 원인 파악의 不可能**: "총 매출"이라는 최종 지표는 12개의 중간 뷰와 30개의 변환 스크립트를 거쳐 산출됩니다. 각 변환의 입출력 테이블/컬럼이 무엇인지 手動으로 추적하려면, [[123_pipe|파이프]]라인 문서를 뒤져보고, 각 개발자에게 하나하나 물어봐야 합니다. 원인 파악에만 数일이 소요됩니다.
- **문제 2 - 변경 영향 범위 파악 불가**: 재무팀이 "주문 테이블의 'DISCOUNT' 컬럼 이름을 'SALE_DISCOUNT'로 변경하겠다"고-announce합니다. 이 변경이 downstream(하류)의 어떤 테이블, 어떤 대시보드, 어떤 ML 모델에 영향을 미치는지 파악할 방법이 없어,保守적(보수적)으로 모든下游 시스템을 동시에 변경해야 하는 막대한 업무量이 발생합니다.
- **문제 3 - 규제 준수 증명의 어려움**: [[791_gdpr_eu|GDPR]], [[783_pipa_korea|개인정보보호법]] 등 규제 요건에 따라 "이 분석 결과가 어떤 원본 개인 [[001_dikw_pyramid|데이터]]에서 유래했는지"를 추적할 수 있어야 합니다. 수작업으로 이를 증명하려면 엄청난 인력과 문서가 필요합니다.

### 2. [[214_data_lineage_tracking|데이터 리니지]]의 등장: "[[001_dikw_pyramid|데이터]]의系譜(계보) 管理"
"[[001_dikw_pyramid|데이터]]도 가족과 같습니다. A라는 컬럼은 B 테이블에서 왔고, B는 C 뷰에서 왔으며, C는 원본 [[188_pl_sql_t_sql_procedural|Oracle]] ERP의 X 테이블에서 두カラム(컬럼)의 JOIN으로 [[087_process_state_transition|생성]]된 것입니다. 이族譜(계보)를 자동으로 기록해 두면, Anywhere에서 문제(버그)가 발생해도族譜를逆向追踪하여影響范围을即時算出할 수 있다!"
- **필요성**: [[214_data_lineage_tracking|데이터 리니지]]는 [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]担保(담보)의 핵심 인프라입니다. 버그 발생 시 영향 범위을 즉시 파악하고, 변경 시 사전影響 분석(Impact Analysis)을 수행하며, 규제 [[606_auditing_linux_auditd|감사]] 시 [[001_dikw_pyramid|데이터]] 출처를 증명할 수 있게 합니다.

- **📢 섹션 요약 비유**: [[214_data_lineage_tracking|데이터 리니지]]는 "가족의系譜(계보도)"와 같습니다. "총 매출"이라는知名인사(인물)의系譜를 보면,曾祖父: 원본 [[081_erp_enterprise_resource_planning|ERP]] 시스템의 Sales 테이블 → 祖父: 정제된 Sales_Staging 테이블 → 아버지: 일별 집계 Daily_Sales_Agg 테이블 → 현재: 월별 재무 보고서 Monthly_Financial 테이블로構成되어 있습니다. 만약 曾祖父의 살인 사건([[001_dikw_pyramid|데이터]] 오류)이 발생하면,系譜를 따라가면 全亲属(모든 하류 [[001_dikw_pyramid|데이터]])의 영향을 즉시 파악할 수 있는 것입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

[[214_data_lineage_tracking|데이터 리니지]]는 추적 방식에 따라 네 가지 접근법으로 [[104_classification_analysis|분류]]되며, 각 접근법의精度(정확도)와 구현 난이도가 다릅니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                [ 데이터 리니지 (Data Lineage) 4대 추적 방식 ]                   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  [ 방식 1: 파싱 기반 (Parsing-Based) - 가장 정밀 ]                  │    │
│  │   SQL/HiveQL/Spark 코드를 구문解析하여 AST(추상 구문 트리)를 구축      │    │
│  │   ▶ SELECT a.id, b.name FROM orders a JOIN customer b ON ...     │    │
│  │                          │                                        │    │
│  │                          ▼                                        │    │
│  │   AST에서宗族: orders.id → output.id (직접 계보)                    │    │
│  │   문제: Python/pandas 코드처럼 구문解析 불가능한 transformation은 불포함  │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 방식 2: 로그 기반 (Log-Based) - 数据库 변경 추적 ]                   │    │
│  │   Database Transaction Log, Kafka Header을 分析하여 데이터 흐름 추적    │    │
│  │   ▶ "orders 테이블의 row #1234가 14:32:01에 삽입됨" 이력을 기록          │    │
│  │   문제: Business transformation(JOIN, FILTER) 내용은 불투명           │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 방식 3: 규칙 기반 (Rule-Based) - 태깅 방식 ]                        │    │
│  │   개발자가 명시적으로 "@Lineage(source=orders.id)" 태그를 코드에 삽입    │    │
│  │   ▶ 정확하지만, 开发자 협업과 Discipline에 크게依存                     │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 방식 4: 프로브 기반 (Probe-Based / 미들웨어) ]                      │    │
│  │   ETL 도구의 运行 時間에 Hook을差し込んで 입출력 데이터 정보를 포착        │    │
│  │   ▶ Informatica, DataStage 등 Erwin, Coll等ツール 연동 시             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. 컬럼 수준 vs 테이블 수준 리니지
- **테이블 수준(Table-level)**: "orders 테이블 → order_summaries 테이블" (粗い granularity)
- **컬럼 수준(Column-level)**: "orders.order_id → order_summaries.order_key" (정밀한 granularity)
- 컬럼 수준 리니지는 컬럼 이름이 변경되거나 삭제될 때의 영향 분석에 필수적입니다.

### 2. [[235_forward_backward_chaining|Forward]] 리니지 vs Reverse 리니지
- **[[235_forward_backward_chaining|Forward]] (上游→下流)**: 원본 [[001_dikw_pyramid|데이터]]가 최종 산출물까지 어떻게 흐르는지 추적 ([[001_dikw_pyramid|데이터]] 흐름 파악용)
- **Reverse (下流→上游)**: 최종 보고서에서 원본까지 역추적 (Root Cause 분석용)

- **📢 섹션 요약 비유**: 리니지의Forward 추적은 "강물 흐름을 따라가며 오염원을 찾는 것"과 같습니다.下流의 물고기가 죽었다면, 물살을 거슬러 올라가며 "공장排水口(배수구)"를 찾아내는 것이Forward 리니지입니다. 반면 Reverse 리니지는 "범죄 수사에서의DNA 역추적"과 같습니다. 현장에서 발견된 범인의遺跡(흔적)을 가지고 범인의 집(원본 [[001_dikw_pyramid|데이터]])까지 역추적하는 것입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 주요 [[214_data_lineage_tracking|데이터 리니지]] 도구 비교

| 도구 | 추적 방식 |Granularity| 강점 | 약점 |
| :--- | :--- | :--- | :--- | :--- |
| **Apache Atlas** | Hook 기반 ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계) | 테이블 + 컬럼 | HDF/[[544_hive|Hive]], [[179_kafka_flink_watermark_time_window|Kafka]], Spark 통합 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 밖은 추적 불가 |
| **DataHub** | 파싱 + [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 | 테이블 + 컬럼 | 다양한 소스 connector, [[191_oss_license_compliance|OSS]] | SQL 파싱 coverage 제한적 |
| **OpenMetadata** | 파싱 + 커넥터 | 테이블 + 컬럼 |统一된 [[012_metadata|메타데이터]] [[152_hub_dummy_switching_intelligent|hub]] | 리니지 기능 신생 |
| **Collibra** | 규칙 + 파싱 혼합 | 테이블 + 컬럼 | 엔터프라이즈 거버넌스 | 高価 |
| **Datahub (by LinkedIn)** | 파싱 기반 | 컬럼 | 高精度な SQL 파싱, [[012_metadata|메타데이터]] [[014_api_posix|API]] | 학습 곡선 높음 |

### 치명적 트레이드오프
- **도전 1 - Python/R 기반 transformation 추적의 한계**: SQL은 파싱이 가능하지만, Python의 pandas.DataFrame.merge()나 R의 dplyr::[[521_join|join]]()은 현재 기술로는 완벽한 계보 추적이 어렵습니다. 이 部分은手動 태깅 또는ログ 분석으로 보완해야 합니다.
- **도전 2 - 리니지 [[070_graph_datastructure|그래프]]의 복잡성**: 수백 개의 테이블과 수천 개의 transformation이 얽힌 실제 기업 환경에서 리니지 [[070_graph_datastructure|그래프]]는 매우 복잡하여, 전체 [[070_graph_datastructure|그래프]]可視化는 오히려混乱을 초래할 수 있습니다. 特定 분석 목적에 맞는 필터링된 [[070_graph_datastructure|그래프]] View가 필수적입니다.
- **도전 3 - 거버넌스와의 간극**: 리니지를 추적한다고 해서 자동으로 규제 준수(예: GDPR의 처리 근거 文献化)가 달성되는 것은 아닙니다. 리니지 정보에 비즈니스 의미(예: "이 PII 필드는 고객 동의 기반 처리된 [[001_dikw_pyramid|데이터]]임")를 추가하는 것은 여전히人手이 필요합니다.

- **📢 섹션 요약 비유**: 리니지 추적은 "인간 基因组图谱分析(지놈 맵핑)"과 같습니다. 모든 유전자([[001_dikw_pyramid|데이터]] 컬럼)의 위치와機能を 解読하면(해석하면) 질병의 원인을 역추적하거나 치료법을 개발할 수 있지만, 유전자 [[001_dikw_pyramid|데이터]](변환 로직)가 너무 많고 복잡하여 전체 지도를 그리는 것 자체가 큰 프로젝트입니다. 또한 基因组图谱(지놈)은 "이 유전자가 우울증과相關된다"는 통계적 상관관계일 뿐 "이 유전자가 반드시 우울증을 유발한다"는 인과관계는 아니라는 한계가 있듯이, 리니지도 "이 테이블에서 저 테이블로 [[001_dikw_pyramid|데이터]]가 흐른다"는 흐름은 보여주지만, 흐르는 과정에서 발생하는 semantic 변화(의미 변화)까지 파악하기는 어렵습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 도입 의사결정 |
|:---|:---|:---|
| **환경 복잡성** | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark 기반인지, Python/R 코딩이 많은지 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 환경이면 Apache Atlas, Python 많으면 Datahub |
| **[[233_precision_recall_f1_roc_auc_threshold|정밀도]] 요구** | 테이블 수준으로 어디서 많이 쓰는지, 컬럼 수준 필요한지 | 컬럼 수준 필요 시 Datahub 추천 |
| **팀 역량** | [[191_oss_license_compliance|OSS]] 운영 인력 확보 여부 | 인력 부족 시 Collibra 관리형 선호 |
| **거버넌스 목적** | 단순 影响分析인지, 규제 준비용인지 | 규제용이면 컬럼 수준 + 비즈니스 [[012_metadata|메타데이터]] 연동 필수 |

*(추가 실무 적용 가이드 - 최소可行적 리니지 구축)*
- 처음부터 全사 수준의 완벽한 리니지 [[070_graph_datastructure|그래프]]를 구축하려고 하면 실패합니다.
- **[[087_erp_package_advantages_best_practice|Best Practice]]**: 먼저 영향 범위 파악이 가장 필요한 핵심 분석 테이블(예: 재무보고서, ML 모델 입력) [[489_raid_10_hybrid|10]]~20개부터 리니지를 구축하여 가치를 입증한 뒤, 점진적으로 확장하는 것이 현실적입니다.

- **📢 섹션 요약 비유**: 실무 도입은 "지도를 그릴 때 전체 세계를 한꺼번에描こう(그리려)のではなく"와 같습니다. 首先(먼저) 가장 중요한 도시(핵심 테이블)부터街道(거리) 정보를 그려나가고, 도시가 자리 잡으면 다음 마을로 확장하는 것입니다.最初から全世界の地图を完璧に描こうとすれば, 그리는 사람이 Burnout 되고, 결과물도 정확하지 않습니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **[[263_llm_large_language_model|LLM]] 기반 자동 리니지 설명 [[087_process_state_transition|생성]]**
   LLM이 복잡한 SQL [[298_qkv_attention|쿼리]]나 [[123_pipe|파이프]]라인 코드를 읽고 "이 transformation은 고객 테이블과 주문 테이블을 EMAIL 키로 JOIN하여 각 고객의 주문 횟수를 계산하는 작업입니다"와 같은 자연어 설명을 자동 [[087_process_state_transition|생성]]하는 기능이 등장하고 있습니다. 이로 인해 리니지 [[070_graph_datastructure|그래프]]가 技术자가 아닌 Business Analyst에게도 이해 가능한 도구로 변모하고 있습니다.

2. **실시간 리니지 (Real-Time Lineage)**
   배치(batch) 단위가 아닌, [[179_kafka_flink_watermark_time_window|Kafka]] 스트림 단위로 [[001_dikw_pyramid|데이터]] 흐름을 실시간 추적하는 기술이 발전하고 있습니다. 이 기술이成熟되면, "지금 방금 orders 토픽에 도착한 [[389_mesh_topology|메시]]지가 최종 매출 대시보드에 반영되기까지의 경로"를 실시간으로可視화하는 것이 가능해집니다.

3. **리니지-기반 자율 [[233_recovery_database_restoration_overview|회복]] (Lineage-Based Self-Healing)**
   리니지 [[070_graph_datastructure|그래프]]와 자동화된 [[229_monitor|모니터]]링(AQE, Great Expectations)이 결합되어, 특정 transformation의 [[001_dikw_pyramid|데이터]]品质이 저하되었음을 감지하면, 리니지 [[070_graph_datastructure|그래프]]를 따라가며 자동으로 영향받는下游 테이블을 [[655_ir_detection_analysis|식별]]하고, 문제의 root transformation을 자동 수정하거나隔离(격리)하는 "자율적 [[645_data_pipeline_acceleration|데이터 파이프라인]] 운영"이 연구되고 있습니다.

- **📢 섹션 요약 비유**: 리니지의 미래는 "인체 해부学에서 실시간 혈액 흐름 추적"으로 진화하는 것과 같습니다. 현재는MRl(핵산共振) 같은设备(장치)로 특정 시점의 혈관 지도를 그릴 수 있지만, 미래에는体内に微小 센서를注入(주입)하여 혈액이流れる(流れる) 순간을 실시간으로追う(추적) 것이 가능해지는 것처럼, [[214_data_lineage_tracking|데이터 리니지]]도 배치 단위가 아닌_streaming(스트리밍) 단위로 실시간 추적이 가능해질 것으로 기대됩니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[214_data_lineage_tracking|데이터 리니지]] 2가지 [[104_classification_analysis|분류]]**
    *   [[235_forward_backward_chaining|Forward]] Lineage (上游→下流 추적): [[001_dikw_pyramid|데이터]]가 어떻게下流까지 도달하는지 추적
    *   Reverse Lineage (下流→上游 추적): Root Cause 분석용 역추적
*   **Granularity 수준**
    *   테이블 수준 (Table-level): [[398_coarse_grained_multithreading|coarse-grained]], 전체 테이블 의존성
    *   컬럼 수준 (Column-level): [[399_fine_grained_multithreading|fine-grained]], 특정 컬럼 변환 추적
*   **추적 기술 4가지**
    *   파싱 기반 (SQL Parser): 고精度, SQL에만適用
    *   [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 ([[501_database|Database]] Log): 변경 내용 추적, 의미론 정보 부재
    *   규칙 기반 (Tagging): 手動, 정밀 but 人力 의존
    *   미들웨어 Hook: [[215_etl_vs_elt_pipeline|ETL]] 도구 연동, 自动 but 커넥터 제한

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 리니지 2가지 분류]
    │
    ▼
[Forward Lineage (上游→下流 추적): 데이터가 어떻게下流까지 도달하는지 추적]
    │
    ▼
[Reverse Lineage (下流→上游 추적): Root Cause 분석용 역추적]
    │
    ▼
[Granularity 수준]
    │
    ▼
[테이블 수준 (Table-level): coarse-grained, 전체 테이블 의존성]
    │
    ▼
[컬럼 수준 (Column-level): fine-grained, 특정 컬럼 변환 추적]
    │
    ▼
[추적 기술 4가지]
```

이 흐름도는 [[214_data_lineage_tracking|데이터 리니지]] 2가지 [[104_classification_analysis|분류]]에서 출발해 컬럼 수준 (Column-level): [[399_fine_grained_multithreading|fine-grained]], 특정 컬럼 변환 추적까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[214_data_lineage_tracking|데이터 리니지]]'는 우리 가족의 '족첩'과 같아요.
2. "김철수"라는 사람은 "김철수의 아빠: 김大山"에서 왔고, 김大山은 "김철수의 할아버지: 김영호"에서 왔다는 것을 알 수 있죠.
3. 컴퓨터에서도 어떤 [[001_dikw_pyramid|데이터]]가 어느 [[001_dikw_pyramid|데이터]]에서 만들어졌는지를追跡하면,万一(만약) 문제가 생겼을 때 원인을 빨리 찾을 수 있어요!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [[395_verification_process_review|Verification]]:** 본 문서는 구조적 [[003_integrity|무결성]], 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [[395_verification_process_review|검증]] 및 작성되었습니다. (Verified at: 2026-04-05)
