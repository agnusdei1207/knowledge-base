---
sidebar:
  order: 45
  label: "045. 12 팩터 앱"
  badge:
    text: "기출 · 50%"
    variant: note
title: "12 팩터 앱 (12 Factor App)"
date: "2026-08-26T17:14:00+09:00"
tags:
  - "notes-software"
weight: 45
extra:
  question_no: "045"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "123회 기출, 클라우드 앱 운영 원칙"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **12 Factor App**: Heroku 창립자들이 클라우드 환경에서 이식성, 확장성, 유지보수성을 극대화하기 위해 정립한 12가지 소프트웨어 아키텍처 원칙.
- **Stateless & Config**: 프로세스를 상태가 없는 무상태로 유지하고, 배포 환경별 설정(DB URL 등)을 환경변수로 주입하는 핵심 철학.

</details>

- 정의/개념: 클라우드 환경에서 이식성과 확장성을 극대화하기 위해 **무상태(Stateless), 환경변수 설정(Config), 선언적 의존성** 등 12개 원칙을 정의한 설계 지침
- 배경/필요성: 로컬 상태·설정 결합으로 **수평 확장·환경 동등성 제약**

#### 한줄 요약
- 컨테이너 기반 수평 확장과 무중단 배포를 지원하는 클라우드 네이티브 12대 개발 원칙이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **개발/운영 동등성(Dev/Prod Parity)**: 개발, 스테이징, 프로덕션 환경의 백엔드 서비스(DB 버전 등)를 최대한 동일하게 유지하여 배포 오류를 차단하는 원칙.
- **폐기 가능성(Disposability)**: 빠른 기동(Fast Startup)과 SIGTERM 수신 시 안전한 종료(Graceful Shutdown)를 보장하는 설계.

</details>

- 설정을 소스 코드에서 완전 분리하여 **OS 환경 변수(ENV)** 로 런타임 주입
- 프로세스를 **무상태(Stateless)** 로 유지하여 Kubernetes 오토스케일링 시 자유로운 복제/소멸
- 빌드-릴리즈-실행의 엄격한 분리 및 **표준 출력(stdout) 기반의 스트림 로그 배출**

#### 한줄 요약
- 환경변수 설정 분리, 무상태 프로세스, stdout 로그 배출로 클라우드 최적화를 달성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **지원 서비스(Backing Services)**: 데이터베이스, 캐시, 메시지 큐 등 프로세스가 네트워크로 연결하는 외부 리소스를 탈부착 가능한 URL 자원으로 취급.

</details>

```text
[12 Factor Cloud-Native 아키텍처]
|-- I. 코드베이스 (Codebase: 단일 Git 저장소에서 여러 환경 배포)
|-- II. 의존성 (Dependencies: 명시적 의존성 선언 및 격리)
|-- III. 설정 (Config: 환경 변수 - ENV로 설정 분리)
|-- IV. 지원 서비스 (Backing Services: DB/Redis를 탈부착 가능한 자원 취급)
|-- V. 빌드/릴리즈/실행 (Build -> Release -> Run 분리)
|-- VI. 프로세스 (Processes: 무상태 - Stateless 프로세스)
|-- VII. 포트 바인딩 (Port Binding: 자체 웹 서버 포트 리스닝)
|-- VIII. 동시성 (Concurrency: 프로세스 모델 기반 Scale-out)
|-- IX. 폐기 가능성 (Disposability: 빠른 시작 & Graceful Shutdown)
|-- X. 개발/운영 동등성 (Dev/Prod Parity: 환경 간 차이 극소화)
|-- XI. 로그 (Logs: stdout 이벤트 스트림 배출)
`-- XII. 관리 프로세스 (Admin Processes: 일회성 관리 작업 격리)
```

선의 의미: 12대 핵심 원칙 계층 구조

| 구성요소 | 책임 |
|:---|:---|
| 설정 | 비밀·환경값의 **ENV 외부 주입** |
| 프로세스 | **무상태 실행·상태 외장화** |
| 빌드·릴리즈·실행 | 불변 산출물의 **단계 분리** |
| 폐기 가능성 | 빠른 기동과 **Graceful Shutdown** |
| 로그 | **stdout 이벤트 스트림 배출** |

#### 한줄 요약
- 단일 코드베이스, ENV 설정, Stateless 프로세스, stdout 로그 배출이 핵심 뼈대다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Build-Release-Run**: 변경 불가능한 바이너리 빌드(Build)에 특정 환경의 Config를 결합하여 고유 릴리즈 ID(Release)를 만들고 실행(Run)하는 파이프라인.

</details>

```text
개발자가 Git 단일 코드베이스(Codebase)에 커밋/푸시
        │
   [Build 단계] 의존성 패키징 및 불변 Docker 이미지 생성
        │
   [Release 단계] 빌드 이미지 + 환경별 Config(K8s ConfigMap/Secret) 결합
        │
   [Run 단계] 포트 바인딩된 Stateless 컨테이너 프로세스 기동
        │
   Kubernetes HPA에 의한 동적 Scale-out (프로세스 복제) 및 자원 자동 회수
