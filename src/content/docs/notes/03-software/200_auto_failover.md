---
sidebar:
  order: 200
  label: "200. 자동 페일오버"
  badge:
    text: "기출 · 50%"
    variant: note
title: "자동 페일오버 (Auto Failover)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 200
extra:
  question_no: "200"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "상태 판정과 자동 전환은 고가용성 하위축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **자동 페일오버(Auto Failover)**: 운영자 개입 없이 감시 데몬이 주 노드 장애를 감지하고 구 노드를 펜싱(Fencing)한 후 대기 노드를 신규 Primary로 자동 승격하는 무인 복구 메커니즘.
- **Fencing 선행 원칙**: 신규 Primary 승격 전 구 Primary 노드의 쓰기 권한과 전원을 물리적으로 강제 차단(STONITH)하는 안전 규칙.

</details>

- 정의/개념: 운영자의 수동 개입 없이 **주 노드 장애 감지, Fencing 격리, Standby 승격 및 트래픽 재라우팅을 자율 수행하는 무인 복구 메커니즘**
- 배경/필요성: 야간 및 휴일 장애 시 엔지니어의 수동 개입 지연으로 인한 **RTO 지연 누적, 휴먼 에러 작업 실수 및 Split-Brain 데이터 오염 해결 불가**

#### 한줄 요약
- 다중 헬스체크, STONITH 펜싱, 쿼럼 합의 기반 승격을 통해 RTO를 초 단위로 단축하고 무결성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Hysteresis(히스테리시스)**: 헬스체크 장애 판정 임계치(3회 연속 실패)와 정상 복귀 임계치(5회 연속 성공)를 다르게 설정하여 플래핑(Flapping) 오탐을 방지.
- **Deep Health Check**: 단순 Ping(L3)이 아닌 실제 트랜잭션 쿼리(L7) 실행 성공 여부까지 검증하는 심층 헬스체크.

</details>

- 단순 Ping을 넘어 실제 DB 쿼리 실행 가능 여부를 검증하는 **심층 헬스체크(Deep Health Check)**
- 네트워크 분할 시에도 단일 노드만 승격되도록 통제하는 **과반수 쿼럼(Quorum: $N/2+1$) 합의**
- 로드밸런서 VIP 및 서비스 디스커버리를 갱신하는 **무중단 트래픽 재라우팅**

#### 한줄 요약
- 심층 헬스체크, 과반수 쿼럼 합의, 무중단 트래픽 재라우팅을 통해 안정적인 자동 복구를 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Auto Failover 4대 엔진**: Detector(상태 감지기), Decision Engine(쿼럼 결정 엔진), Fencing Agent(STONITH 차단), Failover Controller(승격/라우팅 전환).

</details>

```text
[자동 페일오버(Auto Failover) 4대 구성요소 및 제어 구조]
|-- 1. State Detector Layer (Patroni / Sentinel: 심층 헬스체크 및 복제 지연 수집)
`-- 2. Quorum Decision Engine Layer (etcd / Zookeeper 3노드 과반수 합의)
    `-- Hysteresis Filter (일시적 지연 배제 -> 3회 연속 실패 시 장애 확정)
`-- 3. Fencing Agent Layer (STONITH: 구 Primary EC2/서버 전원 및 네트워크 강제 차단)
`-- 4. Failover Controller Layer (신규 Primary 승격 + HAProxy VIP 및 DNS 라우팅 테이블 갱신)
```

선의 의미: 계층 및 감지기가 장애를 포착하면 결정 엔진이 쿼럼으로 확정하고 펜싱 에이전트가 구 노드를 격리한 후 전환 컨트롤러가 Standby를 승격하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **상태 감지기 (Detector)** | 하트비트, TCP 연결성, **복제 지연(Replication Lag)을 실시간 다중 수집** | 심층 감시 에이전트 |
| **결정 엔진 (Decision)** | 쿼럼($N/2+1$) 투표와 히스테리시스를 통해 **일시적 오류를 배제하고 장애를 최종 확정** | etcd 과반 합의 |
| **펜싱 에이전트 (Fencing)**| 승격 전 **구 Primary 노드의 전원/네트워크를 강제 차단하여 스플릿 브레인 원천 방어** | STONITH 격리 |
| **전환 컨트롤러 (Failover)**| Standby를 **Primary로 승격하고 로드밸런서 VIP 및 서비스 디스커버리 라우팅 갱신** | 트래픽 재라우팅 |

#### 한줄 요약
- 감지기, 결정 엔진, 펜싱 에이전트, 전환 컨트롤러가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **자동 페일오버 5단계**: 상태 감시 $\to$ 쿼럼 장애 확정 $\to$ Fencing 선행 격리 $\to$ Standby 쿼럼 승격 $\to$ 트래픽 라우팅 갱신.

