---
title: "032. Pest Steep Analysis"
date: "2026-03-03"
tags:
  - "studynote-enterprise-systems"
weight: 32
---
> **핵심 인사이트 3줄**
> 1. [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/)(Political·Economic·Social·Technological) 분석은 기업 외부 거시 환경을 체계적으로 스캔해 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립의 맥락을 제공하는 프레임워크다.
> 2. STEEP은 PEST에 Environmental(환경) 요인을 추가해 ESG·탄소중립 이슈를 포함하며, PESTLE은 Legal(법적) 요인을 별도로 분리한다.
> 3. PEST는 산업 분석(Porter 5 Forces)·경쟁 분석(SWOT)과 연계해 외부->산업->기업 순서로 분석 레이어를 쌓는 것이 핵심이다.

---

## Ⅰ. [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 분석의 정의와 구성 요소

[PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 분석은 Francis Aguilar(1967)가 제안한 <strong>거시환경(Macro-<a href="/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">environment</a>) 분석 도구</strong>다.

| 요인          | 핵심 변수                                    |
|-------------|---------------------------------------------|
| 정치적 (Political)  | 정부 규제·조세·무역 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·정치 안정성     |
| 경제적 (Economic)   | GDP 성장률·이자율·환율·인플레이션        |
| 사회적 (Social)     | 인구 구조·라이프스타일·문화·소비 트렌드  |
| 기술적 (Technological) | R&D 투자·기술 혁신·특허·자동화 속도   |

```
PEST 분석 프레임
+--------------+--------------+
|  Political   |  Economic    |
|  정부 규제   |  GDP·금리    |
+--------------+--------------+
|  Social      |  Technological|
|  인구·트렌드 |  AI·자동화   |
+--------------+--------------+
```

📢 **섹션 요약 비유**: [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 분석은 항해 전 기상 예보와 같다 — 바람(정치), 조류(경제), 파도(사회), 선박 기술(기술) 네 가지를 파악해야 항로를 결정할 수 있다.

---

## Ⅱ. STEEP / PESTLE 확장 모델

### STEEP 추가 요인

| 요인          | 설명                            | 현대적 중요성          |
|-------------|--------------------------------|----------------------|
| Environmental | 기후변화·탄소 규제·ESG           | 탄소 세금·RE100 강제  |
| Legal        | 노동법·공정거래법·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)보호법    | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)법        |

<strong>PESTLE = <a href="/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/">PEST</a> + Environmental + Legal</strong>

### [디지털 전환](/studynote/12_it_management/01_governance_strategy/055_digital_transformation/) 시대 추가 고려 요인

