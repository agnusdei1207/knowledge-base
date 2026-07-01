---
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 173
---

# 📖 【암기용】 개념 완전 이해

> 목적: 쿠버네티스 아키텍처를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 컨테이너 애플리케이션을 선언형으로 배포, 스케줄링, 복구, 확장하는 오케스트레이션 구조
- **왜 필요한가**: 컨테이너 수가 수십 개를 넘으면 배치 위치, 장애 복구, 설정, 네트워크, 저장소를 수동으로 맞추기 어렵다.
- **핵심 직관**: 사용자는 원하는 상태를 제출하고, Kubernetes는 현재 상태를 관찰해 차이를 계속 줄이는 제어 시스템이다.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 실행 단위일 뿐 클러스터 배치, 장애 감지, 롤링 배포, 서비스 발견을 스스로 처리하지 않는다. Kubernetes는 Desired State와 Controller Reconciliation으로 이 문제를 해결한다.
- **작동 원리**: API Server가 모든 요청의 관문이고, etcd가 상태를 저장한다. Scheduler는 Pod를 Node에 배치하고, Controller Manager는 Deployment, ReplicaSet 등 객체 상태를 맞춘다. kubelet은 노드에서 Pod를 실행한다.
- **비유**: 건물 관리 시스템에서 입주 신청(API), 장부(etcd), 배정 담당(Scheduler), 유지보수팀(Controller), 현장 관리자(kubelet)가 나뉜 구조와 같다.
- **구체 예시**: 사용자가 replicas 3의 Deployment를 제출하면 API Server에 저장되고 Controller가 ReplicaSet을 만들며 Scheduler가 3개 Pod를 Node에 배치하고 kubelet이 containerd를 통해 실행한다.
- **흔한 오해·주의점**: Kubernetes는 애플리케이션 코드를 대신 수정하지 않는다. health check, resource request, 보안 정책, rollout 전략을 명세해야 자동화가 작동한다.

## 연결 개념
- Pod - Kubernetes의 최소 배포 단위
- Controller - Desired State와 Current State를 맞추는 제어 루프
- Service/Ingress - Pod IP 변동을 감추는 접근 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Kubernetes 아키텍처는 구성요소 나열이 아니라 선언형 API와 제어 루프가 상태 차이를 수렴시키는 구조로 설명해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes는 API Server 중심의 선언형 컨테이너 오케스트레이션 플랫폼임.
> 2. **가치**: Scheduler, Controller, kubelet이 Desired State를 지속 조정해 배포, 복구, 확장을 자동화함.
> 3. **판단 포인트**: 설계 시 control plane HA, etcd 백업, resource request, RBAC, observability를 함께 검토해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 아키텍처 구성 이해 확인 | Control Plane, Worker Node, Add-on | Pod 실행만 설명 |
| 선언형 제어 원리 확인 | Desired State, Reconciliation | 명령형 배포 도구로 오해 |
| 운영 설계 역량 확인 | HA, etcd backup, RBAC, monitoring | 장애 도메인과 보안 통제 누락 |

> 요약: Kubernetes 답안은 제어평면과 워커노드의 역할 분리, 상태 수렴 원리, 운영 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Kubernetes는 컨테이너 오케스트레이션 플랫폼임.
- 배경: MSA와 클라우드 환경에서는 컨테이너 배치, 장애 복구, 서비스 발견, 확장, 설정 관리가 반복된다.
- 필요성: 선언형 API와 컨트롤러 루프로 배치, 복구, 확장, 설정 관리 상태를 지속적으로 조정한다.

---

## Ⅱ. 구조 및 구성요소

