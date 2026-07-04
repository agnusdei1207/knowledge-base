---
title: "패키지 관리 - npm·pip·Maven (Package Manager)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 283
---

# 📖 【암기용】 개념 완전 이해

> 목적: 패키지 관리를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: **의존성 관리**(Dependency Management)를 통해 **소프트웨어 공급망**(Software Supply Chain)의 신뢰성을 확보하는 체계 — 외부 라이브러리의 설치·버전 해석·재현을 자동화한다.
- **왜 필요한가**: 현대 애플리케이션은 직접 선언한 것보다 훨씬 많은 **전이 의존성**을 함께 끌고 온다(예: React 앱 하나가 직접 의존성 30여 개로 node_modules에 1,000개 이상의 패키지를 설치하는 경우가 흔하다). 이 사슬 어딘가의 취약 버전·악성 코드가 그대로 내 애플리케이션에 섞여 들어온다.
- **핵심 직관**: 패키지 관리자는 "장보기 목록(manifest)"을 받아 "실제로 어느 가게에서 몇 년도 제품을 살지"까지 정확히 못 박은 "구매 영수증(lockfile)"을 만드는 조달 담당자다. 목록만 있으면 살 때마다 다른 제품이 걸릴 수 있다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 의존성 관리 | 외부 라이브러리의 선언·해석·설치·검증을 다루는 상위 체계 — 이 문서 전체의 대상 | 조달 업무 전체 |
| 소프트웨어 공급망 | 내 코드에 도달하기까지 거치는 모든 외부 패키지·저장소·빌드 경로 | 부품 하청망 |
| Manifest | 필요한 패키지 이름과 버전 "범위"를 선언한 파일(`package.json`, `requirements.txt`, `pom.xml`) | 장보기 목록("우유 1L 이상") |
| Resolver | manifest의 버전 범위를 실제 설치할 단일 버전으로 계산하는 알고리즘 | 여러 요구를 절충해 하나로 정하는 조정자 |
| Lockfile | resolver가 확정한 정확한 버전과 해시값을 고정해 재현을 보장하는 파일 | 제조사·로트번호까지 적힌 구매 영수증 |
| Registry | 패키지가 저장·배포되는 중앙 저장소(npm registry, PyPI, Maven Central) | 공용 창고 |
| Semver(유의적 버전) | MAJOR.MINOR.PATCH 형식과 `^`·`~` 범위 연산자로 호환 가능 범위를 표현하는 규칙 | 버전 번호에 붙인 신호등 |
| 전이 의존성(Transitive Dependency) | 내가 설치한 패키지가 또 의존하는 패키지 — 직접 선언하지 않아도 딸려 온다 | 친구의 친구까지 초대받는 것 |
| Dependency Confusion | 사설(내부) 패키지와 이름이 같은 악성 공개 패키지를 resolver가 더 높은 버전이라고 착각해 잘못 설치하게 만드는 공격 | 같은 이름의 가짜 택배기사가 먼저 문을 두드리는 것 |
| Typosquatting | 유명 패키지 이름의 오타(`reqeusts` 등)로 악성 패키지를 등록해 잘못 설치를 유도하는 공격 | 진짜 간판과 비슷한 가짜 간판 |
| SBOM | 소프트웨어에 포함된 모든 구성요소·버전 목록 | 식품 성분표 |

## 깊이 이해

### 왜 lockfile 없이는 "같은 코드"도 다르게 빌드되는가
- manifest에 `"lodash": "^4.17.0"`이라고만 적으면, `^`는 "4.x.x 범위 내 최신"을 뜻한다. 오늘 설치하면 4.17.21이 깔리지만, 6개월 후 새 팀원이 같은 manifest로 설치하면 그사이 배포된 4.17.30이 깔릴 수 있다 — 코드는 그대로인데 실제 실행되는 라이브러리가 달라진다.
- lockfile(`package-lock.json`, `poetry.lock`, effective POM)은 이 계산 결과를 "4.17.21, sha512 해시 abc..."처럼 정확히 박제한다. 그래서 lockfile이 있으면 1년 후에도 정확히 같은 바이너리가 설치된다 — 이것이 "재현 가능한 빌드(reproducible build)"다.

