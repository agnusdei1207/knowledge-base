+++
title = "97. DevOps (Development + Operations) - 문화, 자동화, 측정, 공유"
weight = 97
date = "2026-02-15"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[652_devops_calms_culture|데브옵스]]([[652_devops_calms_culture|DevOps]])는 특정 도구(Tool)나 직무 타이틀이 아니라, 개발(Dev)과 운영(Ops) 간의 [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]])를 허물고 하나의 목표를 향해 협업하게 만드는 조직의 문화이자 철학이다.
> 2. **가치**: 지속적인 자동화와 [[005_feedback_loop|피드백 루프]]를 통해 소프트웨어 배포 주기를 수개월에서 수분 단위로 단축하면서도, 운영 서버의 안정성을 동시에 보장하는 모순을 해결한다.
> 3. **판단 포인트**: [[071_jenkins_ci_cd_pipeline_automation|젠킨스]]([[071_jenkins_ci_cd_pipeline_automation|Jenkins]])나 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]([[205_kubernetes_container_orchestration|Kubernetes]])를 도입한다고 [[652_devops_calms_culture|데브옵스]]가 완성되는 것이 아니며, 실패를 비난하지 않고 측정된 [[001_dikw_pyramid|데이터]]를 바탕으로 지속 개선하는 [[281_calms|CALMS]] 문화 프레임워크 정착이 선행되어야 한다.

---

## Ⅰ. 개요 및 필요성

[[652_devops_calms_culture|데브옵스]]([[652_devops_calms_culture|DevOps]])는 '새로운 기능을 빨리 출시하려는 개발팀(Development)'과 '시스템의 안정을 위해 변화를 거부하는 운영팀(Operations)' 사이의 구조적 갈등을 해결하기 위해 등장한 개념이다.

과거 레거시 환경에서는 개발팀이 코드를 다 짜면 문서를 던지듯 운영팀에 넘겨버렸다. 두 부서의 [[018_kpi|핵심 성과 지표]]([[018_kpi|KPI]])가 정반대였기 때문에, 운영 서버에서 장애가 나면 서로 책임 공방을 벌이는 "혼란의 벽(Wall of Confusion)"이 존재했다. 이로 인해 작은 버그 패치 하나를 배포하는 데도 복잡한 결재와 수주의 대기 시간이 소요되었다. 비즈니스 환경이 급변하고 하루에도 수십 번의 릴리즈가 필요한 [[531_cloud_native_architecture|클라우드 네이티브]] 시대가 오자, 이 거대한 벽을 부수고 두 팀을 한 몸으로 묶어 자동화 파이프라인 위에 올리는 [[652_devops_calms_culture|데브옵스]] 철학이 생존의 필수 조건이 되었다.

- **📢 섹션 요약 비유**: 자동차 조립부(개발)와 판매검수부(운영)가 서로 멱살을 잡고 불량품 책임을 떠넘기던 옛날 공장에서, 두 팀을 같은 라인에 세우고 100% 자동화된 컨베이어 벨트를 깔아버린 전사적 공장 개조 프로젝트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[652_devops_calms_culture|데브옵스]]는 도구의 조합이 아닌 행동의 프레임워크인 **[[281_calms|CALMS]]** 원리로 내부 작동 기전을 설명한다.

| [[281_calms|CALMS]] 기둥 | 영문 | 핵심 원리 및 메커니즘 | 적용 예시 |
| :--- | :--- | :--- | :--- |
| **C (문화)** | Culture | [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]]) 파괴와 남 탓 없는 장애 [[658_ir_recovery|복구]] 문화 | [[206_postmortem_blameless_devops_culture|Blameless Post-mortem]] (비난 없는 사후 분석) |
| **A (자동화)** | Automation | 빌드, 테스트, 인프라 프로비저닝의 스크립트화 | [[090_configuration_item|CI]]/CD 파이프라인 ([[071_jenkins_ci_cd_pipeline_automation|Jenkins]], GitLab [[090_configuration_item|CI]]) |
| **L (린)** | [[087_lean_software_development_7_principles|Lean]] | 불필요한 결재선 제거 및 작은 배치(Batch) 배포 | Value [[467_http2_stream_multiplexing_tcp_hol|Stream]] Mapping을 통한 병목 [[655_ir_detection_analysis|식별]] |
| **M (측정)** | Measurement| 감이나 직관이 아닌 [[001_dikw_pyramid|데이터]] 기반 의사결정 | 모니터링 및 로깅 체계 ([[136_prometheus|Prometheus]], ELK) |
| **S (공유)** | Sharing | 개발과 운영이 스크립트와 지식을 상호 투명하게 공개 | 코드 저장소(Git) 공동 사용 및 지식 위키 공유 |

