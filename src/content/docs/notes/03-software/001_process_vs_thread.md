---
sidebar:
  order: 1
  label: "001. 프로세스 vs 스레드 (Process vs Thread)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 프로세스 vs 스레드 (Process vs Thread)
date: "2026-08-10T10:00:00+09:00"
tags: [notes-software]
weight: 1
extra:
  question_no: "001"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 프로세스•스레드 자원 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **프로세스(Process)**: OS로부터 독립된 가상 주소 공간(Code, Data, Heap, Stack)과 PCB, 시스템 자원을 할당받아 실행되는 독립 단위.
- **스레드(Thread)**: 프로세스 내부에서 주소 공간(Code, Data, Heap)과 자원을 공유하며, 독자적인 Stack 및 TCB를 갖고 실행되는 CPU 스케줄링의 기본 단위.

</details>

- 정의/개념: 독립된 가상 메모리 주소 공간 및 자원 보호 컨테이너를 갖는 **프로세스** 및 자원 공유 기반 경량 CPU 스케줄링 실행 단위인 **스레드**
- 배경/필요성: 프로세스 간 독자 메모리 격리를 통한 안전성 확보 및 스레드 간 낮은 문맥 전환(Context Switch) 오버헤드를 통한 고성능 병렬성 달성 요구

#### 한줄 요약

- 장애 격리와 상태 공유 빈도에 따라 프로세스 또는 스레드를 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **주소 공간(Virtual Address Space)**: 프로세스마다 독립 할당되어 다른 프로세스가 함부로 접근하지 못하도록 보장된 가상 메모리 영역.
- **격리 범위(Isolation Boundary)**: 특정 프로세스의 메모리 훼손이나 비정상 종료가 타 프로세스에 영향을 주지 않는 보호 경계.
- **공유 범위(Shared Boundary)**: 동일 프로세스 내 스레드들이 Code, Data, Heap 및 개방 파일(File Descriptor)을 함께 공유하는 범위.

</details>

- 프로세스 간 **주소 공간** 완전 독립에 의한 결함 격리(Fault Isolation) 및 보안 **격리 범위** 확보
- 동일 프로세스 내 스레드 간 메모리 **공유 범위** 확장에 따른 초저지연 데이터 통신 및 락(Lock) 동기화 필요성
- 문맥 전환(Context Switching) 시 TLB 플러시 오버헤드 유무 차이 (프로세스: TLB Flush 발생 vs 스레드: Register/Stack 전환만 발생)

#### 한줄 요약

- 프로세스 격리 비용과 스레드 공유 위험 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **PCB(Process Control Block)**: 프로세스 ID, 상태, 가상 주소 매핑(MMU PGD), 개방 파일 목록 및 TCB 리스트를 보유하는 커널 구조체.
- **TCB(Thread Control Block)**: 스레드 ID, 스레드 상태, PC(Program Counter), SP(Stack Pointer) 및 레지스터 세트를 보관하는 스레드 제어 구조체.
- **IPC(Inter-Process Communication)**: 격리된 프로세스 간 메모리 장벽을 넘어 커널(Pipe, Socket, Shared Memory)을 경유하여 데이터를 전송하는 기법.

</details>

```text
                 [운영체제 스케줄러]
                          |
┌────────────── 프로세스 경계 ──────────────┐
│ [PCB] -- [공유 주소 공간] -- [TCB•실행 문맥] │
└───┬───────────────────────────────────────┘
    |
[IPC 채널]
```

선의 의미: OS 스케줄러가 TCB를 선택하여 실행하고, PCB 기반의 독립 주소 공간 내부에서 여러 TCB가 힙/코드를 공유하며, 외부 프로세스와는 IPC 채널로 통신하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 운영체제 스케줄러 | **TCB** 및 **PCB** 기반 디스패치 및 코어 시간 할당 스케줄링 |
| PCB | 가상 **주소 공간**, 파일 디스크립터 메타데이터 관리 및 결함 격리 |
| 공유 주소 공간 | 프로세스 내부 스레드들이 공유하는 Code, Data, Heap 메타 영역 |
| TCB & 실행 문맥 | 스레드 전용 Stack Pointer, Register, Program Counter 상태 저장 |
| IPC 채널 | 소켓, 파이프, **공유 메모리** 기반 프로세스 간 가상 공간 데이터 전송 |

#### 한줄 요약

