+++
title = "1058. 스트리밍 텔레메트리 (Streaming Telemetry) - 푸시 기반 실시간 네트워크 관측"

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스트리밍 텔레메트리 (Streaming Telemetry)는 네트워크 장비가 관리 시스템의 요청을 기다리지 않고 스스로 상태 데이터를 주기적 또는 이벤트 기반으로 능동적(Push)으로 전송하는 실시간 네트워크 관측 방식이다.
> 2. **가치**: 30~60초 간격의 SNMP 폴링이 놓치는 마이크로버스트(수 밀리초 폭주), 순간적 패킷 드롭, 큐 혼잡 등 짧은 이상 현상을 수초 이하의 세밀도로 포착하여 SLA 위반 전 선제 대응이 가능하다.
> 3. **판단 포인트**: YANG 데이터 모델로 구독(Subscription) 대상을 정의하고, gRPC + Protocol Buffers (Protobuf)로 고효율 전송하며, InfluxDB·Prometheus 같은 시계열 DB에 저장하고, Grafana로 시각화하는 전체 파이프라인을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

### SNMP 폴링 방식의 한계

기존 SNMP (Simple Network Management Protocol) 폴링 방식은 NMS (Network Management System)가 일정 주기(보통 30~60초)로 장비에 쿼리를 보내는 Pull 방식이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">SNMP 폴링 방식의 문제</div></div>
<div class="kb-diagram-note">NMS 장비</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Get-Request →</div><div class="kb-diagram-cell">(30초마다 물음)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">←── Response</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">29초 동안 보이지 않는 이벤트</div></div>
<div class="kb-diagram-note">● 마이크로버스트 발생 (10ms, 100Gbps 포트 포화)</div>
<div class="kb-diagram-note">● 패킷 드롭 급증 (1만 개 손실)</div>
<div class="kb-diagram-note">● 큐 100% 채움 → 회복</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이 모든 게 다음 폴링에서 이미 평균화되어 보이지 않음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Get-Request →</div><div class="kb-diagram-cell">(30초 후)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">←── "ifOutOctets: 정상" ─</div><div class="kb-diagram-cell">← 이상 현상 사라져 있음!</div></div>
</div>
</div>



**SNMP 폴링 방식의 5가지 한계**:

| 문제 | 원인 | 영향 |
| :--- | :--- | :--- |
| 관측 맹점 | 폴링 간격 내 이벤트 누락 | SLA 위반 원인 파악 불가 |
| 확장성 한계 | 수천 장비 × 수백 OID 폴링 부하 | NMS 서버 병목 |
| 반응 지연 | 문제 발생 후 최대 폴링 주기 후 인지 | 장애 대응 지연 |
| 평균화 효과 | 카운터 차분 계산으로 순간 값 소실 | 마이크로버스트 탐지 불가 |
| 단방향 폴링 | 장비가 중요 이벤트를 Trap으로만 전송 | 이벤트 유실 가능 |

### 스트리밍 텔레메트리의 등장

구글, 페이스북, 아마존 등 하이퍼스케일 데이터센터 운영자들은 자사 네트워크에서 마이크로버스트와 미세 장애를 추적하기 위해 스트리밍 텔레메트리를 자체 개발했다. 이후 Cisco, Juniper, Arista, Nokia 등 주요 벤더들이 gRPC + Protobuf 기반 텔레메트리를 표준 기능으로 채택했다.

- **📢 섹션 요약 비유**: SNMP 폴링은 30초마다 "환자 상태 어때요?"라고 물어보는 전화 상담이다. 스트리밍 텔레메트리는 환자 몸에 부착된 실시간 모니터가 1초마다 혈압·맥박을 자동으로 전송하는 방식이다. 순간적인 이상을 바로 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스트리밍 텔레메트리 전체 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">스트리밍 텔레메트리 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">네트워크 장비 (Cisco IOS XR / Juniper / Arista EOS)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 생산자 (Data Producer)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● CPU 사용률 (0.1초 샘플링)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● 인터페이스 카운터 (1초 샘플링)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● 큐 깊이 (100ms 샘플링)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● BGP 상태 변화 (이벤트 트리거)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Push (gRPC/gNMI)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">텔레메트리 수집기 (Collector)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● Pipeline (Cisco) ● Telegraf ● gNMIc</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● Streaming Telemetry ● Kafka ● pmacct</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시계열 DB 저장</div><div class="kb-diagram-cell">스트리밍 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">InfluxDB</div><div class="kb-diagram-cell">Apache Kafka</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Prometheus</div><div class="kb-diagram-cell">Apache Flink</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TimescaleDB</div><div class="kb-diagram-cell">Apache Spark Streaming</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분석 및 시각화 / 자동화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● Grafana (대시보드) ● Kibana (로그 분석)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● ML 이상 탐지 ● IBN 자동 조치</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● PagerDuty 알림 ● Ansible 자동 조치</div></div>
</div>
</div>



