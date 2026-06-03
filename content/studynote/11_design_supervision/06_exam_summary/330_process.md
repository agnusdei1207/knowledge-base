+++
title = "330. 기능점수 정산 증빙 (Function Point Settlement Evidence)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/)([Function Point](/knowledge-base/studynote/12_it_management/04_sdlc_testing/140_function_point/)) 정산 증빙은 기능점수 산정서, 변경 이력, 검수 근거를 한 체계로 묶어 대금 정산의 타당성을 입증하는 설계·감리 주제다.
> 2. **가치**: 개발 완료 후 실제 구현 기능량과 계약 기능량 사이의 차이를 수치화하여, 정산 분쟁을 예방하고 투명한 대금 지급 근거를 제공한다.
> 3. **판단 포인트**: 기능점수 산정 근거, 변경 기능의 추가·삭제 이력, 최종 검수 결과가 일관되게 연결되어 있는지가 감리의 핵심이다.

---

## Ⅰ. 개요 및 필요성

기능점수(Function Point, FP)는 소프트웨어의 규모를 기능 단위로 측정하는 국제 표준 방법론이다. 공공 정보화사업에서는 기능점수를 기반으로 개발 원가를 산정하고 계약금액을 결정하기 때문에, 사업 완료 후 실제 개발된 기능의 양과 계약 당시 산정된 기능점수가 일치하는지를 검증하는 정산 증빙이 필수적이다.

기능점수 정산 증빙이 필요한 이유는 크게 세 가지다. 첫째, 사업 진행 중 요구사항 변경으로 인해 기능이 추가·삭제·변경되는 경우가 빈번하다. 둘째, 기능점수 산정 방법에 대한 발주자와 수주자 간 해석 차이가 존재할 수 있다. 셋째, 감리 기관이 정산 타당성을 독립적으로 확인해야 하는 법적·제도적 요구가 있다.

기능점수 정산 증빙은 단순히 문서만 맞는지 확인하는 수준을 넘어, 기능점수 산정서와 소스 코드, 테스트 결과, 사용자 인수 검증 결과가 같은 방향을 가리키는지 교차 검증해야 한다. 그래야 감리 결과가 일회성 지적이 아니라 재현 가능한 개선 기준이 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">기능점수 정산 증빙 전체 흐름</div></div>
<div class="kb-diagram-note">계약 체결 시 기준 FP 확정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">사업 수행 중 변경 관리</div>
<div class="kb-diagram-tree-item" style="--depth:1">기능 추가 → FP 증가 변경 요청서</div>
<div class="kb-diagram-tree-item" style="--depth:1">기능 삭제 → FP 감소 변경 요청서</div>
<div class="kb-diagram-tree-item" style="--depth:1">기능 수정 → 영향 FP 재산정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">납품 전 최종 FP 산정서 작성</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">감리원 독립 검증 (3자 검토)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">정산 근거 확정 → 최종 대금 지급</div>
</div>
</div>



- **📢 섹션 요약 비유**: 체온계 수치를 읽기 전에 언제 어떻게 쟀는지부터 맞추는 것과 같다—측정 기준이 통일되어야 수치가 의미를 가진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 기능점수 산정 유형 비교

기능점수 산정에는 여러 방법이 있으며, 공공 사업에서 어떤 방법을 적용했는지가 정산 증빙의 출발점이다.

| 산정 유형 | 설명 | 적용 시점 | 오차 범위 |
|:---|:---|:---|:---|
| 개략 기능점수 (IFPUG 간이법) | 요구사항 개요 기반 산정 | 기획·제안 단계 | ±30% |
| 기능점수 간이법 | 화면·보고서·인터페이스 수 기반 | 제안·계약 단계 | ±15% |
| 기능점수 정밀법 | 트랜잭션·데이터 기능 상세 분석 | 설계 완료 후 | ±5% |
| ISBSG 방법론 | 국제 벤치마킹 기반 | 비교 산정 시 | 참고용 |

### 2. 기능점수 정산 증빙 3대 구성 요소

**기능점수 산정서**: 정산의 출발점으로, 계약 당시의 기준 FP와 최종 납품 FP를 모두 담아야 한다. 각 기능 항목(트랜잭션 기능 EI/EO/EQ, 데이터 기능 ILF/EIF)별 점수 산출 근거가 명시되어야 한다.

