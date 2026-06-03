---
title: Cloudera CDP (Cloudera Data Platform)
date: '2026-03-04'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. **[[193_crl_distribution_point_cdp|CDP]]**는 클라우드와 [[061_on_premise_legacy_infrastructure|온프레미스]] 환경을 통합 관리하는 클라우데라의 차세대 하이브리드 [[001_dikw_pyramid|데이터]] 플랫폼이다.
2. SDX(Shared [[001_dikw_pyramid|Data]] Experience)를 통해 이기종 인프라 상에서도 일관된 보안, 거버넌스 및 [[203_metadata_management|메타데이터 관리]]를 보장한다.
3. [[001_dikw_pyramid|데이터]] 수집(Streaming)부터 분석([[209_data_warehouse_schema_on_write|DW]]), 기계학습(ML)까지 [[001_dikw_pyramid|데이터]] 생명주기 전체를 지원하는 기업용 통합 솔루션이다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **배경**: Hortonworks(HDP)와 Cloudera(CDH)의 합병 이후, 두 플랫폼의 장점을 결합하고 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에 최적화된 새로운 플랫폼이 필요해졌다.
- **필요성**: 기업들은 [[007_public_cloud|퍼블릭 클라우드]](AWS, GCP, Azure)와 자체 [[001_dikw_pyramid|데이터]] 센터를 혼용하는 하이브리드 [[268_strategy_pattern|전략]]을 채택하고 있으며, 이를 통합 제어할 단일 플랫폼이 필수적이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 아키텍처**:
  - **[[193_crl_distribution_point_cdp|CDP]] [[008_private_cloud|Private Cloud]]**: [[061_on_premise_legacy_infrastructure|온프레미스]] 환경에서 하드웨어 효율을 극대화하기 위해 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 기반으로 동작한다.
  - **[[193_crl_distribution_point_cdp|CDP]] [[007_public_cloud|Public Cloud]]**: 클라우드 상에서 [[090_service_kubernetes_network_load_balancing|서비스]]형([[309_saas|SaaS]]) 분석 환경을 제공한다.
  - **SDX (Shared [[001_dikw_pyramid|Data]] Experience)**: [[007_security_policy|보안 정책]](Ranger), [[012_metadata|메타데이터]](Atlas), [[606_auditing_linux_auditd|감사]]([[606_auditing_linux_auditd|Auditing]])를 통합 관리한다.

```text
[Cloudera Data Platform (CDP) Architecture]

+-------------------------------------------------------------+
|               Experience Apps (ML, DW, Data Flow)           |
+-------------------------------------------------------------+
                                ||
                                \/
+-------------------------------------------------------------+
|       SDX (Shared Data Experience) - Governance & Security  |
|     (Ranger: Policy / Atlas: Catalog / Encryption / Auth)   |
+-------------------------------------------------------------+
                                ||
                                \/
+------------------------------+------------------------------+
|      CDP Public Cloud        |      CDP Private Cloud       |
|  (AWS / Azure / Google)      |     (On-Premise / K8s)       |
+------------------------------+------------------------------+
| S3 / ADLS / GCS Storage      | HDFS / Ozone / Local Storage |
+------------------------------+------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 기존 CDH / HDP | 차세대 [[193_crl_distribution_point_cdp|CDP]] (Hybrid) |
| :--- | :--- | :--- |
| **인프라** | 서버 하드웨어 종속적 (Bare-metal) | [[561_container_based_deployment|컨테이너]] 및 [[206_serverless_cold_start|서버리스]] [[015_virtualization|가상화]] 지원 |
| **보안 관리** | 클러스터별 개별 [[009_config|설정]] | SDX를 통한 전사 통합 [[164_policy|정책]] 적용 |
| **운영 모델** | 정적인 리소스 할당 | 동적인 오토스케일링 및 공유 리소스 풀 |
| **[[603_component_independent_deployment_unit|컴포넌트]]** | [[191_oss_license_compliance|오픈소스]] [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 패키징 | 최신 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]](Iceberg 등) 기본 내장 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **실무 적용**: 금융권에서 [[001_dikw_pyramid|데이터]] 보안과 규제를 준수하기 위해 민감 [[001_dikw_pyramid|데이터]]는 Private Cloud에, 비민감 대규모 분석은 Public Cloud로 [[344_bus|버스]]팅(Bursting)하는 하이브리드 아키텍처 구현에 최적이다.
- **기술사적 판단**: CDP는 '[[010_data_democratization|데이터 민주화]]'를 실현하는 플랫폼이다. 특히 `Cloudera SDX`는 [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]를 방지하고, 전사적인 [[052_data_governance_framework|데이터 거버넌스]]를 코드 하나로 제어할 수 있게 함으로써 기업의 컴플라이언스 대응 능력을 강화한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 멀티클라우드 벤더 락인 방지, 운영 생산성 향상, 엔터프라이즈급 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확보.
- **결론**: [[001_dikw_pyramid|데이터]]의 위치에 상관없이 동일한 경험을 제공하는 CDP는 현대 기업의 [[055_digital_transformation|디지털 전환]]([[726_platform_engineering_idp_dx|DX]])을 위한 핵심 인프라로 자리매김하고 있으며, 향후 [[190_ai_llm_requirements_specification|AI]] 특화 기능이 더욱 강화될 것으로 보인다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
1. **SDX (Shared [[001_dikw_pyramid|Data]] Experience)**: 일관된 거버넌스 제공 핵심 엔진
2. **Apache Ozone**: [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 HDFS를 대체하는 차세대 [[494_object_storage|오브젝트 스토리지]]
3. **Control Plane**: 멀티 클러스터를 중앙에서 관리하는 제어판

### 📈 관련 키워드 및 발전 흐름도

```text
[Cloudera CDH / Hortonworks HDP — 온프레미스 하둡 배포판 시대]
    │
    ▼
[Cloudera + Hortonworks 합병 — 단일 엔터프라이즈 데이터 플랫폼 통합]
    │
    ▼
[CDP (Cloudera Data Platform) — 하이브리드/멀티클라우드 데이터 플랫폼]
    │
    ▼
[SDX (Shared Data Experience) — 거버넌스·보안·메타데이터 일관성 엔진]
    │
    ▼
[Apache Ozone — HDFS 대체 오브젝트 스토리지, 페타바이트급 확장]
```
[[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 배포판(CDH/HDP)을 CDP로 통합하고, SDX로 거버넌스를 [[194_consistency_database_integrity|일관성]] 있게 제공하며 Apache Ozone으로 스토리지 확장성을 확보했다.

### 👶 어린이를 위한 3줄 비유 설명
1. **Cloudera [[193_crl_distribution_point_cdp|CDP]]**: 흩어져 있는 장난감 상자([[001_dikw_pyramid|데이터]])들을 한꺼번에 관리하는 '커다란 로봇 장난감 정리함'이에요.
2. **이유**: 예전에는 내 방, 거실에 따로 정리해야 했지만, 이제는 이 로봇 상자 하나만 있으면 어디서든 똑같은 장난감을 꺼내 놀 수 있어요.
3. **결론**: 아주 크고 똑똑해서 장난감이 섞이거나 잃어버리지 않게 지켜주는 든든한 대장 상자예요.
