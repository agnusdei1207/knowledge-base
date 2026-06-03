+++
title = "348. 동기식 버스 (Synchronous Bus)"
date = 2026-03-27

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) ([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 모든 참여 장치가 하나의 공통 클럭 ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/))을 기준으로 같은 시점에 주소, 제어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 시간 합의형 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조다.
> 2. **가치**: 별도의 복잡한 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)-응답 없이 정해진 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사이클 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Cycle)만 맞추면 되므로 제어가 단순하고, 짧은 거리에서는 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 예측 가능한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 얻기 쉽다.
> 3. **판단 포인트**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심은 클럭을 높이는 것이 아니라, 가장 느린 장치의 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)·클럭 스큐 ([Clock Skew](/knowledge-base/studynote/05_database/06_dw_olap_trends/388_spanner_truetime_clock_skew/))·배선 길이를 모두 감당할 수 있는 범위 안에서 동기성을 유지하는 데 있다.

---

## Ⅰ. 개요 및 필요성

동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) ([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 연결된 장치들이 <strong>언제 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>를 내보내고 언제 읽을지</strong>를 공통 클럭으로 합의한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 방식이다. 즉, 중앙처리장치 (Central Processing Unit, CPU), 메모리, 주변 장치가 제각각 "준비됐나?"를 계속 묻는 대신, 클럭 에지 ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) Edge)가 오면 미리 약속된 동작을 수행한다.

이 방식이 필요해진 이유는 고속 장치 사이 통신에서 제어 오버헤드가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 갉아먹기 때문이다. CPU와 주기억장치가 나노초 (ns) 단위로 동작하는 환경에서는 매 전송마다 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 주고받는 것보다, 1사이클에는 주소를 놓고 2사이클 뒤에는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽는 식으로 타이밍을 고정하는 편이 훨씬 효율적이다. 그래서 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 특히 메인보드 내부의 짧고 빠른 경로, 예를 들어 과거의 [프론트 사이드 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/365_fsb/) (Front Side [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), [FSB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/365_fsb/))나 동기식 메모리 인터페이스에서 강점을 보였다.

하지만 전제도 분명하다. 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 연결된 장치들이 정해진 시간 안에 응답할 수 있어야 한다. 이 약속이 깨지면 빠른 장치는 아직 준비되지 않은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽고, 시스템 전체는 오류나 대기 상태에 빠진다. 결국 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 "빠른 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)"이기 전에 "시간 약속이 지켜지는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)"다.

- **📢 섹션 요약 비유**: 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 모두가 종소리에 맞춰 움직이는 단체 줄넘기와 같다. 종이 울리는 순간에 맞춰 뛰면 빠르고 질서정연하지만, 한 사람이라도 박자를 놓치면 전체 흐름이 꼬인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 핵심은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사이클을 미리 정의하는 것이다. 보통 마스터 장치가 주소와 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 제어를 먼저 내보내고, 슬레이브 장치는 정해진 클럭 수 안에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실어 보낸다. 따라서 제어 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)는 단순하지만, 타이밍 예산은 더 엄격해진다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 클럭 ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/)) | 모든 전송의 기준 시점 제공 | 주기, 지터 (Jitter), 스큐 관리 |
| 주소선 (Address Lines) | 접근 대상 지정 | 클럭 에지 전 안정화 필요 |
| 제어선 (Control Lines) | 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 유효 구간 지시 | 사이클 정의가 명확해야 함 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)선 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lines) | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 | 셋업/홀드 시간 충족 필요 |
| 대기 상태 (Wait [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) | 느린 장치 대응용 완충 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하와 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)의 절충 |

아래 그림은 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 "정해진 클럭 수 뒤에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽는다"는 사실을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│            Synchronous Bus Cycle : fixed timing contract            │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────┤
│ Clock        │      C1      │      C2      │      C3      │    C4    │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────┤
│ Master       │ Addr + Read  │ Hold control │ Sample data  │ Finish   │
│ Slave        │ Decode addr  │ Access data  │ Drive bus    │ Release  │
│ Data bus     │    ----      │    ----      │  VALID DATA  │   ----   │
├──────────────┴──────────────┴──────────────┴──────────────┴──────────┤
│ Rule: data must become valid by the agreed sampling edge.           │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조에서 가장 중요한 식은 간단하다. <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/133_clock_cycle_time/">클럭 주기</a> ≥ 주소 해석 시간 + 장치 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a> + 배선 <a href="/knowledge-base/studynote/03_network/01_data_communication/016_전파_지연/">전파 지연</a> + 안전 마진</strong>이어야 한다. 메모리가 이 시간 안에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 올리지 못하면, 마스터는 잘못된 값을 읽게 된다. 그래서 실제 시스템은 느린 장치를 위해 대기 상태를 삽입하거나, 아예 빠른 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)와 느린 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 분리한다.

