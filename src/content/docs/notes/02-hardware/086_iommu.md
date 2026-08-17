---
sidebar:
  order: 86
  label: "086. 입출력 메모리 관리 장치 (IOMMU)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "입출력 메모리 관리 장치 (IOMMU)"
date: "2026-08-17T09:25:00+09:00"
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

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 입출력 디바이스의 DMA 요청 시 가상 주소(IOVA)를 물리 주소(HPA)로 변환하고 메모리 접근 권한을 제어하는 하드웨어 장치(Intel VT-d, AMD-Vi, ARM SMMU).
- **IOVA(Input/Output Virtual Address)**: 디바이스 드라이버 및 DMA 컨트롤러가 사용하는 가상 I/O 메모리 주소.
- **DMA(Direct Memory Access)**: CPU의 개입 없이 주변장치(NIC, GPU, NVMe)가 시스템 물리 메모리에 직접 데이터를 읽고 쓰는 기술.

</details>

- 정의/개념: 입출력 디바이스(NIC, GPU, NVMe)의 직접 메모리 접근(DMA) 요청 시, I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 메모리 접근 권한을 검증 및 격리하는 하드웨어 유닛(Intel VT-d / AMD-Vi)
- 배경/필요성: 32비트 DMA 장치의 64비트 메모리 접근 지원(바운스 버퍼 제거), 불법적 DMA 공격(악성 펌웨어/Thunderbolt) 방어 및 **가상 머신(VM)에 물리 디바이스를 안전하게 직결(Device Passthrough)하는 하드웨어 격리 필수**

#### 한줄 요약

- I/O 디바이스의 DMA 주소 변환(IOVA $\to$ HPA) 및 **메모리 접근 권한 하드웨어 격리를 수행하는 IOMMU(VT-d)**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: IOMMU 내부에서 최근 변환된 IOVA $\to$ HPA 매핑 정보를 캐싱하여 페이지 테이블 탐색 오버헤드를 줄이는 고속 캐시.
- **IOMMU Domain**: 특정 가상 머신(VM) 또는 프로세스에 할당된 독립된 I/O 가상 주소 공간 및 페이지 테이블 격리 단위.
- **SR-IOV Passthrough**: 단일 물리 PCIe 장치를 복수의 가상 기능(VF)으로 분할하여 각 VM의 IOMMU 도메인에 1:1 직결하는 고성능 I/O 가상화.

</details>

- 장치 및 VM별로 독립된 I/O 가상 주소 공간을 할당하여 무단 메모리 침범을 방지하는 **IOMMU 도메인 하드웨어 격리**
- 불연속적인 물리 메모리 페이지들을 디바이스에게는 연속적인 단일 버퍼로 노출하는 **IOVA 가상 주소화(Scatter-Gather 에뮬레이션)**
- 하이퍼바이저 중계 오버헤드 없이 가상 머신에 물리 NIC/GPU를 1:1 매핑하는 **SR-IOV 및 디바이스 패스스루(Passthrough)**

#### 한줄 요약

- **IOMMU 도메인별 메모리 격리·IOVA 비연속 물리 페이지 매핑·SR-IOV 및 Device Passthrough 지원**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **I/O Page Table**: IOVA와 물리 메모리 주소 간의 매핑 및 읽기/쓰기 권한(Read/Write Bit)을 정의한 다단계 페이지 테이블.
- **Device Context Table**: PCIe 장치의 BDF(Bus:Device:Function) 번호를 인덱스로 하여 해당 장치가 속한 IOMMU 도메인의 페이지 테이블 루트 포인터를 지정하는 테이블.

</details>

