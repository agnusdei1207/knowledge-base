---
title: "143. Structured Analysis Dfd Dd Minispec"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구조적 분석은 <strong><a href="/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/">DFD</a>(<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름도)·<a href="/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/">DD</a>(<a href="/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a>)·<a href="/studynote/04_software_engineering/03_design_architecture/145_1_mini_spec/">Mini-Spec</a>(<a href="/studynote/04_software_engineering/03_design_architecture/145_1_mini_spec/">프로세스 명세서</a>)</strong>로 시스템의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름과 변환을 체계적으로 분석하는 전통적 방법론(DeMarco, 1978)이다.
> 2. **가치**: DFD는 시스템의 <strong>"무엇(What)"을 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 중심으로</strong> 표현하여, 사용자·분석가·개발자 간 <strong>공통 이해</strong>를 형성한다.
> 3. **판단 포인트**: DFD의 4대 구성요소(프로세스·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소·외부 엔티티)와 레벨링([Context](/studynote/02_operating_system/01_overview_architecture/033_context/)->Level 0->Level 1)이 핵심이며, 현재는 [UML](/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/)·User Story에 의해 보완되었다.

---

## Ⅰ. 개요 및 필요성

```text
DFD 4대 구성요소:
  ○ 프로세스 (데이터 변환)
  -> 데이터 흐름 (화살표)
  - 데이터 저장소 (DB)
  □ 외부 엔티티 (사용자·외부 시스템)
레벨링: Context DFD -> Level 0 -> Level 1 (분해)
```

- **📢 섹션 요약 비유**: DFD는 <strong>수도관 배관도</strong>이다. 물([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 어디서 와서 어디로 흐르는지 보여준다.

---

## Ⅱ~Ⅴ. 결론

구조적 분석은 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 중심의 전통적 분석 방법</strong>이며, [DFD](/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/)·[DD](/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/)·Mini-Spec의 3종 세트가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/">DFD</a></strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름도 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/">DD</a></strong> | [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/) |
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/145_1_mini_spec/">Mini-Spec</a></strong> | 프로세스 명세 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a> <a href="/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/">DFD</a></strong> | 최상위 레벨 |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/">UML</a></strong> | 현대적 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[구조적 분석 (DeMarco, 1978)] -> [SSADM (영국, 1980s)]
    -> [UML (1997)] -> [Agile User Story (2001)]
    -> [현재: DFD는 정보처리기사 시험 필수 + 레거시 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DFD는 <strong>수도관 배관도</strong>예요. 물([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 **어디서 어디로** 흐르는지 보여줘요.
2. [DD](/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/)([데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/))는 <strong>단어장</strong>이에요. "주문"이 뭔지 **정확히** 정의해요.
3. Mini-Spec은 <strong>요리 레시피</strong>예요. 프로세스가 **무엇을 하는지** 자세히 설명해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 973

<- **이전**: [142. 요구 분석 & 갈등 해결 - 이해관계자 간 상충 요구 조정](/studynote/04_software_engineering/03_design_architecture/142_requirements_analysis_conflict_resolution/)
**다음**: [144. DFD (Data Flow Diagram) - 데이터 흐름도 상세](/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/) ->

---
