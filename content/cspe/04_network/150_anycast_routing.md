---
title: "애니캐스트 라우팅 (Anycast Routing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 150
---

# 📖 【암기용】 개념 완전 이해

> 목적: 애니캐스트를 로드밸런서 용어가 아니라 같은 IP 주소를 여러 위치에서 광고해 가장 가까운 지점으로 보내는 라우팅 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 동일한 IP prefix를 여러 사이트에서 광고하고 라우팅이 선택한 가까운 사이트로 트래픽을 전달하는 방식
- **왜 필요한가**: DNS, CDN, DDoS 흡수, 글로벌 API는 사용자 위치와 장애 상황에 따라 가까운 서비스 지점으로 연결되어야 한다.
- **핵심 직관**: 같은 프랜차이즈 번호로 전화해도 사용자의 위치에 가까운 지점으로 연결되는 구조와 같다.

## 깊이 이해
- **배경·문제의식**: 단일 서버 IP는 지리적 지연, 장애 영향 범위, DDoS 집중 공격 문제가 발생한다.
- **작동 원리**: 여러 PoP가 같은 prefix를 BGP로 광고하고, 인터넷 라우터는 AS path, local preference, MED 등 정책에 따라 하나의 경로를 선택한다.
- **비유**: 여러 응급실이 같은 대표 번호를 공유하고, 네트워크가 호출자를 가까운 응급실로 보내는 방식이다.
- **구체 예시**: 공용 DNS 서비스는 동일한 Anycast IP를 전 세계 PoP에서 BGP로 광고해 사용자를 인접 PoP로 유도한다.
- **흔한 오해·주의점**: 애니캐스트는 세션 단위 상태 동기화를 자동 제공하지 않으므로 TCP 장기 세션보다 DNS, UDP, stateless API에 적합하다.

## 연결 개념
- BGP - Anycast prefix를 여러 위치에서 광고하는 라우팅 프로토콜
- CDN - 사용자 인접 PoP로 콘텐츠 요청을 분산
- DDoS Mitigation - 공격 트래픽을 여러 스크러빙 센터로 분산

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Anycast 답안은 동일 prefix 광고, BGP 경로 선택, 장애 수렴, 세션 상태 한계를 분리해 작성한다.
> 핵심: 출제자는 Anycast를 DNS 수준 분산과 구분하고 라우팅 정책 기반 분산 구조로 설명하는지 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Anycast Routing은 동일 IP prefix를 여러 노드가 광고하고 라우팅 경로 선택으로 가까운 노드에 트래픽을 전달하는 방식이다.
> 2. **가치**: DNS, CDN, DDoS 방어, 글로벌 서비스에서 지연, 장애 범위, 공격 집중을 라우팅 계층에서 분산한다.
> 3. **판단 포인트**: BGP 광고 범위, route health, prefix withdrawal, 세션 지속성, 관측 지표를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Anycast 원리 확인 | 동일 prefix, 다중 PoP, BGP path selection | DNS 라운드로빈과 같은 방식으로 설명 |
| 적용 분야 판단 확인 | DNS, CDN, DDoS scrubbing, stateless service | 상태ful TCP 서비스에 무조건 적용한다고 단정 |
| 운영 리스크 확인 | route flap, blackhole, 세션 이동, 관측성 | 장애 시 prefix withdrawal과 health check 누락 |

> 요약: Anycast 문제는 같은 IP를 여러 위치에서 광고하고 BGP 정책으로 사용자 경로를 나누는 원리를 써야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 동일 IP를 여러 위치에서 광고
- 배경: 단일 서비스 IP는 지리적 지연, 장애 집중, DDoS 트래픽 집중의 위험이 큼.
- 필요성: DNS, CDN, 글로벌 API, 스크러빙 센터를 사용자 인접 PoP로 유도하고 장애 시 광고 철회로 우회해야 함.
- 판단 기준: BGP 정책, PoP 헬스체크, prefix withdrawal 시간, 세션 특성, 트래픽 관측성을 기준으로 설계함.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Internet Routing -> Anycast Prefix
                         -> PoP A / PoP B / PoP C
                         -> Health Check -> BGP Advertise / Withdraw
                         -> Service Instance
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Anycast Prefix | 여러 위치에서 동일하게 광고되는 IP 대역 | DNS, CDN, scrubbing VIP |
| PoP | 지역별 서비스 거점 | 동일 서비스와 라우팅 정책 운영 |
| BGP Router | prefix 광고와 철회 수행 | AS path, local preference, community |
| Health Check | 서비스 상태에 따른 광고 제어 | 실패 시 withdraw 또는 de-preference |

