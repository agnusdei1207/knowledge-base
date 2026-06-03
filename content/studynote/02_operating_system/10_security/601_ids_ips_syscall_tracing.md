+++
title = "601. 침입 탐지 시스템 (IDS) / 침입 방지 시스템 (IPS) 시스템 콜 트레이싱 기반 이상 탐지"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 침입 탐지 시스템 (IDS, [Intrusion Detection System](/knowledge-base/studynote/09_security/uncategorized/994_ids_ips_intrusion_detection_prevention_false_positive/))과 방지 시스템 ([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/), Intrusion Prevention System)은 네트워크 패킷이나 호스트 OS 내부의 이벤트를 분석하여 비정상적인 악성 행위를 식별하고(IDS) 이를 능동적으로 차단하는([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)) 보안 관제의 핵심 인프라다.
> 2. **가치**: 기존 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 IP/[Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 기반의 정적인 '문지기' 역할만 했다면, IDS/IPS는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 깊은 내용(Payload)과 OS의 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/)) 시퀀스까지 동적으로 추적하여 [셸코드](/knowledge-base/studynote/02_operating_system/10_security/592_shellcode_injection/) 주입이나 [제로데이](/knowledge-base/studynote/09_security/15_malware_attack_vectors/761_zero_day/) 공격을 맥락적(Contextual)으로 탐지해 낸다.
> 3. **융합**: 고성능 패킷 처리를 위한 하드웨어 아키텍처, 알려진 공격을 막는 오용 탐지(Misuse/Signature), 미지의 공격을 탐지하는 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/)/ML), 그리고 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 시스템 콜 트레이싱 메커니즘이 완벽하게 융합된 복합 기술의 결정체다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
침입 탐지 시스템 (IDS)은 네트워크나 호스트에서 발생하는 이벤트를 실시간으로 모니터링하여 침해 시도, [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) 위반을 '경고(Alert)'하는 감시 카메라 역할을 한다. 반면, 침입 방지 시스템 ([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/))은 탐지 기능을 넘어 악성 패킷을 버리거나(Drop), 연결을 끊어버리는(RST) 등 즉각적인 차단 행동을 취하는 '능동형 방어 요원'이다. 

