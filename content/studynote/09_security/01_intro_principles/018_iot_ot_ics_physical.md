---
title: "IoT, OT, ICS & Physical Security"
date: "2025-02-24"
description: "Purdue 모델, IEC 62443, SCADA 보안부터 스마트 팩토리 제어망 및 사이버-물리 시스템(CPS) 보호까지 통합 아키텍처"
tags:
  - "security"
---

# [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/), [ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 및 물리적 보안 ([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/), [ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) & Physical [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)([Operational Technology](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) 및 [ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안의 핵심은 [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/)([Confidentiality](/studynote/09_security/01_intro_principles/002_confidentiality/))이 아닌, 인간의 생명 및 공정의 연속성과 직결되는 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/studynote/09_security/01_intro_principles/003_integrity/))을 사수하는 것이다.
> 2. **가치**: 에어갭(Air Gap)이 붕괴된 [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 환경에서 Purdue 모델과 [IEC 62443](/studynote/09_security/18_iot_ot_physical/904_iec_62443/) 표준을 적용하여 사이버 위협이 물리적 피해로 전이되는 것을 차단한다.
> 3. **융합**: 기존의 단순 통제 시스템이 클라우드 및 5G와 결합하면서, 사이버-물리 시스템([CPS](/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/))이라는 초연결 환경으로 진화하고 있어 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 관점의 기기 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 필수가 되었다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

전통적으로 공장의 생산 라인([OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/))과 발전소의 제어 시스템([ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)/[SCADA](/studynote/09_security/18_iot_ot_physical/894_scada/))은 기업의 인터넷망(IT)과 물리적으로 단절된 '에어갭(Air Gap)' 상태를 유지해왔다. 그러나 인더스트리 4.0(Industry 4.0)의 도래와 함께 빅데이터 분석, 예지 보전(Predictive Maintenance), 원격 제어가 필수가 되면서 IT와 OT의 융합이 급격하게 진행되었다. 문제는 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 환경의 장비들([PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/), [RTU](/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/) 등)이 설계 당시부터 보안을 전혀 고려하지 않은 평문 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)(Modbus, [DNP3](/studynote/09_security/18_iot_ot_physical/899_dnp3_distributed_network_protocol/) 등)을 사용하며, 패치조차 쉽지 않은 레거시 OS를 기반으로 동작한다는 점이다. 스턱스넷(Stuxnet) 사태나 미국 콜로니얼 파이프라인(Colonial [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/)) [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 사건은, IT 망을 통해 침투한 사이버 위협이 어떻게 국가 기반 시설의 '물리적 마비'를 초래할 수 있는지 여실히 보여주었다.

<strong><a href="/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/">IT와 [OT</a> 환경의 융합 및 에어갭 붕괴 도식]</strong>
이 도식은 과거 물리적으로 분리되었던 IT와 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망이 [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 전환으로 인해 어떻게 연결되고, 이로 인해 위협 표면(Attack Surface)이 어떻게 확장되는지를 보여준다.
```text
[과거: Air-Gapped Model]           [현재: IT-OT Convergence Model]
+------------------+             +------------------+
| IT (ERP, Email)  |             | IT (Cloud, ERP)  |
+--------+---------+             +--------+---------+
        (단절)                           v (위협 전이 경로)
+--------+---------+             +--------+---------+
| OT (SCADA, PLC)  |             | OT (SCADA, PLC)  |
| (폐쇄망, 안전)   |             | (IoT 센서 연동)  |
+------------------+             +------------------+
```
이 흐름의 핵심은 '연결' 자체가 취약점이 된다는 것이다. 과거에는 USB나 악의적 내부자 등 물리적 접근(Physical Access)만이 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망을 위협할 수 있었으나, 이제는 IT 망의 이메일 [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/)([Phishing](/studynote/09_security/15_malware_attack_vectors/752_phishing/))으로 탈취한 크리덴셜 하나만으로도 용광로의 온도를 조절하는 [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)([Programmable Logic Controller](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/))에 악성 명령을 주입할 수 있게 되었다. 따라서 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 IT망과 OT망 사이의 완충 지대([DMZ](/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/))를 설정하고, 제어 명령의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 검증하는 데 집중해야 한다.

> 📢 **섹션 요약 비유**: 이것은 마치 수백 년간 외부와 단절되어 면역력이 전혀 없는 원시 부족([OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) 마을에, 외부 세계와 교역하기 위해 다리(IT 연결)를 놓는 것과 같습니다. 철저한 검역소(보안망) 없이 다리를 개방하면, 단순한 감기 [바이러스](/studynote/02_operating_system/10_security/589_virus/)(IT [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/))만으로도 부족 전체가 몰살당할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)/[OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) [보안 아키텍처](/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/)의 글로벌 표준은 <strong><a href="/studynote/09_security/18_iot_ot_physical/902_purdue_model/">Purdue Model</a></strong> (퍼듀 모델, ISA-99)과 이를 현대화한 <strong><a href="/studynote/09_security/18_iot_ot_physical/904_iec_62443/">IEC 62443</a></strong> 규격이다. 이 모델은 공장 네트워크를 수직적인 계층으로 나누어 위협의 하향 전파를 차단한다.

| 구성 요소 | 계층 (Level) | 역할 및 주요 장비 | 보안 통제 핵심 |
|:---|:---|:---|:---|
| **Enterprise Network** | Level 4~5 (IT) | 이메일, [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), 인터넷 통신 | 일반적인 IT 보안, 이메일 게이트웨이 |
| <strong>Industrial <a href="/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/">DMZ</a></strong> | Level 3.5 (IDMZ) | IT와 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 사이의 완충, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), 패치 서버 | [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 기반의 트래픽 종단(Termination) 및 중계 |
| **Site Operations** | Level 3 ([OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) | 생산 스케줄링, 히스토리안 DB, 중앙 [SCADA](/studynote/09_security/18_iot_ot_physical/894_scada/) | IT망에서의 직접 접근 원천 차단 |
| **Control System** | Level 1~2 ([OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) | HMI, [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)(제어기), [RTU](/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/) | 비정상 제어 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(Modbus) DPI 탐지 |
| **Field Devices** | Level 0 (Field) | 모터, 센서, 액추에이터 | 물리적 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/), 하드웨어 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) |

<strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/">Purdue 모델 기반의 계층적 [보안 아키텍처</a> 도식]</strong>
이 계층 구조도는 IT 영역(Level 4)에서 발생한 악성코드가 현장 장비(Level 0)로 도달하기 위해 반드시 통과해야 하는 방어선(Choke Points)을 시각화한다.
```text
+--------------------------------------------------------+
| Level 4, 5: IT Enterprise Zone (인터넷, ERP)           |
+-------------------------+------------------------------+
| Firewall & VPN Gateway  v  (IT 트래픽 차단/프록시)     |
+--------------------------------------------------------+
| Level 3.5: Industrial DMZ (점프 호스트, 패치 서버)     |
+-------------------------+------------------------------+
| OT Firewall (DPI)       v  (엄격한 1-way 데이터 다이오드)|
+--------------------------------------------------------+
| Level 3: Site Operations (SCADA, Historian)            |
+--------------------------------------------------------+
| Level 1, 2: Control Zone (PLC, HMI, RTU)               |
+--------------------------------------------------------+
| Level 0: Field Devices (센서, 밸브, 모터)              |
+--------------------------------------------------------+
```
이 구조의 핵심은 IT 계층과 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 계층 간의 <strong><a href="/studynote/02_operating_system/02_process_thread/120_direct_communication/">직접 통신</a>(<a href="/studynote/02_operating_system/02_process_thread/120_direct_communication/">Direct Communication</a>)을 물리적, 논리적으로 절대 허용하지 않는다</strong>는 점이다. Level 4의 사용자가 Level 2의 HMI에 접근하려면, 반드시 Level 3.5의 점프 호스트(Jump Host/Bastion)를 거쳐야만 한다. 또한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 흐름은 OT에서 IT로 향하는 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)(예: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/) 장비 사용)을 원칙으로 하며, IT에서 OT로 들어오는 패치나 제어 명령은 매우 엄격한 화이트리스트 기반의 검증을 거친다. 최하단 Level 0~2에서는 암호화가 불가능한 경우가 많으므로, [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 비정상적 행위를 탐지하는 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 전용 네트워크 [침입 탐지 시스템](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)(NDR)이 필수적이다.

> 📢 **섹션 요약 비유**: 퍼듀 모델은 성의 방어 구조와 같습니다. 외성(IT)이 함락되더라도, 해자(IDMZ)와 내성([SCADA](/studynote/09_security/18_iot_ot_physical/894_scada/))의 철문을 거쳐야만 왕([PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/))에게 접근할 수 있도록 여러 겹의 성벽을 쌓는 다층 방어([Defense in Depth](/studynote/09_security/01_intro_principles/012_defense_in_depth/)) 전략입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

IT 보안과 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하고자 하는 최우선 가치가 완전히 다르기 때문에, 접근 방식(Paradigm)에 근본적인 차이가 존재한다.

| 구분 | IT 보안 (Information Technology) | [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안 ([Operational Technology](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) | 실무 판단 포인트 |
|:---|:---|:---|:---|
| **최우선 가치** | [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/) ([Confidentiality](/studynote/09_security/01_intro_principles/002_confidentiality/)) > [무결성](/studynote/09_security/01_intro_principles/003_integrity/) > [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) > [무결성](/studynote/09_security/01_intro_principles/003_integrity/) > [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/) | CIA Triad의 역전 현상 |
| **패치 및 업데이트** | 주기적이고 빈번함 (Patch Tuesday) | 매우 드묾, 공정 중단(Downtime) 시에만 가능 | [제로데이 취약점](/studynote/09_security/04_endpoint_security/358_zero_day/) 노출 시간 |
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>)</strong>| 초(Second) 단위 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 허용 | 밀리초(ms) 단위의 실시간성 (Real-time) 필수 | 보안 솔루션 인라인(In-line) 배치 제약 |
| **장비 수명 (Lifecycle)**| 3 ~ 5년 (빠른 교체 주기) | 15 ~ 30년 (레거시 OS, 단종 하드웨어) | 레거시 지원 및 폐쇄망 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) |

**IEC 62443 기반 Zone & Conduit (구역 및 배관) 모델 도식]**
이 도식은 플랫(Flat)한 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 네트워크를 어떻게 논리적으로 격리(Zone)하고 통신 경로(Conduit)를 제어하는지 보여준다.
```text
+-----------------+       [Conduit (배관)]       +-----------------+
| Zone A (포장기) | <-======(Firewall)======-> | Zone B (조합기) |
| - PLC_1         |       DPI Inspection       | - PLC_2         |
| - HMI_1         |                            | - HMI_2         |
+-----------------+                            +-----------------+
```
이 도식의 핵심은 퍼듀 모델의 수직적 방어(North-South)뿐만 아니라, 같은 계층 내의 수평적 이동(East-West)을 차단하는 <strong><a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">세그멘테이션</a>(<a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a>)</strong> 전략이다. [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 네트워크는 역사적으로 하나의 거대한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 허브에 모든 장비가 물려있는 플랫(Flat) 네트워크인 경우가 많다. 이 경우 특정 포장기(Zone A)의 PLC가 악성코드에 감염되면, 즉각적으로 배합기(Zone B)로 감염이 확산된다. IEC 62443은 기계/공정 단위로 구역(Zone)을 나누고, 구역 간 통신은 오직 인가된 배관(Conduit)을 통해서만 이루어지도록 강제한다.

