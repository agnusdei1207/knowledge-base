---
sidebar:
  order: 20
  label: "020. 파일 시스템: FAT•NTFS•ext4•APFS (File System)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "파일 시스템: FAT•NTFS•ext4•APFS (File System)"
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 20
extra:
  question_no: "020"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "할당•메타데이터•장애 일관성 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **File System (파일 시스템)**: OS가 디스크(HDD/SSD/NVM) 블록 장치 상의 데이터를 파일 및 디렉터리 구조로 조직화, 저장, 검색, 권한 제어 및 장애 일관성을 관리하는 구조체.
- **VFS (Virtual File System)**: 복수의 이종 파일 시스템(ext4, NTFS, FAT, NFS 등)을 표준 POSIX System Call 인터페이스(open, read, write, close)로 추상화해 주는 OS 커널 추상화 레이어.

</details>

- 정의/개념: 저장 매체 블록에 파일 이름, 디렉터리, 메타데이터(Metadata) 및 블록 포인터를 구조화 매핑하여 데이터 관리 및 장애 일관성을 보장하는 **파일 시스템(File System)**
- 배경/필요성: raw 디스크 섹터 단위의 무작위 억세스 난해성 극복, OS별 파일 권한(ACL) 및 갑작스러운 전원 차단 시 파일 오염 복구(Journaling/COW) 요구성

#### 한줄 요약

- 이름•메타데이터•블록을 연결하는 파일 시스템이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Inode (Index Node)**: Linux/Unix 파일 시스템에서 파일 이름 제외한 권한(Mode), 소유자(UID/GID), 파일 크기, 시간 인스탬프 및 물리 블록 포인터를 보관하는 128B~256B 데이터 구조체.
- **MFT (Master File Table)**: Windows NTFS 파일 시스템에서 파일 및 디렉터리의 모든 속성, 메타데이터 및 Extent 블록 위치를 1KB 레코드 단위로 총괄 관리하는 데이터베이스.
- **COW (Copy-on-Write)**: 데이터 수정 시 기존 블록을 덮어쓰지 않고 신규 유휴 블록에 새로 기재 후 메타데이터 포인터만 스위칭하여 장애 일관성 및 무중단 스냅샷을 구현하는 기법.

</details>

- **VFS (Virtual File System)** 기반 이종 파일 시스템 커널 추상화
- 메타데이터 관리 방식의 차이 (**FAT Table vs Inode vs MFT vs B-Tree**)
- 장애 복구 일관성 메커니즘 (**Non-Journaling vs Journaling vs COW**)

#### 한줄 요약

- 블록 크기와 내부 단편화의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Extent**: 연속된 여러 물리 블록의 시작 번호와 길이(Length)만을 묶어서 관리함으로써 큰 파일의 메타데이터 크기와 디스크 탐색 오버헤드를 대폭 줄이는 할당 방식.

</details>

```text
            [애플리케이션]
                   |
        [가상 파일 시스템]
                   |
       [디렉터리•메타데이터]
                   |
          [블록 할당 관리자]
                   |
          [일관성 관리자]
```

선의 의미: VFS 레이어 아래로 각 OS 전용 파일 시스템 메타데이터 및 블록 할당자와 Journaling/COW 일관성 관리자가 파이프라인 형성 아키텍처.

| 구분 항목 | FAT32 / exFAT | NTFS | ext4 | APFS |
|:---|:---|:---|:---|:---|
| 운영체제 | 범용 임베디드, 이동식 | Windows | Linux | macOS, iOS |
| 메타데이터 | **FAT (Linked List)** | **MFT (Master File Table)** | **Inode (Extent Tree)** | **B-Tree (COW)** |
| 장애 복구 | 미지원 (chkdsk 필요) | **Journaling** (USN Journal) | **Journaling** (JBD2) | **Redirect-on-Write (COW)** |
| 단일 파일 제한 | FAT32: 4GB (exFAT: 16EB) | 16TB | 16TB | 8EB |
| 주요 기능 | 단순성, 임베디드 호환성 | ACL, EFS 암호화, VSS | Extent 할당, Fast fsck | Atomic Save, Space Sharing, Snapshot |

#### 한줄 요약

