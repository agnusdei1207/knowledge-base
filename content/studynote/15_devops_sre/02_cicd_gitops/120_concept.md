+++
title = "120. DORA Metrics (DevOps Research & Assessment) - 소프트웨어 배포 성과 4대 지표"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Metrics는 Google [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 팀이 정의한 **소프트웨어 배포 성과의 4대 핵심 지표**(배포 빈도·[리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)·변경 실패율·[MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))로, 팀의 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성숙도를 <strong>Elite·High·Medium·Low</strong>로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)한다.
> 2. **가치**: "우리 팀의 DevOps가 잘 되고 있는가?"를 <strong>객관적 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>로 측정할 수 있으며, Elite 팀은 Low 팀 대비 <strong>배포 빈도 973배, <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a> 6570배</strong> 빠르다(Accelerate 보고서).
> 3. **판단 포인트**: 4개 지표를 <strong>균형 있게 개선</strong>해야 하며, 배포 빈도만 높이고 변경 실패율이 높으면 의미 없다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    DORA 4대 지표                                      |
+-------------------------------------------------------+
|  1. 배포 빈도 (Deployment Frequency)                  |
|     -> Elite: 하루 여러 번 | Low: 월 1회 이하         |
|  2. 리드 타임 (Lead Time for Changes)                 |
|     -> Elite: 1시간 이내 | Low: 6개월 이상            |
|  3. 변경 실패율 (Change Failure Rate)                 |
|     -> Elite: 0~15% | Low: 46~60%                    |
|  4. MTTR (Mean Time to Restore)                       |
|     -> Elite: 1시간 이내 | Low: 6개월 이상            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Metrics는 공장의 <strong>품질·속도·불량률·<a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 시간</strong>을 측정하는 4개 계기판이다. 4개 모두 좋아야 진짜 좋은 공장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 성과 등급

| 등급 | 배포 빈도 | [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 변경 실패율 | [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) |
|:---|:---|:---|:---|:---|
| **Elite** | 하루 여러 번 | 1시간 이내 | 0~15% | 1시간 이내 |
| **High** | 주 1~월 1 | 1일~1주 | 16~30% | 1일 이내 |
| **Medium** | 월 1~6개월 1 | 1~6개월 | 16~30% | 1일~1주 |
| **Low** | 6개월 이하 | 6개월+ | 46~60% | 6개월+ |

- **📢 섹션 요약 비유**: Elite 팀은 F1 피트스톱(1.8초 타이어 교체)이고, Low 팀은 일반 정비소(3일 정비)다.

---

## Ⅲ. 비교 및 연결

| 비교 | 속도 지표 | 안정성 지표 |
|:---|:---|:---|
| **배포 빈도** | ✅ | - |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a></strong> | ✅ | - |
| **변경 실패율** | - | ✅ |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a></strong> | - | ✅ |

핵심: 속도 + 안정성 **둘 다** 높아야 Elite.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 측정 도구
- **Sleuth**: GitHub 연동 자동 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 측정.
- **Jellyfish**: 엔지니어링 지표 대시보드.
- **Four Keys**: Google [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 측정 도구.

### 개선 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
- 배포 빈도 ^: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 자동화, [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/).
- [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) v: 작은 배치, [트렁크 기반 개발](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/).
- 변경 실패율 v: 테스트 커버리지, [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/).
- [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) v: 관측성([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)), 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/).

---

## Ⅴ. 기대효과 및 결론

[DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Metrics는 <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/">DevOps</a> 성숙도의 사실상 업계 표준 측정 체계</strong>이며, SPACE 프레임워크(GitHub)와 결합하여 개발자 생산성을 종합적으로 측정하는 방향으로 확장되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **배포 빈도** | 속도 지표, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 성숙도 반영 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a></strong> | 코드 커밋->프로덕션 배포 시간 |
| **변경 실패율** | 안정성 지표, 테스트 품질 반영 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a></strong> | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도, 관측성 수준 반영 |
| **Accelerate** | [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Metrics의 이론적 기반 서적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DevOps 개념 등장 (2009~)]
    |
    v
[DORA 팀 연구 시작 (2013~) — State of DevOps Report]
    |
    v
[Accelerate 출판 (2018) — DORA 4대 지표 정의]
    |
    v
[Google DORA 팀 합류 (2018~) — 산업 표준화]
    |
    v
[현재: DORA + SPACE — 종합 개발자 생산성 측정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DORA는 공장의 <strong>4개 계기판</strong>이에요. 속도·품질·불량률·수리 시간을 재요.
2. **4개 모두 좋은** 공장이 최고 등급(Elite)이에요. 하나만 좋으면 안 돼요.
3. 최고 공장(Elite)은 **하루에 여러 번** 제품을 내놓고, 문제가 생기면 **1시간 안에** 고친답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 373

<- **이전**: [119. Pre-commit Hook 린팅 (Pre-commit Hook Linting) - 커밋 전 자동 코드 품질 검증](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/119_pre_commit_hook_linting/)
**다음**: [121. SRE 철학 (Site Reliability 엔진ering Philosophy) - 신뢰성 엔지니어링의 핵심 원칙](/knowledge-base/studynote/15_devops_sre/03_sre_observability/121_sre_philosophy/) ->

---
