---
title: "PagedAttention"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 57
---

# 📖 【암기용】 개념 완전 이해

> 목적: PagedAttention을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: OS 가상메모리 페이징처럼 LLM KV Cache를 고정 크기 블록으로 나누어 관리하는 Attention 메모리 기법
- **왜 필요한가**: 요청마다 문맥 길이가 달라 KV Cache 공간이 조각나면 GPU 메모리가 남아도 새 요청을 받지 못함.
- **핵심 직관**: 긴 공책을 통째로 빌려주는 대신, 필요한 만큼 낱장 페이지를 배정하고 페이지 번호표로 연결하는 방식임.

## 깊이 이해
- **배경·문제의식**: 기존 KV Cache는 세션별 연속 메모리를 크게 잡아 내부·외부 단편화가 발생함. 동시 요청이 많은 LLM 서빙에서는 메모리 낭비가 곧 처리량 저하로 이어짐.
- **작동 원리**: 토큰의 KV를 물리 블록에 나누어 저장하고, 논리 블록 테이블이 토큰 순서와 물리 위치를 매핑함. Attention 커널은 블록 테이블을 따라 필요한 KV만 읽음.
- **비유**: 도서관 책장을 사람별로 통째 배정하지 않고, 빈 칸마다 책을 꽂은 뒤 목록표로 위치를 찾는 것과 같음.
- **구체 예시**: vLLM은 PagedAttention으로 KV Cache 낭비를 줄여 동일 GPU에서 동시 요청 처리량을 높이는 구조를 제공함.
- **흔한 오해·주의점**: PagedAttention은 모델 정확도를 높이는 기법이 아니라 메모리 배치와 서빙 처리량 최적화 기법임.

## 연결 개념
- KV Cache — PagedAttention이 관리하는 대상
- vLLM — PagedAttention을 대표적으로 구현한 서빙 엔진
- Continuous Batching — 동적 배치와 함께 처리량을 높임


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PagedAttention은 KV Cache를 페이지 블록으로 분할·매핑하여 GPU 메모리 단편화를 줄이는 LLM 서빙 기법임.
> 2. **가치**: 가변 길이 요청의 KV 메모리 낭비를 낮춰 동일 GPU에서 더 많은 동시 세션을 처리함.
> 3. **판단 포인트**: block size, block table, cache eviction, attention kernel 지원 여부가 처리량을 좌우함.


## Ⅰ. 개요 및 필요성

- 개요: KV Cache 페이지 관리 기법
- 배경: LLM 서빙은 요청마다 context/output 길이가 달라 GPU 메모리 단편화와 preemption 비용이 발생함.
- 필요성: fixed-size block, block table, copy-on-write로 KV 메모리 낭비와 동시성 한계를 관리해야 함.


## Ⅱ. 구조 및 구성요소

```text
Logical Token Sequence

Block Table -> Physical KV Blocks
                  [B0][B1][B2][B3][Bn]

Attention Kernel reads mapped blocks
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Logical Block | 토큰 순서 기준 KV 구간 | 세션별 논리 주소 |
| Physical Block | GPU 메모리 실제 KV 저장소 | 고정 크기 페이지 |
| Block Table | 논리->물리 매핑 | OS page table 유사 |
| Attention Kernel | 매핑된 block을 읽어 연산 | 커널 최적화 필요 |

> 요약: PagedAttention은 논리 토큰 순서와 물리 KV 저장 위치를 분리해 가변 길이 세션을 블록 단위로 수용함.


## Ⅲ. 동작원리 및 흐름도

```text
요청 도착 -> KV block 할당 -> block table 갱신
    -> decode 중 block append -> attention 연산 -> 종료 시 block 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청별 초기 KV block 할당 | free block 수 |
| 2 | 토큰 증가 시 block append | block utilization |
| 3 | Attention kernel이 table 기반 KV 조회 | TPOT, GPU memory bandwidth |
| 4 | 요청 종료·중단 시 block 반환 | fragmentation, OOM 건수 |

> 요약: KV를 연속 영역이 아니라 블록 목록으로 관리해 세션 길이 변화에도 메모리를 회수·재사용함.


## Ⅳ. 특징

| 구분 | 연속 KV Cache | PagedAttention | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 메모리 배치 | 세션별 연속 공간 | 고정 블록 분산 배치 | block table 필요 |
| 단편화 | 길이 편차에 취약 | block 단위 회수 | OOM 감소 |
| 처리량 | 동시 요청 증가 시 저하 | continuous batching과 결합 | req/s 개선 |
| 구현 복잡도 | 낮음 | attention kernel 수정 | vLLM 등 엔진 의존 |

> 요약: PagedAttention은 서빙 처리량을 높이는 메모리 가상화 기법이며, 엔진·커널 지원이 적용 전제임.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. vLLM 기반 서빙으로 PagedAttention을 적용하고, block utilization·OOM·req/s를 배포 전후 비교
2. max context/output 정책을 설정해 장문 요청의 block 점유 시간을 제한하고 대기열 지연을 통제
3. Prefix Caching·Continuous Batching과 결합해 공통 prefix와 동적 배치를 동시에 활용

**결론 (2줄):**
- 기술사 판단: 다중 사용자 LLM API는 PagedAttention 기반 엔진을 우선 검토하고, 단일 배치 분석은 단순 KV Cache로 충분함.
- 향후 방향: KV Cache 가상화는 장문맥·고동시성 LLM 서빙의 기본 런타임 기능으로 편입됨.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | block table 기반 KV 조회 흐름 | 연속 cache 대비 단편화 |
| 요구사항 명시형 | 설계하시오, 최적화하시오 | vLLM 적용·지표 측정 절차 | req/s·OOM·TPOT 기준 |

> 요약: 설명형은 메모리 페이징 원리, 설계형은 서빙 엔진 적용과 운영 지표 중심으로 목차를 전환함.
