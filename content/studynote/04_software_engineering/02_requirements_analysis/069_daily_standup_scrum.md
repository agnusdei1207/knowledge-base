+++
title = "69. 데일리 스탠드업 (Daily Scrum) - 진행 상황 공유, 장애 파악"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데일리 스크럼은 매일 15분 내외로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 상황과 장애물을 공유하는 짧은 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 회의다.
> 2. **가치**: 팀의 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 상태를 빠르게 맞추고 장애를 조기에 발견한다.
> 3. **판단**: 관리 보고가 아니라 팀 내 협업과 오늘의 실행 계획이 목적이다.

---

## Ⅰ. 개요 및 필요성

매일 길게 회의할 필요는 없다. 대신 빠르게 상태를 맞추면 팀의 흐름이 좋아진다.

데일리 스크럼은 그런 짧은 점검용 회의다.

- **📢 섹션 요약 비유**: 아침마다 서로 어디까지 왔는지 짧게 말하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Yesterday / Today / Blockers
  ↓
Daily Scrum
  ↓
Team Synchronization
```

| 질문 | 의미 |
| :-- | :-- |
| 어제 한 일 | [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 상황 |
| 오늘 할 일 | 계획 |
| 장애물 | 방해 요소 |

데일리 스크럼은 보고서가 아니라 협업을 위한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)다. 그래서 빠르고 짧아야 한다.

- **📢 섹션 요약 비유**: 출발 전에 서로 방향을 맞추는 짧은 점검이다.

---

## Ⅲ. 비교 및 연결

| 회의 | 목적 | 길이 |
| :-- | :-- | :-- |
| Daily [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 짧음 |
| Planning | 계획 | 중간 |
| [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/) | 결과 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 중간 |
| Retro | 개선 | 중간 |

| 관점 | 의미 |
| :-- | :-- |
| Team-centric | 팀 중심 |
| Blocker [detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) | 장애 조기 발견 |

데일리 스크럼은 팀이 같은 궤도에 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 장치다.

- **📢 섹션 요약 비유**: 달리기 전에 서로 발맞춤을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 15분 내로 끝나는가?
2. 장애물이 드러나는가?
3. 팀원 간 협업에 초점이 있는가?
4. 관리 보고로 변질되지 않는가?
5. 매일 동일한 리듬을 유지하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 긴 회의가 되는 설계
- 관리자 보고용으로 변하는 설계
- 문제 해결보다 설명만 하는 설계
- 참석자만 많고 실질이 없는 설계

기술사 관점에서는 데일리 스크럼을 "상태 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 회의"로 봐야 한다.

- **📢 섹션 요약 비유**: 잠깐 모여서 오늘의 길을 맞추는 시간이다.

---

## Ⅴ. 기대효과 및 결론

데일리 스크럼은 작은 문제를 빨리 발견하게 해 주므로 팀의 흐름을 안정시킨다.

결론적으로 데일리 스크럼은 짧은 팀 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 회의다.

- **📢 섹션 요약 비유**: 오늘도 같은 방향으로 걷는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 시간이다.

---

## 관련 개념 맵

```text
Daily Scrum
  ↓
Blockers
  ↓
Synchronization
  ↓
Team Flow
```

---

## 관련 키워드 및 발전 흐름도

```text
Scrum
  ↓
Daily Scrum
  ↓
Impediment Removal
  ↓
Team Sync
```

---

## 어린이를 위한 3줄 비유 설명

아침에 짧게 이야기해요.
어디까지 왔는지 알려 줘요.
데일리 스크럼은 그런 점검이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 973

← **이전**: [68. 스프린트 계획 회의 (Sprint Planning)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/068_sprint_planning/)
**다음**: [70. 스프린트 리뷰 (Sprint Review) - 데모 및 피드백](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/070_sprint_review_demo/) →

---
