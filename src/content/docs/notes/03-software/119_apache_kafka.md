---
sidebar:
  order: 119
  label: "119. Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-08-02T12:00:00+09:00"
tags:
  - "notes-software"
weight: 119
extra:
  question_no: "119"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "Kafka 로그·파티션·소비자 확장성이 높음"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **스트리밍 플랫폼**: 이벤트를 복제된 파티션 로그에 보존하고 여러 소비자가 독립적으로 읽게 하는 플랫폼이다.

</details>

- 정의/개념: **Apache Kafka**는 생산자가 발행한 이벤트를 복제된 파티션 로그에 순서대로 보존하고 소비자가 독립적으로 읽게 하는 분산 스트리밍 플랫폼
- 배경/필요성: 직접 연동은 소비자 지연·장애가 **생산자 처리 중단**으로 전파

#### 한줄 요약
- 이벤트를 분산 일지에 보존하고 여러 독자가 각자 읽는 플랫폼이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **파티션 순서**: 같은 키의 이벤트를 하나의 파티션에 기록해 로그 순서를 유지하는 특성이다.

</details>

- **파티션 순서**: 같은 키의 기록 순서 유지
- **독립 소비**: 그룹별 오프셋·배정 관리
- **보존·복제**: 재생과 리더 장애 전환 지원
- **로그 압축**: 키별 최신 레코드로 상태 재구성
- **트랜잭션 프로듀서**: 레코드·소비 오프셋 원자 커밋

#### 한줄 요약
- 병렬성과 재처리는 좋으나 순서 보장과 편중 및 재배정을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **Consumer Group·Coordinator**: 소비자 등록과 파티션 배정·재균형·오프셋 관리를 조정하는 구성요소이다.

</details>

```mermaid
block
  columns 3
  A["Kafka 경계"]:3
  P["Producer"]
  T["Topic·Partition·Offset"]
  B["Broker·Leader·Follower"]
  C["Controller"]
  G["Consumer Group·Coordinator"]
  P --- T
  T --- B
  B --- C
  B --- G
```

| 구성요소 | 책임 |
|:---|:---|
| Producer | **키·값 전송·재시도** |
| Topic·Partition·Offset | **분류·병렬 로그·위치** |
| Broker·Leader·Follower | **저장·읽기·쓰기·복제** |
| Controller | **메타데이터·리더** 변경 |
| Consumer Group·Coordinator | **배정·재균형·오프셋** 관리 |

#### 한줄 요약

- 작성자, 번호 일지, 사본 서버, 관리자, 독자 모임으로 구성된다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **2. ISR 복제 위치**: 팔로워가 리더와 같은 순서로 반영한 마지막 오프셋을 반환하는 정보이다.

</details>

```mermaid
sequenceDiagram
    participant P as Producer
    participant L as 파티션 리더
    participant F as 팔로워
    participant C as Consumer
    participant G as 그룹 코디네이터
    P->>L: 이벤트 키·값
    L->>F: 1. 오프셋·레코드
    F-->>L: 2. ISR 복제 위치
    L-->>P: acks 내구성 확인
    C->>G: 소비자 그룹 등록
    G-->>C: 담당 파티션 반환
    C->>L: 커밋 오프셋 이후 조회
    L-->>C: 이벤트 레코드
```

**동작 원리**

1. **오프셋·레코드**: 리더가 증가 번호와 이벤트를 팔로워에 전달
2. **ISR 복제 위치**: 팔로워가 같은 순서로 반영한 오프셋 반환

#### 한줄 요약

- 작성자는 번호 붙은 일지에 기록하고 독자는 마지막으로 처리한 번호를 책갈피로 저장한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **Apache Kafka**: 사건 기록을 보존하고 여러 소비자 그룹이 독립적으로 재생할 때 적합한 메시징 방식이다.

</details>

| 메시징 방식 | Apache Kafka | 전통 작업 큐 |
|:---|:---|:---|
| 적용 기준 | **사건 기록·재생** | **개별 작업 분배** |
| 핵심 특징 | **그룹별 오프셋·로그 보존** | **처리·승인 후 제거** |
| 한계 | **순서·Lag·재균형** | **재전달·대기열 적체** |

#### 한줄 요약

- 작업 큐는 일을 나눠 끝내는 데, Kafka는 사건을 남겨 여러 독자가 다시 읽는 데 초점을 둔다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **편향 키로 특정 파티션에 생산 집중**: 키 분포가 치우쳐 한 파티션과 브로커에 쓰기 부하가 몰리는 문제이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 편향 키로 특정 파티션에 생산 집중 | 순서 경계·키 분포 검증 | **핫 파티션** 방지 |
| 소비자보다 적거나 과도한 파티션 설정 | 처리량·소비자 수로 산정 | **병렬성·재균형** 균형 |
| 재시도 중 중복·순서 역전 발생 | 멱등성·acks·재시도 설정 | **중복·역전** 억제 |
| 처리 전 커밋 또는 처리 후 미커밋 | 처리·커밋 순서·멱등성 설계 | **유실·중복** 통제 |
| 처리량이 생산량보다 낮아 적체 증가 | 파티션별 지연 감시·소비자 확장 | **국소 적체** 해소 |

#### 한줄 요약

- 같은 주문의 순서는 한 일지에서 지키고 각 일지의 밀린 양을 따로 봐야 한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **Kafka**: 사건 재생과 다중 소비가 필요한 이벤트 흐름에 적합한 플랫폼이다.

</details>

- 사건 재생·다중 소비가 필요하면 **Kafka**, 일회성 작업 분배는 **작업 큐** 선택

#### 한줄 요약

- 같은 순서가 필요한 사건은 한 일지에 쓰고 다시 읽을 기간만큼 보존한다.
