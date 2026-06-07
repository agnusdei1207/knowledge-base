---
title: "Chain of Responsibility Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 199
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/) ([Chain of Responsibility](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/) Pattern)은 GoF [행위 패턴](/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/)으로, 요청을 처리할 수 있는 객체들을 체인(연쇄)으로 연결하여, 요청 발신자와 수신자를 분리하고 요청이 적절한 핸들러(Handler)를 찾을 때까지 체인을 따라 전달되게 하는 패턴이다.
> 2. **가치**: 요청의 발신자가 어떤 객체가 요청을 처리할지 알 필요 없고, 핸들러를 동적으로 추가·재배열할 수 있어 유연성이 높다. 서블릿 필터 체인, 스프링 인터셉터 체인, 미들웨어 파이프라인이 대표적인 구현이다.
> 3. **판단 포인트**: [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)은 요청이 반드시 처리된다는 보장이 없다(체인 끝까지 처리자가 없을 수 있음). 반드시 처리되어야 하는 요청은 기본 핸들러(Default Handler)를 체인 끝에 배치하거나, 예외를 발생시켜야 한다. 핸들러 수가 많거나 체인이 복잡해지면 디버깅이 어렵다.

---

## Ⅰ. 개요 및 필요성

고객 지원 시스템에서 문의가 들어오면: 1차(일반 상담원) -> 2차(기술 전문가) -> 3차(관리자)로 처리 능력에 따라 요청이 전달된다. 각 담당자가 처리 가능하면 처리하고, 불가능하면 다음 담당자에게 전달한다.

조건 분기로 구현하면: `if (level == "basic") { ... } else if (level == "tech") { ... }` — 새 레벨 추가 시 기존 코드를 수정해야 한다. [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)은 각 핸들러가 독립적으로 처리 여부를 결정하고 다음 핸들러로 위임한다.

```text
+-------------------------------------------------------------+
|          책임 연쇄 패턴 구조                                  |
+-------------------------------------------------------------+
|  Client -> Handler (인터페이스)                              |
|           - next: Handler                                   |
|           + setNext(h: Handler): Handler                    |
|           + handle(request): void                           |
|                ^                                            |
|  Handler A -> Handler B -> Handler C -> null                   |
|  (처리 or 다음으로)       (처리 or 다음으로)                 |
|                                                             |
|  request -> A가 처리? Yes->결과, No->B로 전달                  |
|              -> B가 처리? Yes->결과, No->C로 전달              |
|                -> C가 처리? Yes->결과, No->처리 안 됨          |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 민원(요청)이 동사무소 창구(Handler A) -> 구청(Handler B) -> 시청(Handler C)을 거쳐 처리된다. 민원인은 누가 처리할지 알 필요 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서블릿 필터 체인이 [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)의 대표 구현이다. 각 필터(`AuthFilter`, `LogFilter`, `CorsFilter`)가 `doFilter(request, response, filterChain)` 메서드에서 처리 후 `filterChain.doFilter()`를 호출해 다음 필터로 전달한다. 전달하지 않으면 체인이 끊긴다(요청 차단).

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 선형 체인 | 순서대로 전달, 처리하면 중단 | 고객 지원 에스컬레이션 |
| 파이프라인 | 모든 핸들러를 통과, 각각 처리 | 서블릿 필터 체인 |
| 분기 체인 | 조건에 따라 다른 체인으로 분기 | 복잡한 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |

```text
+-------------------------------------------------------------+
|       서블릿 필터 체인 동작                                   |
+-------------------------------------------------------------+
|  Request -> AuthFilter -> LogFilter -> CorsFilter -> Servlet    |
|                                                             |
|  AuthFilter.doFilter(req, res, chain) {                     |
|    if (!authenticated) { res.sendError(401); return; }      |
|    chain.doFilter(req, res);  // 다음 필터로 전달            |
|  }                                                          |
|                                                             |
|  Response <- AuthFilter <- LogFilter <- CorsFilter <- Servlet  |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 공항 보안 검색([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) Filter) -> 신분증 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) Filter) -> 짐 검사(CORS Filter)를 모두 통과해야 탑승(Servlet)할 수 있다.

---
## Ⅲ. 비교 및 연결

