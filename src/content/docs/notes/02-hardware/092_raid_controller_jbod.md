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

- **하드웨어 RAID 컨트롤러(Hardware RAID Controller)**: 전용 XOR/Reed-Solomon 패리티 연산 ASIC 및 배터리 백업 캐시 메모리를 탑재하여 디스크 결함 복구와 볼륨 바인딩을 하드웨어로 자체 처리하는 전용 스토리지 카드.
- **JBOD(Just a Bunch of Disks)**: 물리 드라이브들을 RAID 컨트롤러로 묶지 않고, 각각 독립된 개별 원시(Raw) 블록 디바이스로 OS 및 소프트웨어 정의 스토리지(SDS) 계층에 1:1 직결 노출하는 구조.

</details>

- 정의/개념: 전용 ASIC 연산기와 비휘발성 캐시 기반으로 가상 볼륨을 제공하는 **HW RAID**와 물리 디스크를 OS에 1:1 패스스루하는 **JBOD(Just a Bunch of Disks) 아키텍처 비교**
- 배경/필요성: 단일 서버 하드웨어 신뢰성 중심 구조(RAID)와 클라우드 분산 스케일아웃 구조(JBOD/SDS) 간의 **스토리지 계층별 책임 분리, 복구 효율화 및 TCO 최적화 필요**

#### 한줄 요약
- 단일 서버의 하드웨어 캐시 가속(HW RAID)과 클라우드 분산 소프트웨어 정의 스토리지(JBOD)로 역할이 구분된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **플래시 백업 쓰기 캐시(Flash-Backed Write Cache, FBWC)**: 시스템 정전 시 슈퍼커패시터 전력으로 DRAM 캐시 데이터를 비휘발성 NAND 플래시 메모리에 즉시 백업하는 전력 장애 보호 장치.
- **IT 모드(Initiator Target Mode)**: RAID 카드의 하드웨어 볼륨 관리 및 캐싱 기능을 끄고 단순 HBA로 동작시켜 물리 드라이브를 OS에 직접 1:1 투명 패스스루하는 펌웨어 동작 모드.

</details>

- HW RAID의 강점: **FBWC(Flash-Backed Write Cache)** Write-Back 가속을 통한 극초저지연 쓰기 응답 및 불시 정전 시 100% 데이터 보호
- JBOD의 강점: HBA 직결 **IT 모드**를 통해 디스크 텔레메트리(S.M.A.R.T)를 상위 분산 SDS(Ceph, ZFS, MinIO)에 직접 투명하게 노출
- 복구 책임의 차이: HW RAID는 컨트롤러 ASIC이 단일 노드 내 패리티 재구축(Rebuild)을 전담하고, JBOD는 분산 네트워크가 다중 노드 병렬 복제 수행

#### 한줄 요약
- HW RAID는 전용 하드웨어로 데이터 신뢰성을 보장하며, JBOD는 소프트웨어에 원시 디스크 제어권을 위임한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **패리티 연산 엔진(Parity Engine ASIC)**: RAID 5/6의 XOR 및 Reed-Solomon 갈루아 필드($GF(2^8)$) 패리티 연산을 호스트 CPU 개입 없이 초고속 처리하는 하드웨어 가속기.

</details>

