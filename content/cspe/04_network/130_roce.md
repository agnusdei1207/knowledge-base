---
title: "RoCE — RDMA over Converged Ethernet (RoCE)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 130
extra:
  question_no: "130"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- RoCE는 RDMA 전송 의미를 이더넷에서 제공하는 프로토콜임
- RoCEv1은 이더넷 링크 계층에서 동작하고 RoCEv2는 UDP/IP로 라우팅할 수 있음
- PFC는 우선순위별 Pause 프레임으로 특정 트래픽 클래스의 손실을 억제함
- ECN은 큐 혼잡을 패킷 표시로 송신자에게 알려 전송률을 조정하게 함

## Ⅰ. 개요

- **정의/개념**: RoCE는 RNIC의 RDMA Read·Write·Send·Receive 연산을 이더넷 프레임 또는 UDP/IP 패킷으로 전달하는 데이터센터 전송 기술임
- **배경/필요성**: 분산 학습과 스토리지 트래픽에 RDMA를 적용하면서 별도 InfiniBand 패브릭 대신 기존 이더넷의 스위치·광링크·운영 체계를 활용할 방식이 필요함

## Ⅱ. 특징

- RoCEv2는 UDP/IP 캡슐화로 L3 라우팅과 ECMP 경로를 사용할 수 있음
- 전송 손실은 재전송과 지연 변동을 유발하므로 PFC·ECN·DCQCN 같은 혼잡 제어를 함께 구성함
- RDMA 트래픽과 일반 이더넷 트래픽이 링크를 공유하므로 큐와 우선순위 정책이 필요함
- PFC를 넓게 적용하면 Pause 전파와 Head-of-Line Blocking으로 다른 흐름까지 정체될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | RoCEv1 | RoCEv2 |
|:---|:---|:---|
| 캡슐화 | 이더넷 프레임 | UDP/IP 패킷 |
| 전달 범위 | 동일 L2 브로드캐스트 도메인 | L3 라우팅 구간 |
| 경로 확장 | VLAN·L2 경로에 의존 | ECMP와 IP 라우팅 활용 |
| 혼잡 신호 | PFC와 L2 큐 관리 | ECN·DCQCN과 PFC를 조합 |
| 적용 환경 | 단일 랙·L2 패브릭 | 다중 랙·Leaf-Spine 데이터센터 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| RoCE RNIC | RDMA 작업을 이더넷·UDP/IP 패킷으로 처리함 |
| Leaf-Spine 스위치 | ECMP 경로와 우선순위 큐를 제공함 |
| PFC | 지정 트래픽 클래스의 큐 손실을 억제함 |
| ECN·DCQCN | 혼잡 표시를 반영해 송신률을 조정함 |
| 텔레메트리 | 큐 길이, PFC Pause, ECN 표시, 손실을 수집함 |

```text
[RoCE RNIC] -- Leaf -- Spine -- Leaf -- [RoCE RNIC]
                  | ECN·PFC·우선순위 큐 |
                  +---- 혼잡 제어 ------+
```

## Ⅴ. 원리 및 절차

1. **트래픽 분류**: RoCE 패킷을 DSCP·PCP 기반 우선순위 큐에 매핑함
2. **경로 선택**: RoCEv2 패킷을 IP 라우팅과 ECMP로 전달함
3. **혼잡 표시**: 스위치 큐가 임계값을 넘으면 ECN을 표시함
4. **전송률 조정**: 수신 피드백을 받은 송신 RNIC가 DCQCN으로 전송률을 낮춤
5. **손실 억제**: 급격한 큐 증가 시 제한된 우선순위에서 PFC를 적용함

## Ⅵ. 실무 적용 및 유의점

1. AI 클러스터의 All-Reduce에 RoCEv2를 적용할 때는 평균 대역폭만 보지 않고 흐름 간 큐 경합을 포함해 p99 지연, ECN 표시율, 링크 사용률을 검증해야 함
2. PFC 임계값이나 적용 범위가 과도하면 Pause Storm과 교착이 발생할 수 있으므로 케이블 지연과 버퍼 크기로 Headroom을 계산하고 PFC Pause 시간, 큐 길이, 패킷 손실을 함께 점검해야 함

## Ⅶ. 결론

RoCE는 RDMA를 이더넷 패브릭에서 제공하며, RoCE 버전과 라우팅 범위뿐 아니라 ECN·PFC 기반 혼잡·손실 제어를 함께 설계해야 함.
