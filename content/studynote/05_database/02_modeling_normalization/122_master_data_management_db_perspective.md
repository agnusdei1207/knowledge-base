---
title: 122. 마스터 데이터 관리 (MDM, Master Data Management) - 데이터 품질·일관성의 근간
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MDM은 고객·상품·조직·자산 등 **핵심 마스터 [[001_dikw_pyramid|데이터]]의 단일 골든 레코드(Golden Record)를 [[087_process_state_transition|생성]]·유지**하여, 전사 시스템([[081_erp_enterprise_resource_planning|ERP]]·[[107_crm_customer_relationship_management|CRM]]·[[209_data_warehouse_schema_on_write|DW]]) 간 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]과 품질을 보장하는 관리 체계다.
> 2. **가치**: 마스터 [[001_dikw_pyramid|데이터]]가 시스템마다 다르면(고객명이 [[081_erp_enterprise_resource_planning|ERP]]="홍길동", [[107_crm_customer_relationship_management|CRM]]="길동 홍") **보고서 불일치·중복 마케팅·재고 오류**가 발생하며, MDM이 **단일 진실 원천(Single Source of Truth)**을 제공한다.
> 3. **판단 포인트**: [[235_registry_immutable_tag|Registry]]([[316_reference_pattern_nosql|참조]]형)·Consolidation(통합형)·Centralized(중앙 집중형)·Coexistence(공존형)의 4가지 구현 스타일을 구분하고, [[052_data_governance_framework|데이터 거버넌스]]와의 연계가 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    MDM 필요성                                         │
├───────────────────────────────────────────────────────┤
│  [MDM 없음]                                           │
│   ERP: 고객ID=1001, 홍길동                           │
│   CRM: 고객ID=A99, 길동 홍                           │
│   DW: ???  → 같은 사람? 다른 사람?                   │
│                                                       │
│  [MDM 적용]                                           │
│   MDM Hub: 고객 골든 레코드 = "홍길동, ID=M001"      │
│   ERP: M001 → 홍길동 ✅                              │
│   CRM: M001 → 홍길동 ✅                              │
│   → 전사 일관된 고객 뷰                              │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: MDM은 전사 **주민등록 시스템**이다. 이름이 조금씩 다르게 적힌 주민을 하나의 정확한 레코드로 통합한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[539_mdm_master_data_management|MDM]] 구현 스타일

| 스타일 | 설명 | 적합 |
|:---|:---|:---|
| **[[235_registry_immutable_tag|Registry]]** | 기존 시스템에 [[316_reference_pattern_nosql|참조]] 키만 매핑 | 낮은 침습성 |
| **Consolidation** | 읽기 전용 [[152_hub_dummy_switching_intelligent|허브]]에 통합 | 분석·보고 |
| **Centralized** | [[539_mdm_master_data_management|MDM]] [[152_hub_dummy_switching_intelligent|허브]]가 유일한 원천 | **최고 [[194_consistency_database_integrity|일관성]]** |
| **Coexistence** | [[152_hub_dummy_switching_intelligent|허브]] ↔ 시스템 양방향 동기 | 유연성 |

- **📢 섹션 요약 비유**: Registry는 전화번호부([[316_reference_pattern_nosql|참조]]만), Centralized는 중앙은행(모든 거래의 원천)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[539_mdm_master_data_management|MDM]] 없음 | [[539_mdm_master_data_management|MDM]] 적용 |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]** | 시스템별 상이 | **골든 레코드 통합** |
| **보고서** | 불일치 | **신뢰 가능** |
| **중복** | 빈번 | **제거** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[539_mdm_master_data_management|MDM]] 구축 핵심 단계
1. **[[613_profiling_gprof|프로파일링]]**: 현행 [[041_contractor_late_penalty|데이터 품질 진단]].
2. **매칭/병합**: 중복 레코드 [[655_ir_detection_analysis|식별]]·통합.
3. **골든 레코드**: 단일 마스터 [[087_process_state_transition|생성]].
4. **거버넌스**: [[067_data_steward_data_quality|데이터 스튜어드]] 지정·[[164_policy|정책]] 수립.

---

## Ⅴ. 기대효과 및 결론

MDM은 **[[052_data_governance_framework|데이터 거버넌스]]의 기술적 구현체**이며, [[193_crl_distribution_point_cdp|CDP]]·[[211_data_mesh_domain_ownership|데이터 메시]]·[[190_ai_llm_requirements_specification|AI]] 학습 [[001_dikw_pyramid|데이터]] 품질의 기반이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **골든 레코드** | MDM의 핵심 산출물 |
| **[[052_data_governance_framework|데이터 거버넌스]]** | MDM의 [[164_policy|정책]]·조직 프레임워크 |
| **[[193_crl_distribution_point_cdp|CDP]]** | 고객 마스터의 마케팅 특화 [[288_version_ihl_tos_total_length|버전]] |
| **[[001_dikw_pyramid|데이터]] 품질** | MDM이 보장하는 핵심 가치 |
| **[[067_data_steward_data_quality|데이터 스튜어드]]** | [[539_mdm_master_data_management|MDM]] 운영 책임자 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 데이터 정제 (엑셀, 2000s)]
    │
    ▼
[MDM 솔루션 (Informatica·IBM, 2005~)]
    │
    ▼
[클라우드 MDM (Reltio, 2015~)]
    │
    ▼
[데이터 메시 + MDM (2020~) — 분산 소유권]
    │
    ▼
[현재: AI MDM — 자동 매칭·병합·품질 보정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MDM은 학교 **출석부 관리 시스템**이에요. 같은 학생이 다른 이름으로 등록되면 안 돼요.
2. "홍길동"과 "길동 홍"이 같은 사람인지 확인해서 **하나로 합쳐요** (골든 레코드).
3. 덕분에 어떤 선생님(시스템)이 봐도 **같은 학생 정보**를 볼 수 있답니다!
