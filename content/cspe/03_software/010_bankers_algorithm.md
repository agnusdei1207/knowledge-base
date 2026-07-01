---
title: "은행원 알고리즘 (Banker's Algorithm)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 10
---

# 📖 【암기용】 개념 완전 이해

> 목적: 은행원 알고리즘을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 자원 요청을 승인해도 안전 순서가 남는지 확인하는 교착상태 회피 알고리즘
- **왜 필요한가**: 자원을 무작정 할당하면 나중에 모든 프로세스가 추가 자원을 기다리는 교착상태가 생길 수 있다.
- **핵심 직관**: 은행이 대출을 해줘도 모든 고객이 순서대로 상환할 수 있는 현금 여력이 남는지 먼저 계산하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 교착상태 예방은 자원 사용을 과도하게 제한할 수 있다. 회피는 각 프로세스의 최대 요구량을 알고 있다고 가정하고, 요청 시마다 safe state를 유지하는지만 검사한다.
- **작동 원리**: Available은 남은 자원, Max는 최대 요구량, Allocation은 현재 할당량, Need는 Max-Allocation이다. 요청을 임시 할당한 뒤 Work와 Finish 배열로 모든 프로세스를 완료시킬 안전 순서가 있는지 확인한다.
- **비유**: 결혼식장 주차 관리자가 남은 주차면과 하객별 최대 차량 수를 보고, 지금 입장을 허용해도 나중에 모든 팀이 빠져나갈 순서가 있는지 보는 것이다.
- **구체 예시**: Available [3,3,2], 한 프로세스 Need [1,2,2]이면 실행 가능 후보가 된다. 완료 후 Allocation을 Available에 반환해 다음 후보를 찾는다.
- **흔한 오해·주의점**: safe state는 교착상태가 없다는 뜻이지만, unsafe state가 곧 교착상태는 아니다. unsafe는 앞으로 교착상태가 될 가능성을 가진 상태이다.

## 연결 개념
- Deadlock Avoidance: 발생 가능 상태를 사전에 차단
- Safe Sequence: 모든 프로세스가 완료 가능한 실행 순서
- Resource Allocation Graph: 단일 인스턴스 자원 회피 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 은행원 알고리즘은 행렬 계산 절차와 safe/unsafe 의미, 사전 최대 요구량이라는 한계를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 은행원 알고리즘은 자원 요청 승인 전 safe state 여부를 검사해 교착상태를 회피하는 알고리즘이다.
> 2. **가치**: Available, Max, Allocation, Need 행렬로 안전 순서를 확인해 circular wait 가능성을 사전에 차단한다.
> 3. **판단 포인트**: 최대 요구량 사전 파악, 자원 인스턴스 고정, 계산 비용 때문에 범용 OS보다 교육·특수 시스템에 적합하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| deadlock avoidance 이해 확인 | safe state, unsafe state, safe sequence | unsafe와 deadlock 동일시 |
| 행렬 기반 절차 확인 | Available, Max, Allocation, Need | Need=Max-Allocation 누락 |
| 한계 판단 확인 | 최대 요구량 사전 선언, 동적 자원 부적합 | 현실 OS 적용 제약 누락 |

> 요약: 이 문제는 계산 절차와 회피 알고리즘의 적용 한계를 동시에 요구한다.

---

## Ⅰ. 개요 및 필요성

은행원 알고리즘은 safe state 기반 자원 할당 회피 기법이다.
프로세스의 최대 자원 요구량을 미리 알고, 요청 승인 후에도 모든 프로세스를 완료할 안전 순서가 존재하는지 검사한다.
교착상태 예방보다 자원 이용률을 높이면서도 unsafe 상태 진입을 막기 위해 사용한다.

---

## Ⅱ. 구조 및 구성요소

