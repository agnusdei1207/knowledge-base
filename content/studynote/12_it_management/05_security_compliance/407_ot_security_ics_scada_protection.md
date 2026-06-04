---
title: "407. OT 보안 산업 제어 시스템 SCADA (OT Security ICS SCADA Protection)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OT 보안은 ISA/IEC 62443 국제표준과 Purdue Reference Model(Level 0~5) 기반의 **Zoning & Conduit** 구조, **IDMZ(Industrial DMZ)** 이중화, 그리고 Modbus/TCP·DNP3·PROFINET·OPC UA 등 산업 프로토콜 특화 가시성·무결성·기밀성 확보로 정의되며, IT 보안의 CIA(Confidentiality-Integrity-Availability) 원칙을 **AIC(Availability-Integrity-Confidentialty)** 순서로 재배치해 Safety·Continuity를 최우선에 두는 도메인이다.
> 2. **가치**: Stuxnet(2010, 이란 원심분리기 1,000대 파괴), TRITON(2017, SIS 안전계통 직접 타겟), Colonial Pipeline(2021, 미국 동부 45% 연료공급 중단) 등 **산업제어시스템 침해가 인명·환경·국가기반시설에 직접적 피해**를 유발하는 사례를 근거로, IEC 62443-3-3 SL-3(Security Level 3) 달성 시 **평균 탐지시간(MTTD) 280일 -> 24시간 이내 단축**, **평균 복구비용 420만 USD -> 110만 USD 절감**(IBM 2023 Cost of Data Report 기준 OT 확장) 효과를 산출한다.
> 3. **판단 포인트**: 기술사적 핵심 trade-off는 ①Air-gap 유지 vs. IIoT 데이터 활용을 위한 **읽기 전용 미러링(TAP/SPAN) 기반 One-way Diode** 채택 여부, ②레거시 WinCC 7.0·RSView32 등 **미인증 OS 보호**(Whitelisting·Signature-based AV) vs. 노후 PLC 펌웨어 패치 적용의 **가용성 리스크**, ③NERC-CIP·NIS2·OT cybersecurity Act 등 **규제 컴플라이언스** 충족을 위한 Zone 분류 정밀도 결정이며, 이는 곧 **Safety·Security·Production** 3축 균형점의 엔지니어링 의사결정이다.

---

## Ⅰ. 개요 및 필요성

산업제어시스템(ICS: Industrial Control System)은 전력·수도·가스·화학·제조·교통·원자력 등 **국가 핵심기반시설(CNI: Critical National Infrastructure)** 의 두뇌이자 신경계로, 사이버 공격 시 단순 데이터 유출을 넘어 **물리적 파괴·환경오염·인명사고·국가경제 마비**로 직결된다. 2024년 기준 전 세계 OT 자산은 약 **230억 개**(IoT Analytics 2024)로 추산되며, 이 중 노출된 인터넷 facing 디바이스는 약 **15만 대**(Shodan, Claroty Team82 기준)로 약 73%는 **기본 인증 부재·텔넷 23/포트 개방·취약한 펌웨어 버전** 상태다. 한국은 2023년 9월 「산업기술보호법」 개정으로 **국가핵심기술 보유기업의 OT 자산 대상 정기 진단 의무화** 및 산업부·과기정통부 합동으로 **K-OT 보안인증제**를 2024년 본격 시행 중이다.

기존 IT 보안 패러다임("**경계는 안, 외부는 불신**")은 OT 환경에서 **3가지 본질적 모순**을 갖는다: 첫째, IT는 30~90일 패치 주기가 보편적이나, OT PLC는 **15~20년 평균 수명·연 1~2회 정지 점검**으로 패치가 사실상 불가. 둘째, IT 자산은 손상 시 데이터만 유출되나, OT는 **Modbus Coil 0x0001 쓰기 명령 한 줄로 원자로 냉각펌프·송전선 차단기·화학반응기 교반기를 직접 제어** 가능하다. 셋째, IT 가용성 목표 99.9%(연 8.7시간 장애)가 일반적이나, OT는 **99.99% 이상(연 52분 이내)·Safety-critical Loop는 99.999%**(연 5분 이내)가 요구된다.

