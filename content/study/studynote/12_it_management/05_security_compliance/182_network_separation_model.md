+++
weight = 182
title = "182. 망분리 (Network Separation) 모델"
date = "2026-05-06"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 망분리 (Network Separation)는 인터넷 접속 구간과 핵심 업무 구간을 물리적 또는 [[369_logic_bomb|논리]]적으로 분리해, 외부 침입과 내부 확산 경로를 구조적으로 줄이는 [[302_security_architecture_design|보안 아키텍처]] 모델이다.
> 2. **가치**: [[730_ransomware|랜섬웨어]], [[748_apt|APT]] ([[374_apt|Advanced Persistent Threat]]), 자격증명 탈취가 인터넷 구간에서 발생하더라도 업무망으로 곧바로 넘어가지 못하게 하므로, 고가치 정보와 규제 대상 시스템 [[571_protection_vs_security|보호]]에 매우 효과적이다.
> 3. **판단 포인트**: 물리적 망분리는 가장 강력하지만 비용·불편이 크고, [[369_logic_bomb|논리]]적 망분리인 [[079_developer_cleanroom_vdi_security|VDI]] (Virtual Desktop Infrastructure)와 SBC (Server-Based Computing)는 유연하지만 [[015_virtualization|가상화]] 보안과 단말 통제가 전제되므로, [[001_dikw_pyramid|데이터]] 중요도·업무 편의성·원격근무·클라우드 구조까지 함께 보고 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

망분리는 "방화벽을 하나 더 두는 것"보다 강한 개념이다. 방화벽은 연결을 통제하지만, 망분리는 애초에 연결 경로 자체를 분리하거나 극도로 제한한다. 즉 인터넷 브라우징, 메일 수신, 외부 다운로드가 일어나는 구간과 [[781_personal_information|개인정보]]·원천 코드·핵심 업무 시스템이 있는 구간을 분리해 공격 표면을 다르게 관리하는 모델이다.

이 개념이 필요한 이유는 현대 공격이 경계 하나를 뚫는 데서 끝나지 않기 때문이다. [[752_phishing|피싱]] 메일이나 악성 사이트로 단말이 감염되면, 공격자는 그 단말을 발판으로 내부 시스템을 탐색하고 계정 정보를 탈취하며 측면 이동(Lateral Movement)을 시도한다. 인터넷과 업무망이 같은 단말·같은 네트워크 경로 위에 있으면 침입 이후 확산 속도가 매우 빨라진다.

망분리는 그래서 "침입을 완전히 막는다"보다 "침입 이후 이동 경로를 짧게 끊는다"는 관점에서 중요하다. 특히 금융, 공공, 국방, 대규모 [[781_personal_information|개인정보]] 처리 조직처럼 단 한 번의 내부 확산이 대형 사고로 이어질 수 있는 환경에서는 여전히 유효한 기본 아키텍처다.

- **📢 섹션 요약 비유**: 망분리는 학교 운동장 문이 열려 있어도 교무실과 시험지 보관실까지 한 번에 들어갈 수 없도록 복도를 따로 잠가 두는 구조와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

망분리 모델은 보통 네 가지 구역으로 구성된다. 인터넷 구역, 업무 구역, 망연계 구역, 관리 구역이다. 핵심은 단순히 두 네트워크를 나누는 데서 끝나지 않고, [[501_file_definition_logical_record|파일]] 이동·패치·관리자 접속·원격 접속이 어느 경로로 허용되는지까지 설계하는 데 있다. 실무에서 사고가 나는 지점도 대부분 이 "예외 경로"다.

| 구역 / 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 인터넷망 | 웹, 메일, 외부 [[090_service_kubernetes_network_load_balancing|서비스]] 접속 | 감염 가능성을 전제로 모니터링·격리 강화 |
| 업무망 | [[081_erp_enterprise_resource_planning|ERP]] ([[081_erp_enterprise_resource_planning|Enterprise Resource Planning]]), [[002_database_definition|데이터베이스]]([[501_database|Database]]), 개발 자산, [[781_personal_information|개인정보]] 처리 | 인터넷 직접 연결 차단, 최소 권한 접속 |
| [[183_network_linkage_system|망연계 시스템]] | [[501_file_definition_logical_record|파일]]·[[001_dikw_pyramid|데이터]] 이동의 공식 통로 | 악성코드 검사, [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]), CDR (Content Disarm and Reconstruction), 승인 [[568_logs_distributed_logging_elk_fluentd|로그]] |
| 관리망 / 관리자 단말 | 운영·배포·점검 경로 | 인터넷 단말과 분리, 고권한 계정 [[571_protection_vs_security|보호]] |
| [[079_developer_cleanroom_vdi_security|VDI]] (Virtual Desktop Infrastructure) / SBC (Server-Based Computing) | [[369_logic_bomb|논리]]적 망분리 구현 수단 | 화면 전송만 허용하고 [[001_dikw_pyramid|데이터]]는 서버 측 잔류 |

