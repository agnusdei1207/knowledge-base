---
title: "Cloud Architecture Core Topic 575 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 하이퍼바이저(KVM/Xen/Hyper-V)와 컨테이너 오케스트레이터(Kubernetes/ECS)가 추상화한 분산 리소스 풀을 **API 기반 탄력적 셀프서비스**(IaaS/PaaS/SaaS/FaaS)로 제공하며, **NIST 5대 특성**(On-demand Self-service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 **Well-Architected 6대 기둥**(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)으로 거버넌스되는 시스템 설계 체계이다.
> 2. **가치**: AWS/Azure/GCP 사례 기준 **TCO 30~60% 절감**, Auto Scaling을 통한 **peak 트래픽 10x 대응**, 배포 주기 **주->일 단위 70% 단축**, Multi-AZ/Region 구성으로 **가용성 99.99%(연 52분 다운타임) 달성**, Time-to-Market **50% 단축**, 인프라 프로비저닝 시간 **수 주->수 분**으로 압축.
> 3. **판단 포인트**: ① **Lift&Shift(Rehost) -> Refactor(Replatform) -> Re-architect(Refactor) 6R 마이그레이션** 전략, ② 단일 CSP 종속 회피를 위한 **Multi-Cloud / Hybrid (Outposts/Azure Stack/GKE Anthos)** 선택, ③ 분산 데이터의 **CAP 정리 기반 CP(정합성) vs AP(가용성) 트레이드오프**, ④ VM vs Container vs Serverless **단위 granularity 결정**, ⑤ FinOps 기반 **예약 인스턴스(RI)/Savings Plan/SPOT** 비용 최적화 조합.

---

## Ⅰ. 개요 및 필요성

기존 온프레미스 데이터센터는 ① **CapEx(자본지출) 선투자형** capacity planning으로 평균利用率 15~25%에 불과해 peak 부하 대비 이중화(redundancy) 자원이 60% 이상 낭비되며, ② 신규 서버 도입에 4~12주, ③ IDC 동선·전력·냉각 인프라(PUEs 1.8~2.0) 운영 부담, ④ 자연재해·전력 차단 시 **DR(RTO/RPO) 24~72시간** 소요, ⑤ 글로벌 서비스 확장 시 region별 인프라 중복 구축이라는 한계를 가졌다.

2020년 이후 COVID-19로 인한 비대면 트래픽 폭증, AI/BigData 워크로드 등장, 마이크로서비스 아키텍처 보편화, Kubernetes 생태계 성숙(2015년 v1.0 출시, 2024년 v1.31 기준 CNCF 80+ 프로젝트), 그리고 5G/IoT 엣지 컴퓨팅 확산은 **"인프라는 코드로 정의되고, API로 소비되며, 사용량으로 과금되는"** 클라우드 네이티브 패러다임을 필수가 되게 만들었다.

NIST SP 500-145(2011) **클라우드 컴퓨팅 정의**는 ① 5대 필수 특성(필수), ② 3대 서비스 모델(IaaS/PaaS/SaaS), ③ 4대 배치 모델(Public/Private/Hybrid/Community)을 명시하며, 2024년 현재는 여기에 **FaaS(Function-as-a-Service, AWS Lambda/Azure Functions/GCP Cloud Functions)**와 **CaaS(Container-as-a-Service, EKS/AKS/GKE)**가 PaaS의 하위 세분화 모델로 자리잡았다.

