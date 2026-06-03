+++
title = "136. CROSS JOIN & Cartesian Product - 카테시안 곱 결합"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CROSS JOIN은 <strong>두 테이블의 모든 행을 서로 조합(<a href="/knowledge-base/studynote/05_database/07_exam_summary/412_cartesian_product/">Cartesian Product</a>)</strong>하여 N×M 행을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 연산이며, 조인 조건 없이 모든 가능한 조합을 만든다.
> 2. **가치**: 의도적 사용은 드물지만, <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/444_test_data_management/">테스트 데이터</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>·달력×시간대 조합·모든 조합 비교</strong> 등에 활용되며, 실수로 사용 시 행 폭발(100×100=[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000행)에 주의해야 한다.
> 3. **판단 포인트**: CROSS [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) + WHERE 조건 → 실질적으로 INNER JOIN과 동일하며, 의도적 Cartesian 외에는 <strong>반드시 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> 조건을 명시</strong>해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
CROSS JOIN: SELECT * FROM A CROSS JOIN B
  A(3행) × B(4행) = 12행 (모든 조합)
  용도: 달력×시간대, 색상×사이즈 조합 생성
```

- **📢 섹션 요약 비유**: CROSS JOIN은 <strong>뷔페에서 모든 메뉴 조합</strong>을 시도하는 것이다. 메뉴가 많으면 조합이 폭발한다.

---

## Ⅱ~Ⅴ. 결론

CROSS JOIN은 <strong>의도적 조합 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>에만 사용</strong>하고, 조건 없는 실수적 사용은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 재앙을 초래한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>CROSS <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 카테시안 곱 |
| **N×M** | 행 수 폭발 |
| <strong>INNER <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | CROSS + WHERE = INNER |
| <strong>조합 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong> | 달력×시간대 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 의도 외 사용 주의 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">관계 대수 Cartesian Product (이론)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">SQL CROSS JOIN (SQL-92)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">실무: 조합 생성 용도</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: LATERAL + GENERATE_SERIES — 효율적 조합 대안</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. CROSS JOIN은 <strong>모든 짝 만들기</strong>예요. 3명×4명 = <strong>12개 짝</strong>이 나와요.
2. 일부러 "모든 조합"이 필요할 때만 사용해요.
3. 실수로 사용하면 <strong>조합이 폭발(100만 행!)</strong>해서 컴퓨터가 느려져요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 136 / 600

← **이전**: [135. SQL Non-Equi JOIN & Self JOIN - 범위·자기 참조 결합](/knowledge-base/studynote/05_database/03_relational_model/135_sql_non_equi_join/)
**다음**: [137. SQL Self JOIN & Recursive CTE - 자기 참조와 재귀 쿼리](/knowledge-base/studynote/05_database/03_relational_model/137_sql_self_join_recursive/) →

---
