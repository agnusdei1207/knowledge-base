+++
weight = 774
title = "774. 네트워크 파일 시스템 (NFS) 무상태 (Stateless)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[543_nfs_network_file_system|NFS]] ([[543_nfs_network_file_system|Network File System]])는 내 컴퓨터에 없는 다른 서버의 하드 디스크 폴더를 네트워크를 통해 당겨와, 마치 **내 컴퓨터에 꽂힌 물리적 C드라이브(로컬 디스크)인 것처럼 완벽하게 눈속임([[516_mount_mechanism|마운트]], [[516_mount_mechanism|Mount]])해 주는 원격 [[501_file_definition_logical_record|파일]] 공유 [[295_protocol_field_tcp_udp_icmp|프로토콜]]**이다.
> 2. **가치**: [[543_nfs_network_file_system|NFS]] v2/v3 아키텍처의 가장 위대한 철학은 서버가 클라이언트의 상태를 전혀 기억하지 않는 **무상태([[239_stateless_redis|Stateless]]) 아키텍처**에 있다. 덕분에 서버가 갑자기 뻗었다 켜져도 클라이언트들은 에러를 뿜고 죽는 대신 하던 작업을 투명하게 재개(Resilience)할 수 있는 극강의 고가용성을 획득했다.
> 3. **융합**: 가상 [[501_file_definition_logical_record|파일]] 시스템([[517_virtual_file_system_vfs|VFS]]) [[238_switch_operation_principles|스위치]] 계층과 [[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]]) 통신 기술이 융합되어, 응용 프로그램이 코드를 1비트도 수정하지 않고 로컬 `read()/write()` 함수만으로 태평양 건너의 스토리지 [[001_dikw_pyramid|데이터]]를 조작할 수 있게 만든 클라우드 NAS의 역사적 토대다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - Sun Microsystems가 1984년 개발한 [[553_distributed_file_system|분산 파일 시스템]]. 
  - 클라이언트가 서버의 특정 디렉터리를 자신의 폴더에 [[516_mount_mechanism|마운트]]([[516_mount_mechanism|Mount]])하면, [[001_operating_system_purpose|운영체제]]([[517_virtual_file_system_vfs|VFS]])가 몰래 로컬 시스템 콜을 네트워크 [[126_rpc|RPC]] 패킷으로 포장해 서버로 던지고 결과를 받아온다.

- **필요성 ([[136_variance|분산]] 환경의 [[443_isolation_concurrency_control|고립성]] 타파)**: 
  - 과거 수십 대의 유닉스 워크스테이션이 있을 때, A 직원이 B 자리로 가면 자신이 쓰던 소스 코드를 플로피 디스크에 복사해서 옮겨 다녀야 했다(Sneakernet).
  - "중앙의 거대한 [[501_file_definition_logical_record|파일]] 서버 하나에 모든 코드를 두고, 100대의 컴퓨터가 동시에 그 폴더를 C드라이브처럼 연결해서 쓰면 어떨까?"
  - 그런데 이 과정에서 중앙 서버의 랜선이 1초 빠지면 클라이언트 100대가 [[501_file_definition_logical_record|파일]] I/O 에러로 동반 자살하는 끔찍한 연쇄 크래시 위험이 있었다.
  - **해결책 ([[239_stateless_redis|Stateless]])**: "서버는 클라이언트가 [[501_file_definition_logical_record|파일]]을 열었는지 닫았는지 전혀 기억하지 마라! 클라이언트가 매 요청마다 'A [[501_file_definition_logical_record|파일]]의 10번지부터 5바이트 줘'라고 모든 맥락([[033_context|Context]])을 꽉 채워서 보내게 하자!"

  - **상태 유지 (Stateful, 텔레마케터)**: "고객님 아까 말씀하신 그 상품([[501_file_definition_logical_record|파일]] 오픈) 말이죠, 방금 고르신 색상(10번지 오프셋)으로 주문할까요?" -> 중간에 전화가 끊겨서 다시 걸면 처음부터 상황 설명을 다 다시 해야 함.
  - **무상태 ([[239_stateless_redis|Stateless]], 자판기)**: 돈을 넣고 '콜라 1번(정확한 [[501_file_definition_logical_record|파일]] 위치 묘사)'을 누르면 무조건 콜라가 나옴. 자판기 전원이 나갔다 들어와도, 내 손에 동전(요청)만 있으면 처음부터 아무 일 없었던 듯 뽑아 먹을 수 있음.

