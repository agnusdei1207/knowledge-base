---
title: "글로벌 CDN 아키텍처 (Global CDN Architecture)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 134
---

# 📖 【암기용】 개념 완전 이해

> 목적: 글로벌 CDN을 단순 캐시가 아니라 사용자 위치·콘텐츠 정책·오리진 보호가 결합된 분산 전달 구조로 이해하게 만든다.

## 한눈에
- **개요**: 전 세계 edge에서 콘텐츠를 캐시·전달하는 분산 아키텍처
- **왜 필요한가**: 사용자가 오리진 서버와 멀수록 RTT와 전송 지연이 증가한다. CDN은 가까운 POP에서 정적·동적 콘텐츠를 처리해 오리진 부하와 지연을 낮춘다.
- **핵심 직관**: 본사 창고 하나에서 전 세계로 배송하지 않고, 지역 물류센터에 재고를 배치해 현지에서 출고하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 대규모 웹·영상·게임 패치 서비스는 트래픽 피크가 지역별로 다르다. 오리진 직접 제공은 대역폭 비용과 장애 영향 범위가 커진다.
- **작동 원리**: DNS 또는 Anycast가 사용자를 가까운 edge로 유도한다. edge는 cache key와 TTL 정책으로 hit/miss를 판단하고 miss일 때 shield 또는 origin에서 가져온다.
- **비유**: 서점 본사가 모든 주문을 처리하지 않고, 지역 지점이 인기 도서를 보관해 바로 판매하는 방식이다.
- **구체 예시**: 이미지·JS·CSS는 `Cache-Control: max-age=31536000, immutable`로 장기 캐시하고, HTML은 TTL 60초와 purge API로 변경 반영을 통제한다.
- **흔한 오해·주의점**: CDN은 캐시 hit ratio만 높이면 끝나는 구조가 아니다. 개인화 응답, 쿠키, Authorization header는 cache key와 보안 정책을 분리해야 한다.

## 연결 개념
- DNS GSLB / Anycast — 사용자 요청을 edge로 유도하는 방식
- Cache-Control / CDN-Cache-Control — 캐시 정책을 제어하는 헤더
- Origin Shield — 다중 edge miss를 상위 캐시에서 흡수하는 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: CDN 답안은 edge 캐시 구조, 라우팅 방식, purge·보안·관측 지표를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Global CDN은 사용자 근접 edge POP에서 콘텐츠를 캐시·전달하고 오리진을 보호하는 분산 네트워크 아키텍처이다.
> 2. **가치**: cache hit ratio, origin offload, p95 TTFB, egress cost를 지표로 전송 품질과 비용을 통제한다.
> 3. **판단 포인트**: 정적/동적 콘텐츠 분리, cache key 설계, purge 전략, WAF/DDoS 연계가 설계 품질을 결정한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CDN 아키텍처 이해 확인 | Edge POP, GSLB/Anycast, cache hit/miss, origin shield | CDN을 단순 프록시로 설명 |
| 운영 설계 역량 확인 | TTL, purge, cache key, stale-if-error | 캐시 무효화와 개인화 누락 |
| 보안·비용 통제 확인 | WAF, DDoS, TLS, origin offload | hit ratio만 쓰고 보안·비용 미언급 |

> 요약: 출제자는 CDN을 분산 캐시와 오리진 보호 구조로 보고 정책·지표 기반 운영 역량을 확인한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **글로벌 CDN 아키텍처** | 글로벌 CDN 아키텍처 (Global CDN Architecture)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: 전 세계 edge 전달망
- 배경: 글로벌 사용자는 오리진과 RTT가 달라 p95 TTFB와 대역폭 비용 편차가 커짐
- 필요성: cache hit ratio 80% 이상, origin offload, DDoS 흡수로 서비스 지연과 장애 범위 통제
- 판단 기준: hit ratio, miss penalty, purge propagation time, origin egress cost로 검증

---

## Ⅱ. 구조 및 구성요소

