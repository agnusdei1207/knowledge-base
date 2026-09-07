---
sidebar:
  order: 86
  label: "086. IOMMU (Input-Output Memory Management Unit)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "IOMMU (Input-Output Memory Management Unit)"
date: "2026-09-07T09:45:00+09:00"
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

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 입출력 장치가 직접 메모리 접근(DMA)을 수행할 때, I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 메모리 읽기/쓰기 권한을 하드웨어로 통제하는 I/O 가상화 보안 유닛(Intel VT-d, AMD-Vi, ARM SMMU).
- **I/O 가상 주소(IOVA, Input/Output Virtual Address)**: 디바이스 드라이버와 장치 DMA 컨트롤러가 메모리 버퍼를 식별하기 위해 사용하는 가상 주소 공간.

</details>

- 정의/개념: 입출력 장치 DMA 요청 시 **IOVA**를 호스트 물리 주소(HPA)로 고속 변환하고 디바이스별 메모리 접근 권한을 하드웨어로 강제 격리하는 **입출력 메모리 관리 아키텍처**
- 배경/필요성: 고속 PCIe 주변장치가 CPU MMU를 거치지 않고 물리 메모리에 직접 접근(DMA)함에 따라 발생하는 메모리 덮어쓰기 파손 위험 및 악성 DMA 기반 호스트 메모리 탈취 취약점 한계 극복

#### 한줄 요약
- IOMMU는 I/O 디바이스의 DMA 접근을 가상 주소로 변환하고 하드웨어 격리를 수행하여 시스템 안정성과 가상화 패스스루를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: IOMMU 내부에서 최근 변환된 IOVA $\to$ HPA 주소 매핑 엔트리를 캐싱하여 다단계 페이지 테이블 순회 지연을 줄이는 고속 캐시.
- **도메인 격리(IOMMU Domain Isolation)**: 장치 식별자(BDF)별로 독립된 I/O 페이지 테이블과 권한을 적용하여 특정 장치가 허가된 메모리 영역 외에는 절대 접근하지 못하도록 통제하는 기법.
- **IOMMU Fault**: 매핑되지 않은 주소 접근, 쓰기 금지 영역 쓰기 시도, 비인가 BDF 요청 발생 시 트랜잭션을 강제 드롭하고 하드웨어 인터럽트 로그를 남기는 보호 동작.

</details>

- 하드웨어 메모리 보호: PCIe BDF 단위의 독립된 **도메인 격리**를 적용하여 인가되지 않은 메모리 영역 접근 발생 시 하드웨어 **IOMMU Fault** 인터럽트를 발생시키고 트랜잭션을 즉각 차단
- Scatter-Gather 주소 연속화: 물리 메모리 공간상에 파편화된 비연속 페이지들을 장치 관점의 단일 연속 **IOVA** 가상 주소 공간으로 통합 매핑하여 버퍼 복사 오버헤드 해소
- 가상화 패스스루 가속: **IOTLB** 하드웨어 캐싱과 MSI 인터럽트 리매핑을 지원하여 게스트 VM에 물리 PCIe 디바이스를 1:1 직결 할당

#### 한줄 요약
- 도메인 격리로 악성 DMA를 차단하고 Scatter-Gather 주소 연속화로 I/O 성능을 최적화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **장치 컨텍스트 테이블(Device Context Table)**: PCIe 장치의 BDF(Bus:Device:Function) 번호를 인덱스로 하여 해당 장치가 속한 가상화 도메인의 I/O 페이지 테이블 루트 포인터를 찾는 하드웨어 테이블.
- **I/O 페이지 테이블(I/O Page Table)**: IOVA와 물리 메모리 주소(HPA) 간의 매핑 정보와 읽기/쓰기(R/W) 권한 플래그를 담은 다단계 페이지 테이블.

</details>

