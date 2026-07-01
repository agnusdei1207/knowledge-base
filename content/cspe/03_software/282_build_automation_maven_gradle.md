---
title: "빌드 자동화 - Maven·Gradle (Build Automation)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 282
---

# 📖 【암기용】 개념 완전 이해

> 목적: 빌드 자동화를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 소스코드를 실행 가능한 산출물로 반복 생성하는 자동 절차
- **왜 필요한가**: 개발자 PC마다 빌드 명령과 라이브러리 버전이 다르면 같은 소스에서도 다른 결과가 나온다. 빌드 자동화는 컴파일, 테스트, 패키징, 배포 전 검증을 표준 명령으로 고정한다.
- **핵심 직관**: 빌드는 요리 레시피와 같다. Maven과 Gradle은 재료 의존성과 조리 순서를 기계가 재현하도록 만든 레시피 엔진이다.

## 깊이 이해
- **배경·문제의식**: 수동 빌드는 누락된 테스트, 다른 JDK 버전, 로컬 캐시 오염으로 재현성이 깨진다. CI 환경에서는 커밋마다 동일한 빌드 산출물을 만들어야 한다.
- **작동 원리**: Maven은 `pom.xml`과 표준 생명주기(validate, compile, test, package)를 중심으로 동작한다. Gradle은 task DAG와 incremental build, build cache로 변경된 부분만 재실행한다.
- **비유**: Maven은 정해진 공정표가 있는 조립 라인이고, Gradle은 필요한 작업만 골라 병렬로 돌리는 작업 스케줄러에 가깝다.
- **구체 예시**: Java 17 Spring Boot 서비스에서 `mvn test package` 또는 `gradle build`를 CI에서 실행하고, JUnit 실패율 0%, JaCoCo line coverage 80% 이상일 때만 컨테이너 이미지를 만든다.
- **흔한 오해·주의점**: 빌드 자동화는 단순 컴파일 자동화가 아니다. 의존성 고정, 테스트 게이트, SBOM 생성, artifact 저장소 배포까지 포함해야 운영 배포와 연결된다.

## 연결 개념
- CI/CD 파이프라인 - 빌드 자동화 실행 위치
- 패키지 관리 - 의존성 해석과 버전 고정
- 소프트웨어 공급망 보안 - 빌드 산출물 서명과 SBOM

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Maven·Gradle 도구 비교가 아니라 재현 가능한 산출물, 테스트 게이트, 의존성 통제 관점으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 빌드 자동화는 컴파일, 테스트, 패키징, 아티팩트 게시를 표준 절차로 실행하는 개발 자동화 체계이다.
> 2. **가치**: 동일 소스 동일 산출물, 테스트 자동 게이트, 배포 가능 패키지 생성으로 변경 실패율을 낮춘다.
> 3. **판단 포인트**: Maven은 표준 생명주기, Gradle은 task DAG와 캐시 기반 대규모 빌드에 적합하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 빌드 자동화 구성 이해 확인 | compile, test, package, publish 생명주기 | 컴파일 명령만 설명하고 테스트·아티팩트 누락 |
| Maven·Gradle 비교 판단 확인 | Maven convention, Gradle task DAG와 cache | 한 도구가 모든 환경에서 우위라고 단정 |
| CI/CD 연계 역량 확인 | 품질 게이트, artifact repository, SBOM | 로컬 빌드와 운영 배포 연결 누락 |

> 요약: 빌드 자동화 문제는 도구 이름보다 재현성, 품질 게이트, 산출물 추적성을 연결해야 득점 가능하다.

---

## Ⅰ. 개요 및 필요성

빌드 자동화는 소스에서 산출물을 만드는 절차이다. 애플리케이션은 컴파일, 단위 테스트, 정적 분석, 패키징을 거쳐 배포 가능한 artifact가 된다. 자동화가 없으면 개발자 환경 차이와 누락된 검증으로 배포 실패와 결함 유입이 증가한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> Dependency Resolve -> Compile -> Test -> Package -> Artifact Repository
                  +-> Maven pom.xml / Gradle build.gradle
                  +-> Quality Gate / SBOM
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 빌드 스크립트 | 의존성, 플러그인, task 정의 | Maven pom.xml, Gradle Kotlin/Groovy DSL |
| 의존성 해석기 | 라이브러리 버전과 전이 의존성 계산 | Maven Central, private repository |
| 테스트 게이트 | 단위·통합 테스트와 커버리지 검증 | JUnit, JaCoCo 80% 기준 |
| 아티팩트 저장소 | jar, war, container image 보관 | Nexus, Artifactory, GitHub Packages |

