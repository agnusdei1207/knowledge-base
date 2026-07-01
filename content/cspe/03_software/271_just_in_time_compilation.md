---
title: "JIT 컴파일 (Just-In-Time Compilation)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 271
---

# 📖 【암기용】 개념 완전 이해

> 목적: JIT 컴파일을 VM 실행 중 수집한 정보를 이용해 핫 코드를 네이티브 코드로 바꾸는 기술로 이해하게 만든다.

## 한눈에
- **개요**: JIT은 실행 중 자주 쓰는 코드를 즉시 네이티브 코드로 컴파일하는 런타임 최적화다.
- **왜 필요한가**: 바이트코드 이식성과 네이티브 코드 실행 지연 단축을 동시에 얻기 위해 필요하다.
- **핵심 직관**: 처음에는 통역으로 진행하다가 반복되는 문장은 현장에서 번역문을 만들어 계속 재사용하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 바이트코드 VM은 플랫폼 이식성이 있으나 명령 해석 비용이 발생한다. JIT은 실제 실행 프로파일을 바탕으로 자주 실행되는 경로만 컴파일한다.
- **작동 원리**: 인터프리터가 메서드 호출 횟수와 분기 빈도를 수집하고, 임계값을 넘은 코드를 C1/C2 같은 컴파일러가 최적화한다.
- **비유**: 콜센터 상담원이 반복 질문 답변을 스크립트로 만들어 다음 상담부터 읽는 것과 같다.
- **구체 예시**: HotSpot JVM은 메서드 호출 카운터가 임계값을 넘으면 tiered compilation을 수행하고, deoptimization으로 가정이 깨진 코드를 인터프리터로 되돌린다.
- **흔한 오해·주의점**: JIT은 항상 실행 지연을 줄이지 않는다. warm-up 전에는 컴파일 비용과 코드 캐시 사용량이 p95 지연을 늘릴 수 있다.

## 연결 개념
- 바이트코드 VM — JIT이 최적화할 중간 실행 표현
- 프로파일 기반 최적화 — 실제 분기·타입 정보를 활용
- AOT 컴파일 — 배포 전 네이티브 코드 생성 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: JIT을 단순 컴파일 방식이 아니라 프로파일 수집, 핫스팟 탐지, 코드 캐시, deoptimization까지 포함한 런타임 최적화로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: JIT 컴파일은 VM 실행 중 핫스팟 코드를 네이티브 코드로 변환하여 해석 비용을 줄이는 기법이다.
> 2. **가치**: 플랫폼 이식성은 바이트코드가, 실행 경로 최적화는 런타임 프로파일이 담당한다.
> 3. **판단 포인트**: warm-up, code cache, GC, deoptimization 지표를 함께 봐야 서버 운영 적합성을 판단할 수 있다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| VM 최적화 구조 이해 확인 | 인터프리터, profiler, compiler, code cache | "실행 중 컴파일" 한 줄로 종료 |
| 서버 운영 판단 확인 | warm-up time, p95 latency, code cache pressure | 평균 지연만 제시하고 초기 지연 누락 |
| AOT와 비교 역량 확인 | JIT의 동적 최적화 vs AOT의 예측 가능한 시작 시간 | JIT과 AOT를 우열 관계로 단정 |

> 요약: JIT 문제는 핫스팟 탐지부터 운영 지표까지 연결해야 채점 포인트를 확보한다.

---

## Ⅰ. 개요 및 필요성

JIT 컴파일은 실행 중 필요한 시점에 바이트코드를 네이티브 코드로 변환하는 기술이다. VM 기반 언어는 이식성을 확보하지만 해석 비용이 발생하므로, 실제 실행 빈도가 높은 코드만 최적화해 CPU 사용률과 지연을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Bytecode -> Interpreter -> Profiler -> Hotspot Detector
  -> JIT Compiler -> Code Cache -> Native Execution
  -> Deoptimization -> Interpreter
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Interpreter | 바이트코드 초기 실행 | warm-up 구간 담당 |
| Profiler | 호출 횟수, 타입, 분기 빈도 수집 | tiered compilation 입력 |
| JIT Compiler | IR 최적화 후 네이티브 코드 생성 | inlining, escape analysis |
| Code Cache | 생성 코드 저장·재사용 | 용량 부족 시 컴파일 제한 |

