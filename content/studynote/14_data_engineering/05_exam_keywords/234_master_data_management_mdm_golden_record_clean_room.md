---
title: 234. 마스터 데이터 관리 (MDM, Master Data Management) 골든 레코드 클린 룸
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[539_mdm_master_data_management|MDM]](Master [[001_dikw_pyramid|Data]] [[372_management|Management]])은 조직 전체에서 공유되는 핵심 [[001_dikw_pyramid|데이터]](고객·제품·공급자)의 단일 권위 있는 [[288_version_ihl_tos_total_length|버전]]을 관리하여 [[001_dikw_pyramid|데이터]] 불일치와 [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]])를 제거한다.
> 2. **가치**: 골든 레코드(Golden Record)는 중복 제거·병합·스코어링을 거쳐 [[087_process_state_transition|생성]]되는 "유일한 진실의 출처(Single Source of Truth)"로, 기업 의사결정의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 보장한다.
> 3. **판단 포인트**: 아키텍처 유형([[152_hub_dummy_switching_intelligent|허브]]형·가상형·레지스트리형)은 [[001_dikw_pyramid|데이터]] 통제 강도, 시스템 연계 복잡도, 실시간 요건에 따라 선택하며, 프라이버시 이슈는 [[001_dikw_pyramid|데이터]] 클린 룸([[305_data_clean_room|Data Clean Room]])으로 해결한다.

## Ⅰ. 개요 및 필요성

### MDM이 없을 때의 문제

대기업에는 수십 개의 시스템([[107_crm_customer_relationship_management|CRM]]·[[081_erp_enterprise_resource_planning|ERP]]·[[167_scm_software_configuration_management|SCM]]·e-커머스)이 존재하고, 같은 고객이 각 시스템에 다르게 등록되어 있다.

```
CRM 시스템:   홍길동 / 서울시 강남구 / 010-1234-5678
ERP 시스템:   Hong Gil-dong / Seoul Gangnam / 01012345678
e-커머스:     홍 길동 / 강남구 서울 / 010.1234.5678
```

이로 인해 발생하는 문제들:
- **중복 마케팅**: 같은 고객에게 3개의 DM 발송
- **분석 부정확**: 고객 수 집계 시 1명이 3명으로 계산
- **규정 위반**: [[791_gdpr_eu|GDPR]](General [[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]] Regulation) [[781_personal_information|개인정보]] 삭제 요청 시 모든 시스템에서 삭제 불가

### MDM의 정의와 범위

[[539_mdm_master_data_management|MDM]](Master [[001_dikw_pyramid|Data]] [[372_management|Management]])은 기업의 핵심(Master) [[001_dikw_pyramid|데이터]] 엔터티를 [[655_ir_detection_analysis|식별]]하고, 정제하며, 단일 권위 [[288_version_ihl_tos_total_length|버전]]을 유지·관리하는 체계이다.

| [[539_mdm_master_data_management|MDM]] 대상 [[064_relation_domain|도메인]] | 주요 엔터티 | 핵심 [[082_attribute_types_er_model|속성]] |
|:---|:---|:---|
| 고객 마스터 ([[026_three_c_analysis|Customer]] [[539_mdm_master_data_management|MDM]]) | 개인·법인 고객 | [[289_identification_flags_fragmentation_offset|식별자]], 연락처, 거래 이력 |
| 제품 마스터 (Product [[539_mdm_master_data_management|MDM]]) | 제품·SKU·[[394_catalog_metadata|카탈로그]] | 제품명, 사양, 가격, [[104_classification_analysis|분류]] |
| 공급자 마스터 (Supplier [[539_mdm_master_data_management|MDM]]) | 협력사·[[520_supply_chain_attack_and_ci_cd_security|공급망]] | 사업자번호, 계좌, 계약 조건 |
| 위치 마스터 (Location [[539_mdm_master_data_management|MDM]]) | 지점·창고·주소 | 좌표, 행정구역, 운영 시간 |
| 직원 마스터 (Employee [[539_mdm_master_data_management|MDM]]) | HR 인력 | 사번, 부서, 직책, 자격증 |

📢 **섹션 요약 비유**: MDM이 없는 기업은 같은 사람을 다른 이름으로 여러 주소록에 등록한 것과 같다. 전화하려면 어느 주소록이 맞는지 매번 확인해야 하는 혼란이 생긴다.

## Ⅱ. 아키텍처 및 핵심 원리

### 골든 레코드 (Golden Record) [[087_process_state_transition|생성]] 과정

