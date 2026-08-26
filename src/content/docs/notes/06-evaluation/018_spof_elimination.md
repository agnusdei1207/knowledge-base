---
sidebar:
  order: 18
  label: "018. 단일 장애점 SPOF 제거 (SPOF Elimination)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "시스템 전 구간 결함 회피 및 무중단 설계 : 단일 장애점(SPOF) 제거 (Failure Domain & Chaos Engineering)"
date: "2026-08-26T15:33:57+09:00"
tags:
  - "notes-evaluation"
weight: 18
extra:
  question_no: "018"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 단일 장애점(SPOF: Single Point of Failure) 식별 및 제거 방법론, 종단 의존성 맵(End-to-End Dependency Mapping), 계층별 SPOF 제거(DNS Anycast, Multi-AZ 인프라, 분산 쿼럼 제어면, 스토리지 복제), 공통 원인 장애(CCF) 및 카오스 엔지니어링(Chaos Engineering) 복원력 실증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **단일 장애점 제거(SPOF Elimination: Single Point of Failure Elimination)**: 시스템 아키텍처의 전 구간(진입 DNS부터 네트워크, 로드밸런서, 애플리케이션, 데이터베이스, 스토리지, 전원 공급선, 외부 서드파티 API)에서 단 하나의 하드웨어 부품, 소프트웨어 모듈 또는 제어면(Control Plane)의 고장으로 인해 전체 비즈니스 서비스가 전면 마비되는 취약 지점을 전수 식별하고, 물리적 다중화 및 장애 도메인 격리(Failure Domain Isolation)를 통해 원천 제거하는 신뢰성 설계 활동.
- **은닉된 단일 장애점에 의한 전체 서비스 블랙아웃 결함(Hidden SPOF Cascade Defect)**: 수십 대의 WAS 서버를 클러스터링했음에도 불구하고, 단일 내부 DNS 서버, 공유 NFS 스토리지, 단일 인증 토큰 발급기, 또는 단일 PDU 전원 랙의 고장으로 인해 전체 인프라가 도미노처럼 동시 붕괴되는 구조적 결함.

</details>

- 정의/개념: 시스템 전 구간의 결함 격리 독립성을 보증하기 위해 **종단 의존성 맵(End-to-End Dependency Map) 분석 $\rightarrow$ 계층별(진입/컴퓨트/데이터/제어) 잠재 SPOF 식별 $\rightarrow$ 물리적 장애 도메인(Multi-AZ/전원/회선) 분리 $\rightarrow$ N+1 예비 용량 및 자동 페일오버 구축 $\rightarrow$ 카오스 엔지니어링(Chaos Engineering) 기반 장애 주입 실증** 을 집행하는 **내결함성(Fault Tolerance) 엔지니어링 체계**
- 배경/필요성: 분산 의존성 증가로 **숨은 SPOF·CCF** 식별 제약

#### 한줄 요약
- SPOF 제거는 종단 의존성 분석과 장애 도메인 물리적 분리 및 카오스 장애 주입을 통해 단일 고장점을 원천 제거한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPOF 제거 3대 핵심 엔지니어링 원칙**:
  - **종단 의존성 전수 조사 (End-to-End Visibility)**: 사용자 단말부터 외부 결제 PG사까지의 모든 논리적/물리적 호출선 가시화.
  - **물리적 장애 도메인 격리 (Failure Domain Isolation)**: 전원, 냉각, 통신망이 완벽히 독립된 가용영역(Multi-AZ) 이격 배치.
  - **소프트웨어 레벨 결함 격리 (Graceful Degradation)**: 서드파티 API 장애 시 서킷 브레이커(Circuit Breaker)와 Fallback 캐시로 핵심 기능 방어.

</details>

- 장비 다중화와 전원·회선을 나누는 **장애 도메인 분리**
- Raft·Paxos 홀수 노드 기반 **제어면 쿼럼화**
- 실제 장애를 주입하는 **카오스 엔지니어링 검증**

