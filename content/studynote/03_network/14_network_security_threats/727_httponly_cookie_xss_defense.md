+++
title = "727. XSS 방어 HttpOnly 쿠키 속성 설정 원리 스크립트 접근 차단"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…를 이해하면 탐지 가능성과 복구성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 앞선 726번 문서에서, 해커가 성공적으로 웹사이트에 악성 자바스크립트 코드(`<script> ... </script>`)를 심어두면, 접속한 사용자의 브라우저에서 이 코드가 실행됩니다.
- 이때 해커의 코드는 자바스크립트의 기본 기능인 <strong><code>document.cookie</code></strong>라는 내장 명령어를 딱 한 줄만 실행합니다. 이 명령어가 실행되면 현재 브라우저에 저장된 내 네이버 아이디 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/), 은행 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)가 텍스트 형태로 툭 튀어나옵니다. 해커는 이걸 자기 서버로 쓱 날려버리면 끝입니다([세션 하이재킹](/knowledge-base/studynote/03_network/14_network_security_threats/707_session_hijacking_tcp_seq_cookie/)).

```text
[무차별 대입 공격 통신 로그인/SSH 타격]
    │
    ▼
[XSS 방어 HttpOnly 쿠키 속성 설정…]
    │
    └──▶ [크로스 사이트 스크립팅 (XSS]
```

- **📢 섹션 요약 비유**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

가장 근본적으로는 개발자가 꼼꼼해야 합니다.
- <strong>입력값 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>)</strong>: 사용자가 게시판에 글을 쓸 때 꺾쇠 괄호 `<`나 `>` 같은 특수문자를 아예 못 쓰게 막아버립니다.
- **HTML 인코딩 (치환)**: 사용자가 억지로 `<script>`라고 치면, 서버는 이를 `&lt;script&gt;` 같은 무의미한 텍스트 기호로 싹 다 강제 변환해서 DB에 저장합니다. 나중에 다른 사람이 그 글을 봐도 브라우저는 이를 실행 코드가 아닌 단순한 "글자"로 인식해 악성 행위가 차단됩니다. (보안 코딩의 기초)

```text
[무차별 대입 공격 통신 로그인/SSH 타격]
    │
    ▼
[XSS 방어 HttpOnly 쿠키 속성 설정…]
    │
    └──▶ [크로스 사이트 스크립팅 (XSS]
```

- **📢 섹션 요약 비유**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

만약 개발자가 실수로 필터링을 빼먹어서 악성 자바스크립트가 내 화면에서 실행되어 버렸다면? 그래도 내 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 지켜주는 최후의 안전장치가 바로 `HttpOnly`입니다.

### 1. `HttpOnly`의 동작 원리
- 웹 서버(네이버 등)가 로그인에 성공한 사용자에게 임시 통행증인 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 구워줄 때, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 응답 헤더 끝에 <strong><code>HttpOnly</code></strong>라는 꼬리표 옵션을 딱 달아서 보내줍니다.
  - `Set-Cookie: session_id=1234567; HttpOnly;`
- 이 꼬리표가 붙은 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 받은 브라우저(크롬, 사파리)는 맹세합니다. <strong>"앞으로 이 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">쿠키</a>는, 오직 정상적인 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 통신(서버에 화면 달라고 요청할 때)을 할 때만 브라우저가 알아서 꺼내서 쓴다. 그 외에 웹페이지 안에서 돌아가는 자바스크립트 따위가 <code>document.cookie</code> 명령어로 감히 이 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">쿠키</a>를 보여달라고 요구하면 무조건 거절(Access Denied)하겠다!"</strong>

### 2. 해커의 절망
- 해커의 [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 코드가 무사히 실행되어 `document.cookie`를 외쳐도, 브라우저는 텅 빈 문자열만 뱉어줍니다. 핵심 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)는 `HttpOnly` 방탄유리 안에 들어있어 자바스크립트의 손길이 절대 닿지 않기 때문입니다.
- 결과적으로 <strong><a href="/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/">XSS</a> 취약점이 뚫리더라도, 가장 치명적인 타격인 '<a href="/knowledge-base/studynote/03_network/14_network_security_threats/707_session_hijacking_tcp_seq_cookie/">세션 하이재킹</a>(계정 탈취)'만큼은 완벽하게 방어해 내는 최고의 가성비 보호막</strong>이 됩니다.

[XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 무차별 대입 공격 통신 로그인/[SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 타격이 기반 조건을 만든다면, [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 그 위에서 핵심 메커니즘을 구현하고, [크로스 사이트 스크립팅](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/500_xss_defense_escaping_csp/) (XSS는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 탐지 가능성과 복구성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 무차별 대입 공격 통신 로그인/[SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 타격의 기반 정리 | [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…의 핵심 동작 | [크로스 사이트 스크립팅](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/500_xss_defense_escaping_csp/) (XSS의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 탐지 가능성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 탈취당하는 또 다른 구멍은, 와이파이를 몰래 [도청](/knowledge-base/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)(스니핑)하는 것입니다.
- 이를 막기 위해 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 구워줄 때 <strong><code>Secure</code></strong>라는 옵션도 같이 달아줍니다. 이 꼬리표가 붙으면, 브라우저는 평문 통신인 `http://`에서는 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)를 절대 내보내지 않고, 완벽히 암호화된 <strong><code>https://</code> 통신을 할 때만 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">쿠키</a>를 안전하게 실어 보냅니다.</strong>

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)는 놀이공원 'VIP 목걸이 통행증'입니다. 해커가 보낸 자바스크립트 코드(`document.cookie`)는 깡패들이 내 주머니를 뒤져 통행증을 뺏어가는 짓([XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/))입니다. `HttpOnly` [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은, 아예 통행증을 주머니에 넣지 못하게 내 '피부 속에 인식 칩으로 삽입'해 버리는 마법입니다. 놀이기구 입구([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 통신)를 지나갈 땐 게이트가 알아서 내 피부 속 칩을 인식해 문을 열어주지만, 깡패(자바스크립트)들이 내 주머니를 아무리 뒤져봐야 만질 수 있는 통행증 실물이 아예 없으니 헛수고만 하고 털어가지 못하는 완벽한 보안책입니다.

---

## Ⅴ. 기대효과 및 결론

[XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 탐지 가능성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [크로스 사이트 스크립팅](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/500_xss_defense_escaping_csp/) ([XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/), 예측형 위협 대응, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 예측형 위협 대응 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 무차별 대입 공격 통신 로그인/[SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 타격 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 공격 표면 (Attack Surface) | 위협이 침투할 수 있는 노출 지점을 뜻한다. |
| [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) | 정상 패턴과 다른 징후를 찾아낸다. |
| [크로스 사이트 스크립팅](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/500_xss_defense_escaping_csp/) ([XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 무차별 대입 공격 통신 로그인/SSH 타격]
    │
    ▼
[현재 개념: XSS 방어 HttpOnly 쿠키 속성 설정…]
    │
    ├──▶ [확장 A: 크로스 사이트 스크립팅 (XSS]
    └──▶ [확장 B: 예측형 위협 대응]
```

[XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 HttpOnly [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)…는 무차별 대입 공격 통신 로그인/[SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 타격에서 출발해 현재 메커니즘을 정교화하고, 이후 [크로스 사이트 스크립팅](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/500_xss_defense_escaping_csp/) (XSS와 예측형 위협 대응 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 나쁜 친구가 놀이터 규칙을 깨뜨리면 바로 알아차리고 막아야 해요.
2. 이 개념은 어떤 장난이 위험한지 미리 알고, 문제가 생기면 어떻게 다시 정리할지도 알려줘요.
3. 그래서 놀이터를 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 848 / 1120

← **이전**: [726. XSS (Cross Site Scripting) 개요와 3대 기법 (Stored / Reflected / DOM)](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/)
**다음**: [728. CSRF (Cross-Site Request Forgery) 인증 세션 권한 도용](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) →

---
