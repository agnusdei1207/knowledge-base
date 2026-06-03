---
title: 685. LUN (Logical Unit Number) 마스킹
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LUN (Logical Unit Number) 마스킹은 공유 스토리지에서 "어떤 호스트가 어떤 볼륨을 볼 수 있는가"를 결정하는 가시성 제어 기술이다.
> 2. **가치**: 잘못된 서버가 잘못된 디스크를 [[516_mount_mechanism|마운트]]하는 사고를 막아 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]], 보안, 운영 단순성을 동시에 지킨다.
> 3. **판단 포인트**: 조닝 (Zoning), [[501_file_definition_logical_record|파일]] 시스템 [[164_policy|정책]], 클러스터 설계와 함께 써야 진짜 안전하며, LUN 마스킹 하나만으로 모든 보안 문제가 해결되지는 않는다.

---

## Ⅰ. 개요 및 필요성

LUN (Logical Unit Number) 마스킹은 스토리지 배열이 특정 서버에게만 특정 [[369_logic_bomb|논리]] 디스크를 보이게 만드는 접근 제어다. 직접 연결 디스크에서는 "케이블이 꽂힌 서버만 본다"는 물리적 경계가 있지만, 공유 스토리지 네트워크인 [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]])에서는 여러 서버가 같은 저장장치를 동시에 바라보므로 [[369_logic_bomb|논리]]적 경계가 꼭 필요해진다.

문제가 되는 지점은 가시성이다. 서버가 볼 수만 있으면 [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]])가 디스크를 스캔하고, 관리자가 실수로 초기화하거나 잘못된 [[501_file_definition_logical_record|파일]] 시스템을 올릴 가능성이 생긴다. 특히 서로 다른 [[001_operating_system_purpose|운영체제]]나 다른 [[090_service_kubernetes_network_load_balancing|서비스]]가 같은 LUN을 의도치 않게 건드리면 [[012_metadata|메타데이터]] 충돌, [[501_file_definition_logical_record|파일]] 시스템 손상, [[001_dikw_pyramid|데이터]] 유출이 한 번에 일어날 수 있다.

따라서 LUN 마스킹은 "읽기/[[289_cqrs_db|쓰기]] 권한" 이전의 단계, 즉 "아예 보이게 할 것인가"를 결정하는 1차 방어선이다. 이것이 없으면 대규모 [[001_dikw_pyramid|데이터]]센터에서 서버 수백 대가 수백 개 LUN을 모두 들여다보는 혼란이 생기고, 부팅 시 장치 탐색 시간과 운영 실수 가능성도 함께 커진다.

- **📢 섹션 요약 비유**: LUN 마스킹은 대형 창고의 문패 정리와 같다. 같은 건물 안에 방은 많지만, 각 직원에게 자기 방 문만 보이게 해야 남의 방 물건을 잘못 꺼내는 사고가 줄어든다.

---

## Ⅱ. 동작 구조와 핵심 원리

LUN 마스킹은 보통 스토리지 컨트롤러가 호스트 [[289_identification_flags_fragmentation_offset|식별자]]와 LUN 매핑 테이블을 보고 응답을 걸러내는 방식으로 동작한다. [[696_fibre_channel_protocol|Fibre Channel]] 환경에서는 WWN (World Wide Name), [[698_iscsi|iSCSI]] (Internet Small Computer Systems Interface) 환경에서는 IQN ([[698_iscsi|iSCSI]] Qualified Name) 같은 [[289_identification_flags_fragmentation_offset|식별자]]를 기준으로 사용한다.

