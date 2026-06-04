---
title: "776. 클라우드 아키텍처 핵심 토픽 776번 시험 요약 (Cloud Architecture Core Topic 776 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **탄력성(Elasticity)·온디맨드 셀프서비스(On-Demand Self-Service)·가용성(High Availability)·API 기반 프로그래머빌리티(Programmability via API)**를 4대 NIST 특성으로 정의하며, 이를 구현하기 위해 **컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)의 분리**, **이머티브(Imperative) vs 디클러러티브(Declarative) 인프라 관리**, **리소스 추상화(Resource Abstraction)와 멀티테넌시(Multi-tenancy)**를 핵심 메커니즘으로 채택한다.
> 2. **가치**: CapEx(설비투자) -> OpEx(운영비용) 전환으로 **TCO 30~60% 절감**, Auto Scaling을 통해 **트래픽 피크 시 5~20배 용량 자동 확장**, 12-Factor App + 마이크로서비스 + IaC(Infrastructure as Code) 적용 시 **배포 주기 80% 단축**(월 1회 -> 일 10회+), 멀티 AZ/리전 배포로 **가용성 SLA 99.99%(연 52분 이내 장애)** 달성.
> 3. **판단 포인트**: **Lift-and-Shift vs Refactor vs Re-architect(6R 모델)** 마이그레이션 전략, **모놀리식 vs 마이크로서비스**, **베어메탈 vs VM vs 컨테이너 vs 서버리스** 런타임 선택, **Single-Cloud vs Multi-Cloud vs Hybrid Cloud**의 **벤더 종속성(Lock-in)·데이터 주권·지연시간·비용 최적화** 4축 트레이드오프 분석이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premises) 아키텍처는 **수직 확장(Scale-Up) 방식의 예측 기반 용량 계획(Capacity Planning)**, **물리적 자산의 CapEx 투자**, **수동 패치/업그레이드**, **단일 장애점(SPOF: Single Point of Failure) 노출**이라는 구조적 한계를 가진다. 2020년대 이후 **초연결(Hyper-Connected)·초대용량(Hyperscale)·초지연민감(Zero-Latency-Tolerance)** 환경이 도래하면서, **다크 트래픽(Dark Traffic)**과 **블랙스완 이벤트(COVID-19, 2022년 트래픽 4.3배 증가)**에 대응할 수 있는 **탄력적 분산 아키텍처**가 필수불가결해졌다.

NIST SP 800-145 및 ISO/IEC 22123-1 표준에서 정의한 클라우드 컴퓨팅의 5대 필수 특성(Essential Characteristics)은 ① **온디맨드 셀프서비스**, ② **광역 네트워크 액세스(Broad Network Access)**, ③ **리소스 풀링(Resource Pooling)**, ④ **신속한 탄력성(Rapid Elasticity)**, ⑤ **측정 가능한 서비스(Measured Service)**이며, 이를 만족하기 위해 **하이퍼바이저 기반 가상화(KVM, Xen, Hyper-V) -> 컨테이너 오케스트레이션(Kubernetes, ECS) -> 서버리스(Lambda, FaaS) -> 엣지 컴퓨팅(Wavelength, Outposts)**로 컴퓨팅 추상화 레이어가 끊임없이 진화하고 있다.

```text
+---------------------------------------------------------------------+
|            클라우드 아키텍처 패러다임 전환: On-Prem -> Cloud-Native   |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise Era]              [Cloud Era]            [Cloud-Native]|
|  -----------------            --------------         --------------|
|  +----------+                  +----------+          +----------+ |
|  |물리서버  |                  |  VM/EC2  |          |Pod/함수  | |
|  | 1U,R720  |--수직확장-------->|m5.xlarge |--수평----->|EKS Pod  | |
|  |CPU고정  |  CPU/RAM 추가    |  vCPU    |  자동확장 |서버리스  | |
|  +----------+                  +----------+          +----------+ |
|       |                            |                       |     |
|   CapEx(3~5년)                OpEx(사용량)         Pay-per-Invocation|
|   수동 배포(월)               IaC(Terraform)       GitOps(ArgoCD)  |
|   RAID/SAN 스토리지          EBS/EFS/Object        CSI Driver      |
|   단일 IDC 의존              Multi-AZ/Multi-Region  Multi-Cloud K8s|
|                                                                     |
|  [장애 허용성]              [가용성]                 [탄력성]       |
|  99.9% (연 8.7H)           99.95% (연 4.4H)        99.99%(52.6m)  |
+---------------------------------------------------------------------+
```

