---
title: "StatefulSet (StatefulSet)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 179
---

# 📖 【암기용】 개념 완전 이해

> 목적: StatefulSet을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: StatefulSet은 Pod마다 **고정된 정체성(ordinal identity)**과 **전용 PVC**를 보장하는 Kubernetes **상태 저장 워크로드 컨트롤러**다. PVC/PV/StorageClass 자체의 구조는 178(Kubernetes Storage)을 참조하고, 여기서는 "Pod의 정체성을 어떻게 고정하는가"가 핵심이다.
- **왜 필요한가**: Deployment는 replica가 서로 완전히 동일·교체 가능하다는 전제로 동작한다. 하지만 DB replica, Kafka broker, ZooKeeper/etcd 노드는 각자 고유 ID·역할·데이터를 가지므로, 이름과 디스크가 무작위로 바뀌면 quorum이 깨지거나 클러스터 재구성에 실패한다.
- **핵심 직관**: Deployment가 "번호표 없는 임시 인력 파견"이라면 StatefulSet은 "사번, 지정석, 개인 사물함이 있는 정규직 배치"다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 상태 저장 워크로드(Stateful Workload) | 인스턴스마다 고유 식별자·데이터를 가져 서로 교체 불가능한 워크로드 — 이 개념의 상위 카테고리 | 지정석 승객 |
| Ordinal Identity | `<name>-0`, `<name>-1`처럼 0부터 순번이 매겨진 고정 Pod 이름 | 사번 |
| Headless Service | ClusterIP를 `None`으로 두어 각 Pod에 개별 DNS(`pod-0.svc.ns.svc.cluster.local`)를 부여하는 Service | 대표 전화번호 대신 내선번호 직통 연결 |
| volumeClaimTemplates | StatefulSet이 Pod별로 자동 생성하는 PVC 템플릿(PVC 자체는 178 참조) | 사물함 자동 배정 규정 |
| OrderedReady (기본 podManagementPolicy) | `pod-0`이 Ready 되어야 `pod-1` 생성을 시작하는 순차 생성·삭제 방식 | 줄 서서 한 명씩 입장 |
| Parallel (podManagementPolicy) | 순서 없이 모든 Pod를 동시에 생성 | 동시 입장 |
| quorum | 분산 시스템이 정상 동작하려면 필요한 최소 생존 노드 수(대개 과반) | 회의 성사에 필요한 최소 출석 인원 |

## 깊이 이해

### Deployment로는 왜 부족한가 (배경)
- Deployment의 Pod는 ReplicaSet이 임의 해시 이름(`web-7d8f9c-x2k1p`)으로 만들고, 어느 Pod가 죽어도 아무 이름의 새 Pod로 대체하면 그만이다. 로드밸런서 뒤의 stateless API 서버라면 문제없다.
- 하지만 3대짜리 MongoDB replica set을 Deployment로 운영하면, Pod가 재시작될 때마다 이름과 (기본 설정이라면) 연결되는 PVC가 달라질 수 있어 "어느 replica가 primary였는지" 식별이 깨지고, 최악의 경우 replica가 서로 다른 디스크를 계속 새로 붙잡아 데이터 정합성이 무너진다.

### ordinal identity + headless Service가 정체성을 고정하는 방식
- StatefulSet `mongo`를 3 replica로 만들면 Pod 이름은 항상 `mongo-0`, `mongo-1`, `mongo-2`로 고정된다. Pod가 죽어도 재생성된 Pod는 같은 순번 이름을 그대로 받는다.
- headless Service(`mongo`)를 붙이면 `mongo-0.mongo.default.svc.cluster.local`처럼 Pod별 고정 DNS가 생겨, 클러스터 안의 다른 노드가 "0번은 항상 이 DNS"로 접속할 수 있다 — Pod IP가 바뀌어도 DNS 레코드가 갱신되어 재접속 로직이 단순해진다.

### volumeClaimTemplates가 178의 PVC 구조를 그대로 재사용하는 방식
- StatefulSet은 Pod마다 별도 PVC를 volumeClaimTemplates로 자동 생성한다. `mongo-0`은 `data-mongo-0`, `mongo-1`은 `data-mongo-1` PVC를 갖는다(PVC/PV/StorageClass 자체 구조는 178 참조).
- 핵심 차이: Pod가 삭제·재생성돼도 같은 순번의 Pod는 같은 이름의 PVC를 다시 mount한다. `mongo-1`이 재시작되면 새 `mongo-1` Pod는 반드시 기존 `data-mongo-1`을 다시 붙잡는다 — 이 "Pod 순번 - PVC 이름"의 1:1 고정이 StatefulSet만의 특징이다.

