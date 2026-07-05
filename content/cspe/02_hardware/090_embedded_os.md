---
title: 임베디드 OS 아키텍처 (Embedded OS)
date: 2026-07-05
tags: [cspe-hardware]
weight: 90
---

## Ⅰ. 개요
- 제한된 자원을 가진 임베디드 시스템에서 하드웨어를 제어하고 응용 프로그램을 실행하는 운영체제.
- 저전력, 고신뢰성, 실시간성 보장이 설계의 핵심 목표임.
| 구분 | 내용 | 비고 |
|---|---|---|
| 정의 | 특정 목적을 수행하기 위해 최적화된 하드웨어 제어 OS | 경량화 중심 |
| 의도 | 시스템 자원 제약 하의 OS 설계 역량 및 구조 이해 측정 | 가용성 중점 |

## Ⅱ. 구성요소
[ Application Layer ]
[ OS Service (FS, NW) ]
[ Micro/Monolithic Kernel ]
[ HAL (Hardware Abstraction Layer) ]
[ Hardware (CPU, Memory, I/O) ]
| 구성요소 | 설명 | 비유 |
|---|---|---|
| HAL | HW 의존적 코드를 분리하여 이식성 제공 계층 | 어댑터 |
| 커널 | 스케줄링, 메모리 관리 등 OS 핵심 기능 수행 | 심장 |
| BSP | 특정 보드 부팅을 위한 드라이버 및 설정 패키지 | 기초공사 |
> 요약: HAL, 커널, 서비스 라이브러리로 계층화된 최적화 구조임.

## Ⅲ. 절차
(1) Booting -> (2) Initialization -> (3) Scheduling -> (4) Task Execution
1. Booting: Bootloader가 HW 점검 후 OS 커널을 메모리에 로드함.
2. Initialization: HAL 및 장치 드라이버를 초기화하고 인터럽트 벡터 설정.
3. Scheduling: 우선순위 기반으로 실행할 태스크를 결정하고 컨텍스트 스위칭.
4. Task Execution: 응용 프로그램이 커널 서비스를 통해 자원을 사용하며 동작.
> 요약: 부팅, HW 초기화, 커널 활성화, 태스크 관리 순으로 실행됨.

## Ⅳ. 문제점
- 자원 제약: 메모리와 CPU 성능 부족으로 대규모 스택 및 복잡한 알고리즘 제약.
- 파편화: 하드웨어 사양별 커널 및 드라이버 수정으로 유지보수 복잡도 증대.

## Ⅴ. 개선방안
- 경량화 기술: 모듈형 커널(Microkernel) 적용 및 불필요한 서비스 제거.
- 표준화: POSIX 준수 및 컨테이너 기술(Docker for Embedded) 통한 이식성 확보.

## Ⅵ. 전망
- Edge AI 대응: 하드웨어 가속기(NPU) 최적화 스케줄링 기술이 핵심 경쟁력임.
- 보안 아키텍처: TrustZone 등 보안 HW와 긴밀히 결합된 격리 구조 OS 확산 전망.
