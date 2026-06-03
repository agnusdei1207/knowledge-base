+++
weight = 147
title = "147. eBPF (Extended Berkeley Packet Filter) - 커널 레벨 샌드박스 관측 기술"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[615_ebpf|eBPF]](Extended [[069_ebpf|Berkeley Packet Filter]])는 리눅스 [[022_kernel_role|커널]] 소스코드를 수정하거나 [[022_kernel_role|커널]] [[192_module_independence|모듈]]을 로드하지 않고도, **[[022_kernel_role|커널]] 공간([[022_kernel_role|Kernel]] Space)에 안전하게 샌드박스화된 프로그램을 동적으로 삽입해 네트워크 트래픽·시스템 콜·[[294_function_calling_tool_use|함수 호출]] 이벤트를 오버헤드 없이 관측·필터링**하는 혁신적 리눅스 [[022_kernel_role|커널]] 기술이다.
> 2. **가치**: [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]([[830_sidecar_proxy_architecture_envoy_decoupling|Sidecar Proxy]]) 없이도 네트워크 관측성([[642_observability_telemetry|Observability]])을 구현하고, 시스템 콜 수준의 [[007_security_policy|보안 정책]]을 런타임에 적용하며, [[670_xdp|XDP]]([[661_ebpf_xdp_express_data_path|Express Data Path]])로 [[022_kernel_role|커널]]에서 직접 패킷을 처리해 DDoS 방어·로드밸런싱이 가능하다.
> 3. **판단 포인트**: eBPF는 [[022_kernel_role|커널]]을 건드리지 않는 안전한 실행 환경(Verifier + [[568_jit_access|JIT]] 컴파일)이라는 점이 핵심이며, [[825_cilium_ebpf_kubernetes_networking_security|Cilium]]·Falco·BCC·bpftrace 등 [[531_cloud_native_architecture|클라우드 네이티브]] 인프라 도구의 핵심 엔진으로 자리잡았다.

---

## Ⅰ. 개요 및 필요성

전통적으로 [[022_kernel_role|커널]]의 동작을 관측하거나 수정하려면 [[022_kernel_role|커널]] [[192_module_independence|모듈]]([[022_kernel_role|Kernel]] [[192_module_independence|Module]])을 작성해 로드하거나, [[022_kernel_role|커널]] 소스코드를 패치하고 재컴파일해야 했다. 두 방법 모두 버그 하나로 시스템 전체가 패닉([[036_kernel_panic|Kernel Panic]])에 빠질 수 있는 위험이 있었다.

eBPF는 이 문제를 해결한다:
- [[022_kernel_role|커널]] 공간에서 실행되지만 **[[395_verification_process_review|검증]]기(Verifier)** 가 무한 루프·메모리 오류를 사전 차단
- **[[568_jit_access|JIT]]([[568_jit_access|Just-In-Time]]) 컴파일**로 인터프리터 오버헤드 없이 네이티브 속도 실행
- **특정 이벤트(tracepoint, kprobe, 네트워크 패킷)** 에 [[615_ebpf|eBPF]] 프로그램을 Hook으로 부착

원래 [[069_ebpf|BPF]]([[069_ebpf|Berkeley Packet Filter]])는 tcpdump 같은 도구가 [[022_kernel_role|커널]] 레벨에서 패킷을 필터링하기 위해 1992년 개발됐다. 2014년 리눅스 3.18에서 확장(extended)되어 네트워크 이외 [[022_kernel_role|커널]] 이벤트 전반으로 적용 범위가 폭발적으로 확대됐다.

**[[615_ebpf|eBPF]] 없으면 발생하는 문제**:
- 관측성([[642_observability_telemetry|Observability]]): 모든 Pod에 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]](Envoy) 주입 → CPU·메모리 오버헤드
- 보안: 런타임 시스템 콜 감시 불가 → 악성 코드 탐지 [[015_지연_데이터_관점|지연]]
- [[282_performance_tactics|성능]]: 패킷 처리를 유저스페이스에서 하면 [[022_kernel_role|커널]]-유저 전환 비용 발생

- **📢 섹션 요약 비유**: eBPF는 **'운영 중인 건물의 설계도를 바꾸지 않고, 특수 투명 카메라를 각 방에 설치해 실시간으로 [[229_monitor|모니터]]링하는 기술'** 입니다. 건물([[022_kernel_role|커널]])을 허물거나 재건축(재컴파일)하지 않고, 관찰 도구만 조용히 설치해 모든 활동을 포착합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [[615_ebpf|eBPF]] 실행 흐름