> 요약: Anycast는 여러 PoP가 같은 prefix를 광고하고 BGP와 헬스체크가 트래픽 유입 위치를 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
PoP별 동일 prefix 광고 -> 인터넷 BGP 경로 계산
-> 사용자가 선택 경로로 접속 -> PoP 서비스 처리
-> 장애 감지 -> prefix withdraw / de-preference -> 경로 재수렴
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 여러 PoP가 동일 Anycast prefix를 BGP로 광고 | route visibility |
| 2 | 인터넷 라우터가 정책과 경로 속성으로 최적 경로를 선택 | AS path, local preference |
| 3 | 사용자는 선택된 PoP의 서비스 인스턴스에 접속 | RTT, PoP hit ratio |
| 4 | 헬스체크가 PoP 또는 서비스 장애를 탐지 | health check failure |
| 5 | 장애 PoP는 prefix를 철회하거나 선호도를 낮춤 | convergence time, blackhole count |

> 요약: Anycast는 BGP 광고와 철회가 서비스 인입 경로를 바꾸며, 수렴 시간과 blackhole 여부가 운영 품질을 좌우한다.

---

## Ⅳ. 특징

| 구분 | Unicast/Geo DNS | BGP Anycast | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 경로 선택 | 단일 IP 또는 DNS 응답 | 라우팅 경로 선택 | BGP path selection |
| 장애 대응 | DNS TTL 영향 | prefix withdraw 후 재수렴 | convergence time |
| 적용 서비스 | 상태ful 서비스 가능 | stateless, DNS, CDN, UDP에 적합 | DNS 53/UDP, CDN edge |
| 운영 위험 | 지역 장애 직접 영향 | route flap, blackhole, 세션 이동 | BGP monitor, RPKI |

> 요약: Anycast는 라우팅 계층 분산에 유리하지만 세션 상태와 BGP 수렴 특성을 고려해 서비스 유형을 선택해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DNS LB, GSLB | BGP Anycast | DNS, CDN, DDoS처럼 지리 분산이 필요한 서비스에 적용 |
| 비용/성능 | 중앙 서비스 또는 DNS TTL 의존 | 다중 PoP와 BGP 운영 필요 | PoP 수, RTT, 수렴 시간으로 판단 |
| 운영/위험 | 애플리케이션 LB 중심 | 라우팅 정책과 서비스 헬스 연동 | NOC의 BGP 운영 역량 필요 |

> 요약: Anycast는 전 세계 사용자 경로 분산에 적합하지만 BGP 정책과 서비스 헬스체크 자동화가 전제이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Blackhole | 장애 서비스가 prefix를 계속 광고 | 헬스체크 기반 withdraw | blackhole event count |
| Route flap | 잦은 광고·철회 | dampening, 안정화 타이머, staged withdraw | flap count |
| 세션 단절 | 경로 변경으로 PoP가 바뀜 | stateless 설계, 세션 복제, DNS/TCP 적용 범위 제한 | session reset rate |

> 요약: Anycast 운영 리스크는 blackhole, route flap, 세션 단절이며 헬스체크와 서비스 특성 설계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 경로 가시성 | 주요 ISP에서 prefix 관측 | route collector, RIPE RIS |
| 사용자 품질 | RTT와 PoP hit ratio 추적 | synthetic monitoring, RUM |
| 장애 수렴 | withdraw 후 경로 전환 시간 측정 | BGP log, active probe |

> 요약: Anycast 도입 후에는 경로 가시성, 사용자 지연, 장애 수렴 시간을 같은 대시보드에서 관리해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. DNS, CDN, DDoS scrubbing처럼 stateless 또는 짧은 세션 서비스를 우선 Anycast 대상으로 선정함.
2. PoP별 헬스체크와 BGP advertise/withdraw 자동화를 구성하고 route collector로 외부 가시성을 확인함.
3. RPKI, prefix filter, BGP community 정책을 적용해 잘못된 광고와 우회 경로를 통제함.

**결론 (2줄):**
- 기술사 판단: 글로벌 분산과 장애 흡수가 필요하면 Anycast를 선택하고, 긴 상태ful 세션은 GSLB·L7 LB와 병행 검토함.
- 향후 방향: Anycast는 CDN, DNS, Edge Cloud, DDoS 스크러빙의 기본 라우팅 패턴으로 유지되며 관측성과 자동 철회 체계가 핵심이 됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Anycast를 설명하시오" | BGP 광고와 경로 선택 흐름 | Unicast, Geo DNS 대비 특징 |
| 요구사항 명시형 | "글로벌 서비스 설계 방안을 제시하시오" | 장애 감지와 prefix withdrawal 흐름 | 세션 한계, blackhole, route flap 대응 |

> 요약: 설명형은 라우팅 원리를, 설계형은 BGP 헬스체크·수렴·세션 특성 중심으로 목차를 전환한다.
