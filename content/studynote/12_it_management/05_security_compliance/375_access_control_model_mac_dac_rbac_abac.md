+++
title = "375. 접근 제어 모델 MAC DAC RBAC ABAC (Access Control Model MAC DAC RBAC ABAC)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 접근 제어 모델은 `Subject(사용자/주체)`, `Object(자원)`, `Action(동작)`의 3축과 **신원(Identity)**, **역할(Role)**, **속성(Attribute)**, **분류 등급(Classification)**이라는 결정 변수를 통해 인가(Authorization) 정책을 결정하는 **신원-권한 매핑(Identity-to-Permission Mapping)** 메커니즘으로, DAC(소유자 재량) → MAC(중앙 정책) → RBAC(역할 추상화) → ABAC(속성 기반 동적 평가)로 발전하며 **결정론적 매핑**에서 **확률적·상황적 정책 평가**로 패러다임이 전환되었다.
> 2. **가치**: NIST SP 800-162(ABAC 가이드) 및 RBAC0~RBAC3 표준(NIST INCITS 359)에 따르면, RBAC 도입 시 권한 관리 오버헤드를 약 70% 절감(역할 템플릿화), ABAC 도입 시 세분화된 접근(Per-Record) 정책으로 데이터 유출 표면(Attack Surface)을 80% 이상 축소 가능하며, Zero Trust Architecture(NIST SP 800-207) 및 BeyondCorp 프레임워크의 핵심 인가 엔진으로 작동한다.
> 3. **판단 포인트**: **"정책 표현력(Expressiveness) vs. 관리 복잡성(Administrative Cost) vs. 평가 지연(Evaluation Latency)"** 의 트레이드오프를 정량적으로 비교해야 하며, **규제 환경(DoD 8500, 의료 HIPAA, 금융 PCI-DSS 4.0)**, **조직 규모(Few-Dozen Users vs. 10K+ SaaS Tenant)**, **결정론이 필요한 감사(Deterministic Audit)** vs **맥락 기반 동적 판단(Adaptive Authorization)**의 요건에 따라 모델을 선택하거나 하이브리드(예: RBAC + ABAC PEP/PDP) 구성 여부를 결정한다.

---

## Ⅰ. 개요 및 필요성

현대 엔터프라이즈 환경에서 권한은 더 이상 `사용자 → 권한`의 단순 1:1 매핑으로 표현되지 못한다. 마이크로서비스가 수백 개로 분할되고, 사용자 신원이 SSO/페더레이션(SAML 2.0, OIDC)으로 가상화되며, 자원이 S3 버킷·DocumentDB·Lambda·Kubernetes Namespace 등 폴리글롯 저장소에 흩어지면서 **"누가(Subject), 무엇을(Object), 어떤 맥락에서(Context), 무엇을 할 수 있는가(Action)"** 라는 4-tuple 인가 질의가 **초당 수만~수십만 건** 단위로 발생한다. 1970년대 Lampson의 **Access Matrix(보호 행렬)** 이론에서 출발한 접근 제어는, 시분할 시스템(CTSS, Multics)의 **DAC** → 미 국방부 BLP(Bell-LaPadula) 모델 기반 **MAC** → 1992년 Ferraiolo-Kuhn의 **RBAC** → 2000년대 OASIS XACML/XACML 3.0 기반 **ABAC** 으로 진화해왔으며, 최근에는 **ReBAC(Relationship-Based)**, **PBAC(Policy-Based)**, **RiskBAC** 까지 확장되고 있다.

핵심 기술적 과제는 (1) **정책 평가의 결정성(Determinism)** — 동일 입력에 항상 동일 출력(감사/컴플라이언스 요건), (2) **평가 지연(Evaluation Latency)** — 게이트웨이에서 μs~ms 단위 응답(보통 p99 < 50ms 요건), (3) **정책 결합(Policy Composition)** — 여러 PDP(Policy Decision Point)의 결론을 **deny-overrides / permit-overrides / first-applicable** 알고리즘으로 통합, (4) **상태 폭발(State Explosion)** — ABAC에서 속성 조합이 기하급수적으로 증가(Combinatorial Explosion)하는 문제의 4가지로 요약된다.

