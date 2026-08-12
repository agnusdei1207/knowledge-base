---
sidebar:
  order: 157
  label: "157. 쿠버네티스 스토리지: PVC•PV•StorageClass (Kubernetes Storage)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "쿠버네티스 스토리지: PVC•PV•StorageClass (Kubernetes Storage)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 157
extra:
  question_no: "157"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "영속 볼륨의 요청•자원•정책 관계가 독립적임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **쿠버네티스 영속 스토리지(Persistent Storage)**: Pod 파기 후에도 데이터를 보존하기 위해 PVC(요청), PV(자원), StorageClass(자동 설정)로 추상화한 체계.
- **PVC (PersistentVolumeClaim)**: 스토리지 용량과 접근 모드 등을 명시하여 사용자(개발자)가 자원을 요청하는 객체.
- **PV (PersistentVolume)**: 실제 클라우드 EBS나 NFS 등 할당된 영속 스토리지 물리 자원.
- **StorageClass (SC)**: 관리자 설정에 따라 PVC 요청 시 특정 스토리지(AWS EBS `gp3` 등)를 자동 생성(Dynamic Provisioning)하는 규격 객체.

</details>

- 정의/개념: 가변적인 Pod와 하부 물리 스토리지(EBS, EFS, Ceph)를 분리하고 PVC, PV, StorageClass 객체를 통해 동적 프로비저닝(Dynamic Provisioning)을 제공하는 **Kubernetes Persistent Storage Architecture**
- 배경/필요성: Pod 재시작 시 컨테이너 내부 데이터 소멸(Ephemeral Storage) 방지, RDBMS DB/StatefulSet 앱의 영속성 보장 요구성

#### 한줄 요약

- 애플리케이션은 저장 제품을 직접 고르지 않고 PVC에 필요한 크기와 접근 방법만 적어 인프라 변경과 데이터 수명을 분리한다.

## Ⅱ. 특징 (스토리지 추상화 3대 메커니즘)

<details><summary>핵심 용어</summary>

- **Dynamic Provisioning**: 관리자가 일일이 PV 디스크를 만들어 두지 않아도, PVC 신청 즉시 StorageClass와 CSI 드라이버가 AWS EBS를 3초 만에 자동 생성.

</details>

- **스토리지 추상화**: PVC(요청)와 PV(자원)를 분리하여 애플리케이션 종속성 제거.
- **동적 프로비저닝(Dynamic Provisioning)**: StorageClass 기반 AWS EBS/EFS 실시간 자동 생성.
- **접근 모드 제어(Access Modes)**: RWO(ReadWriteOnce), ROX(ReadOnlyMany), RWX(ReadWriteMany) 권한 관리.

#### 한줄 요약

- PVC는 창고 요청서, PV는 배정된 창고, 스토리지 클래스는 창고를 만드는 표준으로 보면 세 객체의 책임이 구분된다.

## Ⅲ. 구조 및 구성요소 (Kubernetes Storage 3-Tier Layer 아키텍처)

<details><summary>핵심 용어</summary>

- **CSI (Container Storage Interface)**: K8s 코어 엔진과 외부 스토리지 벤더(AWS EBS, NetApp, Portworx) 간의 플러그인 호환 표준 규격.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                  Kubernetes Storage 3-Tier Architecture                │
├────────────────────────────────────────────────────────────────────────┤
│ [Stateful Pod] ──► [PVC Request (10GB RWO)]                            │
│                         │                                              │
│                         ▼                                              │
│ [StorageClass (gp3)] ──► [CSI Controller (AWS EBS Plugin)]             │
│                         │                                              │
│                         ▼                                              │
│ [PV (PersistentVolume)] ──► [Actual Physical Storage (AWS EBS Volume)] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Pod가 PVC를 요청하면 StorageClass와 CSI가 실제 AWS EBS 디스크(PV)를 자동으로 뚫어 마운트하는 구조.

| 객체/컴포넌트 | 관리 주체 | 핵심 역할 |
|:---|:---|:---|
| **PVC** | 개발자 | 스토리지 주문서 작성 |
| **StorageClass**| 관리자 | 프로비저닝 규격 지정 |
| **PV** | 시스템 | 실제 할당된 자원 실체 |
| **CSI Driver** | 벤더 | 볼륨 마운트/연결 수행 |

#### 한줄 요약