```
┌─────────────────────────────────────────────────────────────────┐
│                  골든 레코드 생성 파이프라인                         │
│                                                                 │
│  소스 시스템      수집         정제          매칭         병합       │
│                                                                 │
│  CRM ──────┐                                                    │
│  ERP ──────┼──→ [프로파일링] → [표준화]  → [중복    → [골든     │
│  ECM ──────┘    데이터 품질    주소·이름    탐지·     레코드]     │
│                 분석          정규화]      링킹]                  │
│                                                                 │
│         1단계        2단계       3단계       4단계     5단계      │
│        수집·통합    데이터 정제  표준화    매칭·링킹   병합·게시    │
└─────────────────────────────────────────────────────────────────┘
```

#### 각 단계 상세

| 단계 | 활동 | 기술/방법 |
|:---|:---|:---|
| **1. 수집** | 다중 소스에서 레코드 수집 | [[215_etl_vs_elt_pipeline|ETL]]([[033_etl|Extract Transform Load]]), [[217_cdc_binlog_change_capture_debezium|CDC]] |
| **2. [[613_profiling_gprof|프로파일링]]** | [[001_dikw_pyramid|데이터]] 품질·완전성 분석 | 통계 분석, 이상값 탐지 |
| **3. 정제** | 결측·오류·불일치 수정 | 규칙 기반 보정, ML 보완 |
| **4. 표준화** | 주소·이름·전화번호 형식 통일 | 표준 주소 [[014_api_posix|API]], 정규식 |
| **5. 매칭·링킹** | 동일 엔터티 [[655_ir_detection_analysis|식별]]·연결 | 확률적 매칭(Probabilistic Matching), [[070_graph_datastructure|그래프]] |
| **6. 병합·스코어링** | 최신·[[085_confidence_association_rule_conditional_probability|신뢰도]] 높은 [[082_attribute_types_er_model|속성]] 선택 | [[085_confidence_association_rule_conditional_probability|신뢰도]] 점수([[085_confidence_association_rule_conditional_probability|Confidence]] Score) |
| **7. 골든 레코드 게시** | 단일 권위 레코드 배포 | [[014_api_posix|API]], 이벤트 스트림 |

### [[539_mdm_master_data_management|MDM]] 아키텍처 유형

```
┌─────────────────────────────────────────────────────────────────┐
│                 MDM 아키텍처 유형 비교                             │
├──────────────────┬────────────────────────────────────────────┤
│  허브형          │          가상형                              │
│  (Hub Style)     │         (Virtual/Federation Style)          │
│                  │                                            │
│  MDM Hub         │  소스시스템1 ──┐                            │
│  ┌─────────┐     │  소스시스템2 ──┼──→ [가상 레이어]            │
│  │골든레코드│     │  소스시스템3 ──┘   (실시간 연합)             │
│  └──┬──┬───┘     │                                            │
│     │  │         │  원본 유지, 물리적 복사 없음                  │
│  CRM ERP SCM     │                                            │
└──────────────────┴────────────────────────────────────────────┘

레지스트리형 (Registry Style):
  소스시스템 → 각자 원본 유지
  MDM       → 식별자·링크만 관리 (실제 데이터 미보유)
  특징: 가볍고 빠르나 통제력 낮음
```

### 아키텍처 유형 비교

| 유형 | [[001_dikw_pyramid|데이터]] 위치 | 통제 강도 | 구현 복잡도 | 적합 상황 |
|:---|:---|:---:|:---:|:---|
| [[152_hub_dummy_switching_intelligent|허브]]형 ([[152_hub_dummy_switching_intelligent|Hub]]) | [[539_mdm_master_data_management|MDM]] [[152_hub_dummy_switching_intelligent|Hub]] 중앙 저장 | ⭐⭐⭐ | 높음 | 강한 거버넌스 필요 |
| 가상형 (Virtual) | 소스 시스템 원본 | ⭐⭐ | 중간 | 실시간 연동 중요 |
| 레지스트리형 ([[235_registry_immutable_tag|Registry]]) | 소스 시스템 원본 | ⭐ | 낮음 | 간단한 [[289_identification_flags_fragmentation_offset|식별자]] 연계 |
| 하이브리드 (Hybrid) | 혼합 | ⭐⭐⭐ | 매우 높음 | 대기업 복합 요건 |

📢 **섹션 요약 비유**: [[152_hub_dummy_switching_intelligent|허브]]형은 모든 주소록을 하나의 마스터 노트에 통합하는 것, 레지스트리형은 "각 주소록 몇 번째 줄에 있는 사람이 동일인"이라는 색인만 만드는 것이다.

