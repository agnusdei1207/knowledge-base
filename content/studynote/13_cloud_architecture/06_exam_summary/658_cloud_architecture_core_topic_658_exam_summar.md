---
title: "658. 클라우드 아키텍처 핵심 토픽 658번 시험 요약 (Cloud Architecture Core Topic 658 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **IaaS/PaaS/SaaS/FaaS/CaaS**의 서비스 모델과 **Public/Private/Hybrid/Multi-Cloud** 배치 모델을 기반으로, **Well-Architected Framework**(보안·신뢰성·성능 효율·비용 최적화·운영 우수성·지속 가능성)의 6대 필러를 동시 만족시키는 **분산 시스템 설계의 종합 학문**이다.
> 2. **가치**: 온프레미스 대비 **CapEx->OpEx 전환**, Auto Scaling을 통한 **사용량 기반 비용 30~70% 절감**, Region/AZ 다중화를 통한 **가용성 99.99%(Four Nines) 확보**, MTTR 평균 **60% 단축**, 배포 주기 **D+1 -> Hourly/Minute-level**로 단축 가능하다.
> 3. **판단 포인트**: **트레이드오프 핵심은 CAP(일관성·가용성·분할내성)와 동기·비동기 처리, Stateful vs Stateless, Strong vs Eventual Consistency, Shared-Nothing vs Shared-Disk 아키텍처** 선택이며, 워크로드 특성(OLTP/OLAP/Batch/Streaming)에 따라 Storage·Compute·Network·Identity 4계층의 결합 방식을 결정한다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 단순한 "서버 대여"가 아니다. NIST SP 800-145가 정의한 5대 특성(**온디맨드 셀프서비스, 광대역 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스**)을 구현하기 위해, **가상화(KVM/Hyper-V), 컨테이너(Docker/Containerd), 오케스트레이션(Kubernetes/ECS), IaC(Terraform/CloudFormation/ARM), GitOps(ArgoCD/Flux), Service Mesh(Istio/Linkerd)**가 유기적으로 결합된 분산 시스템 설계 체계다.

기존 온프레미스 환경은 **수직 확장(Scale-Up)**, **모놀리식 아키텍처**, **장기 납품 주기(Waterfall)**, **CapEx 중심 투자**로 인해 트래픽 급증 시 인프라 병목, 이기종 DB Lock-in, DR 사이트 미비, 운영 인력 부족 문제를 야기했다. 2020년 이후 **COVID-19 디지털 전환 가속**, **MSA(Microservices Architecture) 보편화**, **Kubernetes의 CNCF 표준화**, **AI/ML 워크로드의 GPU 수요 폭증**으로 인해, **클라우드 네이티브(Cloud-Native)** 패러다임이 엔터프라이즈 IT의 디폴트가 되었다.

```text
[전통 아키텍처 vs 클라우드 네이티브 아키텍처 진화 흐름]

  +----------------------+                  +----------------------+
  |   2000s Monolithic   |                  |   2024 Cloud-Native  |
  |  +----------------+  |                  |   +--------------+   |
  |  |   Web / WAS   |  |                  |   |  API Gateway |   |
  |  |   (단일 JVM)   |  |                  |   +------+-------+   |
  |  |                |  |                  |   +------+-------+   |
  |  |   Oracle DB   |  |                  |   | Service Mesh |   |
  |  |   (RDBMS)     |  |                  |   +------+-------+   |
  |  +----------------+  |                  |  +---+---+---+---+  |
  |   물리 서버 1~3대    |                  |  | MSA  | MSA  |  |
  |   수직 확장만 가능   |                  |  | Pod  | Pod  |  |
  |   장애 = 전면 중단   |                  |  +--+---+---+---+  |
  +----------------------+                  |     |       |      |
                                            |  +--+--+ +--+--+   |
                                            |  |K8s  | |K8s  |   |
                                            |  +-----+ +-----+   |
                                            | Region Multi-AZ    |
                                            +----------------------+
   - HW 구매 3~6개월                    - Provisioning 5분
   - CAPEX 1억원+                       - Pay-per-Use 종량제
   - 가용성 99.5%                       - 가용성 99.99%
   - 배포: 월 1회                       - 배포: 1일 수십 회
```

