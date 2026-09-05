---
sidebar:
  order: 56
  label: "056. 소프트웨어 정의 네트워킹"
  badge:
    text: "기출 · 50%"
    variant: note
title: "소프트웨어 정의 네트워킹 : SDN (Software-Defined Networking)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 56
extra:
  question_no: "56"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 50
  priority_note: "ONF 3계층 아키텍처, 제어/데이터 평면 분리, OpenFlow 및 전역 트래픽 엔지니어링"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SDN (Software-Defined Networking)**: 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하여 중앙 컨트롤러로 네트워크 흐름을 프로그래밍하는 기술.
- **Control Plane vs Data Plane**: 경로 계산과 정책을 수립하는 제어 평면과 Flow Table에 따라 라인 레이트로 패킷을 포워딩하는 데이터 평면.

</details>

- 정의/개념: 제어 평면과 데이터 평면을 분리하고 개방형 API(OpenFlow/P4)를 통해 중앙 컨트롤러로 네트워크 전체 흐름을 프로그래밍 제어하는 아키텍처
- 배경/필요성: 전통적인 분산 IP 네트워크는 라우터/스위치 장비마다 제어 평면(**Control Plane**)과 데이터 평면(Data Plane)이 일체형으로 결합되어 있어, 수천 대의 이종 장비를 엔지니어가 개별 CLI로 수동 설정함에 따른 휴먼 에러 발생, 구성 변경 반영의 긴 지연, 국소 최단 경로(SPF/OSPF) 기반 라우팅의 한계로 인한 전역 트래픽 엔지니어링(Traffic Engineering) 불가 및 고가의 독점 벤더 종속성(Lock-in) 문제를 극복하기 위해, 복잡한 제어 평면을 중앙 집중형 소프트웨어 컨트롤러로 격리하고 단순화된 데이터 평면(화이트박스 스위치)과 개방형 사우스바운드 API(OpenFlow/P4)로 연결하는 **SDN**(Software-Defined Networking) 아키텍처를 도입하여 전역 가시성(Global Visibility) 확보, 네트워크 프로그래머블 자동화(NetDevOps) 및 대역폭 활용률 90% 이상의 유연한 트래픽 최적화를 달성할 필요

#### 한줄 요약
- 제어와 전달의 분리, 중앙 집중형 전역 가시성, 개방형 API 기반 자동화를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Global Visibility (전역 가시성)**: 중앙 컨트롤러가 전체 스위치의 링크 상태와 대역폭 사용량을 한눈에 파악하여 전역 최적 경로를 산출하는 특성.
- **Northbound vs Southbound API**: 응용 프로그램과 컨트롤러를 잇는 NBI(REST/gRPC)와 컨트롤러와 스위치를 잇는 SBI(OpenFlow/NETCONF).

</details>

- 제어 평면과 데이터 평면의 완전 분리: 고가의 독점 라우터를 저비용 표준 화이트박스 스위치로 대체
- 논리적 중앙 집중 제어 및 **전역 가시성**: 전체 네트워크 토폴로지를 단일 뷰로 파악하여 전역 트래픽 엔지니어링(TE) 최적화
- 소프트웨어 프로그래머블 자동화(NetDevOps): NBI API 코드를 통해 방화벽, QoS, 라우팅 정책을 무중단 일괄 배포

#### 한줄 요약
- 평면 분리, 전역 가시성 기반 트래픽 최적화, 개방형 API를 통한 프로그래머블 자동화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SDN Controller**: 네트워크 운영체제(Network OS) 역할을 수행하며 스위치에 Flow Table을 프로그래밍하는 두뇌.
- **OpenFlow / P4**: 패킷 헤더 매칭 및 액션을 정의하는 표준 사우스바운드 프로토콜(OpenFlow)과 데이터 플레인 프로그래밍 언어(P4).

</details>

```text
[SDN 구성]
|-- 응용 계층
|-- 노스바운드 API
|-- 제어 계층
|-- 사우스바운드 API
`-- 인프라 계층
```

선의 의미: 상위 비즈니스 앱 요구사항이 NBI를 통해 제어 계층으로 전달되고 계산된 흐름 규칙이 SBI를 통해 인프라 스위치로 하향 주입되는 구조

| 계층 | 주요 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| 응용 계층 (Application) | 트래픽 엔지니어링, 보안 모니터링, 가상 네트워크 | 비즈니스 SLA 정책 정의 및 NBI REST API 호출 | 비즈니스 로직 |
| 노스바운드 API (NBI) | RESTful API, gRPC, Java SDK | 응용 프로그램과 제어 계층 간의 추상화 인터페이스 제공 | 개방형 프로그래밍 |
| 제어 계층 (Controller) | ONOS, OpenDaylight, Ryu, 클라우드 컨트롤러 | 전역 토폴로지 관리, 최적 경로 연산, 흐름 규칙 생성 | Network OS |
| 사우스바운드 API (SBI) | **OpenFlow**, P4 Runtime, NETCONF, gNMI | 컨트롤러의 흐름 규칙을 스위치 하드웨어 TCAM에 프로그래밍 | 장치 제어 표준 |
| 인프라 계층 (Data Plane) | Open vSwitch(OVS), 화이트박스 ASIC 스위치 | Flow Table 매칭에 따른 라인 레이트 고속 패킷 포워딩 | 고속 패킷 전달 |

#### 한줄 요약
- 컨트롤러가 스위치마다 흩어져 있던 경로 계산을 걷어와 전역 토폴로지 하나로 대신 풀고 NBI와 SBI가 장비별 개별 설정을 표준 호출로 바꾸므로, 응용은 규칙이 어느 하드웨어 TCAM에 실리는지 알 필요가 없다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Packet-In vs Packet-Out / Flow-Mod**: Table-Miss 시 스위치가 컨트롤러로 패킷을 보고(Packet-In)하고, 컨트롤러가 규칙을 주입(Flow-Mod)하며 패킷을 방출(Packet-Out)하는 과정.

</details>

```text
SDN Flow Table 매칭 및 Packet-In/Flow-Mod 파이프라인
        │
   1. [패킷 인입 및 룩업] 신규 패킷이 스위치 포트에 인입 -> Flow Table 매칭 검색
        │
   2. [Table-Miss Packet-In] 일치 규칙 부재 시 스위치가 OpenFlow로 컨트롤러에 Packet-In 전송
        │
   3. [전역 최적 경로 연산] SDN 컨트롤러가 전역 토폴로지 및 QoS 정책을 기반으로 경로 산출
        │
   4. [Flow-Mod 규칙 설치] 컨트롤러가 경로상 스위치 TCAM에 Flow-Mod 주입 및 Packet-Out 하달
        │
   ▼
