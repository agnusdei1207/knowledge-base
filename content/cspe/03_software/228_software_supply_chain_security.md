---
title: "소프트웨어 공급망 보안 (Software Supply Chain Security)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 228
---

# 📖 【암기용】 개념 완전 이해

> 목적: 소프트웨어 공급망 보안을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 소스코드, 의존성, 빌드, 패키지, 배포, 운영까지 SW 생산 전 과정을 보호하는 보안 체계
- **왜 필요한가**: 공격자는 기업 내부 코드를 직접 공격하지 않고 오픈소스 패키지, CI 토큰, 빌드 산출물, 업데이트 서버를 노린다
- **핵심 직관**: 제품 코드만 검사하는 시대에서 "코드가 만들어지고 전달되는 경로 전체"를 검증하는 시대로 바뀐 것이다

## 깊이 이해
- **배경·문제의식**: dependency confusion, typosquatting, CI secret 탈취, 악성 package 업로드, 빌드 서버 변조는 정상 배포 흐름을 타고 고객에게 도달한다.
- **작동 원리**: 소스 보호, 의존성 검증, SBOM, SCA, secret scanning, build provenance, artifact signing, 배포 정책, runtime 모니터링을 pipeline에 배치한다.
- **비유**: 식품 안전이 농장, 공장, 운송, 매장까지 추적하듯 SW 공급망 보안도 개발자 PC부터 고객 배포까지 이력을 추적한다.
- **구체 예시**: npm 패키지 설치 시 lockfile과 private registry를 사용하고, 빌드 이미지는 cosign 서명 검증 후 Kubernetes admission에서 무서명 이미지를 차단한다.
- **흔한 오해·주의점**: 공급망 보안은 오픈소스 취약점 관리만이 아니다. CI 권한, 빌드 무결성, 서명 검증, 배포 정책까지 포함한다.

## 연결 개념
- SBOM/VEX - 구성요소와 취약점 영향 상태 관리
- SLSA - 빌드 출처와 무결성 보증
- DevSecOps - 개발 pipeline 보안 자동화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 공격 표면을 소스, 의존성, 빌드, artifact, 배포로 나누고 각 단계별 통제와 지표를 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 소프트웨어 공급망 보안은 SW 생산·배포 전 단계의 신뢰성과 무결성을 보장하는 통제 체계이다.
> 2. **가치**: 악성 의존성, CI 탈취, 빌드 조작, 무서명 배포를 조기에 차단해 고객 제품 오염을 막는다.
> 3. **판단 포인트**: SBOM, SCA, secret scan, SLSA provenance, code signing, admission policy를 단계별로 배치한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공급망 공격면 이해 확인 | source, dependency, build, registry, deploy | 오픈소스 CVE만 설명 |
| 통제 설계 역량 확인 | SBOM, SCA, 서명, provenance, policy gate | 도구 나열 후 단계 연결 누락 |
| 운영 지표 판단 확인 | CVE SLA, unsigned 차단, secret leak 0건 | 실제 측정 지표 부재 |

> 요약: 이 문제는 공급망 단계별 공격과 방어 통제를 연결하는 설계형 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 공급망 보안은 SW 생산 경로 보호이다. 현대 서비스는 오픈소스, CI/CD, 컨테이너 registry, 클라우드 배포가 연결되어 있다. 한 단계가 오염되면 정상 릴리스가 악성 코드 전달 경로가 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Developer -> Source Repo -> Dependency Registry
-> CI Build -> Artifact Registry -> Deployment
-> Runtime Monitoring -> Incident Response
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Control | 코드 변경 승인과 secret 차단 | branch protection, signed commit |
| Dependency Control | 외부 패키지 검증 | SCA, lockfile, private proxy |
| Build/Artifact | 빌드 무결성과 산출물 서명 | SLSA, provenance, cosign |
| Deploy Policy | 무서명·취약 artifact 차단 | admission controller, policy-as-code |

