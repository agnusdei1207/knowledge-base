---
sidebar:
  order: 108
  label: "108. HTTP/2•HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "HTTP/2•HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
date: "2026-08-13T16:51:54+09:00"
tags: ["notes-network"]
weight: 108
extra:
  question_no: "108"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "비교형: HTTP/2•HTTP/3 선택 조건"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하이퍼텍스트 전송 프로토콜 버전 2(Hypertext Transfer Protocol version 2, HTTP/2)**: TCP에서 다중 스트림을 제공하는 웹 전송 표준이다.
- **하이퍼텍스트 전송 프로토콜 버전 3(Hypertext Transfer Protocol version 3, HTTP/3)**: QUIC에서 독립 스트림을 제공하는 웹 전송 표준이다.
- **전송 제어 프로토콜(Transmission Control Protocol, TCP)**: 신뢰성 있는 바이트 흐름을 제공하는 전송 프로토콜이다.
- **빠른 UDP 인터넷 연결(Quick UDP Internet Connections, QUIC)**: UDP 기반 연결•스트림•보안을 통합한 전송 프로토콜이다.
- **웹 전송 표준**: HTTP 의미를 다중 스트림•헤더 압축•신뢰 전송으로 교환하는 규격이다.
- **스트림 간 선두 차단**: 하나의 전송 손실 복구가 관련 없는 다른 스트림의 진행까지 막는 현상이다.

</details>

- 정의/개념: **HTTP/2**•**HTTP/3** — 같은 HTTP 의미를 각각 TCP와 QUIC의 다중 스트림으로 전달하는 **웹 전송 표준**이다.
- 배경/필요성: TCP 손실 복구가 다른 스트림까지 막는 **스트림 간 선두 차단**이 발생한다.

#### 한줄 요약

- HTTP/2는 여러 요청이 한 TCP 복구를 함께 기다리지만 HTTP/3는 손실된 QUIC 스트림만 복구해 나머지를 진행시킨다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **HTTP/3 운영•보안 제약**: UDP 차단•암호화 관측 저하•0-RTT 재전송 위험이다.
- **사용자 데이터그램 프로토콜(User Datagram Protocol, UDP)**: 비연결형 데이터그램을 전달하는 전송 프로토콜이다.
- **왕복 시간(Round-Trip Time, RTT)**: 요청 전송부터 응답 수신까지 걸리는 시간이다.
- **대체 서비스(Alternative Service, Alt-Svc)**: 서버가 지원하는 대체 프로토콜•주소를 클라이언트에 알리는 HTTP 필드이다.

</details>

- 공통 HTTP 의미에서 **TCP**와 **QUIC**의 전송 계층 차이가 핵심이다.
- **Alt-Svc** 발견과 스트림 손실 격리•연결 이동으로 **RTT**를 줄이는 것이 핵심이다.
- **UDP** 차단•0-RTT의 **HTTP/3 운영•보안 제약**이 핵심이다.

#### 한줄 요약

- 이동과 손실이 잦으면 HTTP/3 이점이 커지지만 UDP가 막힌 환경에서는 HTTP/2로 안전하게 돌아갈 수 있어야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **전송 계층 보안 1.3(Transport Layer Security 1.3, TLS 1.3)**: 전송 구간 암호화와 인증을 제공하는 보안 프로토콜이다.
- **HTTP/2 헤더 압축(HTTP/2 Header Compression, HPACK)**: HTTP/2 필드의 중복을 줄이는 압축 방식이다.
- **HTTP/3 헤더 압축(HTTP/3 Header Compression, QPACK)**: QUIC의 독립 스트림에 맞게 설계된 헤더 압축 방식이다.

</details>

```text
HTTP 전송 구조
├─ HTTP 의미 계층
├─ HTTP/2•HPACK 계층
├─ TCP•TLS 전송부
├─ HTTP/3•QPACK 계층
└─ QUIC•TLS 1.3 전송부
```

가지의 의미: 공통 의미와 버전별 압축•전송 책임을 분리한 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| HTTP 의미 계층 | 메서드•상태•필드 의미 유지 |
| HTTP/2•HPACK 계층 | TCP 스트림에 **HPACK** 프레임•헤더 압축 적용 |
| TCP•TLS 전송부 | HTTP/2에 **TCP** 신뢰 전송•보안 제공 |
| HTTP/3•QPACK 계층 | QUIC 스트림에 **QPACK** 프레임•헤더 압축 적용 |
| QUIC•TLS 1.3 전송부 | HTTP/3에 **TLS 1.3** 스트림•복구•보안 제공 |

