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
- **개요**: 가비지 컬렉션(GC)은 **힙(Heap) 메모리**에서 더 이상 **도달 불가능한(unreachable)** 객체를 자동으로 찾아 회수하는 런타임 메모리 관리 기법이다.
- **왜 필요한가**: 개발자가 직접 `malloc/free`를 관리하면 해제를 잊거나(누수), 두 번 해제하거나(double free), 이미 해제된 메모리를 참조하는(use-after-free) 결함이 반복적으로 발생한다. GC는 이 판단을 런타임이 대신 맡아 결함 발생 지점을 언어 차원에서 없앤다.
- **핵심 직관**: 회사 출입 카드가 곧 "살아있는 직원 목록"이라면, 카드와 연결되지 않은 사물함(=아무도 참조하지 않는 객체)을 주기적으로 찾아 비우는 재고 정리 작업이다.

## 핵심 용어 정리 표 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 가비지 컬렉션(GC) | 도달 불가능 객체를 자동 회수하는 메모리 관리 기법 (상위 개념) | 자동 재고 정리 |
| 힙(Heap) | 객체가 동적으로 할당되는 메모리 영역, GC의 대상 공간 | 창고 전체 |
| GC Root | 스택 변수·static 필드처럼 항상 살아있다고 간주하는 참조 시작점 | 현재 유효한 출입 카드 목록 |
| 도달 가능성(Reachability) | GC Root에서 참조를 따라갔을 때 그 객체에 닿을 수 있는지 여부 | 카드로 열 수 있는 사물함인지 확인 |
| Mark-Sweep | 살아있는 객체를 표시(Mark)하고, 표시 안 된 객체를 회수(Sweep) | 표시 안 된 물건을 치우기 |
| Copying(복사) | 살아있는 객체만 다른 영역으로 복사하고 원래 영역을 통째로 비움 | 쓸 물건만 새 창고로 옮기고 헌 창고는 폐기 |
| Generational(세대별) GC | 객체를 young/old로 나눠 young을 자주, old를 드물게 검사 | 신입 사물함은 자주, 고참 사물함은 가끔 점검 |
| Reference Counting | 객체를 참조하는 수를 세어 0이 되면 즉시 회수 | 대여 횟수가 0이 되면 바로 반납 처리 |
| Stop-The-World(STW) | GC가 도는 동안 애플리케이션 스레드를 전부 멈추는 구간 | 재고 정리 중 매장 영업 중단 |
| Concurrent GC | 애플리케이션 스레드를 계속 돌리면서 GC를 병행 수행 | 영업하면서 동시에 재고 정리 |
| 단편화(Fragmentation) | 회수는 됐지만 조각난 빈 공간이라 큰 객체를 못 담는 상태 | 빈 칸은 많은데 큰 짐은 못 넣는 창고 |

## 깊이 이해

### 왜 자동 회수가 필요한가 (배경)
- C의 `malloc/free`처럼 개발자가 직접 메모리를 관리하면, 객체를 다 쓴 시점을 정확히 맞춰야 한다. 한 곳이라도 `free`를 빼먹으면 메모리 누수, 두 번 부르면 이중 해제, 이미 해제된 주소를 계속 쓰면 use-after-free다.
- 이런 결함은 장시간 실행되는 서버에서 서서히 메모리를 잠식하거나 보안 취약점으로 이어진다. GC는 "이 객체를 아직 누가 쓰고 있는가"를 런타임이 그래프 탐색으로 직접 판정해, 해제 시점을 사람이 맞출 필요를 없앤다.

### 도달 가능성 판정을 구체적으로 따라가기
- GC Root(현재 스레드 스택의 지역 변수, static 필드, JNI 참조 등)에서 출발해 객체가 들고 있는 참조를 계속 따라가며 방문한 객체를 전부 표시(mark)한다.
- 예를 들어 `Order` 객체를 지역 변수가 참조하고, `Order`가 `Customer`를 참조하고, `Customer`가 `Address`를 참조한다면 이 셋은 모두 도달 가능해 살아남는다. 반면 어떤 `TempBuffer` 객체를 참조하던 지역 변수가 함수를 빠져나가며 사라졌다면, 그 순간부터 `TempBuffer`는 GC Root에서 출발한 어떤 경로로도 닿을 수 없으므로 다음 GC 사이클에서 회수 대상이 된다.