**왜 필요한가?**
- **글로벌 트래픽 패턴 변화**: 카카오톡 데이타임 피크 5,000만 동시접속, 넷플릭스 시청 시간대 90% 집중 -> 정적 용량 계획 한계
- **비즈니스 민첩성(Agility) 요구**: 한국은행 BaaS, 토스 슈퍼앱처럼 **신규 서비스 TTM(Time-to-Market)을 6개월 -> 2주로 단축**하기 위한 개발-배포-모니터링 파이프라인 자동화
- **데이터 폭증**: 2025년 전 세계 데이터 175 ZB(제타바이트) -> **스토리지 계층화(Tiered Storage: Hot/Warm/Cold/Archive)**와 **오브젝트 스토리지(S3, GCS)**의 병행 필수
- **규제 준수**: 개인정보보호법, GDPR, 클라우드 서비스 보안 인증(CSAP) -> **리전 선택(데이터 레지던시)**, **암호화 키 관리(KMS, HSM)**, **감사 로그(Audit Trail)** 기술 필수

- **📢 섹션 요약 비유**: 온프레미스는 **자기 집 정원에 수영장 짓는 것**(평생 사용, 손수 관리, 확장 시 뜯어고침)이고, 클라우드는 **수영장 이용권 가진 클럽会员**(필요한 만큼만, 늘 깨끗, 피크시 풀 추가 개장)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 **참조 모델(Reference Architecture)**은 **NIST 클라우드 참조 모델**, **AWS Well-Architected Framework**(5대 기둥: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization), **Azure Architecture Center**, **GCP Architecture Framework**가 사실상 표준이다. 이를 **5계층(Layer) 모델**로 추상화하면 다음과 같다.

```text
+----------------------------------------------------------------------+
|                  클라우드 아키텍처 5계층 참조 모델                    |
+----------------------------------------------------------------------+
|  [L5] 거버넌스/관리 평면  | IAM(SSO/MFA), KMS, CloudTrail, OrgUnit  |
|  -----------------------+------------------------------------------  |
|  [L4] 플랫폼/서비스 평면  | API GW, Service Mesh(Istio), BFF        |
|  -----------------------+------------------------------------------  |
|  [L3] 애플리케이션 평면   | 마이크로서비스(Pod/Lambda), BaaS         |
|  -----------------------+------------------------------------------  |
|  [L2] 데이터 평면         | RDB Aurora, NoSQL DynamoDB, Redis, S3   |
|  -----------------------+------------------------------------------  |
|  [L1] 인프라/컴퓨팅 평면  | Region->AZ->VPC->Subnet->EC2/EKS/ECS       |
|  -----------------------+------------------------------------------  |
|  [L0] 물리/엣지 평면      | 데이터센터, PoP, Wavelength, Outposts   |
+----------------------------------------------------------------------+
```