- 공유 주소 공간과 IPC 채널로 경계 내부 공유와 경계 간 통신을 구분한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **보호 구간(Critical Section)**: 스레드가 공유 메모리에 접근하여 갱신할 때 데이터 상호 배제(Mutex)가 보장되어야 하는 코드 영역.
- **직렬화(Serialization)**: IPC 전송 시 가상 주소 공간 내의 구조체/객체를 연속된 바이트 스트림(Byte Stream)으로 변환하는 동작.

</details>

```text
[작업 간 통신•장애 요구]
           │
           ▼
1. 신뢰•장애 경계 판정
      ┌────┴──────────┐
      │ 경계 분리     │ 상태 공유
      ▼               ▼
   [프로세스]       [스레드]
      │               │
      ▼               ▼
2. IPC 직렬화•전달 3. 공유 상태 소유권 설정
      │               │
      │               ▼
      │          4. 잠금•동기화
      └───────┬───────┘
              ▼
        [작업 결과 반환]
```

### 동작 원리

1. **신뢰·장애 경계 판정**: 작업 간 보안/오류 격리 수준에 따라 프로세스 분리 또는 스레드 멀티태스킹 1차 결정.
2. **IPC 직렬화·전달**: 프로세스 선택 시 데이터 **직렬화(Serialization)** 및 **IPC** 파이프라인 수용.
3. **공유 상태 소유권 설정**: 스레드 선택 시 Heap 공유 영역 수용 및 데이터 변경 소유권 지정.
4. **잠금·동기화**: 스레드가 **Critical Section** 진입 시 Mutex/Spinlock 인가 및 전역 상태 갱신 완료.

#### 한줄 요약

- 프로세스는 IPC 직렬화·전달, 스레드는 공유 상태 소유권 설정과 잠금·동기화를 사용한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Context Switch Overhead**: CPU 레지스터 덤프 및 MMU 페이지 테이블(CR3) 갱신, TLB 무효화 시 소모되는 시스템 오버헤드.

</details>

| 비교 항목 | 프로세스 (Process) | 스레드 (Thread) |
|:---|:---|:---|
| 메모리 구성 | 독립 가상 **주소 공간** 보유 (Code, Data, Heap, Stack) | Code, Data, Heap 공유 / 독자 Stack만 소유 |
| 결함 영향 (Fault Impact)| 단일 프로세스 아웃 시 타 프로세스 영향 없음 (**Fault Isolation**) | 단일 스레드 파손 시 전 프로세스 다운 (**Crash**) |
| 통신 방식 | **IPC** (Pipe, Shared Memory, Socket) 필요 | 전역 변수, 힙 메모리 직접 접근 (초고속) |
| 문맥 전환 오버헤드 | 높음 (**TLB Flush**, MMU CR3 레지스터 체인지) | 낮음 (CPU 레지스터 및 Stack Pointer만 변경) |

#### 한줄 요약

- 장애 격리는 프로세스, 빈번한 상태 공유는 스레드가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Thread Pool**: 스레드 생성/소멸 오버헤드를 막기 위해 미리 스레드 큐를 생성하여 재사용하는 자원 관리 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스레드 간 무분별한 힙 공유로 인한 동시성 경합 및 데드락 | **불변 객체(Immutable)** 패턴 및 Mutex/Spinlock 인가 | 데이터 경합 원천 예방 |
| 단일 스레드 예외(Segmentation Fault) 시 전체  crash | **신뢰 경계** 단위 멀티 프로세스 분리 및 Supervisor 패턴 적용 | 장애 격리(Fault Isolation) 보장 |
| 과도한 스레드 생성에 따른 문맥 전환 오버헤드 및 OOM | **Thread Pool** 제한 및 포화 정책(Saturation Policy) 세팅 | CPU/메모리 사용량 안정화 |

> 사례: 크롬 브라우저의 탭별 **Multi-Process** 구조 및 웹 서버(Nginx/Netty)의 **Worker Thread Pool** 인프라 적용

#### 한줄 요약

- 웹 브라우저 탭별 Multi-process Architecture 적용 및 Watchdog 기반 프로세스 Supervisor/재시작 패턴을 도입하여 Fault Isolation을 보장한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **실행 단위 선택 기준(Execution Unit Selection Criteria)**: 시스템 결함 격리 수준, 메모리 공유 빈도, 지연시간 타깃에 근거한 설계 아키텍처 수립 체계.

</details>

- **실행 단위 선택 기준**에 따라 완전 격리 및 안전성은 **프로세스**, 초고속 데이터 통신 및 병동 처리는 **스레드** 채택

#### 한줄 요약

- Fault Tolerance & Privilege Boundary에는 Process isolation, Intra-process Parallelism & In-Memory State Exchange에는 Thread concurrency 모델을 적용한다.
