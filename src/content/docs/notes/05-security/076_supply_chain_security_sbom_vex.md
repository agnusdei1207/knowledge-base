---
sidebar:
  order: 76
  label: "076. 소프트웨어 공급망 보안 (Supply Chain Security)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "소프트웨어 공급망 전주기 무결성 보증 : SBOM, VEX, SLSA (NIST SP 800-218 & Sigstore)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-security"
weight: 76
extra:
  question_no: "076"
  source_status: "기출"
  source_history: "128회, 134회, 135회, 138회"
  priority: 85
  priority_note: "128•134•135•138회 반복 기출, 소프트웨어 공급망 보안 3각 편대(SBOM: SPDX/CycloneDX, VEX: CSAF/OpenVEX, 출처 증명: SLSA v1.0/in-toto), Sigstore/Cosign 전자서명, NIST SSDF 1.1(SP 800-218)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **소프트웨어 공급망 보안(Software Supply Chain Security / NIST SP 800-218)**: 소스코드 작성, 오픈소스 라이브러리(3rd-party) 의존성 수입, CI/CD 빌드 파이프라인, 아티팩트 레지스트리 저장, 프로덕션 배포에 이르는 전체 소프트웨어 생애주기 전반에 걸쳐 악성코드 주입, 소스코드 변조, 종속성 혼란(Dependency Confusion) 공격을 방어하고 소프트웨어의 출처와 무결성을 보증하는 종합 보안 체계.
- **전이 의존성 및 보이지 않는 부품 위험(Transitive Dependency Blind Spot Defect)**: 현대 애플리케이션의 80% 이상이 오픈소스 컴포넌트로 구성되나, 개발자가 직접 임포트한 패키지가 다시 하위로 불러오는 수백 개의 간접 라이브러리(Transitive Dependency)에 포함된 취약점(Log4j, XZ Utils 등)을 사전에 식별하지 못하는 가시성 결함.

</details>

- 정의/개념: NIST SSDF 1.1 및 SLSA v1.0 표준에 기반하여 **SBOM(부품 명세서) $\rightarrow$ VEX(실질 악용 가능성) $\rightarrow$ SLSA 출처 증명(Provenance) $\rightarrow$ Sigstore 전자서명 $\rightarrow$ 배포 게이트(Admission Controller) 검증** 을 집행하는 **엔드투엔드 소프트웨어 무결성 아키텍처**
- 배경/필요성: 현대 소프트웨어 개발에서 오픈소스 라이브러리와 3rd-party 컴포넌트의 의존성이 80% 이상으로 급증함에 따라, 개발자가 인지하지 못한 하위 전이 의존성(Transitive Dependency) 취약점(Log4j, XZ Utils)과 빌드 파이프라인 침해를 통한 백도어 주입(SolarWinds) 등의 소프트웨어 공급망 공격이 급증하는 치명적 한계가 발생함에 따라, NIST SP 800-218(SSDF 1.1) 및 SLSA v1.0 표준에 기반하여 소프트웨어 자재명세서(SBOM), 취약점 악용성 교환(VEX), 출처 증명(Provenance) 및 Sigstore 전자서명을 배포 게이트(Admission Controller)와 결합하는 소프트웨어 공급망 보안 아키텍처를 도입하여 **소프트웨어 전이 의존성의 100% 가시화, VEX 기반 실질 악용성 중심 패치 최적화 및 빌드-배포 전주기 무결성 보증**을 달성할 필요

#### 한줄 요약
- SBOM(부품 식별), VEX(악용성 평가), SLSA(출처 증명), Sigstore(전자서명)를 결합하여 공급망 전주기 무결성을 완성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **공급망 보안 3각 편대**:
  - **SBOM (Software Bill of Materials / SPDX & CycloneDX)**: 소프트웨어에 포함된 모든 오픈소스 라이브러리의 이름, 버전, 라이선스, 해시, 종속 관계를 명시한 기계 판독형 자재명세서.
  - **VEX (Vulnerability Exploitability eXchange / CSAF & OpenVEX)**: SBOM에 명시된 취약점(CVE)이 해당 제품의 특정 실행 환경에서 실제 호출/악용될 수 있는지(`affected`, `not_affected`, `fixed`, `under_investigation`) 판정하여 불필요한 패치 공수를 줄이는 문서.
  - **출처 증명 (Provenance / SLSA v1.0 & in-toto)**: 빌드 산출물이 변조되지 않은 소스 Commit, 지정된 빌드 도구, 격리된 빌드 환경에서 생성되었음을 암호학적으로 입증하는 진품 증명서.

