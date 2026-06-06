---
title: "AIOps Intelligent IT Operations"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AIOps(Artificial Intelligence for IT Operations)는 대규모 분산 시스템에서 발생하는 Metrics·Logs·Traces·Events(MELT) 4대 관측 데이터를 스트리밍 처리하고, 머신러닝·통계 분석·인과 추론을 통해 이상 탐지(Anomaly Detection), 이벤트 상관관계 분석(Event Correlation), 근본 원인 분석(RCA), 자동 복구(Self-Healing)를 수행하는 지능형 운영 패러다임이다.
> 2. **가치**: Gartner 보고 기준 AIOps 도입 기업은 MTTD(Mean Time To Detect) 70%, MTTR(Mean Time To Resolve) 60%, 알림 노이즈(Alert Noise) 90% 절감을 달성하며, L1/L2 운영 인력을 30~50% 절감하고 SLO/SLA 준수율을 99.95% 이상으로 끌어올린다.
> 3. **판단 포인트**: AIOps는 "데이터 파이프라인 품질 -> 특징 공학(Feature Engineering) 고도화 -> MLOps 거버넌스 -> 폐루프 자동화(Closed-Loop Automation)"의 4단계 성숙도 모델을 따르며, 기술사적 판단 기준은 ①관측 데이터 통합(Observability Integration) ②도메인별 모델 선택(지도/비지도/강화학습) ③인과관계 추론의 인공 상관 제거 ④Human-in-the-Loop 거버넌스 ⑤Shadow Mode 검증 전략이다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 운영은 Nagios/Zabbix 같은 룰 기반 모니터링과 ITIL 기반 ITSM 프로세스에 의존해왔다. 그러나 클라우드 네이티브 환경(쿠버네티스, MSA, 서버리스)으로 전환되면서 시스템 구성 요소가 수십만 개로 폭증하고, 하루에 발생하는 이벤트 수가 PB급에 달하면서 **"3V 문제(Volume·Velocity·Variety)"**가 발생했다. IDC 보고에 따르면 Fortune 500 기업의 평균 이벤트 발생량은 하루 5~10억 건으로, 운영자가 이 중 의미 있는 인시던트를 식별하는 확률은 1% 미만이다.

기존 방식의 한계:
- **정적 임계치(Static Threshold)**: CPU 80% 같은 고정 규칙은 시간대별, 워크로드별 정상 패턴을 구분하지 못해 오탐(False Positive)이 70~95%에 달함
- **사일로 데이터(Siloed Data)**: APM, NPM, 로그, ITSM 데이터가 분리되어 있어 상관 분석 불가
- **수대응(Reactive)**: 장애 발생 후 알림 -> 수동 티켓 생성 -> 수동 Runbook 실행으로 MTTR 평균 4~8시간 소요
- **알림 피로(Alert Fatigue)**: 야간/주말에도 1,000건/일 알림으로 인한 On-call 이탈률 40% 이상

AIOps는 **"관측 가능성(Observability) 2.0"**의 핵심 엔진으로, 2016년 Gartner가 처음 명명했으며 현재는 하이퍼-자동화(Hyper-Automation) 플랫폼의 중추 신경계로 자리잡았다. 한국에서는 2021년 금융권 클라우드 도입 확대, 2023년 디지털 인재원 AIOps 교육과정 개설, 2024년 과기정통부 "지능형 IT 운영 자율화 가이드라인"发布 이후 공공·금융·통신 중심으로 확산 중이다.

