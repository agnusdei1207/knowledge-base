---
title: 185. 네트워크 지터 (Network Jitter) 및 패킷 손실 관측 메트릭
date: '2026-04-28'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]] (Network Jitter)는 패킷 왕복시간이 큰가보다 패킷 간 [[015_지연_데이터_관점|지연]] 편차가 얼마나 흔들리는가를 보는 지표이며, 패킷 손실과 함께 실사용 품질을 좌우한다.
> 2. **가치**: 평균 [[015_지연_데이터_관점|지연]]시간만으로는 보이지 않는 마이크로 [[344_bus|버스]]트, 큐 적체, 무선 간섭, [[339_routing_overview_best_path_selection|라우팅]] 변화가 지터와 손실 [[342_routing_metric_hop_bandwidth_delay|메트릭]]에서는 먼저 드러나므로, 음성·영상·실시간 응용 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]]) 품질을 더 빨리 감지할 수 있다.
> 3. **판단 포인트**: 좋은 관측은 핑 평균값이 아니라 [[483_active_vs_passive_ftp|액티브]] 프로브, 전송계층 재전송, 인터페이스 드롭, 백분위수 히스토그램을 함께 보고 [[090_service_kubernetes_network_load_balancing|서비스]]별 허용치로 경보를 거는 데서 나온다.

---

## Ⅰ. 개요 및 필요성

[[808_network_jitter_delay_variation_storage_sync|네트워크 지터]]는 연속된 패킷들의 [[015_지연_데이터_관점|지연]]시간이 얼마나 들쑥날쑥한지를 뜻한다. 평균 왕복시간이 낮아도 어떤 패킷은 5ms, 어떤 패킷은 40ms에 도착한다면 실시간 통신은 끊겨 보일 수 있다. 패킷 손실은 전송되어야 할 패킷이 중간에서 사라지거나 너무 늦어 사실상 버려지는 현상이다.

운영 현장에서 지터와 손실이 중요한 이유는 사용자 체감 품질이 평균값보다 **꼬리 구간과 변동성**에 더 민감하기 때문이다. 인터넷 전화, 화상 회의, 온라인 게임은 물론이고, [[090_service_kubernetes_network_load_balancing|서비스]] 간 원격 프로시저 호출 ([[126_rpc|Remote Procedure Call]], [[126_rpc|RPC]]), [[002_database_definition|데이터베이스]] [[016_replication_factor|복제]], [[145_message_broker_sync_async|메시지 브로커]] [[212_synchronization_mechanisms|동기화]]도 지터와 손실이 커지면 재시도와 큐 적체가 연쇄적으로 커진다. 이때 평균 응답시간만 보면 "대체로 괜찮다"고 오판하기 쉽다.

지터와 손실을 같이 봐야 하는 이유도 분명하다. 지터만 높고 손실이 없으면 재생 버퍼나 재정렬로 흡수될 수 있지만, 지터가 커지는 순간 큐 오버플로와 재전송이 뒤따르면 곧 손실로 이어질 수 있다. 반대로 손실만 봐서는 왜 끊기는지 모르는 경우가 많다. 따라서 사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 공학 ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]], [[100_sre_site_reliability_engineering_error_budget|SRE]]) 관점에서는 네트워크를 빠른가 느린가가 아니라 **안정적으로 일정한가**의 관점으로 읽어야 한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Delay vs jitter                                                   │
├────────────────────────────────────────────────────────────────────┤
│ ideal send gap : 20ms | 20ms | 20ms | 20ms                        │
│ arrival gap    : 18ms | 44ms | 11ms | 27ms                        │
│                                                                    │
│ latency = average end-to-end delay                                 │
│ jitter  = variation between consecutive delays                     │
│ loss    = packets missing or arriving too late to be useful        │
└────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 지터는 [[344_bus|버스]]가 느린 것보다 도착 간격이 들쑥날쑥한 상태와 같다. 평균 이동시간이 비슷해도 어떤 [[344_bus|버스]]는 바로 오고 어떤 [[344_bus|버스]]는 한참 늦으면 승객 체감은 훨씬 나빠진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

