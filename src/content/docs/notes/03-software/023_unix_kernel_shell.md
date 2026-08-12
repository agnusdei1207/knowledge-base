---
sidebar:
  order: 23
  label: "023. UNIX 커널•쉘•파일시스템 3요소 (UNIX Kernel Shell)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "UNIX 커널•쉘•파일시스템 3요소 (UNIX Kernel Shell)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 23
extra:
  question_no: "023"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 기출 후 저빈도, UNIX 구성 기초"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **UNIX Architecture (UNIX 3대 구성요소)**: 사용자-하드웨어 간의 인터페이스 역할을 수행하는 Shell(명령어 해석기), OS의 핵심 제어를 담당하는 Kernel, 데이터를 영구 관리하는 File System으로 분할된 3대 아키텍처 구조.
- **Kernel (커널)**: 하드웨어 직접 제어, 메모리/프로세스 스케줄링, I/O 관리 및 보안 특권 모드(Kernel Mode)를 담당하는 UNIX 핵심 서비스엔진.
- **Shell (쉘)**: 사용자 입력 명령어(Command)를 받아 해석한 후 커널이 수행할 수 있는 System Call 형태로 변환 전달하는 CLI/GUI 명령어 해석기.

</details>

- 정의/개념: 하드웨어 자원을 은닉하고 사용자 명령 처리와 파일 저장을 명확히 계층 분리한 운영체제 표준 3대 아키텍처인 **UNIX Kernel, Shell & File System**
- 배경/필요성: 사용자 응용 프로그램의 하드웨어 직접 억세스로 인한 시스템 크래시 차단, 모듈식 명령 조합(Pipe/Redirection) 및 계층형 데이터 관리 요구성

#### 한줄 요약

- 유닉스는 명령•자원•저장 책임을 분리하고 특권 접근을 커널로 제한한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **System Call (시스템 콜)**: 사용자 공간(User Space)에서 커널 공간(Kernel Space)의 자원에 접근하기 위해 커널 인터페이스를 호출하는 소프트웨어 트랩 메커니즘.
- **Everything is a File**: UNIX 철학 중 하나로, 일반 파일, 디렉터리, 키보드/모니터, 하드디스크, 네트워크 소켓 등 모든 하드웨어 장치를 단일 파일 인터페이스(`/dev`)로 다루는 특성.

</details>

- **User Space (Shell)** 대 **Kernel Space (Kernel)**의 이원화된 특권 보호 경계
- **Everything is a File** 원칙 기반 디바이스/소켓 파일 통합 추상화
- **Pipe(`|`)** 및 Redirection 기반 소형 CLI 명령어의 강력한 연쇄 조합성

#### 한줄 요약

- 시스템 호출, 파이프, 파일 시스템의 역할 분리가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **POSIX Standard**: UNIX 계열 운영체제 간 소프트웨어 호환성을 보장하기 위해 IEEE가 정립한 가식 인터페이스 규격 표준.

</details>

```text
[사용자 응용프로그램 / CLI]
            |
         [Shell] (bash, zsh)
            |
    [System Call Interface]
            |
   [Kernel System] (CPU/Memory/IPC)
            |
      [File System] (ext4/VFS)
            |
      [Hardware Device]
```

선의 의미: 사용자 입력이 Shell을 거쳐 System Call Interface를 통해 Kernel 특권 구역으로 전달되어 File System 및 하드웨어를 구동하는 상하 계층 아키텍처.

| 3대 구성요소 | 역할 및 핵심 기능 | 주요 구현체 및 예시 |
|:---|:---|:---|
| **Shell (쉘)** | 사용자 명령어 해석, 스크립팅, 환경변수 제어, **Pipe/Redirection** | bash, zsh, sh, ksh, csh |
| **Kernel (커널)** | 프로세스/메모리/I/O 스케줄링, **System Call**, 보안 특권 제어 | Linux Kernel, BSD Kernel, System V |
| **File System** | 계층적 디렉터리 구조(`/`), Inode 메타데이터, 파일 저장 및 **VFS** | ext4, XFS, UFS, ZFS |

#### 한줄 요약

