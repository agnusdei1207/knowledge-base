---
sidebar:
  order: 80
  label: "080. 스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "스토리지 계층: DAS•NAS•SAN (Storage DAS NAS SAN)"
date: "2026-08-13T12:00:06+09:00"
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

- **DAS(Direct Attached Storage)**: 서버에 HBA 전용 케이블(SATA/SAS/NVMe)을 통하여 직접 물리 결합하는 블록 스토리지.
- **NAS(Network Attached Storage)**: 표준 Ethernet IP 네트워크 기반으로 파일 서버(NFS/SMB)가 파일 레벨 입출력을 서빙하는 네트워크 스토리지.
- **SAN(Storage Area Network)**: 전용 Fibre Channel(FC) 또는 iSCSI 고속 패브릭망을 구축하여 블록(LBA) 레벨 입출력을 서빙하는 전용 스토리지 네트워크.

</details>

- 정의/개념: I/O 단위와 공유 범위 및 전송 경로로 구분하는 **DAS·NAS·SAN** 저장 연결 구조
- 배경/필요성: 단일 호스트 기반 저장 용량 확장 한계 해소 및 기업 데이터 공유, 중앙 집중 관리, 고가용성 고속 데이터 트랜잭션 요구성

#### 한줄 요약

- I/O 단위와 공유 범위 및 전송 경로에 따라 DAS, NAS 또는 SAN을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **블록 레벨 I/O(Block-Level I/O)**: 논리 블록 주소 기반으로 호스트 파일시스템이 블록 장치에 접근하는 방식.
- **파일 레벨 I/O(File-Level I/O)**: 파일 경로와 오프셋으로 원격 파일시스템에 접근하는 방식.
- **NFS/SMB**: NAS 환경에서 UNIX/Linux(NFS) 및 Windows(SMB/CIFS) 시스템이 네트워크 상에서 파일 공유를 수행하는 파일 전송 프로토콜.
- **FC/iSCSI**: SAN 환경에서 광케이블 패브릭(FC) 또는 Ethernet TCP/IP(iSCSI) 상에 SCSI 명령어를 인코딩하여 전송하는 블록 프로토콜.

</details>

- 서버 호스트가 직접 파일시스템을 제어하는 **블록 레벨 I/O** (DAS, SAN) 및 **LBA** 접근
- 스토리지 장비가 자체 파일시스템(NFS/SMB)을 보유 관리하는 **파일 레벨 I/O** (NAS)
- FC·iSCSI 패브릭의 경로 장애에 대비하는 **Multipathing** 구성

#### 한줄 요약

- 파일시스템 위치에 따른 블록•파일 I/O 경계를 구분한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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
| 직결•네트워크 경로 | **HBA** 직결, IP Ethernet, **FC Switch·iSCSI** 패브릭 전송 |
| 저장장치•배열 | RAID 어레이, **LUN** 볼륨 생성 및 물리 드라이브 암호화/저장 |

#### 한줄 요약

- 호스트·클라이언트·파일·블록 접근 계층·직결·네트워크 경로·저장장치·배열을 계층적으로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LUN Masking**: 지정된 호스트 식별자에만 특정 **LUN** 접근을 허용하는 스토리지 설정.
- **Zoning**: FC 패브릭에서 통신 가능한 포트·WWN 집합을 제한하는 접근 통제.

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

<details><summary>용어 설명</summary>

- **Multipathing**: 서버와 SAN 사이에 복수 I/O 경로를 구성하고 장애 경로에서 대체 경로로 전환하는 기법.

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

<details><summary>용어 설명</summary>

- **NVMe-oF(NVMe over Fabrics)**: Ethernet·FC 등 패브릭을 통해 원격 NVMe 블록 접근을 제공하는 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NAS 공유망 트래픽 증가로 인한 네트워크 병목 | 전용 VLAN·링크 집성 및 NIC 대역폭 확장 | 파일 전송 대역폭 확충 |
| SAN 단일 경로 단절 시 서비스 중단 위험 | MPIO(**Multipathing**)와 이중 패브릭 구성 | 단일 경로 장애 시 대체 경로 제공 |
| SAN 패브릭 상의 미인가 호스트 타 타깃 볼륨 침범 | **Zoning** 및 **LUN Masking** 적용 | 보안 볼륨 데이터 격리 |

> 사례: SAN 경로 장애 주입으로 MPIO 전환과 응용 I/O 영향을 검증

#### 한줄 요약

- 요구하는 공유 범위와 I/O 단위 및 장애 경로에 맞춰 스토리지 연결과 접근 통제를 설계한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **스토리지 선택 기준(Storage Architecture Selection Criteria)**: 데이터 억세스 단위(Block vs File), 성능/지연시간 목표, 공유 범위 및 TCO에 기반한 체계.

</details>

- **스토리지 선택 기준**에 따라 단일 서버는 **DAS**, 파일 공유는 **NAS**, 대용량 고성능 DB/가상화는 **SAN** 채택

#### 한줄 요약

- 단일 블록은 DAS, 공유 파일은 NAS, 중앙 원격 블록은 SAN을 선택한다.
