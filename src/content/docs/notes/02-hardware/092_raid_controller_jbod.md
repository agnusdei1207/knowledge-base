---
sidebar:
  order: 92
  label: "092. RAID 컨트롤러•JBOD"
  badge:
    text: "미출 • 50%"
    variant: note
title: "RAID 컨트롤러•JBOD (RAID Controller and JBOD)"
date: "2026-08-17T09:25:00+09:00"
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

- **HW RAID Controller**: 전용 XOR/Reed-Solomon 연산 ASIC 및 캐시 메모리를 탑재하여 디스크 스트라이핑, 미러링, 패리티 연산을 하드웨어로 처리하는 스토리지 카드.
- **JBOD(Just a Bunch of Disks)**: 물리 드라이브들을 RAID로 묶지 않고 각각 독립된 개별 블록 디바이스로 운영체제에 그대로 노출하는 구조.
- **SDS(Software-Defined Storage)**: 하드웨어 RAID 컨트롤러 대신 Ceph, GlusterFS, VMware vSAN, ZFS 등 소프트웨어 계층에서 데이터 복제(Replication) 및 이레이저 코딩을 수행하는 분산 스토리지.

</details>

- 정의/개념: 다수의 물리 디스크를 전용 하드웨어 ASIC 및 배터리 백업 캐시(BBU/FBWC)를 통해 단일 고신뢰성 볼륨으로 묶어주는 HW RAID 컨트롤러와, 하드웨어 추상화 없이 원시 디스크(Raw Disk)를 운영체제 및 SDS(Software-Defined Storage)에 1:1 직결 노출하는 JBOD(Just a Bunch of Disks)의 스토리지 구성 아키텍처 비교
- 배경/필요성: 단일 서버 무중단 고가용성(RAID)과 클라우드 분산 스케일아웃(JBOD) 간 데이터 보호 책임 계층 및 복구 트레이드오프 분석 필요

#### 한줄 요약

- 하드웨어 ASIC 기반 패리티 제어의 **HW RAID**와 원시 디스크 1:1 직결 기반의 **JBOD(SDS)** 비교

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **BBU/FBWC(Flash-Backed Write Cache)**: 서버 전원 차단 시 DRAM 캐시의 미기록 데이터를 슈퍼캐퍼시터 전력으로 플래시 메모리에 즉시 백업하는 전력 장애 보호 장치.
- **HBA Passthrough Mode(IT Mode)**: RAID 카드의 가상 볼륨 관리 기능을 비활성화하고 물리 드라이브를 OS에 직접 1:1로 패스스루하는 HBA 동작 모드.
- **Rebuild Penalty**: RAID 배열에서 단일 드라이브 고장 시 새 드라이브로 교체 후 패리티를 역계산하여 복구하는 과정에서 발생하는 극심한 I/O 성능 저하 현상.

</details>

- 배터리/플래시 보호 캐시(**FBWC**)를 통해 정전 시에도 데이터 유실 없이 초고속 Write-Back 캐싱을 지원하는 **HW RAID**
- 하드웨어 개입 없이 원시 디스크의 S.M.A.R.T 텔레메트리와 직접 I/O 제어권을 소프트웨어로 넘기는 **JBOD (HBA Passthrough)**
- 대용량 드라이브 고장 시 수십 시간 동안 I/O 병목을 유발하는 **하드웨어 리빌드 페널티 vs 소프트웨어 네트워크 병렬 복구**

#### 한줄 요약

- **BBU/FBWC 쓰기 캐시 가속(RAID) vs HBA Passthrough 원시 I/O(JBOD)·소프트웨어 장애 제어**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RAID Engine (XOR/P+Q ASIC)**: CPU 대신 RAID 5/6 패리티 계산을 전담하여 메인 프로세서 부하를 0으로 만드는 전용 연산기.
- **Passthrough Controller(HBA)**: 드라이브 번역 없이 SAS/SATA/NVMe 프로토콜 프레임을 OS 드라이버로 직접 중계하는 저지연 브리지.

</details>

