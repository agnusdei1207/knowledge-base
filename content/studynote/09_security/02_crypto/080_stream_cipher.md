---
title: "Stream Cipher - RC4, ChaCha20"
date: "2026-05-05"
tags:
  - "studynote-security"
weight: 80
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)([Stream Cipher](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 뭉텅이(Block)로 모아서 처리하는 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)와 달리, 평문 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물 흐르듯 연속적으로 들이부으며 <strong><a href="/studynote/01_computer_architecture/14_hardware_security_trends/486_trng/">난수 생성기</a>가 뽑아낸 '키 스트림(<a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> <a href="/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/">Stream</a>)'과 1비트(또는 1바이트) 단위로 실시간 XOR(배타적 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>합) 연산을 때려버리는 <a href="/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a> 암호화 아키텍처</strong>다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모을 때까지 기다릴 필요가 없어 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 사실상 '0'에 수렴하며, 복잡한 치환(S-box)이나 라운드 뺑뺑이 없이 [논리 게이트](/studynote/01_computer_architecture/01_basic_electronics_logic/027_logic_gates/) 하나(XOR)로 암호화와 복호화를 동시에 끝내버리므로 모바일 기기나 저전력 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경에서 극강의 가성비와 속도를 자랑한다.
> 3. **판단 포인트**: 엄청나게 빠르고 가볍지만, 동일한 암호키와 초기화 벡터([IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))를 두 번 재사용([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Reuse)하는 순간 두 암호문을 XOR 연산만 해도 원본 평문이 홀라당 벗겨지는 치명적인 수학적 태생의 약점을 가지므로 키 관리 거버넌스에 목숨을 걸어야 한다.

---

## Ⅰ. 개요 및 필요성

군대의 무전병이 실시간으로 "적진 100m 앞 도달"이라고 음성 무전을 치고 있다고 치자. 이 엄청나게 빠른 실시간 스트리밍 음성 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 128비트씩 뭉텅이(Block)로 모아서 암호화([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/))하려고 기다리면 무전에 렉(Lag)이 걸려 전투에서 진다.

아키텍트들은 "기다리지 말고, 평문이 1비트 들어오는 그 찰나의 순간에 마법의 난수([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)) 1비트를 섞어서 곧바로 내보내자!"라고 결단했다. 쇳덩어리(CPU) 입장에서 가장 싸고 빠른 연산은 두 개의 비트가 다르면 1, 같으면 0을 뱉는 <strong>XOR(배타적 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>합)</strong> 게이트다. 평문 `A`에 마법의 열쇠 `K`를 XOR하면 쓰레기 값 `C`가 되고, 목적지에서 그 쓰레기 값 `C`에 똑같은 열쇠 `K`를 다시 XOR하면 기적처럼 평문 `A`가 튀어나온다. 이 극도의 단순함과 빛의 속도가 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)가 와이파이([WEP](/studynote/03_network/11_wireless_mobile_communication/580_wep_wired_equivalent_privacy_rc4/), [WPA](/studynote/03_network/11_wireless_mobile_communication/581_wpa_tkip_802_1x_eap/))와 구글의 웹 브라우저([TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)/ChaCha20) 통신을 지배하게 만든 근원적 힘이다.

- **📢 섹션 요약 비유**: [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)가 컨베이어 벨트에 상자 100개(블록)가 다 찰 때까지 기다렸다가 한 번에 포장지를 씌우는 '도매상'이라면, [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 사탕이 파이프에서 하나씩 떨어질 때마다 레이저를 쏴서 실시간으로 껍질을 코팅해 버리는 광속의 '소매상'이다. 기다림([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/))이란 존재하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 키 스트림 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)기(PRNG)와 XOR의 완벽한 이중주
[스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)의 설계 철학은 "어떻게 하면 우주 끝까지 패턴이 반복되지 않는 진짜 같은 가짜 난수(Pseudo Random Number)를 무한대로 뿜어낼 것인가?"에 모든 것을 건다.

```text
+--------------------------------------------------------+
|           스트림 암호(Stream Cipher)의 초고속 XOR 파이프라인        |
+--------------------------------------------------------+
|                                                        |
|  [ 씨앗 (Seed Key + IV) ] ---> (해커가 절대 모르는 비밀 암호키)|
|            |                                           |
|            v                                           |
|  [ 난수 생성 공장 (PRNG / LFSR) ]                       |
|    - 알고리즘: "1011001110001011..." (끝없이 뿜어지는 키 스트림!)|
|            |                                           |
|            v      (XOR 연산: ⊕)                        |
|   평문(Data) ---> ⊕ ---> [ 암호문(Cipher Text) 실시간 전송! ]|
|   (10011010)            (00101001)                     |
|                                                        |
| * 핵심 논리: 암호화 기계와 복호화 기계는 '100% 똑같은 구조'다.   |
|   목적지에서도 똑같은 씨앗(Key)을 넣고 똑같은 난수 폭포를 뿜어내어|
|   암호문에 한 번 더 XOR(⊕)를 때리면 원래의 평문이 돌아온다.      |
+--------------------------------------------------------+
```

<strong><a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>(<a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">Synchronization</a>)의 절대 법칙</strong>: 송신자와 수신자의 난수 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 공장(PRNG)은 무조건 똑같은 타이밍에 똑같은 난수를 뱉어야 한다. 네트워크 전송 중에 중간에 1비트가 유실(소실)되어 박자가 어긋나버리면, 그 뒤에 오는 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 엉뚱한 난수와 섞여 영구적인 쓰레기가 되어버린다(에러 증식). 그래서 현대 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잘게 자른 뒤 초기화 벡터([IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)/[Nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/))를 계속 섞어주어 박자를 리셋한다.

- **📢 섹션 요약 비유**: [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 '송신자와 수신자의 싱크로나이즈드 수영([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))'이다. 두 선수가 똑같은 비밀 카세트테이프(키 스트림)를 들으며 물 밖과 물속에서 똑같은 동작(XOR)을 쳐내야 한다. 중간에 이어폰이 끊겨 한 선수가 1초라도 박자를 놓치면, 그 뒤의 모든 안무([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복호화)는 엉망진창으로 꼬여버려 완전히 망친다.

---

## Ⅲ. 비교 및 연결

### 1비트의 미학(스트림) vs 128비트의 파괴력(블록)
암호 아키텍트는 하드웨어(CPU) 환경에 맞춰 이 두 쇳덩어리를 취사선택한다.

| 비교 항목 | [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/) ([Stream Cipher](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)) | [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) ([Block Cipher](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)) |
|:---|:---|:---|
| **처리 단위** | <strong>1 <a href="/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">bit</a> 또는 1 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/">Byte</a> 단위 (물 흐르듯)</strong> | <strong>64 <a href="/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">bit</a>, 128 <a href="/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">bit</a> 덩어리 단위</strong> |
| **핵심 연산 구조**| [난수 생성기](/studynote/01_computer_architecture/14_hardware_security_trends/486_trng/)(PRNG) + 단일 XOR [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)합 | 10회 이상의 반복 치환(S-box)과 섞기(Permutation) |
| **속도 및 하드웨어**| **엄청나게 빠름. 회로 면적이 작고 가벼움** | 상대적으로 무겁고 전력을 더 먹음 ([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-NI 가속기 필요) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 변형 전파</strong>| 1비트 에러는 딱 1비트만 망가뜨림 (전파 안 됨) | **1비트만 바뀌어도 128비트 블록 전체가 폭발함 (눈사태)** |
| **치명적 약점** | <strong>같은 키(<a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a>) 두 번 쓰면 평문 100% 털림</strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 끝 빈 공간을 강제로 채워야 함 ([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 오라클 위협) |
| <strong>대표 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | <strong><a href="/studynote/09_security/02_crypto/081_rc4_stream_cipher/">RC4</a>(털려서 사망), ChaCha20(현재 대장)</strong> | [DES](/studynote/09_security/02_crypto/086_des_data_encryption_standard/)(사망), <strong><a href="/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/">AES</a>(현존 최강의 황제)</strong> |

과거엔 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)로 RC4가 와이파이([WEP](/studynote/03_network/11_wireless_mobile_communication/580_wep_wired_equivalent_privacy_rc4/))를 지배했으나 쇳덩어리 수학적 결함으로 박살이 났다. 하지만 스마트폰 시대에 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)) 연산조차 배터리를 갉아먹자, 구글(Google)은 모바일 환경에서 AES보다 3배나 빠르고 전력을 아끼는 새로운 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/) <strong>ChaCha20</strong>을 들고나와 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 웹 표준의 판도를 뒤집어버렸다.

- **📢 섹션 요약 비유**: [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)는 튼튼하지만 무거운 '전신 갑옷'이다. 적의 칼은 잘 막지만, 입고 벗는 데 오래 걸리고 기사가 뛰어다니면(모바일 환경) 금방 지친다. [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 방탄유리 섬유로 짠 '가벼운 쫄쫄이 타이츠'다. 엄청나게 가볍고 빨라서 닌자처럼 날아다니면서도 총알을 튕겨내는 최고의 기동성(속도)을 자랑한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. **모바일 우선(Mobile First) 통신 환경의 ChaCha20-Poly1305 융합**: 스마트폰에서 카카오톡이나 유튜브 웹([HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/))에 접속할 때, 아키텍트는 서버와 클라이언트 협상(Handshake) 과정에서 1순위 암호 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 `AES-256-GCM` 대신 `ChaCha20-Poly1305`로 우선 제안(Cipher Suite)하게 셋팅한다. 최신 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) CPU는 [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 가속 칩([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-NI)이 있어 AES가 빠르지만, 저가형 스마트폰이나 구형 ARM AP에서는 하드웨어 가속이 없어 AES가 배터리를 녹인다. 순수 소프트웨어 연산만으로도 AES보다 압도적으로 빠른 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)(ChaCha20)가 모바일 통신의 최후의 구원자다.
2. <strong>동기식(<a href="/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/">Synchronous</a>) 난수 붕괴 시 재동기화 아키텍처</strong>: 과거의 단순 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 중간에 패킷이 하나 유실되면 뒤따라오는 수 기가바이트의 영상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 몽땅 노이즈(쓰레기 화면)로 변했다. 이를 막기 위해 현대 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 설계자는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프레임마다 평문과 독립적인 고유의 '[IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)(Initialization Vector, 초기화 벡터)'를 끼워 넣어 매번 난수 공장(PRNG)의 박자를 초기화해 준다. 1번 프레임이 날아가도 2번 프레임부터는 다시 IV로 리셋되어 깨끗하게 복호화되는 완벽한 스트리밍 생존성을 획득한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>키 스트림 재사용(<a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> Reuse / Two-Time Pad)에 의한 자살 행위</strong>: [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/) 최악의 금기. "암호키 하나 잘 만들어 놨으니, A한테 메시지 보낼 때도 이 키로 섞고, 내일 B한테 보낼 때도 똑같은 키로 섞어서 XOR 해야지!"라고 하는 순간 시스템은 끝장난다. 암호문 A와 암호문 B를 가로챈 해커가 두 암호문끼리 XOR 연산(⊕)을 때려버리는 순간, 수학적으로 공통된 난수(키 스트림)가 `0`이 되어 소멸하고 평문 A와 평문 B의 순수한 결합이 튀어나와 버린다. 키([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))와 IV의 조합은 우주가 끝날 때까지 단 한 번만 쓰고 버려야([Nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/)) 한다.

- **📢 섹션 요약 비유**: [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/) 키를 두 번 재사용하는 것은, 보안 문서를 가리기 위해 '구멍 뚫린 똑같은 패턴의 검은 도화지(키 스트림)'를 여러 다른 문서 위에 덮어서 보여주는 짓이다. 도둑이 그 도화지가 덮인 사진 두 장을 겹쳐보는 순간(XOR), 구멍의 패턴이 지워지고 뒤에 숨은 원래 글씨(평문)가 선명하게 다 드러나는 치명적인 마술 트릭의 붕괴다.

---

## Ⅴ. 기대효과 및 결론

[스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)([Stream Cipher](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/))는 한때 무겁고 강력한 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/))의 그늘에 가려져 "보안이 약하고 가벼운 싸구려 암호"로 무시당했던 시절이 있었다([RC4](/studynote/09_security/02_crypto/081_rc4_stream_cipher/) 붕괴 사건).

하지만 스마트폰과 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 등 저전력 기기 100억 대가 인터넷에 연결되는 초연결 시대가 도래하자, 극도로 가벼운 연산량으로 1비트의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)도 없이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화해 쏘아내는 이 단순한 XOR 기계장치는 'ChaCha20'이라는 완전체로 진화하며 웹 보안 생태계의 패권을 되찾았다. [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 쇳덩어리 덩치를 키우지 않고 물의 흐름처럼 순결하고 빠르게 흘려보내는, 속도와 전력 최적화의 극의에 달한 아키텍처다.

- **📢 섹션 요약 비유**: [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 디지털 세계의 '투명 망토 스프레이'다. [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/)처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 무거운 쇳덩어리 철가방에 담고 자물쇠를 채울([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생) 필요 없이, 파이프라인을 통과하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위에 실시간으로 투명 스프레이(XOR 키 스트림)를 칙 뿌리기만 하면 즉시 외계어로 변해서 0.001초의 딜레이도 없이 날아가는 궁극의 스피드 마법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>XOR 연산 (배타적 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>합, ⊕)</strong> | [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)를 구성하는 유일무이한 마법의 수학 기호. 두 값이 같으면 0, 다르면 1을 뱉는 이 단순한 스위치가 암호화와 복호화를 동시에 1클럭 만에 끝내버린다. |
| <strong>PRNG (의사 <a href="/studynote/01_computer_architecture/14_hardware_security_trends/486_trng/">난수 생성기</a>)</strong> | 짧은 암호키(Seed)를 먹고, 우주 끝까지 패턴이 반복되지 않는 거대한 난수 폭포(키 스트림)를 뿜어내는 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)의 심장 엔진 (LFSR 구조 등) |
| <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">IV</a> (초기화 벡터) / <a href="/studynote/09_security/05_web_app_security/519_oidc_nonce/">Nonce</a></strong> | 고정된 암호키만 계속 쓰면 해커에게 난수 패턴이 털리므로([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Reuse 붕괴), 통신할 때마다 매번 키 꼬리에 랜덤한 소금을 쳐서 완전히 새로운 난수가 뿜어지게 만드는 1회용 쇳덩어리 조미료 |

### 📈 관련 키워드 및 발전 흐름도

```text
무전 통신 등 실시간 스트리밍 환경에서 블록 암호(기다림)의 지연(Latency) 한계 직면
    |
    v
평문 1비트와 난수 1비트를 실시간 XOR 융합하는 스트림 암호 (Stream Cipher) 탄생
    |
    v
RC4 알고리즘의 무선 인터넷(WEP, WPA/TKIP) 싹쓸이 및 전성기
    |
    v
RC4 초기 키 스트림의 수학적 편향성(취약점) 폭로 및 몰락 ---> 한동안 AES(블록 암호) 천하
    |
    v
모바일/IoT 폭증으로 가벼운 암호화 수요 재점화 ---> 초경량/초강력 난수 엔진 'ChaCha20' 등장 및 TLS 표준 장악
```

이 흐름도는 "실시간성 요구 -> 단순 구조의 성공([RC4](/studynote/09_security/02_crypto/081_rc4_stream_cipher/)) -> 치명적 수학 결함으로 인한 몰락 -> 모바일 시대의 배터리 최적화 요구에 맞춘 완벽한 부활(ChaCha20)"이라는 [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)의 롤러코스터 같은 생존사를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [스트림 암호](/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/)는 사탕이 컨베이어 벨트를 지나갈 때 상자에 다 찰 때까지 기다리지 않고, 1개씩 지나갈 때마다 실시간으로 보이지 않는 투명 페인트를 뿌리는(암호화) 기술이에요.
2. 기다리는 시간이 0초라서 엄청나게 빠르고 스마트폰 배터리도 거의 닳지 않는 최고의 가성비 마법이죠.
3. 하지만 투명 페인트 통(암호키)을 실수로 두 번 재사용하면 도둑이 마법의 비밀을 바로 눈치채버리니까, 매번 새로운 페인트 통을 까서 써야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 80 / 1108

<- **이전**: [079. 블록 암호 (Block Cipher - DES, AES)](/studynote/09_security/02_crypto/079_block_cipher/)
**다음**: [81. RC4 (Rivest Cipher 4)](/studynote/09_security/02_crypto/081_rc4_stream_cipher/) ->

---
