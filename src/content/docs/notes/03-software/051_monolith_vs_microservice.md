---
sidebar:
  order: 51
  label: "051. 모놀리식 vs 마이크로서비스 비교 (Monolith vs Microservice)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "모놀리식 vs 마이크로서비스 비교 (Monolith vs Microservice)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 51
extra:
  question_no: "051"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "135회 기출, 배포•결합도•운영 절충"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Monolithic Architecture**: 모든 비즈니스 기능, 데이터베이스 억세스 및 UI 처리 로직이 단일 실행 단위(Single Deployment Unit) 및 코드베이스로 묶여 작동하는 전통적 아키텍처.
- **Microservice Architecture (MSA)**: 비즈니스 도메인(Bounded Context) 단위로 분할된 소형 독립 서비스들이 자체 DB와 CI/CD 파이프라인을 구동하며 REST/gRPC로 통신하는 분산 아키텍처.
- **Modulith (Modular Monolith)**: Monolithic과 MSA의 중간 대안으로, 단일 프로세스 실행 단위를 유지하되 코드 모듈 간 경계(Module Boundary)를 엄격히 분리한 구조.

</details>

- 정의/개념: 단일 배포 파일의 개발 단순성(Monolithic) 대 소형 독립 서비스의 민첩한 배포/확장성(MSA) 간 아키텍처 양대 패러다임 비교 분석인 **Monolith vs Microservice**
- 배경/필요성: 무분별한 MSA 도입으로 인한 분산 오버헤드(Distributed Overhead) 폭발 방지, 프로젝트 초기와 성숙도 단계별 아키텍처 이행(Migration) 체계 수립 요구성

#### 한줄 요약

- 모놀리식과 마이크로서비스는 변경•확장 독립성과 분산 운영 비용이 다르다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Coupling & Cohesion**: Monolithic은 인메모리 함수 호출의 강한 결합(High Coupling)과 트랜잭션 수월성이 특징인 반면, MSA는 느슨한 결합(Loose Coupling)과 독립적 확장성 강조.
- **Distributed Overhead**: MSA 전환 시 발생하는 네트워크 latency, 데이터 최종 일관성(Eventual Consistency) 관리, 분산 Tracing 등 분산 시스템 고유의 복잡도 및 비용.

</details>

- 단일 DB 중심 **ACID Transaction** 및 초고속 인메모리 함수 호출 (**Monolithic**)
- **Database-per-Service** 및 서비스 단위 **Independent Deployment & Scale-out** (**MSA**)
- **Distributed Overhead (분산 트랜잭션, 분산 모니터링, Network Latency)** 의 트레이드오프

#### 한줄 요약

- 내부 호출, 독립 배포, 분산 일관성의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Strangler Fig Pattern (스트랭글러 패턴)**: 레거시 Monolithic 시스템의 기능을 하나씩 마이크로서비스로 떼어내어 점진적으로(Incremental) MSA로 이행하는 전환 아키텍처 패턴.

</details>

```text
+-- 모놀리식 ------------------+
| [단일 애플리케이션]          |
|            |                 |
| [공용 데이터 저장소]         |
+------------------------------+

+-- 마이크로서비스 ------------+
| [요청 라우터 (API Gateway)]  |
|            |                 |
| [독립 서비스군]              |
|            |                 |
| [전용 데이터 저장소군]       |
+------------------------------+
```

선의 의미: Monolithic은 단일 App이 중앙 DB를 바라보지만, MSA는 API Gateway가 전용 DB를 보유한 개별 독립 서비스로 라우팅하는 아키텍처 비교.

| 아키텍처 비교 항목 | Monolithic Architecture | Microservice Architecture (MSA) |
|:---|:---|:---|
| 배포 단위 (Deployment) | **단일 묶음 실행 파일 (JAR/WAR)** | **수십 개 개별 컨테이너 (Docker Pod)** |
| 데이터베이스 | 단일 중앙 RDBMS 공유 | **Database-per-Service (독립 DB)** |
| 통신 메커니즘 | **In-memory Direct Function Call** | **Network IPC (REST, gRPC, Kafka)** |
| 트랜잭션 특성 | **ACID (Atomicity, Consistency)** | **Eventual Consistency (Saga Pattern)** |
| 스케일링 (Scale) | 애플리케이션 전체 Scale-up/out | **특정 병목 서비스만 선택적 Scale-out** |
| 조직 구조 | 기능별 조직 (DBA, Backend, QA) | **Cross-Functional Team (1팀 1서비스)** |

