---
title: 445. 레거시 현대화 스트랭글러 피그 변환 감리 (Strangler Fig Pattern for Legacy Modernization
  Audit)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

1. [[310_strangler_fig_pattern|스트랭글러 피그]] 변환 감리는 레거시를 한 번에 버리지 않고 게이트웨이, [[064_relation_domain|도메인]] 분리, 점진 전환으로 현대화를 통제하는 감리 주제다.
2. 핵심 가치는 [[090_service_kubernetes_network_load_balancing|서비스]] 연속성을 유지하면서도 전환 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]], [[001_dikw_pyramid|데이터]] 정합성, 이중 운영 비용을 증거 기반으로 관리하는 데 있다.
3. 기술사 판단에서는 [[339_routing_overview_best_path_selection|라우팅]] 경계, [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]], 철거 기준이 단계별 산출물로 닫히는지를 분명히 써야 한다.

## Ⅰ. 개요 및 필요성

레거시 현대화에서 가장 위험한 선택은 모든 기능을 새 시스템으로 한 번에 갈아타는 빅뱅 전환이다. 기능 누락, 회귀 [[352_defect_definition|결함]], 운영자 학습 공백이 한 시점에 겹치면 일정과 품질이 동시에 무너진다. [[310_strangler_fig_pattern|스트랭글러 피그]] 변환 감리는 이런 위험을 작게 쪼개어 관리하는 관점이며, 감리인은 단순히 "새 시스템이 좋아 보이는가"가 아니라 "구 시스템을 어떤 순서와 증거로 줄여 나가는가"를 본다.

특히 공공·금융처럼 가동 중단 허용 폭이 좁은 환경에서는 신규 [[090_service_kubernetes_network_load_balancing|서비스]] 구축 자체보다 전환 경계의 설계가 더 중요하다. 요청이 어느 순간부터 신규로 분기되는지, [[001_dikw_pyramid|데이터]]는 어떤 기준으로 이관되는지, 레거시는 언제 폐기 가능한지를 명확히 해야 사업 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 통제된다.

```text
┌──────────────┐    ┌────────────────┐    ┌──────────────────┐
│ Legacy Only  │──▶│ Dual Operation │──▶│ Legacy Retire    │
└──────────────┘    └────────────────┘    └──────────────────┘
       │                     │                        │
       └──── 고위험 구간 ────┴──── 통제 필요 ────────┘
```

위 흐름은 현대화의 본질이 신규 개발보다 단계적 축소 통제에 있음을 보여 준다. 감리 문서는 단계별 진입 기준과 종료 기준을 함께 제시해야 설계와 운영이 어긋나지 않는다.

- **📢 섹션 요약 비유**: 낡은 건물을 한 번에 비우지 않고 층별로 새 건물로 옮겨 가며 안전 점검표를 확인하는 이사 계획과 같다.

## Ⅱ. 아키텍처 및 핵심 원리

[[310_strangler_fig_pattern|스트랭글러 피그]]의 핵심 원리는 가로채기(Intercept) - 점진 이전(Strangle) - 종료(Retire)를 한 체계로 묶는 데 있다. 전면 게이트웨이가 모든 요청을 받아 신구 시스템으로 분기하고, 기능 단위로 신규 [[090_service_kubernetes_network_load_balancing|서비스]]를 늘리며, 마지막에는 잔존 기능과 [[001_dikw_pyramid|데이터]]까지 철거 가능 상태를 판정한다. 감리 관점에서는 기능 분리보다도 [[339_routing_overview_best_path_selection|라우팅]] 규칙, [[212_synchronization_mechanisms|동기화]] 방식, [[658_ir_recovery|복구]] 절차가 추적 가능하게 남아 있는지가 중요하다.

```text
┌─────────────┐      ┌──────────────────┐      ┌──────────────┐
│ 사용자 요청 │───▶│ Gateway / Facade │───▶│ 신규 서비스   │
└─────────────┘      └──────────────────┘      └──────────────┘
                             │
                             ├───────────────▶┌──────────────┐
                             │                │ 레거시 시스템 │
                             │                └──────────────┘
                             └───────────────▶┌──────────────┐      ┌──────────┐
                                              │ CDC / 동기화 │───▶│ 신규 DB   │
                                              └──────────────┘      └──────────┘
```

