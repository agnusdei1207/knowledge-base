---
title: 158. 프록시 패턴 (Proxy Pattern)
date: '2025-05-22'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[264_proxy_pattern_surrogate_access_control|프록시]] 패턴 ([[264_proxy_pattern_surrogate_access_control|Proxy]] Pattern)은 실제 객체(Real Subject) 앞에 동일한 인터페이스의 대리 객체를 두어, 접근 제어·[[182_lazy_loading|지연 로딩]]·원격 호출 캡슐화 같은 부가 책임을 중간에서 처리하게 하는 구조 패턴이다.
> 2. **가치**: 클라이언트는 실제 객체를 직접 다루지 않아도 되므로, 무거운 객체 [[087_process_state_transition|생성]] 비용·[[007_security_policy|보안 정책]]·[[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] 같은 복잡성을 감추면서도 사용 방식은 단순하게 유지할 수 있다.
> 3. **판단 포인트**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 기능 확장이 목적이 아니라 접근 중재가 목적이므로, [[262_decorator_pattern_dynamic_wrapper|데코레이터]]([[262_decorator_pattern_dynamic_wrapper|Decorator]])나 [[259_adapter_pattern_interface_wrapper|어댑터]]([[259_adapter_pattern_interface_wrapper|Adapter]])와 혼동하지 말고 "실제 객체 접근을 왜 통제해야 하는가"가 분명할 때 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[264_proxy_pattern_surrogate_access_control|프록시]] 패턴 ([[264_proxy_pattern_surrogate_access_control|Proxy]] Pattern)은 실제 객체에 대한 접근을 다른 객체가 대신 받는 구조다. 객체 [[087_process_state_transition|생성]] 비용이 크거나, 외부 시스템 호출이 느리거나, 권한 통제가 필요하면 클라이언트가 직접 실제 객체를 다루는 순간 코드가 무거워지고 관심사가 섞인다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 이 중간에 서서 "언제 실제 객체를 만들지", "누가 접근할 수 있는지", "호출 전후에 무엇을 기록할지"를 통제한다.

이 패턴이 필요한 이유는 객체지향 설계에서 사용 편의성과 운영 제어가 자주 충돌하기 때문이다. 클라이언트는 단순한 인터페이스를 원하지만, 시스템은 [[303_authentication_authorization_patterns|인증]]·[[456_caching|캐싱]]·원격 통신·[[182_lazy_loading|지연 로딩]] 같은 현실 문제를 처리해야 한다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 인터페이스는 유지하면서도 접근 경로만 바꿔, 클라이언트와 운영 [[164_policy|정책]]을 분리한다.

특히 대용량 이미지 로더, 원격 [[090_service_kubernetes_network_load_balancing|서비스]] 호출 [[460_stub_test_double|stub]], 객체 [[083_relationship_in_er_model|관계]] 매핑(ORM, Object-Relational [[010_schema_mapping|Mapping]])의 [[182_lazy_loading|지연 로딩]]에서 이 패턴의 효과가 뚜렷하다. 실제 객체를 항상 즉시 만들면 메모리와 응답 시간이 낭비되고, 아무 제어 없이 열어 두면 보안과 [[606_auditing_linux_auditd|감사]] 추적이 어려워진다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 이 두 문제를 동시에 다루는 설계 장치다.

- **📢 섹션 요약 비유**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 회사 대표 대신 먼저 방문객을 맞는 비서와 같다. 방문 목적을 확인하고, 필요한 사람만 연결하고, 아직 준비되지 않았다면 잠시 대기시키며 전체 흐름을 정리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[264_proxy_pattern_surrogate_access_control|프록시]] 패턴의 핵심은 [[264_proxy_pattern_surrogate_access_control|프록시]]와 실제 객체가 같은 추상 인터페이스를 구현한다는 점이다. 클라이언트는 인터페이스만 보고 호출하므로, [[264_proxy_pattern_surrogate_access_control|프록시]]가 있든 실제 객체가 직접 오든 코드를 바꿀 필요가 없다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 요청을 가로채 필요한 검사를 수행한 뒤, 조건이 맞으면 실제 객체에 위임한다.

