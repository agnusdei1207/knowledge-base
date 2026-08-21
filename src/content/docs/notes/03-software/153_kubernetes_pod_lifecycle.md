---
sidebar:
  order: 153
  label: "153. 쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-08-18T01:45:00+09:00"
tags: ["notes-software"]
weight: 153
extra:
  question_no: "153"
  source_status: "기출"
  source_history: "123회"
  priority: 30
  priority_note: "파드 상태 전이와 프로브 역할 구분 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **파드 생명주기(Pod Lifecycle)**: 파드의 생성(Pending), 실행(Running), 성공/실패(Succeeded/Failed)의 상태 전이와 3대 헬스체크 프로브(Probe) 및 정상 종료(Graceful Shutdown)를 관리하는 체계.
- **프로브 오설정 및 서비스 에러 위험(Probe Misconfiguration & 502 Bad Gateway)**: 애플리케이션의 내부 데드락과 외부 종속성 지연을 구분하지 못해 무한 재시작이 발생하거나 롤링 배포 중 502 에러가 발생하는 위험.

</details>

- 정의/개념: 쿠버네티스 파드의 생성부터 소멸까지의 **상태 전이(Phase)와 3대 프로브(Startup/Liveness/Readiness)를 관리**하는 생명주기 제어 메커니즘
- 배경/필요성: 컨테이너 프로세스 생존 여부만으로는 **초기 부팅 지연, 데드락 발생 및 트래픽 수용 준비 상태를 식별하지 못해 서비스 장애 초래 위험** 직면

#### 한줄 요약

- 파드의 단계별 상태 전이와 3대 프로브를 정밀 제어하여 무중단 배포와 안정적인 자가 치유를 보장

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3대 상태 점검(Probes)**: 초기 기동 완료를 기다리는 Startup Probe, 데드락 시 컨테이너를 재시작하는 Liveness Probe, 준비 미완료 시 트래픽을 차단하는 Readiness Probe.
- **정상 종료(Graceful Termination)**: `preStop` 훅 실행 $\to$ `SIGTERM` 전달 $\to$ 유예 기간 대기 $\to$ `SIGKILL` 강제 종료로 이어지는 안전한 커넥션 정리 절차.

</details>

- Pending $\to$ Running $\to$ Succeeded/Failed로 이어지는 **명확한 파드 상태 전이(Pod Phase)**
- 프로세스 기동, 생존, 트래픽 준비 상태를 독립적으로 감시하는 **3대 프로브(Probe) 체계**
- 롤링 업데이트 시 트래픽 유실을 방지하는 **preStop 훅 및 Graceful Shutdown 보장** #### 한줄 요약

- 프로브의 역할 분리와 정상 종료 절차를 통해 서비스 단절 없는 고가용성을 실현

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **파드 3대 프로브 점검 체계**: Startup Probe(초기 기동 보호), Liveness Probe(내부 결함 복구), Readiness Probe(서비스 엔드포인트 연동).

</details>

```text
[ 쿠버네티스 파드 3대 프로브 및 생명주기 구조도 ]

 1. [ 파드 기동 단계 (Startup Phase) ]
    [ Pod Pending ] ──► [ Init Containers ] ──► [ App Container Started ]
                                                         │
                                                         ▼
 2. [ 3대 프로브 감시 계층 (Kubelet Monitoring) ]
    ┌─────────────────────────────────────────────────────────────┐
    │ • Startup Probe: 대규모 JVM/Spring 초기 부팅 완료까지 대기 │
    │   (성공할 때까지 Liveness/Readiness 프로브 실행 보류)      │
    ├─────────────────────────────────────────────────────────────┤
    │ • Liveness Probe: 내부 Deadlock/무한루프 감지 ➔ [재시작]   │
    ├─────────────────────────────────────────────────────────────┤
    │ • Readiness Probe: 트래픽 수용 준비 여부 ➔ [Endpoint 등록] │
    └────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
 3. [ 서비스 트래픽 수용 (Running) ] ──► [ K8s Service / Ingress 유입 ]
```

선의 의미: kubelet이 3대 프로브를 순차적/병렬적으로 실행하여 컨테이너 상태를 제어하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 초기화 컨테이너 (Init) | 메인 앱 실행 전 **DB 마이그레이션, 설정 파일 다운로드 등 사전 작업 완료** |
| 스타트업 프로브 (Startup) | 무거운 애플리케이션의 **초기 기동 시간을 보장하여 불필요한 조기 재시작 차단** |
| 라이브니스 프로브 (Liveness) | 내부 데드락이나 무한 루프 발생 시 **컨테이너 프로세스를 강제 재시작하여 복구** |
| 레디니스 프로브 (Readiness) | 워밍업 미완료 시 **Service Endpoint IP에서 파드를 제외하여 503 에러 차단** |
| 프리엔드 훅 (preStop) | 파드 종료 전 **`sleep` 등을 수행하여 신규 트래픽 유입 차단 및 기존 세션 정리** |