**핵심 컴포넌트별 동작 원리:**

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **리전(Region) / 가용영역(AZ)** | 지리적 격리 단위, 재해복구 단위 | 리전 간 100~200ms RTT, AZ 간 1ms 미만, **동기 복제(Synchronous, Aurora) vs 비동기 복제(Asynchronous, S3 CRR)** 선택. 한국: ap-northeast-2 (서울, 4개 AZ: a/b/c/d) |
| **가상 네트워크(VPC/VNet)** | 논리적 L2/L3 격리, SDN 기반 | **VXLAN 오버레이**(MTU 9001, Jumbo Frame), **서브넷 라우팅 테이블(RT) + NACL + Security Group**의 **3단 방화벽** 모델, **Transit Gateway**로 VPC 피어링 N² 문제 해결 |
| **컴퓨트 추상화** | 워크로드 실행 단위 | ① 베어메탈(i3.metal) -> ② VM(EC2 m6i) -> ③ 컨테이너(EKS Fargate, vCPU/GB 단위 과금) -> ④ 함수(Lambda, 1ms 단위, **콜드 스타트 100~500ms**)로 추상화 단계 상승 |
| **오브젝트 스토리지(S3/GCS/Blob)** | 무한 확장 BLOB 저장 | **Erasure Coding(Reed-Solomon)**: 11+3 또는 6+3 -> 디스크 2~3개 손실 허용, **수명주기 정책**(S3 IA -> Glacier Instant/Deep Archive), **Strong Consistency**(2020년 도입) |
| **로드밸런서 & 오토스케일링** | 트래픽 분산 및 탄력성 | **L4 NLB(Network Load Balancer) -> L7 ALB(Application Load Balancer) -> Gateway LB(GWLB)**, **Target Tracking Policy**(CPU 70% 유지), **Predictive Scaling**(ML 기반 사전 확장), **Step Scaling** |
| **IaC & GitOps** | 인프라 선언적 코딩 | **Terraform(HCL) / Pulumi(코드) / CloudFormation(JSON/YAML)**로 선언형 인프라, **ArgoCD/Flux**로 **Git = Single Source of Truth**, PR 리뷰 기반 프로덕션 변경 |
| **관측가능성(Observability)** | 3대 시그널 측정 | **Metrics(Prometheus/CloudWatch, 15s 해상도) + Logs(중앙집중, Loki/ELK) + Traces(OpenTelemetry, Jaeger/Tempo)**. **SLI/SLO/SLI Budget** 기반 **Error Budget Policy** |

**심화 기술 원리:**

- **컨트롤 플레인 vs 데이터 플레인 분리**: AWS의 **S3 데이터 경로**(디스크 I/O)와 **관리 경로**(API 호출, IAM 검사) 분리는 일관성과 성능을 양립시키는 핵심. 컨트롤 플레인 SLA는 일반적으로 99.9%, 데이터 플레인은 99.99%.
- **선형적 일관성 모델(Consistency)**: DynamoDB는 **튜닝 가능 일관성**(Strongly/Eventually/Transactional Read) 제공 -> **Quorum W+R>N 공식**: 3개 노드 중 W=2, R=2이면 Strong Consistency.
- **AWS Nitro System**: 2017년 도입된 **경량 하이퍼바이저 + 전용 Nitro Card(네트워크/스토리지 가속) + 보안 칩**으로 호스트 OS 제거 -> 인스턴스 성능 30% 향상, Bare Metal 인스턴스 제공.
- **Kubernetes 제어 루프**: **Declarative Spec -> API Server -> etcd(RAFT 합의) -> Controller(노드/Pod/스케줄러) -> kubelet -> Status**로의 **Reconciliation Loop**가 클러스터 **Desired State**를 유지.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **만화영화의 영화 세트장**과 같다. **리전 = 촬영소(국가)**, **AZ = 스튜디오 건물(건물 한 채가 불나도 다른 건물에서 촬영 계속)**, **VPC = 세트장 안의 도시 전체**, **보안그룹 = 촬영장 출입 게이트**, **Auto Scaling = 인형 탈 교대근무**(자연스럽게 추가/제거), **Multi-Region = 같은 영화를 다른 나라에서 동시에 찍어 보험** 드는 것.

---

## Ⅲ. 비교 및 연결

**서비스 모델 비교** (IaaS / PaaS / SaaS / FaaS)

