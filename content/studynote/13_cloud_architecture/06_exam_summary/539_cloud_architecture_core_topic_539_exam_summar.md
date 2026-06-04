---
title: "539. 클라우드 아키텍처 핵심 토픽 539번 시험 요약 (Cloud Architecture Core Topic 539 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


# 📘 기술사 시험 대비 – 클라우드 아키텍처 핵심 토픽 (539번) 요약

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 *Well-Architected Framework(WAF)의 6대 필러(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)*를 코드형 인프라(IaC), 마이크로서비스, 서버리스, 옵저버빌리티로 구현하는 **클라우드 네이티브(Cloud-Native) 설계 체계**이며, *12-Factor App*과 *Cloud Native Computing Foundation(CNCF) 트래일 맵*을 토대로 자가치유·탄력적 확장·선언적 자동화를 달성한다.
> 2. **가치**: CAPEX->OPEX 전환으로 TCO 30~60% 절감, Auto-Scaling으로 트래픽 피크 시 응답지연 40~70% 단축, MTTR 80% 감소, 멀티 리전 Active-Active 구성으로 가용성 99.99%(4-nines, 연간 downtime 52.6분) 확보가 가능하다.
> 3. **판단 포인트**: *6R 마이그레이션 전략(Rehost/Replatform/Refactor/Re-purchase/Retire/Retain)* 중 어디에 해당하는지, **트레이드오프 매트릭스(Stateful vs Stateless, 동기 vs 비동기, 일관성 vs 가용성 - CAP/ACID/BASE)**, 그리고 *클라우드 락인 리스크(AWS Graviton vs Azure ARM vs GCP Anthos)*를 정량적 비용/성능/SLA로 비교하여 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-Tier 아키텍처는 L4/L7 로드밸런서, Web-WAS-DB 티어, SAN 스토리지, IDC의 HW 수명주기(3~5년)에 종속되어 *Capacity Planning* 실패 시 *Over-Provisioning*으로 CAPEX가 2~3배 증가하고, Peak 시간 외 70% 자원이 유휴 상태로 낭비된다. 또한 *Monolithic Application*은 배포 단위가 크기 때문에 1일 1배포가 사실상 불가능하며, *Mean Time To Recovery(MTTR)*가 수십 분~수 시간에 달한다.

클라우드 아키텍처는 *탄력성(Elasticity)*, *민첩성(Agility)*, *페이퍼롭니스(Pay-per-use)*라는 본질적 특성으로 이러한 한계를 극복한다. NFV(Network Functions Virtualization)와 SDN(Software Defined Networking)의 결합, *Hypervisor(KVM/Xen/Hyper-V)* 기반의 컴퓨트 가상화, *Software-Defined Storage(Ceph, vSAN)*, 그리고 *Multi-AZ(Availability Zone)*·*Multi-Region* 토폴로지를 통해 동일 데이터센터 내에서도 물리적/논리적 장애 도메인을 분리한다.

```text
[클라우드 컴퓨팅 진화 단계 & 책임 공유 모델]

   책임 범위
   ^ 많이   +-----------------------------------------+
   |  고객   |  On-Premise    IaaS    PaaS    SaaS    | <- 사용자가 관리
   |         |  ████████    ████░░░  ██░░░░  ░░░░░░  |
   |         |  ████████    ████░░░  ██░░░░  ░░░░░░  |
   |         |  ████████    ████░░░  ██░░░░  ░░░░░░  |
   |         |  ████████    ████░░░  ░░░░░░  ░░░░░░  |
   |         |  ████████    ░░░░░░░  ░░░░░░  ░░░░░░  |
   | 적게    |  ████████    ████████  ████████  ████████| <- CSP가 관리
   |         +-----------------------------------------+
   |              앱/데이터  앱/데이터  앱/데이터  앱/데이터
   |              런타임     런타임     데이터
   |              미들웨어   미들웨어
   |              OS         OS
   |              가상화     가상화
   |              서버       서버       서버       서버
   |              스토리지   스토리지   스토리지   스토리지
   |              네트워크   네트워크   네트워크   네트워크
   +-----------------------------------------►

   [배포 모델 스펙트럼]
   +----------+  +----------+  +----------+  +----------+  +----------+
   | Private  |  |Community |  | Public   |  | Hybrid   |  | Multi    |
   | Cloud    |  | Cloud    |  | Cloud    |  | Cloud    |  | Cloud    |
   | (전용)   |  | (공동)   |  | (AWS 등) |  | (연계)   |  | (분산)   |
   +----------+  +----------+  +----------+  +----------+  +----------+
        |              |              |              |              |
        +--------------+------+-------+--------------+--------------+
                              v
                  클라우드 버스팅(Bursting) /
                  데이터 주권(Residency) / DR
```

