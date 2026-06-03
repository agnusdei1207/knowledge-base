+++
title = "65. Shuffle 최적화 — spark.sql.shuffle.partitions, AQE 코어리스"
date = 2026-04-05

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Spark Shuffle은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재분배로, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용의 큰 비중을 차지하는 핵심 병목이다.
> 2. **가치**: spark.sql.shuffle.partitions, AQE(Adaptive Query Execution), 브로드캐스트 조인, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐 대응을 통해 셔플 비용을 줄일 수 있다.
> 3. **판단**: 셔플 최적화는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수를 무작정 늘리거나 줄이는 문제가 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포와 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴에 맞추는 문제다.

---

## Ⅰ. 개요 및 필요성

Spark는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다시 나눠야 하는 순간 셔플을 수행한다. 이때 네트워크, 디스크, 정렬 비용이 크게 발생한다.

따라서 셔플을 이해하지 못하면 Spark 튜닝은 절반만 이해한 셈이다.

- **📢 섹션 요약 비유**: 물건을 방마다 다시 옮기는 이사가 가장 힘든 이유와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Partition A / B / C</div>
<div class="kb-diagram-note">↓ shuffle ↓</div>
<div class="kb-diagram-note">New Partitions</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Execution</div>
</div>
</div>



| 항목 | 역할 |
| :-- | :-- |
| [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 작업 분할 단위 |
| Shuffle | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재배치 |
| AQE | 실행 중 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)/조인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 조정 |
| Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 작은 테이블을 복제해 셔플 줄임 |

셔플은 Stage 경계를 만들고, 각 Stage는 독립적으로 실행된다. 그래서 셔플 양을 줄이면 전체 실행 시간과 메모리 사용량이 크게 줄어든다.

- **📢 섹션 요약 비유**: 짐을 여러 방으로 나누되, 다시 모으는 횟수를 줄여야 이사가 빨라진다.

---

## Ⅲ. 비교 및 연결

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 장점 | 주의점 |
| :-- | :-- | :-- |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 조정 | 병렬성 개선 | 너무 많거나 적으면 비효율 |
| AQE | 실행 중 최적화 | Spark [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)/[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 |
| Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 작은 테이블 셔플 제거 | 메모리 한계 고려 |

| 문제 | 대응 |
| :-- | :-- |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Skew | [skew join](/knowledge-base/studynote/16_bigdata/03_spark/069_skew_join/) / [salting](/knowledge-base/studynote/02_operating_system/10_security/605_password_salting_hash/) |
| 작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 많음 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 병합 및 [파티션 최적화](/knowledge-base/studynote/16_bigdata/03_spark/070_partition_optimization/) |
| 과도한 셔플 | 조인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 변경 |

셔플 최적화는 단일 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값으로 끝나지 않는다. [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기, 분포, 클러스터 자원을 함께 봐야 한다.

- **📢 섹션 요약 비유**: 방 크기와 물건 크기를 함께 봐야 가구 배치가 쉬운 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 셔플이 어디서 발생하는지 확인했는가?
2. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기에 맞는가?
3. AQE가 활성화되어 있는가?
4. 브로드캐스트 조인을 적용할 수 있는가?
5. 스큐 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 별도로 다뤘는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- `spark.sql.shuffle.partitions`만 무작정 조정하는 설계
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포를 보지 않고 조인하는 설계
- 셔플 비용을 무시한 상태에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 찾는 설계
- AQE를 켰다고 모든 문제가 해결된다고 믿는 설계

기술사 관점에서는 셔플을 "피해야 하는 비용"으로 보고, 어디서 왜 발생하는지 설명할 수 있어야 한다.

- **📢 섹션 요약 비유**: 이사할 때 박스 수를 잘 나누고, 한 번에 옮길 양을 줄이는 것이 핵심이다.

---

## Ⅴ. 기대효과 및 결론

셔플을 줄이면 Spark [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 크게 좋아진다. 그래서 튜닝의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재배치 비용을 읽는 것이다.

결론적으로 Shuffle 최적화는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비용을 줄이는 대표 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

- **📢 섹션 요약 비유**: 짐을 덜 옮길수록 이사가 빨라진다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Partition</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Shuffle</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AQE</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Spark Performance</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">spark.sql.shuffle.partitions</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AQE</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Broadcast Join</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Skew Optimization</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

장난감을 방마다 다시 옮기면 시간이 오래 걸려요.  
Spark의 셔플도 그런 옮기기예요.  
그래서 옮기는 양을 줄이는 것이 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 113 / 587

← **이전**: [64. 서비스 전략 (Service Strategy)](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_service_strategy/)
**다음**: [65. 서비스 설계 (Service Design)](/knowledge-base/studynote/12_it_management/02_itsm_itil/065_service_design/) →

---
