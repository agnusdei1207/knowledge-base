---
sidebar:
  order: 38
  label: "038. 5G 코어 SBA (5G Core SBA)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G 코어 서비스 기반 아키텍처 : SBA (Service Based Architecture)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 38
extra:
  question_no: "038"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "5GC SBA 구성요소, NRF 서비스 검색 및 CUPS 제어 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5G 코어(5G Core, 5GC)**: 네트워크 기능 가상화(NFV)와 클라우드 네이티브 기반으로 제어 평면과 사용자 평면을 완전 분리한 차세대 이동통신 코어 시스템.
- **서비스 기반 아키텍처(Service-Based Architecture, SBA)**: 코어망의 제어 평면 기능(Network Function, NF)들을 마이크로서비스로 분할하고, 웹 표준 RESTful API(HTTP/2, JSON)를 통해 상호 통신하도록 설계한 5GC 표준 구조.
- **네트워크 저장소 기능(Network Repository Function, NRF)**: 제어 평면 내 모든 NF 인스턴스의 프로파일과 서비스 상태를 등록받아 관리하고 동적 서비스 검색(Discovery)을 중계하는 중앙 서비스 디렉터리.

</details>

- 정의/개념: 5G 코어 제어 평면 기능들을 독립적인 **NF(Network Function)** 로 모듈화하고, **웹 표준 인터페이스(HTTP/2, JSON)** 와 **NRF** 기반의 서비스 검색을 통해 상호 연동하는 **클라우드 네이티브 코어 아키텍처(SBA)**
- 배경/필요성: 기존 4G 코어의 전용 하드웨어 및 점대점(Point-to-Point) 참조점 결합으로 인한 신규 서비스 배포 지연, 확장성 한계 및 E2E 슬라이싱 구현의 기술적 제약 해소

#### 한줄 요약
- 제어 평면 NF들을 마이크로서비스로 모듈화하고 HTTP/2 API와 NRF로 동적 연동하는 클라우드 네이티브 아키텍처이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **제어·사용자 평면 분리(CUPS, Control and User Plane Separation)**: 신호 제어(SMF)와 대용량 패킷 포워딩(UPF)을 물리적·논리적으로 분리하여 각각 독립적으로 확장 및 전진 배치할 수 있도록 한 아키텍처.
- **상태 비저장(Stateless) NF**: NF 인스턴스가 세션 상태 데이터를 자체 메모리에 보관하지 않고 비정형 데이터 저장소(UDSF)에 외부화하여 인스턴스의 무중단 생성·폐기(Auto-scaling)를 가능하게 하는 설계.

</details>

- **웹 표준 프로토콜 적용**: 3GPP 전용 바이너리 프로토콜(Diameter, GTP-C) 대신 HTTP/2 기반 RESTful API 및 JSON 페이로드 채택
- **동적 서비스 등록 및 검색**: NRF를 통한 **서비스 인스턴스 자동 발견(Service Discovery)** 으로 결합도(Coupling) 최소화
- **CUPS 완전 분리**: 제어 평면(SMF)과 사용자 데이터 평면(UPF)을 PFCP(Packet Forwarding Control Protocol)로 분리하여 엣지(MEC) 분산 배치 실현

#### 한줄 요약
- HTTP/2 REST API 통신, NRF 기반 동적 검색, CUPS 분리 및 Stateless 설계를 통해 유연한 확장을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AMF(Access and Mobility Management Function)**: 단말의 등록, 인증, 연결 및 이동성 관리를 전담하는 코어 제어 노드.
- **SMF(Session Management Function)**: PDU 세션 수립, IP 주소 할당 및 UPF의 패킷 포워딩 규칙을 제어하는 세션 관리 노드.
- **UPF(User Plane Function)**: 사용자 패킷의 라우팅, 포워딩, QoS 마킹 및 외부 데이터망(DN) 연동을 수행하는 데이터 플레인 노드.

</details>

