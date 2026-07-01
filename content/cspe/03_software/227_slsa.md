---
title: "SLSA 공급망 보안 프레임워크 (SLSA)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 227
---

# 📖 【암기용】 개념 완전 이해

> 목적: SLSA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 소프트웨어 빌드·출처·무결성을 단계적으로 보증하기 위한 공급망 보안 프레임워크
- **왜 필요한가**: 공격자는 소스코드보다 CI, 빌드 스크립트, 패키지 저장소, 배포 artifact를 조작해 제품에 악성 코드를 넣는다
- **핵심 직관**: SLSA는 "누가 어떤 소스로 어디서 빌드했는지"를 위조하기 어렵게 만드는 출처 보증 체계이다

## 깊이 이해
- **배경·문제의식**: SolarWinds, Codecov, dependency confusion 사례처럼 빌드와 배포 경로가 공격 표면이 되었다. 최종 바이너리만 검사하면 빌드 중 삽입된 악성 변경을 추적하기 어렵다.
- **작동 원리**: 버전관리, 빌드 서비스, provenance, 서명, 격리된 빌더, 검증 정책을 연결해 artifact가 신뢰 가능한 프로세스에서 생성됐음을 증명한다.
- **비유**: 의약품이 원료, 제조공장, 품질검사, 유통 이력을 추적하듯 SLSA는 소스, 빌더, 산출물, 서명 이력을 추적한다.
- **구체 예시**: GitHub Actions에서 빌드한 container image에 SLSA provenance와 cosign 서명을 붙이고 Kubernetes admission controller가 서명과 builder identity를 검증한다.
- **흔한 오해·주의점**: SLSA는 취약점 스캐너가 아니다. 빌드 무결성, 출처 증명, 변조 방지를 다루며 CVE 관리는 SBOM/SCA와 함께 운영한다.

## 연결 개념
- SBOM - artifact 구성요소 목록
- in-toto - 공급망 단계별 attestation 표현
- Sigstore/cosign - artifact 서명과 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SLSA는 레벨 명칭보다 소스 보호, 빌드 격리, provenance 생성, 서명 검증, 배포 차단 정책을 연결해 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SLSA는 소프트웨어 artifact가 신뢰 가능한 소스와 빌드 절차에서 생성됐음을 증명하는 공급망 보안 프레임워크이다.
> 2. **가치**: 빌드 조작, dependency confusion, artifact 변조를 provenance와 서명 검증으로 탐지·차단한다.
> 3. **판단 포인트**: 소스 보호, 빌드 서비스 신뢰성, provenance, non-falsifiable attestation, 배포 검증 정책이 평가 축이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공급망 보안 프레임워크 이해 확인 | SLSA, provenance, builder, artifact | CVE 스캐너로 오해 |
| 빌드 무결성 설계 확인 | hermetic build, isolated builder, signed attestation | 소스코드 보안만 설명 |
| 운영 적용 판단 확인 | CI/CD 서명, admission 검증, 정책 차단 | 생성만 하고 배포 검증 누락 |

> 요약: 이 문제는 취약점 탐지가 아니라 빌드 출처와 산출물 무결성 검증을 요구한다.

---

## Ⅰ. 개요 및 필요성

SLSA는 SW 공급망 무결성 프레임워크이다. 공격자는 코드 저장소, CI, 빌드 서버, 패키지 저장소를 조작해 정상 릴리스처럼 배포한다. SLSA는 provenance와 서명을 통해 artifact 출처를 검증한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Repo -> Controlled Build Service -> Artifact
-> Provenance/Attestation -> Signature
-> Policy Verification -> Deployment
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Control | 코드 변경 승인과 이력 관리 | branch protection, 2인 리뷰 |
| Build Service | 격리된 환경에서 빌드 수행 | hosted builder, ephemeral runner |
| Provenance | 소스, 빌더, 명령, 산출물 digest 증명 | in-toto statement |
| Policy Verifier | 서명·출처·레벨 검증 | admission controller, CI gate |