```text
Resource Request -> Available / Max / Allocation / Need 확인
-> 임시 할당 -> Safety Algorithm
-> Safe Sequence 존재: 승인 / 없음: 대기
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Available | 현재 사용 가능한 자원 벡터 | 전체 자원-할당량 |
| Max | 프로세스별 최대 요구 행렬 | 사전 선언 필요 |
| Allocation | 현재 할당된 자원 행렬 | 실행 중 갱신 |
| Need | 남은 필요량 행렬 | Max-Allocation |
| Safe sequence | 완료 가능한 프로세스 순서 | 존재 시 safe state |

> 요약: 은행원 알고리즘은 네 행렬과 안전 순서 존재 여부로 요청 승인 여부를 판단한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request_i 접수 -> Request_i <= Need_i 확인
-> Request_i <= Available 확인
-> Available/Allocation/Need 임시 갱신
-> Safety Algorithm 수행
-> Safe면 Commit / Unsafe면 Rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청량이 Need 이하인지 확인 | Request_i <= Need_i |
| 2 | 요청량이 Available 이하인지 확인 | Request_i <= Available |
| 3 | 임시로 Available 감소, Allocation 증가, Need 감소 | matrix consistency |
| 4 | Work, Finish로 완료 가능한 프로세스 반복 탐색 | Finish all true |
| 5 | safe sequence 있으면 승인, 없으면 원복 | safe/unsafe 판정 |

> 요약: 요청 검사는 범위 확인, 임시 할당, 안전성 검사, 승인 또는 원복 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | 은행원 알고리즘 | 탐지·복구 방식 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 대응 시점 | 요청 승인 전 | deadlock 발생 후 | avoidance vs detection |
| 필요 정보 | Max, Allocation, Available | wait-for graph | Need=Max-Allocation |
| 장점/한계 | unsafe 차단, 사전 정보 필요 | 이용률 높음, 복구 비용 | O(mn^2) 수준 검사 |
| 적용 대상 | 자원 수 고정·최대 요구량 명확 | DBMS·일반 OS | embedded, batch |

> 요약: 은행원 알고리즘은 안전 상태를 보장하지만 최대 요구량을 모르면 적용하기 어렵다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | deadlock prevention | deadlock avoidance | 자원 이용률과 안전성 균형 |
| 비용/성능 | 조건 제거로 보수적 | 요청마다 safety check | 프로세스 수 n, 자원종류 m |
| 운영/위험 | 사전 제한 | Max 오신고 시 실패 | 최대 요구량 신뢰성 |

> 요약: 최대 요구량이 신뢰 가능하고 자원 종류가 제한적이면 회피 방식이 의미가 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Max 부정확 | 프로세스가 최대 요구량을 모름 | admission 단계에서 계약화 | Max violation count |
| 계산 부담 | 요청마다 matrix scan | 자원 종류 제한, batch check | safety check latency |
| 자원 이용률 저하 | unsafe 요청 대기 | priority와 timeout 정책 | wait time, utilization |

> 요약: 실무 적용 리스크는 Max 신뢰성, 계산 지연, 대기 증가이며 적용 범위를 제한해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 안전성 | unsafe 승인 0건 | simulation, unit test |
| 계산 지연 | safety check p95 5ms 이하 | benchmark |
| 이용률 | resource utilization 70% 이상 | allocation log |

> 요약: 은행원 알고리즘은 unsafe 승인 0건과 계산 지연, 자원 이용률을 함께 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. batch scheduler나 embedded controller처럼 task set과 Max가 고정된 환경에서 Available·Max·Allocation·Need 행렬을 사전 검증
2. 요청 승인 경로에 safety check p95 5ms 이하 기준을 두고, 초과 시 자원 종류 축소 또는 batch 승인으로 조정
3. unsafe 판정 요청은 대기 queue에 넣고 timeout·priority 정책을 결합해 장기 대기와 기아를 방지

**결론 (2줄):**
- 기술사 판단: Max 요구량을 사전에 알 수 있으면 은행원 알고리즘, 동적 workload가 크면 lock ordering 또는 탐지·복구를 선택함
- 향후 방향: 클라우드·DBMS 환경에서는 순수 Banker보다 quota, admission control, retry 정책과 결합한 회피 모델이 실용적임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "은행원 알고리즘을 설명하시오" | Request와 Safety Algorithm 단계 | safe/unsafe와 한계 |
| 요구사항 명시형 | "교착상태 회피 방안을 제시하시오" | 행렬 계산과 승인/거절 흐름 | 예방·탐지 방식과 선택 기준 |

> 요약: 설명형은 행렬 절차, 비교형은 회피 방식의 적용 조건과 한계를 중심으로 작성한다.
