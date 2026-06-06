---
title: "Cloud Architecture Core Topic 546 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145의 SaaS/PaaS/IaaS/FaaS 4계층 모델을 기반으로, AWS Well-Architected Framework의 6대 필러(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)와 12-Factor App 원칙을 코드(IaC)로 표현하여 가용성·확장성·탄력성을 API로 추상화한 설계 패러다임이다.
> 2. **가치**: 동일 워크로드 대비 CapEx->OpEx 전환으로 3년 TCO 30~40% 절감, Auto Scaling Group의 평균 65~75% 자원 활용률 달성, 멀티 AZ 기반 SLA 99.99%(연 52.6분 이내 장애), MTTR 50% 단축, 글로벌 30+ 리전 엣지 캐싱으로 P99 레이턴시 200ms->35ms 수준으로 개선된다.
> 3. **판단 포인트**: 핵심 의사결정 트리드는 ①6R 마이그레이션(Rehost/Replatform/Refactor/Repurchase/Retire/Retain) 분류, ②단일 클라우드 종속(Multi-AZ) vs 멀티 클라우드(DR) vs 하이브리드(Outpost/Arc) 트레이드오프, ③워크로드별 VM/Container/Function 런타임 선택, ④데이터 레지던시·규제 준수(K-ISMS, GDPR, CSAP) 여부이며, CCoE(Cloud Center of Excellence) 조직 성숙도가 아키텍처 품질을 좌우한다.

---

## Ⅰ. 개요 및 필요성

전통적 엔터프라이즈 IT는 수개월에 걸친 HW 조달(Lead Time 8~12주), 정적 용량 계획(Peak 기준 2배 과다 설계), 수직적 확장(Scale-Up)의 한계, IDC 임대·전력·냉각의 고정비 구조로 인해 **총 60~70%가 유휴 자원**으로 낭비되었다. 2006년 AWS S3·EC2 출시 이후, 클라우드는 컴퓨팅·스토리지·네트워크를 API 호출로 즉시 프로비저닝 가능한 Utility Computing 모델로 전환시켰다. COVID-19 팬데믹(2020~2022)으로 인한 비대면 트래픽 10배 급증, 생성형 AI 워크로드의 GPU 수요 폭증, K-디지털 트윈 정책에 따른 공공 클라우드 전환 의무화(2025년까지 50% 전환 목표)가 기업의 클라우드 네이티브 전환을 가속화하고 있다.

```text
+---------------------------------------------------------------------+
|           전통적 IDC 아키텍처 vs 클라우드 네이티브 아키텍처            |
+------------------------------+--------------------------------------+
|  [On-Premise Legacy]         |  [Cloud-Native Reference Arch.]      |
|                              |                                      |
|   +----------+  +--------+  |   +---------+    +--------------+    |
|   | L4/L7 LB |--|  WAS   |  |   | Route53 |---->| CloudFront   |    |
|   | (F5 BIG-IP)| |(WebLogic)| |   |  (DNS)  |    |   (CDN)      |    |
|   +----------+  +----+---+  |   +---------+    +------+-------+    |
|                      |      |                         |            |
|                +-----v---+  |              +----------v---------+  |
|                |  RDBMS  |  |              |   API Gateway      |  |
|                | (Oracle)|  |              | (Kong/Amazon APIGW)|  |
|                |   RAC   |  |              +----------+---------+  |
|                +----+----+  |                         |            |
|                     |       |        +----------------+--------+  |
|              +------v-----+ |        v                v        v  |
|              | SAN Storage| |  +---------+  +---------+  +------+|
|              | (EMC VMAX) | |  | Lambda  |  |  ECS    |  |  EKS ||
|              +------------+ |  |(FaaS)   |  |(Docker) |  |(K8s) ||
|                              |  +----+----+  +----+----+  +--+---+|
|   CapEx 중심, Peak 2배 과다   |       |            |          |    |
|   장애시 수동 failover         |  +----v------------v----------v-+  |
|   수직확장(Scale-Up) 한계       |  |   Aurora / DynamoDB / S3     |  |
|                              |  |   (Multi-AZ, Auto Scaling)   |  |
|                              |  +------------------------------+  |
|                              |                                      |
|                              |  OpEx 중심, Auto Scaling            |
|                              |  IaC/Terraform, Immutable Infra     |
|                              |  수평확장(Scale-Out), Pay-per-Use    |
+------------------------------+--------------------------------------+
```

전통적 아키텍처 대비 클라우드 네이티브는 **①선언적 프로비저닝(Terraform HCL, CloudFormation YAML)** ②**불변 인프라(Immutable Infra, Packer로 AMI 빌드)** ③**Self-Healing(Health Check + ASG)** ④**관측 가능성(Observability, OpenTelemetry 3요소: Metrics/Logs/Traces)** 을 통해 시스템의 SRE(Site Reliability Engineering) 원칙을 실현한다.

