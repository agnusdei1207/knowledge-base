---
title: "Backstage 개발자 포털 (Backstage Developer Portal)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 296
---

# 📖 【암기용】 개념 완전 이해

> 목적: Backstage 개발자 포털을 처음 보는 사람도 개념과 내부 용어를 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Backstage는 295에서 설명한 **내부 개발자 플랫폼(IDP)** 개념을 실제로 구현하는 **오픈소스 개발자 포털 프레임워크**로, **소프트웨어 카탈로그(Software Catalog)**를 핵심 데이터 모델 삼아 서비스 소유자·문서·템플릿·운영 도구를 한 화면에 연결한다.
- **왜 필요한가**: 마이크로서비스가 수십~수백 개로 늘면 "이 서비스는 누가 담당하지?", "배포는 어떻게 하지?", "문서가 어디 있지?"에 답하는 데 시간이 든다. 이 탐색 비용이 장애 대응 시간(MTTR)과 신규 개발자 온보딩 시간을 직접 늘린다.
- **핵심 직관**: 회사의 모든 서비스에 대한 전화번호부(누가 담당?), 신청 창구(새로 만들려면?), 매뉴얼(문서는?), 상태판(지금 상태는?)을 한 화면에 모은 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| IDP(295와 연결) | Backstage가 구현하는 상위 개념 — 셀프서비스 개발자 플랫폼 | Backstage는 IDP라는 개념의 대표 제품 |
| Software Catalog | 조직의 모든 서비스·API·시스템·팀을 등록·조회하는 핵심 데이터 저장소 | 회사 전체 조직도 겸 서비스 명부 |
| catalog-info.yaml | 각 저장소에 두는, 그 서비스의 메타데이터(소유자·타입·수명주기)를 선언하는 파일 | 서비스의 신분증 |
| Entity(Kind) | 카탈로그에 등록되는 개체 단위 — Component(서비스), API, System(묶음), Resource(DB 등), Group(팀), User | 명부에 등록되는 항목의 종류 |
| Ownership | 어떤 팀(Group)이 어떤 Entity를 소유하는지의 관계 | 담당자 지정 |
| Lifecycle | 서비스의 성숙 단계 — experimental / production / deprecated | 제품의 생애주기 라벨 |
| TechDocs | 코드 저장소 안 마크다운 문서를 MkDocs로 빌드해 포털에서 바로 보여주는 기능 | 코드 옆에 붙어 다니는 자동 갱신 매뉴얼 |
| Scaffolder | 템플릿 기반으로 새 저장소·CI·배포 설정을 자동 생성하는 기능(295의 Golden Path 구현체) | 붕어빵 틀을 실제로 눌러 찍는 기계 |
| Plugin | Backstage에 외부 도구(CI, Kubernetes, SonarQube 등) 데이터를 붙이는 확장 모듈 | 스마트폰 앱 하나하나 |

## 깊이 이해

### catalog-info.yaml — 실제 구조로 이해하기
- 모든 서비스 저장소 루트에 `catalog-info.yaml`을 두면, Backstage의 catalog processor가 주기적으로 이를 읽어 카탈로그에 등록한다. 최소 예시는 다음과 같다.
  - `apiVersion: backstage.io/v1alpha1`
  - `kind: Component`
  - `metadata.name: order-service`
  - `spec.type: service`
  - `spec.owner: team-payments` (Group Entity 참조)
  - `spec.lifecycle: production`
  - `spec.system: billing` (System Entity 참조)
- 이 필드들이 곧 카탈로그 그래프의 노드와 간선이 된다: `order-service`는 `team-payments`가 소유하고(ownedBy), `billing` 시스템에 속하며(partOf), 다른 서비스와의 의존 관계도 `spec.dependsOn: [resource:orders-db]`처럼 선언한다.
- 이 관계 데이터 덕분에 "이 DB가 죽으면 어떤 서비스가 영향받는가"를 그래프 탐색으로 즉시 답할 수 있다 — 장애 대응(MTTR) 시간이 줄어드는 핵심 이유다.

