---
title: 769. 데드락 희생자 롤백 복구망 (Deadlock Victim Rollback Recovery)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데드락 희생자 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[658_ir_recovery|복구]] ([[243_deadlock_recovery|Deadlock Recovery]] & [[313_rollback|Rollback]])는 시스템이 꼬리 물기 식의 영원한 멈춤([[281_deadlock_definition|교착 상태]])에 빠졌을 때, 이를 해결하기 위해 **관련된 프로세스 중 가장 만만한 녀석(희생자, Victim)을 골라 강제로 죽이거나 뒤로 후퇴시켜 자원을 뱉어내게 만드는 응급 수술 메커니즘**이다.
> 2. **가치**: 데드락 예방(Prevention)이나 회피(Avoidance)처럼 미리 깐깐하게 검사해서 시스템 [[282_performance_tactics|성능]]을 갉아먹는 대신, 일단 자유롭게 놔두다가 사고가 터지면 그때 가서 최소한의 피해로 엉킨 실타래를 끊어내어 **[[001_operating_system_purpose|운영체제]]의 [[139_throughput|처리량]]([[139_throughput|Throughput]])과 생존율을 동시에 확보**한다.
> 3. **융합**: [[001_operating_system_purpose|운영체제]] 차원에서는 프로세스 강제 종료(Kill)라는 투박한 방식을 쓰지만, [[002_database_definition|데이터베이스]]([[502_dbms|DBMS]]) [[191_transaction_concept_states|트랜잭션]] 시스템과 융합되면서 피해를 최소화하는 '세이브포인트([[200_savepoint_partial_rollback|Savepoint]]) 기반 부분 [[098_rollback_strategy_pipeline_error_threshold|롤백]]'과 '기아([[314_starvation_prevention|Starvation]]) 방지 [[001_algorithm_definition|알고리즘]]'으로 고도로 정교화되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 4가지 데드락 발생 조건([[283_mutual_exclusion|상호 배제]], [[231_hold_and_wait|점유 대기]], [[285_no_preemption|비선점]], 환형 대기)이 겹쳐 완전히 굳어버린 시스템에서, 탐지기([[961_deepfake_detection|Detection]] [[001_algorithm_definition|Algorithm]])가 데드락을 발견한 직후 취하는 사후 조치([[658_ir_recovery|Recovery]])다.
  - **[[310_victim_selection|희생자 선택]] ([[310_victim_selection|Victim Selection]])**: 엉켜있는 프로세스들 중 누구의 목을 칠 것인가를 수학적 비용(Cost) 모델로 계산한다.
  - **[[098_rollback_strategy_pipeline_error_threshold|롤백]] ([[313_rollback|Rollback]])**: 희생자로 선정된 프로세스가 하던 일을 몽땅 취소하고 시작 전 상태나 안전한 중간 저장 지점으로 강제 후퇴시키는 작업이다.

- **필요성(문제의식)**: 
  - 데드락이 발생하면 A, B, C 프로세스는 서로의 자원을 원하며 영원히 기다린다. 놔두면 서버를 물리적으로 재부팅해야 한다.
  - 은행원의 [[001_algorithm_definition|알고리즘]](회피)처럼 미리 데드락을 피하려고 매번 검사하면 서버 속도가 반토막 난다.
  - **해결책**: "어차피 데드락은 1년에 한두 번 날까 말까다. 차라리 평소엔 쌩쌩하게 달리게 내버려 두고, 아주 가끔 데드락이 났을 때만 **가장 피해가 적은 한 놈만 골라 패서(Kill/[[313_rollback|Rollback]]) 꼬인 걸 풀자!**"

  - 좁은 외나무다리 한가운데서 양방향으로 오던 자동차 4대가 코가 맞닿아 꽉 끼어버렸다(데드락). 서로 뒤로 안 물러나면 영원히 집에 못 간다.
  - **[[310_victim_selection|희생자 선택]]**: 경찰(OS)이 출동해서 4대 중 "가장 작고 후진하기 편한 경차(가장 비용이 적은 프로세스)"를 골라 희생자로 지목한다.
  - **[[098_rollback_strategy_pipeline_error_threshold|롤백]]**: 지목당한 경차는 어쩔 수 없이 왔던 길을 빙빙 후진해서 다리 밖으로 돌아 나가고([[098_rollback_strategy_pipeline_error_threshold|롤백]], 자원 토해냄), 나머지 3대의 큰 차들이 무사히 지나간 뒤에야 경차는 다시 다리를 건널 수 있다.

