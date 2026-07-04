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
- **개요**: **소프트웨어 공급망 보안**(Software Supply Chain Security)은 소스코드·오픈소스 의존성·빌드·패키지·배포·운영까지 SW가 만들어져 고객에게 전달되는 전체 경로의 **무결성(Integrity)**과 **출처(Provenance)**를 보증하는 보안 체계다. **DevSecOps**의 한 축으로, 실행 중인 시스템을 지키는 전통 보안과 달리 "코드가 태어나서 배포되기까지의 경로" 자체를 보호 대상으로 삼는다.
- **왜 필요한가**: 공격자는 더 이상 방어가 두꺼운 기업 내부 코드를 직접 뚫지 않는다. 상대적으로 허술한 오픈소스 패키지·CI 토큰·빌드 서버·업데이트 채널을 노리면, "신뢰된 정상 배포 경로"를 그대로 타고 고객사까지 자동 전파되기 때문이다.
- **핵심 직관**: 완성된 코드만 검사하던 시대에서, "그 코드가 어디서 와서 어떻게 만들어졌는가"까지 증명해야 하는 시대로 바뀐 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 표기/용어 | 의미 | 비유 |
|:---|:---|:---|
| 공급망(Supply Chain) | SW가 개발자 PC→저장소→의존성→빌드→아티팩트→배포→운영까지 이동하는 전체 경로 — 이 개념이 보호하려는 **대상** | 식자재가 농장에서 식탁까지 오는 유통 경로 |
| SBOM (Software Bill of Materials) | 제품에 포함된 모든 구성요소(오픈소스 라이브러리·버전·라이선스)의 목록 | 가공식품의 원재료명 표시 |
| SCA (Software Composition Analysis) | SBOM에 담긴 오픈소스 의존성을 스캔해 알려진 취약점(CVE)·라이선스 위반을 찾는 분석 | 원재료 성분을 검사해 유해물질 여부 확인 |
| VEX (Vulnerability Exploitability eXchange) | SBOM에 있는 CVE가 "이 제품에서 실제로 악용 가능한지"를 표시하는 문서 — CVE 존재 ≠ 실제 위험이라 별도 판단이 필요 | 알레르기 성분이 들어있어도 "이 조리법에선 미량이라 안전"이라는 표기 |
| Dependency Confusion | 사내 전용 패키지명과 동일한 이름으로, 더 높은 버전 번호를 붙인 악성 패키지를 공개 레지스트리에 등록해 빌드 시스템이 사내용 대신 그 악성 패키지를 설치하게 만드는 공격 | 사내 전용 상품과 이름이 같은 가짜 상품을 공용 매대에 더 신상품처럼 올려 착오 구매 유도 |
| Typosquatting | `lodash`를 `1odash`처럼 철자를 살짝 바꾼 악성 패키지를 등록해 오타로 설치를 유도하는 공격 | 유명 브랜드와 이름이 비슷한 짝퉁 상표 |
| Secret Scanning | 코드·로그·설정파일에 실수로 노출된 API 키·비밀번호·토큰을 자동 탐지 | 편지 봉투에 비밀번호가 그대로 적혀 나가는지 검수 |
| SLSA (Supply-chain Levels for Software Artifacts) | 빌드 파이프라인의 무결성 성숙도를 단계(v1.0 기준 Build Level 1~3)로 정의한 프레임워크 — 레벨이 높을수록 빌드 출처 위조가 어려움 | 식품 HACCP 인증 등급처럼 "이 공정이 얼마나 신뢰할 수 있는가"의 등급표 |
| Provenance (빌드 출처 증명) | "이 아티팩트가 어떤 소스코드·빌더·환경에서, 언제 만들어졌는가"를 암호학적으로 증명하는 메타데이터 | 원산지 증명서 |
| Code Signing / cosign | 빌드 결과물(컨테이너 이미지 등)에 개인키로 서명해 이후 위변조 여부를 검증 가능하게 만드는 것 — Sigstore 프로젝트의 대표 서명 도구가 cosign | 봉인씰 — 뜯겨 있으면 위조로 간주 |
| Sigstore | cosign(서명)·Rekor(투명성 로그)·Fulcio(단기 인증서 발급)로 구성된 오픈소스 서명 인프라 | 공증 시스템 전체(서명+공개 등기부+신원확인) |
| Admission Controller | Kubernetes가 파드를 배포하기 직전에 정책 위반 여부를 검사해 반려하는 게이트 | 공항 보안검색대 — 통과 기준 미달 시 탑승 자체를 막음 |
| Policy-as-Code | "서명 없는 이미지 배포 금지" 같은 배포 정책을 코드로 정의해 자동 검증하는 방식(OPA/Gatekeeper 등) | 법조문을 자동 심사 로봇에게 넘겨 사람 재량 없이 일괄 적용 |

## 깊이 이해