- 쉘과 커널 및 파일 시스템의 책임 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **fork() / exec()**: Shell에서 신규 명령어를 구동할 때, 자식 프로세스를 복제 생성(`fork`) 후 신규 실행 파일 바이너리를 Overwrite(`exec`)하여 디스패치하는 과정.

</details>

```text
┌──────────────────────────────┐
│ 사용자 명령•인수           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 명령 해석               │
│ 2. 프로세스 실행 요청      │
│ 3. 경로•권한 조회          │
│ 4. 프로세스 생성•실행      │
│ 5. 종료 상태 처리          │
└──────────────────────────────┘
```

### 동작 원리

1. **명령 해석**: 사용자가 Shell 프롬프트 상에 `ls -al | grep log` 명령어 입력 및 토큰 해석.
2. **프로세스 실행 요청**: Shell이 **fork()** 시스템 콜을 인가하여 자식 프로세스 생성.
3. **경로·권한 조회**: PATH 환경 변수를 검색하여 File System(VFS)에서 해당 바이너리의 Inode 권한(r-x) 검증.
4. **프로세스 생성·실행**: **execve()** 호출로 커널 메모리에 바이너리 적재 후 CPU 디스패치 연산.
5. **종료 상태 처리**: **waitpid()** 시스템 콜을 통해 프로세스 exit() 상태값 수거 후 Shell 프롬프트 복귀.

#### 한줄 요약

- 명령 해석부터 종료 상태 처리까지의 실행 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Monolithic Kernel vs Microkernel**: monolithic은 모든 OS 서비스(FS, Net, Driver)가 단일 커널 공간에 포함된 반면, microkernel은 최소 기능만 커널에 두고 나머지는 유저 서비스로 분리.

</details>

| 비교 항목 | Shell (쉘) | Kernel (커널) | File System (파일 시스템) |
|:---|:---|:---|:---|
| 실행 공간 | **User Space** (비특권 모드) | **Kernel Space** (Ring 0 특권 모드) | Kernel Space 내의 VFS 서브모듈 |
| 데이터 상주 | 메모리 유저 스택 / 환경변수 | 메인 메모리(DRAM) 커널 상주 | 물리 저장 매체 (HDD/SSD/NVMe) |
| 사용자 접점 | 사용자 직접 인터랙션 (CLI/GUI) | 사용자 직접 접촉 불가 (System Call 경유) | 쉘/응용프로그램의 입출력 대상 |

#### 한줄 요약

- 커널은 자원, 쉘은 명령, 파일 시스템은 저장을 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Shell Injection**: 신뢰할 수 없는 사용자 입력값을 Shell 스크립트 실행 명령 파라미터로 그대로 결합 시 의도치 않은 하위 악성 세미콜론(`;`) 명령어가 동시 실행되는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Shell 스크립트 실행 시 **Shell Injection** 공격 위험 | 파라미터 샌니타이징 및 **eval** 구문 사용 절대 금지 | 무단 명령 임의 실행 예방 |
| User 프로세스의 오류로 인한 Kernel Crash 파급 | **User Mode(Ring 3) / Kernel Mode(Ring 0)** 완전 분리 | 시스템 전체 정지 차단 |
| 수많은 파이프(`|`) 연결 시 자식 프로세스 생성 폭증 | 파이프라인 프로세스 수 제어 및 **Limit (ulimit)** 인가 | OS PID/Process 고갈 차단 |

> 사례: Linux **Bash Shell Vulnerability (Shellshock)** 패치 및 POSIX 준수 인프라 구축

#### 한줄 요약

- 허용 목록, 최소 권한, 파이프 실패 전파를 적용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **UNIX 아키텍처 설계 기준(UNIX Architecture Standards)**: 모듈화, 책임 분리(Separation of Concerns), POSIX 표준 준수 및 보안 격리에 의거한 설계 체계.

</details>

- **UNIX 아키텍처 설계 기준**에 따라 안정적인 서포트 시스템 구축을 위해 **Shell-Kernel-FileSystem** 3대 역할 분담 구조 유지

#### 한줄 요약

- 명령•특권 자원•영속 데이터의 책임 경계를 유지하는 것이 핵심이다.
