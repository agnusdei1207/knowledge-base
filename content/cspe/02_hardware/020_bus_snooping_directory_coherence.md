---
title: "버스 스누핑·디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 20
extra:
  question_no: "020"
  exam_status: "기출"
  exam_history: "123회"
---

## 미리 알고가기

- 버스 스누핑은 모든 캐시가 공용 버스를 감시하는 방식임
- 디렉터리 방식은 중앙 또는 분산 디렉터리가 캐시 상태를 관리함
- 코어 수가 적으면 스누핑, 많아지면 디렉터리 쪽이 유리해짐

## Ⅰ. 개요

- **정의/개념**: 버스 스누핑과 디렉터리 기반 일관성은 캐시 일관성 프로토콜을 실제 하드웨어 통신 구조로 구현하는 두 방식으로, 스누핑은 모든 캐시가 방송 메시지를 직접 감시하고 디렉터리는 특정 관리자 구조가 소유자와 상태를 추적함
- **배경/필요성**: 소규모 멀티코어에서는 방송형 제어가 단순하고 빠르지만, 코어 수가 커지면 불필요한 메시지가 급증하므로 시스템 규모에 맞는 일관성 통신 구조를 선택해야 함

## Ⅱ. 특징

- 스누핑은 구현이 단순하고 짧은 지연에 유리함
- 디렉터리는 필요한 노드에만 메시지를 보내 확장성이 높음
- 스누핑은 코어 수 증가 시 버스 병목이 심해짐
- 디렉터리는 메모리 오버헤드와 조회 지연이 추가됨

## Ⅲ. 종류 및 비교

| 판단 기준 | 버스 스누핑 | 디렉터리 방식 |
|:---|:---|:---|
| 통신 방식 | broadcast | targeted message |
| 강점 | 단순성과 짧은 지연 | 확장성과 메시지 효율 |
| 한계 | 대규모 확장 취약 | 메타데이터와 조회 비용 |
| 적합 환경 | 소규모 칩 내 코어 | 대규모 many-core·NUMA |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Shared Bus or Fabric | 스누핑에서는 모든 코어가 감시하는 공용 통신 경로가 됨 |
| Snoop Logic | 각 캐시가 버스 주소를 비교해 자신의 상태를 갱신함 |
| Directory Entry | 특정 라인의 소유자와 공유자 목록을 기록해 targeted invalidation을 가능하게 함 |
| Interconnect Message Path | 디렉터리 구조에서 필요한 코어에만 invalidate와 data 메시지를 전달함 |

```text
+---------------+     +-------------+     +-------------------+
| Shared Bus    | --> | Snoop Logic | --> | Cache State Update |
+---------------+     +-------------+     +-------------------+

+----------------+     +---------------------+     +----------------------+
| Directory Entry | --> | Interconnect Message | --> | Target Cache Update |
+----------------+     +---------------------+     +----------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 접근 요청 발생   | --> | 소유자/공유자 확인 | --> | broadcast 또는 target | --> | 상태 갱신      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **접근 요청 발생**: 한 코어가 읽기 또는 쓰기를 요청함
2. **소유자와 공유자 확인**: 버스 감시 또는 디렉터리 조회를 수행함
3. **broadcast 또는 target 메시지 수행**: invalidate와 data 전달을 처리함
4. **상태 갱신**: 관련 캐시 상태를 최신으로 맞춤

## Ⅵ. 문제점 및 해결 방안

1. 문제: 스누핑은 코어 수가 늘수록 불필요한 broadcast 메시지로 대역폭 효율이 급격히 떨어질 수 있음
   - 해결방안: snoop filter와 계층형 버스를 적용하고 broadcast traffic ratio와 effective bus bandwidth로 검증함
2. 문제: 디렉터리 방식은 상태 정보를 저장하는 메타데이터 오버헤드가 커질 수 있음
   - 해결방안: sparse directory와 compression을 적용하고 directory overhead ratio와 metadata hit rate로 검증함
3. 문제: 디렉터리 조회 지연이 커지면 일관성 효율은 좋아도 단일 접근 지연이 증가할 수 있음
   - 해결방안: distributed directory와 local caching을 적용하고 directory lookup latency와 coherence completion time로 검증함

## Ⅶ. 적용 사례

- 소규모 멀티코어 CPU에서는 필터링된 스누핑을 적용하고 확인 지표는 broadcast traffic ratio와 effective bus bandwidth임
- NUMA 서버에서는 희소 디렉터리를 적용하고 확인 지표는 directory overhead ratio와 metadata hit rate임
- 칩렛 기반 시스템에서는 분산 디렉터리를 적용하고 확인 지표는 directory lookup latency와 coherence completion time임

## Ⅷ. 결론

스누핑과 디렉터리의 선택은 어느 방식이 더 고급인지가 아니라 코어 수와 통신 비용에 맞춰 최신성 유지 비용을 어떻게 최소화할지의 문제임.
