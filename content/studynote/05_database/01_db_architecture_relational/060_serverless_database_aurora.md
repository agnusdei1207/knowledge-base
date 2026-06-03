+++
title = "60. 서버리스 데이터베이스 (Serverless DB) - Amazon Aurora Serverless 등 자동 확장 아키텍처"
date = 2026-04-10

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 컴퓨팅 자원을 미리 고정하지 않고 필요할 때만 늘리고 줄이는 자동 확장형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)다.
> 2. **가치**: 수요가 들쑥날쑥한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 비용을 줄이고, [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 부담을 크게 낮춘다.
> 3. **판단 포인트**: 스토리지와 컴퓨팅 분리, [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층, [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)와 지속 트래픽 적합성을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 클라우드 DB는 CPU와 메모리 크기를 먼저 정해야 했다. 트래픽이 없을 때는 낭비가 크고, 갑자기 늘면 즉시 대응이 어렵다.

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 이런 문제를 풀기 위해 컴퓨팅을 탄력적으로 붙였다 떼고, 스토리지는 별도로 유지한다. [Aurora](/knowledge-base/studynote/05_database/06_dw_olap_trends/390_aurora_serverless_quorum_write/) Serverless가 대표적이다.

- **📢 섹션 요약 비유**: 자동차를 사는 대신 필요한 시간에만 기사와 차를 부르는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 [스토리지와 컴퓨팅의 분리](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/293_storage_compute_separation/)다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 안정적으로 저장하고, 실행 노드는 부하에 맞춰 자동 조절한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">App</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Proxy / Router</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Compute Node (scale up/down)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Shared Storage</div>
</div>
</div>



| 계층 | 역할 |
| :-- | :-- |
| [Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)/Router | 연결 유지와 요청 분배 |
| Compute Node | SQL 실행과 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 |
| Shared Storage | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영구 저장 |

접속이 줄면 컴퓨팅은 0에 가깝게 내려가고, 트래픽이 몰리면 빠르게 노드를 늘린다. 그래서 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 불규칙한 워크로드에 적합하다.

- **📢 섹션 요약 비유**: 창고는 그대로 두고, 계산대 인원만 손님 수에 따라 늘리는 가게다.

---

## Ⅲ. 비교 및 연결

| 방식 | 장점 | 한계 |
| :-- | :-- | :-- |
| Provisioned DB | 예측 가능, 꾸준한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 과다 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 낭비 |
| [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB | 자동 확장, 비용 최적화 | [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/), 변동성 |
| Self-managed DB | 세밀한 통제 | 운영 부담 큼 |

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 [스파이크](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/)가 큰 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 테스트/개발, 비정기 업무에 강하다. 반대로 24시간 고부하가 계속되는 시스템은 기존 Provisioned DB가 더 나을 수 있다.

- **📢 섹션 요약 비유**: 항상 손님이 많은 식당에는 정규 직원이 낫고, 들쑥날쑥한 식당에는 파트타임이 낫다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB를 고를 때는 "얼마나 자주, 얼마나 급하게 트래픽이 변하나"를 먼저 본다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 트래픽 패턴이 예측 불가능한가?
2. 0에 가까운 유휴 비용이 중요한가?
3. [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 치명적이지 않은가?
4. 커넥션 풀과 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 준비됐는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 꾸준한 초고부하 시스템에 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)를 적용하는 설계
- [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)은 자동인데 커넥션 관리는 수동인 설계
- 저장 비용보다 실행 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 더 크게 보는 설계

- **📢 섹션 요약 비유**: 문을 열고 닫는 사람이 자동이어도, 손님이 계속 꽉 차 있으면 결국 작은 가게는 버티기 어렵다.

---

## Ⅴ. 기대효과 및 결론

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 비용과 확장성 문제를 동시에 줄인다. 특히 짧게 몰리는 트래픽에는 매우 유리하다.

하지만 모든 DB 문제를 해결하지는 않는다. 결국 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 패턴을 보고 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)가 맞는지 선택해야 한다.

- **📢 섹션 요약 비유**: 풍선처럼 필요할 때만 커지는 창고지만, 항상 큰 창고가 필요한 곳도 있다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">트래픽 변동</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Serverless DB</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Compute / Storage 분리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">자동 확장 / 비용 최적화</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Provisioned DB</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Auto Scaling DB</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Serverless DB</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Aurora Serverless</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB는 손님이 올 때만 계산대를 늘리는 가게예요.  
손님이 없으면 계산대를 줄여서 돈을 아껴요.  
그래서 왔다 갔다 하는 손님이 많은 곳에 잘 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 60 / 600

← **이전**: [59. 영구 저장소 (Persistent Storage) - 데이터 파일, 로그 파일, 제어 파일](/knowledge-base/studynote/05_database/01_db_architecture_relational/059_persistent_storage_data_log_control_file/)
**다음**: [61. 릴레이션 (Relation) - 데이터를 2차원 표로 표현한 구조](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) →

---