또 하나의 핵심은 물리 한계다. 클럭이 빨라질수록 배선 길이 차이에서 생기는 클럭 스큐가 더 치명적이 된다. 인쇄회로기판 (Printed Circuit Board, PCB) 위에서 몇 밀리미터 차이도 고속 인터페이스에서는 무시하기 어렵기 때문에, 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계만이 아니라 배선 정합까지 포함한 타이밍 공학이다.

- **📢 섹션 요약 비유**: 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 벨트 속도가 정해진 공장 컨베이어와 같다. 작업자들이 벨트 박자를 정확히 알고 있으면 빠르게 물건을 넘길 수 있지만, 누군가 제시간에 올려놓지 못하면 다음 공정이 빈손으로 지나가 버린다.

---

## Ⅲ. 비교 및 연결

동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 경계는 [비동기식 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/) ([Asynchronous Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/))와 비교할 때 가장 또렷해진다. 동기식은 공통 시간축이 있는 대신 거리와 속도 차이에 약하고, 비동기식은 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)-응답 기반이라 유연하지만 제어 오버헤드가 크다.

| 항목 | 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | [비동기식 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/) |
| :-- | :-- | :-- |
| 시간 기준 | 공통 클럭 | 요청-응답 핸드셰이크 |
| 장점 | 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 단순한 제어, 예측 가능한 사이클 | 이기종 장치 수용, 거리 확장, 유연한 응답 |
| 약점 | 가장 느린 장치에 영향, 클럭 스큐 민감 | 오버헤드 증가, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 변동 큼 |
| 적합 환경 | 칩 내부, 메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), 짧은 보드 레벨 연결 | 외부 장치, 장거리 링크, 저속 혼재 환경 |

이 비교는 다른 컴퓨터구조 개념과도 바로 이어진다. 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 동기식 동적 램 ([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) Dynamic Random Access Memory, [SDRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/252_sdram/))과 이중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송률 ([Double Data Rate](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/253_ddr_sdram/), DDR) 계열 메모리의 기반 철학이며, 동시에 멀티클럭 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 설계의 출발점이기도 하다. 반대로 [비동기식 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/)는 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 중심의 입출력 (Input/Output, I/O) 인터페이스 사고방식과 닿아 있다.

즉, 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 이해한다는 것은 단순히 "클럭이 있다"를 외우는 것이 아니라, <strong>공통 시간축이 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 올리는 대신 시스템 경계를 더 엄격하게 만든다</strong>는 점을 이해하는 것이다. 그래서 현대 시스템은 빠른 구간은 동기식으로 묶고, 경계에서는 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)와 버퍼로 비동기성을 흡수하는 계층형 구조를 선택한다.

- **📢 섹션 요약 비유**: 동기식은 군악대 행진처럼 모두가 같은 박자로 움직이는 방식이고, 비동기식은 서로 눈짓을 하며 합을 맞추는 소규모 합주와 같다. 전자는 웅장하고 빠르지만 규율이 필요하고, 후자는 유연하지만 템포가 흔들리기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 쓸지 판단할 때는 "클럭 공유가 가능한가"를 먼저 본다. 장치 간 거리가 짧고, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 편차가 작고, 높은 대역폭이 우선이라면 동기식이 유리하다. 반대로 장치 속도가 제각각이거나 배선 거리가 길다면, 클럭 분배 비용과 타이밍 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 비용이 급격히 커진다.

### 실무 판단 체크포인트

1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a> 상한</strong>: 가장 느린 장치도 정해진 사이클 안에 응답할 수 있는가?
2. **배선 길이 제어**: 보드 배선 길이와 스큐를 관리할 수 있는가?
3. **대기 상태 허용도**: 느린 장치를 위해 wait state를 넣어도 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표를 만족하는가?
4. <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 분리 필요성</strong>: 고속 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)와 저속 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)로 분리해야 하는가?