기존 *Waterfall + 수작업 인프라*에서 *DevOps + IaC(Terraform/CloudFormation/ARM/Pulumi)* 기반으로 패러다임이 전환되면서, *Code Commit -> CodeBuild -> CodeDeploy/ArgoCD*로 이어지는 GitOps 파이프라인이 *불변 인프라(Immutable Infrastructure)*를 코드 형태로 관리한다. 이로써 *환경 드리프트(Environment Drift)*가 제거되고, *Auditability*와 *Reproducibility*가 확보된다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **호텔 체인의 객실 관리 시스템**과 같다. 손님(트래픽)이 몰리면 빈 방을 즉시 배정(Auto-Scaling)하고, 손님이 떠나면 청소 후 일반 객실로 회수(Scale-In)하며, 지진(리전 장애)이 발생하면 다른 지점 호텔로 즉시 이관(DR)한다. 고정 식당(On-Prem)은 좌석 수만큼만 매출이 가능하지만, 호텔은 수요에 따라 객실을 빌려쓰는(Pay-per-use) 만큼 수익을 극대화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 메커니즘은 **선언적 API(Declarative API) + 컨트롤 루프(Control Loop)**이다. 사용자가 *"원하는 상태(Desired State)"*를 YAML/JSON으로 선언하면, 컨트롤러(Kubernetes Controller, AWS Auto Scaling Group, Azure VMSS 등)가 *Observe -> Diff -> Reconcile* 루프를 통해 지속적으로 실제 상태를 원하는 상태로 수렴시킨다.

```text
[AWS Well-Architected Framework 6대 필러 구조]

                         +------------------+
                         |   Cloud          |
                         |   Workload       |
                         |  (Application)   |
                         +--------+---------+
                                  |
        +------------+------------+------------+------------+------------+
        v            v            v            v            v            v
  +----------+ +----------+ +----------+ +----------+ +----------+ +----------+
  |운영 우수성| |  보안     | | 안정성    | |성능 효율성| |비용 최적화| |지속 가능성|
  |  OPS    | |  SEC     | |  REL     | |  PERF    | |  COST    | |  SUS     |
  +----+-----+ +----+-----+ +----+-----+ +----+-----+ +----+-----+ +----+-----+
       |            |            |            |            |            |
  +----+----+  +----+----+  +----+----+  +----+----+  +----+----+  +----+----+
  |Monitoring|  |IAM/KMS/ |  |Multi-AZ |  |Caching/ |  |RI/SP/   |  |Carbon   |
  |Runbook   |  |WAF/      |  |Circuit  |  |CDN/     |  |Savings   |  |Aware    |
  |CI/CD     |  |Shield/   |  |Breaker/ |  |Auto-    |  |Plans/   |  |Region   |
  |SRE       |  |GuardDuty |  |Retry/   |  |Scaling/ |  |S3       |  |Choice/  |
  |          |  |          |  |Bulkhead |  |Lambda   |  |Glacier  |  |Efficient|
  +----------+  +----------+  +----------+  +----------+  +----------+  +----------+

   <---- Design Principles ----->
   • Stop guessing capacity     • Implement strong identity foundation
   • Produce systems in small,  • Enable traceability              • Manage ...
   • Test security at all layers • Automate failure recovery
```