- **등장 배경**: 
  - LAN(근거리 통신망) 시대의 도래와 함께 썬 마이크로시스템즈의 "네트워크가 곧 컴퓨터다(The Network is the Computer)"라는 사상을 현실화한 기술이며, 오늘날 AWS EFS 같은 관리형 클라우드 [[492_nas_network_attached_storage|NAS]] 시스템의 표준 뼈대로 자리 잡았다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 VFS와 RPC를 융합한 NFS의 투명한 동작 아키텍처         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │   [ 클라이언트 (Client PC) ]                                   │
  │                                                             │
  │    App: `read(fd, buf, 1024)` 호출 (난 로컬 디스크인줄 앎)         │
  │            │                                                │
  │            ▼                                                │
  │    [ VFS (Virtual File System) 계층 ]                       │
  │    "어? 이 파일은 로컬(ext4)이 아니라 NFS 타입으로 마운트됐네?"        │
  │            │ (분기)                                          │
  │            ▼                                                │
  │    [ NFS Client 모듈 ]                                       │
  │    read() 함수를 RPC(원격 프로시저 호출) 네트워크 패킷으로 캡슐화 포장    │
  │            │ "안녕? 파일핸들 X의 1024번지부터 읽어줘!"              │
  │  ==========│================ (TCP/IP 네트워크) ===============│
  │            ▼                                                │
  │   [ 파일 서버 (NFS Server) ]                                   │
  │                                                             │
  │    [ NFS Server Daemon (nfsd) ]                             │
  │    RPC 패킷 해독 -> 진짜 로컬 VFS로 `read()` 찔러넣음                │
  │            │                                                │
  │            ▼                                                │
  │    [ 로컬 파일 시스템 (ext4) & 디스크 ]                            │
  │    데이터 읽어서 역순으로 네트워크를 통해 클라이언트로 배달 슝~ 🚀          │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 클라이언트 애플리케이션 입장에서는 이 과정이 완벽하게 은폐(투명성, Transparency)되어 있다. 일반 텍스트 [[501_file_definition_logical_record|파일]]을 읽듯 코딩했는데, 밑단에서 [[517_virtual_file_system_vfs|VFS]] [[238_switch_operation_principles|스위치]]가 기찻길을 틀어버린다. 로컬 디스크 드라이버로 갈 신호를 낚아채어 네트워크 랜카드를 통해 태평양 너머의 서버로 날려버린다. 이 모든 통신의 근간인 **[[126_rpc|RPC]]([[126_rpc|Remote Procedure Call]])**는 마치 네트워크 건너편 서버의 함수를 내 컴퓨터에 있는 함수처럼 편하게 호출하게 해주는 통신 규격이다. NFS는 이 [[126_rpc|RPC]] 위에서 동작하는 '[[501_file_definition_logical_record|파일]] 입출력 특화된 원격 심부름꾼'이다.

- **📢 섹션 요약 비유**: 회사 사장님(앱)이 "비서([[517_virtual_file_system_vfs|VFS]]), 창고에서 서류 좀 가져와!"라고 지시했을 때, 사장님은 그 창고가 옆방(로컬 디스크)인지, KTX를 타고 가야 하는 부산 창고([[543_nfs_network_file_system|NFS]] 원격 서버)인지 전혀 알 필요 없이 똑같이 1시간 뒤에 책상 위에서 서류를 받아보는 완벽한 심부름 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[543_nfs_network_file_system|NFS]] [[162_rest_statelessness|무상태성]] ([[162_rest_statelessness|Statelessness]])의 심연

전통적인 [[543_nfs_network_file_system|NFS]] v2와 v3의 가장 위대한 설계적 결단이 바로 "서버는 클라이언트의 상태를 저장하지 않는다"는 것이다.

