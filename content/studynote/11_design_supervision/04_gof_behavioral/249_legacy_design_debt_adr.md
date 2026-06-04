---
title: "249. 레거시 설계 부채와 ADR (Legacy Design Debt & Architecture Decision Record)"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 레거시 시스템 (Legacy System) 의 [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/) ([Design Debt](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)) 는 과거의 빠른 의사결정이 현재와 미래의 유지보수 비용으로 돌아오는 복리 이자이며, [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) ([Architecture Decision Record](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/), 아키텍처 결정 기록) 은 그 의사결정을 가시화하고 맥락을 보존하는 문서 체계다.
> 2. **가치**: ADR을 통해 "왜 이렇게 만들었는가"를 추적 가능하게 함으로써 무분별한 변경을 막고, [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/) 청산의 우선순위를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반으로 결정할 수 있다.
> 3. **판단 포인트**: "이 코드를 변경하려는 사람이 원래 결정의 맥락을 알 수 있는가?" — No라면 ADR이 필요하다.

---

## Ⅰ. 개요 및 필요성
[워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 커닝햄 (Ward Cunningham) 이 1992년 제안한 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) ([Technical Debt](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)) 개념은 "빠른 해결책"이 장기적으로 초과 작업을 요구한다는 메타포다. [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/) ([Design Debt](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)) 는 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 중에서 <strong>아키텍처·설계 수준의 잘못된 결정</strong>에서 발생하는 부채를 가리킨다.

| 특성 | 설명 |
|:---|:---|
| 가시성 부족 | 코드 외부에서 부채 규모를 정량화하기 어려움 |
| 맥락 손실 | 원래 결정을 한 사람이 없거나 기억하지 못함 |
| 복합 이자 | 한 부채가 다른 부채를 유발하는 연쇄 효과 |
| 두려움 효과 | 변경 시 무엇이 깨질지 몰라 아무도 건드리지 않음 |

