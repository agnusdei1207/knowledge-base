---
title: "Cloud Architecture Core Topic 665 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드·멀티클라우드 환경에서 IaaS/PaaS/SaaS/FaaS 추상화 계층과 컨트롤 플레인–데이터 플레인 분리, 셀프서비스 API 기반의 **프로비저닝 자동화 및 탄력적 확장(Elasticity)** 구조가 클라우드 아키텍처의 본질이며, CNCF가 정의한 12-Factor App, Well-Architected Framework(WAFF) 5대 축(운영 우수성·보안·안정성·성능 효율·비용 최적화)이 평가 기준의 척도다.
> 2. **가치**: Auto Scaling Group + Spot/On-Demand 혼합 + Reserved Instance(또는 Savings Plans) 활용 시 **TCO 30~60% 절감**, MTTR은 Immutable Infrastructure + IaC(Terraform/CloudFormation) 적용 시 평균 **65% 단축**, 멀티 AZ·리전 분산으로 가용성 **99.95% -> 99.99%(Four-Nines) 상향**이 가능하다.
> 3. **판단 포인트**: **가용성–일관성–분할내성(CAP Theorem)** 트레이드오프, VM vs Container vs Serverless(FaaS)의 콜드 스타트·상태 관리·비용 모델 차이, Egress Lock-in·API 종속성(Vendor Lock-in)·Shared Responsibility 경계, 그리고 Control Plane의 단일 장애점(SPOF) 회피 설계가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 3-Tier 아키텍처는 **수직 확장(Scale-Up)** 중심의 CAPEX(자본 지출) 모델로, 트래픽 예측 실패 시 **과잉 프로비저닝(Over-Provisioning) 200~400%** 또는 서비스 장애가 빈번했다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 **API 기반 셀프서비스 프로비저닝, 사용량 기반 과금(Pay-as-you-go), 무한 확장성(Elasticity)**을 통해 IT 인프라의 **유틸리티화(Utility Computing)**를 실현했다.

핵심 패러다임 전환은 다음 4가지다:
- **CapEx -> OpEx**: 선불 인프라 구매 -> 종량제 과금
- **수직확장 -> 수평확장(Scale-Out)**: 32코어 1대 -> 2코어 100대
- **수동 운영 -> IaC(Infrastructure as Code)**: 클릭·콘솔 -> Terraform HCL/CloudFormation YAML 선언형 코드
- **Mutable(변경 가능) -> Immutable(불변) 인프라**: 패치·업데이트 -> AMI/컨테이너 이미지 재기반 배포

NIST SP 800-145는 클라우드를 **5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)**과 **3대 서비스 모델(IaaS/PaaS/SaaS)**, **4배치 모델(Public/Private/Hybrid/Community)**로 정의하며, 이 분류 체계가 현재까지 클라우드 아키텍처 평가의 표준 프레임이다.

