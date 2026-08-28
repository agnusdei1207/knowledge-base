---
sidebar:
  order: 116
  label: "116. 멀티캐스트 IGMP•PIM"
  badge:
    text: "기출 · 50%"
    variant: note
title: "IP 멀티캐스트 라우팅 및 그룹 제어 : IGMP 및 PIM"
date: "2026-08-26T14:16:00+09:00"
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

- 정의/개념: **IGMP 가입·PIM 트리** 기반 1:N 전송 기술
- 배경/필요성: 동일 콘텐츠를 유니캐스트로 보내면 수신자 수만큼 **송신원과 백본의 복제 전송 비용**이 곱해지므로, 복제 지점을 분기 라우터로 내려 링크마다 사본이 1개만 흐르게 함

#### 한줄 요약
- IGMP 그룹 관리와 PIM 분배 트리를 통해 가입자 분기점에서만 패킷을 복제 전송한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RPF (Reverse Path Forwarding) Check**: 인입된 멀티캐스트 패킷의 송신지 IP에 대해 유니캐스트 최적 역방향 인터페이스와 일치하는지 검사하여 루프를 원천 방지하는 메커니즘.
- **IGMP Snooping**: L2 스위치가 IGMP Join/Leave 패킷을 감청하여 멀티캐스트 트래픽을 실제 가입 포트로만 선별 전달하는 기술.

</details>

- 분기점 복제로 **송신원·백본 대역폭 절감**
- **RPF 검사**로 잘못된 인입 인터페이스 패킷 폐기
- **IGMP Snooping**으로 가입 포트만 선택 전달

#### 한줄 요약
- 대역폭 절감, RPF 기반 루프 방지, IGMP Snooping을 통한 L2 플러딩 방지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Rendezvous Point (RP, 집결점)**: PIM-SM에서 송신원 등록과 수신자 가입을 중계하는 중앙 기준 라우터.

</details>

```text
IP Multicast
|-- IGMP
|-- PIM Router
|-- RP
|-- RPF Engine
`-- IGMP Snooping
```

선의 의미: 송신원이 보낸 단일 패킷이 PIM 코어망의 RPF 검증과 분배 트리를 거쳐 L2 스위치의 IGMP Snooping을 통해 실제 가입 단말로만 선택 복제되는 구조

| 구성요소 | 책임 |
|:---|:---|
| **IGMP** | 호스트-라우터 간 그룹 가입 관리 |
| **PIM Router** | 라우터 간 분배 트리 구성 |
| **RP** | PIM-SM 송신원 등록과 가입 중계 |
| **RPF Engine** | 유니캐스트 FIB 기반 인입 경로 검사 |
| **IGMP Snooping** | L2 가입 포트 선택 전달 |

#### 한줄 요약
- IGMP가 말단 가입 정보를, PIM이 그 정보를 상류로 잇는 분배 트리를 맡으므로, 패킷 복제는 트리가 갈라지는 지점에서만 발생한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SPT Switchover**: PIM-SM에서 RP를 경유하는 공유 트리`(*, G)`로 패킷을 받다가 대역폭 임계치 초과 시 송신원 직결 소스 트리`(S, G)`로 자동 전환하는 기법.

</details>

```text
IGMP 가입, PIM 공유 트리 구축, RPF 검증 및 SPT 전환 파이프라인
        │
       [IGMP 그룹 가입]
        │
   1. [IGMP Snooping 등록]
        │
   2. [PIM 공유 트리 구축]
        │
   3. [RPF 검사 및 RP 경유 전송]
        │
   ▼
   4. [SPT 스위치오버]
```

- 1. IGMP Snooping 등록
- 2. PIM 공유 트리 구축
- 3. RPF 검사 및 RP 경유 전송
- 4. SPT 스위치오버

#### 한줄 요약
- 공유 트리에서 최단 경로 트리로 넘어가는 지점에서 RP 경유 지연과 라우터가 보관할 상태량이 맞바뀐다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PIM-SM** vs **PIM-SSM** vs **PIM-DM**.

</details>

| 비교 항목 | PIM-SM (Sparse Mode) | PIM-SSM (Source-Specific) | PIM-DM (Dense Mode) |
|:---|:---|:---|:---|
| 트리 구축 | `(*,G)` 후 `(S,G)` 전환 | `(S,G)` 직접 가입 | 범람 후 가지치기 |
| RP 필요 | 필요 | 불필요 | 불필요 |
| IGMP 조건 | v2·v3 | **v3 Source Include** | v1·v2 |
| 초기 부하 | 가입 경로만 전송 | 송신원별 가입 경로 | **전역 범람** 가능 |
| 주요 적용 | ASM 기업망 | **SSM 방송·시세** | 소규모 밀집 수신망 |

#### 한줄 요약
- PIM-SM은 범용 풀 모델(RP 필요), PIM-SSM은 IPTV/금융 특화 최단 직결 모델(RP 불필요), PIM-DM은 레거시 플러딩 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Anycast RP (RFC 4610)**: 복수의 RP 라우터에 동일한 Anycast IP를 부여하고 MSDP로 소스를 동기화하여 무중단 고가용성을 보장하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비가입 포트로 **멀티캐스트 범람** | **IGMP Snooping·Querier** | 가입 포트만 전달 |
| RP 단일 장애로 방송 중단 | **Anycast RP** 이중화 | RP 장애 영향 완화 |
| 비대칭 경로로 **RPF 실패** | 정적 **M-Route** 또는 경로 정렬 | 인입 경로 정합성 확보 |
| 비인가 소스·그룹 가입 | **PIM Boundary·IGMP ACL** | 허용 범위 제한 |

#### 한줄 요약
- IGMP Snooping으로 L2 범람을 막고, Anycast RP로 가용성을 확보하며, M-Route로 RPF 실패를 해결한다.

## Ⅶ. 결론

- 송신원 지정 서비스는 **PIM-SSM**, ASM은 **PIM-SM** 선택

#### 한줄 요약
- IP 멀티캐스트는 IGMPv3와 PIM-SSM/SM 및 Anycast RP 이중화를 결합하여 고효율 무중단 1:N 스트리밍을 실현하는 핵심 네트워크 기술이다.
