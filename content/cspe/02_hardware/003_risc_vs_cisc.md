---
title: ISA — RISC vs CISC (Instruction Set Architecture)
date: 2026-07-05
tags: ["cspe-hardware"]
weight: 3
---

## Ⅰ. 개요
- 정의: 소프트웨어와 하드웨어 사이의 인터페이스인 명령어 집합 구조
- 배경: 프로그래밍 편의성(CISC)과 하드웨어 효율성(RISC) 간의 설계 철학 차이
- 출제 의도: 명령어 복잡도에 따른 프로세서 성능 지표(CPI, 사이클 타임) 영향 분석

## Ⅱ. 구성요소
- ASCII 구조도
  [CISC]                     [RISC]
  +------------------+       +------------------+
  | Complex Inst     |       | Simple Inst      |
  | (Multi-Cycle)    |       | (Single-Cycle)   |
  +--------+---------+       +--------+---------+
           | Microcode                | Hardwired
  +--------v---------+       +--------v---------+
  | Hardware Logic   |       | Hardware Logic   |
  +------------------+       +------------------+

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 명령어 길이 | CISC는 가변 길이, RISC는 고정 길이 | 문장 vs 단어 |
| 레지스터 | RISC는 다수의 범용 레지스터 사용 | 큰 창고 |
| 어드레싱 | CISC는 복합 주소 지정, RISC는 Load/Store 중심 | 배달 vs 직접 |
> 요약: CISC는 SW 편의성, RISC는 HW 파이프라이닝 효율에 최적화됨

## Ⅲ. 절차
- ASCII 흐름도
  CISC: [Read] -> [Micro-op 1] -> [Micro-op 2] -> [Write]
  RISC: [Fetch] -> [Decode] -> [Execute] -> [Mem] -> [WB]

- 4단계 설명
1. CISC 해석: 하나의 명령어를 여러 개의 마이크로 연산으로 분해
2. RISC 실행: 단순화된 명령어를 파이프라인 각 단계에서 즉시 실행
3. 컴파일러 역할: CISC는 단순 컴파일, RISC는 최적화 컴파일러 의존도 높음
4. 처리 방식: CISC는 명령어당 기능 극대화, RISC는 사이클당 명령어 수 극대화
> 요약: CISC는 하드웨어 내 마이크로코드로, RISC는 컴파일러 최적화로 처리함

## Ⅳ. 문제점
- CISC 복잡도: 하드웨어 설계가 복잡하여 전력 소모 및 발열 증가
- RISC 코드 밀도: 명령어 수가 많아져 코드 크기가 커지고 메모리 대역폭 점유

## Ⅴ. 개선방안
- (단기) CISC의 RISC화: x86처럼 외부 명령어는 CISC, 내부 연산은 RISC로 처리
- (중기) 압축 명령어: RISC-V C-extension 등을 통한 코드 밀도 개선
- (장기) 가변 길이 벡터 ISA: 데이터 특성에 따른 유연한 명령어 확장

## Ⅵ. 전망
- 로드맵: 모바일/IoT는 RISC(ARM/RISC-V) 주도, 서버/PC는 CISC(x86)와 RISC 혼용
- CSF: 전력 효율(PPA) 극대화 및 생태계(Toolchain) 확보가 시장 점유의 핵심임
