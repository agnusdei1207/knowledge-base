+++
title = "12. 무상태 프로세스 (Stateless Processes) - 애플리케이션은 상태를 공유하지 않고 무상태로 실행되며, 상태는 DB 등에 저장"
date = 2026-04-05

[taxonomies]
tags = ["devops_sre"]

[extra]
tags = ["devops_sre"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무상태 프로세스 원칙은 애플리케이션이 각 요청/응답 사이클 간에 상태를 저장하지 않고 실행되며, 필요한 상태는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 캐시 같은 외부 자원에 저장해야 한다는 12팩터 앱의 제6원칙이다.
> 2. **가치**: 무상태로 설계된 애플리케이션은 수평적 확장이 용이하고, 인스턴스 장애 시에도 다른 인스턴스가즉시에 작업을인き계ぐこ와/과가あり, 배포 및 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)이 단순화된다.
> 3. **융합**: 무상태 원칙은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [쿠버네티스 오토스케일링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/206_kubernetes_autoscaling_hpa_vpa_ca/), [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 클러스터링, 그리고 MSA의 상태 관리 패턴과 긴밀하게 연결되어 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

"상태([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))"란 애플리케이션이 처리를 수행하기 위해 유지하는 정보로, 이는 메모리 내 변수, 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 또는 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 객체 등 다양한 형태로 존재할 수 있다. 상태를 저장하는 애플리케이션을"상태 저장(Stateful)"하다고 하고, 상태를 저장하지 않는 애플리케이션을"무상태([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))"하다고 한다.

전통적인 웹 애플리케이션에서는 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 메모리에 저장하거나, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 캐시를 저장하는 것이 일반적이었다. 이렇게 하면 동일한 사용자의 이후 요청이 동일한 서버 인스턴스로 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)되어야 했다(Sticky [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)). 그러나 이러한 설계는 다음과 같은 문제를 야기한다:

- **확장의 어려움**: 트래픽 증가 시 새 인스턴스를 추가해도, 기존 사용자는 여전히"자신의 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)이 있는" 기존 인스턴스로 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)되어야 하므로 확장이 복잡하다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 저하</strong>: 특정 인스턴스가 장애가 발생하면 그 인스턴스에 저장된 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)/상태가 모두 손실된다.
- **배포의 어려움**: 인스턴스를 업데이트할 때 해당 인스턴스의 모든 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)/상태를 처리해야 한다.

12팩터 앱의 무상태 프로세스 원칙은 이러한 문제를 해결하기 위해"애플리케이션은 무상태로 설계되어야 하며, 상태가 필요한 경우에는 명시적으로 외부 자원([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), 캐시, 객체 스토리지 등)에 저장해야 한다"고 명시한다.

아래 다이어그램은 상태 저장 애플리케이션과 무상태 애플리케이션의 차이를 보여준다.

```text
[상태 저장 vs 무상태 아키텍처]

❌ 상태 저장 (Stateful) - 문제 있는 설계
+-------------------------------------------------------------+
|                                                             |
|  사용자 A --+                                                |
|  사용자 B --+----> 로드밸런서 ---> [인스턴스 1] <- 메모리에 세션 저장  |
|  사용자 C --+                        [인스턴스 2] <- 다른 세션 저장   |
|                                    [인스턴스 3] <- 또 다른 세션 저장 |
|                                                             |
|  문제:                                                     |
|  1. 사용자 A가 인스턴스 1에 연결되어 있으면,                 |
|     인스턴스 1이 장애 시 세션 손실 -> 사용자 불만             |
|  2. 트래픽 증가로 인스턴스 4 추가해도,                       |
|     기존 사용자는 여전히 기존 인스턴스로 라우팅 -> 확장이 의미 없음|
|  3. 인스턴스 배포 시 해당 인스턴스의 세션 처리 필요         |
+-------------------------------------------------------------+

✓ 무상태 (Stateless) - 12팩터 원칙 준수
+-------------------------------------------------------------+
|                                                             |
|  사용자 A --+                                                |
|  사용자 B --+----> 로드밸런서 ---> [인스턴스 1] -+             |
|  사용자 C --+                        [인스턴스 2] -+--> Redis (세션)|
|                                    [인스턴스 3] -+   |
|                                    [인스턴스 N] --->        |
|                                                             |
|  장점:                                                     |
|  1. 모든 인스턴스가 동일하게 동작 -> 어느 인스턴스로든 라우팅 OK|
|  2. 특정 인스턴스 장애 -> 다른 인스턴스가即時に 작업을引き継ぐ|
|  3. 인스턴스 배포/스케일링이 단순 -> 상태 걱정 불필요         |
|  4. 상태는 외부에 저장 -> 영속성 보장                        |
+-------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: 무상태 원칙은"호텔의 짐기존サービス"와 같다. 지갑과 카드키를 호텔 짐기존소에예け고（외부 상태 저장）바다 입실하면(무상태 요청 처리), 어느거태(인스턴스)에서 체크인해도 동일한 절차를 따른다. 만약 한거태(인스턴스)가고장되어소폐해도(장애) 다른거태(인스턴스)에서 즉시 업무를 continuity할 수 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

무상태 원칙을 효과적으로 구현하기 위해서는 상태 관리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 외부 상태 저장소 활용법에 대한 깊은 이해가 필요하다.

| 상태 유형 | 저장 위치 | 무상태 원칙 적용 방법 | 예시 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), Memcached, DB | 외부 캐시/DB에 저장, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ID로 조회 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 장바구니 |
| **사용자 캐시** | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) | 가능하면 포함하지 않거나 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 추천 상품, 임시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong>업로드 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong> | S3, GCS, [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) | 객체 스토어에 저장, 경로만 DB에 | 프로필 이미지, 첨부 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| <strong>임시 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong> | Ephemeral Disk (없음) | 사용 후 즉시 삭제 | 업로드 임시 저장 |
| **애플리케이션 상태** | 외부 DB | 설계 시부터 외부 저장 고려 | 워크플로우 상태, 주문 상태 |

아래는 무상태 프로세스의 내부 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 보여주는 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램이다.

```text
[무상태 애플리케이션의 요청 처리 흐름]

