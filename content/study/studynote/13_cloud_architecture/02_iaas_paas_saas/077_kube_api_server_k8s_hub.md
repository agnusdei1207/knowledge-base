+++
weight = 77
title = "77. Kube-API Server - 모든 K8s 명령(kubectl)을 REST API로 수신하고 컴포넌트 간 통신을 중계하는 허브"
date = "2026-04-07"
[extra]
categories = "studynote-cloud"
+++

# Kube-[[014_api_posix|API]] Server - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 통제망의 [[152_hub_dummy_switching_intelligent|허브]]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kube-[[014_api_posix|API]] Server는 K8s ([[205_kubernetes_container_orchestration|Kubernetes]]) 클러스터에서 모든 요청이 먼저 도달하는 중앙 [[014_api_posix|API]] 관문이다.
> 2. **가치**: [[303_authentication_authorization_patterns|인증]], [[509_authorization_models_rbac_abac|인가]], 승인, 저장, 감시를 한 곳에 모아 클러스터 상태의 단일 진실을 만든다.
> 3. **판단 포인트**: [[014_api_posix|API]] Server가 멈추면 워크로드는 잠시 돌아가도, 새 제어와 변경은 사실상 멈춘다.

---

## Ⅰ. 개요 및 필요성
[[196_kubernetes_k8s_container_orchestration|쿠버네티스]]는 여러 컴포넌트가 협업하는 제어평면(control plane) 구조다. 그 가운데 Kube-[[014_api_posix|API]] Server는 외부 사용자, 컨트롤러, [[079_kube_scheduler_pod_placement|스케줄러]], kubelet이 모두 거쳐 가는 [[477_rest_api_architecture|REST API]] 입구다. 입구가 하나여야 상태 변경을 일관되게 기록할 수 있다.

[[014_api_posix|API]] Server가 필요한 이유는 분산된 명령을 하나의 규칙과 하나의 저장소로 모아야 하기 때문이다. 그렇지 않으면 각 컴포넌트가 서로 직접 통신하며 상태 충돌을 일으키기 쉽다.

📢 섹션 요약 비유: 건물의 모든 민원 창구를 하나의 안내 데스크로 모아 두는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리
요청은 `인증(Authentication) → 인가(Authorization) → 승인(Admission) → 저장(etcd) → 감시(Watch)` 순서로 흐른다. [[014_api_posix|API]] Server는 단순 전달기가 아니라, [[164_policy|정책]]을 적용하고 상태를 기록하고 변경을 배포하는 관문이다.

| 단계 | 역할 | 관련 요소 |
| :--- | :--- | :--- |
| [[604_authentication_factors|Authentication]] | 신원 [[396_validation|확인]] | 토큰, [[303_authentication_authorization_patterns|인증]]서 |
| [[509_authorization_models_rbac_abac|Authorization]] | 권한 판단 | [[569_rbac|RBAC]] ([[569_rbac|Role-Based Access Control]]) |
| Admission | [[164_policy|정책]] [[395_verification_process_review|검증]]/변경 | Admission Controller, [[498_webhook_rest_api_reverse_callback|Webhook]] |
| Persistence | 클러스터 상태 저장 | [[078_etcd_distributed_key_value_store|etcd]] |
| Watch | 변경 알림 | scheduler, controller, [[082_kubelet_node_agent|kubelet]] |

```text
kubectl / controller / kubelet
           │
           ▼
  ┌──────────────────┐
  │  Kube-API Server  │
  └───────┬──────────┘
          │ authn / authz / admission
          ▼
         etcd
          │
          ├─ watch ▶ controller manager
          ├─ watch ▶ scheduler
          └─ watch ▶ kubelet
```

[[014_api_posix|API]] Server는 원하는 상태([[080_kube_controller_manager_desired_state|desired state]])를 수락하고, 그 상태를 etcd에 저장한 뒤, 다른 컴포넌트가 watch로 반응하게 만든다. 그래서 Kubernetes의 제어는 [[014_api_posix|API]] Server를 중심으로 수렴한다.

📢 섹션 요약 비유: 접수창구가 신청서를 받아 심사하고, 기록하고, 관련 부서에 동시에 알려주는 흐름이다.

