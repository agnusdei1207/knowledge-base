---
sidebar:
  order: 80
  label: "080. 스토리지 계층: DAS•NAS•SAN"
  badge:
    text: "미출 · 50%"
    variant: note
title: "스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
date: "2026-09-07T09:45:00+09:00"
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

- **DAS(Direct Attached Storage)**: 서버 본체에 전용 케이블(SAS/SATA/NVMe)로 저장장치를 1:1 점대점으로 직접 연결하는 단독 전용 스토리지.
- **NAS(Network Attached Storage)**: 범용 TCP/IP 이더넷 LAN 망에 접속하여 파일 시스템 레벨(NFS/SMB)로 다중 이기종 클라이언트에 파일 공유 서비스를 제공하는 스토리지.
- **SAN(Storage Area Network)**: 고속 전용 파이버 채널(FC) 또는 IP 패브릭(RoCEv2)을 구축하여 호스트 서버에 원시 블록(Block) 볼륨을 할당하는 고성능 스토리지 전용망.

</details>

- 정의/개념: 연결 토폴로지와 데이터 I/O 접근 단위(Block vs File)에 따라 분류한 스토리지 계층(**DAS**·NAS·SAN) 아키텍처
- 배경/필요성: 서버 로컬 디스크의 데이터 사일로(Silo) 및 용량 확장 한계와 워크로드별 I/O 지연시간 요구에 따른 스토리지 자원 비효율

#### 한줄 요약
- 직접 직결형 DAS, 이더넷 파일 공유형 NAS, 고속 전용 블록망 SAN으로 계층화되어 워크로드별 I/O 요구를 분담한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **블록 레벨 I/O(Block-Level I/O)**: 파일 시스템 추상화 없이 디스크의 원시 논리 블록 주소(LBA)에 직접 읽기/쓰기를 수행하는 초저지연 I/O 방식 (DAS, SAN).
- **파일 레벨 I/O(File-Level I/O)**: 스토리지 내부의 파일 시스템이 파일과 디렉터리 트리 메타데이터를 관리하며 클라이언트는 파일 경로로 요청하는 방식 (NAS).
- **MPIO(Multi-Path I/O)**: 서버와 스토리지 사이에 복수의 물리적 파이버 채널/이더넷 경로를 구성하여 로드 밸런싱과 무중단 페일오버를 보장하는 다중 경로 기술.
- **NVMe-oF(NVMe over Fabrics)**: RoCEv2(RDMA) 또는 FC 패브릭 상에서 NVMe 명령어를 캡슐화하여 SAN 전송 지연을 마이크로초($\mu\text{s}$) 단위로 단축하는 초고속 규격.

</details>

- 접근 단위별 이원화: 호스트가 파일 시스템을 직접 포맷하는 **블록 레벨 I/O**와 스토리지 OS가 관리하는 **파일 레벨 I/O**
- 고성능 전용망 분리: SAN은 전용 파이버 채널 또는 **NVMe-oF**를 통해 스토리지 트래픽을 물리적 분리
- 무중단 고가용성: **MPIO(Multi-Path I/O)** 다중 경로 설계를 통해 경로 단선 시 무순단 절체 달성

#### 한줄 요약
- 블록(DAS/SAN)과 파일(NAS) 단위 접근, 전용 패브릭 분리, MPIO 다중 경로를 통해 성능과 고가용성을 차별화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HBA(Host Bus Adapter)**: 서버 호스트와 SAN 광 파이버 채널(FC) 또는 SAS 패브릭 간을 연결하는 전용 고속 컨트롤러 카드.
- **LUN(Logical Unit Number)**: SAN 스토리지 어레이에서 프로비저닝되어 호스트 서버에 단일 물리 디스크 드라이브처럼 인식되는 가상 블록 볼륨.

</details>

```text
[엔터프라이즈 스토리지 계층 구조]
  │
  ├─ [DAS 계층 (Direct Attached)]
  │     └─ [단일 호스트 직결] (SAS/PCIe 케이블, JBOD)
  │
  ├─ [NAS 계층 (Network Attached)]
  │     └─ [다중 클라이언트 파일 공유] (TCP/IP LAN, NFS/SMB)
  │
  └─ [SAN 계층 (Storage Area Network)]
        ├─ [호스트 클러스터] (서버별 HBA 카드)
        ├─ [SAN 스위칭 패브릭] (FC Switch, RoCEv2)
        └─ [All-Flash 어레이] (듀얼 컨트롤러, LUN 볼륨)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 **HBA** 카드 | 블록 명령의 FC·RoCE 변환 |
| SAN 스위칭 패브릭 | 무손실 프레임 라우팅 |
| 스토리지 컨트롤러 | RAID·캐시·**LUN** 매핑 |
| LUN 볼륨 | 호스트용 가상 블록 저장소 |
| NAS 어플라이언스 | NFS·SMB 파일 공유 |

#### 한줄 요약
- HBA가 호스트의 블록 명령을 패브릭 프레임으로 바꿔 전송 처리를 CPU에서 떼어 내고, 스토리지 컨트롤러의 LUN 매핑이 그 너머 물리 디스크의 배치를 가려 호스트에는 로컬 디스크와 다를 바 없는 블록 장치 하나만 남긴다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **패브릭 조닝(Zoning)**: SAN 스위치 상에서 특정 HBA 포트(WWN)와 스토리지 타깃 포트 간의 통신 경로를 가상으로 격리하는 패브릭 보안.
- **LUN 마스킹(LUN Masking)**: 스토리지 컨트롤러 단에서 인가된 호스트 HBA에게만 지정된 LUN 볼륨이 보이도록 접근을 통제하는 기술.

</details>

```text
1. 비즈니스 워크로드 요구사항 분석 (접근 단위 및 성능 판정)
                      │
                      ▼
