---
title: "프로세스 생성·종료·상태 전이 (Process Lifecycle)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 3
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 프로세스 상태 전이는 하나의 프로세스가 생성(New)부터 종료(Terminated)까지 거치는 **상태 모델**로, OS가 CPU·메모리 자원 상황에 따라 프로세스를 상태 간에 옮기는 관리 체계다.
- **왜 필요한가**: CPU는 한 번에 한 프로세스만 실행하므로, 지금 CPU를 기다리는 프로세스와 I/O를 기다리는 프로세스를 구분해야 OS가 낭비 없이 스케줄링할 수 있다.
- **핵심 직관**: 병원 진료와 같다. 접수(New) → 대기실(Ready) → 진찰(Running) → 검사 대기(Blocked) → 귀가(Terminated), 병실 부족 시 집에서 대기(Suspend).

## 핵심 용어 정리 (내부에 등장하는 것들)

프로세스·PCB·전환 개념은 001·002에서 세웠으므로, 여기서는 "어떤 상태가 있고 무엇이 상태를 바꾸는가"의 용어를 정리한다.

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 상태 전이 (State Transition) | 특정 이벤트로 프로세스가 상태를 바꾸는 것 (상위 키워드) | 진료 단계 이동 |
| New (생성) | PCB는 만들어졌으나 아직 메모리 적재 전 | 접수 완료, 대기실 진입 전 |
| Ready (준비) | 메모리에 적재돼 CPU 배정을 기다림 | 대기실에서 호명 대기 |
| Running (실행) | CPU를 점유해 명령어 실행 중 | 의사와 면담 중 |
| Blocked / Waiting (대기) | I/O 완료 등 특정 이벤트를 기다림 | 엑스레이 결과 대기 |
| Terminated (종료) | 실행을 마치고 자원 회수 대기(좀비 포함) | 진료 종료·귀가 |
| Suspend (지연) | 메모리 부족으로 디스크(Swap)로 내보내진 상태 | 병실 부족으로 귀가 대기 |
| Admit | New → Ready 전이 (메모리 적재 승인) | 대기실 입장 허가 |
| Dispatch | Ready → Running 전이 (CPU 배정) | 진료실 호출 |
| Timeout / Preemption | Running → Ready 전이 (타임슬라이스 만료·선점) | 시간 초과로 다음 사람에 양보 |
| Block | Running → Blocked 전이 (I/O 요청) | 검사받으러 이동 |
| Wakeup | Blocked → Ready 전이 (이벤트 완료) | 검사 끝나 대기실 복귀 |
| Swap-out / Swap-in | 메모리↔디스크로 프로세스를 내리고 올림 | 귀가시켰다 다시 호출 |
| 기아 (Starvation) | 우선순위에 밀려 특정 프로세스가 영구 대기 | 계속 뒷사람에 밀려 못 들어감 |
| 에이징 (Aging) | 대기 시간이 길수록 우선순위를 높여 기아를 막는 기법 | 오래 기다린 순서로 가점 |

## 깊이 이해
- **배경·문제의식**: 프로세스가 I/O를 요청한 뒤 응답을 기다리는 동안 CPU를 붙잡고 있으면 큰 낭비다(CPU와 디스크의 속도 차는 수만 배). OS는 상태를 정의해, I/O를 기다리는 프로세스에서 CPU를 회수(Blocked)하고 준비된(Ready) 다른 프로세스에 넘긴다.
- **작동 원리(어떻게+왜)**: 핵심 전이는 Dispatch(Ready→Running), Timeout(Running→Ready), Block(Running→Blocked), Wakeup(Blocked→Ready)이다. 여기에 메모리가 부족하면 활성 프로세스를 디스크로 내리는 Suspend(Swap-out)가 더해져 5상태가 7상태로 확장된다. 상태 전이 시 실제 CPU 문맥 저장·복원은 002의 컨텍스트 스위칭이 수행한다.
- **비유**: Running 프로세스가 파일 읽기를 요청하면 OS는 "결과 나올 때까지 비켜"라며 Blocked로 보내고, 그 사이 Ready 큐의 다른 프로세스를 Running으로 올린다(Dispatch). 병실(메모리)이 모자라면 안정된 환자를 잠시 집으로 돌려보낸다(Suspend).
- **구체 예시**: `sleep(1)`을 호출하면 프로세스는 즉시 Running→Blocked가 되고, 1초 뒤 타이머 인터럽트로 Wakeup되어 Ready로 간다. `top`의 상태 열에서 `R`(Running/Ready), `D`(Blocked, 무중단 대기), `S`(Sleep), `Z`(좀비), `T`(중지)로 이 상태들을 관측한다.
- **흔한 오해·주의점**: Blocked에서 이벤트가 완료돼도 곧장 Running이 되지 **않는다**. 반드시 Ready 큐로 가서 CPU 배정 순서를 다시 기다린다. 이 지점을 틀리면 상태 모델 이해 자체를 의심받는 대표 오답이다.

