---
sidebar:
  order: 200
  label: "200. 자동 페일오버 (Auto Failover)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "자동 페일오버 (Auto Failover)"
date: "2026-08-14T05:25:00+09:00"
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

<details><summary>핵심 용어</summary>

- **Auto Failover (자동 장애 전환)**: 관리자가 수동으로 개입하지 않아도 시스템이 스스로 장애를 감지하고, 이전 활성 자원을 격리(Fencing)한 뒤 대체 자원을 Primary로 승격하여 요청 경로를 자동 전환하는 고가용성 핵심 메커니즘.
- **Recovery Time Objective (RTO, 복구 시간 목표)**: 장애 발생 후 서비스가 정상화되어야 하는 최대 허용 시간. Auto Failover는 이 RTO를 분/시간 단위에서 초 단위로 줄이는 것을 목표로 함.
- **Split Brain (분할 뇌 현상)**: 장애 판정 후 Fencing 없이 Standby를 승격할 경우, 구 Primary가 아직 살아서 동시에 쓰기를 수행하여 데이터가 양쪽에서 다르게 변경되는 치명적 데이터 정합성 문제.

</details>

- 정의/개념: 감지•Fencing•승격•Routing을 자동 수행하는 **Failover**
- 배경/필요성: 수동 전환의 **RTO 초과•이중 쓰기•절차 누락** 위험 발생

#### 한줄 요약

- 사람이 개입하지 않고 안전하게 예비 자원으로 전환하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Heartbeat (하트비트)**: 클러스터 노드들이 "나는 살아있다"는 신호를 주기적으로 주고받는 생존 신호. 일정 횟수 이상 하트비트를 받지 못하면 해당 노드를 장애로 의심하는 1차 판단 근거.

</details>

- **정확한 장애 판정**: Heartbeat 단절 외에도 복제 지연, 실제 요청 처리 가능 여부(Deep Health Check) 등 다중 신호와 지속 시간(히스테리시스)을 조합하여 일시적 오류와 실제 장애를 구분.
- **Fencing 선행 원칙**: Standby를 Primary로 승격하기 **전에** 반드시 구 Primary의 전원·스토리지·쓰기 자격을 차단(STONITH 등)하여 Split Brain을 원천 봉쇄.
- **Quorum 기반 단일 승격**: 클러스터 과반수 노드의 합의(Quorum)를 얻은 단 하나의 Standby만 Primary로 승격하여, 동시에 여러 노드가 Primary가 되는 사태 방지.
- **State Synchronization (상태 동기화)**: 승격된 Standby가 구 Primary의 최신 상태(미처리 트랜잭션, 세션 등)를 RPO 범위 내에서 이어받아 처리를 연속.

#### 한줄 요약

- 고장 노드 권한을 차단하고 복구 전환하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Decision Engine (결정기)**: 여러 감지기에서 수집된 신호(헬스 체크 실패 횟수, 복제 지연, 쿼럼 충족 여부)를 종합하여 "진짜 장애인가?" 최종 판정을 내리는 두뇌 역할 구성요소.

</details>

```text
[Auto Failover]
 ├── [Detector | Heartbeat•Health•Lag]
 ├── [Decision Engine | Quorum•Hysteresis]
 ├── [Fencing Agent | 구 Primary 격리]
 ├── [Failover Controller | 승격•Routing]
 └── [Failback Controller | 재동기화•복귀]
```

| 구성요소 | 책임 |
|---|---|
| Detector | Heartbeat•Health•**복제 지연** 수집 |
| Decision Engine | Quorum•Hysteresis로 **장애 확정** |
| Fencing Agent | 구 Primary의 **쓰기 권한** 차단 |
| Failover Controller | Standby 승격과 **Routing 갱신** |
| Failback Controller | 상태 재동기화 후 **안전 복귀** |

#### 한줄 요약

- 감지 결과를 합의한 뒤 이전 쓰기를 끊고 예비 자원과 요청 경로를 바꿈이 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Hysteresis (히스테리시스)**: 장애 진입 조건(예: 헬스 체크 5회 연속 실패)과 장애 해제 조건(예: 3회 연속 성공)을 다른 임계값으로 설정하여, 상태가 임계값 근처에서 켰다 껐다 반복(Flapping)하는 것을 방지하는 제어 기법.

</details>

