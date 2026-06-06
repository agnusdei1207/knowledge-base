---
title: "Cloud Architecture Core Topic 535 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 Well-Architected Framework(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성) 6대 원칙을 토대로, 마이크로서비스·이벤트 드리븐·메시 기반·서버리스·멀티클라우드 패턴을 워크로드 특성에 맞게 조합하는 분산 시스템 설계 체계이다.
> 2. **가치**: CAPEX->OPEX 전환(초기 인프라 비용 70~80% 절감), Auto Scaling을 통한 트래픽 10배 변동 흡수(응답 지연 P99 200ms 이하 유지), 글로벌 멀티리전 배포로 RTO 1분/RPO 0 달성, IaC(Infrastructure as Code) 기반 재해복구 자동화로 DR 훈련 시간 90% 단축이 가능하다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티클라우드/하이브리드, 동기 RPC vs 비동기 메시징(결과적 일관성), Stateful(데이터 일관성) vs Stateless(탄력성), Egress 비용·데이터 주권·컴플라이언스(개인정보보호법, ISMS-P, CSAP) 회피 trade-off가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-tier 아키텍처(웹-앱-DB)는 CAPEX 중심의 수직적 확장(Scale-up) 방식으로, 트래픽 예측 불가능한 현대 서비스 환경에서 **자원 과잉 투자(평균利用率 15~25%)**, **긴 프로비저닝 시간(주 단위)**, **DR 사이트의 유휴 비용 이중 발생** 문제를 야기한다. 2024년 기준 국내 공공·금융권을 중심으로 클라우드 전환 가속화(행정안전부 「클라우드 이용 촉진 기본 계획(2023~2027)」, 금융감독원 「금융회사 업무 연속성 관리 감독규정」)되며, AWS·Azure·GCP의 국내 리전 확충(각 3개 이상 리전)과 CSAP(클라우드 서비스 보안 인증) 도입 확대로 기술사 출제 빈도가 급격히 증가하고 있다.

특히 2024~2025년 트렌드는 단순 Lift & Shift를 넘어 **클라우드 네이티브**(Kubernetes, Istio, ArgoCD), **AI/LLM 통합**(클라우드 GPU 인스턴스, Bedrock/Vertex AI), **FinOps**(비용-성능-탄소 통합 거버넌스), **Zero Trust**(BeyondCorp, SDP) 중심으로 진화하고 있다.

