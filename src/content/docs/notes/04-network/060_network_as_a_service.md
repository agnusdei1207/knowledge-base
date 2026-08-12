---
sidebar:
  order: 60
  label: "060. 서비스형 네트워크 (NaaS, Network as a Service)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "서비스형 네트워크 (NaaS, Network as a Service)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 60
extra:
  question_no: "060"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "구조•설계형: 135회 NaaS 장문 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **서비스형 네트워크(Network as a Service, NaaS)**: 하드웨어 네트워크 장비와 유무선 회선을 직접 구매·소유하지 않고, 소프트웨어 기반 가상 인프라를 필요한 만큼 구독하여 사용료(OpEx)를 지급하는 클라우드 네트워크 서비스 모델이다.
- **소프트웨어 정의 네트워킹(Software-Defined Networking, SDN)**: NaaS 서비스 제공자가 네트워크 장비 제어 평면을 중앙 오케스트레이터로 가상화하여 고객에게 프로그래밍 가능 환경을 제공하는 핵심 기술이다.
- **네트워크 기능 가상화(Network Functions Virtualization, NFV)**: 방화벽, 가상 라우터, SD-WAN 등 네트워크 기능(VNF/CNF)을 하드웨어 설치 없이 엣지 및 클라우드 상에서 온디맨드로 인스턴스화하는 기술이다.

</details>

- 정의/개념: **NaaS(Network as a Service)**는 물리 라우터, 스위치 및 유무선 회선 인프라를 직접 구매하지 않고, 소프트웨어 정의 네트워킹(SDN)과 NFV 기반 클라우드 가상화 기술을 활용하여 온디맨드(On-Demand) 형태로 네트워크 자원을 구독·제어하는 클라우드 연동 네트워크 서비스 모델이다.
- 배경/필요성: 전통적 Enterprise WAN/LAN 구축 시 발생하는 막대한 초기 자본 지출(CapEx) 부담, 지사 구축 시 장비 조달 지연, 그리고 멀티 클라우드(AWS, Azure 등) 수송 트래픽의 복잡성을 해결하기 위해 제정되었다.

#### 한줄 요약

- 하드웨어 소유 없이 SDN/NFV 가상화 기반으로 대역폭, SD-WAN, SASE 보안 기능을 온디맨드 종량제(OpEx)로 구독·제어하는 클라우드 네트워크 서비스 패러다임.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **자본 지출 및 운영 지출(Capital Expenditure & Operational Expenditure, CapEx & OpEx)**: 네트워크 하드웨어 구입 시의 고정 자산 투자(CapEx)를 사용한 만큼 지불하는 월간 가변 비용(OpEx) 구조로 전환하는 경제성 지표이다.
- **서비스 수준 협약(Service Level Agreement, SLA)**: NaaS 공급자가 이용자에게 약속하는 대역폭, 종단 간 지연시간(Latency), 패킷 손실률 및 가용률(99.99%)에 관한 서비스 품질 계약 체계이다.

</details>

- **CapEx 기반 소유 구조에서 OpEx 중심 구독 체계 전환**: 물리 인프라 자산 매입 비용을 전면 제거하고, 대역폭 및 연결 시간 기반의 종량제/구독형 체계로 비용 효율성을 극대화한다.
- **오픈 API 기반 온디맨드 프로비저닝 (On-Demand Self-service)**: 포털 웹 및 RESTful API 호출만으로 수분 내 멀티 클라우드 전용선(Direct Connect) 및 SD-WAN 보안 터널을 신속 개통한다.
- **글로벌 오케스트레이션 및 무자산 확장성**: 전 세계에 분산된 NaaS PoP(Point of Presence) 및 SASE 에지를 기반으로 지사/클라우드 통신망을 지연 없이 통합 관리한다.

#### 한줄 요약

- OpEx 중심 구독제 비용 구조, 오픈 API 기반 수초 내 자동 프로비저닝, 멀티 클라우드 지능형 통합 연동 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **서비스 접점(Portal & Open API)**: 고객이 대시보드나 코드(IaC)를 통해 대역폭을 동적 가조정하고 보안 정책을 배포하는 통합 인터페이스 계층이다.
- **제어 기능(Central Orchestrator)**: 고객 의도(Intent)를 해석하여 SD-WAN 터널 생성, NFV 방화벽 체이닝 및 L2/L3 경로를 자동 연산·주입하는 중앙 두뇌 모듈이다.
- **네트워크 패브릭·기능(Network Fabric & VNF/CNF)**: VXLAN, MPLS, SD-WAN 터널과 vFW, vWAF 등 실제 데이터 전달 및 보안 처리를 담당하는 물리/가상 실행망이다.