### Reference Counting이 왜 GC의 전부가 아닌가
- 객체마다 "지금 몇 곳에서 참조하는지" 카운트를 두고 0이 되면 즉시 회수하는 방식도 있다(Python의 기본 메커니즘). 장점은 회수가 즉시 일어나 STW가 없다는 것이지만, 치명적 약점이 있다.
- `A`가 `B`를 참조하고 `B`가 다시 `A`를 참조하는 순환 참조가 생기면, 둘 다 카운트가 0이 되지 않아 아무도 안 쓰는데도 영원히 회수되지 않는다. 그래서 Python도 순환 참조를 잡기 위해 별도의 세대별 사이클 컬렉터를 함께 쓴다.

### Mark-Sweep vs Copying — 회수 방식의 차이
- Mark-Sweep은 살아있는 객체에 표시만 하고, 표시 안 된 객체가 있던 자리를 free list에 등록해 재사용한다. 회수는 빠르지만 회수된 공간이 곳곳에 조각나(단편화) 큰 객체를 넣을 연속 공간이 부족해질 수 있다.
- Copying은 살아있는 객체만 골라 다른 영역(to-space)으로 복사하고, 기존 영역(from-space) 전체를 통째로 비운다 — 복사 비용은 들지만 빈 공간이 한 덩어리로 모여 단편화가 없다. 생존율이 낮은 영역(대부분 죽는 곳)일수록 복사할 객체가 적어 Copying이 유리하다.

### Generational GC를 수치로 이해하기 (약한 세대 가설)
- 실측에 따르면 새로 생성된 객체의 90% 이상이 매우 짧은 시간 안에(다음 GC 전에) 죽는 경향이 있다 — 이를 "약한 세대 가설(Weak Generational Hypothesis)"이라 한다.
- 그래서 힙을 young(신생)과 old(장수) 영역으로 나눠, young은 자주(예: 수백 ms~수 초 간격) 작은 범위만 훑고, old는 드물게(예: 수 분 간격) 훑는다. young에서 몇 차례(예: 15회) GC를 살아남은 객체만 old로 승격시킨다. 이렇게 하면 매번 힙 전체를 검사하지 않아도 되어 평균 pause 시간이 크게 줄어든다.

### STW pause를 G1 예로 구체화
- JVM의 G1 GC는 힙을 여러 개의 작은 Region(예: 2,048개, 각 1~32MB)으로 쪼갠 뒤, pause target(예: 200ms)을 정해두고 그 시간 안에 회수 가능한 만큼의 Region만 골라 회수한다.
- 예를 들어 살아있는 객체 비율(live set)이 낮은 Region 10개를 골라 회수하면 200ms 안에 끝나지만, 살아있는 객체가 많은 Region이 섞이면 목표 시간을 넘길 수 있다 — 그래서 p99 GC pause를 SLO 지표로 관측해야 한다. Concurrent GC(ZGC, Shenandoah 등)는 mark 단계를 애플리케이션과 동시에 수행하는 read/write barrier를 둬 STW 구간을 수 ms 수준까지 더 줄인다.

### 비유와 흔한 오해
- 회사 출입 카드 목록이 GC Root라면, 카드가 활성화된 직원과 연결된 사물함(참조 그래프로 닿는 객체)은 안전하고, 아무 카드와도 안 이어진 사물함은 정리 대상이다.
- 흔한 오해는 "GC가 있으면 메모리 누수가 없다"는 것이다. 틀렸다 — static Map에 계속 데이터를 추가만 하고 지우지 않거나, 리스너·캐시가 더는 안 쓰는 객체를 계속 참조하고 있으면, 그 객체는 여전히 "도달 가능"하므로 GC가 절대 회수하지 않는다. 이것이 GC 환경에서도 발생하는 논리적 메모리 누수다.

## 연결 개념
- 힙·스택 — GC Root와 객체가 저장되는 메모리 공간의 기준
- Stop-The-World — GC 수행 중 애플리케이션이 멈추는 구간, pause time 지표의 근거
- 메모리 누수 — 도달은 가능하지만 실제로는 불필요한 객체를 계속 참조해 회수되지 않는 문제

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

- 개요: 가비지 컬렉션은 사용 불가능 객체를 자동 회수하는 기술이다.
- 배경: 장시간 실행 애플리케이션은 객체 생성과 해제 시점이 불일치해 힙 사용량과 단편화가 누적될 수 있다.
- 필요성: 런타임 참조 그래프 분석과 GC 정책으로 메모리 누수, pause time, 힙 사용률을 통제해야 한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