```text
User -> DNS GSLB / Anycast -> Edge POP -> Cache lookup
                                  +-> Origin Shield -> Origin
                                  +-> WAF / Bot / TLS / Logs
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Edge POP | 사용자 근접 캐시와 TLS 종료 | 지역별 RTT·capacity 관리 |
| Routing | DNS GSLB 또는 Anycast로 POP 선택 | 장애 시 우회 정책 필요 |
| Cache Policy | TTL, cache key, bypass 조건 결정 | 쿠키·쿼리·헤더 처리 |
| Origin Shield | edge miss를 상위 캐시에서 흡수 | 오리진 연결 수 감소 |
| Security Layer | WAF, DDoS, bot, rate limit | 캐시 전후 적용 위치 구분 |

> 요약: CDN은 POP 라우팅, 캐시 정책, origin shield, 보안 계층이 결합된 분산 전달 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> POP 선택 -> cache key 산출 -> hit면 edge 응답
-> miss면 shield/origin fetch -> TTL 저장 -> 로그·지표 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DNS/Anycast로 가까운 POP 선택 | geo latency, routing failover |
| 2 | URL·쿼리·헤더로 cache key 산출 | key cardinality, bypass rate |
| 3 | hit이면 edge에서 응답 | cache hit ratio, edge TTFB |
| 4 | miss이면 shield 또는 origin에서 fetch | origin request rate, miss penalty |
| 5 | TTL·purge 정책과 로그 수집 | purge time, stale response count |

> 요약: CDN은 POP 선택, cache key 판단, hit/miss 처리, TTL·purge 운영 흐름으로 동작한다.

---

## Ⅳ. 특징

| 구분 | 오리진 직접 제공 | 글로벌 CDN | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 지연 | 사용자-오리진 RTT 의존 | 사용자-edge RTT 중심 | p95 TTFB, 지역별 RTT |
| 부하 | 오리진 요청 집중 | cache hit로 오리진 offload | hit ratio 80~95% 목표 |
| 장애 | 오리진 장애가 전역 영향 | stale-if-error, shield로 완충 | 5xx rate, stale count |
| 보안 | 오리진 노출 | WAF/DDoS edge 차단 | origin IP 보호, bot score |

> 요약: CDN은 지연 감소보다 캐시 정책, 오리진 보호, 보안 통제를 함께 설계해야 효과가 확인된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | Global CDN | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 리전 오리진 | 다중 POP edge | 글로벌 사용자 비율 30% 이상 |
| 비용/성능 | 클라우드 egress 집중 | CDN egress·request 과금 | origin egress 절감액과 CDN 비용 비교 |
| 운영/위험 | 배포 경로 단순 | TTL·purge·key 운영 복잡 | 배포 빈도와 purge SLA |

> 요약: CDN 적용은 글로벌 지연, 오리진 비용, 캐시 무효화 운영 부담을 함께 판단해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 캐시 | 개인화 응답 cache key 누락 | Authorization·Cookie bypass, private cache 금지 | cache poisoning incident |
| Purge 지연 | POP 전파 시간 편차 | versioned URL, soft purge, TTL 단축 | purge propagation p95 |
| 오리진 폭주 | 동시 miss·cache stampede | origin shield, request collapsing | origin RPS, 5xx rate |

> 요약: CDN 운영 리스크는 캐시 오염, purge 지연, 동시 miss 폭주로 나눠 대응한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 캐시 품질 | hit ratio 80~95%, bypass 사유 관리 | CDN analytics, response header |
| 사용자 지연 | p95 TTFB 지역별 SLA 충족 | RUM, synthetic monitoring |
| 오리진 보호 | origin RPS·egress 감소 | origin log, cloud billing |

> 요약: CDN 성공 여부는 hit ratio, p95 TTFB, origin offload를 동시에 만족하는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 정적 자산은 파일명 해시와 장기 TTL을 적용하고 HTML·API는 짧은 TTL 또는 bypass 정책을 분리한다.
2. Origin Shield와 request collapsing을 적용해 대규모 miss 상황에서 오리진 RPS를 제한한다.
3. WAF, bot 관리, TLS, access log를 edge에 배치하고 origin IP는 허용된 CDN 대역만 접근하게 한다.

**결론 (2줄):**
- 기술사 판단: 글로벌 트래픽과 정적 자산 비중이 높으면 CDN을 기본 적용하고, 개인화 API는 cache key와 bypass 조건을 먼저 검증한다.
- 향후 방향: CDN은 단순 캐시에서 edge compute, zero trust access, API protection이 결합된 edge platform으로 확장된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CDN 아키텍처를 설명하시오" | POP 선택과 hit/miss 흐름 | 오리진 직접 제공 대비 차이 |
| 요구사항 명시형 | "글로벌 서비스 가속 방안을 제시하시오" | cache key, TTL, purge 설계 | hit ratio, TTFB, origin offload |

> 요약: 설명형은 분산 캐시 구조를, 방안형은 캐시 정책과 운영 지표를 중심으로 전환한다.
