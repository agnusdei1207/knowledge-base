---
title: "159. 프록시 패턴 유형 (Proxy Pattern Types)"
date: "2026-04-21"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트

> 1. **본질**: [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) 패턴은 실제 객체 (Real Subject)와 동일한 인터페이스를 가진 대리 객체를 앞단에 두어, 클라이언트가 원본 대신 대리자를 통해 접근하도록 만드는 [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/)이다.
> 2. **가치**: 같은 인터페이스 뒤에서 [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), 권한 통제, 원격 호출을 숨길 수 있어 클라이언트 코드를 바꾸지 않고도 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·보안·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리를 분리할 수 있다.
> 3. **판단 포인트**: [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 유형 선택은 "무엇을 숨기거나 제어하려는가"에 달려 있다. [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용이면 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) (Virtual [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)), 접근 권한이면 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)), 네트워크 경계면 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) (Remote [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))가 맞다.

---

## Ⅰ. 개요 및 필요성

[프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 패턴은 원본 객체에 직접 접근할 때 생기는 비용과 위험을 대리 객체 하나로 흡수하는 패턴이다. 객체 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 무겁거나, 사용자 권한을 먼저 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 하거나, 실제 객체가 다른 프로세스·서버에 있을 때 클라이언트가 그 복잡성을 알 필요는 없다. 이때 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 "같은 문 손잡이"를 유지한 채, 문 뒤에서 필요한 절차를 대신 수행한다.

이 패턴이 중요한 이유는 관심사 분리 (Separation of Concerns) 때문이다. 비즈니스 로직은 핵심 동작에 집중하고, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점 제어·보안 검사·직렬화와 네트워크 전송 같은 횡단 관심사 (Cross-Cutting Concern)는 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 맡는다. 직접 코드마다 삽입하면 중복과 [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)가 커지지만, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 쓰면 구조적으로 제어 지점을 한곳에 모을 수 있다.

- **📢 섹션 요약 비유**: [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 사장실 앞 비서와 같다. 방문자는 같은 문으로 들어오지만, 비서는 약속 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)·신분 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)·원격 전달 같은 절차를 먼저 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)의 구조는 단순하다. 핵심은 `Client`가 `Subject` 인터페이스만 의존하고, `Proxy`와 `Real Subject`가 같은 계약을 구현한다는 점이다. 덕분에 클라이언트는 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 있는지조차 몰라도 되며, 교체 비용이 매우 낮다.

```text
+----------------------------------------------------------------------+
|               프록시 패턴의 공통 구조와 유형별 개입 지점            |
+----------------------------------------------------------------------+
|  Client ---> Subject 인터페이스 ---> Proxy ---> Real Subject           |
|                                   |                                  |
|                                   +- 가상 프록시: 필요 시점에 생성   |
|                                   +- 보호 프록시: 권한 통과 후 위임   |
|                                   +- 원격 프록시: 직렬화·전송 후 위임 |
+----------------------------------------------------------------------+
```

이 그림의 핵심은 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 단순 중계자가 아니라 <strong>개입 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>의 실행 지점</strong>이라는 점이다. 같은 인터페이스를 유지하므로 설계는 투명하지만, 내부에서는 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점·접근 허용 여부·원격 통신 절차가 달라진다.

| 유형 | 해결하려는 문제 | 핵심 동작 | 대표 사례 |
| :--- | :--- | :--- | :--- |
| 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) (Virtual [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | 무거운 객체의 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용 | 최초 접근 시 실제 객체 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 이미지 [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), ORM [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/) |
| [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | 권한 없는 접근 차단 | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 후 실제 객체 위임 | 관리자 기능, 문서 열람 권한 제어 |
| 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) (Remote [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | 네트워크 경계의 복잡성 은닉 | 직렬화·호출·응답 복원 수행 | [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)), [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) |

가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 메모리와 시작 시간을 절약하지만, 첫 접근 시 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 생긴다. [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 보안을 강화하지만 권한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)에 과도하게 쌓이면 복잡해질 수 있다. 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 로컬 객체처럼 사용하게 해 주지만, 실제로는 네트워크 실패와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 동반하므로 "투명성"이 지나치면 오히려 위험하다.

- **📢 섹션 요약 비유**: 같은 창구라도 어떤 창구는 물건이 필요할 때만 창고를 열고, 어떤 창구는 신분증을 먼저 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 어떤 창구는 다른 지점에 전화를 걸어 대신 처리해 준다.

---

## Ⅲ. 비교 및 연결

[프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/))나 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))와 외형이 비슷해 자주 혼동된다. 하지만 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 기능 추가보다 **접근 제어**, [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 **인터페이스 변환**, [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 <strong>책임 확장</strong>이 목적이다. 즉 모두 감싸지만, 왜 감싸는지가 다르다.

| 비교 항목 | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)) | [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)) |
| :--- | :--- | :--- | :--- |
| 핵심 목적 | 접근 제어와 대리 실행 | 기능 추가와 조합 | 인터페이스 호환 |
| 인터페이스 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 원본과 동일 | 원본과 동일 | 다른 인터페이스를 변환 |
| 클라이언트 기대 | 원본처럼 투명해야 함 | 장식 조합을 인지할 수 있음 | 대상 인터페이스만 알면 됨 |
| 대표 질문 | "언제/누가 접근 가능한가?" | "무슨 기능을 더 붙일까?" | "어떻게 연결 가능하게 바꿀까?" |