```text
[IOMMU 서브시스템 아키텍처]
  │
  ├─ [PCIe 엔드포인트 장치]
  │     └─ [DMA 엔진] (IOVA 기반 트랜잭션 및 BDF 인가)
  │
  ├─ [IOMMU 하드웨어 계층] (VT-d/AMD-Vi/SMMU)
  │     ├─ [장치 컨텍스트 테이블] (BDF별 도메인 포인터)
  │     ├─ [IOTLB 고속 캐시] (IOVA->HPA 변환 캐싱)
  │     ├─ [I/O 페이지 워커] (다단계 주소 변환 및 권한 검증)
  │     └─ [인터럽트 리매핑기] (MSI/MSI-X to vCPU 라우팅)
  │
  └─ [호스트 물리 메모리 (DRAM)]
        └─ [대상 DMA 버퍼] (검증 완료된 HPA 접근 허가)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| PCIe 엔드포인트 장치 | BDF 식별자를 포함하여 **IOVA** 기반의 고속 DMA 읽기/쓰기 요청 발행 |
| 장치 컨텍스트 테이블 | BDF 식별자 기반 소속 도메인의 **I/O 페이지 테이블** 루트 포인터 탐색 |
| IOTLB 캐시 유닛 | 최근 변환된 **IOVA** to HPA 엔트리를 캐싱하여 페이지 순회 지연 단축 |
| I/O 페이지 워커 | 캐시 미스 시 다단계 I/O 페이지 테이블을 탐색하여 HPA 산출 및 접근 권한 검증 |
| 인터럽트 리매핑기 | 디바이스 MSI/MSI-X 인터럽트를 대상 게스트 vCPU로 안전하게 변환 격리 |

#### 한줄 요약
- 장치 컨텍스트 테이블이 BDF 번호를 열쇠로 장치마다 다른 페이지 테이블을 물려 호스트 물리 주소를 직접 들고 다니던 DMA를 도메인 안에 가두고, 인터럽트 리매핑기가 같은 원리를 인터럽트 경로에도 얹어 장치가 임의 vCPU를 겨냥하지 못하게 한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOVA(Input/Output Virtual Address)**: 디바이스 드라이버 및 DMA 엔진이 호스트 물리 주소를 직접 참조하지 않고 가상화된 버퍼를 식별하기 위해 사용하는 I/O 가상 주소.
- **IOMMU Fault**: 미매핑 메모리 접근, 쓰기 금지 영역 변조, 비인가 BDF 트랜잭션 등 위반 발생 시 즉각 패킷을 드롭하고 CPU 인터럽트를 발생하는 하드웨어 보호 메커니즘.

</details>

```text
[디바이스 DMA 트랜잭션 인입 (BDF + IOVA)]
           │
           ▼
[1. BDF 인덱스 기반 장치 컨텍스트 테이블 검색]
           │
           ▼
[2. IOTLB 캐시 적중 여부 판정]
           │
     ┌─────┴─────┐
     │           │
[IOTLB 적중]   [IOTLB 미스]
     │           │
     │           ▼
     │    [3. 다단계 I/O 페이지 테이블 순회(Walk) 및 HPA 획득]
     │           │
     └─────────> ┼
                 │
                 ▼
     <메모리 접근 권한 및 도메인 유효성 판정>
                 │
           ┌─────┴─────┐
           │           │
       [정상 인가]   [비인가 / 유효성 위반]
           │           │
           │           ▼
           │    [4. 트랜잭션 즉각 차단 및 IOMMU Fault 인터럽트 발생]
           │           │
           ▼           ▼