#### 한줄 요약
- 종단 의존성 가시화, Multi-AZ 물리 격리, 분산 쿼럼 제어면, 카오스 장애 주입 실증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **전 계층 SPOF 제거 4대 아키텍처 매트릭스**:
  1. **Entry & Network Tier**: Anycast BGP DNS, 다중 통신사 ISP 회선, VRRP 로드밸런서.
  2. **Compute Tier**: Multi-AZ 분산 컨테이너 클러스터 (N+1 용량 확보, Anti-affinity).
  3. **Data & Storage Tier**: Multi-AZ 동기 복제 DBMS (자동 페일오버), 분산 객체 스토리지(Ceph/S3).
  4. **Control & External Tier**: Raft 분산 쿼럼(etcd), 서킷 브레이커(Resilience4j Fallback).

</details>

```text
전 계층 SPOF 제거 체계
├─ Entry·Network Tier
├─ Compute Tier
├─ Data·Storage Tier
└─ Control·External Tier
```

선의 의미: 진입부터 네트워크, Multi-AZ 컴퓨트, 분산 DB 쿼럼, 외부 연계까지 전 구간의 단일 결함점을 격리하고 이중화한 구조

| 구성요소 | 책임 |
|:---|:---|
| **Entry·Network Tier** | Anycast DNS·다중 회선·VRRP 진입점 보호 |
| **Compute Tier** | Multi-AZ와 N+1 용량으로 노드 장애 수용 |
| **Data·Storage Tier** | 동기 복제와 자동 페일오버로 데이터 보호 |
| **Control·External Tier** | 분산 쿼럼과 서킷 브레이커로 의존성 격리 |

#### 한줄 요약
- Anycast DNS, Multi-AZ 컴퓨트, 3-Node 분산 DB 쿼럼, 서킷 브레이커로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SPOF 전수 식별 및 제거 5단계 수명주기 프로세스**:
  1. 종단 의존성 맵 작성을 통해 인프라, 소프트웨어, 제어면의 단일 의존선 식별
  2. 공통 원인 장애(CCF)가 존재하는 단일 랙/전원/가용영역을 Multi-AZ로 물리적 분리
  3. 모든 컴포넌트에 N+1 예비 용량과 자동 페일오버(VIP 플로팅) 메커니즘 구축
  4. 외부 서드파티 연계 구간에 타임아웃 및 서킷 브레이커 격리벽 설치
  5. 카오스 엔지니어링(Chaos Mesh)으로 무작위 노드 셧다운 테스트를 수행하여 복원력 최종 입증

</details>

```text
1. [종단 의존성 맵 작성 및 SPOF 탐색]
    ├─ 전 구간 호출선 분석: Client ➔ DNS ➔ L4 ➔ WAS ➔ Redis ➔ DB ➔ 외부 결제 PG
    └─ [식별된 치명적 SPOF: 단일 L4 스위치, 단일 Redis 인스턴스, 외부 PG사 동기 호출]
            │
            ▼
2. [물리적 장애 도메인 분리 (Multi-AZ)]
    ├─ 단일 데이터센터 ➔ AWS 3개 가용영역(AZ-a, AZ-b, AZ-c)으로 인프라 재배치
    └─ [독립된 변전소 전원선, 독립된 광케이블 통신로, 독립 냉각 시스템 확보]
            │
            ▼
3. [계층별 이중화 및 자동 페일오버 구축]
    ├─ L4 로드밸런서: Keepalived VRRP 이중화 (VIP 10.0.0.1 자동 인계)
    ├─ Redis 세션: 3-Master 3-Slave Redis Cluster 샤딩 및 자동 복제
    └─ [DB: AZ-a(Primary) - AZ-b(Standby) - AZ-c(Quorum Witness) 3중화]
            │
            ▼
4. [외부 의존성 서킷 브레이커 격리]
    ├─ 외부 결제 PG 호출 구간에 Resilience4j 서킷 브레이커 래핑
    └─ [외부 PG 지연 2초 초과 시 ➔ 서킷 오픈 후 "점검 중 안내 및 예약 결제" Fallback 작동]
            │
            ▼
5. [카오스 엔지니어링 장애 주입 실증]
    ├─ Chaos Mesh 구동 ➔ 대낮 피크 부하 중 AZ-a 전체 네트워크를 강제 단절
    ├─ 실측 결과: AZ-b/c가 3초 내 트래픽 100% 흡수, 사용자 에러율 0.001% 미만 유지
    └─ [SPOF 100% 제거 확인 및 상용 프로덕션 운영 인가]
```

**동작 원리**