```text
User/YAML -> API Server -> etcd
API Server -> Scheduler -> Worker Node
API Server -> Controller Manager -> Desired State 조정
Worker Node -> kubelet -> container runtime -> Pod
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Server | 인증, 인가, 객체 저장 관문 | RBAC, Admission |
| etcd | 클러스터 상태 저장 | quorum, snapshot |
| Scheduler | Pod를 Node에 배치 | request, affinity, taint |
| kubelet | 노드의 Pod 실행 상태 관리 | CRI 연동 |

> 요약: Control Plane은 상태 결정을 담당하고 Worker Node는 kubelet과 런타임으로 Pod 실행을 담당함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Manifest 제출 -> API 검증/저장 -> Controller 감지 -> Scheduler 배치 -> kubelet 실행 -> 상태 보고
  / 불일치 발생 -> Controller 재조정
  / 노드 장애 -> 재스케줄링
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | kubectl 또는 CI/CD가 YAML 제출 | schema, admission 통과 |
| 2 | API Server가 etcd에 Desired State 저장 | resourceVersion 생성 |
| 3 | Controller가 필요한 Pod 수 계산 | replica 일치 |
| 4 | Scheduler가 Node 선택 | request 충족, 정책 충족 |
| 5 | kubelet이 Runtime으로 Pod 실행 | Ready 상태, event |

> 요약: Kubernetes는 상태 저장, 감지, 배치, 실행, 보고를 반복해 선언한 상태에 수렴함.

---

## Ⅳ. 특징

| 구분 | 수동 컨테이너 운영 | Kubernetes | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 배포 | 서버별 명령 실행 | Deployment, rollout | 배포 실패율 5% 이하 |
| 복구 | 운영자 개입 | Controller 재생성 | MTTR 10분 이하 |
| 확장 | VM/서버 증설 | HPA, Cluster Autoscaler | CPU 70% 기준 |
| 접근 | 고정 IP 의존 | Service, Ingress | endpoint 자동 갱신 |

> 요약: Kubernetes는 컨테이너 실행보다 상태 기반 운영 자동화와 서비스 추상화에 가치가 있음.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM/수동 스크립트 | Control Plane + Worker Node | 컨테이너 50개 이상 |
| 비용/처리 | 서버별 배포 | 선언형 rollout | 배포 주기 일 1회 이상 |
| 운영/위험 | 운영자 의존 복구 | controller 기반 복구 | SLO 99.9% 요구 |

> 요약: 컨테이너 수와 배포 빈도가 커질수록 Kubernetes의 선언형 운영 구조가 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Control Plane 장애 | API Server, etcd 단일 장애 | 3/5 node HA, etcd snapshot | API p99, etcd quorum |
| 자원 경합 | request/limit 미설정 | LimitRange, ResourceQuota | CPU throttling, OOMKilled |
| 권한 과다 | cluster-admin 남용 | RBAC least privilege, audit log | cluster-admin 사용자 수 |

> 요약: Kubernetes 운영 리스크는 제어평면 가용성, 자원 모델, 권한 통제로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| API 지연 | API Server p99 1초 이하 | apiserver metric |
| 복구 시간 | Pod 재생성 2분 이하 | event, Prometheus |
| 보안 통제 | RBAC audit 위반 0건 | audit log, OPA |

> 요약: 아키텍처 검증은 API 응답, 복구 시간, 권한 감사 지표로 수행함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 제어평면 설계: API Server 3대, etcd 3/5대 quorum, snapshot 주기 1시간 이하로 Control Plane HA 구성
2. 워크로드 표준: request/limit, liveness/readiness probe, PDB, rollout strategy를 기본 템플릿에 포함
3. 운영 통제: RBAC least privilege, audit log 180일 보관, Prometheus/Grafana 기반 SLO dashboard 구축

**결론 (2줄):**
- 기술사 판단: Kubernetes는 컨테이너 실행 도구가 아니라 선언형 상태 제어 플랫폼으로 도입해야 함
- 향후 방향: GitOps, Service Mesh, Policy as Code와 결합해 플랫폼 엔지니어링의 실행 기반이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "쿠버네티스 아키텍처를 설명하시오" | 선언형 상태 수렴 흐름 | Control Plane/Worker Node 역할 |
| 요구사항 명시형 | "설계하시오", "운영 방안을 제시하시오" | HA, 배포, 복구, 관측 흐름 | SLO, RBAC, etcd 백업 기준 |

> 요약: 설명형은 구성과 원리, 설계형은 HA와 운영 통제 중심으로 전환함.
