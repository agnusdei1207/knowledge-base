---
title: "AS·IGP·EGP (Autonomous System/Interior·Exterior Gateway Protocol)"
date: "2026-06-30"
weight: 45
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> AS(Autonomous System)는 단일 관리 정책으로 운영되는 라우터 집합이며, IGP(Interior Gateway Protocol)는 AS 내부 라우팅, EGP(Exterior Gateway Protocol)는 AS 간 라우팅을 담당하는 프로토콜 분류이다.

## Ⅱ. 구성요소 / 원리
- AS 번호(ASN): 16비트/32비트 고유 번호로 인터넷상 AS 식별
- IGP: AS 내부 최적 경로 계산(RIP, OSPF, EIGRP, IS-IS)
- EGP: AS 간 정책 기반 경로 교환, 현재 사실상 BGP(Border Gateway Protocol)가 유일
- IGP는 속도·최단경로 중시, EGP는 정책·확장성·안정성 중시
- BGP는 경로 속성(AS-Path 등)으로 루프 방지 및 정책 적용

## Ⅲ. 흐름도 / 구조
```text
      ┌── AS 100 ──┐        ┌── AS 200 ──┐
      │ R1─IGP─R2  │  EGP   │ R3─IGP─R4  │
      │ (OSPF/RIP) │◀─BGP──▶│ (OSPF/RIP) │
      └────────────┘        └────────────┘
  AS 내부: IGP로 최단경로
  AS 경계: BGP로 정책 기반 경로 광고
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 인터넷을 AS 단위로 계층화하여 내부·외부 라우팅을 분리·확장 |
| 장점 | 도메인 자율성 확보, IGP/EGP 역할 분담으로 확장성·정책 제어 |
| 한계 | BGP 경로 전파 지연·오설정 시 광역 장애 위험, AS 간 정책 협상 복잡 |

## Ⅴ. 기술사적 적용
- ISP·대형 조직은 ASN 할당받아 BGP로 멀티홈(Multi-homing) 이중화 구성
- AS 내부는 OSPF/IS-IS, AS 간은 eBGP, 내부 전달은 iBGP로 조합 설계
- BGP 보안: RPKI(Resource PKI), 경로 필터링으로 경로 하이재킹 방지
