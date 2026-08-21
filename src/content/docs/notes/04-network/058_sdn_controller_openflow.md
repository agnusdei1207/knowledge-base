---
sidebar:
  order: 58
  label: "058. SDN 컨트롤러와 OpenFlow"
  badge:
    text: "기출 · 30%"
    variant: note
title: "SDN 제어 평면 및 통신 프로토콜 : SDN 컨트롤러와 OpenFlow"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 58
extra:
  question_no: "058"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 30
  priority_note: "OpenFlow 1.3+ 파이프라인(Match-Action, Multi-Table), Packet-In/Out, Flow-Mod 및 보안 채널(TLS)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SDN 컨트롤러(SDN Controller)**: 분산된 네트워크 스위치 장비의 제어 평면을 중앙 집중화하여 전역 토폴로지를 관리하고, 소프트웨어 기반으로 최적 포워딩 경로를 계산하는 제어 시스템.
- **OpenFlow(오픈플로우)**: SDN 컨트롤러(제어 평면)와 네트워크 스위치(데이터 평면) 간에 표준화된 흐름 테이블(Flow Table) 엔트리를 추가, 수정, 삭제하기 위해 사용되는 표준 사우스바운드(SBI) 프로토콜 (ONF 표준).

</details>

- 정의/개념: 논리적 중앙 관제 두뇌로서 전역 라우팅을 총괄하는 **SDN 컨트롤러** 와, 표준화된 **Match-Action 파이프라인** 을 통해 스위치 TCAM 메모리에 흐름 규칙(Flow Rule)을 프로그래밍하는 **OpenFlow 프로토콜**
- 배경/필요성: 이기종 벤더 스위치별 비표준 제어 인터페이스로 인한 장비 종속성을 타파하고, 단일 공통 사우스바운드 프로토콜로 대규모 데이터센터의 패킷 포워딩 경로를 실시간 제어할 요구

#### 한줄 요약
- SDN 컨트롤러가 전역 경로를 연산하고 OpenFlow 프로토콜로 스위치 Flow Table을 프로그래밍한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **매칭-액션 파이프라인(Match-Action Pipeline)**: 수신 패킷의 L2~L4 헤더 필드(Match)를 대조한 후, 일치할 경우 사전 정의된 지시자(Action: 출력 포트 지정, 헤더 수정, 패킷 드롭 등)를 순차 실행하는 메커니즘.
- **테이블 미스(Table-Miss)**: 수신 패킷의 헤더가 스위치 Flow Table의 어떤 규칙과도 일치하지 않을 때 발생하는 이벤트로, 기본 지정된 액션(컨트롤러 보고 또는 드롭)을 트리거.

</details>

- **다중 흐름 테이블(Multi-Table) 파이프라인**: 0번 테이블부터 순차적으로 파이프라인 처리를 수행하여 단일 테이블의 엔트리 폭증을 방지하고 복합 정책(VLAN $\rightarrow$ ACL $\rightarrow$ 라우팅) 적용
- **비동기 이벤트 기반 보고(Packet-In)**: 미지의 패킷(Table-Miss)이나 상태 변경 발생 시 스위치가 비동기적으로 컨트롤러에 패킷 페이로드 및 수신 포트를 보고
- **TLS 보안 제어 채널**: 컨트롤러와 스위치 간 통신은 상호 인증된 TLS(TCP 포트 6653) 보안 채널을 통해 암호화되어 제어 평면 도청 및 변조 차단

#### 한줄 요약
- Match-Action 파이프라인, 비동기 Packet-In 제어 보고, TLS 보안 전송 채널을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **흐름 테이블 엔트리(Flow Table Entry)**: 매칭 필드(Match Fields), 우선순위(Priority), 카운터(Counters), 명령어 세트(Instructions), 만료 타이머(Timeouts), 쿠키(Cookie)로 구성된 규칙 단위.
- **그룹 테이블(Group Table)**: 브로드캐스트/멀티캐스트(ALL), 패스트 페일오버(FF), 로드 밸런싱(SELECT) 등 복잡한 다중 포트 포워딩 액션을 지원하는 별도 테이블.

