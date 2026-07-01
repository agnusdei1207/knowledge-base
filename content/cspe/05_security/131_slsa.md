---
title: "SLSA 공급망 보안 프레임워크 (SLSA)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 131
---

# 📖 【암기용】 개념 완전 이해

> 목적: SLSA를 처음 봐도 소프트웨어 공급망 보안 관점에서 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: SLSA는 소스부터 빌드·배포 아티팩트까지 변조를 막기 위한 공급망 보안 성숙도 프레임워크임
- **왜 필요한가**: 개발자가 작성한 코드가 운영 이미지가 되기 전까지 CI, 패키지 저장소, 빌드 스크립트, 의존성이 모두 공격면이 됨. SolarWinds, Codecov, 의존성 탈취 같은 사고는 결과물 서명만으로 설명되지 않음.
- **핵심 직관**: 제품에 원산지 증명서와 제조 공정 기록을 붙여, "누가·어디서·무엇으로·어떻게 만들었는지"를 검증하는 방식임.

## 깊이 이해
- **배경·문제의식**: 기존 취약점 관리는 CVE 패치와 이미지 스캔에 치우쳐 있었으나, 공격자는 빌드 서버·CI 토큰·오픈소스 의존성을 노림. SLSA는 결과물이 아니라 생산 과정의 신뢰를 단계별로 올림.
- **작동 원리**: Build Track은 provenance 존재, hosted build platform, hardened build 순으로 보증 수준을 높임. Source Track은 소스 제어, 리뷰, 브랜치 보호, 변경 이력 통제를 다룸.
- **비유**: 약품 제조에서 원료 입고, 생산 설비, 배치 번호, 검사 기록을 남기는 GMP와 유사함. 소프트웨어도 소스·빌드·아티팩트의 이력을 남겨야 리콜과 책임 추적이 가능함.
- **구체 예시**: GitHub Actions에서 커밋 SHA로 컨테이너 이미지를 빌드하고, SLSA provenance를 발급한 뒤 배포 단계에서 subject digest·builder id·source repo를 검증함.
- **흔한 오해·주의점**: SLSA는 취약점 스캐너가 아님. CVE 탐지는 SBOM·SCA가 담당하고, SLSA는 빌드 무결성·출처·조작 방지 수준을 증명함.

## 연결 개념
- SBOM·VEX: 구성요소와 취약점 영향 여부를 설명하는 자료
- Sigstore·Cosign: provenance와 아티팩트 서명을 검증하는 구현 수단
- DevSecOps: CI/CD 단계에 정책 검증과 배포 차단을 넣는 운영 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SLSA는 도구명이 아니라 소스·빌드·아티팩트 provenance를 검증 가능한 증거로 만드는 공급망 보안 성숙도 모델임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SLSA (Supply-chain Levels for Software Artifacts)는 소프트웨어 생산 과정의 출처·빌드·아티팩트 무결성을 단계별 요구사항으로 통제하는 프레임워크임.
> 2. **가치**: provenance, isolated build, tamper-resistant log, policy gate를 통해 CI 토큰 탈취·빌드 스크립트 변조·패키지 바꿔치기를 탐지·차단함.
> 3. **판단 포인트**: SLSA Level 자체보다 builder 신뢰, provenance 검증 자동화, 배포 차단 정책, SBOM·서명 연계 여부가 채점 포인트임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공급망 공격면 식별 역량 확인 | 소스, 의존성, 빌드, 아티팩트, 배포 단계별 변조 지점 | SLSA를 단순 오픈소스 보안 캠페인으로 설명 |
| 성숙도 모델 적용 판단 확인 | Build Track L1~L3, Source Track, provenance 검증 | 레벨 번호만 암기하고 통제 요건 누락 |
| DevSecOps 통제 설계 확인 | SBOM, Sigstore, OPA, admission control 연계 | 서명 생성만 쓰고 배포 시 검증·차단 누락 |

> 요약: SLSA 문제는 공급망 공격 시나리오를 provenance 기반 통제와 배포 정책으로 연결하는 답안이 요구됨.

---

## Ⅰ. 개요 및 필요성

- 개요: SW 공급망 무결성 프레임워크
- 배경: 오픈소스 의존성, CI/CD, 컨테이너 레지스트리, 배포 자동화가 연결되면서 코드 작성 후 배포 전까지 변조 지점이 증가함.
- 필요성: SLSA v1.0 provenance와 build level 요구사항으로 산출물이 검증된 절차에서 생성됐는지 확인해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Repo -> Build Platform -> Provenance Attestation -> Artifact Registry
                    +-> SBOM / Signature / Policy Gate
Consumer Verify -> Deploy Allow / Reject
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Track | 소스 제어, 변경 승인, 브랜치 보호 통제 | 코드 리뷰 2인 승인, protected branch 기준 |
| Build Track | 빌드 플랫폼과 provenance 보증 수준 정의 | L1 provenance, L2 hosted build, L3 hardened build |
| Provenance | builder, source, materials, subject digest 기록 | SLSA provenance, in-toto attestation 활용 |
| Policy Gate | 배포 전 서명·출처·빌더 검증 | OPA, Kyverno, admission controller 연계 |

