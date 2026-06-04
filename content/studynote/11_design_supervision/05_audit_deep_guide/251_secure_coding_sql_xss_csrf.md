+++
title = "251. 시큐어 코딩 SQL/XSS/CSRF 진단 (Secure Coding SQL/XSS/CSRF Audit)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SW 개발보안([시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/), [Secure Coding](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/))은 취약점을 설계·개발 단계에서 원천 차단하는 예방 중심 접근이다.
> 2. **가치**: SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)([SQL Injection](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/)), [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/)([Cross-Site Scripting](/knowledge-base/studynote/09_security/05_web_app_security/470_xss/)), [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/)([Cross-Site Request Forgery](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/)) 세 공격 유형은 OWASP(Open Web Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/)) Top 10의 핵심으로, 감리 점검 빈도가 가장 높다.
> 3. **판단 포인트**: 입력값 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Input Validation](/knowledge-base/studynote/09_security/uncategorized/601_input_validation/))·출력값 인코딩(Output Encoding)·토큰 기반 요청 인증이 코드 레벨에서 구현되었는지를 소스코드 및 실행 결과 모두에서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅰ. 개요 및 필요성
SW 개발보안([시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/), [Secure Coding](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/))은 소프트웨어 개발 생명주기([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) 전 단계에 걸쳐 보안 취약점을 제거하는 실천 체계다. 행정안전부 「소프트웨어 개발보안 가이드」는 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/), [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/), CSRF를 포함한 43개 취약점 진단 항목을 규정하며, 공공정보화사업 감리 시 반드시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

| 공격 유형 | 영문 Full Name | 공격 원리 | 피해 범위 |
|:---|:---|:---|:---|
| SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) | [SQL Injection](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/) | 사용자 입력을 SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 직접 삽입 | DB 전체 탈취·삭제 |
| OS [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) | [OS Command Injection](/knowledge-base/studynote/09_security/05_web_app_security/435_os_command_injection/) | 입력값으로 시스템 명령 실행 | 서버 루트 권한 탈취 |
| [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) | [Cross-Site Scripting](/knowledge-base/studynote/09_security/05_web_app_security/470_xss/) | 악성 스크립트를 피해자 브라우저에서 실행 | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 탈취·[피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/752_phishing/) |
| [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) | [Cross-Site Request Forgery](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) | 인증된 사용자의 권한으로 위조 요청 실행 | 계정 변경·결제 위조 |

