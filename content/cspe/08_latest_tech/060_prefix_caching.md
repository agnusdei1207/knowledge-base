---
title: "Prefix Caching (접두 캐싱)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 60
extra:
  question_no: "060"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Prefix는 여러 요청이 공통으로 공유하는 프롬프트 앞부분을 의미함
- Prompt Caching은 동일 prefix의 prefill 결과를 재사용해 중복 계산을 줄이는 전략임
- Copy-on-Write는 공통 prefix를 공유하다가 분기 지점부터만 새 메모리를 할당하는 방식임

## Ⅰ. 개요

- **정의/개념**: Prefix Caching은 동일하거나 매우 유사한 프롬프트 앞부분의 KV cache를 식별해 다시 계산하지 않고 재사용함으로써 prefill 비용과 TTFT를 줄이는 서빙 캐시 기술임
- **배경/필요성**: 시스템 프롬프트와 공통 문서와 대화 이력처럼 반복적으로 등장하는 긴 prefix를 매 요청마다 다시 읽으면 비용과 지연이 커지므로, 공통 부분을 서버 차원에서 공유하는 캐시 구조가 필요함

## Ⅱ. 특징

- 긴 시스템 프롬프트와 반복 문서 질의에서 TTFT와 비용 절감 효과가 큼
- 캐시 적중 시 prefill 계산을 크게 줄여 장문맥 서비스 운영성을 높임
- 프롬프트 배열 순서와 구분자 설계가 캐시 적중률에 직접 영향을 줌
- 캐시 적중 실패와 TTL 정책이 성능 편차를 만들 수 있어 운영 정책이 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | 캐싱 없음 | Prefix Caching | Session Memory 재사용 |
|:---|:---|:---|:---|
| 재사용 범위 | 없음 | 공통 prefix | 특정 세션 이력 |
| TTFT 개선 | 없음 | 큼 | 중간 |
| 적용 조건 | 단순 요청 | 동일 prefix 반복 | 장기 대화 |
| 핵심 기술 | 없음 | block sharing, hash match | history management |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Prefix Matcher | 들어온 프롬프트의 앞부분이 기존 캐시와 동일한지 비교해 재사용 가능성을 판정함 |
| Cache Store | prefix별 KV cache와 메타데이터를 저장해 재사용 대상 풀을 형성함 |
| Sharing Manager | 동일 prefix를 여러 요청이 함께 참조하도록 연결하고 분기 시 Copy-on-Write를 수행함 |
| Eviction Policy | TTL, LRU 등으로 오래된 prefix cache를 정리해 메모리 예산을 유지함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| prefix 비교  | --> | 캐시 적중 판정 | --> | 캐시 공유    | --> | 분기/회수    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **prefix 비교**: 새 요청의 앞부분을 저장된 prefix 캐시와 비교해 동일 구간을 찾음
2. **캐시 적중 판정**: 해시나 트리 구조를 이용해 재사용 가능한 길이를 계산함
3. **캐시 공유**: 적중한 구간의 KV cache를 새 요청에 직접 연결해 prefill을 생략함
4. **분기 및 회수**: 이후 서로 다른 질의 부분부터는 별도 캐시를 만들고 만료 시 회수함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 프롬프트의 앞부분에 날짜나 세션 ID 같은 동적 값이 들어가면 의미는 같아도 캐시 적중이 깨져 효과가 크게 줄 수 있음
   - 해결방안: 고정 규칙을 prefix 앞에 두고 동적 값은 뒤로 미루며 cache hit rate와 TTFT로 구조 최적화를 검증함
2. 문제: 캐시를 오래 유지하면 메모리 사용량이 누적되고 TTL이 짧으면 재사용 이점이 급격히 줄어들 수 있음
   - 해결방안: workload별 TTL과 eviction 정책을 나누어 적용하고 memory usage와 cache reuse ratio로 정책 적합성을 검증함
3. 문제: 유사하지만 완전히 동일하지 않은 prefix를 무리하게 공유하면 잘못된 캐시 참조나 품질 문제가 발생할 수 있음
   - 해결방안: exact match 기준과 안전한 block sharing 규칙을 유지하고 cache correctness와 answer faithfulness로 안정성을 검증함

## Ⅶ. 적용 사례

- 기업용 챗봇: 공통 시스템 프롬프트와 매뉴얼을 재사용함, 확인 지표는 TTFT와 cache hit rate임
- 동일 문서 반복 질의: 긴 문서 기반 질의를 여러 번 처리함, 확인 지표는 요청당 비용과 prefill skip 비율임
- 멀티턴 대화: 이전 대화 이력을 prefix로 공유함, 확인 지표는 context reuse ratio와 latency임

## Ⅷ. 결론

Prefix Caching의 핵심은 캐시를 많이 쌓는 데 있지 않고 공통 프롬프트 구조를 의도적으로 설계해 높은 적중률로 prefill 비용을 줄이는 데 있음.