| 구성축 | 핵심 내용 | 감리 포인트 |
|:---|:---|:---|
| 전환 경계 | [[014_api_posix|API]] 게이트웨이, [[264_proxy_pattern_surrogate_access_control|프록시]], 어댑터로 기능별 분기 | 어떤 URL·업무가 신규로 전환됐는지 [[339_routing_overview_best_path_selection|라우팅]] 표가 있어야 한다 |
| [[001_dikw_pyramid|데이터]] [[268_strategy_pattern|전략]] | [[217_cdc_binlog_change_capture_debezium|CDC]], 이벤트 [[016_replication_factor|복제]], 배치 이행으로 신구 정합성 유지 | 이중 기록 충돌과 최종 정합 시점을 증빙해야 한다 |
| 운영 통제 | [[115_canary_deployment_gradual_rollout|카나리 배포]], 관측성, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차로 위험 최소화 | 전환 실패 시 복귀 경로와 장애 책임자가 명시돼야 한다 |
| 철거 기준 | 사용량 0, 배치 제거, 인터페이스 제거 후 레거시 폐기 | 폐기 판정 근거가 없으면 기술 부채만 이중으로 남는다 |

핵심 원리는 새 시스템을 빨리 만드는 것이 아니라 옛 시스템을 안전하게 줄이는 것이다. 따라서 감리 답안에는 [[064_relation_domain|도메인]] 분해, 게이트웨이 분기, [[001_dikw_pyramid|데이터]] 분리, 폐기 기준을 하나의 흐름으로 연결해 써야 완성도가 높다.

- **📢 섹션 요약 비유**: 도로 공사에서 임시 우회 차선을 먼저 만들고 차량을 조금씩 새 길로 보내며 사고 없이 본선을 바꾸는 방식과 같다.

## Ⅲ. 비교 및 연결

레거시 전환 [[268_strategy_pattern|전략]]은 모두 현대화를 말하지만 통제 방식이 다르다. [[310_strangler_fig_pattern|스트랭글러 피그]]는 운영 중 전환과 감리 증적 확보에 강하고, 빅뱅은 구조 단순성은 높지만 실패 비용이 크다. 브랜치 바이 [[198_abstraction_control_data_process|추상화]]는 코드 내부 교체에는 유리하지만 대외 인터페이스와 [[001_dikw_pyramid|데이터]] 전환 통제에는 보완 장치가 더 필요하다.

| 비교 항목 | 빅뱅 재개발 | [[310_strangler_fig_pattern|스트랭글러 피그]] | 브랜치 바이 [[198_abstraction_control_data_process|추상화]] |
|:---|:---|:---|:---|
| 전환 방식 | 한 시점 일괄 교체 | 기능 단위 점진 교체 | 추상 계층 뒤에서 구현 교체 |
| [[090_service_kubernetes_network_load_balancing|서비스]] 연속성 | 낮음 | 높음 | 중간 |
| [[001_dikw_pyramid|데이터]] 정합 통제 | 전환일 집중 [[395_verification_process_review|검증]] | 기간 중 상시 [[395_verification_process_review|검증]] | 코드 단 중심 [[395_verification_process_review|검증]] |
| 감리 적합성 | 종료 시점 점검 위주 | 단계별 증적 점검 용이 | 소스 구조 [[395_verification_process_review|검증]]에 강함 |
| 적합 상황 | 규모 작고 중단 허용 가능 | 대규모 핵심 업무 | 내부 [[192_module_independence|모듈]] 교체 중심 |

또한 이 주제는 [[014_api_posix|API]] 게이트웨이, [[217_cdc_binlog_change_capture_debezium|CDC]], 블루그린·[[115_canary_deployment_gradual_rollout|카나리 배포]]와 직접 연결된다. 시험에서는 단순 패턴 설명보다 "왜 감리에서 선호되는가"를 비교 문장으로 정리하면 답안 밀도가 올라간다.

- **📢 섹션 요약 비유**: 집 전체를 하루 만에 리모델링할지, 방마다 순서대로 공사할지 비교해 공사 중에도 생활을 이어 가는 문제와 같다.

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "점진 전환"이라는 말보다 증거가 중요하다. 기능 전환 로드맵, 인터페이스 목록, [[001_dikw_pyramid|데이터]] 정합 [[395_verification_process_review|검증]]서, 전환 승인 기준이 모두 있어야 감리가 가능하다. 특히 레거시와 신규가 동시에 돈을 벌고 있는 기간에는 장애가 나면 어느 쪽 책임인지 모호해지므로, 책임 경계와 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차를 운영 문서로 남겨야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]

