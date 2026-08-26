---
sidebar:
  order: 153
  label: "153. 쿠버네티스 Pod 생명주기"
  badge:
    text: "기출 · 30%"
    variant: note
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-08-26T09:59:00+09:00"
tags:
  - "notes-software"
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

- **Pod 생명주기(Pod Lifecycle)**: 파드의 상태 전이(Pending $\to$ Running $\to$ Succeeded/Failed)와 3대 헬스체크 프로브 및 Graceful Shutdown 제어 체계.
- **3대 프로브(Startup / Liveness / Readiness)**: 초기 부팅 보호(Startup), 데드락 복구(Liveness), 트래픽 격리(Readiness).

</details>

- 정의/개념: 쿠버네티스 파드의 생성부터 소멸까지의 **상태 전이(Phase)와 3대 프로브 및 Graceful Shutdown을 제어하는 생명주기 관리 메커니즘**
- 배경/필요성: 단순 프로세스 생존 검사만으로는 **초기 부팅 지연 감지 불가, 데드락 무한 방치 및 롤링 배포 시 502 에러 발생 해결 불가**

#### 한줄 요약
- 3대 프로브와 Graceful Shutdown을 통해 무중단 배포와 안정적인 자가 치유를 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Graceful Shutdown**: 파드 삭제 시 `preStop` 훅 실행 $\to$ `SIGTERM` 전송 $\to$ 유예 기간 대기 $\to$ `SIGKILL` 강제 종료 순으로 커넥션을 안전하게 정리.
- **Init Container**: 메인 애플리케이션 컨테이너 실행 전 DB 마이그레이션이나 사전 설정을 1회성으로 완수하는 초기화 컨테이너.

</details>

- Pending $\to$ Running $\to$ Succeeded/Failed로 이어지는 **명확한 파드 상태 전이(Pod Phase)**
- 프로세스 기동, 생존, 트래픽 준비 상태를 독립 감시하는 **3대 프로브(Probe) 체계**
- 롤링 업데이트 시 트래픽 유실을 방지하는 **preStop 훅 및 Graceful Shutdown**

#### 한줄 요약
- 상태 전이 관리, 3대 프로브 분리, Graceful Shutdown을 통해 서비스 연속성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Pod 생명주기 3대 감시 구조**: Init Phase(초기화 컨테이너), Probe Monitoring(Startup/Liveness/Readiness), Traffic Routing(Service/Endpoints).

</details>

```text
[쿠버네티스 파드 생명주기 및 3대 프로브 아키텍처]
|-- 1. Pod Initialization Phase (파드 초기화 단계)
|   `-- [Pending] -> [Init Containers (DB 마이그레이션)] -> [App Container Started]
|-- 2. Kubelet Probe Monitoring Layer (3대 프로브 감시 계층)
|   |-- Startup Probe (초기 부팅 완료 시까지 Liveness/Readiness 실행 보류)
|   |-- Liveness Probe (데드락/무한루프 감지 시 -> 컨테이너 프로세스 자동 재시작)
|   `-- Readiness Probe (트래픽 수용 준비 판정 -> K8s Service Endpoints 등록/제외)
`-- 3. Traffic Routing Layer (Running 상태 도달 시 Service / Ingress 트래픽 유입)
```

선의 의미: 계층 및 kubelet이 3대 프로브를 순차적/병렬적으로 실행하여 컨테이너 상태를 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 초기화 컨테이너 (Init) | 메인 앱 실행 전 **DB 마이그레이션, 설정 파일 다운로드 등 사전 작업 완료** | 순차 실행 후 종료 |
| 스타트업 프로브 (Startup) | 무거운 애플리케이션의 **초기 기동 시간을 보장하여 불필요한 조기 재시작 차단** | 부팅 완료 시 비활성 |
| 라이브니스 프로브 (Liveness) | 내부 데드락이나 무한 루프 발생 시 **컨테이너 프로세스를 강제 재시작하여 복구** | 실패 시 Container Restart |
| 레디니스 프로브 (Readiness) | 워밍업 미완료 시 **Service Endpoint IP에서 파드를 제외하여 503 에러 차단** | 실패 시 트래픽 격리 |
| 프리엔드 훅 (preStop) | 파드 종료 전 **`sleep` 등을 수행하여 신규 트래픽 유입 차단 및 기존 세션 정리** | Graceful Shutdown 보조 |

#### 한줄 요약
- 초기화 컨테이너, 3대 프로브, preStop 훅이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Graceful Shutdown 5단계**: 삭제 요청 $\to$ Endpoints 제외 $\to$ preStop 훅 실행 $\to$ SIGTERM 전달 및 유예 $\to$ SIGKILL 종료.

</details>

```text
Deployment 롤링 배포 또는 파드 삭제 요청 수신
        │
   [종료 이벤트 수신] API 서버가 파드 상태를 Terminating으로 전환
        │
   [Endpoints IP 제거] kube-proxy 및 Ingress 컨트롤러가 라우팅 테이블에서 파드 IP 제외
        │
   [preStop 훅 실행] 네트워크 갱신 지연을 고려하여 `sleep 10` 훅을 실행해 안전 대기
        │
   [SIGTERM 전달] 메인 프로세스에 SIGTERM을 전송하여 처리 중이던 세션 정상 완료 유도
        │
   `terminationGracePeriodSeconds`(기본 30초) 초과 시 SIGKILL로 잔여 프로세스 강제 정리
