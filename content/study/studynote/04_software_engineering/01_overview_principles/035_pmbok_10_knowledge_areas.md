+++
title = "035. PMBOK 10대 지식 영역"
date = "2026-03-03"
[extra]
categories = "studynote-software-engineering"
+++

> **핵심 인사이트**
> 1. [[147_pmbok_10_knowledge_areas|PMBOK]] ([[042_relational_algebra_project|Project]] [[372_management|Management]] Body of Knowledge) 10대 지식 영역은 프로젝트 관리의 전 영역을 통합·범위·일정·원가·품질·자원·의사소통·위험·조달·[[173_stakeholder_identification_impact_matrix|이해관계자]]로 구조화한 국제 표준 프레임워크다.
> 2. 각 지식 영역은 착수·계획·실행·감시통제·종료의 5개 [[159_process_group|프로세스 그룹]]과 교차되어 49개 프로세스를 구성한다([[147_pmbok_10_knowledge_areas|PMBOK]] 6th).
> 3. [[055_digital_transformation|디지털 전환]] 시대에 [[004_agile_relation|애자일]] 방법론이 확산됨에 따라 [[147_pmbok_10_knowledge_areas|PMBOK]] 7th([[477_owasp_top_10_2021|2021]])는 12개 원칙과 8개 성과 영역으로 패러다임이 전환되었지만, 6th의 10대 지식 영역은 여전히 PMP 시험의 기반이다.

---

## Ⅰ. 10대 지식 영역 개요

```
프로젝트 관리 지식 영역 (PMBOK 6th)
+-- 1. 통합 (Integration)        ← 핵심 조율
+-- 2. 범위 (Scope)
+-- 3. 일정 (Schedule)
+-- 4. 원가 (Cost)
+-- 5. 품질 (Quality)
+-- 6. 자원 (Resource)
+-- 7. 의사소통 (Communications)
+-- 8. 위험 (Risk)
+-- 9. 조달 (Procurement)
+-- 10. 이해관계자 (Stakeholder)
```

| 영역         | 핵심 산출물                    | 핵심 도구         |
|-------------|-------------------------------|------------------|
| 통합         | [[232_project_charter_sponsor|프로젝트 헌장]], 프로젝트 관리 계획 | 전문가 판단      |
| 범위         | [[149_wbs_work_breakdown_structure|WBS]], 범위 [[025_baseline|기준선]]               | [[149_wbs_work_breakdown_structure|WBS]] 분해, 검사   |
| 일정         | 프로젝트 일정, [[150_cpm_critical_path_method|CPM]]             | [[123_pdm_product_data_management|PDM]], 일정 [[347_compaction|압축]]   |
| 원가         | 원가 [[025_baseline|기준선]], [[152_evm_earned_value_management|EVM]]               | 유사 산정, 모수  |
| 품질         | 품질 관리 계획, [[435_checklist_based_testing|체크리스트]]     | 파레토, 관리도   |
| 자원         | RAM, 자원 달력                 | RACI 매트릭스    |
| 의사소통     | 의사소통 관리 계획             | 커뮤니케이션 모델|
| 위험         | 위험 등록부                    | [[130_probability|확률]]·영향 매트릭스|
| 조달         | 계약서, 입찰 문서              | 공급업체 선정    |
| [[173_stakeholder_identification_impact_matrix|이해관계자]]   | [[173_stakeholder_identification_impact_matrix|이해관계자]] 등록부              | 권력/관심 그리드  |

> 📢 **섹션 요약 비유**: 집 짓기의 10가지 역할 — 건축가(통합), 설계도(범위), 공사 일정표(일정), 예산(원가), 감리(품질)...

---

## Ⅱ. 5 [[159_process_group|프로세스 그룹]] × [[489_raid_10_hybrid|10]] 지식 영역

```
프로세스 그룹
  착수   계획   실행   감시통제   종료
   |      |      |        |        |
   +------+------+---------+--------+
   |         49개 프로세스          |
   +--------------------------------+

주요 프로세스 예시:
- 착수: 프로젝트 헌장 개발, 이해관계자 식별
- 계획: WBS 작성, 일정 개발, 위험 식별
- 실행: 품질 보증 수행, 팀 개발
- 감시통제: 범위 검증, EVM 분석
- 종료: 프로젝트 또는 단계 종료
```

> 📢 **섹션 요약 비유**: 10가지 역할이 5막 연극에 각자 등장하는 것 — 모든 배우가 전막에 나오지 않고 필요한 장면에만 나온다.

---

## Ⅲ. 핵심 지식 영역 심화

### 3-1. 범위 관리 — [[149_wbs_work_breakdown_structure|WBS]] ([[149_wbs_work_breakdown_structure|Work Breakdown Structure]])

```
프로젝트
+-- 단계 1
|   +-- 작업 패키지 1.1
|   +-- 작업 패키지 1.2
+-- 단계 2
    +-- 작업 패키지 2.1
```

- **100% 규칙**: WBS는 전체 작업을 빠짐없이 포함
- **롤링 웨이브 계획**: 가까운 작업은 상세, 먼 작업은 고수준

### 3-2. 일정 관리 — [[150_cpm_critical_path_method|CPM]] ([[037_cpm|Critical Path Method]])

