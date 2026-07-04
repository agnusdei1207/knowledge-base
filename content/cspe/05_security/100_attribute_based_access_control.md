---
title: "ABAC 속성 기반 접근 제어 (Attribute-Based Access Control)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 100
---

# 📖 【암기용】 개념 완전 이해

> 목적: ABAC를 속성 나열이 아니라 PDP/PEP 정책 평가와 context freshness 관점으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: ABAC는 주체·객체·행위·환경 속성을 정책으로 평가하는 접근 제어 모델
- **왜 필요한가**: 역할만으로는 "외부망에서 야간에 고객정보 대량 다운로드" 같은 위험 조건을 구분하기 어렵다. ABAC는 시간, 위치, 단말 상태, 데이터 등급, 위험 점수를 함께 본다.
- **핵심 직관**: "누구 역할인가"만 묻는 RBAC와 달리, ABAC는 "누가, 무엇을, 어떤 상황에서, 어떤 행위로" 접근하는지 판단함.

## 깊이 이해
- **배경·문제의식**: 클라우드·API·제로트러스트 환경에서는 사용자 역할이 같아도 접속 위치, 단말 보안 상태, 데이터 민감도에 따라 권한이 달라져야 한다. ABAC는 속성과 정책을 분리해 동적 인가를 수행함.
- **작동 원리**: PEP가 접근 요청을 가로채고 subject, object, action, environment 속성을 수집한다. PDP는 PAP가 관리하는 정책과 PIP가 제공한 속성을 평가하여 Permit/Deny를 반환한다. PEP는 결정을 집행하고 로그를 남김.
- **비유**: 공항 보안검색이 탑승권만 보지 않고 여권, 목적지, 수하물, 시간, 위험 경보를 함께 확인하는 구조임.
- **구체 예시**: 고객정보 API는 `role=상담원`, `device=managed`, `network=corp`, `time=09-18`, `data_class=PII`, `risk_score<50` 조건을 모두 만족할 때 조회만 허용함.
- **흔한 오해·주의점**: ABAC는 역할을 없애는 모델이 아니다. RBAC 역할도 subject attribute로 사용하며, 정책과 속성 신선도 관리가 없으면 예측 불가한 인가 결과가 발생함.

## 연결 개념
- RBAC - 역할을 subject attribute로 사용하는 보완 모델
- Zero Trust - 지속 검증과 동적 정책 평가의 기반
- XACML/OPA - ABAC 정책 표현과 PDP 구현 기술

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. ABAC 속성 종류 나열보다 PEP/PDP/PIP/PAP, context freshness, 정책 검증과 감사 지표를 연결한다.
> 핵심: subject/object/action/environment 속성과 정책 결정 위치를 분명히 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ABAC는 속성과 정책을 조합해 요청 시점의 접근 허용 여부를 동적으로 결정하는 접근 제어 모델이다.
> 2. **가치**: 역할, 데이터 등급, 단말 상태, 위치, 시간, 위험 점수를 결합해 최소권한과 제로트러스트 정책을 구현한다.
> 3. **판단 포인트**: PEP/PDP 분리, 속성 신선도, 정책 충돌, 감사 로그와 정책 테스트가 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 접근 제어 이해 확인 | subject, object, action, environment 속성 | ABAC를 단순 사용자 속성 목록으로 설명 |
| 정책 평가 구조 확인 | PEP, PDP, PIP, PAP와 Permit/Deny 흐름 | 정책 결정과 집행 위치 혼동 |
| 운영 리스크 판단 확인 | context freshness, 정책 충돌, explainability, 감사 | 속성 최신성·테스트·로그 지표 누락 |

> 요약: ABAC 답안은 속성 4종과 정책 평가 컴포넌트, 속성 신선도 통제를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 속성 조건 기반 인가
- 배경: RBAC만으로는 동일 역할 사용자의 데이터 등급, 단말 상태, 위치, 시간, 위험 점수 차이를 반영하기 어렵다.
- 필요성: NIST SP 800-162 ABAC 모델을 적용해 클라우드 IAM, 개인정보 API, 제로트러스트에서 동적 최소권한을 평가해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Access Request -> PEP -> PDP -> Decision
                 +-> PIP Attributes
                 +-> PAP Policy
