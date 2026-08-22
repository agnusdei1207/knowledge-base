---
sidebar:
  order: 17
  label: "017. 고가용성 설계 - Active-Active•Active-Standby (High Availability Architecture)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "무중단 시스템 이중화 및 장애 복구 : 고가용성 아키텍처 (Active-Active vs Active-Standby & 펜싱)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-evaluation"
weight: 17
extra:
  question_no: "017"
  source_status: "기출"
  source_history: "135회, 137회"
  priority: 70
  priority_note: "135회·137회 반복 출제, 고가용성(HA: High Availability) 아키텍처 설계, Active-Active(무상태 계층, 100% 자원 활용, 부하 분산) vs Active-Standby(상태 저장 계층, Hot/Warm/Cold Standby, 단일 쓰기 보장), 하트비트(Heartbeat), 정족수 쿼럼(Quorum (N/2)+1), STONITH 펜싱(Fencing), 가상 IP(VIP) 페일오버 및 N-1 용량 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **고가용성 아키텍처(High Availability Architecture / Active-Active & Active-Standby)**: 단일 장애점(SPOF)으로 인한 시스템 중단을 방지하고 99.99% 이상의 서비스 가용성을 보장하기 위해, 모든 인프라 계층(네트워크, 서버, 데이터베이스, 스토리지)을 이중화하고 장애 발생 시 자동 페일오버(Auto-Failover) 및 트래픽 재라우팅을 1초 내에 집행하는 고신뢰성 아키텍처 설계 기법.
- **단일 장애점 중단 및 스플릿 브레인 데이터 오염 결함(SPOF Outage & Split-Brain Defect)**: 서버 1대 다운 시 전체 서비스가 마비되는 단일 장애점(SPOF) 결함이나, 이중화 환경에서 노드 간 하트비트 통신망 단절로 인해 양쪽 서버가 동시에 자신을 마스터로 선언하여 데이터베이스에 동시 쓰기를 수행함으로써 데이터가 영구적으로 파괴되는 구조적 결함.

</details>

- 정의/개념: 무중단 비즈니스 연속성을 달성하기 위해 **계층별 특성(Stateless vs Stateful) 분류 $\rightarrow$ 무상태 계층 Active-Active 부하 분산 $\rightarrow$ 상태 저장 계층 Active-Standby 동기 복제 $\rightarrow$ 하트비트 및 홀수 쿼럼($(N/2)+1$) 감시 $\rightarrow$ STONITH 노드 펜싱(Fencing) 기반 스플릿 브레인 방어 $\rightarrow$ 가상 IP(VIP) 자동 페일오버** 를 집행하는 **엔드투엔드 고가용성 엔지니어링 체계**
- 배경/필요성: 금융 거래, 의료 시스템, 대규모 이커머스 환경에서 단 수 분의 서비스 중단도 수억 원의 금전적 피해와 기업 신뢰도 추락을 초래하므로, 인프라 고장 발생 시에도 사용자 체감 다운타임을 0으로 수렴시키는 자동 복원 체계 필수

#### 한줄 요약
- 고가용성 설계는 Active-Active 및 Active-Standby 이중화와 펜싱 메커니즘을 통해 무중단 서비스 연속성을 보증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **고가용성 2대 핵심 이중화 모델**:
  - **Active-Active (활성-활성)**: 모든 복제 노드가 동시 활성화되어 클라이언트 트래픽을 병렬 분산 처리하는 구조 (자원 활용률 100%).
  - **Active-Standby (활성-대기)**: 주 노드(Active)만 트래픽을 처리하고 대기 노드(Standby)는 실시간 데이터 복제만 유지하다가 장애 시 승격하는 구조 (단일 쓰기 보장).

</details>

- **소프트웨어 계층별 분리 적용 원칙**: 웹/WAS와 같은 무상태(Stateless) 계층은 Active-Active로 수평 확장하고, RDBMS와 같은 상태 저장(Stateful) 계층은 데이터 일관성을 위해 Active-Standby로 단일 쓰기 통제
- **스플릿 브레인(Split-Brain)의 완벽한 억제**: 홀수 노드 쿼럼(Quorum) 합의와 하드웨어 전원 강제 차단(STONITH: Shoot The Other Node In The Head) 펜싱으로 다중 마스터 출현 원천 방어
- **N-1 예비 용량(Headroom) 확보**: 액티브 노드 중 1대가 이탈하더라도 잔여 노드만으로 피크 부하를 70% 가동률 내에서 100% 정상 수용하도록 클러스터 용량 사이징

