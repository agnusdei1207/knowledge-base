---
title: "하드웨어 보조 가상화 (Hardware-assisted Virtualization, Intel VT-x)"
date: "2026-06-30"
weight: 8
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 하드웨어 보조 가상화(Hardware-assisted Virtualization)는 CPU가 가상화 전용 실행 모드(Intel VT-x, AMD-V)를 제공하여, 게스트 OS의 특권명령을 소프트웨어 변환 없이 하드웨어 차원에서 트랩·처리함으로써 가상화 오버헤드를 최소화하는 기술이다.

## Ⅱ. 구성요소 / 원리
- **VT-x(Intel Virtualization Technology) / AMD-V**: 가상화 지원 CPU 확장 명령 집합
- **루트 모드(Root Mode)**: 하이퍼바이저(VMM)가 실행되는 모드
- **논루트 모드(Non-root Mode)**: 게스트 OS가 실행되는 모드
- **VM Entry/VM Exit**: 게스트↔하이퍼바이저 전환, VMCS(VM Control Structure)로 상태 관리
- **EPT(Extended Page Table) / NPT**: 게스트→호스트 물리주소 2단계 메모리 변환을 HW로 가속

## Ⅲ. 흐름도 / 구조
```text
[Root Mode] Hypervisor(VMM)
     │ VM Entry
     ▼
[Non-root Mode] Guest OS 실행
     │ 민감 명령/이벤트 발생
     ▼ VM Exit (VMCS에 상태 저장)
[Root Mode] VMM이 처리
     │ 메모리 접근은 EPT로 GPA→HPA 변환
     ▼ VM Entry로 게스트 재개
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 소프트웨어 가상화(Binary Translation) 없이 고성능·무수정 가상화 |
| 장점 | 게스트 OS 무수정, 낮은 오버헤드, EPT로 메모리 변환 가속 |
| 한계 | CPU·BIOS 지원 필수, VM Exit 빈발 시 성능 저하 |

## Ⅴ. 기술사적 적용
- 전가상화의 바이너리 변환을 대체하여 성능 격차를 크게 축소
- KVM은 VT-x/AMD-V 기반으로 Linux 커널을 하이퍼바이저화
- SR-IOV·IOMMU(VT-d)와 결합해 I/O까지 하드웨어 가상화 확장
