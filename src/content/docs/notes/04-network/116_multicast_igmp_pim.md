---
sidebar:
  order: 116
  label: "116. 멀티캐스트 IGMP•PIM"
  badge:
    text: "기출 · 50%"
    variant: note
title: "IP 멀티캐스트 라우팅 및 그룹 제어 : IGMP 및 PIM"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 116
extra:
  question_no: "116"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "호스트-라우터 간 IGMPv1/v2/v3, 라우터 간 PIM-SM/PIM-SSM, RPF(Reverse Path Forwarding) 루프 방지, IGMP Snooping"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IP Multicast**: 송신자가 단 1개의 패킷만 송출해도 분기점 라우터가 명시적 가입자 방향으로만 패킷을 복제 전송하는 1:N 전송 기술.
- **IGMP vs PIM**: 단말-로컬 라우터 간 그룹 가입/탈퇴를 관리하는 IGMP와 라우터 간 최적 분배 트리를 수립하는 PIM.

</details>

- 정의/개념: 단말-라우터 간 그룹 가입(IGMP)과 라우터 간 분배 트리(PIM)를 결합하여 **가입자 경로 분기점에서만 패킷을 복제 전송하는 1:N 통신 기술**
- 배경/필요성: 대규모 라이브 방송 시 유니캐스트 중복 전송으로 인한 **송신 서버 부하 폭증, 백본 대역폭 고갈 및 브로드캐스트의 전역 네트워크 마비**

#### 한줄 요약
- IGMP 그룹 관리와 PIM 분배 트리를 통해 가입자 분기점에서만 패킷을 복제 전송한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RPF (Reverse Path Forwarding) Check**: 인입된 멀티캐스트 패킷의 송신지 IP에 대해 유니캐스트 최적 역방향 인터페이스와 일치하는지 검사하여 루프를 원천 방지하는 메커니즘.
- **IGMP Snooping**: L2 스위치가 IGMP Join/Leave 패킷을 감청하여 멀티캐스트 트래픽을 실제 가입 포트로만 선별 전달하는 기술.

</details>

- **네트워크 대역폭 절감 및 서버 부하 극소화**: 수신자가 수만 명이어도 **송신원은 단 1개의 스트림만 송출하여 네트워크 효율 극대화**
- **RPF(Reverse Path Forwarding) 기반 루프 방지**: 유니캐스트 라우팅 테이블 역방향 검사를 통해 **멀티캐스트 루프를 원천 차단**
- **L2 계층 IGMP Snooping 최적화**: 스위치가 IGMP 리포트를 감청하여 **비가입 단말 포트로의 무차별 플러딩(Flooding) 방지**

#### 한줄 요약
- 대역폭 절감, RPF 기반 루프 방지, IGMP Snooping을 통한 L2 플러딩 방지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Rendezvous Point (RP, 집결점)**: PIM-SM에서 송신원 등록과 수신자 가입을 중계하는 중앙 기준 라우터.

</details>

```text
[IP 멀티캐스트 IGMP 및 PIM 라우팅 토폴로지]
|-- Multicast Source (송신 서버: 239.1.1.1 단일 스트림 송출)
`-- PIM Multicast Core Routers (PIM-SM / PIM-SSM)
    |-- RPF Verification Engine (유니캐스트 FIB 대조 역방향 루프 검사)
    |-- Rendezvous Point (RP: PIM-SM 공유 트리 (*, G) 중심점)
    `-- SPT Switchover Engine (대용량 트래픽 최단 경로 (S, G) 소스 트리 전환)
`-- Access Layer (Gateway Router & L2 Switch)
    |-- IGMPv3 Router (Membership Query / Report 관리)
    `-- L2 Switch IGMP Snooping Table (가입 단말 포트로만 선택적 하드웨어 복제)
`-- Receiver Hosts (IGMP Report 송출 및 IPTV 스트림 수신)
```

선의 의미: 송신원이 보낸 단일 패킷이 PIM 코어망의 RPF 검증과 분배 트리를 거쳐 L2 스위치의 IGMP Snooping을 통해 실제 가입 단말로만 선택 복제되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **IGMP (단말-라우터)** | IGMPv2/v3 Membership Report 및 **Leave 메시지로 로컬 가입자 관리** | RFC 3376 |
| **PIM-SM 라우터** | 수신자 요청 시에만 트래픽을 당겨오는 **Sparse Mode 분배 트리 수립** | RFC 7761 |
| **집결점 (RP)** | PIM-SM에서 **송신원 등록과 수신자 가입을 중계하는 앵커 포인트** | Auto-RP / BSR |
| **RPF 검증 엔진** | 유니캐스트 라우팅 테이블(FIB)을 대조하여 **역방향 적합 패킷만 수용** | Loop-Free Engine |
| **IGMP Snooping** | L2 스위치가 **멀티캐스트 MAC 테이블을 동적 필터링하여 선택 복제** | L2 Optimization |

#### 한줄 요약
- IGMP 가입자 관리, PIM-SM/SSM 트리 라우터, RP 중계점, RPF 루프 검증기, IGMP Snooping 스위치가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SPT Switchover**: PIM-SM에서 RP를 경유하는 공유 트리`(*, G)`로 패킷을 받다가 대역폭 임계치 초과 시 송신원 직결 소스 트리`(S, G)`로 자동 전환하는 기법.

</details>

```text
IGMP 가입, PIM 공유 트리 구축, RPF 검증 및 SPT 전환 파이프라인
        │
   1. [IGMP 그룹 가입] 수신 단말이 'IGMPv3 Membership Report(Group: 239.1.1.1)' 송출
        │
   2. [IGMP Snooping 등록] L2 스위치가 포트를 등록하고 상류 라우터(DR)로 IGMP 전달
        │
   3. [PIM 공유 트리 구축] 라우터가 PIM Join을 상류 RP 방향으로 전송하여 공유 트리 `(*, G)` 구축
        │
   4. [RP 경유 스트리밍] 송신원 트래픽이 RP를 거쳐 RPF 검사를 통과한 후 수신 라우터로 인입
        │
   ▼