> 요약: 빌드 자동화는 스크립트, 의존성, 테스트, 저장소를 묶어 산출물 생성 절차를 반복 가능하게 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
커밋 발생 -> CI 빌드 실행 -> 의존성 다운로드 -> 컴파일 -> 테스트 -> 패키징 -> 게시
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 빌드 환경 준비 | JDK 17, wrapper 버전 고정 |
| 2 | 의존성 해석과 캐시 사용 | lockfile, checksum 검증 |
| 3 | 컴파일과 정적 분석 | compile error 0건, Checkstyle 위반 0건 |
| 4 | 테스트와 패키징 | JUnit 실패 0건, coverage 80% 이상 |
| 5 | artifact 게시 | 버전 태그, checksum, SBOM 생성 |

> 요약: 빌드 자동화는 커밋 단위로 동일한 환경에서 검증된 산출물을 만들고 저장소에 게시한다.

---

## Ⅳ. 특징

| 구분 | Maven | Gradle | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 실행 모델 | 표준 lifecycle 중심 | task DAG 중심 | multi-module 100개 이상에서 cache 효과 |
| 설정 방식 | XML convention | Groovy/Kotlin DSL | convention vs flexibility |
| 증분 처리 | 플러그인 의존 | incremental build, build cache | 변경 파일 기준 task 재실행 |
| 적용 환경 | 기업 표준 Java 프로젝트 | Android, 대규모 JVM 프로젝트 | Gradle wrapper로 버전 고정 |

> 요약: Maven은 표준화된 생명주기, Gradle은 캐시와 task DAG가 필요한 대규모 빌드에 맞춘다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | IDE 수동 빌드 | CI 기반 자동 빌드 | 커밋당 검증 필요 여부 |
| 비용/성능 | 전체 재빌드 | incremental build, cache | 빌드 시간 10분 초과 시 Gradle cache 검토 |
| 운영/위험 | 산출물 로컬 공유 | artifact repository 게시 | 감사·롤백을 위한 versioning 필요 |

> 요약: 빌드 시간이 길고 모듈 수가 많으면 Gradle 캐시, 표준 Java 업무 시스템은 Maven convention을 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 재현성 깨짐 | 로컬 JDK·플러그인 차이 | Maven/Gradle wrapper, Docker build image | build reproducibility 100% |
| 의존성 오염 | 전이 의존성 버전 충돌 | dependency lock, BOM, checksum | dependency conflict 0건 |
| 테스트 우회 | 개발자 로컬 검증 누락 | CI quality gate 강제 | main branch failed build 0건 |

> 요약: 빌드 자동화 리스크는 환경 차이, 의존성 충돌, 테스트 우회이며 wrapper와 CI 게이트로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 빌드 시간 | PR 빌드 10분 이하 | CI duration metric |
| 품질 게이트 | 테스트 실패 0건, coverage 80% 이상 | JUnit, JaCoCo report |
| 산출물 추적 | commit-artifact-SBOM 100% 연결 | Git tag, repository metadata |

> 요약: 빌드 자동화는 시간, 품질, 추적성 지표가 동시에 충족될 때 배포 파이프라인의 입력으로 사용한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Maven 프로젝트는 BOM과 `mvnw`를 적용해 Spring Boot, JDK, 플러그인 버전을 고정하고 `mvn verify`를 PR 게이트로 설정함
2. Gradle 프로젝트는 configuration cache와 remote build cache를 적용해 multi-module 빌드 시간을 30분에서 10분 이하로 줄이는 목표를 둠
3. CI에서 SBOM(CycloneDX), checksum, artifact 서명을 생성하고 Nexus/Artifactory에 versioned artifact로 게시함

**결론 (2줄):**
- 기술사 판단: 표준 업무 시스템은 Maven, 대규모 모듈·Android·증분 빌드 요구는 Gradle을 선택함
- 향후 방향: 빌드 자동화는 SLSA, SBOM, provenance attestation과 결합해 공급망 통제 기반으로 발전함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "빌드 자동화를 설명하시오" | 컴파일·테스트·패키징 생명주기 | Maven·Gradle 특징과 CI 연계 |
| 요구사항 명시형 | "Maven과 Gradle을 비교하시오", "도입 방안을 제시하시오" | task DAG, cache, lifecycle 차이 | 빌드 시간·모듈 규모·재현성 선택 기준 |

> 요약: 설명형은 생명주기 중심, 비교형은 도구별 실행 모델과 적용 조건 중심으로 답안을 전개한다.