```text
[HW RAID vs JBOD/SDS 스토리지 계층 구조 비교]
 ┌─ [HW RAID 아키텍처 (하드웨어 책임 모델)]
 │   ├─ 호스트 운영체제 (단일 Logical Virtual LUN 블록 디바이스로 인식)
 │   ├─ [HW RAID 컨트롤러 카드] ── PCIe Gen4/Gen5 x8 슬롯 장착
 │   │   ├─ [전용 하드웨어 ASIC] ── XOR / Reed-Solomon 패리티 연산 엔진
 │   │   └─ [FBWC 캐시 메모리] ── DRAM 캐시 + 슈퍼커패시터 백업 유닛
 │   └─ 물리 드라이브 인클로저 ── SAS/SATA 드라이브 어레이 (RAID 5/6/10 바인딩)
 │
 └─ [JBOD / SDS 아키텍처 (소프트웨어 책임 모델)]
     ├─ [분산 SDS 엔진 / 파일시스템] ── Ceph, ZFS, MinIO, Lustre (복제/EC 연산)
     ├─ [HBA 컨트롤러 (IT 모드)] ────── 단순 프로토콜 변환기 (RAID 로직 완전 배제)
     └─ 개별 원시 물리 디스크 ──────── Disk 1, Disk 2, Disk N (1:1 개별 디바이스 노출)
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 제어 주체; HW RAID는 컨트롤러가 패리티와 캐시를 전담하고, JBOD는 단순 HBA를 통해 상위 소프트웨어에 원시 디스크를 직결함

| 비교 항목 | HW RAID 컨트롤러 책임 | JBOD / SDS 책임 |
|:---|:---|:---|
| **I/O 처리 방식** | **FBWC 캐시 Write-Back 가속 및 가상 LUN 단일 노출** | HBA 패스스루로 원시 디스크 1:1 직접 I/O 전달 |
| **패리티/복제 연산** | **전용 하드웨어 ASIC**이 XOR/RS 패리티 연산 전담 | 호스트 CPU/네트워크가 ZFS/Ceph 분산 Erasure Coding 연산 |
| **장애 복구 주체** | 드라이브 교체 시 로컬 컨트롤러가 백그라운드 리빌드 | 분산 네트워크를 통해 타 정상 노드에서 병렬 데이터 복제 |
| **디스크 상태 모니터링**| 컨트롤러 펌웨어가 드라이버 가상화 상태 보고 | 상위 SDS가 디스크 **S.M.A.R.T 텔레메트리 직접 감시** |
| **단일 장애점 (SPOF)** | **컨트롤러 카드 고장 시 볼륨 전체 접근 불가** | 개별 노드/디스크 장애 시에도 클러스터 전체 서비스 지속 |

#### 한줄 요약
- HW RAID는 컨트롤러 카드가 모든 책임을 지며, JBOD는 단순 HBA를 통해 소프트웨어에 자원을 직결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Back vs Write-Through**: FBWC 캐시에 쓰고 즉시 호스트에 I/O 성공을 반환하는 방식(Write-Back)과 실제 물리 디스크 기록 완료까지 대기하는 동기식 방식(Write-Through).

</details>

```text
1. 스토리지 아키텍처에 따른 쓰기(Write) 요청 인입
                      │
                      ▼
2. 스토리지 컨트롤러 유형 판별
   ┌──────────────────┴──────────────────┐
[ HW RAID 컨트롤러 ]                   [ JBOD / HBA (IT 모드) ]
   │                                     │
   ▼                                     ▼
3. FBWC 비휘발성 캐시에 Write-Back 기록  3. HBA가 원시 디스크로 직접 I/O 패스스루
   ➔ 호스트로 0.1ms 이내 즉각 성공 응답   │
   │                                     ▼
   ▼                                  4. 상위 SDS(Ceph/ZFS)가 네트워크 다중 노드로
4. 컨트롤러 하드웨어 ASIC이              병렬 복제(3-Way) 또는 Erasure Coding 분산 기록
   패리티(XOR/RS) 계산 후 디스크 스트라이핑 │
   │                                     │
   └──────────────────┬──────────────────┘
                      │
                      ▼
