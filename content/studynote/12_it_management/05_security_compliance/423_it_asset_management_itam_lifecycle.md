---
title: "IT Asset Management ITAM Lifecycle"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITAM(IT Asset Management)은 조직의 하드웨어·소프트웨어·클라우드·데이터 자산을 **ISO/IEC 19770-1~5** 및 **ITIL 4 Asset Management Practice** 기반으로 **Plan -> Acquire -> Deploy -> Operate -> Refresh -> Retire** 6단계 라이프사이클에 걸쳐 식별·계량·최적화하는 거버넌스 체계이며, CMDB·FinOps·SAM·HAM·SaaS Management의 단일 통합 진실 원천(SSOT)을 형성한다.
> 2. **가치**: 전사적 ITAM 성숙도 1단계에서 4단계로 도약 시 평균 **TCO 23~30% 절감**, **소프트웨어 라이선스 과다 지출 15~20% 회수**, **Shadow IT 가시화 80%+ 달성**, **EoL/EoS 자산의 보안사고 60% 감소**(Gartner 2023 Asset Management Survey) 효과가 보고된다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ①Discovery 도구의 적극적 스캔(정확도 ^ vs 네트워크 부하·프라이버시 이슈), ②클라우드 지출 가시화를 FinOps로 분리 운영 vs ITAM 단일 통합, ③계약 단위 라이선스(per-seat/per-core/per-usage) 선택에 따른 최적화 알고리즘 차이, ④자동 폐기 워크플로의 NIST SP 800-88 Purge vs Clear vs Destroy 단계 결정이다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 자산 관리는 **재무 회계 관점의 "감가상각 대장"** 수준에 머물렀다. 그러나 ①**하이브리드·멀티클라우드 환경의 확산**(AWS·Azure·GCP·Naver Cloud·KT Cloud 자산의 동적 생성/소멸), ②**SaaS 구독 모델의 폭증**(평균 기업 SaaS 앱 200~300개, 직원이 인지하지 못하는 Shadow IT 30~40%), ③**원격·하이브리드 근무常态化**로 인한 EDR/EMM 대상 단말의 지리적 분산, ④**ESG 규제 강화**(EU CSRD, 한국 ESG 정보공시, Scope 3 탄소배출에 IT 폐기물 포함)이라는 4대 환경 변화로 인해, IT 자산은 단순한 "목록"이 아닌 **실시간 의사결정 의사결정(FinOps·SecOps·GreenOps)에 직접 투입되는 데이터 객체**로 격상되었다.

특히 **2024년 기준 글로벌 평균 데이터 유출 비용이 488만 USD**(IBM Cost of a Data Breach)로 사상 최고치를 경신하면서, EoL(End-of-Life) 하드웨어의 미폐기·미초기화, 미회수 Shadow SaaS 계정, 라이선스 초과 과다구매로 인한 재무 손실이 동시에 C-Level 리스크로 부상했다. ITAM은 이를 **단일 플랫폼에서 가시화·자동화·정책 통제**하기 위한 해법으로, IT 거버넌스의 최상위 계층에 위치한다.

```text
[ ITAM의 진화적 위치 — 과거 vs 현재 ]

   +----------------------------------+      +----------------------------------+
   |         [ 1990s~2000s ]          |      |            [ 2024+ ]             |
   |                                  |      |                                  |
   |   재무부서 -- 감가상각 스프레드시트|      |   CIO/CDO/CTO 단일 진실원천(SSOT)|
   |   IT운영 -- 수동 인벤토리(Excel)  |  ->   |   +- Hardware Asset(HAM)         |
   |   구매 -- PO/계약서 폴더         |      |   +- Software Asset(SAM)         |
   |                                  |      |   +- Cloud/SaaS (FinOps 연계)    |
   |   ⇒ 자산 = "회계 항목"            |      |   +- IoT/OT 자산                 |
   |   ⇒ 정확도 60~70%, 갱신주기 분기  |      |   +- 데이터·라이선스 자산        |
   +----------------------------------+      |                                  |
                                            |   ⇒ 자산 = "실시간 의사결정 데이터" |
                                            |   ⇒ 정확도 98%+, 갱신주기 분/시간  |
                                            +----------------------------------+
```

