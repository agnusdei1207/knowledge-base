---
title: "Cloud Account Management Organization Landing Zone"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티 계정 클라우드 환경에서 거버넌스(IAM/SCP/Policy), 네트워크(Hub-Spoke/Transit Gateway), 보안(SIEM/Guardrails), 운영(Logging/Monitoring), 재무(FinOps/Tagging)를 **자동화된 표준 baseline**으로 통합한 Well-Architected 기반의 **계정 단위 셀(self-contained account unit)** 구조이다.
> 2. **가치**: AWS Control Tower 기준 신규 워크로드 온보딩 시간 **주 단위 -> 시간 단위(30분~1시간)**로 단축, 보안 사고 평균 탐지 시간 **MTTD 60% 이상 감소**, 계정 생성·폐기 자동화로 운영 인건비 **연 40~70% 절감**, SCP 기반 Preventive Guardrail로 **컴플라이언스 위반 사전 차단율 95% 이상** 달성.
> 3. **판단 포인트**: **단일 계정 vs 멀티 계정(OU 분할)**, **중앙 집중형(중앙 IT 거버넌스 팀) vs 분산형(셀프 서비스 Account Vending Machine)**, **Preventive(SCP/Deny) vs Detective(Config/Cloud Custodian) 가드레일 비중**, **Hub-Spoke vs Mesh 네트워크 토폴로지**, **단일 CSP Landing Zone vs Multi-Cloud Abstraction(Terraform/Backstage/Pulumi)**의 5대 아키텍처 결정이 TCO와 운영 복잡도를 결정한다.

---

## Ⅰ. 개요 및 필요성

클라우드 도입 초기 단계에서 가장 빈번하게 발생하는 실패는 **"Account Sprawl(계정 난립)"** 이다. SI(System Integrator)나 개별 사업부가 자체적으로 Root 계정을 발급받아 Shadow IT 형태로 클라우드를 운영하면, 중앙 거버넌스는 IAM 정책 누락, 네트워크 단편화, 비용 불투명, 컴플라이언스 공백이라는 4대 문제를 통제하지 못한다. 전통적 온프레미스 환경에서는 Active Directory OU(Organizational Unit)와 GPO(Group Policy)가 거버넌스의 중심이었으나, 클라우드에서는 계정(Account) 자체가 **가장 강력한 보안 경계(Strongest Security Boundary)** 이므로 이를 조직 단위로 분할·관리하는 새로운 운영 모델이 필요하다. AWS, Azure, GCP는 각각 Control Tower, CAF(Azure Landing Zone), GCP Landing Zone이라는 참조 아키텍처를 제공하며, 이들의 공통 핵심이 바로 **Cloud Landing Zone**이다.

```text
[ Before Landing Zone : Account Sprawl Chaos ]
                                                            +------------------+
   +----------+  +----------+  +----------+  +----------+ |  Finance Dept    |
   | SI-A Root|  | SI-B Root|  | Biz-1    |  | Biz-2    | |  Root Account    |
   | (자체 IAM|  | (Shadow  |  | (카드결제|  | (부서장  | |  (예산 분리)     |
   |  관리)   |  |  IT)     |  |  후 청구)|  |  개인계정)| +------------------+
   +----+-----+  +----+-----+  +----+-----+  +----+-----+         |
        |              |             |              |               |
        v              v             v              v               v
   +--------------------------------------------------------------------+
   |   ❌ No Centralized Identity  ❌ No Network Segmentation          |
   |   ❌ No Cost Visibility        ❌ No Compliance Baseline         |
   |   ❌ No Log Aggregation        ❌ No Tagging Enforcement         |
   +--------------------------------------------------------------------+

                              ⬇  ⬇  ⬇  Landing Zone 도입

[ After Landing Zone : Governed Multi-Account Structure ]
   +--------------------------------------------------------------------+
   |                   Organization Root (Master Payer)                  |
   |              [SCP / Tag Policy / Backup Policy 강제]                |
   +--------------------------------+-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            v                       v                       v
   +-----------------+    +-----------------+    +-----------------+
   |   OU : Security |    | OU : Infrastructure|  | OU : Workloads  |
   |   (Log Archive, |    | (Network Hub,    |  | (Dev / Stg /    |
   |    Audit, SecHR)|    |  Shared Services)|  |  Prod / Sandbox)|
   +--------+--------+    +--------+--------+    +--------+--------+
            |                      |                      |
       +----+----+            +----+----+            +----+----+
       v         v            v         v            v         v
   +------+  +------+    +------+  +------+    +------+  +------+
   | Log  |  |Audit |    | Net  |  |Shared|    |Prod-A|  |Dev-B |
   |Archive|  |Acct |    | Hub  |  |Svc   |    |App   |  |App   |
   +------+  +------+    +------+  +------+    +------+  +------+
        ^         ^            ^         ^            ^         ^
        +---------+------------+---------+------------+---------+
            SCP 적용 / Guardrail 강제 / Tag 기반 비용 집계
```

