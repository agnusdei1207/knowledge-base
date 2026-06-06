---
title: "Open Source Governance License Management"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈소스 거버넌스 라이선스 관리는 SBOM(SPDX 2.3 / CycloneDX 1.5)을 단일 진실 공급원(SSOT)으로 삼아, 카피레프트(GPLv2/v3, AGPLv3, EPL)와 퍼미시브(MIT, BSD, Apache-2.0, MPL-2.0) 라이선스의 notice·source-disclosure·patent-grant 의무를 CI/CD 파이프라인의 빌드-테스트-배포 단계에 정적·동적 분석(SCA)으로 자동 매핑하는 거버넌스 체계다.
> 2. **가치**: 현대 엔터프라이즈 SW의 평균 70~90%가 OSS 컴포넌트(Synopsys 2023 OSSRA 보고서 기준 96%)로 구성되며, 라이선스·보안·공급망 리스크를 코드 단위로 추적하여 Log4Shell(CVE-2021-44228, 피해 5억 달러+)·xz-utils(CVE-2024-3094)·Heartbleed(CVE-2014-0160) 같은 사고와 EU CRA(2024), 美 EO 14028(2021), 국내 「소프트웨어산업법」 제19조의2 위반을 사전에 차단한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① SCA 도구(Tidelift/Black Duck/Snyk/FOSSA/Sonatype Nexus IQ/JFrog Xray/Mend) 도입·라이선스 비용 vs 컴플라이언스 위반 시 발생 가능한 정산금·배상액, ② 빌드시점 SCA(Shift-Left) vs 배포 후 Runtime SCA(Shift-Right) 배치, ③ OSPO(Open Source Program Office) 운영 성숙도 모델(OSMM Level 1~5) 선택, ④ 카피레프트 정책 허용 범위(예: AGPL 사용 전면 금지 vs SaaS 예외 허용) 결정이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 공급망이 1st-party(자체 코드) -> 2nd-party(상용 SW) -> 3rd-party(상용 SW에 내장된 OSS) -> Nth-party(Nth-party OSS의 transitive dependency)로 다층화되면서, 한 애플리케이션이 수천 개의 라이선스 의무를 동시에 부담하는 구조가 일반화되었다. 2000년대 초반 GPL 해석론을 중심으로 한 "라이선스 컴플라이언스"는 2018년 Equifax(Apache Struts, 1.47억 명 정보 유출, 7억 달러 합의)·2021년 Log4Shell(Log4j, 5억 달러+ 피해)·2022년 node-ipc(v8.1.1 라이선스 변조 사건)을 거치며 "공급망 보안·법적 거버넌스"로 패러다임이 전환되었다. 더 이상 OSS는 "무료 라이브러리"가 아니라 **법적 의무·보안 책임·규제 대상이 결합된 1급 컴플라이언스 자산**이다.

```text
[Legacy Paradigm: 2000s]                [Modern Paradigm: 2024+]
━━━━━━━━━━━━━━━━━━━━━━━                ━━━━━━━━━━━━━━━━━━━━━━━━
  1차: 자체 개발 코드                      1차: 자체 코드 (Proprietary)
       +                                     +
  2차: 상용 SW 패키지                      2차: 상용 SW (Oracle/IBM/SAP)
       +                                     +
  3차: OSS (GPL 정도만 인식)               3차: 직접 OSS (직접 의존성)
                                           +
                                          N차: 전이 의존성 (npm/pip/maven
                                               transitives) — 전체의 60~80%
                                           +
                                          메타데이터: SBOM, VEX, CSAF
                                          + 규제: EU CRA / EO 14028
                                          + 공격면: Supply Chain Attack
                                            (SolarWinds, 3CX, xz-utils)
```

**왜 오픈소스 거버넌스 라이선스 관리가 필수인가?**

