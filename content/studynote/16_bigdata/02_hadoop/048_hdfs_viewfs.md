---
title: 26. HDFS ViewFS — Hadoop 연합 네임스페이스 통합 뷰
date: '2026-04-29'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[013_hdfs|HDFS]] ViewFS ([[151_sql_view_virtual_table|View]] [[501_file_definition_logical_record|File]] System)는 [[013_hdfs|HDFS]] 연합([[543_federation|Federation]]) 환경에서 여러 독립 [[014_namenode|NameNode]] 클러스터를 단일 [[369_logic_bomb|논리]] [[061_namespace|네임스페이스]] `/user`, `/data`, `/tmp` 등으로 [[516_mount_mechanism|마운트]]하여 통합 [[501_file_definition_logical_record|파일]] 시스템 뷰를 제공하는 클라이언트 측 가상 [[516_mount_mechanism|마운트]] 레이어다.
> 2. **가치**: [[013_hdfs|HDFS]] Federation은 단일 NameNode의 메모리 한계(수억 개 [[501_file_definition_logical_record|파일]] = ~GB 메모리)를 해결하기 위해 [[061_namespace|네임스페이스]]를 [[268_horizontal_fragmentation|수평 분할]]한다. ViewFS는 이 [[136_variance|분산]]된 [[061_namespace|네임스페이스]]를 사용자·애플리케이션 입장에서 단일 경로처럼 접근 가능하게 [[198_abstraction_control_data_process|추상화]]하여 기존 [[013_hdfs|HDFS]] 코드 변경 없이 사용할 수 있다.
> 3. **판단 포인트**: ViewFS는 클라이언트 측 [[198_abstraction_control_data_process|추상화]]이므로 [[516_mount_mechanism|마운트]] 포인트 [[009_config|설정]]이 각 클라이언트에 일치해야 하고, 크로스 [[516_mount_mechanism|마운트]] 포인트 [[501_file_definition_logical_record|파일]] 이동(rename)이 불가능하다는 한계가 있다. 이 한계를 극복하기 위해 [[013_hdfs|HDFS]] [[543_federation|Federation]] + ViewFS + RBF(Router Based [[543_federation|Federation]])로 발전했다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│           HDFS Federation + ViewFS 구조                │
├───────────────────────────────────────────────────────┤
│ 클라이언트 (ViewFS 설정 적용)                           │
│   /user  → viewfs://cluster1/user                      │
│   /data  → viewfs://cluster2/data                      │
│   /tmp   → viewfs://cluster1/tmp                       │
│                ↓                                       │
│  NameNode-1 (cluster1): /user, /tmp 담당               │
│  NameNode-2 (cluster2): /data 담당                     │
│                ↓                                       │
│  DataNode 풀 (공유) — 실제 블록 저장                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ViewFS는 여러 도서관([[014_namenode|NameNode]])을 하나의 통합 [[394_catalog_metadata|카탈로그]]로 보여주는 시스템이다. "컴퓨터 책은 A도서관, 역사 책은 B도서관"에 있지만, 독자는 하나의 검색창에서 모두 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ViewFS [[009_config|설정]] (core-site.xml)

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

### ViewFS vs. RBF (Router-Based [[543_federation|Federation]])

| 비교 | ViewFS | RBF |
|:---|:---|:---|
| [[198_abstraction_control_data_process|추상화]] 위치 | 클라이언트 측 | 서버 측 (Router) |
| [[009_config|설정]] 위치 | 각 클라이언트 | 중앙 Router 서버 |
| 크로스 경계 rename | 불가 | Router 지원 |
| 투명성 | 클라이언트 인식 필요 | 완전 투명 |

- **📢 섹션 요약 비유**: ViewFS는 각 직원 PC에 설치된 도서관 통합 검색 앱이다. RBF는 도서관 앞에 설치된 통합 안내데스크다. 데스크(RBF) 방식이 더 투명하고 중앙 관리가 쉽다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 [[014_namenode|NameNode]] | [[013_hdfs|HDFS]] [[543_federation|Federation]] | ViewFS |
|:---|:---|:---|:---|
| 확장성 | [[014_namenode|NameNode]] 메모리 한계 | [[061_namespace|네임스페이스]] [[268_horizontal_fragmentation|수평 분할]] | 통합 뷰 제공 |
| [[454_spof|단일 장애점]] | [[014_namenode|NameNode]] HA 필요 | 독립 NN per 풀 | 클라이언트 [[198_abstraction_control_data_process|추상화]] |
| 관리 복잡도 | 낮음 | 높음 | [[009_config|설정]] [[501_file_definition_logical_record|파일]] 관리 |

