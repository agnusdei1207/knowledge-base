---
title: "101. Lossless Join Decomposition"
date: "2026-06-07"
tags:
  - "database"
  - "studynote-database"
weight: 101
---
## 핵심 인사이트 (3줄 요약)
1. **본질**: 무손실 분해 (Lossless-[Join](/studynote/05_database/04_transactions_concurrency/521_join/) Decomposition)는 하나의 거대한 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 두 개로 분해한 후 다시 조인([Join](/studynote/05_database/04_transactions_concurrency/521_join/))했을 때, 원래의 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 100% 동일하게 복원됨을 수학적으로 보장하는 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 과정의 필수 조건이다.
2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 유실되는 것뿐만 아니라, 분해 전에는 없었던 가짜 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Spurious Tuples)가 생성되어 정보의 정확성이 심각하게 훼손되는 현상을 원천 차단한다.
3. **판단 포인트**: 두 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 쪼갤 때, 분해된 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 간의 공통 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 반드시 둘 중 최소 한 곳에서 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)(Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))나 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)([Candidate Key](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)) 역할을 해야만 무손실 분해가 성립한다.

---

## Ⅰ. 개요 및 필요성

무손실 분해는 관계형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 [이상 현상](/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)([Anomaly](/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 제거하기 위해 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 분해할 때 반드시 만족해야 하는 1원칙이다. [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 잘못 쪼개면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단순히 사라지는 것이 아니라, 교집합 정보의 부재로 인해 다시 조인([Join](/studynote/05_database/04_transactions_concurrency/521_join/))할 때 잘못된 행들이 조합되는 정보 손실(Loss of Information)이 발생한다.

[데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 핵심은 '중복의 최소화'와 '[무결성](/studynote/09_security/01_intro_principles/003_integrity/) 유지'다. 하지만 분해 과정에서 복원 가능성을 담보하지 않는다면, 쪼개진 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들은 원래 어떤 연관 관계를 가졌는지 알 수 없게 되어 쓸모없는 쓰레기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 전락한다. 따라서 모든 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 과정은 이 무손실 분해 원칙을 기저에 깔고 진행되어야 한다.

- **📢 섹션 요약 비유**: 무손실 분해는 거대한 종이 지도를 보관하기 위해 반으로 찢는 방법과 같다. 아무렇게나 찢으면 다시 붙일 때 길이 어긋나서 가짜 지도가 되지만, 양쪽에 똑같은 '정밀 마커(공통 키)'를 남기고 자르면 나중에 1mm 오차 없이 원래 지도를 100% 복원할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

무손실 분해의 핵심 원리는 '공통 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 통한 결정권 유지'에 있다. [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) $R$을 $R_1$과 $R_2$로 분해했을 때, 이 둘을 [자연 조인](/studynote/05_database/07_exam_summary/413_natural_join/)([Natural Join](/studynote/05_database/07_exam_summary/413_natural_join/))하면 정확히 $R$이 되어야 한다 ($R = R_1 \bowtie R_2$).

이를 수학적으로 보장하는 조건은 다음과 같다. $R_1 \[cap](/studynote/13_cloud_architecture/05_data_engineering/341_process/) R_2$ (공통 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))가 $R_1$ 또는 $R_2$의 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)(PK) 혹은 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)여야 한다. 즉, $R_1 \[cap](/studynote/13_cloud_architecture/05_data_engineering/341_process/) R_2 \rightarrow R_1$ 이거나 $R_1 \[cap](/studynote/13_cloud_architecture/05_data_engineering/341_process/) R_2 \rightarrow R_2$ 여야 한다는 뜻이다.

```text
+--------------------------------------------------------------+
|                  손실 분해 vs 무손실 분해                    |
+--------------------------------------------------------------+
| [원본 R (사번, 이름, 프로젝트)]                              |
|  (1, 김철수, A)                                              |
|  (2, 김철수, B)                                              |
|                                                              |
| [손실 분해 (이름 기준 쪼개기 - 이름은 PK가 아님)]            |
|  R1(사번, 이름)      R2(이름, 프로젝트)                      |
|  (1, 김철수)    bowtie  (김철수, A)                          |
|  (2, 김철수)            (김철수, B)                          |
|  => 결과: (1, 김철수, B)와 같은 '가짜 데이터' 뻥튀기 발생!   |
|                                                              |
| [무손실 분해 (사번 기준 쪼개기 - 사번이 PK)]                 |
|  R1(사번, 이름)      R2(사번, 프로젝트)                      |
|  (1, 김철수)    bowtie  (1, A)                               |
|  (2, 김철수)            (2, B)                               |
|  => 결과: 원래 데이터 100% 정확하게 복원 성공                |
+--------------------------------------------------------------+
```

이 다이어그램은 [결정자](/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) 역할을 하지 못하는 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(이름)을 기준으로 분해했을 때 왜 조인 결과가 카르테시안 곱([Cartesian Product](/studynote/05_database/07_exam_summary/412_cartesian_product/))처럼 부풀어 올라 가짜 행(Spurious Tuple)을 만드는지를 보여준다.

- **📢 섹션 요약 비유**: 두 개의 퍼즐 조각으로 나눌 때, 이어지는 부분이 밋밋한 일자면(일반 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) 나중에 어디든 맞출 수 있어 그림이 엉망이 되지만, 고유한 모양의 요철([기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/))을 만들어두면 오직 원래 짝과만 조립된다.

---

## Ⅲ. 비교 및 연결

분해 시 고려해야 할 또 다른 중요한 개념은 [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)([Dependency Preservation](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/))이다. 무손실 분해가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Tuple) 자체의 복원에 초점을 맞춘다면, [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)은 업무적 규칙(Functional Dependency)의 유지를 의미한다.

