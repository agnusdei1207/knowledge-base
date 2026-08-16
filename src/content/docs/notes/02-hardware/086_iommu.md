---
sidebar:
  order: 86
  label: "086. 입출력 메모리 관리 장치 (IOMMU)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "입출력 메모리 관리 장치 (IOMMU)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "DMA 주소•권한 격리와 IOTLB 비용"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 디바이스의 DMA(Direct Memory Access) 트랜잭션 상에서 입출력 가상 주소(IOVA)를 물리 주소(HPA)로 변환하고 메모리 접근 권한을 검증하는 하드웨어 (Intel VT-d / AMD-Vi).
- **IOVA(Input/Output Virtual Address)**: I/O 디바이스가 DMA 수행 시 사용하는 입출력 가상 주소.
- **DMA(Direct Memory Access)**: CPU 관여 없이 PCI/PCIe 디바이스가 호스트 DRAM 메모리를 직접 읽고 쓰는 고속 전송 기술.

</details>

- 정의/개념: I/O 디바이스의 **IOVA** 가상 주소를 호스트 물리 주소로 재매핑하고 **DMA** 트랜잭션 수용 권한을 검증 제어하는 **IOMMU**
- 배경/필요성: 무검증 물리 DMA 수행 시 악의적/오류 디바이스에 의한 OS 커널 메모리 오염 및 VM 간 메모리 침범 파급 차단 요구성

#### 한줄 요약

- IOMMU는 IOVA 변환과 DMA 권한 검사를 함께 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: 최근 완료된 IOVA->HPA 변환 래칭 데이터를 보관하는 IOMMU 내장 초고속 캐시.
- **IOMMU Domain**: 가상 머신(VM) 또는 특정 디바이스 그룹별로 독립된 I/O 페이지 테이블을 할당하여 메모리를 격리하는 논리 보안 영역.
- **SR-IOV(Single Root I/O Virtualization)**: 단일 물리 PCIe 장치를 복수의 VF(Virtual Function)로 쪼개어 VM에 1:1 패스스루 할당하는 기술.

</details>

- 장치·VM별 허용 메모리를 구분하는 **IOMMU Domain** 격리
- **IOVA** 연속 주소를 비연속 물리 페이지에 매핑
- **SR-IOV**와 연동한 가상 기능별 직접 DMA 제공

#### 한줄 요약

- IOMMU 도메인 격리와 IOTLB 미스•무효화 비용이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **I/O Page Table**: IOVA를 물리 주소와 읽기·쓰기 권한에 매핑하는 하드웨어 변환표.
- **Device Context Table**: PCIe BDF(Bus:Device:Function) 식별자 기반으로 해당 디바이스의 IOMMU Domain 매핑 정보를 저장하는 인덱스 테이블.

</details>

```text
[도메인 관리자] -- [페이지 테이블] -- [IOMMU•IOTLB] -- [DMA 장치]
```

선의 의미: 도메인 관리자가 I/O 페이지 테이블을 관리하고, IOMMU/IOTLB 하드웨어가 이를 통하여 DMA 장치 트랜잭션을 실시간 검증하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 도메인 관리자 | **IOMMU Domain** 할당, 디바이스 Passthrough 바인딩 및 커널 매핑 관리 |
| 페이지 테이블 | **IOVA**와 HPA 변환 및 읽기·쓰기 접근 권한 매핑 보관 |
| IOMMU•IOTLB | **IOTLB** 캐싱, 페이지 순회와 DMA 주소·권한 검증 |
| DMA 장치 | **IOVA** 주소를 포함한 PCIe 읽기·쓰기 TLP 능동 발행 |

#### 한줄 요약

- 도메인 관리자, 페이지 테이블, IOMMU•IOTLB가 DMA 접근 경계를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOMMU Fault**: 비인가 주소 억세스, 권한 위반 또는 미할당 IOVA DMA 요청 발생 시 하드웨어가 트랜잭션을 차단하고 트리거하는 예외 신호.

</details>