</details>

```text
NaaS 4계층 참조 아키텍처
├─ 가입자 인터페이스 계층 (Customer Portal & Open REST APIs)
├─ 서비스 오케스트레이션 계층 (Central NaaS Orchestrator - Intent Engine)
├─ 융합 네트워크 실행 패브릭 (SD-WAN / SASE / Virtual Edge Network Fabric)
└─ 가시성 및 과금 관제 계층 (Closed-loop Telemetry, SLA & Metering System)
```

선의 의미: 가입자가 포털/API로 주문을 입력하면 오케스트레이터가 자원을 해석하여 SD-WAN/SASE 패브릭을 개통하고, 텔레메트리 시스템이 SLA 및 과금을 추적하는 계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 서비스 접점 (Portal & API) | 가입자 셀프 서비스 주문, 실시간 성능 대시보드, RESTful API를 통한 IaC 코드 연동 기능 제공 |
| 중앙 오케스트레이터 (Orchestrator) | 고객 서비스 의도(Intent) 분석, 멀티 벤더 SD-WAN/클라우드 자원 매핑 및 프로비저닝 자동화 |
| 서비스 에지 (Service Edge) | 지사, 본사, 데이터센터 및 AWS/Azure/GCP 멀티 클라우드로 연결되는 NaaS 접속 터미널 |
| 융합 데이터 패브릭 (Network Fabric) | VXLAN/MPLS 터널링, L3 라우팅, SD-WAN 패킷 최적화 및 vFW/vWAF 보안 VNF 체이닝 실행 |
| 관측·SLA·과금 (Observability & Billing) | In-band 텔레메트리로 지연/손실을 실시간 측정하고 SLA 이행 평가 및 시간/대역폭 기반 과금 정산 |

#### 한줄 요약

- 중앙 오케스트레이터가 가입자 의도를 분석하고 SD-WAN/SASE 패브릭을 자동 프로비저닝하며 SLA 관측 시스템이 모니터링하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **서비스 의도(Service Intent / Intent-Based Networking)**: 이용자가 요구하는 종단 간 대역폭, 보안 등급, 지연 시간 조건을 장비 독립적 언어로 선언한 주문 사양서이다.
- **소프트웨어 정의 광역망(Software-Defined Wide Area Network, SD-WAN)**: 멀티 벤더 회선 및 복합 트래픽 정책을 중앙 제어 소프트웨어로 최적화하는 WAN 가상화 기술이다.
- **보안 액세스 서비스 에지(Secure Access Service Edge, SASE)**: SD-WAN 네트워크 연결 기능과 클라우드 기반 SWG, CASB, ZTNA 보안 기능을 단일 서비스 에지에서 융합 제공하는 플랫폼 architecture이다.

</details>

```text
1. 가입자 포털/API 기반 네트워크 서비스 주문 (Service Intent Order)
      │
      v
2. 오케스트레이터의 서비스 의도 검증 및 자원 할당 (Intent Verification)
      │
      v
3. SD-WAN 터널, SASE 보안 및 L3 경로 자동 프로비저닝 (Path & VNF Provisioning)
      │
      v
4. 가상 에지 개통 및 실시간 텔레메트리 메트릭 수집 (Active Provisioned)
      │
      v
5. SLA 판정, 종량제 과금 산정 및 가시성 대시보드 가공 (SLA & Billing Evaluation)
```

### 동작 원리

1. **서비스 주문 수신**: 가입자가 NaaS 포털 또는 RESTful API로 원하는 지점 간 대역폭(예: 1Gbps)과 보안 정책을 의도(Intent) 형태로 주문한다.
2. **의도 검증 및 자원 연산**: 중앙 오케스트레이터가 가용 인프라 대역폭 및 PoP 상태를 체크하고 경로와 VNF 필요 구성을 연산한다.
3. **자동 프로비저닝 수용**: SD-WAN 터널링, SASE 보안 게이트웨이 및 언더레이 전용선 경로를 소프트웨어로 즉시 개통한다.
4. **텔레메트리 수집 및 모니터링**: 개통 완료된 터널상에서 In-band Telemetry를 구동하여 지연시간, 패킷 유실률, 전송 대역폭 수치를 수집한다.
5. **SLA 판정 및 과금 가시화**: 수집 수치를 기반으로 SLA 계약 위반 여부를 자동 계산하고, 실제 사용된 자원만큼 종량제 금액을 산정하여 가입자 대시보드에 표시한다.

#### 한줄 요약

