---
title: "가비지 컬렉션 알고리즘 (Garbage Collection)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 272
---

# 📖 【암기용】 개념 완전 이해

> 목적: 가비지 컬렉션을 사용하지 않는 객체를 자동 회수하는 메모리 관리 기술로 이해하게 만든다.

## 한눈에
- **개요**: GC는 더 이상 접근할 수 없는 객체를 찾아 힙 메모리를 회수한다.
- **왜 필요한가**: 수동 `free` 누락, 중복 해제, use-after-free 같은 결함을 줄이고 장시간 실행 서버의 힙 사용량을 통제한다.
- **핵심 직관**: 창고에서 현재 주문서와 연결되지 않은 물건을 주기적으로 찾아 치우는 재고 정리다.

## 깊이 이해
- **배경·문제의식**: 동적 객체는 생성 시점과 해제 시점이 다르다. 개발자가 모든 해제 시점을 맞추면 결함이 늘어나므로 런타임이 객체 도달 가능성을 추적한다.
- **작동 원리**: GC Root에서 참조 그래프를 따라 살아 있는 객체를 표시하고, 표시되지 않은 객체를 회수하거나 살아 있는 객체를 이동해 단편화를 줄인다.
- **비유**: 회사 출입 카드가 살아 있는 직원 목록이라면, 카드와 연결되지 않은 사물함은 정리 대상이다.
- **구체 예시**: JVM G1은 힙을 Region으로 나누고, pause target 예: 200ms에 맞춰 일부 Region을 선택해 회수한다.
- **흔한 오해·주의점**: GC가 있어도 메모리 누수가 사라지지 않는다. 캐시, static map, listener가 참조를 유지하면 객체는 계속 살아 있는 것으로 판단된다.

## 연결 개념
- 힙·스택 — GC Root와 객체 저장 공간의 기준
- Stop-The-World — 애플리케이션 스레드 일시 중지 구간
- 메모리 누수 — 도달 가능한 불필요 객체 보존 문제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: GC 알고리즘을 mark-sweep, copy, generational, concurrent 방식과 pause·throughput 지표로 정리한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GC는 GC Root 기준으로 도달 불가능 객체를 식별해 힙 메모리를 자동 회수하는 런타임 기능이다.
> 2. **가치**: 수동 메모리 해제 결함을 줄이고, 힙 사용률·pause time·throughput을 정책으로 관리한다.
> 3. **판단 포인트**: 알고리즘 선택은 평균 처리량이 아니라 p99 pause, live set 크기, allocation rate, 힙 단편화로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 자동 메모리 관리 원리 확인 | GC Root, reachability, mark, sweep, compact | "자동으로 메모리 정리" 수준의 답안 |
| 알고리즘 비교 역량 확인 | reference counting, mark-sweep, copying, generational | 순환 참조와 pause trade-off 누락 |
| 운영 튜닝 판단 확인 | heap sizing, pause target, GC log, allocation rate | 튜닝 옵션만 나열하고 지표 미제시 |

> 요약: GC 답안은 도달 가능성 판정 원리와 pause·throughput·메모리 사용량의 균형을 보여야 한다.

---

## Ⅰ. 개요 및 필요성

가비지 컬렉션은 사용 불가능 객체를 자동 회수하는 힙 메모리 관리 기술이다. 장시간 실행 애플리케이션은 객체 생성과 해제 시점이 불일치하므로, 런타임이 참조 그래프를 분석해 메모리 누수와 단편화를 통제해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
GC Roots -> Object Graph -> Reachability Analysis
  -> Mark -> Sweep/Copy/Compact -> Free Space
  -> GC Log/Metric -> Tuning
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| GC Roots | 스택, static, JNI 참조 시작점 | 생존 판정 기준 |
| Mark Phase | 도달 가능한 객체 표시 | STW 또는 concurrent 수행 |
| Sweep/Copy | 미표시 객체 회수 또는 이동 | 단편화와 pause에 영향 |
| Collector Policy | Young/Old, Region, pause target | G1, ZGC, Shenandoah 등 |

