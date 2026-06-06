---
title: "Replatform Partial Optimization Migration"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리플랫폼 부분 최적화 마이그레이션(Replatform with Partial Optimization)은 Gartner 6R 모델의 "Replatform(Lift·Tinker·Shift)" 단계에서 전체 리팩터링이 아닌, 운영 부담이 큰 특정 계층(Managed DB, Container Runtime, Object Storage, Caching, Message Broker 등)만 선택적으로 PaaS/Managed Service로 교체하여 TCO를 절감하는 점진적 클라우드 전환 전략이다.
> 2. **가치**: 동일 코드/도메인 모델을 유지하면서 IaaS 대비 운영비 30~60% 절감, 배포 리드타임 70% 단축, DB 라이선스 비용 80% 이상 제거(예: Oracle SE -> AWS Aurora PostgreSQL 전환 시), 그리고 무중단·저위험 방식으로 레거시 핵심 시스템의 기술 부채를 6~18개월 내 해소 가능하다.
> 3. **판단 포인트**: "어디까지 최적화할 것인가(Granularity)", "동시 운영 기간의 데이터·트랜잭션 정합성 보장", "Managed Service 종속성(Vendor Lock-in) vs 운영 효율 Trade-off", "Strangler Fig·Anti-Corruption Layer 설계", "ROI 산정 시 라이선스 회수·인력 전환·SLA 영향까지 포함한 TCO 회수 기간(Payback Period) 산출"이 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

전통적 엔터프라이즈 시스템은 On-Premise의 상용 솔루션(Oracle DB, WebLogic, IBM MQ 등)에 깊이 종속되어 있으며, 10년 이상 운영된 레거시 시스템은 (1) 라이선스·하드웨어 유지비 증가, (2) EOL(End of Life) 도래, (3) 신규 프레임워크(Spring Boot, Node.js, Go 등)와의 통합 한계, (4) Monolithic 아키텍처로 인한 배포 주기 장기화라는 4대 기술 부채에 직면한다. 그러나 "한 번에 전면 리팩토링(Refactor/Re-architect)"은 비즈니스 연속성·예산·조직 역량 측면에서 실패 확률이 매우 높다(Forrester 조사: 전면 리호스팅 대비 리팩토링 프로젝트의 60% 이상이 일정·예산 초과).

이에 대한 현실적 해법이 **리플랫폼 부분 최적화 마이그레이션**이다. 이는 전체 시스템을 그대로 옮기는 Lift & Shift(Rehost)와 전면 재설계인 Refactor/Re-architect의 중간 지점이며, 도메인 로직과 API Contract는 보존하면서 **병목·고비용·EOL 임박 컴포넌트**만 Cloud-Native Managed Service로 선택적 치환한다. 대표적으로 (a) RDBMS를 Aurora·Cloud SQL·Azure Database로, (b) EJB/Servlet 컨테이너를 Tomcat·Spring Boot로, (c) 자체 MQ를 Kafka·SQS·Pub/Sub으로, (d) 로컬 파일 시스템 기반의 로그·첨부파일 저장소를 S3·GCS·Blob Storage로 전환하는 케이스가 해당한다.

핵심 사고방식은 "**최소 변경으로 최대 효과(Minimum Viable Migration)**"이며, 이를 통해 CapEx -> OpEx 전환, 라이선스 회수, 자동화(Autoscale, Self-healing) 효과를 얻으면서도 비즈니스 리스크를 최소화한다.

```text
[레거시 환경 - As-Is]                              [리플랫폼 부분 최적화 - To-Be]
+---------------------------------+                 +---------------------------------+
|        Monolithic Application   |                 |    부분 최적화된 Hybrid App      |
|  +--------------------------+   |                 |  +--------------------------+   |
|  |  JSP/Servlet + EJB      |   |                 |  |  Spring Boot (Container) |   | <- 부분 리팩터
|  |  + 비즈니스 로직          |   |                 |  |  + 도메인 로직 보존       |   |
|  +----------+---------------+   |                 |  +----------+---------------+   |
|             | JDBC              |                 |             | HikariCP          |
|  +----------v---------------+   |    Replatform   |  +----------v---------------+   |
|  |  Oracle RAC (SE/EE)      |   |  -----------►   |  |  AWS Aurora PostgreSQL  |   | <- Managed DB
|  |  + TDE + 수동 백업        |   |   Partial       |  |  + 자동 Failover + KMS   |   |
|  +----------+---------------+   |   Optimization  |  +--------------------------+   |
|  +----------v---------------+   |                 |  +--------------------------+   |
|  |  IBM MQ / RabbitMQ (자체)|   |                 |  |  Amazon SQS / MSK(Kafka)|   | <- Managed MQ
|  +--------------------------+   |                 |  +--------------------------+   |
|  +----------v---------------+   |                 |  +--------------------------+   |
|  |  NAS/SAN 파일 스토리지    |   |                 |  |  S3 + CloudFront (CDN)   |   | <- Object Storage
|  +--------------------------+   |                 |  +--------------------------+   |
|  +----------v---------------+   |                 |  +--------------------------+   |
|  |  WebLogic/JBoss + License|   |                 |  |  ECS Fargate / EKS       |   | <- Container Runtime
|  +--------------------------+   |                 |  +--------------------------+   |
|  비용구조: CapEx 60% + Lic 30%  |                 |  비용구조: OpEx 100% (사용량 기반)|
+---------------------------------+                 +---------------------------------+
```

