---
sidebar:
  order: 92
  label: "092. RAID 컨트롤러•JBOD"
  badge:
    text: "미출 · 50%"
    variant: note
title: "RAID 컨트롤러•JBOD (RAID Controller and JBOD)"
date: "2026-08-26T16:23:00+09:00"
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

- **하드웨어 RAID 컨트롤러(Hardware RAID Controller)**: 전용 XOR/Reed-Solomon 패리티 연산 ASIC 및 배터리 백업 캐시 메모리를 탑재하여 디스크 결함 복구와 볼륨 바인딩을 하드웨어로 자체 처리하는 전용 스토리지 카드.
- **JBOD(Just a Bunch of Disks)**: 물리 드라이브들을 RAID 컨트롤러로 묶지 않고, 각각 독립된 개별 원시(Raw) 블록 디바이스로 OS 및 소프트웨어 정의 스토리지(SDS) 계층에 1:1 직결 노출하는 구조.

</details>

- 정의/개념: 전용 ASIC으로 볼륨을 가상화하는 **HW RAID**와 원시 디스크를 직접 노출하는 **JBOD** 아키텍처
- 배경/필요성: 데이터 보호를 어느 계층이 맡을지 정하지 않으면 컨트롤러와 분산 소프트웨어가 패리티를 중복 계산해 쓰기 비용만 이중으로 치르므로, 캐시·패리티를 전용 ASIC에 맡길지 원시 디스크를 그대로 노출해 상위 소프트웨어에 위임할지로 **스토리지 계층별 책임 모델**을 가를 필요

#### 한줄 요약
- 단일 서버의 하드웨어 캐시 가속(HW RAID)과 클라우드 분산 소프트웨어 정의 스토리지(JBOD)로 역할이 구분된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **플래시 백업 쓰기 캐시(Flash-Backed Write Cache, FBWC)**: 시스템 정전 시 슈퍼커패시터 전력으로 DRAM 캐시 데이터를 비휘발성 NAND 플래시 메모리에 즉시 백업하는 전력 장애 보호 장치.
- **IT 모드(Initiator Target Mode)**: RAID 카드의 하드웨어 볼륨 관리 및 캐싱 기능을 끄고 단순 HBA로 동작시켜 물리 드라이브를 OS에 직접 1:1 투명 패스스루하는 펌웨어 동작 모드.

</details>

- HW RAID의 강점: **FBWC** 캐시 Write-Back 가속을 통한 극초저지연 응답 및 전력 장애 보호
- JBOD의 강점: HBA **IT 모드**를 통해 디스크 **S.M.A.R.T 텔레메트리**를 분산 SDS에 직접 노출
- 복구 책임의 차이: HW RAID는 컨트롤러의 로컬 리빌드, JBOD는 **분산 SDS**의 네트워크 병렬 복제 수행

#### 한줄 요약
- HW RAID는 전용 하드웨어로 데이터 신뢰성을 보장하며, JBOD는 소프트웨어에 원시 디스크 제어권을 위임한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **패리티 연산 엔진(Parity Engine ASIC)**: RAID 5/6의 XOR 및 Reed-Solomon 갈루아 필드($GF(2^8)$) 패리티 연산을 호스트 CPU 개입 없이 초고속 처리하는 하드웨어 가속기.

</details>

```text
[HW RAID vs JBOD/SDS 스토리지 계층 구조 비교]
 ├── HW RAID 아키텍처 (하드웨어 책임 모델)
 │   ├── 호스트 운영체제 ──────────── 단일 Virtual LUN 블록 디바이스로 인식
 │   ├── HW RAID 컨트롤러 카드 ────── 전용 하드웨어 ASIC + FBWC 캐시 메모리
 │   └── 물리 드라이브 어레이 ──────── SAS/SATA 드라이브 (RAID 5/6/10 바인딩)
 └── JBOD / SDS 아키텍처 (소프트웨어 책임 모델)
     ├── 분산 SDS 엔진 / 파일시스템 ── Ceph, ZFS, MinIO (복제/Erasure Coding 연산)
     ├── HBA 컨트롤러 (IT 모드) ────── 단순 프로토콜 변환기 (RAID 로직 배제)
     └── 개별 원시 물리 디스크 ─────── Raw Disks (1:1 개별 디바이스 노출)
```

선의 의미: 가지(`├──`, `└──`)는 하드웨어 소속 및 제어 주체; HW RAID는 컨트롤러가 패리티와 캐시를 전담하고, JBOD는 단순 HBA를 통해 상위 소프트웨어에 원시 디스크를 직결함

| 구성요소 | 책임 |
|:---|:---|
| HW RAID 컨트롤러 | **FBWC·패리티·리빌드** 처리 |
| 가상 LUN | 물리 디스크의 **단일 볼륨 추상화** |
| HBA IT 모드 | 원시 디스크의 **1:1 패스스루** |
| 분산 SDS 엔진 | **복제·이레이저 코딩·자가 치유** |
| 원시 물리 디스크 | 상태·블록 장치의 **직접 노출** |