### 왜 지금 공급망 보안이 부각됐나 (배경)
- SolarWinds Orion 사건(2020)이 대표적이다. 공격자가 SolarWinds의 **빌드 시스템**에 침투해 정상 서명된 업데이트 파일 안에 악성 코드(SUNBURST)를 심었고, 이 업데이트가 정상 배포 채널을 타고 약 1만8천 개 고객사에 자동 전파됐다. 각 고객사 입장에선 "신뢰하는 벤더의 정상 서명된 업데이트"를 설치했을 뿐인데 뚫린 것이다.
- Log4Shell(CVE-2021-44228, CVSS 10.0, 2021)도 마찬가지다. 전 세계 수많은 서비스가 간접 의존성(자신이 직접 쓴 적 없는, 의존성의 의존성)으로 Log4j를 물고 있었고, SBOM이 없던 조직은 "우리가 이 취약점에 영향받는지"조차 파악하는 데 수 주가 걸렸다. 이 두 사건 이후 SBOM 요구 확산(미국 행정명령 14028 등)과 SLSA 표준화가 본격화됐다.

### 공급망 5단계와 단계별 공격·방어 — 수치로 이해
- 공급망은 ① Source(소스) → ② Dependency(의존성) → ③ Build(빌드) → ④ Artifact/Registry(산출물) → ⑤ Deploy/Runtime(배포·운영) 5단계로 쪼개 이해하면 명확하다.
- ① Source: 공격자가 커밋 권한을 훔치거나 악성 PR을 병합시키는 단계 → 방어는 2인 리뷰(branch protection)와 signed commit.
- ② Dependency: dependency confusion·typosquatting으로 악성 패키지를 주입 → 방어는 SCA + lockfile(버전 고정) + private registry(사내 패키지는 공개 레지스트리에 동일 이름이 없게 네임스페이스 분리).
- ③ Build: CI 서버 자체를 변조하거나 CI 토큰을 훔쳐 빌드 산출물에 코드를 주입(SolarWinds 패턴) → 방어는 SLSA provenance 생성 + OIDC 기반 short-lived 토큰(CI가 장기 비밀키를 들고 있지 않게).
- ④ Artifact: 이미 만들어진 이미지를 레지스트리에서 몰래 바꿔치기 → 방어는 cosign 서명 + immutable tag(태그 재사용 금지).
- ⑤ Deploy/Runtime: 서명 검증 없이 아무 이미지나 배포되는 경우 → 방어는 admission controller가 무서명 이미지를 강제로 반려.

### SBOM과 SCA는 다르다 — 혼동 주의
- SBOM은 **목록**(무엇이 들어있는가)이고, SCA는 그 목록을 **스캔해 판정**(그중 무엇이 위험한가)하는 활동이다. SBOM 없이 SCA는 불가능하고, SCA 없이 SBOM은 그냥 재고 목록에 불과하다.
- 예: 한 웹 서비스의 SBOM에 350개 오픈소스 컴포넌트가 있고, SCA 스캔 결과 그중 12개에 알려진 CVE가 있으며, VEX 검토 결과 실제로 이 서비스의 사용 방식상 악용 가능한 것은 3개뿐이라고 판정할 수 있다 — 이 3개만 우선 패치하면 된다.

### SLSA 레벨 — 판별 기준
- Level 1: 빌드 과정이 스크립트화되고 provenance가 존재(단, 위조 방지는 안 됨). Level 2: 신뢰된 빌드 서비스(호스티드 CI)가 provenance에 서명. Level 3: 빌드 환경이 격리돼 있어 빌드 도중 소스나 파라미터를 조작해도 provenance가 이를 탐지.
- 판별 원리: "이 provenance를 누가 위조할 수 있는가"로 레벨을 가른다 — 레벨이 낮을수록 개발자 본인도 provenance를 조작할 수 있고, 레벨이 높을수록 빌드 인프라 자체가 격리돼 아무도 조작 못 한다.

### 비유와 흔한 오해
- **비유**: 식품 이력추적제가 농장(소스)→가공공장(빌드)→물류(레지스트리)→매장(배포)까지 이력을 남기듯, 공급망 보안은 개발자 커밋부터 고객 배포까지의 이력을 전 구간 추적한다.
- **오해 1**: 공급망 보안 = 오픈소스 취약점 관리(SCA)라고 오해하기 쉽지만, CI 권한·빌드 무결성·서명 검증·배포 정책까지 포함하는 더 넓은 개념이다.
- **오해 2**: SBOM만 만들면 끝이라고 생각하기 쉽지만, SBOM은 "재고 목록"일 뿐 VEX로 실제 악용 가능성을 판정하고 SCA로 지속 모니터링해야 의미가 있다.

## 연결 개념
- SBOM/VEX (구성요소 목록과 실제 위험 여부 판정 — 위 표에서 다룬 세부 개념)
- SLSA (빌드 무결성 등급 프레임워크 — 위에서 다룬 세부 개념)
- DevSecOps (개발 파이프라인 전체 보안 자동화 — 공급망 보안이 속한 상위 실천 체계)

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

- 개요: SW 생산 경로 보호 체계
- 배경: 현대 서비스는 오픈소스, CI/CD, 컨테이너 registry, 클라우드 배포가 연결되어 있다.
- 필요성: 한 단계 오염이 정상 릴리스를 악성 코드 전달 경로로 바꾸지 않도록 통제해야 한다.

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

| 구분 | 기존/대안 | Software Supply Chain Security | 선택 기준 |
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