1. **상태([[272_state_pattern|State]])란 무엇인가?**: 로컬에서 `open()`을 하면 커널은 "A 프로세스가 B [[501_file_definition_logical_record|파일]]을 읽고 있고, 현재 [[501_file_definition_logical_record|파일]] 포인터(읽는 위치)는 100번지다"라는 테이블을 램에 적어둔다. (상태 유지).
2. **[[543_nfs_network_file_system|NFS]] 서버의 망각**: [[543_nfs_network_file_system|NFS]] 서버에는 `open()` 이나 `close()` 개념이 없다! 클라이언트가 "[[501_file_definition_logical_record|파일]] A 열어줘"라고 하면 서버는 그냥 암호화된 '[[501_file_definition_logical_record|파일]] 핸들([[501_file_definition_logical_record|File]] Handle)' 껍데기만 하나 던져주고 기억에서 지워버린다.
3. **클라이언트의 멱살 캐리**: 클라이언트가 읽기를 원하면 멍청한 서버에게 매번 이렇게 풀센텐스(Full [[033_context|Context]])로 쏴줘야 한다. *"서버야, 내가 누구냐면 [[501_file_definition_logical_record|파일]] 핸들 X를 가진 놈인데, 예전에 내가 어디까지 읽었는진 네가 모를 테니까 내가 기억해 왔어. 100번지 오프셋부터 50바이트만 읽어서 리턴해 줘!"*

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 NFS Stateless 서버의 기적적인 장애 복원력 시나리오      │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [ 상황: 클라이언트가 원격 파일을 복사하다가 💥 서버의 전원 코드가 뽑힘! ] │
  │                                                                   │
  │  1. 클라이언트: "핸들 X, 오프셋 100번지 데이터 줘!" ──▶ (네트워크 요청)   │
  │                                                                   │
  │  2. 서버 전원 나감 ☠️ (네트워크 응답 없음)                               │
  │                                                                   │
  │  3. 클라이언트 반응: "어? 응답이 없네? 올 때까지 계속 재시도(Retry)해야지!"│
  │     - (App은 블로킹 된 채로 뻗지 않고 하염없이 버팀. Soft 마운트면 에러냄)│
  │                                                                   │
  │  4. (10분 뒤) 서버 재부팅 완료 🔄                                      │
  │     - 서버 메모리는 텅 빔. 클라이언트가 누군지 기억상실증.                    │
  │                                                                   │
  │  5. 클라이언트: "핸들 X, 오프셋 100번지 데이터 줘!" (무한 츠쿠요미 요청 중)│
  │                                                                   │
  │  6. 서버: "너 누군지 모르겠지만 네가 요청한 핸들 X 주소로 디스크 찾아서 줄게."│
  │     ──▶ 🟢 즉각 정상 응답 및 복사 101번지부터 완벽히 작업 속개!           │
  │                                                                   │
  │  ▶ 결론: 서버가 미쳐서 재부팅 되어도, 복잡한 세션 복구/재연결 핑퐁 없이    │
  │          10분 동안 일시 정지됐다가 아무 일 없던 듯 파일 복사가 이어지는 기적! │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 시나리오는 [[136_variance|분산]] 시스템에서 왜 [[477_rest_api_architecture|REST API]] ([[461_http_stateless_connection_oriented|HTTP]])나 무상태 설계가 세상을 지배했는지 보여주는 원초적 예시다. 만약 Stateful [[501_file_definition_logical_record|파일]] 서버(예: Windows SMB/CIFS 구버전)였다면, 서버가 재부팅되는 순간 서버 메모리에 있던 "클라이언트의 [[160_session_controlling_terminal|세션]] 정보"가 다 날아가 버린다. 클라이언트가 "아까 이어서 줘!"라고 해봤자 서버는 "너 누구야? 연결 처음부터 다시 맺어([[160_session_controlling_terminal|Session]] Expired)"라며 매몰차게 에러를 뱉고, 클라이언트의 다운로드는 99%에서 취소(Crash)된다. [[162_rest_statelessness|무상태성]]은 이 끔찍한 네트워크의 불안정성을 완벽한 재시도(Idempotent Retry)의 마법으로 덮어버린 것이다.