1. 요청 수신 (Request)
+-------------------------------------------------------------+
|  사용자 요청                                                    |
|  +-----------------------------------------------------+   |
|  |  HTTP GET /api/user/profile                         |   |
|  |  Header: Authorization: Bearer <token>              |   |
|  |  Cookie: session_id=abc123                          |   |
|  +-----------------------------------------------------+   |
+-------------------------------------------------------------+

2. 세션 조회 (Stateless - 상태는 외부에)
+-------------------------------------------------------------+
|  애플리케이션 (무상태)                                        |
|  +-----------------------------------------------------+   |
|  |  1. 세션 ID 추출 (session_id)                        |   |
|  |  2. Redis에서 세션 데이터 조회                        |   |
|  |     session = redis.get(f"session:{session_id}")    |   |
|  |  3. 세션 기반 요청 처리                                |   |
|  |     user = db.get_user(session['user_id'])          |   |
|  |  4. 응답 반환                                        |   |
|  |     return {"user": user.name, ...}                |   |
|  +-----------------------------------------------------+   |
|                                                             |
|  ※ 애플리케이션 메모리에 상태 저장 ❌ (무상태 원칙 위반)       |
|  ※ 모든 인스턴스에서 동일한 동작 ✅ (무상태 원칙 준수)        |
+-------------------------------------------------------------+

3. 외부 상태 저장소 (Redis)
+-------------------------------------------------------------+
|  +-----------------------------------------------------+   |
|  |  Key: session:abc123                                |   |
|  |  Value: {                                          |   |
|  |    "user_id": "u12345",                           |   |
|  |    "login_at": "2024-04-05T10:30:00Z",            |   |
|  |    "preferences": {"theme": "dark"}               |   |
|  |  }                                                  |   |
|  +-----------------------------------------------------+   |
|                                                             |
|  ※ 세션 데이터는 중앙化管理 + 영속성 보장                     |
|  ※ TTL 설정으로 자동 만료 (보안)                            |
+-------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: 무상태 처리 방식은"은행의 계좌 시스템"과 같다. 은행원이 바뀌었다고(인스턴스 장애/교체) 고객의 계좌 잔고(외부 상태)가 사라지지 않는다. 고객은 새로운 은행원(다른 인스턴스)에게 가서 자신의 계좌 번호([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ID)를 말하면 계좌 정보를 조회할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

무상태 원칙은 현대적인 [클라우드 네이티브 아키텍처](/knowledge-base/studynote/12_it_management/05_security_compliance/204_cloud_native_architecture/)와 긴밀하게 연결되어 있으며, 다른 기술과 어떻게 시너지를 발생하는지 분석한다.

| 관련 기술 | 무상태 원칙과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 시너지 효과 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>)</strong> | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는ephemeral이므로 상태 저장 불가 | 자연스럽게 무상태 설계 강제 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a></strong> | Pod는 언제든 재생성될 수 있음 | 무상태 설계 없으면 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 곤란 |
| **오토스케일링** | 인스턴스가 동적으로 추가/제거 | 무상태여야만 올바른 로드밸런싱 가능 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a> 클러스터링</strong> | Redis를 사용한 중앙화 [세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/) | Tomcat/Jetty 등의 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 클러스터링 대체 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a></strong> | MSA에서는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 상태 공유 불허 | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 stateless하게 설계 필수 |

