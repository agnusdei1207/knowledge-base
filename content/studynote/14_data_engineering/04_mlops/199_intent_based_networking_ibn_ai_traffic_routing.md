---
title: "Intent Based Networking Ibn Ai Traffic Routing"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 199
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/)([Intent](/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/)-Based Networking)은 비즈니스 의도([Intent](/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/))를 자연어 또는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 입력하면 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML이 자동으로 네트워크 구성을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·운영하는 자율 네트워킹 패러다임이다.
> 2. **가치**: 변환(Translation) -> 활성화(Activation) -> 보증(Assurance) 3단계 루프로 네트워크가 항상 의도된 상태를 유지하며, 이상 감지 시 자동 자가 치유(Self-Healing)한다.
> 3. **판단 포인트**: IBN은 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)(Software-Defined Networking) 위에 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진을 추가한 상위 개념이며, [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)과 결합하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 동적 네트워크 보장이 가능하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) ([Intent](/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/)-Based Networking) 정의

IBN은 Gartner(2017)가 제안한 개념으로, 네트워크 관리자가 "무엇을(What)" 원하는지 비즈니스 의도를 표현하면, 시스템이 자동으로 "어떻게(How)" 네트워크를 구성할지 결정한다.

### 1.2 전통 네트워킹의 한계