- **등장 배경**: 
  - 예방 및 회피 [[001_algorithm_definition|알고리즘]]의 막대한 런타임 오버헤드를 견디지 못한 상용 [[002_database_definition|데이터베이스]] 엔진([[188_pl_sql_t_sql_procedural|Oracle]], MySQL)과 [[001_operating_system_purpose|운영체제]]들이, '사후 약방문'이 가장 현실적인 최적의 가성비(Cost-effective) 솔루션임을 깨닫고 도입한 방어 체계다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 데드락 탐지 및 희생자 롤백 복구 시퀀스 시각화           │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │   [ 1. 데드락 발생 (환형 대기, Circular Wait) ]                   │
  │     P1(DB 업데이트) ──(Lock A 점유)──▶ 기다림 ──(Lock B 요청)──┐ │
  │        ▲                                               │ │
  │        │                                               ▼ │
  │   (Lock A 요청) ◀──기다림 ──(Lock B 점유)── P2(통계 배치 작업)   │
  │                                                             │
  │   [ 2. 데드락 탐지기 (Detection Algorithm) 작동 ]                │
  │     - OS: "이봐, P1과 P2가 서로 맞물려서 사이클(Cycle)이 생겼어!"      │
  │                                                             │
  │   [ 3. 희생자 선택 (Victim Selection) ]                         │
  │     - P1 비용: 99% 진행 완료, 중요도 높음, 롤백 비용 수만 클럭.         │
  │     - P2 비용: 방금 1% 진행 시작함, 중요도 낮음, 롤백 비용 저렴.         │
  │     ▶ OS의 판결: "P2, 네가 희생자(Victim)다! 죽어라!"               │
  │                                                             │
  │   [ 4. 롤백(Rollback) 및 복구 ]                                │
  │     - P2를 강제 종료(또는 중간 지점으로 후퇴) 시킴.                    │
  │     - P2가 쥐고 있던 [Lock B]가 허공에 툭 떨어짐! 🔓                │
  │     - 꽉 막혀있던 P1이 Lock B를 낚아채고 정상적으로 실행 마침. 🚀        │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 그림은 데드락 [[658_ir_recovery|복구]]의 냉혹하고도 기계적인 자본주의 철학을 보여준다. [[281_deadlock_definition|교착 상태]]라는 꽉 막힌 사거리를 뚫는 유일한 방법은 누군가 가진 자원([[510_lock|Lock]])을 강제로 빼앗는 것(Preemption)뿐이다. 하지만 무턱대고 아무나 죽이면 기껏 1시간 동안 연산해 둔 아까운 [[001_dikw_pyramid|데이터]]를 통째로 날릴 수 있다. 따라서 [[001_operating_system_purpose|운영체제]]와 DB 엔진은 [[216_progress_in_synchronization|진행]] 상황, 우선순위, 소모한 자원의 양을 종합적으로 계산하여 가장 '값싼' 녀석(P2)의 모가지를 친다. 죽은 P2는 자원을 토해내고, 이로 인해 고리가 끊기며 시스템 전체에 다시 피가 돌기 시작한다.

- **📢 섹션 요약 비유**: 두 마리의 뱀이 서로의 꼬리를 물고 삼키려다 둥글게 굳어버렸을 때, 어쩔 수 없이 덜 예쁜 뱀의 꼬리(희생자)를 칼로 살짝 잘라내어([[098_rollback_strategy_pipeline_error_threshold|롤백]]) 엉킨 고리를 풀고 둘 다 살려내는 정밀한 응급 외과 수술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[310_victim_selection|희생자 선택]] [[001_algorithm_definition|알고리즘]] ([[310_victim_selection|Victim Selection]] Criteria)

