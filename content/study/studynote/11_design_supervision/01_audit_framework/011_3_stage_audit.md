---
title: 11. 3단계 감리 - 요구정의 단계 감리, 설계 단계 감리, 종료 단계 감리
date: '2024-05-20'
description: 정보시스템 구축 사업의 효과성, 효율성, 안전성을 검증하는 요구정의, 설계, 종료 단계의 3단계 감리 프레임워크 심층 분석
tags:
- design_supervision
---

# [[308_static_dynamic_nat_pat_port_address_translation|11]]. [[322_audit|3단계 감리]] (3-Stage [[363_audit|Audit]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[322_audit|3단계 감리]]는 정보시스템 구축의 Life Cycle(요구정의, 설계, 구현/테스트)에 맞추어 각 단계별 산출물과 공정의 품질을 제3자적 관점에서 [[395_verification_process_review|검증]]하는 핵심 통제 프레임워크이다.
> 2. **가치**: 프로젝트 [[459_quic_fec_forward_error_correction|초기]](요구정의)의 요구사항 누락 및 모호성을 사전 차단하여 후반부 재작업(Rework) 비용을 기하급수적으로 절감(최대 100배)하고, 시스템의 효과성과 안전성을 보장한다.
> 3. **융합**: 소프트웨어 공학의 폭포수(Waterfall) 및 테일러링 모델, 아키텍처 평가([[229_atam_architecture_trade_off_analysis_method|ATAM]]) 방법론과 강력하게 결합하여 품질 보증(QA)의 [[056_objective_evidence_collection|객관적 증거]]를 제공한다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[187_information_system_audit|정보시스템 감리]] ([[187_information_system_audit|Information System Audit]])는 발주자와 사업자 간의 정보 비대칭을 해소하고 사업의 품질을 보증하기 위해 도입된 제도이다. 과거 2단계(설계, 종료) 위주의 감리는 요구사항 확정 전 설계가 진행되면서 발생하는 요구사항 추적성의 단절과 빈번한 설계 변경이라는 치명적 한계를 안고 있었다. 이를 극복하기 위해 등장한 것이 **[[322_audit|3단계 감리]] (3-Stage [[363_audit|Audit]])** 이다. [[322_audit|3단계 감리]]는 요구정의(Requirements Definition), 설계(Design), 종료(Close/Implementation) 단계로 감리를 세분화하여, 사업 [[459_quic_fec_forward_error_correction|초기]]의 요구사항 모호성이라는 근본 원인을 선제적으로 타격한다. 이는 폭포수 모델에서 [[459_quic_fec_forward_error_correction|초기]] [[352_defect_definition|결함]]이 후기 단계로 갈수록 [[658_ir_recovery|복구]] 비용이 기하급수적으로 증가하는 '[[352_defect_definition|결함]] 증폭 현상'을 방지하는 가장 효과적인 방어선이다.

이 도식은 [[459_quic_fec_forward_error_correction|초기]] 요구사항의 불명확성이 프로젝트 후반부에 미치는 파괴적인 [[015_지연_데이터_관점|지연]] 효과와 병목을 보여준다.

```text
[요구사항 불명확] => [설계 왜곡] => [개발/테스트 지연 Queue >>>] => [오픈 실패 병목]
      ▲                 ▲                      ▲
  (요구정의 감리 부재) (설계 감리만으로 한계)   (종료 감리 시점엔 복구 불능)
```

