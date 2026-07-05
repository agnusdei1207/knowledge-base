---
title: "RBAC 역할 기반 접근 제어 (Role-Based Access Control)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 99
---

# 📖 【암기용】 개념 완전 이해

> 목적: RBAC를 역할 목록 암기가 아니라 사용자-역할-권한 매핑과 SoD, access review 운영 관점으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: RBAC는 사용자에게 역할을 부여하고 역할에 권한을 연결하는 접근 제어 모델
- **왜 필요한가**: 사용자마다 권한을 직접 붙이면 1,000명 조직에서 권한 변경과 회수가 사람이 감당하기 어려운 수준으로 늘어난다. 역할은 직무 단위 권한 묶음으로 운영 복잡도를 줄인다.
- **핵심 직관**: "김대리에게 DB 조회권한"이 아니라 "김대리에게 정산담당자 역할"을 주고, 정산담당자 역할에 필요한 권한을 묶는 방식임.

## 깊이 이해
- **배경·문제의식**: DAC는 소유자가 권한을 주고, MAC은 보안 등급이 강제한다. 기업 시스템은 직무·부서·승인 체계가 중심이므로 역할 기반 관리가 접근권한 운영에 적합함.
- **작동 원리**: 관리자는 Permission을 Role에 연결하고 User를 Role에 배정한다. 사용자가 요청하면 PEP가 세션의 role을 확인하고 허용된 operation만 수행한다. SoD(직무분리)는 결재자와 실행자를 동시에 가질 수 없도록 제한함.
- **비유**: 건물 출입증에 "재무팀" 권한이 찍혀 있으면 재무층 문이 열리고, 서버실 문은 열리지 않는 구조임.
- **구체 예시**: ERP에서 구매요청자, 구매승인자, 지급처리자 역할을 분리하고 동일 사용자가 구매승인자와 지급처리자를 동시에 보유하지 못하게 SoD rule을 둠.
- **흔한 오해·주의점**: RBAC는 인증 모델이 아니다. 로그인으로 사용자 신원이 확인된 뒤, 역할을 기준으로 인가 여부를 판단하는 모델임.

## 연결 개념
- ABAC - 속성과 환경 조건까지 반영하는 동적 접근 제어
- SSO/OIDC - 사용자 인증과 역할 claim 전달
- IAM Governance - access review, SoD, 권한 회수 프로세스

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. RBAC 정의보다 role explosion, SoD, access review, 감사 지표를 중심으로 작성한다.
> 핵심: 인증은 IdP, 인가는 RBAC 정책 평가이며, 역할 설계와 권한 검토가 채점 포인트이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RBAC는 사용자(User), 역할(Role), 권한(Permission)을 분리해 직무 단위로 인가를 관리하는 모델이다.
> 2. **가치**: 직무 변경 시 사용자-역할 매핑만 조정해 권한 부여·회수의 감사 가능성을 높인다.
> 3. **판단 포인트**: role explosion, SoD 충돌, 장기 미사용 권한, 정기 access review를 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 접근 제어 모델 이해 확인 | User-Role-Permission, session, hierarchy, constraint | RBAC를 로그인 인증으로 설명 |
| 기업 권한 운영 판단 확인 | 최소권한, SoD, role engineering, access review | 역할만 나열하고 권한 회수 절차 누락 |
| RBAC 한계 인식 확인 | role explosion, context 미반영, ABAC 보완 | 모든 동적 조건을 RBAC로 해결한다고 서술 |

> 요약: RBAC 답안은 역할 매핑 구조와 운영 통제(SoD·검토·회수)를 함께 써야 채점 포인트를 충족한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | RBAC는 사용자에게 역할을 부여하고 역할에 권한을 연결하는 접근 제어 모델 | "이 개념의 핵심" |
| **왜 필요한가** | 사용자마다 권한을 직접 붙이면 1,000명 조직에서 권한 변경과 회수가 사람이 감당하기 어려운 수준으로 늘어난다 | "이 개념의 핵심" |
| **핵심 직관** | "김대리에게 DB 조회권한"이 아니라 "김대리에게 정산담당자 역할"을 주고, 정산담당자 역할에 필요한 권한을 묶는 방식임 | "이 개념의 핵심" |
| **배경·문제의식** | DAC는 소유자가 권한을 주고, MAC은 보안 등급이 강제한다 | "이 개념의 핵심" |
| **작동 원리** | 관리자는 Permission을 Role에 연결하고 User를 Role에 배정한다 | "이 개념의 핵심" |
| **비유** | 건물 출입증에 "재무팀" 권한이 찍혀 있으면 재무층 문이 열리고, 서버실 문은 열리지 않는 구조임 | "이 개념의 핵심" |
| **구체 예시** | ERP에서 구매요청자, 구매승인자, 지급처리자 역할을 분리하고 동일 사용자가 구매승인자와 지급처리자를 동시에 보유하지 못하게 SoD rul... | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성

