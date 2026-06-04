---
title: "733. 클라우드 아키텍처 핵심 토픽 733번 시험 요약 (Cloud Architecture Core Topic 733 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS Well-Architected Framework의 6대 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)과 12가지 설계 원칙(예: 분산 시스템 설계, 자동화, 무상태 컴퓨트 등)을 코드·인프라·조직 운영 전 계층에 적용하는 클라우드 네이티브 아키텍처 설계 방법론
> 2. **가치**: Multi-AZ/리전 구성을 통한 99.99% 가용성 SLA 달성, Auto Scaling으로 평균 60~70% 컴퓨트 비용 절감, RTO < 1분 / RPO < 1초의 재해복구 역량 확보, MTTR 평균 80% 단축
> 3. **판단 포인트**: CAP 정리 하의 일관성(Consistency)·가용성(Availability)·분단 내성(Partition Tolerance) 트레이드오프, 동기(sync)·비동기(async)·이벤트 드리븐 패턴 선택, 단일 장애점(SPOF) 제거, 강한 결합(Strong Coupling) vs 느슨한 결합(Loose Coupling) 경계 설정

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 3-tier 아키텍처(L4/L7 스위치, SAN 스토리지, Active-Active DB Clustering)는 CAPER(비용, 가용성, 성능, 탄력성, 복원력) 5대 요구를 동시에 충족하지 못하는 한계가 있다. 특히 N+1 이중화 구성조차도 IDC 전력·냉각·네트워크 단일 장애와 라이선스 종속성(VMware vSphere, Oracle RAC), 그리고 수직 확장(Scale-Up) 물리 한계에 갇혀 트래픽 변동성(Burstiness)에 대응하지 못한다. 클라우드 아키텍처는 이를 **"탄력성(Elasticity)", "불변 인프라(Immutable Infrastructure)", "관측 가능성(Observability)"** 으로 전환한다.

```text
   ┌──────────────── 전통적 온프레미스 아키텍처의 한계 ────────────────┐
   │                                                                   │
   │   [Client] ──> [L4/L7 LB] ──> [Web Tier: 2EA N+1]                │
   │                                       │                           │
   │                              ┌────────┴────────┐                  │
   │                              │ WAS: 2EA (Sticky)│                  │
   │                              └────────┬────────┘                  │
   │                                       │                           │
   │                              [SAN Storage] ← SPOP!                │
   │                                       │                           │
   │                              [Oracle RAC]  ← License Lock-in!     │
   │                                                                   │
   │   ✗ Burst 대응 불가  ✗ 수직확장 한계  ✗ DR RPO/RTO ≥ 24h          │
   └───────────────────────────────────────────────────────────────────┘
                              ▼ ▼ ▼ 변환 ▼ ▼ ▼
   ┌─────────────────── 클라우드 네이티브 아키텍처 ───────────────────┐
   │                                                                   │
   │   [Route 53]                                                       │
   │      │ (Health Check, Latency-based)                              │
   │      ▼                                                            │
   │   [CloudFront Edge] ──> [S3 Static Hosting]                       │
   │      │                                                            │
   │      ▼                                                            │
   │   [ALB / NLB] ──> [ECS Fargate / Lambda]  ← Auto Scaling        │
   │      │                  │ Stateless Pod (12-factor)               │
   │      │                  ▼                                        │
   │      │       [ElastiCache Redis]  ← Session 외부화               │
   │      │                  │                                        │
   │      ▼                  ▼                                        │
   │   [RDS Multi-AZ + Read Replica] / [DynamoDB Global Tables]        │
   │                                                                   │
   │   ✓ 수평확장 무제한  ✓ AZ 독립 장애  ✓ RPO<1s, RTO<1m            │
   └───────────────────────────────────────────────────────────────────┘
```

