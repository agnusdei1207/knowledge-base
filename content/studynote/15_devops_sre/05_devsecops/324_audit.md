+++
title = "Chaos Engineering"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [Chaos Engineering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/) ([카오스 엔지니어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/))은 프로덕션 시스템에 의도적 장애를 주입해 시스템의 약점을 사전에 발견하는 규율이다.
> - [Steady State Hypothesis](/knowledge-base/studynote/15_devops_sre/03_sre_observability/151_steady_state_hypothesis_validation/) (정상 상태 가설)을 정의하고, 실험 후 시스템이 가설을 유지하는지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 과학적 방법론이다.
> - Netflix가 2011년 Chaos Monkey를 공개하며 시작됐고, 현재 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) [에코](/knowledge-base/studynote/03_network/01_data_communication/031_에코_반향/)시스템에서 광범위하게 적용된다.

---

## Ⅰ. [Chaos Engineering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/) 원칙

카오스 실험 5단계:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">1. Steady State 정의 → SLI 기준 정상 상태 지표 선정</div>
<div class="kb-diagram-note">2. 가설 설정 → "노드 하나 장애나도 응답률 99% 유지"</div>
<div class="kb-diagram-note">3. 실험 설계 → 실패 유형 선택</div>
<div class="kb-diagram-note">4. 실험 실행 → 최소 폭발 반경으로 시작 → 점진적 확대</div>
<div class="kb-diagram-note">5. 결과 분석 → Steady State 벗어난 경우 취약점 발견</div>
</div>
</div>



> 📢 **Ⅰ 섹션 요약 비유**
> [카오스 엔지니어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)은 소방 훈련 — 실제 화재 전에 연기를 피워 대피 경로와 소화 시스템을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

---

## Ⅱ. 주요 장애 주입 유형

| 장애 유형          | 예시                                     |
|--------------------|------------------------------------------|
| [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)/[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 종료  | 랜덤 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 삭제                           |
| [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)       | 특정 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 200ms [latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 주입        |
| 네트워크 패킷 손실  | 30% 패킷 드롭                            |
| 노드 장애           | 워커 노드 중단                           |
| CPU/메모리 포화     | 리소스 고갈 시뮬레이션                   |
| 클라우드 AZ 장애    | 전체 가용 영역 트래픽 차단               |

> 📢 **Ⅱ 섹션 요약 비유**
> 장애 주입은 예방주사 — 약한 형태의 병원균을 넣어 항체(내성)를 키운다.

---

## Ⅲ. 도구 생태계

| 도구         | 특징                                       |
|--------------|--------------------------------------------|
| [Chaos Monkey](/knowledge-base/studynote/15_devops_sre/03_sre_observability/149_chaos_monkey_chaos_mesh/) | Netflix [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), EC2 랜덤 종료            |
| LitmusChaos  | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 프로젝트, K8s 네이티브 카오스         |
| Chaos [Mesh](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)   | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 인큐베이팅, 네트워크 장애 특화        |
| Gremlin      | 상용 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/), 엔터프라이즈 기능               |
| AWS FIS      | AWS [Fault Injection](/knowledge-base/studynote/02_operating_system/10_security/670_fault_injection_chaos_testing_kernel/) Simulator              |

GameDay (게임데이): 전체 팀이 참가해 대규모 장애 시나리오를 실제로 실행하는 훈련 이벤트.

> 📢 **Ⅲ 섹션 요약 비유**
> LitmusChaos는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경의 소방청 — 훈련 시나리오를 체계적으로 관리하고 결과를 리포트한다.

---

## Ⅳ. 카오스 실험의 안전 원칙

1. **최소 폭발 반경**: 스테이징 → 운영 일부 → 전체 순으로 확대
2. **자동 중단 장치**: Steady [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 벗어나면 실험 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)
3. **비즈니스 영향 최소화**: 저트래픽 시간대 실행
4. **팀 공지**: 실험 전 On-[call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) 팀에 사전 통보



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">카오스 실험 안전 게이트</div>
<div class="kb-diagram-note">Staging → Canary(5%) → 25% → 50% → 100%</div>
<div class="kb-diagram-note">자동 중단 조건 항상 활성화</div>
</div>
</div>



> 📢 **Ⅳ 섹션 요약 비유**
> 카오스 실험은 다이너마이트 폭파 훈련 — 항상 안전거리를 확보하고, 비상 정지 버튼을 손에 쥔 채 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)한다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소              | 역할                                      |
|------------------------|-------------------------------------------|
| [Chaos Engineering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)      | 의도적 장애 주입으로 내성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)           |
| [Steady State Hypothesis](/knowledge-base/studynote/15_devops_sre/03_sre_observability/151_steady_state_hypothesis_validation/)| 정상 상태 기준 지표 정의                  |
| Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/)           | 실험으로 영향받는 범위                    |
| [Chaos Monkey](/knowledge-base/studynote/15_devops_sre/03_sre_observability/149_chaos_monkey_chaos_mesh/)           | Netflix의 최초 카오스 도구                |
| LitmusChaos            | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) K8s 네이티브 카오스 프레임워크       |
| GameDay                | 대규모 팀 장애 시나리오 훈련 이벤트      |

### 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Chaos Engineering</div>
<div class="kb-diagram-tree-item" style="--depth:2">Steady State Hypothesis → 실험 기준 정의</div>
<div class="kb-diagram-tree-item" style="--depth:2">장애 주입 → 네트워크/파드/노드/리소스</div>
<div class="kb-diagram-tree-item" style="--depth:2">LitmusChaos / Chaos Mesh → K8s 네이티브 도구</div>
<div class="kb-diagram-tree-item" style="--depth:2">GameDay → 팀 규모 장애 훈련</div>
<div class="kb-diagram-tree-item" style="--depth:2">Resilience Engineering → 장애 내성 시스템 설계</div>
</div>
</div>



> 🧒 **어린이 비유**
> [카오스 엔지니어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)은 레고 성이 얼마나 튼튼한지 보려고 일부러 블록 하나를 빼보는 것이에요. 그래도 성이 무너지지 않으면 합격!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 324 / 373

← **이전**: [Prometheus Grafana Monitoring](/knowledge-base/studynote/15_devops_sre/05_devsecops/323_process/)
**다음**: [325. DevSecOps 시프트 레프트 보안 조기 점검 (DevSecOps Shift-Left Security STRIDE Threat](/knowledge-base/studynote/11_design_supervision/06_exam_summary/325_audit/) →

---
