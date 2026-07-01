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
- **개요**: Pod가 생성 요청부터 스케줄링, 실행, 준비, 종료, 재시작까지 거치는 상태 변화
- **왜 필요한가**: 장애 복구와 무중단 배포는 Pod 상태, probe, restartPolicy, termination 처리를 이해해야 설계할 수 있다.
- **핵심 직관**: Pod는 한 번 태어나면 상태를 보고하고, 준비되면 트래픽을 받고, 종료 신호를 처리한 뒤 사라지는 실행 생명체이다.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 프로세스 실행 단위지만 Kubernetes는 Pod를 스케줄링 단위로 다룬다. Pod가 언제 트래픽을 받아도 되는지, 언제 재시작해야 하는지, 언제 종료할지 명확히 해야 서비스 중단을 줄일 수 있다.
- **작동 원리**: Pending 단계에서 스케줄링과 이미지 다운로드가 수행되고, Running 단계에서 컨테이너가 시작된다. readinessProbe가 성공해야 Service endpoint에 포함되고, livenessProbe 실패 시 kubelet이 재시작한다.
- **비유**: 매장 직원이 출근(Pending), 업무 준비(Ready), 고객 응대(Running), 건강 점검(liveness), 퇴근 인수인계(preStop)를 거치는 절차와 같다.
- **구체 예시**: readinessProbe `/health/ready`가 200을 반환하기 전에는 Service가 트래픽을 보내지 않는다. 종료 시 terminationGracePeriodSeconds 30초 동안 SIGTERM 처리 후 SIGKILL이 발생한다.
- **흔한 오해·주의점**: Running은 트래픽 수신 가능 상태가 아니다. Service 트래픽은 Ready condition과 endpoint 반영 여부로 판단해야 한다.

## 연결 개념
- Probe - startup, readiness, liveness 상태 점검
- Deployment - Pod 생명주기를 rollout 단위로 관리
- Service Endpoint - Ready Pod만 트래픽 대상으로 등록

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
