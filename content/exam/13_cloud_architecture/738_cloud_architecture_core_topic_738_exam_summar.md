---
title: "Cloud Architecture Core Topic 738 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

# 738. 클라우드 아키텍처 핵심 토픽 — 클라우드 네이티브 및 분산 시스템 설계

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 12-Factor App 원칙, 마이크로서비스, 컨테이너 오케스트레이션(Kubernetes), 서버리스(FaaS), 서비스 메시(Istio) 등을 결합하여 **탄력성(Elasticity), 장애 격리(Bulkhead), 무중단 배포(Zero-Downtime)** 를 코드로 구현하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)을 적용 시 **배포 빈도 200배·복구 시간 2,604배·변경 실패율 7분의 1**(DORA Report 2023), **TCO 30~60% 절감**, **Auto-Scaling으로 트래픽 10배 변동 대응**이 가능하다.
> 3. **판단 포인트**: Monolith vs Microservices, 동기(REST/gRPC) vs 비동기(Event-Driven/Kafka), Stateful vs Stateless, 단일 클라우드 vs 멀티/하이브리드, **CAP 정리 하의 일관성-가용성 트레이드오프**, 그리고 **FinOps 기반 비용-성능 최적점**이 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처는 **수직 확장(Scale-Up) 한계, 수개월 단위 배포 주기, 라이선스 종속성, Capacity Planning 실패**라는 구조적 문제를 안고 있었다. Netflix가 2008년 DB 손상으로 3일간 서비스 장애를 겪은 사건(Reese-Wikipedia 사례), 그리고 2017년 AWS S3 us-east-1 장애로 전 세계 인터넷 서비스가 마비된 사건은 **단일 장애점(SPOF)의 위험성**과 **클라우드 종속성(Vendor Lock-in)** 문제를 동시에 부각시켰다.

이에 따라 2013년 Netflix OSS(Netflix Open Source Software) 공개, 2014년 Docker GA, 2015년 Kubernetes 1.0, 2017년 Cloud Native Computing Foundation(CNCF) 설립, 2019년 Istio 1.0 등 **클라우드 네이티브 4대 축(컨테이너·오케스트레이션·서비스 메시·GitOps)**이 표준화되었다. 2024년 현재는 **Kubernetes + Service Mesh + Observability(OpenTelemetry) + GitOps(ArgoCD) + FinOps**가 de-facto 표준 스택으로 자리 잡았으며, AWS·Azure·GCP 모두 **Managed Kubernetes(EKS/AKS/GKE)**와 **서버리스(Lambda/Functions/Cloud Functions)**를 양대 핵심 서비스로 운영 중이다.

```text
[클라우드 네이티브 아키텍처 진화 흐름]

   2000s         2010s              2015            2020s
+---------+   +----------+      +----------+    +--------------+
|Monolith | -> | SOA/ESB  |  ->   |Container | ->  | Cloud-Native |
|  + DB   |   |(WebLogic)|      |+K8s+MSA  |    |Serverless+AI|
+---------+   +----------+      +----------+    +--------------+
      |              |                |                |
   수직확장       가상화          Docker 등장        eBPF+wasm
   라이선스       SOAP/REST       CNCF 설립         Edge+AI 통합
```

- **📢 섹션 요약 비유**: 기존 모놀리식 아키텍처는 **"한 권의 두꺼운 백과사전"** 처럼 한 곳에 모든 지식이 묶여 있어 한 페이지가 찢어지면 전체를 못 읽는다. 클라우드 네이티브는 **"위키피디아"** 처럼 수만 개의 작은 문서(서비스)로 나뉘어 있고, 일부가 사라져도 다른 문서로 보완되며, 조회수가 늘면 자동으로 미러 서버가 추가된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **"Stateless·분산·자가치유·선언적"** 4대 속성을 코드로 실현하는 것이다. 이를 구현하기 위한 5계층 참조 아키텍처는 다음과 같다.

