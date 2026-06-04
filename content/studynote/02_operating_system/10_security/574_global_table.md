+++
title = "574. 전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 전역 테이블(Global Table)은 [접근 제어 행렬](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/)에서 <strong>권한이 존재하는 칸만</strong>을 `<도메인, 객체, 권한>` 3단 튜플로 저장하는 자료구조이다. 빈 칸(Null)을 저장하지 않아 **[공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)를 $O(실제 권한 수)$로 절감**한다.
> 2. **가치**: 이 <strong>희소성 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>(Sparse <a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/">Compression</a>)</strong> 덕분에, 수천만 개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 있는 시스템에서도 실제 권한 설정만 메모리에 저장하여 RAM을 절약할 수 있다.
> 3. **한계**: 권한 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 시 리스트 전체를 순차 탐색해야 하므로 **$O(N)$ [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)**가 발생하고, 중앙 테이블에 동시 접근 시 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/">락 경합</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/">Lock Contention</a>)</strong> 문제가 발생한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 희소 행렬의 문제점

| 구분 | 전체 칸 수 | 실제 권한 칸 | 낭비 공간 |
|:---|:---|:---|:---|
| **수치** | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 1만 × [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1만 = 1억 칸 | 약 1만 칸 | **99.99%** |

1억 칸의 메모리를 할당하면 대부분의 칸이 비어있어 극심한 메모리 낭비가 발생한다.

### 1.2 전역 테이블의 해결책

**"권한이 있는 경우만 저장한다"**

```text
[ 기존 2차원 행렬 ]
        파일1     파일2     파일3
도메인A  Read     Null      Null
도메인B  Null     Read     Null
도메인C  Null     Read     Write

[ 전역 테이블 (Linked List) ]
Head -> < 도메인A, 파일1, {Read} >
      -> < 도메인B, 파일2, {Read} >
      -> < 도메인C, 파일2, {Read} >
      -> < 도메인C, 파일3, {Write} >
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 시간-공간 트레이드오프

| 구분 | 2차원 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) | 전역 테이블 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/">공간 복잡도</a></strong> | $O(|D| \times |O|)$ | $O(실제 권한 수)$ |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/">시간 복잡도</a></strong> | $O(1)$ (인덱싱) | $O(N)$ ([선형 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)) |
| **적용** | 메모리 풍부한 환경 | 메모리 제약 환경 |

### 2.2 동시 접근 문제

여러 프로세스가 동시에 전역 테이블에 접근하면:
1. 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 충돌 방지을 위해 <strong>뮤텍스 잠금(<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/699_mutex_lock_sleep_wait/">Mutex Lock</a>)</strong> 필요
2. 잠금 대기 시간이 증가하면 <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하</strong> 발생

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 iptables와 전역 테이블

[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(iptables)의 규칙 체인도 전역 테이블과 유사한 구조다:

```
[Chain: INPUT]
Rule 1: DROP   IP 192.168.1.100
Rule 2: ACCEPT TCP 80
Rule 3: DROP   ALL
```

패킷이 들어올 때마다 위에서 아래로 <strong>순차적으로 규칙을 매칭</strong>한다. 규칙이 10만 개인 경우, 마지막 규칙까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 하므로 **$O(N)$ 시간**이 소요된다.

### 3.2 eBPF와 해시 기반 최적화

최신 리눅스에서는 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a>(extended <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/">Berkeley Packet Filter</a>)</strong>를 활용하여:
- 규칙을 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/">해시 테이블</a></strong>에 저장
- 평균 **$O(1)$ 시간**에 규칙 매칭

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **공간 절약**: 희소 행렬 문제를 해결하여 메모리를 효율적으로 사용
- **시간 비용**: [선형 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)으로 인해 접근 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 시간이 증가
- **현대적 대안**: [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/), [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) 등을 활용한 최적화

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/knowledge-base/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [접근 제어 목록](/knowledge-base/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), [Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [보호 도메인](/knowledge-base/studynote/02_operating_system/10_security/572_protection_domain/) ([Protection Domain](/knowledge-base/studynote/02_operating_system/10_security/572_protection_domain/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [접근 제어 행렬](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/) ([Access Matrix](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [접근 제어 목록](/knowledge-base/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), [Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [자격 증명 리스트](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) ([Capability List](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) / Ticket) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[접근 제어 행렬 (Access Matrix)]
    |
    v
[전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)]
    |
    +---> [접근 제어 목록 (ACL, Access Control List)]
    +---> [자격 증명 리스트 (Capability List / Ticket)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>전역 테이블</strong>은 학교의 <strong>"출입 가능 명단"</strong>과 같다. 모든 학생과 모든 교실의 관계를 적는 게 아니라, <strong>"출입 가능한 조합"만</strong>을 적어둔다.

2. <strong>공간 절약</strong>은명부(명부)에서 빈 칸을 지우고 **허가(허용)된 경우만** 적는 것과 같다. 공간은 절약되지만, 모든 학생의 출입 가능 교실을 알려면명부를 모두 읽어야 한다.

3. <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/">락 경합</a></strong>은 여러 명부(명부) 관리자가 동시에명부를 수정하려고 할 때, <strong>한 명씩만 수정</strong>해야 해서 대기 시간이 발생하는 것과 같다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 574 / 800

<- **이전**: [573. 접근 제어 행렬 (Access Matrix) - 주체(행)와 객체(열) 교차점의 권한 표현 모형](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/)
**다음**: [575. 접근 제어 목록 (ACL, Access Control List) - 객체 중심 (해당 객체에 접근 가능한 주체 목록)](/knowledge-base/studynote/02_operating_system/10_security/575_acl_access_control_list/) ->

---