**핵심 작동 원리 - Kubernetes Control Loop 예시**:
1. 사용자가 `kubectl apply -f deployment.yaml`로 `replicas: 5` 선언
2. API Server가 etcd에 desired state 저장
3. Deployment Controller가 `actual=3, desired=5` 차이 감지
4. ReplicaSet Controller가 2개 Pod 추가 생성 (Scheduler가 Node 할당)
5. kubelet이 Container Runtime(containerd/CRI-O) 통해 Pod 기동
6. 30초 주기로 status reconcile -> Self-Healing

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층 (Compute)** | 워크로드 실행 | EC2(Intel/AMD/Graviton3 ARM), Lambda(Cold Start 100~300ms, 10GB 메모리), Fargate(EKS/ECS), Azure VMSS, GCP MIG(Machine Type: n2/m2/c2) |
| **네트워크 계층 (Network)** | 라우팅/보안 | VPC/Subnet(CIDR 설계, /16~/19), Transit Gateway(Hub-Spoke), ALB(L7, WAF 통합), NLB(L4, 고정 IP), CloudFront/Cloud CDN, PrivateLink/VPC Endpoint, Cilium(eBPF) |
| **스토리지 계층 (Storage)** | 데이터 영속성 | Block(EBS gp3 12,000 IOPS, io2 64,000 IOPS), Object(S3 11 9s durability, Intelligent-Tiering), File(EFS/FSx for Lustre), Cold(Glacier Deep Archive $0.00099/GB) |
| **데이터 계층 (Data)** | 트랜잭션/분석 | OLTP(Aurora 5x MySQL, Aurora Global Database < 1초 RPO), OLAP(Redshift Serverless, BigQuery, Snowflake), NoSQL(DynamoDB Single-Master->Global Tables Multi-Region, Cassandra) |
| **오케스트레이션** | 컨테이너 관리 | Kubernetes 1.29+(CRD, Operator Pattern), Service Mesh(Istio Ambient, Linkerd 2.15+), GitOps(ArgoCD/Flux), Karpenter(Just-in-Time Node Provisioning) |
| **옵저버빌리티** | 가시성/관측 | 3 Pillars: Metrics(Prometheus, CloudWatch), Logs(Loki, OpenSearch), Traces(OpenTelemetry->Jaeger/Tempo), AIOps(Datadog Watchdog, Grafana ML) |
| **보안 계층** | Zero Trust 구현 | IAM RBAC/ABAC, KMS/HSM, Secrets Manager, SOC2/ISO27001/PCI-DSS, CSPM(Prisma Cloud, Wiz), CIEM, CWPP, SBOM(Syft, Grype) |
| **IaC/거버넌스** | 선언적 자동화 | Terraform 1.6+(State Locking, Module Registry), Pulumi(Multi-Language), OPA/Gatekeeper(Policy as Code), Service Catalog, Landing Zone(AWS Control Tower, Azure CAF) |

**핵심 알고리즘/수식**:
- **Auto-Scaling 의사결정**: `desired = ceil(current_capacity × max(1, current_metric / target_metric))`
- **Consistent Hashing (DynamoDB/Cassandra Partitioning)**: `partition = hash(partition_key) mod N` -> 가상 노드 256개로 리밸런싱 최소화
- **Raft Consensus** (etcd/Consul): Leader Election + Log Replication, `election_timeout = 150~300ms` 랜덤화
- **비용 최적화 공식**: `TCO = Σ(Compute×Hours + Storage×GB×Months + Egress×GB) + λ×License - μ×Reserved Discount`
- **가용성 공식**: `System_Availability = 1 - Π(1 - Component_Availability)` -> 직렬 99.9% × 99.9% = 99.99%

- **📢 섹션 요약 비유**: **자율주행차의 비전 시스템**과 같다. 라이다/LiDAR(Observability)로 주변을 살피고, GPS/지도(IaC 선언)를 기준으로 현재 위치(Actual State)와 목적지(Desired State)를 비교하며, ECU(Controller Loop)가 핸들·액셀러레이터를 자동으로 조작하여 목적지까지 이동한다. 운전자가 매번 미세조정(수동 배포)을 할 필요 없이 *"목적지만 알려주면"* 알아서 운행한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 유사/대안/선행 기술과 비교할 때 **추상화 수준**, **관리 책임 경계**, **확장 단위**, **과금 모델**의 네 축으로 명확히 구분된다. 기술사 시험에서는 *언제 어떤 모델을 선택할 것인가*의 **결정론적 트레이드오프**를 묻는 문제가 빈출한다.

| 구분 | **IaaS (Infrastructure-as-a-Service)** | **PaaS (Platform-as-a-Service)** | **SaaS (Software-as-a-Service)** | **FaaS (Function-as-a-Service)** | **On-Premise** |
| :--- | :--- | :--- | :---
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 539 / 800

<- **이전**: [538. 클라우드 아키텍처 핵심 토픽 538번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/538_cloud_architecture_core_topic_538_exam_summar/)
**다음**: [540. 클라우드 아키텍처 핵심 토픽 540번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/540_cloud_architecture_core_topic_540_exam_summar/) ->

---
