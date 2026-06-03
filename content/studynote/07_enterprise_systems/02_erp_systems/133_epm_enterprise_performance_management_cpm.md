+++
title = "133. EPM/CPM (Enterprise Performance Management) - 기업 성과 관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EPM(Enterprise [Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/), =[CPM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/150_cpm_critical_path_method/))은 <strong>기업의 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 목표를 재무·운영 성과 지표로 분해하고 계획→실행→<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링→분석의 순환으로 경영 성과를 관리</strong>하는 시스템이다.
> 2. **가치**: ERP가 "운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기록"한다면, EPM은 <strong>"<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 분석하여 의사결정을 지원"</strong>하며, 예산 계획·실적 비교·시나리오 분석·[KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 대시보드가 핵심 기능이다.
> 3. **판단 포인트**: [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/)(Balanced Scorecard)가 EPM의 성과 관리 프레임워크이며, [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) Hyperion·SAP BPC·Anaplan이 대표 솔루션이다.

---

## Ⅰ. 개요 및 필요성

```text
EPM 순환: 전략 → 계획(예산) → 실행 → 모니터링(KPI) → 분석 → 조정
  ERP: 운영 데이터 (거래, 재고)
  EPM: 경영 데이터 (예산, 성과, 예측)
```

- **📢 섹션 요약 비유**: ERP는 **계기판(현재 속도·연료)**, EPM은 <strong>내비게이션(목적지까지 경로·도착 예측)</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 기능 | 설명 |
|:---|:---|
| **계획·예산** | 연간 예산·Rolling Forecast |
| **실적 분석** | 예산 vs 실적 비교 |
| **시나리오** | What-if 분석 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/">KPI</a> 대시보드</strong> | [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) 기반 성과 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |

---

## Ⅲ~Ⅴ. 결론

EPM은 <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 경영 의사결정으로 전환</strong>하는 핵심 시스템이며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 예측과 결합하여 지능형 경영 관리로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>EPM/<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/150_cpm_critical_path_method/">CPM</a></strong> | 기업 성과 관리 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/">BSC</a></strong> | 균형 성과 관리 (4관점) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> | 운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/">KPI</a></strong> | [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) |
| **Anaplan** | 클라우드 EPM 대표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Excel 기반 예산 (2000s)] → [Oracle Hyperion (2005~)]
    → [클라우드 EPM (Anaplan, 2015~)]
    → [xP&A (확장 계획, 2020~)]
    → [현재: AI EPM — 예측·시나리오 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ERP는 **계기판**(지금 속도·연료)이에요. EPM은 **내비게이션**(목적지 경로)이에요.
2. 내비가 없으면 "지금 어디쯤이지? 언제 도착하지?" **알 수 없어요**.
3. EPM 덕분에 회사가 **목표까지 얼마나 남았는지** 정확히 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 482

← **이전**: [132. HRIS·e-HR·인재관리시스템 (Talent Management) - 디지털 인사 관리](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/132_hris_e_hr_talent_management_system/)
**다음**: [134. ESG 경영 & IT 시스템 - 탄소 추적·ESG 데이터 관리](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/134_esg_management_it_system_carbon_tracking/) →

---
