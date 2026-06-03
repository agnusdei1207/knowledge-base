+++
title = "039. 샘플링 감리 기법 (Sampling Audit Technique)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

> **핵심 인사이트**
> 1. 감리에서 전수 검토(100% 검사)는 비용·시간상 불가능한 경우가 많으므로, 통계적 샘플링(Statistical [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))을 통해 모집단(Population)의 특성을 신뢰 수준([Confidence](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) Level)과 허용 오차(Tolerable Error) 내에서 추론한다.
> 2. 샘플링 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)([Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/) [Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/))는 샘플이 모집단을 대표하지 못할 위험으로, 표본 크기(Sample Size)가 클수록 줄어들지만 영구적으로 제거되지는 않는다 — 이것이 샘플링 기반 감리 의견의 근본적 한계이자 전제이다.
> 3. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 샘플링([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))은 통제의 준수율 평가에, 변수 샘플링(Variables [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))은 금액적 오류의 규모 추정에 사용 — 감리 목적에 따라 방법을 선택해야 한다.

---

## I. 샘플링의 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전수 검토가 어려운 이유:</div>
<div class="kb-diagram-note">거래 건수: 연간 수백만 건 가능</div>
<div class="kb-diagram-note">문서 수: 수만 장</div>
<div class="kb-diagram-note">비용: 전수 = 감리 비용 수십 배</div>
<div class="kb-diagram-note">시간: 감리 기간 내 불가</div>
<div class="kb-diagram-note">샘플링 접근:</div>
<div class="kb-diagram-note">모집단의 일부(표본)를 검토</div>
<div class="kb-diagram-note">표본 특성 -&gt; 모집단 특성 추론</div>
<div class="kb-diagram-note">기본 개념:</div>
<div class="kb-diagram-note">모집단 (Population): 전체 검토 대상</div>
<div class="kb-diagram-note">표본 (Sample): 선택된 항목들</div>
<div class="kb-diagram-note">샘플링 단위: 각 개별 항목 (거래, 문서 등)</div>
<div class="kb-diagram-note">오류 유형:</div>
<div class="kb-diagram-note">α 오류 (Type I / 과도한 거부):</div>
<div class="kb-diagram-note">실제 통제가 잘 되고 있는데 문제 있다고 판단</div>
<div class="kb-diagram-tree-item" style="--depth:2">감리 비용 증가</div>
<div class="kb-diagram-note">β 오류 (Type II / 과도한 수용):</div>
<div class="kb-diagram-note">실제 통제에 문제 있는데 없다고 판단</div>
<div class="kb-diagram-tree-item" style="--depth:2">감리 실패 (더 위험)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 식품 공장 품질 검사처럼 제품 100개 중 5개만 검사 — 5개가 모두 합격이면 100개도 대부분 합격이라고 추론.

---

## II. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 샘플링



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">속성 샘플링 (Attribute Sampling):</div>
<div class="kb-diagram-note">통제의 준수율(%)을 추정</div>
<div class="kb-diagram-note">예: "모든 변경 요청에 승인자 서명 있는가?"</div>
<div class="kb-diagram-note">절차:</div>
<div class="kb-diagram-note">1. 목표 설정:</div>
<div class="kb-diagram-note">허용 이탈률 (TER): 5% (5% 이하면 합격)</div>
<div class="kb-diagram-note">신뢰 수준: 95%</div>
<div class="kb-diagram-note">2. 표본 크기 결정:</div>
<div class="kb-diagram-note">TER이 낮을수록 더 많은 표본 필요</div>
<div class="kb-diagram-note">표준 표본 크기 테이블 사용</div>
<div class="kb-diagram-note">(예: TER=5%, 신뢰 95% -&gt; n=60)</div>
<div class="kb-diagram-note">3. 무작위 선택 후 검토:</div>
<div class="kb-diagram-note">60개 변경 요청 검토</div>
<div class="kb-diagram-note">4. 결과 평가:</div>
<div class="kb-diagram-note">실제 오류 2개 발견 (3.3%)</div>
<div class="kb-diagram-tree-item" style="--depth:2">TER(5%) 이하 -&gt; 통제 효과적</div>
<div class="kb-diagram-note">표본 크기 영향 요소:</div>
<div class="kb-diagram-note">신뢰 수준 ↑ -&gt; 표본 크기 ↑</div>
<div class="kb-diagram-note">허용 오류율 ↓ -&gt; 표본 크기 ↑</div>
<div class="kb-diagram-note">예상 모집단 오류율 ↑ -&gt; 표본 크기 ↑</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 샘플링은 선거 여론조사처럼 — 1,000명 물어보고 "60% 지지 ± 3%" 추론, 더 확실하려면 더 많이 물어봐야 함.

