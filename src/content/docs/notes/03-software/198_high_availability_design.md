---
sidebar:
  order: 198
  label: "198. 고가용성 설계: Active-Active•Active-Standby"
  badge:
    text: "기출 · 70%"
    variant: note
title: "고가용성 설계: Active-Active•Active-Standby (High Availability Design)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 198
extra:
  question_no: "198"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "이중화 방식과 장애 전환 비교가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **고가용성(High Availability)**: 시스템의 단일 장애점(SPOF)을 제거하고 인프라와 소프트웨어를 다중화하여 99.999%(Five Nines) 무중단 가용성을 달성하는 아키텍처.
- **Active-Active vs Active-Standby**: 모든 노드가 동시에 트래픽을 처리하는 방식(Active-Active)과 주 노드 장애 시 대기 노드가 승격하는 방식(Active-Standby).

</details>

- 정의/개념: 단일 장애점(SPOF)을 제거하고 다운타임을 극소화하기 위해 **컴포넌트를 다중화하고 자동 페일오버를 구현하는 고가용성 설계 체계**
- 배경/필요성: 단일 서버나 인프라 노드 장애 발생 시 전체 서비스가 전면 마비되는 단일 장애점(SPOF)의 취약점과, 페일오버 과정에서 양쪽 노드가 동시에 활성화되어 데이터를 파괴하는 스플릿 브레인(Split-Brain) 위험을 해결하기 위해, 모든 계층(웹/앱/DB/네트워크)을 2개 이상의 독립 가용영역(AZ)에 다중화(Active-Active, Active-Standby)하고 쿼럼(Quorum) 합의 및 STONITH 펜싱을 적용하는 고가용성(HA) 아키텍처를 도입하여 **99.999%(Five Nines) 무중단 가용성과 데이터 무결성을 달성**할 필요

#### 한줄 요약
- Active-Active와 Active-Standby 다중화 및 쿼럼/펜싱 기반 페일오버를 통해 99.999% 무중단 가용성을 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Quorum Consensus**: 네트워크 단절 시 과반수($N/2+1$) 투표 합의를 통해 오직 한쪽 진영만 Primary로 승격하도록 보장.
- **STONITH(Shoot The Other Node In The Head)**: 페일오버 승격 전 구 Primary 노드의 전원/네트워크를 강제 차단(Fencing)하여 이중 쓰기를 봉쇄.

</details>

- 모든 컴포넌트를 최소 2개 이상의 독립 경로로 구성하는 **완전 다중화(Full Redundancy)**
- 과반수 노드 투표 합의를 통해 단일 Primary를 선출하는 **쿼럼(Quorum) 합의 기반 스플릿 브레인 방어**
- 심층 헬스체크와 가상 IP(VIP) 전환을 통한 **초단기 자동 장애 전환(Failover)**

#### 한줄 요약
- 완전 다중화, 쿼럼 합의, STONITH 펜싱, 자동 페일오버를 통해 서비스 연속성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HA 클러스터 4대 구성요소**: Traffic Controller(로드밸런서), Multi-AZ Nodes(주/대기 노드), Quorum Engine(etcd 과반 합의), Fencing Device(STONITH 전원 차단).

</details>

```text
[고가용성(HA) 다중화 클러스터 및 페일오버 아키텍처]
|-- 트래픽 컨트롤러 (헬스체크·라우팅)
|-- 액티브·스탠바이 노드 (업무 처리·복제)
|-- 쿼럼 엔진 (Primary 합의)
`-- 펜싱 장치 (구 Primary 격리)
```

선의 의미: 계층 및 로드밸런서가 헬스체크로 정상 노드에 라우팅하고 쿼럼과 펜싱 장치가 단일 Primary를 유지하며 복제를 수행하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 트래픽 컨트롤러 | 비정상 노드 배제와 **정상 노드 라우팅** |
| 액티브·스탠바이 노드 | **업무 처리·실시간 복제** |
| 쿼럼 엔진 | 과반 합의로 **단일 Primary 보장** |
| 펜싱 장치 | 구 Primary를 격리해 **스플릿 브레인 방지** |

#### 한줄 요약
- 다중화만으로는 어느 쪽이 주인인지 정할 수 없어 쿼럼 엔진과 펜싱 장치가 그 판정과 강제 격리를 대신 떠맡으며, 그때 비로소 이중화가 가용성으로 바뀐다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **자동 장애 전환 5단계**: 헬스체크 실패 $\to$ STONITH 펜싱 격리 $\to$ Quorum 승격 합의 $\to$ 데이터 무결성 검증 $\to$ VIP/트래픽 전환.

</details>

```text
Active 노드 장애 발생 (Heartbeat 두절)
        │
   1. [장애 감지] 로드밸런서 및 감시 데몬이 Active 노드의 헬스체크 3회 연속 실패 감지
        │
   2. [STONITH 펜싱] 스플릿 브레인 방지를 위해 구 Active 노드의 전원/네트워크 강제 차단
        │
   3. [Quorum 승격 합의] 3노드 etcd 클러스터의 과반수(2/3) 합의를 얻어 Standby 노드 승격
        │
   4. [정합성 검증] WAL(Write-Ahead Log) 복제 지점을 대조하여 유실 없는 최신 데이터 무결성 검증
        │
   5. [트래픽 전환] 로드밸런서 VIP 및 라우팅 테이블을 갱신하여 신규 Active로 트래픽 절체 완료
