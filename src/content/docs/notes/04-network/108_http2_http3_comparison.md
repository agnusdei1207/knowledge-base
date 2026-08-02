---
sidebar:
  order: 108
  label: "108. HTTP/2·HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
  badge:
    text: "미출제 · 50%"
    variant: note
title: "HTTP/2·HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
date: "2026-08-02T12:00:00+09:00"
tags: ["notes-network"]
weight: 108
extra:
  question_no: "108"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "비교형: HTTP/2·HTTP/3 선택 조건"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **웹 전송 표준**: HTTP/2·HTTP/3은 같은 HTTP 의미를 각각 TCP·QUIC 스트림에 다중화해 전달하는 웹 전송 표준이다.

</details>

- 정의/개념: **HTTP/2·HTTP/3**은 같은 HTTP 의미를 각각 TCP와 QUIC의 다중 스트림으로 전달하는 **웹 전송 표준**
- 배경/필요성: TCP 손실의 **스트림 간 선두 차단** 완화

### 쉽게 이해하기 (학습용)

- HTTP/2는 여러 요청이 한 TCP 복구를 함께 기다리지만 HTTP/3는 손실된 QUIC 스트림만 복구해 나머지를 진행시킨다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **운영·보안 제약**: HTTP/3의 운영·보안 제약은 UDP 차단·암호화 관측 저하와 0-RTT 재전송 위험을 함께 관리해야 하는 점이다.

</details>

- 공통 HTTP 의미와 **TCP·QUIC 전송 계층 차이**
- **Alt-Svc** 발견과 스트림 손실 격리·연결 이동
- UDP 차단·0-RTT의 **운영·보안 제약**

### 쉽게 이해하기 (학습용)

- 이동과 손실이 잦으면 HTTP/3 이점이 커지지만 UDP가 막힌 환경에서는 HTTP/2로 안전하게 돌아갈 수 있어야 한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **QUIC·TLS 1.3 전송부**: QUIC·TLS 1.3 전송부는 HTTP/3에 독립 스트림·손실 복구·연결 이동·통합 보안을 제공한다.

</details>

```mermaid
block-beta
    columns 2
    A["HTTP 의미 계층"]:2
    B["HTTP/2·HPACK 계층"]
    D["HTTP/3·QPACK 계층"]
    C["TCP·TLS 전송부"]
    E["QUIC·TLS 1.3 전송부"]
    A --- B
    A --- D
    B --- C
    D --- E
```

| 구성요소 | 책임 |
|:---|:---|
| HTTP 의미 계층 | **메서드·상태·필드 의미** 유지 |
| HTTP/2·HPACK 계층 | TCP 스트림의 **프레임·헤더 압축** |
| TCP·TLS 전송부 | HTTP/2의 **신뢰 전송·보안** 제공 |
| HTTP/3·QPACK 계층 | QUIC 스트림의 **프레임·헤더 압축** |
| QUIC·TLS 1.3 전송부 | HTTP/3의 **스트림·복구·보안** 제공 |

> 요약: HTTP 의미는 같고 전송·압축 계층이 다름

### 쉽게 이해하기 (학습용)

- 요청의 뜻은 같지만 HTTP/2는 TCP와 HPACK, HTTP/3는 QUIC과 QPACK을 사용해 스트림을 전달한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **3. HTTP/2 대체**: 클라이언트는 UDP 차단이나 QUIC 협상 실패 시 TCP·TLS 기반 HTTP/2 경로로 자동 전환한다.

</details>

```mermaid
sequenceDiagram
    participant 클라이언트
    participant 서버
    participant QUIC
    participant TCP
    클라이언트->>서버: HTTP 버전 정보 요청
    서버-->>클라이언트: Alt-Svc·지원 버전
    클라이언트->>QUIC: 1. QUIC·TLS 협상
    alt QUIC 사용 가능
        클라이언트->>QUIC: 2. 독립 스트림 전송
        QUIC->>서버: HTTP/3 요청
        서버-->>클라이언트: HTTP 응답
    else QUIC 실패
        클라이언트->>TCP: 3. HTTP/2 대체
        TCP->>서버: HTTP/2 요청
        서버-->>클라이언트: HTTP 응답
    end
```

**동작 원리**

1. **QUIC·TLS 협상**: UDP 연결·암호·연결 ID 생성
2. **독립 스트림 전송**: 요청별 QUIC 스트림으로 전달
3. **HTTP/2 대체**: QUIC 실패 시 TCP 연결로 전환
> 요약: HTTP/3 우선 협상 후 실패 시 HTTP/2 전환

### 쉽게 이해하기 (학습용)

- 먼저 QUIC으로 연결해 독립 스트림을 쓰고 UDP가 막히거나 실패하면 TCP 기반 HTTP/2로 자동 전환한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **HTTP/3**: HTTP/3는 QUIC의 독립 스트림으로 손실을 격리하고 연결 이동을 지원해 손실·주소 변경이 잦은 환경에 유리하다.

</details>

| HTTP 버전 | HTTP/2 | HTTP/3 |
|:---|:---|:---|
| 적용 기준 | **저손실 고정망·기존 TCP 장비** 활용 | 손실·이동이 잦고 **UDP 사용 가능** |
| 핵심 특징 | **RFC 9113 TCP·HPACK** | **RFC 9114 QUIC·QPACK** |
| 한계 | TCP 손실의 **전체 스트림 지연** | **UDP 차단·0-RTT 재전송·관측 제약** |

> 요약: 손실·이동성·UDP 통과로 버전 선택

### 쉽게 이해하기 (학습용)

- 안정된 고정망과 기존 장비 활용은 HTTP/2, 손실과 주소 변경이 잦은 이동망은 HTTP/3가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **0-RTT 요청 재전송**: 0-RTT 요청 재전송은 공격자가 이전 조기 데이터를 다시 보내 비멱등 업무를 중복 실행하게 할 수 있는 위험이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기업망의 **UDP 차단** | **HTTP/2 자동 대체 경로** | **연결 성공률 유지** |
| **0-RTT 요청 재전송** | **멱등 요청만 조기 전송** | **중복 처리 위험 감소** |
| 암호화 전송의 **관측 저하** | **종단 지표·대체 사유 수집** | **장애 원인 식별** |

### 쉽게 이해하기 (학습용)

- 일부 사용자부터 HTTP/3를 적용하고 지연·손실·HTTP/2 대체 비율을 검증한 뒤 범위를 확대한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **HTTP/2**: HTTP/2는 저손실 고정망과 UDP가 차단된 기업망에서 기존 TCP 기반 장비·관측 체계를 활용하기에 적합하다.

</details>

- 저손실·UDP 차단 환경은 **HTTP/2**, 손실·이동 환경은 **HTTP/3** 선택

### 쉽게 이해하기 (학습용)

- HTTP/3 도입은 사용률보다 사용자 지연이 줄고 실패 때 HTTP/2로 돌아가며 보안 관측이 유지되는지로 판단해야 한다.
