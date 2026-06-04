+++
title = "마이데이터 (MyData)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

> **핵심 인사이트 3줄**
> 1. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))는 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집·이용·제공을 직접 통제하는 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 자기결정권 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유통 패러다임이다.
> 2. 한국은 2021년 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)를 시작으로 의료·공공·통신 등 전 분야로 확대해 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동권을 법제화하고 있다.
> 3. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 개인에게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통제권을 부여하는 동시에, 기업에겐 동의 기반 개인화 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 새로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비즈니스 모델의 기회를 제공한다.

---

## Ⅰ. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)의 정의와 배경

[마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))는 <strong>개인이 자신의 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 주도적으로 관리·활용하는 <a href="/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/">데이터 주권</a>(<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/410_ai_intellectual_property_data_sovereignty_data_act/">Data Sovereignty</a>) 개념</strong>이다.

### 기존 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유통 vs [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)

| 특성          | 기존 방식              | [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)              |
|-------------|----------------------|------------------------|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주체   | 기업 ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유)    | 개인 ([데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/))      |
| 수집 동의    | 포괄적·묵시적         | 명시적·세분화된 동의    |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동   | 기업 간 계약 기반     | 개인 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청 기반      |
| 투명성       | 낮음                  | 높음 (이용 내역 조회)   |

### 법적 근거

