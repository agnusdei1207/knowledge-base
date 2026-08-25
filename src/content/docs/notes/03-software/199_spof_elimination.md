---
sidebar:
  order: 199
  label: "199. 단일 장애점 SPOF 제거"
  badge:
    text: "기출 · 50%"
    variant: note
title: "단일 장애점 SPOF 제거 (SPOF Elimination)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 199
extra:
  question_no: "199"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "단일 장애점 제거는 고가용성 설계 하위축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SPOF (Single Point of Failure)**: 단 하나의 구성요소 결함으로 인해 전체 시스템이 마비되는 치명적인 단일 취약 지점.
- **Hidden Logical SPOF**: 서버 이중화 뒤에 숨겨진 단일 DNS, 공유 NFS 스토리지, 단일 인증 DB 등의 논리적 단일 종속성.

</details>

- 정의/개념: 단일 요소의 고장이 전체 서비스 마비로 이어지지 않도록 **물리·논리적 단일 장애점(SPOF)을 식별하고 전 계층 다중화 및 장애 격리를 구현하는 설계 기법**
- 배경/필요성: 서버를 다중화했음에도 단일 DNS, 공유 스토리지, 공통 인증 DB 등 **숨겨진 논리적 SPOF 결함으로 인한 전사 서비스 연쇄 다운 해결 불가**

#### 한줄 요약
- 의존성 맵과 FMEA 분석을 통해 물리·논리적 SPOF를 제거하고 장애 격리를 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **FMEA(Failure Mode and Effects Analysis)**: 각 구성요소의 고장 형태와 파급 영향도를 체계적으로 평가하여 SPOF를 발굴하는 기법.
- **Circuit Breaker**: 외부 연계 서비스 장애 시 호출을 즉시 차단하여 스레드 고갈 및 연쇄 장애 전파를 방어하는 패턴.

</details>

- 시스템 전체의 하드웨어, 소프트웨어, 네트워크 의존성을 전수 조사하는 **의존성 맵 기반 가시화**
- 전원, 스위치, 가용영역(AZ)을 완전히 분리하는 **물리적·논리적 다중화(Redundancy)**
- 제어 경로(Control Plane)와 데이터 경로(Data Plane)를 분리하는 **대역 외(Out-of-Band) 관리 체계**

#### 한줄 요약
- 전수 의존성 분석, 전 계층 다중화, 제어/데이터 경로 분리를 통해 무결점 내결함성을 확립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SPOF 제거 4대 계층 아키텍처**: Entry Layer(다중 DNS/CDN), Service Layer(Multi-AZ 무상태), Data Layer(쿼럼/동기 복제), Control Layer(대역 외 관리망).

</details>

```text
[전 계층 단일 장애점(SPOF) 제거 및 장애 격리 구조]
|-- 1. Entry Layer: Anycast Multi-DNS & Multi-CDN (도메인/CDN 단일 장애점 제거)
`-- 2. Service Layer: Multi-AZ Stateless Pods & Cell Architecture
    |-- Kubernetes Multi-AZ HPA 수평 확장 배포
    `-- Resilience4j Circuit Breaker (외부 연계 장애 전파 차단)
`-- 3. Data Layer: Quorum Consensus & Multi-AZ Synchronous Replication
    `-- etcd 3노드 쿼럼 + Aurora Multi-AZ DB + Air-Gap WORM 불변 백업
`-- 4. Control Layer: Out-of-Band Management Network (별도 관리 VLAN/콘솔 분리)
```

선의 의미: 계층 및 진입, 서비스, 데이터, 제어의 전 계층에서 공통 의존성을 제거하고 독립 장애 도메인으로 격리한 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **진입 계층 (Entry)** | 다중 DNS 및 멀티 CDN을 구성하여 **도메인 네임서버 장애 시에도 접속 경로 유지** | 진입로 이중화 |
| **서비스 계층 (Service)** | Multi-AZ 수평 확장 및 서킷 브레이커로 **특정 서버/AZ 고장 시에도 무중단 처리** | 장애 격리/확장 |
| **데이터 계층 (Data)** | Raft 쿼럼 및 교차 AZ 동기 복제로 **단일 DB 장애 시 데이터 유실 없이 승격** | 쿼럼 무결성 |
| **제어 계층 (Control)** | 서비스 망과 분리된 독립 대역 외(Out-of-Band) 관리망으로 **장애 노드 강제 격리** | 비상 통제권 확보 |

#### 한줄 요약
- 진입, 서비스, 데이터, 제어 계층이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SPOF 제거 5단계**: 의존성 지도 작성 $\to$ FMEA 고장 분석 $\to$ SPOF 목록화 $\to$ 다중화/격리 설계 $\to$ 장애 주입(Fault Injection) 검증.

</details>

```text
SPOF 식별 및 제거 프로젝트 착수
        │
   1. [전사 의존성 맵 작성] DNS, 웹, DB, 스토리지, 외부 PG사까지의 전사 호출 그래프 도출
        │
   2. [FMEA 고장 영향도 분석] 단일 부품 결함 시 전체 시스템에 미치는 심각도(RPN) 전수 평가
        │
   3. [숨겨진 SPOF 도출] 공유 Redis 캐시 및 단일 DNS 네임서버가 전사 핵심 SPOF임을 식별
        │
   4. [다중화 및 격리 설계] Redis를 Multi-AZ 센티널로 전환하고 보조 DNS 및 서킷 브레이커 구축
        │
   5. [장애 주입 실증 검증] Chaos Mesh로 프라이머리 Redis 파드를 강제 Kill하여 무중단 전환 실증
