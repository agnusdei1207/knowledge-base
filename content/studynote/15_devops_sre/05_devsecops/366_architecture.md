+++
title = "366. 퍼듀 모델 산업 제어망 스마트팩토리 보안 (Purdue Model ICS OT Security IEC 62443 Smart Factory)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Purdue 모델([ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95)은 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) ([Operational Technology](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) 환경을 Level 0~4로 계층화해 제어망과 기업망을 물리적·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 분리하는 [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) ([Industrial Control System](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)) 보안 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 아키텍처이며, IEC 62443은 이 구조의 국제 보안 표준이다.
> 2. **가치**: [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)/[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안은 IT 보안과 달리 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) > [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) > [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 우선순위를 따르며, [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)/[SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/) 취약점이 실물 제조 라인 정지·인명 사고로 직결되어 패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 불가피한 환경에서 네트워크 격리와 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)가 핵심이다.
> 3. **판단 포인트**: IT-[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 통합(Industry 4.0/스마트팩토리)은 레벨 3과 레벨 4 경계([DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/))를 허용하지만, 이 연결이 [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/)·[APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/) 공격의 주요 진입로가 되므로 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 게이트웨이([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Diode](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/))와 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 전용 IDS가 필수다.

---

## Ⅰ. 개요 및 필요성

2021년 Colonial [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 공격은 IT 시스템 마비로 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 운영을 5일간 중단시켰다. 2010년 Stuxnet은 [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)를 표적 공격해 이란 핵 원심분리기를 물리적으로 손상시켰다. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안 침해는 사이버 공간을 넘어 물리 세계에 즉각적인 영향을 미친다.

전통 [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 환경은 에어갭(Air Gap, 물리적 네트워크 단절)으로 보안을 유지했다. Industry 4.0 전환으로 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 시스템이 인터넷 또는 기업 IT망과 연결되면서 공격 표면이 급증하고 있다.

- 📢 섹션 요약 비유: 전통 공장 제어망은 외부와 단절된 섬이었다. 스마트팩토리는 그 섬에 다리를 놓았는데, 다리 없이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연동이 안 되고, 다리가 있으면 해커가 건너올 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|              Purdue 참조 모델 계층 구조                          |
+------------------------------------------------------------------+
|  Level 4: 기업 네트워크 (ERP, MES, IT 시스템)                   |
|           --- DMZ (방화벽 + 데이터 다이오드) ----------------- |
|  Level 3: 제조 운영 (MES, 히스토리안, 엔지니어링 워크스테이션)  |
|           --- 내부 방화벽 ------------------------------------ |
|  Level 2: 제어 감시 (SCADA, HMI, DCS)                           |
|           --- 제어망 방화벽 ---------------------------------- |
|  Level 1: 기본 제어 (PLC, RTU, 지능형 장치)                     |
|           --- 필드버스 --------------------------------------  |
|  Level 0: 물리 공정 (센서, 액추에이터, 모터)                    |
+------------------------------------------------------------------+
```

| 레벨  | 구성 요소                  | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수단                    |
| :---- | :------------------------- | :--------------------------- |
| 0~1   | [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/), [RTU](/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/), 센서             | 물리 잠금, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 서명       |
| 2     | [SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/), HMI                 | [패치 관리](/knowledge-base/studynote/09_security/04_endpoint_security/406_patch_management/), 화이트리스트       |
| [DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/)   | 히스토리안, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송 서버  | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/), [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 게이트|
| 4     | [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), 기업 IT               | [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/), [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/), [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/)               |

<strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/">다이오드</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/">Diode</a>)</strong>: 물리적으로 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 전송만 허용하는 하드웨어 장치. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)->IT 방향 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송은 허용하고, IT->[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 방향 접근은 물리적으로 차단한다.

- 📢 섹션 요약 비유: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)는 한쪽 방향으로만 흐르는 강의 갑문이다. 공장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 외부로 나가는 것은 허용하지만, 외부에서 공장으로 들어오는 것은 물리적으로 막는다.

---

## Ⅲ. 비교 및 연결

| 항목             | IT 보안                      | [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)/[ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안                   |
| :--------------- | :--------------------------- | :---------------------------- |
| 우선순위         | CIA ([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) > [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) > [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))| AIC ([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) > [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) > [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))|
| 패치 주기        | 즉각 패치 가능               | 계획된 정기 다운타임 필요     |
| [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)         | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 표준                  | Modbus, [DNP3](/knowledge-base/studynote/09_security/18_iot_ot_physical/899_dnp3_distributed_network_protocol/), [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/), OPC   |

[Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 아키텍처와 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 환경의 통합이 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 기기는 Agent 설치가 불가해 네트워크 행동 분석(NBA) 기반 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)(Claroty, Dragos)로 [Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust를 구현한다.

- 📢 섹션 요약 비유: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안에서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선은 수술실 전등과 같다. 수술 중 전등이 꺼지면 사람이 죽는다. 보안 패치로 잠깐 끄는 것도 매우 신중하게 계획해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/">ICS</a>/<a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/">OT</a> 보안 강화 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. Purdue 모델 기반 [네트워크 세그멘테이션](/knowledge-base/studynote/09_security/05_web_app_security/223_network_segmentation_vlan_vrf_isolation/) 구현
2. IT-[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 연결 구간에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/) 또는 일방향 게이트웨이 적용
3. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 전용 [IDS](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/[ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 자산 가시성 도구 도입 (Claroty, Dragos)
4. [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)/[SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/) 취약점 관리: 패치 불가 시 [가상 패치](/knowledge-base/studynote/09_security/05_web_app_security/244_virtual_patching_waf/)([Virtual Patching](/knowledge-base/studynote/09_security/05_web_app_security/244_virtual_patching_waf/)) 적용
5. 원격 접근: [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) + [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) + 권한 최소화, 작업 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 녹화

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 시스템에 IT [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) 그대로 적용 -> [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 저하, 생산 중단
- [DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/) 없는 IT-[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 직접 연결 -> [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 전파 경로
- [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 원격 접근에 공유 계정 사용 -> [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 불가

- 📢 섹션 요약 비유: IT [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/)을 OT에 그대로 적용하는 것은 병원 수술실에 일반 사무실 소방 규정을 적용하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[IEC 62443](/knowledge-base/studynote/09_security/18_iot_ot_physical/904_iec_62443/) 기반 [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안 체계 구축 시 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 침해 [사고 대응](/knowledge-base/studynote/09_security/01_intro_principles/009_incident_response/) 시간이 50% 이상 단축되고, 레거시 취약점의 실제 공격 경로를 네트워크 격리로 차단해 위험을 크게 줄일 수 있다.

미래는 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 사설망 기반 스마트팩토리에서 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 기기 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 SIM/eSIM으로 수행하고, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)가 자율 방어 [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 체계로 발전한다.

- 📢 섹션 요약 비유: [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) 보안은 발전소 보안 요원과 같다. 발전소를 멈추지 않으면서 침입자를 막아야 하는 극도로 어려운 임무로, 경보 시스템이 울려도 전원을 끌 수 없는 환경에서 판단한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| Purdue 모델 ([ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95)                    | [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 환경 Level 0~4 계층화 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 아키텍처                   |
| [IEC 62443](/knowledge-base/studynote/09_security/18_iot_ot_physical/904_iec_62443/)                               | 산업 자동화 사이버보안 국제 표준, SL 0~4                 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)                          | 물리적 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 전송 장치, IT-[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) [DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/) 핵심 보안 장치        |
| [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) [IDS](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) (Claroty, Dragos, Nozomi)        | [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 전용 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), 자산 가시성 확보                      |
| AIC 우선순위                            | [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 최우선 원칙                               |

### 📈 관련 키워드 및 발전 흐름도

```text
에어갭 ICS (물리적 완전 격리)
    |
    v
Purdue 모델 (계층별 논리 분리)
    |
    v
IT-OT DMZ + 데이터 다이오드 (Industry 4.0 연동)
    |
    v
IEC 62443 (국제 OT 보안 표준화)
    |
    v
OT IDS + 자산 가시성 (이상 탐지 고도화)
    |
    v
5G 사설망 + AI 기반 자율 방어 ICS
```

### 👶 어린이를 위한 3줄 비유 설명

1. Purdue 모델은 공장을 층별로 나눠서 각 층이 허락 없이 다른 층에 마음대로 들어가지 못하게 만든 보안 구조예요.
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)는 공장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 밖으로만 나갈 수 있고, 바깥에서 공장 안으로는 절대 못 들어오게 하는 물리적 잠금장치예요.
3. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 보안에서는 공장이 멈추지 않는 게 가장 중요해서, 아파도 수술(패치)을 바로 못 하고 방역(격리)으로 버티는 방식을 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 366 / 373

<- **이전**: [365. C-V2X 자율주행 모빌리티 5G 엣지 레이턴시 제어 (C-V2X Cellular Vehicle-to-Everything 5G](/knowledge-base/studynote/15_devops_sre/05_devsecops/365_c_v2x_5g/)
**다음**: [367. DPU SmartNIC 인프라 오프로딩 데이터 처리 장치 (DPU SmartNIC Infrastructure Offloading](/knowledge-base/studynote/15_devops_sre/05_devsecops/367_dpu_smartnic/) ->

---
