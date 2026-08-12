---
sidebar:
  order: 183
  label: "183. SBOM 소프트웨어 자재명세서 (SBOM)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "SBOM 소프트웨어 자재명세서 (SBOM)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 183
extra:
  question_no: "183"
  source_status: "기출"
  source_history: "128회, 134회, 135회, 138회"
  priority: 85
  priority_note: "구성요소 식별과 취약점 추적 반복 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **SBOM (Software Bill of Materials, 소프트웨어 자재 명세서)**: 소프트웨어 구성 오픈소스, 서드파티 라이브러리, 컴포넌트의 이름, 버전, 라이선스, 의존성 관계를 기계 판독 가능한 형태(Machine-Readable)로 명세한 문서.
- **Log4Shell**: 2021년 Log4j 취약점 사태. 자사 시스템 내 Log4j 존재 여부를 파악하지 못해 발생한 대규모 피해로 SBOM 도입의 결정적 계기.
- **NTIA (국가통신정보청)**: 미국 상무부 산하 기관. 행정명령(EO 14028)에 따라 연방정부 납품 소프트웨어의 SBOM 제출 의무화 및 최소 요건(Minimum Elements) 제정.

</details>

- 정의: 패키지 내 직접 의존성 및 전이(Transitive) 의존성을 추적하여 구성요소 가시성을 확보하는 소프트웨어 부품 명세서.
- 배경: 오픈소스 의존성 증가에 따른 구성요소 취약점(CVE) 및 라이선스 리스크 투명성 확보 요구.

#### 한줄 요약

- 완제품 안에 어떤 부품과 버전이 어떤 관계로 들어갔는지 적어 문제 부품이 발견됐을 때 영향 제품을 바로 찾는 디지털 부품표다.

## Ⅱ. 특징 (SBOM이 갖추어야 할 3대 최소 요건 - NTIA 기준)

<details><summary>핵심 용어</summary>

- **Transitive Dependency (전이 의존성)**: 개발자가 직접 포함한 라이브러리(A)가 내부적으로 의존하고 있는 또 다른 라이브러리(B, C). 해커들이 주로 공격하는 공급망의 숨겨진 사각지대.

</details>

- **Data Fields (데이터 필드)**: 공급자명, 컴포넌트명, 버전, 식별자(purl 등), 의존성 관계 등 부품 고유 식별 필수 메타데이터.
- **Automation Support (자동화 지원)**: SPDX, CycloneDX, SWID 등 표준 포맷을 활용한 기계(CI/CD) 기반 자동 생성 및 분석 체계.
- **Practices & Processes (운영 프로세스)**: 릴리즈별 SBOM 갱신, 하위 의존성 추적, 접근 통제 등 관리 절차.

#### 한줄 요약

- 이름만 적은 목록이 아니라 제품 버전·해시와 부품 관계를 연결해야 다른 빌드의 SBOM을 잘못 적용하지 않는다.

## Ⅲ. 구조 및 구성요소 (SBOM 포맷 및 생성 아키텍처)

<details><summary>핵심 용어</summary>

- **SPDX (Software Package Data Exchange)**: 리눅스 재단이 주도하는 ISO 표준(ISO/IEC 5962) SBOM 포맷으로, 라이선스 호환성 검증에 특화된 광범위한 스펙.
- **CycloneDX (사이클론DX)**: OWASP가 주도하는 포맷으로, 취약점 분석과 소프트웨어 공급망 보안(AppSec) 목적에 가벼우면서도 매우 적합하게 설계된 XML/JSON 규격.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   SBOM Generation & Usage Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. [Source Code / CI Pipeline] (package.json, pom.xml)                 │
│         │                                                              │
│         ▼ (SCA Tools: Syft, Trivy)                                     │
│ 2. [SBOM Generator] ──► 3. [SBOM Document (SPDX / CycloneDX 포맷)]     │
│                                 │ (JSON / XML)                         │
│                                 ▼                                      │
│ 4. [Vulnerability Database (NVD, CVE)] ◄──(비교 대조)──► [Security Ops]│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 빌드 파이프라인에서 SCA(소프트웨어 구성 분석) 도구가 소스와 바이너리를 스캔하여 SBOM 문서를 뽑아내면, 보안 시스템이 이를 CVE DB와 대조하여 취약 여부를 지속 판정하는 자동화 흐름.

| 핵심 구성요소 | 역할 및 정의 | 대표 도구 / 표준 |
|:---|:---|:---|
| **SCA Tool** | **소스 및 바이너리에서 의존성 트리를 추출하는 분석기** | Syft, Trivy, Snyk |
| **Standard Format**| **추출된 데이터를 담아내는 국제 표준 데이터 포맷** | **SPDX, CycloneDX** |
| **Component ID** | **전 세계에서 패키지를 유일하게 식별하는 고유 식별자** | **purl** (Package URL) |
| **VEX (보완재)** | **발견된 취약점이 실제 악용 가능한지(Exploitable) 명세**| CSAF VEX |

#### 한줄 요약

- 빌드에서 실제 부품을 뽑아 표준 목록을 만들고 제품 해시와 묶어 서명한 뒤 취약점 목록과 대조한다.

## Ⅳ. 흐름도 (SBOM 생성부터 취약점 대응 파이프라인)

<details><summary>핵심 용어</summary>

