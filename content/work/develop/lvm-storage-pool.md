---
title: "🗄️ Ubuntu LVM — 외장 하드 여러 개를 하나의 스토리지 풀로 묶기"
tags:
  - "work"
  - "lvm"
  - "ubuntu"
  - "storage"
  - "operations"
---


> 우분투에서 외장 하드 2~N개를 **LVM(Logical Volume Manager, 논리 볼륨 관리자)**으로 묶어
> 하나의 거대한 스토리지 풀처럼 쓰고, 나중에 디스크를 더 사서 **무중단 수평 확장**하는 전 과정을 정리한 운영 가이드.

---

## 🧭 이 글이 답하는 질문

- 외장 하드 3개를 사서 "한 폴더에 통으로" 12TB처럼 쓰고 싶다.
- 나중에 하드를 더 사면, 데이터 옮기지 않고 용량만 늘리고 싶다.
- 디스크 한 개가 죽으면 RAID-1처럼 거울로 보호받고 싶진 않은데, **그래도 한 풀로 합쳐서 편하게** 쓰고 싶다.

-> 정답은 **LVM**이다. RAID와는 다른 "공간 추상화" 도구다.

---

## 🧠 0단계. 원리부터 — LVM이 뭔데?

LVM을 한 줄로 요약하면:

> **"디스크를 직접 다루지 않고, 디스크들을 합친 가상 공간(풀)에서 잘라 쓰는 공간 관리자"**

### 0-1. RAID와 LVM은 다르다

| | RAID (예: mdadm, LVM RAID) | **LVM (공간 관리)** |
|---|---|---|
| 목적 | **신뢰성** (디스크 1개 죽어도 데이터 살림) | **유연성** (디스크 N개를 한 풀처럼) |
| 디스크 N개 묶기 | 미러링·스트라이핑이 자동 | 그냥 합쳐서 큰 풀 |
| 용량 확장 | 동일 크기 디스크로만 교체 가능 | **다른 크기 디스크도 섞어 추가 가능** |
| 중첩 가능 여부 | RAID 위에 LVM 올릴 수 있음 | LVM 위에 RAID 올릴 수 있음 |

이번 가이드는 **LVM만** 사용한다. (RAID 미러링·장애복구는 별도 가이드에서 다룬다.)

### 0-2. LVM 3계층 구조 — PV / VG / LV

LVM은 **물리 -> 그룹 -> 논리** 3계층을 거친다. 약어는 외우면 편하다.

```
+----------------------------------------------------------+
|  LV (Logical Volume, 논리 볼륨)                           |  <- 우리가 실제로 포맷·마운트하는 "가상 디스크"
|      +- /dev/media_pool/media_disk (4TB)                  |
+----------------------------------------------------------+
|  VG (Volume Group, 볼륨 그룹)                              |  <- 여러 PV를 합친 "하나의 거대한 풀"
|      +- media_pool (총 4TB)                               |
+----------------------------------------------------------+
|  PV (Physical Volume, 물리 볼륨)                           |  <- 실제 디스크(또는 디스크의 파티션)
|      +- /dev/sdb (2TB)                                    |
|      +- /dev/sdc (2TB)                                    |
+----------------------------------------------------------+
```

| 약어 | 풀네임 | 비유 | 비고 |
|---|---|---|---|
| **PV** | **P**hysical **V**olume | 진흙 덩어리 | 실제 디스크 또는 그 위의 파티션. `pvcreate`로 표시. |
| **VG** | **V**olume **G**roup | 커다란 화분 | PV 여러 개를 합친 단일 풀. `vgcreate`로 생성. |
| **LV** | **L**ogical **V**olume | 화분에서 잘라낸 분재 | VG에서 잘라낸 "포맷 가능한 가상 디스크". `lvcreate`로 생성. |
| **PE** | **P**hysical **E**xtent | 진흙의 최소 단위 | LVM이 내부적으로 디스크를 자르는 기본 블록(보통 4MiB). 신경 안 써도 됨. |
| **LE** | **L**ogical **E**xtent | 분재의 최소 단위 | LV의 최소 단위. PE와 1:1로 매핑됨. |

### 0-3. 왜 좋은가 — LVM의 3대 장점

1. **확장이 쉽다** — 새 디스크를 꽂고 3줄이면 풀이 커진다. 데이터를 옮길 필요 없음.
2. **디스크 크기가 달라도 된다** — 2TB + 4TB + 500GB 섞어 묶어도 OK. RAID-5/6는 동일 크기 요구.
3. **스냅샷** — LV 단위로 "지금 상태 그대로"를 동결해서 백업/실험에 쓸 수 있다. (`lvcreate --snapshot`)