| 구분 | 기존(As-Is) | 리플랫폼 부분 최적화 후(To-Be) |
| :--- | :--- | :--- |
| **데이터 계층** | Oracle SE/EE, 수동 HA 구성, TDE·RMAN 운영 | Aurora PostgreSQL/MySQL Multi-AZ, 자동 백업·PITR |
| **런타임** | WebLogic/JBoss(상용 WAS 라이선스) | Open Liberty / Tomcat / Spring Boot 내장 WAS |
| **메시징** | IBM MQ / TIBCO EMS | Amazon SQS/SNS 또는 MSK(Kafka) |
| **스토리지** | NAS/SAN, NFS, Tape 백업 | S3 Standard/IA, Glacier, Object Lifecycle |
| **인프라 운영** | IDC 입주, HW 유지보수, OS 패치 | Fargate/EKS, AWS가 OS·미들웨어 패치 |
| **비용 흐름** | CapEx 60%, OpEx 40% | OpEx 100% (Pay-per-use) |

- **📢 섹션 요약 비유**: 낡은 집의 골조(기둥·보)와 인테리어(도메인 로직)는 그대로 두고, **지붕(Managed DB)·보일러(Container)·창문(Storage)·인터폰(Message Broker)** 만 최신식·무인동작·에너지 1등급으로 교체하는 "선택적 리모델링"과 같다. 철거(Rehost)도, 전면 재건축(Refactor)도 아닌, **살면서 고치는** 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

리플랫폼 부분 최적화 마이그레이션은 **① 도메인·계약 보존(Contract-First)** 원칙 하에, **② Anti-Corruption Layer(ACL)** 를 통해 신규 Managed Service와 기존 시스템의 어댑터를 분리하고, **③ Strangler Fig Pattern** 으로 트래픽을 점진적으로 전환하며, **④ 데이터 이중화·CDC(Change Data Capture)** 로 동기화 일관성을 유지하는 것이 핵심 원리이다.

전체 흐름은 (1) As-Is 시스템 분석 -> (2) 최적화 대상 컴포넌트 선정(6R 판단 매트릭스) -> (3) 대상 Managed Service PoC -> (4) ACL·Strangler 라우터 설계 -> (5) 데이터 마이그레이션(DMS/CDC) -> (6) 카나리 트래픽 전환(5% -> 25% -> 50% -> 100%) -> (7) 레거시 컴포넌트 Retire의 7단계로 진행된다.

