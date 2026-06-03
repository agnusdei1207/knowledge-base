---
title: 137. 자율주행 Level 3 조건부 자율 - 시스템 책임의 시작
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SAE Level 3는 **특정 ODD(운행 설계 영역) 내에서 시스템이 모든 주행 기능을 수행**하며, 시스템이 한계를 인식하면 운전자에게 **전환 요청(Takeover Request)**을 보내는 조건부 자율주행이다.
> 2. **가치**: L2와의 결정적 차이는 **법적 책임이 시스템에** 있다는 것이다. L3에서는 ODD 내에서 운전자가 **다른 활동(스마트폰 등)**을 할 수 있다.
> 3. **판단 포인트**: Mercedes Drive Pilot(고속도로 60km/h 이하)·Honda SENSING Elite가 최초 L3 양산이며, **Takeover 시간(최소 10초)**과 [[129_fallback|Fallback]](안전 정차) 설계가 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
L3: ODD 내 시스템 완전 제어 (Hands-free, Eyes-off)
  → 한계 인식 시: Takeover Request (10초+)
  → 운전자 무응답 시: Fallback (감속·정차)
  → 법적 책임: 시스템 (ODD 내)
```

- **📢 섹션 요약 비유**: L3는 **특정 구간 대리운전**이다. 정해진 구간에서만 맡기고, 구간 끝나면 운전자가 받는다.

---

## Ⅱ~Ⅴ. 결론

L3는 **자율주행 책임 전환의 분기점**이며, ODD 정의·Takeover·[[129_fallback|Fallback]] 설계가 기술·법적 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **L3** | 조건부 자율 |
| **ODD** | 운행 설계 영역 |
| **Takeover** | 전환 요청 |
| **[[129_fallback|Fallback]]** | 안전 정차 |
| **Mercedes Drive Pilot** | 최초 L3 양산 |

### 📈 관련 키워드 및 발전 흐름도

```text
[L2 ADAS (2015)] → [L3 Mercedes Drive Pilot (2023)]
    → [L3 Honda SENSING Elite (2021)]
    → [L3 ODD 확대 (고속도로→도심)]
    → [현재: L3→L4 전환 연구]
```

### 👶 어린이를 위한 3줄 비유 설명
1. L3는 **특정 구간 대리운전**이에요. 고속도로에서만 AI가 운전해요.
2. 구간이 끝나면 **"이제 운전해 주세요!"** 알려줘요(Takeover).
3. 운전자가 안 받으면 **자동으로 안전하게 멈춰요([[129_fallback|Fallback]])**!
