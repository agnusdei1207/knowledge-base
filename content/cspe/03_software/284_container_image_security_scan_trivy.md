---
title: "컨테이너 이미지 보안 스캔 - Trivy (Container Image Security Scan)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 284
---

# 📖 【암기용】 개념 완전 이해

> 목적: 컨테이너 이미지 보안 스캔을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: **컨테이너 이미지 취약점 스캔**은 **SCA(Software Composition Analysis, 소프트웨어 구성요소 분석)**의 한 형태로, 이미지 안에 포장된 OS 패키지·언어 라이브러리·설정을 알려진 취약점 DB와 대조하는 절차다.
- **왜 필요한가**: 컨테이너 이미지는 베이스 OS, 미들웨어, 애플리케이션 의존성을 한 덩어리로 굳혀 배포한다. 이 덩어리 안의 취약 버전 하나가 그 이미지를 쓰는 모든 클러스터·파드에 그대로 복제된다.
- **핵심 직관**: 이미지 스캔은 택배가 창고를 나가기 전 여는 "출고 전 X-ray 검사"다. 상자를 열어 내용물 목록(SBOM)을 뽑고, 그 목록을 리콜 제품 리스트(CVE DB)와 대조해 리콜 대상이 있으면 출고를 막는다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 컨테이너 이미지 취약점 스캔 | 이미지 구성요소를 취약점 DB와 대조하는 SCA 활동 전체 | 출고 전 X-ray 검사 |
| 이미지 레이어 | Dockerfile 한 명령(RUN, COPY 등)이 만드는 파일시스템 diff 단위. 이미지는 이 레이어들을 겹쳐 쌓은 것 | 라자냐의 층 |
| CVE(Common Vulnerabilities and Exposures) | 공개적으로 식별번호가 부여된 알려진 취약점(예: CVE-2021-44228) | 리콜 제품 고유 번호 |
| CVSS(Common Vulnerability Scoring System) | 취약점 심각도를 0.0~10.0 점수로 매기는 국제 표준 | 태풍 등급(1~5호) |
| Severity 등급 | CVSS 점수를 LOW(0.1~3.9)·MEDIUM(4.0~6.9)·HIGH(7.0~8.9)·CRITICAL(9.0~10.0)로 구간화한 것 | 태풍 등급을 위험 단계로 라벨링 |
| SBOM | 이미지에 포함된 모든 패키지·버전의 목록 | 제품 성분표 |
| VEX(Vulnerability Exploitability eXchange) | 특정 CVE가 이 제품에서는 실제로 악용 불가능하다고 공급자가 밝히는 문서 | "이 로트는 리콜 대상 아님" 안내문 |
| Base Image | 애플리케이션이 얹히는 최하단 OS 계층 이미지(예: alpine, ubuntu) | 건물의 기초 |
| exit-code | 스캔 결과에 따라 스캐너 프로세스가 반환하는 종료 코드 — CI가 이 값을 보고 빌드 성공/실패를 결정 | 검사관의 합격/불합격 도장 |

## 깊이 이해

### 레이어를 어떻게 "열어서" 분석하는가
- 이미지는 union filesystem으로 레이어를 순서대로 겹쳐 최종 파일시스템을 구성한다. Trivy는 이 레이어들을 하나씩 풀어(extract) 각 레이어의 OS 패키지 관리자 메타데이터(`dpkg`의 `/var/lib/dpkg/status`, `rpm` DB, `apk`의 `installed` 파일)를 읽어 "이 이미지에 어떤 패키지의 어떤 버전이 실제로 존재하는가" 목록(=SBOM)을 만든다.
- 언어별 의존성(Node의 `package-lock.json`, Python의 site-packages, Java의 jar 내 `pom.properties`)도 같은 방식으로 레이어 안에서 읽어낸다. 즉 스캔 대상은 OS 패키지 하나만이 아니라 이미지 안에 실존하는 모든 소프트웨어 구성요소다.