```text
+----------------------------------------------------------------------+
|              AIOps 도입 배경: 4대 Pain Point 해결                      |
+----------------------------------------------------------------------+
|                                                                      |
|  [Before: 전통 운영]              [After: AIOps 기반 운영]              |
|                                                                      |
|  +----------------+               +---------------------+             |
|  | 정적 임계치     |  ------►     | 동적 베이스라인       |             |
|  | (CPU>80% 고정) |               | (시계열+계절성 학습)   |             |
|  +----------------+               +---------------------+             |
|                                                                      |
|  +----------------+               +---------------------+             |
|  |사일로 모니터링   |  ------►     | 통합 Observability   |             |
|  |(도구 10개 이상)  |               | (OpenTelemetry 표준)  |             |
|  +----------------+               +---------------------+             |
|                                                                      |
|  +----------------+               +---------------------+             |
|  | 수동 티켓팅     |  ------►     | Auto-Ticketing +     |             |
|  | (티켓 작성 30분) |               | LLM 기반 요약(1초)   |             |
|  +----------------+               +---------------------+             |
|                                                                      |
|  +----------------+               +---------------------+             |
|  | 사후 대응       |  ------►     | 예측·예방(Predictive)|             |
|  | (MTTR 4시간+)  |               | (장애 30분 전 탐지)   |             |
|  +----------------+               +---------------------+             |
|                                                                      |
+----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: AIOps는 마치 "항공관제사의 두뇌"와 같다. 레이다(관측 데이터)만으로는 비행기가 100대일 때 감당이 되지만, 1만 대가 되면 통제불능이다. AI 두뇌를 이식하면 충돌 위험을 사전에 예측하고, 최적 활주로까지 자동 안내한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AIOps 표준 아키텍처는 Gartner가 제시한 **"3-Domain Model"** (Domain Observability, Domain Engagement, Domain Action)을 중심으로 5계층 파이프라인으로 구성된다.

```text
+-------------------------------------------------------------------------+
|                  AIOps 5-Layer Reference Architecture                    |
|                                                                          |
|  +-------------------------------------------------------------------+  |
|  | ① Data Ingestion Layer (수집)                                     |  |
|  |  • Metrics: Prometheus scrape, Telegraf, Vector, OTel Collector   |  |
|  |  • Logs:    Fluentd/Logstash, Loki, Fluent Bit, Vector            |  |
|  |  • Traces:  Jaeger, Zipkin, OpenTelemetry SDK, eBPF               |  |
|  |  • Events:  ITSM APIs(ServiceNow/Jira), ChatOps(Slack/Webex)     |  |
|  |  • CMDB:    ServiceNow CMDB, Backstage, AWS Config                 |  |
|  +--------------------------+----------------------------------------+  |
|                             v                                            |
|  +-------------------------------------------------------------------+  |
|  | ② Big Data Storage Layer (저장·가공)                              |  |
|  |  • Time-series:   InfluxDB, TimescaleDB, Prometheus TSDB, M3     |  |
|  |  • Log Store:     Elasticsearch, ClickHouse, Loki, Splunk SPL    |  |
|  |  • Data Lake:     S3/MinIO + Delta Lake/Iceberg (Parquet)         |  |
|  |  • Stream Buffer: Apache Kafka, Pulsar, Redpanda (Exactly-Once)   |  |
|  |  • Feature Store: Feast, Tecton (모델 학습용 특징 저장)             |  |
|  +--------------------------+----------------------------------------+  |
|                             v                                            |
|  +-------------------------------------------------------------------+  |
|  | ③ AI/ML Analytics Layer (지능 분석) - AIOps Core Brain             |  |
|  |                                                                    |  |
|  |  [3-A] Anomaly Detection (이상 탐지)                               |  |
|  |         • 통계: STL 분해, EWMA, Prophet(메타)                       |  |
|  |         • ML:   Isolation Forest, One-Class SVM                     |  |
|  |         • DL:   LSTM-AE, Transformer(N-BEATS, Informer)            |  |
|  |                                                                    |  |
|  |  [3-B] Event Correlation (이벤트 상관)                             |  |
|  |         • Topology-aware: CMDB/Service Graph 기반 그래프 탐색      |  |
|  |         • Temporal:    Hawkes Process, Granger Causality           |  |
|  |         • NLP-based:   sentence-BERT 임베딩 유사도 클러스터링        |  |
|  |         • Graph:       GNN(GCN/GAT) 전파 모델                       |  |
|  |                                                                    |  |
|  |  [3-C] Root Cause Analysis (근본 원인 분석)                        |  |
|  |         • Causal Inference: DoWhy, CausalImpact, PC-Algorithm      |  |
|  |         • Bayesian Network: pgmpy, bnlearn                         |  |
|  |         • Log Mining:   LogCluster, Drain, LogBERT                  |  |
|  |                                                                    |  |
|  |  [3-D] Predictive (예측)                                           |  |
|  |         • Capacity: TFT(Temporal Fusion Transformer)               |  |
|  |         • Incident: Gradient Boosting + Survival Analysis          |  |
|  |         • LLM Ops:    GPT-4/Claude/Exaone for RAG Runbook          |  |
|  +--------------------------+----------------------------------------+  |
|                             v                                            |
|  +-------------------------------------------------------------------+  |
|  | ④ Engagement Layer (참여·오케스트레이션)                           |  |
|  |  • Alert Deduplication & Grouping (알림 중복 제거)                 |  |
|  |  • Priority Scoring (비즈니스 영향 기반 우선순위)                   |  |
|  |  • Collaboration: Slackbot, MS Teams, PagerDuty/Opsgenie           |  |
|  |  • ITSM Auto-Ticket: ServiceNow/Jira/Zendesk 양방향 연동           |  |
|  |  • War Room: Zoom/Webex 자동 개설, LLM 기반 인시던트 요약            |  |
|  +--------------------------+----------------------------------------+  |
|                             v                                            |
|  +-------------------------------------------------------------------+  |
|  | ⑤ Action Layer (자동화·폐루프 실행)                                |  |
|  |  • Runbook Automation: Ansible, Terraform, ArgoCD, Crossplane     |  |
|  |  • ChatOps:  Slack Workflow + Slash Command                        |  |
|  |  • Closed-Loop: ITSM -> Runbook -> 검증 -> CMDB 업데이트              |  |
|  |  • Self-Healing:  K8s Operator, Lambda, Azure Arc, GCP Config      |  |
|  |  • Approval Gate: 고위험 액션은 Human-in-the-Loop 필수               |  |
|  +-------------------------------------------------------------------+  |
|                                                                          |
|  [보안 횡단 계층: RBAC/ABAC, Audit Logging, PII 마스킹, DLP]              |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Data Ingestion** | MELT+E(Metrics/Logs/Traces/Events+CMDB) 통합 수집 | OpenTelemetry Collector(OTLP 프로토콜), eBPF 기반 커널 레벨 수집(Cilium Tetragon), Kafka Exactly-Once SemEOS, Vector vs Fluent Bit 경량 에이전트 |
| **② Storage & Lake** | 시계열·로그·원시 데이터 분리 저장 | Cold Path(S3+Parquet+ZSTD) + Hot Path(TSDB/Loki) 하이브리드, Kafka 7일 retention, Feature Store로 모델 학습/추론 일관성 보장 |
| **③ Analytics (Core)** | AI/ML 기반 4대 분석(Anomaly/Correlation/RCA/Predict) | STL 시계열 분해 + Prophet(메타) + LSTM-AE(다변량) 하이브리드, GNN으로 토폴로지 전파 모델링, DoWhy 인과 그래프, LogBERT 토큰 임베딩 |
| **④ Engagement** | 알림 노이즈 제거 및 협업 자동화 | Median Absolute Deviation(MAD) 기반 동적 임계치, TF-IDF+Cosine 유사도 알림 그룹핑, 비즈니스 컨텍스트(BLM) 기반 우선순위 |
| **⑤ Action & Remediation** | 폐루프 자동 복구 및 Human Gate | Ansible/Terraform IaC, Argo Rollouts 카나리 배포, K8s Operator 패턴, Argo Events 트리거, ChatOps 승인 워크플로우 |
| **MLOps 거버넌스** | 모델 학습·배포·모니터링 표준화 | MLflow + Kubeflow, Shadow Mode A/B, Data Drift(KL-divergence)/Concept Drift 감시, Champion/Challenger 자동 승격 |
| **보안·컴플라이언스** | 데이터 거버넌스 및 감사 | ISO 27001/SOC2, PII 토큰화(MaskGAN), Audit Log 변조 방지(Blockchain 또는 WORM), RBA(Risk-Based Authentication) |

