---
sidebar:
  order: 13
  label: "013. 다중 프로토콜 레이블 스위칭 (MPLS)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "다중 프로토콜 레이블 스위칭 (Multiprotocol Label Switching, MPLS)"
date: "2026-08-13T16:27:00+09:00"
tags:
  - "notes-network"
weight: 13
extra:
  question_no: "013"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "비교형: 126회 MPLS-TP•IP-MPLS 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **다중 프로토콜 레이블 스위칭(Multiprotocol Label Switching, MPLS)**: IP 패킷 헤더의 3계층 목적지 주소를 매 홉마다 복잡하게 룩업하지 않고, L2와 L3 사이의 32비트 고정 크기 레이블(Label)을 기반으로 고속 포워딩하는 2.5계층 캡슐화 기술.
- **전달 등가 클래스(Forwarding Equivalence Class, FEC)**: 동일한 목적지, 품질 요구사항(QoS) 및 제어 정책을 가져 동일한 LSP 경로로 전달되는 패킷들의 논리적 그룹.
- **인터넷 프로토콜(Internet Protocol, IP)**: 네트워크 계층에서 수신처 호스트의 논리적 지정을 담당하는 라우팅 프로토콜.
- **레이블 스위치 경로(Label Switched Path, LSP)**: 입구 LER부터 출구 LER까지 MPLS 레이블 스왑을 통해 연결되는 단방향 논리적 단일 패킷 전송 경로.

</details>

- 정의/개념: FEC별 레이블 경로로 전달하는 **MPLS**
- 배경/필요성: IP 최단 경로만으로는 **명시 경로•VPN 격리 불가**

#### 한줄 요약

- FEC 분류와 LSP 레이블 스위칭

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **레이블 경계 라우터(Label Edge Router, LER)**: IP 네트워크와 MPLS 네트워크의 경계에 위치하여 IP 패킷에 레이블을 최초 부착(Push)하거나 최종 제거(Pop)하는 라우터.
- **레이블 스위칭 라우터(Label Switching Router, LSR)**: MPLS 백본 코어 중심에 위치하여 LFIB 테이블을 참조해 레이블을 교환(Swap)하고 고속 포워딩하는 코어 라우터.
- **레이블 스택(Label Stack)**: 32비트 MPLS 레이블 헤더를 다층(Multi-level)으로 중첩(예: Outer Label=LSP 백본 전송, Inner Label=VPN 고객 식별)하여 복합 서비스를 제공하는 구조.

</details>

- 입구 **레이블 경계 라우터**에서 패킷을 FEC로 정의하고 **레이블 스택** 부착.
- 코어 **레이블 스위칭 라우터**에서는 IP 헤더 분석 없이 단지 20비트 Label ID 교환으로 하드웨어 고속 포워딩 수행.
- **레이블 스택** 구조를 통해 L3VPN(BGP/MPLS VPN), L2VPN(VPWS/VPLS) 및 Traffic Engineering의 정밀한 서비스 격리 수용.

#### 한줄 요약

- LER Push•Pop과 LSR Swap•레이블 스택


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **레이블 전달 정보 기반(Label Forwarding Information Base, LFIB)**: LDP/RSVP-TE 프로토콜을 통해 수집한 [입력 인터페이스/입력 Label] -> [출력 인터페이스/출력 Label/동작(Push/Swap/Pop)] 매핑 정보를 저장하는 MPLS 고속 포워딩 데이터베이스.

</details>

```text
[ IP Network ] -> [ Ingress LER ] === (MPLS Core Backbone) ===> [ Egress LER ] -> [ IP Network ]
   IP Packet        Push Label        LSR (Swap Label)          Pop Label       IP Packet
                   (LFIB Lookup)       (LFIB Lookup)           (LFIB Lookup)
```

*Ingress LER(Push), Core LSR(Swap), Egress LER(Pop)의 계층적 MPLS 패킷 포워딩 구조.*

| 구성요소 | 주요 역할 및 책임 | 대응 패킷 동작 |
|:---|:---|:---|
| Ingress LER | IP 패킷 검사, FEC 분류, MPLS Shim Header 부착 | **Push** (레이블 삽입) |
| Core LSR | LFIB 룩업, In-Label을 Out-Label로 1:1 대체 교환 | **Swap** (레이블 교환) |
| Egress LER | MPLS Shim Header 제거, 순수 L3 IP 패킷으로 복원 후 전송 | **Pop** (레이블 제거) |
| PHP (Penultimate Hop Popping) | Egress LER 전단 라우터(Egress-1)에서 미리 Outer Label을 Pop 하여 Egress 부하 경감 | **Pop** (PHP 동작) |
| MPLS Shim Header | 32-bit (Label ID 20-bit + TC/QoS 3-bit + Bottom of Stack 1-bit + TTL 8-bit) | L2와 L3 사이에 위치 |

#### 한줄 요약

- LDP•RSVP-TE와 LFIB 기반 레이블 전달

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **레이블 푸시(Label Push)**: Ingress LER에서 L3 IP 패킷 앞단에 32비트 MPLS Shim Header를 추가 삽입하는 동작.
- **레이블 스왑(Label Swap)**: Transit LSR에서 유입된 패킷의 Ingress Label을 LFIB 표에 정의된 Egress Label로 교체하여 출구 포트로 보충 포워딩하는 동작.
- **레이블 팝(Label Pop)**: Egress LER (또는 PHP 라우터)에서 최상위 MPLS Label을 떼어내고 원본 L2/L3 패킷으로 복원하는 동작.