```text
 1. [지속적 상태 감시] ── Heartbeat, Deep Health Check, 복제 지연 다중 수집
          │
          ▼
 2. [장애 판정] ────────── Quorum 충족 + 히스테리시스 지속 시간 초과 시 확정
          │
          ├─(오탐·일시 오류)──► 기존 상태 유지, 감시 계속
          │
          └─(장애 확정)──────► Failover 프로세스 시작
                                      │
                                      ▼
 3. [Fencing 실행] ─────── 구 Primary 전원·스토리지·쓰기 자격 강제 차단
          │
          ├─(Fencing 실패)────► 자동 승격 중단, 수동 승인 요구 (안전 우선)
          │
          └─(Fencing 완료)────► Standby 승격 진행
                                      │
                                      ▼
 4. [Standby 상태·용량 검증] ── RPO 범위 내 복제 상태 + N-1 부하 처리 가능 확인
          │
          ▼
 5. [트래픽 전환] ─────────── DNS TTL, LB 라우팅, 서비스 디스커버리 일괄 갱신
```

### 동작 원리

1. **지속적 상태 감시**: Heartbeat•Health•Lag 다중 수집
2. **장애 판정**: Quorum•Hysteresis로 지속 장애 확정
3. **Fencing 실행**: 구 Primary 전원•Storage•쓰기 차단
4. **Standby 상태•용량 검증**: RPO와 N-1 용량 확인
5. **트래픽 전환**: DNS•LB•Service Discovery 갱신

#### 한줄 요약

- 여러 신호로 장애를 확정하고 이전 쓰기를 끊은 뒤 예비 자원으로 전환하는 것이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Graceful Failover vs Forced Failover**: Graceful Failover는 Active 노드가 정상적으로 상태를 Standby에 넘기고 역할을 전환하는 계획된 전환(예: 유지보수). Forced Failover는 Active가 응답 불가 시 Fencing 후 강제 전환하는 비계획 전환.

</details>

| 자동 전환 계층 | Client Failover | Service Failover | Data Failover |
|:---|:---|:---|:---|
| **전환 대상** | **호출자의 연결 대상 주소·경로** | **무상태 서비스 인스턴스** | **상태형 DB Primary 쓰기 노드** |
| **핵심 통제** | 재시도 상한, DNS TTL 최소화 | 헬스 체크 기반 LB 제외 | Fencing + Quorum 기반 단일 승격 |
| **Fencing 필요** | 불필요 | 불필요 (무상태) | **필수 (Split Brain 방지)** |

#### 한줄 요약

- 호출 주소, 서비스 인스턴스, 데이터 쓰기 주체를 각각 다른 계층에서 바꿈이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Backoff with Jitter (지수 백오프 + 지터)**: Failover 직후 대량의 클라이언트 재시도가 신규 Primary에 동시 폭주(Thundering Herd)하는 것을 막기 위해, 재시도 간격을 지수적으로 늘리면서 무작위 시간 편차(Jitter)를 추가하여 요청을 시간적으로 분산하는 기법.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 오탐 전환 (Flapping)** | 순간 네트워크 지연으로 헬스 체크 실패 → 불필요한 Failover | **히스테리시스 기반 연속 실패 횟수+지속 시간 조합으로 장애 판정 기준 엄격화**|
| **2. Split Brain (이중 쓰기)** | Fencing 없이 Standby 승격 또는 Fencing 실패 무시 | **Fencing 실패 시 자동 승격 전면 중단, 반드시 수동 승인 요구 정책 강제화** |
| **3. 전환 후 재시도 폭주** | Failover 완료 직후 모든 클라이언트가 동시 재접속 | **지수 백오프+지터(Jitter)로 재시도 분산 + N-1 용량 사전 검증으로 여유 확보** |

> 사례: **PostgreSQL Patroni + etcd 기반 자동 Leader 선출 및 Fencing(AWS API로 구 Primary 강제 정지) 구현으로 RTO 30초 이내 Auto Failover 달성, MySQL InnoDB Cluster의 자동 장애 전환 운영 사례**

#### 한줄 요약

- 데이터베이스는 이전 주 노드를 차단한 뒤 새 쓰기를 허용하는 것이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Chaos Test (카오스 시험)**: 정기적으로 실제 장애를 주입하여 Auto Failover 파이프라인(감지→펜싱→승격→전환)이 실제로 RTO 이내에 완료되는지 검증하고 증적을 보존하는 신뢰성 검증 활동.

</details>

- **자동 전환 승인 기준**에 따라 Quorum·Fencing 확보와 RPO·N-1 용량 충족 시 자동 전환하고, 불확실 상황에서는 수동 승인 후 전환하는 **안전 우선 Auto Failover 정책** 적용

#### 한줄 요약

- 빠른 전환보다 이중 쓰기 없는 전환이 먼저이다.