측정의 기본은 [[015_지연_데이터_관점|지연]]시간, 지터, 손실을 각각 다른 값으로 분리하는 것이다. 일반적으로 [[015_지연_데이터_관점|지연]]시간은 왕복시간 (Round-Trip Time, [[441_rtt_round_trip_time_srtt_smoothed|RTT]]) 또는 [[008_단방향_반이중_전이중|단방향]] [[015_지연_데이터_관점|지연]]으로 측정하고, 지터는 연속 패킷 [[015_지연_데이터_관점|지연]] 차이의 절댓값 평균이나 [[136_variance|분산]]으로 본다. 실시간 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[451_rtp_real_time_transport_protocol|Real-time Transport Protocol]], [[451_rtp_real_time_transport_protocol|RTP]])에서는 완만한 추적을 위해 `J = J + (|D(i-1,i)| - J) / 16` 같은 평활화 식을 [[289_cqrs_db|쓰기]]도 한다.

[[008_단방향_반이중_전이중|단방향]] [[015_지연_데이터_관점|지연]]을 정확히 보려면 양 끝 시계가 정밀하게 맞아야 한다. 일반적인 네트워크 시간 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[536_ntp_network_time_protocol_stratum|Network Time Protocol]], [[536_ntp_network_time_protocol_stratum|NTP]]) 수준으로는 추세 파악은 가능하지만, 더 엄격한 측정은 정밀 시간 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[233_precision_recall_f1_roc_auc_threshold|Precision]] Time [[295_protocol_field_tcp_udp_icmp|Protocol]], PTP) 같은 [[212_synchronization_mechanisms|동기화]]가 필요하다. 그래서 많은 [[100_sre_site_reliability_engineering_error_budget|SRE]] 환경에서는 먼저 RTT와 그 변동성을 실용적 대리값으로 보고, 필요할 때만 더 정밀한 측정을 붙인다.

