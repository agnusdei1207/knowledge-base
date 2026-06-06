---
title: "Page Table"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/))은 가상 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호를 물리 프레임 번호로 바꾸는 번역표이자, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 [메모리 보호](/studynote/01_computer_architecture/07_virtual_memory_os_integration/803_memory_protection/) 정책을 하드웨어에 전달하는 제어 표다.
> 2. **가치**: 프로그램은 연속된 가상 주소 공간을 쓰는 것처럼 보이지만, 실제 메모리는 흩어진 프레임으로 배치할 수 있어 효율과 격리를 동시에 얻는다.
> 3. **판단 포인트**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 유연한 대신 메모리와 접근 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 비용이 크므로, 다단계 구조·[TLB](/studynote/02_operating_system/06_memory_management/357_tlb/)·[Huge Page](/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/) 같은 보완책을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/))은 가상 주소를 물리 주소로 바꾸기 위한 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 핵심 자료구조다. CPU가 가상 주소를 생성하면, [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/))는 그 주소의 가상 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호를 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)에서 조회해 실제 메모리 프레임을 찾아낸다. 즉 프로그램이 보는 주소 세계와 하드웨어가 실제로 접근하는 주소 세계 사이에 놓인 공식 통역사라고 볼 수 있다.

이 구조가 필요한 이유는 프로그램이 사용하는 메모리와 실제 RAM의 배치 방식이 다르기 때문이다. 프로세스는 0번지부터 연속된 공간을 기대하지만, 물리 메모리는 여러 프로세스와 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 함께 쓰므로 조각나기 쉽다. [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)이 없으면 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 프로세스마다 큰 연속 공간을 미리 확보해야 하고, 그 결과 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)와 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 문제를 동시에 떠안게 된다.

또한 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 단순 번역표가 아니라 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치이기도 하다. 읽기 전용 코드 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/), 사용자 접근 금지 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/), 아직 메모리에 없는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 모두 엔트리 상태로 표현할 수 있다. 그래서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 "주소를 어디로 보낼까?"와 "이 접근을 허용할까?"를 한 번에 결정한다.

