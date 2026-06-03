+++
title = "14. 동시성 (Concurrency) - 프로세스 모델을 통한 스케일 아웃(Scale-out) 수평 확장"
date = 2026-04-05

[taxonomies]
tags = ["devops_sre"]

[extra]
tags = ["devops_sre"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동시성 원칙은 애플리케이션을 여러 독립적 프로세스(또는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))로 구성하여, 각각이 동시에 처리할 수 있는 요청 수를 늘리는 것이 아니라 프로세스 인스턴스를 늘려 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 극대화해야 한다는 12팩터 앱의 제8원칙이다.
> 2. **가치**: 동시성 원칙을 적용하면 트래픽 변동에 유연하게 대응할 수 있고, 특정 인스턴스 장애가 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 영향을 주지 않으며, 시스템 리소스를보다 효율적으로 활용할 수 있다.
> 3. **융합**: [컨테이너 오케스트레이션](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)), 오토스케일링, 그리고 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)아키텍처의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 긴밀하게 연결되어 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

동시성([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/))는 컴퓨터 과학에서 동일한 시간대에수의처리이/가실행된다을/를 의미한다. 소프트웨어 시스템의에서는、 동시성은 두 가지 접근법으로 구현된다: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 기반처리()와 프로세스 기반의 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))이다.

전통적인 웹 애플리케이션에서는Apache Prefork MPM이나 IIS의 프로세스 모델처럼, 하나의한 프로세스가 모든 요청을 처리하려 했던 경우가 많았다. 이 방식은 다음과 같은 한계를 가졌다:

- **확장성의 한계**: 단일 프로세스의처리에는이/가、 이를 넘어서면 전체 시스템을 업그레이드해야 했다(Vertical Scaling, 수직 확장).
- **안정성 문제**: 단일 프로세스가 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/)나 예외로 종료되면 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 중단된다.
- **리소스 활용 비효율**: 하나의 거대한 프로세스가 모든 요청을처리하려다 보니, 일부 요청만 CPU 집약적이고 나머지는 I/O 대기가 되는 불균형이 발생한다.

12팩터 앱의 동시성 원칙은 이러한문제을/를하기 위해"프로세스 모델을 통한 수평 확장"을 권장한다. 즉, 하나의 거대한 프로세스를 여러 작은 프로세스로 분리하고, 각 프로세스가 자신의에 집중하게 함으로써 전체 시스템의처리와/과을/를 것이다.

아래 다이어그램은 전통적 단일 프로세스 모델과 동시성 원칙의 차이를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">단일 프로세스 모델 vs 동시성 원칙</div></div>
<div class="kb-diagram-note">❌ 전통적 단일 프로세스 모델 (한계)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거대한 단일 프로세스 (Vertical Scaling 만으로 대응)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">단일 프로세스</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">처리 완료 │</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU 사용률 100%</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리 과부하 ──▶ 서비스 중단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한계에 도달하면 시스템 전체 업그레이드</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 확장에 한계 (Vertical Scaling은 비용이수에)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 단일 장애점 (SPOF)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 리소스 활용 비효율</div></div>
<div class="kb-diagram-note">✓ 동시성 원칙 (Scale-out)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">여러 경량 프로세스 (Horizontal Scaling으로 유연하게 대응)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">프로세스 1</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">프로세스 2</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">Workers (배경 작업)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">프로세스 3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">프로세스 N</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">로드밸런서 (Traffic Distributor)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장점:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 프로세스 추가만으로능력 증가 (선형적 확장)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 특정 프로세스 장애 ≠ 전체 서비스 중단 (격리성)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- CPU/메모리 집약적 작업을 별도 프로세스로 분리 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 트래픽 변화에 유연하게 대응</div></div>
</div>
</div>



> 📢 **섹션 요약 비유**: 동시성 원칙은"은행 창구의 증설"와 같다. 과거에는 한 명은행원(단일 프로세스)이 모든 업무를 처리하려 했으나, 고객 대기 시간이 길어지고 은행원이 과로로 쓰러지면(장애) 업무가 마비되었다. 그러나 창구를 여러 개(프로세스 동시 실행)로 늘리면, 고객이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되어 대기 시간이 줄어들고, 한 창구가 고장 나도 다른 창구가 업무를 계속 처리한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

