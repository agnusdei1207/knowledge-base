---
sidebar:
  order: 38
  label: "038. 5G 코어 SBA"
  badge: { text: "기출 • 70%", variant: note }
title: "5G 코어 SBA"
date: "2026-08-13T16:52:00+09:00"
tags: ["notes-network"]
weight: 38
extra:
  question_no: "038"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "135회 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: 초고속, 초저지연, 대규모 연결을 제공하는 차세대 이동통신 기술 표준이다.
- **4세대 이동통신(Fourth-Generation Mobile Communication, 4G)**: LTE 중심의 4세대 이동통신 기술 표준 규격이다.
- **서비스 기반 아키텍처(Service-Based Architecture, SBA)**: 5G 코어의 제어 평면 망 기능(NF)들을 독립적인 웹 서비스 단위로 모듈화하고 RESTful API 기반으로 통신하는 아키텍처이다.

</details>

- 정의/개념: **5G 코어 SBA(Service-Based Architecture)**는 5G 코어망의 제어 평면(Control Plane) Network Function(NF)들을 웹 표준 RESTful API 기반으로 모듈화하고, NRF를 통해 동적 서비스 등록, 발견, 호출을 수행하는 클라우드 네이티브 코어 아키텍처이다.
- 배경/필요성: 기존 4G EPC의 점대점(Point-to-Point) 하드코딩 인터페이스 구조로 인한 망 확장성 제약, 신규 기능 추가의 복잡성 및 제어/사용자 평면 결합 한계를 극복하기 위해 도입되었다.

#### 한줄 요약

- 5G 코어 제어 평면의 NF들을 RESTful API 기반 서비스 단위로 모듈화하여 NRF 자동 발견 및 유연한 자원 확장을 제공하는 클라우드 네이티브 아키텍처.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **망 기능(Network Function, NF)**: 5G 코어 아키텍처 내에서 독자적인 기능과 서비스 API를 제공하는 소프트웨어 모듈 단위이다.
- **망 기능 저장소(Network Repository Function, NRF)**: NF 인스턴스의 프로필 등록, 상태 관리 및 동적 서비스 검색(Discovery)을 전담하는 코어 엔티티이다.
- **세션 관리 기능(Session Management Function, SMF)**: PDU 세션의 생성을 제어하고 UPF의 사용자 패킷 전달 규칙을 지정하는 제어 평면 NF이다.
- **사용자면 기능(User Plane Function, UPF)**: SMF의 PFCP 제어 신호에 따라 사용자 데이터 패킷의 라우팅, 캡슐화 및 엣지 분기를 수행하는 사용자 평면 NF이다.
- **느슨한 결합(Loose Coupling)**: NF 인스턴스가 타 NF의 IP나 하드웨어 위치에 고정되지 않고 API 인터페이스 수준에서 유연하게 연동되는 구조적 특성이다.

</details>

- **RESTful API 기반 SBI 통신**: HTTP/2, JSON, OpenAPI 규격을 사용하여 제어 평면 NF 간 표준 서비스 기반 인터페이스(SBI) 통신을 실행한다.
- **NRF 중심 동적 발견(Discovery)**: 신규 NF 인스턴스는 NRF에 프로필을 동적 등록하며, 타 NF는 NRF 조회를 통해 최적의 대상 NF를 자동 발굴·연결한다.
- **제어/사용자 평면 완벽 분리(CUPS)**: 세션 제어(SMF)와 패킷 전달(UPF)을 완전 분리하여 독립적인 오토스케일링과 에지 전진 배치를 구현한다.

#### 한줄 요약

- NRF 기반 NF 자동 등록 및 동적 발견, HTTP/2 REST API 표준 인터페이스 적용, CUPS 분리를 통한 독립적 자원 스케일링 제공.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **접속·이동성 관리 기능(Access and Mobility Management Function, AMF)**: 단말의 무선 접속, 가입자 인증 및 이동성을 관장하는 5G 제어 평면 NF이다.
- **통합 데이터 관리(Unified Data Management, UDM)**: 가입자 프로필, 인증 자격 증명 및 암호화 키를 관리하는 5G 데이터베이스 NF이다.

