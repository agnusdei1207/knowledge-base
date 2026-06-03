---
title: 184. 재해 복구 훈련과 카오스 엔지니어링 융합 (Disaster Recovery + Chaos Engineering)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[379_dr_architecture|재해 복구]] (Disaster [[658_ir_recovery|Recovery]], [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 훈련과 [[751_chaos_engineering|카오스 엔지니어링]]의 융합은 문서로만 존재하던 [[658_ir_recovery|복구]] 절차를 계획된 장애 실험으로 [[395_verification_process_review|검증]]해, 실제 위기에서 작동하는 운영 역량으로 바꾸는 방법이다.
> 2. **가치**: 이 접근은 [[658_ir_recovery|복구]] 시간 목표 ([[176_rto_recovery_time_objective|Recovery Time Objective]], [[176_rto_recovery_time_objective|RTO]])와 [[658_ir_recovery|복구]] 시점 목표 ([[177_rpo_recovery_point_objective|Recovery Point Objective]], [[177_rpo_recovery_point_objective|RPO]])를 서류상의 숫자에서 실측 가능한 능력으로 바꾸고, 팀의 근육 기억과 협업 절차를 동시에 강화한다.
> 3. **판단 포인트**: 좋은 GameDay는 장애를 크게 만드는 행사가 아니라, 가설·정상 상태·폭발 반경·중단 조건·사후 학습이 명확한 통제 실험이어야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 훈련은 보통 "정해진 날에 정해진 절차를 따라 해 보는 행사"에 머무르기 쉽다. 하지만 실제 장애는 더 지저분하다. 연락망은 늦게 연결되고, 의존 [[090_service_kubernetes_network_load_balancing|서비스]]는 예상과 다르게 반응하며, 문서에 적힌 [[158_instruction|명령어]]는 [[288_version_ihl_tos_total_length|버전]]이 달라질 수 있다. 그래서 현대 운영에서는 [[658_ir_recovery|복구]] 절차를 읽는 것만으로는 충분하지 않고, **실제 불확실성을 일부러 주입해 보는 [[395_verification_process_review|검증]]**이 필요해졌다.

[[751_chaos_engineering|카오스 엔지니어링]]은 바로 그 [[395_verification_process_review|검증]]을 위해 등장했다. 정상 상태를 먼저 정의하고, 통제된 장애를 주입한 뒤, 시스템과 조직이 기대한 대로 [[233_recovery_database_restoration_overview|회복]]하는지 [[396_validation|확인]]한다. 여기에 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 관점을 결합하면 단순한 장애 주입이 아니라 "지역 장애가 나면 어느 순서로 우회하는가", "기본 [[002_database_definition|데이터베이스]]가 사라지면 손실 없이 승격되는가", "운영팀은 몇 분 안에 의사결정을 끝내는가" 같은 [[658_ir_recovery|복구]] 시나리오 [[395_verification_process_review|검증]]으로 확장된다.

이 융합이 필요한 이유는 두 가지다. 첫째, [[658_ir_recovery|복구]] 계획은 써 놓았다고 작동하지 않는다. 둘째, 시스템 [[658_ir_recovery|복구]]와 사람 [[658_ir_recovery|복구]]는 별개의 문제가 아니다. 즉 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] + 카오스 접근의 핵심 가치는 시스템 내구성과 팀 대응 절차를 하나의 훈련 루프로 묶는 데 있다.

- **📢 섹션 요약 비유**: 이 방식은 소방 매뉴얼을 책으로 읽는 데서 끝내지 않고, 실제 경보를 울려 대피 동선과 소화 장비가 정말 작동하는지 [[396_validation|확인]]해 보는 훈련과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스 실험은 "무작위로 망가뜨리기"가 아니라, 통제된 운영 실험이다. 기본 구조는 비즈니스 가설 [[009_config|설정]], 정상 상태 측정, 장애 주입, [[658_ir_recovery|복구]] 실행, 사후 학습의 5단계로 정리할 수 있다. 여기서 정상 상태는 단순히 서버가 떠 있는지가 아니라, [[090_service_kubernetes_network_load_balancing|서비스]] 수준 지표 ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]], [[102_sli_slo_service_level_indicator_objective|SLI]])와 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 ([[123_slo_service_level_objective|Service Level Objective]], [[181_slo_service_level_objective|SLO]]), 사용자 성공률, [[001_dikw_pyramid|데이터]] 정합성 같은 실제 품질 [[130_signal|신호]]로 정의해야 한다.

