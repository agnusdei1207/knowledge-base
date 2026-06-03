+++
title = "342. 시정 조치 조율 위원회 (Corrective Action Coordination Committee)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시정 조치 조율 위원회(CACC, Corrective Action Coordination Committee)는 조치 우선순위, 책임 부서 조정, 종결 검증을 한 체계로 묶어 감리 지적사항이 실질적인 개선으로 이어지도록 조율·감독하는 설계·감리 주제다.
> 2. **가치**: 감리 결과는 보고서 제출로 끝나는 것이 아니라 실제 시정이 완료되어야 의미가 있다. 시정 조치 조율 위원회는 지적사항의 우선순위 조정, 부서 간 책임 배분, 종결 기준 합의를 통해 감리 효과를 현장에 착지시키는 실행 기구다.
> 3. **판단 포인트**: 지적사항별 조치 계획, 담당자, 기한이 명확히 배정되었는지, 종결 검증이 독립적 확인으로 수행되었는지가 감리의 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

감리 지적사항은 감리 보고서에 기재된 순간부터 시정 조치가 완결되기까지 체계적으로 추적·관리되어야 한다. 그러나 현실에서는 감리 보고서가 제출된 후 시정 조치가 지연되거나, 부서 간 책임 공방으로 조치가 이루어지지 않거나, 형식적인 '완료' 선언으로 실질적 개선 없이 종결 처리되는 경우가 빈번하다.

시정 조치 조율 위원회(CACC)는 이러한 문제를 구조적으로 해결하기 위한 거버넌스 기구다. CACC는 발주 기관 내 관련 부서 책임자로 구성되며, 감리 지적사항에 대해 다음을 공식적으로 수행한다.

- **우선순위 조정**: 긴급도와 영향도를 기준으로 지적사항의 처리 순서를 결정
- **책임 배분**: 각 지적사항의 조치 책임 부서와 담당자를 명확히 지정
- **기한 설정**: 현실적이고 강제력 있는 조치 완료 기한 설정
- **진행 상황 모니터링**: 정기 회의를 통해 조치 진행 현황 점검
- **종결 검증**: 조치 완료 보고 후 독립적 재검증 수행

최근 공공 정보화사업의 복잡도가 높아지면서 단일 감리 지적사항이 여러 부서에 걸친 시정 조치를 필요로 하는 경우가 증가하고 있다. 이런 상황에서 CACC는 부서 간 조율과 갈등 해소를 위한 공식 채널로서 더욱 중요한 역할을 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">시정 조치 조율 위원회 운영 사이클</div></div>
<div class="kb-diagram-note">감리 보고서 수신</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CACC 1차 회의: 지적사항 분류 및 배분</div>
<div class="kb-diagram-tree-item" style="--depth:1">긴급/중요/일반 우선순위 분류</div>
<div class="kb-diagram-tree-item" style="--depth:1">부서별 책임 배분</div>
<div class="kb-diagram-tree-item" style="--depth:1">조치 기한 설정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">각 부서 조치 계획 수립 및 이행</div>
<div class="kb-diagram-tree-item" style="--depth:1">개별 조치 담당자 지정</div>
<div class="kb-diagram-tree-item" style="--depth:1">조치 내용 문서화</div>
<div class="kb-diagram-tree-item" style="--depth:1">이행 증거 수집</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CACC 정기 점검 회의 (주간/월간)</div>
<div class="kb-diagram-tree-item" style="--depth:1">진행 현황 보고</div>
<div class="kb-diagram-tree-item" style="--depth:1">지연 항목 재조율</div>
<div class="kb-diagram-tree-item" style="--depth:1">위험 항목 에스컬레이션</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">조치 완료 보고</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">독립 종결 검증</div>
<div class="kb-diagram-tree-item" style="--depth:1">조치 내용 실제 확인</div>
<div class="kb-diagram-tree-item" style="--depth:1">재발 방지 조치 점검</div>
<div class="kb-diagram-tree-item" style="--depth:1">CACC 공식 종결 승인</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">감리 이력 데이터베이스 갱신</div>
</div>
</div>



- **📢 섹션 요약 비유**: 학교에서 숙제 검사 후 틀린 학생들이 실제로 고쳤는지 다시 확인하는 선생님과 학부모 회의와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. CACC 구성 및 역할

| 구성원 | 역할 | 책임 |
|:---|:---|:---|
| CACC 위원장 | 주요 의사결정, 최종 승인 | 발주 기관 사업 총괄자 |
| 업무 부서 책임자 | 업무 관련 시정 조치 이행 | 담당 업무 시정 완료 |
| IT 담당자 | 기술 조치 이행, 증빙 수집 | 시스템 변경·패치 적용 |
| 품질 관리자 | 조치 내용 검증, 문서화 | 종결 검증 수행 |
| 감리 기관 대표 | 조치 적정성 확인 (자문) | 독립적 검증 지원 |

