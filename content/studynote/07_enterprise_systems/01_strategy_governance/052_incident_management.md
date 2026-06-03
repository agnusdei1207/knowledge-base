---
title: 52. 인시던트 관리 (Incident Management)
date: '2026-05-01'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[075_incident_management|인시던트 관리]] ([[075_incident_management|Incident Management]])는 [[090_service_kubernetes_network_load_balancing|서비스]] 중단이나 [[282_performance_tactics|성능]] 저하가 발생했을 때, 근본 원인보다 먼저 [[090_service_kubernetes_network_load_balancing|서비스]]를 빠르게 [[658_ir_recovery|복구]]하는 운영 프로세스다.
> 2. **가치**: [[076_workaround_temporary_fix_incident|워크어라운드]] ([[076_workaround_temporary_fix_incident|Workaround]]), 에스컬레이션, 우선순위 조정으로 사용자 영향 시간을 줄이고 [[085_sla|SLA]] ([[085_sla|Service Level Agreement]])를 지키게 한다.
> 3. **판단 포인트**: 인시던트는 [[077_problem_management|문제 관리]] ([[077_problem_management|Problem Management]])와 다르다. 인시던트는 "지금 살리는 것", [[077_problem_management|문제 관리]]는 "왜 그런지 깊게 파는 것"이다.

---

## Ⅰ. 개요 및 필요성

인시던트는 IT [[090_service_kubernetes_network_load_balancing|서비스]]가 계획대로 동작하지 않아 사용자에게 장애를 주는 사건이다. 서버 다운, 결제 [[015_지연_데이터_관점|지연]], [[286_page_frame|페이지]] 오픈 실패처럼 눈에 띄는 장애뿐 아니라, [[282_performance_tactics|성능]] 저하도 인시던트로 다뤄진다. 목표는 원인 규명이 아니라 [[090_service_kubernetes_network_load_balancing|서비스]] [[658_ir_recovery|복구]]다.

기업 입장에서 [[090_service_kubernetes_network_load_balancing|서비스]]가 1분 멈추는 비용은 매우 크다. 그래서 [[075_incident_management|인시던트 관리]]에서는 일단 [[658_ir_recovery|복구]]하고, 원인은 뒤에서 분석한다. 이 순서를 뒤집으면 사용자는 더 오래 기다리게 된다.

- **📢 섹션 요약 비유**: [[075_incident_management|인시던트 관리]]는 응급실이다. 먼저 숨을 쉬게 만들고, 그다음에 왜 쓰러졌는지 본다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[075_incident_management|인시던트 관리]]의 핵심은 탐지, [[104_classification_analysis|분류]], 우선순위 지정, [[658_ir_recovery|복구]], 종료다. [[072_service_desk|서비스 데스크]]가 단일 접점 ([[073_spoc|SPOC]], [[073_spoc|Single Point of Contact]]) 역할을 하고, 해결이 어려우면 전문 팀으로 넘긴다.

```text
┌──────────────────────────────────────────────────────────────┐
│               인시던트 관리의 서비스 복구 흐름              │
├──────────────────────────────────────────────────────────────┤
│ 사용자/모니터링 탐지                                          │
│          │                                                   │
│          ▼                                                   │
│ 접수 및 기록 → 분류/우선순위 → 초기 진단 → 에스컬레이션      │
│          │                                                   │
│          ▼                                                   │
│ 워크어라운드/복구 → 확인 → 종료                              │
└──────────────────────────────────────────────────────────────┘
```

| 단계 | 의미 | 핵심 포인트 |
| :--- | :--- | :--- |
| 접수/기록 | 티켓 [[087_process_state_transition|생성]] | 증상, 시간, 영향 범위 기록 |
| [[104_classification_analysis|분류]] | 인시던트 유형 판단 | [[090_service_kubernetes_network_load_balancing|서비스]]/시스템/보안 구분 |
| 우선순위 | 긴급도와 영향도 평가 | 사용자 수와 업무 중요도 반영 |
| [[459_quic_fec_forward_error_correction|초기]] 진단 | 1차 대응 | 재기동, 캐시 [[459_quic_fec_forward_error_correction|초기]]화, [[009_config|설정]] [[396_validation|확인]] |
| [[658_ir_recovery|복구]]/종료 | [[090_service_kubernetes_network_load_balancing|서비스]] 정상화 [[396_validation|확인]] | 사용자 [[396_validation|확인]]과 기록 정리 |

[[075_incident_management|인시던트 관리]]에서는 진짜 원인을 고치는 것보다 "사용자가 다시 일하게 만드는 것"이 우선이다. 그래서 재부팅, 트래픽 우회, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 같은 임시 [[658_ir_recovery|복구]]가 자주 등장한다. 이 임시 [[658_ir_recovery|복구]]가 바로 [[076_workaround_temporary_fix_incident|워크어라운드]]다.

- **📢 섹션 요약 비유**: [[075_incident_management|인시던트 관리]]는 자동차가 고장 났을 때, 일단 견인차를 불러 길을 비우고 나중에 정비소에서 고치는 것과 같다.

---

## Ⅲ. 비교 및 연결

[[075_incident_management|인시던트 관리]], [[077_problem_management|문제 관리]], [[079_change_enablement|변경 관리]]는 자주 헷갈린다. 인시던트는 [[090_service_kubernetes_network_load_balancing|서비스]] [[658_ir_recovery|복구]], [[077_problem_management|문제 관리]]는 근본 원인 제거, [[079_change_enablement|변경 관리]]는 시스템 수정 승인과 배포를 다룬다.