### 순차 배포(OrderedReady)를 수치로 이해 — quorum 보호
- 기본 정책 OrderedReady에서는 `pod-0`이 Running+Ready 상태가 되어야 `pod-1` 생성을 시작한다. 업데이트(rolling update)도 마찬가지로 번호가 큰 것부터 역순으로 하나씩 교체한다.
- 예: 5노드 etcd 클러스터는 과반(quorum) 3대 이상이 살아 있어야 쓰기가 가능하다. Deployment처럼 여러 Pod를 동시에 재시작하면 순간적으로 생존 노드가 2대로 떨어져 쓰기 불가 상태에 빠질 수 있다. OrderedReady와 PodDisruptionBudget(`maxUnavailable: 1`)을 함께 쓰면 한 번에 1대씩만 내려가게 강제해 quorum 3/5을 항상 유지한다.

### 비유와 흔한 오해
- **비유**: 콜센터 상담원 전원이 동일 업무를 하는 것이 Deployment라면, 상담원마다 개인 내선번호·개인 서류함·담당 고객 이력을 유지해야 하는 전담팀이 StatefulSet이다.
- **오해 1**: "StatefulSet을 쓰면 백업이 자동으로 된다" — 틀렸다. StatefulSet은 이름과 PVC 연결만 고정할 뿐이고, 실제 스냅샷·백업·failover 로직은 Operator나 별도 자동화가 필요하다.
- **오해 2**: "상태가 있으면 무조건 StatefulSet" — 틀렸다. 상태가 외부 관리형 DB(RDS 등)에 있고 Pod 자체는 무상태 API 서버라면 Deployment로 충분하다. 판별 기준은 "Pod 자신이 고유 ID·로컬 디스크·순서를 필요로 하는가"다.

## 연결 개념
- PVC/PV/StorageClass (178) - StatefulSet이 volumeClaimTemplates로 그대로 활용하는 저장소 구조
- Headless Service - ordinal DNS를 제공하는 기반 오브젝트
- Operator - StatefulSet이 다루지 않는 백업·failover·quorum 자동화를 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: StatefulSet 답안은 Deployment와의 차이를 고정 ID, 순서, 고유 PVC, headless Service 기준으로 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: StatefulSet은 상태 저장 애플리케이션에 고정 네트워크 ID와 고유 저장소를 제공하는 컨트롤러임.
> 2. **가치**: Pod 재생성 후에도 ordinal name과 PVC가 유지되어 DB replica, broker, quorum node 운영이 가능함.
> 3. **판단 포인트**: 순서, identity, volume 보존이 필요한 워크로드는 StatefulSet, 무상태 서비스는 Deployment를 선택함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨트롤러 선택 기준 확인 | Deployment vs StatefulSet | 상태 저장이면 무조건 StatefulSet으로 단정 |
| 상태 보존 구조 확인 | ordinal, headless Service, PVC | PVC와 백업을 동일시 |
| 운영 리스크 이해 확인 | quorum, 순차 rollout, 복구 절차 | DB 운영 책임을 Kubernetes에 전가 |

> 요약: StatefulSet 문제는 고정 ID와 고유 저장소가 필요한 조건을 정확히 판단해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: StatefulSet은 상태 저장 Pod 컨트롤러임.
- 배경: 상태 저장 시스템은 Pod별 이름, 순서, 저장소가 바뀌면 quorum, replica, 데이터 정합성 문제가 생긴다.
- 필요성: 고정 네트워크 ID, 순차 배포, PVC 연결로 데이터베이스와 메시지 브로커의 상태 요구를 충족한다.

---

## Ⅱ. 구조 및 구성요소

