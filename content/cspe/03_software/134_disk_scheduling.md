---
title: 디스크 스케줄링 알고리즘 (Disk Scheduling)
date: 2026-07-05
tags: [cspe-software]
weight: 134
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 디스크 헤드의 이동 거리를 최소화하기 위해 I/O 요청 순서를 결정하는 기법 |
| 필요성 | 기계적 장치인 HDD의 탐색 시간(Seek Time) 최소화 및 처리량 극대화 |
| 출제 의도 | FCFS, SSTF, SCAN, C-SCAN 등 알고리즘별 특성 및 차이점 비교 |

## Ⅱ. 구성요소
```text
(Request Queue: 98, 183, 37, 122, 14, 124, 65, 67)
[ SSTF ]            [ SCAN ]            [ C-SCAN ]
Current: 53         Current: 53         Current: 53
-> 65 -> 67 -> 37   -> 37 -> 14 -> 0    -> 65 -> 67 ... -> 199
(Closest Next)      (Directional)       (Circular One-way)
```
| 알고리즘 | 설명 | 비유 |
|---|---|---|
| SSTF | 현재 헤드 위치에서 가장 가까운 요청 먼저 처리 | 가까운 배달지 우선 |
| SCAN | 한쪽 끝까지 이동하며 경로 상 모든 요청 처리 | 엘리베이터 방식 |
| C-SCAN | 한쪽 끝 도달 시 반대쪽으로 급복귀 후 재시작 | 편도 전용 셔틀 |
> 요약: SSTF는 기아 현상 가능성이 있으며, SCAN은 응답 시간의 편차가 존재함.

## Ⅲ. 절차
```text
I/O Request -> Insert into Queue -> Apply Scheduling Algo -> Move Head
      ^                                                     |
      +------ (Complete) ------ Select Next Request <-------+
```
1. 요청 대기: 여러 프로세스로부터 디스크 데이터 읽기/쓰기 요청이 Queue에 누적.
2. 알고리즘 선택: 시스템 특성에 최적화된 스케줄링 기법 가동 (예: 서버는 C-SCAN).
3. 헤드 이동: 선택된 트랙 번호로 디스크 암(Arm)을 물리적으로 이동.
4. 데이터 전송: 헤드가 해당 섹터에 도달하면 데이터 입출력 수행 후 다음 요청 처리.
> 요약: 기계적 구동부의 이동 동선을 최적화하여 시스템 전체 I/O 병목을 해소함.

## Ⅳ. 문제점
- SSTF의 경우 중심부 트랙 요청만 처리되고 외곽 요청은 무한정 대기할 수 있음.
- HDD 위주 알고리즘은 물리적 헤드가 없는 SSD(NAND) 환경에서 비효율적.

## Ⅴ. 개선방안
- N-Step SCAN 또는 F-SCAN을 사용하여 대기 중인 요청의 공정성 확보.
- SSD 환경에서는 NCQ(Native Command Queuing) 등 병렬 처리 최적화 적용.

## Ⅵ. 전망
- ZNS(Zoned Namespace): 데이터 성격별 구역화 관리를 통해 SSD 수명 및 성능 향상.
- 지능형 스케줄러: I/O 패턴을 학습하여 워크로드에 따른 가변 알고리즘 적용.
