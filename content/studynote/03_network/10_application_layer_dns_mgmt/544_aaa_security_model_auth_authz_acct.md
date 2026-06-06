---
title: "Authentication , Authorization , Accounting /"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AAA 보안 모델은 이름 해석과 네트워크 관리에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: AAA 보안 모델을 이해하면 가시성과 관리 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: AAA는 네트워크나 시스템의 자원에 접근하려는 주체(사용자, 디바이스, 프로세스)를 통제하기 위한 3단계 프레임워크다. <strong><a href="/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>)</strong>은 신원 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a> (<a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>)</strong>는 권한 부여, <strong>Accounting (과금/<a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a>)</strong>는 자원 사용량 측정 및 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기록을 의미한다.
- **필요성**: 보안의 가장 흔한 실패는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인)에만 집착하고 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)와 로깅을 소홀히 하는 데서 발생한다. 해커가 말단 직원의 아이디를 탈취해 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인에 성공([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))했더라도, 그 계정이 DB 삭제 권한이 없고([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 실패), 접속 시도 내역이 실시간으로 관제센터에 찍힌다면(로깅) 해커는 목적을 달성할 수 없다. 이처럼 단일 방어의 취약성을 보완하기 위해 3단계가 톱니바퀴처럼 얽혀 돌아가야 한다.
- **등장 배경**: ① 다이얼업/[ISP](/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) 시절 과금(돈을 받기 위한 시간 측정)의 필요성 대두 -> ② [RADIUS](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/), [TACACS](/studynote/03_network/10_application_layer_dns_mgmt/542_tacacs_plus_terminal_access_control_cisco/)+ 등 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 구현체 등장 -> ③ 내부자 위협 증가 및 컴플라이언스([Compliance](/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) 강화로 인한 강력한 권한 분리 및 사후 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit Trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/)) 철학의 정립.

