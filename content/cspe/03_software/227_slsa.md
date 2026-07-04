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
- **개요**: SLSA(Supply-chain Levels for Software Artifacts, "살사"라고 읽음)는 소프트웨어 **공급망 보안**을 위해 소스 관리부터 빌드까지의 **출처(provenance)**와 무결성을 단계적 레벨로 보증하는 프레임워크다.
- **왜 필요한가**: 2020년 SolarWinds 공격(SUNBURST)에서 공격자는 소스코드 자체가 아니라 빌드 서버에 침투해 정상 빌드 과정 중간에 악성 코드를 주입했다 — 최종 바이너리에 서명까지 정상적으로 찍혀 나갔기 때문에 약 18,000곳의 고객이 오염된 업데이트를 그대로 설치했다. 소스코드 검사나 최종 바이너리 스캔만으로는 "빌드 과정 자체가 조작됐는지"를 알 수 없다.
- **핵심 직관**: SLSA는 "이 결과물이 정말 신뢰할 수 있는 소스·빌더에서, 조작 없이 만들어졌는가"를 증명 가능하게(non-falsifiable) 만드는 체계다 — 최종 결과물만 믿지 말고 만들어진 과정을 추적하라는 것.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| SLSA | 소스~빌드 무결성을 레벨로 나눈 공급망 보안 프레임워크 자체 | 식품·의약품 GMP(우수제조관리기준) 인증 등급 |
| Provenance (출처 증명) | 어떤 소스·빌더·명령으로 이 산출물이 만들어졌는지 기록한 메타데이터 | 제품의 제조 이력서 |
| Attestation (증명서) | provenance 등을 서명해 위변조를 막은 서명된 진술서 | 공증받은 이력서 |
| in-toto | attestation을 표현하는 표준 포맷(SLSA provenance가 이 형식을 씀) | 이력서 표준 양식 |
| Builder (빌더) | 소스를 받아 실제로 빌드를 수행하는 서비스 | 위탁 제조 공장 |
| Hermetic Build (밀폐 빌드) | 빌드 중 외부 네트워크·임의 입력을 차단해 선언된 재료만 사용하도록 격리한 빌드 | 외부 반입이 금지된 무균 제조실 |
| Ephemeral/Isolated Builder | 매 빌드마다 새로 생성되고 끝나면 폐기되는 격리된 실행 환경 | 1회용 멸균 작업대 |
| Sigstore/cosign | 산출물과 provenance에 서명·검증하는 오픈소스 도구 | 제품에 찍는 위조 방지 홀로그램 |
| Dependency Confusion (의존성 혼동 공격) | 내부 패키지명과 같은 이름의 악성 패키지를 공개 저장소에 올려 잘못 설치되게 하는 공격 | 가짜 택배가 진짜 주소로 배달되게 하는 사기 |

## 깊이 이해

### SLSA가 막으려는 공격 지점 — SolarWinds 사례로 이해
- 공격자가 노리는 지점은 셋이다: ① 소스코드 저장소 자체를 변조 ② CI·빌드 서버에 침투해 빌드 "중간" 산출물을 조작 ③ 배포 채널·패키지 저장소를 변조. SolarWinds는 ②에 해당한다 — 소스코드 리뷰 기록은 정상이었지만 실제 컴파일 단계에서 악성 코드가 삽입됐다. 이 때문에 SLSA는 "소스 보호"뿐 아니라 "빌드 자체의 신뢰성"을 별도 레벨로 다룬다.

### SLSA 레벨이 실제로 요구하는 것 (Build Track 기준)
- Level 1: provenance(출처 기록)가 존재하기만 하면 된다. 자동 생성이든 수동 작성이든 최소한의 이력은 남긴다는 뜻이며, 위변조 방지는 아직 보장하지 않는다.
- Level 2: 호스팅된 빌드 서비스(예: GitHub Actions, GitLab CI)가 서명된 provenance를 자동 생성한다. 빌드 로그가 아니라 서명된 증명이라는 점에서 신뢰도가 올라간다.
- Level 3: 빌드 환경이 격리·일회성(ephemeral)이며, provenance가 위조 불가능(non-falsifiable)함을 강한 격리로 보장한다 — 예: 빌드 담당자조차 실행 중인 빌드 프로세스에 개입해 provenance 값을 조작할 수 없도록 시스템 수준에서 차단한다.
- 숫자로 감을 잡으면, Level 1→2는 "기록을 남기느냐"의 문제이고, Level 2→3은 "그 기록을 사람이 손댈 수 있느냐 없느냐"의 문제다 — 격리 강도가 핵심 축이다.

### provenance 검증이 배포를 막는 실제 흐름
- 코드 리뷰(2인 승인) → 격리된 빌더에서 hermetic build 실행 → artifact의 digest(해시값)와 소스 커밋, 빌더 신원을 담은 provenance 생성 → cosign으로 서명 → 배포 직전 admission controller(예: Kubernetes에서 이미지 배포를 막는 검증 단계)가 서명과 builder identity, provenance의 predicate를 검사해 조건 미충족 시 배포 자체를 차단한다.
- 예: 어떤 이미지가 서명은 있지만 provenance의 builder identity가 승인된 CI가 아니라면(예: 개인 노트북에서 수동 빌드), 서명이 없는 것과 동일하게 차단된다 — "서명 유무"가 아니라 "누가 어떻게 만들었는지"까지 검증하는 것이 SLSA의 핵심이다.

### 비유와 흔한 오해
- **비유**: 의약품이 원료 산지, 제조 공장, 품질 검사, 유통 이력을 추적할 수 있어야 시중에 유통되듯, SLSA는 소스, 빌더, 산출물, 서명 이력을 추적 가능하게 만든다.
- **오해 1**: SLSA는 취약점 스캐너가 아니다 — 코드에 CVE가 있는지는 SBOM·SCA의 역할이고, SLSA는 "이 산출물이 조작 없이 만들어졌는가"만 다룬다. 취약점이 없는 코드도 빌드 과정에서 조작되면 SLSA가 이를 문제 삼는다.
- **오해 2**: 서명만 있으면 안전하다고 착각하기 쉽다 — 개인 키로 아무 빌드에나 서명할 수 있다면 서명 자체가 무의미하다. SLSA는 "누가 서명했는가"(빌더 신원)와 "어떤 과정으로 만들었는가"(provenance)까지 함께 검증해야 의미가 있다고 본다.

## 연결 개념
- SBOM — 산출물에 포함된 구성요소 목록(SLSA는 그 산출물이 조작 없이 만들어졌음을 보증)
- in-toto — SLSA provenance가 사용하는 attestation 표준 포맷
- Sigstore/cosign — provenance와 산출물에 서명·검증을 실제로 수행하는 도구

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

- 개요: SW 공급망 무결성 프레임워크
- 배경: 공격자는 코드 저장소, CI, 빌드 서버, 패키지 저장소를 조작해 정상 릴리스처럼 배포한다.
- 필요성: provenance, 서명, 빌드 격리로 artifact 출처와 변조 여부를 검증해야 한다.

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

| 구분 | 기존/대안 | SLSA | 선택 기준 |
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
