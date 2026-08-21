---
sidebar:
  order: 39
  label: "039. 5G 네트워크 슬라이싱 (5G Network Slicing)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G 종단간 가상화 격리 기술 : 네트워크 슬라이싱 (Network Slicing)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 39
extra:
  question_no: "039"
  source_status: "기출"
  source_history: "126회, 137회"
  priority: 70
  priority_note: "E2E(RAN-Transport-Core) 슬라이싱, NSSF, S-NSSAI 및 자원 격리(Hard vs Soft)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 슬라이싱(Network Slicing)**: 단일 물리적 5G 네트워크 인프라를 NFV(네트워크 기능 가상화)와 SDN(소프트웨어 정의 네트워킹)을 통해 논리적으로 분할하여, 서비스 요구사항(SLA)별로 완전히 격리된 종단간(End-to-End) 가상 네트워크를 제공하는 기술.
- **서비스 수준 협약(Service Level Agreement, SLA)**: 통신 서비스의 가용성, 지연 시간(Latency), 패킷 손실률, 대역폭 처리량에 대해 사업자와 가입자 간에 합의한 정량적 성능 보장 계약.

</details>

- 정의/개념: 무선 접속망(RAN), 전송망(Transport), 코어망(5GC) 전 구간에 걸쳐 서비스 유형별(**eMBB, URLLC, mMTC**) 성능 지표에 맞춤화된 독립 논리 네트워크를 동적으로 생성·격리하는 **5G 핵심 가상화 아키텍처**
- 배경/필요성: 단일 공용 인프라에서 발생하는 트래픽 경합을 차단하고, 초고속 대용량 비디오, 1ms 초저지연 자율주행, 대규모 저전력 IoT 센서의 상충하는 요구조건을 동시 충족할 필요성

#### 한줄 요약
- 단일 물리망을 RAN부터 Core까지 E2E 가상화하여 서비스별 전용 SLA를 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **종단간 오케스트레이션(E2E Orchestration)**: 서비스 요구사항을 분석하여 무선망(RAN), 전송망(Transport), 코어망(Core)의 개별 슬라이스 관리자(NSSMF)를 통합 지휘하고 가상 자원을 자동 프로비저닝하는 상위 프레임워크.
- **자원 격리(Resource Isolation)**: 특정 슬라이스에서 트래픽 폭주나 장애가 발생하더라도 인접한 타 슬라이스의 대역폭, CPU, 메모리, 지연 시간 품질에 전혀 영향을 미치지 않도록 물리적/논리적으로 자원을 보호하는 속성.

</details>

- **전 구간(E2E) 논리적 파티셔닝**: 단말 $\leftrightarrow$ gNB(RAN) $\leftrightarrow$ 백홀/프론트홀(IP/MPLS/FlexE) $\leftrightarrow$ 5GC(Core)에 이르는 전 경로 독립 슬라이스 매핑
- **엄격한 다계층 자원 격리**: 하드 슬라이싱(물리적 무선 자원/전송 타임슬롯 고정) 및 소프트 슬라이싱(가상 큐/QoS 가중치 제어)을 통한 SLA 상호 침범 차단
- **동적 생애주기 관리(Lifecycle Management)**: 서비스 수요에 따른 슬라이스의 실시간 생성(Instantiate), 수정(Modify), 자동 확장(Scale), 폐기(Terminate)

#### 한줄 요약
- E2E 전 구간 제어, 하드/소프트 다계층 자원 격리, 자동 확장 생애주기 관리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **단일 네트워크 슬라이스 선택 지원 정보(S-NSSAI)**: 슬라이스 서비스 유형(SST, 예: eMBB 1, URLLC 2, mMTC 3)과 슬라이스 구분자(SD)로 구성된 32비트 글로벌 슬라이스 식별자.
- **네트워크 슬라이스 선택 기능(Network Slice Selection Function, NSSF)**: 단말이 접속할 때 가입 정보(UDM)와 요청 S-NSSAI를 대조하여 최적의 AMF 및 슬라이스 인스턴스를 지정하는 5GC 코어 노드.

</details>

