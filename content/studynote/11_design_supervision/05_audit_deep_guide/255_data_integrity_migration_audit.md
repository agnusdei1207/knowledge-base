---
title: 255. 데이터 무결성 이행 감리 (Data Integrity Migration Audit)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]([[001_dikw_pyramid|Data]] [[003_integrity|Integrity]]) 이행 감리는 소스 시스템의 [[001_dikw_pyramid|데이터]]가 타겟 시스템으로 100% 정확하게 이전되었는지를 정량적으로 [[395_verification_process_review|검증]]하는 작업이다.
> 2. **가치**: 이행 오류는 배포 후 발견 시 [[090_service_kubernetes_network_load_balancing|서비스]] 중단·[[001_dikw_pyramid|데이터]] [[658_ir_recovery|복구]] 비용이 기하급수적으로 증가하므로, 이행 직전·직후 이중 [[395_verification_process_review|검증]]이 필수다.
> 3. **판단 포인트**: 건수(Count) 일치는 필요조건이지 충분조건이 아니다. 핵심 필드 합계값(Sum), 분포(Distribution), NULL 비율, [[075_referential_integrity_foreign_key_cascade|참조 무결성]]([[075_referential_integrity_foreign_key_cascade|Referential Integrity]]) 모두를 체크해야 한다.

---

## Ⅰ. 개요 및 필요성
[[001_dikw_pyramid|데이터]] 이행([[001_dikw_pyramid|Data]] Migration)은 시스템 전환 시 소스(Source) DB에서 타겟(Target) DB로 [[001_dikw_pyramid|데이터]]를 옮기는 과정이다. 이행 오류는 금융 계좌 잔액 불일치, 행정 기록 손실, 의료 진료 [[001_dikw_pyramid|데이터]] 누락 등 심각한 결과를 초래한다. 공공정보화 감리에서는 이행 완료 후 반드시 [[003_integrity|무결성]] [[395_verification_process_review|검증]] 결과를 증빙으로 제출받는다.

| [[003_integrity|무결성]] 유형 | 정의 | [[396_validation|확인]] 방법 |
|:---|:---|:---|
| [[074_entity_integrity_primary_key|개체 무결성]] ([[074_entity_integrity_primary_key|Entity Integrity]]) | PK(Primary [[067_db_key_uniqueness_minimality|Key]])는 NULL·중복 불가 | PK NULL/중복 건수 [[298_qkv_attention|쿼리]] |
| [[075_referential_integrity_foreign_key_cascade|참조 무결성]] ([[075_referential_integrity_foreign_key_cascade|Referential Integrity]]) | FK(Foreign [[067_db_key_uniqueness_minimality|Key]])는 부모 레코드 반드시 존재 | 고아(Orphan) 레코드 건수 |
| [[076_domain_integrity|도메인 무결성]] ([[076_domain_integrity|Domain Integrity]]) | 컬럼 값이 허용 범위 내 | 범위 외 값 건수 |
| [[077_user_defined_integrity_check_trigger|사용자 정의 무결성]] | 비즈니스 규칙 만족 | 업무 로직 기반 [[395_verification_process_review|검증]] [[298_qkv_attention|쿼리]] |

- **이행 전(Before)**: 소스 [[001_dikw_pyramid|데이터]] 품질 [[025_baseline|기준선]]([[025_baseline|Baseline]]) 측정
- **이행 중(During)**: 실시간 오류 [[568_logs_distributed_logging_elk_fluentd|로그]] 모니터링
- **이행 후(After)**: 소스-타겟 비교 [[395_verification_process_review|검증]] (100% 일치 목표)

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Problem      │──▶│ Core Idea    │──▶│ Expected Gain │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 이행 감리는 "이삿짐 센터가 물건을 다 옮겼다고 했을 때, 목록을 보고 하나씩 [[396_validation|확인]]하는 것"이다. 트럭이 두 번 다녀간다고 해서 모든 물건이 도착했다고 볼 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
┌─────────────────────────────────────────────────────────────┐
│              데이터 이행 무결성 검증 파이프라인               │
│                                                             │
│  ┌──────────────┐   ETL   ┌──────────────┐                  │
│  │  소스 DB      │ ──────► │  타겟 DB      │                  │
│  │  (Source)    │         │  (Target)    │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
│         │                        │                         │
│         ▼                        ▼                         │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │ 소스 체크섬   │         │ 타겟 체크섬   │                  │
│  │ Count: 1,200 │         │ Count: 1,200 │                  │
│  │ Sum(금액):   │         │ Sum(금액):   │                  │
│  │  98,450,000  │         │  98,450,000  │ ← 일치 ✅         │
│  │ NULL비율: 0% │         │ NULL비율: 0% │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
│         │                        │                         │
│         └──────────┬─────────────┘                         │
│                    ▼                                        │
│           ┌──────────────────┐                              │
│           │  비교 결과 보고서  │                              │
│           │  (Reconciliation)│                              │
│           └──────────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 소스 DB 기준선 측정
SELECT
    COUNT(*)        AS total_count,
    SUM(amount)     AS total_amount,
    MIN(created_at) AS min_date,
    MAX(created_at) AS max_date,
    COUNT(CASE WHEN cust_id IS NULL THEN 1 END) AS null_cust_count
