---
title: 205. 프로세스 마이닝 (Process Mining)
date: '2026-05-08'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 정보시스템에 남은 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]를 이용해 실제 업무 흐름을 [[001_dikw_pyramid|데이터]]로 재구성하는 분석 기법이다.
> 2. **가치**: 인터뷰나 매뉴얼이 놓치기 쉬운 재작업, 우회 경로, 병목을 실측 [[001_dikw_pyramid|데이터]]로 드러내어 개선 우선순위를 정확히 잡게 한다.
> 3. **판단 포인트**: 좋은 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]의 출발점은 화려한 [[003_bigdata_7v|시각화]]가 아니라 Case ID, Activity, Timestamp가 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있게 수집된 [[568_logs_distributed_logging_elk_fluentd|로그]] 품질에 있다.

---

## Ⅰ. 개요 및 필요성

[[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]] ([[129_process_mining_bpr_event_log_bottleneck_analysis|Process Mining]])은 [[081_erp_enterprise_resource_planning|ERP]] ([[081_erp_enterprise_resource_planning|Enterprise Resource Planning]]), [[107_crm_customer_relationship_management|CRM]] ([[026_three_c_analysis|Customer]] [[083_relationship_in_er_model|Relationship]] [[372_management|Management]]), 그룹웨어, 티켓 시스템 등에 남은 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]를 분석해 실제 프로세스 흐름을 발견하고 평가하는 기법이다. 전통적인 프로세스 분석은 인터뷰와 워크숍에 크게 의존했기 때문에, 예외 처리나 반복 루프처럼 현장이 체감하지 못하는 흐름을 놓치기 쉬웠다. 반면 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 시스템이 남긴 흔적을 기반으로 하므로, "문서상 절차"가 아니라 "실제 수행 절차"를 드러내는 데 강하다.

이 기법이 중요해진 이유는 디지털 업무가 대부분 시스템 [[568_logs_distributed_logging_elk_fluentd|로그]]를 남기기 때문이다. 주문, 승인, 발송, 환불처럼 반복적 프로세스는 클릭과 상태 변경이 누적되므로, 이를 연결하면 실제 흐름과 [[015_지연_데이터_관점|지연]] 구간을 역으로 복원할 수 있다. [[568_logs_distributed_logging_elk_fluentd|로그]]가 풍부한 조직일수록 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 인터뷰보다 더 빠르고 정밀한 진단 도구가 된다.

- **📢 섹션 요약 비유**: [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 사람들이 길을 어떻게 갔다고 말하는 것을 믿는 대신, 휴대전화 GPS 기록을 모아 진짜 이동 경로를 그려 보는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]의 최소 입력은 Case ID, Activity, Timestamp다. Case ID는 어떤 업무 건인지, Activity는 어떤 단계가 수행되었는지, Timestamp는 그 일이 언제 일어났는지를 뜻한다. 여기에 Resource, Cost, Channel 같은 [[082_attribute_types_er_model|속성]]이 추가되면 담당자별 병목, 채널별 [[015_지연_데이터_관점|지연]], 비용 편차까지 분석할 수 있다.

| [[568_logs_distributed_logging_elk_fluentd|로그]] [[082_attribute_types_er_model|속성]] | 의미 | 왜 중요한가 |
| :--- | :--- | :--- |
| Case ID | 동일 업무 건 [[289_identification_flags_fragmentation_offset|식별자]] | 서로 다른 건의 이벤트가 섞이지 않게 함 |
| Activity | 수행된 작업 이름 | 실제 흐름과 루프를 구성함 |
| Timestamp | 발생 시각 | 대기시간, 처리시간 계산의 기준 |
| Resource | 수행 주체 | 조직별 병목과 편차 분석 |
| [[082_attribute_types_er_model|Attribute]] | 금액, 채널, 상품군 등 | 원인 분석과 세분화에 활용 |

