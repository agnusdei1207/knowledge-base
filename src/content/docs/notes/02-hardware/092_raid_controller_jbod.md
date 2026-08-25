---
sidebar:
  order: 92
  label: "092. RAID 컨트롤러•JBOD"
  badge:
    text: "미출 · 50%"
    variant: note
title: "RAID 컨트롤러•JBOD (RAID Controller and JBOD)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 92
extra:
  question_no: "092"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "보호•복구 책임 계층에 따른 경로 선택"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하드웨어 RAID 컨트롤러(HW RAID)**: 전용 XOR/RS 연산 ASIC 및 캐시 메모리를 탑재하여 패리티 연산과 볼륨을 하드웨어로 처리하는 스토리지 카드.
- **JBOD(Just a Bunch of Disks)**: 물리 드라이브들을 묶지 않고 각각 독립된 개별 블록 디바이스로 OS/SDS 계층에 1:1 노출하는 구조.

</details>

- 정의/개념: 전용 ASIC 및 캐시 기반 볼륨을 제공하는 **HW RAID**와 원시 디스크를 1:1 직결 노출하는 **JBOD**
- 배경/필요성: 단일 서버 하드웨어 신뢰성(RAID)과 클라우드 분산 스케일아웃(JBOD) 간 **스토리지 계층별 책임 분리 및 복구 최적화 필수**

#### 한줄 요약
- 단일 서버의 하드웨어 캐시 가속(RAID)과 클라우드 분산 소프트웨어 정의 스토리지(JBOD)로 역할이 구분된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **FBWC(Flash-Backed Write Cache)**: 정전 시 슈퍼캐패시터 전력으로 DRAM 캐시 데이터를 플래시 메모리에 즉시 백업하는 전력 장애 보호 장치.
- **IT 모드(Initiator Target Mode)**: RAID 카드의 가상 볼륨 관리 기능을 끄고 물리 드라이브를 OS에 직접 1:1로 패스스루하는 HBA 동작 모드.

</details>

- HW RAID: **FBWC** 배터리 보호 Write-Back 캐시를 통한 고속 쓰기 응답 및 전력 장애 완벽 방어
- JBOD: HBA 직결 **IT 모드**를 통해 디스크 텔레메트리(S.M.A.R.T)를 상위 SDS(Ceph, ZFS)에 직접 노출
- 복구 책임: HW RAID는 컨트롤러 ASIC이 패리티 재구축(Rebuild)을 전담, JBOD는 분산 네트워크가 복제 수행

#### 한줄 요약
- HW RAID는 전용 하드웨어로 데이터 신뢰성을 보장하며, JBOD는 소프트웨어에 원시 디스크 제어권을 위임한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **패리티 연산 엔진(Parity Engine)**: RAID 5/6의 XOR 및 Reed-Solomon 갈루아 필드($GF(2^8)$) 패리티 연산을 가속하는 하드웨어 ASIC.

</details>

```text
[HW RAID vs JBOD/SDS 스토리지 구조]
|-- HW RAID 아키텍처 (하드웨어 책임 모델)
|   |-- 호스트 OS (단일 Logical Virtual LUN 인식)
|   |-- RAID 컨트롤러 카드 (HW ASIC 패리티 가속 엔진)
|   |-- FBWC DRAM 캐시 및 슈퍼캐패시터 BBU
|   `-- 물리 드라이브 어레이 (RAID 5/6/10 볼륨 바인딩)
`-- JBOD / SDS 아키텍처 (소프트웨어 책임 모델)
    |-- 호스트 OS 및 분산 SDS 엔진 (Ceph, ZFS, MinIO)
    |-- HBA 컨트롤러 카드 (IT 모드 직결 패스스루)
    `-- 개별 원시 물리 디스크 (Disk 1, Disk 2, Disk N 1:1 직결)
```

선의 의미: 계층 및 하드웨어/소프트웨어 제어 구조

| 구성요소 | HW RAID 컨트롤러 책임 | JBOD / SDS 책임 |
|:---|:---|:---|
| I/O 처리 방식 | **FBWC 캐시** Write-Back 가속 및 가상 LUN 노출 | HBA 패스스루로 원시 디스크 1:1 직접 I/O 전달 |
| 패리티 연산 | **전용 하드웨어 ASIC**이 XOR/RS 연산 전담 | 호스트 CPU가 ZFS/Ceph 분산 Erasure Coding 연산 |
| 장애 복구 | 드라이브 교체 시 로컬 컨트롤러가 리빌드 수행 | 분산 네트워크를 통해 타 정상 노드에서 데이터 복제 |
| 모니터링 | 컨트롤러 펌웨어가 드라이버 가상화 상태 보고 | 상위 SDS가 디스크 **S.M.A.R.T** 텔레메트리 직접 감시 |

#### 한줄 요약
- HW RAID는 컨트롤러 카드가 모든 책임을 지며, JBOD는 단순 HBA를 통해 소프트웨어에 자원을 직결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Back vs Write-Through**: FBWC 캐시에 쓰고 즉시 성공을 반환하는 방식(Write-Back)과 디스크 미디어 기록까지 대기하는 동기식 방식(Write-Through).

</details>

```text
스토리지 아키텍처 선정 (단일 서버 HW RAID vs 분산 SDS JBOD)
        │
   스토리지 쓰기 요청 인입
   ┌────┴─────┐
