---
title: "CDN 콘텐츠 전송 네트워크 (CDN Content Delivery Network)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 216
---

# 📖 【암기용】 개념 완전 이해

> 목적: CDN을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: CDN(콘텐츠 전송 네트워크)은 사용자와 물리적으로 가까운 **엣지(Edge) POP**에 콘텐츠를 미리 캐시해두는 **지리적 분산 캐싱(Geo-distributed Caching)** 네트워크로, 원본(origin) 서버의 부하와 전송 지연(RTT)을 함께 줄인다.
- **왜 필요한가**: 이미지·JS·동영상을 전 세계 사용자에게 모두 origin에서 직접 주면, 물리 거리가 먼 사용자일수록 지연이 늘고 origin의 대역폭 비용도 급증한다.
- **핵심 직관**: 본점 창고 대신 동네 물류 거점에 인기 상품을 미리 가져다 두는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Edge POP(Point of Presence) | 사용자와 가까운 지역에 배치된 캐시 서버 거점 | 동네 물류 거점 |
| Origin(오리진) 서버 | 콘텐츠가 최초로 보관된 원본 서버 | 본점 창고 |
| Origin Shield | 여러 edge의 miss를 한곳에 모아 origin으로 가는 요청을 줄이는 중간 집약 계층 | 지역 거점들이 한 광역 물류센터를 거쳐 본점에 요청 |
| Anycast | 동일한 IP 주소를 여러 지점에 배포해, 사용자를 네트워크상 가장 가까운 지점으로 자동 라우팅하는 기술 | 같은 대표번호로 걸어도 가장 가까운 지점이 응답 |
| Cache Key | 캐시된 객체를 구분하는 기준(URL, 쿼리, 헤더 조합) | 상품을 구분하는 바코드 |
| TTL(Time To Live) | edge에 저장된 캐시 객체의 유효 시간 | 진열 상품의 유통기한 |
| Purge(퍼지, 무효화) | 원본이 바뀌었을 때 edge 캐시를 강제로 지우는 동작 | 리콜 상품을 매장에서 즉시 회수 |
| RTT(Round Trip Time) | 요청을 보내고 응답을 받기까지의 왕복 지연 | 주문부터 배송까지 걸리는 왕복 시간 |
| Origin Offload(오리진 오프로드) | CDN이 대신 처리해서 origin이 받지 않아도 되는 트래픽의 비율 | 매장 판매량만큼 본점 배송이 줄어드는 비율 |

## 깊이 이해

### 왜 필요했나 (배경)
- 네트워크 지연은 물리 거리에 비례한다. 예를 들어 서울 사용자가 미국 동부 origin에 직접 접속하면 왕복(RTT)이 약 180ms 안팎으로, 국내 서버 접속(수 ms~수십 ms)보다 훨씬 느리다.
- 피크 이벤트(할인 행사, 신제품 출시)에는 origin 하나로 전 세계 트래픽을 받아내야 해 대역폭과 커넥션 수가 병목이 된다. 이 두 문제(거리·집중)를 동시에 푸는 것이 CDN이다.

### Hit/Miss 흐름을 수치로 이해하기
- 정적 이미지 트래픽이 하루 1TB라고 하자. CDN hit ratio가 95%라면, origin으로 실제 전달되는 트래픽은 50GB/day(1TB × 5%)로 줄어든다. hit ratio가 99%면 10GB/day까지 더 줄어든다.
- hit ratio 4%p 차이가 origin 트래픽을 5배 가른다. 그래서 CDN 운영에서는 hit ratio를 90% 이상으로 유지하는 것이 핵심 목표가 된다.

### Anycast가 가까운 POP을 고르는 원리
- 여러 지역의 POP이 동일한 IP를 광고(BGP)하면, 라우터는 네트워크 경로상 가장 가까운(홉 수가 적은) 경로로 패킷을 보낸다. 그 결과 서울 사용자는 자동으로 서울 또는 도쿄 POP으로 연결되고, 별도의 클라이언트 설정 없이 지리적으로 가까운 곳에서 응답을 받는다.

