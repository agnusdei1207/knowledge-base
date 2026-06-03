---
title: 119. MES (Manufacturing Execution System) - 제조 실행 시스템·스마트 팩토리 핵심
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MES는 **[[081_erp_enterprise_resource_planning|ERP]](경영 계획)와 [[896_plc_programmable_logic_controller|PLC]]/[[894_scada|SCADA]](설비 제어) 사이**에서 **생산 현장의 실시간 실행·[[229_monitor|모니터]]링·추적·품질 관리**를 수행하는 제조 실행 시스템이다.
> 2. **가치**: ERP가 "1000개 생산하라"는 계획을 세우면, MES가 "어떤 설비에서, 어떤 순서로, 현재 [[216_progress_in_synchronization|진행]]률은?"을 **실시간으로 관리하고 실적을 ERP에 피드백**한다.
> 3. **판단 포인트**: [[157_isa|ISA]]-95 표준이 [[081_erp_enterprise_resource_planning|ERP]]-MES-설비 계층을 정의하며, [[166_smart_factory|스마트 팩토리]](Industry 4.0)에서 MES는 **[[101_iot_concept|IoT]] 센서·[[126_digital_twin_concept|디지털 트윈]]·[[190_ai_llm_requirements_specification|AI]] 품질 예측**과 통합되어 진화하고 있다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    ISA-95 계층 구조                                   │
├───────────────────────────────────────────────────────┤
│  Level 4: ERP (경영 계획·수요 예측·재무)              │
│      ↕ 생산 계획·실적 피드백                          │
│  Level 3: MES (실행·추적·품질·일정)                   │
│      ↕ 제어 명령·센서 데이터                          │
│  Level 2: SCADA (감시·제어)                           │
│  Level 1: PLC (자동화 컨트롤러)                       │
│  Level 0: 센서·액추에이터 (현장 설비)                 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ERP는 회사 본사([[268_strategy_pattern|전략]]), MES는 공장 현장 관리자(실행), [[896_plc_programmable_logic_controller|PLC]]/SCADA는 기계 운전사(제어)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MES 11대 기능 (MESA 모델)

| 기능 | 설명 |
|:---|:---|
| **생산 일정** | 작업 순서·시간 배정 |
| **작업 지시** | 설비별 작업 명령 전달 |
| **실적 추적** | 로트·시리얼 단위 추적 |
| **품질 관리** | [[203_spc_signed_public_key_challenge|SPC]]·불량 검출 |
| **설비 관리** | 가동률·예방 정비 |

- **📢 섹션 요약 비유**: MES는 요리사(설비)에게 레시피(작업지시)를 주고, 조리 과정(실적)을 실시간 [[229_monitor|모니터]]링하며, 맛 검사(품질)까지 하는 주방 관리자다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[081_erp_enterprise_resource_planning|ERP]] | MES | [[894_scada|SCADA]] |
|:---|:---|:---|:---|
| **관점** | 경영 | **생산 현장** | 설비 |
| **주기** | 일/주/월 | **분/초 (실시간)** | ms |
| **[[001_dikw_pyramid|데이터]]** | 재무·주문 | 작업·품질·로트 | 센서 [[130_signal|신호]] |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[166_smart_factory|스마트 팩토리]]에서의 MES 진화
- **[[101_iot_concept|IoT]] 연동**: 센서 [[001_dikw_pyramid|데이터]] 실시간 수집 → MES 대시보드.
- **[[126_digital_twin_concept|디지털 트윈]]**: 생산 라인의 가상 [[016_replication_factor|복제]] → 시뮬레이션.
- **[[190_ai_llm_requirements_specification|AI]] 품질 예측**: 불량 발생 전 예측 → 예방 조치.

---

## Ⅴ. 기대효과 및 결론

| 지표 | MES 미도입 | MES 도입 | 개선 |
|:---|:---|:---|:---|
| 생산 가시성 | 사후 보고 | **실시간** | 즉시 의사결정 |
| 불량률 | 높음 | **[[203_spc_signed_public_key_challenge|SPC]]+[[190_ai_llm_requirements_specification|AI]] 예측** | 감소 |
| 납기 준수 | 불확실 | **실시간 추적** | 향상 |

MES는 [[166_smart_factory|스마트 팩토리]]의 **중추 신경계**이며, 클라우드 MES([[309_saas|SaaS]])로 전환되면서 중소기업도 접근 가능해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[081_erp_enterprise_resource_planning|ERP]]** | MES의 상위 계층 (경영 계획) |
| **[[894_scada|SCADA]]/[[896_plc_programmable_logic_controller|PLC]]** | MES의 하위 계층 (설비 제어) |
| **[[157_isa|ISA]]-95** | [[081_erp_enterprise_resource_planning|ERP]]-MES-설비 계층 표준 |
| **[[126_digital_twin_concept|디지털 트윈]]** | MES와 연동하는 가상 공장 |
| **[[166_smart_factory|스마트 팩토리]]** | MES+[[101_iot_concept|IoT]]+AI의 통합 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 생산 관리 (종이 작업지시, 1980s)]
    │
    ▼
[MES 도입 (1990s) — MESA 11대 기능 정의]
    │
    ▼
[ISA-95 표준화 (2000s) — ERP-MES 통합 인터페이스]
    │
    ▼
[스마트 팩토리 (Industry 4.0, 2015~) — IoT+MES+AI]
    │
    ▼
[현재: 클라우드 MES + 디지털 트윈 + AI 품질 예측]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ERP는 "케이크 1000개 만들어!"라고 계획하는 **사장님**이에요.
2. MES는 "오븐 1번에서 100개씩, 지금 300개 완료!"라고 **현장에서 관리하는 관리자**예요.
3. [[166_smart_factory|스마트 팩토리]]에서는 센서가 실시간으로 알려줘서 **불량이 나기 전에 미리 막을 수** 있답니다!