이 흐름의 핵심은 [[395_verification_process_review|검증]] 단계가 선행되지 않은 실행(설계/개발)은 필연적으로 백엔드(테스트/오픈)에서 막대한 큐 적체(재작업)를 유발한다는 점이다. 따라서 요구사항 자체를 [[395_verification_process_review|검증]]하는 요구정의 단계 감리가 없다면, 시스템 전체의 성공률은 [[459_quic_fec_forward_error_correction|초기]] 요구사항의 운에 맡겨지게 된다. 실무에서는 이러한 [[459_quic_fec_forward_error_correction|초기]] [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 통제하기 위해 의무적으로 [[322_audit|3단계 감리]]를 적용하여 프로젝트의 불확실성을 통제한다.

📢 **섹션 요약 비유**: 마치 건축 공사에서 철근을 올리기 전 '지반 및 설계도 검사(요구정의)'를 추가하여, 건물이 다 올라간 뒤(종료) 무너지는 참사를 예방하는 다중 안전망과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[322_audit|3단계 감리]]는 각 단계마다 명확한 진입 조건(Entry Criteria)과 진출 조건(Exit Criteria)을 가지며, 상호 유기적으로 연결된 [[395_verification_process_review|검증]] 아키텍처를 구성한다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 점검 [[295_protocol_field_tcp_udp_icmp|프로토콜]] / 산출물 | 비유 |
|:---|:---|:---|:---|:---|
| **요구정의 감리** | 요구사항 명확성/완전성 [[395_verification_process_review|검증]] | 과업 대비표와 [[148_requirements_specification_formal_informal|요구사항 명세]]서의 1:1 양방향 추적성 [[395_verification_process_review|검증]], 모호성 제거 | [[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]]([[667_requirements_traceability_matrix|RTM]]), [[673_function_point_ilf_eif|기능점수]]([[293_fp_function_point|FP]]) | 건물의 용도/크기 확정 |
| **설계 감리** | 설계 산출물 아키텍처 타당성 [[395_verification_process_review|검증]] | 아키텍처 설계([[369_logic_bomb|논리]]/물리) 및 DB ERD [[093_normalization|정규화]], UI/UX 흐름 [[395_verification_process_review|검증]] | 아키텍처 정의서, DB 설계서, 화면 설계서 | 건물의 상세 청사진 검토 |
| **종료 감리** | 구현 완료 및 이관 품질 최종 [[395_verification_process_review|검증]] | 소스코드 [[190_secure_coding_guideline|시큐어 코딩]], [[445_performance_test_types|성능 테스트]], [[001_dikw_pyramid|데이터]] 이행, 사용자 [[406_acceptance_test_uat|인수 테스트]](UAT) [[395_verification_process_review|검증]] | 테스트 결과서, 이행 결과서, 보안 진단 | 준공 검사 및 입주 승인 |
| **추가 감리** | 지적 사항 최종 이행 여부 [[396_validation|확인]] | 종료 감리에서 지적된 필수 조치 사항의 코드/문서 반영 여부 대조 [[396_validation|확인]] | 시정조치 [[396_validation|확인]] 보고서 | 입주 전 하자 보수 [[396_validation|확인]] |
| **PM 영역 통제** | 전체 사업 관리 상태 [[395_verification_process_review|검증]] | 일정, 범위, 인력, 위험 관리 지표([[152_evm_earned_value_management|EVM]]) 모니터링 및 진척률 조작 [[395_verification_process_review|검증]] | 주간보고서, 위험관리대장 | 공사 감리 단장의 전체 진척 통제 |

이 구조도는 [[322_audit|3단계 감리]] 내에서 요구사항이 어떻게 각 단계를 거치며 구체화되고 [[395_verification_process_review|검증]]되는지를 보여주는 순차 및 계층 아키텍처이다.

```text
┌───────────────── Business Requirements ─────────────────┐
│ [과업지시서] / [제안서]                                │
└─────────────────────────┬─────────────────────────────┘
                          │ (추적성 Base)
┌─────────────────────────▼─────────────────────────────┐
│ 1단계: 요구정의 감리 (Requirements Definition Audit)   │
│ - 요구사항 명세서, RTM 검증 (완전성, 일관성)            │
└─────────────────────────┬─────────────────────────────┘
                          │ (RTM Baseline 확장)
┌─────────────────────────▼─────────────────────────────┐
│ 2단계: 설계 감리 (Design Audit)                        │
│ - 시스템 아키텍처, ERD, 인터페이스 설계 검증            │
└─────────────────────────┬─────────────────────────────┘
                          │ (Test Scenario 연계)
┌─────────────────────────▼─────────────────────────────┐
│ 3단계: 종료 감리 (Close/Implementation Audit)          │
│ - 통합/시스템 테스트, 마이그레이션, 성능/보안 검증        │
└───────────────────────────────────────────────────────┘
```