아래 그림은 [[264_proxy_pattern_surrogate_access_control|프록시]]가 단순 전달자가 아니라 "접근 [[164_policy|정책]]이 모이는 제어 지점"임을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────┐
│              프록시 패턴의 호출 흐름과 제어 지점                 │
├──────────────────────────────────────────────────────────────────┤
│ Client                                                           │
│   │                                                              │
│   ▼                                                              │
│ Subject Interface                                                │
│   │                                                              │
│   ▼                                                              │
│ Proxy ---------------------------------------------------------┐ │
│   │ 1) 권한 확인                                              │ │
│   │ 2) 캐시/로그 확인                                         │ │
│   │ 3) 필요 시 Real Subject 생성                              │ │
│   ▼                                                            │ │
│ Real Subject                                                   │ │
│   │                                                            │ │
│   └────────────── 실제 업무 처리 결과 반환 ─────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

이 구조에서 중요한 설계 포인트는 [[264_proxy_pattern_surrogate_access_control|프록시]]가 실제 객체를 "대체"하는 것이 아니라 "대표"한다는 점이다. 즉 [[264_proxy_pattern_surrogate_access_control|프록시]]의 책임은 본업을 새로 만드는 것이 아니라, 접근 조건을 조율하고 실제 객체 호출을 관리하는 데 있다.

| [[264_proxy_pattern_surrogate_access_control|프록시]] 유형 | 핵심 역할 | 대표 사례 | 주의점 |
| :--- | :--- | :--- | :--- |
| 가상 [[264_proxy_pattern_surrogate_access_control|프록시]] (Virtual [[264_proxy_pattern_surrogate_access_control|Proxy]]) | 무거운 객체 [[087_process_state_transition|생성]]을 [[015_지연_데이터_관점|지연]] | 이미지 로딩, ORM [[015_지연_데이터_관점|지연]] 조회 | 첫 호출 [[015_지연_데이터_관점|지연]] 발생 가능 |
| [[571_protection_vs_security|보호]] [[264_proxy_pattern_surrogate_access_control|프록시]] ([[571_protection_vs_security|Protection]] [[264_proxy_pattern_surrogate_access_control|Proxy]]) | 권한 검사와 접근 제어 | 관리자 기능, 결재 승인 | [[164_policy|정책]] 누락 시 보안 구멍 발생 |
| 원격 [[264_proxy_pattern_surrogate_access_control|프록시]] (Remote [[264_proxy_pattern_surrogate_access_control|Proxy]]) | 원격 객체를 로컬처럼 보이게 함 | [[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]]), [[479_grpc_protobuf_http2|gRPC]] (Google [[126_rpc|Remote Procedure Call]]) 클라이언트 [[460_stub_test_double|스텁]] | 네트워크 실패를 숨기면 위험 |
| 캐시 [[264_proxy_pattern_surrogate_access_control|프록시]] | 결과 재사용으로 [[282_performance_tactics|성능]] 개선 | 조회 캐시, [[506_cdn_content_delivery_network_edge_caching|CDN]] 계층 | [[402_cache_coherence|캐시 일관성]] 관리 필요 |

핵심 원리는 결국 "동일 인터페이스 + [[015_지연_데이터_관점|지연]] 위임"이다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 인터페이스 투명성을 유지하면서도 호출 전후에 [[164_policy|정책]]을 삽입할 수 있기 때문에, 객체지향 내부 설계뿐 아니라 리버스 [[264_proxy_pattern_surrogate_access_control|프록시]](Reverse [[264_proxy_pattern_surrogate_access_control|Proxy]]), 응용 프로그래밍 인터페이스([[014_api_posix|API]], [[014_api_posix|Application Programming Interface]]) 게이트웨이, [[302_service_mesh_istio|서비스 메시]] 사이드카처럼 시스템 아키텍처 전체로 확장된다.

- **📢 섹션 요약 비유**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 공연장 입구의 안내 데스크와 같다. 관객은 같은 공연을 보러 오지만, 안내 데스크는 표를 확인하고, 좌석을 안내하고, 필요한 경우 입장을 잠시 [[015_지연_데이터_관점|지연]]시키며 전체 질서를 지킨다.

