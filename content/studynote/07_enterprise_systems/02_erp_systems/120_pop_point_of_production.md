---
title: "Pop Point Of Production"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 120
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: POP(Point of Production)는 <strong>생산 현장의 각 공정·설비에서 실적 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(생산량·불량·가동시간)를 실시간으로 수집</strong>하여 [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)·ERP에 전달하는 현장 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 시스템이다.
> 2. **가치**: POP 없이는 생산 실적이 <strong>종이·수기 입력</strong>에 의존하여 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·오류가 발생하지만, POP은 바코드·RFID·센서로 <strong>자동 수집</strong>하여 실시간 생산 가시성을 확보한다.
> 3. **판단 포인트**: POP은 MES의 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 수집 계층</strong>이며, POP->[MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)->[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 순서로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 상향 전달되어 경영 의사결정에 활용된다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    POP 데이터 흐름                                    |
+-------------------------------------------------------+
|  [현장] 바코드 스캔 / RFID / 센서                     |
|     |                                                 |
|     v                                                 |
|  [POP 단말] 실적 데이터 자동 수집                     |
|     |                                                 |
|     v                                                 |
|  [MES] 생산 실행 관리 (일정·품질·추적)                |
|     |                                                 |
|     v                                                 |
|  [ERP] 경영 계획 반영 (재고·원가·납기)                |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: POP은 공장 CCTV이다. 각 라인에서 무슨 일이 일어나는지 실시간으로 기록하여 관리자([MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/))에게 보고한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### POP 수집 방식

| 방식 | 설명 | 장점 |
|:---|:---|:---|
| **바코드** | 작업 지시서·제품 바코드 스캔 | 저비용 |
| **RFID** | 비접촉 자동 인식 | 대량·자동 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 센서</strong> | 설비 상태 자동 수집 | 실시간·무인 |
| **터치 단말** | 작업자 입력 | [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) |

- **📢 섹션 요약 비유**: POP은 마트 POS(판매 시점 관리)의 공장 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다. 마트에서 바코드를 찍으면 재고가 줄듯, 공장에서 스캔하면 생산 실적이 올라간다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수기 실적 | POP |
|:---|:---|:---|
| **정확도** | 오류 빈번 | **자동 수집** |
| **실시간** | 일 단위 | **분/초 단위** |
| **분석** | 사후 | **즉시** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/)에서의 POP
- [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 -> POP -> [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) -> [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) 연동.
- [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 품질 예측 모델에 POP 실적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 피딩.

---

## Ⅴ. 기대효과 및 결론

POP은 [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)·ERP의 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 원천</strong>이며, 정확한 POP [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없이는 MES의 실시간 관리·ERP의 정확한 원가 계산이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/">MES</a></strong> | POP [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수신하는 상위 시스템 |
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> | MES를 통해 POP 실적을 경영에 반영 |
| **바코드/RFID** | POP의 핵심 수집 기술 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 센서</strong> | [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) POP의 자동 수집 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a></strong> | POP [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 구동되는 가상 공장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수기 생산 실적 관리 (종이, 1980s)]
    |
    v
[바코드 POP (1990s) — 스캔 기반 실적 수집]
    |
    v
[RFID POP (2000s) — 비접촉 자동 인식]
    |
    v
[IoT POP (2015~) — 센서 자동 수집, 실시간]
    |
    v
[현재: AI + POP — 실적 데이터 기반 예측·최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. POP은 마트의 <strong>바코드 스캐너(POS)</strong>의 공장 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이에요.
2. 제품을 만들 때마다 **바코드를 찍으면** 자동으로 "몇 개 만들었는지" 기록돼요.
3. 덕분에 공장 사장님이 <strong>실시간으로 생산 현황</strong>을 볼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 482

<- **이전**: [119. MES (Manufacturing Execution System) - 제조 실행 시스템·스마트 팩토리 핵심](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)
**다음**: [121. 스마트 팩토리 4단계 (Smart Factory Maturity Levels) - Industry 4.0 성숙도 모델](/studynote/07_enterprise_systems/02_erp_systems/121_smart_factory_4_levels/) ->

---
