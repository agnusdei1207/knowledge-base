+++
weight = 88
title = "88. 스테이트풀셋 (StatefulSet) - K8s 상태 저장 DB 배포"
date = "2026-04-10"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스테이트풀셋 (StatefulSet)은 `K8s (Kubernetes)` 환경에서 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])의 [[289_identification_flags_fragmentation_offset|식별자]]와 스토리지 볼륨을 영구적으로 보장하는 워크로드 컨트롤러다.
> 2. **가치**: [[085_pod_kubernetes_container_unit|파드]]가 재시작되거나 재생성되더라도 항상 동일한 이름(Ordinal [[154_database_index_b_tree_search_optimization|Index]])과 동일한 [[001_dikw_pyramid|데이터]] 볼륨을 할당받아, [[001_dikw_pyramid|데이터]] 유실과 [[136_variance|분산]] 시스템의 합의 붕괴를 원천 차단한다.
> 3. **판단 포인트**: 무상태([[239_stateless_redis|Stateless]]) 웹 서버나 API는 `Deployment`로 배포하고, [[002_database_definition|데이터베이스]]나 메시지 큐처럼 고유한 정체성과 상태 유지가 필수적인 시스템은 `StatefulSet`을 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

스테이트풀셋 (StatefulSet)은 [[085_pod_kubernetes_container_unit|파드]] 간의 순서와 고유성을 보장하여 상태 저장(Stateful) 애플리케이션을 안정적으로 운영하기 위한 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 객체다. 기존 `Deployment`는 [[085_pod_kubernetes_container_unit|파드]]를 언제든 대체 가능한 소모품으로 취급하기 때문에, [[085_pod_kubernetes_container_unit|파드]]가 재시작되면 이름과 IP가 바뀌고 기존 디스크와의 연결도 끊어진다.

[[002_database_definition|데이터베이스]] 클러스터나 메시지 브로커처럼 각 노드가 "자신이 누구인지"와 "어떤 [[001_dikw_pyramid|데이터]]를 들고 있는지"를 기억해야 하는 [[136_variance|분산]] 시스템에서는 이러한 무상태 철학이 치명적인 장애를 유발한다. 따라서 [[085_pod_kubernetes_container_unit|파드]]가 죽고 다시 살아나도 어제와 똑같은 이름과 [[001_dikw_pyramid|데이터]]를 돌려주는 엄격한 배정 시스템이 필요해졌고, 이를 위해 StatefulSet이 등장했다.

- **📢 섹션 요약 비유**: 무상태 [[085_pod_kubernetes_container_unit|파드]]가 이름표 없이 언제든 교체되는 공장 노동자라면, 상태 저장 [[085_pod_kubernetes_container_unit|파드]]는 자기 전용 금고와 고정된 직통 번호를 가진 은행 지점장과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

StatefulSet은 고정된 [[289_identification_flags_fragmentation_offset|식별자]], [[597_headless_cms_architecture|헤드리스]] [[090_service_kubernetes_network_load_balancing|서비스]]([[597_headless_cms_architecture|Headless]] [[090_service_kubernetes_network_load_balancing|Service]]), 그리고 개별 영구 볼륨이라는 3대 요소를 결합하여 [[085_pod_kubernetes_container_unit|파드]]의 정체성을 유지한다.

| 구성 요소 | 핵심 역할 | 동작 원리 및 효과 |
| :--- | :--- | :--- |
| **Ordinal Identity** | [[085_pod_kubernetes_container_unit|파드]]의 순차적 명명 | `mysql-0`, `mysql-1`처럼 인덱스가 부여되며, 재기동 시에도 동일 이름 유지 |
| **[[597_headless_cms_architecture|Headless]] [[090_service_kubernetes_network_load_balancing|Service]]** | 고유한 네트워크 신원 제공 | [[085_pod_kubernetes_container_unit|파드]]마다 개별 `DNS (Domain Name System)` 레코드를 [[087_process_state_transition|생성]]하여 [[120_direct_communication|직접 통신]] 지원 |
| **VolumeClaimTemplates** | [[085_pod_kubernetes_container_unit|파드]]별 영구 볼륨 할당 | [[085_pod_kubernetes_container_unit|파드]] [[087_process_state_transition|생성]] 시 각각 독립적인 `PVC (PersistentVolumeClaim)`를 자동 [[087_process_state_transition|생성]] |