"누구를 죽여야 시스템의 타격이 가장 적은가?" 아키텍트는 아래의 항목들을 [[267_weight_bias_activation|가중치]]로 두어 [[658_ir_recovery|복구]] 비용(Cost) 함수를 짠다.

1. **프로세스의 우선순위 (Priority)**: 백그라운드 배치 작업보다는 사용자 대화형 UI 응답 프로세스를 살린다.
2. **[[216_progress_in_synchronization|진행]]도 (Computation Time)**: 지금까지 10시간 동안 연산한 프로세스(죽이면 10시간 날아감)를 살리고, 방금 5초 전에 시작한 프로세스를 죽인다.
3. **사용 중인 자원의 수**: 락을 100개나 쥐고 있는 무거운 놈을 죽일 것인가, 1개 쥔 가벼운 놈을 죽일 것인가? (보통 가벼운 놈을 죽여 국소적으로 푸는 것을 선호한다).
4. **종료 후 복원 비용**: 죽였을 때 이 프로세스를 처음부터 다시 실행하기 위한 [[501_file_definition_logical_record|파일]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] 오버헤드가 얼마나 큰지 계산한다.

### [[098_rollback_strategy_pipeline_error_threshold|롤백]] ([[313_rollback|Rollback]])의 2가지 아키텍처적 깊이

희생자를 골랐다면, 얼만큼 뒤로 후퇴시킬 것인가에 대한 [[268_strategy_pattern|전략]]이 나뉜다.

| [[098_rollback_strategy_pipeline_error_threshold|롤백]] 종류 | 원리 및 동작 메커니즘 | 장점 및 단점 | 적용 분야 |
|:---|:---|:---|:---|
| **전체 [[098_rollback_strategy_pipeline_error_threshold|롤백]] (Total [[313_rollback|Rollback]])** | 프로세스를 묻지도 따지지도 않고 `kill` (Aborted). 완전히 소멸시키고 처음부터 재시작(Restart) 시킨다. | **장점**: 구현이 극도로 쉽다. OS 단의 기본 조치.<br>**단점**: 여태껏 [[216_progress_in_synchronization|진행]]한 수십 분 치의 연산 비용이 허공에 다 날아간다. | 일반적인 [[001_operating_system_purpose|운영체제]] 프로세스 ([[157_oom_killer|OOM]] 킬러 등) |
| **부분 [[098_rollback_strategy_pipeline_error_threshold|롤백]] (Partial [[313_rollback|Rollback]])**| 프로세스가 작업을 하며 주기적으로 저장해 둔 '체크포인트(Checkpoint/[[200_savepoint_partial_rollback|Savepoint]])'로 시간을 되돌린다. 얽힌 락만 살짝 푸는 수준까지만 [[098_rollback_strategy_pipeline_error_threshold|롤백]]. | **장점**: 잃어버리는 연산 자원을 극소화하여 [[658_ir_recovery|복구]] 속도가 압도적으로 빠르다.<br>**단점**: OS가 시스템의 모든 상태를 틈틈이 백업해야 하므로 런타임 오버헤드가 존재한다. | 엔터프라이즈 [[002_database_definition|데이터베이스]] ([[502_dbms|DBMS]] [[191_transaction_concept_states|트랜잭션]] [[098_rollback_strategy_pipeline_error_threshold|롤백]]) |

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 세이브포인트(Savepoint) 기반의 부분 롤백 매커니즘         │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 희생자 프로세스의 타임라인 ]                                        │
  │   시작 ──▶ [SP 1 저장] ──▶ 연산 ──▶ [SP 2 저장] ──▶ Lock 요청(데드락 펑!) │
  │                                                                   │
  │   [ 일반적인 전체 롤백 ]                                              │
  │   전부 폐기하고 `시작` 지점으로 강제 환생! (지금까지의 작업 100% 날아감)         │
  │   ◀─────────────────────────────────────────────────────────────  │
  │                                                                   │
  │   [ 우아한 부분 롤백 (Partial Rollback) ]                            │
  │   데드락을 일으킨 그 Lock 요청 직전의 가장 안전한 저장소인 [SP 2] 로만 후퇴!     │
  │                                            ◀───────────────────   │
  │   ※ 결과: SP 2 시점에서 쥐고 있던 불법 락만 살짝 토해내어 데드락 고리를 끊어냄.    │
  │           앞선 99%의 연산 내용은 고스란히 살려서 연산 낭비(Cost)를 극도로 줄임.  │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 부분 [[098_rollback_strategy_pipeline_error_threshold|롤백]]은 시간을 되돌리는 마법사다. 게임을 하다가 보스한테 죽었다고 게임을 처음 튜토리얼부터 다시 하는(전체 [[098_rollback_strategy_pipeline_error_threshold|롤백]]) 바보는 없다. 가장 최근에 저장해 둔 모닥불 세이브 포인트([[166_sp|SP]] 2)에서 되살아나서 보스전만 다시 치르는 것이 정상이다. [[002_database_definition|데이터베이스]] [[191_transaction_concept_states|트랜잭션]] 시스템(예: [[188_pl_sql_t_sql_procedural|Oracle]], PostgreSQL)이 위대하게 평가받는 이유가 바로 이 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 트리의 촘촘한 세이브포인트 구축 능력 덕분이며, 이를 통해 데드락 희생자가 되더라도 수십만 줄의 이전 [[298_qkv_attention|쿼리]] 연산을 안전하게 보존한다.

