+++
weight = 681
title = "681. SSL/TLS (Secure Socket Layer / Transport Layer Security) 통신 모델 개요"
date = "2026-05-08"
[extra]
categories = "studynote-network"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 [[1117_network_security_zero_trust_policy|네트워크 보안]] 기본에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요를 이해하면 [[002_confidentiality|기밀성]]과 [[003_integrity|무결성]] 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 컴퓨터 네트워크에서 두 응용 프로그램(예: 내 웹 브라우저와 네이버 서버)이 서로 **[[001_dikw_pyramid|데이터]]를 안전하게 주고받을 수 있도록 [[002_confidentiality|기밀성]], [[003_integrity|무결성]], [[303_authentication_authorization_patterns|인증]]을 제공하는 4계층(전송 계층) 위의 암호화 [[295_protocol_field_tcp_udp_icmp|프로토콜]]**입니다.
- **역사**: 
  - 1995년 넷스케이프(Netscape) [[312_saga_pattern_choreography_orchestration|사가]] **SSL (Secure [[125_socket|Socket]] Layer)**이라는 이름으로 처음 세상에 내놓았습니다.
  - 이후 [[635_ietf_core_working_group_coap|IETF]](국제 표준화 기구)가 이 훌륭한 기술을 공식 표준으로 채택하면서, 이름을 **[[694_thread_local_storage_tls|TLS]] (Transport Layer [[283_security_tactics|Security]])**로 바꾸었습니다. (현재는 SSL 3.0의 후속 버전인 [[694_thread_local_storage_tls|TLS]] 1.2, [[694_thread_local_storage_tls|TLS]] 1.3을 쓰지만, 관습적으로 SSL/TLS라고 혼용해서 부릅니다.)

```text
[OCSP Stapling]
    │
    ▼
[SSL/TLS 통신 모델 개요]
    │
    └──▶ [TLS Handshake 프로토콜]
```

- **📢 섹션 요약 비유**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

통신 과정에서 다음 3가지 보안 기능을 완벽하게 묶어서(Suite) 제공합니다.

1. **[[002_confidentiality|기밀성]] ([[002_confidentiality|Confidentiality]])**: 오직 통신하는 둘만 아는 대칭키([[656_aes_advanced_encryption_standard_rijndael|AES]], ChaCha20)로 모든 [[001_dikw_pyramid|데이터]]를 암호화하여 중간에 해커가 가로채도 쓰레기 값만 보이게 만듭니다.
2. **[[003_integrity|무결성]] ([[003_integrity|Integrity]])**: 패킷 끝에 메시지 [[303_authentication_authorization_patterns|인증]] 코드([[674_hmac_hash_based_mac_ipsec|HMAC]], [[659_gcm_galois_counter_mode_aead|GCM]])를 달아서 전송 중 [[001_dikw_pyramid|데이터]]가 1비트라도 조작(변조)되지 않았음을 보증합니다.
3. **[[303_authentication_authorization_patterns|인증]] ([[604_authentication_factors|Authentication]])**: 통신하는 상대방이 해커가 만든 가짜 [[752_phishing|피싱]] 사이트가 아니라 '진짜 네이버 서버'가 맞는지, 국가 공인 **디지털 [[303_authentication_authorization_patterns|인증]]서(X.509, [[159_pki_public_key_infrastructure|PKI]])**를 통해 신원을 100% [[396_validation|확인]]합니다.

```text
[OCSP Stapling]
    │
    ▼
[SSL/TLS 통신 모델 개요]
    │
    └──▶ [TLS Handshake 프로토콜]
```