</details>

```text
[ IP Packet (Dest: 10.1.1.1) Ingress LER 유입 ]
                      |
                      v
[ 1. Ingress LER (Label Push) ] ----> FEC 분류 후 Shim Header (Label 100) 삽입
                      |
                      v
[ 2. Transit LSR (Label Swap) ] ----> In-Label 100 -> Out-Label 200 로 LFIB 스왑
                      |
                      v
[ 3. Penultimate LSR (PHP Pop) ] ---> Egress LER 직전 장비에서 Outer Label 제거 (PHP)
                      |
                      v
[ 4. Egress LER (IP Forwarding) ] --> 원본 IP 패킷 복원 후 목적지 라우팅 전달
```

### 동작 원리

1. **Ingress LER (Label Push)**: FEC별 레이블 부착
2. **Transit LSR (Label Swap)**: LFIB의 출력 레이블로 교환
3. **Penultimate LSR (PHP Pop)**: 마지막 전 홉에서 레이블 제거
4. **Egress LER (IP Forwarding)**: 원본 IP 패킷 전달

#### 한줄 요약

- LER Push•LSR Swap•PHP Pop으로 LSP 전달

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가상 사설망(Virtual Private Network, VPN)**: MPLS 레이블 스택(Outer=LSP, Inner=VPN ID)을 활용하여 이동통신사/ISP 백본 망 상에서 다수 기업의 사설망을 완벽히 논리 격리해주는 서비스.

</details>

| 비교 항목 | **MPLS 스위칭** | **일반 L3 IP 라우팅** |
|:---|:---|:---|
| 포워딩 기준 | 20비트 고정 크기 MPLS Label ID 스위칭 | 가변 길이 IP 패킷 목적지 주소 LPM(Longest Prefix Match) |
| 패킷 룩업 위치 | L2와 L3 사이의 2.5 계층 Shim Header | L3 IP 헤더 (20~60 바이트) |
| 트래픽 엔지니어링 | RSVP-TE를 통해 명시적 우회 경로 (Explicit Route) 설정 가능 | 기본적으로 IGP Metric 기반 최단 경로로만 집중 |
| 고가용성 방어 | MPLS FRR (Fast Reroute) 적용 시 50ms 이내 절체 가능 | IGP 수렴 속도에 의존 (수 초~수십 초 소요) |

> 요약: 매 홉 LPM을 연산하는 IP 라우팅 대비, 고정 Label ID 기반의 고속 스위칭과 Traffic Engineering, VPN 서비스 격리를 지원하는 MPLS의 우위성.

#### 한줄 요약

- IP LPM과 달리 레이블로 VPN•명시 경로 전달

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **레이블 분배 프로토콜(Label Distribution Protocol, LDP)**: Hop-by-Hop 방식으로 IP 서브넷 프리픽스와 MPLS Label 바인딩 정보를 인접 라우터 간에 자동으로 할당/전파하는 표준 프로토콜.
- **자원 예약 프로토콜-트래픽 엔지니어링(Resource Reservation Protocol-Traffic Engineering, RSVP-TE)**: 원하는 대역폭(Bandwidth)과 명시적 경로(Explicit Route)를 지정하여 백본 내에 우회 LSP를 사전에 예약 생성하는 프로토콜.
- **양방향 전달 탐지(Bidirectional Forwarding Detection, BFD)**: 수 ms 단위의 빠른 헬로 패킷으로 LSP 물리/논리 장애를 실시간 감지하는 고속 탐지 기술.
- **고속 우회(Fast Reroute, FRR)**: 링크/노드 장애 발생 시 BFD와 연동하여 50ms 미만의 시간 내에 사전에 구축된 Backup LSP 경로로 주회차 스위칭하는 기술.
- **경로 최대 전송 단위(Path Maximum Transmission Unit, PMTU)**: MPLS Shim Header(4바이트~12바이트) 추가 부착에 따라 단편화(Fragmentation)가 발생하지 않도록 이더넷 MTU(예: 1500 -> 1512~1524 바이트)를 확장 수용해 주는 백본 MTU 튜닝.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| MPLS 백본 패킷 단편화 | MPLS Label Stack 부착으로 MTU 1500바이트 초과 | 백본 라우터 인터페이스 MTU를 1524~9000(Jumbo Frame)으로 **PMTU** 확장 | 단편화/패킷 Drop 예방 |
| 백본 링크 단절 시 통신 끊김 | LDP 기본 수렴 속도로는 미디어/VoIP 세션 단절 | **BFD** 탐지 연동 및 **RSVP-TE FRR(Fast Reroute)** 백업 LSP 구축 | 50ms 이내 무중단 고속 우회 절체 |
| 이종 고객 간 IP 대역 중첩 | 다수 기업 고객이 동일한 192.168.x.x 사설 IP 사용 | BGP/MPLS L3VPN 적용 (Outer Label + Inner Route Distinguisher/Target Label) | 완벽한 **서비스 격리** 구현 |

#### 한줄 요약

- BFD•FRR•PMTU로 복구 시간과 오버헤드 통제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **서비스 격리(Service Isolation)**: 다층 레이블 스택(Multi-level Label Stacking)을 활용하여 기업 간 VPN 트래픽을 완벽하게 분리하고 독자적인 QoS를 보장하는 기술.

</details>

- VPN 격리는 **레이블 스택**, 고속 복구는 **FRR** 적용

#### 한줄 요약

- 격리•복구 요구에 따라 레이블 스택과 FRR 선택
