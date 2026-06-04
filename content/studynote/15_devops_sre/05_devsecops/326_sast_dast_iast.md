+++
title = "326. SAST DAST IAST 보안 테스트 비교 CI 파이프라인 배치 (SAST DAST IAST Security Testing Pipeline)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) ([Static Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/))는 코드를 실행하지 않고 소스코드를 분석해 취약점을 찾고, [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) ([Dynamic Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/))는 실행 중인 애플리케이션에 공격을 시뮬레이션한다. [IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/) ([Interactive Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/))는 두 방식을 결합해 런타임에 내부에서 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링한다.
> 2. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 배치</strong>: SAST는 코딩 단계([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 시), DAST는 스테이징 환경 배포 후, IAST는 [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) 실행 시에 배치한다. 각각 다른 유형의 취약점을 찾으므로 상호 보완적이다.
> 3. **판단 포인트**: SAST의 최대 문제는 False Positive(오탐) 비율이 높다는 것이다. [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 결과를 그대로 All-Block하면 개발팀이 경고를 무시하게 된다. 위험도 기반 필터링과 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 인식 분석이 필요하다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 취약점의 대부분은 코딩 실수([SQL Injection](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/), [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/), 버퍼 오버플로)에서 시작된다. 이 취약점들은 개발 단계에서 자동 도구로 잡을 수 있음에도, 전통적으로 운영 환경에서 침투 테스터나 실제 공격자에 의해 발견되는 경우가 많았다.

[SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)/IAST는 이 취약점들을 개발 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 내에서 자동으로 찾는 도구들이다. OWASP (Open Web Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/)) Top [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 취약점 대부분이 이 도구들로 탐지 가능하다.

> 📢 **섹션 요약 비유**: SAST는 건물 도면의 구조적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 찾고, DAST는 완성된 건물을 실제로 흔들어보는 내진 테스트다. IAST는 건물 내부 센서가 실시간으로 구조 이상을 감지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+----------------------------------------------------------------+
|              SAST / DAST / IAST 파이프라인 배치                  |
+----------------------------------------------------------------+
|                                                                |
|  [코드 커밋]--->[SAST]--->[빌드]--->[단위테스트]--->[스테이징 배포]|
|       |          |                                    |        |
|      PR 생성    정적 분석                         [DAST]       |
|                소스코드에서                      [IAST]        |
|                SQL Injection                  동적 공격        |
|                XSS 패턴 탐지                   시뮬레이션       |
|                하드코딩 시크릿                  런타임 내부      |
|                                                모니터링         |
+----------------------------------------------------------------+
```

| 항목 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) | [IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/) |
|:---|:---|:---|:---|
| 분석 대상 | 소스코드 (정적) | 실행 중 앱 (동적) | 런타임 내부 (하이브리드) |
| 실행 시점 | 빌드 전 | 스테이징 후 | [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) 중 |
| 언어 의존 | 언어별 분석기 필요 | 언어 무관 | 에이전트 언어 지원 |
| False Positive | 높음 | 낮음 | 낮음 |
| False Negative | 낮음 (코드 전수 분석) | 높음 (공격 경로 제한) | 중간 |
| 대표 도구 | [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/), Semgrep, Checkmarx | [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/), [Burp Suite](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/) | Contrast [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) |

> 📢 **섹션 요약 비유**: SAST는 책의 오탈자를 편집자가 읽으면서 찾는 것이고, DAST는 독자가 실제 읽다가 오탈자를 발견하는 것이며, IAST는 책 내부에 센서가 있어 읽는 순간 오탈자를 알려주는 것이다.

---

## Ⅲ. 비교 및 연결

[SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 주요 탐지 취약점:
- <strong><a href="/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/">SQL Injection</a></strong>: 사용자 입력이 직접 SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 삽입되는 패턴
- <strong><a href="/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/">XSS</a> (<a href="/knowledge-base/studynote/09_security/05_web_app_security/470_xss/">Cross-Site Scripting</a>)</strong>: 사용자 입력이 HTML에 직접 출력되는 패턴
- <strong>하드코딩된 <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/">시크릿</a></strong>: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키, 비밀번호가 코드에 직접 기재
- <strong>취약한 <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/">암호화 알고리즘</a></strong>: [MD5](/knowledge-base/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/), SHA-1 사용

[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) 주요 탐지:
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 우회</strong>: [세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/) 취약점
- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 엔드포인트 취약점</strong>: 숨겨진 파라미터, [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 누락
- <strong>서버 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 오류</strong>: 디버그 모드, 불필요한 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메서드 허용

> 📢 **섹션 요약 비유**: SAST와 DAST는 서로 다른 안경을 쓰고 보는 것이다. SAST는 설계 안경으로 코드의 패턴을 보고, DAST는 공격자 안경으로 실제 동작을 본다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) False Positive 관리

1. **룰 튜닝**: 프로젝트 특성에 맞게 규칙 비활성화/조정
2. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a> 필터</strong>: 테스트 코드, [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 코드 제외
3. **위험도 기반 게이트**: Critical/High만 차단, Medium 이하 경고
4. <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: 기존 이슈 무시, 신규 이슈만 차단

### 도구 선택 기준

- **소규모 프로젝트**: Semgrep (빠름, 커스텀 룰 용이) + [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/)
- **엔터프라이즈**: [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) Enterprise + Checkmarx + [Burp Suite](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/) Enterprise
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 우선</strong>: Semgrep + [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/) + Trivy ([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))

> 📢 **섹션 요약 비유**: [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 룰 튜닝은 화재경보기 민감도 조정이다. 너무 민감하면 요리할 때마다 경보가 울리고, 너무 둔하면 실제 화재를 놓친다.

---

## Ⅴ. 기대효과 및 결론

[SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)/IAST를 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD에 통합하면 [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) 취약점의 상당 부분을 운영 이전에 제거할 수 있다. 침투 테스터의 수동 작업 범위가 줄어들고, 실제 0-day와 비즈니스 로직 취약점에 집중할 수 있다.

핵심은 <strong>도구가 개발 속도를 방해하지 않는 것</strong>이다. PR에서 SAST가 30분이 걸린다면 개발자가 우회방법을 찾는다. 5분 내 피드백, 높은 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)의 결과만이 문화로 정착한다.

> 📢 **섹션 요약 비유**: [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/DAST는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등이다. 정확하게 작동하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등은 교통을 안전하게 하지만, 오작동하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등은 교통 혼란을 일으킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) ([Static Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)) | 소스코드 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/), 언어 종속 |
| [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) ([Dynamic Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)) | 실행 중 동적 공격 시뮬레이션 |
| [IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/) ([Interactive Application Security Testing](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/)) | 런타임 에이전트 기반 하이브리드 |
| [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) | 웹 애플리케이션 10대 취약점 |
| [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) 플랫폼 |
| Semgrep | 빠른 커스텀 룰 기반 [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 보안 검수 시대         SAST/DAST 자동화             AI 보안 분석 시대
------------------   --------------------------   -----------------------
수동 코드 리뷰        ->  SAST CI 통합 (SonarQube) ->  AI 기반 취약점 분류
침투 테스터 전담           DAST 스테이징 자동화          Semgrep 커스텀 룰
운영 후 취약점 발견         IAST 하이브리드 접근          CNAPP 내 SAST 통합
                            False Positive 관리           LLM 코드 보안 리뷰
```

### 👶 어린이를 위한 3줄 비유 설명

1. SAST는 글을 쓰고 나서 맞춤법 검사기로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 거예요. 코드를 실행하지 않아도 실수를 찾을 수 있어요.
2. DAST는 완성된 음식을 직접 먹어보고 맛이 이상한지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 거예요. 실제로 해보지 않으면 모르는 문제가 있어요.
3. IAST는 음식 재료 안에 센서를 넣어서 요리하면서 자동으로 이상한 점을 알려주는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 326 / 373

<- **이전**: [325. DevSecOps 시프트 레프트 보안 조기 점검 (DevSecOps Shift-Left Security STRIDE Threat](/knowledge-base/studynote/11_design_supervision/06_exam_summary/325_audit/)
**다음**: [327. SCA 오픈소스 컴플라이언스 스캔 (SCA Software Composition Analysis Open Source Compliance](/knowledge-base/studynote/11_design_supervision/06_exam_summary/327_process/) ->

---
