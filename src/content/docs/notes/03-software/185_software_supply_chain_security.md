---
sidebar:
  order: 185
  label: "185. 소프트웨어 공급망 보안"
  badge:
    text: "기출 • 85%"
    variant: note
title: "소프트웨어 공급망 보안"
date: "2026-08-14T04:12:00+09:00"
tags:
  - "notes-software"
weight: 185
extra:
  question_no: "185"
  source_status: "기출"
  source_history: "128회, 134회, 135회"
  priority: 85
  priority_note: "개발•빌드•배포 신뢰사슬 반복 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Software Supply Chain Security (소프트웨어 공급망 보안)**: 소스 코드 작성부터 빌드, 테스트, 패키징, 배포에 이르는 소프트웨어 생명주기(SDLC) 전 과정에서 의도적인 위조나 악성코드 삽입을 방어하는 보안 체계.
- **SolarWinds Hack (솔라윈즈 사태)**: 2020년 발생한 대형 사건으로, 해커가 솔라윈즈의 '오리온' 네트워크 모니터링 소프트웨어의 빌드 시스템을 장악하고 악성코드를 심어, 업데이트를 받은 미국 정부 및 수만 개 기업이 뚫린 공급망 공격의 대표 사례.
- **Supply Chain Attack (공급망 공격)**: 타깃 기업을 직접 해킹하기 어려울 때, 그 기업이 신뢰하고 사용하는 서드파티 소프트웨어나 오픈소스 라이브러리에 백도어를 심어 간접 침투하는 우회 공격 기법.

</details>

- 정의/개념: Source부터 배포 Artifact까지 보호하는 **공급망 보안**
- 배경/필요성: 외부 의존성•Build System 침해는 **신뢰 Update 경로**로 확산

#### 한줄 요약

- 소스 코드·빌드 주체·패키징 출처가 모두 검증된 산출물만 배포 환경에 적용하도록 개발부터 배포까지 증적이 연속되어야 한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **SLSA (Supply-chain Levels for Software Artifacts)**: 구글이 제안한 소프트웨어 공급망 무결성 프레임워크로, 빌드 프로세스의 보안 수준을 1단계부터 4단계까지 정의하여 위변조 저항성을 정량화한 국제 표준.

</details>

- **Provenance (출처 증명)**: "이 바이너리는 어떤 소스 코드(Git Commit)에서, 어떤 빌드 서버 환경(CI)을 거쳐, 누가 만들었는가?"를 암호학적으로 증명하는 메타데이터 문서.
- **Reproducible Build (재현 가능한 빌드)**: 똑같은 소스코드와 똑같은 의존성을 넣고 컴파일하면, 언제 어디서든 바이트 단위까지 100% 똑같은 해시값을 가진 바이너리가 나와야 한다는 엄격한 빌드 규칙 (SLSA 최고 등급 요건).
- **Hermetic Build (격리된 빌드)**: 빌드 과정 중에 인터넷 연결을 완전히 차단하여, 해커가 외부에서 악성 패키지를 몰래 다운로드하거나 악성 스크립트를 실행하는 것을 원천 봉쇄하는 격리 기법.

#### 한줄 요약

- 승인된 의존성으로 격리 빌드하고 산출물 다이제스트에 SBOM과 빌드 증적을 결합해야 변조를 탐지할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Policy Gate (정책 게이트)**: 배포(Deployment) 직전에 쿠버네티스나 배포 서버 앞단에서, 해당 컨테이너 이미지에 서명(Signature)과 출처(Provenance)가 올바르게 붙어있는지 확인하고 미달 시 배포를 차단하는 검문소.

</details>

```text
[Secure Supply Chain]
 ├── [Source Control]
 ├── [Trusted Builder]
 ├── [Attestation Store]
 └── [Policy Gate]
```

| 구성요소 | 책임 |
|---|---|
| Source Control | **Review•서명•Branch 보호**와 입력 이력 관리 |
| Trusted Builder | 격리•일회 환경에서 **승인 입력만 Build** |
| Attestation Store | SBOM•Provenance•서명을 **Digest에 결속** |
| Policy Gate | 소비 지점에서 **Identity•Signature•Policy** 검증 |

#### 한줄 요약

- 소스 통제가 의존성을 승인하고 빌더가 산출물을 생성하면 증적 체계와 저장소가 이력을 불변 보존하고 정책 게이트가 배포를 결정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Immutable Input (불변 입력)**: 빌드 시스템에 들어가는 모든 재료(소스코드, 의존성 라이브러리)의 버전과 해시값을 사전에 정확히 고정(Lock)하여, 중간에 내용이 몰래 바뀌는 것을 막는 통제.

</details>

