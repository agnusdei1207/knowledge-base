+++
title = "기능점수 간이법 vs 상세법 (FP Simple vs Detailed)"
description = "기능점수(FP) 추정의 간이법과 상세법 차이, 조정 인자, COSMIC FP와의 비교를 다룬다."
date = 2025-01-01

[taxonomies]
tags = ["COSMIC", "FP", "IFPUG", "UFP", "VAF", "function point", "software estimation", "studynote-se", "간이법", "상세법"]

[extra]
tags = ["COSMIC", "FP", "IFPUG", "UFP", "VAF", "function point", "software estimation", "studynote-se", "간이법", "상세법"]
+++

> **핵심 인사이트 3줄**
> 1. [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/)([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/), [Function Point](/knowledge-base/studynote/12_it_management/04_sdlc_testing/140_function_point/))는 소프트웨어의 기능 크기를 사용자 관점에서 정량화하는 표준 규모 측정 기법으로, IFPUG가 국제 표준을 관리한다.
> 2. 간이법(Approximate [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))은 개발 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 빠른 견적에 쓰이고, 상세법(Detailed [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))은 전체 요구사항 확정 후 정확한 산정에 쓰인다.
> 3. VAF(Value Adjustment Factor) 기반 AFP = UFP × VAF로 기술 복잡도를 반영하며, COSMIC FP는 소프트웨어 이동 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 기반의 차세대 표준이다.

---

## Ⅰ. [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/) 개요

### 1.1 [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/) 구성 요소 (IFPUG 기준)

| 기능 유형 | 약어 | 설명                           |
|----------|------|-------------------------------|
| External Input     | EI  | 외부에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력           |
| External Output    | EO  | 외부로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출력             |
| External Inquiry   | EQ  | 외부 조회 (입력+출력)          |
| Internal Logical [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | ILF | 내부 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 그룹          |
| External Interface [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | EIF | 외부 인터페이스 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)       |

### 1.2 UFP 계산

UFP(Unadjusted [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) = Σ(기능 유형별 복잡도 × [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))

| 유형  | 단순(Low) | 보통(Avg) | 복잡(High) |
|-------|----------|----------|-----------|
| EI    | 3        | 4        | 6         |
| EO    | 4        | 5        | 7         |
| EQ    | 3        | 4        | 6         |
| ILF   | 7        | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)       | 15        |
| EIF   | 5        | 7        | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)        |

📢 **섹션 요약 비유**: FP는 건물 크기를 방 개수와 종류(화장실, 거실 등)로 측정하는 것 — 실제 공사법과 무관.

---

## Ⅱ. 간이법 (Approximate / Simple [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))

### 2.1 적용 시점과 방법

개발 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)(요구사항 불명확) -> 상세 분석 없이 기능 유형만 카운트.

<strong>평균 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 적용</strong>:
UFP_간이 = EI×4 + EO×5 + EQ×4 + ILF×[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) + EIF×7

### 2.2 장단점

| 항목 | 간이법        |
|------|--------------|
| 속도 | 빠름 (수 시간) |
| 정확도 | ±30~40%    |
| 필요 정보 | 기능 목록 수준 |
| 용도 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 견적, 예산 요청 |

📢 **섹션 요약 비유**: 간이법은 집 크기를 방 개수만 세는 것 — 빠르지만 방 크기가 다를 수 있어 오차가 있다.

---

## Ⅲ. 상세법 (Detailed [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))

### 3.1 VAF — 가치 조정 인자