</details>

- **부품 식별과 실질 악용성의 분리 (SBOM + VEX)**: 단순 CVE 개수에 따른 패닉을 방지하고, 실행 경로상 도달 불가능한 취약점은 VEX `not_affected`로 판정하여 패치 리소스 최적화
- **격리된 빌드 및 재현 빌드 (Reproducible Builds)**: 인터넷 접속이 차단된 샌드박스 컨테이너 빌드를 통해 빌드 스크립트 오염을 방지하고 동일 해시 재현성 검증
- **암호학적 서명 결속 및 게이트키퍼 집행**: 아티팩트에 Sigstore(Cosign) 서명을 주입하고 쿠버네티스 Admission Controller에서 미서명 산출물 배포를 원천 차단

#### 한줄 요약
- SBOM 부품 가시화, VEX 실질 악용성 판별, SLSA 빌드 출처 증명, Sigstore 서명 배포 게이트를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **공급망 보안 4대 핵심 컴포넌트**:
  1. **Source & Dependency Gate**: 오픈소스 패키지 해시 고정(Pinning) 및 악성 패키지(Typosquatting) 사전 차단.
  2. **Isolated Build Engine (SLSA Level 3)**: 변조 불가능한 호스팅 빌더 및 단명 OIDC 자격증명(Ephemeral Tokens) 기반 빌드.
  3. **Attestation & Artifact Registry**: OCI 이미지, SBOM, VEX, Provenance를 단일 번들로 불변 저장.
  4. **Admission Controller (Gatekeeper)**: 클러스터 배포 시 암호학적 전자서명과 정책 일치성을 검증하는 관문.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 소스 및 오픈소스 수입 계층 (Source & Dependency Ingestion) ]       │
│  ├─ Git Commit: 서명된 커밋(GPG/SSH)만 수용                             │
│  └─ 의존성 고정: 해시 락파일(Lockfile) 기반으로 승인된 오픈소스만 다운로드│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (검증된 소스 주입)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 격리된 빌드 파이프라인 (Hermetic & Isolated Build: SLSA Level 3) ]  │
│  ├─ 샌드박스 빌드 실행 (외부 인터넷 접속 차단)                          │
│  ├─ SBOM 자동 생성 (CycloneDX JSON) & VEX 악용성 분석 (OpenVEX)          │
│  └─ [ Sigstore / Cosign ➔ OIDC 기반 단명 키로 빌드 산출물 전자서명 ]   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (서명된 바이너리 + SBOM + VEX + SLSA 번들)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 불변 아티팩트 레지스트리 (Immutable Registry & Attestation Store) ]│
│  └─ [ OCI 아티팩트, Cosign 서명, in-toto Attestation 메타데이터 보관 ]   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (쿠버네티스 배포 요청: kubectl apply)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 배포 관문 집행 계층 (Admission Controller: Kyverno / Gatekeeper) ] │
│  ├─ Sigstore 공개키 서명 검증 ➔ "변조되지 않은 진품 이미지 확인"         │
│  ├─ VEX 상태 검증 ➔ "미조치된 Critical Exploit 취약점 부재 확인"        │
│  └─ [ 전 항목 충족 시 ➔ 프로덕션 클러스터 Pod 기동 승인 ]                │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 소스와 의존성이 격리된 빌드 환경에서 컴파일되어 SBOM/VEX/서명이 결속되고, 배포 게이트에서 무결성이 검증되어 런타임에 안착하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **의존성 락커 (Dependency Pinning)**| 락파일 및 체크섬 해시 검증을 통해 패키지 변조 및 종속성 혼란 공격 차단 | Ingestion Gate |
| **격리 빌드 엔진 (Hermetic Builder)**| 외부 통신이 차단된 샌드박스 환경에서 빌드를 수행하여 빌드 스크립트 오염 방어 | SLSA Level 3 |
| **SBOM/VEX 생성기** | 바이너리 분석을 통해 부품 목록(CycloneDX)과 실제 악용성(OpenVEX) 메타데이터 생성 | Metadata |
| **Sigstore / Cosign** | OIDC 신원 기반으로 키 관리 부담 없이 산출물에 단기 비대칭 전자서명 주입 | Keyless Signing|
| **Admission Controller** | 서명 무결성, SBOM 존재, VEX 승인 정책을 만족하는 아티팩트만 배포 인가 | Gatekeeper |