- **📢 섹션 요약 비유**: 전통적 IDC는 **"사장님이 직접 짓는 단독주택"**(건축 기간 6개월, 이사비 1억, 냉난방 낭비)이고, 클라우드는 **"Airbnb 같은 공유 주거 플랫폼"**(1분 예약, 사용한 만큼 과금, 수요 폭증시 즉시 옆집 연결)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **NIST SP 800-145(미국 표준기술연구소)** 가 정의한 4가지 서비스 모델과 4가지 배포 모델(Public/Private/Hybrid/Community)을 토대로, **5대 핵심 메커니즘(가상화·오케스트레이션·API·자동화·관측)** 이 상호작용하는 계층 구조다.

```text
+------------------------------------------------------------------+
|        AWS Well-Architected Framework 6 Pillars + 12-Factor       |
|           (운영·보안·안정성·성능·비용·지속가능성)                  |
+------------------------------------------------------------------+
|  [Layer 4] SaaS  : SaaS 사용자 (Slack, Office365, Salesforce)      |
+------------------------------------------------------------------+
|  [Layer 3] FaaS  : Lambda / Azure Functions / Cloud Functions     |
|                   (이벤트 기반, 15분 timeout, 콜드스타트 200~500ms) |
+------------------------------------------------------------------+
|  [Layer 2] PaaS  : RDS, Aurora, EKS, App Runner, Elastic Beanstalk|
|                   (관리형 런타임, OS/미들웨어 추상화)               |
+------------------------------------------------------------------+
|  [Layer 1] IaaS  : EC2, VPC, EBS, S3, ALB (Hypervisor 추상화)    |
|                   (가상화: KVM/Xen/Nitro, Nitro System HW Offload)|
+------------------------------------------------------------------+
|  [Foundation] Region/AZ/Edge : 물리 DC 30+ 리전, 600+ PoP(CDN)    |
|              Region(≥2 AZ) / AZ(≥1 DC) / Local Zone / Wavelength |
+------------------------------------------------------------------+
|  [Cross-Cutting] Shared Responsibility Model                      |
|   - Customer 책임: 데이터, IAM, OS 패치, 네트워크 설정            |
|   - CSP 책임:        HW, 물리 보안, 글로벌 인프라, Hypervisor     |
+------------------------------------------------------------------+

    [Multi-Region Active-Active 트래픽 흐름]

    Client ---> Route53(Geolocation/Latency Routing)
                  |
       +----------+----------+
       v          v          v
    us-east-1  ap-northeast-2  eu-west-1
   (Virginia)   (Seoul)        (Ireland)
       |          |              |
   Aurora      Aurora         Aurora
   Global DB  (Writer)       (Reader)
       +----------+--------------+
            Binlog Replication
         (RPO < 1초, RTO < 30초)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ / Edge** | 물리적 격리 단위 | Region은 지리적으로 분리된 ≥2개의 AZ(가용 영역)로 구성, AZ간 Latency < 2ms, 광케이블 전용선 연결. Local Zone(예: AWS Seoul-ICN Local Zone)은 5G MEC용 1ms 레이턴시 보장 |
| **컴퓨트 서비스** | 워크로드 실행 | EC2(Nitro System: 네트워킹/EBS/스토리지를 HW 오프로드, KVM 기반), Lambda(컨테이너당 10GB 메모리, 동시성 1000/함수), Fargate(서버리스 K8s, vCPU 16GB까지) |
| **스토리지 서비스** | 데이터 영속성 | S3(11 9s 내구성 99.999999999%, 3-way replication, Intelligent-Tiering), EBS(gp3: 4000 IOPS/볼륨, io2 Block Express: 256K IOPS), EFS(NFS v4, 병렬 처리) |
| **네트워크·전송** | 트래픽 라우팅 | VPC(소프트웨어 정의 네트워크, /16~/28 CIDR), Transit Gateway(다중 VPC Hub-Spoke), CloudFront(600+ PoP, TLS 1.3, Brotli 압축), Global Accelerator(Anycast IP) |
| **관리·자동화** | IaC·관측 | Terraform(상태 파일 S3 백엔드, Remote State Locking via DynamoDB), CloudWatch + X-Ray(Distributed Tracing), EventBridge(110+ SaaS 이벤트 버스), AWS Config(규정 준수 평가) |
| **보안·거버넌스** | Zero Trust | IAM(최소 권한, ABAC 태그 기반), KMS(Envelope 암호화, FIPS 140-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 546 / 800

<- **이전**: [545. 클라우드 아키텍처 핵심 토픽 545번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/545_cloud_architecture_core_topic_545_exam_summar/)
**다음**: [547. 클라우드 아키텍처 핵심 토픽 547번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/547_cloud_architecture_core_topic_547_exam_summar/) ->

---