> 요약: 공급망 보안은 개발자부터 운영 배포까지 연결된 각 지점에 통제를 배치한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 커밋 -> Secret/SAST Scan -> Dependency/SCA Scan
-> Build Provenance 생성 -> Artifact 서명
-> Registry 저장 -> 배포 전 정책 검증 -> Runtime 탐지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 코드 변경 승인과 secret 검사 | secret leak 0건 |
| 2 | 의존성·라이선스·CVE 검사 | critical CVE 차단 100% |
| 3 | 빌드 provenance와 서명 생성 | artifact 서명 100% |
| 4 | 배포 정책과 런타임 탐지 | unsigned image 배포 0건 |

> 요약: 공급망 보안은 CI/CD 각 단계에서 스캔, 서명, 검증, 차단을 자동 수행한다.

---

## Ⅳ. 특징

| 구분 | 전통 보안 | 공급망 보안 | 판단 수치 |
|:---|:---|:---|:---|
| 보호 대상 | 실행 중 시스템 | 개발·빌드·배포 경로 | pipeline coverage 100% |
| 취약점 관리 | 배포 후 스캔 | 빌드 전 SCA/SBOM | critical CVE 7일 SLA |
| 무결성 | 파일 해시 일부 사용 | provenance+signature | unsigned artifact 0건 |
| 한계 | 내부 개발 중심 | 외부 공급자 의존 | 공급자 평가 연 1회 |

> 요약: 공급망 보안은 운영 환경 방어에서 SW 생산 경로의 출처와 무결성 검증으로 범위를 넓힌다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Software Supply Chain Security | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 보안팀 사후 점검 | pipeline 내 자동 gate | 배포 주 1회 이상 서비스 |
| 비용/성능 | 릴리스 직전 결함 발견 | 개발 단계 조기 차단 | 보안 피드백 15분 이하 |
| 운영/위험 | CI 토큰·패키지 오염 노출 | 서명·권한·SBOM 통제 | 핵심 서비스 100% 적용 |

> 요약: 배포 빈도와 외부 의존성이 클수록 공급망 보안 gate를 개발 pipeline에 넣어야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 악성 의존성 | typosquatting, dependency confusion | private registry, lockfile, package allowlist | 신규 패키지 승인 100% |
| CI 탈취 | secret 노출, 과도 권한 | OIDC, short-lived token, secret scan | 장기 토큰 0건 |
| Artifact 변조 | registry 권한 오남용 | cosign 서명, immutable tag | 서명 검증 실패 차단 100% |

> 요약: 핵심 리스크는 의존성, CI 권한, artifact 변조이며 registry 통제와 서명 검증으로 막는다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 보안 gate | SAST/SCA/secret scan 수행 100% | CI report |
| 무결성 검증 | provenance+signature 100% | SLSA/cosign audit |
| 대응 시간 | critical CVE 영향 분석 24시간 이하 | SBOM query, incident ticket |

> 요약: 도입 성숙도는 pipeline gate 수행률, 서명 검증률, CVE 영향 분석 시간으로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 소스 저장소에 branch protection, 2인 리뷰, secret scanning, signed commit을 적용하고 CI 권한은 OIDC short-lived token으로 제한
2. SCA와 SBOM을 build gate에 연결해 critical CVE, 금지 라이선스, 미승인 신규 패키지를 릴리스 차단 조건으로 지정
3. SLSA provenance와 cosign 서명을 생성하고 Kubernetes admission에서 unsigned image와 미승인 builder artifact 배포를 차단

**결론 (2줄):**
- 기술사 판단: 외부 패키지와 자동 배포를 사용하는 서비스는 공급망 보안을 DevSecOps pipeline의 필수 통제로 설계
- 향후 방향: SBOM, VEX, SLSA, Sigstore, policy-as-code가 결합된 증거 기반 소프트웨어 신뢰 체계로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "소프트웨어 공급망 보안을 설명하시오" | 코드부터 배포까지 단계별 흐름 | 전통 보안 대비 범위 차이 |
| 요구사항 명시형 | "공급망 공격 대응 방안을 제시하시오" | 의존성, CI, artifact 통제 절차 | 악성 패키지·토큰·변조 리스크 대응 |

> 요약: 설명형은 공격면 전체, 방안형은 pipeline gate와 배포 차단 기준 중심으로 전환한다.