아래 그림은 망분리가 단순한 "두 박스"가 아니라, [[001_dikw_pyramid|데이터]] 이동과 관리 경로까지 포함하는 모델이라는 점을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Network separation reference model                                   │
├──────────────────────────────────────────────────────────────────────┤
│ [Internet Zone]                                                      │
│   web / mail / browsing                                              │
│        │                                                             │
│        │ controlled access only                                      │
│        ▼                                                             │
│ ┌──────────────────┐    inspect / approve    ┌────────────────────┐  │
│ │ Secure Transfer  │<----------------------->│ Review / Logging    │  │
│ │ scan, DLP, CDR   │                         │ approval workflow   │  │
│ └────────┬─────────┘                         └────────┬───────────┘  │
│          │ one-way or tightly controlled flow                  │      │
│          ▼                                                     │      │
│ [Business Zone]                                                │      │
│   ERP / DB / source code / personal data                       │      │
│          ▲                                                     │      │
│          │ admin only from separated management zone           │      │
│          │                                                     │      │
│  Physical model : separate PC + switch + line                  │      │
│  Logical model  : VDI / SBC session on controlled endpoint     │      │
└──────────────────────────────────────────────────────────────────────┘
```

물리적 망분리는 단말, [[238_switch_operation_principles|스위치]], 회선까지 분리하므로 보안 강도가 가장 높다. 반면 [[369_logic_bomb|논리]]적 망분리는 단말 한 대에서 [[079_developer_cleanroom_vdi_security|VDI]] (Virtual Desktop Infrastructure)나 SBC (Server-Based Computing)를 이용해 업무 [[160_session_controlling_terminal|세션]]을 별도 환경으로 제공한다. 이 경우 [[001_dikw_pyramid|데이터]]는 중앙 서버에 남기고 화면만 전달하므로 편의성과 중앙 통제가 좋아지지만, [[054_hypervisor|하이퍼바이저]]·원격 [[295_protocol_field_tcp_udp_icmp|프로토콜]]·클립보드·[[359_usb|USB]] 제어 같은 추가 통제가 반드시 따라와야 한다.

- **📢 섹션 요약 비유**: 망분리 아키텍처는 큰 집을 벽 하나로만 나누는 게 아니라, 현관·택배실·관리실까지 각각 다른 출입 규칙으로 운영하는 집 구조와 같다.

---

## Ⅲ. 비교 및 연결

망분리에서는 "물리 vs [[369_logic_bomb|논리]]"만 외우면 절반만 이해한 셈이다. 물리적 망분리, [[079_developer_cleanroom_vdi_security|VDI]] 기반 [[369_logic_bomb|논리]]적 망분리, SBC 기반 [[369_logic_bomb|논리]]적 망분리, 그리고 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 기반 내부 세분화는 역할이 서로 다르다.

| 비교 축 | 물리적 망분리 | [[369_logic_bomb|논리]]적 망분리 ([[079_developer_cleanroom_vdi_security|VDI]]) | [[369_logic_bomb|논리]]적 망분리 (SBC) | [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] / [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access) |
| :--- | :--- | :--- | :--- | :--- |
| 분리 단위 | 단말·회선·[[238_switch_operation_principles|스위치]] | 가상 데스크톱 | 서버 [[160_session_controlling_terminal|세션]] | 사용자·기기·애플리케이션 단위 |
| 보안 강도 | 가장 강함 | 높음 | 중간 | 내부 접근 통제에 강함 |
| 사용자 편의성 | 낮음 | 높음 | 높음 | [[164_policy|정책]] 설계에 따라 다름 |
| 운영 비용 | 높음 | 중간 | 중간 이하 | 도구와 [[164_policy|정책]] 성숙도에 좌우 |
| 주된 목적 | 외부 경로 원천 차단 | 편의성과 중앙 통제의 균형 | 비용 효율적 중앙화 | 내부 신뢰 최소화 |

여기서 중요한 경계는 "망분리 ≠ [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]"라는 점이다. 망분리는 외부 인터넷과 업무 구역 사이의 큰 경계를 다루고, [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 내부에서도 매번 인증과 권한 [[395_verification_process_review|검증]]을 요구한다. 즉 망분리가 동서남북 성문을 나누는 구조라면, [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 성 안에서도 방마다 열쇠를 다시 확인하는 방식이다.

또한 망분리는 반드시 망연계와 함께 봐야 한다. 업무상 [[501_file_definition_logical_record|파일]]이나 [[001_dikw_pyramid|데이터]]가 오갈 수밖에 없다면, 그 이동을 어디까지 허용할지와 어떤 검사 절차를 둘지가 실질 보안 수준을 결정한다. 그래서 많은 조직에서 실제 사고는 망분리 자체가 아니라, 예외적으로 열어 둔 연계 경로에서 발생한다.

- **📢 섹션 요약 비유**: 물리적 망분리가 다른 건물로 이사하는 수준이라면, [[369_logic_bomb|논리]]적 망분리는 같은 건물 안의 보안실을 쓰는 방식이고, [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 그 보안실 안에서도 매번 출입증을 다시 찍게 하는 규칙이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 [[571_protection_vs_security|보호]] 대상과 업무 방식을 분리해 판단해야 한다. 국가기밀, 제어 시스템, 대규모 [[781_personal_information|개인정보]]처럼 인터넷 경로를 원천 차단해야 하는 대상은 물리적 망분리가 적합하다. 반면 일반 사무, 개발, 콜센터처럼 사용자 경험과 중앙 관리가 중요한 환경은 [[079_developer_cleanroom_vdi_security|VDI]] 기반 [[369_logic_bomb|논리]]적 망분리가 현실적이다.

| 실무 상황 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 기밀 자료·국방·산업 제어 | 물리적 망분리 우선 | 최대한 경로를 줄이는 것이 핵심 |
| 일반 행정·금융 사무 | [[079_developer_cleanroom_vdi_security|VDI]] 기반 [[369_logic_bomb|논리]]적 망분리 | 보안과 생산성의 균형 |
| 소규모 조직·표준 업무 | SBC 검토 | 비용 효율과 중앙 운영에 유리 |
| 클라우드 중심 업무 | 가상 네트워크 분리 + [[079_developer_cleanroom_vdi_security|VDI]] + [[339_ztna|ZTNA]] 병행 | 단순 서브넷 분리만으로는 부족 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 인터넷망과 업무망 사이의 공식 [[001_dikw_pyramid|데이터]] 이동 경로가 문서화되어 있는가?
2. [[183_network_linkage_system|망연계 시스템]]에 악성코드 검사, [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]), 승인 이력, 전송 [[568_logs_distributed_logging_elk_fluentd|로그]]가 있는가?
3. 관리자 단말은 인터넷 브라우징 단말과 분리되어 있는가?
4. [[369_logic_bomb|논리]]적 망분리라면 클립보드, 프린트, [[359_usb|USB]], 스크린 캡처 [[164_policy|정책]]을 명확히 통제하는가?
5. 클라우드 환경에서도 Private Subnet, Bastion, [[079_developer_cleanroom_vdi_security|VDI]], 보안 그룹, [[339_ztna|ZTNA]] [[164_policy|정책]]을 함께 설계했는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 인터넷망과 업무망을 한 단말에 동시에 물려 놓고 망분리라고 부르는 형식적 설계
- [[369_logic_bomb|논리]]적 망분리 환경에서 클립보드·[[501_file_definition_logical_record|파일]] 드래그·[[359_usb|USB]] 예외를 무분별하게 허용하는 운영
- 관리자 계정이 인터넷 메일과 업무 시스템을 같은 단말에서 모두 사용하는 구조
- 내부망은 안전하다고 가정해 [[325_edr|EDR]] (Endpoint [[961_deepfake_detection|Detection]] and Response)·접근통제·[[568_logs_distributed_logging_elk_fluentd|로그]] 분석을 생략하는 경우

기술사 답안에서는 **"망분리는 외부 공격 경로를 줄이는 구조적 통제이며, 실제 품질은 물리/[[369_logic_bomb|논리]] 분리 선택보다 망연계, 관리자 경로, 예외 통제, 내부 [[395_verification_process_review|검증]]까지 함께 설계했는지에 달려 있다"**고 정리하면 좋다.

- **📢 섹션 요약 비유**: 망분리를 잘하는 조직은 정문만 잠그는 것이 아니라 택배문, 비상구, 관리자 열쇠까지 모두 다른 규칙으로 관리하는 건물 관리자와 같다.

---

## Ⅴ. 기대효과 및 결론

망분리의 가장 큰 효과는 외부 침입 후 내부 확산 가능성을 구조적으로 낮춘다는 점이다. 인터넷 단말이 감염되더라도 업무망으로 곧바로 점프하기 어렵고, 고가치 자산을 별도 구역에 두어 사고 범위를 줄일 수 있다. 규제 대응과 [[606_auditing_linux_auditd|감사]] 관점에서도 설명 가능한 통제 모델을 제공한다는 장점이 있다.

그러나 망분리만으로 모든 문제가 해결되지는 않는다. 승인된 연계 경로를 통한 악성 [[501_file_definition_logical_record|파일]] 유입, 내부자 오남용, [[764_supply_chain_attack|공급망 공격]], 관리자 계정 탈취는 별도의 통제가 필요하다. 그래서 오늘날 망분리는 [[386_dlp|DLP]], [[325_edr|EDR]], [[613_ueba|UEBA]] (User and Entity Behavior Analytics), [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access) 같은 추가 계층과 함께 설계될 때 비로소 완성도가 높아진다.

결론적으로 망분리는 구식 경계 보안이 아니라, 여전히 강력한 **공격 경로 축소 모델**이다. 다만 "망을 나눴다"는 선언보다 더 중요한 것은, 나뉜 뒤에도 무엇이 오가고 누가 관리하며 예외가 어떻게 통제되는지를 끝까지 설계하는 일이다.

- **📢 섹션 요약 비유**: 망분리는 성벽을 세우는 일이고, 현대 보안은 거기에 감시탑, 출입기록, 순찰까지 더하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[079_developer_cleanroom_vdi_security|VDI]] (Virtual Desktop Infrastructure) | [[369_logic_bomb|논리]]적 망분리에서 [[001_dikw_pyramid|데이터]]는 서버에 두고 화면만 전달하는 대표 구현이다. |
| SBC (Server-Based Computing) | 공유 [[160_session_controlling_terminal|세션]] 기반으로 비용 효율적인 [[369_logic_bomb|논리]]적 망분리 모델을 제공한다. |
| [[183_network_linkage_system|망연계 시스템]] | 망분리 환경에서 [[501_file_definition_logical_record|파일]]과 [[001_dikw_pyramid|데이터]] 교환을 허용하는 공식 통로다. |
| [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]) | 승인된 경로를 통해서도 정보 유출을 통제하는 보완 수단이다. |
| [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access) | 망분리 이후 내부 접근도 매번 [[395_verification_process_review|검증]]하는 현대적 확장 개념이다. |
| [[325_edr|EDR]] (Endpoint [[961_deepfake_detection|Detection]] and Response) | 인터넷망과 업무망 단말 모두에서 침해 징후를 탐지하는 운영 통제다. |

### 📈 관련 키워드 및 발전 흐름도

```text
인터넷 기반 업무 확산
    │
    ▼
외부 침입 + 내부 측면 이동 위험 증가
    │
    ▼
물리적 / 논리적 망분리 도입
    │
    ├─ internet zone
    ├─ business zone
    ├─ secure transfer zone
    └─ admin zone
    │
    ▼
망연계 통제 + DLP + EDR
    │
    ▼
Zero Trust와 결합한 현대적 내부 보안
```

이 흐름은 망분리가 단독 기술이 아니라, 외부 경로 차단에서 시작해 내부 [[395_verification_process_review|검증]] 강화로 이어지는 보안 운영 모델임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 망분리는 놀이터와 선생님 방 사이에 잠긴 문을 하나 더 두는 거예요.
2. 놀이터에서 문제가 생겨도 그 문 때문에 중요한 방까지 바로 들어가기 어려워져요.
3. 그리고 문만 두는 게 아니라, 택배를 넣는 작은 창문도 검사해야 정말 안전해져요.
