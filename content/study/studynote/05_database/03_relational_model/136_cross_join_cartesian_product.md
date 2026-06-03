---
title: 136. CROSS JOIN & Cartesian Product - 카테시안 곱 결합
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CROSS JOIN은 **두 테이블의 모든 행을 서로 조합([[412_cartesian_product|Cartesian Product]])**하여 N×M 행을 [[087_process_state_transition|생성]]하는 연산이며, 조인 조건 없이 모든 가능한 조합을 만든다.
> 2. **가치**: 의도적 사용은 드물지만, **[[444_test_data_management|테스트 데이터]] [[087_process_state_transition|생성]]·달력×시간대 조합·모든 조합 비교** 등에 활용되며, 실수로 사용 시 행 폭발(100×100=[[489_raid_10_hybrid|10]],000행)에 주의해야 한다.
> 3. **판단 포인트**: CROSS [[521_join|JOIN]] + WHERE 조건 → 실질적으로 INNER JOIN과 동일하며, 의도적 Cartesian 외에는 **반드시 [[521_join|JOIN]] 조건을 명시**해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
CROSS JOIN: SELECT * FROM A CROSS JOIN B
  A(3행) × B(4행) = 12행 (모든 조합)
  용도: 달력×시간대, 색상×사이즈 조합 생성
```

- **📢 섹션 요약 비유**: CROSS JOIN은 **뷔페에서 모든 메뉴 조합**을 시도하는 것이다. 메뉴가 많으면 조합이 폭발한다.

---

## Ⅱ~Ⅴ. 결론

CROSS JOIN은 **의도적 조합 [[087_process_state_transition|생성]]에만 사용**하고, 조건 없는 실수적 사용은 [[282_performance_tactics|성능]] 재앙을 초래한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CROSS [[521_join|JOIN]]** | 카테시안 곱 |
| **N×M** | 행 수 폭발 |
| **INNER [[521_join|JOIN]]** | CROSS + WHERE = INNER |
| **조합 [[087_process_state_transition|생성]]** | 달력×시간대 |
| **[[282_performance_tactics|성능]]** | 의도 외 사용 주의 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 대수 Cartesian Product (이론)]
    → [SQL CROSS JOIN (SQL-92)]
    → [실무: 조합 생성 용도]
    → [현재: LATERAL + GENERATE_SERIES — 효율적 조합 대안]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CROSS JOIN은 **모든 짝 만들기**예요. 3명×4명 = **12개 짝**이 나와요.
2. 일부러 "모든 조합"이 필요할 때만 사용해요.
3. 실수로 사용하면 **조합이 폭발(100만 행!)**해서 컴퓨터가 느려져요!