```text
[5-Layer Cloud-Native Reference Architecture]

+-------------------------------------------------------------+
| L5. Observability (Prometheus+Grafana+OpenTelemetry+Loki)  |
+-------------------------------------------------------------+
| L4. Security/Policy (OPA, Falco, Trivy, cert-manager, mTLS) |
+-------------------------------------------------------------+
| L3. Service Mesh (Istio/Linkerd: mTLS, Traffic Mgmt, Retry) |
+-------------------------------------------------------------+
| L2. Orchestration (K8s+Helm+Kustomize+ArgoCD + Operators)   |
+-------------------------------------------------------------+
| L1. Runtime (Containerd/CRI-O, gVisor/Kata, WASM Runtime)   |
+-------------------------------------------------------------+
| L0. Infra(IaC): Terraform/Pulumi/Crossplane + Git Repo      |
+-------------------------------------------------------------+
           ^                ^                  ^
           |                |                  |
       [개발자]      [CI/CD Pipeline]    [Self-Healing Loop]
       Git Push ->  GitHub Actions/Jenkins  ->  자동 롤아웃
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 라우팅·인증·속도 제한 | **Kong(nginx+Lua), AWS API Gateway, Envoy**; OAuth2.0/JWT 검증, Rate Limiting(Token Bucket), Canary Release 5%->50%->100% 단계적 라우팅, **OpenAPI 3.0 스펙 자동 변환** |
| **Service Mesh** | 서비스 간 mTLS·관측·트래픽 제어 | **Istio(Envoy Sidecar), Linkerd(Rust Proxy), Cilium(eBPF)**: SPIFFE/SPIRE 기반 워크로드 ID, **SLO 99.9% -> 99.99% 전환 시 Circuit Breaker + Retry(2xx 한정) + Timeout(150ms p99) 정책 주입** |
| **Container Orchestration** | 컨테이너 스케줄링·자가치유·HPA | **Kubernetes 1.30+**: Pod(최소 배포 단위) -> Deployment(롤링 업데이트 maxSurge 25% / maxUnavailable 0) -> StatefulSet(순서 보장, PVC 바인딩) -> **HPA: CPU>70% 시 30초 간격 스케일 아웃, Karpenter로 노드 90초 내 프로비저닝** |
| **Event Streaming** | 비동기 메시지 전달·이벤트 소싱 | **Apache Kafka 3.6(KRaft 모드, Zookeeper 제거)**: Partition 128개, ISR(in-sync replicas) 3, Exactly-Once Semantics(EOS), **Pulsar(계층화 스토리지)·NATS(경량 pub/sub)·AWS Kinesis(완전 관리형)** |
| **Observability Stack** | 메트릭·로그·트레이스 통합 | **3 Pillars**: Prometheus(Counter/Gauge/Histogram + PromQL) + Grafana + Loki(Labels-based Log) + Tempo/Jaeger(Distributed Tracing, W3C TraceContext); **OpenTelemetry SDK로 자동 계측, RED/USE 메서드 적용** |
| **IaC & GitOps** | 인프라 코드화·선언적 배포 | **Terraform 1.7+(State locking by DynamoDB)+ Atlantis**: HCL로 멀티 클라우드 동일 코드, **ArgoCD(ApplicationSet) / Flux v2**: Git Repo와 Cluster 상태 동기화, Drift Detection 3분 주기 |
| **Serverless/FaaS** | 이벤트 기반 stateless 함수 실행 | **AWS Lambda(10GB 메모리, 15분 타임아웃), Azure Functions, GCP Cloud Run Jobs**: Cold Start 100~300ms->SnapStart/SnapStart Profiling로 50ms 단축, **Concurrency 1000, Provisioned Concurrency로 Warm Pool 운영** |

### 12-Factor App 원칙 (Heroku 2011, 현 PA&A 2022 확장판)

1. **Codebase**: 단일 Git Repo, 다중 배포
2. **Dependencies**: 명시적 선언(`requirements.txt`, `package-lock.json`)
3. **Config**: 환경변수 분리 (Vault/AWS Secrets Manager로 KMS 암호화)
4. **Backing Services**: DB·캐시를 Attached Resource로 취급, **AWS RDS↔Aurora Failover**
5. **Build, Release, Run**: 3단계 엄격 분리 (CI = Build, CD = Release, Runtime = Run)
6. **Processes**: Stateless, Sticky Session 금지 (Redis Session Storage)
7. **Port Binding**: 자체 HTTP 서버(`uvicorn :8000`), Tomcat 내장
8. **Concurrency**: 프로세스 모델로 수평 확장
9. **Disposability**: 빠른 시작(10s 내)·优雅 종료(SIGTERM 후 30s)
10. **Dev/Prod Parity**: 동일 백엔드 서비스 (Docker compose로 로컬 동일 환경)
11. **Logs**: 표준 출력(stdout) -> Fluent Bit -> OpenSearch
12. **Admin Processes**: 일회성 마이그레이션은 `kubectl job` 또는 AWS ECS Run Task

### 분산 시스템 핵심 알고리즘

- **Consensus**: **Raft Consensus**(etcd 내부 구현) - Leader Election 150~300ms, Log Replication
- **Service Discovery**: **DNS-based(K8s CoreDNS) + Client-side Load Balancing(Ribbon -> Envoy EDS)**
- **Distributed Lock**: Redis Redlock (5개 노드 중 과반수 3개 획득, lease-time 30s)
- **Consistent Hashing**: Cassandra/DynamoDB, **Virtual Node 256개로 데이터 편향 방지**
- **Saga Pattern**: **Orchestration(Step Functions/Temporal) vs Choreography(Event)**, 보상 트랜잭션(Compensating Tx) 정의 필수
- **Outbox Pattern**: DB 트랜잭션 + Outbox 테이블 -> Debezium CDC -> Kafka 발행 (Dual Write 문제 해결)
- **CRDT**: Redis Gears·Akka·Riak - 최종 일관성(Eventual Consistency) 보장 자료구조

- **📢 섹션 요약 비유**: Service Mesh는 **"도시의 도로교통 시스템"** 과 같다. 각 차량(서비스)이 직접 교차로 신호를 관리하지 않고, 중앙 교통관제센터(Istio Control Plane)가 실시간으로 신호를 조정한다. 사고 시 우회로를 자동 안내하고, 특정 구간에 정체량이 늘면 자동으로 신호 체계를 바꾼다. 개발자는 차만 만들면 된다(비즈니스 로직 집중).

---

## Ⅲ. 비교 및 연결

### Monolith vs Microservices vs Serverless 비교

| 구분 | Monolithic | Microservices (K8s) | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR (수 GB) | 컨테이너 이미지 (수백 MB) | 함수 코드 (수십 MB) |
| **확장 방식** | Scale-Up (수직) | Scale-Out (HPA, 수평) | 자동 (Concurrency 기반) |
| **장애 도메인** | 전체 중단 (1) | 서비스별 격리 (10~100) | 함수별 격리 (1000+) |
| **Cold Start** | 없음 (5~30s 부팅) | 1~3s (이미지 풀) | 100~500ms (Lambda) |
| **적합 워크로드** | 소규모·단일 도메인 | 중대형·MSA 전환 | 이벤트·간헐적·버스트성 |
| **TCO (3년)** | 초기 낮음, 스케일 시 급등 | 중상 (K8s 운영비 30%) | 종량제 (유휴 시 0원) |
| **장애 대응** | Rolling Deploy (수 분) | Blue/Green, Canary (분 단위) | 자동 (초 단위) |
| **Vendor Lock-in** | 없음 (WAS 종속) | 중간 (K8s API 표준화) | 높음 (벤더 종속) |
| **조직 정렬** | Conway's Law 위배 시 위험 | **2-pizza team (8명) 단위** | 단일 함수 = 단일 책임 |
| **트랜잭션** | ACID 단일 DB | Saga / 2PC / Outbox | Step Functions + DynamoDB |

### 주요 오케스트레이터 비교

| 구분 | Kubernetes 1.30 | Docker Swarm | Nomad 1.8 | AWS ECS Fargate |
| :--- | :--- | :--- | :--- | :--- |
| **시장 점유율** | 92% (CNCF 2023) | 5% 이하 | 3% | AWS 종속 |
| **학습 곡선** | 매우 높음 | 낮음 | 중간 | 중간 |
| **확장성** | 5,000 노드/클러스터 | 1,000 노드 | 10,000+ | 무제한 |
| **네이티브 기능** | Service Mesh·CRD·Operator | 제한적 | Consul/Vault 연동 | ALB·IAM·CloudWatch |
| **Multi-Cloud** | K8s 자체 + Rancher/Cluster API | △ | ◎ (HCL 통합) | △ (AWS 한정) |
| **비용** | 자체 운영 시 무료 | 무료 | OSS 무료 | Pay-per-use |

### 통신 패턴 비교

| 구분 | REST (동기) | gRPC (동기) | Kafka (비동기) | WebSocket (양방향) |
| :--- | :--- | :--- | :--- | :--- |
| **프로토콜** | HTTP/1.1 JSON | HTTP/2 + Protobuf 3 | TCP Binary | HTTP Upgrade |
| **지연시간** | 20~80ms | 5~15ms | 5~20ms (poll) | 1~5ms |
| **Throughput** | 1K rps | 10K rps | **수백만 msg/s** | 5K connections |
| **계약** | OpenAPI 3.0 | .proto IDL | Avro/Schema Registry | 자유 |
| **적합 사례** | 외부 API, BFF | 내부 MSA, Streaming | 이벤트 소싱, CDC | 채팅, 알림, IoT |

### 통합 생태계

- **개발 -> 배포**: Git -> **GitHub Actions**(CI: Build, Test, Trivy Scan) -> **ArgoCD**(CD: GitOps Sync) -> **K8s**
- **관측**: OpenTelemetry Collector -> **Tempo(Trace) + Loki(Log) + Mimir(Metric)** -> Grafana Unified Dashboard
- **보안**: **SLSA Level 3**(Supply Chain) + Sigstore(Cosign 서명) + **OPA/Gatekeeper**(Admission Control) + **Falco**(Runtime Threat Detection)
- **비용**: Kubecost / **OpenCost**(CNCF) -> AWS Cost Explorer 연동 -> FinOps Foundation Framework(Inform->Optimize->Operate)
- **데이터**: Transactional(PostgreSQL/CockroachDB) + Cache(Redis/Valkey) + Search(OpenSearch) + OLAP(ClickHouse/BigQuery) + Lakehouse(Iceberg/Delta)

- **📢 섹션 요약 비유**: Monolithic은 **"종합병원 한 곳"** (내과·외과·응급실 모두 한 건물, 한 곳 침수 시 전체 마비), Microservices는 **"전문화 의료단지"** (심장·신경·정형외과 별도 동, 한 곳 폐쇄 시에도 다른 진료 가능), Serverless는 **"119 구급차 호출"** (사고 발생 시에만 출동, 평소 대기 비용 0).

---


## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 738 / 800

<- **이전**: [737. 클라우드 아키텍처 핵심 토픽 737번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/737_cloud_architecture_core_topic_737_exam_summar/)
**다음**: [739. 클라우드 아키텍처 핵심 토픽 739번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/739_cloud_architecture_core_topic_739_exam_summar/) ->

---
