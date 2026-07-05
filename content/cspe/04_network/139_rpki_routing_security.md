---
title: "RPKI 라우팅 보안 (RPKI Routing Security)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 139
---

# 📖 【암기용】 개념 완전 이해

> 목적: RPKI를 BGP 경로의 origin AS 검증 체계로 이해하게 만든다.

## 한눈에
- **개요**: IP prefix를 광고할 수 있는 AS를 인증하는 공개키 기반 라우팅 보안 체계
- **왜 필요한가**: BGP는 상대 AS가 특정 prefix를 광고할 권한이 있는지 기본적으로 검증하지 않는다. 잘못된 origin 광고는 트래픽 우회·블랙홀·중간자 공격으로 이어진다.
- **핵심 직관**: 인터넷 주소 블록 소유자가 "이 AS가 내 주소를 광고해도 된다"는 서명된 위임장을 만들어 라우터가 확인하는 구조이다.

## 깊이 이해
- **배경·문제의식**: BGP는 신뢰 기반 경로 교환 프로토콜이다. 악의적 또는 실수로 더 구체적인 prefix나 잘못된 origin AS가 광고되면 라우팅이 탈취될 수 있다.
- **작동 원리**: 주소 자원 보유자는 ROA에 prefix, maxLength, origin AS를 서명해 저장소에 게시한다. RPKI validator는 ROA를 검증해 VRP를 만들고, 라우터는 RTR로 받아 BGP 경로를 Valid/Invalid/NotFound로 분류한다.
- **비유**: 택배 구역을 맡은 대리점 목록을 본사가 서명해 배포하고, 물류센터가 배송 전 담당 대리점인지 확인하는 방식이다.
- **구체 예시**: `203.0.113.0/24, AS64500, maxLength 24` ROA가 있을 때 AS64501이 같은 prefix를 광고하면 origin validation 결과는 Invalid가 된다.
- **흔한 오해·주의점**: RPKI ROV는 origin AS 검증이다. AS_PATH 전체의 정책 위반이나 route leak 전체를 완전히 검증하지는 않는다.

## 연결 개념
- ROA / VRP — RPKI 검증 데이터와 라우터 입력 데이터
- BGP Origin Validation — Valid, Invalid, NotFound 분류
- BGPsec / ASPA — 경로 전체 검증과 route leak 대응 확장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: RPKI 답안은 공격 원리, ROA 검증 체계, 운영 지표를 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RPKI는 IP prefix 보유자가 origin AS 권한을 ROA로 서명하고 라우터가 BGP 경로 origin을 검증하는 체계이다.
> 2. **가치**: RFC 6482 ROA와 RFC 6811 origin validation으로 prefix hijack과 잘못된 origin 광고를 줄인다.
> 3. **판단 포인트**: ROA coverage, invalid reject policy, validator availability, NotFound route 처리 기준을 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 라우팅 공격 원리 확인 | 잘못된 origin AS, more-specific hijack | 암호화 통신 기술로 오해 |
| 검증 체계 이해 확인 | ROA, VRP, validator, RTR, Valid/Invalid/NotFound | ROA와 BGP route 직접 비교 누락 |
| 운영 정책 판단 확인 | invalid reject, maxLength 관리, validator 이중화 | Invalid 전체 차단만 단정 |

> 요약: 출제자는 RPKI를 BGP origin 검증 체계로 보고 공격 원리와 운영 정책을 분리하길 요구한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **라우팅** | 패킷을 목적지까지 최적 경로로 전달하는 과정 | "내비게이션" |
| **라우팅 테이블** | 목적지별 다음 홉 정보를 저장하는 테이블 | "도로 안내 표지판" |
| **AS(자율 시스템)** | 단일 라우팅 정책으로 관리되는 네트워크 집합 | "한 나라" |

---

## Ⅰ. 개요 및 필요성

- 개요: BGP origin 검증 체계
- 배경: BGP는 prefix를 광고한 AS의 권한을 기본 검증하지 않아 hijack·오광고 위험이 있음
- 필요성: ROA와 origin validation으로 Invalid 경로를 식별해 라우팅 피해 범위를 줄임
- 판단 기준: ROA coverage, invalid route count, validator uptime, RTR session 상태로 검증

---

## Ⅱ. 구조 및 구성요소

