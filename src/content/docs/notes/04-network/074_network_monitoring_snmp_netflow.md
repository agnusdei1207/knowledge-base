---
sidebar:
  order: 74
  label: "074. 네트워크 모니터링: SNMP, NetFlow"
  badge:
    text: "미출 · 50%"
    variant: note
title: "네트워크 모니터링 및 텔레메트리 : SNMP, NetFlow, sFlow"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: **SNMP·NetFlow·sFlow**를 결합한 통합 관제 기술
- 배경/필요성: 대규모 복합 네트워크 환경에서 장비 인터페이스의 단순 Up/Down 및 대역폭 사용률만을 폴링(Polling)하는 고전적 모니터링 방식은 네트워크 혼잡이나 이상 트래픽 발생 시 어떤 IP, 포트, 애플리케이션이 병목을 유발했는지 세부적인 원인 규명이 불가능하고 엔지니어가 개별 장비에 직접 접속하여 수동 트러블슈팅해야 하는 막대한 운영 비용을 초래함에 따라, 장비의 물리적 헬스 상태(CPU, 메모리, 인터페이스 에러)를 감시하는 SNMP(MIB/OID)와 통신 세션 단위의 5-Tuple 통계를 집약하는 NetFlow/IPFIX 및 하드웨어 ASIC 레벨 표본 추출(sFlow)을 융합한 텔레메트리 관제 아키텍처를 도입하여 **이상 징후의 조기 감지, 세션 단위 심층 가시성(Deep Visibility) 확보 및 NTP 기반 이벤트 상관 분석을 통한 신속한 장애 복구**를 달성할 필요

#### 한줄 요약
- SNMP(장비 상태), NetFlow(세션 분석), sFlow(패킷 샘플링)를 결합하여 전방위 관측성을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **5-Tuple Flow (5개조 플로우)**: 출발지 IP, 목적지 IP, 출발지 포트, 목적지 포트, 프로토콜 5개 필드로 유일 식별되는 통신 세션 단위.
- **MIB & OID (Management Information Base & Object Identifier)**: 트리 구조 계층으로 정의된 네트워크 장비의 관리 객체 데이터베이스 및 식별 번호.

</details>

- **다차원 가시성**: 장비 상태와 세션 흐름을 결합
- **이벤트 상관 분석**: 동기화 시각으로 **근본 원인** 규명
- **수집 부하 분산**: 코어는 **sFlow**, 엣지는 **NetFlow** 적용

#### 한줄 요약
- 다차원 관측성, 시간 동기화 기반 이벤트 상관 분석, 라우터 부하 분산 수집을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Flow Exporter vs Collector**: 라우터 내부에서 플로우 캐시를 생성해 UDP로 방출하는 모듈(Exporter)과 이를 수신·저장·분석하는 관제 서버(Collector).

</details>

```text
[통합 네트워크 관제]
|-- SNMP 수집기       : MIB/OID 장비 상태
|-- NetFlow 수집기    : 5-Tuple 세션 통계
|-- sFlow 수집기      : 패킷 표본
|-- 플로우 저장소     : 레코드 인덱싱
`-- 상관 분석기       : 시각 기반 이벤트 연계
```

선의 의미: 인프라 장비의 에이전트들이 서로 다른 포트와 프로토콜로 상태/플로우 데이터를 전송하고 중앙 분석 엔진이 이를 정규화하여 통합 관제하는 구조

| 구성요소 | 책임 |
|:---|:---|
| SNMP 수집기 | **MIB/OID** 기반 장비 상태 수집 |
| NetFlow 수집기 | **5-Tuple** 세션 레코드 집약 |
| sFlow 수집기 | **ASIC** 기반 패킷 표본 추출 |
| 플로우 저장소 | 레코드 **파싱·인덱싱** |
| 상관 분석기 | 시각 기반 **이상 이벤트 연계** |

#### 한줄 요약
- 익스포터가 장비 곁에서 원본 트래픽을 요약 레코드로 줄여 보내므로, 컬렉터는 패킷 전량이 아니라 축약 사본만으로 세션을 재구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Active/Inactive Timeout**: 플로우가 계속 지속될 때 주기적으로 내보내는 Active 타임아웃(예: 60초)과 세션 종료 후 내보내는 Inactive 타임아웃(예: 15초).

</details>

```text
장비·트래픽
     |
     +-- 1. SNMP 임계치 감지
     +-- 2. NetFlow 레코드 송출
     +-- 3. 타임스탬프 정규화
     `-- 4. 교차 상관 분석
                 |
              관제·차단
```