```text
[DMA 장치의 IOVA•식별자]
             │
             ▼
1. IOMMU 도메인 선택
             │
             ▼
2. IOTLB 변환 조회
       ┌─────┴─────────┐
       │ 적중          │ 미스
       │               ▼
       │       3. 페이지 테이블 순회
       │               │
       └───────┬───────┘
               ▼
4. 주소•권한 검증
       ┌───────┴────────┐
       │ 허용           │ 위반
       ▼                ▼
[물리 DMA 접근]   5. IOMMU 폴트•차단
       │
       ▼
   [DMA 완료]
```

### 동작 원리

1. IOMMU 도메인 선택: PCIe BDF 수치를 매핑하여 디바이스에 해당하는 **IOMMU Domain** 식별.
2. IOTLB 변환 조회: 인가된 **IOVA** 주소의 **IOTLB** 캐시 적중 여부 파악.
3. 페이지 테이블 순회: 캐시 Miss 발생 시 하드웨어 **I/O Page Table** 순회(Page Walk) 수행.
4. 주소·권한 검증: 요청된 DMA 트랜잭션의 읽기·쓰기 접근 권한 검증.
5. IOMMU 폴트·차단: 매핑·권한 위반 시 **IOMMU Fault**를 기록하고 DMA 요청 차단.

#### 한줄 요약

- IOMMU는 IOMMU 도메인 선택, IOTLB 변환 조회, 주소·권한 검증을 모두 통과한 DMA 요청만 메모리로 전달한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Passthrough**: 물리 PCIe 장치 제어권을 특정 VM에 직접 할당하는 기능.

</details>

| 비교 항목 | IOMMU 활성화 (VT-d Enabled) | IOMMU 비활성화 (Bypass Mode) |
|:---|:---|:---|
| 주소 변환 | **IOVA**에서 HPA로 재매핑 | 물리 주소 또는 항등 매핑 사용 |
| 보안 격리성 | **IOMMU Domain**별 DMA 범위와 권한 제한 | 장치 DMA의 메모리 범위 제한 어려움 |
| 가상화 적용 | VM **Passthrough**와 **SR-IOV** 직접 할당 지원 | 직접 할당 격리 불가, 가상 장치 경로 사용 |
| 성능 오버헤드 | **IOTLB Miss**와 무효화 비용 발생 | 주소 번역 비용은 낮으나 격리 약화 |

#### 한줄 요약

- 외부 장치와 VM 직접 할당 장치에는 필요한 버퍼만 노출하는 최소 권한 매핑을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IOTLB Invalidation**: I/O 매핑 갱신/해제 시 캐시 상의 만료된 IOTLB 변환 정보를 명시적 파기하는 하드웨어 플러시.

- **인텔 I/O 가상화 기술(Intel VT-d)**: CPU MMU와 독립적으로 작동하여 PCIe 주변장치의 가상 DMA 주소를 물리 호스트 주소로 매핑하고 인터럽트를 재매핑하는 하드웨어 유닛.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잦은 **IOTLB Miss**로 인한 DMA 처리량 하락 | 큰 페이지 I/O 매핑과 배치 처리 | IOTLB 커버리지 확대와 순회 감소 |
| 매핑 해제 후 잔여 캐시로 인한 메모리 오염 위험 | **IOTLB Invalidation**을 완료한 뒤 페이지 재사용 | 해제 페이지로 향하는 잔여 DMA 방지 |
| 비인가 PCIe 장치의 무단 DMA 접근 공격 | 기본 거부 도메인과 최소 권한 매핑 | DMA로 노출되는 메모리 범위 제한 |

> 사례: **Intel VT-d** 및 **SR-IOV** 결합을 통한 VM 패킷 처리 지연 극소화 시스템 구현

#### 한줄 요약

- 장치별 드라이버 버퍼에 최소 권한 매핑을 적용하고 변경•해제할 때 IOTLB 무효화를 수행한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **IOMMU 채택 기준(IOMMU Adoption Criteria)**: 디바이스 Passthrough 여부, 보안 격리 등급 및 DMA 스루풋에 기반한 체계.

</details>

- VM 직접 할당·비신뢰 DMA는 **IOMMU 격리**, 고정 신뢰 경로는 **항등 매핑** 검토

#### 한줄 요약

- VM 직접 할당과 비신뢰 DMA에는 IOMMU 최소 권한 도메인을 적용한다.
