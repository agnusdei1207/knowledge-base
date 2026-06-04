---
title: "402. DevSecOps 보안 내재화 파이프라인 (DevSecOps Security Integration Pipeline)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevSecOps 보안 내재화 파이프라인은 SAST/DAST/SCA/IAST/Secrets·Container·IaC·SBOM·Supply Chain Signing·Policy-as-Code·Runtime Security 도구를 CI/CD 단계(Plan->Code->Build->Test->Release->Deploy->Operate)에 정책 기반 게이트(OPA/Kyverno/SLSA L3+)로 종단 통합하여, 취약점·악성코드·서명 무결성·컴플라이언스 위반을 **Shift-Left + Shield-Right** 양방향으로 자동 차단·추적·회수하는 소프트웨어공학 보안 체계이다.
> 2. **가치**: Gartner 조사(2024) 기준 보안 내재화 조직은 MTTR(평균 취약점 해결시간)이 65% 단축(32일->11일), 보안 결함 유출률 73% 감소, 컴플라이언스 증빙 자동화로 감사비용 약 40% 절감이 가능하며, SBOM·SLSA·VEX·Sigstore 기반 Supply Chain 무결성 보증을 통해 SBOM 의무화(美 EO 14028, EU CRA, 한국 전자정부법 개정안)에 대응한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **Pipeline Throughput vs Security Coverage**(전 단계 스캔은 빌드시간 30~120% 증가), ② **Shift-Left 정밀도 vs 노이즈**(False Positive 60% 이상 시 개발자 신뢰 붕괴), ③ **Agent-based vs Agentless 런타임 보안**(Falco vs eBPK-based Tetragon의 성능/가시성 균형), ④ **중앙 정책(OPA) vs 셀프서비스(Kyverno)**, ⑤ **Pull Request 게이트 vs Merge 후 Backport 스캔** 전략 선택이며, **기술사 결단 포인트**는 "Critical/High 취약점의 빌드 차단 임계값"과 "Signature Verification 실패 시 Fail-Open vs Fail-Closed" 정책이다.

---

## Ⅰ. 개요 및 필요성

전통적 SDLC(Software Development Life Cycle)에서 보안은 릴리즈 직후 또는 운영 단계에서 **Penetration Test·수동 코드 리뷰·WAF·NVA** 형태로 **End-of-Pipeline**에 부착되었다. 이는 ① 평균 10,000 LoC 당 1건의 Critical 취약점이 운영 환경까지 전이(Veracode 2023 State of Software Security), ② 컨테이너 이미지·서드파티 라이브러리·IaC 모듈 등 **SBOM(Software Bill of Materials)** 미관리로 인한 **Supply Chain Attack**(SolarWinds, Codecov, 3CX, xz-utils 백도어, Log4Shell) 노출, ③ 컴플라이언스(ISO 27001, PCI-DSS 4.0, ISMS-P, CSAP, K-ISMS) 요구사항이 수동 점검으로 처리되어 **릴리즈 사이클 2~6주 지연**을 야기했다. 또한 클라우드 네이티브 환경으로의 전환(Kubernetes, Microservice, Service Mesh, GitOps)으로 공격면(Attack Surface)이 **API·컨테이너·Service Account·IAM Role·Secret**로 폭증하면서, **Zero Trust** 원칙이 CI/CD 자체에도 적용되어야 하는 상황이다.

DevSecOps 보안 내재화 파이프라인은 **"보안은 팀의 책임이 아니라 파이프라인의 책임"**이라는 문화적 전환(People) + **자동화된 검증 도구**(Process) + **SBOM·Sigstore·Policy-as-Code 기반 인프라**(Technology)를 통해, 코드 커밋 시점부터 런타임까지 **모든 산출물(Artifact)이 정책·서명·취약점 기준을 통과해야만 다음 단계로 진행**하는 **Quality Gate** 체계를 구축한다. NIST SSDF(Secure Software Development Framework, SP 800-218)·OWASP SAMM v2·SLSA(Supply-chain Levels for Software Artifacts) v1.0·CNCF Security TAG Whitepaper가 이를 위한 표준 참조 모델이며, 한국에서는 행정안전부 **클라우드 보안 인증(CSAP)**, KISA **DevSecOps 도입 가이드(2023)**, **국정원 국가·공공기관 소프트웨어 개발보안 가이드**가 적용 프레임워크로 활용된다.

```text
+------------------------------------------------------------------------------+
|                       DevSecOps 보안 내재화 파이프라인 (개념)                  |
|                                                                              |
|  [Legacy: Bolt-on Security]              [DevSecOps: Built-in Security]       |
|                                                                              |
|  Plan -> Code -> Build -> Test -> Deploy       Plan(S) -> Code(S) -> Build(S)      |
|                         |                            v                       |
|                      [Sec]  <- 사후 검사         Test(S) -> Release(S)          |
|                         |                            v                       |
|                       Operate                    Deploy(S) -> Operate(S)       |
|                                                  v                           |
|                                              Monitor(S)                      |
|                                                                              |
|   (S) = Security Activity 내재화 ----------------------------------------►   |
|   +- Threat Modeling (pytm/Threat Dragon)                                    |
|   +- Pre-commit Hooks (gitleaks, detect-secrets, husky)                      |
|   +- SAST (Semgrep/CodeQL/SonarQube)                                        |
|   +- SCA (Snyk/Dependabot/Trivy) -+                                         |
|   +- Container Scan (Trivy/Clair) |  SBOM (CycloneDX/SPDX) 생성            |
|   +- IaC Scan (Checkov/tfsec)     |         v                              |
|   +- DAST/IAST (ZAP/Contrast)     |    Sigstore Cosign 서명                |
|   +- Policy Gate (OPA/Kyverno) ◄--+    SLSA Provenance 생성                |
|   +- Admission Control (Gatekeeper/Kyverno)                                 |
|   +- Runtime Security (Falco/Tetragon/eBPF)                                 |
|   +- Feedback -> DefectDojo/Jira/SIEM                                        |
+------------------------------------------------------------------------------+
```