**핵심 알고리즘 상세 (기술사 빈출)**

1. **이상 탐지 (Anomaly Detection)**
   - **통계적 방법**: STL(Seasonal-Trend decomposition using LOESS)로 시계열을 Trend/Seasonal/Residual로 분해 -> Residual의 MAD(Median Absolute Deviation)로 동적 임계치 산출. Z-score = (x - median) / (1.4826 × MAD) ≥ 3.5 시 알람
   - **머신러닝**: Isolation Forest는 iTree 100개로 무작위 분할하여 고립 깊이가 짧은 포인트를 이상으로 판정 (메모리 O(n), 학습 O(n log n))
   - **딥러닝**: LSTM-Autoencoder는 정상 패턴을 재구성하도록 학습 후, Reconstruction Error가 임계치 초과 시 이상. 변수가 100+ 일 때 PCA 사전 차원축소 필수

2. **이벤트 상관관계 분석 (Event Correlation)**
   - **시간적 상관**: Granger Causality Test로 "A 시계열의 과거가 B를 예측하는가" 검증 (p-value < 0.05)
   - **의미적 상관**: sentence-BERT로 로그 메시지를 768차원 벡터로 임베딩 -> DBSCAN 클러스터링 (eps=0.3, min_samples=5)
   - **토폴로지 상관**: CMDB/Service Map을 그래프로 모델링 -> PageRank 변형으로 영향도 전파 계산 -> 노드 간 인과 점수 산출

3. **근본 원인 분석 (RCA)**
   - **인과 추론 (Causal Inference)**: DoWhy 라이브러리로
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 584 / 600

<- **이전**: [583. MLOps 머신러닝 운영 자동화 파이프라인](/studynote/11_design_supervision/06_exam_summary/583_mlops_machine_learning_operations_pipeli)
**다음**: [585. GitOps 선언적 인프라 관리 패턴](/studynote/11_design_supervision/06_exam_summary/585_gitops_declarative_infrastructure_patter/) ->

---