FROM source_orders
WHERE year = 2025;

-- 타겟 DB 동일 쿼리 실행 후 결과 비교
-- 모든 항목 100% 일치 여부 확인
```

```
┌─────────────────────────────────────────────────────────────┐
│           이행 오류 유형 및 감지 방법                         │
│                                                             │
│  ① 누락 (Missing)                                           │
│     SELECT s.id FROM source s                               │
│     LEFT JOIN target t ON s.id = t.id                       │
│     WHERE t.id IS NULL;  ← 타겟에 없는 소스 레코드           │
│                                                             │
│  ② 중복 (Duplicate)                                         │
│     SELECT id, COUNT(*) FROM target                         │
│     GROUP BY id HAVING COUNT(*) > 1;                        │
│                                                             │
│  ③ 값 불일치 (Value Mismatch)                               │
│     SELECT s.id, s.amount, t.amount                         │
│     FROM source s JOIN target t ON s.id = t.id              │
│     WHERE s.amount <> t.amount;                             │
│                                                             │
│  ④ 참조 무결성 위반 (Orphan Record)                         │
│     SELECT o.id FROM orders o                               │
│     LEFT JOIN customers c ON o.cust_id = c.id               │
│     WHERE c.id IS NULL;  ← 고아 주문 레코드                  │
└─────────────────────────────────────────────────────────────┘
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [[395_verification_process_review|검증]] 포인트 | 테스트·[[568_logs_distributed_logging_elk_fluentd|로그]]·모니터링으로 [[396_validation|확인]]할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 이행 [[395_verification_process_review|검증]] [[298_qkv_attention|쿼리]]는 "이삿짐 목록과 실제 물건을 하나씩 체크박스로 [[396_validation|확인]]"하는 것이다. 이름만 맞는지가 아니라 내용물(금액, 날짜, [[083_relationship_in_er_model|관계]])까지 전부 비교한다.

---

## Ⅲ. 비교 및 연결
| [[395_verification_process_review|검증]] 방법 | 탐지 가능 오류 | 소요 시간 | 권장 시점 |
|:---|:---|:---|:---|
| 건수(Count) 비교 | 누락, 중복 | 빠름 (초 단위) | 필수 기본 [[395_verification_process_review|검증]] |
| 합계(Sum/Hash) 비교 | 값 변경, 누락 | 빠름 | 필수 기본 [[395_verification_process_review|검증]] |
| 전수 행(Row) 비교 | 모든 오류 | 느림 (시간~일) | 중요 테이블 대상 |
| 샘플링([[056_표본화_Sampling|Sampling]]) [[395_verification_process_review|검증]] | 통계적 추정 | 중간 | 대용량 테이블 |
| 비즈니스 로직 [[395_verification_process_review|검증]] | 업무 규칙 위반 | 중간~느림 | 핵심 업무 테이블 |

| 이행 [[268_strategy_pattern|전략]] | 특징 | [[003_integrity|무결성]] 위험 | 감리 포인트 |
|:---|:---|:---|:---|
| 빅뱅(Big Bang) | 일괄 전환 | 높음 | [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[313_rollback|Rollback]]) 계획 필수 |
| 단계적(Phased) | 모듈별 순차 전환 | 중간 | 구 시스템과의 [[212_synchronization_mechanisms|동기화]] |
| 병행 운영(Parallel) | 구·신 동시 운영 | 낮음 | 양쪽 [[001_dikw_pyramid|데이터]] 일치성 |
| 실시간 [[212_synchronization_mechanisms|동기화]]([[217_cdc_binlog_change_capture_debezium|CDC]]) | [[217_cdc_binlog_change_capture_debezium|Change Data Capture]] | 낮음 | [[015_지연_데이터_관점|지연]](Lag) 모니터링 |

- **📢 섹션 요약 비유**: 빅뱅 이행은 "이사하는 날 모든 물건을 한 번에 옮기는 것"으로, 빠르지만 분실 위험이 크다. 단계적 이행은 "방 하나씩 옮기는 것"으로 느리지만 추적이 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단
| 점검 항목 | 판정 기준 | 증빙 자료 |
|:---|:---|:---|
| 소스·타겟 건수 일치 | 100% 일치 | 테이블별 Count 비교표 |
| 핵심 필드 합계 일치 | 100% 일치 (금액, 수량 등) | Sum 비교 [[298_qkv_attention|쿼리]] 결과 |
| NULL/공백 비율 | 소스 기준 동일 비율 | NULL 통계 비교표 |
| PK 중복 없음 | 0건 | 중복 검사 [[298_qkv_attention|쿼리]] 결과 |
| FK [[075_referential_integrity_foreign_key_cascade|참조 무결성]] | 고아 레코드 0건 | Orphan 검사 결과 |
| 이행 [[568_logs_distributed_logging_elk_fluentd|로그]] 보존 | 전체 이행 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] | [[215_etl_vs_elt_pipeline|ETL]] 도구 [[568_logs_distributed_logging_elk_fluentd|로그]] |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] 테스트 완료 | 이행 실패 시 [[658_ir_recovery|복구]] 절차 [[395_verification_process_review|검증]] | [[098_rollback_strategy_pipeline_error_threshold|롤백]] 테스트 결과서 |

