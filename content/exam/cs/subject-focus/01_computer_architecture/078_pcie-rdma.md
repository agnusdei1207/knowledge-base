---
title: "PCIe·RDMA (Peripheral Component Interconnect express / Remote Direct Memory Access)"
date: "2026-06-30"
weight: 78
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> PCIe(Peripheral Component Interconnect express)는 직렬 차동 레인 기반 고속 시스템 버스 인터커넥트이며, RDMA(Remote Direct Memory Access)는 CPU·OS 개입 없이 원격 노드 메모리에 직접 접근하는 네트워크 기술이다.

## Ⅱ. 구성요소 / 원리
- PCIe: 포인트투포인트, 레인(x1~x16), 세대별 대역폭(Gen4·Gen5·Gen6)
- 패킷 기반 계층(트랜잭션·데이터링크·물리)
- RDMA: 커널 우회(Kernel Bypass), Zero-Copy, CPU 오프로드
- 구현: InfiniBand, RoCE(RDMA over Converged Ethernet), iWARP

## Ⅲ. 흐름도 / 구조
```text
PCIe: [CPU/Root]─lanes─[Switch]─[Endpoint:GPU/NIC/SSD]
RDMA: [App A 메모리]──NIC──network──NIC──[App B 메모리]
        └ CPU/커널 우회, Zero-Copy 직접 전송
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 고대역폭 장치연결 / 저지연 원격 메모리 접근 |
| 장점 | 대역폭 확장, CPU 부하 제거, 마이크로초 지연 |
| 한계 | 거리 제약(PCIe), 무손실망 요구(RoCE), 비용 |

## Ⅴ. 기술사적 적용
- NVMe-oF·GPUDirect RDMA로 AI 클러스터 데이터 이동 가속
- CXL이 PCIe 물리계층 위에 캐시 일관성 메모리 확장
- HPC·분산학습 노드간 통신(All-Reduce) 핵심 인프라