---

## III. 변수 샘플링



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">변수 샘플링 (Variables Sampling):</div>
<div class="kb-diagram-note">금액적 오류의 규모를 추정</div>
<div class="kb-diagram-note">계정 잔액의 정확성 평가</div>
<div class="kb-diagram-note">MUS (Monetary Unit Sampling, 금액 단위 샘플링):</div>
<div class="kb-diagram-note">가장 일반적인 변수 샘플링 방법</div>
<div class="kb-diagram-note">금액에 비례한 선택 (큰 금액 항목 자주 선택)</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">재고 자산 총액: 10억원</div>
<div class="kb-diagram-note">표본 크기: 100개</div>
<div class="kb-diagram-note">무작위 선택: 금액 단위로 (1원~10억원)</div>
<div class="kb-diagram-tree-item" style="--depth:1">큰 금액 거래가 선택될 확률 높음</div>
<div class="kb-diagram-note">결과 해석:</div>
<div class="kb-diagram-note">표본 오류율 = 2%</div>
<div class="kb-diagram-tree-item" style="--depth:1">추정 모집단 오류: 10억 × 2% = 2천만원</div>
<div class="kb-diagram-note">허용 가능 오류 한계: 5천만원</div>
<div class="kb-diagram-tree-item" style="--depth:1">2천만원 &lt; 5천만원 -&gt; 수용</div>
<div class="kb-diagram-note">만약 추정 오류 &gt; 허용 한계:</div>
<div class="kb-diagram-tree-item" style="--depth:1">추가 샘플링 또는 전수 조사</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 변수 샘플링은 은행 대출 포트폴리오 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) — 100억 대출 중 5억 샘플링해서 전체 오류 금액 추정.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 샘플링 방법



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">표본 선택 방법:</div>
<div class="kb-diagram-note">1. 단순 무작위 (Simple Random):</div>
<div class="kb-diagram-note">난수 테이블/컴퓨터로 균등 선택</div>
<div class="kb-diagram-note">편향 없음, 가장 기본</div>
<div class="kb-diagram-note">2. 계통 (Systematic):</div>
<div class="kb-diagram-note">일정 간격으로 선택</div>
<div class="kb-diagram-note">예: 100개 중 10개 -&gt; 매 10번째</div>
<div class="kb-diagram-note">주의: 주기적 패턴 있으면 편향 가능</div>
<div class="kb-diagram-note">3. 층화 (Stratified):</div>
<div class="kb-diagram-note">모집단을 층으로 나눠 각 층에서 추출</div>
<div class="kb-diagram-note">예: 금액 규모별 층 (소액/중액/대액)</div>
<div class="kb-diagram-note">변동성 높은 모집단에 효과적</div>
<div class="kb-diagram-note">4. 군집 (Cluster):</div>
<div class="kb-diagram-note">군집 단위로 선택 후 전수 조사</div>
<div class="kb-diagram-note">예: 10개 지점 중 3개 선택 -&gt; 3개 전수</div>
<div class="kb-diagram-note">비용 절감 but 샘플링 리스크 증가</div>
<div class="kb-diagram-note">5. PPS (확률-크기 비례):</div>
<div class="kb-diagram-note">금액에 비례한 선택 확률 (= MUS)</div>
<div class="kb-diagram-note">감리에서 가장 권장</div>
</div>
</div>



| 방법    | 특징          | 주요 용도        |
|-------|-------------|--------------|
| 단순 무작위 | 편향 없음    | 일반 감리       |
| 계통   | 편의성        | 순서 있는 모집단  |
| 층화   | 효율성        | 변동성 큰 모집단  |
| PPS   | 금액 비례 선택  | 재무 감리       |

> 📢 **섹션 요약 비유**: 층화 샘플링은 학교 설문에서 학년별로 따로 뽑는 것 — 균형 잡힌 대표성 확보.

---

