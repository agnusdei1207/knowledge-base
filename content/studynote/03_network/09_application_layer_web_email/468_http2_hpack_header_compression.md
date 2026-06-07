---
title: "HPACK"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 468
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)은 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 이해하면 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 헤더의 비만증 (Pain Point)
현대의 웹 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나를 열려면 이미지, [CSS](/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/) 등 100개가 넘는 자원을 요청해야 합니다.
- **문제 발생**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 상태를 기억하지 않으므로, 100번의 요청마다 똑같은 `User-Agent: Mozilla/5.0...`과 수 KB에 달하는 거대한 `Cookie` 문자열을 매번 헤더에 붙여서 보냈습니다.
- 정작 요청하는 본문(Body) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 10바이트인데, 헤더(Header) 텍스트가 2,000바이트가 넘는 <strong>배보다 배꼽이 큰 <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 비대화 현상</strong>이 발생했습니다. 텍스트 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)(Gzip)은 본문(Body)에만 적용되고 헤더에는 적용되지 않아, 모바일 네트워크의 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 심각하게 낭비했습니다.

### 2. HPACK의 등장: "한 번 한 말은 번호표로 대신하자!"
구글의 엔지니어들은 이 낭비를 막기 위해 SPDY에서 쓰던 Gzip 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 버리고(보안 취약점 때문), [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 전용 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 알고리즘인 <strong>HPACK</strong>을 발명했습니다.
- **필요성**: 브라우저와 서버 양쪽에 똑같은 '메모장(Table)'을 펼쳐놓고, 처음에 `User-Agent: Chrome`을 보내면 메모장 62번에 적어둡니다. 두 번째 요청부터는 긴 글씨 대신 "아까 메모장 62번 줘!"라는 숫자 1개만 보내어 수천 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)의 텍스트를 1바이트로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 혁명을 이뤄냈습니다.