### resolver가 버전 충돌을 푸는 방식 — 언어마다 다르다
- **npm**: 패키지 A가 `lodash@^3.0.0`을, 패키지 B가 `lodash@^4.0.0`을 요구하면 두 메이저 버전이 호환되지 않으므로, npm은 최상위에 하나(예: 4.x)를 두고 나머지는 A의 `node_modules` 하위에 중첩 설치한다. 그 결과 하나의 프로젝트에 같은 라이브러리 서로 다른 버전이 동시에 존재할 수 있다.
- **Maven**: "nearest wins(최근접 우선)" 방식이다. 루트 pom이 모듈 A(commons-lang 2.4에 의존)와 모듈 B(commons-lang 2.6에 의존)를 함께 참조하면, 의존성 트리에서 루트로부터 더 가까운(depth가 낮은) 선언이 이긴다. 깊이가 같으면 pom.xml에 먼저 선언된 쪽이 이긴다. `dependencyManagement`와 BOM(Bill of Materials)은 이 판단을 프로젝트 전체에서 한 번에 고정하는 장치다.

### 실제 사고 사례로 보는 위험 3가지
- **가용성 붕괴 — left-pad 사태(2016)**: 단 11줄짜리 `left-pad` 패키지가 npm에서 삭제되자, 이를 전이 의존성으로 물고 있던 Babel·React 등 수천 개 프로젝트의 빌드가 동시에 실패했다. "작은 패키지 하나"가 전체 공급망의 단일 장애점이 될 수 있음을 보여준 사건이다.
- **악성 코드 주입 — event-stream 사건(2018)**: 인기 npm 패키지 `event-stream`의 유지관리 권한이 공격자에게 넘어가고, 공격자가 심은 전이 의존성(`flatmap-stream`)에 비트코인 지갑을 노리는 악성 코드가 숨겨져 수백만 다운로드에 유포됐다. 직접 의존성만 감사해서는 못 막는 이유다.
- **Dependency Confusion — 2021년 실증 연구**: 보안 연구자 Alex Birsan은 PayPal·Apple·Microsoft 등 내부에서만 쓰는 사설 패키지명을 그대로 공개 레지스트리(npm, PyPI)에 "더 높은 버전 번호"로 등록했다. 다수 기업의 빌드 시스템이 "버전이 더 높은 쪽"을 자동으로 선택하는 resolver 규칙 때문에 사설 패키지 대신 공격자 패키지를 설치해, 35개 이상 기업 침투에 성공했다.

### 취약 버전 유입을 막는 실제 도구
- npm은 `npm audit`, pip은 `pip-audit`/Safety, Maven은 OWASP Dependency-Check로 설치될 패키지 트리를 CVE DB와 대조한다. 예를 들어 Log4j의 취약 버전(2.0~2.14, Log4Shell CVE-2021-44228)이 전이 의존성으로 들어오면, 이 스캐너들이 pom.xml의 `dependencyManagement`로 강제 상향(예: 2.17.1 이상)해야 한다고 표시한다.
- hash pinning(`pip install --require-hashes`)은 버전 번호가 같아도 내용이 바뀌었으면(패키지 탈취·재배포) 설치를 거부한다 — 버전 문자열만으로는 위변조를 못 잡기 때문이다.

## 연결 개념
- 빌드 자동화 - 의존성 해석을 포함한 산출물 생성
- SBOM - 패키지 목록과 버전 가시화
- 소프트웨어 공급망 보안 - 악성 패키지와 취약 의존성 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: npm·pip·Maven 명령어 나열이 아니라 의존성 해석, 버전 고정, 공급망 위험 통제 관점으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 패키지 관리는 라이브러리 의존성 선언, 버전 해석, 설치, 배포, 취약점 점검을 자동화하는 체계이다.
> 2. **가치**: 동일 빌드 재현, 취약 의존성 탐지, 라이선스 준수, 내부 저장소 통제로 공급망 위험을 낮춘다.
> 3. **판단 포인트**: manifest와 lockfile, 공개 저장소와 사설 저장소, 직접 의존성과 전이 의존성을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 패키지 관리 구조 이해 확인 | manifest, resolver, lockfile, registry | 설치 명령어만 나열 |
| 언어별 도구 비교 판단 확인 | npm, pip, Maven의 버전 해석 차이 | JavaScript·Python·Java 생태계 차이 누락 |
| 공급망 보안 인식 확인 | 취약점 스캔, hash pinning, 내부 저장소 | 최신 버전 업데이트만 해결책으로 제시 |

> 요약: 패키지 관리 답안은 의존성 재현성과 공급망 위험 통제를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 패키지 관리는 의존성을 선언·해석·검증하는 체계이다.
- 배경: 애플리케이션은 공개 라이브러리와 전이 의존성에 의존하므로 버전 충돌, 취약점, 라이선스 문제가 빌드와 운영 위험이 된다.
- 필요성: npm·pip·Maven의 lockfile, checksum, registry 정책으로 동일 산출물과 정책 준수를 보장해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Manifest -> Resolver -> Registry Download -> Lock/Tree -> Build/Test -> Vulnerability Scan
                +-> Private Mirror
                +-> License Policy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Manifest | 의존성 이름과 버전 범위 선언 | package.json, requirements.txt, pom.xml |