이 그림은 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스 실험의 제어 루프를 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ DR + Chaos GameDay control loop                                    │
├────────────────────────────────────────────────────────────────────┤
│ 1. 가설 설정 : "주 데이터베이스 장애 시 5분 내 승격, RPO 0"       │
│ 2. 정상 상태 : 성공률, 지연시간, 복제 지연, 데이터 정합성 확인     │
│ 3. 장애 주입 : 노드 종료, 네트워크 단절, 지역 격리                  │
│ 4. 대응 실행 : 알람, 온콜 호출, 런북 수행, 우회 또는 승격            │
│ 5. 학습 반영 : 포스트모템, 자동화 추가, 문서 수정, 재실험            │
│                                                                    │
│ Guardrails : 폭발 반경 제한 · 중단 조건 · 롤백 경로                │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 시 핵심 질문 |
| :--- | :--- | :--- |
| 가설 | 성공 기준 선언 | 어느 시간 안에 무엇이 [[233_recovery_database_restoration_overview|회복]]되어야 하는가? |
| 정상 상태 | 실험 전 [[025_baseline|기준선]] | 사용자 영향 없이 평소 품질이 유지되는가? |
| 장애 주입 | 실패 조건 재현 | 어떤 계층을 끊어야 실제 위험이 드러나는가? |
| 가드레일 | 실험의 안전장치 | 어디까지 영향을 허용하고 언제 중단할 것인가? |
| 관측성 | 결과 측정 | [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스로 [[658_ir_recovery|복구]] 과정을 설명할 수 있는가? |
| 학습 루프 | 개선 반영 | 다음 실험 전에 무엇을 자동화하고 문서화할 것인가? |

실험은 보통 인프라 계층부터 시작해 애플리케이션, [[001_dikw_pyramid|데이터]] 계층, 운영 절차로 확장한다. 예를 들어 가상 머신 종료는 비교적 단순한 수준이고, 주 [[002_database_definition|데이터베이스]] 손실·[[064_relation_domain|도메인]] 이름 체계 ([[511_dns_hierarchical_distributed_architecture|Domain Name System]], [[511_dns_hierarchical_distributed_architecture|DNS]]) 장애·비밀값 만료·[[389_mesh_topology|메시]]지 큐 [[015_지연_데이터_관점|지연]]은 더 높은 수준의 복합 장애다. 진짜 의미 있는 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스는 이 복합 경계에서 숨은 의존성을 드러낸다.

또 하나의 핵심은 폭발 반경 관리다. 처음부터 전체 운영 환경을 대상으로 하면 훈련이 아니라 실제 사고가 된다. 따라서 특정 [[090_service_kubernetes_network_load_balancing|서비스]], 특정 가용 영역 ([[452_availability|Availability]] Zone, AZ), 일부 트래픽 비율, 읽기 전용 경로처럼 작은 범위에서 시작해 [[395_verification_process_review|검증]] 범위를 넓히는 식이 안전하다.

- **📢 섹션 요약 비유**: [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스 실험은 학교 전체에 갑자기 정전을 내는 일이 아니라, 한 층의 비상등만 꺼 보고 대피 유도와 비상 발전기가 기대대로 작동하는지 [[396_validation|확인]]해 보는 훈련에 가깝다.

---

## Ⅲ. 비교 및 연결

[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] [[395_verification_process_review|검증]] 방식은 보통 세 단계로 나뉜다. 문서 중심의 탁상 훈련, 절차 중심의 스크립트형 [[658_ir_recovery|복구]] 훈련, 그리고 실제 운영 [[130_signal|신호]]를 보는 카오스 기반 GameDay다. 셋은 대체 [[083_relationship_in_er_model|관계]]가 아니라 성숙도 단계에 가깝지만, 어디까지 실제성을 가져가느냐에 따라 발견되는 [[352_defect_definition|결함]]의 종류가 크게 달라진다.

| 방식 | 무엇을 [[395_verification_process_review|검증]]하는가 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| 탁상 훈련 | 역할, 연락 체계, 의사결정 흐름 | 비용이 낮고 빠르게 자주 가능 | 시스템 자동화 [[352_defect_definition|결함]]은 드러나지 않음 |
| 스크립트형 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 훈련 | 정해진 절차와 [[658_ir_recovery|복구]] 명령 | 재현성과 교육 효과가 높음 | 예상 밖 의존성과 운영 압박이 약함 |
| 카오스 기반 GameDay | 실제 [[130_signal|신호]], 자동화, 사람 대응, 숨은 의존성 | 가장 현실적인 [[395_verification_process_review|검증]] | 설계 미흡 시 운영 위험이 큼 |

이 접근은 사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 엔지니어링 ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]], [[100_sre_site_reliability_engineering_error_budget|SRE]]), [[056_bcp_business_continuity_plan_bia|비즈니스 연속성 계획]] (Business Continuity Planning, BCP), [[101_error_budget_sre|에러 예산]] 운영과도 연결된다. SRE는 [[090_service_kubernetes_network_load_balancing|서비스]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 수치로 관리하고, BCP는 비즈니스 지속을 계획하며, [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스는 그 계획을 실험으로 [[395_verification_process_review|검증]]한다. 즉 "운영 철학"과 "[[658_ir_recovery|복구]] 문서" 사이의 마지막 연결 고리가 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스라고 볼 수 있다.

환경 [[170_selectivity_cardinality_distribution_tuning|선택도]] 중요하다. 스테이징은 안전하지만 실제 [[001_dikw_pyramid|데이터]] 규모와 외부 의존성을 충분히 재현하지 못할 수 있다. 운영 환경은 현실성이 높지만 가드레일이 필수다. 따라서 일반적으로는 스테이징에서 패턴을 익힌 뒤, 운영 환경에서는 일부 트래픽·일부 [[090_service_kubernetes_network_load_balancing|서비스]]에 한해 점진적으로 확대하는 [[268_strategy_pattern|전략]]이 바람직하다.

- **📢 섹션 요약 비유**: 탁상 훈련이 비상 대피 경로를 지도로 보는 것이라면, GameDay는 실제 복도를 걸어 보고 출구문이 잠겨 있지 않은지 [[396_validation|확인]]하는 것이다. 지도와 현장은 같아 보이지만 자주 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "무슨 장애를 주입할 것인가"보다 "어떤 비즈니스 기능을 [[395_verification_process_review|검증]]할 것인가"부터 정하는 편이 좋다. 주문, 결제, [[568_logs_distributed_logging_elk_fluentd|로그]]인, [[001_dikw_pyramid|데이터]] 수집처럼 핵심 여정을 기준으로 시나리오를 잡아야 RTO와 RPO도 의미 있게 측정된다. 단순히 서버를 한 대 죽이는 실험만 반복하면 팀은 도구 사용법은 익히지만 실제 [[658_ir_recovery|복구]] [[268_strategy_pattern|전략]]은 배우지 못한다.

| [[395_verification_process_review|검증]] 대상 | 대표 장애 시나리오 | 핵심 관측 지표 | 합격 기준 예시 |
| :--- | :--- | :--- | :--- |
| 주 [[002_database_definition|데이터베이스]] | 리더 노드 강제 중단, [[016_replication_factor|복제]] 링크 단절 | [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]], 승격 시간, [[001_dikw_pyramid|데이터]] 손실 여부 | [[176_rto_recovery_time_objective|RTO]] 5분 이내, [[177_rpo_recovery_point_objective|RPO]] 0 |
| 지역 단위 [[090_service_kubernetes_network_load_balancing|서비스]] | 특정 AZ 격리, [[339_routing_overview_best_path_selection|라우팅]] 차단 | 성공률, [[015_지연_데이터_관점|지연]]시간, 자동 우회 여부 | 사용자 오류율 급증 없이 우회 |
| [[389_mesh_topology|메시]]지 처리 [[123_pipe|파이프]]라인 | 큐 적체, 소비자 중단 | 적체량, [[019_처리_지연|처리 지연]], 재처리 성공률 | 백로그가 임계시간 안에 해소 |
| 운영 절차 자체 | 알람 발송, 온콜 호출, 승인 체계 | [[138_response_time|응답 시간]], 커뮤니케이션 누락, 런북 이행률 | 지정 역할이 정해진 시간 안에 대응 |

기술사 관점에서 강조할 실무 판단은 다음과 같다.

1. **가설 명시**: "정상 [[658_ir_recovery|복구]]된다"가 아니라 시간, [[001_dikw_pyramid|데이터]] 손실, 사용자 영향까지 수치로 적는가?
2. **중단 조건**: 오류율 급등, [[001_dikw_pyramid|데이터]] 손실 징후, 외부 고객 영향 확대 시 자동 또는 수동 중단 기준이 있는가?
3. **관측성 준비**: 실험 중 대시보드, 트레이스, 운영 채팅 기록이 모두 남는가?
4. **런북 품질**: 담당자가 처음 보는 문서만으로도 [[658_ir_recovery|복구]]할 수 있을 만큼 절차가 최신인가?
5. **사후 개선**: 포스트모템 결과가 자동화, 접근 권한, 아키텍처 수정으로 실제 반영되는가?

대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]은 네 가지다. 첫째, [[658_ir_recovery|복구]] 성공 여부를 서버 생존 여부로만 보는 경우다. 둘째, 운영 환경 실험인데 중단 조건과 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차가 없는 경우다. 셋째, 매번 같은 쉬운 시나리오만 반복해 팀이 진짜 약점을 못 보는 경우다. 넷째, 실험이 끝난 뒤 문서 업데이트와 재검증이 없어 같은 [[352_defect_definition|결함]]을 다시 만나는 경우다.