핵심 변화는 **"Capacity Planning → Capacity Just-in-Time"** 으로의 전환이다. Netflix는 AWS 마이그레이션 후, 평시 30% 여유분의 Auto Scaling Buffer로 Black Friday 트래픽 8배 급증을 5분 내 흡수한다(Nielsen Reelgood 2024 기준). 이 패러다임 전환이 필요한 이유는 **MOSFET 트래픽(SNS, 이벤트성 마케팅)** 패턴이 예측 불가능한 트래픽 스파이크를 유발하기 때문이다.

- **📢 섹션 요약 비유**: 전통적 아키텍처는 "정원용 정수탱크(고정 용량, 폭우 시 넘침)"이고, 클라우드 아키텍처는 "강물의 수위와 함께 자동으로 부풀고 줄어드는 풍선(탄력 용량, 무한 흡수)"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. AWS Well-Architected Framework 6대 기둥과 12가지 설계 원칙

```text
   ┌─────────── AWS Well-Architected Framework 6 Pillars ───────────┐
   │                                                                 │
   │        ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
   │        │ 운영우수성 │  │   보안    │  │  안정성   │                 │
   │        │ OpsExc.   │  │ Security │  │Reliab.   │                 │
   │        │   ▲       │  │   ▲      │  │   ▲      │                 │
   │        │   │       │  │   │      │  │   │      │                 │
   │ ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
   │ │ 지속가능성 │  │ 비용최적화│  │성능효율성 │                       │
   │ │Sustain.   │  │ CostOpt. │  │ PerfEff. │                       │
   │ └──────────┘  └──────────┘  └──────────┘                       │
   │                                                                 │
   │  Design Principles (12개, 추출):                                │
   │   1) 분산시스템  2) 자동화  3) 무상태(Stateless)                 │
   │   4) 권한최소화  5) IaC/Terraform  6) 푸시 아키텍처              │
   │   7) 결함방지>복구  8) 데이터 플레인/컨트롤 플레인 분리          │
   │   9) 변화예측  10) 가드레일  11) 시간절약 자동화  12) 검증      │
   └─────────────────────────────────────────────────────────────────┘
```

### B. 핵심 아키텍처 패턴: Multi-AZ Active-Active 3-Tier

```text
   ┌────────────── Region: ap-northeast-2 (Seoul) ───────────────┐
   │                                                              │
   │   ┌─────── AZ-a ────────┐   ┌─────── AZ-c ────────┐          │
   │   │                     │   │                     │          │
   │   │  [ALB #1] ───> [ECS ASG (min:2, max:10)]   │          │
   │   │     ▲              │   │     │              │          │
   │   │     │              │   │     ▼              │          │
   │   │  [RDS Primary] <──── Replication ────> [RDS Standby]     │
   │   │     │                                  │                │
   │   │     └────> [ElastiCache Replication Group]              │
   │   │              Primary (a)  +  Replica (c) + Replica (c)  │
   │   │                                                             │
   │   └─────────────────────┘   └─────────────────────┘          │
   │                                                              │
   │   Cross-Region:                                              │
   │   [S3 CRR] ──> [Tokyo Region Bucket]  ← RPO ≈ 15분        │
   │   [Route 53 Failover Policy: PRIMARY = Seoul, FAILOVER=Tokyo]│
   │                                                              │
   └──────────────────────────────────────────────────────────────┘

   Auto Scaling 의사결정 루프:
   ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
   │ CloudWatch   │───>│ Target Tracking│───>│   ASG API    │
   │ (ASG Metrics)│    │  Scaling Policy│    │ (Launch/Term)│
   │ CPU > 70%    │    │  Cooldown 300s │    │              │
   └──────────────┘    └───────────────┘    └──────────────┘
            ▲                                       │
            │                                       ▼
            └──── Metric Polling (1분 주기) ──── [EC2/Pod 상태]
```

### C. 무상태(Stateless) 컴퓨트 핵심 원리

12-Factor App §VI을 구현하기 위해 모든 사용자 세션·업로드 파일·트랜잭션 상태는 외부화한다:

