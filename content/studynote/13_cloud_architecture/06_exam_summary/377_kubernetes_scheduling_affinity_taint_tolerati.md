---
title: "377. 쿠버네티스 스케줄링 노드 어피니티 테인트 (Kubernetes Scheduling Affinity Taint Toleration)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스 스케줄링은 **kube-scheduler**의 Scheduling Framework(PreFilter->Filter->Score->Reserve->Permit->PreBind->Bind 플러그인 체인)를 통해 **Node Affinity(노드 속성 매칭)**, **Pod Affinity/Anti-Affinity(토폴로지 도메인 기반 동거/분리)**, **Taints & Tolerations(노드 거부 + 파드 허용 매커니즘)** 3축으로 제어하며, 각 규칙은 `required`와 `preferred` 두 가지 강도(또는 `IgnoredDuringExecution` vs `RequiredDuringExecution`)로 정의된다.
> 2. **가치**: 단일 클러스터에서 GPU 노드, SSD 노드, 베어메탈 노드 등 **이종(heterogeneous) 하드웨어 자원**을 효율적으로 분리 활용하고, 고가용성·비용 최적화·데이터 지역성(Data Locality)을 동시에 달성할 수 있어, 멀티 AZ·하이브리드 클라우드 환경의 **TCO 30~50% 절감**과 **SLO 위반 0건** 수준의 배치가 가능하다.
> 3. **판단 포인트**: 스케줄링 규칙이 과도하게 엄격(strict)하면 **Pending 파드 누적**으로 인한 클러스터 포화, 너무 느슨하면 **노드 편중(Skew)·핫스팟** 발생. `requiredDuringSchedulingRequiredDuringExecution` 사용 시 롤링 업데이트 중 노드 컨디션 변경으로 **예기치 못한 Eviction**이 발생할 수 있어, 운영 시 **PodDisruptionBudget(PDB)**·`topologySpreadConstraints`·`cluster-autoscaler`와의 정합성을 반드시 검증해야 한다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스 초기(v1.0~v1.5)에는 스케줄링 제어가 `nodeName` 하드코딩과 `nodeSelector`(라벨 단순 매칭) 수준에 머물러, **GPU·NVMe·베어메탈** 등 이종 하드웨어가 혼재하는 환경에서 "어떤 파드를 어디에 배치할 것인가"를 세밀하게 제어하기 어려웠다. 특히 ① **전용 노드 분리**(법적 컴플라이언스용), ② **데이터 지역성**(빅데이터·ML 워크로드), ③ **장애 도메인 분산**(HA), ④ **비용 최적화**(스팟 인스턴스 활용)을 단일 메커니즘으로 표현할 수 없었다.

