---
title: "마이크로서비스 아키텍처 (Microservice Architecture, MSA)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 42
---

## 핵심 인사이트 (3줄 요약)
- 단일 거대 애플리케이션(Monolith)을 독립적으로 배포 가능한 작은 비즈니스 도메인 단위의 서비스들로 잘게 쪼갠 아키텍처.
- 각 서비스는 자신만의 독립적인 데이터베이스(Database per Service)를 가지며, 가벼운 통신 방식(REST API, 메시지 큐)으로 서로 협력함.
- 개발 속도와 확장성을 비약적으로 높여주지만, 분산 트랜잭션과 데이터 정합성 유지라는 막대한 기술적 복잡도(Trade-off)를 수반함.
---
## Ⅰ. 개요 및 필요성
- **개요**: 클라우드 네이티브(Cloud Native) 환경의 핵심 설계 철학으로, 단일 책임 원칙(SRP)에 따라 비즈니스 역량별로 분리된 서비스들의 조합.
- **필요성**: 기존 모놀리식 구조에서는 코드 한 줄을 수정해도 전체 시스템을 빌드/테스트/배포해야 하므로 타임투마켓(Time to Market)이 극도로 느림. 대규모 트래픽 환경에서 특정 기능(예: 주문)만 스케일 아웃(Scale-out)하기 위해 서비스 분리가 필수적임.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **MSA의 4대 핵심 원칙**:
  1. **독립적 배포성(Independent Deployability)**: 타 서비스 변경 없이 언제든 배포 가능해야 함.
  2. **비즈니스 도메인 중심(Domain-driven)**: 기술 레이어가 아닌 비즈니스 기능(결제, 배송 등) 단위로 분리.
  3. **데이터 격리(Database per Service)**: 타 서비스의 DB에 직접 접근 불가(API를 통해서만 접근).
  4. **탈중앙화된 거버넌스(Decentralized Governance)**: 서비스별로 최적의 언어와 프레임워크 선택(Polyglot).

```text
[ 모놀리식 vs MSA 데이터 아키텍처 ]

    (Monolithic)                      (Microservices)
 [ Order + Payment ]           [ Order Service ]   [ Payment Service ]
          |                            |                   |
          v                            v                   v
 [ Single Database ]           [ Order DB ]        [ Payment DB ]
                                     ^                   ^
                                     |___( API 통신 )____|
```
---
## Ⅲ. 비교 및 연결
| 특성 | Monolithic Architecture | Microservice Architecture (MSA) |
|---|---|---|
| **배포 단위** | 전체 시스템 통합 배포 (WAR/EAR) | 서비스별 독립 배포 (Container/Pod) |
| **장애 격리** | 하나의 버그가 전체 시스템 다운 유발 | 특정 서비스 장애가 전체로 전파되지 않음 |
| **데이터 정합성** | DB 레벨의 트랜잭션(ACID) 보장 | 분산 트랜잭션(Saga, Eventual Consistency) |
| **테스트/모니터링**| 상대적으로 단순함 | 서비스 간 추적(Zipkin 등) 및 모니터링 복잡 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **MSA 안티 패턴(분산 모놀리스)**: 서비스를 쪼개 놓았으나, 서로 API로 강결합(Synchronous Call)되어 있어 하나가 죽으면 다 같이 죽고 배포도 동시에 해야 하는 최악의 상태(Distributed Monolith)를 가장 경계해야 함.
- **도입의 전제 조건**: 마틴 파울러가 지적했듯, CI/CD 파이프라인 자동화, 컨테이너 오케스트레이션(Kubernetes), 통합 모니터링 체계가 없는 상태에서 MSA를 도입하는 것은 재앙에 가까움.
---
## Ⅴ. 기대효과 및 결론
- MSA는 조직의 구조가 소프트웨어 아키텍처에 반영된다는 '콘웨이의 법칙(Conway's Law)'을 실현하여, 두 판의 피자로 식사할 수 있는 작은 팀(Two-Pizza Team)의 자율성과 기민성을 극대화함.
- 은통알(Silver Bullet)이 아니며, 초기 스타트업은 모놀리식으로 시작하여 비즈니스가 입증되고 한계에 부딪혔을 때 MSA로 전환(Strangler Fig Pattern)하는 진화적 접근이 바람직함.
---
### 📌 관련 개념 맵
- 클라우드 네이티브 ➡️ MSA ➡️ Bounded Context (DDD) ➡️ API Gateway / Service Mesh

### 📈 관련 키워드 및 발전 흐름도
- Monolithic ➡️ SOA (ESB 중심) ➡️ MSA (Smart Endpoints, Dumb Pipes) ➡️ Serverless/FaaS

### 👶 어린이를 위한 3줄 비유 설명
1. 거대한 스위스 아미 나이프(모놀리스)는 칼, 가위, 드라이버가 다 붙어있어서 하나만 고장 나도 전체를 수리 맡겨야 해요.
2. MSA는 칼, 가위, 드라이버를 각각 따로 분리해서 필통에 넣어두는 거예요.
3. 가위가 고장 나면 가위만 버리고 새로 사면 되니까 훨씬 편하고, 친구에게 가위만 빌려주기도 쉽답니다!
