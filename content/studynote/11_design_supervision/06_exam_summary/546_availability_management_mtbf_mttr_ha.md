+++
title = "546. 가용성 관리 MTBF MTTR 고가용성 (Availability Management MTBF MTTR HA)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가용성(Availability)은 `A = MTBF / (MTBF + MTTR)` 공식으로 정의되며, MTBF(평균 고장 간격)를 늘리고 MTTR(평균 수리 시간)을 줄이는 것이 곧 고가용성(HA) 설계의 두 축이다. SPOF(단일 장애점) 제거, 이중화(Redundancy), 페일오버(Failover), 데이터 복제(Replication)가 4대 핵심 메커니즘으로 작동한다.
> 2. **가치**: SLA 99.99%(Four 9s) 기준으로 연간 52.56분의 다운타임을 허용하며, 99.999%(Five 9s)는 5.26분으로 금융·공공·원자력 등 미션 크리티컬 시스템의 운영·법적·평판 리스크를 직접적으로 결정한다. 가용성 1% 향상은 매출 손실, 페널티, 고객 이탈 비용의 수십억 원 절감과 직결된다.
> 3. **판단 포인트**: Active-Active vs Active-Passive, 동기(Synchronous) vs 비동기(Asynchronous) 복제, RTO/RPO 목표치, CAP 정리 기반의 트레이드오프(일관성 vs 분할 허용성), 그리고 비용 곡선(가용성 99.9%->99.99%는 비용 10배 증가)을 종합적으로权衡해야 한다.

---

## Ⅰ. 개요 및 필요성

정보시스템이 24×365 무중단 서비스를 제공해야 하는 시대에서, **가용성 관리(Availability Management)** 는 ITIL Service Design 단계의 핵심 프로세스로, 비즈니스 요구에 부합하는 서비스 가용 수준을 정의·측정·개선하는 체계적 활동이다. 전통적인 단일 서버 아키텍처(SPOF 100%)는 하드웨어 장애 시 100% 서비스 중단으로 이어지며, IDC 보고에 따르면 downtime 1시간당 금융사는 약 5억~10억 원, 전자상거래는 약 1억~3억 원, B2B SaaS는 약 50만~200만 달러의 손실을 입는다. 이로 인해 클라우드 네이티브 환경(Kubernetes, Multi-AZ, Multi-Region)에서도 HA는 선택이 아닌 필수 요건이 되었다.

가용성 관리는 단순한 "서버 이중화"를 넘어 **사람·프로세스·기술**의 통합 접근을 요구한다. 모니터링·알람 체계, 표준 운영 절차(SOP), 인시던트 매니지먼트, 변경 관리(Change Management), 용량 관리(Capacity Management)와 연계되어야 비로소 SLA를 안정적으로 달성할 수 있다.

```text
+--------------------------------------------------------------------+
|                서비스 가용성 타임라인 (Availability Timeline)        |
|                                                                    |
|  +-MTBF(평균 고장 간격)--++-MTTR(평균 수리 시간)-+                  |
|  |  정상 가동 구간       | | 장애~복구 구간      |                  |
|  |  ████████████        | | ░░░░░               |                  |
|  |  1000시간            | | 4시간               |                  |
|  |                      | |                     |                  |
|  |  --- 장애 발생 --->  v                     v 다음 고장까지    |
|  |                       ^ 복구 완료                              |
|                                                                    |
|  가용성(Availability) = MTBF / (MTBF + MTTR)                       |
|                      = 1000 / (1000 + 4) = 99.60%                 |
|                                                                    |
|  ※ Five 9s (99.999%) 목표: MTBF 5,256,000h / MTTR ≤ 5.26min       |
+--------------------------------------------------------------------+
```

**📢 섹션 요약 비유**: 가용성 관리는 마치 **종합병원의 응급실 운영**과 같다. 평소엔 한가해도(Green Day) 사고가 터지면(Green Day) 1분 1초가 생명을 좌우한다. 응급실 자체(MTBF, 정상 가동)가 견고해야 하고, 환자가 들어왔을 때 처치 속도(MTTR)가 빨라야 한다. 의사·간호사·장비·혈액망이 모두 **다중화된 백업 체계**로 갖춰져야 24시간 빈틈없는 진료가 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

가용성 아키텍처는 **"이중화(Redundancy) + 자동화(Automation) + 관측(Observability)"**의 3박자로 구성된다. 가장 보편적인 **Active-Passive(또는 Active-Active) HA 클러스터** 구조는 다음과 같다.

