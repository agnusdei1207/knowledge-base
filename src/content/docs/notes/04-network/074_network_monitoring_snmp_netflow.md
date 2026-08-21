---
sidebar:
  order: 74
  label: "074. 네트워크 모니터링 (SNMP, NetFlow)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "네트워크 모니터링 및 텔레메트리 : SNMP, NetFlow/IPFIX 및 sFlow"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 74
extra:
  question_no: "074"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "장비 상태 감시(SNMP MIB/OID), 플로우 통계(NetFlow/IPFIX), 패킷 샘플링(sFlow) 및 상관 분석"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 모니터링(Network Monitoring)**: 네트워크 인프라의 가용성(Availability), 링크 대역폭 사용률, 트래픽 구성 성분, 패킷 손실 및 이상 징후를 실시간 탐지하고 분석하기 위한 통합 관제 기술.
- **SNMP(Simple Network Management Protocol)**: NMS(네트워크 관리 시스템)와 에이전트 간에 MIB(관리 정보 베이스) 객체 식별자(OID)를 기반으로 장비의 하드웨어 상태(CPU, 메모리, 인터페이스 업/다운, 트래픽 카운터)를 주기적으로 질의(Polling) 및 보고(Trap)하는 IETF 표준 프로토콜.
- **NetFlow / IPFIX 및 sFlow**: 라우터를 통과하는 패킷의 5-Tuple 헤더를 집약하여 플로우 단위 통계를 추출하는 기술(NetFlow/IPFIX)과 스위치 ASIC 하드웨어에서 패킷을 1/N 확률로 표본 추출(Sampling)하여 헤더를 전달하는 기술(sFlow).

</details>

- 정의/개념: 장비의 물리적 헬스 상태를 주기적으로 측정하는 **SNMP**, 5-Tuple 기반의 통신 플로우 세션 통계를 집약하는 **NetFlow/IPFIX**, 고속 스위칭 환경에서 표본 패킷을 추출하는 **sFlow** 를 유기적으로 결합한 **입체적 네트워크 관측성(Observability) 아키텍처**
- 배경/필요성: 단순한 장비 CPU/대역폭 임계치 경보(SNMP)만으로는 대규모 DDoS 공격, 비인가 대용량 데이터 유출, 이상 트래픽 발생 시의 발신지(IP)와 프로토콜 원인을 규명할 수 없어 심층 플로우 분석 기술이 요구됨

#### 한줄 요약
- SNMP의 장비 상태 감시와 NetFlow/sFlow의 플로우 통계 분석을 결합하여 통합 네트워크 가시성을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **이벤트 상관 분석(Event Correlation)**: SNMP 인터페이스 부하 급증 알람과 NetFlow 상의 특정 발신지 IP 대용량 플로우 레코드를 동일 타임스탬프 기반으로 교차 결합하여 장애 원인을 자동 규명하는 분석 기법.
- **NTP 시간 동기화(Network Time Protocol)**: 모든 분산 네트워크 장비와 로그 수집기 간의 시스템 시계를 밀리초(ms) 단위로 정밀 일치시켜 사건 발생 순서의 인과성을 검증 가능하게 하는 기반 기술.

</details>

- **다차원 입체 관측성(Multi-Dimensional Observability)**: 장비 가용성(SNMP) + 트래픽 주체(NetFlow) + 원시 패킷 헤더(sFlow)의 3단계 계층적 결합
- **실시간 상관 분석을 통한 인과 관계 규명**: 대역폭 포화 시점과 특정 호스트의 통신 세션을 시간축($\Delta t$)으로 자동 매핑
- **오버헤드 최적화 분업**: 코어 백본망에서는 패킷 샘플링(sFlow)을 적용하여 라우터 CPU 부하를 방지하고, 엣지 관문망에서는 전수 플로우 분석(NetFlow) 적용

#### 한줄 요약
- 다차원 관측성, 시간 동기화 기반 이벤트 상관 분석, 라우터 부하 분산 수집을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **익스포터(Flow Exporter)와 컬렉터(Flow Collector)**: 네트워크 장비 내부에서 플로우 캐시를 생성하여 UDP 패킷으로 방출하는 모듈(Exporter)과 이를 수신·저장·색인하는 중앙 관제 서버(Collector).
- **객체 식별자(Object Identifier, OID)**: MIB 트리 구조에서 CPU 점유율(`1.3.6.1.4.1...`), 포트 상태 등 특정 관리 항목을 유일하게 지시하는 점 표기법 번호.

