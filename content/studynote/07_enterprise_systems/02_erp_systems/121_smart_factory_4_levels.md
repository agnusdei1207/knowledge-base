---
title: "Smart Factory 4 Levels"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 121
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 4단계는 제조 현장의 [디지털 전환](/studynote/12_it_management/01_governance_strategy/055_digital_transformation/) 수준을 <strong>기초(ICT 미적용)->중간1(자동화)->중간2(연결·가시화)->고도화(지능화·자율 최적화)</strong>로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 성숙도 모델이다.
> 2. **가치**: 기업이 현재 위치를 진단하고 <strong>다음 단계로 가기 위한 투자 우선순위</strong>를 결정하는 로드맵 역할을 하며, 정부의 [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 지원 사업에서도 이 단계를 기준으로 지원 수준을 결정한다.
> 3. **판단 포인트**: 4단계(고도화)는 <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>·<a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a>·자율 최적화</strong>가 핵심이며, 대부분 국내 제조업은 1~2단계에 머물러 있다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    스마트 팩토리 성숙도 4단계                          |
+-------------------------------------------------------+
|  Level 1 (기초): 수기 관리, ICT 미적용               |
|  Level 2 (중간1): 바코드·POP, 자동화 설비            |
|  Level 3 (중간2): MES·ERP 연동, 실시간 모니터링      |
|  Level 4 (고도화): AI 예측, 디지털 트윈, 자율 최적화 |
|                                                       |
|  국내 현황: 70%+ 기업이 Level 1~2                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 4단계는 자동차 운전 자율주행 레벨과 비슷하다. Level 1은 수동 운전, Level 4는 완전 자율주행이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 단계별 핵심 기술

| 단계 | 핵심 기술 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 |
|:---|:---|:---|
| **기초** | 수기·엑셀 | 사후 분석 |
| **중간1** | [POP](/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/)·바코드·자동화 설비 | 수집 |
| **중간2** | [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)·[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)·[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | <strong>실시간 <a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링</strong> |
| **고도화** | <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>·<a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a>·<a href="/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/">CPS</a></strong> | **예측·자율 최적화** |

- **📢 섹션 요약 비유**: Level 1은 종이 지도, Level 2는 GPS, Level 3는 실시간 네비, Level 4는 자율주행 네비다.

---

## Ⅲ. 비교 및 연결

| 비교 | Level 1~2 | Level 3~4 |
|:---|:---|:---|
| **의사결정** | 사후·직감 | <strong>실시간·<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반</strong> |
| **자동화** | 부분 | <strong>전체 (<a href="/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/">CPS</a>)</strong> |
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong> | 없음 | **예측·최적화** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Level 4 핵심 구성 요소
1. <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/">CPS</a> (Cyber-Physical System)</strong>: 물리 설비와 사이버 모델 연동.
2. <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a></strong>: 공장의 가상 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) -> 시뮬레이션.
3. <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 품질 예측</strong>: 불량 발생 전 예측 -> 예방.

---

## Ⅴ. 기대효과 및 결론

[스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 4단계는 <strong>제조업 <a href="/studynote/12_it_management/01_governance_strategy/055_digital_transformation/">디지털 전환</a>의 로드맵</strong>이며, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)의 발전으로 Level 4 고도화가 가속화되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/">MES</a></strong> | Level 3의 핵심 시스템 |
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/">POP</a></strong> | Level 2의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a></strong> | Level 4의 가상 공장 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/167_cps_cyber_physical_system/">CPS</a></strong> | Level 4의 사이버-물리 통합 |
| **Industry 4.0** | [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/)의 상위 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 제조 (Level 1, ~2000s)]
    |
    v
[자동화 + POP (Level 2, 2005~)]
    |
    v
[MES + IoT 실시간 (Level 3, 2015~)]
    |
    v
[AI + 디지털 트윈 (Level 4, 2020~)]
    |
    v
[현재: Industry 5.0 — 인간-AI 협업 제조]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Level 1은 <strong>종이에 직접 기록</strong>하는 옛날 공장이에요.
2. Level 3은 <strong>화면에서 공장 상태를 실시간</strong>으로 볼 수 있어요.
3. Level 4는 <strong>AI가 알아서 문제를 미리 예측하고 해결</strong>하는 미래 공장이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 482

<- **이전**: [120. POP (Point of Production) - 생산 현장 실적 수집 시스템](/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/)
**다음**: [122. PLM (Product Lifecycle Management) - 제품 전주기 관리 시스템](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) ->

---