```text
+-------------------------------------------------------------+
|               AAA 3단계 라이프사이클의 유기적 흐름도               |
+-------------------------------------------------------------+
|                                                             |
|   [방문자(User)] ----> (네트워크 접근 시도)                     |
|                                                             |
|       v                                                     |
|   1. Authentication (인증) : "당신은 누구인가?"               |
|       - 방법: 패스워드, 생체 인식, 2FA/MFA, PKI 인증서         |
|       - 결과: 신원 확인 완료 (티켓 발급)                        |
|                                                             |
|       v                                                     |
|   2. Authorization (인가) : "무엇을 할 수 있는가?"              |
|       - 방법: RBAC(역할 기반), ABAC(속성 기반), MAC/DAC 통제   |
|       - 결과: 읽기/쓰기, 특정 명령어 실행 권한 필터링 부여          |
|                                                             |
|       v                                                     |
|   3. Accounting (과금/감사) : "무엇을 하고 언제 나갔는가?"        |
|       - 방법: Syslog 전송, 세션 지속 시간 기록, 트래픽 양 측정     |
|       - 결과: 증적 자료(Audit Trail) 확보 및 비용 청구 근거 마련   |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** AAA는 순차적인 관문이다. 첫 번째 관문([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))을 통과하지 못하면 두 번째 관문은 열리지 않는다. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 통과한 주체라도 시스템 전체를 마음대로 헤집을 수 없다. 두 번째 관문([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))에서 "너는 영업팀이니까 고객 DB 조회 버튼만 활성화해줄게. 삭제 버튼은 비활성화야"라고 권한의 범위를 깎아낸다. 사용자가 버튼을 클릭하는 순간순간의 모든 행위는 세 번째 관문([감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))을 통해 실시간으로 뒷단 서버에 영구 기록되어, 추후 해킹 사고가 터졌을 때 범인을 잡아내는 100% 확실한 법적 증거 자료가 된다.

- **📢 섹션 요약 비유**: 클럽 입구에서 민증을 검사하는 것([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), 들어가서 일반석에만 머물고 VIP 룸에는 못 들어가게 막는 것([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)), 그리고 퇴장할 때 마신 술값을 정확히 계산해서 영수증을 청구하는 것(과금)이 하나로 합쳐진 완벽한 영업 방침과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### AAA 구성 요소와 구현 기술

| 단계 | 철학적 의미 | 핵심 원리 및 기법 | 관련 시스템 및 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>)</strong> | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)과 증명 | 사용자가 제시한 정보(Something you know, have, are)를 중앙 DB와 대조 | AD, [LDAP](/studynote/03_network/10_application_layer_dns_mgmt/543_ldap_lightweight_directory_access_protocol/), 생체인증, [OTP](/studynote/01_computer_architecture/15_advanced_topics/748_otp/) (2FA), [RADIUS](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) | 문지기의 신원 조회 |
| <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a> (<a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>)</strong> | [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)된 주체의 직급, 접속 위치, 시간([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))을 조합해 자원 접근을 수락/거절 | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/), [ABAC](/studynote/09_security/11_iam_access_control/572_abac/), [TACACS](/studynote/03_network/10_application_layer_dns_mgmt/542_tacacs_plus_terminal_access_control_cisco/)+, [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) ISE, [IAM](/studynote/09_security/11_iam_access_control/526_iam/) | 출입증 등급 부여 (일반/특급) |
| <strong>Accounting (과금/<a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a>)</strong> | 불가쟁성 확보 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 시점부터 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)아웃 시점까지의 패킷, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 량, 실행한 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 기록 | [RADIUS](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) Accounting, [Syslog](/studynote/03_network/10_application_layer_dns_mgmt/535_syslog_protocol_udp_514/), [SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/), [Splunk](/studynote/09_security/13_secops_ir_forensics/630_splunk/) | 블랙박스 및 영수증 |

### AAA의 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)) 모델 깊이 파보기 ([RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) vs [ABAC](/studynote/09_security/11_iam_access_control/572_abac/))

AAA에서 가장 고도화하기 어려운 단계가 바로 <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>(<a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a>)</strong>다. 단순히 "들어와도 좋다"가 아니라 "어디까지 만져도 좋은가"를 규칙으로 짜야 하기 때문이다.

```text
+---------------------------------------------------------------+
|               인가(Authorization) 접근 통제 모델의 진화          |
+---------------------------------------------------------------+
|                                                               |
|   [1세대] DAC (임의적 접근 통제)                                 |
|   - 철학: "내가 만든 파일이니까 내가 권한을 줄게!"                   |
|   - 취약점: 주인이 바이러스에 걸려 남에게 권한을 넘기면 통제 불능.       |
|                                                               |
|   [2세대] MAC (강제적 접근 통제)                                 |
|   - 철학: "개인은 권한 못 정해! 국가 기밀(Top Secret) 등급표에 따라!" |
|   - 취약점: 군대, 정부기관 외의 일반 기업이 쓰기엔 너무 딱딱하고 무거움. |
|                                                               |
|   [3세대] RBAC (역할 기반 접근 통제) - 현재 기업의 표준            |
|   - 철학: "사람한테 권한 주지 마! '팀장'이라는 역할에 권한을 줘!"       |
|   - 장점: 직원이 퇴사/이동해도 그 직원의 역할(Role) 뱃지만 떼면 됨.   |
|                                                               |
|   [4세대] ABAC (속성 기반 접근 통제) - Zero Trust의 핵심           |
|   - 철학: "팀장이라도 밤 12시에 카페 Wi-Fi로 접속하면 차단해!"         |
|   - 장점: 직급(Role) + 접속 위치 + 디바이스 보안 상태 등 환경(Context) |
|           속성을 모두 융합하여 동적으로 권한을 계산함.                 |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))의 역사는 권한을 부여하는 기준을 바꾸어온 역사다. 오늘날 대부분의 사내 시스템과 클라우드(AWS [IAM](/studynote/09_security/11_iam_access_control/526_iam/))는 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)(역할 기반)을 채택하고 있다. 하지만 클라우드 리모트 워크 시대로 접어들며, 정상적인 계정과 역할을 가진 직원의 노트북이 해킹당하는 사례가 속출했다. 이를 막기 위해 최신 AAA 아키텍처는 사용자 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)뿐 아니라 '디바이스가 백신을 켰는가?', '접속 위치가 평소와 다른 국가인가?'를 종합적으로 따져 권한을 실시간으로 깎거나 거부하는 [ABAC](/studynote/09_security/11_iam_access_control/572_abac/)([속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반)으로 진화하여 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/))의 두뇌 역할을 하고 있다.


