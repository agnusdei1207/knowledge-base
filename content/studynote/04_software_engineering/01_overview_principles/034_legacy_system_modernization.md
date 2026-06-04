+++
title = "레거시 시스템 현대화 (Legacy System Modernization)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

> **핵심 인사이트 3줄**
> 1. 레거시 시스템 현대화(Legacy System Modernization)는 기존 시스템을 단순 교체가 아닌 비즈니스 연속성을 유지하면서 점진적으로 전환하는 복잡한 아키텍처 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. [Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/) 패턴은 레거시를 점진적으로 대체하는 가장 안전한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로, 신규 마이크로서비스가 레거시 기능을 하나씩 감싸며 결국 전체를 대체한다.
> 3. 현대화 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 계산 시 직접 비용(개발)뿐 아니라 레거시 유지 비용([기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 이자), 비즈니스 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)(EOL 지원 종료), 운영 병목(배포 속도 저하)을 모두 포함해야 한다.

---

## Ⅰ. 레거시 시스템의 정의와 문제점

레거시 시스템(Legacy System)은 <strong>현재 비즈니스에서 여전히 중요하게 사용되지만 기술적으로 노후화된 시스템</strong>이다.

### 레거시 특성 진단 기준 (Lehman's Laws)

| 특성             | 증상                               |
|---------------|----------------------------------|
| [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 누적  | 수정할 때마다 버그 증가, 테스트 없음 |
| 문서 부재       | 원작자 없이 코드 이해 불가           |
| 언어/플랫폼 노후 | COBOL, VB6, EOL [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)         |
| 강한 결합       | 하나 수정 시 전체 재배포 필요        |
| 확장 불가       | 클라우드/[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통합 불가              |

📢 **섹션 요약 비유**: 레거시 시스템은 오래된 낡은 수도관이다 — 지금도 물(비즈니스)은 흐르지만, 수리할 때마다 다른 곳이 터지고 교체 비용이 계속 늘어난다.

---

## Ⅱ. 현대화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 6R

```
6R 전략 (Cloud Migration + Modernization):

Retain    -> 현상 유지 (수명 연장, 일정 기간 유지)
Retire    -> 폐기 (사용하지 않는 시스템 제거)
Rehost    -> 리호스팅 "Lift & Shift" (코드 변경 없이 클라우드 이전)
Replatform-> 리플랫폼 (최소 변경, 클라우드 최적화)
Refactor  -> 리팩터 (아키텍처 재설계, MSA 전환)
Replace   -> 교체 (SaaS·COTS 제품으로 대체)
```

### [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택 기준

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)        | 비용  | 위험  | 비즈니스 혜택 | 권장 상황              |
|-----------|-----|-----|-----------|----------------------|
| Rehost    | 낮음 | 낮음 | 낮음       | 빠른 클라우드 이전    |
| Replatform| 중간 | 중간 | 중간       | 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 활용    |
| [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)  | 높음 | 높음 | 높음       | 민첩성·확장성 필요    |
| Replace   | 중간 | 중간 | 중간       | 핵심 아닌 기능       |

📢 **섹션 요약 비유**: 6R은 오래된 집 처리 방법이다 — 그냥 살기(Retain), 철거(Retire), 이사(Rehost), 리모델링(Replatform), 신축([Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)), 아파트 구매(Replace).

---

## Ⅲ. [Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/) 패턴

Martin Fowler가 제안한 <strong>점진적 레거시 교체 패턴</strong>이다.

```
Strangler Fig 전환 단계:

1단계: 새 API 게이트웨이/프록시 앞에 배치
   [클라이언트] -> [API Gateway] -> [레거시 모놀리스]

2단계: 기능을 하나씩 새 MSA로 이관
   [클라이언트] -> [API Gateway] -> [신규 MSA 1 (주문)]
                              -> [레거시 (나머지)]

3단계: 레거시가 완전히 대체됨
   [클라이언트] -> [API Gateway] -> [MSA 1, 2, 3, ...]
   (레거시 종료)
```

**장점**: 무중단 전환, [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 단계별 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 용이

📢 **섹션 요약 비유**: Strangler Fig는 담쟁이덩굴이다 — 낡은 나무(레거시)를 감싸며 자라다가 결국 나무가 죽으면 덩굴(신규 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))만 남는다.

---

## Ⅳ. 현대화 성공 지표 ([KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/))

| 지표              | Before          | After (목표)      |
|-----------------|-----------------|-----------------|
| 배포 빈도         | 분기 1회        | 주 1회+          |
| [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)         | 6개월           | 2주              |
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)              | 24시간          | 1시간 이내       |
| 변경 실패율        | 20%             | 5% 이하          |
| 인프라 비용        | 고정 서버비용   | 사용량 기반 절감 |