이를 해결하기 위해 v1.6에서 **Taints and Tolerations**(#41511), v1.8에서 **Inter-Pod Affinity/Anti-Affinity**(#26880), v1.10에서 **Node Affinity**가 GA 되었고, v1.16에서 **Even Pods Spread(현 topologySpreadConstraints)**가 베타 도입되었다. 현재는 Scheduling Framework v2 기반의 12개 확장 포인트(QueueSort, PreFilter, Filter, PostFilter, Reserve, Permit, PreBind, Bind, Unreserve, PostBind, Reserve, WaitOnPermit)에서 플러그인 형태로 구현되어, **확장성과 선언형 정책 표현**을 동시에 만족한다.

```text
[문제 상황: 이종 하드웨어 클러스터의 스케줄링 난제]

   +---------------------------------------------------------+
   |                Kubernetes Cluster (v1.28+)               |
   |                                                         |
   |  Node-A (GPU A100)  Node-B (CPU 64c)  Node-C (Spot VM)  |
   |  +------------+    +------------+    +------------+    |
   |  | GPU Driver |    | NVMe SSD   |    | Preemptible|    |
   |  | 80GB VRAM  |    | 4TB Local  |    | Low Cost   |    |
   |  +------------+    +------------+    +------------+    |
   |       ^                  ^                 ^           |
   |       |                  |                 |           |
   |   +---+----+        +----+---+        +----+---+      |
   |   |ML Pod  |        |DB Pod  |        |BatchPod|      |
   |   |(need   |        |(need   |        |(tolerate|     |
   |   | GPU)   |        | SSD)   |        | spot)   |     |
   |   +--------+        +--------+        +--------+      |
   |                                                         |
   |   ❌ 문제1: ML Pod가 CPU 노드에 스케줄 -> OOM 즉시 실패 |
   |   ❌ 문제2: DB Pod가 HDD 노드 스케줄 -> IOPS 1/10     |
   |   ❌ 문제3: 핵심 파드가 Spot 노드 -> 강제 Eviction     |
   +---------------------------------------------------------+

   ✅ 해결: Affinity(긍정적 끌어당김) + Taint(부정적 밀어냄)로
            양방향 제어로 "맞는 파드를 맞는 노드에" 배치
```

**기존(nodeSelector only) vs 신규(Affinity+Taint+Toleration) 비교**:
- `nodeSelector`: `kubernetes.io/os=linux` 같은 **단일 라벨 equality**만 지원, OR·IN 연산 불가
- `nodeAffinity`: `In/NotIn/Exists/DoesNotExist` 4종 연산자 + Gt/Lt(버전 1.28 GA) + `required/preferred` 강도
- `podAffinity`: 라벨 셀렉터로 **다른 파드와의 관계**를 토폴로지 키(`kubernetes.io/hostname`, `topology.kubernetes.io/zone` 등)로 표현

- **📢 섹션 요약 비유**: 마치 **호텔 컨시어지 시스템**과 같다. "VIP 손님(파드)"이 "스위트룸(GPU 노드)"만 받겠다고 선언(Affinity)하고, 동시에 "스위트룸" 쪽에서 "VIP 외 출입금지(Taint)"라고 적어두면, 오직 VIP만 열쇠(Toleration)를 들고 들어가게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Scheduling Framework 플러그인 체인

kube-scheduler는 **2단계**(Scheduling Cycle, Binding Cycle)로 동작하며, 각 단계에서 확장 포인트가 호출된다. Node Affinity와 Taint/Toleration은 **Filter** 단계의 `NodeAffinity` 플러그인과 `TaintToleration` 플러그인이 담당하고, Pod Affinity는 `InterPodAffinity` 플러그인이 담당한다.

```text
[Scheduling Framework 처리 흐름 - Affinity/Taint 관점]

  +--------------------------------------------------------------+
  |                    Scheduling Cycle                          |
  |                                                              |
  |  Pod In   --->  QueueSort  --->  PreFilter  --->  Filter       |
  |                                          |                   |
  |                                          v                   |
  |                  +-------------------------------+            |
  |                  |   Filter (Node 후보군 축소)    |            |
  |                  |  +- NodeUnschedulable         |            |
  |                  |  +- NodeName                  |            |
  |                  |  +- NodeAffinity ⭐           |            |
  |                  |  +- NodePorts                 |            |
  |                  |  +- NodeResourcesFit          |            |
  |                  |  +- NodeSelector              |            |
  |                  |  +- TaintToleration ⭐        |            |
  |                  |  +- NodeAffinity during Exec  |            |
  |                  |  +- ...                       |            |
  |                  +-------------------------------+            |
  |                                          |                   |
  |                                          v                   |
  |                  +-------------------------------+            |
  |                  |   Reserve (자원 가용량 선점)    |            |
  |                  |  VolumeBinding, NodeResources  |            |
  |                  +-------------------------------+            |
  |                                          |                   |
  |                                          v                   |
  |                  +-------------------------------+            |
  |                  |   Permit (특수 게이팅)          |            |
  |                  +-------------------------------+            |
  |                                                              |
  |  - - - - - - - - - - - - - - - - - - - - - - - - - - -   |
  |                                                              |
  |                    Binding Cycle                             |
  |                                                              |
  |  PreBind  --->  Bind (apiserver patch)  --->  PostBind          |
  +--------------------------------------------------------------+

  ⭐ = 본 토픽 핵심 플러그인
```

### Taint와 Toleration의 매칭 메커니즘

Taint는 `key=value:Effect` 3-tuple로 구성되며, **3가지 Effect**가 있다:

| Effect | 동작 | 대표 사용 사례 |
|:---|:---|:---|
| `NoSchedule` | 해당 Taint를 tolerate하지 않는 파드는 신규 스케줄링 차단 (기존 파드는 유지) | 전용 노드, GPU 격리 |
| `PreferNoSchedule` | 가능하면 스케줄하지 않음(soft), 단 필터링은 하지 않음 | 베스트-에포트 회피 |
| `NoExecute` | tolerate하지 않는 기존 파드까지 **즉시 evict**(exclusionTimeout 적용) | 노드 컨디션 `NotReady`, 스팟 인터럽트, Drain |

매칭은 `key`(필수), `value`(옵션), `effect`(옵션) 3개 조합으로 `operator`(`Equal`/`Exists`)와 비교한다. `Exists`는 값 무시, `Equal`은 키·값·이펙트 완전 일치 요구.

```text
[Taint/Toleration 매칭 의사코드 - kube-scheduler TaintToleration 플러그인]

  for each node N with taints T₁..Tₖ:
    for each taint tᵢ in N:
      tolerationFound = false
      for each toleration tolⱼ in pod.spec.tolerations:
        if (tolⱼ.key == tᵢ.key || tolⱼ.key == "")          # "" == wildcard
           AND (tolⱼ.operator == "Exists"
                || (tolⱼ.operator == "Equal"
                    && tolⱼ.value == tᵢ.value))
           AND (tolⱼ.effect == tᵢ.effect || tolⱼ.effect == ""):
          tolerationFound = true
          break
        if !tolerationFound && tᵢ.effect in ["NoSchedule","NoExecute"]:
          node_excluded = true

      # PreferNoSchedule: count 후 Score 단계에서 페널티
      if tᵢ.effect == "PreferNoSchedule" && !tolerationFound:
        node.preferredScore -= 1

  if node_excluded: return Unschedulable
```

### Affinity 명세 상세 (YAML 스키마)

```yaml
# pod.spec.affinity 전체 구조
affinity:
  nodeAffinity:                       # ① 노드 속성 기반
    requiredDuringSchedulingIgnoredDuringExecution:   # hard - 스케줄 시점만 강제
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/egress-gateway
          operator: In                  # In, NotIn, Exists, DoesNotExist
          values: ["egress-gw-1"]
    requiredDuringSchedulingRequiredDuringExecution:   # hard - 실행 중에도 강제
      nodeSelectorTerms:
      - matchExpressions:
        - key: node.kubernetes.io/unreachable
          operator: Exists              # unreachable 노드에서도 떠 있게
    preferredDuringSchedulingIgnoredDuringExecution:   # soft - 가중치 기반 선호
    - weight: 80
      preference:
        matchExpressions:
        - key: topology.kubernetes.io/zone
            operator: In
            values: ["ap-northeast-2a"]   # 동일 AZ 우선

  podAffinity:                        # ② 다른 파드와의 동거
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: cache
          tier: redis
      topologyKey: kubernetes.io/hostname # 같은 호스트에 배치
      namespaceSelector: {}             # 모든 ns에서 검색

  podAntiAffinity:                    # ③ 다른 파드와의 분리 (HA 핵심)
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: api-gateway
        topologyKey: topology.kubernetes.io/zone
```

### 구성 요소 요약

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Node Affinity** | 파드를 특정 노드 라벨에 매칭 | `In/NotIn/Exists/DoesNotExist/Gt/Lt` 6종 연산자, `required`/`preferred` 2종 강도, `IgnoredDuringExecution`(v1 기본) vs `RequiredDuringExecution`(v1.24+ Stable) |
| **Pod Affinity** | 동일 토폴로지 도메인 내 다른 파드와 **동거** | `topologyKey`로 정의한 도메인(hostname/zone/region) 안에서 `labelSelector` 매칭 파드 존재 시 스케줄 허용, 캐시·사이드카·gRPC locality 활용 |
| **Pod Anti-Affinity** | 동일 도메인 내 동일 파드 **분산 배치** | `topologyKey` 기준 분산, ReplicaSet/StatefulSet과 결합해 **HA 클러스터 표준**, 단 도메인당 Pod 수 < required 수면 Pending 발생 가능 |
| **Taints** | 노드 측에서 파드 배치를 **거부/제약** 선언 | `key=value:Effect` 3-tuple, Effect 3종(`NoSchedule`/`PreferNoSchedule`/`NoExecute`), `kubectl taint node N1 key=val:NoSchedule` |
| **Tolerations** | 파드 측에서 특정 Taint를 **허용** 선언 | `key`/`operator`/`value`/`effect`/`tolerationSeconds` 필드, `tolerationSeconds`는 `NoExecute`에 한해 evict까지의 유예시간 |
| **NodeSelector** | (Legacy) 단순 라벨 equality 매칭 | `pod.spec.nodeSelector: {disktype: ssd}` 형태, `nodeAffinity`의 `required...IgnoredDuringExecution`과 동치 |
| **Topology Spread Constraints** | 도메인별 Pod 수 균등 분배 | `maxSkew`, `minDomains`, `topologyKey`, `whenUnsatisfiable`(`DoNotSchedule`/`ScheduleAnyway`), v1.19 GA |
| **Scheduling Framework 플러그인** | kube-scheduler 확장 지점 | PreFilter/Filter/PostFilter/Score/Reserve/Permit/PreBind/Bind 등 12개 확장점, 플러그인 체이닝 |

### 핵심 알고리즘: PreFilter 단계의 InterPodAffinity

`InterPodAffinity` 플러그인은 **이전 스케줄링 결과 캐시**(`PodAffinityMatcher`)를 활용한다. 신규 파드 P가 `podAffinity` 규칙을 가지면:
1. P와 라벨 셀렉터가 매칭되는 기존 파드 집합 `M`을 클러스터 전역에서 검색
2. `M`의 파드가 존재하는 노드 집합 `N_M`을 topologyKey 기준으로 도메인 매핑
3. `N_M`의 모든 노드를 "호환 노드 셋"으로 표시 -> Filter 단계에서 후보 보존
4. 반대로 `podAntiAffinity`는 `N_M`을 **제외** 후보로 처리

이때 **시간 복잡도**는 `O(P × N × |affinityTerms|)`이며, 대규모 클러스터(1만 노드+)에서는 `MatchInterPodAffinity` Score 플러그인이 **Hot Path**가 되어 `SchedulingThroughput`이 20~30% 저하될 수 있어, **NamespaceSelector** 범위 제한과 **PreferNoSchedule 가중치 튜닝**이 필수적이다.

- **📢 섹션 요약 비유**: **Taint**는 노드의 "이 방은 VIP 전용입니다" 팻말이고, **Toleration**은 파드의 "저는 VIP 패스를 가진 손님입니다" 카드이다. `NoExecute`는 "유예시간 30초 후 퇴장"이라는 시한부 퇴장 명령과 같고, **Affinity**는 "저는 창가가 좋은 친구와 같은 자리에 앉고 싶어요"라는 선호를 표현한다.

---

## Ⅲ. 비교 및 연결

### 주요 스케줄링 메커니즘 비교

| 구분 | `nodeSelector` | `nodeAffinity` | `podAffinity/Anti-Affinity` | `Taint/T
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 377 / 800

<- **이전**: [376. 쿠버네티스 오퍼레이터 커스텀 리소스 정의](/studynote/13_cloud_architecture/06_exam_summary/376_kubernetes_operator_custom_resource_definitio/)
**다음**: [378. 쿠버네티스 오토스케일링 HPA VPA CA](/studynote/13_cloud_architecture/06_exam_summary/378_kubernetes_autoscaling_hpa_vpa_cluster/) ->

---
