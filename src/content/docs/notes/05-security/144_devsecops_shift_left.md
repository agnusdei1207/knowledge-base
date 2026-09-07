---
sidebar:
  order: 144
  label: "144. DevSecOps 보안 시프트 레프트 (DevSecOps Shift-Left)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "소프트웨어 개발 생명주기 보안 내재화 : DevSecOps 및 Shift-Left (NIST SP 800-218 SSDF)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 144
extra:
  question_no: "144"
  source_status: "기출"
  source_history: "128회, 134회, 135회"
  priority: 85
  priority_note: "128회·134회·135회 최다 빈출, DevSecOps Shift-Left(보안 좌측 이동), CI/CD 파이프라인 단계별 보안 통제(Pre-commit Secret Scan ➔ SAST/SCA ➔ IaC/Container Scan ➔ DAST/IAST ➔ Image Signing & SBOM ➔ RASP/WAF 런타임 방어), 보안 품질 게이트(Quality Gate), NIST SP 800-218(SSDF) 및 SLSA 표준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DevSecOps 보안 시프트 레프트(Shift-Left / NIST SP 800-218 SSDF)**: 소프트웨어 개발 생명주기(SDLC)의 마지막 배포 직전에 일회성으로 수행하던 보안 점검(모의해킹, 감사) 방식을 탈피하여, 기획, 설계, 코딩, 빌드, 테스트 등 개발 초기(시간 축의 좌측) 단계부터 보안 활동과 도구(SAST, SCA, Secret Scan, IaC Scan)를 CI/CD 파이프라인에 코드형 보안(Security as Code)으로 자동 통합하는 방법론.
