---
title: "Aggregate Root Consistency Boundary"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 애그리게이트 루트(Aggregate Root)는 **불변식(Invariant)이 트랜잭션 단위로 보장되는 클러스터의 유일한 외부 진입점**이며, 일관성 경계(Consistency Boundary)는 **강한 일관성(Strong Consistency)**과 **결과적 일관성(Eventual Consistency)**이 만나는 트랜잭션의 물리적/논리적 경계이다. Eric Evans의 DDD 전술 패턴과 Vaughn Vernon의 "Effective Aggregate Design" 3부작에서 정립된 개념으로, 내부의 Entity/VO 변경은 원자성(Atomicity)을, 외부의 다른 애그리게이트는 **도메인 이벤트(Domain Event)**를 통한 비동기 전파로 분리한다.
> 2. **가치**: 잘못 설계된 경계는 분산 환경에서 **Lost Update, Phantom Read, 재고 음수** 같은 도메인 무결성 오류를 유발하지만, 올바르게 설계하면 **단일 트랜잭션 내 동시성 충돌 90%v**, 마이크로서비스 **Bounded Context 분할 기준** 제공, Eventual Consistency 기반 **Saga/CQRS 적용의 토대**가 된다. Vaughn Vernon의 "한 애그리게이트는 한 사람이 손으로 편집 가능한 크기" 원칙을 따르면 평균 동시 트랜잭션 처리량 3~5배 향상이 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) 애그리게이트 크기 vs 트랜잭션 처리량** — 작을수록 락 경합(lock contention)이 줄지만 원자성 보장이 약해지고, 클수록 강한 일관성이 강해지지만 동시성이 저하된다. **(b) 강한 일관성 vs 결과적 일관성** — Invariant 보호가 필요한 영역(재고, 금액)에는 Aggregate 내부 강제, 그 외(주문 -> 배송, 결제 알림)는 도메인 이벤트로 분리. **(c) ID 참조 vs 객체 참조** — 다른 애그리게이트는 반드시 ID로만 참조하여 결합도를 낮추고, 읽기 전용 조회 모델은 CQRS로 분리한다.

---

## Ⅰ. 개요 및 필요성

**도메인 주도 설계(DDD, Domain-Driven Design)**에서 트랜잭션 일관성을 보장하는 단위는 개별 객체가 아니라 **애그리게이트**다. 객체지향 분석·설계(OOAD) 시대에는 클래스 단위로 잠금(lock)을 걸었으나, 이로 인해 데드락과 동시성 저하가 발생했다. Eric Evans는 2003년 저서 *Domain-Driven Design*에서 **"불변식이 유지되는 클러스터의 경계"**를 애그리게이트로 정의하고, 클러스터 내부에 **Cluster Root**(즉, Aggregate Root) 한 개만을 두어 모든 외부 접근을 강제하도록 설계했다. Vaughn Vernon은 2014년 저서 *Implementing Domain-Driven Design*에서 "**한 트랜잭션은 한 애그리게이트만 수정해야 한다(HTTP PUT, RDBMS의 경우 단일 Tx)**"는 원칙을 명확히 하며, 이를 실전 패턴으로 정교화했다.

전통적인 CRUD 트랜잭션 스크립트
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 475 / 600

<- **이전**: [474. 바운디드 컨텍스트 컨텍스트 매핑](/studynote/11_design_supervision/06_exam_summary/474_bounded_context)
**다음**: [476. 유비쿼터스 언어 도메인 모델링](/studynote/11_design_supervision/06_exam_summary/476_ubiquitous_language/) ->

---