5. 트랜잭션 정상 커밋 완료
```

분기 결과: **HW RAID는** FBWC 캐시를 통해 초저지연 로컬 쓰기를 수행하며, **JBOD는** SDS 분산 복제를 통해 데이터센터급 내구성을 달성함

#### 한줄 요약
- 쓰기 인입 ➔ RAID 캐시 Write-Back 또는 JBOD 패스스루 SDS 복제 ➔ 트랜잭션 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **JBOF(Just a Bunch of Flash)**: 수십 개의 NVMe SSD를 고밀도 섀시에 장착하여 PCIe 스위치 또는 NVMe-oF(RoCEv2) 패브릭으로 다중 서버에 공유하는 올플래시 스토리지.

</details>

| 스토리지 아키텍처 | 하드웨어 RAID 컨트롤러 (HW RAID) | JBOD / HBA 패스스루 (JBOD / SDS) | 올플래시 JBOF (NVMe-oF) |
|:---|:---|:---|:---|
| 데이터 보호 및 복구 주체| **전용 하드웨어 RAID ASIC / 펌웨어** | **상위 OS 파일시스템(ZFS) 및 분산 SDS** | 분산 SDS 및 RDMA 스토리지 클러스터 |
| 캐싱 및 쓰기 가속 방식 | **FBWC BBU 캐시 Write-Back 가속** | 호스트 NVMe 저널 / 캐시 티어링 | 엔드포인트 NVMe DRAM 캐시 직결 |
| 스토리지 확장성 | 단일 서버 내부 드라이브 수량 한계 | **노드 추가를 통한 무제한 Scale-Out** | **초고속 NVMe-oF 네트워크 공유** |
| 주요 적용 분야 | **단일 고성능 RDBMS, 전통 엔터프라이즈**| **Ceph, vSAN, 하둡, 대규모 오브젝트** | **AI 초거대 모델 학습, 실시간 빅데이터** |

#### 한줄 요약
- 단일 서버 RDBMS는 HW RAID가, 대규모 클라우드 스토리지에는 JBOD(SDS)와 JBOF가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVMe 캐시 티어링(NVMe Cache Tiering)**: JBOD 구성 시 소프트웨어 동기식 복제로 인한 쓰기 지연을 극복하기 위해 고성능 NVMe SSD를 쓰기 저널(WAL) 계층으로 전면 배치하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| JBOD 구성 시 분산 소프트웨어 동기식 쓰기 레이턴시 증가 | **고성능 NVMe SSD 저널/캐시 티어링(WAL) 계층 전면 배치** | 디스크 쓰기 지연 80% 완화 및 IOPS 처리량 극대화 |
| 단일 HW RAID 컨트롤러 고장 시 전체 가상 볼륨 마비 | **액티브-액티브 듀얼 RAID 컨트롤러 이중화 섀시 구축** | 컨트롤러 단일 장애점(SPOF) 원천 배제 및 무중단 HA 확보 |
| ZFS/Ceph SDS 환경에서 HW RAID 구성 시 데이터 손상 | **RAID 카드를 HBA IT 모드(패스스루)로 펌웨어 플래싱** | 물리 디스크 상태 직접 감시 및 SDS 자가 치유 정상화 |
| 대용량 HDD(16TB+) RAID 5 리빌드 중 2차 고장으로 데이터 유실 | **RAID 6(이중 패리티) 또는 SDS 이레이저 코딩(8+3) 전환** | 리빌드 중 추가 디스크 장애 시에도 100% 데이터 보존 |

#### 한줄 요약
- 실무에서는 NVMe 티어링으로 속도를 올리고, 듀얼 컨트롤러로 HA를 보장하며, IT 모드로 SDS 호환성을 확보한다.

## Ⅶ. 결론

- 단일 고성능 트랜잭션 데이터베이스 서버는 **FBWC 캐시와 이중 패리티를 갖춘 HW RAID 6/10 컨트롤러를 구축**하고, 대규모 클라우드 및 AI 빅데이터 분산 인프라는 **HBA IT 모드 JBOD/JBOF 기반의 소프트웨어 정의 스토리지(SDS)를 표준 채택**하며, 디스크 확장 시 **NVMe 캐시 티어링과 이레이저 코딩**을 결합하는 최적 스토리지 아키텍처 확립

#### 한줄 요약
- 스토리지 아키텍처는 단일 노드 하드웨어 캐싱 가속과 분산 소프트웨어 확장성 간의 요구사항에 맞춰 최적으로 선택해야 한다.