[HW RAID 경로]   [JBOD / SDS 경로]
   │             │
FBWC 캐시에      HBA가 원시 디스크로 직접 패스스루 전달
Write-Back 기록   │
   │             상위 SDS(Ceph/ZFS)가 네트워크 다중 노드로
하드웨어 ASIC이   병렬 복제(3-Way) 또는 Erasure Coding 분산 기록
패리티 분할 계산 후 │
물리 디스크 스트라이프│
비동기 기록       │
   │             │
   └────┬────────┘
        │
   쓰기 완료 응답 반환 및 트랜잭션 종결
```

#### 한줄 요약
- 아키텍처 분기 → RAID 캐시 Write-Back 또는 JBOD 패스스루 SDS 복제 → 쓰기 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **JBOF(Just a Bunch of Flash)**: 수십 개의 NVMe SSD를 고밀도 섀시에 장착하여 PCIe/RoCEv2 패브릭으로 공유하는 올플래시 스토리지.

</details>

| 구분 | 하드웨어 RAID 컨트롤러 (HW RAID) | JBOD / HBA 패스스루 (JBOD / SDS) | 올플래시 JBOF (NVMe-oF) |
|:---|:---|:---|:---|
| 데이터 보호 주체 | 전용 하드웨어 RAID ASIC/펌웨어 | 상위 OS 파일시스템(ZFS) 및 SDS | 분산 SDS 및 RDMA 스토리지 클러스터 |
| 캐싱 및 쓰기 가속 | **FBWC BBU** 캐시 Write-Back 가속 | 호스트 NVMe 저널/캐시 티어링 | 엔드포인트 NVMe DRAM 캐시 직결 |
| 장단점 및 한계 | 컨트롤러 고장 시 단일 장애점(SPOF) | 단일 노드 캐시 부재, 높은 CPU 사용 | 초저지연·초고속, 무손실 RoCE 망 필수 |
| 주요 응용처 | 단일 고성능 RDBMS, 전통 엔터프라이즈 | Ceph, vSAN, 하둡, 오브젝트 스토리지 | AI 슈퍼클러스터, 실시간 빅데이터 분석 |

#### 한줄 요약
- 단일 서버 RDBMS는 HW RAID가, 대규모 클라우드 스토리지에는 JBOD(SDS)와 JBOF가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVMe 캐시 티어링(NVMe Cache Tiering)**: JBOD 구성 시 쓰기 성능 저하를 극복하기 위해 고성능 NVMe SSD를 쓰기 버퍼/저널 계층으로 전면 배치하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| JBOD 구성 시 소프트웨어 동기식 복제 쓰기 지연 | 고성능 **NVMe SSD 저널/캐시 티어링 계층** 전면 배치 | 원시 디스크 쓰기 지연 80% 완화 및 처리량 극대화 |
| 단일 HW RAID 컨트롤러 고장 시 전체 LUN 마비 | **액티브-액티브 듀얼 RAID 컨트롤러** 이중화 구성 | 컨트롤러 단일 장애점(SPOF) 원천 배제 및 무중단 가용성 확보 |
| ZFS/Ceph SDS 환경에서 HW RAID 구성 시 충돌 | RAID 카드를 **HBA IT 모드(패스스루)** 로 펌웨어 플래싱 | 물리 디스크 상태 직접 감시 및 SDS 자가 치유 정상 동작 |
| 대용량 HDD(16TB+) RAID 5 리빌드 중 2차 고장 | RAID 6(이중 패리티) 또는 SDS 이레이저 코딩(8+3) 전환 | 리빌드 중 추가 디스크 손상 시 데이터 유실 방지 |

#### 한줄 요약
- NVMe 캐시 티어링, 듀얼 컨트롤러 HA, IT 모드 펌웨어 플래싱, 이중 패리티 적용으로 스토리지 무결성을 보장한다.

## Ⅶ. 결론

- 단일 고성능 데이터베이스 서버는 **HW RAID 6/10 컨트롤러**를 구축하고, 대규모 클라우드 분산 환경은 **HBA IT 모드 JBOD/JBOF 기반 SDS**를 표준 채택

#### 한줄 요약
- 스토리지 아키텍처는 단일 노드 하드웨어 캐싱 가속과 분산 소프트웨어 확장성 간의 요구사항에 맞춰 최적으로 선택해야 한다.