- 개요: 역할 매개 접근 제어
- 배경: 사용자별 권한 직접 부여는 직무 변경, 겸직, 퇴사 시 권한 회수 누락과 감사 추적 단절을 만든다.
- 필요성: RBAC는 NIST RBAC 모델처럼 역할-권한-사용자 매핑으로 내부통제, 개인정보 접근, 관리자 권한 검토를 표준화한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Role Assignment -> Role -> Permission Assignment -> Resource
             +-> SoD Constraint / Role Hierarchy
Session -> Active Role -> Policy Enforcement -> Audit Log
```

| 구성요소 | 역할 | 검증 포인트 |
|:---|:---|:---|
| User | 인증된 주체 | employee status, department |
| Role | 직무 기반 권한 묶음 | owner, purpose, review cycle |
| Permission | resource와 operation 조합 | read/write/delete, API scope |
| Constraint | SoD, 시간, 승인 제한 | static SoD, dynamic SoD |
| Session | 활성 역할과 요청 컨텍스트 | role activation, timeout |

> 요약: RBAC는 사용자와 권한을 직접 연결하지 않고 역할과 제약조건을 통해 인가 결정을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
User Login -> Identity Verify -> Role Load
-> SoD / Status Check -> Permission Match
-> Allow or Deny -> Access Log -> Review
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IdP 또는 IAM에서 사용자 인증 | MFA, 계정 상태 |
| 2 | 사용자-역할 매핑 조회 | HR 직무, 부서, 승인 이력 |
| 3 | 역할 제약조건 평가 | SoD 충돌, 만료일, 비활성 역할 |
| 4 | 요청 권한과 Role Permission 비교 | resource, action, scope |
| 5 | 허용·거부와 감사 기록 | who, what, when, decision |

> 요약: RBAC 인가는 인증된 사용자의 역할을 불러온 뒤 SoD와 권한 매칭을 거쳐 허용·거부를 기록한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | RBAC | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 권한 관리 | 사용자별 ACL | 역할별 Permission 묶음 | NIST RBAC, INCITS 359 |
| 운영 통제 | 수동 권한 부여 | role owner 승인·검토 | access review 분기 1회 |
| 내부통제 | 사후 감사 | SoD constraint 사전 차단 | 결재/지급 겸직 금지 |
| 한계 | 단순 구조 | 역할 수 증가와 context 부족 | role 수 사용자 수의 20% 이하 목표 |

> 요약: RBAC는 직무 기반 권한 운영에 적합하지만, 역할이 과도하게 늘면 ABAC나 policy 조건 보완이 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | RBAC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | ACL | User-Role-Permission | 직무 반복성이 높고 감사 필요 |
| 비용/성능 | 권한 직접 관리 | role engineering 초기 비용 | 사용자 500명 이상, 업무 역할 20개 이상 |
| 운영/위험 | 권한 누락·잔존 | role explosion, SoD 관리 | 역할 owner와 검토 주기 확보 |

> 요약: RBAC는 직무가 명확한 조직에 우선 적용하고, 동적 조건이 많은 서비스는 ABAC와 결합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Role Explosion | 부서·시스템별 역할 중복 생성 | role mining, role consolidation | 사용자 대비 role 비율 20% 이하 |
| SoD 위반 | 승인자와 실행자 역할 동시 보유 | static/dynamic SoD rule, 승인 workflow | SoD 위반 0건 |
| 권한 잔존 | 전보·퇴사 반영 지연 | HRIS 연동, access review 분기 1회 | 미사용 권한 회수율 95% 이상 |

> 요약: RBAC 리스크는 역할 수, SoD 충돌, 권한 잔존으로 측정하고 정기 검토로 줄인다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 권한 정확도 | role-permission 승인 이력 100% | IAM workflow, 변경 로그 |
| 검토 주기 | 핵심 시스템 분기 1회 review | reviewer sign-off, 표본 점검 |
| 감사 추적 | deny/allow decision 1년 보관 | IAM 로그, SIEM 상관분석 |

> 요약: RBAC 운영 성과는 역할 정의서, 검토 완료율, 권한 결정 로그로 증명해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. HR 직무와 시스템 권한을 매핑해 role catalog를 만들고 role owner, 목적, 권한 목록, 검토 주기를 문서화함.
2. 결재자/집행자, 개발자/운영자 등 SoD rule을 IAM에 등록하고 예외 권한은 만료일 7일 이하로 제한함.
3. 분기 1회 access review, 90일 미사용 권한 회수, allow/deny 로그 1년 보관을 SIEM과 연계함.

**결론 (2줄):**
- 기술사 판단: 정형 직무와 내부통제 중심 시스템은 RBAC, 위치·시간·위험도 조건이 중요한 시스템은 ABAC 병행이 적합함.
- 향후 방향: IAM Governance, IGA, Zero Trust와 결합해 role mining 자동화와 지속적 access review로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RBAC를 설명하시오" | User-Role-Permission, session, constraint 흐름 | NIST RBAC, SoD, ACL/ABAC 비교 |
| 요구사항 명시형 | "접근통제 방안을 제시하시오", "RBAC와 ABAC를 비교하시오" | 역할 설계, SoD, access review 흐름 | role explosion, 동적 조건 한계, 선택 기준 |

> 요약: 포괄형은 RBAC 모델 구조, 비교·방안형은 역할 설계와 권한 검토 운영을 중심으로 쓴다.