- 제어기가 PVC에 맞는 PV를 탐색하고 없으면 스토리지 클래스와 CSI로 새 PV를 동적 프로비저닝한 뒤 바인딩한다.

## Ⅳ. 흐름도 (Dynamic Provisioning & Volume Mount 4단계 흐름)

<details><summary>핵심 용어</summary>

- **VolumeBindingMode**: `WaitForFirstConsumer` 옵션을 설정하여, Pod가 실제 스케줄링된 동일 AZ(가용 영역)에 EBS 디스크를 뒤늦게 동적 생성하도록 보장하는 옵션.

</details>

```text
[Create PVC (10GB gp3)] ──► [StorageClass Calls AWS CSI Driver]
                                          │
                                          ▼
   [Pod Mounts EBS at /data] ◄── [PV Bound to PVC & Attach to Node] ◄── [Create AWS EBS Volume]
```

### 동작 원리

1. **PVC Request**: 개발자가 10GB `gp3` StorageClass 지정 PVC 적용.
2. **CSI Provision**: StorageClass가 AWS EBS CSI 드라이버를 호출해 AWS 콘솔 상에 10GB EBS 디스크 자동 생성.
3. **Bind & Mount**: 생성된 EBS 디스크가 PV 객체로 K8s에 등록되고 PVC와 1:1 Binding 된 후 Pod `/data` 디렉토리에 마운트 완결 (**Kubernetes Storage 완결**).

#### 한줄 요약

- 첫 소비자 대기를 사용하면 파드가 놓일 영역을 먼저 정하고 같은 영역에 볼륨을 만들어 지역 불일치로 인한 배치 실패를 막는다.

## Ⅴ. 종류 및 비교 (Access Modes 3대 접근 권한 1:1 비교)

<details><summary>핵심 용어</summary>

- **RWO vs RWX**: RWO(ReadWriteOnce)는 단 1개 Node만 읽기/쓰기 가능(EBS 디스크), RWX(ReadWriteMany)는 수십 개 Node가 동시 읽기/쓰기 가능(EFS NFS/S3).

</details>

| Access Mode | 약어 | 동시 접속 노드 수 | 대표 지원 스토리지 솔루션 |
|:---|:---|:---|:---|
| **ReadWriteOnce** | **RWO** | **단 1개 Node만 읽기/쓰기 단독 점유** | **AWS EBS, GCP Persistent Disk** |
| **ReadOnlyMany** | **ROX** | **수십 개 Node가 동시에 읽기(Read) 전용**| **AWS EBS Snapshot, ISO Image** |
| **ReadWriteMany** | **RWX** | **수십 개 Node가 동시에 읽기/쓰기 공유**| **AWS EFS (NFS), Ceph, GlusterFS** |

#### 한줄 요약

- PVC는 소비자의 요구, PV는 공급된 자원, 스토리지 클래스는 공급 방식을 나타내므로 저장 제품 변경을 파드 명세에서 숨길 수 있다.

## Ⅵ. 실무 고려사항 및 대책 (Kubernetes Storage 3대 장애 대책)

<details><summary>핵심 용어</summary>

- **Multi-AZ EBS Volume Attach Error**: AWS EBS 디스크는 특정 AZ(ap-northeast-2a)에 고정되므로, Pod가 타 AZ(2c)로 이사 가면 디스크 마운트 불가 500 에러 발생.

</details>

| 3대 스토리지 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Multi-AZ Multi-Attach Fail**| EBS 디스크와 Pod의 AZ 불일치 | **`volumeBindingMode: WaitForFirstConsumer` 설정** |
| **2. Multi-Pod Log Share Fail**| EBS(RWO)로는 여러 Pod가 로그 못 씀| **AWS EFS (RWX 수용 스토리지) 로 교체** |
| **3. Accidental PVC Deletion**| PVC 실수 삭제로 EBS 데이터 날아감 | **`reclaimPolicy: Retain` 으로 디스크 파기 방지** |

> 사례: **카카오 / 당근마켓 StatefulSet DB (EBS RWO + Retain Policy) 구축 운영**

#### 한줄 요약

- 데이터베이스 파드의 영역과 볼륨 영역을 맞추고 PVC 삭제와 별개인 백업을 복원해 봐야 노드 손실과 오삭제를 모두 견딜 수 있다.

## Ⅶ. 결론

- **영속 볼륨 기반 데이터 보존 체계 및 스토리지 동적 프로비저닝 최적화 구현**