```text
[ IOMMU 하드웨어 주소 변환 및 격리 아키텍처 ]
┌─────────────────────────────────────────────────────────────┐
│ 1. PCIe DMA 장치 (GPU / 100GbE NIC : BDF 01:00.0)           │
└──────────────────────────────┬──────────────────────────────┘
                               │ [ DMA Read/Write 요청 : <BDF, IOVA> ]
┌──────────────────────────────┴──────────────────────────────┐
│ 2. IOMMU 하드웨어 엔진 (Intel VT-d / AMD-Vi / ARM SMMU)      │
│  ├─ 장치 컨텍스트 테이블 (BDF ──> 도메인 페이지 테이블 매핑)│
│  ├─ 3. IOTLB 캐시 (초고속 IOVA <──> HPA 캐시 탐색)          │
│  └─ 4. 입출력 페이지 테이블 워커 (Multi-Level Page Walk)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ [ 5. 검증 완료된 물리 주소 (HPA) DMA 실행 ]
┌──────────────────────────────┴──────────────────────────────┐
│ 6. 호스트 시스템 물리 메모리 (Host Physical Memory)         │
└─────────────────────────────────────────────────────────────┘
```

선의 의미: DMA 요청 디바이스(BDF), IOTLB 캐시, I/O 페이지 테이블 변환 엔진 및 호스트 물리 메모리 간의 IOMMU 아키텍처 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 도메인 관리자 | "이 VM은 저 그래픽카드 써" 하고 짝을 지어주고(**도메인** 할당), 주소 변환표를 세팅하는 총책임자 |
| 입출력 페이지 테이블 | 가짜 주소(IOVA)를 진짜 주소(HPA)로 번역하고, "여긴 읽기만 해라" 하고 권한까지 쾅쾅 박아둔 번역 장부 |
| IOMMU•IOTLB | 번역표(장부)를 미친 듯이 뒤져서 주소를 바꾸고, 방금 찾은 건 **IOTLB** 캐시에 짱박아두는 톨게이트 |
| DMA 장치 | 뇌 비우고 그냥 IOVA 주소 들이밀면서 "데이터 내놔!" 하고 **DMA** 요청을 날려대는 무식한 노가다 장비 |

#### 한줄 요약

- **도메인 관리자·입출력 페이지 테이블(I/O Page Table)·IOMMU 변환기 및 IOTLB·DMA 엔드포인트 장치**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOMMU Fault**: 매핑되지 않은 주소 접근, 권한 위반(쓰기 금지 구역 쓰기), 잘못된 BDF 접근 시 IOMMU가 인터럽트를 발생시키고 트랜잭션을 차단하는 이벤트.

</details>

```text
[ IOMMU DMA 주소 변환 및 접근 제어 시퀀스 ]
                         │
                         ▼
   [ 1. PCIe 장치가 BDF 및 IOVA 를 싣고 DMA 메모리 접근 요청 인가 ]
                         │
                         ▼
   [ 2. IOTLB 캐시 조회 : 최근 변환 엔트리 존재 여부 확인 ]
        /                                               \
   [ IOTLB Hit ]                                  [ IOTLB Miss ]
        │                                               │
        │                                         [ 3. I/O 페이지 테이블 워크 수행 ]
        │                                               │
        │                                         [ 4. 변환 엔트리 IOTLB 에 적재 ]
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
   [ 5. 읽기/쓰기 권한 검증 및 도메인 범위 유효성 체크 ]
        /                                               \
   [ 권한 유효 (정상) ]                           [ 권한 위반 / 미매핑 주소 ]
        │                                               │
   [ 호스트 물리 메모리로 DMA 전송 허용 ]         [ 6. IOMMU Fault 발생 및 DMA 차단 ]
```

**동작 원리**

1. **DMA 요청**: PCIe 엔드포인트 장치가 자신의 BDF 식별자와 대상 IOVA 주소를 담은 메모리 TLP 전송
2. **IOTLB 검색**: IOMMU가 내부 IOTLB 캐시를 조회하여 주소 변환 엔트리 즉시 확인
3. **페이지 워크**: IOTLB Miss 시 컨텍스트 테이블에서 도메인을 찾고 I/O 페이지 테이블을 순회하여 물리 주소(HPA) 도출
4. **권한 검증**: 해당 페이지 엔트리의 R/W 권한 비트와 DMA 요청 유형이 일치하는지 대조
5. **트랜잭션 결말**: 인가된 요청은 물리 메모리로 포워딩, 위반된 요청은 즉각 드롭하고 IOMMU Fault 로깅

#### 한줄 요약