### 2. 지적사항 우선순위 분류 체계

감리 지적사항은 긴급도와 영향도를 기준으로 3단계로 분류된다.

| 분류 | 기준 | 조치 기한 | 예시 |
|:---|:---|:---|:---|
| 긴급 (Critical) | 서비스 장애·보안 침해 위험 | 즉시~7일 이내 | 암호화 미적용, SQL 인젝션 취약점 |
| 중요 (Major) | 주요 업무 프로세스 영향 | 30일 이내 | 접근 통제 미흡, 백업 정책 부재 |
| 일반 (Minor) | 문서 미비, 경미한 절차 개선 | 60~90일 이내 | 산출물 형식 불일치, 담당자 명기 누락 |

### 3. 시정 조치 추적 관리 체계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">시정 조치 추적 문서 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">지적사항 목록 (Issue Register)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 지적번호, 지적내용, 감리 유형</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 우선순위, 책임 부서, 담당자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 조치 기한, 현재 상태 (Open/In Progress/Closed)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조치 계획서 (Action Plan)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 지적번호별 구체적 조치 내용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 조치 방법, 담당자, 중간 점검 기준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 예상 완료일, 실제 완료일</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이행 증거 (Evidence Package)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 조치 전/후 스크린샷, 로그</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 설정 변경 내역, 테스트 결과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 담당자 서명, 책임자 승인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">종결 검증 보고서 (Closure Verification Report)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- CACC 검증 날짜, 검증자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 조치 적정성 판단 근거</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 공식 종결 승인 기록</div></div>
</div>
</div>



또한 시정 조치 조율 위원회는 한 단계만 잘해서는 완성되지 않는다. [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/), 실행 메커니즘, 증적이 순환 구조를 이루어야 하며, 하나라도 비면 적합 판정의 신뢰도가 떨어진다.

- **📢 섹션 요약 비유**: 재료 창고, 작업 순서, 검수표가 한 줄로 이어져야 하는 공장과 같다.

---

## Ⅲ. 비교 및 연결

### CACC vs. CCB (변경통제위원회) 비교

| 비교 항목 | CACC (시정 조치 조율 위원회) | CCB (변경통제위원회) |
|:---|:---|:---|
| 목적 | 감리 지적사항의 시정 완결 | 설계 변경의 승인·통제 |
| 운영 시점 | 감리 보고서 수신 후 | 개발·운영 전 주기 |
| 구성원 | 발주 기관 부서 책임자 + 감리 기관 | 프로젝트 관리자 + 개발팀 + 발주자 |
| 주요 산출물 | 지적사항 목록, 조치 계획서, 종결 보고서 | 변경 요청서, 영향도 분석서, CCB 회의록 |
| 법적 근거 | 전자정부법·감리 기준 | 형상관리 계획서 |

### 관련 개념 연결

| 관련 개념 | 연결 포인트 |
|:---|:---|
| 감리 독립성 | CACC 검증은 독립적으로 수행되어야 신뢰성 확보 |
| 리스크 관리 | 긴급 지적사항은 리스크 레지스터와 연동 관리 |
| 변경관리 | 시정 조치가 시스템 변경을 수반하는 경우 CCB 연동 필요 |
| IT 거버넌스 | CACC는 IT 거버넌스 체계 내 실행 위원회로 위치 |

연결 개념으로는 시정 조치 추적, 변경관리, 재검증이 있다. 즉 시정 조치 조율 위원회는 단일 기법이 아니라 거버넌스와 운영 체계 속에서 읽어야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 계획표만 있는 반과 숙제 검사까지 하는 반의 차이를 비교하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 시정 조치 조율 위원회를 도입했는가보다 어떤 조건에서 지적사항이 실질적으로 개선되는가를 먼저 봐야 한다. 기술사 답안도 '위원회 설치'만이 아니라 범위, 증거, 예외, 비용을 함께 써야 설득력이 생긴다.

### 실무 적용 시나리오

**시나리오 1 - 긴급 지적사항 처리**: 보안 취약점(SQL 인젝션)이 감리에서 발견된 경우, CACC가 긴급 소집되어 3일 이내 패치 적용을 결정하고, 품질 관리자가 패치 적용 후 독립 검증 수행