</details>

```text
[ 제어 평면 (SDN 컨트롤러) ]
   ▲ (Packet-In: 미등록 플로우 보고)
   │
   ├─ [ TLS 암호화 보안 채널 (TCP 6653) ]
   │
   ▼ (Flow-Mod / Packet-Out: 흐름 규칙 하향 주입 및 패킷 송출)
[ 데이터 평면 (OpenFlow 지원 스위치) ]
   ├─ Table 0 (L2 매칭) ──(Goto)──▶ Table 1 (L3/L4 ACL) ──(Goto)──▶ Table 2 (포워딩)
   ├─ [ 그룹 테이블 (Group Table) ] ── (멀티캐스트 / 페일오버)
   └─ [ 미터 테이블 (Meter Table) ] ── (QoS 대역폭 제한)
```

선의 의미: TLS 보안 채널을 통해 제어 평면의 지시가 데이터 평면의 다중 테이블 파이프라인으로 적재되어 패킷을 처리하는 아키텍처

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **SDN 컨트롤러** | 전역 토폴로지 분석, 최적 경로 계산, Flow-Mod 명령 생성 및 상태 모니터링 | 제어 평면 |
| **OpenFlow 채널** | 컨트롤러와 스위치 간 메시지(대칭형/비동기/동기)를 교환하는 보안 링크 | TLS / TCP 6653 |
| **흐름 테이블 (Flow Table)** | 매칭 필드와 액션 인스트럭션을 저장하여 라인 레이트 패킷 스위칭 수행 | TCAM 메모리 |
| **그룹 테이블 (Group)** | 플러딩, 멀티캐스트 복제, 링크 단선 시 즉각 우회(Fast-Failover) 처리 | L2/L3 다중화 |
| **미터 테이블 (Meter)** | 플로우별 최대 대역폭 측정(Rate Limiter) 및 초과 패킷 DSCP 마킹/드롭 | QoS 제어 |

#### 한줄 요약
- SDN 컨트롤러, TLS 보안 채널, Flow Table, Group Table, Meter Table이 결합하여 패킷을 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Flow-Mod (Flow Modification)**: 컨트롤러가 스위치에 새로운 흐름 규칙을 추가(ADD), 수정(MODIFY), 삭제(DELETE)하도록 명령하는 메시지.

</details>

```text
1. 스위치 포트로 패킷 인입 ➔ 다중 Flow Table(Table 0부터) 순차 매칭 검사
            │
            ▼ (Table-Miss 발생: 일치하는 엔트리 없음)
2. 스위치가 패킷 헤더와 수신 인터페이스 정보를 캡슐화하여 OpenFlow Packet-In 메시지 송출
            │
            ▼
3. SDN 컨트롤러가 Packet-In 분석 ➔ 전역 토폴로지 기반 최적 전송 경로 산출
            │
            ▼
4. 컨트롤러가 스위치로 Flow-Mod(TCAM 룰 등록) 및 Packet-Out(해당 패킷 송출 지시) 메시지 하향 전송
            │
            ▼
5. 스위치가 하드웨어 Flow Table에 규칙을 적재하고, 후속 패킷부터는 스위치 자체에서 고속 포워딩
```

**동작 원리**

1. **파이프라인 룩업**: 스위치가 인입 패킷을 테이블 0에서 평가하고 `Goto-Table` 지시에 따라 다음 테이블 순차 검색
2. **미등록 트래픽 보고**: 일치 엔트리가 없으면 `OFPT_PACKET_IN` 메시지를 컨트롤러로 비동기 발송
3. **중앙 제어 결정**: 컨트롤러의 라우팅 알고리즘이 송수신 종단 간 전 경로 스위치에 대한 룰 생성
4. **엔트리 프로그래밍**: `OFPT_FLOW_MOD`를 통해 각 스위치의 TCAM에 우선순위 및 타임아웃과 함께 액션 적재
5. **데이터 평면 스위칭**: 인스톨된 규칙에 매칭되는 후속 패킷은 컨트롤러 개입 없이 마이크로초 단위 전송

