---
sidebar:
  order: 137
  label: "137. 보안 설계 원칙 — 페일 세이프•최소 노출 (Security Design Principles)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "시스템 보안 아키텍처 8대 기본 설계 원칙 : Saltzer & Schroeder 원칙 (NIST SP 800-160 & SP 800-53)"
date: "2026-08-26T15:15:53+09:00"
tags:
  - "notes-security"
weight: 137
extra:
  question_no: "137"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Saltzer & Schroeder의 8대 보안 설계 원칙(Economy of Mechanism, Fail-safe Defaults, Complete Mediation, Open Design, Separation of Privilege, Least Privilege, Least Common Mechanism, Psychological Acceptability), NIST SP 800-160(시스템 보안 공학), 제로 트러스트(Zero Trust PDP/PEP) 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Saltzer & Schroeder 8대 보안 설계 원칙(Security Design Principles / NIST SP 800-160)**: 1975년 Saltzer와 Schroeder가 제안한 컴퓨터 시스템 보안 아키텍처 설계의 기본 철학으로, 시스템 구축 후 사후에 보안 솔루션을 추가하는 방식(Bolt-on)을 지양하고, 시스템 기획·설계 초기부터 보안 취약점과 공격 표면(Attack Surface)을 원천 최소화하도록 규정한 8대 핵심 공학 원칙.
- **사후 보안 덧붙이기 및 기본 허용 정책의 구조적 결함(Bolt-on & Default-Allow Defect)**: 시스템 개발 단계에서 보안을 고려하지 않고 기본 허용(Default-Allow)으로 개통한 후 사후 방화벽이나 백신에만 의존할 경우, 내부 로직 결함, 과도한 관리자 권한(Over-privileged), 권한 검증 캐싱 누락으로 인해 단일 침투만으로 전체 시스템이 장악되는 구조적 결함.

</details>

- 정의/개념: 안전한 시스템 아키텍처를 구현하기 위해 **안전한 기본값(Fail-safe Defaults / Default Deny) $\rightarrow$ 최소 권한(Least Privilege) $\rightarrow$ 완전 중재(Complete Mediation) $\rightarrow$ 메커니즘의 경제성(Economy of Mechanism) $\rightarrow$ 공개 설계(Open Design) $\rightarrow$ 권한 분리(Separation of Privilege) $\rightarrow$ 최소 공통 메커니즘 $\rightarrow$ 심리적 수용성** 을 내재화하는 **시스템 보안 공학 설계 패러다임**
- 배경/필요성: 경계 통제만으로는 내부 과권한과 **검증 우회** 차단 불가

#### 한줄 요약
- Saltzer & Schroeder 8대 원칙은 설계 단계부터 기본 거부, 최소 권한, 완전 중재를 내재화하는 보안 원칙이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Saltzer & Schroeder 3대 핵심 필수 원칙**:
  - **Fail-safe Defaults (안전한 기본값 / Default Deny)**: 접근 권한이 명시적으로 부여되지 않은 모든 요청은 기본적으로 차단하며, 시스템 오류 발생 시 안전한 잠금 상태로 전이.
  - **Least Privilege (최소 권한의 원칙)**: 모든 주체(사용자, 프로세스)에게 특정 과업을 수행하는 데 필수적인 최소한의 권한과 시간만 부여.
  - **Complete Mediation (완전 중재)**: 과거 인증 결과에 의존하거나 검증을 캐싱하지 않고, 모든 자원에 대한 모든 접근 요청을 매번 예외 없이 실시간 검증.

</details>

- 설계 단계부터 공격 표면을 줄이는 **Security by Design**
- 기본 거부와 완전 중재에 기반한 **제로 트러스트**
- 사용자의 통제 우회를 줄이는 **심리적 수용성**

#### 한줄 요약
- 안전한 기본값(Default Deny), 최소 권한(Least Privilege), 완전 중재(Complete Mediation)를 핵심으로 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Saltzer & Schroeder 8대 보안 설계 원칙**:
  1. **Economy of Mechanism**: 설계의 단순성 유지로 검증 용이성 확보 및 버그 최소화.
  2. **Fail-safe Defaults**: 기본 거부(Default Deny) 및 실패 시 안전 잠금.
  3. **Complete Mediation**: 모든 접근에 대한 우회 없는 전수 실시간 검사.
  4. **Open Design**: 알고리즘 공개 상태에서도 키의 비밀성만으로 안전성 유지 (Kerckhoffs 원리).
  5. **Separation of Privilege**: 다중 주체의 다중 조건 승인 강제 (2-Man Rule).
  6. **Least Privilege**: 과업 수행에 필요한 최소 권한 및 최소 시간 부여.
  7. **Least Common Mechanism**: 주체 간 공유 자원 및 경로 최소화로 부채널/연쇄 침해 방지.
  8. **Psychological Acceptability**: 사용자가 거부감 없이 쉽게 준수할 수 있는 사용성 보장.

