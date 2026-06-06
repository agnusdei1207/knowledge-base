---
title: "Five Forces Model"
date: "2026-04-29"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파이브 포스 모델([Five Forces](/studynote/12_it_management/01_governance_strategy/023_five_forces/) Model)은 마이클 포터(Michael E. Porter)가 1979년 제시한 산업 구조 분석 프레임워크로, 신규 진입자 위협·공급자 교섭력·구매자 교섭력·대체재 위협·기존 경쟁자 간 경쟁이라는 5가지 힘이 산업의 수익성(Profitability)을 결정한다는 이론이다.
> 2. **가치**: IT 기업의 경쟁 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립 시 포터의 5 Forces로 산업 매력도를 정량·정성 평가하면, 진입 장벽(Entry Barrier)을 높이거나 교섭력을 강화할 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 포지셔닝(Strategic Positioning) 방향을 도출할 수 있다.
> 3. **판단 포인트**: 디지털 플랫폼 경제에서는 [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/)([Network Effect](/studynote/12_it_management/01_governance_strategy/824_network_effect/))가 기존 경쟁자 간 경쟁의 패턴을 바꾸고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 독점이 새로운 진입 장벽이 되며, 플랫폼 자체가 공급자·구매자 양면을 지배하는 방식으로 5 Forces 분석이 재해석되고 있다.

---

## Ⅰ. 개요 및 필요성

파이브 포스 모델([Five Forces](/studynote/12_it_management/01_governance_strategy/023_five_forces/) Model)은 하버드 경영대학원 마이클 포터 교수가 제시한 산업 경쟁 분석 도구로, 기업의 수익성은 내부 역량만이 아니라 5가지 외부 경쟁 세력의 구조적 압력에 의해 결정된다는 것을 체계화한 모델이다.