### Push 방식의 두 가지 모드

| 모드 | 방식 | 적합한 데이터 | 예시 |
| :--- | :--- | :--- | :--- |
| **Periodic (주기형)** | 고정 주기마다 전송 | 연속적 메트릭 | CPU 사용률, 인터페이스 트래픽 |
| **On-Change (이벤트형)** | 값 변경 시 즉시 전송 | 상태 변화 이벤트 | BGP peer 상태, 인터페이스 Up/Down |

### 데이터 모델과 전송 포맷



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 전송 스택 비교</div></div>
<div class="kb-diagram-note">SNMP 폴링:</div>
<div class="kb-diagram-note">UDP → SNMPv2c PDU → MIB OID 바이너리 인코딩</div>
<div class="kb-diagram-note">오버헤드: 상대적으로 큼, 가공 필요</div>
<div class="kb-diagram-note">스트리밍 텔레메트리:</div>
<div class="kb-diagram-note">gRPC → Protocol Buffers (Protobuf) 직렬화</div>
<div class="kb-diagram-note">오버헤드: 약 3~10배 작음, 처리 속도 빠름</div>
<div class="kb-diagram-note">JSON 인코딩 (YANG-JSON):</div>
<div class="kb-diagram-note">gRPC 또는 WebSocket → JSON 직렬화</div>
<div class="kb-diagram-note">오버헤드: 크지만 사람이 읽을 수 있음 (디버그 용이)</div>
</div>
</div>



**Protocol Buffers vs JSON 비교**:

| 항목 | Protocol Buffers (Protobuf) | JSON |
| :--- | :--- | :--- |
| 직렬화 크기 | 작음 (3~10배 압축) | 큼 |
| 처리 속도 | 매우 빠름 | 느림 |
| 가독성 | 없음 (바이너리) | 있음 |
| 스키마 필요 | 필요 (.proto 파일) | 불필요 |
| 주요 용도 | 고성능 프로덕션 환경 | 디버그, 소규모 환경 |

### gNMI (gRPC Network Management Interface) 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">gNMI 구독 프로토콜 흐름</div></div>
<div class="kb-diagram-note">컨트롤러 (Client) 장비 (gNMI Target)</div>
<div class="kb-diagram-tree-item" style="--depth:2">SubscribeRequest →</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">subscription: [</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ path: "interfaces/interface",</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">mode: SAMPLE,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">sample_interval: 1000000000 }</div><div class="kb-diagram-cell">(1초)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">]</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">←── SubscribeResponse (매 1초마다)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ timestamp: ...,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">updates: [</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ path: "interfaces/.../in-octets",</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">val: 12345678 }</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">]</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">←── SubscribeResponse</div><div class="kb-diagram-cell">(계속 스트리밍)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 스트리밍 텔레메트리는 스포츠 중계에서 선수의 실시간 심박수·속도·위치 데이터가 1초마다 방송국 서버로 자동 전송되는 것과 같다. 코치가 30초마다 "잘 되고 있어?"라고 묻는 것(SNMP 폴링)보다 훨씬 상세한 실시간 데이터를 얻을 수 있다.

---

## Ⅲ. 비교 및 연결

### SNMP 폴링 vs 스트리밍 텔레메트리 상세 비교