</details>

```text
보안 설계 원칙
├─ 단순성·기본선
│  ├─ Economy of Mechanism
│  └─ Fail-safe Defaults
├─ 접근 통제
│  ├─ Complete Mediation
│  ├─ Separation of Privilege
│  └─ Least Privilege
└─ 구조·사용성
   ├─ Open Design
   ├─ Least Common Mechanism
   └─ Psychological Acceptability
```

선의 의미: 기본 거부와 단순 설계 위에 완전 중재 및 최소 권한 검증을 거쳐, 공유 자원을 격리하고 사용자 수용성을 보장하는 구조

| 설계 원칙 | 핵심 정의 및 내용 | 현대적 구현 기술 및 표준 | 비고 |
|:---|:---|:---|:---|
| **Economy of Mechanism** | 보안 메커니즘을 최대한 작고 단순하게 설계하여 검증 오류 최소화 | 마이크로커널(Microkernel), TCB 최소화 | Simplicity |
| **Fail-safe Defaults** | 기본 상태를 접근 거부(Deny)로 설정하고 명시적 허용 시에만 개방 | 방화벽 Default Drop, 제로 트러스트 | Baseline |
| **Complete Mediation** | 모든 주체의 모든 객체 접근을 캐싱 없이 매번 인터셉트 검증 | 제로 트러스트 PEP/PDP, IAM 정책 엔진 | Mediation |
| **Open Design** | 설계가 공개되어도 암호키만 안전하면 시스템 보안성 유지 | Kerckhoffs의 원리, AES/RSA 표준 암호 | Transparency |
| **Separation of Privilege** | 단일 권한으로 치명적 동작 불가, 2인 이상의 다중 조건 승인 강제 | 직무 분리(SoD), 다중 서명(Multisig) | Separation |
| **Least Privilege** | 직무 수행에 필요한 최소한의 권한만 부여하고 과권한 방지 | RBAC, ABAC, Just-In-Time(JIT) 권한 | Authorization |
| **Least Common Mechanism** | 서로 다른 사용자 간 공유하는 메커니즘을 최소화하여 상호 간섭 방지 | 컨테이너 격리, 가상화 멀티테넌시 | Isolation |
| **Psychological Acceptability**| 보안 통제가 사용자 업무를 과도하게 방해하지 않도록 설계 | 패스키(Passkey), FIDO2 생체인증 | Usability |

#### 한줄 요약
- 단순성, 기본 거부, 완전 중재, 공개 설계, 권한 분리, 최소 권한, 최소 공통 메커니즘, 심리적 수용성 8대 원칙으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **보안 설계 원칙 기반 접근 통제 5단계 프로세스**:
  1. 클라이언트 요청 인입 시 안전한 기본값(Default Deny) 상태 적용
  2. 정책 집행점(PEP)에서 완전 중재(Complete Mediation) 인터셉트
  3. 정책 결정점(PDP)에서 최소 권한(Least Privilege) 및 직무 분리(SoD) 평가
  4. 최소 공통 메커니즘(Least Common Mechanism) 기반 격리 환경 할당
  5. 감사 로그 기록 및 세션 만료 후 권한 자동 회수

</details>

```text
[사용자] ── 자원 접근 요청 ──> [정책 집행점]
            │
            ▼
1. [완전 중재]
    ├─ 게이트웨이(PEP)가 이전 세션 토큰을 무조건 신뢰하지 않고 패킷 가로채기
    └─ [PDP 정책 결정 서버로 실시간 접근 제어 질의(XACML) 전송]
            │
            ▼
2. [기본 거부 및 최소 권한 평가]
    ├─ [기본 판정: Default Deny] ➔ 명시적 허용 정책이 없으면 1초 내 즉시 차단
    ├─ 사용자 A의 역할(Role) 대조 ➔ "조회 권한"만 확인 (수정/삭제 권한 원천 배제)
    └─ [고위험 자산 확인 시 ➔ 팀장 2차 승인(Separation of Privilege) 요구]
            │
            ▼
3. [최소 공통 메커니즘 실행]
    ├─ 사용자 A에게 전용 단독 격리 세션(Dedicated Session) 할당
    └─ [타 테넌트와의 메모리 및 캐시 공유 버퍼를 물리적으로 분리]
            │
            ▼
4. [인가 및 자동 회수]
    ├─ 15분 만료 시한부(JIT) 토큰 발급 ➔ 계좌 조회 1회 허용
    └─ [세션 종료 즉시 메모리 권한 회수 및 불변 감사 원장(Audit Trail) 기록]
```

