---
sidebar:
  order: 201
  label: "201. 멱등성 설계 (Idempotency Design)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "멱등성 설계 (Idempotency Design)"
date: "2026-08-14T05:30:00+09:00"
tags:
  - "notes-software"
weight: 201
extra:
  question_no: "201"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "중복 요청의 단일 효과 보장이 분산 설계 핵심임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Idempotency (멱등성)**: 수학에서 유래한 개념. 동일한 연산을 1회 또는 N회 반복해도 최종 결과가 동일한 성질. 분산 시스템에서 네트워크 재시도·메시지 중복 전달에도 결제 중복 등 부작용이 발생하지 않도록 보장하는 핵심 설계 원칙.
- **Idempotency Key (멱등 키)**: 클라이언트가 "이 요청은 저번에 보낸 것과 같은 요청이다"를 서버에 알리기 위해 요청 헤더에 포함하는 고유 식별자(UUID 등). Stripe, AWS 등 주요 결제/클라우드 API가 표준으로 채택.
- **At-least-once Delivery (최소 1회 전달)**: 메시지 브로커(Kafka, SQS 등)가 네트워크 장애 시 메시지를 재전송하는 보장 방식. "최소 1회"이므로 2회 이상 전달될 수 있어, 소비자 측의 멱등 처리가 필수.

- **멱등성 설계(Idempotency Design)**: 동일한 요청(동일 Idempotency-Key)을 여러 번 실행하더라도 시스템의 최종 상태가 단 한 번 실행했을 때와 정확히 동일하게 유지되도록 보장하는 분산 API 설계 원칙.
</details>

- 정의/개념: 동일 요청 반복에도 업무 효과를 한 번만 만드는 **멱등성 설계**
- 배경/필요성: 처리 완료 후 응답 유실 시 재시도로 **중복 결제•차감** 발생

#### 한줄 요약

- 같은 주문이 여러 번 도착해도 한 번만 결제하고 처음 영수증을 다시 보여 준다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Request Fingerprint (요청 지문)**: 멱등 키가 같은데 요청 본문(금액, 수신자 등)이 다른 '변조 재시도'를 검출하기 위해, 요청 본문의 해시값을 최초 저장 시 함께 기록하고 재시도 시 비교하는 기법.

</details>

- **Idempotency Key 기반 식별**: 클라이언트가 UUID 등 고유 키를 요청에 포함하고, 서버는 이 키로 최초 처리 여부를 판단.
- **Atomic Commit (원자적 확정)**: 업무 처리(DB 갱신)와 멱등 키+결과 저장을 단일 트랜잭션으로 묶어, 절반만 처리된 상태(부분 확정)가 발생하지 않도록 보장.
- **Response Replay (응답 재생)**: 동일 키의 중복 요청이 들어오면 업무를 다시 실행하지 않고 최초 저장된 응답 데이터를 그대로 반환하여 처리 비용 없이 일관성 보장.
- **TTL 관리**: 멱등 키와 저장 응답의 보존 기간을 클라이언트 재시도 창(예: 24시간)보다 충분히 길게 설정하고, 만료 후 자동 삭제로 스토리지 낭비 방지.

#### 한줄 요약

- 요청 이름표와 결과를 함께 저장해야 동시에 도착한 복사본도 한 번만 처리할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Idempotency Gate (멱등성 게이트)**: API 핸들러 앞에 위치하여 멱등 키와 요청 지문을 검사하고, 최초 요청만 업무 처리기로 통과시키고 중복 요청에는 저장된 응답을 반환하는 진입 제어 계층.

</details>

```text
[Idempotency 처리 체계]
 ├── [Gate | Key•Fingerprint•상태 분기]
 ├── [처리권 Store | 원자적 최초 실행권]
 ├── [Business Logic | 업무 상태 변경]
 └── [Result Store | 상태•응답•TTL]
```

| 구성요소 | 책임 |
|---|---|
| Gate | Key•Fingerprint로 **최초•중복•진행 중** 분기 |
| 처리권 Store | SETNX•Unique Key로 **단일 실행권** 부여 |
| Business Logic | 처리권 보유 요청의 **업무 효과** 수행 |
| Result Store | Key•상태•응답•**TTL** 원자적 저장 |

#### 한줄 요약

- 게이트가 주문 이름표를 확인해 처음 주문만 실행하고 복사본에는 저장한 결과를 돌려준다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Transactional Outbox Pattern**: 업무 DB 갱신과 메시지 발행을 원자적으로 처리하기 위해, 메시지를 별도 Outbox 테이블에 저장(같은 DB 트랜잭션)한 뒤, 별도 발행기(CDC 등)가 Outbox를 읽어 메시지 브로커에 발행하는 패턴.

