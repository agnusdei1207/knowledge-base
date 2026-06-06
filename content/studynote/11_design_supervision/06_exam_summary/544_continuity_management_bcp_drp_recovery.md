---
title: "Continuity Management BCP DRP Recovery"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 연속성 관리(BCM, ISO 22301)는 BIA·RA·BCP·DRP·테스팅을 하나의 PDCA 사이클로 통합하는 거버넌스 체계이며, DRP는 그 실행 산출물로 RTO/RPO를 SLA로 수치화하여 동기식/비동기식 스토리지 복제, DB 이중화(Oracle Data Guard, SQL Server Always On AG), DRaaS(AWS CloudEndure, Zerto, Azure Site Recovery)를 통해 데이터 손실 0초~수 분, 복구 시간 분 단위로 달성하는 기술적 회복 메커니즘이다.
> 2. **가치**: 한국 전자금융감독규정 제15조의2(전자금융기반시설의 안전성 확보), ISMS-P, 클라우드컴퓨팅법 제23조(재해복구), 그리고 금융·공공·의료 분야의 BCR/DRC 인증 의무화에 따라 미준수 시 과태료·과징금·업무정지 처분과 직결되며, DR 자동화·테스트 고도화 시 MTTR 70%v, 연간 다운타임 비용 평균 9,000만 원/시스템 절감(업계 벤치마크 기준) 효과를 제공한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① RPO=0을 위한 동기식 복제(거리 한계 약 200km, RTT 5ms 이내) vs 비용 효율적 비동기식(전송 지연·데이터 손실 허용), ② 핫사이트 Active-Active(고가·고복잡) vs 파일럿 라이트(저비용·콜드 스타트), ③ 클라우드 DRaaS(탄력성·종량제) vs 자가 DR 센터(데이터 주권·예측 가능성), ④ 테스트 빈도(연 2회 실전 모의훈련 vs 분기 1회 토의 시뮬레이션)의 4축을 BIA 결과와 비용 곡선으로 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)과 4차 산업혁명 이후, 기업의 핵심 자산은 더 이상 물리적 공장이 아닌 **데이터·서비스 가용성**으로 이동했다. IDC 보고에 따르면 글로벌 기업의 평균 다운타임 비용은 분당 8,000~25,000 USD 수준이며, 한국은 금융·공공 분야의 24×365 무중단 요구가 강화되면서 'BCM(사업연속성관리) 부재 = 경영 거버넌스 부실'이라는 인식이 정착되었다. 2017년 영국항공 IT 장애(데이터센터 전력 공급기 화재), 2021년 KBS·KT·이마트·SK 등 동시다발 사이버 공격·인프라 장애, 2023년 대한항공 알로하 사태가 BCM·DRP 투자를 가속화했다.

기술적 도전은 ① 멀티 하이브리드 클라우드 환경에서의 데이터 일관성, ② 랜섬웨어·DDoS 등 사이버 재해의 BCP 범위 편입, ③ RTO/RPO 0에 근접하는 Zero Trust + Active-Active 아키텍처 설계 복잡도, ④ 클라우드 종속 시 발생하는 리전 단위 광역 장애 대응, ⑤ IT-OT-물리 보안 융합 리스크(자연재해·전쟁·전염병) 등 5가지 축으로 수렴한다. 과거(mainframe+자가 DR센터 중심 단일 거점) 패러다임은 분산·가상화·클라우드 네이티브 패러다임으로 전환되었으며, 이는 "데이터는 복제되지만 비즈니스 프로세스는 복제되지 않는다"는 격차를 만들었다.

```text
[BCM 거버넌스 ↔ DRP 실행의 관계]
+--------------------------------------------------------------+
|   ISO 22301 / 22320 BCM 프레임워크 (경영 거버넌스)            |
|  +-------------------------------------------------------+   |
|  |  1. 정책·조직·리더십      2. BIA (Business Impact)    |   |
|  |  3. Risk Assessment       4. 전략 결정 (RTO/RPO)      |   |
|  |  5. BC 절차·DR 절차       6. 교육·인지·커뮤니케이션    |   |
|  |  7. 테스트·모의훈련        8. 검토·개선(PDCA)          |   |
|  +-------------------------------------------------------+   |
|                          |                                   |
|                          v (연결점)                          |
|  +-------------------------------------------------------+   |
|  |  DRP (Disaster Recovery Plan) - IT 실행 계획서         |   |
|  |  · 아키텍처(Active-Active / Pilot Light / Warm Standby)|   |
|  |  · 데이터 보호(Storage SR / DB Log Shipping / Snapshot)|   |
|  |  · 네트워크(DNS GSLB, Anycast, VPN 4-tunnel)           |   |
|  |  · 오케스트레이션(DRaaS, Runbook Automation)           |   |
|  |  · 검증(Chaos Engineering: AWS Fault Injection, Gremlin)|  |
|  +-------------------------------------------------------+   |
|                          |                                   |
|                          v                                   |
|  운영 환경: Tier-1 On-Prem DC ---> Tier-2 DR Site / Cloud     |
|            (Primary)              (Hot/Warm/Cold/Pilot)       |
+--------------------------------------------------------------+
```

