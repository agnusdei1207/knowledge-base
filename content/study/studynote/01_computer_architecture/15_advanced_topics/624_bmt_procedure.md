+++
weight = 624
title = "624. BMT (Bench Mark Test) 절차 및 평가 항목"
date = "2026-05-08"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[450_benchmark_test|벤치마크 테스트]] (BMT, Bench Mark Test)는 장비 도입 전에 실제 업무와 유사한 부하를 걸어, 후보 시스템의 [[282_performance_tactics|성능]]·[[452_availability|가용성]]·운영성을 객관적으로 비교하는 [[395_verification_process_review|검증]] 절차다.
> 2. **가치**: 카탈로그의 최대 [[139_throughput|처리량]] 대신, 조직이 정의한 [[001_dikw_pyramid|데이터]] 크기·동시 사용자·[[015_지연_데이터_관점|지연]] 기준·장애 시나리오를 동일 조건에서 시험함으로써 구매 실패 위험을 크게 줄인다.
> 3. **판단 포인트**: 좋은 BMT는 최고 속도 한 번이 아니라 p95/p99 [[015_지연_데이터_관점|지연]], 장애 [[658_ir_recovery|복구]] 시간, 운영 편의성, 재현성을 함께 본다.

---

## Ⅰ. 개요 및 필요성

BMT는 서버, 스토리지, [[002_database_definition|데이터베이스]] 장비, 네트워크 장비를 실제 도입하기 전에 시험 환경에서 [[395_verification_process_review|검증]]하는 절차다. 핵심은 "무엇이 가장 빠른가"보다 "우리 업무 조건에서 누가 안정적으로 요구 수준을 만족하는가"를 [[396_validation|확인]]하는 데 있다. 그래서 BMT는 단순 기술 테스트가 아니라, 조달과 운영을 연결하는 의사결정 단계라고 볼 수 있다.

BMT가 필요한 이유는 제조사 스펙이 대개 특정 조건에서 측정된 최댓값이기 때문이다. 예를 들어 저장장치가 4KB, 100% 읽기, 큐 깊이 최대 조건에서 100만 IOPS를 낸다고 해도, 실제 업무가 64KB 혼합 읽기/[[289_cqrs_db|쓰기]]와 높은 동시성으로 움직인다면 체감 [[282_performance_tactics|성능]]은 크게 다를 수 있다. 결국 구매자는 자기 업무 패턴을 반영한 [[395_verification_process_review|검증]] 없이는 "빠른 장비"가 아니라 "우리 환경에서 맞는 장비"를 고르기 어렵다.

특히 공공·금융·대형 기업 환경에서는 한 번의 장비 선정이 수년의 운영 안정성을 좌우한다. 따라서 BMT는 단순한 기술 비교가 아니라, 장애 비용과 재도입 비용을 줄이는 **사전 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 통제 장치**로 이해해야 한다.

- **📢 섹션 요약 비유**: BMT는 광고만 보고 차를 사지 않고, 내가 매일 다니는 언덕길과 막히는 출근길에서 직접 시승해 보는 절차와 같다. 화려한 카탈로그보다 내 길에서의 실제 반응이 더 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 BMT는 요구사항 정의부터 점수화까지 단계가 분명해야 한다. 먼저 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약 ([[085_sla|SLA]], [[085_sla|Service Level Agreement]]), 목표 [[658_ir_recovery|복구]] 시간 ([[176_rto_recovery_time_objective|RTO]], [[176_rto_recovery_time_objective|Recovery Time Objective]]), 목표 [[658_ir_recovery|복구]] 시점 ([[177_rpo_recovery_point_objective|RPO]], [[177_rpo_recovery_point_objective|Recovery Point Objective]]) 같은 운영 기준을 수치로 확정한다. 그 다음 생산계와 유사한 [[001_dikw_pyramid|데이터]]셋, 동시 사용자 수, 읽기/[[289_cqrs_db|쓰기]] 비율, 배치 작업 패턴을 설계하고, 후보 장비들을 같은 조건에서 반복 측정한다.

| 단계 | 수행 내용 | 대표 평가 항목 |
| :-- | :-- | :-- |
| 요구사항 정의 | [[085_sla|SLA]], 용량, [[015_지연_데이터_관점|지연]] 목표, 장애 허용 범위 확정 | p95/p99 [[015_지연_데이터_관점|지연]], [[139_throughput|처리량]], [[658_ir_recovery|복구]] 시간 |
| 시험 환경 구축 | 네트워크, OS, [[288_version_ihl_tos_total_length|버전]], [[009_config|설정]] 기준 통일 | 비교 공정성, 재현성 |
| [[282_performance_tactics|성능]] 시험 | 정상 부하·최대 부하·혼합 부하 실행 | TPS/IOPS, CPU headroom, tail [[141_latency|latency]] |
| [[452_availability|가용성]] 시험 | 디스크, [[587_nic_offloading|NIC]], 전원, 노드 장애 주입 | [[300_failover_architecture|Failover]] 시간, [[001_dikw_pyramid|데이터]] 손실 여부 |
| 운영성 평가 | 설치, 증설, 모니터링, 알람, [[555_backup_and_restore_strategy|백업]] [[396_validation|확인]] | 관리 편의성, 자동화 수준 |