**기술사 출제 관점**: 단순히 "클라우드를 써라"가 아니라, **"왜 이 워크로드에 이 아키텍처 패턴을 선택했는가?"의 트레이드오프 정당화 능력**이 핵심이다. 예를 들어, 결제 시스템은 Strong Consistency(2PC/Saga), 게임 세션은 AP 중심(EVENTUAL/Dynamo-style), IoT 데이터 수집은 Lambda/Kappa 아키텍처로 분리 설계해야 한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기를 직접 발전기 돌려 쓰던 시절에서, 한국전력 그리드에 연결해 콘센트만 꽂는 시대"**로의 전환이다. 발전기(물리 서버) 운영 노하우가 사라진 대신, 전력 품질(가용성), 요금제(비용 모델), 부하 분산(Smart Grid) 설계 능력이 새로운 핵심 역량이 되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **4계층(컴퓨트·스토리지·네트워크·아이덴티티) + 1패브릭(관측·자동화·보안)**으로 분해할 수 있다. 각 계층은 독립적으로 Auto-Scaling, Multi-AZ Replication, Encryption을 지원하며, CSP(Cloud Service Provider) API를 통해 선언적으로 통합 관리된다.

```text
[클라우드 아키텍처 4계층 + 1패브릭 상세 구성도]

   +-------------------------------------------------------------+
   |                  Well-Architected Framework                  |
   |  Security | Reliability | Perf.Eff. | Cost Opt. | Ops | Sust.|
   +-------------------------------------------------------------+
                                  ^
   +------------------------------+-------------------------------+
   |  F. Observability & Governance Fabric                         |
   |  +------------+  +------------+  +------------+              |
   |  | Prometheus |  | OpenTelemetry|  | CloudTrail |              |
   |  | Grafana    |  |   (OTLP)    |  |  Audit     |              |
   |  +------------+  +------------+  +------------+              |
   |  + IaC(Terraform/CDK) + GitOps(ArgoCD) + Policy(OPA/Kyverno)|
   +--------------------------------------------------------------+
   +--------------+  +--------------+  +--------------+  +--------------+
   | 1. Identity  |  | 2. Compute   |  | 3. Storage   |  | 4. Network   |
   | +----------+ |  | +----------+ |  | +----------+ |  | +----------+ |
   | | IAM/IRSA | |  | | EC2/EKS  | |  | | S3/Blob  | |  | | VPC/VNet | |
   | | RBAC/ABAC| |  | | Lambda   | |  | | EBS/Disk | |  | | TGW/CCN  | |
   | | SSO/MFA  | |  | | Fargate  | |  | | EFS/FSx  | |  | | DX/ER    | |
   | | KMS/HSM  | |  | | GPU/ARM  | |  | | DynamoDB | |  | | CDN/Edge | |
   | +----------+ |  | +----------+ |  | +----------+ |  | +----------+ |
   +--------------+  +--------------+  +--------------+  +--------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Compute 계층** | 워크로드 실행 | **EC2/VM**(가상머신, KVM/Xen/Hyper-V), **ECS/EKS/AKS/GKE**(관리형 K8s, Control Plane 관리형), **Fargate/Cloud Run**(서버리스 컨테이너, 노드 관리 불요), **Lambda/Cloud Functions**(이벤트 기반 FaaS, Cold Start 100~800ms, Provisioned Concurrency로 해결), **Spot/Preemptible**(미사용 자원 경매, 60~90% 저렴, 2분 사전 종료 통보) |
| **Storage 계층** | 데이터 영속성 | **Object**(S3/Blob/GCS, 11 9s 내구성, 99.99% 가용성, Lifecycle 정책으로 Glacier로 자동 이관), **Block**(EBS/PD, IOPS 256K, NVMe 기반), **File**(EFS/FSx, NFS/SMB, 다중 AZ 공유), **NoSQL**(DynamoDB/CosmosDB, Single-digit millisecond, Global Tables로 Multi-Region Replication), **Data Warehouse**(Redshift/BigQuery/Snowflake, Columnar, MPP) |
| **Network 계층** | 트래픽 라우팅 | **VPC/VNet**(10.0.0.0/8 CIDR, Public/Private/DB Subnet 3-Tier), **TGW/Cloud Router**(리전 간 피어링, Transit Hub), **DX/ExpressRoute**(전용선, 1~100Gbps, BGP), **ALB/NLB**(L7/L4 Load Balancer, WAF 통합), **CloudFront/Cloud CDN**(엣지 캐싱, TTL 기반, Lambda@Edge로 코드 실행) |
| **Identity 계층** | 인증·인가 | **IAM**(Policy JSON, Allow/Deny 평가, SCP로 계정 단위 Guardrail), **Cognito/Auth0**(OIDC/SAML 2.0, JWT Token), **KMS/HSM**(Envelope Encryption, FIPS 140-2 L3 HSM), **Secrets Manager**(자동 Rotation, RDS 통합) |
| **Observability Fabric** | 가시성·자동화 | **CloudWatch/Stackdriver/Cloud Monitoring**(Metrics/Logs/Traces 3-Pillar), **Prometheus + Grafana**(CNCF 표준, PromQL), **Jaeger/Tempo**(Distributed Tracing, W3C TraceContext), **X-Ray/OpenTelemetry**(계측 표준), **CloudTrail/Config**(API Audit, Compliance) |

### 핵심 원리 심화

**1. 가용성(Availability) 공식과 AZ 배치**
- 가용성 = 1 - Σ(상호 의존 장애 확률의 곱)
- 단일 AZ 가용성 99.95% × Multi-AZ 2개 = 1 - (0.0005 × 0.0005) = **99.999975%**
- **N+1, N+2 이중화 원칙**: 트래픽의 N배까지 흡수 가능하도록 예비 용량 설계

**2. 일관성 모델(Consistency Model)**
- **Strong Consistency**: 쓰기 직후 모든 읽기에서 최신값 보장 (RDBMS, Spanner)
- **Eventual Consistency**: 수 ms~수 s 후 수렴 (DynamoDB 기본, S3)
- **Read-your-writes**: 본인이 쓴 데이터는 즉시 읽기 가능 (Cassandra R=ONE, W=QUORUM)
- **Vector Clock / LWW(Last-Write-Wins)**: 충돌 해결 알고리즘

**3. Auto Scaling 알고리즘**
- **Reactive(반응형)**: CPU/Memory 임계치 기반 (HPA, 기본 30초 주기)
- **Predictive(예측형)**: ML 기반 시계열 예측 (AWS Predictive Scaling, 2주 학습)
- **Scheduled(예약형)**: cron 기반 사전 확장 (배치/캠페인 트래픽)
- **Target Tracking**: ASG TargetValue=70.0, **Step Scaling**: 임계치별 단계 조정

**4. CAP 정리 실전 적용**
| 시스템 | C / A / P 선택 | 적용 사례 |
| :--- | :--- | :--- |
| RDBMS(MySQL, Aurora) | **CP** | 금융 결제, 재고 |
| Cassandra, DynamoDB | **AP** | 카탈로그, 세션 |
| HBase, MongoDB(기본) | **CP** | 사용자 프로필 |
| ZooKeeper, etcd | **CP** | K8s Control Plane |

- **📢 섹션 요약 비유**: 4계층 아키텍처는 **"아파트 단지의 4종 설비"**와 같다. 전기(Compute), 수도(Storage), 도로(Network), 출입통제(Identity) 각각이 독립 인프라로 동작하면서, 관제실(Observability Fabric)이 한 곳에서 통합 모니터링하는 구조다. 한 설비가 고장나도 다른 설비는 독립적으로 동작해야 한다(장애 격리).

---

## Ⅲ. 비교 및 연결

### 서비스 모델 비교 (IaaS / PaaS / SaaS / FaaS / CaaS)

| 구분 | **IaaS** (EC2, Compute Engine) | **PaaS** (RDS, Elastic Beanstalk) | **SaaS** (Office 365, Salesforce) | **FaaS** (Lambda, Cloud Functions) | **CaaS** (EKS, Cloud Run) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | App + Data + Runtime + OS + Middleware | App + Data | 모두 CSP | Function 코드만 | Container Image |
| **유연성** | ★★★★★ | ★★★ | ★ | ★★ | ★★★★ |
| **운영 부담** | ★★★★★ | ★★★ | ★ | ★ | ★★ |
| **Cold Start** | 없음 | 없음 | 없음 | 100~800ms | 컨테이너 1~10s |
| **적합 워크로드** | 레거시 마이그레이션, 커스텀 OS | 웹앱 표준 배포 | 정형 업무 (메일, CRM) | 이벤트 처리, API Gateway 후단 | MSA, CI/CD 표준 |
| **과금 단위** | 시간/초 | 인스턴스 시간 | 사용자/월 | 호출 수 + GB-초 | vCPU·Memory·초 |
| **Lock-in 정도** | 낮음 (이미지 기반) | 중간 (DB 엔진 종속) | 높음 (API 종속) | 높음 (벤더 종속) | 낮음 (OCI/K8s 표준) |

### 배포 모델 비교

| 구분 | **Public Cloud** | **Private Cloud** | **Hybrid Cloud** | **Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | AWS/Azure/GCP | 자체 DC + OpenStack | Public + Private | 2개 이상 Public |
| **규제 준수** | 글로벌 표준, 데이터 주권 이슈 | 온프레미스 데이터 통제 | 데이터 계층 분리 가능 | 벤더 종속 회피 |
| **확장성** | 무한 (실질
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 658 / 800

<- **이전**: [657. 클라우드 아키텍처 핵심 토픽 657번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/657_cloud_architecture_core_topic_657_exam_summar/)
**다음**: [659. 클라우드 아키텍처 핵심 토픽 659번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/659_cloud_architecture_core_topic_659_exam_summar/) ->

---
