---
sidebar:
  order: 80
  label: "080. 스토리지 계층: DAS•NAS•SAN"
  badge:
    text: "미출 · 50%"
    variant: note
title: "스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 80
extra:
  question_no: "080"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "직결•파일•패브릭 I/O 선택 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DAS(Direct Attached Storage)**: 서버 본체에 전용 케이블(SAS/SATA/NVMe)로 저장장치를 1:1 직접 연결하는 전용 스토리지.
- **NAS(Network Attached Storage)**: 범용 TCP/IP LAN 망에 접속하여 파일 시스템 레벨(NFS/SMB)로 다중 클라이언트에게 파일 공유 서비스를 제공하는 어플라이언스.
- **SAN(Storage Area Network)**: 고속 전용 파이버 채널(FC) 또는 IP 패브릭을 구축하여 다중 서버에 블록(Block) 레벨 스토리지를 유연하게 할당하는 고성능 스토리지 전용망.

</details>

- 정의/개념: 서버와 스토리지 디바이스 간의 연결 방식, 전송 프로토콜 및 I/O 접근 단위(Block vs File)에 따라 직결형(DAS), 네트워크 파일 공유형(NAS), 전용 고속 패브릭 블록 스토리지망(SAN)으로 분류되는 엔터프라이즈 스토리지 아키텍처 계층
- 배경/필요성: 단일 서버 로컬 디스크 용량 한계 극복 및 고가용성(HA)·무중단 백업 기반 엔터프라이즈 스토리지 풀링 필요

#### 한줄 요약

- I/O 접근 단위(Block/File) 및 연결 패브릭에 따른 **DAS(직결)·NAS(파일 공유)·SAN(전용 블록망) 아키텍처** ## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Block-Level I/O**: 파일 시스템 없이 디스크의 원시 논리 블록 주소(LBA)에 직접 읽기/쓰기를 수행하는 초저지연 I/O 방식 (DAS, SAN).
- **File-Level I/O**: 스토리지 내부의 파일 시스템이 관리하는 파일/디렉터리 트리 경로 기반으로 데이터를 요청하는 방식 (NAS).
- **MPIO(Multi-Path I/O)**: 서버와 스토리지 사이에 복수의 물리 HBA/케이블 경로를 구성하여 로드 밸런싱과 장애 시 자동 페일오버를 지원하는 다중 경로 기술.

</details>

- 호스트 서버가 파일 시스템을 직접 포맷하고 원시 디스크 블록(LBA)을 제어하는 **블록 레벨 I/O (DAS, SAN)**
- 스토리지 장비가 자체 OS로 파일 시스템을 관리하고 이종 OS(Windows/Linux) 간 공유를 지원하는 **파일 레벨 I/O (NAS)**
- 전용 광케이블(FC) 및 무손실 스위치 패브릭을 통해 대규모 볼륨 통합 및 **MPIO 기반 고가용성(HA)** 지원

#### 한줄 요약

- **블록 I/O(DAS/SAN) vs 파일 I/O(NAS)·FC/iSCSI 전용 패브릭·MPIO 다중 경로 고가용성** ## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HBA(Host Bus Adapter)**: 서버 메인보드 PCIe 슬롯에 장착되어 파이버 채널(FC) 또는 SAS 패브릭과 통신하는 전용 인터페이스 카드.
- **FC Switch**: 파이버 채널 프로토콜 프레임을 전용 광 스위칭 패브릭을 통해 마이크로초 단위로 전달하는 스토리지 전용 스위치.
- **LUN(Logical Unit Number)**: 스토리지 어레이 내부의 RAID 볼륨을 논리적으로 분할하여 특정 호스트 서버에 블록 디스크로 마운트해 주는 논리 단위 번호.

</details>

