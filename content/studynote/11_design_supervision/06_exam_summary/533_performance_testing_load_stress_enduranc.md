+++
title = "533. 퍼포먼스 테스팅 부하 스트레스 엔듀런스 (Performance Testing Load Stress Endurance)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼포먼스 테스팅은 시스템의 **응답시간(Latency)·처리량(Throughput)·자원 사용률(Utilization)** 3대 KPI를 정량적으로 측정·검증하는 공학적 행위이며, 부하(Load)·스트레스(Stress)·엔듀런스(Endurance) 테스트는 각각 **"예상 피크의 검증", "한계점·회복력의 탐색", "장기 안정성의 입증"**이라는 서로 다른 목적을 가진 상호 보완적 시험 체계다.
> 2. **가치**: SLA 기준(P99 응답시간 ≤ 1s, 에러율 ≤ 0.1%, 동시 1만 사용자 TPS 5,000 등)을 런칭 전 객관적으로 입증함으로써 **다운타임으로 인한 매출 손실 1분당 약 5,600~9,000 USD(Gartner 통계)**, 고객 이탈(아마존 기준 100ms 지연 시 매출 1% 감소)을 사전에 차단하고, **인프라 CapEx/Opex를 30~50% 절감**하는 용량계획(Capacity Planning)의 정량적 근거를 산출한다.
> 3. **판단 포인트**: 워크로드 모델링 시 **사고시간(Think Time)·랜덤화·트랜잭션 믹스·워밍업 구간**을 실 운영 트래픽과 일치시켜야 통계적 유의성이 생기며, **인젝터-제네레이터-모니터링 분리**, **클라우드 비용 폭증 방지(스팟 인스턴스·오토스케일링)**, **마스킹된 실데이터 vs 합성 데이터**, **CI/CD 파이프라인 임베드** 여부가 기술사적 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

현대 엔터프라이즈 시스템은 MSA(Microservices Architecture), 이벤트 드리븐(Event-Driven), 클라우드 네이티브(Cloud-Native)로 진화하며 **수십~수백 개 컴포넌트 간 동기/비동기 호출, 외부 API, 캐시, 메시지 브로커, DB 샤딩**이 얽힌 분산 시스템이 되었다. 이러한 환경에서 **기능적 정합성(Functional Correctness)만으로는 시스템의 가치를 보증할 수 없으며**, 트래픽이 폭증하는 블랙프라이데이, 신년 이벤트, 마케팅 프로모션 등에서 시스템이 "터지지 않는다"는 비기능 요구사항(Non-Functional Requirement)을 정량적으로 입증하는 유일한 수단이 퍼포먼스 테스팅이다.

과거 모놀리식 JSP/Servlet 기반 시스템은 **단일 WAS + 단일 DB**였기에 부하 테스트가 단순했지만, 현재의 시스템은 다음과 같은 이유로 인해 성능 시뮬레이션 난이도가 기하급수적으로 상승했다.

1. **다층 의존성(Layered Dependency)**: API Gateway -> BFF -> MSA × N -> Kafka/RabbitMQ -> RDB/NoSQL -> External API로 이어지는 호출 체인에서 **단일 노드 병목이 전체 SLA를 결정**한다.
2. **동적 스케일링**: Kubernetes HPA, AWS Auto Scaling Group이 동작하는 환경에서는 **스케일 아웃 지연(Cold Start, Image Pull), DB Connection Pool 고갈, 캐시 미스 폭증** 등 스케일링 자체가 병목이 될 수 있다.
3. **다양한 트래픽 패턴**: 일반 트래픽(Steady-State), 피크 트래픽(Burst), 주기적 트래픽(Daily Cycle), 외부 이벤트 유발 트래픽 등 **워크로드 모델링(Workload Modeling)**이 점점 복잡해졌다.
4. **비동기·배치 워크로드 혼재**: REST API 같은 동기 트래픽 외에 Kafka Consumer, Cron Batch, CDC(Change Data Capture) 같은 백그라운드 워크로드가 자원을 두고 경합한다.
5. **데이터 볼륨**: 단순 조회 API라 할지라도 **10억 건 테이블 풀스캔 vs 인덱스 탐색**은 수천 배 성능 차이를 만든다(Volume Testing 필요).

따라서 **부하(Load)·스트레스(Stress)·엔듀런스(Endurance) 테스트는 "시스템을 실제로 깨뜨려 보며 한계와 회복력을 파악하는 파괴적 검증(Destructive Verification)"**이라 할 수 있다.

```text
  +------------------------------------------------------------------+
  |         퍼포먼스 테스트 3대 축: 부하 · 스트레스 · 엔듀런스        |
  +------------------------------------------------------------------+

        사용자 수 / 트래픽
             ^
             |
  20K - - - +- - - - - - - - - - - - - - - - - - - - - -  <- 스트레스

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 533 / 600

<- **이전**: [532. 모델 기반 테스팅 MBT 자동화](/knowledge-base/studynote/11_design_supervision/06_exam_summary/533_model_based_testing_mbt_automation/)
**다음**: [534. 보안 테스팅 OWASP 취약점 진단](/knowledge-base/studynote/11_design_supervision/06_exam_summary/534_security_testing_owasp_vulnerability/) ->

---