[5. HPA 대상 DMA 완료]  [오류 로깅 및 시스템 보호]
```

분기 결과: 장치 권한 검증이 통과되면 호스트 물리 메모리로 고속 DMA 전송이 인가되며, 비인가 주소 접근이나 권한 위반 시에는 하드웨어 트랜잭션이 즉각 차단되고 IOMMU Fault가 로깅됨

**동작 원리**:
1. PCIe 장치의 BDF 식별자 및 IOVA 가상 주소 포함 DMA 읽기/쓰기 요청 패킷 IOMMU 송신.
2. 수신 BDF 번호 기반 장치 컨텍스트 테이블 조회 및 소속 도메인 I/O 페이지 테이블 베이스 주소 식별.
3. IOTLB 캐시 조회를 통한 HPA 즉시 반환 또는 캐시 미스 시 다단계 I/O 페이지 테이블 순회 기반 물리 주소 산출.
4. I/O 페이지 테이블 엔트리 R/W 권한 및 유효성 검증 실패 시 트랜잭션 강제 드롭 및 CPU 대상 IOMMU Fault 인터럽트 송신.
5. 인가 완료 HPA 물리 주소의 메모리 컨트롤러 전달 기반 호스트 메모리 버퍼-PCIe 장치 간 직접 고속 DMA 데이터 전송 완료.

#### 한줄 요약
- IOTLB는 DMA마다 반복되던 다단계 I/O 페이지 테이블 순회를 사본으로 대신하며, 그 주소 변환 경로가 곧 권한 검사 경로여서 격리를 위한 별도 계층을 더 두지 않아도 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Strict Mode**: 모든 DMA 요청마다 즉시 I/O 페이지 테이블 매핑 및 IOTLB 무효화를 수행하는 최고 보안 모드.
- **Bypass Mode / Passthrough**: IOMMU 주소 변환을 끄고 물리 주소를 직접 사용하여 초저지연을 얻는 베어메탈 모드.

</details>

| 대상 구분 | Strict Mode (엄격 격리) | Lazy / Deferred Mode (지연 무효화) | Bypass Mode (우회 직결) |
|:---|:---|:---|:---|
| 적용 기준 | 멀티테넌트 가상화 클라우드 및 제로 트러스트 보안 환경 시 | 초고속 100GbE 이상 고성능 네트워크 및 스토리지 가속 환경 시 | 단일 전용 HPC 노드 및 실시간 초저지연 연산 극대화 시 |
| 핵심 특징 | 모든 DMA 트랜잭션 100% 실시간 검증, Zero-Trust 하드웨어 격리, 주소 변환 오버헤드 감내 | 지연 IOTLB 플러시 기반 일괄 검증, 일시적 취약 창 존재, 지연시간 대폭 단축 | 주소 변환 생략(물리 주소 직접 사용), 악성 DMA 공격 노출, 베어메탈 수준 초저지연(0) |
| 한계 | 빈번한 IOTLB 플러시로 인한 CPU 사이클 증가 | 버퍼 해제 후 플러시 전까지 잠재적 취약 창 잔존 | 하드웨어 메모리 보호 부재로 보안 격리 불가 |

#### 한줄 요약
- 가상화 및 클라우드 보안 환경에는 Strict 모드가 필수적이며, 극단적인 HPC 환경에서는 제한적으로 Bypass 모드가 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Kernel DMA Protection**: 운영체제 부팅 전후 썬더볼트(Thunderbolt) 및 외장 PCIe 포트를 통한 승인되지 않은 주변장치의 DMA 메모리 접근을 원천 차단하는 OS-BIOS 연계 보안 기능.
- **IOTLB Invalidation**: DMA 버퍼 해제(Unmap) 시 IOTLB 캐시에 남아 있는 잔여 주소 엔트리를 강제로 플러시하여 Use-After-Free DMA 보안 취약점을 차단하는 명령.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잦은 IOTLB 미스로 인한 초고속 I/O 처리율 저하 | **IOMMU 대용량 페이지(Huge Pages, 2MB/1GB)** 적용 | IOTLB 적중률 향상 및 주소 변환 지연 최소화 |
| DMA 버퍼 해제 후 잔여 캐시로 인한 Use-After-Free 메모리 변조 | 버퍼 Unmap 시 즉각적인 **IOTLB Invalidation** 강제 | Use-After-Free DMA 보안 취약점 원천 차단 |
| 썬더볼트 등 외장 포트를 통한 하드웨어 악성 DMA 인젝션 공격 | BIOS 및 OS 수준의 **Kernel DMA Protection** 정책 강제 | 비인가 외장 디바이스의 물리 메모리 덤프 차단 |

#### 한줄 요약
- 실무에서는 Huge Pages로 IOTLB를 가속하고, 즉각 Invalidation으로 보안을 지키며, Kernel DMA Protection으로 외부 공격을 막는다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **시스템 메모리 관리 장치(System Memory Management Unit, Arm SMMU)**: Arm 아키텍처 환경에서 온칩 가속기 및 PCIe 디바이스의 DMA 주소 변환과 2단계 가상화 격리를 전담하는 하드웨어 유닛.
- **단일 루트 입출력 가상화(Single Root I/O Virtualization, SR-IOV)**: 단일 물리 PCIe 어댑터를 여러 가상 기능(VF)으로 분할하여 IOMMU를 통해 VM에 직결하는 가상화 표준.

</details>

- PCIe 장치 식별자(BDF) 기반 도메인 격리와 IOTLB 캐시 가속을 바탕으로 I/O 패스스루 및 제로 트러스트 보안 표준으로 안착되었으며, CXL 메모리 풀링 및 DPU/IPU 가속 환경의 복합 이종 메모리 격리 장치로의 진화 추세.
- 워크로드 보안 등급에 따른 엄격 모드와 지연 무효화 모드의 선별적 적용과 함께, 대용량 페이지 기반 IOTLB 적중률 튜닝을 병행하는 정밀한 공학적 절충 필요.

#### 한줄 요약
- PCIe 도메인 격리와 IOTLB 캐싱으로 악성 DMA를 차단하고 워크로드별 모드 선별 및 대용량 페이지 튜닝으로 보안과 I/O 처리율을 동시 달성해야 한다.