> 요약: JIT은 해석, 프로파일링, 컴파일, 코드 캐시, 역최적화가 순환하는 런타임 파이프라인이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로그램 시작 -> 바이트코드 해석 -> 호출 카운터 증가
  -> 임계값 초과 -> 네이티브 코드 생성 -> 코드 캐시 실행
  -> 가정 실패 -> deoptimization -> 재해석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 바이트코드 로딩 및 인터프리터 실행 | class loading time |
| 2 | 메서드 호출·루프 반복 프로파일 수집 | invocation/backedge counter |
| 3 | hot method 컴파일 및 인라이닝 | compilation count, tier level |
| 4 | 코드 캐시 실행 및 가정 검증 | deopt count, code cache usage |

> 요약: JIT은 실행 빈도 기반으로 컴파일 대상을 좁히고, 가정이 깨지면 역최적화로 실행 정확성을 보존한다.

---

## Ⅳ. 특징

| 구분 | 인터프리터 | JIT | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 시작 시간 | 즉시 실행 | 컴파일 전 warm-up 필요 | cold start 1~10초 가능 |
| 최적화 정보 | 정적 정보 제한 | 실제 타입·분기 정보 활용 | profile guided optimization |
| 메모리 | 코드 캐시 없음 | 코드 캐시·메타데이터 사용 | code cache 128~512MB |
| 운영 영향 | 예측 가능 | 컴파일 스파이크 발생 가능 | p95/p99 latency 관측 |

> 요약: JIT은 장시간 실행 서버에서 유리한 구조이나 cold start와 코드 캐시를 운영 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| AOT | 배포 전 네이티브 생성 | 실행 중 네이티브 생성 | cold start 500ms 이하 필요 시 AOT |
| 인터프리터 | 해석 비용 지속 | 핫스팟만 컴파일 | 반복 실행 비율 70% 이상인 서버 |
| 컨테이너 | 시작 시간 민감 | warm-up 필요 | readiness probe와 pre-warm 적용 |

> 요약: JIT은 반복 호출이 많은 장수 프로세스에 적합하고, 짧은 실행 함수는 AOT 또는 인터프리터가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| cold start 지연 | 초기 해석·컴파일 비용 | CDS, pre-warm, AOT 검토 | startup time, readiness time |
| 지연 스파이크 | JIT 컴파일 CPU 점유 | tiered level 조정, compilation thread 제한 | p99 latency, CPU steal |
| 코드 캐시 고갈 | 동적 생성 코드 증가 | code cache sizing, class unloading | code cache used percent |

> 요약: JIT 운영 리스크는 시작 시간, 지연 스파이크, 코드 캐시 고갈로 구분해 대응한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| warm-up | 배포 후 3분 내 p95 목표 도달 | load test, APM |
| 컴파일 상태 | deopt rate 1% 이하 | JVM JFR, perf event |
| 메모리 | code cache 사용률 80% 이하 | runtime metric, alert |

> 요약: JIT 적용 성공은 warm-up 시간, deoptimization 비율, 코드 캐시 사용률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. JVM 서비스는 JFR로 compilation time, deopt count, code cache 사용률을 수집하고 배포 전 부하 테스트에 반영함.
2. Kubernetes 배포는 startup probe와 readiness probe를 분리하고, pre-warm 트래픽으로 p95 지연 목표 도달 후 라우팅함.
3. 서버리스·CLI는 GraalVM Native Image, ReadyToRun, AOT를 검토해 cold start 500ms 이하 요구를 충족함.

**결론 (2줄):**
- 기술사 판단: 반복 실행 서버는 JIT, 짧은 수명 워크로드는 AOT 또는 인터프리터 중심으로 선택.
- 향후 방향: tiered JIT, profile guided AOT, CRaC 같은 체크포인트 복원 기술이 결합되는 방향임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "JIT을 설명하시오" | hot method 탐지와 코드 캐시 흐름 | 인터프리터·AOT 대비 특징 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "비교하시오" | warm-up, deopt, code cache 관측 흐름 | cold start, p99 지연, 메모리 리스크 |

> 요약: 설명형은 런타임 구조, 운영형은 warm-up과 관측 지표 중심으로 전환한다.