- **체크포인트(Checkpoint)**: 이행 중 장애 시 전체 재시작 방지를 위한 중간 저장 지점 [[009_config|설정]]
- **이행 윈도우(Migration Window)**: 업무 영향을 최소화하는 이행 시간대(새벽 2~6시) 선정
- **[[430_index_fast_full_scan|병렬]] 처리(Parallel [[215_etl_vs_elt_pipeline|ETL]])**: 대용량 테이블 분할 [[430_index_fast_full_scan|병렬]] 이행 시 순서 의존성 고려

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·[[568_logs_distributed_logging_elk_fluentd|로그]]가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: 체크포인트는 "게임 세이브 포인트"다. 보스 몬스터(이행 오류)를 만나도 처음부터 다시 시작하지 않고 저장된 지점부터 재개한다.

---

## Ⅴ. 기대효과 및 결론
체계적인 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 이행 감리는 시스템 전환 후 [[001_dikw_pyramid|데이터]] 불일치로 인한 [[090_service_kubernetes_network_load_balancing|서비스]] 장애와 업무 혼란을 사전에 방지한다. 이행 완료 후 문제 발견 시 정정 비용은 이행 전 발견 대비 10배 이상이며, 공공서비스의 경우 민원 폭증과 법적 책임으로 이어진다. 전수 [[395_verification_process_review|검증]]이 어려운 대용량 시스템에서는 통계적 샘플링과 핵심 필드 합계 [[395_verification_process_review|검증]]을 조합하여 [[395_verification_process_review|검증]] 커버리지를 극대화해야 한다.

확장 방향은 ① [[164_policy|Policy]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]], ② Continuous [[363_audit|Audit]], ③ [[231_ai_turing_test|인공지능]]([[190_ai_llm_requirements_specification|AI]], [[001_artificial_intelligence|Artificial Intelligence]]) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: 이행 감리 없이 [[001_dikw_pyramid|데이터]]를 이전하는 것은 "눈을 감고 이삿짐을 나르는 것"이다. 다 옮겼다고 생각했지만 중요한 서류 한 장이 누락되어 계약 전체가 무효화될 수 있다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 시스템 전환 감리 | 이행 감리의 상위 범주 |
| 상위 개념 | [[001_dikw_pyramid|데이터]] 품질 관리 (DQM) | 이행 전 소스 [[001_dikw_pyramid|데이터]] 품질 기준 |
| 하위 개념 | [[215_etl_vs_elt_pipeline|ETL]] ([[033_etl|Extract Transform Load]]) | 이행 도구 및 프로세스 |
| 하위 개념 | [[112_checksum|체크섬]] ([[112_checksum|Checksum]]) | [[001_dikw_pyramid|데이터]] 일치 여부 수치 비교 |
| 하위 개념 | [[075_referential_integrity_foreign_key_cascade|참조 무결성]] ([[075_referential_integrity_foreign_key_cascade|Referential Integrity]]) | FK 고아 레코드 감지 |
| 연관 개념 | [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | 실시간 이행 [[212_synchronization_mechanisms|동기화]] 기술 |
| 연관 개념 | [[098_rollback_strategy_pipeline_error_threshold|롤백]] 계획 ([[313_rollback|Rollback]] Plan) | 이행 실패 시 [[658_ir_recovery|복구]] 절차 |

### 📈 관련 키워드 및 발전 흐름도
[[001_dikw_pyramid|데이터]] 매핑 → [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 이행 감리 → [[395_verification_process_review|검증]]·[[098_rollback_strategy_pipeline_error_threshold|롤백]] 체계

### 👶 어린이를 위한 3줄 비유 설명
1. [[001_dikw_pyramid|데이터]] 이행 감리는 이사 후 새 집에서 "가져온 물건 목록을 보고 하나씩 체크하는 것"이야.
2. 건수만 맞는 게 아니라 "가방 안에 진짜 노트북이 들어있는지, 아니면 벽돌이 들어있는지"도 [[396_validation|확인]]해야 해.
3. 만약 이사 도중 물건이 사라지면 되돌아가서 다시 가져올 수 있도록 "세이브 포인트(체크포인트)"를 중간에 찍어두는 거야.
