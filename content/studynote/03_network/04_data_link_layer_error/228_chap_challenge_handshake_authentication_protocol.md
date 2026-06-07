---
title: "228. CHAP (Challenge Handshake Authentication Protocol)"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 228
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CHAP는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: CHAP를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: CHAP (Challenge Handshake [Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), RFC 1994)는 PAP의 치명적인 평문 전송 취약점을 극복하기 위해 설계된 보안 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 프로토콜이다. 클라이언트와 서버가 사전에 공유된 비밀번호(Shared [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))를 가지고 있다는 전제하에, 비밀번호 자체를 넘기지 않고 "나는 비밀번호를 알고 있다"는 사실만 해시 연산을 통해 증명(Zero-Knowledge Proof의 일종)한다.

- **필요성**: 해커가 패킷을 가로채서(Sniffing) 비밀번호를 알아내거나, 탈취한 패킷을 다시 보내어([Replay Attack](/studynote/09_security/03_network_security/274_replay_attack/)) 정상 사용자로 위장하는 공격이 빈번해지자, 비밀번호 자체가 네트워크 선로를 타지 않게 만드는 근본적인 해결책이 필요해졌다.

- **💡 비유**: [스파이](/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/) 영화의 "암구호"와 같습니다. 문지기(서버)가 매일 바뀌는 질문(Challenge, 예: "오늘 점심은?")을 던지면, [스파이](/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/)(클라이언트)는 머릿속에 있는 비밀번호(예: "사과")를 조합하여 정해진 규칙(해시)에 따라 암호화된 대답("사과가 들어간 샐러드")을 합니다. 해커가 대답을 엿듣고 다음 날 "사과가 들어간 샐러드"라고 말해도, 그날의 질문(Challenge)이 달라서 틀린 대답이 되므로 쫓겨나게 됩니다.

```text
[PAP]
    |
    v
[CHAP]
    |
    +---> [EAP]
```

- **📢 섹션 요약 비유**: <strong> CHAP <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>은 비밀번호를 그대로 말하지 않고, 매번 바뀌는 </strong>"1회용 난수 퍼즐 조각"**에 비밀번호를 끼워 맞춘 결과물(해시)만 검사관에게 보여주어 정답을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)받는 고도의 보안 검문소입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 3-Way 핸드셰이크 메커니즘
CHAP는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 과정을 서버(Authenticator)가 주도(Server-driven)한다.

1. **Challenge (질의)**: 서버가 클라이언트에게 임의의 무작위 값([Nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/), Challenge)과 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ID를 전송한다.
2. **Response (응답)**: 클라이언트는 받은 난수, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ID, 그리고 자신이 알고 있는 '비밀번호'를 [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/)(Message-Digest [algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 5) 같은 해시 함수에 넣고 돌려 <strong>해시값(Response)</strong>을 생성해 서버로 보낸다. *(이때 비밀번호는 전송되지 않음)*
3. **Success / Failure (결과)**: 서버도 자신이 보낸 난수와 DB에 저장된 클라이언트의 비밀번호를 똑같이 해시 함수에 넣어 결과값을 계산한다. 서버가 계산한 값과 클라이언트가 보낸 응답값(Response)이 정확히 일치하면 승인(Success)한다.

```text
 +-------------------------------------------------------------+
 |                    CHAP 동작 방식 (3-Way)                   |
 +-------------------------------------------------------------+
 |                                                             |
 |   [클라이언트 (Peer)]                       [서버 (Authenticator)]|
 |     (PW = "sec123")                          (DB: PW = "sec123")|
 |           |                                         |       |
 |           |      1. Challenge (난수값 X 전송)         |       |
 |           |<-----------------------------------------+       |
 |           |                                         |       |
 | MD5(X + "sec123")                                   |       |
 | = 해시값 Y 도출     2. Response (해시값 Y 전송)         |       |
 |           +----------------------------------------->| 서버도 자체적으로  |
 |           |                                         | MD5(X + "sec123") |
 |           |                                         | = 해시값 Y' 계산  |
 |           |                                         |                   |
 |           |      3. Success/Failure (Y == Y' 비교)  |                   |
 |           |<-----------------------------------------+       |
 |                                                             |
 +-------------------------------------------------------------+
```

### 2. 해시 함수의 일방향성(One-way)과 [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어
- **스니핑 방어**: 네트워크로 전송되는 값은 난수 X와 해시값 Y뿐이다. 해시 함수는 일방향 함수이므로 해커가 Y를 가로채도 원래의 비밀번호("sec123")를 역산하여 알아낼 수 없다.
- <strong><a href="/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/">재생 공격</a>(<a href="/studynote/09_security/03_network_security/274_replay_attack/">Replay Attack</a>) 방어</strong>: 서버는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 시도마다 매번 다른 난수 X(Challenge)를 생성한다. 해커가 어제 캡처한 해시 응답값 Y를 오늘 다시 서버에 전송해 봐야, 오늘 서버가 요구한 난수 Z에 대한 정답(해시값 W)과는 일치하지 않으므로 즉시 차단된다.
- **주기적 재인증**: 통신 중에도 서버가 랜덤한 주기로 다시 Challenge를 보내 재인증을 요구하여 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 하이재킹을 방어한다.

- **📢 섹션 요약 비유**: ** CHAP는 **"수학적 믹서기(해시)"**입니다. 과일(난수)과 설탕(비밀번호)을 넣고 갈아버린 주스(응답)만 전송하므로, 해커가 주스를 훔쳐 가도 원래 설탕의 결정 모양(비밀번호 문자열)을 절대 복원할 수 없습니다.

---

## Ⅲ. 비교 및 연결

CHAP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. PAP가 기반 조건을 만든다면, CHAP는 그 위에서 핵심 메커니즘을 구현하고, EAP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 오류율과 재전송 비용에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | PAP의 기반 정리 | CHAP의 핵심 동작 | EAP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 오류율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: CHAP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CHAP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [PAP](/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) 수준의 기본 대책으로 충분한지, 아니면 CHAP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 EAP와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 오류율 부족인지, 재전송 비용 악화인지 먼저 분리한다.
2. CHAP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 EAP와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CHAP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- PAP와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: CHAP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

CHAP는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 오류율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [EAP](/studynote/03_network/04_data_link_layer_error/229_eap_extensible_authentication_protocol/), 고신뢰 저지연 링크 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: CHAP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [PAP](/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) | 비트열을 의미 있는 전송 단위로 구분한다. |
| [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) ([Error Control](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)) | 검출과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계해야 한다. |
| [EAP](/studynote/03_network/04_data_link_layer_error/229_eap_extensible_authentication_protocol/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: PAP]
    |
    v
[현재 개념: CHAP]
    |
    +---> [확장 A: EAP]
    +---> [확장 B: 고신뢰 저지연 링크 제어]
```

CHAP는 PAP에서 출발해 현재 메커니즘을 정교화하고, 이후 EAP와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 349 / 1120

<- **이전**: [227. PAP (Password Authentication Protocol)](/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/)
**다음**: [229. EAP (Extensible Authentication Protocol)](/studynote/03_network/04_data_link_layer_error/229_eap_extensible_authentication_protocol/) ->

---
