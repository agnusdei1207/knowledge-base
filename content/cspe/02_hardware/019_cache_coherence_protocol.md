---
title: "캐시 일관성 프로토콜 — MESI·MOESI (Cache Coherence Protocol)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 19
extra:
  question_no: "019"
  exam_status: "기출"
  exam_history: "123회, 135회"
---

## 미리 알고가기

- 캐시 일관성은 여러 코어가 같은 데이터의 최신성을 맞추는 규칙임
- MESI는 M/E/S/I 네 상태를, MOESI는 Owned 상태를 추가로 사용함
- 프로토콜 효율은 공유 패턴과 메시지 비용에 좌우됨

## Ⅰ. 개요

- **정의/개념**: 캐시 일관성 프로토콜은 멀티코어 환경에서 각 코어 캐시에 존재하는 동일 주소 데이터의 상태를 관리해 모든 코어가 의미적으로 일관된 값을 보도록 하는 하드웨어 통신 규약임
- **배경/필요성**: 각 코어가 private cache를 가지면 한 코어가 수정한 데이터와 다른 코어가 읽는 데이터가 달라질 수 있으므로, 상태 전이와 무효화 규칙이 반드시 필요함

## Ⅱ. 특징

- MESI는 단순하고 널리 쓰이는 기본 일관성 모델임
- MOESI는 Owned 상태를 추가해 메모리 쓰기 없이 dirty data 공유를 줄일 수 있음
- 일관성 유지에는 invalidate와 snoop 메시지 비용이 수반됨
- false sharing이 심하면 프로토콜 자체보다 데이터 배치가 더 큰 병목이 될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | MESI | MOESI |
|:---|:---|:---|
| 상태 수 | 4개 | 5개 |
| 추가 상태 | 없음 | Owned |
| 강점 | 구현 단순 | 메모리 트래픽 절감 |
| 한계 | dirty 공유 비효율 | 상태 전이 복잡도 증가 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cache Line State | M/E/S/I/O 상태가 현재 데이터 소유와 공유 수준을 나타냄 |
| Snoop or Directory Signal | 다른 코어 접근을 감시하거나 통지해 상태 전이를 유도함 |
| Invalidation Logic | 쓰기 의도를 가진 코어가 다른 사본을 무효화해 최신본을 확보함 |
| Data Transfer Path | 필요 시 캐시 간 또는 메모리와 캐시 간 최신 데이터를 전달함 |

```text
+------------------+     +--------------------+     +--------------------+
| Cache Line State | --> | Invalidation Logic | --> | Data Transfer Path |
+------------------+     +--------------------+     +--------------------+
            |
            v
   +----------------------+
   | Snoop/Directory Sig  |
   +----------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 공유 상태 감지    | --> | 상태 전이 결정    | --> | 무효화/전달 수행  | --> | 최신성 확정     |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **공유 상태 감지**: 다른 캐시에 사본 존재 여부를 확인함
2. **상태 전이 결정**: 읽기와 쓰기 의도에 맞는 상태를 정함
3. **무효화 또는 전달 수행**: 필요한 메시지와 데이터 전송을 처리함
4. **최신성 확정**: 각 캐시가 일관된 상태로 수렴함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 코어 수와 공유 데이터가 늘면 invalidate와 snoop 메시지가 급증해 버스와 네트워크 병목이 커질 수 있음
   - 해결방안: directory 기반 제어와 snoop filter를 적용하고 coherence traffic ratio와 bus utilization로 검증함
2. 문제: false sharing이 심하면 실제 공유하지 않는 변수도 반복 무효화되어 성능이 떨어질 수 있음
   - 해결방안: cache line aware padding을 적용하고 false sharing miss ratio와 write invalidate rate로 검증함
3. 문제: MOESI처럼 상태가 늘어나면 구현과 검증 복잡도가 커져 corner case 오류가 생길 수 있음
   - 해결방안: formal state verification을 수행하고 protocol bug count와 validation coverage로 검증함

## Ⅶ. 적용 사례

- 다코어 서버에서는 디렉터리 제어를 적용하고 확인 지표는 coherence traffic ratio와 bus utilization임
- 고성능 병렬 코드에서는 패딩을 적용하고 확인 지표는 false sharing miss ratio와 write invalidate rate임
- 프로토콜 검증 환경에서는 상태 검증을 강화하고 확인 지표는 protocol bug count와 validation coverage임

## Ⅷ. 결론

캐시 일관성 프로토콜의 핵심은 상태 이름을 외우는 데 있지 않고 최신 데이터를 최소한의 통신 비용으로 공유하는 구조를 설계하는 데 있음.