#### 한줄 요약
- 계층별 이중화 분리(무상태 A-A / 상태 A-S), 쿼럼 및 STONITH 펜싱, N-1 용량 확보를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **고가용성 4대 아키텍처 계층**:
  1. **Traffic & Routing Layer**: GSLB, Anycast BGP, L4/L7 로드밸런서 (VIP 바인딩).
  2. **Stateless Compute Layer**: Active-Active WAS/컨테이너 클러스터 (공유 세션 Redis).
  3. **Stateful Data Layer**: Active-Standby DBMS (Primary-Replica 반동기/동기 복제).
  4. **Cluster Management & Fencing Layer**: Pacemaker, Corosync, IPMI STONITH 펜싱.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 트래픽 분산 및 진입 계층 (Traffic Routing Layer: Active-Active) ]  │
│  ├─ [ Anycast GSLB / L4 Load Balancer (VRRP 이중화) ]                   │
│  └─ [ 가상 IP(VIP: 10.0.0.100) 기반 트래픽 로드밸런싱 ]                 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (병렬 트래픽 라운드로빈 분산)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 무상태 애플리케이션 계층 (Stateless Web/WAS: Active-Active) ]      │
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ WAS Node 1 (Active) ]           │ [ WAS Node 2 (Active) ]             │
│ ├─ 트래픽 50% 병렬 처리           │ ├─ 트래픽 50% 병렬 처리             │
│ └─ 세션 상태: [ Redis Cluster ] ◄─┴─► 세션 상태: [ Redis Cluster ]      │
└───────────────────────────────────┴─────────────────────────────────────┘
                                     │ (단일 쓰기 및 읽기 분기)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 상태 저장 데이터 계층 (Stateful DB Layer: Active-Standby & Fencing)]│
│                                                                         │
│  [ Primary DB (Active: 쓰기/읽기) ] ──(동기 복제)──► [ Replica DB (Standby: 읽기)]
│               ▲                                            ▲            │
│               │ (전용 하트비트 네트워크)                    │            │
│               ▼                                            ▼            │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ [ 클러스터 오케스트레이터: Pacemaker & Corosync (3-Node Quorum) ]  │  │
│  │ ├─ 하트비트 3회 유실 감지 ➔ 과반수 합의 ➔ Primary STONITH 전원 차단 │  │
│  │ └─ Replica를 New Primary로 마스터 승격 ➔ VIP 바인딩 즉시 전환     │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 로드밸런서가 무상태 WAS로 트래픽을 분산하고, 상태 저장 DB는 액티브-스탠바이 동기 복제와 쿼럼 펜싱으로 무중단 가용성을 보장하는 구조

| 계층 컴포넌트 | 적용 이중화 방식 | 핵심 기술 및 메커니즘 | 실무 역할 |
|:---|:---|:---|:---|
| **로드밸런서 계층** | **Active-Active (Anycast) / Active-Standby (VRRP)** | Keepalived, F5 BIG-IP, VIP 플로팅 | 단일 진입점 SPOF 제거 |
| **애플리케이션 계층**| **Active-Active (완전 병렬 분산)** | Stateless WAS, K8s HPA, Redis Session | 100% 자원 가동 및 N-1 수용 |
| **데이터베이스 계층**| **Active-Standby (단일 마스터 복제)** | MySQL Group Replication, Oracle RAC | 데이터 일관성 및 무손실 승격 |
| **클러스터 매니저** | **홀수 쿼럼 (Quorum 3-Node)** | Corosync, Pacemaker, etcd Quorum | 하트비트 감시 및 페일오버 오케스트레이션 |
| **하드웨어 펜싱** | **STONITH (Shoot The Other Node)** | IPMI, iLO, vSphere API 전원 강제 차단 | 스플릿 브레인 원천 차단 |

#### 한줄 요약
- Anycast 로드밸런서, 무상태 Active-Active WAS, Active-Standby DB, Pacemaker 쿼럼, STONITH 펜싱으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Active-Standby 자동 페일오버 5단계 수명주기 프로세스**:
  1. 평시 Primary DB(Active)와 Replica DB(Standby) 간 동기 복제 및 1초 주기 하트비트 교환
  2. Primary DB의 하드웨어 커널 패닉으로 하트비트 신호 유실 발생
  3. Corosync 쿼럼 클러스터가 3회 연속 타임아웃 감지 후 비정상 노드 확정
  4. 구 Primary 노드에 대해 IPMI STONITH 신호를 보내 전원을 강제 차단(펜싱)
  5. Replica 노드를 New Primary로 마스터 승격하고 VIP를 재할당하여 서비스 정상화