```text
                  +------- DNS / GSLB -------+
                  |   (Anycast / Geo-DNS)    |
                  +----------+---------------+
                             |
                  +----------v---------------+
                  |   L4/L7 Load Balancer   |
                  | (F5 BIG-IP, HAProxy,     |
                  |  AWS ALB, Nginx Plus)    |
                  +--+------------------+----+
                     | Health Check      | Health Check
          +----------v------+    +------v--------+
          |  Node A (Active)|◄--►| Node B (Standby)|
          |  - App/DB       | VRRP/Heartbeat | - App/DB idle  |
          |  - VIP 소유     |    | - VIP 대기     |
          +------+----------+    +------+---------+
                 | (동기 복제)           |
                 |     SAN/DRBD/iSCSI/  |
                 |     RDS Multi-AZ     |
                 v                      v
       +--------------------------------------+
       |  Shared Storage / DB Replication     |
       |  (Quorum/Witness 포함)               |
       +--------------------------------------+
                          |
                  +-------v--------+
                  |  DR Site       |
                  |  (Cross-Region |
                  |   Standby)     |
                  +----------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Load Balancer / L4 Switch** | 트래픽 분산 및 Health Check 기반 라우팅 | F5 BIG-IP(상태 확인 주기 1~3초), HAProxy(server health check), Nginx Plus, AWS ALB/ELB. 알고리즘: Round Robin, Least Connections, IP Hash, Weighted RR. |
| **HA Cluster Manager** | 노드 간 상태 감지·페일오버 오케스트레이션 | Linux: Pacemaker + Corosync(QUORUM 합의), Keepalived(VRRP), Heartbeat. Windows: WSFC(Windows Server Failover Cluster). DB: Oracle RAC, MySQL MHA, PostgreSQL Patroni, MongoDB ReplicaSet. |
| **Replication / Storage** | 데이터 정합성 보장 및 RPO 결정 | **동기(Sync)**: 커밋 시 양쪽 디스크 기록 확인, RPO=0, 지연^ (Infiniband, SRDF, AWS Aurora 6-way sync). **비동기(Async)**: 커밋 후 비동기 전파, RPO=초~분, 지연v, DR 사이트에 적합. **반동기(Semi-sync)**: MySQL 5.7+, 1대 Slave ACK 후 커밋. |
| **Monitoring / Observability** | 장애 탐지·SLA 측정·사후 분석 | Prometheus + Alertmanager, Zabbix, Datadog, Elastic APM, PagerDuty, Opsgenie. 핵심 메트릭: MTTD(평균 탐지 시간), MTTA(평균 인지 시간), MTTR. |
| **Runbook / Automation** | 반복 장애 대응 자동화 | Ansible, Terraform, Rundeck, ArgoCD(GitOps). 자동 페일오버 시퀀스: VIP 이동 -> 복제본 승격 -> DNS 갱신 -> 트래픽 재라우팅. |

### 핵심 산식 및 지표

- **가용성 (Availability)**: `A = MTBF / (MTBF + MTTR)`
- **연간 허용 Downtime (Downtime/year)**: `(1 - A) × 365 × 24 × 60` 분
- **MTBF(Mean Time Between Failures)**: 가동 시간 ÷ 장애 횟수. IEC 61709, SR-332, MIL-HDBK-217로 산정.
- **MTTR(Mean Time To Repair/Recover)**: `MTTR = MTTD + MTTI + MTTP + MTTV` (Detect+Identify+Process+Verify).
- **RTO(Recovery Time Objective)**: 재해 후 서비스 복구까지 목표 시간.
- **RPO(Recovery Point Objective)**: 재해 시 손실 허용 데이터량(시간 단위).
- **SLO/SLA**: SLO 99.95% / SLA 99.9%처럼 **1단계 여유** 두는 것이 업계 관행.
- **가용성 등급표 (Tier)**:
  - 99% (Two 9s) -> 3.65일/년 — 단일 시스템
  - 99.9% (Three 9s) -> 8.77시간/년 — Active-Passive
  - 99.95% -> 4.38시간/년 — Active-Active + DR Drill
  - 99.99% (Four 9s) -> 52.56분/년 — Multi-AZ + Auto-Failover
  - 99.999% (Five 9s) -> 5.26분/년 — Multi-Region Active-Active + 검증된 DR

### 페일오버 메커니즘 상세

**VRRP(Virtual Router Redundancy Protocol, RFC 5798)**: Master/Backup 라우터가 224.0.0.18 멀티캐스트로 1초 간격 Advertisement 교환, 3회 미수신 시 Backup이 Master로 승격. 우선순위(Priority 1~254)와 Preemption 옵션으로 결정. Linux `keepalived`가 대표 구현체.

**Quorum(쿼럼) 기반 페일오버**: 클러스터 노드 과반수(>50%)의 합의가 있어야 페일오버 실행. **Split-Brain**(네트워크 단절로 양쪽 모두 Master 자처) 방지를 위해 Witness/Arbiter 노드, STONITH(Shoot The Other Node In The Head), fencing 메커니즘 필수. AWS EC2는 `stop-terminate` 방지로, On-Prem은 IPMI/iLO/iDRAC 전원 차단으로 STONITH 구현.

**📢 섹션 요약 비유**: HA 아키텍처는 **쌍발기 엔진의 이륙 절차**와 같다. 한쪽 엔진이 꺼져도(Master 장애) 자동 시동 장치(Heartbeat)가 다른 쪽 엔진(Standby)을 즉시 점화하고, 관제탑(Load Balancer)이 항공기의 위치를 추적해 관제 신호를 재라우팅한다. 엔진이 동기적으로 추력(Sync Replication)을 맞춰야 흔들림 없이 직진하고, 관제탑과 조종사 사이의 통신(Heartbeat)이 끊기면 **Split-Brain**(두 사람이 같은 비행기를 동시에 조종하는 상황)이라는 재앙이 발생한다.

---

## Ⅲ. 비교 및 연결

가용성 관련 개념들은 서로 보완적이면서도 미묘한 차이가 있어, 설계 시 정확한 구분이 필요하다.

| 구분 | **Active-Passive(Hot Standby)** | **Active-Active(Load Sharing)** | **DR Site(Disaster Recovery)** | **Backup(Cold Standby)** |
| :--- | :--- | :--- | :--- | :--- |
| **리소스 활용도** | Standby 50% 유휴, 자원 낭비 | 양쪽 모두 부하 분산, 활용 90%+ | 평소 유휴, 평시엔 보고/테스트용 | 평소 0% 가동, 수동 복구 |
| **페일오버 시간** | 10~30초 (Auto) | 0~5초 (즉시 재분배) | 수 분~수 시간 (DNS/GSLB 의존) | 수 시간~수 일 |
| **데이터 정합성** | 동기 복제 시 RPO=0 가능 | 양쪽 쓰기 -> Conflict 발생 가능 | 비동기 -> RPO=분~시간 단위 | 스냅샷 -> RPO=시간~일 |
| **적합 워크로드** | RDBMS, Stateful Stateful 서비스 | Stateless API, 캐시, CDN | BCP/DRP 대상 전 시스템 | 개발/테스트, 비핵심 백업 |
| **비용 곡선** | 중간 (Standby 1대) | 높음 (2배 처리량) | 매우 높음 (지리적 이중화) | 낮음 (가끔만 기동) |
| **대표 기술** | Oracle Data Guard, SQL Server AG, MHA | MySQL Group Replication, Galera, Cassandra, Kafka | SRDF, S3 Cross-Region Replication, Azure Site Recovery | Veeam, NetBackup, Amanda |

| 구분 | **MTBF vs MTTR** | **SLO vs SLA** | **RTO vs RPO** | **HA vs DR vs BCP** |
| :--- | :--- | :--- | :--- | :--- |
| **정의** | MTBF=가동 신뢰성, MTTR=복구 속도 | SLO=내부 목표, SLA=고객 계약 | RTO=복구 시간, RPO=데이터 손실 | HA=시스템, DR=사이트, BCP=사업 |
| **측정 단위** | 시간(h), 건 | 가용성(%) | 시간(분), 데이터(MB) | 계획·정책 |
| **담당** | SRE/Infra | PM/Service Manager | DR Manager | CIO/위기관리 |
| **예시** | MTBF 8,760h, MTTR 2h | SLO 99.95%, SLA 99.9% | RTO 1h, RPO 15min | HA: 서버이중화, DR: IDC이전, BCP: 본사 화재 시 |
| **개선 방법** | 고품질 HW, 예방정비 | 자동화, 다중리전 | 동기복제, 빈번 스냅샷 | 거버넌스, 훈련, 매뉴얼 |

### 연계 기술·프레임워크

- **ITIL 4**: Availability Management -> Incident Management -> Problem Management -> Change Enablement. AIMS(Availability, IT Service Continuity, Capacity) 가이드라인.
- **SRE(Service Reliability Engineering)**: Google SRE Workbook의 **Error Budget** 개념 — SLO 99.9%면 연간 43.8분의 에러 예산을 부여하고, 예산 소진 시 신규 배포 동결.
- **CAP 정리**: 분산 시스템에서 **일관성(C) vs 가용성(A) vs 분할 허용성(P)** 중 2가지만 선택. CP 시스템(예: HBase, MongoDB 강한 일관성 모드)은 P 발생 시 가용성 양보, AP 시스템(예: Cassandra, DynamoDB)은 일관성 양보.
- **Observability 3요소**: Metrics(Prometheus
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 546 / 600

<- **이전**: [545. 용량 관리 수요 예측 확장 계획](/knowledge-base/studynote/11_design_supervision/06_exam_summary/546_capacity_management_demand_forecasting/)
**다음**: [547. IT 자산 관리 라이프사이클 최적화](/knowledge-base/studynote/11_design_supervision/06_exam_summary/547_it_asset_management_lifecycle_optimizati/) ->

---
