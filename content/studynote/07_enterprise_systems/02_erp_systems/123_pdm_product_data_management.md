---
title: "123. Pdm Product Data Management"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 123
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PDM은 CAD 도면·[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)·설계 문서 등 <strong>제품 설계 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 <a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리·접근 제어·변경 이력 추적</strong>을 수행하는 시스템으로, PLM의 핵심 하위 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이다.
> 2. **가치**: 설계팀이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버에 CAD를 저장하면 <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 충돌·권한 없는 수정·변경 이력 누락</strong>이 발생하지만, PDM은 <strong>체크인/체크아웃·리비전 관리·워크플로 승인</strong>으로 설계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장한다.
> 3. **판단 포인트**: PDM은 <strong>설계 단계에 특화</strong>되어 있고, PLM은 PDM을 포함하여 <strong>기획~폐기 전주기</strong>를 관리한다. PDM ⊂ [PLM](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    PDM 핵심 기능                                      |
+-------------------------------------------------------+
|  [Vault — 데이터 저장소]                              |
|   CAD 도면, 3D 모델, 문서 -> 버전 관리                |
|                                                       |
|  [체크인/체크아웃]                                    |
|   수정 시 체크아웃(잠금) -> 완료 후 체크인(신 버전)   |
|                                                       |
|  [BOM 관리]                                           |
|   E-BOM(설계) -> M-BOM(제조) 변환                     |
|                                                       |
|  [변경 관리]                                          |
|   ECR(요청) -> ECO(승인) -> ECN(통보)                  |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: PDM은 설계팀의 <strong>Git</strong>이다. CAD 도면을 커밋(체크인)·브랜치(리비전)·[PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)(ECO 승인)로 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PDM vs [PLM](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/)

| 비교 | PDM | [PLM](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) |
|:---|:---|:---|
| **범위** | 설계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | **전주기 (기획~폐기)** |
| **대상** | CAD·[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) | + [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·폐기 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | PLM의 하위 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | PDM을 포함 |

- **📢 섹션 요약 비유**: PDM은 도서관(설계 문서 보관·대출)이고, PLM은 출판사(기획~절판까지 전 과정 관리)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버 | PDM |
|:---|:---|:---|
| <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a></strong> | 수동 (v1, v2...) | **자동 리비전** |
| **동시 편집** | 충돌 | **체크아웃 잠금** |
| **변경 이력** | 없음 | **전체 추적** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 PDM/[PLM](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/) 솔루션
- **Siemens Teamcenter**: 글로벌 1위 [PLM](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/)/PDM.
- **PTC Windchill**: CAD 연동 강점.
- **Dassault ENOVIA**: 3DEXPERIENCE 플랫폼.

---

## Ⅴ. 기대효과 및 결론

PDM은 <strong>설계 협업의 기본 인프라</strong>이며, PLM으로 확장하여 전주기 관리, 나아가 [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **PDM** | 설계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·[변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/) |
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/">PLM</a></strong> | PDM의 상위 개념 (전주기) |
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/">BOM</a></strong> | PDM이 관리하는 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **체크인/체크아웃** | PDM의 동시 편집 방지 |
| **ECO** | 설계 변경 승인 워크플로 |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 서버 (수동 CAD 관리, 1980s)]
    |
    v
[PDM (1990s) — CAD 버전·BOM 관리]
    |
    v
[PLM (2000s) — 전주기 확장]
    |
    v
[클라우드 PLM (2015~) — SaaS 기반]
    |
    v
[현재: AI+PDM — 자동 BOM 생성·도면 유사 검색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. PDM은 설계팀의 <strong>도서관</strong>이에요. 도면(책)을 빌리고(체크아웃) 돌려놓아요(체크인).
2. 같은 도면을 두 사람이 동시에 수정하면 <strong>충돌</strong>이 나니까, 한 명이 빌리면 다른 사람은 기다려야 해요.
3. 덕분에 도면이 <strong>항상 최신 <a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a>으로 안전하게</strong> 관리된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 482

<- **이전**: [122. PLM (Product Lifecycle Management) - 제품 전주기 관리 시스템](/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/)
**다음**: [124. BOM (Bill of Materials) - 부품 구성 목록·제조업 데이터 핵심](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) ->

---
