+++
title = "773. 오브젝트 스토리지 메타데이터 분리 (Object Storage Metadata Decoupling)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) ([Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/))는 기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 깊은 폴더-트리 구조나 블록 디스크의 조각 방식(섹터)을 버리고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>단일한 통짜 덩어리(Object)와 꼬리표(고유 ID), 그리고 풍부한 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a>) 묶음으로 평평하게(Flat) 관리하는 아키텍처</strong>다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 저장되는 물리적 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Pool)'과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 위치/[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 검색하는 '[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 공간([Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) Server)'을 아키텍처적으로 완벽히 쪼개어(분리), 수십 페타바이트(PB) 규모로 무한정 늘어나는 클라우드 환경에서 폴더 검색 병목 없이 선형적인 확장성(Scalability)을 보장한다.
> 3. **융합**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 고전적 [VFS](/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 트리 구조가 인터넷 스케일에서 한계에 부딪히자, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)(S) 기반의 [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)(DHT)이 결합되어 AWS S3, Ceph와 같은 현대 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 애플리케이션의 절대적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 댐으로 진화했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 사진, 영상, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 등 크기가 다양하고 수정할 일이 거의 없는 비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하는 데 특화된 스토리지다.
  - [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 3가지로 구성된다: ① <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 본체</strong> (사진 그 자체) ② <strong>고유 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">식별자</a> ID</strong> (해시값처럼 고유한 이름) ③ <strong>확장 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> ("이 사진은 2026년 철수가 찍은 고양이 사진" 등 텍스트 태그).

- **필요성(문제의식)**: 
  - 전통적인 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템([NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/), [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/))은 폴더 안에 폴더를 넣는 트리(Tree) 계층 구조다. 
  - 사진이 100만 장일 땐 괜찮지만, 클라우드에 100억 장이 쌓이면? C드라이브에서 `\Users\photo\2026\cat.jpg` 를 찾느라 폴더 테이블을 5번씩 뒤져야 하고, 트리 구조를 관리하는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서버가 과부하로 터져버린다.
  - 블록 스토리지([SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))는 빠르지만 서버에 직접 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)해야 해서 여러 대의 웹 서버가 동시에 공유하기 까다롭고, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(작성자 등)을 남기기 어렵다.
  - **해결책**: "폴더의 벽을 다 허물고 거대한 광장(Flat)에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 던져두자. 대신 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 '고유한 일련번호(ID)'를 붙이고, 그 번호만 치면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어느 대륙의 어느 서버에 있든 한 번에([REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)) 꺼내 주자!"

  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 (폴더 구조)</strong>: 도서관에서 책을 찾을 때, '3층 -> 과학 섹션 -> 물리 책장 -> 3번째 선반' 순서대로 계단을 오르내리며 찾아가야 하는 빡빡한 구조. (책이 너무 많아지면 미로가 됨).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">오브젝트 스토리지</a></strong>: 자동차 발레파킹(Valet Parking) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/). 차([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 맡기면 직원이 차를 어디 주차장 구석에 댔는지 나는 알 필요가 없다. 그냥 받은 '플라스틱 번호표(오브젝트 ID)'만 건네주면, 직원이 알아서 1분 만에 차를 내 앞에 대령해 준다.