이 도식의 핵심은 모든 감리 단계가 이전 단계의 산출물([[159_baseline_requirements_configuration_management|베이스라인]])을 입력으로 받아 [[395_verification_process_review|검증]]의 깊이를 심화시킨다는 점이다. 즉, 요구정의 감리에서 [[667_requirements_traceability_matrix|RTM]]([[667_requirements_traceability_matrix|Requirements Traceability Matrix]])이 부실하면 설계 및 종료 감리에서의 추적성 [[395_verification_process_review|검증]]은 근본적으로 붕괴된다. 따라서 1단계 감리는 전체 감리 품질의 중추를 담당한다. 실무에서는 이 단계 간의 [[159_baseline_requirements_configuration_management|베이스라인]] 전이(Transition) 과정에서 무단 형상 변경이 발생하지 않는지 [[020_software_configuration_management|형상 관리]]([[089_configuration_management|Configuration Management]]) [[606_auditing_linux_auditd|감사]]를 병행해야 한다.

동작 원리를 상세히 살펴보면, ① 과업지시서의 모든 요건을 추출하여 요구사항 ID를 부여하고, ② 요구정의 감리에서 이 ID들이 명세서에 100% 매핑되었는지(완전성) [[396_validation|확인]]한다. ③ 설계 감리에서는 각 요구사항 ID가 클래스 설계나 DB 스키마로 정확히 전환되었는지 아키텍처의 적합성을 평가한다. ④ 종료 감리에서는 해당 요구사항 ID를 [[395_verification_process_review|검증]]할 수 있는 단위/[[400_integration_testing|통합 테스트]] 시나리오가 실행되었고 [[352_defect_definition|결함]]이 조치되었는지를 추적한다. ⑤ 최종적으로는 이 모든 과정이 [[056_objective_evidence_collection|객관적 증거]]([[056_objective_evidence_collection|Objective Evidence]])로 감리 보고서에 기록된다.

📢 **섹션 요약 비유**: 이는 재판에서 기소(요구정의) → 증거 수집 및 심리(설계) → 최종 선고(종료)로 이어지는 절차처럼, 이전 단계의 무결성이 다음 단계의 정당성을 보장하는 사슬 구조와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[187_information_system_audit|정보시스템 감리]]는 사업 규모와 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]에 따라 2단계 감리와 [[322_audit|3단계 감리]]로 나뉜다. 이 둘의 구조적 차이와 선택 기준을 명확히 이해하는 것이 핵심이다.

| 항목 | [[322_audit|3단계 감리]] (3-Stage [[363_audit|Audit]]) | 2단계 감리 (2-Stage [[363_audit|Audit]]) | 판단 포인트 (실무 기준) |
|:---|:---|:---|:---|
| **적용 대상** | 20억 이상 대형 개발 사업, [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 높은 신규 구축 | 상용 SW 단순 도입, 20억 미만 소규모 사업 | 시스템 복잡도 및 개발 비중 |
| **요구정의 [[395_verification_process_review|검증]]** | 독립적인 감리 단계로 심층 [[395_verification_process_review|검증]] ([[459_quic_fec_forward_error_correction|초기]] [[159_baseline_requirements_configuration_management|베이스라인]] 확정) | 설계 감리에 통합하여 병행 수행 (시간 촉박) | 요구사항 변경 빈도와 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] |
| **오류 수정 비용** | [[459_quic_fec_forward_error_correction|초기]] 식별로 수정 비용 최소화 (비용 곡선 완만) | 설계 이후 발견되어 재설계 오버헤드 급증 | 프로젝트 [[015_지연_데이터_관점|지연]] 방어선 위치 |
| **산출물 추적성** | 제안서 → [[148_requirements_specification_formal_informal|요구사항 명세]] → 아키텍처 설계의 완벽한 맵핑 | 제안서 → 설계 산출물로 압축되어 추적 단절 우려 | 품질 보증(QA)의 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 요구 수준 |

이 비교 매트릭스는 프로젝트 위험도에 따른 감리 모드(3단계 vs 2단계)의 아키텍처 트레이드오프를 보여준다.

```text
┌──────────┬───────────────────────┬───────────────────────┬──────────────────────┐
│ 관점     │ 3단계 감리 (3-Stage)  │ 2단계 감리 (2-Stage)  │ 품질/비용 트레이드오프│
├──────────┼───────────────────────┼───────────────────────┼──────────────────────┤
│ 시간/비용│ 감리 비용 및 기간 증가 │ 비용 절감, 기간 단축  │ 예산 제약 vs 품질 보증│
│ 리스크   │ 초기 리스크 강력 통제 │ 잠복 리스크 후기 폭발 │ 장애 격리(Isolation)  │
│ 일관성   │ RTM 기반 강한 일관성  │ 느슨한 일관성(추적 약화)│ 운영 복잡도 통제력    │
└──────────┴───────────────────────┴───────────────────────┴──────────────────────┘
```

