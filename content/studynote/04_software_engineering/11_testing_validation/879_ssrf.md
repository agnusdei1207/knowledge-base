+++
title = "879. SSRF (Server-Side Request Forgery)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))는 서버의 네트워크 권한을 악용하는 공격이다. 사용자가 입력한 URL을 서버가 직접 호출할 때 자주 생긴다.

내부 주소 접근과 클라우드 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 유출이 특히 위험하다.

- **📢 섹션 요약 비유**: 배달원이 대신 문을 열어 보게 만드는 것과 같다.

---

다음은 [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) (Server-Side Re의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  SSRF (Server-Side Re                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) (Server-Side Re가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 서버가 요청할 수 있는 대상을 제한하는 것이다.

```text
사용자 입력 URL -> 서버 요청 -> 내부/외부 자원 접근
                   ^ 여기서 통제 필요
```

| 방어 | 설명 |
|:---|:---|
| Allowlist | 허용 도메인만 접근 |
| [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 내부 IP 우회 차단 |
| 네트워크 격리 | 민감 자원 분리 |

- **📢 섹션 요약 비유**: 택배 기사가 아무 집이나 가지 못하게 배달 구역을 정하는 것이다.

---

---

---

---

## Ⅲ. 비교 및 연결

SSRF는 입력 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 아니라 네트워크 경계 문제이기도 하다.

| 구분 | 안전한 설계 | 위험한 설계 |
|:---|:---|:---|
| 대상 | 허용된 목적지 | 임의 URL |
| 효과 | 요청 통제 | 내부망 노출 |
| 범위 | 애플리케이션/네트워크 | 서버 전체 |

클라우드 환경에서는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 접근 차단이 중요하다.

- **📢 섹션 요약 비유**: 집 밖에서 전화를 걸게 했는데, 그 전화가 금고 열쇠로 이어지면 큰일이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 외부 URL 프리뷰, 이미지 가져오기, [웹훅](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/), [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 기능에서 많이 점검한다.

검토 포인트는 다음과 같다.
1. 요청 목적지가 허용 목록에 있는가?
2. 내부 IP, 루프백, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 주소를 차단하는가?
3. 리다이렉트와 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 재해석을 통제하는가?

- **📢 섹션 요약 비유**: 우체국 창구에서 보낼 수 있는 나라를 미리 정해야 한다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

SSRF를 막으면 내부 시스템과 클라우드 자산을 지킬 수 있다.

결론적으로 이 항목은 "서버가 대신 공격받는 문제"다.

- **📢 섹션 요약 비유**: 집 문을 대신 두드려 주는 심부름을 아무에게나 맡기면 안 된다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/)) 적용 결과는 QA 활동을 통해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
SSRF (Server-Side Request Forgery) 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) ([Server-Side Request Forgery](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 565 / 973

<- **이전**: [486. Security Logging and Monitoring Failures (보안 로깅 및 모니터링 실패)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/878_security_logging_and_monitoring_failures/)
**다음**: [487. SSRF (Server-Side Request Forgery) - 서버 측 요청 위조](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/487_ssrf_server_side_request_forgery/) ->

---