```text
[ 5G SBA 제어 평면 (Control Plane / Service-Based Interface Bus) ]

  [ AMF ]     [ SMF ]     [ PCF ]     [ UDM ]     [ AUSF ]
     │           │           │           │           │
 ────┴───────────┴───────────┴───────────┴───────────┴──── (Namf, Nsmf, Npcf, Nnrf 등 HTTP/2 버스)
                             │                                │
                             │                                └──▶ [ NRF (서비스 등록/검색) ]
                             ▼ (N4 인터페이스: PFCP 규격)
 [ 사용자 평면 (User Plane) ]
  [ gNB (5G 기지국) ] ──────── (N3) ────────▶ [ UPF (데이터 라우터) ] ── (N6) ──▶ [ 데이터 네트워크 (DN) ]
```

선의 의미: 제어 평면 NF들은 HTTP/2 서비스 기반 버스로 연동되고, SMF가 N4(PFCP)를 통해 하위 UPF를 원격 제어하는 5GC 구조

| 구성요소 | 책임 | 통신 인터페이스 |
|:---|:---|:---|
| **AMF** | 단말 등록, 이동성 제어, 보안 및 무선 인터페이스(N1/N2) 시그널링 종단 | Namf (HTTP/2) |
| **SMF** | PDU 세션 생애주기 관리, IP 할당, UPF 포워딩 규칙(PFCP) 제어 | Nsmf (HTTP/2) |
| **UPF** | 사용자 패킷 고속 포워딩, 로컬 트래픽 브레이크아웃, 과금 계량 | N3(GTP-U), N4(PFCP) |
| **NRF** | 전체 NF 인스턴스의 프로파일 등록(Heartbeat) 수신 및 서비스 질의 응답 | Nnrf (HTTP/2) |
| **UDM / UDR** | 가입자 인증 데이터(AKA), 서비스 프로파일 저장 및 가입자 상태 관리 | Nudm / Nudr |
| **PCF** | 네트워크 슬라이스별 QoS 정책 및 과금 규칙(PCC) 결정 | Npcf (HTTP/2) |

#### 한줄 요약
- AMF, SMF, PCF, UDM, NRF가 HTTP/2 버스로 제어를 분담하고 UPF가 패킷 전송을 전담한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **패킷 포워딩 제어 프로토콜(Packet Forwarding Control Protocol, PFCP)**: 3GPP 표준 제어 프로토콜로, 제어 노드(SMF)가 사용자 데이터 노드(UPF)에 패킷 처리 규칙(PDR, FAR, QER)을 하달하는 N4 인터페이스 프로토콜.

</details>

```text
1. 단말(UE)이 AMF로 PDU 세션 수립 요청 (N1 NAS 시그널링)
            │
            ▼
2. AMF가 NRF로 최적의 SMF 인스턴스 검색 (Nnrf_NFDiscovery_Request)
            │
            ▼
3. SMF가 PCF 정책 및 UDM 가입 정보 조회 후 세션 생성
            │
            ▼
4. SMF가 N4(PFCP)를 통해 UPF에 패킷 탐지 및 포워딩 규칙(PDR/FAR) 하달
            │
            ▼
5. 단말 ➔ gNB ➔ UPF ➔ 외부 데이터망(DN) 간 엔드투엔드 데이터 세션 개통
```

**동작 원리**

1. **세션 요청 인입**: 단말의 무선 세션 연결 요청을 AMF가 수신
2. **동적 NF 발견**: AMF가 NRF를 질의하여 단말의 위치 및 슬라이스(S-NSSAI)에 최적화된 SMF 인스턴스 URI 획득
3. **정책 및 세션 확립**: SMF가 PCF로부터 QoS 규칙을 수신하고 IP 풀에서 IP 주소 할당
4. **사용자 평면 규칙 주입**: SMF가 UPF에 PFCP 패킷 탐지 규칙(PDR)과 포워딩 동작 규칙(FAR)을 주입하여 데이터 파이프라인 수립

