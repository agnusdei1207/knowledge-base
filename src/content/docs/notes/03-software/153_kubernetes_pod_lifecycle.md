---
sidebar:
  order: 153
  label: "153. 쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-08-14T02:04:00+09:00"
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

- **파드 생명주기(Pod Lifecycle)**: 파드(Pod)의 생성부터 종료까지 상태 전이 단계 및 상태 점검(Probe)을 관리하는 절차.
- **프로브(Probe)**: 큐블릿(Kubelet)이 컨테이너의 생존(Liveness), 준비(Readiness), 기동(Startup) 상태를 주기적으로 확인하는 메커니즘.
- **정상 종료(Graceful Termination)**: 파드 삭제 요청 시 `preStop` 훅(Hook)과 `SIGTERM` 신호를 통해 기존 연결을 안전하게 정리(Drain)한 후 프로세스를 종료하는 절차.

</details>

- 정의/개념: Pod 생성•실행•종료 상태와 Probe의 **Pod Lifecycle**
- 배경/필요성: 실행 여부만으로는 **기동•생존•서비스 준비** 구분 불가

#### 한줄 요약

- 프로그램이 켜진 상태와 손님을 받을 준비가 된 상태는 다르므로 파드는 실행, 생존, 준비 여부를 서로 다른 신호로 표현한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **생존 vs 준비 프로브(Liveness vs Readiness Probe)**: Liveness Probe는 고장 시 컨테이너를 재시작하여 정상 상태 회복, Readiness Probe는 미준비 상태 시 서비스 엔드포인트에서 제외하여 트래픽 유입 차단.

</details>

- **5대 상태 전이**: Pending → Running → Succeeded/Failed/Unknown.
- **3대 상태 점검(Probes)**: Startup, Liveness, Readiness.
- **정상 종료 보장**: preStop 훅(Hook) → SIGTERM → 종료 유예 기간 → SIGKILL 강제 종료.

#### 한줄 요약

- 시작이 늦은 상황, 멈춘 상황, 잠시 요청을 받지 못하는 상황을 구분해야 불필요한 재시작과 서비스 단절을 줄일 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Startup Probe**: Java/Spring 애플리케이션처럼 부팅에 2분이 걸리는 앱의 초기 부팅 완료 여부를 기다려 주는 전용 헬스체크.

</details>

```text
[Pod 상태 점검]
 ├── [Startup Probe]
 ├── [Liveness Probe]
 └── [Readiness Probe]
```

| 구성요소 | 책임 |
|---|---|
| Startup Probe | 느린 기동 중 **조기 재시작** 방지 |
| Liveness Probe | 복구 불가 내부 정지 시 **Container 재시작** |
| Readiness Probe | 미준비 Pod를 **Service Endpoint**에서 제외 |

#### 한줄 요약

- kubelet이 현장 관리자라면 초기화 컨테이너는 개점 준비, 프로브는 안전·영업 검사, 종료 제어는 폐점 정리 절차에 해당한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **preStop 훅(preStop Hook)**: `kubectl delete pod` 신호 수신 시 SIGTERM 전달 직전, 트래픽 차단 및 세션 정리를 위해 수행하는 스크립트 훅.

</details>

```text
[Pod 종료 요청]
      │
      ▼
1. 종료 상태 전환
      │
      ▼
2. Endpoint 제외
      │
      ▼
3. preStop Hook 실행
      │
      ▼
4. SIGTERM•유예
      │
      ▼
5. 잔여 Process 종료
      │
      ▼
[Pod 삭제 완료]
```

### 동작 원리

1. **종료 상태 전환**: Kubelet이 Pod 종료 절차 인지
2. **Endpoint 제외**: 신규 Traffic 전달 대상에서 제거
3. **preStop Hook 실행**: Application별 사전 정리 수행
4. **SIGTERM•유예**: 연결•작업 종료 시간을 제공
5. **잔여 Process 종료**: 유예 후 남은 Process 강제 종료

#### 한줄 요약

- 파드가 시작되면 kubelet은 세 가지 검사를 반복하고, 준비 검사 결과만 서비스에 반영해 요청 차단과 프로세스 재시작을 분리한다.

## Ⅴ. 종류 및 비교

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

## Ⅵ. 실무 고려사항 및 대책

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

- 내부 정지는 **Liveness**, 외부 의존 장애는 Readiness로 분리

#### 한줄 요약

- 다시 켜야 할 고장과 요청만 멈춰야 할 미준비 상태를 서로 다른 Probe로 처리한다.
