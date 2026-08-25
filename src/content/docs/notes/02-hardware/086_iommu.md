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

- **IOMMU(Input-Output Memory Management Unit)**: PCI/PCIe 입출력 장치가 직접 메모리 접근(DMA)을 수행할 때, I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 메모리 읽기/쓰기 권한을 하드웨어로 통제하는 I/O 가상화 보안 유닛(Intel VT-d, AMD-Vi, ARM SMMU).
- **I/O 가상 주소(IOVA, Input/Output Virtual Address)**: 디바이스 드라이버와 장치 DMA 컨트롤러가 메모리 버퍼를 식별하기 위해 사용하는 가상 주소 공간.

</details>

- 정의/개념: 입출력 디바이스의 DMA 요청 시 **I/O 가상 주소(IOVA)를 호스트 물리 주소(HPA)로 변환하고 장치별 메모리 접근 권한을 하드웨어로 격리**하는 **IOMMU(Input-Output Memory Management Unit) 아키텍처**
- 배경/필요성: 기존 직접 물리 DMA 구조는 CPU의 MMU 메모리 보호를 우회하므로 **악성 장치의 물리 메모리 무단 덤프(DMA 공격) 및 가상화 환경에서 VM 간 메모리 침범 차단 불가**

#### 한줄 요약
- IOMMU는 I/O 디바이스의 DMA 접근을 가상 주소로 변환하고 하드웨어 격리를 수행하여 시스템 안정성과 가상화 패스스루를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IOTLB(Input/Output Translation Lookaside Buffer)**: IOMMU 내부에서 최근 변환된 IOVA $\to$ HPA 주소 매핑 엔트리를 캐싱하여 다단계 페이지 테이블 순회 지연을 줄이는 고속 캐시.
- **도메인 격리(IOMMU Domain Isolation)**: 장치 식별자(BDF)별로 독립된 I/O 페이지 테이블과 권한을 적용하여 특정 장치가 허가된 메모리 영역 외에는 절대 접근하지 못하도록 통제하는 기법.

</details>

- 하드웨어 메모리 보호: 장치(BDF)별 독립 **도메인 격리**를 통해 비인가 물리 메모리 접근 시 IOMMU Fault를 발생시켜 트랜잭션 즉각 차단
- Scatter-Gather 주소 연속화: 물리적으로 파편화된 불연속 메모리 페이지들을 디바이스 관점에서 **단일 연속 I/O 가상 주소(IOVA) 공간으로 매핑**
- 초고속 가상화 패스스루: **IOTLB** 캐싱 및 **인터럽트 리매핑(Interrupt Remapping)**을 통해 PCIe NIC/GPU를 게스트 VM에 직접 1:1 직결(Direct Assignment)

#### 한줄 요약
- 도메인 격리로 악성 DMA를 차단하고 Scatter-Gather 주소 연속화로 I/O 성능을 최적화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **장치 컨텍스트 테이블(Device Context Table)**: PCIe 장치의 BDF(Bus:Device:Function) 번호를 인덱스로 하여 해당 장치가 속한 가상화 도메인의 I/O 페이지 테이블 루트 포인터를 찾는 하드웨어 테이블.
- **I/O 페이지 테이블(I/O Page Table)**: IOVA와 물리 메모리 주소(HPA) 간의 매핑 정보와 읽기/쓰기(R/W) 권한 플래그를 담은 다단계 페이지 테이블.

</details>

