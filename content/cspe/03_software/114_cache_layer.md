---
title: "캐시 계층 — Redis·Memcached (Cache Layer)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 114
extra:
  question_no: "114"
  exam_status: "미출제"
  exam_note: "기본"
---

## 미리 알고가기

- 캐시 계층은 자주 조회되는 데이터를 메모리에 두어 응답 시간을 줄이는 구조임
- Redis와 Memcached는 대표적인 인메모리 캐시 도구임
- hit ratio보다 일관성 정책과 만료 전략이 운영 품질에 더 큰 영향을 줄 수 있음

## Ⅰ. 개요

- **정의/개념**: 캐시 계층은 데이터베이스나 외부 서비스에 반복적으로 접근하는 대신 자주 사용되는 결과를 메모리 기반 저장소에 임시 보관해 응답 지연과 백엔드 부하를 줄이는 성능 최적화 계층임
- **배경/필요성**: 트래픽 증가 시 모든 조회를 원본 저장소로 보내면 병목과 비용이 커지므로, 접근 빈도가 높은 데이터를 빠르게 재사용할 중간 계층이 필요함

## Ⅱ. 특징

- 읽기 응답 시간과 원본 부하를 크게 줄일 수 있음
- Redis는 자료구조와 영속화와 pub/sub 등 기능이 풍부함
- Memcached는 단순 key-value 캐시에 가볍고 빠름
- 만료와 갱신 정책이 잘못되면 stale data와 cache stampede가 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | Redis | Memcached |
|:---|:---|:---|
| 데이터 구조 | 문자열·리스트·셋 등 다양 | 단순 key-value |
| 강점 | 기능 풍부와 운영 유연성 | 단순성과 낮은 오버헤드 |
| 한계 | 기능 복잡성에 따른 운영 부담 | 기능 제한 |
| 적합 용도 | 세션·랭킹·분산락·캐시 | 단순 조회 캐시 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cache Key Design | 충돌 없는 키 설계가 재사용성과 무효화 정확도를 좌우함 |
| Expiration Policy | TTL과 무효화 규칙으로 데이터 신선도와 hit ratio 균형을 맞춤 |
| Fill Strategy | cache-aside나 write-through 같은 적재 방식이 일관성 특성을 결정함 |
| Protection Mechanism | stampede 방지와 fallback 정책이 장애 전파를 줄임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 수신      | --> | 캐시 조회      | --> | miss 시 원본 조회 | --> | 캐시 적재/만료  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 수신**: 애플리케이션이 데이터를 요청함
2. **캐시 조회**: key로 캐시 히트 여부를 확인함
3. **miss 시 원본 조회**: 원본 저장소에서 값을 읽음
4. **캐시 적재와 만료**: 결과를 저장하고 TTL을 관리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 캐시 키와 TTL을 경험적으로만 정하면 hit ratio는 높아도 stale data와 miss burst가 반복될 수 있음
   - 해결방안: key taxonomy와 ttl policy를 표준화하고 cache hit ratio와 stale read rate로 검증함
2. 문제: 인기 키 만료가 동시에 일어나면 원본 DB로 요청이 폭주해 전체 장애로 번질 수 있음
   - 해결방안: request coalescing과 jittered TTL을 적용하고 stampede incident count와 backend surge ratio로 검증함
3. 문제: 캐시 의존성이 커져도 장애 우회 경로가 없으면 캐시 장애가 곧 서비스 장애가 될 수 있음
   - 해결방안: fallback path와 degradation policy를 마련하고 cache failover success rate와 user-visible error rate로 검증함

## Ⅶ. 적용 사례

- 상품 조회 서비스에서는 키와 TTL 정책을 표준화하고, cache hit ratio와 stale read rate로 결과를 확인함
- 대형 이벤트 시스템에서는 stampede 방지 기법을 적용하고, stampede incident count와 backend surge ratio로 결과를 확인함
- SaaS 운영 플랫폼에서는 장애 우회 경로를 마련하고, cache failover success rate와 user-visible error rate로 결과를 확인함

## Ⅷ. 결론

캐시 계층의 성능 효과는 단순 메모리 적재보다 데이터 신선도와 장애 전파를 함께 통제하는 운영 정책에서 완성됨.
