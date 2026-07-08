---
title: "PagedAttention (페이지드 어텐션)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 57
extra:
  question_no: "057"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- PagedAttention은 KV cache를 고정 길이 블록으로 나누어 관리하는 메모리 가상화 기법임
- Block Table은 논리적 토큰 순서와 실제 물리 메모리 블록 위치를 매핑하는 구조임
- Fragmentation은 메모리가 남아 있어도 연속 공간 부족으로 할당 효율이 떨어지는 현상임

## Ⅰ. 개요

- **정의/개념**: PagedAttention은 KV cache를 연속 텐서로 고정 할당하지 않고 페이지 단위 블록으로 분해해 논리 주소와 물리 주소를 분리 관리함으로써 메모리 파편화를 줄이는 서빙 메모리 관리 기법임
- **배경/필요성**: 생성 길이를 미리 확정하기 어려운 LLM 서빙에서는 요청마다 최대 길이를 통째로 예약하면 VRAM 낭비가 커지므로, 운영체제의 가상 메모리처럼 필요한 만큼만 유연하게 메모리를 배정할 구조가 필요함

## Ⅱ. 특징

- 연속 메모리 강제를 없애 VRAM 파편화와 과도한 사전 예약을 줄임
- 요청 길이가 가변적인 챗봇, agent, batch serving 환경에서 메모리 효율이 높음
- Prefix Caching, Copy-on-Write, Continuous Batching과 결합할 때 효과가 커짐
- 커널 구현이 복잡해 단순 텐서 처리보다 시스템 소프트웨어 의존도가 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | 연속 할당 방식 | PagedAttention | Prefix Caching 결합형 |
|:---|:---|:---|:---|
| 메모리 배치 | 연속 공간 필요 | 비연속 블록 허용 | 비연속 블록 + 공유 |
| 파편화 대응 | 약함 | 강함 | 매우 강함 |
| 재사용성 | 낮음 | 중간 | 높음 |
| 대표 활용 | 단순 생성 환경 | vLLM 핵심 | 반복 프롬프트 서비스 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Logical Block | 토큰 순서 기준으로 쪼갠 논리적 캐시 단위이며 요청별 문맥 흐름을 표현함 |
| Physical Page | GPU 메모리에 실제 배치되는 고정 크기 블록으로 여러 요청 사이에 동적으로 재배정됨 |
| Block Table | 논리 블록이 어떤 물리 페이지를 참조하는지 기록해 불연속 메모리 접근을 가능하게 함 |
| Page Allocator | 페이지 할당, 회수, 공유, Copy-on-Write를 관리해 실제 메모리 효율을 좌우함 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| Logical Block    | --> | Physical Page    | --> | Block Table      | --> | Page Allocator   |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 캐시 분할    | --> | 페이지 할당  | --> | 블록 매핑    | --> | 공유/회수    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **캐시 분할**: KV cache를 고정 크기 논리 블록으로 나누어 토큰 증가에 따라 확장 가능하게 만듦
2. **페이지 할당**: 새 블록이 필요할 때 GPU 메모리의 가용 물리 페이지를 동적으로 배정함
3. **블록 매핑**: Block Table을 통해 논리 블록 순서와 실제 물리 페이지 위치를 연결함
4. **공유 및 회수**: 요청 종료 시 페이지를 회수하고 공통 prefix는 공유 또는 Copy-on-Write로 재사용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 페이지 단위 관리가 정교하지 않으면 블록 매핑 오버헤드와 커널 복잡성 때문에 실제 속도 이점이 줄어들 수 있음
   - 해결방안: block size와 allocator 정책을 튜닝하고 memory utilization과 scheduler overhead로 효율을 검증함
2. 문제: 공통 prefix를 공유하는 환경에서 page reference 관리가 어긋나면 잘못된 캐시 참조나 복제 비용 증가가 발생할 수 있음
   - 해결방안: reference counting과 Copy-on-Write 검증을 적용하고 cache hit rate와 duplication ratio로 안전성을 검증함
3. 문제: VRAM이 부족할 때 무분별한 페이지 확장은 swap, preemption을 유발해 TTFT와 TPOT을 모두 악화시킬 수 있음
   - 해결방안: 메모리 watermark와 eviction 정책을 설정하고 p95 latency와 OOM rate로 운영 적정성을 검증함

## Ⅶ. 적용 사례

- vLLM 기반 챗봇 서빙: 다양한 길이 요청을 효율적으로 수용함, 확인 지표는 memory utilization과 throughput임
- Prefix Caching 서비스: 공통 시스템 프롬프트를 블록 공유로 재사용함, 확인 지표는 cache hit rate와 TTFT임
- 복수 샘플 생성: beam search나 multi-response 생성 시 공통 prefix를 공유함, 확인 지표는 VRAM saving과 latency임

## Ⅷ. 결론

PagedAttention의 본질은 attention 수식을 바꾸는 데 있지 않고 운영체제식 메모리 가상화를 LLM 캐시에 적용해 실제 서빙 효율을 크게 높이는 시스템 설계에 있음.