**변경 이력**: 사업 중 발생한 모든 기능 변경을 기록한 문서다. 변경 일자, 변경 요청자, 변경 내용, 승인자, FP 변동량이 포함되어야 하며, 계약 변경(계약 변경 서류)과 연동되어야 한다.

**검수 근거**: 최종 납품된 기능이 실제로 동작함을 입증하는 문서다. 사용자 인수 테스트 결과서, 기능 시연 화면 캡처, 검수 확인서가 포함된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">기능점수 정산 증빙 3대 구성 요소</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기능점수 산정서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 기준 FP: 계약 당시 산정값</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 최종 FP: 납품 시점 산정값</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 항목별 FP 산출 근거 (EI/EO/EQ/ILF/EIF)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">변경 이력</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 변경 일자·요청자·승인자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 기능 추가/삭제/수정 내역</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- FP 변동량 및 계약 변경 연동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">검수 근거</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 사용자 인수 테스트 결과서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 기능 시연 화면·로그</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 발주자 검수 확인서</div></div>
</div>
</div>



또한 기능점수 정산 증빙은 한 단계만 잘해서는 완성되지 않는다. [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/), 실행 메커니즘, 증적이 순환 구조를 이루어야 하며, 하나라도 비면 정산 타당성의 신뢰도가 떨어진다.

- **📢 섹션 요약 비유**: 계기판 숫자가 실제 엔진 상태와 연결되어야 운전이 가능한 것과 같다.

---

## Ⅲ. 비교 및 연결

### 기능점수 기반 정산 vs. 투입 인력 기반 정산

공공 정보화사업의 대금 정산 방식으로 기능점수 기반과 투입 인력(Man-Month) 기반이 있다. 두 방식의 차이를 이해하는 것이 실무와 시험 모두에서 중요하다.

| 비교 항목 | 기능점수 기반 정산 | 투입 인력 기반 정산 |
|:---|:---|:---|
| 측정 대상 | 소프트웨어 기능의 양 | 투입된 인력·시간 |
| 객관성 | 상대적으로 높음 | 주관적 요소 개입 가능 |
| 분쟁 위험 | 산정 방법 해석 차이 | 실제 투입 인력 검증 어려움 |
| 공공사업 적합성 | 높음 (SW사업대가기준 권고) | 유지보수·운영 사업에 혼용 |
| 감리 초점 | FP 산정 적정성 검증 | 출퇴근 기록·산출물 연계 확인 |

### 관련 제도 연결

| 관련 제도 | 연결 포인트 |
|:---|:---|
| SW사업대가기준 | 기능점수별 단가 산정 표준 |
| ISO/IEC 20926 (IFPUG FPA) | 기능점수 산정 국제 표준 |
| NESMA 간이법 | 초기 단계 빠른 산정 지원 |
| 정보화사업 감리 기준 | FP 검증 항목 명시 |

연결 개념으로는 목표치와 추세, 변경관리, 재검증이 있다. 즉 기능점수 정산 증빙은 단일 기법이 아니라 거버넌스와 운영 체계 속에서 읽어야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 한 번의 시험 점수보다 여러 번의 변화 추이를 보는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 기능점수 정산 증빙을 도입했는가보다 어떤 조건에서 정산 분쟁이 예방되는가를 먼저 봐야 한다. 기술사 답안도 '무조건 FP 적용'이 아니라 범위, 증거, 예외, 비용을 함께 써야 설득력이 생긴다.

### 실무 적용 시나리오

**분쟁 예방 시나리오**: 사업 초기에 FP 산정 방법론(IFPUG/NESMA 구분)과 기능 항목 목록을 발주자·수주자·감리원 3자가 합의하면, 사업 완료 후 정산 분쟁 가능성이 현저히 감소한다.

**변경 관리 연동 시나리오**: 매 스프린트(또는 단계) 완료 시마다 FP 변경 이력을 실시간으로 업데이트하면, 최종 정산 시 증빙 준비 부담이 줄어든다.

### 판단 체크리스트