- **📢 섹션 요약 비유**: 문서 작성을 하다가 프로그램이 멈췄을 때, 저장 안 한 3시간 치 문서가 모조리 다 날아가서 멘붕이 오는 것(전체 [[098_rollback_strategy_pipeline_error_threshold|롤백]])과, 5분 전에 "자동 저장(부분 [[098_rollback_strategy_pipeline_error_threshold|롤백]])"된 [[501_file_definition_logical_record|파일]]이 열려 5분 치만 다시 쓰면 되는 완벽한 심리적 안정감의 차이입니다.

---

## Ⅲ. 비교 및 연결

### 데드락 처리의 4대 사상 (예방 vs 회피 vs 탐지/[[658_ir_recovery|복구]] vs 무시)

시스템의 목적(보안이냐 속도냐)에 따라 아키텍트가 취하는 [[001_operating_system_purpose|운영체제]] 설계 사상은 완전히 다르다.

| 접근 사상 | 핵심 [[268_strategy_pattern|전략]] | 치명적인 단점 (Trade-off) | 사용 환경 |
|:---|:---|:---|:---|
| **1. 예방 (Prevention)** | 락을 줄 때 [[231_hold_and_wait|점유 대기]], [[286_circular_wait|순환 대기]] 등 데드락 조건 4가지 중 하나를 아예 법으로 원천 차단함. | 제약이 너무 심해 자원 낭비가 극심함 (예: 필요 없는 락까지 한 번에 다 잡아야만 실행 허가) | 제어 시스템 (보수적) |
| **2. 회피 (Avoidance)** | 은행원의 [[001_algorithm_definition|알고리즘]]처럼, 락을 줄 때마다 이 락을 주면 데드락이 날지 시뮬레이션([[298_safe_state|안전 상태]] 계산)해 보고 줌. | 매번 행렬 계산을 돌려야 하므로 **CPU 오버헤드가 극악으로 무거워 시스템이 느려짐.** | 이론적 모델링 |
| **3. 탐지 & [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[658_ir_recovery|복구]]** | 평소엔 막 쓰게 놔두다 데드락 터지면 **희생자를 찾아 죽여버림(Kill).** | 누군가 한 명은 죽거나 연산을 잃는 피해를 감수해야 함. **(희생자 발생)** | **현대 [[002_database_definition|데이터베이스]](DB)**, [[191_transaction_concept_states|트랜잭션]] 시스템 |
| **4. 무시 (Ostrich)** | "데드락? 1년에 한 번 날까 말까 한데 뭘 막아. 터지면 걍 사용자가 껐다 켜라." [[291_ostrich_algorithm|타조 알고리즘]]. | 뻗으면 리부팅해야 하는 무식함. | **Windows, Linux** 등 거의 모든 현대 범용 OS |

