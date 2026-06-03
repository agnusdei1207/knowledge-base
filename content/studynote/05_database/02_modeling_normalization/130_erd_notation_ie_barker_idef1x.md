+++
title = "130. ERD 표기법 비교 (IE·Barker·IDEF1X)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ERD 표기법은 엔터티·[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)·관계를 시각적으로 표현하는 규칙이며, **IE(Information Engineering, 까마귀발)·Barker(원·실선)·IDEF1X(국방 표준)** 3가지가 대표적이다.
> 2. **가치**: 표기법을 통일하지 않으면 같은 모델을 팀원마다 다르게 해석하고, 도구 간 호환이 안 되며, 발주처·감리 기준 충족이 어렵다.
> 3. **판단 포인트**: 한국 공공 SI는 <strong>IE(까마귀발)</strong>이 사실상 표준이며, Oracle은 Barker, 국방·항공은 IDEF1X를 사용한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3대 ERD 표기법</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IE (까마귀발): ── ── (1:N)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Barker: ──O── (선택), ──</div><div class="kb-diagram-cell">── (필수)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IDEF1X: ●── (식별), ◇── (비식별)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한국 SI 표준: IE (까마귀발)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 표기법은 지도의 <strong>범례</strong>이다. 같은 지형도 범례가 다르면 다르게 읽힌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 표기법 | 카디널리티 | [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)/비식별 | 도구 |
|:---|:---|:---|:---|
| **IE** | 까마귀발 | 실선/점선 | <strong>ERwin, <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">DA</a>#</strong> |
| **Barker** | 원·바 | 라인 스타일 | <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/">Oracle</a> Designer</strong> |
| **IDEF1X** | ●·◇ | 원형 마크 | **ERwin** |

---

## Ⅲ~Ⅴ. 결론

ERD 표기법 선택은 <strong>프로젝트·조직·도구에 의해 결정</strong>되며, IE(까마귀발)가 국내 SI의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IE 표기법** | 까마귀발 (한국 SI 표준) |
| **Barker** | [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) 표기법 |
| **IDEF1X** | 국방 표준 |
| **카디널리티** | 1:1, 1:N, M:N |
| **ERwin** | 대표 모델링 도구 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Chen 표기법 (1976)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">IE 까마귀발 (1981)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">IDEF1X (1985, 국방)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Barker (Oracle, 1990s)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">UML 클래스 (2000s)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: 도구 자동 변환 — 표기법 간 호환</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. ERD 표기법은 지도의 <strong>범례</strong>예요. "산은 △, 강은 ~" 같은 약속이에요.
2. 같은 데이터도 **범례(표기법)가 다르면** 다르게 그려져요.
3. 한국에서는 **IE(까마귀발)** 표기법을 가장 많이 사용한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 600

← **이전**: [129. ORM & 임피던스 불일치 (Object-Relational Mismatch)](/knowledge-base/studynote/05_database/02_modeling_normalization/129_orm_impedance_mismatch/)
**다음**: [131. SQL 표준 (ANSI/ISO SQL) - 관계형 데이터베이스 질의 언어 표준](/knowledge-base/studynote/05_database/03_relational_model/131_sql_ansi_iso_standard/) →

---
