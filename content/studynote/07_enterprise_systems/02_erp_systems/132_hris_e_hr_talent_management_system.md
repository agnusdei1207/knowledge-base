+++
title = "132. HRIS·e-HR·인재관리시스템 (Talent Management) - 디지털 인사 관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HRIS(Human Resource Information System)는 <strong>인사 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(급여·근태·조직)를 통합 관리</strong>하는 시스템이고, e-HR은 <strong>웹 기반 셀프서비스(휴가신청·급여조회)</strong>를 제공하며, [TMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/098_tms_transportation_management_system/)(Talent [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System)는 <strong>채용→육성→평가→승계의 인재 라이프사이클을 관리</strong>한다.
> 2. **가치**: 수작업 인사 관리는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 오류·<a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>·분석 불가</strong>이지만, 디지털 HR은 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반 의사결정(People Analytics)</strong>으로 이직 예측·적합 인재 배치를 실현한다.
> 3. **판단 포인트**: SAP SuccessFactors·Workday가 글로벌 표준이며, AI가 이력서 스크리닝·이직 예측·맞춤 교육 추천에 활용되고 있다.

---

## Ⅰ. 개요 및 필요성

```text
HRIS: 인사 데이터 (급여·근태·조직)
e-HR: 셀프서비스 (휴가·급여조회)
TMS:  채용 → 온보딩 → 교육 → 평가 → 승계
  → People Analytics: 데이터 기반 HR 의사결정
```

- **📢 섹션 요약 비유**: HRIS는 인사과의 <strong>장부(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>)</strong>, e-HR은 **직원용 키오스크(셀프서비스)**, TMS는 **인재 육성 로드맵**.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 시스템 | 핵심 기능 |
|:---|:---|
| **HRIS** | 급여·근태·조직 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **e-HR** | 셀프서비스·전자결재 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/098_tms_transportation_management_system/">TMS</a></strong> | 채용·교육·평가·승계 |
| **People Analytics** | 이직 예측·인재 배치 |

---

## Ⅲ~Ⅴ. 결론

디지털 HR은 <strong>People Analytics + AI로 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반 인사 혁신</strong>을 실현하며, 단순 관리에서 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 인재 경영으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **HRIS** | 인사 정보 시스템 |
| **e-HR** | 웹 셀프서비스 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/098_tms_transportation_management_system/">TMS</a></strong> | 인재 관리 (라이프사이클) |
| **People Analytics** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 HR |
| **Workday** | 클라우드 HR 대표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수작업 인사 (1990s)] → [HRIS (SAP HR, 2000s)]
    → [e-HR 셀프서비스 (2005~)] → [TMS (2010s)]
    → [People Analytics (2018~)]
    → [현재: AI HR — 이력서 스크리닝·이직 예측 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. HRIS는 회사의 <strong>직원 명부</strong>예요. 누가 어디서 일하고 급여가 얼마인지 기록해요.
2. e-HR은 <strong>키오스크</strong>예요. 직원이 직접 휴가를 신청하고 급여를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있어요.
3. TMS는 <strong>인재 육성 계획</strong>이에요. 누구를 **어떻게 키울지** 체계적으로 관리해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 482

← **이전**: [131. 그룹웨어 & Enterprise 2.0 협업 - 기업 협업 플랫폼의 진화](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/131_groupware_enterprise_2_0_collaboration/)
**다음**: [133. EPM/CPM (Enterprise Performance Management) - 기업 성과 관리](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/133_epm_enterprise_performance_management_cpm/) →

---