> 요약: HTTP 의미는 같고 전송•압축 계층이 다르다.

#### 한줄 요약

- 요청의 뜻은 같지만 HTTP/2는 TCP와 HPACK, HTTP/3는 QUIC과 QPACK을 사용해 스트림을 전달한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HTTP/2 대체(Fallback)**: UDP 차단이나 QUIC 실패 시 TCP•TLS 기반 HTTP/2로 전환하는 동작이다.
- **QUIC•TLS 협상**: UDP 연결•암호 매개변수•연결 ID를 설정하는 단계이다.
- **독립 스트림 전송**: 요청별 QUIC 스트림에서 손실 복구를 분리해 전달하는 단계이다.

</details>

```text
Alt-Svc•지원 버전 확인
        │
        ▼
1. QUIC•TLS 협상
        ├─ 성공
        │    │
        │    ▼
        │  2. 독립 스트림 전송
        │    └── HTTP/3 응답 반환
        │
        └─ 실패
             │
             ▼
           3. HTTP/2 대체
             └── HTTP/2 응답 반환
```

### 동작 원리

1. **QUIC•TLS 협상**: UDP 연결•암호•연결 ID의 **QUIC•TLS 협상**을 수행한다.
2. **독립 스트림 전송**: 요청별 QUIC 스트림에서 **독립 스트림 전송**을 수행한다.
3. **HTTP/2 대체**: QUIC 실패 시 **HTTP/2 대체**로 TCP 연결에 전환한다.
> 요약: HTTP/3 우선 협상 후 실패 시 HTTP/2로 전환한다.

#### 한줄 요약

- 먼저 QUIC으로 연결해 독립 스트림을 쓰고 UDP가 막히거나 실패하면 TCP 기반 HTTP/2로 자동 전환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **의견 요청 문서(Request for Comments, RFC)**: 인터넷 기술 규격을 공개하는 문서 체계이다.

</details>

| HTTP 버전 | **HTTP/2** | **HTTP/3** |
|:---|:---|:---|
| 적용 기준 | 저손실 고정망•기존 TCP 장비 활용 | 손실•이동이 잦고 UDP 사용 가능 |
| 핵심 특징 | **RFC** 9113의 TCP•HPACK | RFC 9114의 QUIC•QPACK |
| 한계 | TCP 손실의 전체 스트림 지연 | UDP 차단•0-RTT 재전송•관측 제약 |

> 요약: 손실•이동성•UDP 통과로 버전을 선택한다.

#### 한줄 요약

- 안정된 고정망과 기존 장비 활용은 HTTP/2, 손실과 주소 변경이 잦은 이동망은 HTTP/3가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **0 왕복 시간 요청 재전송(Zero Round-Trip Time Request Replay, 0-RTT 요청 재전송)**: 공격자가 이전 조기 데이터를 다시 보내 비멱등 업무를 중복 실행하게 할 수 있는 위험이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기업망의 UDP 차단 | **HTTP/2 대체** 경로 | 연결 성공률 유지 |
| 0-RTT 요청 재전송 | 멱등 요청만 조기 전송 | 중복 처리 위험 감소 |
| 암호화 전송의 관측 저하 | 종단 지표•대체 사유 수집 | 장애 원인 식별 |

#### 한줄 요약

- 일부 사용자부터 HTTP/3를 적용하고 지연•손실•HTTP/2 대체 비율을 검증한 뒤 범위를 확대한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **HTTP 버전 선택**: 손실•이동성•UDP 통과 가능성과 대체 경로를 근거로 HTTP/2와 HTTP/3을 결정하는 판단이다.

</details>

- 저손실•UDP 차단 환경은 **HTTP/2**, 손실•이동 환경은 **HTTP/3**을 택하는 **HTTP 버전 선택**이 필요하다.

#### 한줄 요약

- HTTP/3 도입은 사용률보다 사용자 지연이 줄고 실패 때 HTTP/2로 돌아가며 보안 관측이 유지되는지로 판단해야 한다.
