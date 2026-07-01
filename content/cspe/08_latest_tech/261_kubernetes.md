---
title: "Kubernetes 쿠버네티스 (Kubernetes)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 261
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes를 컨테이너를 원하는 상태로 유지하는 control plane 기반 orchestration system으로 이해하게 만든다.

## 한눈에
- **개요**: 컨테이너화된 application의 배포, scaling, service discovery, self-healing을 자동화하는 open source orchestration platform
- **왜 필요한가**: 수십~수천 개 컨테이너를 서버에 직접 배치하면 장애 복구, 배포 순서, scaling, secret 관리가 사람의 수작업에 의존한다.
- **핵심 직관**: 운영자가 "웹 서버 5개를 항상 유지"라고 선언하면 Kubernetes가 어느 서버에 둘지, 죽으면 어디서 다시 띄울지 계속 맞추는 시스템이다.

## 깊이 이해
- **배경·문제의식**: Docker는 컨테이너 실행 단위를 제공하지만 여러 노드에 걸친 배포, service discovery, rolling update, 장애 복구는 별도 orchestration이 필요하다.
- **작동 원리**: 사용자는 YAML manifest로 desired state를 선언하고, API Server, Scheduler, Controller Manager, kubelet이 실제 cluster 상태를 계속 관찰해 desired state와 맞춘다.
- **비유**: 항공 관제 시스템처럼 비행기가 어디에 있고 어디로 가야 하는지 계속 확인해 충돌과 결항을 줄이는 운영 계층이다.
- **구체 예시**: Deployment replicas를 3으로 선언하면 controller가 Pod 3개를 유지하고, 노드 장애 시 scheduler가 다른 노드에 새 Pod를 배치한다.
- **흔한 오해·주의점**: Kubernetes는 application 품질을 자동으로 보장하지 않는다. Readiness/Liveness probe, resource request/limit, network policy, RBAC를 설계해야 운영 품질이 나온다.

## 연결 개념
- Container Orchestration — Kubernetes가 구현하는 상위 개념
- Service Mesh — Kubernetes service 통신을 세밀하게 제어하는 보완 계층
- GitOps — Kubernetes manifest를 Git 기준으로 배포하는 운영 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Kubernetes는 Pod 실행 도구가 아니라 desired state reconciliation, control plane, workload/resource abstraction으로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes는 container workload의 desired state를 선언하고 controller가 실제 상태를 지속 조정하는 orchestration platform임.
> 2. **가치**: Deployment, Service, HPA, ConfigMap, Secret, RBAC로 배포·확장·발견·보안 운영을 표준화함.
> 3. **판단 포인트**: Cluster 운영 복잡도, resource quota, network policy, observability 없이는 platform risk가 application risk로 전이됨.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Kubernetes 구조 이해 확인 | control plane, node, Pod, Service | Docker 실행 도구로만 설명 |
| 운영 원리 확인 | desired state, reconciliation, scheduler | YAML 배포 절차만 나열 |
| 적용 판단 확인 | HPA, rollout, RBAC, observability | 무조건 MSA에 필요하다고 단정 |

> 요약: 이 문제는 Kubernetes가 선언 상태를 지속 조정하는 control plane임을 설명하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 컨테이너 orchestration platform
- 배경: 컨테이너 수가 증가하면 배포, 장애 복구, service discovery, secret 관리가 수작업 운영으로 감당하기 어려움.
- 필요성: Desired state 기반 control plane으로 Pod 배치, scaling, rollout, self-healing을 자동화해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User / CI-CD -> API Server -> etcd
API Server -> Scheduler / Controller Manager -> Node kubelet -> Pod / Container
           +-> Service / Ingress / RBAC / Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Server | 모든 요청의 control plane 진입점 | 인증·인가·admission 적용 |
| etcd | cluster desired/actual state 저장 | backup과 암호화 필요 |
| Scheduler | Pod를 node에 배치 | request, affinity, taint 고려 |
| kubelet | node에서 Pod 상태 유지 | container runtime과 연동 |

