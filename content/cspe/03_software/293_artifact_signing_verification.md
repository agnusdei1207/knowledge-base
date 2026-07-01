---
title: "아티팩트 서명·검증 (Artifact Signing Verification)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 293
---

# 📖 【암기용】 개념 완전 이해

> 목적: 아티팩트 서명·검증을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 빌드 산출물에 전자서명을 붙이고 배포 시 서명자·무결성·출처를 확인하는 공급망 통제
- **왜 필요한가**: 레지스트리 변조, CI 계정 탈취, 중간자 공격으로 악성 이미지가 배포될 수 있다.
- **핵심 직관**: 택배 상자에 봉인과 발송자 확인서를 붙이고, 수령 시 봉인 훼손과 발송자를 확인하는 절차이다.

## 깊이 이해
- **배경·문제의식**: 배포 파이프라인은 소스, 빌드 서버, 레지스트리, 런타임으로 이어진다. 어느 지점이든 산출물이 바뀌면 정상 코드 검토를 통과한 것처럼 보일 수 있다.
- **작동 원리**: 빌드 후 이미지 digest를 계산하고 Cosign·GPG·Sigstore로 서명한다. Kubernetes admission controller는 digest, certificate identity, transparency log 기록을 확인한 뒤 실행을 허용한다.
- **비유**: 계약서에 도장을 찍는 것이 아니라, 계약서 해시와 서명자 신원을 공증 장부에 남겨 나중에 위조 여부를 확인하는 것이다.
- **구체 예시**: `registry/app@sha256:3a1b2c4d5e6f7890` digest를 Cosign으로 keyless 서명하고 Rekor transparency log에 기록한 뒤, Kyverno 정책으로 서명 없는 이미지를 차단한다.
- **흔한 오해·주의점**: 태그 서명만으로는 부족하다. `latest` 태그는 같은 이름으로 다른 digest를 가리킬 수 있으므로 digest 기준 검증이 필요하다.

## 연결 개념
- SLSA - 빌드 출처와 무결성 보증 수준
- SBOM - 서명 대상 산출물과 구성요소 연결
- Admission Control - 런타임 배포 전 정책 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 서명 알고리즘 나열보다 출처 증명, 무결성, 배포 차단 기준을 중심으로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 아티팩트 서명·검증은 빌드 산출물의 작성 주체와 변경 여부를 암호학적으로 확인하는 공급망 보증 절차이다.
> 2. **가치**: digest, certificate identity, transparency log를 결합해 서명 없는 이미지와 변조 이미지를 배포 전 차단한다.
> 3. **판단 포인트**: 태그가 아니라 digest를 기준으로 서명하고, CI 신원과 런타임 admission 정책을 연결해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 소프트웨어 공급망 무결성 이해 확인 | digest, 서명, 인증서, 투명성 로그, 검증 정책 | GPG 명령만 설명하고 배포 차단 누락 |
| CI/CD 보안 설계 확인 | 빌드 후 서명, 레지스트리 저장, admission 검증 | 개발자 로컬 서명만 제시 |
| 운영 통제 기준 확인 | keyless, key rotation, signer allowlist | 태그 기준 검증으로 설명 |

> 요약: 이 문제는 산출물 신뢰를 코드 리뷰가 아니라 암호학적 출처 증명과 런타임 정책으로 보장하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

아티팩트 서명·검증은 빌드 산출물의 무결성과 출처를 확인하는 통제이다. 컨테이너 이미지와 패키지가 레지스트리를 거쳐 배포되므로, 변조 산출물을 배포 전에 차단해야 한다. Sigstore·Cosign·SLSA 기반으로 CI 신원, digest, 투명성 로그를 연결한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Commit -> CI Build -> Artifact Digest -> Signing -> Registry
                                           / Transparency Log
Runtime Admission -> Signature Verify -> Policy Decision -> Deploy/Reject
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Digest | 산출물 변경 여부 식별 | SHA-256 기반 이미지 digest |
| Signer | digest에 전자서명 생성 | Cosign, GPG, Sigstore keyless |
| Transparency Log | 서명 이력 공개 장부 | Rekor로 서명 위조 탐지 |
| Policy Verifier | 배포 전 검증·차단 | Kyverno, OPA Gatekeeper |

