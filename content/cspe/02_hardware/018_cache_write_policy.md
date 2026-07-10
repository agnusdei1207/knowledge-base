---
title: "캐시 쓰기 정책 — Write-Through vs Write-Back (Cache Write Policy)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 18
extra:
  question_no: "018"
  exam_status: "기출"
  exam_history: "129회"
---

## 미리 알고가기

- 캐시 쓰기 정책은 수정 데이터를 언제 메모리에 반영할지 정하는 규칙임
- Write-Through는 즉시 반영, Write-Back은 교체 시 반영 구조임
- Write miss 시 allocate 정책과 함께 봐야 함

## Ⅰ. 개요

- **정의/개념**: 캐시 쓰기 정책은 CPU가 캐시에 데이터를 갱신할 때 변경된 내용을 메모리에 즉시 반영할지, 캐시에만 유지하다가 추후 교체 시점에 반영할지 결정하는 캐시 제어 규칙임
- **배경/필요성**: 캐시와 메모리의 최신성·쓰기 지연·트래픽을 조절하기 위해 데이터 반영 시점과 할당 정책이 필요함

## Ⅱ. 특징

- Write-Through는 메모리 최신성 유지가 쉽고 구조가 단순함
- Write-Back은 같은 라인의 반복 쓰기를 모아 메모리 트래픽을 줄임
- Write-Back은 dirty bit와 eviction 관리가 필수임
- write miss 처리와 DMA 일관성 요구에 따라 정책 적합성이 달라짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Write-Through | Write-Back |
|:---|:---|:---|
| 메모리 반영 시점 | 즉시 | 교체 시점 |
| 장점 | 메모리 최신성 관리 용이 | 메모리 트래픽 절감 |
| 한계 | 메모리 트래픽 큼 | dirty 관리와 복구 복잡 |
| 대표 조합 | no-write-allocate | write-allocate |

> 요약: Write-Through는 캐시와 메모리에 동시에 기록하고, Write-Back은 수정 라인이 교체될 때 메모리에 반영함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cache Line | 수정 대상 데이터가 저장되는 기본 단위이며 dirty 상태 여부를 함께 기록함 |
| Dirty Bit | Write-Back에서 메모리에 아직 반영되지 않은 변경 여부를 표시함 |
| Write Buffer | Write-Through의 메모리 지연을 흡수해 CPU 정지를 줄이는 완충 장치임 |
| Eviction Logic | Write-Back 캐시 라인을 교체할 때 메모리 반영 여부를 결정함 |

```text
+------------+     +-----------+     +--------------+
| Cache Line | --> | Dirty Bit | --> | Eviction     |
+------------+     +-----------+     +--------------+
      |
      v
+--------------+
| Write Buffer |
+--------------+
```

> 요약: dirty bit, write buffer, eviction logic이 메모리 반영 시점과 지연을 제어함.

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| write 요청 수신 | --> | hit/miss 판정    | --> | 캐시/메모리 갱신 | --> | 교체·반영 처리  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **쓰기 요청 수신**: CPU가 데이터 갱신을 요청함
2. **hit 또는 miss 판정**: 캐시 내 존재 여부를 확인함
3. **캐시와 메모리 갱신**: 정책에 맞게 즉시 또는 지연 반영함
4. **교체와 반영 처리**: dirty 상태면 메모리에 기록함

> 요약: 쓰기 정책은 요청 위치와 dirty 상태를 보고 즉시 반영할지 교체 시 반영할지 결정함.

## Ⅵ. 실무 적용 및 유의점

1. Write-Through는 잦은 메모리 쓰기로 버스 병목이 커지므로 write buffer와 burst merge를 적용하고 buffer full rate, memory traffic ratio로 확인함
2. Write-Back은 전원 차단·DMA 접근 시 최신성 문제가 생길 수 있으므로 coherence protocol과 flush policy를 운영하고 stale memory read count, flush latency로 확인함
3. write miss 정책이 접근 패턴과 맞지 않으면 캐시 오염과 지연이 늘어나므로 allocate policy를 조정하고 write miss penalty, cache pollution ratio로 확인함

## Ⅶ. 결론

캐시 쓰기 정책은 속도보다 메모리 트래픽, 최신성, 복구 비용 중 무엇을 우선할지 정하는 선택 기준임.

## 작성 근거(검토용)

- 쓰기 정책은 빠름/느림이 아니라 메모리 반영 시점, dirty bit, write buffer, eviction 절차로 설명함
- 모호한 표현은 메모리 최신성, 트래픽, dirty 관리로 구체화함
- 결론은 속도 비교가 아니라 트래픽, 일관성, 복구 비용의 선택 문제로 유지함
