---
title: "MSA 분해 전략 — 도메인 주도 설계 (MSA Decomposition DDD)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 43
extra:
  question_no: "043"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- 서비스 분해는 기술 레이어가 아니라 도메인 경계를 기준으로 해야 함
- DDD는 bounded context와 ubiquitous language로 경계를 잡는 접근임
- 잘못 자른 서비스는 MSA 전체 비용을 키움

## Ⅰ. 개요

- **정의/개념**: MSA 분해 전략은 어떤 기준으로 시스템을 서비스 단위로 나눌지 결정하는 설계 활동이며, 도메인 주도 설계는 bounded context와 ubiquitous language를 활용해 비즈니스 의미 단위로 경계를 정의하는 대표 접근법임
- **배경/필요성**: 기능 목록이나 기술 계층 기준 분해는 서비스 간 결합을 오히려 키우기 쉬우므로, 변경 이유와 데이터 소유와 팀 책임이 일치하는 도메인 기준 분해가 필요함

## Ⅱ. 특징

- 서비스 경계가 비즈니스 책임과 함께 정의되어 변경 충돌을 줄임
- bounded context를 기준으로 데이터 소유와 언어를 분리함
- 분해 초기에 완벽한 정답을 얻기 어렵고 점진 조정이 필요함
- 조직 구조와 팀 책임 설계가 경계 품질에 직접 영향을 줌

## Ⅲ. 종류 및 비교

| 판단 기준 | 기술 계층 분해 | DDD 기반 분해 |
|:---|:---|:---|
| 경계 기준 | UI, API, DB 같은 기술 층 | 비즈니스 능력과 도메인 의미 |
| 장점 | 시작이 쉬움 | 변경 이유와 책임 정렬 우수 |
| 한계 | 서비스 간 결합 심화 가능 | 분석과 도메인 이해 비용 필요 |
| 적합 환경 | 단순 초기 분리 | 장기 운영형 복합 도메인 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Bounded Context | 동일한 용어와 규칙이 유효한 경계를 정의해 서비스 분해 기준이 됨 |
| Ubiquitous Language | 도메인 언어를 통일해 팀 간 해석 차이를 줄이고 계약 설계를 안정화함 |
| Domain Event | 경계 사이 상태 변화를 이벤트로 표현해 결합도를 낮추는 수단이 됨 |
| Context Map | 컨텍스트 간 관계와 통합 방식을 나타내 서비스 간 의존 구조를 가시화함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 도메인 탐색      | --> | 컨텍스트 정의  | --> | 데이터/계약 분리 | --> | 경계 검증/조정 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **도메인 탐색**: 핵심 업무 흐름과 용어와 규칙을 식별함
2. **컨텍스트 정의**: bounded context 단위로 경계를 설정함
3. **데이터와 계약 분리**: 소유 데이터와 API와 이벤트를 구분함
4. **경계 검증 및 조정**: 변경 빈도와 호출 관계를 보며 경계를 보정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 기술 계층 기준으로 서비스를 자르면 실제 변경 이유가 달라 서비스 간 조정 비용이 커질 수 있음
   - 해결방안: 도메인 이벤트와 변경 원인을 기준으로 경계를 재설계하고 deployment coupling rate와 change overlap ratio로 검증함
2. 문제: bounded context가 모호하면 같은 데이터 의미가 서비스마다 달라져 통합 결함이 늘 수 있음
   - 해결방안: ubiquitous language와 context map을 운영하고 terminology conflict count와 integration defect rate로 검증함
3. 문제: 조직 책임과 서비스 경계가 어긋나면 경계가 유지되지 않고 무단 의존성이 쌓일 수 있음
   - 해결방안: team ownership alignment를 맞추고 ownership clarity score와 cross-team dependency lead time으로 검증함

## Ⅶ. 적용 사례

- 주문·결제·배송 도메인 분리에서는 bounded context를 사용하고, change overlap ratio와 deployment coupling rate로 결과를 확인함
- 대형 플랫폼 조직에서는 context map을 유지하고, terminology conflict count와 integration defect rate로 결과를 확인함
- 제품 조직 재편 시에는 서비스와 팀 책임을 함께 조정하고, ownership clarity score와 cross-team dependency lead time로 결과를 확인함

## Ⅷ. 결론

MSA 분해 전략의 성패는 서비스를 몇 개로 나누느냐보다 변경 이유와 데이터 소유와 팀 책임이 같은 경계 위에 놓이는가에 달림.