```text
+---------------------------------------------------------------------+
|                  클라우드 아키텍처 패러다임 전환 흐름                |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise 3-Tier]  ---->  [Lift & Shift]  ---->  [Cloud-Native]  |
|        |                       |                       |           |
|  +-----+-----+           +-----+-----+          +------+------+    |
|  | Web/App/DB|           |  VM 단위  |          |  K8s/Istio  |    |
|  | 수직확장  |           |  IaaS 마이그 |          | 마이크로서비스|    |
|  | 수동 장애복구|           |  간단 이전  |          | CI/CD 자동화 |    |
|  +-----------+           +-----------+          +-------------+    |
|  CAPEX 다수 /           CAPEX+OPEX /            OPEX 중심 /        |
|  유틸 15~20%            유틸 30~40%             유틸 60~80%         |
|  DR RTO: 일 단위        DR RTO: 시간            DR RTO: 분 단위     |
+---------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 자가용(온프레미스)에서 시작해, 렌터카(VM 기반 IaaS)를 거쳐, 우버(서버리스·관리형 서비스)로 진화한 교통 수단과 같다. 각 단계는 통제권과 편의성·비용 간의 trade-off를 의미한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 책임 분담 모델**(책임 공유 모델)과 **4대 핵심 설계 패턴**(마이크로서비스, 이벤트 드리븐, CQRS/이벤트 소싱, 서킷 브레이커/벌크헤드)을 기반으로 한다. AWS Well-Architected, Azure WAF, GCP Architecture Framework 모두 6개 기둥을 공통으로 채택하므로 기술사 답안 작성 시 이 프레임워크를 명시해야 한다.

```text
+--------------------------------------------------------------------+
|          클라우드 네이티브 레퍼런스 아키텍처 (상위->하위)           |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------------------------------------------------------+      |
|  | Edge / CDN: CloudFront, Cloud CDN, Akamai, WAF/DDoS    |      |
|  +------------------------+---------------------------------+      |
|  +------------------------+---------------------------------+      |
|  | API Gateway / Ingress: Kong, AWS API GW, Apigee, Gloo   |      |
|  |  - 인증/인가(OAuth2, JWT, mTLS), Rate Limit, 라우팅      |      |
|  +------------------------+---------------------------------+      |
|  +------------+-----------+-----------+---------------------+      |
|  | Service A  |      Service B       |      Service C      |      |
|  | (Stateless)|      (Stateful)      |   (Serverless)     |      |
|  | K8s Pod ×N |   DB+RDS/Cloud SQL   |   Lambda/Functions |      |
|  +----+-------+-----------+-----------+----------+---------+      |
|  +----+-------------------+----------------------+---------+      |
|  |   Service Mesh: Istio / Linkerd (mTLS, 트래픽 관리)     |      |
|  +----+---------------------------------------------------++      |
|  +----+---------+  +--------------+  +------------------+|      |
|  |  Message Bus |  |  Event Bus   |  |  Stream Process  ||      |
|  | RabbitMQ/SQS |  | Kafka/PubSub |  |  Flink/Kinesis  ||      |
|  +----+---------+  +------+-------+  +--------+---------+|      |
|  +----+-------------------+------------------+------------++      |
|  | Data Layer: Polyglot Persistence                          |      |
|  |  - RDB (MySQL/PostgreSQL/Aurora)  - NoSQL (Dynamo/Mongo) |      |
|  |  - Cache (Redis/Memcached)        - Search (OpenSearch)  |      |
|  |  - OLAP (BigQuery/Snowflake/Redshift)                    |      |
|  +----------------------------------------------------------+      |
|  +----------------------------------------------------------+      |
|  | Cross-Cutting: Observability (Prometheus/Grafana/ELK)    |      |
|  |  Security (CSPM/CWPP/CIEM) / FinOps / IaC (Terraform)    |      |
|  +----------------------------------------------------------+      |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / BFF** | 단일 진입점, 라우팅·인증·스로틀링 | AWS API Gateway + Lambda Authorizer(OAuth2 JWT), Kong(nginx 기반, 플러그인 200+), GraphQL Federation(Apollo) |
| **Service Mesh** | 서비스 간 통신·보안·관찰성 | Istio(Envoy sidecar, mTLS 자동, 1% 카나리 배포), Linkerd(Linkerd2-proxy, Rust 기반 경량), Cilium(eBPF 기반 L3/L4/L7) |
| **Container Orchestrator** | 컨테이너 라이프사이클 관리 | Kubernetes 1.30+(CRD, Operator 패턴), EKS/AKS/GKE 관리형, Karpenter(V2 스케일링, 30초 내 노드 프로비저닝) |
| **이벤트·메시지 미들웨어** | 비동기 결합·이벤트 전파 | Kafka(Raft KRaft 모드, 100만 TPS/브로커), RabbitMQ(AMQP 0-9-1, 우선순위 큐), NATS JetStream(At-least-once) |
| **데이터 계층(Polyglot)** | 워크로드별 최적 스토리지 | OLTP(Aurora MySQL 5.6x), KV(DynamoDB 10ms p99), 시계열(Timestream), 검색(OpenSearch BM25+KNN) |
| **Observability 스택** | 3대 신호(Metric·Log·Trace) | OpenTelemetry SDK -> Tempo/Jaeger(Trace) + Prometheus(Metric) + Loki(Log) + Grafana, eBPF 기반 Cilium Tetragon |
| **IaC / GitOps** | 선언적 인프라·앱 배포 | Terraform 1.7+(HCL, State Lock), Pulumi(TS/Python), ArgoCD(Application CRD, 자동 Sync), Atlantis(Terraform PR 워크플로) |

**핵심 알고리즘·파라미터 심화**:
- **Auto Scaling 3축**: HPA(Horizontal Pod Autoscaler, CPU/메모리/커스텀 메트릭) + VPA(Vertical Pod) + Karpenter(노드) — 예측 스케일링(Predictive Scaling, 30분 선학습) 조합으로 콜드 스타트 제거
- **CAP 정리는 클라우드 분산 트랜잭션의 본질**: PostgreSQL+CockroachDB는 CP, DynamoDB/Cassandra는 AP, RabbitMQ+Kafka는 결과적 일관성(Eventually Consistent) — Saga 패턴(Orchestration/Choreography)으로 보완
- **서킷 브레이커 임계값**: Hystrix/Resilience4j 기준 `failureRateThreshold=50%`, `slidingWindowSize=100`, `waitDurationInOpenState=10s` -> Half-Open으로 점진 회복
- **k8s Pod 스케줄링**: `requests/limits`는 QoS Class(Guaranteed/Burstable/BestEffort) 결정, `topologySpreadConstraints`로 AZ 분산, `podAntiAffinity`로 노드 분산

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 오케스트라에 비유할 수 있다. 컨덕터(Service Mesh/Istio control plane)가 악기들(서비스)을 조율하고, 악보(IaC 코드)가 일관된 연주를 보장하며, 관객(Observability)은 실시간으로 연주 상태를 듣는다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 내 핵심 개념들의 비교는 기술사 답안에서 가장 빈번히 출제되는 영역이다. 단순 암기형이 아닌 **"X 상황에서 Y를 선택하는가"**라는 시나리오형 답안이 고득점의 열쇠다.

