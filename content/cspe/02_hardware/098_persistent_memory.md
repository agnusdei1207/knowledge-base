---
title: "퍼시스턴트 메모리 (Persistent Memory)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 98
extra:
  question_no: "098"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 퍼시스턴트 메모리는 바이트 주소 지정과 영속성을 함께 제공하는 메모리 계층임
- DAX는 page cache를 우회해 영속 메모리에 직접 접근하는 방식임
- flush와 fence는 데이터를 실제 영속 영역까지 반영하고 순서를 보장하는 메커니즘임

## Ⅰ. 개요

- **정의/개념**: 퍼시스턴트 메모리는 CPU가 바이트 단위로 직접 접근하면서 전원 장애 후에도 데이터가 유지되는 메모리와 스토리지 사이의 영속 계층임
- **배경/필요성**: DRAM 기반 인메모리 시스템은 재시작 복구가 느리고 SSD 기반 저장은 I/O 경로 오버헤드가 크므로, 빠른 접근과 빠른 복구를 동시에 원하는 업무에는 중간 계층이 필요함

## Ⅱ. 특징

- 블록 I/O 대신 load/store 방식으로 영속 데이터를 다룰 수 있음
- page cache 우회와 in-place 업데이트로 복구 시간을 줄일 수 있음
- 애플리케이션이 flush와 ordering을 직접 고려해야 하므로 프로그래밍 부담이 큼
- 메모리처럼 보이지만 데이터 보안과 폐기 정책은 저장장치 수준으로 다뤄야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | DRAM | SSD | Persistent Memory |
|:---|:---|:---|:---|
| 주소 지정 | 바이트 단위 | 블록 단위 | 바이트 단위 |
| 지속성 | 없음 | 있음 | 있음 |
| 접근 경로 | load/store | syscall과 block I/O | load/store 또는 DAX |
| 설계 부담 | 재적재 필요 | I/O 최적화 필요 | flush와 crash consistency 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Application | 영속 자료구조를 직접 다루므로 성능 이득과 동시에 일관성 설계 책임을 가짐 |
| PM Library | transaction과 allocator와 recovery helper를 제공해 복잡한 영속 구조 구현 부담을 줄임 |
| CPU Cache Control | flush와 fence가 실제 영속 시점과 쓰기 순서를 보장해 crash consistency의 핵심이 됨 |
| PM Namespace | OS가 노출한 영속 메모리 영역으로 데이터 생명주기 관리와 접근 정책의 기준점이 됨 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 영역 할당      | --> | 데이터 기록    | --> | 영속 보장      | --> | 장애 복구      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **영역 할당**: OS가 DAX 파일시스템 또는 namespace를 애플리케이션에 제공함
2. **데이터 기록**: 애플리케이션이 load/store로 영속 자료구조를 갱신함
3. **영속 보장**: flush와 fence로 기록 순서와 실제 반영 시점을 보장함
4. **장애 복구**: 로그와 checksum과 version 정보를 기반으로 일관된 상태를 복원함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 개발자가 flush와 ordering을 잘못 처리하면 장애 후 데이터 구조가 쉽게 손상될 수 있음
   - 해결방안: PMDK류 라이브러리와 transaction 패턴을 표준화하고 recovery consistency pass rate와 crash test defect count로 검증함
2. 문제: flush 비용과 NUMA 배치와 write amplification이 섞이면 성능 예측이 어려워질 수 있음
   - 해결방안: NUMA-aware allocation과 batching 최적화를 적용하고 p99 persist latency와 write amplification ratio로 검증함
3. 문제: 장비 폐기나 재할당 시 영속 데이터가 남아 있으면 잔존 정보 유출 위험이 커질 수 있음
   - 해결방안: namespace 암호화와 secure erase 절차를 운영하고 residual data scan result와 erase verification rate로 검증함

## Ⅶ. 적용 사례

- 인메모리 데이터베이스에서는 주요 자료구조를 퍼시스턴트 메모리에 배치하고, recovery time과 consistency pass rate로 결과를 확인함
- 파일시스템 메타데이터 최적화에서는 저널과 checkpoint를 영속 영역에 배치하고, p99 persist latency와 write amplification ratio로 결과를 확인함
- 장비 재할당 운영에서는 영속 영역의 암호화와 폐기 절차를 자동화하고, residual data scan result와 erase verification rate로 결과를 확인함

## Ⅷ. 결론

퍼시스턴트 메모리는 빠른 저장장치가 아니라 바이트 주소 지정과 영속성을 결합한 새로운 프로그래밍 모델이므로, 성능보다 crash consistency와 데이터 생명주기 통제가 먼저임.