| 구분 | IaaS (Infrastructure-as-a-Service) | PaaS (Platform-as-a-Service) | SaaS (Software-as-a-Service) | FaaS (Function-as-a-Service) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 책임** | 앱/데이터/OS/미들웨어, 사용자가 런타임까지 | 앱/데이터만 (OS 이하 CSP 관리) | 사용자는 데이터와 접근권한만 | 코드(함수)만, 상태 없음 |
| **대표 서비스** | EC2, GCE, Azure VM | RDS, Elastic Beanstalk, App Engine | Office 365, Slack, Salesforce | Lambda, Cloud Functions, Azure Functions |
| **확장 단위** | 인스턴스(수 분 소요) | 인스턴스/컨테이너(수 초) | 사용자 수에 따라 자동 | 호출당 1ms 단위 과금 |
| **적합 워크로드** | 레거시 Lift&Shift, HPC | API 서버, 웹앱, 데이터 분석 | 정형 업무 (CRM, HRM) | 이벤트 기반, 간헐적 워크로드 |
| **과금 모델** | 시간/초당 (On-Demand, Reserved, Spot) | 시간당 + 사용량 | 사용자/월 (Per Seat) | GB-초 + 호출 횟수 |
| **콜드 스타트** | 없음 (이미 기동) | 10~30초 | N/A | 100ms~10초 (의존성 많을수록 ^) |

**배포 모델 비교** (Public / Private / Hybrid / Multi-Cloud)

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- |
| **소유/운영** | CSP (AWS/Azure/GCP) | 자체/전용 CSP (SK C&C T-Cloud, NHN) | 온프레미스 + 퍼블릭 연동 | 2개 이상 퍼블릭 |
| **주 사용 사례** | 신사업 MVP, 글로벌 서비스 | 금융/공공 규제, 데이터 주권 | Burst-Out, 재해복구, 레거시 연동 | 벤더 종속 회피, 최적 서비스 |
| **연결 기술** | Internet/Direct Connect | 전용회선/MPLS | **ExpressRoute/DX + Transit GW** | **Interconnect, VPN, CASB** |
| **보안 통제** | CSP 책임공유 모델 | 완전 통제 | 정책별 분장 | **CSPM(Cross-Cloud Security Posture Mgmt)** |
| **비용 구조** | OpEx 100% | CapEx+OpEx | CapEx+OpEx 혼합 | OpEx + 이중 관리비 |

**핵심 통합·연결 포인트:**
- **클라우드-온프레미스 연결**: **AWS Direct Connect / Azure ExpressRoute / GCP Interconnect**(전용선 1~10Gbps) + **VPN IPSec**(암호화 오버레이, BGP 라우팅)
- **컨테이너 오케스트레이션**: Kubernetes가 **Multi-Cloud 추상화 계층** -> EKS(AWS) + GKE(GCP) + AKS(Azure) **Anthos / Tanzu / OpenShift**로 통합
- **데이터 레이크 통합**: **S3 + Glue(Data Catalog) + Athena(SQL on S3) + Redshift(Spectrum)** 파이프라인 또는 **Snowflake / Databricks**의 멀티클라우드 데이터 레이크하우스
- **CI/CD 파이프라인**: GitHub Actions -> ECR(컨테이너 레지스트리) -> ArgoCD(GitOps 동기화) -> Istio(서비스 메시 카나리 배포 5%->25%->100%) -> Datadog(관측)

- **📢 섹션 요약 비유**: 서비스 모델은 **주방 조리 단계**와 같다. **IaaS = 마트에서 재료 사와 직접 요리**, **PaaS = 배
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 776 / 800

<- **이전**: [775. 클라우드 아키텍처 핵심 토픽 775번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/775_cloud_architecture_core_topic_775_exam_summar/)
**다음**: [777. 클라우드 아키텍처 핵심 토픽 777번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/777_cloud_architecture_core_topic_777_exam_summar/) ->

---