### Scaffolder 동작 — 신규 서비스가 만들어지는 과정
1. 개발자가 포털에서 "Spring Boot Microservice" 템플릿을 선택하고 서비스 이름·소유팀 같은 파라미터를 입력한다.
2. Scaffolder는 `template.yaml`에 정의된 단계(steps)를 순서대로 실행한다 — 예: `fetch:template`(뼈대 코드 복제) → `publish:github`(신규 저장소 생성) → `catalog:register`(방금 만든 저장소의 catalog-info.yaml을 자동으로 카탈로그에 등록).
3. 결과적으로 몇 분 안에 Git 저장소, CI 파이프라인 설정, catalog 등록, (연동돼 있다면) Kubernetes 네임스페이스까지 표준 상태로 생성된다 — 이것이 295에서 말한 "리드타임 5일 → 수 분" 셀프서비스의 실제 구현 지점이다.

### Plugin 아키텍처 — 왜 "포털"이 아니라 "프레임워크"인가
- Backstage 자체는 카탈로그·문서·템플릿 코어만 제공하고, CI 상태·Kubernetes pod 상태·SonarQube 코드 품질·PagerDuty 알림 이력 등은 각각 별도 Plugin이 외부 API를 호출해 포털 화면에 끼워 넣는다.
- 예: Kubernetes 플러그인은 카탈로그의 `order-service` Entity와 실제 클러스터의 `order-service` 배포를 라벨로 매칭해, 포털 화면에 pod 개수·재시작 횟수를 실시간으로 보여준다.
- 이 구조 때문에 Backstage는 "고정된 대시보드"가 아니라, 조직마다 필요한 도구를 꽂아 넣는 "포털을 만드는 프레임워크"로 봐야 한다.

### 비유와 흔한 오해
- **비유**: 대학 포털에서 수강신청(Scaffolder), 강의계획서(TechDocs), 성적·수강 이력(Catalog), 공지·연동 시스템(Plugin)을 한 화면에서 보는 것과 같다.
- **오해**: "Backstage를 설치하면 플랫폼 엔지니어링이 완성된다"가 아니다. Backstage는 그릇일 뿐이고, catalog-info.yaml을 팀마다 정확히 채워 넣는 **데이터 품질**(ownership 정합성, lifecycle 최신화)과 템플릿을 계속 관리하는 **거버넌스**가 없으면 곧 정보가 낡은(stale) 빈 포털이 된다. 293~295에서 다룬 서명·재현성·정책 통제도 결국 이 카탈로그의 owner·lifecycle 데이터를 기준으로 누구에게 책임을 물을지 정해진다.

## 연결 개념
- Service Catalog — Backstage의 핵심 데이터 모델(소유자·의존성·수명주기)
- TechDocs — 문서를 코드와 함께 최신 상태로 유지하는 서브시스템
- Platform Engineering Self-Service(295) — Backstage가 구현하는 상위 운영 모델, Scaffolder가 그 실행 도구

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. Backstage를 도구명이 아니라 개발자 포털 아키텍처로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Backstage는 서비스 카탈로그와 플러그인 생태계를 기반으로 개발자 작업 진입점을 통합하는 IDP 프레임워크이다.
> 2. **가치**: 소유자, 문서, 템플릿, 운영 상태를 한 화면에 연결해 온보딩 시간과 서비스 탐색 시간을 줄인다.
> 3. **판단 포인트**: catalog 메타데이터 품질과 template governance가 없으면 포털은 링크 모음으로 전락한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IDP 구현 기술 이해 확인 | Catalog, TechDocs, Scaffolder, Plugins | 단순 위키·링크 포털로 설명 |
| 플랫폼 엔지니어링 적용 확인 | ownership, golden path, self-service | 설치 절차만 나열 |
| 운영 거버넌스 확인 | catalog 품질, RBAC, template versioning | 서비스 메타데이터 최신성 누락 |

> 요약: 이 문제는 Backstage 기능보다 카탈로그 기반 개발자 경험과 운영 거버넌스 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Backstage는 내부 개발자 포털 프레임워크이다.
- 배경: MSA 환경에서는 서비스 소유자, 문서, CI/CD, 운영 상태가 여러 도구에 흩어진다.
- 필요성: 서비스 카탈로그와 플러그인으로 개발자 셀프서비스와 운영 정보를 통합해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Developer -> Backstage UI -> Software Catalog -> Plugins -> External Tools
                             / TechDocs
                             / Scaffolder Templates
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Software Catalog | Component, API, System, Group 관리 | catalog-info.yaml 기반 |
| TechDocs | 저장소 기반 문서 생성·조회 | MkDocs 연동 |
| Scaffolder | 서비스·라이브러리 템플릿 생성 | golden path 구현 |
| Plugins | CI, Kubernetes, 보안, 모니터링 연결 | 플러그인 품질 관리 필요 |