</details>

```text
[ 관리 대상 네트워크 인프라 (Switches / Routers / Firewalls) ]
 ├─ [ SNMP Agent ] ──────────(SNMP Poll / Trap: UDP 161/162)────▶ [ NMS 상태 관리기 ]
 ├─ [ NetFlow/IPFIX Exporter ] ─(5-Tuple Flow Record: UDP 2055)──▶ [ Flow Collector ]
 └─ [ sFlow Agent (ASIC) ] ────(1/N Sampled Packets: UDP 6343)───▶ [ Packet Analyzer ]
                                                                          │
                                                                          ▼ (정규화 및 시간 동기 결합)
                                                               [ 통합 AIOps 상관 분석 엔진 ]
```

선의 의미: 인프라 장비의 에이전트들이 서로 다른 포트와 프로토콜로 상태/플로우 데이터를 전송하고, 중앙 분석 엔진이 이를 정규화하여 통합 관제하는 파이프라인

| 구성요소 | 책임 및 역할 | 프로토콜 / 포트 |
|:---|:---|:---|
| **SNMP Agent / NMS** | MIB/OID 기반 장비 CPU, 메모리, 포트 Up/Down, 에러 패킷 계측 | UDP 161 (Poll), 162 (Trap) |
| **NetFlow / IPFIX Exporter** | 라우터 플로우 캐시에서 세션 시작/종료 시간, 바이트 수, 5-Tuple 집약 송출 | UDP 2055, 4739 (IPFIX) |
| **sFlow Agent (ASIC)** | 스위치 데이터 평면 ASIC에서 1/1000 확률로 패킷 헤더 복제 송출 | UDP 6343 |
| **Flow Collector** | 분산 장비로부터 유입되는 대규모 플로우 레코드 파싱, 인덱싱 및 시계열 저장 | Elasticsearch / ClickHouse |
| **상관 분석기 (Correlator)** | SNMP 부하 그래프와 NetFlow Top-N 발신지를 매핑하여 이상 트래픽 경보 생성 | AIOps / SIEM |

#### 한줄 요약
- SNMP 에이전트, Flow 익스포터, sFlow 에이전트, 플로우 컬렉터, 상관 분석 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **5-Tuple 플로우 정의**: 출발지 IP, 목적지 IP, 출발지 포트, 목적지 포트, L4 프로토콜 번호가 동일한 연속된 IP 패킷의 집합.

</details>

```text
1. NMS가 주기적(1~5분)으로 라우터에 SNMP GetRequest(OID 질의) 송신 ➔ 인터페이스 대역폭 95% 초과 감지
            │
            ▼
2. 라우터 NetFlow/IPFIX 모듈이 활성 플로우 캐시를 주기적으로 플러시(Flush)하여 Collector로 레코드 송출
            │
            ▼
3. Flow Collector가 유입된 플로우 레코드를 시간순으로 정렬하고 NTP 타임스탬프 기준으로 정규화
            │
            ▼
4. 상관 분석 엔진이 SNMP 대역폭 임계치 초과 시점($T_0$)과 NetFlow 발신지 트래픽량 순위(Top-N) 교차 대조
            │
            ▼
5. 특정 내부 IP의 비인가 UDP Flooding 트래픽이 원인임을 확정 ➔ 관리자 경보 발송 및 방화벽 차단 연동
```

**동작 원리**

1. **상태 폴링**: NMS가 SNMP OID 조회를 통해 스위치 포트별 패킷 카운터(ifInOctets) 증감률 계측
2. **플로우 집약**: 라우터가 수신 패킷을 5-Tuple 기준으로 캐싱하고 타임아웃(Active/Inactive) 만료 시 레코드 방출
3. **표본 추출(sFlow)**: 100G 고속 백본에서는 하드웨어 ASIC 레벨에서 패킷 헤더를 통계적 샘플링하여 전송
4. **타임라인 정렬**: NTP 동기화된 타임스탬프를 기준으로 SNMP 부하 이벤트와 Flow 발신자를 1:1 매핑
5. **사전 조치 집행**: 분석 결과에 따라 비인가 트래픽 발신 포트를 즉각 셧다운하거나 QoS 폴리싱 집행

