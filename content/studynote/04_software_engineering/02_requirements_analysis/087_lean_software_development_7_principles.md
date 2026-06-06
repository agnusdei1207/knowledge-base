---
title: "087. Lean Software Development 7 Principles"
tags:
  - "software_engineering"
---

## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: Lean (Lean Software Development)은 고객 가치에 직접 기여하지 않는 낭비를 줄여 흐름과 학습을 최대화하는 개발 방식이다.
    > 2. **가치**: 7대 원칙은 단순한 슬로건이 아니라, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·재작업·과잉기능을 줄이고 품질과 팀 자율성을 높이는 운영 규칙이다.
    > 3. **판단 포인트**: 린을 인원 감축으로 오해하면 실패하고, 가치 흐름과 피드백 속도를 관리하는 시스템으로 보면 효과가 분명해진다.

    ---

    ## Ⅰ. 개요 및 필요성

    Lean (Lean Software Development)은 Toyota Production System에서 나온 낭비 제거 철학을 소프트웨어에 적용한 것이다. 소프트웨어는 재고가 아니라 코드·요구사항·대기 작업이 쌓이는 순간 비용이 커지므로, 흐름이 막히면 바로 손실로 이어진다.

린이 필요한 이유는 요구사항이 자주 바뀌고, 학습이 곧 경쟁력이기 때문이다. 완성품을 크게 한 번에 만드는 방식보다, 작게 만들고 빨리 배우는 방식이 불확실성을 더 잘 흡수한다.

    - **📢 섹션 요약 비유**: 공부방에서 쓰지 않는 물건을 치우면 필요한 책이 바로 보이는 것과 같다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    7대 원칙은 하나의 흐름으로 연결된다.

| 원칙 | 핵심 행동 | 효과 |
| :-- | :-- | :-- |
| 낭비 제거 | 기다림, 재작업, 과잉 문서 축소 | 리드타임 감소 |
| 학습 증진 | 짧은 피드백과 실험 | 요구사항 이해 향상 |
| 결정 늦추기 | 불확실성이 줄 때까지 선택 보류 | 잘못된 확정 방지 |
| 빠른 인도 | 작은 배치로 자주 배포 | 시장 반응 확보 |
| 팀 권한 부여 | 현장 판단 확대 | 의사결정 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 감소 |
| 품질 내장 | 테스트·코드리뷰 자동화 | [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 전파 차단 |
| 전체 최적화 | 부분 효율보다 흐름 최적화 | 시스템 병목 제거 |

```text
고객 가치
    |
    v
작은 배치 개발 --► 빠른 피드백 --► 학습 강화
    |                                 |
    +------------► 품질 내장 ◄---------+
                    |
                    v
               흐름 개선 / 낭비 감소
```

Lean의 핵심은 "더 열심히"가 아니라 "더 늦지 않게 배우는 구조"를 만드는 데 있다.

    - **📢 섹션 요약 비유**: 작은 실험을 빨리 해 보고, 틀린 부분은 바로 고치는 탐구 수업 같은 방식이다.

    ---

    ## Ⅲ. 비교 및 연결

    Lean은 [Agile](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/), [Scrum](/studynote/04_software_engineering/uncategorized/969_agile_scrum_roles/), DevOps와 겹치지만 초점이 다르다.

| 구분 | 초점 | 대표 포인트 |
| :-- | :-- | :-- |
| Lean | 낭비 제거와 흐름 최적화 | 가치 흐름, WIP 제한 |
| [Agile](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) | 변화 수용과 반복 학습 | 짧은 반복, 고객 협업 |
| [Scrum](/studynote/04_software_engineering/uncategorized/969_agile_scrum_roles/) | 팀 운영 프레임 | [스프린트](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/), 백로그, 회고 |
| [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | 개발·운영 통합 | 자동화, 배포, 관측성 |

Lean은 Scrum의 규칙보다 더 넓은 경영·프로세스 관점에서 작동한다. 따라서 [칸반](/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) ([Kanban](/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/)) 보드나 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Continuous Delivery](/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) 자동화도 Lean의 실행 수단으로 연결될 수 있다.

    - **📢 섹션 요약 비유**: 먼저 다 만들고 나중에 고치기보다, 한 조각씩 보내며 방향을 확인하는 배달 방식이다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 먼저 가치 흐름을 보라. 요구사항 접수에서 배포까지 어디서 기다림이 생기는지 찾고, 승인 절차·배치 크기·테스트 자동화를 함께 줄여야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. WIP ([Work In Progress](/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/))를 제한해 대기열을 줄였는가?
2. 배포 전 수작업 검증을 자동화했는가?
3. 실패를 빨리 학습하는 회고 루프가 있는가?
4. 팀이 현장에서 결정을 내릴 권한을 갖는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- Lean을 인력 감축으로만 해석하는 것
- 린 보드만 만들고 배포 속도는 그대로인 것
- 부분 최적화 때문에 전체 흐름이 느려지는 것

    - **📢 섹션 요약 비유**: 부엌에서 한 접시씩 바로 내보내면 식탁이 빨리 차고, 남는 음식도 줄어든다.

    ---

    ## Ⅴ. 기대효과 및 결론

    Lean은 "많이 만드는 조직"보다 "빨리 배우는 조직"을 만든다. [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)과 대기를 줄이면 고객 가치 도달 시간이 짧아지고, 같은 인력으로 더 많은 학습이 가능해진다.

다만 린은 문서나 회의가 적다는 뜻이 아니다. 필요한 정보는 충분히 남기되, 가치에 기여하지 않는 낭비를 없애는 것이 핵심이다. 그래서 린은 절약이 아니라 설계의 문제로 기억해야 한다.

    - **📢 섹션 요약 비유**: 지저분한 방을 한 번에 다 고치기보다, 자주 정리해서 길을 막지 않게 하는 방법이다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| Toyota Production System | Lean의 기원 |
| WIP ([Work In Progress](/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/)) | 처리 중 작업 수 제한 |
| [Kanban](/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) | 흐름 시각화와 pull 방식 |
| [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Continuous Delivery](/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) | 작은 배치의 빠른 전달 |
| [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | 개발·운영 협업과 자동화 |

    ### 📈 관련 키워드 및 발전 흐름도

    낭비 제거
    |
    v
작은 배치와 pull 흐름
    |
    v
빠른 피드백과 학습
    |
    v
품질 내장과 전체 최적화

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 먹지 않는 간식은 책상에서 치워야 공부할 자리가 생겨요.
    2. 숙제도 한꺼번에 다 하기보다 조금씩 확인하면 덜 틀려요.
    3. 그래서 린은 낭비를 줄이고 빨리 배우는 공부법 같아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 87 / 973

<- **이전**: [86. 누적 흐름도 (CFD, Cumulative Flow Diagram)](/studynote/04_software_engineering/02_requirements_analysis/086_cumulative_flow_diagram_cfd/)
**다음**: [88. 가치 스트림 맵 (Value Stream Mapping)](/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/) ->

---