```text
[HTTP/2 스트림 다중화]
    |
    v
[HTTP/2 헤더 압축]
    |
    +---> [HTTP/2 서버 푸시]
```

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 식당에 갈 때마다 종업원에게 "저는 알러지가 있고, 매운 걸 못 먹고, 밥은 적게 주시고..."를 매번 처음부터 끝까지 랩퍼처럼 읊어대는 피곤한 단골손님입니다. HPACK은 종업원이 손님의 식성을 장부에 '1번 메뉴얼'로 적어두고, 다음부터는 손님이 식당에 들어오며 손가락 1개만 펴도([인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 번호) 똑같은 밥상이 완벽하게 차려지는 VIP 회원 관리 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

HPACK 아키텍처는 3가지 강력한 수학적/논리적 무기로 구성됩니다.

```text
+-------------------------------------------------------------+
|             [ HTTP/2 HPACK 알고리즘 3대 핵심 아키텍처 ]            |
|                                                             |
|   [ 1. 정적 테이블 (Static Table) ] - 영원히 변하지 않는 규칙        |
|    -> 전 세계 모든 브라우저와 서버가 공유하는 61개의 고정 딕셔너리      |
|       - 인덱스 2번: `method: GET`                             |
|       - 인덱스 8번: `status: 200`                             |
|                                                             |
|   [ 2. 동적 테이블 (Dynamic Table) ] - 통신하면서 실시간 기록        |
|    -> 클라이언트와 서버가 연결된(TCP) 동안 유지되는 메모장             |
|       - 인덱스 62번: `Cookie: session_id=ABC123XYZ...`        |
|       - 인덱스 63번: `Custom-Header: my-app-v1`               |
|                                                             |
|   [ 3. 허프만 코딩 (Huffman Coding) ] - 텍스트 자체의 픽셀 압축       |
|    -> 테이블에 없는 완전 새로운 헤더 글자를 보낼 때 사용               |
|    -> 자주 쓰이는 알파벳(e, a)은 5비트로, 안 쓰이는 글자(z, q)는 10비트|
|       로 가변 압축하여 전송 용량을 물리적으로 30% 추가 삭감           |
+-------------------------------------------------------------+
```

### 동작 메커니즘 (인덱싱 통신)
1. 브라우저가 첫 요청 시 `Cookie: abcd`를 보냅니다. 서버는 이를 받아 자신의 <strong>동적 테이블 62번</strong>에 저장합니다.
2. 두 번째 요청 시 브라우저는 거대한 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 텍스트 대신 `62`라는 바이너리 숫자 하나만 달랑 보냅니다.
3. 서버는 자신의 메모리에서 62번을 조회해 `Cookie: abcd`로 완벽하게 복원(Decompression)해 냅니다.

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 왜 Gzip을 안 쓰고 HPACK을 새로 만들었나? ([CRIME](/studynote/09_security/03_network_security/296_crime_attack/) 공격 방어)
[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 시절에도 SPDY는 헤더를 Gzip으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)했습니다. 하지만 <strong><a href="/studynote/09_security/03_network_security/296_crime_attack/">CRIME</a>(<a href="/studynote/08_algorithm_stats/09_info_theory/159_compression/">Compression</a> Ratio Info-leak Made Easy) 공격</strong>이라는 치명적 해킹이 발견되었습니다.
- **해킹 원리**: Gzip은 텍스트가 비슷하면 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)률이 높아집니다. 해커가 브라우저에 몰래 스크립트를 심어 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 값의 알파벳을 하나씩 무작위로 추측해서 보냅니다. 우연히 해커가 찌른 알파벳 1개가 진짜 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)와 일치하면, Gzip [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)률이 확 높아져 패킷 크기가 작아집니다. 해커는 이 패킷 크기의 변화만 보고 남의 [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 암호를 알아맞히는 암호학적 재앙이 터졌습니다.
- **해결책**: HPACK은 해커가 추측할 수 있는 Gzip 방식을 버리고, 단순히 번호표([인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))로 치환하거나 개별 문자열을 허프만 코딩으로 고정 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 버려 [CRIME](/studynote/09_security/03_network_security/296_crime_attack/) 공격을 수학적으로 원천 차단했습니다.

### ⚡ 치명적 트레이드오프: 상태 유지(Statefulness) 메모리 폭발
[REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 통신의 제1원칙은 "서버는 상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 저장하지 않는다([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))"였습니다. 그래야 서버 1대가 죽어도 옆 서버가 요청을 똑같이 처리할 수 있기 때문입니다.
- **트레이드오프**: HPACK은 이 대원칙을 박살 냈습니다. 동적 테이블은 철저하게 <strong>특정 <a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> 커넥션(특정 클라이언트)에 종속된 상태(<a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a>)</strong>입니다.
- 만약 아마존(AWS) 웹 서버에 100만 명의 사용자가 동시 접속하면, 서버는 100만 개의 각기 다른 '동적 테이블 메모장'을 RAM에 유지해야 합니다. 네트워크 트래픽([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 극적으로 아낀 대가로, <strong>서버의 RAM(메모리) 용량을 갈아 넣는 지독한 등가교환(Trade-off)</strong>이 발생한 것입니다.

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)가 기반 조건을 만든다면, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)은 그 위에서 핵심 메커니즘을 구현하고, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 서버 푸시는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)의 기반 정리 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 핵심 동작 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 서버 푸시의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: HPACK의 딜레마는 "전화 요금([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 아끼기 위해 통화 내용을 줄이는 대신, 콜센터 직원이 100만 명 고객의 모든 과거 통화 내역을 자기 머릿속(RAM)에 전부 암기하고 있어야 하는 가혹한 근무 환경"과 같습니다. 회선 비용은 줄어들지만, 직원의 머리(서버 메모리)는 터져나갈 위험이 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **도입 환경** | 기존 레거시 시스템과의 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 분석 | 마이그레이션 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 및 단계별 전환 계획 수립 |
| <strong>비용(<a href="/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a>)</strong> | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용(CAPEX) 및 운영 비용(OPEX) | [TCO](/studynote/12_it_management/01_governance_strategy/016_tco/) 관점의 장기적 효율성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **보안/위험** | 컴플라이언스 준수 및 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/studynote/05_database/07_exam_summary/442_consistency_integrity/) | [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 기반 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 체계 연계 |

*(추가 실무 적용 가이드 - L7 로드밸런서의 메모리 폭발 방어 아키텍처)*
- **실무 의사결정 (동적 테이블 크기 제어)**: 인프라 아키텍트가 Nginx나 AWS ALB(Application [Load Balancer](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/))에 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2를 활성화할 때, 반드시 설정해야 하는 파라미터가 `SETTINGS_HEADER_TABLE_SIZE` 입니다.
- 브라우저가 악의적으로 수만 개의 쓰레기 헤더를 뿜어내면, 서버의 동적 테이블이 무한정 커져서 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/studynote/02_operating_system/02_process_thread/157_oom_killer/))으로 서버가 다운되는 DDoS 공격을 맞게 됩니다. 아키텍트는 이 테이블의 최대 크기를 표준 권장치인 <strong>4KB(4096 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/">바이트</a>)</strong> 정도로 단호하게 제한(Limit)해야 합니다. 공간이 다 차면 오래된 헤더부터 지우는 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 방식으로 동작하게 하여, 서버의 물리적 RAM이 붕괴하는 것을 하드코딩으로 막아내야 합니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. "손님(브라우저)의 외상 장부(동적 테이블)를 끝없이 다 적어주다간 가게 장부가 찢어집니다. 훌륭한 사장님은 '한 사람당 외상은 딱 4천 원(4KB)까지만 기억한다!'는 철칙을 가게 문 앞에 붙여두어야 악성 진상 고객으로부터 식당을 지켜낼 수 있습니다."

---

## Ⅴ. 기대효과 및 결론

1. <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3의 QPACK 진화: <a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> <a href="/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">HOL</a> 블로킹 우회</strong>
   [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2의 HPACK은 치명적 약점이 있었습니다. 헤더 1번 패킷이 공중에서 유실(Loss)되면, 뒤따라오던 2번, 3번 패킷은 1번이 채워주어야 할 '동적 테이블'이 완성되지 않아서 디코딩을 못한 채 서버에서 대기해야 했습니다 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [HOL](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) Blocking의 연장선).
   - 이를 해결하기 위해 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3([QUIC](/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/))에서는 <strong>QPACK</strong>이라는 새로운 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 알고리즘으로 진화했습니다. QPACK은 헤더 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송하는 스트림과, 제어 명령을 전송하는 스트림을 물리적으로 완전히 분리하여, 1번 패킷이 유실되어도 2번 패킷이 다른 테이블 상태를 참조해 멈춤 없이 렌더링되게 만드는 비동기 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 궁극을 보여줍니다.

2. <strong>서버 푸시(<a href="/studynote/03_network/09_application_layer_web_email/469_http2_server_push/">Server Push</a>)와의 연계 하락</strong>
   과거 HPACK은 서버 푸시를 할 때, 서버가 브라우저 캐시에 없는 파일만 똑똑하게 골라 밀어 넣는(Cache Digest) 용도로도 융합되었습니다. 하지만 서버 푸시 자체가 브라우저 캐시와 충돌하는 부작용이 커지면서 최근 Chrome 등에서 지원을 중단하는 추세이며, HPACK은 순수하게 헤더 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 본연의 임무에만 집중하는 형태로 정제되고 있습니다.


## 🧠 지식 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

*   <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화 계층</strong>
    *   통신 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/): [Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) (바이너리 [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/))
    *   <strong><a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>: HPACK (<a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2), QPACK (<a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3)</strong>
