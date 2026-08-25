---
sidebar:
  order: 183
  label: "183. SBOM 소프트웨어 자재명세서"
  badge:
    text: "기출 · 85%"
    variant: note
title: "SBOM 소프트웨어 자재명세서 (Software Bill of Materials)"
date: "2026-08-25T11:00:00+09:00"
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

<details><summary>용어 설명</summary>

- **SBOM (Software Bill of Materials)**: 소프트웨어를 구성하는 오픈소스 모듈, 버전, 라이선스, 패키지 해시, 직접/전이 의존성을 기계 판독 가능한 표준 규격으로 명세한 디지털 부품 명세서.
- **Transitive Dependency(전이 의존성)**: 직접 선언한 모듈이 내부적으로 참조하는 2차, 3차 하위 종속 라이브러리.

</details>

- 정의/개념: 소프트웨어를 구성하는 오픈소스 모듈, 라이선스, 의존성을 **기계 판독 가능한 표준 규격(SPDX, CycloneDX)으로 기술한 디지털 소프트웨어 자재명세서**
- 배경/필요성: 오픈소스 및 서드파티 모듈 의존성 심화로 인한 **Log4j 등 공급망 취약점 발생 시 영향도 파악 불가 및 라이선스 위반 해결 불가**

#### 한줄 요약
- 기계 판독 가능한 표준 부품표(SBOM)를 통해 소프트웨어 공급망 투명성과 보안성을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPDX & CycloneDX**: ISO 국제 표준 라이선스 중심 규격(SPDX)과 OWASP 주도의 취약점/보안 중심 경량 규격(CycloneDX).
- **purl(Package URL)**: 생태계(npm, maven, pypi)와 무관하게 오픈소스 패키지를 표준 형식으로 식별하는 고유 URI 규격.

</details>

- 컴포넌트명, 버전, 공급자, 해시, 고유 패키지 URL(purl)을 포함하는 **표준 메타데이터 제공**
- 기계 판독(Machine-Readable: JSON/XML) 규격 기반의 **CI/CD 파이프라인 자동화 연동**
- 빌드 산출물과 SBOM의 일치성을 보장하는 **전자서명(Cosign) 및 무결성 검증**

#### 한줄 요약
- 표준 메타데이터, CI/CD 자동화, 전자서명 검증을 통해 공급망 보안을 완성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SBOM 3대 구성 계층**: Source/Artifacts(의존성 추출), Standard Document(SPDX/CycloneDX 스키마), Vulnerability/VEX(취약점 대조).

</details>

```text
[소프트웨어 자재명세서(SBOM) 생성 및 검증 구조]
|-- 1. Source & Artifacts Layer (npm `package-lock.json`, Maven `pom.xml`, 컨테이너 이미지)
`-- 2. Standard SBOM Document Layer (Syft / Trivy SCA 스캔)
    |-- Standard Formats: SPDX (ISO/IEC 5962) 또는 CycloneDX (JSON 규격)
    |-- Package Identifier: `pkg:npm/lodash@4.17.21` (purl) + SHA-256 Checksum
    `-- Dependency Graph: 직접 의존성 및 전이 의존성(Transitive) 계층 트리
`-- 3. Vulnerability & VEX Analysis Layer (NVD / Grype / Cosign 전자서명)
    |-- CVE Vulnerability Matching (알려진 보안 취약점 대조)
    `-- VEX Mapping (실제 런타임 악용 가능 여부 `not_affected` 판정)
```

선의 의미: 계층 및 빌드 산출물에서 SCA 도구가 의존성을 추출해 표준 SBOM을 생성하고 취약점 DB 및 VEX와 교차 분석하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SCA 분석 도구 (Syft)** | 소스코드 매니페스트와 바이너리를 스캔하여 **직접/전이 의존성 및 라이선스 자동 추출** | 의존성 분석기 |
| **표준 포맷 (SPDX/CycloneDX)**| 기계 판독 가능한 JSON/XML 스키마로 **부품명, 버전, 라이선스, 관계 그래프 표준화** | 표준 스키마 |
| **패키지 식별자 (purl & Hash)**| 생태계와 무관하게 **전 세계 공통으로 패키지와 버전을 고유 식별(Package URL)** | 고유 식별 체계 |
| **VEX (악용성 명세서)** | 발견된 CVE 취약점이 **실제 런타임 환경에서 악용 가능한지(Affected 여부) 상태 명시**| 오탐 제거 명세 |

