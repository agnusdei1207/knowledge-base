---
title: "하이퍼바이저 (Hypervisor)"
date: "2026-06-30"
weight: 6
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 하이퍼바이저(Hypervisor)는 물리 하드웨어 위에서 다수의 가상머신(VM, Virtual Machine)을 생성·격리·관리하는 가상화 계층(VMM, Virtual Machine Monitor)으로, CPU·메모리·I/O 자원을 가상화하여 게스트 OS에 할당한다.

## Ⅱ. 구성요소 / 원리
- **VMM(Virtual Machine Monitor)**: 게스트 OS의 특권명령을 가로채 처리하는 핵심 계층
- **Type 1(베어메탈, Bare-metal)**: 하드웨어 위에 직접 설치(ESXi, Xen, Hyper-V)
- **Type 2(호스트형, Hosted)**: 호스트 OS 위에 응용처럼 설치(VirtualBox, VMware Workstation)
- **자원 가상화**: vCPU, 가상 메모리, 가상 I/O 장치 제공
- **격리(Isolation)**: VM 간 장애·보안 격리 보장

## Ⅲ. 흐름도 / 구조
```text
[Type 1 베어메탈]          [Type 2 호스트형]
 ┌─────┬─────┐             ┌─────┬─────┐
 │게스트│게스트│            │게스트│게스트│ VM
 │ OS  │ OS  │             │ OS  │ OS  │
 ├─────┴─────┤             ├─────┴─────┤
 │ Hypervisor│             │Hypervisor │
 ├───────────┤             ├───────────┤
 │ Hardware  │             │ Host OS   │
 └───────────┘             ├───────────┤
                           │ Hardware  │
                           └───────────┘
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 단일 물리 서버의 자원을 다수 VM으로 분할·통합(서버 통합) |
| 장점 | 자원 활용률·격리·이식성 향상, 스냅샷·마이그레이션 지원 |
| 한계 | 가상화 오버헤드, 게스트마다 전체 OS 필요(자원 중복) |

### Type 1 vs Type 2 비교표
| 구분 | Type 1 (베어메탈) | Type 2 (호스트형) |
|:---|:---|:---|
| 설치 위치 | 하드웨어 직접 | 호스트 OS 위 |
| 성능 | 높음 | 상대적 낮음 |
| 용도 | 데이터센터·서버 | 개발·테스트·데스크톱 |
| 예시 | ESXi, Xen, Hyper-V | VirtualBox, Workstation |

## Ⅴ. 기술사적 적용
- 하드웨어 보조 가상화(VT-x/AMD-V)와 결합해 오버헤드 최소화
- 컨테이너(커널 공유)와 비교 시 격리성↑·경량성↓의 트레이드오프
- 라이브 마이그레이션·HA로 클라우드 IaaS 인프라의 기반 기술
