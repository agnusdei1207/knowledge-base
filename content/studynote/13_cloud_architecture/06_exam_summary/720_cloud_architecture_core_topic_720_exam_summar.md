---
title: "720. 클라우드 아키텍처 핵심 토픽 720번 시험 요약 (Cloud Architecture Core Topic 720 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 "탄력적 자원 풀(Elastic Resource Pool) + 셀프서비스 API + 사용량 기반 과금(Pay-per-Use) + 무한 확장 가능한 분산 시스템"의 4대 특성을 만족시키기 위해 IaaS/PaaS/SaaS/FaaS 계층을 분리하고, 12-Factor App·Cloud-Native·Well-Architected Framework로 구조화한 **도메인 주도(DDD) + 마이크로서비스 + 이벤트 기반 + 옵저버빌리티**의 통합 청사진이다.
> 2. **가치**: AWS·Azure·GCP 기준 동일 워크로드(On-Prem 대비) 평균 TCO 30~40% 절감, Auto-Scaling으로 Peak 대비 60~80% Capacity 절감, Multi-AZ 구성 시 99.99%(Four 9s) 가용성, DevOps 파이프라인과 결합 시 배포 빈도 200배·리드타임 1/100·변경 실패율 1/7 향상(2019~2024 DORA 리포트 평균).
> 3. **판단 포인트**: **Lift-and-Shift vs Re-Platform vs Re-Architect(Refactor)** 트레이드오프, **Multi-Cloud vs Hybrid Cloud vs Single-Cloud** 거버넌스 복잡도·데이터 중력·벤더 종속(Lock-in)·법적 컴플라이언스(데이터 주권/Residency)·Egress 비용, **동기 REST vs 비동기 이벤트(Pub/Sub·Kafka)** 일관성 모델, **서버리스(Lambda) vs 컨테이너(EKS/GKE) vs VM(EC2)** 콜드 스타트·상태 관리·장기 실행 워크로드 적합성.

---

## Ⅰ. 개요 및 필요성

기존 On-Premise 데이터센터 기반의 3-Tier 아키텍처(웹서버-WAS-DB)는 **수직 확장(Scale-Up) 한계, Capacity 계획 실패 시 발생되는 Over-Provisioning(평균 30~70% 유휴 자원)**, 하드웨어 도입 리드타임(60~180일), CAPEX 중심 재무구조, 장애 시 RTO/RPO 수 시간~수 일이라는 고질적 문제를 안고 있었다. 2006년 AWS S3·EC2 출시 이후 **Utility Computing** 모델이 산업 표준으로 정착되었고, 2013~2015년 Docker·Kubernetes 등장으로 **Application Containerization**이 PaaS의 새로운 표준이 되었으며, 2014년 AWS Lambda 출시 이후 **Serverless/FaaS**가 이벤트 기반 워크로드의 핵심으로 부상했다.

2020년 COVID-19 이후 Digital Transformation이 가속화되며, IDC 보고서(2023)에 따르면 전 세계 기업 IT 지출의 **65% 이상이 Public Cloud**로 이동하였고, 한국은 2024년 기준 약 48%(과학기술정보통신부 클라우드 컴퓨팅 이용실태 조사)로 여전히 On-Premise 비중이 높아 **클라우드 네이티브 전환 전략**이 기술사 시험의 핵심 사안으로 부상했다.

