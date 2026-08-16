---
sidebar:
  order: 92
  label: "092. RAID 컨트롤러•JBOD (RAID Controller and JBOD)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "RAID 컨트롤러•JBOD (RAID Controller and JBOD)"
date: "2026-08-13T12:21:04+09:00"
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

- **RAID Controller**: 하드웨어 가속 칩셋과 전원 보호 캐시(BBU/Flash)를 탑재하여 디스크 스트라이핑, 패리티 연산(RAID 5/6) 및 미러링을 온전 오프로드하는 전용 어댑터.
- **JBOD(Just a Bunch of Disks)**: 디스크들을 하드웨어 RAID 묶음이나 패리티 생성 없이 각각 개별 물리 블록 디바이스로 OS/SDS에 1:1 직결 패스스루 노출하는 방식.
- **SDS(Software Defined Storage)**: 하드웨어 RAID 대신 Ceph, vSAN, ZFS 등 상위 소프트웨어가 JBOD 디스크들을 소프트웨어 레벨에서 분산 복제/에레이저 코딩 관리하는 시스템.

</details>

- 정의/개념: 데이터 중복성 및 장애 복구 책임을 물리 하드웨어 어댑터(HW RAID)에 두는지, 상위 소프트웨어 레벨(SDS/JBOD)로 이관하는지에 따른 스토리지 토폴로지 비교인 **RAID 컨트롤러 vs JBOD**
- 배경/필요성: 단일 서버 하드웨어 내결함성 수용(HW RAID) 및 대규모 클라우드/HCI 인프라 상의 디바이스 1:1 제어 및 소프트웨어 분산 수용(JBOD) 요구성

#### 한줄 요약

- 보호•복구 책임 계층에 따라 RAID 또는 JBOD를 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **BBU/Flash Backup Unit**: 정전 시 RAID 쓰기 캐시를 배터리로 유지하거나 비휘발 매체에 보존하는 모듈.
- **HBA Passthrough Mode**: RAID 논리 볼륨을 만들지 않고 각 디스크를 OS에 직접 노출하는 컨트롤러 모드.
- **Rebuild Penalty**: RAID 5/6 디스크 고장 시 새로운 디스크로 교체 후 패리티 연산을 통해 데이터를 복원할 때 발생하는 심각한 I/O 지연 현상.

</details>

- 하드웨어 칩셋 상에서 패리티 연산 및 **BBU/Flash** 백업을 동반한 **Write-Back** 캐싱 제공 (RAID Controller)
- **HBA Passthrough Mode** 기반 각 물리 드라이브 S.M.A.R.T 텔레메트리 데이터의 상위 **SDS** 노출 (JBOD)
- 디스크 장애 시 하드웨어 자체 재구성(**Rebuild**) 수행(RAID) vs 소프트웨어 분산 재복제(JBOD/SDS)

#### 한줄 요약

- 전원 보호 쓰기 캐시의 성능 이득과 컨트롤러 장애 위험 및 JBOD 상태 노출 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RAID Engine (XOR/P+Q Engine)**: RAID 5/6 패리티 데이터 생성을 위해 hardware XOR 및 Reed-Solomon 연산을 전용 가속하는 컨트롤러 내 코어.
- **Passthrough Controller**: 디스크 어레이를 단일 LUN으로 묶지 않고 JBOD 1:1 원형 디바이스로 OS에 맵핑하는 패스스루 커넥터.

</details>

```text
                 [호스트]
                /       \
     [보호 쓰기 캐시]   [패스스루 컨트롤러]
              |               |
         [RAID 엔진]           |
                \             /
                  [물리 디스크]
```

선의 의미: 호스트가 RAID 엔진·보호 캐시를 통해 LUN에 접근하거나 패스스루로 개별 디스크에 접근하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 | LUN 블록 요청 인가 및 **SDS** 상의 소프트웨어 분산 복제 정책 실행 |
| 보호 쓰기 캐시 | **BBU/Flash** 모듈과 연동하여 정전 시에도 Write-Back 캐시 데이터 보존 |
| RAID Engine | 하드웨어 XOR/P+Q 패리티 연산, 스트라이핑 및 **Rebuild** 인가 |
| Passthrough Controller | 디스크를 논리 LUN으로 래칭하지 않고 **JBOD** 1:1 원시 디바이스로 노출 |
| 물리 디스크 | HDD, NVMe/SATA SSD 상에 데이터 블록 및 S.M.A.R.T 건강 상태 보관 |

#### 한줄 요약

