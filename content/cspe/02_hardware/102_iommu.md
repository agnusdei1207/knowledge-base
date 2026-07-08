---
title: "IOMMU (Input-Output Memory Management Unit)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 102
extra:
  question_no: "102"
  exam_status: "미출제"
---

## 미리 알고가기

- DMA는 장치가 CPU 개입 없이 메모리에 직접 접근하는 방식임
- IOVA는 장치가 사용하는 I/O 가상 주소임
- IOMMU는 장치 DMA 주소를 실제 메모리 주소로 변환하고 권한을 검사함

## Ⅰ. 개요

- **정의/개념**: IOMMU는 장치가 DMA로 접근하는 주소를 IOVA에서 물리 주소로 변환하고 장치별 접근 권한을 검사해 메모리 격리와 장치 직접 할당을 지원하는 하드웨어 메모리 관리 장치임
- **배경/필요성**: DMA 장치는 CPU MMU를 우회해 메모리에 접근하므로, 오류나 악성 장치가 임의 메모리를 손상시키지 않게 하려면 장치 전용 주소 변환과 권한 제어 계층이 필요함

## Ⅱ. 특징

- 장치 DMA 경로에 별도의 주소 변환과 접근 통제를 추가함
- SR-IOV와 PCI passthrough 같은 가상화 시나리오의 기본 보호 장치가 됨
- 장치별 domain 단위로 메모리 접근 범위를 나눌 수 있음
- IOTLB miss와 map or unmap 비용이 성능 저하 요인이 될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | IOMMU 미사용 | IOMMU 사용 |
|:---|:---|:---|
| DMA 주소 사용 | 물리 주소 직접 사용 | IOVA를 통한 변환 사용 |
| 보안 격리 | 장치 오동작 시 전체 메모리 위험 | 장치별 접근 범위 제한 가능 |
| 가상화 지원 | 패스스루 격리 어려움 | VM별 장치 직접 할당 가능 |
| 성능 특성 | 변환 오버헤드 적음 | IOTLB와 매핑 관리 비용 존재 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| DMA Device | NIC와 GPU와 NVMe처럼 직접 메모리 접근 요청을 생성하며 격리 대상의 출발점이 됨 |
| IOMMU Engine | 주소 변환과 권한 검사를 수행해 허용된 DMA만 메모리로 전달함 |
| I/O Page Table | 장치별 IOVA와 물리 주소 매핑을 저장해 접근 범위와 권한 정책을 결정함 |
| IOTLB | 자주 사용하는 변환 결과를 캐시해 고속 I/O에서 발생할 변환 지연을 완화함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 매핑 설정      | --> | DMA 요청 발생  | --> | 변환/권한 검사 | --> | 접근 허용/차단 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **매핑 설정**: OS나 하이퍼바이저가 장치 domain과 IOVA 매핑을 구성함
2. **DMA 요청 발생**: 장치가 IOVA 기반 읽기나 쓰기 요청을 보냄
3. **변환 및 권한 검사**: IOMMU가 IOTLB 또는 페이지 테이블을 사용해 주소와 권한을 확인함
4. **접근 허용 또는 차단**: 허용 요청은 메모리로 전달하고 위반 요청은 fault로 보고함

## Ⅵ. 문제점 및 해결 방안

1. 문제: IOTLB miss와 빈번한 map or unmap 작업이 고속 네트워크와 스토리지 지연을 높일 수 있음
   - 해결방안: large page와 batching 전략을 적용하고 IOTLB miss rate와 packet p99 latency로 검증함
2. 문제: SR-IOV와 passthrough 설정이 잘못되면 VM 간 장치 격리가 무너질 수 있음
   - 해결방안: IOMMU group과 interrupt remapping을 표준 검증하고 device isolation matrix와 DMA fault count로 검증함
3. 문제: ACS 미설정이나 펌웨어 결함이 있으면 peer-to-peer DMA 우회 경로가 남을 수 있음
   - 해결방안: ACS 활성화와 DMA protection test를 운영하고 unauthorized DMA block rate와 firmware compliance로 검증함

## Ⅶ. 적용 사례

- GPU passthrough 환경에서는 VM별 IOMMU group을 분리하고 확인 지표는 device isolation matrix와 DMA fault count임
- 고속 NIC 운영에서는 large page 기반 DMA 매핑을 적용하고 확인 지표는 IOTLB miss rate와 packet p99 latency임
- 외부 확장 포트 보안에서는 IOMMU와 장치 승인을 함께 적용하고 확인 지표는 unauthorized DMA block rate와 security incident count임

## Ⅷ. 결론

IOMMU는 성능 저하를 감수하고도 DMA 경계를 통제하는 장치이므로, 장치 직접 할당 환경에서는 선택 옵션이 아니라 기본 보안 기반임.
