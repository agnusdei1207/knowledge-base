---
title: "DevOps Environment Audit Automation"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevOps 파이프라인(Plan->Code->Build->Test->Release->Deploy->Operate->Monitor)의 모든 산출물(IaC, 컨테이너 이미지, SBOM, 배포 매니페스트, 정책 로그)을 Policy-as-Code(OPA/Rego, Sentinel, Kyverno) 기반으로 기계 판독 가능한 형태로 자동 검증하여, 감리 통제 항목(Control Objective)을 Continuous Controls Monitoring(CCM) 수준으로 전환하는 기법이다.
> 2. **가치**: 전통 수동 감리의 평균 120~180 영업일 소요를 72시간 이내의 자동 증적 수집(Automated Evidence Collection)으로 단축하며, ISO 27001·SOC2·PCI-DSS·전자금융감독규정 등 다중 규제 매핑 시 중복 작업 약 65% 제거, 감리 통제 미흡(Coverage Gap) 발견 시점 MTTD(Mean Time To Detect)를 30일->수 분으로 단축한다.
> 3. **판단 포인트**: (a) Policy Engine 선택 시 Rego(Datalog 기반) vs Sentinel(Go-like) vs Cedar(Logic-programming) 트레이드오프, (b) Shift-Left(이슈 발생 시점) vs Shield-Left(배포 차단 시점) 적용 균형, (c) Attestation(서명·해시) 기반 Supply Chain 보장과 Runtime Admission Control(Kyverno/OPA Gatekeeper)의 이중 계층 설계가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적인 정보시스템 감리는 ① 감리인 도임 -> ② 통제 항목(Control Item)별 증적(Evidence) 수기 수집 -> ③ 인터뷰·점검표 작성 -> ④ 결론 도출의 4단계 워터폴 방식으로 진행되어, 통상 1차 시스템 1,200~2,000개 통제 항목에 대해 4~6개월이 소요된다. 그러나 클라우드 네이티브 환경에서 Kubernetes 매니페스트가 하루 수십 회, Terraform 모듈이 주 수백 회 변경되는 상황에서, **"Point-in-time Audit(특정 시점 스냅샷)"** 패러다임은 본질적으로 작동하지 못한다. 감리가 끝나는 시점에는 이미 검증 대상 시스템이 완전히 변모(snapshot rot)되어 있다.

DevOps 환경 감리 자동화 검증(DevOps Environment Audit Automation, 이하 DEAA)은 이러한 문제를 해결하기 위해 **(1) 통제를 코드로 표현(Policy-as-Code, PaC)**, **(2) 빌드·배포 파이프라인 자체에 통제 게이트(Policy Enforcement Point, PEP)를 삽입**, **(3) 모든 의사결정 로그를 불변 저장소(WORM, 예: AWS S3 Object Lock)에 attestation 형태로 보존**하는 3축 통합 프레임워크이다.

```text
[전통 감리]  수동 샘플링 -> 4~6개월 소요 -> 결과 무효화 위험
                v 진화
[DEAA]      통제 코드화 + 자동 PEP + 불변 증적체인
   +--------------------------------------------------------------+
   |  Source  | Build | Test | Stage | Prod |   Audit Plane      |
   |  (Git)   |(CI)   |(QA)  |(Pre-Prod)|(Live)|  (Always-on)     |
   |          |       |      |        |     |                    |
   |  v IaC  | v SBOM|vSAST |v Admission|v Drift|   v Continuous  |
   |  Scan   | Gen   |DAST  | Control | Detect|     Monitoring   |
   |  v      | v Sign |v CVE |v OPA   |v eBPF |   v Compliance   |
   |  Trivy  | Cosign |SBOM  | Gatekeepr| Falco|     Dashboard   |
   +--------------------------------------------------------------+
                       |
                       v
        +----------------------------------+
        |  Immutable Evidence Store (WORM) |
        |   +- in-toto Attestation        |
        |   +- Sigstore Rekor(Log)        |
        |   +- SIEM -> SOAR -> Audit Report |
        +----------------------------------+
```

기존 패러다임 대비 핵심 변화는 **"증적(Evidence)을 사람이 만들면 비용이 들고, 위조 가능하며, 사후에야 존재한다"**는 전제에서 **"증적은 시스템이 암호학적 서명(SHA-256 + Sigstore/RFC 3161 TSA)으로 자동 생성하며, 정책 위반 자체가 빌드 차단으로 이어지므로 사후 위반이 구조적으로 불가능"**한 패러다임으로의 전환이다.

- **📢 섹션 요약 비유**: 전통 감리가 "1년에 한 번 총 들고 다니며 현장을 둘러보는 건강검진"이라면, DEAA는 **"웨어러블 심전도 모니터처럼 24시간 심장 박동을 측정해 이상이 감지되는 즉시 알람이 울리는 상시 모니터링 시스템"**과 같다. 심전도 데이터(WORM 저장된 attestation)는 의사가 필요할 때 언제든 불러 검토할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DEAA의 참조 아키텍처는 ISO/IEC 42001(AI), ISO 27001:2022(Annex A 5.37~5.41 개발 통제), NIST SSDF(Secure Software Development Framework SP 800-218), SLSA v1.0(Build L3), 그리고 가이드라인으로는 CIS Software Supply Chain Guide, OWASP CICD-SEC-01~10, CISA SBOM 최소요소(Type·Version·Supplier·Dependency 관계)를 상호 매핑한 5-Layer Audit Plane 위에 구성된다.

