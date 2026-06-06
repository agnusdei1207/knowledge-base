---
title: "Acceptance Criteria vs Definition of Done"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/)([Acceptance Criteria](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/))는 <strong>개별 스토리의 비즈니스 요구사항 충족 조건</strong>이고, DoD(Definition of Done)는 <strong>모든 스토리에 공통 적용되는 품질·프로세스 완료 기준</strong>이다.
> 2. **가치**: AC만 있으면 "기능은 작동하지만 테스트·[코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/)·배포 준비가 안 된" 상태가 발생하고, DoD만 있으면 "프로세스는 통과했지만 비즈니스 요건을 충족하지 못한" 결과가 나온다. 둘 다 필요하다.
> 3. **판단 포인트**: AC는 PO가 정의(스토리별 다름), DoD는 팀이 합의(전체 공통)하며, 스토리가 "Done"이 되려면 <strong>AC와 DoD 모두 충족</strong>해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
AC (스토리별): "올바른 비밀번호로 로그인 시 대시보드 표시"
DoD (전체 공통): 코드 리뷰 완료, 단위 테스트 80%+, CI 통과, 배포 가능
-> Done = AC ✅ + DoD ✅
```

- **📢 섹션 요약 비유**: AC는 요리의 **레시피(이 요리의 맛 조건)**, DoD는 <strong>위생 기준(모든 요리의 공통 규칙)</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | [AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/) | DoD |
|:---|:---|:---|
| **범위** | 개별 스토리 | **전체 공통** |
| **정의자** | PO | **팀 합의** |
| **내용** | 비즈니스 조건 | **품질·프로세스** |
| **형식** | Given/When/Then | [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) |

---

## Ⅲ~Ⅴ. 결론

[AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/)+DoD는 <strong>Agile에서 "완료"의 의미를 명확히 하는 두 축</strong>이며, 둘 다 충족해야 진정한 Done이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/">AC</a></strong> | 스토리별 비즈니스 조건 |
| **DoD** | 전체 공통 품질 기준 |
| <strong><a href="/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/">BDD</a></strong> | AC를 Given/When/Then으로 표현 |
| **DoR** | 스토리 시작 준비 조건 |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/">Sprint Review</a></strong> | [AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 시점 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 완료 기준 (~2005)] -> [DoD 표준화 (Scrum Guide, 2010)]
    -> [AC + DoD 분리 (2015~)]
    -> [BDD로 AC 자동화 (2018~)]
    -> [현재: AI AC 생성 — 요구사항->AC 자동 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. AC는 <strong>요리 레시피(맛 조건)</strong>예요. "이 케이크는 딸기맛이어야 해!"
2. DoD는 <strong>위생 기준</strong>이에요. "모든 요리는 깨끗한 주방에서, 유통기한 내 재료로!"
3. 레시피([AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/))와 위생(DoD) <strong>둘 다 통과</strong>해야 손님에게 낼 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 973

<- **이전**: [129. Spike (스파이크) - Agile 기술 불확실성 해소 탐구](/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/)
**다음**: [131. 요구사항 공학 (Requirements 엔진ering) - 체계적 요구 수집·분석·관리](/studynote/04_software_engineering/03_design_architecture/131_requirements_engineering/) ->

---
