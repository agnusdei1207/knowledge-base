---
title: 143. 구조적 분석 (Structured Analysis) - DFD·DD·Mini-Spec
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구조적 분석은 **[[144_dfd_data_flow_diagram|DFD]]([[001_dikw_pyramid|데이터]] 흐름도)·[[769_architecture|DD]]([[393_data_dictionary|데이터 사전]])·[[145_1_mini_spec|Mini-Spec]]([[145_1_mini_spec|프로세스 명세서]])**로 시스템의 [[001_dikw_pyramid|데이터]] 흐름과 변환을 체계적으로 분석하는 전통적 방법론(DeMarco, 1978)이다.
> 2. **가치**: DFD는 시스템의 **"무엇(What)"을 [[001_dikw_pyramid|데이터]] 흐름 중심으로** 표현하여, 사용자·분석가·개발자 간 **공통 이해**를 형성한다.
> 3. **판단 포인트**: DFD의 4대 구성요소(프로세스·[[001_dikw_pyramid|데이터]] 흐름·[[001_dikw_pyramid|데이터]] 저장소·외부 엔티티)와 레벨링([[033_context|Context]]→Level 0→Level 1)이 핵심이며, 현재는 [[232_uml_unified_modeling_language_overview|UML]]·User Story에 의해 보완되었다.

---

## Ⅰ. 개요 및 필요성

```text
DFD 4대 구성요소:
  ○ 프로세스 (데이터 변환)
  → 데이터 흐름 (화살표)
  ═ 데이터 저장소 (DB)
  □ 외부 엔티티 (사용자·외부 시스템)
레벨링: Context DFD → Level 0 → Level 1 (분해)
```

- **📢 섹션 요약 비유**: DFD는 **수도관 배관도**이다. 물([[001_dikw_pyramid|데이터]])이 어디서 와서 어디로 흐르는지 보여준다.

---

## Ⅱ~Ⅴ. 결론

구조적 분석은 **[[001_dikw_pyramid|데이터]] 흐름 중심의 전통적 분석 방법**이며, [[144_dfd_data_flow_diagram|DFD]]·[[769_architecture|DD]]·Mini-Spec의 3종 세트가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[144_dfd_data_flow_diagram|DFD]]** | [[001_dikw_pyramid|데이터]] 흐름도 |
| **[[769_architecture|DD]]** | [[393_data_dictionary|데이터 사전]] |
| **[[145_1_mini_spec|Mini-Spec]]** | 프로세스 명세 |
| **[[033_context|Context]] [[144_dfd_data_flow_diagram|DFD]]** | 최상위 레벨 |
| **[[232_uml_unified_modeling_language_overview|UML]]** | 현대적 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[구조적 분석 (DeMarco, 1978)] → [SSADM (영국, 1980s)]
    → [UML (1997)] → [Agile User Story (2001)]
    → [현재: DFD는 정보처리기사 시험 필수 + 레거시 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DFD는 **수도관 배관도**예요. 물([[001_dikw_pyramid|데이터]])이 **어디서 어디로** 흐르는지 보여줘요.
2. [[769_architecture|DD]]([[393_data_dictionary|데이터 사전]])는 **단어장**이에요. "주문"이 뭔지 **정확히** 정의해요.
3. Mini-Spec은 **요리 레시피**예요. 프로세스가 **무엇을 하는지** 자세히 설명해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 973

← **이전**: [[142_requirements_analysis_conflict_resolution|142. 요구 분석 & 갈등 해결 - 이해관계자 간 상충 요구 조정]]
**다음**: [[144_dfd_data_flow_diagram|144. DFD (Data Flow Diagram) - 데이터 흐름도 상세]] →

---
