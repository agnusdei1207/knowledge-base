---
title: "534. 클라우드 아키텍처 핵심 토픽 534번 시험 요약 (Cloud Architecture Core Topic 534 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 아키텍처의 핵심은 **"12-Factor App + 컨테이너(OCI) + 오케스트레이션(Kubernetes) + 서비스 메시(Istio) + IaC(Terraform) + GitOps(ArgoCD) + 옵저버빌리티(OTel/Prometheus)"**의 7대 축이 상호 결합되어, 애플리케이션을 불변(Immutable) 인프라 위에서 탄력적·회복력 있게 운영하는 패러다임이다.
> 2. **가치**: Fortune 500 도입 사례 기준 배포 빈도 **월 1회->일 1,000회 이상**, MTTR **93% 단축**, 인프라 CAPEX->OPEX 전환으로 TCO **30~50% 절감**, AWS Well-Architected 5대 기둥 준수 시 가용성 **99.95%->99.99%** 도출.
> 3. **판단 포인트**: **6R 마이그레이션 전략(Rehost/Replatform/Repurchase/Refactor/Retire/Retain)** 중 조직 성숙도(DevOps 성숙도 모델)와 도메인 결합도(Bounded Context 식별 가능 여부)에 따라 선택해야 하며, 분산 트랜잭션·데이터 일관성·네트워크 지연이라는 MSA 3대 트레이드오프를 Saga/CQRS/Event Sourcing으로 설계적으로 보완한다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅이 2006년 AWS S3·EC2 출시로 본격 상용화된 이래, 단순 IaaS(Virtual Machine 임대) 단계를 넘어 **애플리케이션 아키텍처 자체를 클라우드 환경에 맞게 재설계**하는 Cloud Native 사상이 2015년 CNCF(Cloud Native Computing Foundation) 결성으로 체계화되었다. 정보관리기술사 시험에서 "534번" 토픽은 일반적으로 **클라우드 네이티브 아키텍처 설계와 Well-Architected Framework 기반의 거버넌스**를 다룬다.

기존 Monolithic 아키텍처는 ①배포 단위의 거대화로 인한 **Hotfix-전체배포** 부담, ②Auto Scaling이 **Stack 전체 단위**로만 가능한 비효율, ③단일 DB로 인한 **데이터 락 경합**, ④기술 스택 Lock-in이라는 4대 구조적 한계를 가진다. Netflix가 2008년 DB 손상으로 3일간 서비스 장애를 겪은 사건(Reese Witherspoon DVD 사고)이 MSA 전환의 결정적 계기가 되었고, 이후 Spring Cloud(2014) -> Kubernetes 1.0(2015) -> Istio 1.0(2018) -> eBPF 기반 Cilium(2021)으로 기술 스택이 성숙해졌다.

```text
[아키텍처 진화 단계 — 클라우드 네이티브의 등장 배경]

  +----------+    +----------+    +--------------+    +--------------+    +------------+
  | Mainframe|    |Monolith  |    |  SOA / ESB   |    |Microservices |    |Cloud Native |
  |  (1960s) |---->| (1990s)  |---->|   (2005)     |---->|   (2014)     |---->|  (2018~)   |
  +----------+    +----------+    +--------------+    +--------------+    +------------+
       |              |                  |                   |                  |
   중앙집중형      단일 WAR/EAR         SOAP/WSDL         REST/gRPC          컨테이너+Mesh
   터미널          DB 공유             Enterprise Bus     독립 DB            선언적 API
   Green Screen    단일 언어           중앙 집중형         도메인 분리        불변 인프라
                                                                       GitOps 자동화
                                                                       OTel 옵저버빌리티
```

COVID-19(2020) 이후 디지털 트랜스포메이션이 가속화되면서 Gartner는 2025년 신규 엔터프라이즈 앱의 **95% 이상이 클라우드 네이티브**로 구축될 것으로 예측했다. 이러한 환경에서 기술사 출제 의도는 단순히 "MSA가 좋다"가 아니라, **언제 어떤 마이그레이션 전략을 채택하고, 어떤 트레이드오프를 수용할 것인가**에 대한 정량적 판단 근거를 요구한다.

- **📢 섹션 요약 비유**: 클라우드 네이티브 이전의 Monolith는 **하나의 거대한 돋보기로 모든 기능을 보는 망원경**과 같다. 클라우드 네이티브는 **망원경·현미경·광각렌즈를 자유자재로 갈아끼는 다목적 카메라 시스템**으로, 상황(트래픽·도메인·장애)에 따라 최적 도구를 선택해 촬영(처리)하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Cloud Native Architecture는 **7계층 참조 모델(7-Layer Reference Model)**로 체계화할 수 있다. CNCF의 Cloud Native Landscape v1.0을 기반으로 한다.