---

## Ⅲ. 비교 및 연결

[[264_proxy_pattern_surrogate_access_control|프록시]]를 제대로 이해하려면 비슷해 보이는 구조 패턴과의 경계를 분명히 해야 한다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 "[[387_access_control_pattern|접근 통제]]"가 목적이고, [[262_decorator_pattern_dynamic_wrapper|데코레이터]]는 "행동 추가", [[259_adapter_pattern_interface_wrapper|어댑터]]는 "인터페이스 변환", [[263_facade_pattern_simplified_interface|퍼사드]]([[263_facade_pattern_simplified_interface|Facade]])는 "복잡한 서브시스템 단순화"가 목적이다. 겉으로는 모두 중간 객체를 두지만, 채택 이유가 다르다.

| 패턴 | 핵심 목적 | 인터페이스 [[083_relationship_in_er_model|관계]] | 대표 질문 |
| :--- | :--- | :--- | :--- |
| [[264_proxy_pattern_surrogate_access_control|프록시]] ([[264_proxy_pattern_surrogate_access_control|Proxy]]) | 접근 제어, 대리 실행 | 실제 객체와 동일 | "직접 접근을 왜 막거나 [[015_지연_데이터_관점|지연]]해야 하는가?" |
| [[262_decorator_pattern_dynamic_wrapper|데코레이터]] ([[262_decorator_pattern_dynamic_wrapper|Decorator]]) | 책임 추가 | 동일 | "기능을 더 붙이고 싶은가?" |
| [[259_adapter_pattern_interface_wrapper|어댑터]] ([[259_adapter_pattern_interface_wrapper|Adapter]]) | 인터페이스 변환 | 다를 수 있음 | "호환되지 않는 인터페이스를 연결해야 하는가?" |
| [[263_facade_pattern_simplified_interface|퍼사드]] ([[263_facade_pattern_simplified_interface|Facade]]) | 사용 단순화 | 새로운 상위 인터페이스 | "복잡한 하위 시스템을 한 창구로 묶을 것인가?" |

[[264_proxy_pattern_surrogate_access_control|프록시]]는 AOP (Aspect-Oriented Programming, [[338_aspect_oriented_programming|관점 지향 프로그래밍]])와도 연결된다. 스프링의 [[191_transaction_concept_states|트랜잭션]], 보안, 로깅은 본질적으로 [[264_proxy_pattern_surrogate_access_control|프록시]]를 이용해 비즈니스 로직 앞뒤에 공통 관심사를 삽입하는 방식이다. 네트워크 레벨에서는 Nginx 리버스 [[264_proxy_pattern_surrogate_access_control|프록시]], 클라우드에서는 [[302_service_mesh_istio|서비스 메시]] 사이드카가 같은 발상을 더 큰 범위로 구현한다.

즉 [[264_proxy_pattern_surrogate_access_control|프록시]]는 단순한 객체지향 시험 문제를 넘어, "직접 처리하지 말고 중간 계층에서 통제하라"는 아키텍처 사고방식을 대표한다. 그래서 설계감리 관점에서는 패턴 이름보다도, 시스템의 제어점(control point)을 어디에 둘 것인지가 더 중요하다.

- **📢 섹션 요약 비유**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 출입문 앞 경비원이고, [[262_decorator_pattern_dynamic_wrapper|데코레이터]]는 선물 포장지이며, [[259_adapter_pattern_interface_wrapper|어댑터]]는 콘센트 변환기이고, [[263_facade_pattern_simplified_interface|퍼사드]]는 종합 안내 데스크다. 모두 중간에 있지만 맡은 임무가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[264_proxy_pattern_surrogate_access_control|프록시]]는 "중간에 하나 더 두면 편해 보인다"는 이유만으로 쓰면 오히려 복잡도를 키운다. 실제로는 접근 시점과 [[164_policy|정책]]을 통제할 명확한 이유가 있을 때만 효과가 난다. 예를 들어 [[182_lazy_loading|지연 로딩]]이 필요한 [[064_relation_domain|도메인]] 객체, 외부 시스템 호출을 감싸는 클라이언트, 권한 검사가 필수인 [[090_service_kubernetes_network_load_balancing|서비스]] 진입점은 [[264_proxy_pattern_surrogate_access_control|프록시]] 채택 타당성이 높다.

