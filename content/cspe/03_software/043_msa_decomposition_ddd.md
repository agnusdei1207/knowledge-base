---
title: "MSA 분해 전략 (MSA Decomposition DDD)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 43
---

## Ⅰ. 개요
- **정의**: DDD의 Bounded Context를 기준으로 모놀리스를 마이크로서비스 단위로 분해하는 전략
- **배경/필요성**: 기술 계층이 아닌 비즈니스 도메인 기준 분해가 서비스 응집도와 독립 배포성을 높임
- **비유**: 백과사전을 주제별 분책으로 나누어 각 권을 독립 편집·출판하는 것

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 서비스 경계 설정 근거 | Bounded Context와 Aggregate 관계 | 단순 기능 분할과 도메인 분해 혼동 금지 |

> 요약: DDD의 전략적 설계를 활용하여 서비스 경계를 도메인 기준으로 도출하는 방법론임

## Ⅱ. 구성요소
```text
Domain
  +-- Subdomain A (Core)
  |     +-- Bounded Context A-1
  |           +-- Aggregate --> Service A
  +-- Subdomain B (Supporting)
  |     +-- Bounded Context B-1
  |           +-- Aggregate --> Service B
  +-- Subdomain C (Generic)
        +-- Bounded Context C-1
              +-- Aggregate --> Service C
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Bounded Context | 동일 용어가 일관된 의미를 갖는 모델 경계이며 서비스 경계의 후보임 | 부서별 업무 용어 사전 |
| Aggregate | 데이터 일관성을 보장하는 트랜잭션 경계 단위임 | 주문서 1장 묶음 |
| Context Map | Bounded Context 간 관계(공유·준수·분리)를 시각화한 지도임 | 부서 간 협업 계약서 |

> 요약: Bounded Context가 서비스 경계, Aggregate가 트랜잭션 경계, Context Map이 관계를 정의함

## Ⅲ. 절차
```text
도메인 이벤트 도출 --> Bounded Context 식별 --> Context Map 작성 --> 서비스 분리
```
- 1단계: 이벤트 스토밍으로 도메인 이벤트·커맨드·액터를 도출함
- 2단계: 관련 이벤트를 그룹핑하여 Bounded Context 경계를 식별함
- 3단계: Context Map으로 컨텍스트 간 관계(ACL·OHS·Shared Kernel)를 정의함
- 4단계: Bounded Context 단위로 서비스를 분리하고 API 계약을 확정함

> 요약: 이벤트 스토밍 → 컨텍스트 식별 → 관계 정의 → 서비스 분리의 4단계로 진행함

## Ⅳ. 문제점
- 경계 오판: 컨텍스트 경계를 잘못 설정 — 서비스 간 과도한 동기 호출이 발생하여 결합도가 높아짐
- 공유 데이터: 여러 컨텍스트가 동일 엔티티 참조 — 데이터 중복·불일치가 발생함
- 도메인 지식 부족: 개발팀의 업무 이해 부족 — 기술 계층 기준 분해로 회귀함

> 요약: 경계 오판·공유 데이터·도메인 지식 부족이 분해 전략의 실패 원인임

## Ⅴ. 개선방안
1. 단기: 이벤트 스토밍 워크숍에 도메인 전문가를 참여시켜 경계 오판을 방지함
2. 중기: Anti-Corruption Layer를 도입하여 컨텍스트 간 공유 데이터 의존을 격리함
3. 장기: 도메인 전문가-개발자 협업 문화를 정착시켜 유비쿼터스 언어 기반 설계를 지속함

> 요약: 도메인 전문가 참여·ACL 도입·협업 문화 정착으로 분해 품질을 확보함

## Ⅵ. 전망
- 발전 방향: AI 기반 코드 분석 도구가 모놀리스의 도메인 경계를 자동 추천하는 방향으로 발전함
- 기술사적 판단: 분해 전략의 성패는 기술 역량보다 도메인 모델링 역량에 달려 있음
- 기술사 제언: 점진적 분해(Strangler Fig)와 병행하여 분해 단위를 검증하며 전환할 필요
