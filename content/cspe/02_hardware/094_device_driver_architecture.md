---
title: 디바이스 드라이버 구조 (Device Driver Architecture)
date: 2026-07-05
tags: [cspe-hardware]
weight: 94
---

## Ⅰ. 개요
- 운영체제가 하드웨어 장치와 통신하기 위해 사용하는 소프트웨어 인터페이스 모듈.
- 하드웨어의 복잡한 물리적 동작을 추상화하여 사용자 영역에 일관된 API를 제공함.
| 구분 | 내용 | 비고 |
|---|---|---|
| 정의 | OS 커널과 물리적 장치 간의 중계 소프트웨어 | 추상화 계층 |
| 의도 | 드라이버 종류별 특성 및 커널 공간 동작 원리 이해 측정 | 시스템 통합 |

## Ⅱ. 구성요소
[ User Application ] --(System Call)--> [ VFS ]
[ Character / Block / Network Driver ]
[ Hardware (Register / Interrupt / DMA) ]
| 구성요소 | 설명 | 비유 |
|---|---|---|
| Char Driver | 데이터를 바이트 단위로 순차 접근하는 장치 (Key, Serial) | 빨대 |
| Block Driver | 데이터를 고정 크기 블록 단위로 랜덤 접근 (Disk, Flash) | 택배박스 |
| Interrupt | HW 상태 변화를 CPU에 즉시 알리는 신호선 | 호출벨 |
> 요약: 캐릭터, 블록, 네트워크 드라이버가 VFS 아래 존재함.

## Ⅲ. 절차
(1) Open -> (2) Read/Write -> (3) Interrupt Handling -> (4) Close
1. Open: 파일 시스템의 노드를 통해 드라이버를 열고 초기화함.
2. Read/Write: 사용자 영역과 커널 영역 간의 데이터 복사(copy_to/from_user).
3. Interrupt Handling: HW 작업 완료 시 ISR이 실행되어 데이터를 처리함.
4. Close: 자원을 반납하고 장치 사용을 종료함.
> 요약: 장치 열기, 데이터 교환, 인터럽트 처리, 닫기 순으로 동작함.

## Ⅳ. 문제점
- 커널 안정성: 드라이버 코드의 작은 오류가 전체 시스템 크래시(Kernel Panic) 유발.
- 동기화 이슈: 멀티코어 환경에서 공유 자원 접근 시 경합(Race Condition) 발생.

## Ⅴ. 개선방안
- 사용자 모드 드라이버: 커널 영역이 아닌 유저 영역에서 구동하여 안정성 확보.
- 동기화 메커니즘: Spinlock, Mutex, Semaphore 등을 활용한 정교한 상호 배제 적용.

## Ⅵ. 전망
- 가상화 대응: Virtio 등 표준화된 가상화 드라이버 구조 채택으로 클라우드 호환성 강화.
- Rust 도입: 커널 드라이버 작성 시 메모리 안전성을 보장하는 Rust 언어 적용 확산.
