---
title: "127. Service Discovery - MSA 서비스 자동 등록·탐색 메커니즘"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery는 <strong>MSA에서 동적으로 변하는 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 인스턴스의 위치(IP:<a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a>)를 자동으로 등록·탐색·갱신</strong>하는 메커니즘이며, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))가 핵심 컴포넌트이다.
> 2. **가치**: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 인스턴스는 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)·재배포 시 <strong>IP가 수시로 변경</strong>되므로 하드코딩이 불가능하며, [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery가 <strong>"주문 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 어디 있어?"에 실시간 답변</strong>한다.
> 3. **판단 포인트**: <strong>Client-side(클라이언트가 <a href="/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a> 조회)</strong> vs <strong>Server-side(로드밸런서가 <a href="/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a> 조회)</strong>를 구분하고, K8s의 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반 [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Service Discovery 동작                             |
+-------------------------------------------------------+
|  1. 서비스 인스턴스 시작 -> Registry에 등록           |
|     (Order-Svc: 10.0.1.5:8080)                       |
|  2. 호출자가 "Order-Svc 어디?" -> Registry 조회       |
|  3. Registry 응답: 10.0.1.5:8080                     |
|  4. 호출자 -> 10.0.1.5:8080 직접 호출                |
|  5. 인스턴스 종료 -> Registry에서 제거 (헬스체크)     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery는 <strong>전화번호부</strong>이다. 사람([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 이사(IP 변경)해도 전화번호부([레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))를 보면 **현재 주소를 찾을 수 있다**.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Client-side vs Server-side

| 방식 | 동작 | 대표 |
|:---|:---|:---|
| **Client-side** | 클라이언트가 [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 조회 + LB | **Eureka** |
| **Server-side** | LB가 [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 조회 | <strong>K8s <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a></strong> |

### K8s [Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/)
- [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> kube-dns에 자동 등록.
- `order-svc.default.svc.cluster.local`로 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 조회.

- **📢 섹션 요약 비유**: Client-side는 직접 전화번호부를 찾는 것, Server-side는 안내 데스크(LB)에 물어보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 하드코딩 | [Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/) |
|:---|:---|:---|
| **IP 변경** | 코드 수정 | **자동 갱신** |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | 수동 | **동적 등록** |
| **장애** | 감지 불가 | **헬스체크 제거** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 도구
- **Consul** (HashiCorp): [Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/) + [Config](/studynote/15_devops_sre/01_culture_methodology/009_config/).
- **Eureka** (Netflix): Client-side, Spring Cloud.
- <strong>K8s <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a></strong>: Server-side, [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반.
- <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/">etcd</a></strong>: K8s의 상태 저장소.

---

## Ⅴ. 기대효과 및 결론

[Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery는 <strong>MSA의 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간 통신의 기본 인프라</strong>이며, K8s 환경에서는 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반으로 투명하게 제공된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> <a href="/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a></strong> | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 위치 저장소 |
| **헬스체크** | 비정상 인스턴스 자동 제거 |
| **Consul** | HashiCorp [서비스 디스커버리](/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/) |
| **Eureka** | Netflix 클라이언트 사이드 |
| <strong>K8s <a href="/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/">DNS</a></strong> | 서버 사이드 디스커버리 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드코딩 IP (전통, ~2010s)]
    |
    v
[Client-side Discovery (Eureka, 2012~)]
    |
    v
[Server-side Discovery (K8s Service, 2015~)]
    |
    v
[Service Mesh (Istio/Envoy, 2018~) — 투명한 Discovery]
    |
    v
[현재: 멀티 클러스터 Discovery — 클러스터 간 서비스 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Discovery는 <strong>전화번호부</strong>예요. 친구([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 이사해도 <strong>새 주소</strong>를 찾을 수 있어요.
2. 전화번호부가 없으면 친구가 이사할 때마다 **직접 물어봐야** 해서 불편해요.
3. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s)는 전화번호부를 <strong>자동으로 업데이트</strong>해줘서 편리하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 126 / 371

<- **이전**: [126. BFF (Backend For Frontend) - 클라이언트별 맞춤 API 레이어](/studynote/13_cloud_architecture/03_msa_serverless/126_bff/)
**다음**: [128. Circuit Breaker - MSA 장애 전파 차단 패턴](/studynote/13_cloud_architecture/03_msa_serverless/128_circuit_breaker/) ->

---
