+++
title = "157. OOM (Out Of Memory) Killer 프로세스 종료 정책"
date = 2026-03-22

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OOM (Out Of Memory) Killer는 Linux [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 메모리 회수와 스왑 (Swap)까지 모두 실패했을 때, 시스템 전체 정지를 막기 위해 일부 프로세스를 강제로 종료하는 최후의 안전장치다.
> 2. **가치**: 모든 프로세스를 살리려다 시스템이 멎는 것보다, 덜 중요한 프로세스를 희생해 핵심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 생존 가능성을 높이는 것이 OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)의 핵심 가치다.
> 3. **판단 포인트**: 중요한 것은 “OOM을 없애는 것”이 아니라, 어떤 상황에서 누가 먼저 죽어야 하는지와 cgroup (Control Group)·`oom_score_adj`·재시작 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 어떻게 설계할 것인지다.

---

## Ⅰ. 개요 및 필요성

OOM Killer는 시스템이 더 이상 만족할 메모리 할당을 찾지 못하는 순간 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 발동하는 비상 대응 메커니즘이다. Linux는 먼저 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시를 회수하고, 메모리 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)과 스왑을 시도하며, 그래도 실패할 때 마지막 수단으로 희생 프로세스를 선택한다. 이런 단계가 없으면 시스템은 심한 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) 상태에 빠지거나, 중요한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 작업이 진행되지 못해 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 사실상 멈출 수 있다.

특히 서버 환경에서는 “프로세스 하나의 종료”와 “노드 전체 불능” 중 무엇이 더 작은 손실인지 판단해야 한다. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/), sshd 같은 핵심 프로세스를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하고, 배치 작업이나 메모리 폭주 애플리케이션을 먼저 정리하도록 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 잡는 이유가 여기에 있다.

- **📢 섹션 요약 비유**: OOM Killer는 배가 가라앉을 때 모든 짐을 그대로 붙잡지 않고, 배를 살리기 위해 일부 화물을 먼저 버리는 선장의 마지막 선택과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OOM은 단순히 “메모리가 가득 찼다”는 숫자 하나로 발생하지 않는다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 할당 요청이 들어올 때 가용 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/), 회수 가능한 캐시, 스왑 가능 여부, 메모리 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/), cgroup 한계까지 함께 본다. 그 결과 회수 경로가 막혔다고 판단되면 전역 OOM 또는 메모리 cgroup OOM으로 진입한다.

### OOM 진입 전 단계

| 단계 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 동작 | 의미 |
| :--- | :--- | :--- |
| 메모리 압박 | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시 회수, [슬랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) 축소 | 재사용 가능한 메모리 확보 시도 |
| 직접 회수 | 할당 요청 프로세스가 직접 회수 수행 | 지연이 커지고 응답성이 떨어지기 시작 |
| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)/스왑 | 연속 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 확보, 익명 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [스왑 아웃](/knowledge-base/studynote/02_operating_system/06_memory_management/336_swap_out_in/) | [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)와 부족 상태를 완화 |
| OOM 판단 | 더 이상 회수 효과가 없다고 판단 | 희생 프로세스 선정 단계로 이동 |