2. 데이터 접근 단위(파일 레벨 vs 블록 레벨) 분기
   ├── [파일 레벨 (File I/O)]: NAS 아키텍처 선정 (범용 LAN에 NFS/SMB 구성)
   └── [블록 레벨 (Block I/O)]: 스토리지 공유 범위 판정
          ├── [단일 서버 전용]: DAS 선정 (SAS/NVMe 직결)
          └── [다중 서버 공유]: SAN 선정 (FC / NVMe-oF)
                      │
                      ▼
3. SAN 패브릭 보안 설정 (스위치 Zoning 및 스토리지 LUN Masking)
                      │
                      ▼
4. 호스트 MPIO 다중 경로 로드밸런싱 가동
                      │
                      ▼
[서비스 개시]: 무중단 엔터프라이즈 스토리지 인프라 가동
```

분기 결과: 파일 공유는 **NAS**, 단일 고속은 **DAS**, 고성능 다중 서버 블록 풀링은 **SAN**을 채택

#### 한줄 요약
- 파일 단위로 갈리면 파일시스템 해석을 스토리지 쪽에 넘겨 범용 LAN만으로 끝나지만, 블록 단위로 갈리면 해석을 호스트가 떠안는 대신 전용 패브릭과 Zoning·LUN Masking·MPIO라는 경로 관리 비용이 추가로 붙는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **iSCSI**: 고가의 광 FC 장비 대신 범용 TCP/IP 이더넷 망 상에서 SCSI 블록 명령어를 캡슐화하여 전송하는 IP-SAN 프로토콜.

</details>

| 스토리지 아키텍처 | DAS (Direct Attached) | NAS (Network Attached) | SAN (Fibre Channel SAN) | NVMe-oF SAN |
|:---|:---|:---|:---|:---|
| 데이터 접근 단위 | 블록 단위 (Raw LBA) | 파일 단위 (File Path) | 블록 단위 (SCSI **LUN**) | 블록 단위 (NVMe 네임스페이스) |
| 통신 인터페이스 | SAS, SATA, PCIe 직결 | 범용 TCP/IP (NFS, SMB) | 광 파이버 채널 (FC) | RoCEv2 / FC-NVMe |
| I/O 지연시간 | 수십 $\mu\text{s}$ (초저지연) | 수 ms (네트워크 오버헤드) | 수백 $\mu\text{s}$ (저지연) | 수십 $\mu\text{s}$ (초저지연) |
| 스토리지 공유성 | 불가 (단일 서버 전유) | 이기종 동시 파일 공유 | **LUN** 단위 분할 할당 | 초고속 클러스터 공유 |
| 주요 적용 분야 | 단일 서버 부팅, 캐시 | 파일 서버, 비정형 데이터 | 엔터프라이즈 DB, 가상화 | 대규모 AI 학습, All-Flash |

#### 한줄 요약
- 단일 서버는 DAS, 파일 공유는 NAS, 엔터프라이즈 트랜잭션 DB는 SAN, 대규모 AI 가속에는 NVMe-oF SAN을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **링크 어그리게이션(LACP, 802.3ad)**: NAS의 다중 이더넷 포트를 하나의 논리적 고대역폭 포트로 묶어 대역폭을 확장하고 장애 시 자동 절체하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다중 클라이언트 동시 접근 시 NAS 네트워크 대역폭 포화 | **LACP(802.3ad)** 포트 본딩 및 25GbE 인터페이스 도입 | 네트워크 대역폭 다중 확장 및 병목 해소 |
| 단일 HBA 또는 광 케이블 단선 시 SAN 스토리지 전체 마비 | HBA 이중화 및 **MPIO(Multi-Path I/O)** 액티브-액티브 구성 | 단일 장애점(SPOF) 배제 및 무중단 절체 |
| 공유 SAN 패브릭 상에서 비인가 서버의 타 테넌트 LUN 침범 | FC 스위치 **Zoning** 및 스토리지 **LUN Masking** 적용 | 테넌트 간 볼륨 침범 차단 및 보안 격리 |
| 스토리지 네트워크 I/O 지연으로 인한 고성능 DB 병목 | **NVMe-oF(RoCEv2)** All-Flash 어레이 도입 | I/O 레이턴시 단축 및 대규모 IOPS 확보 |

#### 한줄 요약
- 실무에서는 LACP로 NAS 대역폭을 늘리고, MPIO로 SAN 경로를 이중화하며, Zoning/LUN Masking으로 보안을 격리한다.

## Ⅶ. 결론

- 엔터프라이즈 환경에서 로컬 초저지연은 **DAS(NVMe)**, 비정형 협업 공유는 **NAS(NFS/SMB)**, 미션 크리티컬 DB/가상화는 FC-**SAN**이 표준으로 안착되었으며, 최근 대규모 AI/빅데이터 인프라에서는 RDMA 기반 초고속 패브릭인 **NVMe-oF**(RoCEv2) 및 분산 객체 스토리지(Ceph, MinIO)로 융합 진화

#### 한줄 요약
- 스토리지 아키텍처는 워크로드의 I/O 특성(파일 vs 블록)과 성능 요구에 따라 DAS, NAS, SAN을 최적 배치하여 완성된다.