1. **상황**: 대기업의 영업사원이 카페 공용 와이파이를 통해 정상적으로 사내망 VPN에 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/))하고 들어와 기밀 도면 파일을 대량으로 다운로드하고 있다. 기존 AAA 모델에서는 "[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 한 번 통과하면" [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)이 끝날 때까지 모든 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 권한이 열려 있어 유출을 막지 못했다.
2. **원인**: 낡은 AAA 아키텍처는 <strong>1회성 <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 및 고정적 <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>(Static <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a>)</strong>에 의존했다. 성문을 한 번 통과한 성 안의 사람은 절대 악당이 아니라는 성선설에 기반한 것이다.
3. **의사결정 및 조치 (CARTA / Continuous AAA 도입)**:
   - 보안 아키텍트는 지속적 적응형 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 신뢰 평가(CARTA, Continuous Adaptive [Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) and Trust Assessment) 개념을 AAA에 결합한다.
   - 직원이 VPN에 들어온 후라도, [EDR](/studynote/09_security/04_endpoint_security/325_edr/)(단말 보안) 요원과 AAA 서버가 통신하여 단말기의 위험도를 1분마다 측정한다.
   - 직원이 갑자기 평소에 안 보던 기밀 도면을 단기간에 100개 이상 열람(비정상 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 변화 탐지)하면, [ABAC](/studynote/09_security/11_iam_access_control/572_abac/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 이를 인지한다.
   - AAA [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 서버가 강제로 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))를 박탈하여 해당 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 그 즉시 끊어버리거나 추가 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([MFA](/studynote/09_security/11_iam_access_control/552_mfa/) [OTP](/studynote/01_computer_architecture/15_advanced_topics/748_otp/) 입력)을 요구하는 <strong>동적 <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>(Dynamic <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a>)</strong> 파이프라인을 구축했다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>AAA 서버 (<a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 엔진) <a href="/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/">이중화</a></strong>: AAA 서버가 다운되면 사내의 모든 네트워크 장비, [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/), 와이파이가 사용자의 접근을 차단하게 된다. 이는 치명적인 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))이다. 메인 데이터센터와 재해복구([DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)) 센터에 AAA 서버를 액티브-스탠바이(Active-Standby) 또는 액티브-액티브(Active-Active)로 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)하고 장애 조치([Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)) 테스트를 정기적으로 수행해야 한다.
- <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)) 체계를 너무 복잡하게(예: 비밀번호 특수문자 4개 섞어 15자리, 매월 변경) 만들어 사용자의 불편함을 극대화하는 행위. 사용자는 비밀번호를 포스트잇에 적어 모니터에 붙여두게 되고, 이는 소셜 엔지니어링 공격에 가장 먼저 털리는 구멍이 된다. 현대의 AAA는 비밀번호를 없애고(Passwordless), 지문/FIDO 및 기기 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 기반으로 전환하되 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))와 모니터링(Accounting)을 두텁게 쌓는 방향으로 설계해야 한다.

- **📢 섹션 요약 비유**: 옛날에는 성문에서 통행증을 꼼꼼히 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 나면 성 안에서 칼을 휘둘러도 아무도 신경 쓰지 않았지만(구형 AAA), 이제는 성 안을 돌아다니는 내내 암행어사가 실시간으로 행동을 감시하다 수상하면 그 즉시 통행증을 빼앗아 쫓아내는(동적 AAA) 스마트한 성곽 방어 시스템으로 진화했습니다.

---

## Ⅲ. 비교 및 연결

이론적 모델인 AAA를 실제 네트워크 장비와 서버 사이의 소프트웨어로 구현해낸 3대 통신 규격의 차이를 파악해야 한다.

