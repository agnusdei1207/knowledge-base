---
sidebar:
  order: 39
  label: "039. 5G 네트워크 슬라이싱"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G 종단간 네트워크 슬라이싱 (5G Network Slicing)"
date: "2026-08-26T13:47:15+09:00"
tags:
  - "notes-network"
weight: 39
extra:
  question_no: "39"
  source_status: "기출"
  source_history: "126회, 137회"
  priority: 70
  priority_note: "E2E(RAN-Transport-Core) 슬라이싱, NSSF, S-NSSAI 및 자원 격리(Hard vs Soft)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Network Slicing (네트워크 슬라이싱)**: 단일 물리 5G 인프라를 NFV/SDN을 통해 논리 분할하여 서비스별(SLA)로 격리된 가상망을 제공하는 기술.
- **SLA (Service Level Agreement)**: 가용성, 지연 시간(Latency), 패킷 손실률, 대역폭 처리량에 대해 사업자와 고객 간에 체결하는 정량적 성능 보장 계약.

</details>

- 정의/개념: 무선(RAN), 전송(Transport), 코어(5GC) 전 구간에 걸쳐 서비스 유형별(**eMBB, URLLC, mMTC**) 맞춤 가상망을 동적 생성·격리하는 **5G 핵심 가상화 기술**
- 배경/필요성: 단일 공용 통신망의 한계로 인한 **트래픽 폭증 시 상호 간섭 발생, 자율주행(URLLC 1ms)과 미디어(eMBB 20Gbps)의 독립적 SLA 보장 불가**

#### 한줄 요약
- RAN-Transport-Core 전 구간을 가상화하여 서비스 요구사항별 독립 가상망을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **E2E Orchestration**: CSMF(고객 서비스 관리)와 NSMF(슬라이스 관리)를 통해 단말부터 코어망까지 E2E 슬라이스를 자동 생성·배포하는 중앙 오케스트레이션.
- **Hard vs Soft Isolation**: 물리적 무선 PRB/FlexE 타임슬롯을 고정 분할하는 하드 격리와 가중치 큐잉 기반으로 동적 분배하는 소프트 격리.

</details>

- **종단간(E2E) 전 구간 격리**: 무선(RAN), 백홀 전송망(Transport), 코어망(5GC)을 유기적으로 연동하여 슬라이스 생성
- **다계층 자원 격리(Isolation)**: 특정 슬라이스(eMBB) 트래픽이 폭증해도 인접 슬라이스(URLLC)에 무영향 보장
- **소프트웨어 정의 라이프사이클 관리**: CSMF/NSMF 오케스트레이터를 통한 **온디맨드 자동 프로비저닝 및 동적 확장**

#### 한줄 요약
- E2E 전 구간 제어, 하드/소프트 다계층 자원 격리, 자동 확장 생애주기 관리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **S-NSSAI (Single NSSAI)**: SST(슬라이스/서비스 유형: eMBB 1, URLLC 2, mMTC 3)와 SD(슬라이스 구분자)로 구성된 32비트 글로벌 슬라이스 식별자.
- **NSSF (Network Slice Selection Function)**: 단말 접속 시 가입 정보와 요청 S-NSSAI를 분석하여 최적의 AMF 및 슬라이스 인스턴스를 지정하는 5GC 노드.

</details>

```text
[5G 네트워크 슬라이싱 구성]
|-- CSMF / NSMF
|-- NSSMF
|-- NSSF
|-- RAN 슬라이싱
`-- 전송망 슬라이싱
```

선의 의미: 계층 및 E2E 오케스트레이터가 도메인별 NSSMF를 통해 RAN, Transport, Core 인프라를 서비스별로 매핑하여 종단간 가상 파이프라인을 완성하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **CSMF / NSMF** | B2B 서비스 SLA를 접수하여 **E2E 네트워크 슬라이스 인스턴스(NSI)를 총괄 생성 및 수명주기 관리** | E2E 오케스트레이터 |
| **NSSMF (도메인 관리자)**| RAN, Transport, Core 각 도메인별 **하위 서브넷 슬라이스(NSSI)의 자원 할당 및 설정 제어** | 도메인별 관리자 |
| **NSSF (슬라이스 선택)** | 단말 접속 시 **S-NSSAI를 분석하여 최적의 AMF 인스턴스 및 슬라이스 세트 선택 매핑** | 5G Core NF |
| **RAN 슬라이싱 (gNB)** | 무선 물리 자원 블록(PRB)을 **슬라이스별로 전용 할당하거나 가변 뉴머롤로지로 스케줄링** | 무선 자원 격리 |
| **전송망 슬라이싱** | **FlexE(Flexible Ethernet) 타임슬롯 분할 및 SRv6 기반 QoS 보장 터널링** | 전송망 분할 |

#### 한줄 요약
- CSMF/NSMF, 도메인 NSSMF, NSSF, RAN/Transport/Core 파티셔닝 기술이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Closed-Loop Assurance (폐루프 자원 보증)**: NWDAF(네트워크 데이터 분석)가 슬라이스 지표를 실시간 분석하여 SLA 위반 위험 시 자동으로 자원을 스케일아웃하는 루프.

</details>

```text
5G E2E 네트워크 슬라이스 생성 및 세션 매핑 파이프라인
        │
   1. [SLA 요구사항 접수] CSMF가 B2B 고객의 대역폭/지연 SLA 요구 접수
        │
   2. [슬라이스 템플릿 생성] NSMF가 E2E 템플릿(NEST)을 생성하고 도메인별 NSSMF에 하달
        │
   3. [다중 도메인 자원 프로비저닝]
      • RAN: gNB 무선 PRB 하드 예약
      • Transport: FlexE / SRv6 전송 터널 구성
      • Core: 컨테이너 기반 전용 UPF/SMF 인스턴스 기동
        │
   4. [단말 접속 및 세션 매핑] NSSF가 S-NSSAI 식별자를 검증하고 전용 슬라이스에 바인딩
        │
   ▼
