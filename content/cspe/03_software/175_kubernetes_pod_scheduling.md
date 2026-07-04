---
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 175
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes Pod 스케줄링을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Pod 스케줄링은 **Scheduler**가 대기 중인 Pod를 **자원 요청(Resource Request)**과 배치 정책을 기준으로 특정 Node에 배정하는 **Filter → Score → Bind** 3단계 과정이다.
- **왜 필요한가**: 클러스터의 노드는 CPU·Memory·GPU·Zone·보안 등급·비용이 서로 다르다. 이를 무시하고 아무 빈 노드에나 배치하면 자원 경합, 장애 도메인 집중, GPU 미사용, 규제 위반이 발생한다.
- **핵심 직관**: Scheduler는 빈 자리에 아무나 앉히는 단순 배정자가 아니라, 조건을 만족 못 하는 곳을 먼저 걸러내고 남은 곳 중 가장 적합한 자리를 골라주는 배치 심사관이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Scheduler | Pending Pod를 감지해 적합한 Node를 결정하는 Control Plane 컴포넌트 — 이 개념이 속한 **상위 개념** | 배치 심사관 |
| Resource Request | 컨테이너가 최소한 보장받는 CPU/Memory 양 — Scheduler의 배치 판단 **기준**이 됨 | 예약된 좌석 수 |
| Resource Limit | 컨테이너가 쓸 수 있는 최대 CPU/Memory — 실행 중 제한일 뿐 배치 판단에는 쓰이지 않음 | 좌석의 정원 상한 |
| Filter (Predicate) | 조건을 만족 못 하는 Node를 걸러내는 1단계 | 예약 조건 미달 객실 제외 |
| Score (Priority) | Filter를 통과한 Node에 점수를 매겨 순위를 매기는 2단계 | 남은 객실 중 랭킹 매기기 |
| Bind | 최종 선택된 Node에 Pod를 확정 할당하는 3단계 | 객실 배정 확정 |
| NodeAffinity / PodAffinity | 특정 라벨을 가진 Node/Pod에 붙거나(Affinity) 떨어지려는(Anti-Affinity) 선호·강제 조건 | 팀원끼리 같은 구역에 앉기 |
| Taint / Toleration | Node가 "허가받지 않은 Pod는 못 온다"를 선언(Taint)하고, Pod가 "나는 이 조건을 견딘다"를 선언(Toleration)해야 배치가 허용되는 방식 | 출입 제한 구역 + 출입증 |
| topologySpreadConstraints | 장애 도메인(Zone·Node)별로 Pod를 고르게 분산 배치하는 제약 | 계란을 한 바구니에 담지 않기 |
| Priority / Preemption | 우선순위가 낮은 기존 Pod를 축출(evict)해서라도 우선순위 높은 Pod를 배치하는 기법 | 응급환자 새치기 |

## 깊이 이해

### 왜 자동 배치 기준이 필요한가 (배경)
- 클러스터에는 CPU·Memory 여유가 다르고, GPU가 달린 노드와 아닌 노드가 섞이고, Zone(가용영역)이 다르고, 결제처럼 보안 등급이 높은 워크로드 전용 노드가 따로 있을 수 있다. Pod마다 요구하는 자원·정책이 다르므로, 사람이 매번 수동으로 고르는 대신 Scheduler가 일관된 규칙으로 판단해야 한다.

### Filter → Score → Bind — 수치 워크드 예제
- 노드 5대 클러스터에서, GPU 1개와 CPU 2코어·Memory 4Gi를 요구하는 Pod가 Pending으로 들어왔다고 하자.
1. **Filter**: 5대 중 GPU가 없는 노드 3대는 즉시 제외된다 → 후보 2대(NodeA, NodeB)로 좁혀진다.
2. **Score**: 남은 2대에 점수를 매긴다. 예를 들어 NodeA는 CPU 여유율 80%로 80점, NodeB는 CPU 여유율 50%로 50점을 받으면 NodeA가 선정된다.
3. **Bind**: API Server에 해당 Pod의 nodeName을 NodeA로 기록해 배치를 확정한다.

