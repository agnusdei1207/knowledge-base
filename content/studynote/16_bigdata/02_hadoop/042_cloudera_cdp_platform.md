+++
title = "Cloudera CDP (Cloudera Data Platform)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. **[CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)**는 클라우드와 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 환경을 통합 관리하는 클라우데라의 차세대 하이브리드 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼이다.
2. SDX(Shared [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Experience)를 통해 이기종 인프라 상에서도 일관된 보안, 거버넌스 및 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/)를 보장한다.
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집(Streaming)부터 분석([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)), 기계학습(ML)까지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생명주기 전체를 지원하는 기업용 통합 솔루션이다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **배경**: Hortonworks(HDP)와 Cloudera(CDH)의 합병 이후, 두 플랫폼의 장점을 결합하고 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에 최적화된 새로운 플랫폼이 필요해졌다.
- **필요성**: 기업들은 [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)(AWS, GCP, Azure)와 자체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터를 혼용하는 하이브리드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 채택하고 있으며, 이를 통합 제어할 단일 플랫폼이 필수적이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 아키텍처**:
  - **[CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) [Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 환경에서 하드웨어 효율을 극대화하기 위해 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반으로 동작한다.
  - **[CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) [Public Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)**: 클라우드 상에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)) 분석 환경을 제공한다.
  - **SDX (Shared [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Experience)**: [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/)(Ranger), [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(Atlas), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Auditing](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))를 통합 관리한다.

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

| 비교 항목 | 기존 CDH / HDP | 차세대 [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) (Hybrid) |
| :--- | :--- | :--- |
| **인프라** | 서버 하드웨어 종속적 (Bare-metal) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 및 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 지원 |
| **보안 관리** | 클러스터별 개별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | SDX를 통한 전사 통합 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 |
| **운영 모델** | 정적인 리소스 할당 | 동적인 오토스케일링 및 공유 리소스 풀 |
| **[컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 패키징 | 최신 [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)(Iceberg 등) 기본 내장 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **실무 적용**: 금융권에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안과 규제를 준수하기 위해 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 Private Cloud에, 비민감 대규모 분석은 Public Cloud로 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)팅(Bursting)하는 하이브리드 아키텍처 구현에 최적이다.
- **기술사적 판단**: CDP는 '[데이터 민주화](/knowledge-base/studynote/16_bigdata/01_intro/010_data_democratization/)'를 실현하는 플랫폼이다. 특히 `Cloudera SDX`는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)를 방지하고, 전사적인 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)를 코드 하나로 제어할 수 있게 함으로써 기업의 컴플라이언스 대응 능력을 강화한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 멀티클라우드 벤더 락인 방지, 운영 생산성 향상, 엔터프라이즈급 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 확보.
- **결론**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 위치에 상관없이 동일한 경험을 제공하는 CDP는 현대 기업의 [디지털 전환](/knowledge-base/studynote/12_it_management/01_governance_strategy/055_digital_transformation/)([DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/))을 위한 핵심 인프라로 자리매김하고 있으며, 향후 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 특화 기능이 더욱 강화될 것으로 보인다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
1. **SDX (Shared [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Experience)**: 일관된 거버넌스 제공 핵심 엔진
2. **Apache Ozone**: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 HDFS를 대체하는 차세대 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)
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
[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 배포판(CDH/HDP)을 CDP로 통합하고, SDX로 거버넌스를 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 있게 제공하며 Apache Ozone으로 스토리지 확장성을 확보했다.

### 👶 어린이를 위한 3줄 비유 설명
1. **Cloudera [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)**: 흩어져 있는 장난감 상자([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))들을 한꺼번에 관리하는 '커다란 로봇 장난감 정리함'이에요.
2. **이유**: 예전에는 내 방, 거실에 따로 정리해야 했지만, 이제는 이 로봇 상자 하나만 있으면 어디서든 똑같은 장난감을 꺼내 놀 수 있어요.
3. **결론**: 아주 크고 똑똑해서 장난감이 섞이거나 잃어버리지 않게 지켜주는 든든한 대장 상자예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 42 / 262

← **이전**: [아파치 암바리 (Apache Ambari)](/knowledge-base/studynote/16_bigdata/02_hadoop/041_apache_ambari_management/)
**다음**: [HDFS Small File Problem (HDFS 작은 파일 문제)](/knowledge-base/studynote/16_bigdata/02_hadoop/043_hdfs_small_file_problem/) →

---
