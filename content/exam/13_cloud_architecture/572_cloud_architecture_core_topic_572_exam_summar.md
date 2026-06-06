---
title: "Cloud Architecture Core Topic 572 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST의 IaaS/PaaS/SaaS/FaaS 서비스 모델과 Public/Hybrid/Multi/Private 배포 모델을 기반으로, 컨테이너 오케스트레이션(Kubernetes), IaC(Terraform/Pulumi), 서비스 메시(Istio/Linkerd), 옵저버빌리티(OpenTelemetry)为核心的 4대 축을 결합해弹性·자동화·비용 최적화를 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: 온프레미스 대비 CAPEX->OPEX 전환으로 초기 인프라 투자 70~90% 절감, 오토스케일링을 통한 트래픽 변동 대응력 10~100배 향상, MTTR(평균 복구 시간)을 Well-Architected Framework 적용 시 60% 단축, 글로벌 멀티리전 배포로 사용자 RTT 50~200ms 개선 효과가 검증되어 있다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티클라우드, Stateless 컨테이너 vs Stateful 워크로드, 중앙 집중 EKS/AKS/GKE vs 분산 셀 아키텍처, 동기식 Strong Consistency vs 비동기식 Eventually Consistent의 CAP 트레이드오프, 그리고 FinOps 기반 Reserved/On-Demand/Spot 인스턴스 조합 비율(전형적 60/30/10)이 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 더 이상 "데이터센터를 외부에 둔다"는 단순한 의미가 아니다. 2026년 현재의 클라우드 아키텍처는 **Infrastructure as Code(IaC) 기반의 선언적 프로비저닝 -> GitOps 기반 지속적 배포 -> 셀프힐링 오케스트레이션 -> AIOps 기반 자동 스케일링**으로 이어지는 *자율운영(Self-Operating)* 체계다. 한국 클라우드 시장 규모는 2024년 기준 약 12조 원으로, 금융권의 Digital Bank 트래픽은 평시 대비 1,000배까지 폭증하는 블랙프라이데이급 이벤트가 일상화되면서 기존 모놀리식 아키텍처로는 SLA 99.99% 보증이 불가능해졌다.

핵심 과제는 세 가지다. 첫째, **탄력성(Elasticity)**: 1분 단위 Auto Scaling으로 리소스를 동적 할당하여 Peak 대비 Idle 비용을 0에 수렴시켜야 한다. 둘째, **불변 인프라(Immutable Infrastructure)**: Cattle vs Pet 패러다임 전환으로 인스턴스를 수리하지 않고 교체(Phoenix Server)하여 Configuration Drift를 원천 차단한다. 셋째, **관측 가능성(Observability)**: 로그·메트릭·트레이스의 3-Pillar 통합 분석을 통해 분산 시스템의 장애를 5분 이내에 근본 원인까지 추적해야 한다.

```text
[전통 모놀리식 vs 클라우드 네이티브 아키텍처 진화]

  +------------------+         +------------------------------+
  |   Monolithic Era |   --->   |     Cloud-Native Era         |
  |  (1990s-2010s)   |         |        (2015~현재)            |
  +------------------+         +------------------------------+
  +--------------+             +--------------+  +--------------+
  |  1대의 거대한|             |  수백~수만 개 |  |   Serverless |
  |   WAS + DB  |             |  마이크로서비스|  |  Function    |
  |  (Pet Server)|             |  (Cattle)    |  |  (Lambda)    |
  +--------------+             +--------------+  +--------------+
        |                            |                |
        v                            v                v
  수동 배포/장애복구              GitOps/CI-CD        Event-Driven
  Scale-up만 가능                HPA/VPA/Cluster   사용량 기반 과금
  월 단위 Capacity Plan          Auto-Scale          Auto-Scale to 0
  HA = Active-Standby            Multi-AZ Active-    0->N Auto-Active
  라이선스 종속(Lock-in)         Active              Open 표준 기반
```

- **📢 섹션 요약 비유**: 전통 아키텍처가 "한 대의 거대한 수족관에 모든 물고기를 키우는 것"이라면, 클라우드 아키텍처는 "IoT 센서로 수질을 실시간 모니터링하며 자동으로 먹이와 산소를 공급하는 스마트 양식장"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 5계층 참조 모델(Well-Architected Framework)을 기준으로 핵심 구성 요소를 분해한다. AWS Well-Architected 6 Pillars(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)와 Azure/AWS/GCP의 공통 베이스라인을 통합한 결과, 현대 클라우드 아키텍처는 **인프라 계층 -> 데이터 계층 -> 애플리케이션 계층 -> 오케스트레이션 계층 -> 거버넌스 계층**의 5-tier 모델로 추상화된다.

