---
sidebar:
  order: 48
  label: "048. 헥사고날 아키텍처: 포트•어댑터"
  badge:
    text: "미출 · 50%"
    variant: note
title: "헥사고날 아키텍처: 포트•어댑터 (Hexagonal Architecture)"
date: "2026-08-26T09:39:00+09:00"
tags:
  - "notes-software"
weight: 48
extra:
  question_no: "048"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "포트•어댑터는 도메인 의존성 격리 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **헥사고날 아키텍처(Ports & Adapters)**: 앨리스터 코번(Alistair Cockburn)이 제안한, 순수 비즈니스 로직을 중심에 두고 외부 DB/웹을 포트와 어댑터로 격리하는 아키텍처.
- **포트(Port) & 어댑터(Adapter)**: 도메인이 정의한 인터페이스 규격(포트)과 외부 기술(JPA, REST)을 포트에 맞게 구현한 변환기(어댑터).

</details>

- 정의/개념: 핵심 비즈니스 로직을 중심에 두고 외부 프레임워크 및 DB와의 결합을 **포트(Port)와 어댑터(Adapter)** 인터페이스로 격리하는 아키텍처
- 배경/필요성: 전통적 계층형(Layered) 구조의 **DB 중심 상위 의존성 전파 및 비즈니스 로직의 독립적 테스트 불가 해결 불가**

#### 한줄 요약
- 도메인 중심 의존성 역전을 통해 외부 인프라 기술 변경에 독립적인 비즈니스 로직을 구축한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **인바운드 vs 아웃바운드 포트**: 외부에서 도메인을 호출하는 진입 인터페이스(Inbound/Driver)와 도메인이 외부 DB/메시징을 호출하는 출력 인터페이스(Outbound/Driven).
- **DIP(의존역전)**: 어댑터가 도메인 포트를 바라보게 하여 모든 의존성 화살표가 도메인 코어 안쪽을 향하도록 역전시키는 원칙.

</details>

- **인바운드(Inbound) 및 아웃바운드(Outbound)** 포트 분리를 통한 도메인 코어의 순수성 보장
- 어댑터가 도메인 포트를 구현하도록 강제하는 **의존성 역전 원칙(DIP)** 전면 적용
- 외부 DB나 웹 프레임워크 없이도 Mock 객체를 주입하여 **순수 POJO 초고속 단위 테스트** 가능

#### 한줄 요약
- 포트 기반 의존성 역전으로 도메인 코어를 외부 인프라 기술과 완벽히 격리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **POJO(Plain Old Java Object)**: 특정 프레임워크(Spring, JPA) 어노테이션이나 상속에 종속되지 않은 순수한 자바 객체.

</details>

```text
[헥사고날(Ports & Adapters) 아키텍처 구조]
|-- 인바운드 어댑터 (Driving / Inbound Adapters: 외부 진입점)
|   |-- REST Controller (HTTP JSON 요청)
|   `-- Kafka Consumer (메시지 이벤트 수신)
|-- 인바운드 포트 (Inbound Port: UseCase Interface)
|-- 도메인 코어 (Domain Core: 순수 POJO Entity & Domain Service)
|-- 아웃바운드 포트 (Outbound Port: SPI Interface - Repository, MailSender)
`-- 아웃바운드 어댑터 (Driven / Outbound Adapters: 인프라 구현체)
    |-- JPA Repository Adapter (RDBMS 영속화)
    `-- Kafka Event Producer Adapter (외부 이벤트 발행)