```text
┌──────────────────────────────────────────────────────────────┐
│           StatefulSet의 정체성 및 볼륨 바인딩 구조           │
├──────────────────────────────────────────────────────────────┤
│  [StatefulSet Controller]                                    │
│       │                                                      │
│       ├─▶ Pod: web-0 ──DNS: web-0.svc──▶ PVC: data-web-0     │
│       │                                                      │
│       ├─▶ Pod: web-1 ──DNS: web-1.svc──▶ PVC: data-web-1     │
│       │                                                      │
│       └─▶ Pod: web-2 ──DNS: web-2.svc──▶ PVC: data-web-2     │
└──────────────────────────────────────────────────────────────┘
```

[[087_process_state_transition|생성]]과 확장은 인덱스가 0인 [[085_pod_kubernetes_container_unit|파드]]부터 순차적으로 이루어지며(0 → 1 → 2), 이전 [[085_pod_kubernetes_container_unit|파드]]가 완전히 `Running` 및 `Ready` 상태가 되어야 다음 [[085_pod_kubernetes_container_unit|파드]]를 시작한다. 축소 및 삭제는 반대 순서(2 → 1 → 0)로 진행되어 [[001_dikw_pyramid|데이터]] 동기화의 충돌을 방지한다.

- **📢 섹션 요약 비유**: 아파트 입주처럼 101호가 지어지고 입주가 끝나야 102호를 짓고, 철거할 때는 102호부터 안전하게 비우는 순차적 건설 방식이다.

---

## Ⅲ. 비교 및 연결

StatefulSet을 정확히 이해하려면 무상태 워크로드를 관리하는 Deployment와의 경계 비교가 필수적이다. [[085_pod_kubernetes_container_unit|파드]]를 다루는 철학 자체가 다르기 때문이다.

| 비교 축 | [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | StatefulSet |
| :--- | :--- | :--- |
| **[[085_pod_kubernetes_container_unit|파드]] 명명 규칙** | 무작위 해시 (예: `web-7abc-x2`) | 고정된 순차 번호 (예: `web-0`, `web-1`) |
| **볼륨 [[516_mount_mechanism|마운트]]** | 모든 [[085_pod_kubernetes_container_unit|파드]]가 동일 볼륨 공유 가능 | [[085_pod_kubernetes_container_unit|파드]]마다 1:1 고유 [[269_pvc_vs_svc_virtual_circuits|PVC]] 할당 |
| **시작 및 종료 순서** | 동시다발적 [[430_index_fast_full_scan|병렬]] 처리 | 엄격한 순차적 처리 |
| **적합한 워크로드** | 웹 서버, [[532_microservices_decomposition_patterns|마이크로서비스]] [[014_api_posix|API]] | DB 클러스터, `Kafka`, `ZooKeeper` |

이러한 차이로 인해 StatefulSet은 스토리지 관리(StorageClass 연동)와 [[511_dns_hierarchical_distributed_architecture|DNS]] 해상도([[597_headless_cms_architecture|Headless]] [[090_service_kubernetes_network_load_balancing|Service]])가 반드시 함께 설정되어야 정상 동작한다. 네트워크 계층과 스토리지 계층을 모두 결합해야 비로소 '상태'가 완성되기 때문이다.

- **📢 섹션 요약 비유**: Deployment가 렌터카 풀에서 아무 차나 꺼내 타는 것이라면, StatefulSet은 번호판과 트렁크 짐이 항상 일치하는 개인 소유 차량을 배정하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 StatefulSet은 [[001_dikw_pyramid|데이터]] 정합성이 생명인 인프라 컴포넌트를 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 위로 올릴 때 핵심적인 의사결정 대상이 된다. 

### 💡 기술사 판단 ([[435_checklist_based_testing|체크리스트]])
1. **워크로드 특성 검토**: [[085_pod_kubernetes_container_unit|파드]] 이름이나 IP가 변경되었을 때, 클러스터 [[011_consensus_algorithm|합의 알고리즘]](예: [[259_raft_paxos|Raft]], Paxos)이 깨지는가?
2. **볼륨 생명주기 분리 [[396_validation|확인]]**: StatefulSet을 삭제해도 PVC는 기본적으로 보존된다. 삭제 시 [[001_dikw_pyramid|데이터]]까지 지울 것인지에 대한 [[555_backup_and_restore_strategy|백업]] 및 정리 정책이 수립되었는가?
3. **[[597_headless_cms_architecture|Headless]] [[090_service_kubernetes_network_load_balancing|Service]] 매핑**: 로드밸런싱이 목적이 아니라 [[085_pod_kubernetes_container_unit|파드]] 간 다이렉트 통신이 목적이므로, `clusterIP: None` 설정이 누락되지 않았는가?

### 🚫 [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **임시 볼륨 사용**: 볼륨 템플릿에 `emptyDir`을 사용하여, [[085_pod_kubernetes_container_unit|파드]] 재시작 시 [[001_dikw_pyramid|데이터]]가 날아가게 구성하는 설계.
- **무조건적인 StatefulSet 도입**: 단순히 [[501_file_definition_logical_record|파일]] 캐시를 저장하려고 StatefulSet을 남용하는 행위. 상태 저장은 관리형 클라우드 DB에 맡기고, K8s는 무상태로 유지하는 것이 운영 부담을 줄이는 길이다.

- **📢 섹션 요약 비유**: 중요한 서류를 보관할 때는 임시 사물함(emptyDir)이 아니라, 이름표가 붙고 자물쇠가 확실한 개인 전용 금고(PVC와 StatefulSet)에 넣어야 한다.

---

## Ⅴ. 기대효과 및 결론

StatefulSet을 적절히 활용하면, 재난 [[658_ir_recovery|복구]]와 노드 장애 시에도 [[136_variance|분산]] [[002_database_definition|데이터베이스]]의 [[001_dikw_pyramid|데이터]] 정합성과 네트워크 신원(Identity)이 완벽하게 보장된다. 이는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]가 단순 [[561_container_based_deployment|컨테이너]] 오케스트레이션을 넘어 스테이트풀 인프라 플랫폼으로 확장되는 기반을 제공한다.