> 요약: GC는 Root 탐색, 생존 표시, 회수·이동, 정책 튜닝으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
객체 할당 -> 힙 사용률 임계값 도달 -> GC Trigger
  -> Root Scan -> Mark Live Object -> Reclaim/Compact
  -> Application Resume -> GC Metric 분석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Eden 또는 heap에 객체 할당 | allocation rate MB/s |
| 2 | young/full/concurrent GC 트리거 | heap occupancy percent |
| 3 | Root scan 및 live object mark | live set size |
| 4 | 회수·압축 후 애플리케이션 재개 | pause time, reclaimed MB |

> 요약: GC는 할당 압력과 힙 점유율에 의해 실행되며, 생존 객체 크기가 pause와 회수량을 결정한다.

---

## Ⅳ. 특징

| 구분 | 전통 알고리즘 | 현대 GC | 정량·기술 포인트 |
|:---|:---|:---|:---|
| Mark-Sweep | 미도달 객체 회수 | 단편화 발생 | free list 관리 필요 |
| Copying | 생존 객체 복사 | young generation에 적합 | 객체 생존율 낮을 때 회수량 큼 |
| Generational | 세대별 회수 | young GC 빈번, old GC 제한 | 약한 세대 가설 활용 |
| Concurrent | 애플리케이션과 병행 | read/write barrier 필요 | p99 pause 10ms 목표 가능 |

> 요약: 알고리즘은 회수량, 단편화, pause time, barrier 비용의 균형으로 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 수동 관리 | `malloc/free` | 자동 GC | use-after-free 위험을 런타임으로 이전 |
| 처리량 우선 | Parallel GC | G1/ZGC | 배치 처리량 vs p99 pause 기준 |
| 지연 우선 | STW 압축 | concurrent compact | SLO p99 50ms 이하 서비스 |

> 요약: 배치 처리는 throughput collector, 사용자 요청 서버는 low-pause collector가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 긴 pause | live set 과다, full GC | heap sizing, region GC, 객체 수명 분석 | p99 GC pause |
| 메모리 누수 | 캐시·리스너 참조 유지 | weak reference, cache TTL, heap dump | retained heap MB |
| CPU 증가 | concurrent barrier 비용 | collector 변경, allocation 감소 | GC CPU percent |

> 요약: GC 리스크는 pause, retained heap, GC CPU 비율로 분리해 대응한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| pause | p99 GC pause 50~200ms 이하 | GC log, JFR |
| 회수 효율 | GC 후 old gen 사용률 70% 이하 | heap metric |
| 누수 탐지 | retained heap 지속 증가 0건 | heap dump diff |

> 요약: GC 튜닝 결과는 pause, old gen 점유율, retained heap 추세로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. JVM은 G1/ZGC 선택 후 `-Xms=-Xmx`, pause target, GC log를 설정하고 부하 테스트에서 p99 GC pause를 확인함.
2. 객체 할당이 많은 경로는 allocation profiler로 상위 10개 타입을 식별하고 pooling보다 객체 수명 단축을 우선 적용함.
3. 누수 의심 시 heap dump 2회 비교, dominator tree, retained heap 기준으로 캐시·리스너·ThreadLocal 참조를 제거함.

**결론 (2줄):**
- 기술사 판단: 처리량 배치는 Parallel GC, 대화형 서버는 G1/ZGC처럼 pause 목표를 제어하는 collector 선택.
- 향후 방향: 대용량 힙과 컨테이너 환경에서 region 기반·concurrent GC와 observability 결합이 표준 운영 방식이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GC 알고리즘을 설명하시오" | Root scan, mark, sweep, compact 흐름 | 알고리즘별 장단점과 사용 조건 |
| 요구사항 명시형 | "튜닝 방안을 제시하시오", "비교하시오" | GC log 분석, pause 원인 흐름 | p99 pause, heap sizing, 누수 대응 |

> 요약: 설명형은 알고리즘 원리, 방안형은 관측 지표와 튜닝 절차 중심으로 전환한다.
