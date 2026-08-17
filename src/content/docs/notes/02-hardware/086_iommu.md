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
  priority_note: "DMA 주소 변환(IOVA to HPA)과 하드웨어 메모리 격리의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 입출력 장치의 DMA 요청 시 I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 메모리 접근 권한을 제어하는 하드웨어 모듈(Intel VT-d, AMD-Vi, ARM SMMU).
- **IOVA(Input/Output Virtual Address)**: 디바이스 드라이버와 장치 DMA 컨트롤러가 사용하는 가상 I/O 메모리 주소 체계.

</details>

- 정의/개념: 주변장치(PCIe NIC/GPU)의 직접 메모리 접근(DMA) 시 **I/O 가상 주소(IOVA)를 물리 주소(HPA)로 변환**하고 메모리 접근을 격리하는 하드웨어 관리 장치
- 배경/필요성: 가상 머신(VM) 간 I/O 자원 간섭 및 비인가 주변장치의 **불법적 다이렉트 DMA 메모리 탈취 위협** 직면

#### 한줄 요약
- CPU에 MMU가 있듯이, 주변장치(랜카드/GPU)의 DMA 메모리 접근을 감시하고 가상 주소를 물리 주소로 안전하게 변환해 주는 장치다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: IOMMU 내부에서 최근 변환된 IOVA $\to$ HPA 주소 매핑 엔트리를 캐싱하여 페이지 테이블 탐색 오버헤드를 줄이는 고속 캐시.
- **도메인 격리(IOMMU Domain Isolation)**: 특정 VM 또는 프로세스마다 독립된 I/O 가상 주소 공간을 할당하여 타 영역 침범을 원천 차단하는 하드웨어 격리 기법.

</details>

- 장치 및 VM별 독립된 주소 공간을 부여하여 메모리 무단 침범을 방지하는 **도메인 격리(Domain Isolation)**
- 불연속적인 물리 페이지를 디바이스에 단일 연속 버퍼로 매핑하는 **Scatter-Gather 가상화**
- 가상 머신에 물리 NIC/GPU를 1:1 직결하는 **SR-IOV 및 디바이스 패스스루(Device Passthrough)** 지원

#### 한줄 요약
- 불연속 메모리를 연속된 버퍼처럼 엮어주고, 가상 머신이 물리 랜카드나 GPU에 직접 고속 접근할 수 있도록 보안 터널을 뚫어준다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **장치 컨텍스트 테이블(Device Context Table)**: PCIe 장치의 BDF(Bus:Device:Function) 번호를 인덱스로 하여 해당 장치가 속한 IOMMU 도메인의 페이지 테이블 루트 포인터를 찾는 테이블.
- **I/O 페이지 테이블(I/O Page Table)**: IOVA와 물리 메모리 주소(HPA) 간의 매핑 정보와 읽기/쓰기(R/W) 권한 플래그를 담은 다단계 테이블.

</details>

```text
┌─────────────────────────────────────────────────────────────┐
│ IOMMU 하드웨어 주소 변환 및 DMA 격리 아키텍처              │
│                                                             │
│  [ PCIe DMA 엔드포인트 장치 (100GbE NIC / GPU : BDF 식별자) ] │
│  └──────────────────────────┬───────────────────────────────┘│
│                             │ (DMA 메모리 읽기/쓰기 요청: IOVA)
│  ┌──────────────────────────▼───────────────────────────────┐│
│  │ IOMMU 하드웨어 엔진 (Intel VT-d / AMD-Vi / ARM SMMU)      ││
│  │  ├─ 장치 컨텍스트 테이블 (BDF ──► 도메인 페이지 테이블)   ││
│  │  ├─ IOTLB 초고속 캐시 (최근 변환 IOVA <──► HPA 캐싱)      ││
│  │  └─ I/O 페이지 테이블 워커 (Multi-Level Page Walk Engine) ││
│  └──────────────────────────┬───────────────────────────────┘│
│                             │ (권한 검증 완료된 물리 주소 HPA 전송)
│  ┌──────────────────────────▼───────────────────────────────┐│
│  │ 호스트 시스템 물리 메모리 (Host Physical Memory, DRAM)    ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

선의 의미: PCIe 장치가 BDF와 IOVA를 보내면 IOMMU가 IOTLB 및 페이지 테이블을 조회해 검증된 물리 주소 HPA로 DMA 수행

| 구성요소 | 책임 |
|:---|:---|
| PCIe 장치 (BDF) | 버스(Bus), 디바이스(Device), 함수(Function) 번호를 식별자로 달고 DMA 요청 전송 |
| 장치 컨텍스트 테이블 | 수신된 BDF를 기반으로 해당 장치가 속한 독립 IOMMU 도메인의 페이지 테이블 루트 탐색 |
| IOTLB 캐시 | 최근 변환된 IOVA $\to$ HPA 매핑 엔트리를 캐싱하여 메모리 접근 지연시간 극소화 |
| I/O 페이지 테이블 워커 | IOTLB 미스 발생 시 다단계 페이지 테이블을 직접 순회(Page Walk)하여 물리 주소 도출 |
| 권한 검증 및 Fault 로거 | 읽기/쓰기 권한 위반 및 미할당 주소 접근 시 DMA를 즉각 차단하고 IOMMU Fault 인터럽트 발생 |

#### 한줄 요약
- BDF 장치 식별자, 장치 컨텍스트 테이블, IOTLB 캐시, I/O 페이지 워커, 권한 검증기가 안전한 DMA 파이프라인을 구축한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOMMU Fault**: 매핑되지 않은 주소 접근, 쓰기 금지 영역 쓰기 시도, 권한 없는 BDF 요청 시 트랜잭션을 강제 차단하고 시스템 로그를 남기는 하드웨어 예외.

</details>

```text
PCIe 장치의 DMA 메모리 접근 요청 (<BDF, IOVA>)
      │
      ▼
