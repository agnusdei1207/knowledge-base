---
title: 184. 제로 트러스트 아키텍처 (Zero Trust Architecture)
date: '2026-05-06'
tags:
- studynote-it-management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 아키텍처 ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] [[319_architecture|Architecture]], [[047_zta|ZTA]])는 내부망 여부를 신뢰 근거로 삼지 않고, 모든 접근 요청마다 사용자·기기·워크로드·[[001_dikw_pyramid|데이터]] 민감도를 다시 평가하는 [[164_policy|정책]] 기반 보안 구조다.
> 2. **가치**: 원격근무, [[309_saas|SaaS]] (Software [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]), 멀티클라우드, 내부자 위협 환경에서 "한 번 [[983_vpn_virtual_private_network|VPN]] (Virtual Private Network)에 들어오면 넓게 허용"하던 경계 보안의 약점을 줄이고, 측면 이동(Lateral Movement)을 세밀하게 제한한다.
> 3. **판단 포인트**: ZTA는 [[552_mfa|MFA]] ([[552_mfa|Multi-Factor Authentication]]) 하나를 추가하는 제품이 아니라, PEP ([[164_policy|Policy]] Enforcement Point)·PDP ([[164_policy|Policy]] Decision Point)·세분화된 [[164_policy|정책]]·지속적 텔레메트리가 함께 돌아가는 운영 체계여야 효과가 난다.

---

## Ⅰ. 개요 및 필요성

전통적인 경계 보안([[936_perimeter_security|Perimeter Security]])은 "밖은 위험하고 안은 안전하다"는 가정 위에 세워졌다. 사내망과 인터넷 경계가 비교적 분명하고, 업무 시스템이 대부분 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 안에 있던 시기에는 이 모델이 일정 부분 통했다. 하지만 오늘날 사용자는 사무실뿐 아니라 재택·모바일·협력사 환경에서 접속하고, 업무 자산은 [[061_on_premise_legacy_infrastructure|온프레미스]]·클라우드·SaaS에 흩어져 있다. 더 이상 네트워크 위치만으로 신뢰를 결정하기 어려워졌다.

더 심각한 문제는 경계 내부에 들어온 뒤의 움직임이다. 공격자가 [[752_phishing|피싱]], 자격 증명 탈취, 취약한 [[983_vpn_virtual_private_network|VPN]], 내부자 오용을 통해 일단 내부 접근 권한을 얻으면, 넓게 열린 네트워크에서 다른 자산으로 이동하기 쉽다. 많은 침해 사고가 바로 이 측면 이동 단계에서 커졌다. 즉 경계 보안의 실패는 외부 침입 자체보다, **내부를 너무 넓게 신뢰한 설계**에서 자주 발생한다.

ZTA는 이 전제를 뒤집는다. 내부냐 외부냐가 아니라, 지금 이 요청이 누구의 것인지, 어떤 기기에서 왔는지, 자산 등급은 무엇인지, 최근 위협 [[130_signal|신호]]는 없는지, 현재 권한이 이 행위에 정말 필요한지까지 본다. 그래서 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]의 본질은 "아무도 못 믿는다"가 아니라, **신뢰를 위치에서 [[033_context|컨텍스트]]로 옮기는 것**이다.