- 서비스 주문, 의도 검증, SD-WAN/SASE 자동 프로비저닝, 텔레메트리 수집 및 SLA/과금 가시화 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **공급자 종속(Vendor Lock-in)**: 특정 NaaS 사업자의 전용 API, 데이터 모델 및 프로토콜 사용으로 인해 다른 서비스 공급자로 전환 시 막대한 이관 비용이 발생하는 상태이다.

</details>

| 비교 항목 | **NaaS (Network as a Service)** | **전통적 온프레미스 자체 구축** | **관리형 네트워크 서비스 (MSP)** |
|:---|:---|:---|:---|
| 자산 소유권 | 서비스 사업자 소유 (100% 무자산 모델) | 기업 직접 소유 (장비 및 회선 자산) | 기업 직접 소유 또는 장기 렌탈 |
| 비용 아키텍처 | 100% 가변 운영비 (OpEx 종량제) | 고정 자본비 (CapEx 구매 + 유지보수) | CapEx 구매 + 고정 운영 대행 수수료 |
| 구축 및 확장성 | 포털/API로 수분~수시간 내 동적 확장 | 발주-입고-배치까지 수주~수개월 지연 | 벤더 작업 요청 후 수일 내 반영 |
| 네트워크 유연성 | 소프트웨어 정의 기반 온디맨드 스케일링 | 장비 최대 사양에 고정되어 확장 제한 | 물리 장비 변경 시 지연 발생 |
| 주요 고려 리스크 | API 규격 벤더 종속(Lock-in), 과다 사용 비용 | 장비 구형화, 초기 거대 CAPEX 부담 | 위탁 벤더 SLA 이행 관리 모호 |

> 요약: NaaS는 100% OpEx 종량제와 온디맨드 수분 내 확장을 제공하고, 온프레미스는 자산 직접 통제권을, MSP는 전문 위탁 운영을 제공.

#### 한줄 요약

- NaaS는 100% OpEx 종량제와 온디맨드 수분 내 확장을 제공하고, 온프레미스는 자산 직접 통제권을, MSP는 전문 위탁 운영을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **종단 측정점(End-to-End Measurement Point)**: 고객 서비스 접속 구간 양 끝단에 위치시켜 실제 체감 품질 및 SLA 위반 책임을 객관적으로 산출하는 모니터링 지점이다.
- **구성 내보내기(Configuration Export & Migration)**: 특정 벤더 NaaS 환경의 네트워크 정책 및 접속 설정을 표준화된 형식(JSON/YAML)으로 이관 가능하게 추출하는 기능이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 멀티 클라우드 장애 책임 공방 | NaaS 사업자와 유선 회선 벤더 간 모니터링 경계 모호 | E2E 측정점 기반 Latency/Loss 실시간 모니터링 | 객관적 장애 구간 규명 및 핑퐁 현상 완벽 방지 |
| 종량제 예산 초과 폭증 | 트래픽 제어 실패로 인한 사용량 및 비용 급증 | 월간 트래픽 Cap 한도 설정 및 자동 알림 경보 | 비상용 트래픽 폭증 시 예산 초과 위험 차단 |
| NaaS 벤더 Lock-in 예속 | 특정 NaaS 사업자의 전용 API 규격에 완벽 예속 | 오픈 API 규격 준수 사업자 선정 및 IaC 코드 구성 | 타 NaaS 또는 멀티 클라우드로의 유연한 이관 가능 |
| 데이터 보안 및 컴플라이언스 | 공유 NaaS 인프라를 통한 사내 민감 패킷 통과 | SASE 기반 IPsec 암호화 터널 및 ZTNA 통제 적용 | 기업 데이터 유출 차단 및 보안 규제 준수 |

#### 한줄 요약

- E2E 객관적 SLA 모니터링 지점 배치, 월간 트래픽 Cap 한도 설정, 표준 REST API 준수 사업자 선정으로 NaaS 완성.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **네트워크 제공 방식(Network Delivery Models)**: 변동성, 투자 비용, 통제권 요소를 다각도로 평가하여 NaaS, On-Premise, Managed Service 중 최적을 선정하는 의사결정 체계이다.

</details>

- 멀티 클라우드 및 차세대 기업망 구축 시 **NaaS 가상화 서비스 모델 도입**, **SD-WAN/SASE 통합 패브릭 구축**, **오픈 API 및 SLA 검증 자동화 체계 구현 필수**.

#### 한줄 요약

- 클라우드 연동 NaaS 서비스 모델 및 SD-WAN/SASE 융합 패브릭 오케스트레이션 구현 필수.
