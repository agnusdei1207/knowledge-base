---
sidebar:
  order: 38
  label: "038. 5G 코어 SBA"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G 코어 서비스 기반 아키텍처 : SBA (Service Based Architecture)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 38
extra:
  question_no: "38"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "5GC SBA 구성요소, NRF 서비스 검색 및 CUPS 제어 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5GC SBA (Service-Based Architecture)**: 5G 코어 제어 평면의 Network Function(NF)들을 마이크로서비스로 모듈화하고 HTTP/2 REST API로 통신하는 아키텍처.
- **NRF (Network Repository Function)**: 모든 NF의 프로파일과 헬스 상태를 등록받아 동적 서비스 검색(Service Discovery)을 제공하는 중앙 디렉터리.

</details>

- 정의/개념: 5G 코어 제어 기능들을 독립적인 **NF(Network Function)로 모듈화하고 웹 표준 HTTP/2 REST API와 NRF로 상호 연동하는 클라우드 네이티브 코어 아키텍처**
- 배경/필요성: 하드웨어 어플라이언스 기반의 4G LTE EPC 코어망이 갖는 점대점(Point-to-Point) 전용 바이너리 프로토콜(GTP-C, Diameter) 종속성으로 인해, 신규 통신 서비스 배포 시 전사적인 망 재구성이 요구되고 트래픽 급증 시의 탄력적 수평 확장(Auto-scaling)과 워크로드별 End-to-End 네트워크 슬라이싱 제어가 불가능한 한계를 극복하기 위해, 코어 제어 평면 기능(AMF, SMF, PCF, UDM 등)을 독립된 마이크로서비스(NF: Network Function)로 분할하고 표준 HTTP/2 RESTful API와 NRF(Network Repository Function) 기반 동적 서비스 검색(Service Discovery) 및 CUPS(제어·데이터 분리)를 적용한 5G 코어 SBA(Service Based Architecture)를 도입하여 **클라우드 네이티브 환경에서의 무중단 기능 배포(CI/CD), 고탄력 확장성 및 민첩한 5G 특화 서비스 개통**을 달성할 필요

#### 한줄 요약
- HTTP/2 REST API 통신, NRF 기반 동적 검색, CUPS 분리를 통해 코어망의 민첩성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CUPS (Control and User Plane Separation)**: 제어 평면(SMF)과 사용자 데이터 평면(UPF)을 PFCP(Packet Forwarding Control Protocol)로 물리/논리 분리하는 아키텍처.
- **Stateless NF**: 세션 상태 데이터를 자체 메모리에 두지 않고 UDSF/UDR 저장소에 외부화하여 인스턴스를 무중단 탄력 확장하는 설계.

</details>

- 3GPP 전용 프로토콜 대신 **HTTP/2 기반 RESTful API 및 JSON 페이로드 표준 채택**
- NRF를 통한 **서비스 인스턴스 자동 발견(Service Discovery)**으로 NF 간 결합도(Coupling) 최소화
- 제어(SMF)와 데이터(UPF)를 완전 분리하는 **CUPS 구조를 통해 엣지(MEC) 분산 배치 지원**

#### 한줄 요약
- HTTP/2 REST 통신, NRF 동적 검색, CUPS 분리, Stateless 탄력 확장을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AMF (Access and Mobility Management Function)**: 단말 등록, 인증, 연결 및 이동성 관리를 전담하는 코어 제어 노드.
- **SMF (Session Management Function)**: PDU 세션 수립, IP 할당 및 UPF 포워딩 규칙을 제어하는 세션 관리 노드.
- **UPF (User Plane Function)**: 사용자 패킷의 라우팅, 포워딩, QoS 마킹 및 외부 데이터망(DN) 연동을 수행하는 데이터 플레인 노드.

</details>

```text
[5G 코어 SBA 구성]
|-- AMF
|-- SMF
|-- UPF
|-- NRF
|-- UDM / UDR
`-- PCF
```

선의 의미: 계층 및 제어 평면 NF들은 HTTP/2 버스로 연동되고 SMF가 N4(PFCP)를 통해 하위 UPF를 원격 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 통신 인터페이스 |
|:---|:---|:---|
| **AMF** | 단말 등록, 이동성 제어, 보안 및 **무선 인터페이스(N1/N2) 시그널링 종단 처리** | Namf (HTTP/2) |
| **SMF** | PDU 세션 수명주기 관리, IP 주소 할당, **UPF 포워딩 규칙(PFCP) 제어** | Nsmf (HTTP/2) |
| **UPF** | 사용자 패킷 고속 포워딩, **로컬 트래픽 브레이크아웃(MEC 연동), 과금 계량** | N3(GTP-U), N4(PFCP) |
| **NRF** | 전체 NF 인스턴스의 **프로파일 등록(Heartbeat) 수신 및 서비스 질의 검색 응답** | Nnrf (HTTP/2) |
| **UDM / UDR** | 가입자 인증 자격 증명(AKA) 검증, **서비스 프로파일 저장 및 가입자 상태 관리** | Nudm / Nudr |
| **PCF** | 네트워크 슬라이스별 **QoS 정책 및 과금 규칙(PCC) 통합 제어 결정** | Npcf (HTTP/2) |

#### 한줄 요약
- AMF, SMF, PCF, UDM, NRF가 HTTP/2 버스로 제어를 분담하고 UPF가 패킷 전송을 전담한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PFCP (Packet Forwarding Control Protocol)**: 3GPP 표준 제어 프로토콜로 SMF가 UPF에 패킷 탐지(PDR) 및 포워딩(FAR) 규칙을 하달하는 인터페이스.

</details>

```text
5G SBA PDU 세션 개통 파이프라인
        │
   1. [세션 요청] 단말(UE)이 AMF로 PDU Session Establishment Request 전송 (N1 NAS)
        │
   2. [동적 SMF 검색] AMF가 NRF로 슬라이스(S-NSSAI)에 최적화된 SMF 검색 (Nnrf_NFDiscovery)
        │
   3. [정책/가입 정보 수신] SMF가 UDM(가입자 프로파일) 및 PCF(QoS 정책) 조회
        │
   4. [PFCP 규칙 주입] SMF가 N4(PFCP)를 통해 UPF에 PDR/FAR 포워딩 규칙 하달
        │
   ▼
