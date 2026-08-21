---
sidebar:
  order: 116
  label: "116. 멀티캐스트 IGMP•PIM"
  badge:
    text: "기출 · 50%"
    variant: note
title: "IP 멀티캐스트 라우팅 및 그룹 제어 : IGMP 및 PIM (Multicast Routing Architecture)"
date: "2026-08-22T08:15:00+09:00"
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

- **IP 멀티캐스트(IP Multicast)**: 송신자가 단 1개의 패킷만을 송출하더라도, 네트워크 경로 상의 스위치와 라우터가 해당 멀티캐스트 그룹(Class D: 224.0.0.0/4)에 명시적으로 가입(Join)한 수신자 방향의 분기점에서만 패킷을 복제하여 전송하는 1:N 고효율 전송 기술.
- **IGMP(RFC 3376) & PIM(RFC 7761)**: 단말과 로컬 라우터 간의 그룹 가입/탈퇴를 관리하는 **호스트 제어 프로토콜(IGMP)** 과, 라우터들 간에 유니캐스트 라우팅 테이블을 참조하여 최적 분배 트리(SPT/RPT)를 구축하는 **멀티캐스트 라우팅 프로토콜(PIM)**.

</details>

- 정의/개념: 가입 호스트의 상태를 관리하는 **L2/L3 경계의 IGMP(Internet Group Management Protocol)** 와 라우터 간 분배 트리를 수립하는 **L3 PIM(Protocol Independent Multicast)** 및 **RPF(Reverse Path Forwarding)** 를 결합하여 대역폭 낭비 없이 실시간 미디어를 일대다 분배하는 **IP 멀티캐스트 네트워크 프레임워크**
- 배경/필요성: IPTV, 금융 시세 피드(Market Data), 대규모 실시간 화상 세미나에서 수만 명의 시청자에게 개별 유니캐스트(Unicast)로 중복 패킷을 전송할 때 발생하는 백본망 대역폭 고갈 및 서버 송신 부하 병목을 해소할 요구

#### 한줄 요약
- 단말은 IGMP로 그룹에 가입하고 라우터는 PIM과 RPF로 트리를 구성하여 분기점에서만 패킷을 복제 전송한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RPF(Reverse Path Forwarding) 검사**: 멀티캐스트 라우팅 루프 및 중복 복제를 방지하기 위해, 패킷의 송신지 IP(Source IP)로 향하는 유니캐스트 최적 경로의 인바운드 인터페이스로 인입된 패킷만 정상 수용하고 타 인터페이스로 들어온 패킷은 즉시 폐기(Drop)하는 검증 메커니즘.
- **공유 트리(RPT / Shared Tree) vs 최단 경로 트리(SPT / Shortest Path Tree)**: RP(Rendezvous Point)를 중심으로 형성되는 `(*, G)` 공유 트리와, 송신원(Source)으로부터 수신자까지 직접 최단 경로로 연결되는 `(S, G)` 소스 트리.

</details>

- **네트워크 링크 대역폭 극적 절감**: 수신자 수($N$)와 무관하게 공통 백본 링크에서는 항상 단 1개의 멀티캐스트 스트림만 점유
- **프로토콜 독립적 라우팅 (Protocol Independent)**: OSPF, BGP, IS-IS 등 기존 유니캐스트 라우팅 프로토콜의 RIB를 그대로 활용하여 RPF 검사 및 트리 수립
- **L2 스위치 레벨 브로드캐스트 범람 차단 (IGMP Snooping)**: L2 스위치가 IGMP Join/Leave 프레임을 엿듣고(Snoop) 실제 가입 포트로만 패킷을 하드웨어 포워딩

#### 한줄 요약
- 백본 대역폭 절감, 유니캐스트 독립적 RPF 검사, SPT/RPT 분배 트리, IGMP Snooping을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **집결점(Rendezvous Point, RP)**: PIM-SM(Sparse Mode) 환경에서 송신원(Source)의 등록 패킷(Register)과 수신자의 가입 요청(Join)이 최초로 만나는 중앙 중계 라우터.
- **SSM(Source-Specific Multicast, RFC 4607)**: 복잡한 RP와 공유 트리를 배제하고, 수신자가 송신원의 IP와 그룹 IP를 함께 지정하여 `(S, G)` 최단 경로 트리를 직접 수립하는 진화된 멀티캐스트 방식 (232.0.0.0/8 대역).