#### 한줄 요약

- 공용 데이터 저장소, 전용 데이터 저장소, API의 구조 차이가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Architecture Migration Threshold**: Monolithic의 코드 복잡도가 극에 달해 MSA의 분산 운영 비용을 상회하는 시점에 실행하는 아키텍처 전환 임계 지점.

</details>

```text
┌──────────────────────────────┐
│ 아키텍처 선택 결정           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 도메인 복잡도 & 팀 규모   │
├──────────────┬───────────────┤
│ (단순/소규모)│ (복잡/대규모) │
│              ▼               ▼
│  [Monolithic 선택]     [MSA 선택]
│        │                     │
│        ▼                     ▼
│  (Modulith 정립)   (Strangler Fig 이행)
└──────────────────────────────┘
```

### 동작 원리

1. **초기 사업 단계**: 빠른 검증과 적은 인력을 위해 **Monolithic (또는 Modulith)** 으로 속도감 있게 개발.
2. **복잡도 증가**: 사용자와 기능이 폭증하며 빌드/배포 병목 및 DB Lock 경합 발생.
3. **아키텍처 전환 판정**: **DDD Bounded Context** 도출 및 **Strangler Fig Pattern** 도입.
4. **점진적 MSA 분구**: 레거시 Monolith에서 주요 서비스를 하나씩 떼어내어 **Database-per-service** 구축 및 완결.

#### 한줄 요약

- 변경•확장 주기 결합, 트랜잭션 결합, 서비스 경계 성숙도, 분산 운영 역량이 선택 기준이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **First Rule of Distributed Systems**: "분산 시스템을 만들지 마라(Don't distribute), 정말 어쩔 수 없이 필요할 때까지는." - Martin Fowler.

</details>

| 아키텍처 형태 | 구현 난이도 | 운영 오버헤드 | 적합한 스타트업/기업 환경 |
|:---|:---|:---|:---|
| **Monolithic** | 낮음 | 매우 낮음 | **초기 창업 팀, 비즈니스 모델 검증 단계 (MVP)** |
| **Modulith** | 중간 | 낮음 | **성장기 스타트업, 코드 정리가 필요한 중형 시스템** |
| **Microservice** | 매우 높음 | 매우 높음 (K8s, CI/CD 필수)| **대규모 엔터프라이즈, 수백 명의 개발 조직** |

#### 한줄 요약

- 주기가 같으면 모놀리식, 다르면 마이크로서비스가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Premature Optimization (조기 최적화)**: 도메인에 대한 이해가 부족한 초기 단계에서 유행을 따라 무작정 MSA를 도입하여 시스템을 파행으로 모는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기술 역량이 부족한 팀이 조기 MSA 도입으로 시스템 붕괴 | **Modulith (Modular Monolith)** 아키텍처 선적용 | 코드 모듈성 확보 및 분산 비용 0% |
| Monolithic에서 한번에 전체를 MSA로 재구축(Re-platforming) 실패 | **Strangler Fig Pattern** 기반 점진적 이행 | 이행 리스크 최소화 |
| MSA 서비스 간 동기 호출 폭증으로 지연시간 증가 | **Event-Driven Architecture (Kafka)** 비동기 전환 | 통신 결합도 소멸 |

> 사례: 쿠팡 / 우아한형제들(배달의민족)의 **Monolith $\rightarrow$ Modulith $\rightarrow$ MSA** 단계적 성장 진화 모델

#### 한줄 요약

- 데이터 소유권, 회로 차단, 보상 처리, 분산 추적, 트래픽 전환으로 분산 운영을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **아키텍처 선택 기준(Architecture Paradigm Selection Criteria)**: 조직 규모, 비즈니스 성숙도, DevOps 자동화 수준 및 도메인 복잡도에 의거한 체계.

</details>

- **아키텍처 선택 기준**에 따라 무분별한 MSA 지양 및 **초기 Monolith/Modulith $\rightarrow$ 성숙 시 점진적 MSA** 진화 모델 채택

#### 한줄 요약

- 서비스 독립성 이익과 분산 시스템 비용을 함께 평가하는 것이 핵심이다.
