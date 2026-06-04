+++
title = "114. 피처 플래그 (Feature Flag/Toggle) - 배포와 릴리즈 분리·다크 런칭"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)([Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/))는 코드에 <strong>if/else <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>를 삽입</strong>하여, 배포(Deploy)와 릴리즈(Release)를 분리하고 <strong>런타임에 기능 ON/OFF를 즉시 전환</strong>할 수 있게 하는 소프트웨어 배포 전략이다.
> 2. **가치**: 코드는 이미 프로덕션에 배포되었지만 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)가 OFF이므로 사용자에게 보이지 않는 <strong>다크 런칭(<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/197_dark_launching_traffic_shadow/">Dark Launching</a>)</strong>이 가능하며, 문제 발생 시 <strong>코드 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 없이 <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/">플래그</a>만 OFF</strong>하면 즉시 무력화된다.
> 3. **판단 포인트**: Release Toggle(단기)·Experiment Toggle(A/B 테스트)·Ops Toggle(운영 제어)·Permission Toggle(사용자별 기능 제한)의 <strong>4가지 유형</strong>을 구분하고, 사용 후 반드시 제거하여 <strong>토글 부채(Toggle Debt)</strong>를 방지해야 한다.

---

## Ⅰ. 개요 및 필요성

새 결제 시스템을 개발 완료했지만, 모든 사용자에게 한 번에 공개하기 두렵다. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)로 **사내 직원 10명에게만 ON** -> [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> <strong>1% <a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a></strong> -> <strong>100% 릴리즈</strong>로 점진 공개할 수 있다.

```text
+-------------------------------------------------------+
|    피처 플래그 = 배포 ≠ 릴리즈                         |
+-------------------------------------------------------+
|  [기존] 배포 = 릴리즈 (동시에 전체 공개)              |
|         문제 시 -> 코드 롤백 (5~30분)                  |
|                                                       |
|  [피처 플래그] 배포 ≠ 릴리즈                          |
|   1. 코드 배포 (Flag OFF -> 아무도 안 보임)            |
|   2. 사내 직원에게 ON -> 검증                          |
|   3. 1% 사용자 ON -> 카나리 검증                      |
|   4. 100% ON -> 전체 릴리즈                           |
|   5. 문제 시 -> Flag OFF (1초, 롤백 불필요)            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 극장 무대의 <strong>조명 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a></strong>다. 배우(코드)는 이미 무대에 서 있지만, 조명을 켜야([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) ON) 관객(사용자)에게 보인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4가지 토글 유형

| 유형 | 수명 | 용도 | 예 |
|:---|:---|:---|:---|
| **Release Toggle** | 단기 (배포~릴리즈) | 미완성 기능 숨기기 | 신규 결제 시스템 |
| **Experiment Toggle** | 중기 (A/B 테스트) | 두 변형 비교 실험 | 버튼 색상 A/B |
| **Ops Toggle** | 장기 (운영) | 부하 시 기능 차단 | 추천 엔진 OFF |
| **Permission Toggle** | 영구 | 사용자별 기능 제한 | 프리미엄 전용 기능 |

### [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 도구

| 도구 | 유형 | 특징 |
|:---|:---|:---|
| **LaunchDarkly** | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) | 타겟팅·A/B·실시간 |
| **Unleash** | [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 자체 호스팅, 무료 |
| **Flagsmith** | [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)/[SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) | 멀티플랫폼 |

- **📢 섹션 요약 비유**: Release Toggle은 영화 개봉 전 시사회 초대권이고, Experiment Toggle은 신메뉴 시식 이벤트며, Ops Toggle은 비상시 전원 차단기다.

---

## Ⅲ. 비교 및 연결

| 비교 | 코드 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) OFF |
|:---|:---|:---|
| **속도** | 5~30분 (빌드+배포) | <strong>1초 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 호출)</strong> |
| **범위** | 전체 코드 | 해당 기능만 |
| **위험** | 다른 기능 영향 가능 | **해당 기능만 비활성** |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 상태 복원 어려움 | 코드 그대로, [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)만 OFF |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 토글 부채 (Toggle Debt) 방지
1. <strong>만료일 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: Release Toggle에 2주 만료일 지정, 자동 알림.
2. **정기 정리**: 분기별 "[Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 대청소" [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/).
3. **문서화**: 각 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)의 목적·소유자·만료일을 레지스트리에 기록.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>50개 이상 <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/">플래그</a> 방치</strong>: 코드 분기 폭발 -> 테스트 경우의 수 $2^{50}$ -> 유지보수 불가.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 미사용 | [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 사용 | 개선 |
|:---|:---|:---|:---|
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도 | 5~30분 | **1초** | 99% 단축 |
| 릴리즈 자신감 | 낮음 (빅뱅) | **높음 (점진적)** | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 감소 |
| A/B 테스트 | 별도 인프라 | <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/">플래그</a>로 즉시</strong> | 실험 가속 |

[피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 Trunk-based Development의 핵심 조력자이며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 롤아웃([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 분석 + 자동 [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) ON/OFF)과 결합하여 자율 릴리즈 시스템으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>다크 런칭 (<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/197_dark_launching_traffic_shadow/">Dark Launching</a>)</strong> | [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) OFF 상태로 프로덕션 배포 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a> 릴리즈</strong> | [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)로 1% 사용자 먼저 공개 |
| **A/B 테스트** | Experiment Toggle로 변형 비교 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/">Trunk-based Development</a></strong> | [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)가 브랜치 전략을 대체 |
| **토글 부채 (Toggle Debt)** | 미정리 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)의 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Feature Branch (2000s) — 브랜치별 기능 개발]
    |
    v
[Feature Flag 개념 (2010s) — 배포와 릴리즈 분리]
    |
    v
[LaunchDarkly SaaS (2014~) — 실시간 플래그 관리]
    |
    v
[Trunk-based + Flag (2018~) — 단일 브랜치 + 플래그 점진 공개]
    |
    v
[현재: AI 기반 자동 롤아웃 — 카나리 분석 + 자동 Flag ON/OFF]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 극장 무대의 <strong>조명 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a></strong>예요. 배우(코드)는 이미 있지만, 불을 켜야 관객이 봐요.
2. 새 공연이 걱정되면 **가족(사내 직원)에게만 먼저 보여주고**, 괜찮으면 모든 관객에게 공개해요.
3. 만약 실수가 있으면 **조명만 끄면(1초)** 돼서, 무대를 부수고([롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)) 다시 만들 필요가 없답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 114 / 973

<- **이전**: [113. 카오스 엔지니어링 (Chaos 엔진ering) - Chaos Monkey·정상 상태 가설·실험 설계](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/113_chaos_engineering_chaos_monkey/)
**다음**: [115. 카나리 배포 (Canary Deployment) - 점진적 롤아웃과 트래픽 분배 전략](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) ->

---
