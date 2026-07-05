---
title: "전·반가상화·컨테이너 (Full Para Container Virtualization)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 21
---

## Ⅰ. 개요
- **정의**: 하드웨어 자원을 논리적으로 분할하여 다수 실행 환경을 격리·제공하는 기술임
- **배경/필요성**: 물리 서버 1대의 자원 활용률이 낮아 다중 워크로드 동시 수용이 필요함
- **비유**: 하나의 건물을 칸막이(전가상화), 반투명 벽(반가상화), 칸막이 없는 공유 주방(컨테이너)으로 나누는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 세 방식의 구조적 차이 비교 | Hypervisor 위치·Guest OS 유무 | 컨테이너를 가상화가 아닌 격리 기술로 구분 |

> 요약: 자원 분할 수준과 Guest OS 유무로 전·반가상화·컨테이너를 구분함

## Ⅱ. 구성요소
```text
Hardware
  |
  +-- Hypervisor (Type-1/Type-2)
  |     +-- Guest OS (Full) --- Binary Translation
  |     +-- Guest OS (Para) --- Hypercall API
  |
  +-- Host OS
        +-- Container Engine --- Namespace/Cgroup
              +-- App Process
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Hypervisor | HW와 Guest OS 사이에서 자원 중재하는 VMM | 건물 관리인 |
| Binary Translation | 전가상화에서 특권 명령을 소프트웨어로 변환 | 동시통역사 |
| Hypercall | 반가상화에서 Guest OS가 직접 Hypervisor 호출 | 내선전화 |
| Namespace/Cgroup | 컨테이너 프로세스의 격리·자원 제한 커널 기능 | 공유 주방의 개인 냉장고 |

> 요약: Hypervisor 기반 VM과 커널 기반 컨테이너로 격리 수준이 구분됨

## Ⅲ. 절차
```text
요청 수신 -> 자원 할당 -> 격리 환경 생성 -> 워크로드 실행
```
- 1단계: 사용자가 VM 또는 컨테이너 생성을 요청함
- 2단계: Hypervisor 또는 Container Engine이 CPU·메모리·스토리지를 할당함
- 3단계: 전가상화는 Guest OS 부팅, 반가상화는 수정 커널 부팅, 컨테이너는 Namespace 격리를 수행함
- 4단계: 격리된 환경에서 애플리케이션을 실행하고 자원 사용량을 모니터링함

> 요약: 자원 할당 후 방식별 격리 메커니즘을 적용하여 워크로드를 실행함

## Ⅳ. 문제점
- 전가상화 오버헤드: Binary Translation으로 특권 명령 변환 시 CPU 사이클 소모가 큼
- 반가상화 커널 수정: Guest OS 소스 수정이 필수여서 비공개 OS 적용이 불가함
- 컨테이너 격리 한계: 커널을 공유하므로 커널 취약점 발생 시 호스트 전체가 노출됨

> 요약: 각 방식은 성능·호환성·보안 측면에서 상충 관계를 가짐

## Ⅴ. 개선방안
1. 단기: HW 가상화 지원(VT-x/AMD-V) 활용으로 Binary Translation 오버헤드 제거
2. 중기: Virtio 등 표준 반가상화 드라이버 채택으로 커널 수정 범위 최소화
3. 장기: gVisor·Kata Containers 등 경량 VM 기반 컨테이너로 커널 격리 수준 강화

> 요약: HW 지원 가상화와 경량 VM 결합으로 성능·보안을 동시에 확보함

## Ⅵ. 전망
- 발전 방향: Unikernel·MicroVM이 컨테이너 수준 경량성과 VM 수준 격리를 동시 제공함
- 기술사적 판단: 클라우드 네이티브 환경에서 컨테이너 중심 아키텍처가 기본이 됨
- 기술사 제언: 워크로드 보안 등급에 따라 VM·컨테이너·MicroVM을 선택 적용할 필요가 있음