#### 한줄 요약

- 초기화 컨테이너, 3대 프로브, preStop 훅이 결합하여 파드의 전 생명주기를 보호

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **파드 정상 종료 5단계 절차**: 삭제 요청 $\to$ Endpoint 제외 $\to$ preStop 훅 $\to$ SIGTERM 및 유예 $\to$ SIGKILL 종료.

</details>

```text
[ 쿠버네티스 파드 Graceful Shutdown 5단계 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. kubectl delete pod 종료 요청 수신   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Service Endpoints에서 파드 IP 제거  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 컨테이너 preStop 훅 (sleep 10s) 실행│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. SIGTERM 전달 및 유예 기간(30s) 대기 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 잔여 프로세스 SIGKILL 강제 종료 완료│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 종료 요청: 사용자의 삭제 또는 Deployment 롤링 배포로 인해 파드 삭제 이벤트가 발생.
2. Endpoint 제외: kube-proxy 및 Ingress 컨트롤러가 라우팅 테이블에서 해당 파드 IP를 즉시 제거.
3. preStop 실행: 네트워크 라우팅 갱신 지연을 고려하여 `sleep 10` 등의 preStop 훅을 실행해 안전 대기.
4. SIGTERM 전달: 메인 프로세스에 `SIGTERM`을 전송하여 진행 중이던 요청을 안전하게 마무리.
5. SIGKILL 종료: `terminationGracePeriodSeconds`(기본 30초) 초과 시 남은 프로세스를 `SIGKILL`로 강제 정리.

#### 한줄 요약

- 종료 요청 $\to$ Endpoint 제외 $\to$ preStop 훅 $\to$ SIGTERM 전달 $\to$ SIGKILL 종료의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Liveness vs Readiness vs Startup**: 점검 목적, 실패 시 조치, 적합 대상에 따른 3대 프로브 비교.

</details>

| 구분 | 스타트업 프로브 (Startup) | 라이브니스 프로브 (Liveness) | 레디니스 프로브 (Readiness) |
|:---|:---|:---|:---|
| **적용 기준** | 대규모 Spring/Java 등 부팅이 느린 앱 | 내부 데드락, 메모리 누수, 무한 루프 감지 | 캐시 워밍업 미완료, 외부 DB 일시 과부하 |
| **핵심 특징** | **초기 기동 완료 시까지 타 프로브 억제** | **실패 시 `docker restart` 컨테이너 재시작** | **실패 시 `Endpoints` 제외 (트래픽 차단)** |
| **한계** | 기동 완료 후에는 더 이상 동작하지 않음 | 외부 DB 일시 장애 시 전사 무한 재시작 위험 | 프로세스 자체 고장 시 자동 재시작 불가 |

#### 한줄 요약

- 부팅 보호는 Startup, 내부 고장 복구는 Liveness, 트래픽 안전 격리는 Readiness를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **연쇄 재시작 장애(Cascading Failure)**: 외부 DB 다운 시 Liveness Probe가 실패하도록 설정하여 클러스터 전체 파드가 동시에 무한 재시작에 빠지는 치명적 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 배포 롤링 업데이트 시 클라이언트에 간헐적 502 에러 발생 | **`preStop: sleep 10` 설정으로 Endpoint 제거 대기 시간 확보** | 무중단 롤링 배포 100% 달성 |
| 초기 부팅이 1분 이상 걸리는 앱의 빈번한 조기 재시작 | **`startupProbe` 도입 및 충분한 `failureThreshold` 부여** | 부팅 타임아웃 오류 완벽 차단 |
| 외부 DB 일시 장애 시 클러스터 전체 파드 무한 재시작 | **Liveness는 내부 헬스만 검사하고 DB 연동은 Readiness로 분리** | 연쇄 재시작 장애 원천 차단 |

#### 한줄 요약

- preStop sleep 훅, 스타트업 프로브 도입, Liveness/Readiness 분리를 통해 프로브 운영 장애를 방지

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **무중단 운영 표준(Zero-Downtime Standards)**: preStop 훅과 3대 프로브를 결합하여 단 한 건의 트랜잭션 유실도 없이 배포와 자가 치유를 수행하는 엔지니어링 규약.

</details>

- **쿠버네티스 파드 생명주기** 기반 컨테이너 가용성을 결정짓는 핵심 메커니즘이며, 내부 프로세스 고장은 Liveness로 복구하고 외부 트래픽 수용은 Readiness로 제어하는 프로브 분리 원칙을 준수해야 함

#### 한줄 요약

- 3대 프로브와 Graceful Shutdown을 정밀 설계하여 무중단 고가용성 서비스를 완성