```text
eBPF 프로그램 실행 파이프라인

  개발자 (User Space)
  ┌──────────────────────────────────────────────────────────┐
  │  eBPF 프로그램 작성 (C 코드 또는 bpftrace 스크립트)        │
  │  └─► LLVM/Clang으로 eBPF 바이트코드 컴파일                │
  └──────────────────────────────────────────────────────────┘
                    │ syscall(bpf)
  커널 (Kernel Space)
  ┌──────────────────────────────────────────────────────────┐
  │  ① Verifier (검증기)                                     │
  │     · 무한 루프 없음 확인 (DAG 분석)                       │
  │     · 메모리 경계 검사                                    │
  │     · 권한 검사                                          │
  │                    │ 통과                                │
  │  ② JIT 컴파일러 → 네이티브 머신 코드 변환                  │
  │                    │                                    │
  │  ③ Hook 포인트에 부착                                     │
  │     · kprobe/kretprobe (커널 함수 진입/반환)               │
  │     · tracepoint (정적 추적 포인트)                       │
  │     · XDP (네트워크 드라이버 레벨 패킷 처리)               │
  │     · tc (트래픽 제어 훅)                                 │
  │     · uprobe (유저스페이스 함수 추적)                      │
  │                    │                                    │
  │  ④ 이벤트 발생 시 eBPF 프로그램 실행 → Maps에 데이터 저장  │
  └──────────────────────────────────────────────────────────┘
                    │ perf_event / ring buffer
  User Space 분석 도구 (BCC, bpftrace, Cilium)
```

### 2. [[615_ebpf|eBPF]] Maps — [[022_kernel_role|커널]]-유저 [[386_data_clean_room_sharing|데이터 공유]]

[[615_ebpf|eBPF]] 프로그램은 **Maps**라는 공유 자료구조를 통해 [[022_kernel_role|커널]]과 유저스페이스 간 [[001_dikw_pyramid|데이터]]를 교환한다.

| Map 타입 | 설명 | 용도 |
|:---|:---|:---|
| Hash Map | [[036_key_value|키-값 저장소]] | 연결 추적, 통계 |
| [[055_array|Array]] | [[154_database_index_b_tree_search_optimization|인덱스]] 기반 | 규칙 테이블 |
| Ring Buffer | 고속 이벤트 스트림 | [[568_logs_distributed_logging_elk_fluentd|로그]]·이벤트 수집 |
| Perf Buffer | CPU별 이벤트 버퍼 | 고성능 이벤트 수집 |

### 3. 주요 활용 분야

