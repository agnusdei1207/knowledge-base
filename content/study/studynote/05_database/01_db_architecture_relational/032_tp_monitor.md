+++
title = "TP 모니터 (Transaction Processing Monitor)"
date = "2026-03-03"
[extra]
categories = "studynote-database"
+++

> **핵심 인사이트 3줄**
> 1. TP [[229_monitor|모니터]]([[191_transaction_concept_states|Transaction]] Processing [[229_monitor|Monitor]])는 대량의 [[327_hint_handoff|OLTP]] [[191_transaction_concept_states|트랜잭션]]을 안정적으로 처리하기 위해 미들웨어 계층에서 [[191_transaction_concept_states|트랜잭션]] 조율·[[833_load_balancing_l4_l7_switch_traffic_distribution|로드 밸런싱]]·자원 관리를 담당한다.
> 2. [[549_2pc_two_phase_commit_limitations_msa|2PC]]([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])와 XA [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]의 ACID를 보장하며, 금융·항공·통신 등 미션 크리티컬 시스템의 기반 인프라다.
> 3. 현대 클라우드 환경에서는 [[305_saga|사가 패턴]]([[305_saga_pattern|Saga Pattern]])·[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]이 TP [[229_monitor|모니터]]의 역할을 대체하지만, 레거시 금융 시스템에서는 CICS·Tuxedo가 여전히 수십억 건/일을 처리한다.

---

## Ⅰ. TP [[229_monitor|모니터]]의 정의와 역할

TP [[229_monitor|모니터]]([[191_transaction_concept_states|Transaction]] Processing [[229_monitor|Monitor]])는 **클라이언트-서버 환경에서 다수의 동시 [[191_transaction_concept_states|트랜잭션]]을 관리·조율하는 미들웨어**다.

```
클라이언트 ──→ TP 모니터 ──→ 애플리케이션 서버 ──→ DBMS
              (트랜잭션 조율)
```

| 기능             | 설명                               |
|----------------|-----------------------------------|
| [[191_transaction_concept_states|트랜잭션]] 관리   | 2PC로 [[136_variance|분산]] ACID 보장               |
| [[833_load_balancing_l4_l7_switch_traffic_distribution|로드 밸런싱]]     | 요청을 여러 서버에 [[136_variance|분산]]             |
| 커넥션 [[285_pooling_layer|풀링]]     | DB 연결 재사용 (N:M [[071_다중화_Multiplexing|다중화]])         |
| 장애 [[658_ir_recovery|복구]]       | 체크포인트·[[568_logs_distributed_logging_elk_fluentd|로그]] 기반 재시작         |
| 보안            | [[303_authentication_authorization_patterns|인증]]·권한 부여·[[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]            |

📢 **섹션 요약 비유**: TP [[229_monitor|모니터]]는 은행 창구 매니저다 — 수백 명의 고객([[191_transaction_concept_states|트랜잭션]])을 줄 세우고, 직원(서버)에게 업무를 배정하며, 실수 없이 처리되도록 감독한다.

---

## Ⅱ. [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) — [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]

### [[549_2pc_two_phase_commit_limitations_msa|2PC]] 동작 과정

```
Phase 1 - Prepare:
  코디네이터 → 참여자들: "커밋 준비됐어?" (PREPARE)
  참여자 → 코디네이터: "예" (VOTE-COMMIT) / "아니오" (VOTE-ABORT)

Phase 2 - Commit:
  모두 "예" → 코디네이터: "커밋해!" (COMMIT)
  하나라도 "아니오" → 코디네이터: "롤백해!" (ABORT)
```

### [[549_2pc_two_phase_commit_limitations_msa|2PC]] 문제점

| 문제          | 설명                          |
|--------------|-------------------------------|
| 블로킹        | 코디네이터 장애 시 참여자 대기  |
| [[282_performance_tactics|성능]] 저하     | 추가 라운드트립 2회            |
| [[454_spof|단일 장애점]]   | 코디네이터 [[454_spof|SPOF]]               |

→ **3PC (Three-Phase Commit)**: Pre-commit 단계 추가로 블로킹 해소 (단, 복잡도 증가)

📢 **섹션 요약 비유**: 2PC는 결혼식 주례와 같다 — "혼인 동의하십니까?" 두 분 모두 "예"라고 해야 혼인이 성립된다. 한 분이 주저하면 식이 중단된다.

---

## Ⅲ. XA [[295_protocol_field_tcp_udp_icmp|프로토콜]]과 JTA

### XA (X/Open [[248_dtp_and_vtp_cisco_dynamic_trunking|DTP]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]]

XA는 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]에서 **[[191_transaction_concept_states|트랜잭션]] 매니저(TM)와 리소스 매니저([[197_rm_rate_monotonic_scheduling|RM]]) 사이의 표준 인터페이스**다.

```
애플리케이션 ─→ 트랜잭션 매니저 (TM)
                    │ XA
               ┌────┴────┐
              RM1        RM2
             (DB1)      (MQ1)
```

**JTA (Java [[191_transaction_concept_states|Transaction]] [[014_api_posix|API]])**: Java EE에서 XA를 [[198_abstraction_control_data_process|추상화]]한 [[014_api_posix|API]] → Atomikos·Bitronix가 구현

### 대표 TP [[229_monitor|모니터]] 제품

