---
title: "121. Data Architecture Framework Zachman"
date: "2026-04-19"
tags:
  - "studynote-database"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Zachman](/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/) Framework는 <strong>6가지 관점(Planner·Owner·Designer·<a href="/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/">Builder</a>·Subcontractor·User) × 6가지 질문(What·How·Where·Who·When·Why)</strong>의 36셀 매트릭스로 엔터프라이즈 아키텍처를 <strong>체계적으로 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>·정리</strong>하는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍처를 설계할 때 "누구의 관점에서, 무엇을 정의하는가"를 명확히 하여, <strong>개념-><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>->물리 모델링의 각 산출물이 어디에 위치하는지</strong> 체계적으로 관리할 수 있다.
> 3. **판단 포인트**: Zachman은 <strong>방법론이 아닌 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> 체계(Taxonomy)</strong>이며, [TOGAF](/studynote/12_it_management/03_ea_isp/113_togaf/)(방법론)과 함께 사용하여 "어떻게 진행하는가"를 보완한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Zachman Framework 매트릭스 (간략)                   |
+-------------------------------------------------------+
|           What    How     Where   Who    When   Why   |
|  Planner  범위    기능목록  장소    조직    일정   동기 |
|  Owner    개념모델 프로세스 네트워크 역할    주기   전략 |
|  Designer 논리모델 논리흐름 분산아키 UI    이벤트  규칙 |
|  Builder  물리모델 물리설계 기술아키 보안    스케줄  제약 |
|                                                       |
|  데이터 관점: What 열 = 개념->논리->물리 모델링         |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Zachman은 건축에서 건축주(Owner)·설계사(Designer)·시공자([Builder](/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/)) 각각이 같은 건물을 다른 관점에서 보는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Zachman](/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/) vs [TOGAF](/studynote/12_it_management/03_ea_isp/113_togaf/)

| 비교 | [Zachman](/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/) | [TOGAF](/studynote/12_it_management/03_ea_isp/113_togaf/) |
|:---|:---|:---|
| **유형** | <strong><a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> 체계</strong> | <strong>방법론 (<a href="/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/">ADM</a>)</strong> |
| **질문** | What/How/Where/Who/When/Why | 아키텍처 개발 단계 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | 산출물 정리 | **프로세스 정의** |

- **📢 섹션 요약 비유**: Zachman은 서랍장([분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/))이고, TOGAF는 정리 순서(방법론)이다. 둘 다 필요하다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Zachman](/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/) | [TOGAF](/studynote/12_it_management/03_ea_isp/113_togaf/) | DoDAF |
|:---|:---|:---|:---|
| **용도** | 범용 [EA](/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) | 범용 [EA](/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) | 국방 |
| **특징** | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계 | **방법론** | 뷰포인트 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍처에서의 활용
- What([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) × Planner = 주제 영역(Subject Area).
- What × Owner = 개념 ERD.
- What × Designer = [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) ERD.
- What × [Builder](/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/) = 물리 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/).

---

## Ⅴ. 기대효과 및 결론

[Zachman](/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/) Framework는 <strong><a href="/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a>(<a href="/studynote/12_it_management/01_governance_strategy/806_ea_enterprise_architecture/">Enterprise Architecture</a>)의 원조 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> 체계</strong>로서, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·프로세스·네트워크·조직 등 모든 아키텍처 산출물을 체계적으로 관리하는 데 필수적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/05_security_compliance/243_zachman_framework_matrix/">Zachman</a></strong> | [EA](/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계 (6×6 매트릭스) |
| <strong><a href="/studynote/12_it_management/03_ea_isp/113_togaf/">TOGAF</a></strong> | [EA](/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 방법론 ([ADM](/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/) 프로세스) |
| **개념 모델** | Zachman의 Owner 행, What 열 |
| <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 모델</strong> | Zachman의 Designer 행, What 열 |
| **물리 모델** | Zachman의 [Builder](/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/) 행, What 열 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Zachman Framework (1987) — EA 분류 체계 제안]
    |
    v
[TOGAF (1995) — EA 방법론 (ADM)]
    |
    v
[FEAF / DoDAF (정부·국방 EA)]
    |
    v
[데이터 아키텍처 표준 (DA, 2010s)]
    |
    v
[현재: 데이터 메시 + EA — 분산 데이터 아키텍처]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Zachman은 <strong>큰 서랍장</strong>이에요. 가로 칸에는 "무엇·어떻게·어디서·누가·언제·왜"가 있어요.
2. 세로 칸에는 "사장님·설계사·건축가" 등 <strong>보는 사람</strong>이 달라요.
3. 같은 건물(시스템)이라도 <strong>보는 사람마다 다르게 정리</strong>하면 빠뜨리는 게 없답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 600

<- **이전**: [120. 데이터 역공학 (Data Reverse 엔진ering) - 기존 DB에서 ERD·모델 복원](/studynote/05_database/02_modeling_normalization/120_data_reverse_engineering/)
**다음**: [122. 마스터 데이터 관리 (MDM, Master Data Management) - 데이터 품질·일관성의 근간](/studynote/05_database/02_modeling_normalization/122_master_data_management_db_perspective/) ->

---