| 항목 | SNMP 폴링 | 스트리밍 텔레메트리 |
| :--- | :--- | :--- |
| 데이터 수집 방식 | Pull (NMS가 요청) | Push (장비가 자발적 전송) |
| 최소 관측 주기 | 30초 (실용적 한계) | 100ms 이하 가능 |
| 마이크로버스트 탐지 | 불가 | 가능 |
| 데이터 포맷 | MIB OID (ASN.1) | YANG 기반 Protobuf/JSON |
| 전송 프로토콜 | UDP (비신뢰성) | TCP/gRPC (신뢰성) |
| 보안 | 커뮤니티 스트링 (v1/v2c) | TLS/mTLS (gRPC) |
| 확장성 | NMS 폴링 부하 증가 | 장비 Push → 수집기 분산 |
| 이상 탐지 | 사후 분석 | 실시간 이상 탐지 가능 |
| 벤더 지원 | 모든 장비 | 최신 장비 위주 |
| 운영 복잡도 | 낮음 | 높음 (파이프라인 구축 필요) |

### 마이크로버스트 탐지 사례



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">마이크로버스트 발생 시나리오</div></div>
<div class="kb-diagram-note">데이터센터 ToR (Top of Rack) 스위치</div>
<div class="kb-diagram-tree-item" style="--depth:1">10GbE 업링크 포트 × 4개 (총 40GbE)</div>
<div class="kb-diagram-tree-item" style="--depth:1">서버 포트 수신 속도: 갑자기 45GbE 발생 (50ms간)</div>
<div class="kb-diagram-note">SNMP 폴링 (60초 주기) 결과:</div>
<div class="kb-diagram-note">t=0: ifOutOctets = 100,000,000</div>
<div class="kb-diagram-note">t=60: ifOutOctets = 103,000,000</div>
<div class="kb-diagram-note">→ 계산: 3,000,000 / 60 = 50,000 bytes/sec = 0.4Mbps (정상으로 보임)</div>
<div class="kb-diagram-note">→ 마이크로버스트 완전 은폐됨!</div>
<div class="kb-diagram-note">스트리밍 텔레메트리 (100ms 주기) 결과:</div>
<div class="kb-diagram-note">t=10.000s: ifOutOctets = 100,000,000</div>
<div class="kb-diagram-note">t=10.100s: ifOutOctets = 100,562,500 → 45Gbps 순간 폭주 감지!</div>
<div class="kb-diagram-note">t=10.200s: 큐 깊이 = 95% 도달 → 드롭 시작</div>
<div class="kb-diagram-note">t=10.300s: 패킷 드롭 카운터 = +15,000</div>
<div class="kb-diagram-note">→ 자동 알림 발송, 버퍼 튜닝 권고</div>
</div>
</div>



### 관련 기술 생태계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">텔레메트리 데이터 생산</div>
<div class="kb-diagram-tree-item" style="--depth:0">gNMI (gRPC Network Management Interface)</div>
<div class="kb-diagram-tree-item" style="--depth:0">gNOI (gRPC Network Operations Interface)</div>
<div class="kb-diagram-tree-item" style="--depth:0">NETCONF + YANG 구독</div>
<div class="kb-diagram-note">텔레메트리 전송</div>
<div class="kb-diagram-tree-item" style="--depth:0">gRPC (HTTP/2 기반 양방향 스트리밍)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Kafka (분산 메시지 큐)</div>
<div class="kb-diagram-tree-item" style="--depth:0">MQTT (IoT 환경)</div>
<div class="kb-diagram-note">텔레메트리 저장</div>
<div class="kb-diagram-tree-item" style="--depth:0">InfluxDB (시계열 DB)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Prometheus (Pull + Push 혼합)</div>
<div class="kb-diagram-tree-item" style="--depth:0">TimescaleDB (PostgreSQL 기반)</div>
<div class="kb-diagram-tree-item" style="--depth:0">OpenTSDB</div>
<div class="kb-diagram-note">텔레메트리 분석</div>
<div class="kb-diagram-tree-item" style="--depth:0">Grafana (시각화)</div>
<div class="kb-diagram-tree-item" style="--depth:0">ELK Stack (Elasticsearch + Logstash + Kibana)</div>
<div class="kb-diagram-tree-item" style="--depth:0">ML 이상 탐지 (Isolation Forest, LSTM)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 스트리밍 텔레메트리와 SNMP의 차이는 체온계로 하루 한 번 체온 측정 vs. ICU(중환자실)의 24시간 연속 생체신호 모니터의 차이다. 체온계는 측정 시점에만 체온을 알 수 있지만, ICU 모니터는 잠자는 동안의 순간적인 이상도 즉시 알람을 울린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Grafana 대시보드 구성 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">네트워크 텔레메트리 Grafana 대시보드 구성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">네트워크 운영 대시보드 (실시간)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인터페이스 트래픽 (1초)</div><div class="kb-diagram-cell">CPU/메모리 (5초)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프: 입출력 bps</div><div class="kb-diagram-node">게이지: 현재 사용률</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">마이크로버스트 이벤트 (100ms)</div><div class="kb-diagram-cell">BGP 상태 변화 (On-Change)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">히트맵: 큐 깊이</div><div class="kb-diagram-node">타임라인: UP/DOWN</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">패킷 드롭 추세</div><div class="kb-diagram-cell">이상 탐지 알림</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시계열: drop rate</div><div class="kb-diagram-node">알림 목록: ML 감지</div></div>
</div>
</div>



