---
sidebar:
  order: 183
  label: "183. SBOM 소프트웨어 자재명세서"
  badge:
    text: "기출 • 85%"
    variant: note
title: "SBOM 소프트웨어 자재명세서 (Software Bill of Materials)"
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

- **SBOM(Software Bill of Materials)**: SW 구성 오픈소스, 라이브러리, 의존성 관계를 기계 판독 가능한 형태(Machine-Readable)로 명세한 디지털 부품표.
- **Log4Shell**: Log4j 취약점 사태. 자사 내 취약 컴포넌트 식별 실패로 인한 SBOM 도입의 계기.
- **NTIA(National Telecommunications and Information Administration)**: 미 상무부 기관. 행정명령을 통해 연방 납품 SW 대상 SBOM 제출 의무화.

</details>

- 정의: SW 패키지의 직접 의존성 및 **전이 의존성(Transitive Dependency)**을 추적하여 구성요소 가시성을 확보하는 부품 명세서.
- 배경: 오픈소스 의존성 증가에 따른 CVE 취약점 및 라이선스 리스크 투명성 확보 요구.

## Ⅱ. 핵심 요건 (NTIA 기준)

<details><summary>핵심 용어</summary>

- **전이 의존성(Transitive Dependency)**: 개발자가 직접 포함한 라이브러리가 다시 의존하고 있는 간접 라이브러리.

</details>

- **Data Fields**: 공급자, 컴포넌트명, 버전, 식별자(**purl** 등), 의존성 관계 등 필수 메타데이터.
- **Automation Support**: **SPDX**, **CycloneDX**, SWID 등 표준 포맷 기반 자동 생성.
- **Practices & Processes**: 릴리즈별 SBOM 갱신, 하위 의존성 추적 등 관리 절차.

## Ⅲ. 아키텍처 및 구성요소

<details><summary>핵심 용어</summary>

- **SPDX(Software Package Data Exchange)**: 리눅스 재단 주도 ISO 표준(ISO/IEC 5962) SBOM 포맷. 라이선스 호환성 검증에 특화.
- **CycloneDX**: OWASP 주도 포맷. 취약점 분석 및 공급망 보안(AppSec) 목적의 최적화된 경량 규격.

</details>

```text
┌────────────────────────────────────────────────────────────┐
│                  SBOM 생성 및 사용 구조                    │
├────────────────────────────────────────────────────────────┤
│ 1. [CI Pipeline] ──► 2. [SCA(Syft, Trivy)] ──► 3. [SBOM]   │
│                                                 │          │
│ 4. [Vulnerability DB(NVD)] ◄───(비교 대조)──────┘          │
└────────────────────────────────────────────────────────────┘
```

| 핵심 구성요소 | 역할 및 정의 | 대표 표준 |
|:---|:---|:---|
| **SCA Tool** | 소스/바이너리 의존성 트리 추출 | Syft, Trivy |
| **Standard Format**| 추출 데이터 표준 포맷 | SPDX, CycloneDX |
| **Component ID** | 고유 식별자 | **purl**(Package URL) |
| **VEX(보완재)** | 취약점 실제 악용 가능성 명세 | CSAF VEX |

## Ⅳ. 취약점 대응 파이프라인

<details><summary>핵심 용어</summary>

- **VEX(Vulnerability Exploitability eXchange)**: 취약점이 존재해도 구동 환경상 실제 악용(Exploit) 불가함을 명세하여 거짓 양성(False Positive)을 제거하는 상태서.

</details>

```text
[Pipeline]
   │
   ├─ 1. Build(컴파일)
   ├─ 2. SBOM 생성 (SCA 도구)
   ├─ 3. 서명(전자 서명, In-toto)
   ├─ 4. 배포(이미지+SBOM)
   └─ 5. 모니터링 ──(CVE 발생)──► [VEX 발행] ──► [패치]
```

- 원리: 빌드 시 부품 추출/서명 후, 운영 중 NVD와 실시간 매칭 및 VEX 기반 대응.

## Ⅴ. SBOM 생성 시점 비교

<details><summary>핵심 용어</summary>

- **바이너리 분석(Binary Analysis)**: 소스코드 없는 레거시 시스템을 역분석하여 포함 라이브러리 목록을 강제 추출하는 기법.

</details>

| 항목 | Source-time SBOM | Binary-time SBOM |
|:---|:---|:---|
| **대상** | 소스코드, 패키지 관리 파일 | 컨테이너 이미지, 실행 파일 |
| **정확도** | 전이 의존성 식별 탁월 | 난독화/정적 링킹 누락 가능 |
| **주요 목적** | 납품용 투명성 증명 | 타사 벤더 SW 검증 |

## Ⅵ. 실무 난제 및 대책

<details><summary>핵심 용어</summary>

- **purl**: `pkg:npm/lodash@4.17.21` 등 패키지 생태계 무관 전 세계 공통 고유 식별 주소 체계.

</details>

| 난제 | 원인 | 대책 |
|:---|:---|:---|
| **이름 오탐지** | 생태계별 동일 패키지명 | **purl** 식별자 강제 |
| **경고 폭탄** | 미사용 라이브러리 취약점 | **VEX** 동반 False Positive 제거 |
| **위변조** | 공급망 악성 부품 삽입 | **SLSA** 프레임워크 및 무결성 서명 |

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **공급망 보안(Software Supply Chain Security)**: 개발부터 운영까지 외부 라이브러리 오염을 막는 보안 체계.

</details>

- 공공/금융 인프라 대상 SPDX/CycloneDX 표준 생성 및 VEX 결합 자동화 체계 적용.
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