> 요약: 구조는 digest 산출, 서명, 투명성 기록, admission 검증으로 공급망 무결성을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
빌드 완료 -> digest 계산 -> CI 신원으로 서명 -> 레지스트리 저장 -> 배포 요청 -> 서명 검증 -> 실행 허용/차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CI가 소스 커밋으로 아티팩트 빌드 | provenance에 commit SHA 포함 |
| 2 | 산출물 digest 계산 후 서명 | SHA-256 digest 기준 |
| 3 | 인증서·서명·로그 기록 저장 | Rekor inclusion proof 확인 |
| 4 | 런타임 admission에서 정책 평가 | signer allowlist 일치 |

> 요약: 동작은 빌드 시 서명하고 실행 시 검증하며, signer identity와 digest 일치 여부가 배포 허용 기준이다.

---

## Ⅳ. 특징

| 구분 | 무서명 배포 | 아티팩트 서명·검증 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 무결성 | 태그 신뢰 | digest 서명 검증 | 서명 없는 이미지 0건 |
| 출처 | 레지스트리 계정 의존 | CI OIDC identity 확인 | signer allowlist 100% 적용 |
| 감사 | 배포 로그 중심 | 투명성 로그·provenance | 1년 이상 보관 |
| 한계 | 통제 부재 | 키·정책 운영 필요 | key rotation 90~365일 |

> 요약: 서명·검증은 태그 신뢰를 digest 신뢰로 바꾸고, 배포 시점에 정책 기반 차단을 수행한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 태그 기반 배포 | digest+signature 기반 배포 | 컨테이너 운영, 다중 팀 배포 |
| 비용/성능 | 검증 지연 없음 | admission 검증 수십 ms | p95 admission 200ms 이하 |
| 운영/위험 | 레지스트리 탈취에 취약 | signer·policy 통제 | release signer 분리 필요 |

> 요약: 컨테이너와 자동 배포 환경은 digest 기반 서명과 admission 검증을 기본 통제로 둬야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 키 유출 | 장기 개인키 보관 | keyless OIDC, HSM/KMS | signer 비정상 사용 건수 |
| 정책 우회 | 예외 namespace 허용 | exception approval, audit | unsigned deploy 0건 |
| 태그 변조 | mutable tag 사용 | digest pinning | digest 미고정 배포 건수 |

> 요약: 키 유출, 정책 우회, 태그 변조는 keyless, 예외 감사, digest pinning으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서명 적용 | 릴리스 아티팩트 100% 서명 | registry scan |
| 검증 차단 | unsigned artifact 배포 0건 | admission audit |
| 출처 추적 | provenance commit 매핑 100% | SLSA attestation 조회 |

> 요약: 운영 성숙도는 서명 적용률, 배포 차단률, provenance 추적률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. GitHub Actions OIDC와 Cosign keyless로 컨테이너 digest를 서명하고 Rekor transparency log에 기록
2. Kubernetes에 Kyverno·OPA 정책을 적용해 signer allowlist와 digest pinning 미충족 이미지를 차단
3. SLSA provenance와 SBOM을 함께 attestation으로 저장해 릴리스별 소스 커밋·빌드 환경·의존성 추적

**결론 (2줄):**
- 기술사 판단: 자동 배포와 다중 레지스트리 환경은 태그 신뢰를 폐기하고 digest 서명·admission 검증을 필수 통제로 선택
- 향후 방향: SLSA, Sigstore, SBOM attestation 결합으로 빌드 출처부터 런타임 실행까지 연속 보증 필요

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | digest 계산, 서명, 검증 흐름 | 무서명 배포와 서명 배포 비교 |
| 요구사항 명시형 | "설계하시오", "보안 대책", "방안을 제시하시오" | CI 신원, keyless, admission 정책 | 키 유출, 정책 우회, 지표 |

> 요약: 설명형은 서명 원리, 설계형은 런타임 차단 정책과 공급망 보증 지표를 중심으로 전환한다.
