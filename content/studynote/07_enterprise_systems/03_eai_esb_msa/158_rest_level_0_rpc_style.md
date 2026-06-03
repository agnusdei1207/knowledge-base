+++
title = "158. Level 0 - 단일 URI, 단일 POST 메서드만 사용 (RPC 스타일)"
date = 2026-05-05

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트

> 1. **본질**: [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) ([Representational State Transfer](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)) 성숙도 모델의 Level 0은 웹 자원 모델을 쓰지 않고, 하나의 엔드포인트에 작업 지시를 담아 보내는 [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/)) over [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 형태다.
> 2. **가치**: 구조는 단순해 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구현이 빠를 수 있지만, URI (Uniform Resource [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)), [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([HyperText Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) 메서드, 상태 코드가 제공하는 표준 의미를 거의 활용하지 못한다.
> 3. **판단 포인트**: 내부 연동용 명령 채널로는 쓸 수 있어도, 이를 [RESTful API](/knowledge-base/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))라고 부르면 캐시·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링·문서화·확장성 판단이 흐려진다. 정확한 명명과 진화 계획이 중요하다.

---

## Ⅰ. 개요 및 필요성

Level 0은 리처드슨 성숙도 모델 ([Richardson Maturity Model](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/157_restful_api_richardson_maturity_model/))에서 가장 낮은 단계로, HTTP를 자원 지향 웹 아키텍처가 아니라 단순 전송 통로로 사용하는 상태를 말한다. 클라이언트는 보통 하나의 URI로 `POST` 요청을 보내고, 실제로 수행할 작업은 본문 안의 `action`, `method`, `command` 같은 필드로 지정한다.

이 방식이 등장한 배경은 이해하기 어렵지 않다. 기존 [SOAP](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/153_soap_simple_object_access_protocol/) ([Simple Object Access Protocol](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/153_soap_simple_object_access_protocol/)), XML-[RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) (XML [Remote Procedure Call](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/)), 사내 원격 호출 시스템은 "함수를 호출한다"는 사고방식에 익숙했고, HTTP는 그 함수를 인터넷으로 전달하는 터널 역할을 했다. 그래서 URI는 단순 접속점이 되고, 요청 바디가 사실상의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 된다.

문제는 이 구조가 REST의 핵심인 "자원 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)"과 "표준 행위 의미"를 모두 놓친다는 점이다. 겉으로는 웹 API처럼 보여도, 실제로는 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)을 웹 위에 실은 형태이기 때문에 REST가 제공하는 장점을 거의 가져오지 못한다.

- **📢 섹션 요약 비유**: Level 0은 시청 민원 업무를 창구별로 나누지 않고, 건물 입구 우편함 하나에 모든 신청서를 던져 넣게 하는 방식과 같다. 전달은 되지만 구조가 보이지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Level 0의 구조는 단순하다. 하나의 URI가 모든 요청의 진입점이 되고, 대부분 `POST`만 사용한다. 요청의 의미는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메서드나 URI가 아니라 본문 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 결정한다. 서버는 본문 안의 작업 이름을 해석해 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메서드로 분기한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Level 0 request pattern</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">POST /api</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ action: cancel, id: 123 }</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Server router</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if action == "cancelOrder" -&gt; service.cancel()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if action == "createOrder" -&gt; service.create()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if action == "getOrder" -&gt; service.find()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">URI and HTTP method do not reveal resource semantics</div></div>
</div>
</div>



이 그림의 핵심은 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 의미가 외부 표준이 아니라 내부 분기 규칙에 숨어 있다는 점이다. 클라이언트와 서버는 문서나 사전 합의 없이는 서로의 요청 의미를 알기 어렵고, [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)·캐시·관측 도구도 요청 의도를 해석하기 힘들다. 즉 HTTP는 운반 수단일 뿐, 아키텍처적 의미는 거의 쓰지 않는다.

| 요소 | Level 0에서의 사용 방식 | 결과 |
| :--- | :--- | :--- |
| URI | 단일 엔드포인트 | 자원 경계가 드러나지 않음 |
| [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메서드 | 대부분 POST 하나 | 행위 의미와 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 구분이 흐려짐 |
| 상태 코드 | 종종 200 중심 사용 | 오류 유형을 표준적으로 전달하기 어려움 |
| 요청 본문 | 액션과 파라미터를 모두 포함 | 문서 의존성과 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 증가 |

이 구조가 항상 틀린 것은 아니다. 하지만 중요한 점은 이것이 REST라기보다 <strong>HTTP를 전송 채널로 쓴 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/">RPC</a> 스타일</strong>이라는 사실이다. 설계 성격을 정확히 이해해야 다음 단계로의 개선도 가능하다.

- **📢 섹션 요약 비유**: Level 0은 건물 내부 안내판 없이, 접수 직원이 종이 내용만 읽고 어느 부서로 보낼지 수동으로 판단하는 방식과 같다. 돌아는 가지만 체계적이지 않다.

---

## Ⅲ. 비교 및 연결

Level 0을 보면 Level 1과 Level 2의 가치가 선명해진다. Level 1은 자원을 URI로 분리해 "무엇을 다루는가"를 외부에 드러내고, Level 2는 `GET`, `POST`, `PUT`, `DELETE`와 상태 코드를 활용해 "어떻게 다루는가"를 표준화한다. Level 0은 이 두 축이 모두 약하기 때문에, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 외형은 있어도 웹의 공용 언어를 거의 쓰지 못한다.

| 항목 | Level 0 | Level 1 | Level 2 |
| :--- | :--- | :--- | :--- |
| URI 역할 | 단일 진입점 | 자원별 분리 | 자원별 분리 |
| 메서드 활용 | POST 중심 | 제한적 | GET/POST/PUT/DELETE 분리 |
| 캐시 활용 | 어려움 | 제한적 | GET 기반 활용 가능 |
| 장애 관측 | 바디 해석 필요 | 일부 개선 | 상태 코드 기반 자동화 용이 |

SOAP나 전통 RPC와도 비교가 된다. SOAP는 더 엄격한 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 규격과 계약 기반 설계를 제공하지만, 사고방식 자체는 "원격 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)"에 가깝다. Level 0도 마찬가지로 웹 자원보다 작업 호출에 초점을 두며, 이 때문에 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, 캐시, 문서화, 브라우저 친화성 측면에서 RESTful 설계보다 불리하다.

즉 Level 0의 문제는 단순히 "멋이 없다"가 아니다. 표준 도구 생태계가 이해할 수 있는 정보를 URI와 메서드에 실어 보내지 않으므로, 웹 인프라 전체와의 결합 효과를 잃는다.

- **📢 섹션 요약 비유**: Level 0이 모든 손님을 같은 번호표 창구로 보내는 방식이라면, Level 1과 Level 2는 업무별 창구와 이용 규칙을 외부에 보이게 적어 둔 시스템이다. 운영 효율 차이가 커질 수밖에 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Level 0 스타일이 아직도 적지 않게 남아 있다. 레거시 통합 시스템, 내부 명령 처리 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 게이트웨이, 빠른 사내 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/)에서는 구현 속도 때문에 단일 엔드포인트 구조를 택하기도 한다. 이 경우 중요한 것은 "이 API는 REST가 아니라 [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) 스타일"이라고 명확히 인식하는 것이다.

외부 공개 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 파트너 연동 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 장기 운영 API라면 Level 0에 머무르는 비용이 점점 커진다. 캐시 활용이 어렵고, 요청 의도가 URI에 드러나지 않으며, 관측 도구가 상태 코드를 통해 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하기도 힘들다. 따라서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수명과 소비자 수가 커질수록 자원 URI 분리와 메서드 정렬, 상태 코드 정비가 필요하다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이 인터페이스가 단기 내부 호출용인지, 장기 공개 API인지 구분했는가?
2. 요청 의미가 바디의 `action` 없이도 URI와 메서드로 드러나는가?
3. 오류와 성공을 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 상태 코드만으로도 1차 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)할 수 있는가?
4. 이후 Level 1 또는 Level 2로 진화할 경로를 고려했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- `POST /api` 하나만 쓰면서 이를 RESTful API라고 홍보하는 것
- 모든 오류를 `200 OK`로 내리고 바디 문자열로만 구분하는 것
- 자원 URI를 도입했지만 실제 작업은 여전히 `action` 필드에 숨겨 두는 것