### request 기준 bin-packing — 수치로 이해
- 8코어 노드에 이미 CPU 5코어가 request된 상태라고 하자. 신규 Pod가 CPU 2코어를 request하면 여유 3코어 안에 들어가므로 Filter를 통과해 배치 가능하다. 반대로 신규 Pod가 CPU 4코어를 request하면 여유(3코어)를 넘으므로 이 노드에서는 Filter에서 제외되고, 클러스터 전체에 여유 노드가 없으면 Pod는 Pending으로 남는다.
- 이때 판단 기준은 Limit이 아니라 Request다. Limit만 설정하고 Request를 비워두면 Scheduler는 사실상 자원을 거의 안 쓰는 것처럼 계산해 과밀 배치(overcommit)를 일으킬 수 있다.

### Taint/Toleration — GPU 전용 노드 예제
- GPU 노드에 `nvidia.com/gpu=true:NoSchedule`이라는 Taint를 걸면, 이 Toleration이 없는 일반 Pod는 Filter 단계에서부터 배치 후보에서 제외된다. GPU 워크로드에 해당 Toleration을 부여해야만 그 노드에 배치될 수 있다.
- Affinity는 "끌어당기는" 선호(있으면 유리)인 반면, Taint/Toleration은 "막는" 방식(허가 없으면 아예 배치 불가)이라는 점이 핵심 차이다.

### topologySpreadConstraints — 수치로 이해
- replicas=6인 서비스가 Zone 3개에 걸쳐 있고 topologySpreadConstraints(maxSkew=1)를 적용하면, Zone당 2개씩 균등 배치된다. Zone 1개에 장애가 나도 전체 6개 중 2개(약 33%)만 손실되어 서비스가 유지된다. 이 제약이 없으면 6개가 한 Zone에 몰려 그 Zone 장애 시 전체가 사라질 수 있다.

### Priority/Preemption — 수치로 이해
- 클러스터 자원이 꽉 찬 상태에서 priority=1000인 Pod가 배치를 요청하면, Scheduler는 priority=100인 기존 Pod를 축출(evict)해 공간을 확보한 뒤 우선순위 높은 Pod를 배치한다. 핵심 업무(P1)를 보호하고 부가 업무(배치 작업 등)를 밀어내는 데 쓰인다.

### 비유
- 호텔 예약에서 금연실·침대 수·전망·가격 조건을 먼저 걸러내고(Filter), 남은 객실 중 점수가 높은 방을 고르는(Score) 뒤 최종 배정(Bind)하는 절차와 같다.

### 흔한 오해·주의점
- Limit만 설정하고 Request를 비워두면 스케줄링 기준으로 반영되지 않는다. Scheduler는 Request를 기준으로 배치 가능성을 계산하며 Limit은 실행 중 자원 상한일 뿐이다.

## 연결 개념
- Pod 생명주기(174) — 여기서 Filter를 통과 못 하면 Pod는 Pending Phase에 계속 머무름
- 쿠버네티스 아키텍처(173) — Scheduler는 Control Plane의 한 컴포넌트
- Service/Ingress(176) — Bind되어 Ready가 된 Pod가 Endpoint에 편입돼 실제 트래픽 대상이 됨

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스케줄링 답안은 Filter, Score, Bind 흐름과 request/affinity/taint 정책을 장애 도메인·비용·자원 활용 관점으로 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pod 스케줄링은 Pending Pod를 자원과 정책 조건에 맞는 Node에 binding하는 의사결정 과정임.
> 2. **가치**: CPU/Memory/GPU request, affinity, taint로 자원 경합과 장애 집중을 통제함.
> 3. **판단 포인트**: 배치 실패는 용량 부족뿐 아니라 정책 충돌, taint 미허용, PVC zone 제약으로 분석해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스케줄러 원리 이해 확인 | Filter, Score, Bind | 라운드로빈 배치로 설명 |
| 배치 정책 설계 확인 | request, affinity, taint, topology spread | limit와 request 혼동 |
| 장애 분석 역량 확인 | Pending 원인, event, resource pressure | CPU 부족만 원인으로 단정 |

