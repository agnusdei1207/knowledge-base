---
title: 스파크 배포 모드 (Spark Deployment Modes)
date: '2024-03-23'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- 스파크 배포 모드는 애플리케이션의 드라이버(Driver)와 실행기(Executor)가 물리적으로 어디에서 실행될지 결정하는 운영 [[268_strategy_pattern|전략]]이다.
- 클러스터 관리자([[020_yarn|YARN]], [[205_kubernetes_container_orchestration|Kubernetes]], Mesos 등)의 종류와 네트워크 위치에 따라 Local, [[003_audit_stakeholders|Client]], Cluster 모드로 구분된다.
- 각 모드는 보안, 네트워크 오버헤드, 대화형 분석 여부 등 실무 요구사항에 따라 선택하며, 리소스 격리와 안정성 차이를 가진다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
[[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]]는 [[136_variance|분산]] 환경에서 동작하므로, 작업을 지시하는 '두뇌(Driver)'와 실제 연산을 수행하는 '팔다리(Executor)'의 배치 [[268_strategy_pattern|전략]]이 중요하다. **배포 모드([[087_deployment_kubernetes_workload_rolling_update|Deployment]] Mode)**는 이 배치를 결정하며, 특히 클라우드 기반의 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 도입이 늘어나면서 단순 자원 관리를 넘어 인프라 아키텍처의 핵심 의사결정 요소가 되었다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
드라이버가 클라이언트([[003_audit_stakeholders|Client]]) 측에 있느냐, 아니면 클러스터(Cluster) 내부에 있느냐에 따라 아키텍처가 달라진다.

```text
[ Spark Deployment: Client Mode vs Cluster Mode ]
(스파크 배포: 클라이언트 모드 vs 클러스터 모드)

   < Client Mode >                  < Cluster Mode >
   (대화형 분석/디버깅 유리)           (프로덕션 배포/안정성 유리)
   
     Client Node                       Cluster Node (Master)
   +---------------+                 +--------------------+
   | [Driver]      |                 | Cluster Manager    |
   | (User Code)   | <---- Net ----> | (YARN, K8s, Mesos) |
   +---------------+                 +---------+----------+
          |                                    |
   +------v-------+                    +-------v--------+
   | Cluster Node |                    | Cluster Node   |
   | [Executor]   |                    | [Driver]       |
   +--------------+                    +-------+--------+
                                               |
                                       +-------v--------+
                                       | Cluster Node   |
                                       | [Executor]     |
                                       +----------------+
```

1. **Local Mode:** 단일 컴퓨터(JVM)에서 드라이버와 실행기가 모두 실행된다. (개발/테스트용)
2. **[[003_audit_stakeholders|Client]] Mode:** 드라이버가 클러스터 외부(사용자 로컬 장비)에서 실행된다. 즉시 결과 [[396_validation|확인]]이 필요한 REPL(쉘) 환경에 적합하다.
3. **Cluster Mode:** 드라이버가 클러스터 내부의 워커 노드 중 하나에서 실행된다. 드라이버가 종료되더라도 클러스터 내에서 관리되므로 장기 실행 작업(Production Batch)에 필수적이다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 항목 (Mode) | Local Mode | [[003_audit_stakeholders|Client]] Mode | Cluster Mode |
| :--- | :--- | :--- | :--- |
| **드라이버 위치** | 로컬 JVM 내부 | 사용자 실행 장비 (외부) | 클러스터 워커 노드 (내부) |
| **권장 용도** | [[397_unit_test|단위 테스트]], 코드 [[395_verification_process_review|검증]] | 대화형 [[298_qkv_attention|쿼리]] (Spark [[044_shell|Shell]]) | 프로덕션 배치 작업 |
| **네트워크 부하** | 없음 (로컬 I/O) | 외부-내부간 잦은 통신 발생 | 내부 노드간 고속 통신 |
| **리소스 관리자** | - | [[020_yarn|YARN]], K8s, [[150_5g_sa_standalone_architecture|Standalone]] | [[020_yarn|YARN]], K8s, [[150_5g_sa_standalone_architecture|Standalone]] |
| **장애 조치** | [[107_process_termination|프로세스 종료]] 시 끝 | 드라이버 [[454_spof|SPOF]] 위험 | 클러스터 매니저가 재시작 지원 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
**실무적 판단 (Technical Insight):**
배포 모드 선택은 **네트워크 토폴로지**와 직결된다.
- **[[019_data_locality|Data Locality]]:** 드라이버가 워커 노드와 물리적으로 멀리 떨어져 있으면([[003_audit_stakeholders|Client]] 모드), 셔플링(Shuffle)이나 [[012_metadata|메타데이터]] 교환 시 레이턴시가 급증한다.
- **K8s & Cloud:** 현대적인 스파크 아키텍처는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 위에서 Cluster 모드로 실행하는 것이 표준이다. 이는 리소스 격리와 자동 [[658_ir_recovery|복구]](Self-healing) 기능을 클러스터 매니저에게 완전히 위임할 수 있기 때문이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
스파크 배포 모드의 올바른 선택은 [[123_pipe|파이프]]라인의 효율성과 비용에 직접적인 영향을 미친다. 앞으로의 트렌드는 [[206_serverless_cold_start|서버리스]]([[206_serverless_cold_start|Serverless]]) 스파크다. 사용자가 모드를 고민할 필요 없이 인프라가 워크로드에 맞춰 최적의 배치를 자동 수행하는 방향으로 진화하고 있다. 하지만 여전히 [[282_performance_tactics|성능]] 트러블슈팅의 핵심 지점은 드라이버와 워커의 물리적 배치([[087_deployment_kubernetes_workload_rolling_update|Deployment]] Mode) 분석에서 시작된다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **부모 개념:** Distributed Computing, Resource [[372_management|Management]]
- **유사 개념:** [[020_yarn|YARN]] Scheduler, [[205_kubernetes_container_orchestration|Kubernetes]] [[565_operator_pattern_kubernetes_automation|Operator]]
- **하위 개념:** spark-submit, Application Master, Spark UI

### 📈 관련 키워드 및 발전 흐름도

```text
[로컬 모드 (Local Mode) — 단일 JVM에서 드라이버·익스큐터 실행, 개발·테스트용]
    │
    ▼
[독립 실행 모드 (Standalone Mode) — Spark 자체 클러스터 매니저, 소규모 전용 환경]
    │
    ▼
[YARN 모드 (YARN Mode) — 하둡 클러스터 자원 공유, 엔터프라이즈 표준]
    │
    ▼
[Kubernetes 모드 (K8s Mode) — Pod 단위 동적 프로비저닝, 클라우드 네이티브 표준]
    │
    ▼
[서버리스 Spark (Serverless Spark) — 클라우드 완전 관리형, 인프라 추상화 극대화]
```

이 흐름은 Spark의 배포 모드가 로컬 개발 환경에서 출발하여 [[020_yarn|YARN]] 클러스터 공유를 거쳐 [[205_kubernetes_container_orchestration|Kubernetes]] 기반 [[531_cloud_native_architecture|클라우드 네이티브]] 배포로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 지휘자(드라이버)가 연주자(실행기)들과 어디에 있느냐의 차이예요.
- 지휘자가 집에서 전화로 지휘하면 '클라이언트 모드', 공연장 무대 위에서 함께 있으면 '클러스터 모드'예요.
- 당연히 공연장 안에서 함께 호흡하며 연주하는 게 훨씬 소리도 잘 들리고 실수도 적겠죠?