### CVE DB와 매칭해 severity를 매기는 과정 — 수치로 확인
- 추출한 "패키지명@버전" 목록을 NVD(National Vulnerability Database)나 배포판별 보안 트래커(Debian Security Tracker 등)와 대조한다. 예를 들어 이미지 안에 `log4j-core:2.14.1`이 있으면, 이 버전이 CVE-2021-44228(Log4Shell)의 영향 범위(2.0-beta9 ~ 2.14.1)에 포함되므로 매칭되고, 이 CVE의 CVSS는 10.0(최고 등급)이므로 CRITICAL로 분류된다.
- 실행 예: `trivy image --severity HIGH,CRITICAL --exit-code 1 app:1.2.3`을 CI에서 돌리면, 스캐너가 이미지 전체 레이어를 분석해 "CRITICAL 3건, HIGH 12건" 같은 표를 출력하고, 하나라도 있으면 exit-code 1을 반환해 파이프라인을 실패시킨다. `fixed version` 컬럼에는 "2.17.1로 올리면 해결"처럼 패치 버전이 함께 표시된다.

### "스캔 통과 = 안전"이 아닌 이유
- CVE DB는 실시간이 아니다. 새 취약점이 공개된 후 NVD·배포판 트래커에 등재되기까지 며칠의 시차가 있고, 그 사이 스캔은 CRITICAL 0건으로 통과하지만 실제로는 아직 미등재 취약점이 남아있을 수 있다. 그래서 registry에 저장된 이미지도 DB 갱신 후 24시간 내 재스캔하는 운영이 필요하다.
- False Positive도 흔하다. 예를 들어 이미지 안에 취약한 함수가 포함된 라이브러리가 있어도, 애플리케이션 코드가 그 함수를 실제로 호출하지 않으면 익스플로잇이 불가능하다. 이런 경우를 매번 사람이 재확인하는 대신, VEX 문서로 "not_affected"라고 표시해 반복 리뷰 부담을 줄인다.
- 스캐너는 취약한 "패키지 버전"만 볼 뿐, 이미지가 root로 실행되는지·불필요한 권한이 있는지 같은 misconfiguration은 별도 규칙(Trivy의 config scan)으로 봐야 한다. 그래서 CVE 스캔 하나로 끝내지 않고 SBOM·서명·admission control과 겹겹이 결합한다.

## 연결 개념
- SBOM - 이미지 구성요소 목록
- CI/CD 보안 게이트 - 빌드 후 배포 전 차단
- Kubernetes Admission Control - 취약 이미지 반입 정책

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Trivy 명령어 소개가 아니라 이미지 레이어, CVE 매핑, CI/CD 차단 기준, 운영 보완 통제까지 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컨테이너 이미지 보안 스캔은 이미지 레이어와 의존성을 분석해 CVE, secret, misconfiguration을 탐지하는 통제이다.
> 2. **가치**: 취약 이미지의 registry push와 Kubernetes 배포를 사전에 차단해 운영 침해 가능성을 낮춘다.
> 3. **판단 포인트**: build-time 스캔, registry 스캔, admission 스캔, runtime 탐지를 계층화해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 이미지 보안 위험 이해 확인 | OS 패키지, 앱 의존성, secret, misconfig | 컨테이너 격리만 설명하고 이미지 공급망 누락 |
| Trivy 적용 구조 판단 확인 | 레이어 분석, CVE DB, severity, exit-code | 스캔 보고서만 만들고 배포 차단 기준 누락 |
| DevSecOps 통합 역량 확인 | CI gate, registry policy, admission control | 런타임 탐지와 구분하지 않음 |

> 요약: 이미지 스캔 답안은 탐지 대상, 차단 위치, 예외 처리, 재스캔 주기를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 이미지 스캔은 컨테이너 취약점을 배포 전 찾는 절차이다.
- 배경: 컨테이너 이미지는 OS 패키지와 애플리케이션 의존성을 레이어로 포함하므로 취약점이 복제 배포된다.
- 필요성: Trivy 같은 도구로 critical CVE 0건 기준을 CI/CD에 넣어 취약 이미지 반입을 통제해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Container Image -> Layer Extract -> Package Detect -> CVE DB Match -> Policy Gate -> Registry/Deploy
                         +-> Secret Scan
                         +-> Misconfiguration Scan
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 이미지 레이어 | 베이스 OS와 앱 파일 포함 | Dockerfile, OCI image |
| 취약점 DB | CVE와 fixed version 제공 | NVD, distro advisory |
| Trivy Scanner | OS·언어 패키지·secret·IaC 검사 | image, fs, repo, config scan |
| 정책 게이트 | severity 기준으로 빌드 실패 처리 | HIGH/CRITICAL exit-code 1 |
| Registry/Admission | 저장·배포 전 반입 통제 | Harbor, Kyverno, OPA Gatekeeper |

