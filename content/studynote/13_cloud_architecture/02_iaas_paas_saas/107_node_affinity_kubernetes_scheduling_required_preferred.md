+++
title = "107. 노드 어피니티 (Node Affinity) - K8s 스케줄링 유도"
date = 2026-04-10

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 노드 어피니티 (Node [Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/))는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))가 자신이 실행될 노드(Node)의 조건을 명시하여, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 특정 라벨(Label)을 가진 노드에 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 배치하도록 유도하는 규칙이다.
> 2. **가치**: 특정 워크로드(예: [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 필요, 특정 지역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 법규 준수)를 물리적/논리적으로 적합한 인프라에 정확히 배치하여 가용성과 규제 준수성을 보장한다.
> 3. **판단 포인트**: '반드시 충족해야 하는 강제 조건(Required)'과 '가급적 충족하면 좋은 선호 조건(Preferred)' 중 서비스의 중단 허용성과 인프라 유연성을 고려하여 적절한 강도를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

노드 어피니티 (Node [Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/))는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터 내에서 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 특정 노드를 선택하는 정교한 매칭 메커니즘이다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 단순한 `nodeSelector`는 일치하는 라벨이 없으면 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 영원히 대기 상태(Pending)에 빠지는 한계가 있었다. 이를 극복하기 위해 OR 조건, 크기 비교, 유연한 선호도 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 등 복잡한 스케줄링 요구사항을 수학적으로 처리할 수 있는 노드 어피니티가 등장했다.

규모가 큰 클러스터일수록 노드의 하드웨어 스펙([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), 고속 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))이나 물리적 위치(EU, US)가 다양해진다. 이러한 이기종 환경에서 애플리케이션의 특성에 맞는 노드에 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 배치하지 않으면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하나 법적 문제가 발생할 수 있다. 노드 어피니티는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 스스로가 "나는 이런 조건의 노드에서 돌아가야 해"라고 선언함으로써 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 최적의 짝짓기를 수행하게 만든다.

- **📢 섹션 요약 비유**: 부동산에서 집을 구할 때, "반드시 강남에 있고, 남향이어야 하며, 엘리베이터가 있으면 더 좋겠다"고 중개사([스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))에게 구체적인 매물 조건을 요구하는 세입자의 체크리스트와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

노드 어피니티는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 명세(Spec)에 작성되며, [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 이를 읽고 노드의 라벨과 연산자(`In`, `NotIn`, `Exists` 등)를 통해 조건을 평가한다. 가장 중요한 것은 조건의 '강도(Strength)'와 '실행 중 변경 시 처리 방법(Execution phase)'이다.

```text
┌──────────────────────────────────────────────────────────────┐
│         Node Affinity: 스케줄러의 노드 필터링 및 점수화      │
├──────────────────────────────────────────────────────────────┤
│ [파드 생성 요청] ─▶ API Server ─▶ [Kube-Scheduler]          │
│                                           │                  │
│  1. Required (강제 필터링)                │                  │
│     - 조건 불일치 노드는 후보에서 제외 ◀──┘                  │
│                                           │                  │
│  2. Preferred (선호도 점수화)             ▼                  │
│     - 통과된 노드들에 가중치 합산 ───▶ [최고 점수 노드 선택] │
└──────────────────────────────────────────────────────────────┘
```

1. **강제 조건 (Required)**: `requiredDuringSchedulingIgnoredDuringExecution`
   - 스케줄링 시점에 **반드시** 만족해야 한다. 조건을 만족하는 노드가 없으면 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 스케줄링되지 않는다(Pending).
2. **선호 조건 (Preferred)**: `preferredDuringSchedulingIgnoredDuringExecution`
   - 스케줄링 시점에 **가급적** 만족하려고 시도한다. 각 조건에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(1~100)를 부여하며, 모든 조건을 만족하는 노드가 없더라도 가장 점수가 높은 노드에 차선으로 배치된다.
3. **IgnoredDuringExecution**:
   - 이미 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 노드에 배치되어 실행 중일 때 노드의 라벨이 변경되어 조건이 틀어지더라도, [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 쫓아내지 않고 <strong>무시</strong>한다. (안정성 우선)

- **📢 섹션 요약 비유**: 소개팅에서 "키 180cm 이상은 절대 포기 못해(Required)"라고 필터링한 후, 남은 사람들 중에서 "성격 좋은 사람(Preferred, [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))"에게 점수를 매겨 최종 1명을 고르는 과정이다.

---

## Ⅲ. 비교 및 연결

스케줄링을 통제하는 대표적인 두 가지 방법인 [테인트](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/)/톨러레이션과 노드 어피니티는 서로 반대되는 관점을 가진다.

| 비교 항목 | 노드 어피니티 (Node [Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/)) | [테인트](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/)와 톨러레이션 (Taints and Tolerations) |
| :--- | :--- | :--- |
| **주체와 방향** | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) ─▶ 노드 (끌어당김, Attraction) | 노드 ─▶ [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) (밀어냄, Repulsion) |
| **목적** | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 **특정 노드에** 배치하고 싶을 때 | 특정 노드에 <strong>아무 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/">파드</a>나 들어오는 것을</strong> 막을 때 |
| **실패 시 결과** | 조건 불일치 시 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배치 실패 | 톨러레이션 없으면 노드 진입 불가 |
| **결합 사용** | "나는 전용 DB 서버에만 갈래" | "여기는 전용 DB 서버니 딴 놈들 오지마" |

두 기능을 함께 사용하면 완벽한 격리 환경을 만들 수 있다. 노드에 [테인트](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/)를 걸어 불순물 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 차단하고, 특정 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 톨러레이션(면역)과 어피니티(목적지 지향)를 동시에 부여하면, 오직 그 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)만이 전용 노드에 단독으로 배치된다.

