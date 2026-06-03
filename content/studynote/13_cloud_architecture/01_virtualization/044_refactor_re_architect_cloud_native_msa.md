+++
title = "044. Re-factor & Re-architect — 클라우드 네이티브 MSA"
date = 2026-04-05

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

> **핵심 인사이트**
> 1. Re-factor(재구성)와 Re-architect(재설계)는 클라우드 마이그레이션 6R [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 가장 높은 가치를 창출하는 단계로 — Re-factor는 애플리케이션 코드를 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)/서버리스에 최적화하고, Re-architect는 모놀리스를 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))로 근본적으로 재설계한다.
> 2. [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환의 핵심 원칙은 [도메인 주도 설계](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/)([DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/))의 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)([Bounded Context](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/))를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계로 삼는 것으로 — 각 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)는 독립적으로 배포·확장·장애 격리가 가능해야 하며, "두 피자 팀(Two-Pizza Team)"이 소유·운영할 수 있는 크기가 적절하다.
> 3. [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환은 [Strangler Fig Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/308_strangler_fig_pattern/)(교살 무화과 패턴)으로 점진적으로 진행하는 것이 권장되며 — 모놀리스를 즉시 전부 전환하는 "Big Bang" 방식은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 리스크와 복잡성으로 인해 대부분 실패한다.

---

## Ⅰ. 클라우드 마이그레이션 6R



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">6R 마이그레이션 전략:</div>
<div class="kb-diagram-note">1. Retire (폐기):</div>
<div class="kb-diagram-note">더 이상 필요 없는 애플리케이션 폐기</div>
<div class="kb-diagram-note">예: 중복 CRM 시스템</div>
<div class="kb-diagram-note">2. Retain (유지):</div>
<div class="kb-diagram-note">현재 온프레미스 유지 (규제, 레이턴시)</div>
<div class="kb-diagram-note">예: 실시간 금융 거래 코어</div>
<div class="kb-diagram-note">3. Rehost (리호스팅, Lift &amp; Shift):</div>
<div class="kb-diagram-note">코드 변경 없이 클라우드로 이전</div>
<div class="kb-diagram-note">빠르지만 클라우드 혜택 최소화</div>
<div class="kb-diagram-note">4. Replatform (리플랫폼):</div>
<div class="kb-diagram-note">소규모 최적화 (RDS로 DB 이전 등)</div>
<div class="kb-diagram-note">코드 변경 최소화</div>
<div class="kb-diagram-note">5. Re-factor / Re-purchase (재구성):</div>
<div class="kb-diagram-note">클라우드 네이티브로 코드 재작성</div>
<div class="kb-diagram-note">PaaS, 서버리스 활용</div>
<div class="kb-diagram-note">6. Re-architect (재설계):</div>
<div class="kb-diagram-note">아키텍처 근본 변경 (MSA 전환)</div>
<div class="kb-diagram-note">가장 많은 투자, 가장 큰 가치</div>
<div class="kb-diagram-note">Re-factor vs Re-architect:</div>
<div class="kb-diagram-note">Re-factor:</div>
<div class="kb-diagram-note">기존 기능 유지, 구현 방식 변경</div>
<div class="kb-diagram-note">예: 모놀리스 → Lambda + DynamoDB</div>
<div class="kb-diagram-note">Re-architect:</div>
<div class="kb-diagram-note">기능 분리, 서비스 경계 재정의</div>
<div class="kb-diagram-note">예: 모놀리스 → 10개 마이크로서비스</div>
<div class="kb-diagram-note">투자 vs 가치:</div>
<div class="kb-diagram-note">Rehost: 비용 20~30% 절감 (이전 비용 낮음)</div>
<div class="kb-diagram-note">Replatform: 비용 40~50% 절감</div>
<div class="kb-diagram-note">Re-architect: 비용 60~80% 절감 + 민첩성 향상</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 6R은 이사 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 짐 그대로 옮기기(Rehost), 조금 정리하기(Replatform), 새로 디자인하기(Re-architect). 비용은 커지지만 새 집을 제대로 활용할수록 효과도 커요.

---

## Ⅱ. [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 설계 원칙

```
MSA (Microservices Architecture) 원칙:

핵심 원칙:
  1. 단일 책임 (Single Responsibility):
     하나의 서비스 = 하나의 비즈니스 기능
     
  2. 독립 배포 (Independent Deployment):
     각 서비스 독립적 CI/CD
     
  3. 기술 다양성 (Polyglot):
     서비스별 적합한 언어/DB 선택
     
  4. 장애 격리 (Fault Isolation):
     서비스 A 장애 → 서비스 B 영향 최소화
     
  5. 분산 데이터 (Decentralized Data):
     서비스별 독립적 DB

DDD (Domain-Driven Design) 기반 서비스 분리:
  바운디드 컨텍스트 = 서비스 경계
  
  이커머스 도메인 분리:
  모놀리스: 하나의 코드베이스
    └── 사용자, 주문, 상품, 결제, 배송...
    
  MSA:
    사용자 서비스 (User Service)
    상품 서비스 (Product Service)
    주문 서비스 (Order Service)
    결제 서비스 (Payment Service)
    배송 서비스 (Delivery Service)
    알림 서비스 (Notification Service)

서비스 통신:
  동기: REST API, gRPC
  비동기: 메시지 큐 (Kafka, RabbitMQ)
  
  이벤트 소싱 (Event Sourcing):
  상태 대신 이벤트 로그로 상태 재현
  
  CQRS (Command Query Responsibility Segregation):
  쓰기(Command)와 읽기(Query) 분리

Two-Pizza Team:
  Amazon: "팀이 피자 두 판으로 먹을 수 있는 규모" = 6~8명
  하나의 마이크로서비스 = 하나의 팀이 소유·운영
```

> 📢 **섹션 요약 비유**: MSA는 레스토랑 → 푸드코트 전환 — 하나의 주방(모놀리스)에서 모든 요리를 만들다가, 각 음식별 전문점([마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/))으로 분리. 피자 가게가 파스타 가게와 독립적으로 운영.

---

## Ⅲ. [Strangler Fig Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/308_strangler_fig_pattern/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Strangler Fig Pattern (교살 무화과 패턴):</div>
<div class="kb-diagram-note">Martin Fowler 제안</div>
<div class="kb-diagram-note">모놀리스 → MSA 점진적 전환 전략</div>
<div class="kb-diagram-note">이름 유래:</div>
<div class="kb-diagram-note">교살 무화과나무: 기존 나무를 감으며 천천히 대체</div>
<div class="kb-diagram-note">→ 기존 시스템을 유지하면서 새 시스템이 점진적 대체</div>
<div class="kb-diagram-note">전환 단계:</div>
<div class="kb-diagram-note">Stage 1: API Gateway 도입</div>
<div class="kb-diagram-note">모든 트래픽 → API Gateway</div>
<div class="kb-diagram-note">처음에는 모두 모놀리스로 라우팅</div>
<div class="kb-diagram-note">Stage 2: 기능 분리 시작</div>
<div class="kb-diagram-note">가장 독립적인 기능부터 추출</div>
<div class="kb-diagram-note">알림 서비스: 모놀리스에서 분리 (낮은 의존성)</div>
<div class="kb-diagram-note">Gateway → 알림: 신규 서비스</div>
<div class="kb-diagram-note">Gateway → 나머지: 모놀리스</div>
<div class="kb-diagram-note">Stage 3: 점진적 분리 계속</div>
<div class="kb-diagram-note">배송 → 상품 → 결제 순서로 분리</div>
<div class="kb-diagram-note">각 분리 후 검증 (A/B 트래픽)</div>
<div class="kb-diagram-note">Stage 4: 모놀리스 최소화</div>
<div class="kb-diagram-note">핵심 기능만 남은 모놀리스</div>
<div class="kb-diagram-note">Stage 5: 완전 대체</div>
<div class="kb-diagram-note">모놀리스 폐기</div>
<div class="kb-diagram-note">Anti-Pattern (Big Bang):</div>
<div class="kb-diagram-note">전체를 한번에 재설계</div>
<div class="kb-diagram-note">→ 수개월~수년의 "개발 블랙홀"</div>
<div class="kb-diagram-note">→ 서비스 중단 리스크</div>
<div class="kb-diagram-note">→ 대부분 실패</div>
<div class="kb-diagram-note">Strangler 장점:</div>
<div class="kb-diagram-note">비즈니스 연속성 유지</div>
<div class="kb-diagram-note">점진적 위험 관리</div>
<div class="kb-diagram-note">팀 학습 곡선 완화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Strangler Fig는 점진적 집 수리 — 사람이 살면서 방 하나씩 리모델링. 전체 집을 비우고 한꺼번에 고치면(Big Bang) 살 곳이 없어지는 위험.

---

## Ⅳ. [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 패턴



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클라우드 네이티브 패턴:</div>
<div class="kb-diagram-note">1. Circuit Breaker (회로 차단기):</div>
<div class="kb-diagram-note">연쇄 장애 방지</div>
<div class="kb-diagram-note">상태: Closed → Open → Half-Open</div>
<div class="kb-diagram-note">실패 임계값 초과 시 Open → 빠른 실패 반환</div>
<div class="kb-diagram-note">일정 시간 후 Half-Open → 재시도 허용</div>
<div class="kb-diagram-note">도구: Resilience4j, Hystrix</div>
<div class="kb-diagram-note">2. Service Mesh:</div>
<div class="kb-diagram-note">서비스 간 통신 인프라를 사이드카 프록시로 관리</div>
<div class="kb-diagram-note">기능: 로드밸런싱, 암호화, 트레이싱, 레이트 리미팅</div>
<div class="kb-diagram-note">Istio: 가장 많이 사용되는 Service Mesh</div>
<div class="kb-diagram-note">Envoy 사이드카 프록시</div>
<div class="kb-diagram-note">3. API Gateway:</div>
<div class="kb-diagram-note">단일 진입점 (Single Entry Point)</div>
<div class="kb-diagram-note">인증, 라우팅, 로드밸런싱, 로깅</div>
<div class="kb-diagram-note">AWS API Gateway, Kong, nginx</div>
<div class="kb-diagram-note">4. Sidecar Pattern:</div>
<div class="kb-diagram-note">메인 컨테이너 옆에 보조 컨테이너</div>
<div class="kb-diagram-note">로깅, 모니터링, 보안 에이전트</div>
<div class="kb-diagram-note">5. Saga Pattern:</div>
<div class="kb-diagram-note">분산 트랜잭션 처리</div>
<div class="kb-diagram-note">Choreography Saga: 이벤트 기반 자율 조율</div>
<div class="kb-diagram-note">Orchestration Saga: 중앙 조율자(Orchestrator)</div>
<div class="kb-diagram-note">쿠버네티스(Kubernetes) 기반:</div>
<div class="kb-diagram-note">컨테이너 오케스트레이션 표준</div>
<div class="kb-diagram-note">자동 확장 (HPA, VPA)</div>
<div class="kb-diagram-note">자가 치유 (Self-Healing)</div>
<div class="kb-diagram-note">롤링 업데이트</div>
<div class="kb-diagram-note">서비스 디스커버리</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Circuit Breaker는 전기 차단기 — 한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 망가져서 요청이 계속 오면, 전기 차단기처럼 "뚝!" 차단해서 전체 시스템이 쓰러지지 않도록 보호해요.

---

## Ⅴ. 실무 시나리오 — 이커머스 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">대형 이커머스 모놀리스 → MSA 전환:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">Java 모놀리스: 200만 라인 코드</div>
<div class="kb-diagram-note">문제: 배포 6시간, 특정 기능 확장 불가</div>
<div class="kb-diagram-note">목표: 마이크로서비스로 전환</div>
<div class="kb-diagram-note">전환 전략: Strangler Fig</div>
<div class="kb-diagram-note">Phase 1 (Q1): API Gateway 도입</div>
<div class="kb-diagram-note">Kong Gateway 앞단 배치</div>
<div class="kb-diagram-note">기존 모놀리스 유지</div>
<div class="kb-diagram-note">→ 영향 없이 인프라 준비</div>
<div class="kb-diagram-note">Phase 2 (Q2): 알림 서비스 분리</div>
<div class="kb-diagram-note">이메일/SMS 발송 기능 추출</div>
<div class="kb-diagram-note">모놀리스 코드 비활성화</div>
<div class="kb-diagram-note">Gateway에서 알림 요청 → 신규 서비스 라우팅</div>
<div class="kb-diagram-note">A/B 테스트로 안전 검증</div>
<div class="kb-diagram-note">기술: Python FastAPI + AWS SQS + Lambda</div>
<div class="kb-diagram-note">Phase 3 (Q3~Q4): 상품/카탈로그 분리</div>
<div class="kb-diagram-note">가장 높은 조회 트래픽 → 독립 확장 필요</div>
<div class="kb-diagram-note">기술: Go + Redis + Elasticsearch</div>
<div class="kb-diagram-note">오토스케일링 효과:</div>
<div class="kb-diagram-note">기존: 전체 모놀리스 스케일업 (비효율)</div>
<div class="kb-diagram-note">신규: 상품 서비스만 스케일 (20→200 인스턴스)</div>
<div class="kb-diagram-note">Phase 4~6 (다음 해): 주문/결제/배송 분리</div>
<div class="kb-diagram-note">결과 (2년 후):</div>
<div class="kb-diagram-note">배포 시간: 6시간 → 15분</div>
<div class="kb-diagram-note">장애 격리: 알림 장애 → 결제 영향 없음</div>
<div class="kb-diagram-note">팀 자율성: 각 팀 독립 배포 주 3회 이상</div>
<div class="kb-diagram-note">인프라 비용: 20% 절감 (세밀한 스케일링)</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">서비스 경계 결정이 가장 중요 (DDD 필수)</div>
<div class="kb-diagram-note">공유 DB 문제: 서비스마다 DB 분리가 핵심 난제</div>
<div class="kb-diagram-note">분산 트랜잭션: Saga 패턴으로 해결</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 이커머스 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환은 대형마트 → 전문점 거리 — 모든 것 파는 대형마트(모놀리스)를 식료품점·전자제품점·의류점([마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/))으로 분리. 각 점포가 독립적으로 영업!

---

## 📌 관련 개념 맵

```
Re-architect / MSA
+-- 설계 원칙
|   +-- DDD 바운디드 컨텍스트
|   +-- Two-Pizza Team
|   +-- 독립 배포, 분산 데이터
+-- 전환 전략
|   +-- Strangler Fig Pattern (점진적)
|   +-- 6R (Rehost~Re-architect)
+-- 패턴
|   +-- Circuit Breaker, Service Mesh
|   +-- Saga, API Gateway
+-- 인프라
|   +-- Kubernetes, 컨테이너
|   +-- Istio Service Mesh
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[SOA (2000s)]
서비스 지향 아키텍처 (무거운 ESB)
      |
      v
[MSA 개념화 (2014)]
Martin Fowler/James Lewis 명문화
Netflix, Amazon 사례 공개
      |
      v
[컨테이너 + 쿠버네티스 (2015~)]
Docker + K8s: MSA 인프라 표준
Service Mesh (Istio) 등장
      |
      v
[클라우드 네이티브 패턴 (2018~)]
CNCF: 표준 패턴 정립
Circuit Breaker, Saga 표준화
      |
      v
[현재: 서버리스 MSA]
Lambda Function as a Service
이벤트 드리븐 MSA 아키텍처
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. MSA는 대형마트 → 전문점 거리 전환 — 하나의 큰 가게(모놀리스) 대신, 각 물건별 전문점([마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/))으로 분리해서 각자 독립 운영해요!
2. Strangler Fig는 점진적 집 수리 — 한꺼번에 헐고 짓는 대신(Big Bang), 사람이 살면서 방 하나씩 리모델링. 훨씬 안전해요.
3. Circuit Breaker는 전기 차단기 — [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 하나가 망가졌을 때 전체로 퍼지지 않도록 "뚝!" 차단해서 시스템을 보호해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 43 / 371

← **이전**: [043. Re-platform — 클라우드 관리형 서비스 전환](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/043_replatform_cloud_managed_services/)
**다음**: [045. 클라우드 이전 전략 — Repurchase & SaaS Migration](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/045_migration_repurchase_saas/) →

---
