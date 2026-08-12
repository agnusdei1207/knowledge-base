---
sidebar:
  order: 153
  label: "153. 쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Pod Lifecycle (파드 생명주기)**: K8s Pod가 생성(Pending)되어 노드에 배치(Running), 정상 종료(Succeeded) 또는 실패(Failed)로 끝나는 전체 상태 전이(State Transition) 단계 및 프로브(Probe) 헬스체크 프로세스.
- **Probe (Health Check Probes)**: kubelet이 Pod 내부 컨테이너의 생존 여부 및 트래픽 서빙 준비 상태를 주동적으로 체크하는 3대 헬스체크 기법 (Liveness, Readiness, Startup Probe).
- **Graceful Termination (정상 종료)**: Pod가 삭제될 때 `preStop` 훅과 `SIGTERM` 신호를 수신받아 기존 연결을 안전하게 정리(Drain)하고 종료하는 메커니즘.

</details>

- 정의/개념: Pod의 5대 상태 Phase(Pending $\rightarrow$ Running $\rightarrow$ Succeeded/Failed/Unknown) 전이 및 3대 Probes 헬스체크를 통해 무중단 트래픽 차단과 자가 치유를 도모하는 관리 체계인 **Pod Lifecycle**
- 배경/필요성: 앱 부팅이 안 끝났는데 트래픽이 유입되어 502 Bad Gateway가 터지거나, Deadlock 걸린 컨테이너가 멈춘 채 방치되는 파행 예방 요구성

#### 한줄 요약

- 프로그램이 켜진 상태와 손님을 받을 준비가 된 상태는 다르므로 파드는 실행, 생존, 준비 여부를 서로 다른 신호로 표현한다.

## Ⅱ. 특징 (Pod 5대 Phase 및 3대 Probes)

<details><summary>핵심 용어</summary>

- **Liveness vs Readiness**: Liveness는 고장 시 컨테이너 재시작, Readiness는 미준비 시 Service 엔드포인트 트래픽 차단.

</details>

- **5 Pod Phase Transition (Pending $\rightarrow$ Running $\rightarrow$ Succeeded / Failed / Unknown)**
- **3 Health Check Probes (Startup Probe, Liveness Probe, Readiness Probe)**
- **Graceful Shutdown Guarantee (preStop Hook $\rightarrow$ SIGTERM $\rightarrow$ TerminationGracePeriodSeconds 30s $\rightarrow$ SIGKILL)**

#### 한줄 요약

- 시작이 늦은 상황, 멈춘 상황, 잠시 요청을 받지 못하는 상황을 구분해야 불필요한 재시작과 서비스 단절을 줄일 수 있다.

## Ⅲ. 구조 및 구성요소 (Pod 3대 Probes 및 5대 Phase 상세)

<details><summary>핵심 용어</summary>

- **Startup Probe**: Java/Spring 애플리케이션처럼 부팅에 2분이 걸리는 앱의 초기 부팅 완료 여부를 기다려 주는 전용 헬스체크.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      Pod 3-Probe Health Check Architecture             │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Startup Probe   ──► Boots App Complete? ──► YES ──► (Disables itself)│
│                                                                        │
│ 2. Liveness Probe  ──► Is App Alive?       ──► NO  ──► Container Restart│
│                                                                        │
│ 3. Readiness Probe ──► Ready for Traffic?  ──► NO  ──► Cut Service Endpoint│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 3가지 프로브가 각자 다른 관점에서 컨테이너의 기동, 생존, 트래픽 유입 준비를 독자적으로 제어하는 아키텍처.

| 구분 지표 | 1. Startup Probe | 2. Liveness Probe | 3. Readiness Probe |
|:---|:---|:---|:---|
| **핵심 목적** | **느린 부팅 앱 초기 완료 체크** | **Deadlock/Hang 컨테이너 생존 체크**| **실제 HTTP 트래픽 서빙 가능 체크** |
| **실패 시 뚝 끊김 결과**| **컨테이너 재시작 (Restart)** | **컨테이너 즉시 재시작 (Restart)** | **Service K8s Endpoint 에서 뺌 (No Traffic)** |
| **적용 시점** | Pod 생성 직후 (1회성 유예) | Startup 성공 후 무한 반복 | Startup 성공 후 무한 반복 |
| **대표 유스케이스**| **Spring Boot, Heavy Java App**| **Infinite Loop, Deadlock 예방** | **DB 커넥션 웜업, 캐시 로딩 완료** |

#### 한줄 요약

- kubelet이 현장 관리자라면 초기화 컨테이너는 개점 준비, 프로브는 안전·영업 검사, 종료 제어는 폐점 정리 절차에 해당한다.