A 방식([[322_audit|3단계 감리]])은 단일 감리 일정(레이턴시)은 길어지지만, 요구사항의 상태 공유 오류를 [[459_quic_fec_forward_error_correction|초기]]에 잡아내어 후속 공정의 [[275_lock_contention_monitoring|락 경합]](병목)을 방지한다. 반면 B 방식(2단계 감리)은 [[017_audit_execution|감리 수행]] 기간은 짧지만, 요구사항 [[395_verification_process_review|검증]]이 설계 감리에 묻히기 때문에 요구사항 변경이 빈번한 환경에서는 오히려 전체 [[139_throughput|처리량]](성공적인 개발 완료율)을 심각하게 떨어뜨린다.

**융합 관점 분석**:
- **SW 공학 ([[131_requirements_engineering|Requirements Engineering]]) 연계**: [[322_audit|3단계 감리]]의 요구정의 단계는 SW 공학의 요구사항 추출, 분석, 명세, [[395_verification_process_review|검증]]([[396_validation|Validation]]) 단계를 완벽히 투영한다. IEEE 830 명세 표준 준수 여부가 핵심 감리 지표가 된다.
- **아키텍처 ([[201_software_architecture_definition|Software Architecture]]) 연계**: 설계 감리 단계는 [[229_atam_architecture_trade_off_analysis_method|ATAM]]([[319_architecture|Architecture]] Trade-off Analysis Method)의 민감도 점과 상충 점을 평가하는 과정과 유사하다. 시스템이 요구하는 [[452_availability|가용성]], [[282_performance_tactics|성능]] 등의 품질 [[082_attribute_types_er_model|속성]]을 설계 산출물이 만족하는지 정량적으로 [[395_verification_process_review|검증]]한다.

📢 **섹션 요약 비유**: 고속도로를 달릴 때 톨게이트를 3번 거치며(3단계) 차량을 꼼꼼히 점검하면 시간은 걸려도 사고율이 0%에 수렴하지만, 톨게이트를 2번만 거치면(2단계) 정체는 줄어도 후반부 대형 추돌 사고(프로젝트 실패) 위험을 안고 달리는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무 프로젝트에서 [[322_audit|3단계 감리]]를 성공적으로 수행하기 위해서는 감리인과 피감리인(사업자) 간의 첨예한 대립을 중재하고, 객관적인 증거 기반의 판정을 내려야 한다.

1. **시나리오 1: 요구사항 폭증과 과업 범위 분쟁**
   - **상황**: 발주처가 제안서에 없는 신규 요건을 요구정의 단계에서 대거 추가하려 하고 사업자는 반발한다.
   - **판단**: 감리인은 '과업 대비표'를 [[159_baseline_requirements_configuration_management|베이스라인]]으로 삼아 범위를 벗어난 요구사항은 '과업 외 사항'으로 명확히 분리([[195_isolation_concurrency_control|Isolation]])해야 한다. [[080_cab|변경 통제 위원회]]([[160_change_control_board_ccb_requirements_review|CCB]])를 통한 공식 승인 절차가 없는 무분별한 수용은 추후 일정 [[015_지연_데이터_관점|지연]]과 품질 저하([[128_water_scrum_fall_anti_pattern|안티패턴]]: [[161_scope_creep_requirements_inflation_prevention|Scope Creep]])를 유발하므로 [[352_defect_definition|결함]]으로 지적해야 한다.

2. **시나리오 2: 설계 감리 시 아키텍처 상세화 부족**
   - **상황**: 사업자가 설계 산출물로 껍데기뿐인 클래스 다이어그램과 물리 테이블 구조만 제출했다.
   - **판단**: [[369_logic_bomb|논리]] 아키텍처와 프로세스 흐름([[235_sequence_diagram_dynamic_interaction_uml|시퀀스 다이어그램]])이 생략된 설계는 개발자 간의 해석 오류를 낳는다. 특히 [[136_variance|분산]] 환경([[619_msa_traffic_hardware|MSA]])에서 [[191_transaction_concept_states|트랜잭션]] 보상([[305_saga|Saga]]) 설계가 누락된 경우 치명적 [[352_defect_definition|결함]]으로 판단하여, 설계도 보완 전에는 개발 단계 진입을 차단해야 한다.