```text
[ ITAM 도입의 비즈니스 트리거(왜 지금인가) ]

  +----------------------+    +----------------------+    +----------------------+
  |  라이선스 컴플라이언스 |    |   클라우드 비용 폭증   |    |  사이버보안 사고      |
  |  +--------------+    |    |  +--------------+    |    |  +--------------+    |
  |  | BSA/BSA-K    |    |    |  | Shadow IT    |    |    |  | EoL 자산      |    |
  |  | SIIA 감사    |    |    |  | 멀티클라우드  |    |    |  | 미반환 단말   |    |
  |  | 계약 위반 과태료|    |    |  | FinOps 실패  |    |    |  | 자격증명 잔존 |    |
  |  +------+-------+    |    |  +------+-------+    |    |  +------+-------+    |
  +---------+------------+    +---------+------------+    +---------+------------+
            |                           |                           |
            +-------------+-------------+-------------+-------------+
                          v                             v
                  +----------------------------------------------+
                  |          ITAM 단일 플랫폼 요구                |
                  |   - 가시성(Visibility)·통제(Control)·최적화 |
                  |   - 자동화(Automation)·컴플라이언스(Compli.)|
                  +----------------------------------------------+
```

- **📢 섹션 요약 비유**: ITAM은 마치 **"대형 병원의 의료장비 통합관리시스템"**과 같다. 1990년대에는 엑셀로 "MRI 1대, CT 2대" 정도만 기록했지만, 지금은 **각 장비의 위치·가동률·예약·유지보수주기·교체주기·폐기 시 납 함유 폐수 처리까지** 실시간으로 추적·예측해야 한다. 자산이 곧 곧바로 환자 진료(매출)와 직결되기 때문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ITAM은 4계층 아키텍처(Discovery -> Reconciliation -> Repository -> Insight)로 구성되며, 각 계층은 표준 프로토콜·데이터 모델·거버넌스 정책으로 상호 연결된다.