### 실무 적용 포인트

1. **[[182_lazy_loading|지연 로딩]]**: ORM 연관 객체를 처음부터 전부 읽지 않고, 실제 접근 시점에만 조회한다.
2. **보안 제어**: 관리자 화면, 결재 [[014_api_posix|API]], 중요 [[501_file_definition_logical_record|파일]] 접근 전 권한을 중앙에서 검사한다.
3. **원격 호출 캡슐화**: 네트워크 재시도, [[573_timeout_retry_backoff_strategy|타임아웃]], 로깅을 [[264_proxy_pattern_surrogate_access_control|프록시]] 계층에 모아 클라이언트를 단순화한다.
4. **[[606_auditing_linux_auditd|감사]] 추적**: 누가 언제 어떤 자원에 접근했는지 일관된 로깅 포인트를 만든다.

### 설계 감리 관점의 [[435_checklist_based_testing|체크리스트]]

- [[264_proxy_pattern_surrogate_access_control|프록시]]와 실제 객체가 정말 같은 인터페이스를 유지하는가?
- [[264_proxy_pattern_surrogate_access_control|프록시]] 내부에 본업 로직이 침투해 [[355_process|단일 책임 원칙]]([[243_srp_single_responsibility_principle|SRP]], [[243_srp_single_responsibility_principle|Single Responsibility Principle]])을 해치지 않는가?
- 원격 [[264_proxy_pattern_surrogate_access_control|프록시]]라면 네트워크 실패와 [[015_지연_데이터_관점|지연]]을 호출자에게 적절히 드러내는가?
- [[182_lazy_loading|지연 로딩]]으로 인해 N+1 조회 같은 [[282_performance_tactics|성능]] 함정이 생기지 않는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- **만능 [[264_proxy_pattern_surrogate_access_control|프록시]]화**: 로깅, 보안, 캐시, [[395_verification_process_review|검증]], 업무 규칙을 한 [[264_proxy_pattern_surrogate_access_control|프록시]]에 몰아넣는 경우
- **원격 호출 은폐**: 로컬 메서드처럼 보이게 만들어 네트워크 비용과 실패 가능성을 잊게 하는 경우
- **불필요한 래핑**: 직접 호출해도 충분한 단순 객체에 억지로 [[264_proxy_pattern_surrogate_access_control|프록시]]를 두는 경우

기술사 답안에서는 [[264_proxy_pattern_surrogate_access_control|프록시]]를 "객체 접근의 제어점"으로 설명하고, 적용 사례로 AOP, ORM [[182_lazy_loading|지연 로딩]], 리버스 [[264_proxy_pattern_surrogate_access_control|프록시]]를 연결하면 설계 수준의 이해를 보여주기 좋다.

- **📢 섹션 요약 비유**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 모든 길목에 톨게이트를 세우는 일이 아니라, 통제가 꼭 필요한 진입로에만 게이트를 두는 일이다. 필요한 곳에 두면 질서가 생기지만, 아무 데나 세우면 차만 막힌다.

---

## Ⅴ. 기대효과 및 결론

[[264_proxy_pattern_surrogate_access_control|프록시]] 패턴을 올바르게 적용하면 클라이언트 코드는 단순해지고, 접근 제어 [[164_policy|정책]]은 중앙화되며, 무거운 객체 [[087_process_state_transition|생성]] 시점도 조절할 수 있다. 이는 [[282_performance_tactics|성능]] 최적화와 보안 강화, [[346_maintainability_portability|유지보수성]] 향상으로 이어진다. 특히 공통 관심사를 한곳에 모을 수 있어, 기능 변경보다 운영 [[164_policy|정책]] 변경이 잦은 시스템에서 효과가 크다.

