---
sidebar:
  order: 56
  label: "056. 소프트웨어 정의 네트워킹 (SDN, Software-Defined Networking)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "소프트웨어 정의 네트워킹 (SDN, Software-Defined Networking)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 56
extra:
  question_no: "056"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 50
  priority_note: "설계형: 131회 SDN•ML Traffic 최적화"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **소프트웨어 정의 네트워킹(Software-Defined Networking, SDN)**: 네트워크 장비의 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 물리적으로 분리하고, 소프트웨어 중앙 제어기를 통해 망 제어와 경로 스케줄링을 동적으로 프로그래밍하는 네트워크 아키텍처이다.
- **제어 평면 및 데이터 평면(Control Plane & Data Plane)**: 패킷의 최적 이동 경로를 결정하는 제어 평면과 결정된 라우팅 규칙에 따라 하드웨어 패킷을 고속 포워딩하는 데이터 평면의 분리 구성이다.

</details>

- 정의/개념: **소프트웨어 정의 네트워킹(SDN, Software-Defined Networking)**은 네트워크 장비의 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 물리적으로 분리하고, 소프트웨어 기반 중앙 컨트롤러가 사우스바운드 API(OpenFlow, gNMI)를 통해 네트워크 트래픽 경로를 동적 프로그래밍 제어하는 무선/유선 네트워크 패러다임이다.
- 배경/필요성: 기존 전통적 라우터/스위치의 분산 제어 구조로 인한 개별 장비 CLI 설정 오버헤드, 전역 네트워크 변경의 한계 및 멀티 테넌트 클라우드 가상화 수용의 문제를 극복하기 위해 제정되었다.

#### 한줄 요약

- 제어 평면과 데이터 평면을 분리하고 중앙 SDN 컨트롤러를 통해 전역 네트워크 트래픽 경로와 정책을 동적 소프트웨어로 제어하는 기술.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **논리적 중앙 제어(Logical Centralized Control)**: 복수의 물리 컨트롤러를 클러스터링하여 전체 토폴로지와 노드 상태를 단일 뷰(Single-pane-of-glass)로 제어하는 구조이다.
- **텔레메트리 폐루프(Telemetry Closed-Loop Automation)**: 인밴드 네트워크 텔레메트리(INT) 모니터링 수치와 AI/ML 알고리즘을 결합하여 자율적으로 흐름 테이블 규칙을 보정·재배포하는 자동화 체계이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 상위 응용 애플리케이션과 컨트롤러를 연결하는 노스바운드 API(RESTful) 및 컨트롤러와 스위치를 연결하는 사우스바운드 API(OpenFlow)이다.

</details>

- **제어 및 전달 평면의 물리적 분리**: 데이터 전달은 범용 Bare-metal 스위치(ASIC)가 담당하고, 패킷 라우팅 연산은 소프트웨어 SDN 컨트롤러가 전담한다.
- **전역 토폴로지 기반 최적 경로 연산**: 단일 통제면에서 전체 네트워크 노드 및 링크 상태를 실시간 파악하여 병목 없는 트래픽 엔지니어링(TE)을 실행한다.
- **오픈 API 기반 프로그래밍 연동**: 노스바운드 API(NBI) 및 사우스바운드 API(SBI)를 통해 네트워크 변경을 소프트웨어 코드(NetDevOps)로 자동 조율한다.

#### 한줄 요약

- 제어/데이터 평면 분리, 논리적 중앙 전역 뷰 제공, 오픈 API 기반 소프트웨어 프로그래밍 기능 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **노스바운드·사우스바운드 인터페이스(Northbound & Southbound Interface, NBI/SBI)**: NBI는 애플리케이션 요구사항을 컨트롤러에 전달하고, SBI는 컨트롤러가 결정한 흐름 규칙을 스위치 하드웨어에 주입하는 규격이다.
- **흐름 규칙(Flow Rules / Flow Entry)**: 스위치 메모리(TCAM)에 저장되어 수신 패킷 매칭 조건(Match)과 수행 동작(Action: Forward, Drop, Modify)을 규정하는 테이블 엔트리이다.

</details>

```text
SDN 3계층 참조 아키텍처
├─ 응용 계층 (Application Layer - Traffic Engineering, Security, QoS Apps)
│  └─ 노스바운드 인터페이스 (Northbound API - RESTful / gRPC / Intent API)
├─ 제어 계층 (Control Layer - SDN Controller / ONOS, OpenDaylight)
│  └─ 사우스바운드 인터페이스 (Southbound API - OpenFlow, NETCONF, P4, gNMI)
└─ 인프라 계층 (Infrastructure Layer - OpenFlow Switches, Bare-metal Switches)
```