아래 그림은 여러 시스템에서 추출한 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]가 정제 과정을 거쳐 실제 프로세스 맵과 [[282_performance_tactics|성능]] 지표로 변환되는 기본 흐름을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ERP / CRM / Ticket System Logs                                      │
│          │                                                           │
│          ▼                                                           │
│ Event Log (Case, Activity, Timestamp, Resource)                     │
│          │                                                           │
│          ▼                                                           │
│ Discovery -> Variant Analysis -> Bottleneck / Rework Insight        │
└──────────────────────────────────────────────────────────────────────┘
```

핵심 원리는 관찰된 이벤트 순서를 바탕으로 프로세스 모델을 추정하는 것이다. 이때 단순히 가장 많이 발생한 경로만 보면 예외 흐름이 사라지고, 모든 이벤트를 그대로 그리면 스파게티 맵이 된다. 그래서 필터링, 변형(Variant) 분석, 빈도·[[282_performance_tactics|성능]] 지표를 함께 사용해 "중요한 흐름"과 "문제 흐름"을 구분하는 것이 중요하다.

- **📢 섹션 요약 비유**: [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 흙 묻은 발자국을 모아서 누가 어디로 다녔는지 지도를 그리는 일과 같다. 발자국이 많을수록 진짜 길과 샛길이 함께 드러난다.

---

## Ⅲ. 비교 및 연결

[[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 일반 BI (Business Intelligence) 리포팅과 비슷해 보이지만 분석 단위가 다르다. BI가 보통 건수, 매출, [[139_throughput|처리량]] 같은 집계 결과를 보여 준다면, [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 이벤트 간 순서와 시간 차이를 기반으로 흐름 자체를 복원한다. 그래서 "승인 건수가 많다"보다 "어떤 경로를 거쳐 승인되었고 어디서 반복되었는가"를 설명하는 데 적합하다.

| 항목 | BI 대시보드 | [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]] | [[150_task|태스크]] 마이닝 |
| :--- | :--- | :--- | :--- |
| 분석 대상 | 집계 지표 | 프로세스 흐름 | 사용자 화면/행동 세부 작업 |
| [[001_dikw_pyramid|데이터]] 원천 | 요약 테이블 | 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]] | 데스크톱 활동 기록 |
| 강점 | 경영 현황 파악 | 병목·재작업·변형 분석 | 세부 작업 자동화 후보 발굴 |
| 한계 | 흐름 맥락 부족 | [[568_logs_distributed_logging_elk_fluentd|로그]] 품질 의존 | [[781_personal_information|개인정보]]·과잉 감시 이슈 |

[[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 [[206_conformance_checking_process_mining_deviation_audit|적합성 검사]], [[207_model_enhancement_process_mining_simulation|모델 향상]], [[060_rpa_hyperautomation|RPA]] ([[060_rpa_hyperautomation|Robotic Process Automation]]) 선정과도 긴밀히 이어진다. Discovery로 현재 흐름을 찾고, Conformance Checking으로 규정 위반을 [[396_validation|확인]]하며, Enhancement로 개선안을 도출하는 식이다. 따라서 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 독립 도구라기보다, 프로세스 개선 생태계의 [[001_dikw_pyramid|데이터]] 기반 진단 층으로 보는 것이 적절하다.

- **📢 섹션 요약 비유**: BI가 도시의 총 교통량 표라면, [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 차들이 실제로 어느 길에서 꼬였는지 보여 주는 도로 [[933_cctv|CCTV]] 분석이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 주문-출고, 청구-수납, 사고 접수-보상처럼 거래 건이 많고 [[568_logs_distributed_logging_elk_fluentd|로그]]가 풍부한 프로세스에서 효과가 크다. 병목 구간의 체류 시간, 반려 후 재작업 횟수, 변형별 처리 편차를 [[396_validation|확인]]하면 자동화나 조직 재배치의 우선순위를 세우기 쉽다. 특히 [[060_rpa_hyperautomation|RPA]] 후보를 찾을 때 반복 횟수와 대기시간을 동시에 볼 수 있어 투자 타당성을 높일 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[568_logs_distributed_logging_elk_fluentd|로그]]에 Case ID가 일관되게 유지되는가?
2. Activity 명이 화면 버튼명이 아니라 업무 의미를 담고 있는가?
3. 시간대, 중복 이벤트, 누락 [[568_logs_distributed_logging_elk_fluentd|로그]]를 정제했는가?
4. [[781_personal_information|개인정보]]와 민감 정보 비식별화가 되었는가?

### 회피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 스파게티 맵 자체를 결과물로 오해하고 원인 분석을 생략하는 경우
- [[568_logs_distributed_logging_elk_fluentd|로그]] 정제 없이 도구에 바로 투입해 잘못된 결론을 내리는 경우
- 병목이 조직 승인 [[164_policy|정책]] 때문인데 RPA만 투입하는 경우

- **📢 섹션 요약 비유**: [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 병원 MRI처럼 먼저 정확히 찍어 보는 단계다. 사진도 안 보고 수술부터 하면 돈도 쓰고 문제도 못 고친다.

---

## Ⅴ. 기대효과 및 결론

[[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]의 가장 큰 효과는 조직이 실제 흐름을 감이 아니라 [[001_dikw_pyramid|데이터]]로 보게 된다는 점이다. 숨어 있던 재작업, 예외 비율, 우회 경로가 드러나면 개선 논의가 구체적 행동과 수치 중심으로 바뀐다. 또한 규정 위반 탐지, 자동화 대상 선정, 성과 비교 같은 후속 활동의 기반 [[001_dikw_pyramid|데이터]]로 활용할 수 있다.

다만 [[568_logs_distributed_logging_elk_fluentd|로그]] 품질이 나쁘면 분석 결과도 왜곡된다. 시스템 간 [[289_identification_flags_fragmentation_offset|식별자]]가 맞지 않거나 타임스탬프가 불완전하면, 매우 정교한 도구를 써도 잘못된 프로세스가 그려질 수 있다. 따라서 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 "예쁜 흐름 그림"보다 "신뢰 가능한 이벤트 [[001_dikw_pyramid|데이터]]에 기반한 운영 진단"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 흐릿한 소문 지도가 아니라, 시간과 위치가 정확히 찍힌 블랙박스 기록을 보는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Discovery | 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]로 실제 프로세스 흐름을 도출하는 단계 |
| [[206_conformance_checking_process_mining_deviation_audit|Conformance Checking]] | 표준 모델과 실제 [[568_logs_distributed_logging_elk_fluentd|로그]]의 차이를 [[395_verification_process_review|검증]] |
| Variant Analysis | 서로 다른 처리 경로를 유형별로 분리해 비교 |
| [[060_rpa_hyperautomation|RPA]] ([[060_rpa_hyperautomation|Robotic Process Automation]]) | 반복적 병목 구간의 자동화 후보로 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
ERP · CRM 이벤트 축적
    │
    ▼
Event Log 정제
    │
    ▼
Discovery · Variant Analysis
    │
    ▼
Conformance Checking · Enhancement
    │
    ▼
RPA · Digital Twin of Process
```

이 흐름은 [[626_log_collection|로그 수집]]에서 시작해, 실제 프로세스 발견과 개선, 그리고 [[126_digital_twin_concept|디지털 트윈]] 기반 예측으로 이어지는 확장 경로를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 사람들이 무슨 일을 했는지 발자국처럼 기록을 남겨요.
2. [[129_process_mining_bpr_event_log_bottleneck_analysis|프로세스 마이닝]]은 그 발자국을 이어서 모두가 실제로 어떤 길로 다녔는지 찾는 거예요.
3. 그래서 어디가 막히고 어디서 돌아갔는지 금방 알 수 있어요.