## Ⅲ. 비교 및 연결

### [[001_dikw_pyramid|데이터]] 클린 룸 ([[305_data_clean_room|Data Clean Room]])

[[001_dikw_pyramid|데이터]] 클린 룸은 **두 조직이 원시 [[781_personal_information|개인정보]]를 공유하지 않고** 공통 고객 분석을 수행할 수 있는 프라이버시 [[571_protection_vs_security|보호]] 환경이다.

```
        광고주 A                   플랫폼 B
    (구매 이력 보유)            (광고 노출 데이터 보유)
           │                          │
           ▼                          ▼
     ┌─────────────────────────────────┐
     │         데이터 클린 룸           │
     │  (Data Clean Room)              │
     │                                │
     │  원시 데이터 직접 공유 금지      │
     │  집계 결과·통계만 반출 허용      │
     │  개인 식별 불가 보장             │
     │                                │
     │  분석: 광고 도달 고객의 구매 전환율│
     └─────────────────────────────────┘
           결과: "캠페인 전환율 3.2%"만 공유
```

### 클린 룸 구현 기술

| 기술 | 설명 | 제공 업체 |
|:---|:---|:---|
| 안전한 다자 계산 (MPC, Multi-Party Computation) | 원시 [[001_dikw_pyramid|데이터]] 없이 공동 계산 | 학술/스타트업 |
| [[256_federated_learning_privacy_model_security|연합 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]]) | 모델만 이동, [[001_dikw_pyramid|데이터]] 불동 | Google, Apple |
| [[396_differential_privacy|차분 프라이버시]] (DP, [[817_differential_privacy|Differential Privacy]]) | 노이즈 추가로 개인 [[571_protection_vs_security|보호]] | Apple, US Census |
| [[478_tee|신뢰 실행 환경]] ([[478_tee|TEE]], [[972_tee_based_ml|Trusted Execution Environment]]) | 하드웨어 격리 분석 | [[480_intel_sgx|Intel SGX]] |
| Google ADH | Google Ads [[001_dikw_pyramid|데이터]] 클린 룸 | Google |
| AWS Clean Rooms | AWS 기반 클린 룸 [[090_service_kubernetes_network_load_balancing|서비스]] | AWS |

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 클린 룸은 두 회사가 각자 레시피 비밀을 지키면서도 같이 요리한 결과물(분석 결과)만 보는 공유 주방이다.

## Ⅳ. 실무 적용 및 기술사 판단

### [[539_mdm_master_data_management|MDM]] 구축 단계별 [[435_checklist_based_testing|체크리스트]]

```
Phase 1: 준비 (0~3개월)
  ☐ 마스터 데이터 도메인 식별
  ☐ 데이터 오너십·거버넌스 체계 수립
  ☐ 데이터 품질 현황 진단 (프로파일링)

Phase 2: 설계 (3~6개월)
  ☐ MDM 아키텍처 유형 선택 (Hub/Virtual/Registry)
  ☐ 골든 레코드 모델 설계
  ☐ 매칭 규칙·신뢰도 점수 기준 정의

Phase 3: 구현 (6~12개월)
  ☐ ETL 파이프라인 구축
  ☐ 중복 탐지·병합 알고리즘 구현
  ☐ MDM 플랫폼 구축 (Informatica, IBM InfoSphere 등)

Phase 4: 운영
  ☐ 데이터 스튜어드 역할 배정
  ☐ 변경 이벤트 스트림 발행 (CDC)
  ☐ 품질 KPI 모니터링 대시보드
```

### 기술사 판단 포인트

1. **아키텍처 선택**: 통합 강도 vs 유연성 트레이드오프 명확히 제시
2. **매칭 [[001_algorithm_definition|알고리즘]]**: 결정적 매칭(완전 일치) + 확률적 매칭(유사도) 조합
3. **거버넌스**: 기술보다 조직·프로세스 문제가 더 어려움 — [[067_data_steward_data_quality|데이터 스튜어드]] 필수
4. **클린 룸**: [[791_gdpr_eu|GDPR]]/[[783_pipa_korea|개인정보보호법]] 준수하면서 [[001_dikw_pyramid|데이터]] 공동 활용 시 필수 선택지

📢 **섹션 요약 비유**: [[539_mdm_master_data_management|MDM]] 구축은 집 정리와 같다. 먼저 무엇이 있는지 파악([[613_profiling_gprof|프로파일링]])하고, 중복을 버리고(중복 제거), 제자리에 놓고(표준화), 잘 정돈된 상태를 유지(거버넌스)해야 한다.