| 계층 | 상태 보존 방식 | AWS 서비스 매핑 | 용량/지연 |
| :--- | :--- | :--- | :--- |
| **세션** | 분산 In-Memory K/V | ElastiCache for Redis (Cluster Mode) | 1ms 미만 |
| **파일/객체** | Object Storage | S3 Standard / IA / Glacier | 100ms 미만 |
| **관계형 데이터** | Multi-AZ Managed RDBMS | RDS Aurora MySQL/PostgreSQL | Single-digit ms |
| **비관계형** | Multi-Region NoSQL | DynamoDB Global Tables | 10ms 미만 (p99) |
| **메시지 큐** | At-least-once 비동기 버퍼 | SQS Standard / FIFO, Kafka(MSK) | ms~s |
| **이벤트 스트림** | Pub/Sub Fan-out | SNS, EventBridge, Kinesis | 100ms 미만 |

### D. CAP 정리와 클라우드 트레이드오프

```text
        Consistency (일관성)
               ▲
              /│\
             / │ \
            /  │  \   ← CP: DynamoDB(강한 일관성 모드), RDS
           /   │   \
          /    │    \  ← CA: 전통적 RDBMS 단일 리전
         /     │     \
        /______│______\ ───> Availability (가용성)
              │
              ↓
        Partition Tolerance (분단 내성) — 분산 시스템은 필수

   실전 매트릭스 (AWS 매핑):
   ┌────────────┬──────────────────┬──────────────────┐
   │   우선순위   │   선택 시스템     │   AWS 서비스      │
   ├────────────┼──────────────────┼──────────────────┤
   │  AP (가용)  │ Eventually Con. │ S3, DynamoDB,    │
   │            │ + 빠른 응답       │ Aurora 글로벌      │
   │ CP (일관)   │ 강한 일관성,     │ RDS Multi-AZ,     │
   │            │ 응답지연 허용     │ Redshift          │
   │ BASE       │ Basically Avail. │ Lambda + DynamoDB │
   │            │ Soft state, Ev.  │ Streams           │
   └────────────┴──────────────────┴──────────────────┘
```

### E. 가용성 수식과 예산 (SLO/SLA)

```
  가용성 = Uptime / (Uptime + Downtime)
  ┌──────────┬──────────┬──────────────┬─────────────┐
  │  가용성   │ 일일 허용  │ 월간 허용     │ 연간 허용     │
  │  99%     │  14.4분   │  7.2시간     │  3.65일      │
  │  99.9%   │  1.44분   │  43.2분      │  8.77시간    │
  │  99.95%  │  43.2초   │  21.6분      │  4.38시간    │
  │  99.99%  │  8.64초   │  4.32분      │  52.6분      │ ← 대부분의 SaaS 목표
  │  99.999% │  0.86초   │  25.9초      │  5.26분      │ ← "Five Nines"
  └──────────┴──────────┴──────────────┴─────────────┘
  Error Budget = (1 - SLO) × 기간
  99.9% SLO, 30일 → 43.2분의 장애 허용치 (이를 소비하면 배포 잠금)
```

- **📢 섹션 요약 비유**: Stateless 컴퓨트는 "언제든 교체 가능한 승무원이 공유 라운지(외부 저장소)에서 손님 응대 기록을 인계받는" 시스템이고, Stateful은 "특정 승무원 머릿속에만 기억이 있는" 시스템이라 그 사람이 아프면 모든 손님이 대기를 겪는다.

---

## Ⅲ. 비교 및 연결

### A. 컴퓨트 아키텍처 3대 패러다임 비교

| 구분 | Monolithic | Microservices (Container) | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR 단일 산출물 | 컨테이너 이미지 (Docker) | 함수 코드 + 이벤트 소스 |
| **확장 단위** | 인스턴스 전체 | Pod/Replica 수 | 동시 실행 수 (Concurrency) |
| **Cold Start** | 1~3분 (AMI 부팅) | 5~30초 (ECS) / 30
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 733 / 800

<- **이전**: [732. 클라우드 아키텍처 핵심 토픽 732번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/732_cloud_architecture_core_topic_732_exam_summar/)
**다음**: [734. 클라우드 아키텍처 핵심 토픽 734번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/734_cloud_architecture_core_topic_734_exam_summar/) ->

---