```

#### 한줄 요약
- 의존성 작성 → FMEA 분석 → SPOF 도출 → 다중화 설계 → 장애 주입 검증 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SPOF 제거 3대 접근법**: 무상태 수평 다중화, 상태형 쿼럼 이중화, 기능 점진적 저하(Graceful Degradation).

</details>

| 비교 항목 | 무상태 수평 다중화 | 상태형 쿼럼 이중화 | 점진적 기능 저하 (Graceful Degradation) |
|:---|:---|:---|:---|
| 핵심 관리 대상 | **웹 서버, API 게이트웨이, 무상태 앱** | **핵심 RDBMS, NoSQL, etcd 분산 저장소** | **AI 추천 엔진, 댓글, 마케팅 배너 등 부가 기능**|
| 장애 복구 방식 | **로드밸런서에서 불량 노드 자동 제외**| **과반수 합의(Quorum) 기반 신규 리더 승격** | **서킷 브레이커 오픈 후 정적 캐시/더미 응답** |
| 구현 복잡도 | 낮음 (HPA 수평 확장으로 달성) | 중간~높음 (스플릿 브레인 방어 필요) | 중간 (폴백 로직 및 서킷 브레이커 구현) |
| 가용성 보장 수준 | 무중단 트래픽 분산 보장 | 수 초 이내 자동 페일오버 보장 | 핵심 결제는 정상 유지, 부가 기능만 차단 |

#### 한줄 요약
- 무상태는 수평 다중화, 데이터베이스는 쿼럼 이중화, 부가 기능은 서킷 브레이커 점진적 저하를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cell-Based Architecture**: 전체 시스템을 독립된 세포(Cell) 단위로 분할하여 특정 셀 장애가 전체 고객으로 확산되지 않도록 폭발 반경(Blast Radius)을 격리하는 설계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 서버 이중화 후 동일한 공유 스토리지(NFS) 장애로 전사 다운 | **공유 스토리지 종속을 제거하고 분산 객체 스토리지(S3/Ceph)로 전환** | 인프라 단일 장애점 100% 제거 |
| 서비스 망과 관리망이 동일하여 네트워크 마비 시 페일오버 명령 불가 | **별도 VLAN 및 콘솔 기반 '대역 외(Out-of-Band) 관리망' 구축** | 비상 원격 제어 통제권 확보 |
| 설계 상으로만 SPOF를 제거하고 실제 운영 장애 시 페일오버 실패 | **정기적 카오스 엔지니어링(Chaos Monkey) 장애 주입 테스트 의무화** | 실전 내결함성 신뢰도 확보 |
| 특정 고객 트래픽 폭주로 인한 전사 공용 자원 고갈 | **셀 아키텍처(Cell Architecture)를 도입하여 장애 폭발 반경 1% 격리** | 테넌트 간 장애 격리 달성 |

#### 한줄 요약
- 공유 스토리지 제거, 대역 외 관리망 분리, 카오스 테스트, 셀 아키텍처로 운영한다.

## Ⅶ. 결론

- 시스템의 불의의 단일 결함으로 인한 서비스 전면 마비를 방지하기 위해 **FMEA 분석을 통해 전 계층의 물리·논리적 숨겨진 SPOF를 전수 식별**하고, **Multi-AZ 다중화, 쿼럼 기반 상태 동기화, 서킷 브레이커 및 카오스 엔지니어링 실증**을 결합하여 완벽한 내결함성 인프라 완성

#### 한줄 요약
- SPOF 제거는 전 계층 독립 다중화, 쿼럼 합의, 서킷 브레이커, 카오스 검증을 통해 단 하나의 결함으로도 서비스가 중단되지 않도록 보장하는 핵심 아키텍처 엔지니어링 기술이다.