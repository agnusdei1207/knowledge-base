---
title: "048. Hdfs Viewfs"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 48
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ViewFS ([View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System)는 [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 연합([Federation](/studynote/09_security/11_iam_access_control/543_federation/)) 환경에서 여러 독립 [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) 클러스터를 단일 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) `/user`, `/data`, `/tmp` 등으로 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)하여 통합 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 뷰를 제공하는 클라이언트 측 가상 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 레이어다.
> 2. **가치**: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) Federation은 단일 NameNode의 메모리 한계(수억 개 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) = ~GB 메모리)를 해결하기 위해 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)를 [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/)한다. ViewFS는 이 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)를 사용자·애플리케이션 입장에서 단일 경로처럼 접근 가능하게 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하여 기존 [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 코드 변경 없이 사용할 수 있다.
> 3. **판단 포인트**: ViewFS는 클라이언트 측 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)이므로 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 포인트 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 각 클라이언트에 일치해야 하고, 크로스 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 포인트 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이동(rename)이 불가능하다는 한계가 있다. 이 한계를 극복하기 위해 [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [Federation](/studynote/09_security/11_iam_access_control/543_federation/) + ViewFS + RBF(Router Based [Federation](/studynote/09_security/11_iam_access_control/543_federation/))로 발전했다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|           HDFS Federation + ViewFS 구조                |
+-------------------------------------------------------+
| 클라이언트 (ViewFS 설정 적용)                           |
|   /user  -> viewfs://cluster1/user                      |
|   /data  -> viewfs://cluster2/data                      |
|   /tmp   -> viewfs://cluster1/tmp                       |
|                v                                       |
|  NameNode-1 (cluster1): /user, /tmp 담당               |
|  NameNode-2 (cluster2): /data 담당                     |
|                v                                       |
|  DataNode 풀 (공유) — 실제 블록 저장                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: ViewFS는 여러 도서관([NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/))을 하나의 통합 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)로 보여주는 시스템이다. "컴퓨터 책은 A도서관, 역사 책은 B도서관"에 있지만, 독자는 하나의 검색창에서 모두 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ViewFS [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (core-site.xml)

```xml
<property>
  <name>fs.viewfs.mounttable.default.link./user</name>
  <value>hdfs://nn1/user</value>
</property>
<property>
  <name>fs.viewfs.mounttable.default.link./data</name>
  <value>hdfs://nn2/data</value>
</property>
<property>
  <name>fs.defaultFS</name>
  <value>viewfs://default</value>
</property>
```

### ViewFS vs. RBF (Router-Based [Federation](/studynote/09_security/11_iam_access_control/543_federation/))

| 비교 | ViewFS | RBF |
|:---|:---|:---|
| [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 위치 | 클라이언트 측 | 서버 측 (Router) |
| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 위치 | 각 클라이언트 | 중앙 Router 서버 |
| 크로스 경계 rename | 불가 | Router 지원 |
| 투명성 | 클라이언트 인식 필요 | 완전 투명 |

- **📢 섹션 요약 비유**: ViewFS는 각 직원 PC에 설치된 도서관 통합 검색 앱이다. RBF는 도서관 앞에 설치된 통합 안내데스크다. 데스크(RBF) 방식이 더 투명하고 중앙 관리가 쉽다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [Federation](/studynote/09_security/11_iam_access_control/543_federation/) | ViewFS |
|:---|:---|:---|:---|
| 확장성 | [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리 한계 | [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/) | 통합 뷰 제공 |
| [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) HA 필요 | 독립 NN per 풀 | 클라이언트 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |
| 관리 복잡도 | 낮음 | 높음 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 관리 |

- **📢 섹션 요약 비유**: 단일 NameNode는 시청의 민원실 한 곳이다. Federation은 구청마다 민원실이 있는 구조, ViewFS는 구청별 위치를 알아서 안내해주는 종합 안내앱이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대규모 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 설계
- [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수 > 1억 개: 단일 [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) JVM 힙 ~60GB 초과 -> [Federation](/studynote/09_security/11_iam_access_control/543_federation/) 분리 시점.
- 분리 기준: 팀별, 부서별, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성별(배치/실시간/아카이브) [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 분리.
- ViewFS로 기존 [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)/Spark 잡 경로 변경 없이 전환.

### Ozone (차세대 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 스토리지)
- [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 3.x: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ViewFS -> Apache Ozone으로 진화. Ozone은 객체 스토리지 기반으로 수십 억 개 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리 없이 처리한다.

- **📢 섹션 요약 비유**: Ozone은 HDFS의 한계를 넘는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 스토리지다. 기존 도서관 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 시스템이 수십억 권을 관리할 수 없을 때, 전자 클라우드 도서관으로 업그레이드하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **확장성** | 수십 억 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수용을 위한 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| **투명성** | 기존 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 잡 코드 변경 없이 [Federation](/studynote/09_security/11_iam_access_control/543_federation/) 적용 |
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong> | [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) 독립 운영으로 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 제거 |

[HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ViewFS는 RBF로 진화하고, 궁극적으로 Ozone의 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 객체 스토리지로 대체되는 방향으로 발전 중이다.

- **📢 섹션 요약 비유**: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 진화는 도서관의 발전이다. 수동 카드 목록(단일 [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/)) -> 구청별 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 목록([Federation](/studynote/09_security/11_iam_access_control/543_federation/)+ViewFS) -> 클라우드 전자도서관(Ozone)으로 진화한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/013_hdfs/">HDFS</a> <a href="/studynote/09_security/11_iam_access_control/543_federation/">Federation</a></strong> | ViewFS가 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 구조 |
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/014_namenode/">NameNode</a></strong> | [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) [메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/) 서버 |
| **RBF** | ViewFS의 서버 측 진화 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| **Apache Ozone** | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 한계 극복을 위한 차세대 스토리지 |
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/015_datanode/">DataNode</a></strong> | 실제 블록을 저장하는 공유 스토리지 노드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 NameNode HDFS — 수억 파일 한계]
    |
    v
[HDFS Federation — 네임스페이스 수평 분할]
    |
    v
[ViewFS — 클라이언트 측 통합 마운트 뷰]
    |
    v
[RBF (Router-Based Federation) — 서버 측 통합 라우팅]
    |
    v
[Apache Ozone — 객체 스토리지 기반 무제한 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. ViewFS는 여러 도서관을 하나의 검색창에서 찾을 수 있는 통합 앱이에요! 각 도서관([NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/))은 따로 있지만, 앱에서는 한 번에 검색할 수 있어요.
2. "컴퓨터 책은 A도서관, 역사 책은 B도서관"인데 앱에서는 모두 /computer, /history로 통일해서 보여줘요!
3. 요즘은 클라우드 전자도서관(Ozone)으로 업그레이드해서 수십 억 권도 거뜬히 관리할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 262

<- **이전**: [25. 처방 분석 (Prescriptive Analytics) — 최적 행동 처방](/studynote/16_bigdata/02_hadoop/047_prescriptive_analytics/)
**다음**: [27. 데이터 직렬화: Avro / Protobuf / Thrift](/studynote/16_bigdata/02_hadoop/049_data_serialization_avro_protobuf_thrift/) ->

---
