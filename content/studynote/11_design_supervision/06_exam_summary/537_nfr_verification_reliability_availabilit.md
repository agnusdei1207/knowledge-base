---
title: "NFR Verification Reliability Availability"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비기능 요구사항 검증은 시스템의 신뢰성(Reliability: MTBF/MTTF 지표)과 가용성(Availability: A=MTBF/(MTBF+MTTR), 99.9%~99.999% 업타임 SLA)을 정량적으로 측정·입증하는 엔지니어링 활동이며, ISO/IEC 25010 품질 모델과 SRE의 SLI/SLO/SLA 체계로 체계화됩니다.
> 2. **가치**: 연간 허용 다운타임을 99.9%(연 8.76시간)에서 99.999%(연 5.26분)로 1단계 향상시킬 때 SLA 페널티 비용 절감, 고객 이탈률 0.5~1%p 감소, 비즈니스 연속성 확보 효과가 발생하며, 카오스 엔지니어링과 회복 테스트를 통해 사전 검증된 시스템은 장애 시 MTTR을 평균 60% 단축할 수 있습니다.
> 3. **판단 포인트**: Active-Active 다중화(고비용·저지연·데이터 정합성 위험) vs Active-Passive(저비용·페일오버 지연), 동기식 복제(RPO=0·지연 비용) vs 비동기식 복제(RPO>0·성능 우위), 무중단 배포 전략(Blue-Green·Canary·Rolling)의 트레이드오프를 RTO/RPO 목표와 TCO 관점에서 결정해야 합니다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 시스템의 품질은 기능적 요구사항(Functional Requirements)이 "무엇을 하는가"를 정의한다면, 비기능 요구사항(Non-Functional Requirements, NFR)은 "얼마나 잘, 얼마나 안정적으로, 얼마나 빠르게 수행하는가"를 정의합니다. 특히 **신뢰성(Reliability)**과 **가용성(Availability)**은 금융·공공·의료 등 미션 크리티컬(Mission-Critical) 시스템에서 SLA 위반이 곧 막대한 금전적·법적 손실로 직결되기 때문에, 검증 가능한 객관적 지표로 측정되어야 합니다.

그러나 실무에서 NFR은 "시스템은 안정적이어야 한다", "트래픽이 많으면 빨라야 한다"와 같은 모호한 표현으로 정의되어 검증 불가능한 경우가 많습니다. 2017년 AWS S3 us-east-1 리전 장애(4시간 중단, S&P 500 기업 영향), 2021년 Facebook BGP 설정 오류로 인한 6시간 전역 장애 등은 가용성 검증 부재의典型적인 사례이며, 기술사 시험에서도 "신뢰성과 가용성을 어떻게 정량적으로 검증할 것인가"가 핵심 논점입니다.

```text
+-------------------------------------------------------------------------+
|                NFR 검증 프레임워크 (V-Model 기반)                         |
+-------------------------------------------------------------------------+
|                                                                         |
|   요구사항 정의          시스템 설계           구현           테스트     |
|   +----------+         +----------+       +----------+   +----------+ |
|   | NFR 정의 |--------->| 아키텍처 |------->|  코딩/구축|--->|  인수    | |
|   | SLA 수립 |         | 패턴선택 |       |  IaC/CI  |   |  테스트  | |
|   +----------+         +----------+       +----------+   +----------+ |
|        |                    |                                  ^        |
|        v                    v                                  |        |
|   +----------+         +----------+                            |        |
|   | SLI 식별 |         | 위험분석 |                            |        |
|   | SLO 설정 |         | FMEA/FTA |       +--------------------+--+    |
|   | Error    |         | RTO/RPO  |       |  NFR 검증 기법         |    |
|   | Budget   |         | 결정     |       |  • 부하/스트레스 테스트|    |
|   +----------+         +----------+       |  • 카오스 엔지니어링  |    |
|                                            |  • 회복/DR 훈련       |    |
|                                            |  • 침투/장애 주입      |    |
|                                            |  • Soak/내구 테스트    |    |
|                                            +-----------------------+    |
+-------------------------------------------------------------------------+

  +----------- 가용성 등급별 연간 허용 다운타임 -----------+
  | 등급      비율          연간 다운타임       월간        |
  | ----------------------------------------------------- |
  | 2-nine    99%           87.60 시간          7.30 시간  |
  | 3-nine    99.9%         8.76 시간           43.83 분   |
  | 4-nine    99.99%        52.60 분            4.38 분    |
  | 5-nine    99.999%       5.26 분             26.30 초   |
  | 6-nine    99.9999%      31.56 초            2.63 초    |
  +------------------------------------------------------+
```