```text
[IOMMU 하드웨어 주소 변환 및 격리 아키텍처]
 ┌─ [PCIe 엔드포인트 장치단] ──────────── [BDF 식별자] + IOVA 기반 DMA 읽기/쓰기 요청 발행
 │                                                    │ (PCIe TLP 패킷)
 ├─ [IOMMU 하드웨어 엔진 (Intel VT-d / AMD-Vi / ARM SMMU)]
 │   ├─ [장치 컨텍스트 테이블] ────────── BDF 번호 ➔ 도메인 I/O 페이지 테이블 루트 검색
 │   ├─ [IOTLB 캐시 유닛] ────────────── 최근 변환된 IOVA ➔ HPA 매핑 엔트리 고속 캐싱
 │   ├─ [다단계 I/O 페이지 워커] ──────── 4단계 I/O 페이징 순회 및 R/W 메모리 권한 검증
 │   └─ [인터럽트 리매핑 유닛] ────────── 디바이스 MSI/MSI-X 인터럽트를 대상 vCPU로 안전 라우팅
 │                                                    │
 └─ [호스트 시스템 물리 메모리 (HPA)] ─── 인가된 물리 메모리 블록에만 DMA 전송 허용
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 주소 변환 트랜잭션 흐름; IOMMU가 BDF를 확인해 I/O 페이지 테이블을 순회한 후 인가된 HPA 메모리로만 DMA를 통과시킴

| 구성요소 | 계층 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| **PCIe 장치 (BDF)** | I/O 버스단 | 버스·디바이스·기능 번호를 패킷에 싣고 IOVA 가상 주소로 DMA 트랜잭션 요청 | 엔드포인트 장치 |
| **장치 컨텍스트 테이블**| IOMMU 제어단 | BDF 식별자를 기반으로 소속 도메인의 **I/O 페이지 테이블 루트 포인터 획득** | 도메인 매핑 |
| **IOTLB 캐시 유닛** | IOMMU 내부 | 최근 변환된 IOVA $\to$ HPA 엔트리를 캐싱하여 **페이지 테이블 순회 지연 단축** | 고속 주소 캐시 |
| **I/O 페이지 워커** | 주소 변환단 | IOTLB 미스 시 4단계 I/O 페이지 테이블을 탐색하여 HPA 산출 및 권한 검증 | 하드웨어 워커 |
| **인터럽트 리매핑기** | 인터럽트단 | 디바이스 MSI/MSI-X 신호를 대상 게스트 vCPU로 안전하게 변환 격리 라우팅 | 인터럽트 위변조 차단 |

#### 한줄 요약
- IOMMU는 BDF 컨텍스트 테이블, IOTLB 캐시, I/O 페이지 테이블 워커 및 인터럽트 리매핑 유닛으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IOMMU Fault**: 매핑되지 않은 주소 접근, 쓰기 금지 영역 쓰기 시도, 비인가 BDF 요청 발생 시 트랜잭션을 강제 드롭하고 하드웨어 인터럽트 로그를 남기는 보호 동작.

</details>

```text
1. PCIe 장치: BDF 번호 및 IOVA 가상 주소를 포함한 DMA 읽기/쓰기 TLP 송출
                      │
                      ▼
2. IOMMU 하드웨어: BDF 번호로 장치 컨텍스트 테이블 조회 ➔ 도메인 식별
                      │
                      ▼
3. 해당 IOVA $\to$ HPA 변환 엔트리가 IOTLB 캐시에 존재하는가?
   ┌──────────────────┴──────────────────┐
[ IOTLB 적중 (Hit) ]                  [ IOTLB 미스 (Miss) ]
   │                                     │
   ▼                                     ▼
4. 캐시된 HPA 주소 즉시 획득            4. 다단계 I/O 페이지 테이블 하드웨어 워크 수행
   │                                     │
   └──────────────────┬──────────────────┘
                      │
                      ▼
5. 요청된 DMA 동작(Read/Write)이 I/O 페이지 테이블 권한과 일치하는가?
   ┌──────────────────┴──────────────────┐
[ 권한 일치 (정상 접근) ]              [ 권한 불일치 / 미매핑 (위반) ]
   │                                     │
   ▼                                     ▼
6. 호스트 물리 메모리(HPA)로           6. IOMMU Fault 하드웨어 예외 발생
   DMA 데이터 전송 최종 완료             ➔ DMA 트랜잭션 즉각 차단 및 커널 로그 기록