1. **종단 의존성 맵 작성 및 SPOF 탐색**: 단일 의존선 식별
2. **물리적 장애 도메인 분리**: 전원·회선·AZ 독립화
3. **계층별 이중화 및 자동 페일오버 구축**: N+1 확보
4. **외부 의존성 서킷 브레이커 격리**: 장애 전파 차단
5. **카오스 엔지니어링 장애 주입 실증**: 복원력 확인

#### 한줄 요약
- 종단 의존성 맵 작성, Multi-AZ 물리 격리, 계층별 이중화 구축, 서킷 브레이커 격리, 카오스 장애 주입 실증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SPOF 3대 유형 및 격리 기법 비교**:
  - 인프라 SPOF: 단일 서버, 전원, 스위치, 스토리지 (하드웨어 레벨).
  - 제어면 SPOF: 단일 마스터 노드, 중앙 스케줄러 (소프트웨어 관리 레벨).
  - 외부 의존성 SPOF: 외부 SMS 인증, PG사 결제, 서드파티 SaaS (외부 연계 레벨).

</details>

| 비교 항목 | 인프라 레벨 SPOF | 제어면 레벨 SPOF | 외부 의존성 SPOF |
|:---|:---|:---|:---|
| **발생 위치** | **단일 물리 서버, 전원 PDU, ToR 스위치**| **단일 K8s Master, 단일 DBMS Master** | **외부 결제 PG, 휴대폰 본인인증, 지도 API**|
| **핵심 제거 기술**| **Multi-AZ 분산, Anycast DNS, VRRP** | **Raft / Paxos 홀수 분산 쿼럼 (Quorum)**| **서킷 브레이커 (Circuit Breaker), 캐시** |
| **복구 메커니즘** | L4/GSLB 트래픽 우회 전환 | **스탠바이 노드의 마스터 승격 (STONITH)**| **Fallback 기본값 반환, 비동기 큐 전환**|
| **장애 시 영향** | 전체 네트워크 및 서버 다운 | 클러스터 제어 및 쓰기 트랜잭션 중단 | 특정 외부 연동 화면 멈춤 및 무한 대기 |
| **검증 방법** | 전원 케이블 강제 발거 시험 | Master 프로세스 강제 kill 시험 | 네트워크 지연/패킷 드롭 퍼징(Fuzzing) |

#### 한줄 요약
- 인프라는 Multi-AZ 분산, 제어면은 Raft 쿼럼 합의, 외부 의존성은 서킷 브레이커로 SPOF를 제거한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SPOF 제거 실무 수행 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| WAS와 DB를 Multi-AZ로 이중화했으나 공통 사내 DNS 서버 1대가 다운되어 **도메인 해석 실패로 전체 시스템이 전면 마비되는 사각지대 SPOF 발생** | **공통 인프라 서비스를 포함한 전 구간 종단 의존성 맵을 작성하고 CoreDNS 및 사설 DNS를 Multi-AZ Anycast로 이중화** | 숨은 인프라 공통 의존성 완벽 제거 |
| 서버 2대를 이중화했으나 동일한 전원 멀티탭(PDU) 및 단일 상단 스위치에 연결되어 **PDU 전원 단락 시 두 서버가 동시에 블랙아웃되는 공통 원인 장애(CCF) 발생** | **서버의 Dual Power Supply를 서로 다른 A/B PDU 전원 라인에 연결하고 네트워크 케이블을 LACP/Bonding으로 이중화** | 전원 및 스위치 단일 고장에 의한 동시 다운 100% 차단 |
| 외부 결제 PG사 API가 30초 타임아웃 지연을 유발하여 **내부 WAS 스레드 200개가 전부 블로킹되어 결제와 무관한 메인 홈 화면까지 마비** | **외부 API 호출 구간에 Resilience4j 서킷 브레이커를 적용하고 타임아웃을 1초로 강제하여 Fallback 응답 즉각 반환** | 외부 장애의 내부 전파 및 스레드 고갈 원천 차단 |

#### 한줄 요약
- 종단 의존성 맵으로 사각지대를 없애고, Dual Power로 CCF를 막으며, 서킷 브레이커로 외부 장애 전파를 차단한다.

## Ⅶ. 결론

- 내부 SPOF는 **Multi-AZ·쿼럼**, 외부 의존성은 **서킷 브레이커** 적용

#### 한줄 요약
- Multi-AZ 물리 격리와 서킷 브레이커 및 카오스 엔지니어링을 통해 완벽한 무결점 SPOF 제거를 완성한다.