#### 한줄 요약
- SCA 도구, 표준 포맷, 고유 식별자(purl), VEX 명세서가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SBOM 공급망 보안 5단계**: 의존성 추출 $\to$ 표준 SBOM 생성 $\to$ Cosign 전자서명 $\to$ NVD/VEX 대조 $\to$ 패치 배포.

</details>

```text
CI/CD 빌드 파이프라인 가동
        │
   1. [의존성 추출] Syft 도구가 소스코드 패키지 매니페스트 및 컨테이너 레이어 스캔
        │
   2. [표준 SBOM 생성] purl 및 SHA-256 해시를 포함한 CycloneDX 표준 JSON 문서 생성
        │
   3. [전자서명] Sigstore Cosign 도구를 사용하여 빌드 산출물과 SBOM 파일에 전자서명 수행
        │
   4. [취약점/VEX 대조] Grype 스캐너가 NVD 취약점 DB와 대조하고 VEX 명세서로 오탐 필터링
        │
   5. [패치 배포] 실제 악용 가능한 취약 컴포넌트의 버전을 업그레이드하고 프로덕션 배포
```

#### 한줄 요약
- 의존성 추출 → SBOM 생성 → 전자서명 → CVE/VEX 대조 → 패치 배포 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SPDX vs CycloneDX**: ISO 라이선스 거버넌스 표준(SPDX)과 OWASP 보안/취약점 분석 중심 표준(CycloneDX).

</details>

| 비교 항목 | SPDX (Linux Foundation / ISO 5962) | CycloneDX (OWASP) |
|:---|:---|:---|
| 핵심 지향점 | **오픈소스 라이선스 법적 컴플라이언스 및 저작권** | **애플리케이션 보안(AppSec) 및 취약점/VEX 분석** |
| 표준화 기구 | **ISO/IEC 5962 국제 표준** | **OWASP (Open Web Application Security Project)**|
| 스펙 및 데이터 구조| 방대하고 정밀한 라이선스 표현 스키마 | **경량 JSON/XML 스키마 및 VEX 친화적 구조** |
| 최적 적용 분야 | **엔터프라이즈 간 SW 납품 계약, 라이선스 검증** | **DevSecOps CI/CD 파이프라인, 컨테이너 보안 스캔** |

#### 한줄 요약
- 법적 라이선스 검증은 SPDX, DevSecOps 취약점 분석은 CycloneDX를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **VEX (Vulnerability Exploitability eXchange)**: 발견된 CVE 취약점이 실제 실행 환경에서 호출되지 않는 경우 `not_affected` 상태를 명시하여 불필요한 패치를 방지하는 문서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 패키지명 중복으로 인한 취약점 스캐너의 엉뚱한 오탐 발생 | **표준 패키지 고유 식별자인 `purl` (Package URL) 전사 강제** | 컴포넌트 식별 정확도 100% 달성 |
| 미사용 모듈 취약점으로 인한 수백 건의 보안 경보 과부하 | **`VEX (Vulnerability Exploitability eXchange)` 문서 동시 배포** | 개발팀 불필요 패치 공수 80% 절감 |
| 공급망 공격(Supply Chain Attack)으로 변조된 악성 라이브러리 유입 | **SLSA 프레임워크 준수 및 Sigstore/Cosign 기반 SBOM 서명 검증** | 악의적 모듈 무단 삽입 원천 차단 |
| 개발 완료 후 수동 SBOM 작성 시 누락 발생 | **CI/CD 빌드 단계에 Syft 자동 생성 스텝을 파이프라인 필수로 통합** | SBOM 최신성 및 100% 자동화 |

#### 한줄 요약
- purl 식별자 강제, VEX 오탐 제거, Cosign 전자서명, CI/CD 자동화로 운영한다.

## Ⅶ. 결론

- 글로벌 소프트웨어 공급망 보안 규제(미 행정명령 14028, EU CRA)에 대응하고 사이버 복원력을 강화하기 위해 **CI/CD 파이프라인 내 CycloneDX 표준 SBOM 자동 생성과 Cosign 전자서명 체계를 전사 의무화**하고, **VEX 기반의 취약점 오탐 정제 프로세스**를 결합하여 엔터프라이즈 공급망 보안 완성

#### 한줄 요약
- SBOM은 소프트웨어의 부품 명세를 표준화하고 전자서명 및 VEX와 결합하여 오픈소스 취약점과 라이선스 위험을 완벽히 통제하는 핵심 공급망 보안 기술이다.