- **Ethical**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 윤리·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 편향·[알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 공정성
- **Demographic**: 고령화·MZ세대 노동력
- **International**: [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 재편·디커플링

📢 **섹션 요약 비유**: STEEP은 PEST에 환경 감시관(Green)을 추가한 것이다 — 현대 기업은 탄소발자국(환경)과 법규(법적) 없이는 사업 허가 자체가 위험해진다.

---

## Ⅲ. [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 분석 수행 방법

### 분석 프로세스

```
1단계: 환경 스캐닝 -> 주요 트렌드 수집
2단계: 요인 분류 -> P·E·S·T 매핑
3단계: 영향 평가 -> 기회/위협 분류
4단계: 우선순위화 -> 확률 × 영향 매트릭스
5단계: 전략 연계 -> SWOT 분석 외부 요인으로 활용
```

### 영향 평가 매트릭스

| 요인        | 영향도 (1-5) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) (1-5) | 종합 점수 | 기회/위협 |
|------------|------------|------------|---------|---------|
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 규제 강화 |    4      |     3      |   12    |  위협    |
| 탄소세 도입  |    3      |     4      |   12    |  위협    |
| [디지털 전환](/studynote/12_it_management/01_governance_strategy/055_digital_transformation/)  |    5      |     5      |   25    |  기회    |

📢 **섹션 요약 비유**: [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 영향 매트릭스는 보험 위험 평가와 같다 — 사고 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)과 피해 규모를 곱해 가장 주의해야 할 위험을 골라낸다.

---

## Ⅳ. PEST와 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 프레임워크 연계

```
거시환경 (PEST/STEEP)
      v 외부 기회·위협 도출
산업 구조 분석 (Porter 5 Forces)
      v 경쟁 강도·수익성 파악
기업 내부 분석 (Value Chain / VRIO)
      v 강점·약점 도출
SWOT 통합 분석
      v
전략 수립 (SO·ST·WO·WT 전략)
```

### IT 기업 [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 예시

| 요인 | 내용                          | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 시사점               |
|------|------------------------------|--------------------------|
| P   | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 규제(EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act) 강화       | 컴플라이언스 조기 대응      |
| E   | 금리 상승 -> 클라우드 비용 압박 | [FinOps](/studynote/12_it_management/05_security_compliance/344_finops/)·비용 최적화         |
| S   | MZ세대 원격근무 선호           | 리모트-퍼스트 HR [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)      |
| T   | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 도입 가속            | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 제품 차별화        |

📢 **섹션 요약 비유**: [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/)->Porter->SWOT 연계는 지도-나침반-GPS를 순서대로 쓰는 것과 같다 — 큰 지형([PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/))을 보고, 경쟁 도로(Porter)를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 현재 위치(SWOT)를 파악해야 목적지 경로가 나온다.

---

## Ⅴ. 실무 적용과 한계

### 활용 시나리오

- **신시장 진출 평가**: 해외 진출 시 현지 P·E·S·T 분석
- **M&A 실사**: 피인수 기업의 외부 환경 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 평가
- <strong><a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 계획 수립</strong>: 3~5년 로드맵에 거시 트렌드 반영
- **ESG 보고서**: Environmental 요인 위험·기회 공시

### [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 한계와 보완

| 한계          | 내용                         | 보완                    |
|-------------|------------------------------|------------------------|
| [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)    | 현시점 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)만 제공           | 시나리오 플래닝 병행      |
| 상호작용 미반영 | 요인 간 상호 영향 무시        | 시스템 다이나믹스        |
| 우선순위 부재  | 모든 요인을 동등하게 취급     | 영향도·[확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 매트릭스     |

📢 **섹션 요약 비유**: PEST는 사진 한 장과 같다 — 지금 상황은 잘 보이지만, 시간이 지나면 새로 찍어야 하고, 요인들이 서로 어떻게 영향을 주는지는 보여주지 않는다.

---

## 📌 관련 개념 맵

```
PEST / STEEP 분석
+-- 구성 요인
|   +-- P: Political (정치·규제)
|   +-- E: Economic (경제·금융)
|   +-- S: Social (사회·문화)
|   +-- T: Technological (기술·혁신)
|   +-- E: Environmental (환경·ESG) — STEEP
+-- 확장 모델
|   +-- PESTLE (Legal 추가)
|   +-- STEEPLE (Ethical 추가)
+-- 연계 프레임워크
    +-- Porter 5 Forces (산업 분석)
    +-- SWOT 분석 (외부 요인 공급)
    +-- 시나리오 플래닝
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              PEST 분석 발전 흐름                                 |
+--------------+--------------------+-----------------------------+
| 1967년       | ETPS (Aguilar)     | 환경 스캐닝 최초 체계화      |
| 1980년대     | PEST 명칭 정착     | 전략 경영 교과서 표준 도구   |
| 1990년대     | PESTLE 확장        | 법적·환경 요인 추가          |
| 2000년대     | STEEP·PESTLE 혼용  | 환경/지속가능성 이슈 부상    |
| 2010년대     | 디지털 PEST        | 플랫폼 파괴·사이버보안 추가  |
| 2020년대     | ESG STEEP          | 탄소중립·AI 윤리 요인 부각   |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
거시환경 -> PEST/STEEP -> 기회/위협 도출 -> SWOT
    v           v              v
정치·경제·사회·기술  ESG/규제    전략 방향 수립
    v
Porter 5 Forces -> 산업 경쟁 분석 -> 포지셔닝 전략
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/) 분석은 소풍 전 날씨 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이다 — 비(정치), 더위(경제), 친구들 분위기(사회), 새 운동화(기술)를 모두 체크해야 즐거운 소풍이 된다.
2. STEEP은 PEST에 환경 지킴이를 추가한 것이다 — 요즘은 탄소발자국(E)도 기업 성적표에 들어간다.
3. [PEST](/studynote/12_it_management/03_ea_isp/886_isp_environmental_analysis_pest_5forces/)->SWOT 연계는 수능 모의고사다 — 외부 환경(시험 난이도)을 분석한 뒤, 내 강점·약점과 연결해 공부 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 세운다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 32 / 482

<- **이전**: [31. 3C 분석 — 고객·경쟁자·자사 전략 삼각형](/studynote/07_enterprise_systems/01_strategy_governance/031_3c_analysis/)
**다음**: [맥킨지 7S 모델 (McKinsey 7S Model)](/studynote/07_enterprise_systems/01_strategy_governance/033_mckinsey_7s_model/) ->

---
