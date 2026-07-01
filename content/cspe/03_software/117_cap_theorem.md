---
title: "CAP 정리 (CAP Theorem)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 117
---

# 📖 【암기용】 개념 완전 이해

> 목적: CAP 정리를 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 분산 시스템에서 네트워크 분할이 발생하면 일관성(C)과 가용성(A)을 동시에 완전 보장할 수 없다는 원칙
- **왜 필요한가**: 여러 노드에 데이터를 나누면 네트워크 장애가 언젠가 발생한다. 그때 요청을 거부해도 같은 값을 지킬지, 응답을 계속하되 값 차이를 허용할지 결정해야 한다.
- **핵심 직관**: 지점 간 통신이 끊겼을 때 본점 확인 없이는 같은 잔액을 보장할 수 없고, 확인을 기다리면 일부 요청은 멈춘다.

## 깊이 이해
- **배경·문제의식**: 분산 DB는 복제와 샤딩으로 노드를 늘리지만, 네트워크 지연·패킷 손실·AZ 장애가 발생한다. CAP는 정상 상태가 아니라 partition 상황에서 시스템이 C 또는 A 중 무엇을 희생하는지 설명한다.
- **작동 원리**: Consistency는 모든 노드가 같은 최신 값을 보는 성질, Availability는 모든 정상 노드가 요청에 응답하는 성질, Partition tolerance는 노드 간 통신 장애를 견디는 성질이다. 실제 분산 시스템은 P를 피할 수 없으므로 CP 또는 AP 선택이 된다.
- **비유**: 두 은행 지점 연결이 끊기면 한쪽은 거래를 막아 잔액 불일치를 피하고(CP), 다른 쪽은 거래를 계속 받아 나중에 맞춘다(AP).
- **구체 예시**: etcd·ZooKeeper는 quorum 없으면 쓰기를 거부해 CP를 택한다. Cassandra·Dynamo 계열은 일부 노드만 살아도 쓰기를 받아 AP 성향을 갖는다.
- **흔한 오해·주의점**: CAP는 평상시 C/A/P 중 둘만 고르는 단순 체크표가 아니다. 네트워크 분할 발생 시 어떤 응답 정책을 선택하는지에 관한 판단 기준이다.

## 연결 개념
- PACELC — 분할이 없을 때 지연과 일관성의 선택까지 설명
- Quorum — CP 계열에서 다수 노드 합의로 일관성을 지키는 방식
- Eventual Consistency — AP 계열에서 이후 수렴을 보장하는 방식
- 분산 합의 — Raft, Paxos 기반 CP 시스템의 핵심

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CAP 답안은 세 글자 암기가 아니라 네트워크 분할 시 CP/AP 선택과 업무 영향, 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAP 정리는 분산 시스템에서 partition 발생 시 consistency와 availability를 동시에 완전 보장할 수 없다는 원칙이다.
> 2. **가치**: 금융 원장, 설정 저장소, 피드·추천처럼 업무별로 CP/AP 선택 기준을 제시하게 한다.
> 3. **판단 포인트**: partition tolerance는 선택이 아니라 전제이며, 장애 시 요청 거부(CP) 또는 stale 응답 허용(AP)을 결정해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 시스템 기본 원리 확인 | C/A/P 의미와 partition 상황의 선택 | 평상시 3개 중 2개 선택으로 단순화 |
| 업무별 DB 선택 판단 확인 | CP: 금융·설정, AP: 피드·캐시 | 제품명을 CP/AP로 고정 단정 |
| 장애 시 응답 정책 이해 확인 | quorum, timeout, stale read, conflict resolution | 네트워크 분할 조건을 누락 |

> 요약: 이 문제는 네트워크 분할 시 일관성과 응답 지속 중 무엇을 택할지 업무 기준으로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: CAP 정리는 분산 장애 시 선택 원칙이다.
- 배경: 네트워크 분할이 발생하면 모든 노드가 같은 최신값을 보장하면서 모든 정상 노드가 요청에 응답할 수 없다.
- 필요성: 업무별 CP/AP 정책, timeout, quorum, stale read, conflict resolution 기준을 사전에 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Distributed System -> Replicated Nodes
  / Consistency: 동일 최신값 관측
  / Availability: 정상 노드 응답
  / Partition Tolerance: 네트워크 분할 허용
Network Partition -> CP or AP Policy -> Business Outcome
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Consistency | 모든 읽기가 최신 쓰기 결과를 관측 | linearizability 수준과 연결 |
| Availability | 정상 노드가 모든 요청에 응답 | timeout 내 실패 응답은 가용성 저하 |
| Partition Tolerance | 노드 간 통신 단절에도 시스템 지속 | 분산 환경에서는 사실상 전제 |
| CP 정책 | 일관성 우선, 일부 요청 거부 | quorum 미달 시 쓰기 거부 |
| AP 정책 | 응답 우선, 일시 불일치 허용 | 이후 수렴·충돌 해결 필요 |

