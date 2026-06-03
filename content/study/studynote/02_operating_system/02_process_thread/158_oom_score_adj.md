+++
weight = 158
title = "158. oom_score_adj - OOM 킬러 우선순위 조정"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: `oom_score_adj`는 Linux [[022_kernel_role|커널]]이 [[157_oom_killer|OOM]] ([[157_oom_killer|Out Of Memory]]) 상황에서 희생 프로세스를 고를 때, 기본 위험도(`oom_score`)에 [[164_policy|정책]]적 [[267_weight_bias_activation|가중치]]를 더하거나 빼는 조정 손잡이다.
> 2. **가치**: [[002_database_definition|데이터베이스]], `sshd`, `kubelet` 같은 핵심 프로세스는 덜 죽게 하고, 배치 작업이나 실험성 워크로드는 먼저 정리되게 만들어 시스템 전체 생존 확률을 높인다.
> 3. **판단 포인트**: `oom_score_adj`는 메모리를 늘려 주는 기능이 아니라 “누가 먼저 희생될지”를 정하는 [[164_policy|정책]]이므로, cgroup (Control Group) 제한, 재시작 [[164_policy|정책]], [[612_memory_leak_detection|메모리 누수]] 대응과 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

`oom_score_adj`는 Linux가 메모리 부족으로 [[157_oom_killer|OOM]] Killer를 발동할 때 프로세스 중요도를 관리자가 직접 보정하는 인터페이스다. [[022_kernel_role|커널]]은 기본적으로 메모리를 많이 쓰는 프로세스를 위험 후보로 보지만, 실제 운영에서는 메모리 사용량이 많아도 반드시 살아 있어야 하는 프로세스가 있다. 이런 현실을 반영하기 위해 `/proc/<pid>/oom_score_adj`에 `-1000`부터 `+1000` 사이 값을 [[009_config|설정]]해 종료 우선순위를 조정한다.

이 기능이 필요한 이유는 “메모리를 많이 쓴다”와 “먼저 죽어도 된다”가 항상 같지 않기 때문이다. 예를 들어 [[002_database_definition|데이터베이스]]나 노드 관리 에이전트는 메모리를 많이 쓰더라도 함부로 죽이면 전체 [[090_service_kubernetes_network_load_balancing|서비스]]가 더 크게 흔들린다. 반대로 임시 배치, 캐시 워머, 분석 작업은 먼저 종료되어도 시스템이 버틸 수 있다. `oom_score_adj`는 바로 이런 운영 우선순위를 [[022_kernel_role|커널]] 판단에 주입하는 도구다.

- **📢 섹션 요약 비유**: `oom_score_adj`는 비상 탈출 명단에 붙이는 우선순위 스티커와 같다. 모두를 동시에 살릴 수 없을 때, 누가 마지막까지 남아야 하는지 미리 표시해 두는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[157_oom_killer|OOM]] 상황이 오면 [[022_kernel_role|커널]]은 [[286_page_frame|페이지]] 회수, 메모리 [[347_compaction|압축]], 스왑 같은 완화 절차를 먼저 시도한다. 그래도 할당 실패가 계속되면 [[157_oom_killer|OOM]] Killer가 동작하고, 이때 [[022_kernel_role|커널]]이 계산한 기본 위험도인 `oom_score`와 관리자가 준 `oom_score_adj`가 함께 반영된다. 즉 `oom_score`가 현재 상태를 보여 주는 계기판이라면, `oom_score_adj`는 운영 [[164_policy|정책]]을 반영하는 조정 손잡이다.

### 값의 범위와 의미

| 값 범위 | 의미 | 운영 해석 |
| :--- | :--- | :--- |
| `-1000` | 사실상 [[157_oom_killer|OOM]] 면제 | 정말 반드시 살아야 할 프로세스에만 제한적으로 사용 |
| `-999 ~ -1` | 종료 가능성 낮춤 | 중요하지만 절대 면제는 아닌 프로세스 [[571_protection_vs_security|보호]] |
| `0` | 기본값 | [[022_kernel_role|커널]] 계산 결과를 그대로 따름 |
| `1 ~ 999` | 종료 가능성 높임 | 먼저 정리해도 되는 작업성 프로세스 지정 |
| `1000` | 최우선 희생 후보 | 실험성/임시성 워크로드에만 신중히 사용 |

