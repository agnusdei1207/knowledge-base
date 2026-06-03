+++
title = "125. C-Commerce (Collaborative Commerce) - 기업 간 협업 상거래"
date = 2026-04-19

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: C-Commerce는 <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 파트너(공급자·제조자·유통자)가 정보 시스템을 통해 실시간으로 정보·프로세스를 공유하고 협업</strong>하여 공동의 비즈니스 가치를 창출하는 전자상거래 모델이다.
> 2. **가치**: B2B·B2C가 거래 중심이라면, C-Commerce는 **설계 협업·수요 예측 공유·재고 가시화** 등 거래 이전·이후의 프로세스까지 포함하여 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 전체를 최적화한다.
> 3. **판단 포인트**: CPFR(공동 수요예측·보충)·[VMI](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/)(공급자 관리 재고)가 대표적 C-Commerce 구현이며, [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)·PLM과 연계하여 파트너 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)를 해소한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    상거래 모델 진화                                    │
├───────────────────────────────────────────────────────┤
│  B2C (기업→소비자) — 쇼핑몰                          │
│  B2B (기업→기업) — 전자 조달                         │
│  B2G (기업→정부) — 전자 입찰                         │
│  C-Commerce — 기업 간 **협업** (수요예측·설계·재고)  │
│                                                       │
│  핵심: 거래가 아닌 "정보 공유 + 프로세스 협업"       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: B2B는 물건 사고파는 것이고, C-Commerce는 <strong>같이 요리하는 것(공동 설계·수요예측)</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### C-Commerce 대표 구현

| 구현 | 설명 |
|:---|:---|
| **CPFR** | 수요예측·보충 계획 공동 수립 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/">VMI</a></strong> | 공급자가 고객 재고를 직접 관리 |
| **공동 설계** | 파트너와 CAD/[PLM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) 공유 |
| **가시화** | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 전체 재고·주문 실시간 공유 |

- **📢 섹션 요약 비유**: CPFR은 식당과 식재료 공급업체가 <strong>함께 다음 주 메뉴와 재료 양을 계획</strong>하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | B2B | C-Commerce |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | 거래 중심 | **협업 중심** |
| **정보** | 주문·송장 | **수요예측·설계·재고** |
| **가치** | 구매 효율 | <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 최적화</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 사례
- 자동차: OEM↔부품사 공동 설계 ([PLM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) 공유).
- 유통: 월마트↔P&G CPFR.
- [반도체](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/): 파운드리↔팹리스 설계 협업.

---

## Ⅴ. 기대효과 및 결론

C-Commerce는 <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 파트너 간 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/">사일로</a>를 해소</strong>하여, 수요 예측 정확도↑·재고 비용↓·출시 기간↓을 실현하는 협업 상거래 모델이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CPFR** | 공동 수요예측·보충 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/">VMI</a></strong> | 공급자 관리 재고 |
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/">SCM</a></strong> | C-Commerce의 인프라 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/">PLM</a></strong> | 공동 설계의 플랫폼 |
| **B2B** | C-Commerce의 하위 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[EDI (전자문서교환, 1990s)]
    │
    ▼
[B2B e-Marketplace (2000s)]
    │
    ▼
[C-Commerce (CPFR·VMI, 2005~)]
    │
    ▼
[디지털 공급망 (클라우드 SCM, 2015~)]
    │
    ▼
[현재: 공급망 AI — 수요예측 자동화·리스크 감지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. B2B는 물건을 **사고파는** 거예요. C-Commerce는 <strong>같이 요리(협업)</strong>하는 거예요.
2. 식당과 재료 가게가 <strong>함께 다음 주 메뉴를 계획(CPFR)</strong>하면 재료 낭비가 줄어요.
3. 덕분에 <strong>필요한 만큼만 준비</strong>하고, 손님에게 더 빨리 음식을 낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 482

← **이전**: [124. BOM (Bill of Materials) - 부품 구성 목록·제조업 데이터 핵심](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)
**다음**: [126. SCM·ERP·MES 수직 통합 - 계획→실행→현장의 데이터 연속성](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/126_scm_erp_mes_vertical_integration/) →

---