> 요약: Kubernetes는 API Server와 controller가 선언 상태를 관리하고, scheduler와 kubelet이 node 실행 상태를 맞춘다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Manifest 작성 -> API Server 제출 -> etcd 저장
-> Controller가 desired state 감지 -> Scheduler가 Node 선택 -> kubelet이 Pod 실행 -> Probe/Metric으로 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Deployment, Service 등 manifest 제출 | admission pass |
| 2 | controller가 replica 등 desired state 계산 | controller event |
| 3 | scheduler가 resource와 policy 기준으로 node 선택 | scheduling latency |
| 4 | kubelet이 container 실행·probe 확인 | Pod ready 상태 |

> 요약: Kubernetes는 manifest 선언부터 Pod ready 상태까지 controller loop가 계속 비교·조정하는 방식으로 동작한다.

---

## Ⅳ. 특징

| 구분 | VM 중심 운영 | Kubernetes 운영 | 판단 기준 |
|:---|:---|:---|:---|
| 배포 단위 | VM image, process | Pod, Deployment | 배포 빈도 |
| 상태 관리 | 운영 절차 중심 | desired state reconciliation | 자동 복구 요구 |
| 네트워크 | host/IP 중심 | Service, Ingress, NetworkPolicy | service discovery |
| 보안 | 서버 계정 중심 | RBAC, Secret, admission | multi-tenant 요구 |

> 요약: Kubernetes는 서버 중심 운영을 workload 선언과 controller 기반 운영으로 전환하지만 platform 운영 역량이 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM/수동 배포 | Kubernetes control plane | workload 수와 변경 빈도 |
| 비용/성능 | 단순 운영, 낮은 플랫폼 비용 | cluster 운영 비용 추가 | 배포 자동화 가치 |
| 운영/위험 | 서버별 운영 편차 | 표준화, 단 cluster 장애 영향 | SRE 역량 |

> 요약: Kubernetes는 container workload 규모와 변경 빈도가 높을 때 타당하며, 소규모 단일 application에는 운영 복잡도가 더 클 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| resource contention | request/limit 미설정 | namespace quota, limit range | OOMKill, throttling |
| 권한 과다 | RBAC broad role | least privilege, audit log | denied/allowed audit |
| 장애 원인 불명 | observability 부재 | log, metric, trace 표준화 | MTTR |

> 요약: Kubernetes 리스크는 자원, 권한, 관측성에서 발생하며 namespace 단위 통제가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | control plane backup과 node 장애 복구 검증 | chaos test |
| 배포 | rollback 가능한 rollout 전략 | deployment event |
| 보안 | RBAC, Secret 암호화, image scan 적용 | audit, policy report |

> 요약: Kubernetes 운영 성과는 배포 자동화뿐 아니라 복구, 권한, 보안 점검 결과로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Namespace, ResourceQuota, LimitRange, NetworkPolicy를 tenant 또는 service 단위로 먼저 설계함.
2. Deployment는 readiness/liveness probe, rolling update, rollback, PodDisruptionBudget을 포함해 배포 표준으로 정의함.
3. etcd backup, audit log, Prometheus metric, centralized logging을 cluster 운영 baseline으로 구성함.

**결론 (2줄):**
- 기술사 판단: 컨테이너 workload가 다수이고 배포·복구 자동화 요구가 크면 Kubernetes를 선택하고, 단순 배치 workload는 managed service나 serverless를 비교함.
- 향후 방향: Kubernetes는 GitOps, service mesh, policy-as-code와 결합해 cloud native control plane의 사실상 표준으로 유지됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Kubernetes를 설명하시오" | desired state와 reconciliation 흐름 | VM 운영 대비 차이 |
| 요구사항 명시형 | "컨테이너 플랫폼 구축 방안을 제시하시오" | namespace, scheduler, rollout 절차 | resource, RBAC, observability 리스크 |

> 요약: 설명형은 control plane 원리를, 구축형은 운영 통제와 점검 기준을 중심으로 작성한다.