- **📢 섹션 요약 비유**: 노드 어피니티가 세입자가 콕 찍어 "저 방으로 갈래" 하는 것이라면, [테인트](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/)는 방주인이 "애완동물 금지!" 라고 방어막을 치는 것이다. 두 개가 결합되면 완벽한 맞춤형 독채가 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 노드 어피니티를 설계할 때는 인프라의 가용성을 무너뜨리지 않는 선에서 강도(Required vs Preferred)를 선택해야 한다.

1. **Required의 위험성**: 고가용성(HA)이 필요한 웹 서버 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 `Required`로 특정 존(Zone)만 고집하게 만들면, 해당 존에 장애가 났을 때 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 다른 존으로 대피하지 못하고 서비스가 중단된다. 규제([데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/))나 물리적 장비([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))가 필수인 경우가 아니면 남용을 피해야 한다.
2. **Preferred를 활용한 유연성**: 일반적인 워크로드는 `Preferred`를 사용하여 "[SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 노드면 좋고, 꽉 차면 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 노드라도 가서 실행은 되게 해라"식으로 설계해야 장애 저항성이 높아진다.
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: `nodeSelector`와 `Node Affinity`를 섞어 쓰는 경우. 룰이 충돌하여 스케줄링 실패 원인을 파악하기 매우 어려워진다. 최신 스펙인 Affinity로 통일해야 한다.

- **📢 섹션 요약 비유**: 깐깐한 조건(Required)만 고집하다간 묵을 방이 없어 길바닥에서 밤을 새우게 된다(Pending). 생존이 우선이라면 적당한 타협(Preferred)을 할 줄 알아야 진짜 인프라 고수다.

---

## Ⅴ. 기대효과 및 결론

노드 어피니티를 도입하면 이기종 클러스터의 자원 활용 효율을 극대화할 수 있다. 비싼 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 노드에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 워크로드만 올리고, 일반 노드에는 가벼운 웹 서버를 올리는 식의 정밀한 자원 배분이 가능해진다.

그러나 스케줄링 규칙이 복잡해질수록 클러스터 유지보수 난이도는 상승한다. 관리자가 실수로 노드의 라벨을 잘못 변경하면 향후 배포되는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들이 엉뚱한 곳으로 가거나 대기 상태에 빠질 수 있다. 결론적으로 노드 어피니티는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 자동 스케줄링 기능에 '인간의 비즈니스적 의도'를 개입시키는 강력한 도구이므로, 반드시 명확한 아키텍처 원칙 하에 사용되어야 한다.

- **📢 섹션 요약 비유**: 노드 어피니티는 자율주행 자동차([스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))에게 네비게이션 목적지(어피니티)를 찍어주는 것이다. 목적지를 똑바로 입력하면 편안하게 도착하지만, 잘못 입력하면 차가 길을 잃고 멈춰버린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **NodeSelector** | 노드 어피니티 이전의 구형 스케줄링 유도 방식 (단순 매칭) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/">Taint</a> &amp; Toleration</strong> | 노드가 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 쫓아내는 방어적 스케줄링 기법 (밀어내기) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/">Pod</a> <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/">Affinity</a> / Anti-<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/">Affinity</a></strong> | 노드가 아닌 '[파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간'의 관계를 따져 같이 띄울지 찢어놓을지 결정 |
| **Label & Annotation** | 노드 어피니티가 판단의 기준으로 삼는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 키-값 쌍 |

### 📈 관련 키워드 및 발전 흐름도

```text
NodeSelector (단순 라벨 매칭)
    │
    ▼
Node Affinity (연산자, 강제/선호 조건 도입)
    │
    ▼
Taint & Toleration (노드 차원의 방어선 구축)
    │
    ▼
Pod Affinity / Anti-Affinity (파드 간 결합/분리 규칙 확장)
    │
    ▼
Custom Scheduler / Descheduler (동적 스케줄링 및 재배치 최적화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)(손님)가 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 호텔에 와서 "저는 꼭 수영장이 있는 방으로 주세요!"라고 요구하는 게 노드 어피니티예요.
2. "수영장 없으면 절대 안 자!"라고 떼쓰는 건 강제 조건(Required)이에요.
3. "수영장 있으면 좋은데, 없으면 그냥 아무 방이나 주세요~" 하는 건 융통성 있는 선호 조건(Preferred)이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 106 / 371

← **이전**: [106. 테인트(Taint)와 톨러레이션(Toleration) - K8s 스케줄링 제어](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/106_taint_toleration_kubernetes_node_scheduling_repel/)
**다음**: [108. K8s 프로브(Probes) 생명주기 관리](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/108_kubernetes_probes_liveness_readiness_startup_health_check/) →

---
