---
sidebar:
  order: 80
  label: "080. 스토리지 계층: DAS•NAS•SAN"
  badge:
    text: "미출 · 50%"
    variant: note
title: "스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
date: "2026-08-25T10:25:00+09:00"
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
- **NAS(Network Attached Storage)**: 범용 TCP/IP LAN 망에 접속하여 파일 시스템 레벨(NFS/SMB)로 파일 공유 서비스를 제공하는 스토리지.
- **SAN(Storage Area Network)**: 고속 전용 파이버 채널(FC) 또는 IP 패브릭을 구축하여 블록(Block) 레벨 스토리지를 할당하는 고성능 스토리지 전용망.

</details>

- 정의/개념: 서버와 스토리지 간의 연결 방식과 I/O 접근 단위(Block vs File)에 따라 분류하는 **스토리지 계층(DAS·NAS·SAN)**
- 배경/필요성: 단일 서버 로컬 디스크의 용량 및 공유 한계로 인해 **대규모 데이터 공유 및 무중단 스토리지 확장 불가**

#### 한줄 요약
- 직접 연결형 DAS, 이더넷 파일 공유형 NAS, 고속 전용 블록망 SAN으로 계층화된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **블록 레벨 I/O(Block-Level I/O)**: 파일 시스템 없이 디스크의 원시 논리 블록 주소(LBA)에 직접 읽기/쓰기를 수행하는 초저지연 I/O 방식 (DAS, SAN).
- **파일 레벨 I/O(File-Level I/O)**: 스토리지 내부 파일 시스템이 관리하는 파일/디렉터리 경로 기반으로 데이터를 요청하는 방식 (NAS).
- **MPIO(Multi-Path I/O)**: 서버와 스토리지 사이에 복수의 물리 경로를 구성하여 로드 밸런싱과 장애 시 자동 페일오버를 지원하는 다중 경로 기술.

</details>

- 호스트가 파일 시스템을 직접 포맷하고 LBA를 제어하는 **블록 레벨 I/O(DAS, SAN)**
- 스토리지 전용 OS가 파일 시스템을 관리하고 표준 네트워크 프로토콜로 공유하는 **파일 레벨 I/O(NAS)**
- **MPIO(Multi-Path I/O)** 다중 경로 구성을 통한 단일 장애점(SPOF) 제거 및 가용성 확보

#### 한줄 요약
- 접근 단위(Block/File)와 전송망 구조에 따라 성능, 공유성, 확장성을 차별화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HBA(Host Bus Adapter)**: 서버 호스트와 SAN 광 파이버 채널(FC) 또는 SAS 패브릭 간을 연결하는 전용 고속 컨트롤러 카드.
- **LUN(Logical Unit Number)**: SAN 스토리지 어레이에서 가상화되어 호스트 서버에 단일 디스크처럼 할당되는 논리 블록 볼륨.

</details>

```text
[엔터프라이즈 스토리지 아키텍처 계층]
|-- DAS 계층 : 호스트 서버 -> SAS/NVMe 전용 케이블 직결 -> 전용 드라이브
|-- NAS 계층 : 다중 클라이언트 -> 범용 TCP/IP LAN (NFS/SMB) -> NAS 어플라이언스
`-- SAN 계층 : 호스트 클러스터 (HBA 카드 장착)
    |-- SAN 스위칭 패브릭 (FC 광 스위치 / 100GbE RoCEv2 패브릭)
    `-- All-Flash 스토리지 어레이 (컨트롤러·RAID 엔진·LUN 1~N)
```

선의 의미: 계층 및 물리 네트워크 연결 토폴로지

| 구성요소 | 책임 |
|:---|:---|
| 호스트 서버 / 클라이언트 | 파일(NFS/SMB) 또는 블록(SCSI/NVMe) I/O 읽기·쓰기 요청 발행 |
| 전송 네트워크 경로 | 점대점 케이블(DAS), 범용 이더넷 LAN(NAS), 광 FC 패브릭(SAN) 제공 |
| 스토리지 컨트롤러 | RAID 패리티 연산, 캐싱, 가상화 볼륨 프로비저닝 및 타깃 포트 제어 |
| **LUN(Logical Unit Number)** | SAN 환경에서 호스트에 단일 물리 디스크 드라이브로 인식되는 가상 블록 볼륨 |
| **HBA(Host Bus Adapter)** | 호스트 OS 블록 명령어를 FC 프레임 또는 NVMe-oF 패킷으로 직렬화 전송 |