#### 한줄 요약
- 파이프라인 매칭, Table-Miss 시 Packet-In 보고, Flow-Mod 규칙 하향 주입, 스위치 자체 고속 포워딩 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **반응형(Reactive) vs 선제적(Proactive) 룰 주입**: 첫 패킷 발생 시 컨트롤러에 질의하여 동적으로 룰을 받는 방식과 서비스 개통 시 컨트롤러가 사전에 모든 룰을 정적으로 주입해 두는 방식.

</details>

| 비교 항목 | 반응형 룰 주입 (Reactive Flow Setup) | 선제적 룰 주입 (Proactive Flow Setup) |
|:---|:---|:---|
| **규칙 주입 시점** | **Table-Miss(미등록 패킷) 발생 시 동적 주입** | **네트워크 개통 시 컨트롤러가 사전에 일괄 주입** |
| **최초 패킷 지연** | **컨트롤러 RTT 왕복으로 인한 초기 지연 발생** | **Flow Table에 기등록되어 초기 지연 0ms** |
| **스위치 TCAM 점유** | **실제 활성 트래픽 규칙만 캐싱하여 절약** | **가능한 모든 경로 규칙을 상시 유지하여 고갈 위험** |
| **컨트롤러 부하** | 대규모 동시 접속 시 Packet-In 폭증으로 과부하 | 초기 주입 후 패킷별 질의가 없어 컨트롤러 부하 극소 |
| **적용 시나리오** | 동적 가상 머신(VM) 마이그레이션, 세션 기반 인가 | 고정 백본 라우팅, 정적 VLAN 간 포워딩 |

#### 한줄 요약
- 반응형은 TCAM 메모리를 절약하지만 초기 지연이 발생하고, 선제적 방식은 초기 지연이 없으나 TCAM을 대량 점유한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스탠드얼론 모드(Standalone / Fail-Secure Mode)**: OpenFlow 컨트롤러와의 연결이 단절되었을 때 스위치가 전통적인 L2/L3 스위칭 모드로 자동 전환하여 트래픽 단절을 방지하는 안전 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 미등록 트래픽(DDoS/스캔) 유입 시 Packet-In 폭풍으로 컨트롤러 마비 | 스위치 레벨 **Packet-In 전송률 제한(Rate Limiting)** 및 CoPP 적용 | 제어 평면 CPU 자원 보호 및 서비스 연속성 유지 |
| 미사용 임시 플로우 누적으로 인한 스위치 하드웨어 TCAM 메모리 고갈 | 흐름 엔트리별 **Idle Timeout 및 Hard Timeout** 최적화 적용 | 유휴 규칙 자동 회수 및 신규 트래픽 수용 공간 확보 |
| 컨트롤러-스위치 간 OpenFlow 채널 단절 시 전체 네트워크 트래픽 정체 | **Fail-Standalone 모드 전환** 및 백업 컨트롤러 다중 연결(OFPC_ROLE) | 제어 링크 단절 시에도 기존 L2/L3 포워딩 유지로 생존성 확보 |

#### 한줄 요약
- Rate Limiting으로 Packet-In 폭풍을 방어하고, Timeout으로 TCAM을 관리하며, Standalone 모드로 제어 링크 단절에 대비한다.

## Ⅶ. 결론

- SDN 인프라의 표준화된 패킷 제어를 위해 **OpenFlow 프로토콜**과 **SDN 컨트롤러**의 **Match-Action 다중 파이프라인 아키텍처**를 구축하되, 실무 운영 안정성을 확보하기 위해 **반응형/선제적 룰 주입의 하이브리드 운영**, **TCAM 타임아웃 최적화**, **Fail-Standalone 장애 복구 체계**를 통합 적용하여 고성능·고가용성 제어 평면을 완성

#### 한줄 요약
- SDN 컨트롤러와 OpenFlow의 Match-Action 파이프라인을 결합하여 고신뢰 제어 평면을 구현한다.