아래 그림은 OOM 발생 경로를 단계별로 요약한 것이다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    memory allocation failure path                         │
├────────────────────────────────────────────────────────────────────────────┤
│ alloc request                                                             │
│      │                                                                     │
│      ├── reclaim page cache / shrink slabs                                │
│      ├── compact memory / swap out pages                                  │
│      └── still cannot satisfy request                                     │
│              ▼                                                            │
│      OOM context decided                                                  │
│      ├── global OOM  : system-wide victim selection                       │
│      └── memcg OOM   : action inside one memory cgroup                    │
│              ▼                                                            │
│ badness heuristic + oom_score_adj  ──▶  SIGKILL  ──▶  memory released │
└────────────────────────────────────────────────────────────────────────────┘
```

희생자 선정에는 메모리 사용량, 프로세스 특성, `oom_score_adj` 값 등이 반영된다. 사용자 공간에서는 `/proc/<pid>/oom_score`로 현재 위험도를 확인할 수 있고, `/proc/<pid>/oom_score_adj`로 중요도를 조정할 수 있다. 여기서 `-1000`은 사실상 면제에 가깝고, `+1000`은 가장 먼저 종료될 가능성을 크게 높인다.

- **📢 섹션 요약 비유**: OOM 처리 흐름은 응급실 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계와 비슷하다. 먼저 약으로 버텨 보고, 안 되면 수술을 결정하며, 마지막에는 누구를 먼저 치료하거나 포기할지 냉정하게 우선순위를 정한다.

---

## Ⅲ. 비교 및 연결

OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 이해할 때 가장 중요한 경계는 <strong>전역 OOM</strong>과 <strong>메모리 cgroup OOM</strong>의 차이다.

| 구분 | 전역 OOM | 메모리 cgroup OOM |
| :--- | :--- | :--- |
| 발생 범위 | 시스템 전체 메모리 부족 | 특정 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)/[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 그룹 한도 초과 |
| 희생 대상 | [전체 프로세스](/knowledge-base/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/) 집합 중 선정 | 해당 cgroup 내부 프로세스 중심 |
| 운영 의미 | 노드 생존 자체가 위협받는 상태 | 격리된 워크로드만 정리 가능 |
| 주 사용 환경 | 일반 서버, 심각한 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), [멀티테넌트](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/) 환경 |

또한 `oom_score`와 `oom_score_adj`도 역할이 다르다. `oom_score`는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 계산한 현재 위험도이고, `oom_score_adj`는 관리자가 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)적으로 중요도를 가감하는 손잡이다. 여기에 PSI (Pressure Stall Information), `systemd-oomd`, [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) ([Quality of Service](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)) 클래스까지 연결되면, 현대 운영체제의 메모리 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)는 단순 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능을 넘어 <strong>예방형 제어</strong>로 확장된다.

즉 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) OOM Killer는 마지막 단계이고, 실제 운영 품질은 그 이전에 cgroup 제한, 애플리케이션 메모리 상한, 재시작 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 관측성 체계를 얼마나 잘 갖췄는지에 달려 있다.

- **📢 섹션 요약 비유**: 전역 OOM은 건물 전체 정전이고, cgroup OOM은 한 층의 분전함이 차단되는 상황과 같다. 어디서 차단되느냐에 따라 피해 범위가 완전히 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 OOM Killer를 막연히 두려워하기보다, “어떤 프로세스를 반드시 살릴 것인가”를 먼저 정해야 한다. 예를 들어 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 노드 에이전트는 `oom_score_adj`를 낮추고, 배치 작업·캐시 워머·실험성 워크로드는 높게 두는 식으로 우선순위를 분리한다. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서는 `memory.max`, `memory.high`, 요청/제한값, 재시작 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계해야 한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong>핵심 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>: sshd, systemd, [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/), 주요 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소는 낮은 OOM 점수 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 부여했는가?
2. **워크로드 격리**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)나 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별로 메모리 상한과 cgroup 제한이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 있는가?
3. **사전 탐지**: PSI, RSS (Resident Set Size), [page fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/), swap in/out을 모니터링하고 있는가?
4. <strong>사후 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong>: 종료된 프로세스를 자동 재시작하고 원인을 추적할 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·알림 체계가 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 여러 핵심 프로세스에 모두 `oom_score_adj = -1000`을 줘서 실제 위기 때 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 선택지를 지나치게 줄이는 경우
- `oom_kill_disable` 또는 과도한 스왑 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 문제를 숨긴 뒤, 더 큰 지연과 전체 장애를 초래하는 경우
- 애플리케이션 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/)는 방치한 채 [OOM Killer](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)만 만지는 경우

- **📢 섹션 요약 비유**: OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 소방 훈련과 같다. 불이 난 뒤 누구부터 구할지 정하는 것도 필요하지만, 애초에 방화 구획과 경보 시스템을 갖춰 두는 것이 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 장애를 완전히 없애 주지 않지만, 장애의 <strong>폭발 반경</strong>을 크게 줄여 준다. 즉 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/)나 순간 폭주가 발생해도 핵심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 노드 전체를 지키고, 피해를 특정 프로세스나 특정 cgroup 안에 가두는 효과가 있다. 반대로 OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 없이 용량만 늘리면 비용은 커지는데 장애 양상은 여전히 예측하기 어렵다.

다만 OOM Killer는 어디까지나 최후 수단이다. 장기적으로는 메모리 사용량 예측, 상한 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 캐시 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), `systemd-oomd` 같은 사용자 공간 조정자, 그리고 애플리케이션 수준의 누수 제거가 함께 가야 한다. 결국 OOM은 “죽이는 기능”이 아니라 <strong>시스템이 끝까지 살아남도록 손실을 통제하는 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>으로 이해해야 한다.

- **📢 섹션 요약 비유**: 좋은 OOM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 자동차의 에어백과 같다. 에어백은 사고를 없애 주지 않지만, 충돌이 일어났을 때 사람이 치명상을 입지 않도록 피해를 줄여 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| `oom_score` | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 산정한 현재 프로세스의 OOM 위험도 |
| `oom_score_adj` | 관리자가 중요도를 가감하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 값 |
| cgroup (Control Group) | 워크로드 단위 메모리 제한과 OOM 격리를 담당 |
| RSS (Resident Set Size) | 실제 상주 메모리 사용량을 보는 핵심 지표 |
| PSI (Pressure Stall Information) | 메모리 압박을 OOM 이전에 감지하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |
| `systemd-oomd` | 사용자 공간에서 선제적으로 프로세스를 정리하는 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
메모리 압박
    │
    ▼
페이지 회수 · 스왑 · 압축
    │
    ▼
전역 OOM / 메모리 cgroup OOM
    │
    ▼
oom_score · oom_score_adj
    │
    ▼
SIGKILL · 자동 재시작 · PSI 기반 선제 대응
```

이 흐름은 OOM이 단발성 종료 이벤트가 아니라, 메모리 압박 감지에서 격리·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·예방으로 이어지는 운영 체계임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 메모리가 꽉 차서 모두가 숨을 못 쉬면, OOM Killer가 가장 덜 중요한 프로그램을 먼저 꺼요.
2. 어떤 프로그램은 “중요해요” 표시를 붙여서 덜 꺼지게 만들 수 있어요.
3. 하지만 진짜 좋은 방법은 방이 꽉 차기 전에 사람 수를 조절하고, 빨리 치우는 규칙을 미리 만드는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 800

← **이전**: [156. 환경 변수 (Environment Variables) 상속](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)
**다음**: [158. oom_score_adj - OOM 킬러 우선순위 조정](/knowledge-base/studynote/02_operating_system/02_process_thread/158_oom_score_adj/) →

---
