+++
title = "243. 코드 스멜 진단 (Code Smell Diagnosis)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) ([Code Smell](/knowledge-base/studynote/12_it_management/05_security_compliance/365_5_solid_code_smell/)) 은 설계 문제를 암시하는 코드 패턴으로, 버그는 아니지만 미래의 버그·유지보수 비용을 예고하는 경고 신호다.
> 2. **가치**: 스멜을 명명하고 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)함으로써 팀이 공통 언어로 설계 문제를 논의하고 우선순위를 정해 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) ([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)) 로드맵을 수립할 수 있다.
> 3. **판단 포인트**: "이 코드를 처음 보는 개발자가 10분 안에 이해할 수 있는가?" — No라면 스멜을 찾아야 한다.

---

## Ⅰ. 개요 및 필요성
마틴 파울러 (Martin Fowler) 와 켄트 벡 (Kent Beck) 이 체계화한 개념으로, "코드에서 나는 나쁜 냄새"를 의미한다. 스멜은 그 자체가 결함은 아니지만, <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/">리팩토링</a>이 필요함을 나타내는 표면적 지시자</strong>다.

| # | 스멜 이름 | 한국어 | 핵심 증상 |
|:---:|:---|:---|:---|
| 1 | Long Method | 롱 메서드 | 메서드 길이 과도 (20줄+) |
| 2 | Large Class | 라지 클래스 | 클래스가 너무 많은 책임 담당 |
| 3 | Primitive Obsession | 프리미티브 강박 | 원시 타입으로 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 개념 표현 |
| 4 | Shotgun Surgery | 샷건 수술 | 변경 1개에 수십 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 필요 |
| 5 | Feature Envy | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔비 | 메서드가 다른 클래스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 집착 |

