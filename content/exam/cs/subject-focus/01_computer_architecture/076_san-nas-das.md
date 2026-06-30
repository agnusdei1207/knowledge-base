---
title: "SAN·NAS·DAS (Storage Area Network / Network Attached Storage / Direct Attached Storage)"
date: "2026-06-30"
weight: 76
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> DAS(Direct Attached Storage)는 서버 직접연결, NAS(Network Attached Storage)는 파일 단위 네트워크 공유, SAN(Storage Area Network)은 블록 단위 전용 스토리지 네트워크를 제공하는 스토리지 연결 방식이다.

## Ⅱ. 구성요소 / 원리
- DAS: SCSI/SAS/SATA로 서버에 직결, 서버 종속
- NAS: 이더넷+파일 프로토콜(NFS/CIFS/SMB), 파일 레벨 접근
- SAN: FC(Fibre Channel)/iSCSI, 블록 레벨 접근, 전용망
- 접근 단위: DAS·SAN=블록(Block), NAS=파일(File)

## Ⅲ. 흐름도 / 구조
```text
DAS: [Server]──직결──[Storage]
NAS: [Client]──LAN(NFS/SMB)──[NAS Filer]
SAN: [Server]──FC/iSCSI 전용망──[Storage Array]
```

## Ⅳ. 핵심 특징
| 구분 | DAS | NAS | SAN |
|:---|:---|:---|:---|
| 단위 | 블록 | 파일 | 블록 |
| 연결 | 직결 | LAN | 전용 SAN망 |
| 장점 | 단순·저가·고속 | 공유·관리 용이 | 고성능·확장성 |
| 한계 | 공유 불가 | LAN 부하·지연 | 고비용·복잡 |

## Ⅴ. 기술사적 적용
- 소규모는 DAS·NAS, 미션크리티컬 DB는 SAN 적용
- NVMe-oF로 SAN 저지연화, 유니파이드 스토리지로 NAS+SAN 통합
- 클라우드 환경은 오브젝트 스토리지(S3)로 확장
