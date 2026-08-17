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
- 배경/필요성: 단일 서버 레벨의 무중단 고가용성(RAID)과 클라우드 네이티브 대규모 분산 스케일아웃(Ceph/vSAN/ZFS 기반 JBOD) 환경 간의 **데이터 보호 책임 계층 및 복구 트레이드오프 분석 필수**

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
               │ [ RAID 5/6 볼륨 ]  │ Disk 1 │ Disk 2 │ Disk 3 │...│
┌──────────────▼──────────────┐    └──────────────────────────────┘
│ 물리 드라이브 어레이 (HDD/SSD)│
└─────────────────────────────┘
```

선의 의미: 호스트 I/O 요청, RAID 전용 ASIC/BBU 캐시, HBA Passthrough 컨트롤러 및 물리 HDD/SSD 드라이브 간의 스토리지 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 | "이 데이터 안전하게 저장해!" 하고 디스크 덩어리(LUN)나 개별 디스크에 냅다 명령을 갈기는 메인 서버 |
| 보호 쓰기 캐시 | **비비유(BBU)** 배터리 등에 업고서, 전원이 뽑혀도 저장 중이던 데이터를 꽉 쥐고 버티는 생명줄 캐시 |
| 레이드 엔진 | 하드디스크 10개를 1개처럼 묶고, 에러 복구용 수학 계산(XOR 패리티)을 미친 듯이 돌려대는 하드웨어 가속기 |
| 패스스루 컨트롤러 | "난 묶는 거 몰라" 하면서 디스크 10개를 OS에 낱개 10개로 쿨하게 던져버리는 **제이보드(JBOD)** 커넥터 |
| 물리 디스크 | 실제로 데이터를 짱박아두고 뻑나면 S.M.A.R.T 진단값으로 "나 죽어간다"고 비명 지르는 하드/SSD |

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
| **제이보드** 쓰면서 소프트웨어로만 복제하려니 속도가 구토 나올 정도로 느려 터짐 | 속도 미친 비싼 캐시 디스크(NVMe) 꽂아서 거기다 먼저 박고 천천히 복제하는 꼼수 시전 | 캐시 없는 생짜 디스크의 미친 지연시간(Latency)을 씹어먹고 쓸만한 성능 방어 |
| 레이드 카드 고장 났더니 디스크 20개 묶인 게 통째로 날아가는 기적의 동반 자살 사태 | 돈 두 배로 발라서 똑같은 레이드 카드를 2개 꽂아놓는 **듀얼 레이드 컨트롤러** 떡칠 | 카드 하나 뻗어도 옆 카드가 멱살 잡고 살려내서 서버 단일 장애점(SPOF) 완벽 파괴 |
| 최신 클라우드 소프트웨어(**SDS**) 썼는데 레이드 카드가 몰래 묶어버려서 디스크 관리가 다 꼬임 | 쓸데없이 묶는 짓거리 막아버리고 무조건 **패스스루 모드**(JBOD)로 낱개로 까발려버림 | 하드웨어랑 소프트웨어가 겹쳐서 싸우는 뻘짓을 막고 소프트웨어에 절대 권력 위임 |

#### 한줄 요약

- **SDS 전용 NVMe Write-Buffer 티어링·듀얼 RAID 컨트롤러(HA) 구축·ZFS/Ceph 도입 시 HBA IT(Initiator Target) 모드 플래싱**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **JBOF(Just a Bunch of Flash) 및 NVMe-oF 진화**: HDD 중심의 JBOD에서 수십 개의 U.2/E1.S NVMe SSD를 장착하고 RoCEv2 네트워크로 풀링하는 JBOF 아키텍처로 진화.

</details>

- 차세대 하이퍼컨버지드(HCI) 및 분산 클라우드 인프라에서 **NVMe-oF 기반 JBOD 풀링 및 소프트웨어 정의 이레이저 코딩(Erasure Coding) 표준 채택**

#### 한줄 요약

- **단일 서버 하드웨어 신뢰성(RAID)과 분산 소프트웨어 확장성(JBOD)**의 최적 선택