```text
[ 서비스 관리 오케스트레이션 (CSMF / NSMF) ]
   │ (E2E 슬라이스 프로파일 정의 및 SLA 라이프사이클 관리)
   ├───────────────────────────────┬───────────────────────────────┐
   ▼ (무선 도메인)                 ▼ (전송 도메인)                 ▼ (코어 도메인)
[ RAN NSSMF ]                   [ Transport NSSMF ]             [ Core NSSMF ]
   │ (PRB 파티셔닝)                │ (FlexE / SRv6 터널링)          │ (NFV 가상 인스턴스)
   ▼                               ▼                               ▼
[ 5G gNB (RAN) ] ──────────▶ [ 전송망 (Transport) ] ──────────▶ [ 5G 코어 (5GC) ]
 ├─ eMBB 무선 슬라이스 ─────── ├─ eMBB 고대역폭 터널 ──────── ├─ 중앙 고용량 UPF
 ├─ URLLC 미니슬롯 슬라이스 ── ├─ URLLC 저지연 전용 타임슬롯 ── ├─ 로컬 MEC / 전진 UPF
 └─ mMTC 협대역 슬라이스 ───── └─ mMTC 최선형 대역 ────────── └─ C-Plane 최적화 코어
```

선의 의미: E2E 오케스트레이터가 도메인별 NSSMF를 통해 RAN, Transport, Core 인프라를 서비스별로 매핑하여 종단간 가상 파이프라인을 완성하는 아키텍처

| 구성요소 | 책임 | 3GPP 표준 엔티티 |
|:---|:---|:---|
| **CSMF / NSMF** | 통신 서비스 요구사항(SLA)을 접수하여 E2E 네트워크 슬라이스 인스턴스(NSI)를 총괄 배포 | E2E 오케스트레이터 |
| **NSSMF (도메인 관리자)**| RAN, Transport, Core 각 도메인별 하위 서브넷 슬라이스(NSSI)의 자원 할당 및 설정 제어 | 도메인별 관리자 |
| **NSSF (슬라이스 선택)** | 단말의 접속 요청 시 가입자 프로파일(S-NSSAI)을 분석하여 서빙 AMF 및 슬라이스 세트 선택 | 5G Core NF |
| **RAN 슬라이싱 (gNB)** | 무선 물리 자원 블록(PRB)을 슬라이스별로 전용 할당하거나 가변 스케줄링 | 가변 뉴머롤로지 |
| **전송망 슬라이싱** | FlexE(Flexible Ethernet) 타임슬롯 분할 및 SRv6(Segment Routing) 기반 QoS 터널링 | 전송 백홀/프론트홀 |

#### 한줄 요약
- CSMF/NSMF, 도메인 NSSMF, NSSF, RAN/Transport/Core 파티셔닝 기술이 결합하여 E2E 슬라이스를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **폐루프 자원 제어(Closed-Loop Assurance)**: 네트워크 데이터 분석 기능(NWDAF)이 슬라이스 성능 지표를 실시간 모니터링하여 SLA 위반 징후 감지 시 오케스트레이터가 자동으로 자원을 증설하는 자율 제어 루프.

</details>

```text
1. B2B 고객의 SLA 요구사항(대역폭, 최대 지연, 가용성) 접수 (CSMF)
            │
            ▼
2. NSMF가 E2E 슬라이스 템플릿(NEST) 생성 ➔ 도메인별 NSSMF로 자원 분할 요청
            │
            ▼
3. 도메인별 자원 프로비저닝: gNB(PRB 분할) + 전송망(SRv6 정책) + 코어망(NFV UPF 인스턴스 기동)
            │
            ▼
4. E2E 슬라이스 바인딩 및 S-NSSAI 식별자 등록 ➔ 단말 세션 접속 및 트래픽 격리 전송
```

**동작 원리**

1. **슬라이스 템플릿 정의**: 서비스 요구조건을 표준 네트워크 슬라이스 템플릿(NEST) 파라미터로 변환
2. **다중 도메인 자원 할당**: RAN(PRB 예약), Transport(FlexE 채널), Core(가상 NF)를 동시 할당
3. **단말 매핑**: 단말이 요청한 S-NSSAI를 NSSF가 검증하고 전용 AMF/SMF/UPF 경로로 유도
4. **실시간 보증**: NWDAF가 슬라이스별 QoS를 지속 계측하고 부하 증가 시 자동 스케일아웃(Auto-scaling) 실행