#### 한줄 요약
- HW RAID는 컨트롤러 카드가 모든 책임을 지며, JBOD는 단순 HBA를 통해 소프트웨어에 자원을 직결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Back vs Write-Through**: FBWC 캐시에 쓰고 즉시 호스트에 I/O 성공을 반환하는 방식(Write-Back)과 실제 물리 디스크 기록 완료까지 대기하는 동기식 방식(Write-Through).

</details>

```text
[스토리지 쓰기 요청 인입]
                │
                ▼
1. 스토리지 컨트롤러 유형(HW RAID vs JBOD) 판별
                │
                ▼
2. FBWC 캐시 Write-Back 기록 또는 HBA 원시 디스크 패스스루
                │
                ▼
3. 하드웨어 ASIC 패리티 연산 또는 분산 SDS 네트워크 복제
                │
                ▼
4. 물리 디스크 블록 영구 기록 및 트랜잭션 커밋 완료
                │
                ▼
[스토리지 I/O 정상 완료]
```

분기 결과: HW RAID는 **FBWC 캐시**를 통해 초저지연 로컬 쓰기를 수행하며 JBOD는 **SDS 분산 복제**로 무중단 내구성을 달성함

**동작 원리**

1. 스토리지 컨트롤러 유형(HW RAID vs JBOD) 판별
2. FBWC 캐시 Write-Back 기록 또는 HBA 원시 디스크 패스스루
3. 하드웨어 ASIC 패리티 연산 또는 분산 SDS 네트워크 복제
4. 물리 디스크 블록 영구 기록 및 트랜잭션 커밋 완료

#### 한줄 요약
- HW RAID로 갈리면 캐시에 적은 시점을 완료로 응답해 디스크 도달 비용을 뒤로 미루고 패리티 연산까지 ASIC이 떠안는 대신 컨트롤러 자체가 단일 고장점이 되고, JBOD로 갈리면 그 계층을 걷어낸 대가로 내구성 비용을 네트워크 복제로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **JBOF(Just a Bunch of Flash)**: 수십 개의 NVMe SSD를 고밀도 섀시에 장착하여 PCIe 스위치 또는 NVMe-oF(RoCEv2) 패브릭으로 다중 서버에 공유하는 올플래시 스토리지.

</details>

| 스토리지 아키텍처 | 하드웨어 RAID 컨트롤러 (HW RAID) | JBOD / HBA 패스스루 (JBOD / SDS) | 올플래시 JBOF (NVMe-oF) |
|:---|:---|:---|:---|
| 데이터 보호 주체 | **전용 하드웨어 ASIC** / 펌웨어 | **상위 파일시스템(ZFS) 및 분산 SDS** | 분산 SDS 및 RDMA 스토리지 |
| 캐싱 가속 방식 | **FBWC 캐시 Write-Back 가속** | 호스트 NVMe 저널 / 캐시 티어링 | 엔드포인트 DRAM 캐시 직결 |
| 스토리지 확장성 | 단일 서버 내부 수량 한계 | **노드 추가 기반 수평 확장** | **초고속 NVMe-oF 네트워크 공유** |
| 주요 적용 분야 | **단일 RDBMS, 엔터프라이즈** | **Ceph, vSAN, 대규모 오브젝트** | **AI 초거대 모델 학습, 빅데이터** |

#### 한줄 요약
- 단일 서버 RDBMS는 HW RAID가, 대규모 클라우드 스토리지에는 JBOD(SDS)와 JBOF가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVMe 캐시 티어링(NVMe Cache Tiering)**: JBOD 구성 시 소프트웨어 동기식 복제로 인한 쓰기 지연을 극복하기 위해 고성능 NVMe SSD를 쓰기 저널(WAL) 계층으로 전면 배치하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| JBOD 구성 시 소프트웨어 쓰기 지연 | **고성능 NVMe 저널/캐시 티어링(WAL)** 전면 배치 | 디스크 지연 완화 및 **IOPS 극대화** |
| 단일 RAID 카드 장애 시 볼륨 마비 | **액티브-액티브 듀얼 컨트롤러** 이중화 구축 | 단일 장애점(SPOF) 제거 및 **무중단 HA** |
| SDS 환경에서 RAID 사용 시 충돌 | RAID 카드를 **HBA IT 모드(패스스루)**로 플래싱 | 디스크 감시 및 **SDS 자가 치유** 보장 |
| 대용량 HDD 리빌드 중 2차 고장 | **RAID 6(이중 패리티)** 또는 **이레이저 코딩** 전환 | 다중 디스크 장애 시 **데이터 보존** |

#### 한줄 요약
- 실무에서는 NVMe 티어링으로 속도를 올리고, 듀얼 컨트롤러로 HA를 보장하며, IT 모드로 SDS 호환성을 확보한다.

## Ⅶ. 결론

- 단일 노드 캐시·복구는 **HW RAID**, 분산 확장은 **JBOD·SDS** 선택

#### 한줄 요약
- 스토리지 아키텍처는 단일 노드 하드웨어 캐싱 가속과 분산 소프트웨어 확장성 간의 요구사항에 맞춰 최적으로 선택해야 한다.
