---
title: "파일 시스템 — FAT·NTFS·ext4·APFS (File System)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 22
---

# 📖 【암기용】 개념 완전 이해

> 목적: 파일 시스템을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 저장장치의 블록을 파일·디렉터리·권한·메타데이터로 조직하는 OS 계층
- **왜 필요한가**: 디스크와 SSD는 블록 주소만 제공한다. 사용자는 이름, 폴더, 접근권한, 수정시간, 스냅샷 같은 논리 단위가 필요하다.
- **핵심 직관**: 파일 시스템은 창고의 선반 번호를 사람이 읽는 물품명·위치표·출입권한으로 바꾸는 장부이다.

## 깊이 이해
- **배경·문제의식**: 저장장치는 4KB 블록 단위 읽기·쓰기를 제공하지만 애플리케이션은 파일 단위 저장을 요구한다. 파일 시스템은 블록 할당, 이름 해석, 권한 검사, 장애 후 복구를 담당한다.
- **작동 원리**: 디렉터리 엔트리가 파일명을 inode 또는 MFT 레코드에 연결하고, 메타데이터가 크기·권한·시간·블록 위치를 가진다. 파일 쓰기는 page cache에 들어간 뒤 block allocator와 I/O scheduler를 거쳐 저장장치에 반영된다.
- **비유**: 파일명은 책 제목, 디렉터리는 서가, inode는 도서 관리 카드, 데이터 블록은 책 페이지에 해당한다.
- **구체 예시**: ext4는 extent 기반 할당과 journaling을 사용하고, NTFS는 MFT와 ACL, APFS는 copy-on-write와 snapshot을 제공한다. FAT는 단순 구조로 USB 호환성은 넓지만 권한·저널링 기능이 제한된다.
- **흔한 오해·주의점**: "삭제"는 데이터 블록을 즉시 지우는 동작이 아니라 메타데이터 연결을 끊는 동작일 수 있다. 보안 삭제는 overwrite 또는 암호키 폐기가 필요하다.

## 연결 개념
- 파일 시스템 저널링 — 장애 시 메타데이터 일관성 보장
- 페이지 캐시 — 파일 I/O 지연과 쓰기 순서에 영향
- 권한 모델 — UNIX mode bit, ACL, capability 기반 접근통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 파일 시스템은 종류 암기가 아니라 메타데이터 구조, 할당 방식, 일관성, 권한, 스냅샷 기능을 비교해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파일 시스템은 블록 저장장치를 파일·디렉터리·메타데이터·권한의 논리 구조로 추상화하는 OS 저장 계층이다.
> 2. **가치**: 이름 기반 접근, 공간 할당, 장애 복구, 접근통제, 스냅샷을 제공해 애플리케이션의 저장 복잡도를 낮춘다.
> 3. **판단 포인트**: FAT·NTFS·ext4·APFS는 메타데이터, 저널링/COW, 권한, 스냅샷, 호환성 기준으로 구분한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OS 저장 구조 이해 확인 | inode/MFT, directory entry, block allocation | 파일명과 실제 데이터 위치 연결 누락 |
| 파일 시스템 비교 역량 확인 | FAT, NTFS, ext4, APFS의 권한·복구·스냅샷 차이 | 단순 OS별 파일 시스템 이름 나열 |
| 실무 운영 판단 확인 | journaling, snapshot, permission, fragmentation | SSD와 HDD 특성 차이 미반영 |

> 요약: 이 문제는 저장장치 블록을 파일 논리 구조로 바꾸는 계층과 파일 시스템별 선택 기준을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 파일 시스템은 블록을 파일로 추상화하는 계층이다.
- 배경: 저장장치는 block address를 제공하지만 사용자와 애플리케이션은 파일명, 디렉터리, 권한, 수정시간으로 데이터를 다룬다.
- 필요성: 파일 시스템은 fsync p95, fsck 오류 0건, ACL 예외 0건 기준으로 공간 할당·메타데이터·복구·접근통제를 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> VFS -> File System Driver -> Block Layer -> Disk / SSD
  / Metadata: inode / MFT / catalog
  / Data: block / extent / cluster
  / Control: permission / journal / snapshot
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| VFS | 파일 시스템 공통 인터페이스 제공 | Linux open/read/write 추상화 |
| 메타데이터 | 파일 크기·권한·시간·블록 위치 저장 | inode, MFT, APFS catalog |
| 할당 관리자 | 빈 블록을 파일 데이터에 연결 | bitmap, FAT chain, extent |
| 복구 기능 | 장애 후 일관성 회복 | journaling, copy-on-write |
| 권한 모델 | 사용자·그룹·프로세스 접근 제어 | mode bit, ACL, encryption |

