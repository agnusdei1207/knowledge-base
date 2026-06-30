---
title: "프로세스 상태전이 (Process State Transition)"
date: "2026-06-30"
weight: 13
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 프로세스가 생성부터 소멸까지 자원 할당·이벤트 발생에 따라 생성(New)·준비(Ready)·실행(Running)·대기(Waiting)·종료(Terminated) 상태 간을 옮겨가는 생명주기 모델.

## Ⅱ. 구성요소 / 원리
- New(생성): 프로세스 생성, PCB 할당 후 준비 큐 진입 대기
- Ready(준비): CPU 할당만 기다리는 실행 가능 상태(준비 큐 대기)
- Running(실행): CPU를 점유해 명령을 수행하는 상태
- Waiting/Blocked(대기): I/O·이벤트 완료를 기다리는 비실행 상태
- Terminated(종료): 수행 완료, 자원 회수 후 PCB 제거

## Ⅲ. 흐름도 / 구조
```text
[New] --admit--> [Ready] --dispatch--> [Running] --exit--> [Terminated]
                   ^   ^                   |  |
        interrupt  |   |  I/O완료(wakeup)   |  | I/O요청(event wait)
                   |   +------ [Waiting] <-+  |
                   +-----------(timeout/선점)-+
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 한정된 CPU를 다수 프로세스가 효율적으로 공유 |
| 장점 | 멀티프로그래밍·시분할로 CPU 이용률·응답성 향상 |
| 한계 | 잦은 상태전이 시 문맥교환(Context Switch) 오버헤드 증가 |

## Ⅴ. 기술사적 적용
- Running→Ready 전이(선점)는 스케줄링 정책(RR·우선순위)과 직접 연계
- Waiting 누적은 I/O 병목·기아(Starvation) 진단 지표로 활용
- 상태전이 통계는 시스템 튜닝(큐 길이, 타임퀀텀) 근거로 사용