마이클 나이가드 (Michael Nygard) 가 2011년 제안한 ADR은 아키텍처 결정의 <strong>맥락 (<a href="/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a>), 결정 내용 (Decision), 결과 (Consequences)</strong> 를 간결한 문서로 기록하는 체계다.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 오래된 건물의 도면 없이 벽을 허물다가 내력벽을 건드리는 것 — ADR은 그 도면이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+------------------------------------------------------+
|  ADR-0012: 사용자 세션 관리에 JWT 채택               |
+------------------------------------------------------+
|  상태 (Status): Accepted                             |
|  날짜 (Date):   2023-03-15                           |
+------------------------------------------------------+
|  맥락 (Context)                                      |
|  - 기존 서버 세션 방식이 수평 확장(Scale-Out)에 장애  |
|  - 마이크로서비스 전환 예정                          |
+------------------------------------------------------+
|  결정 (Decision)                                     |
|  - JWT (JSON Web Token) 기반 무상태 인증 채택         |
|  - 토큰 만료 15분, 리프레시 토큰 7일                 |
+------------------------------------------------------+
|  결과 (Consequences)                                 |
|  + 서버 무상태화 -> 수평 확장 용이                    |
|  + 마이크로서비스 간 인증 전파 단순화                |
|  - 토큰 무효화(Revocation) 복잡도 증가               |
|  - 토큰 크기 증가로 요청 헤더 용량 증가             |
+------------------------------------------------------+
```

```
+-----------------------------------------------------+
|          설계 부채 우선순위 결정 매트릭스            |
|                                                     |
|  높은  |  즉시 청산  |  계획적 청산  |              |
|  영향  +-------------+---------------+              |
|        |  모니터링   |  수용/문서화  |              |
|  낮은  +-------------+---------------+              |
|                낮은 비용    높은 비용                |
+-----------------------------------------------------+
```

| 상태 | 의미 |
|:---|:---|
| Proposed | 검토 중인 결정 |
| Accepted | 채택된 결정 |
| Deprecated | 더 이상 권고하지 않음 |
| Superseded by [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/)-XXX | 다른 ADR로 대체됨 |

- **📢 섹션 요약 비유**: 회사 이사회 회의록처럼, ADR은 "왜 그때 그 결정을 했는가"를 나중에 확인할 수 있는 공식 기록이다.

---

## Ⅲ. 비교 및 연결
| 방법 | 목적 | 장점 | 단점 |
|:---|:---|:---|:---|
| [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 문서화 | 결정 맥락 보존 | 가볍고 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 용이 | 작성 규율 필요 |
| 아키텍처 다이어그램 | 구조 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 한눈에 파악 | 업데이트 누락 빈번 |
| [SonarQube](/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 지표 | 코드 수준 부채 정량화 | 자동화 측정 | 설계 수준 미반영 |
| 이벤트 스토밍 (Event Storming) | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 재설계 | 팀 공유 지식 | 시간·비용 소요 |

```
레거시 시스템 분석
    |
    +- 코드 스멜 탐지 (SonarQube)
    +- ADR 검토 (기존 결정 파악)
    |
    v
설계 부채 목록 작성
    |
    +- 우선순위 결정 (영향 × 비용)
    +- 신규 ADR 작성 (변경 결정 기록)
    |
    v
리팩토링 실행 (TDD 안전망 하에)
    |
    +- ADR 상태 업데이트 (Superseded)
```

- **📢 섹션 요약 비유**: 국가대표팀 감독 교체 시 전임 감독의 전술 노트가 있으면 선수들의 역할과 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 빠르게 파악할 수 있다 — ADR이 그 전술 노트다.

---

## Ⅳ. 실무 적용 및 기술사 판단
ADR은 **코드 저장소 (Repository) 와 함께** [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리되어야 한다.

```
project-root/
  docs/
    decisions/
      ADR-0001_use-postgresql.md
      ADR-0002_adopt-hexagonal-architecture.md
      ADR-0003_jwt-session-management.md (Superseded)
      ADR-0012_jwt-session-management-v2.md (Accepted)
```

도구: `adr-tools` (CLI), Confluence [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/), GitHub Wiki

레거시 시스템을 한 번에 교체하는 빅뱅 (Big Bang) 방식 대신, 마틴 파울러가 제안한 [스트랭글러 피그 패턴](/studynote/11_design_supervision/06_exam_summary/376_strangler_fig_summary/) ([Strangler Fig Pattern](/studynote/12_it_management/05_security_compliance/950_strangler_fig_pattern/)) 은 레거시를 점진적으로 새 시스템으로 교살하듯 대체한다. 각 교체 결정은 ADR로 문서화해 트레이드오프를 기록한다.

- <strong><a href="/studynote/11_design_supervision/02_architecture_principles/140_design_debt/">설계 부채</a> 정량화</strong>: SonarQube의 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 일수 + [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 위반 건수로 이중 측정
- **거버넌스 (Governance)**: [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 리뷰 프로세스를 아키텍처 거버넌스의 일환으로 제도화
- <strong>지식 경영 (Knowledge <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong>: 개인 지식을 조직 지식으로 전환하는 수단으로 [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 강조

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 단위를 작게 나눠 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 오래된 레시피 노트에 "왜 이 재료를 넣었는지" 이유가 적혀 있으면 수십 년 후 후계자도 레시피를 개선할 수 있다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 미사용 | [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 도입 |
|:---|:---:|:---:|
| 아키텍처 결정 이해 시간 (신입) | 2주 | 3일 |
| 잘못된 이유로 인한 [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 비율 | 30% | 5% |
| 아키텍처 지식 퇴직자 손실률 | 높음 | 낮음 (문서화) |
| [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/) 청산 우선순위 합의 시간 | 2주 | 1일 |

레거시 [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/) (Legacy [Design Debt](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)) 와 [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) ([Architecture Decision Record](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/)) 은 동전의 양면이다. 부채가 쌓이는 것을 막으려면 결정의 <strong>이유와 트레이드오프</strong>를 기록하고, 시간이 지나 그 결정이 부적합해졌을 때 <strong>새 ADR로 대체</strong>하는 순환 구조가 필요하다. 이는 기술 조직의 집단 기억 (Collective Memory) 을 코드베이스와 함께 성장시키는 실천이다.

확장 방향은 ① [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 자동화, ② 아키텍처 적합성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), ③ 작은 단위의 상시 [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 문화 정착이다.

- **📢 섹션 요약 비유**: 의료 차트에 모든 진단과 처방 이력이 기록되어야 다음 의사가 올바른 판단을 할 수 있다 — ADR은 소프트웨어 시스템의 의료 차트다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) ([Technical Debt](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)) | [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)는 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)의 하위 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 핵심 도구 | [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) ([Architecture Decision Record](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/)) | 결정 맥락 보존 문서 |
| 연관 개념 | 레거시 시스템 (Legacy System) | [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)의 주요 발생처 |
| 연관 개념 | [스트랭글러 피그 패턴](/studynote/11_design_supervision/06_exam_summary/376_strangler_fig_summary/) ([Strangler Fig Pattern](/studynote/12_it_management/05_security_compliance/950_strangler_fig_pattern/)) | 레거시 점진적 교체 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| 연관 개념 | [SonarQube](/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) | 코드 수준 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 정량화 |
| 연관 개념 | 아키텍처 거버넌스 ([Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) Governance) | [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) 리뷰 제도화 |
| 연관 개념 | 이벤트 스토밍 (Event Storming) | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 재설계 협업 기법 |

### 📈 관련 키워드 및 발전 흐름도
부채 가시화 -> 레거시 [설계 부채](/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)와 [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) -> [architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) governance

### 👶 어린이를 위한 3줄 비유 설명
1. 오래된 장난감 상자에 "왜 이 장난감을 샀는지" 메모가 없으면 엄마가 함부로 버릴 수 있다.
2. ADR은 "이 장난감은 비가 올 때만 쓰는 거야"라고 적어두는 메모지다.
3. 메모가 있으면 나중에 "이 장난감이 필요 없어졌나?"를 기준에 따라 결정할 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 310 / 530

<- **이전**: [248. 리팩토링 TDD 안전망 (Refactoring TDD Safety Net)](/studynote/11_design_supervision/04_gof_behavioral/248_refactoring_tdd_safety_net/)
**다음**: [250. 메시지 패싱과 위임 (Message Passing & Delegation)](/studynote/11_design_supervision/04_gof_behavioral/250_message_passing_delegation/) ->

---