- **📢 섹션 요약 비유**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- TLS는 OSI 7계층 중 **전송 계층([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 4계층)과 응용 계층([[461_http_stateless_connection_oriented|HTTP]] 7계층) 사이에 살짝 끼어들어가는 '보안 껍데기' 역할**을 합니다.
- [[461_http_stateless_connection_oriented|HTTP]] [[001_dikw_pyramid|데이터]]가 TCP로 넘어가기 직전에, TLS가 그 [[001_dikw_pyramid|데이터]]를 낚아채어 암호화([[656_aes_advanced_encryption_standard_rijndael|AES]])하고 [[003_integrity|무결성]] 도장([[673_mac_message_authentication_code|MAC]])을 찍은 뒤 TCP로 넘깁니다. 
- 이렇게 HTTP와 TLS가 결합된 통신을 **[[471_https_http_over_tls|HTTPS]] ([[471_https_http_over_tls|HTTP over TLS]], [[446_port_and_bus|포트]] 443)**라고 부릅니다. (FTP에 붙으면 [[486_ftps_ftp_over_ssl_tls|FTPS]], SMTP에 붙으면 SMTPS가 됩니다.)

SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[679_ocsp_online_certificate_status_protocol|OCSP]] Stapling가 기반 조건을 만든다면, SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 그 위에서 핵심 메커니즘을 구현하고, [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [[002_confidentiality|기밀성]]과 [[003_integrity|무결성]]에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[679_ocsp_online_certificate_status_protocol|OCSP]] Stapling의 기반 정리 | SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요의 핵심 동작 | [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [[002_confidentiality|기밀성]] 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[694_thread_local_storage_tls|TLS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 겉보기엔 하나지만, 내부적으로는 '협상팀'과 '포장팀' 두 개로 나뉘어 동작합니다.
1. **협상팀 (Handshake, Alert, Change Cipher Spec)**: 
   - 진짜 통신([[001_dikw_pyramid|데이터]] 전송)을 시작하기 전에, 먼저 둘이 만나서 인사를 나누고(Handshake), 각자 신분증([[303_authentication_authorization_patterns|인증]]서)을 검사한 뒤, 앞으로 [[001_dikw_pyramid|데이터]]를 잠글 **'비밀 열쇠(대칭키)'를 해커 몰래 나눠 가지는(키 교환) 가장 중요하고 복잡한 사전 작업**을 수행합니다. (다음 682번 문서에서 상세히 다룸)
2. **포장팀 (Record [[295_protocol_field_tcp_udp_icmp|Protocol]])**: 
   - 협상팀이 비밀 열쇠를 주고 떠나면, 포장팀이 나서서 실제 [[461_http_stateless_connection_oriented|HTTP]] [[001_dikw_pyramid|데이터]] 덩어리를 썰고, 그 열쇠로 암호화하고, [[673_mac_message_authentication_code|MAC]] 꼬리표를 딱딱 붙여서 TCP로 내려보내는 '단순 노동(암호화 전송)'을 전담합니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 인터넷 세상에서 편지([[001_dikw_pyramid|데이터]])를 보낼 때, 그냥 보내면 우체부나 중간 배달부(해커)가 다 읽어볼 수 있습니다. TLS는 편지를 보내기 전, 먼저 수신자와 투명한 유리방(핸드셰이크)에서 만나 각자의 신분증([[303_authentication_authorization_patterns|인증]]서)을 [[396_validation|확인]]하고 서로만 아는 금고 비밀번호([[140_session_key|세션 키]])를 몰래 정하는 협상 과정입니다. 협상이 끝나면, 앞으로 보내는 모든 편지는 그 비밀번호로 열리는 튼튼한 티타늄 금고(레코드 [[295_protocol_field_tcp_udp_icmp|프로토콜]])에 담겨 배송되므로 절대 안전합니다.

---

## Ⅴ. 기대효과 및 결론

SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 [[1117_network_security_zero_trust_policy|네트워크 보안]] 기본을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [[002_confidentiality|기밀성]] 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]], 자동화된 신뢰 체계, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 자동화된 신뢰 체계 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[680_ocsp_stapling_tls_handshake_performance|OCSP Stapling]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[303_authentication_authorization_patterns|인증]] ([[604_authentication_factors|Authentication]]) | 통신 상대가 진짜인지 [[396_validation|확인]]한다. |
| 암호화 (Encryption) | [[001_dikw_pyramid|데이터]]를 읽지 못하게 보호한다. |
| [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: OCSP Stapling]
    │
    ▼
[현재 개념: SSL/TLS 통신 모델 개요]
    │
    ├──▶ [확장 A: TLS Handshake 프로토콜]
    └──▶ [확장 B: 자동화된 신뢰 체계]
```

SSL/[[694_thread_local_storage_tls|TLS]] 통신 모델 개요는 [[679_ocsp_online_certificate_status_protocol|OCSP]] Stapling에서 출발해 현재 메커니즘을 정교화하고, 이후 [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]]와 자동화된 신뢰 체계 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비밀 편지를 보낼 때는 자물쇠와 비밀번호가 필요해요.
2. 이 개념은 누가 진짜 친구인지 [[396_validation|확인]]하고, 편지가 바뀌지 않았는지도 살펴봐요.
3. 그래서 나쁜 사람이 중간에 훔쳐보거나 바꾸기 어려워져요.
