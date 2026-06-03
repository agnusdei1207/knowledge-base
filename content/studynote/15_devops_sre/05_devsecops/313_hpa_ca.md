+++
title = "HPA CA Autoscaling"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ([Horizontal Pod Autoscaler](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/))는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 수를 늘리고, [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Cluster Autoscaler)는 노드 수를 늘려 이중 레이어 오토스케일링을 구성한다.
> - HPA는 CPU/메모리·[커스텀 메트릭](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/189_custom_metrics/)을 기준으로 ReplicaSet을 조정하고, CA는 Pending [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 감지해 클라우드 노드를 추가한다.
> - [VPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) ([Vertical Pod Autoscaler](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/))는 리소스 Request·Limit 자체를 조정하는 세 번째 차원이다.

---

## Ⅰ. [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ([Horizontal Pod Autoscaler](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)) 원리

HPA는 `metrics-server`에서 CPU/메모리 사용률을 주기적으로 수집해 목표 비율에 맞게 레플리카 수를 조정한다.

```
replicas = ceil(currentReplicas × currentMetricValue / desiredMetricValue)
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HPA 제어 루프</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">metrics-server ──▶ HPA Controller ──▶ ReplicaSet</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(CPU 80%)</div><div class="kb-diagram-cell">(3 → 5)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">60% 목표 초과</div></div>
</div>
</div>



> 📢 **Ⅰ 섹션 요약 비유**
> HPA는 계산원이 부족하면 더 불러오는 매장 관리자다 — 줄이 길어지면 창구를 늘린다.

---

## Ⅱ. [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Cluster Autoscaler) 원리

CA는 Pending 상태인 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 감지해 클라우드 Node Group에 노드를 추가하거나, 유휴 노드를 종료한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CA 동작 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Pod Pending ──▶ CA 감지 ──▶ Cloud API 호출</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(노드 +1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">──▶ 노드 등록 ──▶ Pod 배치</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Idle Node ──▶ CA 감지 ──▶ 파드 이동 ──▶ 삭제</div></div>
</div>
</div>



조건:
- 추가: [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 불가 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 존재
- 삭제: 노드 사용률 50% 미만 + [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 안전 이동 가능

> 📢 **Ⅱ 섹션 요약 비유**
> CA는 레스토랑에서 손님이 넘치면 테이블을 추가하고, 손님이 없으면 빈 테이블을 치우는 매니저다.

---

## Ⅲ. [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) + [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 연동 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">트래픽 급증</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">HPA: 파드 수 증가 (Pending 발생 가능)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CA: Pending 파드 감지 → 노드 추가</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파드 정상 배치 → 서비스 안정화</div>
</div>
</div>



**스케일 다운 안전 메커니즘**:
- [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/): `--horizontal-pod-autoscaler-downscale-stabilization`(기본 5분)
- [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/): `scale-down-unneeded-time`(기본 10분)

> 📢 **Ⅲ 섹션 요약 비유**
> HPA가 직원을 더 부르면 CA가 그 직원들이 앉을 책상을 추가로 주문하는 구조다.

---

## Ⅳ. [VPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) ([Vertical Pod Autoscaler](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/))

VPA는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 CPU/메모리 Request·Limit을 자동 조정한다.

| 항목        | [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)                    | [VPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/)                    |
|-------------|------------------------|------------------------|
| 조정 대상   | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 수(레플리카)       | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 리소스 Request     |
| 적합한 앱   | 수평 확장 가능한 웹앱  | DB·[싱글톤](/knowledge-base/studynote/04_software_engineering/04_testing_quality/253_singleton_pattern_single_instance/)처럼 확장 어려운 앱 |
| 병행 사용   | VPA와 동시 권장 안 됨  | -                      |

> 📢 **Ⅳ 섹션 요약 비유**
> HPA가 배달 기사 수를 늘린다면, VPA는 각 기사에게 더 큰 가방을 준다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소             | 역할                                    |
|-----------------------|-----------------------------------------|
| [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)                   | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 수 자동 조정 (수평 스케일)          |
| [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)                    | 노드 수 자동 조정 (클러스터 스케일)      |
| [VPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/)                   | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 리소스 크기 자동 조정 (수직 스케일) |
| [metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)-server        | CPU/메모리 사용량 수집 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)          |
| Node Group            | CA가 조정하는 클라우드 노드 풀           |
| KEDA                  | 이벤트 기반 오토스케일러([HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) 확장)       |

### 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Autoscaling</div>
<div class="kb-diagram-tree-item" style="--depth:2">HPA → 파드 수 조정 (metrics-server 기반)</div>
<div class="kb-diagram-tree-item" style="--depth:2">CA → 노드 수 조정 (Pending 파드 감지)</div>
<div class="kb-diagram-tree-item" style="--depth:2">VPA → 리소스 크기 조정</div>
<div class="kb-diagram-tree-item" style="--depth:2">KEDA → 이벤트/큐 기반 고급 오토스케일링</div>
</div>
</div>



> 🧒 **어린이 비유**
> HPA는 바쁠 때 친구를 더 부르는 것, CA는 그 친구들이 앉을 의자를 구해오는 것, VPA는 한 친구에게 더 힘센 도구를 주는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 313 / 373

← **이전**: [Taint and Toleration](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/312_process/)
**다음**: [PV PVC PersistentVolume](/knowledge-base/studynote/15_devops_sre/05_devsecops/314_pv_pvc/) →

---
