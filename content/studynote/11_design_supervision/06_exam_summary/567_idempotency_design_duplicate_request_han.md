---
title: "567. 멱등성 설계 중복 요청 처리 (Idempotency Design Duplicate Request Handling)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멱등성(Idempotency)은 `f(f(x)) = f(x)`를 만족하도록 API·메시지·DB 연산을 설계하여, 네트워크 재전송·타임아웃 재시도·동시성 충돌로 인한 **중복 호출이 단일 효과(Single Effect)**로 수렴하도록 보장하는 분산 시스템의 핵심 불변식(Invariant)이다.
> 2. **가치**: 결제·재고 차감·쿠폰 발급처럼 **Side-Effect가 비즈니스 금전적 손실**로 직결되는 도메인에서 Stripe·토스·카카오페이는 멱등 키(Idempotency-Key) 도입으로 **중복 결제 사고를 99.9%v** 차단하며, IETF `Idempotency-Key` RFC 표준화(2024) 및 IETF HTTP API 디자인 권고로 글로벌 베스트 프랙티스가 확립되었다.
> 3. **판단 포인트**: **저장소 선택(Redis vs RDBMS vs Key-Value Store)**, **Key 생성 전략(Client UUID vs Server-issued)**, **TTL 정책(보통 24h~72h)**, **부분 실패 시 보상 트랜잭션(Saga)**, **Outbox 패턴과의 결합**, **동시성 모델(낙관적 락 vs 분산 락)**이 설계의 핵심 트레이드오프이며, P2PE(Payment-Processor)·이체·환불 같은 **금융 트랜잭션**에서는 멱등성 미보장은 곧 **컴플라이언스 위반**(금감원 전자금융감독규정 제17조) 사안이다.

---

## Ⅰ. 개요 및 필요성

분산 시스템에서 "요청"은 본질적으로 **불안정(uncertain)**합니다. 클라이언트가 `POST /payments`를 호출했으나 응답이 네트워크 단절로 유실되면, 클라이언트는 재시도(retry)를 수행하고 서버는 동일한 결제 요청을 **두 번** 수신합니다. 만약 서버가 멱등성을 보장하지 않으면 사용자는 **10,000원을 두 번 결제**당하는灾难가 발생합니다.

특히 2020년대 이후 MSA(Microservice Architecture), Event-Driven Architecture, Serverless(Lambda·Cloud Functions), gRPC Streaming이 보편화되면서 **At-Least-Once Delivery**가 사실상 표준이 되었고, 이는 **반드시 멱등 수신자(Idempotent Consumer)**를 요구합니다. Apache Kafka, RabbitMQ, AWS SQS, Google Pub/Sub 모두 기본적으로 At-Least-Once 또는 Exactly-Once-With-Idempotency-Producer 패턴을 권고합니다.

또한 결제 산업 표준 **PCI-DSS v4.0**(2024년 발효), **PSD2 SCA(Strong Customer Authentication)**, 그리고 한국 **금감원 전자금융감독규정**은 중복 결제 방지를 위해 멱등 키 사용을 사실상 의무화하고 있습니다.

```text
[분산 시스템에서 중복 요청이 발생하는 5가지 근본 원인]

  +--------------+                +--------------+
  |   Client A   |                |   Client B   |
  +------+-------+                +------+-------+
         | (1) HTTP POST /pay 10000원      | (4) 동시 재요청
         v                                  v
  +-------------------------------------------------+
  |             Network / Load Balancer              |
  |     (2) Timeout·TCP RST·503 응답 유실             |
  +-------------------------+-----------------------+
                            v
  +-------------------------------------------------+
  |              Payment Service (서버)              |
  |   (3) DB Commit 직전 Crash -> Retry 시 두 번 실행 |
  +-------------------------+-----------------------+
                            v
  +-------------------------------------------------+
  |  Bank / Card Gateway (외부 PSP)                  |
  |  (5) 응답 지연으로 Timeout 후 Duplicate Req 도달  |
  +-------------------------------------------------+

  ⚠ 5가지 원인 모두 "같은 비즈니스 의도"의 요청이
    "서로 다른 트랜잭션 ID"로 도달하는 것이 핵심 문제.
    -> 멱등 키(Idempotency-Key)로 의도를 식별 가능하게 만든다.
```

