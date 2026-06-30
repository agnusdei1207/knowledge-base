---
title: "듀얼모드 (Dual Mode)"
date: "2026-06-30"
weight: 1
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 듀얼모드(Dual Mode)는 CPU의 실행 상태를 사용자모드(User Mode)와 커널모드(Kernel Mode)로 구분하고, 모드비트(Mode Bit)로 현재 모드를 표시하여 특권명령(Privileged Instruction)을 보호하는 하드웨어 지원 보호 기법이다.

## Ⅱ. 구성요소 / 원리
- **모드비트(Mode Bit)**: 0=커널모드, 1=사용자모드로 현재 실행 권한 표시
- **사용자모드(User Mode)**: 응용 프로그램 실행, 특권명령 수행 불가
- **커널모드(Kernel Mode)**: 운영체제 코드 실행, 모든 명령 수행 가능
- **특권명령(Privileged Instruction)**: I/O, 인터럽트 제어, 타이머 설정 등 커널모드 전용 명령
- **모드 전환**: 시스템콜·인터럽트·예외 발생 시 사용자→커널, 처리 완료 후 복귀

## Ⅲ. 흐름도 / 구조
```text
[User Mode, bit=1]
   응용 프로그램
      │ system call / interrupt (trap)
      ▼  모드비트 1→0 전환
[Kernel Mode, bit=0]
   특권명령 수행 (OS)
      │ 처리 완료 (return)
      ▼  모드비트 0→1 복귀
[User Mode, bit=1]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 사용자 프로그램으로부터 OS·하드웨어 자원을 보호 |
| 장점 | 특권명령 오·남용 차단, 시스템 안정성·보안성 확보 |
| 한계 | 모드 전환 오버헤드 발생, HW(CPU) 모드비트 지원 필수 |

## Ⅴ. 기술사적 적용
- 시스템콜·인터럽트의 안전한 진입점(trap) 제공의 기반 메커니즘
- 가상화 환경에서 root/non-root(VT-x) 모드 등 다단계 보호로 확장
- 메모리 보호(MMU), 타이머 기반 선점 스케줄링과 연계되어 자원 격리 구현