대표 사례는 [SDRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/252_sdram/) 계열 메모리다. 메모리 컨트롤러와 메모리는 같은 클럭 기준으로 명령과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받기 때문에 연속 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송에서 높은 효율을 낸다. 다만 속도가 올라갈수록 배선 정합, 타이밍 캘리브레이션, [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 관리가 필수이며, 이 부담을 감당하지 못하면 이론 대역폭은 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 이어지지 않는다.

안티패턴도 분명하다. 첫째, 느린 장치를 고속 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 무리하게 직접 매다는 설계다. 이 경우 wait state가 반복되어 빠른 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 장점이 사라진다. 둘째, 클럭 주파수만 높이고 보드 레이아웃과 타이밍 폐쇄를 가볍게 보는 접근이다. 이런 설계는 벤치마크보다 현장 장애를 먼저 만든다.

- **📢 섹션 요약 비유**: 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계는 고속도로 제한속도 표지판만 세우는 일이 아니다. 노면 상태, 차 간격, 진입로 길이까지 맞아야 진짜로 그 속도를 안전하게 낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 가장 큰 효과는 예측 가능성이다. [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사이클이 고정되면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 분석, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 파이프라인 설계가 쉬워지고, 짧은 구간에서는 매우 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 안정적으로 낼 수 있다. 그래서 프로세서 내부 인터커넥트와 메모리 인터페이스는 오랫동안 동기식 철학을 중심으로 발전해 왔다.

하지만 한계도 분명하다. 클럭을 공유해야 하므로 물리적 거리 확장에 불리하고, 서로 다른 속도의 장치를 자연스럽게 수용하기 어렵다. 결국 현대 아키텍처는 "모든 곳을 동기식으로 통일"하지 않고, 고속 핵심 구간에서만 동기식을 강하게 적용한 뒤 경계에서는 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/), 버퍼, 패킷 기반 인터커넥트로 문제를 푼다.

따라서 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 "무조건 빠른 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)"로 기억하기보다, <strong>공통 시간 기준을 무기로 단순성과 고속성을 얻는 대신, 물리 제약과 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">호환성</a> 비용을 떠안는 구조</strong>로 기억하는 것이 정확하다. 기술사 관점에서도 핵심은 장점 암기가 아니라, 어디까지 동기성을 유지하고 어디서 경계를 끊을지 판단하는 데 있다.

- **📢 섹션 요약 비유**: 좋은 지휘자는 무조건 빠른 템포만 고집하지 않는다. 모든 연주자가 정확히 맞출 수 있는 범위 안에서 템포를 정해야 합주가 아름답게 완성된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 클럭 ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/)) | 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 공통 시간 기준이며 모든 전송 타이밍의 출발점 |
| 대기 상태 (Wait [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) | 느린 장치를 수용하기 위한 예외 처리이자 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 요인 |
| 클럭 스큐 ([Clock Skew](/knowledge-base/studynote/05_database/06_dw_olap_trends/388_spanner_truetime_clock_skew/)) | 고속 동기식 설계에서 배선 길이 차이로 생기는 대표 위험 |
| [SDRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/252_sdram/) ([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) Dynamic Random Access Memory) | 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 철학이 메모리 인터페이스로 구현된 대표 사례 |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)) | 서로 다른 속도·[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 연결하며 경계를 완충하는 장치 |

### 📈 관련 키워드 및 발전 흐름도

```text
공통 시간 기준 수립
    │
    ▼
동기식 버스 (Synchronous Bus)
    │
    ├─▶ 고정 버스 사이클 · 버스트 전송
    │
    ▼
SDRAM (Synchronous Dynamic Random Access Memory)
    │
    ▼
DDR (Double Data Rate) 계열 고속 메모리
    │
    ▼
멀티버스 구조 · 브리지 · 클럭 도메인 분리
```

이 흐름은 "시간 합의"에서 출발해 "고속 메모리 최적화"로 발전하고, 이후에는 다시 "경계 분리"와 "[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 관리"로 확장되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 동기식 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 친구들이 모두 같은 북소리를 듣고 동시에 움직이는 놀이예요.
2. 북소리에 맞추면 아주 빨리 물건을 주고받을 수 있지만, 느린 친구가 있으면 모두 그 친구 속도에 맞춰야 해요.
3. 그래서 가까이 있는 빠른 친구들끼리는 이 방법이 좋고, 멀리 있거나 느린 친구와는 다른 방법이 더 잘 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 349 / 803

← **이전**: [347. 제어 버스 (Control Bus)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)
**다음**: [349. 비동기식 버스 (Asynchronous Bus)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/) →

---
