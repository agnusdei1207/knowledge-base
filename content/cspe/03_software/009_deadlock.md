---
title: "교착상태 조건·예방·회피·탐지·복구 (Deadlock)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 9
---

# 📖 【암기용】 개념 완전 이해

> 목적: 교착상태를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서로 자원을 쥔 채 상대 자원을 기다려 모두 멈춘 상태
- **왜 필요한가**: OS, DBMS, 분산 시스템은 lock, file, memory, device 같은 한정 자원을 공유하므로 대기 관계가 순환되면 처리 중단이 발생한다.
- **핵심 직관**: 두 사람이 서로의 열쇠를 들고 상대방이 먼저 문을 열어주기만 기다리는 상황이다.

## 깊이 이해
- **배경·문제의식**: 동시성은 자원 공유를 필요로 한다. 하지만 상호배제 자원을 점유한 상태에서 추가 자원을 기다리면, 작은 lock 순서 오류가 전체 서비스 중단으로 커질 수 있다.
- **작동 원리**: 교착상태는 mutual exclusion, hold and wait, no preemption, circular wait 네 조건이 동시에 성립할 때 발생한다. 대응은 조건을 깨는 예방, safe state만 허용하는 회피, wait-for graph 탐지, victim rollback 복구로 나뉜다.
- **비유**: 좁은 다리 양쪽에서 차가 서로 양보 없이 진입해, 뒤로 물러날 수도 없고 앞차가 빠질 수도 없는 상황이다.
- **구체 예시**: Thread A가 lock X를 잡고 lock Y를 기다리고, Thread B가 lock Y를 잡고 lock X를 기다리면 wait-for graph A -> B -> A cycle이 생긴다.
- **흔한 오해·주의점**: 기아(starvation)는 계속 밀려 실행 기회를 못 얻는 것이고, 교착상태는 순환 대기로 아무도 진행하지 못하는 상태이다.

## 연결 개념
- Banker's Algorithm: safe state 기반 회피
- Wait-for Graph: cycle 탐지
- Lock Ordering: circular wait 예방 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 교착상태는 4조건 암기보다 발생 조건을 깨는 정책과 탐지·복구 비용을 비교하는 답안이 필요하다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 교착상태는 여러 프로세스가 서로 보유 자원을 놓지 않고 상대 자원을 기다려 진행 불능이 되는 동시성 장애이다.
> 2. **가치**: 예방·회피·탐지·복구 전략을 통해 lock 기반 시스템의 무한 대기와 서비스 중단을 통제한다.
> 3. **판단 포인트**: mutual exclusion, hold and wait, no preemption, circular wait 중 어떤 조건을 정책적으로 끊을지 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 교착상태 발생 조건 이해 확인 | Coffman 4조건과 동시 성립 | 4조건 중 일부만 제시 |
| 대응 전략 비교 확인 | prevention, avoidance, detection, recovery | 예방과 회피 구분 누락 |
| 실무 lock 설계 판단 확인 | lock ordering, timeout, rollback, wait-for graph | starvation과 deadlock 혼동 |

> 요약: 이 문제는 4조건을 기반으로 정책 선택과 운영 대응을 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

교착상태는 순환 대기로 진행이 멈춘 상태이다.
프로세스·스레드가 lock, file, device, transaction 자원을 공유할 때 발생하며, 한 번 발생하면 외부 개입 없이는 해소되지 않는다.
운영체제와 DBMS는 예방·회피·탐지·복구를 상황별로 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Process A holds R1 -> waits R2
Process B holds R2 -> waits R1
Mutual Exclusion / Hold and Wait / No Preemption / Circular Wait
-> Deadlock
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Mutual exclusion | 동시에 공유 불가 자원 | mutex, printer, row lock |
| Hold and wait | 자원 보유 중 추가 자원 대기 | multi-lock transaction |
| No preemption | 강제 회수 불가 | 임계구역 일관성 보호 |
| Circular wait | 대기 관계 cycle 형성 | wait-for graph cycle |