```text
[ HW RAID 컨트롤러 vs JBOD 패스스루 아키텍처 비교 ]
 
 [ 1. HW RAID 아키텍처 ]             [ 2. JBOD / SDS 아키텍처 ]
┌──────────────────────────────┐    ┌──────────────────────────────┐
│ 호스트 OS (단일 Logical LUN) │    │ 호스트 OS / 분산 SDS (Ceph)  │
├──────────────────────────────┤    ├──────────────────────────────┤
│ RAID 컨트롤러 카드 (HW ASIC) │    │ HBA 카드 (Passthrough IT Mode│
│  ├─ FBWC 쓰기 캐시 (BBU 보호)│    └──────────────┬───────────────┘
│  └─ 하드웨어 패리티 가속 엔진│                   │ [ 개별 원시 디스크 1:1 노출 ]
└──────────────┬───────────────┘    ┌──────────────▼──────────────┐
               │ [ RAID 5/6 볼륨 ]  │ Disk 1 │ Disk 2 │ Disk 3 │..│
┌──────────────▼──────────────┐    └──────────────────────────────┘
│ 물리 드라이브 어레이 (HDD/SSD)│
└─────────────────────────────┘
```

선의 의미: 호스트 I/O 요청, RAID 전용 ASIC/BBU 캐시, HBA Passthrough 컨트롤러 및 물리 HDD/SSD 드라이브 간의 스토리지 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 서버 | 스토리지 계층에 단일 LUN 또는 개별 물리 드라이브 단위로 I/O 명령을 발행하는 서버 |
| FBWC 쓰기 캐시(BBU) | 정전 시에도 미기록 캐시 데이터를 플래시로 백업 보존하는 하드웨어 보호 캐시 메모리 |
| 하드웨어 RAID 엔진 | CPU 대신 XOR 및 Reed-Solomon 패리티 연산을 전담 수행하는 전용 하드웨어 가속 ASIC |
| HBA 패스스루 컨트롤러 | 가상화나 패리티 처리 없이 물리 드라이브를 OS 및 SDS 계층에 1:1 직접 노출하는 인터페이스 카드 |
| 물리 드라이브(HDD/SSD) | 실제 데이터를 저장하며 S.M.A.R.T 텔레메트리로 디바이스 상태를 보고하는 저장 매체 |

#### 한줄 요약

- **호스트 서버·BBU/FBWC 쓰기 캐시·하드웨어 RAID 엔진(XOR/P+Q)·HBA Passthrough 컨트롤러·물리 드라이브**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Back vs Write-Through**: 데이터를 배터리 백업 캐시에만 쓰고 즉시 성공을 반환하는 고속 방식(Write-Back)과, 실제 물리 디스크 미디어에 기록될 때까지 대기하는 동기식 방식(Write-Through).

</details>

```text
[ 스토리지 쓰기 요청 처리 및 복제 경로 흐름 ]
                         │
                         ▼
   [ 1. 아키텍처 경로 선정 (단일 서버 HW RAID vs 클라우드 분산 SDS) ]
        /                                               \
   [ HW RAID 경로 ]                               [ JBOD / SDS 경로 ]
        │                                               │
   [ 2. FBWC 캐시에 Write-Back 기록 ]             [ 4. HBA 가 원시 디스크로 직접 전달 ]
        │                                               │
   [ 3. RAID ASIC 이 패리티 분할 계산 후 ]        [ 5. 상위 SDS 소프트웨어가 ]
   [ 물리 디스크 스트라이프에 비동기 기록 ]       [ 네트워크 다중 노드로 병렬 복제 ]
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
   [ 6. 쓰기 완료 응답 및 트랜잭션 종결 ]
```

**동작 원리**

1. **경로 분기**: 고성능 단일 서버는 HW RAID, 분산 클라우드 환경은 JBOD/SDS로 분기
2. **RAID 캐싱**: Write-Back 모드에서 FBWC 캐시에 데이터 적재 후 즉각 ACK 반환
3. **하드웨어 패리티**: 컨트롤러 ASIC이 XOR 연산을 수행하여 데이터와 패리티를 복수 디스크에 기록
4. **JBOD 패스스루**: HBA가 I/O 명령을 변환 없이 타깃 원시 디스크로 직접 전달
5. **소프트웨어 복제**: Ceph/ZFS가 3중 복제(3-Way Replication) 또는 이레이저 코딩으로 다중 서버에 분산 기록

