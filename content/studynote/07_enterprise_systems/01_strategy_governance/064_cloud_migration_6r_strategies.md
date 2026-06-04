+++
title = "64. 클라우드 마이그레이션 전략 (6R: Rehost, Replatform, Refactor, Repurchase, Retire, Retain)"
date = 2026-04-07

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 6R은 기존 시스템을 클라우드로 옮길 때 Rehost, Replatform, [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/), Repurchase, Retire, Retain 중 어떤 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 택할지 정리하는 프레임워크다.
> 2. **가치**: 모든 시스템을 같은 방식으로 옮기지 않고, 업무 가치와 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)에 따라 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 다르게 고를 수 있다.
> 3. **판단**: 마이그레이션은 "이사"가 아니라 "재배치와 재설계"이므로 비용, 위험, 일정, 조직 변화를 같이 봐야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 마이그레이션은 단순 복사가 아니다. 레거시 시스템마다 적합한 이행 방식이 다르기 때문에, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 먼저 정해야 한다.

6R은 시스템을 옮길지, 바꿀지, 버릴지, 유지할지 판단하는 실무형 도구다.

- **📢 섹션 요약 비유**: 짐을 옮길 때도 그대로 옮길 것, 새로 고칠 것, 버릴 것을 먼저 나눠야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Legacy System
  ↓
6R Decision
  ↓
Cloud Migration Plan
  ↓
Execution
```

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 의미 |
| :-- | :-- |
| Rehost | 그대로 옮김 |
| Replatform | 일부만 수정해 옮김 |
| [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | 구조를 재설계 |
| Repurchase | SaaS로 교체 |
| Retire | 폐기 |
| Retain | 유지 |

6R은 "기술적으로 가능한가"보다 "비즈니스적으로 가치가 있는가"를 먼저 묻는다. 그래서 시스템의 중요도, 비용, 위험, 일정이 함께 고려되어야 한다.

- **📢 섹션 요약 비유**: 물건마다 택배, 새 가구, 중고 판매, 버리기 중 고를 수 있는 선택표다.

---

## Ⅲ. 비교 및 연결

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 장점 | 단점 | 추천 상황 |
| :-- | :-- | :-- | :-- |
| Rehost | 빠름 | 개선 적음 | 시간 부족 |
| Replatform | 효율 개선 | 일부 수정 필요 | 중간 난이도 |
| [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | 장기 가치 큼 | 비용 큼 | 핵심 시스템 |
| Repurchase | 빠른 전환 | [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) | 범용 업무 |
| Retire | 비용 절감 | 기능 상실 | 사용 적음 |
| Retain | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 회피 | 클라우드 이점 적음 | 규제/종속 |

6R은 서로 배타적이지 않다. 시스템별로 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 섞어 쓰는 것이 일반적이다.

- **📢 섹션 요약 비유**: 모든 짐을 한 박스에 넣지 않고, 종류별로 다른 상자를 쓰는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 시스템별 비즈니스 가치를 평가했는가?
2. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)와 변경 비용을 수치화했는가?
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 인터페이스 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 봤는가?
4. 규제와 보안 요구를 고려했는가?
5. 전환 후 운영모델을 준비했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 시스템을 Rehost로만 옮기는 설계
- [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 대체가 가능한데도 유지하는 설계
- 재설계가 필요한데 그대로 복사하는 설계
- 비용과 조직 변화를 고려하지 않는 설계

기술사 관점에서는 6R을 "클라우드 가는 길"이 아니라 "의사결정 표"로 봐야 한다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 맞아야 마이그레이션이 성공한다.

- **📢 섹션 요약 비유**: 이사할 때 버릴 것, 팔 것, 가져갈 것을 먼저 정해야 짐이 줄어든다.

---

## Ⅴ. 기대효과 및 결론

6R은 시스템별 최적의 클라우드 전환 방식을 정리해 준다. 덕분에 비용과 위험을 줄이고, 가치가 큰 곳에 집중할 수 있다.

결론적으로 6R은 클라우드 이행의 실무용 의사결정 프레임이다.

- **📢 섹션 요약 비유**: 짐 정리 목록이 있어야 이사가 빨라진다.

---

## 관련 개념 맵

```text
Legacy System
  ↓
6R Strategy
  ↓
Migration Plan
  ↓
Cloud Execution
```

---

## 관련 키워드 및 발전 흐름도

```text
Rehost
  ↓
Replatform / Refactor
  ↓
Repurchase / Retire / Retain
  ↓
Cloud Transformation
```

---

## 어린이를 위한 3줄 비유 설명

이사할 때 다 가져갈 필요는 없어요.
어떤 건 고치고, 어떤 건 버리고, 어떤 건 새로 살 수 있어요.
6R은 그 선택을 도와주는 표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 64 / 482

← **이전**: [63. 클라우드 벤더 락인 (Cloud Vendor Lock-in) 회피 전략](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/063_cloud_vendor_lock_in_avoidance/)
**다음**: [65. 섀도우 데이터 (Shadow Data) - 통제받지 않은 클라우드 내 산재된 기업 민감 데이터](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/065_shadow_data_cloud_security/) →

---