```text
StatefulSet -> Headless Service -> Pod ordinal DNS
StatefulSet -> volumeClaimTemplates -> Pod별 PVC -> PV
  / web-0 -> pvc-web-0
  / web-1 -> pvc-web-1
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ordinal Identity | `name-0`, `name-1` 고정 이름 | 순서 기반 |
| Headless Service | Pod별 DNS 제공 | ClusterIP None |
| volumeClaimTemplates | Pod별 PVC 생성 | 삭제 후에도 PVC 유지 가능 |
| Ordered rollout | 생성, 업데이트, 삭제 순서 제어 | OrderedReady |

> 요약: StatefulSet은 고정 이름, 고정 DNS, 고유 PVC, 순서 제어로 상태 저장 요구를 처리함.

---

## Ⅲ. 동작원리 및 흐름도

```text
StatefulSet 생성 -> web-0 생성/Ready -> web-1 생성/Ready -> PVC bind -> 고정 DNS 제공 -> 순차 업데이트
  / 장애 발생 -> 같은 ordinal Pod 재생성
  / PVC 유지 -> 기존 데이터 재사용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | StatefulSet과 Headless Service 생성 | serviceName 연결 |
| 2 | ordinal 순서대로 Pod 생성 | `pod-0` Ready 후 `pod-1` |
| 3 | volumeClaimTemplates로 PVC 생성 | PVC Bound |
| 4 | Pod 재생성 시 동일 PVC mount | 데이터 유지 |
| 5 | updateStrategy로 순차 교체 | quorum 유지 |

> 요약: StatefulSet은 ordinal 순서와 PVC 재사용으로 상태 저장 인스턴스의 정체성을 유지함.

---

## Ⅳ. 특징

| 구분 | Deployment | StatefulSet | 수치/판단 포인트 |
|:---|:---|:---|:---|
| Pod identity | 임의 이름 | ordinal 고정 | broker ID, replica ID |
| 네트워크 | Service로 집합 접근 | Pod별 DNS | `pod-0.svc` |
| 저장소 | 공유/임시 가능 | Pod별 PVC | RWO volume |
| 배포 순서 | 병렬 중심 | 순차 생성/삭제 | quorum 3/5 유지 |

> 요약: StatefulSet은 무상태 확장보다 정체성과 저장소 보존이 필요한 워크로드에 적합함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Deployment + PVC | StatefulSet + Headless Service | 고정 ID 필요 |
| 비용/처리 | 수동 DB VM 운영 | Kubernetes 상태 저장 운영 | replica 3개 이상 |
| 운영/위험 | Pod 교체 시 ID 변동 | ordinal/PVC 유지 | quorum, failover 설계 |

> 요약: StatefulSet은 identity 의존성이 있는 상태 저장 시스템에서 선택하고 무상태 API는 Deployment를 유지함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| quorum 손상 | 동시 Pod 교체 | OrderedReady, PDB, maxUnavailable 제한 | available replica 수 |
| 데이터 손실 | PVC 삭제, 백업 부재 | Retain policy, snapshot | restore test 성공 |
| 복구 지연 | 수동 failover | Operator, readiness gate | RTO 30분 이하 |

> 요약: StatefulSet 운영 리스크는 quorum, PVC, failover 절차로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용 replica | quorum 유지 3/5 이상 | app metric |
| 저장소 | PVC Bound 100%, snapshot 성공 | CSI metric |
| 배포 영향 | rolling update 중 error 0.1% 이하 | APM, event |

> 요약: StatefulSet은 replica quorum, PVC 상태, 배포 중 오류율로 운영 품질을 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 식별성 설계: headless Service와 ordinal DNS를 사용해 DB replica, broker ID, shard ID를 고정
2. 저장소 설계: volumeClaimTemplates, RWO PVC, reclaimPolicy Retain, VolumeSnapshot 주기 15분 적용
3. 운영 통제: PDB, OrderedReady, readinessProbe, Operator 기반 backup/failover 절차를 함께 구성

**결론 (2줄):**
- 기술사 판단: 고정 ID와 고유 PVC가 필요하면 StatefulSet, 동일 replica 확장이면 Deployment를 선택함
- 향후 방향: StatefulSet은 CSI, Operator, Snapshot과 결합해 Kubernetes 상태 저장 플랫폼의 기본 컨트롤러가 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "StatefulSet을 설명하시오" | ordinal 생성, PVC bind, 순차 업데이트 흐름 | Deployment와 차이 |
| 요구사항 명시형 | "DB 운영 방안을 제시하시오", "비교하시오" | backup, quorum, failover 흐름 | PVC, PDB, Operator 선택 기준 |

> 요약: 설명형은 구조와 원리, 운영형은 quorum과 복구 절차 중심으로 전환함.
