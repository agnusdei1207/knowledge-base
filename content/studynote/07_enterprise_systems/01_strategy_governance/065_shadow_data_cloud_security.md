---
title: "Shadow Data Cloud Security"
date: "2026-04-07"
tags:
  - "studynote-enterprise-systems"
weight: 65
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Shadow [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 조직이 통제하지 못하는 클라우드 내 산재 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로, [민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/) 노출 위험이 크다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치, 소유자, 접근 권한, 보존 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줄일 수 있다.
> 3. **판단**: 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 섀도우 IT와 다르지만 연결되며, 클라우드 거버넌스의 핵심 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)다.

---

## Ⅰ. 개요 및 필요성

클라우드는 빠르게 저장하고 공유할 수 있게 해 주지만, 그만큼 통제되지 않은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 쉽게 늘어난다.

특히 [민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/)가 여러 계정과 스토리지에 흩어지면 검색도 어렵고 삭제도 어렵다.

- **📢 섹션 요약 비유**: 집 안 여기저기에 중요한 서류를 숨겨 두면 찾기도 어렵고 도난 위험도 커진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data Sources
  v
Cloud Storage / SaaS
  v
Discovery / Classification
  v
Access Control / Encryption
  v
Governance
```

| 위험 요인 | 설명 |
| :-- | :-- |
| Uncontrolled Storage | 승인 없는 저장소 사용 |
| Sensitive [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Sprawl | [민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| Weak [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) | 과도한 권한 |
| [Retention](/studynote/05_database/04_transactions_concurrency/515_mvcc/) Gap | 보존/삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 부재 |

섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 발견되지 않으면 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)할 수 없다. 따라서 발견(Discovery)과 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/studynote/12_it_management/03_ea_isp/107_classification/))가 첫 단계다.

- **📢 섹션 요약 비유**: 어디에 있는지 모르면 자물쇠를 채울 수도 없다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 | 차이 |
| :-- | :-- | :-- |
| Shadow [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 통제 밖 민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 위치/권한 문제 |
| [Dark Data](/studynote/12_it_management/02_itsm_itil/062_darkdata/) | 활용되지 않는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 가치 미활용 문제 |
| [Shadow IT](/studynote/12_it_management/01_governance_strategy/049_shadow_it/) | 승인 없는 IT 사용 | 시스템/[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 문제 |

| 대응 수단 | 역할 |
| :-- | :-- |
| [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Discovery | 숨은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐지 |
| [DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/) | 유출 방지 |
| Encryption | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 강화 |
| Lifecycle [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) | 보존/삭제 관리 |

섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 단순 저장 문제가 아니라 거버넌스 문제다. 저장소, 권한, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 함께 관리되어야 한다.

- **📢 섹션 요약 비유**: 숨은 보물과 다르게, 숨은 위험물은 먼저 찾아내야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 클라우드 자산과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치를 모두 파악했는가?
2. 민감도 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 태그가 적용되는가?
3. 접근 권한이 최소화되어 있는가?
4. 보존/삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 자동화되어 있는가?
5. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발견과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 반복 가능한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 계정과 버킷이 늘어나는데 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 목록이 없는 설계
- [민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/)를 일반 저장소에 방치하는 설계
- 권한 회수와 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 점검을 하지 않는 설계
- 섀도우 IT와 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 문제로만 보는 설계

기술사 관점에서는 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 "관리 안 되는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"로 보고, 기술·조직·[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 합산 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)로 설명해야 한다.

- **📢 섹션 요약 비유**: 창고가 많아질수록 열쇠와 목록표가 같이 늘어나야 한다.

---

## Ⅴ. 기대효과 및 결론

섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줄이면 보안 사고 가능성이 줄고, 규정 준수와 삭제 대응도 쉬워진다. 결국 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치의 가시성이 핵심이다.

결론적으로 섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 클라우드 시대의 대표적인 거버넌스 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)다.

- **📢 섹션 요약 비유**: 보이지 않는 곳에 둔 물건은 잃어버리기 쉽다.

---

## 관련 개념 맵

```text
Cloud Data
  v
Shadow Data
  v
Discovery / Classification
  v
Governance
```

---

## 관련 키워드 및 발전 흐름도

```text
Shadow IT
  v
Shadow Data
  v
Data Discovery
  v
Cloud Governance
```

---

## 어린이를 위한 3줄 비유 설명

중요한 서류를 여기저기 숨겨 두면 안 돼요.
어디 있는지 찾아내고, 잠그고, 목록을 적어야 해요.
섀도우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 그런 숨은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 말해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 65 / 482

<- **이전**: [64. 클라우드 마이그레이션 전략 (6R: Rehost, Replatform, Refactor, Repurchase, Retire,](/studynote/07_enterprise_systems/01_strategy_governance/064_cloud_migration_6r_strategies/)
**다음**: [66. 데이터 거버넌스 (Data Governance) - 데이터 품질, 보안, 프라이버시 전사 관리 체계](/studynote/07_enterprise_systems/01_strategy_governance/066_data_governance_framework/) ->

---