동시성 원칙을 구현하는 다양한 방법과 그 내부 동작 메커니즘을 분석한다.

| 동시성 유형 | 구현 방식 | 적합한 작업 | 예시 |
|:---|:---|:---|:---|
| <strong>프로세스 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a></strong> | 여러 프로세스 인스턴스 실행 | Web 요청 처리 | Node.js cluster [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), Puma (Ruby) |
| **워커 프로세스** | 별도 백그라운드 프로세스 | 이메일 전송, 이미지 처리 | Sidekiq (Ruby), Celery (Python) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a></strong> | 하나의 프로세스 내 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) | I/O 대기가 많은 작업 | Java threading, Go [goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a></strong> | 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), 비동기 I/O | 높은 동시성, 낮은 리소스 | Node.js, Nginx (event-driven) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 오토스케일링</strong> | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 수 동적 조절 | 트래픽 변동 대응 | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) |

아래는 동시성 원칙이 실제 시스템에서 어떻게 구현되는지 보여주는 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동시성 원칙의 실제 구현: Node.js cluster 모듈</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">마스터 프로세스 (Master)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">const cluster = require('cluster');</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">const numCPUs = require('os').cpus().length;</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if (cluster.isMaster) {</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">for (let i = 0; i &lt; numCPUs; i++) {</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">cluster.fork(); // 워커 프로세스 생성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">} else {</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">// 워커 프로세스: HTTP 서버 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">app.listen(PORT);</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Worker 1</div><div class="kb-diagram-cell">Worker 2</div><div class="kb-diagram-cell">Worker N</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(CPU 1)</div><div class="kb-diagram-cell">(CPU 2)</div><div class="kb-diagram-cell">(CPU N)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">:3000</div><div class="kb-diagram-cell">:3000</div><div class="kb-diagram-cell">:3000</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">로드밸런서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(요청 분배)</div></div>
</div>
</div>





<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동시성 원칙의 실제 구현: Kubernetes HPA</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubernetes Horizontal Pod Autoscaler (HPA)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">apiVersion: autoscaling/v2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">kind: HorizontalPodAutoscaler</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">metadata:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">name: myapp-hpa</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">spec:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">scaleTargetRef:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">apiVersion: apps/v1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">kind: Deployment</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">name: myapp</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">minReplicas: 2 ← 최소 복제본 수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">maxReplicas: 10 ← 최대 복제본 수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">metrics:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- type: Resource</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">resource:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">name: cpu</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">target:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">type: Utilization</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">averageUtilization: 70</div></div>
<div class="kb-diagram-note">트래픽 증가 시:</div>
<div class="kb-diagram-note">CPU 사용률 70% 초과 → 파드 2개 → 4개 → 8개 ... 자동 확장</div>
<div class="kb-diagram-note">CPU 사용률 50% 이하 → 파드 수 점진적 축소</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 동시성 원칙의 구현은"음식 배달 시스템의 확대"와 같다. 배달 원이 한 명(단일 프로세스)일 때는 주문을 많이 받으면 배달이 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되고, 한 명씩만 추가해야 했다. 그러나(Uber Eats 등) 플랫폼을 통해 여려 배달원(여러 프로세스/[파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))을 동시에 운용하면, 주문이 증가할 때 배달원을 더 많이 투입하고, 주문이 줄면 배달원을 줄일 수 있어 효율적인 운영이 가능하다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

동시성 원칙은 현대적인 [클라우드 네이티브 아키텍처](/knowledge-base/studynote/12_it_management/05_security_compliance/204_cloud_native_architecture/)와 긴밀하게 연결되어 있으며, 다른 기술과 어떻게 시너지를 발생하는지 분석한다.

| 관련 기술 | 동시성 원칙과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 시너지 효과 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>)</strong> | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리로 프로세스 수준 동시성 | 자원 격리 + 유연한 확장 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a> (K8s)</strong> | [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ([Horizontal Pod Autoscaler](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/))로 동적 확장 | CPU/메모리 기반 자동 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)</strong> | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 독립적으로 확장 가능 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 최적 확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong>비동기 <a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>징</strong> | 워커 프로세스가 백그라운드 작업 처리 | 요청/응답과작업 분리 |
| **이벤트 아키텍처** | 이벤트에 따라 처리 인스턴스 동적 조절 | 트래픽 패턴에맞는 확장이 가능 |