기존 패러다임은 개발 완료 후 QA팀이 "잘 돌아가는지"를 주관적으로 확인하는 것이었습니다. 현대 패러다임은 **SLI(지표) -> SLO(목표) -> SLA(계약) -> Error Budget(허용 오류 예산)**으로 연결되는 Google SRE 모델을 도입하여, NFR을 코드처럼 버전 관리하고 자동화된 카오스 실험으로 지속 검증하는 것입니다. 이는 가용성을 "최선의 노력(Best Effort)"에서 "엔지니어링 제약 조건(Engineering Constraint)"으로 격상시켰습니다.

- **📢 섹션 요약 비유**: 신뢰성·가용성 검증은 마치 **고속철도(KTX) 시스템**과 같습니다. 단순히 "기차가 달린다"가 아니라, 1년 365일 99.9% 정시 운행(가용성), 10만 km당 고장 0.1회 이하(신뢰성, MTBF), 고장 시 30분 내 복구(MTTR)를 매일 시뮬레이션하고 인증하는 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

신뢰성과 가용성을 보장하는 시스템 아키텍처는 **SPOF(Single Point Of Failure) 제거**가 핵심이며, 이를 위해 다중화(Redundancy)·격리(Isolation)·자동화(Automation) 원칙이 적용됩니다. 핵심 수식은 다음과 같습니다.

| 수식 | 설명 | 적용 |
|:---|:---|:---|
| **A = MTBF / (MTBF + MTTR)** | 가용성 = 평균 고장 간격 / (평균 고장 간격 + 평균 수리 시간) | 시스템·서비스 단위 가용성 계산 |
| **λ = 1 / MTBF** (고장률, Failure Rate) | 단위 시간당 고장 발생 빈도 | FIT(Failures In Time, 10⁹ 시간당) 단위 |
| **R(t) = e^(-λt)** (신뢰도 함수) | 시간 t까지 무고장 생존 확률 | 전자부품·SW 모듈 (지수분포) |
| **R(t) = e^(-(t/η)^β)** (Weibull) | 기계·마모 부품의 수명 분포 | 디스크·배터리·팬 등 |
| **MTTR = MTTI + MTTR_fix** | 복구시간 = 장애 인지 시간 + 실제 수리 시간 | 관측 가능성(Observability) 중요성 |
| **N+1 / 2N / 2N+1 이중화** | 이중화 등급 결정 | N: 정상 운영 필요 컴포넌트 수 |

