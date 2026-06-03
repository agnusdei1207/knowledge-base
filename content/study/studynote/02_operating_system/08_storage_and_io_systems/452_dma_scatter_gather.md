---
title: 452. DMA 산란-수집 (Scatter-Gather) - 불연속적 물리 메모리 블록을 한 번의 DMA로 전송
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[164_scattering_reflection_radio_waves|산란]]-수집(Scatter-Gather) DMA는 램(RAM)의 물리적 주소가 4KB [[286_page_frame|페이지]] 단위로 갈기갈기 찢어져 있을 때, 디스크나 랜카드에서 대용량 [[001_dikw_pyramid|데이터]]를 퍼와 **여러 개의 찢어진 물리 프레임에 알아서 흩뿌리거나(Scatter), 흩어진 [[001_dikw_pyramid|데이터]]들을 한 번에 모아서(Gather) 전송해 주는 고도화된 지능형 하드웨어 I/O 기술**이다.
> 2. **가치**: 기존 DMA처럼 "물리적으로 연속된 램 주소"를 억지로 만들어주기 위해 시스템을 멈추고 램 조각모음([[347_compaction|Compaction]])을 하거나 쓸데없는 램 복사(Bounce [[454_buffering|Buffering]])를 할 필요를 100% 소거하여, **[[381_virtual_memory|가상 메모리]]([[259_paging|페이징]]) 아키텍처와 [[746_io_direct_memory_access_dma|DMA]] 하드웨어 간의 치명적 충돌을 우주 끝까지 해결해 낸다.**
> 3. **융합**: 운영체제가 **"여러 개의 [[323_physical_address|물리 주소]] 조각들이 적힌 목록표(Scatter-Gather List)"**를 메모리에 던져주면, [[746_io_direct_memory_access_dma|DMA]] 칩셋이 이를 스스로 읽어가며 CPU [[016_interrupt_mechanism|인터럽트]] 단 1회만으로 기가바이트의 쪼개진 램 전송을 완수하는 **HW-SW 리스트 파싱 융합의 정점**이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 일반 DMA는 "100번지부터 연속으로 12KB 쏴라"라는 1차원적 명령만 알아듣는다. 하지만 Scatter-Gather(S-G) DMA는 "이 주소록([[056_linked_list|Linked List]])을 보고, 10번지에 4K, 80번지에 4K, 150번지에 4K 흩어 뿌려라"라는 복합 명령을 수행할 지능을 가진 하드웨어 칩셋이다. 디스크에서 램으로 부을 땐 Scatter([[164_scattering_reflection_radio_waves|산란]]), 램 조각들을 긁어서 랜카드로 쏠 땐 Gather(수집)라고 부른다.
- **필요성**: [[259_paging|페이징]] 시스템의 기본 철학은 "가상 주소만 12KB 이어져 있으면, 진짜 물리 램은 1번 프레임, 8번 프레임, 90번 프레임으로 찢어져(파편화) 있어도 노상관!"이다. 하지만 하드웨어 DMA는 가상 주소([[328_mmu|MMU]])를 이해하지 못하는 깡통이다. 12KB의 덩어리 패킷이 들어오면 그걸 찢어서 넣을 능력이 없어 연속된 물리 램 12KB를 요구한다. 하지만 서버가 오래 돌다 보면 [[342_external_fragmentation|외부 단편화]] 때문에 연속된 물리 램 12KB를 찾을 수가 없다. OS가 억지로 램 조각들을 모으느라 서버를 일시 정지([[370_memory_compaction|Memory Compaction]])시키는 대재앙이 터졌다. "아니, 그냥 배달원([[746_io_direct_memory_access_dma|DMA]])한테 여러 군데 주소를 적어주고 알아서 조각내서 배달해달라고 하면 안 돼?"라는 뼈저린 효율성의 요구가 S-G 칩셋을 탄생시켰다.

