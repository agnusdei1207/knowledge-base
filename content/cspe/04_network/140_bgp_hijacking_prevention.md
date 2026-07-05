---
title: "BGP 하이재킹 방지 (BGP Hijacking Prevention)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 140
---

# 📖 【암기용】 개념 완전 이해

> 목적: BGP 하이재킹을 공격 원리, 예방 통제, 탐지·대응 지표로 나눠 이해하게 만든다.

## 한눈에
- **개요**: 잘못된 BGP prefix 광고로 트래픽을 탈취·우회·블랙홀시키는 공격과 그 대응
- **왜 필요한가**: BGP는 전 세계 AS가 경로를 교환하는 기반이다. 잘못된 prefix 또는 more-specific prefix가 전파되면 정상 트래픽이 공격자·오광고 AS로 향한다.
- **핵심 직관**: 도로 표지판을 누군가 바꿔 목적지 차량을 엉뚱한 출구로 보내는 문제이며, 표지판 권한 확인과 실시간 감시가 필요하다.

## 깊이 이해
- **배경·문제의식**: BGP는 분산 신뢰 모델이라 prefix 소유권과 AS_PATH 정책 위반을 기본적으로 강제 검증하지 않는다. 운영 실수와 악의적 광고가 모두 사고가 된다.
- **작동 원리**: 공격자는 victim prefix와 같거나 더 구체적인 prefix를 광고한다. 인터넷 라우터는 longest prefix match와 BGP path selection에 따라 잘못된 경로를 선택할 수 있다.
- **비유**: 같은 주소를 더 자세히 적은 가짜 안내문이 배포되면 배달원이 그 안내문을 우선 믿고 다른 장소로 이동하는 상황이다.
- **구체 예시**: 피해자가 `/23`을 광고하고 공격자가 같은 주소의 `/24`를 광고하면 longest prefix match로 일부 트래픽이 공격자 AS로 이동할 수 있다.
- **흔한 오해·주의점**: RPKI만 적용하면 모든 BGP 하이재킹이 사라지는 것은 아니다. origin 검증, prefix filter, max-prefix, route leak 탐지, 외부 모니터링을 함께 운영해야 한다.

## 연결 개념
- RPKI ROV — prefix-origin AS 검증
- Route Leak — 의도 범위를 벗어난 경로 전파
- IRR Filtering / MANRS — 운영자 간 라우팅 보안 모범 조치

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: BGP 하이재킹 방지는 공격 원리, 예방 통제, 탐지·대응, 운영 지표를 분리해 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BGP hijacking은 권한 없는 AS가 victim prefix 또는 more-specific prefix를 광고해 트래픽 경로를 탈취하는 라우팅 공격이다.
> 2. **가치**: RPKI ROV, prefix filter, max-prefix, route monitoring으로 오광고 전파와 피해 시간을 줄인다.
> 3. **판단 포인트**: origin validation, route leak 탐지, upstream 필터링, MTTR, affected prefix count를 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공격 원리 이해 확인 | prefix hijack, more-specific hijack, route leak | BGP 암호화 문제로만 설명 |
| 검증·예방 체계 확인 | RPKI ROA/ROV, IRR filter, max-prefix | RPKI만으로 전체 해결 단정 |
| 운영 대응 판단 확인 | 모니터링, upstream 연락, withdrawal, postmortem | 탐지 지표와 복구 절차 누락 |

> 요약: 출제자는 하이재킹의 경로 선택 원리와 다층 통제·운영 대응을 함께 보길 요구한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **라우팅** | 패킷을 목적지까지 최적 경로로 전달하는 과정 | "내비게이션" |
| **라우팅 테이블** | 목적지별 다음 홉 정보를 저장하는 테이블 | "도로 안내 표지판" |
| **AS(자율 시스템)** | 단일 라우팅 정책으로 관리되는 네트워크 집합 | "한 나라" |

---

## Ⅰ. 개요 및 필요성

- 개요: BGP 경로 탈취 방지
- 배경: BGP는 prefix 광고 권한을 기본 강제하지 않아 오광고가 전 세계로 전파될 수 있음
- 필요성: RPKI, prefix filter, monitoring으로 hijack 전파와 트래픽 블랙홀 시간을 줄임
- 판단 기준: affected prefix count, invalid route count, detection time, mitigation MTTR로 검증

---

## Ⅱ. 구조 및 구성요소