SWOT 분석이 내부·외부를 단편적으로 나열하는 것과 달리, 파이브 포스는 산업의 구조적 수익성을 체계적으로 진단하여 "어느 산업에 진입할 것인가" 또는 "현재 산업에서 어떻게 포지셔닝할 것인가"의 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 의사결정을 지원한다. IT [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 기획 및 디지털 비즈니스 포트폴리오 결정에서 필수 분석 도구다.

```text
+--------------------------------------------------------------+
|               포터의 5 Forces 구조                            |
+--------------------------------------------------------------+
|                                                              |
|              [신규 진입자 위협]                                |
|                    | v                                       |
|  [공급자 교섭력] ---> [기존 경쟁자 간 경쟁] <--- [구매자 교섭력]  |
|                    | ^                                       |
|              [대체재 위협]                                    |
|                                                              |
|  5가지 힘이 강할수록 -> 산업 수익성 낮음                        |
|  5가지 힘이 약할수록 -> 산업 수익성 높음                        |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 파이브 포스는 식당을 열기 전 동네 분위기를 파악하는 것과 같다. 경쟁 식당이 많은지(기존 경쟁), 새 식당이 쉽게 들어오는지(신규 진입), 손님들이 대체 음식을 선호하는지(대체재), 재료 공급업체가 갑질하는지(공급자), 손님들이 가격 흥정을 심하게 하는지(구매자)를 한꺼번에 분석한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 5가지 경쟁 세력 상세 분석

| 경쟁 세력 | 강화 요인 | IT 산업 적용 예시 |
|:---|:---|:---|
| **신규 진입자 위협** | 낮은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자, 규제 완화 | 클라우드 덕분에 스타트업이 대기업 IT 시장 진입 용이 |
| **공급자 교섭력** | 공급자 집중, 대체 공급처 없음 | AWS/Azure/GCP 3사 독점 -> [CSP](/studynote/09_security/05_web_app_security/475_csp/) 교섭력 높음 |
| **구매자 교섭력** | 구매자 집중, 전환 비용 낮음 | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 구독 취소 용이 -> 구매자 교섭력 높음 |
| **대체재 위협** | 대체재 가격 저렴, 기능 유사 | 특정 SW가 오픈소스로 대체됨 (예: MySQL vs [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) |
| **기존 경쟁자 경쟁** | 성장 정체, 차별화 어려움 | 스마트폰 시장 포화 -> 삼성·애플 치열한 경쟁 |

### 5 Forces 강도 매핑

```text
+----------------------------------------------------------+
|           클라우드 SaaS 산업 5 Forces 예시 평가            |
+----------------------------------------------------------+
|                                                          |
|  신규 진입자 위협   ★★★★☆  (진입 쉬움: 초기 비용 낮음)     |
|  공급자 교섭력      ★★★★☆  (AWS/Azure 의존 높음)           |
|  구매자 교섭력      ★★★☆☆  (전환 비용 중간)               |
|  대체재 위협        ★★★★☆  (오픈소스 대안 풍부)            |
|  기존 경쟁자 경쟁   ★★★★★  (Salesforce·Microsoft 치열)    |
|                                                          |
|  -> 전체 경쟁압력 높음 -> 차별화 전략 필수                    |
+----------------------------------------------------------+
```

- **�� 섹션 요약 비유**: 5 Forces 매핑은 산업의 "압력계"다. 5개 바늘이 모두 높은 쪽을 가리키면 이 산업은 돈 벌기 힘든 레드오션이고, 낮은 쪽을 가리키면 수익성이 높은 블루오션이다.

---

## Ⅲ. 비교 및 연결

| 분석 도구 | 목적 | 관점 | 한계 |
|:---|:---|:---|:---|
| **5 Forces** | 산업 구조·수익성 분석 | 외부 경쟁 환경 | 내부 역량 분석 없음 |
| **SWOT** | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 방향 도출 | 내부+외부 | 수익성 정량화 어려움 |
| **PESTEL** | [거시 환경 분석](/studynote/12_it_management/01_governance_strategy/025_pest_analysis/) | 정치·경제·사회·기술 등 | 경쟁 구조 심층 분석 부재 |
| <strong>가치사슬 (<a href="/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/">Value Chain</a>)</strong> | 내부 경쟁 우위 원천 분석 | 내부 프로세스 | 산업 구조 분석 없음 |

5 Forces는 [BSC](/studynote/12_it_management/01_governance_strategy/019_bsc/) (Balanced Scorecard, 균형 성과 지표)와 연계하여 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 목표로 폭포수처럼 전개되며, 포터의 본원적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(Generic Strategies)인 원가 우위·차별화·집중화의 선택 근거를 제공한다.

- **📢 섹션 요약 비유**: 5 Forces가 산업의 날씨 예보라면, SWOT은 여행 준비물 목록이고, PESTEL은 지구 기후 변화 분석이다. 각각 다른 스케일의 질문에 답한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: IT 기업의 신규 사업 진입 타당성 검토
중견 SI 기업이 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/)([Robotic Process Automation](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/)) 사업 진입 여부를 결정한다.

1. **신규 진입자 위협**: UiPath, Automation Anywhere 등 글로벌 전문 기업 이미 시장 점유 -> 높음.
2. **공급자 교섭력**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 의존 (OpenAI, MS Azure [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) -> 높음.
3. **구매자 교섭력**: 기업 고객의 POC(Proof of [Concept](/studynote/14_data_engineering/02_math_mining/120_concept/)) 요구 많음, 전환 비용 낮음 -> 중간.
4. **대체재 위협**: [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 에이전트가 RPA를 대체할 가능성 -> 높음.
5. **기존 경쟁자**: 삼성SDS, LG CNS 등 대형 SI 이미 진출 -> 높음.

-> **결론**: 5 Forces 모두 높음 -> 범용 [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/) 제품보다 **특정 산업(금융/제조) 수직 특화** [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 포지셔닝.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 분석 대상 산업의 경계(Industry Definition)를 명확히 정의 (너무 넓거나 좁으면 결론 왜곡).
- 각 Force의 강도(High/Medium/Low)를 정성 근거와 함께 제시.
- 디지털 산업에서 [네트워크 효과](/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/)와 플랫폼 효과를 추가 변수로 고려.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 5 Forces 분석을 1회 수행하고 수년간 재활용하는 오류. 디지털 산업은 6~12개월 만에 Force 강도가 역전될 수 있으므로 정기적(반기~연간) 재분석이 필수다.

- **📢 섹션 요약 비유**: 5 Forces 분석을 한 번만 하고 방치하는 건 5년 전 지도로 네비게이션을 쓰는 것과 같다. 새 도로(플랫폼 등장)와 폐쇄 도로(기업 퇴출)가 반영되지 않으면 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 엉뚱한 곳으로 향한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| <strong>진입 타당성 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> | 신규 사업 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 사전 평가 | 신규 사업 실패율 30% 감소 |
| <strong>경쟁 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 수립</strong> | 차별화 포인트 명확화 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 집중도 향상 |
| **투자 우선순위** | 포트폴리오 매력도 순위화 | IT 투자 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 개선 |

파이브 포스 모델은 45년이 지난 지금도 MBA [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 과목의 핵심 프레임워크로 자리를 지키고 있다. 디지털 플랫폼 시대에는 보완재(Complementors)를 6번째 Force로 추가하는 확장 모델(Value Net)이나, 에코시스템 경쟁을 반영한 Industry [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) 분석으로 진화하고 있다.

- **📢 섹션 요약 비유**: 파이브 포스는 시장에 뛰어들기 전 물의 깊이, 온도, 상어 유무, 조류 방향, 경쟁 수영선수 수를 한꺼번에 파악하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 다이빙 전 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>포터의 본원적 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | 5 Forces 분석 결과에 따른 원가 우위·차별화·집중화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택 |
| **SWOT 분석** | 5 Forces(외부)와 내부 역량을 결합한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 분석 |
| <strong>가치사슬 (<a href="/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/">Value Chain</a>)</strong> | 경쟁 우위 원천을 내부 프로세스에서 찾는 보완 분석 도구 |
| <strong>블루오션 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | 기존 5 Forces가 모두 높은 레드오션을 벗어나는 시장 재창조 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/253_network_effect_metcalfe/">네트워크 효과</a></strong> | 디지털 플랫폼에서 기존 경쟁자 간 경쟁 구조를 바꾸는 핵심 변수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[산업 조직론 (IO Theory) — 시장 구조가 성과를 결정]
    |
    v
[포터의 5 Forces (1979) — 산업 수익성 5가지 힘]
    |
    v
[본원적 전략 (Generic Strategies) — 원가우위·차별화·집중]
    |
    v
[가치사슬 (Value Chain) — 내부 경쟁 우위 원천 분석]
    |
    v
[디지털 플랫폼 확장 — 네트워크 효과·에코시스템 경쟁]
```
산업 조직론에서 5 Forces, 본원적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 가치사슬로 심화되며, 디지털 플랫폼 시대의 에코시스템 경쟁으로 확장되는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 분석의 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 파이브 포스는 새 레스토랑을 열기 전에 "우리 동네에서 장사가 잘 될까?"를 알아보는 <strong>5가지 질문</strong>이에요!
2. 경쟁 식당이 많은지, 새 식당이 쉽게 생기는지, 손님들이 다른 걸 더 좋아하는지, 재료 공급업체가 갑질하는지, 손님들이 가격 흥정을 심하게 하는지를 확인해요.
3. 5가지 모두 나쁘면 장사하기 힘든 동네, 5가지 모두 좋으면 장사하기 좋은 동네라는 걸 알 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 40 / 587

<- **이전**: [23. 5 Forces 모델](/studynote/12_it_management/01_governance_strategy/023_five_forces/)
**다음**: [24. SWOT 분석 / TOWS 매트릭스](/studynote/12_it_management/01_governance_strategy/024_swot_analysis_tows_matrix/) ->

---