아래 그림은 같은 스토리지라도 호스트마다 다른 LUN 목록을 보게 만드는 구조를 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│                  LUN Masking Visibility Flow                │
├──────────────────────────────────────────────────────────────┤
│ Host A (WWN-A) ─┐                                           │
│ Host B (WWN-B) ─┼──▶ SAN Fabric ─▶ Storage Controller       │
│ Host C (WWN-C) ─┘                 │                         │
│                                   ├─ Mapping Table          │
│                                   │   WWN-A -> LUN 10, 11   │
│                                   │   WWN-B -> LUN 20       │
│                                   │   WWN-C -> none         │
│                                   └─ Filtered REPORT LUNS   │
└──────────────────────────────────────────────────────────────┘
```

동작 순서는 단순하지만 중요하다. 첫째, 관리자는 호스트의 [[289_identification_flags_fragmentation_offset|식별자]]를 등록한다. 둘째, LUN을 호스트 또는 호스트 그룹에 매핑한다. 셋째, 서버가 장치 검색 명령을 보내면 컨트롤러는 매핑된 LUN만 응답한다. 서버 입장에서는 허용되지 않은 LUN이 "없는 것처럼" 보인다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 호스트 [[344_bus|버스]] [[259_adapter_pattern_interface_wrapper|어댑터]] (Host [[344_bus|Bus]] [[259_adapter_pattern_interface_wrapper|Adapter]], HBA) | 서버의 스토리지 접속 [[446_port_and_bus|포트]] | 멀티패스 구성이면 모든 [[446_port_and_bus|포트]]를 등록해야 함 |
| 스토리지 [[446_port_and_bus|포트]] | LUN 정보를 광고하는 지점 | [[446_port_and_bus|포트]]별 [[164_policy|정책]]보다 호스트 그룹 [[164_policy|정책]]이 관리에 유리 |
| 매핑 테이블 | [[289_identification_flags_fragmentation_offset|식별자]]와 LUN의 연결 정보 | 운영 표준 없으면 실수 가능성 급증 |
| [[369_logic_bomb|논리]] 디스크 | 실제로 노출할 저장 단위 | [[090_service_kubernetes_network_load_balancing|서비스]] 단위와 장애 [[658_ir_recovery|복구]] 단위를 함께 고려 |

실행 시 [[282_performance_tactics|성능]] 오버헤드는 크지 않다. 결국 조회해야 하는 것은 작은 매핑 테이블이기 때문이다. 대신 운영 정확도가 핵심이다. 잘못된 WWN을 등록하거나, 멀티패스용 보조 [[446_port_and_bus|포트]]를 빼먹으면 장애 시 보조 경로가 있어도 디스크가 안 보이는 일이 생긴다.

- **📢 섹션 요약 비유**: LUN 마스킹은 호텔 프런트의 객실 배정표와 같다. 손님이 같은 호텔에 들어와도 프런트는 예약된 방 번호만 알려주고, 나머지 방은 존재를 알려주지 않는다.

---

## Ⅲ. 비교 및 연결

LUN 마스킹을 제대로 이해하려면 조닝과 [[501_file_definition_logical_record|파일]] 시스템 권한을 함께 구분해야 한다. 이 셋은 모두 "접근 제한"처럼 보이지만 막는 위치가 다르다.

| 구분 | 막는 위치 | 제어 단위 | 왜 중요한가 |
| :--- | :--- | :--- | :--- |
| 조닝 (Zoning) | [[238_switch_operation_principles|스위치]] 패브릭 | [[446_port_and_bus|포트]], WWN | 애초에 어느 장치끼리 통신할지 제한 |
| LUN 마스킹 | 스토리지 컨트롤러 | LUN | 통신 가능해도 어떤 볼륨이 보일지 제한 |
| [[501_file_definition_logical_record|파일]] 시스템 권한 | [[001_operating_system_purpose|운영체제]]와 응용계층 | [[501_file_definition_logical_record|파일]], [[506_directory_structure_symbol_table|디렉터리]] | [[516_mount_mechanism|마운트]] 이후 사용자 행위를 제한 |

즉 조닝은 "길을 열어 줄지"를 정하고, LUN 마스킹은 "창고 안 어느 방을 보여 줄지"를 정하며, [[501_file_definition_logical_record|파일]] 시스템 권한은 "들어간 뒤 무엇을 할 수 있는지"를 정한다. 보안과 안정성을 높이려면 세 단계가 모두 필요하다. 특히 금융, 의료, [[310_multi_tenant_database_architecture|멀티테넌트]] 환경에서는 조닝 없이 LUN 마스킹만 두는 설계보다, 두 계층을 함께 써서 실수 범위를 줄이는 설계가 더 안전하다.

한편 의도적으로 여러 서버에 같은 LUN을 보여 줘야 하는 예외도 있다. 대표적으로 클러스터 [[501_file_definition_logical_record|파일]] 시스템이나 [[015_virtualization|가상화]] [[001_dikw_pyramid|데이터]]스토어다. 이 경우 LUN 마스킹 자체를 푸는 것이 아니라, "같은 LUN을 봐도 안전한 상위 소프트웨어"가 있다는 전제 아래 제한된 서버 그룹에만 공유 노출한다.

- **📢 섹션 요약 비유**: 조닝이 건물 출입 게이트라면, LUN 마스킹은 층별 출입 통제이고, [[501_file_definition_logical_record|파일]] 권한은 방 안 서랍 열쇠다. 같은 건물 보안이라도 막는 지점이 서로 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 LUN 마스킹을 [[090_service_kubernetes_network_load_balancing|서비스]] 경계 정의 도구로 써야 한다. 예를 들어 [[015_virtualization|가상화]] 클러스터 두 대와 [[002_database_definition|데이터베이스]] 서버 두 대가 같은 스토리지를 공유한다면, [[015_virtualization|가상화]]용 [[001_dikw_pyramid|데이터]]스토어 LUN은 클러스터 노드에만, [[002_database_definition|데이터베이스]]용 [[568_logs_distributed_logging_elk_fluentd|로그]] LUN은 [[002_database_definition|데이터베이스]] 노드에만 보여 주는 식으로 호스트 그룹을 분리한다. "잘못 보여 주지 않는 설계"가 "나중에 잘 막는 설계"보다 훨씬 낫다.

또한 멀티패스 I/O ([[500_multipath_io|Multipath]] Input/Output)를 쓴다면 한 서버의 모든 경로 [[289_identification_flags_fragmentation_offset|식별자]]를 빠짐없이 등록해야 한다. 운영자는 경로 두 개를 구성해 놓고도 한쪽 HBA [[446_port_and_bus|포트]]만 마스킹해 두는 실수를 자주 한다. 이 경우 평소에는 정상처럼 보여도 장애 시 대체 경로에서 LUN이 사라져 페일오버가 실패한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[090_service_kubernetes_network_load_balancing|서비스]] 단위가 아닌 "호스트 그룹 단위"로 LUN을 묶어 관리하고 있는가?
2. 퇴역 서버의 WWN 또는 IQN이 매핑 테이블에 남아 있지 않은가?
3. 클러스터 공유 LUN은 정말로 클러스터 인지 [[501_file_definition_logical_record|파일]] 시스템이 있는 경우에만 열어 두었는가?
4. 조닝과 LUN 마스킹 결과를 서버 재검색으로 실제 검증했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 개발, 운영, [[555_backup_and_restore_strategy|백업]] 서버에 같은 LUN을 일괄 노출하는 Any-to-Any 구성
- 호스트 내부에서 장치를 숨기는 스크립트를 LUN 마스킹 대체책으로 믿는 구성
- 운영 문서 없이 WWN 이름을 사람 기억에만 의존하는 구성

- **📢 섹션 요약 비유**: 실무의 LUN 마스킹은 병원 약품 창고 분류와 같다. 같은 병원이라도 수술실 약, 응급실 약, 연구실 약을 아무 데나 꺼내 쓰게 두면 사고는 언젠가 반드시 난다.

---

## Ⅴ. 기대효과 및 결론

LUN 마스킹을 잘 설계하면 첫째, [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]이 좋아진다. 잘못된 서버가 잘못된 볼륨을 건드릴 확률을 구조적으로 낮추기 때문이다. 둘째, 운영 가시성이 좋아진다. 서버가 자기에게 필요한 디스크만 보므로 장치 스캔, 장애 분석, 변경 관리가 단순해진다. 셋째, [[310_multi_tenant_database_architecture|멀티테넌트]] 환경에서 기본적인 자원 격리 수준을 확보할 수 있다.

다만 한계도 분명하다. WWN 기반 통제는 암호화가 아니므로 계층적 보안의 일부일 뿐이며, 잘못 매핑된 합법 사용자까지 막아 주지는 않는다. 또한 자동화가 약한 환경에서는 변경 이력 누락이 큰 리스크가 된다. 최근에는 [[499_nvme_over_fabrics|NVMe-oF]] ([[482_nvme|Non-Volatile Memory Express]] over Fabrics)의 NQN ([[482_nvme|NVMe]] Qualified Name) 기반 접근 제어처럼 더 현대적인 [[655_ir_detection_analysis|식별]] 체계와 응용 프로그래밍 인터페이스 기반 [[164_policy|정책]] 관리가 확산되는 중이다.

결국 LUN 마스킹은 "디스크를 보호하는 기술"이라기보다 "가시성을 설계하는 기술"로 기억하는 것이 정확하다. 기술사 관점에서는 저장장치 [[282_performance_tactics|성능]]보다 먼저, 누가 무엇을 볼 수 있는지의 경계를 명확히 그려야 한다.

- **📢 섹션 요약 비유**: LUN 마스킹은 도서관 서가 전체를 잠그는 기술이 아니라, 사람마다 볼 수 있는 서가 목록을 다르게 배포하는 출입 카드와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| LUN (Logical Unit Number) | 마스킹의 대상이 되는 [[369_logic_bomb|논리]] 저장 단위 |
| WWN (World Wide Name) | [[696_fibre_channel_protocol|Fibre Channel]] 호스트를 [[655_ir_detection_analysis|식별]]하는 기준 |
| IQN ([[698_iscsi|iSCSI]] Qualified Name) | [[698_iscsi|iSCSI]] 환경에서의 호스트 [[289_identification_flags_fragmentation_offset|식별자]] |
| 조닝 (Zoning) | LUN 마스킹보다 앞단에서 통신 경로를 제한 |
| 멀티패스 I/O ([[500_multipath_io|Multipath]] Input/Output) | 동일 LUN에 대한 다중 경로 접근을 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
Direct Attached Storage
        │
        ▼
Shared SAN (Storage Area Network)
        │
        ▼
Zoning for fabric isolation
        │
        ▼
LUN Masking for volume visibility control
        │
        ▼
Host-group automation / NVMe-oF access policy
```

이 흐름은 저장장치가 "물리 연결" 중심에서 "[[164_policy|정책]] 기반 가시성 제어" 중심으로 이동하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 장난감 창고에 서랍이 아주 많아도, 네 이름표가 붙은 서랍만 보여 주면 헷갈리지 않아요.
2. 남의 서랍이 안 보이면 실수로 남 장난감을 꺼내 망가뜨릴 일도 줄어들어요.
3. LUN 마스킹은 창고 관리자가 "누구에게 어떤 서랍을 보여 줄지" 정해 주는 규칙이에요.

