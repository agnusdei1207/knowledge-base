---
sidebar:
  order: 13
  label: "013. 다중 프로토콜 레이블 스위칭 (MPLS)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "다중 프로토콜 레이블 스위칭 (Multiprotocol Label Switching, MPLS)"
date: "2026-08-06T23:27:50+09:00"
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

<details>
<summary>핵심 용어</summary>

- **다중 프로토콜 레이블 스위칭(Multiprotocol Label Switching, MPLS)**: 레이블로 패킷을 전달하는 기술이다.
- **전달 등가 클래스(Forwarding Equivalence Class, FEC)**: 같은 전달 정책을 적용할 패킷 묶음이다.
- **IP(Internet Protocol)**: 논리 주소를 기반으로 네트워크 사이에서 패킷을 전달하는 프로토콜이다.
- **레이블 스위치 경로(Label Switched Path, LSP)**: 입구부터 출구까지 레이블 교환으로 패킷을 전달하는 단방향 논리 경로이다.

</details>

- 정의/개념: **MPLS**는 입구에서 패킷을 **FEC**로 분류하고 레이블을 붙여 **LSP**로 전달하는 기술이다.
- 배경/필요성: 목적지별 **IP** 경로만으로는 서비스 격리와 명시 경로 표현이 제약된다.

#### 한줄 요약

- 운송표를 붙여 정해진 거점만 거치게 하는 전달 기술이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **레이블 경계 라우터(Label Edge Router, LER)**: MPLS 경계에서 레이블을 부착•제거하는 라우터이다.
- **레이블 스위칭 라우터(Label Switching Router, LSR)**: MPLS 내부에서 레이블을 교환하는 라우터이다.
- **레이블 스택**: 전송 경로•고객 서비스 등 여러 전달 문맥을 표현하도록 레이블을 겹친 구조이다.

</details>

- 입구 **LER**는 FEC를 분류해 레이블을 부착한다.
- 중간 **LSR**는 레이블을 교환해 전달한다.
- **레이블 스택**은 전송•서비스 문맥을 함께 표현한다.

#### 한줄 요약

- 운송표를 여러 장 겹치면 바깥 표는 백본 길, 안쪽 표는 고객•서비스 구분을 나타낸다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **레이블 전달 정보 기반(Label Forwarding Information Base, LFIB)**: 입력 레이블별 출력 레이블•다음 홉•동작을 저장한 전달 표이다.

</details>

```text
MPLS 영역
├── 입구 LER
├── 중계 LSR
└── 출구 LER
```

선의 의미: 입구 LER와 출구 LER 사이에 중계 LSR이 놓이는 MPLS 영역의 정적 LSP 연결 토폴로지이다.

| 구성요소 | 책임 |
|:---|:---|
| 입구 LER | **LER**가 **FEC** 분류•**레이블 스택** 부착 |
| 중계 LSR | **LSR**가 **LFIB** 조회로 출력 레이블•다음 홉 교환 |
| 출구 LER | LER가 레이블 제거 후 **IP** 패킷 전달 |

#### 한줄 요약

- 관리 체계가 운송표 교환 규칙을 먼저 배포하면 실제 거점은 표에 적힌 다음 동작만 수행하는 것이 핵심이다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **레이블 푸시(Push)**: 입구에서 패킷에 새 레이블을 붙이는 동작이다.
- **레이블 스왑(Swap)**: 중계 구간에서 입력 레이블을 출력 레이블로 교환하는 동작이다.
- **레이블 팝(Pop)**: 출구에서 패킷의 최상위 레이블을 제거하는 동작이다.

</details>

```text
출발망 IP 패킷
       |
       v
1. 레이블 푸시
       |
       `-- 입구 LER: FEC별 레이블 스택 부착
                          |
                          v
                  2. 레이블 스왑
                          |
                          `-- 중계 LSR: LFIB 기반 교환
                                           |
                                           v
                                   3. 레이블 팝
                                           |
                                           `-- 출구 LER: 목적망 IP 패킷
```

### 동작 원리

1. **레이블 푸시**: FEC에 대응하는 레이블 스택을 추가한다.
2. **레이블 스왑**: LFIB로 출력 레이블•다음 홉을 결정한다.
3. **레이블 팝**: 출구 LER에서 레이블을 제거해 IP을 복원한다.

#### 한줄 요약

- 입구는 레이블을 붙이고 중간은 바꾸며 출구는 제거한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **가상 사설망(Virtual Private Network, VPN)**: 공용 전달망 위에서 고객별 주소와 경로를 논리적으로 격리한 사설망이다.

</details>

| 패킷 전달 방식 | **MPLS** | **IP** 라우팅 |
|:---|:---|:---|
| 적용 기준 | **VPN** 격리•명시적 경로 제어 | 일반 인터넷 도달성 |
| 핵심 특징 | 입구 FEC 분류•레이블 교환 | 매 홉 목적지 프리픽스 조회 |
| 한계 | 레이블 상태•LSP 운영 복잡도 | 서비스 분리에 별도 오버레이 필요 |

> 요약: MPLS는 FEC별 LSP로 경로•서비스 제어가 핵심이다.

#### 한줄 요약

- IP는 매 홉에서 주소를 보고 MPLS는 입구에서 정한 레이블 경로를 따른다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **레이블 분배 프로토콜(Label Distribution Protocol, LDP)**: 프리픽스와 레이블의 연결 정보를 교환하는 프로토콜이다.
- **자원 예약 프로토콜-트래픽 엔지니어링(Resource Reservation Protocol-Traffic Engineering, RSVP-TE)**: 제약 기반 LSP를 설정하는 프로토콜이다.
- **양방향 전달 탐지(Bidirectional Forwarding Detection, BFD)**: 전달 경로 장애를 빠르게 탐지하는 기능이다.
- **고속 우회(Fast Reroute, FRR)**: 장애 시 미리 계산한 보호 경로로 우회하는 기능이다.
- **경로 MTU(Path Maximum Transmission Unit)**: 경로 전체에서 단편화 없이 전달할 수 있는 최대 패킷 크기이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 여러 고객의 사설 주소가 중첩 | VPN별 **레이블 스택** 분리 | 고객 경로 격리 |
| LSP 단절 탐지가 늦어 트래픽 손실 | **BFD**와 **FRR** 보호 경로 연동 | 장애 전환 시간 단축 |
| 깊은 레이블 스택으로 MTU 초과 | 스택 깊이를 포함한 **경로 MTU** 산정 | 패킷 단편화•폐기 예방 |
| 제어 평면과 LFIB 매핑이 불일치 | **LDP**•**RSVP-TE**와 LFIB 대응 관계 대조 | 전달 블랙홀 방지 |

#### 한줄 요약

- 안쪽 레이블은 고객 경로를, 바깥 레이블은 백본 경로를 가리켜 여러 고객의 주소가 겹쳐도 섞이지 않는다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **서비스 격리**: VPN별 내부 레이블과 백본 전달 레이블을 나눠 고객 경로가 섞이지 않게 하는 방식이다.

</details>

- **서비스 격리**가 필요하면 **레이블 스택**을 구성하고 **경로 MTU** 이내로 패킷 크기를 제한한다.

#### 한줄 요약

- 고객 서비스와 백본 경로를 함께 구분하려면 목적별 레이블을 겹쳐 사용한다.