## Ⅳ. 흐름도 (Graceful Termination 5단계 셧다운 흐름)

<details><summary>핵심 용어</summary>

- **preStop Hook**: `kubectl delete pod` 수신 시 SIGTERM 전달 직전, Nginx 릴로딩이나 K8s Service Endpoint 맵핑 제거 시간을 벌어주는 스크립트 훅.

</details>

```text
[kubectl delete pod] ──► [Service Endpoint Removal & preStop Hook Exec (sleep 10)]
                                                   │
                                                   ▼
 [SIGKILL (Force Kill)] ◄── [TerminationGracePeriod (30s Expiry)] ◄── [SIGTERM Signal]
```

### 동작 원리

1. **Endpoint Detach & preStop**: delete 명령 수신 즉시 K8s Service Endpoint에서 Pod IP를 제거하여 신규 트래픽 유입 차단 후 preStop 훅 실행.
2. **SIGTERM & Grace Period**: 프로세스에 `SIGTERM` 신호를 보내 처리 중인 기존 커넥션 마무리 유예(기본 30초).
3. **SIGKILL**: 30초 경과 후에도 종료 안 되면 `SIGKILL`로 강제 파기 (**Graceful Termination 완결**).

#### 한줄 요약

- 파드가 시작되면 kubelet은 세 가지 검사를 반복하고, 준비 검사 결과만 서비스에 반영해 요청 차단과 프로세스 재시작을 분리한다.

## Ⅴ. 종류 및 비교 (Liveness vs Readiness Probe 1:1 비교)

<details><summary>핵심 용어</summary>

- **Cascade Restart Danger**: DB장애로 Readiness 대신 Liveness를 잘못 걸면, 전사 컨테이너가 무한 재시작(Cascade Fail)되는 안티패턴.

</details>

| 비교 항목 | Liveness Probe (생존 프로브) | Readiness Probe (준비 프로브) |
|:---|:---|:---|
| **검사 실패 원인** | 프로세스 다운, Deadlock, 무한 루프 | DB 커넥션 풀 차오름, 캐시 웜업 미완료 |
| **K8s 조치 행위** | **`docker restart` (컨테이너 강제 재시작)**| **Service Endpoint IP 제거 (트래픽 유입 차단)**|
| **장애 복구 효과** | 프로세스 재기동으로 데드락 해제 | **사용자에게 502/503 에러 표출 차단** |
| **안티패턴 오용** | **외부 DB 접속 실패 시 Liveness 걸면 안 됨**| 외부 DB 연결 체크용으로 적극 활용 |

#### 한줄 요약

- 시작 검사는 기다릴 시간을, 활성 검사는 다시 켤 조건을, 준비 검사는 요청을 보낼 조건을 각각 결정한다.

## Ⅵ. 실무 고려사항 및 대책 (Pod Lifecycle 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **502 Bad Gateway on Deployment**: Deploy rolling update 시 preStop 훅(sleep 10s)이 없어서 K8s Endpoint가 지워지기도 전에 Pod가 꺼져 502 터지는 현상.

</details>

| 3대 Lifecycle 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Rolling Update 502 Error**| Endpoint 제거와 Pod 파기 시점 안 맞음| **`preStop: exec: command: ["sleep", "15"]` 배치**|
| **2. Infinite Spring Boot Loop**| Java 부팅 2분 걸리는데 Liveness 30초 컷| **Startup Probe 도입으로 부팅 완료 시까지 유예**|
| **3. Database Cascading Crash** | DB 다운으로 Liveness 실패해 전 Pod 재시작| **외부 DB 체크는 Liveness 배제하고 Readiness 전용**|

> 사례: **카카오 / 당근마켓 / 쿠팡 preStop sleep 훅 및 3대 Probes 무중단 배포 적용**

#### 한줄 요약

- 데이터베이스가 잠시 느리다는 이유로 모든 컨테이너를 재시작하지 않도록 활성 검사는 내부 고장만 보고 준비 검사로 트래픽부터 걷어 내야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Pod Lifecycle 수립 기준(Pod Lifecycle Standards)**: 3대 Probes(Startup/Liveness/Readiness), preStop sleep 15s 훅 및 Graceful Termination 30s에 의거한 체계.

</details>

- **Pod Lifecycle 수립 기준**에 따라 무중단 클라우드 네이티브 배포 구축 시 **3-Probes & preStop Graceful Hook** 필수 적용

#### 한줄 요약

- 느린 시작은 기다리고 내부 정지는 재시작하며 외부 의존 장애는 요청만 차단하는 기준으로 파드 생명주기를 설계해야 한다.