특히 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경에서는 무상태 여부가직접적으로 확장성과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)에 영향을 미친다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 요청에 따라 Pod를 동적으로 확장/축소하고, 문제가 있는 Pod는자동적에종료させ고새로운しいも의에치き환える.

```text
[쿠버네티스에서 무상태 원칙의중요성]

쿠버네티스 오토스케일링 이벤트:
+-------------------------------------------------------------+
|                                                             |
|  1. 스케일 아웃 (Scale Out)                                  |
|     +----------------------------------------------+        |
|     | 기존 Pod 1개 -> 새 Pod 3개로 확장              |        |
|     |                                               |        |
|     |  [Pod 1]        [Pod 2]      [Pod 3]         |        |
|     |  (기존)         (新增)        (新增)          |        |
|     |                                               |        |
|     |  ※ 3개 모두 동일한 코드/설정                  |        |
|     |  ※ 어떤 Pod로 요청이 가도 동일한 결과        |        |
|     |  ※ 세션/상태는 Redis에서 공유               |        |
|     +----------------------------------------------+        |
|                                                             |
|  2. Rolling Update                                           |
|     +----------------------------------------------+        |
|     |  [Pod v1.0] [Pod v1.0] -> [Pod v1.1] [Pod v1.1]|        |
|     |   (구버전)   (구버전)     (신버전)   (신버전)   |        |
|     |                                               |        |
|     |  ※ 새 버전 Pod逐渐增加, 구버전 점진적 제거      |        |
|     |  ※ 요청 중단 없이 무빙 업데이트 가능            |        |
|     |  ※ 상태는 외부 저장소에서管理되므로影響 없음   |        |
|     +----------------------------------------------+        |
|                                                             |
|  3. Pod 장애/재시작                                         |
|     +----------------------------------------------+        |
|     |  [Pod 1] ❌ (장애)                           |        |
|     |       |                                       |        |
|     |       v (쿠버네티스가 자동 교체)               |        |
|     |  [Pod 1'] ✅ (새 Pod)                        |        |
|     |                                               |        |
|     |  ※ 새 Pod는 동일한 코드로 기동               |        |
|     |  ※ Redis에 세션이保存되어 있어 영향 없음      |        |
|     |  ※ 사용자는 다른 Pod로 라우팅되어 continuity |        |
|     +----------------------------------------------+        |
+-------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 무상태 원칙 적용은"호텔 방 청소 시스템"과 같다. 하루가 끝나면(일정 주기) 하녀([쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/))가 각 방([파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))을 청소하는데, 만약 손님 물건(상태)이 방 안 어딘가에 있을 때(로컬 상태) 문제가 발생한다. 그러나 손님이 짐을 짐기존소(외부 저장소)에예け고 있으면, 하녀는 어떤 방이든 빠르게 정리하고 다음 손님을 맞을 수 있다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

무상태 원칙을 실무에 적용할 때 흔히 직면하는 문제와 해결 방안을 분석한다.

**1. 실무 의사결정 시나리오**
- <strong>시나리오 A: 레거시 앱이 로컬 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템에 큰 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 캐시를 저장하고 있는데 이를 무상태로 전환해야 할 때</strong>
  - **상황**: 기존 앱이 사용자가 업로드한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 로컬 디스크에완존하고 있어, MSA로 전환 시 문제가 될 것으로 예상됨.
  - **판단**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 캐시는 S3나 GCS 같은 객체 스토리지로 마이그레이션해야 한다. 앱에서는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)할 때 로컬 경로가 아닌 S3 URL을 사용하며, CDN과 결합하면 더 빠른 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송이 가능하다.

- <strong>시나리오 B: 스프링 부트의 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a>을 Redis로천이해야 할 때</strong>
  - **상황**: 현재 스프링 부트 앱이 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 JVM 메모리에 저장하고 있는데, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경으로 이전하려고 함.
  - **판단**: 스프링 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 Redis로 저장하도록 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하면 된다. `spring-session-data-redis` 의존성을추가하고 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)만 하면, 기존 코드 변경 없이 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 외부 Redis에 저장할 수 있다.

```text
[무상태 전환 체크리스트]

□ 세션 관리
  □ 세션은 Redis/Memcached에 저장
  □ Sticky Session 사용 안 함
  □ 세션에 민감 정보는暗号화

□ 파일 저장
  □ 사용자가 생성한 파일은 로컬 FS에 저장하지 않음
  □ S3/GCS/Azure Blob 등 객체 스토리지 활용
  □ 임시 파일은ephemeral 볼륨에 저장 후 삭제

□ 캐시 데이터
  □ 장기간 저장할 캐시는 DB/Redis에
  □ 짧은 TTL로 설정하여 정합성 유지
  □ 중요한 데이터는 캐시에만保存하지 않음
