---
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 174
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes Pod 생명주기를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Pod 생명주기는 쿠버네티스의 최소 배포 단위인 **Pod**가 생성부터 소멸까지 거치는 **상태 전이(Phase)**와, 그 위에서 트래픽 수신 가능 여부를 판정하는 **Probe** 체계를 함께 부르는 말이다.
- **왜 필요한가**: 컨테이너가 "시작된 시점"과 "실제로 요청을 받아도 되는 시점"은 다르다. 이 둘을 구분하지 않으면 배포 중이나 장애 복구 중에 아직 준비 안 된 Pod로 트래픽이 들어가 오류가 발생한다.
- **핵심 직관**: Pod는 태어나서(Pending) 자리를 잡고(Running) 스스로 "영업 준비 완료"를 알린 뒤(Ready)에만 손님(트래픽)을 받고, 문 닫을 때는 정리 시간을 갖고(Terminating) 사라지는 실행 생명체다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Pod | 하나 이상의 컨테이너를 묶어 함께 스케줄링·실행하는 쿠버네티스 최소 배포 단위 — 이 개념이 속한 **상위 개념** | 한 방에 같이 사는 룸메이트들 |
| Phase | Pod의 대분류 상태(Pending·Running·Succeeded·Failed·Unknown) | 신호등의 큰 색 구분 |
| Condition | Phase보다 세밀한 상태 플래그(PodScheduled·Initialized·ContainersReady·Ready) | 체크리스트의 개별 항목 |
| Ready Condition | Service가 이 Pod로 트래픽을 보내도 되는지 판단하는 최종 기준 | "영업 준비 완료" 표시등 |
| startupProbe | 느린 초기 부팅 시간을 봐주는 점검 — 성공 전까지는 readiness·liveness 점검을 유예 | 신입사원 수습기간 |
| readinessProbe | 트래픽 받을 준비가 됐는지 점검 — 실패하면 재시작이 아니라 Endpoint에서만 제외 | 손님 받을 준비가 됐는지 확인 |
| livenessProbe | 컨테이너가 정상 동작 중인지(살아있는지) 점검 — 실패하면 kubelet이 컨테이너를 재시작 | 맥박 체크 |
| restartPolicy | 컨테이너 종료 시 재시작 여부·조건(Always·OnFailure·Never) | 재도전 규칙 |
| terminationGracePeriodSeconds | SIGTERM 전달 후 SIGKILL 강제종료까지 주는 유예 시간(기본 30초) | 퇴근 인수인계 시간 |
| preStop hook | SIGTERM 직전에 실행되는 종료 준비 작업(예: LB에서 빠질 시간 벌기) | 퇴근 전 마지막 정리 |
| CrashLoopBackOff | 재시작이 반복 실패할 때 재시도 간격을 지수적으로 늘리는 상태 | 계속 실패하는 문 앞에서 점점 오래 기다렸다 두드리기 |

## 깊이 이해

### 왜 Phase와 Ready를 구분하나 (배경)
- Kubernetes는 컨테이너가 아니라 Pod를 스케줄링 단위로 다룬다(사이드카처럼 네트워크·스토리지를 공유하는 컨테이너 묶음을 하나로 배치해야 하기 때문). 문제는 "컨테이너 프로세스가 시작됨(Running)"과 "이 Pod가 실제 요청을 처리할 준비가 됨(Ready)" 사이에 시간차가 있다는 점이다. 이 둘을 하나로 취급하면 DB 커넥션도 안 맺은 Pod로 트래픽이 몰려 500 에러가 난다.

### Phase 흐름 — 수치로 이해
- Pending: 스케줄링 결정 + 이미지 다운로드가 일어나는 구간. 예를 들어 이미지 크기가 500MB면 캐시가 없는 노드에서는 pull에만 수십 초가 걸릴 수 있어, 이 시간 동안 Pod는 계속 Pending으로 남는다.
- Running: 컨테이너 프로세스가 시작된 상태. 하지만 아직 Ready는 아닐 수 있다(예: 스프링 부트 앱이 기동 후 초기화에 15초를 더 쓴다면, 그 15초 동안 Running이지만 Ready는 false).
- Succeeded/Failed: 1회성 Job처럼 종료를 전제로 한 Pod의 최종 상태. 계속 떠 있어야 하는 Deployment의 Pod는 정상 동작 중이면 Running에 머문다.