| 단계 | 전통 네트워킹 | [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) |
|:---|:---|:---|
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | CLI [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수동 입력 | 비즈니스 의도 입력 |
| 구성 적용 | 장비별 수동 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 자동 변환·배포 |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 수동 핑 테스트 | 지속적 자동 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 장애 대응 | 수동 트러블슈팅 | 자동 자가 치유 |
| 규모 확장 | 선형적 관리 비용 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 재사용 |

### 1.3 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 동작 개요

```
비즈니스 의도 입력 예시:

"영업팀은 CRM 시스템에 99.9% 가용성으로 접근 가능해야 하며,
 의료 데이터는 반드시 암호화되어 전송되어야 한다."

                    v IBN 시스템

자동 생성 네트워크 정책:
  +- VLAN 분리: 영업팀 VLAN 100, 의료 VLAN 200
  +- QoS: 영업팀 CRM 트래픽 우선순위 높음
  +- 암호화: VLAN 200 모든 트래픽 TLS 강제
  +- 모니터링: 가용성 99.9% 미만 시 즉시 경보
```

📢 **섹션 요약 비유**: IBN은 "스마트 건물 관리 시스템"과 같다. "오전 9시 회의실은 20도로 유지"라고 말하면, 시스템이 보일러·에어컨·환기를 자동으로 조절한다. 관리자는 "무엇을"만 정하고, "어떻게"는 시스템이 해결한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 3단계 루프 아키텍처

```
+------------------------------------------------------------+
|                   IBN 핵심 루프                              |
|                                                            |
|  +-----------------------------------------------------+   |
|  |  1단계: 변환 (Translation)                           |   |
|  |                                                     |   |
|  |  비즈니스 의도 입력 -> 네트워크 정책으로 변환           |   |
|  |  자연어 / GUI / API -> 구성 명세 (Intent Spec)        |   |
|  +------------------------+----------------------------+   |
|                           |                                |
|  +------------------------v----------------------------+   |
|  |  2단계: 활성화 (Activation)                          |   |
|  |                                                     |   |
|  |  정책 검증 -> 충돌 감지 -> 네트워크 장비에 배포         |   |
|  |  SDN 컨트롤러 / 장비별 드라이버 통한 설정 적용        |   |
|  +------------------------+----------------------------+   |
|                           |                                |
|  +------------------------v----------------------------+   |
|  |  3단계: 보증 (Assurance)                             |   |
|  |                                                     |   |
|  |  실시간 모니터링 -> 의도 상태 검증 -> 이탈 시 자가 치유  |   |
|  |  AI/ML 기반 이상 감지 + 자동 재구성                  |   |
|  +------------------------+----------------------------+   |
|                           | 피드백 루프                     |
|                           +-------> 변환 단계으로 재입력      |
+------------------------------------------------------------+
```

### 2.2 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 구성요소 상세

| 구성요소 | 역할 | 기술 구현 |
|:---|:---|:---|
| [Intent](/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/) 엔진 (의도 엔진) | 의도 -> [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변환 | NLP, ML, 규칙 기반 |
| Network Controller (네트워크 컨트롤러) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) -> 장비 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 배포 | ONOS, OpenDaylight, [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) DNA |
| Network Analytics (네트워크 분석) | 실시간 상태 수집·분석 | Streaming Analytics, ML |
| [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Repository ([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 저장소) | 의도·[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 | Git 기반 |
| Simulation 엔진 (시뮬레이션) | 변경 전 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [Digital Twin](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) |

### 2.3 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 활용 영역

```
IBN에서 AI/ML 활용

1. 의도 해석 (NLP)
   "영업팀 트래픽 우선 보장" -> DSCP 46 마킹, 대역폭 보장

2. 트래픽 예측 (Time-series)
   과거 트래픽 패턴 -> 미래 혼잡 예측 -> 선제적 경로 최적화

3. 이상 감지 (Anomaly Detection)
   정상 베이스라인 모델링 -> 이탈 감지 -> 알림 또는 자동 수정

4. 자율 최적화 (Reinforcement Learning)
   트래픽 분산 환경에서 최적 라우팅 정책 자율 학습

5. 장애 예측 (Predictive Maintenance)
   장비 성능 지표 분석 -> 장애 발생 전 예방 조치
```

### 2.4 주요 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 제품 비교

| 제품 | 개발사 | 특징 |
|:---|:---|:---|
| [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) DNA Center | [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) | 엔터프라이즈 최다 채택, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Network Analytics |
| Juniper Apstra | Juniper Networks | 멀티벤더 지원, [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 특화 |
| VMware NSX-T | VMware | [소프트웨어 정의 네트워킹](/studynote/03_network/17_sdn_nfv/850_sdn_software_defined_networking_concept/), 마이크로세그멘테이션 |
| AWS Network Manager | AWS | 클라우드 WAN 자동화 |
| ONAP | Linux Foundation | 통신사 [NFV](/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/)/[SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 자동화 |

📢 **섹션 요약 비유**: IBN의 3단계 루프는 자동 온도 조절기(스마트 서모스탯)와 같다. "22도 유지"(의도 입력) -> 보일러·에어컨 가동(활성화) -> 온도 센서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(보증) -> 목표 달성 안되면 재조정(피드백)이 자동으로 반복된다.

---

## Ⅲ. 비교 및 연결

### 3.1 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) vs [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) vs 전통 네트워킹 비교

| 항목 | 전통 네트워킹 | [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) | [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) |
|:---|:---|:---|:---|
| [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 수준 | 하드웨어/CLI | 제어·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 분리 | 비즈니스 의도 수준 |
| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방법 | 장비별 CLI | 중앙 컨트롤러 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 자연어/[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| 자동화 | 없음 | 부분 자동화 | 완전 자동화 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용 | 없음 | 제한적 | 핵심 |
| 자가 치유 | 없음 | 제한적 | 포함 |
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 수동 | 제한적 | 자동 |
| 적합 환경 | 소규모 | [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) | 대규모 엔터프라이즈 |

### 3.2 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)([Network Slicing](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/))과 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 연계

```
5G 슬라이싱 + IBN 아키텍처

비즈니스 의도:
  "자율주행 차량에 5ms 이하 지연 보장"
  "스트리밍 서비스에 100Mbps 보장"
  "IoT 센서에 저전력 저대역 연결"

             v IBN이 자동 슬라이스 설정

+---------------------------------------------------+
|            5G 코어 네트워크                         |
|                                                   |
|  +--------------+ +--------------+ +------------+ |
|  | Slice 1      | | Slice 2      | | Slice 3    | |
|  | URLLC        | | eMBB         | | mMTC       | |
|  | (초저지연)    | | (고대역폭)    | | (대규모IoT)| |
|  | 자율주행      | | 스트리밍     | | 센서 통신  | |
|  | 5ms 이하     | | 100Mbps+    | | 저전력     | |
|  +--------------+ +--------------+ +------------+ |
+---------------------------------------------------+

IBN이 각 슬라이스 SLA(Service Level Agreement) 자동 모니터링
위반 시 리소스 자동 재할당
```

### 3.3 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 언어 예시

```yaml
# IBN 정책 정의 예시 (YAML 기반 의도 표현)

intent:
  name: "영업팀 CRM 우선 보장"
  description: "영업팀이 CRM 시스템에 안정적으로 접근"

  subjects:
    - group: "sales-team"
      location: "HQ-Building-A"

  resources:
    - system: "crm.company.com"
      port: 443

  requirements:
    availability: "99.9%"
    latency_max: "50ms"
    bandwidth_min: "10Mbps"

  security:
    encryption: "TLS 1.3"
    authentication: "MFA"

  priority: "HIGH"
```

📢 **섹션 요약 비유**: IBN의 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 슬라이싱 연계는 고속도로의 차선 관리와 같다. 응급차(자율주행, [URLLC](/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))에는 항상 비어있는 응급 차선을, 일반 차량(스트리밍, [eMBB](/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))에는 일반 차선을, 자전거([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [mMTC](/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))에는 자전거 도로를 자동으로 할당한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 도입 시나리오

| 시나리오 | [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 적용 방법 | 기대효과 |
|:---|:---|:---|
| [제로 트러스트 보안](/studynote/03_network/14_network_security_threats/738_zero_trust_architecture_least_privilege/) | 사용자 역할 기반 자동 [세그멘테이션](/studynote/02_operating_system/06_memory_management/364_segmentation/) | 공격 반경 최소화 |
| 멀티클라우드 연결 | 클라우드 간 WAN [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 자동 최적화 | 비용 30% 절감 |
| 재택근무 확대 | [SD-WAN](/studynote/03_network/16_data_center_cloud/849_sd_wan_software_defined_wide_area_network/) + IBN으로 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 품질 자동 보장 | 사용자 경험 향상 |
| 공장 자동화 | [OT](/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)(운영 기술) 네트워크 격리 자동화 | 보안 사고 예방 |

### 4.2 [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) DNA Center [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 구현

```
Cisco DNA Center 적용 예시

1. 의도 정의 (UI/API)
   보안 그룹 설정: "개발팀 ↔ 운영팀 통신 차단"

2. 정책 변환
   TrustSec 태그: DEV_GROUP=100, OPS_GROUP=200
   SGACL 정책: DENY DEV->OPS, DENY OPS->DEV

3. 배포
   ISE(Identity Services Engine) 연계
   스위치/라우터/무선AP에 자동 배포

4. 보증
   Network Assurance: 실시간 경로 추적
   AI-driven Issues: 자동 근원 원인 분석

5. 자가 치유
   연결 이상 감지 -> 대체 경로 자동 전환
   VLAN 충돌 감지 -> 자동 재구성
```

### 4.3 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 도입 성숙도 모델

```
IBN 도입 단계

0단계: 수동 관리
  +- CLI 명령어, 엑셀 관리

1단계: 자동화
  +- Ansible/Python 스크립트, 일부 자동화

2단계: SDN
  +- 중앙 컨트롤러, API 기반 관리

3단계: IBN 기초
  +- 정책 기반 관리, 분석 도구 도입

4단계: 완전 IBN
  +- AI 기반 의도 해석, 자가 치유, 예측 운영
```

### 4.4 기술사 논술 핵심 포인트

| 논점 | 핵심 내용 |
|:---|:---|
| [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) vs [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 차이 | SDN은 제어 분리, IBN은 의도 기반 자동화 추가 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 역할 | 의도 해석 + 이상 감지 + 자율 최적화 3가지 |
| [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 슬라이싱 연계 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 자동 보장 ([URLLC](/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)/[eMBB](/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/)/[mMTC](/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/)) |
| 보증(Assurance) 핵심 | 지속적 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 의도-현실 간격 [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) |

📢 **섹션 요약 비유**: IBN의 보증(Assurance) 단계는 비행기의 자동 항법 장치(오토파일럿)와 같다. 목적지(의도)를 입력하면 시스템이 기상 변화(네트워크 이상)에 맞춰 경로를 자동 조정하고, 조종사(관리자)는 전체 상황만 모니터링한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 도입 기대효과

| 효과 | 정량 지표 |
|:---|:---|
| 운영 비용 절감 | 수동 작업 70~80% 자동화 |
| 장애 평균 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)) | 4시간 -> 15분 (75% 감소) |
| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류 감소 | 인적 오류 90% 감소 |
| [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 100% [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 준수 보장 |
| 신규 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 배포 | 3주 -> 1일 (93% 단축) |

### 5.2 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 미래 발전 방향

```
IBN 진화 방향

현재 (2024):
  +- 엔터프라이즈 캠퍼스/데이터센터 자동화
  +- SDN 위에 정책 레이어 추가

단기 (2025~2027):
  +- 5G/6G 코어 네트워크 통합
  +- 멀티클라우드 의도 기반 연결
  +- AI-Native 네트워크 구성

장기 (2028+):
  +- 완전 자율 네트워크 (Autonomous Network)
  +- 자연어 인터페이스 (LLM + IBN)
  +- 제로 터치 프로비저닝 (ZTP) 완성
```

### 5.3 결론 요약

IBN은 복잡한 네트워크 운영을 비즈니스 의도 중심으로 단순화하고, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML로 자율 최적화·자가 치유를 실현하는 차세대 네트워킹 패러다임이다. 기술사 관점에서는 <strong><a href="/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/">IBN</a> vs SDN의 <a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a> 수준 차이, 변환-활성화-보증 3단계 루프, <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 슬라이싱과의 결합</strong>을 명확히 이해해야 한다.

📢 **섹션 요약 비유**: IBN은 네트워크 운영의 "자율 주행 자동차"다. 목적지(비즈니스 의도)를 입력하면 센서(모니터링)로 주변 상황을 파악하고, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진)가 최적 경로(네트워크 구성)를 실시간으로 조정하며 안전하게 목적지에 도달한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기술 | [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) ([Intent](/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/)-Based Networking) | 의도 기반 자율 네트워킹 |
| 3단계 루프 | Translation (변환) | 의도 -> 네트워크 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변환 |
| 3단계 루프 | Activation (활성화) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) -> 장비 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 배포 |
| 3단계 루프 | Assurance (보증) | 지속적 의도 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 기반 기술 | [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Networking) | 제어·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 분리 |
| 연계 기술 | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [Network Slicing](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) ([네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 네트워크 분리 |
| 제품 | [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) DNA Center | 엔터프라이즈 [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 플랫폼 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기능 | [Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/) (이상 감지) | 트래픽 이상 자동 감지 |
| 보안 | [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) ([제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) | [IBN](/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/) 기반 자동 [세그멘테이션](/studynote/02_operating_system/06_memory_management/364_segmentation/) |

### 👶 어린이를 위한 3줄 비유 설명

1. IBN은 스마트 집의 자동 조절 시스템이에요. "방을 22도로 유지해줘"라고 말하면, 보일러·에어컨·창문을 자동으로 조절해서 목표 온도를 맞춰요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 네트워크 관리 (CLI 기반 설정)
    |
    v
SDN (Software-Defined Networking): 제어 평면 분리
    |
    v
IBN (Intent-Based Networking)
    +-► 인텐트 정의: "웹 서버 -> DB 10ms 이내" (선언적)
    +-► 자동 변환: 인텐트 -> 네트워크 정책 -> 장비 설정
    +-► 지속 검증: 실시간 모니터링 · 의도 준수 확인
    |
    v
AI 기반 트래픽 라우팅
    +-► 트래픽 예측 · 경로 최적화
    +-► 자가 치유 (Self-Healing) 네트워크
```
2. IBN의 3단계는 요리사의 작업과 같아요. 레시피 이해(변환) -> 요리 실행(활성화) -> 맛 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(보증)이 계속 반복되고, 맛이 이상하면 자동으로 조리법을 수정해요.
3. [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 슬라이싱 + IBN은 고속도로 자동 차선 배정이에요. 응급차에는 항상 비어있는 차선을, 일반 차량에는 빈 차선을 자동으로 배정해 모두가 목적지에 빠르게 도달하게 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 199 / 258

<- **이전**: [198. 지식 증류 (Knowledge Distillation) 소프트 타겟 확률 분포 모방](/studynote/14_data_engineering/04_mlops/198_knowledge_distillation_soft_target_probability/)
**다음**: [200. 자율주행 모방 학습 (Imitation Learning) 시뮬레이터 디지털 트윈 합성 데이터 생성](/studynote/14_data_engineering/04_mlops/200_autonomous_driving_imitation_learning_digital_twin/) ->

---
