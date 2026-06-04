---
title: "424. 형상 관리 CMDB 구성 항목 관리 (Configuration Management CMDB CI)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CMDB는 ITIL V2/V3/V4의 SACM(Service Asset & Configuration Management) 프로세스가 운영하는 단일 진실 공급원(SSOT, Single Source of Truth)으로서, CI(Configuration Item)와 CI 간 관계(CI Relationship)를 식별·제어·기록·감사하는 ITSM 핵심 데이터 저장소이다. ServiceNow CMDB, BMC Helix CMDB, Ivanti Asset Manager 등이 이를 구현한다.
> 2. **가치**: 잘 구축된 CMDB는 MTTR(평균 복구 시간)을 30~50% 단축하고, 변경 실패율을 25% 감소시키며, 감사 및 컴플라이언스(ISO 20000, SOX, PCI-DSS) 대응 시간을 70% 이상 단축한다. Gartner에 따르면 Fortune 500 기업의 78%가 CMDB를 ITSM 운영의 핵심으로 사용한다.
> 3. **판단 포인트**: CMDB 설계 시 가장 중요한 결정은 (1) 단일 CMDB 통합 vs Federation 아키텍처, (2) 자동 디스커버리 우선 vs 수동 등록 우선, (3) Identified vs Authorized vs Audited CI의 단계적 도입, (4) 관계 데이터 모델(Relationship Cardinality)의 정의 범위, (5) EOL(End-of-Life)된 CI의 보관/아카이빙 정책이다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 환경에서는 시스템 인벤토리를 Excel, Visio, 메모장 등 비정형 문서로 관리했다. 이로 인해 장애 발생 시 "어떤 서버가 어떤 서비스를 지원하는지", "변경 영향 분석에서 어떤 애플리케이션이 영향을 받는지"를 파악하는 데 평균 4~6시간이 소요되었다. CMDB(Configuration Management Database)는 이러한 문제를 해결하기 위해 1980년대 말 ITIL V1에서 처음 등장한 개념으로, 2000년대 ITIL V2에서 "Configuration Management"로 정식 프로세스화되었다.

현대 IT 환경은 하이브리드 클라우드, 마이크로서비스, 컨테이너, IaC(Infrastructure as Code)로 급변하면서 CMDB의 역할이 더욱 중요해졌다. AWS EC2 인스턴스, Azure VM, Kubernetes Pod, OpenShift Deployment 같은 동적 자원은 수 분 단위로 생성·소멸하므로, 전통적인 수동 등록 방식으로는 CMDB의 데이터 정확성을 유지할 수 없다. ServiceNow CMDB는 2019년 CMDB Health Dashboard를 도입하여 CI당 평균 정확도(CMDB Health Score)를 측정하고, BMC Helix ITSM은 2022년 Discovery 22.x에서 멀티클라우드 자동 인벤토리 수집 기능을 강화했다.

형상 관리의 대상은 단순한 서버/네트워크 장비뿐 아니라 라이선스, 문서, SLA 계약, 심지어 서비스 카탈로그 항목까지 확장된다. 이를 **CI(Configuration Item)**라고 하며, 각각의 CI는 고유한 식별자(예: ServiceNow의 Sys_id, BMC의 ClassId+InstanceId)와 속성(Attribute), 그리고 다른 CI와의 관계(Relationship)를 가진다.

```text
+---------------------------------------------------------------------+
|                    현대 IT 환경의 CMDB 필요성                         |
+---------------------------------------------------------------------+

[Legacy 환경]                          [Modern CMDB 환경]
+--------------+                       +------------------+
| Excel 인벤토리 | --증식--> 수동추적   |  자동 Discovery    |
| (변경 지연)   |      지옥        |  + Federation     |
+--------------+                       |  + 관계 그래프      |
                                       |  + CMDB Health    |
+--------------+                       +------------------+
| Visio 다이어그램|                        ^
| (구버전 잔존)  |                        |
+--------------+                        |
                                        |
+--------------+                        | 자동 동기화
| 개별 시스템 DB| -------CMDB Federation --+
| (Active Directory, |       |       |
|  vCenter, AWS)   |       |       |
+--------------+      +----+----+  ++--------+
                       | ServiceNow|  | BMC Helix|
                       |   CMDB    |  |   CMDB   |
                       +----------+  +---------+
```