1. **법적 리스크**: GPL 계열을 영업비밀 SW와 정적/동적 링킹 시 소스코드 공개 의무 발생. BusyBox·Cisco·Samsung(2018, FSF와의 합의 1,500만 USD)·Westinghouse·Skype 등 다수 분쟁 사례.
2. **보안 리스크**: NVD(2023) 기준 신규 CVE 중 OSS 비중 약 80%, 0-day는 프로젝트 평균 7년 이상 미패치. SCA 도구 없이 transitive dep 추적 불가능.
3. **규제 리스크**: EU Cyber Resilience Act(2024.10 발효, 2027 전면시행)는 제조사에게 5년간 보안 패치 제공·SBOM 제공·취약점 신고 의무화. 미 EO 14028(2021)은 연방기관에 SBOM 필수. 한국 행정안전부 「공공기관 공개SW 도입·활용 가이드라인」(2021) 및 「소프트웨어산업법」 제19조의2(2022 개정).
4. **계약·고객 요구**: 글로벌 OEM/고객사에서 SBOM(SPDX 또는 CycloneDX)·CRA 적합성 선언서·VEX 문서를 계약 필수 조건으로 요구.

- **📢 섹션 요약 비유**: 오픈소스 거버넌스는 마치 **다국적 결혼 상담소**와 같다. 100개국에서 온 외국인(OSS) 배우자의 국적·법(라이선스)·건강검진(보안)·가족관계(transitive dep)를 등록제(SBOM)로 관리하지 않으면, 혼인 신고(출시) 후에 신원보증료(GPL 배상금)·의료비(CVE 패치)·이혼소송(소송)이 한꺼번에 청구된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

오픈소스 거버넌스 시스템은 **정책 계층(Policy) -> 인벤토리 계층(Inventory/SBOM) -> 분석 계층(Analysis) -> 워크플로우 계층(Workflow) -> 보고 계층(Reporting)**의 5계층 아키텍처로 구성된다. Linux Foundation의 OSSF(OpenSSF) SLSA(Supply-chain Levels for Software Artifacts) 프레임워크 v1.0, SPDX 2.3(Specification), CycloneDX 1.5 OWASP 표준과 직접 연동된다.

```text
+---------------------------------------------------------------------+
|                  5-Layer Open Source Governance Architecture        |
+---------------------------------------------------------------------+
|  L5 Reporting       |  KPI 대시보드 | 컴플라이언스 리포트 | exec 뷰  |
|  ----------------------------------------------------------------  |
|  L4 Workflow        |  Jira/ServiceNow | 승인 라우팅 | PR 차단 정책 |
|  ----------------------------------------------------------------  |
|  L3 Analysis        |  SCA(Black Duck/Snyk/FOSSA/Mend)              |
|                     |  SAST/SCA/SBOM diff | License compatibility   |
|  ----------------------------------------------------------------  |
|  L2 Inventory       |  SBOM Repo (SPDX 2.3 / CycloneDX 1.5)         |
|                     |  Component DB | Version Graph | Provenance    |
|  ----------------------------------------------------------------  |
|  L1 Policy          |  OSPO 정책 | 화이트/블랙리스트 | Risk Tier    |
|  ----------------------------------------------------------------  |
|  L0 Source          |  Monorepo | Polyrepo | Package Registry       |
|                     |  (npm/pip/maven/cargo/go/nuget)              |
+---------------------------------------------------------------------+

         ^                ^                ^
         | PR/Push         | Build           | Deploy
         |                 |                 |
    +----+----+       +----+----+       +----+----+
    |  GitOps |       | CI/CD   |       | Runtime |
    | Webhook |       | (Jenkins/|       | eBPF/   |
    |  (pre)  |       |  GH A/  |       | Falco/  |
    |         |       | GitLab) |       | Tracee  |
    +---------+       +---------+       +---------+
```

### 1) 정책 계층 (L1: Policy Layer)

조직의 **OSPO**(Open Source Program Office, 예: Google OSPO, Microsoft OSS Office, Samsung Research OSS Center)가 다음 정책을 코드화·버전관리(GitOps) 한다.

- **Allowed License List**: Apache-2.0, MIT, BSD-2/3-Clause, ISC, MPL-2.0, Unlicense, CC0, Python-2.0 (legacy)
- **Conditional License**: LGPL-2.1+ (동적 링킹 시 허용), EPL-2.0 (수정 시 EPL 공개 의무)
- **Banned License**: AGPL-3.0(SaaS 공개 의무), SSPL, BUSL, Commons-Clause, Elastic License v2, RPL, JSON License
- **Tier 분류**: Tier-1(허용), Tier-2(조건부), Tier-3(금지), Tier-4(법무팀 개별 검토)
- **Risk Score**: CVSS × Exploit Maturity × License Risk × Maintainer Health(OpenSSF Scorecard)

