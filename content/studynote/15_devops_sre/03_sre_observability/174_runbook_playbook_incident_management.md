---
title: "Runbook/Playbook"
date: "2026-04-21"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 런북 (Runbook)은 특정 알람·장애 유형에 대한 <strong>실행 절차 문서</strong>이고, [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/) ([Playbook](/studynote/09_security/13_secops_ir_forensics/637_playbook/))은 여러 런북과 커뮤니케이션 규칙을 묶어 <strong><a href="/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/">인시던트 대응</a> 전체를 지휘하는 운영 시나리오</strong>다.
> 2. **가치**: 좋은 런북/[플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 전문가의 기억을 문서와 자동화로 옮겨, Mean Time To [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) ([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))를 사람 의존형에서 절차 의존형으로 바꾼다.
> 3. **판단 포인트**: 문서는 설명서가 아니라 행동 지시서여야 한다. <strong>명령, 기대 결과, 분기 조건, 에스컬레이션 기준</strong>이 없다면 위기 상황에서 거의 쓸모가 없다.

---

## Ⅰ. 개요 및 필요성

[인시던트 대응](/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/)은 기술 문제이면서 동시에 [인지 부하](/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/) 문제다. 알람이 새벽에 울렸을 때 운영자는 원인 파악, 임시 조치, 영향 범위 판단, [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 커뮤니케이션을 동시에 처리해야 한다. 이때 경험 많은 엔지니어 한 명의 기억에만 기대면, 담당자가 바뀌거나 압박이 큰 상황에서 대응 품질이 급격히 흔들린다.

런북은 이런 불확실성을 줄이는 가장 기본적인 장치다. 특정 증상에 대해 "무엇을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 어떤 명령을 실행하며, 결과가 A면 어디로 가고 B면 누구를 호출하는가"를 정리해 둔 문서이기 때문이다. 반면 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 [Severity](/studynote/04_software_engineering/06_software_architecture/354_defect_severity_priority/)(심각도) 판정, Incident Commander 지정, 상황실 개설, 고객 공지, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)까지 포함해 <strong>사람과 절차 전체를 조율하는 상위 문서</strong>다.

아래 그림은 문서가 없는 대응과 있는 대응의 차이를 단순화한 것이다.

```text
+--------------------------------------------------------------------+
|                Incident response with and without docs             |
+-----------------------+--------------------------------------------+
| No runbook            | With runbook / playbook                   |
+-----------------------+--------------------------------------------+
| alert -> guess ->     | alert -> triage -> runbook branch ->      |
| ask expert -> retry   | mitigation -> playbook communication      |
| => slow, inconsistent | => repeatable, auditable                  |
+-----------------------+--------------------------------------------+
```

즉 런북/[플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)의 목적은 문서를 예쁘게 남기는 것이 아니라, 위기 상황에서 "다음 행동"을 즉시 제공하는 것이다. 특히 [Site Reliability 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/))에서는 [인시던트 대응](/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/) 시간이 비용이므로, 진단과 의사결정 시간을 줄이는 문서가 곧 운영 품질이 된다.

- **📢 섹션 요약 비유**: 비행기 조종사는 비상 상황에서 머릿속 기억만 믿지 않고 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)를 펼친다. 런북과 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)도 같은 이유로 존재한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