```

#### 한줄 요약
- 단일 코드베이스 → 불변 빌드 → 환경설정 결합 릴리즈 → Stateless 실행 순으로 배포된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통 레거시 앱 vs 12 Factor 클라우드 네이티브 앱**: 로컬 상태 의존성과 불변 컨테이너 수평 확장성의 비교.

</details>

| 비교 항목 | 전통 레거시 애플리케이션 | 12 Factor 클라우드 네이티브 앱 |
|:---|:---|:---|
| 설정 관리 | 소스 코드 내 XML/YAML 하드코딩 | **OS 환경 변수(ENV) 외부 주입** |
| 상태 및 세션 | 로컬 톰캣 인메모리 세션 저장 | **완전 무상태 (Stateless), Redis 외장화** |
| 로그 처리 | 로컬 디스크 파일(`app.log`) 롤링 | **표준 출력(`stdout`) 이벤트 스트림** |
| 확장 방식 | 단일 서버 하드웨어 증설(Scale-up) | **컨테이너 단위 즉각 수평 확장(Scale-out)** |
| 기동/종료 | 기동 수 분 소요, 강제 킬(SIGKILL) | **초고속 기동, 우아한 종료(Graceful Shutdown)** |

#### 한줄 요약
- 레거시는 로컬 결합으로 확장이 어렵고, 12 Factor 앱은 완전 분리로 무한 확장을 지원한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Graceful Shutdown(우아한 종료)**: 컨테이너 롤링 업데이트 시 SIGTERM 신호를 받아 신규 요청 유입을 차단하고, 이미 진행 중인 요청을 안전하게 처리한 뒤 종료하는 절차.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Git 레포지토리에 DB 비밀번호 노출 보안 사고 | **K8s Secret 및 Vault 기반 환경 변수 주입** | 소스 코드 유출 시에도 자격 증명 안전 보호 |
| 컨테이너 배포 시 처리 중이던 사용자 요청 유실 | **Spring Boot `graceful-shutdown` 및 SIGTERM 핸들러** | 배포 중 502/503 에러 0화 및 무중단 배포 |
| Pod 재생성 시 컨테이너 로컬 로그 파일 영구 소실 | 로그를 **stdout 배출 후 DaemonSet(Fluentd/Loki) 수집** | 컨테이너 소멸과 무관한 중앙 로그 영구 보존 |
| 로컬 세션 클러스터링 미흡으로 인한 로그인 풀림 | 세션 저장소를 **Redis 클러스터로 외장화** | 인스턴스 소멸 시에도 사용자 세션 100% 유지 |

#### 한줄 요약
- Secret 환경변수 주입, Graceful Shutdown, stdout 중앙 로그화, Redis 세션 외장화로 안정성을 확보한다.

## Ⅶ. 결론

- 클라우드 확장은 **12 Factor 원칙**과 **무상태 컨테이너** 선택

#### 한줄 요약
- 12 Factor App은 애플리케이션을 클라우드 및 컨테이너 플랫폼에 최적화하여 수평 확장과 장애 회복을 자동화하는 필수 엔지니어링 표준이다.