- **📢 섹션 요약 비유**: CMDB는 마치 병원의 **전자의무기록(EHR)**과 같다. 환자의 모든 진료 이력, 처방, 알레르기, 가족력을 한 곳에 통합해 두면 응급실에서도 즉시 정확한 치료가 가능하지만, 산부인과·내과·외과 기록이 따로 흩어져 있으면 의사들은 매번 "어떤 약을 먹었나요?"라고 물어야 한다. CI는 환자 정보, 관계(Relationship)는 진료과 간 협진 기록에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CMDB는 크게 4계층 아키텍처로 구성된다: (1) **Data Layer**(실제 CI 데이터 저장), (2) **Integration Layer**(외부 시스템에서 데이터 수집), (3) **Reconciliation Layer**(중복/충돌 데이터 정제), (4) **Presentation/API Layer**(CMDB 조회 및 활용).

핵심 데이터 모델은 **CIs**와 **Relationships** 두 가지 엔터티로 구성된다. ServiceNow의 CMDB는 17,000개 이상의 CI Class를 제공하며(예: cmdb_ci_server, cmdb_ci_appl, cmdb_ci_db_instance), 상속 계층을 통해 계층적 속성을 관리한다. 예를 들어 `cmdb_ci_server`는 `cmdb_ci_computer`를, `cmdb_ci_computer`는 `cmdb_ci_hardware`를 상속받아 공통 속성(IP, hostname, serial_number 등)을 공유한다.