```text
eBPF 활용 영역

  ┌──────────────────────────────────────────────────────────┐
  │  네트워킹                                                 │
  │  XDP ─ 커널 NIC 드라이버 레벨에서 패킷 드롭/포워딩         │
  │         DDoS 방어, 로드밸런싱 (Katran, Cilium LB)          │
  ├──────────────────────────────────────────────────────────┤
  │  관측성 (Observability)                                   │
  │  kprobe/tracepoint ─ 시스템 콜, 레이턴시, CPU 프로파일링   │
  │  사이드카 없는 서비스 메시 (Cilium, Hubble)                │
  ├──────────────────────────────────────────────────────────┤
  │  보안                                                    │
  │  시스템 콜 감시 ─ 비정상 행동 탐지 (Falco, Tetragon)       │
  │  런타임 정책 적용 (Seccomp BPF)                           │
  └──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[615_ebpf|eBPF]] Maps는 **'[[022_kernel_role|커널]]과 관리자 사이의 공용 화이트보드'** 입니다. [[615_ebpf|eBPF]] 프로그램이 [[022_kernel_role|커널]]에서 발견한 정보(패킷 수, [[015_지연_데이터_관점|지연]]시간)를 화이트보드(Map)에 적으면, 관리자 도구가 화이트보드를 읽어 대시보드에 표시합니다.

---

## Ⅲ. 비교 및 연결

### [[615_ebpf|eBPF]] vs. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] (Envoy/[[302_service_mesh_istio|Istio]])

| 구분 | [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] | [[615_ebpf|eBPF]] ([[825_cilium_ebpf_kubernetes_networking_security|Cilium]]) |
|:---|:---|:---|
| 구조 | Pod마다 Envoy [[561_container_based_deployment|컨테이너]] 주입 | [[022_kernel_role|커널]] 레벨 단일 [[615_ebpf|eBPF]] 프로그램 |
| 오버헤드 | CPU 5~15%, 메모리 50~200MB/[[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 오버헤드 < 1% |
| 가시성 | L7 [[461_http_stateless_connection_oriented|HTTP]] 수준 | L3~L7 + 시스템 콜 수준 |
| 레이턴시 추가 | 1~10ms ([[264_proxy_pattern_surrogate_access_control|프록시]] 경유) | <1μs |
| [[009_config|설정]] 복잡도 | 높음 ([[302_service_mesh_istio|Istio]] [[009_config|설정]] 복잡) | 낮음 ([[615_ebpf|eBPF]] 자동 부착) |

### 주요 [[615_ebpf|eBPF]] 기반 도구

| 도구 | 목적 |
|:---|:---|
| **[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]** | [[615_ebpf|eBPF]] 기반 [[205_kubernetes_container_orchestration|Kubernetes]] 네트워킹·[[302_service_mesh_istio|서비스 메시]] |
| **Falco** | 런타임 보안 위협 탐지 (시스템 콜 [[229_monitor|모니터]]링) |
| **BCC ([[069_ebpf|BPF]] Compiler Collection)** | [[615_ebpf|eBPF]] 프로그램 작성·실행 [[336_library_vs_framework|라이브러리]] |
| **bpftrace** | [[615_ebpf|eBPF]] 기반 고급 추적 스크립팅 언어 |
| **Tetragon** | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 기반 보안 관측성 |
| **Katran** | Facebook의 [[670_xdp|XDP]] 기반 로드밸런서 |

- **📢 섹션 요약 비유**: [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]와 eBPF의 차이는 **'각 방에 경비원을 배치하는 것([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]])'** 과 **'건물 [[933_cctv|CCTV]] 시스템 하나로 모든 방을 관제하는 것([[615_ebpf|eBPF]])'** 의 차이입니다. 경비원은 공간·비용이 필요하지만, CCTV는 거의 추가 비용 없이 전체를 커버합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 [[435_checklist_based_testing|체크리스트]]

| 요구사항 | [[615_ebpf|eBPF]] 활용 방법 | 도구 |
|:---|:---|:---|
| [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 없는 [[302_service_mesh_istio|서비스 메시]] | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] [[822_cni_container_network_interface_kubernetes|CNI]] + [[615_ebpf|eBPF]] | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] + Hubble |
| 런타임 보안 위협 탐지 | 시스템 콜 [[229_monitor|모니터]]링 | Falco, Tetragon |
| DDoS 방어 (패킷 드롭) | [[670_xdp|XDP]] [[615_ebpf|eBPF]] 프로그램 | Katran, [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] |
| [[090_service_kubernetes_network_load_balancing|서비스]] 레이턴시 [[613_profiling_gprof|프로파일링]] | kprobe + bpftrace | bpftrace, BCC |
| [[205_kubernetes_container_orchestration|Kubernetes]] 네트워크 [[164_policy|정책]] | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] Network [[164_policy|Policy]] | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] |

### 기술사 시험 핵심 포인트

1. **[[615_ebpf|eBPF]] Verifier**: [[022_kernel_role|커널]] 안전성을 컴파일 전 [[331_static_analysis|정적 분석]]으로 보장
2. **[[670_xdp|XDP]]([[661_ebpf_xdp_express_data_path|Express Data Path]])**: [[587_nic_offloading|NIC]] 드라이버 레벨의 최고속 패킷 처리 Hook
3. **[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]**: [[615_ebpf|eBPF]] 기반 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[822_cni_container_network_interface_kubernetes|CNI]]([[100_cni_container_network_interface_flannel_calico|Container Network Interface]]); [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 대체
4. **bpftrace**: AWK와 유사한 문법의 [[615_ebpf|eBPF]] 추적 스크립팅 언어

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**[[615_ebpf|eBPF]] 프로그램 Verifier 우회 시도**: Verifier를 통과하지 못한 [[615_ebpf|eBPF]] 프로그램은 [[022_kernel_role|커널]]에 로드할 수 없다. 루프·포인터 역참조 오류를 우회하려는 트릭은 [[036_kernel_panic|커널 패닉]]을 초래한다. Verifier 오류 [[389_mesh_topology|메시]]지를 읽고 올바르게 수정해야 한다.

**eBPF를 모든 곳에 적용**: eBPF는 강력하지만, 단순한 [[626_log_collection|로그 수집]]에는 기존 로깅 [[336_library_vs_framework|라이브러리]]가 훨씬 단순하다. eBPF는 **[[022_kernel_role|커널]] 레벨 가시성이 진짜 필요한 경우**에만 적용해야 한다.

- **📢 섹션 요약 비유**: [[615_ebpf|eBPF]] Verifier 우회는 **'안전 검사 없이 원자로에 들어가는 것'** 과 같습니다. 잠깐 들어갈 수 있어도, 방사선([[036_kernel_panic|커널 패닉]])은 시스템 전체를 죽입니다. [[395_verification_process_review|검증]]을 통과한 장비만 원자로에 들어갈 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

eBPF는 리눅스 [[022_kernel_role|커널]] 기술 중 지난 10년간 가장 혁신적인 기술로 평가받는다. [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 오버헤드 없는 [[302_service_mesh_istio|서비스 메시]], [[022_kernel_role|커널]] 레벨 [[007_security_policy|보안 정책]], [[670_xdp|XDP]] 기반 고성능 패킷 처리를 모두 안전하게 구현할 수 있게 했다.

**한계**: [[615_ebpf|eBPF]] 프로그램 작성은 C 또는 전용 언어로 이루어져 개발 진입 장벽이 높다. 또한 [[022_kernel_role|커널]] [[288_version_ihl_tos_total_length|버전]]마다 지원 기능이 달라 이식성 문제가 발생할 수 있다. CO-RE(Compile Once - Run Everywhere) 기술이 이 문제를 완화하고 있다.

**미래 방향**: ① [[615_ebpf|eBPF]] for Windows (Microsoft 프로젝트), ② eBPF가 [[302_service_mesh_istio|서비스 메시]]의 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 완전 대체, ③ [[615_ebpf|eBPF]] 기반 [[615_ebpf|eBPF]]-[[344_as_autonomous_system_asn|as]]-a-[[090_service_kubernetes_network_load_balancing|Service]] 플랫폼 등장.

eBPF는 "[[022_kernel_role|커널]]을 안전하게 프로그래밍하는 것"이 아니라, **"운영 중인 [[022_kernel_role|커널]]을 멈추지 않고 X-ray처럼 들여다보고 [[164_policy|정책]]을 주입하는 것"** 이라는 관점으로 이해해야 한다.

- **📢 섹션 요약 비유**: eBPF는 **'심장 수술을 멈추지 않고 하는 수술 로봇'** 과 같습니다. 서버(심장)를 멈추지 않고(무중단) [[022_kernel_role|커널]] 내부에 도구를 삽입해 진단·치료·관측하는 기적의 기술입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[670_xdp|XDP]] ([[661_ebpf_xdp_express_data_path|Express Data Path]])** | [[587_nic_offloading|NIC]] 드라이버 레벨 최고속 [[615_ebpf|eBPF]] Hook; DDoS 방어·로드밸런싱 |
| **[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]** | [[615_ebpf|eBPF]] 기반 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 네트워킹·보안·관측성; [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 대체 |
| **kprobe / tracepoint** | [[022_kernel_role|커널]] 함수·이벤트에 [[615_ebpf|eBPF]] 프로그램을 부착하는 Hook 포인트 |
| **Falco** | [[615_ebpf|eBPF]] 기반 런타임 보안 위협 탐지 도구 |
| **[[642_observability_telemetry|Observability]] (관측성)** | [[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces; eBPF가 가장 낮은 레이어에서 [[001_dikw_pyramid|데이터]] 제공 |

### 📈 관련 키워드 및 발전 흐름도

```text
BPF (Berkeley Packet Filter, 1992) — 패킷 필터링
    │
    ▼