| 비교 기준 | [RADIUS](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) (1세대 범용) | [TACACS](/studynote/03_network/10_application_layer_dns_mgmt/542_tacacs_plus_terminal_access_control_cisco/)+ (인프라 관리용) | Diameter (차세대 4G/[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신망) |
|:---|:---|:---|:---|
| **기본 사상** | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 결합 (속도 중시) | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)/과금 분리 (정밀 제어) | [3GPP](/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 모바일 네트워크 [로밍](/studynote/03_network/11_wireless_mobile_communication/560_roaming/)([Roaming](/studynote/03_network/11_wireless_mobile_communication/560_roaming/)) 등 초대규모 확장성 |
| **전송 계층** | [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) (오버헤드 적음) | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 높음) | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) / [SCTP](/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/) (초고신뢰, 멀티호밍 지원) |
| **보안 (암호화)** | 패스워드만 암호화 | 패킷 본문 전체 암호화 | [IPsec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) / [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 필수 결합 구조 |
| **적용 타겟** | 무선랜 802.[1X](/studynote/03_network/11_wireless_mobile_communication/584_802_1x_pnac_eap_radius/), 사내 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | 라우터/[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 관리자 접속 통제 | [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) / [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어망 가입자 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 및 과금(Billing) 인프라 |
| <strong>메시지 <a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | 응답 없으면 클라이언트가 재전송 | TCP가 알아서 재전송 보장 | [SCTP](/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/) 기반 패킷 순서 보장, 헤더 레벨 실패 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |

RADIUS는 가볍고 대중적이어서 기업의 와이파이나 VPN에 깔려 있다. [TACACS](/studynote/03_network/10_application_layer_dns_mgmt/542_tacacs_plus_terminal_access_control_cisco/)+는 시스코 장비 등 핵심 뼈대를 만지는 소수 엘리트들의 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 오타를 막기 위해 존재한다. Diameter는 이름(반지름 Radius의 두 배인 지름)에서 알 수 있듯, 수천만 대의 스마트폰이 기지국 사이를 이동([핸드오버](/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/))할 때마다 과금과 권한을 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 처리하기 위해 통신사(Telco) 뼈대에 박혀있는 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

```text
+---------------------------------------------------------------+
|               Accounting (과금/감사)의 포렌식 추적 시각화            |
+---------------------------------------------------------------+
|                                                               |
|   [해커의 내부망 침투 후 행동]                                     |
|   (해커) Router# config t      -------(TACACS+ Acct 전송)-------> |
|   (해커) Router(config)# user admin root  -(Acct 전송)------> |
|   (해커) Router# clear logging -------(Acct 전송)-------> |
|          (해커: "장비에 남은 내 흔적 다 지웠다! 완전 범죄!")               |
|                                                               |
|   [중앙 SIEM / AAA 감사 서버] (해커가 접근 불가능한 별도 서버)           |
|   | 시간       | 사용자 | 행위             | 결과      |         |
|   | 10:01:00  | jdoe  | config t       | Success  |         |
|   | 10:01:05  | jdoe  | user admin...  | Success  | <- 증거 확립!|
|   | 10:01:10  | jdoe  | clear logging  | Success  |         |
|   => 해커가 로컬(라우터) 장비의 로그를 지워도, AAA 회선을 타고 실시간으로  |
|      날아간 중앙 서버의 로그(Accounting)는 지울 수 없다!               |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** 초보 해커들은 해킹 성공 후 장비 내부의 접속 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(`clear logging`)를 지우면 흔적이 사라진다고 믿는다. 그러나 AAA 아키텍처가 제대로 구현된 인프라에서는 사용자가 엔터를 치는 그 밀리초(ms) 단위의 순간에 Accounting 패킷이 별도의 강력하게 보호된 중앙 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 수집기([SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/))로 실시간 복사되어 날아간다. 해커가 침투한 말단 장비의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 포맷해버린다 한들, 이미 AAA 서버에는 해커의 모든 키보드 타이핑 내역이 박제되어 있다. 이것이 Accounting이 단순 통계용을 넘어 궁극의 보안 방어선이자 '불가쟁성(Non-repudiation)'을 제공하는 이유다.

- **📢 섹션 요약 비유**: 도둑이 은행 지점의 [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 테이프를 훔쳐 갔지만, 이미 그 화면이 실시간으로 본사 클라우드 서버에 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)(Accounting)되고 있어서 경찰이 1시간 만에 도둑을 잡는 것과 같은 원리입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 AAA 보안 모델을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [LDAP](/studynote/03_network/10_application_layer_dns_mgmt/543_ldap_lightweight_directory_access_protocol/) 수준의 기본 대책으로 충분한지, 아니면 AAA 보안 모델이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 가시성 부족인지, 관리 자동화 악화인지 먼저 분리한다.
2. AAA 보안 모델가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- AAA 보안 모델의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- LDAP와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: AAA 보안 모델을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | AAA 부재 및 파편화 환경 | 중앙 통합 AAA 모델 구현 환경 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 추적)</strong> | 보안 사고 발생 시 파편화된 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 수집에 수일 소요 | 중앙 서버에 모든 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/행위 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 즉시 수합 | 포렌식 조사 소요 시간 **90% 이상 단축** |
| **정량 (비용 과금)** | 통신 인프라 초과 사용량 청구 분쟁 빈발 | Accounting 패킷 기반 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)/초 단위 정확한 과금 | 빌링(Billing) 누락 [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) 및 비용 투명성 **100% 확보** |
| **정성 (보안 통제력)** | 공유 계정 사용으로 내부망 침해 시 책임 소재 불분명 | [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)([RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)) 및 개인별 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 강제 | 내부자 위협 억제력 극대화 및 [ISMS](/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 심사 완벽 통과 |

### 미래 전망 및 진화 방향
- <strong>클라우드 <a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> (Identity and Access <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)과의 통합</strong>: 기업 인프라가 AWS, Azure 같은 퍼블릭 클라우드로 넘어가면서, 네트워크 장비 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(L2/L3) 통제 중심이었던 AAA의 철학은 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 함수, 클라우드 스토리지(S3) 버킷의 권한 통제를 지휘하는 거대한 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진으로 흡수 진화하고 있다.
- <strong><a href="/studynote/10_ai/03_llm_nlp/231_ai_turing_test/">인공지능</a>(<a href="/studynote/09_security/12_identity_threat_advanced/613_ueba/">UEBA</a>) 결합 로깅 (Accounting)</strong>: 수십 기가바이트씩 쌓이는 Accounting [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 사람이 눈으로 보는 시대는 끝났다. 향후의 AAA는 사용자 및 엔티티 행동 분석([UEBA](/studynote/09_security/12_identity_threat_advanced/613_ueba/), User and Entity Behavior Analytics) [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 엔진과 결합하여, 사용자의 평소 접속 패턴(출퇴근 시간, 주로 접속하는 IP)과 다른 아주 미세한 변형 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 찍히는 순간 선제적으로 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)(Authz)를 차단하는 자율 방어 체계로 진화할 것이다.

### 참고 표준
- **ISO/IEC 27001**: 정보보호 관리체계 국제 표준 (접근 통제의 필수 요구사항으로 AAA 사상 명시)
- <strong><a href="/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/">NIST SP 800-207</a></strong>: [Zero Trust Architecture](/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/) (동적 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 및 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 모델에 대한 미국 표준 가이드)

컴퓨터 과학에서 시스템 아키텍처는 수없이 변해왔지만, "너는 누구고, 무엇을 할 수 있으며, 무슨 짓을 했는가"라는 질문(AAA)은 절대 변하지 않는 철학적 본질이다. 통신선이 구리선에서 광케이블로, 다시 무선과 우주 통신으로 바뀐다 해도 AAA의 삼위일체는 네트워크를 지키는 가장 견고한 방패로 영원히 남을 것이다.

- **📢 섹션 요약 비유**: 건물의 형태가 오두막에서 수백 층짜리 최첨단 스마트 빌딩으로 바뀐다 해도, 입구에서 신분을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), 갈 수 있는 층수를 엘리베이터에 제한하며([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)), 복도의 CCTV로 흔적을 남기는([감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)) 경비의 3법칙은 영원히 변하지 않는 절대 진리입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LDAP](/studynote/03_network/10_application_layer_dns_mgmt/543_ldap_lightweight_directory_access_protocol/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) | 이름과 주소를 연결해 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 접근성을 만든다. |
| 모니터링 (Monitoring) | 장애 징후를 조기에 발견하기 위한 기초다. |
| [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: LDAP]
    |
    v
[현재 개념: AAA 보안 모델]
    |
    +---> [확장 A: 커버로스]
    +---> [확장 B: 자율 운영 네트워크]
```

AAA 보안 모델는 LDAP에서 출발해 현재 메커니즘을 정교화하고, 이후 [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)와 자율 운영 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. AAA 모델은 놀이공원의 완벽한 3단계 경비 시스템이에요. 첫 번째([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))는 입구에서 "너 표 샀어?" 하고 신분증을 꼼꼼히 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 과정이에요.
2. 두 번째([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))는 놀이공원 안에서 무서운 롤러코스터를 탈 때 "너 키가 130cm 넘어? 넌 회전목마만 타!" 하고 탈 수 있는 놀이기구 권한을 나누어 주는 거예요.
3. 세 번째(과금/[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))는 나갈 때 "너 오늘 츄러스 2개 먹고 사파리 3번 탔지?" 하고 영수증을 뽑아서 네가 한 모든 행동을 다 기록해두는 완벽한 일기장 같은 거랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 665 / 1120

<- **이전**: [543. LDAP (Lightweight Directory Access Protocol)](/studynote/03_network/10_application_layer_dns_mgmt/543_ldap_lightweight_directory_access_protocol/)
**다음**: [545. 커버로스 (Kerberos)](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) ->

---