> 요약: Backstage는 카탈로그를 중심에 두고 문서, 템플릿, 외부 도구 플러그인을 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
catalog-info 작성 -> Repository 등록 -> Catalog 수집 -> Plugin 데이터 연결 -> Portal 조회/실행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스 저장소에 catalog-info.yaml 작성 | owner·lifecycle 필수 |
| 2 | Backstage catalog processor가 메타데이터 수집 | 등록 성공률 95% 이상 |
| 3 | TechDocs·CI·K8s 플러그인이 외부 API 조회 | 토큰 권한 최소화 |
| 4 | Scaffolder로 신규 서비스 생성 | 표준 템플릿 사용률 80% 이상 |

> 요약: 동작은 메타데이터 수집, 외부 도구 연결, 포털 조회, 템플릿 실행으로 이어진다.

---

## Ⅳ. 특징

| 구분 | 분산 도구 운영 | Backstage 포털 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 정보 탐색 | 위키·채팅 검색 | 카탈로그 단일 조회 | owner 등록률 100% |
| 문서 | 저장소·위키 분산 | TechDocs 통합 | 문서 최신성 30일 이내 |
| 생성 | 수동 저장소 생성 | Scaffolder 자동화 | 템플릿 사용률 80% 이상 |
| 한계 | 도구 설치 불필요 | catalog 유지관리 필요 | stale entity 5% 이하 |

> 요약: Backstage는 정보 탐색과 서비스 생성을 통합하지만, 메타데이터 최신성 관리가 성패를 좌우한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 위키+CI 링크 모음 | catalog 중심 IDP | 서비스 50개 이상 |
| 비용/성능 | 초기 구축 낮음 | 플러그인·운영 비용 발생 | 온보딩 1주 이상 소요 조직 |
| 운영/위험 | 소유자 불명확 | owner·lifecycle 관리 | 운영 책임 추적 필요 |

> 요약: 서비스 수와 도구 수가 늘면 링크 포털보다 catalog 중심 Backstage가 관리 기준을 제공한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 카탈로그 부정확 | owner 변경 미반영 | repository PR check, stale scan | stale entity 비율 |
| 플러그인 과다 | 무분별한 연동 | plugin review board | 플러그인 장애 건수 |
| 접근 권한 오류 | 외부 도구 토큰 과권한 | RBAC, service account 분리 | 권한 위반 감사 건수 |

> 요약: Backstage 운영 위험은 카탈로그 품질, 플러그인 관리, 접근 권한에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 카탈로그 품질 | owner·lifecycle 등록 100% | catalog lint |
| 개발자 사용 | 월 활성 사용자 70% 이상 | portal analytics |
| 셀프서비스 | 템플릿 생성 성공률 95% 이상 | Scaffolder task log |

> 요약: 성공 여부는 카탈로그 완전성, 사용률, 템플릿 실행 성공률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. `catalog-info.yaml` 표준을 정의해 owner, system, lifecycle, dependency, SLO link를 PR 필수 검증 항목으로 지정
2. Scaffolder로 Spring Boot, Node API, batch service 템플릿을 제공하고 GitHub Actions·Argo CD·Grafana 링크 자동 생성
3. TechDocs와 Kubernetes·SonarQube·PagerDuty 플러그인을 연동하되 RBAC와 토큰 범위를 서비스 단위로 제한

**결론 (2줄):**
- 기술사 판단: 서비스와 도구가 분산된 조직은 Backstage로 카탈로그를 먼저 구축하고, 템플릿·플러그인은 사용률 기준으로 단계 확대
- 향후 방향: IDP는 포털 구축보다 ownership, scorecard, golden path 품질을 지속 개선하는 플랫폼 제품 운영으로 발전해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | catalog 수집, plugin 연결, scaffolder 실행 | 위키·링크 포털과 차이 |
| 요구사항 명시형 | "설계하시오", "운영 방안", "비교하시오" | 카탈로그 표준, RBAC, 템플릿 거버넌스 | stale entity, 플러그인 리스크, 지표 |

> 요약: 설명형은 구성요소, 설계형은 카탈로그 품질과 권한 통제 기준 중심으로 전환한다.