5. [SPT 스위치오버] 대역폭 임계치 초과 시 송신원으로 직결 PIM Join 전송 ➔ 최단 경로 `(S, G)` 전환 완결
```

#### 한줄 요약
- IGMP 가입 → PIM 공유 트리 수립 → RPF 검증 통과 → SPT 스위치오버 → 로컬 선택 복제 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PIM-SM** vs **PIM-SSM** vs **PIM-DM**.

</details>

| 비교 항목 | PIM-SM (Sparse Mode) | PIM-SSM (Source-Specific) | PIM-DM (Dense Mode) |
|:---|:---|:---|:---|
| **트리 구축 방식** | **명시적 가입 (Pull: `(*,G)` ➔ `(S,G)`)**| **송신원 직결 가입 (Pull: `(S,G)` Only)**| **전역 범람 후 가지치기 (Push: Flood & Prune)**|
| **집결점 (RP) 필요성**| **필수 (RP 구성 및 이중화 관리 요구)** | **불필요 (RP 제거로 구조 단순화)** | **불필요 (전체 플러딩 기반)** |
| **IGMP 프로토콜 버전**| IGMPv2 / IGMPv3 호환 | **IGMPv3 필수 (Include Source 지원)** | IGMPv1 / IGMPv2 |
| **네트워크 부하** | 낮음 (가입자 경로에만 전송) | **최저 (최단 경로 즉시 직결)** | **매우 높음 (주기적 전역 플러딩 발생)** |
| **주요 적용 영역** | **기업 인트라넷, 다자 화상 회의** | **IPTV 방송망, 대규모 금융 시세 피드**| 소규모 폐쇄망, 레거시 테스트 환경 |

#### 한줄 요약
- PIM-SM은 범용 풀 모델(RP 필요), PIM-SSM은 IPTV/금융 특화 최단 직결 모델(RP 불필요), PIM-DM은 레거시 플러딩 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Anycast RP (RFC 4610)**: 복수의 RP 라우터에 동일한 Anycast IP를 부여하고 MSDP로 소스를 동기화하여 무중단 고가용성을 보장하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| L2 스위치가 멀티캐스트를 브로드캐스트로 취급하여 **비가입 단말로 패킷 범람** | **`스위치 전 포트에 IGMP Snooping 및 IGMP Querier 활성화`** | 가입 포트로만 포워딩 제한 및 L2 대역폭 90% 보존 |
| PIM-SM 앵커인 RP 라우터 단일 장애(SPOF) 시 **전사 멀티캐스트 방송 중단** | **`Anycast RP (RFC 4610 MSDP / PIM Anycast RP)` 이중화** 구성 | RP 장애 시 1초 내 자동 우회 및 무중단 연속성 확보 |
| 비대칭 라우팅 환경에서 유니캐스트 경로 불일치로 인한 **RPF 실패 및 패킷 드롭** | **`멀티캐스트 전용 정적 M-Route 구성` 또는 PIM 인터페이스 정렬** | RPF 검사 100% 정상 통과 및 패킷 폐기 원천 해결 |
| 비인가자가 임의의 멀티캐스트 트래픽을 주입하여 네트워크를 마비시키는 위협 | **스위치/라우터 포트에 `PIM Boundary 및 IGMP Join 필터링 ACL`** 적용 | 비인가 멀티캐스트 소스 및 불법 그룹 가입 원천 차단 |

#### 한줄 요약
- IGMP Snooping으로 L2 범람을 막고, Anycast RP로 가용성을 확보하며, M-Route로 RPF 실패를 해결한다.

## Ⅶ. 결론

- 대용량 미디어 스트리밍 및 실시간 금융 데이터 전송의 인프라 효율성을 극대화하기 위해 **IP 멀티캐스트 아키텍처를 핵심 전송 메커니즘으로 채택**하되, 실무 구축 시 **단순하고 효율적인 PIM-SSM 및 IGMPv3 전환, Anycast RP 기반 고가용성 설계, L2 IGMP Snooping 및 RPF 경로 정합성 검증**을 통합 구현하여 대규모 고신뢰 일대다 전송망 완성

#### 한줄 요약
- IP 멀티캐스트는 IGMPv3와 PIM-SSM/SM 및 Anycast RP 이중화를 결합하여 고효율 무중단 1:N 스트리밍을 실현하는 핵심 네트워크 기술이다.