```

#### 동작 원리
- 1. 장애 감지: 연속 **헬스체크 실패 판정**
- 2. STONITH 펜싱: 구 Active의 **전원·네트워크 차단**
- 3. Quorum 승격 합의: 과반수로 **Standby 승격**
- 4. 정합성 검증: WAL 복제 지점의 **무결성 확인**
- 5. 트래픽 전환: VIP를 **신규 Active로 절체**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Active-Active vs Hot Standby vs Warm Standby**: 상시 동시 처리(Active-Active), 즉시 승격 대기(Hot), 기동 시간 소요 대기(Warm).

</details>

| 비교 항목 | 액티브-액티브 (Active-Active) | 핫 스탠바이 (Active-Hot Standby) | 웜 스탠바이 (Active-Warm Standby) |
|:---|:---|:---|:---|
| 트래픽 처리 방식 | **모든 노드가 상시 동시 처리 (부하 분산)** | **주 노드만 처리, 대기 노드는 복제 대기** | 주 노드만 처리, 대기 노드는 최소 기동 |
| 페일오버 시간(RTO) | **사실상 0초 (무중단)** | **수 초 ~ 수십 초 (자동 승격)** | 수 분 ~ 수십 분 (자원 스케일업 필요) |
| 인프라 비용 효율 | **100% 자원 활용 (비용 효율 극대화)** | 유휴 대기 자원 유지 (2배 인프라 비용) | 축소 자원 유지 (상대적 저비용) |
| 최적 적용 대상 | **무상태(Stateless) 웹/앱, NoSQL** | **단일 마스터 필수 RDBMS (Oracle/PG)** | 비핵심 내부 시스템, 스테이징 환경 |

#### 한줄 요약
- 무상태 웹/앱 계층은 Active-Active, 데이터베이스 계층은 Hot Standby, 비핵심은 Warm Standby를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Flapping(플래핑)**: 일시적인 네트워크 지연으로 인해 Active와 Standby가 주도권을 번갈아 바꾸며 서비스가 마비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 일시적 네트워크 지연으로 불필요한 페일오버 반복 (Flapping) | **헬스체크 다중 임계치(3회 이상 연속 실패) 및 쿨다운 시간 설정** | 오탐 페일오버 사고 0건 달성 |
| 네트워크 단절 시 양쪽 노드가 동시 Primary로 동작 (Split-Brain) | **STONITH 펜싱 강제 및 3노드 이상 홀수 쿼럼(Quorum) 합의 의무화** | 데이터 덮어쓰기 충돌 원천 차단 |
| 페일오버 후 단일 노드가 전체 피크 트래픽을 감당 못해 연쇄 다운 | **$N-1$ 부하 테스트 검증 및 K8s HPA 자동 오토스케일링 연계** | 장애 전환 후 2차 다운 완벽 방어 |
| 상태 저장소의 비동기 복제 지연으로 페일오버 시 데이터 유실 | **Semi-Sync(반동기) 복제 및 쿼럼 커밋 기법 적용** | 무손실 페일오버(RPO=0) 달성 |

#### 한줄 요약
- 네 대책은 자동 전환이 만들어 낸 오탐·이중 쓰기·잔여 용량 문제를 감지 지연과 복제 동기화 비용으로 되사는 선택이다.

## Ⅶ. 결론

- 대규모 트래픽을 처리하는 클라우드 네이티브 및 미션 크리티컬 엔터프라이즈 환경에서 무중단 가용성을 보장하는 **가장 핵심적인 시스템 인프라 및 아키텍처 엔지니어링 표준**으로 자리잡았으며, 실무 구축 시에는 **무상태(Stateless) 웹/앱 계층의 Active-Active L7 로드밸런싱, 상태 저장(Stateful) RDBMS의 Hot Standby 및 반동기(Semi-Sync) 복제, 스플릿 브레인을 방어하는 3노드 홀수 쿼럼(etcd) 및 STONITH 전원 펜싱, 플래핑을 방지하는 헬스체크 다중 임계치 통제**를 결합하여 완벽한 자동 장애 절체(Failover) 신뢰성을 완성

#### 한줄 요약
- 고가용성 설계는 독립 장애 도메인 분리, 쿼럼 합의, STONITH 펜싱을 통해 단일 장애점을 제거하고 무중단 서비스를 실현하는 핵심 시스템 엔지니어링 기술이다.