> 요약: SLSA 구조는 소스 통제, 신뢰 빌드, provenance 발급, 소비자 검증을 하나의 공급망 신뢰 체인으로 묶음.

---

## Ⅲ. 동작원리 및 흐름도

```text
Commit -> Protected Review -> Hosted Build -> Provenance Generate
-> Artifact Sign -> Registry Store -> Deploy Policy Verify -> Runtime Deploy
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 커밋·태그 생성 및 변경 승인 | branch protection, CODEOWNERS, 2인 리뷰 |
| 2 | 격리된 CI 빌드 수행 | reusable workflow, ephemeral runner, secret scope |
| 3 | provenance·SBOM·서명 생성 | subject digest, builder id, source URI 일치 |
| 4 | 배포 전 정책 검증 | trusted builder allowlist, signature verification |
| 5 | 감사·사후 추적 | immutable log, build run id, artifact digest 보관 |

> 요약: SLSA는 생성 시점의 증거를 배포 시점의 정책 검증으로 연결해 미승인 아티팩트 실행을 차단함.

---

## Ⅳ. 특징

| 구분 | 기존 방식 | SLSA 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 통제 범위 | 이미지 스캔·CVE 중심 | 소스·빌드·아티팩트 전 단계 | 빌드 provenance 100% 첨부 |
| 신뢰 근거 | 레지스트리 태그·수동 승인 | digest·builder id·attestation | tag 대신 SHA256 digest 검증 |
| 운영 방식 | 배포 후 탐지 | 배포 전 정책 차단 | 미서명 이미지 admission deny |
| 한계 | 취약점 영향 설명 부족 | SBOM·VEX와 결합 필요 | CVE false positive는 VEX로 보완 |

> 요약: SLSA는 "무엇이 들어있는가"보다 "어떻게 만들어졌는가"를 검증하며, SBOM·서명과 결합해야 공급망 통제가 완성됨.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SCA·이미지 스캔 단독 | SLSA+SBOM+Cosign 체인 | 배포 전 provenance 검증 필요 시 |
| 비용/성능 | CI 단계 1~2분 스캔 추가 | attestation·서명·정책 검증 추가 | 릴리스 빈도 일 10회 이상이면 자동화 필수 |
| 운영/위험 | 담당자 승인 중심 | 정책 기반 허용·거부 | 미승인 builder 사용률 0% 목표 |

> 요약: SLSA는 릴리스가 잦고 외부 의존성이 많은 조직에서 수동 승인보다 정책 검증 비용 대비 추적성이 높음.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 위조 provenance | self-hosted runner 탈취, signing key 유출 | ephemeral runner, OIDC keyless signing, key rotation | trusted builder mismatch 0건 |
| 정책 우회 | 긴급 배포 예외 남용 | break-glass 승인 2인, TTL 24시간, 감사 로그 | 예외 배포 월 3건 이하 |
| 의존성 변조 | lockfile 미고정, package hijacking | lockfile, private mirror, SCA, VEX | dependency drift 0건 |

> 요약: SLSA 운영 리스크는 증거 위조와 예외 남용이므로 빌더 신뢰와 예외 TTL을 지표로 통제해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| provenance 적용률 | 운영 배포 아티팩트 100% | registry metadata, CI attestation scan |
| 검증 차단률 | 미서명·불일치 artifact 100% deny | admission controller audit |
| 추적성 | 사고 artifact에서 commit·builder 5분 내 역추적 | SIEM, build log, Rekor log |

> 요약: SLSA 성공 여부는 레벨 선언이 아니라 provenance 적용률, 정책 차단률, 역추적 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. CI/CD: GitHub Actions OIDC, ephemeral runner, protected branch, reusable workflow로 SLSA Build L2 이상 빌드 경로 고정.
2. 아티팩트: SBOM(SPDX 또는 CycloneDX), SLSA provenance, Cosign 서명을 SHA256 digest 기준으로 레지스트리에 저장.
3. 배포 통제: OPA Gatekeeper 또는 Kyverno로 trusted builder, certificate identity, source repo allowlist 불일치 시 admission deny.

**결론 (2줄):**
- 기술사 판단: 외부 의존성과 자동 배포가 많은 서비스는 SLSA+SBOM+서명 검증을 최소 기준으로 두고, 핵심 업무는 hardened build까지 적용함.
- 향후 방향: SLSA Source Track, 하드웨어 attestation, VEX 자동화가 결합되어 공급망 증거를 지속 검증하는 방향으로 전개됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SLSA를 설명하시오", "공급망 보안을 기술하시오" | Source·Build Track과 provenance 생성 흐름 | SBOM·서명·정책 게이트 연계 |
| 요구사항 명시형 | "설계하시오", "도입 방안을 제시하시오", "비교하시오" | CI/CD 단계별 검증 지점과 배포 차단 흐름 | 레벨 선택 기준, 리스크 대응, 점검 지표 |

> 요약: 설명형은 SLSA 구조와 레벨을 넓게 쓰고, 설계·방안형은 provenance 검증과 admission deny 정책을 중심으로 목차를 전환함.