## V. 실무 시나리오 — [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) 감리 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 샘플링



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">감리 목적: 접근 권한 검토 절차 준수 확인</div>
<div class="kb-diagram-note">모집단: 지난 1년간 권한 변경 이력 2,400건</div>
<div class="kb-diagram-note">설계:</div>
<div class="kb-diagram-note">허용 이탈률 (TER): 5%</div>
<div class="kb-diagram-note">신뢰 수준: 90%</div>
<div class="kb-diagram-note">예상 모집단 오류율: 2%</div>
<div class="kb-diagram-tree-item" style="--depth:1">표본 크기 계산: 77건 (표준 테이블)</div>
<div class="kb-diagram-note">샘플 선택:</div>
<div class="kb-diagram-note">MUS로 77건 무작위 선택</div>
<div class="kb-diagram-note">검토 항목:</div>
<div class="kb-diagram-tree-item" style="--depth:1">승인자 서명 있는가?</div>
<div class="kb-diagram-tree-item" style="--depth:1">직무 분리 원칙 준수?</div>
<div class="kb-diagram-tree-item" style="--depth:1">최소 권한 원칙 적용?</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">실제 오류 4건 (5.2%) 발견</div>
<div class="kb-diagram-tree-item" style="--depth:1">TER 5% 초과!</div>
<div class="kb-diagram-tree-item" style="--depth:1">통제 효과성 미달 결론</div>
<div class="kb-diagram-note">발견 사항:</div>
<div class="kb-diagram-note">"권한 변경 승인 프로세스 준수율 94.8%</div>
<div class="kb-diagram-note">허용 기준(95%) 미달</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">증거: 샘플링 워크시트 Appendix B</div><div class="kb-diagram-note">"</div></div>
<div class="kb-diagram-note">권고:</div>
<div class="kb-diagram-note">권한 변경 워크플로우 자동화로</div>
<div class="kb-diagram-note">미승인 변경 원천 차단 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 77건 샘플에서 4건 오류 -> 전체 2,400건에서 약 125건 [오류 추정](/knowledge-base/studynote/04_software_engineering/11_testing_validation/434_error_guessing/) — 전수 검토 없이도 문제 규모 파악 가능.

---

## 📌 관련 개념 맵

```
샘플링 감리 기법
+-- 샘플링 유형
|   +-- 속성 샘플링 (준수율 %)
|   +-- 변수 샘플링 (금액 오류)
+-- 샘플링 방법
|   +-- 단순 무작위, 계통, 층화
|   +-- PPS/MUS (금액 비례)
+-- 품질 지표
|   +-- 신뢰 수준 (90%, 95%)
|   +-- 허용 오류율 (TER)
+-- 리스크
    +-- α 오류 (과도한 거부)
    +-- β 오류 (과도한 수용)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[통계적 샘플링 이론 (Fisher, 1920s)]
표본 이론, 신뢰 구간
      |
      v
[감사 샘플링 적용 (AICPA, 1970s)]
속성/변수 샘플링 감사 기준
      |
      v
[MUS 보편화 (1980s)]
재무 감사 표준 기법
      |
      v
[IT 감리 적용 (2000s)]
통제 준수율 샘플링
ISACA, IIA 가이드라인
      |
      v
[현재: 빅데이터 전수 분석]
데이터 분석 기반 전수 검토 가능
(단, 통계적 샘플링 원칙은 여전히 유효)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 샘플링 감리는 식품 공장에서 제품 10개만 검사하고 전체 품질을 판단하는 것처럼, 모든 서류를 다 확인하는 대신 일부만 골라 전체를 추론하는 방법이에요.
2. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 샘플링은 "승인 서명이 있는 서류 비율이 5% 이상 없으면 문제"처럼 통제 준수율을 확인하고, 변수 샘플링은 "오류 금액이 얼마나 되는지"를 추정해요.
3. 표본이 클수록 더 정확하지만 비용이 늘어나서, 신뢰 수준과 허용 오류 범위를 정해 적정한 표본 크기를 계산하는 것이 핵심이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 530

← **이전**: [39. 전자정부 표준 프레임워크 아키텍처 및 적용 기준 점검 (eGovFrame Architecture Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/039_egovframe_architecture_audit/)
**다음**: [040. 감리인 독립성 (Auditor Independence)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/040_auditor_independence/) →

---
