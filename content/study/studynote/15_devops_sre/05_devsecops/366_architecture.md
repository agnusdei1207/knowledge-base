---
title: 366. 퍼듀 모델 산업 제어망 스마트팩토리 보안 (Purdue Model ICS OT Security IEC 62443 Smart Factory)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Purdue 모델([[157_isa|ISA]]-95)은 [[891_ot_operational_technology|OT]] ([[891_ot_operational_technology|Operational Technology]]) 환경을 Level 0~4로 계층화해 제어망과 기업망을 물리적·[[369_logic_bomb|논리]]적으로 분리하는 [[893_ics_industrial_control_system|ICS]] ([[893_ics_industrial_control_system|Industrial Control System]]) 보안 [[316_reference_pattern_nosql|참조]] 아키텍처이며, IEC 62443은 이 구조의 국제 보안 표준이다.
> 2. **가치**: [[893_ics_industrial_control_system|ICS]]/[[891_ot_operational_technology|OT]] 보안은 IT 보안과 달리 [[452_availability|가용성]]([[452_availability|Availability]]) > [[003_integrity|무결성]] > [[002_confidentiality|기밀성]] 우선순위를 따르며, [[896_plc_programmable_logic_controller|PLC]]/[[894_scada|SCADA]] 취약점이 실물 제조 라인 정지·인명 사고로 직결되어 패치 [[015_지연_데이터_관점|지연]]이 불가피한 환경에서 네트워크 격리와 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]가 핵심이다.
> 3. **판단 포인트**: IT-[[891_ot_operational_technology|OT]] 통합(Industry 4.0/스마트팩토리)은 레벨 3과 레벨 4 경계([[219_demilitarized_zone_dmz_public_subnet|DMZ]])를 허용하지만, 이 연결이 [[730_ransomware|랜섬웨어]]·[[748_apt|APT]] 공격의 주요 진입로가 되므로 [[008_단방향_반이중_전이중|단방향]] 게이트웨이([[001_dikw_pyramid|Data]] [[011_diode|Diode]])와 [[891_ot_operational_technology|OT]] 전용 IDS가 필수다.

---

## Ⅰ. 개요 및 필요성

2021년 Colonial [[082_pipeline|Pipeline]] [[730_ransomware|랜섬웨어]] 공격은 IT 시스템 마비로 [[123_pipe|파이프]]라인 운영을 5일간 중단시켰다. 2010년 Stuxnet은 [[896_plc_programmable_logic_controller|PLC]] [[032_firmware|펌웨어]]를 표적 공격해 이란 핵 원심분리기를 물리적으로 손상시켰다. [[891_ot_operational_technology|OT]] 보안 침해는 사이버 공간을 넘어 물리 세계에 즉각적인 영향을 미친다.

전통 [[893_ics_industrial_control_system|ICS]] 환경은 에어갭(Air Gap, 물리적 네트워크 단절)으로 보안을 유지했다. Industry 4.0 전환으로 [[891_ot_operational_technology|OT]] 시스템이 인터넷 또는 기업 IT망과 연결되면서 공격 표면이 급증하고 있다.