| 구분 | Monolith (전통) | Microservices | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR | 컨테이너 이미지 | 함수 코드(ZIP/Container) |
| **확장성** | Scale-up (수직) | HPA + Service Mesh | 자동(Concurrency 한도) |
| **장애 도메인** | 1개 (전체) | 서비스별 격리 | 함수별 격리 |
| **콜드 스타트** | 없음 | 없음 | 100ms~3s(런타임별 상이) |
| **적합 워크로드** | 소규모·단일팀·CRUD | 중대형·다기능·MSA | 이벤트성·간헐적·API |
| **Vendor Lock-in** | 낮음 | 중간 | 높음(벤더 종속) |
| **비용 모델** | 상시 과금 | 상시 과금 | 호출당 과금(GB-초) |
| **대표 사례** | Legacy ERP | Netflix 700+ 서비스 | 이미지 썸네일, Cron |

| 구분 | IaaS (EC2) | PaaS (Beanstalk/App Service) | SaaS (구글 워크스페이스) | CaaS (EKS/AKS) |
| :--- | :--- | :--- | :--- | :--- |
| **제어 수준** | OS·네트워크까지 | 앱 코드만 | 사용만 | 컨테이너까지 |
| **책임** | 사용자(OS^) | 중간 | 벤더(전부) | OS 미들웨어(공유) |
| **자동화** | 수동/Ansible | 부분 자동 | 완전 자동 | 완전 자동 |
| **이식성** | 높음(VM 이미지만) | 중간 | 없음 | 높음(OCI 표준) |
| **적합** | 레거시 리프트 | 웹앱 빠른 출시 | 협업툴 | MSA 표준 |

**연계 기술 스택**:
- **CI/CD**: Jenkins -> GitHub Actions -> GitLab CI -> Tekton(쿠버네티스 네이티브) -> Argo Workflows
- **보안**: CSPM(Prisma Cloud, Wiz, Lacework) + CWPP(Twistlock, Aqua) + CIEM(시드 권한 분석)
- **FinOps**: CloudHealth, AWS Cost Explorer, KubeCost, OpenCost(쿠버네티스 네이티브), Spot.io(스팟 인스턴스 최적화)
- **AIOps/관찰**: Datadog, New Relic, Dynatrace, Splunk Observability, Grafana Cloud(LGTM 스택)

- **📢 섹션 요약 비유**: IaaS/PaaS/SaaS/CaaS는 식당에서 주방 사용 범위에 비유할 수 있다. IaaS는 식재료·불판까지 직접 만지고, PaaS는 불판은 주방장이 관리, SaaS는 배달로 받고, CaaS는 화구만 빌리는 개념이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험은 단순 지식 암기가 아닌 **"주어진 시나리오에서 어떤 아키텍처를 선택하고 그 이유는 무엇인가"**를 묻는 시나리오 문제가 70% 이상이다. 특히 "비용/성능/보안/가용성"의 4축 trade-off와 **"현실적 제약(예산, 인력, 일정)"**을 어떻게 합리화하는지가 채점 포인트다.

### 기술사형 판단 체크리스트

1. **워크로드 분류 후 패턴 결정**: 트랜잭션 OLTP/배치 OLAP/스트리밍/배달 보장(DLQ 포함) — 각 도메인에 맞는 분산 패턴(Saga/Outbox/Choreography)을 적용했는가? 동시성 1000 TPS 이상이면 CQRS+이벤트 소싱 검토
2. **멀티 AZ/리전 가용성**: 단일 AZ(99.5%, 월 4시간 장애) -> 멀티 AZ(99.99%, 52분) -> 멀티 리전 액티브-액티브(99.999%, 5분) — RTO/RPO 요구 수준별 데이터 복제 전략 결정. Aurora Global Database(크로스 리전 복제 1초 미만 RPO), DynamoDB Global Tables(멀티 리전 멀티 마스터)
3. **비용 최적화(FinOps)**: RI/Savings Plans(40~60% 절감) + Spot Instance(70~90% 절감, 배칭·테스트 워크로드) + S3 Intelligent-Tiering(자동 계층화) + Egress 비용 최소화(클라우드 간 전송 $0.02~0.09/GB) — NACL·VPC Endpoint(S3 Gateway Endpoint 무료)로 NAT 비용 절감
4. **보안·컴플라이언스**: CSAP/ISMS-P/개인정보보호법 — KMS-CMK 고객 관리 키 + CloudHSM(FIPS 140-2 L3) + Secrets Manager/Parameter Store 회전 + VPC Flow Logs + GuardDuty(ML 기반 이상 행위) + AWS Macie(PII 자동 탐지)
5. **관찰 가능성(Observability)**: SLI/SLO/SLI Budget 정의(예: 99
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 535 / 800

<- **이전**: [534. 클라우드 아키텍처 핵심 토픽 534번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/534_cloud_architecture_core_topic_534_exam_summar/)
**다음**: [536. 클라우드 아키텍처 핵심 토픽 536번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/536_cloud_architecture_core_topic_536_exam_summar/) ->

---