- 가상 파일 시스템, 블록 할당 관리자, 일관성 관리자가 파일 연산을 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **fsync()**: 메모리 페이지 캐시(Page Cache)에 딜레이되어 있는 변경 데이터를 실제 물리 블록 디스크까지 강제 조율 확정(Flush/Commit)하는 POSIX 시스템 콜.

</details>

```text
┌──────────────────────────────┐
│ 파일 경로•쓰기 데이터       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 경로•권한 확인           │
│ 2. 블록 할당                │
│ 3. 일관성 방식 선택         │
└───────┬──────────────────────┘
        ├─ 직접 갱신
        ├─ 저널링
        └─ 쓰기 시 복사
               │
               ▼
┌──────────────────────────────┐
│ 4. 데이터•복구 정보 기록    │
│ 5. 매핑•메타데이터 확정     │
└──────────────────────────────┘
```

### 동작 원리

1. **경로·권한 확인**: VFS 레이어를 통해 디렉터리 경로 트래버스 및 권한(ACL/Permission Bit) 검증.
2. **블록 할당**: 유휴 **Extent/Block** 할당 탐색 및 디스크 블록 할당.
3. **일관성 방식 선택**: 파일 시스템 타입에 따라 Journaling Log 기록 또는 COW 버퍼 할당.
4. **데이터·복구 정보 기록**: 물리 디스크에 파일 내용 수용 및 저널 블록 Write.
5. **매핑·메타데이터 확정**: Inode/MFT/B-Tree 포인터 **Commit** 갱신 완결.

#### 한줄 요약

- 데이터•복구 정보 기록 후 매핑•메타데이터 확정이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Space Sharing**: APFS 전용 기능으로, 동일 디스크 파티션 안에서 복수의 가상 볼륨이 물리 용량을 정적으로 나누지 않고 동적으로 공유하는 기술.

</details>

| 기능 비교 | Journaling File System (ext4/NTFS) | COW File System (APFS/ZFS/Btrfs) |
|:---|:---|:---|
| 데이터 덮어쓰기 | 기존 블록 위치에 직접 In-Place Overwrite | 신규 유휴 블록에 Write 후 포획 스위치 (**Out-of-Place**) |
| 스냅샷 성능 | Copy-on-Write 흉내로 느림 / 오버헤드 큼 | **즉각적 (Zero-Copy Instant Snapshot)** 생성 |
| 디스크 단편화 | 관리 우수 (Extent 연속 할당 유지) | COW 특성 상 조각화(Fragmentation) 증대 가능 |
| 무결성 검증 | 메타데이터만 체크섬 검증 | **데이터 + 메타데이터 전체 Checksum** 검증 (Self-Healing) |

#### 한줄 요약

- 이동식 호환은 FAT, 플랫폼 기능은 NTFS•ext4•APFS가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Dirty Page Flush**: OS 페이지 캐시(Page Cache)의 찌꺼기(Dirty) 데이터를 커널 백그라운드 스레드(flusher/pdflush)가 디스크로 주기적 동기화 기록하는 동작.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전원 누출 시 파일 메타데이터 붕괴 | **Journaling (data=ordered 또는 journal)** 모드 적용 | 시스템 무결성 보장 |
| SSD 매체에서 잦은 덮어쓰기로 인한 수명 단축 | **COW 기반 APFS/Btrfs** 및 **TRIM** 명령어 인가 | SSD 낸드 래치 수명 연장 |
| DB 엔진 구동 시 OS Page Cache 이중 버퍼링 | **O_DIRECT** 플래그 오픈 및 파일 시스템 버퍼링 바이패스 | DB 억세스 속도 극대화 |

> 사례: Linux **ext4 / XFS** 서버 튜닝 및 macOS **APFS Container** 동적 파티셔닝

#### 한줄 요약

- 내구성, 내부 단편화, 쓰기 증폭을 기준으로 정책을 검증한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **파일 시스템 선택 기준(File System Selection Criteria)**: 타깃 OS 호환성, 디바이스 매체(HDD/SSD/Flash), 장애 내구성 및 스냅샷 요구에 따른 수립 체계.

</details>

- **파일 시스템 선택 기준**에 따라 Linux 엔터프라이즈 서버는 **ext4/XFS**, Flash/Apple 장비는 **APFS**, 임베디드는 **exFAT** 채택

#### 한줄 요약

- 호환성•플랫폼•스냅샷 요구를 함께 평가하는 것이 핵심이다.