```

선의 의미: 계층 및 의존성 역전(DIP) 안쪽 진입 구조

| 구성요소 | 책임 |
|:---|:---|
| 인바운드 어댑터 (Driving) | HTTP, gRPC, CLI 요청을 파싱하여 **도메인 커맨드 객체로 변환 후 포트 호출** |
| 인바운드 포트 (Inbound Port) | 애플리케이션 코어가 외부에 노출하는 **유스케이스(UseCase) 인터페이스** 정의 |
| 도메인 코어 (Domain Core) | 외부 프레임워크 종속성 없이 **순수 비즈니스 엔티티 및 규칙 연산 수행** |
| 아웃바운드 포트 (Outbound Port) | 도메인이 인프라에 요구하는 영속성/메시징 기능을 정의한 **SPI 인터페이스** |
| 아웃바운드 어댑터 (Driven) | 아웃바운드 포트를 구현하여 **실제 JPA SQL 실행 또는 Kafka 메시지 전송** |

#### 한줄 요약
- 인바운드 어댑터/포트, 순수 도메인 코어, 아웃바운드 포트/어댑터가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **도메인 모델 매핑(Domain Model Mapping)**: 외부 DTO와 JPA Entity를 순수 도메인 객체로 상호 변환하여 계층 간 오염을 차단하는 기법.

</details>

```text
외부 클라이언트의 HTTP 주문 생성 요청 인입
        │
   인바운드 어댑터(REST Controller): 요청 DTO 검증 및 CreateOrderCommand 생성
        │
   인바운드 포트(OrderUseCase) 인터페이스 호출
        │
   도메인 서비스가 비즈니스 규칙(재고 확인, 가격 계산)을 순수 POJO로 수행
        │
   도메인이 아웃바운드 포트(OrderRepositoryPort SPI) 인터페이스 호출
        │
   아웃바운드 어댑터(JPA Adapter): 도메인 객체를 JPA Entity로 매핑 후 DB 커밋
```

#### 한줄 요약
- HTTP 수신 → Command 변환 → 인바운드 포트 실행 → 도메인 규칙 연산 → 아웃바운드 어댑터 저장 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **계층형 vs 헥사고날 vs 클린 아키텍처**: 데이터베이스 중심의 계층형과 도메인 중심 의존성 역전의 헥사고날/클린 아키텍처.

</details>

| 비교 항목 | 계층형 아키텍처 (Layered) | 헥사고날 아키텍처 (Hexagonal) | 클린 아키텍처 (Clean) |
|:---|:---|:---|:---|
| 의존성 방향 | **상위 $\to$ 하위 (DB 중심 종속)** | **외부 $\to$ 내부 도메인 코어 (DIP)** | 외부 $\to$ 내부 엔티티 (의존성 규칙) |
| 기술 결합도 | JPA/RDBMS에 비즈니스 로직 결합 | **프레임워크/DB 완전 격리 (POJO)** | 프레임워크/DB 완전 격리 |
| 테스트 용이성 | Spring/DB 기동 필요 (느린 테스트) | **Mock 주입 순수 단위 테스트 (수 ms)** | Mock 주입 순수 단위 테스트 |
| 코드 복잡도 | 낮음 (초기 개발 빠름) | 포트/어댑터/매퍼로 다소 증가 | UseCase/Presenter 세분화로 높음 |

#### 한줄 요약
- 단순 CRUD는 계층형, 복잡한 비즈니스 규칙과 장기 유지보수는 헥사고날/클린 아키텍처가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **MapStruct**: 컴파일 타임에 DTO $\leftrightarrow$ Domain Model $\leftrightarrow$ JPA Entity 간의 변환 코드를 자동 생성해주는 매핑 라이브러리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| JPA `@Entity` 어노테이션으로 인한 도메인 모델 오염 | **순수 도메인 엔티티와 JPA 영속성 엔티티 물리 분리** | DB 테이블 변경이 비즈니스 로직에 영향 0화 |
| 계층 간 객체 매핑(DTO/Entity)으로 보일러플레이트 급증 | **MapStruct 컴파일 타임 매퍼 라이브러리** 표준화 | 매핑 코드 수작업 오버헤드 90% 제거 |
| 단순 CRUD 도메인에 헥사고날 적용 시 오버엔지니어링 | **도메인 복잡도에 따른 하이브리드 적용 (핵심만 헥사고날)** | 개발 생산성과 유지보수성의 최적 절충 |
| 포트 인터페이스 명명 규칙 혼선 | **`Inbound/UseCase`, `Outbound/Port` 명명 표준화** | 개발팀 내 아키텍처 일관성 확립 |

#### 한줄 요약
- 엔티티 물리 분리, MapStruct 자동화, 선택적 적용, 명명 규칙 표준화로 실무 완성도를 높인다.

## Ⅶ. 결론

- 도메인 격리는 **헥사고날**, 인프라 연계는 **어댑터** 선택

#### 한줄 요약
- 헥사고날 아키텍처는 포트와 어댑터를 통해 비즈니스 로직을 기술 인프라로부터 해방시키는 도메인 중심의 현대 소프트웨어 아키텍처다.