1. 지표 정의와 산식이 기능점수 산정서 기준으로 고정되었는가?
2. 변경 이력 수집 경로가 자동화되고 검증 가능한가?
3. 검수 근거(사용자 인수 결과)가 FP 산정서와 1:1 대응되는가?
4. FP 변동이 계약 변경 서류와 연동되었는가?
5. 목표치 미달 시 우선순위와 보고 체계가 연결되는가?

### 안티패턴

- **FP 부풀리기**: 같은 기능을 여러 트랜잭션으로 쪼개 FP를 과다 산정하는 경우 → 감리에서 적발 시 계약 해지 사유
- **변경 미기록**: 요구사항 변경이 발생했지만 FP 변경 이력을 업데이트하지 않는 경우 → 정산 시 소급 적용 분쟁 발생
- **검수 형식화**: 실제 기능 동작 확인 없이 검수 확인서만 서명하는 경우 → 운영 후 하자 분쟁의 원인

- **📢 섹션 요약 비유**: 성적표에 원인과 보완 계획까지 적어 두는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

기능점수 정산 증빙을 제대로 적용하면 다음과 같은 효과가 나타난다.

**정량적 효과**
- 정산 분쟁 건수 50% 이상 감소 (3자 합의 기반 FP 산정 적용 시)
- 사업 완료 후 추가 비용 청구 분쟁 방지
- 감리 지적사항 중 FP 관련 항목 60~70% 감소

**정성적 효과**
- 발주자-수주자 신뢰 관계 강화
- 투명한 예산 집행 문화 정착
- 향후 유사 사업의 원가 산정 정확도 향상

결론적으로 기능점수 정산 증빙은 개념 암기보다 실제 적용 흐름과 분쟁 예방 관점에서 이해하는 것이 중요하다. 범위 정의, 구조 설계, 증거 검증, 종결 관리의 네 축을 함께 쓰는 것이 실무형 답안의 핵심이다. 향후에는 코드 분석 도구와 FP 자동 계산 시스템이 결합되어 정산 증빙의 자동화와 객관성이 더욱 높아질 전망이다.

- **📢 섹션 요약 비유**: 숫자를 보는 목적은 점수 자랑이 아니라 다음 행동을 정하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/) 산정서 | 기능점수 정산 증빙의 출발점이 되는 핵심 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)이다. |
| ILF/EIF/EI/EO/EQ | 기능점수 산정의 5가지 기본 요소로, 정산 근거의 세부 구성 단위다. |
| 변경 이력 | 실제 설계·운영·관리 메커니즘으로 이어지는 연결 축이다. |
| 검수 근거 | 판정과 재검증의 신뢰도를 높이는 증거 축이다. |
| SW사업대가기준 | 기능점수별 단가 산정의 법적 근거다. |
| 목표치와 추세 | 개별 활동을 거버넌스와 지속 개선으로 확장하는 축이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수작업 FP 산정 (전문가 판단 의존)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">정산 증빙 표준화 (SW사업대가기준 정착)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">도구 기반 자동 FP 계수 (화면 분석 자동화)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">코드 정적 분석 기반 FP 자동 산정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 기반 기능점수 예측 및 정산 자동화</div></div>
</div>
</div>



- 관련 키워드: [기능점수](/knowledge-base/studynote/04_software_engineering/uncategorized/673_function_point_ilf_eif/) 산정서, 변경 이력, 검수 근거, SW사업대가기준, ILF, EIF, IFPUG, NESMA

### 👶 어린이를 위한 3줄 비유 설명

1. 기능점수 정산 증빙은 레고 블록으로 무엇을 얼마나 만들었는지 세어서 기록하는 것과 같아요.
2. 처음에 약속한 블록 수와 실제 만든 블록 수가 맞는지 확인하는 선생님이 필요해요.
3. 중간에 블록이 늘었거나 줄었으면 그것도 모두 기록해야 나중에 돈을 정확히 받을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 408 / 530

← **이전**: [329. 전자정부법 의무 대상 (Mandatory Scope under the E-Government Act)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/329_process/)
**다음**: [331. 웹 접근성 KWCAG (Korean Web Content Accessibility Guidelines)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/331_kwcag/) →

---