#### 한줄 요약
- 단말 요청 인입, NRF를 통한 SMF 검색, 정책 수립, PFCP 포워딩 규칙 하달 순으로 세션이 개통된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **참조점 인터페이스(Reference Point Interface)**: 4G 코어에서 특정 장비 간 1:1로 고정 정의된 통신 경로(예: S11, S5/S8, S6a 등).

</details>

| 비교 항목 | 4G LTE 코어 (EPC) | 5G 코어 (5GC SBA) |
|:---|:---|:---|
| **아키텍처 모델** | 모놀리식 전용 하드웨어 / 점대점 참조점 | **마이크로서비스 / 서비스 기반 버스 (SBA)** |
| **제어 평면 프로토콜** | GTP-C, Diameter, SS7 (바이너리 전용망) | **HTTP/2, RESTful API, JSON (웹 표준)** |
| **NF 검색 방식** | DNS 기반 정적 IP 매핑 | **NRF 기반 실시간 동적 등록 및 검색 (Discovery)** |
| **제어/사용자 평면 분리** | SGW/PGW 결합 (CUPS 제한적) | **SMF(제어)와 UPF(데이터) 완전 분리 (CUPS)** |
| **배포 및 확장성** | 전용 어플라이언스 / 펌웨어 업그레이드 | **쿠버네티스 컨테이너 / 수평 자동 확장(Auto-scaling)** |

#### 한줄 요약
- 4G EPC의 점대점 전용 장비 구조에서 5GC SBA의 HTTP/2 기반 마이크로서비스 클라우드 아키텍처로 진화했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **서킷 브레이커(Circuit Breaker)**: 특정 마이크로서비스(NF) 장애 시 호출 차단(Open)을 통해 시스템 전체로의 연쇄 장애(Cascading Failure) 전파를 방지하는 안정성 패턴.
- **상호 TLS(mTLS)**: 통신하는 클라이언트 NF와 서버 NF가 상호 간의 X.509 인증서를 검증하여 세션 암호화와 무인가 접근을 차단하는 보안 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 제어 NF 장애 시 호출 타임아웃 대기로 인한 코어망 연쇄 마비 | NF 서비스 메시 내 **서킷 브레이커(Circuit Breaker)** 및 타임아웃 적용 | 연쇄 장애 차단 및 정상 NF 서비스 연속성 유지 |
| HTTP/2 웹 API 노출에 따른 제어 평면 위변조 및 무인가 NF 접속 위협 | NF 간 **상호 TLS(mTLS)** 암호화 및 **OAuth 2.0 토큰 인가** 의무화 | 비인가 NF 위장 통신 차단 및 시그널링 기밀성 확보 |
| NF 비정상 종료 시 NRF 디렉터리 내 Stale 정보 잔존으로 라우팅 실패 | NRF 기반 **주기적 하트비트(Heartbeat)** 및 상태 헬스체크 강제 | 비정상 NF 즉시 등록 해제 및 최신 가용 NF로의 라우팅 보증 |

#### 한줄 요약
- 서킷 브레이커로 연쇄 장애를 차단하고, mTLS/OAuth 2.0으로 API 보안을 확립하며, 헬스체크로 NRF 정합성을 유지한다.

## Ⅶ. 결론

- 5G 코어망은 클라우드 네이티브 **SBA 아키텍처**를 채택하여 민첩한 신규 기능 배포와 **E2E 네트워크 슬라이싱**을 완성하되, 제어 평면의 신뢰성을 보장하기 위해 **mTLS/OAuth 2.0 보안 체계**와 **서비스 메시 기반 복원력(Circuit Breaker)** 패턴을 결합하여 가용성과 유연성을 동시에 확보

#### 한줄 요약
- SBA 마이크로서비스 아키텍처와 제로 트러스트 보안을 결합하여 고성능 5GC 인프라를 완성한다.