```text
+--------------------------------------------------------------------------+
|              Purdue Reference Model for Industrial Control Security      |
|                       (ISA-99 / IEC 62443-3-2 기반)                       |
+--------------------------------------------------------------------------+
|  Level 5 : Enterprise Network (IT)                                      |
|  +----------------------------------------------------------------+     |
|  |  ERP(SAP), MES, CRM, Email, AD, SIEM, SOC                      |     |
|  |  보안영역: IT-OT 경계(IDMZ), 방화벽, DLP, NAC                  |     |
|  +-------------------------+--------------------------------------+     |
|  --- IDMZ (Industrial DMZ) --- Jump Server / WSUS / AV / Reverse Proxy |
|  Level 4 : Site Business Planning & Logistics                           |
|  +----------------------------------------------------------------+     |
|  |  Historian(PI System), EAM, 공장관리시스템                      |     |
|  |  보안영역: Zone 분리, VLAN, RBAC                                |     |
|  +-------------------------+--------------------------------------+     |
|  Level 3 : Site Operations (Operations DMZ)                             |
|  +----------------------------------------------------------------+     |
|  |  SCADA Server, HMI, Alarm Mgmt, Engineer Station, OPC UA Server|     |
|  |  보안영역: Application Whitelisting, USB 제어, 로그 집중화      |     |
|  +-------------------------+--------------------------------------+     |
|  Level 2 : Area Supervisory Control (Control Center)                    |
|  +----------------------------------------------------------------+     |
|  |  SCADA Master, Engineering Workstation, Alarm Panel, NTP        |     |
|  |  보안영역: 방화벽(L4), IPS(프로토콜 인지), Port Lockdown       |     |
|  +-------------------------+--------------------------------------+     |
|  Level 1 : Basic Control (Local Control)                                |
|  +----------------------------------------------------------------+     |
|  |  PLC, DCS Controller, RTU, SIS Logic Solver, Drive Controller  |     |
|  |  보안영역: Zone&Conduit, MAC ACL, 물리적 잠금                  |     |
|  +-------------------------+--------------------------------------+     |
|  Level 0 : Process (Physical Process)                                   |
|  +----------------------------------------------------------------+     |
|  |  Sensor, Valve, Motor, Switch, Breaker, Transmitter, RTD/TC     |     |
|  |  보안영역: Field Intrinsic Safety(IEC 60079), Tamper Seal      |     |
|  +----------------------------------------------------------------+     |
|  ※ 2020년 이후 IEC 62443-3-2가 Purdue Level 0~5를                       |
|     Zone / Conduit 개념으로 재정의 (Level별 1:1 매핑 X)                 |
+--------------------------------------------------------------------------+
```

**구 vs 신 패러다임 비교**: 과거(1990~2010)에는 OT 시스템이 **"Air-gap(물리적 격리) = 보안"** 이라는 신화로 폐쇄망 운영되었으나, 원격진단·클라우드 Historian·예지정비(PdM) 수요로 **점진적 네트워크 연결**이 불가피해졌고, 2010년 Stuxnet이 USB 매체로 격리망 침투를 입증하면서 **"Air-gap는 신화"** 로 전환되었다. 현재의 신 패러다임은 ①**Purdue 모델 기반 명시적 Zone 분리** + ②**Conduit(구간)별 보안통제** + ③**Defense-in-Depth(다층 방어)** + ④**OT-native 가시성(Deep Packet Inspection of Modbus/DNP3/PROFINET)** 으로 요약된다.

- **📢 섹션 요약 비유**: OT 보안은 "**공항 보안**"과 같다. 일반 구역(터미널·Level 5)은 자유로운 통행이 가능하지만, **탑승구(Conduit)** 에서 신분증·탑승권·보안검색을 거쳐야만 **비행기(PLC·Level 1)** 에 접근할 수 있다. IT 보안이 건물 출입 통제라면, OT 보안은 **탑승 후 조종석 진입 통제**까지 수행하는 다층 게이트 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IEC 62443 시리즈는 OT 보안을 **4단계 도메인**(General, Policies & Procedures, System, Component)으로 정의하며, 핵심은 **62443-3-3(시스템 보안요구사항·SL 1~4)** 과 **62443-4-2(컴포넌트 보안요구사항)** 이다. Security Level(SL)은 **SL-T(Target, 목표)·SL-A(Achieved, 달성)·SL-C(Capability, 컴포넌트 능력)·SL-UC(Use Case)** 4개로 구분되며, SL-1(부주의) -> SL-2(단순 공격자) -> SL-3(숙련 공격자·자원 보유) -> SL-4(국가·APT 그룹)으로 정의된다.

### 산업제어 핵심 프로토콜과 보안 취약점