5. [NWDAF AI 폐루프 보증] 실시간 SLA 모니터링 및 트래픽 폭증 시 자동 Auto-scaling
```

#### 한줄 요약
- SLA 요구사항 접수 → 슬라이스 템플릿 생성 → 다중 도메인 자원 프로비저닝 → 단말 접속 및 세션 매핑 → NWDAF AI 폐루프 보증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hard Slicing vs Soft Slicing**: 물리 PRB/타임슬롯을 물리 고정 할당하는 완전 격리(Hard)와 가중치 큐잉 기반 동적 분배(Soft).

</details>

| 비교 항목 | 전통적 QoS 우선순위 제어 (DiffServ) | 5G 네트워크 슬라이싱 (E2E Slicing) |
|:---|:---|:---|
| **제어 적용 범위** | 홉별(Per-Hop) 라우터/스위치 국소 구간 | **단말부터 코어망까지 E2E 전 구간 통합 제어** |
| **자원 격리 수준** | 논리적 큐 우선순위 (전체 트래픽 폭주 시 침범)| **물리/논리적 자원 완전 격리 (No Interference)** |
| **SLA 보장 수준** | 상대적 우선순위 (Best-Effort 기반 한계) | **결정론적 초저지연(1ms) 및 대역폭 100% 보장** |
| **오케스트레이션** | 네트워크 장비별 CLI/QoS 정책 수동 설정 | **CSMF/NSMF 기반 온디맨드 자동 프로비저닝** |
| **주요 대표 용도** | 단순 웹/음성 트래픽 우선순위 차등 | **자율주행(V2X), 스마트 팩토리, 원격 의료, 특화망**|

#### 한줄 요약
- 단순 홉별 QoS 우선순위 제어를 넘어 전 구간 자원 격리와 자동 오케스트레이션을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PRB (Physical Resource Block)**: 5G 무선 구간에서 12개 부반송파와 1개 슬롯 단위로 구성되는 최소 무선 주파수-시간 자원 블록.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 eMBB 트래픽 폭증 시 무선 구간 간섭으로 URLLC 1ms 지연 초과 | 무선 **`PRB 하드 파티셔닝(Hard Reservation)` 및 선점형 스케줄링** | 무선 간섭 원천 차단 및 URLLC 1ms 지연 보증 |
| 슬라이스 내 급격한 트래픽 증가로 인한 가상 NF 과부하 및 SLA 위반 | **`NWDAF 연계 AI 폐루프(Closed-Loop) 오케스트레이션` 적용** | 부하 발생 전 선제적 자원 증설(Auto-scaling) |
| 공용 슬라이스 침해 시 인접 핵심 산업 슬라이스로의 횡적 침투 위협 | 슬라이스 간 **`IPsec/mTLS 격리 터널링` 및 독립 UDM/AUSF 인증** | 슬라이스 간 침해 전파 차단 및 제로 트러스트 달성 |
| 수백 개 슬라이스 운영 시 도메인 간 오케스트레이션 복잡도 증가 | **`3GPP 표준 NEST (Network Slice Template)` 및 자동화 파이프라인** | 배포 시간 수 주에서 수 분으로 단축 |

#### 한줄 요약
- PRB 하드 파티셔닝, NWDAF 폐루프 제어, IPsec/독립 인증, NEST 표준 템플릿으로 운영한다.

## Ⅶ. 결론

- 결정론적 SLA는 **하드 슬라이싱**, 탄력 효율은 **소프트 슬라이싱** 선택

#### 한줄 요약
- 5G 네트워크 슬라이싱은 RAN-Transport-Core 전 구간을 가상화하여 서비스별 SLA를 100% 보장하는 차세대 핵심 통신 가상화 기술이다.
