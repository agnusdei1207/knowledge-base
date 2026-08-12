---
sidebar:
  order: 86
  label: "086. 입출력 메모리 관리 장치 (IOMMU)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "입출력 메모리 관리 장치 (IOMMU)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 디바이스의 DMA(Direct Memory Access) 트랜잭션 상에서 입출력 가상 주소(IOVA)를 물리 주소(HPA)로 변환하고 메모리 접근 권한을 검증하는 하드웨어 (Intel VT-d / AMD-Vi).
- **IOVA(Input/Output Virtual Address)**: I/O 디바이스가 DMA 수행 시 억세스하는 입출력 가상 메모리 주소.
- **DMA(Direct Memory Access)**: CPU 관여 없이 PCI/PCIe 디바이스가 호스트 DRAM 메모리를 직접 읽고 쓰는 고속 전송 기술.

</details>

- 정의/개념: I/O 디바이스의 **IOVA** 가상 주소를 호스트 물리 주소로 재매핑하고 **DMA** 트랜잭션 수용 권한을 검증 제어하는 **IOMMU**
- 배경/필요성: 무검증 물리 DMA 수행 시 악의적/오류 디바이스에 의한 OS 커널 메모리 오염 및 VM 간 메모리 침범 파급 차단 요구성

#### 한줄 요약

- IOMMU는 IOVA 변환과 DMA 권한 검사를 함께 수행한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: 최근 완료된 IOVA->HPA 변환 래칭 데이터를 보관하는 IOMMU 내장 초고속 캐시.
- **IOMMU Domain**: 가상 머신(VM) 또는 특정 디바이스 그룹별로 독립된 I/O 페이지 테이블을 할당하여 메모리를 격리하는 논리 보안 영역.
- **SR-IOV(Single Root I/O Virtualization)**: 단일 물리 PCIe 장치를 복수의 VF(Virtual Function)로 쪼개어 VM에 1:1 패스스루 할당하는 기술.

</details>

- VM 간 및 디바이스 간 메모리 간섭을 원천 차단하는 **IOMMU Domain** 독립 격리
- **IOVA** 기반 가상 주소 변환을 통한 4GB 이상 리컨티규어스 물리 메모리 서빙
- **SR-IOV** 기법과 연동된 무중단 하드웨어 직결(Passthrough) DMA 제공

#### 한줄 요약

- IOMMU 도메인 격리와 IOTLB 미스•무효화 비용이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **I/O Page Table**: IOVA 주소를 4KB/2MB 단위의 물리 주소(HPA) 및 Read/Write 억세스 권한 비트와 바인딩한 하드웨어 변환표.
- **Device Context Table**: PCIe BDF(Bus:Device:Function) 식별자 기반으로 해당 디바이스의 IOMMU Domain 매핑 정보를 저장하는 인덱스 테이블.

</details>

```text
[도메인 관리자] -- [페이지 테이블] -- [IOMMU•IOTLB] -- [DMA 장치]
```

선의 의미: 도메인 관리자가 I/O 페이지 테이블을 관리하고, IOMMU/IOTLB 하드웨어가 이를 통하여 DMA 장치 트랜잭션을 실시간 검증하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 도메인 관리자 | **IOMMU Domain** 할당, 디바이스 Passthrough 바인딩 및 커널 매핑 관리 |
| 페이지 테이블 | **IOVA** 대 HPA 변환 포인터 및 R/W 억세스 권한 비트 맵핑 보관 |
| IOMMU•IOTLB | **IOTLB** 캐싱, 2단계 페이지 걷기(Page Walk) 및 DMA 트랜잭션 실시간 라우팅 |
| DMA 장치 | **IOVA** 주소를 동반한 PCIe Read/Write TLP 패킷 능동 발상 |

#### 한줄 요약

- 도메인 관리자, 페이지 테이블, IOMMU•IOTLB가 DMA 접근 경계를 구성한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

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

1. **IOMMU 도메인 선택**: PCIe BDF 수치를 매핑하여 디바이스에 해당하는 **IOMMU Domain** 식별.
2. **IOTLB 변환 조회**: 인가된 **IOVA** 주소의 **IOTLB** 캐시 적중 여부 파악.
3. **페이지 테이블 순회**: 캐시 Miss 발생 시 하드웨어 **I/O Page Table** 순회(Page Walk) 수행.
4. **주소·권한 검증**: 요청된 DMA 트랜잭션의 R/W 억세스 권한 비트 검증.
5. **허용 또는 폴트 처리**: 정상 승인 시 물리 DMA 전송, 권한 위반 시 **IOMMU Fault** 강제 발생 및 패킷 차단.

#### 한줄 요약

- IOMMU는 IOMMU 도메인 선택, IOTLB 변환 조회, 주소·권한 검증을 모두 통과한 DMA 요청만 메모리로 전달한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Passthrough**: 하이퍼바이저 억세스를 우회하여 물리 PCIe 장치 제어권을 특정 VM에 1:1 직접 넘겨주는 기능.

</details>

| 비교 항목 | IOMMU 활성화 (VT-d Enabled) | IOMMU 비활성화 (Bypass Mode) |
|:---|:---|:---|
| 주소 변환 | **IOVA** -> HPA 가상 주소 재매핑 | 물리 HPA 주소 직접 인가 (No Translation) |
| 보안 격리성 | 완전 격리 (**IOMMU Domain** / Fault 차단) | 보안 격리 전무 (오류 장치가 타 메모리 침범 수용) |
| 가상화 적용 | VM 전용 **Passthrough** 및 **SR-IOV** 수용 가능 | 가상화 1:1 장치 직결 불가 (SW 에뮬레이션 전용) |
| 성능 오버헤드 | **IOTLB Miss** 시 페이징 미세 지연 발생 (~ns) | 번역 오버헤드 제로 |

#### 한줄 요약

- 외부 장치와 VM 직접 할당 장치에는 필요한 버퍼만 노출하는 최소 권한 매핑을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **IOTLB Invalidation**: I/O 매핑 갱신/해제 시 캐시 상의 만료된 IOTLB 변환 정보를 명시적 파기하는 하드웨어 플러시.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **IOTLB Miss** 잦은 발생으로 인한 DMA 스루풋 하락 | **Huge Pages (2MB/1GB)** I/O 매핑 수용 | IOTLB 커버리지 확대 및 지연 단축 |
| 매핑 해제 후 잔여 캐시로 인한 메모리 오염 위험 | **IOTLB Invalidation** 명령어 즉시 인가 | 해제 메모리 무단 억세스 차단 |
| 비인가 PCIe 디바이스의 무단 DMA 억세스 공격 | 칩셋 차원 **IOMMU Strict Mode** 인가 | DMA 기반 하드웨어 덤프 차단 |

> 사례: **Intel VT-d** 및 **SR-IOV** 결합을 통한 VM 패킷 처리 지연 극소화 시스템 구현

#### 한줄 요약

- 장치별 드라이버 버퍼에 최소 권한 매핑을 적용하고 변경•해제할 때 IOTLB 무효화를 수행한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **IOMMU 채택 기준(IOMMU Adoption Criteria)**: 디바이스 Passthrough 여부, 보안 격리 등급 및 DMA 스루풋에 기반한 체계.

</details>

- **IOMMU 채택 기준**에 따라 가상화 데이터센터, SR-IOV 및 고보안 클라우드 인프라에 **IOMMU(VT-d/AMD-Vi)** 필수 적용

#### 한줄 요약

- 장치별 최소 권한 매핑과 IOTLB 무효화 빈도를 최적화한다.
