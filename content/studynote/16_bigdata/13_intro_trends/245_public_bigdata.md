---
title: "Public Big Data"
date: "2026-03-03"
tags:
  - "studynote-bigdata"
weight: 245
---
> **핵심 인사이트 3줄**
> 1. 공공 빅데이터는 정부·공공기관이 생산·보유한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 민간에 개방해 사회·경제적 가치를 창출하는 [데이터 민주화](/studynote/16_bigdata/01_intro/010_data_democratization/)의 핵심 인프라다.
> 2. 한국의 공공데이터포털([data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/).go.kr)은 78,000여 개 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋을 제공하며, 교통·복지·의료·환경 분야 혁신 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 기반이 되고 있다.
> 3. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·[개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)·민감 정보 비식별화가 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용의 3대 과제이며, FAIR 원칙(Findable·Accessible·Interoperable·Reusable)이 국제 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개방의 표준이다.

---

## Ⅰ. 공공 빅데이터의 정의와 특성

공공 빅데이터(Public Big [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 <strong>정부·지자체·공공기관이 행정·사업 과정에서 생산·수집한 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 디지털 형태로 공개한 것</strong>이다.

### 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형

| 유형          | 예시                               |
|-------------|-----------------------------------|
| 행정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | 인구 통계, 사업자 등록, 부동산 거래 |
| 의료 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | 건강보험 진료 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 건강 통계     |
| 교통 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)/지하철 운행, 교통량, 주차 정보 |
| 환경 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | 대기질, 수질, 기상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)           |
| 재정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | 국가 예산·결산, 공공 조달           |
| 교육 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)  | 학교 정보, 교육 통계               |

### 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특성

- <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong>: 공공기관의 공식 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)
- **규모**: 국가 단위 대규모 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)
- **희소성**: 민간이 수집 불가능한 정보
- **공공성**: 사회 전체의 이익을 위한 개방

📢 **섹션 요약 비유**: 공공 빅데이터는 국가가 운영하는 도서관이다 — 세금으로 만든 책([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 모든 시민이 무료로 빌려 볼 수 있다.

---

## Ⅱ. 한국 [공공데이터 개방](/studynote/11_design_supervision/01_audit_framework/060_open_data_public_api_standards/) 현황

### 공공데이터포털 ([data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/).go.kr)

```
공공데이터포털 현황 (2024년 기준):
  - 등록 데이터셋: 78,000여 개
  - API 서비스: 8,000여 개
  - 제공 기관: 1,100여 개
  - 월간 이용: 1억 건 이상
```

### 주요 활용 사례

| 분야   | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)                         | 사용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)             |
|------|-------------------------------|------------------------|
| 교통  | 카카오맵 실시간 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 정보         | 공공 교통 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)           |
| 부동산 | 호갱노노 실거래가 분석           | 국토부 아파트 실거래가   |
| 날씨  | 기상 예보 앱                    | 기상청 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)              |
| 의료  | 코로나19 확진자 동선 추적         | 건강보험공단 진료 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 창업  | 상권 분석 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)                  | 소상공인시장진흥공단     |

📢 **섹션 요약 비유**: 공공데이터포털은 국가 주방이다 — 정부가 키운 식재료(원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 민간 요리사(개발자·기업)가 자유롭게 가져다 요리([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 만든다.

---

## Ⅲ. FAIR 원칙 — 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개방 국제 표준

| 원칙             | 의미                          | 실천 방법              |
|--------------|------------------------------|----------------------|
| Findable (발견성) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쉽게 찾을 수 있음   | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)·검색 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)   |
| Accessible ([접근성](/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/)) | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·권한에 맞게 접근 가능 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)·개방 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)       |
| Interoperable ([상호운용성](/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)) | 표준 형식으로 교환 가능 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/CSV·표준 코드  |
| Reusable (재사용성) | 라이선스 명확, 재사용 허용 | CCL·공공누리 라이선스   |

### 5성급 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([Tim](/studynote/01_computer_architecture/15_advanced_topics/737_thermal_paste_tim/) Berners-Lee)

```
★     : 어떤 형식이든 오픈 라이선스
★★    : 기계 판독 가능 구조화 형식 (xls -> csv)
★★★   : 비독점 형식 (csv, json)
★★★★  : RDF URI 사용 (연결 데이터)
★★★★★ : 다른 데이터와 링크 (Linked Open Data)
```

📢 **섹션 요약 비유**: FAIR 원칙은 요리 레시피 공유 기준이다 — 인터넷에서 찾기 쉽고(Findable), 누구나 볼 수 있고(Accessible), 다른 레시피와 합치기 쉽고(Interoperable), 마음대로 써도 되는(Reusable) 레시피가 좋은 레시피이다.

---

## Ⅳ. 공공 빅데이터 활용 — 스마트시티·행정 혁신

### 교통 빅데이터 분석

