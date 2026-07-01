---
title: "Backstage 개발자 포털 (Backstage Developer Portal)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 296
---

# 📖 【암기용】 개념 완전 이해

> 목적: Backstage 개발자 포털을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 서비스 카탈로그, 문서, 템플릿, 플러그인을 한곳에 묶는 오픈소스 내부 개발자 포털
- **왜 필요한가**: 서비스가 많아지면 소유자, API, 배포 상태, 문서가 흩어져 장애 대응과 온보딩 시간이 길어진다.
- **핵심 직관**: 회사의 모든 서비스에 대한 전화번호부, 신청 창구, 매뉴얼, 상태판을 한 화면에 모은 것이다.

## 깊이 이해
- **배경·문제의식**: MSA와 클라우드 전환 후 서비스 수와 도구 수가 증가했다. 개발자는 소유자를 찾고 배포 방법을 확인하는 데 시간을 쓴다.
- **작동 원리**: Backstage는 `catalog-info.yaml`로 서비스 메타데이터를 수집하고, TechDocs로 문서를 제공하며, Scaffolder 템플릿으로 새 서비스를 생성한다. 플러그인으로 CI, Kubernetes, SonarQube, PagerDuty를 연결한다.
- **비유**: 대학 포털에서 수강신청, 강의계획서, 성적, 공지를 한 번에 보는 것처럼 개발자가 서비스 정보를 한곳에서 확인한다.
- **구체 예시**: `owner: team-payments`, `system: billing`, `lifecycle: production`을 catalog에 등록하면 소유팀, 의존성, 배포 상태를 포털에서 조회한다.
- **흔한 오해·주의점**: Backstage 설치 자체가 플랫폼 엔지니어링은 아니다. 카탈로그 품질, 템플릿 관리, 플러그인 운영, ownership 정합성이 더 큰 과제이다.

## 연결 개념
- Service Catalog - 서비스 소유자·의존성·수명주기 관리
- TechDocs - 문서를 코드 저장소와 함께 관리
- Scaffolder - 표준 서비스 템플릿 자동 생성

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

Backstage는 Spotify가 공개한 내부 개발자 포털 프레임워크이다. MSA 환경에서는 서비스 소유자, 문서, CI/CD, 운영 상태가 여러 도구에 흩어진다. Backstage는 서비스 카탈로그와 플러그인을 중심으로 개발자 셀프서비스와 운영 정보를 통합한다.

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