**시나리오 2 - 부서 간 책임 분쟁**: 개인정보 암호화 미적용 지적에 대해 개발팀과 운영팀이 서로 책임을 전가하는 경우, CACC가 조정회의를 통해 책임 범위를 명확히 분리하고 각각에 기한을 배정

**시나리오 3 - 형식적 종결 방지**: 담당자가 "완료"라고 보고했지만 실제 변경이 미흡한 경우, CACC 품질 관리자가 이행 증거(로그·화면 캡처)를 직접 확인 후 재조치 요구

### 판단 체크리스트

1. 지적사항별 조치 우선순위가 긴급도·영향도 기준으로 분류되었는가?
2. 각 지적사항의 책임 부서·담당자·기한이 명확히 배정되었는가?
3. 정기 진행 상황 점검 회의가 운영되고 회의록이 남아 있는가?
4. 종결 검증이 담당자 자체 선언이 아닌 독립적 확인으로 수행되었는가?
5. 지적사항의 Open/Closed 현황이 실시간으로 추적되는가?

### 안티패턴

- **자체 종결 선언**: 담당자가 "완료했다"고 보고하면 그대로 종결 처리하는 경우 → 실질적 개선 없이 동일 문제 반복
- **기한 없는 조치 계획**: 조치 계획은 수립했지만 완료 기한이 없거나 "협의 중" 상태로 방치되는 경우 → 영구 미해결 지적사항 발생
- **위원회 미소집**: 감리 보고서 수신 후 CACC 회의를 소집하지 않고 이메일로만 처리하는 경우 → 부서 간 조율 실패, 지연 장기화

- **📢 섹션 요약 비유**: 체크리스트에 담당자와 마감일을 적어 실제로 끝내는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

시정 조치 조율 위원회를 제대로 적용하면 다음과 같은 효과가 나타난다.

**정량적 효과**
- 감리 지적사항 평균 처리 기간 40~50% 단축 (CACC 운영 기관 기준)
- 동일 유형 지적사항 반복 발생률 30~40% 감소
- 기한 내 조치 완료율 90% 이상 달성

**정성적 효과**
- 감리 결과의 실효성 제고 (보고서가 아닌 개선으로 귀결)
- 발주 기관 내 IT 거버넌스 문화 성숙
- 이해관계자 사이의 책임 명확화로 분쟁 예방

결론적으로 시정 조치 조율 위원회는 감리 프로세스의 완성을 위한 필수 실행 기구다. 범위 정의, 구조 설계, 증거 검증, 종결 관리의 네 축을 함께 쓰는 것이 실무형 답안의 핵심이다. 앞으로는 디지털 대시보드 기반의 실시간 지적사항 추적 시스템이 CACC 운영을 지원하여 투명성과 효율성이 더욱 향상될 전망이다.

- **📢 섹션 요약 비유**: 인수인계 노트가 좋아야 다음 사람이 같은 실수를 반복하지 않는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 조치 우선순위 | 시정 조치 조율 위원회의 자원 배분 기준이다. |
| 책임 부서 조정 | 부서 간 책임 경계를 명확히 하여 조치 지연을 방지한다. |
| 종결 검증 | 형식적 완료를 방지하는 독립적 확인 활동이다. |
| 지적사항 목록 | 전체 감리 지적사항을 추적하는 핵심 관리 문서다. |
| 시정 조치 추적 | 개별 활동을 거버넌스와 지속 개선으로 확장하는 축이다. |
| IT 거버넌스 | CACC를 상위 거버넌스 체계와 연결하는 개념이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">개별 부서 자율 보완 (감리 이후 방치)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">위원회 기반 공식 조율 (CACC 운영)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">대시보드 기반 실시간 추적</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전사 리스크 보드 연동 (지적 → 리스크 관리)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 기반 지적사항 재발 예측 및 예방</div></div>
</div>
</div>



- 관련 키워드: 시정 조치, CACC, 지적사항 추적, 종결 검증, IT 거버넌스, 리스크 관리

### 👶 어린이를 위한 3줄 비유 설명

1. 시정 조치 조율 위원회는 숙제를 잘못한 학생들이 실제로 고쳤는지 부모님과 선생님이 함께 확인하는 것과 같아요.
2. 누가 어떤 숙제를 언제까지 고칠지 미리 정해야 모두가 기억할 수 있어요.
3. "다 했어요"라고 말만 하는 게 아니라 실제로 고친 숙제를 보여줘야 끝나는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 420 / 530

← **이전**: [341. 감리 독립성 지배 구조 (Audit Independence Governance)](/knowledge-base/studynote/12_it_management/05_security_compliance/341_audit/)
**다음**: [343. 공공데이터 개방 JSON 규격 (Public Data JSON Standard)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) →

---
