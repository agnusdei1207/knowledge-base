---
sidebar:
  order: 62
  label: "062. 쿠버네티스 네트워킹 - CNI·Ingress (Kubernetes Networking)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "쿠버네티스 네트워킹 - CNI·Ingress (Kubernetes Networking)"
date: "2026-07-29T23:30:00+09:00"
tags:
  - "notes-network"
weight: 62
extra:
  question_no: "062"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "설계형: 137회 CNI·Ingress·Policy 장문"
---

## 미리 알고가기

- **파드(Pod)**: 하나 이상의 컨테이너가 네트워크 이름공간과 IP 주소를 공유하는 쿠버네티스 실행 단위
- **컨테이너 네트워크 인터페이스(Container Network Interface, CNI)**: 런타임이 플러그인을 호출해 파드 인터페이스·IP·경로를 구성하는 규격
- **서비스(Service)**: 변하는 파드 집합을 고정 가상 IP와 이름으로 추상화하는 쿠버네티스 객체
- **엔드포인트슬라이스(EndpointSlice)**: 서비스가 선택한 준비된 파드의 IP·포트 목록을 분할 저장하는 객체
- **인그레스(Ingress)**: 외부 HTTP·HTTPS 요청을 서비스로 전달하는 호스트·경로 규칙 객체
- **인그레스 컨트롤러(Ingress Controller)**: Ingress 객체를 읽어 프록시·로드밸런서의 실제 전달 규칙을 구성하는 제어기
- **네트워크 정책(NetworkPolicy)**: 선택한 파드에 허용할 수신·송신 대상을 선언하는 객체
- **확장 버클리 패킷 필터(extended Berkeley Packet Filter, eBPF·이비피에프)**: Berkeley Packet Filter 앞에 확장을 뜻하는 소문자 e를 붙인 표기이며, 커널에서 패킷 전달과 정책을 실행하는 기술
- **가상 IP(Virtual IP, VIP)**: 서비스의 여러 파드 종단을 하나의 고정 주소로 나타내는 IP
- **게이트웨이 API(Gateway API)**: 인프라·경로 역할을 분리해 다양한 외부 트래픽 전달을 선언하는 쿠버네티스 API
- **쿠버네티스(Kubernetes)**: 그리스어로 조타수·항해사를 뜻하는 공식 프로젝트명이며, 파드의 배포·확장·복구와 네트워크 객체를 선언적으로 관리하는 플랫폼
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 소프트웨어 객체와 기능을 구조화된 요청으로 다루는 호출 규약
- **하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**: 웹 요청과 응답을 교환하는 응용 계층 프로토콜
- **보안 하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol Secure, HTTPS)**: HTTP를 TLS로 보호해 웹 요청과 응답을 암호화하는 방식
- **전송 계층 보안(Transport Layer Security, TLS)**: 통신 상대를 인증하고 전송 데이터를 암호화하는 보안 프로토콜
- **CNI·VIP·API**: CNI는 Pod 네트워크를 구성하고, VIP는 안정적인 서비스 주소를 제공하며, API는 쿠버네티스 객체의 조회·변경 규약을 제공함
- **HTTP·HTTPS·TLS**: HTTP는 웹 요청을 전달하고, HTTPS는 TLS로 서버 인증과 전송 암호화를 적용한 웹 통신을 제공함

## Ⅰ. 개요

- 정의/개념: CNI·Service·Ingress로 **파드 연결·분산·외부 진입 추상화**
- 배경/필요성: 파드 IP 변동은 **고정 접근점·정책 유지 곤란**

### 쉽게 이해하기 (학습용)

- 파드가 바뀌어도 Service 이름과 외부 진입 규칙은 유지돼 사용자가 같은 서비스에 접속한다

## Ⅱ. 특징

- **CNI**가 파드 인터페이스·IP·노드 간 경로를 구성한다.
- **Service·EndpointSlice**가 준비된 파드로 VIP 트래픽을 분산한다.
- **Ingress·NetworkPolicy**는 외부 경로·허용 통신을 선언한다.