### Probe 파라미터로 판정 원리 이해하기
- 각 probe는 initialDelaySeconds(첫 점검까지 대기)·periodSeconds(점검 주기)·timeoutSeconds(응답 대기 한도)·failureThreshold(연속 실패 허용 횟수)로 판정 시점을 조절한다.
- 예: periodSeconds=10, failureThreshold=3이면 10초마다 점검하다 3회 연속 실패해야 "실패"로 확정되므로, 최대 30초의 감지 지연이 생긴다. 이 지연 동안 readinessProbe라면 계속 트래픽이 들어가고, livenessProbe라면 아직 재시작되지 않는다.
- readinessProbe가 `/health/ready` 경로에서 200을 반환하기 전까지는 Service의 Endpoint 목록에 이 Pod가 등록되지 않아, 트래픽이 아예 도달하지 않는다.

### 종료 시퀀스 — 워크드 예제 (grace period 30초 vs 정리 시간 35초)
1. Pod 삭제 요청이 오면 Pod는 즉시 Terminating 상태가 되고, **동시에** Service의 Endpoint 목록에서 제외된다(이 시점부터 새 트래픽이 안 들어옴).
2. preStop hook이 실행된다(예: 5초 sleep — 로드밸런서가 Endpoint 변경을 반영할 시간을 벌기 위함).
3. 컨테이너에 SIGTERM이 전달되고, 애플리케이션은 진행 중인 요청을 마무리한다.
4. terminationGracePeriodSeconds(기본 30초)가 지나도 프로세스가 안 끝나면 SIGKILL로 강제 종료된다.
- 만약 preStop 5초 + 요청 마무리에 실제로 35초가 걸리는데 grace period가 기본값 30초라면, 5초분의 처리 중 요청이 SIGKILL로 강제 종료돼 유실된다. 이런 서비스는 grace period를 60초처럼 여유 있게 늘려야 한다.

### 재시작 백오프 — CrashLoopBackOff 수치
- livenessProbe 실패나 프로세스 크래시로 재시작이 반복되면, kubelet은 재시도 간격을 10초 → 20초 → 40초 → … 최대 5분까지 지수적으로 늘린다. 짧은 시간에 재시작이 반복될수록 복구까지 더 오래 걸리게 만들어 장애 컨테이너가 시스템을 계속 두드리는 것을 막는 장치다.

### 비유
- 매장 직원이 출근(Pending) → 업무 준비(Running이지만 아직 Ready 아님) → "영업 준비 완료" 표시(Ready, 손님 응대 시작) → 정기 건강 점검(liveness) → 퇴근 인수인계(preStop) → 퇴근(Terminated) 절차를 거치는 것과 같다.

### 흔한 오해·주의점
- Running은 트래픽을 받아도 되는 상태가 아니다. Service가 트래픽을 보낼지는 오직 Ready Condition과 Endpoint 반영 여부로 판단해야 한다.

## 연결 개념
- 쿠버네티스 아키텍처(173) — kubelet이 이 Phase 전이를 실행·보고하는 주체
- Pod 스케줄링(175) — Pending 단계에서 Scheduler가 Node를 결정하는 과정
- Service/Ingress(176) — Ready Pod만 Endpoint에 등록돼 실제 트래픽 대상이 되는 연결점

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Pod 생명주기 답안은 상태명 암기가 아니라 probe와 종료 처리로 트래픽 유입 시점을 통제하는 운영 설계로 작성해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pod 생명주기는 Pending, Running, Succeeded/Failed와 Ready condition으로 표현되는 실행 상태 흐름임.
> 2. **가치**: readiness, liveness, startup probe와 graceful termination으로 배포 중 장애 전파를 줄임.
> 3. **판단 포인트**: 트래픽 수신은 Running이 아니라 Ready 조건, 재시작은 restartPolicy와 probe 결과로 판단함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Pod 상태 전이 이해 확인 | Pending, Running, Succeeded, Failed, Unknown | 상태명만 나열 |
| 무중단 배포 판단 확인 | readinessProbe, preStop, grace period | Running과 Ready 혼동 |
| 장애 대응 설계 확인 | livenessProbe, restartPolicy, CrashLoopBackOff | probe 오설정 리스크 누락 |

> 요약: 생명주기 문제는 상태 전이와 트래픽 통제 조건을 연결해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Pod 생명주기는 Pod 실행 상태 변화 체계임.
- 배경: Kubernetes 배포에서는 컨테이너가 시작된 시점과 서비스 트래픽을 받을 수 있는 시점이 다르다.
- 필요성: Pending, Running, Ready, Terminating 상태 기준으로 롤링 업데이트, 장애 복구, 종료 처리를 설계한다.