> 요약: 이미지 스캔은 레이어 분석 결과를 CVE DB와 대조하고 정책 게이트로 배포 여부를 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
이미지 생성 -> Trivy 스캔 -> CVE/Secret/Misconfig 판정 -> 정책 평가 -> Push 허용/차단 -> 재스캔
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Dockerfile 빌드 후 이미지 생성 | tag, digest 생성 |
| 2 | Trivy가 레이어와 package metadata 분석 | OS·라이브러리 식별률 100% |
| 3 | CVE DB와 severity 매핑 | HIGH/CRITICAL 목록 산출 |
| 4 | 정책 기준으로 CI 성공·실패 결정 | critical 0건, high 예외 승인 |
| 5 | registry 저장 후 주기 재스캔 | DB 갱신 후 24시간 내 재평가 |

> 요약: 이미지 스캔은 빌드 시점뿐 아니라 CVE DB 갱신 후 재스캔까지 포함해야 한다.

---

## Ⅳ. 특징

| 구분 | 기존 이미지 배포 | Trivy 기반 스캔 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 취약점 확인 | 운영 반영 후 수동 점검 | CI에서 CVE 매핑 | CVSS 7.0 이상 차단 |
| 대상 범위 | OS 패키지 중심 | OS, npm, pip, Maven, secret, IaC | multi-language scan |
| 배포 통제 | registry push 허용 후 대응 | exit-code로 push 차단 | critical CVE 0건 |
| 한계 | CVE DB 의존 | false positive와 예외 관리 필요 | VEX로 영향 없음 표시 |

> 요약: Trivy는 이미지 취약점을 배포 전 차단하지만 CVE 영향 판단과 예외 승인은 별도 프로세스가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 보안 점검 | CI/registry 자동 스캔 | 이미지 배포 빈도 일 1회 이상 |
| 비용/성능 | 운영 후 패치 | build-time 차단 | critical CVE 운영 반입 0건 목표 |
| 운영/위험 | 스캔 결과 미반영 | admission control과 연계 | Kubernetes 운영 환경 |

> 요약: 컨테이너 운영 조직은 CI 스캔만으로 끝내지 말고 registry와 admission 단계까지 정책을 연결한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| False Positive | 사용하지 않는 취약 코드 포함 | VEX, risk acceptance 만료일 | 예외 만료 30일 이하 |
| CVE DB 지연 | 신규 취약점 반영 시간차 | daily DB update, registry 재스캔 | 재스캔 주기 24시간 |
| Secret 유출 | 이미지 레이어에 토큰 포함 | secret scan, build secret 사용 | hardcoded secret 0건 |

> 요약: 이미지 스캔 운영은 오탐 예외, DB 갱신, secret 유출을 별도 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 취약점 | critical CVE 0건, high 예외 승인 | Trivy SARIF, JSON report |
| 배포 차단 | 정책 위반 image deploy 0건 | CI log, admission audit |
| 재스캔 | registry 이미지 24시간 내 재평가 | Harbor/Trivy scan schedule |

> 요약: 이미지 스캔 효과는 CVE 수, 차단률, 재스캔 주기로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CI에서 `trivy image --severity HIGH,CRITICAL --exit-code 1`을 적용하고 critical CVE 0건 기준으로 push를 제어함
2. registry에는 digest 기준 SBOM과 스캔 리포트를 저장하고 CVE DB 갱신 시 24시간 내 재스캔을 예약함
3. Kubernetes admission 단계에서 서명 없는 이미지, 스캔 실패 이미지, root 실행 이미지를 OPA/Kyverno로 차단함

**결론 (2줄):**
- 기술사 판단: 단일 CI 스캔은 부족하며 build, registry, admission, runtime 탐지를 계층형으로 구성해야 함
- 향후 방향: Trivy 스캔은 SBOM, VEX, Sigstore 서명과 결합해 컨테이너 공급망 통제로 확장됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 이미지 보안 스캔을 설명하시오" | 이미지 레이어 분석과 CVE 매핑 흐름 | Trivy 대상 범위와 한계 |
| 요구사항 명시형 | "DevSecOps 적용 방안을 제시하시오" | CI, registry, admission 차단 흐름 | CVE 기준, 예외 승인, 재스캔 지표 |

> 요약: 설명형은 스캔 구조, 방안형은 차단 기준과 운영 예외 처리 중심으로 전개한다.