- **등장 배경**: 
  - 2006년 아마존이 AWS S3 (Simple Storage [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 출시하며 "어떤 양의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)든 저장하고 검색할 수 있는 인터넷 스토리지" 개념을 대중화시켰고, 넷플릭스, 페이스북 등의 미디어 폭발을 견뎌낸 뼈대가 되었다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 파일 스토리지 트리 구조 vs 오브젝트 스토리지 플랫 구조   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ 전통적 파일 스토리지 (Hierarchical Tree) - NAS ]               │
  │   / (Root)                                                  │
  │   ├── app/                                                  │
  │   └── var/                                                  │
  │       └── www/                                              │
  │           └── images/                                       │
  │               └── cat.jpg  ◀ 여기까지 찾느라 디스크 메타데이터 5번 읽음 │
  │   ※ 파일이 10억 개가 넘어가면 뼈대(Directory Tree) 관리가 붕괴함.       │
  │                                                             │
  │  [ 오브젝트 스토리지 (Flat Address Space) - S3 ]                  │
  │   거대한 하나의 버킷(Bucket) 평면:                                 │
  │   [ID: 1A2B] (cat.jpg) (태그: 귀여움, 2026년생)                  │
  │   [ID: 9F8D] (dog.mp4) (태그: 강아지, 해상도4k)                  │
  │   [ID: 3E7C] (log.txt) (태그: 시스템로그)                       │
  │                                                             │
  │   ※ 검색: GET https://s3.cloud.com/bucket/1A2B                │
  │   ※ 결과: ID 1A2B 해시값을 계산해 해당 서버로 직행. (디렉터리 탐색 비용 0) │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지는 인간의 뇌가 분류하기 편하게 만들어진 인위적 계층이다. 반면 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 오로지 기계([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))가 무한대로 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))하기 편하게 만들어진 평면(Flat) 우주다. 폴더 구조가 없기 때문에 상위 폴더를 잠그고 푸는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합이 원천적으로 소멸한다. 오브젝트 ID(보통 해시값)만 알면 내부 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 의해 이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 한국 서버에 있는지 미국 서버에 있는지 단 한 번의 연산으로 찾아낸다. 따라서 스토리지 용량이 페타바이트 단위로 무한정 늘어나도 검색 속도가 느려지지 않는 완벽한 선형 확장이 가능하다.

- **📢 섹션 요약 비유**: 서랍장에 양말, 팬티 칸을 나눠서 예쁘게 정리(폴더)하다가 옷이 만 벌이 되면 서랍을 열지도 못하고 무너집니다. 차라리 거대한 창고 바닥(플랫)에 옷을 쫙 깔아두고, 옷마다 삐삐(번호표)를 달아놔서 번호만 누르면 옷이 소리치게 만드는 게 무한 창고의 관리법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 노드의 완전 분리 (Decoupling) 아키텍처