선의 의미: 응용 계층이 NBI API를 통해 네트워크 의도를 전달하면 제어 계층(SDN Controller)이 사우스바운드 API(SBI)로 인프라 계층 스위치에 흐름 규칙을 주입하는 계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 응용 계층 (Application Layer) | 트래픽 엔지니어링, 보안 방화벽, QoS 오케스트레이션 등 네트워크 서비스 비즈니스 로직 작성 |
| 노스바운드 API (NBI) | RESTful API, gRPC 및 Intent API를 사용하여 상위 앱과 컨트롤러 간의 커뮤니케이션 매개 |
| SDN 컨트롤러 (Control Layer) | 전체 망 토폴로지를 관리하고, 신규 패킷(Packet-In) 수신 시 최적 흐름 경로를 계산하여 스위치에 배포 |
| 사우스바운드 API (SBI) | OpenFlow, P4, NETCONF, gNMI 프로토콜을 사용하여 스위치에 흐름 규칙(Flow Entry)을 하향 주입 |
| 인프라 계층 (Infrastructure Layer) | 주입된 흐름 테이블(Flow Table) 규칙에 따라 패킷을 고속 무선/유선 포워딩, 변조 또는 폐기 수행 |

#### 한줄 요약

- 응용 계층이 NBI로 네트워크 의도를 전달하면 제어 계층(SDN Controller)이 전역 경로를 연산하여 SBI(OpenFlow)를 통해 인프라 계층 스위치에 흐름 규칙을 하향 설치하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **네트워크 의도(Network Intent / Intent-Driven Networking)**: 운용자가 "단말 A와 B 간 10Gbps 대역폭 및 1ms 지연 보장"과 같이 결과 중심 요구조건을 선언하는 언어 표현식이다.
- **텔레메트리(Network Telemetry / In-band Network Telemetry - INT)**: 데이터 패킷 헤더에 지연, 수신 스위치 ID, 큐 점유율을 적재하여 Real-time 트래픽 상태를 수집하는 모니터링 방식이다.

</details>

```text
1. 네트워크 정책 및 의도 수신 (Network Intent Input)
      │
      v
2. SDN 컨트롤러의 전역 토폴로지 및 링크 텔레메트리 수집 (Topology Discovery)
      │
      v
3. 최적 패킷 전송 경로 연산 및 흐름 테이블 규칙 생성 (Flow Rule Generation)
      │
      v
4. 사우스바운드 API를 통한 스위치 흐름 테이블 하향 설치 (Flow Table Push)
      │
      v
5. INT/eBPF 텔레메트리 기반 폐루프 모니터링 및 AI/ML 혼잡 시 재배포 (Closed-loop Re-routing)
```

### 동작 원리

1. **네트워크 의도(Intent) 수신**: NBI를 통해 애플리케이션 또는 운용자로부터 대역폭, 경로 격리 등의 네트워크 정책 의도를 전달받는다.
2. **전역 토폴로지 탐색**: 컨트롤러가 LLDP 패킷 및 텔레메트리를 이용하여 전체 스위치 연결 상태 및 링크 별 사용 대역폭을 수집한다.
3. **최적 경로 및 흐름 규칙 연산**: 그래프 알고리즘 및 AI/ML 엔진을 구동하여 요구 조건을 충족하는 스위치별 흐름 테이블 엔트리(Match-Action)를 생성한다.
4. **사우스바운드 주입 (Push)**: OpenFlow/gNMI 메시지를 활용하여 각 스위치의 TCAM 메모리에 흐름 규칙(Flow Entry)을 하향 주입한다.
5. **폐루프 텔레메트리 피드백 (Closed-loop)**: INT 및 eBPF 기반으로 실시간 패킷 전송 품질을 모니터링하고, 혼잡 발생 시 AI 연산으로 경로를 즉시 재설정(Re-routing)한다.

#### 한줄 요약

