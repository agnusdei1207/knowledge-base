---
sidebar:
  order: 60
  label: "060. ABAC 속성 기반 접근 제어 (Attribute-Based Access Control)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "ABAC 속성 기반 접근 제어 (Attribute-Based Access Control)"
date: "2026-08-13T20:00:00+09:00"
tags:
  - "notes-security"
weight: 60
extra:
  question_no: "060"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 70
  priority_note: "122•135회 반복된 속성 기반 동적 권한 핵심임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **속성 기반 접근 제어(Attribute-Based Access Control, ABAC)**: 주체(Subject), 객체(Resource/Object), 행위(Action), 환경(Environment)의 속성(Attribute) 조합 조건문을 Boolean 정책(Policy)으로 평가하여 동적 인가 여부를 판정하는 메커니즘.
- **역할 기반 접근 제어(Role-Based Access Control, RBAC)**: 직무(Role) 단위로 정적 권한을 맵핑하는 3계층 접근 제어 모델.

</details>

- 정의/개념: 요청 속성 조합을 평가하는 **ABAC**
- 배경/필요성: 정적 역할만으로는 **역할 폭발•실시간 맥락** 통제 불가

#### 한줄 요약

- 주체, 객체, 행위, 환경 속성을 조건으로 조합하여 실시간 동적 인가를 집행함.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **주체 속성(Subject Attributes)**: 요청자의 신원 ID, 직급, 부서, 보안 승인 등급.
- **객체 속성(Object Attributes)**: 대상 데이터의 비밀 등급(Sensitive/Public), 소유자, 문서 유형.
- **행위 속성(Action Attributes)**: 요청 작업 종류(Read, Write, Approve, Delete, Export).
- **환경 속성(Environment Attributes)**: 접근 시간(Business Hours), 접속 IP, 기기 하드닝 상태, 지리적 위치.
- **정책 정보점(Policy Information Point, PIP)**: 외부 DB/LDAP 등에서 최신 속성 데이터를 조회 및 공급하는 컴포넌트.
- **정책 결정점(Policy Decision Point, PDP)**: 속성 데이터와 수록된 정책 규칙을 대조하여 최종 허용/거부(Permit/Deny)를 결정하는 엔진.
- **정책 집행점(Policy Enforcement Point, PEP)**: 클라이언트 요청을 차단 가로채기하여 PDP의 결정값에 따라 실제 접속을 통제하는 게이트웨이.
- **속성 신선도(Attribute Freshness)**: PIP가 제공하는 속성이 실시간으로 동기화되어 유효한 상태인지 지칭하는 수치.

</details>

- **주체**, **객체**, **행위**, **환경** 4대 속성의 논리 조합을 통한 세밀한(Fine-Grained) 인가 통제.
- **PEP**, **PDP**, **PIP**, PAP 표준 논리 컴포넌트 분리 아키텍처 적용.
- 실시간 Context 기반 **속성 신선도(Attribute Freshness)** 확보 및 무상태(Stateless) 인가 대조.

#### 한줄 요약

- 4대 속성 결합, PEP-PDP-PIP 분리 구조 및 실시간 컨텍스트 반영을 통한 Fine-Grained 통제를 제공함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **속성 권위자(Attribute Authority)**: HR DB, 기기 관리(MDM) 등 신뢰할 수 있는 속성을 원천 생성 및 관리하는 주체.
- **정책 저장소(Policy Store)**: XACML 기반 허용/거부 규칙 및 정책 결합 알고리즘(Deny-Overrides 등)을 보관하는 DB.

</details>

```text
ABAC 정책 구조
├─ 정책 집행점 PEP: 정책 결정 집행
├─ 정책 결정점 PDP: 속성•정책 평가
├─ 정책 저장소: 규칙•충돌 기준 관리
├─ 속성 정보점 PIP: 신뢰 속성 조회
└─ 속성 권위자: 신뢰 속성 생성•갱신
```

| 구성요소 | 책임 |
|:---|:---|
| 정책 집행점 (PEP) | 접근 요청 인터셉트, **PDP**로 결정 위탁 및 **PEP**가 승인/거부 결과 집행 |
| 정책 결정점 (PDP) | XACML 정책 규칙을 읽고 **PIP** 속성을 대조하여 Permit/Deny 인가 판정 |
| 정책 저장소 (PAP) | 인가 정책(Rules, Policies, Policy Sets) 저술 및 보관 관리 |
| 속성 정보점 (PIP) | HR, IAM, MDM 등 **속성 권위자**로부터 실시간 판단 데이터 조회 공급 |
| 속성 권위자 | 주체/객체/환경 속성의 신뢰성(Truth)을 관리하는 원천 시스템 |

#### 한줄 요약

