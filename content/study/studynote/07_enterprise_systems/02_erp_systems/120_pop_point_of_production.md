---
title: 120. POP (Point of Production) - 생산 현장 실적 수집 시스템
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: POP(Point of Production)는 **생산 현장의 각 공정·설비에서 실적 [[001_dikw_pyramid|데이터]](생산량·불량·가동시간)를 실시간으로 수집**하여 [[119_mes_manufacturing_execution_system|MES]]·ERP에 전달하는 현장 [[001_dikw_pyramid|데이터]] 수집 시스템이다.
> 2. **가치**: POP 없이는 생산 실적이 **종이·수기 입력**에 의존하여 [[015_지연_데이터_관점|지연]]·오류가 발생하지만, POP은 바코드·RFID·센서로 **자동 수집**하여 실시간 생산 가시성을 확보한다.
> 3. **판단 포인트**: POP은 MES의 **[[001_dikw_pyramid|데이터]] 수집 계층**이며, POP→[[119_mes_manufacturing_execution_system|MES]]→[[081_erp_enterprise_resource_planning|ERP]] 순서로 [[001_dikw_pyramid|데이터]]가 상향 전달되어 경영 의사결정에 활용된다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    POP 데이터 흐름                                    │
├───────────────────────────────────────────────────────┤
│  [현장] 바코드 스캔 / RFID / 센서                     │
│     │                                                 │
│     ▼                                                 │
│  [POP 단말] 실적 데이터 자동 수집                     │
│     │                                                 │
│     ▼                                                 │
│  [MES] 생산 실행 관리 (일정·품질·추적)                │
│     │                                                 │
│     ▼                                                 │
│  [ERP] 경영 계획 반영 (재고·원가·납기)                │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: POP은 공장 CCTV이다. 각 라인에서 무슨 일이 일어나는지 실시간으로 기록하여 관리자([[119_mes_manufacturing_execution_system|MES]])에게 보고한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### POP 수집 방식

| 방식 | 설명 | 장점 |
|:---|:---|:---|
| **바코드** | 작업 지시서·제품 바코드 스캔 | 저비용 |
| **RFID** | 비접촉 자동 인식 | 대량·자동 |
| **[[101_iot_concept|IoT]] 센서** | 설비 상태 자동 수집 | 실시간·무인 |
| **터치 단말** | 작업자 입력 | [[004_unstructured_data|비정형 데이터]] |

- **📢 섹션 요약 비유**: POP은 마트 POS(판매 시점 관리)의 공장 [[288_version_ihl_tos_total_length|버전]]이다. 마트에서 바코드를 찍으면 재고가 줄듯, 공장에서 스캔하면 생산 실적이 올라간다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수기 실적 | POP |
|:---|:---|:---|
| **정확도** | 오류 빈번 | **자동 수집** |
| **실시간** | 일 단위 | **분/초 단위** |
| **분석** | 사후 | **즉시** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[166_smart_factory|스마트 팩토리]]에서의 POP
- [[101_iot_concept|IoT]] 센서 → POP → [[119_mes_manufacturing_execution_system|MES]] → [[126_digital_twin_concept|디지털 트윈]] 연동.
- [[190_ai_llm_requirements_specification|AI]] 품질 예측 모델에 POP 실적 [[001_dikw_pyramid|데이터]] 피딩.

---

## Ⅴ. 기대효과 및 결론

POP은 [[119_mes_manufacturing_execution_system|MES]]·ERP의 **[[001_dikw_pyramid|데이터]] 원천**이며, 정확한 POP [[001_dikw_pyramid|데이터]] 없이는 MES의 실시간 관리·ERP의 정확한 원가 계산이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[119_mes_manufacturing_execution_system|MES]]** | POP [[001_dikw_pyramid|데이터]]를 수신하는 상위 시스템 |
| **[[081_erp_enterprise_resource_planning|ERP]]** | MES를 통해 POP 실적을 경영에 반영 |
| **바코드/RFID** | POP의 핵심 수집 기술 |
| **[[101_iot_concept|IoT]] 센서** | [[166_smart_factory|스마트 팩토리]] POP의 자동 수집 |
| **[[126_digital_twin_concept|디지털 트윈]]** | POP [[001_dikw_pyramid|데이터]]로 구동되는 가상 공장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수기 생산 실적 관리 (종이, 1980s)]
    │
    ▼
[바코드 POP (1990s) — 스캔 기반 실적 수집]
    │
    ▼
[RFID POP (2000s) — 비접촉 자동 인식]
    │
    ▼
[IoT POP (2015~) — 센서 자동 수집, 실시간]
    │
    ▼
[현재: AI + POP — 실적 데이터 기반 예측·최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. POP은 마트의 **바코드 스캐너(POS)**의 공장 [[288_version_ihl_tos_total_length|버전]]이에요.
2. 제품을 만들 때마다 **바코드를 찍으면** 자동으로 "몇 개 만들었는지" 기록돼요.
3. 덕분에 공장 사장님이 **실시간으로 생산 현황**을 볼 수 있답니다!