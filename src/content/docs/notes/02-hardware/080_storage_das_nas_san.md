---
sidebar:
  order: 80
  label: "080. 스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
date: "2026-08-08T20:11:00+09:00"
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

<details><summary>핵심 용어</summary>

- **DAS(Direct Attached Storage)**: 서버에 HBA 전용 케이블(SATA/SAS/NVMe)을 통하여 직접 물리 결합하는 블록 스토리지.
- **NAS(Network Attached Storage)**: 표준 Ethernet IP 네트워크 기반으로 파일 서버(NFS/SMB)가 파일 레벨 입출력을 서빙하는 네트워크 스토리지.
- **SAN(Storage Area Network)**: 전용 Fibre Channel(FC) 또는 iSCSI 고속 패브릭망을 구축하여 블록(LBA) 레벨 입출력을 서빙하는 전용 스토리지 네트워크.

</details>

- 정의/개념: 서버 입출력 데이터 형태(Block vs File) 및 전송 패브릭 매체에 따른 대표적 3대 혜택 저장 연결 아키텍처인 **DAS·NAS·SAN**
- 배경/필요성: 단일 호스트 기반 저장 용량 확장 한계 해소 및 기업 데이터 공유, 중앙 집중 관리, 고가용성 고속 데이터 트랜잭션 요구성

#### 한줄 요약

- I/O 단위와 공유 범위 및 전송 경로에 따라 DAS, NAS 또는 SAN을 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **블록 레벨 I/O(Block-Level I/O)**: 논리 블록 주소(LBA) 기반으로 호스트 파일시스템이 직접 블록을 억세스하는 방식 (DAS, SAN).
- **파일 레벨 I/O(File-Level I/O)**: 파일 경로 및 오프셋 기반으로 스토리지 내 캡슐화된 파일시스템을 억세스하는 방식 (NAS).
- **NFS/SMB**: NAS 환경에서 UNIX/Linux(NFS) 및 Windows(SMB/CIFS) 시스템이 네트워크 상에서 파일 공유를 수행하는 파일 전송 프로토콜.
- **FC/iSCSI**: SAN 환경에서 광케이블 패브릭(FC) 또는 Ethernet TCP/IP(iSCSI) 상에 SCSI 명령어를 인코딩하여 전송하는 블록 프로토콜.

</details>

- 서버 호스트가 직접 파일시스템을 제어하는 **블록 레벨 I/O** (DAS, SAN) 및 **LBA** 접근
- 스토리지 장비가 자체 파일시스템(NFS/SMB)을 보유 관리하는 **파일 레벨 I/O** (NAS)
- FC Switched Fabric 패브릭망을 통한 고가용성 및 무중단 **Multipathing** (SAN)

#### 한줄 요약

- 파일시스템 위치에 따른 블록•파일 I/O 경계를 구분한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **HBA(Host Bus Adapter)**: 서버 호스트 슬롯 상에서 FC/SAS 인터페이스를 물리 제어하는 전용 어댑터 카드.
- **FC Switch**: SAN 전용 광 인터커넥트 패브릭을 형성하고 Zoning 및 LUN Masking을 수행하는 스위치.
- **LUN(Logical Unit Number)**: SAN 스토리지 어레이에서 논리적으로 분할하여 서버 호스트에 볼륨으로 할당하는 블록 영역.

</details>

```text
[호스트•클라이언트]
          |
[파일•블록 접근 계층]
          |
[직결•네트워크 경로]
          |
   [저장장치•배열]
```

선의 의미: 호스트/클라이언트 요청이 파일/블록 접근 계층을 거쳐 DAS, NAS, SAN 전송 경로 및 물리 저장장치 어레이로 전달되는 인터페이스.

| 구성요소 | 책임 |
|:---|:---|
| 호스트•클라이언트 | 파일 오프셋 및 **LBA** 블록 요청 트랜잭션 능동 발행 |
| 파일•블록 접근 계층 | **NFS/SMB** 파일 서비스 해독 및 **SCSI/NVMe** 블록 커맨드 인코딩 |
| 직결•네트워크 경로 | SAS 케이블(DAS), IP Ethernet(NAS), **FC/iSCSI** 전용 패브릭(SAN) 전송 |
| 저장장치•배열 | RAID 어레이, **LUN** 볼륨 생성 및 물리 드라이브 암호화/저장 |

#### 한줄 요약

- 호스트·클라이언트·파일·블록 접근 계층·직결·네트워크 경로·저장장치·배열을 계층적으로 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **LUN Masking**: 특정 서버 호스트(HBA WWN 수치)에게만 허용된 **LUN** 볼륨을 억세스하게 제한하는 보안 설정.
- **Zoning**: FC 스위치 상에서 물리/논리적으로 포트 그룹을 분리하여 무단 억세스를 차단하는 SAN 네트워크 보안.

