---
title: "215. Window Size Sender Receiver"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

슬라이딩 윈도우는 송신자 혼자 치는 장난이 아닙니다. 수신자 쪽에도 똑같은 돋보기 틀(버퍼 메모리)이 존재합니다.

1. **송신 윈도우 (Sender Window, $W_s$)**:
   - "내가 지금부터 ACK를 받지 않고도 연달아 쏠 수 있는 프레임의 최대 한도(개수)"입니다.
   - 송신 윈도우가 10이면, 1번부터 10번까지의 총알을 한 방에 장전하고 기관총처럼 쏠 수 있습니다.
2. **수신 윈도우 (Receiver Window, $W_r$)**:
   - "내가 순서가 뒤죽박죽으로 들어오더라도, 버리지 않고 임시로 내 메모리(버퍼)에 저장해 둘 수 있는 빈 공간의 크기"입니다.
   - 수신 윈도우가 1이면, 오직 순서에 딱 맞는 1개만 받아먹고 나머지는 다 버립니다(옹졸함). 수신 윈도우가 10이면, 10개가 섞여 들어와도 일단 뱃속에 다 품어줍니다(관대함).

```text
[슬라이딩 윈도우 프로토콜 개념]
    |
    v
[윈도우 크기, 송신/수신 윈도우]
    |
    +---> [HDLC]
```

- **📢 섹션 요약 비유**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

앞서 배운 3가지 [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) 방식은 이 두 윈도우의 크기(세팅 값)만 다를 뿐, 본질적으로 모두 슬라이딩 윈도우의 변형입니다.

| [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 송신 윈도우 ($W_s$) | 수신 윈도우 ($W_r$) | 특징 |
| :--- | :---: | :---: | :--- |
| **정지-대기 (Stop-and-Wait)** | **1** | **1** | 1개 쏘고, 1개 받음. 제일 멍청하지만 가장 안전. |
| **Go-Back-N (GBN)** | **$N$** (여러 개) | **1** | 기관총처럼 쏘지만, 수신기는 까탈스러워서 순서 어긋나면 다 버림. (연대 책임 재전송). |
| **Selective Repeat (SR)** | **$N$** (여러 개) | **$N$** (여러 개) | 쏘기도 많이 쏘고, 수신기도 넓은 아량으로 다 받아줌. 에러 난 것만 쏙 다시 받음. (가장 똑똑하고 복잡함). |

```text
[슬라이딩 윈도우 프로토콜 개념]
    |
    v
[윈도우 크기, 송신/수신 윈도우]
    |
    +---> [HDLC]
```

- **📢 섹션 요약 비유**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

프레임을 구별하기 위해 헤더에 0, 1, 2, 3.. 이라는 '순서 번호(Sequence Number)'를 붙입니다.
만약 헤더의 순서 번호 공간이 <strong>m비트</strong>라면, 우리가 쓸 수 있는 번호는 총 **$2^m$개** ($0$부터 $2^m - 1$까지)입니다. (예: 3비트면 0~7번까지 총 8개 번호를 돌려 씁니다).

이때 **SR(Selective Repeat)** 방식에서 윈도우 사이즈를 욕심부려 전체 번호 개수(8칸)만큼 다 늘려버리면 치명적인 버그가 터집니다.
- 1차 전송: 송신기가 0~7번을 다 쐈습니다. 수신기도 다 받아서 ACK 0(새로운 0번 내놔)을 쳤는데 이 ACK가 날아갔습니다.
- 2차 전송: 송신기는 타임아웃이 걸려 아까 그 <strong>'옛날 0~7번'</strong>을 다시 쏩니다.
- 수신기의 착각: 수신기는 방금 자기가 0~7을 다 비우고 윈도우를 전진시켰기 때문에, 날아온 이 옛날 0번을 <strong>'새로운 2회차의 0번 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>'로 착각하고 낼름 받아버립니다.</strong> ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복의 대재앙).

**[ 절대 룰 ]**
- GBN의 최대 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/): **$2^m - 1$** (전체 번호보다 무조건 1개는 작아야 함).
- SR의 최대 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/): **$2^{m-1}$** (전체 번호의 **정확히 절반(1/2)** 이하여야 앞뒤 번호가 겹치지 않고 안전함).

[윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념이 기반 조건을 만든다면, [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 그 위에서 핵심 메커니즘을 구현하고, HDLC는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 오류율과 재전송 비용에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념의 기반 정리 | [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우의 핵심 동작 | HDLC의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 오류율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: <strong> 송신 윈도우는 <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 머신이 한 번에 날릴 수 있는 </strong>'야구공의 묶음 수'**이고, 수신 윈도우는 포수가 들고 있는 **'포수 미트의 크기'**입니다. 포수 미트가 1개(GBN)면 공이 5개가 날아올 때 1개만 잡고 나머진 다 얼굴에 맞아 튕겨 나가지만, 미트가 5개(SR)면 5개의 공을 한 번에 다 잡아서 주머니에 차곡차곡 모아둘 수 있는 여유가 생깁니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념 수준의 기본 대책으로 충분한지, 아니면 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 HDLC와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 오류율 부족인지, 재전송 비용 악화인지 먼저 분리한다.
2. [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 HDLC와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 오류율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/), 고신뢰 저지연 링크 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) | 비트열을 의미 있는 전송 단위로 구분한다. |
| [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) ([Error Control](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)) | 검출과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계해야 한다. |
| [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 슬라이딩 윈도우 프로토콜 개념]
    |
    v
[현재 개념: 윈도우 크기, 송신/수신 윈도우]
    |
    +---> [확장 A: HDLC]
    +---> [확장 B: 고신뢰 저지연 링크 제어]
```

[윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/), 송신/수신 윈도우는 [슬라이딩 윈도우 프로토콜](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/) 개념에서 출발해 현재 메커니즘을 정교화하고, 이후 HDLC와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 336 / 1120

<- **이전**: [214. 슬라이딩 윈도우 프로토콜 (Sliding Window Protocol) 개념](/studynote/03_network/04_data_link_layer_error/214_sliding_window_protocol/)
**다음**: [216. HDLC (High-Level Data Link Control)](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) ->

---