### 0-4. 단점도 알아두자

- 단일 디스크 장애가 VG 전체로 번진다. (RAID 미러링이 아니므로)
- 다른 OS(Windows 등)에서 바로 읽기 어렵다. (LVM 메타데이터를 모르는 OS)
- USB로 빼서 다른 리눅스에 꽂으면 VG/LV가 **자동 인식 안 될 수 있다**. `vgscan` -> `vgchange -ay` 필요.

-> **"여러 디스크를 한 풀처럼 편하게"가 목적**, **"장애 대비"는 별도 백업으로 해결**하는 게 일반적인 워크플로.

---

## 🛠️ 1~7단계. 실전 — 외장 하드 2개를 묶는 최소 시나리오

> **시나리오 가정**
> - 본체 디스크: `/dev/sda` (건드리면 안 됨)
> - 외장 하드 1: `/dev/sdb` (2TB, 비어있음)
> - 외장 하드 2: `/dev/sdc` (2TB, 비어있음)
> - 마운트 포인트: `/media/storage` (4TB 통으로 쓸 폴더)
>
> 본인 환경에 따라 장치명만 바꿔서 그대로 따라치면 된다.

---

### 1단계. 사전 확인 — 디스크 이름 찍어보기

무엇을 건드릴지 **반드시 확인**한다. 외장 하드를 다른 이름으로 착각하면 본체 디스크가 날아간다.

```bash
lsblk
```

출력 예시:

```
sda      8:0    0   500G  0 disk
+-sda1   8:1    0   500G  0 part /
sdb      8:16   0     2T  0 disk          <- 외장 1 (비어있음)
sdc      8:32   0     2T  0 disk          <- 외장 2 (비어있음)
```

> ⚠️ `sda`가 본체라면 절대 `pvcreate`하지 말 것. 확인했으면 다음 단계로.

---

### 2단계. LVM 패키지 설치

LVM 도구(`lvm2`)가 설치돼 있는지 확인하고, 없으면 설치한다.

```bash
sudo apt update
sudo apt install lvm2 -y
```

> **왜 필요한가?** 우분투 기본 설치에서는 `lvm2`가 들어있지 않을 수 있다. `pvcreate` 같은 명령어는 이 패키지에 들어있다.

설치 확인:

```bash
which pvcreate vgcreate lvcreate
```

세 명령어 모두 경로가 나오면 OK.

---

### 3단계. PV(물리 볼륨) 생성 — 디스크를 "LVM 재료"로 표시

```bash
sudo pvcreate /dev/sdb /dev/sdc
```

**성공 메시지:**

```
Physical volume "/dev/sdb" successfully created.
Physical volume "/dev/sdc" successfully created.
```

> **원리**: `pvcreate`는 디스크의 첫 부분에 **LVM 메타데이터 헤더**(PVMeta 데이터)를 쓴다. 이게 있어야 LVM이 "아, 이 디스크는 내가 관리하는 PV구나" 라고 인식한다. 디스크 내용을 **지우지는 않지만**, 기존 파티션 테이블은 덮어쓰기 때문에 **반드시 빈 디스크여야** 한다.

확인:

```bash
sudo pvs
# 또는 더 자세히
sudo pvdisplay
```

---

### 4단계. VG(볼륨 그룹) 생성 — 두 디스크를 "하나의 풀"로 합치기

```bash
sudo vgcreate media_pool /dev/sdb /dev/sdc
```

**성공 메시지:**

```
Volume group "media_pool" successfully created
```

> **원리**: VG는 "PE(Physical Extent)라는 동일한 크기 블록의 배열"이다. 디스크 2개의 PE가 하나의 연속된 배열로 합쳐진다. `media_pool`은 우리가 지은 이름 — 마음대로 바꿔도 된다.
>
> 비유로 다시 말하면: 화분(`media_pool`)이 하나 생겼고, 그 안에 진흙(`PV` 두 개)이 4TB 분량 들어있는 상태다.

확인:

```bash
sudo vgs
# VG         #PV #SN #VSize   VFree
# media_pool   2   0   3.99T  3.99T
```

`VSize`가 4TB 근처로 나오면 정상.

---

### 5단계. LV(논리 볼륨) 생성 — 풀에서 "실제 쓸 가상 디스크" 잘라내기

```bash
sudo lvcreate -l 100%FREE -n media_disk media_pool
```

옵션 의미:
- `-l 100%FREE` -> VG의 **남은 PE 100%**를 다 쓰겠다.
- `-n media_disk` -> 새로 만들 LV의 이름.
- `media_pool` -> 어떤 VG에서 잘라낼지.

**성공 메시지:**