---

## Ⅱ. 구조 및 구성요소

```text
PodSpec -> Scheduler -> Node/kubelet -> Container Runtime -> Pod Status
  / Conditions: PodScheduled, Initialized, Ready
  / Probes: startup, readiness, liveness
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Pod Phase | Pending, Running, Succeeded, Failed, Unknown | 전체 상태 |
| Conditions | Ready, ContainersReady 등 세부 조건 | Service endpoint 판단 |
| Probe | startup/readiness/liveness 점검 | HTTP, TCP, exec |
| Termination | SIGTERM, preStop, grace period | 기본 30초 |

> 요약: Pod 생명주기는 phase, condition, probe, termination이 결합되어 서비스 가능 상태를 결정함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> Pending -> 스케줄링/이미지 pull -> Running -> Ready -> 종료 요청 -> Terminating
  / readiness 실패 -> endpoint 제외
  / liveness 실패 -> 컨테이너 재시작
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API Server에 PodSpec 저장 | PodScheduled false/true |
| 2 | Scheduler가 Node 선택 | assigned node 존재 |
| 3 | kubelet이 이미지 pull과 컨테이너 시작 | Running phase |
| 4 | readinessProbe 성공 후 endpoint 등록 | Ready true |
| 5 | 종료 시 preStop, SIGTERM, grace 처리 | 5xx 증가 0건 |

> 요약: Pod는 생성, 배치, 실행, 준비, 종료를 거치며 Ready 조건이 트래픽 유입의 기준임.

---

## Ⅳ. 특징

| 구분 | 단순 프로세스 실행 | Pod 생명주기 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 시작 | 프로세스 start | Pending, pull, startupProbe | startup timeout |
| 트래픽 | 포트 open 즉시 | readiness true 후 endpoint 등록 | 5xx 0건 목표 |
| 장애 | 프로세스 종료 | liveness 실패 후 restart | CrashLoopBackOff |
| 종료 | kill 처리 | preStop, grace period | 30~120초 설정 |

> 요약: Kubernetes는 프로세스 실행보다 준비 상태와 종료 절차를 세밀하게 통제함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서버 프로세스 감시 | Pod phase/condition 관리 | 서비스 endpoint 필요 |
| 비용/처리 | 수동 재기동 | kubelet 자동 재시작 | 장애 감지 30초 이하 |
| 운영/위험 | 강제 종료 | graceful termination | in-flight request 존재 |

> 요약: 트래픽이 있는 서비스는 readiness와 graceful termination을 필수로 설계해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 조기 트래픽 | readinessProbe 부재 | readiness endpoint 분리 | 배포 중 5xx 0건 |
| 재시작 루프 | liveness 조건 과민 | startupProbe 추가, threshold 조정 | CrashLoopBackOff 수 |
| 종료 손실 | grace period 부족 | preStop, drain time 30초 이상 | request drop 수 |

> 요약: 생명주기 리스크는 준비 전 트래픽, 과도한 재시작, 종료 중 요청 손실에서 발생함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 준비 시간 | readiness p95 60초 이하 | kube event, metric |
| 재시작 | restart count 일 0~1회 | kube-state-metrics |
| 종료 품질 | rollout 중 5xx 0건 | ingress log, APM |

> 요약: Pod 생명주기 설계 결과는 준비 시간, 재시작 횟수, 배포 중 5xx로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Probe 분리: startupProbe는 초기 부팅, readinessProbe는 의존성 연결, livenessProbe는 복구 불가 상태에만 적용
2. 종료 처리: preStop hook과 terminationGracePeriodSeconds 30~120초를 설정하고 LB drain 시간을 반영
3. 배포 검증: rollout 동안 Ready Pod 수, restart count, 5xx rate를 SLO dashboard에 표시

**결론 (2줄):**
- 기술사 판단: Pod 트래픽 수신 여부는 Running이 아니라 Ready condition과 endpoint 등록으로 판단해야 함
- 향후 방향: probe, PDB, rollout strategy가 결합되어 Kubernetes 무중단 배포의 기본 통제 세트가 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Pod 생명주기를 설명하시오" | phase, condition, probe 전이 | Running과 Ready 차이 |
| 요구사항 명시형 | "무중단 배포 방안을 제시하시오", "장애 대응을 설명하시오" | readiness, liveness, preStop 흐름 | 5xx, restart, grace period 기준 |

> 요약: 설명형은 상태 전이, 방안형은 트래픽 통제와 종료 처리 중심으로 전환함.