> 요약: 스케줄링 문제는 배치 알고리즘과 정책 충돌 분석을 함께 써야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Pod 스케줄링은 Pod를 Node에 배치하는 과정임.
- 배경: 클러스터에는 자원, Zone, 보안 등급, 비용이 다른 노드가 존재한다.
- 필요성: request, affinity, taint, topology spread 기준으로 Pending, 자원 경합, 장애 도메인 집중을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Pending Pod -> Scheduler Queue -> Filter -> Score -> Bind -> kubelet 실행
  / Filter: resource, taint, volume
  / Score: spread, affinity, utilization
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scheduling Queue | 배치 대기 Pod 관리 | priority 반영 |
| Filter Plugin | 배치 불가 노드 제거 | NodeResourcesFit, TaintToleration |
| Score Plugin | 후보 노드 점수화 | topology spread |
| Bind | 선택 노드에 Pod 할당 | API Server binding |

> 요약: Scheduler는 대기 Pod를 필터링, 점수화, 바인딩 단계로 처리함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> request/정책 확인 -> 노드 필터링 -> 노드 점수화 -> 바인딩 -> kubelet 실행
  / 후보 없음 -> Pending
  / preemption 가능 -> 낮은 priority Pod 축출
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Pending Pod 감지 | scheduling queue 입력 |
| 2 | request, nodeSelector, affinity, taint 확인 | 후보 노드 수 |
| 3 | Filter로 부적합 노드 제외 | Unschedulable event |
| 4 | Score로 최종 노드 선정 | plugin score |
| 5 | Bind 후 kubelet 실행 | assigned node, Ready |

> 요약: 스케줄러는 배치 불가 노드를 제거한 뒤 정책 점수를 반영해 최종 노드를 결정함.

---

## Ⅳ. 특징

| 구분 | 기본 배치 | 정책 기반 스케줄링 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 자원 | request 기준 | CPU/Memory/GPU request | Pending 0건 |
| 장애 분산 | 노드 여유 기준 | topology spread, anti-affinity | Zone별 replica 분산 |
| 전용 노드 | 구분 약함 | taint/toleration | GPU/보안 노드 |
| 우선순위 | 동일 처리 | priority, preemption | P1 workload 보호 |

> 요약: Kubernetes 스케줄링은 자원 충족, 장애 분산, 전용 노드, 우선순위를 함께 판단함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 서버 지정 | Scheduler plugin 기반 배치 | 노드 10대 이상 |
| 비용/처리 | 과잉 증설 | request 기반 bin packing | CPU 사용률 40~70% |
| 운영/위험 | 장애 도메인 집중 | topology spread | Zone 장애 영향 |

> 요약: 대규모 클러스터는 request와 topology 정책을 함께 적용해야 비용과 장애 영향을 통제함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Pending 증가 | request 과다, taint 미허용 | event 분석, request 조정 | unschedulable Pod 수 |
| 노드 경합 | request 미설정 | LimitRange, VPA 권고 | CPU throttling |
| 장애 집중 | anti-affinity 부재 | topologySpreadConstraints | Zone별 replica 편차 |

> 요약: 스케줄링 리스크는 Pending, 자원 경합, 장애 집중 지표로 조기 식별함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배치 지연 | scheduling latency p95 5초 이하 | scheduler metric |
| 자원 모델 | request 설정률 100% | policy report |
| 장애 분산 | Zone별 replica 편차 1 이하 | kube-state-metrics |

> 요약: 스케줄링 품질은 지연, request 설정률, topology 분산으로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 자원 기준화: 모든 Pod에 CPU/Memory request를 설정하고 LimitRange로 request 누락 0건 유지
2. 배치 정책화: P1 서비스는 topologySpreadConstraints와 podAntiAffinity로 Zone별 replica 편차 1 이하 적용
3. 전용 노드 운영: GPU, 보안, 배치 노드는 taint/toleration과 nodeSelector로 workload를 분리

**결론 (2줄):**
- 기술사 판단: Scheduler는 빈 노드 선택기가 아니라 자원, 정책, 장애 도메인을 동시에 평가하는 제어 구성요소임
- 향후 방향: Scheduler Framework, VPA, Cluster Autoscaler가 결합되어 정책 기반 용량 관리로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Pod 스케줄링을 설명하시오" | Filter, Score, Bind 흐름 | request, affinity, taint 비교 |
| 요구사항 명시형 | "배치 정책을 설계하시오", "Pending 원인을 설명하시오" | 정책 충돌과 event 분석 | topology, priority, 전용 노드 기준 |

> 요약: 설명형은 알고리즘 흐름, 설계형은 정책 조합과 장애 분석 중심으로 전환함.
