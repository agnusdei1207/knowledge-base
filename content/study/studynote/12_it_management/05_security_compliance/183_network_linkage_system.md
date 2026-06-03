+++
weight = 183
title = "183. 망연계 시스템 (Network Linkage System)"
date = "2026-05-06"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 망연계 시스템 (Network Linkage System)은 물리적·논리적으로 분리된 망 사이에 공식 전송 경로를 두고, 수집·검사·승인·기록을 거친 [[001_dikw_pyramid|데이터]]만 건네는 보안 중개 아키텍처다.
> 2. **가치**: [[182_network_separation_model|망분리]]의 경계를 무너뜨리지 않으면서 [[501_file_definition_logical_record|파일]], 배치 [[001_dikw_pyramid|데이터]], [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]), 메시지 흐름을 업무에 필요한 수준으로 허용해 보안과 운영 연속성을 동시에 확보한다.
> 3. **판단 포인트**: 핵심 판단은 전송 방향([[008_단방향_반이중_전이중|단방향]]/양방향), [[001_dikw_pyramid|데이터]] 성격([[501_file_definition_logical_record|파일]]/[[002_database_definition|데이터베이스]]([[501_database|Database]])/[[014_api_posix|API]]), 요구 지연시간, 검열 강도(CDR (Content Disarm and Reconstruction) / [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]) / [[005_schema|스키마]] [[395_verification_process_review|검증]]), [[606_auditing_linux_auditd|감사]] 추적성을 어떻게 조합할지이며, 이를 잘못 잡으면 우회 사용이나 병목이 생긴다.

---

## Ⅰ. 개요 및 필요성

[[182_network_separation_model|망분리]] ([[182_network_separation_model|Network Separation]])는 인터넷 구간과 핵심 업무 구간을 끊어 외부 침입의 확산 경로를 줄이는 강력한 통제다. 그러나 현실의 업무는 완전한 고립 상태로 돌아가지 않는다. 인터넷에서 받은 자료를 내부로 들여와야 하고, 내부 시스템의 결과를 외부 기관·고객·[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] (Disaster [[658_ir_recovery|Recovery]]) 센터로 내보내야 하며, 분리된 두 시스템이 제한적으로 [[001_dikw_pyramid|데이터]]를 교환해야 하는 순간이 계속 생긴다.

이때 공식 경로가 없으면 사용자는 개인 메일, 임의 [[359_usb|USB]], 메신저, 화면 캡처 같은 비인가 우회로를 찾게 된다. 즉 [[182_network_separation_model|망분리]]만 있고 망연계가 없으면 경계는 강해 보이지만 실제 운영은 더 취약해질 수 있다. 망연계 시스템은 바로 이 모순을 해결하기 위해 등장한 "보안된 예외 경로"다.

중요한 점은 망연계가 [[182_network_separation_model|망분리]]를 무력화하는 통로가 아니라는 것이다. 목적은 연결을 넓히는 것이 아니라, 필요한 교환을 **가장 좁고 가장 기록 가능하게** 만드는 데 있다. 따라서 망연계의 품질은 단순 연결 성공 여부가 아니라, 무엇이 어떤 조건으로 왜 통과했는지를 설명할 수 있는지에 달려 있다.

- **📢 섹션 요약 비유**: 망연계 시스템은 잠긴 건물 사이를 잇는 비밀 통로가 아니라, 검색대와 출입기록을 거쳐야만 지날 수 있는 보안 게이트와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전형적인 망연계 시스템은 원천 구간, 수집/임시 저장 구간, 검사 구간, [[164_policy|정책]]/승인 구간, 전송 중개 구간, 목적지 구간으로 나뉜다. [[001_dikw_pyramid|데이터]]는 원본 그대로 곧바로 넘어가지 않고, [[012_metadata|메타데이터]] 추출, 악성코드 검사, CDR (Content Disarm and Reconstruction), [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]), 포맷/[[005_schema|스키마]] [[395_verification_process_review|검증]], 결재 또는 [[164_policy|정책]] 확인을 거친 뒤 전달된다. 실패한 항목은 폐기 또는 격리되고, 모든 단계는 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]로 남는다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Source Collector | 원천 망의 [[501_file_definition_logical_record|파일]]·레코드·이벤트 수집 | 어떤 [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 받을지 allowlist 필요 |
| Staging Zone | 임시 저장 및 [[012_metadata|메타데이터]] 추출 | 원본과 정제본 분리 보관 |
| Inspection Engine | [[323_antivirus|Antivirus]] ([[323_antivirus|AV]]), CDR, [[386_dlp|DLP]], [[005_schema|스키마]] [[395_verification_process_review|검증]] 수행 | 정적 검사와 동적 검사의 조합 중요 |
| [[164_policy|Policy]] / Approval Engine | 규칙 판단 또는 결재 워크플로우 | 역할 분리와 승인 책임 추적 필요 |
| Transfer Broker | [[008_단방향_반이중_전이중|단방향]] 또는 통제된 중개 전송 | 재전송, 순서 보장, 큐 적체 관리 |
| [[363_audit|Audit]] / [[624_siem|SIEM]] ([[283_security_tactics|Security]] Information and [[074_event_management|Event Management]]) | [[568_logs_distributed_logging_elk_fluentd|로그]] 보관과 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] | 최소 1년 이상 보관, 경보 연계 |

