---
title: "컴퓨터 구조 핵심 트랙"
date: "2026-06-29"
tags:
  - "exam-cspe-computer-architecture"
  - "exam-cspe-track"
weight: 91
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컴퓨터 구조는 성능, 전력, 신뢰성의 물리적 한계를 설계 판단으로 바꾸는 시험의 기반 과목이다.
> 2. **가치**: 중앙처리장치(CPU), 메모리, 입출력(I/O) 병목을 설명할 수 있어야 시스템형 서술 문제의 골격이 잡힌다.
> 3. **판단 포인트**: 인공지능(AI) 가속기, 캐시 일관성, 하드웨어 보안까지 연결해야 컴퓨터시스템응용기술사 관점이 살아난다.

---

## Ⅰ. 과목 개요

- 총 노트 수: `804`
- 추천 핵심 키워드 목표 수: `250개`

## Ⅱ. 왜 시험 핵심인가

- 시스템 성능 저하 원인을 중앙처리장치(CPU), 캐시(Cache), 버스(Bus), 저장장치까지 구조적으로 설명할 수 있는 출발점이다.
- 운영체제, 데이터베이스, 네트워크의 병목 원인을 결국 하드웨어 자원 경쟁과 메모리 계층으로 환원해 설명하게 만든다.
- 서술형 답안에서 처리량(Throughput), 지연시간(Latency), 전력효율(Watt per Performance) 트레이드오프를 제시하기 좋다.
- 컴퓨터시스템응용기술사는 단순 이론보다 적용 판단을 보므로 멀티코어, 가속기, 신뢰성 설계를 묶어 쓰는 능력이 중요하다.

## Ⅲ. 우선 학습 챕터

- `03_architecture_basics_performance`
- `04_instruction_set_architecture`
- `05_control_unit_pipelining`
- `06_memory_hierarchy_cache`
- `07_virtual_memory_os_integration`
- `10_parallel_processing_architecture`
- `12_accelerators_ai_hardware`
- `14_hardware_security_trends`

## Ⅳ. 단답형 / 서술형 분리 포인트

- 단답형: ISA(Instruction Set Architecture), CPI(Clock Per Instruction), 캐시 사상, 파이프라인 해저드, 메모리 일관성 프로토콜 정의 구분
- 서술형: 병목 원인, 성능 개선 구조, 멀티코어 동기화 한계, 전력 대비 성능, 장애 대응 구조를 비교형으로 전개
- 답안 기준: "구조도 → 병목 → 개선기법 → 적용사례" 순서로 쓰면 채점 포인트가 빠르게 드러난다.

## Ⅴ. 최신 기술 동향 연결

- 인공지능(AI) 가속기: 신경망 처리장치(NPU), 고대역폭 메모리(HBM), 칩렛(Chiplet) 구조
- 데이터센터 서버: 데이터 처리 장치(DPU), 스마트 네트워크 인터페이스 카드(SmartNIC), 메모리 중심 컴퓨팅
- 보안: 기밀 컴퓨팅(Confidential Computing), 신뢰 실행 환경(TEE), 하드웨어 루트 오브 트러스트(Root of Trust)
- 전력/신뢰성: 저전력 설계, 열 설계 전력(TDP), 오류 정정 코드(ECC), RAS(Reliability Availability Serviceability)