### 과목 융합 관점

- **[[002_database_definition|데이터베이스]] ([[304_deadlock_detection|교착 상태 탐지]] [[092_thread_lwp|스레드]])**: [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[658_ir_recovery|복구]]망이 가장 화려하게 피어난 곳이 [[002_database_definition|데이터베이스]]다. MySQL(InnoDB)은 백그라운드에 `lock_wait_timeout`과 탐지 [[092_thread_lwp|스레드]]를 둔다. 두 [[191_transaction_concept_states|트랜잭션]]이 서로의 Row(행)를 쥐고 `Update` 데드락을 유발하면, InnoDB는 1초도 안 돼서 사이클을 감지하고, "지금까지 Insert/Update 한 [[001_dikw_pyramid|데이터]]([[393_undo|Undo]] [[568_logs_distributed_logging_elk_fluentd|로그]] 양)가 더 적은" [[191_transaction_concept_states|트랜잭션]], 즉 만만한 놈을 즉각 에러(`Deadlock found when trying to get lock; try restarting transaction`)와 함께 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 시켜버리고 하나를 구출한다.
- **[[136_variance|분산]] 시스템 ([[136_variance|분산]] 데드락)**: 단일 서버가 아니라 클라우드의 노드 A, 노드 B, 노드 C 간에 네트워크 락이 얽혀버리는 [[136_variance|분산]] 데드락 상황에서는 글로벌 탐지기가 없다. 이때는 락 획득 [[573_timeout_retry_backoff_strategy|타임아웃]]([[319_timeout_prevention|Timeout]])이라는 무식하지만 확실한 기법을 쓴다. "내가 락 요청하고 5초 동안 안 오면, 아 이거 [[136_variance|분산]] 데드락 났구나" 하고 스스로 [[098_rollback_strategy_pipeline_error_threshold|롤백]]해 버리는(자기 희생) 자율적 파훼법을 사용한다.

- **📢 섹션 요약 비유**: 예방이 '모든 길에 중앙분리대를 쳐서 유턴을 원천 금지'하는 답답한 도로라면, 탐지/[[658_ir_recovery|복구]]는 '차들이 맘대로 다니게 놔두다가, 사거리가 꽉 막히면 경찰 헬기가 떠서 한 대만 강제로 견인차로 들어 올려 빼버리는' 가장 빠르고 현실적인 미국식 자본주의 교통 체계입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 운영 [[128_water_scrum_fall_anti_pattern|안티패턴]]

1. **시나리오 — 배치 서버의 특정 Job만 계속 죽는 기아([[314_starvation_prevention|Starvation]]) 현상**: 밤마다 도는 거대한 DB 정산 배치 프로그램이 자꾸 데드락 희생자로 선정되어 에러를 뿜으며 죽는다. 매번 죽어서 처음부터 다시 도느라 아침 출근 전까지 정산이 끝나지 않는 심각한 비즈니스 장애가 터졌다.
   - **원인 분석**: 데드락 희생자를 고르는 비용 계산 로직이 "지금까지 연산한 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 비용이 가장 싼 놈"이나 "특정 우선순위가 낮은 놈"만 계속 때리도록 편향되어 있었다. 하필 그 배치 프로세스가 항상 타겟이 된 것이다. 한 번 죽고 다시 시작했는데, 또 데드락이 나서 또 그 녀석이 비용이 제일 낮아 또 지목당해 죽는 영원한 학대([[314_starvation_prevention|Starvation]])에 빠졌다.
   - **아키텍트 판단 ([[314_starvation_prevention|Starvation]] 방어 로직 추가)**: 아키텍트는 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 대상 선정 [[001_algorithm_definition|알고리즘]]에 **"희생 횟수([[313_rollback|Rollback]] Count)"** 파라미터를 반드시 추가해야 한다. "네가 비용이 제일 싸긴 한데, 너 방금 전에도 희생자로 뽑혀서 죽었었네? 그럼 이번엔 불쌍하니까 살려주고, 두 번째로 싼 저놈을 죽이자!"라고 판결을 틀어주는 [[267_weight_bias_activation|가중치]] 튜닝이 필수적이다. 희생자의 공평한 로테이션이 이루어져야 특정 작업이 무한 굴레에 빠지는 것을 막을 수 있다.