```

#### 한줄 요약
- 종료 요청 → Endpoints 제외 → preStop 훅 → SIGTERM 전달 → SIGKILL 종료 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Startup vs Liveness vs Readiness**: 부팅 완료 보호(Startup), 고장 자동 재시작(Liveness), 트래픽 수용 판정(Readiness).

</details>

| 비교 항목 | 스타트업 프로브 (Startup) | 라이브니스 프로브 (Liveness) | 레디니스 프로브 (Readiness) |
|:---|:---|:---|:---|
| 점검 목적 | **초기 기동 완료 여부 감시** | **내부 데드락 및 고장 프로세스 감지** | **외부 트래픽 수용 준비 여부 감시** |
| 실패 시 조치 | 실패 지속 시 컨테이너 재시작 | **`docker restart` 컨테이너 강제 재시작** | **`Endpoints`에서 파드 IP 제거 (트래픽 차단)** |
| 적합 대상 | **Spring/Java 등 무거운 부팅 앱** | **내부 무한 루프, 스레드 데드락** | **캐시 워밍업, 외부 DB 일시 과부하** |
| 타 프로브 영향 | 성공 전까지 타 프로브 실행 보류 | Startup 성공 후 주기적 독립 실행 | Startup 성공 후 주기적 독립 실행 |

#### 한줄 요약
- 부팅 보호는 Startup, 내부 고장 복구는 Liveness, 트래픽 안전 격리는 Readiness를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cascading Restart Failure**: 외부 DB 다운 시 Liveness Probe가 실패하도록 설정하여 클러스터 전체 파드가 동시에 무한 재시작에 빠지는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 배포 롤링 업데이트 시 클라이언트에 간헐적 502 에러 발생 | **`preStop: sleep 10` 설정으로 Endpoint 제거 대기 시간 확보** | 무중단 롤링 배포 100% 달성 |
| 초기 부팅이 1분 이상 걸리는 앱의 빈번한 조기 재시작 | **`startupProbe` 도입 및 충분한 `failureThreshold` 부여** | 부팅 타임아웃 오류 완벽 차단 |
| 외부 DB 일시 장애 시 클러스터 전체 파드 무한 재시작 | **Liveness는 내부 헬스만 검사하고 DB 연동은 Readiness로 분리** | 연쇄 재시작 장애 원천 차단 |
| 장기 트랜잭션 도중 파드가 30초 만에 강제 종료 | **`terminationGracePeriodSeconds: 60`으로 유예 시간 연장** | 진행 중인 트랜잭션 무손실 완수 |

#### 한줄 요약
- preStop sleep 훅, 스타트업 프로브 도입, Liveness/Readiness 분리, 유예 시간 연장으로 운영한다.

## Ⅶ. 결론

- 프로세스 복구는 **Liveness**, 트래픽 격리는 **Readiness** 선택

#### 한줄 요약
- 파드 생명주기 관리는 3대 프로브와 정상 종료 절차를 정밀 제어하여 무중단 배포와 안정적 자가 치유를 실현하는 쿠버네티스의 핵심 운영 기술이다.