</details>

```text
1. [정상 가동 및 동기 복제 상태]
    ├─ Primary DB(Active, VIP 10.0.0.200 바인딩)가 모든 Read/Write 트랜잭션 전담
    ├─ Replica DB(Standby)로 트랜잭션 로그 실시간 동기 복제 (Sync Replication)
    └─ [전용 사설망을 통해 500ms 주기로 Corosync 하트비트 패킷 정상 교환]
            │
            ▼
2. [장애 발생 및 하트비트 유실 감지]
    ├─ 00:00:00 Primary DB 전원 공급장치 고장으로 셧다운
    ├─ 00:00:01.5 500ms 하트비트 3회 연속 실패 감지 (타임아웃)
    └─ [Corosync 쿼럼(3개 노드 중 2개 정상) 합의 ➔ Primary 장애 상태 최종 선언]
            │
            ▼
3. [STONITH 하드웨어 펜싱 집행]
    ├─ Pacemaker가 네트워크 분리(Split-Brain) 가능성을 배제하기 위해 펜싱 가동
    ├─ Primary 서버의 IPMI/BMC 원격 관리 포트로 전원 차단(Power Off) 명령 전송
    └─ [구 Primary의 스토리지 I/O 및 잔여 쓰기 시도를 물리적으로 100% 차단]
            │
            ▼
4. [마스터 승격 및 VIP 플로팅 인계]
    ├─ Replica DB의 WAL(Write-Ahead Log) 재실행 완료 및 최종 트랜잭션 정합성 검증
    ├─ Replica DB를 'New Primary (Read-Write Mode)'로 마스터 승격
    └─ [ARP 브로드캐스팅(Gratuitous ARP)을 통해 VIP(10.0.0.200)를 신규 마스터로 즉시 이전]
            │
            ▼
5. [서비스 정상화 및 RTO 달성]
    ├─ 애플리케이션 커넥션 풀이 신규 마스터로 자동 재연결 ➔ 트랜잭션 정상 재개
    ├─ 총 장애 복구 소요 시간: $\text{RTO} = 4.5\text{초}$, 데이터 손실량: $\text{RPO} = 0\text{초}$
    └─ [구 서버 수리 후 신규 Replica(Standby)로 클러스터에 안전 재편입(Failback)]
```

**동작 원리**

1. **무상태 계층의 자원 효율 극대화**: Active-Active 구성은 유휴 자원 없이 모든 서버가 부하를 나누어 처리하므로 인프라 가성비(Cost Efficiency)가 최고 수준
2. **단일 쓰기 원칙(Single-Writer Principle)**: 분산 DB가 아닌 전통적 RDBMS에서는 2개 노드가 동시 쓰기를 수행하면 데이터 충돌이 발생하므로 Active-Standby 모델로 쓰기 권한을 엄격히 단일화
3. **홀수 정족수(Odd Quorum)의 수학적 원리**: $2N+1$개 노드 중 과반수인 $N+1$개 노드의 동의를 얻은 진영만 살아남게 하여 네트워크가 반으로 잘려도(50:50) 양쪽 모두 쓰기를 멈추는 안전 메커니즘
4. **펜싱(STONITH)의 절대성**: 하트비트가 끊겼을 때 "상대 노드가 죽었는지, 네트워크만 끊겼는지" 알 수 없으므로, 무조건 상대를 강제 종료시킨 후 승격하여 데이터 오염 방지
5. **무손실 동기 복제(Semi-sync / Sync)**: Active에서 Standby로 커밋 로그가 최소 1대 이상 복제되었음을 확인한 후 클라이언트에 응답하여 RPO=0 보장

#### 한줄 요약
- 정상 동기 복제, 하트비트 유실 감지, STONITH 펜싱 차단, Standby 마스터 승격, VIP 인계 및 RTO 0초 수렴 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Active-Standby 3대 대기 방식(Hot vs Warm vs Cold) 비교**:
  - Hot Standby: 대기 서버가 상시 기동되어 데이터 동기화 완료 상태 (RTO 초 단위).
  - Warm Standby: 대기 서버 OS/미들웨어는 기동 중이나 앱/DB는 준비 상태 (RTO 수 분 단위).
  - Cold Standby: 대기 서버가 전원 OFF 상태로 장애 시 전원 투입 및 복원 (RTO 수 시간 단위).