기존 패러다임은 **두려움 없는 설계(Fearless Design)** 였습니다. "DB UNIQUE 인덱스 + if-exists" 분기로 중복을 차단하는 식이었으나, 이는 **읽기-쓰기 원자성(Read-Write Atomicity)**이 깨지면 무용지물이며, 외부 PSP(토스페이먼츠, 아임포트, Stripe) 호출처럼 **외부 시스템에는 UNIQUE 제약을 걸 수 없는** 환경에서 좌초합니다. 새로운 패러다임은 **명시적 멱등 키 + 서버 측 상태 머신(State Machine)**이며, 2024년 IETF draft `draft-ietf-httpapi-idempotency-key-header`로 HTTP 표준화되었습니다.

- **📢 섹션 요약 비유**: 멱등성은 **택배 운송장 번호**와 같습니다. "내 택배가 안 와서 다시 시켰는데 두 번 오면?"이라고 걱정될 때, 운송장 번호 하나로 **이미 처리된 건은 자동 합치기**해주는 시스템이 멱등 키의 역할입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

멱등성 시스템의 핵심은 **4대 컴포넌트**로 구성됩니다: ① 멱등 키 생성기, ② 멱등 저장소(Idempotency Store), ③ 상태 머신(State Machine), ④ 응답 캐시(Response Cache). Stripe는 이를 `Idempotency-Key`라는 HTTP 헤더 + 서버 측 Redis Cluster 기반 저장소로 구현하며, 응답 본문까지 **24시간 보존**하여 재시도 시 동일 응답을 반환합니다.