- BDF 장치 식별 $\to$ **IOTLB 캐시 히트 검사 $\to$ I/O 페이지 테이블 워크(IOVA $\to$ HPA) $\to$ 읽기/쓰기 권한 검증 $\to$ 물리 메모리 DMA 허용 / 위반 시 IOMMU Fault 차단**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IOMMU Enabled vs Bypass Mode**:
  - Enabled: IOVA $\to$ HPA 변환, VM 디바이스 패스스루, DMA 하드웨어 격리, 약간의 레이턴시
  - Bypass: 변환 없음(HPA 직결), 베어메탈 최고 속도, DMA 공격에 완전 무방비

</details>

| 비교 항목 | IOMMU 활성화 모드 (VT-d / Strict Mode) | IOMMU 비활성화 / 우회 모드 (Pass-Through / Bypass) |
|:---|:---|:---|
| 주소 변환 및 가상화 | IOVA $\to$ HPA 변환 수행, VM 디바이스 패스스루 완벽 지원 | 변환 없이 물리 주소(HPA) 직결, VM 간 하드웨어 격리 불가 |
| 보안성 및 DMA 보호 | 도메인별 메모리 격리, 악성 DMA 공격(Thunderbolt) 완벽 차단 | 비신뢰 장치의 시스템 커널 및 전 영역 메모리 변조 위험 노출 |
| 한계 및 오버헤드 | IOTLB 미스 시 페이지 워크 레이턴시 발생 (1~5% 오버헤드) | 보안성 0 (베어메탈 최고 속도 전용) |

#### 한줄 요약

- 가상화/보안 격리는 **IOMMU 활성화(VT-d)**, 극단적 초저지연은 **Bypass 모드**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IOTLB Invalidation**: DMA 버퍼 해제(Unmap) 시 IOMMU 캐시에 남아있는 무효 엔트리를 강제로 플러시하여 Use-After-Free DMA 보안 취약점을 차단하는 동작.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 캐시 못 찾고 장부 뒤지는 짓(**IOTLB Miss**)을 너무 자주 해서 10기가 랜카드 속도가 반토막 나는 끔찍한 병목 터짐 | 찌끄레기 페이지 대신 거대한 통짜 페이지(Huge Pages)로 묶어서 번역표 덩치를 줄여버림 | 캐시 폭발을 씹어먹고 메모리 번역 딜레이를 극한까지 깎아내려 무지막지한 전송량 사수 |
| 메모리 다 쓰고 반납했는데 캐시(**IOTLB**)에 옛날 주소가 남아있어서, 엉뚱한 장치가 남의 새 메모리를 쑤셔버리는 재앙 | 매핑 끊을 때마다 "이 주소 캐시 싹 다 지워라!" 하고 **입출력 변환 색인 버퍼 무효화** 명령어를 얄짤없이 날림 | 잔여 캐시 때문에 생기는 치명적인 보안 펑크와 데이터 오염을 100% 원천 차단 |
| 해킹당한 싸구려 랜카드가 DMA를 갈겨서 윈도우 커널을 통째로 파괴하려는 무차별 묻지마 공격 시전 | 아예 기본 설정을 '전부 차단'으로 걸고, 딱 필요한 버퍼만 찔끔 열어주는 짠돌이 최소 권한 매핑 시전 | 악성 I/O 장치가 시스템을 엎어버리는 끔찍한 제로데이 붕괴 사태를 완벽하게 틀어막음 |

#### 한줄 요약

- **Huge Pages 기반 IOTLB 미스 페널티 억제·DMA 언맵 시 IOTLB Invalidation 강제 플러시·최소 권한 기반 DMA 버퍼 매핑**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **CXL(Compute Express Link) 환경의 IOMMU 발전**: CXL.io 및 CXL.mem 프로토콜 상에서 장치와 호스트 간의 공유 가상 메모리(SVM: Shared Virtual Memory) 및 캐시 일관성 매핑으로 역할 확대.

</details>

- 클라우드 가상화 및 고보안 제로 트러스트 하드웨어 환경에서 **Intel VT-d/AMD-Vi 기본 활성화 및 SR-IOV/DPDK 고속 패스스루 표준 채택**

#### 한줄 요약

- **안전한 DMA 격리와 고성능 VM 디바이스 직결**을 위한 IOMMU 필수 구현
