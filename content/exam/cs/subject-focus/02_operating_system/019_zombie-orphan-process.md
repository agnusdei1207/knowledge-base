---
title: "좀비·고아 프로세스 (Zombie/Orphan Process)"
date: "2026-06-30"
weight: 19
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 좀비(Zombie)는 종료했으나 부모가 wait()로 종료상태를 수거하지 않아 PCB만 남은 프로세스, 고아(Orphan)는 부모가 먼저 종료되어 보호자를 잃은 실행 중 자식 프로세스.

## Ⅱ. 구성요소 / 원리
- 좀비: exit() 완료, 자원 회수했으나 종료코드 보존용 PCB 잔존
- 부모 wait()/waitpid() 호출 시 좀비 회수(reap)
- 고아: 부모 먼저 종료, 자식은 계속 실행
- init/systemd(PID 1)가 고아를 입양(re-parenting)
- 입양된 고아 종료 시 init이 자동 wait로 수거

## Ⅲ. 흐름도 / 구조
```text
[좀비]  Child exit() --> Zombie(PCB 잔존)
         Parent wait() --> 수거 → 소멸
         (wait 미호출 시 좀비 누적)

[고아]  Parent 먼저 exit --> Child 고아
         init(PID 1) 입양 --> Child exit --> init이 wait 수거
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 종료상태 전달 보장 및 자원 회수 책임 명확화 |
| 장점 | 부모가 자식 종료코드 확인 가능, init 입양으로 누수 방지 |
| 한계 | 좀비 누적 시 PID 고갈, 부모 코딩 결함에 취약 |

## Ⅴ. 기술사적 적용
- 좀비 누적 = wait 누락 버그 신호 → SIGCHLD 핸들러로 회수
- 데몬화 시 더블 fork로 고아 만들어 init 입양 유도
- 컨테이너 PID 1은 좀비 수거(reaper) 역할 명시 설계 필요
