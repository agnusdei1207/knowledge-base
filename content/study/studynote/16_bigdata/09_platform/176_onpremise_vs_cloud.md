---
title: 176. 온프레미스 Hadoop vs 클라우드 빅데이터 비교
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[061_on_premise_legacy_infrastructure|온프레미스]](On-Premises) Hadoop은 저장소와 계산을 같은 클러스터에 묶어 [[019_data_locality|데이터 지역성]]([[019_data_locality|Data Locality]])과 강한 통제권을 얻고, 클라우드 빅데이터는 객체 스토리지와 탄력적 계산 자원을 분리해 유연성과 확장성을 얻는다.
> 2. **가치**: 어느 쪽이 더 낫다는 단순 비교보다, 비용 구조·규제 요구·조직 운영 모델이 플랫폼 아키텍처에 어떻게 반영되는지가 더 중요하다.
> 3. **판단 포인트**: 고정적이고 규제가 강한 대용량 워크로드는 [[061_on_premise_legacy_infrastructure|온프레미스]]나 하이브리드가 유리하고, 변동성이 크고 실험 주기가 빠른 분석 환경은 [[531_cloud_native_architecture|클라우드 네이티브]] 재설계가 장기 효율이 높다.

---

## Ⅰ. 개요 및 필요성

[[061_on_premise_legacy_infrastructure|온프레미스]] Hadoop과 클라우드 빅데이터 비교는 단순한 배치 위치 선택이 아니라, 조직이 [[001_dikw_pyramid|데이터]]를 어떤 방식으로 저장·처리·운영할 것인가를 결정하는 플랫폼 [[268_strategy_pattern|전략]] 문제다. 전통적인 Hadoop은 범용 서버 여러 대를 묶어 대규모 저장과 [[136_variance|분산]] 처리를 가능하게 했고, 이후 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]]는 같은 목적을 더 유연한 방식으로 제공하면서 선택지가 크게 넓어졌다.

[[061_on_premise_legacy_infrastructure|온프레미스]] 모델은 하드웨어를 직접 보유하고 네트워크, 보안, 저장 [[164_policy|정책]]을 세밀하게 통제할 수 있다는 장점이 있다. 반면 [[459_quic_fec_forward_error_correction|초기]] 구축비가 크고, 수요 예측을 잘못하면 과잉 투자나 용량 부족이 동시에 발생한다. 클라우드는 [[459_quic_fec_forward_error_correction|초기]] 진입장벽이 낮고 수분 단위 확장이 가능하지만, 장기적 비용 최적화와 [[189_egress|데이터 이동 비용]], [[051_vendor_lock_in_cloud_computing|벤더 종속]]성 문제를 함께 고민해야 한다.

즉 이 비교의 핵심 질문은 "어디가 더 현대적인가"가 아니다. 오히려 **우리 [[001_dikw_pyramid|데이터]]는 얼마나 고정적인가, 얼마나 빨리 늘어나는가, 얼마나 강하게 통제해야 하는가**에 가깝다. 잘못 고르면 저장은 싸도 연산이 비싸지거나, 반대로 통제는 강하지만 민첩성이 급감하는 구조가 된다.