```text
[리플랫폼 부분 최적화 마이그레이션 - 7단계 실행 아키텍처]

  ① Discovery --► ② Decide(6R) --► ③ PoC --► ④ Design(ACL/Strangler)
                                                        |
                                                        v
  +----------------------------------------------------------------+
  |                  Strangler Fig Proxy / API Gateway              |
  |   +------------+    +-------------+    +----------------+      |
  |   | Router Rule|---►| Legacy App  |    | Optimized App  |      |
  |   | (Header,   |    | (유지)      |    | (신규 PaaS)    |      |
  |   |  Path, % ) |    +------+------+    +--------+-------+      |
  |   +------------+           |                    |              |
  +---------------------------+--------------------+--------------+
                              | Anti-Corruption    | Anti-Corruption
                              | Layer(Adapter)     | Layer(Adapter)
                              v                    v
                    +------------------+  +----------------------+
                    | Legacy Oracle DB |  | AWS Aurora PostgreSQL|
                    +--------+---------+  +----------+-----------+
                             |   AWS DMS / Debezium   |
                             |   (CDC, Full+Incr.)    |
                             +----------+-------------+
                                        v
                            +----------------------+
                            | Migration Task State |
                            |  (Validating->Loading |
                            |   -> Ready->Cutover)   |
                            +----------------------+
                                        v
  ⑤ Migrate(DMS) --► ⑥ Canary(5%->100%) --► ⑦ Retire Legacy
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Strangler Fig Router** | 트래픽 점진 전환의 관문. 헤더·경로·비율 기반 라우팅 | Spring Cloud Gateway, AWS ALB(Weighted Target Group), Kong, Istio VirtualService. v1/v2 Weight를 95:5 -> 50:50 -> 0:100 순으로 변경 |
| **Anti-Corruption Layer (ACL)** | 신규 Managed Service의 API/스키마 차이를 흡수, 레거시 도메인 모델 격리 | DDD Bounded Context 경계에서 Adapter·Translator·Facade 패턴. 예) Oracle의 `NUMBER(15,2)` -> PostgreSQL `NUMERIC(15,2)` 변환기 |
| **Data Migration Service (DMS)** | 무중단 데이터 이관, CDC로 양방향 동기화 유지 | AWS DMS, Azure DMS, GCP DMS. Full Load + Ongoing Replication 모드, SCN/LSN 기반 체크포인트, Lag 1초 미만 |
| **Managed DB Proxy** | Connection Pool, Read/Write Split, Failover | RDS Proxy, Azure DB Proxy, ProxySQL. Spring의 `HikariCP` 와 함께 이중 Pool 구성으로 cold start 제거 |
| **Container Runtime (부분 최적화 핵심)** | JSP/EJB 컨테이너를 경량화 | Spring Boot Embedded Tomcat + Docker -> ECS Fargate / EKS / Cloud Run. JVM 옵션(`-XX:MaxRAMPercentage=75.0`)으로 메모리 효율화 |
| **Observability Layer** | 양 시스템의 통합 가시성, 전환 기간 SLA 보장 | OpenTelemetry -> Prometheus + Grafana, AWS CloudWatch, Datadog. RED(Rate/Error/Duration) + USE(Utilization/Saturation/Error) |
| **Feature Flag / Kill-Switch** | 문제 발생 시 즉시 Legacy로 트래픽 복귀 | LaunchDarkly, Unleash, AWS AppConfig. Canary 단계에서 RPS·Error Rate 임계치 초과 시 자동 Rollback |

핵심 파라미터 및 알고리즘은 다음과 같다.

- **6R 판단 매트릭스**: `Score = (Cost_Saving × 0.35) + (Risk_Reduction × 0.25) + (Time_to_Value × 0.20) + (Vendor_LockIn_Risk⁻¹ × 0.20)`. 임계치 0.6 이상 시 Replatform 후보.
- **CDC 동기화 지연(Lag) 허용치**: 일반 OLTP는 `Lag < 5s`, 금융/결제는 `Lag < 500ms`. AWS DMS의 `CDCStartPosition "server time"` 옵션 + Kafka Connect Debezium의 `snapshot.mode=initial` 조합.
- **Strangler 전환 비율 산정**: `r(t) = r₀ + (1 - r₀) × (1 - e^(-kt))`, 초기 비율 `r₀=0.05`, `k=0.1/day`. 30일 만에 95% 도달하는 Sigmoid 곡선.
- **TCO 회수 기간(Payback Period)**: `PP = (Migration_Cost) / (Annual_Saving)`. Aurora 전환 시 평균 14~22개월, IBM MQ -> SQS 전환 시 8~12개월이 일반적.

- **📢 섹션 요약 비유**: 심장 수술에서 **"전신 마취 + 개흉술(Refactor)"** 이 아니라, **"심도자술(Catheter)"** 처럼 대퇴동맥에 가는 관(Strangler Router)을 넣고, 좁아진 관상동맥(병목 Managed Service)만 스텐트(Managed DB/SQS)로 확장하는 것과 같다. 몸(레거시 도메인)은 깨어있고, 회복도 빠르다.

---

## Ⅲ. 비교 및 연결

리플랫폼 부분 최적화 마이그레이션은 다른 클라우드 마이그레이션 전략 및 관련 아키텍처 패턴과 명확히 구분된다. 가장 많이 혼동되는 4가지 전략과의 비교는 다음과 같다.

| 구분 | Rehost (Lift & Shift) | **Replatform (부분 최적화)** | Repurchase (SaaS 교체) | Refactor / Re-architect |
| :--- | :--- | :--- | :--- | :--- |
| **코드 변경** | 없음 (바이너리 그대로) | **최소-중간 (Driver/Config/ACL만)** | 전면 신규 (SaaS 도입) | 전면 재설계 (Cloud-Native) |
| **아키텍처** | 동등 (1:1 매핑) | **부분 Hybrid (Strangler)** | SaaS 종속 (멀티테넌트) | MSA·Serverless·Event-Driven |
| **데이터 계층** | 기존 그대로 (EC2 Oracle) | **Managed DB로 치환 (RDS/Aurora)** | SaaS DB 종속 (Salesforce 등) | NoSQL·NewSQL (DynamoDB/Cosmos) |
| **소요 기간** | 3~6개월 | **6~18개월** | 6~12개월 | 18~48개월 |
| **리스크** | 낮음 | **중간 (핵심은 CDC·이중 운영)** | 중간-높음 (커스텀 손실) | 높음 (재설계 결함) |
| **비용 절감** | 10~20% (HW·IDC료) | **30~60% (License 회수 효과)** | 40~70% (라이선스·인프라 통합) | 50~80% (Scale-to-Zero) |
| **대표 사례** | Oracle on RH
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 443 / 800

<- **이전**: [442. 리호스트 리프트 앤 시프트 마이그레이션](/studynote/13_cloud_architecture/06_exam_summary/442_rehost_lift_and_shift_migration/)
**다음**: [444. 리팩터 클라우드 네이티브 재설계](/studynote/13_cloud_architecture/06_exam_summary/444_refactor_cloud_native_redesign/) ->

---
