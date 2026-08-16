---
sidebar:
  order: 76
  label: "076. 소프트웨어 공급망 보안 (Supply Chain Security)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "소프트웨어 공급망 보안 (Supply Chain Security)"
date: "2026-08-13T20:34:00+09:00"
tags:
  - "notes-security"
weight: 76
extra:
  question_no: "076"
  source_status: "기출"
  source_history: "128회, 134회, 135회, 138회"
  priority: 85
  priority_note: "128•134•135•138회 반복된 최우선 공급망 주제임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **소프트웨어 공급망(Software Supply Chain)**: 소스코드, 오픈소스 의존성 획득, 빌드, 바이너리 저장소, CI/CD 배포로 연결되는 소프트웨어 조립 및 유통 파이프라인 구조이다.
- **전이 의존성(Transitive Dependency)**: 개발자가 직접 추가한 라이브러리가 다시 하위로 엮어 불러오는 간접 수용 의존성 요소이다.

</details>

- 정의/개념: 소스부터 배포까지 무결성을 보증하는 **공급망 보안**
- 배경/필요성: 전이 의존성은 **취약점•악성 코드**를 연쇄 전파

#### 한줄 요약

- 소스, 빌드 파이프라인, 오픈소스 의존성의 출처와 무결성을 정밀 검증하여 공급망 내 위변조 및 악성 코드 침투를 차단하는 체계이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **소프트웨어 자재명세서(Software Bill of Materials, SBOM)**: 소프트웨어를 구성하는 모든 오픈소스 부품, 라이브러리 버전, 관계를 표준(SPDX, CycloneDX)으로 명시한 명세서이다.
- **취약점 악용 가능성 교환(Vulnerability Exploitability eXchange, VEX)**: SBOM 상 취약점 CVE의 실질적 영향 여부(Not Affected, Affected 등)와 판단 근거를 기계 읽기 양식으로 기재한 서술서이다.
- **출처 증명(Provenance / Attestation)**: 빌드 산출물이 소유자, 코드 깃 commit ID, 빌드 도구에 의해 변조 없이 생성되었음을 입증하는 디지털 증명서(SLSA 등)이다.

</details>

- **SBOM**과 **VEX** 표준을 결합하여 명세 파악과 실제 취약점 영향 조치 우선순위 산정을 자동화한다.
- 격리된 빌드 환경과 전자서명을 기반으로 소프트웨어 아티팩트의 주입 변조를 근본적으로 방어한다.
- **출처 증명**을 이용해 배포 관문(Deployment Gate)에서 검증된 아티팩트만 운영 서버에 승격 배치한다.

#### 한줄 요약

- SBOM으로 명세화하고 VEX로 실질적 악용 영향을 판단하며, SLSA 기반 출처 증명으로 무결성을 검증한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **격리 빌드(Isolated Build)**: 외부 인터넷 접속과 권한이 통제된 샌드박스 파이프라인 컨테이너 내에서 빌드를 수행하는 방식이다.
- **단명 자격(Ephemeral Credentials)**: 빌드 및 배포 작업 실행 시간 동안에만 임시로 발급되고 소멸하는 OIDC 기반 임시 자격 증명이다.
- **불변 저장소(Immutable Repository)**: 한번 업로드된 아티팩트 및 이미지가 동일 태그/식별자로 덮어쓰기 불가능하도록 보관하는 레포지토리이다.
- **배포 게이트(Deployment Gate)**: 전자서명, SBOM, VEX, 출처 증명이 승인 정책에 부합할 때만 배포를 승인하는 자동화 검증 문이다.

</details>

```text
[소스·의존성 제어] ----- [격리 빌드] ----- [산출물·서명]
                                                |
                                    [SBOM·VEX·출처]
                                                |
                                    [검증·배포 게이트]
```

선의 의미: 승인된 의존성 제어, 샌드박스 격리 빌드, 서명된 바이너리 및 SBOM/VEX 증적을 검증해 배포 게이트를 통과시키는 공급망 라인 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 소스·의존성 제어 | 핀다운(Pinning) 및 해시 고정을 통한 승인된 오픈소스 패키지 유입 제어 |
| 격리 빌드 | **단명 자격**과 **격리 빌드** 환경을 통해 외부 침투 및 빌드 스크립트 오염 차단 |
| 산출물·서명 | Sigstore/Cosign 기반 전자서명과 **불변 저장소** 저장을 통한 위변조 방지 |
| SBOM·VEX·출처 | SPDX/CycloneDX 표준 **SBOM**, **VEX**, **출처 증명** 메타데이터 결속 |
| 검증·배포 게이트 | **배포 게이트**를 통해 미서명 산출물 및 고위험 VEX 항목의 인프라 반영 차단 |

#### 한줄 요약

- 승인된 의존성을 샌드박스 격리 환경에서 빌드 및 서명하고, SBOM/VEX 증적을 배포 게이트에서 검증한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **서명 산출물(Signed Artifact)**: Cosign/Sigstore 전자서명이 포함되어 무결성 및 발행자 출처가 검증된 빌드 바이너리/이미지이다.
- **증적(Attestation / Evidence)**: 빌드 과정의 소스 ID, SBOM, VEX 결과가 암호학적으로 결속된 검증용 메타데이터이다.
- **운영 영향 추적(Operational Impact Tracking)**: 신규 Zero-day CVE 발생 시 이미 배포되어 실행 중인 인프라 산출물의 실시간 영향을 추적하는 기능이다.
- **출처•버전•해시 검증(Provenance, Version & Hash Verification)**: 수입된 소스 및 패키지의 해시값이 등록치와 동일한지 확인하는 단계이다.
- **격리 빌드•산출물 서명(Isolated Build & Artifact Signing)**: 임시 자격을 이용해 빌드하고 결과물에 서명을 부여하는 단계이다.
- **불변 저장•증적 결속(Immutable Storage & Attestation Binding)**: 바이너리를 불변 보관하고 SBOM 및 VEX 문서를 묶는 단계이다.
- **서명•영향•승격 정책 검증(Signature, Impact & Promotion Policy Verification)**: 전자서명 및 VEX 악용성을 검사해 승인 여부를 결정하는 단계이다.
- **배포•운영 구성 연계(Deployment & Runtime Configuration Linking)**: 배포 아티팩트를 런타임 환경과 1:1 바인딩하여 사후 영향을 관제하는 단계이다.