반면 [[264_proxy_pattern_surrogate_access_control|프록시]]는 호출 경로를 한 단계 더 늘리기 때문에, 숨겨진 [[015_지연_데이터_관점|지연]]과 디버깅 난도를 높일 수 있다. 또한 [[264_proxy_pattern_surrogate_access_control|프록시]] 내부가 비대해지면 본래 의도였던 단순화가 사라지고, 실제 객체보다 [[264_proxy_pattern_surrogate_access_control|프록시]]가 더 중요한 복합 객체가 되는 역전 현상도 생긴다. 따라서 [[264_proxy_pattern_surrogate_access_control|프록시]]는 "기능을 더하는 패턴"이 아니라 "직접 접근을 통제하는 패턴"이라는 초점을 잃지 않아야 한다.

앞으로도 [[264_proxy_pattern_surrogate_access_control|프록시]]의 중요성은 줄지 않는다. 객체지향 코드 안에서는 동적 [[264_proxy_pattern_surrogate_access_control|프록시]]와 AOP로, 인프라에서는 [[014_api_posix|API]] 게이트웨이와 [[302_service_mesh_istio|서비스 메시]]로 계속 확장되고 있기 때문이다. 기억해야 할 핵심은 하나다. [[264_proxy_pattern_surrogate_access_control|프록시]]는 실제 일을 대신하는 척하면서, 사실은 시스템의 통제 질서를 세우는 패턴이다.

- **📢 섹션 요약 비유**: [[264_proxy_pattern_surrogate_access_control|프록시]]는 집 현관문과 같다. 문 자체가 생활을 대신하지는 않지만, 누가 들어오고 나가는지 통제함으로써 집 전체의 안전과 질서를 지켜 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Subject Interface | 클라이언트가 의존하는 추상 계약으로, [[264_proxy_pattern_surrogate_access_control|프록시]]의 투명성을 보장함 |
| Real Subject | 실제 업무를 수행하는 원본 객체 |
| Virtual [[264_proxy_pattern_surrogate_access_control|Proxy]] | 무거운 객체 [[087_process_state_transition|생성]]을 실제 사용 시점까지 미루는 방식 |
| [[571_protection_vs_security|Protection]] [[264_proxy_pattern_surrogate_access_control|Proxy]] | 권한·[[303_authentication_authorization_patterns|인증]] [[164_policy|정책]]을 실제 호출 전에 적용하는 방식 |
| Remote [[264_proxy_pattern_surrogate_access_control|Proxy]] | 원격 [[090_service_kubernetes_network_load_balancing|서비스]] 호출을 로컬 객체처럼 감싸는 방식 |
| [[262_decorator_pattern_dynamic_wrapper|데코레이터]] ([[262_decorator_pattern_dynamic_wrapper|Decorator]]) | 동일 인터페이스를 쓰지만 목적이 접근 제어가 아니라 기능 확장임 |
| AOP (Aspect-Oriented Programming) | [[264_proxy_pattern_surrogate_access_control|프록시]] 기반으로 공통 관심사를 삽입하는 대표 활용 영역 |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 접근의 한계
    │
    ▼
추상 인터페이스 분리
    │
    ▼
프록시 (Proxy) 패턴
    │
    ├─▶ 가상 프록시 (Virtual Proxy)
    ├─▶ 보호 프록시 (Protection Proxy)
    ├─▶ 원격 프록시 (Remote Proxy)
    │
    ▼
AOP · ORM 지연 로딩 · 리버스 프록시 · 서비스 메시
```

이 흐름은 [[264_proxy_pattern_surrogate_access_control|프록시]]가 단순 객체 패턴에서 출발해, 애플리케이션 프레임워크와 인프라 제어 계층으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[264_proxy_pattern_surrogate_access_control|프록시]]는 중요한 사람을 바로 만나기 전에 먼저 이야기해 주는 비서 같은 거예요.
2. 비서는 아무나 들여보내지 않고, 준비가 되면 그때 진짜 사람에게 연결해 줘요.
3. 그래서 사람들은 더 안전하고 편하게 일을 맡길 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 214 / 530

← **이전**: [[157_flyweight_pattern|157. 플라이웨이트 (Flyweight) 패턴]]
**다음**: [[159_proxy_pattern_types|159. 프록시 패턴 유형 (Proxy Pattern Types)]] →

---