- 보호 쓰기 캐시와 RAID 엔진 경로 및 패스스루 컨트롤러 경로의 책임을 분리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Back vs Write-Through**: 데이터를 캐시에만 써서 즉시 완료를 반환(Write-Back)할지, 물리 디스크 덤프까지 대기(Write-Through)할지 결정하는 캐시 정책.

</details>

```text
[호스트 블록 쓰기]
        │
        ▼
1. 보호•복구 책임 판정
   ┌────┴──────────────┐
   │ RAID 컨트롤러     │ JBOD•SDS
   ▼                   ▼
2. 보호 캐시 기록   4. 개별 디스크 매핑
   │                   │
   ▼                   ▼
3. 데이터•패리티 배치 5. 소프트웨어 사본 배치
   │                   │
   └─────────┬─────────┘
              ▼
      [쓰기 완료 반환]
```

### 동작 원리

1. 보호·복구 책임 판정: 하드웨어 **RAID 컨트롤러** 중심 LUN 통합인지, **JBOD & SDS** 소프트웨어 분산 정책인지 결정.
2. 보호 캐시 기록: RAID 사용 시 전원 보호가 검증된 **Write-Back 캐시**에 데이터 기록.
3. 데이터·패리티 배치: HW **RAID Engine**을 이용한 패리티/미러 생성 후 물리 디스크 저장.
4. 개별 디스크 매핑: JBOD 사용 시 **Passthrough Controller**를 통해 디스크 디바이스 1:1 노출.
5. 소프트웨어 사본 배치: **SDS**가 노드·디스크 장애 영역에 따라 복제본이나 삭제 코딩 조각 배치.

#### 한줄 요약

- RAID 경로는 보호 캐시 기록과 데이터·패리티 배치, JBOD 경로는 개별 디스크 매핑과 소프트웨어 사본 배치를 사용한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **S.M.A.R.T**: 디스크의 에러율, 온도, 섹터 상태를 측정하는 자가 진단 메타데이터.

</details>

| 비교 항목 | HW RAID 컨트롤러 (Hardware RAID) | JBOD 패스스루 (Software-Defined) |
|:---|:---|:---|
| 중복성 관장 계층 | 전용 하드웨어 어댑터 칩셋 (LUN 가속) | 상위 **SDS** 커널/소프트웨어 (Ceph, vSAN) |
| 쓰기 속도/캐시 | **BBU/Flash 기반 Write-Back** 캐싱으로 고속 | 디스크 직결, SW 쓰기 캐시 및 네트워크 전달 오버헤드 |
| S.M.A.R.T 진단 | 컨트롤러·드라이버에 따라 OS 가시성 제약 | OS·SDS가 각 디스크 **S.M.A.R.T** 직접 수집 |
| 장애 범위 | 컨트롤러 장애가 연결 LUN에 영향 | **SDS** 정책에 따라 디스크·노드 장애를 복구 |

#### 한줄 요약

- RAID는 컨트롤러가 디스크를 재구성하고, JBOD 기반 SDS는 분산 계층이 사본을 재복제하여 중복도를 회복한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Dual RAID Controller**: 컨트롤러 장애(SPOF)에 대비하여 2개의 RAID 컨트롤러를 Active-Active/Active-Standby 구성하는 고가용성 설계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **JBOD** 경로의 동기 쓰기 지연 증가 | SDS가 지원하는 전용 로그·캐시 장치의 장애 의미 검증 | 동기 쓰기 지연과 복구 안전성 균형 |
| RAID 컨트롤러 고장 시 LUN 접근 중단 | **Dual RAID Controller**와 Multipathing 이중화 | 컨트롤러 단일 장애 경로 제거 |
| SDS에 HW RAID를 중복 적용해 장애 가시성 저하 | SDS 전용 장치는 **HBA/Passthrough Mode** 적용 | 디스크 상태 노출과 중복 정책 단일화 |

> 사례: 대규모 클라우드 인프라 상의 **JBOD 패스스루** 및 **Ceph SDS** 분산 스토리지 구축

#### 한줄 요약

- RAID는 보호 캐시 복구를, JBOD는 디스크 가시성과 SDS 복구 정책을 검증한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **스토리지 토폴로지 선택 기준(Storage Topology Selection Criteria)**: 단일 서버 vs 대규모 분산 스토리지, BBU 캐시 필요성, 비용 및 SDS 적용 여부에 따른 체계.

</details>

- **스토리지 토폴로지 선택 기준**에 따라 단일 DB 서버 부트/데이터 볼륨은 **HW RAID**, 대규모 클라우드 HCI는 **JBOD & SDS** 채택

#### 한줄 요약

- 단일 서버 보호는 HW RAID, 분산 복구 정책은 JBOD와 SDS를 선택한다.
