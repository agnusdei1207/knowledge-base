+++
weight = 124
title = "124. BOM (Bill of Materials) - 부품 구성 목록·제조업 데이터 핵심"
date = "2026-04-19"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BOM은 **제품을 구성하는 모든 부품·원자재·반조립품의 계층적 목록**이며, 각 부품의 수량·사양·대체품을 정의하여 설계→조달→제조→[[090_service_kubernetes_network_load_balancing|서비스]]의 기준 [[001_dikw_pyramid|데이터]] 역할을 한다.
> 2. **가치**: BOM이 부정확하면 부품 발주 오류·제조 라인 정지·완제품 불량이 발생하며, E-BOM(설계 관점)→M-BOM(제조 관점)→S-BOM([[090_service_kubernetes_network_load_balancing|서비스]] 관점) 변환이 제조업 [[001_dikw_pyramid|데이터]] 관리의 핵심이다.
> 3. **판단 포인트**: **단계 BOM(계층적, 모든 레벨)** vs **단일 수준 BOM(부모-자식 1레벨)**을 구분하고, BOM은 [[123_pdm_product_data_management|PDM]]/PLM에서 관리되어 [[081_erp_enterprise_resource_planning|ERP]]·MES에 전달된다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    BOM 계층 구조 예시 (자동차 시트)                    │
├───────────────────────────────────────────────────────┤
│  완제품: 자동차 시트 (1EA)                            │
│  ├── 프레임 어셈블리 (1EA)                            │
│  │   ├── 강철 프레임 (1EA)                            │
│  │   ├── 볼트 (8EA)                                   │
│  │   └── 용접 부품 (2EA)                              │
│  ├── 쿠션 어셈블리 (1EA)                              │
│  │   ├── 폼 패드 (1EA)                                │
│  │   └── 커버 (1EA)                                   │
│  └── 리클라이너 모터 (1EA)                            │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: BOM은 요리의 **레시피(재료 목록)**이다. 밀가루 200g, 계란 3개, 설탕 50g처럼 제품을 만드는 데 필요한 모든 부품과 수량을 정의한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### BOM 유형

| 유형 | 관점 | 용도 |
|:---|:---|:---|
| **E-BOM** | 설계 (Engineering) | 기능 구조 |
| **M-BOM** | 제조 (Manufacturing) | 조립 공정 순서 |
| **S-BOM** | [[090_service_kubernetes_network_load_balancing|서비스]] ([[090_service_kubernetes_network_load_balancing|Service]]) | 교체 부품 |

- **📢 섹션 요약 비유**: E-BOM은 건축 설계도, M-BOM은 시공 순서도, S-BOM은 수리 매뉴얼이다.

---

## Ⅲ. 비교 및 연결

| 비교 | E-BOM | M-BOM |
|:---|:---|:---|
| **관점** | 기능 (설계) | **공정 (제조)** |
| **구조** | 기능별 그룹 | **조립 순서** |
| **관리** | [[123_pdm_product_data_management|PDM]] | **[[081_erp_enterprise_resource_planning|ERP]]/[[119_mes_manufacturing_execution_system|MES]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### BOM [[002_bigdata_5v|정확성]]의 중요성
- BOM 오류 1건 → 부품 발주 오류 → 제조 [[015_지연_데이터_관점|지연]] → 납기 위반.
- 글로벌 제조사는 BOM 정확도 **99.5% 이상**을 목표.

---

## Ⅴ. 기대효과 및 결론

BOM은 **제조업 [[001_dikw_pyramid|데이터]]의 DNA**이며, [[122_plm_product_lifecycle_management|PLM]]→[[081_erp_enterprise_resource_planning|ERP]]→MES를 관통하는 Digital Thread의 핵심 [[001_dikw_pyramid|데이터]] 자산이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **E-BOM** | 설계 관점 부품 목록 |
| **M-BOM** | 제조 관점 부품 목록 |
| **[[123_pdm_product_data_management|PDM]]/[[122_plm_product_lifecycle_management|PLM]]** | BOM을 관리하는 시스템 |
| **[[082_mrp_material_requirements_planning|MRP]]** | BOM 기반 자재 소요량 계산 |
| **Digital [[092_thread_lwp|Thread]]** | BOM이 흐르는 [[001_dikw_pyramid|데이터]] 연속 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[종이 BOM (수동, ~1990s)]
    │
    ▼
[PDM BOM 관리 (전자화, 2000s)]
    │
    ▼
[PLM → ERP BOM 연동 (2010s)]
    │
    ▼
[클라우드 BOM (SaaS PLM, 2020~)]
    │
    ▼
[현재: AI BOM — 자동 부품 추천·대체품 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BOM은 요리 **레시피**예요. 밀가루·계란·설탕 등 **재료(부품)와 양(수량)**이 적혀 있어요.
2. 레시피가 틀리면 **맛없는 요리(불량 제품)**가 나오니까, 정확해야 해요.
3. 설계 레시피(E-BOM)와 조리 순서(M-BOM)가 **다를 수 있어서** 변환이 필요하답니다!