```text
+-------------------------------------------------------------------------+
|                OT 프로토콜별 보안 특성 및 공격 표면 분석                |
+-------------------------------------------------------------------------+
|                                                                         |
|  [Modbus/TCP] Port 502                          [DNP3/TCP] Port 20000  |
|  +--------------------------+                  +----------------------+|
|  | Master --Query/Response---> Slave            | Outstation ---> Master ||
|  | FC 01:Read Coil          |                  | Object 30 g1v1: AI    ||
|  | FC 05:Write Single Coil  | <-- 위변조 취약    | Function Code 0x06:   ||
|  | FC 16:Write Multi Reg    |    (인증·암호화 X) | Write Attribute      ||
|  | -> 평문전송, No Auth, No  |                  | -> DNP3-SA(인증옵션)  ||
|  |   Integrity Check        |                  |   부분 지원, 약한암호 ||
|  +--------------------------+                  +----------------------+|
|                                                                         |
|  [PROFINET] (실시간 이더넷, Siemens)         [OPC UA] Port 4840          |
|  +--------------------------+                  +----------------------+|
|  | IO Controller ⇄ IO Device|                  | Client ⇄ Server      ||
|  | Real-Time Class 1~3(RT) |                  | Pub/Sub, Method Call ||
|  | -> Cycle Time 31.25μs~  |                  | -> Security Policy:   ||
|  |   100ms, 무결성 검증 미약|                  |   None/Basic/Sign&Enc||
|  +--------------------------+                  |   SecurityModes 0/1  ||
|                                                 |   /2/3 -> 2 이상 권장 ||
|  [EtherNet/IP] Port 44818 / 2222              +----------------------+|
|  +--------------------------+                                       |
|  | CIP(Classic Industrial   |       [EtherCAT] (Beckhoff)            |
|  | Protocol) over UDP/TCP   |       +--------------------------+    |
|  | Service 0x4E: Get_Attr   |       | Master ⇄ Slave, ET1100 ASIC|  |
|  | Service 0x4D: Set_Attr   |       | Distributed Clock(μs)    |    |
|  | -> CIP Security(2018~)    |       | -> EtherCATP(보안) 개발중 |    |
|  |   TLS/DTLS 기반, 적용低   |       +--------------------------+    |
|  +--------------------------+                                       |
+-------------------------------------------------------------------------+
```

### Defense-in-Depth 7계층 보안 아키텍처

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L7. 정책·거버넌스** | 보안정책 수립, 컴플라이언스 | IEC 62443-2-1, NERC-CIP-002~014, NIST CSF 2.0(2024), K-OT 인증, 사이버보안보험 |
| **L6. 인적·물리 보안** | 인가자 통제, 사찰, USB/Device Control | CIS Controls v8 #1~6, Mantrap, CCTV, Kensington Lock, OT USB 화이트리스트(SilivTerm 4D, Endpoint Protector) |
| **L5. 네트워크 보안** | Zone 분리, 침입탐지/방지, 데이터 다이오드 | IEC 62443-3-3 SR 1.1~1.13, Conduit 암호화, Industrial IDS(Claroty, Nozomi, Dragos, Cisco Cyber Vision), Niagara, Owl Cyber, Hirschmann EAGLE |
| **L4. 시스템 보안** | OS·DB·App 경화, Anti-Malware, Patch | Application Whitelisting(Carbon Black, McAfee Application Control, Tripwire Enterprise), SIGMA Rules, YARA 룰, OT 전용 AV(Tenable.ad, Claroty Edge) |
| **L3. 애플리케이션 보안** | SCADA/DCS HMI 인증, RBAC, 세션관리 | 802.1X(레벨3 네트워크), SAML 2.0/OIDC(Historian 연동), 코드사이닝, IBC(Identity-Based Cryptography) |
| **L2. 호스트 보안** | 엔지니어링 워크스테이션, 패치, 로그 | Change Window 통제, 로그 보존(3년), Sysmon + Wazuh + ELK, PLC Project File 해시 비교 |
| **L1. 필드 디바이스** | PLC·RTU·SIS·Drive 보안 | PLC Code Signing(Siemens S7-1500 F-CPU, Rockwell ControlLogix GuardLogix), 펌웨어 무결성(TPM 2.0), 물리 Tamper Switch, SIS IEC 61508 SIL 2/3 |

### IDMZ(Industrial DMZ) 핵심 설계 패턴

```text
+------------------+      +--------------------+      +------------------+
|  Enterprise Zone |      |   IDMZ (Purdue L5-L4 경계)  |  Operations Zone |
|  (IT Domain)     |      |                    |      |  (OT Domain)     |
|                  |      |  +--------------+  |      |                  |
|  +------------+  |  FW  |  | Jump Server  |  |  FW  |  +------------+  |
|  | SIEM/SOAR  |  | L4-L7|  | (Hardened)   |  | L4-L7|  | SCADA Master|  |
|  | (Splunk)   |<--+------+-->|              |<--+------+-->| Historian  |  |
|  +------------+  |      |  +--------------+  |      |  | (PI Server)|  |
|  +------------+  |      |  +--------------+  |      |  +------------+  |
|  | AD/LDAP    |  |      |  | WSUS/AV Repo |  |      |  +------------+  |
|  | (Domain    |  |      |  | (Read-Only)  |  |      |  | Engineering|  |
|  |  Trust)    |  |      |  +--------------+  |      |  | Workstation|  |
|  +------------+  |      |  +--------------+  |      |  +------------+  |
|                  |      |  | Reverse Proxy|  |      |                  |
|                  |      |  | (Modbus/TLS, |  |      |                  |
|                  |      |  |  OPC UA GW)  |  |      |                  |
|                  |      |  +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 407 / 800

<- **이전**: [406. IoT 보안 디바이스 인증 펌웨어](/studynote/12_it_management/05_security_compliance/406_iot_security_device_authentication_firmware/)
**다음**: [408. AI 보안 적대적 공격 방어 전략](/studynote/12_it_management/05_security_compliance/408_ai_security_adversarial_attack_defense/) ->

---