실무 관측 아키텍처는 보통 [[483_active_vs_passive_ftp|액티브]] 프로브와 패시브 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 함께 쓴다. [[483_active_vs_passive_ftp|액티브]] 프로브는 blackbox_exporter, [[191_transaction_concept_states|트랜잭션]] 프로브, 인터넷 제어 [[389_mesh_topology|메시]]지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[318_icmp_internet_control_message_protocol_diagnostics|Internet Control Message Protocol]], [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]]), 전송 제어 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]], [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]), 하이퍼텍스트 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[461_http_stateless_connection_oriented|Hypertext Transfer Protocol]], [[461_http_stateless_connection_oriented|HTTP]]) 체크처럼 "일부러 보내 보는 트래픽"이다. 패시브 [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 트래픽에서 재전송, 인터페이스 드롭, 큐 길이, 버퍼 오버런, 흐름 [[568_logs_distributed_logging_elk_fluentd|로그]]를 읽어 오거나, 확장 버클리 [[691_packet_filter_application_proxy|패킷 필터]] ([[147_ebpf_kernel_observability_cilium|extended Berkeley Packet Filter]], [[615_ebpf|eBPF]])로 [[125_socket|소켓]] [[015_지연_데이터_관점|지연]]을 관측하는 방식이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Jitter and loss observability path                                │
├────────────────────────────────────────────────────────────────────┤
│ Probe Agent / Client / eBPF                                       │
│   ├─ active RTT samples                                            │
│   ├─ packet loss ratio                                              │
│   ├─ tcp retransmissions                                            │
│   └─ interface drops / queue depth                                  │
│                 │                                                   │
│                 ▼                                                   │
│ Metrics pipeline                                                    │
│   ├─ Prometheus histograms                                          │
│   ├─ percentiles by path / region / service                         │
│   └─ alert rules                                                    │
│                 │                                                   │
│                 ▼                                                   │
│ Grafana dashboards -> SLO view -> incident routing                 │
└────────────────────────────────────────────────────────────────────┘
```

| [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 의미 | 대표 수식 또는 예 | 해석 포인트 |
| :--- | :--- | :--- | :--- |
| [[441_rtt_round_trip_time_srtt_smoothed|RTT]] p95 / p99 | 왕복 [[015_지연_데이터_관점|지연]]시간 꼬리 구간 | `histogram_quantile()` | 평균보다 사용자 체감에 가까움 |
| 지터 p95 | [[015_지연_데이터_관점|지연]] 편차의 상위 구간 | `abs(delay_i - delay_(i-1))` 기반 집계 | 마이크로 [[344_bus|버스]]트와 경로 불안정성 탐지 |
| 패킷 손실률 | 보낸 패킷 중 누락 비율 | `lost / sent * 100` | 무선 구간, 과부하, 드롭 [[396_validation|확인]] |
| [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 재전송률 | 손실 또는 혼잡의 간접 지표 | `retransmits / segments_sent` | 애플리케이션 느림과 직접 연결되기 쉬움 |
| 인터페이스 드롭 | 장비·호스트 큐 오버플로 | network interface, [[238_switch_operation_principles|switch]], [[022_kernel_role|kernel]] [[059_counter|counter]] | 어느 계층에서 버려지는지 좁히기 좋음 |

포인트는 평균값 하나로 끝내지 않는 것이다. 지터와 손실은 대부분 짧은 구간에서 폭발적으로 치솟았다가 사라지므로, 히스토그램과 백분위수로 보는 편이 훨씬 유용하다. 예를 들어 `5m avg RTT`는 멀쩡해 보여도 `p99 jitter`가 치솟으면 화상 회의 품질은 이미 나빠졌을 수 있다.

- **📢 섹션 요약 비유**: [[483_active_vs_passive_ftp|액티브]] 프로브와 패시브 [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 도로 위 시험 주행차와 실제 교통카메라를 함께 보는 것과 같다. 시험차만 보면 실제 혼잡을 놓치고, 카메라만 보면 기준 속도와 비교가 어렵다.

---

## Ⅲ. 비교 및 연결

지터는 [[015_지연_데이터_관점|지연]]시간과 비슷해 보이지만 다루는 질문이 다르다. [[015_지연_데이터_관점|지연]]시간은 "얼마나 멀리 돌아갔는가"를 묻고, 지터는 "매번 도착 시간이 얼마나 흔들리는가"를 묻는다. 패킷 손실은 "아예 도착하지 못한 패킷이 있는가"를 보여 준다. 이 셋이 서로 연결되지만 동일한 지표는 아니다.

| 항목 | [[015_지연_데이터_관점|지연]]시간 ([[141_latency|Latency]]) | 지터 (Jitter) | 패킷 손실 (Packet Loss) | 재전송 (Retransmission) |
| :--- | :--- | :--- | :--- | :--- |
| 핵심 질문 | 느린가 | 불안정한가 | 사라졌는가 | [[658_ir_recovery|복구]] 비용이 커졌는가 |
| 주 사용자 증상 | 전체 반응 [[015_지연_데이터_관점|지연]] | 음성 끊김, 프레임 튐, 꼬리 [[015_지연_데이터_관점|지연]] | [[573_timeout_retry_backoff_strategy|타임아웃]], 품질 저하 | [[139_throughput|처리량]] 저하, 큐 적체 |
| 흔한 원인 | 장거리 경로, 혼잡 | 큐 변동, 무선 간섭, 경로 변화 | 드롭, 오류, 과부하 | 손실, 혼잡 제어 |
| 대표 관측값 | [[441_rtt_round_trip_time_srtt_smoothed|RTT]] p95 | delay delta p95 | loss percentage | [[405_tcp_transmission_control_protocol_connection_oriented|tcp]] retrans ratio |

측정 방식도 비교해야 한다. [[483_active_vs_passive_ftp|액티브]] 프로브는 특정 경로의 품질을 일정한 기준으로 비교하기 좋지만, 실제 애플리케이션 트래픽의 혼잡 패턴을 100퍼센트 반영하지는 못한다. 패시브 관측은 실제 사용 트래픽을 보여 주지만, 암호화와 샘플링 제약 때문에 원인 분석이 어려울 수 있다. 따라서 두 방식을 함께 써야 "기준 품질"과 "실사용 품질"을 동시에 읽을 수 있다.

또한 네트워크 [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 애플리케이션 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 이어서 봐야 한다. 같은 시각에 지터가 급증하고, 동시에 `gRPC deadline exceeded`, `5xx` 오류율, 소비자 랙 (Lag)이 올라간다면 네트워크 원인이 더 유력해진다. 반대로 네트워크는 정상인데 오류율만 오른다면 애플리케이션 병목일 가능성이 높다. 즉 [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 단독 진단 도구가 아니라, 상위 [[090_service_kubernetes_network_load_balancing|서비스]] 지표와 결합될 때 의미가 커진다.

- **📢 섹션 요약 비유**: [[015_지연_데이터_관점|지연]]시간은 학교까지 걸리는 총 거리, 지터는 매일 걸리는 시간이 들쑥날쑥한 정도, 손실은 아예 숙제를 학교에 못 가져간 경우와 같다. 셋을 섞어 보면 문제 원인을 잘못 짚기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[090_service_kubernetes_network_load_balancing|서비스]] 특성에 따라 허용치를 다르게 잡아야 한다. 음성·영상은 낮은 [[015_지연_데이터_관점|지연]]보다도 일정한 도착 간격이 중요해 보통 지터 20~30ms 이하, 손실 1퍼센트 이하를 출발점으로 본다. 실시간 게임이나 원격 제어는 더 엄격할 수 있고, 배치 전송은 순간 지터보다 총 [[139_throughput|처리량]]과 재전송 비용이 더 중요할 수 있다. 따라서 단일 숫자 임계값을 모든 [[090_service_kubernetes_network_load_balancing|서비스]]에 강제하는 것은 좋은 운영이 아니다.

| [[090_service_kubernetes_network_load_balancing|서비스]] 유형 | 중점 [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 출발점으로 볼 수 있는 기준 | 운영 판단 |
| :--- | :--- | :--- | :--- |
| 음성·영상 회의 | 지터 p95, 손실률, 체감 품질 점수 | 지터 20~30ms 이하, 손실 1% 이하 | 버퍼 크기와 품질 저하를 함께 조정 |
| 실시간 [[014_api_posix|API]] 호출 | [[441_rtt_round_trip_time_srtt_smoothed|RTT]] p95, 지터, [[573_timeout_retry_backoff_strategy|타임아웃]]률 | [[015_지연_데이터_관점|지연]] 꼬리와 지터를 함께 관리 | 재시도 폭증 여부까지 [[396_validation|확인]] |
| [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]] / [[389_mesh_topology|메시]]지 [[123_pipe|파이프]] | 손실률, 재전송률, 큐 적체 | 손실에 매우 민감 | [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]], 랙, 스루풋과 함께 판단 |
| 일반 웹 [[090_service_kubernetes_network_load_balancing|서비스]] | [[441_rtt_round_trip_time_srtt_smoothed|RTT]] p95, 오류율 | 순간 손실보다 지속 추세 중요 | 네트워크와 애플리케이션 원인 분리 필요 |

경보 설계는 단일 핑 실패보다 더 신중해야 한다. 예를 들어 1분 동안 패킷 1개 손실로 바로 호출하면 오탐이 많아진다. 대신 "지터 p95 상승 + 손실률 상승 + 재전송 증가"처럼 둘 이상 [[130_signal|신호]]가 일정 시간 지속될 때 사건으로 취급하는 편이 좋다. 경로별, 리전별, 공급자별로 분리된 대시보드를 두면 마지막 구간 문제인지, 클라우드 구간 문제인지, 내부 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 문제인지도 더 빨리 좁힐 수 있다.

기술사 관점의 [[435_checklist_based_testing|체크리스트]]도 명확하다.

1. 측정 지점을 사용자 측, [[090_service_kubernetes_network_load_balancing|서비스]] 측, 중간 구간으로 나눠 비대칭 경로를 고려했는가?
2. 평균값 대신 백분위수와 히스토그램으로 꼬리 품질을 보고 있는가?
3. [[483_active_vs_passive_ftp|액티브]] 프로브와 패시브 재전송·드롭 [[059_counter|카운터]]를 함께 수집하는가?
4. 경보가 네트워크 현상 자체가 아니라 [[090_service_kubernetes_network_load_balancing|서비스]] 영향과 연결되는가?
5. 클라우드 공급자, [[983_vpn_virtual_private_network|가상 사설망]] (Virtual Private Network, [[983_vpn_virtual_private_network|VPN]]), 무선 구간처럼 외부 요인 구분이 가능한가?

대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]도 자주 보인다. 첫째, 평균 핑만 보고 네트워크가 정상이라고 판단하는 경우다. 둘째, 인터넷 제어 [[389_mesh_topology|메시]]지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 트래픽이 우선순위가 낮다는 사실을 무시하고 [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] 손실만으로 장애를 단정하는 경우다. 셋째, 네트워크 지표를 보면서도 애플리케이션 [[573_timeout_retry_backoff_strategy|타임아웃]], 재시도, 큐 길이를 함께 보지 않는 경우다. 넷째, [[008_단방향_반이중_전이중|단방향]] 측정 정확도가 필요한데 시계 [[212_synchronization_mechanisms|동기화]]를 [[395_verification_process_review|검증]]하지 않는 경우다.

- **📢 섹션 요약 비유**: 네트워크 경보는 비 오는 날 우산 하나 젖었다고 바로 재난 문자를 보내는 일이 아니다. 비가 얼마나 오래, 얼마나 세게, 어느 동네에 집중되는지 함께 봐야 진짜 대응이 된다.

---

## Ⅴ. 기대효과 및 결론

지터와 손실 [[342_routing_metric_hop_bandwidth_delay|메트릭]]이 잘 설계되면 네트워크 문제를 "느린 것 같다"는 감각이 아니라 재현 가능한 숫자로 설명할 수 있다. 이는 통신사 품질 협의, 멀티클라우드 경로 비교, [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 운영, 실시간 [[090_service_kubernetes_network_load_balancing|서비스]] 품질 개선에서 큰 차이를 만든다. 평균 [[015_지연_데이터_관점|지연]]이 정상인데도 사용자가 끊김을 호소하는 상황을 더 빨리 이해할 수 있다는 점도 실무 가치가 크다.

물론 한계도 있다. [[008_단방향_반이중_전이중|단방향]] [[015_지연_데이터_관점|지연]]은 시계 [[212_synchronization_mechanisms|동기화]] 정확도에 민감하고, 암호화된 트래픽에서는 패시브 분석 정보가 제한된다. 또한 애플리케이션 자체의 큐 적체나 서버 과부하가 [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]]처럼 보일 수도 있으므로, 호스트·애플리케이션 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 분리해서 읽어야 한다.

결론적으로 [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]]는 "빠른가"보다 "안정적으로 일정한가"를 묻는 지표다. 패킷 손실 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 함께 봐야 사용자 체감 품질을 제대로 설명할 수 있다. 기억할 핵심은 단순하다. **지터는 속도의 평균이 아니라 도착 시간의 흔들림이며, 관측은 평균 핑이 아니라 변동성과 손실의 결합으로 해야 한다.**

- **📢 섹션 요약 비유**: 지터 관측은 물이 빠르게 나오는지보다 수도꼭지에서 물줄기가 일정하게 나오는지를 보는 일과 같다. 순간순간 세기가 흔들리면 설거지도 샤워도 불편해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 왕복시간 (Round-Trip Time, [[441_rtt_round_trip_time_srtt_smoothed|RTT]]) | [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]의 기본 측정값이지만 지터와는 별개 |
| [[008_단방향_반이중_전이중|단방향]] [[015_지연_데이터_관점|지연]] (One-Way Delay) | 정확한 지터 분석에 유리하지만 시계 [[212_synchronization_mechanisms|동기화]]가 필요 |
| 패킷 손실률 | 지터가 실제 품질 저하로 번졌는지 판단하는 핵심 지표 |
| [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 재전송 | 손실·혼잡의 간접 [[130_signal|신호]]로 애플리케이션 [[282_performance_tactics|성능]]과 연결됨 |
| 버퍼블로트 (Bufferbloat) | 긴 큐로 인해 [[015_지연_데이터_관점|지연]]과 지터가 함께 커지는 대표 원인 |
| [[090_service_kubernetes_network_load_balancing|서비스]] 품질 ([[388_qos_quality_of_service_best_effort_intserv_diffserv|Quality of Service]], [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]]) | 우선순위·[[140_bandwidth|대역폭]] 제어로 지터 민감 트래픽을 [[571_protection_vs_security|보호]] |
| blackbox_exporter | [[483_active_vs_passive_ftp|액티브]] 프로브 기반 네트워크 품질 측정에 자주 쓰는 도구 |
| [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 ([[123_slo_service_level_objective|Service Level Objective]], [[181_slo_service_level_objective|SLO]]) | 네트워크 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 운영 [[164_policy|정책]]과 연결하는 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
RTT 기본 측정
    │
    ▼
지터 · 손실 백분위수 관측
    │
    ▼
재전송 · 인터페이스 드롭 상관분석
    │
    ▼
서비스 영향 기반 경보
    │
    ▼
QoS · 경로 최적화 · 회선 품질 개선
    │
    ▼
SLO 기반 실시간 네트워크 운영
```

### 👶 어린이를 위한 3줄 비유 설명

1. 지터는 공을 친구에게 던질 때 매번 도착 시간이 들쑥날쑥한 모습이에요.
2. 패킷 손실은 어떤 공은 아예 친구 손에 도착하지 못하고 사라지는 거예요.
3. 그래서 네트워크를 볼 때는 빨리 가는지뿐 아니라, 꾸준히 잘 도착하는지도 같이 봐야 해요.