| 항목 | [[075_incident_management|인시던트 관리]] | [[077_problem_management|문제 관리]] | [[079_change_enablement|변경 관리]] |
| :--- | :--- | :--- | :--- |
| 목표 | 빠른 [[658_ir_recovery|복구]] | 근본 원인 제거 | 안전한 변경 |
| 시간축 | 즉시 | 중장기 | 변경 전/중 |
| 산출물 | 티켓, [[658_ir_recovery|복구]] 기록 | RCA, 문제 기록 | 변경 요청, 승인 |
| 우선순위 | 사용자 영향 | 재발 방지 | 안정성 |

[[075_incident_management|인시던트 관리]]는 [[072_service_desk|서비스 데스크]], [[367_noc|NOC]], [[100_sre_site_reliability_engineering_error_budget|SRE]], 운영팀과 연결된다. 특히 대규모 [[090_service_kubernetes_network_load_balancing|서비스]]에서는 major incident 절차를 두어, 커뮤니케이션 담당과 기술 해결 담당을 분리하기도 한다.

- **📢 섹션 요약 비유**: 인시던트는 불 끄기, [[077_problem_management|문제 관리]]는 왜 불이 났는지 조사, [[079_change_enablement|변경 관리]]는 전기 배선을 고치는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 중요한 것은 우선순위다. 모든 장애를 같은 방식으로 다루면 핵심 업무가 막힌다. 그래서 영향도, 긴급도, 고객 수, SLA를 종합해 우선순위를 정하고, 필요하면 워룸 ([[226_war|War]] Room)을 열어 집중 대응한다.

### [[435_checklist_based_testing|체크리스트]]

1. [[090_service_kubernetes_network_load_balancing|서비스]] 영향 범위가 명확한가?
2. 우회책이 먼저 정리되어 있는가?
3. 에스컬레이션 경로와 담당자가 정의되어 있는가?
4. 고객 커뮤니케이션이 [[015_지연_데이터_관점|지연]] 없이 이뤄지는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 원인 분석부터 시작해 [[658_ir_recovery|복구]]가 늦어지는 경우
- 티켓만 쌓고 우선순위 조정이 없는 경우
- 장애 공지 없이 내부에서만 소통하는 경우

대형 인시던트는 기술 문제이면서 커뮤니케이션 문제다. 그래서 [[658_ir_recovery|복구]]와 함께 사용자 공지, [[182_status_page_public_sla|상태 페이지]], 내부 보고 체계를 동시에 굴려야 한다.

- **📢 섹션 요약 비유**: [[652_incident_response_nist_800_61|인시던트 대응]]은 학교 운동회에서 방송, 응급처치, [[216_progress_in_synchronization|진행]] 정리가 동시에 필요한 상황과 같다.

---

## Ⅴ. 기대효과 및 결론

좋은 [[075_incident_management|인시던트 관리]]는 [[658_ir_recovery|복구]] 시간을 줄이고, 장애의 파급을 제한하며, 조직의 신뢰를 지킨다. 또한 반복되는 장애는 [[077_problem_management|문제 관리]]로 넘겨 근본 원인을 제거할 수 있게 해 준다.

즉 [[075_incident_management|인시던트 관리]]는 운영의 첫 방어선이다. 빨리 살리고, 정확히 기록하고, 다음에는 더 잘 막게 만드는 프로세스로 기억하면 된다.

- **📢 섹션 요약 비유**: [[075_incident_management|인시던트 관리]]는 넘어졌을 때 먼저 일으켜 세우고, 그다음 넘어지지 않게 길을 정리하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[085_sla|SLA]] | [[658_ir_recovery|복구]] 우선순위를 정하는 기준 |
| [[076_workaround_temporary_fix_incident|워크어라운드]] ([[076_workaround_temporary_fix_incident|Workaround]]) | 임시 [[658_ir_recovery|복구]] 수단 |
| [[077_problem_management|문제 관리]] | 근본 원인 분석 단계 |
| [[079_change_enablement|변경 관리]] | 수정/배포 승인 단계 |
| [[072_service_desk|서비스 데스크]] ([[073_spoc|SPOC]]) | 인시던트 접수의 단일 창구 |

### 📈 관련 키워드 및 발전 흐름도

```text
탐지 / 사용자 신고
    │
    ▼
인시던트 등록
    │
    ▼
분류 · 우선순위
    │
    ▼
초기 진단 · 에스컬레이션
    │
    ▼
워크어라운드 · 복구
    │
    ▼
문제 관리 / 변경 관리로 이관
```

이 흐름은 "빨리 [[658_ir_recovery|복구]]"와 "나중에 근본 해결"을 분리하는 운영 원칙을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 인시던트는 놀이터가 갑자기 멈춘 상황이에요.
2. 선생님은 먼저 아이들이 다시 놀 수 있게 그네를 고쳐요.
3. 그다음에 왜 고장 났는지는 따로 알아봐요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 52 / 482

← **이전**: [[051_help_desk_service_desk_spoc|051. 헬프 데스크, 서비스 데스크, SPOC]]
**다음**: [[053_problem_management_rca|53. 문제 관리와 근본 원인 분석 (Problem Management RCA)]] →

---