### 텔레메트리 설정 예시 (Cisco IOS XR)

```text
[Cisco IOS XR 텔레메트리 설정]

telemetry model-driven
 destination-group DG_GRAFANA
  address-family ipv4 10.1.1.100 port 57000
   encoding self-describing-gpb      ! Protobuf 인코딩
   protocol grpc no-tls
  !
 !
 sensor-group SG_INTERFACE
  sensor-path Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters
 !
 sensor-group SG_CPU
  sensor-path Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization
 !
 subscription SUB_1SEC
  sensor-group-id SG_INTERFACE sample-interval 1000    ! 1초
  sensor-group-id SG_CPU sample-interval 5000          ! 5초
  destination-id DG_GRAFANA
 !
```

### 설계 판단 체크리스트

1. **폴링 vs 텔레메트리 선택 기준**: SLA가 분 단위라면 SNMP 폴링으로 충분하다. 초 단위 이하 SLA, 마이크로버스트 탐지, AI 기반 이상 탐지가 필요하다면 스트리밍 텔레메트리가 필수다.
2. **장비 gNMI 지원 여부 확인**: 레거시 장비는 스트리밍 텔레메트리 미지원이다. 장비 목록과 지원 여부를 사전에 파악한다.
3. **수집기 확장성 설계**: 수천 장비에서 초당 수만 건 메시지를 처리하려면 Kafka + 멀티 컨슈머 구조가 필요하다.
4. **시계열 DB 보존 정책**: 고해상도 데이터(1초 주기)는 디스크 사용량이 크다. 7일 고해상도 + 30일 1분 집계 + 1년 1시간 집계 등 계층적 보존 정책을 설계한다.
5. **SNMP와 병행 전략**: 텔레메트리로 전환 중에는 SNMP와 병행 운영이 필요하다. 레거시 장비는 SNMP 유지, 신규 장비는 텔레메트리로 점진적 전환한다.

### 안티패턴

- **모든 OID를 텔레메트리로 전환**: 텔레메트리가 좋다고 모든 데이터를 100ms 주기로 수집하면 스토리지와 처리 비용이 폭증한다. 필요한 데이터만 적절한 주기로 선택해야 한다.
- **수집기 단일 노드 구성**: 수천 장비의 데이터를 단일 수집기로 받으면 장애 시 전체 관측이 불가해진다. Kafka + 다중 컨슈머 또는 수집기 클러스터가 필요하다.
- **알림 임계치 미설정**: 데이터만 수집하고 알림을 설정하지 않으면 수집의 의미가 없다. Grafana Alerting 또는 Prometheus AlertManager로 임계치 알림을 반드시 구성해야 한다.
- **시계열 DB 무기한 보존**: 고해상도 데이터를 무기한 보존하면 스토리지 비용이 급증한다. 자동 데이터 집계(Downsampling)와 만료 정책을 설정해야 한다.

- **📢 섹션 요약 비유**: 스트리밍 텔레메트리 파이프라인 설계는 CCTV 시스템 구축과 같다. 카메라(장비)는 영상을 찍고, 녹화 서버(수집기+시계열 DB)는 저장하고, 모니터링 센터(Grafana)는 이상 행동을 감지하고 알람을 울린다. 카메라만 달고 녹화 서버를 안 달면 의미가 없다.

