---
title: "명령어 집합 — RISC vs CISC (ISA RISC CISC)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 3
extra:
  question_no: "003"
  exam_status: "기출"
  exam_history: "124회"
---

## 미리 알고가기

- ISA는 하드웨어와 소프트웨어 사이의 실행 계약임
- RISC는 단순한 고정 길이 명령어를, CISC는 복합 가변 길이 명령어를 지향함
- 현대 CPU는 외부 ISA와 내부 실행 구조가 완전히 일치하지 않을 수 있음

## Ⅰ. 개요

- **정의/개념**: RISC와 CISC는 명령어 집합 구조를 나누는 방식으로, RISC는 단순 명령어와 규칙적 실행을, CISC는 복합 명령어와 높은 코드 밀도를 중시함
- **배경/필요성**: ISA 선택은 명령어 복잡도, 코드 밀도, 해독 비용, 파이프라인 설계가 워크로드에 맞는지 판단하는 문제임

## Ⅱ. 특징

- RISC는 고정 길이 명령어와 load/store 구조로 실행 흐름이 단순함
- CISC는 가변 길이와 복합 명령으로 코드 밀도와 호환성에 강함
- RISC는 규칙적 해독과 load/store 구조로 파이프라인 구성에 유리함
- CISC는 해독 복잡도와 내부 마이크로오퍼레이션 분해 비용이 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | RISC | CISC |
|:---|:---|:---|
| 명령어 길이 | 고정 길이 중심 | 가변 길이 중심 |
| 메모리 접근 | load/store 분리 | 메모리 직접 연산 가능 |
| 장점 | 규칙적 해독·파이프라인 구성 | 코드 밀도·생태계 호환성 |
| 대표 계열 | ARM, RISC-V | x86 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Opcode Format | 명령 길이와 해독 규칙을 정하며 RISC와 CISC 차이를 가장 직접적으로 드러냄 |
| Register Model | 피연산자 사용 방식과 compiler 스케줄링 범위를 결정함 |
| Decode Logic | 명령어를 내부 실행 단위로 바꾸며 CISC에서 부담이 더 큼 |
| Execution Path | 파이프라인과 u-op 변환 구조가 실행 지연과 전력 소모를 좌우함 |

```text
+-----------+     +-------------+     +---------------+
| ISA Format | --> | Decode Logic | --> | Execution Path |
+-----------+     +-------------+     +---------------+
      |
      v
+---------------+
| Register Model |
+---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 명령어 인출     | --> | 명령어 해독     | --> | 내부 실행 단위화  | --> | 연산 수행      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **명령어 인출**: ISA 형식에 맞는 명령어를 가져옴
2. **명령어 해독**: opcode와 피연산자 구조를 분석함
3. **내부 실행 단위화**: 필요 시 복합 명령을 u-op로 분해함
4. **연산 수행**: 실행 유닛이 실제 연산을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: CISC는 가변 길이 해독과 u-op 분해 부담이 커서 전력과 지연 비용이 증가함
   - 해결방안: u-op cache와 병렬 decoder를 적용하고 decode bandwidth와 perf per watt로 검증함
2. 문제: RISC는 단순 명령어 중심이라 같은 기능을 위해 코드 크기가 커짐
   - 해결방안: compressed instruction과 compiler optimization을 적용하고 binary size와 i-cache hit rate로 검증함
3. 문제: ISA 철학만 보고 선택하면 실제 워크로드와 생태계 제약을 놓칠 수 있음
   - 해결방안: workload fit과 toolchain maturity를 함께 평가하고 software porting effort와 benchmark score로 검증함

## Ⅶ. 적용 사례

- 모바일 프로세서에서는 RISC 계열을 선택하고, perf per watt와 i-cache hit rate로 검증함
- 레거시 서버 플랫폼에서는 CISC 계열을 유지하고, software porting effort와 single-thread performance로 검증함
- 신규 SoC 설계에서는 압축 명령과 toolchain을 함께 검토하고, binary size와 benchmark score로 검증함

## Ⅷ. 결론

RISC와 CISC의 실무 선택 기준은 명령어 수 자체가 아니라 파이프라인 구성, 코드 밀도, 생태계 호환성 중 무엇을 우선할지에 있음.

## 작성 근거(검토용)

- RISC/CISC를 속도 우열이 아니라 해독 규칙, 코드 밀도, 호환성의 선택 문제로 정리함
- 넓은 단어는 ISA 형식과 파이프라인 구성이라는 판단 축으로 좁힘
- 현대 CPU는 외부 ISA와 내부 u-op 실행이 다를 수 있으므로 구성요소에 decode와 execution path를 분리함