```text
[Stripe 스타일 멱등 처리 상세 시퀀스 - 결제 $9.99 요청]

  Client                API Gateway            Idempotency Store         Payment Service      DB
    |                       |                          |                       |              |
    |  POST /charges        |                          |                       |              |
    |  Idempotency-Key:     |                          |                       |              |
    |  "8c2f-4a91-..."      |                          |                       |              |
    |  Body: {amount:999}   |                          |                       |              |
    +----------------------►|                          |                       |              |
    |                       |  SETNX key req:payload   |                       |              |
    |                       |  TTL 24h                 |                       |              |
    |                       +-------------------------►|                       |              |
    |                       |                          |                       |              |
    |                       |  ◄-- "PROCESSING" ------►|                       |              |
    |                       |                          |                       |              |
    |                       | (CASE-1: 신규)          |                       |              |
    |                       |  상태="IN_FLIGHT" 저장   |                       |              |
    |                       +-------------------------►|                       |              |
    |                       |                          |  charge.create()      |              |
    |                       +--------------------------+----------------------►|              |
    |                       |                          |                       | INSERT       |
    |                       |                          |                       +-------------►|
    |                       |                          |                       |              |
    |                       |                          |  ◄- tx_id: ch_3Oq... -+--------------+
    |                       |                          |                       |              |
    |                       |  SET key=COMPLETED       |                       |              |
    |                       |  body={charge response}  |                       |              |
    |                       +-------------------------►|                       |              |
    |                       |                          |                       |              |
    |  200 OK               |                          |                       |              |
    |  {id:ch_3Oq...,       |                          |                       |              |
    |   status:succeeded}   |                          |                       |              |
    | ◄---------------------+                          |                       |              |
    |                       |                          |                       |              |
    |  --- 30초 뒤 Client 재시도 (네트워크 끊김 후) ---  |                       |              |
    |                       |                          |                       |              |
    |  POST /charges        |                          |                       |              |
    |  Idempotency-Key:     |                          |                       |              |
    |  "8c2f-4a91-..."      |                          |                       |              |
    +----------------------►|  GET key                 |                       |              |
    |                       +-------------------------►|                       |              |
    |                       |  ◄- {COMPLETED, response}|                       |              |
    |                       |                          |                       |              |
    |  200 OK (동일 응답!)  |                          |                       |              |
    |  {id:ch_3Oq...}       |  ⚠ 비즈니스 로직 재실행 X |                       |              |
    | ◄---------------------+                          |                       |              |
    |                       |                          |                       |              |
    |  --- 동시 요청 (경합) ---                          |                       |              |
    |  POST /charges        |                          |                       |              |
    |  Idempotency-Key:     |                          |                       |              |
    |  "8c2f-4a91-..."      |                          |                       |              |
    +----------------------►|  GET key                 |                       |              |
    |                       +-------------------------►|                       |              |
    |                       |  ◄- {IN_FLIGHT}          |                       |              |
    |                       |                          |                       |              |
    |  409 Conflict         |  "요청 처리 중, 재시도 바람"|                       |              |
    |  Retry-After: 1       |                          |                       |              |
    | ◄---------------------+                          |                       |              |
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Idempotency-Key 헤더** | 클라이언트가 생성한 **UUID v4 또는 v7**(시간 정렬 가능) 36자. RFC 9562/4122 준수. SHA-256 해시로 페이로드 fingerprint 병행. | Stripe는 **헤더 누락 시 400 에러**, AWS API Gateway는 **자동 생성 정책** 지원. 토스페이먼츠는 `Idempotency-Key` 길이 16~255자 검증. |
| **Idempotency Store** | Key -> (상태, 요청 페이로드 해시, 응답 본문, 만료시각) 저장. **Redis Cluster**(권장), **DynamoDB**(AWS), **PostgreSQL JSONB** 활용. | Redis 사용 시 `SET key value NX EX 86400`(24h TTL) + `HSET`로 sub-field 저장. **Race Condition** 방지를 위해 `SETNX` 원자 명령 필수. |
| **State Machine** | `NONE -> IN_FLIGHT -> COMPLETED` 또는 `FAILED` 전이. IN_FLIGHT는 **심장박동(Heartbeat) 키**로 stale lock 회수. | IN_FLIGHT 상태가 5분 이상 지속되면 락 해제 + 클라이언트에게 409 반환. 동시 요청은 **Bottleneck 방지** 위해 큐잉 대신 즉시 거절 권고. |
| **Payload Fingerprint 비교** | 동일 키에 다른 바디가 오면 **422 Unprocessable Entity**로 거부. 보안적 관점에서 **Replay Attack 방지**. | SHA-256(requestBody) hex string. `if fingerprint != stored.fingerprint: 422`. |
| **Response Cache & Replay** | COMPLETED 상태에서 동일 키 요청 시 **저장된 응답을 byte-perfect하게** 반환. HTTP 헤더 `Idempotent-Replayed: true` 추가. | 캐시 무효화는 명시적 DELETE 엔드포인트 또는 TTL 만료로만. **불변성(Immutability)**이 핵심. |

핵심 알고리즘의 의사코드(Pseudo-code)는 다음과 같습니다:

```python
def handle_request(idempotency_key, request_body):
    fingerprint = sha256(canonical(request_body))

    # 1) 원자적 락 획득 (SETNX)
    locked = idempotency_store.setnx(
        key=f"idem:{idempotency_key}",
        value={"state": "IN_FLIGHT", "fingerprint": fingerprint, "started_at": now()},
        ttl=LOCK_TIMEOUT  # e.g., 300s
    )

    if not locked:
        existing = idempotency_store.get(f"idem:{idempotency_key}")
        if existing.state == "COMPLETED":
            if existing.fingerprint != fingerprint:
                return 422, "Idempotency-Key reused with different payload"
            return existing.response  # Replay
        elif existing.state == "IN_FLIGHT":
            return 409, "Request in flight, retry later"
        elif existing.state == "FAILED":
            # 실패는 멱등하지 않으므로 (DB 일관성 깨질 수 있음)
            # 정책 결정: 재시도 허용 vs 영구 차단
            pass

    try:
        # 2) 실제 비즈니스 로직 실행
        result = payment_service.charge(request_body)

        # 3) 응답 저장 (TTL 24h)
        idempotency_store.set(
            key=f"idem:{idempotency_key}",
            value={"state": "COMPLETED", "fingerprint": fingerprint,
                   "response": result, "completed_at": now()},
            ttl=RESPONSE_TTL  # e.g., 86400s
        )
        return 200, result
    except Exception as e:
        idempotency_store.set(
            key=f"idem:{idempotency_key}",
            value={"state": "FAILED", "error": str(e), ...},
            ttl=ERROR_TTL
        )
        raise
