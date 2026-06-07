---
title: "973. Http2 Multiplexing Binary Framing Hpack Push"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 973
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱을 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **1 커넥션 = 1 요청 원칙**: 브라우저가 서버와 랜선([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 커넥션) 하나를 뚫으면 한 번에 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개만 요청하고 받았습니다.
- 너무 느려서 브라우저는 꼼수로 **동시 커넥션을 6개** 뚫어서 사진 6개를 동시에 받았지만, 컴퓨터 자원이 엄청 깨졌습니다.
- **파이프라이닝 실패**: 1개의 선에서 사진 10개를 릴레이로 요청했지만, 서버는 무조건 순서대로 응답해야 했습니다. 1번 사진이 용량이 커서 10초가 걸리면, 2~10번 사진은 멀쩡히 준비됐는데도 출발을 못 하고 갇히는 <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> <a href="/studynote/03_network/19_frequent_topics_terms/971_hol_blocking_head_of_line_tcp_http_delay/">HOL Blocking</a> (971번 문서)</strong> 지옥이 터졌습니다.

```text
[QUIC]
    |
    v
[HTTP/2 멀티플렉싱]
    |
    +---> [RESTful API]
```

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

구글 SPDY 프로젝트를 기반으로 2015년 표준화된 혁명입니다.

### 1. 텍스트 버리고 바이너리로 (Binary [Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) Layer)
- 옛날엔 데이터와 헤더(주소)를 텍스트 글자로 보냈습니다.
- [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 데이터를 컴퓨터가 제일 빨리 읽는 0과 1의 **바이너리 레고 블록(프레임)** 단위로 무자비하게 쪼개버립니다([프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)).

### 2. 멀티플렉싱 ([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) - "섞어 찌개 전송" 🌟 핵심 🌟
- **개념**: 단 <strong>1개의 <a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> 커넥션(1차선 도로)</strong>만 뚫어놓고, 수백 개의 사진과 텍스트를 무작위로 섞어서([다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 한꺼번에 쏟아버리는 기술입니다.
- **동작**:
  - 서버는 1번 사진 조각, 2번 사진 조각, 3번 사진 조각을 뒤죽박죽 섞어서 막 던집니다.
  - 1번 사진을 렌더링하다 딜레이가 걸려도, 2번 3번 사진 조각은 1번을 기다리지 않고 옆으로 추월해서 쌩쌩 날아가 폰 화면에 먼저 뜹니다([HOL](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹 완벽 타파).
  - 브라우저는 섞여 들어온 블록에 적힌 '스트림 번호표(ID)'를 보고 자기들끼리 퍼즐처럼 100% 깔끔하게 재조립합니다.

```text
[QUIC]
    |
    v
[HTTP/2 멀티플렉싱]
    |
    +---> [RESTful API]
```

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 1. 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) (HPACK)
- [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 매번 요청할 때마다 무거운 헤더([쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/), 브라우저 정보 등 1KB)를 똑같이 반복해서 보냈습니다.
- [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 "야! 아까 보낸 헤더랑 똑같지? 그럼 바뀐 글자 하나만 보내!(델타 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/))" 라며 중복되는 헤더를 10바이트 수준으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 버리는 <strong>HPACK <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>을 써서 트래픽 낭비를 0%로 만들었습니다.

### 2. 서버 푸시 ([Server Push](/studynote/03_network/09_application_layer_web_email/469_http2_server_push/))
- 옛날엔 브라우저가 "HTML 줘" ➜ (받음) ➜ "오 HTML 까보니까 [CSS](/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 필요하네? [CSS](/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/) 줘!" (왕복 2번)
- [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 서버의 선빵: "야, 너 HTML 달라고? 내가 볼 때 너 이거 받으면 무조건 CSS랑 이미지 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)도 필요할걸? 네가 달라고 안 했지만 걍 덤으로 묶어서 미리 쏴버릴게!(서버 푸시)" 브라우저가 뒤늦게 요청할 시간을 미리 앞당겨 절약하는 마법입니다.

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. QUIC가 기반 조건을 만든다면, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 그 위에서 핵심 메커니즘을 구현하고, RESTful API는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 구분 명확성과 설명력에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | QUIC의 기반 정리 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱의 핵심 동작 | RESTful API의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 구분 명확성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2가 웹 계층의 [HOL](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹은 다 해결했지만, 그 밑에 깔린 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 자체가 가진 <strong><a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> <a href="/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">HOL</a> 블로킹(패킷 유실 시 전체 대기)</strong>은 극복하지 못했습니다. 결국 이 마지막 한계를 부수기 위해 탄생한 것이 972번 문서의 <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3 (<a href="/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/">QUIC</a>)</strong>입니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 구형 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 '꽉 막힌 은행 창구 1개'입니다. 내 앞사람이 대출 심사(용량 큰 사진)를 받느라 30분을 허비하면, 뒤에서 동전 하나 바꾸려는 사람(용량 작은 텍스트)도 꼼짝없이 30분을 기다려야 합니다([HOL](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹). 그래서 창구를 6개(멀티 커넥션) 열었지만 알바생 인건비가 터졌습니다. <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2 멀티플렉싱</strong>은 '천재적인 회전초밥 컨베이어 벨트'입니다. 주방장(서버)은 손님이 주문한 음식 10개를 1개씩 순서대로 내보내지 않습니다. 조리된 순서도 무시하고, 계란초밥 접시, 연어초밥 접시를 컨베이어 벨트 1개(단일 커넥션) 위에 마구잡이로 섞어서 한 번에 미친 듯이 쏟아냅니다. 장어초밥을 굽느라 늦어져도([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)), 이미 만들어진 계란초밥은 병목없이 손님 입(브라우저)으로 쌩쌩 굴러갑니다. 손님은 접시에 적힌 자기 이름표(스트림 ID)만 보고 쏙쏙 뽑아 먹어 웹페이지가 1초 만에 풀 로딩되는 혁명적 동시 처리 시스템입니다.

---

## Ⅴ. 기대효과 및 결론

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 빈출 주제와 용어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 구분 명확성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [RESTful API](/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/), [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [QUIC](/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [RESTful API](/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: QUIC]
    |
    v
[현재 개념: HTTP/2 멀티플렉싱]
    |
    +---> [확장 A: RESTful API]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 멀티플렉싱는 QUIC에서 출발해 현재 메커니즘을 정교화하고, 이후 RESTful API와 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비슷한 이름의 장난감을 헷갈리지 않게 표를 붙이는 것과 같아요.
2. 이 개념은 무엇이 어떻게 다른지 쉽게 구별하게 도와줘요.
3. 그래서 시험에서도 실무에서도 말을 더 정확하게 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1094 / 1120

<- **이전**: [972. QUIC (0-RTT 핸드셰이크)](/studynote/03_network/19_frequent_topics_terms/972_quic_0_rtt_handshake_http3_udp_multiplexing/)
**다음**: [974. RESTful API](/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/) ->

---