*   **HPACK 3대 내부 메커니즘**
    *   Static Table (정적 테이블): 고정 딕셔너리 (61개)
    *   Dynamic Table (동적 테이블): [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 유지형 실시간 기록 (Stateful)
    *   [Huffman Coding](/studynote/08_algorithm_stats/05_string/100_huffman_coding/) (허프만 인코딩): 가변 길이 문자열 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)
*   **아키텍처 트레이드오프 및 보안**
    *   [CRIME](/studynote/09_security/03_network_security/296_crime_attack/)/BREACH 해킹 방어 (Gzip 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 암호학적 취약점 극복)
    *   서버 메모리 부하 (Stateful 연결 오버헤드 증가) 향후에는 지능형 애플리케이션 전달 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 역사는 "종이에 글을 써서 편지를 보내던 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 시대"에서 "서로가 암호표(HPACK)를 나눠 가지고 숫자만 부호로 날리는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2의 [스파이](/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/) 통신"으로 진화했고, 이제는 "암호표 한 장이 찢어져도 통신이 끊기지 않는 독립 무전기(QPACK)" 시대로 접어들며 인터넷의 군더더기 살점을 1g도 남기지 않고 도려내고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ([Session](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 서버 푸시 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: HTTP/2 스트림 다중화]
    |
    v
[현재 개념: HTTP/2 헤더 압축]
    |
    +---> [확장 A: HTTP/2 서버 푸시]
    +---> [확장 B: 지능형 애플리케이션 전달]
```

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 서버 푸시와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 마치 우리가 매일 사용하는 "스마트폰"과 같아요.
2. 복잡한 기계 장치들이 숨어 있지만, 우리는 화면만 터치하면 쉽게 원하는 것을 할 수 있죠.
3. 이처럼 보이지 않는 곳에서 시스템이 잘 돌아가도록 돕는 멋진 마법 같은 기술이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 589 / 1120

<- **이전**: [467. HTTP/2 스트림 (Stream) 다중화 (Multiplexing)](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)
**다음**: [469. HTTP/2 서버 푸시 (Server Push)](/studynote/03_network/09_application_layer_web_email/469_http2_server_push/) ->

---