전통적인 단절 구조와 [[652_devops_calms_culture|데브옵스]]의 [[005_feedback_loop|피드백 루프]] 아키텍처를 비교 시각화한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           전통적 Silo 장벽 vs DevOps 무한 루프 아키텍처          │
├──────────────────────────────────────────────────────────────┤
│ [ 과거: 혼란의 벽 (Wall of Confusion) ]                       │
│    개발팀 (속도!) ─────(코드 투척)───X──▶ 운영팀 (안정!)     │
│    (알아서 배포해)       단절/장애       (우리 서버 터트리지 마)│
│                                                              │
│ [ 현재: DevOps 피드백 루프 ]                                  │
│         ◀──── 지속적 피드백 (모니터링/공유) ─────┐             │
│         │                                      │             │
│   [ Dev (개발/테스트) ] ──(CI/CD 자동화)──▶ [ Ops (배포/운영) ]│
│    - 코드 작성           무중단 컨베이어 벨트    - 인프라 배포       │
│    - 단위 테스트                               - 로깅/모니터링     │
│                                                              │
│ * 핵심: 하나의 툴체인 위에서 작은 변화를 자주, 안전하게 굴린다.    │
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [[652_devops_calms_culture|데브옵스]]가 단절된 부서 간 벽을 어떻게 파이프라인으로 연결하는지를 보여준다. [[652_devops_calms_culture|데브옵스]] 환경에서는 코드가 작성되는 순간부터 빌드, 테스트, 인프라 셋업, [[090_service_kubernetes_network_load_balancing|서비스]] 배포까지의 모든 과정이 인간의 마우스 클릭 없이 로봇(스크립트)에 의해 끊임없이 안전하게 흘러간다.

- **📢 섹션 요약 비유**: 요리사(Dev)가 주방에서 요리를 마치고 웨이터(Ops)에게 그릇을 던지는 대신, 식당 전체를 자동 회전초밥 레일로 개조하여 요리가 완성되자마자 즉시 손님상으로 배달되고 맛 평가가 즉각 주방으로 전달되는 시스템이다.

---

## Ⅲ. 비교 및 연결

[[652_devops_calms_culture|데브옵스]]는 폭포수(Waterfall) 모델의 경직성을 깨고 [[004_agile_relation|애자일]]([[004_agile_relation|Agile]])이 가져온 '개발 속도'를 '운영 환경'까지 매끄럽게 확장시킨 개념이다.

| 비교 항목 | 전통적 IT 운영 ([[062_itil|ITIL]]/폭포수) | [[004_agile_relation|애자일]] ([[004_agile_relation|Agile]]) | [[652_devops_calms_culture|데브옵스]] ([[652_devops_calms_culture|DevOps]]) |
| :--- | :--- | :--- | :--- |
| **포커스 영역** | 프로젝트 계획 및 서버 안정성 | 소프트웨어 개발 속도 최적화 | **코드 개발부터 인프라 운영까지 전체 연결** |
| **배포 주기** | 분기별 또는 연 단위 (거대한 묶음) | 주 단위 ([[067_sprint_timebox|스프린트]]) | **하루 수십 번 ([[076_ci_continuous_integration|지속적 통합]]/배포)** |
| **인프라 환경** | 물리 서버 수동 설치 (Hardware) | (인프라 개념은 약함) | **코드로서의 인프라 ([[793_iac_idempotency_template|IaC]]), [[561_container_based_deployment|컨테이너]]** |
| **실패의 대우** | 치명적인 징계와 책임 추궁 대상 | 빠른 궤도 수정의 기회 | **시스템 개선을 위한 핵심 측정 [[001_dikw_pyramid|데이터]]** |

[[004_agile_relation|애자일]]이 개발팀 내부의 혁신이었다면, [[652_devops_calms_culture|데브옵스]]는 그 혁신의 결과물이 고객에게 닿기까지 막고 있던 인프라팀의 문을 열어젖힌 확장판이다. 최근에는 이 파이프라인 안에 '보안([[283_security_tactics|Security]])' [[395_verification_process_review|검증]] 단계를 끼워 넣어 DevSecOps로 진화하며 보안 체크조차 자동화의 흐름 속에 녹여내고 있다.

- **📢 섹션 요약 비유**: [[004_agile_relation|애자일]]이 "우리 팀 코딩 속도를 스포츠카처럼 빠르게 만들자!"라면, [[652_devops_calms_culture|데브옵스]]는 "그 스포츠카가 꽉 막힌 요금소(운영 배포)에서 멈추지 않도록 하이패스와 자동 차단기까지 설치하자!"라는 인프라 전 구간의 혁신이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[652_devops_calms_culture|데브옵스]]는 실무에서 툴셋 도입만으로 성공할 수 없으며, 조직의 권한 구조와 배포 방식의 완전한 개편을 수반해야 한다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]
1. **코드로서의 인프라 ([[793_iac_idempotency_template|IaC]]) 적용 여부**: 새로운 운영 서버를 띄울 때 아직도 엔지니어가 SSH로 접속해 밤새워 리눅스 패키지를 설치하는가? Terraform이나 [[198_ansible_os_configuration_management_ssh|Ansible]] 등을 이용해 인프라 스펙 자체를 코드로 작성하고 [[288_version_ihl_tos_total_length|버전]] 관리 시스템(Git)에 올려 자동 프로비저닝되게 판단/결정해야 한다.
2. **배포 작은 배치 (Small Batches) 원칙**: 한 달 치 코드를 모아 토요일 새벽에 한 번에 배포(빅뱅 배포)하고 있는가? 장애 발생 시 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 추적이 불가능하다. 변경 사항을 극도로 잘게 쪼개어 하루에도 수차례 자동화 배포를 태워 파급 반경(Blast [[541_radius_remote_authentication_aaa|Radius]])을 최소화해야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 개발팀과 운영팀의 분리 구조는 그대로 둔 채 중간에 **'[[652_devops_calms_culture|데브옵스]]팀'**이라는 새로운 부서를 하나 더 만드는 행위. 이는 [[002_silo_hyeonhyung|사일로]]를 허무는 게 아니라 벽을 하나 더 추가하는 최악의 아키텍처 역행이다.