하지만 [[085_pod_kubernetes_container_unit|파드]]의 자동 교체가 제한되고 순차적 처리로 인해 배포 속도가 느려지며, 스토리지 관리에 대한 운영 복잡도가 크게 상승한다는 한계가 있다. 결론적으로 StatefulSet은 "무조건 피해야 할 것도, 무조건 써야 할 것도 아니며, 애플리케이션이 상태의 영속성을 스스로 책임져야만 할 때 사용하는 최후의 보루"로 인식해야 한다.

- **📢 섹션 요약 비유**: 절대 자리를 뜨면 안 되는 초소 경비병처럼, 배치와 철수가 까다롭지만 그 덕분에 진지([[001_dikw_pyramid|데이터]])가 흔들리지 않게 지켜내는 핵심 방어선이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[597_headless_cms_architecture|Headless]] [[090_service_kubernetes_network_load_balancing|Service]]** | `clusterIP: None`으로 설정되어, 로드밸런싱 없이 [[085_pod_kubernetes_container_unit|파드]] 개별의 [[511_dns_hierarchical_distributed_architecture|DNS]] 레코드를 직접 반환 |
| **[[269_pvc_vs_svc_virtual_circuits|PVC]] (PersistentVolumeClaim)** | StatefulSet의 `VolumeClaimTemplates`에 의해 [[085_pod_kubernetes_container_unit|파드]]별로 동적 프로비저닝되는 [[098_kubernetes_storage_volume_pv_pvc|영구 스토리지]] |
| **[[565_operator_pattern|Operator Pattern]]** | StatefulSet만으로 부족한 DB [[555_backup_and_restore_strategy|백업]], [[658_ir_recovery|복구]], [[288_version_ihl_tos_total_length|버전]] 업그레이드 등 복잡한 상태 관리를 자동화하는 패턴 |
| **[[334_process|DaemonSet]]** | 상태와 무관하게 모든 노드에 1개씩 떠야 하는 [[568_logs_distributed_logging_elk_fluentd|로그]]/모니터링 에이전트 워크로드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[무상태 워크로드 관리]
Deployment / ReplicaSet (일회성 파드)
        │
        ▼
[상태 의존성 문제 발생]
네트워크 신원 변경 및 볼륨 공유 충돌
        │
        ▼
[상태 저장 제어기 도입]
StatefulSet (고정 Ordinal Index)
        │
        ▼
[정체성 및 데이터 영속성 결합]
Headless Service (고정 DNS) + VolumeClaimTemplates (고유 PVC)
        │
        ▼
[고도화된 상태 관리]
Kubernetes Operator (DB 특화 자동화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원 범퍼카는 아무나 빈 차에 타면 되지만([[087_deployment_kubernetes_workload_rolling_update|Deployment]]), 지정 좌석제 버스는 자기 이름표가 있는 자리에만 앉아야 해요.
2. 스테이트풀셋(StatefulSet)은 [[085_pod_kubernetes_container_unit|파드]]라는 친구들에게 '지정 좌석'과 '자기만의 서랍'을 영원히 만들어주는 선생님이에요.
3. 그래서 컴퓨터가 잠깐 꺼졌다 켜져도, 항상 원래 내 자리에서 원래 내 물건을 그대로 찾을 수 있답니다!