```text
[DEAA 5-Layer Reference Architecture]
-------------------------------------------------------------------
 Layer 5  |  Governance & Reporting Layer
          |  +-------------------------------------------------+
          |  | Compliance Scorecard | Risk Heatmap | Audit PDF |
          |  |  - ISO 27001 Ctrl Map |  - CVSS > 7 | Gen via   |
          |  |  - SOC2 CC-series     |  - Drift %  | Jinja2    |
          |  +-------------------------------------------------+
-------------------------------------------------------------------
 Layer 4  |  Continuous Controls Monitoring (CCM)
          |  +--------------------------------------------------+
          |  |  Evidence Aggregator ->  Time-Series DB (Prometheus)|
          |  |  - Control State(t)  = f(policy_eval, runtime_obs)|
          |  |  - Violation EventBus (NATS/Kafka) -> SOAR          |
          |  +--------------------------------------------------+
-------------------------------------------------------------------
 Layer 3  |  Policy Decision Point (PDP) & Enforcement Point (PEP)
          |  +----------------+    +--------------------------+
          |  | OPA / Rego     |◄--►|  Kyverno (K8s)           |
          |  | Cedar (AWS)    |    |  Gatekeeper (K8s)        |
          |  | Sentinel (TF)  |    |  Conftest (YAML)         |
          |  +----------------+    +--------------------------+
-------------------------------------------------------------------
 Layer 2  |  Software Supply Chain Integrity
          |  +--------------------------------------------------+
          |  |  Source -► SLSA L3 Build -► SBOM(CycloneDX/SPDX) |
          |  |  -► Cosign Sign -► Rekor Transparency Log        |
          |  |  -► in-toto Attestation (predicate: vuln-scan)   |
          |  +--------------------------------------------------+
-------------------------------------------------------------------
 Layer 1  |  Infrastructure & Runtime Telemetry
          |  +----------------+  +------------+  +------------+
          |  | Terraform/Cloud |  | K8s API    |  | eBPF/Falco |
          |  | Formation Drift |  | Audit Log  |  | Runtime    |
          |  +----------------+  +------------+  +------------+
-------------------------------------------------------------------
```

각 계층의 동작 원리를 보다 자세히 살펴보자.

### 1) Layer 1 — 원천 데이터 수집 계층

인프라 변경 사실(Change Truth)은 세 곳에서 발생한다: (a) **IaC Repository**(Git commit SHA), (b) **Cloud Provider의 State Store**(Terraform State, AWS CloudTrail, Azure Activity Log), (c) **Kubernetes Control Plane**(etcd). 이 세 원천의 일치 여부가 감사 통제 A.8.32(Change Management)의 핵심이다. **Drift Detection**은 `terraform plan -detailed-exitcode` 또는 `driftctl`로 IaC 의도(Intent)와 실세계 상태(Actual State)의 차이를 산출하며, 이 결과 자체가 하나의 통제 증적이 된다.

Runtime 계층에서는 eBPF 기반 Falco가 Syscall 이벤트를 스트리밍하여 컨테이너 내부의 비정상 행위(예: `/bin/bash` in production pod, outbound to non-allowlisted CIDR)를 탐지한다. 이 이벤트 로그에는 Kubernetes Namespace, Pod UID, Container Image SHA, cgroup ID가 태그로 부착되어, **증적 단위(Evidence Unit) = (행위자, 행위, 시점, 자원)**의 4-tuple을 만족한다.

### 2) Layer 2 — Supply Chain Integrity 계층

**SLSA(Supply-chain Levels for Secure Artifacts) v1.0**의 Level 3 요건은 빌드 환경의 격리(Hermetic, Two-party review, Hardened runner)와 출처 무결성(Provenance)이다. **in-toto Attestation**은 `predicateType`(예: `https://cyclonedx.org/bom`, `https://slsa.dev/verification/v1`)과 `subject[].digest.sha256`을 갖는 JSON-LD 형태의 진술서로, Cosign이 이를 Sigstore Rekor 투명 로그(append-only Merkle Tree)에 기록한다. Rekor의 inclusion proof는 **"X 시점에 Y 해시값의 attestation이 제출되었다"**는 시간적 증명(Time-Stamp Authority, RFC 3161)을 제공한다.

SBOM(Software Bill of Materials)은 CISA 최소요소인 CycloneDX 1.5 또는 SPDX 2.3 포맷을 따른다. SBOM 내부의 의존성 그래프(Dependency Graph)는 VEX(Vulnerability Exploitability eXchange) 문서와 결합되어, "해당 CVE가 우리 빌드에 영향이 있는가(Reachability Analysis)"를 판단하는 근거가 된다.

### 3) Layer 3 — Policy Decision / Enforcement 계층

