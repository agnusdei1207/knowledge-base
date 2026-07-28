---
sidebar:
  order: 72
  label: "072. QoS, DiffServ, IntServ"
  badge:
    text: "미출제 · 50%"
    variant: note
title: "QoS, DiffServ, IntServ"
date: "2026-07-25T12:26:00+09:00"
tags:
  - "notes-network"
weight: 72
extra:
  question_no: "072"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "비교·설계형: DiffServ·IntServ QoS 기반"
---

## 미리 알고가기

- **지터(Jitter)**: 패킷 도착 간격의 흔들림
- **통합 서비스(Integrated Services, IntServ)**: 흐름별 자원을 예약하고 라우터가 상태를 유지하는 QoS 구조
- **차등 서비스(Differentiated Services, DiffServ)**: 패킷 등급을 표시하고 영역 내 라우터가 등급별 동작을 적용하는 QoS 구조
- **홉별 동작(Per-Hop Behavior, PHB)**: DiffServ 노드가 등급별로 수행하는 큐잉·스케줄링·폐기 동작
- **서비스 품질(Quality of Service, QoS·큐오에스)**: Quality·of·Service의 핵심 글자를 딴 표기이며, 지연·지터·손실·대역폭을 트래픽별로 차등 관리하는 체계
- **차등 서비스 코드점(Differentiated Services Code Point, DSCP·디에스씨피)**: 영문 각 단어의 머리글자를 딴 표기이며, IP 헤더에 등급을 표시해 홉별 동작을 선택하게 하는 값
- **자원 예약 프로토콜(Resource Reservation Protocol, RSVP·알에스브이피)**: 영문 각 단어의 머리글자를 딴 표기이며, IntServ 흐름의 종단 간 자원을 예약하는 신호 프로토콜
- **구조 약어 읽기와 표기**: IntServ·DiffServ·PHB는 인트서브·디프서브·피에이치비로 읽고 Integrated·Differentiated Service와 Per-Hop Behavior를 줄인 표기이며, 흐름 예약·등급 차등·홉별 실행 역할을 구분함
- **서비스 수준 협약(Service Level Agreement, SLA·에스엘에이)**: 영문 각 단어의 머리글자를 딴 표기이며, 측정한 품질을 계약 목표와 비교하는 기준

## Ⅰ. 개요

- 정의: 분류·표시·큐잉으로 자원을 차등 관리한다
- 배경: 혼잡 중 서비스별 품질 목표를 지킨다

### 쉽게 이해하기 (학습용)

- 한정된 회선이 붐빌 때 중요한 패킷의 순서·대역폭·폐기 기준을 미리 정해 품질 차이를 만든다


## Ⅱ. 특징

- 큐잉·폐기 차등은 중요 흐름의 지연·손실을 줄인다
- 도메인 정책 불일치는 종단 품질 보장을 끊는다

### 쉽게 이해하기 (학습용)

- 혼잡하지 않을 때는 차이가 작지만 큐가 차면 어떤 패킷을 먼저 보내고 버릴지가 품질을 가른다


## Ⅲ. 아키텍처 및 구성요소

```mermaid
flowchart LR
    F[트래픽 흐름]
    subgraph Q[QoS 영역]
        CLASS[분류·표시]
        CTRL[수용·트래픽 제어]
        PHB[PHB·큐잉]
        OBS[측정·SLA]
        CLASS -->|DSCP·흐름 식별| CTRL
        CTRL -->|허용 트래픽| PHB
        PHB -->|지연·손실 결과| OBS
        OBS -.->|정책 보정| CTRL
    end
    F --> CLASS
```

| 설계 요소 | 설명 |
|:---|:---|
| 분류·표시 | 흐름 식별과 DSCP 등급 설정 |
| 수용·트래픽 제어 | 자원 허용과 속도·버스트 제한 |
| PHB·큐잉 | 등급별 버퍼·전송·폐기 처리 |
| 측정·SLA | 지연·지터·손실·대역폭 판정 |

> 요약: 분류 등급을 실제 큐 자원 처리로 연결한다

### 쉽게 이해하기 (학습용)
- 등급 표시는 약속일 뿐 실제 처리는 PHB와 큐잉 자원이 결정함

## Ⅳ. 원리 및 절차 흐름도

```mermaid
sequenceDiagram
    participant S as 송신 흐름
    participant E as 경계 라우터
    participant C as 코어 라우터
    participant M as 품질 측정기
    S->>E: 패킷 전달
    E->>E: 분류·표시
    E->>E: 수용·트래픽 제어
    E->>C: 등급 패킷 전달
    C->>C: PHB·큐잉 처리
    C->>M: 품질 결과 보고
```

| 절차 | 설명 |
|:---|:---|
| 패킷 전달 | 송신 흐름이 경계 라우터에 진입 |
| 분류·표시 | 트래픽을 식별해 DSCP 등급 설정 |
| 수용·트래픽 제어 | 자원 한도와 속도 정책 적용 |
| 등급 패킷 전달 | 표시를 보존해 코어 영역으로 전달 |
| PHB·큐잉 처리 | 등급별 순서·대역·폐기 정책 실행 |
| 품질 결과 보고 | 지연·지터·손실을 SLA와 비교 |

> 요약: 분류와 큐 자원으로 서비스 품질을 차등화한다


### 쉽게 이해하기 (학습용)
- 중간 경로가 등급 표시를 지우면 이후 장비의 차등 처리가 끊긴다

## Ⅴ. 종류 및 비교

| 판단 기준 | IntServ | DiffServ |
|:---|:---|:---|
| 핵심 특징 | 흐름별 RSVP 예약·상태 | 등급별 DSCP·PHB 처리 |
| 적용 기준 | 소수 흐름의 명시적 자원 예약 | 대규모 IP망의 통계적 차등 |
| 주요 위험 | 라우터 상태·신호 부하 증가 | 종단 자원 보장·도메인 정합 한계 |

> 요약: IntServ는 흐름 예약, DiffServ는 등급 처리다


### 쉽게 이해하기 (학습용)
- IntServ는 예약제, DiffServ는 서비스 등급 기반 차등제임

## Ⅵ. 실무 사례

1. 기업망의 **음성 트래픽 우선 처리**

### 쉽게 이해하기 (학습용)

- 음성 패킷에 DSCP 우선 등급을 표시하고 경로상의 장비가 지연이 짧은 우선 큐로 일관되게 처리한다

## Ⅶ. 결론

- 혼잡 상황에서도 중요 트래픽의 품질을 보장하기 위해 **흐름 수·지연 및 손실 목표·상태 유지 비용·망 경계 정책**을 검토하고, 개별 흐름 예약은 IntServ, 대규모 등급 제어는 DiffServ를 선택해야 한다.

### 쉽게 이해하기 (학습용)

- 적은 흐름을 확실히 예약하면 IntServ, 많은 흐름을 등급으로 나누면 DiffServ를 선택한다