```

> 📢 **섹션 요약 비유**: 무상태 원칙의 부재는"여권에 사진을 붙여두는 것"과 같다. 만약 출입국 심사대에서 여권 사진이 떨어져 나오면(인스턴스 장애) 그 사람은 누구인지 증명할 수 없다. 그러나 출입국관리 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(외부 상태 저장소)에 사진이 있고([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)), 여권에는 그를 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 있는 여권 번호만 있으면([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ID), 어느 심사대(인스턴스)를 가든 동일한 심사를 받을 수 있다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

무상태 원칙의 올바른 적용은 시스템의 확장성, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), 그리고 운영 효율성에 직접적인 긍정적 영향을 미친다.

| 관점 | 상태 저장 설계 ([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) | 무상태 설계 (TO-BE) | [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) |
|:---|:---|:---|:---|
| **확장성** | Sticky Session으로 확장 제한 | 모든 인스턴스 동일, 무제한 확장 가능 | [스케일 아웃](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 단축 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong> | 인스턴스 장애 시 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 | 인스턴스 장애 시즉시 [failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) | 장애에 따른 영향 최소화 |
| **배포 민첩성** | 인스턴스별 상태 처리 필요 | 상태 걱정 없이 언제든 배포/교체 가능 | 배포 시간 단축 |
| **테스트 용이성** | 특정 인스턴스에서만재현 가능 | 모든 인스턴스에서 동일 동작 | 디버깅/테스트 용이 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a> 적합성</strong> | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 교체 시 상태 손실 위험 | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) lifecycle와 무관하게 상태 유지 | [Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) 완전 지원 |

**미래 전망 및 결론**:
무상태 원칙은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/), [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 등 현대적 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 플랫폼의 기본 전제 조건이다. 특히 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)(AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions)에서는 애플리케이션이 상태를보존할 수 없으며, 모든 상태는 외부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 저장해야 한다. 따라서 무상태 설계는"선택이 아닌 필수"가 되었다.

결론적으로, 무상태 원칙은 12팩터 앱의 제6원칙으로, 현대적 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서 시스템의 확장성, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), 그리고 민첩성을단보하는 기본적인 설계 원칙이다. 모든 새로운 시스템은 무상태로 설계해야 하며, 기존 상태 저장 시스템도 점진적으로 무상태로 전환하는 것이 권장된다.

> 📢 **섹션 요약 비유**: 무상태 원칙은"스마트폰의 연락처 앱"과 같다. 과거에는 전화기에 직접 연락처를 저장했지만(상태 저장), 이제는 Gmail/icloud 연락처(외부 상태 저장소)에 저장한다. 이렇게 하면 핸드폰을 바꿔도(인스턴스 교체) 같은 계정으로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인하면 모든 연락처가 그대로이고, 어떤 기기에서든 연락처를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다.


### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>12팩터 앱 (<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/">12-Factor App</a>)</strong> | 상태를 코드 밖으로 분리하는 설계 원칙 |
| <strong>무상태 프로세스 (<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/">Stateless</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/">Process</a>)</strong> | 요청 간 로컬 상태를 유지하지 않는 실행 방식 |
| <strong>외부 상태 저장소 (External <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a> Store)</strong> | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)/DB로 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보관하는 영역 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">컨테이너 오케스트레이션</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/122_container_orchestration_kubernetes_k8s/">Container Orchestration</a>)</strong> | 무상태 인스턴스를 자동 배치·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 운영 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
[12팩터 앱 (12-Factor App) — 원칙 기반 앱 설계]
    |
    v
[무상태 프로세스 (Stateless Process) — 로컬 상태 금지]
    |
    v
[외부 상태 저장소 (External State Store) — Redis/DB 활용]
    |
    v
[수평 확장 (Horizontal Scaling) — 인스턴스 복제]
    |
    v
[컨테이너 오케스트레이션 (Container Orchestration) — Kubernetes 자동 배치]
```

이 흐름은 12-Factor App의 원칙에서 출발해 로컬 상태를 배제하고, 외부 저장소와 수평 확장을 거쳐 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 같은 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)으로 자동 배치되는 구조를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 무상태 프로세스는 서버가 자기 물건을 잔뜩 들고 있지 않게 하는 규칙이에요.
2. 필요한 기억은 Redis나 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 같은 바깥 창고에 맡겨요.
3. 그래서 서버를 여러 대로 늘려도 같은 일을 똑같이 할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 12 / 373

<- **이전**: [11. 빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/011_build_release_run/)
**다음**: [13. 포트 바인딩 (Port Binding) - 자체적으로 포트를 바인딩하여 웹 서비스 노출](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/013_port_binding/) ->

---