```text
+----------------------------------------------------------------------+
|  On-Premise (3-Tier)            vs        Cloud-Native (분산형)        |
|                                                                       |
|   [Client]                          [Client/Mobile/Web/App]            |
|       |                                  |                            |
|       v                                  v (CDN: CloudFront/Akamai)  |
|  +---------+                  +--------------------------+            |
|  | L4/L7 LB|  하드웨어        |   API Gateway/Edge       |            |
|  +----+----+  60~180일         +------------+-------------+            |
|       v                                    v                          |
|  +---------+                  +--------------------------+            |
|  | Web/App |  Scale-Up       |  Microservices (EKS/GKE) |  HPA/VPA   |
|  | Server  |  수직확장        |  Pod Auto-Scaling        |  HPA(20%) |
|  +----+----+                  +------------+-------------+            |
|       v                                    v                          |
|  +---------+  RDBMS         +--------------------------+            |
|  |   DB    |  단일장애점     |  Polyglot Persistence    |  Multi-AZ  |
|  | (Oracle)|                |  (RDS+Redis+Dynamo+ES)   |  Active-   |
|  +---------+                +--------------------------+  Active    |
|                                                                       |
|  CAPEX 중심                      OPEX 중심 (Pay-per-Use)              |
|  평균가용성 99.9%                 평균가용성 99.99% (Multi-AZ)          |
|  배포주기 월 1회                  배포주기 일 1~수십회 (CI/CD)          |
+----------------------------------------------------------------------+
```

**On-Premise 대비 Cloud-Native로 전환 시 발생하는 핵심 변화 4가지**:
1. **불변 인프라(Immutable Infrastructure)**: 서버를 패치하지 않고 새로 배포(AWS의 AMI 재빌드, Kubernetes의 ReplicaSet 교체) -> Configuration Drift 제거
2. **Pet vs Cattle**: 서버를 개체(애완동물)가 아닌 가축(대량·교체 가능)으로 취급 -> 1대 장애 시 자동 치환
3. **API-Driven 선언적 프로비저닝**: Terraform/CloudFormation/CDK로 **Desired State** 선언 -> Drift Detection 및 자동 복구
4. **Observability 우선**: Logs(CLF), Metrics(CloudWatch/Prometheus), Traces(OpenTelemetry/X-Ray)의 3-Pillar 통합

- **📢 섹션 요약 비유**: 기존 On-Premise가 "자기 집을 짓고 수도·전기·난방을 직접 관리하는 것"이라면, 클라우드는 "이미 잘 지어진 호텔의 방을 필요한 만큼 빌리고, 룸서비스·청소·보안·확장까지 호텔 측에서 자동 제공하는 것"이다. 다만 호텔 규칙(API·리전·Egress 요금)에 맞춰 살아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **책임 분담 모델(Shared Responsibility Model)**과 **5대 핵심 특성(NIST SP 800-145)**을 이해하는 데서 출발한다. NIST는 ①On-demand Self-Service ②Broad Network Access ③Resource Pooling ④Rapid Elasticity ⑤Measured Service의 5가지를 정의하고, 배포 모델로 Public/Private/Hybrid/Community, 서비스 모델로 IaaS/PaaS/SaaS를 표준화했다.

```text
        [사용자 책임 영역]          <-->         [CSP(공급자) 책임 영역]
   +------------------------+         +----------------------------+
   | • 데이터 암호화(Key)   |         | • Region/AZ 물리 보안      |
   | • IAM 정책/접근통제     |         | • Hypervisor (Nitro, Fire- |
   | • OS 패치(EC2/IaaS)    |         |   cracker) 격리             |
   | • 네트워크(보안그룹)    |         | • 스토리지 내구성/암호화   |
   | • 애플리케이션 코드     |         | • 네트워크 백본 전송 암호화 |
   | • 데이터 분류/백업      |         | • DDoS Shield (AWS Shield) |
   | • 클라이언트 측 암호화  |         | • HSM (CloudHSM/KMS)       |
   +------------------------+         +----------------------------+
   IaaS: 사용자 많음 <------- 공통 -------> SaaS: 사용자 적음
   PaaS: 중간
```

아래는 **Cloud-Native Multi-Tier Reference Architecture**의 표준 패턴이다.