```

심층 고려 사항:
- **Outbox Pattern 결합**: 외부 PSP 호출은 **Transactional Outbox**로 DB 트랜잭션과 메시지 발행을 원자화. Kafka는 `enable.idempotence=true` + `transactional.id`로 Producer 레벨 멱등 보장.
- **Saga Pattern**: 분산 트랜잭션의 보상 액션(Compensation)에서도 멱등성 필수. **`refund(paymentId)`가 5번 호출돼도 1번만 환불**되어야 함.
- **CRDT & Event Sourcing**: 이벤트 로그의 멱등성은 `eventId` + `aggregateVersion`으로 처리. EventStoreDB는 낙관적 동시성 + 멱등 자동 처리.

- **📢 섹션 요약 비유**: 멱등 처리 시스템은 **은행 번호표 발급기**와 같습니다. 손님이 "잠깐, 제가 몇 번이었지?" 물으면 "100번이에요, 30분 전에 발급하셨고 아직 진행 중이에요"라고 응답해줍니다. 또 오면 "100번, 같은 자리에서 계속 진행"이지, **두 번 호출되지 않습니다**.

---

## Ⅲ. 비교 및 연결

| 구분 | **Idempotency Key (헤더 기반)** | **DB UNIQUE 제약 + SELECT FOR UPDATE** | **Distributed Lock (Redlock)** | **Optimistic Lock (version 컬럼)** |
| :--- | :--- | :--- | :--- | :--- |
| **저장소** | Redis/DynamoDB(KV) | RDBMS (PostgreSQL, MySQL) | Redis(Zookeeper, etcd) | RDBMS |
| **성능** | **O(1)·수만 TPS** 가능 | DB I/O 비용, 수천 TPS | 락 경합 시 지연 | 가벼움, 충돌 시 재시도 |
| **외부 시스템 멱등** | ✅ 가능 (헤더로 PSP 전달) | ❌ DB에만 적용 가능 | ❌ 락은 내부 한정 | ❌ |
| **응답 캐시/Replay** | ✅ 24h 동일 응답 보장 | ❌ 직접 구현 필요 | ❌ | ❌ |
| **부분 실패 복구** | IN_FLIGHT TTL + Heartbeat | Row-level Lock (DB Crash 시 위험) | Lock Lease (Redlock 권고 30s) | 자동 |
| **적합 도메인** | 결제·이체·환불 API | 단일 DB 내 도메인 | 분산 락이 필요한 자원 | Aggregate 동시성 |
| **대표 사례** | Stripe, Toss, PayPal, AWS SDK | 전통적 CRUD, 회원가입 중복 체크 | 선착순 쿠폰, 재고 차감 | JPA `@Version`, Event Sourcing |
| **단점** | KV 만료 후 재요청 시 새 트랜잭션 | 락 경합·Deadlock 위험 |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 567 / 600

<- **이전**: [566. 데이터 일관성 패턴 최종 일관성](/studynote/11_design_supervision/06_exam_summary/567_data_consistency_pattern_eventual_consis/)
**다음**: [568. 관측 가능성 메트릭 로그 트레이스](/studynote/11_design_supervision/06_exam_summary/568_observability_metrics_logs_traces/) ->

---