</details>

```text
[Client 요청 (Idempotency-Key: UUID-1234)]
          │
          ▼
 1. [키·요청 유효성 검증] ── 키 형식, 유효 기간, 요청 지문(Fingerprint) 확인
          │
          ├─(형식/기간 오류)────► 400 Bad Request
          ├─(같은 키·다른 지문)──► 409 Conflict (변조 재시도)
          │
          └─(검증 통과)──────────────────────────────────┐
                                                         ▼
 2. [처리권 획득 (SETNX)]                                │
     ├─(완료 상태)────► 저장 응답 Replay (HTTP 200)       │
     ├─(진행 중)──────► 완료 대기 후 재조회 (HTTP 202)    │
     └─(최초 획득)────► 업무 처리 진행                    │
          │                                              │
          ▼                                              │
 3. [업무 처리] ─── 결제, DB 갱신 등 실제 상태 변경       │
          │                                              │
          ▼                                              │
 4. [원자적 결과 확정] ─── 업무 결과 + 응답을 멱등 키에 묶어 저장
          │
          ▼
 [저장된 응답 반환] (이후 같은 키 요청 → Replay)
```

### 동작 원리

1. 키•요청 유효성 검증: Key•TTL•Fingerprint 확인
2. 처리권 획득 : 최초 실행권 하나만 원자적 부여
3. 업무 처리: 결제•재고 등 업무 상태 변경
4. 원자적 결과 확정: 업무 결과와 응답을 함께 저장

#### 한줄 요약

- 같은 이름표로 먼저 온 주문만 처리하고 나머지는 처음 영수증을 받는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Naturally Idempotent Operation (자연 멱등 연산)**: 추가 구현 없이 본래부터 멱등한 연산. HTTP PUT(리소스를 특정 값으로 설정), DELETE(이미 없으면 성공 반환), 특정 값으로의 UPDATE(SET status = 'PAID') 등이 해당.

</details>

| 멱등 처리 방식 | Idempotency Key | Naturally Idempotent | Conditional Update |
|:---|:---|:---|:---|
| 적용 대상 | **POST 결제·주문 생성 등 생성/실행 요청** | PUT 상태 설정, DELETE 처리 | 동시 수정 경합이 있는 UPDATE |
| 구현 방법 | 멱등 키 저장 + 응답 Replay | 동일 값 반복 설정 (추가 구현 불필요) | WHERE version = :v 조건부 실행 |
| 주요 한계 | 키 스토리지 관리, TTL 만료 후 중복 위험 | 증가(INCREMENT) 연산에 적용 불가 | 버전 충돌 시 재시도 로직 필요 |

#### 한줄 요약

- 새 주문은 이름표를 저장하고 상태 설정은 같은 값을 반복하며 수정은 버전을 확인한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Partial Commit (부분 확정)**: 업무 처리(결제 승인)는 성공했지만 멱등 키·응답 저장이 실패한 상태. 이 경우 재시도 시 결제가 중복 실행되어 Idempotency가 깨짐. Atomic Commit 또는 Transactional Outbox로 방지.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. 부분 확정 (Partial Commit) | 업무 처리 성공, 멱등 키 저장 실패 시 이중 처리 | **업무 DB 갱신과 멱등 키·응답 저장을 단일 ACID 트랜잭션으로 묶기**|
| 2. 멱등 키 범위 혼용 | 서로 다른 사용자의 키가 충돌 | **멱등 키에 사용자 ID + 업무 유형 접두어(Prefix)를 포함하여 충돌 방지** |
| 3. TTL 만료 후 중복 요청 | 클라이언트 재시도 창(예: 7일)보다 TTL이 짧게 설정됨 | **클라이언트 최대 재시도 기간의 2배 이상 TTL 설정 및 모니터링**|

> 사례: **Stripe의 Idempotency-Key 헤더 표준화로 결제 중복 방지 구현, Kafka Consumer의 At-least-once 메시지를 멱등 처리하여 DB에 중복 Insert 방지하는 패턴**

#### 한줄 요약

- 결제 요청이 다시 와도 주문 키에 저장한 승인 결과만 반환한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **멱등 처리 방식 선택 기준**: 요청 성격(생성/설정/수정)과 분산 환경의 중복 위험 수준을 평가하여, Idempotency Key, 자연 멱등 연산, Conditional Update 중 적합한 방식을 선택하는 설계 기준.

</details>

- POST 결제는 **Idempotency Key•Atomic Commit**, 상태 설정은 PUT 적용

#### 한줄 요약

- 요청이 어디서 재시도되든 같은 업무 키와 최초 결과를 끝까지 추적해야 한다.