```text
                         +----------------------+
                         |  Route 53 / DNS      |
                         +----------+-----------+
                                    v
            +----------------------------------------------+
            |  CloudFront / Azure CDN / Cloud CDN (GCP)    |  <- Edge
            |  - TLS 1.3, HTTP/3, OAC, Lambda@Edge        |
            +----------------------+-----------------------+
                                   v
            +----------------------------------------------+
            |  WAF + Shield (L7) + ALB / NLB (L4/L7)      |  <- Edge
            |  - OWASP Top10 Rule Group, Rate Limiting     |
            +----------------------+-----------------------+
                                   v
            +----------------------------------------------+
            |  API Gateway / Kong / Apigee                 |  <- BFF/Edge
            |  - AuthN (JWT/OIDC), Throttling, Routing     |
            +----------------------+-----------------------+
                                   v
            +----------------------------------------------+
            |  Microservices (EKS/GKE/AKS)                 |  <- App
            |  +--------+ +--------+ +--------+            |
            |  |Order Svc| |Pay Svc | |User Svc|  HPA,VPA  |
            |  |(Java 21)| |(Node22)| |(Go 1.22)|  Istio   |
            |  +----+----+ +----+---+ +----+---+ Service  |
            |       +-----------+----------+    Mesh      |
            +----------------------+-----------------------+
                                   v
            +----------------------------------------------+
            |  비동기 이벤트 버스                          |  <- Async
            |  Kafka/MSK / Pub/Sub / EventBridge/Kinesis  |
            +----------------------+-----------------------+
                                   v
            +----------------------------------------------+
            |  Polyglot Data Layer                         |  <- Data
            |  Aurora PG (RDB) + DynamoDB (KV) + Redis    |
            |  (Cache) + S3 (Object) + OpenSearch (검색)  |
            |  + Neptune (Graph) + Timestream (시계열)     |
            +----------------------------------------------+

   Cross-Cutting:
   - Observability: CloudWatch + X-Ray + Grafana + Loki
   - Secrets: AWS Secrets Manager / HashiCorp Vault
   - CI/CD: GitHub Actions / CodePipeline / ArgoCD (GitOps)
   - Policy: OPA/Kyverno, Service Control Policy (SCP)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region & AZ** | 물리적 데이터센터 분리 단위 | AWS는 32개 Region, 각 Region 내 3개 이상 AZ(가용 영역) 유지. AZ 간 latency < 10ms, AZ 간 광케이블 전용선(Direct Connect)으로 동기 복제 가능. 한국은 `ap-northeast-2`(서울) Region, 4개 AZ 운영. |
| **컴퓨트 계층** | IaaS/PaaS/FaaS | EC2(가상머신), EKS(관리형 K8s), ECS(Fargate 컨테이너), Lambda(Serverless, 15분 한도·최대 10GB 메모리·10GB /tmp), Batch(HPC). 인스턴스 타입(M: 범용, C: 컴퓨트, R: 메모리, X: 스토리지, G/P: GPU, I: I/O)·세대별 성능 15~30% 향상. |
| **스토리지 계층** | 객체/블록/파일/아카이브 | S3(객체 11 9s 내구성·99.99% 가용성, 5TB/객체 한도), EBS(gp3 16K IOPS baseline, io2 64K IOPS, NVMe SSD), EFS(NFS v4), FSx(Lustre/ONTAP), Glacier(아카이브, retrieval 1분~12시간). **3-2-1 백업 규칙**(3개 사본, 2개 미디어, 1개 오프사이트)을 CSP의 Cross-Region 복제로 구현. |
| **네트워크 계층** | VPC·Subnet·라우팅 | VPC는 /16~/28 CIDR, Public/Private/Isolated Subnet 3-Tier 구성, NAT Gateway(Private -> Outbound), Internet Gateway, Transit Gateway(다중 VPC Hub-Spoke), PrivateLink(VPC Endpoint로 내부 통신), VPC Peering(비-전이적), Cloud WAN(Global SD-WAN). |
| **데이터 계층** | RDB·NoSQL·Warehouse | Aurora(MySQL/PostgreSQL 호환, 6-way 복제·Storage Auto-Scaling 128TiB), DynamoDB(Global Table Multi-Region Active-Active, p99 < 10ms), ElastiCache(Redis 7.x Cluster Mode), Neptune(Gremlin/SPARQL), Redshift(MPP 컬럼형, RA3 분리 컴퓨트-스토리지), OpenSearch(BM25+KNN 하이브리드 검색). |
| **보안 계층** | Zero-Trust·IAM·암호화 | IAM 사용자/Role/Policy(JSON), SCP(Service Control Policy, Org 단위), KMS(Customer Managed Key, FIPS 140-2 Level 3), Secrets Manager(Auto-Rotation), GuardDuty(ML 기반 이상행위 탐지), Macie(PII 자동 분류), Security Hub(CSPM 중앙), Detective(포렌식), Audit Manager(컴플라이언스 자동증적). |
| **관찰가능성** | Logs·Metrics·Traces | CloudWatch Logs(Metric Filter), CloudWatch Metrics(1분 기본, 1초 High-Resolution), X-Ray(Distributed Tracing, Service Map), Container Insights(ECS/EKS), Lambda Insights, Application Signals. OpenTelemetry(OTel) SDK로 벤더 중립 수집. |
| **거버넌스** | 멀티계정·정책자동화 | AWS Organizations(SCPs), Control Tower(Landing Zone), AWS Config(규정 준수·Drift 감지), CloudFormation StackSets(전계정 정책), Terraform(멀티클라우드 IaC), Pulumi(코드형 IaC, TypeScript/Python). |

**12-Factor App(Heroku, 2011)·Cloud-Native·Well-Architected Framework 6 Pillars**는 아키텍처 평가 기준으로 빈출한다:

1. **Codebase**: 단일 코드베이스, 다중 배포(Dev/Stg/Prod)
2. **Dependencies**: 명시적 의존성 선언(`package.json`, `requirements.txt`), 시스템 전역 암묵 의존 금지
3. **Config**: 환경변수(ENV) 주입, 코드 내 하드코딩 금지
4. **Backing Services**: DB/Queue/캐시를 **Attached Resource**로 취급(URL만으로 교체 가능)
5. **Build, Release, Run**: 세 단계 엄격 분리
6. **Processes**: Stateless, 영속 데이터는 Backing Service로
7. **Port Binding**: 자체 HTTP 포트로 서비스 노출
8. **Concurrency**: 프로세스 모델로 수평확장
9. **Disposability**: 빠른 시작·정상 종료(SIGTERM 핸들러, Grace Period)
10. **Dev/Prod Parity**: Gap 최소화(도커로 동일 이미지 사용)
11. **Logs**: stdout/stderr 스트림으로 외부 수집(12-factor 1.1+에서 12번째 항목)
12. **Admin Processes**: 일회성 관리 작업은 동일 env에서 run

**AWS Well-Architected 6 Pillars**: ①Operational Excellence ②Security ③Reliability ④Performance Efficiency ⑤Cost Optimization ⑥Sustainability. **Microsoft Azure Well-Architected 5 Pillar**(Reliability·Security·Cost·Operational·Performance Excellence)에 Sustainability 추가. **GCP Architecture Framework**: System/Application Design·Operational Excellence·Security/Privacy/Compliance·Reliability·Cost Optimization·Performance.

- **📢 섹션 요약 비유**: 12-Factor App은 "**출장용 캐리어 룰**"이다. 어떤 도시(환경)에 가도 같은 옷(코드)을 가져가고, 캐리어는 가볍게(Stateless), 옷에 태그(ENV)를 붙여 어떤 호텔에 가도 똑같이 풀 수 있게 표준화한 것이다. 캐리어가 무거우면 비행기(클라우드)에 못 태운다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 의사결정 트레이드오프는 **컴퓨트 모델**, **배포 모델**, **데이터 일관성 모델**, **통신 패턴**의 4축으로 요약
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 720 / 800

<- **이전**: [719. 클라우드 아키텍처 핵심 토픽 719번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/719_cloud_architecture_core_topic_719_exam_summar/)
**다음**: [721. 클라우드 아키텍처 핵심 토픽 721번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/721_cloud_architecture_core_topic_721_exam_summar/) ->

---