핵심 알고리즘으로 **OPA(Open Policy Agent)**는 Rego라는 Datalog-inspired 언어를 사용해 정책 표현식 `input` (JSON 형태의 평가 대상)과 `data` (외부에서 주입되는 참조 데이터, 예: 허용된 이미지 레지스트리 목록)를 받아 `result = { "allow": bool, "violations": [...] }`를 반환한다. 평가 시점은 크게 4종: ① **PR Time**(GitHub Action의 `opa test`, `conftest verify` -> Merge 차단), ② **Build Time**(Tekton/Chains에서 in-toto predicate 생성 직전), ③ **Admission Time**(kube-apiserver의 ValidatingAdmissionWebhook, 평균 레이턴시 < 50ms), ④ **Runtime**(Falco output -> OPA input 재평가 -> SOAR 액션).

**Kyverno**는 Kubernetes CRD 네이티브 정책 엔진으로, `validate`, `mutate`, `generate`, `verifyImages` 4가지 액션을 지원한다. `verifyImages`는 컨테이너 이미지의 Cosign 서명을 자동 검증하여 unsigned image 배포를 차단한다. **Sentinel**(HashiCorp)은 Terraform Cloud, Vault, Nomad에 임베드되며, 정책에 따라 `soft-mandatory`, `hard-mandatory`를 구분한다(soft는 override 가능, hard는 불가).

### 4) Layer 4 — Continuous Controls Monitoring(CCM) 계층

CCM은 **통제 상태의 시간 함수** `S_c(t) ∈ {0, 1, 2, 3}` (0=Failed, 1=At-Risk, 2=Compliant, 3=Verified)를 정의하고, 매 평가 사이클(예: 5분)마다 갱신한다. Open Policy Administration Layer(OPAL)는 OPA의 데이터 평면과 정책 평면을 분리하여, 정책 변경을 OPA 인스턴스에 핫리로드(보통 3초 내)하는 채널을 제공한다. CCM의 출력은 Prometheus 메트릭(`opa_policy_decision_total{policy="...",result="deny"}`)로 노출되어 Grafana 대시보드에서 시계열로 조회 가능하며, 90일 보관 후 WORM 스토리지로 이전된다.

### 5) Layer 5 — Governance & Reporting 계층

감사 보고서는 **자동 생성**된다. Jinja2 + LaTeX 템플릿이 다음을 결합: (i) 정책 평가 이력, (ii) SBOM, (iii) in-toto attestation, (iv) Runtime incident, (v) 사람의 승인 기록(e-signature, PKI 기반). PDF는 PAdES(ETSI EN 319 142) 표준에 따라 디지털 서명되어, 감리인이 검토 후 추가 서명할 수 있다. SOC2 Type II 보고서 자동 생성 도구로는 **Drata, Vanta, Secureframe, Tugboat Logic**(이 분야를 "Trust Assurance"라 칭함)이 있으며, 이들은 100여 SaaS(Okta, GitHub, AWS, GCP) API를 통합하여 통제 항목을 자동 폴링한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IaC Scanner** | Terraform/CloudFormation 정적 분석, 드리프트 탐지 | Checkov(2,000+ 정책, Python AST 분석), tfsec(Golang, Go AST), Terrascan(OPA 기반, Rego 정책 500+), driftctl(RFC 1918 망 외 IP 식별, JSON diff). 평가: 평균 1,000 LoC IaC를 8~15초 스캔 |
| **Policy Engine (PDP)** | 정책 표현식 평가, 결정 반환 | OPA v0.60+(Rego v1), HashiCorp Sentinel v0.21+, AWS Cedar v4.0+, Kyverno v1.11+. 평가 모델: Allow/Deny + Reason + Metadata(통제 매핑, 예: `control_id="ISO27001-A.8.32"`) |
| **Admission Controller (PEP)** | K8s API 호출 시 정책 강제 | OPA Gatekeeper(v3, mutation+validation), Kyverno(Native CRD), AWS EKS Pod Identity webhook. latency P99 < 80ms, 5xx error 시 Fail-Open vs Fail-Closed 정책 결정 필요 |
| **SBOM Generator** | 빌드 산출물 의존성 트리 생성 | Syft(Anchore), CycloneDX-gomod, cdxgen, SPDX SBOM Generator. 출력 포맷: CycloneDX 1.5, SPDX 2.3, 내부 RDF 변환 |
| **Attestation Signer** | 진술서에 서명 및 투명 로그 기록 | Sigstore Cosign(키리스 서명, OIDC + Fulcio CA), Rekor(append-only Merkle tree, 1.4M+ entries), in-toto-golang v0.9, Witness(루트 정책) |
| **Runtime Detector** | 컨테이너 비정상 행위 탐지 | Falco v
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 492 / 600

<- **이전**: [491. 애자일 프로젝트 감리 방법론](/studynote/11_design_supervision/06_exam_summary/491_agile_project_audit_methodology)
**다음**: [493. 마이크로서비스 감리 분산 시스템 진단](/studynote/11_design_supervision/06_exam_summary/493_microservice_audit_distributed_system/) ->

---
