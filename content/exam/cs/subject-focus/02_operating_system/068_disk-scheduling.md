---
title: "디스크 스케줄링 (Disk Scheduling, FCFS/SSTF/SCAN/C-SCAN/LOOK)"
date: "2026-06-30"
weight: 68
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 다수의 디스크 I/O 요청에 대해 헤드(Head)의 이동(탐색거리)을 최소화하도록 처리 순서를 결정하는 기법으로, 디스크 처리량과 평균 응답시간을 최적화한다.

## Ⅱ. 구성요소 / 원리
- FCFS(First Come First Served): 요청 도착 순서대로 처리, 공정하나 탐색거리 큼
- SSTF(Shortest Seek Time First): 현재 헤드에서 가장 가까운 요청 우선, 기아(Starvation) 발생
- SCAN(엘리베이터): 한 방향 끝까지 진행하며 처리 후 반대로 회귀
- C-SCAN(Circular SCAN): 끝 도달 시 처음으로 즉시 복귀해 균일한 대기시간 보장
- LOOK / C-LOOK: 마지막 요청까지만 이동(끝까지 안 감)하는 SCAN/C-SCAN 개선형

## Ⅲ. 흐름도 / 구조
```text
요청 큐 → [스케줄러: 헤드 위치·방향 판단] → 처리 순서 결정
  FCFS  : 도착순
  SSTF  : 최근접 우선  →  탐색거리↓, 기아↑
  SCAN  : ←──헤드──→ 끝까지 후 반전
  C-SCAN: ──헤드──→끝 ↺ 처음 복귀(원형)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 탐색거리(헤드 이동) 최소화로 처리량 향상·응답시간 단축 |
| 장점 | SSTF·SCAN 계열은 FCFS 대비 평균 탐색거리 대폭 감소 |
| 한계 | SSTF는 기아, SCAN은 양끝 편향, 알고리즘별 트레이드오프 존재 |

알고리즘 비교

| 알고리즘 | 탐색거리 | 기아 | 특징 |
|:---|:---|:---|:---|
| FCFS | 큼 | 없음 | 공정·단순 |
| SSTF | 작음 | 발생 | 최근접 우선 |
| SCAN | 중간 | 없음 | 양방향 왕복 |
| C-SCAN | 중간 | 없음 | 대기시간 균일 |
| LOOK/C-LOOK | 작음 | 없음 | 끝 이동 생략 |

## Ⅴ. 기술사적 적용
- HDD 환경에서 탐색거리 기반 SCAN 계열이 표준, 데이터센터 처리량 최적화
- SSD는 탐색 개념이 없어 NOOP·요청 병합 위주 스케줄러로 전환
- 리눅스 CFQ·Deadline·mq-deadline 등 I/O 스케줄러 설계 기반