2. **시나리오 — 클라이언트 앱의 무한 멈춤(Hang) 및 데드락 에러 미처리**: 스마트폰 뱅킹 앱에서 이체를 눌렀는데 로딩만 뜨고 아무 반응이 없다. 서버 [[568_logs_distributed_logging_elk_fluentd|로그]]를 보니 "[[281_deadlock_definition|Deadlock]] victim [[098_rollback_strategy_pipeline_error_threshold|롤백]]" 처리가 되어 정상적으로 [[002_database_definition|데이터베이스]] 엉킴은 풀렸는데, 앱은 그대로 멈춰있다.
   - **원인 분석**: DB가 데드락을 감지하고 B [[191_transaction_concept_states|트랜잭션]]을 희생자로 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 시키면서 에러(Exception)를 웹 서버로 던졌다. 그런데 주니어 백엔드 개발자가 이 에러를 `try-catch`로 먹어버리고 그냥 로직을 종료해 버린 것이다. 클라이언트는 실패 응답조차 받지 못해 무한 로딩에 빠졌다.
   - **아키텍트 판단 (애플리케이션 계층의 Retry 아키텍처)**: 데드락 희생자로 지목당해 [[098_rollback_strategy_pipeline_error_threshold|롤백]]당하는 것은 '코드의 버그'가 아니라 고도로 동시성이 높은 시스템에서 발생하는 '자연스러운 기상 현상(교통 체증)'이다. 따라서 데드락 에러(예: MySQL Error 1213)를 캐치했다면, 쫄지 말고 **아무 일도 없었다는 듯이 [[191_transaction_concept_states|트랜잭션]]을 처음부터 다시 묶어서 재시도(Retry)하는 로직**을 애플리케이션 프레임워크(Spring Retry 등) 단에 반드시 캡슐화해 두어야 한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 안전한 데드락 예외 처리(Exception Handling) 설계 템플릿     │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   int retry_count = 0;                                            │
  │   while (retry_count < MAX_RETRIES) {                             │
  │       try {                                                       │
  │           [ 트랜잭션 시작 (Begin) ]                                  │
  │           // ... 복잡한 다중 테이블 Insert / Update 수행 ...          │
  │           [ 트랜잭션 완료 (Commit) ]                                 │
  │           break;  // 🟢 성공 시 즉시 탈출!                           │
  │                                                                   │
  │       } catch (DeadlockVictimException e) {                       │
  │           // 🚨 내가 희생자(Victim)로 지목당해 롤백당했다!                │
  │           retry_count++;                                          │
  │           if (retry_count == MAX_RETRIES) throw e; // 최종 실패 처리  │
  │                                                                   │
  │           // 다시 충돌하는 걸 피하기 위해 짧게 랜덤 백오프(Sleep) 대기        │
  │           sleep(random(10, 100) ms);                              │
  │           // 🔄 while 문을 타고 트랜잭션을 처음부터 씩씩하게 재시도함!        │
  │       }                                                           │
  │   }                                                               │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 코드는 클라우드 및 대용량 [[191_transaction_concept_states|트랜잭션]] 아키텍처의 필수 교양이다. OS나 DB가 나를 희생양으로 삼아 [[098_rollback_strategy_pipeline_error_threshold|롤백]]시켰다고 분노할 필요가 없다. 희생양의 미덕은 "조용히 한 템포 쉬었다가, 방해꾼이 지나간 빈 다리로 다시 건너가는 것"이다. 약간의 랜덤 대기 시간(Exponential Backoff)을 주어 동시 진입을 비틀어버린 후 재시도(Retry)하면, 사용자([[003_audit_stakeholders|Client]]) 눈에는 단지 로딩 바가 0.1초 정도 더 돌아가고 완벽하게 결제가 성공한 것처럼 보이는 환상의 에러 복원력을 갖추게 된다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **단일 우선순위 몰빵**: 운영 환경에서 희생자를 안 당하게 하겠다고, 모든 앱 [[092_thread_lwp|스레드]]의 우선순위를 Max로 높여버리거나, [[191_transaction_concept_states|트랜잭션]] 비용 [[267_weight_bias_activation|가중치]]를 똑같이 줘버리는 세팅. 이러면 탐지기가 "누굴 죽여야 할지" 비용 구분을 못 해서, 랜덤으로 막 죽이거나 심지어 해결을 못 하고 탐지기 자체가 뻗어버리는 극단적 Livelock에 빠진다. 모든 프로세스는 명확한 계급과 비용 체계의 차등을 두어야 시스템이 수술할 수 있다.

