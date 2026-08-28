---
sidebar:
  order: 19
  label: "019. L4•L7 로드 밸런서"
  badge:
    text: "기출 · 50%"
    variant: note
title: "로드 밸런서 L4•L7 (Load Balancer L4 L7)"
date: "2026-08-26T13:40:30+09:00"
tags:
  - "notes-network"
weight: 19
extra:
  question_no: "19"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "L4 및 L7 부하 분산 계층 구조와 헬스 체크 및 세션 유지"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Load Balancer (로드 밸런서)**: 단일 가상 IP(VIP)로 인입되는 트래픽을 백엔드의 여러 서버 인스턴스로 분산 전달하는 전송/응용 계층 장치.
- **VIP (Virtual IP Address)**: 클라이언트가 서비스에 접근하는 단일 공용 대표 IP 주소로, 실제 백엔드 서버들의 물리적 IP를 은닉.

</details>

- 정의/개념: 단일 대표 가상 IP(VIP)를 통해 **5-튜플(L4) 또는 HTTP/URL/쿠키(L7) 정보를 분석하여 다중 백엔드 서버 풀로 분산하는 부하 분산 시스템**
- 배경/필요성: 단일 서버 수직 확장(Scale-Up)은 처리량을 올릴수록 **장비 등급을 높이는 비용이 가파르게 붙고 그 장비 하나가 단일 장애점으로 남는 대가**를 함께 치렀으므로, 클라이언트 앞단에 대표 가상 IP(VIP)를 세워 실제 서버 집합을 감추는 분산 계층을 두고 고가의 수직 확장을 값싼 서버 다수의 수평 확장으로 대체할 필요

#### 한줄 요약
- L4는 헤더만 보므로 빠른 대신 콘텐츠 기반 분기가 불가능하고, L7은 페이로드를 해석해 정교하게 나누는 대신 세션을 종단 처리하는 연산 비용을 부담한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DSR (Direct Server Return)**: 요청 트래픽만 로드 밸런서를 통과하고, 응답 트래픽은 백엔드 서버가 클라이언트로 직접 전송하여 대역폭 병목을 제거하는 L4 모드.
- **Sticky Session (세션 지속성)**: 동일 클라이언트의 연속된 요청을 최초 연결된 동일 백엔드 서버로 고정 매핑하는 세션 어피니티 기능.

</details>

- 단일 가상 IP(VIP)를 통해 백엔드 서버 팜을 추상화하고 은닉하는 **단일 진입점 제공**
- TCP 연결 및 HTTP 200 OK 상태를 지속 감시하여 장애 서버를 격리하는 **주기적 다계층 헬스 체크**
- L4(초고속 5-튜플/DSR)와 L7(URL/쿠키/TLS 오프로딩)의 **계층별 분산 아키텍처 지원**

#### 한줄 요약
- VIP 추상화, 다계층 헬스 체크, L4 초고속 분산 및 L7 지능형 콘텐츠 라우팅을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Listener (리스너)**: VIP와 특정 프로토콜/포트(HTTP 80, HTTPS 443)에서 클라이언트 요청을 수신 대기하는 컴포넌트.
- **Target Group (백엔드 서버 풀)**: 실제 비즈니스 로직을 처리하는 동일 워크로드 서버 인스턴스들의 집합.

</details>

```text
[L4 / L7 로드 밸런서 트래픽 분산 및 헬스체크 아키텍처]
|-- Client Layer (HTTPS 443 -> VIP:443 Request 인입)
`-- Load Balancer Engine (L4 NLB / L7 ALB)
    |-- VIP Listener (Port 80/443 수신, SSL/TLS Termination)
    |-- Health Check Engine (L3 ICMP, L4 TCP 3-Way, L7 HTTP GET `/health`)
    |-- Scheduling Algorithm (Round-Robin, Least Connection, IP Hash)
    `-- Session Affinity Module (Cookie / Source IP Sticky Session)
`-- Backend Server Target Group
    |-- Server 1 (Active / Healthy: 정상 트래픽 분산)
    |-- Server 2 (Active / Healthy: 정상 트래픽 분산)
    `-- Server 3 (Inactive / Unhealthy: 헬스체크 실패로 트래픽 차단 격리)
```

선의 의미: 계층 및 클라이언트의 VIP 요청이 리스너와 스케줄러를 거쳐 헬스체크가 검증된 정상 백엔드 서버로 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **VIP / 리스너** | 클라이언트 트래픽을 단일 IP로 수신하고 **SSL/TLS 암복호화 및 포트별 세션 인입 관리** | 프런트엔드 관문 |
| **스케줄러 엔진** | 라운드 로빈(RR), **최소 연결(Least Connection), 가중치 기반 최적 백엔드 서버 결정** | LB 알고리즘 |
| **백엔드 서버 풀** | 분산된 요청을 실질적으로 처리하는 **복수 개의 워크로드 서버(EC2/컨테이너) 집합** | 타겟 그룹 |
| **상태 확인 (Health Check)**| L4(TCP 핸드셰이크), **L7(HTTP 200 OK) 상태를 주기적으로 계측하여 결함 서버 자동 격리**| 결함 탐지 |
| **세션 지속성 모듈** | 클라이언트 IP 해시 또는 **쿠키(Cookie)를 기반으로 동일 백엔드 서버로의 연결 바인딩 유지**| Sticky Session |

