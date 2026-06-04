---
title: "435. 클라우드 IAM 역할 정책 최소 권한 (Cloud IAM Role Policy Least Privilege)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 IAM 역할 정책 최소 권한은 **Subject–Action–Resource–Condition** 4-tuple 기반의 정책 그래프에서 `Action: "*"` `Resource: "*"` 와일드카드를 제거하고, `Condition` 블록(시간/IP/MFA/태그 기반)으로 컨텍스트를 좁혀 권한 그래프(Authorization Graph)의 Out-degree를 최소화하는 **Zero Trust-Ready RBAC/ABAC 하이브리드 통제**이다.
> 2. **가치**: AWS IAM Access Analyzer 정책 검증 결과 적용 시 정책 위반 가능성 평균 73% 감소, 침해 사고 시 **블래스트 레이더(Blast Radius)** 가 계정 단위에서 단일 리소스 단위로 축소되어 NIST 800-53 AC-6 / ISO 27001 A.9.4 / PCI-DSS 7.1 컴플라이언스 통과율 30% 이상 향상, 권한 감사(Audit) 시간 평균 60% 단축.
> 3. **판단 포인트**: **과소 권한(Under-privilege) -> 업무 마비** vs **과대 권한(Over-privilege) -> 침해 표면 확장** 트레이드오프, **Role Assumption Chain**(사용자->역할->다른 역할)의 깊이 제한(2-hop 권장), Permission Boundary/Session Policy의 **이중 통제** 사용 여부, 그리고 **자격 증명 명명(Naming Convention)** 및 **태그 거버넌스(Tag Governance)** 성숙도가 결정적.

---

## Ⅰ. 개요 및 필요성

클라우드 환경으로의 전환이 가속화되면서, **수백 개 계정에 수천 개의 IAM 역할/정책**이 산재하는 **"Permission Sprawl"** 현상이 발생한다. 전통적인 온프레미스 AD/LDAP 기반 그룹 정책(Group Policy)은 ① 정적(Static)이고 ② 변경 이력 추적이 어려우며 ③ 클라우드 네이티브 서비스(S3, Lambda, DynamoDB 등)에 대한 세밀한 리소스 제어가 불가능하다는 한계를 가진다. AWS·Azure·GCP 같은 Hyperscaler는 각각 **IAM Policy JSON**(AWS), **Azure RBAC + ABAC 조건**(Azure), **IAM Policy v3 Bindings**(GCP)이라는 형태로 정책을 코드화(IaC)하여 정밀한 제어가 가능해졌지만, **편의성**을 위해 `*:*` 와일드카드나 관리형 정책(AdministratorAccess)을 그대로 부여하는 안티패턴이 만연하다.

실제로 2023년 Capital One 침해 사고(Capitol One SSRF -> S3 버킷 데이터 유출)는 과도한 IAM 권한이 핵심 원인이었고, 2024년 Microsoft Midnight Blizzard(러시아 APT29) 사건에서도 OAuth Application에 부여된 과도한 Mail.ReadWrite 권한이 이메일窃取로 이어졌다. 즉, **IAM 최소 권한은 클라우드 보안의 1차 방어선(First Line of Defense)** 이자 **컴플라이언스 감사의 필수 통제 항목**이다.

```text
[전통적 접근 vs 클라우드 IAM 최소 권한]

  +--------------------------+        +------------------------------+
  |  On-Premise Legacy Model |        |  Cloud-Native Least Privilege |
  |  ----------------------  |        |  ---------------------------  |
  |   AD Group: SG_Admins   |   ->->->  |  IAM Role: S3ReadOnlyRole    |
  |   OU: Finance_Dept      |        |  Trust: Federated SAML/SSO    |
  |   GPO: FullControl      |        |  Policy: s3:GetObject on     |
  |   Effective: Domain-wide|        |           arn:aws:s3:::bucket |
  |   Audit: EventLog(주기) |        |           /finance/*         |
  |   Revoke: GPO 재배포    |        |           Condition:          |
  |                          |        |             aws:MultiFactor… |
  |                          |        |             aws:SourceIp=VPN |
  |                          |        |  Audit: CloudTrail (실시간)   |
  |                          |        |  Revoke: sts:AssumeRole 차단  |
  +--------------------------+        +------------------------------+
        ❌ Coarse-grained, Static          ✅ Fine-grained, Dynamic,
        ❌ Audit Lag (수일~수주)            ✅ Policy-as-Code (Terraform)
```

