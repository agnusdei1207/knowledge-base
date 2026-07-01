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
- **개요**: Pod별 고정 이름, 순서 있는 배포, 고유 PVC를 제공하는 Kubernetes 상태 저장 워크로드 컨트롤러
- **왜 필요한가**: 데이터베이스, 메시지 큐, 분산 저장소는 Pod가 교체되어도 같은 이름과 같은 디스크가 유지되어야 한다.
- **핵심 직관**: Deployment가 번호표 없는 임시 직원을 뽑는 방식이라면 StatefulSet은 직원별 사번, 자리, 개인 사물함을 유지하는 방식이다.

## 깊이 이해
- **배경·문제의식**: Deployment는 replica가 서로 동일하고 어느 Pod가 사라져도 대체 가능하다는 전제에 적합하다. 하지만 DB replica, Kafka broker, ZooKeeper node처럼 각 인스턴스가 고유 ID와 데이터를 가지면 무작위 교체가 장애 원인이 된다.
- **작동 원리**: StatefulSet은 `web-0`, `web-1` 같은 ordinal identity를 부여하고 headless Service로 고정 DNS를 제공한다. volumeClaimTemplates로 Pod별 PVC를 만들며 생성, 업데이트, 삭제 순서를 제어한다.
- **비유**: 같은 역할의 상담원이라도 개인 내선번호와 보관함이 있으면 아무 자리나 바꿔 앉을 수 없는 것과 같다.
- **구체 예시**: 3개 replica MongoDB를 StatefulSet으로 구성하면 `mongo-0`, `mongo-1`, `mongo-2`가 각각 `data-mongo-0` PVC를 사용하고, 재시작 후에도 같은 PVC를 다시 mount한다.
- **흔한 오해·주의점**: StatefulSet이 데이터 백업을 대신하지 않는다. 고유 PVC를 유지할 뿐이며 스냅샷, 복구, quorum 관리는 별도 설계가 필요하다.

## 연결 개념
- Headless Service - Pod별 고정 DNS 제공
- PVC/PV - Pod별 고유 저장소 유지
- Operator - DB 클러스터 생성, 백업, failover 자동화 보완

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