또한 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 유형끼리도 경계가 중요하다. 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화, [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 보안, 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 추상화가 핵심이다. 따라서 설계 답안에서는 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 한 단어로 뭉뚱그리지 말고, <strong>문제 유형에 따라 어떤 <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a>가 맞는지</strong> 분리해 써야 한다.

- **📢 섹션 요약 비유**: [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 문지기, [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 액세서리, [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 변환 젠더다. 겉모습은 비슷해도 맡은 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 객체 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 매핑 (ORM, Object-Relational [Mapping](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))의 [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/)에서 자주 보인다. 예를 들어 JPA (Java Persistence [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))의 연관 컬렉션은 실제 데이터를 바로 읽지 않고, 접근 순간 SQL을 실행하는 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 객체로 주입된다. 이때 편리함은 크지만, 반복 조회가 쌓이면 N+1 문제가 발생하므로 `fetch join`이나 배치 조회 전략과 함께 판단해야 한다.

[보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메서드 앞단의 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 처리에 적합하다. 관리자만 가능한 기능을 실제 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 객체 내부에 하드코딩하면 로직이 오염되지만, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)나 AOP (Aspect-Oriented Programming, [관점 지향 프로그래밍](/studynote/04_software_engineering/06_software_architecture/338_aspect_oriented_programming/)) 레이어에서 권한을 검사하면 핵심 기능과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 분리할 수 있다. 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) (Google [Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)), RMI (Remote Method Invocation)처럼 네트워크를 캡슐화할 때 유용하지만, 로컬 호출처럼 보이게 만든 탓에 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)·재시도·부분 실패를 과소평가하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이 자주 생긴다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용 제어가 목적이면 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를, 보안이 목적이면 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 우선 고려한다.
2. 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 쓸 때는 반드시 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)·재시도·서킷 브레이커를 함께 설계한다.
3. [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 도입해도 인터페이스가 불안정하면 [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 완화 효과가 줄어든다.
4. 숨겨진 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 예외 흐름이 운영 장애로 이어지지 않도록 관측성을 확보한다.

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 원격 호출을 로컬 메서드처럼 가볍게 취급하는 설계
- [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)에 모든 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 몰아 넣어 비대해지는 설계
- 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 남발해 첫 조회 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 N+1 문제를 키우는 설계

- **📢 섹션 요약 비유**: [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 편리한 대리 창구지만, 창구 뒤에 창고·보안 게이트·해외 연락망이 숨어 있다는 사실을 잊으면 운영 사고가 난다.

---

## Ⅴ. 기대효과 및 결론

[프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 패턴을 올바르게 적용하면 클라이언트는 단순해지고, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·보안·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 독립적으로 교체 가능해진다. 이는 [개방-폐쇄 원칙](/studynote/11_design_supervision/06_exam_summary/356_process/) ([OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/), [Open-Closed Principle](/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/))과 [의존 역전 원칙](/studynote/11_design_supervision/06_exam_summary/359_process/) ([DIP](/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/), [Dependency Inversion Principle](/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/))을 실무적으로 구현하는 좋은 방법이기도 하다. 특히 [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) 관점에서 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 "동일 인터페이스 유지"와 "[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 삽입"을 동시에 달성한다.

다만 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 투명성이 장점인 동시에 함정이다. 호출 비용, 권한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 네트워크 실패가 숨겨져 보이지 않으면 개발자는 실제 시스템 경계를 과소평가하게 된다. 따라서 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 "감추는 패턴"이 아니라, <strong>필요한 복잡성을 인터페이스 뒤로 정리하되 운영상 의미는 분명히 드러내는 패턴</strong>으로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 일을 대신 처리해 주는 비서지만, 나쁜 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 어디서 시간이 새고 왜 막혔는지 보이지 않게 만드는 검은 상자가 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) (Structural Pattern) | 객체 조합과 인터페이스 구성을 다루는 상위 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 실제 객체 (Real Subject) | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 대신 접근을 제어하는 원본 대상 |
| [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/) ([Lazy Loading](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/)) | 가상 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 해결하는 대표 문제 |
| 접근 제어 ([Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)의 핵심 목적 |
| 원격 호출 (Remote [Call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/)) | 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 숨기는 네트워크 경계 |
| [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/)) | 동일 인터페이스 래핑이지만 목적이 다른 비교 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
구조 패턴 (Structural Pattern)
    |
    v
프록시 (Proxy) 패턴
    |
    +--> 가상 프록시 (지연 로딩)
    +--> 보호 프록시 (권한 통제)
    +--> 원격 프록시 (분산 호출 캡슐화)
    |
    v
AOP 기반 동적 프록시 · ORM 지연 로딩 · RPC 스텁
```

이 흐름은 "[구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/)의 일반론 -> [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)의 공통 구조 -> 목적별 세부 유형 -> 현대 프레임워크 적용"으로 이어지는 학습 경로를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 진짜 사람 대신 먼저 나와서 일을 처리해 주는 대리인이에요.
2. 어떤 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 물건이 필요할 때만 창고를 열고, 어떤 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 출입증을 먼저 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
3. 또 어떤 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 멀리 있는 사람에게 대신 전화해서 답을 받아오는 똑똑한 전달자예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 215 / 530

<- **이전**: [158. 프록시 패턴 (Proxy Pattern)](/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)
**다음**: [160. 디자인 패턴과 설계 원칙 (OCP·DIP와 디자인 패턴)](/studynote/11_design_supervision/03_gof_creational_structural/160_design_pattern_ocp_dip_principles/) ->

---
