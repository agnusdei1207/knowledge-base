---
title: 파이썬 GIL 및 메모리 관리 (Python GIL)
date: 2026-07-05
tags: ["cspe-software"]
weight: 162
---

## Ⅰ. 개요
- 정의: Python 인터프리터가 한 번에 하나의 쓰레드만 바이트코드를 실행하도록 보장하는 뮤텍스
- 배경: CPython의 레퍼런스 카운팅 메모리 관리 방식의 쓰레드 안전성 확보 목적
| 구분 | 내용 |
|------|------|
| 출제 의도 | 멀티코어 환경에서 파이썬의 성능 제약 및 이를 극복하기 위한 멀티프로세싱 활용 이해 |

## Ⅱ. 구성요소
  Thread A -> [ GIL Lock ] -> Interpreter Exec
  Thread B -> [ Wait...  ] -> (Context Switch)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Global Lock | 인터프리터 수준의 단일 잠금 장치 | 단일 통행권 |
| Bytecode | 파이썬 코드가 컴파일된 중간 형태 | 악보 |
| Ref Count | 객체 참조 횟수 기반 메모리 해제 | 인원 체크 |
> 요약: 단일 락 기반 구조로 인한 멀티쓰레드 병렬 실행 제약

## Ⅲ. 절차
  Acquire GIL -> Execute -> Release GIL -> Context Switch
1. Lock Check: 실행 전 GIL 획득 가능 여부 확인
2. Execution: 특정 시간(ticks) 또는 I/O 발생 전까지 실행
3. Release: 실행 후 GIL 반납 및 대기 쓰레드 깨움
4. Scheduling: 운영체제 스케줄러에 의한 쓰레드 교체
> 요약: 시분할 방식의 쓰레드 실행으로 인한 CPU Bound 작업 성능 한계

## Ⅳ. 문제점
- 멀티코어 CPU 환경에서도 CPU 집중 작업 시 단일 코어만 활용
- 쓰레드 간 GIL 획득 경쟁(Throttling)으로 인한 컨텍스트 스위칭 비용

## Ⅴ. 개선방안
- 멀티프로세싱(multiprocessing) 모듈 활용으로 독립된 GIL 환경 구성
- C-Extension 사용 시 GIL 해제 및 No-GIL 파이썬(PEP 703) 도입 검토

## Ⅵ. 전망
- PEP 703의 단계적 적용을 통해 락 없는(Lock-free) 멀티쓰레딩 공식 지원 및 AI/데이터 과학 성능 혁신 가속