기존 패러다임 대비 변화 양상은 ① 24시간 DR 사이트 운영에서 DRaaS 종량제로의 CapEx->OpEx 전환, ② 백업·복제·DR을 분리하던 영역을 CDP(Continuous Data Protection)와 통합, ③ 테스트가 실전 모의훈련에서 GameDay·Chaos Engineering으로 진화, ④ BCP 범위에 사이버 회복(Cyber Resilience) 및 공급망(3rd Party) 연동을 필수 포함시키는 점이다.

- **📢 섹션 요약 비유**: BCM이 회사의 종합비상매뉴얼이고 DRP는 그 매뉴얼의 "전산팀용 실전 기술 부록"이다. 종합 매뉴얼 없이 전산팀 기술만 있으면 경영 판단이 빠지고, 반대로 매뉴얼만 있고 기술이 없으면 명령을 내릴 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BCP/DRP의 핵심은 **BIA(Business Impact Analysis) -> 전략 결정 -> DR 아키텍처 -> 테스트·개선**의 4단 파이프라인이다. BIA에서는 핵심 업무(CSF, Critical Success Factor)를 식별하고 MTPD(Maximum Tolerable Period of Disruption) -> RTO -> RPO -> 최소 자원 산정 -> 비용 곡선 도출 순서로 정량화한다. RA(Risk Assessment)는 ISO 31000, NIST SP 800-30 기반으로 자연재해(지진·홍수), 기술 장애(하드웨어·소프트웨어), 인적 장애(휴먼 에러·내부 부정), 사이버 공격(랜섬웨어·DDoS), 외부 의존성(공급망·전력·통신), 팬데믹 6개 카테고리로 분류한다.

DR 아키텍처는 4-tier로 분류된다.
- **Tier-1 (Active-Active / Multi-Active)**: 두 개 이상의 DC가 동시 운영, GSLB(F5 BIG-IP DNS, AWS Route 53) 기반 트래픽 분산. RTO ≈ 0초, RPO ≈ 0초(동기식). 비용 최대.
- **Tier-2 (Active-Passive / Hot Standby)**: 보조 사이트가 상시 Warm 상태로 동기화, 장애 시 자동 Failover. VMware SRM, Zerto, Azure Site Recovery 활용. RTO 분 단위, RPO 0~수 초.
- **Tier-3 (Pilot Light)**: 핵심 데이터만 동기화, 컴퓨팅 자원은 On-Demand 기동. AWS CloudEndure, CloudEndure Disaster Recovery 패턴. RTO 10~60분, RPO 수 초~수 분.
- **Tier-4 (Warm/Cold Standby)**: 주기적 스냅샷/백업 복제, 장애 시 수동/반자동 복구. RTO 수 시간~수 일, RPO 수 시간.

데이터 복제 메커니즘은 동기식(쓰기 동시 양쪽 완료 후 ACK, 거리 ≤ 200km, RTT ≤ 5ms)과 비동기식(주 사이트 ACK 후 비동기 전송, 손실 가능, 거리 무관)으로 구분된다. 3-tier 복제(메모리->로컬 디스크->원격)·스토리지 레벨 복제(EMC SRDF, IBM PPRC/Global Mirror, Hitachi TrueCopy/Universal Replicator, HPE 3PAR Remote Copy)·DB 레벨 복제(Oracle Data Guard Maximum Protection/Availability/Performance 모드, SQL Server Always On AG Sync/Async, MySQL Group Replication, PostgreSQL WAL Streaming)·하이퍼바이저 레벨(Zerto Journal-based CDP, VMware vSphere Replication, Veeam CDP)·애플리케이션 레복(Active Directory 복제, SAP HANA System Replication) 다섯 계층이 있다.