```
Logical volume "media_disk" created.
```

> **원리**: LV는 VG의 PE를 가리키는 매핑표일 뿐이다. 실제 데이터는 PV(디스크) 위에 그대로 있다. 그래서 나중에 새 디스크를 VG에 추가하면, 새 PE가 LV에 자동으로 추가된다 — **데이터를 옮기지 않아도** LV가 커진다.

확인:

```bash
sudo lvs
# LV         VG         Attr       LSize
# media_disk media_pool -wi-a----- 3.99T
```

이제 `/dev/media_pool/media_disk` 라는 **4TB짜리 단일 가상 디스크**가 생겼다.

---

### 6단계. 파일 시스템 포맷 — ext4로 포맷

가상 디스크를 실제로 사용하려면 파일 시스템을 씌워야 한다.

```bash
sudo mkfs.ext4 /dev/media_pool/media_disk
```

> **왜 ext4인가?**
> - 리눅스 네이티브 — 별도 드라이버 설치 불필요.
> - **온라인 리사이즈(`resize2fs`)**가 안정적으로 동작.
> - Git clone 같은 메타데이터 권한이 명확.
> - (대안: XFS — 대용량·고성능에 강하지만 리사이즈가 약간 까다로움)

확인:

```bash
sudo blkid /dev/media_pool/media_disk
# /dev/media_pool/media_disk: UUID="xxxx-xxxx" TYPE="ext4"
```

---

### 7단계. 마운트 + 자동 마운트 설정

#### 7-1. 마운트할 폴더 만들기 & 즉시 마운트

```bash
sudo mkdir -p /media/storage
sudo mount /dev/media_pool/media_disk /media/storage
df -h /media/storage
# Filesystem                          Size  Used Avail Use% Mounted on
# /dev/mapper/media_pool-media_disk   3.9T  ...   ...   ..  /media/storage
```

#### 7-2. 권한 풀기 (협업·Git 클론용)

```bash
sudo chmod 777 /media/storage
```

> 본인 단독 사용이라면 `chown $USER:$USER`가 더 안전. 공유·다중 사용자 환경이면 777이 단순하다.

#### 7-3. 재부팅 후에도 자동 마운트 (`/etc/fstab` 등록)

이걸 안 하면 **재부팅할 때마다 수동으로 `mount`해야** 한다.

먼저 LV의 **UUID**를 확인한다. (장치명 `/dev/...`은 부팅 순서가 바뀌면 깨질 수 있어 UUID가 안전)

```bash
sudo blkid /dev/media_pool/media_disk
```

출력된 `UUID="..."` 값을 복사한 뒤:

```bash
sudo nano /etc/fstab
```

파일 맨 아래에 다음 한 줄을 추가하고 저장(`Ctrl+O` -> `Enter` -> 종료 `Ctrl+X`):

```
# LVM media_pool/media_disk -> /media/storage
UUID=여기에-복사한-UUID  /media/storage  ext4  defaults  0  2
```

> **fstab 필드 설명** (왼쪽부터):
> 1. 장치 식별자 (UUID 권장)
> 2. 마운트 포인트
> 3. 파일 시스템 타입 (`ext4`)
> 4. 마운트 옵션 (`defaults` = 기본값 묶음)
> 5. 덤프 여부 (`0` = 안 함)
> 6. fsck 검사 순서 (`2` = root 다음 우선순위)

재부팅하지 않고 즉시 검증:

```bash
sudo umount /media/storage
sudo mount -a
df -h /media/storage
```

에러 없이 마운트되고 용량이 보이면 성공.

---

## 📈 확장 시나리오 — 나중에 디스크를 더 사면?

**상황**: `media_pool`이 4TB인데 2TB짜리 외장(`/dev/sdd`)를 새로 샀다. 데이터를 옮기지 않고 풀을 6TB로 키우고 싶다.

### 3줄로 끝난다

```bash
# 1. 새 디스크를 PV로 표시
sudo pvcreate /dev/sdd

# 2. 기존 VG(media_pool)에 새 PV 합치기
sudo vgextend media_pool /dev/sdd

# 3. LV에 새 PE를 할당하고 파일 시스템도 온라인으로 키우기
sudo lvextend -l +100%FREE /dev/media_pool/media_disk
sudo resize2fs /dev/media_pool/media_disk
```

> **왜 `lvextend` + `resize2fs` 둘 다?**
> - `lvextend` -> LV(LVM 레벨) 의 크기를 키운다.
> - `resize2fs` -> 그 안의 **파일 시스템**(ext4)도 함께 키운다.
> 둘 다 해야 OS가 "디스크가 커졌다"고 인식한다. `resize2fs`는 **마운트 상태에서**도 동작 — **무중단 확장** 가능.