</details>

```text
[ 멀티캐스트 송신원 (Source: 192.168.1.10) ]
                       │ (1. Multicast Packet 전송: Group 239.1.1.1)
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ PIM 라우팅 도메인 (PIM-SM / PIM-SSM Core Network) ]                   │
│  ├─ RPF (Reverse Path Forwarding) 검증 엔진 ── (루프 방지)               │
│  ├─ 집결점 (RP: Rendezvous Point) ── (PIM-SM 공유 트리 `(*, G)` 중심)    │
│  └─ SPT (Shortest Path Tree) 스위치오버 ── (대용량 트래픽 최단 경로 `(S, G)`)│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. PIM Join/Prune 분기 복제)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ L2/L3 라스트 마일 접속망 (Access Switch & Gateway) ]                  │
│  ├─ IGMPv3 라우터 (Query / Report 관리)                                 │
│  └─ L2 스위치 IGMP Snooping 테이블 ── (가입 포트 1, 3번에만 패킷 복제)   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (3. 선택적 복제 스트림 전달)
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
         [ 수신 단말 A (Host 1) ]          [ 수신 단말 B (Host 2) ]
```

선의 의미: 송신원이 보낸 단일 패킷이 PIM 코어망의 RPF 검증과 분배 트리를 거쳐, L2 스위치의 IGMP Snooping을 통해 실제 가입 단말로만 선택 복제되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **IGMP (단말-라우터)** | IGMPv2/v3 Membership Report 및 Leave Group 메시지로 로컬 가입자 관리 | RFC 3376 |
| **PIM-SM 라우터** | 수신자 요청 시에만 트래픽을 당겨오는(Pull) Sparse Mode 분배 트리 수립 | RFC 7761 |
| **집결점 (RP)** | PIM-SM에서 송신원 등록(Register)과 수신자 가입(Join)을 중계하는 앵커 포인트 | Auto-RP / BSR |
| **RPF 검증 엔진** | 유니캐스트 라우팅 테이블(FIB)을 대조하여 역방향 적합 인터페이스 패킷만 수용 | Loop-Free Engine |
| **IGMP Snooping** | L2 스위치 ASIC이 멀티캐스트 MAC(01:00:5e:xx:xx:xx) 테이블을 동적 필터링 | L2 Optimization |

#### 한줄 요약
- IGMP 가입자 관리, PIM-SM/SSM 트리 라우터, RP 중계점, RPF 루프 검증기, IGMP Snooping 스위치가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SPT 스위치오버(SPT Switchover)**: PIM-SM에서 수신 측 라우터가 최초에는 RP를 경유하는 공유 트리`(*, G)`로 패킷을 받다가, 트래픽 임계치를 초과하면 송신원으로 직접 최단 경로를 연결하는 소스 트리`(S, G)`로 자동 전환하는 최적화 프로세스.

</details>

```text
1. 수신 단말이 IPTV 채널 시청을 위해 'IGMPv3 Membership Report (Group: 239.1.1.1)' 전송
            │
            ▼
2. L2 스위치가 IGMP Snooping으로 단말 포트를 등록하고, 상류 로컬 라우터(DR)로 IGMP 프레임 전달
            │
            ▼
3. 라우터(DR)가 PIM Join 메시지를 상류 RP 방향으로 홉 바이 홉 전송 ➔ 공유 트리 `(*, G)` 구축
            │
            ▼
4. 송신원이 방송 스트림 송출 ➔ RP를 거쳐 RPF 검사를 통과한 패킷이 수신 라우터로 인입
            │
            ▼
5. [대역폭 임계치 초과 시] ➔ 수신 라우터가 송신원(Source)으로 직접 PIM Join 전송 (SPT Switchover)
            │
            ▼
6. 최단 경로 `(S, G)` 트리 확립 ➔ RP 경유 제거 및 초저지연 패킷 스트리밍 완수
```

**동작 원리**

1. **로컬 그룹 등록**: 단말이 IGMP 리포트를 송출하여 로컬 라우터에 수신 의사 전달
2. **트리 상향 확장**: 로컬 라우터가 상류 라우터들로 PIM Join을 전파하여 분기 경로 활성화
3. **RPF 무결성 검증**: 각 라우터가 패킷 인입 포트의 유니캐스트 역방향 경로 일치 여부 확인
4. **선택적 분기 복제**: 라우터 출력 인터페이스 목록(OIL: Outgoing Interface List)에만 사본 전송
5. **최단 경로 전환**: 패킷 수신율이 높아지면 RP 홉을 우회하고 송신원 직결 SPT로 전환하여 지연 최소화

