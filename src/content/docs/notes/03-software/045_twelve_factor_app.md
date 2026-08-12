---
sidebar:
  order: 45
  label: "045. 12 팩터 앱 (12 Factor App)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "12 팩터 앱 (12 Factor App)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **The Twelve-Factor App (12-Factor App)**: Heroku 엔지니어들이 정립한 모던 클라우드 네이티브(Cloud-Native) SaaS 애플리케이션 구축 및 배포를 위한 12가지 베스트 프랙티스 아키텍처 원칙.
- **Cloud-Native App**: 클라우드 가상화/컨테이너(Kubernetes) 환경에서 수평적 확장(Scale-out), 자동 배포, 및 장애 복구(Self-healing)가 최적화되어 작동하는 소프트웨어.
- **Stateless App**: 애플리케이션 실행 프로세스가 로컬 세션이나 상태를 가지지 않고(Stateless), 모든 상태 데이터를 외부 공유 서비스(Redis, DB)로 위임하는 상태 구조.

</details>

- 정의/개념: 클라우드 컨테이너 환경에서 이식성(Portability), 수평적 확장성(Scale-out) 및 자동화 배포를 극대화하기 위한 12가지 모던 소프트웨어 개발 원칙인 **12-Factor App**
- 배경/필요성: 서버 의존적 설정, 로컬 파일/세션 저장으로 인한 컨테이너 확장(Scale-out) 불능 및 환경(Dev/Staging/Prod) 불일치 장애 극복 요구성

#### 한줄 요약

- 상태•설정 외부화를 통한 열두 팩터 앱과 수평 확장이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Dev/Prod Parity (개발/운영 환경 동등성)**: 개발 환경, 검증 환경, 실운영 환경 간의 도구, DB, 네트워크 격차를 최소화하여 "내 컴퓨터에선 되는데요" 장애를 차단하는 원칙.
- **Disposability (폐기 가능성)**: 프로세스가 빠른 시작(Fast Startup)과 안전한 종료(Graceful Shutdown)를 지원하여 언제든 파기 및 재생성 가능한 상태.

</details>

- 환경 변수(Environment Variables) 기반 설정 분리 및 코드-설정 완전 격리
- 무상태(**Stateless**) 프로세스 및 수평적 동시성(**Concurrency**) 확장
- **Dev/Prod Parity** 및 빠른 시작/안전 종료(**Disposability**) 확보

#### 한줄 요약

- 의존성, 무상태 프로세스, 개발•운영 환경 동등성이 재현성을 만든다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Backing Services**: 애플리케이션이 네트워크를 통해 이용하는 모든 부가 서비스(Database, Message Broker, SMTP, Caching)를 바인딩된 자원으로 취급하는 원칙.

</details>

```text
[코드베이스•의존성]
          |
[빌드•릴리스•실행] --- [설정•지원 서비스]
          |
  [프로세스•동시성]
          |
[폐기•로그•관리 작업]
```

선의 의미: Codebase가 Build-Release-Run 단계를 거쳐 Stateless Process로 구동되고, Config 및 Backing Services가 외부 연결 결합되는 12가지 요소 구조.

| 번호 | 12-Factor 원칙 (Factors) | 핵심 정의 및 내용 |
|:---|:---|:---|
| **Ⅰ. Codebase** | 단일 코드베이스 (One Codebase) | 하나의 코드베이스가 버전에 따라 추적되고 여러 환경에 배포 |
| **Ⅱ. Dependencies** | 의존성 명시 (Explicit Dependencies)| Maven/npm/pip 등을 통해 외부 라이브러리 명시적 격리 선언 |
| **Ⅲ. Config** | 리포지토리 설정 분리 (In Environment)| 환경 변수(ENV)를 통해 코드와 설정을 엄격히 분리 관리 |
| **Ⅳ. Backing Services**| 보조 서비스 (Backing Services) | DB, 메시지 큐 등 외부 서비스를 바인딩된 원격 자원으로 취급 |
| **Ⅴ. Build, Release, Run**| 빌드, 릴리스, 실행 분리 | **Build(바이너리 생성) $\rightarrow$ Release(설합) $\rightarrow$ Run(실행)** 엄격 분리 |
| **Ⅵ. Processes** | 무상태 프로세스 (Stateless) | **프로세스는 무상태(Stateless)로 구동, 세션은 Redis로 외부화** |
| **Ⅶ. Port Binding** | 포트 바인딩 (Port Binding) | 웹 앱이 자체 포트(e.g., 8080)를 독립 바인딩하여 직접 서비스 |
| **Ⅷ. Concurrency** | 동시성 수평 확장 (Scale-out) | 프로세스 모델을 통해 수평적으로 인스턴스(Scale-out) 확장 |
| **Ⅸ. Disposability** | 빠른 시작과 안전한 종료 | 빠른 스타트업 및 **Graceful Shutdown (SIGTERM 처리)** |
| **Ⅹ. Dev/Prod Parity**| 환경 동등성 유지 | 개발, 검증, 운영 환경을 최대한 유사하게 유지 |
| **Ⅺ. Logs** | 로그 이벤트 스트림 처리 | 로그를 파일 저장이 아닌 **stdout(표준 출력) 스트림**으로 분사 |
| **Ⅻ. Admin Processes** | 일회성 관리 프로세스 분리 | DB 마이그레이션 등 일회성 관리 작업을 동등 환경에서 실행 |