#### 한줄 요약
- SNMP 이상 감지, NetFlow 레코드 수집, 타임스탬프 정규화, 상관 분석 인과 규명, 자동 차단 연계 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SNMP vs NetFlow/IPFIX vs sFlow**: 물리 장치 상태 계측(SNMP), 세션 단위 흐름 전수/통계 분석(NetFlow), 하드웨어 패킷 표본 추출(sFlow)의 기술적 특성 비교.

</details>

| 비교 항목 | SNMP (IETF RFC 1157/3411) | NetFlow / IPFIX (RFC 7011) | sFlow (RFC 3176) |
|:---|:---|:---|:---|
| **수집 관점** | **장비 및 인터페이스 헬스 상태** | **통신 세션 및 트래픽 흐름 통계** | **네트워크 패킷 통계적 표본 (헤더)** |
| **데이터 단위** | MIB 트리 기반의 **OID 카운터/값** | **5-Tuple 세션 플로우 레코드** | **1/N 비율로 추출된 원시 패킷 헤더** |
| **라우터 CPU 부하** | 낮음 (주기적 폴링) | **중간~높음 (소프트웨어 캐시 관리)** | **매우 낮음 (스위치 하드웨어 ASIC 처리)** |
| **모니터링 정밀도** | 링크 총량 대역폭 확인 가능 | **누가, 어디로, 얼마나 쐈는지 완벽 파악**| 표본 추출로 통계적 추정 (희소 패킷 누락) |
| **주요 활용 분야** | 기본 NMS 장애/가용성 감시 | **트래픽 과금, 대역폭 분석, 이상 징후 탐지**| **100G/400G 초고속 데이터센터 백본망** |

#### 한줄 요약
- SNMP는 장비 가용성, NetFlow는 세션 상세 분석, sFlow는 초고속 백본 저부하 관제에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **순환 버퍼 오버플로우(Collector Drop)**: DDoS 공격이나 트래픽 폭증 시 초당 수십만 개의 플로우 UDP 패킷이 쏟아져 컬렉터 서버의 소켓 수신 버퍼가 오버플로우되어 관제 데이터가 유실되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장비 간 시계 불일치로 인한 이벤트 타임스탬프 오차 및 장애 원인 추적 실패 | 전 인프라에 **NTP/PTP(정밀 시간 프로토콜) 계층 구조 동기화** 의무화 | 밀리초(ms) 단위 이벤트 타임라인 일치 및 상관 분석 신뢰성 확보 |
| 100Gbps 고속 인터페이스에서 NetFlow 활성화 시 라우터 CPU 점유율 100% 폭증 | **하드웨어 ASIC 기반 sFlow 샘플링(1:1000)** 또는 Sampled NetFlow 전환 | 라우터 패킷 포워딩 성능 저하 방지 및 관제 부하 최적화 |
| 트래픽 폭주 시 NetFlow UDP 패킷 유실로 인한 컬렉터 통계 왜곡 | **Kafka 기반 메시지 큐 완충 버퍼링** 및 Collector 스케일아웃 구성 | 대규모 플로우 데이터 무손실 수용 및 관제 시스템 복원력 확보 |

#### 한줄 요약
- NTP 동기화로 타임라인을 일치시키고, sFlow로 라우터 부하를 방지하며, Kafka 버퍼로 플로우 유실을 방어한다.

## Ⅶ. 결론

- 복잡 다변화된 하이브리드 클라우드 및 대규모 백본망의 신뢰성을 확보하기 위해 **SNMP**, **IPFIX/NetFlow**, **sFlow** 를 결합한 **엔드투엔드 네트워크 가시성 플랫폼**을 구축하되, 실무 운영의 정확성을 보장하기 위해 **NTP 정밀 시간 동기화**, **고속망 sFlow 하드웨어 오프로딩**, **AI 기반 상관 분석 및 자동 격리(SOAR)** 체계를 통합 적용하여 지능형 자율 관제(AIOps)를 완성

#### 한줄 요약
- SNMP 상태 감시와 Flow 세션 분석을 NTP 기반으로 결합하여 지능형 네트워크 AIOps를 구현한다.
