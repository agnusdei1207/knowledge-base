---
sidebar:
  order: 183
  label: "183. SBOM 소프트웨어 자재명세서"
  badge:
    text: "기출 • 85%"
    variant: note
title: "SBOM 소프트웨어 자재명세서 (Software Bill of Materials)"
date: "2026-08-14T04:04:00+09:00"
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

- **SBOM(Software Bill of Materials)**: SW 구성 오픈소스, 라이브러리, 의존성 관계를 기계 판독 가능한 형태(Machine-Readable)로 명세한 디지털 부품표.
- **Log4Shell**: Log4j 취약점 사태. 자사 내 취약 컴포넌트 식별 실패로 인한 SBOM 도입의 계기.
- **NTIA(National Telecommunications and Information Administration)**: 미 상무부 기관. 행정명령을 통해 연방 납품 SW 대상 SBOM 제출 의무화.

</details>

- 정의/개념: SW 구성요소•의존성•식별자를 담은 **SBOM**
- 배경/필요성: 외부 Component 증가로 **취약 제품•License 영향** 식별 지연

#### 한줄 요약

- 제품에 포함된 직접·전이 부품을 기계 판독 목록으로 남겨 영향 제품을 찾는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **전이 의존성(Transitive Dependency)**: 개발자가 직접 포함한 라이브러리가 다시 의존하고 있는 간접 라이브러리.

</details>

- **Data Fields**로 공급자•이름•Version•purl•관계 기록
- **SPDX**•**CycloneDX**로 생성•교환 자동화
- Release•산출물별 **SBOM 갱신•서명•배포 연결**

#### 한줄 요약

- 표준 식별자와 의존 경로를 제품 Version마다 갱신해야 자동 대조가 가능하다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SPDX(Software Package Data Exchange)**: 리눅스 재단 주도 ISO 표준(ISO/IEC 5962) SBOM 포맷. 라이선스 호환성 검증에 특화.
- **CycloneDX**: OWASP 주도 포맷. 취약점 분석 및 공급망 보안(AppSec) 목적의 최적화된 경량 규격.

</details>

```text
[SBOM]
 ├── [SCA Tool]
 ├── [Standard Format]
 ├── [Component ID]
 └── [VEX]
```

| 구성요소 | 책임 |
|---|---|
| SCA Tool | Source•Binary의 **Component**•**Dependency** 추출 |
| Standard Format | SPDX•CycloneDX로 **교환 Schema** 제공 |
| Component ID | **purl**•**Hash**로 부품과 산출물 식별 |
| VEX | 취약점의 **영향•악용 가능 상태**와 근거 전달 |

#### 한줄 요약

- SCA가 부품을 찾고 표준 문서가 관계를 담으며 VEX가 실제 영향 판단을 보완한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VEX(Vulnerability Exploitability eXchange)**: 취약점이 존재해도 구동 환경상 실제 악용(Exploit) 불가함을 명세하여 거짓 양성(False Positive)을 제거하는 상태서.

</details>

```text
[Build 산출물]
      │
      ▼
1. Component•Dependency 추출
      │
      ▼
2. SBOM 생성•검증
      │
      ▼
3. 산출물•SBOM 서명•연결
      │
      ▼
4. 취약점•VEX 상관 분석
      │
      ▼
5. 영향 제품 Patch•추적
      │
      ▼
[대응 결과 반환]
```

### 동작 원리

1. Component•Dependency 추출: Source•Binary 부품 식별
2. SBOM 생성•검증: 필수 Field와 관계 완전성 확인
3. 산출물•SBOM 서명•연결: Digest•Attestation 보존
4. 취약점•VEX 상관 분석: 영향 Version과 실행 가능성 평가
5. 영향 제품 Patch•추적: 우선순위•조치•잔여 위험 관리

#### 한줄 요약

- 새 취약점이 나오면 서명된 부품표로 배포 제품과 경로를 찾고 VEX 근거로 순서를 정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **바이너리 분석(Binary Analysis)**: 소스코드 없는 레거시 시스템을 역분석하여 포함 라이브러리 목록을 강제 추출하는 기법.

</details>

| 항목 | Source•Build-time SBOM | Binary•Run-time SBOM |
|:---|:---|:---|
| 대상 | 소스코드, 패키지 관리 파일 | 컨테이너 이미지, 실행 파일 |
| 강점 | 선언된 전이 의존성 추적 | 실제 산출물의 숨은 부품 보완 |
| 한계 | 미포함 개발 의존성 혼입 가능 | 난독화•정적 Linking 누락 가능 |
| 주요 목적 | 개발 제품 투명성 | 외부•Legacy 산출물 검증 |

#### 한줄 요약

- Build 시 생성을 정본으로 삼고 Binary 분석으로 실제 산출물 차이를 보완한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **purl**: `pkg:npm/lodash@4.17.21` 등 패키지 생태계 무관 전 세계 공통 고유 식별 주소 체계.

</details>

| 난제 | 원인 | 대책 |
|:---|:---|:---|
| 이름 오탐지 | 생태계별 동일 패키지명 | **purl** 식별자 강제 |
| 경고 폭탄 | 미사용 라이브러리 취약점 | **VEX** 동반 False Positive 제거 |
| 위변조 | 공급망 악성 부품 삽입 | **SLSA** 프레임워크 및 무결성 서명 |

#### 한줄 요약

- 이름 대신 purl•Hash를 쓰고 VEX 근거와 서명을 제품 Version에 함께 연결한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **공급망 보안(Software Supply Chain Security)**: 개발부터 운영까지 외부 라이브러리 오염을 막는 보안 체계.

</details>

- Release마다 **서명 SBOM**, 운영은 취약점•VEX•배포 자산 연결

#### 한줄 요약

- 빌드마다 제품 해시와 서명된 SBOM을 만들고 배포 자산·취약점·VEX를 연결해야 부품표가 실제 대응 도구가 된다.
