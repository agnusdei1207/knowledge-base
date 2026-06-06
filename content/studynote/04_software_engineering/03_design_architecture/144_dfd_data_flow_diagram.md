---
title: "144. Dfd Data Flow Diagram"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DFD는 <strong>프로세스(○)·<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름(->)·<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 저장소(-)·외부 엔티티(□)</strong> 4가지 기호로 시스템의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환과 흐름을 계층적으로 표현하는 [구조적 분석](/studynote/04_software_engineering/03_design_architecture/143_structured_analysis_dfd_dd_minispec/) 도구이다.
> 2. **가치**: DFD는 <strong>"무엇(What)"에 집중</strong>하여 "어떻게(How)"를 배제하므로, 사용자·분석가·개발자가 시스템 범위와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름에 대해 <strong>공통 이해</strong>를 형성할 수 있다.
> 3. **판단 포인트**: [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) DFD(Level 0, 시스템 전체)->Level 1(주요 프로세스 분해)->Level 2(상세 분해)로 레벨링하며, 균형 규칙(입출력 일치)을 준수해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
Context DFD: 시스템 전체를 하나의 프로세스로 표현
Level 1: 주요 프로세스 3~7개로 분해
Level 2: 각 프로세스를 더 상세히 분해
균형 규칙: 상위 DFD의 입출력 = 하위 DFD의 입출력
```

- **📢 섹션 요약 비유**: DFD 레벨링은 <strong>지도 확대</strong>이다. 세계지도([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))->나라(L1)->도시(L2)로 점점 상세해진다.

---

## Ⅱ~Ⅴ. 결론

DFD는 <strong><a href="/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/">데이터 중심</a> 시스템 분석의 표준 도구</strong>이며, 정보처리기사·SSADM의 필수 산출물이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DFD** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름도 |
| **프로세스** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 (○) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 저장소</strong> | DB (-) |
| **균형 규칙** | 입출력 일치 |
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/145_1_mini_spec/">Mini-Spec</a></strong> | 프로세스 상세 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DFD (DeMarco, 1978)] -> [Yourdon DFD (1989)]
    -> [SSADM (영국 표준)] -> [UML Activity Diagram (대안)]
    -> [현재: 정보처리기사 필수 + 레거시 분석 도구]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DFD는 <strong>지도</strong>예요. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 **어디서 어디로** 흐르는지 보여줘요.
2. 세계지도(전체)->나라(L1)->도시(L2)처럼 **점점 자세히** 그려요.
3. 동그라미(프로세스)는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 바꾸는 곳</strong>, 화살표는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 가는 길</strong>이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 973

<- **이전**: [143. 구조적 분석 (Structured Analysis) - DFD·DD·Mini-Spec](/studynote/04_software_engineering/03_design_architecture/143_structured_analysis_dfd_dd_minispec/)
**다음**: [145. Mini-Spec (프로세스 명세서) - DFD 프로세스 상세 정의](/studynote/04_software_engineering/03_design_architecture/145_1_mini_spec/) ->

---
