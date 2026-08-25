---
sidebar:
  order: 86
  label: "086. IOMMU (Input-Output Memory Management Unit)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "IOMMU (Input-Output Memory Management Unit)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "DMA 주소 변환(IOVA to HPA)과 하드웨어 메모리 격리의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 입출력 장치의 DMA 요청 시 I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 메모리 접근 권한을 제어하는 하드웨어 모듈(Intel VT-d, AMD-Vi, ARM SMMU).
- **IOVA(Input/Output Virtual Address)**: 디바이스 드라이버와 장치 DMA 컨트롤러가 사용하는 가상 I/O 메모리 주소 체계.

</details>

- 정의/개념: 입출력 디바이스의 DMA 요청 시 **IOVA**를 호스트 물리 주소(HPA)로 변환하고 권한을 통제하는 **IOMMU**
- 배경/필요성: 기존 직접 DMA 구조는 CPU 메모리 권한 검사를 우회하므로 **악성 장치의 물리 메모리 무단 침범 차단 불가**

#### 한줄 요약
- I/O 디바이스의 DMA 접근을 가상 주소로 변환하고 하드웨어 격리를 수행하여 시스템 안정성과 가상화 패스스루를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: IOMMU 내부에서 최근 변환된 IOVA $\to$ HPA 주소 매핑 엔트리를 캐싱하여 페이지 테이블 탐색 오버헤드를 줄이는 고속 캐시.
- **도메인 격리(IOMMU Domain Isolation)**: 장치 집합마다 독립 I/O 페이지 테이블과 권한을 적용해 DMA 가능 범위를 제한하는 기법.

</details>

- 장치(BDF)별로 독립된 I/O 가상 주소 공간을 할당하는 **도메인 격리**
- 물리적으로 흩어진 불연속 메모리 페이지를 디바이스 관점에서 단일 연속 가상 버퍼로 매핑(Scatter-Gather 가속)
- **IOTLB** 캐싱 및 인터럽트 리매핑(Interrupt Remapping)을 통한 가상 머신(VM) 직결 패스스루 지원

#### 한줄 요약
- 도메인 격리로 악성 DMA를 차단하고 Scatter-Gather 주소 연속화로 I/O 성능을 최적화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **장치 컨텍스트 테이블(Device Context Table)**: PCIe 장치의 BDF(Bus:Device:Function) 번호를 인덱스로 하여 해당 장치가 속한 IOMMU 도메인의 페이지 테이블 루트 포인터를 찾는 테이블.
- **I/O 페이지 테이블(I/O Page Table)**: IOVA와 물리 메모리 주소(HPA) 간의 매핑 정보와 읽기/쓰기(R/W) 권한 플래그를 담은 다단계 테이블.

</details>

```text
[IOMMU 하드웨어 주소 변환 및 격리 아키텍처]
|-- PCIe 엔드포인트 장치 (BDF 식별자 + IOVA 기반 DMA 요청 발행)
|-- IOMMU 하드웨어 엔진 (Intel VT-d / AMD-Vi / ARM SMMU)
|   |-- 장치 컨텍스트 테이블 (BDF -> 도메인 I/O 페이지 테이블 포인터 검색)
|   |-- IOTLB 캐시 유닛 (최근 주소 변환 엔트리 고속 캐싱)
|   |-- 다단계 I/O 페이지 워커 (IOVA -> HPA 변환 및 R/W 권한 검사)
|   `-- 인터럽트 리매핑 유닛 (MSI/MSI-X 가상 인터럽트 라우팅)
`-- 호스트 시스템 메모리 (HPA 격리 보호 도메인)
```

선의 의미: 계층 및 주소 변환 트랜잭션 흐름

| 구성요소 | 책임 |
|:---|:---|
| PCIe 장치 (BDF) | 버스·디바이스·기능 번호를 헤더에 싣고 IOVA 가상 주소로 DMA 요청 |
| **장치 컨텍스트 테이블** | BDF 번호로 소속 가상화 도메인을 찾고 I/O 페이지 테이블 루트 포인터 획득 |
| **IOTLB 캐시 유닛** | 최근 변환된 IOVA $\to$ HPA 매핑을 캐싱하여 페이지 테이블 순회 지연 단축 |
| I/O 페이지 테이블 워커 | IOTLB 미스 시 4단계 페이징을 탐색하여 물리 주소 산출 및 권한 검증 |
| 인터럽트 리매핑 유닛 | 디바이스 MSI/MSI-X 인터럽트를 대상 게스트 vCPU로 안전하게 변환 라우팅 |