</details>

```text
5G 코어 서비스 기반 아키텍처 (5GC SBA)
└─ 서비스 기반 인터페이스 통신 버스 (SBI Bus)
   ├─ 접속 및 이동성 관리 기능 (AMF)
   ├─ 통합 데이터 관리 (UDM)
   ├─ 망 기능 저장소 (NRF)
   ├─ 정책 제어 기능 (PCF)
   └─ 세션 관리 기능 (SMF)
      └─ 사용자 평면 기능 (UPF - N3/N4/N6)
```

선의 의미: HTTP/2 기반 SBI 통신 버스를 중심으로 제어 평면 NF들이 연동되고, SMF가 PFCP(N4) 프로토콜을 통해 UPF를 제어하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| AMF (Access & Mobility Mgmt Function) | 단말 N1/N2 무선 제어 신호 수신, 가입자 5G 인증 및 이동성 관리 |
| UDM (Unified Data Management) | 5G 가입자 식별자(SUPI/SUCI) 및 서비스 권한 프로필 통합 관리 |
| NRF (Network Repository Function) | 전체 NF 인스턴스 등록, 상태 모니터링 및 동적 서비스 발견(Discovery) 검색 제공 |
| PCF (Policy Control Function) | 서비스별 QoS 정책 및 네트워크 슬라이스 인가 규칙을 통제하여 SMF에 제공 |
| SMF (Session Management Function) | PDU 세션 생성/변경/해제 및 UPF 패킷 전달 규칙(PDR/FAR) 생성 및 하향 전달 |
| UPF (User Plane Function) | N4 규격(PFCP) 제어에 따라 N3 무선 구간과 N6 외부망 간 사용자 패킷 라우팅 |

#### 한줄 요약

- AMF, SMF, UDM, PCF 등의 제어 NF들이 SBI 통신 버스로 연결되고 NRF를 통해 상호 발견하며 SMF가 UPF 데이터 경로를 제어하는 구조.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **전달 규칙(Forwarding Rule, PFCP)**: SMF가 PFCP 프로토콜을 통해 UPF에 설치하는 패킷 탐지(PDR) 및 전달 행동(FAR) 지침이다.
- **세션 기능 발견(NF Discovery)**: AMF가 가입자 요구 세션을 처리하기 위해 NRF에 최적의 가용 SMF 인스턴스 검색을 요청하는 절차이다.

</details>

```text
AMF: 가입자 접속 및 세션 발생
      │
      v
1. AMF -> NRF: 가용 SMF 검색 및 서비스 발견
      │
      v
2. NRF -> AMF: 가용 SMF 엔드포인트 및 상태 반환
      │
      v
3. AMF -> SMF: 세션 생성 요청
      │
      v
4. SMF -> UPF: PFCP 패킷 전달 규칙 설치
      │
      v
PDU 세션 확립 완료
```

### 동작 원리

1. **AMF -> NRF: 가용 SMF 검색 및 서비스 발견**: 조건 전달
2. **NRF -> AMF: 가용 SMF 엔드포인트 및 상태 반환**: 대상 선택
3. **AMF -> SMF: 세션 생성 요청**: PDU 컨텍스트 생성
4. **SMF -> UPF: PFCP 패킷 전달 규칙 설치**: 데이터 경로 확립

#### 한줄 요약

- AMF의 NRF 세션 기능 발견, SMF 정보 수신, 세션 생성 요청 및 SMF-UPF 간 PFCP 규칙 설치를 통한 PDU 세션 확립 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 소프트웨어 모듈 간 기능 및 데이터를 표준 규격으로 주고받는 통신 인터페이스이다.
- **서비스 기반 인터페이스(Service-Based Interface, SBI)**: 5G 코어 제어 평면 NF 간 HTTP/2 RESTful 통신을 가능하게 하는 3GPP 표준 인터페이스 버스이다.