- 네트워크 의도 수신, 전역 토폴로지 수집, 흐름 규칙 연산, SBI 하향 설치 및 Closed-loop 텔레메트리 보정 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **소프트웨어 정의 네트워킹 중앙 제어(SDN Centralized Control)**: 모든 스위치가 자체 라우팅 계산을 하지 않고 중앙 컨트롤러가 작성해 준 라우팅 엔트리대로 지정 이동하는 제어 방식이다.
- **분산 제어(Distributed Routing Control / Traditional IP)**: 각 라우터가 이웃 라우터와 OSPF/BGP 제어 메시지를 주고받으며 독립적으로 분산 최단 경로 알고리즘을 계산하는 방식이다.

</details>

| 비교 항목 | **소프트웨어 정의 네트워킹 (SDN)** | **전통적 IP 네트워킹 (Traditional Network)** |
|:---|:---|:---|
| 평면 구조 | 제어 평면과 데이터 평면 물리적 분리 | 각 장비 내부 제어 및 데이터 평면 일체형 수용 |
| 경로 결정 주체 | 중앙 SDN 컨트롤러가 전역 경로 연산 | 각 라우터/스위치가 OSPF/BGP 분산 연산 |
| 네트워크 프로그래밍 | 오픈 API (NBI/SBI) 기반 소프트웨어 자동화 | 장비별 전용 CLI 및 수동 스크립트 작성 |
| 복구 및 트래픽 공학 | 중앙 텔레메트리 기반 전역 최적 자원 분배 | OSPF Metric 기반 국소 최단 경로 분배 (핫스팟 발생) |
| 단일 장애점 (SPOF) | 컨트롤러 클러스터링 동기화 실패 시 마비 위험 | 개별 라우터 분산 동작으로 중앙 장애 파급 없음 |

> 요약: SDN은 평면 분리와 중앙 컨트롤러의 동적 프로그램 라우팅을 제공하고, 전통 네트워크는 분산 알고리즘 기반 국소 라우팅을 제공.

#### 한줄 요약

- SDN은 평면 분리와 중앙 컨트롤러의 동적 프로그램 라우팅을 제공하고, 전통 네트워크는 분산 알고리즘 기반 국소 라우팅을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **상태 동기화(State Synchronization / Consensus)**: 다중 SDN 컨트롤러 클러스터(Raft/Paxos) 노드 간 전역 네트워크 토폴로지 데이터베이스의 일관성을 동일하게 유지하는 기술이다.
- **자동 절체(Automatic Failover & High Availability)**: 주(Master) 컨트롤러 고장 시 대기(Standby) 컨트롤러가 제어 권한을 1초 이내 인수하는 고가용성 설계이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 단일 컨트롤러 장애 (SPOF) | 중앙 컨트롤러 다운 시 전체 네트워크 제어 중단 | Raft 기반 다중 컨트롤러 HA 클러스터링 및 자동 절체 | 컨트롤러 고장 시에도 네트워크 지속 제어 |
| 패킷-인(Packet-in) 폭주 | 미정의 신규 패킷 폭주 시 컨트롤러 CPU 과부하 | 스위치 레벨 P4 프로그래밍 기반 1차 필터링 | 컨트롤러 제어면 마비 및 부하 방지 |
| 컨트롤러 간 상태 동기화 오차 | 분산 컨트롤러 노드 간 DB 동기화 지연 | 분산 합의 알고리즘(Raft Consensus) 적용 | 네트워크 전역 정책 일관성 100% 보장 |
| TCAM 흐름 테이블 용량 한계 | 스위치의 TCAM 메모리가 협소하여 유휴 규칙 누적 | Flow Entry Expiration Idle/Hard Timeout 최적화 | TCAM 자원 고갈 방지 및 빠른 스위칭 보장 |

#### 한줄 요약

- Controller HA 클러스터링 동기화, In-band Network Telemetry(INT) 기반 폐루프 트래픽 최적화, P4 프로그래밍을 통해 SDN 운영 안정성 확립.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **전역 정책 자동화(Global Policy Automation)**: 사람의 개입 없이 오픈 API와 AI 폐루프 텔레메트리를 결합해 네트워크 전체 인프라 제어를 실시간 자동화하는 상태이다.

</details>

- 차세대 데이터센터 및 통신망 구축 시 **SDN 아키텍처 도입**, **OpenFlow/P4 기반 사우스바운드 자동화**, **INT 연동 Closed-loop AI 트래픽 최적화 구현 필수**.

#### 한줄 요약

- 제어/데이터 평면 분리 아키텍처 및 INT 연동 AI/ML 기반 폐루프 트래픽 최적화 구현 필수.
