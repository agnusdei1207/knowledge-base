---
title: "IOMMU (Input-Output Memory Management Unit)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 102
---

# IOMMU (Input-Output Memory Management Unit)

## 미리 알고가기

- DMA(Direct Memory Access): 장치가 CPU(Central Processing Unit) 개입 없이 메모리에 직접 읽기·쓰기를 수행하는 방식임
- IOVA(Input/Output Virtual Address): 장치가 보는 I/O(Input/Output) 가상 주소임
- DMA Remapping: 장치 DMA 주소를 실제 물리 주소로 변환하고 권한을 검사하는 기능임
- SR-IOV(Single Root I/O Virtualization): 하나의 물리 장치를 여러 가상 기능으로 나누어 VM(Virtual Machine)에 제공하는 기술임
- IOTLB(Input/Output Translation Lookaside Buffer): IOMMU 주소 변환 결과를 캐시하는 버퍼임

## 1. 개요

- **정의/개념**: IOMMU(Input-Output Memory Management Unit)는 I/O 장치가 DMA로 접근하는 주소를 IOVA에서 물리 주소로 변환하고 장치별 접근 권한을 검사하는 메모리 관리 장치임.
- **배경/필요성**: DMA 장치는 CPU MMU(Memory Management Unit)를 거치지 않고 메모리에 접근하므로 악성 또는 오류 장치가 임의 메모리를 손상시킬 수 있음. IOMMU는 장치마다 허용된 메모리 범위를 제한해 성능과 보안을 함께 확보함.
- **비유**: 물류 차량이 창고에 직접 들어가더라도 출입 가능한 구역과 경로를 게이트에서 검사하는 장치임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DMA 보안과 가상화 장치 격리 이해 | IOVA, DMA remapping, device domain, passthrough | CPU MMU(Memory Management Unit)와 동일 기능으로만 설명 |

> 요약: IOMMU는 장치의 직접 메모리 접근을 주소 변환과 권한 검사로 통제하는 하드웨어임.

## 2. 특징 및 비교

| 판단 기준 | IOMMU 미사용 DMA | IOMMU 사용 DMA |
|:---|:---|:---|
| 주소 사용 | 장치가 물리 주소를 직접 사용함 | 장치가 IOVA를 사용하고 변환됨 |
| 보안 격리 | 장치 오류가 전체 메모리를 손상시킬 수 있음 | device domain별 접근 범위를 제한함 |
| 가상화 지원 | VM 장치 패스스루가 위험하거나 어려움 | SR-IOV, PCI(Peripheral Component Interconnect) passthrough 격리를 지원함 |
| 비용 | 변환 오버헤드가 적음 | IOTLB miss와 매핑 관리 비용이 생김 |

> 요약: IOMMU는 DMA 성능을 일부 희생하더라도 장치 격리와 가상화 유연성을 제공함.

- **적용 조건**: 장치 패스스루나 외부 DMA가 있는 플랫폼에서는 격리 요구가 우선됨
- **선택 지표**: IOTLB miss rate, DMA fault count, isolation group을 함께 확인해야 함
- **운영 관점**: IOMMU 설정은 BIOS(Basic Input/Output System), OS(Operating System), 하이퍼바이저, PCIe(Peripheral Component Interconnect Express) topology 전체에서 일관되어야 함

## 3. 구성요소/구조

```text
+----------+      +----------+      +----------+      +----------+
| PCIe dev | ---> | IOMMU    | ---> | Memory   | ---> | CPU/MMU  |
+----------+      +----------+      +----------+      +----------+
                       |
                       v
                +-------------+
                | Page tables |
                +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| I/O 장치 | NIC(Network Interface Card), GPU(Graphics Processing Unit), NVMe(Non-Volatile Memory Express)처럼 DMA 요청을 생성하는 장치임 | 물류 차량 |
| IOMMU 엔진 | DMA 주소 변환, 권한 검사, fault 보고를 수행함 | 출입 게이트 |
| I/O 페이지 테이블 | 장치별 IOVA와 물리 주소 매핑 정보를 저장함 | 구역 허가 목록 |
| IOTLB | 최근 변환 결과를 캐시해 IOMMU 변환 지연을 줄임 | 빠른 출입증 확인대 |

> 요약: IOMMU는 장치 요청을 페이지 테이블과 IOTLB로 검사해 허용된 메모리만 접근하게 함.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Map      | ---> | DMA req  | ---> | Check    | ---> | Access   |
+----------+      +----------+      +----------+      +----------+
```

1. **매핑 설정** — OS나 하이퍼바이저가 장치 domain과 IOVA-물리 주소 매핑을 구성함
2. **DMA 요청** — 장치가 IOVA를 포함한 읽기·쓰기 요청을 PCIe 등으로 발행함
3. **변환·검사** — IOMMU가 IOTLB 또는 페이지 테이블로 주소와 권한을 확인함
4. **접근·차단** — 허용 요청은 메모리로 전달하고 위반 요청은 fault로 보고함

> 요약: IOMMU는 DMA 요청마다 장치별 매핑과 권한을 확인해 메모리 접근을 중재함.

## 4. 문제점 및 개선방안

- **P1 성능 오버헤드**: IOTLB miss, 페이지 테이블 walk, map/unmap 호출이 고속 I/O 지연을 늘릴 수 있음
- **P1 대응**: large page, IOTLB sizing, batching map/unmap, passthrough mode를 워크로드별로 조정함 (확인: IOTLB miss rate)
- **P2 설정 복잡도**: passthrough, SR-IOV, interrupt remapping 설정이 잘못되면 VM 격리가 깨지거나 장치가 동작하지 않음
- **P2 대응**: IOMMU group, interrupt remapping, SR-IOV VF(Virtual Function) 정책을 표준 구성으로 검증함 (확인: device isolation matrix)
- **P3 우회 경로 위험**: 펌웨어 버그, ACS(Access Control Services) 미설정, peer-to-peer DMA가 IOMMU 보호 범위를 약화시킬 수 있음
- **P3 대응**: PCIe ACS, firmware update, DMA protection test로 우회 경로를 점검함 (확인: unauthorized DMA blocked)

> 요약: IOMMU는 DMA 격리를 제공하지만 변환 비용 최적화와 장치·펌웨어 우회 경로 검증을 함께 수행해야 함.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| GPU 패스스루 가상화 | IOMMU group을 분리하고 SR-IOV 또는 PCIe passthrough 장치를 VM(Virtual Machine)에 직접 할당함 | device isolation matrix, DMA fault count |
| 고속 네트워크 장치 | large page와 map/unmap batching으로 NIC(Network Interface Card) DMA 변환 오버헤드를 줄임 | IOTLB miss rate, packet p99 latency |
| 외부 포트 보안 | Thunderbolt 같은 외부 PCIe 장치에 DMA remapping과 device authorization을 적용함 | unauthorized DMA blocked |

> 요약: IOMMU 적용은 장치 직접 할당의 성능 이득과 DMA 격리 검증을 같은 기준으로 평가해야 함.

## 6. 결론

- **발전 방향**: confidential VM, CXL(Compute Express Link) device, DPU(Data Processing Unit), user-space driver 확산으로 장치 DMA 격리의 중요성이 더 커짐
- **기술사적 판단**: 고성능 장치 패스스루는 throughput뿐 아니라 DMA threat model과 IOMMU group 분리를 기준으로 승인해야 함
- **기술사 제언**: 서버 표준 이미지에는 IOMMU, interrupt remapping, ACS 검증 결과를 포함해 가상화 보안 기준으로 관리해야 함