```text
[ 엔터프라이즈 DAS / NAS / SAN 스토리지 계층 아키텍처 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ 1. 호스트 서버 (Host Server) │        │ 1. 클라이언트 (PC / VDI)     │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │                                       │
  [ 전용 케이블 (SAS/SATA) ]             [ 범용 IP 이더넷 (NFS/SMB) ]
               ▼                                       ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ 2. DAS 직결 스토리지         │        │ 2. NAS 파일 스토리지         │
└──────────────────────────────┘        └──────────────────────────────┘
 
┌─────────────────────────────────────────────────────────────────────┐
│ 3. SAN 전용 패브릭 (호스트 HBA ──> FC/iSCSI 스위치 ──> 스토리지 LUN) │
│  └─ 엔터프라이즈 All-Flash 스토리지 어레이 (LUN 1, LUN 2, LUN N)     │
└─────────────────────────────────────────────────────────────────────┘
```

선의 의미: 호스트 서버(HBA/NIC), 파일/블록 접근 프로토콜 계층, 물리 전송 채널(SAS/IP/FC) 및 엔터프라이즈 스토리지 배열(LUN/RAID) 간의 스토리지 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트·클라이언트 | 스토리지 계층에 파일 또는 블록 I/O 읽기/쓰기 요청을 발행하는 컴퓨팅 서버 및 단말 |
| 파일·블록 접근 계층 | NFS/SMB 파일 시스템 공유 규약 및 SCSI/NVMe 블록 명령어 캡슐화 처리 |
| 전송 네트워크 경로 | SAS 직결 케이블, IP 이더넷 스위치, FC 광 스위칭 패브릭 등 물리적 데이터 전송망 |
| 스토리지 어레이 | 디스크 드라이브를 RAID로 묶고 LUN 단위로 볼륨을 프로비저닝하는 저장장치 |

#### 한줄 요약

- **호스트 서버(HBA/NIC)·접근 계층(NFS/SMB/SCSI)·물리 전송 채널(SAS/Ethernet/FC)·스토리지 어레이(LUN/RAID)** ## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Zoning(조닝)**: FC 스위치에서 특정 HBA WWN(World Wide Name)과 스토리지 타깃 포트 간의 가상 통신 구역을 분리하는 패브릭 보안.
- **LUN Masking(LUN 마스킹)**: 스토리지 컨트롤러 단에서 인가된 호스트의 HBA ID에만 특정 LUN 볼륨이 보이도록 접근을 통제하는 기술.

</details>

```text
[ 스토리지 아키텍처 선정 및 접근 제어 흐름 ]
                         │
                         ▼
   [ 1. I/O 데이터 접근 단위 판별 (파일 공유형 vs 원시 블록형) ]
        /                                               \
   [ 파일 레벨 (File I/O) ]                       [ 블록 레벨 (Block I/O) ]
        │                                               │
   [ NAS 채택 (NFS / SMB) ]                [ 2. 스토리지 공유 및 규모 판별 ]
                                                /                 \
                                           [ 단일 호스트 ]     [ 다중 호스트 공유 ]
                                                │                 │
                                           [ DAS 채택 ]        [ SAN 채택 (FC/iSCSI) ]
                                                                  │
                                           [ 3. FC Zoning 및 LUN Masking 보안 적용 ]
                                                                  │
                                           [ 4. MPIO 다중 경로 로드밸런싱 가동 ]
```

**동작 원리** 1. **접근 단위 판정**: 다수 클라이언트 간 문서/미디어 파일 공유가 주 목적이면 NAS(NFS/SMB)로 분기
2. **블록 공유 판정**: 단일 서버 전용 초저비용 저장이면 DAS, 대규모 고성능 DB/가상화 클러스터면 SAN 분기
3. **패브릭 보안 설정**: SAN 구성 시 비인가 접근을 차단하기 위해 FC 스위치 Zoning 및 스토리지 LUN Masking 체결
4. **MPIO 경로 가동**: 호스트 OS의 MPIO 드라이버가 다중 HBA 링크에 Round-Robin 또는 Failover 정책을 활성화

#### 한줄 요약