- **한국**: 신용정보법 개정(2020), [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)법 개정(2020) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동권
- **EU**: [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 제20조 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동권 (Right to [Data Portability](/knowledge-base/studynote/09_security/16_data_privacy/795_data_portability/))
- **미국**: [CCPA](/knowledge-base/studynote/09_security/16_data_privacy/800_ccpa/) — 캘리포니아 소비자 프라이버시법

📢 **섹션 요약 비유**: [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 은행 계좌를 다른 앱으로 옮기는 권리다 — 내 돈([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 내가 원하는 곳에 가져갈 수 있어야 한다는 원칙.

---

## Ⅱ. 한국 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)

### [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구조 (2022년 1월 정식 출범)

```
개인 ---> 마이데이터 앱 (토스, 뱅크샐러드, 카카오페이)
   |
   +- 동의 -> 마이데이터 사업자 API 요청
                   |
            금융 API (은행·카드·증권·보험)
                   |
         통합 금융 정보 조회·분석·서비스
```

### [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 정보 범위

| 분야    | 포함 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)                           |
|-------|---------------------------------------|
| 은행    | 계좌, 거래 내역, 대출 현황             |
| 카드    | 이용 내역, 청구 정보                   |
| 증권    | 보유 종목, 잔고                        |
| 보험    | 가입 내역, 보험료                      |
| 통신    | 요금 정보 (확대 예정)                   |

<strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/">마이데이터</a> 사업자 허가</strong>: 금융위원회 허가 -> [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준 준수 의무

📢 **섹션 요약 비유**: 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 여러 은행 통장을 한 앱에서 보는 것이다 — 은행마다 앱을 켜지 않아도 내 모든 자산을 한눈에 볼 수 있다.

---

## Ⅲ. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 아키텍처

```
+-------------------------------------------------------+
|                 마이데이터 플랫폼                      |
|                                                       |
|  개인      --->  마이데이터 사업자  --->  정보 제공 기관|
| (본인 인증)    (앱/플랫폼)          (은행·카드사 등) |
|                   |                       |          |
|                OAuth 2.0                 Open API     |
|                /동의 관리                REST/JSON    |
|                   |                                   |
|           마이데이터 종합 포털                        |
|           (금융결제원 중계)                           |
+-------------------------------------------------------+
```

### 기술 표준

- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong>: OAuth 2.0 + [PKCE](/knowledge-base/studynote/09_security/05_web_app_security/509_pkce_public_client/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong>: [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/[JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), OpenAPI 3.0 스펙
- **보안**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3, 상호 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/)
- **중계**: 금융결제원 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 중계 서버

📢 **섹션 요약 비유**: [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) API는 통역사가 있는 외교 회담이다 — 각기 다른 언어(은행·카드·보험 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식)를 공통 언어([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준)로 번역해 하나의 앱에 모아준다.

---

## Ⅳ. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 비즈니스 모델

| 모델              | 내용                                |
|-----------------|-------------------------------------|
| 자산 통합 관리    | PFM (Personal Financial [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/)) |
| 개인화 추천       | 맞춤 금융상품·보험 추천             |
| 신용 평가        | 대안 신용 평가 (통신·쇼핑 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))   |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마켓플레이스 | 개인 동의 기반 익명화 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 판매  |
| 헬스케어 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) | 진료·검진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 건강 관리    |

### [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 3.0 비전

```
1.0: 조회 (내 데이터 한곳에 보기)
2.0: 분석 (AI 기반 맞춤 조언)
3.0: 실행 (자동 금융 최적화·자산 관리 AI)
```

📢 **섹션 요약 비유**: [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 비즈니스는 개인 비서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다 — 내 모든 금융 정보를 파악한 AI가 "이 대출로 갈아타면 월 3만 원 절약돼요"를 자동으로 알려준다.

---

## Ⅴ. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 확대와 도전 과제

### 분야별 확대 현황

| 분야    | [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 현황                      |
|-------|-------------------------------|
| 금융    | 2022년 법 시행, 사업자 100개+  |
| 의료    | 마이헬스웨이 시범 (2023~)      |
| 공공    | 행정데이터 이동권 논의 중       |
| 통신    | 통신 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 추진 중         |

### 도전 과제

| 과제          | 내용                           |
|-------------|-------------------------------|
| [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 대규모 집중화 -> 해킹 위험       |
| 정보 비대칭   | 개인의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치 이해 부족    |
| 플랫폼 독점   | 대형 앱에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쏠림 현상      |
| 동의 피로     | 과도한 동의 요청 -> 묵시적 동의  |

📢 **섹션 요약 비유**: [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 도전 과제는 집 열쇠를 한 곳에 보관하는 것이다 — 편리하지만, 그 보관함이 털리면 모든 열쇠가 한꺼번에 노출된다.

---

## 📌 관련 개념 맵

```
마이데이터 (MyData)
+-- 법적 기반
|   +-- 데이터 이동권 (Right to Data Portability)
|   +-- GDPR 제20조
|   +-- 한국 신용정보법·개인정보보호법
+-- 기술
|   +-- OAuth 2.0 / PKCE
|   +-- Open API (REST/JSON)
|   +-- 마이데이터 중계 서버
+-- 서비스
|   +-- 금융 마이데이터 (PFM)
|   +-- 의료 마이데이터 (마이헬스웨이)
|   +-- 공공 마이데이터
+-- 비즈니스 모델
    +-- 자산 통합 관리
    +-- 개인화 금융 추천
    +-- 대안 신용 평가
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|                마이데이터 발전 흐름                              |
+--------------+--------------------+-----------------------------+
| 2016년       | EU GDPR 입법       | 데이터 이동권 법제화 시작    |
| 2018년       | GDPR 시행          | 글로벌 개인정보 패러다임 전환|
| 2020년       | 한국 데이터 3법 개정| 신용정보법·개인정보보호법   |
| 2022년       | 금융 마이데이터 출범| 토스·뱅크샐러드·카카오페이  |
| 2023년       | 마이헬스웨이 시범  | 의료 마이데이터 본격 추진   |
| 2024~현재    | 전 분야 확대       | 통신·공공·유통 데이터 이동권|
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
개인정보 자기결정권 -> 마이데이터 -> 데이터 이동권
       v                   v              v
GDPR/개인정보법    금융·의료·공공    Open API 표준
       v
PFM 서비스 -> AI 개인화 -> 데이터 주권 실현
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 내 성적표를 내가 관리하는 것이다 — 선생님(은행·병원)이 가지고 있던 성적표를 내가 직접 볼 수 있고, 필요한 곳에 가져갈 수 있다.
2. 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 여러 통장을 하나의 앱에서 보는 것이다 — 은행마다 앱을 열지 않아도 내 모든 돈이 어디에 얼마나 있는지 한눈에 알 수 있다.
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동권은 전학 갈 때 성적표를 가져갈 권리다 — 학교([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 바꿔도 내 기록([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 내가 새 학교(앱)에 직접 가져갈 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 244 / 262

<- **이전**: [31. 데이터 경제 — 데이터가 자산이 되는 세계](/knowledge-base/studynote/16_bigdata/13_intro_trends/243_data_economy/)
**다음**: [공공 빅데이터 (Public Big Data)](/knowledge-base/studynote/16_bigdata/13_intro_trends/245_public_bigdata/) ->

---
