---
title: "NVMe·NVMe-oF (Non-Volatile Memory express / NVMe over Fabrics)"
date: "2026-06-30"
weight: 77
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> NVMe(Non-Volatile Memory express)는 PCIe 기반 SSD를 위한 고속 저지연 인터페이스 프로토콜이며, NVMe-oF(NVMe over Fabrics)는 이를 네트워크 패브릭으로 확장해 원격 스토리지를 블록 접근하는 표준이다.

## Ⅱ. 구성요소 / 원리
- 다중 큐: 최대 64K 큐 × 큐당 64K 명령으로 병렬성 극대화
- 경량 명령셋, 낮은 레이턴시, MSI-X 인터럽트 분산
- NVMe-oF 전송: RDMA(RoCE/iWARP/InfiniBand), FC, TCP
- 캡슐(Capsule) 기반 명령 전달, 원격을 로컬처럼 접근

## Ⅲ. 흐름도 / 구조
```text
NVMe:    [Host]─PCIe─[Submission/Completion Queue]─[SSD]
NVMe-oF: [Host]─Fabric(RDMA/TCP/FC)─[Target]─[NVMe SSD]
            └ 다중 큐 매핑으로 병렬 전송
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | SSD 잠재성능 활용·스토리지 분리(Disaggregation) |
| 장점 | 초저지연, 대규모 병렬큐, 확장성 |
| 한계 | 패브릭 인프라 필요, 구현 복잡, 호환성 |

## Ⅴ. 기술사적 적용
- AHCI/SATA 대비 큐·지연에서 압도적 우위
- NVMe over TCP로 기존 이더넷 인프라 재활용
- 분리형 스토리지(Composable Infra)·AI 데이터 파이프라인에 적용