**동작 원리**

1. **완전 중재**: PEP가 매 요청의 권한을 PDP에 질의
2. **기본 거부 및 최소 권한 평가**: 허용 범위와 추가 승인 판정
3. **최소 공통 메커니즘 실행**: 전용 격리 세션 할당
4. **인가 및 자동 회수**: JIT 토큰 만료 후 권한 회수·감사

#### 한줄 요약
- 요청 인입, 완전 중재 가로채기, 기본 거부/최소 권한 평가, 격리 자원 할당, 자동 회수 및 감사 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **시스템 장애 시 안전 보증 3대 메커니즘 비교**:
  - Fail-Safe (안전 실패): 장애 발생 시 시스템을 안전한 차단/잠금 상태로 전환 (보안성 최우선).
  - Fail-Secure: 보안 통제가 상실될 바에야 시스템을 완전 정지 (기밀성 최우선).
  - Fail-Open: 장애 발생 시 가용성을 위해 검증을 건너뛰고 문을 개방 (가용성 최우선, 보안 위험).

</details>

| 비교 항목 | 안전 실패 (Fail-Safe) | 보안 최우선 실패 (Fail-Secure) | 개방 실패 (Fail-Open) |
|:---|:---|:---|:---|
| **장애 시 동작** | **사전에 정의된 안전한 기본 상태로 전이** | **모든 접근 완전 잠금 및 시스템 셧다운**| **인증/검사를 건너뛰고 접근 허용** |
| **최우선 가치** | **물리적 안전성(Safety) & 위험 방지** | **기밀성(Confidentiality) 보존** | **가용성(Availability) & 서비스 연속성**|
| **장점** | 인명 사고 및 물리적 파괴 방어 | 악의적 침입 및 데이터 유출 100% 차단| 비상시 서비스 중단 없음 |
| **단점/위험** | 일시적 서비스 가용성 저하 | **정상 업무 완전 마비 리스크** | **해커의 무혈입성 및 전면 침해 위험** |
| **적용 분야** | **철도 신호, 원자력 발전, 스마트 자동차**| **국방 기밀망, 금융 결제 코어 DB** | **화재 비상문, 단순 홍보용 웹서버** |

#### 한줄 요약
- Fail-Safe는 안전 상태 전이, Fail-Secure는 완전 잠금 차단, Fail-Open은 가용성 우선 개방이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-160 (시스템 보안 공학) 및 NIST SP 800-53 (보안 통제)**: 시스템 설계 단계의 보안 내재화 및 접근 통제(AC) 국제 표준 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 개발 단계에서 편의를 위해 'Default Allow'로 설정하여 **신규 배포된 마이크로서비스 API가 인증 없이 외부 인터넷에 노출되어 데이터 유출** | **NIST SP 800-160 준수, 인프라 코드화(IaC) 템플릿에 'Fail-safe Defaults'를 강제하여 명시적 승인 전까지 인바운드 100% 차단** | 설정 누락으로 인한 외부 침해 사고 100% 원천 차단 |
| 관리자 계정에 상시 전지전능한 Root 권한을 부여하여 **관리자 PC 침해 시 전사 클라우드 인프라가 1초 만에 랜섬웨어에 완전 장악** | **NIST SP 800-53 AC-6 준수, JIT(Just-In-Time) 임시 권한 승인 및 직무 분리(Separation of Privilege) 다중 승인 파이프라인 구축** | 과도한 권한 남용 및 단일 계정 탈취 피해 반경 90% 이상 축소 |
| 인증 검증 결과를 세션 캐시에 영구 보관하여 **인사과에서 퇴사 처리된 직원의 권한이 즉시 회수되지 않고 잔여 세션으로 무단 접속 지속** | **Complete Mediation 원칙 적용, 제로 트러스트 PDP/PEP 아키텍처를 구축하여 매 자원 접근 시마다 권한 유효성을 실시간 재검증** | 퇴사자 및 권한 박탈자의 잔여 세션 악용 100% 방지 |

#### 한줄 요약
- Fail-safe Defaults로 노출을 막고, 최소 권한/직무 분리로 피해를 줄이며, Complete Mediation으로 퇴사자 세션을 차단한다.

## Ⅶ. 결론

- 모든 접근은 **기본 거부·완전 중재**, 권한은 과업 기간만 최소 부여

#### 한줄 요약
- Saltzer & Schroeder 8대 원칙을 설계 초기부터 내재화하여 무결점 제로 트러스트 보안 아키텍처를 완성한다.