```text
[클라우드 아키텍처 5계층 참조 모델]

   +-----------------------------------------------------+
   |  5. 거버넌스 계층 (Governance)                       |
   |  - Cloud Center of Excellence (CCoE)                |
   |  - FinOps, Policy as Code (OPA/Sentinel)            |
   |  - CSPM(CWPP/CIEM) : Wiz, PrismaCloud, Lacework     |
   +-----------------------------------------------------+
   |  4. 옵저버빌리티 계층 (Observability)                |
   |  - Logs(Loki/CloudWatch) Metrics(Prom/CloudWatch)  |
   |  - Traces(Jaeger/Tempo/X-Ray) - OpenTelemetry 표준 |
   |  - AIOps: Coralogix/Datadog/New Relic               |
   +-----------------------------------------------------+
   |  3. 오케스트레이션 계층 (Orchestration)              |
   |  - K8s Controller Loop(관찰->비교->조정)              |
   |  - Service Mesh: Istio(Envoy Sidecar) mTLS/L7라우팅|
   |  - API Gateway: Kong/Apigee/ALB+Kong KIC           |
   +-----------------------------------------------------+
   |  2. 플랫폼/데이터 계층 (Platform & Data)             |
   |  - 컨테이너 런타임: containerd, CRI-O, runC        |
   |  - DB: OLTP(Aurora/Cloud SQL/CockroachDB)          |
   |  - OLAP(BigQuery/Snowflake/Redshift)                |
   |  - Cache: Redis 7.x Cluster Mode(샤딩 16384 슬롯)  |
   +-----------------------------------------------------+
   |  1. 인프라 계층 (Infrastructure)                     |
   |  - Compute: EC2/GCE/Azure VM + BareMetal            |
  |  - Network: VPC/Subnet(Public/Private/DB 분리)      |
   |  - Storage: Block(EBS)/Object(S3)/File(EFS)        |
   |  - IaC: Terraform/Pulumi/CloudFormation/CDK        |
   +-----------------------------------------------------+
                              ^
                              | AWS/Azure/GCP API, Crossplane
                              |
              +---------------+---------------+
              |  Multi-Cloud / Hybrid Edge    |
              |  (Anthos, ARO, AWS Outposts)  |
              +-------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IaC 엔진 (Terraform/Pulumi/CDK)** | 인프라의 선언적 정의 및 프로비저닝 자동화 | HCL 또는 TypeScript로 `.tf` 작성 -> `terraform plan`(Diff 확인) -> `terraform apply`(State Lock: DynamoDB/Consul로 동시성 제어) -> State File을 S3+GCS에 버전 관리, Drift Detection(30분 주기 reconcile)으로 실제 인프라와 코드 일치 보장 |
| **Kubernetes Control Plane** | 컨테이너화된 워크로드의 선언적 배포/스케일링/자가 치유 | `etcd`(RAFT 합의 알고리즘) + `kube-apiserver` + `scheduler`(Bin-packing/스프레드 토폴로지) + `controller-manager`(ReplicaSet/Deployment/StatefulSet) + `cloud-controller-manager`(AWS/GCP 통합) 구성, 5초 주기 Reconcile Loop로 Desired State 유지 |
| **Service Mesh (Istio/Linkerd)** | L7 트래픽 관리, mTLS 기반 Zero-Trust 보안, 관측성 | Envoy Sidecar가 Pod 내 모든 트래픽을 Interception(iptables/pf) -> mTLS 1.3 자동 적용 -> xDS API로 Control Plane에서 동적 라우팅/Retry/Circuit Breaker 주입, Ambient Mesh(2024~)로 Sidecar 제거 가능 |
| **오브젝트 스토리지 (S3/GCS/Blob)** | 11 nines(99.999999999%) 내구성으로 페타바급 데이터 저장 | Erasure Coding(Reed-Solomon, 4+2 또는 6+3 패리티), Multi-AZ/Region 자동 복제, 버전 관리 + Object Lock(WORM) + Lifecycle Policy(IA/Glacier 자동 계층화) |
| **API Gateway (Kong/Apigee/Envoy Gateway)** | 외부 트래픽 진입점, 인증/인가/속도 제한/변환 | OAuth 2.0/OIDC JWT 검증, Rate Limiting(Token Bucket 알고리즘, Redis 백엔드), Circuit Breaker(50% 실패율 시 30초 Open), GraphQL/REST/WebSocket 프로토콜 변환, Plugin SDK로 Lua/Go 확장 |

**핵심 알고리즘 및 파라미터**:

- **K8s HPA(Horizontal Pod Autoscaler)**: 메트릭 수집 주기 15초, `targetAverageUtilization=70%` 기준, 안정화 윈도우(`--horizontal-pod-autoscaler-downscale-stabilization`) 기본 5분으로 Flapping 방지. 예측 스케일링(KEDA + K8s-based Event-driven Autoscaling)은 Cron 메트릭으로 트래픽 30분 전 사전 증설.
- **Consistent Hashing in Redis Cluster**: 키 공간을 16,384개 슬롯으로 분할 -> `CRC16(key) mod 16384` -> 3 Master × 3 Replica 구성, 노드 추가 시 재배치 비율 1/N(전체 키의 약 1/N만 이동).
- **CAP Theorem in Cloud DB**: DynamoDB/Cassandra는 AP(가용성 + 파티션 허용, Eventually Consistent, 1초 내 정합), Google Spanner/CockroachDB는 CP+순간 일관성(트루타임 API + 2PC), RDBMS Aurora Global은 동기식 Secondary로 Strong Consistency.
- **SR-IOV/DPDK 네트워킹**: VM에서 물리 NIC를 직접 바이패스하여 25Gbps 라인레이트 달성, 컨테이너에서는 Cilium eBPF가 커널 우회로 Pod-to-Pod 지연을 0.1ms 이하로 단축.

- **📢 섹션 요약 비유**: IaC가 "건축 설계 도면"이라면, K8s는 "자동으로 건축 자재를 배치하는 로봇", Service Mesh는 "건물 내 모든 통로의 보안·방화·환기 시스템", 옵저버빌리티는 "CCTV·온도·전력 센서 통합 관제실"이다.

---

## Ⅲ. 비교 및 연결

### A. 서비스 모델(IaaS/PaaS/SaaS/FaaS) 비교

| 구분 | IaaS (EC2/Azure VM) | PaaS (Beanstalk/App Engine) | SaaS (Salesforce/Office 365) | FaaS (Lambda/Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 책임 범위** | OS~미들웨어 직접 관리 | 런타임·OS 자동, 코드만 관리 | 완전 관리(설정·확장) | 함수 코드만 관리, 전부 자동 |
| **콜드 스타트 지연** | 1~3분(인스턴스 기동) | 30초~2분 | 즉시(브라우저) | 100ms~5초(예약 Concurrency로 0) |
| **최대 실행 시간** | 무제한 | 플랫폼별 60~120분 | 무제한 | 15분(AWS Lambda 최대) |
| **확장 단위** | 인스턴스(수직/수평) | 인스턴스/App 단위 | 사용자 단위 | 동시성(Concurrency, 1000 기본) |
| **과금 모델** | 시간/초 단위 | 인스턴스 + 요청 | 사용자 라이선스 | 호출 수(ms 단위) + GB-초 |
| **적합 워크로드** | 레거시 리프트앤시프트, GPU | API·웹 표준 워크로드 | CRM·메일·협업 | 이벤트 기반, 간헐적 작업, ETL |
| **TCO 우위** | 장기 부하 안정 | 중간 부하 변동 | 사용자 수 확정 | 극단적 변동(0->N) |

### B. 배포 모델(Public/Hybrid/Private/Multi/Community) 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | CSP(AWS/Azure/GCP) | 자체 데이터센터 | Public + Private 혼용 | 2개 이상 CSP |
| **컴플라이언스** | 글로벌 표준(Iso27001/SOC2) | 규제 산업 최적 | 데이터 주권 충족 | 벤더 종속 회피 |
| **네트워크 연결** | Internet/BGP | 전용선/SDN | Direct Connect/ExpressRoute + VPN IPSec | Transit Gateway + Interconnect |
| **대표 사례** | Netflix, Airbnb | 금융·공공(KEPCO NCP) | 뱅크샐러드, 토스 | Spotify(GCP+S3) |
| **도입 난이도** | ★☆☆ | ★★★ | ★★★★ | ★★★★★ |
| **Latency** | Region 내 1~10ms | On-Prem 0.5ms | Cross-Region 20~80ms | Cross-Cloud 30~100ms |

### C. 클라우드 아키텍처의 통합 연결

```text
[클라우드 생태계 통합 아키텍처 - Zone 분리]

  +---------------- Edge Zone (CDN/5G MEC) ----------------+
  |  Cloudflare Workers / AWS Wavelength / CloudFront     |
  |  Cache Hit Ratio 90%+, 사용자 RTT 10ms 이하            |
  +---------------------+----------------------------------+
                        | HTTPS/gRPC
                        v
  +---------------- Public Zone (DMZ) ---------------------+
  |  - WAF(AWS WAF 룰셋: SQL Injection, XSS)               |
  |  - DDoS Shield(AWS Shield Advanced 1Tbps 흡수)         |
  |  - API Gateway + Lambda@Edge                            |
  +---------------------+----------------------------------+
                        |
                        v
  +---------------- Private Zone (VPC 내부) ----------------+
  |  - EKS/AKS/GKE Worker Node (3+ AZ 분산)                |
  |  - RDS Aurora Multi-Master, ElastiCache Redis Cluster   |
  |  - Internal ALB + Istio Service Mesh                    |
  +---------------------+----------------------------------+
                        | VPC Peering / TGW
                        v
  +---------------- Data Zone (관리 격리) ------------------+
  |  - S3 Glacier Deep Archive(연 1회 접근)                 |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 572 / 800

<- **이전**: [571. 클라우드 아키텍처 핵심 토픽 571번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/571_cloud_architecture_core_topic_571_exam_summar/)
**다음**: [573. 클라우드 아키텍처 핵심 토픽 573번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/573_cloud_architecture_core_topic_573_exam_summar/) ->

---