아래 흐름은 BMT가 단순 벤치마크 한 번이 아니라, 사전 기준을 둔 의사결정 과정임을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│            BMT flow: same workload, same rules, measurable result         │
├────────────────────────────────────────────────────────────────────────────┤
│  Requirement                                                               │
│      │                                                                     │
│      ▼                                                                     │
│  Workload Model -> Testbed Setup -> Run & Repeat -> Fault Injection       │
│      │                                │                    │               │
│      └─────────────── Scorecard & Pass/Fail Decision ─────┘               │
└────────────────────────────────────────────────────────────────────────────┘
```

이 과정에서 중요한 것은 워밍업 구간과 정상 상태 구간을 분리하고, 평균값뿐 아니라 꼬리 [[015_지연_데이터_관점|지연]]과 자원 여유율을 함께 보는 것이다. 또한 장애 시험은 단순 핑 손실이 아니라 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 절체, [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], 운영 알람까지 [[396_validation|확인]]해야 한다. BMT의 품질은 테스트 도구보다 **조건 통제와 평가 기준의 명확성**에서 결정된다.

- **📢 섹션 요약 비유**: BMT는 한 번의 달리기 기록만 보는 체력장이 아니라, 오래 뛰기·비 오는 날 달리기·넘어졌다 다시 일어나기까지 함께 보는 종합 체력 검사와 같다.

---

## Ⅲ. 비교 및 연결

실무에서는 개념 증명 (PoC, Proof of [[120_concept|Concept]])과 BMT를 자주 혼동하지만 목적이 다르다. PoC는 "이 기술이 우리 문제를 해결할 가능성이 있는가"를 빠르게 [[396_validation|확인]]하는 탐색 단계이고, BMT는 "도입 후보 중 누가 요구 기준을 안정적으로 만족하는가"를 비교하는 [[395_verification_process_review|검증]] 단계다. 또한 구매 이후 장비가 계약 조건에 맞게 납품되었는지 [[396_validation|확인]]하는 인수 시험 ([[525_fat_file_allocation_table|FAT]]/[[103_chaining|SAT]], Factory/Site [[406_acceptance_test_uat|Acceptance Test]])과도 구분해야 한다.

| 구분 | 질문 | 시점 | 결과물 |
| :-- | :-- | :-- | :-- |
| PoC | 적용 가능성은 있는가? | 도입 검토 초반 | 기술 적합성 판단 |
| BMT | 후보 장비 중 누가 기준을 만족하는가? | 제안·선정 단계 | 점수표, 우선협상 근거 |
| [[525_fat_file_allocation_table|FAT]]/[[103_chaining|SAT]] | 계약 장비가 약속대로 납품·설치되었는가? | 구매 이후 | 인수 승인 근거 |

BMT는 다른 운영 지표와도 연결된다. 예를 들어 고가용성 장비라면 [[176_rto_recovery_time_objective|RTO]], [[177_rpo_recovery_point_objective|RPO]], 절체 성공률을 함께 봐야 하고, [[002_database_definition|데이터베이스]] 장비라면 표준 [[282_performance_tactics|성능]]평가위원회 ([[154_tpc|TPC]], [[191_transaction_concept_states|Transaction]] Processing [[282_performance_tactics|Performance]] Council) 벤치마크 같은 참고 지표와 자체 실부하 시험을 같이 활용할 수 있다. 즉 BMT는 단독 이벤트가 아니라, SLA와 인수 기준을 수치로 연결하는 중간 다리다.

- **📢 섹션 요약 비유**: PoC는 메뉴 시식회, BMT는 본선 요리 대회, [[525_fat_file_allocation_table|FAT]]/SAT는 배달 온 음식이 주문서와 맞는지 [[396_validation|확인]]하는 단계와 같다. 이름은 비슷해 보여도 묻는 질문이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 좋은 BMT를 만들려면 먼저 합격 기준을 벤더 시험 전에 확정해야 한다. 예를 들어 "p99 [[015_지연_데이터_관점|지연]] 50ms 이하, 노드 장애 시 30초 내 절체, 72시간 안정 운전, 운영 알람 자동 연동"처럼 수치와 조건을 먼저 못 박아야, 시험 중에 기준이 흔들리지 않는다. 또한 [[001_dikw_pyramid|데이터]]셋은 익명화하더라도 실제 분포와 크기를 반영해야 하며, 후보별 튜닝 허용 범위도 동일하게 맞춰야 공정성이 유지된다.

기술사 관점의 체크리스트는 다음과 같다.

1. 평균 응답시간이 아니라 p95/p99 [[015_지연_데이터_관점|지연]]과 자원 여유율을 함께 보는가?
2. 정상 부하, 피크 부하, 장시간 안정성 시험이 모두 포함되는가?
3. 장애 주입 시 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]], 절체 시간, 운영 알람까지 [[395_verification_process_review|검증]]하는가?
4. [[282_performance_tactics|성능]] 40, [[452_availability|가용성]] 30, 운영성 20, 비용 10처럼 가중치가 사전에 정의돼 있는가?

흔한 실패는 벤더가 잘하는 스크립트만 돌리고 끝내는 것이다. 또 하나의 실패는 최고 [[139_throughput|처리량]] 숫자만 보고 선택해, 실제 운영에서 꼬리 [[015_지연_데이터_관점|지연]]이나 장애 [[658_ir_recovery|복구]]가 나쁜 장비를 뽑는 경우다. BMT의 목표는 우승 기록이 아니라 **운영 가능한 장비를 증거 기반으로 고르는 것**이라는 점을 잊지 말아야 한다.

- **📢 섹션 요약 비유**: 시험 범위를 미리 정하지 않으면 학생이 잘하는 문제만 풀고도 만점처럼 보일 수 있다. BMT는 전 과목과 실전 상황까지 포함해 진짜 실력을 보게 만드는 감독 규칙이다.

---

## Ⅴ. 기대효과 및 결론

BMT를 제대로 수행하면 장비 선정의 실패 확률을 줄이고, 운영 중 예상치 못한 병목과 [[658_ir_recovery|복구]] 문제를 사전에 발견할 수 있다. 또한 벤더 제안서의 추상적 표현을 수치와 로그로 바꾸어, 내부 승인과 [[606_auditing_linux_auditd|감사]] 대응에도 강한 근거를 남길 수 있다. 대규모 사업일수록 이 문서화 효과는 기술적 효과만큼 중요하다.

물론 BMT가 모든 미래를 보장하지는 않는다. 생산계 [[001_dikw_pyramid|데이터]] 변화, 사용자 증가, 소프트웨어 [[288_version_ihl_tos_total_length|버전]] 차이로 실제 운영 결과는 달라질 수 있으므로, 도입 후에도 주기적 재검증과 모니터링이 필요하다. 그래도 BMT는 "감으로 사는 장비"를 "증거로 고르는 장비"로 바꾸는 핵심 절차다. 이 주제는 결국 **벤더 스펙을 믿을 것인가가 아니라, 우리 기준으로 증명시킬 것인가의 문제**로 기억하면 된다.

- **📢 섹션 요약 비유**: BMT는 큰 시험 전에 미리 실전 모의고사를 치러 보는 것과 같다. 점수를 미리 [[396_validation|확인]]하면 본시험에서 놀랄 일이 줄어든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약 ([[085_sla|SLA]], [[085_sla|Service Level Agreement]]) | BMT의 합격 기준을 정의하는 출발점 |
| 개념 증명 (PoC, Proof of [[120_concept|Concept]]) | BMT 이전 단계의 기술 가능성 검토 |
| 꼬리 [[015_지연_데이터_관점|지연]] (Tail [[141_latency|Latency]]) | 평균값만으로 숨겨지는 실사용 체감 [[282_performance_tactics|성능]] 문제 |
| 절체 ([[300_failover_architecture|Failover]]) | [[452_availability|가용성]] 시험에서 반드시 [[396_validation|확인]]할 핵심 동작 |
| 인수 시험 ([[525_fat_file_allocation_table|FAT]]/[[103_chaining|SAT]], Factory/Site [[406_acceptance_test_uat|Acceptance Test]]) | 구매 이후 계약 이행 여부를 [[396_validation|확인]]하는 후속 절차 |

### 📈 관련 키워드 및 발전 흐름도

```text
요구사항 · SLA 정의
    │
    ▼
워크로드 모델링 · 시험 환경 통일
    │
    ▼
성능 · 가용성 · 운영성 반복 측정
    │
    ▼
점수화 · 우선순위 결정
    │
    ▼
도입 이후 FAT/SAT 및 운영 검증 연계
```

이 흐름은 BMT가 단발 테스트가 아니라, 선정·구매·운영 [[395_verification_process_review|검증]]을 잇는 연속 절차임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. BMT는 새 자전거를 사기 전에 진짜 길에서 타 보고 고르는 시험이에요.
2. 빨리 달리는지만 보는 게 아니라, 오래 타도 괜찮은지와 넘어졌을 때 잘 버티는지도 함께 봐요.
3. 그래서 BMT를 하면 멋져 보이기만 하는 자전거보다 정말 잘 탈 수 있는 자전거를 고를 수 있답니다.