- **VEX (Vulnerability Exploitability eXchange)**: SBOM을 통해 취약점(CVE)이 발견되었더라도, 실제 해당 소프트웨어의 구동 환경에서는 그 취약점을 찌를 수 없는 상태(Not Affected)임을 해명하여 불필요한 패치 경고(False Positive)를 없애주는 상태 명세서.

</details>

```text
[DevOps Pipeline]
   │
   ├─ 1. Build Phase (소스코드 컴파일 및 패키징)
   │
   ├─ 2. SBOM Generation (SCA 도구가 의존성 트리 및 해시 추출)
   │
   ├─ 3. Attestation & Sign (SBOM 무결성 보장을 위한 전자 서명/In-toto)
   │
   ├─ 4. Store & Distribute (도커 이미지와 함께 레지스트리에 SBOM 저장)
   │
   └─ 5. Continuous Monitoring (운영 중 NVD에 새 CVE 뜨면 SBOM과 즉시 매칭)
           │
           ├─ (취약점 매칭됨) ──► VEX 발행 (이 취약점은 우리 코드에서 막혀있음)
           └─ (실제 위험함)   ──► 긴급 패치 파이프라인 가동
```

### 동작 원리

1. **추출**: 빌드 시점 도구(Syft 등)가 파일(pom.xml 등)을 스캔하여 부품 해시 및 버전 추출.
2. **서명**: SBOM 파일 위변조 방지(공급망 보안)를 위한 디지털 서명 수행.
3. **매칭 및 VEX**: CVE 매칭 후 실제 악용 가능 여부를 평가하여 VEX 발행(공급망 가시성 완결).

#### 한줄 요약

- 새 취약점이 공개되면 부품 식별자와 의존 경로를 따라 실제 배포 중인 제품 버전과 호출 가능성을 확인한다.

## Ⅴ. 종류 및 비교 (SBOM 생성 시점 1:1 비교)

<details><summary>핵심 용어</summary>

- **Binary Analysis (바이너리 분석)**: 소스코드가 없는 상용 솔루션이나 레거시 시스템의 경우, 최종 컴파일된 실행 파일이나 컨테이너 이미지를 역분석하여 포함된 라이브러리 목록(SBOM)을 강제로 추출하는 기법.

</details>

| 비교 항목 | Source / Build-time SBOM | Binary / Run-time SBOM |
|:---|:---|:---|
| **분석 대상** | **소스 코드 (git), 패키지 매니저 파일** | **도커 이미지, 컴파일된 실행 파일(.jar, .exe)**|
| **정확도 (포괄성)**| **전이 의존성 및 개발용 패키지까지 100% 식별** | 난독화, 정적 링킹 등으로 인해 식별 누락 발생 |
| **적용 시점** | CI/CD 파이프라인 (Shift-Left 보안) | CD 이후 배포/운영 단계 (사후 검증) |
| **주요 목적** | **자사 개발 소프트웨어의 투명성 증명 (납품용)**| **타사가 납품한 벤더 소프트웨어 검증** |

#### 한줄 요약

- 선언 파일은 빠르지만 실제 산출물과 다를 수 있어 빌드 시 생성을 정본으로 삼고 바이너리 분석으로 숨은 부품을 보완한다.

## Ⅵ. 실무 고려사항 및 대책 (SBOM 3대 실무 한계 대책)

<details><summary>핵심 용어</summary>

- **purl (Package URL)**: 패키지 매니저(npm, maven)마다 부품을 부르는 이름 규칙이 달라 생기는 혼란을 막기 위해, `pkg:npm/lodash@4.17.21` 처럼 전 세계 공통으로 부품을 식별하는 범용 주소 체계.

</details>

| 3대 SBOM 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 이름 기반 오탐지** | 동일 이름의 패키지가 다른 생태계에 존재 | **CPE 대신 명확한 생태계를 명시하는 purl 식별자 강제**|
| **2. 취약점 경고 폭탄** | 수천 개의 라이브러리 중 90%는 실제 미사용 | **VEX(취약점 악용 가능성) 문서를 동반하여 False Positive 제거**|
| **3. SBOM 위변조 공격** | 해커가 악성 부품을 넣고 SBOM에는 뺐다고 위조 | **SLSA 프레임워크 도입 및 SBOM 파일에 무결성 서명(Sigstore)**|

> 사례: **미국 연방정부(CISA)의 SW 납품 기업 대상 SBOM 제출 의무화 및 국내 금융권의 오픈소스 컴플라이언스 체계 구축 사례**

#### 한줄 요약

- 취약 라이브러리가 목록에 있어도 실행 경로와 설정상 사용할 수 없는지 VEX 근거를 확인해야 실제 위험 제품부터 고칠 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Software Supply Chain Security (소프트웨어 공급망 보안)**: 개발(코드 작성)부터 빌드, 배포, 운영에 이르는 전 과정에서 외부 라이브러리 오염을 막고 무결성을 보장하는 보안 체계로, SBOM은 이를 위한 가장 기본적인 인프라.

</details>

- SBOM 수립 기준에 따라 공공/금융 및 클라우드 네이티브 서비스 구축 시 CI/CD 파이프라인 내 SPDX/CycloneDX 포맷 생성 자동화 필수 적용.

#### 한줄 요약

- 빌드마다 제품 해시와 서명된 SBOM을 만들고 배포 자산·취약점·VEX를 연결해야 부품표가 실제 대응 도구가 된다.