- **후행 보안 감사에 따른 배포 병목 및 결함 수정 비용 폭증 결함(Late-stage Security Bottleneck Defect)**: 개발이 완료된 후 운영 배포 직전에 보안 취약점이 발견될 경우, 아키텍처 재설계 및 코드 전면 수정으로 인해 결함 수정 비용이 설계 단계 대비 최대 100배(Boehm's Law) 폭증하고 릴리스 일정이 무기한 지연되는 구조적 결함.

</details>

- 정의/개념: 고품질의 안전한 소프트웨어를 신속 배포하기 위해 **Pre-commit 시크릿 스캔 $\rightarrow$ CI 빌드 시 SAST(정적 분석)/SCA(오픈소스 취약점) $\rightarrow$ 컨테이너/IaC 보안 검증 $\rightarrow$ CD 스테이징 시 DAST/IAST 동적 테스트 $\rightarrow$ SBOM 생성 및 이미지 서명(Cosign) $\rightarrow$ 런타임 RASP/EDR 연계** 를 집행하는 **전 주기 보안 자동화 파이프라인**
- 배경/필요성: 소프트웨어 개발 생명주기(SDLC)의 마지막 배포 직전에 수동으로 수행하던 전통적인 사후 보안 감사 및 모의해킹 방식은 결함 발견 시점의 수정 비용을 설계 대비 최대 100배(Boehm's Law) 폭증시키고 릴리스 일정을 무기한 지연시키는 심각한 병목을 초래함에 따라, NIST SP 800-218(SSDF) 및 SLSA 프레임워크에 기반하여 코딩, 빌드, 패키징, 테스트 전 단계에 SAST, SCA, 시크릿 스캔, IaC 검증, SBOM 생성 및 컨테이너 전자서명(Cosign)을 CI/CD 파이프라인에 코드형 보안(Security as Code)으로 자동 통합하는 DevSecOps Shift-Left 아키텍처를 도입하여 **보안 취약점 조기 식별 및 수정 비용 최소화, 오픈소스 공급망 무결성 보증 및 민첩한 무중단 배포(Agile Delivery)**를 달성할 필요

#### 한줄 요약
- DevSecOps Shift-Left는 CI/CD 파이프라인 전 단계에 보안 검증을 자동 내재화하여 결함 비용을 최소화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DevSecOps 3대 핵심 구현 메커니즘**:
  - **코드형 보안 (Security as Code / Policy as Code)**: OPA(Open Policy Agent), Kyverno 등을 활용하여 보안 규정을 선언적 코드로 정의하고 파이프라인에서 자동 검증.
  - **보안 품질 게이트 (Security Quality Gate)**: Critical/High 등급 취약점이나 하드코딩된 API Key 발견 시 CI/CD 빌드를 즉시 중단(Build Break).
  - **지속적 피드백 루프 (Fast Feedback Loop)**: 개발자가 PR(Pull Request) 생성 시 수 분 이내에 IDE나 PR 코멘트로 취약점 라인과 수정 가이드를 즉시 제공.

</details>

- 코딩·빌드 단계에서 결함을 찾는 **수정 비용 절감**
- SBOM과 이미지 서명에 기반한 **공급망 무결성**
- 런타임 위협을 개발에 돌려주는 **폐쇄 루프 피드백**

#### 한줄 요약
- 코드형 보안(PaC), 품질 게이트 빌드 차단, SBOM 공급망 무결성, 런타임 폐쇄 루프 피드백을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DevSecOps 파이프라인 6단계 핵심 보안 컴포넌트**:
  1. **Code (IDE & Pre-commit)**: SonarLint, TruffleHog (Secret Scan, 정적 린팅).
  2. **Build (CI Pipeline)**: SAST (SonarQube), SCA (Snyk, Dependency-Check).
  3. **Package & Infra (Container/IaC)**: Trivy (이미지 스캔), Checkov/KICS (Terraform/K8s IaC 스캔).
  4. **Test (Staging CD)**: DAST (OWASP ZAP), IAST (Contrast Security).
  5. **Deploy (Admission Control)**: Sigstore Cosign 이미지 검증 및 Kyverno 배포 통제.
  6. **Operate (Runtime)**: RASP, WAF, SIEM 기반 런타임 방어 및 개발 환류.

</details>

```text
[DevSecOps 보안 파이프라인]
├── [Code 단계 (사전 검증)]
│   └── Pre-commit 및 Secret Scan
├── [Build 단계 (정적 분석)]
│   └── SAST · SCA 및 Quality Gate
├── [Package 단계 (패키징)]
│   └── IaC 검증 · 컨테이너 스캔 · SBOM
├── [Test 단계 (동적 분석)]
│   └── DAST 및 IAST 런타임 테스트
├── [Deploy 단계 (배포 통제)]
│   └── Admission Control 및 Cosign 서명
└── [Operate 단계 (운영 방어)]
    └── RASP · WAF · SIEM 및 개발 환류
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **Code (코딩)** | Pre-commit 훅 기반 하드코딩된 시크릿 및 토큰 유출 차단 |
| **Build (빌드)** | SAST 시큐어코딩 검증과 SCA 오픈소스 취약점(CVE) 탐지 |
| **Package (패키지)** | 컨테이너 이미지 스캔, IaC 설정 오류 점검 및 SBOM 생성 |
| **Test (테스트)** | DAST 및 IAST 기반 동적 모의 침투 및 취약점 퍼징 |
| **Deploy (배포)** | 전자서명 무결성 검증 및 어드미션 컨트롤 기반 안전 배포 |
| **Operate (운영)** | RASP 및 WAF 기반 런타임 공격 방어와 취약점 개발 환류 |

#### 한줄 요약
- 각 도구는 별도의 보안 승인 조직을 거치지 않고 파이프라인 단계 자체에 박혀 빌드 실패로 판정을 대신하므로, 검증 책임이 배포 직전의 관문에서 코드를 쓰는 시점으로 옮겨지고 Admission Control만이 마지막 서명 확인을 남긴다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DevSecOps 자동화 파이프라인 5단계 프로세스**:
  1. 개발자 로컬 환경에서 코드 커밋 시 시크릿 스캔 수행
  2. Git Push 시 CI 파이프라인에서 SAST 및 SCA 정적 분석 실행
  3. Quality Gate 판정(취약점 0건 시 빌드 진행, 발견 시 빌드 중단 및 PR 반려)
  4. 컨테이너 빌드 후 IaC 스캔, SBOM 생성 및 전자서명(Cosign)
  5. 스테이징 DAST 검증 후 K8s 클러스터에 안전한 최종 배포

</details>

```text
1. [로컬 코딩 및 Commit]
    ├─ 개발자가 IDE에서 코드 작성 후 git commit 실행
    └─ [Pre-commit Hook(TruffleHog) 작동 ➔ 하드코딩된 AWS 키 검출 시 커밋 즉시 취소]
            │
            ▼
2. [CI 파이프라인 트리거 및 SAST/SCA 검증]
    ├─ GitHub Actions 트리거 ➔ SonarQube(SAST) 및 Snyk(SCA) 동시 실행
    └─ [CWE-89(SQL Injection) 및 Log4j 취약 라이브러리 자동 식별]
            │
            ▼
3. [품질 게이트 (Quality Gate) 판정]
    ├─ [시나리오 A: Critical 취약점 1건 이상] ➔ Exit 1 (Build Break), Slack 알림 및 PR 자동 차단
    └─ [시나리오 B: 취약점 임계치 0건 통과] ➔ 애플리케이션 빌드 및 Dockerfile 패키징
            │
            ▼
4. [컨테이너/IaC 검사 및 서명]
    ├─ Trivy로 컨테이너 이미지 스캔 + Checkov로 K8s 배포 매니페스트 보안 점검
    └─ [Syft로 SBOM(CycloneDX) 생성 ➔ Cosign으로 컨테이너 이미지에 전자서명 주입]
            │
            ▼
5. [배포 검증 및 CD 롤아웃]
    ├─ ArgoCD 배포 시 K8s Kyverno가 컨테이너 이미지 전자서명 무결성 검증
    ├─ 스테이징 서버에서 OWASP ZAP(DAST) 자동 동적 취약점 진단
    └─ [이상 없음 확인 ➔ 제로 트러스트 프로덕션 클러스터 무중단 배포]
```

**동작 원리**

1. **로컬 코딩 및 Commit**: Pre-commit 시크릿 탐지와 커밋 차단
2. **CI 파이프라인 트리거 및 SAST/SCA 검증**: 코드·종속성 분석
3. **품질 게이트 판정**: 취약점 임계치에 따른 빌드 중단
4. **컨테이너/IaC 검사 및 서명**: SBOM 생성과 이미지 서명
5. **배포 검증 및 CD 롤아웃**: 서명·DAST 통과 아티팩트 배포

#### 한줄 요약
- 게이트를 앞단으로 옮길수록 수정 비용은 싸지지만 오탐이 개발 속도를 직접 깎으므로, 초기 단계일수록 차단 기준을 좁게 잡고 배포에 가까울수록 엄격히 하는 배치가 유효하다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **애플리케이션 보안 테스트 3대 접근 방식 비교**:
  - Shift-Left (CI 단계): SAST, SCA, IaC Scan (초기 예방, 화이트박스).
  - Shift-Right (CD/테스트 단계): DAST, 모의해킹 (동적 런타임, 블랙박스).
  - Shield-Right (운영 단계): RASP, WAF, CWP (운영 환경 능동 방어).

</details>

| 비교 항목 | 보안 시프트 레프트 (Shift-Left) | 보안 시프트 라이트 (Shift-Right) | 런타임 실드 (Shield-Right) |
|:---|:---|:---|:---|
| **수행 단계** | **Plan, Code, Build (CI 단계)** | **Test, Staging, Release (CD 단계)**| **Production Operate (런타임 단계)**|
| **핵심 기법** | **SAST, SCA, Pre-commit, IaC Scan** | **DAST, 침투 테스트, 카오스 엔지니어링**| **RASP, 클라우드 WAF, EDR/XDR** |
| **분석 방식** | **화이트박스 (소스코드/설정 직접 분석)**| **블랙박스 (외부 HTTP 요청/응답 분석)**| **그레이박스 (애플리케이션 내부 훅 인터셉트)**|
| **주요 장점** | **결함 수정 비용 극소화, 빠른 피드백**| 실제 런타임 환경 취약점 정밀 검증 | **패치 전 제로데이 공격 실시간 차단**|
| **단점/한계** | 런타임 비즈니스 로직 취약점 탐지 불가| 빌드 완료 후 검사로 수정 비용 증가 | 앱 성능 오버헤드, 에이전트 관리 부담|

#### 한줄 요약
- Shift-Left는 초기 코드 예방, Shift-Right는 스테이징 동적 검증, Shield-Right는 런타임 실시간 방어에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-218 (SSDF) 및 SLSA (공급망 보안 레벨)**: 안전한 소프트웨어 개발 프레임워크 및 오픈소스 공급망 무결성 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무분별한 SAST/SCA 도입으로 수천 건의 오탐(False Positive)이 발생하여 **개발자의 알람 피로(Alert Fatigue) 및 CI 빌드 지연으로 개발팀의 보안 도구 비활성화** | **초기 도입 시 감사 모드(Audit Mode)로 운영하여 베이스라인을 설정하고, Critical/High 등급 한정 Quality Gate 적용 및 예외(Waiver) 자동화** | 오탐 노이즈 80% 감소 및 파이프라인 개발 속도 유지 |
| 개발자가 AWS Access Key나 DB 패스워드를 코드에 하드코딩하여 **GitHub 퍼블릭 레포지토리에 푸시됨으로써 클라우드 인프라 전면 해킹 발생** | **TruffleHog 기반 Pre-commit Hook을 전사 강제화하고, HashiCorp Vault 등 외부 KMS 시크릿 매니저 연동 강제** | 시크릿 하드코딩 유출 사고 100% 원천 차단 |
| Log4j 사태와 같이 신뢰할 수 없는 외부 오픈소스 패키지의 취약점이 **내부 빌드 시스템으로 유입되어 전사 백도어로 전이되는 공급망 침해 발생** | **NIST SP 800-218 준수, CycloneDX SBOM 자동 생성 및 Sigstore Cosign 컨테이너 서명 기반 K8s 배포 통제(SLSA Level 3) 구축** | 오픈소스 공급망 위조 및 변조 100% 원천 방어 |

#### 한줄 요약
- 베이스라인 튜닝으로 오탐을 줄이고, Pre-commit으로 시크릿 유출을 막으며, SBOM/Cosign으로 공급망을 방어한다.

## Ⅶ. 결론

- 보안을 개발과 배포의 장애물이 아닌 소프트웨어 품질의 필수 속성으로 내재화하여 민첩성과 안전성을 동시에 확보하는 **소프트웨어 개발 생명주기 보안 및 시프트 레프트(NIST SP 800-218 SSDF / SLSA / DevSecOps Pipeline)의 핵심 엔지니어링 표준**으로 확고히 자리 잡았으며, 클라우드 네이티브 환경의 CNAPP(Cloud Native Application Protection Platform) 및 AI 기반 코드 취약점 자동 패치(Remediation)로 진화하는 가운데, 실무 CI/CD 파이프라인 구축 시에는 **오탐 피로 방지를 위한 Critical/High 등급 한정의 품질 게이트(Quality Gate) 엄격 적용, TruffleHog 기반 로컬 Pre-commit 시크릿 유출 차단, CycloneDX SBOM 및 Sigstore Cosign 기반 컨테이너 이미지 무결성 입증**을 결합하여 완벽한 소프트웨어 공급망 보안을 완성

#### 한줄 요약
- CI/CD 전 단계 보안 자동화와 코드형 정책(PaC)을 통해 무결점 DevSecOps Shift-Left를 완성한다.