```text
Victim Prefix / Attacker AS -> BGP Advertisement -> Upstream / IX
-> Global Routing Table -> Monitoring / RPKI / Prefix Filter -> Mitigation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 공격 광고 | 동일 prefix 또는 more-specific prefix 전파 | longest prefix match 악용 |
| RPKI ROV | prefix-origin AS 권한 검증 | Invalid route reject |
| Prefix Filter | 고객·피어별 허용 prefix 제한 | IRR/RPKI 데이터 활용 |
| Route Monitoring | 전 세계 경로 변화 탐지 | RIS, RouteViews, 상용 모니터링 |
| Mitigation | withdrawal, deaggregate, upstream 필터 요청 | 사고 대응 runbook 필요 |

> 요약: BGP 하이재킹 방지는 광고 경로, origin 검증, prefix 필터, 외부 모니터링, 대응 절차가 결합된 체계이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
공격자 prefix 광고 -> upstream 수신 -> best path 선택
-> 전파 확산 -> 모니터링 탐지 -> RPKI/filter 차단 -> 경로 회복
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격자 또는 오구성 AS가 victim prefix 광고 | unexpected origin AS 탐지 |
| 2 | upstream·peer가 필터 없이 경로 수용 | AS_PATH, prefix length 확인 |
| 3 | longest prefix match 또는 path selection으로 트래픽 이동 | affected ASN, traffic drop |
| 4 | RPKI/monitoring이 이상 경로 탐지 | invalid status, alert time |
| 5 | withdrawal·filter·upstream 조치로 경로 복구 | mitigation MTTR, route convergence |

> 요약: 하이재킹은 잘못된 광고 수용과 전파로 발생하며 탐지·차단·withdrawal로 정상 경로를 회복한다.

---

## Ⅳ. 특징

| 구분 | 무통제 BGP 운영 | 하이재킹 방지 운영 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 광고 검증 | peer 신뢰 중심 | RPKI ROV·IRR filter | invalid reject count |
| 경로 제한 | 고객 prefix 제한 부족 | prefix-list, max-prefix | allowed prefix coverage |
| 탐지 | 장애 신고 의존 | external route monitoring | detection time 5분 이하 |
| 대응 | 수동 연락 지연 | runbook·upstream NOC 절차 | mitigation MTTR |

> 요약: 하이재킹 방지는 사전 필터와 사후 모니터링을 함께 운영해야 피해 시간을 줄일 수 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 방지 체계 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 prefix-list | RPKI+IRR+monitoring | AS 운영 규모와 prefix 수 |
| 비용/성능 | 운영 부담 낮음 | validator·모니터링 비용 | hijack 피해 비용과 MTTR |
| 운영/위험 | 오탐 적음 | 잘못된 ROA·필터로 자기 차단 | change review와 rollback |

> 요약: 방지 체계는 필터 강도와 자기 차단 위험의 균형을 변경관리 절차로 맞춰야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| More-specific hijack | 공격자가 더 긴 prefix 광고 | ROA maxLength 제한, upstream filter | unexpected more-specific count |
| Route leak | 고객·피어 정책 위반 전파 | import/export policy, ASPA 검토 | leak alert, valley-free violation |
| 자기 차단 | 잘못된 ROA·prefix-list | staged rollout, pre-check | self-inflicted outage count |

> 요약: 공격·검증·운영 리스크를 분리해야 RPKI와 필터가 서비스 장애로 바뀌는 것을 막을 수 있다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 예방 | 자사 prefix ROA coverage 100% | RPKI validator, RIR portal |
| 탐지 | hijack alert 5분 이하 | RIPE RIS, RouteViews, BGP monitor |
| 복구 | mitigation MTTR 30분 이하 | incident timeline, NOC ticket |

> 요약: 하이재킹 대응 품질은 ROA 커버리지, 탐지 시간, 복구 시간으로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 자사 prefix 전체에 ROA를 생성하고 maxLength는 실제 deaggregation 계획과 일치하게 설정한다.
2. 고객·피어 세션에 IRR/RPKI 기반 prefix filter, max-prefix, AS-PATH filter를 적용한다.
3. 외부 BGP 모니터링과 NOC runbook을 구성해 unexpected origin AS 탐지 후 upstream에 차단 요청을 즉시 수행한다.

**결론 (2줄):**
- 기술사 판단: 인터넷 노출 AS는 RPKI ROV와 prefix filter를 기본 적용하고, critical prefix는 외부 경로 모니터링을 필수로 둔다.
- 향후 방향: BGP 보안은 RPKI origin validation에서 ASPA, BGPsec, route leak 자동 탐지로 확장된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "BGP 하이재킹을 설명하시오" | 공격 광고 전파와 경로 선택 흐름 | 무통제 BGP 대비 방지 체계 |
| 요구사항 명시형 | "라우팅 보안 대책을 제시하시오" | RPKI, filter, monitoring 대응 절차 | detection time, MTTR, ROA coverage |

> 요약: 설명형은 공격 원리를, 보안형은 예방·탐지·복구 지표를 중심으로 전환한다.
