---
title: "Pipe-Filter Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)
1. **본질**: [파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/)([Pipe-Filter](/studynote/04_software_engineering/04_testing_quality/207_pipe_filter_architecture_data_stream/) Pattern)은 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 독립 필터가 순차 또는 병렬로 변환하고, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)가 그 결과를 다음 단계로 전달하는 [데이터 중심](/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/) 처리 구조다.
2. **가치**: 필터 재사용, 단계별 병렬화, 장애 격리, 점진적 확장이 쉬워 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 처리·스트리밍 변환·추출·변환·적재(Extract, Transform, Load, [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)) 흐름에 강하다.
3. **판단 포인트**: 필터의 독립성, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식 표준화, 순서 보장, 버퍼링과 백프레셔(Back Pressure) 제어가 확보되어야 구조 이점이 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 이어진다.

## Ⅰ. 개요 및 필요성
[파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/)은 유닉스(Unix) 셸 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)처럼 “작은 처리기를 연결해 큰 흐름을 만든다”는 철학을 가진다. 각 필터는 하나의 역할에 집중하고, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다음 단계로 넘긴다. 감리 관점에서는 전체 거대 프로그램보다 단계별 책임과 입력·출력 계약이 분리되어 추적 가능한지가 핵심이다.

이 구조가 필요한 이유는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 요구가 점점 복잡해지고 실시간성이 커졌기 때문이다. [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/), 미디어 변환, 이벤트 정제, [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 전처리처럼 한 덩어리 코드로 처리하면 변경 영향이 크고 병목 지점을 찾기 어렵다. 반면 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 구조는 문제를 작은 변환 단계로 나누어 확장성과 유지보수성을 높인다.

```text
+--------+   +--------+   +--------+   +--------+
| Source |--->|Filter A|--->|Filter B|--->| Sink   |
+--------+   +--------+   +--------+   +--------+
```

시험에서는 단순히 “[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 흐른다”가 아니라, 각 필터가 독립적으로 교체 가능하며 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)가 단계 간 결합도를 낮춘다는 점을 써야 한다. 여기에 스트리밍 처리와 단계별 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 용이성을 붙이면 답안이 더 실무적으로 보인다.
- **📢 섹션 요약 비유**: 빨래를 세탁-헹굼-탈수로 나눠 맡기면 각 기계가 자기 일만 잘해도 전체 빨래가 깔끔해지는 세탁 공정과 같다.

## Ⅱ. 아키텍처 및 핵심 원리
[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 아키텍처의 핵심은 필터가 이전 단계 내부를 몰라도 입력 형식만 맞으면 동작한다는 점이다. 따라서 필터는 높은 [응집도](/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/), 낮은 결합도를 가져야 하며, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식과 전달 순서를 안정적으로 보장해야 한다. 필터는 상태가 거의 없을수록 재사용과 확장이 쉽다.

| 구성 요소 | 핵심 원리 | 감리 포인트 |
| --- | --- | --- |
| 필터 | 입력을 받아 특정 규칙으로 변환 후 표준 출력 형식으로 내보낸다. | 단일 책임, [무상태성](/studynote/07_enterprise_systems/03_eai_esb_msa/162_rest_statelessness/), 오류 처리 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) | 단계 사이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 채널 역할을 한다. | 포맷 표준화, 순서 보장, 버퍼 크기와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 검토 |
| 종단 처리 | 시작점은 수집하고 끝점은 저장·전송·시각화한다. | 재시도, [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/), 실패 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 기준 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 운영 제어 | 모니터링과 병목 분석으로 필터별 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 최적화한다. | 백프레셔 제어, 관측성, 확장 단위 검토 |

```text
+----------+   +----------+   +----------+   +----------+
| Ingest   |--->| Normalize|--->| Enrich   |--->| Publish  |
+----+-----+   +----+-----+   +----+-----+   +----+-----+
     |              |              |              |
     +--------------+------Audit / Metrics--------+
```

핵심 원리는 표준 입력·표준 출력, 단계적 분리, 조합 가능성이다. 예를 들어 새로운 정제 규칙이 필요하면 해당 필터만 바꾸면 되므로 전체 시스템 재작성 부담이 작다. 다만 필터 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식이 불안정하거나 특정 필터가 상태를 과도하게 가지면 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터의 장점이 급감한다.
- **📢 섹션 요약 비유**: 공장 컨베이어벨트에서 각 작업자가 한 공정만 맡으면 숙련도와 속도가 올라가지만, 중간 규격이 제각각이면 다음 작업자가 바로 일할 수 없는 것과 같다.

## Ⅲ. 비교 및 연결
[파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/)은 일괄 배치 프로그램이나 [블랙보드 패턴](/studynote/04_software_engineering/04_testing_quality/209_blackboard_pattern_ai_heuristic/)과 비교해 설명하면 특징이 명확해진다. 핵심은 순차적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환과 공용 문제 공간 기반 협업의 차이다.

| 비교 항목 | [파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/) | 일괄 배치 프로그램 | [블랙보드 패턴](/studynote/04_software_engineering/04_testing_quality/209_blackboard_pattern_ai_heuristic/) |
| --- | --- | --- | --- |
| 처리 흐름 | 단계별 연속 변환 | 한 번에 묶어서 처리 | 부분 해답을 공유 공간에 누적 |
| 결합 구조 | 필터 간 느슨한 연결 | 내부 로직이 한 덩어리 | 모듈이 공용 상태에 간접 결합 |
| 적합 분야 | 스트리밍, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 미디어, [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 정기 대량 처리 | 탐색형·비정형 문제 |
| 주의점 | 포맷 변화와 병목 관리 필요 | 변경 영향이 큼 | 제어기와 상태 표현이 복잡 |

연결 개념으로는 메시지 큐, 이벤트 스트림, 함수형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리, 미디어 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 있다. 기술사 답안에서는 필터의 독립성과 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 표준 계약을 강조해 “변환 공정 설계” 관점으로 서술하면 좋다.
- **📢 섹션 요약 비유**: 도시락을 한 번에 통째로 만드는 것은 일괄 배치이고, 반찬을 순서대로 조리해 옆 사람에게 넘기는 것은 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터다.

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름이 명확하고 변환 단계가 잘 분리될수록 [파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/)이 강력하다. 반대로 단계마다 서로의 내부 상태를 깊게 알아야 하거나 실시간 상호 피드백이 많으면 다른 구조가 더 적합할 수 있다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 필터별 입력·출력 형식이 명확하고 표준화되어 있는가?
- 특정 필터가 과도한 상태를 가지지 않아 독립 배포·교체가 가능한가?
- 장애 발생 시 어느 필터에서 병목이 생겼는지 추적 가능한가?
- 재처리와 중복 처리에 대비한 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 설계가 되어 있는가?
- 스트리밍 환경에서 버퍼, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 백프레셔 제어가 가능한가?

기술사 답안에서는 “필터 추가가 쉽다”에 더해 “표준 포맷 없으면 유지보수 지옥이 된다”는 경고를 함께 쓰는 것이 중요하다. 또한 운영 관점에서는 각 단계의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간과 오류율을 측정할 수 있어야 구조의 실제 가치를 입증할 수 있다.
- **📢 섹션 요약 비유**: 급식 줄에서 앞사람이 너무 느리면 뒤가 막히듯, 필터 하나가 느리면 전체 흐름이 멈추니 줄의 속도를 같이 봐야 한다.

## Ⅴ. 기대효과 및 결론
기대효과는 분명하다. 첫째, 작은 단계 조합으로 대형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 유연하게 구성할 수 있다. 둘째, 필터 단위 재사용으로 개발 속도와 테스트 효율이 높아진다. 셋째, 병목 위치가 명확해 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선과 확장이 수월하다.

결론적으로 [파이프-필터 패턴](/studynote/11_design_supervision/02_architecture_principles/134_pipe_filter_pattern/)은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환을 큰 덩어리 로직이 아니라 연결 가능한 작은 공정으로 바라보게 만든다. 기술사 시험에서는 필터 독립성, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 계약, 스트리밍 적합성, 병목 관리라는 네 요소를 중심으로 쓰면 구조적 완성도가 높다.
- **📢 섹션 요약 비유**: 레고 블록을 이어 긴 기차를 만들듯, 작은 객차를 잘 연결하면 목적에 따라 길고 빠른 열차를 쉽게 만들 수 있다.

### 📌 관련 개념 맵
- <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/">스트림 처리</a>(<a href="/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/">Stream Processing</a>)</strong>: 흐르는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 끊지 않고 즉시 변환·분석하는 처리 방식
- <strong>메시지 큐(Message <a href="/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong>: [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 역할을 비동기적으로 수행하는 대표 구현 수단
- <strong><a href="/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a>(<a href="/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/">Idempotency</a>)</strong>: 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 번 처리해도 결과가 같도록 보장하는 성질
- <strong>관측성(<a href="/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/">Observability</a>)</strong>: 필터별 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 오류, 처리량을 추적해 병목을 찾는 운영 역량

### 📈 관련 키워드 및 발전 흐름도
```text
단일 배치 프로그램
    v
유닉스 셸 파이프 조합
    v
ETL 단계 분리
    v
실시간 스트림 처리
    v
관측 가능한 데이터 파이프라인
```

### 👶 어린이를 위한 3줄 비유 설명
1. 사과를 씻고, 자르고, 접시에 담는 일을 한 사람이 다 하지 않고 차례로 맡는 거예요.
2. 앞사람이 한 일을 다음 사람이 받아서 자기 일만 하면 돼요.
3. 그래서 새 일이 생기면 중간 사람 하나만 바꿔도 전체가 더 좋아질 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 511 / 530

<- **이전**: [432. 블랙보드 패턴 전문가 모듈 AI 초기 구조망 (Blackboard Pattern)](/studynote/11_design_supervision/06_exam_summary/432_architecture/)
**다음**: [434. 컴포저블 아키텍처 PBS API 조합 유연 모듈 (Composable Architecture with PBS API)](/studynote/11_design_supervision/06_exam_summary/434_pbs_api/) ->

---