확인:

```bash
df -h /media/storage
# Size가 3.9T -> 5.9T 로 바뀌었을 것
```

### 디스크가 여러 개 한꺼번에 추가된다면?

```bash
sudo pvcreate /dev/sdd /dev/sde /dev/sdf
sudo vgextend media_pool /dev/sdd /dev/sde /dev/sdf
sudo lvextend -l +100%FREE /dev/media_pool/media_disk
sudo resize2fs /dev/media_pool/media_disk
```

각각 **공백으로 여러 개** 지정할 수 있다. 명령어 자체는 동일.

---

## 🩹 트러블슈팅 — 자주 만나는 에러

### `Cannot use /dev/sdb: device is partitioned`

PV로 쓸 디스크에 **기존 파티션**이 남아 있을 때 발생.

해결:

```bash
# 1) 파티션이 진짜 비어있는지 확인 (필수)
sudo fdisk -l /dev/sdb

# 2) 비어있다면, 파티션 테이블을 통째로 지움
sudo dd if=/dev/zero of=/dev/sdb bs=1M count=10
# 또는
sudo wipefs -a /dev/sdb

# 3) 다시 pvcreate
sudo pvcreate /dev/sdb
```

> ⚠️ `dd`나 `wipefs`는 **디스크의 모든 데이터를 지운다**. 절대 본체 디스크(`sda`)에 하지 말 것.

### `Can't open /dev/sdb exclusively. Mounted filesystem?`

디스크가 이미 어디에 마운트돼 있을 때.

해결:

```bash
# 어디에 마운트돼 있는지 확인
mount | grep sdb
# 또는
lsblk /dev/sdb

# 마운트 해제
sudo umount /dev/sdb
```

### `Volume group "media_pool" not found`

다른 OS에서 디스크를 꽂았거나, 시스템 재시작 후 VG가 **비활성화**된 상태일 수 있다.

해결:

```bash
sudo vgscan           # VG 메타데이터 다시 스캔
sudo vgchange -ay media_pool   # 활성화
```

### `resize2fs: Bad magic number in super-block`

파일 시스템이 ext4가 아닐 때 (혹은 LV와 FS가 매칭 안 될 때).

해결:

```bash
# 파일 시스템 종류 재확인
sudo blkid /dev/media_pool/media_disk

# XFS 였다면 resize2fs 대신
sudo xfs_growfs /media/storage
```

---

## 📋 한눈에 보는 명령어 요약

| 시점 | 명령어 | 하는 일 |
|---|---|---|
| 시작 | `lsblk` | 디스크 식별 |
| 시작 | `sudo apt install lvm2` | LVM 도구 설치 |
| 초기 구축 | `sudo pvcreate /dev/sdX` | 디스크를 PV로 표시 |
| 초기 구축 | `sudo vgcreate media_pool /dev/sdX ...` | PV들을 풀(VG)로 합치기 |
| 초기 구축 | `sudo lvcreate -l 100%FREE -n media_disk media_pool` | 풀에서 LV 잘라내기 |
| 초기 구축 | `sudo mkfs.ext4 /dev/media_pool/media_disk` | ext4로 포맷 |
| 초기 구축 | `sudo mount /dev/media_pool/media_disk /media/storage` | 폴더에 연결 |
| 초기 구축 | `/etc/fstab`에 UUID 등록 | 재부팅 시 자동 마운트 |
| 확장 | `sudo pvcreate /dev/sdY` | 새 디스크 PV 등록 |
| 확장 | `sudo vgextend media_pool /dev/sdY` | 기존 VG에 추가 |
| 확장 | `sudo lvextend -l +100%FREE /dev/media_pool/media_disk` | LV 확장 |
| 확장 | `sudo resize2fs /dev/media_pool/media_disk` | 파일 시스템 확장 |
| 상태 확인 | `pvs` / `vgs` / `lvs` | 각각 PV/VG/LV 한 줄 요약 |
| 상태 확인 | `pvdisplay` / `vgdisplay` / `lvdisplay` | 각각 자세한 정보 |

---

## 🔗 관련 문서

- RAID와 차이: [RAID 0/1/5/6/10 정리](/studynote/01_computer_architecture/08_io_storage_systems/331_raid/)
- NAS / SAN / DAS 구분: [338. NAS](/studynote/01_computer_architecture/08_io_storage_systems/338_nas/)
- 파일 시스템 이해: ext4 · XFS · ZFS (별도 가이드에서 다루는 것을 권장)
- 운영 자동화 / Ansible로 위 일괄 적용: 별도 가이드