- I/O 단위(File vs Block) 판별 $\to$ **공유 범위(단일 vs 다중) 판정 $\to$ DAS(직결) / NAS(파일) / SAN(FC망) 결정 $\to$ Zoning & LUN Masking 보안 $\to$ MPIO 다중 경로 확정** ## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DAS vs NAS vs SAN 비교**:
  - DAS: 1:1 직결, 블록 I/O, 초저지연/저비용, 서버 간 공유 불가
  - NAS: 이더넷 LAN 망, 파일 I/O(NFS/SMB), 다기종 파일 공유, 네트워크 혼잡 시 지연
  - SAN: 전용 FC/IP 패브릭, 블록 I/O(FC/iSCSI), 최고 성능/확장성, 고비용

</details>

| 구분 | DAS (Direct Attached Storage) | NAS (Network Attached Storage) | SAN (Storage Area Network) |
|:---|:---|:---|:---|
| I/O 접근 단위 및 프로토콜 | 블록 레벨 (Block I/O), SAS/SATA/NVMe | 파일 레벨 (File I/O), NFS/SMB/CIFS | 블록 레벨 (Block I/O), FC/iSCSI/NVMe-oF |
| 연결 매체 및 네트워크 | 점대점 전용 케이블 직결 (No Network) | 범용 TCP/IP 이더넷 (LAN 공유망) | 전용 광 파이버 채널(FC) 또는 분리된 SAN 망 |
| 한계 및 주 적용 분야 | 서버 간 스토리지 공유 불가 (단일 서버 OS) | 네트워크 트래픽 혼잡 시 지연 (파일 서버/VDI) | 구축 비용 고가 및 복잡한 관리 (대규모 DB/가상화) |

#### 한줄 요약

- 로컬 직결은 **DAS**, 범용 파일 공유는 **NAS**, 고성능 엔터프라이즈 블록 풀은 **SAN** ## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVMe-oF(NVMe over Fabrics)**: RoCEv2(RDMA over Converged Ethernet) 또는 FC 패브릭 상에서 NVMe 명령을 전달하여 SAN 블록 전송 지연시간을 수 마이크로초 수준으로 단축하는 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 클라이언트의 동시 파일 I/O 집중으로 인한 NAS 이더넷 네트워크 대역폭 포화 | **10/25GbE 고속 인터페이스 도입 및 LACP(802.3ad) 링크 집성** 구성 | 네트워크 처리량 증대 및 병목 구간 해소 |
| 단일 HBA 포트 또는 FC 광케이블 장애 시 스토리지 연결 단절 및 시스템 다운 발생 | **MPIO(Multi-Path I/O) 이중화 경로 구축** 및 액티브-스탠바이/액티브-액티브 페일오버 구성 | 단일 장애점(SPOF) 제거 및 무중단 스토리지 가용성 보장 |
| SAN 패브릭 공유 환경에서 비인가 호스트의 타 서버 LUN 볼륨 무단 접근 및 데이터 오염 위험 | FC 스위치 레벨 **Zoning 구성** 및 스토리지 컨트롤러 레벨 **LUN Masking** 적용 | 비인가 호스트 볼륨 접근 원천 차단 및 데이터 격리 확보 |

#### 한줄 요약

- **10/25GbE LACP 링크 집성(NAS)·MPIO(다중 경로) 이중화 페일오버·FC Zoning 및 LUN Masking 볼륨 보안** ## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Unified Storage & SDS(소프트웨어 정의 스토리지)**: 단일 스토리지 컨트롤러에서 SAN(블록)과 NAS(파일), 오브젝트 스토리지를 모두 수용하고 Ceph/vSAN 등 SDS로 통합 관리하는 추세.

</details>

- 데이터센터 엔지니어링 구축 시 **단일 노드는 NVMe DAS, 파일 공유는 Scale-Out NAS, 고성능 DB는 NVMe-oF 기반 All-Flash SAN 표준 채택** #### 한줄 요약

- **I/O 프로토콜(Block vs File)과 대역폭/지연시간 요구치** 대상 맞춘 스토리지 계층화