```

분기 결과: **권한이 일치하면** 고속 DMA가 허용되며, **비인가 접근은** IOMMU Fault로 즉시 차단되어 시스템 메모리를 완벽히 보호함

#### 한줄 요약
- DMA 인입 ➔ BDF 컨텍스트 조회 ➔ IOTLB/페이지 워크 ➔ 권한 검증 후 HPA 전송 또는 IOMMU Fault 차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Strict Mode**: 모든 DMA 요청마다 즉시 I/O 페이지 테이블 매핑 및 IOTLB 무효화를 수행하는 최고 보안 모드.
- **Bypass Mode / Passthrough**: IOMMU 주소 변환을 끄고 물리 주소를 직접 사용하여 초저지연을 얻는 베어메탈 모드.

</details>

| IOMMU 동작 모드 | Strict Mode (엄격 격리) | Lazy / Deferred Mode | Bypass Mode (우회 직결) |
|:---|:---|:---|:---|
| 주소 변환 및 권한 검사| **모든 DMA 트랜잭션 100% 검증** | 지연 IOTLB 플러시로 성능 개선 | **주소 변환 없음 (물리 주소 직접 사용)**|
| 보안 격리성 수준 | **최고 (Zero-Trust 하드웨어 격리)**| 높음 (짧은 취약 시간 창 존재) | **취약 (악성 DMA 공격에 완전 노출)** |
| DMA I/O 지연시간 | 변환 및 무효화 오버헤드 발생 | 오버헤드 대폭 축소 | **0 (네이티브 베어메탈 속도)** |
| 주요 적용 분야 | **멀티테넌트 클라우드, 금융 서버** | 고속 네트워크 NIC, 대규모 스토리지 | HPC 슈퍼컴퓨터 초저지연 노드 |

#### 한줄 요약
- 가상화 및 클라우드 보안 환경에는 Strict 모드가 필수적이며, 극단적인 HPC 환경에서는 제한적으로 Bypass 모드가 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IOTLB Invalidation**: DMA 버퍼 해제(Unmap) 시 IOTLB 캐시에 남아 있는 잔여 주소 엔트리를 강제로 플러시하여 Use-After-Free DMA 보안 취약점을 차단하는 명령.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잦은 IOTLB 미스로 인한 고속 100GbE NIC/GPU 처리율 저하 | **IOMMU 대용량 페이지(Huge Pages 2MB) 및 도메인 배치 적용** | IOTLB 적중률 99% 달성 및 DMA 지연 최소화 |
| DMA 버퍼 해제 후 잔여 캐시로 인한 무단 메모리 접근 | **버퍼 Unmap 시 즉각적인 IOTLB Invalidation 명령 강제 수행** | DMA Use-After-Free 및 메모리 정보 유출 원천 차단 |
| 썬더볼트/외부 PCIe 포트를 통한 외부 물리 악성 DMA 공격 | **부팅 전 IOMMU 활성화(Kernel DMA Protection) 정책 강제** | 비인가 외장 디바이스의 물리 메모리 덤프 차단 |

#### 한줄 요약
- 실무에서는 Huge Pages로 IOTLB를 가속하고, 즉각 Invalidation으로 보안을 지키며, Kernel DMA Protection으로 외부 공격을 막는다.

## Ⅶ. 결론

- 클라우드 멀티테넌트 가상화 및 AI 가속기 인프라의 메모리 보안을 위해 **IOMMU(VT-d/SMMU) 기반의 하드웨어 DMA 주소 변환 및 도메인 격리를 표준 구축**하고, PCIe 패스스루 가속을 위해 **인터럽트 리매핑 및 IOMMU Huge Pages**를 연계하며, 외부 물리 해킹을 차단하기 위해 **Kernel DMA Protection 정책**을 필수 구현하는 고신뢰 I/O 서브시스템 아키텍처 확립

#### 한줄 요약
- IOMMU는 CPU의 MMU와 대등하게 I/O 서브시스템의 가상화와 메모리 보안을 책임지는 핵심 하드웨어 아키텍처다.