#### 한줄 요약
- 의존성 락커, 격리 빌드 엔진, SBOM/VEX 생성기, Sigstore 전자서명, Admission Controller가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **공급망 보안 5단계 전주기 파이프라인**:
  1. 소스 커밋 및 오픈소스 의존성 무결성 검증
  2. 인터넷 격리 샌드박스 빌드 및 SBOM/출처 증명 생성
  3. Sigstore Keyless 비대칭 전자서명 수행
  4. 불변 OCI 레지스트리에 아티팩트 및 증적(Attestation) 업로드
  5. 배포 게이트에서 서명/VEX 정책 검증 후 런타임 승격

</details>

```text
1. [소스 및 의존성 무결성 검사] 개발자 GPG 서명 커밋 확인 ➔ `package-lock.json` 해시 대조 후 오픈소스 다운로드
            │
            ▼
2. [격리 빌드 및 증적 생성]
    ├─ 외부 인터넷이 차단된 샌드박스 러너에서 소스 컴파일
    └─ Syft/Trivy 도구를 실행하여 `sbom.json`(부품 목록) 및 `provenance.json`(SLSA 출처) 자동 생성
            │
            ▼
3. [Sigstore 암호학적 전자서명] Cosign이 GitHub OIDC 토큰을 이용해 Fulcio/Rekor 기반으로 아티팩트에 전자서명
            │
            ▼
4. [불변 레지스트리 번들링] 컨테이너 이미지와 전자서명, SBOM, VEX, Attestation을 OCI 레지스트리에 불변 저장
            │
            ▼
5. [배포 게이트(Gatekeeper) 검증 및 런타임 기동]
    ├─ Kyverno가 OCI 레지스트리에서 Cosign 서명 무결성 및 Rekor 투명성 로그 검증
    ├─ VEX 문서 대조: "알려진 RCE 취약점이 `not_affected`로 소명되었는지" 확인
    └─ [검증 100% 통과 ➔ 운영 노드에 컨테이너 Pod 배포 완료]
```

**동작 원리**

1. **소스 및 의존성 무결성 검사**: 서명·해시 대조
2. **격리 빌드 및 증적 생성**: SBOM·출처 증명 생성
3. **Sigstore 암호학적 전자서명**: 단명 신원으로 서명
4. **불변 레지스트리 번들링**: 산출물·증적 함께 저장
5. **배포 게이트 검증 및 런타임 기동**: 정책 충족 시 승인

#### 한줄 요약
- 증적 생성은 빌드 시점의 일회성 비용이지만 그 증적이 없으면 배포 게이트가 매번 사람의 조사로 되돌아가므로, 앞단의 격리 빌드 투자가 뒷단의 반복 검증 비용을 대신 치르는 구조다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **공급망 보안 3대 핵심 증적 포맷 비교**: SBOM, VEX, SLSA 출처 증명(Provenance)의 비교.

</details>

