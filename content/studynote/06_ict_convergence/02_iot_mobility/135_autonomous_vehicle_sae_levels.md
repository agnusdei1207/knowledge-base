+++
title = "135. 자율주행 SAE 레벨 (Level 0~5) - 자율주행 단계 분류"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SAE J3016은 <strong>자율주행을 Level 0(비자동)~Level 5(완전 자율)의 6단계</strong>로 분류하는 국제 표준이며, Level 3(조건부 자율)부터 시스템이 주행의 주체가 된다.
> 2. **가치**: Level 2(ADAS)와 Level 3의 결정적 차이는 <strong>법적 책임의 주체</strong>이다. L2는 운전자, L3+는 시스템이 책임이며, 이 구분이 보험·법규·기술 요구사항을 완전히 바꾼다.
> 3. **판단 포인트**: 현재 양산 차량은 L2+(Tesla FSD, Hyundai HDA)~L3(Mercedes, Honda)이며, L4(Waymo, 특정 지역)가 상용화, L5(모든 조건)는 미달성이다.

---

## Ⅰ. 개요 및 필요성

```text
L0: 비자동 | L1: 운전 보조 | L2: 부분 자동 (운전자 감시)
L3: 조건부 자율 (시스템 책임, 요청 시 전환)
L4: 고도 자율 (특정 조건에서 완전 자율)
L5: 완전 자율 (모든 조건, 핸들 불필요)
```

- **📢 섹션 요약 비유**: L2는 조수석 도우미(운전자가 항상 봄), L3는 대리운전(특정 구간 맡김), L5는 무인택시이다.

---

## Ⅱ~Ⅴ. 결론

SAE 레벨은 <strong>자율주행 기술·법규·보험의 기준 프레임</strong>이며, L3→L4 전환이 현재 산업의 핵심 과제이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SAE L0~L5** | 자율주행 6단계 |
| **ADAS** | L1~L2 (운전 보조) |
| **ODD** | 운행 설계 영역 (L3+) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/141_v2x_vehicle_to_everything_communication/">V2X</a></strong> | 차량-인프라 통신 |
| **Waymo** | L4 로보택시 |

### 📈 관련 키워드 및 발전 흐름도

```text
[L1 크루즈컨트롤 (2000s)] → [L2 ADAS (Tesla AP, 2015)]
    → [L3 조건부 자율 (Mercedes, 2023)]
    → [L4 로보택시 (Waymo, 2024)]
    → [현재: L5 연구 — 범용 자율주행 (미달성)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. L2는 <strong>조수석 도우미</strong>예요. 도와주지만 **운전자가 항상 봐야** 해요.
2. L4는 <strong>특정 구간 무인택시</strong>예요. 정해진 곳에서 **혼자 달려요**.
3. L5는 <strong>어디든 혼자 가는 완전 무인차</strong>예요. 아직 만들어지지 않았어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 552

← **이전**: [134. 메타버스 & 가상 현실 경제 - 디지털 세계의 경제 생태계](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/134_metaverse_virtual_reality_economy/)
**다음**: [136. 자율주행 Level 2 ADAS - 운전 보조의 현재와 한계](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/136_autonomous_vehicle_level_2_adas/) →

---
