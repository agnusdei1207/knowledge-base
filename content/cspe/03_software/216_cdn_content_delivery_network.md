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
- **개요**: 사용자와 가까운 edge 서버에서 콘텐츠를 제공해 원본 서버 부하와 전송 지연을 줄이는 네트워크 계층
- **왜 필요한가**: 이미지, JS, 동영상, 다운로드 파일을 모두 origin에서 주면 지역별 지연과 대역폭 비용이 증가함
- **핵심 직관**: 본점 창고 대신 동네 물류 거점에 인기 상품을 미리 두는 구조임

## 깊이 이해
- **배경·문제의식**: 글로벌 사용자는 origin과 물리 거리가 멀수록 RTT가 증가한다. 피크 이벤트에는 origin bandwidth와 connection이 병목이 된다.
- **작동 원리**: DNS 또는 Anycast가 사용자를 edge POP으로 보낸다. edge는 캐시 hit이면 즉시 응답하고 miss이면 origin에서 가져와 TTL 동안 저장한다.
- **비유**: 전국 서점이 베스트셀러를 지역 매장에 보관해 고객이 출판사 창고까지 가지 않게 하는 방식임
- **구체 예시**: 정적 이미지 1TB/day 서비스에서 CDN hit ratio 95%면 origin 전송은 50GB/day로 감소한다.
- **흔한 오해·주의점**: CDN은 정적 파일만 담당하지 않는다. API cache, WAF, DDoS 흡수, TLS 종료도 가능하지만 캐시 키와 개인정보 응답을 구분해야 함

## 연결 개념
- 캐싱 전략 - TTL, invalidation, cache key
- 리버스 프록시 - origin 앞단의 요청 중계
- 로드 밸런싱 - 지역·상태 기반 origin 선택

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

CDN은 edge 서버에서 콘텐츠를 제공하는 전송 네트워크이다. 글로벌 서비스는 RTT, 대역폭 비용, origin 집중 부하가 사용자 경험과 장애 가능성을 좌우한다. CDN은 캐시와 보안 정책을 함께 설계해야 효과를 낸다.

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