### Origin Shield로 miss 폭주를 줄이는 원리 - 수치 예제
- POP이 전 세계 50곳에 흩어져 있는데 Origin Shield 없이 운영하면, 같은 콘텐츠가 각 POP에서 독립적으로 miss가 나 origin이 최악의 경우 50번(POP 수만큼) 같은 파일을 받아야 한다.
- Origin Shield를 하나 두면 POP들의 miss를 그 Shield가 먼저 모아 자기 캐시를 채우고, origin에는 딱 1번만 요청한다. 즉 origin 요청 횟수가 50배에서 1배로 줄어든다.

### 비유와 흔한 오해
- **비유**: 전국 서점이 베스트셀러를 지역 매장에 미리 가져다 둬, 고객이 출판사 창고까지 가지 않게 하는 것과 같다.
- **오해**: "CDN은 정적 파일만 담당한다." 실제로는 API 응답 캐시, WAF, DDoS 트래픽 흡수, TLS 종료까지 edge에서 처리할 수 있다. 단, 이때는 사용자마다 다른 개인정보 응답을 캐시하지 않도록 cache key와 `Cache-Control: private/no-store` 설정을 반드시 구분해야 한다.

## 연결 개념
- 캐싱 전략 - TTL, invalidation, cache key 개념을 CDN도 그대로 공유
- 리버스 프록시 - CDN edge 자체가 origin 앞단에 놓인 대규모 분산 리버스 프록시
- 로드 밸런싱 - origin이 여러 대일 때 지역·상태 기반으로 origin을 선택하는 다음 단계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CDN 답안은 캐시 hit ratio, origin offload, 보안, 무효화 시간을 지표로 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CDN은 edge POP에 콘텐츠를 캐시하고 사용자 요청을 가까운 지점에서 처리하는 전송 아키텍처이다.
> 2. **가치**: RTT, origin 대역폭, DDoS 노출을 줄이고 글로벌 사용자 응답 p95를 낮춘다.
> 3. **판단 포인트**: 정적/동적 캐시 구분, cache key, TTL, purge, 보안 헤더, origin 보호를 함께 설계한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CDN 구조 이해 확인 | Edge POP, DNS/Anycast, cache hit/miss, origin shield | 단순 "가까운 서버"로만 설명 |
| 운영 설계 확인 | TTL, purge, cache key, stale-while-revalidate | 개인정보 응답 캐시 리스크 누락 |
| 성능·보안 판단 확인 | origin offload, WAF, TLS, DDoS 흡수 | hit ratio와 origin 부하 지표 누락 |

> 요약: CDN은 전송 거리 단축과 origin 보호를 캐시 정책·보안 정책으로 달성하는 구조이다.

---

## Ⅰ. 개요 및 필요성

- 개요: edge 기반 콘텐츠 전송망
- 배경: 글로벌 서비스는 RTT, 대역폭 비용, origin 집중 부하가 사용자 경험과 장애 가능성을 좌우한다.
- 필요성: 캐시 정책, TLS, WAF, DDoS 대응을 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> DNS/Anycast -> Edge POP
  / Cache Hit -> Response
  / Cache Miss -> Origin Shield -> Origin Server -> Edge Cache Fill
Edge -> WAF/TLS/Log -> Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Edge POP | 사용자 근접 캐시 응답 | 지역별 latency 차이 측정 |
| Origin Shield | edge miss를 집약해 origin 보호 | multi-CDN 구성 시 유용 |
| Cache Policy | TTL, key, header, cookie 제어 | 개인정보 응답 캐시 금지 |
| Security Layer | WAF, TLS, DDoS 흡수 | Bot 차단, rate rule 연계 |

> 요약: CDN 구조는 edge cache, origin 보호, 캐시 정책, 보안 계층으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> Edge Route -> Cache Key Build
  / Hit -> Return Object
  / Miss -> Fetch Origin -> Store with TTL -> Return