---

## Ⅴ. 기대효과 및 결론

스트리밍 텔레메트리 도입 효과:

| 항목 | SNMP 폴링 환경 | 텔레메트리 환경 | 개선 효과 |
| :--- | :--- | :--- | :--- |
| 마이크로버스트 탐지율 | ~0% | ~95%+ | 탐지 가능 |
| 장애 인지 시간 | 폴링 주기 내 | 수초 이내 | 5~30배 단축 |
| MTTR (평균 복구 시간) | 30~60분 | 10~20분 | 40~60% 단축 |
| 네트워크 가시성 | 분 단위 | 초 단위 | 10~60배 향상 |
| SLA 예방적 대응 | 사후 대응 | 사전 대응 | 선제 관리 |

**미래 전망**: 스트리밍 텔레메트리는 IBN (Intent-Based Networking)과 결합하여 네트워크 상태를 실시간으로 파악하고 자동으로 조치하는 자율 네트워크(Autonomous Network) 구현의 핵심 기반이 되고 있다. AI/ML 기반 이상 탐지와 결합하면, 관리자가 장애를 인식하기도 전에 자동으로 대응하는 자가 치유 네트워크가 가능해진다.

기술사 관점에서 스트리밍 텔레메트리를 설명할 때는 단순히 "SNMP보다 빠르다"가 아니라, <strong>마이크로버스트 탐지 가능, AI 이상 탐지 기반 마련, IBN과의 통합</strong>이라는 세 가지 핵심 가치를 함께 제시하는 것이 중요하다.

- **📢 섹션 요약 비유**: 스트리밍 텔레메트리는 네트워크 세계의 스마트 팩토리 센서 네트워크다. 모든 기계(장비)가 실시간으로 상태를 보고하고, AI가 이상을 감지하면 자동으로 조치하는 인더스트리 4.0의 네트워크 버전이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| SNMP 폴링 | 스트리밍 텔레메트리가 극복하는 기존 방식 |
| YANG | 텔레메트리 데이터 경로(path) 정의에 사용 |
| gNMI | 스트리밍 텔레메트리의 gRPC 기반 구독 프로토콜 |
| gRPC + Protobuf | 고효율 텔레메트리 전송 스택 |
| InfluxDB / Prometheus | 텔레메트리 데이터 저장 시계열 DB |
| Grafana | 텔레메트리 데이터 시각화 도구 |
| IBN (의도 기반 네트워킹) | 텔레메트리 데이터로 자동 정책 적용 |
| NETCONF/YANG | 텔레메트리로 감지된 이상에 대한 자동 설정 조치 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SNMP Polling (1988~) - Pull 방식, 30초 주기, 분 단위 가시성</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SNMP Trap (비동기) - 이벤트 알림, 단방향, 유실 가능</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">하이퍼스케일 자체 개발 (2010s) - Google/Facebook 사내 텔레메트리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">gRPC + Protobuf 표준화 (2015~) - 고효율 스트리밍 전송</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">gNMI / OpenConfig 텔레메트리 (2017~) - YANG 기반 표준화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">벤더 내장 지원 (2018~) - Cisco/Juniper/Arista 기본 기능화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI/ML 이상 탐지 통합 (2020~) - 텔레메트리 + 머신러닝</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IBN 자율 네트워크 (현재~) - 실시간 상태 기반 자동 정책 조정</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 스트리밍 텔레메트리는 장난감이 스스로 "나 지금 배터리 30%, 온도 37도"라고 1초마다 엄마한테 문자를 보내는 것과 같아요.
2. 엄마가 30초마다 물어보는 것(SNMP 폴링)보다 훨씬 빠르게 문제를 알 수 있어요.
3. 잠깐 생겼다 사라지는 문제(마이크로버스트)도 실시간으로 찾을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 163 / 1120

← **이전**: [1057. NETCONF / YANG 모델링 규격체 - 차세대 네트워크 자동화](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1057_netconf_yang_network_configuration_modeling/)
**다음**: [1059. 디지털 트윈 및 관제 시스템 연동](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1059_digital_twin_network_management_simulation/) →

---
