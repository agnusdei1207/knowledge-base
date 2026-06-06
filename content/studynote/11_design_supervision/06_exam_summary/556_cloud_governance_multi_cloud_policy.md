---
title: "Cloud Governance Multi Cloud Policy"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티 클라우드 거버넌스는 AWS Organizations(SCP), Azure Policy(Blueprint), GCP Org Policy(CI) 등 CSP 고유 정책 엔진과 Open Policy Agent(OPA/Rego), HashiCorp Sentinel 같은 중립적 PaC(Policy as Code) 엔진을 **이중 레이어**로 추상화하여, 이기종 CSP 환경에서 보안·컴플라이언스·비용 통제를 **declarative 정책 선언 -> 자동화된 enforcement -> continuous compliance** 사이클로 통합하는 프레임워크이다.
> 2. **가치**: FinOps 성숙도 모델( crawl-walk-run ) 기반 성숙도 1단계 대비 운영비 20~35% 절감, 정책 위반 탐지 MTTD 12시간 -> 5분(99.3% 단축), 컴플라이언스 감사 준비 시간 70% 감소, CSP 종속 지수(Vendor Lock-in Index) 50% 저감을 통한 협상력 확보가 가능하다.
> 3. **판단 포인트**: 추상화 레이어 깊이(CSP-native vs. CNAPP/CSPM), 정책 전파 지연(SCP 적용 글로벌 전파 ~15분, Azure Policy 30분, GCP Org Policy ~수 분), Egress 비용(Inter-region $0.02/GB, Inter-cloud $0.09/GB), 데이터 주권(K-ISMS, GDPR Schrems II, 클라우드컴퓨팅법 §23 개인정보 처리 제한), 워크로드별 최적 CSP 선정(예: GPU -> GCP/AWS, MSSQL/AD -> Azure, 국내 공공·금융 -> NCP/KT Cloud) 이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT가 단일 CSP(AWS-only, Azure-only)에서 멀티·하이브리드 클라우드로 전환됨에 따라, **N개의 클라우드 × M개의 계정/구독/프로젝트 × K명의 개발자** 가 만들어내는 거버넌스 표면적은 N×M×K 로 기하급수적으로 증가한다. Gartner는 2025년 엔터프라이즈의 75%가 멀티/하이브리드 클라우드를 운영할 것으로 예측하며, 한국은 2023년 「클라우드컴퓨팅법」 시행과 금융·공공부문의 클라우드 이용 가이드라인(금감원, 과기정통부)으로 인해 **국내외 이중 CSP 운영** 이 사실상 표준이 되었다.

특히 (1) M&A 시 피인수사의 상이한 클라우드 스택 흡수, (2) GPU 자원의 글로벌 가용성(AWS P5, GCP H100, Azure ND H100 v5) 확보, (3) 데이터 주권 규제(개인정보보호법 §29, EU Schrems II), (4) 베어메탈 락인 회피를 통한 가격 협상력 확보가 멀티 클라우드의 **필수 동인** 이 된다. 그러나 멀티 클라우드는 동시에 **Shadow IT**, **Egress fee 폭증**, **정책 불일치로 인한 감사 실패**, **상호 운용성 부재(예: EKS ↔ AKS ↔ GKE)** 라는 4대 거버넌스 부채를 야기한다.

기존 단일 클라우드 거버넌스는 CSP가 제공하는 콘솔(예: AWS Management Console) + IAM + Organizations SCP로 충분했으나, 멀티 클라우드에서는 **CSP 간 정책 모델의 비동질성**(AWS: JSON SCP, Azure: ARM/PolicyDefinition JSON, GCP: YAML/CEL) 으로 인해 동일 정책(예: "S3는 반드시 KMS로 암호화")을 N번 작성·유지보수해야 하는 **Policy Sprawl** 문제가 발생한다.