- 📢 섹션 요약 비유: 전통 공장 제어망은 외부와 단절된 섬이었다. 스마트팩토리는 그 섬에 다리를 놓았는데, 다리 없이는 [[001_dikw_pyramid|데이터]] 연동이 안 되고, 다리가 있으면 해커가 건너올 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│              Purdue 참조 모델 계층 구조                          │
├──────────────────────────────────────────────────────────────────┤
│  Level 4: 기업 네트워크 (ERP, MES, IT 시스템)                   │
│           ─── DMZ (방화벽 + 데이터 다이오드) ───────────────── │
│  Level 3: 제조 운영 (MES, 히스토리안, 엔지니어링 워크스테이션)  │
│           ─── 내부 방화벽 ──────────────────────────────────── │
│  Level 2: 제어 감시 (SCADA, HMI, DCS)                           │
│           ─── 제어망 방화벽 ────────────────────────────────── │
│  Level 1: 기본 제어 (PLC, RTU, 지능형 장치)                     │
│           ─── 필드버스 ──────────────────────────────────────  │
│  Level 0: 물리 공정 (센서, 액추에이터, 모터)                    │
└──────────────────────────────────────────────────────────────────┘
```

| 레벨  | 구성 요소                  | [[571_protection_vs_security|보호]] 수단                    |
| :---- | :------------------------- | :--------------------------- |
| 0~1   | [[896_plc_programmable_logic_controller|PLC]], [[897_rtu_remote_terminal_unit|RTU]], 센서             | 물리 잠금, [[032_firmware|펌웨어]] 서명       |
| 2     | [[894_scada|SCADA]], HMI                 | [[406_patch_management|패치 관리]], 화이트리스트       |
| [[219_demilitarized_zone_dmz_public_subnet|DMZ]]   | 히스토리안, [[501_file_definition_logical_record|파일]] 전송 서버  | [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]], [[008_단방향_반이중_전이중|단방향]] 게이트|
| 4     | [[081_erp_enterprise_resource_planning|ERP]], 기업 IT               | [[325_edr|EDR]], [[552_mfa|MFA]], [[624_siem|SIEM]]               |

**[[001_dikw_pyramid|데이터]] [[011_diode|다이오드]]([[001_dikw_pyramid|Data]] [[011_diode|Diode]])**: 물리적으로 [[008_단방향_반이중_전이중|단방향]] 전송만 허용하는 하드웨어 장치. [[891_ot_operational_technology|OT]]→IT 방향 [[001_dikw_pyramid|데이터]] 전송은 허용하고, IT→[[891_ot_operational_technology|OT]] 방향 접근은 물리적으로 차단한다.

- 📢 섹션 요약 비유: [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]]는 한쪽 방향으로만 흐르는 강의 갑문이다. 공장 [[001_dikw_pyramid|데이터]]가 외부로 나가는 것은 허용하지만, 외부에서 공장으로 들어오는 것은 물리적으로 막는다.

---

## Ⅲ. 비교 및 연결

| 항목             | IT 보안                      | [[891_ot_operational_technology|OT]]/[[893_ics_industrial_control_system|ICS]] 보안                   |
| :--------------- | :--------------------------- | :---------------------------- |
| 우선순위         | CIA ([[002_confidentiality|기밀성]] > [[003_integrity|무결성]] > [[452_availability|가용성]])| AIC ([[452_availability|가용성]] > [[003_integrity|무결성]] > [[002_confidentiality|기밀성]])|
| 패치 주기        | 즉각 패치 가능               | 계획된 정기 다운타임 필요     |
| [[295_protocol_field_tcp_udp_icmp|프로토콜]]         | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 표준                  | Modbus, [[899_dnp3_distributed_network_protocol|DNP3]], [[900_profinet|PROFINET]], OPC   |

[[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 아키텍처와 [[891_ot_operational_technology|OT]] 환경의 통합이 [[216_progress_in_synchronization|진행]] 중이다. [[891_ot_operational_technology|OT]] 기기는 Agent 설치가 불가해 네트워크 행동 분석(NBA) 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]](Claroty, Dragos)로 [[585_zero_skipping|Zero]] Trust를 구현한다.

- 📢 섹션 요약 비유: [[891_ot_operational_technology|OT]] 보안에서 [[452_availability|가용성]] 우선은 수술실 전등과 같다. 수술 중 전등이 꺼지면 사람이 죽는다. 보안 패치로 잠깐 끄는 것도 매우 신중하게 계획해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[893_ics_industrial_control_system|ICS]]/[[891_ot_operational_technology|OT]] 보안 강화 [[435_checklist_based_testing|체크리스트]]**
1. Purdue 모델 기반 [[223_network_segmentation_vlan_vrf_isolation|네트워크 세그멘테이션]] 구현
2. IT-[[891_ot_operational_technology|OT]] 연결 구간에 [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]] 또는 일방향 게이트웨이 적용
3. [[891_ot_operational_technology|OT]] 전용 [[601_ids_ips_syscall_tracing|IDS]]/[[893_ics_industrial_control_system|ICS]] 자산 가시성 도구 도입 (Claroty, Dragos)
4. [[896_plc_programmable_logic_controller|PLC]]/[[894_scada|SCADA]] 취약점 관리: 패치 불가 시 [[244_virtual_patching_waf|가상 패치]]([[244_virtual_patching_waf|Virtual Patching]]) 적용
5. 원격 접근: [[983_vpn_virtual_private_network|VPN]] + [[552_mfa|MFA]] + 권한 최소화, 작업 [[160_session_controlling_terminal|세션]] 녹화

**[[128_water_scrum_fall_anti_pattern|안티패턴]]**
- [[891_ot_operational_technology|OT]] 시스템에 IT [[007_security_policy|보안 정책]] 그대로 적용 → [[452_availability|가용성]] 저하, 생산 중단
- [[219_demilitarized_zone_dmz_public_subnet|DMZ]] 없는 IT-[[891_ot_operational_technology|OT]] 직접 연결 → [[730_ransomware|랜섬웨어]] 전파 경로
- [[891_ot_operational_technology|OT]] 원격 접근에 공유 계정 사용 → [[606_auditing_linux_auditd|감사]] 추적 불가

- 📢 섹션 요약 비유: IT [[007_security_policy|보안 정책]]을 OT에 그대로 적용하는 것은 병원 수술실에 일반 사무실 소방 규정을 적용하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[[904_iec_62443|IEC 62443]] 기반 [[893_ics_industrial_control_system|ICS]] 보안 체계 구축 시 [[891_ot_operational_technology|OT]] 침해 [[009_incident_response|사고 대응]] 시간이 50% 이상 단축되고, 레거시 취약점의 실제 공격 경로를 네트워크 격리로 차단해 위험을 크게 줄일 수 있다.

미래는 [[418_5g_embb_urllc_mmtc_slicing|5G]] 사설망 기반 스마트팩토리에서 [[891_ot_operational_technology|OT]] 기기 [[303_authentication_authorization_patterns|인증]]을 SIM/eSIM으로 수행하고, [[190_ai_llm_requirements_specification|AI]] 기반 [[891_ot_operational_technology|OT]] [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]가 자율 방어 [[893_ics_industrial_control_system|ICS]] 체계로 발전한다.

- 📢 섹션 요약 비유: [[893_ics_industrial_control_system|ICS]] 보안은 발전소 보안 요원과 같다. 발전소를 멈추지 않으면서 침입자를 막아야 하는 극도로 어려운 임무로, 경보 시스템이 울려도 전원을 끌 수 없는 환경에서 판단한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| Purdue 모델 ([[157_isa|ISA]]-95)                    | [[891_ot_operational_technology|OT]] 환경 Level 0~4 계층화 [[316_reference_pattern_nosql|참조]] 아키텍처                   |
| [[904_iec_62443|IEC 62443]]                               | 산업 자동화 사이버보안 국제 표준, SL 0~4                 |
| [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]]                          | 물리적 [[008_단방향_반이중_전이중|단방향]] 전송 장치, IT-[[891_ot_operational_technology|OT]] [[219_demilitarized_zone_dmz_public_subnet|DMZ]] 핵심 보안 장치        |
| [[891_ot_operational_technology|OT]] [[601_ids_ips_syscall_tracing|IDS]] (Claroty, Dragos, Nozomi)        | [[891_ot_operational_technology|OT]] 전용 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]], 자산 가시성 확보                      |
| AIC 우선순위                            | [[891_ot_operational_technology|OT]] 보안 [[452_availability|가용성]] 최우선 원칙                               |

### 📈 관련 키워드 및 발전 흐름도

```text
에어갭 ICS (물리적 완전 격리)
    │
    ▼
Purdue 모델 (계층별 논리 분리)
    │
    ▼
IT-OT DMZ + 데이터 다이오드 (Industry 4.0 연동)
    │
    ▼
IEC 62443 (국제 OT 보안 표준화)
    │
    ▼
OT IDS + 자산 가시성 (이상 탐지 고도화)
    │
    ▼
5G 사설망 + AI 기반 자율 방어 ICS
```

### 👶 어린이를 위한 3줄 비유 설명

1. Purdue 모델은 공장을 층별로 나눠서 각 층이 허락 없이 다른 층에 마음대로 들어가지 못하게 만든 보안 구조예요.
2. [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]]는 공장 [[001_dikw_pyramid|데이터]]가 밖으로만 나갈 수 있고, 바깥에서 공장 안으로는 절대 못 들어오게 하는 물리적 잠금장치예요.
3. [[891_ot_operational_technology|OT]] 보안에서는 공장이 멈추지 않는 게 가장 중요해서, 아파도 수술(패치)을 바로 못 하고 방역(격리)으로 버티는 방식을 써요.
