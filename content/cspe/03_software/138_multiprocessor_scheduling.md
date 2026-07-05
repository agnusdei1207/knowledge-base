---
title: 다중 프로세서 스케줄링 (Multiprocessor Scheduling)
date: 2026-07-05
tags: [cspe-software]
weight: 138
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 여러 개의 CPU/코어가 존재하는 환경에서 프로세스를 효율적으로 배분하는 기법 |
| 필요성 | 처리량(Throughput) 극대화, 응답 시간 단축 및 부하 분산(Load Balancing) |
| 출제 의도 | 대칭형(SMP) vs 비대칭형, 친화도(Affinity), 부하 이동성 이해 |

## Ⅱ. 구성요소
```text
[ Global Queue ] vs [ Local Queues ]
   +-----+            +-----+     +-----+
   | Q 1 |            | Q 1 |     | Q 2 |
   +-----+            +-----+     +-----+
   /  |  \               |           |
[P1] [P2] [P3]         [CPU1]      [CPU2]
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| SMP | 모든 프로세서가 대등하게 스케줄링 및 I/O 수행 | 평등한 팀 구조 |
| Processor Affinity | 프로세스를 특정 코어에서 계속 실행하려는 성향 | 단골 손님 |
| Load Balancing | 코어 간 작업량을 균등하게 유지하는 기능 | 업무 재배분 |
> 요약: 공유 큐는 동기화 오버헤드가 크고, 개별 큐는 부하 불균형 위험이 있음.

## Ⅲ. 절차
```text
Process Creation -> Assign to Queue -> Core Selection (Affinity/Load)
      ^                                         |
      +--- (Push/Pull Migration) <--- Check Balance <---+
```
1. 큐 할당: 생성된 프로세스를 전역 큐 또는 특정 코어의 로컬 큐에 배정.
2. 코어 선택: 캐시 효율성을 위해 이전에 실행됐던 코어(Affinity) 우선 고려.
3. 부하 모니터링: 커널이 주기적으로 각 코어의 Ready Queue 길이를 체크.
4. 부하 재분배: 유휴 코어가 바쁜 코어의 작업을 가져오거나(Pull) 커널이 보냄(Push).
> 요약: 캐시 지역성과 공정성 사이의 균형을 맞추는 것이 핵심임.

## Ⅳ. 문제점
- 공유 자원에 대한 락(Lock) 경쟁으로 인한 스케줄러 성능 저하 및 병목.
- 프로세스 이동 시 캐시 미스(Cache Miss) 발생으로 인한 개별 성능 하락.

## Ⅴ. 개선방안
- 하이퍼스레딩 지원 및 캐시 계층 구조를 고려한 계층적 스케줄링 적용.
- NUMA(Non-Uniform Memory Access) 인지 스케줄링으로 원격 메모리 참조 최소화.

## Ⅵ. 전망
- 이기종 코어 스케줄링: Big-LITTLE(ARM) 등 성능/전력 효율 특화 배치 중요성 증대.
- AI 가속기 통합: CPU-NPU 간 워크로드 자동 분산 및 예측 스케줄링 진화.