## Ⅴ. 기대효과 및 결론

### [[539_mdm_master_data_management|MDM]] 도입 기대효과

| 영역 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 품질 | 중복률 15~30% | 중복률 < 1% | 90%+ 개선 |
| 마케팅 효율 | 동일 고객 중복 발송 | 단일 정확 고객 [[655_ir_detection_analysis|식별]] | 마케팅 비용 절감 |
| 분석 정확도 | 집계 오차 큼 | 신뢰 가능 집계 | [[018_kpi|KPI]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확보 |
| 규정 준수 | [[781_personal_information|개인정보]] 위치 불명 | 전 시스템 즉시 삭제 가능 | [[791_gdpr_eu|GDPR]] 대응 |
| 시스템 통합 | 포인트-투-포인트 연결 | [[539_mdm_master_data_management|MDM]] 단일 [[152_hub_dummy_switching_intelligent|허브]] | 통합 복잡도 감소 |

### 결론

MDM은 [[001_dikw_pyramid|데이터]] 기반 경영의 기반 인프라다. 기술적 구현보다 조직의 [[052_data_governance_framework|데이터 거버넌스]] 체계와 [[273_data_stewardship|데이터 스튜어드십]] 문화가 성공 요인이다. [[001_dikw_pyramid|데이터]] 클린 룸은 MDM의 경계를 넘어 파트너사·플랫폼 간 프라이버시 안전 협업을 가능케 하는 차세대 [[386_data_clean_room_sharing|데이터 공유]] 패러다임이다.

📢 **섹션 요약 비유**: MDM은 기업의 "공식 전화번호부"다. 모든 부서가 같은 전화번호부를 쓰면 혼선이 없어진다. [[001_dikw_pyramid|데이터]] 클린 룸은 두 회사가 서로의 전화번호부를 직접 보지 않고 "공통 고객이 몇 명인지"만 확인하는 방법이다.

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 핵심 목표 | [[539_mdm_master_data_management|MDM]] (Master [[001_dikw_pyramid|Data]] [[372_management|Management]]) | 핵심 [[001_dikw_pyramid|데이터]] 단일 권위 [[288_version_ihl_tos_total_length|버전]] 관리 |
| 최종 산출물 | 골든 레코드 (Golden Record) | 중복 제거·병합된 단일 진실 레코드 |
| 아키텍처 | [[152_hub_dummy_switching_intelligent|허브]]형 / 가상형 / 레지스트리형 | [[539_mdm_master_data_management|MDM]] 시스템 설계 방식 |
| [[386_data_clean_room_sharing|데이터 공유]] | [[001_dikw_pyramid|데이터]] 클린 룸 ([[305_data_clean_room|Data Clean Room]]) | 프라이버시 [[571_protection_vs_security|보호]] 공동 분석 환경 |
| 관련 기술 | [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | [[539_mdm_master_data_management|MDM]] 변경 이벤트 실시간 전파 |
| 관련 프레임워크 | [[791_gdpr_eu|GDPR]] / [[783_pipa_korea|개인정보보호법]] | 클린 룸 도입 동인 |
| 조직 역할 | [[067_data_steward_data_quality|데이터 스튜어드]] | [[539_mdm_master_data_management|MDM]] [[001_dikw_pyramid|데이터]] 품질 책임자 |

### 👶 어린이를 위한 3줄 비유 설명

1. MDM은 학교에서 "홍길동"이 1반에도, 2반에도, 3반에도 다른 이름으로 등록된 것을 하나로 합쳐 "우리 학교 홍길동은 이 한 명"이라고 확정하는 것이다.

### 📈 관련 키워드 및 발전 흐름도

```text
마스터 데이터 사일로 (부서별 중복 · 불일치)
    │
    ▼
MDM: 골든 레코드 생성 · 데이터 통합
    ├─► 매칭 · 머지 · 서바이버십 규칙
    └─► Clean Room: 개인정보 보호 합동 분석
    │
    ▼
데이터 거버넌스: 품질 · 보안 · 컴플라이언스
```
2. 골든 레코드는 여러 반의 기록 중 가장 정확한 정보만 골라 만든 "공식 학생 기록부"다.
3. [[001_dikw_pyramid|데이터]] 클린 룸은 두 학교가 서로의 학생 명단을 공유하지 않고 "두 학교에 모두 다니는 학생이 몇 명인지"만 같이 세어보는 비밀 방이다.
