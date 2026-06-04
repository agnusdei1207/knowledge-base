+++
title = "31. 소프트웨어 유지보수 유형 — 4가지 변경 분류"
date = 2026-04-29

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 유지보수(Software Maintenance)는 ISO/IEC 14764에 따라 수정([Corrective](/knowledge-base/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/))·적응(Adaptive)·완전화(Perfective)·예방(Preventive)의 4가지 유형으로 분류된다. 운영 중인 소프트웨어에 가해지는 모든 변경이 이 네 유형 중 하나다.
> 2. **가치**: 현실에서 유지보수가 전체 소프트웨어 비용의 60~80%를 차지한다. 유지보수 유형 분류는 변경 요청(Change Request)의 우선순위·자원 배분·[SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) 결정의 기준이 된다.
> 3. **판단 포인트**: 완전화 유지보수(Perfective)가 실제 비용의 가장 큰 비중(약 50%)을 차지한다. 사용자 요구 기능 추가·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선이 버그 수정보다 더 많은 자원을 소모한다.

---

## Ⅰ. 개요 및 필요성

```text
유지보수 4유형:

  수정(Corrective):    버그·결함 수정
  적응(Adaptive):      환경 변화 대응 (OS 업그레이드, 법 개정)
  완전화(Perfective):  기능 추가·성능 개선 (요구사항 진화)
  예방(Preventive):    미래 결함 방지 (리팩토링·문서화)

비용 비율 (일반적):
  완전화: ~50%
  적응:   ~25%
  수정:   ~21%
  예방:   ~4%
```

- **📢 섹션 요약 비유**: 유지보수 4유형은 자동차 관리 유형이다. 고장 수리(수정), 배출가스 규제 맞추기(적응), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝(완전화), 정기 점검(예방)으로 모든 차량 관리 활동을 분류할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 유지보수 유형 상세

| 유형 | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | 예시 |
|:---|:---|:---|
| **수정** | [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 발견 | NullPointer 오류 수정, SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/) 패치 |
| **적응** | 환경 변화 | Java 17 마이그레이션, [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 법 개정 반영 |
| **완전화** | 사용자 요청 | 검색 필터 추가, 응답 속도 개선 |
| **예방** | [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) | 레거시 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/), 코드 문서화 |

### 변경 [관리 프로세스](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/018_admin_processes/)

```text
변경 요청(CR) 제출
    |
    v
영향 분석 (Impact Analysis)
    +- 변경 범위 파악
    +- 리스크 평가
    +- 비용·일정 추정
    |
    v
변경 승인위원회(CCB: Configuration Change Board)
    |
    v
구현 -> 테스트 -> 배포
    |
    v
구성 관리 시스템 업데이트
```

- **📢 섹션 요약 비유**: [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 아파트 공사 허가다. 벽에 못 하나 박는 것도(작은 변경) 관리실([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/)) 신고 절차가 있고, 벽 철거(큰 변경)는 더 엄격한 허가가 필요하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수정 | 적응 | 완전화 | 예방 |
|:---|:---|:---|:---|:---|
| 긴급도 | 높음 | 중간 | 낮음 | 낮음 |
| 비용 | 낮음 | 중간 | 높음 | 중간 |
| [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 즉시~24시간 | 계획 | 릴리즈 주기 | 백로그 |
| 발생 빈도 | 지속적 | 주기적 | 요청 시 | 계획 시 |

- **📢 섹션 요약 비유**: 4유형 우선순위는 병원 응급실 분류다. 수정(응급실 즉시 처치), 적응(예약 진료), 완전화(선택 수술), 예방(건강 검진) 순으로 긴급도와 우선순위가 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)([Maintainability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)) 향상 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```text
코드 품질:
  - 높은 응집도(Cohesion)·낮은 결합도(Coupling)
  - 명확한 모듈 경계
  - 테스트 커버리지 > 80%

문서화:
  - 아키텍처 결정 기록 (ADR, Architecture Decision Record)
  - API 문서 (OpenAPI Spec)
  - 변경 이력 (CHANGELOG)

자동화:
  - CI/CD: 회귀 테스트 자동화
  - 모니터링: 결함 자동 감지·알림
  - 의존성: 자동 업데이트 (Dependabot)
```

- **📢 섹션 요약 비유**: [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/) 향상은 정리정돈된 집 관리다. 물건 정리([응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)·[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)), 라벨 부착(문서화), 청소 자동화([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD)로 집(소프트웨어)을 쉽게 관리할 수 있게 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **비용 관리** | 유형별 자원 배분 최적화 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 준수</strong> | 유형별 대응 시간 차별화 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a> 관리</strong> | 예방 유지보수로 장기 품질 유지 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 유지보수가 등장하고 있다. GitHub Copilot·Amazon CodeWhisperer가 버그 자동 수정을 제안하고, Dependabot이 의존성 자동 업데이트 PR을 생성하며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 코드 리뷰가 예방 유지보수를 자동화하는 방향으로 발전하고 있다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동 유지보수는 스마트 홈 자동 수리 시스템이다. AI가 집(코드)의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 감지하고 수리 방법을 제안하며, 법 개정(환경 변화)에 맞춘 자동 적응까지 처리하는 미래가 오고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ISO/IEC 14764** | 유지보수 4유형 표준 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/">변경 관리</a> (<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a>)</strong> | 유지보수 변경 승인 프로세스 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a></strong> | 예방 유지보수의 대상 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a></strong> | 유형별 대응 시간 기준 |
| **Dependabot** | 적응 유지보수 자동화 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[소프트웨어 유지보수 — 전체 비용의 60~80%]
    |
    v
[4유형 분류 — 수정/적응/완전화/예방 (ISO 14764)]
    |
    v
[변경 관리 (CCB) — 체계적 변경 승인 프로세스]
    |
    v
[유지보수성 향상 — 응집도·결합도·테스트 자동화]
    |
    v
[AI 자동 유지보수 — 결함 자동 감지·수정 제안]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 소프트웨어 유지보수는 자동차 관리처럼 4가지 유형이 있어요 — 고장 수리·환경 대응·기능 추가·예방 점검이에요!
2. 소프트웨어를 만드는 것보다 유지하는 비용이 더 크다는 것을 알고 계셨나요? (전체 비용의 60~80%!)
3. AI가 버그를 자동으로 찾아서 수정 방법을 제안해주는 시대가 되고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 973

<- **이전**: [30. 소프트웨어 재사용과 CBD — Component Based Development](/knowledge-base/studynote/04_software_engineering/01_overview_principles/030_software_reuse_cbd/)
**다음**: [소프트웨어 노후화 (Software Obsolescence)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/032_software_obsolescence/) ->

---
