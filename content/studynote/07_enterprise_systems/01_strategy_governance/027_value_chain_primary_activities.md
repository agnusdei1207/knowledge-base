---
title: 27. 가치 사슬 본원적 활동 (Value Chain Primary Activities)
date: '2026-04-29'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이클 포터(Michael Porter)의 [[249_value_chain_competitive_analysis|가치 사슬]]([[249_value_chain_competitive_analysis|Value Chain]]) 분석에서 본원적 활동(Primary Activities)은 제품·[[090_service_kubernetes_network_load_balancing|서비스]]의 물리적 생산, 판매, 배송, 사후 [[090_service_kubernetes_network_load_balancing|서비스]]에 직접 관여하는 5가지 활동(내부 물류·운영·외부 물류·마케팅·[[090_service_kubernetes_network_load_balancing|서비스]])으로 구성된다.
> 2. **가치**: 각 본원적 활동에서 비용 우위 또는 차별화를 달성하는 것이 경쟁 우위의 원천이다. 5가지 활동 중 어느 단계에서 경쟁자보다 더 잘하거나 더 싸게 할 수 있는가가 [[268_strategy_pattern|전략]] 분석의 핵심이다.
> 3. **판단 포인트**: [[055_digital_transformation|디지털 전환]](DT) 맥락에서 [[026_value_chain_analysis|가치 사슬 분석]]은 [[190_ai_llm_requirements_specification|AI]]·클라우드·[[001_dikw_pyramid|데이터]]가 각 본원적 활동을 어떻게 강화하는가를 분석하는 틀로 활용된다. IT 투자 우선순위를 결정할 때 "어느 활동의 디지털화가 가장 큰 가치를 창출하는가"를 [[655_ir_detection_analysis|식별]]한다.

---

## Ⅰ. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────────┐
│                Porter 가치 사슬 구조                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  지원 활동:  ┌─────────────────────────────────────────┐   │
│              │ 기업 인프라 / HR / 기술 개발 / 조달      │   │
│              └─────────────────────────────────────────┘   │
│                                                            │
│  본원적 활동: [내부물류]→[운영]→[외부물류]→[마케팅]→[서비스]│
│                                        ───────────────►    │
│                                          이익 마진          │
└────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[249_value_chain_competitive_analysis|가치 사슬]]은 음식점 운영 흐름이다. 식재료 입고(내부 물류) → 요리(운영) → 서빙(외부 물류) → 홍보(마케팅) → 애프터 [[090_service_kubernetes_network_load_balancing|서비스]](고객 [[090_service_kubernetes_network_load_balancing|서비스]]). 각 단계를 잘할수록 더 많은 이익이 남는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 5가지 본원적 활동

| 활동 | 정의 | IT 디지털화 예시 |
|:---|:---|:---|
| **내부 물류** | 원재료·부품 수입, 보관, 분배 | [[097_wms_warehouse_management_system|WMS]](창고관리시스템), [[101_iot_concept|IoT]] 재고 |
| **운영** | 제품·[[090_service_kubernetes_network_load_balancing|서비스]] 생산 | [[119_mes_manufacturing_execution_system|MES]](제조실행시스템), [[190_ai_llm_requirements_specification|AI]] 품질 검사 |
| **외부 물류** | 완제품 보관·배송 | [[098_tms_transportation_management_system|TMS]](운송관리), 라스트마일 드론 |
| **마케팅·판매** | 제품 홍보, 주문 수주 | [[107_crm_customer_relationship_management|CRM]], 개인화 추천, 디지털 광고 |
| **[[090_service_kubernetes_network_load_balancing|서비스]]** | [[344_as_autonomous_system_asn|AS]], 고객 지원, 설치 | [[190_ai_llm_requirements_specification|AI]] 챗봇, 예측 정비 |

- **📢 섹션 요약 비유**: 디지털화된 [[249_value_chain_competitive_analysis|가치 사슬]]은 스마트 공장이다. 재료 입고부터 배송까지 모든 단계가 [[101_iot_concept|IoT]]·[[190_ai_llm_requirements_specification|AI]]·클라우드로 연결되어 자동화·최적화된다.

---

## Ⅲ. 비교 및 연결

| 비교 | 비용 우위 [[268_strategy_pattern|전략]] | 차별화 [[268_strategy_pattern|전략]] |
|:---|:---|:---|
| **내부 물류** | JIT로 재고 최소화 | 신속 조달로 리드타임 단축 |
| **운영** | 자동화로 생산 비용 절감 | [[091_kustomize_kubernetes_declarative_overlay_manifest|커스터마이즈]] 생산 |
| **마케팅** | [[001_dikw_pyramid|데이터]] 기반 타기팅 광고 | 브랜드 프리미엄 구축 |