- **📢 섹션 요약 비유**: [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스 운영은 비행 훈련에서 아무 경고 없이 엔진을 끄는 일이 아니라, 고도와 안전 범위를 정해 둔 상태에서 조종사가 비상 절차를 정확히 수행하는지 [[396_validation|확인]]하는 시험과 같다.

---

## Ⅴ. 기대효과 및 결론

DR과 [[751_chaos_engineering|카오스 엔지니어링]]을 결합하면 조직은 장애를 "일어나면 대응하는 사건"이 아니라 "미리 [[395_verification_process_review|검증]]하는 역량"으로 다루게 된다. 그 결과 숨은 의존성, 오래된 런북, 느린 승인 절차, 부족한 권한, 잘못된 알람 같은 현실적 [[352_defect_definition|결함]]이 실제 사고 전에 드러난다. 특히 사람과 시스템을 함께 훈련한다는 점에서 단순 자동 [[658_ir_recovery|복구]] 테스트보다 학습 효과가 크다.

물론 비용과 피로도도 있다. 실험 설계가 미숙하면 훈련이 실사고가 될 수 있고, 너무 자주 반복하면 팀이 형식적 [[435_checklist_based_testing|체크리스트]]만 수행하게 될 위험도 있다. 따라서 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스는 "자극적인 장애 놀이"가 아니라, 사업 영향이 큰 경로를 우선순위화한 정교한 운영 프로그램이어야 한다.

결론적으로 이 융합의 핵심은 분명하다. **[[658_ir_recovery|복구]] 계획은 읽는 문서가 아니라 주기적으로 [[395_verification_process_review|검증]]되는 능력이어야 하며, 카오스 실험은 그 능력을 수치와 경험으로 [[396_validation|확인]]하는 가장 현실적인 방법이다.** 그래서 좋은 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스 문화는 장애를 줄이는 것뿐 아니라, 장애가 와도 조직이 흔들리지 않게 만든다.

- **📢 섹션 요약 비유**: 좋은 GameDay는 시험 전 모의고사와 같다. 점수를 잘 보이게 꾸미는 행사가 아니라, 어디서 실수하는지 미리 드러내어 본시험에서 무너지지 않게 하는 준비다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[379_dr_architecture|재해 복구]] (Disaster [[658_ir_recovery|Recovery]], [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) | 대규모 장애 뒤 [[090_service_kubernetes_network_load_balancing|서비스]]와 [[001_dikw_pyramid|데이터]]를 복원하는 운영 체계 |
| [[751_chaos_engineering|카오스 엔지니어링]] | 통제된 실패 실험으로 시스템 [[233_recovery_database_restoration_overview|회복]]력을 [[395_verification_process_review|검증]]하는 방법론 |
| [[176_rto_recovery_time_objective|RTO]] | 허용 가능한 [[658_ir_recovery|복구]] 시간 기준 |
| [[177_rpo_recovery_point_objective|RPO]] | 허용 가능한 [[001_dikw_pyramid|데이터]] 손실 시점 기준 |
| 폭발 반경 (Blast [[541_radius_remote_authentication_aaa|Radius]]) | 실험 영향 범위를 제한하는 핵심 안전장치 |
| 런북 (Runbook) | 장애 대응 절차를 실행 가능한 문서로 정리한 자산 |
| 포스트모템 (Postmortem) | 실험 또는 사고 뒤 학습 내용을 구조화하는 회고 절차 |

### 📈 관련 키워드 및 발전 흐름도

```text
탁상형 DR 점검
    │
    ▼
스크립트 기반 복구 훈련
    │
    ▼
관측성 기반 GameDay
    │
    ▼
운영 환경 일부 트래픽 카오스 검증
    │
    ▼
지속적 복원력 검증 · 자동화된 런북 개선
```

### 👶 어린이를 위한 3줄 비유 설명

1. 진짜 불이 나기 전에 학교에서 대피 연습을 하면 어디로 뛰어가야 하는지 몸이 먼저 기억하게 돼요.
2. [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 카오스는 컴퓨터 세상에서 그런 연습을 일부러 해 보는 거예요.
3. 다만 진짜 위험해지지 않게 작은 구역부터 시험하고, 이상하면 바로 멈추는 규칙이 꼭 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 184 / 373

← **이전**: [[183_zero_data_loss_architecture|183. 데이터 손실 제로 (Zero Data Loss) 아키텍처]]
**다음**: [[185_network_jitter|185. 네트워크 지터 (Network Jitter) 및 패킷 손실 관측 메트릭]] →

---
