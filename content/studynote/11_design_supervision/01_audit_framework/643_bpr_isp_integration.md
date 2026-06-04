+++
title = "643. BPR/ISP 연계 - 구축된 시스템이 당초 전략적 목표(AS-IS 대비 TO-BE 효과)를 달성했는지 사후 평가"

[taxonomies]
tags = ["design_supervision"]

[extra]
tags = ["design_supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/) ([Business Process Reengineering](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/))과 [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) (Information [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Planning)는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 프로세스, 시스템을 한 줄로 묶어야 사후 효과를 검증할 수 있다.
> 2. **가치**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)만 있고 재설계가 없으면 시스템은 기존 업무를 전산화하는 데 그치므로 개선 효과가 작다.
> 3. **판단 포인트**: 기술사는 구축 완료가 아니라 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) ([Key Performance Indicator](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/020_kpi/))와 추적성으로 [AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 대비 TO-BE 성과를 증명해야 한다.

---

## Ⅰ. 개요 및 필요성

BPR과 ISP는 모두 기업 변화를 다루지만 역할이 다르다. ISP는 목표 아키텍처와 투자 우선순위를 정하고, BPR은 그 목표에 맞게 핵심 업무를 다시 설계한다.
두 작업이 분리되면 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 문서는 멋있지만 현업은 그대로인 상태가 되기 쉽다. 그래서 시스템 구축 뒤에는 사후평가로 원래 목표가 실제로 달성됐는지 확인해야 한다.
```text
+----------------------------------------------+
| 전략 목표 -> ISP -> BPR -> 시스템 구축 -> KPI 검증 |
+----------------------------------------------+
| AS-IS 업무 ---> TO-BE 업무 ---> 데이터/화면/권한 정렬 |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 설계 전에 방향을 맞추지 않으면 구축 후에는 원래 문제로 되돌아간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ISP는 비전, 응용, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 인프라 방향을 내놓고, BPR은 업무 순서와 승인·예외 규칙을 바꾼다. 둘이 같은 목표 문구와 지표를 공유해야 요구사항 추적표가 흔들리지 않는다.
즉, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 문서가 설계 문서와 따로 놀지 않도록 사업 목표 -> 프로세스 변경 -> 화면/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구현이 한 묶음으로 내려와야 한다.
| 구분 | 역할 | 판단 포인트 |
| --- | --- | --- |
| [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) | 목표 아키텍처와 로드맵 수립 | 범위와 투자 우선순위를 정한다 |
| [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/) | 핵심 업무 재설계 | 승인·역할·예외 규칙을 바꾼다 |
| 시스템 구축 | 기능·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·권한 구현 | 설계와 실행이 일치해야 한다 |
| 사후평가 | 성과 측정과 보완 과제 도출 | KPI와 실제 효과를 비교한다 |

- **📢 섹션 요약 비유**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 재설계, 구현, 검증이 한 체인으로 이어져야 한다.

---

## Ⅲ. 비교 및 연결

ISP는 "어디로 갈 것인가"를, BPR은 "어떻게 일할 것인가"를 정한다. [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/806_ea_enterprise_architecture/))와 [PMO](/knowledge-base/studynote/04_software_engineering/01_overview_principles/059_pmo_project_management_office/) ([Project Management Office](/knowledge-base/studynote/04_software_engineering/01_overview_principles/059_pmo_project_management_office/))는 이 둘을 실행 가능한 구조로 묶는다.
[BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/) 없는 시스템은 업무 자동화에 머무르고, [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) 없는 BPR은 전사 투자 순서가 흔들린다. 반대로 둘이 연결되면 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)와 경영 보고가 같은 지표를 볼 수 있다.
| 기준 | [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) | [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/) | 시스템 구축 |
| --- | --- | --- | --- |
| 초점 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 구조 | 업무와 통제 | 기능과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 산출물 | 로드맵·표준·원칙 | 업무 절차·역할 | 화면·인터페이스·DB |
| 실패 시 | 방향 상실 | 비효율 자동화 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 미반영 |

- **📢 섹션 요약 비유**: ISP는 방향, BPR은 방법, EA와 PMO는 연결 장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 처리 시간, 재작업률, 오류율, 승인 단계 수, 사용자 채택률로 효과를 본다. [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 관점에서는 경영 목표 -> 프로세스 변경 -> 기능 구현 -> 결과 보고서의 연결이 끊기지 않아야 한다.
또한 사업 책임자와 프로세스 오너가 분리되지 않아야 하고, 변경된 업무가 교육과 운영 규정에 반영돼야 한다.
### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현행([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/))과 목표(TO-BE)의 차이가 수치로 설명되는가?
2. 요구사항이 프로세스와 화면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 추적되는가?
3. 구축 후 KPI가 실제로 개선됐는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 시스템부터 먼저 사는 "툴 우선" 접근
- 사후평가 없이 완료 보고만 하는 방식

- **📢 섹션 요약 비유**: 숫자와 추적성으로 효과를 보여주지 못하면 개선이 아니다.

---

## Ⅴ. 기대효과 및 결론

통합된 [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/)/ISP는 투자와 운영을 함께 설계하게 해 정량적 효과를 남긴다. 그래서 문서가 아니라 변화의 증거가 조직 안에 남는다.
앞으로는 일회성 문서보다 [Process Mining](/knowledge-base/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)([프로세스 마이닝](/knowledge-base/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/))과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 개선을 연결하는 방식이 중요해진다.
기술사는 이 주제를 "계획과 실행, 효과 검증을 하나로 묶는 거버넌스"로 기억하면 된다.

- **📢 섹션 요약 비유**: 변화를 만든다는 말보다 변화를 증명하는 구조가 더 중요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 목표와 로드맵을 정리한다 |
| [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/911_bpr_business_process_reengineering_radical_redesign/) | 핵심 업무와 통제 흐름을 재설계한다 |
| [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) | 사업·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·기술 구조를 정렬한다 |
| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) | 성과 달성 여부를 수치로 확인한다 |
| [PMO](/knowledge-base/studynote/04_software_engineering/01_overview_principles/059_pmo_project_management_office/) | 일정·범위·변경을 통제한다 |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | 목표와 결과의 증빙을 확인한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
경영 목표
  |
  v
ISP (전략/로드맵)
  |
  v
BPR (프로세스 재설계)
  |
  v
시스템 구축
  |
  v
사후평가 -> 개선 과제
```

### 👶 어린이를 위한 3줄 비유 설명

1. 학교가 교실을 새로 짓기 전에 먼저 시간표와 규칙부터 다시 정하는 것과 같다.
2. 그다음 책상 배치와 수업 흐름을 바꾸면, 새 건물도 진짜 편해진다.
3. 마지막에 시험 점수와 만족도를 보면, 바꾼 일이 정말 도움이 됐는지 알 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 530

<- **이전**: [78. BPR/ISP 연계 사후 평가 (BPR/ISP Alignment Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/078_bpr_isp_alignment_audit/)
**다음**: [79. 개발자 클린룸 망분리(VDI) 환경 및 보안 이동 경로 점검 (Security)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/) ->

---
