---
title: "MPLS (Multi-Protocol Label Switching)"
date: "2026-06-30"
weight: 52
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> IP 라우팅의 홉바이홉 조회 대신 고정 길이 라벨(Label)로 패킷을 스위칭하는 기술로, L2와 L3 사이(2.5계층)에서 동작하며 고속 전달과 트래픽 엔지니어링을 제공한다.

## Ⅱ. 구성요소 / 원리
- 라벨스위칭: 32비트 라벨 헤더(Shim)로 경로 결정, IP 헤더 재조회 불필요
- LER(Label Edge Router): 진입/출구에서 라벨 부착(Push)·제거(Pop)
- LSR(Label Switching Router): 코어에서 라벨 교환(Swap) 전달
- LSP(Label Switched Path): 진입 LER→출구 LER 단방향 라벨 경로
- FEC(Forwarding Equivalence Class): 동일 처리 패킷 그룹, LDP로 라벨 분배

## Ⅲ. 흐름도 / 구조
```text
[IP패킷] -> LER(Push 라벨L1) -> LSR(Swap L1->L2)
                                    |
                                    v
                LSR(Swap L2->L3) -> LER(Pop) -> [IP패킷]
        << 단방향 LSP, FEC 단위 전달 >>
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 고속 전달·트래픽 엔지니어링(TE)·VPN 통합 제공 |
| 장점 | 라우팅 부하 감소, 명시적 경로/QoS, L2/L3 VPN 수용 |
| 한계 | 라벨 관리 복잡, 도메인 내 한정, 초기 구축 비용 |

## Ⅴ. 기술사적 적용
- MPLS-TE: RSVP-TE로 명시적 경로·대역폭 예약, 장애 시 FRR 보호
- L3VPN(MP-BGP/VRF), L2VPN(VPLS)로 사업자 백본 가상화
- SR(Segment Routing)·SD-WAN으로 진화, 라벨 스택 단순화
