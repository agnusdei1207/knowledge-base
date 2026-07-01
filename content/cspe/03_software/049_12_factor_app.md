---
title: "12 팩터 앱 (12 Factor App)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 49
---

# 📖 【암기용】 개념 완전 이해

> 목적: 12 Factor App을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라우드 환경에서 배포·운영 가능한 애플리케이션을 만들기 위한 12개 원칙
- **왜 필요한가**: 서버에 직접 설정을 넣고, 로그 파일을 로컬에 남기고, 세션을 메모리에 저장하면 컨테이너와 오토스케일 환경에서 장애와 배포 실패가 늘어남.
- **핵심 직관**: 애플리케이션을 어느 컨테이너에 올려도 같은 방식으로 실행되도록 포장 규격을 맞추는 원칙임.

## 깊이 이해
- **배경·문제의식**: 클라우드는 인스턴스가 생성·삭제되고 배포가 자주 일어남. 환경별 설정, 종속성, 로그, 프로세스 상태를 코드와 분리하지 않으면 재현성이 낮아짐.
- **작동 원리**: 코드베이스는 하나로 관리하고, 설정은 환경변수로 분리함. backing service는 교체 가능한 자원으로 취급하고, build/release/run 단계를 분리함.
- **비유**: 이삿짐 상자에 물건 종류와 주소를 표준 라벨로 붙이면 어느 트럭에 실어도 목적지에서 같은 방식으로 풀 수 있는 것과 같음.
- **구체 예시**: DB 접속정보를 `.env`나 Kubernetes Secret으로 관리하고, 앱은 stdout으로 로그를 출력하며, Pod는 stateless로 구성해 HPA min2/max20으로 수평 확장함.
- **흔한 오해·주의점**: 12 Factor는 특정 프레임워크가 아님. 배포 가능성과 운영 재현성을 높이는 원칙이며, 상태 저장 업무는 외부 저장소와 세션 저장소로 분리해야 함.

## 연결 개념
- Config: 환경별 설정 분리
- Build/Release/Run: 배포 단계 분리
- Stateless Process: 수평 확장과 장애 복구 전제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 12 Factor App은 config, backing service, build/release/run, stateless process, logs, disposability를 클라우드 운영 지표와 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 12 Factor App은 클라우드 네이티브 애플리케이션의 코드, 설정, 종속성, 프로세스, 로그, 배포 방식을 표준화한 원칙이다.
> 2. **가치**: 환경 재현성, 자동 배포, 수평 확장, 장애 복구를 가능하게 하며 컨테이너와 Kubernetes 운영에 적합한 구조를 만든다.
> 3. **판단 포인트**: config 분리, stateless process, backing service 교체성, build/release/run 분리가 지켜지는지 점검해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 앱 원칙 이해 확인 | 12개 factor 중 운영 핵심 항목 | 단순 개발 방법론으로 설명 |
| 배포 자동화 판단 확인 | build/release/run, config, dependency | 서버 수작업 설정 누락 |
| 운영 적합성 확인 | stateless, logs stdout, disposability | 로컬 파일·세션 의존 허용 |

> 요약: 이 문제는 원칙 암기보다 클라우드 배포와 운영 재현성을 확보하는 구조를 요구한다.

---

## Ⅰ. 개요 및 필요성

12 Factor App은 클라우드 운영형 애플리케이션 원칙이다. 컨테이너와 오토스케일 환경에서는 서버 로컬 상태와 수작업 설정이 배포 실패를 만든다. 12 Factor는 코드와 설정을 분리하고 프로세스를 stateless로 만들어 재현성을 확보한다.

---

## Ⅱ. 구조 및 구성요소

