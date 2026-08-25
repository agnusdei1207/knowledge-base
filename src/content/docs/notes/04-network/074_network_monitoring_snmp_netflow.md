---
sidebar:
  order: 74
  label: "074. 네트워크 모니터링: SNMP, NetFlow"
  badge:
    text: "미출 · 50%"
    variant: note
title: "네트워크 모니터링 및 텔레메트리 : SNMP, NetFlow, sFlow"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 74
extra:
  question_no: "74"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "장비 상태 감시(SNMP MIB/OID), 플로우 통계(NetFlow/IPFIX), 패킷 샘플링(sFlow) 및 상관 분석"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SNMP (Simple Network Management Protocol)**: MIB/OID 기반으로 라우터/스위치의 CPU, 메모리, 포트 트래픽을 폴링/트랩하는 관리 프로토콜.
- **NetFlow / IPFIX & sFlow**: 5-Tuple 세션 플로우 통계를 집약하는 NetFlow/IPFIX와 ASIC 레벨에서 1/N 확률로 패킷을 샘플링하는 sFlow.

</details>

- 정의/개념: 장비의 하드웨어 헬스 상태를 수집하는 **SNMP와 5-Tuple 기반 세션 통계를 추출하는 NetFlow, 하드웨어 표본을 추출하는 sFlow를 결합한 통합 관제 기술**
- 배경/필요성: 단순 링크 Up/Down 및 포트 상태 감시(SNMP)만으로는 **대역폭을 과점하는 이상 트래픽 발신자(Top-N) 및 DDoS 공격의 세부 세션 인과 규명 불가**

#### 한줄 요약
- SNMP(장비 상태), NetFlow(세션 분석), sFlow(패킷 샘플링)를 결합하여 전방위 관측성을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **5-Tuple Flow (5개조 플로우)**: 출발지 IP, 목적지 IP, 출발지 포트, 목적지 포트, 프로토콜 5개 필드로 유일 식별되는 통신 세션 단위.
- **MIB & OID (Management Information Base & Object Identifier)**: 트리 구조 계층으로 정의된 네트워크 장비의 관리 객체 데이터베이스 및 식별 번호.

</details>

- **다차원 네트워크 가시성 확보**: 장비 하드웨어 리소스(SNMP)와 네트워크 패킷 세션 흐름(NetFlow)을 입체 결합
- **시간 동기화 기반 이벤트 상관 분석**: NTP/PTP 동기화 타임스탬프를 대조하여 **대역폭 이상 징후의 근본 원인(RCA) 규명**
- **오버헤드 최적화 분업 체계**: 코어 백본은 **ASIC 기반 sFlow 샘플링**으로 부하를 방지하고, 엣지는 **전수 NetFlow 분석** 적용

#### 한줄 요약
- 다차원 관측성, 시간 동기화 기반 이벤트 상관 분석, 라우터 부하 분산 수집을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Flow Exporter vs Collector**: 라우터 내부에서 플로우 캐시를 생성해 UDP로 방출하는 모듈(Exporter)과 이를 수신·저장·분석하는 관제 서버(Collector).

</details>

```text
[네트워크 모니터링 및 텔레메트리 통합 수집 아키텍처]
|-- Managed Network Infrastructure (스위치 / 라우터 / 방화벽)
|   |-- SNMP Agent (MIB/OID 상태 계측 -> UDP 161 Poll / UDP 162 Trap)
|   |-- NetFlow/IPFIX Exporter (5-Tuple 플로우 캐시 집약 -> UDP 2055/4739)
|   `-- sFlow Agent (하드웨어 ASIC 1/1000 샘플링 -> UDP 6343)
`-- Central Ingestion & Storage Layer
|   |-- NMS Server (SNMP RRD 시계열 메트릭 저장소)
|   `-- Flow Collector (Elasticsearch / ClickHouse 플로우 인덱싱)
`-- Analytics & AIOps Engine (NTP 시간 동기화 기반 이벤트 교차 상관 분석)
```

선의 의미: 인프라 장비의 에이전트들이 서로 다른 포트와 프로토콜로 상태/플로우 데이터를 전송하고 중앙 분석 엔진이 이를 정규화하여 통합 관제하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 프로토콜 / 포트 |
|:---|:---|:---|
| **SNMP Agent / NMS** | MIB/OID 기반 **장비 CPU, 메모리, 포트 Up/Down, 에러 패킷 계측** | UDP 161 (Poll), 162 (Trap) |
| **NetFlow / IPFIX** | 라우터 플로우 캐시에서 **세션 시간, 바이트 수, 5-Tuple 집약 송출** | UDP 2055, 4739 (IPFIX) |
| **sFlow Agent (ASIC)**| 스위치 데이터 평면 ASIC에서 **1/N 확률로 패킷 헤더 복제 송출** | UDP 6343 |
| **Flow Collector** | 분산 장비로부터 유입되는 **플로우 레코드 파싱, 인덱싱 및 시계열 저장** | Elasticsearch, ClickHouse |
| **상관 분석기 (AIOps)**| SNMP 부하 그래프와 **NetFlow Top-N 발신지를 매핑하여 이상 트래픽 경보** | SIEM / SOAR |

