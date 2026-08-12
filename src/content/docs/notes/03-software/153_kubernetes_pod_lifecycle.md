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

- **파드 생명주기(Pod Lifecycle)**: 파드의 생성(Pending)부터 실행(Running), 종료(Succeeded/Failed)까지의 상태 전이 단계와 상태 점검(Probe) 절차.
- **프로브(Probe)**: kubelet이 파드 내 컨테이너의 생존 여부와 트래픽 서빙 준비 상태를 주기적으로 점검하는 3대 메커니즘(Liveness, Readiness, Startup).
- **정상 종료(Graceful Termination)**: 파드 삭제 시 `preStop` 훅과 `SIGTERM` 신호를 통해 연결을 안전하게 정리(Drain) 후 종료하는 절차.

</details>

- 정의: 파드의 5대 상태 전이와 3대 프로브 점검을 통해 무중단 서비스와 자동 장애 복구를 수행하는 관리 체계.
- 배경: 서비스 준비 전 트래픽 유입으로 인한 오류 발생이나 응답 불능 컨테이너 방치 등 파행 상황 예방 요구.

#### 한줄 요약

- 프로그램이 켜진 상태와 손님을 받을 준비가 된 상태는 다르므로 파드는 실행, 생존, 준비 여부를 서로 다른 신호로 표현한다.

## Ⅱ. 특징 (Pod 5대 Phase 및 3대 Probes)

<details><summary>핵심 용어</summary>

- **Liveness vs Readiness**: Liveness는 고장 시 컨테이너 재시작, Readiness는 미준비 시 Service 엔드포인트 트래픽 차단.

</details>

- **5대 상태 전이**: Pending → Running → Succeeded/Failed/Unknown.
- **3대 상태 점검(Probes)**: Startup, Liveness, Readiness.
- **정상 종료 보장**: preStop 훅 → SIGTERM → 종료 유예 기간 → SIGKILL 강제 종료.

#### 한줄 요약

- 시작이 늦은 상황, 멈춘 상황, 잠시 요청을 받지 못하는 상황을 구분해야 불필요한 재시작과 서비스 단절을 줄일 수 있다.

## Ⅲ. 구조 및 구성요소 (Pod 3대 Probes 및 5대 Phase 상세)

<details><summary>핵심 용어</summary>

- **Startup Probe**: Java/Spring 애플리케이션처럼 부팅에 2분이 걸리는 앱의 초기 부팅 완료 여부를 기다려 주는 전용 헬스체크.

</details>

```text
┌────────────────────────────────────────┬──────────────────────────────────────────┐
│           3대 프로브 점검 기능          │             기능 및 결과                │
├────────────────────────────────────────┼──────────────────────────────────────────┤
│ 1. Startup Probe   ──► 부팅 완료 점검   │ 완료 시 다음 프로브 작동                 │
│ 2. Liveness Probe  ──► 생존 점검        │ 실패 시 컨테이너 재시작                  │
│ 3. Readiness Probe ──► 준비 점검        │ 실패 시 트래픽 유입 차단                 │
└────────────────────────────────────────┴──────────────────────────────────────────┘
```

선의 의미: 3가지 프로브가 각자 다른 관점에서 컨테이너의 기동, 생존, 트래픽 유입 준비를 독자적으로 제어하는 아키텍처.

| 구분 | Startup Probe | Liveness Probe | Readiness Probe |
|:---|:---|:---|:---|
| **목적** | 초기 부팅 완료 체크 | 생존(Deadlock) 체크 | 트래픽 서빙 가능 체크 |
| **실패 결과**| 컨테이너 재시작 | 컨테이너 재시작 | 엔드포인트에서 제외(트래픽 차단) |
| **적용 시점** | 생성 직후 (유예) | 부팅 성공 후 | 부팅 성공 후 |
| **사례** | Java/Spring 앱 | 무한 루프, 데드락 | DB 연결, 캐시 로딩 |

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

| 3대 난제 | 원인 | 실무 대책 |
|:---|:---|:---|
| **1. Rolling Update 502**| 종료 전 트래픽 유입 | `preStop` sleep 훅 배치 |
| **2. 부팅 타임아웃** | 느린 부팅 시 재시작 | Startup Probe 도입 |
| **3. DB 연동 장애** | DB 다운 시 전체 재시작 | Liveness 배제 및 Readiness 사용 |

> 사례: **카카오 / 당근마켓 / 쿠팡 preStop sleep 훅 및 3대 Probes 무중단 배포 적용**

#### 한줄 요약

- 데이터베이스가 잠시 느리다는 이유로 모든 컨테이너를 재시작하지 않도록 활성 검사는 내부 고장만 보고 준비 검사로 트래픽부터 걷어 내야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Pod Lifecycle 수립 기준(Pod Lifecycle Standards)**: 3대 Probes(Startup/Liveness/Readiness), preStop sleep 15s 훅 및 Graceful Termination 30s에 의거한 체계.

</details>

- **파드 생명주기 수립 기준**에 따라 무중단 배포 구축 시 **3대 프로브 및 preStop 훅** 필수 적용.

#### 한줄 요약

- 느린 시작은 기다리고 내부 정지는 재시작하며 외부 의존 장애는 요청만 차단하는 기준으로 파드 생명주기를 설계해야 한다.