- **등장 배경 및 구시대의 꼼수 박살**:
  1. **바운스 버퍼(Bounce Buffer)의 한계**: 옛날엔 OS가 연속된 '[[022_kernel_role|커널]] 전용 버퍼' 12KB에 일단 DMA로 [[001_dikw_pyramid|데이터]]를 받고, 그걸 CPU가 찢어진 유저 램에 포문 돌며 일일이 복사(Memcpy)해 주는 노가다를 뛰었다. (속도 반토막).
  2. **Zero-Copy의 절대적 열망**: CPU 100% 점유율을 만드는 저 멍청한 메모리 복사를 없애려면, 랜카드 하드웨어가 직접 찢어진 유저 램으로 쏴주는 수밖에 없었다.
  3. **하드웨어의 진화**: 칩셋 벤더들이 램에서 '[[056_linked_list|연결 리스트]] 장부'를 직접 읽고 파싱할 수 있는 마이크로컨트롤러를 랜카드와 디스크 제어기에 탑재하며 문제가 완전히 해결되었다.

```text
┌───────────────────────────────────────────────────────────────────────────┐
│        일반 DMA vs Scatter-Gather DMA의 메모리 맵핑 시각화                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ [ 상황: 12KB 파일(4KB * 3장)을 디스크에서 RAM으로 로드해야 함 ]           │
│ * 물리 램(RAM)은 파편화되어 [방1] [방8] [방90] 3곳만 비어있음.            │
│                                                                           │
│ ▶ 1. 낡은 일반 DMA (연속 메모리 강박증)                                   │
│   OS: "DMA야, 12KB 퍼와."                                                 │
│   DMA: "물리적으로 연속된 12KB 빈방 없는데? 나 못해 (Error!)"             │
│   OS: 💦 눈물을 머금고 기존 앱들을 멈추고 램 12KB를 한 곳으로 쫙 미는     │
│       압축(Compaction) 노가다를 수 초간 진행 후 다시 DMA 시킴 (지옥)      │
│                                                                           │
│ ▶ 2. 구원자 S-G DMA (가상 메모리의 찰떡궁합)                              │
│   OS: "DMA야, 여기 [방1, 방8, 방90] 주소 적힌 쪽지(S-G List) 줄게!"       │
│   DMA: "ㅇㅋ 접수!"                                                       │
│   [ 디스크 ] ──4K──▶ [ 물리 RAM 방 1 ] (Scatter 1)                        │
│   [ 디스크 ] ──4K──▶ [ 물리 RAM 방 8 ] (Scatter 2)                        │
│   [ 디스크 ] ──4K──▶ [ 물리 RAM 방 90 ] (Scatter 3)                       │
│   DMA: 💥 "쪽지에 적힌 3곳 다 배달 끝! (인터럽트 1번 빵!)"                │
│   ✅ 결과: 램 파편화를 전혀 신경 쓰지 않고 초고속으로 Zero-Copy 적재 완료.│
└───────────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** "흩어 뿌리다(Scatter)"라는 단어가 가장 예술적으로 어울리는 아키텍처다. 유저 입장에서는 가상 주소가 `0x1000 ~ 0x4000`으로 12KB가 쫙 붙어있지만, 현실 세계(물리 램)는 찢어져 있다. S-G DMA는 하드웨어이면서도 소프트웨어의 [[381_virtual_memory|가상 메모리]]가 쳐놓은 이 어지러운 찢김을 완벽하게 수용하고 이해해 준다. CPU는 중간에 단 한 번도 [[016_interrupt_mechanism|인터럽트]]에 불려 나오지 않고 편안하게 숙면을 취한다.

- **📢 섹션 요약 비유**: 이삿짐센터에서 큰 장롱(12KB [[501_file_definition_logical_record|파일]])을 새집([[381_virtual_memory|가상 메모리]])에 넣으려는데, 새집 방문이 좁아서 통째로 안 들어갑니다(연속 물리 램 부족). 옛날 일꾼(일반 [[746_io_direct_memory_access_dma|DMA]])은 문을 부수자고 난리를 치지만, S-G 일꾼은 조용히 장롱을 분해해서 각 부품을 창문, 뒷문, 안방으로 다 흩어 뿌려(Scatter) 넣은 뒤, 방 안에서 다시 하나로 예쁘게 조립해 주는 가장 스마트하고 피해 없는 이사 방법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### S-G List (Scatterlist) 구조체의 흑마술

OS와 DMA는 어떻게 주소 목록을 주고받을까? 리눅스 [[022_kernel_role|커널]] 안에는 `struct scatterlist` 라는 구조체 배열이 존재한다.
- OS는 램에 `[시작 주소, 길이], [시작 주소, 길이], [시작 주소, 길이]` 형태로 배열을 쫙 적어놓는다. 
- 그리고 이 **배열의 첫 번째 주소(포인터)**만 랜카드나 디스크의 [[746_io_direct_memory_access_dma|DMA]] 제어 레지스터에 틱 던져준다.
- 똑똑한 [[746_io_direct_memory_access_dma|DMA]] 칩셋은 램에 있는 이 배열을 스스로 읽고(Fetch), 1번째 줄 주소에 [[001_dikw_pyramid|데이터]]를 꽂고, 다 끝나면 2번째 줄 주소를 읽어서 또 [[001_dikw_pyramid|데이터]]를 꽂는 **셀프 루프 연산**을 하드웨어 내부 트랜지스터로 징징징 돌려버린다.

---

### Gather (수집)의 위력: 네트워크 패킷 전송 ([[566_mmap_zero_copy_sendfile|Zero-Copy]])

디스크에서 램으로 뿌릴 때가 Scatter라면, 반대로 **램에서 네트워크(랜카드)로 쏠 때가 Gather(수집)**다.
1. 웹 서버(Nginx)가 영화 [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]를 보낸다. 유저 램 공간에 영상 [[001_dikw_pyramid|데이터]]가 있다. (주소 A)
2. OS [[022_kernel_role|커널]]이 이 [[001_dikw_pyramid|데이터]]에 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 헤더(출발지, 목적지 IP)를 붙인다. 이 헤더는 [[022_kernel_role|커널]] 램 공간에 있다. (주소 B)
3. 만약 S-G DMA가 없다면? OS는 주소 A와 주소 B의 내용을 제3의 연속된 버퍼(주소 C)로 몽땅 복사(Memcpy)해서 하나로 예쁘게 뭉친 뒤에야 랜카드에 쏴야 한다. 서버 CPU가 복사하다가 100% 터져 죽는다.
4. **S-G DMA의 등판 ([[566_mmap_zero_copy_sendfile|Zero-Copy]])**:
   - OS는 복사를 안 한다. 그냥 DMA에게 S-G 리스트를 던진다. 
   - `[주소 B에서 64바이트(헤더) 가져와라, 그 다음 주소 A에서 1500바이트(영상) 가져와라]`
   - 랜카드 [[746_io_direct_memory_access_dma|DMA]] 칩셋이 알아서 찢어져 있는 주소 B와 A를 쓱쓱 긁어와(Gather), 랜카드 내부에서 하나의 1564바이트짜리 뚱뚱한 패킷으로 이쁘게 조립해 인터넷으로 쏴버린다!
   - 램 [[001_dikw_pyramid|데이터]]는 1mm도 움직이지 않았다. CPU 복사 연산 0회. 이것이 초당 수천만 번의 패킷을 쳐내는 10G/40G 현대 네트워크 서버 최강의 비밀 병기, **Tso ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[364_segmentation|Segmentation]] Offload)**와 융합된 Gather 기술의 정수다.

- **📢 섹션 요약 비유**: 햄버거 세트를 포장할 때, 주방(유저 램)에 있는 햄버거와 [[059_counter|카운터]]([[022_kernel_role|커널]] 램)에 있는 콜라를 굳이 직원이 한곳에 모아 종이봉투(복사 버퍼)에 예쁘게 담을 필요가 없습니다. 그냥 배달 기사(S-G [[746_io_direct_memory_access_dma|DMA]])한테 "주방 가서 햄버거 집고, [[059_counter|카운터]] 가서 콜라 집어서 네 오토바이(랜카드)에서 한 번에 묶어 배달해!"라고 시키면 직원의 동선 낭비(CPU 멤카피)가 완벽히 사라지는 꿀알바 시스템입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: Bounce [[454_buffering|Buffering]] (바운스 버퍼) vs Scatter-Gather [[746_io_direct_memory_access_dma|DMA]]

S-G 기술이 없을 때 [[022_kernel_role|커널]] 해커들이 울며 겨자 먹기로 쓰던 낡은 꼼수와의 비교다.

| 관점 | 바운스 [[454_buffering|버퍼링]] (Bounce [[454_buffering|Buffering]]) | [[164_scattering_reflection_radio_waves|산란]]-수집 (Scatter-Gather [[746_io_direct_memory_access_dma|DMA]]) |
|:---|:---|:---|
| **메모리 확보** | OS가 부팅 시 연속된 거대 램([[022_kernel_role|커널]] 공터)을 미리 1개 빼놓음 | 램이 4KB로 완전히 갈기갈기 찢어져 있어도 상관없음 |
| **[[001_dikw_pyramid|데이터]] 동선** | 찢어진 유저 램 -> 바운스 버퍼로 복사 -> [[746_io_direct_memory_access_dma|DMA]] 전송 | **유저 램 -> (복사 없음) -> [[746_io_direct_memory_access_dma|DMA]] 전송 ([[566_mmap_zero_copy_sendfile|Zero-Copy]])** |
| **CPU 점유율** | 램 복사(Memcpy) 하느라 **CPU 폭주 ☠️** | S-G 리스트 몇 줄 적어주는 거 빼면 **CPU 0% 🚀** |
| **적용 하드웨어**| 저가형 [[359_usb|USB]] 메모리, 구형 구석기 랜카드 | 최신 [[482_nvme|NVMe]] [[327_ssd|SSD]], 10Gbps+ 엔터프라이즈 랜카드, [[418_gpu|GPU]] |

### [[257_thrashing|스래싱]]([[257_thrashing|Thrashing]]) 방어의 최후 저지선
서버가 1년 내내 돌다 보면 램 파편화가 극에 달해, 1MB(256프레임)짜리 연속된 물리 프레임을 찾는 게 아예 불가능해진다. 만약 모든 하드웨어가 구형 일반 DMA만 지원했다면, 리눅스 [[022_kernel_role|커널]]은 1MB 네트워크 패킷을 받기 위해 하루 종일 램 조각을 미는 '컴팩션([[347_compaction|Compaction]])'을 돌리느라 서버가 1분에 한 번씩 얼어붙었을 것이다([[257_thrashing|스래싱]]).
하지만 전 세계의 모든 서버 벤더들이 **네트워크([[587_nic_offloading|NIC]])와 스토리지(HBA) 칩셋에 S-G 기능을 하드웨어 표준으로 강제 탑재**함으로써, OS [[022_kernel_role|커널]]은 램 파편화를 신경 쓰지 않고 무책임하게(?) 4KB 쪼가리들을 툭툭 던져주면서도 시스템을 100% 쾌속으로 굴릴 수 있게 되었다. 하드웨어가 소프트웨어의 똥(파편화)을 묵묵히 치워주는 가장 완벽한 헌신이다.

```text
┌──────────┬────────────┬────────────┬──────────────────────────────────────┐
│ OS 파편화 수준│ 일반 DMA 체감 렉│ S-G DMA 체감 렉 │ 디바이스 칩셋 가격    │
├──────────┼────────────┼────────────┼──────────────────────────────────────┤
│ 깨끗함 (초기)│ 0초 컷 (쾌적)  │ 0초 컷 (쾌적)   │ 싸다                    │
│ 극심함 (1년) │ ☠️ 3~5초 정지  │ 🚀 여전히 0초 컷 │ 칩셋에 로직 추가로 비쌈│
└──────────┴────────────┴────────────┴──────────────────────────────────────┘
```
**[매트릭스 해설]** "좋은 하드웨어는 OS의 무능함(파편화)을 가려준다." S-G DMA는 비싼 칩셋 단가라는 허들을 넘고 모든 서버의 디폴트가 되었다. 램 파편화를 막으려고 죽어라 소프트웨어를 튜닝하는 것보다, 파편화된 걸 그대로 씹어먹을 수 있는 하드웨어를 꽂는 게 현대 IT 인프라의 가장 쿨한 해결책이기 때문이다.

- **📢 섹션 요약 비유**: 도로에 구멍(파편화)이 뻥뻥 뚫렸을 때, 일반 자동차(기본 [[746_io_direct_memory_access_dma|DMA]])는 구멍을 메우는 아스팔트 공사(컴팩션)가 끝날 때까지 며칠을 기다려야 하지만, 무한 궤도가 달린 군용 탱크(S-G [[746_io_direct_memory_access_dma|DMA]])는 도로가 깨지든 말든 구멍을 밟고 우렁차게 지나가는 무지막지한 돌파력을 보여줍니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: iSCSI와 [[493_san_storage_area_network|SAN]]([[493_san_storage_area_network|Storage Area Network]])의 심장
1. **문제 상황**: AWS [[001_dikw_pyramid|데이터]]센터에서 내 가상 서버([[598_vm_migration_nic|VM]])가 100GB짜리 네트워크 디스크(EBS)에 [[298_qkv_attention|쿼리]] [[001_dikw_pyramid|데이터]]를 쓴다.
2. **소프트웨어의 찢기**:
   - [[381_virtual_memory|가상 메모리]]의 [[259_paging|페이징]] 시스템 때문에 100GB [[298_qkv_attention|쿼리]] [[001_dikw_pyramid|데이터]]는 램에서 2,500만 개의 4KB 조각으로 갈기갈기 찢겨 있다.
3. **블록 레이어의 합치기 (S-G List [[087_process_state_transition|생성]])**:
   - 리눅스 [[022_kernel_role|커널]]의 블록 I/O 계층은 이 찢어진 2,500만 개의 [[286_page_frame|페이지]] 중, 운 좋게 물리적으로 연속된 놈들끼리 묶고 나머지는 S-G 리스트로 주소록을 짠다.
4. **HBA (Host [[344_bus|Bus]] [[259_adapter_pattern_interface_wrapper|Adapter]]) 칩셋의 발진**:
   - 서버 뒤에 꽂힌 광케이블 랜카드(HBA)가 이 S-G 리스트를 낚아챈다. 
   - 칩셋 내부의 하드웨어 모터가 이 수천만 개의 램 조각을 빛의 속도로 스캔하여(Gather) 한 덩어리의 거대한 광케이블 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 패킷([[696_fibre_channel_protocol|Fibre Channel]])으로 묶어버린다.
   - 단 한 번의 CPU 복사도 없이 100GB의 [[001_dikw_pyramid|데이터]]가 네트워크 건너편의 스토리지 서버로 꽂힌다.
   - 이 S-G 기술이 없었다면 현대의 넷플릭스, 유튜브가 제공하는 테라바이트 급 [[001_dikw_pyramid|데이터]] 스트리밍은 CPU가 다 타버려서 애초에 불가능했다.

### 보안의 위협: IOMMU의 필요성
S-G DMA는 치명적인 보안 리스크가 있다. 랜카드가 리스트를 잘못 읽거나, 해커가 랜카드 펌웨어를 해킹해서 S-G 리스트에 "0번지 [[022_kernel_role|커널]] 메모리(비밀번호)" 주소를 쓱 끼워 넣으면? CPU의 권한 검사를 거치지 않는 무법자 DMA가 [[022_kernel_role|커널]] 램의 비밀 [[001_dikw_pyramid|데이터]]를 그대로 긁어서(Gather) 인터넷 밖으로 유출해 버린다([[0993_dma_attack|DMA Attack]]).
이를 막기 위해 서버 메인보드에는 **[[627_iommu_dma_isolation|IOMMU]] (Input-Output [[328_mmu|MMU]])**라는 추가 방어벽이 꽂혀있다. DMA가 램 주소로 손을 뻗을 때마다, 이 IOMMU가 문지기처럼 서서 "너 이 주소 접근할 권한(S-G 맵핑) 받은 거 맞아?" 하고 한 번 더 깐깐하게 검사해서 해커를 쳐내는 현대 서버의 철통 보안을 담당한다.

- **📢 섹션 요약 비유**: S-G DMA는 공장(램)의 모든 구역을 프리패스로 드나들며 물건을 긁어가는 [[148_5g_embb_urllc_mmtc|초고속]] 외주 청소 로봇입니다. 너무 편하지만, 로봇이 미쳐서 사장님 금고([[022_kernel_role|커널]])까지 긁어갈까 봐 두렵죠. 그래서 로봇 전용 감시 카메라와 구역 제한 울타리([[627_iommu_dma_isolation|IOMMU]])를 쳐서 "로봇아, 넌 화장실과 거실만 긁어모아라"라고 통제하는 것이 현대 보안의 정석입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **[[566_mmap_zero_copy_sendfile|Zero-Copy]] I/O 실현** | [[022_kernel_role|커널]] 메모리 복사 작업(Bounce [[454_buffering|Buffering]])을 삭제하여, 기가비트 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 환경에서 CPU 100% 코어 독점 현상 완벽 해결 |
| **메모리 파편화([[291_fragmentation_and_reassembly_process|Fragmentation]]) 면역** | [[342_external_fragmentation|외부 단편화]]로 인해 연속된 프레임이 소멸하더라도 OS가 램 [[347_compaction|압축]]([[347_compaction|Compaction]])을 하지 않고 I/O를 내보낼 수 있는 강건함 제공 |
| **[[381_virtual_memory|가상 메모리]] 체제와의 궁극적 화해**| 4KB로 찢는 소프트웨어의 철학([[259_paging|페이징]])을 덩어리를 묶는 하드웨어가 100% 수용함으로써 가장 이상적인 HW/SW 코디자인 달성 |

### 결론 및 미래 전망

[[746_io_direct_memory_access_dma|DMA]] [[164_scattering_reflection_radio_waves|산란]]-수집 (Scatter-Gather) 기술은, "컴퓨터 공학의 모든 문제는 중간에 포인터(Indirection) 계층을 하나 추가하면 해결된다"는 데이비드 휠러의 진리를 하드웨어 실리콘 레벨에서 증명한 걸작이다. [[381_virtual_memory|가상 메모리]]의 자유(파편화)가 낳은 최악의 I/O 병목을, 어리석게 OS의 코딩으로 땜빵(Memcpy)하려 하지 않고, 하드웨어 장비 스스로가 지능(List Parsing)을 갖게 함으로써 우아하게 돌파해 냈다. 향후 [[441_cxl|CXL]] 3.0([[441_cxl|Compute Express Link]]) 기반의 완전한 메모리 [[136_variance|분산]] 시대가 오더라도, 네트워크 너머에 수만 개로 찢어진 [[001_dikw_pyramid|데이터]] 조각들을 모으고 흩뿌리는 이 S-G 리스트의 뼈대는, 중앙 집중형 CPU를 바보 같은 짐 나르기에서 영원히 해방시켜 준 구원자로서 IT 인프라의 영원한 핵심 혈관으로 남을 것이다.

- **📢 섹션 요약 비유**: 책상 위에 어지럽게 흩어진 100조각의 퍼즐([[381_virtual_memory|가상 메모리]] 파편화)을 다른 방으로 옮길 때, 엄마(OS)가 100조각을 예쁘게 하나의 네모로 맞추고(Memcpy/[[347_compaction|압축]]) 나서야 옮기던 헛수고를 멈췄습니다. 똑똑한 로봇 청소기(S-G [[746_io_direct_memory_access_dma|DMA]])가 바닥에 널브러진 채로 조각들을 후루룩 빨아들인(Gather) 다음, 다른 방에 가서 원래 있던 모양대로 완벽하게 뱉어주며(Scatter) 엄마를 영원히 노가다에서 해방시킨 가사 노동(시스템) 혁명입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[450_dma_direct_memory_access|직접 메모리 접근]] ([[746_io_direct_memory_access_dma|DMA]], [[318_dma|Direct Memory Access]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| I/O 서브시스템의 [[022_kernel_role|커널]] [[090_service_kubernetes_network_load_balancing|서비스]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[454_buffering|버퍼링]] ([[454_buffering|Buffering]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[사이클 스틸링 (Cycle Stealing)]
    │
    ▼
[DMA 산란-수집 (Scatter-Gather)]
    │
    ├──▶ [I/O 서브시스템의 커널 서비스]
    └──▶ [버퍼링 (Buffering)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [[347_compaction|압축]]해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[746_io_direct_memory_access_dma|DMA]] [[164_scattering_reflection_radio_waves|산란]]-수집 (Scatter-Gather)은 컴퓨터가 디스크와 장치가 [[001_dikw_pyramid|데이터]]를 주고받는 길을 정리하는 방법이에요.
2. 먼저 [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]])을 이해하면 [[746_io_direct_memory_access_dma|DMA]] [[164_scattering_reflection_radio_waves|산란]]-수집 (Scatter-Gather)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 [[746_io_direct_memory_access_dma|DMA]] [[164_scattering_reflection_radio_waves|산란]]-수집 (Scatter-Gather)을 잘 알면 나중에 I/O 서브시스템의 [[022_kernel_role|커널]] [[090_service_kubernetes_network_load_balancing|서비스]]도 훨씬 쉽게 배울 수 있어요.