```text
[ End-to-End Access Control Architecture (Zero Trust Reference Model) ]

   ┌──────────────────────────────────────────────────────────────────┐
   │                       User / Service Account                     │
   │   (IdP Token : SAML/OIDC + Claims + Device Posture + Geo/Risk)  │
   └────────────────────────────┬─────────────────────────────────────┘
                                │  1. Request
                                ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │   PEP (Policy Enforcement Point)                                │
   │   - API Gateway / Sidecar Proxy (Envoy/Istio) / WAF / DB Proxy │
   │   - TLS 종단, mTLS 상호인증, JWT 검증                          │
   └────────────────────────────┬─────────────────────────────────────┘
                                │  2. Req + Context (XACML Request)
                                ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │   PDP (Policy Decision Point) / Policy Engine                   │
   │   - OPA (Rego) / Cedar (AWS) / OpenFGA / Cerbos                │
   │   - 정책 캐시, 병렬 평가, 결정 캐싱(Decision Cache)            │
   └────────────────┬───────────────────────┬────────────────────────┘
                    │ 3a. PIP Query          │ 3b. Attribute Pull
                    ▼                       ▼
   ┌──────────────────────┐    ┌──────────────────────────────────┐
   │ PIP (Policy Info Pt) │    │   PAP (Policy Admin Point)        │
   │  - User/Role Store   │    │  - GitOps 정책 레포 (OPA Bundle) │
   │  - Resource Metadata │    │  - RBAC Role Catalog             │
   │  - Risk/Threat Intel │    │  - ABAC Policy as Code (Rego)    │
   └──────────────────────┘    └──────────────────────────────────┘
                                │  4. Decision: Permit / Deny / NotApplicable
                                ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │   Object Layer (S3, RDS, K8s API, SFTP, SaaS)                  │
   │   - 서버 측 재검증(Server-side AuthZ), KMS 봉인, ACL            │
   └──────────────────────────────────────────────────────────────────┘
```

| 패러다임 | 시대 | 등장 배경 | 한계 |
| :--- | :--- | :--- | :--- |
| **DAC** | 1970s | UNIX `rwx` 권한, NFSv3 ACL, SMB Share | 트로이 목마, 권한 누적(Privilege Creep), Root 권한 남용 |
| **MAC** | 1970s~80s | Multics·SELinux·Trusted Solaris, BLP·Biba | 유연성 부족(Tightly Coupled), 관리 비용 폭증,商用 환경 부적합 |
| **RBAC** | 1990s~2000s | NIST INCITS 359, ERP/CRM 도입 급증, 역할-기반 업무 분리(SoD) | 역할 폭발(Role Explosion), 정적 정책, 동적 컨텍스트 반영 불가 |
| **ABAC** | 2010s~ | XACML 3.0(OASIS), Zero Trust, 클라우드 네이티브, GDPR/CCPA | 정책 평가 비용, 디버깅 난이도, 결정론 보장 어려움 |
| **ReBAC** | 2020s~ | Google Zanzibar, Auth0 FGA, Authzed, 공유·소셜 그래프 | 관계 그래프의 인덱싱/일관성, Cypher-like Query 비용 |

- **📢 섹션 요약 비유**: 접근 제어 모델의 진화는 **아파트 출입 시스템**의 변화와 같다. ① DAC = 집주인이 열쇠를 만들어 친구에게 주는 방식(친절하지만 도난 위험), ② MAC = 군부대처럼 본부와 경비실이 모든 출입을 통제(철저하지만 불편), ③ RBAC = 우편배달부·경비원·관리인 등 **직급 카드**로 출입区分(효율적), ④ ABAC = "평일 낮, 본사 건물, 노트북 등록, MFA 통과, 평판 점수 70 이상" 등 **상황 조건**을 종합한 스마트 게이트(가장 정밀).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DAC (Discretionary Access Control) — 소유자 재량형