```text
+------------------------------------------------------------------+
|                클라우드 컴퓨팅 패러다임 전환 흐름도                 |
+------------------------------------------------------------------+
|                                                                  |
|  [전통적 온프레미스]                  [클라우드 네이티브]            |
|                                                                  |
|  +----------+                      +------------------+          |
|  |Server    |  ---- 전환 ---->     |VM/Container/     |          |
|  |Rack/Mount|     자동화·추상화     |Function (탄력)    |          |
|  +----------+                      +------------------+          |
|                                                                  |
|  CAPEX (선불)                    -->  OPEX (종량제)              |
|  Scale-Up (수직)                 -->  Scale-Out (수평)            |
|  수동/스크립트 (Mutable)          -->  IaC + GitOps (Immutable)  |
|  단일 장애점                     -->  Multi-AZ/Region 이중화      |
|  MTTR 평균 4~8시간               -->  MTTR < 30분 (자동복구)      |
|                                                                  |
|  +--------------------------------------------------------+      |
|  |    NIST 5대 특성  |  AWS/Azure/GCP 공통 구현 메커니즘     |      |
|  |    Self-Service   |  REST API + SDK + CLI                |      |
|  |    Elasticity     |  Auto Scaling Group + HPA            |      |
|  |    Pooling        |  Region/AZ/Edge Location 계층        |      |
|  |    Measured       |  CloudWatch/Azure Monitor + Billing   |      |
|  |    Network Access  |  VPC/VNet + CDN + Direct Connect    |      |
|  +--------------------------------------------------------+      |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 온프레미스는 "집을 사서 관리하는 것"이고, 클라우드는 "전기·수도처럼 필요할 때만 꺼내 쓰는 요금제"이며, IaaS는 빈 방(VM)을 빌려 가구(OS/미들웨어)를 스스로 배치, PaaS는 가구 배치까지 된 방, SaaS는 호텔에 짐 풀고 머무는 것에 비유할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **제어 평면(Control Plane)**과 **데이터 평면(Data Plane)**의 분리다. 제어 평면은 API Gateway·IAM·오케스트레이터(Kubernetes Control Plane)·상태 관리(etcd)로 구성되며 정책·구성을 담당하고, 데이터 평면은 실제 트래픽을 처리하는 컴퓨트·스토리지·네트워크 워커 노드로 구성된다.

```text
+---------------------------------------------------------------------+
|            클라우드 네이티브 참조 아키텍처 (CNCF Landscape)          |
+---------------------------------------------------------------------+
|                                                                     |
|  +------------------------------------------------------------+    |
|  |  Layer 5: Application Definition & Development              |    |
|  |  +------+ +------+ +------+ +------+ +------+ +------+  |    |
|  |  |Helm | |Operator| |Skaffold| |Buildpacks| |Backstage| |    |
|  |  +------+ +------+ +------+ +------+ +------+ +------+  |    |
|  +------------------------------------------------------------+    |
|  +------------------------------------------------------------+    |
|  |  Layer 4: Orchestration & Management  (Kubernetes, K3s)    |    |
|  |   +----------+    +----------+    +------------------+    |    |
|  |   |API Server|◄--►|  etcd    |    |Scheduler+Controller|    |    |
|  |   +----------+    +----------+    +------------------+    |    |
|  +------------------------------------------------------------+    |
|  +------------------------------------------------------------+    |
|  |  Layer 3: Runtime & Provisioning  (containerd, CRI-O)     |    |
|  +------------------------------------------------------------+    |
|  +------------------------------------------------------------+    |
|  |  Layer 2: Compute / Storage / Networking (VPC, EBS, S3)   |    |
|  +------------------------------------------------------------+    |
|  +------------------------------------------------------------+    |
|  |  Layer 1: Provisioning / IaC (Terraform, Pulumi, CFN)     |    |
|  +------------------------------------------------------------+    |
|                                                                     |
|  --- Data Plane ------------|------------ Control Plane -----      |
|  Pod/Node 워커 (트래픽 처리)  |  API/etcd/Scheduler (정책 결정)      |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane** | 정책·구성·상태 관리 | Kubernetes API Server(6443/TCP), etcd(Raft 합의 알고리즘, write 약 10ms), AWS Control Tower, Azure Arc 기반 멀티 계정 거버넌스 |
| **Data Plane** | 실제 트래픽·워크로드 처리 | kubelet + containerd, AWS Nitro Enclave(격리 하드웨어), EKS Fargate(서버리스 K8s 데이터 평면) |
| **Service Mesh** | L7 트래픽 관리·mTLS·관측 | Istio/Linkerd/Consul — Envoy 사이드카 패턴, mTLS 1.3, gRPC 기반 xDS 프로토콜로 설정 동기화 |
| **IaC Layer** | 인프라 선언적 프로비저닝 | Terraform 1.5+(State Locking via DynamoDB), AWS CDK(TypeScript/Python 추상화), Pulumi — Plan->Apply 2단계 검증 |
| **Serverless/FaaS** | 이벤트 기반 stateless 실행 | AWS Lambda(10GB 메모리, 15분 타임아웃), Azure Functions(4분 default), GCP Cloud Run(Cold Start < 1s) — Firecracker microVM 기반 샌드박스 |
| **Storage Tiering** | 데이터 특성별 계층화 | Hot(S3 Standard, 3 AZ 복제) / IA(Glacier IR, ms 단위 검색) / Cold(Glacier Deep Archive, 12시간 복원) — 라이프사이클 정책으로 자동 이동 |
| **Observability Stack** | 메트릭·로그·트레이스 통합 | OpenTelemetry(OTLP) -> Prometheus + Grafana + Loki + Tempo (3-파넛) 또는 Datadog/New Relic SaaS |

**탄력성(Elasticity) 알고리즘 핵심 파라미터:**
- **HPA(Horizontal Pod Autoscaler)**: `target = avg_cpu_utilization=70%` 또는 `avg_value="http_requests:1000"` 기준, `scaleDown stabilizationWindowSeconds=300` (5분) — **Karpenter**가 등장하면서 노드 프로비저닝까지 90초 -> 15초로 단축됨
- **Predictive Scaling**: AWS Auto Scaling의 예측 정책은 과거 14일 트래픽을 Prophet/ARIMA 계열 알고리즘으로 분석하여 사전 확장
- **서버리스 Concurrency**: Lambda Reserved Concurrency = 100으로 설정 시 그 수치만큼 콜드 컨테이너가 사전 워밍, Provisioned Concurrency로 영구 유지 가능

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"지휘자(Control Plane)와 오케스트라(Data Plane)의 분리"** 와 같다. 지휘자는 음표(상태)를 보고만 있고, 무대 위 연주자(워커)만 실제 소리를 내며, Kubernetes는 오케스트라의 지휘자, Service Mesh는 각 섹션의 단장, Auto Scaling은 수요에 따른 보조 연주자 자동 투입에 비유된다.

---

## Ⅲ. 비교 및 연결

### 1) 서비스 모델 비교 (IaaS / PaaS / SaaS / FaaS)