- **📢 섹션 요약 비유**: 동네 단골 식당(Stateful)은 주인이 바뀌면 "저번처럼 주세요"가 안 통해서 짜증 나지만, 맥도날드 키오스크([[239_stateless_redis|Stateless]])는 매장이 정전됐다가 켜져도 내가 '빅맥 세트' 버튼만 다시 누르면 지구 어디서나 똑같은 햄버거가 나오는 든든한 복원력입니다.

---

## Ⅲ. 비교 및 연결

### [[543_nfs_network_file_system|NFS]] 버전별 진화와 Stateful로의 변절 ([[543_nfs_network_file_system|NFS]] v3 vs v4)

무상태([[239_stateless_redis|Stateless]]) 철학은 아름다웠지만 시대가 변하며 한계를 맞았다. 

| 비교 항목 | [[543_nfs_network_file_system|NFS]] v3 (고전적 무상태 표준) | [[543_nfs_network_file_system|NFS]] v4 (현대적 Stateful 설계) |
|:---|:---|:---|
| **철학 및 연결 방식** | 완벽한 **무상태([[239_stateless_redis|Stateless]])** 유지. | 놀랍게도 **상태 보존(Stateful)**으로 선회함. |
| **[[446_port_and_bus|포트]] 통신** | RPCbind, Mountd 등 여러 [[446_port_and_bus|포트]]를 산발적으로 써서 **[[690_firewall_generation_evolution|방화벽]] [[009_config|설정]]이 지옥**임. | **[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 2049 [[446_port_and_bus|포트]] 딱 하나**만 사용하여 [[690_firewall_generation_evolution|방화벽]] 통과 및 [[307_nat_network_address_translation_router_principles|NAT]] 친화성 극대화. |
| **[[501_file_definition_logical_record|파일]] 락 ([[213_locking_mechanism_concurrency_control|Locking]])** | 무상태라서 서버가 누가 락을 쥐었는지 모름. NLM이라는 별도 락 데몬을 덕지덕지 붙여서 개판으로 동작. (동시 수정 시 [[501_file_definition_logical_record|파일]] 꼬임) | **Stateful 전환의 핵심 이유**. 서버가 [[160_session_controlling_terminal|세션]]을 기억하므로 [[501_file_definition_logical_record|파일]] 락(Lease) 제어를 완벽하게 수행. 여러 서버가 동시 수정해도 안전 보장. |
| **보안 강화** | 단순 IP/사용자 ID 기반 (IP 스푸핑에 속음) | [[545_kerberos_kdc_ticket_based_auth|Kerberos]] [[303_authentication_authorization_patterns|인증]] 및 [[126_rpc|RPC]] 암호화를 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 내재화 |

### 과목 융합 관점

- **[[001_operating_system_purpose|운영체제]] [[212_synchronization_mechanisms|동기화]] ([[501_file_definition_logical_record|파일]] 락 병목)**: 100대의 리눅스 서버가 [[543_nfs_network_file_system|NFS]] 버렉토리 1개에 동시에 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]을 쓴다 치자. [[543_nfs_network_file_system|NFS]] v3는 무상태이므로 A 서버가 쓰는 도중 B 서버가 무식하게 덮어써버려서 [[001_dikw_pyramid|데이터]] 블록이 믹서기처럼 갈려버리는 참사가 흔했다. 그래서 [[543_nfs_network_file_system|NFS]] 위에 [[002_database_definition|데이터베이스]] [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]을 두면 DB가 박살 난다는 룰이 있었다. 결국 무상태의 우아함을 버리고 [[501_file_definition_logical_record|파일]] 락([[510_lock|Lock]]) 무결성을 지키기 위해 [[543_nfs_network_file_system|NFS]] v4는 서버가 클라이언트의 [[160_session_controlling_terminal|세션]] 상태를 기억하는 방향(Stateful)으로 스스로 진화(타협)했다.
- **클라우드 스토리지 (EFS / [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]])**: AWS의 EFS(Elastic [[501_file_definition_logical_record|File]] System)는 겉보기엔 그냥 [[543_nfs_network_file_system|NFS]] v4.1 [[516_mount_mechanism|마운트]] 포인트 1개지만, 뒷단에서는 수백 대의 [[136_variance|분산]] 스토리지 랙이 엮여있는 클러스터다. 수천 대의 [[561_container_based_deployment|컨테이너]](EKS)가 동시에 EFS 볼륨을 물고 읽기/쓰기를 [[430_index_fast_full_scan|병렬]]로 때릴 수 있는 이유는, 이 [[543_nfs_network_file_system|NFS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 표준 인터페이스가 클라우드 시대 [[136_variance|분산]] 인프라의 [[532_microservices_decomposition_patterns|마이크로서비스]] 공유 볼륨 규격으로 완벽히 부활했기 때문이다.

- **📢 섹션 요약 비유**: 처음엔 손님 얼굴 기억하기 귀찮아서 자판기(v3 무상태)로 장사했는데, 손님들이 서로 같은 콜라를 집겠다고 싸우다 캔이 터지는 사고([[501_file_definition_logical_record|파일]] 락 붕괴)가 잦아지자, 결국 매니저를 고용해 손님 대기표를 뽑아주고 순서를 기억하게(v4 Stateful) 만든 현실적 시스템 발전사입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 트러블슈팅

1. **시나리오 — [[543_nfs_network_file_system|NFS]] 서버 다운 시 모든 웹 서버의 동반 패닉 (Hard vs Soft [[516_mount_mechanism|마운트]])**: 사내 Nginx 웹 서버 10대가 이미지 폴더를 공용 [[543_nfs_network_file_system|NFS]] 서버에 물려놨다. 어느 날 [[543_nfs_network_file_system|NFS]] 서버가 랜선 불량으로 10분간 뻗었다. 그런데 Nginx 앱들이 이미지를 서빙하려다 큐에 막혀, 웹 서버 전체의 프로세스 슬롯이 꽉 차서 정작 DB에서 가져오는 텍스트 API조차 응답하지 못하는 전면 마비 사태가 일어났다.
   - **원인 분석**: 리눅스 [[543_nfs_network_file_system|NFS]] [[516_mount_mechanism|마운트]]의 기본값은 **`hard`** [[516_mount_mechanism|마운트]]다. 이 모드는 [[543_nfs_network_file_system|NFS]] 서버가 응답할 때까지 프로세스를 "D [[272_state_pattern|State]](Uninterruptible Sleep)"로 무한정 블로킹([[122_sync_async_communication|Blocking]]) 시킨다. 심지어 `kill -9` [[158_instruction|명령어]]로도 죽일 수 없는 불사신 좀비가 되어 CPU 스케줄러를 물고 늘어진다.
   - **아키텍트 판단 (안티패래질 방어 튜닝)**: [[001_dikw_pyramid|데이터]]를 안전하게 보존하는 것보다 웹 서비스의 응답성이 중요하다면(예: 썸네일 이미지 서빙), [[516_mount_mechanism|마운트]] 옵션을 **`soft`**로 바꾸고 `timeo(타임아웃)`, `retrans(재시도 횟수)` 값을 짧게 주어야 한다. 이렇게 하면 서버가 죽었을 때 무한 대기하지 않고, 앱에 "I/O Error"를 쿨하게 뱉어주어 앱이 깨어나고 에러 처리를 한 뒤 생존할 수 있다. 하지만 결제 [[568_logs_distributed_logging_elk_fluentd|로그]] 같은 중요 [[501_file_definition_logical_record|파일]]이라면 D State를 감수하더라도 끝까지 재시도하는 `hard` 옵션을 유지하고 `intr` ([[016_interrupt_mechanism|인터럽트]] 허용) 옵션만 섞어 관리자의 킬 명령을 받게 튜닝하는 고도의 저울질이 필요하다.

2. **시나리오 — 루트 권한 탈취 (Root Squashing의 마법)**: 어떤 해커가 자기가 통제하는 [[164_pc|PC]](클라이언트)를 해킹한 뒤, 회사 중앙 [[543_nfs_network_file_system|NFS]] 서버를 [[516_mount_mechanism|마운트]]했다. 클라이언트에서 `sudo su`로 root 권한을 얻은 뒤, 공유 폴더에 악성 쉘 스크립트를 밀어 넣고 권한을 777로 바꿨다.
   - **원인 분석**: [[501_file_definition_logical_record|파일]] 시스템은 오직 "User ID 번호"로만 권한을 검사한다. 클라이언트의 짱구(UID 0번 = root)가 접근하면, [[543_nfs_network_file_system|NFS]] 서버 입장에서도 "어? UID 0번이 오셨네? 우리 서버의 root랑 같은 번호니 프리패스!" 라며 시스템 최고 권한을 털려버리는(Root Trust 붕괴) 어처구니없는 일이 발생한다.
   - **아키텍트 판단 (보안 격리)**: 이를 막기 위해 [[543_nfs_network_file_system|NFS]] 서버의 익스포트 [[009_config|설정]](`/etc/exports`)에는 반드시 **`root_squash` (루트 짓누르기)** 옵션이 기본으로 활성화되어 있다. 이 옵션이 켜져 있으면 클라이언트에서 당당하게 UID 0(root)으로 접근해도, [[543_nfs_network_file_system|NFS]] 서버가 문지기에서 그 신분을 무권한 유령 계정인 `nobody(UID 65534)`로 강등(Squash)시켜 버려 루트 권한 해킹의 싹을 잘라버린다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 네트워크 파일 공유 프로토콜 도입 아키텍트 결정 트리           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 여러 대의 머신이 스토리지 하나를 공유해야 한다 ]                        │
  │                │                                                  │
  │                ▼                                                  │
  │      공유할 클라이언트들이 주로 Windows OS 중심의 사무 환경인가?             │
  │          ├─ 예 ─────▶ [ SMB / CIFS (Samba) 채택 ]                   │
  │          │             (윈도우 AD 인증과 완벽 호환, Stateful 구조)         │
  │          └─ 아니오 (Linux/UNIX 중심의 백엔드 서버 팜 환경이다)             │
  │                │                                                  │
  │                ▼                                                  │
  │      하나의 파일에 여러 서버가 동시에 쓰기(Write)를 시도하여 락 관리가 필수인가? │
  │          ├─ 아니오 ──▶ [ NFS v3 채택 가능 ]                           │
  │          │             (가볍고 무상태의 탄력성으로 정적 미디어 서빙 등에 적합)    │
  │          │                                                        │
  │          └─ 예 ─────▶ [ NFS v4 채택 강제! ]                           │
  │                        - TCP 단일 포트로 클라우드 방화벽(VPC) 구성 용이      │
  │                        - 파일 락(Lease) 내장으로 동시 수정 꼬임 원천 방어    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 수많은 클라우드 초보자들이 AWS 환경에서 NAS를 붙일 때 보안 그룹([[690_firewall_generation_evolution|방화벽]]) 규칙이 자꾸 막혀서 며칠을 밤샌다. 그 원인은 구형 [[543_nfs_network_file_system|NFS]] v3가 rpcbind를 쓰느라 접속할 때마다 동적 [[446_port_and_bus|포트]](랜덤 [[446_port_and_bus|포트]])를 수만 개씩 열어대기 때문이다. 현대 클라우드 [[690_firewall_generation_evolution|방화벽]]([[283_security_tactics|Security]] Group)에서 동적 [[446_port_and_bus|포트]]를 여는 것은 미친 짓이다. 따라서 인프라 아키텍트는 묻지도 따지지도 않고 [[446_port_and_bus|포트]] 2049 하나만 얌전하게 쓰는 [[543_nfs_network_file_system|NFS]] v4를 표준으로 강제해야 클라우드 네트워크 아키텍처와 평화롭게 공존할 수 있다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[543_nfs_network_file_system|NFS]] 위에 관계형 [[002_database_definition|데이터베이스]](DB) 설치**: MySQL [[001_dikw_pyramid|데이터]] 폴더(`/var/lib/mysql`)를 [[543_nfs_network_file_system|NFS]] [[516_mount_mechanism|마운트]] 경로로 잡아두는 엽기적인 행위. RDBMS의 생명은 [[501_file_definition_logical_record|파일]] 시스템의 `fsync()` 시스템 콜을 통한 동기적 로컬 디스크 기록(물리적 락)에 있다. 이것을 핑퐁 치는 네트워크 너머의 NFS로 보내면, 미세한 패킷 로스나 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]]) 한 방에 DB의 전체 [[191_transaction_concept_states|트랜잭션]] 성능이 나락으로 떨어지며, [[501_file_definition_logical_record|파일]] 락 꼬임으로 DB 인덱스가 통째로 깨져버리는(Corruption) 최악의 재앙을 겪게 된다. DB는 무조건 블록 스토리지(EBS, 로컬 [[482_nvme|NVMe]])에 올려야 한다.

