---
title: "Load Balancer"
date: "2026-04-29"
tags:
  - "studynote-cloud-architecture"
weight: 31
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로드 밸런서(Load Balancer)는 들어오는 네트워크 트래픽을 여러 서버에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)하여 단일 서버 과부하를 방지하고, 가용성과 확장성을 높이는 인프라 컴포넌트다.
> 2. **가치**: L4 로드 밸런서([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/))는 빠른 패킷 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)에, L7 로드 밸런서([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/))는 경로·헤더·[쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 기반 지능적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)에 강점이 있다. 현대 마이크로서비스는 L7 + [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 조합이 표준이다.
> 3. **판단 포인트**: 로드 밸런서 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정한다. Round Robin은 단순하지만 서버 부하 차이를 고려하지 않는다. Least Connections·Weighted [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 이를 보완한다.

---

## Ⅰ. 개요 및 필요성

```text
로드 밸런서 역할:

  클라이언트들
  | | | |
  v v v v
  [로드 밸런서]
  /    |    서버A  서버B  서버C
(CPU 40%) (CPU 30%) (CPU 70%)

역할:
  1. 트래픽 분산 (성능·확장성)
  2. 헬스 체크 (가용성)
  3. SSL 종료 (보안 오프로딩)
  4. 세션 지속성 (Sticky Session)
  5. 속도 제한 (Rate Limiting)
```

- **📢 섹션 요약 비유**: 로드 밸런서는 교통 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 교차로 경찰이다. 모든 차(트래픽)가 한 도로(서버)에 몰리지 않게 여러 방향으로 유도하고, 막힌 도로(다운 서버)는 우회시킨다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 설명 | 적합 상황 |
|:---|:---|:---|
| **Round Robin** | 순서대로 균등 분배 | 서버 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 동일 |
| **Weighted Round Robin** | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 비례 분배 | 서버 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이 |
| **Least Connections** | 최소 연결 수 서버 선택 | 처리 시간 차이 |
| **IP Hash** | 클라이언트 IP->서버 고정 | [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| **Random** | 무작위 선택 | 단순 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| <strong>Least <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">Response Time</a></strong> | 최소 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 서버 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |

### L4 vs L7 로드 밸런서

```text
L4 (Transport Layer):
  - IP + TCP/UDP 기반 분산
  - 패킷 수준 빠른 처리
  - 내용 기반 라우팅 불가
  - 예: AWS NLB, HAProxy (TCP 모드)

L7 (Application Layer):
  - HTTP 헤더·URL·쿠키 기반 분산
  - Path-based Routing: /api -> API 서버, /web -> 웹 서버
  - Header-based: User-Agent별 모바일/PC 서버 분리
  - 예: AWS ALB, Nginx, Traefik
```

- **📢 섹션 요약 비유**: L4 vs L7은 택배 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 방식이다. L4(우편번호 기준 지역 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)), L7(내용물 유형 기준 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) — 냉동식품은 냉장 창고, 일반 물품은 일반 창고)처럼 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준의 깊이가 다르다.

---

## Ⅲ. 비교 및 연결

| 비교 | L4 LB | L7 LB | [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) |
|:---|:---|:---|:---|
| 레이어 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) | 앱 레이어 |
| [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 기준 | IP·[포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | URL·헤더 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ID |
| 속도 | 매우 빠름 | 빠름 | 중간 |
| 기능 | 단순 | 풍부 | 가장 풍부 |
| 예시 | NLB | ALB, Nginx | [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) |

- **📢 섹션 요약 비유**: LB·[서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 교통 시스템 진화다. L4 LB([신호](/studynote/02_operating_system/02_process_thread/130_signal/)등), L7 LB(스마트 내비게이션), [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)(자율주행 교통 관제)로 지능화되고 기능이 풍부해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### AWS 로드 밸런서 선택 가이드

```text
ALB (Application Load Balancer):
  ✅ HTTP/HTTPS 웹 서비스
  ✅ 마이크로서비스 경로 기반 라우팅
  ✅ WebSocket, HTTP/2
  ✅ WAF(Web Application Firewall) 통합

NLB (Network Load Balancer):
  ✅ TCP/UDP 초저지연 요구
  ✅ 고정 IP 필요 (Elastic IP)
  ✅ 비 HTTP 프로토콜 (게임 서버, IoT)

GLB (Gateway Load Balancer):
  ✅ 보안 어플라이언스 트래픽 검사
  ✅ IDS/IPS, 방화벽 통합
```

### 헬스 체크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)

```text
헬스 체크 엔드포인트:
  GET /health -> HTTP 200 응답 -> 정상
  GET /health -> HTTP 500 / 타임아웃 -> 이상

설정 파라미터:
  interval:           30초마다 체크
  timeout:            5초 응답 대기
  healthy_threshold:  2회 연속 성공 -> 정상
  unhealthy_threshold: 3회 연속 실패 -> 제외
```

- **📢 섹션 요약 비유**: 헬스 체크는 의사 정기 검진이다. 30초마다 혈압([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 200)을 측정하고, 3번 연속 이상(500 오류)이면 환자(서버)를 격리(트래픽 제외)하여 다른 환자(클라이언트)에게 영향이 없게 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **고가용성** | 서버 장애 자동 우회 |
| **확장성** | 서버 추가로 선형 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 증가 |
| **보안** | SSL 종료·[WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 통합 |

[eBPF](/studynote/02_operating_system/10_security/615_ebpf/)(Extended [Berkeley Packet Filter](/studynote/02_operating_system/01_overview_architecture/069_ebpf/)) 기반 로드 밸런서가 차세대 기술로 주목받고 있다. [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)·Katran 같은 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 로드 밸런서는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 직접 패킷을 처리하여 기존 iptables 기반 대비 100배 이상의 처리 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보인다.

- **📢 섹션 요약 비유**: [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 로드 밸런서는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 교통경찰이다. 기존 LB가 도로 위에서 수신호를 하는 것이라면, [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) LB는 차량 내부 GPS 시스템처럼 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 직접 트래픽을 조종하여 100배 빠르다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Round Robin / LC** | [로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| **L4 / L7** | OSI 계층별 로드 밸런서 |
| **헬스 체크** | 서버 상태 자동 감지·제외 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a></strong> | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 LB |
| <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a></strong> | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 고성능 패킷 처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DNS 로드 밸런싱 — 단순 DNS 기반 분산]
    |
    v
[L4/L7 로드 밸런서 — TCP/HTTP 지능 분산]
    |
    v
[API 게이트웨이 — MSA 진입점 통합 LB]
    |
    v
[서비스 메시 (Istio) — 사이드카 기반 서비스 간 LB]
    |
    v
[eBPF LB — 커널 레벨 초고성능 패킷 처리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 로드 밸런서는 교통 경찰이에요 — 모든 손님(트래픽)이 한 계산대(서버)에 몰리지 않게 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시켜요!
2. L7은 더 똑똑한 경찰이에요 — 짐의 종류(URL)에 따라 다른 창고(서버)로 보내요!
3. 서버가 다운되면 자동으로 다른 서버로 트래픽을 우회시켜서 사용자가 오류를 느끼지 못하게 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 371

<- **이전**: [30. 오토 스케일링 — 클라우드 자동 용량 조정](/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/)
**다음**: [블록·파일·오브젝트 스토리지 (Block / File / Object Storage)](/studynote/13_cloud_architecture/01_virtualization/032_block_file_object_storage/) ->

---
