---
title: "클라우드 인터커넥트 (Cloud Interconnect)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 75
---

## Ⅰ. 개요
- **정의**: 온프레미스와 클라우드 VPC를 전용 회선으로 연결하는 네트워크 서비스임
- **배경/필요성**: 공용 인터넷 경유 시 지연·대역폭·보안 문제가 발생하므로 전용 연결이 필요함
- **비유**: 혼잡한 일반도로 대신 전용 고속도로를 개설하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전용 회선 기반 하이브리드 연결 원리 | Dedicated vs Partner Interconnect 차이 | VPN과 Interconnect의 대역폭·SLA 차이 명시 필요 |

> 요약: 전용 회선으로 온프레미스와 클라우드를 저지연·고대역으로 연결하는 서비스임

## Ⅱ. 구성요소
```text
On-Prem Router --> Cross-Connect --> CSP Edge --> Cloud Router --> VPC
                   (Colocation)      (PoP)        (BGP Peering)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Cross-Connect | 코로케이션 시설에서 고객 장비와 CSP 장비를 물리적으로 직결하는 케이블임 | 고속도로 진입 램프 |
| CSP Edge (PoP) | CSP의 네트워크 경계 지점으로 고객 트래픽을 수용하는 접점임 | 톨게이트 |
| Cloud Router | BGP를 통해 온프레미스와 VPC 간 동적 라우팅을 수행함 | 교차로 교통 신호 |

> 요약: Cross-Connect → CSP Edge → Cloud Router 경로로 전용 연결을 구성함

## Ⅲ. 절차
```text
Step1 Provision --> Step2 Cross-Connect --> Step3 BGP Setup --> Step4 Verify
```
- 1단계: CSP 콘솔에서 Interconnect 포트·대역폭(10G/100G)을 신청함
- 2단계: 코로케이션 시설에서 고객 라우터와 CSP PoP 간 물리 케이블을 연결함
- 3단계: BGP 세션을 설정하여 온프레미스·VPC 간 라우팅 경로를 교환함
- 4단계: BFD(Bidirectional Forwarding Detection)로 링크 장애 감지·Failover를 검증함

> 요약: 포트 신청-물리 연결-BGP 설정-검증 순서로 전용 회선을 구성함

## Ⅳ. 문제점
- 단일 장애점: 단일 PoP·회선 장애 시 전체 클라우드 연결이 중단됨
- 초기 비용: 전용 회선 개설·코로케이션 비용이 높아 소규모 조직에 부담이 큼
- 확장 지연: 대역폭 증설 시 물리 회선 추가가 필요하여 수주 이상 소요됨

> 요약: 단일 장애점, 초기 비용, 확장 지연이 핵심 과제임

## Ⅴ. 개선방안
1. 단기: 이중화 PoP·회선으로 Active-Active 구성하여 단일 장애점을 제거함
2. 중기: Partner Interconnect로 초기 투자 없이 통신사 공유 회선을 활용함
3. 장기: SD-WAN과 Interconnect를 결합하여 트래픽 패턴에 따라 대역폭을 탄력적으로 조절함

> 요약: 이중화, 파트너 모델, SD-WAN 결합으로 비용과 가용성을 개선함

## Ⅵ. 전망
- 발전 방향: NaaS 기반 On-Demand Interconnect로 API 호출만으로 대역폭을 조절하는 방향으로 진화함
- 기술사적 판단: 멀티 클라우드(076 참조) 환경에서 CSP 간 직접 Interconnect 수요가 증가함
- 기술사 제언: 하이브리드 네트워크 설계 시 Interconnect·VPN·SD-WAN의 역할 분담 기준 수립이 필요함