- **📢 섹션 요약 비유**: 수류탄([[002_database_definition|데이터베이스]]) 핀을 뽑아서 직접 조심조심 땅에 내려놓지 않고, 저격수 10명이 총을 쏘고 있는 전장(네트워크망)을 가로질러 택배 기사([[543_nfs_network_file_system|NFS]])에게 "저기 옆 벙커에 내려놔 줘"라고 심부름을 시키는 꼴입니다. 택배 기사가 총에 맞고 쓰러지면 수류탄은 내 진영에서 폭발합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 각자 로컬 디스크 구성 시 | 중앙 집중형 [[543_nfs_network_file_system|NFS]] 클러스터 구성 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (스토리지 낭비)** | 100대 서버에 똑같은 [[001_dikw_pyramid|데이터]] 100벌 복사 | 1대 스토리지에 원본 저장 후 100대 [[516_mount_mechanism|마운트]] | 스토리지 물리 볼륨 구매 비용 99% 절감 |
| **정량 (수평 확장, [[202_scale_out_distributed_horizontal_expansion|Scale-out]])**| 웹 서버 추가 시 이미지 [[501_file_definition_logical_record|파일]] 복제에 수 시간 소요| [[516_mount_mechanism|마운트]] [[158_instruction|명령어]] 한 줄로 1초 만에 [[001_dikw_pyramid|데이터]] 연동 | Auto-Scaling 봇(Bot)을 통한 무한 [[571_resiliency_fault_tolerance_patterns|탄력성]] 확보 |
| **정성 ([[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]])** | A서버에서 바꾼 프로필 사진 B서버에선 안 보임 | 100대 서버가 항상 100% 동일한 [[501_file_definition_logical_record|파일]] 뷰 보유 | [[136_variance|분산]] 웹 아키텍처의 상태 공유([[160_session_controlling_terminal|Session]]/[[501_file_definition_logical_record|File]]) 난제 극복 |