5. [데이터 파이프라인 개통] UE <-> gNB <-> UPF <-> 데이터망(DN) 간 초고속 데이터 전송 개시
```

#### 한줄 요약
- 개통 시점에 NRF 검색 한 번을 치르는 대신 어느 SMF가 어디 있는지 미리 고정해 둘 필요가 사라지고, 이후 사용자 데이터는 규칙만 받아 둔 UPF가 제어 평면을 거치지 않고 흘려보낸다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Reference Point (참조점)** vs **SBA (서비스 기반)**: 장비 간 1:1 고정 연결(4G)과 마이크로서비스 버스 연동(5G).

</details>

| 비교 항목 | 4G LTE 코어 (EPC) | 5G 코어 (5GC SBA) |
|:---|:---|:---|
| **아키텍처 모델** | 모놀리식 전용 하드웨어 / 점대점 참조점 | **마이크로서비스 / 서비스 기반 버스 (SBA)** |
| **제어 평면 프로토콜**| GTP-C, Diameter, SS7 (바이너리 전용 프로토콜)| **HTTP/2, RESTful API, JSON (웹 표준)** |
| **NF 검색 메커니즘** | DNS 기반 정적 IP 매핑 | **NRF 기반 실시간 동적 등록 및 검색 (Discovery)**|
| **제어/데이터 분리** | SGW/PGW 결합 (CUPS 제한적 지원) | **SMF(제어)와 UPF(데이터)의 완전 분리 (CUPS)** |
| **배포 및 확장성** | 전용 어플라이언스 / 펌웨어 업그레이드 | **쿠버네티스 컨테이너 / 수평 자동 확장 (Auto-scaling)**|

#### 한줄 요약
- 4G EPC의 점대점 전용 장비 구조에서 5GC SBA의 HTTP/2 기반 마이크로서비스 클라우드 아키텍처로 진화했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Circuit Breaker (서킷 브레이커)**: 특정 마이크로서비스(NF) 장애 시 호출을 즉각 차단하여 시스템 전체로의 연쇄 장애(Cascading Failure) 전파를 막는 복원력 패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 제어 NF 장애 시 호출 타임아웃 대기로 코어망 연쇄 마비 | **NF 서비스 메시 내 `서킷 브레이커(Circuit Breaker)` 적용** | 연쇄 장애 차단 및 정상 NF 서비스 연속성 유지 |
| HTTP/2 웹 API 노출에 따른 제어 평면 위변조 및 무인가 NF 접속 | **NF 간 `상호 TLS(mTLS)` 암호화 및 `OAuth 2.0 토큰 인가` 의무화** | 비인가 NF 위장 통신 차단 및 시그널링 보안 |
| NF 비정상 종료 시 NRF 디렉터리 내 Stale 정보 잔존으로 라우팅 실패 | **NRF 기반 `주기적 하트비트(Heartbeat)` 및 헬스체크 강제** | 비정상 NF 즉시 등록 해제 및 최신 가용 NF 라우팅 |
| 마이크로서비스 간 HTTP/2 REST API 통신 오버헤드로 인한 지연 | **서비스 메시(Envoy) 프록시 및 TCP 연결 재사용 풀링** | 메시지 직렬화/역직렬화 오버헤드 최소화 |

#### 한줄 요약
- 서킷 브레이커, mTLS/OAuth 2.0 인가, NRF 헬스체크, 서비스 메시 풀링으로 운영한다.

## Ⅶ. 결론

- 이동통신 코어망을 독점적 하드웨어 중심에서 IT 표준 클라우드 네이티브(Cloud-Native) 컨테이너 및 마이크로서비스 생태계로 완전히 전환시킨 **5G 및 미래 6G 코어 네트워크의 가장 핵심적인 아키텍처 패러다임**으로 확립되었으며, 실무 시스템 운영 시에는 **NF 간 연쇄 장애를 방지하는 서킷 브레이커(Circuit Breaker) 패턴 적용, 제어 평면 보안을 위한 mTLS 및 OAuth 2.0 인가 의무화, NRF 기반 실시간 헬스체크, N4(PFCP) 기반 로컬 UPF 엣지 분산 오케스트레이션**을 결합하여 캐리어 그레이드(Carrier-Grade)의 고가용성과 신뢰성을 완성

#### 한줄 요약
- 5G 코어 SBA는 HTTP/2 REST API와 NRF를 통해 마이크로서비스 제어를 실현하며, CUPS와 서비스 메시를 결합하여 유연성과 가용성을 보장하는 핵심 차세대 코어 아키텍처다.