```text
[DR Failover 시퀀스 다이어그램]
시간 ->  -------------------------------------------------►
        T0         T0+1s         T0+30s        T0+1m
        |          |             |             |
Primary | 정상 운영| 장애 감지    | 데이터      |  서비스
        |          | (HA/Fail)   |  동기화     |  전환완료
        |          v             v             |
        |      Monitoring    RPO=0 확인        |
        |      (Prometheus,  (DB/Storage      |
        |       Zabbix,      log shipping)    |
        |       CloudWatch)                   |
        |                                      v
        |                                Secondary
        |                                 정상 서비스
        |                                 시작
        |                                      |
        |  ------- Orchestration -------      |
        |   Runbook (Ansible/Terraform/        |
        |   AWS Systems Manager/Azure          |
        |   Automation/Rundeck) 자동 트리거     |
        |                                      |
        v
   GSLB (DNS TTL 60s) -> 사용자 트래픽 자동 라우팅
   F5 BIG-IP / Akamai Edge / Cloudflare Load Balancer
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| BIA 도구 | 업무 영향 정량화 | RiskLens, Avaloq, 자체 Excel-MonteCarlo 시뮬레이션. 임계값 결정: 4시간(CSF Tier-1), 24시간(Tier-2), 72시간(Tier-3) |
| 데이터 복제 엔진 | RPO 결정 | EMC SRDF/S(Metro Sync ≤ 200km, ≤ 5ms RTT), SRDF/A(Async, RPO 수 초~수 분), Oracle Data Guard Redo Apply/SQL Apply, AWS EBS Snapshot + S3 Cross-Region Replication(S3 CRR, RPO 15분), Azure Blob GRS/RA-GRS |
| 오케스트레이션 플랫폼 | RTO 결정 | Zerto Virtual Replication(Journal-based CDP, RPO ≈ 수 초, RTO 분), VMware Site Recovery Manager(vSAN Stretched Cluster, vSphere Replication), AWS CloudEndure(블록 레벨 연속 복제 + Pilot Light), Azure Site Recovery(ASR, Recovery Plan as Code), Veeam Backup & Replication(Instant VM Recovery) |
| 네트워크 페일오버 | 사용자 인지 최소화 | GSLB(F5 BIG-IP DNS, NS1, AWS Route 53 Traffic Flow, Azure Traffic Manager), Anycast IP, SD-WAN(Cisco Viptela, VeloCloud, Meraki) 4-tunnel ECMP, BGP AS-path Prepending 기반 트래픽 엔지니어링 |
| 검증 자동화 | 회복 신뢰도 확보 | AWS Fault Injection Service(FIS), Azure Chaos Studio, Gremlin, ChaosBlade, LitmusChaos(K8s). PagerDuty/Opsgenie 기반 GameDay |
| 거버넌스·정책 | 규정 준수·감사 추적 | ISO 22301/27001/27031, NIST SP 800-34 Rev.1, BCI Good Practice Guidelines(GPG) 2018, K-ISMS-P, 전자금융감독규정, PCI-DSS 12.10, SOC 2 CC7.5, GDPR Art.32(가용성) |

핵심 파라미터는 다음과 같이 정의된다.
- **RTO(Recovery Time Objective)**: 서비스 복구까지 허용 시간. 산식: `RTO = MTPD × (0.25 ~ 0.5)` (BCI 권장 마진)
- **RPO(Recovery Point Objective)**: 데이터 손실 허용량. 산식: `RPO = (백업 주기) + (복제 지연 시간) + (인덱싱·압축 지연)`
- **MTTR(Mean Time To Repair)**: 장애 감지->복구 평균. DR 자동화 시 MTTD(Mean Time To Detect) < 1분, MTTR < 15분 달성 가능 (SRE 4-golden signal 기반)
- **MAUM(Maximum Acceptable Outage Minutes)**: 연간 허용 다운타임 = ` (1 - 가용성 %) × 365 × 24 × 60` 예: 99.99% = 52.6분/년

아키텍처 선택 시 고려할 알고리즘·공식은 ① `비용 = (CapEx: DR 사이트 투자) + (OpEx: 대역·전력·라이선스) + (Lost Revenue: 다운타임 × 단가)` 최소화, ② `가용성 = MTBF / (MTBF + MTTR)` 시스템 신뢰도 모델, ③ RPO 0을 원할 때 `동기식 대역폭 = (변경량) × (압축 효율) × (overhead 1.4)`, 통상 OLTP DB의 경우 쓰기 1,000~10,000 IOPS × 8KB ≈ 8~80MB/s 요구 -> 전용선 100Mbps~1Gbps 필요.

- **📢 섹션 요약 비유**: DR 아키텍처를 자동차의 안전장치로 비유하면, Active-Active는 두 대의 차가 동시에 달리는 것이고, Pilot Light는 주 차가 고장나면 미리 시동을 걸어둔 예비 차가 즉시 출발하는 것이며, Cold Standby는 주차장에 있는 차를 사람이 직접 끌고 와서 시거를 꽂는 것에 가깝다.

---

## Ⅲ. 비교 및 연결

| 구분 | BCP (사업연속성계획) | DRP (재해복구계획) | BCM (연속성관리체계) | ITSCM (IT서비스연속성) |
| :--- | :--- | :--- | :--- | :--- |
| 정의 | 전사적·업무 중심 복구 계획 | IT 인프라·데이터 중심 복구 절차 | 조직 거버넌스·PDCA 체계 | IT 서비스 한정 연속성 |
| 범위 | 인적·물적·IT·공급망·대외 | 서버·스토리지·네트워크·DB·앱 | 전체 BCM 라이프사이클 | IT 조직·시스템·서비스 |
| 소유 부서 | CISO·COO·리스크 관리 | CIO·IT 운영·인프라 | 최고경영자·BCM 위원회 | IT 서비스 매니저 |
| 핵심 산출물 | BIA·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 544 / 600

<- **이전**: [543. 서비스 수준 관리 SLA SLO SLI](/studynote/11_design_supervision/06_exam_summary/543_service_level_management_sla_slo_sli)
**다음**: [545. 용량 관리 수요 예측 확장 계획](/studynote/11_design_supervision/06_exam_summary/545_capacity_management_demand_forecasting/) ->

---