**핵심 원리**: 자원의 **소유자(Owner)**가 임의로 ACL(Access Control List)을 수정할 수 있다. UNIX 파일 시스템(`/etc/passwd`, `chmod 750`), NFSv4 ACL, Windows NTFS DACL, PostgreSQL `GRANT SELECT ON table TO user`, SMB Share Permission이 대표적이다.

```text
[ DAC: UNIX-style Permission Bits ]

   $ ls -la /var/data/finance.db
   -rwxr-x---  1 root   finance   2.1G  finance.db

   Owner(u)   Group(g)   Others(o)
     rwx         r-x        ---
   (7=4+2+1)  (5=4+0+1)  (0)

   Process(pid=1001, uid=alice, gid=finance)
     ├── effective uid = alice
     ├── supplementary groups = {finance, audit}
     └── Access Check:
         1) uid == owner?       → use Owner bits (rwx)
         2) gid in groups?      → use Group bits (r-x)
         3) else               → use Other bits (---)
```

**핵심 메커니즘**: 9-bit Mode Bits 또는 POSIX ACL(`setfacl -m u:alice:rw- file`). SMB/CIFS는 **Share Permission(서버 측)** + **NTFS DACL(파일 시스템 측)** 의 이중 검사를 수행하며, NFSv4는 RFC 3530 기반으로 `OWNER@`, `GROUP@`, `EVERYONE@` ACE를 가진 POSIX-style ACL을 사용한다.

### 2. MAC (Mandatory Access Control) — 강제 접근 통제

**핵심 원리**: **신분(Identity)**이 아니라 **라벨(Label)**에 기반해, 운영자가 변경 불가능한 시스템 전역 정책(TCSEC/Common Criteria)에 따라 강제 결정한다. DoD Orange Book(TCSEC, 1983) B1등급 이상 필수.

```text
[ MAC: Bell-LaPadula (BLP) Confidentiality Model ]

   Subjects  :   TS  S  C  U    (Clearance)
   Objects   :   TS  S  C  U    (Classification)

   ── Security Lattice (격자) ───────────────────────────
           TS  (Top Secret)        ▲ higher
            │                          │
            S   (Secret)              │  No Read Up (NRU)
            │                          │  ★ Property
            C   (Confidential)        │  No Write Down (NWD)
            │                          │  (BLP: Biba는 역방향)
            U   (Unclassified)     ▼ lower

   Example:
   Subject  (S, Clearance = SECRET)
   Object   (C, Classification = CONFIDENTIAL)
   Decision:
       Read?  Clearance(SECRET) >= Classification(CONF) → PERMIT
       Write? (NWD) SECRET subject cannot write to CONF obj → DENY
       (이유: SECRET 사용자가 CONFIDENTIAL 문서를 만들어
        CONF 사용자가 SECRET 정보를 흘려받지 못하게 차단)
```

| MAC 변형 | 보호 목표 | 핵심 규칙 | 적용 사례 |
| :--- | :--- | :--- | :--- |
| **BLP (Bell-LaPadula)** | 기밀성(Confidentiality) | No Read Up, No Write Down (★-property, tranquility) | 군 통신망, NSS(SIPRNet) |
| **Biba** | 무결성(Integrity) | No Read Down, No Write Up | 금융 결제 시스템, SW Supply Chain |
| **Clark-Wilson** | 무결성+상호감사 | Well-formed Tx, Separation of Duty | ERP/회계, 의료 EHR |
| **Chinese Wall (Brewer-Nash)** | 이해상충 방지 | 동일 COI(Conflict of Interest) 클래스 접근 후, 경쟁사 데이터 차단 | 컨설팅, 투자은행 |
| **DTE (Domain-Type Enforcement)** | 격리 | Domain(프로세스)×Type(파일) 매트릭스 | SELinux, Android SE Linux |
| **MLS (Multi-Level Security)** | 등급 혼재 운영 | Single-system with multiple sensitivity levels | Trusted Solaris, Red Hat RHEL MLS |