| 구분 | **IaaS** (EC2, Compute Engine) | **PaaS** (Elastic Beanstalk, App Engine) | **SaaS** (Office 365, Salesforce) | **FaaS** (Lambda, Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS·미들웨어·런타임 모두 사용자 | 앱 코드만, 런타임은 CSP | 소프트웨어 전체 사용 | 함수 코드만 |
| **확장 단위** | VM 인스턴스 | 컨테이너/앱 단위 | 사용자 라이선스 | 동시 실행(Concurrency) |
| **콜드 스타트** | 없음 (이미 가동) | 없음~수 초 | 없음 | 100ms ~ 5s |
| **상태 관리** | Stateful 가능 | Stateless 권장 | 무관 | 반드시 Stateless, 외부 저장소 |
| **최적 워크로드** | 레거시 마이그레이션, 커스텀 네트워크 | 마이크로서비스, API 백엔드 | 일반 업무·CRM·협업 | 이벤트 처리, 배치, IoT, Webhook |
| **과금 모델** | 시간당 (per-second) | 인스턴스 시간 | 사용자/월 | 호출 수 × 실행 시간(ms) GB-초 |

### 2) 배포 모델 비교

| 구분 | **Public Cloud** | **Private Cloud** | **Hybrid Cloud** | **Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | CSP (AWS, Azure, GCP) | 자체/전용 (OpenStack, VMware on AWS Outposts) | 온프레미스 + 퍼블릭 연결 | 2개 이상 퍼블릭 (AWS+Azure) |
| **연결 기술** | Internet, Direct Connect | 전용선/SDN | AWS Transit Gateway, Azure Arc, GCP Anthos | Terraform, Crossplane, CAST.AI |
| **데이터 주권** | 해외 리전 이슈 (한국 ISMS-P) | 국내 통제 가능 | 워크로드별 분기 | CSP별 컴플라이언스 별도 |
| **Lock-in 위험** | 높음 | 낮음 | 중간 | 낮음 (추상화) |
| **Bursting** | 불가 | 불가 (용량 한계) | 가능 (Cloud Bursting) | 가능 (CSP 간 Failover) |
| **적합 케이스** | 빠른 개발, 글로벌 서비스 | 규제/금융/공공 | 단계적 마이그레이션 | 벤더 회피, 최적 가격 |

### 3) 통합·연계 핵심

- **하이브리드 연결**: **AWS Direct Connect(1~100Gbps 전용선)**, Azure ExpressRoute, GCP Interconnect + SD-WAN(Cisco Viptela, Cato) 조합으로 일관 latency 보장
- **멀티클라우드 추상화**: Kubernetes(K8s) + **Anthos / EKS Anywhere / AKS Arc**로 워크로드 이식성 확보, **Crossplane/Cluster API**로 클러스터 자체를 IaC로 관리
- **보안 통합**: **HashiCorp Vault** (시크릿), **SPIFFE/SPIRE** (워크로드 ID), **OPA/Gatekeeper** (정책 as Code) — 클라우드·온프레 환경 동시 적용
- **데이터 사일로 해체**: **Apache Kafka / Amazon MSK / Confluent Cloud**로 멀티 클라우드·하이브리드 이벤트 스트림 단일화

- **📢 섹션 요약 비유**: **서비스 모델은 피자 만드는 단계의 차이**다. IaaS는 밀가루·치즈·오븐을 받아 직접 굽기, PaaS는 도우만 올려 굽기, SaaS는 피자 배달, FaaS는 조각 주문 시 그때 피자 한 조각만 데워 배달. **배포 모델은 점포의 형태**로, Public은 프랜차이즈 임대, Private는 본사 직영, Hybrid는 본사+프랜차이즈, Multi-Cloud는 둘 이상의 프랜차이즈 동시 운영에 비유된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **서비스 모델 선정**: 워크로드가 ① **콜드 스타트 허용 가능?** (FaaS 가능) ② **OS/미들웨어 커스터마이징 필수?** (IaaS 필요) ③ **데이터 거버넌스·규제 요건?** (Private/Hybrid + Sovereign Cloud 검토) — KR에서 공공·금융은 CSAP 인증 클라우드 우선 (NIPA 클라우드 서비스 보안인증)
2. **가용성 SLA 계산**: 99.9%(Three-Nines) = 월 43.83분, 99.95% = 21.9분, 99.99% = 4.38분 — **단일 AZ는 99.9%**, **Multi-AZ는 99.95%**, **Multi-Region Active-Active는 99.99%** 가능. 요구 SLA 달성에 필요한 AZ/Region 토폴로지 명시
3. **RTO/RPO 정의 후 DR 전략 매핑**: Backup/Restore(수 시간), Pilot Light(수십 분), Warm Standby(수 분), **Multi-Site Active-Active
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 665 / 800

<- **이전**: [664. 클라우드 아키텍처 핵심 토픽 664번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/664_cloud_architecture_core_topic_664_exam_summar/)
**다음**: [666. 클라우드 아키텍처 핵심 토픽 666번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/666_cloud_architecture_core_topic_666_exam_summar/) ->

---