```text
+-------------------------------------------------------------------------+
|                  클라우드 컴퓨팅 패러다임 전환 (2010 ~ 2024)                |
+-------------------------------------------------------------------------+
|                                                                         |
|   [온프레미스 시대]              [하이브리드 전환기]       [클라우드 네이티브] |
|   ----------------              ------------------       ---------------- |
|   CapEx 중심 투자         ->     CapEx+OpEx 혼합     ->    OpEx 완전 전환   |
|   수직확장(Scale-Up)      ->     수직+수평 혼합       ->    수평확장(Scale-Out)|
|   수동 프로비저닝         ->     IaC(Terraform)       ->    GitOps 자동화    |
|   3-Tier Monolith         ->     SOA/ESB            ->    Microservice    |
|   수 개월 배포주기        ->     2주 스프린트         ->    일 단위 CI/CD   |
|   연 99.9% (8.7h 다운)    ->     99.95% (4.4h 다운)  ->    99.99% (52분)   |
|                                                                         |
|   +----------------------+    +----------------------+  +------------+ |
|   |  데이터센터(Owned)   |    |  Private + Public    |  | Multi-Cloud| |
|   |  +- Mainframe        |    |  +- On-Prem Cluster  |  | +- Region A | |
|   |  +- UNIX Server      |    |  +- VPC Peering      |  | +- Region B | |
|   |  +- SAN Storage      |    |     (DirectConnect)  |  | +- Edge POP | |
|   +----------------------+    +----------------------+  +------------+ |
+-------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 온프레미스는 **"호텔 객실을 통째로 사두는 것"** — 365일 사용하지 않는 객실도 비용을 내야 한다. 클라우드는 **"필요한 날짜·인원·방 종류만 골라 쓰는 Airbnb"** — 사용한 만큼만 결제하고, 손님이 몰리면 즉시 옆집도 자동 연계한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 글로벌 인프라 계층**, **② 컴퓨트 추상화 계층**, **③ 데이터·메시징 계층**, **④ 네트워크·연결 계층**, **⑤ 운영 자동화 계층**으로 구성된다.

```text
+---------------------------------------------------------------------------+
|         하이퍼스케일 클라우드 글로벌 아키텍처 (AWS/Azure/GCP 공통 모델)    |
+---------------------------------------------------------------------------+
|                                                                           |
|  +--- Edge Layer (CDN/Edge Compute) ---------------------------------+  |
|  |  CloudFront/Azure CDN/Cloud CDN  |  Lambda@Edge / Cloudflare Workers |  |
|  +-------------+-----------------------------------------------------+  |
|                | HTTPS/QUIC                                             |
|  +-------------v-----------------------------------------------------+  |
|  |  Global Services Layer                                             |  |
|  |  +----------+ +----------+ +----------+ +----------+ +----------+  |  |
|  |  |   IAM    | | Route53/ | |   WAF    | |   KMS    | |CloudTrail|  |  |
|  |  |   SSO    | |  DNS     | |  DDoS    | |   HSM    | |   Audit  |  |  |
|  |  +----------+ +----------+ +----------+ +----------+ +----------+  |  |
|  +-------------+-----------------------------------------------------+  |
|                | gRPC/REST API                                          |
|  +-------------v-----------------------------------------------------+  |
|  |  Regional Services (Region 단위, 통상 2개 이상 AZ 보유)             |  |
|  |  +----------AZ-A--------+  +----------AZ-B--------+  +---AZ-C--+ |  |
|  |  | EC2/VM  EKS/AKS     |  | EC2/VM  RDS/Aurora   |  | Fargate  | |  |
|  |  | Lambda  Lambda      |  | EKS    ElastiCache   |  | Lambda   | |  |
|  |  | ALB/NLB  API GW     |  | ALB    SQS/SNS       |  | S3       | |  |
|  |  +---------+------------+  +---------+------------+  +----+-----+ |  |
|  |            |  AZ간 latency 1~2ms / 전용光纤              |       |  |
|  |            +---------- Intra-Region Backbone ------------+       |  |
|  +-------------+-----------------------------------------------------+  |
|                | Cross-Region Replication (s3 CRR/Azure GRS)            |
|  +-------------v-----------------------------------------------------+  |
|  |  Core Infrastructure (Global Backbone, 100+ PoPs, 25+ Regions)     |  |
|  +-------------------------------------------------------------------+  |
+---------------------------------------------------------------------------+
```

### Well-Architected Framework 6대 기둥 (AWS 기준, 타 CSP도 유사)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **운영 우수성**<br>(Operational Excellence) | 워크로드 운영·모니터링·지속적 개선 체계 | CloudWatch/Stackdriver Monitoring, X-Ray/Application Insights 분산 트레이싱, CloudTrail 감사 로그, IaC(Terraform/CloudFormation/CDK) 선언적 프로비저닝, Runbook·Postmortem 문서화 |
| **보안**<br>(Security) | 데이터·시스템·자산 보호 및 위험 평가 | IAM Least Privilege(RBAC/ABAC), VPC Isolation(Private/Public Subnet, NACL/SG), KMS HSM 기반 envelope encryption, GuardDuty/Security Center 위협 탐지, OWASP Top10 방어, Zero Trust Architecture(mTLS, BeyondCorp) |
| **안정성**<br>(Reliability) | 장애 복구·수요 변화 대응·재해 복구 | Multi-AZ/Region Active-Active, Auto Scaling Group(예측·반응·스케줄링), Health Check & Self-healing, RTO/RPO 정의, Chaos Engineering(Litmus/Chaos Monkey), Circuit Breaker Pattern(Hystrix/Resilience4j), 데이터 백업·스냅샷·CRR |
| **성능 효율**<br>(Performance Efficiency) | 컴퓨팅·스토리지·네트워크 등 리소스 최적화 | 캐싱 다층화(CloudFront->ElastiCache->DAX), Right-Sizing(GPU/CPU/Memory), 읽기 전용 복제본, Sharding·Partition Key, CDN 캐시 무효화, Performance Testing(k6/Gatling), C10K/C10M 대응 |
| **비용 최적화**<br>(Cost Optimization) | TCO 최소화·ROI 극대화 | FinOps 3단계(Inform/Optimize/Operate), RI/Savings Plan 최대 72% 할인, SPOT 인스턴스 최대 90% 할인, S3 Intelligent-Tiering, Idle Resource Sweep, Showback/Chargeback, Cost Anomaly Detection |
| **지속가능성**<br>(Sustainability) | 환경 영향 최소화(2021년 추가) | Region Selection(탄소 intensity 낮은 곳), Right-Sizing으로 에너지 효율, Spot 활용, 탄소 발자국 측정( Customer Carbon Footprint Tool), 그린 데이터센터(MS 100% 재생에너지 2025 목표) |

### 컴퓨트 추상화 단계 (가장 핵심 의사결정 축)

```text
+------------------------------------------------------------------+
|           클라우드 컴퓨트 추상화 스펙트럼 (Granularity 변화)       |
+------------------------------------------------------------------+
|  제어력 ^  <---------------------------------------------->  ^ 편의성|
|  Cold Start v                                            v 오토스케일|
|                                                                  |
|  +----------+  +----------+  +----------+  +----------+  +------+|
|  |  Bare    |  |   VM     |  | Container|  |  K8s Pod |  |FaaS  ||
|  |  Metal   |  |  EC2     |  |  Docker  |  |  EKS     |  |Lambda||
|  |          |  |  AzureVM |  |  CRI-O   |  |  AKS     |  |Func. ||
|  |          |  |  GCE     |  | containerd| |  GKE     |  |      ||
|  +----------+  +----------+  +----------+  +----------+  +------+|
|   minutes        minutes         seconds        seconds      ms  |
|   프로비저닝     프로비저닝       부팅            부팅        콜드스타트|
|   단위: 서버     단위: VM         단위: 컨테이너  단위: Pod   단위:함수|
|   과금:
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 575 / 800

<- **이전**: [574. 클라우드 아키텍처 핵심 토픽 574번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/574_cloud_architecture_core_topic_574_exam_summar/)
**다음**: [576. 클라우드 아키텍처 핵심 토픽 576번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/576_cloud_architecture_core_topic_576_exam_summar/) ->

---