```text
[공급망 보안 파이프라인 (SLSA 기반)]
 1. [불변 입력 확정] : Version•Digest•Source 고정
          │
 2. [격리 빌드 수행] : Ephemeral Builder에서 Build
          │
 3. [증적 생성•결속] : Artifact+SBOM+Provenance 서명
          │
 4. [불변 저장•배포 요청] : Registry에 Artifact•증적 보관
          │
 5. [정책 검증•운영 배포] : 승인 Artifact만 실행
```

### 동작 원리

1. **불변 입력 확정**: Source•Dependency Version•Digest 고정
2. **격리 빌드 수행**: 승인 Builder와 최소 권한 자격 증명 사용
3. **증적 생성•결속**: Artifact Digest에 SBOM•Provenance 서명
4. **불변 저장•배포 요청**: Registry에 Artifact와 증적 보관
5. **정책 검증•운영 배포**: 소비 지점에서 신뢰 Policy 강제

#### 한줄 요약

- 정책 게이트는 제품 이름이 아니라 지문을 기준으로 부품표와 제조 서명을 대조한 뒤 같은 지문만 운영에 보낸다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Detection (탐지)**: 빌드가 끝난 뒤에 SBOM과 산출물을 까보며 취약점(CVE)이나 서명 변조를 사후에 찾아내는 모니터링 방식 (SCA 스캔, 컨테이너 스캔).

</details>

| 비교 항목 | Prevention (예방적 통제) | Detection (탐지 및 복구 통제) |
|:---|:---|:---|
| **적용 시점** | **코딩 및 빌드 파이프라인 동작 중** | **빌드 완료 후 저장소 및 운영계 배포 시** |
| **핵심 기법** | **의존성 Lock, GPG 커밋 서명, 격리 빌드** | **SBOM 생성, 서명 검증(Cosign), 취약점 스캔**|
| **대응 목표** | **악성 코드가 빌드 결과물에 섞이는 것을 차단** | **이미 섞인 악성 결과물이 운영에 나가는 것을 차단**|
| **대표 도구** | GitHub Branch Protection, SLSA Builder | Syft(SBOM), Trivy(스캔), OPA(정책) |

#### 한줄 요약

- 예방은 비승인 의존성의 유입을 차단하고 탐지는 산출물의 서명·증적을 검증하며 대응은 동일 다이제스트의 산출물을 추적해 철회한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Dependency Confusion (의존성 혼동 공격)**: 사내 전용으로 쓰는 프라이빗 패키지(예: `my-corp-auth`)와 똑같은 이름의 악성 패키지를 공개 저장소(npm, PyPI)에 더 높은 버전으로 올리면, 패키지 매니저가 공개 저장소의 악성 패키지를 낚아채서 설치해 버리는 해킹 기법.
- **Typosquatting (타이포스쿼팅)**: 유명한 패키지 이름(`requests`)과 비슷하게 철자를 꼬아서(`requsts`) 악성 패키지를 올리고, 개발자의 오타를 유도하여 악성코드를 퍼뜨리는 공격.

</details>

| 공급망 해킹 기법 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 의존성 혼동 공격** | 패키지 매니저의 Public 우선순위 로직 | **내부 레지스트리(Nexus) 우선 검색 및 Hash 값 고정(Lock)**|
| **2. 타이포스쿼팅 오타**| 개발자의 휴먼 에러 및 서드파티 신뢰 | **패키지 다운로드 전 화이트리스트 및 퍼블리셔(서명) 검증**|
| **3. CI/CD 서버 장악** | CI 스크립트 변조 또는 환경변수 탈취 | **단기 자격 증명(OIDC) 사용 및 Ephemeral(일회성) 빌드 적용**|

> 사례: **구글이 주도하는 OpenSSF 프레임워크(SLSA, Sigstore)를 활용한 쿠버네티스 생태계의 무서명(Keyless) 서명 및 투명성 로그(Rekor) 적용 사례**

#### 한줄 요약

- 빌드 작업마다 짧게 쓰는 자격증명을 발급하고 소스·바이너리 부품표를 대조하면 공격자가 훔칠 열쇠와 숨길 부품이 줄어든다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Attestation (아테스테이션 / 증명)**: "이 바이너리는 정상적인 파이프라인에서 내가 정당하게 빌드했다"는 것을 증명하기 위해, Provenance 정보에 암호학적 서명을 덧붙인 최종 문서.

</details>

- 중요 Artifact는 **격리 Build•Provenance•서명 Policy Gate** 적용

#### 한줄 요약

- 승인 입력에서 만든 사실을 같은 Digest의 증적으로 입증하고 소비 지점에서 다시 검사하며 문제 지문을 즉시 철회해야 한다.