**왜 최소 권한이 필수인가?**
- **공격 표면(Attack Surface) 축소**: 권한이 적을수록 Lateral Movement 차단에 유리
- **내부자 위협(Insider Threat) 통제**: 최소 권한은 악의적 행위자가 접근할 수 있는 데이터 범위 자체를 제한
- **사고 대응(IR) 격리**: IAM Permission Boundary를 통해 단일 계정 침해가 Org 전체로 확산되는 것을 차단
- **컴플라이언스**: PCI-DSS 7.1, HIPAA §164.308(a)(4), GDPR Article 32, ISMS-P 인증 기준

- **📢 섹션 요약 비유**: "회사 사물함 키(전체 층 접근)와는 다르게, 클라우드 IAM 최소 권한은 **'오늘 3층 305호 회의실만 09:00–18:00에 입장 가능한 임시 출입 카드'**를 발급하는 것과 같다. 키 자체에 시간·위치·신원이 모두 새겨져 있어, 분실 시 피해가 그 회의실 하나로 한정된다."

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 IAM은 **인증(Authentication, "누구인가")** + **인가(Authorization, "무엇을 할 수 있는가")** 로 분리되며, 인가 결정은 다음 4가지 요소의 교집합(Boolean AND)으로 평가된다.

```text
[클라우드 IAM 4-Tuple 권한 평가 엔진 (Policy Evaluation Logic)]

              +-----------------------------------------------------+
              |            Authorization Decision (True/False)       |
              +--------------------------^--------------------------+
                                         |
        +--------------------------------+--------------------------------+
        |                                |                                |
   +----v-----+     +--------------v--------------+     +--------------v--------------+
   | Principal|     |        Action               |     |       Resource              |
   | (Subject)| AND |  (s3:GetObject,             | AND |  (ARN, Tag,                 |
   |          |     |   ec2:TerminateInstances)   |     |   Resource Graph)           |
   +----+-----+     +--------------+--------------+     +--------------+--------------+
        |                          |                                   |
   +----v------+              +----v------+                       +----v------+
   | User/IAM  |              | IAM API   |                       | ARN Path  |
   | Role/Srv  |              | Namespace |                       | s3:::prod |
   | /Group    |              | Wildcard  |                       | /data/*   |
   | +Tag+Sid  |              | * 제어    |                       | +Tag Env  |
   +-----------+              +-----------+                       +-----------+
                                         |
                              +----------v----------+
                              |     Condition       |  <--- AND 결합
                              |  • aws:MultiFactor  |
                              |  • aws:CurrentTime  |
                              |  • aws:SourceIp     |
                              |  • aws:PrincipalTag |
                              |  • aws:RequestTag   |
                              |  • s3:prefix        |
                              |  • kms:Encryption…  |
                              +---------------------+
```

### 정책 평가 알고리즘 (AWS IAM Policy Evaluation Logic 예)