- **📢 섹션 요약 비유**: 비용 우위는 더 싸게 만드는 [[268_strategy_pattern|전략]](삼성 [[009_semiconductor|반도체]] 대량 생산), 차별화는 더 특별하게 만드는 [[268_strategy_pattern|전략]](애플 디자인)이다. [[249_value_chain_competitive_analysis|가치 사슬]] 각 단계에서 어느 [[268_strategy_pattern|전략]]을 선택하느냐가 기업 [[268_strategy_pattern|전략]]을 결정한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### DT [[268_strategy_pattern|전략]] 수립에서 [[249_value_chain_competitive_analysis|가치 사슬]] 활용
1. 각 본원적 활동의 현행 수준 평가([[178_as_is_to_be_analysis|As-Is]]).
2. 디지털 기술이 어떤 활동을 강화할 수 있는가 [[655_ir_detection_analysis|식별]].
3. 경쟁사 대비 취약한 활동에 우선 투자.
4. 디지털 [[249_value_chain_competitive_analysis|가치 사슬]] 목표 상태(To-Be) 설계.

예시: 제조기업 DT 우선순위
- 운영([[119_mes_manufacturing_execution_system|MES]] + [[190_ai_llm_requirements_specification|AI]] 품질 검사) > 내부물류([[097_wms_warehouse_management_system|WMS]] [[101_iot_concept|IoT]]) > [[090_service_kubernetes_network_load_balancing|서비스]](예측 정비)

- **📢 섹션 요약 비유**: [[249_value_chain_competitive_analysis|가치 사슬]] DT 우선순위 결정은 집 수리 순서 정하기다. 지붕(운영)이 새면 먼저 고치고, 다음 창문(물류), 마지막 인테리어(마케팅) 순으로 가장 중요한 것부터 고친다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **[[268_strategy_pattern|전략]] 명확화** | 경쟁 우위 원천 활동 [[655_ir_detection_analysis|식별]] |
| **IT 투자 우선순위** | 가장 큰 가치를 창출하는 디지털화 활동 결정 |
| **[[219_benchmarking_best_practice|벤치마킹]]** | 경쟁사 대비 각 활동 역량 비교 |

AI와 [[001_dikw_pyramid|데이터]] 분석이 모든 본원적 활동에 통합되면서 [[249_value_chain_competitive_analysis|가치 사슬]]이 디지털 [[249_value_chain_competitive_analysis|가치 사슬]](Digital [[249_value_chain_competitive_analysis|Value Chain]])로 진화하고, [[033_platform_business_model|플랫폼 비즈니스 모델]]에서는 [[249_value_chain_competitive_analysis|가치 사슬]]이 가치 네트워크(Value Network)로 재편되고 있다.

- **📢 섹션 요약 비유**: 디지털 [[249_value_chain_competitive_analysis|가치 사슬]]은 스마트 고속도로다. 전통 [[249_value_chain_competitive_analysis|가치 사슬]]이 일방통행 도로라면, 디지털 [[249_value_chain_competitive_analysis|가치 사슬]]은 [[190_ai_llm_requirements_specification|AI]] [[130_signal|신호]]등·자율주행 차량이 모든 진입로를 동시에 최적화하는 지능형 교통망이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **지원 활동** | 본원적 활동을 뒷받침하는 HR·IT·조달·인프라 |
| **비용 우위** | [[249_value_chain_competitive_analysis|가치 사슬]] 활동의 비용 최소화 [[268_strategy_pattern|전략]] |
| **차별화** | [[249_value_chain_competitive_analysis|가치 사슬]] 활동의 독특한 가치 창출 [[268_strategy_pattern|전략]] |
| **3C 분석** | [[249_value_chain_competitive_analysis|가치 사슬]]과 연계하는 [[268_strategy_pattern|전략]] 분석 도구 |
| **디지털 [[249_value_chain_competitive_analysis|가치 사슬]]** | [[190_ai_llm_requirements_specification|AI]]·[[101_iot_concept|IoT]] 통합으로 자동화된 [[249_value_chain_competitive_analysis|가치 사슬]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 가치 사슬 — 5개 본원적 활동 순차 흐름]
    │
    ▼
[가치 사슬 분석 — 경쟁 우위 원천 활동 식별]
    │
    ▼
[IT 통합 — ERP/SCM/CRM으로 활동 연결]
    │
    ▼
[디지털 가치 사슬 — AI·IoT·클라우드 통합]
    │
    ▼
[가치 네트워크 — 플랫폼 기반 다방향 가치 생성]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[249_value_chain_competitive_analysis|가치 사슬]] 본원적 활동은 음식점 운영 5단계예요! 재료 입고 → 요리 → 서빙 → 홍보 → [[344_as_autonomous_system_asn|AS]] 순서예요.
2. 각 단계를 더 잘하거나 더 싸게 할수록 경쟁자를 이길 수 있어요!
3. 요즘은 [[190_ai_llm_requirements_specification|AI]]·IoT가 모든 단계를 자동화해서 더 빠르고 저렴하게 운영할 수 있는 디지털 [[249_value_chain_competitive_analysis|가치 사슬]]로 진화하고 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 27 / 482

← **이전**: [[026_value_chain_analysis|26. 가치 사슬 분석 (Value Chain Analysis) — 포터의 경쟁 우위 원천 분석]]
**다음**: [[028_value_chain_support_activities|28. 가치 사슬 지원 활동 (Value Chain Support Activities)]] →

---