기존 패러다임(Shift-Left 만 강조)에서는 **빌드 시점까지만 보안이 적용**되어 컨테이너 런타임·Service Mesh·Supply Chain 단계의 위협(메모리 기반 공격, SBOM 무결성 침해, 클러스터 RBAC 오남용)을 방어할 수 없었다. 따라서 현대 DevSecOps는 **Shift-Left(이른 정적 분석 + 위협 모델링) + Shield-Right(런타임 eBPF 모니터링 + Admission Control)** 양쪽을 **동일한 Policy Repo(GitOps)**에서 통합 관리하는 **Policy as Code** 중심으로 재설계된다.

- **📢 섹션 요약 비유**: 기존 방식은 **"집을 다 짓고 나서 방범창을 달고, 부엌을 다 쓰고 나서 가스 누경기를 점검하는 것"**이고, DevSecOps 내재화는 **"설계도 단계에서 방범창·가스누경기·소화기 배관 위치를 함께 그려서, 벽돌 하나 쌓일 때마다 자동 검침하는 것"**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DevSecOps 보안 내재화 파이프라인은 **7-Stage Reference Model**(Plan / Code / Build / Test / Release / Deploy / Operate) 각 단계에 **정합성 있는 보안 도구 + 정책 + 아티팩트**를 매핑한다. 핵심은 **(1) 자동화된 정책 평가(Policy as Code) (2) 불변 아티팩트(SBOM + Signature + Provenance) (3) 양방향 피드백(DefectDojo/SIEM)**의 3축 통합이다.

```text
+------------------------------------------------------------------------------+
|              DevSecOps 7-Stage Security Integration Architecture             |
|                                                                              |
| +--------+  +--------+  +--------+  +--------+  +--------+  +--------+      |
| |  PLAN  |-> |  CODE  |-> | BUILD  |-> |  TEST  |-> |RELEASE |-> | DEPLOY |      |
| +---+----+  +---+----+  +---+----+  +---+----+  +---+----+  +---+----+      |
|     |           |           |           |           |           |           |
|  +--v--+    +---v---+   +--v---+   +---v---+   +--v----+  +---v----+      |
|  |pytm |    |gitleaks|   |Semgr.|   |OWASP  |   |Cosign |  |Kyverno |      |
|  |Thrt.|    |detect- |   |CodeQL|   |  ZAP  |   |Rekor  |  |OPA     |      |
|  |Drag.|    |secrets |   |Sonar |   |Stack- |   |SLSA   |  |Gatekpr.|      |
|  |     |    |husky   |   |Snyk  |   |Hawk   |   |Syft   |  |ArgoCD  |      |
|  |     |    |Snyk    |   |Trivy |   |Cont-  |   |(SBOM) |  |Flagger |      |
|  |     |    |IDE     |   |Check.|   | rast  |   |Notary |  |Falco   |      |
|  +-----+    +--------+   +------+   +-------+   +-------+  +--------+      |
|     |           |           |           |           |           |           |
|     +-----------+-----------+-----+-----+-----------+-----------+           |
|                                   v                                          |
|                       +----------------------+                               |
|                       |  Policy Repo (GitOps) |                               |
|                       |  +- OPA Rego 정책    |                               |
|                       |  +- Kyverno YAML     |                               |
|                       |  +- SLSA L3 Proven.  |                               |
|                       |  +- VEX (CSAF 형식)  |                               |
|                       +----------+-----------+                               |
|                                  v                                           |
|                       +----------------------+    +----------------+          |
|                       |   Artifact Registry  |---->|  Sigstore TUF  |          |
|                       |   (Harbor/Quay/OCI)  |    |  (Cosign/ Rekor|          |
|                       +----------+-----------+    |   Fulcio/Rekor)|          |
|                                  |                +----------------+          |
|                                  v                                           |
|   +----------+  +--------------+--------------+  +--------------+            |
|   |  Operate |  |   Admission Controller      |  |  Runtime Sec |            |
|   |  Stage   |◄-|  (ValidatingAdmissionPolicy |-->|  Falco/Tetra.|            |
|   |  CSPM    |  |   + ImagePolicyWebhook)     |  |  Tracee/CSPM |            |
|   |  CIEM    |  +-----------------------------+  +--------------+            |
|   +----+-----+                                                            |
|        v                                                                  |
|   +----------+                                                            |
|   | DefectDo |◄--- SIEM (Splunk/Elastic/Sentinel) ---- IR/Forensics       |
|   | jo/Jira  |                                                            |
|   +----------+                                                            |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Threat Modeling (Plan 단계)** | 설계 단계에서 STRIDE/PASTA/LINDDUN 기반 위협 식별 | `OWASP pytm` (Python DSL로 Threat 자동 생성), `Microsoft Threat Modeling Tool`, `IriusRisk`, `Threat Dragon`. Plan 단계에서 `tm.json`을 산출하고 동일 모델을 빌드 시 SAST 룰셋으로 매핑(Semgrep Registry). |
| **Secret Scanning (Code 단계)** | 커밋/PR 시점 Secret(API Key, AWS Key, Private Key,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 402 / 800

<- **이전**: [401. 보안 개발 생명주기 SDL 보안 코딩](/studynote/12_it_management/05_security_compliance/401_security_development_lifecycle_sdl_coding/)
**다음**: [403. 클라우드 네이티브 보안 CNAPP CWPP](/studynote/12_it_management/05_security_compliance/403_cloud_native_security_cnapp_cwpp/) ->

---