---

## Ⅲ. 비교 및 연결
[[014_api_posix|API]] Server는 [[079_kube_scheduler_pod_placement|스케줄러]]나 kubelet과 다르다. [[079_kube_scheduler_pod_placement|스케줄러]]는 어떤 노드에 배치할지 결정하고, kubelet은 노드에서 실제 [[561_container_based_deployment|컨테이너]]를 실행하며, [[014_api_posix|API]] Server는 그 모든 결정을 받아들이는 통제 [[152_hub_dummy_switching_intelligent|허브]]다.

etcd는 상태 저장소이고, [[014_api_posix|API]] Server는 그 저장소 앞의 [[164_policy|정책]] 관문이다. 즉 저장소와 관문을 혼동하면 안 된다. 또한 control plane의 고가용성(HA)은 [[014_api_posix|API]] Server 자체를 여러 개 두고 로드밸런서(LB) 뒤에 배치하는 방식으로 확보한다.

📢 섹션 요약 비유: 교통경찰, 차고, 운행기록부는 역할이 다르다. 겉으로는 다 연결돼 보여도 기능은 분리되어 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 [[694_thread_local_storage_tls|TLS]] (Transport Layer [[283_security_tactics|Security]]), [[569_rbac|RBAC]], [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]], rate limit, [[078_etcd_distributed_key_value_store|etcd]] 백업이 중요하다. 업그레이드 시에는 [[288_version_ihl_tos_total_length|버전]] 호환성과 watch 부하를 [[396_validation|확인]]해야 한다.

- 채택: 중앙 [[164_policy|정책]], [[606_auditing_linux_auditd|감사]], 확장성이 중요한 클러스터
- 회피: [[014_api_posix|API]] Server [[454_spof|단일 장애점]]([[454_spof|SPOF]])을 허용하는 설계
- [[435_checklist_based_testing|체크리스트]]
  1. [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]]·승인 [[164_policy|정책]]이 분리되어 있는가?
  2. 다중 [[014_api_posix|API]] Server와 LB가 구성되어 있는가?
  3. [[078_etcd_distributed_key_value_store|etcd]] 백업과 [[658_ir_recovery|복구]] 절차가 준비되어 있는가?
  4. [[363_audit|audit]] log로 누가 무엇을 바꿨는지 추적되는가?

Kube-[[014_api_posix|API]] Server는 단순 포트가 아니라 운영 통제의 기준점이다. 따라서 가용성과 보안은 함께 봐야 한다.

📢 섹션 요약 비유: 회사의 모든 도장을 한 사무실에 모아두되, 그 사무실이 멈추지 않게 해야 한다.

---

## Ⅴ. 기대효과 및 결론
[[014_api_posix|API]] Server를 제대로 설계하면 클러스터 변경이 일관되고, [[606_auditing_linux_auditd|감사]] 가능하며, 자동화하기 쉬워진다. 결국 이 개념은 "[[196_kubernetes_k8s_container_orchestration|쿠버네티스]]의 입구이자 기록원"으로 기억하는 것이 맞다.

📢 섹션 요약 비유: 건물의 본관 접수처처럼, 여기서 통과한 일만 전체 건물에 반영된다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| K8s ([[205_kubernetes_container_orchestration|Kubernetes]]) | [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]] |
| [[477_rest_api_architecture|REST API]] | 외부/내부 제어 인터페이스 |
| [[569_rbac|RBAC]] ([[569_rbac|Role-Based Access Control]]) | 권한 제어 |
| [[078_etcd_distributed_key_value_store|etcd]] | 클러스터 상태 저장소 |
| Admission Controller | [[164_policy|정책]] [[395_verification_process_review|검증]]과 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
kubectl / controller / kubelet
    │
    ▼
Kube-API Server
    │
    ▼
인증 → 인가 → 승인 → 저장(etcd)
    │
    ▼
Watch 기반 제어평면 반응
```

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 모든 신청서는 먼저 행정실로 가요.
2. 행정실이 [[396_validation|확인]]하고 기록한 뒤 필요한 반에 알려줘요.
3. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]의 [[014_api_posix|API]] 서버도 그 행정실 같은 역할을 해요.