5. [라인 레이트 고속 전달] 이후 동일 플로우 패킷은 컨트롤러 개입 없이 스위치 단독 고속 포워딩
```

#### 한줄 요약
- 첫 패킷만 컨트롤러 왕복이라는 비싼 판단 비용을 치르고 이후 같은 플로우는 설치된 규칙을 재사용하므로, 제어와 전달의 분리 비용이 그 한 번에 상환된다.

## Ⅴ. 종류 및 비교


| 비교 항목 | 소프트웨어 정의 네트워킹 (SDN) | 전통적 분산 IP 네트워크 |
|:---|:---|:---|
| 제어 아키텍처 | 논리적 중앙 집중형 (Centralized Control) | 노드별 완전 분산형 (Distributed Control) |
| 장비 기능 구성 | 제어/데이터 평면 분리 (스위치는 전달 전담)| 라우터마다 제어/데이터 평면 일체형 탑재 |
| 망 관리 및 변경 | 중앙 NBI API 및 코드로 일괄 자동 적용 | 장비별 개별 CLI 콘솔 접속 수동 구성 |
| 트래픽 경로 최적화 | 전역 토폴로지 맵 기반 실시간 TE 최적화 | 홉별(Hop-by-Hop) 국소 최단 경로(SPF) 종속 |
| 장비 종속성 | 개방형 화이트박스 스위치 활용 (CapEx 절감)| 특정 제조사의 독점 어플라이언스 종속 |

#### 한줄 요약
- SDN은 논리적 중앙 집중 제어, 전역 트래픽 최적화, 개방형 하드웨어를 통한 자동화를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Raft Controller Clustering**: 단일 컨트롤러 장애(SPOF)를 막기 위해 분산 합의 알고리즘으로 복수 컨트롤러 간 상태를 동기화하는 고가용성 구조.
- **TCAM Timeout (Idle/Hard Timeout)**: 스위치 고비용 TCAM 메모리의 고갈을 막기 위해 일정 시간 트래픽이 없는 룰을 자동 삭제하는 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 중앙 SDN 컨트롤러 단일 장애 시 전체 네트워크 제어 마비 | Raft 분산 합의 기반 컨트롤러 클러스터링(ONOS/ODL) 구축 | 단일 장애점 제거 및 무중단 제어 평면 가용성 보장 |
| 대규모 미등록 트래픽 폭증 시 Packet-In 폭풍으로 CPU 과부하 | 선제적(Proactive) 룰 사전 주입 및 P4 기반 엣지 필터링 | Packet-In 발생률 95% 감소 및 제어 평면 안정성 확보 |
| 스위치 TCAM 하드웨어 용량 한계로 인한 Flow Table 오버플로우 | 흐름 규칙 수명 관리(Idle/Hard Timeout) 및 와일드카드 집약 | 미사용 엔트리 자동 회수 및 TCAM 자원 고갈 차단 |
| 컨트롤러와 스위치 간 통신 채널 도청 및 위조 룰 주입 위협 | 사우스바운드 채널 TLS 1.3 암호화 및 mTLS 인증 의무화 | 비인가 컨트롤러 사칭 차단 및 무결성 확보 |

#### 한줄 요약
- Raft 클러스터링, Proactive 룰 주입, **TCAM Timeout**, TLS 1.3 암호화로 운영한다.

## Ⅶ. 결론

- 하이퍼스케일 클라우드 데이터센터(SDDC), 광역 통신망(SD-WAN), 이동통신 코어망(5G SBA)에 이르기까지 현대 IT 네트워크 인프라의 운영 패러다임을 하드웨어에서 소프트웨어 코드로 완전히 전환시킨 핵심 아키텍처로 자리매김하였으며, 향후 생성형 AI 및 NetDevOps와 결합된 IBN(Intent-Based Networking)으로 진화해 나가는 가운데, 실무 아키텍처 구축 시에는 컨트롤러 단일 장애점(SPOF)을 제거하는 Raft 합의 기반 클러스터링(ONOS/ODL), Packet-In 폭풍을 방지하는 Proactive 룰 사전 주입, 하드웨어 TCAM 한계를 극복하는 유효 수명(Idle/Hard Timeout) 관리, 제어 채널 보안을 위한 mTLS 상호 인증을 결합하여 완벽한 네트워크 프로그래머빌리티와 고가용성을 완성

#### 한줄 요약
- SDN은 제어와 데이터 평면을 분리하여 전역 가시성과 소프트웨어 자동화를 실현하는 핵심 네트워크 기술이다.