- **📢 섹션 요약 비유**: 자전거 타는 법(문화)을 모른 채 가장 비싼 선수용 자전거(자동화 툴)를 사 준다고 빨리 달릴 수 없다. [[652_devops_calms_culture|데브옵스]]는 도구를 사기 전에 두 부서가 같이 페달을 밟는 연습부터 해야 성공한다.

---

## Ⅴ. 기대효과 및 결론

[[652_devops_calms_culture|데브옵스]]가 완벽히 정착되면 넷플릭스나 아마존처럼 하루에 수천 번 배포를 하면서도 [[090_service_kubernetes_network_load_balancing|서비스]] 장애율을 기적적으로 떨어뜨릴 수 있다. 개발자는 인프라 고민 없이 코딩에 집중하고, 운영자는 반복된 수동 설치 작업에서 해방되어 시스템 고도화에 집중할 수 있다.

궁극적으로 [[652_devops_calms_culture|데브옵스]]는 소프트웨어가 아이디어에서 가치로 변환되어 고객에게 도달하는 [[085_lead_time_cycle_time|리드 타임]]([[085_lead_time_cycle_time|Lead Time]])을 극단적으로 압축하는 비즈니스 무기다. 도구는 계속 바뀌겠지만, "개발과 운영을 하나의 [[005_feedback_loop|피드백 루프]]로 융합한다"는 본질적 문화는 [[531_cloud_native_architecture|클라우드 네이티브]] 아키텍처가 존재하는 한 변하지 않을 영원한 뼈대다.

- **📢 섹션 요약 비유**: [[652_devops_calms_culture|데브옵스]]는 100미터 달리기 선수의 다리(개발)와 심장(운영)이 서로 자기가 중요하다고 싸우는 것을 끝내고, 뇌의 명령(자동화) 하나로 호흡을 완벽하게 일치시켜 결승선으로 질주하게 만든 기적의 신체 교정술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[090_configuration_item|CI]]/CD ([[076_ci_continuous_integration|지속적 통합]]/[[099_continuous_deployment_cd|지속적 배포]])** | [[652_devops_calms_culture|데브옵스]]의 자동화(Automation) 철학을 구현하는 구체적인 파이프라인 실천 기술 |
| **[[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]])** | 거대한 모놀리식 시스템을 작게 쪼개어 [[652_devops_calms_culture|데브옵스]] 소규모 배포([[087_lean_software_development_7_principles|Lean]])를 기술적으로 뒷받침하는 구조 |
| **[[100_sre_site_reliability_engineering_error_budget|SRE]] (사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 엔지니어링)** | [[652_devops_calms_culture|데브옵스]]의 추상적인 철학을 구체적인 시스템 엔지니어링 직무와 [[001_dikw_pyramid|데이터]] 지표([[102_sli_slo_service_level_indicator_objective|SLI]]/[[181_slo_service_level_objective|SLO]])로 구현한 구글의 방법론 |
| **[[793_iac_idempotency_template|IaC]] (코드로서의 인프라)** | 하드웨어 인프라 셋업을 소프트웨어 코드처럼 다루어 [[652_devops_calms_culture|데브옵스]]의 재현성과 공유(Sharing)를 강화하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
폭포수 (단절된 개발과 인프라)
    │
    ▼
애자일 (개발 속도의 혁신)
    │
    ▼
데브옵스 (개발부터 운영까지의 자동화 융합, CALMS)
    │
    ▼
DevSecOps (파이프라인 내 보안 자동 검증 통합)
    │
    ▼
AIOps / NoOps (AI를 활용한 이상 탐지 및 완전 무인 운영)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날에는 레고를 만드는 팀과 성이 안 부서지게 지키는 팀이 서로 자기 일만 하다가 맨날 싸웠어요.
2. [[652_devops_calms_culture|데브옵스]]는 이 두 팀을 한 팀으로 묶고, "버튼 하나만 누르면 로봇이 레고를 멋지게 조립해 주는 마법 기계"를 같이 만들게 했어요.
3. 그래서 이제는 레고 성이 부서질 걱정 없이 하루에도 수십 번씩 새롭고 멋진 장난감을 뚝딱뚝딱 완성해서 친구들에게 보여줄 수 있게 되었답니다!