eBPF (Extended BPF, Linux 3.18, 2014) — 커널 이벤트 전반
    │
    ├─► XDP — NIC 레벨 고속 패킷 처리 (DDoS 방어)
    ├─► kprobe/tracepoint — 커널 함수 추적
    ├─► Cilium — eBPF 기반 쿠버네티스 CNI·서비스 메시
    │
    ▼
사이드카 프록시(Envoy/Istio) 대체 움직임
    │
    ▼
eBPF for Windows / CO-RE / eBPF-as-a-Service (미래)
```

### 👶 어린이를 위한 3줄 비유 설명

1. eBPF는 **'서버 컴퓨터 속 [[001_operating_system_purpose|운영체제]]([[022_kernel_role|커널]])에 작은 감시 카메라를 설치하는 기술'** 이에요. 컴퓨터를 끄거나 다시 시작하지 않고도 카메라를 달아서 모든 [[001_dikw_pyramid|데이터]] 흐름을 볼 수 있어요!
2. 특별한 **안전 검사관(Verifier)** 이 카메라 프로그램을 먼저 검사해서, 혹시라도 컴퓨터를 망가뜨릴 코드는 절대 설치 못하게 막아요.
3. 이 기술 덕분에 각 앱마다 경비원([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]])을 따로 배치하지 않아도, **[[022_kernel_role|커널]] 하나로 모든 앱을 동시에 관찰하고 [[571_protection_vs_security|보호]]**할 수 있어서, 클라우드 서버 관리가 훨씬 가벼워졌어요!