📢 **섹션 요약 비유**: 현대화 KPI는 병원 건강검진 결과다 — 레거시는 콜레스테롤 높고 혈압 높은(배포 느리고 장애 많음) 상태, 현대화 후는 정상 수치(빠른 배포·낮은 장애)로 회복된 상태.

---

## Ⅴ. 현대화 함정과 회피 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)              | 설명                             | 회피 방법           |
|--------------------|--------------------------------|-------------------|
| Big Bang 재작성     | 전체를 한 번에 재작성           | [Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/) 사용 |
| 레거시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관 무시 | [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 변환 과소평가     | 이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴     |
| 조직 변화 무시       | 기술만 바꾸고 팀 구조는 그대로  | 역 콘웨이 기동      |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 회귀           | MSA로 [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/) 증가        | [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)·[캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) |

📢 **섹션 요약 비유**: Big Bang 재작성은 도심에서 고속도로 일괄 재공사다 — 전면 통제(시스템 중단) 후 공사하면 트래픽(업무) 마비 위험이 크고, 구간별 보수([Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/))가 훨씬 안전하다.

---

## 📌 관련 개념 맵

```
레거시 시스템 현대화
+-- 전략 프레임워크
|   +-- 6R (Retain/Retire/Rehost/Replatform/Refactor/Replace)
|   +-- 기술 부채 측정 (SQALE·SonarQube)
+-- 전환 패턴
|   +-- Strangler Fig (점진적 교체)
|   +-- Branch by Abstraction
|   +-- Event Interception
+-- KPI
|   +-- DORA 4대 지표 (배포 빈도·리드 타임·MTTR·변경 실패율)
|   +-- 비용 절감 (TCO)
+-- 연관 기술
    +-- 마이크로서비스 아키텍처
    +-- API Gateway
    +-- 역 콘웨이 기동
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              레거시 현대화 발전 흐름                             |
+--------------+--------------------+-----------------------------+
| 2004년       | Strangler Fig 제안 | Martin Fowler, MSA 전환 패턴|
| 2010년       | 클라우드 이전 붐   | AWS 6R 전략 표준화           |
| 2015년       | 마이크로서비스     | Netflix·Amazon MSA 공개      |
| 2018년       | DORA 보고서        | DevOps 현대화 지표 체계화    |
| 2020년대     | Platform Eng.      | 현대화 + 개발자 플랫폼 통합 |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
레거시 진단 -> 6R 전략 선택 -> Strangler Fig 점진 전환
    v              v                    v
기술 부채 측정  Lift&Shift/Refactor  API Gateway + MSA
    v
DORA 지표 개선 -> 비즈니스 민첩성 확보
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 레거시 시스템은 낡은 수도관이다 — 지금은 작동하지만, 고칠수록 다른 곳이 터지고 수리 비용이 계속 늘어난다.
2. Strangler Fig는 담쟁이덩굴 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다 — 새 코드가 낡은 코드를 감싸며 자라다가, 결국 낡은 코드를 완전히 대체한다.
3. Big Bang 재작성은 위험하다 — 자동차가 달리는 중에 엔진 전체를 교체하려는 것처럼, 시스템이 운영되는 중에 전부 바꾸면 사고가 난다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 34 / 973

<- **이전**: [기술 부채 (Technical Debt)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/033_technical_debt/)
**다음**: [035. PMBOK 10대 지식 영역](/knowledge-base/studynote/04_software_engineering/01_overview_principles/035_pmbok_10_knowledge_areas/) ->

---
