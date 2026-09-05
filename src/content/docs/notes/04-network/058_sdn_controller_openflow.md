---
sidebar:
  order: 58
  label: "058. SDN 컨트롤러와 OpenFlow"
  badge:
    text: "기출 · 30%"
    variant: note
title: "SDN 제어 평면 : SDN 컨트롤러와 OpenFlow"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 58
extra:
  question_no: "58"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 30
  priority_note: "OpenFlow 1.3+ 파이프라인(Match-Action, Multi-Table), Packet-In/Out, Flow-Mod 및 보안 채널(TLS)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SDN Controller**: 분산 스위치의 제어 평면을 중앙 집중화하여 전역 토폴로지를 관리하고 흐름 규칙을 계산하는 핵심 두뇌.
- **OpenFlow Protocol**: 컨트롤러(제어)와 스위치(데이터) 간에 Flow Table 규칙을 추가·수정·삭제하는 표준 사우스바운드 인터페이스 (ONF).

</details>

- 정의/개념: 전역 토폴로지를 관리하는 SDN 컨트롤러와 Match-Action 파이프라인을 통해 스위치 TCAM에 룰을 프로그래밍하는 OpenFlow 표준 프로토콜
- 배경/필요성: 초기 SDN 환경에서 이종 네트워크 장비 제조사마다 서로 다른 독점(Proprietary) 제어 인터페이스와 관리 CLI를 제공함에 따라 벤더 종속성(Lock-in)이 심화되고, 중앙 컨트롤러가 물리 스위치 및 가상 스위치(OVS)의 하드웨어 포워딩 엔진을 표준화된 방식으로 직접 프로그래밍하지 못하는 한계를 극복하기 위해, 제어 평면의 중앙 SDN 컨트롤러와 데이터 평면의 스위치 간에 Match-Action 기반 다중 테이블 파이프라인(Multi-Table Pipeline)과 표준 메시지 규격을 정의한 OpenFlow(ONF) 프로토콜을 도입하여 하드웨어 추상화, 실시간 플로우 단위 동적 경로 제어(Flow-Mod/Packet-In) 및 벤더 독립적 사우스바운드 제어 표준화를 달성할 필요

#### 한줄 요약
- OpenFlow는 제어를 표준 추상으로 옮겨 벤더 종속을 끊는 대신, 플로우 규칙이 스위치 TCAM 용량에 갇히므로 규칙 세분화 정도와 수용 가능한 플로우 수가 서로를 제약한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-Table Pipeline**: Table 0번부터 순차적으로 파이프라인(Goto-Table) 처리를 수행하여 단일 테이블의 엔트리 폭증을 방지하는 구조.
- **TLS Secure Channel**: 컨트롤러와 스위치 간 통신을 TCP 6653 포트에서 상호 인증 TLS로 암호화하여 제어 평면을 보호하는 보안 링크.

</details>

- 다중 흐름 테이블(Multi-Table) 파이프라인: 0번 테이블부터 순차 검색(Goto-Table)하여 단일 테이블의 엔트리 폭증 방지
- 비동기 이벤트 기반 보고(Packet-In): 미지의 패킷(Table-Miss) 발생 시 스위치가 비동기적으로 컨트롤러에 패킷 보고
- TLS 보안 제어 채널: 컨트롤러와 스위치 간 상호 인증된 TLS(TCP 6653) 보안 채널을 통해 제어 평면 위변조 차단

#### 한줄 요약
- Packet-In으로 미지의 플로우를 컨트롤러에 올려 유연성을 얻지만 그 왕복이 곧 첫 패킷의 지연이 되므로, 규칙을 미리 심는 방식과 필요할 때 묻는 방식의 비율이 성능을 좌우한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Group Table vs Meter Table**: 멀티캐스트 복제 및 Fast-Failover를 처리하는 그룹 테이블과 대역폭 측정(Rate Limit)을 수행하는 미터 테이블.

</details>

```text
[SDN 제어 평면 구성]
|-- SDN 컨트롤러
|-- OpenFlow 채널
|-- 흐름 테이블
|-- 그룹 테이블
`-- 미터 테이블
```

선의 의미: TLS 보안 채널을 통해 제어 평면의 지시가 데이터 평면의 다중 테이블 파이프라인으로 적재되어 패킷을 처리하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SDN 컨트롤러** | 전역 토폴로지 분석, 최적 경로 계산, Flow-Mod 명령 생성 및 상태 모니터링 | 제어 평면 |
| **OpenFlow 채널** | 컨트롤러와 스위치 간 메시지(대칭형/비동기/동기)를 교환하는 보안 링크 | TLS / TCP 6653 |
| 흐름 테이블 (Flow Table)| 매칭 필드와 액션 인스트럭션을 저장하여 **라인 레이트 패킷 스위칭 수행** | TCAM 메모리 |
| 그룹 테이블 (**Group Table**)| 플러딩, 멀티캐스트 복제, 링크 단선 시 즉각 우회(Fast-Failover) 처리 | L2/L3 다중화 |
| 미터 테이블 (Meter Table)| 플로우별 최대 대역폭 측정(Rate Limiter) 및 **초과 패킷 DSCP 마킹/드롭** | QoS 제어 |

#### 한줄 요약
- 그룹 테이블과 미터 테이블은 우회 전환과 대역폭 제한 판단을 스위치 안에 미리 심어 둔 계층이라 컨트롤러 왕복 없이 데이터 평면에서 끝나고, 흐름 테이블 TCAM은 매칭과 전달에만 전념한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Flow-Mod (Flow Modification)**: 컨트롤러가 스위치에 새로운 흐름 규칙을 추가(ADD), 수정(MODIFY), 삭제(DELETE)하도록 명령하는 메시지.

</details>

```text
OpenFlow Table-Miss 및 Flow-Mod 파이프라인
        │
   1. [패킷 인입 및 다중 매칭] 패킷 인입 -> Table 0부터 순차적 Match-Action 파이프라인 검색
        │
   2. [Table-Miss Packet-In] 일치 규칙 부재 시 스위치가 OpenFlow Packet-In 메시지 송출
        │
   3. [전역 경로 연산] SDN 컨트롤러가 전역 토폴로지 기반 최적 전송 경로 산출
        │
   4. [Flow-Mod 규칙 설치] 컨트롤러가 스위치로 Flow-Mod(TCAM 룰 주입) 및 Packet-Out 하달
        │
   ▼