아래 그림은 [[157_oom_killer|OOM]] 판단에 `oom_score_adj`가 개입하는 지점을 요약한다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                 OOM selection path with policy override                    │
├────────────────────────────────────────────────────────────────────────────┤
│ memory pressure                                                            │
│      │                                                                     │
│      ├── reclaim / compact / swap try                                      │
│      └── still allocation failure                                          │
│              ▼                                                             │
│      kernel badness heuristic ──▶ oom_score                                │
│                                   +                                        │
│                          admin policy ──▶ oom_score_adj                    │
│                                   │                                        │
│                                   ▼                                        │
│                        victim chosen and SIGKILL issued                     │
└────────────────────────────────────────────────────────────────────────────┘
```

실무적으로 기억할 점은 세 가지다. 첫째, `oom_score_adj`는 프로세스 단위 값이며 자식 프로세스에 상속될 수 있어 [[090_service_kubernetes_network_load_balancing|서비스]] 트리 전체에 영향을 준다. 둘째, 직접 `/proc`에 쓴 값은 프로세스가 재시작되면 사라지므로 지속 [[164_policy|정책]]은 `systemd`나 오케스트레이터에서 관리하는 편이 낫다. 셋째, `-1000`은 강력하지만 남용하면 [[022_kernel_role|커널]]이 실제 위기 때 선택할 후보를 잃어 더 큰 장애를 만들 수 있다.

- **📢 섹션 요약 비유**: 기본 위험도 계산이 시험 점수라면, `oom_score_adj`는 교사가 붙이는 가감점이다. 같은 점수를 받아도 중요한 역할을 맡은 학생은 덜 탈락하게 만들 수 있다.

---

## Ⅲ. 비교 및 연결

`oom_score_adj`를 제대로 이해하려면 비슷해 보이는 다른 메커니즘과 구분해야 한다.

| 항목 | 역할 | 무엇을 바꾸는가 | 한계 |
| :--- | :--- | :--- | :--- |
| `oom_score` | 현재 위험도 지표 | [[022_kernel_role|커널]]이 계산한 [[157_oom_killer|OOM]] 후보 점수 | 관리자가 직접 [[164_policy|정책]]을 담기 어려움 |
| `oom_score_adj` | [[164_policy|정책]] [[267_weight_bias_activation|가중치]] | 종료 우선순위 | 메모리 총량 자체는 늘리지 못함 |
| `memory.max` / cgroup 제한 | 격리 한도 | 워크로드별 사용 가능 메모리 상한 | 잘못 잡으면 cgroup 내부 OOM이 자주 발생 |
| `systemd` `OOMScoreAdjust=` | [[090_service_kubernetes_network_load_balancing|서비스]] 단위 지속 [[009_config|설정]] | 재시작 후에도 [[164_policy|정책]] 유지 | [[090_service_kubernetes_network_load_balancing|서비스]] 경계 밖까지 자동 해결되진 않음 |
| [[205_kubernetes_container_orchestration|Kubernetes]] [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] ([[388_qos_quality_of_service_best_effort_intserv_diffserv|Quality of Service]]) | [[561_container_based_deployment|컨테이너]] 계층 [[164_policy|정책]] | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 중요도에 따른 자동 보정 | 애플리케이션 누수 자체는 해결하지 못함 |

즉 `oom_score_adj`는 **[[164_policy|정책]] [[130_signal|신호]]**이고, cgroup 제한은 **격리 장치**다. 둘은 경쟁 관계가 아니라 보완 관계다. 예를 들어 Kubernetes는 Guaranteed, Burstable, BestEffort [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 클래스에 따라 `oom_score_adj`를 자동 부여해 노드 [[157_oom_killer|OOM]] 시 종료 순서를 정리한다. 하지만 [[561_container_based_deployment|컨테이너]]가 메모리를 무한정 먹지 못하게 막는 일은 여전히 `requests/limits`와 cgroup이 맡는다.

- **📢 섹션 요약 비유**: `oom_score_adj`가 좌석 우선순위표라면, cgroup은 아예 객실 칸막이다. 먼저 내릴 사람을 정하는 일과, 방마다 정원을 정하는 일은 서로 다른 관리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

운영 현장에서는 `oom_score_adj`를 “중요 [[090_service_kubernetes_network_load_balancing|서비스]] [[571_protection_vs_security|보호]] [[164_policy|정책]]”으로 설계한다. 예를 들어 `systemd` [[090_service_kubernetes_network_load_balancing|서비스]]에서는 `OOMScoreAdjust=-500`처럼 명시해 [[002_database_definition|데이터베이스]]와 노드 에이전트를 [[571_protection_vs_security|보호]]하고, 실험성 워커나 배치 잡에는 양수 값을 주어 먼저 정리되도록 한다. [[561_container_based_deployment|컨테이너]] 환경에서는 단일 프로세스보다 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 전체 중요도, 재시작 [[164_policy|정책]], 노드 메모리 압박 [[130_signal|신호]]까지 함께 봐야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. **정말 반드시 살아야 하는 프로세스만 음수로 [[571_protection_vs_security|보호]]했는가?** 핵심 제어면만 선별해야 한다.
2. **`-1000`을 남발하지 않았는가?** 면제 대상이 많을수록 [[022_kernel_role|커널]] 선택 폭이 줄어든다.
3. **재시작 후에도 [[164_policy|정책]]이 유지되는가?** `/proc` 직접 수정만으로는 지속되지 않는다.
4. **[[612_memory_leak_detection|메모리 누수]]와 상한 [[009_config|설정]]을 같이 관리하는가?** `oom_score_adj`만으로 근본 원인은 해결되지 않는다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 중요 [[090_service_kubernetes_network_load_balancing|서비스]]에 일괄적으로 `-1000`을 주는 경우
- 애플리케이션 [[612_memory_leak_detection|메모리 누수]]는 방치한 채 [[157_oom_killer|OOM]] 점수만 조정하는 경우
- Kubernetes나 `systemd` 기본 [[164_policy|정책]]을 이해하지 않고 수동 값만 덮어쓰는 경우

- **📢 섹션 요약 비유**: `oom_score_adj` [[009_config|설정]]은 병원 응급실의 중증도 분류와 같다. 누구를 먼저 돌볼지 정하는 것은 중요하지만, 병실 수와 의료 장비 부족 문제 자체를 없애 주지는 못한다.

---

## Ⅴ. 기대효과 및 결론

`oom_score_adj`를 올바르게 쓰면 메모리 위기가 왔을 때 장애 반경을 줄일 수 있다. 즉 모든 프로세스를 무차별적으로 위험에 노출하는 대신, 핵심 제어 프로세스는 살리고 비핵심 작업을 먼저 정리하게 만들어 노드 전체 다운 가능성을 낮춘다. 특히 `systemd`, [[205_kubernetes_container_orchestration|Kubernetes]], 재시작 [[164_policy|정책]]과 결합하면 “누가 죽고 누가 복구되는가”를 훨씬 예측 가능하게 만든다.

하지만 이 값은 어디까지나 최후의 순간을 위한 [[164_policy|정책]]이다. 메모리 사용량 예측, 상한 [[009_config|설정]], 캐시 [[268_strategy_pattern|전략]], 누수 제거, PSI (Pressure Stall Information) 기반 조기 경보가 함께 있어야 진짜 운영 품질이 올라간다. 따라서 `oom_score_adj`는 “메모리 문제 해결책”이 아니라 **메모리 재난 시 생존 순서를 정하는 운영 레버**로 기억해야 한다.

- **📢 섹션 요약 비유**: `oom_score_adj`는 배가 침수될 때 어떤 짐을 먼저 버릴지 정해 둔 목록과 같다. 배를 더 크게 만들어 주지는 않지만, 침몰 직전에 무엇을 지켜야 할지는 분명하게 해 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[425_oom_killer_score|OOM Killer]] | 메모리 회수 실패 후 희생 프로세스를 선택하는 최종 메커니즘 |
| `oom_score` | [[022_kernel_role|커널]]이 계산하는 현재 프로세스 위험도 |
| cgroup (Control Group) | 워크로드별 메모리 격리와 제한을 담당 |
| `systemd` `OOMScoreAdjust=` | [[090_service_kubernetes_network_load_balancing|서비스]] 단위의 지속적 `oom_score_adj` [[009_config|설정]] 방법 |
| [[205_kubernetes_container_orchestration|Kubernetes]] [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] ([[388_qos_quality_of_service_best_effort_intserv_diffserv|Quality of Service]]) | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 중요도에 따라 자동 우선순위를 조정하는 상위 [[164_policy|정책]] |
| PSI (Pressure Stall Information) | [[157_oom_killer|OOM]] 이전의 메모리 압박을 조기 감지하는 [[130_signal|신호]] |

### 📈 관련 키워드 및 발전 흐름도

```text
메모리 압박
    │
    ▼
페이지 회수 · 스왑 · 압축 시도
    │
    ▼
OOM Killer 진입
    │
    ▼
oom_score + oom_score_adj
    │
    ▼
cgroup 정책 · systemd · Kubernetes QoS와 결합한 생존 우선순위 설계
```

이 흐름은 `oom_score_adj`가 단독 기능이 아니라, 메모리 압박 감지에서 희생자 선정과 상위 [[073_container_orchestration_tools|오케스트레이션]] [[164_policy|정책]]으로 이어지는 운영 체계의 한 요소임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 방이 너무 꽉 차면, 누군가는 밖으로 나가야 해서 [[157_oom_killer|OOM]] Killer가 누굴 먼저 내보낼지 골라요.
2. `oom_score_adj`는 “이 친구는 중요해요” 또는 “이 친구는 먼저 나가도 돼요”라고 붙이는 스티커예요.
3. 하지만 방이 너무 좁은 문제까지 없어지는 건 아니어서, 원래부터 방 크기와 사람 수를 잘 맞춰야 해요.