> 📢 **섹션 요약 비유**: IT 보안이 은행 금고의 돈([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 지키는 것이라면, [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 달리는 고속열차([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))가 탈선하지 않도록 철로와 신호기(제어 [무결성](/studynote/09_security/01_intro_principles/003_integrity/))를 지키는 것입니다. 열차를 세워서(패치 적용) 검사하는 것 자체가 비즈니스에 치명적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

[OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)/[ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안을 실무에 적용할 때, IT 보안의 관행을 그대로 이식하려다 치명적인 공정 중단을 유발하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)([Anti-pattern](/studynote/11_design_supervision/03_gof_creational_structural/161_anti_pattern/))이 자주 발생한다.

1. <strong>인라인(In-line) 차단 모드 강제 적용 (<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 파괴)</strong>
   - **상황**: 보안팀이 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 IT용 [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)(Intrusion Prevention System)를 인라인으로 설치하고 차단([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 모드를 활성화함.
   - **문제**: IPS의 미세한 패킷 검사 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 PLC와 로봇 팔 간의 타이밍 동기화를 깨뜨리거나, 오탐(False Positive)으로 정상 제어 패킷을 드롭하여 전체 생산 라인이 급정지함.
   - **의사결정**: [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 환경에서는 보안 장비를 절대 인라인으로 배치하지 않고, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)(Mirror/SPAN) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 통해 아웃오브밴드(Out-of-band) 형태로 트래픽을 수집하여 <strong>모니터링 및 탐지(<a href="/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a> Only)</strong> 위주로 구성해야 한다.

2. <strong>레거시 윈도우 OS 대상 백신(<a href="/studynote/09_security/04_endpoint_security/323_antivirus/">AV</a>) 스캔 강제</strong>
   - **상황**: HMI(Human Machine Interface) 시스템이 Windows XP를 사용 중이라, 백신 프로그램을 설치하고 매일 정오에 전체 스캔(Full Scan)을 예약함.
   - **문제**: 스캔 시 발생하는 CPU/Disk I/O 부하로 인해 HMI 화면이 멈추고 제어 명령 하달이 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)됨.
   - **의사결정**: 레거시 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 단말에는 리소스를 많이 먹는 시그니처 기반 백신 대신, 인가된 프로세스만 실행을 허용하는 **애플리케이션 화이트리스팅(Application Whitelisting / Lockdown)** 솔루션을 적용해야 한다.

3. <strong>물리적 보안(Physical <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>) 통제 누락</strong>
   - **상황**: 네트워크 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 철저히 구축했으나, 공장 현장(Shop Floor)에 있는 PLC의 관리자 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)([USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/), [Serial](/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/))가 물리적으로 외부에 노출되어 있음.
   - **문제**: 유지보수 직원이 감염된 개인 노트북이나 USB를 직접 장비에 꽂아([Evil Maid Attack](/studynote/09_security/20_extra_exam_prep/0991_evil_maid_attack/)) 모든 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 통제를 우회함.
   - **의사결정**: 사이버 보안뿐만 아니라 기기 자체의 물리적 잠금장치([Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)), [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 감시, 출입 통제([Mantrap](/studynote/09_security/18_iot_ot_physical/935_mantrap/)) 등 물리적 보안 체계를 통합하여 관리해야 한다.

> 📢 **섹션 요약 비유**: 수술 중인 환자([OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 공정)에게 백신(IT 보안 솔루션)을 주사하겠다고 생명유지장치를 잠시 끄는 것은 의료 사고입니다. 환자의 수술을 방해하지 않는 선에서 철저히 모니터링만 수행하는 것이 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안의 철칙입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

산업 제어 시스템에 대한 선제적 [보안 아키텍처](/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/) 구축은 기업의 생산 연속성을 담보하고, 인명 피해라는 최악의 파국을 방지하는 안전판 역할을 한다.

| 기대 효과 | 정성적 지표 | 정량적 지표 |
|:---|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 보장 (Downtime 방지)</strong> | [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/)로 인한 생산 라인 마비 차단 | 악성코드로 인한 비계획적 공정 중단율 99% 감소 |
| **안전사고 예방 (Safety)** | 센서값 조작으로 인한 기계 폭발/오작동 방지 | 사이버 원인으로 인한 중대재해 발생 건수 0건 |
| **가시성(Visibility) 확보** | 섀도우 IT 및 미인가 산업용 기기 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 자산 및 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)률 100% 달성 |

향후 [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 개별 공장 단위의 방어를 넘어, [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 특화망([eMBB](/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/), [URLLC](/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))과 [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)([MEC](/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/))이 결합된 <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/">스마트 팩토리</a> 전체의 <a href="/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">제로 트러스트</a> 도입</strong>으로 발전할 것이다. 레거시 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 대신 암호화가 내장된 [OPC UA](/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) (Open Platform Communications Unified [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/)) 기반으로 표준이 이동하고 있으며, 물리적 제어 로직 자체에 대한 변조를 탐지하기 위해 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 기반의 공정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)([Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) 기술이 적극적으로 도입될 전망이다. 물리 세계와 사이버 세계의 경계가 사라진 [CPS](/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/)(Cyber-Physical System) 시대에, 보안은 곧 생명 존중이자 국가 안보이다.

> 📢 **섹션 요약 비유**: 미래의 산업 보안은 성벽([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))에만 의존하지 않고, 공장 내 모든 로봇과 기계가 스스로 신분증([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)을 검사하고 비정상적인 명령([바이러스](/studynote/02_operating_system/10_security/589_virus/))은 스스로 거부하는 지능형 자가 면역 시스템으로 진화할 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 퍼듀 모델 ([Purdue Model](/studynote/09_security/18_iot_ot_physical/902_purdue_model/)) | -> 아키텍처 기준 | IT-[OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 5계층 분리 표준 |
| [IEC 62443](/studynote/09_security/18_iot_ot_physical/904_iec_62443/) | -> 국제 표준 | [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안 요구사항 및 구역 통제 |
| [SCADA](/studynote/09_security/18_iot_ot_physical/894_scada/) / [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) | -> [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상 | 산업 제어 장비, 레거시 OS |
| 스턱스넷 (Stuxnet) | -> 대표 위협 사례 | 핵 원심분리기 [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) 공격 |
| [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) | -> 발전 방향 | 기기 단위 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 및 최소 권한 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IT 보안 (IT Security) — 기밀성 중심, 패치·업데이트 가능]
    |
    v
[OT/ICS 보안 (Operational Technology) — 가용성·무결성 우선, 레거시 환경]
    |
    v
[에어갭 붕괴 (Air Gap 붕괴) — IT·OT 융합, 스마트 팩토리 전환]
    |
    v
[퍼듀 모델 (Purdue Model) / IEC 62443 — 계층 분리, 구역·배관 통제]
    |
    v
[제로 트러스트 OT (Zero Trust OT) — 기기 인증, OPC UA 암호화 표준화]
```
[OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)/[ICS](/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안은 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 최우선으로 하며, 퍼듀 모델과 [IEC 62443](/studynote/09_security/18_iot_ot_physical/904_iec_62443/) 기반의 구역 격리로 사이버-물리 위협을 차단한다.

### 👶 어린이를 위한 3줄 비유 설명

🏭 **공장 방어선**: [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 인터넷 해커가 공장 로봇팔에 나쁜 명령을 보내지 못하도록 막는 것이에요. 공장이 멈추면 사람이 다칠 수도 있어서 매우 중요해요!
🔌 **연결의 위험**: 예전에는 공장 컴퓨터가 인터넷과 완전히 분리되어 안전했어요. 하지만 이제 인터넷으로 공장을 원격 관리하면서 해커가 침입할 구멍이 생겼어요!
🛡️ **층별 방어**: 퍼듀 모델은 공장 네트워크를 층별로 나눠서 한 층이 뚫려도 다른 층은 안전하게 지키는 방어 방법이에요. 아파트 각 층에 자물쇠를 따로 달아두는 것처럼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 18 / 1108

<- **이전**: [17. 보안 프레임워크 및 컴플라이언스 (Security Framework & Compliance)](/studynote/09_security/01_intro_principles/017_security_framework_compliance/)
**다음**: [19. 완전한 통제 원칙 (Open Platform for Security) — 분리 보호](/studynote/09_security/01_intro_principles/019_ai_emerging_tech/) ->

---