5. [라인 레이트 고속 포워딩] 스위치 하드웨어 TCAM에 규칙이 적재되어 후속 패킷부터 고속 전달
```

#### 한줄 요약
- Table-Miss가 난 패킷만 컨트롤러까지 올라가고 나머지는 TCAM에 남은 규칙으로 처리되므로, 규칙을 미리 깔아 둘수록 첫 패킷 지연은 줄고 테이블 자원은 더 든다.

## Ⅴ. 종류 및 비교


| 비교 항목 | 반응형 룰 주입 (Reactive Flow Setup) | 선제적 룰 주입 (Proactive Flow Setup) |
|:---|:---|:---|
| 규칙 주입 시점 | Table-Miss(미등록 패킷) 발생 시 동적 주입 | 네트워크 개통 시 컨트롤러가 사전에 일괄 주입 |
| 최초 패킷 지연 | 컨트롤러 RTT 왕복으로 인한 초기 지연 발생 | Flow Table에 기등록되어 초기 지연 0ms |
| 스위치 TCAM 점유 | 실제 활성 트래픽 규칙만 캐싱하여 절약 | 가능한 모든 경로 규칙을 상시 유지하여 고갈 위험|
| 컨트롤러 부하 | 대규모 동시 접속 시 Packet-In 폭증으로 과부하 | 초기 주입 후 패킷별 질의가 없어 부하 극소 |
| 적합 서비스 환경 | 동적 가상 머신(VM) 마이그레이션, 세션 인가 | 고정 백본 라우팅, 정적 VLAN 간 포워딩 |

#### 한줄 요약
- 반응형은 TCAM 메모리를 절약하지만 초기 지연이 발생하고, 선제적 방식은 초기 지연이 없으나 TCAM을 대량 점유한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Fail-Standalone Mode**: 컨트롤러와의 OpenFlow 채널이 단절되었을 때 스위치가 전통적인 L2/L3 스위칭 모드로 자동 전환하여 망 마비를 막는 복원 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 미등록 트래픽 유입 시 Packet-In 폭풍으로 컨트롤러 마비 | 스위치 레벨 Packet-In 전송률 제한(Rate Limiting) 및 CoPP 적용 | 제어 평면 CPU 자원 보호 및 서비스 연속성 유지 |
| 미사용 임시 플로우 누적으로 인한 스위치 하드웨어 TCAM 고갈 | 흐름 엔트리별 Idle Timeout 및 Hard Timeout 최적화 적용 | 유휴 규칙 자동 회수 및 신규 트래픽 수용 공간 확보 |
| 컨트롤러-스위치 간 OpenFlow 채널 단절 시 전체 네트워크 마비 | Fail-Standalone 모드 전환 및 백업 컨트롤러 다중 연결 | 제어 링크 단절 시에도 기존 L2/L3 포워딩 유지 |
| 스위치 TCAM 엔트리 검색 지연으로 인한 고속 패킷 손실 | 다중 테이블 파이프라인에서 하드웨어 EM(Exact Match) 엔진 우선 매핑 | 검색 지연 단축 및 100Gbps 라인 레이트 유지 |

#### 한줄 요약
- Packet-In Rate Limiting, Timeout 최적화, Fail-Standalone 모드, Exact Match 가속으로 운영한다.

## Ⅶ. 결론

- 소프트웨어 정의 네트워킹의 기초를 확립하고 데이터센터 가상 스위치(OVS) 및 통신사 연구망에서 SDN 사우스바운드 표준 인터페이스의 상징적 레퍼런스 모델로 기여하였으며, 최근 P4(Programming Protocol-independent Packet Processors) 및 gNMI/NETCONF 등 차세대 프로그래머블 데이터 플레인으로 확장·발전하는 가운데, 실무 컨트롤러-스위치 연동 설계 시에는 Packet-In 폭풍을 억제하는 스위치 CoPP 레이트 리미팅, 하드웨어 TCAM 고갈을 방지하는 유휴 수명(Idle/Hard Timeout) 최적화, 제어 채널 단절 시 망 마비를 방지하는 Fail-Standalone 모드 및 컨트롤러 다중 연결, 상호 인증 TLS 암호화를 결합하여 완벽한 제어 평면 안정성을 완성

#### 한줄 요약
- SDN 컨트롤러와 OpenFlow의 Match-Action 파이프라인을 결합하여 고신뢰 제어 평면을 구현한다.
