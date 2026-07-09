---
title: "비순서 실행·레지스터 리네이밍 (Out-of-Order Execution Register Renaming)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 12
extra:
  question_no: "012"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- 비순서 실행은 준비된 명령부터 먼저 실행하는 구조임
- 레지스터 리네이밍은 WAR·WAW 같은 가짜 의존성을 제거함
- 결과 확정은 여전히 프로그램 순서를 유지해야 함

## Ⅰ. 개요

- **정의/개념**: 비순서 실행은 프로그램 순서와 다르게 준비된 명령어를 먼저 실행해 실행 유닛 유휴 시간을 줄이는 기술이고, 레지스터 리네이밍은 논리 레지스터 이름을 물리 레지스터로 매핑해 가짜 의존성을 제거하는 메커니즘임
- **배경/필요성**: 순차 실행에서는 앞선 명령이 메모리 지연에 묶이면 뒤의 독립 명령도 함께 멈추므로, 단일 스레드 성능을 높이려면 의존성 분석과 순서 재배치가 필요함

## Ⅱ. 특징

- 준비된 연산을 먼저 실행해 실행 유닛 활용률을 높임
- 리네이밍으로 WAR와 WAW를 제거해 ILP를 확장함
- 결과는 ROB를 통해 순차적으로 commit되어 정합성을 유지함
- 하드웨어 구조와 전력 비용이 크게 증가함

## Ⅲ. 종류 및 비교

| 판단 기준 | In-order | Out-of-Order |
|:---|:---|:---|
| 실행 순서 | 프로그램 순서 고정 | 준비된 순서 중심 |
| 장점 | 단순성과 예측 가능성 | 대기 중인 독립 명령 실행 |
| 한계 | 긴 대기 전파 | 회로 복잡도와 전력 증가 |
| 대표 기술 | 간단한 파이프라인 | rename, RS, ROB |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Register Alias Table | 논리 레지스터를 물리 레지스터로 매핑해 이름 충돌을 제거함 |
| Reservation Station | 피연산자가 준비될 때까지 명령어를 대기시키고 준비 즉시 발행함 |
| Physical Register File | 실제 연산 결과를 저장하며 rename 이후 데이터 저장의 기반이 됨 |
| Reorder Buffer | 비순서로 끝난 결과를 프로그램 순서대로 retire해 precise exception과 상태 일관성을 유지함 |

```text
+---------------------+     +-------------------+     +----------------------+
| Register Alias Table | --> | Reservation Station | --> | Physical Register File |
+---------------------+     +-------------------+     +----------------------+
                                                     |
                                                     v
                                              +---------------+
                                              | Reorder Buffer |
                                              +---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| rename 수행     | --> | 준비 상태 대기    | --> | 비순서 실행      | --> | 순차 commit   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **rename 수행**: 논리 레지스터를 물리 레지스터에 매핑함
2. **준비 상태 대기**: 피연산자 도착까지 RS에서 기다림
3. **비순서 실행**: 준비된 명령부터 실행 유닛에 발행함
4. **순차 commit**: ROB가 원래 순서대로 결과를 확정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 명령어 윈도우와 리네이밍 구조가 커질수록 회로 면적과 전력 소모가 증가함
   - 해결방안: window size와 rename depth를 workload에 맞춰 조정하고 area efficiency와 perf per watt로 검증함
2. 문제: 복잡한 투기 실행 구조는 보안 취약점과 예외 복구 부담을 동시에 키울 수 있음
   - 해결방안: speculation control과 precise exception 검증 범위를 넓히고 rollback latency와 security exposure count로 검증함
3. 문제: 메모리 의존성 예측이 틀리면 비순서 이점보다 재실행 비용이 더 커짐
   - 해결방안: memory dependence prediction을 튜닝하고 replay rate와 load-store conflict ratio로 검증함

## Ⅶ. 적용 사례

- 서버 CPU에서는 window 크기를 조정하고, area cost와 perf per watt로 검증함
- 보안 민감 플랫폼에서는 투기 제어 정책을 적용하고, rollback latency와 security exposure count로 검증함
- 메모리 병목 워크로드에서는 의존성 예측을 조정하고, replay rate와 load-store conflict ratio로 검증함

## Ⅷ. 결론

비순서 실행과 레지스터 리네이밍의 판단 기준은 순서를 무너뜨리는 것이 아니라 진짜 의존성만 남긴 채 하드웨어 유휴 시간을 줄이는 데 있음.

## 작성 근거(검토용)

- OoO와 리네이밍은 순서를 없애는 기술이 아니라 가짜 의존성을 제거하고 commit 순서를 보존하는 기술로 설명함
- 추상 표현은 precise exception과 상태 일관성 유지라는 구체 결과로 바꿈
- 적용 사례는 window 크기, rollback, replay처럼 구조 변화가 드러나는 지표로 검증하도록 정리함