```
공공 교통 데이터 파이프라인:
  버스 GPS -> 실시간 수집 -> Apache Kafka
                                v
                         실시간 처리 (Flink)
                                v
                     배차 최적화·혼잡 예측 알림
```

### 의료 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용

- **건강보험공단 빅데이터**: 2억 건 이상 진료 내역 -> 질병 예측 모델
- <strong>DUR (Drug Utilization <a href="/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/">Review</a>)</strong>: 처방 안전성 실시간 점검
- **국가암데이터**: 암 발생·생존율 분석, 조기 발견 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발

### 사회복지 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 매칭

```
복지 사각지대 발굴:
  전기·수도 단수 데이터 + 건강보험 미납 + 복지 수급 여부
  -> AI 고위험군 예측 -> 담당자 선제 방문
```

📢 **섹션 요약 비유**: 복지 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 매칭은 동네 이장이 어려운 이웃을 찾는 것이다 — 전기가 끊기고 연락이 안 되면([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)) 먼저 찾아가는 능동적 복지를 AI로 구현한다.

---

## Ⅴ. 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)

### 공공 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 5대 기준

| 기준        | 설명                          |
|-----------|-------------------------------|
| [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)     | 실제 값과 일치                 |
| 완전성     | 필수 항목 누락 없음             |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)     | 기관 간 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 일관 유지   |
| 적시성     | 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유지                |
| 유효성     | 정해진 형식·범위 내 값          |

### [개인정보 비식별화](/studynote/16_bigdata/13_intro_trends/251_data_anonymization/) 기법

| 기법          | 방법                          | 적용 예시              |
|------------|-------------------------------|----------------------|
| 가명처리    | 개인 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 정보를 가명으로 대체  | 이름 -> 홍XX           |
| 총계처리    | 합계·평균으로 개인 정보 제거    | 개별 소득 -> 연령대 평균 |
| [k-익명성](/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/)   | k명 이상의 동일 특성 보장       | 주민등록->5세 단위 집계  |
| 범주화      | 정확한 값을 범위로 대체         | 나이 25->20대           |

📢 **섹션 요약 비유**: 비식별화는 사진 속 얼굴 모자이크 처리다 — 모자이크 후에도 사진의 내용([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치)은 유지되지만, 누가 누구인지(개인 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/))는 알 수 없다.

---

## 📌 관련 개념 맵

```
공공 빅데이터 (Public Big Data)
+-- 개방 플랫폼
|   +-- 공공데이터포털 (data.go.kr)
|   +-- 국가통계포털 (KOSIS)
|   +-- 건강보험공단 빅데이터
+-- 국제 표준
|   +-- FAIR 원칙 (Findable·Accessible·Interoperable·Reusable)
|   +-- 5성급 공공 데이터 (Tim Berners-Lee)
+-- 활용 분야
|   +-- 스마트시티 (교통·환경)
|   +-- 의료·복지 혁신
|   +-- 창업·상권 분석
+-- 품질·보호
    +-- 데이터 품질 5대 기준
    +-- 개인정보 비식별화 (k-익명성)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|               공공 빅데이터 발전 흐름                            |
+--------------+--------------------+-----------------------------+
| 2010년       | 공공데이터법 제정  | 미국 Data.gov 등장, 오픈 데이터|
| 2013년       | 공공데이터법 (한국) | data.go.kr 공식 운영         |
| 2016년       | 데이터 경제 선언   | EU 데이터 전략, 마이데이터 연계|
| 2020년       | 데이터 3법 개정   | 가명정보 처리·결합 허용       |
| 2022년       | 디지털플랫폼정부  | 공공데이터 API 고도화         |
| 2024~현재    | AI 공공 데이터    | AI 학습 공개 데이터 구축 확대  |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
공공 데이터 -> data.go.kr -> FAIR 원칙 -> 민간 서비스
    v              v            v           v
행정·의료·교통  API 개방     메타데이터    카카오맵·호갱노노
    v
비식별화 -> 개인정보 보호 -> 데이터 품질 -> 신뢰성 확보
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 공공 빅데이터는 국가가 운영하는 도서관이다 — 세금으로 만든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책을 누구나 무료로 읽고 이용할 수 있다.
2. FAIR 원칙은 좋은 도서관 운영 기준이다 — 책을 쉽게 찾고(Findable), 빌리고(Accessible), 다른 책과 합쳐 쓰고(Interoperable), 자유롭게 참고(Reusable)할 수 있어야 한다.
3. 비식별화는 사진 속 얼굴 모자이크다 — 내용([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치)은 유지하되, 누가 누구인지([개인정보](/studynote/09_security/16_data_privacy/781_personal_information/))는 알 수 없게 처리한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 245 / 262

<- **이전**: [마이데이터 (MyData)](/studynote/16_bigdata/13_intro_trends/244_mydata/)
**다음**: [데이터바우처 사업 (Data Voucher Program)](/studynote/16_bigdata/13_intro_trends/246_data_voucher/) ->

---