Decision -> Permit / Deny / Obligation -> Audit
```

| 구성요소 | 역할 | 검증 포인트 |
|:---|:---|:---|
| PEP | 요청 차단과 결정 집행 | fail-close, obligation 처리 |
| PDP | 정책 평가와 Permit/Deny 결정 | policy version, latency |
| PIP | 속성 제공자 | HR, CMDB, EDR, GeoIP freshness |
| PAP | 정책 작성·배포 | approval, versioning, test |
| Attribute Set | 주체·객체·행위·환경 속성 | schema, integrity, TTL |

> 요약: ABAC는 PEP가 집행하고 PDP가 판단하며, PIP 속성과 PAP 정책 품질이 인가 결과를 좌우한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request Capture -> Attribute Collect -> Policy Evaluate
-> Conflict Resolve -> Permit or Deny -> Obligation Execute
-> Decision Log -> Policy Review
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PEP가 접근 요청 수집 | subject, object, action, environment |
| 2 | PIP에서 속성 조회 | TTL 5분 이하, source integrity |
| 3 | PDP가 정책 평가 | deny-overrides, priority, version |
| 4 | PEP가 결정 집행 | permit, deny, mask, step-up MFA |
| 5 | 결정 로그와 정책 검토 | policy id, attribute snapshot |

> 요약: ABAC는 요청 시점 속성을 수집해 정책으로 평가하고, 결정 근거를 로그로 남겨 감사 가능성을 확보한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | ABAC | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 판단 기준 | RBAC 역할 | 속성 4종+정책 | NIST SP 800-162, XACML |
| 동적 조건 | 사전 역할 부여 | 시간·위치·단말·위험도 반영 | risk_score, device compliance |
| 정책 운영 | role mapping | policy version/test/deploy | 정책 테스트 100건 이상 |
| 한계 | 단순 운영 | 속성 품질·정책 복잡도 | PDP p95 50ms 이하 목표 |

> 요약: ABAC는 동적 인가에 적합하지만, 속성 신선도와 정책 테스트 없이는 오판정 위험이 커진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | ABAC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RBAC 역할 매핑 | 속성+정책 평가 | 위치·시간·데이터 등급 조건 필요 |
| 비용/성능 | 단순 role lookup | PDP 호출과 속성 조회 | PDP p95 50ms, cache TTL 5분 |
| 운영/위험 | role explosion | policy conflict, stale attribute | 정책 owner와 테스트 체계 필요 |

> 요약: ABAC는 동적 조건이 중요할 때 선택하고, 정형 직무 권한은 RBAC와 결합해 운영한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Stale Attribute | HR/EDR/CMDB 동기화 지연 | TTL, event-driven update, fail-close | 속성 지연 5분 이하 |
| Policy Conflict | permit/deny 정책 충돌 | deny-overrides, priority, policy lint | 충돌 탐지 0건 배포 |
| 감사 어려움 | 결정 근거 미기록 | attribute snapshot, policy id logging | 결정 로그 완전성 100% |

> 요약: ABAC 운영 리스크는 속성 지연, 정책 충돌, 결정 근거 누락이며 자동 테스트와 로그로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 정확도 | permit/deny 테스트 100건 이상 통과 | policy unit test, simulation |
| 결정 지연 | PDP p95 50ms 이하 | APM, gateway metric |
| 감사 추적 | policy id와 attribute snapshot 1년 보관 | SIEM, 로그 샘플링 |

> 요약: ABAC 성공 여부는 정책 테스트, PDP 지연시간, 결정 근거 로그로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. subject/object/action/environment attribute schema를 정의하고 HR, CMDB, EDR, DLP를 PIP로 연동함.
2. PDP는 OPA 또는 XACML 엔진으로 구성하고, PEP는 API Gateway·Service Mesh·DB Proxy에 배치함.
3. deny-overrides 원칙, 속성 TTL 5분 이하, policy unit test 100건 이상, 결정 로그 1년 보관을 운영 기준으로 둠.

**결론 (2줄):**
- 기술사 판단: 직무가 고정된 권한은 RBAC, 데이터 민감도·위치·단말·위험 점수 조건은 ABAC로 설계함.
- 향후 방향: Zero Trust와 결합해 세션 단위 허용에서 요청 단위 지속 인가와 risk-based step-up으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ABAC를 설명하시오" | 속성 수집, PDP 평가, PEP 집행 흐름 | RBAC와 차이, NIST SP 800-162 |
| 요구사항 명시형 | "접근통제 설계 방안을 제시하시오", "RBAC와 비교하시오" | 속성 신선도, 정책 충돌, 감사 흐름 | 선택 기준, PDP 지연, 정책 테스트 지표 |

> 요약: 포괄형은 ABAC 구성요소, 설계·비교형은 속성 품질과 정책 운영 지표를 전면에 둔다.