스멜을 방치하면 <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">Technical Debt</a>)</strong> 가 복리로 쌓인다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 발견 시 수정 비용 대비 후기 발견 시 수정 비용은 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 차이가 난다고 알려져 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Problem</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Core Idea</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Expected Gain</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 냄새나는 음식은 먹으면 탈이 나기 전에 버려야 한다 — [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)도 버그가 터지기 전에 제거해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">코드 스멜 분류 체계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스멜 유형</div><div class="kb-diagram-cell">영향 범위</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Long Method</div><div class="kb-diagram-cell">단일 메서드 내부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Large Class</div><div class="kb-diagram-cell">단일 클래스 내부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Primitive</div><div class="kb-diagram-cell">타입 시스템 전체</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Obsession</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Shotgun Surgery</div><div class="kb-diagram-cell">시스템 전체 (변경 시 파급 효과)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Feature Envy</div><div class="kb-diagram-cell">클래스 간 의존 관계</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">피처 엔비 (Feature Envy) 예시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Order</div><div class="kb-diagram-cell">Customer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- name</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">printLabel()</div><div class="kb-diagram-cell">──많이──▶</div><div class="kb-diagram-cell">- address</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(이 메서드가</div><div class="kb-diagram-cell">접근</div><div class="kb-diagram-cell">- postalCode</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Customer</div><div class="kb-diagram-cell">- country</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터에</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">집착)</div></div>
<div class="kb-diagram-note">→ printLabel()을 Customer로 이동해야 함</div>
</div>
</div>



**① 롱 메서드 (Long Method)**
- 진단: 메서드 길이 > 20줄, 들여쓰기 > 3단
- 처방: 메서드 분리 (Extract Method)

**② 라지 클래스 (Large Class)**
- 진단: 필드 > 10개, 메서드 > 20개, 2000줄+
- 처방: 클래스 분리 (Extract Class), 인터페이스 추출 (Extract Interface)

**③ 프리미티브 강박 (Primitive Obsession)**
- 진단: `String`으로 전화번호·통화·상태 표현, `int`로 금액 표현
- 처방: 값 객체 (Value Object) 도입

**④ 샷건 수술 (Shotgun Surgery)**
- 진단: 기능 1개 변경 시 10개+ 클래스 수정 필요
- 처방: 메서드 이동 (Move Method), 클래스 합병 (Inline Class)

<strong>⑤ <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 엔비 (Feature Envy)</strong>
- 진단: 메서드 내 다른 클래스 getter 5회+ 연속 호출
- 처방: 메서드 이동 (Move Method), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 행동을 같은 클래스로

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 의사가 X레이를 보며 "이건 폐렴 징후, 이건 골절 징후"라고 판단하듯, [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)도 각각 고유한 '증상 패턴'으로 진단한다.

---

## Ⅲ. 비교 및 연결
| [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) | 핵심 처방 | 보조 처방 | 영향 원칙 |
|:---|:---|:---|:---|
| 롱 메서드 (Long Method) | 메서드 분리 (Extract Method) | 조건부 분리 | [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/), [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) |
| 라지 클래스 (Large Class) | 클래스 분리 (Extract Class) | 슈퍼클래스 분리 | [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/) |
| 프리미티브 강박 (Primitive Obsession) | 값 객체 도입 | 타입 코드 교체 | 표현력, 타입 안전 |
| 샷건 수술 (Shotgun Surgery) | 메서드/필드 이동 | 클래스 합병 | [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) ([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)) |
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔비 (Feature Envy) | 메서드 이동 (Move Method) | 함수 추출 후 이동 | [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/), [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">프리미티브 강박</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 클럼프 (Data Clumps) ──▶ 라지 클래스</div>
<div class="kb-diagram-note">파라미터 목록 과다 ▶ 롱 메서드</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">샷건 수술 / 피처 엔비</div>
</div>
</div>



- **📢 섹션 요약 비유**: 감기→폐렴→패혈증처럼 스멜도 방치하면 연쇄 악화한다 — [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 잡는 것이 최선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
[정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구 ([Static Analysis](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) Tool) 를 활용하면 [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)을 자동 탐지할 수 있다.

| 도구 | 언어 | 주요 탐지 스멜 |
|:---|:---|:---|
| [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) | 다국어 | 복잡도, 중복, [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) |
| PMD | Java | 롱 메서드, 복잡 조건 |
| Checkstyle | Java | 명명 규칙, 길이 |
| ESLint | JavaScript | 복잡도, 미사용 변수 |
| Pylint | Python | 복잡도, 스타일 |

- [ ] 메서드 길이 20줄 이하인가?
- [ ] 클래스당 책임이 1개인가 ([SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/) 검토)?
- [ ] 원시 타입으로 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 개념을 표현하지 않는가?
- [ ] 변경 시 영향 범위가 최소화되어 있는가?
- [ ] 메서드가 소속 클래스의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주로 사용하는가?

기술사 논술에서 [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) 진단 도구 ([SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/)) 도입 → 스멜 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) → 우선순위 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 로드맵 → [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 감소 정량화 순서로 서술하면 체계적인 답안이 완성된다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 단위를 작게 나눠 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 건강 검진 결과지에서 "고혈압 위험", "당뇨 전단계"를 보고 식단 조절 계획을 세우듯, [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) 리포트로 코드 개선 로드맵을 세운다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | 제거 전 | 제거 후 |
|:---|:---:|:---:|
| 순환 복잡도 (Cyclomatic Complexity) 평균 | 18.4 | 4.2 |
| 코드 중복률 | 23% | 5% |
| 클래스 평균 라인 수 | 650줄 | 180줄 |
| 빌드 후 발생 버그 수 (월) | 12건 | 3건 |

[코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) 진단 ([Code Smell](/knowledge-base/studynote/12_it_management/05_security_compliance/365_5_solid_code_smell/) Diagnosis) 은 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 <strong>나침반</strong>이다. 스멜 없이는 무엇을, 어디서, 왜 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)해야 하는지 논증할 수 없다. 팀이 스멜 어휘를 공유하면 코드 리뷰가 감정이 아닌 **객관적 기준** 위에 서게 되고, [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 관리가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반으로 전환된다.

확장 방향은 ① [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 자동화, ② 아키텍처 적합성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), ③ 작은 단위의 상시 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 문화 정착이다.

- **📢 섹션 요약 비유**: 미세먼지 농도 수치 없이 "오늘 공기 나쁜 것 같다"고 말하는 것과, PM2.5 150µg/m³ 수치를 근거로 "마스크 착용 필요"라고 말하는 것의 차이 — [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) 이름이 그 측정 수치다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) ([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)) | 스멜 제거의 수단 |
| 상위 개념 | [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) ([Technical Debt](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)) | 스멜 누적의 거시적 결과 |
| 하위 개념 | 롱 메서드 (Long Method) | 가장 흔한 스멜 1위 |
| 하위 개념 | 라지 클래스 (Large Class) | [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/) 위반의 전형 |
| 하위 개념 | 프리미티브 강박 (Primitive Obsession) | 타입 시스템 오남용 |
| 하위 개념 | 샷건 수술 (Shotgun Surgery) | 낮은 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 증상 |
| 하위 개념 | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔비 (Feature Envy) | 잘못된 클래스 배치 |
| 도구 | [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) | 스멜 자동 탐지 도구 |

### 📈 관련 키워드 및 발전 흐름도
[정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 지표 → [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/) 진단 → [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 우선순위

### 👶 어린이를 위한 3줄 비유 설명
1. 방이 지저분하면 "장난감이 여기저기", "옷이 바닥에", "책상 위에 뭔지 모를 것들" 처럼 문제 유형을 이름 붙여야 어디부터 치울지 알 수 있다.
2. [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)도 이름을 붙이면 "롱 메서드 먼저, 그 다음 라지 클래스" 순서로 정리할 수 있다.
3. 냄새를 맡을 줄 아는 코드 탐정이 되면 문제가 커지기 전에 예방할 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 304 / 530

← **이전**: [242. 파라미터 객체화 (Introduce Parameter Object)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/242_introduce_parameter_object/)
**다음**: [244. 데이터 클럼프 리팩토링 (Data Clumps Refactoring)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/244_data_clumps_refactoring/) →

---