#### 한줄 요약

- 아키텍처 선정(HW RAID vs JBOD/SDS) $\to$ **RAID 경로(BBU 캐시 Write-Back $\to$ 하드웨어 패리티 계산 및 드라이브 분산) vs JBOD 경로(HBA Passthrough $\to$ SDS 다중 복제/Erasure Coding) $\to$ 쓰기 완료**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HW RAID vs JBOD/SDS**:
  - HW RAID: 전용 하드웨어 ASIC/BBU, Write-Back 캐시 가속, 단일 서버 DB/OS 볼륨
  - JBOD/SDS: HBA 직결 패스스루, 소프트웨어 정의 분산 복제, 대규모 클라우드 스토리지

</details>

| 비교 항목 | 하드웨어 RAID 컨트롤러 (HW RAID) | JBOD / HBA 패스스루 (JBOD / SDS) |
|:---|:---|:---|
| 데이터 보호 구현 계층 | 전용 하드웨어 RAID ASIC 및 온보드 펌웨어 | 상위 OS 커널 파일시스템(ZFS) 또는 분산 SDS(Ceph) |
| 캐싱 및 쓰기 가속 | BBU/플래시 보호(FBWC) Write-Back 캐시 가속 | 드라이브 자체 캐시 또는 NVMe 저널/캐시 티어링 |
| 한계 및 주 적용 분야 | 컨트롤러 고장 시 단일 실패점(SPOF), 단일 서버 DB | 컨트롤러 캐시 부재로 단일 노드 성능 저하, 분산 클라우드 |

#### 한줄 요약

- 단일 서버 고성능 DB는 **HW RAID**, 대규모 분산 스케일아웃은 **JBOD(SDS)**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IT Mode(Initiator Target Mode)**: RAID 카드의 메가RAID 펌웨어를 순수 HBA 통과 펌웨어로 교체(Flashing)하여 ZFS/Ceph와의 호환성을 극대화하는 엔지니어링 튜닝.
- **NVMe Cache Tiering**: JBOD 구성 시 쓰기 성능 저하를 방지하기 위해 초고속 NVMe SSD를 저널(WAL)/캐시 계층으로 전면에 배치하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| JBOD 구성 시 소프트웨어 계층 동기식 복제로 인한 쓰기 I/O 지연시간 증가 | 초고속 **NVMe SSD 저널(WAL)/캐시 티어링 계층** 전면 배치 | 원시 디스크 쓰기 지연 완화 및 분산 처리량 개선 |
| 단일 HW RAID 컨트롤러 고장 시 전체 LUN 볼륨 접근 불가(SPOF) 위험 | **듀얼 액티브-스탠바이/액티브-액티브 RAID 컨트롤러** 이중화 구성 | 컨트롤러 단일 장애점 제거 및 무중단 스토리지 서비스 가용성 보장 |
| ZFS, Ceph 등 SDS 환경에서 HW RAID 볼륨 중복 매핑 시 디스크 제어 및 복구 충돌 | RAID 카드를 **HBA IT(Initiator Target) 모드(패스스루)** 로 플래싱하여 개별 드라이브 직접 노출 | SDS 소프트웨어의 완벽한 물리 디스크 텔레메트리 감시 및 자가 치유 기능 보장 |

#### 한줄 요약

- **SDS 전용 NVMe Write-Buffer 티어링·듀얼 RAID 컨트롤러(HA) 구축·ZFS/Ceph 도입 시 HBA IT(Initiator Target) 모드 플래싱**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **JBOF(Just a Bunch of Flash) 및 NVMe-oF 진화**: HDD 중심의 JBOD에서 수십 개의 U.2/E1.S NVMe SSD를 장착하고 RoCEv2 네트워크로 풀링하는 JBOF 아키텍처로 진화.

</details>

- 차세대 하이퍼컨버지드(HCI) 및 분산 클라우드 인프라에서 **NVMe-oF 기반 JBOD 풀링 및 소프트웨어 정의 이레이저 코딩(Erasure Coding) 표준 채택**

#### 한줄 요약

- **단일 서버 하드웨어 신뢰성(RAID)과 분산 소프트웨어 확장성(JBOD)** 의 최적 선택