### 2) 인벤토리 계층 (L2: Inventory / SBOM)

SBOM(Software Bill of Materials)은 SPDX(ISO/IEC 5962:2024)와 CycloneDX(OWASP, 1.5) 두 표준이 양대축이다.

| SBOM 표준 | 주 사용처 | 핵심 필드 | 식별자 |
| :--- | :--- | :--- | :--- |
| **SPDX 2.3** | Linux Foundation, 법규(EU CRA), SDLC | `SPDXID`, `PackageLicenseConcluded`, `PackageLicenseDeclared`, `FilesAnalyzed` | PURL, CPE 2.3, SWID |
| **CycloneDX 1.5** | OWASP, 보안 도구, DevSecOps | `bom-ref`, `components`, `dependencies`, `vulnerabilities`, `compositions`(L1/L2/L3) | PURL, OmniBOR, SWID |
| **CSAF 2.0** | 보안 권고(공급사 발행) | `Vulnerabilities`, `Product Tree`, `CVSS`, `Remediations` | CPE |
| **VEX** (Vulnerability Exploitability eXchange) | SBOM과 함께 배포 | `state(not_affected/investigated/fixed)`, `justification` | CycloneDX/SPDX 확장 |

SBOM은 **NTIA Minimum Field**(Supplier, Component, Version, Author of SBOM, Timestamp, Relationship, License) 7개 필드를 반드시 포함해야 한다.

### 3) 분석 계층 (L3: Analysis)

- **SCA(Software Composition Analysis)**: 패키지 매니페스트(package.json, pom.xml, requirements.txt, go.mod, Cargo.toml, Gemfile, build.gradle) + Lock file + Binary fingerprint(해시 기반).
- **License Compatibility Engine**: 트리 구조로 transitive license 해석. **공식 호환성 매트릭스** 예:

|          | GPL-2.0 | GPL-3.0 | LGPL-2.1 | LGPL-3.0 | AGPL-3.0 | Apache-2.0 | MIT/BSD | MPL-2.0 | Proprietary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPL-2.0** | ✅ | ⬆(2-only) | ⚠링킹 | ⬆ | ⬆ | ✅ | ✅ | ⚠파일 | ⚠링킹 |
| **GPL-3.0** | ⬇(2-only) | ✅ | ⬆ | ✅ | ✅ | ✅(patent) | ✅ | ⚠파일 | ⚠링킹 |
| **Apache-2.0** | ⚠ | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **MIT/BSD** | ⚠ | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **MPL-2.0** | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ✅ | ✅ | ✅ | ✅(파일단위) |
| **Proprietary** | ❌ | ❌ | ⚠동적 | ⚠동적 | ❌ | ✅ | ✅ | ✅ | ✅ |

> ※ ⚠=조건부, ⬆/⬇=호환되나 일방향, ❌=금지, ✅=자유. 자세한 매트릭스는 OSI·FSF·SPDX License List 참조.

- **보안 분석**: CVE/NVD/GHSA(OSV)/OSV.dev API -> EPSS(Exploit Prediction Scoring System, FIRST) -> KEV(known exploited vulnerabilities, CISA) -> VEX 매핑.
- **메타데이터**: OpenSSF Scorecard, deps.dev(BigQuery), Libraries.io, ecosystems(Tidelift Catalog).

### 4) 워크플로우 계층 (L4: Workflow)

- **Pre-commit**: pre-commit hook + license-checker(JS) / scancode-toolkit
- **PR/MR Gate**: GitHub/GitLab Branch Protection + OPA(Open Policy Agent, Rego 정책) / Conftest
- **Build Gate**: Jenkins/GitHub Actions의 `mend bolt`, `blackduck detect`, `snyk test`, `fossa-cli`, `trivy fs`, `grype`
- **Container Gate**: `trivy image`, `grype`, `syft`(SBOM 생성) + `cosign`(서명) + `in-toto`(SLSA Level 3)
- **Runtime Gate**: eBPF 기반 Falco,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 557 / 600

<- **이전**: [556. 클라우드 거버넌스 멀티 클라우드 정책](/studynote/11_design_supervision/06_exam_summary/556_cloud_governance_multi_cloud_policy)
**다음**: [558. 디지털 전환 전략 로드맵 수립](/studynote/11_design_supervision/06_exam_summary/558_digital_transformation_strategy_roadmap/) ->

---