1. IOTLB 캐시 조회: 최근 변환된 IOVA 매핑 엔트리가 존재하는지 확인
      ├── [Hit]  ──► 4. 권한 검증 단계로 즉시 직행
      └── [Miss] ──► 2. 다단계 I/O 페이지 테이블 워크(Page Walk) 수행
                             │
                             ▼
3. 주소 변환 엔트리 인출 및 IOTLB 캐시 적재
                             │
                             ▼
4. 접근 권한 검증: 요청된 읽기/쓰기 속성과 페이지 권한 비트 대조
      ├── [정상 인가] ──► 5-1. 호스트 물리 메모리로 최종 HPA DMA 전송 허용
      └── [권한 위반] ──► 5-2. 즉각 트랜잭션 드롭 및 IOMMU Fault 인터럽트 발생
```

**동작 원리**

1. **요청 인입**: PCIe 엔드포인트 장치가 BDF 식별자와 대상 IOVA 주소를 싣고 DMA 요청 송신
2. **고속 캐시 탐색**: IOMMU가 IOTLB를 조회하여 즉각적인 물리 주소 매핑 엔트리 유무 판별
3. **페이지 워크**: IOTLB Miss 시 컨텍스트 테이블을 거쳐 다단계 I/O 페이지 테이블을 순회해 HPA 도출
4. **보안 권한 체크**: 해당 메모리 블록의 Read/Write 권한 비트와 DMA 요청 유형의 일치 여부 검증
5. **결과 집행**: 인가된 요청은 DRAM으로 직접 전달하고, 비인가 접근은 즉시 차단 후 Fault 이벤트 통지

#### 한줄 요약
- DMA 요청 인입 → IOTLB 캐시 확인 → I/O 페이지 테이블 순회 → 읽기/쓰기 권한 검증 → DRAM DMA 실행/차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

| IOMMU 동작 모드 | IOMMU 활성화 (Strict Mode) | IOMMU 우회 (Bypass Mode) | 소프트웨어 바운스 버퍼 | 에뮬레이션 가상 I/O |
|:---|:---|:---|:---|:---|
| 적용 기준 | 가상화 클라우드 및 고보안 제로 트러스트 | 베어메탈 HPC 초저지연 연산 | 32비트 레거시 구형 하드웨어 | 단순 범용 하이퍼바이저 가상화 |
| 핵심 특징 | IOVA $\to$ HPA 변환 및 완벽한 DMA 하드웨어 격리 | 주소 변환 없이 물리 주소(HPA) 직결 통신 | 저위 4GB 메모리에 임시 복사 후 전송 | 하이퍼바이저 소프트웨어가 I/O 패킷 복사 |
| 한계 | IOTLB 미스 시 약간의 페이지 워크 지연(1~3%) | 악성 DMA 해킹(Thunderbolt 공격) 무방비 | CPU 복사 오버헤드로 인한 처리량 급감 | 극심한 VM-Exit 발생 및 CPU 자원 낭비 |

#### 한줄 요약
- 보안과 가상화는 IOMMU 활성화, 극단적 초저지연은 Bypass, 레거시는 바운스 버퍼, 단순 가상화는 에뮬레이션을 쓴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IOTLB Invalidation**: DMA 버퍼 해제(Unmap) 시 IOTLB 캐시에 남아 있는 잔여 주소 엔트리를 강제로 플러시하여 Use-After-Free DMA 보안 취약점을 막는 명령.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잦은 IOTLB 미스 발생으로 인한 **100GbE 네트워크 전송량 급감** | **대용량 페이지(Huge Pages: 2MB/1GB)** I/O 매핑 적용 | IOTLB 엔트리 수량 축소 및 주소 변환 지연 극소화 |
| DMA 버퍼 해제 후 잔여 캐시로 인한 **Use-After-Free 메모리 오염 위험** | DMA 언맵(Unmap) 즉시 **IOTLB Invalidation 강제 플러시** 수행 | 반납된 메모리에 대한 불법 DMA 접근 원천 차단 |
| 썬더볼트(Thunderbolt) 외장 포트를 통한 **다이렉트 DMA 메모리 탈취 해킹** | OS 커널의 **IOMMU DMA 보호 정책(Strict Isolation)** 의무 활성화 | 비인가 외장 장치의 커널 메모리 직접 덤프 100% 방어 |
| 디바이스 패스스루 시 **VM 간 인터럽트 간섭 및 서비스 거부(DoS)** | **인터럽트 리매핑(Interrupt Remapping)** 하드웨어 테이블 적용 | VM별 독립 가상 인터럽트 안전 라우팅 보장 |

#### 한줄 요약
- Huge Pages로 전송량을 끌어올리고, IOTLB Invalidation으로 오염을 막으며, Strict 격리로 외장 포트 해킹을 방어한다.

## Ⅶ. 결론

- 클라우드 엔터프라이즈 가상화 및 고성능 AI 데이터센터 구축 시 **IOMMU(Intel VT-d/AMD-Vi) 기반 DMA 격리 및 SR-IOV 직결** 필수

#### 한줄 요약
- 하드웨어 기반의 입출력 메모리 관리(IOMMU)를 통해 성능 손실 없는 가상 머신 장치 직결과 강력한 DMA 보안을 동시에 달성해야 한다.
