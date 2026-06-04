---
title: "573. 클라우드 아키텍처 핵심 토픽 573번 시험 요약 (Cloud Architecture Core Topic 573 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 On-Premise의 CapEx 중심 정적 인프라를 AWS Well-Architected Framework 6대 축(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성) 기반의 가변형 분산 시스템(Region × AZ × Edge)으로 전환하는 설계 체계이며, API·SDK·IaC(Terraform/CloudFormation)를 통해 Control Plane과 Data Plane을 분리하여 선언적·반응형·탄력적(Elastic) 운영을 구현하는 것이 핵심이다.
> 2. **가치**: Auto Scaling Group + ALB + Multi-AZ RDS 패턴 적용 시 가용성 99.95%->99.99%(연 52분->4.38분 다운타임 단축), Spot Instance + Savings Plans + S3 Intelligent-Tiering 결합으로 TCO 30~70% 절감, Lambda + EventBridge 기반 이벤트 드리븐 아키텍처로 평균 응답 지연 200ms->40ms·운영 인력 1/3 감축 효과가 검증된다.
> 3. **판단 포인트**: Stateful(OLTP, RDS, ElastiCache) vs Stateless(API Gateway, Lambda, CloudFront) 워크로드 구분, 동기(REST/gRPC) vs 비동기(SQS/SNS/Kafka/EventBridge) 트래픽 패턴, 단일 리전 vs 액티브-액티브 멀티 리전 vs Pilot Light vs Warm Standby DR 전략의 RTO/RPO/비용 트레이드오프, 그리고 EKS·ECS·Lambda·EC2 중 컨테이너 오케스트레이션과 서버리스 경계 설정이 아키텍트 의사결정의 4대 핵심 축이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3·EC2 출시 이후 18년간 **Monolithic On-Premise -> 가상화 -> 클라우드 마이그레이션 -> Cloud-Native 리팩토링 -> 분산·엣지·AI 통합**으로 급속 진화했다. 한국 시장은 2023년 기준 Public Cloud 시장 규모 7.5조 원, 2027년 21조 원 전망(메가존클라우드/Gartner)이며, 금융·공공·제조 업권에서 클라우드 네이티브 전환이 가속화됨에 따라 기술사 시험에서 **"클라우드 아키텍처 설계 시 안정성·보안·비용·성능 4축의 Trade-off 분석 및 Well-Architected Framework 기반 정량적 의사결정"** 이 핵심 평가 영역으로 부상했다.

기존 On-Premise 아키텍처는 **(1) 예측 기반 Capacity Planning**, **(2) 수직 확장(Scale-Up) 한계**, **(3) HA 구성의 복잡성(Active-Passive 클러스터링)**, **(4) DR 사이트 별도 구축(고비용)**, **(5) 라이선스 종속성**, **(6) CapEx 회수 불가**라는 6대 구조적 한계를 가졌다. 반면 클라우드 아키텍처는 **Pay-as-you-go OpEx 모델, Auto Scaling을 통한 Horizontal Scale, Multi-AZ 기본 제공, API 기반 셀프 서비스 프로비저닝, 글로벌 리전 엣지, IaC를 통한 불변 인프라(Immutable Infrastructure)** 로 전환하여, 비즈니스 변동성에 따라 인프라가 코드처럼 유연하게 대응하는 **"Infrastructure as Code as Architecture"** 패러다임을 실현한다.

```text
   +------------------------------------------------------------------+
   |          클라우드 아키텍처 패러다임 전환 (Before vs After)         |
   +------------------------------------------------------------------+

   [Before: On-Premise Monolithic]              [After: Cloud-Native Distributed]
   +-------------------------+                 +------------------------------+
   |  사용자 (LAN/WAN)        |                 |  Global Users (CDN/Edge)     |
   +----------+--------------+                 +----------+-------------------+
              | F5 BIG-IP L4/L7 LB                          | CloudFront / Cloudflare
   +----------v--------------+                 +----------v-------------------+
   |  WebSphere / Tomcat     |  --------►     |  ALB / API Gateway / CloudFront|
   |  (수직확장, 라이선스)    |                 |  (Lambda@Edge, WAF 연동)      |
   +----------+--------------+                 +----------+-------------------+
              |                                              |
   +----------v--------------+                 +----------v-------------------+
   |  Oracle RAC / DB2 HADR  |  --------►     |  Aurora Multi-Master / DynamoDB|
   |  (Active-Passive, SAN)  |                 |  (3 AZ 동기 복제, Global Table) |
   +----------+--------------+                 +----------+-------------------+
              |                                              |
   +----------v--------------+                 +----------v-------------------+
   |  SAN/NAS 스토리지       |  --------►     |  S3 / EBS gp3 / EFS / FSx    |
   |  (LUN, NFS, CIFS)       |                 |  (Object, Block, File 3-Tier) |
   +----------+--------------+                 +----------+-------------------+
              |                                              |
   +----------v--------------+                 +----------v-------------------+
   |  수동 Capacity Planning |  --------►     |  Auto Scaling + Event-Driven |
   |  수동 패치/백업         |                 |  CloudWatch + EventBridge    |
   +-------------------------+                 +------------------------------+
   CAPEX (자산) + OPEX (유지)                    OPEX (사용량 기반) + 변동비
   6~12개월 구축 사이클                          1일~1주 프로비저닝, API 기반
```