[책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)과 [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/)의 비교: [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 기능을 추가하고 항상 다음으로 전달하지만, [책임 연쇄](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)는 처리 여부에 따라 전달 여부를 결정한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 전달 여부 | 조건부 (처리하면 중단 가능) | 항상 다음으로 전달 |
| 목적 | 요청 처리자 탐색 | 기능 추가 |
| 체인 순서 | 중요 (처리자 찾는 순서) | 중요 (기능 추가 순서) |
| GoF [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [행위 패턴](/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/) | [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) |

- **📢 섹션 요약 비유**: [책임 연쇄](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)는 고객 상담 에스컬레이션(처리 가능하면 중단), [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 피자에 토핑 추가(모두 통과, 기능 누적)다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링 Security는 `SecurityFilterChain`으로 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)를 처리한다. 각 필터가 [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [세션 관리](/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/), [CSRF](/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 등 독립적인 보안 처리를 담당하고, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 실패 시 체인을 끊어 요청을 차단한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 요청이 체인을 따라 전달되고, 각 핸들러가 독립적으로 처리 여부를 결정하는가?
2. 처리 불가 시 next.handle()로 다음 핸들러에 위임하는가?
3. 처리 보장이 필요한 경우 기본 핸들러(Default Handler)가 체인 끝에 있는가?
4. 핸들러를 동적으로 추가·재배열할 수 있어 유연성이 높은가?
5. 서블릿 필터 체인처럼 파이프라인 방식(모두 통과)과 선택적 처리 방식의 차이를 이해하는가?

- **📢 섹션 요약 비유**: 스프링 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 필터 체인은 공항 보안처럼, 각 단계([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)->[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)->[CSRF](/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/))를 통과해야 하고, 하나라도 실패하면 요청이 차단된다.

---

## Ⅴ. 기대효과 및 결론

[책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)을 적용하면 요청 발신자와 수신자가 분리되고, 핸들러를 동적으로 추가·재배열하여 처리 흐름을 유연하게 변경할 수 있다. 서블릿 필터 체인, 스프링 인터셉터, 미들웨어 파이프라인이 이 패턴의 실무 구현이다.

한계는 처리 보장이 없고, 긴 체인에서 디버깅이 어려우며, 처리자를 추적하기 어렵다. 모든 핸들러를 항상 통과해야 하는 경우 파이프라인 패턴([Pipe-Filter](/studynote/04_software_engineering/04_testing_quality/207_pipe_filter_architecture_data_stream/))이 더 명확한 표현이다.

- **📢 섹션 요약 비유**: [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)은 공문서가 부서를 거쳐 결재되듯, 각 부서(핸들러)가 처리 가능하면 결재하고 불가능하면 상위 부서(다음 핸들러)로 올린다.

---

### 📌 관련 개념 맵

[요청-처리자 결합 문제] -> [책임 연쇄 패턴] -> [서블릿 필터 체인] -> [스프링 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) FilterChain] -> [미들웨어 파이프라인]

| 개념 | 연결 포인트 |
|:---|:---|
| [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) | [책임 연쇄](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)와 구조 유사, 의도 다름 |
| [파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/) | [책임 연쇄](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)의 모두-통과 변형 |
| 스프링 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | SecurityFilterChain 구현 |
| 미들웨어 | Node.js Express 미들웨어가 [책임 연쇄](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/) 구현 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [Chain of Responsibility](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)(1994)] -> [서블릿 필터 체인] -> [스프링 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)] -> [클라우드 [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) 미들웨어] -> [서비스 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 필터]

### 👶 어린이를 위한 3줄 비유 설명

1. [책임 연쇄 패턴](/studynote/11_design_supervision/06_exam_summary/395_process/)은 고객 센터처럼, 1차 상담원이 못 해결하면 2차 전문가, 그래도 안 되면 3차 관리자에게 전달해요.
2. 서블릿 필터 체인이 바로 이 패턴이에요 - 각 필터가 처리하고 다음으로 넘겨요.
3. 요청을 보내는 쪽은 누가 처리할지 알 필요 없어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 260 / 530

<- **이전**: [198. 상태 vs 전략 패턴 비교 (State vs Strategy Pattern)](/studynote/11_design_supervision/04_gof_behavioral/198_state_vs_strategy/)
**다음**: [200. 책임 연쇄 패턴 장단점 (Chain of Responsibility Pros and Cons)](/studynote/11_design_supervision/04_gof_behavioral/200_chain_of_responsibility_pros_cons/) ->

---