- **📢 섹션 요약 비유**: 예전 보안이 회사 건물 현관에서 한 번만 사원증을 보는 방식이었다면, [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 중요한 층과 방마다 다시 확인하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

NIST (National Institute of Standards and Technology) [[166_sp|SP]] 800-207 기준으로 보면 ZTA의 중심은 [[164_policy|정책]] 결정과 [[164_policy|정책]] 집행의 분리다. 실제 접근을 허용하거나 차단하는 지점은 PEP이고, 그 결정을 내리는 두뇌는 PDP다. PDP 내부에는 [[164_policy|정책]] 엔진 PE ([[164_policy|Policy]] Engine)와 [[164_policy|정책]] 관리자 PA ([[164_policy|Policy]] Administrator)가 있고, 이들은 [[536_idp_identity_provider|IdP]] ([[536_idp_identity_provider|Identity Provider]]), 기기 상태, 위협 인텔리전스, [[808_data_classification|데이터 분류]], [[160_session_controlling_terminal|세션]] 이력 같은 [[130_signal|신호]]를 받아 판단한다.

아래 그림은 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]의 의사결정 루프를 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Zero Trust decision loop                                            │
├──────────────────────────────────────────────────────────────────────┤
│ Subject: user + device + workload                                   │
│        │ request                                                    │
│        ▼                                                            │
│ PEP (Policy Enforcement Point)                                      │
│        │ ask decision                                               │
│        ▼                                                            │
│ PDP (Policy Decision Point)                                         │
│   ├─ PE (Policy Engine): risk / context evaluation                  │
│   └─ PA (Policy Administrator): token / session issue               │
│        ▲                                                            │
│        │ signals                                                    │
│ IdP + MFA | device posture | threat intel | data sensitivity        │
│        │                                                            │
│        ▼                                                            │
│ allow / deny / step-up auth / short-lived session                   │
│        │                                                            │
│        ▼                                                            │
│ resource-specific access + continuous re-evaluation                 │
└──────────────────────────────────────────────────────────────────────┘
```

여기서 중요한 것은 "로그인 한 번으로 끝나지 않는다"는 점이다. [[160_session_controlling_terminal|세션]] 중에도 기기 보안 상태가 나빠지거나, 위치가 급변하거나, 이상 행위가 감지되면 접근을 다시 평가할 수 있어야 한다. 그래서 ZTA는 [[303_authentication_authorization_patterns|인증]]([[604_authentication_factors|Authentication]])뿐 아니라 권한 부여([[509_authorization_models_rbac_abac|Authorization]]), 세분화([[059_micro_segmentation_east_west_traffic|Micro-Segmentation]]), [[160_session_controlling_terminal|세션]] 수명 관리, 지속 관찰(Telemetry)을 한 묶음으로 본다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| PEP ([[164_policy|Policy]] Enforcement Point) | 접근 허용·차단을 실제 집행 | [[264_proxy_pattern_surrogate_access_control|프록시]], 게이트웨이, 에이전트 등 배치 위치가 중요 |
| PDP ([[164_policy|Policy]] Decision Point) | 접근 여부를 판단 | [[164_policy|정책]] 일관성과 응답 속도 확보 필요 |
| PE ([[164_policy|Policy]] Engine) | [[033_context|컨텍스트]] 기반 위험 평가 | 정적 규칙 + 동적 [[130_signal|신호]] 결합 |
| PA ([[164_policy|Policy]] Administrator) | [[160_session_controlling_terminal|세션]]·토큰 생성과 [[164_policy|정책]] 적용 | 짧은 수명 [[160_session_controlling_terminal|세션]], 즉시 철회 지원 |
| Device Posture | 기기 패치·[[325_edr|EDR]] (Endpoint [[961_deepfake_detection|Detection]] and Response) 상태 반영 | 미준수 기기 격리 |
| [[059_micro_segmentation_east_west_traffic|Micro-Segmentation]] | 자산 단위 세분화 | 내부 진입 후 측면 이동 최소화 |

ZTA를 강하게 만드는 핵심 문장은 "최소 권한([[010_least_privilege|Least Privilege]])을 지속적으로 계산한다"는 것이다. 따라서 단순히 [[983_vpn_virtual_private_network|VPN]] 뒤에 MFA를 붙인 것만으로는 충분하지 않다. 사용자가 한번 연결되면 내부망 대부분에 닿을 수 있다면, 신원은 강화되었어도 신뢰 모델은 여전히 경계 중심에 머문다.

- **📢 섹션 요약 비유**: ZTA는 경비원이 혼자 모든 결정을 내리는 건물이 아니라, 현관 경비가 본사 보안실에 계속 질의하면서 출입문마다 다른 규칙을 적용하는 구조와 같다.

---

## Ⅲ. 비교 및 연결

[[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 기존 경계 보안, [[983_vpn_virtual_private_network|VPN]], [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access), [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] (Secure Access [[090_service_kubernetes_network_load_balancing|Service]] Edge), [[048_sdp|SDP]] (Software Defined Perimeter)와 자주 함께 언급된다. 이때 가장 중요한 구분은 ZTA가 상위 원칙이고, [[339_ztna|ZTNA]]·[[048_sdp|SDP]]·SASE는 그 원칙을 구현하는 접근이라는 점이다.

| 구분 | 전통 경계 보안 | [[983_vpn_virtual_private_network|VPN]] 중심 접근 | [[047_zta|ZTA]] | [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] / [[048_sdp|SDP]] / [[339_ztna|ZTNA]] |
| :--- | :--- | :--- | :--- | :--- |
| 신뢰 기준 | 내부망 위치 | [[983_vpn_virtual_private_network|VPN]] 접속 성공 | 요청별 [[033_context|컨텍스트]] | [[047_zta|ZTA]] 구현 수단 |
| 접근 단위 | 네트워크 세그먼트 | 내부망 전체 또는 광범위 | 애플리케이션·[[001_dikw_pyramid|데이터]] 단위 | [[090_service_kubernetes_network_load_balancing|서비스]]별 세밀한 접속 |
| 재평가 | 거의 없음 | 접속 시 1회 중심 | 지속적 재평가 | 구현 방식에 따라 지원 |
| 측면 이동 방어 | 약함 | 보통~약함 | 강함 | [[047_zta|ZTA]] [[164_policy|정책]] 수준에 좌우 |
| 핵심 한계 | 내부 과신 | 연결되면 넓은 권한 | 설계·운영 복잡도 | 벤더 의존 가능성 |

[[164_policy|정책]] 모델 측면에서는 [[569_rbac|RBAC]] ([[569_rbac|Role-Based Access Control]])만으로는 부족할 때가 많다. ZTA는 사용자의 역할뿐 아니라 기기 등급, 위치, 시간, [[001_dikw_pyramid|데이터]] 민감도, 위험 점수를 함께 보므로 [[572_abac|ABAC]] ([[572_abac|Attribute-Based Access Control]])나 Risk-Based Access가 자주 결합된다. 즉 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 "누구인가"에 더해 "지금 어떤 상태인가"를 같이 묻는 구조다.

또한 망연계 시스템과의 연결도 생각할 수 있다. 망연계가 큰 경계 사이의 안전한 [[001_dikw_pyramid|데이터]] 이동 통로라면, ZTA는 그 통로를 지난 뒤에도 사용자·[[160_session_controlling_terminal|세션]]·리소스별 [[395_verification_process_review|검증]]을 계속 수행하는 원리다. 하나는 경계 운영, 다른 하나는 경계 이후까지 이어지는 지속 [[395_verification_process_review|검증]]이라고 볼 수 있다.

- **📢 섹션 요약 비유**: ZTA가 보안 철학이라면, ZTNA는 그 철학으로 만든 출입 시스템이고, SASE는 출입 시스템과 보안 장비를 클라우드에 묶어 놓은 종합 [[090_service_kubernetes_network_load_balancing|서비스]]에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[047_zta|ZTA]] 전환은 보통 "모든 것을 한 번에 바꾸는 프로젝트"가 아니라 성숙도 향상 여정으로 진행된다. 가장 먼저 해야 할 일은 사용자·기기·애플리케이션·[[001_dikw_pyramid|데이터]]의 [[655_ir_detection_analysis|식별]]과 [[104_classification_analysis|분류]]다. [[571_protection_vs_security|보호]] 대상이 무엇인지 모르면 어떤 요청을 어디에서 차단해야 할지도 정할 수 없다. 따라서 자산 목록, 계정 정리, 관리되지 않는 기기 파악이 출발점이다.

그다음은 고가치 자산을 중심으로 [[164_policy|정책]]을 좁혀 가는 방식이 현실적이다. 예를 들어 관리자 포털, 핵심 [[002_database_definition|데이터베이스]]([[501_database|Database]]), 개발자 배포 체계, 원격 접속 경로부터 [[552_mfa|MFA]], 기기 준수 검사, 최소 권한, 짧은 [[160_session_controlling_terminal|세션]], 세분화 [[164_policy|정책]]을 적용한다. 이후 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신(Workload Identity), [[001_dikw_pyramid|데이터]] 접근, 자동화 계정까지 확장하면 비로소 전사적 ZTA에 가까워진다.

| 단계 | 실무 초점 | 대표 통제 |
| :--- | :--- | :--- |
| 1단계: 가시화 | 자산·계정·기기 [[655_ir_detection_analysis|식별]] | [[526_iam|IAM]] (Identity and Access [[372_management|Management]]), 자산 인벤토리 |
| 2단계: 신원 강화 | 사용자 [[395_verification_process_review|검증]] 고도화 | [[552_mfa|MFA]], [[531_sso|SSO]] ([[531_sso|Single Sign-On]]), 비정상 로그인 탐지 |
| 3단계: 기기·[[160_session_controlling_terminal|세션]] 통제 | 준수 상태와 [[160_session_controlling_terminal|세션]] 수명 반영 | Device Posture, [[610_azure_ad_conditional_access|Conditional Access]] |
| 4단계: 자산 세분화 | 리소스 단위 최소 권한 | [[059_micro_segmentation_east_west_traffic|Micro-Segmentation]], [[339_ztna|ZTNA]] |
| 5단계: 지속 대응 | 이상 징후 기반 재평가 | [[624_siem|SIEM]] ([[283_security_tactics|Security]] Information and [[074_event_management|Event Management]]), [[745_soar_security_orchestration_automation_response|SOAR]] ([[283_security_tactics|Security]] [[073_container_orchestration_tools|Orchestration]], Automation, and Response) |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[571_protection_vs_security|보호]]해야 할 고가치 자산과 사용자 군이 명확한가?
2. [[983_vpn_virtual_private_network|VPN]] 연결 뒤에 넓은 내부망 접근이 그대로 남아 있지 않은가?
3. 사용자뿐 아니라 기기와 [[090_service_kubernetes_network_load_balancing|서비스]] 계정에도 신뢰 점수를 반영하는가?
4. [[164_policy|정책]] 변경 시 예외 승인, 비상 계정(Break-Glass), [[606_auditing_linux_auditd|감사]] 로그가 준비되어 있는가?
5. [[164_policy|정책]] 효과를 측정할 텔레메트리와 운영 대시보드가 있는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[552_mfa|MFA]] 도입만 하고 내부망 평면 구조는 그대로 두는 경우
- 기존 [[983_vpn_virtual_private_network|VPN]] 제품 이름만 바꿔 ZTA라고 부르는 경우
- [[001_dikw_pyramid|데이터]] 민감도 [[104_classification_analysis|분류]] 없이 모든 자산에 똑같은 [[164_policy|정책]]을 적용하는 경우
- 사용자 계정만 보고 [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[014_api_posix|API]] 호출이나 배치 계정을 놓치는 경우
- 운영 예외 절차가 없어 보안 우회와 불편을 동시에 만드는 경우

기술사 답안에서는 "Never Trust, Always Verify"라는 구호만 쓰기보다, **PEP/PDP 분리, 최소 권한, 기기 상태 반영, 지속적 재평가, 측면 이동 차단**을 구조적으로 설명해야 점수가 살아난다. 특히 ZTA는 보안 제품명보다 운영 원칙이라는 점을 분명히 적는 것이 중요하다.

- **📢 섹션 요약 비유**: 좋은 [[047_zta|ZTA]] 전환은 오래된 집의 모든 문을 하루아침에 바꾸는 일이 아니라, 가장 중요한 방부터 스마트 잠금장치와 출입 기록을 단계적으로 붙여 가는 작업과 같다.

---

## Ⅴ. 기대효과 및 결론

잘 구현된 ZTA는 공격자의 이동 반경을 줄이고, 정상 사용자의 접속도 더 설명 가능하게 만든다. 누가 어떤 기기에서 어떤 자산에 왜 접근했는지가 로그로 남고, 위험 [[130_signal|신호]]가 올라오면 [[160_session_controlling_terminal|세션]]을 줄이거나 추가 [[303_authentication_authorization_patterns|인증]]을 요구할 수 있다. 그래서 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]의 효과는 단순 차단률보다, **사고가 나더라도 피해를 좁게 묶는 능력**에서 크게 드러난다.

물론 비용과 복잡도는 분명하다. [[164_policy|정책]] 설계가 서투르면 사용자 경험이 나빠지고, 자산 [[104_classification_analysis|분류]]와 [[526_iam|IAM]] 정비 없이 도입하면 운영이 혼란스러워질 수 있다. 그러나 원격근무·클라우드·내부자 위협이 일상이 된 환경에서는 이 복잡도를 피하는 대신, 더 큰 사고 비용을 감수하게 된다.

결론적으로 ZTA는 "내부망을 더 안전하게 만드는 기술"이 아니라, **신뢰의 기준을 네트워크 위치에서 신원·기기·행동·[[001_dikw_pyramid|데이터]] 맥락으로 옮기는 아키텍처 전환**이다. 따라서 기억할 문장은 단순하다. "안에 있다고 믿지 말고, 지금 이 요청이 타당한지 계속 [[395_verification_process_review|검증]]하라."

- **📢 섹션 요약 비유**: [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 건물 한 번 들어왔다고 자유 출입을 허용하는 것이 아니라, 중요한 문마다 이유와 상태를 다시 확인하는 스마트 출입 체계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PEP ([[164_policy|Policy]] Enforcement Point) | 실제 접근 허용·차단을 집행하는 관문이다. |
| PDP ([[164_policy|Policy]] Decision Point) | [[033_context|컨텍스트]]를 바탕으로 [[164_policy|정책]] 결정을 내리는 두뇌다. |
| [[552_mfa|MFA]] ([[552_mfa|Multi-Factor Authentication]]) | 사용자 신원 강화를 위한 기본 통제지만 ZTA의 전부는 아니다. |
| [[059_micro_segmentation_east_west_traffic|Micro-Segmentation]] | 내부 진입 이후의 측면 이동을 줄이는 핵심 구조다. |
| [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access) | [[047_zta|ZTA]] 원칙을 원격 접근 경로에 구현한 대표 방식이다. |
| [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] (Secure Access [[090_service_kubernetes_network_load_balancing|Service]] Edge) | ZTA와 여러 보안 기능을 클라우드 엣지에서 통합하는 프레임워크다. |

### 📈 관련 키워드 및 발전 흐름도

```text
경계 기반 보안
    │
    ▼
원격근무 · SaaS · 클라우드 확산
    │
    ▼
내부망 과신의 한계 노출
    │
    ▼
MFA + Device Posture + Least Privilege
    │
    ▼
PEP / PDP 기반 Zero Trust Architecture
    │
    ▼
ZTNA + Micro-Segmentation + Continuous Telemetry
```

이 흐름은 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]가 단순한 [[303_authentication_authorization_patterns|인증]] 강화가 아니라, 경계 중심 신뢰 모델을 요청 중심 [[395_verification_process_review|검증]] 모델로 바꾸는 과정임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 학교 안에 들어왔다고 해서 아무 교실이나 들어가게 하지 않는 규칙이에요.
2. 문을 열 때마다 누구인지, 어떤 준비물을 가졌는지, 지금 들어가도 되는지 다시 확인해요.
3. 그래서 나쁜 사람이 한 번 안으로 들어와도 다른 방으로 쉽게 돌아다니지 못해요.