#### 한줄 요약
- SNMP 에이전트, Flow 익스포터, sFlow 에이전트, 플로우 컬렉터, 상관 분석 엔진이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Active/Inactive Timeout**: 플로우가 계속 지속될 때 주기적으로 내보내는 Active 타임아웃(예: 60초)과 세션 종료 후 내보내는 Inactive 타임아웃(예: 15초).

</details>

```text
통합 네트워크 모니터링 및 이상 트래픽 원인 규명 파이프라인
        │
   1. [SNMP 임계치 초과 감지] NMS가 SNMP OID 질의를 통해 인터페이스 대역폭 95% 초과 감지
        │
   2. [NetFlow 레코드 송출] 라우터가 플로우 캐시를 플러시하여 Collector로 5-Tuple 레코드 방출
        │
   3. [NTP 타임스탬프 정규화] Flow Collector가 유입된 플로우를 시간순 정렬 및 표준화
        │
   4. [교차 상관 분석 실행] AIOps 엔진이 SNMP 피크 시점과 NetFlow Top-N 발신지 IP 대조
        │
   ▼
5. [이상 원인 특정 및 차단] 특정 내부 호스트의 UDP Flooding 원인을 확정하고 방화벽 차단 연동
```

#### 한줄 요약
- SNMP 이상 감지 → NetFlow 레코드 수집 → 타임스탬프 정규화 → 상관 분석 인과 규명 → 자동 차단 연계 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SNMP** vs **NetFlow/IPFIX** vs **sFlow**: 하드웨어 헬스 상태, 5-Tuple 세션 통계, ASIC 패킷 표본 추출.

</details>

| 비교 항목 | SNMP (IETF RFC 1157/3411) | NetFlow / IPFIX (RFC 7011) | sFlow (RFC 3176) |
|:---|:---|:---|:---|
| **수집 관점** | **장비 및 인터페이스 헬스 상태** | **통신 세션 및 트래픽 흐름 통계** | **네트워크 패킷 통계적 표본 (헤더)** |
| **데이터 단위** | MIB 트리 기반의 **OID 카운터/값** | **5-Tuple 세션 플로우 레코드** | **1/N 비율로 추출된 원시 패킷 헤더**|
| **라우터 CPU 부하** | 낮음 (주기적 폴링) | **중간~높음 (소프트웨어 캐시 관리)** | **매우 낮음 (스위치 하드웨어 ASIC 처리)**|
| **모니터링 정밀도** | 링크 총량 대역폭 확인 가능 | **누가, 어디로, 얼마나 쐈는지 완벽 파악**| 표본 추출로 통계적 추정 (희소 패킷 누락) |
| **주요 활용 분야** | 기본 NMS 장애/가용성 감시 | **트래픽 과금, 대역폭 분석, 이상 탐지**| **100G/400G 초고속 데이터센터 백본망** |

#### 한줄 요약
- SNMP는 장비 가용성, NetFlow는 세션 상세 분석, sFlow는 초고속 백본 저부하 관제에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Kafka Ingestion Buffer**: DDoS 공격이나 트래픽 폭증 시 초당 수십만 개의 UDP 플로우 패킷이 컬렉터로 쏟아질 때 패킷 유실을 방지하는 메시지 큐 완충 계층.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장비 간 시계 불일치로 인한 이벤트 타임스탬프 오차 및 원인 추적 실패 | 전 인프라에 **`NTP/PTP (정밀 시간 프로토콜) 계층 구조 동기화`** 의무화 | 밀리초 단위 이벤트 타임라인 일치 및 상관 분석 신뢰성 확보 |
| 100Gbps 고속 인터페이스에서 NetFlow 활성화 시 라우터 CPU 폭증 | **`하드웨어 ASIC 기반 sFlow 샘플링(1:1000)`** 또는 Sampled NetFlow 전환 | 라우터 포워딩 성능 저하 방지 및 관제 부하 최적화 |
| 트래픽 폭주 시 NetFlow UDP 패킷 유실로 인한 통계 왜곡 | **`Kafka 기반 분산 메시지 큐 완충 버퍼링`** 및 Collector 스케일아웃 | 대규모 플로우 데이터 무손실 수용 및 관제 시스템 복원력 확보 |
| SNMP v1/v2c의 평문 Community String 노출로 인한 장비 장악 위험 | **`SNMP v3 (SHA-256 인증 + AES-256 암호화)` 표준 적용** | 제3자 도청 및 비인가 장비 설정 변조 원천 차단 |

#### 한줄 요약
- NTP 동기화, sFlow ASIC 가속, Kafka 완충 큐, SNMP v3 암호화로 운영한다.

## Ⅶ. 결론

- 복잡 다변화된 하이브리드 클라우드 및 대규모 백본망의 신뢰성을 확보하기 위해 **SNMP, IPFIX/NetFlow, sFlow를 결합한 엔드투엔드 네트워크 가시성 플랫폼을 구축**하되, 실무 운영의 정확성을 보장하기 위해 **NTP 정밀 시간 동기화, 고속망 sFlow 하드웨어 오프로딩, AI 기반 상관 분석 및 자동 차단 체계**를 통합 적용하여 지능형 자율 관제(AIOps) 완성

#### 한줄 요약
- SNMP 상태 감시와 NetFlow/sFlow 세션 분석을 NTP 기반으로 결합하여 지능형 네트워크 AIOps를 구현한다.