- **📢 섹션 요약 비유**: 왕따(기아 현상)를 당해 계속 가위바위보에서 지고 짐을 옮기는 불쌍한 친구(프로세스)에게 "넌 방금 한 번 희생했으니 이번 가위바위보는 무적 패스야"라고 룰([[267_weight_bias_activation|가중치]])을 고쳐주어 골고루 희생하게 만들어주는 다정한 선생님(아키텍트)의 배려입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 예방/회피 [[001_algorithm_definition|알고리즘]](Banker's) 고집 | 탐지 및 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[658_ir_recovery|복구]] 채택 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (시스템 스루풋)**| 매 [[041_resource_allocation|자원 할당]]마다 행렬 계산 오버헤드 30% 발생 | [[041_resource_allocation|자원 할당]] 시 오버헤드 0 (그냥 줌) | 평상시 런타임 [[282_performance_tactics|성능]](TPS)의 비약적, 한계 돌파적 상승 |
| **정량 (자원 활용률)** | 보수적 예측으로 남는 자원도 대기시킴 (낭비) | 병렬로 락을 막 쓰므로 CPU 100% 점유 | 잠재적 병렬성([[266_other_transparency|Concurrency]])의 극대화 |
| **정성 (운영 유연성)** | 코드 작성 시 락 획득 순서를 강제해야 함 | 개발자가 락 순서 꼬이는 걸 두려워할 필요 감소| 데드락 공포 해방 및 [[658_ir_recovery|복구]] 로직 캡슐화로 생산성 향상 |

### 미래 전망
- **[[190_ai_llm_requirements_specification|AI]] 기반 데드락 예측 및 회피 융합**: 과거의 수학적 회피(은행원 [[001_algorithm_definition|알고리즘]])는 너무 무거웠지만, 런타임 [[615_ebpf|eBPF]] 모니터링과 [[190_ai_llm_requirements_specification|AI]] 머신러닝이 결합하여, A 앱과 B 앱이 특정 [[298_qkv_attention|쿼리]]를 칠 때 데드락이 날 확률을 딥러닝이 미리 직감하고 아주 미세한 [[015_지연_데이터_관점|지연]](Delay)을 삽입하여 아예 꼬임이 발생하지 않게 비틀어버리는 '스마트 회피'로 패러다임이 진화하고 있다.
- **[[136_variance|분산]] [[191_transaction_concept_states|트랜잭션]]의 [[549_2pc_two_phase_commit_limitations_msa|2PC]] / [[305_saga|Saga]] 패턴 [[098_rollback_strategy_pipeline_error_threshold|롤백]]**: 로컬 OS를 넘어 클라우드 [[532_microservices_decomposition_patterns|마이크로서비스]] 간에 얽힌 [[136_variance|분산]] 데드락과 [[098_rollback_strategy_pipeline_error_threshold|롤백]]을 처리하기 위해, 무거운 중앙 통제식 2-Phase Commit([[549_2pc_two_phase_commit_limitations_msa|2PC]]) 대신, 이벤트 기반으로 "실패 시 이전 [[014_api_posix|API]] 호출의 취소 요청([[551_compensating_transaction_logical_rollback|보상 트랜잭션]])"을 역순으로 쏘며 우아하게 부분 [[098_rollback_strategy_pipeline_error_threshold|롤백]]을 수행하는 [[305_saga|Saga]] 패턴이 [[136_variance|분산]] [[658_ir_recovery|복구]]망의 표준 아키텍처로 등극했다.

### 참고 표준
- **SQL 표준 (ANSI/ISO)**: [[191_transaction_concept_states|트랜잭션]] 격리 수준([[227_transaction_isolation_levels_ansi_sql_standard|Isolation Level]])과 데드락 조치에 대한 명세를 정의하며, 응용 프로그램이 데드락 희생자가 되었을 때 던져야 할 표준 에러 코드 인터페이스를 규정.
- **POSIX Threads ([[790_posix_threads_pthreads_standard_api|Pthreads]])**: [[281_deadlock_definition|교착 상태]]를 막기 위해 `pthread_mutex_trylock` 같은 넌블로킹 락 요청 인터페이스를 제공하여, 개발자 스스로 락 획득 실패 시 [[573_timeout_retry_backoff_strategy|타임아웃]]과 수동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]을 짤 수 있게 돕는 표준 [[014_api_posix|API]].