```text
Codebase -> Dependency -> Build -> Release -> Run
Config -> Environment Variable / Secret
Backing Service -> DB / Cache / Queue
Process -> Stateless -> Logs stdout -> Fast Startup/Shutdown
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Codebase/Dependencies | 단일 코드베이스와 명시적 종속성 | Git, lock file, container image |
| Config | 환경별 설정 외부화 | env var, Kubernetes Secret |
| Backing Services | DB, cache, queue를 부착 자원화 | URL 교체로 자원 변경 |
| Process/Logs | stateless 실행과 stdout 로그 | HPA, centralized logging |

> 요약: 12 Factor는 코드·설정·자원·프로세스·로그를 분리해 배포 재현성과 수평 확장을 가능하게 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 commit -> 의존성 고정 -> 이미지 build
-> release에 config 결합 -> run으로 실행
-> stateless process 확장 -> stdout log 수집
-> health check와 graceful shutdown 수행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Git codebase와 dependency lock 관리 | 재현 build 성공률 |
| 2 | CI에서 immutable artifact 생성 | image digest, SBOM |
| 3 | release 단계에서 config 주입 | secret 누출 0건 |
| 4 | stateless process 실행과 scale out | HPA min2/max20, startup 30초 |
| 5 | stdout log와 health check 운영 | readiness/liveness success |

> 요약: 12 Factor 앱은 build artifact와 config를 분리하고 stateless process로 실행해 배포와 확장을 자동화한다.

---

## Ⅳ. 특징

| 구분 | 전통 앱 | 12 Factor App | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 설정 | 서버 파일 직접 수정 | env var, secret 외부화 | secret scan 0건 |
| 배포 | build와 run 혼합 | build/release/run 분리 | rollback 10분 이하 |
| 상태 | 로컬 세션·파일 의존 | stateless process | Pod 재시작 후 세션 보존 |
| 로그 | 로컬 파일 | stdout, 중앙 수집 | log ingestion 99% 이상 |

> 요약: 12 Factor는 수작업 서버 운영을 줄이고 자동 배포·수평 확장·중앙 로그 수집을 가능하게 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서버 중심 배포 | artifact+config 분리 | 환경 3개 이상, 배포 주 1회 이상 |
| 비용/성능 | 수직 확장 의존 | stateless 수평 확장 | HPA 반응 30초, CPU 70% 기준 |
| 운영/위험 | 로컬 상태 의존 | disposable process | MTTR 10분 이하 목표 |

> 요약: 12 Factor는 클라우드·컨테이너 환경에서 배포 재현성과 장애 복구 시간을 줄이기 위한 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 설정 누출 | config를 코드에 포함 | Secret Manager, git secret scan | secret leak 0건 |
| 상태 유실 | 로컬 파일·세션 저장 | Redis session, object storage | restart 후 오류율 |
| 배포 재현 실패 | 의존성 미고정 | lock file, image digest | build reproducibility |

> 요약: 주요 리스크는 설정 누출과 로컬 상태 의존이며, secret 관리와 stateless 설계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배포 | rollback 10분 이하, 배포 실패율 5% 이하 | CI/CD 로그 |
| 확장 | HPA min2/max20, startup 30초 이하 | Kubernetes metric |
| 운영 | log loss 1% 이하, readiness 통과율 99% | log pipeline, probe metric |

> 요약: 12 Factor 도입 효과는 배포 실패율, 확장 반응, 로그 수집 품질로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Dockerfile, dependency lock, SBOM을 표준화하고 CI에서 immutable image digest를 생성함.
2. 환경 설정은 Kubernetes ConfigMap/Secret 또는 Vault로 분리하고 DB, cache, queue는 URL 기반 backing service로 연결함.
3. 애플리케이션은 stateless로 만들고 stdout log, readiness/liveness probe, graceful shutdown 30초를 구현함.

**결론 (2줄):**
- 기술사 판단: 클라우드 배포와 오토스케일이 목표이면 12 Factor를 기본 기준으로 삼고, 로컬 상태가 필요한 업무는 외부 저장소 설계를 먼저 수행함.
- 향후 방향: 12 Factor는 container, GitOps, platform engineering과 결합해 개발팀이 표준 배포 경로를 사용하도록 확장됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "12 Factor App을 설명하시오" | build/release/run, config, stateless 흐름 | 전통 앱 대비 운영 차이 |
| 요구사항 명시형 | "클라우드 전환 방안을 제시하시오", "설계하시오" | 컨테이너 배포와 설정 분리 절차 | 배포·확장·로그 지표 |

> 요약: 설명형은 원칙과 구조, 방안형은 클라우드 전환 절차와 운영 검증 지표 중심으로 전환한다.