```text
+-------------------------------------------------------------+
|                 CMDB 4-Layer 아키텍처                         |
+-------------------------------------------------------------+

+-------------------------------------------------------------+
|  Layer 4: Presentation & API Layer                          |
|  +------------+ +------------+ +------------+ +----------+ |
|  |  CMDB UI   | |  REST API  | | GraphQL    | | CMDB Health| |
|  |  (Visualize)| |  (Table API)| |  Query     | |  Dashboard| |
|  +------------+ +------------+ +------------+ +----------+ |
+--------------------------^----------------------------------+
                           |
+--------------------------+----------------------------------+
|  Layer 3: Reconciliation & Normalization Engine              |
|  +------------------------------------------------------+  |
|  |  Identification Rules: 동일 CI 매핑 (I&T, IP+DNS)     |  |
|  |  Reconciliation: 충돌 시 우선순위 (Authoritative Src)   |  |
|  |  Deduplication: 중복 CI 병합                          |  |
|  +------------------------------------------------------+  |
+--------------------------^----------------------------------+
                           |
+--------------------------+----------------------------------+
|  Layer 2: Discovery & Integration Layer                      |
|  +----------+ +----------+ +----------+ +----------------+  |
|  | Agentless | | Agent-   | | API-based | | Event-driven  |  |
|  | Discovery | | based    | | Pull      | | (Kafka/Queue)  |  |
|  | (Nmap,    | | (Tachyon, | | (AWS,Azure| |                |  |
|  |  SNMP,    | |  ServiceNow| |  vCenter) | |                |  |
|  |  WMI)     | |  Agent)   | |           | |                |  |
|  +----------+ +----------+ +----------+ +----------------+  |
+--------------------------^----------------------------------+
                           |
+--------------------------+----------------------------------+
|  Layer 1: Data Layer (CMDB Storage)                          |
|  +------------+  +------------+  +----------------------+  |
|  |  CMDB CI   |  |  Relations |  |  Audit & History     |  |
|  |  Table     |  |  Table     |  |  (Updated, By, When) |  |
|  | (cmdb_ci)  |  |(cmdb_rel_  |  |  + Versioning        |  |
|  |            |  |  ci)       |  |                      |  |
|  +------------+  +------------+  +----------------------+  |
|  RDBMS (MySQL, MSSQL, Oracle) / GraphDB (Neo4j 옵션)         |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CI (Configuration Item)** | 관리 대상의 최소 단위 | ServiceNow `cmdb_ci` 테이블, BMC `BMC.CORE:BMC_ConfigurationItem`. 4대 CI 유형: Hardware CIs(서버, 스토리지, 네트워크), Software CIs(앱, OS, DB), Service CIs(비즈니스 서비스), People/Org CIs(사용자, 부서). 각 CI는 `class` 속성으로 분류되고, `name`(식별명), `serial_number`(시리얼), `asset_tag`(자산번호), `operational_status`(Operational/Non-Operational/Disposed) 등의 속성을 가진다. |
| **CI Relationship** | CI 간 의존성 및 연결 표현 | `Runs on::Runs`(앱->서버), `Connects to::Connected to`(서버↔스위치), `Depends on::Used by`(서비스->앱), `Installed on::Contains`(OS->서버). ServiceNow은 `cmdb_rel_ci` 테이블에 `(parent, child, type, additional_attributes)` 형태로 저장하며, Cardinality(1:N, N:M)와 Containment 여부(`type.contains = true/false`)로 구분한다. |
| **Discovery Tool** | 자동화된 CI 식별·수집 | ServiceNow Discovery(Mid-Server 기반, SNMP/WMI/SSH/API), BMC Helix Discovery(전 BMC ADDM), ManageEngine Endpoint Central, Qualys, Tanium, Lansweeper. Agentless 방식은 Nmap/SSH/SNMP 프로토콜 스캔, Agent-based는 Windows WMI, Linux SystemD 서비스 모니터링. AWS/Azure는 CloudWatch/Azure Monitor API로 메타데이터 Pull. |
| **Reconciliation Engine** | 동일 CI 식별 및 중복 제거 | Identification Rule을 통해 동일성 판별. ServiceNow의 IET(Identification and Reconciliation Engine)은 `IP+MAC`, `Serial+Model`, `Name+Class` 등의 Rule을 평가하여 매칭. 충돌 시 **Authoritative Source** 우선순위로 승격. 예: AWS API(우선순위 100) vs SCCM(우선순위 50). |

**CI 라이프사이클과 상태 모델**은 5단계로 구분된다: `Identified`(디스커버리로만 발견) -> `Registered`(공식 등록) -> `Authorized`(변경 승인 후 운영) -> `Audited`(정기 검토 완료) -> `Disposed`(폐기). 이 상태 전이(State Transition)는 ITIL Change Management 프로세스와 강하게 결합되어 있다. ServiceNow의 `cmdb_ci_lifecycle_stage` 필드는 `Request Received`, `Request Approved`, `Being Built`, `In Production`, `Decommissioned`로 구성된다.

**자동 디스커버리 우선순위**는 일반적으로: (1) Cloud Provider API(가장 정확, 즉시 반영) -> (2) Hypervisor API(vSphere, Hyper-V) -> (3) CMDB Agent(설치된 경우) -> (4) Network Discovery(SNMP, WMI) -> (5) Manual Entry. 이 우선순위가 곧 **Authoritative Source**의 정당성이 된다.

- **📢 섹션 요약 비유**: CMDB는 **도서관의 카탈로그 시스템**과 같다. Discovery는 신간이 자동 등록되는 시스템, Reconciliation Engine은 같은 책의 여러 판본(양장본, 전집, 양장 신판)을 하나로 합쳐주는 사서, Relationship은 "이 책은 OO 시리즈의 3권입니다"라는 참조 관계이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **ServiceNow CMDB** | **BMC Helix CMDB** | **Ivanti CMDB** | **Open Source(Glpi/iTop)** |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | SaaS 중심, 단일 CMDB (CSDM 기반) | Federated CMDB (BMC.CORE:CMDB + Atrium) | On-premise 중심, Asset-IT 통합 | RDBMS 백엔드, 자체 스키마 |
| **디스커버리** | ServiceNow Discovery + IntegrationHub | BMC Helix Discovery(전 ADDM), TrueSight | Ivanti Neurons for Discovery | OCS Inventory, FusionInventory |
| **CI Class 수** | 17,000+ (CSDM 4+ 권장) | BMC Class Hierarchy, 약 12,000+ | 비교적 단순 (Asset/IT 분리) | 제한적(직접 정의) |
| **관계 모델** | cmdb_rel_ci + Cardinality | BMC_Component + Dependency | Relationship 테이블 (단순) | Links 테이블 |
| **강점** | 생태계, SaaS, 자동화 워크플로우 | 엔터프라이즈 통합, ITSM AIOps | Endpoint Security 통합 | 무료, 커스터마이징 자유 |
| **약점** | 고가(연 1억+), 종속성 | 구현 복잡도 높음, 라이선스 비쌈 | SaaS 전환 늦음 | 엔터프라이즈 기능 부족 |
| **적합 규모** | 500명 이상 엔터프라이즈 | 대기업, 금융/통신 | 100~1,000명 중소~중대 | 50~200명 중소기업 |

**다른 ITSM 프로세스와의 연결**:
- **Incident Management** -> CI 참조. "Application X 다운" Incident는 CMDB에서 `cmdb_ci_appl`을 조회하여 `Runs on::Runs` 관계로 영향받는 서버, DB, 네트워크 자동 식별 -> 자동 Major Incident 승격
- **Change Management** -> Change Request가 승인되면 해당 CI의 `operational_status`를 변경, 변경 후 자동 Discovery로 검증
- **Problem Management** -> Known Error DB와 CI 연결. 특정 CI에서 반복 장애 발생 시 RCA(Root Cause Analysis) 시 "Affected CI" 자동 나열
- **Asset Management** -> 라이선스 CI(Adobe, MS Office)와 사용자 CI, 디바이스 CI 연결하여 "사용자 A가 사용 중인 모든 SW 라이선스" 추적
- **Monitoring/ Observability** -> Prometheus, Datadog, Dynatrace에서 발생하는 알람을 CMDB의 `cmdb_ci_app_server`에 매핑 -> 알람 발생 시 즉시 관련 팀에게 알림

**CMDB Federation vs 통합 CMDB**:
- **Federation**: 각 도메인별 CMDB(네트워크, 서버, 앱)가 독립 운영되고, 마스터 CMDB가 가상 통합 뷰 제공. ServiceNow CMDB Federation(원격 인스턴스 조회), BMC Federated CMDB.
- **통합 CMDB**: 모든 CI를 단일 저장소에 저장. 데이터 일관성 ^, 단일 실패점(SPOF) 위험 ^.
- 실무 권장: **단계적 통합**(CSDM(CMDB Service Model) 기반 핵심 서비스 CI부터 통합 -> 점진적 확대).

- **📢 섹션 요약 비유**: ServiceNow는 **iPhone의 통합 생태계**(잘 작동하지만 종속), BMC는 **Windows PC의 모듈형**(유연하지만 조립 필요), Open Source는 **라즈베리파이**(무료지만 DIY 정신 필요).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **CSDM (Common Service Data Model) 도입 여부**: ServiceNow 2020년 이후 CSDM 4+ 기반으로 Business Service -> Service Offering -> Application Service -> Technical Service -> Infrastructure CIs 계층을 정의했는지 확인. 미적용 시 BSM(Business Service Mapping)이 불가능하여 "업무 영향도" 분석 실패.

2. **CI Class 정의 범위**: 너무 적으면(예: 10개) -> 세분화 부족으로 관계 표현 불가. 너무 많으면(예: 100개+) -> 데이터 중복, 유지보수 부담. 일반적으로 엔터프라이즈는 30~50개 핵심 Class로 시작 후 점진 확장.

3. **Discovery 범위와 빈도**: 일일 Discovery vs 주 1회 vs 이벤트 기반. 일일이 정밀하지만 부하 ^, 주 1회는 빠르지만 정확도 v. 권장: **Cloud/Container는 5분 단위, 일반 서버는 일 1회, 네트워크 장비는 주 1회**.

4. **Authoritative Source 정책**: 동일 CI 속성이 다를 때 어떤 소
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 424 / 800

<- **이전**: [423. IT 자산 관리 ITAM 라이프사이클](/studynote/12_it_management/05_security_compliance/423_it_asset_management_itam_lifecycle/)
**다음**: [425. 변경 관리 CAB 영향 분석 승인](/studynote/12_it_management/05_security_compliance/425_change_management_cab_impact_approval/) ->

---