- **📢 섹션 요약 비유**: 기존 On-Premise는 **"사계절 수요를 예측해 직물 공장 기계를 한 번에 짓는 방식"**(초과 투자/부족 운영)이고, 클라우드는 **"우산 렌탈 서비스"** — 비 오는 날에만 자동 대여·반납되며 폭우 시엔 대기 우산이 무한히 늘어나는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **Region(국가 단위 데이터센터 클러스터) -> AZ(Availability Zone, 1개 이상 독립 데이터센터) -> Edge Location(CDN/CloudFront POP)** 의 3계층 글로벌 인프라를 토대로, **Control Plane(API 호출, IaC 선언) ↔ Data Plane(실제 트래픽 처리)** 을 분리하고, 이를 **VPC·Subnet·Security Group·NACL·Route Table** 의 5대 네트워크 프리미티브로 격리·연결한다. 컴퓨팅은 **EC2(IaaS, 가상머신) -> ECS/EKS(컨테이너 오케스트레이션) -> Lambda(FaaS, 서버리스)** 의 추상화 스펙트럼을 가지며, 각 계층은 책임 분산 모델(Shared Responsibility Model)에 따라 관리 범위가 달라진다.

```text
   +------------------------------------------------------------------------+
   |        AWS 기반 표준 3-Tier Web Application Reference Architecture     |
   |        (Multi-AZ, Auto Scaling, Managed Services 우선)                |
   +------------------------------------------------------------------------+

                  +---------------------+
                  |  Route 53 (DNS,     |
                  |  Latency-Based,     |   <--- Active-Active Multi-Region
                  |  Health Check)       |
                  +----------+----------+
                             | Anycast
                  +----------v----------+
                  |  CloudFront (CDN)   |   <--- S3 OAI/OAC + Lambda@Edge
                  |  + AWS WAF + Shield |
                  +----------+----------+
                             | HTTPS
                  +----------v----------+  +------------+  +------------+
                  |   ALB (L7)          |--|  ACM 인증서  |  |  Cognito   |
                  |   AZ-a, AZ-c, AZ-d  |  +------------+  |  (OAuth 2) |
                  +----------+----------+                  +------------+
                             | Target Group
              +--------------+--------------+
              |              |              |
   +----------v----+  +------v-----+  +-----v------+
   |  EC2 ASG Min:2 |  |  EC2 ASG  |  |  EC2 ASG   |  <--- AMI + Launch Template
   |  Max:10        |  |  Spot 30% |  |  On-Demand |
   |  AZ-a          |  |  AZ-c     |  |  AZ-d      |  <--- Target Tracking: CPU 60%
   +----------+-----+  +----+------+  +-----+------+
              |              |              |
              +--------------+--------------+
                             | JDBC / gRPC
                  +----------v----------+
                  |  Aurora MySQL       |   <--- Multi-AZ, Cluster: Writer + 2 Reader
                  |  (또는 RDS Proxy)   |   <--- Automated Backup + PITR
                  |  Primary / Standby  |   <--- KMS Encryption at Rest
                  +----------+----------+
                             | Binlog Replication
                  +----------v----------+
                  |  ElastiCache Redis  |   <--- Cluster Mode, Multi-AZ
                  |  (Session, Cache)   |
                  +---------------------+

   --- 비동기/이벤트 경로 ---------------------------------------------
   +--------------+    Kinesis Data Streams    +----------------------+
   |  EC2/Service | -------------------------► |  Lambda Consumer     |
   |  (Producer)  |    (Partition Key Shard)   |  -> S3 Data Lake      |
   +--------------+    (Shard 4개, On-Demand)  |  -> OpenSearch        |
                                                +----------------------+
   +--------------+    SQS Standard/FIFO       +----------------------+
   |  주문 API    | -------------------------► |  결제 Worker Lambda  |
   |  (Producer)  |    (DLQ 3회 재시도)         |  -> DynamoDB          |
   +--------------+                            +----------------------+

   --- 가시성/관측성 --------------------------------------------------
   +----------------------------------------------------------------+
   |  CloudWatch Metrics + Logs + Alarms + X-Ray + EventBridge     |
   |  + AWS Config (규정 준수) + CloudTrail (감사)                  |
   +----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Route 53 + CloudFront** | 글로벌 트래픽 진입점, DNS·CDN·DDoS 방어 | Anycast IP 200개+ PoP, Latency/Weighted/Geoproximity 라우팅 정책, Lambda@Edge로 뷰어 요청/응답 시점 코드 실행, ACM 인증서 종단, Shield Standard 자동 적용 |
| **VPC + Subnet + SG/NACL** | 논리적 네트워크 격리 (Region 단위, /16~ /28) | Public/Private/Isolated Subnet 3-Tier 분리, Security Group(Stateful, Instance 단위) ↔ NACL(Stateless, Subnet 단위) 이중 방어, VPC Endpoint(Gateway/Interface)로 S3·DynamoDB·Secrets Manager 사설 연결, Transit Gateway로 다중 VPC Hub-Spoke 토폴로지 |
| **ALB + NLB + GWLB** | L4/L7 로드밸런싱, GENEVE 터널 | ALB는 Path/Host/Header 기반 라우팅 + WAF 통합, NLB는 초저지연(100ns)·정적 IP·TCP/UDP/TLS 종단, GWLB는 제3자 어플라이언스(Trellix, Palo Alto) 투명 삽입, ALB->Lambda 직접 호출로 EC2 없는 API 구성 가능 |
| **EC2 + ASG + Launch Template** | 가변 컴퓨팅 풀, 수평 확장 | Launch Template(AMI/UserData/IAM Role 불변) + ASG Min/Desired/Max + Target Tracking(CPU/Request Count/Network In) + Predictive Scaling(일 48회 자동 예측), Spot Fleet으로 비용 90% 절감, Mixed Instances Policy로 On-Demand·Spot 혼합 |
| **RDS/Aurora + ElastiCache** | 관리형 RDBMS·인메모리 캐시 | Aurora는 6-way 복제, Reader Endpoint 자동 로드밸런싱, Aurora Global Database로 1초 미만 RPO, RDS Proxy로 커넥션 풀링·Lambda 동시성 폭증 방지, ElastiCache Redis는 Cluster Mode로 Shard당 250GB·수십만 OPS |
| **S3 + EBS + EFS + FSx** | 4종 스토리지 (Object·Block·File·HPC) | S3는 11개 9s 내구성, Lifecycle(Standard->IA->Glacier Instant/Deep Archive), Event Notifications로 SQS·Lambda 트리거, EBS gp3는 3000 IOPS·125MB/s 기본, EFS는 NFS v4·Pay-per-use, FSx for Lustre는 HPC/ML |
| **Lambda + EventBridge + SQS/SNS** | 서버리스·이벤트 드리브 메시징 | Lambda 15분 타임아웃·10GB 메모리·10000 동시성, EventBridge로 SaaS 이벤트·스케줄·이벤트 버스 라우팅, SQS Standard(무제한 처리량, 적어도 1회) vs FIFO(300 TPS, 정확히 1회), SNS Fan-out 패턴 |
| **EKS/ECS/Fargate** | 컨테이너 오케스트레이션 | EKS(managed K8s control plane, CNI VPC IP), Fargate(서버리스 컨테이너, vCPU/GB 단위 과금), Istio/Linkerd 서비스 메시, HPA·Cluster Autoscaler·Karpenter로 노드 자동화, IRSA(IAM Role for Service Account)로 Pod 단위 인증 |
| **IAM + KMS + Secrets Manager** | 인증·인가·키 관리 | IAM Policy JSON(Allow/Deny, Action/Resource/Condition), RBAC vs ABAC, KMS CMK 자동 키 회전(1년), Secrets Manager 자동 로테이션(Lambda 트리거), VPC Endpoint 정책으로 IAM 권한 격
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 573 / 800

<- **이전**: [572. 클라우드 아키텍처 핵심 토픽 572번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/572_cloud_architecture_core_topic_572_exam_summar/)
**다음**: [574. 클라우드 아키텍처 핵심 토픽 574번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/574_cloud_architecture_core_topic_574_exam_summar/) ->

---