동시성 원칙과 오토스케일링의 결합은 현대 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서 가장 강력한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 패턴이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동시성 + 오토스케일링: 트래픽 변화에 유연하게 대응</div></div>
<div class="kb-diagram-note">트래픽</div>
<div class="kb-diagram-note">╱╲</div>
<div class="kb-diagram-note">╱ ╲</div>
<div class="kb-diagram-note">╱ ╲</div>
<div class="kb-diagram-note">╱ ╲ ← 파드 추가 (Scale-out)</div>
<div class="kb-diagram-note">╱ ╲</div>
<div class="kb-diagram-note">╱ ╲</div>
<div class="kb-diagram-note">╱ ╲___</div>
<div class="kb-diagram-note">╱ ← 트래픽 감소 시</div>
<div class="kb-diagram-note">╱ 파드 감소 (Scale-in)</div>
<div class="kb-diagram-tree-item" style="--depth:0">▶ 시간</div>
<div class="kb-diagram-note">1개 2개 3개 4개 3개 2개 1개 1개 (파드 수)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 동시성과 오토스케일링의 결합은"계절에 따른 음식 재료 준비"와 같다. 여름에는 사용량이 늘어난다고 더 많은 재료를 사전에 준비하고, 겨울에는 사용량이 줄면 재료를 줄이며, 항상 적절한 양을 유지한다. 이렇게 하면 재고 낭비도 줄이고 고객 불만도 예방할 수 있다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

동시성 원칙을 실무에 적용할 때 흔히 발생하는 문제와 해결 방안을 분석한다.

**1. 실무 의사결정 시나리오**
- <strong>시나리오 A:CPU를 많이 사용하는 작업(처리)과 I/O를 많이 사용하는 작업(<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 호출)이 동일한 프로세스에서 수행되어 병목이 발생하는 상황</strong>
- **상황**: 단일 프로세스에서 동기적으로 이미지 리사이징과 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출을 모두 처리하여, 이미지 처리 대기 시간 때문에 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답까지 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)됨.
- **판단**: 동시성 원칙에 따라 두 작업을 별도 프로세스로 분리해야 한다. 이미지 처리는CPU 워커(별도 프로세스/서버)로 분리하고, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출은 웹 프론트엔드(또는 event-driven)로 처리하여 각각 최적화된리소스설정구현。

- <strong>시나리오 B: 백그라운드 작업(이메일 전송, <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 처리)이 웹 요청 처리와재되어 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하가 발생하는 상황</strong>
- **판단**: 백그라운드 작업은 워커 프로세스(예: Sidekiq, Celery)가 전용으로 처리하고, 웹 요청은 웹 프로세스가처리하다。 이렇게 하면 웹 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 백그라운드 작업의을 받지 않는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동시성 설계 패턴: 프로세스 유형 분리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">웹 프로세스 (Web Process)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- HTTP 요청/응답 처리에</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 빠른 응답 시간 목표</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- CPU/메모리 적당한 수준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 수평 확장 가능</div></div>
<div class="kb-diagram-note">메시지 큐</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">워커 프로세스 (Background Worker Process)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 이메일 전송, 이미지/동영상 처리 등작업 전문 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 배치 처리 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 웹 프로세스와 독립적 확장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 필요시 인스턴스로 급증 처리 가능</div></div>
<div class="kb-diagram-note">예: Ruby on Rails + Sidekiq</div>
<div class="kb-diagram-tree-item" style="--depth:0">Web: Puma (동시 요청 처리)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Worker: Sidekiq (백그라운드 작업 처리)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 동시성을위한 프로세스 분리는"식당의 주방과 배달 시스템 분리"와 같다. 주방(웹 프로세스)은 요리를 하는 데 집중하고, 배달(워커 프로세스)은 별도의 배달원이 담당한다. 만약 주방장이 요리도 하고 배달도 하면 양쪽 다 실력이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되고, 배달이 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되면 주방장의 집중도도 떨어진다. 그러나 분리되면 각자 전문성에 집중할 수 있다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

동시성 원칙의 올바른 적용은 시스템의처리、、가용성을 크게 향상시킨다.