3. **시나리오 3: 종료 감리 시 [[446_load_test|부하 테스트]]([[282_performance_tactics|성능]]) 미흡**
   - **상황**: UAT는 통과했으나, 동시 접속자 [[139_throughput|처리량]](TPS) 테스트가 생략되었다.
   - **판단**: 리틀의 법칙(Little's Law)에 기반한 적정 [[103_thread_pool|스레드 풀]] 및 커넥션 풀 튜닝 [[395_verification_process_review|검증]]이 누락된 상태다. 오픈 후 즉각적인 장애(병목)가 예상되므로, [[162_apm_application_performance_management|APM]] 툴을 활용한 [[446_load_test|부하 테스트]]([[447_stress_test|Stress Test]])를 필수 시정 조치(Major)로 권고하고 오픈 일정을 통제해야 한다.

이 의사결정 트리는 실무에서 감리인이 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 판별하고 조치 강도를 결정하는 [[369_logic_bomb|논리]] 흐름을 보여준다.

```text
[산출물 검토] ──(기준 미달)──> [결함의 성격 분류]
                                  ├─> (기능 누락/보안 취약) => 필수 시정조치 (Major) 
                                  │                             ↓ (오픈 불가)
                                  └─> (문서 오타/단순 사용성) => 권고 사항 (Minor)
                                                                ↓ (운영 중 개선)
```

이 결정 흐름의 핵심은 '[[352_defect_definition|결함]]의 성격'에 따라 조치 강도(Major vs Minor)를 엄격히 분리하는 것이다. 모든 지적 사항을 Major로 잡으면 프로젝트가 [[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]])에 빠지고, 반대로 치명적 보안 취약점(예: [[604_sql_injection|SQL Injection]])을 Minor로 타협하면 시스템 보안이 붕괴된다. 실무에서는 이 트레이드오프를 조율하는 감리 총괄(총괄 감리원)의 기술적 권위와 중재력이 감리의 성패를 결정한다.

📢 **섹션 요약 비유**: 의사가 환자를 진단할 때, 암세포(기능/보안 [[352_defect_definition|결함]])는 즉각적인 수술(필수 조치)을 지시하고, 단순 감기(문서 오타)는 휴식(권고 사항)을 처방하여 환자(프로젝트)가 생존할 수 있는 최적의 치료 경로를 설계하는 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[322_audit|3단계 감리]] 체계는 단순한 규제([[058_it_compliance_sox_basel_gdpr_isms|Compliance]])를 넘어, 공공 및 대형 민간 IT 프로젝트의 생존을 담보하는 필수 품질 보증 아키텍처로 자리매김했다.

| 구분 | 도입 전 (감리 부재 / 2단계) | 도입 후 ([[322_audit|3단계 감리]] 정착) | [[012_roi_return_on_investment|ROI]] 및 정량적 효과 |
|:---|:---|:---|:---|
| **프로젝트 [[015_지연_데이터_관점|지연]]** | 빈번한 재설계로 30% 이상 [[015_지연_데이터_관점|지연]] | 요구사항 조기 확정으로 [[015_지연_데이터_관점|지연]]율 5% 미만 | 예산 초과(Overrun) 90% 이상 차단 |
| **시스템 보안/안전성** | 오픈 후 치명적 해킹 사고 발생 | [[190_secure_coding_guideline|시큐어 코딩]] 및 취약점 100% 사전 조치 | 침해 사고 [[658_ir_recovery|복구]] 비용 수십억 원 절감 |
| **법적 분쟁** | 발주자-사업자 간 지체상금 소송 빈발 | 과업대비표 기반 객관적 완료 승인 | 분쟁 조정 및 소송 비용 [[784_zeroization_circuit|제로화]] |