#### 한줄 요약
- VIP 리스너가 클라이언트와 서버 풀 사이에 끼어들어 개별 서버 주소를 알아야 할 이유를 없애고, 헬스 체크가 결함 서버를 미리 격리해 클라이언트가 치를 실패 재시도 비용을 대신 흡수한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **트래픽 분산 2단계 파이프라인**: 1단계 지속적 헬스 체크 기반 활성 풀 관리 $\to$ 2단계 클라이언트 인입 요청 알고리즘 분산.

</details>

```text
로드 밸런서 헬스 체크 및 요청 분산 파이프라인
        │
   1. [헬스 체크 탐사] 백엔드 서버 풀로 HTTP GET `/health` 주기적 발송
        │
   2. [활성 풀 갱신] 정상 200 OK 응답 서버만 Active Pool 유지 (장애 서버 즉시 차단)
        │
   3. [클라이언트 VIP 접속] 클라이언트가 `VIP:443`으로 요청 전송
        │
   4. [스케줄링 알고리즘] Least Connection 연산 및 Sticky Cookie 유무 판정
   ┌────┴───────────────────────────┐
  L4 모드 분산                      L7 모드 분산
   │                                 │
5A. [L4 5-Tuple 포워딩 (NAT/DSR)]    5B. [L7 Reverse Proxy 중계]
   초고속 패킷 헤더 변환 후 전달          TLS 복호화 후 URL 경로 기반 백엔드 재전송
   │                                 │
   └────┬────────────────────────────┘
        ▼
   백엔드 서버 정상 응답 및 클라이언트 반환 완료
```

#### 한줄 요약
- 지속적 헬스 체크로 활성 풀을 갱신하고, 인입 요청을 알고리즘에 따라 정상 서버로 전달한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **L4 Load Balancer (NLB)** vs **L7 Load Balancer (ALB)**: 전송 계층 패킷 레벨 분산(L4)과 응용 계층 역방향 프록시 분산(L7).

</details>

| 비교 항목 | L4 로드 밸런서 (NLB 등) | L7 로드 밸런서 (ALB 등) |
|:---|:---|:---|
| **동작 계층 및 판단 기준** | **전송 계층 (TCP/UDP 포트, 5-튜플)** | **응용 계층 (HTTP URI, Host 헤더, Cookie)** |
| **트래픽 중계 방식** | **패킷 레벨 포워딩 (NAT / DSR)** | **양방향 완전 중계 (Reverse Proxy)** |
| **SSL / TLS 암호화 처리** | 단순 패스스루(TCP Pass-through) 또는 L4 종단 | **TLS 가속 종료(Offloading) 및 인증서 일원화** |
| **처리 성능 및 지연 시간** | **초고속, 극소 지연 (마이크로초 단위)** | HTTP 파싱 및 버퍼링으로 상대적 지연 존재 |
| **주요 최적 적용 분야** | **대규모 TCP 스트리밍, 게임 서버, DNS, VPN** | **웹 애플리케이션, 마이크로서비스(MSA), API Gateway**|

#### 한줄 요약
- L4는 5-튜플 기반 초고속 대용량 전송에 적합하고, L7은 URL/쿠키 기반 정밀 애플리케이션 분기에 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Session Externalization (상태 외부화)**: 세션 데이터를 개별 웹 서버 메모리가 아닌 Redis/Memcached 등 분산 인메모리 저장소에 보관하여 무상태(Stateless) 아키텍처를 구현하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| L4 단순 TCP 헬스 체크 시 웹 서버 내부 DB 락/장애 미탐지 | **HTTP `/health` 경로 및 DB 연동을 검증하는 `L7 심층 헬스 체크` 적용** | 결함 서버의 완전한 트래픽 차단 및 가용성 보장 |
| Sticky Session 사용으로 특정 서버에만 트래픽 과부하 편중 | **`Redis 분산 캐시 기반 세션 상태 외부화` 및 완전 무상태(Stateless)화** | 서버 간 완전한 부하 균등 분산 및 Auto-Scaling |
| 로드 밸런서 장비 자체 고장으로 인한 단일 장애점(SPOF) 발생 | **`Multi-AZ Active-Standby / Active-Active 이중화` 및 DNS GSLB** | 로드 밸런서 장애 시 무중단 자동 절체(Failover) |
| L7 로드 밸런서 TLS 복호화로 인한 내부 백엔드 평문 노출 보안 | **로드 밸런서-백엔드 구간 `내부 TLS 재암호화(End-to-End TLS)`** | 내부 네트워크 도청 방지 및 제로 트러스트 달성 |

#### 한줄 요약
- L7 심층 헬스 체크, Redis 상태 외부화, Multi-AZ 이중화, End-to-End TLS로 운영한다.

## Ⅶ. 결론

- 대용량 전송은 **L4**, URL·쿠키 분기는 **L7** 선택

#### 한줄 요약
- L4/L7 로드 밸런서는 VIP 추상화와 계층별 분산 알고리즘을 통해 대규모 트래픽을 처리하며, 다계층 헬스 체크와 상태 외부화를 통해 고가용성을 보장하는 핵심 인프라 기술이다.