```text
┌──────────────────────────────────────────────────────────────┐
│      플랫폼 선택은 서버 위치보다 운영 방식의 선택에 가깝다     │
├──────────────────────────────────────────────────────────────┤
│ 온프레미스: 장비 구매 ─▶ 설치 ─▶ 수년 단위 운영 계획          │
│ 클라우드  : 서비스 선택 ─▶ 즉시 사용 ─▶ 사용량 기반 재조정     │
│                                                              │
│ 기술보다 비용 구조와 조직 속도가 함께 달라짐                  │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드의 차이는 단순히 창고를 어디 두느냐가 아니라, 창고를 직접 지어 운영할지 아니면 필요한 만큼 빌려 쓰는 물류 체계를 쓸지 결정하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[061_on_premise_legacy_infrastructure|온프레미스]] Hadoop의 핵심은 저장과 계산의 결합이다. [[013_hdfs|HDFS]] ([[203_hadoop_hdfs_block_replication_fault_tolerance|Hadoop Distributed File System]])가 [[001_dikw_pyramid|데이터]]를 여러 DataNode에 [[136_variance|분산]] 저장하고, [[020_yarn|YARN]] ([[020_yarn|Yet Another Resource Negotiator]])이 같은 클러스터의 계산 자원을 배분한다. 이 구조는 [[001_dikw_pyramid|데이터]]가 있는 노드 가까이에서 연산을 수행하는 [[019_data_locality|데이터 지역성]]에 강하며, 대규모 [[228_batch_processing_hadoop_spark|배치 처리]]에서 네트워크 이동을 줄이는 이점이 있다.

클라우드 빅데이터는 반대로 저장과 계산을 분리한다. Amazon Simple Storage [[090_service_kubernetes_network_load_balancing|Service]] (S3), Azure [[641_data_lake_storage|Data Lake Storage]] (ADLS), Google Cloud Storage (GCS) 같은 객체 스토리지가 장기 [[001_dikw_pyramid|데이터]]를 맡고, Spark·Presto·[[263_storage_compute_separation_bigquery|BigQuery]]·[[541_cassandra|Snowflake]] 같은 계산 엔진은 필요할 때만 확장된다. 이 구조는 유연하지만, 저장소와 계산 노드가 분리되어 있으므로 네트워크 입출력(Input/Output, I/O)과 [[012_metadata|메타데이터]] 최적화가 더 중요해진다.

```text
┌──────────────────────────────┐      ┌──────────────────────────────┐
│      온프레미스 Hadoop        │      │      클라우드 빅데이터        │
├──────────────────────────────┤      ├──────────────────────────────┤
│ Client / Analytics Tool      │      │ Client / Analytics Tool      │
│        │                     │      │        │                     │
│        ▼                     │      │        ▼                     │
│   YARN / Spark Cluster       │      │ Managed / Elastic Compute    │
│        │                     │      │        │                     │
│        ▼                     │      │        ▼                     │
│ DataNode + Compute           │      │ Object Storage               │
│ HDFS block + task locality   │      │ S3 / ADLS / GCS              │
│        │                     │      │        │                     │
│  저장과 계산이 같은 풀        │      │  저장과 계산이 분리된 풀      │
└──────────────────────────────┘      └──────────────────────────────┘
```

| 비교 축 | [[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] | 클라우드 빅데이터 |
| :--- | :--- | :--- |
| 자원 구조 | 저장·계산 결합 | 저장·계산 분리 |
| 확장 속도 | 장비 조달 주기 의존 | 자동화 호출 기반 즉시 확장 |
| 비용 성격 | Capital Expenditure (CapEx) 중심 | Operational Expenditure (OpEx) 중심 |
| [[001_dikw_pyramid|데이터]] 이동 | 노드 로컬 처리에 유리 | 네트워크·캐시 [[268_strategy_pattern|전략]] 중요 |
| 운영 책임 | 패치, 장애, 용량 계획 직접 수행 | 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] 활용 가능 |

핵심 원리는 결국 trade-off다. [[061_on_premise_legacy_infrastructure|온프레미스]]는 고정 자원을 깊게 최적화하고, 클라우드는 가변 자원을 빠르게 조합한다. 따라서 같은 Spark 작업이라도 어디서 더 유리한지는 작업 패턴과 [[001_dikw_pyramid|데이터]] 배치 방식에 따라 달라진다.

- **📢 섹션 요약 비유**: [[061_on_premise_legacy_infrastructure|온프레미스]]는 재료창고와 주방이 한 건물 안에 있는 식당이고, 클라우드는 외부 냉장창고에서 재료를 받아 즉석 주방을 여는 푸드트럭과 비슷하다. 전자는 안정적이고, 후자는 유연하다.

---

## Ⅲ. 비교 및 연결

실무에서는 보통 [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드만 비교하지 않고, `온프레미스 Hadoop → 관리형 Hadoop → 클라우드 네이티브 레이크하우스`까지 함께 본다. 이 흐름을 이해해야 단순 [[086_lift_association_rule_marketing|Lift]]-and-Shift가 왜 종종 실망스러운지 설명할 수 있다. 같은 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터를 클라우드 가상머신으로 옮겨도 저장·계산 결합 구조와 운영 습관을 그대로 가져오면, 클라우드의 장점을 절반밖에 못 [[289_cqrs_db|쓰기]] 때문이다.

| 모델 | 장점 | 한계 | 연결 개념 |
| :--- | :--- | :--- | :--- |
| [[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] | 통제력, [[019_data_locality|데이터 지역성]], 예측 가능한 [[282_performance_tactics|성능]] | 증설 리드타임, 고정 비용 | [[013_hdfs|HDFS]], [[020_yarn|YARN]], [[017_rack_awareness|Rack Awareness]] |
| 관리형 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] / Amazon EMR (Elastic [[018_mapreduce|MapReduce]]) | 운영 부담 감소, 빠른 확장 | 저장·계산 결합 사고방식 잔존 | Amazon EMR, Dataproc |
| [[531_cloud_native_architecture|클라우드 네이티브]] [[146_lakehouse|레이크하우스]] | 분리 확장, [[090_service_kubernetes_network_load_balancing|서비스]] 조합, 거버넌스 자동화 | [[189_egress|egress]], 벤더 의존, 네트워크 비용 | [[147_delta_lake|Delta Lake]], Iceberg, [[206_serverless_cold_start|Serverless]] Query |

이 비교에서 자주 등장하는 개념이 [[001_dikw_pyramid|데이터]] 중력([[001_dikw_pyramid|Data]] Gravity)이다. [[001_dikw_pyramid|데이터]]가 한 장소에 많이 쌓일수록 애플리케이션과 분석 도구가 그 주변으로 끌려오는 현상이다. 그래서 클라우드 이전은 계산 엔진 이전보다 [[001_dikw_pyramid|데이터]] 위치 [[268_strategy_pattern|전략]]과 [[012_metadata|메타데이터]] 체계가 더 중요하다.

또 다른 연결 축은 거버넌스다. [[061_on_premise_legacy_infrastructure|온프레미스]]는 세밀한 보안 통제를 직접 설계하는 대신 운영 부담을 진다. 클라우드는 기본 제공 보안 [[090_service_kubernetes_network_load_balancing|서비스]]와 [[606_auditing_linux_auditd|감사]] 기능을 활용하기 쉽지만, 계정·리전·[[090_service_kubernetes_network_load_balancing|서비스]] 경계가 복잡해지면 오히려 관리 규칙을 재설계해야 한다. 결국 비교의 핵심은 기술 [[057_stack|스택]]보다 **운영 모델의 재배치**다.

- **📢 섹션 요약 비유**: 단순 이전은 오래 살던 집의 가구를 새 집에 그대로 밀어 넣는 일이고, [[531_cloud_native_architecture|클라우드 네이티브]] 전환은 집 구조에 맞게 가구 배치와 생활 동선을 다시 설계하는 일에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 판단은 기능 비교보다 Total Cost of Ownership ([[016_tco|TCO]])과 운영 적합성을 같이 보는 쪽이 정확하다. 예를 들어 하루 종일 70% 이상 안정적으로 돌아가는 대규모 배치 클러스터는 [[061_on_premise_legacy_infrastructure|온프레미스]]가 유리할 수 있지만, 월말·분기말에만 10배 급증하는 분석 작업은 클라우드가 훨씬 경제적이다. 저장 용량보다 네트워크 [[189_egress|egress]] 비용이 더 큰 조직도 적지 않다.

| 의사결정 조건 | 상대적으로 유리한 선택 | 판단 이유 |
| :--- | :--- | :--- |
| 규제·[[809_data_sovereignty|데이터 주권]] 요구가 강함 | [[061_on_premise_legacy_infrastructure|온프레미스]] / 하이브리드 | 위치 통제와 [[606_auditing_linux_auditd|감사]] 체계 수립이 용이 |
| 실험성 워크로드, 사용량 변동 큼 | 클라우드 | 탄력 확장과 폐기 비용이 낮음 |
| 이미 대규모 장비 투자 완료 | [[061_on_premise_legacy_infrastructure|온프레미스]] | 감가상각 자산 활용 이점 |
| 글로벌 협업·다지역 분석 필요 | 클라우드 | 리전 확장과 [[090_service_kubernetes_network_load_balancing|서비스]] 연결이 빠름 |
| 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 운영 인력 풍부 | [[061_on_premise_legacy_infrastructure|온프레미스]] 또는 관리형 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] | 전환 마찰 비용이 낮음 |

### 현실적인 전환 패턴

1. **하이브리드 아카이브**: 자주 안 쓰는 [[676_cold_data_archiving|콜드 데이터]]만 클라우드 객체 스토리지로 이동
2. **신규 [[123_pipe|파이프]]라인 클라우드 우선**: 기존 배치는 유지하되, 새 분석 업무부터 클라우드에서 시작
3. **연합 질의([[195_federated_query_data_fabric_distributed_join|Federated Query]])**: Trino/Presto로 [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드를 동시에 질의
4. **재설계 전환**: 단순 [[013_hdfs|HDFS]] 마이그레이션이 아니라 [[146_lakehouse|레이크하우스]]·[[206_serverless_cold_start|서버리스]] 질의 엔진으로 운영모델 변경

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 장비 감가상각과 [[189_egress|egress]] 비용을 빼고 월 사용료만 비교하는 경우
- [[086_lift_association_rule_marketing|Lift]]-and-Shift 후에도 24시간 상시 클러스터를 켜 두는 경우
- [[012_metadata|메타데이터]], [[394_catalog_metadata|카탈로그]], 권한 모델을 이전 [[459_quic_fec_forward_error_correction|초기]]에 설계하지 않는 경우
- 클라우드 전환을 인프라 프로젝트로만 보고 운영조직 변화는 무시하는 경우

기술사 답안에서는 "클라우드가 최신이므로 우수"처럼 [[289_cqrs_db|쓰기]]보다, [[001_dikw_pyramid|데이터]] 크기·변동성·규제·인력 역량을 축으로 의사결정을 보여 주는 편이 좋다. 실제 플랫폼 선택은 기술 [[282_performance_tactics|성능]]보다도 비용 모델과 조직 운영 방식에 더 깊게 좌우되기 때문이다.

- **📢 섹션 요약 비유**: 플랫폼 선택은 자동차 [[282_performance_tactics|성능]]표만 보고 차를 고르는 일이 아니다. 출퇴근용인지, 화물운송용인지, 주차장과 정비소를 직접 가질 수 있는지까지 함께 봐야 맞는 차가 나온다.

---

## Ⅴ. 기대효과 및 결론

[[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드의 차이를 제대로 이해하면 플랫폼 논의가 "종교 전쟁"에서 "조건 기반 설계"로 바뀐다. [[061_on_premise_legacy_infrastructure|온프레미스]]는 [[019_data_locality|데이터 지역성]]과 강한 통제를 통해 안정성을 주고, 클라우드는 [[571_resiliency_fault_tolerance_patterns|탄력성]]과 [[090_service_kubernetes_network_load_balancing|서비스]] 조합 능력으로 실험 속도를 높여 준다. 어느 한쪽의 승리가 아니라, 조직 요구에 맞는 조합을 찾는 것이 핵심 효과다.

향후 방향은 완전한 이분법보다 하이브리드와 [[146_lakehouse|레이크하우스]] 중심으로 갈 가능성이 크다. 규제 [[001_dikw_pyramid|데이터]]는 현장이나 전용 리전에 두고, burst성 분석과 [[231_ai_turing_test|인공지능]] 학습은 클라우드로 넘기는 모델이 현실적이다. 동시에 [[342_metadata_catalog|메타데이터 카탈로그]]와 거버넌스를 통합해, 저장 위치가 달라도 하나의 [[001_dikw_pyramid|데이터]] 플랫폼처럼 보이게 만드는 설계가 중요해진다.

결론적으로 이 주제는 "[[843_hadoop_rack_awareness_data_replication_topology|하둡]]을 어디에 설치할까"가 아니라 **[[001_dikw_pyramid|데이터]]와 계산, 비용과 통제, 민첩성과 거버넌스를 어떻게 균형 잡을까**라는 질문으로 기억해야 한다. 그 균형점을 설명할 수 있어야 실무와 시험 모두에서 설득력이 생긴다.

- **📢 섹션 요약 비유**: [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드의 선택은 집을 살지 임대할지 고르는 일과 비슷하다. 오래 머물며 구조를 마음대로 바꾸고 싶으면 소유가 유리하고, 상황 변화에 빨리 대응해야 하면 유연한 임대가 유리하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[019_data_locality|Data Locality]] | [[001_dikw_pyramid|데이터]]가 있는 곳 가까이에서 계산해 네트워크 이동을 줄이는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 핵심 원리 |
| [[013_hdfs|HDFS]] ([[203_hadoop_hdfs_block_replication_fault_tolerance|Hadoop Distributed File System]]) | [[061_on_premise_legacy_infrastructure|온프레미스]] Hadoop의 저장 계층 |
| [[020_yarn|YARN]] ([[020_yarn|Yet Another Resource Negotiator]]) | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터의 자원 배분 계층 |
| [[494_object_storage|Object Storage]] | 클라우드에서 저장과 계산 분리를 가능하게 하는 기반 |
| [[001_dikw_pyramid|Data]] Gravity | [[001_dikw_pyramid|데이터]]가 모인 위치로 [[090_service_kubernetes_network_load_balancing|서비스]]와 도구가 끌리는 현상 |
| [[146_lakehouse|Lakehouse]] | 객체 스토리지 위에서 분석·거버넌스를 통합하려는 현대적 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
온프레미스 Hadoop
    │
    ▼
관리형 Hadoop 서비스
    │
    ▼
객체 스토리지 기반 저장·계산 분리
    │
    ▼
Lakehouse · Serverless Analytics
    │
    ▼
Hybrid Data Platform · Federated Governance
```

이 흐름은 클러스터 중심 사고에서 [[090_service_kubernetes_network_load_balancing|서비스]] 조합형 플랫폼과 하이브리드 거버넌스로 이동하는 발전 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[061_on_premise_legacy_infrastructure|온프레미스]]는 우리 집 창고에 장난감과 책상을 다 두고 노는 방법이라서, 마음대로 정리할 수 있어요.
2. 클라우드는 큰 장난감 창고를 빌려 쓰는 방법이라서, 필요할 때 많이 쓰고 끝나면 줄일 수 있어요.
3. 그래서 매일 많이 쓰면 우리 집 방식이 좋고, 가끔 크게 놀면 빌려 쓰는 방식이 더 편해요.