| 비교 항목 | 소프트웨어 자재명세서 (SBOM) | 취약점 악용성 교환 (VEX) | SLSA 출처 증명 (Provenance) |
|:---|:---|:---|:---|
| **핵심 목적** | **"무엇이 들어있는가?" (부품 목록 식별)**| **"실제 위험한가?" (실질 악용성 판별)**| **"누가 어떻게 만들었는가?" (빌드 무결성)**|
| **주요 표준 규격** | **SPDX (ISO/IEC 5962), CycloneDX** | **CSAF 2.0, OpenVEX** | **SLSA v1.0, in-toto Attestation** |
| **기록 정보** | 패키지명, 버전, 라이선스, SHA 해시 | CVE 식별자, 상태(`not_affected` 등), 근거 | 빌더 ID, Git Commit ID, 빌드 파라미터 |
| **주요 해결 과제** | 보이지 않는 전이 의존성 가시화 | 단순 취약점 스캔 알람 피로 해소 | 빌드 서버 해킹 및 악성코드 주입 차단 |
| **배포 게이트 역할**| 승인되지 않은 부품 포함 여부 심사 | 미해결 Critical 취약점 배포 차단 | 변조되지 않은 빌드 파이프라인 검증 |
|:---|:---|:---|:---|

#### 한줄 요약
- SBOM은 부품 식별, VEX는 실질 악용성 판정, SLSA는 빌드 출처 무결성을 상호보완적으로 보증한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SLSA v1.0(Supply-chain Levels for Software Artifacts)**: 오픈소스 생태계 및 상용 소프트웨어의 소스, 빌드, 배포 전주기 무결성을 보증하기 위한 구글/OpenSSF 주도의 4단계 보안 등급 프레임워크.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 서버가 해킹되어 CI/CD 파이프라인 내부에서 **소스코드에 없는 악성 백도어가 컴파일 시점에 몰래 주입되는 사고(SolarWinds형)** | **NIST SP 800-218 SSDF 준수, 인터넷 격리 샌드박스 빌드(SLSA Level 3) 및 재현 빌드(Reproducible Build) 교차 검증** | 파이프라인 오염 및 빌드 시점의 악성코드 주입 100% 원천 차단 |
| 수만 개의 오픈소스 CVE 취약점이 검출되어 **실제 영향이 없는 취약점 패치에 리소스가 고갈되고 정상 배포가 마비되는 결함** | **CISA 표준 CSAF/OpenVEX 도입, 실행 경로상 도달 불가능한 취약점에 대해 `not_affected` 기계 판독형 VEX 발행** | 불필요한 패치 공수 80% 이상 절감 및 실제 위험한 취약점에 조치 집중 |
| 개발자가 임의로 빌드한 미검증 컨테이너 이미지가 **운영 쿠버네티스 클러스터에 배포되어 보안 통제를 우회하는 사각지대** | **Sigstore/Cosign 기반 Keyless 전자서명 강제 및 Admission Controller(Kyverno/Gatekeeper) 배포 차단 정책 적용** | 무인가/미서명 이미지의 프로덕션 배포 100% 원천 차단 |

#### 한줄 요약
- SLSA 격리 빌드로 백도어 주입을 막고, VEX로 패치 공수를 절감하며, 배포 게이트로 미서명 이미지를 차단한다.

## Ⅶ. 결론

- 오픈소스 생태계와 글로벌 소프트웨어 유통 구조의 복잡성 속에서 소프트웨어의 출처, 구성 요소 및 빌드 무결성을 수학적·암호학적으로 증명하는 **차세대 DevSecOps 및 글로벌 소프트웨어 신뢰성 보증(NIST SSDF / SLSA / 미국 행정명령 EO 14028)의 최상위 핵심 표준 체계**로 확고히 자리 잡았으며, AI 모델 및 데이터셋 공급망 보안(AIBOM)으로 전면 확장되는 가운데, 실무 엔터프라이즈 공급망 보안 인프라 구축 시에는 **CycloneDX/SPDX 기반 SBOM 자동 생성 및 CSAF/OpenVEX 연계를 통한 패치 리소스 최적화, SLSA Level 3 부합 인터넷 격리 샌드박스 빌드 파이프라인 구축, OIDC 기반 Sigstore Keyless 전자서명 및 쿠버네티스 Admission Controller(Kyverno) 배포 차단 게이트 결합**을 완비하여 완벽한 소프트웨어 공급망 전주기 무결성을 완성

#### 한줄 요약
- SBOM 부품 가시화, VEX 악용성 판별, SLSA 격리 빌드 및 Sigstore 서명을 통해 소프트웨어 공급망 보안을 완성한다.