- PEP 게이트웨이, PDP 판단 엔진, PAP 정책 관리자, PIP 속성 수집기 및 속성 권위자 구조로 이뤄짐.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **생존 시간(Time to Live, TTL)**: PIP가 캐싱하여 참조하는 속성 데이터의 최대 무결성 보장 유효 기한.
- **기본 거부(Default Deny)**: 명시적 Permit 정책 조건에 부합하지 않거나 평가 오류 발생 시 접근을 무조건 차단하는 기본 준칙.
- **요청 속성•맥락 추출**: HTTP Header, Token, IP 등에서 4대 속성을 파싱하는 단계.
- **적용 정책•충돌 규칙 선택**: 타겟 리소스에 맵핑된 Policy Set 및 Combining Algorithm을 불러오는 단계.
- **권위자•TTL•무결성 검증**: PIP 속성의 TTL 만료 여부 및 서명 무결성을 검증하는 단계.
- **정책 평가•기본 거부**: Boolean 조건 수식 대조 및 Default Deny 적용 단계.
- **결정 집행•감사 기록**: PEP 통제 및 인가 결과 Audit Log 저장 단계.

</details>

```text
접근 요청
    │
    ▼
1. 요청 속성•맥락 추출
    │
    ▼
2. 적용 정책•충돌 규칙 선택
    │
    ▼
3. 권위자•TTL•무결성 검증
    │
    ▼
4. 정책 평가•기본 거부
    │
    ├─ 오류•불일치 ── 거부
    │
    └─ 명시적 허용 ── 5. 결정 집행•감사 기록
                               │
                               ▼
                          보호 자원 접근
```

### 동작 원리

1. **요청 속성•맥락 추출**: **PEP**에서 요청 신호 파싱 및 4대 속성 파라미터 구성.
2. **적용 정책•충돌 규칙 선택**: **PDP**가 **PAP** 저장소에서 리소스 정책 및 조합 규칙(Policy Combining Algorithm) 로드.
3. **권위자•TTL•무결성 검증**: **PIP**가 HR/MDM 시스템에서 **TTL** 기반 속성 조회 및 무결성 대조.
4. **정책 평가•기본 거부**: **PDP**가 논리 조건 평가 수행, 미합치 시 **Default Deny** 집행.
5. **결정 집행•감사 기록**: **PEP**가 허용된 트래픽을 통과시키고 Audit Log 기록.

#### 한줄 요약

- 속성 추출, 적용 정책 선택, PIP TTL 속성 검증, PDP 정책 평가 및 Default Deny, PEP 집행을 구동함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **혼합 모델(Hybrid RBAC-ABAC / RABAC)**: RBAC 역할을 1차 필터링 프레임으로 사용하고, 2차 세부 조건(시간, 기기, 위치)을 ABAC 속성으로 검증하는 하이브리드 인가 기법.

</details>

| 접근 제어 모델 | RBAC | ABAC | 혼합 모델 (Hybrid RBAC-ABAC) |
|:---|:---|:---|:---|
| 적용 기준 | 정적 직무 기반 접근 통제 | 제로 트러스트 실시간 동적 접근 통제 | 대규모 엔터프라이즈 하이브리드 아키텍처 |
| 핵심 특징 | 사용자-역할-권한 3계층 간접 맵핑 | **주체•객체•행위•환경** 4대 속성 동적 대조 | 역할(RBAC) 1차 필터 + 속성(ABAC) 2차 파라미터 |
| 장단점 | 직관적 / 역할 폭발(Role Explosion) 유의 | 세밀함 / 정책 복잡성 및 **PDP** 성능 부하 | 역할 폭발 억제 및 PDP 연산 최적화 |

#### 한줄 요약

- 직무 중심 RBAC, 동적 속성 ABAC 및 1차 역할+2차 속성을 조합한 Hybrid 모델을 비교 선택함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NIST SP 800-162**: NIST의 ABAC 가이드라인 문서로 아키텍처 설계, 속성 관리 및 정책 평가 수명주기 명시.
- **OASIS XACML 3.0 Errata 01**: eXtensible Access Control Markup Language로 ABAC의 표준 정책 표현 및 프로토콜 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 속성 및 인가 체계 아키텍처 설계 혼선 | **NIST SP 800-162** 가이드 준수 | 속성 수명주기 및 아키텍처 정합성 확보 |
| 솔루션 간 정책 언어 이종성 | **OASIS XACML 3.0** 및 JSON Profile 준수 | PEP-PDP 표준 인터페이스 및 상호운용성 보장 |
| 속성 동기화 지연에 따른 잘못된 허용/거부 | **속성 권위자** 연동, **TTL** 캐싱 단축 및 **기본 거부** 적용 | 속성 신선도 확보 및 Stale 데이터 인가 오류 차단 |

#### 한줄 요약

- NIST SP 800-162 준수, OASIS XACML 3.0 표준 정책 구현 및 PIP 속성 캐싱(TTL) 단축 대책을 수립함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **신뢰 속성(Trusted Attributes)**: cryptographic signature 및 OAuth DPoP 등으로 출처 무결성이 증명된 속성.
- **설명 가능성(Explainability)**: 인가 승인/거부 판단 시 어떤 정책 규칙과 속성값이 적용되었는지 역추적하는 성질.

</details>

- **신뢰 속성** 관리를 위해 **NIST SP 800-162** 및 **XACML 3.0**을 적용하고, **설명 가능성** 향상을 위해 audit trace 로그 시스템 구축.

#### 한줄 요약

- 직무는 **RBAC**, 실시간 세부 조건은 **ABAC** 적용