아래 그림은 [[501_file_definition_logical_record|파일]], 배치, 인터페이스 [[001_dikw_pyramid|데이터]]가 망연계를 통과할 때의 공통 흐름을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Network linkage reference flow                                      │
├──────────────────────────────────────────────────────────────────────┤
│ Source zone                                                         │
│   files / records / API events                                      │
│        │                                                            │
│        ▼                                                            │
│ [Collector / Staging]                                               │
│        │ metadata extraction                                        │
│        ▼                                                            │
│ [Inspection] Antivirus + CDR + DLP + schema validation              │
│        │                                                            │
│        ├─ reject / quarantine -> audit                              │
│        └─ pass                                                      │
│             ▼                                                       │
│      [Approval / Policy Engine]                                     │
│             │                                                       │
│             ▼                                                       │
│      [Transfer Broker / Relay]                                      │
│             │                                                       │
│        one-way or controlled bi-direction                           │
│             ▼                                                       │
│ Target zone + SIEM / immutable logs                                 │
└──────────────────────────────────────────────────────────────────────┘
```

여기서 핵심은 "연결"보다 "중개"다. 보안 수준이 가장 높은 환경에서는 [[001_dikw_pyramid|Data]] Diode로 물리적 [[008_단방향_반이중_전이중|단방향]] 전송만 허용하고, 일반 업무망에서는 [[501_file_definition_logical_record|파일]] 전송 게이트웨이나 [[014_api_posix|API]] 릴레이가 [[164_policy|정책]] 기반 양방향 흐름을 제한적으로 제공한다. 즉 망연계는 단일 제품명이 아니라, **분리된 경계 위에 어떤 형태의 안전한 흐름을 설계할지에 대한 아키텍처 패턴**이다.

- **📢 섹션 요약 비유**: 망연계는 문을 활짝 여는 것이 아니라, 짐을 검수하고 봉인해 전달하는 택배 교환소를 두는 것과 같다.

---

## Ⅲ. 비교 및 연결

망연계 방식은 모두 "분리된 망 사이를 안전하게 잇는다"는 공통 목적을 가지지만, 전송 방향과 허용 수준이 다르다. 그래서 같은 망연계라도 [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]], [[501_file_definition_logical_record|파일]] 전송 게이트웨이, [[014_api_posix|API]]/메시지 릴레이는 서로 다른 문제를 푼다.

| 방식 | 전송 방향 | 강점 | 한계 | 적합한 환경 |
| :--- | :--- | :--- | :--- | :--- |
| [[001_dikw_pyramid|Data]] [[011_diode|Diode]] | 물리적 [[008_단방향_반이중_전이중|단방향]] | 최고 수준 보안, 역방향 침투 차단 | 상호 질의·응답 불가, 유연성 낮음 | [[891_ot_operational_technology|OT]] ([[891_ot_operational_technology|Operational Technology]]), [[893_ics_industrial_control_system|ICS]] ([[893_ics_industrial_control_system|Industrial Control System]]), 국방 |
| [[501_file_definition_logical_record|파일]] 전송 게이트웨이 | [[164_policy|정책]] 기반 양방향 | CDR, 백신, 승인 절차에 유리 | 대용량/실시간성에서 병목 가능 | 공공·금융·일반 사무망 |
| [[014_api_posix|API]] / 메시지 릴레이 | 제한적 양방향 또는 비동기 | 시스템 간 연계 자동화, [[005_schema|스키마]] 통제 | 인터페이스 설계와 인증체계가 복잡 | 업무 시스템 연동, 클라우드 연계 |
| 보안 [[359_usb|USB]] | 수동 이동 | 단순하고 저렴 | 사용자 실수, 추적성 약화 | 비정기적 예외 반출입 |

이 비교에서 중요한 것은 [[690_firewall_generation_evolution|방화벽]]과의 차이다. [[690_firewall_generation_evolution|방화벽]]은 연결 자체를 허용하거나 차단하는 네트워크 제어 장비이고, 망연계 시스템은 콘텐츠와 행위를 해석해 "무엇을 어떤 조건으로 넘길지"를 통제하는 업무형 보안 장치다. 따라서 단순 [[446_port_and_bus|포트]] 오픈은 망연계 대체가 될 수 없다.

또한 망연계는 182번의 [[182_network_separation_model|망분리]] 모델, 184번의 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])와도 연결된다. [[182_network_separation_model|망분리]]가 큰 경계를 만드는 구조라면, 망연계는 그 경계를 통과하는 공식 밸브이고, [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 그 밸브를 통과한 뒤에도 세션과 요청을 계속 [[395_verification_process_review|검증]]하는 원리다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|Data]] Diode가 일방통행 터널이라면, [[501_file_definition_logical_record|파일]] 전송 게이트웨이는 세관 검사를 거치는 국제 화물 터미널이고, [[014_api_posix|API]] 릴레이는 정해진 서류가 있는 차량만 드나드는 물류 전용 차선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 "무엇이 오가는가"보다 "왜 그 흐름이 필요한가"를 정의해야 한다. 전송 목적이 단순 [[501_file_definition_logical_record|파일]] 반입인지, 실시간 인터페이스인지, [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] [[016_replication_factor|복제]]인지에 따라 망연계 방식과 통제 강도가 달라진다. 예를 들어 제어망에서 운영 [[001_dikw_pyramid|데이터]]만 외부로 내보내는 경우는 [[008_단방향_반이중_전이중|단방향]] [[011_diode|다이오드]]가 적합하지만, 민원 시스템과 내부 결재 시스템이 상태를 주고받아야 한다면 승인 가능한 [[014_api_posix|API]] 릴레이가 필요하다.

| 실무 시나리오 | 권장 방식 | 설계 포인트 |
| :--- | :--- | :--- |
| 인터넷 자료를 업무망으로 반입 | [[501_file_definition_logical_record|파일]] 전송 게이트웨이 + CDR + 승인 | [[501_file_definition_logical_record|파일]] 형식 allowlist, 격리 저장소, 사용자 통지 |
| [[891_ot_operational_technology|OT]]/[[893_ics_industrial_control_system|ICS]] [[001_dikw_pyramid|데이터]] 외부 모니터링 | [[001_dikw_pyramid|Data]] [[011_diode|Diode]] | 역방향 명령 차단, [[008_단방향_반이중_전이중|단방향]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환 |
| 분리된 시스템 간 실시간 인터페이스 | [[014_api_posix|API]] 또는 메시지 릴레이 | [[005_schema|스키마]] [[395_verification_process_review|검증]], [[820_tokenization|토큰화]], 재전송·[[171_idempotency_iac_terraform|멱등성]] 설계 |
| [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 센터로 배치 [[016_replication_factor|복제]] | 전용 연계 채널 + [[112_checksum|체크섬]] [[395_verification_process_review|검증]] | 적체 모니터링, [[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]]) 관리 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[808_data_classification|데이터 분류]]와 전송 방향이 문서화되어 있는가?
2. [[501_file_definition_logical_record|파일]] 기반이면 확장자가 아니라 실제 포맷과 콘텐츠를 검사하는가?
3. 인터페이스 기반이면 [[005_schema|스키마]], 필드 단위 마스킹, 호출 주체 인증이 강제되는가?
4. 큐 적체, 재전송, 중복 전송을 감시할 지표가 있는가?
5. 승인·반출입·예외 처리 [[568_logs_distributed_logging_elk_fluentd|로그]]가 [[624_siem|SIEM]] ([[283_security_tactics|Security]] Information and [[074_event_management|Event Management]])에 연동되는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- SMB (Server Message Block) 공유 폴더나 [[690_firewall_generation_evolution|방화벽]] 예외 개방을 망연계라고 부르는 경우
- [[501_file_definition_logical_record|파일]] 확장자만 보고 허용해 실제 포맷 위장과 스테가노그래피를 놓치는 경우
- 실시간 요구사항을 고려하지 않고 수동 승인 절차만 넣어 업무를 마비시키는 경우
- [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] [[016_replication_factor|복제]] 연계에서 적체와 손상 [[395_verification_process_review|검증]] 없이 "전송만 되면 끝"으로 보는 경우

기술사 답안에서는 [[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]])와 RPO까지 함께 언급하면 좋다. 예를 들어 망연계가 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] [[016_replication_factor|복제]]의 유일한 경로라면 큐 지연과 재전송 실패가 곧 [[177_rpo_recovery_point_objective|RPO]] 악화로 이어지고, 장애 시 우회 절차가 없다면 RTO도 늘어난다. 즉 망연계는 보안 장비이면서 동시에 업무 연속성 장치다.

- **📢 섹션 요약 비유**: 망연계를 잘 설계하는 일은 수도관에 밸브를 다는 것과 같아서, 아무 때나 막거나 여는 것이 아니라 수질 검사·유량·비상 차단까지 함께 계산해야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 망연계 시스템은 [[182_network_separation_model|망분리]]의 보안 강도를 유지하면서도 현실 업무가 요구하는 [[001_dikw_pyramid|데이터]] 흐름을 설명 가능하게 만든다. 사용자는 비인가 우회 경로를 찾지 않아도 되고, 보안팀은 어떤 [[001_dikw_pyramid|데이터]]가 어떤 검사와 승인을 거쳐 이동했는지 추적할 수 있다. 이는 단순 편의 개선이 아니라, [[606_auditing_linux_auditd|감사]]와 사고 대응의 근거를 확보한다는 뜻이다.

다만 망연계가 만능은 아니다. 검사 엔진 성능이 부족하면 병목이 되고, [[164_policy|정책]]이 느슨하면 악성 콘텐츠가 통과하며, [[164_policy|정책]]이 과도하면 조직이 다시 우회 경로를 찾는다. 따라서 망연계의 성패는 장비 이름보다 **[[808_data_classification|데이터 분류]], 승인 책임, [[119_log_analysis|로그 분석]], 예외 통제, [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 연동**을 얼마나 함께 설계했는지에 달려 있다.

결론적으로 망연계 시스템은 "분리된 망을 연결하는 터널"이 아니라 "분리 원칙을 유지하면서 필요한 흐름만 조절하는 밸브"로 기억하는 것이 정확하다. 좋은 망연계는 연결을 늘리는 기술이 아니라, 연결을 설명 가능하게 만드는 기술이다.

- **📢 섹션 요약 비유**: 망연계는 성벽에 큰 문을 내는 일이 아니라, 검색대와 기록 장부가 붙은 작은 성문을 운영하는 일과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[182_network_separation_model|망분리]] ([[182_network_separation_model|Network Separation]]) | 망연계 시스템이 보호해야 하는 기본 경계 구조다. |
| CDR (Content Disarm and Reconstruction) | [[501_file_definition_logical_record|파일]] 반입 시 실행 가능한 위험 요소를 제거하는 핵심 기술이다. |
| [[001_dikw_pyramid|Data]] [[011_diode|Diode]] | 최고 수준 [[008_단방향_반이중_전이중|단방향]] 망연계 구현 방식이다. |
| [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]) | 반출 [[001_dikw_pyramid|데이터]]의 [[782_sensitive_information|민감정보]] 유출을 통제하는 보완 계층이다. |
| [[542_api_gateway|API Gateway]] / Message [[058_queue|Queue]] | 시스템 간 자동 연계를 망연계 [[164_policy|정책]] 안에서 구현하는 수단이다. |
| [[624_siem|SIEM]] ([[283_security_tactics|Security]] Information and [[074_event_management|Event Management]]) | 모든 연계 이력과 이상 징후를 통합 분석하는 운영 기반이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
망분리 도입
    │
    ▼
업무상 데이터 교환 필요 발생
    │
    ▼
Staging + Inspection + Approval
    │
    ├─ 단방향 고보안 -> Data Diode
    ├─ 파일 교환     -> Transfer Gateway + CDR
    └─ 시스템 연계   -> API / Message Relay
    │
    ▼
Audit + SIEM + DR 연계
    │
    ▼
Zero Trust와 결합한 현대적 경계 운영
```

이 흐름은 망연계가 단순 [[501_file_definition_logical_record|파일]] 복사가 아니라, 분리된 환경에서 [[001_dikw_pyramid|데이터]]를 안전하게 이동시키기 위한 통제 체계로 진화했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 망연계 시스템은 두 교실 사이에 놓인 작은 전달 창구 같아요.
2. 종이나 물건을 그냥 던져 주는 게 아니라, 선생님이 먼저 열어 보고 안전한 것만 넘겨줘요.
3. 그래서 교실 문은 계속 잠겨 있어도 꼭 필요한 숙제는 안전하게 주고받을 수 있어요.