AFP(Adjusted [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) = UFP × VAF
VAF = 0.65 + 0.01 × Σ(14개 일반 시스템 특성 × 영향도 0~5)

**14개 일반 시스템 특성(GSC)**:

| #  | 특성                   |
|----|----------------------|
| 1  | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신            |
| 2  | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리       |
| 3  | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)                   |
| 4  | 운영 형태              |
| 5  | 거래 빈도              |
| 6  | 온라인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력     |
| 7  | 최종 사용자 효율성     |
| 8  | 온라인 업데이트        |
| 9  | 복잡한 처리 로직       |
| [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 재사용성              |
| [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) | 설치 용이성           |
| 12 | 운영 용이성           |
| 13 | 다중 사이트 운영       |
| 14 | 변경 용이성           |

### 3.2 VAF 범위

- 최소: 0.65 + 0.01×0 = 0.65 (영향도 모두 0)
- 최대: 0.65 + 0.01×70 = 1.35 (영향도 모두 5)
- 즉 UFP 대비 ±35% 조정

📢 **섹션 요약 비유**: VAF는 집값에 입지, 학군, 교통 조건을 반영하는 프리미엄/디스카운트 — 기본 가격(UFP)에 ±35% 가감.

---

## Ⅳ. COSMIC [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) — 차세대 표준

### 4.1 COSMIC 함수점수의 이동 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름

COSMIC(ISO 19761)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동(Movement)을 기준으로 측정:

| 이동 유형 | 설명                        |
|-----------|-----------------------------|
| Entry (E)  | 사용자 -> 소프트웨어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 |
| Exit (X)   | 소프트웨어 -> 사용자 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출력 |
| Read (R)   | [영구 저장소](/knowledge-base/studynote/05_database/01_db_architecture_relational/059_persistent_storage_data_log_control_file/) -> 소프트웨어 읽기  |
| Write (W)  | 소프트웨어 -> [영구 저장소](/knowledge-base/studynote/05_database/01_db_architecture_relational/059_persistent_storage_data_log_control_file/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)  |

CFP(COSMIC [Function Point](/knowledge-base/studynote/12_it_management/04_sdlc_testing/140_function_point/)) = Σ(E+X+R+W) × 1 (단위: Cosmic [Function Point](/knowledge-base/studynote/12_it_management/04_sdlc_testing/140_function_point/), CFP)

### 4.2 IFPUG vs COSMIC 비교

| 항목       | IFPUG [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)          | COSMIC [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)       |
|-----------|-------------------|-----------------|
| 기준       | 기능 유형 (EI 등) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 흐름 |
| 복잡도 처리| [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 테이블      | 없음 (1:1 매핑) |
| 적합 대상  | 비즈니스 정보 시스템 | 실시간, 임베디드 |
| ISO 표준   | ISO 20926         | ISO 19761       |

📢 **섹션 요약 비유**: IFPUG는 방 종류별 점수 합산, COSMIC은 문(입구/출구)과 창고 왕복 횟수 합산.

---

## Ⅴ. [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 기반 생산성 분석

### 5.1 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 활용 지표

- 생산성 = [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) / 인월 (Person-Month)
- 비용 = 총 비용 / [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (원/[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))
- [결함 밀도](/knowledge-base/studynote/04_software_engineering/06_software_architecture/355_defect_density/) = [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수 / [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)

### 5.2 국제 벤치마크

ISBSG(International Software [Benchmarking](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/219_benchmarking_best_practice/) Standards Group) DB:
- 평균 생산성: 약 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)/PM (업종별 편차 큼)
- 한국 공공사업 기준: SW 사업 대가 기준 고시의 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 단가 적용

📢 **섹션 요약 비유**: FP로 소프트웨어를 "평수"로 환산하면 시공사(개발사)끼리 생산성 비교가 가능해진다.

---

## 📌 관련 개념 맵

```
기능점수 (FP)
+-- IFPUG 방식
|   +-- UFP (EI, EO, EQ, ILF, EIF)
|   +-- VAF (14 GSC × 영향도)
|   +-- AFP = UFP × VAF
+-- COSMIC (ISO 19761)
|   +-- E, X, R, W 데이터 이동
+-- 비교 방법론
|   +-- 간이법 (평균 가중치)
|   +-- 상세법 (복잡도 판별)
+-- 활용 지표
    +-- 생산성 (FP/PM)
    +-- 비용 (원/FP)
    +-- 결함 밀도 (결함/FP)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
LOC 기반 측정 (1960s) — 기술 종속적
     |  사용자 관점 필요
     v
Function Point — Albrecht (IBM, 1979)
     |  복잡도 조정 필요
     v
IFPUG FP (VAF, 1984 ~) — 비즈니스 정보 시스템 표준
     |  실시간/임베디드 한계
     v
COSMIC FP (ISO 19761, 2003) — 데이터 이동 기반
     |  AI/ML 크기 측정 한계
     v
SNAP (비기능 요구사항 포인트) + FP 혼용 (현재)
```

**핵심 키워드**: UFP, VAF, AFP, GSC, COSMIC, CFP, ISBSG, 생산성

---

## 👶 어린이를 위한 3줄 비유 설명

1. FP는 소프트웨어 크기를 "방 개수"로 재는 것 — 얼마나 많은 기능이 있는지 숫자로 표현해.
2. 간이법은 방 개수만 세고, 상세법은 방 크기와 위치(VAF)까지 꼼꼼히 따져.
3. COSMIC은 문이 몇 번 열리고 닫히는지 세는 것 — 문([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동) 하나하나가 작업 크기야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 50 / 973

<- **이전**: [049. 기능 점수 — Function Point (FP) Estimation](/knowledge-base/studynote/04_software_engineering/01_overview_principles/049_function_point_fp_estimation/)
**다음**: [51. 델파이 기법 (Delphi Method)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/051_delphi_method/) ->

---