기존 **단일 계정(Single Account) + 다수 프로젝트** 모델은 초기에는 단순하지만, **계정 한도(Account Limit, 예: VPC 5개/리전, EIP 5개)** 도달, **부서간 IAM 격리 불가**, **PCI-DSS/개인정보보호법 등 규제 등급 분리 불가** 같은 한계로 100~200개 워크로드 규모에서 반드시 랜딩존으로 전환해야 한다.

- **📢 섹션 요약 비유**: 이전에는 가족 모두에게 **건물 마스터 키 1개**를 나눠주어 누가 뭘 했는지 추적이 불가능했다면, 랜딩존은 **각 가족에게 개별 현관 도어락 + 출입 기록 서버 + 공용 관리실 모니터링**을 한 번에 세팅해 주는 **아파트 신축 입주 패키지**와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

랜딩존은 일반적으로 **5계층 아키텍처(5-Layer Architecture)**로 설계된다. AWS Control Tower의 Account Factory, Azure의 CAF Ready 개념을 통합한 벤더 중립적 관점에서의 핵심 계층은 아래와 같다.

```text
[ Cloud Landing Zone 5-Layer Architecture ]

   +--------------------------------------------------------------+
   |  L5. Workload Layer (Business Applications)                  |
   |      - 계정별 Application Stack (EKS, RDS, Lambda)           |
   |      - IaC 모듈 (Terraform Module / Service Catalog)        |
   |      - 셀프서비스 배포 파이프라인 (CI/CD + AVM)              |
   +--------------------------------------------------------------+
   |  L4. Platform Layer (Shared Services)                        |
   |      - 중앙 Network Hub (Transit GW / VPC Peering / vWAN)    |
   |      - 공유 서비스 (ECR, CodeArtifact, KMS 중앙화)           |
   |      - Service Catalog / Account Vending Machine (AVM)      |
   +--------------------------------------------------------------+
   |  L3. Security & Compliance Layer (Cross-Account)             |
   |      - Log Archive Account (중앙 S3/Log Analytics)          |
   |      - Audit Account (CloudTrail Lake / Security Lake)       |
   |      - GuardDuty / Security Hub / Defender for Cloud         |
   |      - SCP / Azure Policy / Org Policy (Preventive)         |
   |      - Config / Cloud Custodian / SCC (Detective)           |
   +--------------------------------------------------------------+
   |  L2. Identity & Access Layer (Federated SSO)                 |
   |      - IdP (Azure AD / Okta / Google Workspace)             |
   |      - AWS IAM Identity Center / Azure AD PIM                |
   |      - Cross-Account Role + Permission Set / RBAC 매핑      |
   |      - JIT(Just-In-Time) Elevation / Break Glass 계정        |
   +--------------------------------------------------------------+
   |  L1. Foundation Layer (Organization & Billing)               |
   |      - Org Root / Management Group / Folder 계층구조        |
   |      - Consolidated Billing / Billing Account                |
   |      - Tag Policy / Backup Policy / AI Opt-Out Policy        |
   |      - Account Vending(자동 계정 생성) / Closeout(자동 폐기) |
   +--------------------------------------------------------------+
             ^              ^              ^              ^
             |              |              |              |
       IaC Pipeline    GitOps/CDK    Terraform/Backstage   Policy-as-Code
       (CI/CD)         ArgoCD/Pulumi  Crossplane/Pulumiverse
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Organization Root / MG / Folder** | 전체 계정·정책 계층의 최상위 컨테이너 | AWS Organizations, Azure Management Group, GCP Folder. SCP(Service Control Policy), Azure Policy, Org Policy를 트리 형태로 상속. Root에 **AI services opt-out**, **Region deny(블루밍턴 외 리전 차단)** 등 글로벌 베이스라인 적용 |
| **Account Vending Machine (AVM)** | 신규 워크로드 계정의 자동 발급·폐기 | AWS Service Catalog + Lambda/Step Functions, 또는 Terraform `aws-organization-module`. 입력 변수(사업부, 환경, VPC CIDR, OU 경로)만 주면 **30분 내 표준 준수 계정** 생성. 폐기 시 **S3 Glacier Lock + Detective Control**로 데이터 보존 후 90일 후 삭제 |
| **Identity Federation (SSO)** | 중앙 IdP 기반 페더레이션 인증 | SAML 2.0 / OIDC / SCIM 2.0 프로토콜. AWS IAM Identity Center, Azure AD -> AWS IAM Role 매핑. Permission Set이라는 **권한 번들**로 Admin/Developer/ReadOnly/PIM-Approver 등 7~15개 역할 표준화 |
| **Network Hub (Transit Architecture)** | 계정간 east-west 트래픽과 온프레mise 연동 중앙화 | AWS Transit Gateway(TGW) + RAM(리소스 액세스 관리), Azure vWAN Hub, GCP NCC(Network Connectivity Center). Direct Connect / ExpressRoute / Interconnect는 **단일 또는 이중**으로 Hub 계정에 종단, **TGW Share**로 전 계정 전파. **IPAM(중앙 IP 주소 관리)**으로 CIDR 충돌 방지 |
| **Guardrails (Preventive + Detective)** | 컴플라이언스 위반 사전 차단·사후 탐지 | **Preventive**: SCP `Deny:ec2:RunInstances` 시 `aws:RequestTag/Env != [prod, dev, stg]` 조건, `Deny:iam:CreateUser`(Root 계정 직접 생성 금지). **Detective**: AWS Config Rule(`ec2-instance-no-public-ip`, `s3-bucket-public-read-prohibited`), Security Hub Standards(CIS AWS Foundations v1.4, PCI-DSS v3.2.1), GCP Security Health Analytics |

**핵심 동작 메커니즘(SCP 상속과 평가 순서)**:
AWS Organizations의 정책 평가는 **위에서 아래로 누적 AND**, **명시적 Deny 우선**이라는 2원칙을 따른다. 예를 들어 Root SCP가 `Deny:ec2:RunInstances in ap-northeast-1 외`이고, OU `Workloads/Prod` SCP가 `Deny:RDS:DeleteDBInstance`이면 Prod 계정의 EC2는 N.Virginia에서 못 띄우지만 RDS 삭제는 Prod OU에서만 차단된다. **명시적 Allow는 부모의 Deny를 override 할 수 없다.** 기술사 시험 단골 출제 포인트다.

**계정 폐기 시의 데이터 보존 정책**: AVM으로 계정을 삭제할 때 즉시 hard delete하지 않고, Log Archive 계정으로 **S3 Object Lock(Governance/Compliance 모드)** 또는 **AWS Backup Vault Lock**을 통해 7년치 로그를 WORM(Write Once Read Many)으로 보존한다. 이는 전자금융감독규정 제 22조(전자금융기록물 보존기간) 대응이다.

- **📢 섹션 요약 비유**: 랜딩존은 마치 **대형 호텔의 프런트 데스크 시스템**과 같다. 손님(워크로드)이 오면 신분증(IdP SSO) 확인, 적정 층(OU) 배정, 객실 키(Account) 발급, CCTV(GuardDuty)·소화설비(Config Rule)·미니바 정산(Tag Billing)까지 **표준화된 체크인 절차**가 자동 적용된다.

---

## Ⅲ. 비교 및 연결

| 구분 | AWS Control Tower | Azure Landing Zone (CAF) | GCP Landing Zone | 자체 구축(Landing Zone DIY) |
| :--- | :--- | :--- | :--- | :--- |
| **거버넌스 엔진** | SCP + AWS Config Rules + Lambda 기반 Customization | Azure Policy + Blueprints(Deprecated -> Deployment Stack) + Activity Log | Org Policy + Org Policy Constraints + Cloud Asset Inventory | 직접 구현 (Terraform / Pulumi / Crossplane) |
| **계정 자동화** | Account Factory (Service Catalog 기반) | Subscription Vending (Alzheimers Accelerator / BICEP) | Folder + Project Factory (Terraform 모듈) | AVM 직접 코딩 (Lambda + DynamoDB State) |
| **네트워크 표준** | VPC + TGW 샘플 (Control Tower Reference) | Hub-Spoke vWAN Topology Blueprint | Shared VPC + NCC(Network Connectivity Center) | 사용자 정의 (IPAM + Transit 토폴로지 직접) |
| **ID 연동** | IAM Identity Center + AWS Organizations | Entra ID (Azure AD) PIM + Management Group RBAC | Cloud Identity / Workforce Identity Federation | 외부 IdP 직접 SAML/OIDC 페더레이션 |
| **표준 가드레일 수** | Mandatory(7) + Strongly Recommended(25) + Elective(50+) | Azure Policy Initiative(PCI, ISO27001 내장) | CIS + PCI Constraints (Google Cloud Security Foundations) | 직접 작성 (수십~수백 개 Policy-as-Code) |
| **구축 기간(중견기업 기준)** | 1~2주 (Control Tower 가드온) | 2~4주 (CAF Ready + Hub-Spoke) | 2~3주 | 3~6개월 + 운영 인력 상시 |
| **TCO(3년)** | 중간 (Control Tower 자체는 무료, 백엔드 리소스 비용 발생) | 중간 (Subscription 자체 무료, Blueprint 리소스 비용) | 낮음 (네이티브 통합 우수) | 높음 (자체 인력·도구 비용) |
| **확장성** | 리전 30+ 개 / 계정 1만개 (Organizations 한도) | 테넌트 1개 / MG 10000개 / 구독 10000+ | Folder 깊이 무제한 / 프로젝트 수 무제한(쿼터 있음) | 무제한(설계에 따라) |
| **Multi-Cloud 대응** | ❌ (AWS Only) | ❌ (Azure Only) | ❌ (GCP Only) | ⭕ (Terraform/Backstage/Crossplane 활용) |

**연계 기술 맵**:
- **Infrastructure as Code**: Terraform(가장 보편), Pulumi(타입 안전), AWS CDK(언어 네이티브), Crossplane(Kubernetes 기반) — 이 중 **Crossplane + ArgoCD** 조합이 **GitOps 기반 멀티 클라우드 Landing Zone**의 최신 트렌드다.
- **Policy-as-Code**: OPA(Open Policy Agent) / Rego, HashiCorp Sentinel, Cloud Custodian(Python DSL) — CSP 네이티브 정책의 한계를 넘어 **CSP-Agnostic 정책 통합** 가능.
- **FinOps 도구**: CloudHealth, Vantage, Kubecost, Cloudability — 랜딩존의 Tag Policy와 연동하여 **BU별·환경별·서비스
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 505 / 800

<- **이전**: [504. 클라우드 태그 관리 리소스 분류 전략](/studynote/13_cloud_architecture/06_exam_summary/504_cloud_tag_management_resource_classification/)
**다음**: [506. 멀티 어카운트 전략 AWS Organizations](/studynote/13_cloud_architecture/06_exam_summary/506_multi_account_strategy_aws_organizations/) ->

---