**구현체**: SELinux( NSA, Flask 아키텍처), AppArmor(프로파일 기반), Trusted Solaris(Sun), TrustedBSD, Red Hat Enterprise Linux with MLS mode. **FLASK(Flux Advanced Security Kernel)** 아키텍처가 Linux Security Module(LSM) 훅의 이론적 토대.

### 3. RBAC (Role-Based Access Control) — 역할 기반

**핵심 원리**: `User → Role → Permission` 의 **간접 매핑(Indirection)**으로, NIST INCITS 359(2004)는 **RBAC0(Base) → RBAC1(Hierarchy) → RBAC2(Constraints) → RBAC3(Combined)** 4단阶梯 모델을 정의한다.

```text
[ RBAC Hierarchy & Constraints Diagram ]

              ┌────────────────┐
              │  CFO (Role)    │
              └───────┬────────┘
                      │ inherits (Senior-Junior)
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────────┐
  │ Senior   │  │ Junior   │  │ Auditor      │
  │Accountant│  │Accountant│  │(Read-only)   │
  └──────────┘  └──────────┘  └──────────────┘
        ▲             ▲              ▲
        │ User-Role Assignment (URA)
        │             │              │
   ┌────┴───┐   ┌────┴───┐     ┌────┴───┐
   │ Alice  │   │  Bob   │     │ Carol  │
   └────────┘   └────────┘     └────────┘

   Permission-Role Assignment (PRA):
     JuniorAccountant → { journal:create, ledger:read }
     SeniorAccountant → { + journal:approve, ledger:write }
     CFO             → { + consolidation:run, close:execute }
     Auditor         → { ledger:read, audit:export }  (SoD!)

   Constraints (RBAC2):
     - SSD (Static Separation of Duty): {CFO, Auditor}  (한 사용자가 둘 다 못 가짐)
     - DSD (Dynamic SoD): 트랜잭션 시작자 ≠ 승인자 (4-eyes principle)
     - Cardinality:  시스템 내 CFO ≤ 1명
```

**상용/오픈소스 구현**: AWS IAM Role + Policy, Azure RBAC(Kusto, Storage built-in roles), Kubernetes RBAC(`Role`, `ClusterRole`, `RoleBinding`), PostgreSQL roles, Keycloak Realm Role/Group, Oracle Database Vault. **Role Mining**(역할 마이닝) 기법으로 기존 `User-Permission` 행렬에서 **역할 후보군**을 클러스터링(예: `RoleMiner`, FastMiner)하여 **Role Explosion** 문제를 완화한다.

### 4. ABAC (Attribute-Based Access Control) — 속성 기반

**핵심 원리**: **XACML 3.0(OASIS Standard, 2013)** 또는 **NGAC(Next Generation Access Control, NIST SP 800-178)** 명세를 따르며, 정책은 부울 함수 형태로 표현된다.

```text
[ ABAC: XACML Reference Architecture ]

   ┌─────────────────┐      ┌──────────────────────────┐
   │  PEP (Proxy)    │─────▶│ PDP (engine: OPA, Axiomatics, │
   │  Sidecar/Filter │ Req  │  AuthzForce, WSO2 Balana)  │
   └─────────────────┘      └────────────┬──────────────┘
                                          │
                            ┌────────────
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 375 / 800

← **이전**: [374. 정보보안 정책 수립 거버넌스 프레임워크](/knowledge-base/studynote/12_it_management/05_security_compliance/374_infosec_policy_governance_framework/)
**다음**: [376. 신원 관리 IAM 통합 인증 SSO](/knowledge-base/studynote/12_it_management/05_security_compliance/376_identity_management_iam_sso_integration/) →

---