#### 한줄 요약
- SLA 접수, 도메인별 자원 프로비저닝, S-NSSAI 기반 단말 세션 매핑, NWDAF 폐루프 품질 보증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **하드 슬라이싱(Hard Slicing)**: 물리적 주파수(PRB)나 전송 하드웨어 타임슬롯(FlexE)을 고정 할당하여 100% 완전 격리를 달성하는 방식.
- **소프트 슬라이싱(Soft Slicing)**: 물리 자원을 공유하면서 가중치 기반 우선순위 큐(WFQ, DiffServ)로 논리적 대역폭을 동적 분배하는 방식.

</details>

| 비교 항목 | 전통적 QoS 우선순위 제어 | 5G 네트워크 슬라이싱 (E2E) |
|:---|:---|:---|
| **제어 범위** | 홉별(Per-Hop) 라우터/스위치 국소 구간 | **단말부터 코어망까지 E2E 전 구간** |
| **자원 격리 수준** | 논리적 큐 우선순위 (전체 트래픽 폭주 시 침범) | **물리/논리적 자원 완전 격리 (No Interference)** |
| **SLA 보장성** | 상대적 우선순위 (Best-Effort 기반) | **결정론적 초저지연 및 대역폭 100% 보장** |
| **오케스트레이션** | 장비별 정적 CLI/QoS 정책 수동 설정 | **CSMF/NSMF 기반 자동 동적 프로비저닝** |
| **적용 시나리오** | 단순 웹/음성 트래픽 우선순위 차등 | **자율주행(V2X), 스마트 팩토리, 원격 수술, 특화망** |

#### 한줄 요약
- 단순 홉별 QoS 우선순위 제어를 넘어, 전 구간 자원 격리와 자동 오케스트레이션을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **무선 자원 블록(Physical Resource Block, PRB)**: 5G 무선 구간에서 12개 부반송파와 1개 슬롯 단위로 구성되는 최소 주파수-시간 무선 자원 단위.
- **슬라이스 간 횡적 이동(Lateral Movement)**: 공격자가 보안이 취약한 공용 슬라이스를 침해한 후 내부 가상화망을 타고 핵심 제어 슬라이스로 침투하는 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 eMBB 트래픽 폭증 시 무선 구간 간섭으로 URLLC 1ms 지연 초과 | 무선 **PRB 하드 파티셔닝(Hard PRB Reservation)** 및 선점형 스케줄링 적용 | 무선 구간 트래픽 간섭 원천 차단 및 1ms 지연 보증 |
| 슬라이스 내 급격한 트래픽 증가로 인한 가상 NF 과부하 및 SLA 위반 | **NWDAF 연계 AI 폐루프(Closed-Loop) 오케스트레이션** 적용 | 부하 발생 전 사전 선제적 자원 증설(Auto-scaling) |
| 공용 슬라이스 침해 시 인접 핵심 산업 슬라이스로의 횡적 침투 위협 | 슬라이스 간 **IPsec/mTLS 격리 터널링** 및 독립 UDM/AUSF 인증 분리 | 슬라이스 간 침해 전파 차단 및 제로 트러스트 보안 확립 |

#### 한줄 요약
- PRB 하드 파티셔닝으로 간섭을 방지하고, Closed-Loop 오케스트레이션으로 SLA를 유지하며, IPsec/독립 인증으로 슬라이스 보안을 확보한다.

## Ⅶ. 결론

- 차세대 5G/6G 통신 인프라의 수익성과 서비스 품질을 극대화하기 위해 **E2E 네트워크 슬라이싱**을 표준 아키텍처로 채택하되, 무선(RAN)의 **PRB 하드 격리**, 전송망의 **FlexE/SRv6**, 코어망의 **SBA 가상화**를 통합 제어하는 **NSMF 오케스트레이터**와 **NWDAF 기반 자율 보증 체계**를 구축하여 고신뢰 다중 테넌트 네트워크를 완성

#### 한줄 요약
- RAN-Transport-Core 전 구간 자원 격리와 AI 자율 오케스트레이션으로 맞춤형 5G 네트워크를 실현한다.
