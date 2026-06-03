+++
title = "115. CDP (Customer Data Platform) - 통합 고객 프로파일·Single Customer View"
date = 2026-04-19

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)([Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Platform)는 웹·앱·매장·[CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)·소셜 등 **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 모든 고객 접점 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집하여 통합 고객 프로파일(Single [Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))**을 구축하는 패키지 소프트웨어다.
> 2. **가치**: DMP([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) Platform)가 익명 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 기반·광고 타겟팅 전용이라면, CDP는 **실명([1st Party](/knowledge-base/studynote/12_it_management/05_security_compliance/279_cdp_first_party/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반**으로 고객 ID를 통합하여 마케팅·CS·영업 전 부서에서 활용 가능한 **360° 고객 뷰**를 제공한다.
> 3. **판단 포인트**: CDP의 핵심은 **ID Resolution(동일 고객의 이메일·전화·앱ID를 1명으로 통합)**이며, [Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/)·mParticle·Treasure Data가 대표 제품이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    CDP의 데이터 통합 흐름                              │
├───────────────────────────────────────────────────────┤
│  [데이터 소스]                                        │
│   웹 로그 + 앱 이벤트 + CRM + POS(매장)              │
│   + 이메일 + 소셜 + CS 상담 이력                     │
│         │                                             │
│         ▼                                             │
│  [CDP - ID Resolution]                                │
│   이메일=a@b.com + 전화=010-1234 + 앱ID=user_123     │
│   → 동일 고객 "김철수"로 통합                         │
│         │                                             │
│         ▼                                             │
│  [통합 고객 프로파일]                                 │
│   김철수: 최근 구매 3건, 앱 DAU, 불만 CS 1건         │
│         │                                             │
│         ▼                                             │
│  [활용] 마케팅 타겟팅 | CS 컨텍스트 | 이탈 예측       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: CDP는 각 과목 선생님(채널)이 따로 적은 학생 평가를 **한 장의 생활기록부**로 합치는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) vs DMP vs [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)

| 비교 | [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) | DMP | [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) |
|:---|:---|:---|:---|
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)** | 자사 거래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 익명 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) ([3rd Party](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/)) | **자사 실명 ([1st Party](/knowledge-base/studynote/12_it_management/05_security_compliance/279_cdp_first_party/))** |
| **ID** | 고객ID | [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)/IDFA | **통합 ID (Resolution)** |
| **용도** | 영업·CS | 광고 타겟팅 | **전사 고객 분석** |
| **지속성** | 영구 | [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 만료 | **영구** |

- **📢 섹션 요약 비유**: CRM은 가게 단골 명부, DMP는 전단지 배포 목록(익명), CDP는 고객의 모든 기록을 합친 **VIP 카드**이다.

---

## Ⅲ. 비교 및 연결

[3rd Party](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 폐지(Chrome 2025)로 DMP의 가치가 하락하면서 **[1st Party](/knowledge-base/studynote/12_it_management/05_security_compliance/279_cdp_first_party/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)**의 중요성이 급증하고 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스 인벤토리**: 현재 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되어 있는지 목록화.
2. **ID Resolution [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**: 이메일·전화·앱ID [매핑 규칙](/knowledge-base/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/) 정의.
3. **Activation 연동**: [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) → 마케팅 자동화(Braze)·분석(Amplitude) 연결.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) 미도입 | [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) 도입 | 개선 |
|:---|:---|:---|:---|
| 고객 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 채널별 분리 | **통합 1명** | 360° 뷰 |
| 마케팅 전환율 | 2% | **5%** | 2.5× |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 부서 | 마케팅만 | **전사** | 확장 |

CDP는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 세분화·예측 모델과 결합하여 "고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 → 통합 → 인사이트 → 실행"이 자동화되는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ID Resolution** | CDP의 핵심 기술, 동일 고객 통합 |
| **DMP** | 익명 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 기반, CDP의 이전 세대 |
| **[1st Party](/knowledge-base/studynote/12_it_management/05_security_compliance/279_cdp_first_party/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)** | CDP가 수집·관리하는 자사 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **[CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)** | CDP와 연동하여 영업·CS에 통합 프로파일 제공 |
| **[Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) / mParticle** | 대표적 [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) 제품 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CRM (1990s) — 자사 거래 데이터 관리]
    │
    ▼
[DMP (2010s) — 3rd Party 쿠키 기반 광고 타겟팅]
    │
    ▼
[CDP (2015~) — 1st Party 실명 데이터 통합]
    │
    ▼
[3rd Party 쿠키 폐지 (2023~) — CDP 중요성 급증]
    │
    ▼
[현재: AI CDP — 자동 세분화·예측·개인화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 국어 선생님은 "김철수 발표 잘함", 수학 선생님은 "김철수 계산 빠름"이라고 **따로따로** 적어요.
2. CDP는 이 평가들을 **한 장의 생활기록부**로 합쳐서, 담임 선생님이 김철수를 **전부 이해**할 수 있게 해요.
3. 덕분에 "김철수는 발표에 자신감 있으니까 수학 발표 대회에 추천하자!"처럼 **똑똑한 결정**을 할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 482

← **이전**: [114. AI 기반 CRM (AI-Powered CRM) - Salesforce Einstein·예측 분석·생성형 AI](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/114_ai_based_crm_salesforce_einstein/)
**다음**: [116. 1st Party Data 전략 (Cookie-less Marketing) - 쿠키 폐지 후 데이터 주권 확보](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/116_first_party_data_cookie_less_strategy/) →

---