## 연결 개념
- PCB·컨텍스트 스위칭 (002 참조) — 상태 전이 시 실제 문맥을 저장·복원하는 작업
- 프로세스 스케줄링 (004 참조) — Ready 큐에서 Running으로 올릴 프로세스 선택 정책
- 가상 메모리·스레싱 (016·015 참조) — Suspend와 직결된 Swap 및 과도한 교체 문제

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 상태 전이는 OS가 다중 프로그래밍을 위해 생애주기(New–Ready–Running–Blocked–Terminated)를 관리하는 모델임.
> 2. **가치**: I/O 대기 프로세스를 CPU 스케줄링 후보에서 배제해 CPU 활용률을 극대화함.
> 3. **판단 포인트**: 메모리 고갈 시 Suspend(지연) 상태와 Swap으로 다중 프로그래밍 정도를 통제해 스레싱을 방지함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 생애주기 제어 원리 이해 | 5기본 상태 + 2지연(Suspend) 상태 | Blocked→Running 직접 전이 오답 |
| 이벤트–전이 매핑 | Dispatch·Timeout·Block·Wakeup 트리거 | 상태 명칭만 적고 전이 조건 누락 |
| 메모리 고갈 대처 | Suspend-Ready·Suspend-Blocked, Swap in/out | 메모리 관리 관점 누락 |

> 요약: 기본 5상태에 메모리 부족 시의 지연 2상태를 더한 7상태 모델로 자원 병목 통제를 설명함.

---

## Ⅰ. 개요 및 필요성

- 개요: 프로세스가 생성(New)부터 종료(Terminated)까지 CPU·I/O 이벤트에 따라 겪는 상태 변화 모델임
- 배경: CPU와 I/O 장치의 속도 차가 커, I/O 대기 프로세스가 CPU를 점유하면 심각한 낭비가 발생함
- 필요성: 자원의 효율적 분배와 다중 프로그래밍 정도 유지, 기아 방지를 위해 상태 추적이 필수임

---

## Ⅱ. 구조 및 구성요소

- 상태 전이(선형 도식, 이벤트는 화살표 옆 표기):

```text
New -(Admit)-> Ready -(Dispatch)-> Running -(Exit)-> Terminated
Running -(Timeout)-> Ready
Running -(Block)-> Blocked -(Wakeup)-> Ready
Ready / Blocked -(Suspend·Swap-out)-> Suspend(디스크) -(Resume·Swap-in)-> Ready
```

| 상태 | 설명 | 보관 위치 |
|:---|:---|:---|
| Ready | 메모리에 적재돼 CPU 배정 대기 | Ready Queue(메모리) |
| Running | CPU 점유해 명령어 실행 중 | CPU 레지스터 |
| Blocked | I/O 등 이벤트 완료 대기 | Device/Wait Queue(메모리) |
| Suspend-Ready | Ready이나 메모리 부족으로 디스크로 밀림 | Swap Space(디스크) |
| Suspend-Blocked | Blocked이나 메모리 부족으로 디스크로 밀림 | Swap Space(디스크) |

> 요약: 활성 상태(Ready·Running·Blocked)는 메인 메모리에, 메모리 부족 시 밀려난 Suspend 상태는 디스크에 존재함.