**필요성 및 등장 배경**
[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)의 [패킷 필터링 방화벽](/knowledge-base/studynote/09_security/05_web_app_security/213_packet_filtering_firewall/)(L3/L4)은 내부망으로 향하는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)(80번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) 트래픽을 허용할 수밖에 없었다. 해커들은 이 합법적으로 열린 80번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 [버퍼 오버플로우](/knowledge-base/studynote/02_operating_system/10_security/591_buffer_overflow/) 페이로드나 SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) 공격을 섞어 보냈고, [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 이를 단순한 웹 요청으로 착각해 무사통과시켰다. 따라서 허용된 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 안쪽을 흐르는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Payload)의 내용물을 깊이 뜯어보고(Deep Packet Inspection), [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 프로세스를 실행하는 단계에서 위험한 시스템 콜이 호출되는지를 추적하는 '똑똑한 내용 검사기'의 필요성이 대두되며 IDS/[IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 체계가 발전했다.

```text
┌─────────────────────────────────────────────────────────────┐
│      네트워크 보안 장비의 아키텍처 진화 (방화벽 → IDS → IPS)│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [1세대: 방화벽 (Firewall)]                                 │
│  "포트 80번(웹)은 열어줘. 나머지는 다 차단해!"              │
│  => 해커: "포트 80번 안으로 SQL 인젝션 공격 코드를 넣자!"   │
│  => 결과: 💥 방화벽 무사 통과, 서버 장악됨.                 │
│                                                             │
│  [2세대: NIDS (네트워크 침입 탐지 시스템)]                  │
│  스위치의 Mirror 포트에 연결되어 트래픽을 복사해서 감시.    │
│  "어? 80번 포트로 들어가는 데이터 속에 공격 코드가 보여!"   │
│  => 결과: 📢 관리자에게 경고(알람) 전송. 하지만 이미        │
│            공격 패킷은 서버에 도달해 버림 (탐지 지연).      │
│                                                             │
│  [3세대: NIPS (네트워크 침입 방지 시스템)]                  │
│  네트워크 라인 중간(Inline)에 직접 설치되어 모든 패킷 검문. │
│  "어? 공격 코드가 들어있네? 이 패킷은 여기서 바로 폐기!"    │
│  => 결과: 🛡️ 실시간 차단 성공. 단, 오탐(False Positive)     │
│            발생 시 정상 서비스도 끊어지는 위험 존재.        │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 흐름도는 왜 기업 인프라에 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 하나만으로 부족한지 직관적으로 설명한다. IDS는 네트워크 옆에 비스듬히 연결된(Out-of-band / Mirroring) CCTV와 같아서, 공격을 알아채고 경고를 울리지만 범인을 멈춰 세울 물리적 통제권이 없어 피해를 예방하지 못한다. 이를 극복하기 위해 IPS는 통신망의 정중앙(Inline)에 서서 모든 패킷을 직접 열어보고 통과 여부를 결정하는 톨게이트 방식으로 진화했다. 다만 [IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 인라인 모드는 시스템 오류나 정탐/오탐으로 인해 전체 네트워크 속도가 느려지거나 정상 비즈니스가 멈출 수 있는 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure)이 될 수 있으므로 아키텍처 설계 시 바이패스(Bypass) 하드웨어 구성이 필수적이다.

- **📢 섹션 요약 비유**: [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 건물 입구에서 "방문 목적"만 묻고 통과시키는 경비원이라면, IDS는 방 안에서 무기를 꺼내는지 지켜보고 비상벨을 누르는 CCTV이며, IPS는 그 자리에서 직접 무기를 빼앗고 쫓아내는 무장 경찰과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 탐지 기법 모델: 오용 탐지 vs [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)

어떻게 공격을 알아낼 것인가에 대한 철학적 접근법은 크게 두 가지로 나뉜다.

| 탐지 기법 | 핵심 원리 및 매커니즘 | 장점 | 단점 및 한계 | 비유 |
|:---|:---|:---|:---|:---|
| **오용 탐지 (Misuse)** / 시그니처 기반 | 기 검증된 공격 패턴(시그니처 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))과 매칭 검사. "이 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 배열이 보이면 차단해" | 알려진 공격(1-Day 등)에 대해 **정탐률이 매우 높고 오탐률이 낮음**. | 새로운 변종이나 <strong><a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/761_zero_day/">제로데이</a>(0-Day) 공격 탐지 불가</strong>. DB 업데이트 부하. | 지명수배자 얼굴(몽타주)을 보고 범인 잡기 |
| <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a> (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/">Anomaly</a>)</strong> / 행위 기반 | 시스템의 평상시 정상 상태([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))를 학습한 뒤, 이를 크게 벗어나는 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)(Threshold)나 행위 차단. | <strong><a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/761_zero_day/">제로데이</a> 등 미지의 공격</strong> 탐지 가능. (예: 평소 안 쓰던 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 대량 사용) | 정상 행위를 공격으로 오인하는 **오탐률(False Positive)** 이 매우 높음. | 평소 조용하던 직원이 갑자기 허둥대며 뛰어나가면 막기 |

현대의 최상위 시스템(NG-[IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/), [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/))은 오용 탐지를 기본 방어막으로 깔고, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(ML) 기반의 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 알고리즘을 융합하여 0-Day 탐지력과 낮은 오탐률의 균형을 맞춘다.

### 호스트 기반 HIDS 아키텍처와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시스템 콜 트레이싱

[NIDS](/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/)/NIPS가 네트워크 "외부"의 트래픽을 본다면, **HIDS (Host-based IDS)** 는 서버 OS "내부"에 에이전트로 설치되어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 프로세스 트리, 그리고 가장 중요한 <strong>시스템 콜 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a>)</strong>을 감시한다. 해커가 암호화된 터널([HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/))로 공격 페이로드를 보내 NIDS의 눈을 속이더라도, 결국 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 `execve`(프로세스 실행)나 `open`([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 열기) 같은 시스템 콜을 날려야만 목표를 달성할 수 있기 때문이다.

```text
┌─────────────────────────────────────────────────────────────┐
│      HIDS / EDR의 시스템 콜(System Call) 트레이싱 원리      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [해커의 암호화된 공격 페이로드 유입]                       │
│  네트워크(NIDS 우회) ─(HTTPS 암호화)─▶ 웹 서버 (Application)│
│                                               │             │
│  [웹 서버 내부의 취약점 실행 시퀀스]          │             │
│  ① 웹 서버 프로세스가 해커의 ROP 셸코드 실행 시도           │
│  ② 셸코드가 커널의 핵심 기능을 사용하기 위해 시스템 콜 호출 │
│      - syscall: mprotect (실행 권한 부여)                   │
│      - syscall: execve ("/bin/sh")                          │
│      - syscall: socket, connect (리버스 셸 연결)            │
│                                                             │
│  [HIDS / eBPF 기반 커널 트레이서 (Kernel Tracer)]           │
│    ▲ 커널 모드 진입 시 시스템 콜 후킹(Hooking) 발생!        │
│    │                                                        │
│    ├─▶ 검사 로직: "웹 서버(httpd)가 갑자기 /bin/sh를        │
│    │               자식 프로세스로 실행하려 한다고?"        │
│    │                                                        │
│    └─▶ 판단: [정상 베이스라인 위반 (Anomaly Detected)]      │
│        조치: 해당 프로세스 트리 강제 킬(Kill) 및 차단 (IPS) │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 호스트(OS) 내부에서 침입 탐지가 어떻게 동작하는지를 보여준다. 공격자가 페이로드를 암호화하여 네트워크단([NIDS](/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/))의 시그니처 검사를 무사통과하더라도, 목적지에 도달한 페이로드는 자신이 원하는 악성 행위(쉘 획득 등)를 위해 반드시 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에게 자원을 요청([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))해야 한다. 최신 HIDS나 [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/)(Endpoint [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) and Response) 솔루션은 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 최신 프레임워크인 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> (Extended <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/">Berkeley Packet Filter</a>)</strong> 나 `ptrace`를 이용하여, 시스템 콜이 실행되기 직전 그 인자와 호출의 맥락(누가, 무엇을 부르는가)을 가로채어 분석한다. 평소에 정적 콘텐츠만 반환하던 아파치 워커 프로세스가 갑자기 네트워크 소켓을 새로 열고(리버스 셸) 리눅스 셸(`/bin/sh`)을 실행하는 시스템 콜 시퀀스를 발생시킨다면, 이는 명백한 이상 행위([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))로 규정되어 즉각 차단된다. 이것이 암호화 통신 시대에 HIDS가 네트워크 IPS보다 더 주목받는 이유다.

- **📢 섹션 요약 비유**: 성문 밖 초소([NIDS](/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/))에서 암호로 쓰인 편지([HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/))를 검사하지 못해 통과시켜 주었더라도, 결국 그 편지를 읽은 성 안의 스파이가 무기고의 문을 열려고(시스템 콜) 할 때 성 내부의 잠복 경찰(HIDS/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 트레이서)이 즉각 체포하는 다층 구조와 같습니다.

---

## Ⅲ. 비교 및 연결

### [NIDS](/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/) (네트워크 기반) vs HIDS (호스트 기반)의 입체적 비교

하나의 기술만으로는 방어가 불가능하므로, 아키텍트는 두 시스템의 트레이드오프를 명확히 이해하고 하이브리드(Hybrid) 아키텍처를 구성해야 한다.

| 비교 항목 | [NIDS](/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/) / NIPS (네트워크 기반) | HIDS / HIPS (호스트/OS 기반) |
|:---|:---|:---|
| **모니터링 대상** | 네트워크 세그먼트를 흐르는 전체 패킷 | 특정 서버 내부의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정, 프로세스, 시스템 콜 |
| **운영 및 구축 비용** | 라우터/[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 엣지 1대에만 설치하면 하위 전체 커버 가능 (경제적) | 수백 대의 서버마다 OS별 에이전트를 개별 설치하고 관리해야 함 (높음) |
| **암호화 트래픽 처리** | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 복호화 프록시가 없으면 내용을 읽지 못해 장님(Blind)이 됨 | 앱 단에서 복호화가 끝난 평문 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 시스템 콜 자체를 분석하므로 우수 |
| **자원 소모 오버헤드** | 전용 하드웨어([ASIC](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/)) 사용으로 서버 OS 자원(CPU)에 영향 없음 | 에이전트가 실행되며 서버 자원(CPU, 메모리) 3~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 점유율 차지 |
| <strong>스니핑/<a href="/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/">스푸핑</a> 탐지</strong> | [ARP](/knowledge-base/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/), [포트 스캐닝](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/) 등 네트워크 흐름 파악에 특화됨 | 단일 호스트로 향하지 않는 네트워크 전체의 스캔 행위는 볼 수 없음 |

```text
┌─────────────────────────────────────────────────────────────┐
│      네트워크와 호스트 융합 (Hybrid IDS/IPS) 방어 아키텍처  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [인터넷] ──▶ [ 외부 방화벽 (L3/L4 접근 통제) ]            │
│                      │                                      │
│                      ▼                                      │
│   [ NIPS (인라인) ] ◀── 알려진 취약점 패턴(시그니처)의 패킷 │
│     (네트워크 기반)     유입 시 즉각 Drop (부하 분산 역할)  │
│                      │                                      │
│                      ▼ (정상 및 암호화된 트래픽 통과)       │
│                [ L2 스위치 망 ]                             │
│                  │          │                               │
│                  ▼          ▼                               │
│        [웹 서버 A]        [DB 서버 B]                       │
│        + HIPS 에이전트    + HIPS 에이전트                   │
│                                                             │
│   HIPS 역할: NIPS를 뚫고 들어온 암호화된 제로데이 페이로드가│
│              로컬 OS의 핵심 파일 변조 및 비정상 시스템 콜을 │
│              발생시키면 행위 기반으로 탐지 및 차단!         │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 하이브리드 아키텍처는 "심층 방어([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/))"의 교과서적 모델이다. NIPS는 최전방에서 수십 Gbps로 쏟아지는 알려진 공격(SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) 시그니처, 웜 [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 패턴, 대용량 스캐닝)을 하드웨어 가속을 통해 저비용 고효율로 쳐내는 방파제 역할을 한다. NIPS를 무사 통과한 고도화된 타겟팅 공격이나 암호화된 공격 페이로드는 개별 서버(엔드포인트)에 도달한다. 이때 서버 OS 내부에 심어진 HIPS 에이전트가 마지막 수문장으로서 OS 시스템 콜 수준의 행위 분석을 통해 악성 행위의 '발현'을 차단한다. 두 시스템의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/)(통합 보안 관제 시스템)으로 모여 연관 분석(Correlation)된다.

- **📢 섹션 요약 비유**: NIPS는 국경을 넘는 거대한 화물차들을 엑스레이로 스캔하여 밀수품을 1차로 걸러내는 세관이고, HIPS는 각 가정집 내부에 상주하며 누군가 금고를 열려 할 때 행동을 제압하는 개인 경호원과 같습니다. 두 계층이 모두 있어야 완벽한 방어가 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: False Positive (오탐지)로 인한 운영 장애 및 회피

1. <strong>상황 (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/">IPS</a> 인라인 모드 장애)</strong>: 쇼핑몰의 대형 이벤트 기간 중 트래픽이 폭주하자, NIPS 장비가 정상적인 고객들의 다중 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 시도를 Brute-force 공격으로 오인(False Positive, 오탐)하여 정상 고객 IP들을 무더기로 차단(Drop)하는 사태가 발생했다.
2. **원인 분석**: 룰셋(시그니처) 업데이트 시 "1분에 5회 이상 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 실패 시 IP 차단"이라는 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)가 엄격하게 걸려있었으나, 수만 명이 몰리는 이벤트 특성을 반영하지 못한 경직된 오용 탐지 로직이 문제였다.
3. **방어자의 의사결정 (Fail-Open 및 튜닝)**:
   - **조치 1 (Fail-Open 우회)**: 당장의 비즈니스 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 회복을 위해 [IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 장비의 하드웨어 바이패스(Bypass) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 활성화하여, 공격 여부 검사 없이 패킷을 무조건 통과시키는 `Fail-Open` 상태로 강제 전환한다.
   - <strong>조치 2 (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/694_snort_suricata_misuse_anomaly_detection/">Snort</a>/<a href="/knowledge-base/studynote/09_security/05_web_app_security/240_suricata_multithreaded_nids_ids_ips_engine/">Suricata</a> 룰 튜닝)</strong>: 이벤트가 끝난 후, IDS/[IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 엔진(예: [Snort](/knowledge-base/studynote/03_network/13_network_security_basics/694_snort_suricata_misuse_anomaly_detection/))의 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 조정하고 예외 IP(화이트리스트)를 반영하는 튜닝 작업을 거친다.
   - <strong>조치 3 (ML 기반 <a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a> 도입)</strong>: 단순 고정 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)(Threshold)를 넘어, 과거 이벤트 기간의 트래픽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 알고리즘으로 학습시켜 "평시"와 "이벤트 시"의 정상 동적 베이스라인을 스스로 계산하여 유연하게 차단하는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 NIPS로 고도화를 추진한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) (오탐 및 회피 대응)
- **IDS Evasion (탐지 회피) 차단**: 해커가 페이로드를 아주 작게 쪼개거나(IP [Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)), 순서를 뒤죽박죽 섞어서 보내어 IDS의 패턴 매칭을 무력화시키는 회피 공격을 방어하기 위해, [IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 장비 내에 "IP [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 재조합(Reassembly) 및 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 스트림 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)" 엔진이 활성화되어 있는지 확인해야 한다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 사이징 (Sizing)</strong>: 인라인 NIPS는 패킷을 뜯어보는 검사(DPI) 오버헤드가 크므로 장비 스펙의 [Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 한계를 쉽게 넘는다. 평문 트래픽 대역폭뿐만 아니라 동시 연결 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 수([CPS](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/))와 암호화(SSL) 가속 카드 용량을 실무 트래픽 기준 1.5배 이상으로 사이징했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>운영 인력 없는 <a href="/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/">IPS</a> 도입</strong>: 도입 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 벤더사가 세팅해 준 기본(Default) 차단 룰셋만 켜놓고 방치하는 행위. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 특성에 맞춘 지속적인 튜닝(예외 처리)이 없으면, 잦은 오탐(False Positive)으로 인해 현업 부서의 원성이 폭발하고, 결국 보안팀 스스로 IPS의 차단(Prevention) 모드를 끄고 모니터링(IDS) 모드로만 운영하게 되는 최악의 "비싼 고철 장비 전락" 사태를 맞이한다.

- **📢 섹션 요약 비유**: IPS는 아주 날카로운 칼과 같아서 공격을 잘라내는 데 탁월하지만, 훈련된 요원(관제 인력의 튜닝)이 계속해서 날을 갈고 다듬어주지 않으면 정상적인 비즈니스라는 우리 자신의 팔다리(오탐 장애)를 베어버릴 수 있는 양날의 검입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과 (HIDS 시스템 콜 트레이싱 도입 시)

| 구분 | NIPS만 운용 (레거시 방어) | [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 HIPS 도입 및 융합 운용 | 기술적 함의 |
|:---|:---|:---|:---|
| **가시성** | 암호화 트래픽 내부 및 로컬 공격 경로 맹점 발생 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 시스템 콜, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 액세스, [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/) **가시성 100%** 확보 | 클라우드 워크로드 및 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 내부 통신망 감시 체계 완성 |
| **정량 (탐지 속도)** | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석을 거쳐 수 분~수 시간 소요 | 이상 행위 발생 즉시 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 단에서 프로세스 **밀리초 단위 차단** | [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 암호화가 시작되기 전 극초기 킬 체인 단계에서 절단 |
| **정성 (보안 관제)** | 무의미한 네트워크 알람(Noise)의 홍수 | "A 프로세스가 B [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 변조하려 함"이라는 명확한 맥락([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)) 기반 알람 | 관제 대응([IR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/)) 인력의 피로도 감소 및 신속한 의사결정 지원 |

### 미래 전망
[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), IDS, [IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/), 백신으로 파편화되어 발전하던 기술들은 이제 하나의 통합된 지능형 에이전트인 <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/127_xdr_external_data_representation/">XDR</a> (Extended <a href="/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a> and Response)</strong> 과 클라우드 보안 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([CNAPP](/knowledge-base/studynote/15_devops_sre/05_devsecops/256_cnapp_cloud_native_application_protection/)) 플랫폼으로 수렴하고 있다. 특히 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 생태계에서는 NIPS 하드웨어 장비에 의존하기보다, 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부의 샌드박스 프로그래밍 환경인 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> (Extended <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/">Berkeley Packet Filter</a>)</strong> 를 활용하여 에이전트 설치 오버헤드 없이 OS 자체가 본연적으로 패킷을 필터링하고 시스템 콜을 검증하는 초경량, 고성능의 [내재적 보안](/knowledge-base/studynote/09_security/01_intro_principles/058_security_by_design/)([Security by Design](/knowledge-base/studynote/09_security/01_intro_principles/058_security_by_design/)) 아키텍처가 미래 표준으로 자리 잡을 것이다.

### 참고 표준
- <strong>NIST <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> 800-94</strong>: 침입 탐지 및 방지 시스템(IDPS) 가이드라인
- **ISO/IEC 27039**: 디지털 증거 수집 및 분석 (IDS [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 법적 보존)
- <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/642_mitre_attack/">MITRE ATT&CK</a></strong>: T1055 ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)) 방어 및 완화 체계

- **📢 섹션 요약 비유**: 성벽의 경비병(NIPS)에 의존하던 시대를 넘어, 이제는 모든 병사와 시민의 핏속에 나노 로봇([eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 트레이서)을 주입하여 몸속에 나쁜 [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/)(비정상 명령)가 들어오는 즉시 유전자 단계에서 소멸시켜 버리는 궁극의 면역 체계로 진화하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [서비스 거부](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/) ([DoS](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/)) 및 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/) (DDoS) 네트워크 자원 고갈 공격 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [포트 스캐닝](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/) ([Port Scanning](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/)) 도구 원리 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [샌드박싱](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) ([Sandboxing](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/)) 기술 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 래퍼 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/) ([Rootkit](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 감염 방식 (시스템 콜 테이블 후킹) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[포트 스캐닝 (Port Scanning) 도구 원리]
    │
    ▼
[침입 탐지 시스템 (IDS) / 침입 방지 시스템 (IPS) 시스템 콜 트레이싱 기반 이상 탐지]
    │
    ├──▶ [샌드박싱 (Sandboxing) 기술 커널 래퍼]
    └──▶ [루트킷 (Rootkit) 커널 모듈 감염 방식 (시스템 콜 테이블 후킹)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 아파트 입구에서 비밀번호를 모르는 나쁜 사람을 못 들어오게 막는 <strong>현관문</strong>이에요.
2. 하지만 나쁜 사람이 택배 기사로 위장(암호화/웹 요청)해서 문을 통과해버리면 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 막지 못해요. 이때 복도에 설치된 <strong><a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/">CCTV</a>(IDS)</strong> 가 그걸 보고 "경비 아저씨 출동하세요!" 하고 삐용삐용 알람을 울려주죠.
3. 더 똑똑한 <strong>방어 로봇(<a href="/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/">IPS</a>)</strong> 은 복도에서 나쁜 사람이 택배 상자에서 칼(해킹 코드)을 꺼내는 순간, 알람만 울리는 게 아니라 그 자리에서 직접 로봇 팔로 칼을 빼앗고 쫓아내는 멋진 경찰관 역할을 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 601 / 800

← **이전**: [600. 포트 스캐닝 (Port Scanning) 도구 원리](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/)
**다음**: [602. 샌드박싱 (Sandboxing) 기술 커널 래퍼](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) →

---