| Resolver | 직접·전이 의존성 버전 결정 | semver, Maven nearest-wins |
| Registry | 패키지 저장·배포 | npm registry, PyPI, Maven Central |
| Lock/Tree | 실제 설치 버전 고정 | package-lock, pip hash, effective POM |
| Scanner | 취약점·라이선스 점검 | npm audit, pip-audit, OWASP Dependency-Check |

> 요약: 패키지 관리는 선언 파일에서 실제 설치 버전까지 이어지는 의존성 결정 과정을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
의존성 선언 -> 버전 범위 해석 -> 전이 의존성 계산 -> 패키지 다운로드 -> 검증/설치 -> 빌드 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | manifest에서 의존성 식별 | 직접 의존성 목록 100% 파악 |
| 2 | resolver가 버전 제약 계산 | 충돌 의존성 0건 |
| 3 | registry에서 패키지 다운로드 | checksum, signature, hash 검증 |
| 4 | lockfile 또는 dependency tree 고정 | 재빌드 동일 버전 100% |
| 5 | 취약점·라이선스 검사 | critical CVE 0건, 금지 라이선스 0건 |

> 요약: 패키지 관리 흐름은 버전 해석 후 실제 설치 버전을 고정하고 스캔으로 운영 반입 여부를 결정한다.

---

## Ⅳ. 특징

| 구분 | npm | pip | Maven |
|:---|:---|:---|:---|
| 주요 파일 | package.json, package-lock.json | requirements.txt, pyproject.toml | pom.xml, settings.xml |
| 버전 방식 | semver 범위와 lockfile | pinning, hash 옵션 | dependencyManagement, BOM |
| 전이 의존성 | node_modules tree | wheel/sdist 설치 | nearest definition, scope |
| 보안 점검 | npm audit | pip-audit, Safety | OWASP Dependency-Check |

> 요약: npm은 lockfile, pip은 pinning과 hash, Maven은 BOM과 dependencyManagement로 재현성을 확보한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 jar 복사 | registry 기반 의존성 해석 | 전이 의존성 수 50개 이상 |
| 비용/성능 | 공개 저장소 직접 접근 | 사설 mirror와 cache | CI 다운로드 시간 5분 초과 |
| 운영/위험 | 버전 범위만 선언 | lockfile, BOM, hash pinning | 공급망 감사와 재현 빌드 요구 |

> 요약: 의존성 규모와 감사 요구가 커질수록 사설 저장소, lockfile, 스캔 게이트가 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Dependency Confusion | 내부 패키지명과 공개 패키지명 충돌 | private registry 우선, namespace 예약 | 외부 우선 resolve 0건 |
| Typosquatting | 유사 이름 악성 패키지 | allowlist, package signing | 신규 패키지 승인률 100% |
| 취약 버전 유입 | 전이 의존성 관리 부재 | SBOM, CVE 스캔, BOM 고정 | critical CVE 0건 |

> 요약: 패키지 관리의 핵심 위험은 이름 혼동, 악성 패키지, 취약 전이 의존성이며 정책 게이트로 차단한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 재현성 | 동일 commit 동일 dependency 100% | lockfile diff, build scan |
| 취약점 | critical/high CVE 0건 | SCA 도구, CVE DB |
| 라이선스 | 금지 라이선스 0건 | license scanner, SBOM 검토 |

> 요약: 패키지 관리는 재현성, 취약점, 라이선스 세 지표를 CI에서 자동 검증해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. npm은 `npm ci`와 `package-lock.json`을 사용해 CI 설치 버전을 고정하고 `npm audit --audit-level=high`를 게이트로 둠
2. pip은 `pip-tools` 또는 Poetry로 lockfile을 생성하고 `--require-hashes`로 위변조 패키지 설치를 차단함
3. Maven은 BOM, 사설 Nexus, OWASP Dependency-Check를 적용해 전이 의존성과 CVE를 릴리스 전 검증함

**결론 (2줄):**
- 기술사 판단: 공개 패키지 사용 비율이 높을수록 lockfile, 사설 저장소, SCA 게이트를 기본 통제로 채택함
- 향후 방향: 패키지 관리는 SBOM, Sigstore, SLSA provenance와 결합해 공급망 감사 체계로 확장됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "패키지 관리를 설명하시오" | 의존성 선언·해석·설치 흐름 | npm·pip·Maven별 특징 |
| 요구사항 명시형 | "공급망 보안 방안을 제시하시오", "도구를 비교하시오" | lockfile, hash, registry 정책 | 취약점·라이선스·dependency confusion 대응 |

> 요약: 설명형은 의존성 흐름, 보안형은 공급망 공격면과 정책 게이트를 중심으로 답안을 전개한다.