#### 한줄 요약
- 호스트 HBA, 전송 패브릭, 스토리지 컨트롤러, LUN 볼륨이 통합되어 스토리지 망을 형성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Zoning(조닝)**: FC 스위치에서 특정 HBA WWN과 스토리지 포트 간의 가상 통신 구역을 분리하는 패브릭 보안.
- **LUN Masking(LUN 마스킹)**: 스토리지 컨트롤러 단에서 인가된 호스트의 HBA ID에만 특정 LUN 볼륨이 보이도록 접근을 통제하는 기술.

</details>

```text
스토리지 요구사항 수립 (I/O 접근 단위 판별)
        │
   파일 공유형인가, 원시 블록형인가?
   ┌────┴─────┐
[파일 레벨 (File)] [블록 레벨 (Block)]
   │             │
NAS 채택        스토리지 공유 및 규모 범위 판별
(NFS / SMB)      ┌──┴───┐
                 [단일 서버] [다중 서버 공유]
                  │          │
                 DAS 채택   SAN 채택 (FC / iSCSI / NVMe-oF)
                             │
                        FC 스위치 Zoning 및 LUN Masking 보안 체결
                             │
                        MPIO 다중 경로 로드밸런싱 가동
```

#### 한줄 요약
- 접근 단위(File vs Block) 판별 → 공유 범위(단일 vs 다중) 판정 → 스토리지 방식 결정 → 보안 및 MPIO 체결 순으로 구성된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **iSCSI**: 고가의 FC 장비 대신 범용 TCP/IP 이더넷 망 상에서 SCSI 블록 명령어를 캡슐화하여 전송하는 SAN 프로토콜.

</details>

| 스토리지 아키텍처 | DAS (Direct Attached) | NAS (Network Attached) | SAN (Storage Area Network) | NVMe-oF SAN |
|:---|:---|:---|:---|:---|
| 접근 단위 및 프로토콜 | 블록 레벨 (SAS/NVMe) | 파일 레벨 (NFS/SMB) | 블록 레벨 (FC/iSCSI) | 블록 레벨 (RoCEv2/FC) |
| 연결 네트워크 | 점대점 전용 케이블 직결 | 범용 TCP/IP 이더넷 LAN | 전용 광 파이버 채널(FC) | 100GbE+ 초고속 RDMA 패브릭 |
| 주요 용도 | 단일 서버 OS/로컬 DB | 파일 서버, VDI, 미디어 공유 | 엔터프라이즈 DB, 가상화 팜 | AI 분산 학습, 초고성능 All-Flash |
| 한계점 | 서버 간 스토리지 공유 불가 | 네트워크 혼잡 시 지연 발생 | 구축 비용 고가 및 전문 관리 | 인프라 비용 및 RoCE 무손실망 필수 |

#### 한줄 요약
- 단일 장비는 DAS, 범용 파일 공유는 NAS, 대규모 고성능 블록 풀링에는 SAN/NVMe-oF를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVMe-oF(NVMe over Fabrics)**: RoCEv2 또는 FC 패브릭 상에서 NVMe 프로토콜을 전달하여 SAN 지연시간을 수 $\mu s$ 단위로 단축하는 고속 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다중 클라이언트 I/O 집중으로 NAS 대역폭 포화 | 25GbE 인터페이스 도입 및 LACP(802.3ad) 본딩 | 네트워크 대역폭 다중화 및 전송 병목 해소 |
| 단일 HBA 또는 FC 케이블 단선 시 서비스 중단 | **MPIO(Multi-Path I/O)** 이중화 및 액티브-액티브 구성 | 무중단 페일오버 및 단일 장애점(SPOF) 원천 배제 |
| SAN 패브릭 공유 환경에서 타 서버 LUN 무단 침범 | FC 스위치 **Zoning** 및 스토리지 **LUN Masking** 적용 | 비인가 호스트 볼륨 접근 차단 및 테넌트 격리 |
| 스토리지 I/O 지연으로 인한 고성능 DB 병목 | **NVMe-oF(RoCEv2)** 도입 및 All-Flash NVMe 풀 구축 | 스토리지 레이턴시 80% 단축 및 IOPS 극대화 |

#### 한줄 요약
- LACP 대역폭 확장, MPIO 경로 이중화, Zoning/LUN Masking 보안, NVMe-oF 도입으로 고가용성을 보장한다.

## Ⅶ. 결론

- 파일 공유는 **Scale-Out NAS**, 고성능 트랜잭션 DB 및 가상화 인프라는 **NVMe-oF All-Flash SAN**을 구축하고, **MPIO 이중화**로 무중단 연속성 확립

#### 한줄 요약
- 워크로드의 I/O 특성(파일 vs 블록)과 성능 요구치에 따라 DAS, NAS, SAN을 최적 배치하는 것이 스토리지 아키텍처의 핵심이다.