- 「전자정부법」 제45조의3: 정보보호 진단·점검 의무
- 행정안전부 「소프트웨어 개발보안 가이드([2021](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/))」: 43개 진단 항목
- KISA(한국인터넷진흥원, Korea Internet & [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Agency) 취약점 진단 기준

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)은 "식당 주문서에 '모든 메뉴를 공짜로 주세요'라고 적어 요리사를 혼란에 빠트리는 것"이다. 입력 칸을 신뢰하지 않는 것이 [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/)의 출발점이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+------------------------------------------------------------+
|                    요청 처리 파이프라인                      |
|                                                            |
|  [사용자 입력]                                              |
|       |                                                    |
|       v                                                    |
|  +------------------------------+                          |
|  |  1. 입력값 화이트리스트 검증   |  <- 허용 문자만 통과       |
|  |     (Whitelist Validation)   |                          |
|  +--------------+---------------+                          |
|                 |                                          |
|                 v                                          |
|  +------------------------------+                          |
|  |  2. PreparedStatement 사용   |  <- ? 플레이스홀더 바인딩  |
|  |     (Parameterized Query)    |                          |
|  +--------------+---------------+                          |
|                 |                                          |
|                 v                                          |
|  +------------------------------+                          |
|  |  3. 최소 권한 DB 계정 사용    |  <- SELECT 전용 계정       |
|  |     (Least Privilege)        |                          |
|  +--------------+---------------+                          |
|                 |                                          |
|                 v                                          |
|            [DB 실행 완료]                                   |
+------------------------------------------------------------+
```

XSS는 사용자가 입력한 `<script>` 태그가 다른 사용자의 브라우저에서 실행되는 공격이다. 방어의 핵심은 <strong>출력 시점의 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a>별 인코딩</strong>이다.

```
+------------------------------------------------------------+
|               XSS 방어 필터 흐름                            |
|                                                            |
|  입력: <script>alert('XSS')</script>                        |
|       |                                                    |
|       v                                                    |
|  +--------------------------+                              |
|  |   HTML 컨텍스트 인코딩    |                              |
|  |   < -> &lt;               |                              |
|  |   > -> &gt;               |                              |
|  |   " -> &quot;             |                              |
|  |   ' -> &#x27;             |                              |
|  +--------------+-----------+                              |
|                 |                                          |
|  출력: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt; |
|       -> 브라우저: 텍스트로 표시 (실행 불가)                  |
+------------------------------------------------------------+
```

[CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 토큰([CSRF Token](/knowledge-base/studynote/09_security/05_web_app_security/478_csrf_token/))은 서버가 생성한 난수값을 폼(Form) 히든 필드에 삽입하여 위조 요청을 차단한다.

```
+------------------------------------------------------------+
|              CSRF 토큰 검증 흐름                             |
|                                                            |
|  [서버] 세션 생성 시 토큰 발급                               |
|       |  Token = "a3f9b2c1d8e7..."                         |
|       v                                                    |
|  [클라이언트] 폼에 히든 필드로 포함                          |
|       |  <input type="hidden" name="_csrf" value="..."/>   |
|       v                                                    |
|  [요청 수신] 서버에서 토큰 일치 검증                         |
|       |                                                    |
|       +-- 토큰 일치 -> 요청 처리                              |
|       +-- 토큰 불일치 -> 403 Forbidden 반환                  |
+------------------------------------------------------------+
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어는 "스피커에 전달된 대사를 그대로 읽지 않고 따옴표로 묶어 안전하게 출력"하는 것이고, [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 방어는 "편지에 비밀 도장이 없으면 배달부가 접수를 거부"하는 것이다.

---

## Ⅲ. 비교 및 연결
| 구분 | SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) 방어 | [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어 | [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 방어 |
|:---|:---|:---|:---|
| **핵심 원리** | 입력과 코드 분리 | 출력 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 인코딩 | 요청 출처 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **구현 방법** | PreparedStatement, ORM(Object-Relational [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) | HTML 엔티티 인코딩, [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)([Content Security Policy](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)) 헤더 | [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 토큰, SameSite [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) |
| <strong>감리 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a> 위치</strong> | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Access Object) 레이어 코드 | 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) 템플릿 출력 함수 | 폼 히든 필드, 서버 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직 |
| **자동 탐지 도구** | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)(Static Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)(Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) + 수동 점검 |
| **위험 등급** | Critical | High | High |

| 기준 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) ([정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) ([동적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/332_dynamic_analysis/)) |
|:---|:---|:---|
| 분석 시점 | 코드 작성 후 빌드 단계 | 실행 중인 애플리케이션 |
| 도구 예시 | Fortify, [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/), Checkmarx | [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/), [Burp Suite](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/) |
| 장점 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 발견, 낮은 비용 | 실제 공격 시나리오 재현 |
| 단점 | 오탐(False Positive) 다수 | 실행 환경 필요 |

- **📢 섹션 요약 비유**: SAST는 "요리 전 재료 목록을 검사"하고, DAST는 "완성된 음식을 직접 먹어보며 독성을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"하는 것이다. 감리는 두 방법 모두를 요구한다.

---

## Ⅳ. 실무 적용 및 기술사 판단
| 점검 항목 | [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 방법 | 판정 기준 |
|:---|:---|:---|
| PreparedStatement 적용률 | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 레이어 코드 전수 검사 | SQL 동적 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 0건 |
| [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 인코딩 함수 사용 | 출력 뷰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 검색 | `fn:escapeXml()` 또는 동등 함수 100% 적용 |
| [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 토큰 구현 | 상태 변경 요청(POST/PUT/DELETE) 전수 | 히든 필드 + 서버 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 모두 존재 |
| [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)([Content Security Policy](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)) 헤더 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 응답 헤더 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | `default-src 'self'` 이상 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| 오류 메시지 노출 | 고의 오류 발생 후 응답 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | DB/[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 정보 미노출 |

- <strong>ORM(Object-Relational <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/">Mapping</a>) 사용 시 주의</strong>: JPA(Java Persistence [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))/MyBatis의 `${}` 대신 `#{}` 사용 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/). `${}`는 PreparedStatement를 우회하여 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)에 취약하다.
- <strong>DOM 기반 <a href="/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/">XSS</a></strong>: 서버 응답이 안전해도 JavaScript에서 `innerHTML`, `document.write()` 사용 시 클라이언트 측 [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 발생 가능 — DAST로만 탐지 가능.
- <strong><a href="/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/">CSRF</a> 예외 관리</strong>: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이에서 [JWT](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)([JSON Web Token](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)) 기반 인증을 사용하는 경우 [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 위험은 낮으나, [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 기반 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)과 혼용 시 반드시 토큰 적용.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: ORM에서 `${}` 사용은 "문잠금 장치를 설치했지만 비상구 문은 열어둔 것"이다. 감리는 그 비상구까지 반드시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅴ. 기대효과 및 결론
[시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) 진단이 체계적으로 수행되면 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)을 통한 DB 탈취, XSS를 통한 [세션 하이재킹](/knowledge-base/studynote/03_network/14_network_security_threats/707_session_hijacking_tcp_seq_cookie/)([Session Hijacking](/knowledge-base/studynote/09_security/03_network_security/271_session_hijacking/)), CSRF를 통한 권한 남용이 코드 레벨에서 원천 차단된다. 행정안전부 통계에 따르면 공공기관 침해사고의 약 40%가 웹 취약점에서 발생하며, 특히 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)과 XSS가 주를 이룬다. 감리 단계에서 조기 발견 시 수정 비용은 운영 단계 대비 1/[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이하로 절감된다.

감리인은 자동화 도구([SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)) 결과와 수동 코드리뷰를 병행하고, 특히 **입력 처리->DB 연동->출력 렌더링** 전 경로를 추적하는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 분석(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Flow Analysis)</strong>을 핵심 점검 방법으로 적용해야 한다.

확장 방향은 ① [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), ② Continuous [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/), ③ [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) 감리는 건물 완공 전 소방 배선을 점검하는 것과 같다. 벽을 뜯고 다시 배선하는 비용보다 사전 점검이 훨씬 저렴하고 안전하다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | SW 개발보안 ([Secure Coding](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/)) | 43개 취약점 진단 체계 전체 |
| 상위 개념 | [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) | 웹 보안 10대 위험 목록 |
| 하위 개념 | PreparedStatement | SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) 방어 핵심 구현체 |
| 하위 개념 | [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) ([Content Security Policy](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)) | [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 방어를 위한 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 응답 헤더 |
| 하위 개념 | SameSite [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) | [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 방어를 위한 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
| 연관 개념 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) / [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) | 정적·동적 보안 테스트 도구 |
| 연관 개념 | KISA 취약점 진단 | 공공기관 법적 점검 기준 |

### 📈 관련 키워드 및 발전 흐름도
[위협 모델링](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) -> [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) SQL/[XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/)/[CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) 진단 -> [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)·보안 테스트

### 👶 어린이를 위한 3줄 비유 설명
1. SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)은 마법 주문서에 "내 말을 무조건 따라!"라고 쓴 쪽지를 몰래 끼워 넣는 속임수야.
2. XSS는 친구에게 전달할 편지 속에 폭탄 스티커를 숨겨 상대방 책상에서 터지게 하는 것이고.
3. CSRF는 누군가가 엄마 이름으로 가짜 편지를 써서 용돈을 자기 통장에 넣도록 속이는 것이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 312 / 530

<- **이전**: [250. 메시지 패싱과 위임 (Message Passing & Delegation)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/250_message_passing_delegation/)
**다음**: [252. 암호화 해시 솔트 감리 (Encryption Hash Salt Audit)](/knowledge-base/studynote/11_design_supervision/05_audit_deep_guide/252_encryption_hash_salt_audit/) ->

---