```text
                  +-----------------------------------------+
                  |        Cloud Center of Excellence       |
                  |   (CCoE) + FinOps Practice + SecOps     |
                  +--------------------+--------------------+
                                       | Policy as Code (Rego/Sentinel)
                                       | Unified Tagging Schema (ISO 17263)
                                       | Cross-cloud SCIM Identity Sync
                +----------------------+----------------------+
                |                      |                      |
        +-------v--------+    +--------v--------+    +-------v--------+
        |   AWS  [Org]   |    |  Azure  [MG/TP] |    |  GCP  [Folder] |
        |  12계정/4OU    |    |  8구독/3MG      |    |  6프로젝트/3F |
        |  SCP / Control |    |  Policy/Blueprint|    |  OrgPolicy/CI |
        |  Tower / Guard |    |  Defender/MCAS  |    |  SCC/Chronicle |
        +----------------+    +-----------------+    +----------------+
                ^                      ^                      ^
                |       Observability Bus (OpenTelemetry)     |
                |       Cost & Usage Bus (CUR+AzureMCA+FOCUS)|
                +--------------+-------------------------------+
                               |
                  +------------v------------+
                  |   CNAPP / FinOps Hub    |
                  |  (Wiz, Prisma, Vantage) |
                  +-------------------------+
```

- **📢 섹션 요약 비유**: 단일 클라우드는 "한 호텔 체인의 매니저" 였다면, 멀티 클라우드 거버넌스는 "롯데·메리어트·아코르 3개 체인의 객실·식음료·보안 규칙을 똑같이 강제하는 통합 본사"와 같다. 본사가 없으면 각 호텔이 제멋대로 운영되어 고객(규제기관) 불만이 폭발한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

멀티 클라우드 거버넌스 아키텍처는 **4개 레이어 + 1개 피드백 루프**로 구성된다. 핵심은 모든 정책을 **declarative 코드**로 선언하고, **CI/CD + Admission Control + Periodic Audit**의 3축으로 enforcement 하는 것이다.

```text
   +----------------------------------------------------------------+
   |                  L4. Policy Definition Layer                   |
   |   +----------+  +----------+  +----------+  +----------+      |
   |   | Rego(OPA)|  | Sentinel |  | Cedar    |  | Cloud    |      |
   |   | 정책 Repo|  |  (TFC)   |  | (AWS WA) |  | Custodian|      |
   |   +----+-----+  +----+-----+  +----+-----+  +----+-----+      |
   +--------+-------------+-------------+-------------+-------------+
            |             |             |             |
   +--------v-------------v-------------v-------------v-------------+
   |      L3.  IaC & GitOps Orchestration (Terraform Cloud,         |
   |            Spacelift, Atlantis, ArgoCD, Crossplane)            |
   +--------+-------------------------------------------------------+
            | plan / apply / drift detection
   +--------v-------------------------------------------------------+
   |      L2.  Enforcement Layer (CSP-native + 3rd Party)           |
   |   +--------------+  +--------------+  +--------------+         |
   |   | SCP/CTRLTWR  |  | Azure Policy |  | Org Policy   |         |
   |   | IAM Identity |  | MG Inherit   |  | Folder Hier. |         |
   |   | Center       |  | Blueprint    |  | IAM Deny     |         |
   |   +--------------+  +--------------+  +--------------+         |
   |   +  OPA Gatekeeper / Kyverno (K8s admission)                  |
   |   +  CSPM/CNAPP (Wiz, Prisma Cloud, Defender for Cloud)       |
   +--------+-------------------------------------------------------+
            | runtime events
   +--------v
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 556 / 600

<- **이전**: [555. AI 거버넌스 윤리 규제 프레임워크](/studynote/11_design_supervision/06_exam_summary/555_ai_governance_ethics_regulatory_framewor)
**다음**: [557. 오픈소스 거버넌스 라이선스 관리](/studynote/11_design_supervision/06_exam_summary/557_open_source_governance_license_managemen/) ->

---