| 항목 | 무손실 분해 (Lossless-[Join](/studynote/05_database/04_transactions_concurrency/521_join/)) | [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/) ([Dependency Preservation](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)) |
| :--- | :--- | :--- |
| **목적** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조인 시 정보 손실/가짜 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 방지 | 쪼개진 후에도 원래의 [함수적 종속성](/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) 규칙 유지 |
| **조건** | 공통 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 최소 한 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)의 슈퍼키/후보키 | 원래 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)의 모든 FD가 분해된 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)들에서 유도 가능 |
| **강제성** | 모든 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)에서 **반드시** 만족해야 함 | [제3정규형](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)([3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/))까지는 보장, BCNF에서는 깨질 수 있음 |

[BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/)([Boyce-Codd Normal Form](/studynote/05_database/02_modeling_normalization/106_bcnf_boyce_codd_normal_form/))로 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)할 때, 무손실 분해는 항상 가능하지만 [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)은 불가능한 경우가 수학적으로 존재한다. 이때는 조회의 정합성(무손실)을 지킬지, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 룰([종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/))을 지킬지 트레이드오프가 발생한다.

- **📢 섹션 요약 비유**: 무손실 분해가 빵을 자르고 다시 붙였을 때 무게와 모양이 원래대로 복원되는 것이라면, [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)은 잘라낸 빵 안에 잼과 버터의 비율이 기존 레시피 규칙대로 그대로 남아있는지 확인하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링에서는 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 반정규화 사이에서 갈등하게 된다. [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 진행하면 [이상 현상](/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)은 줄어들지만 잦은 조인으로 인해 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하된다.

- **설계 판단**: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 모델링 단계에서는 반드시 무손실 분해 조건을 충족하는 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 끝까지 수행해야 한다. [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이슈는 그 이후 물리 모델링 단계에서 반정규화나 인덱싱으로 해결하는 것이 올바른 순서다.
- <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 처음부터 조인을 피하겠다고 무손실 분해 원칙을 무시한 채 거대한 하나의 통 테이블(Wide Table)로 설계하면, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 갱신 시 필연적으로 중복 수정 누락에 의한 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 파괴가 일어난다. 반대로, 아무 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이나 기준으로 잘게 찢어버리면 나중에 조인 시 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 결과에 수백만 건의 쓰레기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 뻥튀기되어 시스템이 다운될 수 있다.

- **📢 섹션 요약 비유**: 블록 장난감을 만들 때, 처음부터 거대한 한 덩어리로 본드칠을 해버리면(비정규화) 부서졌을 때 수리할 수 없다. 일단 작은 기본 블록(무손실 분해) 단위로 정확히 분해해 둔 뒤, 필요할 때만 단단하게 묶어서 쓰는 것이 안전한 설계다.

---

## Ⅴ. 기대효과 및 결론

무손실 분해 원칙을 준수하면, 시스템은 어떤 복잡한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 들어와도 '가짜 정보'를 응답하지 않는다는 강력한 수학적 신뢰성을 확보하게 된다. 이는 금융, 의료, 물류 등 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성이 생명인 도메인에서 절대 타협할 수 없는 기준이다.

결론적으로 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 단순히 테이블을 잘게 나누는 작업이 아니다. [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 쪼갰다가 다시 합치는 과정이 수학적으로 투명(Transparent)하게 이루어지도록, 정확한 공통 키를 설계하는 구조적 안정성 확보 과정으로 이해해야 한다.

- **📢 섹션 요약 비유**: 마술사가 미녀를 상자에 넣고 톱으로 반을 갈랐다가 다시 붙이는 마술에서, 이음새(공통 키) 장치를 완벽하게 만들어 두어야만 나중에 상자를 열었을 때 미녀가 온전하게 부활하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a> (<a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">Normalization</a>)</strong> | [이상 현상](/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)을 막기 위해 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 쪼개는 전체 과정 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/">기본 키</a> (Primary <a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a>)</strong> | 무손실 분해를 가능하게 하는 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 간의 연결 고리이자 [결정자](/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) |
| <strong><a href="/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/">이상 현상</a> (<a href="/studynote/05_database/04_transactions_concurrency/530_anomaly/">Anomaly</a>)</strong> | 삽입, 갱신, 삭제 시 발생하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치, 무손실 분해의 회피 대상 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/529_bcnf/">BCNF</a> (<a href="/studynote/05_database/02_modeling_normalization/106_bcnf_boyce_codd_normal_form/">Boyce-Codd Normal Form</a>)</strong> | 모든 [결정자](/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)인 정규형. [종속성 보존](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/)이 깨질 가능성이 있음 |

### 📈 관련 키워드 및 발전 흐름도

```text
이상 현상 (Anomaly) 인지
    |
    v
함수적 종속성 (Functional Dependency) 파악
    |
    v
정규화 및 무손실 분해 (Lossless-Join Decomposition) 적용
    |
    v
종속성 보존 (Dependency Preservation) 검증
    |
    v
물리적 반정규화 (De-normalization) - 성능 필요시 후행
```
이 흐름도는 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 설계 시 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 정합성을 확보한 후, 마지막에 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 타협하는 일련의 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 레고 로봇을 몸통과 다리로 분리해서 보관하려고 해요.
2. 아무 데나 부수면 나중에 다시 조립할 때 엉뚱한 다리가 붙어서 괴물이 될 수 있어요.
3. 하지만 딱 맞는 '특수 연결 블록([기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/))'을 남겨두고 분리하면, 나중에 설명서 없이도 원래 로봇으로 완벽하게 다시 합체할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 101 / 600

<- **이전**: [100. 정규화 (Normalization) - 이상 현상 방지를 위해 릴레이션을 분해(Decomposition)하는 과정](/studynote/05_database/02_modeling_normalization/100_normalization_decomposition/)
**다음**: [102. 종속성 보존 (Dependency Preservation) - 분해 후에도 FD가 유지됨](/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/) ->

---