</details>

| 비교 항목 | Active-Active (활성-활성) | Active-Standby: Hot Standby | Active-Standby: Cold Standby |
|:---|:---|:---|:---|
| **트래픽 처리** | **모든 노드가 실시간 병렬 처리**| **Active만 처리 (Standby는 복제만)**| Active만 처리 (Standby 전원 OFF)|
| **자원 활용률** | **100% (모든 자원 상시 가동)** | **50% (대기 서버 유휴 비용 발생)** | 50% (전원 차단으로 전기세 절감)|
| **복구 시간 (RTO)**| **0초 (즉시 나머지 노드가 수용)** | **초 단위 (1초 ~ 30초 내 승격)** | **수 시간 (장비 부팅 및 백업 복원)**|
| **데이터 손실 (RPO)**| **0초** | **0초 (동기 복제 시)** | 백업 주기만큼 손실 (수 시간) |
| **적합한 계층** | **웹 서버, API Gateway, NoSQL** | **RDBMS (Oracle, MySQL, PostgreSQL)**| 비핵심 배치 서버, 개발/검증 환경 |
| **구축 복잡도** | 세션 공유 및 동기화 설계 복잡 | **클러스터 쿼럼 및 펜싱 구성 필요**| 단순 수동 복구 절차 |

#### 한줄 요약
- Active-Active는 무상태 병렬 처리(RTO 0초), Hot Standby는 상태 저장 단일 쓰기(RTO 초 단위), Cold Standby는 저비용 예비용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **고가용성 아키텍처 실무 구축 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Active 노드 1대 장애 시 남은 1대 노드의 CPU가 100% 포화되어 **클러스터 전체가 도미노처럼 연쇄 붕괴(Cascading Failure)하는 결함 발생** | **평시 가동률을 50% 이하로 통제하고 1대 장애 시에도 피크 부하를 수용할 수 있는 N-1 용량 사이징(Headroom) 강제** | 단일 노드 셧다운 시 무중단 연속성 100% 보장 |
| 노드 간 하트비트 전용 랜선 장애로 상호 통신이 단절되어 **두 서버가 모두 마스터로 동작하며 스플릿 브레인(Split-Brain) 데이터 영구 파괴 발생** | **3개 이상의 홀수 쿼럼(Quorum) 클러스터를 구성하고 IPMI 기반 STONITH 하드웨어 펜싱 필수 구현** | 다중 마스터 출현 및 데이터 충돌 100% 원천 방지 |
| Active-Active WAS 구성에서 로컬 메모리에 세션을 저장하여 **로드밸런서가 다른 서버로 라우팅할 때마다 사용자의 로그인이 강제 풀리는 현상 발생** | **WAS 계층을 완전한 무상태(Stateless)로 전환하고 분산 메모리 캐시(Redis Cluster)에 공유 세션 중앙 집중화** | 세션 무결성 유지 및 자유로운 오토스케일링 달성 |

#### 한줄 요약
- N-1 용량으로 연쇄 붕괴를 막고, 쿼럼/STONITH로 스플릿 브레인을 방어하며, Redis로 세션을 중앙 집중화한다.

## Ⅶ. 결론

- 예기치 못한 하드웨어 고장이나 소프트웨어 장애 상황에서도 비즈니스의 생명줄을 무중단으로 유지하는 최상위 인프라 공학인 **고가용성(HA) 아키텍처 체계**는 단순한 서버 다중화를 넘어 시스템 전체의 회복 탄력성(Resilience)을 보증하는 핵심 뼈대이며, 실무 구현 시 **무상태 계층 Active-Active와 상태 저장 계층 Active-Standby의 계층별 최적 분리**, **홀수 쿼럼($(N/2)+1$) 및 STONITH 펜싱 기반 스플릿 브레인 원천 차단**, **N-1 예비 용량 확보 및 무손실 동기 복제**, **카오스 엔지니어링(Chaos Mesh) 기반의 상시 장애 주입 검증**을 완성하여 최고 수준의 무결점 시스템 신뢰성과 비즈니스 연속성을 완성

#### 한줄 요약
- 계층별 Active-Active/Standby 최적화와 쿼럼 펜싱을 통해 완벽한 고가용성 무중단 아키텍처를 완성한다.
