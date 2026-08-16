---
sidebar:
  order: 45
  label: "045. 12 팩터 앱 (12 Factor App)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "12 팩터 앱 (12 Factor App)"
date: "2026-08-13T15:06:00+09:00"
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

- **The Twelve-Factor App (12-Factor App)**: Heroku 엔지니어들이 정립한 모던 클라우드 네이티브(Cloud-Native) SaaS 애플리케이션 구축 및 배포를 위한 12가지 베스트 프랙티스 아키텍처 원칙.
- **Cloud-Native App**: 클라우드 가상화/컨테이너(Kubernetes) 환경에서 수평적 확장(Scale-out), 자동 배포, 및 장애 복구(Self-healing)가 최적화되어 작동하는 소프트웨어.
- **Stateless App**: 애플리케이션 실행 프로세스가 로컬 세션이나 상태를 가지지 않고(Stateless), 모든 상태 데이터를 외부 공유 서비스(Redis, DB)로 위임하는 상태 구조.

</details>

- 정의/개념: 클라우드 컨테이너 환경에서 이식성(Portability), 수평적 확장성(Scale-out) 및 자동화 배포를 극대화하기 위한 12가지 모던 소프트웨어 개발 원칙인 **12-Factor App**
- 배경/필요성: 서버별 설정•로컬 상태는 **환경 재현과 수평 확장 방해**

#### 한줄 요약

- 상태•설정 외부화를 통한 열두 팩터 앱과 수평 확장이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Dev/Prod Parity (개발/운영 환경 동등성)**: 개발 환경, 검증 환경, 실운영 환경 간의 도구, DB, 네트워크 격차를 최소화하여 "내 컴퓨터에선 되는데요" 장애를 차단하는 원칙.
- **Disposability (폐기 가능성)**: 프로세스가 빠른 시작(Fast Startup)과 안전한 종료(Graceful Shutdown)를 지원하여 언제든 파기 및 재생성 가능한 상태.

</details>

- 환경 변수(Environment Variables) 기반 설정 분리 및 코드-설정 완전 격리
- 무상태(**Stateless**) 프로세스 및 수평적 동시성(**Concurrency**) 확장
- **Dev/Prod Parity** 및 빠른 시작/안전 종료(**Disposability**) 확보

#### 한줄 요약

- 의존성, 무상태 프로세스, 개발•운영 환경 동등성이 재현성을 만든다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| 코드베이스•의존성 | 버전 원본과 모든 런타임 의존성 명시 |
| 빌드•릴리스•실행 | 불변 빌드와 환경 설정 결합•실행 분리 |
| 설정•지원 서비스 | 설정 외부화와 DB•Broker 자원 바인딩 |
| 프로세스•동시성 | 무상태 프로세스를 단위로 수평 확장 |
| 폐기•로그•관리 작업 | 안전 종료•스트림 로그•일회성 작업 분리 |

#### 한줄 요약

- 설정, 지원 서비스, 빌드, 릴리스, 실행, 프로세스의 책임 분리가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Build-Release-Run Pipeline**: 코드 컴파일(Build) $\rightarrow$ 환경 변수 결합(Release) $\rightarrow$ 프로세스 구동(Run)을 명확히 3단계로 차단 분리하는 배포 흐름.

</details>

```text
┌──────────────────────────────┐
│ Git Codebase (단일 원본)    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 빌드                     │
│ 2. 릴리스                   │
│ 3. 실행                     │
│ 4. 로그 스트리밍            │
└──────────────┬───────────────┘
               ▼
        [런타임 운영]
```

### 동작 원리

1. 빌드: 코드와 명시된 의존성으로 불변 실행물 생성
2. 릴리스: 빌드에 환경별 **Config**를 결합해 버전 부여
3. 실행: 릴리스를 무상태 프로세스로 구동
4. 로그 스트리밍: 표준 출력 이벤트를 외부 수집기로 전달

#### 한줄 요약

- 릴리스 승격과 무상태 프로세스 확장 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **Graceful Shutdown**: SIGTERM 신호 수신 시 진행 중인 HTTP 요청을 모두 완결 처리한 후 안전하게 프로세스를 파기(Disposability)하는 종료 처리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 코드 저장소에 비밀정보 포함 | **Secrets Manager•Vault**로 설정 주입 | 코드와 비밀정보 수명주기 분리 |
| 재시작 중 진행 요청 유실 | **Graceful Shutdown**과 준비 상태 제거 | 신규 유입 차단 후 처리 종료 |
| 로컬 로그 증가로 디스크 고갈 | **stdout 스트림**과 외부 보존 정책 적용 | 실행 노드와 로그 수명 분리 |

> 사례: **Kubernetes + Docker + Spring Boot 3** 기반 12-Factor App 전면 수용

#### 한줄 요약

- 세션 외부화, 정상 종료, 배포 재현성을 확보한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Cloud-Native 설계 기준(Cloud-Native Architecture Standards)**: 컨테이너 오케스트레이션, CI/CD 자동화 및 12-Factor 지침 준수율에 의거한 체계.

</details>

- 반복 배포•수평 확장이 필요하면 **12-Factor**, 고정 장비 앱은 선별 적용

#### 한줄 요약

- 반복 배포와 수평 확장 요구를 함께 평가하는 것이 핵심이다.