```text
+----------------------------------------------------------------------------+
|      프로그램이 보는 세계와 하드웨어가 접근하는 세계 사이의 번역 계층      |
+----------------------------------------------------------------------------+
|  프로세스 관점                                                              |
|  [가상 주소 공간]  Page 0 | Page 1 | Page 2 | Page 3                      |
|         |                                                                  |
|         v                                                                  |
|  [페이지 테이블]  "각 페이지가 어느 프레임에 있는가, 접근 가능 상태는?"      |
|         |                                                                  |
|         v                                                                  |
|  물리 메모리 관점                                                           |
|  [RAM 프레임]   Frame 12 | Frame 3 | Frame 88 | Frame 5 ...               |
+----------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 대형 창고의 위치 안내 데스크와 같다. 손님은 "A구역 3번 상자"만 말하지만, 안내 데스크는 실제 창고 선반 위치와 출입 권한까지 함께 확인해 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)의 기본 단위는 PTE ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Entry)다. 각 PTE에는 PFN ([Page Frame](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Number) 같은 실제 위치 정보와 함께 Valid [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/), [Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/), Accessed [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/), [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) 같은 제어 정보가 들어간다. 그래서 한 줄의 엔트리만 읽어도 "어디 있는가, 메모리에 있는가, 수정되었는가, 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/실행이 가능한가"를 동시에 판단할 수 있다.

주소 변환은 보통 가상 주소를 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) (Virtual [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Number)과 Offset으로 나누는 것에서 시작한다. VPN은 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)의 인덱스로 쓰이고, 조회 결과로 얻은 PFN 뒤에 원래 Offset을 붙이면 최종 물리 주소가 된다. 이때 현재 실행 중인 프로세스의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 시작점은 [PTBR](/studynote/02_operating_system/06_memory_management/354_ptbr_ptlr/) ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) [Base Register](/studynote/02_operating_system/06_memory_management/329_base_register/)) 또는 아키텍처별 동등한 레지스터가 가리킨다.

아래 그림은 단일 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 기준의 핵심 흐름을 보여준다. 중요한 점은 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)이 메모리 안에 존재하므로, 주소 하나를 번역하려 해도 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 자체를 한 번 읽어야 한다는 것이다. 그래서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 유연하지만 느릴 수 있고, 이를 보완하기 위해 [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/))가 필수로 붙는다.

```text
+----------------------------------------------------------------------------+
|                 가상 주소 -> 페이지 테이블 -> 물리 주소 변환                  |
+----------------------------------------------------------------------------+
|  가상 주소                                                                  |
|  +-----------------------+-----------------------------------------------+ |
|  | VPN                   | Offset                                        | |
|  +--------------+--------+-----------------------------------------------+ |
|                 |                                                          |
|                 v                                                          |
|        PTBR --> [페이지 테이블 시작 주소]                                   |
|                 |                                                          |
|                 +- VPN으로 PTE 선택                                        |
|                 v                                                          |
|        +---------------------------------------------------------------+   |
|        | PTE = PFN + Valid + Dirty + Access + Protection + ...        |   |
|        +---------------------------------------------------------------+   |
|                 |                                                          |
|                 +- PFN 추출                                                |
|                 v                                                          |
|  물리 주소   +-----------------------+-----------------------------------+ |
|              | PFN                   | Offset                            | |
|              +-----------------------+-----------------------------------+ |
+----------------------------------------------------------------------------+
```

| PTE 항목 | 의미 | 시스템 관점의 중요성 |
| :-- | :-- | :-- |
| PFN ([Page Frame](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Number) | 실제 RAM 프레임 위치 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디 있는지 결정 |
| Valid [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) | 현재 메모리 상주 여부 | 0이면 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) 유발 |
| [Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/) | 적재 후 수정 여부 | 축출 시 디스크 재기록 필요성 판단 |
| [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) | 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/실행 권한 | 사용자/[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 격리와 실행 방지 |
| Accessed [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) | 최근 접근 여부 | 교체 알고리즘의 근거 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

- **📢 섹션 요약 비유**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 단순 주소록이 아니라 출입통제까지 붙은 아파트 관리시스템이다. 몇 동 몇 호인지 알려주는 것에서 끝나지 않고, 지금 집에 있는지, 수리 중인지, 누가 들어갈 수 있는지도 함께 적혀 있다.

---

## Ⅲ. 비교 및 연결

[페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 이해하려면 먼저 "[페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)"와 "[페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)"을 구분해야 한다. [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 나눈 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각이고, [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 그 조각들이 어디에 배치되었는지 기록한 메타데이터다. 즉 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/) ([Paging](/studynote/02_operating_system/04_synchronization/259_paging/))이 배치 방식이라면, [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 그 배치 방식을 실행 가능하게 만드는 운영 장부다.

또한 단일 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 구조가 단순하지만 주소 공간이 커질수록 메모리 낭비가 심해진다. 예를 들어 64비트 시스템에서 모든 가상 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 대해 엔트리를 일괄 보관하면, 실제로 쓰지 않는 넓은 주소 범위까지 장부를 만들어야 한다. 그래서 현대 시스템은 다음 문서의 주제인 [다단계 페이지 테이블](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/) ([Multilevel Page Table](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/))로 확장해 필요한 부분만 계층적으로 생성한다.

[세그먼트 테이블](/studynote/02_operating_system/06_memory_management/365_segment_table/)과 비교하면 경계도 더 선명해진다. [세그먼트 테이블](/studynote/02_operating_system/06_memory_management/365_segment_table/)은 코드, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 스택처럼 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 의미 단위를 관리하는 데 강하지만, 크기가 가변적이라 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 관리 부담이 크다. 반면 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 고정 크기 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 전제로 하므로 공간 관리가 단순하고, [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 비트와 결합해 하드웨어 친화적인 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 체계를 만든다.

| 비교 축 | [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) | [세그먼트 테이블](/studynote/02_operating_system/06_memory_management/365_segment_table/) |
| :-- | :-- | :-- |
| 관리 단위 | 고정 크기 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 가변 크기 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 세그먼트 |
| 강점 | [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 제어와 하드웨어 구현 용이 | 의미 단위 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)와 공유 표현 쉬움 |
| 약점 | 엔트리 수가 많아 장부가 커짐 | [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)와 배치 복잡도 증가 |
| 현대적 위치 | [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 표준 기반 | 보조 개념 또는 제한적 사용 |

- **📢 섹션 요약 비유**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 규격 박스 창고의 선반 목록이고, [세그먼트 테이블](/studynote/02_operating_system/06_memory_management/365_segment_table/)은 책·옷·장난감처럼 종류별 보관 목록에 가깝다. 전자는 정리가 빠르고, 후자는 의미를 살리기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안을 동시에 건드린다. [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)이 크고 깊어질수록 [Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Walk 비용이 커지고, [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 미스가 잦은 워크로드에서는 CPU가 실제 계산보다 주소 번역에 더 많은 시간을 쓸 수 있다. 반대로 권한 비트를 잘 설계하면 사용자 공간과 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간을 분리하고, 코드 주입 공격에 대한 실행 제한도 하드웨어 수준에서 강제할 수 있다.

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 관점에서도 중요하다. [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 스위치가 발생하면 현재 프로세스의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 기준점이 바뀌고, 그에 따라 기존 주소 번역 캐시의 유효성이 흔들릴 수 있다. 그래서 Address Space [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/) 같은 태그 기법, [Huge Page](/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/) 사용, 메모리 지역성 개선은 모두 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 오버헤드를 줄이기 위한 실무적 해법이다.

기술사 답안이나 아키텍처 판단에서는 다음 질문이 핵심이다. 첫째, 워크로드가 큰 연속 메모리 블록을 자주 접근하는가, 아니면 랜덤 접근이 많은가. 둘째, 보안 요구가 높아 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위 권한 분리가 중요한가. 셋째, 메모리 규모가 커서 단일 테이블이 비현실적인가. 이 질문들에 따라 [다단계 페이지 테이블](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/), [Huge Page](/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/), [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 튜닝, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-사용자 분리 전략을 함께 선택해야 한다.

### 체크 포인트

1. [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 미스가 잦아 [Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Walk가 병목이 되는가?
2. 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/실행 권한이 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위로 명확히 설계되었는가?
3. 대용량 메모리 환경에서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 자체의 메모리 사용량을 측정했는가?
4. [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 스위치와 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서 주소 번역 비용을 별도로 관찰하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 메모리 비용을 보지 않고 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 크기만 기본값으로 고정하는 설계
- 실행 금지 비트를 무시해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에서도 코드 실행이 가능한 상태를 방치하는 운영
- 주소 지역성이 낮은 자료구조를 남발해 TLB와 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 양쪽 모두를 괴롭히는 구현

- **📢 섹션 요약 비유**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 회사 건물 출입 시스템과 같다. 사무실 위치를 빨리 찾게 해줘야 하고, 동시에 아무나 서버실에 들어가지 못하게 막아야 한다.

---

## Ⅴ. 기대효과 및 결론

[페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)의 가장 큰 효과는 추상화와 통제의 동시 달성이다. 프로세스는 자신만의 연속된 메모리 공간을 가진 것처럼 단순하게 동작하고, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 실제 메모리를 비연속적으로 배치하면서도 충돌 없이 관리할 수 있다. 이 덕분에 멀티프로그래밍, 프로세스 격리, [스와핑](/studynote/02_operating_system/06_memory_management/335_swapping/), [메모리 보호](/studynote/01_computer_architecture/07_virtual_memory_os_integration/803_memory_protection/) 같은 현대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 기능이 성립한다.

하지만 비용도 분명하다. [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 자체가 메모리를 먹고, 번역 과정은 추가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 만든다. 그래서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 "좋은 개념"이 아니라 "필수지만 공짜는 아닌 개념"으로 기억해야 한다. 현대 시스템이 다단계 테이블, [역 페이지 테이블](/studynote/02_operating_system/06_memory_management/363_inverted_page_table/), [Huge Page](/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/), 하드웨어 가속 번역을 계속 발전시키는 이유도 바로 이 비용을 줄이기 위해서다.

결론적으로 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 부속품이 아니라, [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 실제로 작동시키는 실행 엔진이다. [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 공간 분할의 단위라면, [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 그 단위를 질서 있게 묶는 운영 규칙이다. 따라서 이 개념은 "주소 번역표"로만 외우기보다 "[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·[보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)·확장성의 균형점"으로 이해해야 오래 남는다.

- **📢 섹션 요약 비유**: [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 도시 전체의 지번 체계와 같다. 주소가 정리되어 있어야 택배도 빨라지고, 출입 통제도 가능하며, 새 건물이 생겨도 도시가 혼란 없이 커질 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) | [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 실제로 읽어 가상 주소를 물리 주소로 변환하는 하드웨어 |
| PTE ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Entry) | [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)의 한 줄로서 위치·상태·권한 정보를 담는 최소 단위 |
| [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | 자주 쓰는 번역 결과를 캐시해 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 접근 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄임 |
| [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) | Valid Bit가 꺼진 엔트리에 접근했을 때 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 개입하는 사건 |
| [다단계 페이지 테이블](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/) ([Multilevel Page Table](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/)) | 큰 주소 공간에서 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 자체의 메모리 낭비를 줄이는 확장 구조 |
| [세그멘테이션](/studynote/02_operating_system/06_memory_management/364_segmentation/) ([Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/)) | 의미 단위 메모리 관리 방식으로, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 기반 관리와 경계 비교 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
연속 할당의 한계
    |
    v
페이징 (Paging)
    |
    v
페이지 테이블 (Page Table)
    |
    +- 보호 비트 · Valid Bit · Dirty Bit
    |
    +- TLB (Translation Lookaside Buffer)
    |
    v
다단계 페이지 테이블 (Multilevel Page Table)
    |
    v
역 페이지 테이블 · Huge Page · 가상화용 EPT/NPT
```

이 흐름은 "공간 분할 -> 번역 장부 -> [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보완 -> 대규모 확장"으로 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 기술이 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)은 "내 장난감 번호가 진짜로 어디 서랍에 있는지" 적어 둔 찾기 노트예요.
2. 이 노트는 장난감 위치만 알려주는 게 아니라, 만져도 되는지 못 만지는지도 같이 알려줘요.
3. 그래서 방이 조금 어질러져 있어도, 나는 번호만 알면 필요한 장난감을 안전하게 찾을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 288 / 803

<- **이전**: [287. 내부 단편화 (Internal Fragmentation)](/studynote/01_computer_architecture/07_virtual_memory_os_integration/287_internal_fragmentation/)
**다음**: [289. 다단계 페이지 테이블 (Multilevel Page Table)](/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/) ->

---