### 미래 전망
- **pNFS (Parallel [[543_nfs_network_file_system|NFS]])**: 1대의 [[543_nfs_network_file_system|NFS]] 서버가 주는 중앙 병목 한계를 부수기 위해, [[203_metadata_management|메타데이터 관리]] 서버와 수십 대의 [[001_dikw_pyramid|데이터]] 저장 서버를 분리해, 클라이언트가 여러 대의 서버에 '[[430_index_fast_full_scan|병렬]]'로 동시에 [[001_dikw_pyramid|데이터]]를 쏟아붓는 pNFS 기술이 엔터프라이즈 빅데이터 및 [[548_automotive_hpc|HPC]](슈퍼컴퓨팅) I/O 표준의 구원투수로 자리 잡았다.
- **[[136_variance|분산]] [[494_object_storage|오브젝트 스토리지]](S3)와의 융합**: 레거시 [[543_nfs_network_file_system|NFS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 자체는 너무 무겁고 느려서 클라우드 네이티브에서 버림받는 추세였다. 하지만 최근 AWS Storage Gateway나 S3 [[501_file_definition_logical_record|File]] Gateway처럼, "유저가 [[543_nfs_network_file_system|NFS]] [[516_mount_mechanism|마운트]]로 던지면, 뒷단에서는 캐시를 거쳐 [[494_object_storage|오브젝트 스토리지]](S3) 버킷으로 무한정 번역해 집어넣어 주는" 융합 게이트웨이가 탄생하며 레거시 앱과 최신 클라우드의 다리 역할을 훌륭히 수행 중이다.

### 참고 표준
- **[[635_ietf_core_working_group_coap|IETF]] RFC 7530 (NFSv4.1)**: [[690_firewall_generation_evolution|방화벽]] 뚫기 더러웠던 v3를 폐기하고 단일 [[446_port_and_bus|포트]] 통신, [[456_caching|캐싱]], [[160_session_controlling_terminal|세션]] 기반의 [[501_file_definition_logical_record|파일]] 락(Delegation) 기능을 떡칠하여 인터넷 스케일로 키워낸 인터넷 국제 표준 규격.
- **[[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]])**: 이기종 OS, 이기종 CPU 환경에 상관없이 [[074_byte|바이트]] 순서(엔디안)를 [[127_xdr_external_data_representation|XDR]]([[127_xdr_external_data_representation|External Data Representation]])로 직렬화하여 함수를 원격 호출하게 해주는 NFS의 영원한 영혼의 파트너 표준.

네트워크 [[501_file_definition_logical_record|파일]] 시스템([[543_nfs_network_file_system|NFS]])은 "네트워크라는 불안정하고 시끄러운 골목길" 위에 "로컬 디스크라는 가장 조용하고 안전한 환상"을 강제로 덮어씌운 대담한 발명품이다. 상태를 기억하지 않겠다는 단호한 철학([[239_stateless_redis|Stateless]]) 덕분에 랜선이 뽑히고 서버 전원이 나가도 [[001_dikw_pyramid|데이터]] 전송은 끈질기게 생명력을 이어갈 수 있었다. 비록 현대 클라우드에서는 화려한 [[494_object_storage|오브젝트 스토리지]](S3)에 스포트라이트를 뺏겼지만, 지금 이 순간에도 수천 대의 [[136_variance|분산]] 서버들이 뱉어내는 끈적한 [[009_config|설정]] [[501_file_definition_logical_record|파일]]과 소스 코드를 묵묵히 하나로 묶어주고 있는 인프라의 위대한 접착제다.

- **📢 섹션 요약 비유**: 각자 자기 수첩(로컬 디스크)에 숙제를 적고 매일 모여서 서로 베껴 쓰는 비효율([[212_synchronization_mechanisms|동기화]] 지옥)을 없애고, 반 친구 100명이 동시에 칠판([[543_nfs_network_file_system|NFS]] 서버) 하나를 뚫어져라 쳐다보며 즉시 지우고 고쳐 쓰는 완벽한 공유 오피스의 진화입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 다중 큐 [[327_ssd|SSD]] [[482_nvme|NVMe]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 장점 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[494_object_storage|오브젝트 스토리지]] [[012_metadata|메타데이터]] 분리 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[514_partition_slice_volume|파티션]] [[515_mbr_vs_gpt|MBR]] [[302_gpt_autoregressive|GPT]] 크기 제한 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[052_cloud_computing_os|클라우드 컴퓨팅]] OS [[638_resource_pooling_cxl|자원 풀링]] | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[오브젝트 스토리지 메타데이터 분리]
    │
    ▼
[네트워크 파일 시스템 (NFS) 무상태 (Stateless)]
    │
    ├──▶ [파티션 MBR GPT 크기 제한]
    └──▶ [클라우드 컴퓨팅 OS 자원 풀링]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 맨날 무거운 일기장([[001_dikw_pyramid|데이터]])을 가방에 넣고 학교랑 집을 왔다 갔다 하느라 허리가 부러질 뻔했어요.
2. 그래서 똑똑한 철수는 일기장을 튼튼한 '마을 중앙 창고([[543_nfs_network_file_system|NFS]] 서버)'에 딱 하나만 놔두고, 학교 책상 서랍이랑 집 책상 서랍을 '마법의 터널([[516_mount_mechanism|마운트]])'로 창고랑 몰래 연결했어요!
3. 이제 철수는 학교든 집이든 빈 서랍을 쓱 열기만 하면 마법 터널을 통해 중앙 창고의 일기장이 바로 튀어나와서 아주 편하게 일기를 쓸 수 있게 된 거랍니다!