</details>

```text
[저장 I/O 요구]
       │
       ▼
1. I/O 단위 판정
   ┌───┴────────────┐
   │ 파일           │ 블록
   ▼                ▼
 [NAS]       2. 서버 공유 범위 판정
                    ┌──┴───────┐
                    │ 단일     │ 다중
                    ▼          ▼
                  [DAS]      [SAN]
                    └────┬─────┘
                         ▼
3. 성능•가용성 검증
                         │
                         ▼
                 [연결 구조 확정]
```

### 동작 원리

1. **I/O 단위 판정**: 데이터 서비스 단위가 파일(File)인지 블록(Block/LBA)인지 1차 판정.
2. **서버 공유 범위 판정**: 블록 단위 시 단일 전용 서버 억세스(**DAS**)인지 다중 서버 네트워크 공유(**SAN**)인지 판정.
3. **성능·가용성 검증**: 대역폭, 지연시간, **Multipathing**, **Zoning** 및 **LUN Masking** 보안 검증 후 토폴로지 최종 확정.

#### 한줄 요약

- 파일시스템의 관리 위치와 서버 공유 범위로 DAS, NAS, SAN을 결정하고 성능•가용성을 검증한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Multipathing**: 서버와 SAN 스토리지 간 다중 경로(Dual HBA, Dual FC Switch)를 구성하여 포트 장애 시 무중단 페일오버를 달성하는 기법.

</details>

| 비교 항목 | DAS (Direct Attached) | NAS (Network Attached) | SAN (Storage Area Network) |
|:---|:---|:---|:---|
| Access 단위 | Block-Level (**LBA**) | File-Level (File Offset) | Block-Level (**LBA**) |
| 전송 프로토콜 | SAS, SATA, PCIe/NVMe | **NFS**, **SMB/CIFS** (TCP/IP) | **Fibre Channel (FC)**, **iSCSI** |
| 파일시스템 위치 | 서버 호스트 상에 직접 탑재 | NAS 장비 내부에 캡슐화 탑재 | 서버 호스트 상에 직접 탑재 |
| 주요 용도 | 단일 서버, OS 부팅 드라이브 | 이종 OS 간 파일 공유, NAS 렌더팜 | RDBMS 대용량 DB, 가상화(VMware) |
| 주요 장단점 | 최단 지연시간 / 공유 불가 | 공유 용이 / IP 망 병목 발생 | 초고속 고가용성 / 고비용 및 복잡성 |

#### 한줄 요약

- 단일 서버 전용 블록에는 DAS, 공유 파일에는 NAS, 중앙 원격 블록에는 SAN이 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NVMe-oF(NVMe over Fabrics)**: 기존 FC/iSCSI SAN의 한계를 극복하고 RDMA(RoCEv2) 망 상에서 NVMe 블록 전송을 지연 없이 서빙하는 초고속 SAN 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NAS IP 공유망 트래픽 폭증으로 인한 네트워크 병목 | 10GbE/40GbE 전용 LACP 트렁킹 및 10GbE NAS 적용 | 파일 전송 대역폭 확충 |
| SAN 단일 광선로 물리 절단 시 서비스 중단 위험 | MPIO(**Multipathing**) 이중화 광 패브릭망 구축 | 무중단 스토리징 보장 |
| SAN 패브릭 상의 미인가 호스트 타 타깃 볼륨 침범 | **Zoning** 및 **LUN Masking** 적용 | 보안 볼륨 데이터 격리 |

> 사례: **SAN** 전용 FC 스위치 및 **NVMe-oF** 패브릭 구축을 통한 실시간 초고속 DB 인프라 완성

#### 한줄 요약

- 요구하는 공유 범위와 I/O 단위 및 장애 경로에 맞춰 스토리지 연결과 접근 통제를 설계한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스토리지 선택 기준(Storage Architecture Selection Criteria)**: 데이터 억세스 단위(Block vs File), 성능/지연시간 목표, 공유 범위 및 TCO에 기반한 체계.

</details>

- **스토리지 선택 기준**에 따라 단일 서버는 **DAS**, 파일 공유는 **NAS**, 대용량 고성능 DB/가상화는 **SAN** 채택

#### 한줄 요약

- I/O 액세스 단위(Block vs File) 및 서버 공유 범위에 맞춘 DAS/NAS/SAN 차등 채택 및 최적 스토리지 인프라 구축 체계 적용.
