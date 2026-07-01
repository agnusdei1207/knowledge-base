---
title: "SLSA 공급망 보안 프레임워크 (Supply-chain Levels for Software Artifacts)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 301
---

# 📖 【암기용】 개념 완전 이해

> 목적: SLSA를 소프트웨어 산출물이 어디서, 무엇으로, 어떻게 빌드됐는지 증명하는 공급망 보안 성숙도 모델로 이해하게 만든다.

## 한눈에
- **개요**: 빌드 산출물의 출처와 무결성을 단계별로 증명하는 OpenSSF 프레임워크
- **왜 필요한가**: 공격자가 소스 저장소, 빌드 서버, 패키지 저장소 중 한 곳만 장악해도 정상 배포물처럼 악성 산출물을 유통할 수 있다.
- **핵심 직관**: 제품 박스의 봉인보다 제조 공정 기록, 작업자 신원, 부품 출처를 함께 확인하는 방식임.

## 깊이 이해
- **배경·문제의식**: SolarWinds, Codecov, 패키지 타이포스쿼팅 사례는 실행 파일보다 빌드 과정과 의존성 체인이 공격 표면임을 보였다.
- **작동 원리**: SLSA는 provenance, build platform, source, dependency 트랙으로 산출물 생성 과정을 증명하고, build track은 L0~L3로 빌드 신뢰 수준을 표현한다.
- **비유**: 음식 원산지 증명서가 재료, 조리장, 조리 시간, 검수자를 남기듯 SLSA provenance는 입력, 빌더, 명령, 산출물 해시를 남긴다.
- **구체 예시**: 컨테이너 이미지를 GitHub Actions에서 빌드한 뒤 in-toto provenance와 Sigstore 서명을 붙이면 배포 게이트에서 커밋 SHA와 이미지 digest 일치 여부를 검증할 수 있다.
- **흔한 오해·주의점**: SLSA는 취약점 스캐너가 아니다. CVE 탐지는 SCA/SBOM 영역이고, SLSA는 산출물이 기대한 절차로 생성됐는지 검증하는 프레임워크다.

## 연결 개념
- SBOM — 산출물 내부 구성요소 명세
- Sigstore — 산출물 서명과 투명성 로그
- NIST SSDF — 보안 개발 활동 통제 프레임워크

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: SLSA는 공급망 보안 용어 나열이 아니라 빌드 provenance, 빌더 신뢰, 산출물 검증을 성숙도 단계로 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SLSA는 소스에서 산출물까지의 빌드 경로를 provenance와 빌드 플랫폼 통제로 증명하는 공급망 보안 프레임워크임.
> 2. **가치**: 악성 빌드, 산출물 바꿔치기, 위조 패키지를 배포 전 정책 게이트에서 차단함.
> 3. **판단 포인트**: build level, provenance 서명, hermetic build, artifact digest, 배포 정책 연계가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공급망 보안 성숙도 이해 확인 | SLSA L0~L3, provenance, 빌드 플랫폼 신뢰 | 취약점 스캔 도구로만 설명 |
| DevSecOps 적용 역량 확인 | CI/CD 빌드 증명, 서명, 정책 게이트 | 문서 감사 수준으로 축소 |
| 표준 연계 판단 확인 | SBOM, Sigstore, in-toto, SSDF 연계 | SBOM과 SLSA 역할 혼동 |

> 요약: 이 문제는 SLSA를 빌드 산출물 무결성 증명과 배포 정책 통제로 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 빌드 신뢰도 성숙도 모델
- 배경: 소스 코드가 안전해도 빌드 서버, 의존성, 패키지 저장소가 변조되면 악성 산출물이 배포됨.
- 필요성: 배포 전 artifact digest, provenance, 서명 검증을 자동화해 위조 산출물 반입을 차단해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Repo -> Build Platform -> Provenance Attestation -> Artifact Registry
              +-> Dependency / SBOM
              +-> Signature / Transparency Log -> Deployment Policy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Track | 소스 변경 주체와 승인 절차 통제 | branch protection, review |
| Build Track | 빌더와 입력, 명령, 산출물 해시 증명 | SLSA L0~L3 |
| Provenance | 누가 무엇으로 빌드했는지 기록 | in-toto attestation |
| Policy Gate | 서명·provenance 조건 검사 | admission controller |