- **📢 섹션 요약 비유**: Level 0을 실무에 쓰는 일은 임시 통로를 놓는 것까지는 괜찮지만, 그 통로를 영구 고속도로라고 우기면 운영과 확장에 계속 빚이 쌓이는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Level 0의 장점은 단순성이다. 빠르게 만들 수 있고, 기존 [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) 사고방식을 거의 그대로 가져올 수 있다. 하지만 이 장점은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 개발 단계에서만 크게 보이는 경우가 많고, 시간이 지날수록 URI 설계 부재, 상태 코드 활용 부족, 캐시·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 비효율, 문서 의존성 증가가 비용으로 돌아온다.

따라서 Level 0은 REST의 시작점이라기보다, "아직 HTTP를 웹 아키텍처로 쓰지 못한 상태"로 보는 것이 정확하다. 내부 시스템의 명령 채널로 한정하면 실용적일 수 있지만, 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 설계의 종착점으로 삼기에는 한계가 명확하다.

결론적으로 Level 0은 나쁜 기술이라기보다 <strong>정체를 정확히 불러야 하는 설계</strong>다. 이것을 REST라고 부르는 순간 문제 진단이 흐려지고, RPC라고 인정하는 순간 개선 방향이 선명해진다.

- **📢 섹션 요약 비유**: Level 0은 임시 행사장에서 쓰는 종합 안내 데스크와 같다. 하루 운영에는 편할 수 있지만, 상설 시청 민원 시스템으로는 창구 체계를 다시 갖춰야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/)) | Level 0의 설계 사고방식 |
| [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) | Level 0이 아직 충분히 활용하지 못한 상위 [아키텍처 스타일](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/114_architecture_style/) |
| URI | Level 1부터 자원 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 의미가 살아남 |
| [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메서드 | Level 2에서 행위 의미가 본격 활용됨 |
| 상태 코드 | 웹 인프라와 자동화 관측의 핵심 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SOAP / XML-RPC style</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Level 0</div>
<div class="kb-diagram-note">(single URI + POST + action in body)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Level 1</div>
<div class="kb-diagram-note">(resource-specific URI)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Level 2</div>
<div class="kb-diagram-note">(HTTP verbs + status codes)</div>
</div>
</div>



이 흐름도는 성숙도 상승이 단순 미관 개선이 아니라, 요청 의미를 점점 더 웹 표준 바깥에서 안쪽으로 끌어오는 과정임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Level 0은 모든 부탁을 같은 우체통에 넣고, 종이 안에 "이거 해 주세요"라고 적는 방식이에요.
2. 그래서 우체통만 봐서는 숙제를 낸 건지, 책을 빌린 건지 알 수 없어요.
3. 더 좋은 단계로 가면 창구 이름과 규칙이 밖에서도 보여서, 누구나 더 쉽게 이해할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 482

← **이전**: [157. RESTful API 성숙도 모델 (Richardson Maturity Model)](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/157_restful_api_richardson_maturity_model/)
**다음**: [159. Level 1 - 리소스별 고유 URI 할당](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/159_rest_level_1_resources/) →

---