```text
+----------- 고가용성(HA) 시스템 아키텍처 (Active-Active Multi-AZ) -----------+
|                                                                              |
|                       +-------------------------+                           |
|                       |    Global Load Balancer  | (Anycast / DNS GeoDNS)  |
|                       |   (Route53 / Cloudflare) |  L7 Health Check       |
|                       +------------+------------+                           |
|                                    |                                         |
|              +---------------------+---------------------+                   |
|              v                     v                     v                   |
|     +----------------+    +----------------+    +----------------+          |
|     |  AZ-1 (정상)    |    |  AZ-2 (정상)    |    |  AZ-3 (정상)    |          |
|     |  +----------+  |    |  +----------+  |    |  +----------+  |          |
|     |  | App Pod×3|  |    |  | App Pod×3|  |    |  | App Pod×3|  |          |
|     |  | (HPA 70%)|  |    |  | (HPA 70%)|  |    |  | (HPA 70%)|  |          |
|     |  +----+-----+  |    |  +----+-----+  |    |  +----+-----+  |          |
|     |       |        |    |       |        |    |       |        |          |
|     |  +----v-----+  |    |  +----v-----+  |    |  +----v-----+  |          |
|     |  | Redis    |  |    |  | Redis    |  |    |  | Redis    |  |          |
|     |  | Cluster  |  |    |  | Cluster  |  |    |  | Cluster  |  |          |
|     |  +----+-----+  |    |  +----+-----+  |    |  +----+-----+  |          |
|     |       |        |    |       |        |    |       |        |          |
|     |  +----v-----+  |    |  +----v-----+  |    |  +----v-----+  |          |
|     |  |  MySQL   |<--+----+-->|  MySQL   |<--+----+-->|  MySQL   |  |          |
|     |  |  Primary |  |    |  | Standby  |  |    |  | Standby  |  |          |
|     |  +----------+  |    |  +----------+  |    |  +----------+  |          |
|     +----------------+    +----------------+    +----------------+          |
|              |                     |                     |                   |
|              +---------------------+---------------------+                   |
|                                    v                                         |
|                       +-------------------------+                           |
|                       |  Observability Stack     |                           |
|                       |  Prometheus + Grafana    |                           |
|                       |  Loki + Tempo (Tracing)  |                           |
|                       |  AlertManager + PagerDuty|                           |
|                       +-------------------------+                           |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Load Balancer (L4/L7)** | 트래픽 분산 및 Health Check 기반 자동 페일오버 | L4: IP/Port 기반(NLB, F5), L7: HTTP 헤더·경로·쿠키 기반(ALB, Envoy, Istio). Health Check 주기 5~10초, 임계치 2~3회 실패 시 해당 인스턴스 제외(Drain) |
| **Application Tier (Stateless)** | 무상태 서비스 다중화, HPA 기반 오토스케일링 | Kubernetes Deployment + HPA(CPU 70%, Memory 80% 임계치), PDB(PodDisruptionBudget)로 자발적 중단 한계 설정, Graceful Shutdown(preStop hook, 30s) |
| **Data Tier (Stateful)** | 데이터 영속성·정합성 보장 | 동기식 복제(RPO=0, MySQL Group Replication, Galera), 비동기식 복제(RPO=수초~분, MySQL Binlog, PostgreSQL Streaming), Quorum 기반 리더 선출(Paxos/Raft) |
| **Cache Tier** | DB 부하 경감 및 읽기 가용성 향상 | Redis Sentinel(자동 페일오버, 30초), Redis Cluster(샤딩, 16,384 해시 슬롯), Memcached(다중 노드, Consistent Hashing), 다층 캐시(L1: Caffeine, L2: Redis) |
| **Message Queue** | 비동기 처리·버퍼링·재시도 보장 | Kafka(ISR(In-Sync Replica) 최소 2, acks=all), RabbitMQ(Mirror Queue, Quorum Queue), At-least-once / Exactly-once 시맨틱 |
| **Observability** | SLI 측정·장애 탐지·근본 원인 분석 | 3대 축: Metrics(PromQL), Logs(Loki/ELK), Traces(OpenTelemetry/Jaeger). SLI 예: p99 Latency < 200ms, Error Rate < 0.1% |
| **Chaos Engineering** | 장애 주입을 통한 가용성 사전 검증 | Netflix Chaos Monkey(인스턴스 랜덤 킬), Gremlin(네트워크·리소스 공격), LitmusChaos(K8s 네이티브), AWS Fault Injection Service |
| **Circuit Breaker** | 연쇄 장애(Failure Cascade) 차단 | Resilience4j/Hystrix, Closed->Open->Half-Open 상태 전이, 50% 실패율 10초 윈도우 시 Open, 30초 후 Half-Open |

심화 내용: **가용성 9(Nines)별 시스템 설계 차이**는 매우 큽니다. 99.9% 수준은 Active-Passive + 자동 페일오버(수 분)로 달성 가능하지만, 99.99%는 다중 리전 + 데이터 동기화 + 무중단 배포 + 카오스 테스트가 필수이며, 99.999%(5-nines)는 항공 관제·원자력·증권 거래소급으로 모든 단일 장애가 "예
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 537 / 600

<- **이전**: [536. 회귀 테스팅 자동화 전략 효율화](/studynote/11_design_supervision/06_exam_summary/536_regression_testing_automation_strategy)
**다음**: [538. 형상 관리 버전 제어 변경 추적](/studynote/11_design_supervision/06_exam_summary/538_configuration_management_version_control/) ->

---