런북과 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 보통 계층 구조로 설계된다. 가장 아래에는 알람별 런북이 있고, 그 위에는 심각도별 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)이 있으며, 필요하면 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/), Automation, and Response ([SOAR](/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/))나 [ChatOps](/studynote/13_cloud_architecture/04_devops_observability/207_chatops_slack_bot_deployment/) 자동화가 일부 단계를 대신한다. 중요한 것은 문서 간 역할 분리다. 런북은 "기술적 조치"를, [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 "조직적 대응"을 담당해야 한다.

```text
+----------------------------------------------------------------------+
|                  Layered incident documentation                      |
+----------------------------------------------------------------------+
| Alert catalog                                                        |
|    |                                                                 |
|    +- Runbook: check command -> expected output -> next branch       |
|    |                                                                 |
|    +- Playbook: severity -> roles -> comms -> escalation             |
|    |                                                                 |
|    +- Automation: SOAR / script / runbook-as-code                    |
|                                                                      |
| Postmortem feedback updates both runbook and playbook                |
+----------------------------------------------------------------------+
```

좋은 런북에는 최소한 다음이 들어가야 한다.

| 항목 | 런북에서의 역할 | 빠지면 생기는 문제 |
| :--- | :--- | :--- |
| Trigger | 어떤 알람·증상을 위한 문서인지 명시 | 잘못된 상황에 엉뚱한 절차 적용 |
| Impact | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 영향과 우선순위 판단 | 사소한 문제에 과잉 대응 또는 반대 상황 |
| [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) | 복사 가능한 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)/[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 명령 | 현장 엔지니어가 다시 추측해야 함 |
| Expected Result | 정상/비정상 기준 | 결과를 봐도 다음 행동을 모름 |
| Branch | A/B 분기와 다음 단계 | [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)가 아닌 설명문으로 전락 |
| Escalation | 누구를 언제 호출할지 | 늦은 협업, 책임 공백 |
| [Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/) / [Verification](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 조치 후 되돌림과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 임시 조치가 새 장애를 만듦 |

[플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 여기서 한 단계 올라가서 역할을 정의한다. 누가 Incident Commander인지, 고객 공지를 누가 하는지, 얼마나 자주 상황을 공유할지, 법무·보안·경영진 보고가 필요한 조건이 무엇인지 같은 내용이 포함된다. 즉 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 기술 절차를 넘어 <strong>의사결정 권한과 커뮤니케이션 경로</strong>를 정하는 문서다.

최근에는 Runbook-[as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-[Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 형태도 중요해지고 있다. 정형화된 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차는 YAML, Python, [Ansible](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) 등으로 자동 실행할 수 있고, 사람은 승인과 분기 판단에 집중할 수 있다. 다만 자동화는 "예측 가능한 저위험 조치"부터 시작해야 하며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제나 광범위 재시작처럼 위험한 조치는 수동 승인 단계를 남기는 편이 안전하다.

- **📢 섹션 요약 비유**: 런북은 레시피 한 장이고, [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 주방 전체 운영표다. 요리법만 있어도 안 되고, 누가 조리하고 누가 손님에게 설명할지도 함께 정해져야 식당이 돌아간다.

---

## Ⅲ. 비교 및 연결

런북과 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 자주 혼용되지만 목적이 다르다. 런북은 특정 알람에 바로 대응하기 위한 "실행 단위"이고, [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 여러 런북을 포함해 인시던트 전체 흐름을 조직하는 "시나리오 단위"다. Standard Operating Procedure (SOP)나 위키와도 구분해야 한다.

| 문서 유형 | 핵심 질문 | 주 독자 | 특징 |
| :--- | :--- | :--- | :--- |
| Runbook | 지금 무엇을 실행할까 | 온콜 엔지니어 | 명령·분기·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 중심 |
| [Playbook](/studynote/09_security/13_secops_ir_forensics/637_playbook/) | 누가 어떤 순서로 대응할까 | Incident Commander, 팀 리더 | 역할·커뮤니케이션 중심 |
| SOP | 평상시 표준 절차는 무엇인가 | 운영팀 전체 | 반복 업무 기준 |
| Wiki / [ADR](/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/) | 시스템이 왜 이렇게 설계됐는가 | 개발·운영 전원 | 배경 설명 중심 |
| Postmortem | 무엇이 왜 실패했는가 | 조직 전체 | 학습과 개선 중심 |

이 문서들은 서로 연결되어야 한다. Alert는 런북 링크를 가져야 하고, Severity가 높아지면 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)이 자동으로 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되어야 하며, 인시던트 종료 후 Postmortem은 다시 런북과 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)을 수정하는 입력이 되어야 한다. 이 [피드백 루프](/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)가 없으면 문서는 금방 낡는다.

또한 런북은 [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)), 알람 설계, [ChatOps](/studynote/13_cloud_architecture/04_devops_observability/207_chatops_slack_bot_deployment/), SOAR와 직접 연결된다. 알람이 너무 모호하면 어떤 런북도 쓸모없고, 반대로 런북이 명확하면 일부 알람은 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)로 승격할 수 있다. 결국 좋은 문서는 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 품질과 자동화 수준을 함께 끌어올리는 기반 자산이다.

즉 비교의 핵심은 문서 종류 자체가 아니라, <strong>어떤 문서가 어떤 순간의 의사결정 비용을 줄이는가</strong>에 있다.

- **📢 섹션 요약 비유**: 여행 가이드북, 지하철 노선도, 비상 대피 안내문은 모두 종이지만 쓰는 순간이 다르다. 위기 때는 예쁜 설명보다 바로 행동할 수 있는 안내문이 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "모든 알람에 런북이 있는가"보다 "그 런북이 실제로 동작하는가"가 더 중요하다. [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 바뀌었거나 팀 이름이 바뀌었거나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구조가 바뀌었는데 문서가 예전 상태라면, 위기 상황에서 오히려 잘못된 자신감을 준다. 그래서 작성보다 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 갱신 체계를 먼저 설계해야 한다.

```text
+--------------------------------------------------------------------+
|                  Practical incident decision flow                  |
+--------------------------------------------------------------------+
| alert fired                                                         |
|   |                                                                 |
|   +- known pattern + reversible action? -> runbook / auto-remediate |
|   +- cross-team or high blast radius? -> invoke playbook            |
|   +- no clear diagnosis in time box? -> escalate                     |
|   +- after recovery -> verify -> postmortem -> update docs          |
+--------------------------------------------------------------------+
```

실무 판단 포인트는 다음과 같다.

1. **명령은 복사 가능해야 한다**: "DB 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"이 아니라 실행 명령과 예상 출력 예시가 들어가야 한다.
2. **시간 제한을 둔다**: 10분 내 미해결, 고객 영향 확대, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 의심 같은 에스컬레이션 조건이 있어야 한다.
3. **자동화 후보를 선별한다**: 반복되고 되돌리기 쉬운 조치는 Runbook-[as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-Code로 전환하고, 위험한 조치는 수동 승인 단계를 둔다.
4. <strong>게임 데이로 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>한다</strong>: 문서를 작성한 사람이 아니라 신규 팀원이 따라 해도 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)되는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.
5. <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리한다</strong>: 코드와 같이 Pull Request로 리뷰하고, 시스템 변경과 함께 업데이트한다.

운영 지표도 중요하다. 런북 커버리지, 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 성공률, 문서 최신화 주기, 런북 사용 후 [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 감소율, 잘못된 자동화로 인한 추가 장애율을 함께 봐야 한다. 특히 "문서는 있는데 아무도 안 쓴다"는 상황은 문서 품질이 아니라 알람 품질, [접근성](/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/), 검색성 문제일 수 있다.

기술사 답안에서는 런북을 단순 매뉴얼로 끝내지 말고, <strong>실행 가능성(Actionability), 시간 제한, 역할 분리, 자동화 범위, Postmortem 피드백</strong>을 함께 써야 설계 관점이 살아난다. [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)까지 묻는 문제라면 반드시 Incident Commander, 커뮤니케이션, [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 보고 구조를 포함해야 한다.

- **📢 섹션 요약 비유**: 소방 훈련도 소화기 위치만 적어 두면 부족하다. 누가 119에 전화하고 누가 사람들을 대피시키며 누가 전원을 끌지까지 정해져야 실제 화재 때 움직일 수 있다.

---

## Ⅴ. 기대효과 및 결론

잘 관리된 런북/[플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/) 체계는 단순히 대응 시간을 줄이는 것을 넘어, 조직의 운영 기억을 표준화한다. 숙련자 한 명의 경험이 팀 전체의 자산이 되고, 야간 온콜의 불안이 줄며, 커뮤니케이션 품질도 일정해진다. 자동화 가능한 절차는 점차 SOAR나 스크립트로 넘어가고, 사람은 더 복잡한 판단에 집중할 수 있다.

물론 한계도 있다. 문서가 오래되면 독이 되고, 자동화가 과도하면 잘못된 조치를 대규모로 반복할 위험이 있다. 또한 한 번도 훈련하지 않은 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 위기 시 거의 읽히지 않는다. 따라서 성공 조건은 "문서 보유"가 아니라 <strong>현행성, 훈련, <a href="/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/">접근성</a>, 자동화 경계 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>이다.

결국 런북과 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 운영 문서가 아니라 <strong><a href="/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/">인시던트 대응</a> 시스템의 일부</strong>다. 좋은 문서는 사람의 기억을 대체하는 것이 아니라, 압박 상황에서도 올바른 다음 행동을 꺼내 주는 운영 인터페이스로 기능한다.

- **📢 섹션 요약 비유**: 낯선 도시에서 길을 찾을 때 머릿속 감에만 의존하면 헤매기 쉽다. 신뢰할 수 있는 지도와 안내 체계가 있으면 누구라도 비슷한 속도로 목적지에 도착할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Alert Triage | 어떤 런북을 열어야 하는지 결정하는 첫 관문 |
| Runbook | 특정 장애 유형에 대한 기술적 실행 절차 |
| [Playbook](/studynote/09_security/13_secops_ir_forensics/637_playbook/) | 역할·커뮤니케이션·에스컬레이션을 포함한 상위 대응 시나리오 |
| Incident Commander | 고심각도 인시던트에서 의사결정을 조율하는 역할 |
| Runbook-[as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-[Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) | 반복 조치를 자동화 가능한 형태로 전환한 운영 방식 |
| Postmortem | 대응 후 문서와 시스템을 개선하는 학습 루프 |
| [SOAR](/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/) | 문서 기반 절차를 자동 실행·승인 흐름으로 확장하는 플랫폼 |

### 📈 관련 키워드 및 발전 흐름도

```text
Expert memory and ad-hoc response
    |
    v
Alert-linked runbooks
    |
    v
Severity-based playbooks and incident command
    |
    v
Runbook-as-Code / SOAR automation
    |
    v
Postmortem-driven continuous update loop
```

### 👶 어린이를 위한 3줄 비유 설명

1. 런북은 "이 알람이 울리면 이렇게 해요"라고 적힌 자세한 레시피예요.
2. [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)은 여러 레시피를 모아 두고, 누가 무엇을 맡을지도 적어 둔 큰 작전판이에요.
3. 그래서 갑자기 문제가 생겨도 당황하지 않고 차례대로 움직일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 174 / 373

<- **이전**: [173. 마이크로버스트 트래픽 스파이크 탐지 (Microburst Traffic Spike Detection)](/studynote/15_devops_sre/03_sre_observability/173_microburst_traffic_spike_detection/)
**다음**: [175. 시스템 경계 완충지대 텔레메트리 (Buffer/Queue Telemetry)](/studynote/15_devops_sre/03_sre_observability/175_buffer_queue_telemetry/) ->

---