| 제품     | 벤더  | 특징                     |
|---------|-------|--------------------------|
| CICS    | IBM   | 메인프레임, 50년 이상 운영 |
| Tuxedo  | BEA/[[188_pl_sql_t_sql_procedural|Oracle]] | UNIX 기반 고성능    |
| IMS TM  | IBM   | 계층형 [[502_dbms|DBMS]] 연계          |
| WebSphere MQ | IBM | [[389_mesh_topology|메시]]지 큐 기반 [[191_transaction_concept_states|트랜잭션]] |

📢 **섹션 요약 비유**: XA [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 국제 송금 표준이다 — 어떤 은행([[197_rm_rate_monotonic_scheduling|RM]])이든 같은 규칙(XA)으로 통장 잔액을 동시에 업데이트하거나 모두 취소한다.

---

## Ⅳ. [[282_performance_tactics|성능]] 특성과 병목 분석

### TPS (Transactions Per Second) 지표

```
TPS = 동시 사용자 수 × (1 / 응답 시간)
처리량 = TPS × 트랜잭션 크기
```

| 시스템       | 목표 TPS       | 비고                 |
|-------------|---------------|----------------------|
| 소형 쇼핑몰  | 100~1,000     | 단일 DB 가능          |
| 대형 은행    | [[489_raid_10_hybrid|10]],000~100,000 | TP [[229_monitor|모니터]] + 클러스터 |
| VISA 전산   | 65,000 peak   | 글로벌 [[136_variance|분산]] 처리      |

### 병목 포인트

```
클라이언트 → 네트워크 → TP 모니터 → DB 커넥션 풀 → DBMS → I/O
           ↑            ↑            ↑                ↑
         지연          스레드 풀    커넥션 부족        락 경합
```

📢 **섹션 요약 비유**: TPS는 공장 생산량이다 — 라인([[092_thread_lwp|스레드]]) 수를 늘리거나 각 공정([[298_qkv_attention|쿼리]])을 빠르게 해야 하지만, 부품 창고(DB 커넥션)가 부족하면 라인이 아무리 많아도 멈춘다.

---

## Ⅴ. 현대화 — [[305_saga|사가 패턴]]과 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]

### [[532_microservices_decomposition_patterns|마이크로서비스]]에서의 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]

TP [[229_monitor|모니터]]·2PC는 **강한 [[194_consistency_database_integrity|일관성]]**을 제공하지만, [[532_microservices_decomposition_patterns|마이크로서비스]] 환경에서는 [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[195_coupling_levels|결합도]]를 높인다.

**[[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]])**

```
주문 생성 → 결제 → 재고 차감 → 배송
  실패 시: 배송 취소 → 재고 원복 → 결제 환불 (보상 트랜잭션)
```

| 방식         | 특징                    |
|------------|------------------------|
| 코레오그래피 | 이벤트 기반, [[136_variance|분산]] 결정  |
| [[073_container_orchestration_tools|오케스트레이션]] | 중앙 [[312_saga_pattern_choreography_orchestration|사가]] 매니저 제어   |

📢 **섹션 요약 비유**: [[305_saga|사가 패턴]]은 릴레이 경주 실수 규칙이다 — 한 선수가 넘어지면 이전 선수들이 역방향으로 달려 처음 상태로 되돌린다.

---

## 📌 관련 개념 맵

```
TP 모니터 (Transaction Processing Monitor)
├── 핵심 기능
│   ├── 분산 트랜잭션 관리 (2PC, 3PC)
│   ├── 커넥션 풀링 (Connection Pooling)
│   └── 로드 밸런싱 (Load Balancing)
├── 표준 프로토콜
│   ├── XA (X/Open DTP)
│   └── JTA (Java Transaction API)
├── 제품
│   ├── CICS (IBM)
│   ├── Tuxedo (Oracle)
│   └── IMS TM (IBM)
└── 현대적 대안
    ├── 사가 패턴 (Saga Pattern)
    ├── 이벤트 소싱 (Event Sourcing)
    └── CQRS
```

---

## 📈 관련 키워드 및 발전 흐름도

```
┌─────────────────────────────────────────────────────────────────┐
│                  TP 모니터 발전 흐름                             │
├──────────────┬────────────────────┬─────────────────────────────┤
│ 1970년대     │ IMS·CICS 등장      │ 메인프레임 OLTP 기반         │
│ 1980년대     │ X/Open DTP·XA 표준 │ 이기종 분산 트랜잭션 표준화  │
│ 1990년대     │ Tuxedo·BEA 성장    │ UNIX 기반 고성능 TP 모니터   │
│ 2000년대     │ J2EE·JTA 표준화    │ Java EE 트랜잭션 추상화      │
│ 2010년대     │ MSA 전환 시작      │ 사가 패턴, BASE 일관성       │
│ 2020년대     │ 이벤트 드리븐      │ Kafka + 사가 오케스트레이션  │
└──────────────┴────────────────────┴─────────────────────────────┘

핵심 키워드 연결:
OLTP → TP 모니터 → 2PC → XA → JTA
  ↓        ↓         ↓
TPS     커넥션 풀  분산 ACID
  ↓
사가 패턴 → 이벤트 소싱 → CQRS
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. TP [[229_monitor|모니터]]는 놀이공원 줄 관리 직원이다 — 많은 사람을 여러 놀이기구(서버)에 공평하게 배정하고 사고가 나면 바로 처리한다.
2. 2PC는 두 친구가 동시에 선물을 교환하는 규칙이다 — 둘 다 "줄게"라고 해야 교환하고, 한 명이 거부하면 아무것도 바꾸지 않는다.
3. [[305_saga|사가 패턴]]은 릴레이 달리기 취소 규칙이다 — 중간에 실수하면 이전 주자들이 역방향으로 달려 처음 상태로 되돌린다.