```text
[ ITAM 4계층 참조 아키텍처 ]

  Layer 4: Insight & Optimization  ---------------------------------+
    +- 라이선스 최적화(ELA/True-up), TCO 모델링, What-if 시뮬레이션  |
    +- ESG/GreenOps Scope3 산정(EoL 탄소배출), FinOps showback     |
    +- KPI 대시보드: Utilization, Compliance %, $/user, EoL risk    |
  ------------------------------------------------------------------+
                                       ^
  Layer 3: Central Repository (CMDB / Asset DB)  -----------------+
    +- ServiceNow CMDB, BMC Helix CMDB, Atlassian Insight+CMDB   |
    +- 데이터 모델: CI(설정항목), Relationship Graph, Audit Log    |
    +- 통합: REST API, SOAP, JDBC, GraphQL, ETL(Fivetran/Airbyte)|
    +- 표준: CIsco CMDB Federation, CMDB Federation Schema v2.0  |
  ------------------------------------------------------------------+
                                       ^
  Layer 2: Normalization & Reconciliation Engine  ----------------+
    +- 다중 소스 데이터 매칭·충돌 해결(MDM↔Agent↔SaaS API)         |
    +- 중복 제거, 별칭 정규화(예: "NB-001" = "DELL-1234" = "자산 9")|
    +- 신뢰도 가중치(SIEM=0.9, Agent=0.85, 수동=0.6) 산정          |
    +- 이벤트 드리븰 갱신(예: Intune 신규 등록 시 자동 CI 생성)    |
  ------------------------------------------------------------------+
                                       ^
  Layer 1: Discovery & Collection Plane  -------------------------+
    +- Agent 기반: Intune/MECM, Jamf(Mac), Tanium, Qualys         |
    +- Agentless: SNMP/WMI, SSH/Nmap, AD/Azure AD, DHCP 로그      |
    +- 클라우드: AWS Config/Inspector, Azure Resource Graph, GCP CA|
    +- SaaS: SCIM/SSO(SAML/OIDC), 감사 로그, CASB(Netskope/Zscaler)|
    +- 네트워크: 스위치 ARP/MAC, 와이파이 컨트롤러, NAC(ISE/ClearPass)|
  ------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Discovery Agent** (Layer 1) | 단말 HW·SW·사용자·위치 식별 | `Tanium`, `Microsoft Intune/MECM`, `Jamf Pro`, `BigFix`. 폴링주기 15분~1시간, 하트비트 미수신 시 CMDB CI `Stale -> Retired` 자동 전환. 하드웨어 인벤토리 SMBIOS/DMI, 설치 SW 레지스트리/WMI, 사용자 Azure AD Join 토큰 조회 |
| **Cloud-Native Discovery** (Layer 1) | IaaS·PaaS 자산의 API 기반 수집 | `AWS Config` + `Systems Manager Inventory`, `Azure Resource Graph` + `Resource Graph Explorer`, `GCP Cloud Asset Inventory`. 5분 단위 델타 이벤트 스트리밍, Kinesis/EventBridge -> Lambda -> CMDB 파이프라인 |
| **SaaS Discovery & CASB** (Layer 1) | Shadow IT SaaS 사용량·계약 추출 | `Netskope`, `Zscaler ZIA`, `Microsoft Defender for Cloud Apps`. SWG 프록시 로그 분석, OAuth 토큰 인벤토리, 계약서 OCR(Natixs/Certify/Productiv). SCIM 2.0으로 사용자 라이프사이클 동기화 |
| **CMDB / Asset Repository** (Layer 2) | 자산 데이터 SSOT, 관계 그래프 | `ServiceNow CMDB` (CI Class: cmdb_ci_computer, cmdb_ci_spkg, cmdb_ci_cloud_account), `BMC Helix CMDB`, `Atlassian Insight`. 관계 모델: Runs on::Hosted on::Connected to::Owned by. 식별자: Serial No, MAC, IMEI, ARN, Resource ID |
| **Reconciliation Engine** (Layer 2) | 다중 소스 충돌 해결 | `ServiceNow Identification and Reconciliation Engine(IRE)`. 다단계 매칭: 정확 일치 -> 유사 매칭(퍼지) -> 사용자 주제. `CMDB Health Dashboard`로 정확도(confidence %) 시각화 |
| **Contract & License Mgr** (Layer 3) | 계약·엔타이틀먼트·사용량 추적 | `Flexera One`, `Snow Atlas`, `ServiceNow SAM Pro`, `Open iT`. 라이선스 모델별 계량: `per user`, `per core`(Oracle/UEE), `per processor`(MS SQL Std), `per instance`, `per VM`(SUSE/RHEL). True-up/다운 자동 계산 |
| **Workflow & Automation** (Layer 4) | 라이프사이클 이벤트 자동화 | `ServiceNow ITAM Lifecycle`, `Ivanti Neurons`, `BMC Helix ITSM`. 6단계 게이트: Plan 승인 -> Acquire PO -> Deploy Checklist -> Operate 패치 -> Refresh Refresh Window -> Retire NIST 800-88 |
| **Analytics & FinOps Hook** (Layer 4) | 비용·사용률·ESG 인사이트 | `Apptio Cloudability`, `Vantage`, `CloudHealth` + ITAM 데이터 조인. KPI: **Utilization %**, **$ per FTE**, **Waste %**, **Carbon Footprint(kgCO2e/asset·yr)**, **Compliance %** |

**핵심 알고리즘 및 파라미터** (기술사 빈출):
- **License Position 계산식**: `License Position = (Entitlement − Assignment) − Installed`. `Assignment`가 사용자 수, `Installed`가 실제 설치 수. 이 차이로 과다구매(Overspend)·과소구매(Underlicensed) 동시 판정.
- **TCO 모델**: `TCO = CapEx(초도) + Σ(OpEx) + Σ(End-of-Life Cost)`. OpEx 항목: 라이선스 유지비, 유지보수 계약, 전력(PUE × 24×365 × kW × 단가), 운영 인건비, 데이터센터 점유 면적.
- **자산 신뢰도 점수**: `Confidence = Σ(Source_weight × Freshness)`. 기본 가중치: Agent=0.85, Agentless=0.70, Manual=0.60, Contract=0.95. Freshness는 7일 이내는 1.0, 30일 0.7, 90일 0.4로 감쇠.
- **NIST SP 800-88 Rev.1 3단계 폐기**: ①**Clear**(논리적 덮어쓰기, ATA/SATA), ②**Purge**(크립토 Erase·디스크 자체 암호키 폐기, SSD/가상디스크), ③**Destroy**(물리적 파쇄, NIST 800-88 Appendix A Table A-1).
- **EoL 위험도**: `Risk = P(사고) × 임팩
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 423 / 800

<- **이전**: [422. IT 재무 관리 FinOps 비용 최적화](/studynote/12_it_management/05_security_compliance/422_it_financial_management_finops_cost/)
**다음**: [424. 형상 관리 CMDB 구성 항목 관리](/studynote/12_it_management/05_security_compliance/424_configuration_management_cmdb_ci/) ->

---