> 요약: 파일 시스템은 VFS 아래에서 메타데이터, 데이터 블록, 권한, 복구 기능을 묶어 파일 추상화를 제공한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
파일 요청 -> 경로 해석 -> 권한 검사 -> 메타데이터 조회
  -> 블록 할당 / 읽기 -> 페이지 캐시 반영 -> 저장장치 I/O
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 경로명을 디렉터리 엔트리로 순차 해석 | pathname lookup cache hit |
| 2 | inode/MFT에서 권한·크기·위치 확인 | ACL, mode bit |
| 3 | 읽기는 page cache 조회 후 miss 시 block I/O | cache hit ratio |
| 4 | 쓰기는 공간 할당 후 journal 또는 COW 기록 | fsync latency, write amplification |
| 5 | sync/flush로 저장장치 반영 | dirty page ratio |

> 요약: 파일 접근은 경로 해석, 권한 검사, 메타데이터 조회, 캐시·블록 I/O 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| FAT | 단순 cluster chain | 호환성 중심 | USB, SD 카드, 4GB 단일 파일 한계 |
| NTFS | Windows 기본 | MFT, ACL, journaling | 기업 PC 권한 관리 |
| ext4 | Linux 범용 | extent, journal, delayed allocation | 서버 inode·fsck 시간 고려 |
| APFS | macOS/iOS | copy-on-write, snapshot, encryption | SSD 최적화, snapshot 복구 |

> 요약: FAT는 호환성, NTFS는 ACL, ext4는 Linux 서버 범용성, APFS는 COW·스냅샷이 판단 축이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 블록 직접 관리 | VFS+메타데이터+할당 관리자 | OS 호환성과 복구 요구 |
| 비용/성능 | 단순 FAT chain | extent, delayed allocation, cache | random IOPS, fsync latency |
| 운영/위험 | 백업 중심 복구 | snapshot, journal, ACL | RPO 15분, 권한 감사 필요성 |

> 요약: 파일 시스템 선택은 OS 호환성보다 복구 시간, 권한 모델, 쓰기 지연 요구를 함께 판단해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메타데이터 손상 | 전원 장애 중 쓰기 중단 | journal, COW, UPS | fsck error 0건 |
| 권한 오설정 | ACL 상속·마운트 옵션 오류 | least privilege, auditd | 권한 예외 월 0건 |
| 공간 단편화 | 작은 파일·반복 삭제 | extent, trim, defrag 정책 | 평균 extent 수, free space 20% |

> 요약: 운영 리스크는 메타데이터 손상, 권한 오류, 단편화이며 복구 구조와 감사 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p95 read 10ms 이하, fsync 50ms 이하 | fio, iostat |
| 품질/복구 | fsck 오류 0건, snapshot RPO 15분 | boot log, backup report |
| 운영/보안 | ACL 예외 0건, 암호화 적용률 100% | auditd, MDM, mount option |

> 요약: 도입 효과는 I/O 지연, 복구 가능성, 권한 감사 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Linux 서버는 ext4 또는 XFS를 선택하고 `noatime`, journal mode, inode 수를 워크로드 파일 크기 분포에 맞춘다.
2. 사용자 단말은 NTFS/APFS의 ACL, 디스크 암호화, snapshot을 적용하고 복구 RPO 15분 기준을 둔다.
3. SSD 환경은 TRIM, 4KB 정렬, write amplification 지표를 점검하고 fsync 집중 워크로드는 별도 볼륨으로 분리한다.

**결론 (2줄):**
- 기술사 판단: 이동식 호환성은 FAT/exFAT, Windows 권한 관리는 NTFS, Linux 서버는 ext4/XFS, Apple SSD 환경은 APFS를 선택한다.
- 향후 방향: 파일 시스템은 COW, snapshot, 암호화, 무결성 검증을 기본 기능으로 통합하는 방향으로 진화한다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "파일 시스템을 설명하시오" | 경로 해석, 메타데이터, 블록 I/O 흐름 | FAT·NTFS·ext4·APFS 특징 |
| 요구사항 명시형 | "비교하시오", "선택 기준을 제시하시오" | 권한·복구·스냅샷 처리 흐름 | OS별 선택 기준, 리스크 대응 |

> 요약: 설명형은 파일 접근 흐름을, 비교형은 파일 시스템별 권한·복구·운영 기준을 중심으로 전환한다.