</details>

```text
[승인 소스·의존성]
          |
          v
1. 출처·버전·해시 검증
          |
          v
2. 격리 빌드·산출물 서명
          |
          `-- 서명 산출물·증적
                      |
                      v
[산출물 저장소]
          |
          v
3. 불변 저장·증적 결속
          |
          v
[배포 게이트]
          |
          v
4. 서명·영향·승격 정책 검증
          |
          v
[운영 환경]
          |
          v
5. 배포·운영 구성 연계
          |
          v
+----------------------------------+
| 운영 중 신규 취약점 발견         |
|                                  |
|  신규 취약점·배포 구성           |
|             |                    |
|             v                    |
|  영향 제품·조치 우선순위 환류    |
+----------------------------------+
```

### 동작 원리

1. 출처•버전•해시 검증: 소스•의존성 무결성 확인
2. 격리 빌드•산출물 서명: 샌드박스 빌드•전자서명
3. 불변 저장•증적 결속: 산출물•SBOM•VEX•출처 결속
4. 서명•영향•승격 정책 검증: 서명•악용성•승격 조건 대조
5. 배포•운영 구성 연계: 런타임 자산•신규 취약점 추적

#### 한줄 요약

- **해시•서명•증적•배포 게이트**와 런타임 영향 환류

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SBOM(Software Bill of Materials)**: 구성 부품 목록 및 패키지 간 상하 관계 가시화 문서이다.
- **VEX(Vulnerability Exploitability eXchange)**: 취약점이 해당 애플리케이션에서 실제 실행/악용 가능한지 여부를 증명하는 서술 문서이다.
- **출처 증명(Provenance / Attestation)**: 소프트웨어가 누구에 의해, 어떤 코드 commit과 빌드 파이프라인을 거쳐 생성되었는지 증명하는 이력서이다.

</details>

| 공급망 증적 문서 | 명세 및 역할 | 주요 포맷 및 규격 | 핵심 효과 |
|:---|:---|:---|:---|
| SBOM | 소프트웨어 포함 오픈소스 부품/버전 목록 제공 | SPDX, CycloneDX | 오픈소스•전이 의존성 가시화 |
| VEX | 특정 CVE 취약점의 실질적 악용 영향성 판단 기록 | CSAF, OpenVEX | 불필요한 보안 패치 공수 절감 및 조치 우선순위 산정 |
| 출처 증명 | 빌드 환경, 소스 Commit ID, 주체 무결성 보증 | SLSA v1.0, in-toto | 빌드 파이프라인 내 악성 코드 주입 및 아티팩트 위변조 차단 |

#### 한줄 요약

- SBOM은 구성 부품 식별, VEX는 실질적 악용성 판단, 출처 증명(SLSA)은 빌드 무결성을 상호보완 보증한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-218 SSDF 1.1 (NIST Secure Software Development Framework 1.1, SSDF)**: 미국 정부의 안전한 소프트웨어 개발 생명주기 지침 가이드라인이다.
- **SLSA 1.2 (Supply-chain Levels for Software Artifacts 1.2, SLSA)**: 구글이 주도하는 보안 공급망 산출물 무결성 보증 프레임워크 4단계 등급이다.
- **소프트웨어 개발 생명주기(Software Development Life Cycle, SDLC)**: 요구분석, 설계, 구현, 시험, 배포, 운영의 소프트웨어 개발 전 과정이다.
- **CISA VEX 최소 요구사항(CISA VEX Minimum Requirements)**: 미국 CISA가 규정한 VEX 문서의 5가지 필수 데이터 필드 요구 규격이다.
- **재현 빌드(Reproducible Build)**: 동일한 소스코드와 환경에서 재빌드 시 100% 동일한 바이너리 해시가 도출되는 검증 기법이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SDLC 전반의 공급망 보안 가이드 부재 | **NIST SP 800-218 SSDF 1.1** 프레임워크 준용 | 보안 개발 수명주기(SDLC) 내 공급망 통제 정착 |
| 빌드 산출물 위변조 및 악성 코드 주입 | **SLSA 1.2** 레벨 3 준수 및 **재현 빌드** 적용 | 빌드 파이프라인 오염 및 중간자 변조 공격 무력화 |
| VEX 문서 기계 읽기 호환성 저해 | **CISA VEX 최소 요구사항** 준수 | 보안 도구 간 VEX 악용 가능성 자동 해석 성능 향상 |

#### 한줄 요약

- NIST SSDF 1.1 및 SLSA 레벨 준수, CISA VEX 표준 적용, 재현 빌드 기법을 통해 소프트웨어 공급망 보안을 완성한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **산출물 승격 조건(Artifact Promotion Criteria)**: 서명 유효성, SLSA 출처 증명, VEX 상 고위험 CVE 미악용 판단이 완료되어 운영 환경 배포가 인가된 검증 상태이다.

</details>

- **산출물 승격 조건**을 충족하기 위해 전자서명, **SBOM**, **VEX**, **출처 증명**을 배포 게이트에서 연계 검증한다.

#### 한줄 요약

- **서명•SBOM•VEX•출처 증명** 검증 후 산출물 승격