-> Purge/Expire -> Log and Metric Collect
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 위치 기반 edge 선택 | DNS TTL 60초, Anycast 경로 |
| 2 | cache key 생성 | path, query, header, cookie 정책 |
| 3 | hit/miss 처리와 origin fetch | hit ratio 90% 이상 |
| 4 | purge·만료·로그 수집 | purge p95 60초 이하 |

> 요약: CDN 동작은 edge 선택, cache key, hit/miss, purge 지연으로 검증한다.

---

## Ⅳ. 특징

| 구분 | Origin 직접 전송 | CDN 전송 | 판단 수치 |
|:---|:---|:---|:---|
| 지연 | 사용자-origin RTT 의존 | edge POP RTT로 단축 | 글로벌 p95 300ms 이하 목표 |
| 부하 | origin bandwidth 집중 | hit ratio만큼 offload | hit 95%면 origin 전송 1/20 |
| 보안 | origin IP 노출 가능 | WAF·DDoS edge 흡수 | origin allowlist, TLS 1.3 |
| 운영 | 배포 후 즉시 반영 | TTL·purge 지연 | purge p95 60초 이하 |

> 요약: CDN은 지연과 origin 부하를 줄이지만 cache key와 purge 지연을 통제해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | CDN | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Origin 단일 제공 | Edge POP + Origin Shield | 해외 트래픽 30% 이상 |
| 비용/성능 | origin bandwidth 과금 | edge 전송과 offload | hit ratio 80% 이상 가능 콘텐츠 |
| 운영/위험 | 즉시 반영 | stale·잘못된 캐시 | 개인정보·권한별 응답 cache bypass |

> 요약: CDN 적용은 지역 분산 트래픽과 캐시 가능한 응답 비율을 기준으로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 개인정보 캐시 | cookie 포함 응답 cache key 누락 | private/no-store, auth bypass | cache incident 0건 |
| Stale Content | TTL 과다, purge 지연 | versioned URL, purge API | purge p95 60초 이하 |
| Origin 과부하 | 동시 miss, purge 후 폭주 | origin shield, request coalescing | origin RPS spike |

> 요약: CDN 리스크는 잘못된 캐시, stale, origin 폭주이며 cache policy와 shield로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 캐시 효과 | hit ratio 90~95%, origin offload 80% 이상 | CDN analytics |
| 응답 지연 | edge p95 100ms, global p95 300ms 이하 | RUM, synthetic monitoring |
| 보안/운영 | WAF 차단 로그, origin allowlist 100% | SIEM, firewall rule audit |

> 요약: CDN 성공 여부는 hit ratio, 글로벌 지연, origin 보호 수준으로 판정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 정적 자산은 versioned URL과 TTL 1일 이상, HTML/API는 TTL 0~60초와 `Cache-Control` 분리 적용
2. Origin Shield, request coalescing, WAF, origin IP allowlist로 miss 폭주와 직접 접근을 차단
3. purge p95 60초 이하, hit ratio 90% 이상, origin bandwidth 80% 감소 목표를 운영 대시보드에 등록

**결론 (2줄):**
- 기술사 판단: 캐시 가능한 정적·반정적 콘텐츠와 글로벌 트래픽이 있으면 CDN, 사용자별 민감 응답은 cache bypass 적용
- 향후 방향: Edge Compute와 CDN이 결합되어 인증, A/B 테스트, 이미지 변환을 edge에서 수행하는 형태로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CDN을 설명하시오" | DNS/Anycast, hit/miss, purge 흐름 | Origin 직접 전송 대비 특징 |
| 요구사항 명시형 | "글로벌 서비스 전송 방안을 설계하시오" | cache key, origin shield, WAF 구성 | hit ratio·purge·보안 기준 |

> 요약: 설명형은 edge 전송 원리, 설계형은 캐시 정책과 origin 보호를 중심으로 답안을 전환한다.