> 요약: CAP는 분산 복제 구조에서 네트워크 분할이 발생했을 때 CP 또는 AP 정책으로 업무 결과가 갈리는 원칙이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
정상 요청 -> 복제 노드 응답
Network Partition 발생
  / CP 선택 -> quorum 확인 -> 미달 시 write/read 거부
  / AP 선택 -> local node 응답 -> conflict 기록
Partition 해소 -> reconciliation -> 지표 점검
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 정상 상태에서 복제·합의·읽기 수행 | p95 latency, quorum 성공률 |
| 2 | 네트워크 분할 또는 노드 격리 발생 | packet loss, heartbeat timeout |
| 3 | CP는 quorum 없으면 요청 거부 | rejected write count |
| 4 | AP는 local write/read를 허용 | stale read, conflict count |
| 5 | 복구 후 로그 병합·충돌 해결 | convergence time |

> 요약: CAP 선택은 partition 감지 후 요청을 거부할지, 응답을 계속하고 사후 수렴할지의 운영 흐름으로 나타난다.

---

## Ⅳ. 특징

| 구분 | CP 선택 | AP 선택 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 우선 가치 | 최신값·합의 | 응답 지속 | RPO 0 vs 응답률 99.9% |
| 장애 응답 | quorum 미달 시 거부 | local replica 응답 | timeout, stale 허용 시간 |
| 대표 업무 | 원장, 설정, lock | 피드, 추천, 캐시 | 불일치 피해 금액·범위 |
| 구현 | Raft, Paxos, majority quorum | hinted handoff, read repair | W+R>N 등 |
| 한계 | partition 시 가용성 저하 | 충돌 해결 필요 | conflict rate, convergence |

> 요약: CP는 불일치 비용이 큰 업무, AP는 일시 불일치보다 응답 지속 가치가 큰 업무에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 원장 거래 | AP 허용 | CP 선택 | 이중 지불 허용 불가 |
| 상품 피드 | CP 선택 | AP 선택 가능 | stale 1~60초 허용 |
| 설정 저장소 | AP 허용 | CP 선택 | 설정 불일치가 장애 전파 |
| 글로벌 서비스 | 단일 리전 CP | 지역별 AP+수렴 | 지역 지연 100ms 이상 |

> 요약: 업무 불일치 비용이 금전·권한에 연결되면 CP, 읽기 지속과 UX가 우선이면 AP 성향을 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 서비스 중단 | CP에서 quorum 미달 | replica 수 3/5, 장애 도메인 분산 | quorum failure count |
| 데이터 충돌 | AP에서 동시 쓰기 | version vector, last-write-wins 제한 | conflict count |
| Stale read | 분할 중 local read | session consistency, read repair | stale read 비율 |

> 요약: CAP 리스크는 업무 특성과 정책 불일치이며, quorum·충돌·stale read 지표로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Quorum | 정상 quorum 성공률 99.9% 이상 | cluster metric |
| 가용성 | 업무 SLA 99.9% 등급 충족 | synthetic monitoring |
| 불일치 | conflict rate 0.1% 이하 | reconciliation log |
| 수렴 | partition 해소 후 1분~5분 | convergence metric |

> 요약: CAP 적용 평가는 quorum 성공률, 가용성, 충돌률, 수렴 시간, 지역 지연을 함께 본다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 데이터 등급화: 잔액·권한·설정은 CP, 피드·알림·캐시는 AP 성향으로 분류하고 RPO·stale 허용 시간을 명시함
2. CP 구현: etcd/ZooKeeper/Raft 기반 저장소는 3 또는 5노드 quorum, 장애 도메인 분산, timeout 값을 설계함
3. AP 구현: Cassandra/Dynamo 계열은 replication factor 3, read/write consistency level, read repair, conflict resolver를 설정함

**결론 (2줄):**
- 기술사 판단: 네트워크 분할은 피할 수 없으므로 금전·권한 데이터는 CP, 사용자 경험 중심 데이터는 AP와 수렴 절차를 선택함
- 향후 방향: 분산 SQL과 멀티리전 DB는 quorum·timestamp·TrueTime 등으로 선택 폭을 넓히지만 CAP의 장애 시 선택 원칙은 유지됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CAP 정리를 설명하시오", "기술하시오" | partition 발생 후 CP/AP 흐름 | C/A/P 의미와 업무 예시 |
| 요구사항 명시형 | "비교하시오", "선택 기준을 제시하시오" | quorum·stale read·충돌 처리 | 업무별 CP/AP 선택과 리스크 대응 |

> 요약: 설명형은 CAP 개념과 흐름, 비교형은 업무 불일치 비용을 기준으로 CP/AP 선택을 전개한다.