#### 한줄 요약
- BDF 컨텍스트 테이블, IOTLB 캐시, I/O 페이지 테이블 워커, 인터럽트 리매핑기가 결합된 구조다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOMMU Fault**: 매핑되지 않은 주소 접근, 쓰기 금지 영역 쓰기 시도, 권한 없는 BDF 요청 시 트랜잭션을 강제 차단하고 시스템 로그를 남기는 하드웨어 예외.

</details>

```text
PCIe 장치가 BDF 번호와 함께 IOVA 주소로 DMA 요청 전송
        │
   IOMMU가 BDF 기반으로 장치 컨텍스트 테이블 조회
        │
   해당 IOVA 변환 엔트리가 IOTLB 캐시에 존재하는가?
   ┌────┴─────┐
  예           아니오
   │             │
   │        다단계 I/O 페이지 테이블 워크 수행
   └────┬────────┘
        │
   요청된 R/W 동작이 I/O 페이지 테이블 권한과 일치하는가?
   ┌────┴─────┐
  예           아니오
   │             │
호스트 물리 메모리로   IOMMU Fault 발생 → DMA 트랜잭션 강제 차단
DMA 데이터 전송 완료   및 커널 시스템 로그 기록
```

#### 한줄 요약
- DMA 인입 → BDF 컨텍스트 조회 → IOTLB/페이지 워크 → 권한 검증 후 HPA 전송 또는 IOMMU Fault 차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Bypass Mode**: IOMMU 주소 변환을 끄고 물리 주소를 직접 사용하여 초저지연을 얻는 베어메탈 모드.
- **바운스 버퍼(Bounce Buffer)**: IOMMU가 없을 때 32비트 장치를 위해 64비트 메모리 데이터를 중간 버퍼로 복사해 전달하는 소프트웨어 기법.

</details>

| IOMMU 동작 모드 | IOMMU 활성화 (Strict Mode) | IOMMU 우회 (Bypass Mode) | 소프트웨어 바운스 버퍼 | 에뮬레이션 가상 I/O |
|:---|:---|:---|:---|:---|
| 적용 기준 | 가상화 클라우드 및 고보안 제로 트러스트 | 베어메탈 HPC 초저지연 연산 | 32비트 레거시 구형 하드웨어 | 단순 범용 하이퍼바이저 가상화 |
| 핵심 특징 | IOVA 변환·권한 검증과 장치 도메인 격리 | 주소 변환 없이 물리 주소 직접 사용 | 접근 가능한 메모리로 임시 복사 | 하이퍼바이저가 가상 장치 동작 중개 |
| 한계 | IOTLB 미스·무효화와 페이지 워크 비용 | 장치 오류·공격의 DMA 범위 제한 곤란 | CPU 복사와 버퍼 관리 비용 | VM-Exit·에뮬레이션 비용 증가 |

#### 한줄 요약
- 가상화 및 보안 환경에는 IOMMU Strict 모드가 필수적이며, 고성능 HPC에서는 제한적으로 Bypass 모드가 활용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IOTLB Invalidation**: DMA 버퍼 해제(Unmap) 시 IOTLB 캐시에 남아 있는 잔여 주소 엔트리를 강제로 플러시하여 Use-After-Free DMA 보안 취약점을 막는 명령.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잦은 IOTLB 미스로 인한 고속 NIC/GPU 처리율 저하 | IOMMU 2MB 대용량 페이지(Huge Page) 및 지연 무효화(Lazy) 적용 | IOTLB 적중률 99% 달성 및 DMA 지연 최소화 |
| DMA 버퍼 해제 후 잔여 캐시로 인한 무단 접근 | 버퍼 Unmap 시 즉각적인 **IOTLB Invalidation** 명령 강제 수행 | DMA Use-After-Free 및 메모리 유출 차단 |
| 썬더볼트/외부 PCIe 포트를 통한 악성 DMA 공격 | 부팅 전 IOMMU 활성화(Kernel DMA Protection) 정책 수립 | 비인가 외부 장치의 물리 메모리 덤프 차단 |
| 패스스루 VM 간 장치 인터럽트 간섭 | 하드웨어 **인터럽트 리매핑(Interrupt Remapping)** 활성화 | 가상 머신 간 인터럽트 격리 및 오동작 방지 |

#### 한줄 요약
- Huge Page 적용, IOTLB 즉각 무효화, Kernel DMA Protection, 인터럽트 리매핑으로 성능과 보안을 동시에 달성한다.

## Ⅶ. 결론

- 클라우드 가상화 및 AI 인프라는 **IOMMU 기반 하드웨어 DMA 격리**를 필수 구축하고, **인터럽트 리매핑 및 Huge Page**를 결합하여 보안과 성능 양립

#### 한줄 요약
- IOMMU는 CPU의 MMU와 대등하게 I/O 서브시스템의 가상화와 메모리 보안을 책임지는 핵심 하드웨어 아키텍처다.