> 요약: SLSA 구조는 통제된 소스, 신뢰 빌더, provenance, 서명, 배포 검증으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 변경 -> 리뷰/승인 -> 격리 빌드 실행
-> artifact digest 생성 -> provenance 작성
-> 서명 -> registry 저장 -> 배포 전 정책 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | branch protection과 코드 리뷰 | 2인 승인 100% |
| 2 | 신뢰 빌더에서 reproducible/hermetic build 수행 | 수동 빌드 배포 0건 |
| 3 | provenance와 artifact 서명 | digest 매핑 100% |
| 4 | 배포 전 서명·builder identity 검증 | unsigned artifact 차단 100% |

> 요약: SLSA는 빌드 이전 승인부터 배포 직전 검증까지 artifact 신뢰 체인을 만든다.

---

## Ⅳ. 특징

| 구분 | 일반 CI/CD | SLSA 적용 | 판단 수치 |
|:---|:---|:---|:---|
| 출처 증명 | 빌드 로그 중심 | provenance와 digest | provenance 생성률 100% |
| 빌드 신뢰 | 공유 runner 의존 | 격리·통제 builder | 수동 artifact 0건 |
| 배포 검증 | 이미지 태그 신뢰 | 서명·builder 검증 | unsigned 배포 차단 100% |
| 한계 | 일부 위변조 추적 가능 | 정책·도구 통합 필요 | 검증 실패 MTTR 4시간 |

> 요약: SLSA는 빌드 결과를 믿는 방식에서 출처와 생성 절차를 검증하는 방식으로 전환한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | SLSA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | CI 로그와 registry 태그 | provenance+signature+policy | 외부 배포·금융·공공 서비스 |
| 비용/성능 | 배포 경로 단순 | 서명·검증 단계 추가 | 검증 지연 p95 2초 이하 |
| 운영/위험 | 빌드 조작 탐지 지연 | 무서명 배포 차단 | critical service 100% 적용 |

> 요약: SLSA는 배포 속도보다 artifact 신뢰성과 감사 추적이 요구되는 시스템에 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Provenance 위조 | self-hosted runner 탈취 | hosted/ephemeral builder, OIDC | builder identity 검증 100% |
| 서명키 노출 | 장기 키 보관 | keyless signing, KMS/HSM | key rotation 90일 |
| 정책 우회 | 예외 배포 | admission controller, break-glass 기록 | 우회 배포 0건 |

> 요약: SLSA 리스크는 빌더 신뢰, 키 관리, 정책 우회이며 OIDC와 배포 차단으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 출처 커버리지 | 릴리스 artifact provenance 100% | CI attestation audit |
| 배포 통제 | unsigned artifact 차단 100% | admission log |
| 소스 보호 | main branch 직접 push 0건 | VCS audit |

> 요약: 성숙도는 provenance 생성률, 무서명 차단률, branch 보호 위반 건수로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Git branch protection, mandatory review 2인, CODEOWNERS, OIDC 기반 CI 권한으로 소스와 빌드 트리거를 통제
2. GitHub Actions SLSA generator, in-toto, cosign으로 provenance와 artifact 서명을 생성하고 registry digest와 연결
3. Kubernetes admission controller 또는 CI release gate에서 서명, builder identity, provenance predicate를 검증해 미충족 artifact 배포 차단

**결론 (2줄):**
- 기술사 판단: 외부 배포 artifact와 핵심 서비스 이미지는 SLSA provenance와 서명 검증을 릴리스 조건으로 지정
- 향후 방향: SLSA는 SBOM, VEX, OSSF Scorecard, policy-as-code와 결합되어 공급망 보안 성숙도 지표로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SLSA를 설명하시오" | 소스 승인, 빌드, provenance, 서명 흐름 | 일반 CI/CD 대비 특징 |
| 요구사항 명시형 | "공급망 보안 설계를 제시하시오" | builder 격리, 검증 정책, 배포 차단 절차 | 키·정책 우회·provenance 리스크 대응 |

> 요약: 설명형은 프레임워크 구성, 설계형은 provenance 검증과 배포 차단 기준으로 전환한다.