### 쉽게 이해하기 (학습용)

- 정책 객체만 만들어도 CNI 플러그인이 실행 규칙으로 바꾸지 않으면 실제 패킷은 차단되지 않는다

## Ⅲ. 구조 및 구성요소

```mermaid
block-beta
    columns 1
    A["인그레스 컨트롤러"]
    B["Service"]
    C["EndpointSlice"]
    D["NetworkPolicy"]
    E["프록시·eBPF 데이터 경로"]
    A --- B
    B --- C
    C --- D
    D --- E
```

| 구성요소 | 책임 |
|:---|:---|
| 인그레스 컨트롤러 | 호스트·경로·TLS 규칙 실행 |
| Service | VIP 기반 고정 접근점 제공 |
| EndpointSlice | 준비 파드 IP·포트 관리 |
| NetworkPolicy | 허용 수신·송신 대상 선언 |
| 프록시·eBPF 데이터 경로 | 분산·정책 규칙 실행 |

### 쉽게 이해하기 (학습용)

- 외부 요청은 인그레스가 서비스를 고르고 데이터 경로가 준비된 파드 하나로 보낸다

## Ⅳ. 흐름도

```mermaid
sequenceDiagram
    participant API서버
    participant 인그레스
    participant 데이터경로
    participant Service
    API서버->>인그레스: 1. Ingress·Service 규칙 통지
    인그레스->>데이터경로: 2. 프록시 경로 구성
    API서버->>데이터경로: 3. EndpointSlice·정책 통지
    데이터경로->>Service: 4. 종단·정책 규칙 설치
    인그레스->>Service: 5. HTTP·HTTPS 요청
```

**동작 원리**

1. **Ingress·Service 규칙 통지**: API 서버가 외부 경로 객체 전달
2. **프록시 경로 구성**: 컨트롤러가 실제 전달 규칙 생성
3. **EndpointSlice·정책 통지**: 준비 종단·허용 통신 전달
4. **종단·정책 규칙 설치**: 데이터 경로에 분산·차단 반영
5. **HTTP·HTTPS 요청**: 외부 호스트·경로·TLS 요청

### 쉽게 이해하기 (학습용)

- 준비 상태가 실패한 파드는 후보 목록에서 빠져 정상 파드에만 요청이 전달된다

## Ⅴ. 종류 및 비교

| 외부 트래픽 API | Ingress | Gateway API |
|:---|:---|:---|
| 적용 기준 | 단순 웹 서비스 외부 노출 | 다중 팀·고급 경로 정책 |
| 핵심 특징 | HTTP·HTTPS 경로 객체 | 역할 분리·다중 프로토콜 |
| 한계 | 구현별 확장 기능 종속 | 객체·권한 설계 복잡성 |

> 요약: 단순 웹은 Ingress, 역할 분리는 Gateway API다

### 쉽게 이해하기 (학습용)

- 한 팀의 단순 웹 경로는 Ingress, 플랫폼팀과 응용팀이 권한을 나누면 Gateway API가 맞다

## Ⅵ. 실무 고려사항 및 대책

| 고려사항 | 대책 | 효과 |
|:---|:---|:---|
| 정책 객체만 생성 | CNI의 실제 차단 규칙 확인 | 통신 격리 보장 |
| 준비 종단 부재 | EndpointSlice·준비상태 추적 | 503 오류 원인 식별 |
| 외부 경로 권한 충돌 | Gateway API 역할·소유권 분리 | 다중 팀 운영 안정성 |

### 쉽게 이해하기 (학습용)

- 외부 주소가 정상이어도 EndpointSlice에 준비된 파드가 없으면 요청은 전달되지 않는다

## Ⅶ. 결론

- **정책 실행 기능·외부 노출 경로**로 CNI 데이터 경로 선택

### 쉽게 이해하기 (학습용)

- 객체 존재 여부뿐 아니라 준비된 파드까지 실제 패킷이 도달하는지 확인해야 한다.