#### 한줄 요약

- 설정, 지원 서비스, 빌드, 릴리스, 실행, 프로세스의 책임 분리가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Build-Release-Run Pipeline**: 코드 컴파일(Build) $\rightarrow$ 환경 변수 결합(Release) $\rightarrow$ 프로세스 구동(Run)을 명확히 3단계로 차단 분리하는 배포 흐름.

</details>

```text
┌──────────────────────────────┐
│ Git Codebase (단일 원본)    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Build (바이너리/이미지)  │
│ 2. Release (Config ENV 결합) │
│ 3. Run (Stateless Process)   │
│ 4. Log Stream (stdout 분사)  │
└──────────────┬───────────────┘
               ▼
   [Scale-out 수평 확장 완료]
```

### 동작 원리

1. **Build Phase**: 소스코드 + 의존성(Dependencies)을 묶어 실행 바이너리(Docker Image) 획득.
2. **Release Phase**: 생성된 불변 Build 이미지에 특정 환경(Dev/Prod)의 **Config (ENV)** 값 주입 결합.
3. **Run Phase**: K8s 노드 상에서 **Stateless Process** 인스턴스로 즉시 디스패치 구동.
4. **Log Streaming**: 모든 런타임 로그를 로컬 파일이 아닌 `stdout` 이벤트 스트림으로 분사하여 Fluentd가 수거.

#### 한줄 요약

- 릴리스 승격과 무상태 프로세스 확장 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Legacy Monolith vs 12-Factor App**: Legacy는 로컬 서버 파일/세션 상주 및 하드코딩 설정으로 스케일아웃 불가, 12-Factor는 완벽한 무상태와 환경변수 분리로 컨테이너 최적화.

</details>

| 비교 항목 | Traditional Application | 12-Factor Cloud-Native App |
|:---|:---|:---|
| 설정 관리 | properties/xml 파일 코드 포함 | **OS 환경 변수 (ENV) 외부 수시 주입** |
| 세션/상태 관리 | 웹 서버 로컬 메모리 세션 (Sticky Session) | **Stateless (Redis / Memcached 외부 분리)** |
| 로그 처리 | `/var/log/app.log` 로컬 파일 기록 | **stdout / stderr (표준 출력 이벤트 스트림)** |
| 스케줄 작업 | 서버 내부 Crontab 개별 스케줄링 | **독립 Admin Process (K8s CronJob)** |

#### 한줄 요약

- 반복 배포•수평 확장은 12 팩터 앱을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Graceful Shutdown**: SIGTERM 신호 수신 시 진행 중인 HTTP 요청을 모두 완결 처리한 후 안전하게 프로세스를 파기(Disposability)하는 종료 처리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Git 리포지토리 내 DB 비밀번호 포함 (Config 위반) | **AWS Secrets Manager / Vault / ENV 주입** | 보안 유출 파괴 차단 |
| Pod 배포 재시작 시 진행 중인 유저 요청 강제 유실 | **Graceful Shutdown (SIGTERM 핸들링)** 구현 | 유저 트랜잭션 안전 보장 |
| 디스크 용량 초과로 인한 서버 다운 | 로컬 파일 기록 금지 및 **stdout 스트림 $\rightarrow$ EFK Stack** 수거 | 무제한 인프라 관측성 확보 |

> 사례: **Kubernetes + Docker + Spring Boot 3** 기반 12-Factor App 전면 수용

#### 한줄 요약

- 세션 외부화, 정상 종료, 배포 재현성을 확보한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Cloud-Native 설계 기준(Cloud-Native Architecture Standards)**: 컨테이너 오케스트레이션, CI/CD 자동화 및 12-Factor 지침 준수율에 의거한 체계.

</details>

- **Cloud-Native 설계 기준**에 따라 현대 MSA 및 Kubernetes 파이프라인 구축 시 **12-Factor App 원칙** 필수 집행

#### 한줄 요약

- 반복 배포와 수평 확장 요구를 함께 평가하는 것이 핵심이다.
