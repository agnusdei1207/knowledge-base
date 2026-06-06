---
title: "086. Process View Sequence Diagram Concurrency"
date: "2026-04-10"
tags:
  - "studynote-design"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 뷰([Process](/studynote/12_it_management/05_security_compliance/943_process/) [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))는 실행 중인 프로세스와 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/))의 동시 동작을 설명하는 동적 설계 관점이다.
> 2. **가치**: 경합, [교착 상태](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/), 병목을 미리 보게 해 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성을 같이 설계할 수 있다.
> 3. **판단 포인트**: 프로세스, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/), [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/studynote/12_it_management/05_security_compliance/943_process/) Communication)를 구분해 부하 기준으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다.

---

## Ⅰ. 개요 및 필요성
프로세스 뷰([Process](/studynote/12_it_management/05_security_compliance/943_process/) [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))는 Kruchten의 4+1 [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) Model에서 실행 시점의 구조를 보여 준다. 정적 다이어그램만으로는 보이지 않는 입출력(I/O, Input/Output) 대기, 자원 경합, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간 협업을 드러내기 때문에 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 중심 시스템에서 중요하다.

즉, 이 뷰는 “무엇이 존재하는가”가 아니라 “무엇이 동시에 움직이는가”를 묻는다.
- **📢 섹션 요약 비유**: 사람이 많은 복도는 출입문과 동선까지 봐야 이해된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 구성 요소 | 역할 | 설계 포인트 |
|:---|:---|:---|
| 프로세스 | 자원 경계와 격리 단위 | 장애 격리 |
| [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) | 실행 흐름 | 공유 상태 경합 |
| [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) | [mutex](/studynote/02_operating_system/04_synchronization/223_mutex/) ([mutual exclusion](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)), [semaphore](/studynote/02_operating_system/04_synchronization/224_semaphore/) |
| [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/studynote/12_it_management/05_security_compliance/943_process/) Communication) | [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 직렬화 비용 |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 | 처리량과 응답시간 | 큐 길이, 꼬리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |

+---------+ request +------------------+
| [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/)  |-------->|   [Process](/studynote/12_it_management/05_security_compliance/943_process/) A      |
+---------+        |  +------------+  |
                   |  | [Thread Pool](/studynote/02_operating_system/02_process_thread/103_thread_pool/) |  |
                   |  +--+----+----+  |
                   |     |    |       |
                   |   +-v+ +-v+      |
                   |   |T1| |T2|      |
                   |   +-++ +-++      |
                   |     | [lock](/studynote/05_database/04_transactions_concurrency/510_lock/)      |
                   |  +--v--------+  |
                   |  | Shared    |  |
                   |  | [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)     |  |
                   |  +--+--------+  |
                   +-----+-----------+
                         v
                   +----------+
                   |[Database](/studynote/05_database/04_transactions_concurrency/501_database/)  |
                   +----------+
- **📢 섹션 요약 비유**: 누가 동시에 움직이고 어디서 막히는지 보는 지도다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | [Process](/studynote/12_it_management/05_security_compliance/943_process/) [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) | [Logical View](/studynote/11_design_supervision/02_architecture_principles/085_logical_view_class_diagram_functional_requirements/) | Development [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) | Physical [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) |
|:---|:---|:---|:---|:---|
| 주 질문 | 동시에 무엇이 실행되는가 | 기능이 무엇인가 | 어떤 모듈로 나뉘는가 | 어디에 배치되는가 |
| 위험 | 경합, 교착, 과부하 | 요구 누락 | [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 증가 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 장애 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/), [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 덤프 | 시나리오 검토 | 의존성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 배치 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

[Process](/studynote/12_it_management/05_security_compliance/943_process/) View는 다른 뷰를 대체하지 않고, 실행 문제를 보완한다.
- **📢 섹션 요약 비유**: 정적 설계와 실행 설계는 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- [ ] [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수를 CPU (Central Processing Unit) 코어 수와 단순 1:1로 보지 않는다.
- [ ] 공유 상태는 소유자와 수명 주기를 먼저 정한다.
- [ ] 입출력(I/O) 대기, [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), 재시도 정책을 함께 설계한다.
- [ ] [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/)에서 평균뿐 아니라 꼬리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 큐 길이를 본다.
- [ ] [교착 상태](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)와 기아가 재현되는 시나리오를 만든다.

- ❌ 하나의 거대한 mutex로 전체 요청을 잠그는 설계
- ❌ 블로킹 I/O를 메인 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 그대로 두는 설계
- ❌ [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수만 늘리면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 오른다고 가정하는 태도
- **📢 섹션 요약 비유**: 한 줄로 다 잠그면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 같이 묶인다.

---

## Ⅴ. 기대효과 및 결론
프로세스 뷰는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 사후 장애가 아니라 사전 설계 문제로 바꾼다. [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 구조를 먼저 모델링해야 병목을 설계 단계에서 줄일 수 있다.
- **📢 섹션 요약 비유**: [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 그림이 있으면 튜닝이 감이 아니라 근거가 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 프로세스 뷰 | 실행 중 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)의 전체 그림이다. |
| [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/) | 요청을 나눠 처리량을 높인다. |
| [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/studynote/12_it_management/05_security_compliance/943_process/) Communication) | 프로세스 간 협력 비용을 드러낸다. |
| [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 공유 자원 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)와 경합 제어를 맡는다. |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 | 병목이 어디서 생기는지 알려 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
요구사항 -> 동시성 시나리오 -> 프로세스/스레드 분해 -> IPC·동기화 설계 -> 부하 테스트 -> 병목 분석
```

### 👶 어린이를 위한 3줄 비유 설명

1. 식당에서 손님 동선과 주방 동선을 같이 그려야 안 막힌다.
2. 주문표가 여러 사람 손을 거치면, 누가 어디서 기다리는지 알아야 빨라진다.
3. 문이 열리는 순서까지 봐야 건물이 덜 막힌다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 530

<- **이전**: [85. 논리 뷰 (Logical View) - 최종 사용자 요구사항 개념 설계](/studynote/11_design_supervision/02_architecture_principles/085_logical_view_class_diagram_functional_requirements/)
**다음**: [87. 구현 뷰 (Implementation View) - 소프트웨어 모듈 컴포넌트 설계](/studynote/11_design_supervision/02_architecture_principles/087_implementation_view_component_diagram_packaging/) ->

---