> 요약: 교착상태는 네 조건이 동시에 성립할 때 발생하며, 하나라도 제거하면 예방 가능하다.

---

## Ⅲ. 동작원리 및 흐름도

```text
자원 요청 -> 사용 가능 여부 확인
-> 보유 자원 유지한 채 대기
-> 다른 프로세스도 상호 대기
-> Wait-for Graph cycle 형성
-> 탐지 후 victim 선정/rollback/kill
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프로세스가 lock/resource 요청 | lock wait event |
| 2 | 자원 불가 시 wait queue 진입 | wait duration |
| 3 | 보유 자원은 release하지 않음 | held lock count |
| 4 | wait-for graph에 cycle 생성 | cycle detection |
| 5 | timeout, rollback, kill로 복구 | recovery time |

> 요약: 교착상태는 보유와 대기가 누적되어 cycle이 생기고, 탐지 후 victim 처리로 해소된다.

---

## Ⅳ. 특징

| 대응 | 원리 | 장점/한계 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 예방 | 4조건 중 하나 제거 | 보수적, 자원 이용률 감소 | lock ordering |
| 회피 | safe state만 허용 | 사전 최대 요구량 필요 | Banker's Algorithm |
| 탐지 | cycle 발생 후 발견 | 이용률 유지, 탐지 비용 | wait-for graph O(V+E) |
| 복구 | victim 종료/rollback | 데이터 손실 가능 | rollback log, timeout |

> 요약: 예방은 발생 전 차단, 회피는 안전 상태 유지, 탐지는 발생 후 식별, 복구는 victim 처리이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | lock 무순서 획득 | lock ordering/timeout | 공유 자원 수와 criticality |
| 비용/성능 | 자원 이용률 우선 | deadlock risk 통제 | wait time, throughput |
| 운영/위험 | 수동 재시작 | detection+rollback 자동화 | RTO, data consistency |

> 요약: 핵심 업무는 예방·회피, 일반 업무는 탐지·복구를 선택해 자원 이용률과 장애 위험을 조정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 서비스 중단 | cycle 미탐지 | wait-for graph 주기 탐지 | deadlock count |
| 데이터 불일치 | victim 강제 종료 | transaction log, rollback | rollback success rate |
| 기아 전환 | 동일 victim 반복 선정 | victim cost 함수, aging | victim repeat count |

> 요약: 탐지 후 복구는 중단 시간, rollback 성공률, victim 편중을 함께 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| lock 대기 | lock wait p95 100ms 이하 | DB/OS lock monitor |
| deadlock | deadlock 0건 또는 자동복구 1분 이내 | alert, event log |
| 복구 | rollback success 99% 이상 | transaction audit |

> 요약: 교착상태 관리는 lock wait, deadlock count, rollback 성공률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 모든 lock에 전역 획득 순서를 부여하고 code review에서 order violation을 차단해 circular wait 제거
2. DBMS transaction은 lock timeout 1~5초, deadlock detector, retry with backoff를 적용해 사용자 영향 시간을 제한
3. 운영 지표로 lock wait p95, deadlock count, rollback success rate를 수집하고 deadlock graph를 장애 보고서에 첨부

**결론 (2줄):**
- 기술사 판단: safety-critical 자원은 예방·회피, 처리량 중심 DBMS는 탐지·복구와 retry를 선택함
- 향후 방향: 분산 lock과 microservice transaction에서는 local lock 순서뿐 아니라 lease, fencing token, saga 보상까지 포함해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "교착상태를 설명하시오" | 4조건과 wait-for graph 흐름 | 예방·회피·탐지·복구 비교 |
| 요구사항 명시형 | "해결 방안을 제시하시오" | cycle 탐지와 victim 처리 절차 | lock ordering·timeout·rollback |

> 요약: 설명형은 발생 조건, 방안형은 조건 제거와 운영 복구를 중심으로 답안을 전환한다.