```
A(3일) → B(2일) → D(4일)
              ↓
         C(5일) → D
         
CPM: A→C→D = 3+5+4 = 12일 (최장 경로 = 임계 경로)
여유시간(Float): B = 12 - (3+2+4) = 3일
```

### 3-3. 원가 관리 — [[152_evm_earned_value_management|EVM]] ([[040_evm|Earned Value Management]])

| 지표  | 공식           | 의미                |
|-------|----------------|---------------------|
| [[153_pv_planned_value|PV]]    | 계획 예산      | 완료 예정 작업 가치  |
| [[154_ev_earned_value|EV]]    | 획득 가치      | 실제 완료 작업 가치  |
| [[155_ac_actual_cost|AC]]    | 실제 원가      | 실제 지출 금액       |
| [[158_cpi_cost_performance_index|CPI]]   | [[154_ev_earned_value|EV]]/[[155_ac_actual_cost|AC]]          | 원가 효율 (1=정상)  |
| [[159_spi_schedule_performance_index|SPI]]   | [[154_ev_earned_value|EV]]/[[153_pv_planned_value|PV]]          | 일정 효율 (1=정상)  |

> 📢 **섹션 요약 비유**: WBS는 집의 설계도, CPM은 공사 일정표, EVM은 실시간 가계부 — 세 가지가 함께 있어야 프로젝트가 통제된다.

---

## Ⅳ. [[147_pmbok_10_knowledge_areas|PMBOK]] 7th 변화 — 프로세스에서 원칙으로

| 구분      | [[147_pmbok_10_knowledge_areas|PMBOK]] 6th               | [[147_pmbok_10_knowledge_areas|PMBOK]] 7th              |
|-----------|-------------------------|------------------------|
| 구조      | 10개 지식 영역 + 49 프로세스 | 12개 원칙 + 8개 성과 영역 |
| 초점      | 프로세스 준수            | 가치 전달              |
| 방법론    | 예측형(Waterfall) 중심   | [[004_agile_relation|애자일]] 통합            |
| 산출물    | ITTO(입력·도구·기법·출력) | 모델·방법·공학         |

> 📢 **섹션 요약 비유**: 6th가 '요리 레시피 책'이라면, 7th는 '요리 철학 교과서' — 결과물 중심에서 가치 중심으로.

---

## Ⅴ. 실무 시나리오 — SI 프로젝트 적용

| 단계       | [[147_pmbok_10_knowledge_areas|PMBOK]] 적용 포인트                        |
|-----------|------------------------------------------|
| 착수       | [[173_stakeholder_identification_impact_matrix|이해관계자]] 분석(권력/관심 그리드), 헌장   |
| 계획       | [[149_wbs_work_breakdown_structure|WBS]] → 일정 → [[152_evm_earned_value_management|EVM]] [[025_baseline|기준선]] [[009_config|설정]]            |
| 실행       | 품질 [[606_auditing_linux_auditd|감사]], 조달 관리, 팀 빌딩            |
| 감시통제   | [[158_cpi_cost_performance_index|CPI]]/[[159_spi_schedule_performance_index|SPI]] 추적, [[080_cab|변경 통제 위원회]]([[160_change_control_board_ccb_requirements_review|CCB]])     |
| 종료       | [[659_ir_lessons_learned|교훈]] 기록, 최종 인수 [[396_validation|확인]]               |

> 📢 **섹션 요약 비유**: PMBOK은 건설 현장의 표준 공정표 — 표준을 따르면 누가 감독해도 품질이 일정하게 유지된다.

---

## 📌 관련 개념 맵

```
PMBOK 10대 지식 영역
+-- 통합: 프로젝트 헌장, 변경 통제
+-- 범위: WBS, 요구사항 수집
+-- 일정: CPM, 간트 차트, PDM
+-- 원가: EVM, 예산 책정
+-- 품질: 품질 보증/통제, 파레토
+-- 자원: RACI, 팀 개발
+-- 의사소통: 커뮤니케이션 계획
+-- 위험: 위험 등록부, 몬테카를로
+-- 조달: SOW, 계약 유형(FFP/CPFF)
+-- 이해관계자: 관여 계획, 기대 관리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 프로젝트 관리 (1960s)]
간트 차트, CPM, PERT 등장
      |
      v
[PMBOK 1st~4th (1996~2008)]
9개 지식 영역, 프로세스 중심 표준화
      |
      v
[PMBOK 5th (2012)]
10번째 지식 영역 — 이해관계자 관리 추가
      |
      v
[PMBOK 6th (2017)]
애자일 실무 가이드 별첨, 49 프로세스
      |
      v
[PMBOK 7th (2021)]
12 원칙 + 8 성과 영역 패러다임 전환
      |
      v
[현재: 애자일·하이브리드 PM]
Scrum + PMBOK 조합, SAFe 연계
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [[147_pmbok_10_knowledge_areas|PMBOK]] 10대 지식 영역은 큰 프로젝트를 잘 관리하기 위한 10가지 역할 설명서예요.
2. 일정, 비용, 품질, 위험 등 각 역할이 서로 협력해야 프로젝트가 성공해요.
3. 마치 축구팀의 포지션 역할 매뉴얼처럼, 모두가 자기 역할을 알아야 이길 수 있어요!