동작 원리

1. SNMP 임계치 감지
2. NetFlow 레코드 송출
3. 타임스탬프 정규화
4. 교차 상관 분석

#### 한줄 요약
- SNMP 이상 신호만으로는 원인을 가릴 수 없어 플로우 레코드 상관 분석으로 넘어가며, 그 인과 판정의 정확도는 NTP 타임스탬프 정합 수준이 좌우한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SNMP** vs **NetFlow/IPFIX** vs **sFlow**: 하드웨어 헬스 상태, 5-Tuple 세션 통계, ASIC 패킷 표본 추출.

</details>

| 비교 항목 | SNMP (IETF RFC 1157/3411) | NetFlow / IPFIX (RFC 7011) | sFlow (RFC 3176) |
|:---|:---|:---|:---|
| 수집 관점 | 장비·인터페이스 **상태** | 통신 세션 **흐름 통계** | 패킷 **통계 표본** |
| 데이터 단위 | MIB 기반 **OID 값** | **5-Tuple** 플로우 레코드 | **1/N** 패킷 헤더 |
| 라우터 CPU 부하 | 낮음 | **중간~높음** | **매우 낮음** |
| 모니터링 정밀도 | 링크 총량 확인 | 세션별 **발신지·목적지·사용량** 확인 | 표본 기반 **통계 추정** |
| 주요 활용 분야 | NMS **장애·가용성 감시** | **과금·대역폭·이상 탐지** | 초고속 백본 **저부하 관제** |

#### 한줄 요약
- SNMP는 장비 가용성, NetFlow는 세션 상세 분석, sFlow는 초고속 백본 저부하 관제에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Kafka Ingestion Buffer**: DDoS 공격이나 트래픽 폭증 시 초당 수십만 개의 UDP 플로우 패킷이 컬렉터로 쏟아질 때 패킷 유실을 방지하는 메시지 큐 완충 계층.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장비 시계 불일치로 **원인 추적 실패** | 전 장비 **NTP/PTP 동기화** | 이벤트 상관 분석 **신뢰성 확보** |
| 고속망 NetFlow로 **CPU 부하 증가** | **sFlow 샘플링** 또는 Sampled NetFlow 전환 | 포워딩 성능 저하 방지 |
| 폭주 시 UDP 유실로 **통계 왜곡** | **Kafka 완충**과 Collector 확장 | 플로우 수용 **복원력 확보** |
| SNMP v1/v2c 평문으로 **인증정보 노출** | **SNMP v3 인증·암호화** 적용 | 도청과 설정 변조 차단 |

#### 한줄 요약
- NTP 동기화, sFlow ASIC 가속, Kafka 완충 큐, SNMP v3 암호화로 운영한다.

## Ⅶ. 결론

- 단순 사후 장애 조치를 넘어 인프라 전반의 전방위적 가시성과 실시간 트래픽 패턴을 분석하는 **엔터프라이즈 및 IDC 네트워크 운영 관제(NMS)와 보안 위협 탐지의 핵심 표준 기술**로 확립되었으며, 주기적 폴링을 탈피하여 장비 변경 사항을 이벤트 기반으로 스트리밍하는 gNMI/gRPC 스트리밍 텔레메트리 및 AIOps 기반 이상 감지로 진화하는 가운데, 실무 모니터링 파이프라인 구축 시에는 **취약한 SNMP v1/v2c 평문 통신을 배제하고 HMAC-SHA/AES 암호화를 지원하는 SNMP v3 의무화, 초고속 코어망의 CPU 부하를 방지하기 위한 ASIC 기반 sFlow/Sampled NetFlow 채택, 이벤트 상관 분석의 정합성을 보장하는 전 장비 PTP/NTP 정밀 시각 동기화, 트래픽 폭주 시 플로우 유실을 방지하는 Kafka 완충 큐 연동**을 결합하여 완벽한 인프라 관측성(Observability)을 완성

#### 한줄 요약
- SNMP 상태 감시와 NetFlow/sFlow 세션 분석을 NTP 기반으로 결합하여 지능형 네트워크 AIOps를 구현한다.