[오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)가 페타바이트 확장을 견디는 핵심 비밀은 아키텍처의 분업화에 있다. 

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 오브젝트 스토리지의 메타데이터 / 데이터 분리 모델           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 클라이언트 앱 (웹 브라우저, 백엔드 서버) ]                         │
  │         │  1. "사진(ID: 777) 어딨어?" (REST API)                    │
  │         ▼                                                         │
  │   ┌───────────────────────────────────────────────┐               │
  │   │  MDS (Metadata Server Node / 분산 해시 라우터) │ ◀ 가볍고 빠름  │
  │   │  "ID 777은 OSD-3번 노드의 디스크 5번에 있어!"      │               │
  │   └────────────────────┬──────────────────────────┘               │
  │                        │ 2. 주소 힌트 획득                         │
  │   [ 클라이언트가 직접 OSD로 요청 쏘기 ] ◀ 핵심: MDS를 거쳐서 다운받지 않음! │
  │         │                                                         │
  │         ▼ 3. "OSD-3아, 사진 파일 내놔!"                            │
  │   ┌───────────────────────────────────────────────┐               │
  │   │  OSD (Object Storage Daemon / Data Node)      │ ◀ 무겁고 큼   │
  │   │  [ 디스크 1 ] [ 디스크 2 ] [ 디스크 5 (ID 777) ] │               │
  │   └───────────────────────────────────────────────┘               │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 고전적인 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버([NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/))는 관리 서버가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 찾아서 "자신의 네트워크 대역폭을 통해" 클라이언트에게 전달해 줬다. 사용자가 몰리면 관리 서버의 네트워크가 터진다([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/)). 반면 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 관리 서버([MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/))와 짐꾼 서버(OSD)를 철저히 찢었다. 클라이언트는 가벼운 MDS에게 "어딨어?"라는 주소만 묻고, 무거운 사진 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 다운로드는 주소를 알아낸 뒤 OSD 짐꾼 노드와 직접([Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) 1:1 통신을 뚫어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받아간다. 덕분에 짐꾼 노드(디스크)를 100대, 1000대 병렬로 늘려도 트래픽이 1000갈래로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되므로 절대 중앙 병목이 오지 않는 궁극의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처가 실현된다.

### 풍부한 확장 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) (Rich [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))

기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 고작 `생성일`, `수정일`, `권한` 정도의 깡통 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)만 줬다.
[오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 옆에 무제한의 [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 형태 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 찰싹 붙일 수 있다.
- 예: 영상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`ID: 123`) $\rightarrow$ [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/): `{"patient_id": "P001", "type": "X-ray", "disease": "covid19"}`
- 이 태그 덕분에 수십 억 개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 중 "코로나19 X-ray 사진만 다 찾아와!"라는 검색이 일반 RDBMS를 검색하듯 빠르고 자유롭게 이루어진다.

- **📢 섹션 요약 비유**: 도서관 사서([MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/))가 무거운 책을 직접 꺼내서 내 책상까지 배달해 주다 허리가 부러지는 대신, 사서는 "3층 B구역 5번 책장"이라는 쪽지(주소)만 1초 만에 적어주고, 나는 쪽지를 들고 직접 책장(OSD)으로 뛰어가 책을 빼오는 분업 시스템입니다.

---

## Ⅲ. 비교 및 연결

### 스토리지 3대장 (Block vs [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) vs Object) 총정리

현대 IT 인프라 아키텍트는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 특성에 맞춰 가장 적절한 스토리지를 골라 써야 한다.

| 비교 항목 | 블록 스토리지 (Block / [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) / EBS) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 ([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) / [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) / EFS) | [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) (Object / S3 / Ceph) |
|:---|:---|:---|:---|
| **저장 형태** | 쌩 디스크의 원시([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) 조각 | [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 폴더와 트리 구조 | 납작한 버킷(Bucket) 안의 ID 태그 객체 |
| **수정 방식** | 특정 구역(1바이트)만 **부분 수정 가능** | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 일부 열어서 덮어쓰기 가능 | **부분 수정 절대 불가!** 무조건 통째로 덮어쓰거나 지워야 함 ([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) |
| <strong>통신 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>| [iSCSI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/698_iscsi/), 파이버 채널 (로컬 장착용) | [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/), SMB/CIFS (로컬망 공유용) | <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> / <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/">REST API</a> (인터넷 인터넷 공유용)</strong> |
| **적합한 앱** | OS 루트 드라이브, 부팅 디스크, 오라클 DB 엔진 | 팀 문서 공유, 레거시 CMS 웹하드 | 이미지/영상 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 아카이브, 정적 웹호스팅 |

### 과목 융합 관점

- <strong>네트워크 구조 (HTTP와 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/">REST API</a>)</strong>: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 커널의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템([VFS](/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) 명령어를 쓰지 않는다. `PUT /bucket/cat.jpg`, `GET /bucket/cat.jpg` 같은 순수한 웹 통신([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))으로 동작한다. 따라서 방화벽을 뚫기 쉽고, 자바스크립트나 모바일 앱에서 서버 백엔드(Node.js 등)를 거치지 않고 S3 스토리지로 직접 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 던져버리는 클라우드 프론트엔드 다이렉트 업로드가 가능하다.
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> (이레이저 코딩, <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/">Erasure Coding</a>)</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 100PB일 때, 디스크 고장에 대비해 통째로 복사본을 3개 만들면([Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) 300PB가 되어 비용이 미쳐 날뛴다. 그래서 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조각조각 낸 뒤 수학적 연산을 더한 패리티(Parity) 조각을 만들어 여러 노드에 흩뿌린다. 디스크 2~3대가 박살 나도 남은 조각의 수학 공식을 풀어 원본을 복원하는([RAID 5](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/)/6의 네트워크 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)) 극한의 비용 절감 스토리지 기술을 내장하고 있다.

- **📢 섹션 요약 비유**: 블록 스토리지가 흙과 시멘트를 파는 '건축 자재상'이고, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지가 가구가 잘 정리된 '원룸 오피스텔'이라면, [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 택배 기사가 짐을 던져두고 송장 번호만 붙여놓는 거대한 '아마존 물류 창고'입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 트러블슈팅

1. **시나리오 — SNS 이미지 서버의 디스크 I/O와 네트워크 트래픽 이중 병목**: 인스타그램 같은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). Nginx 웹 서버의 로컬 하드 디스크에 수백만 장의 이미지를 폴더별로 저장해 뒀다. 사용자가 이미지를 요청하면 Nginx가 디스크에서 읽어 네트워크로 쏴주는 바람에 웹 서버의 CPU, 디스크, 대역폭이 모조리 터져나가서 앱 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출조차 안 먹힌다.
   - <strong>아키텍트 판단 (S3 <a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/">Offloading</a> 아키텍처)</strong>: "동적 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 로직"과 "정적 미디어 서빙"을 뼈와 살을 바르듯 완벽히 분리해야 한다. 앱 서버는 단지 DB에 "저 사진은 `https://s3.../123.jpg`에 있다"는 텍스트(URL [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))만 저장하고 빠진다. 사용자의 브라우저나 스마트폰은 앱 서버를 괴롭히지 않고, 저 URL을 타고 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3)나 CDN으로 직행하여 이미지를 퍼간다. 웹 서버의 디스크 I/O 병목이 0으로 수렴하는 모던 백엔드의 알파이자 오메가다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">오브젝트 스토리지</a>에 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>를 실시간으로 쓰려는 행위</strong>: 주니어 개발자가 "S3는 용량이 무제한이니까 싸네!"라며 웹 서버의 실시간 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`app.log`)의 기록 목적지를 S3 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 툴(s3fs 등)을 이용해 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)로 잡아버렸다. 5분 만에 서버가 뻗었다.
   - **원인 분석**: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 "일부분 덮어쓰기(Append/Update)"를 지원하지 않는다. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 "에러 발생"이라는 10바이트 한 줄을 추가하려면, S3는 뒤에서 기존 1GB짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 통째로 다운받아 10바이트를 더한 뒤 다시 1GB 통째로 업로드하는 끔찍한 오버헤드(Rewrite)를 발생시킨다. 게다가 '[결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))' 때문에 방금 쓴 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽어도 옛날 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 나올 수 있다.
   - **아키텍트 판단 (티어링 아키텍처 재설계)**: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 "한 번 쓰고 영원히 읽기만 하는([WORM](/knowledge-base/studynote/02_operating_system/10_security/590_worm/) - Write Once, Read Many)" 차가운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에만 써야 한다. 실시간 핫(Hot) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 로컬 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 블록 스토리지나 [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)(MQ)에 빠르게 밀어 넣고, 자정에 크론([Cron](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/)) 배치가 돌아 하루 치 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 1개의 거대한 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.gz) 덩어리로 예쁘게 뭉쳐서 S3로 던지는 [스토리지 티어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/674_storage_tiering/)(Tiering) 아키텍처로 뜯어고친다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 클라우드 스토리지 선택을 위한 아키텍트 결정 트리           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 서비스에서 새로운 데이터를 저장할 공간이 필요하다 ]                    │
  │                │                                                  │
  │                ▼                                                  │
  │      데이터의 일부만 계속 빈번하게 수정되는가? (예: DB 파일, 실시간 로그)      │
  │          ├─ 예 ─────▶ [ 블록 스토리지 (Block / AWS EBS) ]           │
  │          │             (초고속 랜덤 액세스 및 로컬 마운트 지원)            │
  │          └─ 아니오 (한 번 저장하면 수정 없이 읽기만 함)                  │
  │                │                                                  │
  │                ▼                                                  │
  │      여러 대의 리눅스 서버(EC2)가 동시에 디렉터리로 마운트해서 파일처럼 써야 하나?│
  │          ├─ 예 ─────▶ [ 네트워크 파일 시스템 (NAS / AWS EFS) ]       │
  │          │             (POSIX 파일 락 호환성 지원, 레거시 앱 이전 용이)     │
  │          │                                                        │
  │          └─ 아니오 ──▶ [ 오브젝트 스토리지 (S3 / Ceph) 🚀 ]           │
  │                        - 용량 무제한, 가장 저렴한 비용, 극강의 내구성       │
  │                        - REST API로만 접근! (파일 수정 불가/Immutable)│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "S3가 싸니까 전부 거기로 넣자"는 재앙의 지름길이다. 아키텍트는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 온도(Hot, Warm, Cold)와 성질(Mutable, [Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/))을 파악해야 한다. S3는 무한한 우주 창고지만, 문이 아주 무겁다. 계속 열었다 닫았다 하면서 안의 물건을 꼼지락대면 손가락이 부러진다. 하지만 1TB짜리 거대한 바윗덩이를 한 번에 밀어 넣고, 나중에 꺼내서 구경만 하는 용도로는 지구상에서 이보다 싸고 안전한 시스템은 없다 (내구성 Eleven 9s - 99.999999999%).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **S3 버킷 안에 무의미한 폴더 흉내 내기 남용**: S3는 폴더 개념이 없다. 단지 키([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 이름이 `2026/03/cat.jpg` 처럼 슬래시(/)를 포함한 긴 문자열일 뿐이다. 그런데 마치 일반 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)처럼 쓰겠다고 S3 객체를 일일이 `list_dir()` API로 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 호출하며 트리 탐색 로직을 짜면 엄청난 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 과금(돈)과 지연을 맞고 파산한다. [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)를 다룰 때는 절대 "폴더 경로"로 검색하지 말고, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(RDS, [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/))에 S3 키 매핑 테이블을 만들어두고 DB에서 검색한 뒤 딱 한 방에 S3에서 끄집어내는 아키텍처를 세워야 한다.

- **📢 섹션 요약 비유**: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 물건을 찰흙처럼 주물럭거리며 모양을 바꾸는(수정) 도자기 공방(블록 스토리지)이 아닙니다. 이미 완벽하게 구워진 도자기를 유리 상자에 예쁘게 담아 영원히 보관만 하는 거대한 미술관 수장고([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/))로 다뤄야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 레거시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 ([NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)) | [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 시스템 (S3) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (용량 확장성)** | 디스크 최대 볼륨 크기(예: 100TB) 한계 직면 | 페타/엑사바이트(PB/EB) 무한 증설 | 스토리지 용량 추가 설계 불필요 (무한 [Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) |
| <strong>정량 (검색/응답 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>)</strong>| 뎁스가 10개인 폴더 내 탐색 시 I/O 병목 | Flat 구조로 O(1) 수준의 단일 접근 | 10억 개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 속에서도 레이턴시 증가 0 수렴 |
| <strong>정성 (앱 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/">결합도</a>)</strong> | 서버의 OS [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 및 물리적 경로에 종속됨 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) URL만 있으면 세상 어디서든 접근 | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) 및 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), 글로벌 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 서빙의 기본 토대 확립 |

### 미래 전망
- <strong>S3 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/">Select</a> 및 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 오프로드</strong>: 단순 [WORM](/knowledge-base/studynote/02_operating_system/10_security/590_worm/) 스토리지를 넘어 진화 중이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1TB 덩어리 안에서 1MB의 텍스트만 필요할 때 옛날엔 1TB를 다 다운받아 파싱해야 했지만, 이제는 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 내부 노드(OSD)에서 직접 SQL(`SELECT`)을 실행하여 필요한 1MB만 필터링해서 뱉어주는 '똑똑한 스토리지 연산 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)' 기능이 빅데이터 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))의 핵심으로 떠올랐다.
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 오브젝트 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a> (Alluxio, MinIO)</strong>: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 학습 서버([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))가 S3에 있는 페타바이트급 이미지를 끌어오려다 네트워크 병목에 죽는 문제를 막기 위해, 컴퓨팅 노드들 바로 옆 메모리에 S3의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리를 잘게 쪼개어 계층화 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)해 두는 가상 [분산 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/) 기술이 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인프라의 미싱 링크를 이어주고 있다.

### 참고 표준
- <strong>Amazon S3 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/">REST API</a></strong>: 공식 표준 기구가 만든 건 아니지만, 전 세계 모든 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(Ceph, MinIO, GCP, Azure)가 100% 호환성을 맞추기 위해 강제로 따르고 있는 **실질적 업계 표준(De facto Standard)** 규격.
- <strong>Ceph CRUSH <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 중앙 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서버의 병목조차 허용하지 않기 위해, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이름만 알면 수학적 [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)(CRUSH)로 저장될 물리 디스크 위치를 즉시 계산해 내어 서버 1만 대 규모에서도 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))을 없앤 극한의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/).

[오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 인류가 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정리 정돈하려는 강박"을 쿨하게 포기하고, 대신 "무식하게 바닥에 쏟아버리고 태그([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))라는 강력한 꼬리표만 달자"는 새로운 우주관을 채택한 결과물이다. 계급과 폴더 트리의 벽이 허물어진 이 평평한(Flat) 정보의 바다 덕분에, 넷플릭스의 영상, 스포티파이의 음악, 틱톡의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들은 전 세계 클라우드를 타고 우리 곁으로 1초 만에 배달될 수 있었다. 이는 곧 계층적 질서(Tree)의 종말이자, 무한대로 뻗어나가는 해시(Hash) 기반 융합 아키텍처의 찬란한 승리다.

- **📢 섹션 요약 비유**: 수만 명의 군인을 1소대, 2중대, 3대대(폴더 트리)로 나누어 보고 체계를 거치게 하면 명령 전달에 하루가 걸립니다. 하지만 장군(웹서버)이 마이크([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 잡고 "군번 1234번 철수, 앞으로 나와!"(오브젝트 호출)라고 직접 방송해 버리면 군인이 100만 명이라도 1초 만에 튀어나올 수 있는 완벽한 직접 소통 체계입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/) [마모 평준화](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) ([Wear Leveling](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 다중 큐 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 장점 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [네트워크 파일 시스템](/knowledge-base/studynote/02_operating_system/11_exam_summary/774_nfs_stateless_network_file_system/) ([NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)) 무상태 ([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 크기 제한 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[다중 큐 SSD NVMe 프로토콜 장점]
    │
    ▼
[오브젝트 스토리지 메타데이터 분리 (Object Storage Metadata Decoupling)]
    │
    ├──▶ [네트워크 파일 시스템 (NFS) 무상태 (Stateless)]
    └──▶ [파티션 MBR GPT 크기 제한]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전통 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 보물([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 찾으려면 '아시아 대륙 $\rightarrow$ 한국 $\rightarrow$ 서울 $\rightarrow$ 철수네 집 $\rightarrow$ 서랍장' 지도를 5번이나 보고 찾아가야 해서 너무 느려요.
2. [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 커다란 마법의 운동장(플랫 구조)이에요. 100만 개의 보물을 그냥 휙휙 던져두고, 각 보물에 '비밀번호(ID)'만 달아놨어요.
3. 우리가 "비밀번호 777번 보물!" 하고 외치면([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청), 운동장 어디에 있든 1초 만에 슝~ 하고 내 손으로 날아오니까 아무리 보물이 많아져도 속도가 똑같이 엄청 빠르답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 773 / 800

← **이전**: [772. 다중 큐 SSD NVMe 프로토콜 장점 (Multi Queue SSD NVMe Protocol)](/knowledge-base/studynote/02_operating_system/11_exam_summary/772_multi_queue_ssd_nvme_protocol/)
**다음**: [774. 네트워크 파일 시스템 (NFS) 무상태 (Stateless)](/knowledge-base/studynote/02_operating_system/11_exam_summary/774_nfs_stateless_network_file_system/) →

---