- 업무 기능별로 전환 우선순위와 종료 조건이 정의되어 있는가?
- 게이트웨이 [[339_routing_overview_best_path_selection|라우팅]] 규칙과 변경 이력이 형상관리되고 있는가?
- 신구 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]] 방식과 정합 [[395_verification_process_review|검증]] 주기가 문서화되어 있는가?
- [[595_canary_stack_smashing_protector|카나리]], A/B 테스트, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차가 실제 리허설되었는가?
- 사용량 0, 배치 제거, 인터페이스 종료 등 레거시 철거 판정 기준이 있는가?
- 이중 운영 기간의 비용, 인력, 보안 책임 분담이 명확한가?

흔한 실패는 "신규 [[090_service_kubernetes_network_load_balancing|서비스]]는 만들었지만 레거시를 끄지 못하는 상태"다. 기술사 답안에서는 이 안티패턴을 지적하고, 폐기 기준까지 포함해야 진짜 현대화라고 정리하면 좋다.

- **📢 섹션 요약 비유**: 새 가게를 열었는데 옛 가게 간판과 재고를 정리하지 못해 임대료만 두 배로 나가는 상황과 같다.

## Ⅴ. 기대효과 및 결론

[[310_strangler_fig_pattern|스트랭글러 피그]] 변환 감리를 제대로 수행하면 빅뱅 실패 위험을 줄이고, 사업 연속성을 유지하며, 레거시 축소를 계량적으로 추적할 수 있다. 또한 기능별 책임과 증적이 남기 때문에 경영진, 운영팀, 개발팀이 같은 기준으로 전환 상태를 판단할 수 있다.

결론적으로 이 주제의 본질은 "새것을 만드는 기술"이 아니라 "오래된 것을 안전하게 없애는 통제 기술"이다. 답안에서는 단계, [[001_dikw_pyramid|데이터]], 운영, 철거의 네 축을 묶어 쓰면 감리 관점이 살아난다.

- **📢 섹션 요약 비유**: 오래된 나무를 한 번에 베지 않고 지지대를 세워 가며 위험 구간부터 안전하게 정리하는 작업과 같다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[542_api_gateway|API Gateway]] | 모든 요청을 가로채 전환 경계를 제어하는 전면 통제 지점 |
| [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | 신구 [[001_dikw_pyramid|데이터]] 정합성을 유지하는 핵심 메커니즘 |
| [[115_canary_deployment_gradual_rollout|Canary Deployment]] | 점진 전환 시 장애 반경을 줄이는 운영 기법 |
| [[064_relation_domain|Domain]] Decomposition | 어떤 기능부터 떼어낼지 결정하는 설계 출발점 |
| Legacy Retirement | 현대화의 끝을 정의하는 최종 감리 판정 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
┌─────────────────┐
│ Monolith Legacy │
└─────────────────┘
          │
          ▼
┌────────────────────┐
│ Gateway Intercept  │
└────────────────────┘
          │
          ▼
┌────────────────────┐
│ Service Extraction │
└────────────────────┘
          │
          ▼
┌────────────────────┐
│ Data Sync / Split  │
└────────────────────┘
          │
          ▼
┌────────────────────┐
│ Legacy Retirement  │
└────────────────────┘
```

[[310_strangler_fig_pattern|스트랭글러 피그]]는 단순 분해가 아니라 가로채기, 병행 운영, [[001_dikw_pyramid|데이터]] 정리, 폐기로 이어지는 장기 통제 흐름으로 이해해야 한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 오래된 장난감 상자를 한 번에 버리지 않고 새 상자를 옆에 두고 하나씩 옮기는 거예요.
2. 옮길 때마다 무엇을 옮겼는지 적어 두어야 잃어버리지 않아요.
3. 마지막 장난감까지 다 옮기면 그때 오래된 상자를 치우면 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 523 / 530

← **이전**: [[444_sbom|444. SBOM 소프트웨어 구성 명세 취약 방어 (Software Bill of Materials Vulnerability Defense)]]
**다음**: [[446_csap|446. 공공 클라우드 CSAP 보안 인증 점검 통제 (CSAP Security Certification Control for Public]] →

---