---

## Ⅲ. 동작원리 및 흐름도

```text
New -> Ready(메모리 할당) -> Dispatch -> Running
  -> [I/O 요청] Running -> Blocked -> [I/O 완료] Blocked -> Ready
  -> [타임슬라이스 만료] Running -> Ready
  -> [완료] Running -> Terminated
```

- 1단계 [Dispatch]: 스케줄러가 Ready 큐에서 프로세스를 골라 CPU를 배정함 (Ready → Running)
- 2단계 [Block]: Running 프로세스가 디스크 읽기 등 I/O를 요청하면 대기 큐로 이동함 (Running → Blocked)
- 3단계 [Wakeup]: I/O 완료 인터럽트가 오면 대기 프로세스를 Ready 큐로 되돌림 (Blocked → Ready)
- 4단계 [Timeout]: 라운드로빈 등에서 할당 시간이 만료되면 CPU를 선점당함 (Running → Ready)

> 요약: 스케줄러와 하드웨어 인터럽트가 협력해 프로세스를 큐 사이로 끊임없이 전이시킴.

---

## Ⅳ. 특징

- 제어 주체: 상태 전이는 프로세스 자율이 아니라 OS 스케줄러와 인터럽트 핸들러가 통제함
- 전환 비용 동반: Ready ↔ Running 전이마다 002의 PCB 저장·복원(컨텍스트 스위칭) 비용이 발생함
- 큐 기반 관리: Ready Queue·Device Queue 등 자료구조로 상태별 프로세스를 그룹 단위로 추적함
- 메모리 연동: Suspend 전이는 CPU가 아니라 메모리 가용량이 트리거로, 스케줄링과 메모리 관리가 맞물림

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 활성 상태 (Active) | 지연 상태 (Suspend) | 전환 기준 |
|:---|:---|:---|:---|
| 거주 위치 | 메인 메모리 | 디스크(Swap Space) | 시스템 메모리 가용량 |
| 진입 이벤트 | Admit·Wakeup | Suspend(Swap-out) | 메모리 임계치 미달 시 |
| 복귀 이벤트 | Dispatch | Resume(Swap-in) | 메모리 확보 또는 우선도 상승 |

> 요약: 다중 프로그래밍 한계치를 넘으면 OS가 Blocked 프로세스부터 Suspend해 메모리를 확보함.

**리스크·대응 (불릿):**
- 기아(Starvation): 우선순위 밀림으로 특정 프로세스 영구 대기 → 에이징(Aging) 적용 (지표: Ready Queue 체류 시간)
- 스레싱(Thrashing): Suspend↔Resume 교체 과다 → Working Set 기반 동시 실행 수 조절 (지표: Page Fault Rate)

**점검 지표 (불릿):**
- 성능: Ready Queue 평균 대기 시간, CPU 활용률
- 운영: Swap-in/out 빈도(pswpin/pswpout)

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. I/O 바운드 우선 배정: I/O 바운드 프로세스가 Ready가 되면 우선 Dispatch해 장치 가동률을 높임
2. 메모리 고갈 대비 모니터링: OOM Killer 작동 전 Swap 사용률을 관측해 유휴 프로세스를 선제 정리함
3. 데드락 회복: 영구 Blocked를 탐지하면 프로세스를 강제 종료 후 재기동함

**결론 (2줄):**
- 기술사 판단: 상태 전이는 이론 모델을 넘어, Load Average와 자원 병목을 진단하는 실무 프레임워크임
- 향후 방향: 컨테이너 환경에서 Pod 생명주기(Pending·Running·Succeeded·Failed)로 상태 관리가 확장되는 추세임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "프로세스 상태 전이를 설명하시오" | 5·7상태 도식·전이 조건 | Suspend 필요성·큐 연계 |
| 문제점 대책형 | "메모리 부족 시 상태 전이와 대책" | Suspend 전이 흐름 집중 | 스레싱 원인·Swap 최적화 |

> 요약: 포괄형은 상태 모델과 전이 조건을, 대책형은 Suspend와 메모리 병목 대응을 답안 무게중심으로 둠.