</details>

```text
Primary 데이터베이스 노드 장애 발생
        │
   1. [상태 감시] Patroni 데몬이 매 2초마다 Primary 하트비트와 복제 지연을 etcd에 보고
        │
   2. [장애 확정] Primary가 3회 연속(10초) 응답하지 않자 3노드 중 과반수(2/3) 합의로 장애 확정
        │
   3. [Fencing 선행 격리] AWS API로 구 Primary EC2 인스턴스를 강제 중지(`ec2:StopInstances`)
   ┌────┴───────────────────────────┐
  펜싱 성공                         펜싱 실패
   │                                 │
4A. [Standby 승격]                  4B. [승격 중단 및 온콜 호출]
   WAL 로그 최신 Standby를 Primary 승격  수동 승인 대기로 전환 (안전 우선)
   │                                 │
   └────┬────────────────────────────┘
        ▼
   5. [트래픽 전환] HAProxy 로드밸런서 및 DNS 라우팅을 갱신하여 클라이언트 요청 절체 완료
```

#### 한줄 요약
- 상태 감시 → 장애 확정 → 펜싱 격리 → Standby 승격 → 트래픽 전환 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **계층별 자동 페일오버**: 클라이언트 레벨, 서비스(웹/앱) 레벨, 데이터베이스(DB) 레벨 페일오버.

</details>

| 비교 항목 | 클라이언트 페일오버 (Client Level) | 서비스 페일오버 (Service Level) | 데이터베이스 페일오버 (Data Level) |
|:---|:---|:---|:---|
| 핵심 적용 대상 | **모바일 앱, SDK 내부 엔드포인트** | **무상태(Stateless) 웹/앱, K8s 파드** | **상태형 RDBMS (PostgreSQL, MySQL)**|
| 핵심 동작 메커니즘 | **지수 백오프+지터 재시도, 다중 DNS** | **로드밸런서 헬스체크 기반 불량 파드 제외** | **STONITH 펜싱 필수 선행, 쿼럼 합의 승격**|
| 스플릿 브레인 위험 | 없음 (단순 재시도) | 없음 (무상태 인스턴스 교체) | **매우 높음 (펜싱 실패 시 데이터 파괴)** |
| 평균 RTO 소요 시간 | 1초 이내 (즉각 재시도) | 1~5초 (로드밸런서 제외 즉시) | 10~30초 (감지+펜싱+승격 소요) |

#### 한줄 요약
- 클라이언트는 재시도 분산, 웹 서비스는 로드밸런서 제외, 데이터베이스는 펜싱 기반 쿼럼 승격을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Exponential Backoff with Jitter**: 페일오버 완료 직후 수천 개 클라이언트가 신규 Primary로 동시 재접속하여 2차 다운(Thundering Herd)되는 것을 방지하는 무작위 지연 재시도 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 순간적인 네트워크 튐으로 불필요한 페일오버 남발 (Flapping) | **히스테리시스 기반 연속 3회 실패 및 쿨다운 타임(60초) 적용** | 오탐 페일오버 100% 방지 |
| Fencing 실패 상태에서 Standby를 강제 승격하여 이중 쓰기 발생 | **Fencing 실패 시 자동 승격을 즉시 중단하고 온콜 수동 개입 전환** | 데이터 오염 사고 원천 차단 |
| 페일오버 직후 수만 개 클라이언트 동시 재접속 폭주 (Thundering Herd) | **클라이언트 SDK에 `Exponential Backoff with Jitter` 강제 적용** | 신규 Primary 서버 과부하 보호 |
| 비동기 복제 지연으로 인한 승격 시 데이터 유실 | **Patroni `synchronous_mode: true` 및 Semi-Sync 복제 활성화** | 무손실 자동 승격 달성 |

#### 한줄 요약
- 히스테리시스 오탐 방지, 펜싱 안전 중단, 지수 백오프 지터, Semi-Sync 복제로 운영한다.

## Ⅶ. 결론

- 대규모 클라우드 시스템의 무중단 가용성을 실현하기 위해 **속도보다 안전(Safety First)을 최우선으로 하여 STONITH 펜싱과 쿼럼 합의가 입증된 자동 페일오버 아키텍처를 표준 구축**하고, **정기적인 카오스 엔지니어링 장애 주입 실증**을 결합하여 무결점 무인 복구 체계 완성

#### 한줄 요약
- 자동 페일오버는 심층 헬스체크, STONITH 선행 격리, 과반수 쿼럼 합의를 통해 다운타임을 수십 초 이내로 단축하고 데이터 무결성을 보장하는 핵심 고가용성 기술이다.