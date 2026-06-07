---
title: "057. Shared Pool Oracle Sga"
date: "2026-06-07"
tags:
  - "database"
  - "studynote-database"
weight: 57
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공유 풀(Shared Pool)은 [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) SGA (System Global Area) 안에서 SQL 문장과 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 재사용하도록 돕는 메모리 영역이다.
> 2. **가치**: [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 캐시와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 딕셔너리 캐시가 하드 파싱을 줄여 CPU 낭비를 크게 줄인다.
> 3. **판단 포인트**: [바인드 변수](/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/)([Bind Variable](/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/)) 사용, 파싱 재사용, 파편화 관리가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 반복해서 같은 SQL을 분석하는 비용이 크다. 그래서 자주 쓰는 SQL과 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 공유 풀에 올려 재사용한다.

공유 풀이 없으면 파싱 비용이 계속 쌓이고, CPU는 같은 일을 반복하느라 바빠진다. 대규모 [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 환경에서는 이 차이가 바로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이로 이어진다.

- **📢 섹션 요약 비유**: 공유 풀은 자주 읽는 참고서를 책상 위에 올려 둔 공간이다.

---

## Ⅱ. 공유 풀의 구성 요소

공유 풀은 크게 두 개의 캐시로 나뉜다.

- <strong><a href="/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">Library</a> Cache</strong>: SQL 문장, 파스 트리(Parse Tree), [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)([Execution Plan](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/))을 저장한다.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/056_data_dictionary_cache/">Data Dictionary Cache</a></strong>: 테이블, 컬럼, 권한, 객체 정보 같은 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 저장한다.

```text
SQL 입력
   v
Library Cache 확인
   +- Hit -> Soft Parse
   +- Miss -> Hard Parse
            v
Data Dictionary Cache 확인
```

이 구조 덕분에 같은 SQL은 다시 분석하지 않고 재사용할 수 있다.

- **📢 섹션 요약 비유**: 자주 묻는 질문을 미리 적어 둔 FAQ 게시판과 같다.

---

## Ⅲ. 파싱과 하드 파싱 문제

SQL이 들어오면 Oracle은 먼저 공유 풀에서 같은 문장이 있었는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 있으면 소프트 파싱(Soft Parse), 없으면 하드 파싱(Hard Parse)을 수행한다.

하드 파싱은 문법 분석, 권한 검사, 최적화까지 새로 해야 하므로 비용이 크다. 개발자가 리터럴 값을 많이 박아 넣으면 동일한 로직도 서로 다른 SQL로 인식되어 하드 파싱이 늘어난다.

- **📢 섹션 요약 비유**: 매번 새 문제집을 만드는 대신, 이미 푼 문제를 다시 꺼내 보는 것이 소프트 파싱이다.

---

## Ⅳ. 파편화와 튜닝 포인트

공유 풀은 무작정 크게만 잡는다고 좋은 것이 아니다. 메모리가 파편화되거나, [바인드 변수](/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/)를 쓰지 않거나, [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴이 제각각이면 효율이 떨어진다.

실무에서는 다음을 본다.

- [바인드 변수](/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/) 사용 여부
- 하드 파싱 비율
- [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 캐시 [적중률](/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/)
- [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 조회 빈도
- 불필요한 SQL 문자열 다양성

파편화가 심하면 같은 메모리도 잘게 쪼개져 효율이 떨어진다. 그래서 공유 풀은 "크기"보다 "재사용 패턴"이 더 중요하다.

- **📢 섹션 요약 비유**: 정리 안 된 서랍은 넓어도 찾기 어렵고, 자주 쓰는 물건이 한곳에 모여 있어야 빨리 꺼낼 수 있다.

---

## Ⅴ. 다른 SGA 영역과의 비교

SGA의 다른 영역과 비교하면 공유 풀의 역할이 더 분명해진다.

- <strong><a href="/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/">Buffer Cache</a></strong>: 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록을 저장한다.
- <strong><a href="/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/">Redo</a> Log Buffer</strong>: 변경 이력을 임시로 저장한다.
- **Shared Pool**: SQL과 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 저장한다.

이 세 영역이 각각 제 역할을 해야 Oracle이 안정적으로 빠르게 동작한다.

- **📢 섹션 요약 비유**: 같은 창고라도 재료, 메모, 작업 지시서를 따로 보관해야 혼동이 없다.

---

## 관련 개념 맵

```text
SQL 입력
   v
공유 풀
   +- Library Cache
   +- Data Dictionary Cache
   v
Soft Parse / Hard Parse
   v
CPU 절감 / 성능 향상
```

---

## 관련 키워드 및 발전 흐름도

1. 하드 파싱 중심 구조 -> CPU 낭비 증가
2. [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 캐시 -> [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 재사용
3. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 딕셔너리 캐시 -> [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 조회 가속
4. [바인드 변수](/studynote/05_database/03_relational_model/190_bind_variable_soft_parsing/) -> SQL 재사용률 향상
5. 공유 풀 튜닝 -> [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 안정화

---

## 어린이를 위한 3줄 비유 설명

공유 풀은 자주 보는 책과 노트를 책상 위에 올려 두는 거예요.
그러면 같은 문제를 다시 풀 때 훨씬 빨라져요.
매번 책장까지 뛰어갈 필요가 없거든요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 600

<- **이전**: [56. 데이터 사전 캐시 (Data Dictionary Cache)](/studynote/05_database/01_db_architecture_relational/056_data_dictionary_cache/)
**다음**: [58. 데이터베이스 인스턴스 (Database Instance) - 메모리와 백그라운드 프로세스](/studynote/05_database/01_db_architecture_relational/058_database_instance_architecture/) ->

---