#### 한줄 요약
- IGMP 가입, PIM 공유 트리 수립, RPF 검증 통과, SPT 스위치오버, 로컬 선택 복제 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PIM-SM vs PIM-SSM vs PIM-DM**: 명시적 가입 희소 모드(SM), 송신원 지정 간소화 모드(SSM), 플러딩 후 프룬 밀집 모드(DM)의 비교.

</details>

| 비교 항목 | PIM-SM (Sparse Mode) | PIM-SSM (Source-Specific) | PIM-DM (Dense Mode) |
|:---|:---|:---|:---|
| **트리 구축 방식** | **명시적 가입 (Pull: `(*,G)` ➔ `(S,G)`)**| **송신원 직결 가입 (Pull: `(S,G)` Only)**| **전역 범람 후 가지치기 (Push: Flood & Prune)** |
| **집결점 (RP) 필요성** | **필수 (RP 구성 및 이중화 관리 요구)** | **불필요 (RP 제거로 구조 단순화)** | **불필요 (전체 플러딩 기반)** |
| **IGMP 프로토콜 버전** | IGMPv2 / IGMPv3 호환 | **IGMPv3 필수 (Include Source 지원)** | IGMPv1 / IGMPv2 |
| **네트워크 부하** | 낮음 (가입자 경로에만 전송) | **최저 (최단 경로 즉시 직결)** | **매우 높음 (주기적 전역 플러딩 발생)** |
| **주요 적용 영역** | 기업 인트라넷, 임의 송신원 다자 화상 | **IPTV 방송망, 대규모 금융 시세 피드**| 소규모 폐쇄망, 테스트 환경 (현재 미사용) |

#### 한줄 요약
- PIM-SM은 범용 풀 모델(RP 필요), PIM-SSM은 IPTV/금융 특화 최단 직결 모델(RP 불필요), PIM-DM은 레거시 플러딩 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RP 단일 장애점(SPOF)**: PIM-SM 환경에서 RP 라우터가 다운될 경우 신규 멀티캐스트 그룹 탐색 및 세션 수립이 전면 중단되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| L2 스위치가 멀티캐스트를 브로드캐스트로 취급하여 **비가입 PC들로 패킷이 범람(Flooding)하는 장애** | 스위치 전 포트에 **IGMP Snooping 및 IGMP Querier 활성화** | 가입 포트로만 하드웨어 포워딩 제한 및 L2 네트워크 대역폭 90% 보존 |
| PIM-SM 핵심 앵커인 RP 라우터 단일 장애(SPOF) 시 **전사 멀티캐스트 방송 전면 중단** | **Anycast RP (RFC 4610 MSDP / PIM Anycast RP) 이중화** 구성 | RP 장애 시 1초 내 자동 우회 및 100% 무중단 서비스 연속성 확보 |
| 비대칭 라우팅(Asymmetric Routing) 환경에서 유니캐스트 경로 불일치로 인한 **RPF 실패 및 패킷 드롭** | 멀티캐스트 전용 정적 **M-Route(Multicast Static Route) 구성 또는 PIM 인터페이스 정렬** | RPF 검사 100% 정상 통과 및 비정상 패킷 폐기 원천 해결 |

#### 한줄 요약
- IGMP Snooping으로 L2 범람을 막고, Anycast RP로 가용성을 확보하며, M-Route로 RPF 실패를 해결한다.

## Ⅶ. 결론

- 대용량 미디어 스트리밍 및 실시간 금융 데이터 전송의 인프라 효율성을 극대화하기 위해 **IP 멀티캐스트 아키텍처**는 핵심 전송 메커니즘으로 운용되고 있으며, 실무 구축 시 **단순하고 효율적인 PIM-SSM 및 IGMPv3 전환**, **Anycast RP 기반 고가용성 설계**, **L2 IGMP Snooping 및 RPF 경로 정합성 검증**을 통합 구현하여 대규모 고신뢰 일대다 전송망을 완성

#### 한줄 요약
- IGMPv3와 PIM-SSM/SM 및 Anycast RP 이중화를 결합하여 고효율 무중단 멀티캐스트 스트리밍을 실현한다.