```text
RIR / Resource Holder -> ROA Repository -> RPKI Validator
-> VRP Cache -> Router RTR Session -> BGP Route Validation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ROA | prefix, maxLength, origin AS를 서명 | RFC 6482 프로파일 |
| Repository | ROA와 인증서 게시 | RRDP/rsync 동기화 |
| Validator | 인증서 체인과 ROA 검증 | VRP 생성, stale 관리 |
| RTR Session | 라우터에 VRP 전달 | RFC 6810 계열 프로토콜 |
| Router Policy | Valid/Invalid/NotFound 처리 | Invalid reject 또는 local-pref 조정 |

> 요약: RPKI는 ROA 게시, validator 검증, VRP 전달, 라우터 정책 적용 순서로 BGP origin을 검증한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Prefix 보유자 ROA 생성 -> Repository 게시 -> Validator 검증
-> VRP 생성 -> Router 수신 -> BGP 경로 Valid/Invalid/NotFound 분류
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 주소 자원 보유자가 ROA 생성 | prefix, maxLength, ASN 정확도 |
| 2 | repository가 ROA와 인증서 게시 | RRDP/rsync sync 성공 |
| 3 | validator가 서명·체인·만료 검증 | VRP freshness, validation error |
| 4 | 라우터가 RTR로 VRP 수신 | RTR session up, serial sync |
| 5 | BGP 경로를 Valid/Invalid/NotFound로 표시 | invalid route reject count |

> 요약: RPKI는 서명된 ROA를 VRP로 변환해 라우터가 BGP origin AS 권한을 판정하게 한다.

---

## Ⅳ. 특징

| 구분 | 일반 BGP | RPKI ROV | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 검증 대상 | 경로 속성 신뢰 | prefix-origin AS 권한 | Valid/Invalid/NotFound |
| 공격 대응 | 필터·IRR 수작업 | ROA 기반 자동 검증 | invalid reject rate |
| 범위 | AS_PATH 정책 검증 없음 | origin validation 중심 | route leak 전체 방어 아님 |
| 운영 요소 | BGP 세션 관리 | validator·ROA lifecycle | ROA coverage, stale VRP |

> 요약: RPKI는 origin hijack 방어에 초점을 두며 route leak과 AS_PATH 변조까지 단독으로 해결하지 않는다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | RPKI ROV | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | IRR prefix filter | ROA/VRP 기반 검증 | 자동화와 신뢰 체계 필요 |
| 비용/성능 | 수작업 갱신 부담 | validator 운영 필요 | ROA coverage와 운영 인력 |
| 운영/위험 | stale IRR 위험 | 잘못된 ROA로 자기 차단 | maxLength 변경 절차 |

> 요약: RPKI는 자동 검증을 제공하지만 ROA 오류가 직접 라우팅 차단으로 이어질 수 있어 변경 통제가 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 ROA | maxLength·ASN 입력 오류 | change review, pre-validation | self-invalid route count |
| Validator 장애 | 단일 validator·repository 지연 | validator 2종 이상, cache 유지 | validator uptime, VRP age |
| 과도한 차단 | NotFound를 Invalid처럼 처리 | policy 분리, monitor mode 단계 | dropped prefix count |

> 요약: RPKI 리스크는 ROA 오류, validator 장애, 정책 오적용으로 나눠 운영한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 커버리지 | 자사 prefix ROA coverage 100% | RIR portal, validator report |
| 검증 상태 | self invalid 0건 | router bgp validation table |
| 가용성 | validator 99.9%, VRP age 기준 이하 | monitoring, RTR session log |

> 요약: RPKI 도입 효과는 ROA 커버리지, self invalid 0건, validator 가용성으로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 자사 prefix별 ROA를 생성하고 maxLength는 실제 광고 prefix 길이에 맞춰 최소 권한으로 설정한다.
2. Routinator, rpki-client 등 validator를 2종 이상 구성하고 라우터 RTR session을 이중화한다.
3. monitor-only 단계에서 Invalid 경로 영향도를 분석한 뒤 reject policy를 peer·transit별로 단계 적용한다.

**결론 (2줄):**
- 기술사 판단: 인터넷 연결 AS는 RPKI ROA 생성과 Invalid reject를 기본 통제로 채택하되 NotFound 처리 정책은 경로 영향 분석 후 결정한다.
- 향후 방향: RPKI는 ASPA, BGPsec, route leak 탐지와 결합해 origin 검증에서 경로 검증으로 확장된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RPKI를 설명하시오" | ROA-Validator-Router 검증 흐름 | 일반 BGP 대비 origin 검증 |
| 요구사항 명시형 | "라우팅 보안 방안을 제시하시오" | Invalid 탐지·차단 운영 절차 | ROA coverage, self invalid, RTR 이중화 |

> 요약: 설명형은 검증 체계를, 보안형은 공격 원리와 운영 정책을 중심으로 전환한다.