```text
  Request ---> Identity-based Policy (사용자/역할)  -+
              Resource-based Policy (리소스)        |
              Permission Boundary                  +---> [Explicit DENY] > [Explicit ALLOW] > [Implicit DENY]
              SCP (AWS Organizations)              |       (Default: Deny)
              Session Policy (STS)                 |
                                                 -+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Principal (주체)** | 인증된 Entity(사용자, Role, Service, Federated User, Assumed Role) | `sts:AssumeRole` + External Trust Policy (SAML 2.0/OIDC), Session Token (v1/v2), `aws:PrincipalTag` 기반 ABAC |
| **Action (동작)** | API Operation(`s3:GetObject`, `ec2:StartInstances`) | Action namespace(`service:Action`), 와일드카드 `*` 제어(`iam:List*`는 Read-only), `NotAction`/`NotResource` 사용 금지(혼란 유발) |
| **Resource (대상)** | ARN(Amazon Resource Name) 또는 리소스 패턴 | `arn:aws:s3:::prod-finance/*` 형태로 path-level 제어, 태그(`aws:ResourceTag/Classification=Confidential`) 기반 동적 매칭 |
| **Condition (조건)** | 평가 컨텍스트 제약 | `Bool`, `NumericEquals`, `StringEquals`, `DateGreaterThan`, `IpAddress`, `ArnLike`, `ForAllValues:StringEquals`(세트 의미론) |
| **Permission Boundary** | Role/사용자에 부착되는 **최대 권한 천장(Ceiling)** | `iam:CreateRole`/`iam:PutUserPermissionsBoundary`로 부착, **Effective Permission = Identity Policy ∩ Boundary** (교집합) |
| **Service Control Policy(SCP)** | OU/계정에 적용되는 **Guardrail** | `organizations:AttachPolicy`로 부착, Member 계정이 **무엇을 할 수 있는지의 상한선** (Account-level) |
| **Session Policy** | `sts:AssumeRole` 시 임시 주입 | AssumeRole API 호출 시 inline policy 전달, 동일 Role을 Context별로 다른 권한으로 사용 |
| **Access Analyzer / IAM Policy Validator** | 정적 분석·자동 추천 | CloudTrail 로그 기반 미사용 권한 탐지(`Access Analyzer unused access`), JSON 정책 린팅(`iam-policy-json-to-terraform`) |

### 최소 권한 구현 핵심 메커니즘

**1) 정책 정제(Policy Refinement) 5단계**
1. **사용자 활동 로그 분석**: CloudTrail/Azure Activity Log를 기반으로 실제 호출된 API 추출
2. **액션 매핑**: 실제 호출 Action -> 최소 필요 Action으로 축소 (예: `s3:*` -> `s3:GetObject, s3:ListBucket`)
3. **리소스 ARN 축소**: `*` -> `arn:aws:s3:::company-prod-*/reports/*`
4. **Condition 추가**: 시간, IP, MFA, 디바이스 인증서, SAML 세션 attribute 기반 제약
5. **Permission Boundary 설정**: 실수에 대비한 안전망(Safety Net)

**2) 정책 시뮬레이터(IAM Policy Simulator)**
- `aws iam simulate-custom-policy` / `aws iam simulate-principal-policy`
- 특정 Principal이 특정 Action을 수행했을 때 `allowed | explicitDeny | implicitDeny` 결과 사전 검증

**3) ABAC(Attribute-Based Access Control) 패턴**
- `aws:PrincipalTag/Department = "Finance"` AND `aws:ResourceTag/Department = ${aws:PrincipalTag/Department}` 형태로 **태그 기반 동적 정책** -> 신규 리소스 추가 시 정책 수정 불필요

**4) 자격 증명 페더레이션 & Just-in-Time Provisioning**
- AWS IAM Identity Center(SSO) + Azure AD/Okta 통합 -> 사용자에게 영구 권한 미부여, **JIT(Just-In-Time) Role Assignment** + 자동 회수(Auto-revoke, 기본 1~8시간)

- **📢 섹션 요약 비유**: "최소 권한 정책은 **'자동차 렌트의 옵션 패키지'**와 같다. 풀옵션(FullAccess)을 빌려줄 필요 없이, **'서울 안에서만, 주말 포함 3일간, 1,500cc 차량만'** 처럼 **항목별로 콕 집어** 빌려주는 것. 운전자는 필요한 것만 받고, 렌트사는 사고 리스크를 통제한다."

---

## Ⅲ. 비교 및 연결

| 구분 | AWS IAM | Azure RBAC + ABAC | GCP IAM | On-Prem AD GPO |
| :--- | :--- | :--- | :--- | :--- |
| **정책 언어** | JSON (IAM Policy v2) | JSON (ARM Template) / Portal | YAML (IAM v3, Bindings) | GPO XML / ADM |
| **최소 권한 도구** | IAM Access Analyzer, IAM Policy Simulator | **PIM(Privileged Identity Management)**, Access Reviews | IAM Analyzer, Policy Intelligence | Least Privilege 모드 부재 |
| **Guardrail 메커니즘** | SCP (OU 레벨) | **Azure Policy / Management Group** | Org Policy Constraints | OU 단위 GPO |
| **Permission Boundary** | ✅ 지원 | ❌ 직접 부재 -> **Eligible Role + Activation 시간제**로 대체 | ❌ 직접 부재 -> IAM Conditions로 우회 | ❌ |
| **JIT 권한** | IAM Identity Center + STS | PIM (Time-bound activation) | IAM Conditions + Workforce Identity | ❌ (수동) |
| **세분성(Granularity)** | API Action 단위 (수만 개) | Data Action 포함 (Storage Blob Data Reader 등) | Permission 단위 (최대 14k) | GPO Setting 단위 (수백 개) |
| **평가 우선순위** | Explicit Deny > Allow > Implicit Deny | 동일 (System -> Custom -> Effective) | 동일 (Deny 우선) | 순차 LSDOU |
| **감사 추적** | CloudTrail (Management/Data Event) | Azure Activity Log + PIM History | Cloud Audit Logs (DATA_READ/WRITE/ADMIN) | Event Viewer (Security Log) |
| **컴플라이언스 매핑** | AWS Config Rules (`iam-root-access-key-check`, `iam-password-policy`) | Azure Blueprints, Regulatory Compliance Dashboard | Forseti/SCC (Security Command Center) | CIS Microsoft Benchmark |

### 관련 시스템 통합

- **IaC(Terraform/CloudFormation)**: IAM 정책을 **Git 관리** -> Code Review를 통한 Peer-reviewed Least Privilege (PR Bot: `iam-policy-json-to-terraform`, `cfn-policy-validator`)
- **CSPM(Cloud Security Posture Management)**: Wiz, Prisma Cloud, Trend Micro Cloud One -> 정책 위반/과다 권한 자동 탐지
- **CIEM(Cloud Infrastructure Entitlement Management)**: CyberArk Entitle, Sonrai Dig, Microsoft Defender for Cloud Apps -> 권한 그래프 시각화·최소권한 권고
- **PAM(Privileged Access Management)**: CyberArk Privileged Cloud, BeyondTrust, HashiCorp Boundary -> Break-glass 계정 통제, 세션 녹화

- **📢 섹션 요약 비유**: "AWS는 **'경비원 + 출입 카드 +CCTV'**, Azure는 **'역할 티어 + PIM 타이머 + 손목 밴드(MFA)'**, GCP는 **'조직도 + 태그 + 폴더 상속'**, 그리고 AD GPO는 **'옛날 회사에 새겨진 도장'**에 비유할 수 있다. 새 세 시스템은 모두 **위험 기반 적응형(Adaptive)** 이지만, AD GPO는 **정적 스탬프**라 변조가 어렵고 반응이 느리다."

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **Wildcard(`*`) 사용 감사**: `Action: "*"` 또는 `Resource: "*"` 사용 정책 비율을 IAM Access Analyzer / `Steampipe`로 조회 -> **5% 이하** 유지 (CIS AWS Foundations Benchmark v3.0 §1.16)
2. **Permission Boundary 적용 여부 확인**: 신규 Role 생성 시 `iam:CreateRole` 권한 정책에 `PermissionsBoundary` 필수 조건 부착(`iam:PermissionsBoundary` Condition Key)
3. **MFA·Source IP Condition 검증**: 모든 AssumeRole 정책에 `aws:MultiFactorAuthPresent=true` OR `aws:SourceIp` 화이트리스트 부재 시 거부. 비상용 Break-glass Role은 **별도 경보 + 상시 모니터링**.
4. **미사용 자격 증명 정리(90일 룰)**: Access Analyzer의 `find-unused-access` API로 90일 이상 미사용 키/Role/권한 자동 비활성
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 435 / 800

<- **이전**: [434. 클라우드 DNS Route53 Cloud DNS 관리](/studynote/13_cloud_architecture/06_exam_summary/434_cloud_dns_route53_cloud_dns_management/)
**다음**: [436. 클라우드 KMS 키 관리 암호화 서비스](/studynote/13_cloud_architecture/06_exam_summary/436_cloud_kms_key_management_encryption_service/) ->

---