**미래 전망 (Future Standard)**: 
전통적인 폭포수 방식에 최적화된 [[322_audit|3단계 감리]]는 현재 [[004_agile_relation|애자일]]([[004_agile_relation|Agile]]) 및 클라우드(Cloud), [[619_msa_traffic_hardware|MSA]] 환경으로의 패러다임 전환을 맞이하고 있다. 향후 [[006_audit_framework_3dimensional|감리 프레임워크]]는 3단계의 정적 분할을 넘어, [[090_configuration_item|CI]]/CD 파이프라인 내에 자동화 진단 도구를 임베딩하여 매 [[067_sprint_timebox|스프린트]]([[067_sprint_timebox|Sprint]]) 단위로 코드를 [[395_verification_process_review|검증]]하는 **연속적 통제 (Continuous [[606_auditing_linux_auditd|Auditing]])** 기반의 '상시/자동화 [[006_audit_framework_3dimensional|감리 프레임워크]] ([[363_audit|Audit]] 3.0)'로 진화할 것이다. 이는 행정안전부 [[005_audit_standards|정보시스템 감리기준]] 및 ISACA의 [[022_cisa_certification_audit|CISA]] 최신 통제 지침과 맥을 같이 한다.

📢 **섹션 요약 비유**: 수동으로 도장을 찍어주던 구형 품질 검사소(전통 감리)가, 이제는 공장 컨베이어 벨트 위에서 [[190_ai_llm_requirements_specification|AI]] 카메라가 24시간 불량품을 실시간으로 솎아내는 스마트 품질 관제소(연속적/자동화 감리)로 진화하는 것과 같습니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[005_audit_standards|정보시스템 감리기준]] ([[005_audit_standards|행정안전부 고시]])** : [[322_audit|3단계 감리]]를 비롯한 [[017_audit_execution|감리 수행]]의 법적/제도적 근거를 제공하는 최상위 규정.
- **[[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]] ([[667_requirements_traceability_matrix|RTM]])** : 1단계부터 3단계까지 요구사항의 구현 여부를 양방향으로 증명하는 품질 추적의 백본(Backbone).
- **소프트웨어 개발보안 ([[190_secure_coding_guideline|시큐어 코딩]])** : 종료 감리에서 소스코드의 47개 보안 약점을 [[331_static_analysis|정적 분석]]([[491_sast_static_analysis|SAST]])으로 차단하는 핵심 보안 통제 수단.
- **[[022_cisa_certification_audit|CISA]] (공인 정보시스템 [[606_auditing_linux_auditd|감사]]사)** : ISACA에서 주관하며, 제3자적 관점의 IT [[606_auditing_linux_auditd|감사]] 프로세스와 거버넌스를 설계하는 감리인의 국제 표준 자격.
- **[[229_atam_architecture_trade_off_analysis_method|ATAM]] ([[319_architecture|Architecture]] Trade-off Analysis Method)** : 설계 감리 시 아키텍처의 품질 [[082_attribute_types_er_model|속성]]([[282_performance_tactics|성능]], 보안, [[452_availability|가용성]] 등)이 상충점을 극복했는지 평가하는 과학적 잣대.

### 📈 관련 키워드 및 발전 흐름도

```text
[감리 계획 (Audit Planning) — 범위·일정·기준·체크리스트 확정]
    │
    ▼
[현장 감리 (On-site Audit) — 산출물 검토·인터뷰·시연 수행]
    │
    ▼
[감리 결과 보고 (Audit Report) — 문제점·시정 권고사항 제출]
    │
    ▼
[시정 조치 확인 (Follow-up) — 권고사항 이행 여부 재점검]
    │
    ▼
[품질 보증 체계 (QA Framework) — 지속적 감리 활동으로 프로젝트 리스크 관리]
```

이 흐름은 감리 계획 수립부터 시정 [[396_validation|확인]]까지 [[322_audit|3단계 감리]] 사이클이 품질 보증 체계로 이어지는 과정을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: [[322_audit|3단계 감리]]는 레고 성을 만들 때, 설명서를 잘 읽었는지(1단계), 기초 공사가 튼튼한지(2단계), 완성품이 튼튼한지(3단계)를 똑똑한 선생님이 세 번 검사해주는 거예요.
2. **원리**: 처음에 잘못 조립하면 나중에 다 부수고 다시 만들어야 하니까, 중간중간 멈춰서 제대로 만들고 있는지 꼼꼼하게 사진을 찍고 [[396_validation|확인]]하는 방식이랍니다.
3. **효과**: 이렇게 깐깐하게 3번이나 검사를 받으면 절대 부서지지 않고 아주 튼튼하고 멋진 레고 성을 안전하게 완성할 수 있어요!