> 요약: SLSA는 소스, 빌드, 증명, 배포 정책을 연결해 산출물 생성 경로를 검증 가능한 데이터로 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 변경 -> 승인 / 태그 -> 격리 빌드 -> provenance 생성
-> artifact 서명 -> registry 저장 -> 배포 전 정책 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 소스 변경과 승인 기록 확인 | commit SHA, reviewer |
| 2 | 신뢰 빌더에서 재현 가능한 입력으로 빌드 | builder identity |
| 3 | provenance와 artifact digest 생성 | schema, digest match |
| 4 | 서명·투명성 로그 등록 후 배포 게이트 검사 | signature verify |

> 요약: SLSA는 빌드 시점 증명을 생성하고 배포 시점에 증명과 산출물 해시를 대조한다.

---

## Ⅳ. 특징

| 구분 | SLSA 적용 전 | SLSA 적용 후 | 판단 기준 |
|:---|:---|:---|:---|
| 빌드 추적 | 빌드 로그 중심 | signed provenance | 산출물별 추적 가능성 |
| 신뢰 근거 | 운영자 수동 확인 | 빌더 신원과 해시 검증 | 정책 자동화 |
| 단계 표현 | 통제 수준 불명확 | L0~L3 성숙도 | 도입 로드맵 |
| 한계 | 취약점 자체 제거 아님 | SCA/SBOM 병행 필요 | CVE 대응 범위 |

> 요약: SLSA는 취약점 탐지보다 빌드 과정 변조 방지와 산출물 출처 증명에 초점을 둔다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 통제 대상 | 릴리스 파일 서명 | 빌드 과정과 provenance | 위조 산출물 차단 필요 |
| 적용 방식 | 수동 릴리스 승인 | CI/CD 자동 attest | 배포 빈도 |
| 연계 기술 | SBOM 단독 | SBOM+SLSA+Sigstore | 감사·배포 정책 |

> 요약: 외부 패키지와 컨테이너 배포가 많은 조직은 SBOM만으로 부족하므로 SLSA 증명을 배포 조건에 넣어야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 증명 위조 | 빌더 신원 검증 부재 | OIDC 기반 keyless signing | signature verification rate |
| 빌드 오염 | 외부 네트워크와 비고정 의존성 | hermetic build, dependency pinning | reproducible build pass |
| 정책 우회 | 수동 배포 경로 잔존 | admission policy 강제 | unsigned deploy count |

> 요약: SLSA 리스크는 증명 위조, 빌드 오염, 정책 우회이며 서명·격리·게이트 강제로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| provenance | 릴리스 artifact 100% attestation | registry metadata 대조 |
| 서명 검증 | 배포 전 signature verify 통과 | admission log |
| 성숙도 | 핵심 서비스 SLSA Build L2 이상 | SLSA checklist |

> 요약: 도입 성과는 문서 제출보다 릴리스 산출물별 provenance와 서명 검증률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CI/CD에서 artifact digest, builder identity, source commit을 포함한 in-toto provenance를 생성하고 registry에 저장함.
2. Sigstore cosign으로 컨테이너 이미지와 provenance를 서명하고 Rekor transparency log 검증을 배포 정책에 연결함.
3. 핵심 서비스부터 SLSA Build L1 -> L2 -> L3 순서로 빌더 격리, 의존성 고정, 정책 게이트를 단계 적용함.

**결론 (2줄):**
- 기술사 판단: 공급망 공격 가능성이 높은 서비스는 취약점 스캔보다 빌드 출처 증명을 먼저 자동화해야 함.
- 향후 방향: SLSA는 SBOM, VEX, Sigstore와 결합해 산출물 구성·취약점 영향·빌드 무결성을 함께 증명하는 방향으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SLSA를 설명하시오" | provenance 생성과 배포 검증 흐름 | L0~L3 성숙도와 SBOM 차이 |
| 요구사항 명시형 | "공급망 보안 방안을 제시하시오" | CI/CD attest, 서명, 정책 게이트 | 증명 위조·빌드 오염 대응 |

> 요약: 설명형은 성숙도와 구조를, 방안형은 빌드 증명 자동화와 배포 차단 정책을 중심으로 작성한다.