</details>

| 비교 항목 | **5G 코어 SBA (Service-Based Architecture)** | **4G EPC P2P (Point-to-Point)** |
|:---|:---|:---|
| 네트워크 구조 | 클라우드 네이티브 서비스 통신 버스 (SBI) | 노드 간 1:1 하드코딩 전용 인터페이스 |
| 핵심 프로토콜 | HTTP/2, JSON, OpenAPI RESTful API | GTP-C, Diameter, S1-AP/X2-AP |
| 서비스 발견 및 확장 | NRF 기반 동적 서비스 자동 발견 및 NF 독립 스케일링 | MME/SGW 노드에 IP 및 포트 고정 하드코딩 |
| 제어/사용자 분리 | CUPS 체계 적용으로 SMF와 UPF 완전 독립 구성 | SGW/PGW 제어 및 사용자 기능 부분 결합 |
| 네트워크 슬라이싱 | 슬라이스별 전용 NF 생성 및 가상화 동적 배정 | 슬라이스 논리적 분리 및 차등 제어 불가능 |

> 요약: 4G P2P 구조 대비 5G SBA는 클라우드 네이티브 기반 서비스 동적 발견과 독립적 오토스케일링을 지원.

#### 한줄 요약

- 4G EPC의 점대점 구조 대비 5G SBA는 HTTP/2 API 기반 동적 서비스 발견과 유연한 독립 확장을 제공하는 아키텍처.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **회로 차단기(Circuit Breaker)**: 연동 NF의 트래픽 폭주나 장애 발생 시 호출을 즉시 차단하고 우회하여 연쇄 장애(Cascading Failure)를 방지하는 소프트웨어 패턴이다.
- **상호 전송 계층 보안(Mutual Transport Layer Security, mTLS)**: SBI API 통신 양단간 X.509 인증서를 통해 기계 신원을 상호 검증하는 보안 기술이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| NRF 만료 노드 반환 | NF 인스턴스 비정상 종료 시 NRF 등록 캐시 잔류 | NRF 헬스체크 Heartbeat 주기화 및 만료 자동 즉시 제거 | 비정상 NF 호출 실패 사전 예방 |
| SBI API 무단 호출 | 서비스 버스 내 불인가 NF의 REST API 부적절 접근 | mTLS 암호화 채널 및 OAuth 2.0 기반 API 토큰 인가 적용 | 코어망 위장 호출 차단 및 보안성 확보 |
| 연쇄 장애 확산 | 특정 NF (예: UDM) 지연 시 타 NF(AMF)의 호출 대기 폭주 | Service Mesh 연동 타임아웃 및 Circuit Breaker 패턴 도입 | 연쇄 장애 차단 및 시스템 복원력 확보 |
| API 버전 불일치 | 신규 NF 업데이트 시 레거시 NF 간 API 규격 상충 | OpenAPI 스키마 버전 관리 및 API 게이트웨이(BSF) 수용 | 하위 호환성 유지 및 무중단 업그레이드 |

#### 한줄 요약

- mTLS/OAuth2 인증 통제, NRF 헬스체크 자동화, Service Mesh 기반 Circuit Breaker 도입으로 5G 코어 SBA 안정성 확보.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **서비스 발견(Service Discovery)**: NRF를 통해 가용 NF의 URI, 지원 슬라이스 및 주소 정보를 수신하여 서비스 호출 대상을 결정하는 동적 매핑 과정이다.

</details>

- NF 호출은 **mTLS**•**OAuth2**, 장애 확산은 **회로 차단기** 적용

#### 한줄 요약

- NRF 중심 동적 서비스 발견 체계 및 서킷 브레이커 기반 코어망 장애 격리 통제 구현 필수.