- **📢 섹션 요약 비유**: 단일 NameNode는 시청의 민원실 한 곳이다. Federation은 구청마다 민원실이 있는 구조, ViewFS는 구청별 위치를 알아서 안내해주는 종합 안내앱이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대규모 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터 설계
- [[501_file_definition_logical_record|파일]] 수 > 1억 개: 단일 [[014_namenode|NameNode]] JVM 힙 ~60GB 초과 → [[543_federation|Federation]] 분리 시점.
- 분리 기준: 팀별, 부서별, [[001_dikw_pyramid|데이터]] 특성별(배치/실시간/아카이브) [[369_logic_bomb|논리]] 분리.
- ViewFS로 기존 [[018_mapreduce|MapReduce]]/Spark 잡 경로 변경 없이 전환.

### Ozone (차세대 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 스토리지)
- [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 3.x: [[013_hdfs|HDFS]] ViewFS → Apache Ozone으로 진화. Ozone은 객체 스토리지 기반으로 수십 억 개 [[501_file_definition_logical_record|파일]]을 [[014_namenode|NameNode]] 메모리 없이 처리한다.

- **📢 섹션 요약 비유**: Ozone은 HDFS의 한계를 넘는 [[531_cloud_native_architecture|클라우드 네이티브]] 스토리지다. 기존 도서관 [[394_catalog_metadata|카탈로그]] 시스템이 수십억 권을 관리할 수 없을 때, 전자 클라우드 도서관으로 업그레이드하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **확장성** | 수십 억 [[501_file_definition_logical_record|파일]] 수용을 위한 [[061_namespace|네임스페이스]] [[136_variance|분산]] |
| **투명성** | 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 잡 코드 변경 없이 [[543_federation|Federation]] 적용 |
| **[[452_availability|가용성]]** | [[014_namenode|NameNode]] 독립 운영으로 [[454_spof|단일 장애점]] 제거 |

[[013_hdfs|HDFS]] ViewFS는 RBF로 진화하고, 궁극적으로 Ozone의 [[531_cloud_native_architecture|클라우드 네이티브]] 객체 스토리지로 대체되는 방향으로 발전 중이다.

- **📢 섹션 요약 비유**: [[013_hdfs|HDFS]] 진화는 도서관의 발전이다. 수동 카드 목록(단일 [[014_namenode|NameNode]]) → 구청별 [[136_variance|분산]] 목록([[543_federation|Federation]]+ViewFS) → 클라우드 전자도서관(Ozone)으로 진화한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[013_hdfs|HDFS]] [[543_federation|Federation]]** | ViewFS가 [[198_abstraction_control_data_process|추상화]]하는 [[136_variance|분산]] [[061_namespace|네임스페이스]] 구조 |
| **[[014_namenode|NameNode]]** | [[061_namespace|네임스페이스]] [[203_metadata_management|메타데이터 관리]] 서버 |
| **RBF** | ViewFS의 서버 측 진화 [[288_version_ihl_tos_total_length|버전]] |
| **Apache Ozone** | [[013_hdfs|HDFS]] 한계 극복을 위한 차세대 스토리지 |
| **[[015_datanode|DataNode]]** | 실제 블록을 저장하는 공유 스토리지 노드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 NameNode HDFS — 수억 파일 한계]
    │
    ▼
[HDFS Federation — 네임스페이스 수평 분할]
    │
    ▼
[ViewFS — 클라이언트 측 통합 마운트 뷰]
    │
    ▼
[RBF (Router-Based Federation) — 서버 측 통합 라우팅]
    │
    ▼
[Apache Ozone — 객체 스토리지 기반 무제한 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. ViewFS는 여러 도서관을 하나의 검색창에서 찾을 수 있는 통합 앱이에요! 각 도서관([[014_namenode|NameNode]])은 따로 있지만, 앱에서는 한 번에 검색할 수 있어요.
2. "컴퓨터 책은 A도서관, 역사 책은 B도서관"인데 앱에서는 모두 /computer, /history로 통일해서 보여줘요!
3. 요즘은 클라우드 전자도서관(Ozone)으로 업그레이드해서 수십 억 권도 거뜬히 관리할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 262

← **이전**: [[047_prescriptive_analytics|25. 처방 분석 (Prescriptive Analytics) — 최적 행동 처방]]
**다음**: [[049_data_serialization_avro_protobuf_thrift|27. 데이터 직렬화: Avro / Protobuf / Thrift]] →

---
