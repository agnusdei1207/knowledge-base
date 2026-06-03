+++
title = "28. Hadoop 보안 — Kerberos, Ranger, Atlas"
date = 2026-04-29

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안은 3개 레이어로 구성된다. [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) — 누구인가?), Apache Ranger(권한 부여 — 무엇을 할 수 있는가?), Apache Atlas([데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) — 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)인가·어떻게 이동하는가?)가 완전한 엔터프라이즈 보안 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 형성한다.
> 2. **가치**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) Hadoop은 보안이 없는 "Simple [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Mode"만 지원했다. [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) 통합으로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), Ranger로 세밀한 컬럼·행 레벨 접근 제어, Atlas로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보(Lineage) 추적이 가능해지면서 금융·의료 규제 환경에서도 사용 가능한 플랫폼으로 발전했다.
> 3. **판단 포인트**: 현대 클라우드 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 환경에서는 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) 대신 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/)(Cloud Identity), Ranger 대신 [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)·LakeFormation이 대안이 된다. [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 유지 조직에서는 [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)+Ranger+Atlas [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 여전히 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│           Hadoop 보안 3개 레이어                          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  레이어 1: 인증 (Authentication)                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Kerberos KDC (Key Distribution Center)          │   │
│  │  → TGT 티켓 발급 → 서비스 티켓으로 HDFS/YARN 접근│   │
│  └──────────────────────────────────────────────────┘   │
│                    ↓                                      │
│  레이어 2: 권한 부여 (Authorization)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Ranger — 정책 기반 세밀한 접근 제어       │   │
│  │  (DB·테이블·컬럼·행 레벨 정책)                   │   │
│  └──────────────────────────────────────────────────┘   │
│                    ↓                                      │
│  레이어 3: 데이터 거버넌스 (Governance)                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Atlas — 메타데이터·계보·분류·태그         │   │
│  │  (개인정보 컬럼 자동 태그, 데이터 흐름 추적)      │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안은 회사 출입 관리 시스템이다. 출입 카드([Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) — 신원 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)), 층별 권한(Ranger — 접근 가능 구역), 방문 기록부(Atlas — 어디서 어디로 이동했는지 추적) 3단계로 구성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 흐름

```text
사용자     KDC(AS)           KDC(TGS)        서비스
  │         │                  │               │
  │ kinit   │                  │               │
  │────────→│ TGT 발급         │               │
  │←────────│                  │               │
  │         │ TGT + 서비스 요청 │               │
  │────────────────────────────→ 서비스 티켓 발급│
  │←──────────────────────────────────────────│
  │                                서비스 티켓으로 HDFS 접근│
  │──────────────────────────────────────────→│
```

### Apache Ranger 세밀한 접근 제어

```text
정책 예시 (Hive 테이블):
  - 데이터 분석팀: sales_db.orders 테이블 SELECT
  - 개인정보팀: customer_db.users.phone 컬럼 마스킹 처리
  - 감사팀: 모든 쿼리 감사 로그 활성화
  - DBA: DDL 권한

행 레벨 필터:
  - 지역 관리자: WHERE region = '${user.region}' 자동 적용
```

- **📢 섹션 요약 비유**: Apache Ranger는 스마트 사무실 열쇠 시스템이다. 마케팅 팀은 마케팅 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 읽기 가능, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)가 있는 컬럼은 자동으로 별표(**)로 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)팀은 모든 접근 기록을 볼 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) | 클라우드 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
|:---|:---|:---|
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) | [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) (AWS/Azure/GCP) |
| 권한 부여 | Ranger | LakeFormation / [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) |
| 거버넌스 | Atlas | AWS Glue [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) / Purview |

- **📢 섹션 요약 비유**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안 vs 클라우드 보안은 사내 보안 시스템 vs 클라우드 보안 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다. 클라우드는 CSP가 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·권한·거버넌스를 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 제공해서 운영 부담이 줄어든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Apache Atlas [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 ([Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))

```text
데이터 소스 → ETL 변환 → DW 테이블 → 분석 보고서

Atlas 자동 추적:
  orders.csv → (Spark ETL) → sales_fact → (HiveQL) → monthly_report

규제 준수 활용:
  "이 개인정보 컬럼이 어느 다운스트림 테이블에 흘렀는가?"
  → GDPR 데이터 파악, 개인정보 삭제 영향 범위 분석
```

### 실무 배포 구성
```text
HDP (Hortonworks Data Platform) / CDP (Cloudera Data Platform):
  Kerberos + Ranger + Atlas + Knox(게이트웨이) 번들 제공

Knox Gateway:
  → 외부에서 Hadoop 클러스터 접근 시 단일 진입점 (API Gateway)
  → TLS 종단, SSO 통합
```

- **📢 섹션 요약 비유**: Apache Atlas [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보는 식품 이력 추적 시스템이다. 원재료(원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에서 완제품(분석 보고서)까지 모든 가공 단계를 추적해서 "이 숫자가 어떤 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 왔나?" 역추적이 가능하다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **규제 준수** | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/)·금융 규제 충족 |
| **세밀한 접근 제어** | 컬럼·행 레벨 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 최소 권한 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | 계보 추적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·영향 파악 |

현대 [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)에서 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) Kerberos는 클라우드 IAM으로, Ranger는 [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)/LakeFormation으로, Atlas는 Microsoft Purview/OpenMetadata로 대체되는 추세다. [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 유지 조직에서는 [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)+Ranger+Atlas [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 여전히 표준 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/)다.

- **📢 섹션 요약 비유**: [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 진화는 자동차 안전 기술 발전과 같다. 구형 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)(안전벨트만 있는 차)에서 [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)+Ranger+Atlas(에어백·ABS·차선 유지 시스템 장착 차)로 발전했고, 클라우드 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 완전 자율주행 안전 시스템으로 업그레이드된 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/">Kerberos</a></strong> | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 네트워크 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| **Apache Ranger** | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 세밀한 접근 제어 |
| **Apache Atlas** | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·계보·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·태그 |
| **Knox Gateway** | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 단일 진입점 |
| <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a></strong> | 클라우드 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 통합 거버넌스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Simple Security Mode — 인증 없는 초기 Hadoop]
    │
    ▼
[Kerberos 통합 — 네트워크 신원 인증]
    │
    ▼
[Apache Ranger — 정책 기반 세밀한 접근 제어]
    │
    ▼
[Apache Atlas — 데이터 거버넌스·계보 추적]
    │
    ▼
[Unity Catalog/LakeFormation — 클라우드 통합 거버넌스]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안은 출입 카드([Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)), 층별 권한(Ranger), 방문 기록부(Atlas) 3단계 시스템이에요!
2. Ranger는 "마케팅팀은 마케팅 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 자동으로 숨김"처럼 스마트하게 접근을 제어해요!
3. Atlas는 "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디서 왔고 어디로 갔나" 식품 이력 추적처럼 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 기록해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 50 / 262

← **이전**: [27. 데이터 직렬화: Avro / Protobuf / Thrift](/knowledge-base/studynote/16_bigdata/02_hadoop/049_data_serialization_avro_protobuf_thrift/)
**다음**: [29. Apache Oozie — Hadoop 워크플로 스케줄러](/knowledge-base/studynote/16_bigdata/02_hadoop/051_apache_oozie/) →

---