```text
[Cloud Native 7-Layer Reference Architecture — End-to-End 흐름]

   +-------------------------------------------------------------------------+
   | Layer 7 : 사용자 인터페이스                                                |
   |   +--------+  +--------+  +--------+  +--------+                       |
   |   | Mobile |  |   Web  |  |  B2B   |  |  IoT   |  <--- React, Flutter    |
   |   +----+---+  +----+---+  +----+---+  +----+---+                       |
   +--------+-----------+-----------+-----------+---------------------------+
            |           |           |           |
   +--------v-----------v-----------v-----------v---------------------------+
   | Layer 6 : Edge / Delivery                                                    |
   |   +--------------+  +--------------+  +--------------+                 |
   |   | CDN/CloudFront|  | WAF / Shield |  | API Gateway  |  <--- Kong, Apigee|
   |   | (정적 캐시)    |  | (L7 보안)    |  | (Rate Lim.)  |                 |
   |   +--------------+  +--------------+  +------+-------+                 |
   +---------------------------------------------+---------------------------+
                                                 | mTLS, OAuth2/JWT
   +---------------------------------------------v---------------------------+
   | Layer 5 : Service Mesh (동측/횡단 관심사)                                |
   |   +--------------------------------------------------------------+      |
   |   | Istio / Linkerd / Cilium Service Mesh                          |      |
   |   |  - L7 Routing (VirtualService)        - Retry/Timeout Policy  |      |
   |   |  - Circuit Breaker (Outlier Detection)- mTLS (SPIFFE ID)      |      |
   |   |  - Distributed Tracing (Jaeger)       - Access Log (Kiali)    |      |
   |   +--------------------------------------------------------------+      |
   +-------------------------------------------------------------------------+
            |              |              |              |
   +--------v---+    +-----v-----+   +----v-----+   +----v-----+
   | Order Svc  |    | Pay Svc   |   |Item Svc  |   |User Svc  |  <--- Layer 4
   |(Java/Spring|    |(Node.js)  |   |(Go/Gin)  |   |(Python)  |
   | Boot) Pod  |    | Pod x3    |   | Pod x5   |   | Pod x2   |     Workload
   +----+-------+    +-----+-----+   +----+-----+   +----+-----+
        | (gRPC/HTTP2)     |              |              |
   +----v------------------v--------------v--------------v-------------------+
   | Layer 3 : Container Orchestration (Kubernetes 1.30+)                      |
   |   +-------------+  +-------------+  +-------------+  +------------+    |
   |   | Deployment  |  | StatefulSet |  |   DaemonSet |  |   Job/Cron |    |
   |   | (Stateless) |  | (DB/Queue)  |  |  (Node Agent|  |  (Batch)   |    |
   |   +-------------+  +-------------+  +-------------+  +------------+    |
   |   +--------------------------------------------------------------+      |
   |   | HPA: CPU/Mem/Custom Metric(Queue Lag) -> Pod 1->N 스케일        |      |
   |   | VPA: Right-Sizing 권고     KEDA: Event-Driven Scaling          |      |
   |   | PDB: 자발적 장애 시 최소 Pod 수 보장     Cluster Autoscaler     |      |
   |   +--------------------------------------------------------------+      |
   +-------------------------------------------------------------------------+
            |
   +--------v-----------------------------------------------------------------+
   | Layer 2 : Runtime / Container                                              |
   |   +--------------+  +--------------+  +--------------+                 |
   |   | containerd   |  |   CRI-O      |  |   runC       |  <--- OCI 표준   |
   |   | (CRI gRPC)   |  |              |  | (runc/kata)  |      호환        |
   |   +--------------+  +--------------+  +--------------+                 |
   |   +------------------------------------------------------+               |
   |   | eBPF (Cilium) : 커널 우회 L4/L7 처리, Hubble 관측     |               |
   |   | gVisor/Kata    : 샌드박스 격리로 멀티테넌시 강화       |               |
   |   +------------------------------------------------------+               |
   +-------------------------------------------------------------------------+
            |
   +--------v-----------------------------------------------------------------+
   | Layer 1 : Infrastructure (Cloud Provider IaaS)                            |
   |   +----------------+  +----------------+  +----------------+            |
   |   | AWS EKS / ECS  |  | GCP GKE Autop. |  | Azure AKS      |            |
   |   |  (Control Plane|  | (노드 자동관리) |  | (Azure CNI)    |            |
   |   |   AWS 관리)    |  |                |  |                |            |
   |   +----------------+  +----------------+  +----------------+            |
   |   Node: EC2 m6i / Spot / Graviton3(arm64) / Inferentia / GPU(A100
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 534 / 800

<- **이전**: [533. 클라우드 아키텍처 핵심 토픽 533번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/533_cloud_architecture_core_topic_533_exam_summar/)
**다음**: [535. 클라우드 아키텍처 핵심 토픽 535번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/535_cloud_architecture_core_topic_535_exam_summar/) ->

---