[[281_deadlock_definition|교착 상태]] 희생자 [[098_rollback_strategy_pipeline_error_threshold|롤백]]은 컴퓨터 공학이 "절대 [[003_integrity|무결성]]"이라는 순진한 강박을 버리고, "사고는 어차피 일어난다(Failure is inevitable). 중요한 건 얼마나 우아하고 싸게 사고를 수습하느냐다"라는 대인배적이고 실용적인 엔지니어링 철학으로 넘어온 가장 상징적인 분기점이다. 가장 약한 고리 하나를 희생양으로 삼아 거대한 시스템의 파멸을 구원하는 이 잔혹하고도 효율적인 트리아지(Triage) [[001_algorithm_definition|알고리즘]]은, 오늘도 전 세계 [[001_dikw_pyramid|데이터]]센터의 보이지 않는 혈관을 뚫어주며 디지털 경제를 지탱하고 있다.

- **📢 섹션 요약 비유**: 복잡하게 얽힌 이어폰 줄(데드락)을 풀려고 완벽한 공식을 찾느라 1시간 동안 낑낑대는 대신, 제일 싸구려 이어폰 줄(희생자) 하나를 가위로 툭 자르고([[098_rollback_strategy_pipeline_error_threshold|롤백]]) 1분 만에 음악을 다시 듣는(정상화) 극도의 실용주의적 문제 해결 방식입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[222_spinlock|스핀락]] 멀티 프로세서 전용 활용 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[768_cas_compare_and_swap_lock_free|CAS]] ([[768_cas_compare_and_swap_lock_free|Compare And Swap]]) [[158_instruction|명령어]] 기초 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[363_inverted_page_table|역 페이지 테이블]] 전역 해시 매핑 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[256_flash_memory|플래시 메모리]] [[479_wear_leveling|마모 평준화]] ([[479_wear_leveling|Wear Leveling]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[CAS (Compare And Swap) 명령어 기초]
    │
    ▼
[데드락 희생자 롤백 복구망 (Deadlock Victim Rollback Recovery)]
    │
    ├──▶ [역 페이지 테이블 전역 해시 매핑]
    └──▶ [플래시 메모리 마모 평준화 (Wear Leveling)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 좁은 외나무다리에서 양치기 소년과 덩치 큰 사냥꾼이 마주쳤어요. 서로 비키라며 한 발짝도 안 물러나서 다리가 꽉 막혀버렸죠(데드락).
2. 다리를 관리하는 촌장님([[001_operating_system_purpose|운영체제]])이 와서 딱 보더니, 덩치가 커서 뒤로 가기 힘든 사냥꾼 대신, 작고 몸이 가벼운 소년(가장 비용이 싼 희생자)에게 뒤로 돌아가라고 명령했어요.
3. 소년이 툴툴대며 다리 밖으로 돌아가 주니까([[098_rollback_strategy_pipeline_error_threshold|롤백]]), 사냥꾼이 무사히 다리를 건넜고, 그제야 소년도 다시 다리를 건널 수 있게 되어 마을의 교통 체증이 뻥 뚫렸답니다!