| 관점 | 단일 프로세스 ([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) | 동시성 원칙 적용 (TO-BE) | [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a></strong> | 단일 프로세스 처리 능력에 한계 | 인스턴스 추가만으로 선형적 확장 | 최대 TPS 증가 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a></strong> | 트래픽 증가 시 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 급증 | 트래픽 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)으로 일관된 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | P50/P95/P99 레이턴시 개선 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong> | [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) ([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) | 프로세스 격리로 части | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상 |
| **자원 효율** | 하나의 거대한 프로세스, 자원 낭비 가능 | 필요한 만큼만 프로세스 실행 | 평균 CPU 활용률 향상 |
| **비용 효율** | 항상으로 운영 (과다Provision) | 실제 트래픽에 비례한 [Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) | 인프라 비용 최적화 |

**미래 전망 및 결론**:
동시성 원칙은 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) 컴퓨팅으로의 진화에서 더욱적으로 적용되고 있다. AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions, Google Cloud Functions와 같은 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 환경에서는 개발자가 프로세스나 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를관리하지 않고, 대신 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 수에 따라 자동으로처리능력이 확장/축소된다. 이것은 동시성 원칙의 궁극적 형태라 할 수 있다.

결론적으로, 동시성 원칙은 12팩터 앱의 제8원칙으로, 시스템의처리와/과을/를 데 중요한 설계 원칙이다. 웹 요청 처리와작업을 분리하고, 필요에 따라 프로세스를 수평 확장할 수 있도록 설계함으로써, 트래픽 변동에 유연하게 대응하고 리소스를 효율적으로 활용할 수 있는 시스템을 구축할 수 있다.

> 📢 **섹션 요약 비유**: 동시성 원칙은"레스토랑의 좌석 배치 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)"과 같다. 한 명씩만 앉을 수 있는 작은 테이블(단일 프로세스) 대신, 필요에 따라 합석이 가능한 큰 테이블(프로세스 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))을 사용하고, 손님이 늘어나면 테이블을 더 늘리고([스케일 아웃](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)), 줄어들면 테이블을 합치거나 줄이면(스케일 인) 공간을 효율적으로 활용할 수 있다.


### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

| 개념 | 연결 포인트 |
|:---|:---|
| **12팩터 앱 (Twelve-Factor App)** | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 애플리케이션 설계 원칙 12가지 중 제8원칙이 동시성 |
| <strong>프로세스 매니저 (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/">Process</a> Manager)</strong> | systemd / Procfile 기반으로 프로세스 타입·수량을 선언적으로 관리 |
| <strong>수평 확장 (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">Scale-Out</a>)</strong> | 프로세스 인스턴스를 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 선형적으로 늘리는 확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">Serverless</a> / <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a>)</strong> | 함수 단위 자동 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 확장, 동시성 원칙의 궁극적 진화 형태 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">12팩터 앱 (Twelve-Factor App) — 클라우드 네이티브 애플리케이션 설계 원칙</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">동시성 원칙 (Concurrency, 제8원칙) — 프로세스 타입 분리·수평 복제 확장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">프로세스 매니저 (Process Manager) — systemd/Procfile 기반 수명 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">컨테이너 오케스트레이션 (Kubernetes) — Pod 복제·HPA로 동시성 자동 확장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">서버리스 (Serverless / FaaS) — 함수 단위 무한 병렬 확장, 동시성 극한 구현</div></div>
</div>
</div>



이 흐름은 12팩터 앱의 동시성 원칙에서 출발해 프로세스 매니저로 수명을 관리하고, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)을 거쳐 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 무한 자동 확장으로 진화하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 확장성 아키텍처의 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 동시성은 한 명의 직원이 모든 일을 혼자 처리하는 대신, 같은 일을 하는 직원을 여러 명 고용해서 동시에 일하게 하는 것과 같아요.
2. 손님이 많아지면 직원을 더 뽑고, 손님이 줄어들면 퇴근시키면 되니까 언제나 딱 맞게 일할 수 있어요.
3. [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 직원을 아예 두지 않고 일이 생길 때만 순식간에 로봇을 불러서 처리하는 최첨단 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 14 / 373

← **이전**: [13. 포트 바인딩 (Port Binding) - 자체적으로 포트를 바인딩하여 웹 서비스 노출](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/013_port_binding/)
**다음**: [15. 폐기 가능성 (Disposability) - 빠른 시작과 우아한 종료(Graceful Shutdown)를 통한 안정성 극대화](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/015_disposability/) →

---
